"""The Home Assistant T-Mobile Home Internet integration."""
import logging
from typing import Callable, Dict

from homeassistant.components.select import (SelectEntity)
from homeassistant.core import HomeAssistant
from homeassistant.util import slugify
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers import entity_platform
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import (
    DOMAIN,
)

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: dict,
    async_add_entities: Callable,
):
    """Set up the Home Assistant T-Mobile Home Internet switches."""
    entities = _create_entities(hass, entry)
    async_add_entities(entities)


def _create_entities(hass: HomeAssistant, entry: dict):
    entities = []
    slow_coordinator = hass.data[DOMAIN][entry.entry_id]["slow_coordinator"]
    controller = hass.data[DOMAIN][entry.entry_id]["controller"]

    entities.append(GatewayWiFi24GHzChannelSelect(hass, entry, slow_coordinator, controller))
    entities.append(GatewayWiFi50GHzChannelSelect(hass, entry, slow_coordinator, controller))
    entities.append(GatewayWiFi24GHzBandwidthSelect(hass, entry, slow_coordinator, controller))
    entities.append(GatewayWiFi50GHzBandwidthSelect(hass, entry, slow_coordinator, controller))

    return entities


class GatewaySelect(CoordinatorEntity, SelectEntity):
    """Represent a select for the gateway."""

    def __init__(self, hass, entry, coordinator, controller):
        """Set up a new HA T-Mobile Home Internet select."""
        self._hass = hass
        self._entry = entry
        self._coordinator = coordinator
        self._controller = controller
        self._entity_type = "select"
        super().__init__(coordinator)
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, coordinator.config_entry.entry_id)},
        )


class GatewayWiFi24GHzChannelSelect(GatewaySelect):
    """Represent a select for the gateway."""

    def __init__(self, hass, entry, coordinator, controller):
        """Set up a new HA T-Mobile Home Internet WiFi 2.4GHz channel select."""
        super().__init__(hass, entry, coordinator, controller)

    @property
    def icon(self) -> str:
        """Return icon."""
        return "mdi:access-point"

    @property
    def name(self) -> str:
        """Return the name of this select."""
        return f"T-Mobile Wi-Fi 2.4GHz Channel"

    @property
    def unique_id(self) -> str:
        """Return a unique, Home Assistant friendly identifier for this entity."""
        return slugify(f"{self._entity_type}_tmobile_home_internet_wifi_2_4GHz_channel")

    @property
    def options(self) -> list[str]:
        """A list of available options as strings"""
        return ["Auto", "1", "2", "3"]

    @property
    def current_option(self) -> str:
        """The current select option"""
        access_point = self._coordinator.data["access_point"]
        return access_point["2.4ghz"]["channel"]

    async def async_select_option(self, option: str) -> None:
        """Change the selected option."""
        access_point = self._coordinator.data["access_point"]
        access_point["2.4ghz"]["channel"] = option
        await self._hass.async_add_executor_job(self._controller.set_ap_config, access_point)
        await self._coordinator.async_request_refresh()


class GatewayWiFi50GHzChannelSelect(GatewaySelect):
    """Represent a select for the gateway."""

    def __init__(self, hass, entry, coordinator, controller):
        """Set up a new HA T-Mobile Home Internet WiFi 5.0GHz channel select."""
        super().__init__(hass, entry, coordinator, controller)

    @property
    def icon(self) -> str:
        """Return icon."""
        return "mdi:access-point"

    @property
    def name(self) -> str:
        """Return the name of this select."""
        return f"T-Mobile Wi-Fi 5.0GHz Channel"

    @property
    def unique_id(self) -> str:
        """Return a unique, Home Assistant friendly identifier for this entity."""
        return slugify(f"{self._entity_type}_tmobile_home_internet_wifi_5_0GHz_channel")

    @property
    def options(self) -> list[str]:
        """A list of available options as strings"""
        return ["Auto", "36", "40", "44", "48", "52", "56", "60", "64", "100", "104", "108", "112", "116", "120", "124", "128", "132", "136", "140", "144", "149", "153", "157", "161", "165"]

    @property
    def current_option(self) -> str:
        """The current select option"""
        access_point = self._coordinator.data["access_point"]
        return access_point["5.0ghz"]["channel"]

    async def async_select_option(self, option: str) -> None:
        """Change the selected option."""
        access_point = self._coordinator.data["access_point"]
        access_point["5.0ghz"]["channel"] = option
        await self._hass.async_add_executor_job(self._controller.set_ap_config, access_point)
        await self._coordinator.async_request_refresh()


class GatewayWiFi24GHzBandwidthSelect(GatewaySelect):
    """Represent a select for the gateway."""

    def __init__(self, hass, entry, coordinator, controller):
        """Set up a new HA T-Mobile Home Internet WiFi 2.4GHz bandwidth select."""
        super().__init__(hass, entry, coordinator, controller)

    @property
    def icon(self) -> str:
        """Return icon."""
        return "mdi:access-point"

    @property
    def name(self) -> str:
        """Return the name of this select."""
        return f"T-Mobile Wi-Fi 2.4GHz Bandwidth"

    @property
    def unique_id(self) -> str:
        """Return a unique, Home Assistant friendly identifier for this entity."""
        return slugify(f"{self._entity_type}_tmobile_home_internet_wifi_2_4GHz_bandwidth")

    @property
    def options(self) -> list[str]:
        """A list of available options as strings"""
        return ["Auto", "20MHz", "40MHz"]

    @property
    def current_option(self) -> str:
        """The current select option"""
        access_point = self._coordinator.data["access_point"]
        return access_point["2.4ghz"]["channelBandwidth"]

    async def async_select_option(self, option: str) -> None:
        """Change the selected option."""
        access_point = self._coordinator.data["access_point"]
        access_point["2.4ghz"]["channelBandwidth"] = option
        await self._hass.async_add_executor_job(self._controller.set_ap_config, access_point)
        await self._coordinator.async_request_refresh()


class GatewayWiFi50GHzBandwidthSelect(GatewaySelect):
    """Represent a select for the gateway."""

    def __init__(self, hass, entry, coordinator, controller):
        """Set up a new HA T-Mobile Home Internet WiFi 5.0GHz bandwidth select."""
        super().__init__(hass, entry, coordinator, controller)

    @property
    def icon(self) -> str:
        """Return icon."""
        return "mdi:access-point"

    @property
    def name(self) -> str:
        """Return the name of this select."""
        return f"T-Mobile Wi-Fi 5.0GHz Bandwidth"

    @property
    def unique_id(self) -> str:
        """Return a unique, Home Assistant friendly identifier for this entity."""
        return slugify(f"{self._entity_type}_tmobile_home_internet_wifi_5_0GHz_bandwidth")

    @property
    def options(self) -> list[str]:
        """A list of available options as strings"""
        return ["Auto", "20MHz", "40MHz", "80MHz"]

    @property
    def current_option(self) -> str:
        """The current select option"""
        access_point = self._coordinator.data["access_point"]
        return access_point["5.0ghz"]["channelBandwidth"]

    async def async_select_option(self, option: str) -> None:
        """Change the selected option."""
        access_point = self._coordinator.data["access_point"]
        access_point["5.0ghz"]["channelBandwidth"] = option
        await self._hass.async_add_executor_job(self._controller.set_ap_config, access_point)
        await self._coordinator.async_request_refresh()

