#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from __future__ import annotations

"""String grouping utilities.

Provides utilities for formatting strings with grouping separators,
useful for hash values, IDs, and other long strings.
"""


def format_grouped(
    text: str,
    group_size: int = 8,
    groups: int = 0,
    separator: str = " ",
) -> str:
    """Format a string with grouping separators for display.

    Args:
        text: Text to format
        group_size: Number of characters per group
        groups: Number of groups to show (0 for all)
        separator: Separator between groups

    Returns:
        Formatted string with groups

    Examples:
        >>> format_grouped("abc123def456", group_size=4, separator="-")
        'abc1-23de-f456'
        >>> format_grouped("abc123def456", group_size=4, groups=2)
        'abc1 23de'
        >>> format_grouped("1234567890abcdef", group_size=4)
        '1234 5678 90ab cdef'

    """
    if group_size <= 0:
        return text

    formatted_parts = []
    for i in range(0, len(text), group_size):
        formatted_parts.append(text[i : i + group_size])
        if groups > 0 and len(formatted_parts) >= groups:
            break

    return separator.join(formatted_parts)


__all__ = [
    "format_grouped",
]

# 🧱🏗️🔚
