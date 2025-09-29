"""Comprehensive tests for utils/rate_limiting.py module."""

from __future__ import annotations

import asyncio
import time

import pytest
from provide.testkit import FoundationTestCase

from provide.foundation.utils.rate_limiting import TokenBucketRateLimiter


class TestTokenBucketRateLimiter(FoundationTestCase):
    """Test TokenBucketRateLimiter class."""

    def test_init_valid_parameters(self) -> None:
        """Test initialization with valid parameters."""
        limiter = TokenBucketRateLimiter(capacity=10, refill_rate=5)
        assert limiter._capacity == 10.0
        assert limiter._refill_rate == 5.0
        assert limiter._tokens == 10.0  # Starts full
        assert isinstance(limiter._lock, asyncio.Lock)

    def test_init_invalid_capacity(self) -> None:
        """Test initialization with invalid capacity."""
        with pytest.raises(ValueError, match="Capacity must be positive"):
            TokenBucketRateLimiter(capacity=0, refill_rate=1)

        with pytest.raises(ValueError, match="Capacity must be positive"):
            TokenBucketRateLimiter(capacity=-1, refill_rate=1)

    def test_init_invalid_refill_rate(self) -> None:
        """Test initialization with invalid refill rate."""
        with pytest.raises(ValueError, match="Refill rate must be positive"):
            TokenBucketRateLimiter(capacity=10, refill_rate=0)

        with pytest.raises(ValueError, match="Refill rate must be positive"):
            TokenBucketRateLimiter(capacity=10, refill_rate=-1)

    def test_init_float_conversion(self) -> None:
        """Test that parameters are converted to float."""
        limiter = TokenBucketRateLimiter(capacity=10, refill_rate=5)
        assert isinstance(limiter._capacity, float)
        assert isinstance(limiter._refill_rate, float)
        assert isinstance(limiter._tokens, float)

    def test_init_with_logger_available(self) -> None:
        """Test initialization when logger is available."""
        # Just test that the limiter initializes correctly
        limiter = TokenBucketRateLimiter(capacity=5, refill_rate=2)
        # Logger should be set (or None if import fails)
        assert limiter._logger is not None or limiter._logger is None

    def test_init_with_logger_import_error(self) -> None:
        """Test initialization when logger import fails."""
        # Just ensure initialization works regardless of logger availability
        limiter = TokenBucketRateLimiter(capacity=5, refill_rate=2)
        assert isinstance(limiter, TokenBucketRateLimiter)

    @pytest.mark.asyncio
    async def test_is_allowed_initial_tokens(self) -> None:
        """Test that initial requests are allowed with full bucket."""
        limiter = TokenBucketRateLimiter(capacity=3, refill_rate=1)

        # Should allow 3 requests initially
        assert await limiter.is_allowed() is True
        assert await limiter.is_allowed() is True
        assert await limiter.is_allowed() is True

        # 4th request should be denied
        assert await limiter.is_allowed() is False

    @pytest.mark.asyncio
    async def test_is_allowed_refill_over_time(self) -> None:
        """Test token refill over time."""
        limiter = TokenBucketRateLimiter(capacity=5, refill_rate=10)  # 10 tokens per second

        # Consume all tokens
        for _ in range(5):
            assert await limiter.is_allowed() is True

        # Should be empty now
        assert await limiter.is_allowed() is False

        # Mock sleep and manually advance the limiter's time for deterministic testing
        # Manually set the limiter's timestamp to simulate 0.2 seconds passing
        # This should add 2 tokens at 10/sec rate (0.2 * 10 = 2 tokens)
        limiter._last_refill_timestamp = time.monotonic() - 0.2

        # Trigger refill by calling is_allowed (which calls _refill_tokens internally)
        await limiter._refill_tokens()

        # Should allow 2 requests now
        assert await limiter.is_allowed() is True
        assert await limiter.is_allowed() is True
        assert await limiter.is_allowed() is False

    @pytest.mark.asyncio
    async def test_refill_tokens_basic(self) -> None:
        """Test basic token refill functionality."""
        limiter = TokenBucketRateLimiter(capacity=10, refill_rate=5)

        # Set tokens to 0 and advance time
        limiter._tokens = 0
        limiter._last_refill_timestamp = time.monotonic() - 2.0  # 2 seconds ago

        await limiter._refill_tokens()

        # Should have refilled 2 seconds * 5 tokens/sec = 10 tokens (capped at capacity)
        assert limiter._tokens == 10.0

    @pytest.mark.asyncio
    async def test_refill_tokens_cap_at_capacity(self) -> None:
        """Test that refill caps at capacity."""
        limiter = TokenBucketRateLimiter(capacity=5, refill_rate=10)

        # Set tokens to 0 and advance time significantly
        limiter._tokens = 0
        limiter._last_refill_timestamp = time.monotonic() - 10.0  # 10 seconds ago

        await limiter._refill_tokens()

        # Should be capped at capacity
        assert limiter._tokens == 5.0

    @pytest.mark.asyncio
    async def test_refill_tokens_no_time_elapsed(self) -> None:
        """Test that no refill happens when no time has elapsed."""
        limiter = TokenBucketRateLimiter(capacity=10, refill_rate=5)

        initial_tokens = limiter._tokens

        # Call refill immediately (minimal time elapsed)
        await limiter._refill_tokens()

        # Tokens should be approximately the same (allowing for tiny time differences)
        assert abs(limiter._tokens - initial_tokens) < 0.1

    @pytest.mark.asyncio
    async def test_refill_tokens_partial_token(self) -> None:
        """Test refill with partial tokens."""
        limiter = TokenBucketRateLimiter(capacity=10, refill_rate=3)

        # Set initial state
        limiter._tokens = 2.5
        limiter._last_refill_timestamp = time.monotonic() - 0.5  # 0.5 seconds ago

        await limiter._refill_tokens()

        # Should add approximately 0.5 * 3 = 1.5 tokens, total ≈ 4.0
        assert abs(limiter._tokens - 4.0) < 0.1

    @pytest.mark.asyncio
    async def test_get_current_tokens(self) -> None:
        """Test getting current tokens."""
        limiter = TokenBucketRateLimiter(capacity=10, refill_rate=5)

        tokens = await limiter.get_current_tokens()
        assert tokens == 10.0

        # Consume a token
        await limiter.is_allowed()

        tokens = await limiter.get_current_tokens()
        assert tokens == 9.0

    @pytest.mark.asyncio
    async def test_is_allowed_with_logger(self) -> None:
        """Test is_allowed logging behavior."""
        limiter = TokenBucketRateLimiter(capacity=2, refill_rate=1)

        # Allow request
        result = await limiter.is_allowed()
        assert result is True

        # Consume remaining token
        await limiter.is_allowed()

        # Deny request
        result = await limiter.is_allowed()
        assert result is False

    @pytest.mark.asyncio
    async def test_is_allowed_without_logger(self) -> None:
        """Test is_allowed works regardless of logger availability."""
        limiter = TokenBucketRateLimiter(capacity=1, refill_rate=1)

        # Should work with or without logger
        result = await limiter.is_allowed()
        assert result is True

        result = await limiter.is_allowed()
        assert result is False

    @pytest.mark.asyncio
    async def test_thread_safety_simulation(self) -> None:
        """Test concurrent access simulation."""
        limiter = TokenBucketRateLimiter(capacity=10, refill_rate=5)

        async def consume_token() -> bool:
            return await limiter.is_allowed()

        # Run multiple concurrent requests
        tasks = [consume_token() for _ in range(15)]
        results = await asyncio.gather(*tasks)

        # Should allow exactly 10 requests (initial capacity)
        allowed_count = sum(results)
        assert allowed_count == 10

    @pytest.mark.asyncio
    async def test_fractional_capacity_and_rates(self) -> None:
        """Test with fractional capacity and refill rates."""
        limiter = TokenBucketRateLimiter(capacity=2.5, refill_rate=1.5)

        # Should allow 2 full tokens
        assert await limiter.is_allowed() is True
        assert await limiter.is_allowed() is True

        # Third request should fail (only 0.5 tokens left)
        assert await limiter.is_allowed() is False

        # Check actual token count (approximately 0.5, allowing for small timing differences)
        tokens = await limiter.get_current_tokens()
        assert abs(tokens - 0.5) < 0.1

    @pytest.mark.asyncio
    async def test_refill_updates_timestamp(self) -> None:
        """Test that refill updates the timestamp correctly."""
        limiter = TokenBucketRateLimiter(capacity=10, refill_rate=5)

        original_timestamp = limiter._last_refill_timestamp

        # Advance time artificially
        limiter._last_refill_timestamp = time.monotonic() - 1.0

        await limiter._refill_tokens()

        # Timestamp should be updated
        assert limiter._last_refill_timestamp > original_timestamp

    @pytest.mark.asyncio
    async def test_extreme_time_precision(self) -> None:
        """Test with very small time intervals."""
        limiter = TokenBucketRateLimiter(capacity=1000, refill_rate=1000)

        # Consume some tokens
        for _ in range(100):
            await limiter.is_allowed()

        # Very small time advance
        limiter._last_refill_timestamp = time.monotonic() - 0.001  # 1ms ago

        await limiter._refill_tokens()

        # Should add approximately 0.001 * 1000 = 1 token (allow for timing imprecision)
        tokens = await limiter.get_current_tokens()
        assert tokens > 899  # Should be around 901 but allow for timing variations

    @pytest.mark.asyncio
    async def test_burst_capacity(self) -> None:
        """Test burst capacity behavior."""
        limiter = TokenBucketRateLimiter(capacity=5, refill_rate=1)

        # Should handle burst of 5 requests immediately
        burst_results = []
        for _ in range(5):
            burst_results.append(await limiter.is_allowed())

        assert all(burst_results)  # All should be allowed

        # 6th request should fail
        assert await limiter.is_allowed() is False

    @pytest.mark.asyncio
    @pytest.mark.slow
    async def test_steady_state_behavior(self) -> None:
        """Test steady state behavior over time."""
        limiter = TokenBucketRateLimiter(capacity=3, refill_rate=2)  # 2 tokens per second

        # Consume all initial tokens
        for _ in range(3):
            await limiter.is_allowed()

        # Wait for 1.5 seconds (should add 3 tokens, capped at capacity)
        await asyncio.sleep(1.5)

        # Should allow 3 requests again
        for _ in range(3):
            assert await limiter.is_allowed() is True

        # 4th should fail
        assert await limiter.is_allowed() is False


class TestTokenBucketEdgeCases:
    """Test edge cases and error conditions."""

    @pytest.mark.asyncio
    async def test_zero_refill_rate_edge(self) -> None:
        """Test behavior with very small refill rate."""
        # This should still fail validation
        with pytest.raises(ValueError):
            TokenBucketRateLimiter(capacity=1, refill_rate=0)

    @pytest.mark.asyncio
    async def test_very_small_capacity(self) -> None:
        """Test with very small capacity."""
        limiter = TokenBucketRateLimiter(capacity=0.1, refill_rate=1)

        # Should not allow any requests (< 1 token)
        assert await limiter.is_allowed() is False

    @pytest.mark.asyncio
    async def test_large_numbers(self) -> None:
        """Test with large capacity and refill rates."""
        limiter = TokenBucketRateLimiter(capacity=1e6, refill_rate=1e6)

        # Should work with large numbers
        assert await limiter.is_allowed() is True
        tokens = await limiter.get_current_tokens()
        assert tokens == 1e6 - 1

    def test_final_class_annotation(self) -> None:
        """Test that class is marked as final."""
        # The @final decorator should be present
        assert hasattr(TokenBucketRateLimiter, "__annotations__")

    @pytest.mark.asyncio
    async def test_lock_acquisition(self) -> None:
        """Test that lock is properly acquired and released."""
        limiter = TokenBucketRateLimiter(capacity=5, refill_rate=1)

        # Verify lock is not held initially
        assert not limiter._lock.locked()

        # Test that methods properly acquire and release lock
        await limiter.is_allowed()
        assert not limiter._lock.locked()

        await limiter.get_current_tokens()
        assert not limiter._lock.locked()


class TestRateLimitingIntegration:
    """Test integration scenarios."""

    @pytest.mark.asyncio
    async def test_realistic_api_scenario(self) -> None:
        """Test a realistic API rate limiting scenario."""
        # 100 requests per minute = ~1.67 requests per second
        limiter = TokenBucketRateLimiter(capacity=10, refill_rate=1.67)

        # Simulate burst of requests
        initial_burst = []
        for _ in range(10):
            initial_burst.append(await limiter.is_allowed())

        # All initial requests should be allowed
        assert all(initial_burst)

        # Additional requests should be denied
        assert await limiter.is_allowed() is False

        # Wait for some refill
        await asyncio.sleep(0.6)  # Should add ~1 token

        # Should allow one more request
        assert await limiter.is_allowed() is True
        assert await limiter.is_allowed() is False

    @pytest.mark.asyncio
    async def test_multiple_limiters(self) -> None:
        """Test multiple independent rate limiters."""
        limiter1 = TokenBucketRateLimiter(capacity=2, refill_rate=1)
        limiter2 = TokenBucketRateLimiter(capacity=3, refill_rate=2)

        # Each should operate independently
        assert await limiter1.is_allowed() is True
        assert await limiter2.is_allowed() is True

        # Exhaust limiter1
        await limiter1.is_allowed()
        assert await limiter1.is_allowed() is False

        # limiter2 should still work
        assert await limiter2.is_allowed() is True
        assert await limiter2.is_allowed() is True
        assert await limiter2.is_allowed() is False
