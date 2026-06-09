"""Cover platform for Centurion Garage Door integration."""

import logging
from homeassistant.components.cover import CoverEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.const import (
    STATE_CLOSED,
    STATE_OPEN,
    STATE_OPENING,
    STATE_CLOSING,
    STATE_PROBLEM,
    STATE_UNKNOWN,
    STATE_PAUSED,
)
from custom_components.centurion_garage_door.coordinator import (
    CenturionGarageDataUpdateCoordinator,
)
from .entity import CenturionGarageEntity
from .const import DOMAIN
from .door import parse_door_status

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Centurion Garage Door cover entity from a config entry."""
    runtime_data = hass.data[DOMAIN][config_entry.entry_id]
    coordinator: CenturionGarageDataUpdateCoordinator = runtime_data.coordinator
    async_add_entities([CenturionGarageDoor(coordinator)], update_before_add=True)


class CenturionGarageDoor(CenturionGarageEntity, CoverEntity):
    """Centurion Garage Door cover entity."""

    def __init__(self, coordinator: CenturionGarageDataUpdateCoordinator) -> None:
        """Initialize CenturionGarageDoor entity."""
        super().__init__(coordinator)
        self.coordinator: CenturionGarageDataUpdateCoordinator = coordinator
        self._attr_unique_id = "centurion_garage_cover"

    @property
    def device_info(self) -> dict:
        """Return device information for Home Assistant."""
        api_client = self.coordinator.api_client
        return {
            "identifiers": {(DOMAIN, api_client.ip_address)},
            "name": "Door",
            "manufacturer": "Centurion",
            "model": "Garage",
        }

    @property
    def device_class(self) -> str:
        """Return the device class."""
        return "garage"

    @property
    def supported_features(self) -> int:
        """Return supported features (open, close, stop)."""
        return 7

    @property
    def _door_state(self) -> str:
        """Get current door state from coordinator data."""
        if self.coordinator.data:
            door_state = self.coordinator.data.get("door", "unknown")
            primary_state, _ = parse_door_status(door_state)
            if primary_state == "opening":
                return STATE_OPENING
            elif primary_state == "closing":
                return STATE_CLOSING
            elif primary_state in {"opened", "open"}:
                return STATE_OPEN
            elif primary_state in {"closed", "close"}:
                return STATE_CLOSED
            elif primary_state in {"stopped", "stop"}:
                return STATE_PAUSED
            elif "error" in str(door_state).lower():
                return STATE_PROBLEM
        return STATE_UNKNOWN

    @property
    def extra_state_attributes(self) -> dict:
        """Return entity specific state attributes."""
        raw_door_state = None
        door_message = None
        if self.coordinator.data:
            raw_door_state = self.coordinator.data.get("door")
            _, door_message = parse_door_status(raw_door_state)
        return {
            "raw_door": raw_door_state,
            "door_message": door_message,
        }

    @property
    def name(self) -> str:
        """Return the name of the entity."""
        return "Centurion Garage Door"

    @property
    def is_closed(self) -> bool:
        """Return True if the door is closed."""
        return self._door_state == STATE_CLOSED

    @property
    def state(self) -> str:
        """Return the current state."""
        return self._door_state

    async def async_open_cover(self) -> None:
        """Open the garage door."""
        api_client = self.coordinator.api_client
        await api_client.open_door()
        await self.coordinator.async_request_refresh()

    async def async_close_cover(self) -> None:
        """Close the garage door."""
        api_client = self.coordinator.api_client
        await api_client.close_door()
        await self.coordinator.async_request_refresh()

    async def async_stop_cover(self) -> None:
        """Stop the garage door."""
        api_client = self.coordinator.api_client
        await api_client.stop_door()
        await self.coordinator.async_request_refresh()
