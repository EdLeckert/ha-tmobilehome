"""The Home Assistant T-Mobile Home Internet integration."""
import logging
from typing import Callable

from homeassistant.components.sensor import (SensorDeviceClass, SensorEntity)
from homeassistant.core import HomeAssistant, SupportsResponse
from homeassistant.util import slugify
from homeassistant.helpers.device_registry import CONNECTION_NETWORK_MAC, DeviceEntryType, DeviceInfo
from homeassistant.helpers import entity_platform
from homeassistant.helpers.storage import Store
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import (
    DOMAIN,
    SERVICE_GET_CLIENT_LIST,
    SERVICE_REBOOT_GATEWAY,
    SERVICE_ENABLE_24_WIFI,
    SERVICE_ENABLE_50_WIFI,
    SERVICE_ENABLE_60_WIFI,
    SERVICE_SET_24_WIFI_POWER,
    SERVICE_SET_50_WIFI_POWER,
    SERVICE_SET_CLIENT_HOSTNAME,
    SERVICE_CLEAR_CLIENT_HOSTNAME,
    SERVICE_LIST_CLIENT_HOSTNAMES,
    SERVICE_GET_ACCESS_POINT,
    SERVICE_GET_GATEWAY,
    SERVICE_GET_GATEWAY_CLIENTS,
    SERVICE_GET_GATEWAY_SIM_CARD,
    SERVICE_GET_CELL_STATUS,
    SCHEMA_SERVICE_GET_CLIENT_LIST,
    SCHEMA_SERVICE_REBOOT_GATEWAY,
    SCHEMA_SERVICE_ENABLE_24_WIFI,
    SCHEMA_SERVICE_ENABLE_50_WIFI,
    SCHEMA_SERVICE_ENABLE_60_WIFI,
    SCHEMA_SERVICE_SET_24_WIFI_POWER,
    SCHEMA_SERVICE_SET_50_WIFI_POWER,
    SCHEMA_SERVICE_SET_CLIENT_HOSTNAME,
    SCHEMA_SERVICE_CLEAR_CLIENT_HOSTNAME,
    SCHEMA_SERVICE_LIST_CLIENT_HOSTNAMES,
    SCHEMA_SERVICE_GET_ACCESS_POINT,
    SCHEMA_SERVICE_GET_GATEWAY,
    SCHEMA_SERVICE_GET_GATEWAY_CLIENTS,
    SCHEMA_SERVICE_GET_GATEWAY_SIM_CARD,
    SCHEMA_SERVICE_GET_CELL_STATUS,
    STORAGE_KEY,
    STORAGE_VERSION,
    GatewayDeviceEntityFeature,
)

from .utils import get_ssid_edit_index

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
        [GatewayDeviceEntityFeature.CAN_CALL_SERVICES],
    )

    # This will call Entity._enable_24_wifi
    platform.async_register_entity_service(
        SERVICE_ENABLE_24_WIFI,
        SCHEMA_SERVICE_ENABLE_24_WIFI,
        "_enable_24_wifi",
        [GatewayDeviceEntityFeature.CAN_CALL_SERVICES],
    )

    # This will call Entity._enable_50_wifi
    platform.async_register_entity_service(
        SERVICE_ENABLE_50_WIFI,
        SCHEMA_SERVICE_ENABLE_50_WIFI,
        "_enable_50_wifi",
        [GatewayDeviceEntityFeature.CAN_CALL_SERVICES],
    )

    # This will call Entity._enable_60_wifi
    platform.async_register_entity_service(
        SERVICE_ENABLE_60_WIFI,
        SCHEMA_SERVICE_ENABLE_60_WIFI,
        "_enable_60_wifi",
        [GatewayDeviceEntityFeature.CAN_CALL_SERVICES],
    )

    # This will call Entity._set_24_wifi_power
    platform.async_register_entity_service(
        SERVICE_SET_24_WIFI_POWER,
        SCHEMA_SERVICE_SET_24_WIFI_POWER,
        "_set_24_wifi_power",
        [GatewayDeviceEntityFeature.CAN_CALL_SERVICES],
    )

    # This will call Entity._set_50_wifi_power
    platform.async_register_entity_service(
        SERVICE_SET_50_WIFI_POWER,
        SCHEMA_SERVICE_SET_50_WIFI_POWER,
        "_set_50_wifi_power",
        [GatewayDeviceEntityFeature.CAN_CALL_SERVICES],
    )

    # This will call Entity._get_client_list
    platform.async_register_entity_service(
        SERVICE_GET_CLIENT_LIST,
        SCHEMA_SERVICE_GET_CLIENT_LIST,
        "_get_client_list",
        [GatewayDeviceEntityFeature.CAN_CALL_SERVICES],
        supports_response=SupportsResponse.ONLY,
    )

    # This will call Entity._set_display_hostname
    platform.async_register_entity_service(
        SERVICE_SET_CLIENT_HOSTNAME,
        SCHEMA_SERVICE_SET_CLIENT_HOSTNAME,
        "_set_client_hostname",
        [GatewayDeviceEntityFeature.CAN_CALL_SERVICES],
    )

    # This will call Entity._clear_client_hostname
    platform.async_register_entity_service(
        SERVICE_CLEAR_CLIENT_HOSTNAME,
        SCHEMA_SERVICE_CLEAR_CLIENT_HOSTNAME,
        "_clear_client_hostname",
        [GatewayDeviceEntityFeature.CAN_CALL_SERVICES],
    )

    # This will call Entity._list_client_hostnames
    platform.async_register_entity_service(
        SERVICE_LIST_CLIENT_HOSTNAMES,
        SCHEMA_SERVICE_LIST_CLIENT_HOSTNAMES,
        "_list_client_hostnames",
        [GatewayDeviceEntityFeature.CAN_CALL_SERVICES],
        supports_response=SupportsResponse.ONLY,
    )

    # This will call Entity._get_access_point
    platform.async_register_entity_service(
        SERVICE_GET_ACCESS_POINT,
        SCHEMA_SERVICE_GET_ACCESS_POINT,
        "_get_access_point",
        [GatewayDeviceEntityFeature.CAN_CALL_SERVICES],
        supports_response=SupportsResponse.ONLY,
    )

    # This will call Entity._get_gateway
    platform.async_register_entity_service(
        SERVICE_GET_GATEWAY,
        SCHEMA_SERVICE_GET_GATEWAY,
        "_get_gateway",
        [GatewayDeviceEntityFeature.CAN_CALL_SERVICES],
        supports_response=SupportsResponse.ONLY,
    )

    # This will call Entity._get_gateway_clients
    platform.async_register_entity_service(
        SERVICE_GET_GATEWAY_CLIENTS,
        SCHEMA_SERVICE_GET_GATEWAY_CLIENTS,
        "_get_gateway_clients",
        [GatewayDeviceEntityFeature.CAN_CALL_SERVICES],
        supports_response=SupportsResponse.ONLY,
    )

    # This will call Entity._get_gateway_sim_card
    platform.async_register_entity_service(
        SERVICE_GET_GATEWAY_SIM_CARD,
        SCHEMA_SERVICE_GET_GATEWAY_SIM_CARD,
        "_get_gateway_sim_card",
        [GatewayDeviceEntityFeature.CAN_CALL_SERVICES],
        supports_response=SupportsResponse.ONLY,
    )

    # This will call Entity._get_cell_status
    platform.async_register_entity_service(
        SERVICE_GET_CELL_STATUS,
        SCHEMA_SERVICE_GET_CELL_STATUS,
        "_get_cell_status",
        [GatewayDeviceEntityFeature.CAN_CALL_SERVICES],
        supports_response=SupportsResponse.ONLY,
    )


def _create_entities(hass: HomeAssistant, entry: dict):
    fast_coordinator = hass.data[DOMAIN][entry.entry_id]["fast_coordinator"]
    slow_coordinator = hass.data[DOMAIN][entry.entry_id]["slow_coordinator"]
    controller = hass.data[DOMAIN][entry.entry_id]["controller"]
    store = Store[dict[str, str]](hass, STORAGE_VERSION, STORAGE_KEY)

    entities = []
    entities.append(GatewayDeviceSensor(hass, slow_coordinator, fast_coordinator, controller, store))
    entities.append(GatewayAccessPointSensor(slow_coordinator))
    entities.append(GatewayClientsSensor(slow_coordinator))
    entities.append(GatewayCellSensor(fast_coordinator))
    entities.append(GatewayDeviceSimSensor(slow_coordinator))
    entities.append(Gateway4gBandsSensor(fast_coordinator))
    entities.append(Gateway4gRSRPSensor(fast_coordinator))
    entities.append(Gateway4gRSRQSensor(fast_coordinator))
    entities.append(Gateway4gSINRSensor(fast_coordinator))
    entities.append(Gateway4gAntennaSensor(fast_coordinator))
    entities.append(Gateway4gBandwidthSensor(fast_coordinator))
    entities.append(Gateway4gECGISensor(fast_coordinator))
    entities.append(Gateway5gBandsSensor(fast_coordinator))
    entities.append(Gateway5gRSRPSensor(fast_coordinator))
    entities.append(Gateway5gRSRQSensor(fast_coordinator))
    entities.append(Gateway5gSINRSensor(fast_coordinator))
    entities.append(Gateway5gAntennaSensor(fast_coordinator))
    entities.append(Gateway5gBandwidthSensor(fast_coordinator))
    entities.append(Gateway5gECGISensor(fast_coordinator))
    entities.append(GatewayUptimeSensor(slow_coordinator))
    entities.append(GatewaySSIDEditIndexSensor(hass, slow_coordinator))
    entities.append(GatewaySSIDCountSensor(slow_coordinator))

    return entities


class GatewaySensor(CoordinatorEntity, SensorEntity):
    """Represent a sensor for the gateway."""

    def __init__(self, coordinator):
        """Set up a new HA T-Mobile Home Internet gateway sensor."""
        self._coordinator = coordinator
        self._entity_type = "sensor"
        super().__init__(coordinator)
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, coordinator.config_entry.entry_id)},
        )


class GatewayDeviceSensor(GatewaySensor):
    """Represent a sensor for the gateway."""

    def __init__(self, hass, slow_coordinator, fast_coordinator, controller, store):
        """Set up a new HA T-Mobile Home Internet gateway device sensor."""
        self._hass = hass
        self._coordinator = slow_coordinator
        self._fast_coordinator = fast_coordinator
        self._controller = controller
        self._store = store
        super().__init__(slow_coordinator)
        device = self._coordinator._gateway["device"]
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, self._coordinator.config_entry.entry_id)},
            entry_type=DeviceEntryType.SERVICE,
            connections={(CONNECTION_NETWORK_MAC, device["macId"])},
            serial_number=device["serial"],
            manufacturer=device["manufacturer"],
            model=device["model"],
            name=device.get("name", device.get("model")),
            sw_version=device["softwareVersion"],
            hw_version=device["hardwareVersion"],
        )

    @property
    def icon(self) -> str:
        """Return icon."""
        return "mdi:router-network-wireless"

    @property
    def name(self) -> str:
        """Return the name of this sensor."""
        return f"T-Mobile Gateway"

    @property
    def unique_id(self) -> str:
        """Return a unique, Home Assistant friendly identifier for this entity."""
        return slugify(self._coordinator._gateway["device"]["serial"])

    @property
    def device_class(self) -> str:
        """Return device_class."""
        return "gateway"

    @property
    def supported_features(self) -> GatewayDeviceEntityFeature:
        return GatewayDeviceEntityFeature.CAN_CALL_SERVICES

    @property
    def extra_state_attributes(self):
        attributes = { "device": "None" }
        if self._coordinator.data is not None:
            attributes = self._coordinator._gateway
        return attributes

    @property
    def native_value(self) -> str:
        """Return the value of this sensor."""
        device = self._coordinator._gateway["device"]
        return device.get("friendlyName", device.get("model"))

    # Services
    async def _reboot_gateway(self):
        """Reboot the gateway."""
        await self._hass.async_add_executor_job(self._controller.reboot_gateway)

    async def _enable_24_wifi(self, enabled: bool) -> None:
        """Enable or disable 2.4GHz WiFi."""
        access_point = self._coordinator.data["access_point"]
        access_point["2.4ghz"]["isRadioEnabled"] = enabled
        await self._hass.async_add_executor_job(self._controller.set_ap_config, access_point)

    async def _enable_50_wifi(self, enabled: bool) -> None:
        """Enable or disable 5.0GHz WiFi."""
        access_point = self._coordinator.data["access_point"]
        access_point["5.0ghz"]["isRadioEnabled"] = enabled
        await self._hass.async_add_executor_job(self._controller.set_ap_config, access_point)

    async def _enable_60_wifi(self, enabled: bool) -> None:
        """Enable or disable 6.0GHz WiFi."""
        access_point = self._coordinator.data["access_point"]
        if "6.0ghz" in access_point:
          access_point["6.0ghz"]["isRadioEnabled"] = enabled
          await self._hass.async_add_executor_job(self._controller.set_ap_config, access_point)
        else:
          raise Exception("6.0GHz band not supported by this gateway.")

    async def _set_24_wifi_power(self, power_level: int) -> None:
        """Set 2.4GHz WiFi power level."""
        access_point = self._coordinator.data["access_point"]
        access_point["2.4ghz"]["transmissionPower"] = ('50%' if power_level == "Half" else '100%')
        await self._hass.async_add_executor_job(self._controller.set_ap_config, access_point)

    async def _set_50_wifi_power(self, power_level: int) -> None:
        """Set 5.0GHz WiFi power level."""
        access_point = self._coordinator.data["access_point"]
        access_point["5.0ghz"]["transmissionPower"] = ('50%' if power_level == "Half" else '100%')
        await self._hass.async_add_executor_job(self._controller.set_ap_config, access_point)

    async def _set_client_hostname(self, mac_address: str, hostname: str) -> None:
        """Set Client Hostname."""
        edited_clients = await self._store.async_load() or []
        new_client = { 'mac' : mac_address, 'name' : hostname }
        found = False

        # Remove client if blank hostname
        if len(hostname) == 0:
            edited_clients = [d for d in edited_clients if d.get('mac').upper() != mac_address.upper()]
        else:

            # Update hostname if entry exists
            for client in edited_clients:
                if 'mac' in client and client['mac'].upper() == mac_address.upper():
                    client.update(new_client)
                    found = True

            # Otherwise, add new entry to list
            if not found:
                edited_clients.append(new_client)

        await self._store.async_save(edited_clients)

    async def _clear_client_hostname(self, mac_address: str) -> None:
        """Clear Client Hostname."""
        if mac_address == "*":
            # Remove all entries
            return await self._store.async_remove()
        else:
            edited_clients = await self._store.async_load() or []

            # Remove dict from list if it exists
            edited_clients = [d for d in edited_clients if d.get('mac').upper() != mac_address.upper()]

            await self._store.async_save(edited_clients)

    async def _list_client_hostnames(self) -> None:
        """List Client Hostnames."""
        return await self._store.async_load() or []

    async def _get_client_list(self) -> list[dict]:
        """Get client list."""
        clients = self._coordinator.data['clients']

        # Add "interface" key to dicts
        for client_24 in clients['2.4ghz']:
            client_24.update({'interface' : '2.4GHz' })

        for client_50 in clients['5.0ghz']:
            client_50.update({'interface' : '5.0GHz' })

        for client_eth in clients['ethernet']:
            client_eth.update({'interface' : 'Wired' })

        # Combine dicts into single dict for easier display in grid cards
        combined_clients = { 'clients' : clients['2.4ghz'] + clients['5.0ghz'] + clients['ethernet'] + clients.get('6.0ghz', []) + clients.get('wifi', []) }

        # Update hostnames with local edits
        edited_clients = await self._store.async_load() or []

        for replacement in edited_clients:
            for element in combined_clients['clients']:
                if 'mac' in element and element['mac'].upper() == replacement['mac'].upper():
                    element.update(replacement)

        return combined_clients

    async def _get_access_point(self) -> None:
        """Get Access Point."""
        attributes = { "access_point": "None" }
        if self._coordinator.data is not None:
            attributes = self._coordinator.data["access_point"]
        return attributes

    async def _get_gateway(self) -> None:
        """Get Gateway."""
        attributes = { "device": "None" }
        if self._coordinator.data is not None:
            attributes = self._coordinator._gateway
        return attributes


    async def _get_gateway_clients(self) -> None:
        """Get Gateway Clients."""
        attributes = { "clients": "None" }
        if self._coordinator.data is not None:
            attributes = self._coordinator.data["clients"]
        return attributes

    async def _get_gateway_sim_card(self) -> None:
        """Get Gateway SIM Card."""
        attributes = { "sim": "None" }
        if self._coordinator.data is not None:
            attributes = self._coordinator._sim
        return attributes

    async def _get_cell_status(self) -> None:
        """Get Cell Status."""
        attributes = { "cell": "None" }
        if self._fast_coordinator.data is not None:
            attributes = self._fast_coordinator.data["cell"]
        return attributes


class GatewayAccessPointSensor(GatewaySensor):
    """Represent a sensor for the gateway."""

    def __init__(self, coordinator):
        """Set up a new HA T-Mobile Home Internet access point sensor."""
        super().__init__(coordinator)

    @property
    def icon(self) -> str:
        """Return icon."""
        return "mdi:access-point"

    @property
    def name(self) -> str:
        """Return the name of this sensor."""
        return f"T-Mobile Access Point"

    @property
    def unique_id(self) -> str:
        """Return a unique, Home Assistant friendly identifier for this entity."""
        return slugify(f"{self._entity_type}_tmobile_home_internet_access_point")

    @property
    def entity_registry_enabled_default(self) -> bool:
        """Set entity disabled by default."""
        return False

    @property
    def extra_state_attributes(self):
        attributes = { "access_point": "None" }
        if self.coordinator.data is not None:
            attributes = self.coordinator.data["access_point"]
        return attributes

    @property
    def native_value(self) -> str:
        """Return the value of this sensor."""
        return self.coordinator.data["access_point"]["ssids"][0]["ssidName"]


class GatewayClientsSensor(GatewaySensor):
    """Represent a sensor for the clients of the gateway."""

    def __init__(self, coordinator):
        """Set up a new HA T-Mobile Home Internet gateway clients sensor."""
        super().__init__(coordinator)

    @property
    def icon(self) -> str:
        """Return icon."""
        return "mdi:devices"

    @property
    def name(self) -> str:
        """Return the name of this sensor."""
        return f"T-Mobile Gateway Clients"

    @property
    def entity_registry_enabled_default(self) -> bool:
        """Set entity disabled by default."""
        return False

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
        if "6.0ghz" in clients:
            total_clients += len(clients["6.0ghz"])
        if "wifi" in clients:
            total_clients += len(clients["wifi"])
        return total_clients


class GatewayCellSensor(GatewaySensor):
    """Represent a sensor for the gateway."""

    def __init__(self, coordinator):
        """Set up a new HA T-Mobile Home Internet gateway cell sensor."""
        super().__init__(coordinator)

    @property
    def icon(self) -> str:
        """Return icon."""
        return "mdi:radio-tower"

    @property
    def name(self) -> str:
        """Return the name of this sensor."""
        return f"T-Mobile Cell Status"

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
    def native_value(self) -> str | None:
        """Return the value of this sensor."""
        cell = self.coordinator.data["cell"]
        if "4g" in cell and "5g" in cell:
            return "Bands: " + ' '.join(cell["4g"]["sector"]["bands"]) + ' ' + ' '.join(cell["5g"]["sector"]["bands"])
        elif "4g" in self.coordinator.data["cell"]:
            return "Bands: " + ' '.join(cell["4g"]["sector"]["bands"])
        elif "5g" in self.coordinator.data["cell"]:
            return "Bands: " + ' '.join(cell["5g"]["sector"]["bands"])
        return None

class GatewayDeviceSimSensor(GatewaySensor):
    """Represent a sensor for the gateway."""

    def __init__(self, coordinator):
        """Set up a new HA T-Mobile Home Internet gateway device sim sensor."""
        super().__init__(coordinator)

    @property
    def icon(self) -> str:
        """Return icon."""
        return "mdi:sim"

    @property
    def name(self) -> str:
        """Return the name of this sensor."""
        return f"T-Mobile Gateway Sim Card"

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
    def native_value(self) -> str:
        """Return the value of this sensor."""
        device = self._coordinator._gateway["device"]
        return device.get("friendlyName", device.get("model"))


class Gateway4gBandsSensor(GatewaySensor):
    """Represent a sensor for the gateway 4G active bands."""

    def __init__(self, coordinator):
        """Set up a new HA T-Mobile Home Internet gateway 4G active bands sensor."""
        super().__init__(coordinator)

    @property
    def icon(self) -> str:
        """Return icon."""
        return "mdi:signal"

    @property
    def name(self) -> str:
        """Return the name of this sensor."""
        return f"T-Mobile 4G Bands"

    @property
    def unique_id(self) -> str:
        """Return a unique, Home Assistant friendly identifier for this entity."""
        return slugify(f"{self._entity_type}_tmobile_home_internet_4g_bands")

    @property
    def native_value(self) -> str | None:
        """Return the value of this sensor."""
        if "4g" not in self.coordinator.data["cell"]:
            return None
        return ' '.join(self.coordinator.data["cell"]["4g"]["sector"]["bands"])


class Gateway4gRSRPSensor(GatewaySensor):
    """Represent a sensor for the gateway 4G Reference Signal Received Power."""

    def __init__(self, coordinator):
        """Set up a new HA T-Mobile Home Internet gateway 4G RSRP sensor."""
        super().__init__(coordinator)

    @property
    def icon(self) -> str:
        """Return icon."""
        return "mdi:signal"

    @property
    def name(self) -> str:
        """Return the name of this sensor."""
        return f"T-Mobile 4G RSRP"

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
    def native_value(self) -> int | None:
        """Return the value of this sensor."""
        if "4g" not in self.coordinator.data["cell"]:
            return None
        return self.coordinator.data["cell"]["4g"]["sector"]["rsrp"]


class Gateway4gRSRQSensor(GatewaySensor):
    """Represent a sensor for the gateway 4G Reference Signal Received Quality."""

    def __init__(self, coordinator):
        """Set up a new HA T-Mobile Home Internet gateway 4G RSRQ sensor."""
        super().__init__(coordinator)

    @property
    def icon(self) -> str:
        """Return icon."""
        return "mdi:signal"

    @property
    def name(self) -> str:
        """Return the name of this sensor."""
        return f"T-Mobile 4G RSRQ"

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
    def native_value(self) -> int | None:
        """Return the value of this sensor."""
        if "4g" not in self.coordinator.data["cell"]:
            return None
        return self.coordinator.data["cell"]["4g"]["sector"]["rsrq"]


class Gateway4gSINRSensor(GatewaySensor):
    """Represent a sensor for the gateway 4G Signal-to-interference-plus-noise ratio."""

    def __init__(self, coordinator):
        """Set up a new HA T-Mobile Home Internet gateway 4G SINR sensor."""
        super().__init__(coordinator)

    @property
    def icon(self) -> str:
        """Return icon."""
        return "mdi:signal"

    @property
    def name(self) -> str:
        """Return the name of this sensor."""
        return f"T-Mobile 4G SINR"

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
    def native_value(self) -> int | None:
        """Return the value of this sensor."""
        if "4g" not in self.coordinator.data["cell"]:
            return None
        return self.coordinator.data["cell"]["4g"]["sector"]["sinr"]


class Gateway4gAntennaSensor(GatewaySensor):
    """Represent a sensor for the gateway 4G antenna used."""

    def __init__(self, coordinator):
        """Set up a new HA T-Mobile Home Internet gateway 4G antenna used sensor."""
        super().__init__(coordinator)

    @property
    def icon(self) -> str:
        """Return icon."""
        return "mdi:antenna"

    @property
    def name(self) -> str:
        """Return the name of this sensor."""
        return f"T-Mobile 4G Antenna Used"

    @property
    def unique_id(self) -> str:
        """Return a unique, Home Assistant friendly identifier for this entity."""
        return slugify(f"{self._entity_type}_tmobile_home_internet_4g_antenna")

    @property
    def native_value(self) -> str | None:
        """Return the value of this sensor."""
        if "4g" not in self.coordinator.data["cell"]:
            return None
        return self.coordinator.data["cell"]["4g"]["sector"]["antennaUsed"]


class Gateway4gBandwidthSensor(GatewaySensor):
    """Represent a sensor for the gateway 4G bandwidth."""

    def __init__(self, coordinator):
        """Set up a new HA T-Mobile Home Internet gateway 4G bandwidth sensor."""
        super().__init__(coordinator)

    @property
    def icon(self) -> str:
        """Return icon."""
        return "mdi:gauge"

    @property
    def name(self) -> str:
        """Return the name of this sensor."""
        return f"T-Mobile 4G Bandwidth"

    @property
    def unique_id(self) -> str:
        """Return a unique, Home Assistant friendly identifier for this entity."""
        return slugify(f"{self._entity_type}_tmobile_home_internet_4g_bandwidth")

    @property
    def native_value(self) -> str | None:
        """Return the value of this sensor."""
        if "4g" not in self.coordinator.data["cell"]:
            return None
        return self.coordinator.data["cell"]["4g"]["bandwidth"]


class Gateway4gECGISensor(GatewaySensor):
    """Represent a sensor for the gateway 4G ECGI."""

    def __init__(self, coordinator):
        """Set up a new HA T-Mobile Home Internet gateway 4G ECGI sensor."""
        super().__init__(coordinator)

    @property
    def icon(self) -> str:
        """Return icon."""
        return "mdi:radio-tower"

    @property
    def name(self) -> str:
        """Return the name of this sensor."""
        return f"T-Mobile 4G Cell Global ID"

    @property
    def unique_id(self) -> str:
        """Return a unique, Home Assistant friendly identifier for this entity."""
        return slugify(f"{self._entity_type}_tmobile_home_internet_4g_ecgi")

    @property
    def native_value(self) -> int | None:
        """Return the value of this sensor."""
        if "4g" not in self.coordinator.data["cell"]:
            return None
        return self.coordinator.data["cell"]["4g"]["ecgi"]


class Gateway5gBandsSensor(GatewaySensor):
    """Represent a sensor for the gateway 4G active bands."""

    def __init__(self, coordinator):
        """Set up a new HA T-Mobile Home Internet gateway 5G active bands sensor."""
        super().__init__(coordinator)

    @property
    def icon(self) -> str:
        """Return icon."""
        return "mdi:signal"

    @property
    def name(self) -> str:
        """Return the name of this sensor."""
        return f"T-Mobile 5G Bands"

    @property
    def unique_id(self) -> str:
        """Return a unique, Home Assistant friendly identifier for this entity."""
        return slugify(f"{self._entity_type}_tmobile_home_internet_5g_bands")

    @property
    def native_value(self) -> str | None:
        """Return the value of this sensor."""
        if "5g" not in self.coordinator.data["cell"]:
            return None
        return ' '.join(self.coordinator.data["cell"]["5g"]["sector"]["bands"])


class Gateway5gRSRPSensor(GatewaySensor):
    """Represent a sensor for the gateway 5G Reference Signal Received Power."""

    def __init__(self, coordinator):
        """Set up a new HA T-Mobile Home Internet gateway 5G RSRP sensor."""
        super().__init__(coordinator)

    @property
    def icon(self) -> str:
        """Return icon."""
        return "mdi:signal"

    @property
    def name(self) -> str:
        """Return the name of this sensor."""
        return f"T-Mobile 5G RSRP"

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
    def native_value(self) -> int | None:
        """Return the value of this sensor."""
        if "5g" not in self.coordinator.data["cell"]:
            return None
        return self.coordinator.data["cell"]["5g"]["sector"]["rsrp"]


class Gateway5gRSRQSensor(GatewaySensor):
    """Represent a sensor for the gateway 5G Reference Signal Received Quality."""

    def __init__(self, coordinator):
        """Set up a new HA T-Mobile Home Internet gateway 5G RSRQ sensor."""
        super().__init__(coordinator)

    @property
    def icon(self) -> str:
        """Return icon."""
        return "mdi:signal"

    @property
    def name(self) -> str:
        """Return the name of this sensor."""
        return f"T-Mobile 5G RSRQ"


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
    def native_value(self) -> int | None:
        """Return the value of this sensor."""
        if "5g" not in self.coordinator.data["cell"]:
            return None
        return self.coordinator.data["cell"]["5g"]["sector"]["rsrq"]


class Gateway5gSINRSensor(GatewaySensor):
    """Represent a sensor for the gateway 5G Signal-to-interference-plus-noise ratio."""

    def __init__(self, coordinator):
        """Set up a new HA T-Mobile Home Internet gateway 5G SINR sensor."""
        super().__init__(coordinator)

    @property
    def icon(self) -> str:
        """Return icon."""
        return "mdi:signal"

    @property
    def name(self) -> str:
        """Return the name of this sensor."""
        return f"T-Mobile 5G SINR"

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
    def native_value(self) -> int | None:
        """Return the value of this sensor."""
        if "5g" not in self.coordinator.data["cell"]:
            return None
        return self.coordinator.data["cell"]["5g"]["sector"]["sinr"]


class Gateway5gAntennaSensor(GatewaySensor):
    """Represent a sensor for the gateway 5G antenna used."""

    def __init__(self, coordinator):
        """Set up a new HA T-Mobile Home Internet gateway 5G antenna used sensor."""
        super().__init__(coordinator)

    @property
    def icon(self) -> str:
        """Return icon."""
        return "mdi:antenna"

    @property
    def name(self) -> str:
        """Return the name of this sensor."""
        return f"T-Mobile 5G Antenna Used"

    @property
    def unique_id(self) -> str:
        """Return a unique, Home Assistant friendly identifier for this entity."""
        return slugify(f"{self._entity_type}_tmobile_home_internet_5g_antenna")

    @property
    def native_value(self) -> str | None:
        """Return the value of this sensor."""
        if "5g" not in self.coordinator.data["cell"]:
            return None
        return self.coordinator.data["cell"]["5g"]["sector"]["antennaUsed"]


class Gateway5gBandwidthSensor(GatewaySensor):
    """Represent a sensor for the gateway 5G bandwidth."""

    def __init__(self, coordinator):
        """Set up a new HA T-Mobile Home Internet gateway 5G bandwidth sensor."""
        super().__init__(coordinator)

    @property
    def icon(self) -> str:
        """Return icon."""
        return "mdi:gauge"

    @property
    def name(self) -> str:
        """Return the name of this sensor."""
        return f"T-Mobile 5G Bandwidth"

    @property
    def unique_id(self) -> str:
        """Return a unique, Home Assistant friendly identifier for this entity."""
        return slugify(f"{self._entity_type}_tmobile_home_internet_5g_bandwidth")

    @property
    def native_value(self) -> str | None:
        """Return the value of this sensor."""
        if "5g" not in self.coordinator.data["cell"]:
            return None
        return self.coordinator.data["cell"]["5g"]["bandwidth"]


class Gateway5gECGISensor(GatewaySensor):
    """Represent a sensor for the gateway 5G ECGI."""

    def __init__(self, coordinator):
        """Set up a new HA T-Mobile Home Internet gateway 5G ECGI sensor."""
        super().__init__(coordinator)

    @property
    def icon(self) -> str:
        """Return icon."""
        return "mdi:radio-tower"

    @property
    def name(self) -> str:
        """Return the name of this sensor."""
        return f"T-Mobile 5G Cell Global ID"

    @property
    def unique_id(self) -> str:
        """Return a unique, Home Assistant friendly identifier for this entity."""
        return slugify(f"{self._entity_type}_tmobile_home_internet_5g_ecgi")

    @property
    def native_value(self) -> int | None:
        """Return the value of this sensor."""
        if "5g" not in self.coordinator.data["cell"]:
            return None
        return self.coordinator.data["cell"]["5g"]["ecgi"]


class GatewayUptimeSensor(GatewaySensor):
    """Represent a sensor for the gateway uptime."""

    def __init__(self, coordinator):
        """Set up a new HA T-Mobile Home Internet gateway uptime sensor."""
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
        return f"T-Mobile Gateway Uptime"

    @property
    def unique_id(self) -> str:
        """Return a unique, Home Assistant friendly identifier for this entity."""
        return slugify(f"{self._entity_type}_tmobile_home_internet_gateway_uptime")

    @property
    def native_value(self) -> float:
        """Return the value of this sensor."""
        uptime = self.coordinator.data["time"]["upTime"]
        return 0 if uptime is None else round(uptime / 3600, 1)

class GatewaySSIDEditIndexSensor(GatewaySensor):
    """Represent a sensor for the gateway SSID Edit Index."""

    def __init__(self, hass, coordinator):
        """Set up a new HA T-Mobile Home Internet gateway SSID Edit Index sensor."""
        self._hass = hass
        super().__init__(coordinator)

    @property
    def icon(self) -> str:
        """Return icon."""
        return "mdi:counter"

    @property
    def name(self) -> str:
        """Return the name of this sensor."""
        return f"T-Mobile Gateway SSID Edit Index"

    @property
    def unique_id(self) -> str:
        """Return a unique, Home Assistant friendly identifier for this entity."""
        return slugify(f"{self._entity_type}_tmobile_home_internet_gateway_ssid_edit_index")

    @property
    def entity_registry_visible_default(self) -> bool:
        """Set entity hidden by default."""
        return False

    @property
    def native_value(self) -> int:
        """Return the value of this sensor."""
        return get_ssid_edit_index(self._hass)

class GatewaySSIDCountSensor(GatewaySensor):
    """Represent a sensor for the gateway SSID Count."""

    def __init__(self, coordinator):
        """Set up a new HA T-Mobile Home Internet gateway SSID Count sensor."""
        super().__init__(coordinator)

    @property
    def icon(self) -> str:
        """Return icon."""
        return "mdi:counter"

    @property
    def unit_of_measurement(self) -> str:
        """Return the units of measurement."""
        return "SSID"

    @property
    def name(self) -> str:
        """Return the name of this sensor."""
        return f"T-Mobile Gateway SSID Count"

    @property
    def unique_id(self) -> str:
        """Return a unique, Home Assistant friendly identifier for this entity."""
        return slugify(f"{self._entity_type}_tmobile_home_internet_gateway_ssid_count")

    @property
    def native_value(self) -> int:
        """Return the value of this sensor."""
        return len(self.coordinator.data["access_point"]["ssids"])

