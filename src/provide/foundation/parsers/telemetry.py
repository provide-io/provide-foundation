#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from __future__ import annotations

from typing import TYPE_CHECKING, cast

from provide.foundation.parsers.errors import (
    _VALID_FORMATTER_TUPLE,
    _VALID_LOG_LEVEL_TUPLE,
    _format_invalid_value_error,
)

"""Telemetry and logging-specific parsers.

Handles parsing of domain-specific telemetry configuration like log levels,
console formatters, and foundation-specific output settings.
"""

if TYPE_CHECKING:
    from provide.foundation.logger.types import ConsoleFormatterStr, LogLevelStr
else:
    LogLevelStr = str
    ConsoleFormatterStr = str


def parse_log_level(value: str) -> LogLevelStr:
    """Parse and validate log level string.

    Args:
        value: Log level string (case-insensitive)

    Returns:
        Valid log level string in uppercase

    Raises:
        ValueError: If the log level is invalid

    """
    level = value.upper()
    if level not in _VALID_LOG_LEVEL_TUPLE:
        raise ValueError(
            _format_invalid_value_error(
                "log_level",
                value,
                valid_options=list(_VALID_LOG_LEVEL_TUPLE),
            ),
        )
    return cast("LogLevelStr", level)


def parse_console_formatter(value: str) -> ConsoleFormatterStr:
    """Parse and validate console formatter string.

    Args:
        value: Formatter string (case-insensitive)

    Returns:
        Valid formatter string in lowercase

    Raises:
        ValueError: If the formatter is invalid

    """
    formatter = value.lower()
    if formatter not in _VALID_FORMATTER_TUPLE:
        raise ValueError(
            _format_invalid_value_error(
                "console_formatter",
                value,
                valid_options=list(_VALID_FORMATTER_TUPLE),
            ),
        )
    return cast("ConsoleFormatterStr", formatter)


def parse_foundation_log_output(value: str) -> str:
    """Parse and validate foundation log output destination.

    Args:
        value: Output destination string

    Returns:
        Valid output destination (stderr, stdout, main)

    Raises:
        ValueError: If the value is invalid

    """
    if not value:
        return "stderr"

    normalized = value.lower().strip()
    valid_options = ("stderr", "stdout", "main")

    if normalized in valid_options:
        return normalized
    raise ValueError(
        _format_invalid_value_error(
            "foundation_log_output",
            value,
            valid_options=list(valid_options),
        ),
    )


__all__ = [
    "parse_console_formatter",
    "parse_foundation_log_output",
    "parse_log_level",
]

# 🧱🏗️🔚
