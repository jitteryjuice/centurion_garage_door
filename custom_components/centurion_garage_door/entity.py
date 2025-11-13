"""Base entity for Centurion Garage Door."""

from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
)

from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
)


class CenturionGarageEntity(CoordinatorEntity):
    """Base entity for Centurion Garage Door integration."""

    def __init__(self, coordinator: DataUpdateCoordinator) -> None:
        """Initialize CenturionGarageEntity with coordinator."""
        super().__init__(coordinator)
