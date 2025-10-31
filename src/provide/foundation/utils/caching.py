#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Caching utilities for Foundation.

Provides efficient caching mechanisms for frequently accessed data
with configurable size limits and optional TTL support."""

from __future__ import annotations

from collections import OrderedDict
from collections.abc import Callable
from functools import wraps
import threading
from typing import Any, TypeVar, cast

from provide.foundation.utils.environment import get_bool, get_int

# Configuration from environment
_CACHE_ENABLED = get_bool("FOUNDATION_CACHE_ENABLED", default=True)
_DEFAULT_CACHE_SIZE = get_int("FOUNDATION_CACHE_SIZE", default=128)

T = TypeVar("T")


class LRUCache:
    """Thread-safe LRU cache with configurable size.

    This is a simple LRU cache that maintains insertion order and
    evicts least recently used items when the cache is full.
    """

    def __init__(self, maxsize: int = 128) -> None:
        """Initialize LRU cache.

        Args:
            maxsize: Maximum number of items to cache
        """
        self.maxsize = maxsize
        self._cache: OrderedDict[Any, Any] = OrderedDict()
        self._lock = threading.RLock()
        self._hits = 0
        self._misses = 0

    def get(self, key: Any, default: Any = None) -> Any:
        """Get value from cache.

        Args:
            key: Cache key
            default: Default value if key not found

        Returns:
            Cached value or default
        """
        with self._lock:
            if key in self._cache:
                # Move to end (most recently used)
                self._cache.move_to_end(key)
                self._hits += 1
                return self._cache[key]
            self._misses += 1
            return default

    def set(self, key: Any, value: Any) -> None:
        """Set value in cache.

        Args:
            key: Cache key
            value: Value to cache
        """
        with self._lock:
            if key in self._cache:
                # Update existing and move to end
                self._cache.move_to_end(key)
            self._cache[key] = value

            # Evict oldest if over limit
            if len(self._cache) > self.maxsize:
                self._cache.popitem(last=False)

    def clear(self) -> None:
        """Clear all cached items."""
        with self._lock:
            self._cache.clear()
            self._hits = 0
            self._misses = 0

    def stats(self) -> dict[str, int | float]:
        """Get cache statistics.

        Returns:
            Dictionary with hits, misses, size, maxsize, and hit_rate
        """
        with self._lock:
            total = self._hits + self._misses
            hit_rate = (self._hits / total * 100) if total > 0 else 0.0
            return {
                "hits": self._hits,
                "misses": self._misses,
                "size": len(self._cache),
                "maxsize": self.maxsize,
                "hit_rate": hit_rate,
            }


def cached(maxsize: int = 128, enabled: bool | None = None) -> Callable:
    """Decorator to cache function results with LRU eviction.

    Args:
        maxsize: Maximum number of cached results
        enabled: Whether caching is enabled (defaults to FOUNDATION_CACHE_ENABLED)

    Returns:
        Decorated function with caching

    Example:
        >>> @cached(maxsize=100)
        ... def expensive_operation(x: int) -> int:
        ...     return x * x
    """
    cache_enabled = enabled if enabled is not None else _CACHE_ENABLED

    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        if not cache_enabled:
            # Return original function if caching disabled
            return func

        cache = LRUCache(maxsize=maxsize)

        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> T:
            # Create cache key from args and kwargs
            key = (args, tuple(sorted(kwargs.items())))

            result = cache.get(key)
            if result is None:
                result = func(*args, **kwargs)
                cache.set(key, result)

            return cast(T, result)

        # Attach cache object for testing/inspection
        wrapper.cache = cache  # type: ignore[attr-defined]
        wrapper.cache_clear = cache.clear  # type: ignore[attr-defined]
        wrapper.cache_stats = cache.stats  # type: ignore[attr-defined]

        return wrapper

    return decorator


# Global cache registry for testing and introspection
_cache_registry: dict[str, LRUCache] = {}
_registry_lock = threading.Lock()


def register_cache(name: str, cache: LRUCache) -> None:
    """Register a named cache for global management.

    Args:
        name: Cache identifier
        cache: Cache instance to register
    """
    with _registry_lock:
        _cache_registry[name] = cache


def get_cache(name: str) -> LRUCache | None:
    """Get a registered cache by name.

    Args:
        name: Cache identifier

    Returns:
        Cache instance or None if not found
    """
    with _registry_lock:
        return _cache_registry.get(name)


def clear_all_caches() -> None:
    """Clear all registered caches.

    Useful for testing and cache invalidation.
    """
    with _registry_lock:
        for cache in _cache_registry.values():
            cache.clear()


def get_cache_stats() -> dict[str, dict[str, int | float]]:
    """Get statistics for all registered caches.

    Returns:
        Dictionary mapping cache names to their statistics
    """
    with _registry_lock:
        return {name: cache.stats() for name, cache in _cache_registry.items()}


__all__ = [
    "LRUCache",
    "cached",
    "clear_all_caches",
    "get_cache",
    "get_cache_stats",
    "register_cache",
]

# 🧱🏗️🔚
