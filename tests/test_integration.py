#
# test_integration.py
#
"""
Integration tests for Pyvider Telemetry.

This module contains tests that verify the complete system behavior,
including real-world usage patterns, error conditions, and edge cases.

The integration tests focus on:
- End-to-end functionality verification
- Environment variable configuration
- High-volume performance characteristics
- Thread safety under concurrent load
- Async usage patterns
- Error recovery and resilience
- Configuration edge cases
- Comprehensive emoji matrix coverage

These tests simulate realistic usage scenarios to ensure the telemetry
system behaves correctly in production environments.
"""
import asyncio
from collections.abc import Callable
from concurrent.futures import ThreadPoolExecutor
import io
import json
import os
import time
from typing import Any  # Added for type hints

import pytest

from pyvider.telemetry import (
    LoggingConfig,
    TelemetryConfig,
    logger,
    setup_telemetry,
    shutdown_pyvider_telemetry,
)


def test_full_lifecycle_integration(
    setup_pyvider_telemetry_for_test: Callable[[TelemetryConfig | None], None],
    captured_stderr_for_pyvider: io.StringIO,
) -> None:
    """
    Tests complete setup -> use -> shutdown lifecycle.

    This test verifies that the entire telemetry system lifecycle
    works correctly from initialization through normal usage to shutdown.
    """
    config = TelemetryConfig(
        service_name="integration-test-service",
        logging=LoggingConfig(
            default_level="TRACE",  # Allow TRACE level to pass through
            console_formatter="json",
            logger_name_emoji_prefix_enabled=True,
            das_emoji_prefix_enabled=True,
        ),
    )

    # Setup phase
    setup_pyvider_telemetry_for_test(config)

    # Usage phase - exercise various logging features
    app_logger = logger.get_logger("app.main")
    app_logger.info("Application started", version="1.0.0")
    app_logger.debug("Debug info", component="auth", action="validate", status="success")

    # Test custom TRACE level
    logger.trace("Trace event", _pyvider_logger_name="app.trace", detail="low-level")

    # Test exception logging with traceback
    try:
        raise ValueError("Test exception")
    except ValueError:
        app_logger.exception("Handled error", context="integration_test")

    # Verify output structure and content
    output = captured_stderr_for_pyvider.getvalue()
    lines = [
        line for line in output.strip().splitlines()
        if not line.startswith("[Pyvider Setup]") and line.strip()
    ]

    assert len(lines) >= 4, f"Expected at least 4 log lines, got {len(lines)}"

    # Parse and validate JSON output
    for line in lines:
        try:
            log_data = json.loads(line)

            # Verify required fields are present
            assert "timestamp" in log_data, "Missing timestamp field"
            assert "level" in log_data, "Missing level field"
            assert "event" in log_data, "Missing event field"
            assert "service_name" in log_data, "Missing service_name field"
            assert log_data["service_name"] == "integration-test-service"

        except json.JSONDecodeError as e: # pragma: no cover
            pytest.fail(f"Invalid JSON in log line: {line}. Error: {e}")


def test_environment_variable_integration() -> None:
    """
    Tests configuration loading from environment variables.

    This test verifies that the environment variable configuration
    system works correctly and handles various configuration options.
    """
    # Define test environment variables
    env_vars = {
        "PYVIDER_SERVICE_NAME": "env-test-service",
        "PYVIDER_LOG_LEVEL": "WARNING",
        "PYVIDER_LOG_CONSOLE_FORMATTER": "key_value",
        "PYVIDER_LOG_LOGGER_NAME_EMOJI_ENABLED": "false",
        "PYVIDER_LOG_DAS_EMOJI_ENABLED": "true",
        "PYVIDER_LOG_OMIT_TIMESTAMP": "true",
        "PYVIDER_LOG_MODULE_LEVELS": "app.security:ERROR,app.auth:DEBUG",
    }

    # Save original environment values for restoration
    original_values: dict[str, str | None] = {}
    for key in env_vars:
        original_values[key] = os.environ.get(key)
        os.environ[key] = env_vars[key]

    try:
        # Load configuration from environment
        config = TelemetryConfig.from_env()

        # Verify all configuration values were loaded correctly
        assert config.service_name == "env-test-service"
        assert config.logging.default_level == "WARNING"
        assert config.logging.console_formatter == "key_value"
        assert config.logging.logger_name_emoji_prefix_enabled is False
        assert config.logging.das_emoji_prefix_enabled is True
        assert config.logging.omit_timestamp is True
        assert config.logging.module_levels == {
            "app.security": "ERROR",
            "app.auth": "DEBUG",
        }

    finally:
        # Restore original environment state
        for key, original_value in original_values.items():
            if original_value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = original_value


def test_high_volume_logging_performance(
    setup_pyvider_telemetry_for_test: Callable[[TelemetryConfig | None], None],
    captured_stderr_for_pyvider: io.StringIO,
) -> None:
    """
    Tests performance with high-volume logging.

    This test ensures that the logging system can handle high throughput
    scenarios without significant performance degradation.
    """
    config = TelemetryConfig(
        logging=LoggingConfig(
            default_level="INFO",
            console_formatter="json",
            logger_name_emoji_prefix_enabled=True,
            das_emoji_prefix_enabled=False,
        )
    )
    setup_pyvider_telemetry_for_test(config)

    test_logger = logger.get_logger("perf.test")

    # Perform high-volume logging with timing
    start_time = time.time()
    message_count = 1000

    for i in range(message_count):
        test_logger.info(f"Performance test message {i}", iteration=i)

    end_time = time.time()
    duration = end_time - start_time

    # Verify all messages were logged
    output = captured_stderr_for_pyvider.getvalue()
    lines = [
        line for line in output.strip().splitlines()
        if not line.startswith("[Pyvider Setup]") and line.strip()
    ]

    assert len(lines) == message_count, f"Expected {message_count} lines, got {len(lines)}"

    # Performance assertion - should achieve reasonable throughput
    messages_per_second = message_count / duration
    assert messages_per_second > 500, f"Too slow: {messages_per_second:.1f} msg/sec"


def test_thread_safety_concurrent_logging(
    setup_pyvider_telemetry_for_test: Callable[[TelemetryConfig | None], None],
    captured_stderr_for_pyvider: io.StringIO,
) -> None:
    """
    Tests thread safety with concurrent logging from multiple threads.

    This test verifies that the logging system maintains correctness
    and performance under concurrent access patterns.
    """
    config = TelemetryConfig(
        logging=LoggingConfig(
            default_level="INFO",
            console_formatter="json",
        )
    )
    setup_pyvider_telemetry_for_test(config)

    def worker_thread(thread_id: int, message_count: int) -> None:
        """Worker function for concurrent logging test."""
        thread_logger = logger.get_logger(f"thread.{thread_id}")
        for i in range(message_count):
            thread_logger.info(
                f"Thread {thread_id} message {i}",
                thread_id=thread_id,
                msg_id=i
            )

    # Launch multiple concurrent threads
    thread_count = 5
    messages_per_thread = 100

    with ThreadPoolExecutor(max_workers=thread_count) as executor:
        futures = [
            executor.submit(worker_thread, thread_id, messages_per_thread)
            for thread_id in range(thread_count)
        ]

        # Wait for all threads to complete
        for future in futures:
            future.result()

    # Verify output correctness
    output = captured_stderr_for_pyvider.getvalue()
    lines = [
        line for line in output.strip().splitlines()
        if not line.startswith("[Pyvider Setup]") and line.strip()
    ]

    expected_messages = thread_count * messages_per_thread
    assert len(lines) == expected_messages, f"Expected {expected_messages} lines, got {len(lines)}"

    # Verify all messages are valid JSON and count per thread
    thread_message_counts: dict[int, int] = {}
    for line in lines:
        try:
            log_data = json.loads(line)
            thread_id = log_data.get("thread_id")
            if thread_id is not None:
                thread_message_counts[thread_id] = thread_message_counts.get(thread_id, 0) + 1
        except json.JSONDecodeError as e: # pragma: no cover
            pytest.fail(f"Invalid JSON in concurrent log line: {line}. Error: {e}")

    # Verify each thread logged the expected number of messages
    for thread_id_val in range(thread_count):
        actual_count = thread_message_counts.get(thread_id_val, 0)
        assert actual_count == messages_per_thread, \
            f"Thread {thread_id_val} logged {actual_count} messages, expected {messages_per_thread}"


@pytest.mark.asyncio
async def test_async_usage_patterns() -> None:
    """
    Tests usage patterns in async contexts.

    This test ensures that the logging system works correctly within
    async/await contexts and doesn't interfere with event loop performance.
    """
    config = TelemetryConfig(
        logging=LoggingConfig(
            default_level="DEBUG",
            console_formatter="key_value",
        )
    )

    # Setup in async context
    setup_telemetry(config)

    # Use logger in async context
    async_logger = logger.get_logger("async.test")
    async_logger.info("Async function started")

    # Simulate async work with logging
    await asyncio.sleep(0.01)
    async_logger.debug("Async work in progress")

    # Test async shutdown functionality
    await shutdown_pyvider_telemetry()

    # Logging should still work after shutdown call
    async_logger.info("After shutdown call")


def test_error_recovery_and_resilience(
    setup_pyvider_telemetry_for_test: Callable[[TelemetryConfig | None], None],
    captured_stderr_for_pyvider: io.StringIO,
) -> None:
    """
    Tests error recovery and system resilience.

    This test verifies that the logging system handles various edge cases
    and problematic inputs gracefully without crashing.
    """
    # Configure with valid settings
    config = TelemetryConfig(
        logging=LoggingConfig(
            default_level="INFO",
            module_levels={"app.test": "DEBUG"},  # Valid configuration
        )
    )
    setup_pyvider_telemetry_for_test(config)

    test_logger = logger.get_logger("app.test")

    # Test logging with various problematic inputs
    test_cases: list[tuple[str, dict[str, Any]]] = [
        ("Normal message", {}),
        ("Message with None value", {"value": None}),
        ("Message with large data", {"data": "x" * 10000}),
        ("Message with special characters", {"text": "Hello\n\t\r\x00World"}),
        ("Message with unicode", {"unicode": "🚀🌟💫"}),
        ("Message with complex nested data", {
            "nested": {"level1": {"level2": {"data": ["item1", "item2"]}}}
        }),
    ]

    for message, kwargs in test_cases:
        try:
            test_logger.info(message, **kwargs)
        except Exception as e: # pragma: no cover
            pytest.fail(f"Logger failed with message '{message}': {e}")

    # Verify output exists and is valid
    output = captured_stderr_for_pyvider.getvalue()
    lines = [
        line for line in output.strip().splitlines()
        if not line.startswith("[Pyvider Setup]") and line.strip()
    ]

    assert len(lines) >= len(test_cases), "Not all test messages were logged"


def test_configuration_edge_cases() -> None:
    """
    Tests edge cases in configuration handling.

    This test verifies that configuration objects behave correctly
    in various edge cases and maintain their immutability guarantees.
    """
    # Test with minimal configuration
    minimal_config = TelemetryConfig()
    assert minimal_config.service_name is None
    assert minimal_config.logging.default_level == "DEBUG"
    assert minimal_config.globally_disabled is False

    # Test with disabled telemetry
    disabled_config = TelemetryConfig(globally_disabled=True)
    setup_telemetry(disabled_config)

    # Should not raise errors even when disabled
    logger.info("This should be suppressed")
    logger.error("This should also be suppressed")

    # Test configuration immutability (attrs frozen=True)
    config_immut = TelemetryConfig(service_name="test")
    with pytest.raises(AttributeError):
        config_immut.service_name = "modified"  # type: ignore[misc]


def test_repeated_setup_calls_integration( # Renamed to avoid conflict
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


def test_emoji_matrix_comprehensive_coverage(
    setup_pyvider_telemetry_for_test: Callable[[TelemetryConfig | None], None],
    captured_stderr_for_pyvider: io.StringIO,
) -> None:
    """
    Tests comprehensive emoji matrix coverage.

    This test verifies that the Domain-Action-Status emoji system
    works correctly with various combinations of semantic fields.
    """
    config = TelemetryConfig(
        logging=LoggingConfig(
            default_level="INFO",
            console_formatter="key_value",
            logger_name_emoji_prefix_enabled=True,
            das_emoji_prefix_enabled=True,
        )
    )
    setup_pyvider_telemetry_for_test(config)

    # Test various domain/action/status combinations
    test_combinations = [
        ("auth", "login", "success"),
        ("database", "query", "error"),
        ("network", "connect", "timeout"),
        ("system", "init", "complete"),
        ("unknown_domain", "unknown_action", "unknown_status"),  # Should use defaults
    ]

    test_logger = logger.get_logger("emoji.test")

    for domain, action, status in test_combinations:
        test_logger.info(
            f"Test message for {domain}-{action}-{status}",
            domain=domain,
            action=action,
            status=status,
        )

    # Verify output contains expected emoji prefixes
    output = captured_stderr_for_pyvider.getvalue()

    # Check for specific emoji combinations
    assert "[🔑][➡️][✅]" in output  # auth-login-success
    assert "[🗄️][🔍][🔥]" in output  # database-query-error
    assert "[🌐][🔗][⏱️]" in output  # network-connect-timeout
    assert "[⚙️][🌱][🏁]" in output  # system-init-complete
    # Expectation for unknown defaults, now action should be ❓ (default) consistent with other tests.
    assert "[❓][❓][➡️]" in output  # unknown defaults: domain=❓, action=❓, status=➡️


def test_module_level_filtering_comprehensive(
    setup_pyvider_telemetry_for_test: Callable[[TelemetryConfig | None], None],
    captured_stderr_for_pyvider: io.StringIO,
) -> None:
    """
    Tests comprehensive module-level filtering with hierarchical overrides.

    This test verifies that module-specific log levels work correctly
    with hierarchical module names and proper inheritance behavior.
    """
    config = TelemetryConfig(
        logging=LoggingConfig(
            default_level="WARNING",  # High threshold by default
            module_levels={
                "app": "INFO",
                "app.auth": "DEBUG",
                "app.auth.oauth": "TRACE",
                "external": "ERROR",
            },
            logger_name_emoji_prefix_enabled=False,
            das_emoji_prefix_enabled=False,
        )
    )
    setup_pyvider_telemetry_for_test(config)

    loggers_map = {
        "root": logger.get_logger("root.component"),
        "app": logger.get_logger("app.component"),
        "app_auth": logger.get_logger("app.auth.service"),
        "app_auth_oauth": logger.get_logger("app.auth.oauth.handler"),
        "external": logger.get_logger("external.service"),
    }

    test_cases = [
        ("root", "debug", "Root debug message", False),
        ("root", "warning", "Root warning message", True),
        ("app", "debug", "App debug message", False),
        ("app", "info", "App info message", True),
        ("app_auth", "debug", "Auth debug message", True),
        ("app_auth_oauth", "trace", "OAuth trace message", True),
        ("external", "warning", "External warning", False),
        ("external", "error", "External error", True),
    ]

    for logger_key, level, message, _should_appear_in_loop_unpacking in test_cases:
        test_logger_instance = loggers_map[logger_key]
        log_method = getattr(test_logger_instance, level)

        if level == "trace":
            # Special handling for custom TRACE level
            # Ensure the logger_name from the bound logger is used
            logger.trace(message, _pyvider_logger_name=test_logger_instance._context.get("logger_name"))
        else:
            log_method(message)

    output = captured_stderr_for_pyvider.getvalue()
    filtered_lines = [
        line for line in output.strip().splitlines()
        if not line.startswith("[Pyvider Setup]") and line.strip()
    ]

    expected_messages_count = sum(1 for _, _, _, tc_should_appear in test_cases if tc_should_appear)
    actual_messages_count = len(filtered_lines)

    assert actual_messages_count == expected_messages_count, \
        f"Expected {expected_messages_count} messages, got {actual_messages_count}. Output:\n{output}"

    for _, _, message_text, tc_should_appear_for_assertion in test_cases:
        message_found = any(message_text in line for line in filtered_lines)
        if tc_should_appear_for_assertion:
            assert message_found, f"Expected message '{message_text}' not found in output. Output:\n{output}"
        else:
            assert not message_found, f"Unexpected message '{message_text}' found in output. Output:\n{output}"

# 🧪🔄
