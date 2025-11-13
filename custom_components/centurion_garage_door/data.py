"""Custom types for Centurion Garage Door."""

from dataclasses import dataclass


@dataclass
class CenturionGarageRuntimeData:
    client: object
    coordinator: object
    integration: object
