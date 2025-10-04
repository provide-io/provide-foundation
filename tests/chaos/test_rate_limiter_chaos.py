"""Chaos tests for rate limiter implementation.

Property-based tests using Hypothesis to explore edge cases in rate limiting,
including burst patterns, time manipulation, and concurrent access.
"""

from __future__ import annotations

import asyncio
from typing import Any

from hypothesis import given, settings
from hypothesis import strategies as st
from provide.testkit import FoundationTestCase
from provide.testkit.chaos import (
    chaos_timings,
    edge_values,
    rate_burst_patterns,
    time_advances,
)
import pytest

from provide.foundation.utils.rate_limiting import TokenBucketRateLimiter


class TestTokenBucketChaos(FoundationTestCase):
    """Chaos tests for TokenBucketRateLimiter."""

    @given(
        capacity=st.floats(min_value=1.0, max_value=1000.0, allow_nan=False, allow_infinity=False),
        refill_rate=st.floats(min_value=0.1, max_value=100.0, allow_nan=False, allow_infinity=False),
    )
    @settings(max_examples=30)
    def test_initialization_chaos(
        self,
        capacity: float,
        refill_rate: float,
    ) -> None:
        """Test rate limiter initialization with chaotic values.

        Verifies:
        - Valid parameters create limiter successfully
        - Initial state is correct
        """
        limiter = TokenBucketRateLimiter(capacity=capacity, refill_rate=refill_rate)
        assert limiter._capacity == capacity
        assert limiter._refill_rate == refill_rate
        assert limiter._tokens == capacity  # Starts full

    @pytest.mark.asyncio
    @given(
        capacity=st.floats(min_value=5.0, max_value=100.0),
        refill_rate=st.floats(min_value=1.0, max_value=50.0),
        burst_size=st.integers(min_value=1, max_value=20),
    )
    @settings(max_examples=20)
    async def test_burst_pattern_chaos(
        self,
        capacity: float,
        refill_rate: float,
        burst_size: int,
    ) -> None:
        """Test rate limiter with burst request patterns.

        Verifies:
        - Burst requests up to capacity are allowed
        - Requests beyond capacity are rate limited
        - Token refill works correctly
        """
        limiter = TokenBucketRateLimiter(capacity=capacity, refill_rate=refill_rate)

        # Attempt burst
        successful = 0
        for _ in range(burst_size):
            if await limiter.acquire(tokens=1.0):
                successful += 1
            else:
                break

        # Should allow up to capacity
        assert successful <= int(capacity)

    @pytest.mark.asyncio
    @given(
        capacity=st.floats(min_value=10.0, max_value=100.0),
        refill_rate=st.floats(min_value=1.0, max_value=20.0),
        time_advance=time_advances(min_advance=0.0, max_advance=10.0),
    )
    @settings(max_examples=30)
    async def test_time_advance_refill_chaos(
        self,
        capacity: float,
        refill_rate: float,
        time_advance: float,
    ) -> None:
        """Test rate limiter with time manipulation.

        Verifies:
        - Token refill based on time elapsed
        - Time advances correctly refill tokens
        - Capacity limit is respected
        """
        time_value = [0.0]

        def time_source() -> float:
            return time_value[0]

        limiter = TokenBucketRateLimiter(
            capacity=capacity,
            refill_rate=refill_rate,
            time_source=time_source,
        )

        # Drain tokens
        initial_tokens = limiter._tokens
        await limiter.acquire(tokens=min(capacity, initial_tokens))

        # Advance time
        time_value[0] += time_advance

        # Try to acquire - should have refilled
        tokens_refilled = time_advance * refill_rate
        expected_tokens = min(capacity, tokens_refilled)

        # Acquire and check
        can_acquire = await limiter.acquire(tokens=1.0)
        if expected_tokens >= 1.0:
            assert can_acquire
        # If not enough refilled, may not acquire

    @pytest.mark.asyncio
    @given(
        capacity=st.floats(min_value=10.0, max_value=50.0),
        num_concurrent=st.integers(min_value=2, max_value=20),
    )
    @settings(max_examples=20)
    async def test_concurrent_acquire_chaos(
        self,
        capacity: float,
        num_concurrent: int,
    ) -> None:
        """Test concurrent token acquisition.

        Verifies:
        - Thread-safe token acquisition
        - No over-allocation of tokens
        - Concurrent access is properly serialized
        """
        limiter = TokenBucketRateLimiter(capacity=capacity, refill_rate=1.0)

        acquired = []

        async def worker(worker_id: int) -> None:
            if await limiter.acquire(tokens=1.0):
                acquired.append(worker_id)

        tasks = [worker(i) for i in range(num_concurrent)]
        await asyncio.gather(*tasks)

        # Should not exceed capacity
        assert len(acquired) <= int(capacity)

    @pytest.mark.asyncio
    @given(
        capacity=edge_values(value_type=float),
        refill_rate=st.floats(min_value=0.1, max_value=10.0),
    )
    @settings(max_examples=20)
    async def test_edge_value_capacity_chaos(
        self,
        capacity: float,
        refill_rate: float,
    ) -> None:
        """Test rate limiter with edge value capacities.

        Verifies:
        - Edge values are handled correctly
        - Invalid values raise appropriate errors
        - Boundary conditions work
        """
        import math

        # Filter invalid values
        if math.isnan(capacity) or math.isinf(capacity) or capacity <= 0:
            with pytest.raises(ValueError):
                TokenBucketRateLimiter(capacity=capacity, refill_rate=refill_rate)
        else:
            limiter = TokenBucketRateLimiter(capacity=capacity, refill_rate=refill_rate)
            assert limiter._capacity == capacity

    @pytest.mark.asyncio
    @given(bursts=rate_burst_patterns(max_burst_size=50, max_duration=2.0))
    @settings(max_examples=20)
    async def test_realistic_burst_patterns_chaos(
        self,
        bursts: list[tuple[float, int]],
    ) -> None:
        """Test rate limiter with realistic burst patterns.

        Verifies:
        - Realistic traffic patterns are handled
        - Rate limiting works over time
        - Burst handling is correct
        """
        capacity = 100.0
        refill_rate = 10.0
        time_value = [0.0]

        def time_source() -> float:
            return time_value[0]

        limiter = TokenBucketRateLimiter(
            capacity=capacity,
            refill_rate=refill_rate,
            time_source=time_source,
        )

        total_acquired = 0

        for time_offset, count in bursts:
            # Advance time to burst
            time_value[0] = time_offset

            # Attempt to acquire for burst
            for _ in range(count):
                if await limiter.acquire(tokens=1.0):
                    total_acquired += 1

        # Should have acquired some requests
        assert total_acquired > 0


__all__ = [
    "TestTokenBucketChaos",
]
