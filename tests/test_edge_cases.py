#
# test_edge_cases.py
#
"""
Edge case and error condition tests for Pyvider Telemetry.

This module tests boundary conditions, error handling, and edge cases
that might not be covered in regular functional tests.
"""
from collections.abc import Callable
import io
import os
from typing import Any  # Added for type hints
from unittest.mock import patch

import pytest

from pyvider.telemetry import (
    LoggingConfig,
    TelemetryConfig,
    logger,  # This is the global PyviderLogger instance
    setup_telemetry,
)
from pyvider.telemetry.core import reset_pyvider_setup_for_testing


def test_invalid_environment_variables_handling(monkeypatch, capsys) -> None: # Added capsys
    """Tests handling of invalid environment variables."""
    # Define cases with expected warning snippet, or None if specific warning isn't critical/expected
    invalid_env_cases = [
        ("PYVIDER_LOG_LEVEL", "INVALID_LEVEL", "Invalid PYVIDER_LOG_LEVEL 'INVALID_LEVEL'"),
        ("PYVIDER_LOG_CONSOLE_FORMATTER", "invalid_formatter", "Invalid PYVIDER_LOG_CONSOLE_FORMATTER 'invalid_formatter'"),
        ("PYVIDER_LOG_LOGGER_NAME_EMOJI_ENABLED", "maybe", None), # bool parsing defaults, no specific warning expected by from_env
        ("PYVIDER_LOG_DAS_EMOJI_ENABLED", "sometimes", None),    # bool parsing defaults
        ("PYVIDER_LOG_OMIT_TIMESTAMP", "perhaps", None),       # bool parsing defaults
        ("PYVIDER_TELEMETRY_DISABLED", "kinda", None),         # bool parsing defaults
        ("PYVIDER_LOG_MODULE_LEVELS", "invalid:format:here,also:bad", "Invalid log level 'FORMAT:HERE' for module 'invalid'"),
    ]

    for env_var, invalid_value, expected_warning_snippet in invalid_env_cases:
        # Use monkeypatch to set environment variables cleanly for each case
        # Clear relevant env vars to ensure a clean slate for each iteration,
        # otherwise a previously set valid value might interfere.
        monkeypatch.setenv(env_var, invalid_value)

        # Remove other potentially interfering env vars if they are not the one being tested
        # This ensures that warnings from other default settings don't cloud the specific test.
        possible_interfering_vars = [
            "PYVIDER_LOG_LEVEL", "PYVIDER_LOG_CONSOLE_FORMATTER", "PYVIDER_LOG_MODULE_LEVELS"
        ]
        for var_to_clear in possible_interfering_vars:
            if var_to_clear != env_var:
                monkeypatch.delenv(var_to_clear, raising=False)

        config = TelemetryConfig.from_env()

        # Assert basic config structure
        assert config is not None
        assert isinstance(config.logging, LoggingConfig)

        # Verify fallback to defaults for the specific var being tested
        if env_var == "PYVIDER_LOG_LEVEL":
            assert config.logging.default_level == "DEBUG"  # Default from DEFAULT_ENV_CONFIG or fallback in from_env
        elif env_var == "PYVIDER_LOG_CONSOLE_FORMATTER":
            assert config.logging.console_formatter == "key_value"  # Default from DEFAULT_ENV_CONFIG or fallback in from_env

        # Check for specific warning message if one is expected
        captured = capsys.readouterr()
        if expected_warning_snippet:
            assert "[Pyvider Config Warning]" in captured.err, \
                f"No Pyvider Config Warning for {env_var}={invalid_value}. Output: {captured.err}"
            assert expected_warning_snippet in captured.err, \
                f"Expected warning snippet '{expected_warning_snippet}' not found for {env_var}={invalid_value}. Output: {captured.err}"

        # Clean up the specific environment variable for the next iteration
        monkeypatch.delenv(env_var, raising=False)


def test_module_levels_parsing_edge_cases() -> None:
    """Tests edge cases in module level parsing."""
    edge_cases = [
        ("", {}),  # Empty string
        ("   ", {}),  # Whitespace only
        ("module1:DEBUG", {"module1": "DEBUG"}),  # Single valid
        ("module1:DEBUG,module2:ERROR", {"module1": "DEBUG", "module2": "ERROR"}),  # Multiple valid
        ("module1:INVALID,module2:DEBUG", {"module2": "DEBUG"}),  # Mix valid/invalid
        ("invalid_format,module2:DEBUG", {"module2": "DEBUG"}),  # Missing colon
        ("module1:,module2:DEBUG", {"module2": "DEBUG"}),  # Empty level
        (":DEBUG,module2:ERROR", {"module2": "ERROR"}),  # Empty module name
        ("module1:DEBUG,,module2:ERROR", {"module1": "DEBUG", "module2": "ERROR"}),  # Empty item
        ("module.with.dots:INFO", {"module.with.dots": "INFO"}),  # Dotted module names
    ]

    for levels_str, expected in edge_cases:
        with patch.dict(os.environ, {"PYVIDER_LOG_MODULE_LEVELS": levels_str}):
            config = TelemetryConfig.from_env()
            assert config.logging.module_levels == expected, f"Failed for: '{levels_str}'"


def test_logger_with_extreme_names(
    setup_pyvider_telemetry_for_test: Callable[[TelemetryConfig | None], None],
    captured_stderr_for_pyvider: io.StringIO,
) -> None:
    """Tests logger behavior with extreme names."""
    setup_pyvider_telemetry_for_test(None)

    extreme_names = [
        "",  # Empty string
        "a" * 1000,  # Very long name
        "name.with.many.dots.and.segments",  # Many segments
        "name-with-dashes",  # Dashes
        "name_with_underscores",  # Underscores
        "name with spaces",  # Spaces
        "🚀🌟🔥",  # Unicode/emoji
        "UPPERCASE.logger",  # Mixed case
        "123.numeric.start",  # Starting with numbers
        "logger.name.ending.with.dot.",  # Ending with dot
        ".starting.with.dot",  # Starting with dot
    ]

    for name in extreme_names:
        try:
            test_logger = logger.get_logger(name)
            test_logger.info(f"Test message from logger: {name[:50]}")  # Truncate for readability
        except Exception as e: # pragma: no cover
            pytest.fail(f"Logger failed with name '{name}': {e}")

    # Verify all messages were logged
    output = captured_stderr_for_pyvider.getvalue()
    lines = [
        line for line in output.strip().splitlines()
        if not line.startswith("[Pyvider Setup]") and line.strip()
    ]
    assert len(lines) == len(extreme_names)


def test_log_message_edge_cases(
    setup_pyvider_telemetry_for_test: Callable[[TelemetryConfig | None], None],
    captured_stderr_for_pyvider: io.StringIO,
) -> None:
    """Tests logging with edge case message content."""
    setup_pyvider_telemetry_for_test(None)
    test_logger = logger.get_logger("edge.test")

    edge_case_messages: list[Any] = [ # Allow Any for diverse test inputs
        "",  # Empty message
        " ",  # Whitespace only
        "\n\t\r",  # Control characters
        "a" * 10000,  # Very long message
        "Message with %s %d formatting",  # Format string without args
        "Null byte: \x00",  # Null byte
        "Unicode: 🚀🌟💫🔥⚡",  # Unicode characters
        "JSON-like: {\"key\": \"value\", \"number\": 123}",  # JSON content
        "HTML-like: <script>alert('test')</script>",  # HTML content
        "Multi\nline\nmessage",  # Multiline
        "Tabs\tand\ttabs",  # Tab characters
        "Binary-like: \x01\x02\x03\x04",  # Binary data
    ]

    for message in edge_case_messages:
        try:
            test_logger.info(message)
        except Exception as e: # pragma: no cover
            pytest.fail(f"Logging failed with message '{str(message)[:50]}...': {e}")

    # Verify output exists
    output = captured_stderr_for_pyvider.getvalue()
    lines = [
        line for line in output.strip().splitlines()
        if not line.startswith("[Pyvider Setup]") and line.strip()
    ]
    assert len(lines) >= len(edge_case_messages)


def test_logger_args_formatting_edge_cases(
    setup_pyvider_telemetry_for_test: Callable[[TelemetryConfig | None], None],
    captured_stderr_for_pyvider: io.StringIO,
) -> None:
    """Tests logger argument formatting edge cases using PyviderLogger's methods."""
    setup_pyvider_telemetry_for_test(None)
    # Using the global logger instance which has the PyviderLogger methods

    test_cases: list[tuple[str, tuple[Any, ...], bool]] = [
        # (message, args, should_not_raise)
        ("Simple message with %s", ("arg1",), True),
        ("Multiple args: %s %d %s", ("str", 42, "end"), True),
        ("Too few args: %s %s", ("only_one",), True), # PyviderLogger's _format_message_with_args handles this
        ("Too many args: %s", ("arg1", "arg2", "extra"), True), # PyviderLogger's _format_message_with_args handles this
        ("Invalid format: %q", ("arg",), True), # PyviderLogger's _format_message_with_args handles this
        ("No format but args", ("arg1", "arg2"), True), # PyviderLogger's _format_message_with_args handles this
        ("Empty args", (), True),
        ("Unicode in args: %s", ("🚀🌟",), True),
        ("None arg: %s", (None,), True),
        ("Complex object: %s", ({"key": "value"},), True),
    ]

    for message, args, should_not_raise in test_cases:
        try:
            # Call info method on the global PyviderLogger instance
            logger.info(message, *args)
            if not should_not_raise: # pragma: no cover
                pytest.fail(f"Expected exception for: {message} with args {args}")
        except Exception as e: # pragma: no cover
            if should_not_raise:
                pytest.fail(f"Unexpected exception for '{message}' with args {args}: {e}")

    output = captured_stderr_for_pyvider.getvalue()
    lines = [
        line for line in output.strip().splitlines()
        if not line.startswith("[Pyvider Setup]") and line.strip()
    ]
    assert len(lines) == len(test_cases), f"Expected {len(test_cases)} log lines, got {len(lines)}"


def test_repeated_setup_calls(
    setup_pyvider_telemetry_for_test: Callable[[TelemetryConfig | None], None],
    captured_stderr_for_pyvider: io.StringIO,
) -> None:
    """Tests behavior with repeated setup calls."""
    config1 = TelemetryConfig(
        service_name="service1",
        logging=LoggingConfig(default_level="DEBUG")
    )
    config2 = TelemetryConfig(
        service_name="service2",
        logging=LoggingConfig(default_level="INFO")
    )

    # First setup
    setup_pyvider_telemetry_for_test(config1)
    logger.info("Message after first setup")

    # Second setup (should reconfigure)
    setup_pyvider_telemetry_for_test(config2)
    logger.info("Message after second setup")
    logger.debug("Debug message (should be filtered in INFO level)")

    output = captured_stderr_for_pyvider.getvalue()

    assert "service1" in output
    assert "service2" in output
    assert "Debug message" not in output


def test_concurrent_setup_calls() -> None:
    """Tests thread safety of setup calls."""
    import threading

    configs = [
        TelemetryConfig(service_name=f"service{i}")
        for i in range(5)
    ]

    setup_results: list[str | None] = []
    exceptions: list[Exception] = []

    def setup_worker(config: TelemetryConfig) -> None:
        try:
            setup_telemetry(config)
            setup_results.append(config.service_name)
        except Exception as e: # pragma: no cover
            exceptions.append(e)

    threads = []
    for config_item in configs:
        thread = threading.Thread(target=setup_worker, args=(config_item,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join(timeout=5.0)

    assert len(exceptions) == 0, f"Concurrent setup failed: {exceptions}"
    assert len(setup_results) == len(configs)
    reset_pyvider_setup_for_testing()


def test_memory_usage_with_large_configs() -> None:
    """Tests memory behavior with large configurations."""
    large_module_levels = {
        f"module.{i}.submodule.{j}": "DEBUG"
        for i in range(100)
        for j in range(10)
    }

    config = TelemetryConfig(
        logging=LoggingConfig(
            default_level="INFO",
            module_levels=large_module_levels, # type: ignore [arg-type]
        )
    )

    try:
        setup_telemetry(config)
        for i in range(0, 100, 10):
            test_logger = logger.get_logger(f"module.{i}.submodule.5")
            test_logger.info(f"Message from module {i}")
    except Exception as e: # pragma: no cover
        pytest.fail(f"Large configuration failed: {e}")
    finally:
        reset_pyvider_setup_for_testing()


def test_trace_level_edge_cases(
    setup_pyvider_telemetry_for_test: Callable[[TelemetryConfig | None], None],
    captured_stderr_for_pyvider: io.StringIO,
) -> None:
    """Tests TRACE level edge cases."""
    config = TelemetryConfig(
        logging=LoggingConfig(
            default_level="TRACE",
            module_levels={"trace.test": "TRACE"},
        )
    )
    setup_pyvider_telemetry_for_test(config)

    logger.trace("Default trace message")
    logger.trace("Named trace message", _pyvider_logger_name="trace.test.custom")
    logger.trace("Trace with args %s %d", "test", 42)
    logger.trace("Trace with kwargs", key1="value1", key2=123)

    output = captured_stderr_for_pyvider.getvalue()
    lines = [
        line for line in output.strip().splitlines()
        if not line.startswith("[Pyvider Setup]") and line.strip()
    ]
    assert len(lines) >= 4, "Not all trace messages were logged"
    trace_count = sum(1 for line in lines if "trace" in line.lower())
    assert trace_count >= 4, "TRACE level not properly handled"


def test_configuration_validation_edge_cases() -> None:
    """Tests configuration validation with edge cases."""
    config_none_service = TelemetryConfig(service_name=None)
    assert config_none_service.service_name is None

    bool_test_cases = [
        ("true", True), ("True", True), ("TRUE", True),
        ("false", False), ("False", False), ("FALSE", False),
        ("1", False), ("0", False), ("yes", False), ("no", False), ("", False),
    ]
    for env_value, expected in bool_test_cases:
        with patch.dict(os.environ, {"PYVIDER_LOG_OMIT_TIMESTAMP": env_value}):
            config = TelemetryConfig.from_env()
            assert config.logging.omit_timestamp == expected, f"Failed for '{env_value}'"


def test_configuration_immutability() -> None:
    """Tests that configuration objects are properly immutable."""
    config_telemetry = TelemetryConfig(service_name="test")
    with pytest.raises(AttributeError):
        config_telemetry.service_name = "modified"  # type: ignore[misc]

    config_logging = LoggingConfig(default_level="INFO")
    with pytest.raises(AttributeError):
        config_logging.default_level = "DEBUG"  # type: ignore[misc]


def test_performance_with_disabled_features(
    setup_pyvider_telemetry_for_test: Callable[[TelemetryConfig | None], None],
    captured_stderr_for_pyvider: io.StringIO,
) -> None:
    """Tests performance when emoji features are disabled."""
    import time
    config = TelemetryConfig(
        logging=LoggingConfig(
            default_level="INFO",
            logger_name_emoji_prefix_enabled=False,
            das_emoji_prefix_enabled=False,
        )
    )
    setup_pyvider_telemetry_for_test(config)
    test_logger = logger.get_logger("performance.test")
    start_time = time.time()
    message_count = 1000
    for i in range(message_count):
        test_logger.info(f"Performance test message {i}", iteration=i)
    end_time = time.time()
    duration = end_time - start_time
    output = captured_stderr_for_pyvider.getvalue()
    lines = [
        line for line in output.strip().splitlines()
        if not line.startswith("[Pyvider Setup]") and line.strip()
    ]
    assert len(lines) == message_count
    messages_per_second = message_count / duration
    assert messages_per_second > 500, f"Performance too slow: {messages_per_second:.1f} msg/sec"

# 🧪⚠️
