from __future__ import annotations

import hashlib

from provide.foundation.utils.caching import LRUCache, register_cache
from provide.foundation.utils.environment import get_bool, get_int

"""Caching utilities for serialization operations."""

# Cache configuration
CACHE_ENABLED = get_bool("FOUNDATION_SERIALIZATION_CACHE_ENABLED", default=True)
CACHE_SIZE = get_int("FOUNDATION_SERIALIZATION_CACHE_SIZE", default=128)

# Create and register serialization cache
serialization_cache = LRUCache(maxsize=CACHE_SIZE)
register_cache("serialization", serialization_cache)


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
