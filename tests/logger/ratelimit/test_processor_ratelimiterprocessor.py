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
)


class TestRateLimiterProcessor(FoundationTestCase):
    """Test RateLimiterProcessor class."""

    def setup_method(self) -> None:
        """Reset GlobalRateLimiter singleton before each test."""
        super().setup_method()
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


# 🧱🏗️🔚
