"""DataUpdateCoordinator for Centurion Garage Door."""

from __future__ import annotations

from typing import TYPE_CHECKING

from homeassistant.exceptions import ConfigEntryAuthFailed
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import (
    CenturionGarageApiClient,
    CenturionGarageApiClientAuthenticationError,
    CenturionGarageApiClientError,
)

if TYPE_CHECKING:
    import logging
    from datetime import timedelta

    from homeassistant.core import HomeAssistant


class CenturionGarageDataUpdateCoordinator(DataUpdateCoordinator):
    """
    DataUpdateCoordinator for Centurion Garage Door integration.

    Coordinates periodic data updates and provides access to the
    CenturionGarageApiClient.

    """

    def __init__(
        self,
        hass: HomeAssistant,
        api_client: CenturionGarageApiClient,
        logger: logging.Logger,
        name: str,
        update_interval: timedelta,
    ) -> None:
        """
        Initialize the CenturionGarageDataUpdateCoordinator.

        Args:
            hass: Home Assistant instance.
            api_client: CenturionGarageApiClient instance for device communication.
            logger: Logger for integration logging.
            name: Name of the coordinator.
            update_interval: Interval for periodic updates.

        """
        super().__init__(
            hass, logger=logger, name=name, update_interval=update_interval
        )
        self.api_client = api_client

    async def _async_update_data(self) -> dict:
        try:
            return await self.api_client.async_get_data()
        except CenturionGarageApiClientAuthenticationError as exc:
            raise ConfigEntryAuthFailed(exc) from exc
        except CenturionGarageApiClientError as exc:
            raise UpdateFailed(exc) from exc
