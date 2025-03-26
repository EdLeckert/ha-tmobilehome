"""The Home Assistant T-Mobile Home Internet integration."""
from __future__ import annotations

from datetime import timedelta
import logging
import async_timeout

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.const import CONF_USERNAME, CONF_PASSWORD
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.exceptions import ConfigEntryAuthFailed
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
    UpdateFailed,
)
from homeassistant.helpers.entity_platform import async_get_platforms

from pytmhi import TmiApiClient

from .const import GET_ACCESS_POINT_RETRIES, GET_ACCESS_POINT_RETRY_SECONDS, DOMAIN, FAST_POLL_SECONDS, SLOW_POLL_SECONDS

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[Platform] = [Platform.SELECT, Platform.SENSOR, Platform.SWITCH]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Home Assistant T-Mobile Home Internet from a config entry."""

    hass.data.setdefault(DOMAIN, {})

    try:
        controller = TmiApiClient(entry.data[CONF_USERNAME],entry.data[CONF_PASSWORD])

        # Request some data to validate username/password.
        await hass.async_add_executor_job(controller.auth_token)

    except Exception as exc:
        _LOGGER.error(f"Unable to connect to T-Mobile Home Internet controller: {str(exc)}")
        raise ConfigEntryNotReady

    fast_coordinator = FastCoordinator(hass, controller)
    slow_coordinator = SlowCoordinator(hass, controller)

    hass.data[DOMAIN][entry.entry_id] = {
            "fast_coordinator": fast_coordinator,
            "slow_coordinator": slow_coordinator,
            "controller": controller,
        }

    # Fetch initial data
    await fast_coordinator.async_config_entry_first_refresh()
    await slow_coordinator.async_config_entry_first_refresh()

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


class FastCoordinator(DataUpdateCoordinator):
    """Rapid refresh coordinator."""

    def __init__(self, hass, controller):
        """Initialize fast coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name="T-Mobile Home Internet",
            # Polling interval. Will only be polled if there are subscribers.
            update_interval=timedelta(seconds=FAST_POLL_SECONDS),
            always_update=False
        )
        self._hass = hass
        self._controller = controller

    async def _async_update_data(self):
        """Fetch data from API endpoint.

        This is the place to pre-process the data to lookup tables
        so entities can quickly look up their data.
        """
        try:
            # Note: asyncio.TimeoutError and aiohttp.ClientError are already
            # handled by the data update coordinator.
            async with async_timeout.timeout(10):
                return await self._hass.async_add_executor_job(self._controller.get_cell)

        except Exception as err:
            raise UpdateFailed(f"Error communicating with API: {err}")


class SlowCoordinator(DataUpdateCoordinator):
    """Rapid refresh coordinator."""

    def __init__(self, hass, controller):
        """Initialize fast coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name="T-Mobile Home Internet",
            # Polling interval. Will only be polled if there are subscribers.
            update_interval=timedelta(seconds=SLOW_POLL_SECONDS),
            always_update=False
        )
        self._hass = hass
        self._controller = controller
        self._sim = None
        self._gateway = None

    async def _async_setup(self):
        """Set up the coordinator

        This is the place to set up your coordinator,
        or to load data, that only needs to be loaded once.

        This method will be called automatically during
        coordinator.async_config_entry_first_refresh.
        """
        async with async_timeout.timeout(10):
            config = await self._hass.async_add_executor_job(self._controller.get_gateway_config)
            # Return only "device", since "signal" and "time" contain frequently changing info that will be periodically retrieved elsewhere.
            self._gateway = { "device": config["device"] }

        async with async_timeout.timeout(10):
            self._sim = await self._hass.async_add_executor_job(self._controller.get_sim)


    async def _async_update_data(self):
        """Fetch data from API endpoint.

        This is the place to pre-process the data to lookup tables
        so entities can quickly look up their data.
        """
        try:
            # Note: asyncio.TimeoutError and aiohttp.ClientError are already
            # handled by the data update coordinator.
            async with async_timeout.timeout(30):
                _access_point = {"access_point":  await self._hass.async_add_executor_job(self._controller.get_ap_config, GET_ACCESS_POINT_RETRIES, GET_ACCESS_POINT_RETRY_SECONDS) }

            async with async_timeout.timeout(10):
                config =  await self._hass.async_add_executor_job(self._controller.get_gateway_config)
                _time = { "time": config["time"] }

            async with async_timeout.timeout(10):
                _clients = await self._hass.async_add_executor_job(self._controller.get_clients)

            return _access_point | _time | _clients

        except Exception as err:
            raise UpdateFailed(f"Error communicating with API: {err}")


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok
