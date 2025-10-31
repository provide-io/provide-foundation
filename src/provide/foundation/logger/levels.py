#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

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


def normalize_level(level: str) -> str:
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


def get_numeric_level(level: str, fallback: int | None = None) -> int:
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


def is_valid_level(level: str) -> bool:
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

# 🧱🏗️🔚
