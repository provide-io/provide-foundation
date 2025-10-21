# provide/foundation/utils/scoped_cache.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

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
from inspect import signature as _mutmut_signature
from typing import Annotated
from typing import Callable
from typing import ClassVar


MutantDict = Annotated[dict[str, Callable], "Mutant"]


def _mutmut_trampoline(orig, mutants, call_args, call_kwargs, self_arg = None):
    """Forward call to original or mutated function, depending on the environment"""
    import os
    mutant_under_test = os.environ['MUTANT_UNDER_TEST']
    if mutant_under_test == 'fail':
        from mutmut.__main__ import MutmutProgrammaticFailException
        raise MutmutProgrammaticFailException('Failed programmatically')      
    elif mutant_under_test == 'stats':
        from mutmut.__main__ import record_trampoline_hit
        record_trampoline_hit(orig.__module__ + '.' + orig.__name__)
        result = orig(*call_args, **call_kwargs)
        return result
    prefix = orig.__module__ + '.' + orig.__name__ + '__mutmut_'
    if not mutant_under_test.startswith(prefix):
        result = orig(*call_args, **call_kwargs)
        return result
    mutant_name = mutant_under_test.rpartition('.')[-1]
    if self_arg:
        # call to a class method where self is not bound
        result = mutants[mutant_name](self_arg, *call_args, **call_kwargs)
    else:
        result = mutants[mutant_name](*call_args, **call_kwargs)
    return result


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

    def xǁContextScopedCacheǁ__init____mutmut_orig(self, name: str = "cache") -> None:
        """Initialize a context-scoped cache.

        Args:
            name: Identifier for the cache (used in ContextVar name)
        """
        self._context_var: ContextVar[dict[K, V] | None] = ContextVar(name, default=None)
        self.name = name

    def xǁContextScopedCacheǁ__init____mutmut_1(self, name: str = "XXcacheXX") -> None:
        """Initialize a context-scoped cache.

        Args:
            name: Identifier for the cache (used in ContextVar name)
        """
        self._context_var: ContextVar[dict[K, V] | None] = ContextVar(name, default=None)
        self.name = name

    def xǁContextScopedCacheǁ__init____mutmut_2(self, name: str = "CACHE") -> None:
        """Initialize a context-scoped cache.

        Args:
            name: Identifier for the cache (used in ContextVar name)
        """
        self._context_var: ContextVar[dict[K, V] | None] = ContextVar(name, default=None)
        self.name = name

    def xǁContextScopedCacheǁ__init____mutmut_3(self, name: str = "cache") -> None:
        """Initialize a context-scoped cache.

        Args:
            name: Identifier for the cache (used in ContextVar name)
        """
        self._context_var: ContextVar[dict[K, V] | None] = None
        self.name = name

    def xǁContextScopedCacheǁ__init____mutmut_4(self, name: str = "cache") -> None:
        """Initialize a context-scoped cache.

        Args:
            name: Identifier for the cache (used in ContextVar name)
        """
        self._context_var: ContextVar[dict[K, V] | None] = ContextVar(None, default=None)
        self.name = name

    def xǁContextScopedCacheǁ__init____mutmut_5(self, name: str = "cache") -> None:
        """Initialize a context-scoped cache.

        Args:
            name: Identifier for the cache (used in ContextVar name)
        """
        self._context_var: ContextVar[dict[K, V] | None] = ContextVar(default=None)
        self.name = name

    def xǁContextScopedCacheǁ__init____mutmut_6(self, name: str = "cache") -> None:
        """Initialize a context-scoped cache.

        Args:
            name: Identifier for the cache (used in ContextVar name)
        """
        self._context_var: ContextVar[dict[K, V] | None] = ContextVar(name, )
        self.name = name

    def xǁContextScopedCacheǁ__init____mutmut_7(self, name: str = "cache") -> None:
        """Initialize a context-scoped cache.

        Args:
            name: Identifier for the cache (used in ContextVar name)
        """
        self._context_var: ContextVar[dict[K, V] | None] = ContextVar(name, default=None)
        self.name = None
    
    xǁContextScopedCacheǁ__init____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁContextScopedCacheǁ__init____mutmut_1': xǁContextScopedCacheǁ__init____mutmut_1, 
        'xǁContextScopedCacheǁ__init____mutmut_2': xǁContextScopedCacheǁ__init____mutmut_2, 
        'xǁContextScopedCacheǁ__init____mutmut_3': xǁContextScopedCacheǁ__init____mutmut_3, 
        'xǁContextScopedCacheǁ__init____mutmut_4': xǁContextScopedCacheǁ__init____mutmut_4, 
        'xǁContextScopedCacheǁ__init____mutmut_5': xǁContextScopedCacheǁ__init____mutmut_5, 
        'xǁContextScopedCacheǁ__init____mutmut_6': xǁContextScopedCacheǁ__init____mutmut_6, 
        'xǁContextScopedCacheǁ__init____mutmut_7': xǁContextScopedCacheǁ__init____mutmut_7
    }
    
    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁContextScopedCacheǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁContextScopedCacheǁ__init____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __init__.__signature__ = _mutmut_signature(xǁContextScopedCacheǁ__init____mutmut_orig)
    xǁContextScopedCacheǁ__init____mutmut_orig.__name__ = 'xǁContextScopedCacheǁ__init__'

    @contextmanager
    def scope(self) -> Generator[None]:
        """Create an isolated cache scope.

        If a cache context already exists (nested call), reuses the
        existing cache. Otherwise, creates a new cache and cleans it
        up on exit.

        Yields:
            None (use cache methods within the context)

        Raises:
            No exceptions - cleanup is guaranteed even on errors
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

    def xǁContextScopedCacheǁget__mutmut_orig(self, key: K, default: V | None = None) -> V | None:
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

    def xǁContextScopedCacheǁget__mutmut_1(self, key: K, default: V | None = None) -> V | None:
        """Get value from current context's cache.

        Args:
            key: Cache key
            default: Value to return if key not found

        Returns:
            Cached value or default

        Raises:
            RuntimeError: If called outside a cache scope
        """
        cache = None
        if cache is None:
            raise RuntimeError(f"Cache '{self.name}' accessed outside scope context")
        return cache.get(key, default)

    def xǁContextScopedCacheǁget__mutmut_2(self, key: K, default: V | None = None) -> V | None:
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
        if cache is not None:
            raise RuntimeError(f"Cache '{self.name}' accessed outside scope context")
        return cache.get(key, default)

    def xǁContextScopedCacheǁget__mutmut_3(self, key: K, default: V | None = None) -> V | None:
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
            raise RuntimeError(None)
        return cache.get(key, default)

    def xǁContextScopedCacheǁget__mutmut_4(self, key: K, default: V | None = None) -> V | None:
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
        return cache.get(None, default)

    def xǁContextScopedCacheǁget__mutmut_5(self, key: K, default: V | None = None) -> V | None:
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
        return cache.get(key, None)

    def xǁContextScopedCacheǁget__mutmut_6(self, key: K, default: V | None = None) -> V | None:
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
        return cache.get(default)

    def xǁContextScopedCacheǁget__mutmut_7(self, key: K, default: V | None = None) -> V | None:
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
        return cache.get(key, )
    
    xǁContextScopedCacheǁget__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁContextScopedCacheǁget__mutmut_1': xǁContextScopedCacheǁget__mutmut_1, 
        'xǁContextScopedCacheǁget__mutmut_2': xǁContextScopedCacheǁget__mutmut_2, 
        'xǁContextScopedCacheǁget__mutmut_3': xǁContextScopedCacheǁget__mutmut_3, 
        'xǁContextScopedCacheǁget__mutmut_4': xǁContextScopedCacheǁget__mutmut_4, 
        'xǁContextScopedCacheǁget__mutmut_5': xǁContextScopedCacheǁget__mutmut_5, 
        'xǁContextScopedCacheǁget__mutmut_6': xǁContextScopedCacheǁget__mutmut_6, 
        'xǁContextScopedCacheǁget__mutmut_7': xǁContextScopedCacheǁget__mutmut_7
    }
    
    def get(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁContextScopedCacheǁget__mutmut_orig"), object.__getattribute__(self, "xǁContextScopedCacheǁget__mutmut_mutants"), args, kwargs, self)
        return result 
    
    get.__signature__ = _mutmut_signature(xǁContextScopedCacheǁget__mutmut_orig)
    xǁContextScopedCacheǁget__mutmut_orig.__name__ = 'xǁContextScopedCacheǁget'

    def xǁContextScopedCacheǁset__mutmut_orig(self, key: K, value: V) -> None:
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

    def xǁContextScopedCacheǁset__mutmut_1(self, key: K, value: V) -> None:
        """Set value in current context's cache.

        Args:
            key: Cache key
            value: Value to cache

        Raises:
            RuntimeError: If called outside a cache scope
        """
        cache = None
        if cache is None:
            raise RuntimeError(f"Cache '{self.name}' accessed outside scope context")
        cache[key] = value

    def xǁContextScopedCacheǁset__mutmut_2(self, key: K, value: V) -> None:
        """Set value in current context's cache.

        Args:
            key: Cache key
            value: Value to cache

        Raises:
            RuntimeError: If called outside a cache scope
        """
        cache = self._context_var.get()
        if cache is not None:
            raise RuntimeError(f"Cache '{self.name}' accessed outside scope context")
        cache[key] = value

    def xǁContextScopedCacheǁset__mutmut_3(self, key: K, value: V) -> None:
        """Set value in current context's cache.

        Args:
            key: Cache key
            value: Value to cache

        Raises:
            RuntimeError: If called outside a cache scope
        """
        cache = self._context_var.get()
        if cache is None:
            raise RuntimeError(None)
        cache[key] = value

    def xǁContextScopedCacheǁset__mutmut_4(self, key: K, value: V) -> None:
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
        cache[key] = None
    
    xǁContextScopedCacheǁset__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁContextScopedCacheǁset__mutmut_1': xǁContextScopedCacheǁset__mutmut_1, 
        'xǁContextScopedCacheǁset__mutmut_2': xǁContextScopedCacheǁset__mutmut_2, 
        'xǁContextScopedCacheǁset__mutmut_3': xǁContextScopedCacheǁset__mutmut_3, 
        'xǁContextScopedCacheǁset__mutmut_4': xǁContextScopedCacheǁset__mutmut_4
    }
    
    def set(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁContextScopedCacheǁset__mutmut_orig"), object.__getattribute__(self, "xǁContextScopedCacheǁset__mutmut_mutants"), args, kwargs, self)
        return result 
    
    set.__signature__ = _mutmut_signature(xǁContextScopedCacheǁset__mutmut_orig)
    xǁContextScopedCacheǁset__mutmut_orig.__name__ = 'xǁContextScopedCacheǁset'

    def xǁContextScopedCacheǁcontains__mutmut_orig(self, key: K) -> bool:
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

    def xǁContextScopedCacheǁcontains__mutmut_1(self, key: K) -> bool:
        """Check if key exists in current context's cache.

        Args:
            key: Cache key to check

        Returns:
            True if key exists in cache

        Raises:
            RuntimeError: If called outside a cache scope
        """
        cache = None
        if cache is None:
            raise RuntimeError(f"Cache '{self.name}' accessed outside scope context")
        return key in cache

    def xǁContextScopedCacheǁcontains__mutmut_2(self, key: K) -> bool:
        """Check if key exists in current context's cache.

        Args:
            key: Cache key to check

        Returns:
            True if key exists in cache

        Raises:
            RuntimeError: If called outside a cache scope
        """
        cache = self._context_var.get()
        if cache is not None:
            raise RuntimeError(f"Cache '{self.name}' accessed outside scope context")
        return key in cache

    def xǁContextScopedCacheǁcontains__mutmut_3(self, key: K) -> bool:
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
            raise RuntimeError(None)
        return key in cache

    def xǁContextScopedCacheǁcontains__mutmut_4(self, key: K) -> bool:
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
        return key not in cache
    
    xǁContextScopedCacheǁcontains__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁContextScopedCacheǁcontains__mutmut_1': xǁContextScopedCacheǁcontains__mutmut_1, 
        'xǁContextScopedCacheǁcontains__mutmut_2': xǁContextScopedCacheǁcontains__mutmut_2, 
        'xǁContextScopedCacheǁcontains__mutmut_3': xǁContextScopedCacheǁcontains__mutmut_3, 
        'xǁContextScopedCacheǁcontains__mutmut_4': xǁContextScopedCacheǁcontains__mutmut_4
    }
    
    def contains(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁContextScopedCacheǁcontains__mutmut_orig"), object.__getattribute__(self, "xǁContextScopedCacheǁcontains__mutmut_mutants"), args, kwargs, self)
        return result 
    
    contains.__signature__ = _mutmut_signature(xǁContextScopedCacheǁcontains__mutmut_orig)
    xǁContextScopedCacheǁcontains__mutmut_orig.__name__ = 'xǁContextScopedCacheǁcontains'

    def xǁContextScopedCacheǁclear__mutmut_orig(self) -> None:
        """Clear current context's cache.

        Raises:
            RuntimeError: If called outside a cache scope
        """
        cache = self._context_var.get()
        if cache is None:
            raise RuntimeError(f"Cache '{self.name}' accessed outside scope context")
        cache.clear()

    def xǁContextScopedCacheǁclear__mutmut_1(self) -> None:
        """Clear current context's cache.

        Raises:
            RuntimeError: If called outside a cache scope
        """
        cache = None
        if cache is None:
            raise RuntimeError(f"Cache '{self.name}' accessed outside scope context")
        cache.clear()

    def xǁContextScopedCacheǁclear__mutmut_2(self) -> None:
        """Clear current context's cache.

        Raises:
            RuntimeError: If called outside a cache scope
        """
        cache = self._context_var.get()
        if cache is not None:
            raise RuntimeError(f"Cache '{self.name}' accessed outside scope context")
        cache.clear()

    def xǁContextScopedCacheǁclear__mutmut_3(self) -> None:
        """Clear current context's cache.

        Raises:
            RuntimeError: If called outside a cache scope
        """
        cache = self._context_var.get()
        if cache is None:
            raise RuntimeError(None)
        cache.clear()
    
    xǁContextScopedCacheǁclear__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁContextScopedCacheǁclear__mutmut_1': xǁContextScopedCacheǁclear__mutmut_1, 
        'xǁContextScopedCacheǁclear__mutmut_2': xǁContextScopedCacheǁclear__mutmut_2, 
        'xǁContextScopedCacheǁclear__mutmut_3': xǁContextScopedCacheǁclear__mutmut_3
    }
    
    def clear(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁContextScopedCacheǁclear__mutmut_orig"), object.__getattribute__(self, "xǁContextScopedCacheǁclear__mutmut_mutants"), args, kwargs, self)
        return result 
    
    clear.__signature__ = _mutmut_signature(xǁContextScopedCacheǁclear__mutmut_orig)
    xǁContextScopedCacheǁclear__mutmut_orig.__name__ = 'xǁContextScopedCacheǁclear'

    def xǁContextScopedCacheǁsize__mutmut_orig(self) -> int:
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

    def xǁContextScopedCacheǁsize__mutmut_1(self) -> int:
        """Get number of items in current context's cache.

        Returns:
            Number of cached items

        Raises:
            RuntimeError: If called outside a cache scope
        """
        cache = None
        if cache is None:
            raise RuntimeError(f"Cache '{self.name}' accessed outside scope context")
        return len(cache)

    def xǁContextScopedCacheǁsize__mutmut_2(self) -> int:
        """Get number of items in current context's cache.

        Returns:
            Number of cached items

        Raises:
            RuntimeError: If called outside a cache scope
        """
        cache = self._context_var.get()
        if cache is not None:
            raise RuntimeError(f"Cache '{self.name}' accessed outside scope context")
        return len(cache)

    def xǁContextScopedCacheǁsize__mutmut_3(self) -> int:
        """Get number of items in current context's cache.

        Returns:
            Number of cached items

        Raises:
            RuntimeError: If called outside a cache scope
        """
        cache = self._context_var.get()
        if cache is None:
            raise RuntimeError(None)
        return len(cache)
    
    xǁContextScopedCacheǁsize__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁContextScopedCacheǁsize__mutmut_1': xǁContextScopedCacheǁsize__mutmut_1, 
        'xǁContextScopedCacheǁsize__mutmut_2': xǁContextScopedCacheǁsize__mutmut_2, 
        'xǁContextScopedCacheǁsize__mutmut_3': xǁContextScopedCacheǁsize__mutmut_3
    }
    
    def size(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁContextScopedCacheǁsize__mutmut_orig"), object.__getattribute__(self, "xǁContextScopedCacheǁsize__mutmut_mutants"), args, kwargs, self)
        return result 
    
    size.__signature__ = _mutmut_signature(xǁContextScopedCacheǁsize__mutmut_orig)
    xǁContextScopedCacheǁsize__mutmut_orig.__name__ = 'xǁContextScopedCacheǁsize'

    def xǁContextScopedCacheǁis_active__mutmut_orig(self) -> bool:
        """Check if cache context is currently active.

        Returns:
            True if inside a cache scope, False otherwise
        """
        return self._context_var.get() is not None

    def xǁContextScopedCacheǁis_active__mutmut_1(self) -> bool:
        """Check if cache context is currently active.

        Returns:
            True if inside a cache scope, False otherwise
        """
        return self._context_var.get() is None
    
    xǁContextScopedCacheǁis_active__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁContextScopedCacheǁis_active__mutmut_1': xǁContextScopedCacheǁis_active__mutmut_1
    }
    
    def is_active(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁContextScopedCacheǁis_active__mutmut_orig"), object.__getattribute__(self, "xǁContextScopedCacheǁis_active__mutmut_mutants"), args, kwargs, self)
        return result 
    
    is_active.__signature__ = _mutmut_signature(xǁContextScopedCacheǁis_active__mutmut_orig)
    xǁContextScopedCacheǁis_active__mutmut_orig.__name__ = 'xǁContextScopedCacheǁis_active'


__all__ = ["ContextScopedCache"]


# <3 🧱🤝🧰🪄
