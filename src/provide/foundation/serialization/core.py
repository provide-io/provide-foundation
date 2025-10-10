from __future__ import annotations

import json
from typing import Any

from provide.foundation.errors import ValidationError

"""Core serialization utilities for Foundation."""


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
    try:
        return json.dumps(
            obj, ensure_ascii=ensure_ascii, indent=indent, sort_keys=sort_keys, default=default
        )
    except (TypeError, ValueError) as e:
        raise ValidationError(f"Cannot serialize object to JSON: {e}") from e


def json_loads(s: str) -> Any:
    """Deserialize JSON string to Python object with Foundation tracking.

    Args:
        s: JSON string to deserialize

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
    if not isinstance(s, str):
        raise ValidationError("Input must be a string")

    try:
        return json.loads(s)
    except json.JSONDecodeError as e:
        raise ValidationError(f"Invalid JSON string: {e}") from e
