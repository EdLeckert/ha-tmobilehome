"""The Home Assistant T-Mobile Home Internet integration."""
import logging
from typing import Callable

from homeassistant.components.sensor import (SensorDeviceClass, SensorEntity)
from homeassistant.core import HomeAssistant
from homeassistant.util import slugify
from homeassistant.helpers.device_registry import CONNECTION_NETWORK_MAC, DeviceInfo
from homeassistant.helpers import entity_platform, service
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import (
    DOMAIN,
    SERVICE_REBOOT_GATEWAY,
    SERVICE_ENABLE_24_WIFI,
    SERVICE_ENABLE_50_WIFI,
    SERVICE_SET_24_WIFI_POWER,
    SERVICE_SET_50_WIFI_POWER,
    SCHEMA_SERVICE_REBOOT_GATEWAY,
    SCHEMA_SERVICE_ENABLE_24_WIFI,
    SCHEMA_SERVICE_ENABLE_50_WIFI,
    SCHEMA_SERVICE_SET_24_WIFI_POWER,
    SCHEMA_SERVICE_SET_50_WIFI_POWER,
)

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: dict,
    async_add_entities: Callable,
):
    """Set up the Home Assistant T-Mobile Home Internet sensors."""
    entities = _create_entities(hass, entry)
    async_add_entities(entities)

    platform = entity_platform.async_get_current_platform()

    # This will call Entity._reboot_gateway
    platform.async_register_entity_service(
        SERVICE_REBOOT_GATEWAY,
        SCHEMA_SERVICE_REBOOT_GATEWAY,
        "_reboot_gateway",
    )

    # This will call Entity._enable_24_wifi
    platform.async_register_entity_service(
        SERVICE_ENABLE_24_WIFI,
        SCHEMA_SERVICE_ENABLE_24_WIFI,
        "_enable_24_wifi",
    )

    # This will call Entity._enable_50_wifi
    platform.async_register_entity_service(
        SERVICE_ENABLE_50_WIFI,
        SCHEMA_SERVICE_ENABLE_50_WIFI,
        "_enable_50_wifi",
    )

    # This will call Entity._set_24_wifi_power
    platform.async_register_entity_service(
        SERVICE_SET_24_WIFI_POWER,
        SCHEMA_SERVICE_SET_24_WIFI_POWER,
        "_set_24_wifi_power",
    )

    # This will call Entity._set_50_wifi_power
    platform.async_register_entity_service(
        SERVICE_SET_50_WIFI_POWER,
        SCHEMA_SERVICE_SET_50_WIFI_POWER,
        "_set_50_wifi_power",
    )

def _create_entities(hass: HomeAssistant, entry: dict):
    entities = []
    fast_coordinator = hass.data[DOMAIN][entry.entry_id]["fast_coordinator"]
    slow_coordinator = hass.data[DOMAIN][entry.entry_id]["slow_coordinator"]
    controller = hass.data[DOMAIN][entry.entry_id]["controller"]

    entities.append(GatewayDeviceSensor(hass, entry, slow_coordinator, controller))
    entities.append(GatewayAccessPointSensor(hass, entry, slow_coordinator))
    entities.append(GatewayClientsSensor(hass, entry, slow_coordinator))
    entities.append(GatewayCellSensor(hass, entry, fast_coordinator))
    entities.append(GatewayDeviceSimSensor(hass, entry, slow_coordinator))
    entities.append(Gateway4gBandsSensor(hass, entry, fast_coordinator))
    entities.append(Gateway4gRSRPSensor(hass, entry, fast_coordinator))
    entities.append(Gateway4gRSRQSensor(hass, entry, fast_coordinator))
    entities.append(Gateway4gSINRSensor(hass, entry, fast_coordinator))
    entities.append(Gateway4gAntennaSensor(hass, entry, fast_coordinator))
    entities.append(Gateway4gBandwidthSensor(hass, entry, fast_coordinator))
    entities.append(Gateway4gECGISensor(hass, entry, fast_coordinator))
    entities.append(Gateway5gBandsSensor(hass, entry, fast_coordinator))
    entities.append(Gateway5gRSRPSensor(hass, entry, fast_coordinator))
    entities.append(Gateway5gRSRQSensor(hass, entry, fast_coordinator))
    entities.append(Gateway5gSINRSensor(hass, entry, fast_coordinator))
    entities.append(Gateway5gAntennaSensor(hass, entry, fast_coordinator))
    entities.append(Gateway5gBandwidthSensor(hass, entry, fast_coordinator))
    entities.append(Gateway5gECGISensor(hass, entry, fast_coordinator))
    entities.append(GatewayUptimeSensor(hass, entry, slow_coordinator))

    return entities


class GatewayDeviceSensor(CoordinatorEntity, SensorEntity):
    """Represent a sensor for the gateway."""

    def __init__(self, hass, entry, coordinator, controller):
        """Set up a new HA T-Mobile Home Internet gateway device sensor."""
        self._hass = hass
        self._entry = entry
        self._controller = controller
        self._coordinator = coordinator
        self._entity_type = "sensor"
        super().__init__(coordinator)

    @property
    def device_info(self) -> DeviceInfo:
        """Return the device info."""
        return DeviceInfo(
            identifiers={(DOMAIN, slugify(self._entry.unique_id))},
            connections={(CONNECTION_NETWORK_MAC, self._coordinator._gateway["device"]["macId"])},
            serial_number=self._coordinator._gateway["device"]["serial"],
            manufacturer=self._coordinator._gateway["device"]["manufacturer"],
            model=self._coordinator._gateway["device"]["model"],
            name=self._coordinator._gateway["device"]["name"],
            sw_version=self._coordinator._gateway["device"]["softwareVersion"],
            hw_version=self._coordinator._gateway["device"]["hardwareVersion"],
        )

    @property
    def icon(self) -> str:
        """Return icon."""
        return "mdi:router-network-wireless"

    @property
    def name(self) -> str:
        """Return the name of this sensor."""
        return f"T-Mobile Home Internet Gateway"

    @property
    def unique_id(self) -> str:
        """Return a unique, Home Assistant friendly identifier for this entity."""
        return slugify(self._coordinator._gateway["device"]["serial"])

    @property
    def device_class(self) -> str:
        """Return device_class."""
        return "gateway"

    @property
    def extra_state_attributes(self):
        attributes = { "device": "None" }
        if self.coordinator.data is not None:
            attributes = self.coordinator._gateway
        return attributes

    @property
    def native_value(self) -> int:
        """Return the value of this sensor."""
        return self.coordinator._gateway["device"]["friendlyName"]

    async def _reboot_gateway(self):
        """Reboot the gateway."""
        await self._hass.async_add_executor_job(self._controller.reboot_gateway)

    async def _enable_24_wifi(self, enabled: bool) -> None:
        """Enable or disable 2.4GHz WiFi."""
        access_point = self.coordinator.data["access_point"]
        access_point["2.4ghz"]["isRadioEnabled"] = enabled
        await self._hass.async_add_executor_job(self._controller.set_ap_config, access_point)

    async def _enable_50_wifi(self, enabled: bool) -> None:
        """Enable or disable 5.0GHz WiFi."""
        access_point = self.coordinator.data["access_point"]
        access_point["5.0ghz"]["isRadioEnabled"] = enabled
        await self._hass.async_add_executor_job(self._controller.set_ap_config, access_point)

    async def _set_24_wifi_power(self, power_level: int) -> None:
        """Set 2.4GHz WiFi power level."""
        access_point = self.coordinator.data["access_point"]
        access_point["2.4ghz"]["transmissionPower"] = ('50%' if power_level == "Half" else '100%')
        await self._hass.async_add_executor_job(self._controller.set_ap_config, access_point)

    async def _set_50_wifi_power(self, power_level: int) -> None:
        """Set 5.0GHz WiFi power level."""
        access_point = self.coordinator.data["access_point"]
        access_point["2.4ghz"]["transmissionPower"] = ('50%' if power_level == "Half" else '100%')
        await self._hass.async_add_executor_job(self._controller.set_ap_config, access_point)


class GatewayAccessPointSensor(CoordinatorEntity, SensorEntity):
    """Represent a sensor for the gateway."""

    def __init__(self, hass, entry, coordinator):
        """Set up a new HA T-Mobile Home Internet access point sensor."""
        self._hass = hass
        self._entry = entry
        self._entity_type = "sensor"
        super().__init__(coordinator)

    @property
    def icon(self) -> str:
        """Return icon."""
        return "mdi:access-point"

    @property
    def name(self) -> str:
        """Return the name of this sensor."""
        return f"T-Mobile Home Internet Access Point"

    @property
    def unique_id(self) -> str:
        """Return a unique, Home Assistant friendly identifier for this entity."""
        return slugify(f"{self._entity_type}_tmobile_home_internet_access_point")

    @property
    def extra_state_attributes(self):
        attributes = { "access_point": "None" }
        if self.coordinator.data is not None:
            attributes = self.coordinator.data["access_point"]
        return attributes

    @property
    def native_value(self) -> int:
        """Return the value of this sensor."""
        return self.coordinator.data["access_point"]["ssids"][0]["ssidName"]


class GatewayClientsSensor(CoordinatorEntity, SensorEntity):
    """Represent a sensor for the clients of the gateway."""

    def __init__(self, hass, entry, coordinator):
        """Set up a new HA T-Mobile Home Internet gateway clients sensor."""
        self._hass = hass
        self._entry = entry
        self._entity_type = "sensor"
        super().__init__(coordinator)

    @property
    def icon(self) -> str:
        """Return icon."""
        return "mdi:devices"

    @property
    def name(self) -> str:
        """Return the name of this sensor."""
        return f"T-Mobile Home Internet Gateway Clients"

    @property
    def unique_id(self) -> str:
        """Return a unique, Home Assistant friendly identifier for this entity."""
        return slugify(f"{self._entity_type}_tmobile_home_internet_gateway_clients")

    @property
    def native_unit_of_measurement(self) -> str:
        """The unit of measurement that the sensor's value is expressed in."""
        return "devices"

    @property
    def extra_state_attributes(self):
        attributes = { "clients": "None" }
        if self.coordinator.data is not None:
            attributes = self.coordinator.data["clients"]
        return attributes

    @property
    def native_value(self) -> int:
        """Return the value of this sensor."""
        clients = self.coordinator.data["clients"]
        total_clients = len(clients["2.4ghz"]) + len(clients["5.0ghz"]) + len(clients["ethernet"])
        return total_clients


class GatewayCellSensor(CoordinatorEntity, SensorEntity):
    """Represent a sensor for the gateway."""

    def __init__(self, hass, entry, coordinator):
        """Set up a new HA T-Mobile Home Internet gateway cell sensor."""
        self._hass = hass
        self._entry = entry
        self._entity_type = "sensor"
        super().__init__(coordinator)

    @property
    def icon(self) -> str:
        """Return icon."""
        return "mdi:radio-tower"

    @property
    def name(self) -> str:
        """Return the name of this sensor."""
        return f"T-Mobile Home Internet Cell Status"

    @property
    def unique_id(self) -> str:
        """Return a unique, Home Assistant friendly identifier for this entity."""
        return slugify(f"{self._entity_type}_tmobile_home_internet_cell_status")

    @property
    def entity_registry_enabled_default(self) -> bool:
        """Set entity disabled by default."""
        return False

    @property
    def extra_state_attributes(self):
        attributes = { "cell": "None" }
        if self.coordinator.data is not None:
            attributes = self.coordinator.data["cell"]
        return attributes

    @property
    def native_value(self) -> int:
        """Return the value of this sensor."""
        return "Bands: " + ' '.join(self.coordinator.data["cell"]["4g"]["sector"]["bands"]) + ' ' + ' '.join(self.coordinator.data["cell"]["5g"]["sector"]["bands"])


class GatewayDeviceSimSensor(CoordinatorEntity, SensorEntity):
    """Represent a sensor for the gateway."""

    def __init__(self, hass, entry, coordinator):
        """Set up a new HA T-Mobile Home Internet gateway device sim sensor."""
        self._hass = hass
        self._entry = entry
        self._entity_type = "sensor"
        super().__init__(coordinator)

    @property
    def icon(self) -> str:
        """Return icon."""
        return "mdi:sim"

    @property
    def name(self) -> str:
        """Return the name of this sensor."""
        return f"T-Mobile Home Internet Gateway Sim Card"

    @property
    def unique_id(self) -> str:
        """Return a unique, Home Assistant friendly identifier for this entity."""
        return slugify(f"{self._entity_type}_tmobile_home_internet_gateway_sim_card")

    @property
    def extra_state_attributes(self):
        attributes = { "sim": "None" }
        if self.coordinator.data is not None:
            attributes = self.coordinator._sim
        return attributes

    @property
    def native_value(self) -> int:
        """Return the value of this sensor."""
        return self.coordinator._gateway["device"]["friendlyName"]


class Gateway4gBandsSensor(CoordinatorEntity, SensorEntity):
    """Represent a sensor for the gateway 4G active bands."""

    def __init__(self, hass, entry, coordinator):
        """Set up a new HA T-Mobile Home Internet gateway 4G active bands sensor."""
        self._hass = hass
        self._entry = entry
        self._entity_type = "sensor"
        super().__init__(coordinator)

    @property
    def icon(self) -> str:
        """Return icon."""
        return "mdi:signal"

    @property
    def name(self) -> str:
        """Return the name of this sensor."""
        return f"T-Mobile Home Internet 4G Bands"

    @property
    def unique_id(self) -> str:
        """Return a unique, Home Assistant friendly identifier for this entity."""
        return slugify(f"{self._entry.unique_id}_{self._entity_type}_4g_bands")

    @property
    def native_value(self) -> int:
        """Return the value of this sensor."""
        return ' '.join(self.coordinator.data["cell"]["4g"]["sector"]["bands"])


class Gateway4gRSRPSensor(CoordinatorEntity, SensorEntity):
    """Represent a sensor for the gateway 4G Reference Signal Received Power."""

    def __init__(self, hass, entry, coordinator):
        """Set up a new HA T-Mobile Home Internet gateway 4G RSRP sensor."""
        self._hass = hass
        self._entry = entry
        self._entity_type = "sensor"
        super().__init__(coordinator)

    @property
    def icon(self) -> str:
        """Return icon."""
        return "mdi:signal"

    @property
    def name(self) -> str:
        """Return the name of this sensor."""
        return f"T-Mobile Home Internet 4G RSRP"

    @property
    def unique_id(self) -> str:
        """Return a unique, Home Assistant friendly identifier for this entity."""
        return slugify(f"{self._entity_type}_tmobile_home_internet_4g_RSRP")

    @property
    def device_class(self) -> SensorDeviceClass | None:
        """Return the type of sensor."""
        return SensorDeviceClass.SIGNAL_STRENGTH

    @property
    def extra_state_attributes(self):
        return { "description": "4G Reference Signal Received Power" }

    @property
    def native_unit_of_measurement(self) -> str:
        """The unit of measurement that the sensor's value is expressed in."""
        return "dBm"

    @property
    def native_value(self) -> int:
        """Return the value of this sensor."""
        return self.coordinator.data["cell"]["4g"]["sector"]["rsrp"]


class Gateway4gRSRQSensor(CoordinatorEntity, SensorEntity):
    """Represent a sensor for the gateway 4G Reference Signal Received Quality."""

    def __init__(self, hass, entry, coordinator):
        """Set up a new HA T-Mobile Home Internet gateway 4G RSRQ sensor."""
        self._hass = hass
        self._entry = entry
        self._entity_type = "sensor"
        super().__init__(coordinator)

    @property
    def icon(self) -> str:
        """Return icon."""
        return "mdi:signal"

    @property
    def name(self) -> str:
        """Return the name of this sensor."""
        return f"T-Mobile Home Internet 4G RSRQ"

    @property
    def unique_id(self) -> str:
        """Return a unique, Home Assistant friendly identifier for this entity."""
        return slugify(f"{self._entity_type}_tmobile_home_internet_4g_RSRQ")

    @property
    def device_class(self) -> SensorDeviceClass | None:
        """Return the type of sensor."""
        return SensorDeviceClass.SIGNAL_STRENGTH

    @property
    def native_unit_of_measurement(self) -> str:
        """The unit of measurement that the sensor's value is expressed in."""
        return "dB"

    @property
    def extra_state_attributes(self):
        return { "description": "4G Reference Signal Received Quality" }

    @property
    def native_value(self) -> int:
        """Return the value of this sensor."""
        return self.coordinator.data["cell"]["4g"]["sector"]["rsrq"]


class Gateway4gSINRSensor(CoordinatorEntity, SensorEntity):
    """Represent a sensor for the gateway 4G Signal-to-interference-plus-noise ratio."""

    def __init__(self, hass, entry, coordinator):
        """Set up a new HA T-Mobile Home Internet gateway 4G SINR sensor."""
        self._hass = hass
        self._entry = entry
        self._entity_type = "sensor"
        super().__init__(coordinator)

    @property
    def icon(self) -> str:
        """Return icon."""
        return "mdi:signal"

    @property
    def name(self) -> str:
        """Return the name of this sensor."""
        return f"T-Mobile Home Internet 4G SINR"

    @property
    def unique_id(self) -> str:
        """Return a unique, Home Assistant friendly identifier for this entity."""
        return slugify(f"{self._entity_type}_tmobile_home_internet_4g_SINR")

    @property
    def device_class(self) -> SensorDeviceClass | None:
        """Return the type of sensor."""
        return SensorDeviceClass.SIGNAL_STRENGTH

    @property
    def native_unit_of_measurement(self) -> str:
        """The unit of measurement that the sensor's value is expressed in."""
        return "dB"

    @property
    def extra_state_attributes(self):
        return { "description": "4G Signal to Interference & Noise Ratio" }

    @property
    def native_value(self) -> int:
        """Return the value of this sensor."""
        return self.coordinator.data["cell"]["4g"]["sector"]["sinr"]


class Gateway4gAntennaSensor(CoordinatorEntity, SensorEntity):
    """Represent a sensor for the gateway 4G antenna used."""

    def __init__(self, hass, entry, coordinator):
        """Set up a new HA T-Mobile Home Internet gateway 4G antenna used sensor."""
        self._hass = hass
        self._entry = entry
        self._entity_type = "sensor"
        super().__init__(coordinator)

    @property
    def icon(self) -> str:
        """Return icon."""
        return "mdi:antenna"

    @property
    def name(self) -> str:
        """Return the name of this sensor."""
        return f"T-Mobile Home Internet 4G Antenna Used"

    @property
    def unique_id(self) -> str:
        """Return a unique, Home Assistant friendly identifier for this entity."""
        return slugify(f"{self._entity_type}_tmobile_home_internet_4g_antenna")

    @property
    def native_value(self) -> int:
        """Return the value of this sensor."""
        return self.coordinator.data["cell"]["4g"]["sector"]["antennaUsed"]


class Gateway4gBandwidthSensor(CoordinatorEntity, SensorEntity):
    """Represent a sensor for the gateway 4G bandwidth."""

    def __init__(self, hass, entry, coordinator):
        """Set up a new HA T-Mobile Home Internet gateway 4G bandwidth sensor."""
        self._hass = hass
        self._entry = entry
        self._entity_type = "sensor"
        super().__init__(coordinator)

    @property
    def icon(self) -> str:
        """Return icon."""
        return "mdi:guage"

    @property
    def name(self) -> str:
        """Return the name of this sensor."""
        return f"T-Mobile Home Internet 4G Bandwidth"

    @property
    def unique_id(self) -> str:
        """Return a unique, Home Assistant friendly identifier for this entity."""
        return slugify(f"{self._entity_type}_tmobile_home_internet_4g_bandwidth")

    @property
    def native_value(self) -> int:
        """Return the value of this sensor."""
        return self.coordinator.data["cell"]["4g"]["bandwidth"]


class Gateway4gECGISensor(CoordinatorEntity, SensorEntity):
    """Represent a sensor for the gateway 4G ECGI."""

    def __init__(self, hass, entry, coordinator):
        """Set up a new HA T-Mobile Home Internet gateway 4G ECGI sensor."""
        self._hass = hass
        self._entry = entry
        self._entity_type = "sensor"
        super().__init__(coordinator)

    @property
    def icon(self) -> str:
        """Return icon."""
        return "mdi:radio-tower"

    @property
    def name(self) -> str:
        """Return the name of this sensor."""
        return f"T-Mobile Home Internet 4G Cell Global ID"

    @property
    def unique_id(self) -> str:
        """Return a unique, Home Assistant friendly identifier for this entity."""
        return slugify(f"{self._entity_type}_tmobile_home_internet_4g_ecgi")

    @property
    def native_value(self) -> int:
        """Return the value of this sensor."""
        return self.coordinator.data["cell"]["4g"]["ecgi"]


class Gateway5gBandsSensor(CoordinatorEntity, SensorEntity):
    """Represent a sensor for the gateway 4G active bands."""

    def __init__(self, hass, entry, coordinator):
        """Set up a new HA T-Mobile Home Internet gateway 5G active bands sensor."""
        self._hass = hass
        self._entry = entry
        self._entity_type = "sensor"
        super().__init__(coordinator)

    @property
    def icon(self) -> str:
        """Return icon."""
        return "mdi:signal"

    @property
    def name(self) -> str:
        """Return the name of this sensor."""
        return f"T-Mobile Home Internet 5G Bands"

    @property
    def unique_id(self) -> str:
        """Return a unique, Home Assistant friendly identifier for this entity."""
        return slugify(f"{self._entity_type}_tmobile_home_internet_5g_bands")

    @property
    def native_value(self) -> int:
        """Return the value of this sensor."""
        return ' '.join(self.coordinator.data["cell"]["5g"]["sector"]["bands"])


class Gateway5gRSRPSensor(CoordinatorEntity, SensorEntity):
    """Represent a sensor for the gateway 5G Reference Signal Received Power."""

    def __init__(self, hass, entry, coordinator):
        """Set up a new HA T-Mobile Home Internet gateway 5G RSRP sensor."""
        self._hass = hass
        self._entry = entry
        self._entity_type = "sensor"
        super().__init__(coordinator)

    @property
    def icon(self) -> str:
        """Return icon."""
        return "mdi:signal"

    @property
    def name(self) -> str:
        """Return the name of this sensor."""
        return f"T-Mobile Home Internet 5G RSRP"

    @property
    def unique_id(self) -> str:
        """Return a unique, Home Assistant friendly identifier for this entity."""
        return slugify(f"{self._entity_type}_tmobile_home_internet_5g_RSRP")

    @property
    def device_class(self) -> SensorDeviceClass | None:
        """Return the type of sensor."""
        return SensorDeviceClass.SIGNAL_STRENGTH

    @property
    def native_unit_of_measurement(self) -> str:
        """The unit of measurement that the sensor's value is expressed in."""
        return "dBm"

    @property
    def extra_state_attributes(self):
        return { "description": "5G Reference Signal Received Power" }

    @property
    def native_value(self) -> int:
        """Return the value of this sensor."""
        return self.coordinator.data["cell"]["5g"]["sector"]["rsrp"]


class Gateway5gRSRQSensor(CoordinatorEntity, SensorEntity):
    """Represent a sensor for the gateway 5G Reference Signal Received Quality."""

    def __init__(self, hass, entry, coordinator):
        """Set up a new HA T-Mobile Home Internet gateway 5G RSRQ sensor."""
        self._hass = hass
        self._entry = entry
        self._entity_type = "sensor"
        super().__init__(coordinator)

    @property
    def icon(self) -> str:
        """Return icon."""
        return "mdi:signal"

    @property
    def name(self) -> str:
        """Return the name of this sensor."""
        return f"T-Mobile Home Internet 5G RSRQ"


    @property
    def unique_id(self) -> str:
        """Return a unique, Home Assistant friendly identifier for this entity."""
        return slugify(f"{self._entity_type}_tmobile_home_internet_5g_RSRQ")

    @property
    def device_class(self) -> SensorDeviceClass | None:
        """Return the type of sensor."""
        return SensorDeviceClass.SIGNAL_STRENGTH

    @property
    def native_unit_of_measurement(self) -> str:
        """The unit of measurement that the sensor's value is expressed in."""
        return "dB"

    @property
    def extra_state_attributes(self):
        return { "description": "5G Reference Signal Received Quality" }

    @property
    def native_value(self) -> int:
        """Return the value of this sensor."""
        return self.coordinator.data["cell"]["5g"]["sector"]["rsrq"]


class Gateway5gSINRSensor(CoordinatorEntity, SensorEntity):
    """Represent a sensor for the gateway 5G Signal-to-interference-plus-noise ratio."""

    def __init__(self, hass, entry, coordinator):
        """Set up a new HA T-Mobile Home Internet gateway 5G SINR sensor."""
        self._hass = hass
        self._entry = entry
        self._entity_type = "sensor"
        super().__init__(coordinator)

    @property
    def icon(self) -> str:
        """Return icon."""
        return "mdi:signal"

    @property
    def name(self) -> str:
        """Return the name of this sensor."""
        return f"T-Mobile Home Internet 5G SINR"

    @property
    def unique_id(self) -> str:
        """Return a unique, Home Assistant friendly identifier for this entity."""
        return slugify(f"{self._entity_type}_tmobile_home_internet_5g_SINR")

    @property
    def device_class(self) -> SensorDeviceClass | None:
        """Return the type of sensor."""
        return SensorDeviceClass.SIGNAL_STRENGTH

    @property
    def native_unit_of_measurement(self) -> str:
        """The unit of measurement that the sensor's value is expressed in."""
        return "dB"

    @property
    def extra_state_attributes(self):
        return { "description": "5G Signal to Interference & Noise Ratio" }

    @property
    def native_value(self) -> int:
        """Return the value of this sensor."""
        return self.coordinator.data["cell"]["5g"]["sector"]["sinr"]


class Gateway5gAntennaSensor(CoordinatorEntity, SensorEntity):
    """Represent a sensor for the gateway 5G antenna used."""

    def __init__(self, hass, entry, coordinator):
        """Set up a new HA T-Mobile Home Internet gateway 5G antenna used sensor."""
        self._hass = hass
        self._entry = entry
        self._entity_type = "sensor"
        super().__init__(coordinator)

    @property
    def icon(self) -> str:
        """Return icon."""
        return "mdi:antenna"

    @property
    def name(self) -> str:
        """Return the name of this sensor."""
        return f"T-Mobile Home Internet 5G Antenna Used"

    @property
    def unique_id(self) -> str:
        """Return a unique, Home Assistant friendly identifier for this entity."""
        return slugify(f"{self._entity_type}_tmobile_home_internet_5g_antenna")

    @property
    def native_value(self) -> int:
        """Return the value of this sensor."""
        return self.coordinator.data["cell"]["5g"]["sector"]["antennaUsed"]


class Gateway5gBandwidthSensor(CoordinatorEntity, SensorEntity):
    """Represent a sensor for the gateway 5G bandwidth."""

    def __init__(self, hass, entry, coordinator):
        """Set up a new HA T-Mobile Home Internet gateway 5G bandwidth sensor."""
        self._hass = hass
        self._entry = entry
        self._entity_type = "sensor"
        super().__init__(coordinator)

    @property
    def icon(self) -> str:
        """Return icon."""
        return "mdi:guage"

    @property
    def name(self) -> str:
        """Return the name of this sensor."""
        return f"T-Mobile Home Internet 5G Bandwidth"

    @property
    def unique_id(self) -> str:
        """Return a unique, Home Assistant friendly identifier for this entity."""
        return slugify(f"{self._entity_type}_tmobile_home_internet_5g_bandwidth")

    @property
    def native_value(self) -> int:
        """Return the value of this sensor."""
        return self.coordinator.data["cell"]["5g"]["bandwidth"]


class Gateway5gECGISensor(CoordinatorEntity, SensorEntity):
    """Represent a sensor for the gateway 5G ECGI."""

    def __init__(self, hass, entry, coordinator):
        """Set up a new HA T-Mobile Home Internet gateway 5G ECGI sensor."""
        self._hass = hass
        self._entry = entry
        self._entity_type = "sensor"
        super().__init__(coordinator)

    @property
    def icon(self) -> str:
        """Return icon."""
        return "mdi:radio-tower"

    @property
    def name(self) -> str:
        """Return the name of this sensor."""
        return f"T-Mobile Home Internet 5G Cell Global ID"

    @property
    def unique_id(self) -> str:
        """Return a unique, Home Assistant friendly identifier for this entity."""
        return slugify(f"{self._entity_type}_tmobile_home_internet_5g_ecgi")

    @property
    def native_value(self) -> int:
        """Return the value of this sensor."""
        return self.coordinator.data["cell"]["5g"]["ecgi"]


class GatewayUptimeSensor(CoordinatorEntity, SensorEntity):
    """Represent a sensor for the gateway uptime."""

    def __init__(self, hass, entry, coordinator):
        """Set up a new HA T-Mobile Home Internet gateway uptime sensor."""
        self._hass = hass
        self._entry = entry
        self._entity_type = "sensor"
        super().__init__(coordinator)

    @property
    def icon(self) -> str:
        """Return icon."""
        return "mdi:timelapse"

    @property
    def unit_of_measurement(self) -> str:
        """Return the units of measurement."""
        return "h"

    @property
    def name(self) -> str:
        """Return the name of this sensor."""
        return f"T-Mobile Home Internet Gateway Uptime"

    @property
    def unique_id(self) -> str:
        """Return a unique, Home Assistant friendly identifier for this entity."""
        return slugify(f"{self._entity_type}_tmobile_home_internet_gateway_uptime")

    @property
    def native_value(self) -> float:
        """Return the value of this sensor."""
        uptime = self.coordinator.data["time"]["upTime"]
        return 0 if uptime is None else round(uptime / 3600, 1)