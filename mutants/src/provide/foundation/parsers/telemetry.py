# provide/foundation/parsers/telemetry.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

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


def x_parse_log_level__mutmut_orig(value: str) -> LogLevelStr:
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


def x_parse_log_level__mutmut_1(value: str) -> LogLevelStr:
    """Parse and validate log level string.

    Args:
        value: Log level string (case-insensitive)

    Returns:
        Valid log level string in uppercase

    Raises:
        ValueError: If the log level is invalid

    """
    level = None
    if level not in _VALID_LOG_LEVEL_TUPLE:
        raise ValueError(
            _format_invalid_value_error(
                "log_level",
                value,
                valid_options=list(_VALID_LOG_LEVEL_TUPLE),
            ),
        )
    return cast("LogLevelStr", level)


def x_parse_log_level__mutmut_2(value: str) -> LogLevelStr:
    """Parse and validate log level string.

    Args:
        value: Log level string (case-insensitive)

    Returns:
        Valid log level string in uppercase

    Raises:
        ValueError: If the log level is invalid

    """
    level = value.lower()
    if level not in _VALID_LOG_LEVEL_TUPLE:
        raise ValueError(
            _format_invalid_value_error(
                "log_level",
                value,
                valid_options=list(_VALID_LOG_LEVEL_TUPLE),
            ),
        )
    return cast("LogLevelStr", level)


def x_parse_log_level__mutmut_3(value: str) -> LogLevelStr:
    """Parse and validate log level string.

    Args:
        value: Log level string (case-insensitive)

    Returns:
        Valid log level string in uppercase

    Raises:
        ValueError: If the log level is invalid

    """
    level = value.upper()
    if level in _VALID_LOG_LEVEL_TUPLE:
        raise ValueError(
            _format_invalid_value_error(
                "log_level",
                value,
                valid_options=list(_VALID_LOG_LEVEL_TUPLE),
            ),
        )
    return cast("LogLevelStr", level)


def x_parse_log_level__mutmut_4(value: str) -> LogLevelStr:
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
            None,
        )
    return cast("LogLevelStr", level)


def x_parse_log_level__mutmut_5(value: str) -> LogLevelStr:
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
                None,
                value,
                valid_options=list(_VALID_LOG_LEVEL_TUPLE),
            ),
        )
    return cast("LogLevelStr", level)


def x_parse_log_level__mutmut_6(value: str) -> LogLevelStr:
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
                None,
                valid_options=list(_VALID_LOG_LEVEL_TUPLE),
            ),
        )
    return cast("LogLevelStr", level)


def x_parse_log_level__mutmut_7(value: str) -> LogLevelStr:
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
                valid_options=None,
            ),
        )
    return cast("LogLevelStr", level)


def x_parse_log_level__mutmut_8(value: str) -> LogLevelStr:
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
                value,
                valid_options=list(_VALID_LOG_LEVEL_TUPLE),
            ),
        )
    return cast("LogLevelStr", level)


def x_parse_log_level__mutmut_9(value: str) -> LogLevelStr:
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
                valid_options=list(_VALID_LOG_LEVEL_TUPLE),
            ),
        )
    return cast("LogLevelStr", level)


def x_parse_log_level__mutmut_10(value: str) -> LogLevelStr:
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
            ),
        )
    return cast("LogLevelStr", level)


def x_parse_log_level__mutmut_11(value: str) -> LogLevelStr:
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
                "XXlog_levelXX",
                value,
                valid_options=list(_VALID_LOG_LEVEL_TUPLE),
            ),
        )
    return cast("LogLevelStr", level)


def x_parse_log_level__mutmut_12(value: str) -> LogLevelStr:
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
                "LOG_LEVEL",
                value,
                valid_options=list(_VALID_LOG_LEVEL_TUPLE),
            ),
        )
    return cast("LogLevelStr", level)


def x_parse_log_level__mutmut_13(value: str) -> LogLevelStr:
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
                valid_options=list(None),
            ),
        )
    return cast("LogLevelStr", level)


def x_parse_log_level__mutmut_14(value: str) -> LogLevelStr:
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
    return cast(None, level)


def x_parse_log_level__mutmut_15(value: str) -> LogLevelStr:
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
    return cast("LogLevelStr", None)


def x_parse_log_level__mutmut_16(value: str) -> LogLevelStr:
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
    return cast(level)


def x_parse_log_level__mutmut_17(value: str) -> LogLevelStr:
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
    return cast(
        "LogLevelStr",
    )


def x_parse_log_level__mutmut_18(value: str) -> LogLevelStr:
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
    return cast("XXLogLevelStrXX", level)


def x_parse_log_level__mutmut_19(value: str) -> LogLevelStr:
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
    return cast("loglevelstr", level)


def x_parse_log_level__mutmut_20(value: str) -> LogLevelStr:
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
    return cast("LOGLEVELSTR", level)


x_parse_log_level__mutmut_mutants: ClassVar[MutantDict] = {
    "x_parse_log_level__mutmut_1": x_parse_log_level__mutmut_1,
    "x_parse_log_level__mutmut_2": x_parse_log_level__mutmut_2,
    "x_parse_log_level__mutmut_3": x_parse_log_level__mutmut_3,
    "x_parse_log_level__mutmut_4": x_parse_log_level__mutmut_4,
    "x_parse_log_level__mutmut_5": x_parse_log_level__mutmut_5,
    "x_parse_log_level__mutmut_6": x_parse_log_level__mutmut_6,
    "x_parse_log_level__mutmut_7": x_parse_log_level__mutmut_7,
    "x_parse_log_level__mutmut_8": x_parse_log_level__mutmut_8,
    "x_parse_log_level__mutmut_9": x_parse_log_level__mutmut_9,
    "x_parse_log_level__mutmut_10": x_parse_log_level__mutmut_10,
    "x_parse_log_level__mutmut_11": x_parse_log_level__mutmut_11,
    "x_parse_log_level__mutmut_12": x_parse_log_level__mutmut_12,
    "x_parse_log_level__mutmut_13": x_parse_log_level__mutmut_13,
    "x_parse_log_level__mutmut_14": x_parse_log_level__mutmut_14,
    "x_parse_log_level__mutmut_15": x_parse_log_level__mutmut_15,
    "x_parse_log_level__mutmut_16": x_parse_log_level__mutmut_16,
    "x_parse_log_level__mutmut_17": x_parse_log_level__mutmut_17,
    "x_parse_log_level__mutmut_18": x_parse_log_level__mutmut_18,
    "x_parse_log_level__mutmut_19": x_parse_log_level__mutmut_19,
    "x_parse_log_level__mutmut_20": x_parse_log_level__mutmut_20,
}


def parse_log_level(*args, **kwargs):
    result = _mutmut_trampoline(
        x_parse_log_level__mutmut_orig, x_parse_log_level__mutmut_mutants, args, kwargs
    )
    return result


parse_log_level.__signature__ = _mutmut_signature(x_parse_log_level__mutmut_orig)
x_parse_log_level__mutmut_orig.__name__ = "x_parse_log_level"


def x_parse_console_formatter__mutmut_orig(value: str) -> ConsoleFormatterStr:
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


def x_parse_console_formatter__mutmut_1(value: str) -> ConsoleFormatterStr:
    """Parse and validate console formatter string.

    Args:
        value: Formatter string (case-insensitive)

    Returns:
        Valid formatter string in lowercase

    Raises:
        ValueError: If the formatter is invalid

    """
    formatter = None
    if formatter not in _VALID_FORMATTER_TUPLE:
        raise ValueError(
            _format_invalid_value_error(
                "console_formatter",
                value,
                valid_options=list(_VALID_FORMATTER_TUPLE),
            ),
        )
    return cast("ConsoleFormatterStr", formatter)


def x_parse_console_formatter__mutmut_2(value: str) -> ConsoleFormatterStr:
    """Parse and validate console formatter string.

    Args:
        value: Formatter string (case-insensitive)

    Returns:
        Valid formatter string in lowercase

    Raises:
        ValueError: If the formatter is invalid

    """
    formatter = value.upper()
    if formatter not in _VALID_FORMATTER_TUPLE:
        raise ValueError(
            _format_invalid_value_error(
                "console_formatter",
                value,
                valid_options=list(_VALID_FORMATTER_TUPLE),
            ),
        )
    return cast("ConsoleFormatterStr", formatter)


def x_parse_console_formatter__mutmut_3(value: str) -> ConsoleFormatterStr:
    """Parse and validate console formatter string.

    Args:
        value: Formatter string (case-insensitive)

    Returns:
        Valid formatter string in lowercase

    Raises:
        ValueError: If the formatter is invalid

    """
    formatter = value.lower()
    if formatter in _VALID_FORMATTER_TUPLE:
        raise ValueError(
            _format_invalid_value_error(
                "console_formatter",
                value,
                valid_options=list(_VALID_FORMATTER_TUPLE),
            ),
        )
    return cast("ConsoleFormatterStr", formatter)


def x_parse_console_formatter__mutmut_4(value: str) -> ConsoleFormatterStr:
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
            None,
        )
    return cast("ConsoleFormatterStr", formatter)


def x_parse_console_formatter__mutmut_5(value: str) -> ConsoleFormatterStr:
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
                None,
                value,
                valid_options=list(_VALID_FORMATTER_TUPLE),
            ),
        )
    return cast("ConsoleFormatterStr", formatter)


def x_parse_console_formatter__mutmut_6(value: str) -> ConsoleFormatterStr:
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
                None,
                valid_options=list(_VALID_FORMATTER_TUPLE),
            ),
        )
    return cast("ConsoleFormatterStr", formatter)


def x_parse_console_formatter__mutmut_7(value: str) -> ConsoleFormatterStr:
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
                valid_options=None,
            ),
        )
    return cast("ConsoleFormatterStr", formatter)


def x_parse_console_formatter__mutmut_8(value: str) -> ConsoleFormatterStr:
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
                value,
                valid_options=list(_VALID_FORMATTER_TUPLE),
            ),
        )
    return cast("ConsoleFormatterStr", formatter)


def x_parse_console_formatter__mutmut_9(value: str) -> ConsoleFormatterStr:
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
                valid_options=list(_VALID_FORMATTER_TUPLE),
            ),
        )
    return cast("ConsoleFormatterStr", formatter)


def x_parse_console_formatter__mutmut_10(value: str) -> ConsoleFormatterStr:
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
            ),
        )
    return cast("ConsoleFormatterStr", formatter)


def x_parse_console_formatter__mutmut_11(value: str) -> ConsoleFormatterStr:
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
                "XXconsole_formatterXX",
                value,
                valid_options=list(_VALID_FORMATTER_TUPLE),
            ),
        )
    return cast("ConsoleFormatterStr", formatter)


def x_parse_console_formatter__mutmut_12(value: str) -> ConsoleFormatterStr:
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
                "CONSOLE_FORMATTER",
                value,
                valid_options=list(_VALID_FORMATTER_TUPLE),
            ),
        )
    return cast("ConsoleFormatterStr", formatter)


def x_parse_console_formatter__mutmut_13(value: str) -> ConsoleFormatterStr:
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
                valid_options=list(None),
            ),
        )
    return cast("ConsoleFormatterStr", formatter)


def x_parse_console_formatter__mutmut_14(value: str) -> ConsoleFormatterStr:
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
    return cast(None, formatter)


def x_parse_console_formatter__mutmut_15(value: str) -> ConsoleFormatterStr:
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
    return cast("ConsoleFormatterStr", None)


def x_parse_console_formatter__mutmut_16(value: str) -> ConsoleFormatterStr:
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
    return cast(formatter)


def x_parse_console_formatter__mutmut_17(value: str) -> ConsoleFormatterStr:
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
    return cast(
        "ConsoleFormatterStr",
    )


def x_parse_console_formatter__mutmut_18(value: str) -> ConsoleFormatterStr:
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
    return cast("XXConsoleFormatterStrXX", formatter)


def x_parse_console_formatter__mutmut_19(value: str) -> ConsoleFormatterStr:
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
    return cast("consoleformatterstr", formatter)


def x_parse_console_formatter__mutmut_20(value: str) -> ConsoleFormatterStr:
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
    return cast("CONSOLEFORMATTERSTR", formatter)


x_parse_console_formatter__mutmut_mutants: ClassVar[MutantDict] = {
    "x_parse_console_formatter__mutmut_1": x_parse_console_formatter__mutmut_1,
    "x_parse_console_formatter__mutmut_2": x_parse_console_formatter__mutmut_2,
    "x_parse_console_formatter__mutmut_3": x_parse_console_formatter__mutmut_3,
    "x_parse_console_formatter__mutmut_4": x_parse_console_formatter__mutmut_4,
    "x_parse_console_formatter__mutmut_5": x_parse_console_formatter__mutmut_5,
    "x_parse_console_formatter__mutmut_6": x_parse_console_formatter__mutmut_6,
    "x_parse_console_formatter__mutmut_7": x_parse_console_formatter__mutmut_7,
    "x_parse_console_formatter__mutmut_8": x_parse_console_formatter__mutmut_8,
    "x_parse_console_formatter__mutmut_9": x_parse_console_formatter__mutmut_9,
    "x_parse_console_formatter__mutmut_10": x_parse_console_formatter__mutmut_10,
    "x_parse_console_formatter__mutmut_11": x_parse_console_formatter__mutmut_11,
    "x_parse_console_formatter__mutmut_12": x_parse_console_formatter__mutmut_12,
    "x_parse_console_formatter__mutmut_13": x_parse_console_formatter__mutmut_13,
    "x_parse_console_formatter__mutmut_14": x_parse_console_formatter__mutmut_14,
    "x_parse_console_formatter__mutmut_15": x_parse_console_formatter__mutmut_15,
    "x_parse_console_formatter__mutmut_16": x_parse_console_formatter__mutmut_16,
    "x_parse_console_formatter__mutmut_17": x_parse_console_formatter__mutmut_17,
    "x_parse_console_formatter__mutmut_18": x_parse_console_formatter__mutmut_18,
    "x_parse_console_formatter__mutmut_19": x_parse_console_formatter__mutmut_19,
    "x_parse_console_formatter__mutmut_20": x_parse_console_formatter__mutmut_20,
}


def parse_console_formatter(*args, **kwargs):
    result = _mutmut_trampoline(
        x_parse_console_formatter__mutmut_orig, x_parse_console_formatter__mutmut_mutants, args, kwargs
    )
    return result


parse_console_formatter.__signature__ = _mutmut_signature(x_parse_console_formatter__mutmut_orig)
x_parse_console_formatter__mutmut_orig.__name__ = "x_parse_console_formatter"


def x_parse_foundation_log_output__mutmut_orig(value: str) -> str:
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


def x_parse_foundation_log_output__mutmut_1(value: str) -> str:
    """Parse and validate foundation log output destination.

    Args:
        value: Output destination string

    Returns:
        Valid output destination (stderr, stdout, main)

    Raises:
        ValueError: If the value is invalid

    """
    if value:
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


def x_parse_foundation_log_output__mutmut_2(value: str) -> str:
    """Parse and validate foundation log output destination.

    Args:
        value: Output destination string

    Returns:
        Valid output destination (stderr, stdout, main)

    Raises:
        ValueError: If the value is invalid

    """
    if not value:
        return "XXstderrXX"

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


def x_parse_foundation_log_output__mutmut_3(value: str) -> str:
    """Parse and validate foundation log output destination.

    Args:
        value: Output destination string

    Returns:
        Valid output destination (stderr, stdout, main)

    Raises:
        ValueError: If the value is invalid

    """
    if not value:
        return "STDERR"

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


def x_parse_foundation_log_output__mutmut_4(value: str) -> str:
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

    normalized = None
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


def x_parse_foundation_log_output__mutmut_5(value: str) -> str:
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

    normalized = value.upper().strip()
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


def x_parse_foundation_log_output__mutmut_6(value: str) -> str:
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
    valid_options = None

    if normalized in valid_options:
        return normalized
    raise ValueError(
        _format_invalid_value_error(
            "foundation_log_output",
            value,
            valid_options=list(valid_options),
        ),
    )


def x_parse_foundation_log_output__mutmut_7(value: str) -> str:
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
    valid_options = ("XXstderrXX", "stdout", "main")

    if normalized in valid_options:
        return normalized
    raise ValueError(
        _format_invalid_value_error(
            "foundation_log_output",
            value,
            valid_options=list(valid_options),
        ),
    )


def x_parse_foundation_log_output__mutmut_8(value: str) -> str:
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
    valid_options = ("STDERR", "stdout", "main")

    if normalized in valid_options:
        return normalized
    raise ValueError(
        _format_invalid_value_error(
            "foundation_log_output",
            value,
            valid_options=list(valid_options),
        ),
    )


def x_parse_foundation_log_output__mutmut_9(value: str) -> str:
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
    valid_options = ("stderr", "XXstdoutXX", "main")

    if normalized in valid_options:
        return normalized
    raise ValueError(
        _format_invalid_value_error(
            "foundation_log_output",
            value,
            valid_options=list(valid_options),
        ),
    )


def x_parse_foundation_log_output__mutmut_10(value: str) -> str:
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
    valid_options = ("stderr", "STDOUT", "main")

    if normalized in valid_options:
        return normalized
    raise ValueError(
        _format_invalid_value_error(
            "foundation_log_output",
            value,
            valid_options=list(valid_options),
        ),
    )


def x_parse_foundation_log_output__mutmut_11(value: str) -> str:
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
    valid_options = ("stderr", "stdout", "XXmainXX")

    if normalized in valid_options:
        return normalized
    raise ValueError(
        _format_invalid_value_error(
            "foundation_log_output",
            value,
            valid_options=list(valid_options),
        ),
    )


def x_parse_foundation_log_output__mutmut_12(value: str) -> str:
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
    valid_options = ("stderr", "stdout", "MAIN")

    if normalized in valid_options:
        return normalized
    raise ValueError(
        _format_invalid_value_error(
            "foundation_log_output",
            value,
            valid_options=list(valid_options),
        ),
    )


def x_parse_foundation_log_output__mutmut_13(value: str) -> str:
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

    if normalized not in valid_options:
        return normalized
    raise ValueError(
        _format_invalid_value_error(
            "foundation_log_output",
            value,
            valid_options=list(valid_options),
        ),
    )


def x_parse_foundation_log_output__mutmut_14(value: str) -> str:
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
        None,
    )


def x_parse_foundation_log_output__mutmut_15(value: str) -> str:
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
            None,
            value,
            valid_options=list(valid_options),
        ),
    )


def x_parse_foundation_log_output__mutmut_16(value: str) -> str:
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
            None,
            valid_options=list(valid_options),
        ),
    )


def x_parse_foundation_log_output__mutmut_17(value: str) -> str:
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
            valid_options=None,
        ),
    )


def x_parse_foundation_log_output__mutmut_18(value: str) -> str:
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
            value,
            valid_options=list(valid_options),
        ),
    )


def x_parse_foundation_log_output__mutmut_19(value: str) -> str:
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
            valid_options=list(valid_options),
        ),
    )


def x_parse_foundation_log_output__mutmut_20(value: str) -> str:
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
        ),
    )


def x_parse_foundation_log_output__mutmut_21(value: str) -> str:
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
            "XXfoundation_log_outputXX",
            value,
            valid_options=list(valid_options),
        ),
    )


def x_parse_foundation_log_output__mutmut_22(value: str) -> str:
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
            "FOUNDATION_LOG_OUTPUT",
            value,
            valid_options=list(valid_options),
        ),
    )


def x_parse_foundation_log_output__mutmut_23(value: str) -> str:
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
            valid_options=list(None),
        ),
    )


x_parse_foundation_log_output__mutmut_mutants: ClassVar[MutantDict] = {
    "x_parse_foundation_log_output__mutmut_1": x_parse_foundation_log_output__mutmut_1,
    "x_parse_foundation_log_output__mutmut_2": x_parse_foundation_log_output__mutmut_2,
    "x_parse_foundation_log_output__mutmut_3": x_parse_foundation_log_output__mutmut_3,
    "x_parse_foundation_log_output__mutmut_4": x_parse_foundation_log_output__mutmut_4,
    "x_parse_foundation_log_output__mutmut_5": x_parse_foundation_log_output__mutmut_5,
    "x_parse_foundation_log_output__mutmut_6": x_parse_foundation_log_output__mutmut_6,
    "x_parse_foundation_log_output__mutmut_7": x_parse_foundation_log_output__mutmut_7,
    "x_parse_foundation_log_output__mutmut_8": x_parse_foundation_log_output__mutmut_8,
    "x_parse_foundation_log_output__mutmut_9": x_parse_foundation_log_output__mutmut_9,
    "x_parse_foundation_log_output__mutmut_10": x_parse_foundation_log_output__mutmut_10,
    "x_parse_foundation_log_output__mutmut_11": x_parse_foundation_log_output__mutmut_11,
    "x_parse_foundation_log_output__mutmut_12": x_parse_foundation_log_output__mutmut_12,
    "x_parse_foundation_log_output__mutmut_13": x_parse_foundation_log_output__mutmut_13,
    "x_parse_foundation_log_output__mutmut_14": x_parse_foundation_log_output__mutmut_14,
    "x_parse_foundation_log_output__mutmut_15": x_parse_foundation_log_output__mutmut_15,
    "x_parse_foundation_log_output__mutmut_16": x_parse_foundation_log_output__mutmut_16,
    "x_parse_foundation_log_output__mutmut_17": x_parse_foundation_log_output__mutmut_17,
    "x_parse_foundation_log_output__mutmut_18": x_parse_foundation_log_output__mutmut_18,
    "x_parse_foundation_log_output__mutmut_19": x_parse_foundation_log_output__mutmut_19,
    "x_parse_foundation_log_output__mutmut_20": x_parse_foundation_log_output__mutmut_20,
    "x_parse_foundation_log_output__mutmut_21": x_parse_foundation_log_output__mutmut_21,
    "x_parse_foundation_log_output__mutmut_22": x_parse_foundation_log_output__mutmut_22,
    "x_parse_foundation_log_output__mutmut_23": x_parse_foundation_log_output__mutmut_23,
}


def parse_foundation_log_output(*args, **kwargs):
    result = _mutmut_trampoline(
        x_parse_foundation_log_output__mutmut_orig, x_parse_foundation_log_output__mutmut_mutants, args, kwargs
    )
    return result


parse_foundation_log_output.__signature__ = _mutmut_signature(x_parse_foundation_log_output__mutmut_orig)
x_parse_foundation_log_output__mutmut_orig.__name__ = "x_parse_foundation_log_output"


__all__ = [
    "parse_console_formatter",
    "parse_foundation_log_output",
    "parse_log_level",
]


# <3 🧱🤝🧩🪄
