#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Logger behavior edge case tests for Foundation Telemetry."""

from __future__ import annotations

from collections.abc import Callable
import io
from typing import Any

import pytest

from provide.foundation import (
    LoggingConfig,
    TelemetryConfig,
    logger,  # This is the global FoundationLogger instance
)


def test_logger_with_extreme_names(
    setup_foundation_telemetry_for_test: Callable[[TelemetryConfig | None], None],
    captured_stderr_for_foundation: io.StringIO,
) -> None:
    """Tests logger behavior with extreme names."""
    config = TelemetryConfig(
        logging=LoggingConfig(
            default_level="INFO",
            console_formatter="key_value",
        ),
    )
    setup_foundation_telemetry_for_test(config)

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
            test_logger.info(
                f"Test message from logger: {name[:50]}",
            )  # Truncate for readability
        except Exception as e:  # pragma: no cover
            pytest.fail(f"Logger failed with name '{name}': {e}")

    # Verify all messages were logged
    output = captured_stderr_for_foundation.getvalue()
    lines = [
        line
        for line in output.strip().splitlines()
        if not line.startswith("[Foundation Setup]")
        and "Configuring structlog output processors" not in line
        and "🗣️ Registered item" not in line
        and not ("[trace    ]" in line or "trace    " in line)
        and line.strip()
    ]
    assert len(lines) == len(extreme_names)


def test_log_message_edge_cases(
    setup_foundation_telemetry_for_test: Callable[[TelemetryConfig | None], None],
    captured_stderr_for_foundation: io.StringIO,
) -> None:
    """Tests logging with edge case message content."""
    config = TelemetryConfig(
        logging=LoggingConfig(
            default_level="INFO",
            console_formatter="key_value",
        ),
    )
    setup_foundation_telemetry_for_test(config)
    test_logger = logger.get_logger("edge.test")

    edge_case_messages: list[Any] = [  # Allow Any for diverse test inputs
        "",  # Empty message
        " ",  # Whitespace only
        "\n\t\r",  # Control characters
        "a" * 10000,  # Very long message
        "Message with %s %d formatting",  # Format string without args
        "Null byte: \x00",  # Null byte
        "Unicode: 🚀🌟💫🔥⚡",  # Unicode characters
        'JSON-like: {"key": "value", "number": 123}',  # JSON content
        "HTML-like: <script>alert('test')</script>",  # HTML content
        "Multi\nline\nmessage",  # Multiline
        "Tabs\tand\ttabs",  # Tab characters
        "Binary-like: \x01\x02\x03\x04",  # Binary data
    ]

    for message in edge_case_messages:
        try:
            test_logger.info(message)
        except Exception as e:  # pragma: no cover
            pytest.fail(f"Logging failed with message '{str(message)[:50]}...': {e}")

    # Verify output exists
    output = captured_stderr_for_foundation.getvalue()
    lines = [
        line
        for line in output.strip().splitlines()
        if not line.startswith("[Foundation Setup]")
        and "Configuring structlog output processors" not in line
        and "🗣️ Registered item" not in line
        and not ("[trace    ]" in line or "trace    " in line)
        and line.strip()
    ]
    assert len(lines) >= len(edge_case_messages)


def test_logger_args_formatting_edge_cases(
    setup_foundation_telemetry_for_test: Callable[[TelemetryConfig | None], None],
    captured_stderr_for_foundation: io.StringIO,
) -> None:
    """Tests logger argument formatting edge cases using FoundationLogger's methods."""
    config = TelemetryConfig(
        logging=LoggingConfig(
            default_level="INFO",
            console_formatter="key_value",
        ),
    )
    setup_foundation_telemetry_for_test(config)
    # Using the global logger instance which has the FoundationLogger methods

    test_cases: list[tuple[str, tuple[Any, ...], bool]] = [
        # (message, args, should_not_raise)
        ("Simple message with %s", ("arg1",), True),
        ("Multiple args: %s %d %s", ("str", 42, "end"), True),
        (
            "Too few args: %s %s",
            ("only_one",),
            True,
        ),  # FoundationLogger's _format_message_with_args handles this
        (
            "Too many args: %s",
            ("arg1", "arg2", "extra"),
            True,
        ),  # FoundationLogger's _format_message_with_args handles this
        (
            "Invalid format: %q",
            ("arg",),
            True,
        ),  # FoundationLogger's _format_message_with_args handles this
        (
            "No format but args",
            ("arg1", "arg2"),
            True,
        ),  # FoundationLogger's _format_message_with_args handles this
        ("Empty args", (), True),
        ("Unicode in args: %s", ("🚀🌟",), True),
        ("None arg: %s", (None,), True),
        ("Complex object: %s", ({"key": "value"},), True),
    ]

    for message, args, should_not_raise in test_cases:
        try:
            # Call info method on the global FoundationLogger instance
            logger.info(message, *args)
            if not should_not_raise:  # pragma: no cover
                pytest.fail(f"Expected exception for: {message} with args {args}")
        except Exception as e:  # pragma: no cover
            if should_not_raise:
                pytest.fail(
                    f"Unexpected exception for '{message}' with args {args}: {e}",
                )

    output = captured_stderr_for_foundation.getvalue()
    lines = [
        line
        for line in output.strip().splitlines()
        if not line.startswith("[Foundation Setup]")
        and "Configuring structlog output processors" not in line
        and "🗣️ Registered item" not in line
        and not ("[trace    ]" in line or "trace    " in line)
        and line.strip()
    ]
    assert len(lines) == len(test_cases), f"Expected {len(test_cases)} log lines, got {len(lines)}"


def test_trace_level_edge_cases(
    setup_foundation_telemetry_for_test: Callable[[TelemetryConfig | None], None],
    captured_stderr_for_foundation: io.StringIO,
) -> None:
    """Tests TRACE level edge cases."""
    config = TelemetryConfig(
        logging=LoggingConfig(
            default_level="TRACE",
            module_levels={"trace.test": "TRACE"},
        ),
    )
    setup_foundation_telemetry_for_test(config)

    logger.trace("Default trace message")
    logger.trace("Named trace message", _foundation_logger_name="trace.test.custom")
    logger.trace("Trace with args %s %d", "test", 42)
    logger.trace("Trace with kwargs", key1="value1", key2=123)

    output = captured_stderr_for_foundation.getvalue()
    lines = [
        line
        for line in output.strip().splitlines()
        if not line.startswith("[Foundation Setup]")
        and "Configuring structlog output processors" not in line
        and not (
            ("[trace    ]" in line or "trace    " in line)
            and (
                "enrichment processor" in line
                or "Event set discovery" in line
                or "Event enrichment" in line
                or "already completed" in line
                or "Foundation" in line
            )
        )
        and line.strip()
    ]
    assert len(lines) >= 4, "Not all trace messages were logged"
    trace_count = sum(1 for line in lines if "trace" in line.lower())
    assert trace_count >= 4, "TRACE level not properly handled"


# 🧱🏗️🔚
