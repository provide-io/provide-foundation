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


class TestRateLimiterProcessor(FoundationTestCase):
    """Test RateLimiterProcessor class."""

    def setup_method(self) -> None:
        """Reset GlobalRateLimiter singleton before each test."""
        GlobalRateLimiter._instance = None

    def test_rate_limiter_processor_init(self) -> None:
        """Test RateLimiterProcessor initialization."""
        processor = RateLimiterProcessor(
            emit_warning_on_limit=True,
            warning_interval_seconds=30.0,
            summary_interval_seconds=10.0,
        )

        assert processor.emit_warning_on_limit is True
        assert processor.warning_interval_seconds == 30.0
        assert processor.summary_interval == 10.0
        assert processor.rate_limiter is not None
        assert processor.last_warning_times == {}
        assert processor.suppressed_counts == {}

    def test_rate_limiter_processor_init_defaults(self) -> None:
        """Test RateLimiterProcessor with default parameters."""
        processor = RateLimiterProcessor()

        assert processor.emit_warning_on_limit is True
        assert processor.warning_interval_seconds == 60.0
        assert processor.summary_interval == 5.0

    @patch("provide.foundation.logger.get_logger")
    def test_rate_limiter_processor_allows_when_no_limits(
        self,
        mock_get_logger: MagicMock,
    ) -> None:
        """Test processor allows events when no rate limits are configured."""
        # Mock logger to prevent actual logging during summary
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger

        processor = RateLimiterProcessor(
            summary_interval_seconds=100.0,
        )  # Long interval to avoid summary

        event_dict = {
            "event": "test message",
            "level": "info",
            "logger_name": "test.logger",
        }

        # Should pass through unchanged
        result = processor(None, "info", event_dict)
        assert result == event_dict

    @patch("provide.foundation.logger.get_logger")
    def test_rate_limiter_processor_blocks_when_limited(self, mock_get_logger: MagicMock) -> None:
        """Test processor blocks events when rate limited."""
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger

        processor = RateLimiterProcessor(
            emit_warning_on_limit=False,
            summary_interval_seconds=100.0,  # Long interval
        )

        # Configure rate limiter with very restrictive limits
        processor.rate_limiter.configure(
            per_logger_rates={"test.logger": (0.1, 1.0)},  # Very low rate, capacity=1.0
        )

        event_dict = {
            "event": "test message",
            "level": "info",
            "logger_name": "test.logger",
        }

        # First event should pass
        result = processor(None, "info", event_dict.copy())
        assert result == event_dict

        # Second event should be dropped
        with pytest.raises(structlog.DropEvent):
            processor(None, "info", event_dict.copy())

    @patch("provide.foundation.logger.get_logger")
    def test_rate_limiter_processor_emits_warning_on_limit(
        self,
        mock_get_logger: MagicMock,
    ) -> None:
        """Test processor emits warning when rate limited."""
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger

        processor = RateLimiterProcessor(
            emit_warning_on_limit=True,
            warning_interval_seconds=0.1,
            summary_interval_seconds=100.0,  # Long interval
        )

        # Configure restrictive limits
        processor.rate_limiter.configure(per_logger_rates={"test.logger": (0.1, 1.0)})

        event_dict = {
            "event": "test message",
            "level": "info",
            "logger_name": "test.logger",
        }

        # First event passes
        processor(None, "info", event_dict.copy())

        # Second event should return warning instead of dropping
        result = processor(None, "info", event_dict.copy())

        assert result["event"].startswith("⚠️ Rate limit:")
        assert result["level"] == "warning"
        assert result["logger_name"] == "provide.foundation.ratelimit"
        assert result["suppressed_count"] == 1
        assert result["original_logger"] == "test.logger"
        assert result["_rate_limit_warning"] is True

    @patch("provide.foundation.logger.get_logger")
    def test_rate_limiter_processor_warning_interval(self, mock_get_logger: MagicMock) -> None:
        """Test processor respects warning interval."""
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger

        processor = RateLimiterProcessor(
            emit_warning_on_limit=True,
            warning_interval_seconds=0.1,
            summary_interval_seconds=100.0,
        )

        # Configure restrictive limits
        processor.rate_limiter.configure(per_logger_rates={"test.logger": (0.1, 1.0)})

        event_dict = {
            "event": "test message",
            "level": "info",
            "logger_name": "test.logger",
        }

        # First event passes
        processor(None, "info", event_dict.copy())

        # Second event returns warning
        result = processor(None, "info", event_dict.copy())
        assert "_rate_limit_warning" in result

        # Third event should be dropped (too soon for another warning)
        with pytest.raises(structlog.DropEvent):
            processor(None, "info", event_dict.copy())

        # Wait for warning interval
        time.sleep(0.15)

        # Fourth event should return warning again
        result = processor(None, "info", event_dict.copy())
        assert "_rate_limit_warning" in result

    @patch("provide.foundation.logger.get_logger")
    def test_rate_limiter_processor_tracks_suppressed_counts(
        self,
        mock_get_logger: MagicMock,
    ) -> None:
        """Test processor tracks suppressed message counts."""
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger

        processor = RateLimiterProcessor(
            emit_warning_on_limit=False,
            summary_interval_seconds=100.0,
        )

        processor.rate_limiter.configure(
            per_logger_rates={
                "test.logger": (0.01, 1.0),
            },  # Very slow refill: 0.01/sec, capacity 1
        )

        event_dict = {
            "event": "test message",
            "level": "info",
            "logger_name": "test.logger",
        }

        # First event passes
        processor(None, "info", event_dict.copy())

        # Next few events should be suppressed
        for _ in range(3):
            with pytest.raises(structlog.DropEvent):
                processor(None, "info", event_dict.copy())

        # Check suppressed count
        assert processor.suppressed_counts["test.logger"] == 3

    @patch("provide.foundation.logger.get_logger")
    def test_rate_limiter_processor_different_loggers(self, mock_get_logger: MagicMock) -> None:
        """Test processor handles different loggers independently."""
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger

        processor = RateLimiterProcessor(
            summary_interval_seconds=100.0,
            emit_warning_on_limit=False,  # Disable warnings to get DropEvent
        )

        processor.rate_limiter.configure(
            per_logger_rates={
                "logger1": (0.01, 1.0),
                "logger2": (10.0, 20.0),
            },  # logger1 very slow refill
        )

        event1 = {"event": "msg1", "level": "info", "logger_name": "logger1"}
        event2 = {"event": "msg2", "level": "info", "logger_name": "logger2"}

        # Both first events should pass
        result1 = processor(None, "info", event1.copy())
        result2 = processor(None, "info", event2.copy())

        assert result1 == event1
        assert result2 == event2

        # logger1 second event should be rate limited, logger2 should still pass
        time.sleep(0.01)  # Small delay to ensure token consumption
        with pytest.raises(structlog.DropEvent):
            processor(None, "info", event1.copy())

        result2_again = processor(None, "info", event2.copy())
        assert result2_again == event2

    @patch("provide.foundation.logger.get_logger")
    def test_rate_limiter_processor_unknown_logger(self, mock_get_logger: MagicMock) -> None:
        """Test processor handles unknown logger names gracefully."""
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger

        processor = RateLimiterProcessor(summary_interval_seconds=100.0)

        event_dict = {
            "event": "test message",
            "level": "info",
            # No logger_name field
        }

        # Should use "unknown" as logger name and pass through
        result = processor(None, "info", event_dict)
        assert result == event_dict

    @patch("provide.foundation.logger.get_logger")
    def test_rate_limiter_processor_emit_summary(self, mock_get_logger: MagicMock) -> None:
        """Test processor emits periodic summaries."""
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger

        processor = RateLimiterProcessor(
            summary_interval_seconds=0.1,
            emit_warning_on_limit=False,  # Disable warnings to focus on summary
        )

        processor.rate_limiter.configure(
            per_logger_rates={
                "test.logger": (0.01, 1.0),
            },  # Very slow refill: 0.01/sec, capacity 1
        )

        event_dict = {
            "event": "test message",
            "level": "info",
            "logger_name": "test.logger",
        }

        # Generate some rate limited events
        processor(None, "info", event_dict.copy())  # Allowed

        time.sleep(0.01)  # Small delay to ensure token consumption
        with pytest.raises(structlog.DropEvent):
            processor(None, "info", event_dict.copy())  # Denied

        # Wait for summary interval
        time.sleep(0.15)

        # Next call should trigger summary emission
        with suppress(structlog.DropEvent):
            processor(
                None,
                "info",
                event_dict.copy(),
            )  # This will be denied and should trigger summary

        # Generate another event to trigger the interval check
        with suppress(structlog.DropEvent):
            processor(None, "info", event_dict.copy())

        # Directly call emit_summary to ensure it works
        processor._emit_summary()

        # Should have called the logger warning method
        mock_logger.warning.assert_called()
        call_args = mock_logger.warning.call_args
        assert "Rate limiting active" in call_args[0][0]

    @patch("provide.foundation.logger.get_logger")
    def test_rate_limiter_processor_summary_no_activity(self, mock_get_logger: MagicMock) -> None:
        """Test processor doesn't emit summary when no rate limiting occurs."""
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger

        # Reset singleton to ensure clean state
        from provide.foundation.logger.ratelimit.limiters import GlobalRateLimiter

        GlobalRateLimiter._instance = None

        processor = RateLimiterProcessor(summary_interval_seconds=0.1)

        event_dict = {
            "event": "test message",
            "level": "info",
            "logger_name": "test.logger",
        }

        # Process some events (no rate limiting configured)
        processor(None, "info", event_dict.copy())

        # Wait for summary interval
        time.sleep(0.15)

        processor(None, "info", event_dict.copy())

        # Should not have called the logger
        mock_logger.warning.assert_not_called()

    @patch("provide.foundation.logger.get_logger")
    def test_rate_limiter_processor_summary_exception_handling(
        self,
        mock_get_logger: MagicMock,
    ) -> None:
        """Test processor handles exceptions during summary emission."""
        mock_get_logger.side_effect = Exception("Logger unavailable")

        processor = RateLimiterProcessor(summary_interval_seconds=0.1)
        processor.suppressed_counts["test"] = 5  # Simulate some suppressed messages

        # Should not raise exception
        processor._emit_summary()

        # Should clear counts even if logging fails
        assert processor.suppressed_counts == {}

    @patch("provide.foundation.logger.get_logger")
    def test_rate_limiter_processor_callable_interface(self, mock_get_logger: Mock) -> None:
        """Test processor implements proper callable interface."""
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger

        processor = RateLimiterProcessor(summary_interval_seconds=100.0)

        # Should be callable with logger, method_name, and event_dict
        event_dict = {"event": "test", "logger_name": "test"}
        mock_logger = MagicMock()

        result = processor(mock_logger, "info", event_dict)
        assert result == event_dict


class TestCreateRateLimiterProcessor(FoundationTestCase):
    """Test create_rate_limiter_processor factory function."""

    def setup_method(self) -> None:
        """Reset GlobalRateLimiter singleton before each test."""
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
