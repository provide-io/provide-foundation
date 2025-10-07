"""Tests for async lock manager initialization and race condition handling."""

from __future__ import annotations

import asyncio

from provide.testkit import FoundationTestCase
import pytest


class TestAsyncLockManagerInitialization(FoundationTestCase):
    """Test async lock manager basic initialization."""

    def setup_method(self) -> None:
        """Reset async lock manager before each test."""
        super().setup_method()
        # Reset globals
        import provide.foundation.concurrency.async_locks as module

        module._async_lock_manager = None
        module._async_locks_registered = False
        module._async_locks_registration_event = None

    @pytest.mark.asyncio
    async def test_basic_initialization(self) -> None:
        """Test basic async lock manager initialization."""
        from provide.foundation.concurrency.async_locks import get_async_lock_manager

        manager = await get_async_lock_manager()
        assert manager is not None

        # Verify all foundation locks are registered
        status = await manager.get_lock_status()
        assert len(status) == 8
        assert "foundation.async.hub.init" in status
        assert "foundation.async.logger.lazy" in status

    @pytest.mark.asyncio
    async def test_singleton_behavior(self) -> None:
        """Test that get_async_lock_manager returns same instance."""
        from provide.foundation.concurrency.async_locks import get_async_lock_manager

        manager1 = await get_async_lock_manager()
        manager2 = await get_async_lock_manager()
        assert manager1 is manager2

    @pytest.mark.asyncio
    async def test_lock_acquisition(self) -> None:
        """Test that registered locks can be acquired."""
        from provide.foundation.concurrency.async_locks import get_async_lock_manager

        manager = await get_async_lock_manager()

        # Acquire a lock
        async with manager.acquire("foundation.async.hub.init", timeout=5.0):
            pass  # Lock acquired and released successfully


class TestAsyncLockManagerConcurrentInitialization(FoundationTestCase):
    """Test concurrent initialization race conditions."""

    def setup_method(self) -> None:
        """Reset async lock manager before each test."""
        super().setup_method()
        import provide.foundation.concurrency.async_locks as module

        module._async_lock_manager = None
        module._async_locks_registered = False
        module._async_locks_registration_event = None

    @pytest.mark.asyncio
    async def test_concurrent_initialization_no_race(self) -> None:
        """Test that concurrent calls don't race during initialization.

        This test verifies that if Task B calls get_async_lock_manager() while
        Task A is still registering locks, Task B waits properly and gets a
        fully initialized manager (not one with missing locks).
        """
        import provide.foundation.concurrency.async_locks as module

        original_register = module.register_foundation_async_locks

        async def slow_register() -> None:
            """Simulate slow registration to create race window."""
            await asyncio.sleep(0.1)  # Delay to allow Task B to enter
            await original_register()

        module.register_foundation_async_locks = slow_register

        try:
            results: dict[str, str] = {}

            async def task_a() -> None:
                """First task to call get_async_lock_manager."""
                await module.get_async_lock_manager()
                results["a"] = "success"

            async def task_b() -> None:
                """Second task that races with Task A."""
                await asyncio.sleep(0.05)  # Start after A, during registration
                manager = await module.get_async_lock_manager()
                # This should work - no KeyError
                await manager.get_lock("foundation.async.hub.init")
                results["b"] = "success"

            await asyncio.gather(task_a(), task_b())

            # Both tasks should succeed
            assert results["a"] == "success"
            assert results["b"] == "success"

        finally:
            module.register_foundation_async_locks = original_register


class TestAsyncLockManagerFailureRecovery(FoundationTestCase):
    """Test failure recovery and partial registration cleanup."""

    def setup_method(self) -> None:
        """Reset async lock manager before each test."""
        super().setup_method()
        import provide.foundation.concurrency.async_locks as module

        module._async_lock_manager = None
        module._async_locks_registered = False
        module._async_locks_registration_event = None

    @pytest.mark.asyncio
    async def test_registration_failure_recovery(self) -> None:
        """Test that failed registration can be retried."""
        import provide.foundation.concurrency.async_locks as module

        original_register = module.register_foundation_async_locks
        call_count = [0]

        async def failing_once_register() -> None:
            """Fail on first call, succeed on second."""
            call_count[0] += 1
            if call_count[0] == 1:
                raise RuntimeError("Simulated registration failure")
            await original_register()

        module.register_foundation_async_locks = failing_once_register

        try:
            # First attempt should fail
            with pytest.raises(RuntimeError, match="Simulated registration failure"):
                await module.get_async_lock_manager()

            # Second attempt should succeed
            manager = await module.get_async_lock_manager()
            status = await manager.get_lock_status()
            assert len(status) == 8  # All locks registered on retry

        finally:
            module.register_foundation_async_locks = original_register

    @pytest.mark.asyncio
    async def test_partial_registration_cleanup(self) -> None:
        """Test that partial registration is cleaned up on failure.

        This test verifies that if registration fails halfway through,
        the partially registered locks are cleaned up, allowing retry
        to succeed without ValueError from duplicate registrations.
        """
        import provide.foundation.concurrency.async_locks as module

        original_register = module.register_foundation_async_locks
        call_count = [0]

        async def failing_halfway_register() -> None:
            """Register some locks then fail (first call), succeed on second."""
            call_count[0] += 1
            manager = module._async_lock_manager

            if call_count[0] == 1:
                # First call: register partial locks then fail
                await manager.register_lock("foundation.async.hub.init", order=0, description="Test")
                await manager.register_lock("foundation.async.init.coordinator", order=10, description="Test")
                raise RuntimeError("Simulated failure after partial registration")
            else:
                # Second call: do full registration
                await original_register()

        module.register_foundation_async_locks = failing_halfway_register

        try:
            # First attempt - will fail after partial registration
            with pytest.raises(RuntimeError, match="Simulated failure after partial registration"):
                await module.get_async_lock_manager()

            # Verify locks were cleaned up (should be 0, not 2)
            if module._async_lock_manager:
                status = await module._async_lock_manager.get_lock_status()
                assert len(status) == 0, "Partial locks should be cleaned up"

            # Second attempt - should succeed without ValueError
            manager = await module.get_async_lock_manager()
            status = await manager.get_lock_status()
            assert len(status) == 8  # All locks registered successfully

        finally:
            module.register_foundation_async_locks = original_register

    @pytest.mark.asyncio
    async def test_cancellation_recovery(self) -> None:
        """Test that cancelled registration can be retried."""
        import provide.foundation.concurrency.async_locks as module

        original_register = module.register_foundation_async_locks
        call_count = [0]

        async def cancelling_once_register() -> None:
            """Raise CancelledError on first call, succeed on second."""
            call_count[0] += 1
            if call_count[0] == 1:
                raise asyncio.CancelledError("Simulated cancellation")
            await original_register()

        module.register_foundation_async_locks = cancelling_once_register

        try:
            # First attempt should be cancelled
            with pytest.raises(asyncio.CancelledError):
                await module.get_async_lock_manager()

            # Second attempt should succeed
            manager = await module.get_async_lock_manager()
            status = await manager.get_lock_status()
            assert len(status) == 8  # All locks registered on retry

        finally:
            module.register_foundation_async_locks = original_register


__all__ = [
    "TestAsyncLockManagerConcurrentInitialization",
    "TestAsyncLockManagerFailureRecovery",
    "TestAsyncLockManagerInitialization",
]
