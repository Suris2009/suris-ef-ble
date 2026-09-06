# SPDX-License-Identifier: Apache-2.0
# Suris additions/adaptations, 2026. See NOTICE for upstream attribution.
# This is an independently modified, unofficial integration.
"""Suris-only identities; lifecycle subscriptions are owned by each entity."""
from homeassistant.core import callback
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity import Entity

from .const import DOMAIN


class SurisEntity(Entity):
    _attr_should_poll = False
    _attr_has_entity_name = True
    _attr_entity_registry_enabled_default = True
    _attr_entity_registry_visible_default = True

    def __init__(self, runtime, key, name, *, battery=False, custom=False):
        self.runtime = runtime
        self._device = runtime.device
        self.key = key
        self.battery = battery
        self._attr_name = name
        serial = self._device.serial_number
        self._attr_unique_id = f"suris_ef_ble_{key}_{serial}" if custom else f"ef_{serial}_{key}"

    @property
    def device_info(self):
        serial = self._device.serial_number
        info = DeviceInfo(
            identifiers={(DOMAIN, f"{serial}:battery_1" if self.battery else serial)},
            name=f"{self._device.name} Extra Battery 1" if self.battery else self._device.name,
            manufacturer="EcoFlow",
            model="DELTA 2 Max Smart Extra Battery" if self.battery else "DELTA 2 Max",
        )
        if self.battery:
            info["via_device_id"] = self.runtime.main_device_id
            if sn := getattr(self._device, "battery_1_sn", None):
                info["serial_number"] = sn.strip("\x00")
        else:
            info["serial_number"] = serial
        return info

    @property
    def available(self):
        return self.runtime.authenticated and (not self.battery or self.runtime.battery_live)

    async def async_added_to_hass(self):
        await super().async_added_to_hass()
        self.async_on_remove(self.runtime.subscribe(self._updated))

    @callback
    def _updated(self):
        self.async_write_ha_state()
