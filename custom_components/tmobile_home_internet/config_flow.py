"""Config flow for Home Assistant T-Mobile Home Internet integration."""
from __future__ import annotations

import asyncio
import logging

from requests import ConnectionError,HTTPError
from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult
from homeassistant.exceptions import HomeAssistantError
from homeassistant.const import CONF_USERNAME, CONF_PASSWORD

import pytmhi

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_USERNAME): str,
        vol.Required(CONF_PASSWORD): str
    }
)


async def validate_input(hass: HomeAssistant, data: dict[str, Any]) -> dict[str, Any]:
    """Validate the user input allows us to connect.

    Data has the keys from STEP_USER_DATA_SCHEMA with values provided by the user.
    """
    controller = pytmhi.TmiApiClient(data[CONF_USERNAME], data[CONF_PASSWORD])

    # Request some data to validate username/password.
    await hass.async_add_executor_job(controller.auth_token)

    # Return info that you want to store in the config entry.
    return {"title": "T-Mobile Home Internet"}


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Home Assistant T-Mobile Home Internet"""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}
        if user_input is not None:
            try:
                info = await validate_input(self.hass, user_input)
            except HTTPError as exc:
                _LOGGER.exception(f"HTTPError: {str(exc)}")
                if exc.response.status_code == 401:
                    errors["base"] = "invalid_auth"
                elif exc.response.status_code == 404:
                    errors["base"] = "cannot_connect"
                else:
                    errors["base"] = "unknown"
            except ConnectionError as exc:
                _LOGGER.exception(exc)
                errors["base"] = "cannot_connect"
            except Exception as exc: # pylint: disable=broad-except
                _LOGGER.exception(f"Unexpected exception: {str(exc)}")
                errors["base"] = "unknown"
            else:
                return self.async_create_entry(title=info["title"], data=user_input)

        return self.async_show_form(
            step_id="user", data_schema=STEP_USER_DATA_SCHEMA, errors=errors
        )
