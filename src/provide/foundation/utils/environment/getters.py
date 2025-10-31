#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any, TypeVar, get_origin

from provide.foundation.errors.config import ValidationError
from provide.foundation.logger import get_logger
from provide.foundation.parsers import parse_bool, parse_dict, parse_list, parse_set, parse_tuple

"""Basic environment variable getters with type coercion.

Provides safe functions for reading and parsing environment variables
with automatic type detection and validation.
"""

T = TypeVar("T")


def _get_logger() -> Any:
    """Get logger instance lazily to avoid circular imports."""

    return get_logger(__name__)


def get_bool(name: str, default: bool | None = None) -> bool | None:
    """Get boolean environment variable.

    Args:
        name: Environment variable name
        default: Default value if not set

    Returns:
        Boolean value, None (if set but empty), or default (if unset)

    Note:
        Empty string is treated as ambiguous and returns None with a warning.
        Unset variable returns the default value.

    Examples:
        >>> os.environ['DEBUG'] = 'true'
        >>> get_bool('DEBUG')
        True
        >>> get_bool('MISSING', False)
        False

    """
    from provide.foundation.logger import get_logger

    value = os.environ.get(name)
    if value is None:
        return default

    # Handle empty/whitespace-only strings as ambiguous
    if not value.strip():
        logger = get_logger(__name__)
        logger.warning(
            f"Environment variable {name} is set but empty - treating as None. "
            f"Either provide a value or unset the variable to use default."
        )
        return None

    try:
        return parse_bool(value)
    except ValueError as e:
        raise ValidationError(
            f"Invalid boolean value for {name}: {value}",
            field=name,
            value=value,
            rule="boolean",
        ) from e


def get_int(name: str, default: int | None = None) -> int | None:
    """Get integer environment variable.

    Args:
        name: Environment variable name
        default: Default value if not set

    Returns:
        Integer value or default

    Raises:
        ValidationError: If value cannot be parsed as integer

    """
    value = os.environ.get(name)
    if value is None:
        return default

    try:
        return int(value)
    except ValueError as e:
        raise ValidationError(
            f"Invalid integer value for {name}: {value}",
            field=name,
            value=value,
            rule="integer",
        ) from e


def get_float(name: str, default: float | None = None) -> float | None:
    """Get float environment variable.

    Args:
        name: Environment variable name
        default: Default value if not set

    Returns:
        Float value or default

    Raises:
        ValidationError: If value cannot be parsed as float

    """
    value = os.environ.get(name)
    if value is None:
        return default

    try:
        return float(value)
    except ValueError as e:
        raise ValidationError(
            f"Invalid float value for {name}: {value}",
            field=name,
            value=value,
            rule="float",
        ) from e


def get_str(name: str, default: str | None = None) -> str | None:
    """Get string environment variable.

    Args:
        name: Environment variable name
        default: Default value if not set

    Returns:
        String value or default

    """
    return os.environ.get(name, default)


def get_path(name: str, default: Path | str | None = None) -> Path | None:
    """Get path environment variable.

    Args:
        name: Environment variable name
        default: Default path if not set

    Returns:
        Path object or None

    """
    value = os.environ.get(name)
    if value is None:
        if default is None:
            return None
        return Path(default) if not isinstance(default, Path) else default

    # Expand user and environment variables
    expanded = os.path.expandvars(value)
    return Path(expanded).expanduser()


def get_list(name: str, default: list[str] | None = None, separator: str = ",") -> list[str]:
    """Get list from environment variable.

    Args:
        name: Environment variable name
        default: Default list if not set
        separator: String separator (default: comma)

    Returns:
        List of strings

    Examples:
        >>> os.environ['ITEMS'] = 'a,b,c'
        >>> get_list('ITEMS')
        ['a', 'b', 'c']

    """
    value = os.environ.get(name)
    if value is None:
        return default or []

    # Use existing parse_list which handles empty strings and stripping
    items = parse_list(value, separator=separator, strip=True)
    # Filter empty strings (parse_list doesn't do this by default)
    return [item for item in items if item]


def get_tuple(name: str, default: tuple[str, ...] | None = None, separator: str = ",") -> tuple[str, ...]:
    """Get tuple from environment variable.

    Args:
        name: Environment variable name
        default: Default tuple if not set
        separator: String separator (default: comma)

    Returns:
        Tuple of strings

    Examples:
        >>> os.environ['COORDINATES'] = '1.0,2.0,3.0'
        >>> get_tuple('COORDINATES')
        ('1.0', '2.0', '3.0')

    """
    value = os.environ.get(name)
    if value is None:
        return default or ()

    items = parse_tuple(value, separator=separator, strip=True)
    return tuple(item for item in items if item)


def get_set(name: str, default: set[str] | None = None, separator: str = ",") -> set[str]:
    """Get set from environment variable (duplicates removed).

    Args:
        name: Environment variable name
        default: Default set if not set
        separator: String separator (default: comma)

    Returns:
        Set of strings

    Examples:
        >>> os.environ['TAGS'] = 'dev,test,dev,prod'
        >>> get_set('TAGS')
        {'dev', 'test', 'prod'}

    """
    value = os.environ.get(name)
    if value is None:
        return default or set()

    items = parse_set(value, separator=separator, strip=True)
    return {item for item in items if item}


def get_dict(
    name: str,
    default: dict[str, str] | None = None,
    item_separator: str = ",",
    key_value_separator: str = "=",
) -> dict[str, str]:
    """Get dictionary from environment variable.

    Args:
        name: Environment variable name
        default: Default dict if not set
        item_separator: Separator between items
        key_value_separator: Separator between key and value

    Returns:
        Dictionary of string key-value pairs

    Examples:
        >>> os.environ['CONFIG'] = 'key1=val1,key2=val2'
        >>> get_dict('CONFIG')
        {'key1': 'val1', 'key2': 'val2'}

    """
    value = os.environ.get(name)
    if value is None:
        return default or {}

    try:
        return parse_dict(
            value,
            item_separator=item_separator,
            key_separator=key_value_separator,
            strip=True,
        )
    except ValueError as e:
        # parse_dict raises on invalid format, log warning and return partial result
        _get_logger().warning(
            "Invalid dictionary format in environment variable",
            var=name,
            value=value,
            error=str(e),
        )
        # Try to parse what we can, skipping invalid items
        result = {}
        items = value.split(item_separator)
        for item in items:
            item = item.strip()
            if not item:
                continue
            if key_value_separator not in item:
                continue
            key, val = item.split(key_value_separator, 1)
            result[key.strip()] = val.strip()
        return result


def _parse_simple_type(name: str, type_hint: type) -> Any:
    """Parse environment variable for simple types."""
    if type_hint is bool:
        return get_bool(name)
    if type_hint is int:
        return get_int(name)
    if type_hint is float:
        return get_float(name)
    if type_hint is str:
        return get_str(name)
    if type_hint is Path:
        return get_path(name)
    # Fallback to string for unknown simple types
    return os.environ[name]


def _parse_complex_type(name: str, origin: type) -> Any:
    """Parse environment variable for complex types."""
    if origin is list:
        return get_list(name)
    if origin is tuple:
        return get_tuple(name)
    if origin is set:
        return get_set(name)
    if origin is dict:
        return get_dict(name)
    # Fallback to string for unknown complex types
    return os.environ[name]


def require(name: str, type_hint: type[T] | None = None) -> Any:
    """Require an environment variable to be set.

    Args:
        name: Environment variable name
        type_hint: Optional type hint for parsing

    Returns:
        Parsed value

    Raises:
        ValidationError: If variable is not set

    """
    if name not in os.environ:
        raise ValidationError(
            f"Required environment variable not set: {name}",
            field=name,
            rule="required",
        )

    if type_hint is None:
        return os.environ[name]

    # Parse based on type hint
    origin = get_origin(type_hint)
    if origin is None:
        return _parse_simple_type(name, type_hint)
    else:
        return _parse_complex_type(name, origin)


# 🧱🏗️🔚
