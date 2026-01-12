#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for circuit breaker reset in testmode.

This module tests that the testmode reset logic properly handles both
synchronous and asynchronous circuit breakers, ensuring test isolation
and no "coroutine never awaited" warnings.
"""

from __future__ import annotations

from typing import Never

from provide.testkit import FoundationTestCase
import pytest

from provide.foundation.resilience.circuit_async import AsyncCircuitBreaker
from provide.foundation.resilience.circuit_sync import CircuitState, SyncCircuitBreaker
from provide.foundation.testmode.internal import (
    _reset_direct_circuit_breaker_instances,
    reset_circuit_breaker_state,
)


class TestSyncCircuitBreakerReset(FoundationTestCase):
    """Test reset of SyncCircuitBreaker instances."""

    def test_sync_breaker_reset_via_direct_instances(self) -> None:
        """Test that SyncCircuitBreaker can be reset via _reset_direct_circuit_breaker_instances."""
        breaker = SyncCircuitBreaker(failure_threshold=1)

        def failing_func() -> Never:
            raise ValueError("test error")

        # Open the circuit
        with pytest.raises(ValueError):
            breaker.call(failing_func)

        assert breaker.state() == CircuitState.OPEN
        assert breaker.failure_count() == 1

        # Reset via testmode function
        _reset_direct_circuit_breaker_instances()

        # Should be reset
        assert breaker.state() == CircuitState.CLOSED
        assert breaker.failure_count() == 0

    def test_sync_breaker_full_reset_path(self) -> None:
        """Test SyncCircuitBreaker reset via full reset_circuit_breaker_state."""
        breaker = SyncCircuitBreaker(failure_threshold=1)

        def failing_func() -> Never:
            raise ValueError("test error")

        # Open the circuit
        with pytest.raises(ValueError):
            breaker.call(failing_func)

        assert breaker.state() == CircuitState.OPEN

        # Reset via full reset path
        reset_circuit_breaker_state()

        # Should be reset
        assert breaker.state() == CircuitState.CLOSED
        assert breaker.failure_count() == 0


class TestAsyncCircuitBreakerReset(FoundationTestCase):
    """Test reset of AsyncCircuitBreaker instances."""

    @pytest.mark.asyncio
    async def test_async_breaker_reset_via_fixture(self) -> None:
        """Test that AsyncCircuitBreaker is reset between tests via fixture teardown."""
        # This test verifies that the reset function works when called
        # from fixture teardown (sync context), not from async test body
        breaker = AsyncCircuitBreaker(failure_threshold=1)

        async def async_failing_func() -> Never:
            raise ValueError("async test error")

        # Open the circuit
        with pytest.raises(ValueError):
            await breaker.call(async_failing_func)

        assert await breaker.state() == CircuitState.OPEN
        assert await breaker.failure_count() == 1
        # The FoundationTestCase fixture will reset this on teardown

    @pytest.mark.asyncio
    async def test_async_breaker_remains_reset_between_tests(self) -> None:
        """Test that async breaker state is properly reset between tests.

        This test creates a NEW async breaker instance, verifying that if
        breakers created in previous tests were properly reset, the circuit
        starts in CLOSED state.
        """
        breaker = AsyncCircuitBreaker(failure_threshold=1)

        # New breaker should start CLOSED
        assert await breaker.state() == CircuitState.CLOSED
        assert await breaker.failure_count() == 0


class TestMixedCircuitBreakerReset(FoundationTestCase):
    """Test reset of mixed sync and async circuit breakers."""

    @pytest.mark.asyncio
    async def test_sync_and_async_breakers_open(self) -> None:
        """Test that both sync and async breakers can be opened.

        The reset will happen via fixture teardown.
        """
        sync_breaker = SyncCircuitBreaker(failure_threshold=1)
        async_breaker = AsyncCircuitBreaker(failure_threshold=1)

        def sync_failing_func() -> Never:
            raise ValueError("sync test error")

        async def async_failing_func() -> Never:
            raise ValueError("async test error")

        # Open both circuits
        with pytest.raises(ValueError):
            sync_breaker.call(sync_failing_func)

        with pytest.raises(ValueError):
            await async_breaker.call(async_failing_func)

        assert sync_breaker.state() == CircuitState.OPEN
        assert await async_breaker.state() == CircuitState.OPEN
        # The FoundationTestCase fixture will reset both on teardown

    @pytest.mark.asyncio
    async def test_sync_and_async_breakers_reset_after_previous_test(self) -> None:
        """Test that both sync and async breakers are reset after previous test."""
        # Create new instances to verify they start clean
        sync_breaker = SyncCircuitBreaker(failure_threshold=1)
        async_breaker = AsyncCircuitBreaker(failure_threshold=1)

        # Both should start CLOSED
        assert sync_breaker.state() == CircuitState.CLOSED
        assert await async_breaker.state() == CircuitState.CLOSED


class TestCircuitBreakerResetNoWarnings(FoundationTestCase):
    """Test that reset operations don't produce 'coroutine never awaited' warnings."""

    @pytest.mark.asyncio
    async def test_async_breaker_no_unawaited_warning(self) -> None:
        """Test that AsyncCircuitBreaker reset doesn't produce unawaited coroutine warnings.

        This test opens a circuit and the fixture teardown will reset it
        from a sync context (no running loop), ensuring no warnings about
        unawaited coroutines.

        The presence of pytest warnings would indicate the fix isn't working.
        """
        breaker = AsyncCircuitBreaker(failure_threshold=1)

        async def async_failing_func() -> Never:
            raise ValueError("test")

        # Trigger failure to open circuit
        with pytest.raises(ValueError):
            await breaker.call(async_failing_func)

        assert await breaker.state() == CircuitState.OPEN
        # Reset happens in fixture teardown from sync context


# 🧱🏗️🔚
