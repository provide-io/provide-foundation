#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#


from __future__ import annotations

import asyncio
from concurrent.futures import ThreadPoolExecutor

import pytest

from provide.foundation.utils.scoped_cache import ContextScopedCache


class TestContextScopedCacheBasics:
    """Test basic cache operations."""

    def test_set_and_get(self) -> None:
        """Cache should store and retrieve values."""
        cache = ContextScopedCache[str, int]("test")

        with cache.scope():
            cache.set("key", 42)
            assert cache.get("key") == 42

    def test_get_default(self) -> None:
        """Get should return default for missing keys."""
        cache = ContextScopedCache[str, int]("test")

        with cache.scope():
            assert cache.get("missing") is None
            assert cache.get("missing", 99) == 99

    def test_contains(self) -> None:
        """Contains should check key existence."""
        cache = ContextScopedCache[str, int]("test")

        with cache.scope():
            cache.set("exists", 1)
            assert cache.contains("exists") is True
            assert cache.contains("missing") is False

    def test_clear(self) -> None:
        """Clear should empty the cache."""
        cache = ContextScopedCache[str, int]("test")

        with cache.scope():
            cache.set("a", 1)
            cache.set("b", 2)
            assert cache.size() == 2

            cache.clear()
            assert cache.size() == 0
            assert cache.get("a") is None

    def test_size(self) -> None:
        """Size should return number of items."""
        cache = ContextScopedCache[str, int]("test")

        with cache.scope():
            assert cache.size() == 0
            cache.set("a", 1)
            assert cache.size() == 1
            cache.set("b", 2)
            assert cache.size() == 2


class TestContextScopedCacheScoping:
    """Test cache scoping behavior."""

    def test_scope_isolation(self) -> None:
        """Separate scopes should have isolated caches."""
        cache = ContextScopedCache[str, int]("test")

        with cache.scope():
            cache.set("key", 1)
            assert cache.get("key") == 1

        # New scope should be empty
        with cache.scope():
            assert cache.get("key") is None

    def test_nested_scope_reuses_cache(self) -> None:
        """Nested scopes should reuse parent cache."""
        cache = ContextScopedCache[str, int]("test")

        with cache.scope():
            cache.set("outer", 1)

            with cache.scope():
                # Should see outer cache
                assert cache.get("outer") == 1

                # Can modify it
                cache.set("inner", 2)

            # Modifications persist in outer scope
            assert cache.get("inner") == 2

    def test_scope_cleanup_on_exception(self) -> None:
        """Cache should be cleaned up even on exception."""
        cache = ContextScopedCache[str, int]("test")

        try:
            with cache.scope():
                cache.set("key", 1)
                raise ValueError("test")
        except ValueError:
            pass

        # Cache should be cleaned up
        with cache.scope():
            assert cache.get("key") is None

    def test_is_active(self) -> None:
        """is_active should track scope status."""
        cache = ContextScopedCache[str, int]("test")

        assert cache.is_active() is False

        with cache.scope():
            assert cache.is_active() is True

            with cache.scope():
                assert cache.is_active() is True

        assert cache.is_active() is False


class TestContextScopedCacheErrors:
    """Test error handling."""

    def test_access_outside_scope_raises(self) -> None:
        """Accessing cache outside scope should raise."""
        cache = ContextScopedCache[str, int]("test")

        with pytest.raises(RuntimeError, match="accessed outside scope"):
            cache.get("key")

        with pytest.raises(RuntimeError, match="accessed outside scope"):
            cache.set("key", 1)

        with pytest.raises(RuntimeError, match="accessed outside scope"):
            cache.contains("key")

        with pytest.raises(RuntimeError, match="accessed outside scope"):
            cache.clear()

        with pytest.raises(RuntimeError, match="accessed outside scope"):
            cache.size()


class TestContextScopedCacheThreadSafety:
    """Test thread isolation."""

    def test_thread_isolation(self) -> None:
        """Each thread should have isolated cache."""
        cache = ContextScopedCache[str, int]("test")
        results = []

        def worker(thread_id: int) -> None:
            with cache.scope():
                cache.set("id", thread_id)
                # Small delay to ensure threads overlap
                import time

                time.sleep(0.01)
                # Should always get own thread's value
                results.append(cache.get("id") == thread_id)

        with ThreadPoolExecutor(max_workers=4) as executor:
            futures = [executor.submit(worker, i) for i in range(4)]
            for future in futures:
                future.result()

        # All threads should have seen their own values
        assert all(results)

    def test_concurrent_modifications(self) -> None:
        """Concurrent modifications should not interfere."""
        cache = ContextScopedCache[int, int]("test")
        results = []

        def worker(thread_id: int) -> None:
            with cache.scope():
                # Each thread sets its own values
                for i in range(10):
                    cache.set(i, thread_id * 100 + i)

                # Verify all values are correct
                for i in range(10):
                    if cache.get(i) != thread_id * 100 + i:
                        results.append(False)
                        return

                results.append(True)

        with ThreadPoolExecutor(max_workers=4) as executor:
            futures = [executor.submit(worker, i) for i in range(4)]
            for future in futures:
                future.result()

        assert all(results)


class TestContextScopedCacheAsyncSafety:
    """Test async/await compatibility."""

    @pytest.mark.asyncio(loop_scope="function")
    async def test_async_isolation(self) -> None:
        """Each async task should have isolated cache."""
        cache = ContextScopedCache[str, int]("test")

        async def task(task_id: int) -> bool:
            try:
                with cache.scope():
                    cache.set("id", task_id)
                    await asyncio.sleep(0.01)  # Yield control
                    # Should still get own task's value
                    return cache.get("id") == task_id
            except Exception:
                return False

        # Use timeout to prevent indefinite hanging
        results = await asyncio.wait_for(
            asyncio.gather(*[task(i) for i in range(4)]),
            timeout=5.0,
        )
        assert all(results)

    @pytest.mark.asyncio
    async def test_async_nested_scopes(self) -> None:
        """Nested scopes should work in async contexts."""
        cache = ContextScopedCache[str, int]("test")

        async def inner() -> int:
            with cache.scope():
                # Should see outer cache
                value = cache.get("outer")
                assert value == 42
                cache.set("inner", 99)
                await asyncio.sleep(0.001)
                return cache.get("inner", 0)

        async def outer() -> int:
            with cache.scope():
                cache.set("outer", 42)
                result = await inner()
                # Inner modifications should be visible
                assert cache.get("inner") == 99
                return result

        # Use timeout to prevent indefinite hanging
        result = await asyncio.wait_for(outer(), timeout=5.0)
        assert result == 99


class TestContextScopedCacheTypeHints:
    """Test generic type support."""

    def test_string_keys_int_values(self) -> None:
        """Cache should work with str->int types."""
        cache: ContextScopedCache[str, int] = ContextScopedCache("test")

        with cache.scope():
            cache.set("age", 25)
            value: int | None = cache.get("age")
            assert value == 25

    def test_complex_types(self) -> None:
        """Cache should work with complex types."""
        cache: ContextScopedCache[tuple[str, int], list[str]] = ContextScopedCache("test")

        with cache.scope():
            key = ("user", 123)
            value = ["admin", "editor"]
            cache.set(key, value)
            assert cache.get(key) == value

    def test_any_hashable_key(self) -> None:
        """Cache should accept any hashable key type."""
        cache = ContextScopedCache[object, str]("test")

        with cache.scope():
            # Tuple keys
            cache.set((1, 2, 3), "tuple")
            assert cache.get((1, 2, 3)) == "tuple"

            # Frozen set keys
            key = frozenset([1, 2, 3])
            cache.set(key, "frozenset")
            assert cache.get(key) == "frozenset"

            # String keys
            cache.set("string", "value")
            assert cache.get("string") == "value"


# 🧱🏗️🔚
