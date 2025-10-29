# provide/foundation/parsers/errors.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

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
from inspect import signature as _mutmut_signature
from typing import Annotated
from typing import Callable
from typing import ClassVar


MutantDict = Annotated[dict[str, Callable], "Mutant"]


def _mutmut_trampoline(orig, mutants, call_args, call_kwargs, self_arg=None):
    """Forward call to original or mutated function, depending on the environment"""
    import os

    mutant_under_test = os.environ["MUTANT_UNDER_TEST"]
    if mutant_under_test == "fail":
        from mutmut.__main__ import MutmutProgrammaticFailException

        raise MutmutProgrammaticFailException("Failed programmatically")
    elif mutant_under_test == "stats":
        from mutmut.__main__ import record_trampoline_hit

        record_trampoline_hit(orig.__module__ + "." + orig.__name__)
        result = orig(*call_args, **call_kwargs)
        return result
    prefix = orig.__module__ + "." + orig.__name__ + "__mutmut_"
    if not mutant_under_test.startswith(prefix):
        result = orig(*call_args, **call_kwargs)
        return result
    mutant_name = mutant_under_test.rpartition(".")[-1]
    if self_arg:
        # call to a class method where self is not bound
        result = mutants[mutant_name](self_arg, *call_args, **call_kwargs)
    else:
        result = mutants[mutant_name](*call_args, **call_kwargs)
    return result


# Standardized error message formatting utilities


def x__format_invalid_value_error__mutmut_orig(
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


# Standardized error message formatting utilities


def x__format_invalid_value_error__mutmut_1(
    field_name: str,
    value: Any,
    valid_options: list[str] | None = None,
    expected_type: str | None = None,
    additional_info: str | None = None,
) -> str:
    """Create standardized invalid value error message."""
    parts = None

    if valid_options:
        parts.append(f"Valid options: {', '.join(valid_options)}")
    elif expected_type:
        parts.append(f"Expected: {expected_type}")

    if additional_info:
        parts.append(additional_info)

    return " ".join(parts)


# Standardized error message formatting utilities


def x__format_invalid_value_error__mutmut_2(
    field_name: str,
    value: Any,
    valid_options: list[str] | None = None,
    expected_type: str | None = None,
    additional_info: str | None = None,
) -> str:
    """Create standardized invalid value error message."""
    parts = [f"Invalid {field_name} '{value}'."]

    if valid_options:
        parts.append(None)
    elif expected_type:
        parts.append(f"Expected: {expected_type}")

    if additional_info:
        parts.append(additional_info)

    return " ".join(parts)


# Standardized error message formatting utilities


def x__format_invalid_value_error__mutmut_3(
    field_name: str,
    value: Any,
    valid_options: list[str] | None = None,
    expected_type: str | None = None,
    additional_info: str | None = None,
) -> str:
    """Create standardized invalid value error message."""
    parts = [f"Invalid {field_name} '{value}'."]

    if valid_options:
        parts.append(f"Valid options: {', '.join(None)}")
    elif expected_type:
        parts.append(f"Expected: {expected_type}")

    if additional_info:
        parts.append(additional_info)

    return " ".join(parts)


# Standardized error message formatting utilities


def x__format_invalid_value_error__mutmut_4(
    field_name: str,
    value: Any,
    valid_options: list[str] | None = None,
    expected_type: str | None = None,
    additional_info: str | None = None,
) -> str:
    """Create standardized invalid value error message."""
    parts = [f"Invalid {field_name} '{value}'."]

    if valid_options:
        parts.append(f"Valid options: {'XX, XX'.join(valid_options)}")
    elif expected_type:
        parts.append(f"Expected: {expected_type}")

    if additional_info:
        parts.append(additional_info)

    return " ".join(parts)


# Standardized error message formatting utilities


def x__format_invalid_value_error__mutmut_5(
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
        parts.append(None)

    if additional_info:
        parts.append(additional_info)

    return " ".join(parts)


# Standardized error message formatting utilities


def x__format_invalid_value_error__mutmut_6(
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
        parts.append(None)

    return " ".join(parts)


# Standardized error message formatting utilities


def x__format_invalid_value_error__mutmut_7(
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

    return " ".join(None)


# Standardized error message formatting utilities


def x__format_invalid_value_error__mutmut_8(
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

    return "XX XX".join(parts)


x__format_invalid_value_error__mutmut_mutants: ClassVar[MutantDict] = {
    "x__format_invalid_value_error__mutmut_1": x__format_invalid_value_error__mutmut_1,
    "x__format_invalid_value_error__mutmut_2": x__format_invalid_value_error__mutmut_2,
    "x__format_invalid_value_error__mutmut_3": x__format_invalid_value_error__mutmut_3,
    "x__format_invalid_value_error__mutmut_4": x__format_invalid_value_error__mutmut_4,
    "x__format_invalid_value_error__mutmut_5": x__format_invalid_value_error__mutmut_5,
    "x__format_invalid_value_error__mutmut_6": x__format_invalid_value_error__mutmut_6,
    "x__format_invalid_value_error__mutmut_7": x__format_invalid_value_error__mutmut_7,
    "x__format_invalid_value_error__mutmut_8": x__format_invalid_value_error__mutmut_8,
}


def _format_invalid_value_error(*args, **kwargs):
    result = _mutmut_trampoline(
        x__format_invalid_value_error__mutmut_orig, x__format_invalid_value_error__mutmut_mutants, args, kwargs
    )
    return result


_format_invalid_value_error.__signature__ = _mutmut_signature(x__format_invalid_value_error__mutmut_orig)
x__format_invalid_value_error__mutmut_orig.__name__ = "x__format_invalid_value_error"


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


# <3 🧱🤝🧩🪄
