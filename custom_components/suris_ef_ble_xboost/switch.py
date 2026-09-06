# SPDX-License-Identifier: Apache-2.0
# Suris additions/adaptations, 2026. See NOTICE for upstream attribution.
# This is an independently modified, unofficial integration.
"""All upstream switches and the existing Suris X-Boost packet."""
from homeassistant.components.switch import SwitchDeviceClass, SwitchEntity
from homeassistant.exceptions import HomeAssistantError

from ._vendor.eflib.entity import controls
from ._vendor.eflib.packet import Packet
from .entity import SurisEntity

SWITCH_NAMES = {"ac_ports": "AC Ports", "dc_12v_port": "DC 12V Port", "usb_ports": "USB Ports", "energy_backup": "Backup Reserve"}


async def async_setup_entry(hass, entry, async_add_entities):
    runtime = entry.runtime_data
    async_add_entities([SurisSwitch(runtime, control) for control in runtime.device.get_controls(controls.toggle)] + [EcoFlowXBoostSwitch(runtime)])


class SurisSwitch(SurisEntity, SwitchEntity):
    def __init__(self, runtime, control):
        self.control = control
        super().__init__(runtime, control.key, SWITCH_NAMES[control.key])
        self._attr_device_class = SwitchDeviceClass.OUTLET if isinstance(control, controls.outlet) else SwitchDeviceClass.SWITCH

    @property
    def is_on(self):
        return getattr(self._device, self.key, None)

    async def _set(self, enabled):
        if not self.available:
            raise HomeAssistantError("Delta 2 Max is not connected and authenticated")
        await self.control.enable_func(self._device, enabled)

    async def async_turn_on(self, **kwargs):
        await self._set(True)

    async def async_turn_off(self, **kwargs):
        await self._set(False)


class EcoFlowXBoostSwitch(SurisEntity, SwitchEntity):
    _attr_icon = "mdi:lightning-bolt"
    _attr_device_class = SwitchDeviceClass.SWITCH

    def __init__(self, runtime):
        super().__init__(runtime, "xboost", "X-Boost", custom=True)

    @property
    def is_on(self):
        value = self.runtime.raw_value("DirectInvDeltaHeartbeatPack", "cfg_ac_xboost")
        return bool(value) if value in (0, 1) else None

    async def async_turn_on(self, **kwargs):
        await self._set_xboost(True)

    async def async_turn_off(self, **kwargs):
        await self._set_xboost(False)

    async def _set_xboost(self, enabled):
        if not self.available:
            raise HomeAssistantError("Delta 2 Max is not connected and authenticated")
        payload = bytes([0xFF, 0x01 if enabled else 0x00, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF])
        packet = Packet(0x21, self._device.ac_commands_dst, 0x20, 0x42, payload, version=0x02)
        await self._device.send_packet(packet, raise_on_failure=True)
