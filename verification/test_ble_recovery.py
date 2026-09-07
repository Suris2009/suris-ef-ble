# SPDX-License-Identifier: Apache-2.0
"""Regression checks for rediscovery and cleanup, using real HA entry/BT APIs.

Only radio traffic and actual device connection attempts are simulated.
No EcoFlow account, Bluetooth adapter or physical station is used.
"""
import asyncio
from types import SimpleNamespace
from unittest.mock import AsyncMock, Mock, patch

import pytest
import pytest_asyncio
from bleak_retry_connector import BleakSlotManager
from homeassistant.components import bluetooth
from homeassistant.components.bluetooth.const import DATA_MANAGER
from homeassistant.components.bluetooth.manager import HomeAssistantBluetoothManager
from homeassistant.components.bluetooth.match import IntegrationMatcher
from homeassistant.components.bluetooth.storage import BluetoothStorage
from homeassistant.config_entries import ConfigEntryDisabler, ConfigEntryState
from homeassistant.const import EVENT_HOMEASSISTANT_STOP
from homeassistant.core import CoreState
from homeassistant.exceptions import ConfigEntryNotReady

from custom_components.suris_ef_ble_xboost import (
    async_remove_entry, async_setup, async_setup_entry,
)
from custom_components.suris_ef_ble_xboost.const import DOMAIN
from custom_components.suris_ef_ble_xboost.recovery import DATA_BLE_RECOVERY

from verification.test_integration import (
    ADDRESS, PROFILE, SN, add_entry, device, hass, service_info,
)


@pytest_asyncio.fixture
async def bt_manager(hass):
    # Use HA's real matcher, subscription API and cached-advertisement replay.
    # Do not start adapters, DBus or the manager's background scanning timers.
    manager = HomeAssistantBluetoothManager(
        hass, IntegrationMatcher([]), Mock(adapters={}), BluetoothStorage(hass),
        BleakSlotManager(),
    )
    manager._loop = hass.loop
    hass.data[DATA_MANAGER] = manager
    yield manager
    if recovery := hass.data.get(DOMAIN, {}).get(DATA_BLE_RECOVERY):
        recovery.close()
    manager.async_stop()


def advertisement(hass, *, serial=SN, address=ADDRESS, connectable=True, age=0):
    info = service_info(serial=serial, address=address)
    return bluetooth.BluetoothServiceInfoBleak.from_device_and_advertisement_data(
        info.device, info.advertisement, "synthetic_adapter", hass.loop.time() - age,
        connectable,
    )


def set_state(hass, entry, state):
    entry._async_set_state(hass, state, None)


@pytest.mark.asyncio
async def test_twenty_hour_old_advertisement_does_not_trigger_but_fresh_one_does(hass, bt_manager):
    entry = await add_entry(hass)
    set_state(hass, entry, ConfigEntryState.SETUP_RETRY)
    old = advertisement(hass, age=20 * 3600)
    bt_manager._connectable_history[ADDRESS] = old
    bt_manager._all_history[ADDRESS] = old
    with patch.object(hass.config_entries, "async_schedule_reload") as reload:
        assert await async_setup(hass, {})
        reload.assert_not_called()  # Cached data must not impersonate power-on.
        bt_manager._discover_service_info(advertisement(hass))
        reload.assert_called_once_with(entry.entry_id)
        for _ in range(100):
            bt_manager._discover_service_info(advertisement(hass))
        reload.assert_called_once_with(entry.entry_id)


@pytest.mark.asyncio
@pytest.mark.parametrize("state", [
    ConfigEntryState.LOADED, ConfigEntryState.SETUP_IN_PROGRESS,
    ConfigEntryState.UNLOAD_IN_PROGRESS, ConfigEntryState.NOT_LOADED,
    ConfigEntryState.SETUP_ERROR, ConfigEntryState.FAILED_UNLOAD,
])
async def test_advertisements_do_not_interrupt_other_entry_states(hass, bt_manager, state):
    entry = await add_entry(hass)
    set_state(hass, entry, state)
    await async_setup(hass, {})
    with patch.object(hass.config_entries, "async_schedule_reload") as reload:
        for _ in range(3):
            bt_manager._discover_service_info(advertisement(hass))
        reload.assert_not_called()


@pytest.mark.asyncio
async def test_disabled_entry_and_ha_shutdown_are_not_restarted(hass, bt_manager):
    entry = await add_entry(hass)
    set_state(hass, entry, ConfigEntryState.SETUP_RETRY)
    await async_setup(hass, {})
    with patch.object(hass.config_entries, "async_reload", AsyncMock(return_value=True)):
        await hass.config_entries.async_set_disabled_by(entry.entry_id, ConfigEntryDisabler.USER)
    with patch.object(hass.config_entries, "async_schedule_reload") as reload:
        bt_manager._discover_service_info(advertisement(hass))
        reload.assert_not_called()
        with patch.object(hass.config_entries, "async_reload", AsyncMock(return_value=True)):
            await hass.config_entries.async_set_disabled_by(entry.entry_id, None)
        previous_state = hass.state
        hass.set_state(CoreState.stopping)
        try:
            bt_manager._discover_service_info(advertisement(hass))
            reload.assert_not_called()
        finally:
            hass.set_state(previous_state)


@pytest.mark.asyncio
async def test_only_matching_serial_address_and_connectable_advertisement_can_restart(hass, bt_manager):
    entry = await add_entry(hass)
    set_state(hass, entry, ConfigEntryState.SETUP_RETRY)
    await async_setup(hass, {})
    with patch.object(hass.config_entries, "async_schedule_reload") as reload:
        for info in (
            advertisement(hass, serial="R351TEST00000002"),
            advertisement(hass, address="11:22:33:44:55:66"),
            advertisement(hass, connectable=False),
            advertisement(hass, serial="R701TEST00000001"),
        ):
            bt_manager._discover_service_info(info)
        reload.assert_not_called()
        bt_manager._discover_service_info(advertisement(hass))
        reload.assert_called_once_with(entry.entry_id)


@pytest.mark.asyncio
async def test_failed_early_retry_keeps_backoff_and_new_absence_rearms_it(hass, bt_manager):
    entry = await add_entry(hass)
    set_state(hass, entry, ConfigEntryState.SETUP_RETRY)
    await async_setup(hass, {})
    pending_retry = Mock()
    entry._async_cancel_retry_setup = pending_retry

    async def failed_reload(_entry_id):
        set_state(hass, entry, ConfigEntryState.SETUP_IN_PROGRESS)
        bt_manager._discover_service_info(advertisement(hass))
        set_state(hass, entry, ConfigEntryState.SETUP_RETRY)
        entry._async_cancel_retry_setup = next_retry
        return False

    next_retry = Mock()
    with patch.object(hass.config_entries, "async_reload", AsyncMock(side_effect=failed_reload)) as reload:
        # Real async_schedule_reload cancels the old retry and schedules one task.
        bt_manager._discover_service_info(advertisement(hass))
        await hass.async_block_till_done()
        pending_retry.assert_called_once_with()
        reload.assert_awaited_once_with(entry.entry_id)
        for _ in range(100):
            bt_manager._discover_service_info(advertisement(hass))
        await hass.async_block_till_done()
        reload.assert_awaited_once_with(entry.entry_id)
        next_retry.assert_not_called()  # Ordinary retry was not cancelled again.

        # Simulate another long outage through HA's real unavailable callbacks.
        old = advertisement(hass, age=20 * 3600)
        bt_manager._connectable_history[ADDRESS] = old
        bt_manager._all_history[ADDRESS] = old
        bt_manager._async_check_unavailable()
        bt_manager._discover_service_info(advertisement(hass))
        await hass.async_block_till_done()
        assert reload.await_count == 2
        next_retry.assert_called_once_with()


@pytest.mark.asyncio
async def test_listener_survives_entry_cleanup_and_is_removed_with_entry_or_shutdown(hass, bt_manager):
    entry = await add_entry(hass)
    await async_setup(hass, {})
    recovery = hass.data[DOMAIN][DATA_BLE_RECOVERY]
    assert await async_setup(hass, {})  # No duplicate subscription on repeated setup.
    assert hass.data[DOMAIN][DATA_BLE_RECOVERY] is recovery
    set_state(hass, entry, ConfigEntryState.LOADED)
    bt_manager._discover_service_info(advertisement(hass))
    assert entry.entry_id in recovery._watches
    await entry._async_process_on_unload(hass)
    set_state(hass, entry, ConfigEntryState.SETUP_RETRY)
    with patch.object(hass.config_entries, "async_schedule_reload") as reload:
        bt_manager._discover_service_info(advertisement(hass))
        reload.assert_called_once_with(entry.entry_id)
        await async_remove_entry(hass, entry)
        assert entry.entry_id not in recovery._watches
        hass.bus.async_fire(EVENT_HOMEASSISTANT_STOP)
        await hass.async_block_till_done()
        assert recovery._closed
        recovery.close()
        bt_manager._discover_service_info(advertisement(hass))
        reload.assert_called_once_with(entry.entry_id)


@pytest.mark.asyncio
@pytest.mark.parametrize("failure", [ConfigEntryNotReady("offline"), asyncio.CancelledError()])
async def test_connect_failure_never_unloads_platforms_that_were_not_started(hass, failure):
    entry = await add_entry(hass)
    dev = device()
    target = "custom_components.suris_ef_ble_xboost"
    with (
        patch(target + ".create_device", return_value=dev),
        patch(target + ".connect_device", AsyncMock(side_effect=failure)),
        patch(target + ".disconnect_device", AsyncMock()) as disconnect,
        patch.object(hass.config_entries, "async_forward_entry_setups", AsyncMock()) as forward,
        patch.object(hass.config_entries, "async_unload_platforms", AsyncMock(
            side_effect=AssertionError("Unstarted platforms must not be unloaded")
        )) as unload,
    ):
        with pytest.raises(type(failure)):
            await async_setup_entry(hass, entry)
        forward.assert_not_awaited()
        unload.assert_not_awaited()
        disconnect.assert_awaited_once_with(dev)
        assert entry.runtime_data is None
        assert not dev._raw_listeners.on_message_processed


@pytest.mark.asyncio
async def test_failure_after_platform_setup_started_still_cleans_up(hass):
    entry = await add_entry(hass)
    dev = device()
    target = "custom_components.suris_ef_ble_xboost"
    with (
        patch(target + ".create_device", return_value=dev),
        patch(target + ".connect_device", AsyncMock()),
        patch(target + ".disconnect_device", AsyncMock()) as disconnect,
        patch.object(hass.config_entries, "async_forward_entry_setups", AsyncMock(
            side_effect=RuntimeError("platform setup interrupted")
        )),
        patch.object(hass.config_entries, "async_unload_platforms", AsyncMock(return_value=True)) as unload,
    ):
        with pytest.raises(RuntimeError, match="platform setup interrupted"):
            await async_setup_entry(hass, entry)
        unload.assert_awaited_once()
        disconnect.assert_awaited_once_with(dev)
        assert entry.runtime_data is None
