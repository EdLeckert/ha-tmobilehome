"""The Home Assistant T-Mobile Home Internet integration."""
import logging
from typing import Callable, Dict

from homeassistant.components.switch import (SwitchEntity)
from homeassistant.core import HomeAssistant
from homeassistant.util import slugify
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers import entity_platform
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import (
    DOMAIN,
)

from .utils import set_edits_pending

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

    entities.append(GatewayWiFi24GHzSwitch(hass, entry, slow_coordinator, controller))
    entities.append(GatewayWiFi50GHzSwitch(hass, entry, slow_coordinator, controller))
    entities.append(GatewayEditSSIDsEditsPendingSwitch(hass, entry, slow_coordinator, controller))
    entities.append(GatewayEditSSIDsEditsNameValidSwitch(hass, entry, slow_coordinator, controller))
    entities.append(GatewayEditSSIDsEditsPasswordValidSwitch(hass, entry, slow_coordinator, controller))
    entities.append(GatewayEditSSIDsEditsSavingSwitch(hass, entry, slow_coordinator, controller))
    entities.append(GatewayEditSSIDHiddenSwitch(hass, entry, slow_coordinator, controller))
    entities.append(GatewayEditSSIDGuestSwitch(hass, entry, slow_coordinator, controller))
    entities.append(GatewayEditSSID24GHzSwitch(hass, entry, slow_coordinator, controller))
    entities.append(GatewayEditSSID50GHzSwitch(hass, entry, slow_coordinator, controller))
    entities.append(GatewayEditSSID60GHzSwitch(hass, entry, slow_coordinator, controller))

    return entities


class GatewaySwitch(CoordinatorEntity, SwitchEntity):
    """Represent a switch for the gateway."""

    def __init__(self, hass, entry, coordinator, controller):
        """Set up a new HA T-Mobile Home Internet switch."""
        self._hass = hass
        self._entry = entry
        self._coordinator = coordinator
        self._controller = controller
        self._entity_type = "switch"
        super().__init__(coordinator)
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, coordinator.config_entry.entry_id)},
        )


class GatewayWiFi24GHzSwitch(GatewaySwitch):
    """Represent a switch for the gateway."""

    def __init__(self, hass, entry, coordinator, controller):
        """Set up a new HA T-Mobile Home Internet WiFi 2.4GHz switch."""
        super().__init__(hass, entry, coordinator, controller)

    @property
    def icon(self) -> str:
        """Return icon."""
        return "mdi:access-point"

    @property
    def name(self) -> str:
        """Return the name of this switch."""
        return f"T-Mobile Wi-Fi 2.4GHz"

    @property
    def unique_id(self) -> str:
        """Return a unique, Home Assistant friendly identifier for this entity."""
        return slugify(f"{self._entity_type}_tmobile_home_internet_wifi_2_4GHz")

    @property
    def entity_registry_enabled_default(self) -> bool:
        """Set entity disabled by default."""
        return False

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
        # Doing an async_request_refresh here won't work as the gateway is resetting.
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

class GatewayWiFi50GHzSwitch(GatewaySwitch):
    """Represent a switch for the gateway."""

    def __init__(self, hass, entry, coordinator, controller):
        """Set up a new HA T-Mobile Home Internet WiFi 5.0GHz switch."""
        super().__init__(hass, entry, coordinator, controller)

    @property
    def icon(self) -> str:
        """Return icon."""
        return "mdi:access-point"

    @property
    def name(self) -> str:
        """Return the name of this switch."""
        return f"T-Mobile Wi-Fi 5.0GHz"

    @property
    def unique_id(self) -> str:
        """Return a unique, Home Assistant friendly identifier for this entity."""
        return slugify(f"{self._entity_type}_tmobile_home_internet_wifi_5_0GHz")

    @property
    def entity_registry_enabled_default(self) -> bool:
        """Set entity disabled by default."""
        return False

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


class GatewayWiFi60GHzSwitch(GatewaySwitch):
    """Represent a switch for the gateway."""

    def __init__(self, hass, entry, coordinator, controller):
        """Set up a new HA T-Mobile Home Internet WiFi 6.0GHz switch."""
        super().__init__(hass, entry, coordinator, controller)

    @property
    def icon(self) -> str:
        """Return icon."""
        return "mdi:access-point"

    @property
    def name(self) -> str:
        """Return the name of this switch."""
        return f"T-Mobile Wi-Fi 6.0GHz"

    @property
    def unique_id(self) -> str:
        """Return a unique, Home Assistant friendly identifier for this entity."""
        return slugify(f"{self._entity_type}_tmobile_home_internet_wifi_6_0GHz")

    @property
    def entity_registry_enabled_default(self) -> bool:
        """Set entity disabled by default."""
        return False

    @property
    def extra_state_attributes(self):
        return {
            "warning": "Turning off the 6.0GHz radio disables WiFi on this frequency. Only turn WiFi off if you have a wired connection to your gateway.",
            "notice": "Gateway will reset if this setting is changed, and may lose communications for a minute or more."
            }

    @property
    def is_on(self) -> bool:
        """Return the value of this switch."""
        access_point = self.coordinator.data["access_point"]
        if "6.0ghz" in access_point:
          return bool(access_point["6.0ghz"]["isRadioEnabled"])
        return False

    async def async_turn_on(self, **kwargs):
        """Enable WiFi 6.0GHz."""
        access_point = self.coordinator.data["access_point"]
        if "6.0ghz" in access_point:
          access_point["6.0ghz"]["isRadioEnabled"] = True
          await self._hass.async_add_executor_job(self._controller.set_ap_config, access_point)
          # Doing an async_request_refresh here won't work as the router is resetting.
          self._attr_is_on = True
          self.async_write_ha_state()
        else:
          raise Exception("6.0GHz band not supported by this gateway.")

    async def async_turn_off(self, **kwargs):
        """Disable WiFi 6.GHz."""
        access_point = self.coordinator.data["access_point"]
        if "6.0ghz" in access_point:
          access_point["6.0ghz"]["isRadioEnabled"] = False
          await self._hass.async_add_executor_job(self._controller.set_ap_config, access_point)
          # Doing an async_request_refresh here won't work as the router is resetting.
          self._attr_is_on = False
          self.async_write_ha_state()
        else:
          raise Exception("6.0GHz band not supported by this gateway.")


class GatewayEditSSIDsEditsPendingSwitch(GatewaySwitch):
    """Represent a switch for the gateway."""

    _attr_is_on: bool = False

    def __init__(self, hass, entry, coordinator, controller):
        """Set up a new HA T-Mobile Home Internet Edits Pending switch."""
        super().__init__(hass, entry, coordinator, controller)

    @property
    def icon(self) -> str:
        """Return icon."""
        return "mdi:access-point"

    @property
    def name(self) -> str:
        """Return the name of this switch."""
        return f"T-Mobile Edit SSID Edits Pending"

    @property
    def unique_id(self) -> str:
        """Return a unique, Home Assistant friendly identifier for this entity."""
        return slugify(f"{self._entity_type}_tmobile_home_internet_edit_ssid_edits_pending")

    @property
    def entity_registry_visible_default(self) -> bool:
        """Set entity invisible by default."""
        return False

    @property
    def is_on(self) -> bool:
        """Return the value of this switch."""
        return self._attr_is_on

    async def async_turn_on(self, **kwargs):
        """Note edit pending."""
        self._attr_is_on = True
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs):
        """Note edit no longer pending."""
        self._attr_is_on = False
        self.async_write_ha_state()


class GatewayEditSSIDsEditsNameValidSwitch(GatewaySwitch):
    """Represent a switch for the gateway."""

    _attr_is_on: bool = True

    def __init__(self, hass, entry, coordinator, controller):
        """Set up a new HA T-Mobile Home Internet Edits Name Valid switch."""
        super().__init__(hass, entry, coordinator, controller)

    @property
    def icon(self) -> str:
        """Return icon."""
        return "mdi:access-point"

    @property
    def name(self) -> str:
        """Return the name of this switch."""
        return f"T-Mobile Edit SSID Edits Name Valid"

    @property
    def unique_id(self) -> str:
        """Return a unique, Home Assistant friendly identifier for this entity."""
        return slugify(f"{self._entity_type}_tmobile_home_internet_edit_ssid_edits_name_valid")

    @property
    def entity_registry_visible_default(self) -> bool:
        """Set entity invisible by default."""
        return False

    @property
    def is_on(self) -> bool:
        """Return the value of this switch."""
        return self._attr_is_on

    async def async_turn_on(self, **kwargs):
        """Note edited name valid."""
        self._attr_is_on = True
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs):
        """Note edited name not valid."""
        self._attr_is_on = False
        self.async_write_ha_state()


class GatewayEditSSIDsEditsPasswordValidSwitch(GatewaySwitch):
    """Represent a switch for the gateway."""

    _attr_is_on: bool = True

    def __init__(self, hass, entry, coordinator, controller):
        """Set up a new HA T-Mobile Home Internet Edits Password Valid switch."""
        super().__init__(hass, entry, coordinator, controller)

    @property
    def icon(self) -> str:
        """Return icon."""
        return "mdi:access-point"

    @property
    def name(self) -> str:
        """Return the name of this switch."""
        return f"T-Mobile Edit SSID Edits Password Valid"

    @property
    def unique_id(self) -> str:
        """Return a unique, Home Assistant friendly identifier for this entity."""
        return slugify(f"{self._entity_type}_tmobile_home_internet_edit_ssid_edits_password_valid")

    @property
    def entity_registry_visible_default(self) -> bool:
        """Set entity invisible by default."""
        return False

    @property
    def is_on(self) -> bool:
        """Return the value of this switch."""
        return self._attr_is_on

    async def async_turn_on(self, **kwargs):
        """Note edited password valid."""
        self._attr_is_on = True
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs):
        """Note edited password not valid."""
        self._attr_is_on = False
        self.async_write_ha_state()


class GatewayEditSSIDsEditsSavingSwitch(GatewaySwitch):
    """Represent a switch for the gateway."""

    _attr_is_on: bool = False

    def __init__(self, hass, entry, coordinator, controller):
        """Set up a new HA T-Mobile Home Internet Edits Saving switch."""
        super().__init__(hass, entry, coordinator, controller)

    @property
    def icon(self) -> str:
        """Return icon."""
        return "mdi:access-point"

    @property
    def name(self) -> str:
        """Return the name of this switch."""
        return f"T-Mobile Edit SSID Edits Saving"

    @property
    def unique_id(self) -> str:
        """Return a unique, Home Assistant friendly identifier for this entity."""
        return slugify(f"{self._entity_type}_tmobile_home_internet_edit_ssid_edits_saving")

    @property
    def entity_registry_visible_default(self) -> bool:
        """Set entity invisible by default."""
        return False

    @property
    def is_on(self) -> bool:
        """Return the value of this switch."""
        return self._attr_is_on

    async def async_turn_on(self, **kwargs):
        """Note edit saving."""
        self._attr_is_on = True
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs):
        """Note edit no longer saving."""
        self._attr_is_on = False
        self.async_write_ha_state()


class GatewayEditSSIDHiddenSwitch(GatewaySwitch):
    """Represent a switch for the gateway."""

    _attr_is_on: bool | None = None

    def __init__(self, hass, entry, coordinator, controller):
        """Set up a new HA T-Mobile Home Internet edit SSID Hidden switch."""
        super().__init__(hass, entry, coordinator, controller)

    @property
    def icon(self) -> str:
        """Return icon."""
        return "mdi:access-point"

    @property
    def name(self) -> str:
        """Return the name of this switch."""
        return f"T-Mobile Edit SSID Hidden"

    @property
    def unique_id(self) -> str:
        """Return a unique, Home Assistant friendly identifier for this entity."""
        return slugify(f"{self._entity_type}_tmobile_home_internet_edit_ssid_hidden")

    @property
    def entity_registry_visible_default(self) -> bool:
        """Set entity hidden by default."""
        return False

    @property
    def is_on(self) -> bool:
        """Return the value of this switch."""
        return self._attr_is_on

    async def async_turn_on(self, **kwargs):
        """Hide SSID."""
        self._attr_is_on = True
        self.async_write_ha_state()

        # Show edits pending
        await set_edits_pending(True)

    async def async_turn_off(self, **kwargs):
        """Expose SSID."""
        self._attr_is_on = False
        self.async_write_ha_state()

        # Show edits pending
        await set_edits_pending(True)


class GatewayEditSSIDGuestSwitch(GatewaySwitch):
    """Represent a switch for the gateway."""

    _attr_is_on: bool | None = None

    def __init__(self, hass, entry, coordinator, controller):
        """Set up a new HA T-Mobile Home Internet edit SSID Guest switch."""
        super().__init__(hass, entry, coordinator, controller)

    @property
    def icon(self) -> str:
        """Return icon."""
        return "mdi:access-point"

    @property
    def name(self) -> str:
        """Return the name of this switch."""
        return f"T-Mobile Edit SSID Guest"

    @property
    def unique_id(self) -> str:
        """Return a unique, Home Assistant friendly identifier for this entity."""
        return slugify(f"{self._entity_type}_tmobile_home_internet_edit_ssid_guest")

    @property
    def entity_registry_visible_default(self) -> bool:
        """Set entity hidden by default."""
        return False

    @property
    def is_on(self) -> bool:
        """Return the value of this switch."""
        return self._attr_is_on

    async def async_turn_on(self, **kwargs):
        """Set guest mode."""
        self._attr_is_on = True
        self.async_write_ha_state()

        # Show edits pending
        await set_edits_pending(True)

    async def async_turn_off(self, **kwargs):
        """Clear guest mode."""
        self._attr_is_on = False
        self.async_write_ha_state()

        # Show edits pending
        await set_edits_pending(True)


class GatewayEditSSID24GHzSwitch(GatewaySwitch):
    """Represent a switch for the gateway."""

    _attr_is_on: bool | None = None

    def __init__(self, hass, entry, coordinator, controller):
        """Set up a new HA T-Mobile Home Internet edit SSID 2.4GHz switch."""
        super().__init__(hass, entry, coordinator, controller)

    @property
    def icon(self) -> str:
        """Return icon."""
        return "mdi:access-point"

    @property
    def name(self) -> str:
        """Return the name of this switch."""
        return f"T-Mobile Edit SSID 2.4GHz"

    @property
    def unique_id(self) -> str:
        """Return a unique, Home Assistant friendly identifier for this entity."""
        return slugify(f"{self._entity_type}_tmobile_home_internet_edit_ssid_2_4ghz")

    @property
    def entity_registry_visible_default(self) -> bool:
        """Set entity hidden by default."""
        return False

    @property
    def is_on(self) -> bool:
        """Return the value of this switch."""
        return self._attr_is_on

    async def async_turn_on(self, **kwargs):
        """Enable 2.4GHz band."""
        self._attr_is_on = True
        self.async_write_ha_state()

        # Show edits pending
        await set_edits_pending(True)

    async def async_turn_off(self, **kwargs):
        """Disable 2.4GHz band."""
        self._attr_is_on = False
        self.async_write_ha_state()

        # Show edits pending
        await set_edits_pending(True)


class GatewayEditSSID50GHzSwitch(GatewaySwitch):
    """Represent a switch for the gateway."""

    _attr_is_on: bool | None = None

    def __init__(self, hass, entry, coordinator, controller):
        """Set up a new HA T-Mobile Home Internet edit SSID 5.0GHz switch."""
        super().__init__(hass, entry, coordinator, controller)

    @property
    def icon(self) -> str:
        """Return icon."""
        return "mdi:access-point"

    @property
    def name(self) -> str:
        """Return the name of this switch."""
        return f"T-Mobile Edit SSID 5.0GHz"

    @property
    def unique_id(self) -> str:
        """Return a unique, Home Assistant friendly identifier for this entity."""
        return slugify(f"{self._entity_type}_tmobile_home_internet_edit_ssid_5_0ghz")

    @property
    def entity_registry_visible_default(self) -> bool:
        """Set entity hidden by default."""
        return False

    @property
    def is_on(self) -> bool:
        """Return the value of this switch."""
        return self._attr_is_on

    async def async_turn_on(self, **kwargs):
        """Enable 5.0GHz band."""
        self._attr_is_on = True
        self.async_write_ha_state()

        # Show edits pending
        await set_edits_pending(True)

    async def async_turn_off(self, **kwargs):
        """Disable 5.0GHz band."""
        self._attr_is_on = False
        self.async_write_ha_state()

        # Show edits pending
        await set_edits_pending(True)


class GatewayEditSSID60GHzSwitch(GatewaySwitch):
    """Represent a switch for the gateway."""

    _attr_is_on: bool | None = None

    def __init__(self, hass, entry, coordinator, controller):
        """Set up a new HA T-Mobile Home Internet edit SSID 6.0GHz switch."""
        super().__init__(hass, entry, coordinator, controller)

    @property
    def icon(self) -> str:
        """Return icon."""
        return "mdi:access-point"

    @property
    def name(self) -> str:
        """Return the name of this switch."""
        return f"T-Mobile Edit SSID 6.0GHz"

    @property
    def unique_id(self) -> str:
        """Return a unique, Home Assistant friendly identifier for this entity."""
        return slugify(f"{self._entity_type}_tmobile_home_internet_edit_ssid_6_0ghz")

    @property
    def entity_registry_enabled_default(self) -> bool:
        """Set entity disabled by default."""
        return False

    @property
    def entity_registry_visible_default(self) -> bool:
        """Set entity hidden by default."""
        return False

    @property
    def is_on(self) -> bool:
        """Return the value of this switch."""
        return self._attr_is_on

    async def async_turn_on(self, **kwargs):
        """Enable 6.0GHz band."""
        self._attr_is_on = True
        self.async_write_ha_state()

        # Show edits pending
        await set_edits_pending(True)

    async def async_turn_off(self, **kwargs):
        """Disable 6.0GHz band."""
        self._attr_is_on = False
        self.async_write_ha_state()

        # Show edits pending
        await set_edits_pending(True)
