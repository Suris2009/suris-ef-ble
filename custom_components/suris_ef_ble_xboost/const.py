# SPDX-License-Identifier: Apache-2.0
# Suris additions/adaptations, 2026. See NOTICE for upstream attribution.
# This is an independently modified, unofficial integration.
"""Suris-owned configuration; no credentials or identifiers are hardcoded."""

DOMAIN = "suris_ef_ble_xboost"
VERSION = "0.8.0b4"
ENTRY_TITLE = "Suris EcoFlow BLE"
CONF_ADDRESS = "address"
CONF_SERIAL_NUMBER = "serial_number"
CONF_USER_ID = "user_id"
CONF_AUTH_SOURCE = "auth_source"
AUTH_SOURCE = "suris_ble_verified"
CONF_BATTERY_SEEN = "battery_1_seen"
CONNECTION_TIMEOUT = 25
SETUP_TIMEOUT = 60


def normalize_address(value: str) -> str:
    return value.strip().upper()


def valid_serial(value: object) -> bool:
    return isinstance(value, str) and len(value) == 16 and value.startswith(("R351", "R354")) and value.isascii() and value.isalnum()


def valid_user_id(value: object) -> bool:
    # Upstream authentication uses the account's decimal user ID, never a token.
    return isinstance(value, str) and value.isascii() and value.isdecimal() and 1 <= len(value) <= 32


def same_device(data: dict, other: dict) -> bool:
    serial = data.get(CONF_SERIAL_NUMBER)
    address = data.get(CONF_ADDRESS)
    return bool(
        (serial and serial == other.get(CONF_SERIAL_NUMBER))
        or (address and normalize_address(address) == normalize_address(other.get(CONF_ADDRESS, "")))
    )
