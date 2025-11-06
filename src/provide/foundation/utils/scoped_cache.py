#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from __future__ import annotations

from collections.abc import Generator
from contextlib import contextmanager
from contextvars import ContextVar
from typing import Generic, TypeVar

"""Context-scoped caching utilities for temporary state management.

Provides async-safe, thread-safe caching that's automatically scoped to
execution contexts. Unlike traditional LRU caches that persist globally,
scoped caches are isolated per-context and automatically cleaned up.

Use cases:
- Recursive operations needing temporary memoization
- DAG traversal with cycle detection
- Request-scoped data in async web applications
- Temporary object identity tracking during serialization
"""

K = TypeVar("K")
V = TypeVar("V")


class ContextScopedCache(Generic[K, V]):
    """Thread-safe, async-safe cache scoped to context managers.

    Unlike global LRU caches (for memoization), this provides isolated
    cache instances per execution context - ideal for recursive operations
    that need temporary storage without memory leaks.

    The cache uses ContextVar for automatic thread/async isolation, and
    context managers for automatic cleanup. Nested contexts reuse the
    parent's cache to maintain consistency within an operation.

    Examples:
        >>> cache = ContextScopedCache[str, int]("user_ids")
        >>>
        >>> with cache.scope():
        ...     cache.set("alice", 1)
        ...     cache.set("bob", 2)
        ...     print(cache.get("alice"))  # 1
        ...
        >>> # Cache is automatically cleared when exiting scope
        >>> with cache.scope():
        ...     print(cache.get("alice"))  # None (fresh scope)

        Nested contexts reuse parent cache:
        >>> with cache.scope():
        ...     cache.set("key", "outer")
        ...     with cache.scope():
        ...         print(cache.get("key"))  # "outer" (same cache)
        ...         cache.set("key", "inner")
        ...     print(cache.get("key"))  # "inner" (modified in nested scope)
    """

    def __init__(self, name: str = "cache") -> None:
        """Initialize a context-scoped cache.

        Args:
            name: Identifier for the cache (used in ContextVar name)
        """
        self._context_var: ContextVar[dict[K, V] | None] = ContextVar(name, default=None)
        self.name = name

    @contextmanager
    def scope(self) -> Generator[None]:
        """Create an isolated cache scope.

        If a cache context already exists (nested call), reuses the
        existing cache. Otherwise, creates a new cache and cleans it
        up on exit.

        Yields:
            None (use cache methods within the context)

        Note:
            Cleanup is guaranteed even on errors.
        """
        if self._context_var.get() is None:
            # No existing cache - create new scope
            token = self._context_var.set({})
            try:
                yield
            finally:
                self._context_var.reset(token)
        else:
            # Reuse existing cache (nested scope)
            yield

    def get(self, key: K, default: V | None = None) -> V | None:
        """Get value from current context's cache.

        Args:
            key: Cache key
            default: Value to return if key not found

        Returns:
            Cached value or default

        Raises:
            RuntimeError: If called outside a cache scope
        """
        cache = self._context_var.get()
        if cache is None:
            raise RuntimeError(f"Cache '{self.name}' accessed outside scope context")
        return cache.get(key, default)

    def set(self, key: K, value: V) -> None:
        """Set value in current context's cache.

        Args:
            key: Cache key
            value: Value to cache

        Raises:
            RuntimeError: If called outside a cache scope
        """
        cache = self._context_var.get()
        if cache is None:
            raise RuntimeError(f"Cache '{self.name}' accessed outside scope context")
        cache[key] = value

    def contains(self, key: K) -> bool:
        """Check if key exists in current context's cache.

        Args:
            key: Cache key to check

        Returns:
            True if key exists in cache

        Raises:
            RuntimeError: If called outside a cache scope
        """
        cache = self._context_var.get()
        if cache is None:
            raise RuntimeError(f"Cache '{self.name}' accessed outside scope context")
        return key in cache

    def clear(self) -> None:
        """Clear current context's cache.

        Raises:
            RuntimeError: If called outside a cache scope
        """
        cache = self._context_var.get()
        if cache is None:
            raise RuntimeError(f"Cache '{self.name}' accessed outside scope context")
        cache.clear()

    def size(self) -> int:
        """Get number of items in current context's cache.

        Returns:
            Number of cached items

        Raises:
            RuntimeError: If called outside a cache scope
        """
        cache = self._context_var.get()
        if cache is None:
            raise RuntimeError(f"Cache '{self.name}' accessed outside scope context")
        return len(cache)

    def is_active(self) -> bool:
        """Check if cache context is currently active.

        Returns:
            True if inside a cache scope, False otherwise
        """
        return self._context_var.get() is not None


__all__ = ["ContextScopedCache"]

# 🧱🏗️🔚
