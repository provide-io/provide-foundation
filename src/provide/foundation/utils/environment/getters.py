from __future__ import annotations

"""Basic environment variable getters with type coercion.

Provides safe functions for reading and parsing environment variables
with automatic type detection and validation.
"""
import os
from pathlib import Path
from typing import Any, TypeVar, get_origin

from provide.foundation.errors.config import ValidationError
from provide.foundation.logger import get_logger
from provide.foundation.utils.parsing import parse_bool, parse_dict, parse_list

T = TypeVar("T")


def _get_logger():
    """Get logger instance lazily to avoid circular imports."""

    return get_logger(__name__)


def get_bool(name: str, default: bool | None = None) -> bool | None:
    """Get boolean environment variable.

    Args:
        name: Environment variable name
        default: Default value if not set

    Returns:
        Boolean value or default

    Examples:
        >>> os.environ['DEBUG'] = 'true'
        >>> get_bool('DEBUG')
        True
        >>> get_bool('MISSING', False)
        False

    """
    value = os.environ.get(name)
    if value is None:
        return default

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
    expanded = os.path.expanduser(os.path.expandvars(value))
    return Path(expanded)


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
        # Simple type
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
    elif origin is list:
        return get_list(name)
    elif origin is dict:
        return get_dict(name)

    # Fallback to string
    return os.environ[name]
