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


if __name__ == "__main__":
    unittest.main()
