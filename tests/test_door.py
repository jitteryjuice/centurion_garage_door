"""Tests for Centurion door status parsing."""

from __future__ import annotations

import importlib.util
import pathlib
import unittest

DOOR_MODULE = (
    pathlib.Path(__file__).parents[1]
    / "custom_components"
    / "centurion_garage_door"
    / "door.py"
)

spec = importlib.util.spec_from_file_location("centurion_door", DOOR_MODULE)
door = importlib.util.module_from_spec(spec)
if spec is None or spec.loader is None:
    msg = "Unable to load door parser module"
    raise RuntimeError(msg)
spec.loader.exec_module(door)


class DoorStatusParsingTest(unittest.TestCase):
    """Test parsing primary state and secondary door messages."""

    def check_parse(self, raw_state: str, expected: tuple[str, str | None]) -> None:
        """Check parsed door status against an expected tuple."""
        actual = door.parse_door_status(raw_state)
        if actual != expected:
            msg = f"Expected {expected!r}, got {actual!r}"
            raise AssertionError(msg)

    def test_closed_with_opener_reset_message(self) -> None:
        """Closed remains the primary state when an opener message is present."""
        self.check_parse("Closed|Opener reset", ("closed", "Opener reset"))

    def test_state_without_message(self) -> None:
        """States without a separator keep working."""
        self.check_parse("Opening", ("opening", None))

    def test_empty_message_is_ignored(self) -> None:
        """Blank secondary messages are normalized to None."""
        self.check_parse("Closed| ", ("closed", None))

    def test_message_with_extra_separator_keeps_context(self) -> None:
        """Messages can include additional separators."""
        self.check_parse(
            "Closed|Opener reset|manual",
            ("closed", "Opener reset|manual"),
        )

    def test_opened_with_dot_message(self) -> None:
        """Dot-separated alert messages keep the door state parseable."""
        self.check_parse(
            "Opened. Intruder Alert",
            ("opened", "Intruder Alert"),
        )

    def test_unknown_dotted_text_is_not_split(self) -> None:
        """Only known door states use the dot-separated message format."""
        self.check_parse(
            "Controller rebooted. Waiting for status",
            ("controller rebooted. waiting for status", None),
        )

    def test_closed_by_transmitter_uses_closed_state(self) -> None:
        """Transmitter operation details do not hide the primary door state."""
        self.check_parse("Closed by transmitter No.1", ("closed", None))

    def test_opened_by_transmitter_uses_opened_state(self) -> None:
        """Opened transmitter reports remain parseable as open."""
        self.check_parse("Opened by transmitter No.3", ("opened", None))

    def test_transmitter_source_is_normalized(self) -> None:
        """Transmitter source values use a consistent display format."""
        actual = door.parse_door_source("Closed by transmitter No.1")
        if actual != "Transmitter No. 1":
            msg = f"Expected transmitter source, got {actual!r}"
            raise AssertionError(msg)

    def test_home_assistant_source_is_normalized(self) -> None:
        """Home Assistant source values use a stable slug."""
        actual = door.parse_door_source("Opened by Home Assistant")
        if actual != "home-assistant":
            msg = f"Expected home-assistant source, got {actual!r}"
            raise AssertionError(msg)


if __name__ == "__main__":
    unittest.main()
