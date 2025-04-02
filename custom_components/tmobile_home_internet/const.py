"""Constants for the Home Assistant T-Mobile Home Internet integration."""
from homeassistant.const import CONF_PASSWORD, CONF_USERNAME
import voluptuous as vol
from homeassistant.helpers import config_validation as cv
from typing import Final

DOMAIN: Final = "tmobile_home_internet"
GET_ACCESS_POINT_RETRIES: Final = 20
GET_ACCESS_POINT_RETRY_SECONDS: Final = 4
FAST_POLL_SECONDS: Final = 10
SLOW_POLL_SECONDS: Final = 60

STORAGE_VERSION: Final = 1
STORAGE_KEY: Final = DOMAIN

SCHEMA_SERVICE_REBOOT_GATEWAY: Final = {}

SCHEMA_SERVICE_ENABLE_24_WIFI: Final = {
    vol.Required("enabled"): cv.boolean,
}

SCHEMA_SERVICE_ENABLE_50_WIFI: Final = {
    vol.Required("enabled"): cv.boolean,
}

SCHEMA_SERVICE_SET_24_WIFI_POWER: Final = {
    vol.Required("power_level"): vol.In(["Full","Half"]),
}

SCHEMA_SERVICE_SET_50_WIFI_POWER: Final = {
    vol.Required("power_level"): vol.In(["Full","Half"]),
}

SCHEMA_SERVICE_GET_CLIENT_LIST: Final = {}

SCHEMA_SERVICE_SET_CLIENT_HOSTNAME: Final = {
    vol.Required("mac_address"): cv.string,
    vol.Required("hostname"): cv.string,
}

SCHEMA_SERVICE_CLEAR_CLIENT_HOSTNAME: Final = {
    vol.Required("mac_address"): cv.string,
}

SCHEMA_SERVICE_LIST_CLIENT_HOSTNAMES: Final = {}

SCHEMA_SERVICE_GET_ACCESS_POINT: Final = {}

SCHEMA_SERVICE_GET_GATEWAY: Final = {}

SCHEMA_SERVICE_GET_GATEWAY_CLIENTS: Final = {}

SCHEMA_SERVICE_GET_GATEWAY_SIM_CARD: Final = {}

SCHEMA_SERVICE_GET_CELL_STATUS: Final = {}

SERVICE_REBOOT_GATEWAY: Final = "reboot_gateway"
SERVICE_ENABLE_24_WIFI: Final = "wifi24ghz_enable"
SERVICE_ENABLE_50_WIFI: Final = "wifi50ghz_enable"
SERVICE_SET_24_WIFI_POWER: Final = "set_wifi24ghz_power"
SERVICE_SET_50_WIFI_POWER: Final = "set_wifi50ghz_power"
SERVICE_GET_CLIENT_LIST: Final = "get_client_list"
SERVICE_SET_CLIENT_HOSTNAME: Final = "set_client_hostname"
SERVICE_CLEAR_CLIENT_HOSTNAME: Final = "clear_client_hostname"
SERVICE_LIST_CLIENT_HOSTNAMES: Final = "list_client_hostnames"
SERVICE_GET_ACCESS_POINT: Final = "get_access_point"
SERVICE_GET_GATEWAY: Final = "get_gateway"
SERVICE_GET_GATEWAY_CLIENTS: Final = "get_gateway_clients"
SERVICE_GET_GATEWAY_SIM_CARD: Final = "get_gateway_sim_card"
SERVICE_GET_CELL_STATUS: Final = "get_cell_status"

