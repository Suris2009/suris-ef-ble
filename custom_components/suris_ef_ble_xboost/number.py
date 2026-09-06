# SPDX-License-Identifier: Apache-2.0
# Suris additions/adaptations, 2026. See NOTICE for upstream attribution.
# This is an independently modified, unofficial integration.
"""Upstream decorated number controls, retaining dynamic limits and commands."""
from homeassistant.components.number import NumberDeviceClass, NumberEntity
from homeassistant.exceptions import HomeAssistantError

from ._vendor.eflib.entity import controls
from ._vendor.eflib.entity.base import DynamicValue
from .entity import SurisEntity

NUMBER_NAMES = {"battery_charge_limit_max": "Max Charge Limit", "battery_charge_limit_min": "Min Discharge Limit", "energy_backup_battery_level": "Energy Backup Level", "ac_charging_speed": "AC Charging Speed"}


async def async_setup_entry(hass, entry, async_add_entities):
    runtime = entry.runtime_data
    async_add_entities([SurisNumber(runtime, control) for control in runtime.device.get_controls(controls.NumberType)])


class SurisNumber(SurisEntity, NumberEntity):
    def __init__(self, runtime, control):
        self.control = control
        super().__init__(runtime, control.key, NUMBER_NAMES[control.key])
        self._attr_native_step = control.step
        self._attr_native_unit_of_measurement = "W" if isinstance(control, controls.power) else "%"
        if isinstance(control, controls.power):
            self._attr_device_class = NumberDeviceClass.POWER

    def _limit(self, limit, fallback):
        value = limit.resolve(self._device) if isinstance(limit, DynamicValue) else limit
        return fallback if value is None else value

    @property
    def native_min_value(self):
        return self._limit(self.control.min, 0)

    @property
    def native_max_value(self):
        return self._limit(self.control.max, 100)

    @property
    def native_value(self):
        return getattr(self._device, self.key, None)

    @property
    def available(self):
        if not super().available:
            return False
        return not self.control.availability_prop or bool(getattr(self._device, self.control.availability_prop, False))

    async def async_set_native_value(self, value):
        if not self.available:
            raise HomeAssistantError("Delta 2 Max control is unavailable")
        if not self.native_min_value <= value <= self.native_max_value:
            raise HomeAssistantError("Value is outside the current device limits")
        await self.control.set_value_func(self._device, value)
