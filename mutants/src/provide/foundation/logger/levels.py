# provide/foundation/logger/levels.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from typing import cast

from provide.foundation.logger.constants import (
    DEFAULT_FALLBACK_LEVEL,
    DEFAULT_FALLBACK_NUMERIC,
    LEVEL_TO_NUMERIC,
    VALID_LEVEL_NAMES,
)
from provide.foundation.logger.types import LogLevelStr

"""Log level normalization and safe lookup utilities.

Provides functions for normalizing log levels and performing safe lookups
to prevent KeyError crashes in the logging system.
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


def x_normalize_level__mutmut_orig(level: str) -> str:
    """Normalize log level string to uppercase.

    Args:
        level: Log level string in any case

    Returns:
        Normalized uppercase level string

    Examples:
        >>> normalize_level("info")
        "INFO"
        >>> normalize_level("DEBUG")
        "DEBUG"
        >>> normalize_level("  warning  ")
        "WARNING"
    """
    return level.upper().strip()


def x_normalize_level__mutmut_1(level: str) -> str:
    """Normalize log level string to uppercase.

    Args:
        level: Log level string in any case

    Returns:
        Normalized uppercase level string

    Examples:
        >>> normalize_level("info")
        "INFO"
        >>> normalize_level("DEBUG")
        "DEBUG"
        >>> normalize_level("  warning  ")
        "WARNING"
    """
    return level.lower().strip()

x_normalize_level__mutmut_mutants : ClassVar[MutantDict] = {
'x_normalize_level__mutmut_1': x_normalize_level__mutmut_1
}

def normalize_level(*args, **kwargs):
    result = _mutmut_trampoline(x_normalize_level__mutmut_orig, x_normalize_level__mutmut_mutants, args, kwargs)
    return result 

normalize_level.__signature__ = _mutmut_signature(x_normalize_level__mutmut_orig)
x_normalize_level__mutmut_orig.__name__ = 'x_normalize_level'


def x_get_numeric_level__mutmut_orig(level: str, fallback: int | None = None) -> int:
    """Get numeric value for log level with safe fallback.

    Args:
        level: Log level string in any case
        fallback: Optional fallback numeric value (defaults to INFO level)

    Returns:
        Numeric log level value

    Examples:
        >>> get_numeric_level("info")
        20
        >>> get_numeric_level("invalid", fallback=999)
        999
        >>> get_numeric_level("DEBUG")
        10
    """
    if fallback is None:
        fallback = DEFAULT_FALLBACK_NUMERIC

    normalized = normalize_level(level)
    # Cast to LogLevelStr for type safety - normalize_level validates valid levels
    return LEVEL_TO_NUMERIC.get(cast(LogLevelStr, normalized), fallback)


def x_get_numeric_level__mutmut_1(level: str, fallback: int | None = None) -> int:
    """Get numeric value for log level with safe fallback.

    Args:
        level: Log level string in any case
        fallback: Optional fallback numeric value (defaults to INFO level)

    Returns:
        Numeric log level value

    Examples:
        >>> get_numeric_level("info")
        20
        >>> get_numeric_level("invalid", fallback=999)
        999
        >>> get_numeric_level("DEBUG")
        10
    """
    if fallback is not None:
        fallback = DEFAULT_FALLBACK_NUMERIC

    normalized = normalize_level(level)
    # Cast to LogLevelStr for type safety - normalize_level validates valid levels
    return LEVEL_TO_NUMERIC.get(cast(LogLevelStr, normalized), fallback)


def x_get_numeric_level__mutmut_2(level: str, fallback: int | None = None) -> int:
    """Get numeric value for log level with safe fallback.

    Args:
        level: Log level string in any case
        fallback: Optional fallback numeric value (defaults to INFO level)

    Returns:
        Numeric log level value

    Examples:
        >>> get_numeric_level("info")
        20
        >>> get_numeric_level("invalid", fallback=999)
        999
        >>> get_numeric_level("DEBUG")
        10
    """
    if fallback is None:
        fallback = None

    normalized = normalize_level(level)
    # Cast to LogLevelStr for type safety - normalize_level validates valid levels
    return LEVEL_TO_NUMERIC.get(cast(LogLevelStr, normalized), fallback)


def x_get_numeric_level__mutmut_3(level: str, fallback: int | None = None) -> int:
    """Get numeric value for log level with safe fallback.

    Args:
        level: Log level string in any case
        fallback: Optional fallback numeric value (defaults to INFO level)

    Returns:
        Numeric log level value

    Examples:
        >>> get_numeric_level("info")
        20
        >>> get_numeric_level("invalid", fallback=999)
        999
        >>> get_numeric_level("DEBUG")
        10
    """
    if fallback is None:
        fallback = DEFAULT_FALLBACK_NUMERIC

    normalized = None
    # Cast to LogLevelStr for type safety - normalize_level validates valid levels
    return LEVEL_TO_NUMERIC.get(cast(LogLevelStr, normalized), fallback)


def x_get_numeric_level__mutmut_4(level: str, fallback: int | None = None) -> int:
    """Get numeric value for log level with safe fallback.

    Args:
        level: Log level string in any case
        fallback: Optional fallback numeric value (defaults to INFO level)

    Returns:
        Numeric log level value

    Examples:
        >>> get_numeric_level("info")
        20
        >>> get_numeric_level("invalid", fallback=999)
        999
        >>> get_numeric_level("DEBUG")
        10
    """
    if fallback is None:
        fallback = DEFAULT_FALLBACK_NUMERIC

    normalized = normalize_level(None)
    # Cast to LogLevelStr for type safety - normalize_level validates valid levels
    return LEVEL_TO_NUMERIC.get(cast(LogLevelStr, normalized), fallback)


def x_get_numeric_level__mutmut_5(level: str, fallback: int | None = None) -> int:
    """Get numeric value for log level with safe fallback.

    Args:
        level: Log level string in any case
        fallback: Optional fallback numeric value (defaults to INFO level)

    Returns:
        Numeric log level value

    Examples:
        >>> get_numeric_level("info")
        20
        >>> get_numeric_level("invalid", fallback=999)
        999
        >>> get_numeric_level("DEBUG")
        10
    """
    if fallback is None:
        fallback = DEFAULT_FALLBACK_NUMERIC

    normalized = normalize_level(level)
    # Cast to LogLevelStr for type safety - normalize_level validates valid levels
    return LEVEL_TO_NUMERIC.get(None, fallback)


def x_get_numeric_level__mutmut_6(level: str, fallback: int | None = None) -> int:
    """Get numeric value for log level with safe fallback.

    Args:
        level: Log level string in any case
        fallback: Optional fallback numeric value (defaults to INFO level)

    Returns:
        Numeric log level value

    Examples:
        >>> get_numeric_level("info")
        20
        >>> get_numeric_level("invalid", fallback=999)
        999
        >>> get_numeric_level("DEBUG")
        10
    """
    if fallback is None:
        fallback = DEFAULT_FALLBACK_NUMERIC

    normalized = normalize_level(level)
    # Cast to LogLevelStr for type safety - normalize_level validates valid levels
    return LEVEL_TO_NUMERIC.get(cast(LogLevelStr, normalized), None)


def x_get_numeric_level__mutmut_7(level: str, fallback: int | None = None) -> int:
    """Get numeric value for log level with safe fallback.

    Args:
        level: Log level string in any case
        fallback: Optional fallback numeric value (defaults to INFO level)

    Returns:
        Numeric log level value

    Examples:
        >>> get_numeric_level("info")
        20
        >>> get_numeric_level("invalid", fallback=999)
        999
        >>> get_numeric_level("DEBUG")
        10
    """
    if fallback is None:
        fallback = DEFAULT_FALLBACK_NUMERIC

    normalized = normalize_level(level)
    # Cast to LogLevelStr for type safety - normalize_level validates valid levels
    return LEVEL_TO_NUMERIC.get(fallback)


def x_get_numeric_level__mutmut_8(level: str, fallback: int | None = None) -> int:
    """Get numeric value for log level with safe fallback.

    Args:
        level: Log level string in any case
        fallback: Optional fallback numeric value (defaults to INFO level)

    Returns:
        Numeric log level value

    Examples:
        >>> get_numeric_level("info")
        20
        >>> get_numeric_level("invalid", fallback=999)
        999
        >>> get_numeric_level("DEBUG")
        10
    """
    if fallback is None:
        fallback = DEFAULT_FALLBACK_NUMERIC

    normalized = normalize_level(level)
    # Cast to LogLevelStr for type safety - normalize_level validates valid levels
    return LEVEL_TO_NUMERIC.get(cast(LogLevelStr, normalized), )


def x_get_numeric_level__mutmut_9(level: str, fallback: int | None = None) -> int:
    """Get numeric value for log level with safe fallback.

    Args:
        level: Log level string in any case
        fallback: Optional fallback numeric value (defaults to INFO level)

    Returns:
        Numeric log level value

    Examples:
        >>> get_numeric_level("info")
        20
        >>> get_numeric_level("invalid", fallback=999)
        999
        >>> get_numeric_level("DEBUG")
        10
    """
    if fallback is None:
        fallback = DEFAULT_FALLBACK_NUMERIC

    normalized = normalize_level(level)
    # Cast to LogLevelStr for type safety - normalize_level validates valid levels
    return LEVEL_TO_NUMERIC.get(cast(None, normalized), fallback)


def x_get_numeric_level__mutmut_10(level: str, fallback: int | None = None) -> int:
    """Get numeric value for log level with safe fallback.

    Args:
        level: Log level string in any case
        fallback: Optional fallback numeric value (defaults to INFO level)

    Returns:
        Numeric log level value

    Examples:
        >>> get_numeric_level("info")
        20
        >>> get_numeric_level("invalid", fallback=999)
        999
        >>> get_numeric_level("DEBUG")
        10
    """
    if fallback is None:
        fallback = DEFAULT_FALLBACK_NUMERIC

    normalized = normalize_level(level)
    # Cast to LogLevelStr for type safety - normalize_level validates valid levels
    return LEVEL_TO_NUMERIC.get(cast(LogLevelStr, None), fallback)


def x_get_numeric_level__mutmut_11(level: str, fallback: int | None = None) -> int:
    """Get numeric value for log level with safe fallback.

    Args:
        level: Log level string in any case
        fallback: Optional fallback numeric value (defaults to INFO level)

    Returns:
        Numeric log level value

    Examples:
        >>> get_numeric_level("info")
        20
        >>> get_numeric_level("invalid", fallback=999)
        999
        >>> get_numeric_level("DEBUG")
        10
    """
    if fallback is None:
        fallback = DEFAULT_FALLBACK_NUMERIC

    normalized = normalize_level(level)
    # Cast to LogLevelStr for type safety - normalize_level validates valid levels
    return LEVEL_TO_NUMERIC.get(cast(normalized), fallback)


def x_get_numeric_level__mutmut_12(level: str, fallback: int | None = None) -> int:
    """Get numeric value for log level with safe fallback.

    Args:
        level: Log level string in any case
        fallback: Optional fallback numeric value (defaults to INFO level)

    Returns:
        Numeric log level value

    Examples:
        >>> get_numeric_level("info")
        20
        >>> get_numeric_level("invalid", fallback=999)
        999
        >>> get_numeric_level("DEBUG")
        10
    """
    if fallback is None:
        fallback = DEFAULT_FALLBACK_NUMERIC

    normalized = normalize_level(level)
    # Cast to LogLevelStr for type safety - normalize_level validates valid levels
    return LEVEL_TO_NUMERIC.get(cast(LogLevelStr, ), fallback)

x_get_numeric_level__mutmut_mutants : ClassVar[MutantDict] = {
'x_get_numeric_level__mutmut_1': x_get_numeric_level__mutmut_1, 
    'x_get_numeric_level__mutmut_2': x_get_numeric_level__mutmut_2, 
    'x_get_numeric_level__mutmut_3': x_get_numeric_level__mutmut_3, 
    'x_get_numeric_level__mutmut_4': x_get_numeric_level__mutmut_4, 
    'x_get_numeric_level__mutmut_5': x_get_numeric_level__mutmut_5, 
    'x_get_numeric_level__mutmut_6': x_get_numeric_level__mutmut_6, 
    'x_get_numeric_level__mutmut_7': x_get_numeric_level__mutmut_7, 
    'x_get_numeric_level__mutmut_8': x_get_numeric_level__mutmut_8, 
    'x_get_numeric_level__mutmut_9': x_get_numeric_level__mutmut_9, 
    'x_get_numeric_level__mutmut_10': x_get_numeric_level__mutmut_10, 
    'x_get_numeric_level__mutmut_11': x_get_numeric_level__mutmut_11, 
    'x_get_numeric_level__mutmut_12': x_get_numeric_level__mutmut_12
}

def get_numeric_level(*args, **kwargs):
    result = _mutmut_trampoline(x_get_numeric_level__mutmut_orig, x_get_numeric_level__mutmut_mutants, args, kwargs)
    return result 

get_numeric_level.__signature__ = _mutmut_signature(x_get_numeric_level__mutmut_orig)
x_get_numeric_level__mutmut_orig.__name__ = 'x_get_numeric_level'


def x_is_valid_level__mutmut_orig(level: str) -> bool:
    """Check if log level string is valid.

    Args:
        level: Log level string in any case

    Returns:
        True if level is valid, False otherwise

    Examples:
        >>> is_valid_level("info")
        True
        >>> is_valid_level("INVALID")
        False
        >>> is_valid_level("DEBUG")
        True
    """
    normalized = normalize_level(level)
    return normalized in VALID_LEVEL_NAMES


def x_is_valid_level__mutmut_1(level: str) -> bool:
    """Check if log level string is valid.

    Args:
        level: Log level string in any case

    Returns:
        True if level is valid, False otherwise

    Examples:
        >>> is_valid_level("info")
        True
        >>> is_valid_level("INVALID")
        False
        >>> is_valid_level("DEBUG")
        True
    """
    normalized = None
    return normalized in VALID_LEVEL_NAMES


def x_is_valid_level__mutmut_2(level: str) -> bool:
    """Check if log level string is valid.

    Args:
        level: Log level string in any case

    Returns:
        True if level is valid, False otherwise

    Examples:
        >>> is_valid_level("info")
        True
        >>> is_valid_level("INVALID")
        False
        >>> is_valid_level("DEBUG")
        True
    """
    normalized = normalize_level(None)
    return normalized in VALID_LEVEL_NAMES


def x_is_valid_level__mutmut_3(level: str) -> bool:
    """Check if log level string is valid.

    Args:
        level: Log level string in any case

    Returns:
        True if level is valid, False otherwise

    Examples:
        >>> is_valid_level("info")
        True
        >>> is_valid_level("INVALID")
        False
        >>> is_valid_level("DEBUG")
        True
    """
    normalized = normalize_level(level)
    return normalized not in VALID_LEVEL_NAMES

x_is_valid_level__mutmut_mutants : ClassVar[MutantDict] = {
'x_is_valid_level__mutmut_1': x_is_valid_level__mutmut_1, 
    'x_is_valid_level__mutmut_2': x_is_valid_level__mutmut_2, 
    'x_is_valid_level__mutmut_3': x_is_valid_level__mutmut_3
}

def is_valid_level(*args, **kwargs):
    result = _mutmut_trampoline(x_is_valid_level__mutmut_orig, x_is_valid_level__mutmut_mutants, args, kwargs)
    return result 

is_valid_level.__signature__ = _mutmut_signature(x_is_valid_level__mutmut_orig)
x_is_valid_level__mutmut_orig.__name__ = 'x_is_valid_level'


def get_fallback_level() -> str:
    """Get the default fallback level name.

    Returns:
        Default fallback level string (uppercase)
    """
    return DEFAULT_FALLBACK_LEVEL


def get_fallback_numeric() -> int:
    """Get the default fallback level numeric value.

    Returns:
        Default fallback level numeric value
    """
    return DEFAULT_FALLBACK_NUMERIC


__all__ = [
    "get_fallback_level",
    "get_fallback_numeric",
    "get_numeric_level",
    "is_valid_level",
    "normalize_level",
]


# <3 🧱🤝📝🪄
