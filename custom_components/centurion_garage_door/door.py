"""Door status parsing helpers for Centurion Garage Door."""

from __future__ import annotations


def parse_door_status(raw_state: object) -> tuple[str, str | None]:
    """Return the primary door state and optional status message."""
    primary_state, separator, status_message = str(raw_state).partition("|")
    primary_state = primary_state.strip().lower()
    status_message = status_message.strip() if separator else None
    return primary_state, status_message or None
