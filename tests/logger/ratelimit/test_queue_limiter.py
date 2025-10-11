"""Tests for Foundation queue-based rate limiting."""

from __future__ import annotations

from contextlib import suppress
import sys
import threading
import time

from provide.testkit import FoundationTestCase
import pytest

from provide.foundation.logger.ratelimit.queue_limiter import (
    BufferedRateLimiter,
    QueuedRateLimiter,
)


@pytest.fixture
def ensure_limiter_cleanup() -> any:
    """Ensure all QueuedRateLimiter instances are properly shut down after each test."""
    created_limiters = []

    def track_limiter(limiter: QueuedRateLimiter) -> QueuedRateLimiter:
        created_limiters.append(limiter)
        return limiter

    yield track_limiter

    # Cleanup: shutdown any remaining limiters
    for limiter in created_limiters:
        if hasattr(limiter, "running") and limiter.running:
            with suppress(Exception):
                limiter.shutdown()


class TestQueuedRateLimiter(FoundationTestCase):
    """Test QueuedRateLimiter class."""

    def test_queued_rate_limiter_init_valid(self, ensure_limiter_cleanup: any) -> None:
        """Test QueuedRateLimiter initialization with valid parameters."""
        limiter = ensure_limiter_cleanup(
            QueuedRateLimiter(
                capacity=10.0,
                refill_rate=2.0,
                max_queue_size=100,
                max_memory_mb=1.0,
                overflow_policy="drop_oldest",
            )
        )

        assert limiter.capacity == 10.0
        assert limiter.refill_rate == 2.0
        assert limiter.max_queue_size == 100
        assert limiter.max_memory_bytes == 1024 * 1024
        assert limiter.overflow_policy == "drop_oldest"
        assert limiter.running is True
        assert limiter.worker_thread.is_alive()

        # Clean up
        limiter.shutdown()

    def test_queued_rate_limiter_init_invalid_capacity(self) -> None:
        """Test QueuedRateLimiter raises error for invalid capacity."""
        with pytest.raises(ValueError, match="Capacity must be positive"):
            QueuedRateLimiter(capacity=0, refill_rate=1.0)

        with pytest.raises(ValueError, match="Capacity must be positive"):
            QueuedRateLimiter(capacity=-1.0, refill_rate=1.0)

    def test_queued_rate_limiter_init_invalid_refill_rate(self) -> None:
        """Test QueuedRateLimiter raises error for invalid refill rate."""
        with pytest.raises(ValueError, match="Refill rate must be positive"):
            QueuedRateLimiter(capacity=10.0, refill_rate=0)

        with pytest.raises(ValueError, match="Refill rate must be positive"):
            QueuedRateLimiter(capacity=10.0, refill_rate=-1.0)

    def test_queued_rate_limiter_init_invalid_queue_size(self) -> None:
        """Test QueuedRateLimiter raises error for invalid queue size."""
        with pytest.raises(ValueError, match="Max queue size must be positive"):
            QueuedRateLimiter(capacity=10.0, refill_rate=1.0, max_queue_size=0)

        with pytest.raises(ValueError, match="Max queue size must be positive"):
            QueuedRateLimiter(capacity=10.0, refill_rate=1.0, max_queue_size=-1)

    def test_queued_rate_limiter_enqueue_basic(self, ensure_limiter_cleanup: any) -> None:
        """Test basic enqueueing functionality."""
        limiter = ensure_limiter_cleanup(
            QueuedRateLimiter(
                capacity=10.0,
                refill_rate=5.0,
                max_queue_size=10,
            )
        )

        # Enqueue some items
        for i in range(5):
            accepted, _reason = limiter.enqueue(f"item_{i}")
            assert accepted is True
            assert _reason is None

        stats = limiter.get_stats()
        assert stats["queue_size"] == 5
        assert stats["total_queued"] == 5

        limiter.shutdown()

    def test_queued_rate_limiter_memory_limit(self, ensure_limiter_cleanup: any) -> None:
        """Test memory limit enforcement."""
        # Very small memory limit (0.0005 MB = ~512 bytes)
        limiter = ensure_limiter_cleanup(
            QueuedRateLimiter(
                capacity=10.0,
                refill_rate=5.0,
                max_queue_size=100,
                max_memory_mb=0.0005,
            )
        )

        # Try to add items that clearly exceed memory limit
        # 10KB item vs 512 byte limit = clear failure
        large_item = "x" * 10000  # ~10KB item

        accepted, reason = limiter.enqueue(large_item)
        assert accepted is False
        assert "Memory limit exceeded" in reason

        stats = limiter.get_stats()
        assert stats["total_dropped"] == 1

        limiter.shutdown()

    def test_queued_rate_limiter_drop_oldest_policy(self, ensure_limiter_cleanup: any) -> None:
        """Test drop_oldest overflow policy."""
        limiter = ensure_limiter_cleanup(
            QueuedRateLimiter(
                capacity=10.0,
                refill_rate=0.1,
                max_queue_size=3,
                overflow_policy="drop_oldest",
            )
        )

        # Fill queue to capacity
        for i in range(3):
            accepted, _reason = limiter.enqueue(f"item_{i}")
            assert accepted is True

        # Add one more item - should drop oldest
        accepted, _reason = limiter.enqueue("item_new")
        assert accepted is True

        stats = limiter.get_stats()
        assert stats["queue_size"] == 3  # Still at max
        assert stats["total_dropped"] == 1  # One item dropped

        limiter.shutdown()

    def test_queued_rate_limiter_drop_newest_policy(self, ensure_limiter_cleanup: any) -> None:
        """Test drop_newest overflow policy."""
        limiter = ensure_limiter_cleanup(
            QueuedRateLimiter(
                capacity=10.0,
                refill_rate=0.1,
                max_queue_size=2,
                overflow_policy="drop_newest",
            )
        )

        # Fill queue to capacity
        for i in range(2):
            accepted, _reason = limiter.enqueue(f"item_{i}")
            assert accepted is True

        # Try to add one more - should be rejected
        accepted, reason = limiter.enqueue("item_rejected")
        assert accepted is False
        assert "Queue full" in reason

        stats = limiter.get_stats()
        assert stats["queue_size"] == 2
        assert stats["total_dropped"] == 1

        limiter.shutdown()

    def test_queued_rate_limiter_block_policy(self, ensure_limiter_cleanup: any) -> None:
        """Test block overflow policy."""
        limiter = ensure_limiter_cleanup(
            QueuedRateLimiter(
                capacity=10.0,
                refill_rate=0.1,
                max_queue_size=1,
                overflow_policy="block",
            )
        )

        # Fill queue
        accepted, reason = limiter.enqueue("item_1")
        assert accepted is True

        # Try to add another - should be blocked (rejected for now)
        accepted, reason = limiter.enqueue("item_2")
        assert accepted is False
        assert "blocking not implemented" in reason

        limiter.shutdown()

    def test_queued_rate_limiter_processing(self, ensure_limiter_cleanup: any) -> None:
        """Test that queued items are processed over time."""
        processed_items = []

        class TestQueuedRateLimiter(QueuedRateLimiter):
            def _process_item(self, item: any) -> None:
                processed_items.append(item)

        limiter = ensure_limiter_cleanup(
            TestQueuedRateLimiter(
                capacity=2.0,
                refill_rate=10.0,
                max_queue_size=10,
            )
        )

        # Enqueue items
        for i in range(5):
            limiter.enqueue(f"item_{i}")

        # Wait for processing
        time.sleep(0.3)

        # Some items should have been processed
        assert len(processed_items) > 0

        stats = limiter.get_stats()
        assert stats["total_processed"] > 0

        limiter.shutdown()

    def test_queued_rate_limiter_estimate_size(self, ensure_limiter_cleanup: any) -> None:
        """Test memory size estimation."""
        limiter = ensure_limiter_cleanup(QueuedRateLimiter(capacity=10.0, refill_rate=1.0))

        # Test size estimation
        small_item = "test"
        large_item = "x" * 1000

        small_size = limiter._estimate_size(small_item)
        large_size = limiter._estimate_size(large_item)

        assert large_size > small_size
        assert small_size == sys.getsizeof(small_item)
        assert large_size == sys.getsizeof(large_item)

        limiter.shutdown()

    def test_queued_rate_limiter_get_stats(self, ensure_limiter_cleanup: any) -> None:
        """Test statistics collection."""
        limiter = ensure_limiter_cleanup(
            QueuedRateLimiter(
                capacity=5.0,
                refill_rate=2.0,
                max_queue_size=10,
                max_memory_mb=1.0,
            )
        )

        stats = limiter.get_stats()

        # Check all expected fields are present
        expected_fields = {
            "queue_size",
            "max_queue_size",
            "tokens_available",
            "capacity",
            "refill_rate",
            "total_queued",
            "total_dropped",
            "total_processed",
            "estimated_memory_mb",
            "max_memory_mb",
            "overflow_policy",
        }

        for field in expected_fields:
            assert field in stats

        assert stats["capacity"] == 5.0
        assert stats["refill_rate"] == 2.0
        assert stats["max_queue_size"] == 10
        assert stats["overflow_policy"] == "drop_oldest"

        limiter.shutdown()

    def test_queued_rate_limiter_shutdown(self, ensure_limiter_cleanup: any) -> None:
        """Test proper shutdown."""
        limiter = ensure_limiter_cleanup(QueuedRateLimiter(capacity=10.0, refill_rate=1.0))

        assert limiter.running is True
        assert limiter.worker_thread.is_alive()

        limiter.shutdown()

        # Give it time to shut down
        time.sleep(0.1)

        assert limiter.running is False
        assert not limiter.worker_thread.is_alive()


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

        queued.shutdown()

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
