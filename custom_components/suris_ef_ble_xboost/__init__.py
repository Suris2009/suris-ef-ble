# SPDX-License-Identifier: Apache-2.0
# Suris additions/adaptations, 2026. See NOTICE for upstream attribution.
# This is an independently modified, unofficial integration.
"""Standalone Suris EcoFlow BLE integration for DELTA 2 Max + Extra Battery 1."""
from __future__ import annotations

import asyncio
import logging

from homeassistant.components import bluetooth
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import EVENT_HOMEASSISTANT_STOP, Platform
from homeassistant.core import callback
from homeassistant.exceptions import ConfigEntryAuthFailed, ConfigEntryNotReady

from .const import (
    AUTH_SOURCE, CONF_ADDRESS, CONF_AUTH_SOURCE, CONF_BATTERY_SEEN, CONF_SERIAL_NUMBER,
    CONF_USER_ID, DOMAIN, normalize_address, same_device, valid_serial, valid_user_id,
)
from .driver import connect_device, create_device, disconnect_device, profile_from_service_info
from .recovery import DATA_BLE_RECOVERY, BleRecovery
from .registry import async_merge_duplicates, async_prepare_registry, recover_own_serial
from .runtime import SurisRuntime

_LOGGER = logging.getLogger(__name__)
PLATFORMS = [Platform.SENSOR, Platform.SWITCH, Platform.NUMBER, Platform.SELECT]
type SurisConfigEntry = ConfigEntry[SurisRuntime]


async def async_setup(hass, config):
    """Keep the recovery listener alive while entries wait for setup retries."""
    data = hass.data.setdefault(DOMAIN, {})
    if DATA_BLE_RECOVERY not in data:
        recovery = BleRecovery(hass)
        recovery.start()
        data[DATA_BLE_RECOVERY] = recovery
    return True


async def async_remove_entry(hass, entry: SurisConfigEntry):
    if recovery := hass.data.get(DOMAIN, {}).get(DATA_BLE_RECOVERY):
        recovery.remove_entry(entry.entry_id)


async def async_setup_entry(hass, entry: SurisConfigEntry):
    peers = [e for e in hass.config_entries.async_entries(DOMAIN) if same_device(entry.data, e.data) and e.disabled_by is None]
    canonical = min(peers, key=lambda e: (not valid_user_id(e.data.get(CONF_USER_ID)), e.created_at, e.entry_id), default=entry)
    if canonical.entry_id != entry.entry_id:
        hass.config_entries.async_schedule_reload(canonical.entry_id)
        raise ConfigEntryNotReady("Merging a duplicate Suris entry")
    if not valid_user_id(entry.data.get(CONF_USER_ID)):
        raise ConfigEntryAuthFailed("Enter an EcoFlow login or your own User ID in Suris")
    if not valid_serial(entry.data.get(CONF_SERIAL_NUMBER)) or not entry.data.get(CONF_ADDRESS):
        raise ConfigEntryAuthFailed("Select your DELTA 2 Max and authenticate in Suris")
    if not await async_merge_duplicates(hass, entry):
        raise ConfigEntryNotReady("Waiting for another Suris entry to unload")
    if entry.unique_id != entry.data[CONF_SERIAL_NUMBER]:
        hass.config_entries.async_update_entry(entry, unique_id=entry.data[CONF_SERIAL_NUMBER])

    device = create_device(hass, entry.data)
    runtime = SurisRuntime(hass, entry, device)
    entry.runtime_data = runtime
    platforms_started = False
    try:
        await connect_device(device, entry.data[CONF_USER_ID])
        if entry.data.get(CONF_AUTH_SOURCE) != AUTH_SOURCE:
            hass.config_entries.async_update_entry(entry, data={**entry.data, CONF_AUTH_SOURCE: AUTH_SOURCE})
        async_prepare_registry(hass, entry, runtime)
        # Register disconnect handling before forwarding: a drop during platform setup
        # must not leave an apparently loaded entry with no recovery listener.
        @callback
        def on_disconnect(exc=None):
            def schedule():
                if runtime.closed or hass.is_stopping or runtime.reload_scheduled:
                    return
                runtime.reload_scheduled = True
                hass.config_entries.async_schedule_reload(entry.entry_id)
            runtime._in_loop(schedule)

        runtime.add_remover(device.on_disconnect(on_disconnect))
        platforms_started = True
        await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
        if not runtime.authenticated:
            raise ConfigEntryNotReady("Device disconnected during platform setup")
        runtime.ready = True
        runtime._queue_update()

        async def stop(_event):
            runtime.close()
            await disconnect_device(device)

        runtime.add_remover(hass.bus.async_listen_once(EVENT_HOMEASSISTANT_STOP, stop))
        entry.async_on_unload(runtime.close)
        # Remove already pending discovery cards using the same identity as setup.
        for flow in tuple(hass.config_entries.flow.async_progress_by_handler(DOMAIN)):
            context = flow.get("context", {})
            if context.get("source") == "bluetooth" and context.get("unique_id") in (entry.data[CONF_SERIAL_NUMBER], entry.data[CONF_ADDRESS]):
                hass.config_entries.flow.async_abort(flow["flow_id"])
        return True
    except BaseException:
        runtime.close()
        try:
            if platforms_started:
                await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
        finally:
            await disconnect_device(device)
            entry.runtime_data = None
        raise


async def async_unload_entry(hass, entry: SurisConfigEntry):
    if not await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        return False
    runtime = getattr(entry, "runtime_data", None)
    if runtime is not None:
        runtime.close()
        await disconnect_device(runtime.device)
        entry.runtime_data = None
    return True


async def async_migrate_entry(hass, entry: SurisConfigEntry):
    if entry.version > 3:
        return False
    if entry.version == 3:
        return True
    old = dict(entry.data)
    data = {key: old[key] for key in (CONF_ADDRESS, CONF_SERIAL_NUMBER, CONF_BATTERY_SEEN) if old.get(key)}
    if CONF_ADDRESS in data:
        data[CONF_ADDRESS] = normalize_address(data[CONF_ADDRESS])
    if not valid_serial(data.get(CONF_SERIAL_NUMBER)) and (serial := recover_own_serial(hass, entry)):
        data[CONF_SERIAL_NUMBER] = serial
    # Only the entry's own ID can be considered. Parent-backed alpha entries had
    # copied credentials with no provenance and must go through explicit reauth.
    own_id = str(old.get(CONF_USER_ID, "")).strip()
    if not old.get("ef_ble_entry_id") and valid_user_id(own_id):
        data[CONF_USER_ID] = own_id
    if not data.get(CONF_ADDRESS) and data.get(CONF_SERIAL_NUMBER):
        for info in bluetooth.async_discovered_service_info(hass, connectable=True):
            profile = profile_from_service_info(info)
            if profile and profile[CONF_SERIAL_NUMBER] == data[CONF_SERIAL_NUMBER]:
                data.update(profile)
                break
    data["enable_sensor_migration"] = True
    kwargs = {"version": 3, "minor_version": 0, "data": data, "options": {}, "pref_disable_new_entities": False}
    if data.get(CONF_SERIAL_NUMBER) and not any(
        e.entry_id != entry.entry_id and e.unique_id == data[CONF_SERIAL_NUMBER]
        for e in hass.config_entries.async_entries(DOMAIN)
    ):
        kwargs["unique_id"] = data[CONF_SERIAL_NUMBER]
    hass.config_entries.async_update_entry(entry, **kwargs)
    return True
