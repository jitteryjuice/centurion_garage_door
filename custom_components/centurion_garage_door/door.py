"""Door status parsing helpers for Centurion Garage Door."""

from __future__ import annotations

DOOR_STATES = {
    "close",
    "closed",
    "closing",
    "open",
    "opened",
    "opening",
    "stop",
    "stopped",
}


def parse_door_status(raw_state: object) -> tuple[str, str | None]:
    """Return the primary door state and optional status message."""
    raw_door_state = str(raw_state)
    primary_state, separator, status_message = raw_door_state.partition("|")
    if not separator:
        primary_state, separator, status_message = raw_door_state.partition(". ")
        if separator and primary_state.strip().lower() not in DOOR_STATES:
            primary_state = raw_door_state
            separator = ""
            status_message = None

    primary_state = primary_state.strip().lower()
    status_message = status_message.strip() if separator else None
    return primary_state, status_message or None
