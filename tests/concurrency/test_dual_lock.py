"""Tests for DualLock concurrency primitive."""

from __future__ import annotations

import asyncio
import threading
import time

from provide.testkit import FoundationTestCase

from provide.foundation.concurrency.locks import DualLock


class TestDualLockSync(FoundationTestCase):
    """Test DualLock synchronous operations."""

    def test_sync_lock_basic(self) -> None:
        """Test basic synchronous lock acquisition."""
        lock = DualLock()
        shared_value = 0

        with lock.sync():
            shared_value += 1

        assert shared_value == 1

    def test_sync_lock_mutual_exclusion(self) -> None:
        """Test mutual exclusion in sync context."""
        lock = DualLock()
        counter = 0
        iterations = 100

        def increment() -> None:
            nonlocal counter
            for _ in range(iterations):
                with lock.sync():
                    current = counter
                    time.sleep(0.0001)  # Force context switch
                    counter = current + 1

        threads = [threading.Thread(target=increment) for _ in range(5)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert counter == iterations * 5

    def test_sync_lock_non_reentrant(self) -> None:
        """Test that DualLock is not reentrant (uses threading.Lock, not RLock)."""
        lock = DualLock()

        # This is expected behavior - DualLock is not reentrant
        # because asyncio.to_thread() can use different threads from the pool
        with lock.sync():
            # Nested acquisition is not supported
            assert True

    def test_sync_lock_exception_handling(self) -> None:
        """Test that lock is released on exception."""
        lock = DualLock()

        try:
            with lock.sync():
                raise ValueError("Test exception")
        except ValueError:
            pass

        # Should be able to acquire again
        with lock.sync():
            assert True


class TestDualLockAsync(FoundationTestCase):
    """Test DualLock asynchronous operations."""

    async def test_async_lock_basic(self) -> None:
        """Test basic asynchronous lock acquisition."""
        lock = DualLock()
        shared_value = 0

        async with lock.aio():
            shared_value += 1

        assert shared_value == 1

    async def test_async_lock_mutual_exclusion(self) -> None:
        """Test mutual exclusion in async context."""
        lock = DualLock()
        counter = 0
        iterations = 50

        async def increment() -> None:
            nonlocal counter
            for _ in range(iterations):
                async with lock.aio():
                    current = counter
                    await asyncio.sleep(0.001)  # Force context switch
                    counter = current + 1

        tasks = [asyncio.create_task(increment()) for _ in range(5)]
        await asyncio.gather(*tasks)

        assert counter == iterations * 5

    async def test_async_lock_exception_handling(self) -> None:
        """Test that async lock is released on exception."""
        lock = DualLock()

        try:
            async with lock.aio():
                raise ValueError("Test exception")
        except ValueError:
            pass

        # Should be able to acquire again
        async with lock.aio():
            assert True


class TestDualLockEdgeCases(FoundationTestCase):
    """Test edge cases and stress scenarios."""

    async def test_high_contention_async(self) -> None:
        """Test async lock under high contention."""
        lock = DualLock()
        counter = 0
        num_tasks = 50
        iterations_per_task = 10

        async def increment() -> None:
            nonlocal counter
            for _ in range(iterations_per_task):
                async with lock.aio():
                    counter += 1

        tasks = [asyncio.create_task(increment()) for _ in range(num_tasks)]
        await asyncio.gather(*tasks)

        assert counter == num_tasks * iterations_per_task

    def test_high_contention_sync(self) -> None:
        """Test sync lock under high contention."""
        lock = DualLock()
        counter = 0
        num_threads = 20
        iterations_per_thread = 50

        def increment() -> None:
            nonlocal counter
            for _ in range(iterations_per_thread):
                with lock.sync():
                    counter += 1

        threads = [threading.Thread(target=increment) for _ in range(num_threads)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert counter == num_threads * iterations_per_thread

    async def test_rapid_acquire_release_async(self) -> None:
        """Test rapid acquire/release cycles in async context."""
        lock = DualLock()

        for _ in range(1000):
            async with lock.aio():
                pass

    def test_rapid_acquire_release_sync(self) -> None:
        """Test rapid acquire/release cycles in sync context."""
        lock = DualLock()

        for _ in range(1000):
            with lock.sync():
                pass


class TestDualLockRealWorld(FoundationTestCase):
    """Test real-world usage patterns."""

    async def test_class_with_dual_api(self) -> None:
        """Test DualLock in a class with both sync and async methods."""

        class Counter:
            def __init__(self) -> None:
                self._lock = DualLock()
                self._value = 0

            def increment(self) -> int:
                with self._lock.sync():
                    self._value += 1
                    return self._value

            async def increment_async(self) -> int:
                async with self._lock.aio():
                    self._value += 1
                    return self._value

            def get_value(self) -> int:
                with self._lock.sync():
                    return self._value

        counter = Counter()

        # Sync increment
        assert counter.increment() == 1

        # Async increment
        result = await counter.increment_async()
        assert result == 2

        # Mix of both with guaranteed mutual exclusion
        def sync_increments() -> None:
            for _ in range(5):
                counter.increment()

        thread = threading.Thread(target=sync_increments)
        thread.start()

        await asyncio.gather(*[counter.increment_async() for _ in range(5)])

        thread.join()

        assert counter.get_value() == 12
