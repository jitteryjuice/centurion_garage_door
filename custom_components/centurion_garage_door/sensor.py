"""Sensor platform for Centurion Garage Door integration."""

from __future__ import annotations

import logging
from datetime import timedelta
from typing import TYPE_CHECKING

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.const import SIGNAL_STRENGTH_DECIBELS_MILLIWATT
from homeassistant.helpers.device_registry import DeviceInfo

from .const import DOMAIN
from .door import parse_door_status
from .entity import CenturionGarageEntity

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback

    from .coordinator import CenturionGarageDataUpdateCoordinator

SCAN_INTERVAL = timedelta(seconds=30)
_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Centurion Garage Door sensor entities from a config entry."""
    runtime_data = hass.data[DOMAIN][config_entry.entry_id]
    coordinator: CenturionGarageDataUpdateCoordinator = runtime_data.coordinator
    async_add_entities(
        [
            CenturionWiFiSignalSensor(coordinator),
            CenturionDoorOperationCounterSensor(coordinator),
            CenturionDoorMessageSensor(coordinator),
            CenturionErrorCodeSensor(coordinator),
            CenturionCameraStatusSensor(coordinator),
            CenturionDoorTimestampSensor(coordinator),
        ]
    )


class CenturionBaseSensor(CenturionGarageEntity, SensorEntity):
    """Base class for Centurion Garage Door sensors."""

    def __init__(self, coordinator: CenturionGarageDataUpdateCoordinator) -> None:
        """Initialize the base sensor class."""
        super().__init__(coordinator)
        self.coordinator = coordinator

    @property
    def device_info(self) -> DeviceInfo:
        """Return device information for Home Assistant."""
        api_client = getattr(self.coordinator, "api_client", None)
        ip = getattr(api_client, "ip_address", "unknown") if api_client else "unknown"
        return DeviceInfo(
            identifiers={(DOMAIN, ip)},
            name="Sensor",
            manufacturer="Centurion",
            model="Garage",
        )


class CenturionWiFiSignalSensor(CenturionBaseSensor):
    """Centurion Garage Door WiFi signal strength sensor."""

    def __init__(self, coordinator: CenturionGarageDataUpdateCoordinator) -> None:
        """Initialize the WiFi signal sensor."""
        super().__init__(coordinator)
        self._attr_unique_id = "centurion_wifi_signal"
        self._attr_name = "WiFi Signal Strength"
        self._attr_device_class = SensorDeviceClass.SIGNAL_STRENGTH
        self._attr_state_class = SensorStateClass.MEASUREMENT
        self._attr_native_unit_of_measurement = SIGNAL_STRENGTH_DECIBELS_MILLIWATT
        self._attr_icon = "mdi:wifi"

    @property
    def native_value(self) -> int | None:
        """Return the WiFi signal strength in dBm."""
        if self.coordinator.data:
            value = self.coordinator.data.get("wdBm")
            if value is not None:
                try:
                    return int(value)
                except (ValueError, TypeError):
                    return None
        return None


class CenturionDoorOperationCounterSensor(CenturionBaseSensor):
    """Centurion Garage Door operation counter sensor."""

    def __init__(self, coordinator: CenturionGarageDataUpdateCoordinator) -> None:
        """Initialize the door operation counter sensor."""
        super().__init__(coordinator)
        self._attr_unique_id = "centurion_door_operation_counter"
        self._attr_name = "Cycles"
        self._attr_state_class = SensorStateClass.TOTAL_INCREASING
        self._attr_native_unit_of_measurement = "operations"
        self._attr_icon = "mdi:counter"

    @property
    def native_value(self) -> int | None:
        """Return the number of door operations."""
        if self.coordinator.data:
            value = self.coordinator.data.get("cycles")
            if value is not None:
                try:
                    return int(value)
                except (ValueError, TypeError):
                    return None
        return None


class CenturionDoorMessageSensor(CenturionBaseSensor):
    """Centurion Garage Door message sensor."""

    def __init__(self, coordinator: CenturionGarageDataUpdateCoordinator) -> None:
        """Initialize the door message sensor."""
        super().__init__(coordinator)
        self._attr_unique_id = "centurion_door_message"
        self._attr_name = "Door Message"
        self._attr_icon = "mdi:garage-alert"

    @property
    def native_value(self) -> str | None:
        """Return the secondary door message reported by the API."""
        if self.coordinator.data:
            _, message = parse_door_status(self.coordinator.data.get("door"))
            return message
        return None


class CenturionErrorCodeSensor(CenturionBaseSensor):
    """Centurion Garage Door error code sensor."""

    def __init__(self, coordinator: CenturionGarageDataUpdateCoordinator) -> None:
        """Initialize the error code sensor."""
        super().__init__(coordinator)
        self._attr_unique_id = "centurion_error_code"
        self._attr_name = "Error Code"
        self._attr_icon = "mdi:alert-circle-outline"

    @property
    def native_value(self) -> int | str | None:
        """Return the current error code."""
        if self.coordinator.data:
            value = self.coordinator.data.get("error")
            if value is not None:
                try:
                    return int(value)
                except (ValueError, TypeError):
                    return str(value)
        return None


class CenturionCameraStatusSensor(CenturionBaseSensor):
    """Centurion Garage Door camera status sensor."""

    def __init__(self, coordinator: CenturionGarageDataUpdateCoordinator) -> None:
        """Initialize the camera status sensor."""
        super().__init__(coordinator)
        self._attr_unique_id = "centurion_camera_status"
        self._attr_name = "Camera Status"
        self._attr_icon = "mdi:cctv"

    @property
    def native_value(self) -> str | None:
        """Return the camera status reported by the API."""
        if self.coordinator.data:
            value = self.coordinator.data.get("camera")
            if value is not None:
                return str(value)
        return None


class CenturionDoorTimestampSensor(CenturionBaseSensor):
    """Centurion Garage Door door timestamp sensor."""

    def __init__(self, coordinator: CenturionGarageDataUpdateCoordinator) -> None:
        """Initialize the door timestamp sensor."""
        super().__init__(coordinator)
        self._attr_unique_id = "centurion_door_timestamp"
        self._attr_name = "Door Event Timestamp"
        self._attr_icon = "mdi:clock-outline"

    @property
    def native_value(self) -> str | None:
        """Return the door timestamp reported by the API."""
        if self.coordinator.data:
            value = self.coordinator.data.get("dt")
            if value is not None:
                return str(value)
        return None
