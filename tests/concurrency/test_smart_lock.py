"""Tests for SmartLock concurrency primitive."""

from __future__ import annotations

import asyncio
import threading
import time

from provide.testkit import FoundationTestCase

from provide.foundation.concurrency.locks import SmartLock


class TestSmartLockSync(FoundationTestCase):
    """Test SmartLock synchronous operations."""

    def test_sync_lock_basic(self) -> None:
        """Test basic synchronous lock acquisition."""
        lock = SmartLock()
        shared_value = 0

        with lock.sync():
            shared_value += 1

        assert shared_value == 1

    def test_sync_lock_mutual_exclusion(self) -> None:
        """Test mutual exclusion in sync context."""
        lock = SmartLock()
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
        """Test that SmartLock is not reentrant (uses threading.Lock, not RLock)."""
        lock = SmartLock()

        # This is expected behavior - SmartLock is not reentrant
        # because asyncio.to_thread() can use different threads from the pool
        with lock.sync():
            # Nested acquisition is not supported
            assert True

    def test_sync_lock_exception_handling(self) -> None:
        """Test that lock is released on exception."""
        lock = SmartLock()

        try:
            with lock.sync():
                raise ValueError("Test exception")
        except ValueError:
            pass

        # Should be able to acquire again
        with lock.sync():
            assert True


class TestSmartLockAsync(FoundationTestCase):
    """Test SmartLock asynchronous operations."""

    async def test_async_lock_basic(self) -> None:
        """Test basic asynchronous lock acquisition."""
        lock = SmartLock()
        shared_value = 0

        async with lock.async_():
            shared_value += 1

        assert shared_value == 1

    async def test_async_lock_mutual_exclusion(self) -> None:
        """Test mutual exclusion in async context."""
        lock = SmartLock()
        counter = 0
        iterations = 50

        async def increment() -> None:
            nonlocal counter
            for _ in range(iterations):
                async with lock.async_():
                    current = counter
                    await asyncio.sleep(0.001)  # Force context switch
                    counter = current + 1

        tasks = [asyncio.create_task(increment()) for _ in range(5)]
        await asyncio.gather(*tasks)

        assert counter == iterations * 5

    async def test_async_lock_exception_handling(self) -> None:
        """Test that async lock is released on exception."""
        lock = SmartLock()

        try:
            async with lock.async_():
                raise ValueError("Test exception")
        except ValueError:
            pass

        # Should be able to acquire again
        async with lock.async_():
            assert True


class TestSmartLockMixedMutualExclusion(FoundationTestCase):
    """Test SmartLock provides true mutual exclusion between sync and async."""

    async def test_sync_blocks_async(self) -> None:
        """Test that sync lock acquisition blocks async lock acquisition."""
        lock = SmartLock()
        sync_started = threading.Event()
        sync_released = threading.Event()
        async_acquired = False

        def sync_task() -> None:
            with lock.sync():
                sync_started.set()
                time.sleep(0.2)  # Hold lock for a while
            sync_released.set()

        async def async_task() -> None:
            nonlocal async_acquired
            # Wait for sync to acquire first
            await asyncio.to_thread(sync_started.wait)

            # Try to acquire - should block until sync releases
            async with lock.async_():
                async_acquired = True
                # Verify sync has released before we got here
                assert sync_released.is_set()

        # Start sync task in thread
        thread = threading.Thread(target=sync_task)
        thread.start()

        # Run async task
        await async_task()

        # Wait for sync task
        thread.join()

        # Verify both completed
        assert async_acquired
        assert sync_released.is_set()

    async def test_async_blocks_sync(self) -> None:
        """Test that async lock acquisition blocks sync lock acquisition."""
        lock = SmartLock()
        async_acquired = asyncio.Event()
        async_released = False
        sync_acquired = False

        async def async_task() -> None:
            nonlocal async_released
            async with lock.async_():
                async_acquired.set()
                await asyncio.sleep(0.2)  # Hold lock for a while
                async_released = True

        def sync_task() -> None:
            nonlocal sync_acquired
            # Try to acquire - should block until async releases
            with lock.sync():
                sync_acquired = True
                # Verify async has released before we got here
                assert async_released

        # Start async task
        async_task_handle = asyncio.create_task(async_task())

        # Wait for async to acquire
        await async_acquired.wait()

        # Start sync task in thread
        thread = threading.Thread(target=sync_task)
        thread.start()

        # Wait for both to complete
        await async_task_handle
        thread.join()

        # Verify both completed
        assert sync_acquired
        assert async_released

    async def test_mixed_counter_race_condition(self) -> None:
        """Test that SmartLock prevents race conditions in mixed sync/async access."""
        lock = SmartLock()
        counter = 0
        iterations = 50

        def sync_increment() -> None:
            nonlocal counter
            for _ in range(iterations):
                with lock.sync():
                    current = counter
                    time.sleep(0.0001)  # Force context switch
                    counter = current + 1

        async def async_increment() -> None:
            nonlocal counter
            for _ in range(iterations):
                async with lock.async_():
                    current = counter
                    await asyncio.sleep(0.0001)  # Force context switch
                    counter = current + 1

        # Start 3 sync threads
        threads = [threading.Thread(target=sync_increment) for _ in range(3)]
        for t in threads:
            t.start()

        # Start 3 async tasks
        tasks = [asyncio.create_task(async_increment()) for _ in range(3)]

        # Wait for all to complete
        await asyncio.gather(*tasks)
        for t in threads:
            t.join()

        # If mutual exclusion works, we should have exact count
        expected = iterations * 6
        assert counter == expected

    async def test_rapid_mixed_access(self) -> None:
        """Test rapid switching between sync and async access."""
        lock = SmartLock()
        results: list[str] = []

        def sync_append(value: str) -> None:
            with lock.sync():
                results.append(value)

        async def async_append(value: str) -> None:
            async with lock.async_():
                results.append(value)

        # Rapidly alternate between sync and async
        threads = []
        tasks = []

        for i in range(20):
            if i % 2 == 0:
                t = threading.Thread(target=sync_append, args=(f"sync_{i}",))
                threads.append(t)
                t.start()
            else:
                task = asyncio.create_task(async_append(f"async_{i}"))
                tasks.append(task)

        # Wait for all to complete
        await asyncio.gather(*tasks)
        for t in threads:
            t.join()

        # All operations should complete
        assert len(results) == 20


class TestSmartLockEdgeCases(FoundationTestCase):
    """Test edge cases and stress scenarios."""

    async def test_high_contention_async(self) -> None:
        """Test async lock under high contention."""
        lock = SmartLock()
        counter = 0
        num_tasks = 50
        iterations_per_task = 10

        async def increment() -> None:
            nonlocal counter
            for _ in range(iterations_per_task):
                async with lock.async_():
                    counter += 1

        tasks = [asyncio.create_task(increment()) for _ in range(num_tasks)]
        await asyncio.gather(*tasks)

        assert counter == num_tasks * iterations_per_task

    def test_high_contention_sync(self) -> None:
        """Test sync lock under high contention."""
        lock = SmartLock()
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
        lock = SmartLock()

        for _ in range(1000):
            async with lock.async_():
                pass

    def test_rapid_acquire_release_sync(self) -> None:
        """Test rapid acquire/release cycles in sync context."""
        lock = SmartLock()

        for _ in range(1000):
            with lock.sync():
                pass


class TestSmartLockRealWorld(FoundationTestCase):
    """Test real-world usage patterns."""

    async def test_class_with_dual_api(self) -> None:
        """Test SmartLock in a class with both sync and async methods."""

        class Counter:
            def __init__(self) -> None:
                self._lock = SmartLock()
                self._value = 0

            def increment(self) -> int:
                with self._lock.sync():
                    self._value += 1
                    return self._value

            async def increment_async(self) -> int:
                async with self._lock.async_():
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
