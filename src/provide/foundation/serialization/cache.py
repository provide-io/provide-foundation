from __future__ import annotations

import hashlib
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from provide.foundation.utils.caching import LRUCache

"""Caching utilities for serialization operations."""

# Cache configuration - lazy evaluation to avoid circular imports
_CACHE_ENABLED: bool | None = None
_CACHE_SIZE: int | None = None
_serialization_cache: LRUCache | None = None


def _get_cache_config() -> tuple[bool, int]:
    """Get cache configuration with lazy initialization."""
    global _CACHE_ENABLED, _CACHE_SIZE
    if _CACHE_ENABLED is None or _CACHE_SIZE is None:
        from provide.foundation.utils.environment import get_bool, get_int

        _CACHE_ENABLED = get_bool("FOUNDATION_SERIALIZATION_CACHE_ENABLED", default=True)
        _CACHE_SIZE = get_int("FOUNDATION_SERIALIZATION_CACHE_SIZE", default=128)
    return _CACHE_ENABLED, _CACHE_SIZE


def get_cache_enabled() -> bool:
    """Whether caching is enabled."""
    enabled, _ = _get_cache_config()
    return enabled


def get_cache_size() -> int:
    """Cache size limit."""
    _, size = _get_cache_config()
    return size


def get_serialization_cache() -> LRUCache:
    """Get or create serialization cache with lazy initialization."""
    global _serialization_cache
    if _serialization_cache is None:
        from provide.foundation.utils.caching import LRUCache, register_cache

        _, size = _get_cache_config()
        _serialization_cache = LRUCache(maxsize=size)
        register_cache("serialization", _serialization_cache)
    return _serialization_cache


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
