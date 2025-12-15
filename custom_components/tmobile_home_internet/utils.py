"""The Home Assistant T-Mobile Home Internet integration utils."""
import logging
import random
import re
import string
import time

from homeassistant.core import Event, HomeAssistant

from .const import SSID_NAME_PATTERN, SSID_PASSWORD_PATTERN

_LOGGER = logging.getLogger(__name__)

class Static():
    _hass = None

    @property
    def hass(self) -> HomeAssistant:
        """Return hass object."""
        return Static._hass

    @hass.setter
    def hass(self, hass):
        Static._hass = hass

async def set_ssid_edit_controls(hass: HomeAssistant, coordinator, ssid_index: int) -> None:
    """Restore editing controls to gateway values"""

    # Restore the original values to controls
    ssidName = coordinator.data["access_point"]['ssids'][ssid_index]["ssidName"]
    wpaKey = coordinator.data["access_point"]['ssids'][ssid_index]["wpaKey"]
    encryptionVersion = coordinator.data["access_point"]['ssids'][ssid_index]["encryptionVersion"]
    isBroadcastEnabled = coordinator.data["access_point"]['ssids'][ssid_index]["isBroadcastEnabled"]
    guest = coordinator.data["access_point"]['ssids'][ssid_index]["guest"]
    ssid2_4ghz = coordinator.data["access_point"]['ssids'][ssid_index]["2.4ghzSsid"]
    ssid5_0ghz = coordinator.data["access_point"]['ssids'][ssid_index]["5.0ghzSsid"]
    ssid6_0ghz = coordinator.data["access_point"]['ssids'][ssid_index].get("6.0ghzSsid", False)  # May not exist on all gateways

    # Check ssidName
    name_valid = hass.states.get("switch.t_mobile_edit_ssid_edits_name_valid").state

    # If current string did not pass pattern test, state will not have been updated,
    # so setting it to itself does nothing and card will retain invalid text after Cancel. 
    # Need to tweak the state with a random string first.
    if name_valid == "off":
        random_string = generate_random_mixed_string(12)

        # Set ssidName to random string
        await hass.services.async_call(
                    "text", "set_value", 
                    {"entity_id": "text.t_mobile_edit_ssid_name", "value": random_string}, 
                    blocking=True
                )

        # Delay is necessary or above change will not be applied.
        await hass.async_add_executor_job(time.sleep, 0.05)

    # Set ssidName valid
    await set_SSID_name_valid(True)

    # Set ssidName to gateway value
    await hass.services.async_call(
                "text", "set_value", 
                {"entity_id": "text.t_mobile_edit_ssid_name", "value": ssidName}, 
                blocking=True
            )

    # Check wpaKey
    password_valid = hass.states.get("switch.t_mobile_edit_ssid_edits_password_valid").state

    # Same logic as above with name.
    if password_valid == "off":
        random_string = generate_random_mixed_string(12)

        # Set wpaKey to random string
        await hass.services.async_call(
                    "text", "set_value", 
                    {"entity_id": "text.t_mobile_edit_ssid_password", "value": random_string}, 
                    blocking=True
                )

        # Delay is necessary or above change will not be applied.
        await hass.async_add_executor_job(time.sleep, 0.05)

    # Set wpaKey valid
    await set_SSID_password_valid(True)

    # Set wpaKey to gateway value
    await hass.services.async_call(
                "text", "set_value", 
                {"entity_id": "text.t_mobile_edit_ssid_password", "value": wpaKey}, 
                blocking=True
            )

    # Set encryptionVersion to gateway value
    await hass.services.async_call(
                "select", "select_option", 
                {"entity_id": "select.t_mobile_edit_ssid_encryption_version", "option": encryptionVersion}, 
                blocking=True
            )

    # Set isBroadcastEnabled to gateway value
    action = "turn_off" if isBroadcastEnabled else "turn_on"
    await hass.services.async_call(
                "switch", action, 
                {"entity_id": "switch.t_mobile_edit_ssid_hidden"}, 
                blocking=True
            )

    # Set guest to gateway value
    action = "turn_on" if guest else "turn_off"
    await hass.services.async_call(
                "switch", action, 
                {"entity_id": "switch.t_mobile_edit_ssid_guest"}, 
                blocking=True
            )

    # Set 2.4ghzSsid to gateway value
    action = "turn_on" if ssid2_4ghz else "turn_off"
    await hass.services.async_call(
                "switch", action, 
                {"entity_id": "switch.t_mobile_edit_ssid_2_4ghz"}, 
                blocking=True
            )

    # Set 5.0ghzSsid to gateway value
    action = "turn_on" if ssid5_0ghz else "turn_off"
    await hass.services.async_call(
                "switch", action, 
                {"entity_id": "switch.t_mobile_edit_ssid_5_0ghz"}, 
                blocking=True
            )

    # Set 6.0ghzSsid to gateway value
    action = "turn_on" if ssid6_0ghz else "turn_off"
    await hass.services.async_call(
                "switch", action,
                {"entity_id": "switch.t_mobile_edit_ssid_6_0ghz"},
                blocking=True
            )

    # Clear edits pending
    await hass.services.async_call(
                "switch", "turn_off", 
                {"entity_id": "switch.t_mobile_edit_ssid_edits_pending"}, 
                blocking=True
            )

def get_ssid_edit_index(hass: HomeAssistant) -> int:
    """Get index of selected SSID for editing"""
    ssid = hass.states.get("select.t_mobile_edit_ssids")
    ssid_option = ssid.state
    ssid_options = ssid.attributes["options"]
    try:
        ssid_index = ssid_options.index(ssid_option)
        return ssid_index

    except:
        # If no current selection
        return -1

def generate_random_mixed_string(length):
    characters = string.ascii_letters + string.digits
    random_string = ''.join(random.choice(characters) for _ in range(length))
    return random_string

def generate_random_hex_string(length):
    characters = string.hexdigits.upper()
    random_string = ''.join(random.choice(characters) for _ in range(length))
    return random_string

async def validate_text_and_update_entities(event: Event):
    """Validate input text against pattern and adjust entities used by Save/Cancel buttons"""
    if event.data.get("domain") == "text" and \
        event.data.get("service") == "set_value":
            if event.data.get('service_data')['entity_id'][0] == "text.t_mobile_edit_ssid_name":
                await set_SSID_name_valid(validate_SSID_name(event.data.get('service_data')['value']))
                await set_edits_pending(True)

            elif event.data.get('service_data')['entity_id'][0] == "text.t_mobile_edit_ssid_password":
                await set_SSID_password_valid(validate_SSID_password(event.data.get('service_data')['value']))
                await set_edits_pending(True)

def validate_SSID_name(value: str) -> bool:
    regex = SSID_NAME_PATTERN
    return True if re.match(regex,value) else False

def validate_SSID_password(value: str) -> bool:
    regex = SSID_PASSWORD_PATTERN
    return True if re.match(regex,value) else False

async def set_SSID_name_valid(valid: bool) -> None:
    hass = Static().hass
    if valid:
        # Set name valid indicator
        await hass.services.async_call(
                    "switch", "turn_on", 
                    {"entity_id": "switch.t_mobile_edit_ssid_edits_name_valid"}, 
                    blocking=True
                )
    else:
        # Clear name valid indicator
        await hass.services.async_call(
                    "switch", "turn_off", 
                    {"entity_id": "switch.t_mobile_edit_ssid_edits_name_valid"}, 
                    blocking=True
                )

async def set_SSID_password_valid(valid: bool) -> None:
    hass = Static().hass
    if valid:
        # Set password valid indicator
        await hass.services.async_call(
                    "switch", "turn_on", 
                    {"entity_id": "switch.t_mobile_edit_ssid_edits_password_valid"}, 
                    blocking=True
                )
    else:
        # Clear password valid indicator
        await hass.services.async_call(
                    "switch", "turn_off", 
                    {"entity_id": "switch.t_mobile_edit_ssid_edits_password_valid"}, 
                    blocking=True
                )

async def set_edits_pending(editing: bool) -> None:
    """Set or clear edits pending indicator."""
    hass = Static().hass
    if editing:
        await hass.services.async_call(
                    "switch", "turn_on", 
                    {"entity_id": "switch.t_mobile_edit_ssid_edits_pending"}, 
                    blocking=True
                )
    else:
        await hass.services.async_call(
                    "switch", "turn_off", 
                    {"entity_id": "switch.t_mobile_edit_ssid_edits_pending"}, 
                    blocking=True
                )

async def set_edits_saving(editing: bool) -> None:
    """Set or clear edits saving indicator."""
    hass = Static().hass
    if editing:
        await hass.services.async_call(
                    "switch", "turn_on", 
                    {"entity_id": "switch.t_mobile_edit_ssid_edits_saving"}, 
                    blocking=True
                )
    else:
        await hass.services.async_call(
                    "switch", "turn_off", 
                    {"entity_id": "switch.t_mobile_edit_ssid_edits_saving"}, 
                    blocking=True
                )

async def update_entity(entity_id: str) -> None:
    """Set or clear edits saving indicator."""
    hass = Static().hass
    await hass.services.async_call(
                "homeassistant", "update_entity", 
                {"entity_id": entity_id}, 
                blocking=True
            )

async def select_option(entity_id: str, option: str) -> None:
    """Set or clear edits saving indicator."""
    hass = Static().hass
    await hass.services.async_call(
                "select", "select_option", 
                {"entity_id": entity_id, "option": option}, 
                blocking=True
            )
