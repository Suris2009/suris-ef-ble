# SPDX-License-Identifier: Apache-2.0
# Suris additions/adaptations, 2026. See NOTICE for upstream attribution.
# This is an independently modified, unofficial integration.
"""Migrate only Suris-owned entries/devices/entities through public HA APIs."""
from __future__ import annotations

from homeassistant.core import callback
from homeassistant.helpers import device_registry as dr, entity_registry as er

from .const import CONF_BATTERY_SEEN, CONF_SERIAL_NUMBER, DOMAIN, same_device, valid_serial


def is_battery_entity(unique_id):
    return "_battery_1_" in unique_id or "_slave_1_" in unique_id or "_slave1_" in unique_id


def _is_second_battery(unique_id):
    return "_battery_2_" in unique_id or "_slave_2_" in unique_id


@callback
def recover_own_serial(hass, entry):
    """0.7 entries stored only a parent ID; own entity unique IDs retain the SN."""
    serials = set()
    for entity in er.async_entries_for_config_entry(er.async_get(hass), entry.entry_id):
        if entity.platform != DOMAIN:
            continue
        for part in entity.unique_id.split("_"):
            if valid_serial(part):
                serials.add(part)
    return next(iter(serials)) if len(serials) == 1 else None


@callback
def _owned_devices(hass, entry):
    return dr.async_entries_for_config_entry(dr.async_get(hass), entry.entry_id)


@callback
def async_prepare_registry(hass, entry, runtime):
    """Preserve old device IDs when unambiguously owned, then relink all own entities."""
    registry, entities = dr.async_get(hass), er.async_get(hass)
    serial = runtime.device.serial_number
    main_identifier = (DOMAIN, serial)
    battery_identifier = (DOMAIN, f"{serial}:battery_1")
    owned = list(_owned_devices(hass, entry))
    own_entities = list(er.async_entries_for_config_entry(entities, entry.entry_id))
    main = registry.async_get_device_by_identifier(main_identifier, entry.entry_id)
    if main is None:
        candidates = [d for d in owned if not any("battery_" in i[1] or "slave_" in i[1] for i in d.identifiers)]
        if len(candidates) == 1:
            main = registry.async_update_device(candidates[0].id, new_identifiers={main_identifier}, new_connections=set(), via_device_id=None)
    main = registry.async_get_or_create(
        config_entry_id=entry.entry_id, identifiers={main_identifier}, connections=set(),
        manufacturer="EcoFlow", model="DELTA 2 Max", name=runtime.device.name, serial_number=serial,
    )
    runtime.main_device_id = main.id
    for old in owned:
        if old.id == main.id:
            continue
        if any("battery_1" in ident[1] for ident in old.identifiers):
            existing = registry.async_get_device_by_identifier(battery_identifier, entry.entry_id)
            if existing is None:
                registry.async_update_device(old.id, new_identifiers={battery_identifier}, new_connections=set(), via_device_id=main.id)
                runtime.battery_seen = True
    if any(is_battery_entity(e.unique_id) for e in own_entities):
        runtime.battery_seen = True
    if runtime.battery_seen:
        async_ensure_battery_device(hass, entry, runtime)
    if entry.data.get("enable_sensor_migration", False):
        for device_id in (runtime.main_device_id, runtime.battery_device_id):
            if device_id and (owned_device := registry.async_get(device_id)) and owned_device.disabled_by is not None:
                registry.async_update_device(device_id, disabled_by=None)
    for entity in own_entities:
        if entity.platform != DOMAIN:
            continue
        if _is_second_battery(entity.unique_id):
            entities.async_remove(entity.entity_id)
            continue
        target = runtime.battery_device_id if is_battery_entity(entity.unique_id) else main.id
        updates = {}
        if entity.device_id != target:
            updates["device_id"] = target
        if entity.domain == "sensor":
            # Explicit user requirement: re-enable even previously manually disabled sensors.
            # This migration runs once for old entries, not on every later reload.
            if entry.data.get("enable_sensor_migration", False):
                if entity.disabled_by is not None:
                    updates["disabled_by"] = None
                if entity.hidden_by is not None:
                    updates["hidden_by"] = None
            if entity.entity_category is not None:
                updates["entity_category"] = None
        if updates:
            entities.async_update_entity(entity.entity_id, **updates)
    keep = {runtime.main_device_id, runtime.battery_device_id}
    for old in list(_owned_devices(hass, entry)):
        if old.id not in keep and not er.async_entries_for_device(entities, old.id, include_disabled_entities=True):
            registry.async_remove_device(old.id)
    if entry.data.get("enable_sensor_migration"):
        data = dict(entry.data)
        data.pop("enable_sensor_migration", None)
        hass.config_entries.async_update_entry(entry, data=data, pref_disable_new_entities=False)


@callback
def async_ensure_battery_device(hass, entry, runtime):
    registry = dr.async_get(hass)
    kwargs = {}
    if sn := getattr(runtime.device, "battery_1_sn", None):
        kwargs["serial_number"] = sn.strip("\x00")
    battery = registry.async_get_or_create(
        config_entry_id=entry.entry_id,
        identifiers={(DOMAIN, f"{runtime.device.serial_number}:battery_1")},
        connections=set(), name=f"{runtime.device.name} Extra Battery 1", manufacturer="EcoFlow",
        model="DELTA 2 Max Smart Extra Battery", via_device_id=runtime.main_device_id, **kwargs,
    )
    runtime.battery_device_id = battery.id


async def async_merge_duplicates(hass, entry):
    peers = [e for e in hass.config_entries.async_entries(DOMAIN) if e.entry_id != entry.entry_id and same_device(entry.data, e.data)]
    registry = er.async_get(hass)
    for duplicate in peers:
        if not await hass.config_entries.async_unload(duplicate.entry_id):
            return False
        for entity in list(er.async_entries_for_config_entry(registry, duplicate.entry_id)):
            if entity.platform == DOMAIN:
                registry.async_update_entity(entity.entity_id, config_entry_id=entry.entry_id, device_id=None)
        await hass.config_entries.async_remove(duplicate.entry_id)
    return True
