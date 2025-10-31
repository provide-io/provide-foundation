#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    pass
from provide.foundation.serialization.cache import get_cache_enabled, get_cache_key, get_serialization_cache

"""YAML serialization with caching support."""


def yaml_dumps(
    obj: Any,
    *,
    default_flow_style: bool = False,
    allow_unicode: bool = True,
    sort_keys: bool = False,
) -> str:
    """Serialize object to YAML string.

    Args:
        obj: Object to serialize
        default_flow_style: Use flow style (JSON-like) instead of block style
        allow_unicode: If True, allow unicode characters
        sort_keys: Whether to sort dictionary keys

    Returns:
        YAML string representation

    Raises:
        ValidationError: If object cannot be serialized
        ImportError: If PyYAML is not installed

    Example:
        >>> yaml_dumps({"key": "value"})
        'key: value\\n'

    """
    try:
        import yaml
    except ImportError as e:
        raise ImportError("PyYAML is required for YAML operations") from e

    from provide.foundation.errors import ValidationError

    try:
        return yaml.dump(
            obj,
            default_flow_style=default_flow_style,
            allow_unicode=allow_unicode,
            sort_keys=sort_keys,
        )
    except Exception as e:
        raise ValidationError(f"Cannot serialize object to YAML: {e}") from e


def yaml_loads(s: str, *, use_cache: bool = True) -> Any:
    """Deserialize YAML string to Python object.

    Args:
        s: YAML string to deserialize
        use_cache: Whether to use caching for this operation

    Returns:
        Deserialized Python object

    Raises:
        ValidationError: If string is not valid YAML
        ImportError: If PyYAML is not installed

    Example:
        >>> yaml_loads('key: value')
        {'key': 'value'}
        >>> yaml_loads('[1, 2, 3]')
        [1, 2, 3]

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(s, str):
        raise ValidationError("Input must be a string")

    try:
        import yaml
    except ImportError as e:
        raise ImportError("PyYAML is required for YAML operations") from e

    # Check cache first if enabled
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "yaml")
        cached = get_serialization_cache().get(cache_key)
        if cached is not None:
            return cached

    try:
        result = yaml.safe_load(s)
    except yaml.YAMLError as e:
        raise ValidationError(f"Invalid YAML string: {e}") from e

    # Cache result
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "yaml")
        get_serialization_cache().set(cache_key, result)

    return result


__all__ = [
    "yaml_dumps",
    "yaml_loads",
]

# 🧱🏗️🔚
