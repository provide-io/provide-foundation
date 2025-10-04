"""Tests for bulkhead pattern and ResourcePool."""

from __future__ import annotations

import asyncio
import threading
import time

from provide.testkit import FoundationTestCase
import pytest

from provide.foundation.resilience.bulkhead import Bulkhead, ResourcePool


class TestResourcePool(FoundationTestCase):
    """Test ResourcePool concurrency limits."""

    def test_sync_acquire_release(self) -> None:
        """Test basic sync acquire/release."""
        pool = ResourcePool(max_concurrent=2)

        assert pool.acquire()
        assert pool.active_count == 1

        assert pool.acquire()
        assert pool.active_count == 2

        # Third acquire should fail (no timeout)
        assert not pool.acquire(timeout=0.1)

        pool.release()
        assert pool.active_count == 1

        pool.release()
        assert pool.active_count == 0

    async def test_async_acquire_release(self) -> None:
        """Test basic async acquire/release."""
        pool = ResourcePool(max_concurrent=2)

        assert await pool.acquire_async()
        assert pool.active_count == 1

        assert await pool.acquire_async()
        assert pool.active_count == 2

        # Third acquire should fail (no timeout)
        assert not await pool.acquire_async(timeout=0.1)

        await pool.release_async()
        assert pool.active_count == 1

        await pool.release_async()
        assert pool.active_count == 0

    async def test_mixed_sync_async_no_oversubscription(self) -> None:
        """Test that sync + async together don't exceed max_concurrent.

        This is the critical test for Observation 3 - verifies atomic counter
        prevents oversubscription when both sync and async are used.
        """
        max_concurrent = 5
        pool = ResourcePool(max_concurrent=max_concurrent)
        peak_active = 0
        active_lock = threading.Lock()

        def sync_worker() -> None:
            nonlocal peak_active
            if pool.acquire(timeout=2.0):
                try:
                    with active_lock:
                        current = pool.active_count
                        if current > peak_active:
                            peak_active = current
                    time.sleep(0.1)  # Hold the slot
                finally:
                    pool.release()

        async def async_worker() -> None:
            nonlocal peak_active
            if await pool.acquire_async(timeout=2.0):
                try:
                    with active_lock:
                        current = pool.active_count
                        if current > peak_active:
                            peak_active = current
                    await asyncio.sleep(0.1)  # Hold the slot
                finally:
                    await pool.release_async()

        # Spawn more workers than max to create contention
        num_sync = 8
        num_async = 8

        threads = [threading.Thread(target=sync_worker) for _ in range(num_sync)]
        for t in threads:
            t.start()

        tasks = [asyncio.create_task(async_worker()) for _ in range(num_async)]

        # Wait for all to complete
        await asyncio.gather(*tasks)
        for t in threads:
            t.join()

        # CRITICAL ASSERTION: Peak active should NEVER exceed max_concurrent
        assert peak_active <= max_concurrent, (
            f"Oversubscription detected! Peak active: {peak_active}, "
            f"max_concurrent: {max_concurrent}"
        )

        # All workers should have completed
        assert pool.active_count == 0

    async def test_mixed_sync_async_fairness(self) -> None:
        """Test that sync and async both get fair access."""
        pool = ResourcePool(max_concurrent=2, max_queue_size=20)
        sync_completions = 0
        async_completions = 0
        lock = threading.Lock()

        def sync_worker() -> None:
            nonlocal sync_completions
            if pool.acquire(timeout=2.0):
                try:
                    time.sleep(0.05)
                    with lock:
                        sync_completions += 1
                finally:
                    pool.release()

        async def async_worker() -> None:
            nonlocal async_completions
            if await pool.acquire_async(timeout=2.0):
                try:
                    await asyncio.sleep(0.05)
                    with lock:
                        async_completions += 1
                finally:
                    await pool.release_async()

        # Run equal numbers
        num_each = 10
        threads = [threading.Thread(target=sync_worker) for _ in range(num_each)]
        for t in threads:
            t.start()

        tasks = [asyncio.create_task(async_worker()) for _ in range(num_each)]

        await asyncio.gather(*tasks)
        for t in threads:
            t.join()

        # Both sync and async should have completed successfully
        assert sync_completions > 0, "Sync workers got no access"
        assert async_completions > 0, "Async workers got no access"

    def test_queue_full_error(self) -> None:
        """Test that queue full raises error."""
        pool = ResourcePool(max_concurrent=1, max_queue_size=1)

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

    async def test_async_queue_full_error(self) -> None:
        """Test that async queue full raises error."""
        pool = ResourcePool(max_concurrent=1, max_queue_size=1)

        # Acquire the slot
        assert await pool.acquire_async()

        # Queue one waiter
        task = asyncio.create_task(pool.acquire_async(timeout=2.0))
        await asyncio.sleep(0.1)  # Let it queue

        # Next should raise RuntimeError
        with pytest.raises(RuntimeError, match="Queue is full"):
            await pool.acquire_async(timeout=0.1)

        await pool.release_async()
        await task

    def test_stats(self) -> None:
        """Test pool statistics."""
        pool = ResourcePool(max_concurrent=5)
        assert pool.acquire()
        assert pool.acquire()

        stats = pool.get_stats()
        assert stats["active_count"] == 2
        assert stats["available_capacity"] == 3
        assert stats["max_concurrent"] == 5
        assert stats["utilization"] == 0.4  # 2/5


class TestBulkhead(FoundationTestCase):
    """Test Bulkhead execution wrapper."""

    def test_sync_execute(self) -> None:
        """Test sync execution with bulkhead."""
        pool = ResourcePool(max_concurrent=2)
        bulkhead = Bulkhead(name="test", pool=pool)

        def work(x: int) -> int:
            return x * 2

        result = bulkhead.execute(work, 21)
        assert result == 42

    async def test_async_execute(self) -> None:
        """Test async execution with bulkhead."""
        pool = ResourcePool(max_concurrent=2)
        bulkhead = Bulkhead(name="test", pool=pool)

        async def work(x: int) -> int:
            await asyncio.sleep(0.01)
            return x * 2

        result = await bulkhead.execute_async(work, 21)
        assert result == 42

    def test_at_capacity_error(self) -> None:
        """Test error when at capacity."""
        pool = ResourcePool(max_concurrent=1, max_queue_size=0)
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
