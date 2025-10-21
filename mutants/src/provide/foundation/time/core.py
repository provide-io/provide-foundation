# provide/foundation/time/core.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from datetime import datetime
import time
from zoneinfo import ZoneInfo

from provide.foundation.errors import ValidationError

"""Core time utilities for Foundation."""
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


def provide_time() -> float:
    """Get current time with Foundation tracking.

    Returns:
        Current time as seconds since epoch

    Example:
        >>> current_time = provide_time()
        >>> isinstance(current_time, float)
        True

    """
    return time.time()


def x_provide_sleep__mutmut_orig(seconds: float) -> None:
    """Sleep with Foundation tracking and interruption support.

    Args:
        seconds: Number of seconds to sleep

    Raises:
        ValidationError: If seconds is negative

    Example:
        >>> provide_sleep(0.1)  # Sleep for 100ms

    """
    if seconds < 0:
        raise ValidationError("Sleep duration must be non-negative")
    time.sleep(seconds)


def x_provide_sleep__mutmut_1(seconds: float) -> None:
    """Sleep with Foundation tracking and interruption support.

    Args:
        seconds: Number of seconds to sleep

    Raises:
        ValidationError: If seconds is negative

    Example:
        >>> provide_sleep(0.1)  # Sleep for 100ms

    """
    if seconds <= 0:
        raise ValidationError("Sleep duration must be non-negative")
    time.sleep(seconds)


def x_provide_sleep__mutmut_2(seconds: float) -> None:
    """Sleep with Foundation tracking and interruption support.

    Args:
        seconds: Number of seconds to sleep

    Raises:
        ValidationError: If seconds is negative

    Example:
        >>> provide_sleep(0.1)  # Sleep for 100ms

    """
    if seconds < 1:
        raise ValidationError("Sleep duration must be non-negative")
    time.sleep(seconds)


def x_provide_sleep__mutmut_3(seconds: float) -> None:
    """Sleep with Foundation tracking and interruption support.

    Args:
        seconds: Number of seconds to sleep

    Raises:
        ValidationError: If seconds is negative

    Example:
        >>> provide_sleep(0.1)  # Sleep for 100ms

    """
    if seconds < 0:
        raise ValidationError(None)
    time.sleep(seconds)


def x_provide_sleep__mutmut_4(seconds: float) -> None:
    """Sleep with Foundation tracking and interruption support.

    Args:
        seconds: Number of seconds to sleep

    Raises:
        ValidationError: If seconds is negative

    Example:
        >>> provide_sleep(0.1)  # Sleep for 100ms

    """
    if seconds < 0:
        raise ValidationError("XXSleep duration must be non-negativeXX")
    time.sleep(seconds)


def x_provide_sleep__mutmut_5(seconds: float) -> None:
    """Sleep with Foundation tracking and interruption support.

    Args:
        seconds: Number of seconds to sleep

    Raises:
        ValidationError: If seconds is negative

    Example:
        >>> provide_sleep(0.1)  # Sleep for 100ms

    """
    if seconds < 0:
        raise ValidationError("sleep duration must be non-negative")
    time.sleep(seconds)


def x_provide_sleep__mutmut_6(seconds: float) -> None:
    """Sleep with Foundation tracking and interruption support.

    Args:
        seconds: Number of seconds to sleep

    Raises:
        ValidationError: If seconds is negative

    Example:
        >>> provide_sleep(0.1)  # Sleep for 100ms

    """
    if seconds < 0:
        raise ValidationError("SLEEP DURATION MUST BE NON-NEGATIVE")
    time.sleep(seconds)


def x_provide_sleep__mutmut_7(seconds: float) -> None:
    """Sleep with Foundation tracking and interruption support.

    Args:
        seconds: Number of seconds to sleep

    Raises:
        ValidationError: If seconds is negative

    Example:
        >>> provide_sleep(0.1)  # Sleep for 100ms

    """
    if seconds < 0:
        raise ValidationError("Sleep duration must be non-negative")
    time.sleep(None)

x_provide_sleep__mutmut_mutants : ClassVar[MutantDict] = {
'x_provide_sleep__mutmut_1': x_provide_sleep__mutmut_1, 
    'x_provide_sleep__mutmut_2': x_provide_sleep__mutmut_2, 
    'x_provide_sleep__mutmut_3': x_provide_sleep__mutmut_3, 
    'x_provide_sleep__mutmut_4': x_provide_sleep__mutmut_4, 
    'x_provide_sleep__mutmut_5': x_provide_sleep__mutmut_5, 
    'x_provide_sleep__mutmut_6': x_provide_sleep__mutmut_6, 
    'x_provide_sleep__mutmut_7': x_provide_sleep__mutmut_7
}

def provide_sleep(*args, **kwargs):
    result = _mutmut_trampoline(x_provide_sleep__mutmut_orig, x_provide_sleep__mutmut_mutants, args, kwargs)
    return result 

provide_sleep.__signature__ = _mutmut_signature(x_provide_sleep__mutmut_orig)
x_provide_sleep__mutmut_orig.__name__ = 'x_provide_sleep'


def x_provide_now__mutmut_orig(tz: str | ZoneInfo | None = None) -> datetime:
    """Get current datetime with timezone awareness.

    Args:
        tz: Timezone (string name, ZoneInfo object, or None for local)

    Returns:
        Current datetime with timezone information

    Example:
        >>> now = provide_now()
        >>> now.tzinfo is not None
        True
        >>> utc_now = provide_now("UTC")
        >>> utc_now.tzinfo.key
        'UTC'

    """
    if tz is None:
        return datetime.now()
    zone = ZoneInfo(tz) if isinstance(tz, str) else tz

    return datetime.now(zone)


def x_provide_now__mutmut_1(tz: str | ZoneInfo | None = None) -> datetime:
    """Get current datetime with timezone awareness.

    Args:
        tz: Timezone (string name, ZoneInfo object, or None for local)

    Returns:
        Current datetime with timezone information

    Example:
        >>> now = provide_now()
        >>> now.tzinfo is not None
        True
        >>> utc_now = provide_now("UTC")
        >>> utc_now.tzinfo.key
        'UTC'

    """
    if tz is not None:
        return datetime.now()
    zone = ZoneInfo(tz) if isinstance(tz, str) else tz

    return datetime.now(zone)


def x_provide_now__mutmut_2(tz: str | ZoneInfo | None = None) -> datetime:
    """Get current datetime with timezone awareness.

    Args:
        tz: Timezone (string name, ZoneInfo object, or None for local)

    Returns:
        Current datetime with timezone information

    Example:
        >>> now = provide_now()
        >>> now.tzinfo is not None
        True
        >>> utc_now = provide_now("UTC")
        >>> utc_now.tzinfo.key
        'UTC'

    """
    if tz is None:
        return datetime.now()
    zone = None

    return datetime.now(zone)


def x_provide_now__mutmut_3(tz: str | ZoneInfo | None = None) -> datetime:
    """Get current datetime with timezone awareness.

    Args:
        tz: Timezone (string name, ZoneInfo object, or None for local)

    Returns:
        Current datetime with timezone information

    Example:
        >>> now = provide_now()
        >>> now.tzinfo is not None
        True
        >>> utc_now = provide_now("UTC")
        >>> utc_now.tzinfo.key
        'UTC'

    """
    if tz is None:
        return datetime.now()
    zone = ZoneInfo(None) if isinstance(tz, str) else tz

    return datetime.now(zone)


def x_provide_now__mutmut_4(tz: str | ZoneInfo | None = None) -> datetime:
    """Get current datetime with timezone awareness.

    Args:
        tz: Timezone (string name, ZoneInfo object, or None for local)

    Returns:
        Current datetime with timezone information

    Example:
        >>> now = provide_now()
        >>> now.tzinfo is not None
        True
        >>> utc_now = provide_now("UTC")
        >>> utc_now.tzinfo.key
        'UTC'

    """
    if tz is None:
        return datetime.now()
    zone = ZoneInfo(tz) if isinstance(tz, str) else tz

    return datetime.now(None)

x_provide_now__mutmut_mutants : ClassVar[MutantDict] = {
'x_provide_now__mutmut_1': x_provide_now__mutmut_1, 
    'x_provide_now__mutmut_2': x_provide_now__mutmut_2, 
    'x_provide_now__mutmut_3': x_provide_now__mutmut_3, 
    'x_provide_now__mutmut_4': x_provide_now__mutmut_4
}

def provide_now(*args, **kwargs):
    result = _mutmut_trampoline(x_provide_now__mutmut_orig, x_provide_now__mutmut_mutants, args, kwargs)
    return result 

provide_now.__signature__ = _mutmut_signature(x_provide_now__mutmut_orig)
x_provide_now__mutmut_orig.__name__ = 'x_provide_now'


# <3 🧱🤝🕰️🪄
