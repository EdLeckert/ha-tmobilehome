"""The Home Assistant T-Mobile Home Internet integration."""
import json
import logging
import time

from typing import Callable, Dict

from homeassistant.components.button import (ButtonEntity)
from homeassistant.core import HomeAssistant
from homeassistant.util import slugify
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers import entity_platform
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import (
    DOMAIN,
)

from .utils import (
    generate_random_hex_string, 
    generate_random_mixed_string, 
    get_ssid_edit_index,
    select_option,
    set_edits_pending, 
    set_edits_saving, 
    set_ssid_edit_controls,
    update_entity,
)

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: dict,
    async_add_entities: Callable,
):
    """Set up the Home Assistant T-Mobile Home Internet buttons."""
    entities = _create_entities(hass, entry)
    async_add_entities(entities)


def _create_entities(hass: HomeAssistant, entry: dict):
    entities = []
    slow_coordinator = hass.data[DOMAIN][entry.entry_id]["slow_coordinator"]
    controller = hass.data[DOMAIN][entry.entry_id]["controller"]

    entities.append(GatewayEditSSIDSaveButton(hass, slow_coordinator, controller))
    entities.append(GatewayEditSSIDCancelButton(hass, slow_coordinator, controller))
    entities.append(GatewayEditSSIDsDeleteButton(hass, slow_coordinator, controller))
    entities.append(GatewayEditSSIDsAddButton(hass, slow_coordinator, controller))

    return entities


class GatewayButton(CoordinatorEntity, ButtonEntity):
    """Represent a button for the gateway."""

    def __init__(self, hass, coordinator, controller):
        """Set up a new HA T-Mobile Home Internet button."""
        self._hass = hass
        self._coordinator = coordinator
        self._controller = controller
        self._entity_type = "button"
        super().__init__(coordinator)
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, coordinator.config_entry.entry_id)},
        )


class GatewayEditSSIDSaveButton(GatewayButton):
    """Represent a button for the gateway."""

    def __init__(self, hass, coordinator, controller):
        """Set up a new HA T-Mobile Home Internet Edit SSID Save button."""
        super().__init__(hass, coordinator, controller)

    @property
    def icon(self) -> str:
        """Return icon."""
        return "mdi:content-save"

    @property
    def name(self) -> str:
        """Return the name of this button."""
        return f"T-Mobile Edit SSID Save"

    @property
    def unique_id(self) -> str:
        """Return a unique, Home Assistant friendly identifier for this entity."""
        return slugify(f"{self._entity_type}_tmobile_home_internet_edit_ssid_save")

    async def async_press(self) -> None:
        """Save edits."""

        if self.hass.states.get("switch.t_mobile_edit_ssid_edits_pending").state == 'on':

            try:

                # Clear edits pending flag
                await set_edits_pending(False)

                # Set edits saving flag
                await set_edits_saving(True)

                # Get the index of the SSID being edited
                ssid_index = get_ssid_edit_index(self._hass)

                # Get the new values to be saved
                new_ssid_name = self.hass.states.get("text.t_mobile_edit_ssid_name").state
                new_ssid_password = self.hass.states.get("text.t_mobile_edit_ssid_password").state
                new_encryption_version = self.hass.states.get("select.t_mobile_edit_ssid_encryption_version").state
                new_isBroadcastEnabled = True if self.hass.states.get("switch.t_mobile_edit_ssid_hidden").state == 'off' else False
                new_guest = True if self.hass.states.get("switch.t_mobile_edit_ssid_guest").state == 'on' else False
                new_ssid2_4ghz = True if self.hass.states.get("switch.t_mobile_edit_ssid_2_4ghz").state == 'on' else False
                new_ssid5_0ghz = True if self.hass.states.get("switch.t_mobile_edit_ssid_5_0ghz").state == 'on' else False

                # Get current gateway values
                access_point = self._coordinator.data["access_point"]

                # Save edited values
                access_point["ssids"][ssid_index]["ssidName"] = new_ssid_name
                access_point["ssids"][ssid_index]["wpaKey"] = new_ssid_password
                access_point["ssids"][ssid_index]["encryptionVersion"] = new_encryption_version
                access_point["ssids"][ssid_index]["isBroadcastEnabled"] = new_isBroadcastEnabled
                access_point["ssids"][ssid_index]["guest"] = new_guest
                access_point["ssids"][ssid_index]["2.4ghzSsid"] = new_ssid2_4ghz
                access_point["ssids"][ssid_index]["5.0ghzSsid"] = new_ssid5_0ghz

                # Write changes to gateway and refresh coordinator
                await self._hass.async_add_executor_job(self._controller.set_ap_config, access_point)
                await self._coordinator.async_request_refresh()

                # Set editing controls to current settings - should only be different if failure to update gateway
                await set_ssid_edit_controls(self._hass, self._coordinator, ssid_index)

                # If change to ssid name, refresh the select control and select newly named option.
                current_ssid_name = access_point["ssids"][ssid_index]["ssidName"]
                select_ssid_name = self.hass.states.get("select.t_mobile_edit_ssids").state
                if current_ssid_name != select_ssid_name:
                    await update_entity("select.t_mobile_edit_ssids")

                    # Delay is necessary to allow entity to stabilize.
                    await self.hass.async_add_executor_job(time.sleep, 0.05)

                    await select_option("select.t_mobile_edit_ssids", current_ssid_name)

            finally:
                # Clear edits saving flag
                await set_edits_saving(False)


class GatewayEditSSIDCancelButton(GatewayButton):
    """Represent a button for the gateway."""

    def __init__(self, hass, coordinator, controller):
        """Set up a new HA T-Mobile Home Internet Edit SSID Cancel button."""
        super().__init__(hass, coordinator, controller)

    @property
    def icon(self) -> str:
        """Return icon."""
        return "mdi:cancel"

    @property
    def name(self) -> str:
        """Return the name of this button."""
        return f"T-Mobile Edit SSID Cancel"

    @property
    def unique_id(self) -> str:
        """Return a unique, Home Assistant friendly identifier for this entity."""
        return slugify(f"{self._entity_type}_tmobile_home_internet_edit_ssid_cancel")

    async def async_press(self) -> None:
        """Cancel edits."""
        if self.hass.states.get("switch.t_mobile_edit_ssid_edits_pending").state == 'on':

            # Get the index of the SSID being edited
            ssid_index = get_ssid_edit_index(self._hass)

            # Restore the original values
            await set_ssid_edit_controls(self._hass, self._coordinator, ssid_index)


class GatewayEditSSIDsDeleteButton(GatewayButton):
    """Represent a button for the gateway."""

    def __init__(self, hass, coordinator, controller):
        """Set up a new HA T-Mobile Home Internet Edit SSIDs Delete button."""
        super().__init__(hass, coordinator, controller)

    @property
    def icon(self) -> str:
        """Return icon."""
        return "mdi:delete"

    @property
    def name(self) -> str:
        """Return the name of this button."""
        return f"T-Mobile Edit SSIDs Delete"

    @property
    def unique_id(self) -> str:
        """Return a unique, Home Assistant friendly identifier for this entity."""
        return slugify(f"{self._entity_type}_tmobile_home_internet_edit_ssids_delete")

    async def async_press(self) -> None:
        """Delete SSID."""
        # Set edits saving flag
        await set_edits_saving(True)

        try:

            # Get the index of the SSID being edited
            ssid_index = get_ssid_edit_index(self._hass)

            if ssid_index > 0:
                # Get current gateway values
                access_point = self._coordinator.data["access_point"]

                # Delete the SSID
                del access_point["ssids"][ssid_index]

                # Write changes to gateway and refresh coordinator
                await self._hass.async_add_executor_job(self._controller.set_ap_config, access_point)
                await self._coordinator.async_request_refresh()

                # Refresh the select control
                await update_entity("select.t_mobile_edit_ssids")

        finally:
            # Clear edits saving flag
            await set_edits_saving(False)


class GatewayEditSSIDsAddButton(GatewayButton):
    """Represent a button for the gateway."""

    def __init__(self, hass, coordinator, controller):
        """Set up a new HA T-Mobile Home Internet Edit SSIDs Add button."""
        super().__init__(hass, coordinator, controller)

    @property
    def icon(self) -> str:
        """Return icon."""
        return "mdi:access-point-plus"

    @property
    def name(self) -> str:
        """Return the name of this button."""
        return f"T-Mobile Edit SSIDs Add"

    @property
    def unique_id(self) -> str:
        """Return a unique, Home Assistant friendly identifier for this entity."""
        return slugify(f"{self._entity_type}_tmobile_home_internet_edit_ssids_add")

    async def async_press(self) -> None:
        """Create new SSID."""
        # Set edits saving flag
        await set_edits_saving(True)

        try:
            access_point = self._coordinator.data["access_point"]

            if len(access_point["ssids"]) < 4:

                # Load default values for new SSID
                new_ssid = {}
                new_ssid["ssidName"] = "TMOBILE-" + generate_random_hex_string(4)
                new_ssid["wpaKey"] = generate_random_mixed_string(12)
                new_ssid["encryptionMode"] = "AES"
                new_ssid["encryptionVersion"] = "WPA2/WPA3"
                new_ssid["isBroadcastEnabled"] = True
                new_ssid["guest"] = False
                new_ssid["2.4ghzSsid"] = True
                new_ssid["5.0ghzSsid"] = True

                access_point["ssids"].append(new_ssid)

                # Write changes to gateway and refresh coordinator
                await self._hass.async_add_executor_job(self._controller.set_ap_config, access_point)
                await self._coordinator.async_request_refresh()

                # Refresh select entity with new options.
                await update_entity("select.t_mobile_edit_ssids")

                # Delay is necessary to allow entity to stabilize.
                await self.hass.async_add_executor_job(time.sleep, 0.05)

                # Set editing controls to new entry.
                await select_option("select.t_mobile_edit_ssids", new_ssid["ssidName"])

        finally:
            # Clear edits saving flag
            await set_edits_saving(False)
