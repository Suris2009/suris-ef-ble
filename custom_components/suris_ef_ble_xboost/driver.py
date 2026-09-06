# SPDX-License-Identifier: Apache-2.0
# Suris additions/adaptations, 2026. See NOTICE for upstream attribution.
# This is an independently modified, unofficial integration.
"""Own the BLE session using the bundled, unchanged D2M protocol/commands."""
from __future__ import annotations

import asyncio

from homeassistant.components import bluetooth
from homeassistant.exceptions import ConfigEntryAuthFailed, ConfigEntryNotReady

from ._vendor.eflib.connection import Connection
from ._vendor.eflib.devices.delta2_max import Device
from ._vendor.eflib.exceptions import AuthErrors, AuthFailedError
from .const import (
    CONF_ADDRESS, CONF_SERIAL_NUMBER, CONNECTION_TIMEOUT, SETUP_TIMEOUT,
    normalize_address, valid_serial,
)


def profile_from_service_info(info) -> dict[str, str] | None:
    if info is None:
        return None
    raw = info.manufacturer_data.get(Device.MANUFACTURER_KEY, b"")
    if len(raw) < 17:
        return None
    try:
        serial = raw[1:17].decode("ascii")
    except UnicodeDecodeError:
        return None
    if not valid_serial(serial):
        return None
    return {CONF_ADDRESS: normalize_address(info.address), CONF_SERIAL_NUMBER: serial}


def create_device(hass, profile: dict) -> Device:
    info = bluetooth.async_last_service_info(hass, profile[CONF_ADDRESS], connectable=True)
    actual = profile_from_service_info(info)
    if actual is None:
        raise ConfigEntryNotReady("DELTA 2 Max is not currently visible through Bluetooth")
    if actual[CONF_SERIAL_NUMBER] != profile[CONF_SERIAL_NUMBER]:
        raise ConfigEntryNotReady("The Bluetooth address belongs to a different station")
    return (
        Device(info.device, info.advertisement, actual[CONF_SERIAL_NUMBER])
        .with_disabled_reconnect()
        .with_connection_options(Connection.Options(timeout=CONNECTION_TIMEOUT))
    )


async def connect_device(device: Device, user_id: str) -> None:
    """Authenticate; HA owns retries so a fresh backend is used for each reload."""
    try:
        async with asyncio.timeout(SETUP_TIMEOUT):
            await device.connect(user_id=user_id, max_attempts=2)
            state = await device.wait_until_authenticated_or_error(raise_on_error=True)
            if not state.authenticated or not device.is_connected:
                raise ConfigEntryNotReady("BLE connection ended before authentication")
    except (AuthErrors.BaseException, AuthFailedError) as err:
        raise ConfigEntryAuthFailed("EcoFlow rejected the User ID; authenticate again") from err
    except ConfigEntryNotReady:
        raise
    except Exception as err:
        raise ConfigEntryNotReady(f"BLE connection failed ({type(err).__name__})") from err


async def disconnect_device(device: Device) -> None:
    if device._conn is not None:
        await device.disconnect()


async def validate_credentials(hass, profile: dict, user_id: str) -> None:
    device = create_device(hass, profile)
    try:
        await connect_device(device, user_id)
    finally:
        await disconnect_device(device)
