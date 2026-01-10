#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for Foundation queue-based rate limiting."""

from __future__ import annotations

import sys
import threading
import time

from provide.testkit import FoundationTestCase
import pytest

from provide.foundation.logger.ratelimit.queue_limiter import (
    BufferedRateLimiter,
    QueuedRateLimiter,
)


class TestBufferedRateLimiter(FoundationTestCase):
    """Test BufferedRateLimiter class."""

    def test_buffered_rate_limiter_init_valid(self) -> None:
        """Test BufferedRateLimiter initialization."""
        limiter = BufferedRateLimiter(
            capacity=10.0,
            refill_rate=2.0,
            buffer_size=50,
            track_dropped=True,
        )

        assert limiter.capacity == 10.0
        assert limiter.refill_rate == 2.0
        assert limiter.buffer_size == 50
        assert limiter.track_dropped is True
        assert limiter.dropped_buffer is not None

    def test_buffered_rate_limiter_init_invalid(self) -> None:
        """Test BufferedRateLimiter validation."""
        with pytest.raises(ValueError, match="Capacity must be positive"):
            BufferedRateLimiter(capacity=0, refill_rate=1.0)

        with pytest.raises(ValueError, match="Refill rate must be positive"):
            BufferedRateLimiter(capacity=10.0, refill_rate=-1.0)

    def test_buffered_rate_limiter_no_tracking(self) -> None:
        """Test BufferedRateLimiter without dropped item tracking."""
        limiter = BufferedRateLimiter(
            capacity=10.0,
            refill_rate=2.0,
            track_dropped=False,
        )

        assert limiter.track_dropped is False
        assert limiter.dropped_buffer is None

    def test_buffered_rate_limiter_allows_within_capacity(self) -> None:
        """Test BufferedRateLimiter allows requests within capacity."""
        limiter = BufferedRateLimiter(capacity=3.0, refill_rate=1.0)

        # First 3 should be allowed
        allowed, reason = limiter.is_allowed()
        assert allowed is True
        assert reason is None

        allowed, reason = limiter.is_allowed()
        assert allowed is True
        assert reason is None

        allowed, reason = limiter.is_allowed()
        assert allowed is True
        assert reason is None

        # Fourth should be denied
        allowed, reason = limiter.is_allowed()
        assert allowed is False
        assert reason is not None
        assert "Rate limit exceeded" in reason

    def test_buffered_rate_limiter_refill_tokens(self) -> None:
        """Test token refilling over time."""
        limiter = BufferedRateLimiter(capacity=2.0, refill_rate=10.0)

        # Exhaust tokens
        limiter.is_allowed()
        limiter.is_allowed()
        allowed, _ = limiter.is_allowed()
        assert allowed is False

        # Wait for refill
        time.sleep(0.15)  # 1.5 tokens

        allowed, _ = limiter.is_allowed()
        assert allowed is True

        allowed, _ = limiter.is_allowed()  # Should still be denied
        assert allowed is False

    def test_buffered_rate_limiter_tracks_dropped_items(self) -> None:
        """Test tracking of dropped items."""
        limiter = BufferedRateLimiter(
            capacity=1.0,
            refill_rate=1.0,
            track_dropped=True,
        )

        # Allow one
        allowed, _ = limiter.is_allowed("item1")
        assert allowed is True

        # Deny the rest
        allowed, _ = limiter.is_allowed("item2")
        assert allowed is False

        allowed, _ = limiter.is_allowed("item3")
        assert allowed is False

        # Check dropped samples
        dropped = limiter.get_dropped_samples()
        assert len(dropped) == 2
        assert dropped[0]["item"] == "item2"
        assert dropped[1]["item"] == "item3"

    def test_buffered_rate_limiter_dropped_samples_limit(self) -> None:
        """Test dropped samples buffer limit."""
        limiter = BufferedRateLimiter(
            capacity=0.01,
            refill_rate=1.0,
            buffer_size=3,
            track_dropped=True,
        )

        # Add many dropped items
        for i in range(10):
            limiter.is_allowed(f"item_{i}")

        # Should only keep last 3
        dropped = limiter.get_dropped_samples()
        assert len(dropped) <= 3

    def test_buffered_rate_limiter_get_dropped_samples_count(self) -> None:
        """Test getting limited number of dropped samples."""
        limiter = BufferedRateLimiter(
            capacity=0.01,
            refill_rate=1.0,
            track_dropped=True,
        )

        # Add several dropped items
        for i in range(5):
            limiter.is_allowed(f"item_{i}")

        # Get limited samples
        dropped = limiter.get_dropped_samples(count=2)
        assert len(dropped) <= 2

    def test_buffered_rate_limiter_get_dropped_no_tracking(self) -> None:
        """Test getting dropped samples when tracking is disabled."""
        limiter = BufferedRateLimiter(
            capacity=0.01,
            refill_rate=1.0,
            track_dropped=False,
        )

        # Try to drop some items
        limiter.is_allowed("item1")
        limiter.is_allowed("item2")

        # Should return empty list
        dropped = limiter.get_dropped_samples()
        assert dropped == []

    def test_buffered_rate_limiter_statistics(self) -> None:
        """Test statistics collection."""
        limiter = BufferedRateLimiter(
            capacity=5.0,
            refill_rate=2.0,
            track_dropped=True,
        )

        # Allow some, deny some
        limiter.is_allowed("allowed1")
        limiter.is_allowed("allowed2")
        limiter.is_allowed("denied1")  # This will be denied due to capacity

        stats = limiter.get_stats()

        assert stats["capacity"] == 5.0
        assert stats["refill_rate"] == 2.0
        assert stats["total_allowed"] >= 2
        assert stats["total_denied"] >= 0
        assert "tokens_available" in stats
        assert "total_bytes_dropped" in stats

    def test_buffered_rate_limiter_statistics_with_dropped_buffer(self) -> None:
        """Test statistics when tracking dropped items."""
        limiter = BufferedRateLimiter(
            capacity=1.0,
            refill_rate=1.0,
            track_dropped=True,
        )

        # Fill capacity then add more
        limiter.is_allowed("allowed")
        limiter.is_allowed("denied1")
        time.sleep(0.01)  # Small gap for age calculation
        limiter.is_allowed("denied2")

        stats = limiter.get_stats()

        assert "dropped_buffer_size" in stats
        assert "oldest_dropped_age" in stats
        assert stats["dropped_buffer_size"] > 0
        assert stats["oldest_dropped_age"] >= 0

    def test_buffered_rate_limiter_thread_safety(self) -> None:
        """Test thread safety of BufferedRateLimiter."""
        limiter = BufferedRateLimiter(capacity=100.0, refill_rate=50.0)
        results = []

        def worker() -> None:
            for i in range(20):
                allowed, _ = limiter.is_allowed(f"item_{threading.current_thread().ident}_{i}")
                results.append(allowed)

        threads = [threading.Thread(daemon=True, target=worker) for _ in range(5)]

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join(timeout=10.0)

        # Some should be allowed, some denied
        allowed_count = sum(results)
        denied_count = len(results) - allowed_count

        assert allowed_count > 0
        assert allowed_count <= 100  # Within capacity

        stats = limiter.get_stats()
        assert stats["total_allowed"] == allowed_count
        assert stats["total_denied"] == denied_count


class TestQueueLimiterIntegration(FoundationTestCase):
    """Integration tests for queue-based rate limiters."""

    def test_different_queue_limiters_similar_behavior(self, ensure_limiter_cleanup: any) -> None:
        """Test that different queue limiters have similar core behavior."""
        buffered = BufferedRateLimiter(capacity=5.0, refill_rate=2.0)
        queued = ensure_limiter_cleanup(QueuedRateLimiter(capacity=5.0, refill_rate=2.0, max_queue_size=10))
        queued.start()

        # Both should start similarly
        b_allowed, _ = buffered.is_allowed()
        q_accepted, _ = queued.enqueue("test")

        assert b_allowed is True
        assert q_accepted is True

        # Both should track statistics
        b_stats = buffered.get_stats()
        q_stats = queued.get_stats()

        assert b_stats["capacity"] == q_stats["capacity"]
        assert b_stats["refill_rate"] == q_stats["refill_rate"]

        queued.stop()

    def test_memory_tracking_consistency(self) -> None:
        """Test that memory tracking works consistently."""
        limiter = BufferedRateLimiter(capacity=0.01, refill_rate=1.0, track_dropped=True)

        test_item = "x" * 100
        expected_size = sys.getsizeof(test_item)

        # Should be denied and tracked
        allowed, _ = limiter.is_allowed(test_item)
        assert allowed is False

        stats = limiter.get_stats()
        assert stats["total_bytes_dropped"] == expected_size

        dropped = limiter.get_dropped_samples()
        assert len(dropped) == 1
        assert dropped[0]["size"] == expected_size

    def test_queue_limiter_performance(self) -> None:
        """Test performance characteristics of queue limiters."""
        limiter = BufferedRateLimiter(capacity=1000.0, refill_rate=500.0)

        start_time = time.time()

        # Make many requests quickly
        allowed_count = 0
        for i in range(1000):
            allowed, _ = limiter.is_allowed(f"item_{i}")
            if allowed:
                allowed_count += 1

        end_time = time.time()
        elapsed = end_time - start_time

        # Should be reasonably fast
        assert elapsed < 0.5
        assert allowed_count > 0

    def test_edge_case_zero_capacity(self) -> None:
        """Test edge case with zero capacity."""
        limiter = BufferedRateLimiter(capacity=0.01, refill_rate=1.0)  # Very small capacity

        # First request might be allowed due to initial fractional token
        _allowed, _ = limiter.is_allowed()

        # Subsequent requests should definitely be denied
        allowed2, reason = limiter.is_allowed()
        assert allowed2 is False
        assert reason is not None

    def test_edge_case_very_high_rates(self) -> None:
        """Test edge case with very high refill rates."""
        limiter = BufferedRateLimiter(capacity=1000.0, refill_rate=10000.0)

        # Should handle high rates without issues
        for _ in range(100):
            allowed, _ = limiter.is_allowed()
            assert allowed is True  # High refill rate should keep allowing


# 🧱🏗️🔚
