#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

"""Error formatting utilities and validation constants for parsers.

Provides shared error formatting functions and common constants
used across all parser modules.
"""

if TYPE_CHECKING:
    from provide.foundation.logger.types import ConsoleFormatterStr, LogLevelStr
else:
    LogLevelStr = str
    ConsoleFormatterStr = str


# Standardized error message formatting utilities


def _format_invalid_value_error(
    field_name: str,
    value: Any,
    valid_options: list[str] | None = None,
    expected_type: str | None = None,
    additional_info: str | None = None,
) -> str:
    """Create standardized invalid value error message."""
    parts = [f"Invalid {field_name} '{value}'."]

    if valid_options:
        parts.append(f"Valid options: {', '.join(valid_options)}")
    elif expected_type:
        parts.append(f"Expected: {expected_type}")

    if additional_info:
        parts.append(additional_info)

    return " ".join(parts)


def _format_validation_error(field_name: str, value: Any, constraint: str) -> str:
    """Create standardized validation error message."""
    return f"Value {value} for {field_name} {constraint}"


# Constants for validation

_VALID_LOG_LEVEL_TUPLE = (
    "TRACE",
    "DEBUG",
    "INFO",
    "WARNING",
    "ERROR",
    "CRITICAL",
)

_VALID_FORMATTER_TUPLE = (
    "key_value",
    "json",
)

_VALID_FOUNDATION_LOG_OUTPUT_TUPLE = (
    "console",
    "file",
    "both",
)

_VALID_OVERFLOW_POLICY_TUPLE = (
    "drop_oldest",
    "drop_newest",
    "block",
)

__all__ = [
    "_VALID_FORMATTER_TUPLE",
    "_VALID_FOUNDATION_LOG_OUTPUT_TUPLE",
    "_VALID_LOG_LEVEL_TUPLE",
    "_VALID_OVERFLOW_POLICY_TUPLE",
    "ConsoleFormatterStr",
    "LogLevelStr",
    "_format_invalid_value_error",
    "_format_validation_error",
]

# 🧱🏗️🔚
