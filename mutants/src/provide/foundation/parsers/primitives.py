# provide/foundation/parsers/primitives.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from typing import Any

from provide.foundation.parsers.errors import _format_invalid_value_error, _format_validation_error
from provide.foundation.serialization import json_loads

"""Basic type parsing functions for primitive types.

Handles parsing of primitive types (bool, float, int) and JSON
data structures from string configuration values.
"""
from inspect import signature as _mutmut_signature
from typing import Annotated
from typing import Callable
from typing import ClassVar


MutantDict = Annotated[dict[str, Callable], "Mutant"]


def _mutmut_trampoline(orig, mutants, call_args, call_kwargs, self_arg = None):
    """Forward call to original or mutated function, depending on the environment"""
    import os
    mutant_under_test = os.environ['MUTANT_UNDER_TEST']
    if mutant_under_test == 'fail':
        from mutmut.__main__ import MutmutProgrammaticFailException
        raise MutmutProgrammaticFailException('Failed programmatically')      
    elif mutant_under_test == 'stats':
        from mutmut.__main__ import record_trampoline_hit
        record_trampoline_hit(orig.__module__ + '.' + orig.__name__)
        result = orig(*call_args, **call_kwargs)
        return result
    prefix = orig.__module__ + '.' + orig.__name__ + '__mutmut_'
    if not mutant_under_test.startswith(prefix):
        result = orig(*call_args, **call_kwargs)
        return result
    mutant_name = mutant_under_test.rpartition('.')[-1]
    if self_arg:
        # call to a class method where self is not bound
        result = mutants[mutant_name](self_arg, *call_args, **call_kwargs)
    else:
        result = mutants[mutant_name](*call_args, **call_kwargs)
    return result


def x_parse_bool_extended__mutmut_orig(value: str | bool) -> bool:
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


def x_parse_bool_extended__mutmut_1(value: str | bool) -> bool:
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
    value_lower = None
    # Only return True for explicit true values, everything else is False
    return value_lower in ("true", "yes", "1", "on")


def x_parse_bool_extended__mutmut_2(value: str | bool) -> bool:
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
    value_lower = str(value).upper().strip()
    # Only return True for explicit true values, everything else is False
    return value_lower in ("true", "yes", "1", "on")


def x_parse_bool_extended__mutmut_3(value: str | bool) -> bool:
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
    value_lower = str(None).lower().strip()
    # Only return True for explicit true values, everything else is False
    return value_lower in ("true", "yes", "1", "on")


def x_parse_bool_extended__mutmut_4(value: str | bool) -> bool:
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
    return value_lower not in ("true", "yes", "1", "on")


def x_parse_bool_extended__mutmut_5(value: str | bool) -> bool:
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
    return value_lower in ("XXtrueXX", "yes", "1", "on")


def x_parse_bool_extended__mutmut_6(value: str | bool) -> bool:
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
    return value_lower in ("TRUE", "yes", "1", "on")


def x_parse_bool_extended__mutmut_7(value: str | bool) -> bool:
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
    return value_lower in ("true", "XXyesXX", "1", "on")


def x_parse_bool_extended__mutmut_8(value: str | bool) -> bool:
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
    return value_lower in ("true", "YES", "1", "on")


def x_parse_bool_extended__mutmut_9(value: str | bool) -> bool:
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
    return value_lower in ("true", "yes", "XX1XX", "on")


def x_parse_bool_extended__mutmut_10(value: str | bool) -> bool:
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
    return value_lower in ("true", "yes", "1", "XXonXX")


def x_parse_bool_extended__mutmut_11(value: str | bool) -> bool:
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
    return value_lower in ("true", "yes", "1", "ON")

x_parse_bool_extended__mutmut_mutants : ClassVar[MutantDict] = {
'x_parse_bool_extended__mutmut_1': x_parse_bool_extended__mutmut_1, 
    'x_parse_bool_extended__mutmut_2': x_parse_bool_extended__mutmut_2, 
    'x_parse_bool_extended__mutmut_3': x_parse_bool_extended__mutmut_3, 
    'x_parse_bool_extended__mutmut_4': x_parse_bool_extended__mutmut_4, 
    'x_parse_bool_extended__mutmut_5': x_parse_bool_extended__mutmut_5, 
    'x_parse_bool_extended__mutmut_6': x_parse_bool_extended__mutmut_6, 
    'x_parse_bool_extended__mutmut_7': x_parse_bool_extended__mutmut_7, 
    'x_parse_bool_extended__mutmut_8': x_parse_bool_extended__mutmut_8, 
    'x_parse_bool_extended__mutmut_9': x_parse_bool_extended__mutmut_9, 
    'x_parse_bool_extended__mutmut_10': x_parse_bool_extended__mutmut_10, 
    'x_parse_bool_extended__mutmut_11': x_parse_bool_extended__mutmut_11
}

def parse_bool_extended(*args, **kwargs):
    result = _mutmut_trampoline(x_parse_bool_extended__mutmut_orig, x_parse_bool_extended__mutmut_mutants, args, kwargs)
    return result 

parse_bool_extended.__signature__ = _mutmut_signature(x_parse_bool_extended__mutmut_orig)
x_parse_bool_extended__mutmut_orig.__name__ = 'x_parse_bool_extended'


def x_parse_bool_strict__mutmut_orig(value: str | bool | int | float) -> bool:
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


def x_parse_bool_strict__mutmut_1(value: str | bool | int | float) -> bool:
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
    if isinstance(value, str | bool | int | float):
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


def x_parse_bool_strict__mutmut_2(value: str | bool | int | float) -> bool:
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
            None,
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


def x_parse_bool_strict__mutmut_3(value: str | bool | int | float) -> bool:
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
            f"Boolean field requires str, bool, int, or float, got {type(None).__name__}. "
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


def x_parse_bool_strict__mutmut_4(value: str | bool | int | float) -> bool:
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
        if value == 1 and value == 1.0:
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


def x_parse_bool_strict__mutmut_5(value: str | bool | int | float) -> bool:
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
        if value != 1 or value == 1.0:
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


def x_parse_bool_strict__mutmut_6(value: str | bool | int | float) -> bool:
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
        if value == 2 or value == 1.0:
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


def x_parse_bool_strict__mutmut_7(value: str | bool | int | float) -> bool:
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
        if value == 1 or value != 1.0:
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


def x_parse_bool_strict__mutmut_8(value: str | bool | int | float) -> bool:
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
        if value == 1 or value == 2.0:
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


def x_parse_bool_strict__mutmut_9(value: str | bool | int | float) -> bool:
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
            return False
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


def x_parse_bool_strict__mutmut_10(value: str | bool | int | float) -> bool:
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
        if value == 0 and value == 0.0:
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


def x_parse_bool_strict__mutmut_11(value: str | bool | int | float) -> bool:
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
        if value != 0 or value == 0.0:
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


def x_parse_bool_strict__mutmut_12(value: str | bool | int | float) -> bool:
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
        if value == 1 or value == 0.0:
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


def x_parse_bool_strict__mutmut_13(value: str | bool | int | float) -> bool:
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
        if value == 0 or value != 0.0:
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


def x_parse_bool_strict__mutmut_14(value: str | bool | int | float) -> bool:
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
        if value == 0 or value == 1.0:
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


def x_parse_bool_strict__mutmut_15(value: str | bool | int | float) -> bool:
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
            return True
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


def x_parse_bool_strict__mutmut_16(value: str | bool | int | float) -> bool:
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
            None,
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


def x_parse_bool_strict__mutmut_17(value: str | bool | int | float) -> bool:
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
    value_lower = None

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


def x_parse_bool_strict__mutmut_18(value: str | bool | int | float) -> bool:
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
    value_lower = value.upper().strip()

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


def x_parse_bool_strict__mutmut_19(value: str | bool | int | float) -> bool:
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

    if value_lower not in ("true", "yes", "1", "on", "enabled"):
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


def x_parse_bool_strict__mutmut_20(value: str | bool | int | float) -> bool:
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

    if value_lower in ("XXtrueXX", "yes", "1", "on", "enabled"):
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


def x_parse_bool_strict__mutmut_21(value: str | bool | int | float) -> bool:
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

    if value_lower in ("TRUE", "yes", "1", "on", "enabled"):
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


def x_parse_bool_strict__mutmut_22(value: str | bool | int | float) -> bool:
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

    if value_lower in ("true", "XXyesXX", "1", "on", "enabled"):
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


def x_parse_bool_strict__mutmut_23(value: str | bool | int | float) -> bool:
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

    if value_lower in ("true", "YES", "1", "on", "enabled"):
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


def x_parse_bool_strict__mutmut_24(value: str | bool | int | float) -> bool:
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

    if value_lower in ("true", "yes", "XX1XX", "on", "enabled"):
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


def x_parse_bool_strict__mutmut_25(value: str | bool | int | float) -> bool:
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

    if value_lower in ("true", "yes", "1", "XXonXX", "enabled"):
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


def x_parse_bool_strict__mutmut_26(value: str | bool | int | float) -> bool:
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

    if value_lower in ("true", "yes", "1", "ON", "enabled"):
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


def x_parse_bool_strict__mutmut_27(value: str | bool | int | float) -> bool:
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

    if value_lower in ("true", "yes", "1", "on", "XXenabledXX"):
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


def x_parse_bool_strict__mutmut_28(value: str | bool | int | float) -> bool:
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

    if value_lower in ("true", "yes", "1", "on", "ENABLED"):
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


def x_parse_bool_strict__mutmut_29(value: str | bool | int | float) -> bool:
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
        return False
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


def x_parse_bool_strict__mutmut_30(value: str | bool | int | float) -> bool:
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
    if value_lower not in ("false", "no", "0", "off", "disabled"):
        return False
    raise ValueError(
        _format_invalid_value_error(
            "boolean",
            value,
            valid_options=["true", "false", "yes", "no", "1", "0", "on", "off", "enabled", "disabled"],
            additional_info="Use parse_bool_extended() for lenient parsing that defaults to False",
        ),
    )


def x_parse_bool_strict__mutmut_31(value: str | bool | int | float) -> bool:
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
    if value_lower in ("XXfalseXX", "no", "0", "off", "disabled"):
        return False
    raise ValueError(
        _format_invalid_value_error(
            "boolean",
            value,
            valid_options=["true", "false", "yes", "no", "1", "0", "on", "off", "enabled", "disabled"],
            additional_info="Use parse_bool_extended() for lenient parsing that defaults to False",
        ),
    )


def x_parse_bool_strict__mutmut_32(value: str | bool | int | float) -> bool:
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
    if value_lower in ("FALSE", "no", "0", "off", "disabled"):
        return False
    raise ValueError(
        _format_invalid_value_error(
            "boolean",
            value,
            valid_options=["true", "false", "yes", "no", "1", "0", "on", "off", "enabled", "disabled"],
            additional_info="Use parse_bool_extended() for lenient parsing that defaults to False",
        ),
    )


def x_parse_bool_strict__mutmut_33(value: str | bool | int | float) -> bool:
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
    if value_lower in ("false", "XXnoXX", "0", "off", "disabled"):
        return False
    raise ValueError(
        _format_invalid_value_error(
            "boolean",
            value,
            valid_options=["true", "false", "yes", "no", "1", "0", "on", "off", "enabled", "disabled"],
            additional_info="Use parse_bool_extended() for lenient parsing that defaults to False",
        ),
    )


def x_parse_bool_strict__mutmut_34(value: str | bool | int | float) -> bool:
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
    if value_lower in ("false", "NO", "0", "off", "disabled"):
        return False
    raise ValueError(
        _format_invalid_value_error(
            "boolean",
            value,
            valid_options=["true", "false", "yes", "no", "1", "0", "on", "off", "enabled", "disabled"],
            additional_info="Use parse_bool_extended() for lenient parsing that defaults to False",
        ),
    )


def x_parse_bool_strict__mutmut_35(value: str | bool | int | float) -> bool:
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
    if value_lower in ("false", "no", "XX0XX", "off", "disabled"):
        return False
    raise ValueError(
        _format_invalid_value_error(
            "boolean",
            value,
            valid_options=["true", "false", "yes", "no", "1", "0", "on", "off", "enabled", "disabled"],
            additional_info="Use parse_bool_extended() for lenient parsing that defaults to False",
        ),
    )


def x_parse_bool_strict__mutmut_36(value: str | bool | int | float) -> bool:
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
    if value_lower in ("false", "no", "0", "XXoffXX", "disabled"):
        return False
    raise ValueError(
        _format_invalid_value_error(
            "boolean",
            value,
            valid_options=["true", "false", "yes", "no", "1", "0", "on", "off", "enabled", "disabled"],
            additional_info="Use parse_bool_extended() for lenient parsing that defaults to False",
        ),
    )


def x_parse_bool_strict__mutmut_37(value: str | bool | int | float) -> bool:
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
    if value_lower in ("false", "no", "0", "OFF", "disabled"):
        return False
    raise ValueError(
        _format_invalid_value_error(
            "boolean",
            value,
            valid_options=["true", "false", "yes", "no", "1", "0", "on", "off", "enabled", "disabled"],
            additional_info="Use parse_bool_extended() for lenient parsing that defaults to False",
        ),
    )


def x_parse_bool_strict__mutmut_38(value: str | bool | int | float) -> bool:
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
    if value_lower in ("false", "no", "0", "off", "XXdisabledXX"):
        return False
    raise ValueError(
        _format_invalid_value_error(
            "boolean",
            value,
            valid_options=["true", "false", "yes", "no", "1", "0", "on", "off", "enabled", "disabled"],
            additional_info="Use parse_bool_extended() for lenient parsing that defaults to False",
        ),
    )


def x_parse_bool_strict__mutmut_39(value: str | bool | int | float) -> bool:
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
    if value_lower in ("false", "no", "0", "off", "DISABLED"):
        return False
    raise ValueError(
        _format_invalid_value_error(
            "boolean",
            value,
            valid_options=["true", "false", "yes", "no", "1", "0", "on", "off", "enabled", "disabled"],
            additional_info="Use parse_bool_extended() for lenient parsing that defaults to False",
        ),
    )


def x_parse_bool_strict__mutmut_40(value: str | bool | int | float) -> bool:
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
        return True
    raise ValueError(
        _format_invalid_value_error(
            "boolean",
            value,
            valid_options=["true", "false", "yes", "no", "1", "0", "on", "off", "enabled", "disabled"],
            additional_info="Use parse_bool_extended() for lenient parsing that defaults to False",
        ),
    )


def x_parse_bool_strict__mutmut_41(value: str | bool | int | float) -> bool:
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
        None,
    )


def x_parse_bool_strict__mutmut_42(value: str | bool | int | float) -> bool:
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
            None,
            value,
            valid_options=["true", "false", "yes", "no", "1", "0", "on", "off", "enabled", "disabled"],
            additional_info="Use parse_bool_extended() for lenient parsing that defaults to False",
        ),
    )


def x_parse_bool_strict__mutmut_43(value: str | bool | int | float) -> bool:
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
            None,
            valid_options=["true", "false", "yes", "no", "1", "0", "on", "off", "enabled", "disabled"],
            additional_info="Use parse_bool_extended() for lenient parsing that defaults to False",
        ),
    )


def x_parse_bool_strict__mutmut_44(value: str | bool | int | float) -> bool:
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
            valid_options=None,
            additional_info="Use parse_bool_extended() for lenient parsing that defaults to False",
        ),
    )


def x_parse_bool_strict__mutmut_45(value: str | bool | int | float) -> bool:
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
            additional_info=None,
        ),
    )


def x_parse_bool_strict__mutmut_46(value: str | bool | int | float) -> bool:
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
            value,
            valid_options=["true", "false", "yes", "no", "1", "0", "on", "off", "enabled", "disabled"],
            additional_info="Use parse_bool_extended() for lenient parsing that defaults to False",
        ),
    )


def x_parse_bool_strict__mutmut_47(value: str | bool | int | float) -> bool:
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
            valid_options=["true", "false", "yes", "no", "1", "0", "on", "off", "enabled", "disabled"],
            additional_info="Use parse_bool_extended() for lenient parsing that defaults to False",
        ),
    )


def x_parse_bool_strict__mutmut_48(value: str | bool | int | float) -> bool:
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
            additional_info="Use parse_bool_extended() for lenient parsing that defaults to False",
        ),
    )


def x_parse_bool_strict__mutmut_49(value: str | bool | int | float) -> bool:
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
            ),
    )


def x_parse_bool_strict__mutmut_50(value: str | bool | int | float) -> bool:
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
            "XXbooleanXX",
            value,
            valid_options=["true", "false", "yes", "no", "1", "0", "on", "off", "enabled", "disabled"],
            additional_info="Use parse_bool_extended() for lenient parsing that defaults to False",
        ),
    )


def x_parse_bool_strict__mutmut_51(value: str | bool | int | float) -> bool:
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
            "BOOLEAN",
            value,
            valid_options=["true", "false", "yes", "no", "1", "0", "on", "off", "enabled", "disabled"],
            additional_info="Use parse_bool_extended() for lenient parsing that defaults to False",
        ),
    )


def x_parse_bool_strict__mutmut_52(value: str | bool | int | float) -> bool:
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
            valid_options=["XXtrueXX", "false", "yes", "no", "1", "0", "on", "off", "enabled", "disabled"],
            additional_info="Use parse_bool_extended() for lenient parsing that defaults to False",
        ),
    )


def x_parse_bool_strict__mutmut_53(value: str | bool | int | float) -> bool:
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
            valid_options=["TRUE", "false", "yes", "no", "1", "0", "on", "off", "enabled", "disabled"],
            additional_info="Use parse_bool_extended() for lenient parsing that defaults to False",
        ),
    )


def x_parse_bool_strict__mutmut_54(value: str | bool | int | float) -> bool:
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
            valid_options=["true", "XXfalseXX", "yes", "no", "1", "0", "on", "off", "enabled", "disabled"],
            additional_info="Use parse_bool_extended() for lenient parsing that defaults to False",
        ),
    )


def x_parse_bool_strict__mutmut_55(value: str | bool | int | float) -> bool:
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
            valid_options=["true", "FALSE", "yes", "no", "1", "0", "on", "off", "enabled", "disabled"],
            additional_info="Use parse_bool_extended() for lenient parsing that defaults to False",
        ),
    )


def x_parse_bool_strict__mutmut_56(value: str | bool | int | float) -> bool:
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
            valid_options=["true", "false", "XXyesXX", "no", "1", "0", "on", "off", "enabled", "disabled"],
            additional_info="Use parse_bool_extended() for lenient parsing that defaults to False",
        ),
    )


def x_parse_bool_strict__mutmut_57(value: str | bool | int | float) -> bool:
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
            valid_options=["true", "false", "YES", "no", "1", "0", "on", "off", "enabled", "disabled"],
            additional_info="Use parse_bool_extended() for lenient parsing that defaults to False",
        ),
    )


def x_parse_bool_strict__mutmut_58(value: str | bool | int | float) -> bool:
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
            valid_options=["true", "false", "yes", "XXnoXX", "1", "0", "on", "off", "enabled", "disabled"],
            additional_info="Use parse_bool_extended() for lenient parsing that defaults to False",
        ),
    )


def x_parse_bool_strict__mutmut_59(value: str | bool | int | float) -> bool:
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
            valid_options=["true", "false", "yes", "NO", "1", "0", "on", "off", "enabled", "disabled"],
            additional_info="Use parse_bool_extended() for lenient parsing that defaults to False",
        ),
    )


def x_parse_bool_strict__mutmut_60(value: str | bool | int | float) -> bool:
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
            valid_options=["true", "false", "yes", "no", "XX1XX", "0", "on", "off", "enabled", "disabled"],
            additional_info="Use parse_bool_extended() for lenient parsing that defaults to False",
        ),
    )


def x_parse_bool_strict__mutmut_61(value: str | bool | int | float) -> bool:
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
            valid_options=["true", "false", "yes", "no", "1", "XX0XX", "on", "off", "enabled", "disabled"],
            additional_info="Use parse_bool_extended() for lenient parsing that defaults to False",
        ),
    )


def x_parse_bool_strict__mutmut_62(value: str | bool | int | float) -> bool:
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
            valid_options=["true", "false", "yes", "no", "1", "0", "XXonXX", "off", "enabled", "disabled"],
            additional_info="Use parse_bool_extended() for lenient parsing that defaults to False",
        ),
    )


def x_parse_bool_strict__mutmut_63(value: str | bool | int | float) -> bool:
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
            valid_options=["true", "false", "yes", "no", "1", "0", "ON", "off", "enabled", "disabled"],
            additional_info="Use parse_bool_extended() for lenient parsing that defaults to False",
        ),
    )


def x_parse_bool_strict__mutmut_64(value: str | bool | int | float) -> bool:
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
            valid_options=["true", "false", "yes", "no", "1", "0", "on", "XXoffXX", "enabled", "disabled"],
            additional_info="Use parse_bool_extended() for lenient parsing that defaults to False",
        ),
    )


def x_parse_bool_strict__mutmut_65(value: str | bool | int | float) -> bool:
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
            valid_options=["true", "false", "yes", "no", "1", "0", "on", "OFF", "enabled", "disabled"],
            additional_info="Use parse_bool_extended() for lenient parsing that defaults to False",
        ),
    )


def x_parse_bool_strict__mutmut_66(value: str | bool | int | float) -> bool:
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
            valid_options=["true", "false", "yes", "no", "1", "0", "on", "off", "XXenabledXX", "disabled"],
            additional_info="Use parse_bool_extended() for lenient parsing that defaults to False",
        ),
    )


def x_parse_bool_strict__mutmut_67(value: str | bool | int | float) -> bool:
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
            valid_options=["true", "false", "yes", "no", "1", "0", "on", "off", "ENABLED", "disabled"],
            additional_info="Use parse_bool_extended() for lenient parsing that defaults to False",
        ),
    )


def x_parse_bool_strict__mutmut_68(value: str | bool | int | float) -> bool:
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
            valid_options=["true", "false", "yes", "no", "1", "0", "on", "off", "enabled", "XXdisabledXX"],
            additional_info="Use parse_bool_extended() for lenient parsing that defaults to False",
        ),
    )


def x_parse_bool_strict__mutmut_69(value: str | bool | int | float) -> bool:
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
            valid_options=["true", "false", "yes", "no", "1", "0", "on", "off", "enabled", "DISABLED"],
            additional_info="Use parse_bool_extended() for lenient parsing that defaults to False",
        ),
    )


def x_parse_bool_strict__mutmut_70(value: str | bool | int | float) -> bool:
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
            additional_info="XXUse parse_bool_extended() for lenient parsing that defaults to FalseXX",
        ),
    )


def x_parse_bool_strict__mutmut_71(value: str | bool | int | float) -> bool:
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
            additional_info="use parse_bool_extended() for lenient parsing that defaults to false",
        ),
    )


def x_parse_bool_strict__mutmut_72(value: str | bool | int | float) -> bool:
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
            additional_info="USE PARSE_BOOL_EXTENDED() FOR LENIENT PARSING THAT DEFAULTS TO FALSE",
        ),
    )

x_parse_bool_strict__mutmut_mutants : ClassVar[MutantDict] = {
'x_parse_bool_strict__mutmut_1': x_parse_bool_strict__mutmut_1, 
    'x_parse_bool_strict__mutmut_2': x_parse_bool_strict__mutmut_2, 
    'x_parse_bool_strict__mutmut_3': x_parse_bool_strict__mutmut_3, 
    'x_parse_bool_strict__mutmut_4': x_parse_bool_strict__mutmut_4, 
    'x_parse_bool_strict__mutmut_5': x_parse_bool_strict__mutmut_5, 
    'x_parse_bool_strict__mutmut_6': x_parse_bool_strict__mutmut_6, 
    'x_parse_bool_strict__mutmut_7': x_parse_bool_strict__mutmut_7, 
    'x_parse_bool_strict__mutmut_8': x_parse_bool_strict__mutmut_8, 
    'x_parse_bool_strict__mutmut_9': x_parse_bool_strict__mutmut_9, 
    'x_parse_bool_strict__mutmut_10': x_parse_bool_strict__mutmut_10, 
    'x_parse_bool_strict__mutmut_11': x_parse_bool_strict__mutmut_11, 
    'x_parse_bool_strict__mutmut_12': x_parse_bool_strict__mutmut_12, 
    'x_parse_bool_strict__mutmut_13': x_parse_bool_strict__mutmut_13, 
    'x_parse_bool_strict__mutmut_14': x_parse_bool_strict__mutmut_14, 
    'x_parse_bool_strict__mutmut_15': x_parse_bool_strict__mutmut_15, 
    'x_parse_bool_strict__mutmut_16': x_parse_bool_strict__mutmut_16, 
    'x_parse_bool_strict__mutmut_17': x_parse_bool_strict__mutmut_17, 
    'x_parse_bool_strict__mutmut_18': x_parse_bool_strict__mutmut_18, 
    'x_parse_bool_strict__mutmut_19': x_parse_bool_strict__mutmut_19, 
    'x_parse_bool_strict__mutmut_20': x_parse_bool_strict__mutmut_20, 
    'x_parse_bool_strict__mutmut_21': x_parse_bool_strict__mutmut_21, 
    'x_parse_bool_strict__mutmut_22': x_parse_bool_strict__mutmut_22, 
    'x_parse_bool_strict__mutmut_23': x_parse_bool_strict__mutmut_23, 
    'x_parse_bool_strict__mutmut_24': x_parse_bool_strict__mutmut_24, 
    'x_parse_bool_strict__mutmut_25': x_parse_bool_strict__mutmut_25, 
    'x_parse_bool_strict__mutmut_26': x_parse_bool_strict__mutmut_26, 
    'x_parse_bool_strict__mutmut_27': x_parse_bool_strict__mutmut_27, 
    'x_parse_bool_strict__mutmut_28': x_parse_bool_strict__mutmut_28, 
    'x_parse_bool_strict__mutmut_29': x_parse_bool_strict__mutmut_29, 
    'x_parse_bool_strict__mutmut_30': x_parse_bool_strict__mutmut_30, 
    'x_parse_bool_strict__mutmut_31': x_parse_bool_strict__mutmut_31, 
    'x_parse_bool_strict__mutmut_32': x_parse_bool_strict__mutmut_32, 
    'x_parse_bool_strict__mutmut_33': x_parse_bool_strict__mutmut_33, 
    'x_parse_bool_strict__mutmut_34': x_parse_bool_strict__mutmut_34, 
    'x_parse_bool_strict__mutmut_35': x_parse_bool_strict__mutmut_35, 
    'x_parse_bool_strict__mutmut_36': x_parse_bool_strict__mutmut_36, 
    'x_parse_bool_strict__mutmut_37': x_parse_bool_strict__mutmut_37, 
    'x_parse_bool_strict__mutmut_38': x_parse_bool_strict__mutmut_38, 
    'x_parse_bool_strict__mutmut_39': x_parse_bool_strict__mutmut_39, 
    'x_parse_bool_strict__mutmut_40': x_parse_bool_strict__mutmut_40, 
    'x_parse_bool_strict__mutmut_41': x_parse_bool_strict__mutmut_41, 
    'x_parse_bool_strict__mutmut_42': x_parse_bool_strict__mutmut_42, 
    'x_parse_bool_strict__mutmut_43': x_parse_bool_strict__mutmut_43, 
    'x_parse_bool_strict__mutmut_44': x_parse_bool_strict__mutmut_44, 
    'x_parse_bool_strict__mutmut_45': x_parse_bool_strict__mutmut_45, 
    'x_parse_bool_strict__mutmut_46': x_parse_bool_strict__mutmut_46, 
    'x_parse_bool_strict__mutmut_47': x_parse_bool_strict__mutmut_47, 
    'x_parse_bool_strict__mutmut_48': x_parse_bool_strict__mutmut_48, 
    'x_parse_bool_strict__mutmut_49': x_parse_bool_strict__mutmut_49, 
    'x_parse_bool_strict__mutmut_50': x_parse_bool_strict__mutmut_50, 
    'x_parse_bool_strict__mutmut_51': x_parse_bool_strict__mutmut_51, 
    'x_parse_bool_strict__mutmut_52': x_parse_bool_strict__mutmut_52, 
    'x_parse_bool_strict__mutmut_53': x_parse_bool_strict__mutmut_53, 
    'x_parse_bool_strict__mutmut_54': x_parse_bool_strict__mutmut_54, 
    'x_parse_bool_strict__mutmut_55': x_parse_bool_strict__mutmut_55, 
    'x_parse_bool_strict__mutmut_56': x_parse_bool_strict__mutmut_56, 
    'x_parse_bool_strict__mutmut_57': x_parse_bool_strict__mutmut_57, 
    'x_parse_bool_strict__mutmut_58': x_parse_bool_strict__mutmut_58, 
    'x_parse_bool_strict__mutmut_59': x_parse_bool_strict__mutmut_59, 
    'x_parse_bool_strict__mutmut_60': x_parse_bool_strict__mutmut_60, 
    'x_parse_bool_strict__mutmut_61': x_parse_bool_strict__mutmut_61, 
    'x_parse_bool_strict__mutmut_62': x_parse_bool_strict__mutmut_62, 
    'x_parse_bool_strict__mutmut_63': x_parse_bool_strict__mutmut_63, 
    'x_parse_bool_strict__mutmut_64': x_parse_bool_strict__mutmut_64, 
    'x_parse_bool_strict__mutmut_65': x_parse_bool_strict__mutmut_65, 
    'x_parse_bool_strict__mutmut_66': x_parse_bool_strict__mutmut_66, 
    'x_parse_bool_strict__mutmut_67': x_parse_bool_strict__mutmut_67, 
    'x_parse_bool_strict__mutmut_68': x_parse_bool_strict__mutmut_68, 
    'x_parse_bool_strict__mutmut_69': x_parse_bool_strict__mutmut_69, 
    'x_parse_bool_strict__mutmut_70': x_parse_bool_strict__mutmut_70, 
    'x_parse_bool_strict__mutmut_71': x_parse_bool_strict__mutmut_71, 
    'x_parse_bool_strict__mutmut_72': x_parse_bool_strict__mutmut_72
}

def parse_bool_strict(*args, **kwargs):
    result = _mutmut_trampoline(x_parse_bool_strict__mutmut_orig, x_parse_bool_strict__mutmut_mutants, args, kwargs)
    return result 

parse_bool_strict.__signature__ = _mutmut_signature(x_parse_bool_strict__mutmut_orig)
x_parse_bool_strict__mutmut_orig.__name__ = 'x_parse_bool_strict'


def x_parse_bool__mutmut_orig(value: Any, strict: bool = False) -> bool:
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


def x_parse_bool__mutmut_1(value: Any, strict: bool = True) -> bool:
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


def x_parse_bool__mutmut_2(value: Any, strict: bool = False) -> bool:
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
    if strict or not isinstance(value, (bool, str)):
        raise TypeError(f"Cannot convert {type(value).__name__} to bool: {value!r}")

    return parse_bool_strict(value)


def x_parse_bool__mutmut_3(value: Any, strict: bool = False) -> bool:
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
    if strict and isinstance(value, (bool, str)):
        raise TypeError(f"Cannot convert {type(value).__name__} to bool: {value!r}")

    return parse_bool_strict(value)


def x_parse_bool__mutmut_4(value: Any, strict: bool = False) -> bool:
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
        raise TypeError(None)

    return parse_bool_strict(value)


def x_parse_bool__mutmut_5(value: Any, strict: bool = False) -> bool:
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
        raise TypeError(f"Cannot convert {type(None).__name__} to bool: {value!r}")

    return parse_bool_strict(value)


def x_parse_bool__mutmut_6(value: Any, strict: bool = False) -> bool:
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

    return parse_bool_strict(None)

x_parse_bool__mutmut_mutants : ClassVar[MutantDict] = {
'x_parse_bool__mutmut_1': x_parse_bool__mutmut_1, 
    'x_parse_bool__mutmut_2': x_parse_bool__mutmut_2, 
    'x_parse_bool__mutmut_3': x_parse_bool__mutmut_3, 
    'x_parse_bool__mutmut_4': x_parse_bool__mutmut_4, 
    'x_parse_bool__mutmut_5': x_parse_bool__mutmut_5, 
    'x_parse_bool__mutmut_6': x_parse_bool__mutmut_6
}

def parse_bool(*args, **kwargs):
    result = _mutmut_trampoline(x_parse_bool__mutmut_orig, x_parse_bool__mutmut_mutants, args, kwargs)
    return result 

parse_bool.__signature__ = _mutmut_signature(x_parse_bool__mutmut_orig)
x_parse_bool__mutmut_orig.__name__ = 'x_parse_bool'


def x_parse_float_with_validation__mutmut_orig(
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


def x_parse_float_with_validation__mutmut_1(
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
        result = None
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


def x_parse_float_with_validation__mutmut_2(
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
        result = float(None)
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


def x_parse_float_with_validation__mutmut_3(
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
            None,
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


def x_parse_float_with_validation__mutmut_4(
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
            _format_invalid_value_error(None, value, expected_type="float"),
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


def x_parse_float_with_validation__mutmut_5(
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
            _format_invalid_value_error("float", None, expected_type="float"),
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


def x_parse_float_with_validation__mutmut_6(
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
            _format_invalid_value_error("float", value, expected_type=None),
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


def x_parse_float_with_validation__mutmut_7(
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
            _format_invalid_value_error(value, expected_type="float"),
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


def x_parse_float_with_validation__mutmut_8(
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
            _format_invalid_value_error("float", expected_type="float"),
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


def x_parse_float_with_validation__mutmut_9(
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
            _format_invalid_value_error("float", value, ),
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


def x_parse_float_with_validation__mutmut_10(
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
            _format_invalid_value_error("XXfloatXX", value, expected_type="float"),
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


def x_parse_float_with_validation__mutmut_11(
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
            _format_invalid_value_error("FLOAT", value, expected_type="float"),
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


def x_parse_float_with_validation__mutmut_12(
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
            _format_invalid_value_error("float", value, expected_type="XXfloatXX"),
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


def x_parse_float_with_validation__mutmut_13(
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
            _format_invalid_value_error("float", value, expected_type="FLOAT"),
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


def x_parse_float_with_validation__mutmut_14(
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

    if min_val is not None or result < min_val:
        raise ValueError(
            _format_validation_error("float", result, f"must be >= {min_val}"),
        )

    if max_val is not None and result > max_val:
        raise ValueError(
            _format_validation_error("float", result, f"must be <= {max_val}"),
        )

    return result


def x_parse_float_with_validation__mutmut_15(
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

    if min_val is None and result < min_val:
        raise ValueError(
            _format_validation_error("float", result, f"must be >= {min_val}"),
        )

    if max_val is not None and result > max_val:
        raise ValueError(
            _format_validation_error("float", result, f"must be <= {max_val}"),
        )

    return result


def x_parse_float_with_validation__mutmut_16(
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

    if min_val is not None and result <= min_val:
        raise ValueError(
            _format_validation_error("float", result, f"must be >= {min_val}"),
        )

    if max_val is not None and result > max_val:
        raise ValueError(
            _format_validation_error("float", result, f"must be <= {max_val}"),
        )

    return result


def x_parse_float_with_validation__mutmut_17(
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
            None,
        )

    if max_val is not None and result > max_val:
        raise ValueError(
            _format_validation_error("float", result, f"must be <= {max_val}"),
        )

    return result


def x_parse_float_with_validation__mutmut_18(
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
            _format_validation_error(None, result, f"must be >= {min_val}"),
        )

    if max_val is not None and result > max_val:
        raise ValueError(
            _format_validation_error("float", result, f"must be <= {max_val}"),
        )

    return result


def x_parse_float_with_validation__mutmut_19(
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
            _format_validation_error("float", None, f"must be >= {min_val}"),
        )

    if max_val is not None and result > max_val:
        raise ValueError(
            _format_validation_error("float", result, f"must be <= {max_val}"),
        )

    return result


def x_parse_float_with_validation__mutmut_20(
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
            _format_validation_error("float", result, None),
        )

    if max_val is not None and result > max_val:
        raise ValueError(
            _format_validation_error("float", result, f"must be <= {max_val}"),
        )

    return result


def x_parse_float_with_validation__mutmut_21(
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
            _format_validation_error(result, f"must be >= {min_val}"),
        )

    if max_val is not None and result > max_val:
        raise ValueError(
            _format_validation_error("float", result, f"must be <= {max_val}"),
        )

    return result


def x_parse_float_with_validation__mutmut_22(
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
            _format_validation_error("float", f"must be >= {min_val}"),
        )

    if max_val is not None and result > max_val:
        raise ValueError(
            _format_validation_error("float", result, f"must be <= {max_val}"),
        )

    return result


def x_parse_float_with_validation__mutmut_23(
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
            _format_validation_error("float", result, ),
        )

    if max_val is not None and result > max_val:
        raise ValueError(
            _format_validation_error("float", result, f"must be <= {max_val}"),
        )

    return result


def x_parse_float_with_validation__mutmut_24(
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
            _format_validation_error("XXfloatXX", result, f"must be >= {min_val}"),
        )

    if max_val is not None and result > max_val:
        raise ValueError(
            _format_validation_error("float", result, f"must be <= {max_val}"),
        )

    return result


def x_parse_float_with_validation__mutmut_25(
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
            _format_validation_error("FLOAT", result, f"must be >= {min_val}"),
        )

    if max_val is not None and result > max_val:
        raise ValueError(
            _format_validation_error("float", result, f"must be <= {max_val}"),
        )

    return result


def x_parse_float_with_validation__mutmut_26(
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

    if max_val is not None or result > max_val:
        raise ValueError(
            _format_validation_error("float", result, f"must be <= {max_val}"),
        )

    return result


def x_parse_float_with_validation__mutmut_27(
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

    if max_val is None and result > max_val:
        raise ValueError(
            _format_validation_error("float", result, f"must be <= {max_val}"),
        )

    return result


def x_parse_float_with_validation__mutmut_28(
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

    if max_val is not None and result >= max_val:
        raise ValueError(
            _format_validation_error("float", result, f"must be <= {max_val}"),
        )

    return result


def x_parse_float_with_validation__mutmut_29(
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
            None,
        )

    return result


def x_parse_float_with_validation__mutmut_30(
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
            _format_validation_error(None, result, f"must be <= {max_val}"),
        )

    return result


def x_parse_float_with_validation__mutmut_31(
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
            _format_validation_error("float", None, f"must be <= {max_val}"),
        )

    return result


def x_parse_float_with_validation__mutmut_32(
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
            _format_validation_error("float", result, None),
        )

    return result


def x_parse_float_with_validation__mutmut_33(
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
            _format_validation_error(result, f"must be <= {max_val}"),
        )

    return result


def x_parse_float_with_validation__mutmut_34(
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
            _format_validation_error("float", f"must be <= {max_val}"),
        )

    return result


def x_parse_float_with_validation__mutmut_35(
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
            _format_validation_error("float", result, ),
        )

    return result


def x_parse_float_with_validation__mutmut_36(
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
            _format_validation_error("XXfloatXX", result, f"must be <= {max_val}"),
        )

    return result


def x_parse_float_with_validation__mutmut_37(
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
            _format_validation_error("FLOAT", result, f"must be <= {max_val}"),
        )

    return result

x_parse_float_with_validation__mutmut_mutants : ClassVar[MutantDict] = {
'x_parse_float_with_validation__mutmut_1': x_parse_float_with_validation__mutmut_1, 
    'x_parse_float_with_validation__mutmut_2': x_parse_float_with_validation__mutmut_2, 
    'x_parse_float_with_validation__mutmut_3': x_parse_float_with_validation__mutmut_3, 
    'x_parse_float_with_validation__mutmut_4': x_parse_float_with_validation__mutmut_4, 
    'x_parse_float_with_validation__mutmut_5': x_parse_float_with_validation__mutmut_5, 
    'x_parse_float_with_validation__mutmut_6': x_parse_float_with_validation__mutmut_6, 
    'x_parse_float_with_validation__mutmut_7': x_parse_float_with_validation__mutmut_7, 
    'x_parse_float_with_validation__mutmut_8': x_parse_float_with_validation__mutmut_8, 
    'x_parse_float_with_validation__mutmut_9': x_parse_float_with_validation__mutmut_9, 
    'x_parse_float_with_validation__mutmut_10': x_parse_float_with_validation__mutmut_10, 
    'x_parse_float_with_validation__mutmut_11': x_parse_float_with_validation__mutmut_11, 
    'x_parse_float_with_validation__mutmut_12': x_parse_float_with_validation__mutmut_12, 
    'x_parse_float_with_validation__mutmut_13': x_parse_float_with_validation__mutmut_13, 
    'x_parse_float_with_validation__mutmut_14': x_parse_float_with_validation__mutmut_14, 
    'x_parse_float_with_validation__mutmut_15': x_parse_float_with_validation__mutmut_15, 
    'x_parse_float_with_validation__mutmut_16': x_parse_float_with_validation__mutmut_16, 
    'x_parse_float_with_validation__mutmut_17': x_parse_float_with_validation__mutmut_17, 
    'x_parse_float_with_validation__mutmut_18': x_parse_float_with_validation__mutmut_18, 
    'x_parse_float_with_validation__mutmut_19': x_parse_float_with_validation__mutmut_19, 
    'x_parse_float_with_validation__mutmut_20': x_parse_float_with_validation__mutmut_20, 
    'x_parse_float_with_validation__mutmut_21': x_parse_float_with_validation__mutmut_21, 
    'x_parse_float_with_validation__mutmut_22': x_parse_float_with_validation__mutmut_22, 
    'x_parse_float_with_validation__mutmut_23': x_parse_float_with_validation__mutmut_23, 
    'x_parse_float_with_validation__mutmut_24': x_parse_float_with_validation__mutmut_24, 
    'x_parse_float_with_validation__mutmut_25': x_parse_float_with_validation__mutmut_25, 
    'x_parse_float_with_validation__mutmut_26': x_parse_float_with_validation__mutmut_26, 
    'x_parse_float_with_validation__mutmut_27': x_parse_float_with_validation__mutmut_27, 
    'x_parse_float_with_validation__mutmut_28': x_parse_float_with_validation__mutmut_28, 
    'x_parse_float_with_validation__mutmut_29': x_parse_float_with_validation__mutmut_29, 
    'x_parse_float_with_validation__mutmut_30': x_parse_float_with_validation__mutmut_30, 
    'x_parse_float_with_validation__mutmut_31': x_parse_float_with_validation__mutmut_31, 
    'x_parse_float_with_validation__mutmut_32': x_parse_float_with_validation__mutmut_32, 
    'x_parse_float_with_validation__mutmut_33': x_parse_float_with_validation__mutmut_33, 
    'x_parse_float_with_validation__mutmut_34': x_parse_float_with_validation__mutmut_34, 
    'x_parse_float_with_validation__mutmut_35': x_parse_float_with_validation__mutmut_35, 
    'x_parse_float_with_validation__mutmut_36': x_parse_float_with_validation__mutmut_36, 
    'x_parse_float_with_validation__mutmut_37': x_parse_float_with_validation__mutmut_37
}

def parse_float_with_validation(*args, **kwargs):
    result = _mutmut_trampoline(x_parse_float_with_validation__mutmut_orig, x_parse_float_with_validation__mutmut_mutants, args, kwargs)
    return result 

parse_float_with_validation.__signature__ = _mutmut_signature(x_parse_float_with_validation__mutmut_orig)
x_parse_float_with_validation__mutmut_orig.__name__ = 'x_parse_float_with_validation'


def x_parse_sample_rate__mutmut_orig(value: str) -> float:
    """Parse sampling rate (0.0 to 1.0).

    Args:
        value: String representation of sampling rate

    Returns:
        Float between 0.0 and 1.0

    Raises:
        ValueError: If value is not valid or out of range

    """
    return parse_float_with_validation(value, min_val=0.0, max_val=1.0)


def x_parse_sample_rate__mutmut_1(value: str) -> float:
    """Parse sampling rate (0.0 to 1.0).

    Args:
        value: String representation of sampling rate

    Returns:
        Float between 0.0 and 1.0

    Raises:
        ValueError: If value is not valid or out of range

    """
    return parse_float_with_validation(None, min_val=0.0, max_val=1.0)


def x_parse_sample_rate__mutmut_2(value: str) -> float:
    """Parse sampling rate (0.0 to 1.0).

    Args:
        value: String representation of sampling rate

    Returns:
        Float between 0.0 and 1.0

    Raises:
        ValueError: If value is not valid or out of range

    """
    return parse_float_with_validation(value, min_val=None, max_val=1.0)


def x_parse_sample_rate__mutmut_3(value: str) -> float:
    """Parse sampling rate (0.0 to 1.0).

    Args:
        value: String representation of sampling rate

    Returns:
        Float between 0.0 and 1.0

    Raises:
        ValueError: If value is not valid or out of range

    """
    return parse_float_with_validation(value, min_val=0.0, max_val=None)


def x_parse_sample_rate__mutmut_4(value: str) -> float:
    """Parse sampling rate (0.0 to 1.0).

    Args:
        value: String representation of sampling rate

    Returns:
        Float between 0.0 and 1.0

    Raises:
        ValueError: If value is not valid or out of range

    """
    return parse_float_with_validation(min_val=0.0, max_val=1.0)


def x_parse_sample_rate__mutmut_5(value: str) -> float:
    """Parse sampling rate (0.0 to 1.0).

    Args:
        value: String representation of sampling rate

    Returns:
        Float between 0.0 and 1.0

    Raises:
        ValueError: If value is not valid or out of range

    """
    return parse_float_with_validation(value, max_val=1.0)


def x_parse_sample_rate__mutmut_6(value: str) -> float:
    """Parse sampling rate (0.0 to 1.0).

    Args:
        value: String representation of sampling rate

    Returns:
        Float between 0.0 and 1.0

    Raises:
        ValueError: If value is not valid or out of range

    """
    return parse_float_with_validation(value, min_val=0.0, )


def x_parse_sample_rate__mutmut_7(value: str) -> float:
    """Parse sampling rate (0.0 to 1.0).

    Args:
        value: String representation of sampling rate

    Returns:
        Float between 0.0 and 1.0

    Raises:
        ValueError: If value is not valid or out of range

    """
    return parse_float_with_validation(value, min_val=1.0, max_val=1.0)


def x_parse_sample_rate__mutmut_8(value: str) -> float:
    """Parse sampling rate (0.0 to 1.0).

    Args:
        value: String representation of sampling rate

    Returns:
        Float between 0.0 and 1.0

    Raises:
        ValueError: If value is not valid or out of range

    """
    return parse_float_with_validation(value, min_val=0.0, max_val=2.0)

x_parse_sample_rate__mutmut_mutants : ClassVar[MutantDict] = {
'x_parse_sample_rate__mutmut_1': x_parse_sample_rate__mutmut_1, 
    'x_parse_sample_rate__mutmut_2': x_parse_sample_rate__mutmut_2, 
    'x_parse_sample_rate__mutmut_3': x_parse_sample_rate__mutmut_3, 
    'x_parse_sample_rate__mutmut_4': x_parse_sample_rate__mutmut_4, 
    'x_parse_sample_rate__mutmut_5': x_parse_sample_rate__mutmut_5, 
    'x_parse_sample_rate__mutmut_6': x_parse_sample_rate__mutmut_6, 
    'x_parse_sample_rate__mutmut_7': x_parse_sample_rate__mutmut_7, 
    'x_parse_sample_rate__mutmut_8': x_parse_sample_rate__mutmut_8
}

def parse_sample_rate(*args, **kwargs):
    result = _mutmut_trampoline(x_parse_sample_rate__mutmut_orig, x_parse_sample_rate__mutmut_mutants, args, kwargs)
    return result 

parse_sample_rate.__signature__ = _mutmut_signature(x_parse_sample_rate__mutmut_orig)
x_parse_sample_rate__mutmut_orig.__name__ = 'x_parse_sample_rate'


def x_parse_json_dict__mutmut_orig(value: str) -> dict[str, Any]:
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


def x_parse_json_dict__mutmut_1(value: str) -> dict[str, Any]:
    """Parse JSON string into dictionary.

    Args:
        value: JSON string

    Returns:
        Parsed dictionary

    Raises:
        ValueError: If JSON is invalid

    """
    if not value and not value.strip():
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


def x_parse_json_dict__mutmut_2(value: str) -> dict[str, Any]:
    """Parse JSON string into dictionary.

    Args:
        value: JSON string

    Returns:
        Parsed dictionary

    Raises:
        ValueError: If JSON is invalid

    """
    if value or not value.strip():
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


def x_parse_json_dict__mutmut_3(value: str) -> dict[str, Any]:
    """Parse JSON string into dictionary.

    Args:
        value: JSON string

    Returns:
        Parsed dictionary

    Raises:
        ValueError: If JSON is invalid

    """
    if not value or value.strip():
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


def x_parse_json_dict__mutmut_4(value: str) -> dict[str, Any]:
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
        result = None
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


def x_parse_json_dict__mutmut_5(value: str) -> dict[str, Any]:
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
        result = json_loads(None)
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


def x_parse_json_dict__mutmut_6(value: str) -> dict[str, Any]:
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
        if isinstance(result, dict):
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


def x_parse_json_dict__mutmut_7(value: str) -> dict[str, Any]:
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
                None,
            )
        return result
    except Exception as e:
        raise ValueError(
            _format_invalid_value_error("json_dict", value, expected_type="valid JSON"),
        ) from e


def x_parse_json_dict__mutmut_8(value: str) -> dict[str, Any]:
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
                    None,
                    type(result).__name__,
                    expected_type="JSON object",
                ),
            )
        return result
    except Exception as e:
        raise ValueError(
            _format_invalid_value_error("json_dict", value, expected_type="valid JSON"),
        ) from e


def x_parse_json_dict__mutmut_9(value: str) -> dict[str, Any]:
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
                    None,
                    expected_type="JSON object",
                ),
            )
        return result
    except Exception as e:
        raise ValueError(
            _format_invalid_value_error("json_dict", value, expected_type="valid JSON"),
        ) from e


def x_parse_json_dict__mutmut_10(value: str) -> dict[str, Any]:
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
                    expected_type=None,
                ),
            )
        return result
    except Exception as e:
        raise ValueError(
            _format_invalid_value_error("json_dict", value, expected_type="valid JSON"),
        ) from e


def x_parse_json_dict__mutmut_11(value: str) -> dict[str, Any]:
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
                    type(result).__name__,
                    expected_type="JSON object",
                ),
            )
        return result
    except Exception as e:
        raise ValueError(
            _format_invalid_value_error("json_dict", value, expected_type="valid JSON"),
        ) from e


def x_parse_json_dict__mutmut_12(value: str) -> dict[str, Any]:
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
                    expected_type="JSON object",
                ),
            )
        return result
    except Exception as e:
        raise ValueError(
            _format_invalid_value_error("json_dict", value, expected_type="valid JSON"),
        ) from e


def x_parse_json_dict__mutmut_13(value: str) -> dict[str, Any]:
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
                    ),
            )
        return result
    except Exception as e:
        raise ValueError(
            _format_invalid_value_error("json_dict", value, expected_type="valid JSON"),
        ) from e


def x_parse_json_dict__mutmut_14(value: str) -> dict[str, Any]:
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
                    "XXjson_dictXX",
                    type(result).__name__,
                    expected_type="JSON object",
                ),
            )
        return result
    except Exception as e:
        raise ValueError(
            _format_invalid_value_error("json_dict", value, expected_type="valid JSON"),
        ) from e


def x_parse_json_dict__mutmut_15(value: str) -> dict[str, Any]:
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
                    "JSON_DICT",
                    type(result).__name__,
                    expected_type="JSON object",
                ),
            )
        return result
    except Exception as e:
        raise ValueError(
            _format_invalid_value_error("json_dict", value, expected_type="valid JSON"),
        ) from e


def x_parse_json_dict__mutmut_16(value: str) -> dict[str, Any]:
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
                    type(None).__name__,
                    expected_type="JSON object",
                ),
            )
        return result
    except Exception as e:
        raise ValueError(
            _format_invalid_value_error("json_dict", value, expected_type="valid JSON"),
        ) from e


def x_parse_json_dict__mutmut_17(value: str) -> dict[str, Any]:
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
                    expected_type="XXJSON objectXX",
                ),
            )
        return result
    except Exception as e:
        raise ValueError(
            _format_invalid_value_error("json_dict", value, expected_type="valid JSON"),
        ) from e


def x_parse_json_dict__mutmut_18(value: str) -> dict[str, Any]:
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
                    expected_type="json object",
                ),
            )
        return result
    except Exception as e:
        raise ValueError(
            _format_invalid_value_error("json_dict", value, expected_type="valid JSON"),
        ) from e


def x_parse_json_dict__mutmut_19(value: str) -> dict[str, Any]:
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
                    expected_type="JSON OBJECT",
                ),
            )
        return result
    except Exception as e:
        raise ValueError(
            _format_invalid_value_error("json_dict", value, expected_type="valid JSON"),
        ) from e


def x_parse_json_dict__mutmut_20(value: str) -> dict[str, Any]:
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
            None,
        ) from e


def x_parse_json_dict__mutmut_21(value: str) -> dict[str, Any]:
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
            _format_invalid_value_error(None, value, expected_type="valid JSON"),
        ) from e


def x_parse_json_dict__mutmut_22(value: str) -> dict[str, Any]:
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
            _format_invalid_value_error("json_dict", None, expected_type="valid JSON"),
        ) from e


def x_parse_json_dict__mutmut_23(value: str) -> dict[str, Any]:
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
            _format_invalid_value_error("json_dict", value, expected_type=None),
        ) from e


def x_parse_json_dict__mutmut_24(value: str) -> dict[str, Any]:
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
            _format_invalid_value_error(value, expected_type="valid JSON"),
        ) from e


def x_parse_json_dict__mutmut_25(value: str) -> dict[str, Any]:
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
            _format_invalid_value_error("json_dict", expected_type="valid JSON"),
        ) from e


def x_parse_json_dict__mutmut_26(value: str) -> dict[str, Any]:
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
            _format_invalid_value_error("json_dict", value, ),
        ) from e


def x_parse_json_dict__mutmut_27(value: str) -> dict[str, Any]:
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
            _format_invalid_value_error("XXjson_dictXX", value, expected_type="valid JSON"),
        ) from e


def x_parse_json_dict__mutmut_28(value: str) -> dict[str, Any]:
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
            _format_invalid_value_error("JSON_DICT", value, expected_type="valid JSON"),
        ) from e


def x_parse_json_dict__mutmut_29(value: str) -> dict[str, Any]:
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
            _format_invalid_value_error("json_dict", value, expected_type="XXvalid JSONXX"),
        ) from e


def x_parse_json_dict__mutmut_30(value: str) -> dict[str, Any]:
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
            _format_invalid_value_error("json_dict", value, expected_type="valid json"),
        ) from e


def x_parse_json_dict__mutmut_31(value: str) -> dict[str, Any]:
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
            _format_invalid_value_error("json_dict", value, expected_type="VALID JSON"),
        ) from e

x_parse_json_dict__mutmut_mutants : ClassVar[MutantDict] = {
'x_parse_json_dict__mutmut_1': x_parse_json_dict__mutmut_1, 
    'x_parse_json_dict__mutmut_2': x_parse_json_dict__mutmut_2, 
    'x_parse_json_dict__mutmut_3': x_parse_json_dict__mutmut_3, 
    'x_parse_json_dict__mutmut_4': x_parse_json_dict__mutmut_4, 
    'x_parse_json_dict__mutmut_5': x_parse_json_dict__mutmut_5, 
    'x_parse_json_dict__mutmut_6': x_parse_json_dict__mutmut_6, 
    'x_parse_json_dict__mutmut_7': x_parse_json_dict__mutmut_7, 
    'x_parse_json_dict__mutmut_8': x_parse_json_dict__mutmut_8, 
    'x_parse_json_dict__mutmut_9': x_parse_json_dict__mutmut_9, 
    'x_parse_json_dict__mutmut_10': x_parse_json_dict__mutmut_10, 
    'x_parse_json_dict__mutmut_11': x_parse_json_dict__mutmut_11, 
    'x_parse_json_dict__mutmut_12': x_parse_json_dict__mutmut_12, 
    'x_parse_json_dict__mutmut_13': x_parse_json_dict__mutmut_13, 
    'x_parse_json_dict__mutmut_14': x_parse_json_dict__mutmut_14, 
    'x_parse_json_dict__mutmut_15': x_parse_json_dict__mutmut_15, 
    'x_parse_json_dict__mutmut_16': x_parse_json_dict__mutmut_16, 
    'x_parse_json_dict__mutmut_17': x_parse_json_dict__mutmut_17, 
    'x_parse_json_dict__mutmut_18': x_parse_json_dict__mutmut_18, 
    'x_parse_json_dict__mutmut_19': x_parse_json_dict__mutmut_19, 
    'x_parse_json_dict__mutmut_20': x_parse_json_dict__mutmut_20, 
    'x_parse_json_dict__mutmut_21': x_parse_json_dict__mutmut_21, 
    'x_parse_json_dict__mutmut_22': x_parse_json_dict__mutmut_22, 
    'x_parse_json_dict__mutmut_23': x_parse_json_dict__mutmut_23, 
    'x_parse_json_dict__mutmut_24': x_parse_json_dict__mutmut_24, 
    'x_parse_json_dict__mutmut_25': x_parse_json_dict__mutmut_25, 
    'x_parse_json_dict__mutmut_26': x_parse_json_dict__mutmut_26, 
    'x_parse_json_dict__mutmut_27': x_parse_json_dict__mutmut_27, 
    'x_parse_json_dict__mutmut_28': x_parse_json_dict__mutmut_28, 
    'x_parse_json_dict__mutmut_29': x_parse_json_dict__mutmut_29, 
    'x_parse_json_dict__mutmut_30': x_parse_json_dict__mutmut_30, 
    'x_parse_json_dict__mutmut_31': x_parse_json_dict__mutmut_31
}

def parse_json_dict(*args, **kwargs):
    result = _mutmut_trampoline(x_parse_json_dict__mutmut_orig, x_parse_json_dict__mutmut_mutants, args, kwargs)
    return result 

parse_json_dict.__signature__ = _mutmut_signature(x_parse_json_dict__mutmut_orig)
x_parse_json_dict__mutmut_orig.__name__ = 'x_parse_json_dict'


def x_parse_json_list__mutmut_orig(value: str) -> list[Any]:
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


def x_parse_json_list__mutmut_1(value: str) -> list[Any]:
    """Parse JSON string into list.

    Args:
        value: JSON string

    Returns:
        Parsed list

    Raises:
        ValueError: If JSON is invalid

    """
    if not value and not value.strip():
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


def x_parse_json_list__mutmut_2(value: str) -> list[Any]:
    """Parse JSON string into list.

    Args:
        value: JSON string

    Returns:
        Parsed list

    Raises:
        ValueError: If JSON is invalid

    """
    if value or not value.strip():
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


def x_parse_json_list__mutmut_3(value: str) -> list[Any]:
    """Parse JSON string into list.

    Args:
        value: JSON string

    Returns:
        Parsed list

    Raises:
        ValueError: If JSON is invalid

    """
    if not value or value.strip():
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


def x_parse_json_list__mutmut_4(value: str) -> list[Any]:
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
        result = None
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


def x_parse_json_list__mutmut_5(value: str) -> list[Any]:
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
        result = json_loads(None)
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


def x_parse_json_list__mutmut_6(value: str) -> list[Any]:
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
        if isinstance(result, list):
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


def x_parse_json_list__mutmut_7(value: str) -> list[Any]:
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
                None,
            )
        return result
    except Exception as e:
        raise ValueError(
            _format_invalid_value_error("json_list", value, expected_type="valid JSON"),
        ) from e


def x_parse_json_list__mutmut_8(value: str) -> list[Any]:
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
                    None,
                    type(result).__name__,
                    expected_type="JSON array",
                ),
            )
        return result
    except Exception as e:
        raise ValueError(
            _format_invalid_value_error("json_list", value, expected_type="valid JSON"),
        ) from e


def x_parse_json_list__mutmut_9(value: str) -> list[Any]:
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
                    None,
                    expected_type="JSON array",
                ),
            )
        return result
    except Exception as e:
        raise ValueError(
            _format_invalid_value_error("json_list", value, expected_type="valid JSON"),
        ) from e


def x_parse_json_list__mutmut_10(value: str) -> list[Any]:
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
                    expected_type=None,
                ),
            )
        return result
    except Exception as e:
        raise ValueError(
            _format_invalid_value_error("json_list", value, expected_type="valid JSON"),
        ) from e


def x_parse_json_list__mutmut_11(value: str) -> list[Any]:
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
                    type(result).__name__,
                    expected_type="JSON array",
                ),
            )
        return result
    except Exception as e:
        raise ValueError(
            _format_invalid_value_error("json_list", value, expected_type="valid JSON"),
        ) from e


def x_parse_json_list__mutmut_12(value: str) -> list[Any]:
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
                    expected_type="JSON array",
                ),
            )
        return result
    except Exception as e:
        raise ValueError(
            _format_invalid_value_error("json_list", value, expected_type="valid JSON"),
        ) from e


def x_parse_json_list__mutmut_13(value: str) -> list[Any]:
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
                    ),
            )
        return result
    except Exception as e:
        raise ValueError(
            _format_invalid_value_error("json_list", value, expected_type="valid JSON"),
        ) from e


def x_parse_json_list__mutmut_14(value: str) -> list[Any]:
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
                    "XXjson_listXX",
                    type(result).__name__,
                    expected_type="JSON array",
                ),
            )
        return result
    except Exception as e:
        raise ValueError(
            _format_invalid_value_error("json_list", value, expected_type="valid JSON"),
        ) from e


def x_parse_json_list__mutmut_15(value: str) -> list[Any]:
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
                    "JSON_LIST",
                    type(result).__name__,
                    expected_type="JSON array",
                ),
            )
        return result
    except Exception as e:
        raise ValueError(
            _format_invalid_value_error("json_list", value, expected_type="valid JSON"),
        ) from e


def x_parse_json_list__mutmut_16(value: str) -> list[Any]:
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
                    type(None).__name__,
                    expected_type="JSON array",
                ),
            )
        return result
    except Exception as e:
        raise ValueError(
            _format_invalid_value_error("json_list", value, expected_type="valid JSON"),
        ) from e


def x_parse_json_list__mutmut_17(value: str) -> list[Any]:
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
                    expected_type="XXJSON arrayXX",
                ),
            )
        return result
    except Exception as e:
        raise ValueError(
            _format_invalid_value_error("json_list", value, expected_type="valid JSON"),
        ) from e


def x_parse_json_list__mutmut_18(value: str) -> list[Any]:
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
                    expected_type="json array",
                ),
            )
        return result
    except Exception as e:
        raise ValueError(
            _format_invalid_value_error("json_list", value, expected_type="valid JSON"),
        ) from e


def x_parse_json_list__mutmut_19(value: str) -> list[Any]:
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
                    expected_type="JSON ARRAY",
                ),
            )
        return result
    except Exception as e:
        raise ValueError(
            _format_invalid_value_error("json_list", value, expected_type="valid JSON"),
        ) from e


def x_parse_json_list__mutmut_20(value: str) -> list[Any]:
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
            None,
        ) from e


def x_parse_json_list__mutmut_21(value: str) -> list[Any]:
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
            _format_invalid_value_error(None, value, expected_type="valid JSON"),
        ) from e


def x_parse_json_list__mutmut_22(value: str) -> list[Any]:
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
            _format_invalid_value_error("json_list", None, expected_type="valid JSON"),
        ) from e


def x_parse_json_list__mutmut_23(value: str) -> list[Any]:
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
            _format_invalid_value_error("json_list", value, expected_type=None),
        ) from e


def x_parse_json_list__mutmut_24(value: str) -> list[Any]:
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
            _format_invalid_value_error(value, expected_type="valid JSON"),
        ) from e


def x_parse_json_list__mutmut_25(value: str) -> list[Any]:
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
            _format_invalid_value_error("json_list", expected_type="valid JSON"),
        ) from e


def x_parse_json_list__mutmut_26(value: str) -> list[Any]:
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
            _format_invalid_value_error("json_list", value, ),
        ) from e


def x_parse_json_list__mutmut_27(value: str) -> list[Any]:
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
            _format_invalid_value_error("XXjson_listXX", value, expected_type="valid JSON"),
        ) from e


def x_parse_json_list__mutmut_28(value: str) -> list[Any]:
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
            _format_invalid_value_error("JSON_LIST", value, expected_type="valid JSON"),
        ) from e


def x_parse_json_list__mutmut_29(value: str) -> list[Any]:
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
            _format_invalid_value_error("json_list", value, expected_type="XXvalid JSONXX"),
        ) from e


def x_parse_json_list__mutmut_30(value: str) -> list[Any]:
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
            _format_invalid_value_error("json_list", value, expected_type="valid json"),
        ) from e


def x_parse_json_list__mutmut_31(value: str) -> list[Any]:
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
            _format_invalid_value_error("json_list", value, expected_type="VALID JSON"),
        ) from e

x_parse_json_list__mutmut_mutants : ClassVar[MutantDict] = {
'x_parse_json_list__mutmut_1': x_parse_json_list__mutmut_1, 
    'x_parse_json_list__mutmut_2': x_parse_json_list__mutmut_2, 
    'x_parse_json_list__mutmut_3': x_parse_json_list__mutmut_3, 
    'x_parse_json_list__mutmut_4': x_parse_json_list__mutmut_4, 
    'x_parse_json_list__mutmut_5': x_parse_json_list__mutmut_5, 
    'x_parse_json_list__mutmut_6': x_parse_json_list__mutmut_6, 
    'x_parse_json_list__mutmut_7': x_parse_json_list__mutmut_7, 
    'x_parse_json_list__mutmut_8': x_parse_json_list__mutmut_8, 
    'x_parse_json_list__mutmut_9': x_parse_json_list__mutmut_9, 
    'x_parse_json_list__mutmut_10': x_parse_json_list__mutmut_10, 
    'x_parse_json_list__mutmut_11': x_parse_json_list__mutmut_11, 
    'x_parse_json_list__mutmut_12': x_parse_json_list__mutmut_12, 
    'x_parse_json_list__mutmut_13': x_parse_json_list__mutmut_13, 
    'x_parse_json_list__mutmut_14': x_parse_json_list__mutmut_14, 
    'x_parse_json_list__mutmut_15': x_parse_json_list__mutmut_15, 
    'x_parse_json_list__mutmut_16': x_parse_json_list__mutmut_16, 
    'x_parse_json_list__mutmut_17': x_parse_json_list__mutmut_17, 
    'x_parse_json_list__mutmut_18': x_parse_json_list__mutmut_18, 
    'x_parse_json_list__mutmut_19': x_parse_json_list__mutmut_19, 
    'x_parse_json_list__mutmut_20': x_parse_json_list__mutmut_20, 
    'x_parse_json_list__mutmut_21': x_parse_json_list__mutmut_21, 
    'x_parse_json_list__mutmut_22': x_parse_json_list__mutmut_22, 
    'x_parse_json_list__mutmut_23': x_parse_json_list__mutmut_23, 
    'x_parse_json_list__mutmut_24': x_parse_json_list__mutmut_24, 
    'x_parse_json_list__mutmut_25': x_parse_json_list__mutmut_25, 
    'x_parse_json_list__mutmut_26': x_parse_json_list__mutmut_26, 
    'x_parse_json_list__mutmut_27': x_parse_json_list__mutmut_27, 
    'x_parse_json_list__mutmut_28': x_parse_json_list__mutmut_28, 
    'x_parse_json_list__mutmut_29': x_parse_json_list__mutmut_29, 
    'x_parse_json_list__mutmut_30': x_parse_json_list__mutmut_30, 
    'x_parse_json_list__mutmut_31': x_parse_json_list__mutmut_31
}

def parse_json_list(*args, **kwargs):
    result = _mutmut_trampoline(x_parse_json_list__mutmut_orig, x_parse_json_list__mutmut_mutants, args, kwargs)
    return result 

parse_json_list.__signature__ = _mutmut_signature(x_parse_json_list__mutmut_orig)
x_parse_json_list__mutmut_orig.__name__ = 'x_parse_json_list'


__all__ = [
    "parse_bool",
    "parse_bool_extended",
    "parse_bool_strict",
    "parse_float_with_validation",
    "parse_json_dict",
    "parse_json_list",
    "parse_sample_rate",
]


# <3 🧱🤝🧩🪄
