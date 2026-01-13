"""Centurion Garage Door custom integration package."""

from __future__ import annotations
from datetime import timedelta
from typing import TYPE_CHECKING

from homeassistant.const import Platform
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.loader import async_get_loaded_integration

from .api import CenturionGarageApiClient
import logging
from .const import DOMAIN, CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL
from .coordinator import CenturionGarageDataUpdateCoordinator
from .data import CenturionGarageRuntimeData

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant
    from homeassistant.config_entries import ConfigEntry

PLATFORMS: list[Platform] = [
    Platform.COVER,
    Platform.CAMERA,
    Platform.SWITCH,
    Platform.SENSOR,
]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Centurion Garage Door integration using UI."""
    # Ensure DOMAIN and entry_id are initialized in hass.data
    if DOMAIN not in hass.data:
        hass.data[DOMAIN] = {}

    scan_interval = (
        entry.options.get(CONF_SCAN_INTERVAL) if hasattr(entry, "options") else None
    )
    if scan_interval is None:
        scan_interval = entry.data.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL)
    try:
        scan_interval = int(scan_interval)
    except (TypeError, ValueError):
        scan_interval = DEFAULT_SCAN_INTERVAL
    coordinator = CenturionGarageDataUpdateCoordinator(
        hass=hass,
        api_client=CenturionGarageApiClient(
            ip_address=entry.data.get("ip_address", ""),
            api_key=entry.data.get("api_key", ""),
            session=async_get_clientsession(hass),
        ),
        logger=logging.getLogger(__name__),
        name=DOMAIN,
        update_interval=timedelta(seconds=scan_interval),
    )
    hass.data[DOMAIN][entry.entry_id] = CenturionGarageRuntimeData(
        client=coordinator.api_client,
        integration=async_get_loaded_integration(hass, entry.domain),
        coordinator=coordinator,
    )
    entry.runtime_data = hass.data[DOMAIN][entry.entry_id]
    await coordinator.async_config_entry_first_refresh()
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    entry.async_on_unload(entry.add_update_listener(async_reload_entry))
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Handle removal of an entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)


async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Reload config entry."""
    await hass.config_entries.async_reload(entry.entry_id)
