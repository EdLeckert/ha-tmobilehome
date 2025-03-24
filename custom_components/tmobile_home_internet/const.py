"""Constants for the Home Assistant T-Mobile Home Internet integration."""
from homeassistant.const import CONF_PASSWORD, CONF_USERNAME
import voluptuous as vol
from homeassistant.helpers import config_validation as cv

DOMAIN = "tmobile_home_internet"
GET_ACCESS_POINT_RETRIES = 20
GET_ACCESS_POINT_RETRY_SECONDS = 4
FAST_POLL_SECONDS = 10
SLOW_POLL_SECONDS = 60

SCHEMA_SERVICE_REBOOT_GATEWAY = {}

SCHEMA_SERVICE_ENABLE_24_WIFI = {
    vol.Required("enabled"): cv.boolean,
}

SCHEMA_SERVICE_ENABLE_50_WIFI = {
    vol.Required("enabled"): cv.boolean,
}

SCHEMA_SERVICE_SET_24_WIFI_POWER = {
    vol.Required("power_level"): vol.In(["Full","Half"]),
}

SCHEMA_SERVICE_SET_50_WIFI_POWER = {
    vol.Required("power_level"): vol.In(["Full","Half"]),
}

SERVICE_REBOOT_GATEWAY = "reboot_gateway"
SERVICE_ENABLE_24_WIFI = "wifi24ghz_enable"
SERVICE_ENABLE_50_WIFI = "wifi50ghz_enable"
SERVICE_SET_24_WIFI_POWER = "set_wifi24ghz_power"
SERVICE_SET_50_WIFI_POWER = "set_wifi50ghz_power"