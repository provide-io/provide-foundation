#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from __future__ import annotations

from typing import Any

from provide.foundation.parsers.errors import _format_invalid_value_error, _format_validation_error
from provide.foundation.serialization import json_loads

"""Basic type parsing functions for primitive types.

Handles parsing of primitive types (bool, float, int) and JSON
data structures from string configuration values.
"""


def parse_bool_extended(value: str | bool) -> bool:
    """Parse boolean from string with lenient/forgiving interpretation.

    This is the **lenient** boolean parser - designed for user-facing configuration
    where we want to be forgiving of various inputs. Any unrecognized string
    defaults to False rather than raising an error.

    **Use Cases:**
    - Environment variables set by end users
    - Feature flags that should default to "off" if misconfigured
    - Optional telemetry settings where failure should not break the system

    **Recognized True Values:** true, yes, 1, on (case-insensitive)
    **Recognized False Values:** false, no, 0, off (case-insensitive)
    **Default Behavior:** Any other string → False (no error)

    Args:
        value: Boolean string representation or actual bool

    Returns:
        Boolean value (defaults to False for unrecognized strings)

    Examples:
        >>> parse_bool_extended("yes")  # True
        >>> parse_bool_extended("FALSE")  # False
        >>> parse_bool_extended("invalid")  # False (no error)
        >>> parse_bool_extended(True)  # True

    """
    # If already a bool, return as-is
    if isinstance(value, bool):
        return value

    # Convert to string and parse
    value_lower = str(value).lower().strip()
    # Only return True for explicit true values, everything else is False
    return value_lower in ("true", "yes", "1", "on")


def parse_bool_strict(value: str | bool | int | float) -> bool:
    """Parse boolean from string with strict validation and clear error messages.

    This is the **strict** boolean parser - designed for internal APIs and critical
    configuration where invalid values should cause immediate failure with helpful
    error messages.

    **Use Cases:**
    - Internal API parameters where precision matters
    - Critical system configurations where misconfiguration is dangerous
    - Programmatic configuration where clear validation errors help developers

    **Recognized True Values:** true, yes, 1, on, enabled (case-insensitive), 1.0
    **Recognized False Values:** false, no, 0, off, disabled (case-insensitive), 0.0
    **Error Behavior:** Raises ValueError with helpful message for invalid values

    Args:
        value: Boolean value as string, bool, int, or float

    Returns:
        Boolean value (never defaults - raises on invalid input)

    Raises:
        TypeError: If value is not a string, bool, int, or float
        ValueError: If value cannot be parsed as boolean

    Examples:
        >>> parse_bool_strict("yes")  # True
        >>> parse_bool_strict("FALSE")  # False
        >>> parse_bool_strict(1)  # True
        >>> parse_bool_strict(0.0)  # False
        >>> parse_bool_strict("invalid")  # ValueError with helpful message
        >>> parse_bool_strict(42)  # ValueError - only 0/1 valid for numbers

    """
    # Check type first for clear error messages
    if not isinstance(value, str | bool | int | float):
        raise TypeError(
            f"Boolean field requires str, bool, int, or float, got {type(value).__name__}. "
            f"Received value: {value!r}",
        )

    # If already a bool, return as-is
    if isinstance(value, bool):
        return value

    # Handle numeric types - only 0 and 1 are valid
    if isinstance(value, int | float):
        if value == 1 or value == 1.0:
            return True
        if value == 0 or value == 0.0:
            return False
        raise ValueError(
            f"Numeric boolean must be 0 or 1, got {value}. "
            f"Use parse_bool_extended() for lenient parsing that defaults to False",
        )

    # Convert to string and parse
    value_lower = value.lower().strip()

    if value_lower in ("true", "yes", "1", "on", "enabled"):
        return True
    if value_lower in ("false", "no", "0", "off", "disabled"):
        return False
    raise ValueError(
        _format_invalid_value_error(
            "boolean",
            value,
            valid_options=["true", "false", "yes", "no", "1", "0", "on", "off", "enabled", "disabled"],
            additional_info="Use parse_bool_extended() for lenient parsing that defaults to False",
        ),
    )


def parse_bool(value: Any, strict: bool = False) -> bool:
    """Parse a boolean value from string or other types.

    Accepts: true/false, yes/no, 1/0, on/off (case-insensitive)

    Args:
        value: Value to parse as boolean
        strict: If True, only accept bool or string types (raise TypeError otherwise)

    Returns:
        Boolean value

    Raises:
        TypeError: If strict=True and value is not bool or string, or if value is not bool/str
        ValueError: If value cannot be parsed as boolean

    """
    if strict and not isinstance(value, (bool, str)):
        raise TypeError(f"Cannot convert {type(value).__name__} to bool: {value!r}")

    return parse_bool_strict(value)


def parse_float_with_validation(
    value: str,
    min_val: float | None = None,
    max_val: float | None = None,
) -> float:
    """Parse float with optional range validation.

    Args:
        value: String representation of float
        min_val: Minimum allowed value (inclusive)
        max_val: Maximum allowed value (inclusive)

    Returns:
        Parsed float value

    Raises:
        ValueError: If value is not a valid float or out of range

    """
    try:
        result = float(value)
    except (ValueError, TypeError) as e:
        raise ValueError(
            _format_invalid_value_error("float", value, expected_type="float"),
        ) from e

    if min_val is not None and result < min_val:
        raise ValueError(
            _format_validation_error("float", result, f"must be >= {min_val}"),
        )

    if max_val is not None and result > max_val:
        raise ValueError(
            _format_validation_error("float", result, f"must be <= {max_val}"),
        )

    return result


def parse_sample_rate(value: str) -> float:
    """Parse sampling rate (0.0 to 1.0).

    Args:
        value: String representation of sampling rate

    Returns:
        Float between 0.0 and 1.0

    Raises:
        ValueError: If value is not valid or out of range

    """
    return parse_float_with_validation(value, min_val=0.0, max_val=1.0)


def parse_json_dict(value: str) -> dict[str, Any]:
    """Parse JSON string into dictionary.

    Args:
        value: JSON string

    Returns:
        Parsed dictionary

    Raises:
        ValueError: If JSON is invalid

    """
    if not value or not value.strip():
        return {}

    try:
        result = json_loads(value)
        if not isinstance(result, dict):
            raise ValueError(
                _format_invalid_value_error(
                    "json_dict",
                    type(result).__name__,
                    expected_type="JSON object",
                ),
            )
        return result
    except Exception as e:
        raise ValueError(
            _format_invalid_value_error("json_dict", value, expected_type="valid JSON"),
        ) from e


def parse_json_list(value: str) -> list[Any]:
    """Parse JSON string into list.

    Args:
        value: JSON string

    Returns:
        Parsed list

    Raises:
        ValueError: If JSON is invalid

    """
    if not value or not value.strip():
        return []

    try:
        result = json_loads(value)
        if not isinstance(result, list):
            raise ValueError(
                _format_invalid_value_error(
                    "json_list",
                    type(result).__name__,
                    expected_type="JSON array",
                ),
            )
        return result
    except Exception as e:
        raise ValueError(
            _format_invalid_value_error("json_list", value, expected_type="valid JSON"),
        ) from e


__all__ = [
    "parse_bool",
    "parse_bool_extended",
    "parse_bool_strict",
    "parse_float_with_validation",
    "parse_json_dict",
    "parse_json_list",
    "parse_sample_rate",
]

# 🧱🏗️🔚
