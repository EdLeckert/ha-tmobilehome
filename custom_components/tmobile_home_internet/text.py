"""The Home Assistant T-Mobile Home Internet integration."""
import logging
from typing import Callable

from homeassistant.components.text import (TextEntity)
from homeassistant.core import HomeAssistant
from homeassistant.util import slugify
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers import entity_platform
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import (
    DOMAIN,
    SSID_NAME_PATTERN,
    SSID_PASSWORD_PATTERN,
)

from .utils import set_edits_pending

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(
    hass: HomeAssistant,
    entry: dict,
    async_add_entities: Callable,
):
    """Set up the Home Assistant T-Mobile Home Internet texts."""
    entities = _create_entities(hass, entry)
    async_add_entities(entities)


def _create_entities(hass: HomeAssistant, entry: dict):
    entities = []
    slow_coordinator = hass.data[DOMAIN][entry.entry_id]["slow_coordinator"]

    entities.append(GatewayEditSSIDNameText(hass, slow_coordinator))
    entities.append(GatewayEditSSIDPasswordText(hass, slow_coordinator))

    return entities


class GatewayText(CoordinatorEntity, TextEntity):
    """Represent a text for the gateway."""

    def __init__(self, hass, coordinator):
        """Set up a new HA T-Mobile Home Internet text."""
        self._hass = hass
        self._coordinator = coordinator
        self._entity_type = "text"
        super().__init__(coordinator)
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, coordinator.config_entry.entry_id)},
        )


class GatewayEditSSIDNameText(GatewayText):
    """Represent a text for the gateway."""
    _attr_should_poll = False
    _attr_state: None = None

    def __init__(self, hass, coordinator):
        """Set up a new HA T-Mobile Home Internet SSID text."""
        super().__init__(hass, coordinator)


    @property
    def icon(self) -> str:
        """Return icon."""
        return "mdi:access-point"

    @property
    def name(self) -> str:
        """Return the name of this text."""
        return f"T-Mobile Edit SSID Name"

    @property
    def unique_id(self) -> str:
        """Return a unique, Home Assistant friendly identifier for this entity."""
        return slugify(f"{self._entity_type}_tmobile_home_internet_edit_ssid_name")

    @property
    def entity_registry_visible_default(self) -> bool:
        """Set entity hidden by default."""
        return False

    @property
    def pattern(self) -> str:
        """A regex pattern that the text value must match to be valid."""
        return SSID_NAME_PATTERN

    @property
    def native_min(self) -> int:
        """Return the value of this text."""
        return 1

    @property
    def native_max(self) -> int:
        """Return the value of this text."""
        return 28

    @property
    def native_value(self) -> int:
        """Return the value of this text."""
        return self._attr_state

    async def async_set_value(self, value: str) -> None:
        """Change the value."""
        self._attr_state = value
        self.async_write_ha_state()

        # Show edits pending
        await set_edits_pending(True)


class GatewayEditSSIDPasswordText(GatewayText):
    """Represent a text for the gateway."""
    _attr_should_poll = False
    _attr_state: None = None

    def __init__(self, hass, coordinator):
        """Set up a new HA T-Mobile Home Internet SSID wpaKey text."""
        super().__init__(hass, coordinator)

    @property
    def icon(self) -> str:
        """Return icon."""
        return "mdi:access-point"

    @property
    def name(self) -> str:
        """Return the name of this text."""
        return f"T-Mobile Edit SSID Password"

    @property
    def unique_id(self) -> str:
        """Return a unique, Home Assistant friendly identifier for this entity."""
        return slugify(f"{self._entity_type}_tmobile_home_internet_edit_ssid_password")

    @property
    def entity_registry_visible_default(self) -> bool:
        """Set entity hidden by default."""
        return False

    @property
    def pattern(self) -> str:
        """A regex pattern that the text value must match to be valid."""
        return SSID_PASSWORD_PATTERN

    @property
    def native_min(self) -> int:
        """Return the value of this text."""
        return 8

    @property
    def native_max(self) -> int:
        """Return the value of this text."""
        return 63

    @property
    def native_value(self) -> int:
        """Return the value of this text."""
        return self._attr_state

    async def async_set_value(self, value: str) -> None:
        """Change the value."""
        self._attr_state = value
        self.async_write_ha_state()

        # Show edits pending
        await set_edits_pending(True)

