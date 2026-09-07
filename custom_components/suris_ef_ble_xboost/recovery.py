# SPDX-License-Identifier: Apache-2.0
# Suris additions/adaptations, 2026. See NOTICE for upstream attribution.
"""One early setup retry when a configured station is advertised again."""
from __future__ import annotations

from dataclasses import dataclass
import logging

from homeassistant.components import bluetooth
from homeassistant.config_entries import ConfigEntryState
from homeassistant.const import EVENT_HOMEASSISTANT_STOP
from homeassistant.core import CALLBACK_TYPE, HomeAssistant, callback

from ._vendor.eflib.devices.delta2_max import Device
from .const import CONF_ADDRESS, CONF_SERIAL_NUMBER, DOMAIN, normalize_address
from .driver import profile_from_service_info

_LOGGER = logging.getLogger(__name__)
DATA_BLE_RECOVERY = "ble_recovery"


@dataclass
class _Watch:
    address: str
    remove: CALLBACK_TYPE
    nudged: bool = False


class BleRecovery:
    """Observe HA's scanner without opening or replacing any BLE connections.

    This subscription belongs to the integration, not to one setup attempt:
    entry unload callbacks also run after failed setup, when we must keep
    listening. HA still owns all ordinary retries and connection teardown.
    """

    def __init__(self, hass: HomeAssistant):
        self.hass = hass
        self._watches: dict[str, _Watch] = {}
        self._remove_advertisements: CALLBACK_TYPE | None = None
        self._remove_stop: CALLBACK_TYPE | None = None
        self._closed = False

    @callback
    def start(self):
        self._remove_advertisements = bluetooth.async_register_callback(
            self.hass,
            self._advertised,
            {"manufacturer_id": Device.MANUFACTURER_KEY, "connectable": True},
            bluetooth.BluetoothScanningMode.PASSIVE,
            # An old cached advertisement is not evidence the station is back.
            replay=bluetooth.BluetoothCallbackReplay.DISABLED,
        )
        self._remove_stop = self.hass.bus.async_listen_once(
            EVENT_HOMEASSISTANT_STOP, self._stop
        )

    @callback
    def _advertised(self, info, _change):
        if self._closed or self.hass.is_stopping or not info.connectable:
            return
        profile = profile_from_service_info(info)
        if profile is None:
            return
        entry = self.hass.config_entries.async_entry_for_domain_unique_id(
            DOMAIN, profile[CONF_SERIAL_NUMBER]
        )
        if (
            entry is None
            or entry.disabled_by is not None
            or entry.data.get(CONF_SERIAL_NUMBER) != profile[CONF_SERIAL_NUMBER]
            or normalize_address(entry.data.get(CONF_ADDRESS, "")) != profile[CONF_ADDRESS]
        ):
            return

        watch = self._watches.get(entry.entry_id)
        if watch is None or watch.address != profile[CONF_ADDRESS]:
            self.remove_entry(entry.entry_id)

            @callback
            def unavailable(_info):
                # Only a new disappearance/reappearance arms another early retry.
                # A failed connect with ongoing advertisements keeps HA's backoff.
                if not self._closed and (current := self._watches.get(entry.entry_id)):
                    current.nudged = False

            watch = self._watches[entry.entry_id] = _Watch(
                profile[CONF_ADDRESS],
                bluetooth.async_track_unavailable(
                    self.hass, unavailable, profile[CONF_ADDRESS], connectable=True
                ),
            )

        # Leave loaded, disabled, authenticating and unloading entries alone.
        # This also avoids replacing an actual authentication failure with retries.
        if entry.state is not ConfigEntryState.SETUP_RETRY or watch.nudged:
            return
        watch.nudged = True
        _LOGGER.info("Station rediscovered while waiting; scheduling one BLE reconnect")
        # HA cancels the pending retry and serializes setup through its entry lock.
        self.hass.config_entries.async_schedule_reload(entry.entry_id)

    @callback
    def remove_entry(self, entry_id: str):
        if watch := self._watches.pop(entry_id, None):
            watch.remove()

    @callback
    def _stop(self, _event):
        self.close()

    @callback
    def close(self):
        if self._closed:
            return
        self._closed = True
        if self._remove_advertisements:
            self._remove_advertisements()
        if self._remove_stop:
            self._remove_stop()
        for entry_id in tuple(self._watches):
            self.remove_entry(entry_id)
