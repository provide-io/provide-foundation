#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for Foundation rate limiting system."""

import asyncio
import threading
import time

from provide.testkit import FoundationTestCase
import pytest

from provide.foundation.logger.ratelimit.limiters import (
    AsyncRateLimiter,
    GlobalRateLimiter,
    SyncRateLimiter,
)


class TestSyncRateLimiter(FoundationTestCase):
    """Test SyncRateLimiter class."""

    def test_sync_rate_limiter_init_valid(self) -> None:
        """Test SyncRateLimiter initialization with valid parameters."""
        limiter = SyncRateLimiter(capacity=10.0, refill_rate=2.0)

        assert limiter.capacity == 10.0
        assert limiter.refill_rate == 2.0
        assert limiter.tokens == 10.0
        assert limiter.total_allowed == 0
        assert limiter.total_denied == 0
        assert limiter.last_denied_time is None

    def test_sync_rate_limiter_init_invalid_capacity(self) -> None:
        """Test SyncRateLimiter raises error for invalid capacity."""
        with pytest.raises(ValueError, match="Capacity must be positive"):
            SyncRateLimiter(capacity=0, refill_rate=1.0)

        with pytest.raises(ValueError, match="Capacity must be positive"):
            SyncRateLimiter(capacity=-1.0, refill_rate=1.0)

    def test_sync_rate_limiter_init_invalid_refill_rate(self) -> None:
        """Test SyncRateLimiter raises error for invalid refill rate."""
        with pytest.raises(ValueError, match="Refill rate must be positive"):
            SyncRateLimiter(capacity=10.0, refill_rate=0)

        with pytest.raises(ValueError, match="Refill rate must be positive"):
            SyncRateLimiter(capacity=10.0, refill_rate=-1.0)

    def test_sync_rate_limiter_allows_within_capacity(self) -> None:
        """Test SyncRateLimiter allows requests within capacity."""
        limiter = SyncRateLimiter(capacity=3.0, refill_rate=1.0)

        # Should allow first 3 requests
        assert limiter.is_allowed() is True
        assert limiter.is_allowed() is True
        assert limiter.is_allowed() is True

        # Fourth request should be denied
        assert limiter.is_allowed() is False

        stats = limiter.get_stats()
        assert stats["total_allowed"] == 3
        assert stats["total_denied"] == 1

    def test_sync_rate_limiter_refill_over_time(self) -> None:
        """Test SyncRateLimiter refills tokens over time."""
        limiter = SyncRateLimiter(capacity=2.0, refill_rate=10.0)  # 10 tokens/second

        # Consume all tokens
        assert limiter.is_allowed() is True
        assert limiter.is_allowed() is True
        assert limiter.is_allowed() is False

        # Manually advance time to simulate refill instead of using timing-sensitive sleep
        # Set the last refill timestamp to simulate 0.15 seconds ago (1.5 tokens)
        limiter.last_refill = time.monotonic() - 0.15

        # Should be allowed again after manual time advancement
        assert limiter.is_allowed() is True
        assert limiter.is_allowed() is False  # Only 1.5 tokens refilled

    def test_sync_rate_limiter_thread_safety(self) -> None:
        """Test SyncRateLimiter is thread-safe."""
        limiter = SyncRateLimiter(capacity=100.0, refill_rate=50.0)
        results = []

        def worker() -> None:
            for _ in range(20):
                result = limiter.is_allowed()
                results.append(result)

        # Create multiple threads
        threads = [threading.Thread(daemon=True, target=worker) for _ in range(5)]

        # Start all threads
        for thread in threads:
            thread.start()

        # Wait for completion
        for thread in threads:
            thread.join(timeout=10.0)

        # Check that we got reasonable results
        allowed_count = sum(results)
        denied_count = len(results) - allowed_count

        # Some requests should be allowed, some denied
        assert allowed_count > 0
        assert allowed_count <= 100  # Within capacity

        stats = limiter.get_stats()
        assert stats["total_allowed"] == allowed_count
        assert stats["total_denied"] == denied_count

    def test_sync_rate_limiter_get_stats(self) -> None:
        """Test SyncRateLimiter statistics."""
        limiter = SyncRateLimiter(capacity=5.0, refill_rate=2.0)

        # Initial stats
        stats = limiter.get_stats()
        assert stats["capacity"] == 5.0
        assert stats["refill_rate"] == 2.0
        assert stats["total_allowed"] == 0
        assert stats["total_denied"] == 0
        assert stats["last_denied_time"] is None

        # Use some tokens
        limiter.is_allowed()  # allowed
        limiter.is_allowed()  # allowed

        stats = limiter.get_stats()
        assert stats["total_allowed"] == 2
        # Allow for small floating point precision issues
        assert abs(stats["tokens_available"] - 3.0) < 0.01


class TestAsyncRateLimiter(FoundationTestCase):
    """Test AsyncRateLimiter class."""

    def test_async_rate_limiter_init_valid(self) -> None:
        """Test AsyncRateLimiter initialization with valid parameters."""
        limiter = AsyncRateLimiter(capacity=5.0, refill_rate=1.0)

        assert limiter.capacity == 5.0
        assert limiter.refill_rate == 1.0
        assert limiter.tokens == 5.0
        assert limiter.total_allowed == 0
        assert limiter.total_denied == 0

    def test_async_rate_limiter_init_invalid(self) -> None:
        """Test AsyncRateLimiter raises error for invalid parameters."""
        with pytest.raises(ValueError, match="Capacity must be positive"):
            AsyncRateLimiter(capacity=-1.0, refill_rate=1.0)

        with pytest.raises(ValueError, match="Refill rate must be positive"):
            AsyncRateLimiter(capacity=5.0, refill_rate=0)

    @pytest.mark.asyncio
    async def test_async_rate_limiter_allows_within_capacity(self) -> None:
        """Test AsyncRateLimiter allows requests within capacity."""
        limiter = AsyncRateLimiter(capacity=3.0, refill_rate=1.0)

        # Should allow first 3 requests
        assert await limiter.is_allowed() is True
        assert await limiter.is_allowed() is True
        assert await limiter.is_allowed() is True

        # Fourth request should be denied
        assert await limiter.is_allowed() is False

        stats = await limiter.get_stats()
        assert stats["total_allowed"] == 3
        assert stats["total_denied"] == 1

    @pytest.mark.asyncio
    async def test_async_rate_limiter_refill_over_time(self) -> None:
        """Test AsyncRateLimiter refills tokens over time."""
        limiter = AsyncRateLimiter(capacity=2.0, refill_rate=10.0)

        # Consume all tokens
        assert await limiter.is_allowed() is True
        assert await limiter.is_allowed() is True
        assert await limiter.is_allowed() is False

        # Manually advance time to simulate refill instead of using timing-sensitive sleep
        # Set the last refill timestamp to simulate 0.15 seconds ago (1.5 tokens)
        import time

        limiter.last_refill = time.monotonic() - 0.15

        # Minimal async yield to allow event loop processing
        await asyncio.sleep(0)

        # Should be allowed again after manual time advancement
        assert await limiter.is_allowed() is True
        assert await limiter.is_allowed() is False

    @pytest.mark.asyncio
    async def test_async_rate_limiter_concurrent_access(self) -> None:
        """Test AsyncRateLimiter handles concurrent access."""
        limiter = AsyncRateLimiter(capacity=50.0, refill_rate=25.0)

        async def worker() -> list[bool]:
            results = []
            for _ in range(10):
                result = await limiter.is_allowed()
                results.append(result)
            return results

        # Run multiple concurrent workers
        tasks = [asyncio.create_task(worker()) for _ in range(8)]
        all_results = await asyncio.gather(*tasks)

        # Flatten results
        results = [result for worker_results in all_results for result in worker_results]

        allowed_count = sum(results)
        denied_count = len(results) - allowed_count

        # Some should be allowed, some denied
        assert allowed_count > 0
        assert allowed_count <= 50  # Within capacity

        stats = await limiter.get_stats()
        assert stats["total_allowed"] == allowed_count
        assert stats["total_denied"] == denied_count

    @pytest.mark.asyncio
    async def test_async_rate_limiter_get_stats(self) -> None:
        """Test AsyncRateLimiter statistics."""
        limiter = AsyncRateLimiter(capacity=10.0, refill_rate=3.0)

        stats = await limiter.get_stats()
        assert stats["capacity"] == 10.0
        assert stats["refill_rate"] == 3.0
        assert stats["total_allowed"] == 0
        assert stats["total_denied"] == 0

        # Use some tokens
        await limiter.is_allowed()
        await limiter.is_allowed()

        stats = await limiter.get_stats()
        assert stats["total_allowed"] == 2
        # Allow for small floating point precision issues
        assert abs(stats["tokens_available"] - 8.0) < 0.01


class TestGlobalRateLimiter(FoundationTestCase):
    """Test GlobalRateLimiter singleton class."""

    def test_global_rate_limiter_singleton(self) -> None:
        """Test GlobalRateLimiter is a singleton."""
        limiter1 = GlobalRateLimiter()
        limiter2 = GlobalRateLimiter()

        assert limiter1 is limiter2

    def test_global_rate_limiter_thread_safe_singleton(self) -> None:
        """Test GlobalRateLimiter singleton is thread-safe."""
        instances = []

        def create_instance() -> None:
            instances.append(GlobalRateLimiter())

        threads = [threading.Thread(daemon=True, target=create_instance) for _ in range(10)]

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join(timeout=10.0)

        # All instances should be the same
        first_instance = instances[0]
        for instance in instances[1:]:
            assert instance is first_instance

    def test_global_rate_limiter_configure_global_only(self) -> None:
        """Test GlobalRateLimiter configuration with global limits only."""
        limiter = GlobalRateLimiter()

        limiter.configure(global_rate=10.0, global_capacity=20.0)

        assert limiter.global_rate == 10.0
        assert limiter.global_capacity == 20.0
        assert limiter.global_limiter is not None
        assert isinstance(limiter.global_limiter, SyncRateLimiter)

    def test_global_rate_limiter_configure_per_logger(self) -> None:
        """Test GlobalRateLimiter configuration with per-logger limits."""
        limiter = GlobalRateLimiter()

        per_logger_rates = {
            "app.module1": (5.0, 10.0),
            "app.module2": (2.0, 5.0),
        }

        limiter.configure(per_logger_rates=per_logger_rates)

        assert len(limiter.logger_limiters) == 2
        assert "app.module1" in limiter.logger_limiters
        assert "app.module2" in limiter.logger_limiters

    def test_global_rate_limiter_configure_buffered(self) -> None:
        """Test GlobalRateLimiter configuration with buffered limiter."""
        limiter = GlobalRateLimiter()

        limiter.configure(
            global_rate=5.0,
            global_capacity=10.0,
            use_buffered=True,
            max_queue_size=100,
        )

        assert limiter.use_buffered is True
        assert limiter.max_queue_size == 100
        # BufferedRateLimiter is imported dynamically, so just check it's not SyncRateLimiter
        assert limiter.global_limiter is not None

    def test_global_rate_limiter_is_allowed_no_limits(self) -> None:
        """Test GlobalRateLimiter allows everything when no limits configured."""
        limiter = GlobalRateLimiter()
        limiter.configure()  # No limits

        allowed, reason = limiter.is_allowed("test.logger")
        assert allowed is True
        assert reason is None

    def test_global_rate_limiter_is_allowed_per_logger_limit(self) -> None:
        """Test GlobalRateLimiter applies per-logger limits."""
        limiter = GlobalRateLimiter()

        limiter.configure(per_logger_rates={"test.logger": (1.0, 1.0)})

        # First request should be allowed
        allowed, reason = limiter.is_allowed("test.logger")
        assert allowed is True
        assert reason is None

        # Second request should be denied
        allowed, reason = limiter.is_allowed("test.logger")
        assert allowed is False
        assert reason is not None
        assert "test.logger" in reason

    def test_global_rate_limiter_is_allowed_global_limit(self) -> None:
        """Test GlobalRateLimiter applies global limits."""
        limiter = GlobalRateLimiter()

        limiter.configure(global_rate=1.0, global_capacity=1.0)

        # First request should be allowed
        allowed, reason = limiter.is_allowed("any.logger")
        assert allowed is True
        assert reason is None

        # Second request should be denied
        allowed, reason = limiter.is_allowed("any.logger")
        assert allowed is False
        assert reason == "Global rate limit exceeded"

    def test_global_rate_limiter_is_allowed_both_limits(self) -> None:
        """Test GlobalRateLimiter applies both per-logger and global limits."""
        limiter = GlobalRateLimiter()

        limiter.configure(
            global_rate=10.0,
            global_capacity=10.0,
            per_logger_rates={"test.logger": (1.0, 1.0)},
        )

        # First request to test.logger should be allowed
        allowed, reason = limiter.is_allowed("test.logger")
        assert allowed is True

        # Second request to test.logger should be denied by per-logger limit
        allowed, reason = limiter.is_allowed("test.logger")
        assert allowed is False
        assert reason is not None
        assert "test.logger" in reason

        # Request to other logger should still be allowed (global limit not reached)
        allowed, reason = limiter.is_allowed("other.logger")
        assert allowed is True

    def test_global_rate_limiter_get_stats(self) -> None:
        """Test GlobalRateLimiter statistics."""
        limiter = GlobalRateLimiter()

        limiter.configure(
            global_rate=5.0,
            global_capacity=10.0,
            per_logger_rates={"test.logger": (2.0, 3.0)},
        )

        # Use some capacity
        limiter.is_allowed("test.logger")
        limiter.is_allowed("other.logger")

        stats = limiter.get_stats()

        assert "global" in stats
        assert "per_logger" in stats
        assert stats["global"] is not None
        assert "test.logger" in stats["per_logger"]

    def test_global_rate_limiter_reset_between_tests(self) -> None:
        """Test that we can reset GlobalRateLimiter for testing."""
        # Reset the singleton
        GlobalRateLimiter._instance = None

        limiter = GlobalRateLimiter()
        limiter.configure(global_rate=1.0, global_capacity=1.0)

        # Use up capacity
        allowed, _ = limiter.is_allowed("test")
        assert allowed is True

        allowed, _ = limiter.is_allowed("test")
        assert allowed is False


class TestRateLimiterIntegration(FoundationTestCase):
    """Integration tests for rate limiter components."""

    def test_rate_limiters_work_together(self) -> None:
        """Test that different rate limiters can work together."""
        # Create separate limiters for different purposes
        global_limiter = SyncRateLimiter(capacity=20.0, refill_rate=10.0)
        user_limiter = SyncRateLimiter(capacity=5.0, refill_rate=2.0)

        # Simulate a scenario where both global and user limits apply
        for i in range(10):
            global_allowed = global_limiter.is_allowed()
            user_allowed = user_limiter.is_allowed()

            # Both must allow for overall allowance
            overall_allowed = global_allowed and user_allowed

            if i < 5:
                assert overall_allowed is True
            else:
                # After 5 requests, user limiter should start denying
                assert overall_allowed is False

    @pytest.mark.asyncio
    async def test_sync_async_compatibility(self) -> None:
        """Test that sync and async rate limiters have compatible interfaces."""
        sync_limiter = SyncRateLimiter(capacity=5.0, refill_rate=1.0)
        async_limiter = AsyncRateLimiter(capacity=5.0, refill_rate=1.0)

        # Both should start with same state
        sync_stats = sync_limiter.get_stats()
        async_stats = await async_limiter.get_stats()

        assert sync_stats["capacity"] == async_stats["capacity"]
        assert sync_stats["refill_rate"] == async_stats["refill_rate"]
        assert sync_stats["tokens_available"] == async_stats["tokens_available"]

    def test_rate_limiter_performance_basic(self) -> None:
        """Test basic performance characteristics."""
        limiter = SyncRateLimiter(capacity=1000.0, refill_rate=500.0)

        start_time = time.time()

        # Make many requests
        allowed_count = 0
        for _ in range(1000):
            if limiter.is_allowed():
                allowed_count += 1

        end_time = time.time()
        elapsed = end_time - start_time

        # Should be fast (< 0.1 seconds for 1000 requests)
        assert elapsed < 0.1

        # Should allow all requests within capacity
        assert allowed_count == 1000

    def test_rate_limiter_memory_efficiency(self) -> None:
        """Test that rate limiters don't leak memory over time."""
        limiter = SyncRateLimiter(capacity=10.0, refill_rate=5.0)

        # Simulate long-running usage
        for _ in range(10000):
            limiter.is_allowed()

        # Statistics should still be reasonable
        stats = limiter.get_stats()
        assert stats["total_allowed"] + stats["total_denied"] == 10000

        # Token count should be bounded
        assert 0 <= stats["tokens_available"] <= stats["capacity"]


# 🧱🏗️🔚
