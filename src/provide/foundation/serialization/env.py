#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    pass

from provide.foundation.serialization.cache import get_cache_enabled, get_cache_key, get_serialization_cache

""".env file format serialization with caching support."""


def env_dumps(obj: dict[str, str], *, quote_values: bool = True) -> str:
    """Serialize dictionary to .env file format string.

    Args:
        obj: Dictionary of environment variables
        quote_values: Whether to quote string values

    Returns:
        .env format string

    Raises:
        ValidationError: If object cannot be serialized

    Example:
        >>> env_dumps({"KEY": "value"})
        'KEY="value"\\n'
        >>> env_dumps({"KEY": "value"}, quote_values=False)
        'KEY=value\\n'

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(obj, dict):
        raise ValidationError("ENV serialization requires a dictionary")

    lines: list[str] = []

    try:
        for key, value in obj.items():
            # Ensure key is valid
            if not isinstance(key, str) or not key:
                raise ValidationError(f"Invalid environment variable name: {key}")

            value_str = str(value)

            # Quote if requested and contains spaces
            if quote_values and (" " in value_str or "\t" in value_str):
                value_str = f'"{value_str}"'

            lines.append(f"{key}={value_str}")

        return "\n".join(lines) + "\n"
    except Exception as e:
        raise ValidationError(f"Cannot serialize object to ENV format: {e}") from e


def _parse_env_line(line: str, line_num: int) -> tuple[str, str] | None:
    """Parse a single line from .env format.

    Args:
        line: Line to parse
        line_num: Line number for error messages

    Returns:
        (key, value) tuple or None if line should be skipped

    Raises:
        ValidationError: If line is invalid

    """
    from provide.foundation.errors import ValidationError

    line = line.strip()

    # Skip comments and empty lines
    if not line or line.startswith("#"):
        return None

    # Parse key=value
    if "=" not in line:
        raise ValidationError(f"Invalid .env format at line {line_num}: missing '='")

    key, value = line.split("=", 1)
    key = key.strip()
    value = value.strip()

    # Validate key
    if not key:
        raise ValidationError(f"Invalid .env format at line {line_num}: empty key")

    # Remove quotes if present
    if (value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith("'")):
        value = value[1:-1]

    return (key, value)


def env_loads(s: str, *, use_cache: bool = True) -> dict[str, str]:
    """Deserialize .env file format string to dictionary.

    Args:
        s: .env format string to deserialize
        use_cache: Whether to use caching for this operation

    Returns:
        Dictionary of environment variables

    Raises:
        ValidationError: If string is not valid .env format

    Example:
        >>> env_loads('KEY=value')
        {'KEY': 'value'}
        >>> env_loads('KEY="value"')
        {'KEY': 'value'}

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(s, str):
        raise ValidationError("Input must be a string")

    # Check cache first if enabled
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "env")
        cached = get_serialization_cache().get(cache_key)
        if cached is not None:
            return cached

    result: dict[str, str] = {}

    try:
        for line_num, line in enumerate(s.splitlines(), 1):
            parsed = _parse_env_line(line, line_num)
            if parsed is not None:
                key, value = parsed
                result[key] = value
    except ValidationError:
        raise
    except Exception as e:
        raise ValidationError(f"Invalid .env format string: {e}") from e

    # Cache result
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "env")
        get_serialization_cache().set(cache_key, result)

    return result


__all__ = [
    "env_dumps",
    "env_loads",
]

# 🧱🏗️🔚
