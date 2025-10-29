# provide/foundation/utils/caching.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

"""Caching utilities for Foundation.

Provides efficient caching mechanisms for frequently accessed data
with configurable size limits and optional TTL support.
"""

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
from inspect import signature as _mutmut_signature
from typing import Annotated
from typing import Callable
from typing import ClassVar


MutantDict = Annotated[dict[str, Callable], "Mutant"]


def _mutmut_trampoline(orig, mutants, call_args, call_kwargs, self_arg=None):
    """Forward call to original or mutated function, depending on the environment"""
    import os

    mutant_under_test = os.environ["MUTANT_UNDER_TEST"]
    if mutant_under_test == "fail":
        from mutmut.__main__ import MutmutProgrammaticFailException

        raise MutmutProgrammaticFailException("Failed programmatically")
    elif mutant_under_test == "stats":
        from mutmut.__main__ import record_trampoline_hit

        record_trampoline_hit(orig.__module__ + "." + orig.__name__)
        result = orig(*call_args, **call_kwargs)
        return result
    prefix = orig.__module__ + "." + orig.__name__ + "__mutmut_"
    if not mutant_under_test.startswith(prefix):
        result = orig(*call_args, **call_kwargs)
        return result
    mutant_name = mutant_under_test.rpartition(".")[-1]
    if self_arg:
        # call to a class method where self is not bound
        result = mutants[mutant_name](self_arg, *call_args, **call_kwargs)
    else:
        result = mutants[mutant_name](*call_args, **call_kwargs)
    return result


class LRUCache:
    """Thread-safe LRU cache with configurable size.

    This is a simple LRU cache that maintains insertion order and
    evicts least recently used items when the cache is full.
    """

    def xǁLRUCacheǁ__init____mutmut_orig(self, maxsize: int = 128) -> None:
        """Initialize LRU cache.

        Args:
            maxsize: Maximum number of items to cache
        """
        self.maxsize = maxsize
        self._cache: OrderedDict[Any, Any] = OrderedDict()
        self._lock = threading.RLock()
        self._hits = 0
        self._misses = 0

    def xǁLRUCacheǁ__init____mutmut_1(self, maxsize: int = 129) -> None:
        """Initialize LRU cache.

        Args:
            maxsize: Maximum number of items to cache
        """
        self.maxsize = maxsize
        self._cache: OrderedDict[Any, Any] = OrderedDict()
        self._lock = threading.RLock()
        self._hits = 0
        self._misses = 0

    def xǁLRUCacheǁ__init____mutmut_2(self, maxsize: int = 128) -> None:
        """Initialize LRU cache.

        Args:
            maxsize: Maximum number of items to cache
        """
        self.maxsize = None
        self._cache: OrderedDict[Any, Any] = OrderedDict()
        self._lock = threading.RLock()
        self._hits = 0
        self._misses = 0

    def xǁLRUCacheǁ__init____mutmut_3(self, maxsize: int = 128) -> None:
        """Initialize LRU cache.

        Args:
            maxsize: Maximum number of items to cache
        """
        self.maxsize = maxsize
        self._cache: OrderedDict[Any, Any] = None
        self._lock = threading.RLock()
        self._hits = 0
        self._misses = 0

    def xǁLRUCacheǁ__init____mutmut_4(self, maxsize: int = 128) -> None:
        """Initialize LRU cache.

        Args:
            maxsize: Maximum number of items to cache
        """
        self.maxsize = maxsize
        self._cache: OrderedDict[Any, Any] = OrderedDict()
        self._lock = None
        self._hits = 0
        self._misses = 0

    def xǁLRUCacheǁ__init____mutmut_5(self, maxsize: int = 128) -> None:
        """Initialize LRU cache.

        Args:
            maxsize: Maximum number of items to cache
        """
        self.maxsize = maxsize
        self._cache: OrderedDict[Any, Any] = OrderedDict()
        self._lock = threading.RLock()
        self._hits = None
        self._misses = 0

    def xǁLRUCacheǁ__init____mutmut_6(self, maxsize: int = 128) -> None:
        """Initialize LRU cache.

        Args:
            maxsize: Maximum number of items to cache
        """
        self.maxsize = maxsize
        self._cache: OrderedDict[Any, Any] = OrderedDict()
        self._lock = threading.RLock()
        self._hits = 1
        self._misses = 0

    def xǁLRUCacheǁ__init____mutmut_7(self, maxsize: int = 128) -> None:
        """Initialize LRU cache.

        Args:
            maxsize: Maximum number of items to cache
        """
        self.maxsize = maxsize
        self._cache: OrderedDict[Any, Any] = OrderedDict()
        self._lock = threading.RLock()
        self._hits = 0
        self._misses = None

    def xǁLRUCacheǁ__init____mutmut_8(self, maxsize: int = 128) -> None:
        """Initialize LRU cache.

        Args:
            maxsize: Maximum number of items to cache
        """
        self.maxsize = maxsize
        self._cache: OrderedDict[Any, Any] = OrderedDict()
        self._lock = threading.RLock()
        self._hits = 0
        self._misses = 1

    xǁLRUCacheǁ__init____mutmut_mutants: ClassVar[MutantDict] = {
        "xǁLRUCacheǁ__init____mutmut_1": xǁLRUCacheǁ__init____mutmut_1,
        "xǁLRUCacheǁ__init____mutmut_2": xǁLRUCacheǁ__init____mutmut_2,
        "xǁLRUCacheǁ__init____mutmut_3": xǁLRUCacheǁ__init____mutmut_3,
        "xǁLRUCacheǁ__init____mutmut_4": xǁLRUCacheǁ__init____mutmut_4,
        "xǁLRUCacheǁ__init____mutmut_5": xǁLRUCacheǁ__init____mutmut_5,
        "xǁLRUCacheǁ__init____mutmut_6": xǁLRUCacheǁ__init____mutmut_6,
        "xǁLRUCacheǁ__init____mutmut_7": xǁLRUCacheǁ__init____mutmut_7,
        "xǁLRUCacheǁ__init____mutmut_8": xǁLRUCacheǁ__init____mutmut_8,
    }

    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁLRUCacheǁ__init____mutmut_orig"),
            object.__getattribute__(self, "xǁLRUCacheǁ__init____mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    __init__.__signature__ = _mutmut_signature(xǁLRUCacheǁ__init____mutmut_orig)
    xǁLRUCacheǁ__init____mutmut_orig.__name__ = "xǁLRUCacheǁ__init__"

    def xǁLRUCacheǁget__mutmut_orig(self, key: Any, default: Any = None) -> Any:
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

    def xǁLRUCacheǁget__mutmut_1(self, key: Any, default: Any = None) -> Any:
        """Get value from cache.

        Args:
            key: Cache key
            default: Default value if key not found

        Returns:
            Cached value or default
        """
        with self._lock:
            if key not in self._cache:
                # Move to end (most recently used)
                self._cache.move_to_end(key)
                self._hits += 1
                return self._cache[key]
            self._misses += 1
            return default

    def xǁLRUCacheǁget__mutmut_2(self, key: Any, default: Any = None) -> Any:
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
                self._cache.move_to_end(None)
                self._hits += 1
                return self._cache[key]
            self._misses += 1
            return default

    def xǁLRUCacheǁget__mutmut_3(self, key: Any, default: Any = None) -> Any:
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
                self._hits = 1
                return self._cache[key]
            self._misses += 1
            return default

    def xǁLRUCacheǁget__mutmut_4(self, key: Any, default: Any = None) -> Any:
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
                self._hits -= 1
                return self._cache[key]
            self._misses += 1
            return default

    def xǁLRUCacheǁget__mutmut_5(self, key: Any, default: Any = None) -> Any:
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
                self._hits += 2
                return self._cache[key]
            self._misses += 1
            return default

    def xǁLRUCacheǁget__mutmut_6(self, key: Any, default: Any = None) -> Any:
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
            self._misses = 1
            return default

    def xǁLRUCacheǁget__mutmut_7(self, key: Any, default: Any = None) -> Any:
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
            self._misses -= 1
            return default

    def xǁLRUCacheǁget__mutmut_8(self, key: Any, default: Any = None) -> Any:
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
            self._misses += 2
            return default

    xǁLRUCacheǁget__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁLRUCacheǁget__mutmut_1": xǁLRUCacheǁget__mutmut_1,
        "xǁLRUCacheǁget__mutmut_2": xǁLRUCacheǁget__mutmut_2,
        "xǁLRUCacheǁget__mutmut_3": xǁLRUCacheǁget__mutmut_3,
        "xǁLRUCacheǁget__mutmut_4": xǁLRUCacheǁget__mutmut_4,
        "xǁLRUCacheǁget__mutmut_5": xǁLRUCacheǁget__mutmut_5,
        "xǁLRUCacheǁget__mutmut_6": xǁLRUCacheǁget__mutmut_6,
        "xǁLRUCacheǁget__mutmut_7": xǁLRUCacheǁget__mutmut_7,
        "xǁLRUCacheǁget__mutmut_8": xǁLRUCacheǁget__mutmut_8,
    }

    def get(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁLRUCacheǁget__mutmut_orig"),
            object.__getattribute__(self, "xǁLRUCacheǁget__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    get.__signature__ = _mutmut_signature(xǁLRUCacheǁget__mutmut_orig)
    xǁLRUCacheǁget__mutmut_orig.__name__ = "xǁLRUCacheǁget"

    def xǁLRUCacheǁset__mutmut_orig(self, key: Any, value: Any) -> None:
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

    def xǁLRUCacheǁset__mutmut_1(self, key: Any, value: Any) -> None:
        """Set value in cache.

        Args:
            key: Cache key
            value: Value to cache
        """
        with self._lock:
            if key not in self._cache:
                # Update existing and move to end
                self._cache.move_to_end(key)
            self._cache[key] = value

            # Evict oldest if over limit
            if len(self._cache) > self.maxsize:
                self._cache.popitem(last=False)

    def xǁLRUCacheǁset__mutmut_2(self, key: Any, value: Any) -> None:
        """Set value in cache.

        Args:
            key: Cache key
            value: Value to cache
        """
        with self._lock:
            if key in self._cache:
                # Update existing and move to end
                self._cache.move_to_end(None)
            self._cache[key] = value

            # Evict oldest if over limit
            if len(self._cache) > self.maxsize:
                self._cache.popitem(last=False)

    def xǁLRUCacheǁset__mutmut_3(self, key: Any, value: Any) -> None:
        """Set value in cache.

        Args:
            key: Cache key
            value: Value to cache
        """
        with self._lock:
            if key in self._cache:
                # Update existing and move to end
                self._cache.move_to_end(key)
            self._cache[key] = None

            # Evict oldest if over limit
            if len(self._cache) > self.maxsize:
                self._cache.popitem(last=False)

    def xǁLRUCacheǁset__mutmut_4(self, key: Any, value: Any) -> None:
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
            if len(self._cache) >= self.maxsize:
                self._cache.popitem(last=False)

    def xǁLRUCacheǁset__mutmut_5(self, key: Any, value: Any) -> None:
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
                self._cache.popitem(last=None)

    def xǁLRUCacheǁset__mutmut_6(self, key: Any, value: Any) -> None:
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
                self._cache.popitem(last=True)

    xǁLRUCacheǁset__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁLRUCacheǁset__mutmut_1": xǁLRUCacheǁset__mutmut_1,
        "xǁLRUCacheǁset__mutmut_2": xǁLRUCacheǁset__mutmut_2,
        "xǁLRUCacheǁset__mutmut_3": xǁLRUCacheǁset__mutmut_3,
        "xǁLRUCacheǁset__mutmut_4": xǁLRUCacheǁset__mutmut_4,
        "xǁLRUCacheǁset__mutmut_5": xǁLRUCacheǁset__mutmut_5,
        "xǁLRUCacheǁset__mutmut_6": xǁLRUCacheǁset__mutmut_6,
    }

    def set(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁLRUCacheǁset__mutmut_orig"),
            object.__getattribute__(self, "xǁLRUCacheǁset__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    set.__signature__ = _mutmut_signature(xǁLRUCacheǁset__mutmut_orig)
    xǁLRUCacheǁset__mutmut_orig.__name__ = "xǁLRUCacheǁset"

    def xǁLRUCacheǁclear__mutmut_orig(self) -> None:
        """Clear all cached items."""
        with self._lock:
            self._cache.clear()
            self._hits = 0
            self._misses = 0

    def xǁLRUCacheǁclear__mutmut_1(self) -> None:
        """Clear all cached items."""
        with self._lock:
            self._cache.clear()
            self._hits = None
            self._misses = 0

    def xǁLRUCacheǁclear__mutmut_2(self) -> None:
        """Clear all cached items."""
        with self._lock:
            self._cache.clear()
            self._hits = 1
            self._misses = 0

    def xǁLRUCacheǁclear__mutmut_3(self) -> None:
        """Clear all cached items."""
        with self._lock:
            self._cache.clear()
            self._hits = 0
            self._misses = None

    def xǁLRUCacheǁclear__mutmut_4(self) -> None:
        """Clear all cached items."""
        with self._lock:
            self._cache.clear()
            self._hits = 0
            self._misses = 1

    xǁLRUCacheǁclear__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁLRUCacheǁclear__mutmut_1": xǁLRUCacheǁclear__mutmut_1,
        "xǁLRUCacheǁclear__mutmut_2": xǁLRUCacheǁclear__mutmut_2,
        "xǁLRUCacheǁclear__mutmut_3": xǁLRUCacheǁclear__mutmut_3,
        "xǁLRUCacheǁclear__mutmut_4": xǁLRUCacheǁclear__mutmut_4,
    }

    def clear(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁLRUCacheǁclear__mutmut_orig"),
            object.__getattribute__(self, "xǁLRUCacheǁclear__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    clear.__signature__ = _mutmut_signature(xǁLRUCacheǁclear__mutmut_orig)
    xǁLRUCacheǁclear__mutmut_orig.__name__ = "xǁLRUCacheǁclear"

    def xǁLRUCacheǁstats__mutmut_orig(self) -> dict[str, int | float]:
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

    def xǁLRUCacheǁstats__mutmut_1(self) -> dict[str, int | float]:
        """Get cache statistics.

        Returns:
            Dictionary with hits, misses, size, maxsize, and hit_rate
        """
        with self._lock:
            total = None
            hit_rate = (self._hits / total * 100) if total > 0 else 0.0
            return {
                "hits": self._hits,
                "misses": self._misses,
                "size": len(self._cache),
                "maxsize": self.maxsize,
                "hit_rate": hit_rate,
            }

    def xǁLRUCacheǁstats__mutmut_2(self) -> dict[str, int | float]:
        """Get cache statistics.

        Returns:
            Dictionary with hits, misses, size, maxsize, and hit_rate
        """
        with self._lock:
            total = self._hits - self._misses
            hit_rate = (self._hits / total * 100) if total > 0 else 0.0
            return {
                "hits": self._hits,
                "misses": self._misses,
                "size": len(self._cache),
                "maxsize": self.maxsize,
                "hit_rate": hit_rate,
            }

    def xǁLRUCacheǁstats__mutmut_3(self) -> dict[str, int | float]:
        """Get cache statistics.

        Returns:
            Dictionary with hits, misses, size, maxsize, and hit_rate
        """
        with self._lock:
            total = self._hits + self._misses
            hit_rate = None
            return {
                "hits": self._hits,
                "misses": self._misses,
                "size": len(self._cache),
                "maxsize": self.maxsize,
                "hit_rate": hit_rate,
            }

    def xǁLRUCacheǁstats__mutmut_4(self) -> dict[str, int | float]:
        """Get cache statistics.

        Returns:
            Dictionary with hits, misses, size, maxsize, and hit_rate
        """
        with self._lock:
            total = self._hits + self._misses
            hit_rate = (self._hits / total / 100) if total > 0 else 0.0
            return {
                "hits": self._hits,
                "misses": self._misses,
                "size": len(self._cache),
                "maxsize": self.maxsize,
                "hit_rate": hit_rate,
            }

    def xǁLRUCacheǁstats__mutmut_5(self) -> dict[str, int | float]:
        """Get cache statistics.

        Returns:
            Dictionary with hits, misses, size, maxsize, and hit_rate
        """
        with self._lock:
            total = self._hits + self._misses
            hit_rate = (self._hits * total * 100) if total > 0 else 0.0
            return {
                "hits": self._hits,
                "misses": self._misses,
                "size": len(self._cache),
                "maxsize": self.maxsize,
                "hit_rate": hit_rate,
            }

    def xǁLRUCacheǁstats__mutmut_6(self) -> dict[str, int | float]:
        """Get cache statistics.

        Returns:
            Dictionary with hits, misses, size, maxsize, and hit_rate
        """
        with self._lock:
            total = self._hits + self._misses
            hit_rate = (self._hits / total * 101) if total > 0 else 0.0
            return {
                "hits": self._hits,
                "misses": self._misses,
                "size": len(self._cache),
                "maxsize": self.maxsize,
                "hit_rate": hit_rate,
            }

    def xǁLRUCacheǁstats__mutmut_7(self) -> dict[str, int | float]:
        """Get cache statistics.

        Returns:
            Dictionary with hits, misses, size, maxsize, and hit_rate
        """
        with self._lock:
            total = self._hits + self._misses
            hit_rate = (self._hits / total * 100) if total >= 0 else 0.0
            return {
                "hits": self._hits,
                "misses": self._misses,
                "size": len(self._cache),
                "maxsize": self.maxsize,
                "hit_rate": hit_rate,
            }

    def xǁLRUCacheǁstats__mutmut_8(self) -> dict[str, int | float]:
        """Get cache statistics.

        Returns:
            Dictionary with hits, misses, size, maxsize, and hit_rate
        """
        with self._lock:
            total = self._hits + self._misses
            hit_rate = (self._hits / total * 100) if total > 1 else 0.0
            return {
                "hits": self._hits,
                "misses": self._misses,
                "size": len(self._cache),
                "maxsize": self.maxsize,
                "hit_rate": hit_rate,
            }

    def xǁLRUCacheǁstats__mutmut_9(self) -> dict[str, int | float]:
        """Get cache statistics.

        Returns:
            Dictionary with hits, misses, size, maxsize, and hit_rate
        """
        with self._lock:
            total = self._hits + self._misses
            hit_rate = (self._hits / total * 100) if total > 0 else 1.0
            return {
                "hits": self._hits,
                "misses": self._misses,
                "size": len(self._cache),
                "maxsize": self.maxsize,
                "hit_rate": hit_rate,
            }

    def xǁLRUCacheǁstats__mutmut_10(self) -> dict[str, int | float]:
        """Get cache statistics.

        Returns:
            Dictionary with hits, misses, size, maxsize, and hit_rate
        """
        with self._lock:
            total = self._hits + self._misses
            hit_rate = (self._hits / total * 100) if total > 0 else 0.0
            return {
                "XXhitsXX": self._hits,
                "misses": self._misses,
                "size": len(self._cache),
                "maxsize": self.maxsize,
                "hit_rate": hit_rate,
            }

    def xǁLRUCacheǁstats__mutmut_11(self) -> dict[str, int | float]:
        """Get cache statistics.

        Returns:
            Dictionary with hits, misses, size, maxsize, and hit_rate
        """
        with self._lock:
            total = self._hits + self._misses
            hit_rate = (self._hits / total * 100) if total > 0 else 0.0
            return {
                "HITS": self._hits,
                "misses": self._misses,
                "size": len(self._cache),
                "maxsize": self.maxsize,
                "hit_rate": hit_rate,
            }

    def xǁLRUCacheǁstats__mutmut_12(self) -> dict[str, int | float]:
        """Get cache statistics.

        Returns:
            Dictionary with hits, misses, size, maxsize, and hit_rate
        """
        with self._lock:
            total = self._hits + self._misses
            hit_rate = (self._hits / total * 100) if total > 0 else 0.0
            return {
                "hits": self._hits,
                "XXmissesXX": self._misses,
                "size": len(self._cache),
                "maxsize": self.maxsize,
                "hit_rate": hit_rate,
            }

    def xǁLRUCacheǁstats__mutmut_13(self) -> dict[str, int | float]:
        """Get cache statistics.

        Returns:
            Dictionary with hits, misses, size, maxsize, and hit_rate
        """
        with self._lock:
            total = self._hits + self._misses
            hit_rate = (self._hits / total * 100) if total > 0 else 0.0
            return {
                "hits": self._hits,
                "MISSES": self._misses,
                "size": len(self._cache),
                "maxsize": self.maxsize,
                "hit_rate": hit_rate,
            }

    def xǁLRUCacheǁstats__mutmut_14(self) -> dict[str, int | float]:
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
                "XXsizeXX": len(self._cache),
                "maxsize": self.maxsize,
                "hit_rate": hit_rate,
            }

    def xǁLRUCacheǁstats__mutmut_15(self) -> dict[str, int | float]:
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
                "SIZE": len(self._cache),
                "maxsize": self.maxsize,
                "hit_rate": hit_rate,
            }

    def xǁLRUCacheǁstats__mutmut_16(self) -> dict[str, int | float]:
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
                "XXmaxsizeXX": self.maxsize,
                "hit_rate": hit_rate,
            }

    def xǁLRUCacheǁstats__mutmut_17(self) -> dict[str, int | float]:
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
                "MAXSIZE": self.maxsize,
                "hit_rate": hit_rate,
            }

    def xǁLRUCacheǁstats__mutmut_18(self) -> dict[str, int | float]:
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
                "XXhit_rateXX": hit_rate,
            }

    def xǁLRUCacheǁstats__mutmut_19(self) -> dict[str, int | float]:
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
                "HIT_RATE": hit_rate,
            }

    xǁLRUCacheǁstats__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁLRUCacheǁstats__mutmut_1": xǁLRUCacheǁstats__mutmut_1,
        "xǁLRUCacheǁstats__mutmut_2": xǁLRUCacheǁstats__mutmut_2,
        "xǁLRUCacheǁstats__mutmut_3": xǁLRUCacheǁstats__mutmut_3,
        "xǁLRUCacheǁstats__mutmut_4": xǁLRUCacheǁstats__mutmut_4,
        "xǁLRUCacheǁstats__mutmut_5": xǁLRUCacheǁstats__mutmut_5,
        "xǁLRUCacheǁstats__mutmut_6": xǁLRUCacheǁstats__mutmut_6,
        "xǁLRUCacheǁstats__mutmut_7": xǁLRUCacheǁstats__mutmut_7,
        "xǁLRUCacheǁstats__mutmut_8": xǁLRUCacheǁstats__mutmut_8,
        "xǁLRUCacheǁstats__mutmut_9": xǁLRUCacheǁstats__mutmut_9,
        "xǁLRUCacheǁstats__mutmut_10": xǁLRUCacheǁstats__mutmut_10,
        "xǁLRUCacheǁstats__mutmut_11": xǁLRUCacheǁstats__mutmut_11,
        "xǁLRUCacheǁstats__mutmut_12": xǁLRUCacheǁstats__mutmut_12,
        "xǁLRUCacheǁstats__mutmut_13": xǁLRUCacheǁstats__mutmut_13,
        "xǁLRUCacheǁstats__mutmut_14": xǁLRUCacheǁstats__mutmut_14,
        "xǁLRUCacheǁstats__mutmut_15": xǁLRUCacheǁstats__mutmut_15,
        "xǁLRUCacheǁstats__mutmut_16": xǁLRUCacheǁstats__mutmut_16,
        "xǁLRUCacheǁstats__mutmut_17": xǁLRUCacheǁstats__mutmut_17,
        "xǁLRUCacheǁstats__mutmut_18": xǁLRUCacheǁstats__mutmut_18,
        "xǁLRUCacheǁstats__mutmut_19": xǁLRUCacheǁstats__mutmut_19,
    }

    def stats(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁLRUCacheǁstats__mutmut_orig"),
            object.__getattribute__(self, "xǁLRUCacheǁstats__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    stats.__signature__ = _mutmut_signature(xǁLRUCacheǁstats__mutmut_orig)
    xǁLRUCacheǁstats__mutmut_orig.__name__ = "xǁLRUCacheǁstats"


def x_cached__mutmut_orig(maxsize: int = 128, enabled: bool | None = None) -> Callable:
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


def x_cached__mutmut_1(maxsize: int = 129, enabled: bool | None = None) -> Callable:
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


def x_cached__mutmut_2(maxsize: int = 128, enabled: bool | None = None) -> Callable:
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
    cache_enabled = None

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


def x_cached__mutmut_3(maxsize: int = 128, enabled: bool | None = None) -> Callable:
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
    cache_enabled = enabled if enabled is None else _CACHE_ENABLED

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


def x_cached__mutmut_4(maxsize: int = 128, enabled: bool | None = None) -> Callable:
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
        if cache_enabled:
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


def x_cached__mutmut_5(maxsize: int = 128, enabled: bool | None = None) -> Callable:
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

        cache = None

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


def x_cached__mutmut_6(maxsize: int = 128, enabled: bool | None = None) -> Callable:
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

        cache = LRUCache(maxsize=None)

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


def x_cached__mutmut_7(maxsize: int = 128, enabled: bool | None = None) -> Callable:
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
        wrapper.cache = None  # type: ignore[attr-defined]
        wrapper.cache_clear = cache.clear  # type: ignore[attr-defined]
        wrapper.cache_stats = cache.stats  # type: ignore[attr-defined]

        return wrapper

    return decorator


def x_cached__mutmut_8(maxsize: int = 128, enabled: bool | None = None) -> Callable:
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
        wrapper.cache_clear = None  # type: ignore[attr-defined]
        wrapper.cache_stats = cache.stats  # type: ignore[attr-defined]

        return wrapper

    return decorator


def x_cached__mutmut_9(maxsize: int = 128, enabled: bool | None = None) -> Callable:
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
        wrapper.cache_stats = None  # type: ignore[attr-defined]

        return wrapper

    return decorator


x_cached__mutmut_mutants: ClassVar[MutantDict] = {
    "x_cached__mutmut_1": x_cached__mutmut_1,
    "x_cached__mutmut_2": x_cached__mutmut_2,
    "x_cached__mutmut_3": x_cached__mutmut_3,
    "x_cached__mutmut_4": x_cached__mutmut_4,
    "x_cached__mutmut_5": x_cached__mutmut_5,
    "x_cached__mutmut_6": x_cached__mutmut_6,
    "x_cached__mutmut_7": x_cached__mutmut_7,
    "x_cached__mutmut_8": x_cached__mutmut_8,
    "x_cached__mutmut_9": x_cached__mutmut_9,
}


def cached(*args, **kwargs):
    result = _mutmut_trampoline(x_cached__mutmut_orig, x_cached__mutmut_mutants, args, kwargs)
    return result


cached.__signature__ = _mutmut_signature(x_cached__mutmut_orig)
x_cached__mutmut_orig.__name__ = "x_cached"


# Global cache registry for testing and introspection
_cache_registry: dict[str, LRUCache] = {}
_registry_lock = threading.Lock()


def x_register_cache__mutmut_orig(name: str, cache: LRUCache) -> None:
    """Register a named cache for global management.

    Args:
        name: Cache identifier
        cache: Cache instance to register
    """
    with _registry_lock:
        _cache_registry[name] = cache


def x_register_cache__mutmut_1(name: str, cache: LRUCache) -> None:
    """Register a named cache for global management.

    Args:
        name: Cache identifier
        cache: Cache instance to register
    """
    with _registry_lock:
        _cache_registry[name] = None


x_register_cache__mutmut_mutants: ClassVar[MutantDict] = {
    "x_register_cache__mutmut_1": x_register_cache__mutmut_1
}


def register_cache(*args, **kwargs):
    result = _mutmut_trampoline(x_register_cache__mutmut_orig, x_register_cache__mutmut_mutants, args, kwargs)
    return result


register_cache.__signature__ = _mutmut_signature(x_register_cache__mutmut_orig)
x_register_cache__mutmut_orig.__name__ = "x_register_cache"


def x_get_cache__mutmut_orig(name: str) -> LRUCache | None:
    """Get a registered cache by name.

    Args:
        name: Cache identifier

    Returns:
        Cache instance or None if not found
    """
    with _registry_lock:
        return _cache_registry.get(name)


def x_get_cache__mutmut_1(name: str) -> LRUCache | None:
    """Get a registered cache by name.

    Args:
        name: Cache identifier

    Returns:
        Cache instance or None if not found
    """
    with _registry_lock:
        return _cache_registry.get(None)


x_get_cache__mutmut_mutants: ClassVar[MutantDict] = {"x_get_cache__mutmut_1": x_get_cache__mutmut_1}


def get_cache(*args, **kwargs):
    result = _mutmut_trampoline(x_get_cache__mutmut_orig, x_get_cache__mutmut_mutants, args, kwargs)
    return result


get_cache.__signature__ = _mutmut_signature(x_get_cache__mutmut_orig)
x_get_cache__mutmut_orig.__name__ = "x_get_cache"


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


# <3 🧱🤝🧰🪄
