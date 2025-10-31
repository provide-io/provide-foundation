#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from __future__ import annotations

import json
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    pass
from provide.foundation.serialization.cache import get_cache_enabled, get_cache_key, get_serialization_cache

"""JSON serialization with caching support."""


def json_dumps(
    obj: Any,
    *,
    ensure_ascii: bool = False,
    indent: int | None = None,
    sort_keys: bool = False,
    default: Any = None,
) -> str:
    """Serialize object to JSON string with Foundation tracking.

    Args:
        obj: Object to serialize
        ensure_ascii: If True, non-ASCII characters are escaped
        indent: Number of spaces for indentation (None for compact)
        sort_keys: Whether to sort dictionary keys
        default: Function called for objects that can't be serialized

    Returns:
        JSON string representation

    Raises:
        ValidationError: If object cannot be serialized

    Example:
        >>> json_dumps({"key": "value"})
        '{"key": "value"}'
        >>> json_dumps({"b": 1, "a": 2}, sort_keys=True, indent=2)
        '{\\n  "a": 2,\\n  "b": 1\\n}'

    """
    from provide.foundation.errors import ValidationError

    try:
        return json.dumps(obj, ensure_ascii=ensure_ascii, indent=indent, sort_keys=sort_keys, default=default)
    except (TypeError, ValueError) as e:
        raise ValidationError(f"Cannot serialize object to JSON: {e}") from e


def json_loads(s: str, *, use_cache: bool = True) -> Any:
    """Deserialize JSON string to Python object with Foundation tracking.

    Args:
        s: JSON string to deserialize
        use_cache: Whether to use caching for this operation

    Returns:
        Deserialized Python object

    Raises:
        ValidationError: If string is not valid JSON

    Example:
        >>> json_loads('{"key": "value"}')
        {'key': 'value'}
        >>> json_loads('[1, 2, 3]')
        [1, 2, 3]

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(s, str):
        raise ValidationError("Input must be a string")

    # Check cache first if enabled
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "json")
        cached = get_serialization_cache().get(cache_key)
        if cached is not None:
            return cached

    try:
        result = json.loads(s)
    except json.JSONDecodeError as e:
        raise ValidationError(f"Invalid JSON string: {e}") from e

    # Cache result
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "json")
        get_serialization_cache().set(cache_key, result)

    return result


__all__ = [
    "json_dumps",
    "json_loads",
]

# 🧱🏗️🔚
