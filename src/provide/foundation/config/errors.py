#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from __future__ import annotations

from typing import Any

from provide.foundation.errors.base import FoundationError

"""Configuration-specific error types and utilities.

Provides standardized error handling for configuration parsing and validation
with consistent messages and diagnostic context.
"""


class ConfigError(FoundationError):
    """Base configuration error."""

    def _default_code(self) -> str:
        return "CONFIG_ERROR"


class ParseError(ConfigError):
    """Configuration value parsing failed."""

    def __init__(
        self,
        message: str,
        *,
        value: str | Any,
        field_name: str | None = None,
        expected_type: str | None = None,
        valid_options: list[str] | None = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(
            message,
            value=value,
            field_name=field_name,
            expected_type=expected_type,
            valid_options=valid_options,
            **kwargs,
        )

    def _default_code(self) -> str:
        return "PARSE_ERROR"


class ValidationError(ConfigError):
    """Configuration value validation failed."""

    def __init__(
        self,
        message: str,
        *,
        value: Any,
        field_name: str,
        constraint: str | None = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(
            message,
            value=value,
            field_name=field_name,
            constraint=constraint,
            **kwargs,
        )

    def _default_code(self) -> str:
        return "VALIDATION_ERROR"


# Standardized error message formatters


def format_invalid_value_error(
    field_name: str,
    value: Any,
    expected_type: str | None = None,
    valid_options: list[str] | None = None,
    additional_info: str | None = None,
) -> str:
    """Create a standardized invalid value error message.

    Args:
        field_name: Name of the field being parsed
        value: The invalid value
        expected_type: Expected type (e.g., "boolean", "float")
        valid_options: List of valid option strings
        additional_info: Additional context about the error

    Returns:
        Formatted error message

    Examples:
        >>> format_invalid_value_error("log_level", "INVALID", valid_options=["DEBUG", "INFO"])
        "Invalid log_level 'INVALID'. Valid options: DEBUG, INFO"

        >>> format_invalid_value_error("sample_rate", "abc", expected_type="float")
        "Invalid sample_rate 'abc'. Expected: float"

    """
    parts = [f"Invalid {field_name} '{value}'."]

    if valid_options:
        parts.append(f"Valid options: {', '.join(valid_options)}")
    elif expected_type:
        parts.append(f"Expected: {expected_type}")

    if additional_info:
        parts.append(additional_info)

    return " ".join(parts)


def format_validation_error(
    field_name: str,
    value: Any,
    constraint: str,
    additional_info: str | None = None,
) -> str:
    """Create a standardized validation error message.

    Args:
        field_name: Name of the field being validated
        value: The invalid value
        constraint: Description of the constraint that failed
        additional_info: Additional context

    Returns:
        Formatted error message

    Examples:
        >>> format_validation_error("port", 0, "must be between 1 and 65535")
        "Value 0 for port must be between 1 and 65535"

        >>> format_validation_error("sample_rate", 1.5, "must be between 0.0 and 1.0")
        "Value 1.5 for sample_rate must be between 0.0 and 1.0"

    """
    parts = [f"Value {value} for {field_name} {constraint}"]

    if additional_info:
        parts.append(f"({additional_info})")

    return "".join(parts)


__all__ = [
    "ConfigError",
    "ParseError",
    "ValidationError",
    "format_invalid_value_error",
    "format_validation_error",
]

# 🧱🏗️🔚
