"""Cover platform for Centurion Garage Door integration."""

import logging
import contextlib
from homeassistant.components.cover import CoverEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.const import STATE_CLOSED, STATE_OPEN, STATE_OPENING, STATE_CLOSING
from custom_components.centurion_garage_door.coordinator import (
    CenturionGarageDataUpdateCoordinator,
)
from .entity import CenturionGarageEntity
from .const import DOMAIN

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
        self._state = STATE_CLOSED
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

    async def async_update(self) -> None:
        """Fetch the latest state from the device."""
        api_client = self.coordinator.api_client
        with contextlib.suppress(Exception):
            door_state = await api_client.get_door_state()
            if "opening" in door_state:
                self._state = STATE_OPENING
            elif "closing" in door_state:
                self._state = STATE_CLOSING
            elif "open" in door_state:
                self._state = STATE_OPEN
            elif "close" in door_state:
                self._state = STATE_CLOSED
            elif "stopped" in door_state or "error" in door_state:
                self._state = None
            else:
                self._state = None

    @property
    def name(self) -> str:
        """Return the name of the entity."""
        return "Centurion Garage Door"

    @property
    def is_closed(self) -> bool:
        """Return True if the door is closed."""
        return self._state == STATE_CLOSED

    @property
    def state(self) -> str:
        """Return the current state."""
        return self._state if self._state is not None else "unknown"

    async def async_open_cover(self) -> None:
        """Open the garage door."""
        api_client = self.coordinator.api_client
        with contextlib.suppress(Exception):
            await api_client.open_door()
            self._state = STATE_OPEN
            self.async_schedule_update_ha_state()

    async def async_close_cover(self) -> None:
        """Close the garage door."""
        api_client = self.coordinator.api_client
        with contextlib.suppress(Exception):
            await api_client.close_door()
            self._state = STATE_CLOSED
            self.async_schedule_update_ha_state()

    async def async_stop_cover(self) -> None:
        """Stop the garage door."""
        api_client = self.coordinator.api_client
        with contextlib.suppress(Exception):
            await api_client.stop_door()
