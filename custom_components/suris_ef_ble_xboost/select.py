# SPDX-License-Identifier: Apache-2.0
# Suris additions/adaptations, 2026. See NOTICE for upstream attribution.
# This is an independently modified, unofficial integration.
"""Existing paired 0x47 Car Input command with one entry-owned async lock."""
import asyncio

from homeassistant.components.select import SelectEntity
from homeassistant.exceptions import HomeAssistantError

from ._vendor.eflib.packet import Packet
from .entity import SurisEntity

CURRENT_TO_OPTION = {4000: "4 A", 6000: "6 A", 8000: "8 A"}
OPTION_TO_CURRENT = {v: k for k, v in CURRENT_TO_OPTION.items()}


async def async_setup_entry(hass, entry, async_add_entities):
    state = EcoFlowCarInputCurrentState(entry.runtime_data)
    entry.async_on_unload(state.close)
    async_add_entities([EcoFlowCarInputCurrentSelect(state, i) for i in (1, 2)])


class EcoFlowCarInputCurrentState:
    def __init__(self, runtime):
        self.runtime = runtime
        self.currents = [None, None]
        self._last_message = None
        self._write_lock = asyncio.Lock()
        self._generation = runtime.generation
        self.closed = False
        self._remove = runtime.subscribe(self.update)
        self.update()

    def update(self):
        if self.closed:
            return
        if self._generation != self.runtime.generation:
            self._generation = self.runtime.generation
            self.currents = [None, None]
            self._last_message = None
        if not self.runtime.authenticated:
            self.currents = [None, None]
            self._last_message = None
            return
        message = self.runtime.raw.get("Mr350MpptHeart")
        if message is None or message is self._last_message:
            return
        self._last_message = message
        reserved = getattr(message, "res", None)
        input_2 = int.from_bytes(reserved[:4], "little") if isinstance(reserved, bytes) and len(reserved) >= 4 else None
        self.currents = [getattr(message, "cfg_dc_chg_current", None), input_2]

    @property
    def available(self):
        self.update()
        return not self.closed and self.runtime.authenticated and all(v in CURRENT_TO_OPTION for v in self.currents)

    def close(self):
        self.closed = True
        self.currents = [None, None]
        self._remove()

    async def set_current(self, input_index, current):
        if input_index not in (0, 1) or current not in CURRENT_TO_OPTION:
            raise HomeAssistantError("Unsupported car input current")
        async with self._write_lock:
            if not self.available:
                raise HomeAssistantError("Wait for fresh, valid limits for BOTH car inputs after connecting")
            generation = self.runtime.generation
            new_currents = self.currents.copy()
            new_currents[input_index] = current
            payload = b"".join(value.to_bytes(4, "little") for value in new_currents)
            packet = Packet(0x21, 0x05, 0x20, 0x47, payload, version=0x02)
            await self.runtime.device.send_packet(packet, raise_on_failure=True)
            if self.closed or generation != self.runtime.generation or not self.runtime.authenticated:
                raise HomeAssistantError("Connection changed during the write; wait for fresh device data")
            self.currents = new_currents
            self.runtime._queue_update()


class EcoFlowCarInputCurrentSelect(SurisEntity, SelectEntity):
    _attr_icon = "mdi:current-dc"
    _attr_options = list(OPTION_TO_CURRENT)

    def __init__(self, state, input_number):
        self._state = state
        self.input_index = input_number - 1
        super().__init__(state.runtime, f"car_input_{input_number}_current", f"Car Input {input_number} Current", custom=True)

    @property
    def available(self):
        return self._state.available

    @property
    def current_option(self):
        self._state.update()
        return CURRENT_TO_OPTION.get(self._state.currents[self.input_index])

    async def async_select_option(self, option):
        if option not in OPTION_TO_CURRENT:
            raise HomeAssistantError("Unsupported car input current")
        await self._state.set_current(self.input_index, OPTION_TO_CURRENT[option])
