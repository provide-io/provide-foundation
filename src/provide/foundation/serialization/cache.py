# provide/foundation/serialization/cache.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import hashlib
import threading
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from provide.foundation.serialization.config import SerializationCacheConfig
    from provide.foundation.utils.caching import LRUCache

"""Caching utilities for serialization operations."""

# Cache configuration - lazy evaluation to avoid circular imports
_cached_config: Any | None = None  # SerializationCacheConfig
_serialization_cache: Any | None = None  # LRUCache
_cache_lock = threading.RLock()  # Use RLock to allow reentrant locking


def _get_cache_config() -> Any:  # SerializationCacheConfig
    """Get cache configuration with lazy initialization.

    Uses double-checked locking for thread-safe initialization.
    """
    global _cached_config

    # First check without lock (fast path)
    local_config = _cached_config
    if local_config is None:
        with _cache_lock:
            # Second check with lock held
            local_config = _cached_config
            if local_config is None:
                from provide.foundation.serialization.config import SerializationCacheConfig

                local_config = SerializationCacheConfig.from_env()
                _cached_config = local_config

    return local_config


def get_cache_enabled() -> bool:
    """Whether caching is enabled."""
    config = _get_cache_config()
    return config.cache_enabled


def get_cache_size() -> int:
    """Cache size limit."""
    config = _get_cache_config()
    return config.cache_size


def get_serialization_cache() -> Any:  # LRUCache
    """Get or create serialization cache with lazy initialization.

    Uses double-checked locking for thread-safe initialization.
    """
    global _serialization_cache

    # First check without lock (fast path for already initialized)
    local_cache = _serialization_cache
    if local_cache is None:
        with _cache_lock:
            # Second check with lock held (only one thread initializes)
            local_cache = _serialization_cache
            if local_cache is None:
                from provide.foundation.utils.caching import LRUCache, register_cache

                config = _get_cache_config()
                local_cache = LRUCache(maxsize=config.cache_size)
                _serialization_cache = local_cache
                register_cache("serialization", local_cache)

    return local_cache


def reset_serialization_cache_config() -> None:
    """Reset cached config for testing purposes.

    Thread-safe reset that acquires the lock.
    """
    global _cached_config, _serialization_cache
    with _cache_lock:
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
