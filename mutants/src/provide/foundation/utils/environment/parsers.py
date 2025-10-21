# provide/foundation/utils/environment/parsers.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import re

from provide.foundation.errors.config import ValidationError
from provide.foundation.utils.caching import cached

"""Duration and size parsing utilities for environment variables.

Provides specialized parsers for common environment variable formats
like durations (30s, 1h30m) and sizes (10MB, 1.5GB).
"""

# Pre-compiled regex patterns for performance
_DURATION_PATTERN = re.compile(r"(\d+)([dhms])")
_SIZE_PATTERN = re.compile(r"^(\d+(?:\.\d+)?)\s*([KMGT]?B?)$")
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


@cached(maxsize=256)
def parse_duration(value: str) -> int:
    """Parse duration string to seconds.

    Supports formats like: 30s, 5m, 2h, 1d, 1h30m, etc.

    Results are cached for performance on repeated calls.

    Args:
        value: Duration string

    Returns:
        Duration in seconds

    Examples:
        >>> parse_duration('30s')
        30
        >>> parse_duration('1h30m')
        5400
        >>> parse_duration('2d')
        172800

    """
    if value.isdigit():
        return int(value)

    total_seconds = 0

    # Use pre-compiled pattern
    matches = _DURATION_PATTERN.findall(value.lower())

    if not matches:
        raise ValidationError(f"Invalid duration format: {value}", value=value, rule="duration")

    units = {
        "s": 1,
        "m": 60,
        "h": 3600,
        "d": 86400,
    }

    for amount, unit in matches:
        if unit in units:
            total_seconds += int(amount) * units[unit]
        else:
            raise ValidationError(f"Unknown duration unit: {unit}", value=value, rule="duration_unit")

    return total_seconds


@cached(maxsize=256)
def parse_size(value: str) -> int:
    """Parse size string to bytes.

    Supports formats like: 1024, 1KB, 10MB, 1.5GB, etc.

    Results are cached for performance on repeated calls.

    Args:
        value: Size string

    Returns:
        Size in bytes

    Examples:
        >>> parse_size('1024')
        1024
        >>> parse_size('10MB')
        10485760
        >>> parse_size('1.5GB')
        1610612736

    """
    if value.isdigit():
        return int(value)

    # Use pre-compiled pattern
    match = _SIZE_PATTERN.match(value.upper())

    if not match:
        raise ValidationError(f"Invalid size format: {value}", value=value, rule="size")

    amount = float(match.group(1))
    unit = match.group(2) or "B"

    units = {
        "B": 1,
        "KB": 1024,
        "K": 1024,
        "MB": 1024**2,
        "M": 1024**2,
        "GB": 1024**3,
        "G": 1024**3,
        "TB": 1024**4,
        "T": 1024**4,
    }

    if unit not in units:
        raise ValidationError(f"Unknown size unit: {unit}", value=value, rule="size_unit")

    return int(amount * units[unit])


# <3 🧱🤝🧰🪄
