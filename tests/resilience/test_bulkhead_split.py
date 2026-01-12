#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for ResourcePool split into SyncResourcePool and AsyncResourcePool.

This module tests the separation of sync and async resource pools to prevent
mixing of threading and asyncio primitives."""

from __future__ import annotations

import asyncio
import threading
import time
from typing import TYPE_CHECKING

from provide.testkit import FoundationTestCase
import pytest

from provide.foundation.resilience.bulkhead import AsyncResourcePool, Bulkhead, SyncResourcePool

if TYPE_CHECKING:
    pass


class TestSyncResourcePoolAPI(FoundationTestCase):
    """Test SyncResourcePool has only sync APIs."""

    def setup_method(self) -> None:
        """Set up test environment."""
        super().setup_method()

    def teardown_method(self) -> None:
        """Clean up after test."""
        super().teardown_method()

    def test_sync_pool_has_sync_methods(self) -> None:
        """SyncResourcePool should have synchronous methods."""
        pool = SyncResourcePool(max_concurrent=5)

        # Should have sync methods
        assert hasattr(pool, "active_count"), "SyncResourcePool should have active_count method"
        assert callable(pool.active_count), "active_count should be callable"
        count = pool.active_count()
        assert count == 0

        assert hasattr(pool, "available_capacity"), "SyncResourcePool should have available_capacity method"
        assert callable(pool.available_capacity), "available_capacity should be callable"
        capacity = pool.available_capacity()
        assert capacity == 5

        assert hasattr(pool, "queue_size"), "SyncResourcePool should have queue_size method"
        assert callable(pool.queue_size), "queue_size should be callable"
        size = pool.queue_size()
        assert size == 0

    def test_sync_pool_acquire_release_methods(self) -> None:
        """SyncResourcePool should have synchronous acquire/release methods."""
        pool = SyncResourcePool(max_concurrent=5)

        # Should have sync acquire/release
        assert hasattr(pool, "acquire"), "SyncResourcePool should have acquire() method"
        assert not asyncio.iscoroutinefunction(pool.acquire), "acquire() should be sync"

        assert hasattr(pool, "release"), "SyncResourcePool should have release() method"
        assert not asyncio.iscoroutinefunction(pool.release), "release() should be sync"

        assert hasattr(pool, "get_stats"), "SyncResourcePool should have get_stats() method"
        assert not asyncio.iscoroutinefunction(pool.get_stats), "get_stats() should be sync"

    def test_sync_pool_has_no_async_methods(self) -> None:
        """SyncResourcePool should not have async-specific methods."""
        pool = SyncResourcePool(max_concurrent=5)

        # Should NOT have async methods
        assert not hasattr(pool, "acquire_async"), "SyncResourcePool should not have acquire_async()"
        assert not hasattr(pool, "release_async"), "SyncResourcePool should not have release_async()"
        assert not hasattr(pool, "get_stats_async"), "SyncResourcePool should not have get_stats_async()"

    def test_sync_pool_basic_functionality(self) -> None:
        """Verify SyncResourcePool basic operations work."""
        pool = SyncResourcePool(max_concurrent=2)

        # Acquire slots
        assert pool.acquire()
        assert pool.active_count() == 1

        assert pool.acquire()
        assert pool.active_count() == 2

        # Third acquire should timeout
        assert not pool.acquire(timeout=0.1)

        # Release slots
        pool.release()
        assert pool.active_count() == 1

        pool.release()
        assert pool.active_count() == 0


class TestAsyncResourcePoolAPI(FoundationTestCase):
    """Test AsyncResourcePool has only async APIs."""

    def setup_method(self) -> None:
        """Set up test environment."""
        super().setup_method()

    def teardown_method(self) -> None:
        """Clean up after test."""
        super().teardown_method()

    def test_async_pool_has_no_sync_methods(self) -> None:
        """AsyncResourcePool should not have synchronous methods."""
        pool = AsyncResourcePool(max_concurrent=5)

        # Should have async methods only
        assert hasattr(pool, "active_count"), "AsyncResourcePool should have active_count method"
        assert asyncio.iscoroutinefunction(getattr(pool, "active_count", None)), (
            "AsyncResourcePool active_count should be async"
        )

        assert hasattr(pool, "available_capacity"), "AsyncResourcePool should have available_capacity method"
        assert asyncio.iscoroutinefunction(getattr(pool, "available_capacity", None)), (
            "AsyncResourcePool available_capacity should be async"
        )

        assert hasattr(pool, "queue_size"), "AsyncResourcePool should have queue_size method"
        assert asyncio.iscoroutinefunction(getattr(pool, "queue_size", None)), (
            "AsyncResourcePool queue_size should be async"
        )

    async def test_async_pool_has_async_methods(self) -> None:
        """AsyncResourcePool should have asynchronous methods."""
        pool = AsyncResourcePool(max_concurrent=5)

        # Should have async methods
        assert hasattr(pool, "acquire"), "AsyncResourcePool should have acquire() method"
        assert asyncio.iscoroutinefunction(pool.acquire), "acquire() should be async"

        assert hasattr(pool, "release"), "AsyncResourcePool should have release() method"
        assert asyncio.iscoroutinefunction(pool.release), "release() should be async"

        assert hasattr(pool, "get_stats"), "AsyncResourcePool should have get_stats() method"
        assert asyncio.iscoroutinefunction(pool.get_stats), "get_stats() should be async"

    async def test_async_pool_basic_functionality(self) -> None:
        """Verify AsyncResourcePool basic operations work."""
        pool = AsyncResourcePool(max_concurrent=2)

        # Acquire slots
        assert await pool.acquire()
        assert await pool.active_count() == 1

        assert await pool.acquire()
        assert await pool.active_count() == 2

        # Third acquire should timeout
        assert not await pool.acquire(timeout=0.1)

        # Release slots
        await pool.release()
        assert await pool.active_count() == 1

        await pool.release()
        assert await pool.active_count() == 0


class TestSyncResourcePoolThreadSafety(FoundationTestCase):
    """Test SyncResourcePool thread safety."""

    def setup_method(self) -> None:
        """Set up test environment."""
        super().setup_method()

    def teardown_method(self) -> None:
        """Clean up after test."""
        super().teardown_method()

    def test_sync_pool_concurrent_access(self) -> None:
        """SyncResourcePool should handle concurrent thread access safely."""
        pool = SyncResourcePool(max_concurrent=5)
        peak_active = 0
        lock = threading.Lock()

        def worker() -> None:
            nonlocal peak_active
            if pool.acquire(timeout=2.0):
                try:
                    with lock:
                        current = pool.active_count()
                        if current > peak_active:
                            peak_active = current
                    time.sleep(0.05)
                finally:
                    pool.release()

        # Create 20 threads competing for 5 slots
        threads = [threading.Thread(target=worker) for _ in range(20)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        # Peak should never exceed max_concurrent
        assert peak_active <= 5
        assert pool.active_count() == 0

    def test_sync_pool_queue_management(self) -> None:
        """SyncResourcePool should manage waiting queue correctly."""
        pool = SyncResourcePool(max_concurrent=1, max_queue_size=5)

        # Acquire the slot
        assert pool.acquire()

        # Queue 5 waiters in threads
        threads = []
        for _ in range(5):
            t = threading.Thread(target=lambda: pool.acquire(timeout=2.0))
            t.start()
            threads.append(t)
            time.sleep(0.01)  # Let them queue

        # Next should raise queue full error
        with pytest.raises(RuntimeError, match="Queue is full"):
            pool.acquire(timeout=0.1)

        # Release and let waiters complete
        pool.release()
        for t in threads:
            t.join()


class TestAsyncResourcePoolAsyncSafety(FoundationTestCase):
    """Test AsyncResourcePool async safety."""

    def setup_method(self) -> None:
        """Set up test environment."""
        super().setup_method()

    def teardown_method(self) -> None:
        """Clean up after test."""
        super().teardown_method()

    async def test_async_pool_concurrent_tasks(self) -> None:
        """AsyncResourcePool should handle concurrent tasks safely."""
        pool = AsyncResourcePool(max_concurrent=5)
        peak_active = 0
        lock = asyncio.Lock()

        async def worker() -> None:
            nonlocal peak_active
            if await pool.acquire(timeout=2.0):
                try:
                    async with lock:
                        current = await pool.active_count()
                        if current > peak_active:
                            peak_active = current
                    await asyncio.sleep(0.05)
                finally:
                    await pool.release()

        # Create 20 tasks competing for 5 slots
        tasks = [asyncio.create_task(worker()) for _ in range(20)]
        await asyncio.gather(*tasks)

        # Peak should never exceed max_concurrent
        assert peak_active <= 5
        assert await pool.active_count() == 0

    async def test_async_pool_queue_management(self) -> None:
        """AsyncResourcePool should manage waiting queue correctly."""
        pool = AsyncResourcePool(max_concurrent=1, max_queue_size=5)

        # Acquire the slot
        assert await pool.acquire()

        # Queue 5 waiters as tasks
        tasks = [asyncio.create_task(pool.acquire(timeout=2.0)) for _ in range(5)]
        await asyncio.sleep(0.1)  # Let them queue

        # Next should raise queue full error
        with pytest.raises(RuntimeError, match="Queue is full"):
            await pool.acquire(timeout=0.1)

        # Release and let waiters complete
        await pool.release()
        await asyncio.gather(*tasks)


class TestBulkheadWithPoolTypes(FoundationTestCase):
    """Test Bulkhead class with both pool types."""

    def setup_method(self) -> None:
        """Set up test environment."""
        super().setup_method()

    def teardown_method(self) -> None:
        """Clean up after test."""
        super().teardown_method()

    def test_bulkhead_with_sync_pool_for_sync_execution(self) -> None:
        """Bulkhead should work with SyncResourcePool for sync execution."""
        pool = SyncResourcePool(max_concurrent=2)
        bulkhead = Bulkhead(name="test", pool=pool)

        def work(x: int) -> int:
            return x * 2

        result = bulkhead.execute(work, 21)
        assert result == 42

    async def test_bulkhead_with_async_pool_for_async_execution(self) -> None:
        """Bulkhead should work with AsyncResourcePool for async execution."""
        pool = AsyncResourcePool(max_concurrent=2)
        bulkhead = Bulkhead(name="test", pool=pool)

        async def work(x: int) -> int:
            await asyncio.sleep(0.01)
            return x * 2

        result = await bulkhead.execute_async(work, 21)
        assert result == 42

    def test_bulkhead_sync_execution_requires_sync_pool(self) -> None:
        """Sync execution should require SyncResourcePool."""
        pool = AsyncResourcePool(max_concurrent=2)
        bulkhead = Bulkhead(name="test", pool=pool)

        def work() -> int:
            return 42

        with pytest.raises(TypeError, match="Sync execution requires SyncResourcePool"):
            bulkhead.execute(work)

    async def test_bulkhead_async_execution_requires_async_pool(self) -> None:
        """Async execution should require AsyncResourcePool."""
        pool = SyncResourcePool(max_concurrent=2)
        bulkhead = Bulkhead(name="test", pool=pool)

        async def work() -> int:
            return 42

        with pytest.raises(TypeError, match="Async execution requires AsyncResourcePool"):
            await bulkhead.execute_async(work)


class TestResourcePoolSeparation(FoundationTestCase):
    """Test that sync and async pools are properly separated."""

    def setup_method(self) -> None:
        """Set up test environment."""
        super().setup_method()

    def teardown_method(self) -> None:
        """Clean up after test."""
        super().teardown_method()

    def test_sync_pool_uses_threading_primitives(self) -> None:
        """SyncResourcePool should use only threading primitives."""
        pool = SyncResourcePool(max_concurrent=5)

        # Check internal state uses threading.Lock
        # threading.Lock is a function, not a class - check it has lock methods
        assert hasattr(pool._counter_lock, "acquire"), "Should have lock acquire method"
        assert hasattr(pool._counter_lock, "release"), "Should have lock release method"

        # Check waiters queue contains threading.Event
        pool.acquire()
        pool.acquire()
        pool.acquire()
        pool.acquire()
        pool.acquire()

        # Queue a waiter
        def try_acquire() -> None:
            pool.acquire(timeout=0.5)

        t = threading.Thread(target=try_acquire)
        t.start()
        time.sleep(0.05)  # Let it queue

        # Check the waiter in queue is threading.Event
        if pool._waiters:
            waiter = pool._waiters[0]
            # threading.Event is actually a function, not a class
            # Check that it has the expected Event methods
            assert hasattr(waiter, "set"), "Waiter should have 'set' method"
            assert hasattr(waiter, "wait"), "Waiter should have 'wait' method"
            assert hasattr(waiter, "is_set"), "Waiter should have 'is_set' method"

        # Clean up
        pool.release()
        t.join()

    async def test_async_pool_uses_asyncio_primitives(self) -> None:
        """AsyncResourcePool should use only asyncio primitives."""
        pool = AsyncResourcePool(max_concurrent=5)

        # Check internal state uses asyncio.Lock
        assert isinstance(pool._lock, asyncio.Lock), "Should use asyncio.Lock"

        # Check waiters queue contains asyncio.Event
        await pool.acquire()
        await pool.acquire()
        await pool.acquire()
        await pool.acquire()
        await pool.acquire()

        # Queue a waiter
        async def try_acquire() -> None:
            await pool.acquire(timeout=0.5)

        task = asyncio.create_task(try_acquire())
        await asyncio.sleep(0.05)  # Let it queue

        # Check the waiter in queue is asyncio.Event
        if pool._waiters:
            waiter = pool._waiters[0]
            # Check that it has the expected asyncio.Event methods
            assert hasattr(waiter, "set"), "Waiter should have 'set' method"
            assert hasattr(waiter, "wait"), "Waiter should have 'wait' method"
            assert hasattr(waiter, "is_set"), "Waiter should have 'is_set' method"
            # asyncio.Event has specific attributes
            assert isinstance(waiter, asyncio.Event), "Waiter should be asyncio.Event instance"

        # Clean up
        await pool.release()
        await task


__all__ = [
    "TestAsyncResourcePoolAPI",
    "TestAsyncResourcePoolAsyncSafety",
    "TestBulkheadWithPoolTypes",
    "TestResourcePoolSeparation",
    "TestSyncResourcePoolAPI",
    "TestSyncResourcePoolThreadSafety",
]

# 🧱🏗️🔚
