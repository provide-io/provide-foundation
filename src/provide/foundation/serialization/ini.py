#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from __future__ import annotations

from configparser import ConfigParser
from io import StringIO
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    pass
from provide.foundation.serialization.cache import get_cache_enabled, get_cache_key, get_serialization_cache

"""INI format serialization with caching support."""


def ini_dumps(obj: dict[str, dict[str, str]], *, include_default: bool = False) -> str:
    """Serialize nested dictionary to INI format string.

    Args:
        obj: Nested dictionary (sections -> key-value pairs)
        include_default: Whether to include DEFAULT section

    Returns:
        INI format string

    Raises:
        ValidationError: If object cannot be serialized

    Example:
        >>> ini_dumps({"section": {"key": "value"}})
        '[section]\\nkey = value\\n\\n'

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(obj, dict):
        raise ValidationError("INI serialization requires a dictionary")

    parser = ConfigParser()

    try:
        for section_name, section_data in obj.items():
            if section_name == "DEFAULT" and not include_default:
                continue

            if not isinstance(section_data, dict):
                raise ValidationError(f"Section '{section_name}' must be a dictionary")

            if section_name != "DEFAULT":
                parser.add_section(section_name)

            for key, value in section_data.items():
                parser.set(section_name, key, str(value))

        # Write to string
        output = StringIO()
        parser.write(output)
        return output.getvalue()
    except Exception as e:
        raise ValidationError(f"Cannot serialize object to INI: {e}") from e


def ini_loads(s: str, *, use_cache: bool = True) -> dict[str, dict[str, str]]:
    """Deserialize INI format string to nested dictionary.

    Args:
        s: INI format string to deserialize
        use_cache: Whether to use caching for this operation

    Returns:
        Nested dictionary (sections -> key-value pairs)

    Raises:
        ValidationError: If string is not valid INI format

    Example:
        >>> ini_loads('[section]\\nkey = value')
        {'section': {'key': 'value'}}

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(s, str):
        raise ValidationError("Input must be a string")

    # Check cache first if enabled
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "ini")
        cached = get_serialization_cache().get(cache_key)
        if cached is not None:
            return cached

    parser = ConfigParser()

    try:
        parser.read_string(s)
    except Exception as e:
        raise ValidationError(f"Invalid INI string: {e}") from e

    # Convert to dictionary
    result: dict[str, dict[str, str]] = {}

    for section in parser.sections():
        result[section] = dict(parser.items(section))

    # Include DEFAULT section if present
    if parser.defaults():
        result["DEFAULT"] = dict(parser.defaults())

    # Cache result
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "ini")
        get_serialization_cache().set(cache_key, result)

    return result


__all__ = [
    "ini_dumps",
    "ini_loads",
]

# 🧱🏗️🔚
