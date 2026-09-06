# SPDX-License-Identifier: Apache-2.0
# Suris additions/adaptations, 2026. See NOTICE for upstream attribution.
# This is an independently modified, unofficial integration.
"""Entry-owned telemetry buffer and subscriptions, including late BMS discovery."""
from __future__ import annotations

import asyncio
from collections.abc import Callable
from functools import partial

from homeassistant.core import callback

from .const import CONF_BATTERY_SEEN


class SurisRuntime:
    def __init__(self, hass, entry, device):
        self.hass, self.entry, self.device = hass, entry, device
        self.raw: dict[str, object] = {}
        self.battery_seen = bool(entry.data.get(CONF_BATTERY_SEEN))
        self.battery_live = False
        self.closed = False
        self.ready = False
        self.reload_scheduled = False
        self.generation = 0
        self.main_device_id = None
        self.battery_device_id = None
        self._listeners: set[Callable] = set()
        self._pending = None
        self._removers = [
            device.on_message_processed(self._raw_received),
            device.on_connection_state_change(self._state_received),
        ]
        for field in device._fields:
            prop = field.public_name
            device.register_callback(self._property_updated, prop)
            self._removers.append(partial(device.remove_callback, self._property_updated, prop))

    def _property_updated(self):
        self._in_loop(self._queue_update)

    @property
    def authenticated(self):
        return not self.closed and self.device.is_connected and bool(getattr(self.device.connection_state, "authenticated", False))

    def _in_loop(self, func, *args):
        if self.closed:
            return
        try:
            in_loop = asyncio.get_running_loop() is self.hass.loop
        except RuntimeError:
            in_loop = False
        if in_loop:
            func(*args)
        else:
            self.hass.loop.call_soon_threadsafe(func, *args)

    def _raw_received(self, message):
        self._in_loop(self._accept_raw, message)

    @callback
    def _accept_raw(self, message):
        if self.closed:
            return
        name = type(message).__name__
        self.raw[name] = message
        if name == "_BmsHeartbeatBattery1" and getattr(message, "vol", None) is not None:
            self.battery_seen = True
            self.battery_live = True
        elif name == "AllKitDetailData":
            kits = getattr(message, "kit_base_info", ())
            if kits and kits[0].avai_flag == 0:
                self.battery_live = False
        # Queue after the complete packet parser has notified its properties.
        self._queue_update()

    def _state_received(self, state):
        self._in_loop(self._accept_state, state)

    @callback
    def _accept_state(self, state):
        if self.closed:
            return
        if not state.authenticated:
            self.generation += 1
            self.raw.clear()
            self.battery_live = False
        self._queue_update()

    @callback
    def _queue_update(self):
        if self._pending is None and not self.closed:
            self._pending = self.hass.loop.call_soon(self._dispatch)

    @callback
    def _dispatch(self):
        self._pending = None
        if self.closed:
            return
        if self.ready and self.battery_seen and not self.entry.data.get(CONF_BATTERY_SEEN):
            self.hass.config_entries.async_update_entry(self.entry, data={**self.entry.data, CONF_BATTERY_SEEN: True})
        for listener in tuple(self._listeners):
            listener()

    def subscribe(self, listener):
        self._listeners.add(listener)
        return lambda: self._listeners.discard(listener)

    def raw_value(self, message_type, field):
        return getattr(self.raw.get(message_type), field, None)

    @callback
    def close(self):
        self.closed = True
        self.generation += 1
        if self._pending:
            self._pending.cancel()
            self._pending = None
        for remove in self._removers:
            remove()
        self._removers.clear()
        self._listeners.clear()
        self.raw.clear()

    def add_remover(self, remove):
        self._removers.append(remove)
