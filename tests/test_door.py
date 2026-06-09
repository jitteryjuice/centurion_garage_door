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
assert spec and spec.loader
spec.loader.exec_module(door)


class DoorStatusParsingTest(unittest.TestCase):
    """Test parsing primary state and secondary door messages."""

    def test_closed_with_opener_reset_message(self) -> None:
        """Closed remains the primary state when an opener message is present."""
        self.assertEqual(
            door.parse_door_status("Closed|Opener reset"),
            ("closed", "Opener reset"),
        )

    def test_state_without_message(self) -> None:
        """States without a separator keep working."""
        self.assertEqual(door.parse_door_status("Opening"), ("opening", None))

    def test_empty_message_is_ignored(self) -> None:
        """Blank secondary messages are normalized to None."""
        self.assertEqual(door.parse_door_status("Closed| "), ("closed", None))

    def test_message_with_extra_separator_keeps_context(self) -> None:
        """Messages can include additional separators."""
        self.assertEqual(
            door.parse_door_status("Closed|Opener reset|manual"),
            ("closed", "Opener reset|manual"),
        )


if __name__ == "__main__":
    unittest.main()
