#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for Foundation queue-based rate limiting."""

from __future__ import annotations

import sys
import time

from provide.testkit import FoundationTestCase
import pytest

from provide.foundation.logger.ratelimit.queue_limiter import (
    QueuedRateLimiter,
)


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
        # Thread should not auto-start
        assert limiter.running is False
        assert limiter.worker_thread is None

        # Start explicitly
        limiter.start()
        assert limiter.running is True
        assert limiter.worker_thread.is_alive()

        # Clean up
        limiter.stop()

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
        limiter.start()

        # Enqueue some items
        for i in range(5):
            accepted, _reason = limiter.enqueue(f"item_{i}")
            assert accepted is True
            assert _reason is None

        stats = limiter.get_stats()
        assert stats["queue_size"] == 5
        assert stats["total_queued"] == 5

        limiter.stop()

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
        limiter.start()

        # Try to add items that clearly exceed memory limit
        # 10KB item vs 512 byte limit = clear failure
        large_item = "x" * 10000  # ~10KB item

        accepted, reason = limiter.enqueue(large_item)
        assert accepted is False
        assert "Memory limit exceeded" in reason

        stats = limiter.get_stats()
        assert stats["total_dropped"] == 1

        limiter.stop()

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
        limiter.start()

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

        limiter.stop()

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
        limiter.start()

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

        limiter.stop()

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
        limiter.start()

        # Fill queue
        accepted, reason = limiter.enqueue("item_1")
        assert accepted is True

        # Try to add another - should be blocked (rejected for now)
        accepted, reason = limiter.enqueue("item_2")
        assert accepted is False
        assert "blocking not implemented" in reason

        limiter.stop()

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
        limiter.start()

        # Enqueue items
        for i in range(5):
            limiter.enqueue(f"item_{i}")

        # Wait for processing
        time.sleep(0.3)

        # Some items should have been processed
        assert len(processed_items) > 0

        stats = limiter.get_stats()
        assert stats["total_processed"] > 0

        limiter.stop()

    def test_queued_rate_limiter_estimate_size(self, ensure_limiter_cleanup: any) -> None:
        """Test memory size estimation."""
        limiter = ensure_limiter_cleanup(QueuedRateLimiter(capacity=10.0, refill_rate=1.0))
        limiter.start()

        # Test size estimation
        small_item = "test"
        large_item = "x" * 1000

        small_size = limiter._estimate_size(small_item)
        large_size = limiter._estimate_size(large_item)

        assert large_size > small_size
        assert small_size == sys.getsizeof(small_item)
        assert large_size == sys.getsizeof(large_item)

        limiter.stop()

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
        limiter.start()

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

        limiter.stop()

    def test_queued_rate_limiter_shutdown(self, ensure_limiter_cleanup: any) -> None:
        """Test proper shutdown."""
        limiter = ensure_limiter_cleanup(QueuedRateLimiter(capacity=10.0, refill_rate=1.0))

        # Initially not running
        assert limiter.running is False
        assert limiter.worker_thread is None

        # Start it
        limiter.start()
        assert limiter.running is True
        assert limiter.worker_thread.is_alive()

        # Shutdown
        limiter.stop()

        # Give it time to shut down
        time.sleep(0.1)

        assert limiter.running is False
        assert not limiter.worker_thread.is_alive()


# 🧱🏗️🔚
