"""Custom types for Centurion Garage Door."""

from dataclasses import dataclass


@dataclass
class CenturionGarageRuntimeData:
    """Runtime data stored for a Centurion Garage config entry."""

    client: object
    coordinator: object
    integration: object
