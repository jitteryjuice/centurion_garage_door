"""Switch platform for Centurion Garage Door integration."""

import logging
from datetime import timedelta
from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from custom_components.centurion_garage_door.coordinator import (
    CenturionGarageDataUpdateCoordinator,
)
from .entity import CenturionGarageEntity
from .const import DOMAIN

SCAN_INTERVAL = timedelta(seconds=30)
_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Centurion Garage Door switch entities from a config entry."""
    runtime_data = hass.data[DOMAIN][config_entry.entry_id]
    coordinator: CenturionGarageDataUpdateCoordinator = runtime_data.coordinator
    async_add_entities(
        [
            CenturionLampSwitch(coordinator),
            CenturionVacationSwitch(coordinator),
        ]
    )


class CenturionBaseSwitch(CenturionGarageEntity, SwitchEntity):
    """Base class for Centurion Garage Door switches."""

    def __init__(self, coordinator: CenturionGarageDataUpdateCoordinator) -> None:
        """Initialize the base switch class."""
        super().__init__(coordinator)
        self.coordinator = coordinator

    @property
    def device_info(self) -> DeviceInfo:
        """Return device information for Home Assistant."""
        api_client = getattr(self.coordinator, "api_client", None)
        ip = getattr(api_client, "ip_address", "unknown") if api_client else "unknown"
        return DeviceInfo(
            identifiers={(DOMAIN, ip)},
            name="Switch",
            manufacturer="Centurion",
            model="Garage",
        )


class CenturionLampSwitch(CenturionBaseSwitch):
    """Centurion Garage Door lamp switch."""

    def __init__(self, coordinator: CenturionGarageDataUpdateCoordinator) -> None:
        """Initialize the lamp switch."""
        super().__init__(coordinator)
        self._attr_unique_id = "centurion_lamp_switch"
        self._attr_name = "Lamp Switch"

    @property
    def is_on(self) -> bool:
        """Return True if the lamp is on."""
        if self.coordinator.data:
            lamp_state = self.coordinator.data.get("lamp", "off")
            return lamp_state.lower() == "on"
        return False

    @property
    def icon(self) -> str:
        """Return the icon for the lamp switch."""
        return "mdi:lightbulb"

    async def async_turn_on(self) -> None:
        """Turn on the lamp."""
        api_client = self.coordinator.api_client
        await api_client.lamp_on()
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self) -> None:
        """Turn off the lamp."""
        api_client = self.coordinator.api_client
        await api_client.lamp_off()
        await self.coordinator.async_request_refresh()


class CenturionVacationSwitch(CenturionBaseSwitch):
    """Centurion Garage Door vacation mode switch."""

    def __init__(self, coordinator: CenturionGarageDataUpdateCoordinator) -> None:
        """Initialize the vacation mode switch."""
        super().__init__(coordinator)
        self._attr_unique_id = "centurion_vacation_switch"
        self._attr_name = "Vacation Mode"

    @property
    def is_on(self) -> bool:
        """Return True if vacation mode is on."""
        if self.coordinator.data:
            vacation_state = self.coordinator.data.get("vacation", "off")
            return vacation_state.lower() == "on"
        return False

    @property
    def icon(self) -> str:
        """Return the icon for vacation mode switch."""
        return "mdi:beach"

    async def async_turn_on(self) -> None:
        """Turn on vacation mode."""
        api_client = self.coordinator.api_client
        await api_client.vacation_on()
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self) -> None:
        """Turn off vacation mode."""
        api_client = self.coordinator.api_client
        await api_client.vacation_off()
        await self.coordinator.async_request_refresh()
