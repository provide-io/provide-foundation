#
# test_coverage_completion.py
#
"""
Additional tests specifically designed to achieve 100% code coverage.

This module targets the uncovered lines identified in the coverage report:
- src/pyvider/telemetry/core.py: lines 97->105, 130->exit, 153->155, 290-293, 437, 532->536
- src/pyvider/telemetry/logger/base.py: lines 166, 169-172, 309-310, 416-417
- src/pyvider/telemetry/logger/custom_processors.py: lines 89, 124->136, 130, 132, 359->364, 367-368, 437

These tests focus on edge cases, error conditions, and rarely-used code paths.
"""
import asyncio
import io
import logging as stdlib_logging  # Renamed to avoid conflict
import os
import sys
import threading
from unittest.mock import MagicMock, patch

import pytest
import structlog

from pyvider.telemetry import (
    LoggingConfig,
    TelemetryConfig,
    logger,
    setup_telemetry,
    shutdown_pyvider_telemetry,
)
from pyvider.telemetry.core import (
    _create_core_setup_logger,
    _handle_globally_disabled_setup,
    _set_log_stream_for_testing,
    reset_pyvider_setup_for_testing,
)
from pyvider.telemetry.logger.custom_processors import (
    _compute_emoji_for_logger_name,
    clear_emoji_cache,
    get_emoji_cache_stats,
)
from pyvider.telemetry.logger.emoji_matrix import show_emoji_matrix
from pyvider.telemetry.types import (
    TRACE_LEVEL_NUM,  # Corrected import
    LogLevelStr,  # Corrected import
)


def test_core_setup_logger_with_existing_handlers() -> None:
    """Test core setup logger when handlers already exist."""
    # This covers the handler cleanup path in _create_core_setup_logger

    test_logger_name = "test.cleanup.logger"
    test_logger = stdlib_logging.getLogger(test_logger_name)

    # Add a handler to trigger cleanup path
    handler = stdlib_logging.StreamHandler()
    test_logger.addHandler(handler)

    # Create another handler to test cleanup
    another_handler = stdlib_logging.StreamHandler()
    test_logger.addHandler(another_handler)

    assert test_logger.hasHandlers()

    # This should clean up existing handlers
    with patch('pyvider.telemetry.core._CORE_SETUP_LOGGER_NAME', test_logger_name):
        result_logger = _create_core_setup_logger(globally_disabled=False)

    # Verify handlers were cleaned up and new one added
    assert result_logger.hasHandlers()
    # Original handlers should be removed, new one added
    assert len(result_logger.handlers) == 1


def test_globally_disabled_setup_with_existing_logger() -> None:
    """Test globally disabled setup when temp logger already exists."""
    # This covers the needs_configuration check in _handle_globally_disabled_setup

    temp_logger_name = "pyvider.telemetry.core_setup_temp_disabled_msg"
    temp_logger = stdlib_logging.getLogger(temp_logger_name)

    # Pre-configure the logger to trigger the needs_configuration check
    handler = stdlib_logging.StreamHandler(sys.stderr)
    temp_logger.addHandler(handler)

    # This should detect existing configuration
    _handle_globally_disabled_setup()

    # Verify it still works
    assert temp_logger.hasHandlers()


def test_logger_base_format_message_edge_cases() -> None:
    """Test edge cases in message formatting."""
    setup_telemetry()

    # Test with no args (should return original)
    result = logger._format_message_with_args("test message", ())
    assert result == "test message"

    # Test with single arg (covers special case)
    result = logger._format_message_with_args("test %s", ("value",))
    assert result == "test value"

    # Test with invalid format (should fallback)
    result = logger._format_message_with_args("test %q invalid", ("value",))
    assert result == "test %q invalid value"

    # Test with TypeError (should fallback)
    result = logger._format_message_with_args("test %s %s", ("only_one",))
    assert result == "test %s %s only_one"

    # Test with multiple args in tuple
    result = logger._format_message_with_args("test %s %d", ("str", 42))
    assert result == "test str 42"


def test_logger_base_setattr_coverage() -> None:
    """Test the __setattr__ method for coverage."""
    setup_telemetry()

    # Test setting internal attributes (should work)
    logger._internal_logger = "test" # type: ignore[assignment]
    logger._is_configured_by_setup = True
    logger._active_config = None

    # Test setting other attributes (should also work)
    logger.test_attr = "test_value" # type: ignore[attr-defined]
    assert logger.test_attr == "test_value" # type: ignore[attr-defined]


def test_custom_processors_emoji_cache_functions() -> None:
    """Test emoji cache utility functions."""
    # Clear cache first
    clear_emoji_cache()

    # Test cache stats with empty cache
    stats = get_emoji_cache_stats()
    assert stats["cache_size"] == 0
    assert stats["cache_limit"] == 1000
    assert stats["cache_utilization"] == 0.0

    # Add some entries to cache by using the logger
    # Explicitly enable logger name emojis for this test to ensure cache is populated
    setup_telemetry(TelemetryConfig(logging=LoggingConfig(logger_name_emoji_prefix_enabled=True, console_formatter="key_value")))
    test_logger1 = logger.get_logger("pyvider.telemetry.core.test")
    test_logger2 = logger.get_logger("unknown.test")

    test_logger1.info("Test message 1")
    test_logger2.info("Test message 2")

    # Check cache has entries
    stats = get_emoji_cache_stats()
    assert stats["cache_size"] > 0

    # Test clear function
    clear_emoji_cache()
    stats = get_emoji_cache_stats()
    assert stats["cache_size"] == 0


def test_emoji_matrix_display() -> None:
    """Test emoji matrix display function."""
    # Test with environment variable disabled (default)
    with patch.dict(os.environ, {"PYVIDER_SHOW_EMOJI_MATRIX": "false"}):
        # Should return early without logging
        show_emoji_matrix()

    # Test with environment variable enabled
    with patch.dict(os.environ, {"PYVIDER_SHOW_EMOJI_MATRIX": "true"}):
        setup_telemetry()

        # Capture the output
        with patch('pyvider.telemetry.logger.base.logger') as mock_logger_module:
            mock_matrix_logger = MagicMock()
            mock_logger_module.get_logger.return_value = mock_matrix_logger

            show_emoji_matrix()

            # Verify the matrix logger was called
            mock_logger_module.get_logger.assert_called_with("pyvider.telemetry.emoji_matrix_display")
            mock_matrix_logger.info.assert_called_once()

            # Verify the content includes expected text
            call_args = mock_matrix_logger.info.call_args[0][0]
            assert "Pyvider Emoji Logging Contract" in call_args
            assert "Primary Emojis" in call_args
            assert "Secondary Emojis" in call_args
            assert "Tertiary Emojis" in call_args


def test_trace_level_custom_logger_name() -> None:
    """Test trace logging with custom logger name."""
    setup_telemetry(TelemetryConfig(
        logging=LoggingConfig(default_level="TRACE")
    ))

    # Test trace with custom logger name
    logger.trace("Custom trace message", _pyvider_logger_name="custom.trace.test")

    # Test trace with args and custom logger name
    logger.trace("Trace with %s and %d", "args", 42, _pyvider_logger_name="custom.trace.args")


def test_core_setup_environment_variable_edge_cases() -> None:
    """Test core setup with various environment variable values."""
    # Test with invalid log level
    with patch.dict(os.environ, {"PYVIDER_CORE_SETUP_LOG_LEVEL": "INVALID"}):
        test_logger = _create_core_setup_logger()
        # Should fall back to INFO level
        assert test_logger.level == 20  # INFO level


def test_shutdown_telemetry_coverage() -> None:
    """Test shutdown telemetry function."""
    setup_telemetry()

    # Test async shutdown
    async def test_shutdown() -> None:
        await shutdown_pyvider_telemetry(timeout_millis=1000)

    asyncio.run(test_shutdown())


def test_level_filter_edge_cases() -> None:
    """Test level filter with edge cases."""
    from pyvider.telemetry.logger.custom_processors import _LevelFilter

    # Create filter with complex module levels
    level_to_numeric: dict[LogLevelStr, int] = { # Explicitly type for clarity
        "CRITICAL": 50,
        "ERROR": 40,
        "WARNING": 30,
        "INFO": 20,
        "DEBUG": 10,
        "TRACE": TRACE_LEVEL_NUM,
        "NOTSET": 0,
    }

    filter_instance = _LevelFilter(
        default_level_str="INFO",
        module_levels={
            "app": "DEBUG",
            "app.auth": "TRACE",
            "app.auth.oauth": "DEBUG",  # Less specific than app.auth
        },
        level_to_numeric_map=level_to_numeric
    )

    # Test with unnamed filter target - DEBUG (10) < INFO (20) -> Should drop
    event_dict_debug_below_info = {
        "logger_name": "unnamed_filter_target",
        "level": "debug"
    }
    with pytest.raises(structlog.DropEvent):
        filter_instance(None, None, event_dict_debug_below_info)

    # Test with unknown level (should use INFO default) - INFO (20) == INFO (20) -> Should NOT drop
    event_dict_unknown_level_becomes_info = {
        "logger_name": "test.logger",
        "level": "UNKNOWN_LEVEL" # This will be treated as INFO
    }
    # Assert that DropEvent is NOT raised
    try:
        processed_event = filter_instance(None, None, event_dict_unknown_level_becomes_info)
        assert processed_event is event_dict_unknown_level_becomes_info # Should return the event dict
    except structlog.DropEvent: # pragma: no cover
        pytest.fail("structlog.DropEvent was raised unexpectedly for UNKNOWN_LEVEL case.")


def test_emoji_computation_edge_cases() -> None:
    """Test emoji computation for edge cases."""
    # Test with 'default' keyword (should be skipped)
    result = _compute_emoji_for_logger_name("default.something")
    assert result == "🔹"  # Should get default emoji

    # Test with exact 'default' match
    result = _compute_emoji_for_logger_name("default")
    assert result == "🔹"  # Should get default emoji

    # Test with unknown logger name
    result = _compute_emoji_for_logger_name("completely.unknown.logger.name")
    assert result == "🔹"  # Should get default emoji


def test_concurrent_setup_and_reset() -> None:
    """Test concurrent setup and reset operations."""
    def setup_worker() -> None:
        setup_telemetry(TelemetryConfig(service_name="concurrent_test"))
        logger.info("Concurrent test message")

    def reset_worker() -> None:
        reset_pyvider_setup_for_testing()

    # Run concurrent operations
    threads = []
    for i in range(5):
        if i % 2 == 0:
            t = threading.Thread(target=setup_worker)
        else:
            t = threading.Thread(target=reset_worker)
        threads.append(t)
        t.start()

    # Wait for all threads
    for t in threads:
        t.join()


def test_stream_testing_functions() -> None:
    """Test the testing stream functions."""
    # original_stream = sys.stderr # Not needed for this test logic
    test_stream = io.StringIO()

    # Test setting custom stream
    _set_log_stream_for_testing(test_stream)

    # Test resetting to None (should restore stderr)
    _set_log_stream_for_testing(None)

    # Test setting back to custom
    _set_log_stream_for_testing(test_stream)
    _set_log_stream_for_testing(None)


def test_processor_chain_edge_cases() -> None:
    """Test processor chain building edge cases."""
    # Test with all emoji options disabled
    config = TelemetryConfig(
        logging=LoggingConfig(
            logger_name_emoji_prefix_enabled=False,
            das_emoji_prefix_enabled=False,
            omit_timestamp=True,
        )
    )

    setup_telemetry(config)
    logger.info("Test message without emojis or timestamp")


def test_complex_nested_logger_names() -> None:
    """Test complex nested logger names for emoji mapping."""
    setup_telemetry()

    # Test deeply nested names
    nested_logger = logger.get_logger("pyvider.telemetry.core.sub.module.deep.nest")
    nested_logger.info("Deep nested message")

    # Test with numbers and special chars
    special_logger = logger.get_logger("app.module-1.sub_module.v2")
    special_logger.info("Special character message")


def test_exception_logging_edge_cases() -> None:
    """Test exception logging in various scenarios."""
    setup_telemetry()

    # Test exception with formatting args
    try:
        raise ValueError("Test exception with details")
    except ValueError:
        logger.exception("Error processing item %d of %d", 5, 10, operation="test")

    # Test exception with DAS fields
    try:
        raise ConnectionError("Connection failed")
    except ConnectionError:
        logger.exception(
            "Connection error occurred",
            domain="network",
            action="connect",
            status="error",
            host="example.com"
        )


@pytest.mark.asyncio
async def test_async_logging_edge_cases() -> None:
    """Test async logging in complex scenarios."""
    setup_telemetry()

    async def async_task_with_exception() -> None:
        try:
            raise RuntimeError("Async task failed")
        except RuntimeError:
            logger.exception("Async task exception", task_id="async_001")

    await async_task_with_exception()


def test_warning_alias() -> None:
    """Test the warn alias for warning."""
    setup_telemetry()

    # Test that warn and warning are the same
    assert logger.warn == logger.warning

    # Test using the alias
    logger.warn("Warning message using alias", code="W001")

# 🧪💯
