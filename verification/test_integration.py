# SPDX-License-Identifier: Apache-2.0
# Suris additions/adaptations, 2026. See NOTICE for upstream attribution.
# This is an independently modified, unofficial integration.
"""Offline regression tests using actual Home Assistant 2026.9 APIs.

Transport/cloud and selected setup calls are mocked; core HA classes are real.
Synthetic packets do not prove hardware behavior.
"""
import asyncio
import importlib
import json
import logging
import struct
from dataclasses import fields
from datetime import timedelta
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import AsyncMock, Mock, patch

import pytest
import pytest_asyncio
from bleak.backends.device import BLEDevice
from bleak.backends.scanner import AdvertisementData
from homeassistant.config_entries import ConfigEntries, ConfigEntry, ConfigEntryState
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryAuthFailed, ConfigEntryNotReady, HomeAssistantError
from homeassistant.helpers import device_registry as dr, entity_registry as er, issue_registry as ir
from homeassistant.helpers.entity_platform import EntityPlatform

from custom_components.suris_ef_ble_xboost import async_migrate_entry, async_setup_entry, async_unload_entry
from custom_components.suris_ef_ble_xboost import driver
from custom_components.suris_ef_ble_xboost.const import DOMAIN
from custom_components.suris_ef_ble_xboost.config_flow import SurisEcoFlowBleXBoostConfigFlow
from custom_components.suris_ef_ble_xboost.entity import SurisEntity
from custom_components.suris_ef_ble_xboost.registry import async_prepare_registry, async_merge_duplicates
from custom_components.suris_ef_ble_xboost.runtime import SurisRuntime
from custom_components.suris_ef_ble_xboost.sensor import MAIN_SENSORS, BATTERY_SENSORS, SurisSensor
from custom_components.suris_ef_ble_xboost.select import EcoFlowCarInputCurrentState
from custom_components.suris_ef_ble_xboost._vendor.eflib.connection import Connection, ConnectionState
from custom_components.suris_ef_ble_xboost._vendor.eflib.devices.delta2_max import Device
from custom_components.suris_ef_ble_xboost._vendor.eflib.devices._delta2_base import _BmsHeartbeatBattery1
from custom_components.suris_ef_ble_xboost._vendor.eflib.entity import controls
from custom_components.suris_ef_ble_xboost._vendor.eflib.model import Mr350MpptHeart, DirectBmsMDeltaHeartbeatPack
from custom_components.suris_ef_ble_xboost._vendor.eflib.packet import Packet

SN = 'R351TEST00000001'
ADDRESS = 'AA:BB:CC:DD:EE:FF'
PROFILE = {'address': ADDRESS, 'serial_number': SN}


@pytest_asyncio.fixture
async def hass(tmp_path):
    h = HomeAssistant(str(tmp_path))
    h.config_entries = ConfigEntries(h, {})
    await h.config_entries.async_initialize()
    await ir.async_load(h)
    dr.async_setup(h)
    await dr.async_load(h, load_empty=True)
    await er.async_load(h, load_empty=True)
    yield h
    await h.async_stop(force=True)


async def add_entry(hass, data=None, *, version=3, unique_id=SN, domain=DOMAIN):
    entry = ConfigEntry(data=data if data is not None else {**PROFILE, 'user_id': '12345678'},
        domain=domain, version=version, minor_version=0, title='Test', source='user',
        unique_id=unique_id, options={}, discovery_keys={}, subentries_data=[])
    with patch.object(hass.config_entries, 'async_setup', AsyncMock(return_value=True)):
        await hass.config_entries.async_add(entry)
    return entry


def service_info(*, address=ADDRESS, serial=SN, length=23):
    raw = (b'\x13' + serial.encode() + b'\0'*6)[:length]
    dev = BLEDevice(address, 'EF-R35TEST', {})
    adv = AdvertisementData('EF-R35TEST', {46517: raw}, {}, [], None, -50, ())
    return SimpleNamespace(address=address, manufacturer_data=adv.manufacturer_data, device=dev, advertisement=adv)


def device(connected=True):
    info = service_info()
    dev = Device(info.device, info.advertisement, SN)
    if connected:
        dev._conn = SimpleNamespace(is_connected=True, _connection_state=ConnectionState.AUTHENTICATED)
    return dev


def payload(cls, **values):
    values_list = []
    for field, fmt in zip(fields(cls), cls._FULL_STRUCT_FMT[1:], strict=True):
        default = bytes(int(fmt[:-1] or 1)) if fmt.endswith('s') else (0.0 if fmt in ('f', 'd') else 0)
        values_list.append(values.get(field.name, default))
    return struct.pack(cls._STRUCT_FMT, *values_list)


async def bms_packet(dev):
    data = payload(_BmsHeartbeatBattery1, vol=52000, f32_show_soc=72.5, max_cell_temp=30,
        max_cell_vol=3337, min_cell_vol=3320, cycles=11, input_watts=80, output_watts=30)
    await dev.data_parse(Packet(0x06, 0x21, 0x20, 0x32, data, version=2))


def flow(hass, source='user'):
    f = SurisEcoFlowBleXBoostConfigFlow()
    f.hass = hass
    f.handler = DOMAIN
    f.context = {'source': source}
    return f


@pytest.mark.asyncio
async def test_inventory_matches_real_upstream(hass):
    entry = await add_entry(hass)
    runtime = SurisRuntime(hass, entry, device())
    upstream = json.loads(Path('audit/upstream_inventory.json').read_text())
    assert {s.key for s in MAIN_SENSORS if not s.custom} == {s['key'] for s in upstream['_SENSORS']}
    assert {s['key'] for s in upstream['_BATTERY_ADDON_SENSORS']} <= {s.key for s in BATTERY_SENSORS}
    assert {s.field for s in BATTERY_SENSORS if s.field != 'difference'} == {f.name for f in fields(DirectBmsMDeltaHeartbeatPack)}
    assert len(MAIN_SENSORS) == 37 and len(BATTERY_SENSORS) == 29
    assert len(runtime.device.get_controls(controls.toggle)) == 4
    assert len(runtime.device.get_controls(controls.NumberType)) == 4
    for kind in (controls.select, controls.button, controls.climate):
        assert runtime.device.get_controls(kind) == []
    entities = [SurisSensor(runtime, spec) for spec in MAIN_SENSORS + BATTERY_SENSORS]
    assert len({e.unique_id for e in entities}) == len(entities)
    assert all(e.entity_registry_enabled_default and e.entity_registry_visible_default for e in entities)
    assert all(e.entity_category is None for e in entities)
    assert all('battery_2' not in e.unique_id for e in entities)
    runtime.close()


@pytest.mark.asyncio
async def test_login_choice_and_ble_validation(hass):
    f = flow(hass, 'bluetooth')
    result = await f.async_step_bluetooth(service_info())
    assert result['step_id'] == 'bluetooth_confirm'
    menu = await f.async_step_bluetooth_confirm({})
    assert menu['menu_options'] == ['login', 'user_id']
    assert (await f.async_step_user_id())['step_id'] == 'user_id'
    target = 'custom_components.suris_ef_ble_xboost.config_flow.validate_credentials'
    with patch(target, AsyncMock(side_effect=ConfigEntryAuthFailed('no'))):
        result = await f.async_step_user_id({'user_id': '12345678'})
        assert result['type'] == 'form' and result['errors']['base'] == 'invalid_auth'
    with patch(target, AsyncMock()) as validate:
        result = await f.async_step_user_id({'user_id': '12345678'})
        validate.assert_awaited_once_with(hass, PROFILE, '12345678')
        assert result['type'] == 'create_entry'
        assert result['data'] == {**PROFILE, 'user_id': '12345678', 'auth_source': 'suris_ble_verified'}


@pytest.mark.asyncio
async def test_cloud_login_does_not_store_password(hass):
    f = flow(hass)
    f._profile = PROFILE
    login_result = SimpleNamespace(user_id='12345678', error=None)
    credentials = {'email': 'synthetic@example.test', 'password': 'synthetic-password'}
    with patch('custom_components.suris_ef_ble_xboost.config_flow.async_get_clientsession', return_value=Mock()), patch('custom_components.suris_ef_ble_xboost.config_flow.EcoFlowLogin.login', AsyncMock(return_value=login_result)), patch('custom_components.suris_ef_ble_xboost.config_flow.validate_credentials', AsyncMock()):
        result = await f.async_step_login(credentials)
    assert result['type'] == 'create_entry'
    assert credentials == {}
    assert not any('password' in k or 'email' in k for k in result['data'])
    assert 'synthetic-password' not in repr(vars(f))


@pytest.mark.asyncio
async def test_duplicate_discovery_by_serial_and_legacy_mac(hass):
    await add_entry(hass, unique_id=ADDRESS)
    result = await flow(hass, 'bluetooth').async_step_bluetooth(service_info(address=ADDRESS.lower()))
    assert result['reason'] == 'already_configured'
    result = await flow(hass, 'bluetooth').async_step_bluetooth(service_info(address='11:22:33:44:55:66'))
    assert result['reason'] == 'already_configured'


@pytest.mark.asyncio
async def test_no_foreign_credentials_on_migration(hass):
    entry = await add_entry(hass, {**PROFILE, 'user_id': '777', 'ef_ble_entry_id': 'foreign', 'password': 'bad'}, version=2, unique_id=ADDRESS)
    with patch.object(hass.config_entries, 'async_get_entry', side_effect=AssertionError('external entry lookup forbidden')):
        assert await async_migrate_entry(hass, entry)
    assert 'user_id' not in entry.data and 'ef_ble_entry_id' not in entry.data and 'password' not in entry.data
    assert entry.version == 3 and entry.unique_id == SN
    with pytest.raises(ConfigEntryAuthFailed):
        await async_setup_entry(hass, entry)


@pytest.mark.asyncio
async def test_migration_preserves_own_id_and_entity_ids(hass):
    entry = await add_entry(hass, {**PROFILE, 'user_id': '12345678'}, version=2, unique_id=ADDRESS)
    foreign = await add_entry(hass, {}, domain='ef_ble', unique_id='foreign')
    dreg, ereg = dr.async_get(hass), er.async_get(hass)
    old = dreg.async_get_or_create(config_entry_id=entry.entry_id, identifiers={('ef_ble', ADDRESS)}, connections={('bluetooth', ADDRESS)})
    foreign_device = dreg.async_get_or_create(config_entry_id=foreign.entry_id, identifiers={('ef_ble', ADDRESS)})
    main = ereg.async_get_or_create('sensor', DOMAIN, f'ef_{SN}_battery_level', config_entry=entry, device_id=old.id, disabled_by=er.RegistryEntryDisabler.INTEGRATION)
    extra = ereg.async_get_or_create('sensor', DOMAIN, f'suris_ef_ble_slave_1_cycles_{SN}', config_entry=entry, device_id=old.id, disabled_by=er.RegistryEntryDisabler.USER)
    assert await async_migrate_entry(hass, entry)
    assert entry.data['user_id'] == '12345678'
    runtime = SurisRuntime(hass, entry, device())
    async_prepare_registry(hass, entry, runtime)
    assert runtime.main_device_id == old.id
    assert ereg.async_get(main.entity_id).disabled_by is None
    assert ereg.async_get(extra.entity_id).disabled_by is None
    assert ereg.async_get(extra.entity_id).device_id == runtime.battery_device_id
    assert dreg.async_get(runtime.battery_device_id).via_device_id == old.id
    assert dreg.async_get(old.id).identifiers == {(DOMAIN, SN)}
    assert dreg.async_get(old.id).connections == set()
    assert dreg.async_get(foreign_device.id).identifiers == {('ef_ble', ADDRESS)}
    # Migration is one-shot: later user preferences are not constantly overwritten.
    ereg.async_update_entity(main.entity_id, disabled_by=er.RegistryEntryDisabler.USER)
    async_prepare_registry(hass, entry, runtime)
    assert ereg.async_get(main.entity_id).disabled_by == er.RegistryEntryDisabler.USER
    runtime.close()


@pytest.mark.asyncio
async def test_late_bms_creates_all_entities_once(hass):
    entry = await add_entry(hass)
    runtime = SurisRuntime(hass, entry, device())
    entry.runtime_data = runtime
    async_prepare_registry(hass, entry, runtime)
    added = []
    module = importlib.import_module('custom_components.suris_ef_ble_xboost.sensor')
    await module.async_setup_entry(hass, entry, added.extend)
    assert len(added) == 37 and runtime.battery_device_id is None
    await bms_packet(runtime.device)
    await asyncio.sleep(0)
    assert len(added) == 66 and runtime.battery_device_id
    by_key = {e.key: e for e in added}
    assert by_key['battery_1_battery_level'].native_value == 72.5
    assert by_key['battery_1_voltage'].native_value == 52
    assert by_key['slave_1_power_difference'].native_value == -50
    assert by_key['slave_1_cycles'].native_value == 11
    await bms_packet(runtime.device)
    await asyncio.sleep(0)
    assert len(added) == 66
    runtime._accept_state(ConnectionState.DISCONNECTED)
    assert not by_key['slave_1_cycles'].available
    runtime.close()
    await entry._async_process_on_unload(hass)


@pytest.mark.asyncio
async def test_bms_before_platform_setup_and_thread_callback(hass):
    entry = await add_entry(hass)
    runtime = SurisRuntime(hass, entry, device())
    entry.runtime_data = runtime
    async_prepare_registry(hass, entry, runtime)
    await bms_packet(runtime.device)
    added = []
    await importlib.import_module('custom_components.suris_ef_ble_xboost.sensor').async_setup_entry(hass, entry, added.extend)
    assert len(added) == 66
    observed = []
    runtime.subscribe(lambda: observed.append(asyncio.get_running_loop()))
    await asyncio.to_thread(runtime._raw_received, _BmsHeartbeatBattery1(vol=53000, cycles=12))
    await asyncio.sleep(0)
    assert observed and all(loop is hass.loop for loop in observed)
    runtime.close()
    old_count = len(observed)
    await asyncio.to_thread(runtime._raw_received, _BmsHeartbeatBattery1(vol=54000))
    await asyncio.sleep(0)
    assert len(observed) == old_count
    assert not runtime._listeners and not runtime._removers and runtime._pending is None
    await entry._async_process_on_unload(hass)


@pytest.mark.asyncio
async def test_car_input_serializes_and_rejects_stale_limits(hass):
    entry = await add_entry(hass)
    runtime = SurisRuntime(hass, entry, device())
    state = EcoFlowCarInputCurrentState(runtime)
    sent = []
    async def send(packet, **kwargs):
        sent.append(packet.payload)
        await asyncio.sleep(0)
    runtime.device.send_packet = send
    with pytest.raises(HomeAssistantError):
        await state.set_current(0, 6000)
    runtime.raw['Mr350MpptHeart'] = Mr350MpptHeart(cfg_dc_chg_current=4000, res=(8000).to_bytes(4,'little') + bytes(4))
    await asyncio.gather(state.set_current(0,6000), state.set_current(1,4000))
    assert sent == [struct.pack('<II',6000,8000), struct.pack('<II',6000,4000)]
    runtime._accept_state(ConnectionState.DISCONNECTED)
    with pytest.raises(HomeAssistantError):
        await state.set_current(0,8000)
    assert len(sent) == 2
    state.close()
    runtime.close()


@pytest.mark.asyncio
async def test_car_input_disconnect_during_write(hass):
    entry = await add_entry(hass)
    runtime = SurisRuntime(hass, entry, device())
    state = EcoFlowCarInputCurrentState(runtime)
    runtime.raw['Mr350MpptHeart'] = Mr350MpptHeart(cfg_dc_chg_current=4000, res=(8000).to_bytes(4,'little') + bytes(4))
    async def send(*args, **kwargs):
        runtime._accept_state(ConnectionState.DISCONNECTED)
    runtime.device.send_packet = send
    with pytest.raises(HomeAssistantError):
        await state.set_current(1,6000)
    assert not state.available
    state.close()
    runtime.close()


@pytest.mark.asyncio
async def test_credential_probe_always_disconnects(hass):
    dev = device(connected=False)
    with patch.object(driver, 'create_device', return_value=dev), patch.object(driver, 'connect_device', AsyncMock(side_effect=ConfigEntryAuthFailed('no'))), patch.object(driver, 'disconnect_device', AsyncMock()) as disconnect:
        with pytest.raises(ConfigEntryAuthFailed):
            await driver.validate_credentials(hass, PROFILE, '12345678')
        disconnect.assert_awaited_once_with(dev)


@pytest.mark.asyncio
async def test_advertisement_length_guard(hass):
    assert driver.profile_from_service_info(service_info(length=5)) is None
    for length in (17,19,20,21,22,23):
        info = service_info(length=length)
        assert driver.profile_from_service_info(info) == PROFILE
        assert isinstance(Device(info.device,info.advertisement,SN).scan_record.encrypt_type,int)


@pytest.mark.asyncio
async def test_backend_disconnect_awaits_tasks_and_timers():
    info = service_info()
    conn = Connection(ble_dev=info.device,dev_sn=SN,user_id='12345678',data_parse=AsyncMock(),packet_parse=AsyncMock(),packet_version=2,encrypt_type=0,auth_header_dst=0x35)
    done = []
    async def work():
        try:
            await asyncio.Event().wait()
        finally:
            done.append(True)
    task = conn._add_task(work())
    await asyncio.sleep(0)
    conn.call_later(100, lambda: None)
    conn.call_later(100, lambda: None, key='named')
    assert len(conn._call_later_handles) == 2
    await conn.disconnect()
    assert task.done() and done == [True]
    assert not conn._tasks and not conn._call_later_handles


@pytest.mark.asyncio
async def test_setup_unload_and_failed_setup_cleanup(hass):
    entry = await add_entry(hass)
    dev = device()
    target = 'custom_components.suris_ef_ble_xboost'
    with patch(target+'.create_device', return_value=dev), patch(target+'.connect_device', AsyncMock()), patch(target+'.disconnect_device', AsyncMock()) as disconnect, patch.object(hass.config_entries,'async_forward_entry_setups',AsyncMock()), patch.object(hass.config_entries,'async_unload_platforms',AsyncMock(return_value=True)), patch.object(hass.config_entries,'async_schedule_reload') as reload:
        assert await async_setup_entry(hass,entry)
        runtime = entry.runtime_data
        dev._listeners.on_disconnect(None)
        dev._listeners.on_disconnect(None)
        assert reload.call_count == 1
        assert await async_unload_entry(hass,entry)
        assert runtime.closed and not runtime._listeners and entry.runtime_data is None
        dev._listeners.on_disconnect(None)
        assert reload.call_count == 1
        disconnect.assert_awaited_once_with(dev)
        await entry._async_process_on_unload(hass)
    dev = device()
    with patch(target+'.create_device', return_value=dev), patch(target+'.connect_device',AsyncMock(side_effect=ConfigEntryNotReady('offline'))), patch(target+'.disconnect_device',AsyncMock()) as disconnect, patch.object(hass.config_entries,'async_unload_platforms',AsyncMock(return_value=True)):
        with pytest.raises(ConfigEntryNotReady):
            await async_setup_entry(hass,entry)
        disconnect.assert_awaited_once_with(dev)
        assert not dev._raw_listeners.on_message_processed
        assert entry.runtime_data is None


@pytest.mark.asyncio
async def test_real_ha_entity_platforms_register_77_enabled_entities(hass):
    entry = await add_entry(hass)
    runtime = SurisRuntime(hass, entry, device())
    entry.runtime_data = runtime
    async_prepare_registry(hass, entry, runtime)
    platforms = []
    for name in ('sensor', 'switch', 'number', 'select'):
        module = importlib.import_module(f'custom_components.{DOMAIN}.{name}')
        platform = EntityPlatform(hass=hass, logger=logging.getLogger(__name__), domain=name,
            platform_name=DOMAIN, platform=module, scan_interval=timedelta(seconds=30), entity_namespace=None)
        platform.config_entry = entry
        platforms.append(platform)
        def add_entities(entities, update_before_add=False, platform=platform):
            hass.async_create_task(platform.async_add_entities(entities, update_before_add))
        await module.async_setup_entry(hass, entry, add_entities)
    await hass.async_block_till_done()
    entries = er.async_entries_for_config_entry(er.async_get(hass), entry.entry_id)
    assert len(entries) == 48
    await bms_packet(runtime.device)
    await hass.async_block_till_done()
    entries = er.async_entries_for_config_entry(er.async_get(hass), entry.entry_id)
    assert len(entries) == 77
    assert all(e.disabled_by is None and e.hidden_by is None for e in entries)
    extra = [e for e in entries if e.device_id == runtime.battery_device_id]
    assert len(extra) == 29
    cycle = next(e for e in extra if 'slave_1_cycles' in e.unique_id)
    assert hass.states.get(cycle.entity_id).state == '11'
    assert len(dr.async_entries_for_config_entry(dr.async_get(hass), entry.entry_id)) == 2
    for platform in platforms:
        await platform.async_reset()
    runtime.close()
    await entry._async_process_on_unload(hass)


@pytest.mark.asyncio
async def test_reauth_keeps_registry_migration_flag(hass):
    entry = await add_entry(hass, {**PROFILE, 'enable_sensor_migration': True})
    f = flow(hass, 'reauth')
    f.context['entry_id'] = entry.entry_id
    menu = await f.async_step_reauth(entry.data)
    assert menu['menu_options'] == ['login', 'user_id']
    with patch('custom_components.suris_ef_ble_xboost.config_flow.validate_credentials', AsyncMock()), patch.object(hass.config_entries, 'async_schedule_reload'):
        result = await f.async_step_user_id({'user_id':'12345678'})
    assert result['reason'] == 'reauth_successful'
    assert entry.data['enable_sensor_migration'] is True
    assert entry.data['user_id'] == '12345678'


@pytest.mark.asyncio
async def test_duplicate_entry_merge_preserves_entity_id(hass):
    primary = await add_entry(hass)
    duplicate = await add_entry(hass, unique_id=ADDRESS)
    registry = er.async_get(hass)
    entity = registry.async_get_or_create('sensor',DOMAIN,f'suris_ef_ble_main_battery_cycles_{SN}',config_entry=duplicate)
    with patch.object(hass.config_entries,'async_unload',AsyncMock(return_value=True)), patch.object(ConfigEntry,'async_remove',AsyncMock()):
        assert await async_merge_duplicates(hass,primary)
    assert hass.config_entries.async_get_entry(duplicate.entry_id) is None
    assert registry.async_get(entity.entity_id).config_entry_id == primary.entry_id


@pytest.mark.asyncio
async def test_recover_legacy_serial_without_parent(hass):
    entry = await add_entry(hass, {'ef_ble_entry_id':'gone'}, version=1, unique_id='gone')
    er.async_get(hass).async_get_or_create('sensor',DOMAIN,f'suris_ef_ble_main_battery_cycles_{SN}',config_entry=entry)
    with patch('custom_components.suris_ef_ble_xboost.bluetooth.async_discovered_service_info',return_value=[service_info()]):
        assert await async_migrate_entry(hass,entry)
    assert entry.data['serial_number'] == SN and entry.data['address'] == ADDRESS
    assert 'user_id' not in entry.data


@pytest.mark.asyncio
async def test_probe_cancellation_releases_ble(hass):
    dev = device(connected=False)
    started = asyncio.Event()
    async def connect(*args):
        started.set()
        await asyncio.Event().wait()
    with patch.object(driver,'create_device',return_value=dev),patch.object(driver,'connect_device',connect),patch.object(driver,'disconnect_device',AsyncMock()) as disconnect:
        task = asyncio.create_task(driver.validate_credentials(hass,PROFILE,'12345678'))
        await started.wait()
        task.cancel()
        with pytest.raises(asyncio.CancelledError):
            await task
        disconnect.assert_awaited_once_with(dev)


@pytest.mark.asyncio
async def test_ha_loader_and_managed_initial_config_flow(hass):
    from homeassistant import loader
    loader.async_setup(hass)
    integration = await loader.async_get_integration(hass,DOMAIN)
    assert integration.version == '0.8.0b4'
    assert integration.dependencies == ['bluetooth']
    await integration.async_get_platform('config_flow')
    manager = hass.config_entries.flow
    with patch('custom_components.suris_ef_ble_xboost.config_flow.bluetooth.async_discovered_service_info',return_value=[service_info()]), patch('custom_components.suris_ef_ble_xboost.config_flow.bluetooth.async_last_service_info',return_value=service_info()), patch('custom_components.suris_ef_ble_xboost.config_flow.validate_credentials',AsyncMock()) as validate, patch.object(hass.config_entries,'async_setup',AsyncMock(return_value=True)):
        result = await manager.async_init(DOMAIN,context={'source':'user'})
        result = await manager.async_configure(result['flow_id'],{'address':ADDRESS})
        assert result['type'] == 'menu' and result['step_id'] == 'auth'
        result = await manager.async_configure(result['flow_id'],{'next_step_id':'user_id'})
        assert result['step_id'] == 'user_id'
        result = await manager.async_configure(result['flow_id'],{'user_id':'12345678'})
        assert result['type'] == 'create_entry'
        validate.assert_awaited_once()
        configured = hass.config_entries.async_entries(DOMAIN)
        assert len(configured) == 1 and configured[0].unique_id == SN
        duplicate = await manager.async_init(DOMAIN,context={'source':'bluetooth'},data=service_info())
        assert duplicate['reason'] == 'already_configured'
