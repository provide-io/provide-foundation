#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for Foundation rate limiting processor."""

from __future__ import annotations

from contextlib import suppress
import time

from provide.testkit import FoundationTestCase
from provide.testkit.mocking import MagicMock, Mock, patch
import pytest
import structlog

from provide.foundation.logger.ratelimit.limiters import GlobalRateLimiter
from provide.foundation.logger.ratelimit.processor import (
    RateLimiterProcessor,
    create_rate_limiter_processor,
)


class TestCreateRateLimiterProcessor(FoundationTestCase):
    """Test create_rate_limiter_processor factory function."""

    def setup_method(self) -> None:
        """Reset GlobalRateLimiter singleton before each test."""
        super().setup_method()
        GlobalRateLimiter._instance = None

    def test_create_rate_limiter_processor_basic(self) -> None:
        """Test basic processor creation."""
        processor = create_rate_limiter_processor()

        assert isinstance(processor, RateLimiterProcessor)
        assert processor.emit_warning_on_limit is True
        assert processor.summary_interval == 5.0

    def test_create_rate_limiter_processor_with_global_limits(self) -> None:
        """Test processor creation with global rate limits."""
        processor = create_rate_limiter_processor(
            global_rate=10.0,
            global_capacity=20.0,
        )

        assert processor.rate_limiter.global_rate == 10.0
        assert processor.rate_limiter.global_capacity == 20.0

    def test_create_rate_limiter_processor_with_per_logger_limits(self) -> None:
        """Test processor creation with per-logger limits."""
        # Reset singleton for this test
        from provide.foundation.logger.ratelimit.limiters import GlobalRateLimiter

        GlobalRateLimiter._instance = None

        per_logger_rates = {
            "app.module1": (5.0, 10.0),
            "app.module2": (2.0, 5.0),
        }

        processor = create_rate_limiter_processor(per_logger_rates=per_logger_rates)

        assert len(processor.rate_limiter.logger_limiters) == 2
        assert "app.module1" in processor.rate_limiter.logger_limiters
        assert "app.module2" in processor.rate_limiter.logger_limiters

    def test_create_rate_limiter_processor_with_buffered_config(self) -> None:
        """Test processor creation with buffered rate limiting."""
        processor = create_rate_limiter_processor(
            global_rate=5.0,
            global_capacity=10.0,
            max_queue_size=100,
            overflow_policy="drop_oldest",
        )

        assert processor.rate_limiter.use_buffered is True
        assert processor.rate_limiter.max_queue_size == 100
        assert processor.rate_limiter.overflow_policy == "drop_oldest"

    def test_create_rate_limiter_processor_no_buffering(self) -> None:
        """Test processor creation without buffering."""
        processor = create_rate_limiter_processor(
            global_rate=5.0,
            global_capacity=10.0,
            max_queue_size=0,  # Disables buffering
        )

        assert processor.rate_limiter.use_buffered is False

    def test_create_rate_limiter_processor_custom_intervals(self) -> None:
        """Test processor creation with custom intervals."""
        processor = create_rate_limiter_processor(
            emit_warnings=False,
            summary_interval=15.0,
        )

        assert processor.emit_warning_on_limit is False
        assert processor.summary_interval == 15.0

    def test_create_rate_limiter_processor_memory_limits(self) -> None:
        """Test processor creation with memory limits."""
        processor = create_rate_limiter_processor(
            global_rate=5.0,
            global_capacity=10.0,
            max_queue_size=50,
            max_memory_mb=2.0,
            overflow_policy="drop_newest",
        )

        assert processor.rate_limiter.use_buffered is True
        assert processor.rate_limiter.max_memory_mb == 2.0
        assert processor.rate_limiter.overflow_policy == "drop_newest"

    def test_create_rate_limiter_processor_invalid_overflow_policy(self) -> None:
        """Test processor creation with invalid overflow policy doesn't enable buffering."""
        processor = create_rate_limiter_processor(
            global_rate=5.0,
            global_capacity=10.0,
            max_queue_size=50,
            overflow_policy="invalid_policy",
        )

        # Should not enable buffering with invalid policy
        assert processor.rate_limiter.use_buffered is False


class TestRateLimiterProcessorIntegration(FoundationTestCase):
    """Integration tests for rate limiter processor."""

    def setup_method(self) -> None:
        """Reset GlobalRateLimiter singleton before each test."""
        super().setup_method()
        GlobalRateLimiter._instance = None

    @patch("provide.foundation.logger.get_logger")
    def test_processor_with_structlog_pipeline(self, mock_get_logger: Mock) -> None:
        """Test processor works in structlog pipeline."""
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger

        # Reset singleton
        from provide.foundation.logger.ratelimit.limiters import GlobalRateLimiter

        GlobalRateLimiter._instance = None

        # Create a processor with restrictive limits
        processor = create_rate_limiter_processor(
            per_logger_rates={"test.app": (0.01, 1.0)},  # Very slow refill
            emit_warnings=False,
        )

        # Configure a simple structlog logger with capturing
        structlog.configure(
            processors=[processor],
            wrapper_class=structlog.make_filtering_bound_logger(20),  # INFO level
            logger_factory=structlog.testing.CapturingLoggerFactory(),
            cache_logger_on_first_use=True,
        )

        logger = structlog.get_logger("test.app")

        # First message should work
        logger.info("First message")

        # Small delay to ensure token consumption
        time.sleep(0.01)

        # Second message should be rate limited and not appear
        with suppress(Exception):
            logger.info("Second message")

        # Test passed if no unhandled exceptions occurred

    def test_processor_performance_impact(self) -> None:
        """Test processor has minimal performance impact."""
        processor = create_rate_limiter_processor()

        event_dict = {
            "event": "test message",
            "level": "info",
            "logger_name": "test.logger",
        }

        start_time = time.time()

        # Process many events
        for _i in range(1000):
            with suppress(structlog.DropEvent):
                processor(None, "info", event_dict.copy())

        end_time = time.time()
        elapsed = end_time - start_time

        # Should be reasonably fast (< 0.5 seconds for 1000 events)
        assert elapsed < 0.5

    @patch("provide.foundation.logger.get_logger")
    def test_processor_multiple_logger_names(self, mock_get_logger: Mock) -> None:
        """Test processor handles multiple logger names correctly."""
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger

        # Reset singleton
        from provide.foundation.logger.ratelimit.limiters import GlobalRateLimiter

        GlobalRateLimiter._instance = None

        processor = create_rate_limiter_processor(
            per_logger_rates={
                "app.fast": (100.0, 200.0),  # High limits
                "app.slow": (0.01, 1.0),  # Very slow refill - 1 message then wait
            },
            summary_interval=100.0,
            emit_warnings=False,  # Disable warnings to get DropEvent
        )

        fast_event = {"event": "fast", "level": "info", "logger_name": "app.fast"}
        slow_event = {"event": "slow", "level": "info", "logger_name": "app.slow"}

        # Fast logger should handle many requests
        for _ in range(10):
            result = processor(None, "info", fast_event.copy())
            assert result == fast_event

        # Slow logger should be limited after first request
        processor(None, "info", slow_event.copy())  # Consumes the 0.1 capacity

        # Small delay to ensure token is fully consumed
        time.sleep(0.01)

        with pytest.raises(structlog.DropEvent):
            processor(None, "info", slow_event.copy())  # Second denied

    def test_processor_edge_cases(self) -> None:
        """Test processor handles edge cases."""
        processor = create_rate_limiter_processor()

        # Empty event dict
        result = processor(None, "info", {})
        assert result == {}

        # Event dict with None values
        event = {"event": None, "logger_name": None}
        result = processor(None, "info", event)
        assert result == event

        # Very long event message
        long_event = {
            "event": "x" * 10000,
            "logger_name": "test",
        }
        result = processor(None, "info", long_event)
        assert result == long_event

    def test_processor_statistics_integration(self) -> None:
        """Test processor statistics are properly integrated."""
        processor = create_rate_limiter_processor(
            per_logger_rates={"test.logger": (1.0, 2.0)},
        )

        event_dict = {
            "event": "test message",
            "level": "info",
            "logger_name": "test.logger",
        }

        # Process some events
        processor(None, "info", event_dict.copy())  # Allowed
        processor(None, "info", event_dict.copy())  # Allowed

        with suppress(structlog.DropEvent):
            processor(None, "info", event_dict.copy())  # Should be denied

        # Check statistics
        stats = processor.rate_limiter.get_stats()
        per_logger_stats = stats["per_logger"]["test.logger"]

        assert per_logger_stats["total_allowed"] == 2
        assert per_logger_stats["total_denied"] == 1


# 🧱🏗️🔚
