"""The Home Assistant T-Mobile Home Internet integration."""
import logging
from typing import Callable, Dict

from homeassistant.components.switch import (SwitchEntity)
from homeassistant.core import HomeAssistant
from homeassistant.util import slugify
from homeassistant.helpers import entity_platform, service
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

    platform = entity_platform.async_get_current_platform()

    # # This will call Entity._reboot_gateway
    # platform.async_register_entity_service(
    #     SERVICE_REBOOT_GATEWAY,
    #     SCHEMA_SERVICE_REBOOT_GATEWAY,
    #     "_reboot_gateway",
    # )


def _create_entities(hass: HomeAssistant, entry: dict):
    entities = []
    slow_coordinator = hass.data[DOMAIN][entry.entry_id]["slow_coordinator"]
    controller = hass.data[DOMAIN][entry.entry_id]["controller"]

    entities.append(GatewayWiFi24GHzSwitch(hass, entry, slow_coordinator, controller))
    entities.append(GatewayWiFi50GHzSwitch(hass, entry, slow_coordinator, controller))

    return entities


class GatewayWiFi24GHzSwitch(CoordinatorEntity, SwitchEntity):
    """Represent a switch for the gateway."""

    def __init__(self, hass, entry, coordinator, controller):
        """Set up a new HA T-Mobile Home Internet WiFi 2.4GHz switch."""
        self._hass = hass
        self._entry = entry
        self._coordinator = coordinator
        self._controller = controller
        self._entity_type = "switch"
        super().__init__(coordinator)

    @property
    def icon(self) -> str:
        """Return icon."""
        return "mdi:access-point"

    @property
    def name(self) -> str:
        """Return the name of this switch."""
        return f"T-Mobile Home Internet WiFi 2.4GHz"

    @property
    def unique_id(self) -> str:
        """Return a unique, Home Assistant friendly identifier for this entity."""
        return slugify(f"{self._entity_type}_tmobile_home_internet_wifi_2_4GHz")

    @property
    def extra_state_attributes(self):
        return { 
            "warning": "Turning off the 2.4GHz radio disables WiFi on this frequency. Only turn WiFi off if you have a wired connection to your gateway.",
            "notice": "Gateway will reset if this setting is changed, and may lose communications for a minute or more." 
            }

    @property
    def is_on(self) -> bool:
        """Return the value of this switch."""
        return bool(self.coordinator.data["access_point"]["2.4ghz"]["isRadioEnabled"])

    async def async_turn_on(self, **kwargs):
        """Enable WiFi 2.4GHz."""
        access_point = self.coordinator.data["access_point"]
        access_point["2.4ghz"]["isRadioEnabled"] = True
        await self._hass.async_add_executor_job(self._controller.set_ap_config, access_point)
        # Doing an async_request_refresh here won't work as the router is resetting.
        self._attr_is_on = True
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs):
        """Disable WiFi 2.4GHz."""
        access_point = self.coordinator.data["access_point"]
        access_point["2.4ghz"]["isRadioEnabled"] = False
        await self._hass.async_add_executor_job(self._controller.set_ap_config, access_point)
        # Doing an async_request_refresh here won't work as the router is resetting.
        self._attr_is_on = False
        self.async_write_ha_state()

class GatewayWiFi50GHzSwitch(CoordinatorEntity, SwitchEntity):
    """Represent a switch for the gateway."""

    def __init__(self, hass, entry, coordinator, controller):
        """Set up a new HA T-Mobile Home Internet WiFi 5.0GHz switch."""
        self._hass = hass
        self._entry = entry
        self._coordinator = coordinator
        self._controller = controller
        self._entity_type = "switch"
        super().__init__(coordinator)

    @property
    def icon(self) -> str:
        """Return icon."""
        return "mdi:access-point"

    @property
    def name(self) -> str:
        """Return the name of this switch."""
        return f"T-Mobile Home Internet WiFi 5.0GHz"

    @property
    def unique_id(self) -> str:
        """Return a unique, Home Assistant friendly identifier for this entity."""
        return slugify(f"{self._entity_type}_tmobile_home_internet_wifi_5_0GHz")

    @property
    def extra_state_attributes(self):
        return { 
            "warning": "Turning off the 5.0GHz radio disables WiFi on this frequency. Only turn WiFi off if you have a wired connection to your gateway.",
            "notice": "Gateway will reset if this setting is changed, and may lose communications for a minute or more." 
            }

    @property
    def is_on(self) -> bool:
        """Return the value of this switch."""
        return bool(self.coordinator.data["access_point"]["5.0ghz"]["isRadioEnabled"])

    async def async_turn_on(self, **kwargs):
        """Enable WiFi 5.0GHz."""
        access_point = self.coordinator.data["access_point"]
        access_point["5.0ghz"]["isRadioEnabled"] = True
        await self._hass.async_add_executor_job(self._controller.set_ap_config, access_point)
        # Doing an async_request_refresh here won't work as the router is resetting.
        self._attr_is_on = True
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs):
        """Disable WiFi 5.GHz."""
        access_point = self.coordinator.data["access_point"]
        access_point["5.0ghz"]["isRadioEnabled"] = False
        await self._hass.async_add_executor_job(self._controller.set_ap_config, access_point)
        # Doing an async_request_refresh here won't work as the router is resetting.
        self._attr_is_on = False
        self.async_write_ha_state()
