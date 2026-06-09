"""Door status parsing helpers for Centurion Garage Door."""

from __future__ import annotations

import re

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

_ACTION_SOURCE_RE = re.compile(r"^(?P<state>\w+)\s+by\s+(?P<source>.+)$", re.IGNORECASE)
_TRANSMITTER_RE = re.compile(r"^transmitter\s+no\.?\s*(?P<number>\d+)$", re.IGNORECASE)


def _split_status(raw_state: object) -> tuple[str, str | None]:
    """Return the unsanitized primary value and optional status message."""
    raw_door_state = str(raw_state)
    primary_state, separator, status_message = raw_door_state.partition("|")
    if not separator:
        primary_state, separator, status_message = raw_door_state.partition(". ")
        if separator and primary_state.strip().lower() not in DOOR_STATES:
            primary_state = raw_door_state
            separator = ""
            status_message = None

    return primary_state.strip(), status_message.strip() if separator else None


def _split_action_source(primary_state: str) -> tuple[str, str | None]:
    """Split '<state> by <source>' values when the state is known."""
    match = _ACTION_SOURCE_RE.match(primary_state)
    if match is None:
        return primary_state, None

    state = match.group("state").strip()
    if state.lower() not in DOOR_STATES:
        return primary_state, None

    return state, _normalize_source(match.group("source"))


def _normalize_source(source: str) -> str | None:
    """Normalize an API operation source to a stable Home Assistant attribute."""
    source = source.strip()
    if not source:
        return None

    if source.lower().replace(" ", "-") in {"home-assistant", "homeassistant"}:
        return "home-assistant"

    transmitter = _TRANSMITTER_RE.match(source)
    if transmitter:
        return f"Transmitter No. {transmitter.group('number')}"

    return source


def parse_door_status(raw_state: object) -> tuple[str, str | None]:
    """Return the primary door state and optional status message."""
    primary_state, status_message = _split_status(raw_state)
    primary_state, _ = _split_action_source(primary_state)
    primary_state = primary_state.lower()
    return primary_state, status_message or None


def parse_door_source(raw_state: object) -> str | None:
    """Return the operation source from the API door value, if reported."""
    primary_state, _ = _split_status(raw_state)
    _, source = _split_action_source(primary_state)
    return source
