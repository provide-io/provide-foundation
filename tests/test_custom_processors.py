#
# tests/test_custom_processors.py
#
"""
Unit tests for src.pyvider.telemetry.logger.custom_processors.py
"""
import pytest
import structlog  # For DropEvent

from pyvider.telemetry.logger.custom_processors import (
    add_logger_name_emoji_prefix,
    # add_das_emoji_prefix, # Will add if testing that
    # _LOGGER_NAME_EMOJI_PREFIXES, # For direct manipulation if needed
    # clear_emoji_cache # To reset state for emoji cache tests
    filter_by_level_custom,
)
from pyvider.telemetry.types import LogLevelStr  # Corrected import for type hints

# Helper for level to numeric mapping, mirroring what's in config.py
_LEVEL_TO_NUMERIC_TEST_MAP: dict[LogLevelStr, int] = {
    "CRITICAL": 50, "ERROR": 40, "WARNING": 30, "INFO": 20, "DEBUG": 10, "TRACE": 5, "NOTSET": 0
}

class TestLevelFilterCustom:
    def test_filter_with_unrecognized_event_level_defaults_to_info_numeric(self) -> None:
        """
        Tests that if event_dict['level'] is an unrecognized string, it defaults
        to the numeric value of INFO for filtering purposes.
        This covers the .get() fallback in _LevelFilter.__call__ (around line 217-218).
        """
        # Filter configured with default level WARNING (30)
        # Module levels are empty for simplicity
        log_filter = filter_by_level_custom(
            default_level_str="WARNING",
            module_levels={},
            level_to_numeric_map=_LEVEL_TO_NUMERIC_TEST_MAP
        )

        # Event with an unrecognized level string
        # This "UNRECOGNIZED_LEVEL" will default to INFO's numeric value (20)
        # Since 20 (INFO) < 30 (WARNING threshold), this event should be dropped.
        event_dict_unrecognized_level_dropped = {
            "logger_name": "test_logger",
            "level": "UNRECOGNIZED_LEVEL", # This will default to INFO (20)
            "event": "message with unrecognized level"
        }
        with pytest.raises(structlog.DropEvent):
            log_filter(None, "", event_dict_unrecognized_level_dropped)

        # Event with an unrecognized level string, but threshold is DEBUG (10)
        # "UNRECOGNIZED_LEVEL" (defaults to INFO=20) should pass if threshold is DEBUG (10)
        log_filter_debug_threshold = filter_by_level_custom(
            default_level_str="DEBUG", # Threshold is 10
            module_levels={},
            level_to_numeric_map=_LEVEL_TO_NUMERIC_TEST_MAP
        )
        event_dict_unrecognized_level_passes = {
            "logger_name": "test_logger",
            "level": "ANOTHER_UNRECOGNIZED_LEVEL", # Defaults to INFO (20)
            "event": "message that should pass"
        }
        # No DropEvent should be raised
        try:
            result_event = log_filter_debug_threshold(None, "", event_dict_unrecognized_level_passes)
            assert result_event == event_dict_unrecognized_level_passes
        except structlog.DropEvent: # pragma: no cover
            pytest.fail("Event with unrecognized level (defaulting to INFO) was unexpectedly dropped for DEBUG threshold.")

# Placeholder for next tests
class TestAddLoggerNameEmojiPrefix:
    def test_add_logger_name_emoji_prefix_event_is_none_but_emoji_exists(self) -> None:
        """
        Tests the case where event_dict['event'] is None, but a logger name emoji
        is found. The event should become just the emoji.
        This covers lines around 388-389.
        """
        # Ensure a known logger name that has an emoji
        # From _LOGGER_NAME_EMOJI_PREFIXES in custom_processors.py:
        # 'test.basic': '🧪'
        logger_name_with_emoji = "test.basic"
        expected_emoji = "🧪"

        event_dict = {
            "logger_name": logger_name_with_emoji,
            "event": None # Event message is None
        }

        processed_event = add_logger_name_emoji_prefix(None, "info", event_dict.copy())

        assert "event" in processed_event
        assert processed_event["event"] == expected_emoji

    def test_add_logger_name_emoji_prefix_event_is_none_and_no_emoji(self) -> None:
        """
        Tests the case where event_dict['event'] is None, and no specific emoji
        is found (falls back to default, or empty if default is misconfigured/not found).
        """
        # This logger name is not in _LOGGER_NAME_EMOJI_PREFIXES, so it will use default '🔹'
        logger_name_no_specific_emoji = "some.other.logger.name"
        expected_default_emoji = "🔹" # Default emoji from _LOGGER_NAME_EMOJI_PREFIXES

        event_dict = {
            "logger_name": logger_name_no_specific_emoji,
            "event": None # Event message is None
        }

        processed_event = add_logger_name_emoji_prefix(None, "info", event_dict.copy())

        assert "event" in processed_event
        assert processed_event["event"] == expected_default_emoji

    def test_add_logger_name_emoji_prefix_event_exists_and_emoji_exists(self) -> None:
        """
        Standard case: event message exists, and emoji is found.
        """
        logger_name_with_emoji = "pyvider.telemetry.logger" # Expected: 📝
        expected_emoji = "📝"
        original_message = "This is a test message."

        event_dict = {
            "logger_name": logger_name_with_emoji,
            "event": original_message
        }

        processed_event = add_logger_name_emoji_prefix(None, "info", event_dict.copy())

        assert "event" in processed_event
        assert processed_event["event"] == f"{expected_emoji} {original_message}"
