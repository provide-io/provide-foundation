#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from __future__ import annotations

import tomllib
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    pass
from provide.foundation.serialization.cache import get_cache_enabled, get_cache_key, get_serialization_cache

"""TOML serialization with caching support."""


def toml_dumps(obj: dict[str, Any]) -> str:
    """Serialize dictionary to TOML string.

    Args:
        obj: Dictionary to serialize (TOML requires dict at top level)

    Returns:
        TOML string representation

    Raises:
        ValidationError: If object cannot be serialized
        ImportError: If tomli-w is not installed

    Example:
        >>> toml_dumps({"key": "value"})
        'key = "value"\\n'

    """
    from provide.foundation.errors import ValidationError

    try:
        import tomli_w
    except ImportError as e:
        raise ImportError("tomli-w is required for TOML write operations") from e

    if not isinstance(obj, dict):
        raise ValidationError("TOML serialization requires a dictionary at the top level")

    try:
        return tomli_w.dumps(obj)
    except Exception as e:
        raise ValidationError(f"Cannot serialize object to TOML: {e}") from e


def toml_loads(s: str, *, use_cache: bool = True) -> dict[str, Any]:
    """Deserialize TOML string to Python dictionary.

    Args:
        s: TOML string to deserialize
        use_cache: Whether to use caching for this operation

    Returns:
        Deserialized Python dictionary

    Raises:
        ValidationError: If string is not valid TOML

    Example:
        >>> toml_loads('key = "value"')
        {'key': 'value'}

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(s, str):
        raise ValidationError("Input must be a string")

    # Check cache first if enabled
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "toml")
        cached = get_serialization_cache().get(cache_key)
        if cached is not None:
            return cached

    try:
        result = tomllib.loads(s)
    except Exception as e:
        raise ValidationError(f"Invalid TOML string: {e}") from e

    # Cache result
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "toml")
        get_serialization_cache().set(cache_key, result)

    return result


__all__ = [
    "toml_dumps",
    "toml_loads",
]

# 🧱🏗️🔚
