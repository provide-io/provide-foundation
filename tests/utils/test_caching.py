#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for caching utilities."""

from __future__ import annotations

import threading
import time

from provide.testkit import FoundationTestCase
import pytest

from provide.foundation.utils.caching import (
    LRUCache,
    cached,
    clear_all_caches,
    get_cache_stats,
    register_cache,
)


class TestLRUCache(FoundationTestCase):
    """Test LRUCache functionality."""

    def test_basic_get_set(self) -> None:
        """Test basic cache get/set operations."""
        cache = LRUCache(maxsize=3)

        cache.set("key1", "value1")
        cache.set("key2", "value2")

        assert cache.get("key1") == "value1"
        assert cache.get("key2") == "value2"
        assert cache.get("key3") is None

    def test_lru_eviction(self) -> None:
        """Test that least recently used items are evicted."""
        cache = LRUCache(maxsize=3)

        cache.set("a", 1)
        cache.set("b", 2)
        cache.set("c", 3)

        # Access 'a' to make it most recently used
        cache.get("a")

        # Add new item, should evict 'b'
        cache.set("d", 4)

        assert cache.get("a") == 1
        assert cache.get("b") is None  # Evicted
        assert cache.get("c") == 3
        assert cache.get("d") == 4

    def test_update_existing(self) -> None:
        """Test updating existing cache entries."""
        cache = LRUCache(maxsize=3)

        cache.set("key", "value1")
        cache.set("key", "value2")

        assert cache.get("key") == "value2"
        # Should not increase size
        assert cache.stats()["size"] == 1

    def test_clear(self) -> None:
        """Test clearing cache."""
        cache = LRUCache(maxsize=3)

        cache.set("a", 1)
        cache.set("b", 2)
        cache.clear()

        assert cache.get("a") is None
        assert cache.stats()["size"] == 0

    def test_stats(self) -> None:
        """Test cache statistics."""
        cache = LRUCache(maxsize=10)

        # Initial stats
        stats = cache.stats()
        assert stats["hits"] == 0
        assert stats["misses"] == 0
        assert stats["size"] == 0
        assert stats["hit_rate"] == 0.0

        # Add items and access
        cache.set("a", 1)
        cache.set("b", 2)
        cache.get("a")  # Hit
        cache.get("c")  # Miss

        stats = cache.stats()
        assert stats["hits"] == 1
        assert stats["misses"] == 1
        assert stats["size"] == 2
        assert stats["hit_rate"] == 50.0

    def test_thread_safety(self) -> None:
        """Test that cache is thread-safe."""
        cache = LRUCache(maxsize=100)
        iterations = 100

        def writer(start: int) -> None:
            for i in range(iterations):
                cache.set(f"key_{start}_{i}", i)

        def reader(start: int) -> None:
            for i in range(iterations):
                cache.get(f"key_{start}_{i}")

        threads = []
        for i in range(5):
            threads.append(threading.Thread(target=writer, args=(i,)))
            threads.append(threading.Thread(target=reader, args=(i,)))

        for t in threads:
            t.start()
        for t in threads:
            t.join()

        # Should complete without errors
        assert cache.stats()["size"] <= 100


class TestCachedDecorator(FoundationTestCase):
    """Test @cached decorator."""

    def test_basic_caching(self) -> None:
        """Test basic function result caching."""
        call_count = 0

        @cached(maxsize=10)
        def expensive_func(x: int) -> int:
            nonlocal call_count
            call_count += 1
            return x * x

        # First call
        result1 = expensive_func(5)
        assert result1 == 25
        assert call_count == 1

        # Second call with same args - should use cache
        result2 = expensive_func(5)
        assert result2 == 25
        assert call_count == 1  # Not incremented

        # Different args
        result3 = expensive_func(6)
        assert result3 == 36
        assert call_count == 2

    def test_cache_with_kwargs(self) -> None:
        """Test caching with keyword arguments."""
        call_count = 0

        @cached(maxsize=10)
        def func_with_kwargs(a: int, b: int = 10) -> int:
            nonlocal call_count
            call_count += 1
            return a + b

        func_with_kwargs(5, b=10)
        func_with_kwargs(5, b=10)  # Should use cache

        assert call_count == 1

        func_with_kwargs(5, b=20)  # Different kwargs

        assert call_count == 2

    def test_cache_clear(self) -> None:
        """Test cache clearing."""
        call_count = 0

        @cached(maxsize=10)
        def func(x: int) -> int:
            nonlocal call_count
            call_count += 1
            return x

        func(1)
        func(1)  # Cached
        assert call_count == 1

        func.cache_clear()

        func(1)  # Should call again after clear
        assert call_count == 2

    def test_cache_stats(self) -> None:
        """Test cache statistics access."""

        @cached(maxsize=10)
        def func(x: int) -> int:
            return x * 2

        func(1)
        func(1)  # Hit
        func(2)  # Miss

        stats = func.cache_stats()
        assert stats["hits"] >= 1
        assert stats["misses"] >= 1

    def test_cache_disabled(self) -> None:
        """Test that caching can be disabled."""
        call_count = 0

        @cached(maxsize=10, enabled=False)
        def func(x: int) -> int:
            nonlocal call_count
            call_count += 1
            return x

        func(1)
        func(1)  # Should NOT use cache

        assert call_count == 2


class TestCacheRegistry(FoundationTestCase):
    """Test cache registry functionality."""

    def test_register_and_clear_all(self) -> None:
        """Test registering caches and clearing all."""
        cache1 = LRUCache(maxsize=10)
        cache2 = LRUCache(maxsize=10)

        register_cache("test_cache1", cache1)
        register_cache("test_cache2", cache2)

        cache1.set("a", 1)
        cache2.set("b", 2)

        clear_all_caches()

        assert cache1.get("a") is None
        assert cache2.get("b") is None

    def test_get_cache_stats(self) -> None:
        """Test getting stats for all caches."""
        cache1 = LRUCache(maxsize=10)
        cache2 = LRUCache(maxsize=10)

        register_cache("stats_test1", cache1)
        register_cache("stats_test2", cache2)

        cache1.set("a", 1)
        cache2.set("b", 2)
        cache1.get("a")  # Hit

        all_stats = get_cache_stats()

        assert "stats_test1" in all_stats
        assert "stats_test2" in all_stats
        assert all_stats["stats_test1"]["size"] == 1


class TestCachingIntegration(FoundationTestCase):
    """Integration tests for caching with parsers and env."""

    def test_parse_duration_caching(self) -> None:
        """Test that parse_duration uses caching."""
        from provide.foundation.utils.environment.parsers import parse_duration

        # Clear cache before test
        if hasattr(parse_duration, "cache_clear"):
            parse_duration.cache_clear()

        # First calls
        result1 = parse_duration("1h30m")
        result2 = parse_duration("1h30m")  # Should use cache

        assert result1 == 5400
        assert result2 == 5400

        # Check cache stats
        if hasattr(parse_duration, "cache_stats"):
            stats = parse_duration.cache_stats()
            assert stats["hits"] >= 1

    def test_parse_size_caching(self) -> None:
        """Test that parse_size uses caching."""
        from provide.foundation.utils.environment.parsers import parse_size

        # Clear cache before test
        if hasattr(parse_size, "cache_clear"):
            parse_size.cache_clear()

        result1 = parse_size("10MB")
        result2 = parse_size("10MB")  # Should use cache

        assert result1 == 10 * 1024 * 1024
        assert result2 == 10 * 1024 * 1024

        # Check cache stats
        if hasattr(parse_size, "cache_stats"):
            stats = parse_size.cache_stats()
            assert stats["hits"] >= 1

    def test_env_prefix_name_caching(self) -> None:
        """Test that EnvPrefix caches name normalization."""
        from provide.foundation.utils.environment import EnvPrefix

        env = EnvPrefix("TEST")

        # Access same name multiple times
        name1 = env._make_name("debug-mode")
        name2 = env._make_name("debug-mode")

        assert name1 == "TEST_DEBUG_MODE"
        assert name2 == "TEST_DEBUG_MODE"

        # Check cache stats
        stats = env._name_cache.stats()
        assert stats["hits"] >= 1

    @pytest.mark.time_sensitive
    def test_cache_performance_improvement(self) -> None:
        """Test that caching provides measurable performance improvement."""
        from provide.foundation.utils.environment.parsers import parse_duration

        # Clear cache
        if hasattr(parse_duration, "cache_clear"):
            parse_duration.cache_clear()

        # Time first call (uncached)
        start = time.perf_counter()
        for _ in range(100):
            parse_duration("1d2h3m4s")
        first_time = time.perf_counter() - start

        # Clear and do cached calls
        if hasattr(parse_duration, "cache_clear"):
            parse_duration.cache_clear()

        # First call to populate cache
        parse_duration("1d2h3m4s")

        # Time cached calls
        start = time.perf_counter()
        for _ in range(100):
            parse_duration("1d2h3m4s")
        cached_time = time.perf_counter() - start

        # Cached should be faster (at least 2x)
        # Note: This is a rough check and may vary by system
        assert cached_time < first_time


# 🧱🏗️🔚
