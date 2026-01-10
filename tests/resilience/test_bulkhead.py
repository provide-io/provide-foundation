#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for bulkhead pattern and resource pools."""

from __future__ import annotations

import asyncio
import threading
import time

from provide.testkit import FoundationTestCase
import pytest

from provide.foundation.resilience.bulkhead import AsyncResourcePool, Bulkhead, SyncResourcePool


class TestSyncResourcePool(FoundationTestCase):
    """Test SyncResourcePool concurrency limits."""

    def test_sync_acquire_release(self) -> None:
        """Test basic sync acquire/release."""
        pool = SyncResourcePool(max_concurrent=2)

        assert pool.acquire()
        assert pool.active_count() == 1

        assert pool.acquire()
        assert pool.active_count() == 2

        # Third acquire should fail (no timeout)
        assert not pool.acquire(timeout=0.1)

        pool.release()
        assert pool.active_count() == 1

        pool.release()
        assert pool.active_count() == 0

    def test_queue_full_error(self) -> None:
        """Test that queue full raises error."""
        pool = SyncResourcePool(max_concurrent=1, max_queue_size=1)

        # Acquire the slot
        assert pool.acquire()

        # Queue one waiter
        t1 = threading.Thread(target=lambda: pool.acquire(timeout=2.0))
        t1.start()
        time.sleep(0.1)  # Let it queue

        # Next should raise RuntimeError
        with pytest.raises(RuntimeError, match="Queue is full"):
            pool.acquire(timeout=0.1)

        pool.release()
        t1.join()

    def test_stats(self) -> None:
        """Test pool statistics."""
        pool = SyncResourcePool(max_concurrent=5)
        assert pool.acquire()
        assert pool.acquire()

        stats = pool.get_stats()
        assert stats["active_count"] == 2
        assert stats["available_capacity"] == 3
        assert stats["max_concurrent"] == 5
        assert stats["utilization"] == 0.4  # 2/5


class TestAsyncResourcePool(FoundationTestCase):
    """Test AsyncResourcePool concurrency limits."""

    async def test_async_acquire_release(self) -> None:
        """Test basic async acquire/release."""
        pool = AsyncResourcePool(max_concurrent=2)

        assert await pool.acquire()
        assert await pool.active_count() == 1

        assert await pool.acquire()
        assert await pool.active_count() == 2

        # Third acquire should fail (no timeout)
        assert not await pool.acquire(timeout=0.1)

        await pool.release()
        assert await pool.active_count() == 1

        await pool.release()
        assert await pool.active_count() == 0

    async def test_async_queue_full_error(self) -> None:
        """Test that async queue full raises error."""
        pool = AsyncResourcePool(max_concurrent=1, max_queue_size=1)

        # Acquire the slot
        assert await pool.acquire()

        # Queue one waiter
        task = asyncio.create_task(pool.acquire(timeout=2.0))
        await asyncio.sleep(0.1)  # Let it queue

        # Next should raise RuntimeError
        with pytest.raises(RuntimeError, match="Queue is full"):
            await pool.acquire(timeout=0.1)

        await pool.release()
        await task

    async def test_async_stats(self) -> None:
        """Test async pool statistics."""
        pool = AsyncResourcePool(max_concurrent=5)
        await pool.acquire()
        await pool.acquire()

        stats = await pool.get_stats()
        assert stats["active_count"] == 2
        assert stats["available_capacity"] == 3
        assert stats["max_concurrent"] == 5
        assert stats["utilization"] == 0.4  # 2/5


class TestBulkhead(FoundationTestCase):
    """Test Bulkhead execution wrapper."""

    def test_sync_execute(self) -> None:
        """Test sync execution with bulkhead."""
        pool = SyncResourcePool(max_concurrent=2)
        bulkhead = Bulkhead(name="test", pool=pool)

        def work(x: int) -> int:
            return x * 2

        result = bulkhead.execute(work, 21)
        assert result == 42

    async def test_async_execute(self) -> None:
        """Test async execution with bulkhead."""
        pool = AsyncResourcePool(max_concurrent=2)
        bulkhead = Bulkhead(name="test", pool=pool)

        async def work(x: int) -> int:
            await asyncio.sleep(0.01)
            return x * 2

        result = await bulkhead.execute_async(work, 21)
        assert result == 42

    def test_at_capacity_error(self) -> None:
        """Test error when at capacity."""
        pool = SyncResourcePool(max_concurrent=1, max_queue_size=0)
        bulkhead = Bulkhead(name="test", pool=pool)

        def work() -> None:
            time.sleep(0.2)

        # First execution should succeed
        t = threading.Thread(target=lambda: bulkhead.execute(work))
        t.start()
        time.sleep(0.05)  # Let it acquire

        # Second should fail with queue full error
        with pytest.raises(RuntimeError, match="Queue is full"):
            bulkhead.execute(lambda: None)

        t.join()


# 🧱🏗️🔚
