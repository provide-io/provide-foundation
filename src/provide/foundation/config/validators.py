#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from provide.foundation.parsers.errors import (
    _VALID_LOG_LEVEL_TUPLE,
    _VALID_OVERFLOW_POLICY_TUPLE,
    _format_invalid_value_error,
    _format_validation_error,
)

"""Validation functions for configuration field values.

These validators are used with the attrs `validator` parameter to validate
field values after conversion. They provide consistent error messages and
follow attrs validator conventions.
"""


def validate_log_level(instance: Any, attribute: Any, value: str) -> None:
    """Validate that a log level is valid."""
    # Import ValidationError locally to avoid circular imports
    from provide.foundation.errors.config import ValidationError

    if value not in _VALID_LOG_LEVEL_TUPLE:
        raise ValidationError(
            _format_invalid_value_error(
                attribute.name,
                value,
                valid_options=list(_VALID_LOG_LEVEL_TUPLE),
            ),
        )


def validate_sample_rate(instance: Any, attribute: Any, value: float) -> None:
    """Validate that a sample rate is between 0.0 and 1.0."""
    # Import ValidationError locally to avoid circular imports
    from provide.foundation.errors.config import ValidationError

    if not 0.0 <= value <= 1.0:
        raise ValidationError(
            _format_validation_error(attribute.name, value, "must be between 0.0 and 1.0"),
        )


def validate_port(instance: Any, attribute: Any, value: int) -> None:
    """Validate that a port number is valid."""
    # Import ValidationError locally to avoid circular imports
    from provide.foundation.errors.config import ValidationError

    if not 1 <= value <= 65535:
        raise ValidationError(
            _format_validation_error(attribute.name, value, "must be between 1 and 65535"),
        )


def validate_positive(instance: Any, attribute: Any, value: float) -> None:
    """Validate that a value is positive."""
    # Import ValidationError locally to avoid circular imports
    from provide.foundation.errors.config import ValidationError

    # Check if value is numeric
    if not isinstance(value, (int, float)):
        raise ValidationError(
            f"Value must be a number, got {type(value).__name__}",
        )

    if value <= 0:
        raise ValidationError(
            _format_validation_error(attribute.name, value, "must be positive"),
        )


def validate_non_negative(instance: Any, attribute: Any, value: float) -> None:
    """Validate that a value is non-negative."""
    # Import ValidationError locally to avoid circular imports
    from provide.foundation.errors.config import ValidationError

    # Check if value is numeric
    if not isinstance(value, (int, float)):
        raise ValidationError(
            f"Value must be a number, got {type(value).__name__}",
        )

    if value < 0:
        raise ValidationError(
            _format_validation_error(attribute.name, value, "must be non-negative"),
        )


def validate_overflow_policy(instance: Any, attribute: Any, value: str) -> None:
    """Validate rate limit overflow policy."""
    # Import ValidationError locally to avoid circular imports
    from provide.foundation.errors.config import ValidationError

    if value not in _VALID_OVERFLOW_POLICY_TUPLE:
        raise ValidationError(
            _format_invalid_value_error(
                attribute.name,
                value,
                valid_options=list(_VALID_OVERFLOW_POLICY_TUPLE),
            ),
        )


def validate_choice(choices: list[Any]) -> Callable[[Any, Any, Any], None]:
    """Create a validator that ensures value is one of the given choices.

    Args:
        choices: List of valid choices

    Returns:
        Validator function for use with attrs

    """

    def validator(instance: Any, attribute: Any, value: Any) -> None:
        if value not in choices:
            # Import ValidationError locally to avoid circular imports
            from provide.foundation.errors.config import ValidationError

            raise ValidationError(
                f"Invalid value '{value}' for {attribute.name}. Must be one of: {choices!r}",
            )

    return validator


def validate_range(min_val: float, max_val: float) -> Callable[[Any, Any, Any], None]:
    """Create a validator that ensures value is within the given numeric range.

    Args:
        min_val: Minimum allowed value (inclusive)
        max_val: Maximum allowed value (inclusive)

    Returns:
        Validator function for use with attrs

    """

    def validator(instance: Any, attribute: Any, value: Any) -> None:
        # Import ValidationError locally to avoid circular imports
        from provide.foundation.errors.config import ValidationError

        # Check if value is numeric
        if not isinstance(value, (int, float)):
            raise ValidationError(
                f"Value must be a number, got {type(value).__name__}",
            )

        if not (min_val <= value <= max_val):
            raise ValidationError(
                f"Value must be between {min_val} and {max_val}, got {value}",
            )

    return validator


__all__ = [
    "validate_choice",
    "validate_log_level",
    "validate_non_negative",
    "validate_overflow_policy",
    "validate_port",
    "validate_positive",
    "validate_range",
    "validate_sample_rate",
]

# 🧱🏗️🔚
