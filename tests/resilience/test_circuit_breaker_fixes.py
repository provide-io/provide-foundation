#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for CircuitBreaker issue fixes.

This module tests 4 specific issues that were fixed:
1. Inconsistent sync properties in AsyncCircuitBreaker
2. Unsafe event loop creation
3. Type signature inconsistency for expected_exception
4. Counter thread safety"""

from __future__ import annotations

import asyncio
import threading
from typing import TYPE_CHECKING

from provide.testkit import FoundationTestCase
import pytest

from provide.foundation.resilience.circuit_async import AsyncCircuitBreaker
from provide.foundation.resilience.circuit_sync import SyncCircuitBreaker
from provide.foundation.resilience.decorators import circuit_breaker

if TYPE_CHECKING:
    pass


class TestAsyncCircuitBreakerAPIConsistency(FoundationTestCase):
    """Test Issue 1: AsyncCircuitBreaker has no sync properties."""

    def setup_method(self) -> None:
        """Set up test environment."""
        super().setup_method()

    def teardown_method(self) -> None:
        """Clean up after test."""
        super().teardown_method()

    def test_async_circuit_breaker_no_sync_state_property(self) -> None:
        """AsyncCircuitBreaker should not have a synchronous state property."""
        breaker = AsyncCircuitBreaker(failure_threshold=3)

        # Should NOT have a sync 'state' property
        assert not hasattr(breaker, "_state_property"), (
            "AsyncCircuitBreaker should not have sync 'state' property"
        )

        # Should have async state() method
        assert hasattr(breaker, "state"), "AsyncCircuitBreaker should have async state() method"
        assert asyncio.iscoroutinefunction(breaker.state), "state() should be async"

    def test_async_circuit_breaker_no_sync_failure_count_property(self) -> None:
        """AsyncCircuitBreaker should not have a synchronous failure_count property."""
        breaker = AsyncCircuitBreaker(failure_threshold=3)

        # Should NOT have a sync 'failure_count' property
        # Note: We check if accessing it would give us the async method, not a property
        assert hasattr(breaker, "failure_count"), "AsyncCircuitBreaker should have failure_count() method"
        assert asyncio.iscoroutinefunction(breaker.failure_count), "failure_count() should be async"

    def test_async_circuit_breaker_no_sync_reset(self) -> None:
        """AsyncCircuitBreaker should not have a synchronous reset() method."""
        breaker = AsyncCircuitBreaker(failure_threshold=3)

        # Should have reset() method that is async
        assert hasattr(breaker, "reset"), "AsyncCircuitBreaker should have reset() method"
        assert asyncio.iscoroutinefunction(breaker.reset), "reset() should be async"

    async def test_async_circuit_breaker_api_works(self) -> None:
        """Verify AsyncCircuitBreaker async API works correctly."""
        breaker = AsyncCircuitBreaker(failure_threshold=3)

        # All API methods should be async
        state = await breaker.state()
        assert state is not None

        count = await breaker.failure_count()
        assert count == 0

        await breaker.reset()


class TestAsyncCircuitBreakerEventLoopSafety(FoundationTestCase):
    """Test Issue 2: AsyncCircuitBreaker can be created without event loop."""

    def setup_method(self) -> None:
        """Set up test environment."""
        super().setup_method()

    def teardown_method(self) -> None:
        """Clean up after test."""
        super().teardown_method()

    def test_async_circuit_breaker_instantiation_without_event_loop(self) -> None:
        """AsyncCircuitBreaker should be instantiable without running event loop.

        This tests that we don't create global event loops during instantiation.
        """
        # Create breaker outside of async context
        breaker = AsyncCircuitBreaker(failure_threshold=3, recovery_timeout=10.0)

        # Should succeed without creating global event loop
        assert breaker is not None
        assert breaker._lock is not None, "Lock should be created"
        assert isinstance(breaker._lock, asyncio.Lock), "Lock should be asyncio.Lock"

    async def test_async_circuit_breaker_lock_binds_on_first_await(self) -> None:
        """Verify lock created in __init__ works when first awaited."""
        # Create breaker outside event loop (in test setup)
        breaker = AsyncCircuitBreaker(failure_threshold=3)

        # Now use it in async context - lock should bind to this event loop
        state = await breaker.state()
        assert state is not None

        # Lock should work properly
        async with breaker._lock:
            breaker._failure_count = 5

        count = await breaker.failure_count()
        assert count == 5

    def test_multiple_async_circuit_breakers_no_event_loop_pollution(self) -> None:
        """Creating multiple AsyncCircuitBreakers should not pollute global event loop."""
        import asyncio as asyncio_module

        # Get current event loop policy
        original_policy = asyncio_module.get_event_loop_policy()

        # Create multiple breakers
        breakers = [AsyncCircuitBreaker(failure_threshold=i) for i in range(1, 10)]

        # Event loop policy should not change
        current_policy = asyncio_module.get_event_loop_policy()
        assert current_policy is original_policy, "Event loop policy should not change"

        # All breakers should have locks
        for breaker in breakers:
            assert breaker._lock is not None


class TestCircuitBreakerDecoratorExceptionTypes(FoundationTestCase):
    """Test Issue 3: Decorator accepts single exception or tuple."""

    def setup_method(self) -> None:
        """Set up test environment."""
        super().setup_method()

    def teardown_method(self) -> None:
        """Clean up after test."""
        super().teardown_method()

    def test_decorator_accepts_single_exception_type(self) -> None:
        """Decorator should accept single exception type without tuple."""

        @circuit_breaker(expected_exception=ValueError)
        def risky_func() -> str:
            raise ValueError("test error")

        # Should work without wrapping ValueError in tuple
        with pytest.raises(ValueError):
            risky_func()

    def test_decorator_accepts_tuple_of_exceptions(self) -> None:
        """Decorator should accept tuple of exception types."""

        @circuit_breaker(expected_exception=(ValueError, TypeError))
        def risky_func(error_type: type[Exception]) -> None:
            raise error_type("test error")

        # Should work with tuple
        with pytest.raises(ValueError):
            risky_func(ValueError)

        with pytest.raises(TypeError):
            risky_func(TypeError)

    def test_decorator_single_exception_triggers_circuit(self) -> None:
        """Single exception type should trigger circuit breaker."""

        @circuit_breaker(failure_threshold=2, expected_exception=ValueError)
        def failing_func() -> None:
            raise ValueError("fail")

        # First failure
        with pytest.raises(ValueError):
            failing_func()

        # Second failure - should open circuit
        with pytest.raises(ValueError):
            failing_func()

        # Third call - circuit should be open
        with pytest.raises(RuntimeError, match="Circuit breaker is open"):
            failing_func()

    def test_decorator_single_exception_ignores_others(self) -> None:
        """Single exception type should not trigger on other exceptions."""

        call_count = 0

        @circuit_breaker(failure_threshold=2, expected_exception=ValueError)
        def selective_func() -> None:
            nonlocal call_count
            call_count += 1
            raise TypeError("not watched")

        # TypeError should not trigger circuit breaker
        for _ in range(5):
            with pytest.raises(TypeError):
                selective_func()

        # Should have called 5 times (circuit never opened)
        assert call_count == 5

    async def test_async_decorator_accepts_single_exception_type(self) -> None:
        """Async decorator should accept single exception type."""

        @circuit_breaker(expected_exception=ValueError)
        async def risky_async_func() -> str:
            raise ValueError("async test error")

        # Should work without wrapping ValueError in tuple
        with pytest.raises(ValueError):
            await risky_async_func()


class TestCircuitBreakerCounterThreadSafety(FoundationTestCase):
    """Test Issue 4: Counter has thread safety."""

    def setup_method(self) -> None:
        """Set up test environment."""
        super().setup_method()

    def teardown_method(self) -> None:
        """Clean up after test."""
        super().teardown_method()

    def test_counter_thread_safety_multiple_decorators(self) -> None:
        """Counter should be thread-safe when decorating multiple functions in parallel."""
        from provide.foundation.hub.manager import get_hub

        registry = get_hub()._component_registry  # type: ignore[attr-defined]

        # Get initial breaker names
        initial_names = set(registry.list_dimension("circuit_breaker_test"))

        def create_decorated_function(thread_id: int) -> None:
            """Create a circuit breaker decorated function in a thread."""

            @circuit_breaker(failure_threshold=5)
            def func() -> int:
                return thread_id

            # Execute function to ensure decorator completes
            result = func()
            assert result == thread_id

        # Create 50 decorated functions in parallel threads
        threads = []
        num_threads = 50

        for i in range(num_threads):
            thread = threading.Thread(target=create_decorated_function, args=(i,))
            threads.append(thread)
            thread.start()

        # Wait for all threads to complete
        for thread in threads:
            thread.join()

        # Get final breaker names
        final_names = set(registry.list_dimension("circuit_breaker_test"))
        new_names = final_names - initial_names

        # Should have created exactly num_threads unique breakers
        assert len(new_names) == num_threads, f"Expected {num_threads} unique breakers, got {len(new_names)}"

    def test_counter_increments_correctly_under_contention(self) -> None:
        """Counter should increment correctly even under thread contention."""
        from provide.foundation.resilience import decorators

        # Get initial counter value
        initial_counter = decorators._circuit_breaker_counter

        def create_breaker() -> None:
            """Create a circuit breaker in a thread."""

            @circuit_breaker(failure_threshold=3)
            def dummy() -> None:
                pass

            dummy()

        # Create 100 breakers in parallel
        threads = []
        num_threads = 100

        for _ in range(num_threads):
            thread = threading.Thread(target=create_breaker)
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        # Counter should have incremented by exactly 100
        final_counter = decorators._circuit_breaker_counter
        expected_increment = num_threads
        actual_increment = final_counter - initial_counter

        assert actual_increment == expected_increment, (
            f"Counter incremented by {actual_increment}, expected {expected_increment}"
        )


class TestSyncCircuitBreakerStillWorks(FoundationTestCase):
    """Verify SyncCircuitBreaker still has sync properties."""

    def setup_method(self) -> None:
        """Set up test environment."""
        super().setup_method()

    def teardown_method(self) -> None:
        """Clean up after test."""
        super().teardown_method()

    def test_sync_circuit_breaker_has_sync_methods(self) -> None:
        """SyncCircuitBreaker should have synchronous methods."""
        breaker = SyncCircuitBreaker(failure_threshold=3)

        # Should have sync state method
        assert hasattr(breaker, "state"), "SyncCircuitBreaker should have state method"
        assert callable(breaker.state), "state should be callable"
        state = breaker.state()
        assert state is not None

        # Should have sync failure_count method
        assert hasattr(breaker, "failure_count"), "SyncCircuitBreaker should have failure_count method"
        assert callable(breaker.failure_count), "failure_count should be callable"
        count = breaker.failure_count()
        assert count == 0

        # Should have sync reset method
        assert hasattr(breaker, "reset"), "SyncCircuitBreaker should have reset() method"
        assert not asyncio.iscoroutinefunction(breaker.reset), "reset() should be sync"
        breaker.reset()


# 🧱🏗️🔚
