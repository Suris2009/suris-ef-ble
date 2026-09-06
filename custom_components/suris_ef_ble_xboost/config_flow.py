# SPDX-License-Identifier: Apache-2.0
# Suris additions/adaptations, 2026. See NOTICE for upstream attribution.
# This is an independently modified, unofficial integration.
"""Explicit discovery → authentication → BLE validation → own config entry."""
from __future__ import annotations

import asyncio

import aiohttp
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.components import bluetooth
from homeassistant.exceptions import ConfigEntryAuthFailed, ConfigEntryNotReady
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.selector import TextSelector, TextSelectorConfig, TextSelectorType

from ._vendor.eflib.login import EcoFlowLogin, Region
from .const import (
    AUTH_SOURCE, CONF_ADDRESS, CONF_AUTH_SOURCE, CONF_SERIAL_NUMBER, CONF_USER_ID,
    DOMAIN, ENTRY_TITLE, normalize_address, same_device, valid_user_id,
)
from .driver import profile_from_service_info, validate_credentials


class SurisEcoFlowBleXBoostConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 3
    MINOR_VERSION = 0

    def __init__(self):
        self._profile: dict = {}
        self._reauth_entry = None

    def _configured(self, profile):
        return next((e for e in self._async_current_entries() if
            (self._reauth_entry is None or e.entry_id != self._reauth_entry.entry_id)
            and (same_device(profile, e.data) or e.unique_id in (
                profile.get(CONF_SERIAL_NUMBER), profile.get(CONF_ADDRESS)
            ))), None)

    async def _select_profile(self, profile):
        if profile is None:
            return self.async_abort(reason="not_delta_2_max")
        if self._reauth_entry and (old_sn := self._reauth_entry.data.get(CONF_SERIAL_NUMBER)) and old_sn != profile[CONF_SERIAL_NUMBER]:
            return self.async_abort(reason="wrong_device")
        if self._configured(profile):
            return self.async_abort(reason="already_configured")
        self._profile = profile
        await self.async_set_unique_id(profile[CONF_SERIAL_NUMBER])
        if self._reauth_entry is None:
            self._abort_if_unique_id_configured()
        return None

    async def async_step_bluetooth(self, discovery_info):
        if result := await self._select_profile(profile_from_service_info(discovery_info)):
            return result
        self.context["title_placeholders"] = {"name": f"DELTA 2 Max {self._profile[CONF_SERIAL_NUMBER][-4:]}"}
        return await self.async_step_bluetooth_confirm()

    async def async_step_bluetooth_confirm(self, user_input=None):
        if user_input is not None:
            return await self.async_step_auth()
        return self.async_show_form(step_id="bluetooth_confirm", data_schema=vol.Schema({}), description_placeholders=self._profile)

    async def async_step_user(self, user_input=None):
        discovered = {}
        for info in bluetooth.async_discovered_service_info(self.hass, connectable=True):
            profile = profile_from_service_info(info)
            if profile and not self._configured(profile):
                if self._reauth_entry and (sn := self._reauth_entry.data.get(CONF_SERIAL_NUMBER)) and sn != profile[CONF_SERIAL_NUMBER]:
                    continue
                discovered[profile[CONF_ADDRESS]] = f"DELTA 2 Max · {profile[CONF_SERIAL_NUMBER]} · {profile[CONF_ADDRESS]}"
        errors = {}
        if user_input is not None:
            address = normalize_address(user_input[CONF_ADDRESS])
            info = bluetooth.async_last_service_info(self.hass, address, connectable=True)
            profile = profile_from_service_info(info)
            if profile is None:
                errors["base"] = "device_not_found"
            else:
                if result := await self._select_profile(profile):
                    return result
                return await self.async_step_auth()
        schema = vol.Schema({vol.Required(CONF_ADDRESS): vol.In(discovered) if discovered else str})
        return self.async_show_form(step_id="user", data_schema=schema, errors=errors)

    async def async_step_auth(self, user_input=None):
        return self.async_show_menu(step_id="auth", menu_options=["login", "user_id"])

    async def async_step_reauth(self, entry_data):
        self._reauth_entry = self._get_reauth_entry()
        data = self._reauth_entry.data
        if data.get(CONF_ADDRESS) and data.get(CONF_SERIAL_NUMBER):
            self._profile = {key: data[key] for key in (CONF_ADDRESS, CONF_SERIAL_NUMBER)}
            return await self.async_step_auth()
        return await self.async_step_user()

    async def async_step_user_id(self, user_input=None):
        errors = {}
        if user_input is not None:
            user_id = user_input[CONF_USER_ID].strip()
            if not valid_user_id(user_id):
                errors[CONF_USER_ID] = "invalid_user_id"
            else:
                result, error = await self._validate_and_finish(user_id)
                if result:
                    return result
                errors["base"] = error
        return self.async_show_form(step_id="user_id", data_schema=vol.Schema({vol.Required(CONF_USER_ID): str}), errors=errors)

    async def async_step_login(self, user_input=None):
        errors = {}
        if user_input is not None:
            try:
                async with asyncio.timeout(30):
                    result = await EcoFlowLogin(async_get_clientsession(self.hass)).login(
                        user_input["email"], user_input["password"], Region.AUTO
                    )
                user_id = str(result.user_id or "").strip()
                if result.error or not valid_user_id(user_id):
                    errors["base"] = "login_failed"
                else:
                    finished, error = await self._validate_and_finish(user_id)
                    if finished:
                        return finished
                    errors["base"] = error
            except (aiohttp.ClientError, TimeoutError, ValueError, KeyError, TypeError):
                errors["base"] = "login_failed"
            finally:
                # Neither form defaults, flow attributes nor config entry retain credentials.
                user_input.clear()
        return self.async_show_form(step_id="login", errors=errors, data_schema=vol.Schema({
            vol.Required("email"): TextSelector(TextSelectorConfig(type=TextSelectorType.EMAIL)),
            vol.Required("password"): TextSelector(TextSelectorConfig(type=TextSelectorType.PASSWORD)),
        }))

    async def _validate_and_finish(self, user_id):
        if self._configured(self._profile):
            return self.async_abort(reason="already_configured"), None
        # Reauth can be initiated from the UI while the entry is still loaded.
        if self._reauth_entry and self._reauth_entry.state is config_entries.ConfigEntryState.LOADED:
            if not await self.hass.config_entries.async_unload(self._reauth_entry.entry_id):
                return None, "cannot_connect"
        try:
            await validate_credentials(self.hass, self._profile, user_id)
        except ConfigEntryAuthFailed:
            return None, "invalid_auth"
        except ConfigEntryNotReady:
            return None, "cannot_connect"
        # Check again after the BLE await: another flow may have completed meanwhile.
        if self._configured(self._profile):
            return self.async_abort(reason="already_configured"), None
        data = {**self._profile, CONF_USER_ID: user_id, CONF_AUTH_SOURCE: AUTH_SOURCE}
        if self._reauth_entry:
            for key in ("battery_1_seen", "enable_sensor_migration"):
                if key in self._reauth_entry.data:
                    data[key] = self._reauth_entry.data[key]
            return self.async_update_reload_and_abort(
                self._reauth_entry, unique_id=self._profile[CONF_SERIAL_NUMBER],
                data=data, reason="reauth_successful",
            ), None
        return self.async_create_entry(title=ENTRY_TITLE, data=data), None
