"""Tests for rate limiting utilities."""

import asyncio
import time
import pytest

from provide.foundation.utils.rate_limiting import TokenBucketRateLimiter


class TestTokenBucketRateLimiter:
    """Test TokenBucketRateLimiter functionality."""

    def test_init_validates_parameters(self):
        """Test that initialization validates parameters."""
        # Valid parameters should work
        limiter = TokenBucketRateLimiter(capacity=10.0, refill_rate=5.0)
        assert limiter._capacity == 10.0
        assert limiter._refill_rate == 5.0

        # Invalid capacity should raise ValueError
        with pytest.raises(ValueError, match="Capacity must be positive"):
            TokenBucketRateLimiter(capacity=0, refill_rate=5.0)
        
        with pytest.raises(ValueError, match="Capacity must be positive"):
            TokenBucketRateLimiter(capacity=-1, refill_rate=5.0)

        # Invalid refill rate should raise ValueError  
        with pytest.raises(ValueError, match="Refill rate must be positive"):
            TokenBucketRateLimiter(capacity=10.0, refill_rate=0)
        
        with pytest.raises(ValueError, match="Refill rate must be positive"):
            TokenBucketRateLimiter(capacity=10.0, refill_rate=-1)

    @pytest.mark.asyncio
    async def test_initial_tokens_available(self):
        """Test that limiter starts with full capacity of tokens."""
        limiter = TokenBucketRateLimiter(capacity=5.0, refill_rate=1.0)
        
        # Should allow up to capacity requests immediately
        for _ in range(5):
            assert await limiter.is_allowed() is True
        
        # Next request should be denied
        assert await limiter.is_allowed() is False

    @pytest.mark.asyncio
    async def test_token_refill_over_time(self):
        """Test that tokens are refilled over time."""
        # Create limiter with 1 token capacity, refilling at 2 tokens/second
        limiter = TokenBucketRateLimiter(capacity=1.0, refill_rate=2.0)
        
        # Use the initial token
        assert await limiter.is_allowed() is True
        assert await limiter.is_allowed() is False
        
        # Wait for half a second - should get 1 token back (2 tokens/sec * 0.5s = 1 token)
        await asyncio.sleep(0.6)
        assert await limiter.is_allowed() is True
        
        # Should be denied again immediately
        assert await limiter.is_allowed() is False

    @pytest.mark.asyncio 
    async def test_burst_capacity_limit(self):
        """Test that tokens don't accumulate beyond capacity."""
        limiter = TokenBucketRateLimiter(capacity=3.0, refill_rate=10.0)
        
        # Use all initial tokens
        for _ in range(3):
            assert await limiter.is_allowed() is True
        assert await limiter.is_allowed() is False
        
        # Wait long enough for many tokens to be generated (way more than capacity)
        await asyncio.sleep(1.0)  # Should generate 10 tokens, but capacity is 3
        
        # Should only be able to use 3 tokens (capacity limit)
        for _ in range(3):
            assert await limiter.is_allowed() is True
        assert await limiter.is_allowed() is False

    @pytest.mark.asyncio
    async def test_get_current_tokens(self):
        """Test getting current token count."""
        limiter = TokenBucketRateLimiter(capacity=5.0, refill_rate=1.0)
        
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
    async def test_concurrent_access(self):
        """Test thread-safety with concurrent access."""
        limiter = TokenBucketRateLimiter(capacity=10.0, refill_rate=1.0)
        
        # Create multiple concurrent tasks trying to get tokens
        async def try_get_token():
            return await limiter.is_allowed()
        
        tasks = [try_get_token() for _ in range(20)]
        results = await asyncio.gather(*tasks)
        
        # Should have exactly 10 successes (the initial capacity)
        successful_requests = sum(results)
        assert successful_requests == 10

    @pytest.mark.asyncio
    async def test_fractional_values(self):
        """Test that fractional capacity and refill rates work."""
        limiter = TokenBucketRateLimiter(capacity=2.5, refill_rate=0.5)
        
        # Should allow 2 requests initially (2.5 capacity, but we consume 1.0 per request)
        assert await limiter.is_allowed() is True
        assert await limiter.is_allowed() is True
        assert await limiter.is_allowed() is False  # 0.5 tokens remaining, need 1.0
        
        # Wait for 2 seconds to get 1 more token (0.5 tokens/sec * 2s = 1 token)
        await asyncio.sleep(2.1)
        assert await limiter.is_allowed() is True