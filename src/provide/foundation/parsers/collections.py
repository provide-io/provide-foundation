#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from __future__ import annotations

"""Collection parsing functions for lists, dicts, tuples, and sets.

Handles parsing of collection types from string values with customizable
separators and formatting options.
"""


def parse_list(
    value: str | list[str],
    separator: str = ",",
    strip: bool = True,
) -> list[str]:
    """Parse a list from a string.

    Args:
        value: String or list to parse
        separator: Separator character
        strip: Whether to strip whitespace from items

    Returns:
        List of strings

    """
    if isinstance(value, list):
        return value

    if not value:
        return []

    items = value.split(separator)

    if strip:
        items = [item.strip() for item in items]

    return items


def parse_tuple(
    value: str | tuple[str, ...],
    separator: str = ",",
    strip: bool = True,
) -> tuple[str, ...]:
    """Parse a tuple from a string.

    Args:
        value: String or tuple to parse
        separator: Separator character
        strip: Whether to strip whitespace from items

    Returns:
        Tuple of strings

    """
    if isinstance(value, tuple):
        return value

    # Reuse list parsing logic
    items = parse_list(value, separator=separator, strip=strip)
    return tuple(items)


def parse_set(
    value: str | set[str],
    separator: str = ",",
    strip: bool = True,
) -> set[str]:
    """Parse a set from a string.

    Args:
        value: String or set to parse
        separator: Separator character
        strip: Whether to strip whitespace from items

    Returns:
        Set of strings (duplicates removed)

    """
    if isinstance(value, set):
        return value

    # Reuse list parsing logic, then convert to set
    items = parse_list(value, separator=separator, strip=strip)
    return set(items)


def parse_dict(
    value: str | dict[str, str],
    item_separator: str = ",",
    key_separator: str = "=",
    strip: bool = True,
) -> dict[str, str]:
    """Parse a dictionary from a string.

    Format: "key1=value1,key2=value2"

    Args:
        value: String or dict to parse
        item_separator: Separator between items
        key_separator: Separator between key and value
        strip: Whether to strip whitespace

    Returns:
        Dictionary of string keys and values

    Raises:
        ValueError: If format is invalid

    """
    if isinstance(value, dict):
        return value

    if not value:
        return {}

    result = {}
    items = value.split(item_separator)

    for item in items:
        if not item:
            continue

        if key_separator not in item:
            raise ValueError(f"Invalid dict format: '{item}' missing '{key_separator}'")

        key, val = item.split(key_separator, 1)

        if strip:
            key = key.strip()
            val = val.strip()

        result[key] = val

    return result


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


__all__ = [
    "parse_comma_list",
    "parse_dict",
    "parse_list",
    "parse_set",
    "parse_tuple",
]

# 🧱🏗️🔚
