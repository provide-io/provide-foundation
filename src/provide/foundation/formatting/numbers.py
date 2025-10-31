#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from __future__ import annotations

"""Size, duration, and number formatting utilities.

Provides utilities for human-readable formatting of sizes, durations,
and numeric values.
"""


def format_size(size_bytes: float, precision: int = 1) -> str:
    """Format bytes as human-readable size.

    Args:
        size_bytes: Size in bytes
        precision: Decimal places for display

    Returns:
        Human-readable size string

    Examples:
        >>> format_size(1024)
        '1.0 KB'
        >>> format_size(1536)
        '1.5 KB'
        >>> format_size(1073741824)
        '1.0 GB'
        >>> format_size(0)
        '0 B'

    """
    if size_bytes == 0:
        return "0 B"

    # Handle negative sizes
    negative = size_bytes < 0
    size_bytes = abs(size_bytes)

    units = ["B", "KB", "MB", "GB", "TB", "PB", "EB"]
    unit_index = 0

    while size_bytes >= 1024.0 and unit_index < len(units) - 1:
        size_bytes /= 1024.0
        unit_index += 1

    # Format with specified precision
    if unit_index == 0:
        # Bytes - no decimal places
        formatted = f"{int(size_bytes)} {units[unit_index]}"
    else:
        formatted = f"{size_bytes:.{precision}f} {units[unit_index]}"

    return f"-{formatted}" if negative else formatted


def _format_duration_components(
    days: int, hours: int, minutes: int, seconds: int
) -> tuple[int, int, int, int]:
    """Extract duration components from seconds."""
    return (
        days,
        hours,
        minutes,
        seconds,
    )


def _format_duration_short(days: int, hours: int, minutes: int, seconds: int) -> str:
    """Format duration in short format (1h30m)."""
    parts = []
    if days > 0:
        parts.append(f"{days}d")
    if hours > 0:
        parts.append(f"{hours}h")
    if minutes > 0:
        parts.append(f"{minutes}m")
    if seconds > 0 or not parts:
        parts.append(f"{seconds}s")
    return "".join(parts)


def _format_duration_long(days: int, hours: int, minutes: int, seconds: int) -> str:
    """Format duration in long format (1 hour 30 minutes)."""
    parts = []
    if days > 0:
        parts.append(f"{days} day{'s' if days != 1 else ''}")
    if hours > 0:
        parts.append(f"{hours} hour{'s' if hours != 1 else ''}")
    if minutes > 0:
        parts.append(f"{minutes} minute{'s' if minutes != 1 else ''}")
    if seconds > 0 or not parts:
        parts.append(f"{seconds} second{'s' if seconds != 1 else ''}")
    return " ".join(parts)


def format_duration(seconds: float, short: bool = False) -> str:
    """Format seconds as human-readable duration.

    Args:
        seconds: Duration in seconds
        short: Use short format (1h30m vs 1 hour 30 minutes)

    Returns:
        Human-readable duration string

    Examples:
        >>> format_duration(90)
        '1 minute 30 seconds'
        >>> format_duration(90, short=True)
        '1m30s'
        >>> format_duration(3661)
        '1 hour 1 minute 1 second'
        >>> format_duration(3661, short=True)
        '1h1m1s'

    """
    if seconds < 0:
        return f"-{format_duration(abs(seconds), short)}"

    if seconds == 0:
        return "0s" if short else "0 seconds"

    # Calculate components
    days = int(seconds // 86400)
    hours = int((seconds % 86400) // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)

    if short:
        return _format_duration_short(days, hours, minutes, secs)
    return _format_duration_long(days, hours, minutes, secs)


def format_number(num: float, precision: int | None = None) -> str:
    """Format number with thousands separators.

    Args:
        num: Number to format
        precision: Decimal places (None for automatic)

    Returns:
        Formatted number string

    Examples:
        >>> format_number(1234567)
        '1,234,567'
        >>> format_number(1234.5678, precision=2)
        '1,234.57'

    """
    if precision is None:
        if isinstance(num, int):
            return f"{num:,}"
        # Auto precision for floats
        return f"{num:,.6f}".rstrip("0").rstrip(".")
    return f"{num:,.{precision}f}"


def format_percentage(value: float, precision: int = 1, include_sign: bool = False) -> str:
    """Format value as percentage.

    Args:
        value: Value to format (0.5 = 50%)
        precision: Decimal places
        include_sign: Include + sign for positive values

    Returns:
        Formatted percentage string

    Examples:
        >>> format_percentage(0.5)
        '50.0%'
        >>> format_percentage(0.1234, precision=2)
        '12.34%'
        >>> format_percentage(0.05, include_sign=True)
        '+5.0%'

    """
    percentage = value * 100
    formatted = f"{percentage:.{precision}f}%"

    if include_sign and value > 0:
        formatted = f"+{formatted}"

    return formatted


__all__ = [
    "format_duration",
    "format_number",
    "format_percentage",
    "format_size",
]

# 🧱🏗️🔚
