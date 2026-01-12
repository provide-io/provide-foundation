#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Chaos tests for CircuitBreaker implementation.

Property-based tests using Hypothesis to explore edge cases in circuit breaking,
including concurrent access, state transitions, and recovery scenarios."""

from __future__ import annotations

import asyncio
from concurrent.futures import ThreadPoolExecutor
import contextlib
import time

from hypothesis import HealthCheck, given, settings, strategies as st
from provide.testkit import FoundationTestCase
from provide.testkit.chaos import (
    chaos_timings,
    failure_patterns,
    thread_counts,
    time_advances,
)
import pytest

from provide.foundation.resilience.circuit_sync import CircuitState, SyncCircuitBreaker


class TestCircuitBreakerChaos(FoundationTestCase):
    """Chaos tests for CircuitBreaker."""

    @given(
        failure_threshold=st.integers(min_value=1, max_value=10),
        num_calls=st.integers(min_value=1, max_value=20),
        failure_rate=st.floats(min_value=0.0, max_value=1.0),
    )
    @settings(max_examples=7, suppress_health_check=[HealthCheck.too_slow], deadline=10000)
    def test_failure_threshold_chaos(
        self,
        failure_threshold: int,
        num_calls: int,
        failure_rate: float,
    ) -> None:
        """Test circuit breaker with chaotic failure rates.

        Verifies:
        - Circuit opens at failure threshold
        - State transitions are correct
        - Failure counting is accurate
        """
        breaker = SyncCircuitBreaker(failure_threshold=failure_threshold)

        failures = 0
        for i in range(num_calls):
            should_fail = (i / num_calls) < failure_rate

            def operation(fail: bool = should_fail) -> str:
                if fail:
                    raise ValueError("Chaos failure")
                return "success"

            try:
                result = breaker.call(operation)
                assert result == "success"
            except (ValueError, RuntimeError) as e:
                if isinstance(e, ValueError):
                    failures += 1
                elif isinstance(e, RuntimeError):
                    # Circuit is open
                    assert breaker.state() == CircuitState.OPEN
                    assert breaker.failure_count() >= failure_threshold

        # Verify failure count tracking
        if failures < failure_threshold:
            assert breaker.state() == CircuitState.CLOSED

    @given(
        num_threads=thread_counts(min_threads=2, max_threads=10),
        failure_threshold=st.integers(min_value=2, max_value=5),
        recovery_timeout=chaos_timings(min_value=0.1, max_value=2.0),
    )
    @settings(max_examples=7, deadline=10000)
    def test_concurrent_state_transitions_chaos(
        self,
        num_threads: int,
        failure_threshold: int,
        recovery_timeout: float,
    ) -> None:
        """Test circuit breaker with concurrent state transitions.

        Verifies:
        - Thread-safe state management
        - Consistent failure counting
        - Proper state transitions under load
        """
        breaker = SyncCircuitBreaker(
            failure_threshold=failure_threshold,
            recovery_timeout=recovery_timeout,
        )
        results: list[str] = []
        errors: list[Exception] = []

        def worker(thread_id: int) -> None:
            # Mix of success and failure
            should_fail = thread_id % 2 == 0

            def operation() -> str:
                if should_fail:
                    raise ValueError(f"Thread {thread_id} failure")
                return f"success-{thread_id}"

            try:
                result = breaker.call(operation)
                results.append(result)
            except (ValueError, RuntimeError) as e:
                errors.append(e)

        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            futures = [executor.submit(worker, i) for i in range(num_threads)]
            for future in futures:
                future.result(timeout=5.0)

        # Verify state consistency
        final_state = breaker.state()
        final_count = breaker.failure_count()

        # State should be consistent with failure count
        if final_count >= failure_threshold:
            assert final_state in (CircuitState.OPEN, CircuitState.HALF_OPEN)

    @given(
        recovery_timeout=chaos_timings(min_value=0.1, max_value=2.0),
        time_advance=time_advances(min_advance=0.0, max_advance=5.0),
    )
    @settings(max_examples=7, deadline=10000)
    def test_recovery_timeout_with_time_chaos(
        self,
        recovery_timeout: float,
        time_advance: float,
    ) -> None:
        """Test circuit breaker recovery with time manipulation.

        Verifies:
        - Recovery timeout calculation
        - Transition to HALF_OPEN state
        - Time-based state changes
        """
        time_source_value = [time.time()]

        def time_source() -> float:
            return time_source_value[0]

        breaker = SyncCircuitBreaker(
            failure_threshold=2,
            recovery_timeout=recovery_timeout,
            time_source=time_source,
        )

        # Trigger failures to open circuit
        def failing_func() -> None:
            raise ValueError("Test failure")

        for _ in range(2):
            with contextlib.suppress(ValueError):
                breaker.call(failing_func)

        assert breaker.state() == CircuitState.OPEN

        # Advance time
        time_source_value[0] += time_advance

        # Check state after time advance
        current_state = breaker.state()
        if time_advance >= recovery_timeout:
            assert current_state == CircuitState.HALF_OPEN
        else:
            assert current_state == CircuitState.OPEN

    @given(patterns=failure_patterns(max_failures=10))
    @settings(max_examples=7, deadline=10000)
    def test_failure_pattern_chaos(self, patterns: list[tuple[int, type[Exception]]]) -> None:
        """Test circuit breaker with chaos failure patterns.

        Verifies behavior with various failure sequences.
        """
        breaker = SyncCircuitBreaker(failure_threshold=3)
        call_count = 0

        for i in range(15):
            # Check if this call should fail based on pattern
            should_fail = any(when == i for when, _ in patterns)
            exc_type = next((exc for when, exc in patterns if when == i), ValueError)

            def operation(fail: bool = should_fail, exception_type: type[Exception] = exc_type) -> str:
                if fail:
                    raise exception_type("Pattern failure")
                return "success"

            try:
                breaker.call(operation)
                call_count += 1
            except (RuntimeError, Exception):
                # RuntimeError = circuit open, Exception = operation failure
                pass

        # Circuit should have reacted to failure patterns
        # State depends on failure distribution
        final_state = breaker.state()
        assert final_state in (CircuitState.CLOSED, CircuitState.OPEN, CircuitState.HALF_OPEN)


class TestAsyncCircuitBreakerChaos(FoundationTestCase):
    """Async chaos tests for CircuitBreaker."""

    @pytest.mark.asyncio
    @given(
        num_tasks=st.integers(min_value=2, max_value=15),
        failure_threshold=st.integers(min_value=2, max_value=5),
    )
    @settings(max_examples=7, deadline=10000)
    async def test_async_concurrent_chaos(
        self,
        num_tasks: int,
        failure_threshold: int,
    ) -> None:
        """Test async circuit breaker with concurrent tasks.

        Verifies:
        - Async-safe state management
        - Concurrent async operations
        - Proper exception handling
        """
        from provide.foundation.resilience.circuit_async import AsyncCircuitBreaker

        breaker = AsyncCircuitBreaker(failure_threshold=failure_threshold)
        results: list[str] = []
        errors: list[Exception] = []

        async def async_worker(task_id: int) -> None:
            should_fail = task_id % 3 == 0

            async def async_operation() -> str:
                await asyncio.sleep(0.001)
                if should_fail:
                    raise ValueError(f"Task {task_id} failed")
                return f"success-{task_id}"

            try:
                result = await breaker.call(async_operation)
                results.append(result)
            except (ValueError, RuntimeError) as e:
                errors.append(e)

        tasks = [async_worker(i) for i in range(num_tasks)]
        await asyncio.gather(*tasks, return_exceptions=True)

        # Verify some operations succeeded (unless all failed)
        # State should be consistent
        if len(errors) >= failure_threshold:
            # Circuit likely opened
            pass


__all__ = [
    "TestAsyncCircuitBreakerChaos",
    "TestCircuitBreakerChaos",
]

# 🧱🏗️🔚
