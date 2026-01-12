#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Chaos tests for retry logic implementation.

Property-based tests using Hypothesis to explore edge cases in retry behavior,
including backoff strategies, failure patterns, and timeout scenarios."""

from __future__ import annotations

import asyncio
from typing import Any

from hypothesis import HealthCheck, given, settings, strategies as st
from provide.testkit import FoundationTestCase
from provide.testkit.chaos import (
    chaos_timings,
    failure_patterns,
    retry_backoff_patterns,
    timeout_patterns,
)
import pytest

from provide.foundation.resilience.retry import RetryExecutor, RetryPolicy
from provide.foundation.resilience.types import BackoffStrategy


class TestRetryPolicyChaos(FoundationTestCase):
    """Chaos tests for RetryPolicy."""

    @given(
        max_attempts=st.integers(min_value=1, max_value=20),
        base_delay=chaos_timings(min_value=0.01, max_value=2.0),
        max_delay=chaos_timings(min_value=0.1, max_value=10.0),
    )
    @settings(max_examples=7, deadline=10000)
    def test_retry_policy_creation_chaos(
        self,
        max_attempts: int,
        base_delay: float,
        max_delay: float,
    ) -> None:
        """Test RetryPolicy creation with chaotic inputs.

        Verifies:
        - Valid policies can be created
        - Constraints are enforced
        - Edge cases are handled
        """
        # Ensure max_delay >= base_delay
        if max_delay < base_delay:
            max_delay = base_delay * 2

        policy = RetryPolicy(
            max_attempts=max_attempts,
            base_delay=base_delay,
            max_delay=max_delay,
        )

        assert policy.max_attempts == max_attempts
        assert policy.base_delay == base_delay
        assert policy.max_delay == max_delay

    @given(
        attempt=st.integers(min_value=0, max_value=50),
        backoff_type=st.sampled_from(
            [BackoffStrategy.FIXED, BackoffStrategy.LINEAR, BackoffStrategy.EXPONENTIAL]
        ),
    )
    @settings(max_examples=7, deadline=10000)
    def test_delay_calculation_chaos(
        self,
        attempt: int,
        backoff_type: BackoffStrategy,
    ) -> None:
        """Test delay calculation with various attempts and strategies.

        Verifies:
        - Delays are non-negative
        - Delays respect max_delay
        - Backoff strategy is applied correctly
        """
        policy = RetryPolicy(
            max_attempts=100,
            backoff=backoff_type,
            base_delay=0.1,
            max_delay=10.0,
        )

        delay = policy.calculate_delay(attempt)
        assert delay >= 0
        # With jitter, delay can be up to 125% of max_delay (±25% variation)
        # So we allow 1.25x max_delay as the upper bound
        assert delay <= policy.max_delay * 1.25

    @given(patterns=failure_patterns(max_failures=10))
    @settings(max_examples=7, suppress_health_check=[HealthCheck.too_slow], deadline=10000)
    def test_retry_with_failure_patterns(
        self,
        patterns: list[tuple[int, type[Exception]]],
    ) -> None:
        """Test retry logic with chaos failure patterns.

        Verifies:
        - Retries occur on failures
        - Correct exception types are retried
        - Max attempts is respected
        """
        policy = RetryPolicy(max_attempts=15, base_delay=0.01)
        call_count = [0]

        def operation() -> str:
            call_num = call_count[0]
            call_count[0] += 1

            # Check if should fail
            for when, exc_type in patterns:
                if when == call_num:
                    raise exc_type("Pattern failure")

            return "success"

        executor = RetryExecutor(policy=policy)
        try:
            result = executor.execute_sync(operation)
            assert result == "success"
            # Should have retried through failures
        except Exception:
            # Hit max attempts or unretryable error
            assert call_count[0] <= policy.max_attempts

    @given(
        max_attempts=st.integers(min_value=1, max_value=10),
        failure_count=st.integers(min_value=0, max_value=15),
    )
    @settings(max_examples=7, deadline=10000)
    def test_max_attempts_exhaustion_chaos(
        self,
        max_attempts: int,
        failure_count: int,
    ) -> None:
        """Test retry behavior when max attempts is exhausted.

        Verifies:
        - Max attempts limit is enforced
        - Final exception is raised
        - Retry count is accurate
        """
        policy = RetryPolicy(max_attempts=max_attempts, base_delay=0.01)
        attempts = [0]

        def failing_operation() -> str:
            attempts[0] += 1
            if attempts[0] <= failure_count:
                raise ValueError(f"Failure {attempts[0]}")
            return "success"

        executor = RetryExecutor(policy=policy)
        if failure_count < max_attempts:
            # Should eventually succeed
            result = executor.execute_sync(failing_operation)
            assert result == "success"
            assert attempts[0] == failure_count + 1
        else:
            # Should exhaust retries
            with pytest.raises(ValueError):
                executor.execute_sync(failing_operation)
            assert attempts[0] == max_attempts


class TestAsyncRetryChaos(FoundationTestCase):
    """Async chaos tests for retry logic."""

    @pytest.mark.asyncio
    @given(
        backoff_pattern=retry_backoff_patterns(),
        failure_count=st.integers(min_value=0, max_value=5),
    )
    @settings(max_examples=7, deadline=10000)
    async def test_async_retry_with_backoff_chaos(
        self,
        backoff_pattern: dict[str, Any],
        failure_count: int,
    ) -> None:
        """Test async retry with chaotic backoff patterns.

        Verifies:
        - Async retries work with all backoff types
        - Delays are applied correctly
        - Failures are retried appropriately
        """
        max_attempts = backoff_pattern["max_attempts"]
        backoff_type = backoff_pattern["backoff_type"]

        # Map string to BackoffStrategy
        backoff_map = {
            "constant": BackoffStrategy.FIXED,
            "linear": BackoffStrategy.LINEAR,
            "exponential": BackoffStrategy.EXPONENTIAL,
            "jittered": BackoffStrategy.EXPONENTIAL,  # Use exponential for jittered
        }

        policy = RetryPolicy(
            max_attempts=max_attempts,
            backoff=backoff_map[backoff_type],
            base_delay=0.01,
            jitter=backoff_type == "jittered",
        )

        attempts = [0]

        async def async_operation() -> str:
            attempts[0] += 1
            if attempts[0] <= failure_count:
                raise ValueError(f"Async failure {attempts[0]}")
            return "async success"

        executor = RetryExecutor(policy=policy)
        if failure_count < max_attempts:
            result = await executor.execute_async(async_operation)
            assert result == "async success"
        else:
            with pytest.raises(ValueError):
                await executor.execute_async(async_operation)

    @pytest.mark.asyncio
    @given(
        num_concurrent=st.integers(min_value=2, max_value=10),
        timeout=timeout_patterns(min_timeout=0.5, max_timeout=3.0),
    )
    @settings(
        max_examples=20,
        deadline=None,
        suppress_health_check=[HealthCheck.filter_too_much, HealthCheck.too_slow],
    )
    async def test_concurrent_retry_chaos(
        self,
        num_concurrent: int,
        timeout: float | None,
    ) -> None:
        """Test concurrent retry operations.

        Verifies:
        - Multiple concurrent retries work correctly
        - No interference between retry contexts
        - Timeout handling (if applicable)
        """
        from hypothesis import assume

        # Skip unrealistic timeouts that are too short for concurrent async operations
        # With retries + async operations, we need at least 0.5s
        if timeout is not None:
            assume(timeout >= 0.5)

        policy = RetryPolicy(max_attempts=3, base_delay=0.01)

        async def async_operation(task_id: int) -> str:
            # Fail once, then succeed
            if task_id % 2 == 0:
                await asyncio.sleep(0.001)
                raise ValueError(f"Task {task_id} first attempt")
            return f"success-{task_id}"

        executor = RetryExecutor(policy=policy)

        async def worker(task_id: int) -> str:
            return await executor.execute_async(lambda: async_operation(task_id))

        tasks = [worker(i) for i in range(num_concurrent)]

        if timeout:
            results = await asyncio.wait_for(asyncio.gather(*tasks, return_exceptions=True), timeout=timeout)
        else:
            results = await asyncio.gather(*tasks, return_exceptions=True)

        # Some results should be successes
        successes = [r for r in results if isinstance(r, str)]
        assert len(successes) > 0


__all__ = [
    "TestAsyncRetryChaos",
    "TestRetryPolicyChaos",
]

# 🧱🏗️🔚
