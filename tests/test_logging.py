#
# test_logging.py
#
"""
Tests for the Pyvider Telemetry logging system.

This module contains a comprehensive suite of pytest tests to verify the
functionality of the `pyvider.telemetry` logging library. It covers
various aspects including log levels, formatters (JSON and key-value),
emoji prefixes, exception logging, service name injection, global disablement,
module-specific log level overrides, and timestamp handling.

The test suite is designed to ensure:
- Core logging functionality works correctly
- Configuration options behave as expected
- Output formatting is consistent and parseable
- Error conditions are handled gracefully
- Performance characteristics meet requirements
"""
from collections.abc import Callable
import io
import json
import re
from typing import Any  # Added List, Tuple for expected_warning_parts

import pytest
from pytest import CaptureFixture, MonkeyPatch  # Added
import structlog  # E402: Moved to top

from pyvider.telemetry import (
    LoggingConfig,
    TelemetryConfig,
    logger as pyvider_logger_instance,
)
from pyvider.telemetry.logger.base import PyviderLogger  # E402: Moved to top
from pyvider.telemetry.types import TRACE_LEVEL_NAME  # Corrected import

# TRACE_LEVEL_NAME is already imported from custom_processors; this one was redundant
# from pyvider.telemetry.types import TRACE_LEVEL_NAME # For testing trace level


def _filter_application_logs(output: str) -> list[str]:
    """
    Filter out setup messages and return only application log lines.

    Args:
        output: Raw captured log output.

    Returns:
        List of application log lines with setup messages filtered out.
    """
    return [
        line for line in output.strip().splitlines()
        if not line.startswith("[Pyvider Setup]") and line.strip()
    ]


def _validate_json_log_line(  # noqa: C901
    line: str,
    expected_level: str,
    expected_message: str,
    expected_kvs: dict[str, Any] | None = None,
    expect_timestamp: bool = True
) -> bool:
    """
    Validate a single JSON log line against expected criteria.

    Args:
        line: JSON log line to validate.
        expected_level: Expected log level.
        expected_message: Expected log message.
        expected_kvs: Expected key-value pairs.
        expect_timestamp: Whether to expect a timestamp.

    Returns:
        True if the line matches all criteria, False otherwise.
    """
    try:
        log_json = json.loads(line)

        # Check timestamp expectation
        if expect_timestamp:
            if "timestamp" not in log_json:
                return False
            if not re.match(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{6}", log_json["timestamp"]):
                return False
        else:
            if "timestamp" in log_json:
                return False

        # Check level and message
        if log_json.get("level") != expected_level.lower():
            return False
        if log_json.get("event") != expected_message:
            return False

        # Check key-value pairs
        if expected_kvs:
            for k, v_expected in expected_kvs.items():
                if log_json.get(k) != v_expected:
                    return False

        return True

    except json.JSONDecodeError:
        return False


def _validate_keyvalue_log_line(
    line: str,
    expected_level: str,
    expected_message: str,
    expected_kvs: dict[str, Any] | None = None,
    expect_timestamp: bool = True
) -> bool:
    """
    Validate a single key-value log line against expected criteria.

    Args:
        line: Key-value log line to validate.
        expected_level: Expected log level.
        expected_message: Expected log message.
        expected_kvs: Expected key-value pairs.
        expect_timestamp: Whether to expect a timestamp.

    Returns:
        True if the line matches all criteria, False otherwise.
    """
    # Check timestamp expectation
    has_timestamp = re.match(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{6}", line)
    if expect_timestamp and not has_timestamp:
        return False
    if not expect_timestamp and has_timestamp:
        return False

    # Check level
    if not re.search(rf"\[\s*{re.escape(expected_level)}\s*\]", line, re.IGNORECASE):
        return False

    # Check message
    if expected_message not in line:
        return False

    # Check key-value pairs
    if expected_kvs:
        for k, v_expected in expected_kvs.items():
            val_str = str(v_expected) if not isinstance(v_expected, bool) else str(v_expected).lower()
            expected_kv_substring = f"{k}={val_str}"
            if expected_kv_substring not in line:
                return False

    return True


def _check_traceback_presence(output: str, expected_traceback: str) -> bool:
    """
    Check if expected traceback content is present in output.

    Args:
        output: Full log output to search.
        expected_traceback: Expected traceback content.

    Returns:
        True if traceback is found, False otherwise.
    """
    return (
        "Traceback (most recent call last):" in output and
        expected_traceback in output
    )


def assert_log_output(  # noqa: C901
    output: str,
    expected_level: str,
    expected_message_core: str,
    expected_kvs: dict[str, Any] | None = None,
    is_json: bool = False,
    expect_traceback_containing: str | None = None,
    expect_timestamp: bool = True
) -> None:
    """
    Asserts that the captured log output matches the expected criteria.

    This function validates log output format, content, and structure
    against expected values. It handles both JSON and key-value formats.

    Args:
        output: The captured log output string.
        expected_level: The expected log level string (e.g., "info", "error").
        expected_message_core: The core message expected in the log event.
        expected_kvs: Optional dictionary of key-value pairs expected in the log.
        is_json: True if the log output is expected to be in JSON format.
        expect_traceback_containing: Optional string that must be present in the traceback.
        expect_timestamp: If True (default), expects a timestamp. If False, expects no timestamp.

    Raises:
        AssertionError: If the log output doesn't match expected criteria.
    """
    actual_log_lines = _filter_application_logs(output)

    # Handle expected empty output case
    is_expecting_empty_app_log = (
        expected_level == "" and
        expected_message_core == "" and
        expected_kvs is None and
        not expect_traceback_containing
    )

    if is_expecting_empty_app_log:
        if not actual_log_lines:
            return  # Success - no logs as expected
        else:
            details = "\nExpected no application log lines, but found some."
            filtered_output = "\n".join(actual_log_lines)
            raise AssertionError(
                f"Expected no application log output, but found lines.{details}\n"
                f"Filtered Output:\n{filtered_output}\nFull Raw Output:\n{output}"
            )

    # Ensure we have log lines to check
    if not actual_log_lines:
        details = _build_error_details(expected_level, expected_message_core, expected_kvs)
        raise AssertionError(
            f"No application log lines found to match expectations.{details}\n"
            f"Full Raw Output:\n{output}"
        )

    # Check each line for a match
    found_match = False
    debug_info = None

    for line_str in actual_log_lines:
        if is_json:
            line_matches = _validate_json_log_line(
                line_str, expected_level, expected_message_core, expected_kvs, expect_timestamp
            )
            if not debug_info and not line_matches:
                try:
                    debug_info = json.loads(line_str)
                except json.JSONDecodeError:
                    debug_info = f"Invalid JSON: {line_str[:100]}..."
        else:
            line_matches = _validate_keyvalue_log_line(
                line_str, expected_level, expected_message_core, expected_kvs, expect_timestamp
            )
            if not debug_info and not line_matches:
                debug_info = f"Key-value line: {line_str[:100]}..."

        if line_matches:
            found_match = True
            break

    # Check traceback if required
    if expect_traceback_containing and not _check_traceback_presence(output, expect_traceback_containing):
        found_match = False

    # Build detailed error message if no match found
    if not found_match:
        details = _build_error_details(expected_level, expected_message_core, expected_kvs)
        if expect_traceback_containing:
            details += f"\nExpected Traceback: '{expect_traceback_containing}'"
        details += f"\nTimestamp Expected: {expect_timestamp}"

        if debug_info:
            if is_json and isinstance(debug_info, dict):
                details += f"\nLast Parsed JSON Line (for debugging):\n{json.dumps(debug_info, indent=2)}"
            else:
                details += f"\nFirst Actual Log Line (for debugging):\n{debug_info}"

        filtered_output = "\n".join(actual_log_lines)
        raise AssertionError(
            f"Log line not found or format incorrect.{details}\n"
            f"Full Output (filtered application logs):\n{filtered_output}\n"
            f"Full Raw Output (including setup):\n{output}"
        )


def _build_error_details(
    expected_level: str,
    expected_message: str,
    expected_kvs: dict[str, Any] | None
) -> str:
    """
    Build detailed error information for assertion failures.

    Args:
        expected_level: Expected log level.
        expected_message: Expected log message.
        expected_kvs: Expected key-value pairs.

    Returns:
        Formatted error details string.
    """
    details = f"\nExpected Level: '{expected_level}'"
    details += f"\nExpected Message: '{expected_message}'"
    if expected_kvs:
        details += f"\nExpected KVs: {expected_kvs}"
    return details


def test_pyvider_logger_manager_get_logger_basic(
    setup_pyvider_telemetry_for_test: Callable[[TelemetryConfig | None], None],
    captured_stderr_for_pyvider: io.StringIO
) -> None:
    """Tests basic logging via a logger obtained from `get_logger()`."""
    # Ensure key-value formatting for this test
    config = TelemetryConfig(logging=LoggingConfig(console_formatter="key_value"))
    setup_pyvider_telemetry_for_test(config)
    test_logger = pyvider_logger_instance.get_logger("test.basic")
    test_logger.info("Basic test message from get_logger.")
    output = captured_stderr_for_pyvider.getvalue()
    assert_log_output(output, "info", "🧪 Basic test message from get_logger.")


def test_pyvider_logger_direct_methods(
    setup_pyvider_telemetry_for_test: Callable[[TelemetryConfig | None], None],
    captured_stderr_for_pyvider: io.StringIO
) -> None:
    """Tests direct logging methods on the global `pyvider_logger_instance`."""
    # Explicitly set log level to DEBUG for this test to ensure debug messages are captured.
    config = TelemetryConfig(logging=LoggingConfig(default_level="DEBUG"))
    setup_pyvider_telemetry_for_test(config)
    pyvider_logger_instance.info("Direct info message.")
    pyvider_logger_instance.debug("Direct debug message.")
    output = captured_stderr_for_pyvider.getvalue()  # Capture output once after all logs
    assert_log_output(output, "info", "🗣️ Direct info message.")
    assert_log_output(output, "debug", "🗣️ Direct debug message.") # Assert against the same output


@pytest.mark.parametrize("formatter_type_name", ["key_value", "json"])
def test_log_formatters_via_config(
    formatter_type_name: str,
    setup_pyvider_telemetry_for_test: Callable[[TelemetryConfig | None], None],
    captured_stderr_for_pyvider: io.StringIO
) -> None:
    """Tests key_value and json formatters configured via TelemetryConfig."""
    cfg = TelemetryConfig(
        logging=LoggingConfig(
            default_level="INFO",
            console_formatter=formatter_type_name,
            logger_name_emoji_prefix_enabled=False,
            das_emoji_prefix_enabled=False
        )
    )
    setup_pyvider_telemetry_for_test(cfg)

    msg = f"Message with {formatter_type_name} formatter."
    logger_name_val = "formatter.test"
    extra_kvs: dict[str, Any] = {"field1": "data1", "field2": 200}
    pyvider_logger_instance.get_logger(logger_name_val).info(msg, **extra_kvs)
    output = captured_stderr_for_pyvider.getvalue()

    expected_kvs_for_output: dict[str, Any] = {**extra_kvs}
    if formatter_type_name == "json":
        expected_kvs_for_output["logger_name"] = logger_name_val

    assert_log_output(
        output, "info", msg,
        expected_kvs=expected_kvs_for_output,
        is_json=(formatter_type_name == "json")
    )

    if formatter_type_name == "key_value":
        actual_log_lines = _filter_application_logs(output)
        if actual_log_lines:
            assert f"logger_name={logger_name_val}" not in actual_log_lines[0], \
                f"KV output should NOT contain 'logger_name={logger_name_val}' as it's popped"


def test_globally_disable_telemetry_impacts_logging(
    setup_pyvider_telemetry_for_test: Callable[[TelemetryConfig | None], None],
    captured_stderr_for_pyvider: io.StringIO
) -> None:
    """Tests that logging is disabled when `globally_disabled` is True."""
    cfg = TelemetryConfig(globally_disabled=True)
    setup_pyvider_telemetry_for_test(cfg)
    pyvider_logger_instance.info("This should not be logged.")
    output = captured_stderr_for_pyvider.getvalue()
    assert_log_output(output, "", "", expected_kvs=None, is_json=False, expect_timestamp=False)


def test_module_specific_log_levels(
    setup_pyvider_telemetry_for_test: Callable[[TelemetryConfig | None], None],
    captured_stderr_for_pyvider: io.StringIO
) -> None:
    """Tests module-specific log level overrides."""
    cfg = TelemetryConfig(
        logging=LoggingConfig(
            default_level="INFO",
            module_levels={
                "service.alpha": "DEBUG",
                "service.beta": "WARNING",
                "service.beta.child": "ERROR",
                "service.gamma.trace_enabled": TRACE_LEVEL_NAME
            },
            logger_name_emoji_prefix_enabled=True
        )
    )
    setup_pyvider_telemetry_for_test(cfg)

    pyvider_logger_instance.trace("Alpha trace msg (filtered by alpha's DEBUG)", _pyvider_logger_name="service.alpha")
    pyvider_logger_instance.get_logger("service.alpha").debug("Alpha debug msg (shown)")
    pyvider_logger_instance.get_logger("service.beta").debug("Beta debug msg (filtered)")
    pyvider_logger_instance.get_logger("service.beta").info("Beta info msg (filtered)")
    pyvider_logger_instance.get_logger("service.beta").warning("Beta warning msg (shown)")
    pyvider_logger_instance.get_logger("service.beta.child").info("BetaChild info msg (filtered)")
    pyvider_logger_instance.get_logger("service.beta.child").warning("BetaChild warning msg (filtered)")
    pyvider_logger_instance.get_logger("service.beta.child").error("BetaChild error msg (shown)")
    pyvider_logger_instance.trace("Gamma trace msg (shown)", _pyvider_logger_name="service.gamma.trace_enabled")
    pyvider_logger_instance.get_logger("service.delta").info("Delta info msg (shown - default INFO)")
    pyvider_logger_instance.get_logger("service.delta").debug("Delta debug msg (filtered - default INFO)")

    output = captured_stderr_for_pyvider.getvalue()
    assert_log_output(output, "debug", "🇦 Alpha debug msg (shown)")
    assert_log_output(output, "warning", "🇧 Beta warning msg (shown)")
    assert_log_output(output, "error", "👶 BetaChild error msg (shown)")
    assert_log_output(output, TRACE_LEVEL_NAME.lower(), "🇬 Gamma trace msg (shown)")
    assert_log_output(output, "info", "🇩 Delta info msg (shown - default INFO)")

    filtered_output_app_logs = "\n".join(_filter_application_logs(output))
    assert "Alpha trace msg" not in filtered_output_app_logs
    assert "Beta debug msg" not in filtered_output_app_logs
    assert "Beta info msg" not in filtered_output_app_logs
    assert "BetaChild info msg" not in filtered_output_app_logs
    assert "BetaChild warning msg" not in filtered_output_app_logs
    assert "Delta debug msg" not in filtered_output_app_logs


def test_logger_name_emoji_prefix_processor(
    setup_pyvider_telemetry_for_test: Callable[[TelemetryConfig | None], None],
    captured_stderr_for_pyvider: io.StringIO
) -> None:
    """Tests the logger name emoji prefix processor."""
    cfg = TelemetryConfig(
        logging=LoggingConfig(
            default_level="DEBUG",
            logger_name_emoji_prefix_enabled=True,
            das_emoji_prefix_enabled=False
        )
    )
    setup_pyvider_telemetry_for_test(cfg)
    pyvider_logger_instance.get_logger("pyvider.telemetry.core.test").info("Core test message")
    pyvider_logger_instance.get_logger("unknown.module.test").debug("Default emoji test")
    pyvider_logger_instance.info("Dynamic call info")
    output = captured_stderr_for_pyvider.getvalue()
    assert_log_output(output, "info", "⚙️ Core test message")
    assert_log_output(output, "debug", "❓ Default emoji test")
    assert_log_output(output, "info", "🗣️ Dynamic call info")


def test_das_emoji_prefix_processor(
    setup_pyvider_telemetry_for_test: Callable[[TelemetryConfig | None], None],
    captured_stderr_for_pyvider: io.StringIO
) -> None:
    """Tests the Domain-Action-Status (DAS) emoji prefix processor."""
    cfg = TelemetryConfig(
        logging=LoggingConfig(
            default_level="INFO",
            logger_name_emoji_prefix_enabled=False,
            das_emoji_prefix_enabled=True
        )
    )
    setup_pyvider_telemetry_for_test(cfg)
    pyvider_logger_instance.get_logger("das.test").info(
        "DAS message", domain="auth", action="login", status="success"
    )
    output = captured_stderr_for_pyvider.getvalue()
    assert_log_output(output, "info", "[🔑][➡️][✅] DAS message")


# Test data for combined emoji and formatter testing
COMBINED_EMOJI_TEST_CASES: list[tuple[bool, bool, str, str | None, str | None, str | None, str, str, str, dict[str, Any]]] = [
    (True, False, "pyvider.telemetry.core", None, None, None, "Core msg", "⚙️ Core msg", "⚙️ Core msg", {"logger_name": "pyvider.telemetry.core"}),
    (False, True, "any.logger", "auth", "login", "success", "Auth msg", "[🔑][➡️][✅] Auth msg", "[🔑][➡️][✅] Auth msg", {"logger_name": "any.logger"}),
    (True, True, "pyvider.telemetry.logger", "file", "read", "warning", "Log read warning", "[📄][📖][⚠️] 📝 Log read warning", "[📄][📖][⚠️] 📝 Log read warning", {"logger_name": "pyvider.telemetry.logger"}),
    (True, True, "unknown", "task", "execute", "failure", "Task failed", "[🔄][▶️][❌] ❓ Task failed", "[🔄][▶️][❌] ❓ Task failed", {"logger_name": "unknown"}),
    (False, False, "simple", None, None, None, "Simple message", "Simple message", "Simple message", {"logger_name": "simple"}),
]


@pytest.mark.parametrize(
    "ln_emoji_enabled, das_emoji_enabled, logger_name, domain, action, status, msg, expected_kv_msg, expected_json_msg, json_kvs_param",
    COMBINED_EMOJI_TEST_CASES
)
def test_combined_emoji_prefixes_and_formatters(
    setup_pyvider_telemetry_for_test: Callable[[TelemetryConfig | None], None],
    captured_stderr_for_pyvider: io.StringIO,
    ln_emoji_enabled: bool,
    das_emoji_enabled: bool,
    logger_name: str,
    domain: str | None,
    action: str | None,
    status: str | None,
    msg: str,
    expected_kv_msg: str,
    expected_json_msg: str,
    json_kvs_param: dict[str, Any]
) -> None:
    """Tests combinations of logger name and DAS emojis with both formatters."""
    log_call_kwargs: dict[str, Any] = {}
    if domain:
        log_call_kwargs["domain"] = domain
    if action:
        log_call_kwargs["action"] = action
    if status:
        log_call_kwargs["status"] = status

    cfg_kv = TelemetryConfig(
        logging=LoggingConfig(
            default_level="INFO",
            console_formatter="key_value",
            logger_name_emoji_prefix_enabled=ln_emoji_enabled,
            das_emoji_prefix_enabled=das_emoji_enabled
        )
    )
    setup_pyvider_telemetry_for_test(cfg_kv)
    pyvider_logger_instance.get_logger(logger_name).info(msg, **log_call_kwargs)
    output_kv = captured_stderr_for_pyvider.getvalue()
    assert_log_output(output_kv, "info", expected_kv_msg, expected_kvs=None, is_json=False)

    captured_stderr_for_pyvider.truncate(0)
    captured_stderr_for_pyvider.seek(0)
    cfg_json = TelemetryConfig(
        logging=LoggingConfig(
            default_level="INFO",
            console_formatter="json",
            logger_name_emoji_prefix_enabled=ln_emoji_enabled,
            das_emoji_prefix_enabled=das_emoji_enabled
        )
    )
    setup_pyvider_telemetry_for_test(cfg_json)
    pyvider_logger_instance.get_logger(logger_name).info(msg, **log_call_kwargs)
    output_json = captured_stderr_for_pyvider.getvalue()
    assert_log_output(output_json, "info", expected_json_msg, expected_kvs=json_kvs_param, is_json=True)


def test_exception_logging(
    setup_pyvider_telemetry_for_test: Callable[[TelemetryConfig | None], None],
    captured_stderr_for_pyvider: io.StringIO
) -> None:
    """Tests logging of exceptions with tracebacks."""
    # Ensure key-value formatting for the first part of this test
    config_kv = TelemetryConfig(logging=LoggingConfig(console_formatter="key_value"))
    setup_pyvider_telemetry_for_test(config_kv)
    try:
        raise ValueError("Test exception for logging")
    except ValueError:
        pyvider_logger_instance.exception("An error occurred")
    output = captured_stderr_for_pyvider.getvalue()
    assert_log_output(
        output, "error", "🗣️ An error occurred",
        expect_traceback_containing="ValueError: Test exception for logging"
    )

    captured_stderr_for_pyvider.truncate(0)
    captured_stderr_for_pyvider.seek(0)
    cfg_json = TelemetryConfig(
        logging=LoggingConfig(
            console_formatter="json",
            default_level="DEBUG",
            logger_name_emoji_prefix_enabled=False
        )
    )
    setup_pyvider_telemetry_for_test(cfg_json)
    try:
        raise RuntimeError("JSON exception test")
    except RuntimeError:
        pyvider_logger_instance.get_logger("json.exc.test").exception("JSON error event")
    output_json = captured_stderr_for_pyvider.getvalue()
    assert_log_output(
        output_json, "error", "JSON error event",
        expected_kvs={"logger_name": "json.exc.test"},
        is_json=True,
        expect_traceback_containing="RuntimeError: JSON exception test"
    )


def test_service_name_in_logs(
    setup_pyvider_telemetry_for_test: Callable[[TelemetryConfig | None], None],
    captured_stderr_for_pyvider: io.StringIO
) -> None:
    """Tests that `service_name` from config appears in logs."""
    service_name = "MyTestService"
    cfg_kv = TelemetryConfig(
        service_name=service_name,
        logging=LoggingConfig(
            console_formatter="key_value",
            logger_name_emoji_prefix_enabled=True
        )
    )
    setup_pyvider_telemetry_for_test(cfg_kv)
    pyvider_logger_instance.get_logger("service.name.test").info("KV service log")
    output_kv = captured_stderr_for_pyvider.getvalue()
    assert_log_output(output_kv, "info", "📛 KV service log", expected_kvs={"service_name": service_name})

    captured_stderr_for_pyvider.truncate(0)
    captured_stderr_for_pyvider.seek(0)
    cfg_json = TelemetryConfig(
        service_name=service_name,
        logging=LoggingConfig(
            console_formatter="json",
            logger_name_emoji_prefix_enabled=False
        )
    )
    setup_pyvider_telemetry_for_test(cfg_json)
    pyvider_logger_instance.get_logger("service.name.test").info("JSON service log")
    output_json = captured_stderr_for_pyvider.getvalue()
    assert_log_output(
        output_json, "info", "JSON service log",
        expected_kvs={"logger_name": "service.name.test", "service_name": service_name},
        is_json=True
    )


@pytest.mark.parametrize("formatter_type_name", ["key_value", "json"])
def test_log_format_omit_timestamp(
    formatter_type_name: str,
    setup_pyvider_telemetry_for_test: Callable[[TelemetryConfig | None], None],
    captured_stderr_for_pyvider: io.StringIO,
) -> None:
    """Tests the omit_timestamp configuration for both formatters."""
    cfg = TelemetryConfig(
        logging=LoggingConfig(
            default_level="INFO",
            console_formatter=formatter_type_name,
            omit_timestamp=True,
            logger_name_emoji_prefix_enabled=False,
            das_emoji_prefix_enabled=False
        )
    )
    setup_pyvider_telemetry_for_test(cfg)

    logger_name_val = "timestamp.test"
    msg = "Message without timestamp."
    extra_kvs: dict[str, Any] = {"data": 123}

    pyvider_logger_instance.get_logger(logger_name_val).info(msg, **extra_kvs)
    output = captured_stderr_for_pyvider.getvalue()

    actual_log_lines = _filter_application_logs(output)
    assert len(actual_log_lines) == 1, "Expected exactly one application log line"
    log_line = actual_log_lines[0]

    timestamp_pattern = r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{6}"
    if formatter_type_name == "key_value":
        assert not re.match(timestamp_pattern, log_line), \
            f"Timestamp was unexpectedly present at start of KV log line: {log_line}"

    expected_kvs_for_output: dict[str, Any] = {**extra_kvs}
    if formatter_type_name == "json":
        expected_kvs_for_output["logger_name"] = logger_name_val

    assert_log_output(
        output, "info", msg,
        expected_kvs=expected_kvs_for_output,
        is_json=(formatter_type_name == "json"),
        expect_timestamp=False
    )

# 🧪📊

# Tests for configuration warnings
# These tests use capsys to capture stderr, as the config warnings logger
# writes directly to sys.stderr via its own stdlib_logging.StreamHandler.
# The `captured_stderr_for_pyvider` fixture captures the structlog output stream,
# which is distinct.

class TestConfigWarnings:
    """Tests for warnings generated during TelemetryConfig.from_env() parsing."""

    def test_invalid_pyvider_log_level(self, monkeypatch: MonkeyPatch, capsys: CaptureFixture[str]) -> None:
        """Tests warning for invalid PYVIDER_LOG_LEVEL."""
        monkeypatch.setenv("PYVIDER_LOG_LEVEL", "SUPER_DEBUG")
        TelemetryConfig.from_env()
        captured_err = capsys.readouterr().err
        # print(f"\nDEBUG: Captured stderr in test_invalid_pyvider_log_level: '''{captured_err}'''") # DEBUG print removed
        expected_msg_part = "Invalid PYVIDER_LOG_LEVEL 'SUPER_DEBUG'. Defaulting to DEBUG."
        assert "[Pyvider Config Warning] WARNING (pyvider.telemetry.config_warnings):" in captured_err
        assert expected_msg_part in captured_err

    def test_invalid_pyvider_log_console_formatter(self, monkeypatch: MonkeyPatch, capsys: CaptureFixture[str]) -> None:
        """Tests warning for invalid PYVIDER_LOG_CONSOLE_FORMATTER."""
        monkeypatch.setenv("PYVIDER_LOG_CONSOLE_FORMATTER", "super_formatter")
        TelemetryConfig.from_env()
        captured_err = capsys.readouterr().err
        expected_msg_part = "Invalid PYVIDER_LOG_CONSOLE_FORMATTER 'super_formatter'. Defaulting to 'key_value'."
        assert "[Pyvider Config Warning] WARNING (pyvider.telemetry.config_warnings):" in captured_err
        assert expected_msg_part in captured_err

    @pytest.mark.parametrize(
        "module_levels_env, expected_warning_parts",
        [
            (
                "no_colon_module_level",
                ["Invalid item 'no_colon_module_level' in PYVIDER_LOG_MODULE_LEVELS. Expected 'module:LEVEL' format. Skipping."]
            ),
            (
                ":DEBUG",
                ["Empty module name in PYVIDER_LOG_MODULE_LEVELS item ':DEBUG'. Skipping."]
            ),
            (
                "valid_module:SUPER_LEVEL",
                ["Invalid log level 'SUPER_LEVEL' for module 'valid_module' in PYVIDER_LOG_MODULE_LEVELS. Skipping."]
            ),
            (
                "mod1:INFO,mod2:BOGUS,mod3:DEBUG",
                [
                    "Invalid log level 'BOGUS' for module 'mod2' in PYVIDER_LOG_MODULE_LEVELS. Skipping."
                ]
            ),
            (
                "mod1:INFO,,mod3:DEBUG", # Empty item
                # No specific warning for empty item, it's just skipped.
                # This test ensures it doesn't crash and valid ones are parsed.
                []
            ),
             (
                "mod1:INFO, :TRACE ,mod3:DEBUG", # module name is whitespace
                ["Empty module name in PYVIDER_LOG_MODULE_LEVELS item ':TRACE'. Skipping."]
            ),

        ]
    )
    def test_invalid_pyvider_log_module_levels(
        self, monkeypatch: MonkeyPatch, capsys: CaptureFixture[str], module_levels_env: str, expected_warning_parts: list[str]
    ) -> None:
        """Tests warnings for various invalid PYVIDER_LOG_MODULE_LEVELS entries."""
        monkeypatch.setenv("PYVIDER_LOG_MODULE_LEVELS", module_levels_env)
        config = TelemetryConfig.from_env()
        captured_err = capsys.readouterr().err

        if not expected_warning_parts: # For cases where no warning is expected for a specific part
            # Check that other valid parts might still be processed if any
            if "mod1:INFO" in module_levels_env:
                assert config.logging.module_levels.get("mod1") == "INFO"
            if "mod3:DEBUG" in module_levels_env:
                 assert config.logging.module_levels.get("mod3") == "DEBUG"
            # And no error message beyond what's expected
            if not any(part in captured_err for part in ["Invalid item", "Empty module name", "Invalid log level"]):
                return # Successfully skipped bad part without specific warning for it.

        for part in expected_warning_parts:
            assert "[Pyvider Config Warning] WARNING (pyvider.telemetry.config_warnings):" in captured_err
            assert part in captured_err


def test_default_output_is_stderr(
    setup_pyvider_telemetry_for_test: Callable[[TelemetryConfig | None], None],
    captured_stderr_for_pyvider: io.StringIO
) -> None:
    """
    Tests that the default logging output goes to sys.stderr.
    It relies on `captured_stderr_for_pyvider` to capture stderr.
    """
    # Ensure key-value formatting for this test, as it checks default emoji presentation
    config = TelemetryConfig(logging=LoggingConfig(console_formatter="key_value"))
    setup_pyvider_telemetry_for_test(config) # Use explicit config

    log_message = "Test message to check default stderr output."
    pyvider_logger_instance.info(log_message)

    output = captured_stderr_for_pyvider.getvalue()

    # The default DAS emoji for info is 🗣️, and default logger name is not included in KV.
    # The message itself is "Test message to check default stderr output."
    # We need to ensure the assert_log_output reflects the default emoji and message.
    # Default emoji for info is 🗣️, so the expected message will be "🗣️ Test message to check default stderr output."
    expected_message_with_emoji = f"🗣️ {log_message}"

    assert_log_output(
        output,
        expected_level="info",
        expected_message_core=expected_message_with_emoji,
        is_json=False, # Default is key-value
        expect_timestamp=True # Default includes timestamp
    )

# --- Tests for logger/base.py specific behaviors ---



class TestPyviderLoggerUnconfiguredAndMisc:
    """
    Tests for PyviderLogger in unconfigured states and other miscellaneous
    internal behaviors from logger/base.py.
    """

    def test_get_logger_no_name(self) -> None:
        """Tests get_logger() with no name argument defaults to 'pyvider.default'."""
        # Use the global pyvider_logger_instance or a fresh one
        # Its configuration state doesn't strictly matter for this specific test's goal,
        # which is to check the default name binding.
        logger = pyvider_logger_instance.get_logger()

        # To check the bound name, we can try to access the internal bound variables.
        # This is a bit of an introspection into structlog's BoundLogger.
        # Alternatively, if a processor adds logger_name to event_dict, we could log and check.
        # For a unit test of get_logger, checking internal state is acceptable.
        # structlog.get_logger().bind(...) returns a BoundLogger.
        # The bound variables are in _context.
        assert logger._context.get("logger_name") == "pyvider.default"

    def test_format_message_with_args_fallback(self) -> None:
        """Tests _format_message_with_args() fallback for incorrect format strings."""
        # PyviderLogger instance needed to call the protected method
        logger_instance = PyviderLogger()

        # Mismatched format specifier (%q is not standard Python string formatting)
        formatted_msg = logger_instance._format_message_with_args("Invalid %s %q format", ("test", 123))
        assert formatted_msg == "Invalid %s %q format test 123"

        # Too few arguments
        formatted_msg_too_few = logger_instance._format_message_with_args("Need %s and %s", ("one",))
        assert formatted_msg_too_few == "Need %s and %s one" # Fallback behavior

        # Non-string event with args (should use fallback)
        formatted_msg_non_string = logger_instance._format_message_with_args(12345, ("arg1",))
        assert formatted_msg_non_string == "12345 arg1"


    def test_trace_no_pyvider_logger_name(
        self,
        setup_pyvider_telemetry_for_test: Callable[[TelemetryConfig | None], None],
        captured_stderr_for_pyvider: io.StringIO
    ) -> None:
        """Tests trace() when _pyvider_logger_name is not provided."""
        # Setup telemetry with TRACE enabled for a known logger to capture its output
        # We need to ensure "pyvider.dynamic_call_trace" will output at TRACE level.
        cfg = TelemetryConfig(
            logging=LoggingConfig(
                default_level="INFO", # Default for others
                module_levels={"pyvider.dynamic_call_trace": "TRACE"},
                logger_name_emoji_prefix_enabled=False, # Simplify output
                das_emoji_prefix_enabled=False
            )
        )
        setup_pyvider_telemetry_for_test(cfg)

        pyvider_logger_instance.trace("Trace message no explicit name", key="value")
        captured_stderr_for_pyvider.getvalue()

        # Check that the output contains the message and the logger_name was the default for trace
        # This requires a way to parse the output or ensure logger_name is in the output.
        # If using key-value, logger_name is popped. If JSON, it's present.
        # Let's reconfigure for JSON to make this assertion easier.

        captured_stderr_for_pyvider.truncate(0)
        captured_stderr_for_pyvider.seek(0)

        json_cfg = TelemetryConfig(
            logging=LoggingConfig(
                default_level="INFO",
                console_formatter="json", # Use JSON to see logger_name
                module_levels={"pyvider.dynamic_call_trace": "TRACE"},
                logger_name_emoji_prefix_enabled=False,
                das_emoji_prefix_enabled=False
            )
        )
        setup_pyvider_telemetry_for_test(json_cfg)

        pyvider_logger_instance.trace("Trace message no explicit name JSON", trace_key="trace_val")
        json_output = captured_stderr_for_pyvider.getvalue()

        # Filter out setup messages
        log_lines = [line for line in json_output.strip().splitlines() if not line.startswith("[Pyvider Setup]")]
        assert len(log_lines) == 1
        log_data = json.loads(log_lines[0])

        assert log_data["event"] == "Trace message no explicit name JSON"
        assert log_data["logger_name"] == "pyvider.dynamic_call_trace"
        assert log_data["trace_key"] == "trace_val"
        assert log_data["level"] == TRACE_LEVEL_NAME.lower()

    def test_logging_when_not_configured(self, capsys: CaptureFixture[str]) -> None:
        """
        Tests that logging calls do not crash and produce no output
        if setup_telemetry has not been run (i.e., _is_configured_by_setup is False).
        """
        original_config = structlog.get_config()
        try:
            structlog.configure(
                processors=[],
                logger_factory=structlog.ReturnLoggerFactory(),
                cache_logger_on_first_use=False
            )

            fresh_logger = PyviderLogger()
            assert not fresh_logger._is_configured_by_setup

            fresh_logger.info("Info from unconfigured logger", key="val")
            fresh_logger.error("Error from unconfigured logger", error_code=123)
            try:
                raise ValueError("Test unconfigured exception")
            except ValueError:
                fresh_logger.exception("Exception from unconfigured logger")

            captured = capsys.readouterr()
            assert captured.out == ""
            assert captured.err == ""

            unconfigured_named_logger = fresh_logger.get_logger("unconfigured.test")
            unconfigured_named_logger.info("Info from unconfigured named logger")

            captured_after_named = capsys.readouterr()
            assert captured_after_named.out == ""
            assert captured_after_named.err == ""

            assert fresh_logger._internal_logger._context.get("logger_name") == "pyvider.telemetry.logger.base.PyviderLogger"
        finally:
            if original_config:
                 structlog.configure(**original_config)
            else:
                 structlog.reset_defaults()

# 🧪🏁
