# provide/foundation/serialization/cache.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import hashlib
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from provide.foundation.serialization.config import SerializationCacheConfig
    from provide.foundation.utils.caching import LRUCache

"""Caching utilities for serialization operations."""

# Cache configuration - lazy evaluation to avoid circular imports
_cached_config: SerializationCacheConfig | None = None
_serialization_cache: LRUCache | None = None


def _get_cache_config() -> SerializationCacheConfig:
    """Get cache configuration with lazy initialization."""
    global _cached_config
    if _cached_config is None:
        from provide.foundation.serialization.config import SerializationCacheConfig

        _cached_config = SerializationCacheConfig.from_env()
    return _cached_config


def get_cache_enabled() -> bool:
    """Whether caching is enabled."""
    config = _get_cache_config()
    return config.cache_enabled


def get_cache_size() -> int:
    """Cache size limit."""
    config = _get_cache_config()
    return config.cache_size


def get_serialization_cache() -> LRUCache:
    """Get or create serialization cache with lazy initialization."""
    global _serialization_cache
    if _serialization_cache is None:
        from provide.foundation.utils.caching import LRUCache, register_cache

        config = _get_cache_config()
        _serialization_cache = LRUCache(maxsize=config.cache_size)
        register_cache("serialization", _serialization_cache)
    return _serialization_cache


def reset_serialization_cache_config() -> None:
    """Reset cached config for testing purposes."""
    global _cached_config, _serialization_cache
    _cached_config = None
    _serialization_cache = None


# Convenience constants - use functions for actual access
CACHE_ENABLED = get_cache_enabled
CACHE_SIZE = get_cache_size
serialization_cache = get_serialization_cache


def get_cache_key(content: str, format: str) -> str:
    """Generate cache key from content and format.

    Args:
        content: String content to hash
        format: Format identifier (json, yaml, toml, etc.)

    Returns:
        Cache key string

    """
    content_hash = hashlib.sha256(content.encode()).hexdigest()[:16]
    return f"{format}:{content_hash}"


__all__ = [
    "CACHE_ENABLED",
    "CACHE_SIZE",
    "get_cache_key",
    "serialization_cache",
]


# <3 🧱🤝📜🪄
