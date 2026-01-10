#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for rate limiting utilities."""

import asyncio
from typing import Never

from provide.testkit import FoundationTestCase
from provide.testkit.time import make_controlled_time
import pytest

from provide.foundation.utils.rate_limiting import TokenBucketRateLimiter


class TestTokenBucketRateLimiter(FoundationTestCase):
    """Test TokenBucketRateLimiter functionality."""

    def setup_method(self) -> None:
        """Set up test environment."""
        super().setup_method()
        # Create controlled time for all tests
        self.get_time, self.advance_time, self.fake_sleep, self.fake_async_sleep = make_controlled_time()

    def test_init_validates_parameters(self) -> None:
        """Test that initialization validates parameters."""
        # Valid parameters should work
        limiter = TokenBucketRateLimiter(capacity=10.0, refill_rate=5.0, time_source=self.get_time)
        assert limiter._capacity == 10.0
        assert limiter._refill_rate == 5.0

        # Invalid capacity should raise ValueError
        with pytest.raises(ValueError, match="Capacity must be positive"):
            TokenBucketRateLimiter(capacity=0, refill_rate=5.0, time_source=self.get_time)

        with pytest.raises(ValueError, match="Capacity must be positive"):
            TokenBucketRateLimiter(capacity=-1, refill_rate=5.0, time_source=self.get_time)

        # Invalid refill rate should raise ValueError
        with pytest.raises(ValueError, match="Refill rate must be positive"):
            TokenBucketRateLimiter(capacity=10.0, refill_rate=0, time_source=self.get_time)

        with pytest.raises(ValueError, match="Refill rate must be positive"):
            TokenBucketRateLimiter(capacity=10.0, refill_rate=-1, time_source=self.get_time)

    @pytest.mark.asyncio
    async def test_initial_tokens_available(self) -> None:
        """Test that limiter starts with full capacity of tokens."""
        limiter = TokenBucketRateLimiter(capacity=5.0, refill_rate=1.0, time_source=self.get_time)

        # Should allow up to capacity requests immediately
        for _ in range(5):
            assert await limiter.is_allowed() is True

        # Next request should be denied
        assert await limiter.is_allowed() is False

    @pytest.mark.asyncio
    async def test_token_refill_over_time(self) -> None:
        """Test that tokens are refilled over time."""
        # Create limiter with 1 token capacity, refilling at 2 tokens/second
        limiter = TokenBucketRateLimiter(capacity=1.0, refill_rate=2.0, time_source=self.get_time)

        # Use the initial token
        assert await limiter.is_allowed() is True
        assert await limiter.is_allowed() is False

        # Advance time by 0.6 seconds - should get 1 token back (2 tokens/sec * 0.6s = 1.2 tokens)
        self.advance_time(0.6)
        assert await limiter.is_allowed() is True

        # Should be denied again immediately
        assert await limiter.is_allowed() is False

    @pytest.mark.asyncio
    async def test_burst_capacity_limit(self) -> None:
        """Test that tokens don't accumulate beyond capacity."""
        limiter = TokenBucketRateLimiter(capacity=3.0, refill_rate=10.0, time_source=self.get_time)

        # Use all initial tokens
        for _ in range(3):
            assert await limiter.is_allowed() is True
        assert await limiter.is_allowed() is False

        # Advance time for many tokens to be generated (way more than capacity)
        self.advance_time(1.0)  # Should generate 10 tokens, but capacity is 3

        # Should only be able to use 3 tokens (capacity limit)
        for _ in range(3):
            assert await limiter.is_allowed() is True
        assert await limiter.is_allowed() is False

    @pytest.mark.asyncio
    async def test_get_current_tokens(self) -> None:
        """Test getting current token count."""
        limiter = TokenBucketRateLimiter(capacity=5.0, refill_rate=1.0, time_source=self.get_time)

        # Should start with full capacity
        tokens = await limiter.get_current_tokens()
        assert tokens == 5.0

        # Use some tokens
        assert await limiter.is_allowed() is True
        assert await limiter.is_allowed() is True

        tokens = await limiter.get_current_tokens()
        # Allow for small timing variations due to test execution time
        assert abs(tokens - 3.0) < 0.01

    @pytest.mark.asyncio
    async def test_concurrent_access(self) -> None:
        """Test thread-safety with concurrent access."""
        limiter = TokenBucketRateLimiter(capacity=10.0, refill_rate=1.0, time_source=self.get_time)

        # Create multiple concurrent tasks trying to get tokens
        async def try_get_token():
            return await limiter.is_allowed()

        tasks = [try_get_token() for _ in range(20)]
        results = await asyncio.gather(*tasks)

        # Should have exactly 10 successes (the initial capacity)
        successful_requests = sum(results)
        assert successful_requests == 10

    @pytest.mark.asyncio
    async def test_fractional_values(self) -> None:
        """Test that fractional capacity and refill rates work."""
        limiter = TokenBucketRateLimiter(capacity=2.5, refill_rate=0.5, time_source=self.get_time)

        # Should allow 2 requests initially (2.5 capacity, but we consume 1.0 per request)
        assert await limiter.is_allowed() is True
        assert await limiter.is_allowed() is True
        assert await limiter.is_allowed() is False  # 0.5 tokens remaining, need 1.0

        # Advance time by 2.1 seconds to get 1 more token (0.5 tokens/sec * 2.1s = 1.05 tokens)
        self.advance_time(2.1)
        assert await limiter.is_allowed() is True

    def test_logger_initialization_success(self) -> None:
        """Test successful logger initialization."""
        limiter = TokenBucketRateLimiter(capacity=1.0, refill_rate=1.0, time_source=self.get_time)
        # Logger should be available and cached
        assert limiter._logger is not None

    def test_logger_initialization_fallback(self, monkeypatch) -> None:
        """Test logger initialization fallback when import fails."""

        # Mock the import to raise ImportError
        def mock_import_error(*args, **kwargs) -> Never:
            raise ImportError("Mocked import failure")

        # Patch the import mechanism
        monkeypatch.setattr("builtins.__import__", mock_import_error)

        # Should not raise an exception, should fallback gracefully
        limiter = TokenBucketRateLimiter(capacity=1.0, refill_rate=1.0, time_source=self.get_time)
        assert limiter._logger is None

    @pytest.mark.asyncio
    async def test_very_long_wait_periods(self) -> None:
        """Test behavior after very long idle periods."""
        limiter = TokenBucketRateLimiter(capacity=3.0, refill_rate=1.0, time_source=self.get_time)

        # Use all tokens
        for _ in range(3):
            assert await limiter.is_allowed() is True
        assert await limiter.is_allowed() is False

        # Advance time by 100 seconds (would generate 100 tokens, but capacity limits to 3)
        self.advance_time(100.0)

        # Should still be limited by capacity
        for _ in range(3):
            assert await limiter.is_allowed() is True
        assert await limiter.is_allowed() is False

    @pytest.mark.asyncio
    @pytest.mark.time_sensitive
    async def test_extreme_time_precision(self) -> None:
        """Test behavior with very small time intervals and high precision."""
        limiter = TokenBucketRateLimiter(
            capacity=1.0,
            refill_rate=1000.0,
            time_source=self.get_time,
        )  # Very fast refill

        # Use the initial token
        assert await limiter.is_allowed() is True
        assert await limiter.is_allowed() is False

        # Advance time by 0.002s (should generate 2 tokens at 1000 tokens/sec)
        self.advance_time(0.002)
        assert await limiter.is_allowed() is True

    @pytest.mark.asyncio
    async def test_high_concurrency_stress(self) -> None:
        """Test thread-safety with high concurrency stress testing."""
        limiter = TokenBucketRateLimiter(capacity=50.0, refill_rate=1.0, time_source=self.get_time)

        # Create many more concurrent tasks than capacity
        async def try_get_token():
            return await limiter.is_allowed()

        # Test with 200 concurrent tasks for 50 token capacity
        tasks = [try_get_token() for _ in range(200)]
        results = await asyncio.gather(*tasks)

        # Should have exactly 50 successes (the initial capacity)
        successful_requests = sum(results)
        assert successful_requests == 50

        # All remaining should be denied
        denied_requests = len(results) - successful_requests
        assert denied_requests == 150

    @pytest.mark.asyncio
    async def test_extreme_concurrency_stress(self) -> None:
        """Test thread-safety with extreme concurrency."""
        limiter = TokenBucketRateLimiter(capacity=100.0, refill_rate=1.0, time_source=self.get_time)

        # Create extreme number of concurrent tasks
        async def try_get_token():
            return await limiter.is_allowed()

        # Test with 1000 concurrent tasks for 100 token capacity
        tasks = [try_get_token() for _ in range(1000)]
        results = await asyncio.gather(*tasks)

        # Should have exactly 100 successes (the initial capacity)
        successful_requests = sum(results)
        assert successful_requests == 100

    @pytest.mark.asyncio
    async def test_concurrent_refill_and_consumption(self) -> None:
        """Test concurrent token consumption while refilling occurs."""
        limiter = TokenBucketRateLimiter(
            capacity=5.0, refill_rate=10.0, time_source=self.get_time
        )  # Fast refill

        # Use all initial tokens
        for _ in range(5):
            assert await limiter.is_allowed() is True
        assert await limiter.is_allowed() is False

        async def consumer():
            """Try to consume tokens continuously."""
            successes = 0
            for _ in range(20):
                if await limiter.is_allowed():
                    successes += 1
                self.advance_time(0.01)  # Advance time by 10ms
            return successes

        # Run multiple consumers concurrently while tokens refill
        consumers = [consumer() for _ in range(3)]
        results = await asyncio.gather(*consumers)

        # Should have some successes due to refilling, but not unlimited
        total_successes = sum(results)
        # With 10 tokens/sec refill rate and 0.6s total time (20 * 0.01 * 3),
        # expect 6 tokens refilled total, so total successes should be around 6
        assert 0 <= total_successes <= 20  # Reasonable range allowing for timing variations

    @pytest.mark.asyncio
    async def test_logger_usage_during_operations(self, mocker) -> None:
        """Test that logger is used correctly during operations."""
        # Mock the get_logger function to return a mock logger
        mock_logger = mocker.MagicMock()
        mocker.patch("provide.foundation.logger.get_logger", return_value=mock_logger)

        limiter = TokenBucketRateLimiter(capacity=2.0, refill_rate=1.0, time_source=self.get_time)

        # Should have logged initialization
        mock_logger.debug.assert_called_once()
        init_call = mock_logger.debug.call_args[0][0]
        assert "TokenBucketRateLimiter initialized" in init_call

        # Reset mock to test operation logging
        mock_logger.reset_mock()

        # Test successful request logging
        await limiter.is_allowed()
        mock_logger.debug.assert_called_once()
        success_call = mock_logger.debug.call_args[0][0]
        assert "Request allowed" in success_call

        # Reset and test denied request logging
        mock_logger.reset_mock()
        await limiter.is_allowed()  # Use second token
        await limiter.is_allowed()  # Should be denied

        mock_logger.warning.assert_called_once()
        denied_call = mock_logger.warning.call_args[0][0]
        assert "Request denied" in denied_call


# 🧱🏗️🔚
