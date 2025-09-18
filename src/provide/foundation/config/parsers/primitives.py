from __future__ import annotations

import json
from typing import Any

from provide.foundation.config.parsers.base import _format_invalid_value_error, _format_validation_error

"""Basic type parsing functions for configuration values.

Handles parsing of primitive types (bool, float, int) and simple
data structures (lists) from string configuration values.
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


def parse_bool_strict(value: str | bool) -> bool:
    """Parse boolean from string with strict validation and clear error messages.

    This is the **strict** boolean parser - designed for internal APIs and critical
    configuration where invalid values should cause immediate failure with helpful
    error messages.

    **Use Cases:**
    - Internal API parameters where precision matters
    - Critical system configurations where misconfiguration is dangerous
    - Programmatic configuration where clear validation errors help developers

    **Recognized True Values:** true, yes, 1, on (case-insensitive)
    **Recognized False Values:** false, no, 0, off (case-insensitive)
    **Error Behavior:** Raises ValueError with helpful message for invalid values

    Args:
        value: Boolean string representation or actual bool

    Returns:
        Boolean value (never defaults - raises on invalid input)

    Raises:
        TypeError: If value is not a string or bool
        ValueError: If string value cannot be parsed as boolean

    Examples:
        >>> parse_bool_strict("yes")  # True
        >>> parse_bool_strict("FALSE")  # False
        >>> parse_bool_strict("invalid")  # ValueError with helpful message
        >>> parse_bool_strict(42)  # TypeError

    """
    # Check type first for clear error messages
    if not isinstance(value, (str, bool)):
        raise TypeError(
            f"Boolean field requires str or bool, got {type(value).__name__}. Received value: {value!r}",
        )

    # If already a bool, return as-is
    if isinstance(value, bool):
        return value

    # Convert to string and parse
    value_lower = value.lower().strip()

    if value_lower in ("true", "yes", "1", "on"):
        return True
    if value_lower in ("false", "no", "0", "off"):
        return False
    raise ValueError(
        _format_invalid_value_error(
            "boolean",
            value,
            valid_options=["true", "false", "yes", "no", "1", "0", "on", "off"],
            additional_info="Use parse_bool_extended() for lenient parsing that defaults to False",
        ),
    )


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


def parse_comma_list(value: str) -> list[str]:
    """Parse comma-separated list of strings.

    Args:
        value: Comma-separated string

    Returns:
        List of trimmed non-empty strings

    """
    if not value or not value.strip():
        return []

    return [item.strip() for item in value.split(",") if item.strip()]


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
        result = json.loads(value)
        if not isinstance(result, dict):
            raise ValueError(
                _format_invalid_value_error(
                    "json_dict",
                    type(result).__name__,
                    expected_type="JSON object",
                ),
            )
        return result
    except json.JSONDecodeError as e:
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
        result = json.loads(value)
        if not isinstance(result, list):
            raise ValueError(
                _format_invalid_value_error(
                    "json_list",
                    type(result).__name__,
                    expected_type="JSON array",
                ),
            )
        return result
    except json.JSONDecodeError as e:
        raise ValueError(
            _format_invalid_value_error("json_list", value, expected_type="valid JSON"),
        ) from e


__all__ = [
    "parse_bool_extended",
    "parse_bool_strict",
    "parse_comma_list",
    "parse_float_with_validation",
    "parse_json_dict",
    "parse_json_list",
    "parse_sample_rate",
]
