#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for circuit breaker functionality."""

from __future__ import annotations

import time
from typing import Never

from provide.testkit import FoundationTestCase
import pytest

from provide.foundation.resilience.circuit_async import AsyncCircuitBreaker
from provide.foundation.resilience.circuit_sync import CircuitState, SyncCircuitBreaker


class TestCircuitBreaker(FoundationTestCase):
    """Test SyncCircuitBreaker class."""

    def test_initial_state(self) -> None:
        """Test initial circuit breaker state."""
        breaker = SyncCircuitBreaker()

        assert breaker.state() == CircuitState.CLOSED
        assert breaker.failure_count() == 0

    def test_successful_calls_keep_circuit_closed(self) -> None:
        """Test successful calls don't affect circuit state."""
        breaker = SyncCircuitBreaker(failure_threshold=2)

        def success_func() -> str:
            return "success"

        # Multiple successful calls
        for _ in range(5):
            result = breaker.call(success_func)
            assert result == "success"
            assert breaker.state() == CircuitState.CLOSED
            assert breaker.failure_count() == 0

    def test_failures_increment_count(self) -> None:
        """Test failures increment failure count."""
        breaker = SyncCircuitBreaker(failure_threshold=3)

        def failing_func() -> Never:
            raise ValueError("test error")

        # First failure
        with pytest.raises(ValueError):
            breaker.call(failing_func)

        assert breaker.state() == CircuitState.CLOSED
        assert breaker.failure_count() == 1

        # Second failure
        with pytest.raises(ValueError):
            breaker.call(failing_func)

        assert breaker.state() == CircuitState.CLOSED
        assert breaker.failure_count() == 2

    def test_circuit_opens_after_threshold(self) -> None:
        """Test circuit opens when failure threshold is reached."""
        breaker = SyncCircuitBreaker(failure_threshold=2)

        def failing_func() -> Never:
            raise ValueError("test error")

        # Hit threshold
        for _ in range(2):
            with pytest.raises(ValueError):
                breaker.call(failing_func)

        assert breaker.state() == CircuitState.OPEN
        assert breaker.failure_count() == 2

        # Circuit should now be open and fail fast
        with pytest.raises(RuntimeError, match="Circuit breaker is open"):
            breaker.call(failing_func)

    @pytest.mark.time_sensitive
    def test_circuit_recovery_after_timeout(self) -> None:
        """Test circuit attempts recovery after timeout."""
        breaker = SyncCircuitBreaker(failure_threshold=1, recovery_timeout=0.1)

        def failing_func() -> Never:
            raise ValueError("test error")

        def success_func() -> str:
            return "recovered"

        # Open circuit
        with pytest.raises(ValueError):
            breaker.call(failing_func)

        assert breaker.state() == CircuitState.OPEN

        # Wait for recovery timeout
        time.sleep(0.15)

        # Next call should attempt recovery
        result = breaker.call(success_func)

        assert result == "recovered"
        assert breaker.state() == CircuitState.CLOSED
        assert breaker.failure_count() == 0

    @pytest.mark.time_sensitive
    def test_half_open_failure_reopens_circuit(self) -> None:
        """Test failure in half-open state reopens circuit."""
        breaker = SyncCircuitBreaker(failure_threshold=1, recovery_timeout=0.1)

        def failing_func() -> Never:
            raise ValueError("test error")

        # Open circuit
        with pytest.raises(ValueError):
            breaker.call(failing_func)

        # Wait for recovery timeout
        time.sleep(0.15)

        # This should fail and reopen circuit
        with pytest.raises(ValueError):
            breaker.call(failing_func)

        assert breaker.state() == CircuitState.OPEN

        # Should fail fast again
        with pytest.raises(RuntimeError, match="Circuit breaker is open"):
            breaker.call(failing_func)

    def test_expected_exception_filtering(self) -> None:
        """Test circuit breaker only triggers on expected exceptions."""
        breaker = SyncCircuitBreaker(
            failure_threshold=1,
            expected_exception=(ValueError,),
        )

        def runtime_error_func() -> Never:
            raise RuntimeError("unexpected")

        def value_error_func() -> Never:
            raise ValueError("expected")

        # RuntimeError should not trigger circuit breaker
        with pytest.raises(RuntimeError):
            breaker.call(runtime_error_func)

        assert breaker.state() == CircuitState.CLOSED
        assert breaker.failure_count() == 0

        # ValueError should trigger circuit breaker
        with pytest.raises(ValueError):
            breaker.call(value_error_func)

        assert breaker.state() == CircuitState.OPEN
        assert breaker.failure_count() == 1

    def test_manual_reset(self) -> None:
        """Test manual circuit breaker reset."""
        breaker = SyncCircuitBreaker(failure_threshold=1)

        def failing_func() -> Never:
            raise ValueError("test error")

        # Open circuit
        with pytest.raises(ValueError):
            breaker.call(failing_func)

        assert breaker.state() == CircuitState.OPEN

        # Manual reset
        breaker.reset()

        assert breaker.state() == CircuitState.CLOSED
        assert breaker.failure_count() == 0

    @pytest.mark.asyncio
    async def test_async_circuit_breaker(self) -> None:
        """Test circuit breaker with async functions."""
        breaker = AsyncCircuitBreaker(failure_threshold=2)

        async def async_failing_func() -> Never:
            raise ValueError("async error")

        async def async_success_func() -> str:
            return "async success"

        # Test failures
        for _ in range(2):
            with pytest.raises(ValueError):
                await breaker.call(async_failing_func)

        assert await breaker.state() == CircuitState.OPEN

        # Test fast failure
        with pytest.raises(RuntimeError):
            await breaker.call(async_failing_func)

        # Test success
        await breaker.reset()
        result = await breaker.call(async_success_func)
        assert result == "async success"

    @pytest.mark.time_sensitive
    def test_custom_recovery_timeout(self) -> None:
        """Test custom recovery timeout setting."""
        breaker = SyncCircuitBreaker(failure_threshold=1, recovery_timeout=1.0)

        def failing_func() -> Never:
            raise ValueError("test")

        # Open circuit
        with pytest.raises(ValueError):
            breaker.call(failing_func)

        assert breaker.state() == CircuitState.OPEN

        # Should still be closed before timeout
        time.sleep(0.5)
        with pytest.raises(RuntimeError):
            breaker.call(failing_func)

        # Should attempt recovery after timeout
        time.sleep(0.6)  # Total 1.1 seconds

        # This will fail but should transition to half-open first
        with pytest.raises(ValueError):
            breaker.call(failing_func)

        # Should be open again
        assert breaker.state() == CircuitState.OPEN


# 🧱🏗️🔚
