"""Camera platform for Centurion Garage Door integration."""

from homeassistant.components.mjpeg.camera import MjpegCamera
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from custom_components.centurion_garage_door.coordinator import (
    CenturionGarageDataUpdateCoordinator,
)
from .entity import CenturionGarageEntity
from .const import DOMAIN
import logging

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Centurion Garage Door camera entity from a config entry."""
    runtime_data = hass.data[DOMAIN][config_entry.entry_id]
    coordinator: CenturionGarageDataUpdateCoordinator = runtime_data.coordinator
    async_add_entities([CenturionGarageCamera(coordinator)])


class CenturionGarageCamera(CenturionGarageEntity, MjpegCamera):
    """Centurion Garage Door camera entity."""

    def __init__(self, coordinator: CenturionGarageDataUpdateCoordinator) -> None:
        """Initialize CenturionGarageCamera entity."""
        CenturionGarageEntity.__init__(self, coordinator)
        ip = coordinator.api_client.ip_address
        port = 88
        mjpeg_url = f"http://{ip}:{port}"
        MjpegCamera.__init__(self, mjpeg_url=mjpeg_url, still_image_url=None)
        self.coordinator = coordinator
        self._attr_unique_id = "centurion_garage_camera"
        self._attr_name = "Centurion Garage Camera"

    @property
    def brand(self) -> str:
        """Return the camera brand."""
        return "Centurion"

    @property
    def model(self) -> str:
        """Return the camera model."""
        return "Centurion Garage Camera"

    @property
    def device_info(self) -> dict:
        """Return device information for Home Assistant."""
        api_client = self.coordinator.api_client
        return {
            "identifiers": {(DOMAIN, api_client.ip_address)},
            "name": "Camera",
            "manufacturer": "Centurion",
            "model": "Garage",
        }
