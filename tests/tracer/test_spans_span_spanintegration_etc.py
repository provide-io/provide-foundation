#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for Foundation tracer spans module."""

from typing import Never
import uuid

from provide.testkit import FoundationTestCase
from provide.testkit.mocking import patch
from provide.testkit.time import make_controlled_time
import pytest

from provide.foundation.tracer.spans import Span


class TestSpan(FoundationTestCase):
    """Test Span functionality."""

    def setup_method(self) -> None:
        """Set up test environment."""
        super().setup_method()
        # Create controlled time for all tests
        self.get_time, self.advance_time, self.fake_sleep, self.fake_async_sleep = make_controlled_time()

    def test_span_creation_with_defaults(self) -> None:
        """Test creating a span with default values."""
        span = Span(name="test_operation", time_source=self.get_time)

        assert span.name == "test_operation"
        assert span.span_id is not None
        assert span.trace_id is not None
        assert span.parent_id is None
        assert span.start_time is not None
        assert span.start_time >= 0
        assert span.end_time is None
        assert span.tags == {}
        assert span.status == "ok"
        assert span.error is None
        assert span._active is True

    def test_span_creation_with_custom_values(self) -> None:
        """Test creating a span with custom values."""
        custom_span_id = str(uuid.uuid4())
        custom_trace_id = str(uuid.uuid4())
        custom_parent_id = str(uuid.uuid4())
        custom_start_time = self.get_time()
        custom_tags = {"service": "auth", "user_id": "123"}

        span = Span(
            name="auth_check",
            span_id=custom_span_id,
            trace_id=custom_trace_id,
            parent_id=custom_parent_id,
            start_time=custom_start_time,
            tags=custom_tags,
            status="pending",
            time_source=self.get_time,
        )

        assert span.name == "auth_check"
        assert span.span_id == custom_span_id
        assert span.trace_id == custom_trace_id
        assert span.parent_id == custom_parent_id
        assert span.start_time == custom_start_time
        assert span.tags == custom_tags
        assert span.status == "pending"

    def test_set_tag(self) -> None:
        """Test setting tags on a span."""
        span = Span(name="test_op", time_source=self.get_time)

        span.set_tag("user_id", "12345")
        span.set_tag("action", "login")

        assert span.tags["user_id"] == "12345"
        assert span.tags["action"] == "login"

    def test_set_error_with_string(self) -> None:
        """Test setting error with string message."""
        span = Span(name="test_op", time_source=self.get_time)

        span.set_error("Database connection failed")

        assert span.status == "error"
        assert span.error == "Database connection failed"

    def test_set_error_with_exception(self) -> None:
        """Test setting error with exception object."""
        span = Span(name="test_op", time_source=self.get_time)
        error = ValueError("Invalid input")

        span.set_error(error)

        assert span.status == "error"
        assert span.error == "Invalid input"

    def test_finish_span(self) -> None:
        """Test finishing a span."""
        span = Span(name="test_op", time_source=self.get_time)
        assert span._active is True
        assert span.end_time is None

        self.advance_time(0.5)  # Advance time by 0.5 seconds
        span.finish()

        assert span._active is False
        assert span.end_time is not None
        assert span.end_time > span.start_time

    def test_finish_span_twice(self) -> None:
        """Test that finishing a span twice doesn't change end_time."""
        span = Span(name="test_op", time_source=self.get_time)

        span.finish()
        first_end_time = span.end_time

        self.advance_time(0.001)  # Small delay
        span.finish()

        assert span.end_time == first_end_time

    def test_duration_ms_active_span(self) -> None:
        """Test duration calculation for active span."""
        # Create span at current time
        span = Span(name="test_op", time_source=self.get_time)
        start = span.start_time

        self.advance_time(1.5)  # Advance time by 1.5 seconds
        duration = span.duration_ms()

        assert duration == 1500.0  # 1.5 seconds = 1500ms
        assert span.start_time == start  # Verify start time didn't change

    def test_duration_ms_finished_span(self) -> None:
        """Test duration calculation for finished span."""
        # Create span with known start and end times
        span = Span(name="test_op", start_time=1000.0, time_source=self.get_time)
        span.end_time = 1002.0

        duration = span.duration_ms()
        assert duration == 2000.0  # 2 seconds = 2000ms

    def test_to_dict(self) -> None:
        """Test converting span to dictionary."""
        span = Span(name="test_op", time_source=self.get_time)
        span.set_tag("user_id", "123")
        span.set_tag("action", "login")
        self.advance_time(0.1)  # Advance time
        span.finish()

        span_dict = span.to_dict()

        assert span_dict["name"] == "test_op"
        assert span_dict["span_id"] == span.span_id
        assert span_dict["trace_id"] == span.trace_id
        assert span_dict["parent_id"] is None
        assert span_dict["start_time"] == span.start_time
        assert span_dict["end_time"] == span.end_time
        assert span_dict["duration_ms"] > 0
        assert span_dict["tags"] == {"user_id": "123", "action": "login"}
        assert span_dict["status"] == "ok"
        assert span_dict["error"] is None

    def test_context_manager_success(self) -> None:
        """Test using span as context manager with success."""
        with Span(name="test_op", time_source=self.get_time) as span:
            span.set_tag("result", "success")
            assert span._active is True

        assert span._active is False
        assert span.end_time is not None
        assert span.status == "ok"
        assert span.error is None

    def test_context_manager_with_exception(self) -> Never:
        """Test using span as context manager with exception."""
        with pytest.raises(ValueError), Span(name="test_op", time_source=self.get_time) as span:
            span.set_tag("action", "failing_op")
            raise ValueError("Something went wrong")

        assert span._active is False
        assert span.end_time is not None
        assert span.status == "error"
        assert span.error == "Something went wrong"

    def test_unique_ids_generated(self) -> None:
        """Test that unique IDs are generated for different spans."""
        span1 = Span(name="op1", time_source=self.get_time)
        span2 = Span(name="op2", time_source=self.get_time)

        assert span1.span_id != span2.span_id
        assert span1.trace_id != span2.trace_id

        # But they should be valid UUIDs
        uuid.UUID(span1.span_id)  # Should not raise
        uuid.UUID(span1.trace_id)  # Should not raise
        uuid.UUID(span2.span_id)  # Should not raise
        uuid.UUID(span2.trace_id)  # Should not raise


class TestSpanIntegration(FoundationTestCase):
    """Test span integration scenarios."""

    def setup_method(self) -> None:
        """Set up test environment."""
        super().setup_method()
        # Create controlled time for all tests
        self.get_time, self.advance_time, self.fake_sleep, self.fake_async_sleep = make_controlled_time()

    def test_parent_child_relationship(self) -> None:
        """Test setting up parent-child span relationship."""
        parent_span = Span(name="parent_op", time_source=self.get_time)
        child_span = Span(
            name="child_op",
            parent_id=parent_span.span_id,
            trace_id=parent_span.trace_id,
            time_source=self.get_time,
        )

        assert child_span.parent_id == parent_span.span_id
        assert child_span.trace_id == parent_span.trace_id
        assert child_span.span_id != parent_span.span_id

    def test_nested_context_managers(self) -> None:
        """Test nested spans using context managers."""
        with Span(name="outer_op", time_source=self.get_time) as outer_span:
            outer_span.set_tag("level", "outer")

            with Span(
                name="inner_op",
                parent_id=outer_span.span_id,
                trace_id=outer_span.trace_id,
                time_source=self.get_time,
            ) as inner_span:
                inner_span.set_tag("level", "inner")

                assert inner_span._active is True
                assert outer_span._active is True

            # Inner span should be finished
            assert inner_span._active is False
            assert outer_span._active is True

        # Both spans should be finished
        assert inner_span._active is False
        assert outer_span._active is False

    def test_span_timing_realistic(self) -> None:
        """Test span timing with realistic operation."""
        span = Span(name="database_query", time_source=self.get_time)
        span.set_tag("query", "SELECT * FROM users")

        # Simulate some work
        self.advance_time(0.015)  # 15ms

        span.finish()

        duration = span.duration_ms()
        assert duration >= 10.0  # At least 10ms
        assert duration < 100.0  # But not too long for test


class TestSpanOpenTelemetryIntegration(FoundationTestCase):
    """Test OpenTelemetry integration functionality."""

    def setup_method(self) -> None:
        """Set up test environment."""
        super().setup_method()
        # Create controlled time for all tests
        self.get_time, self.advance_time, self.fake_sleep, self.fake_async_sleep = make_controlled_time()

    def test_span_creation_with_otel_available(self) -> None:
        """Test span creation when OpenTelemetry is available."""
        with (
            patch("provide.foundation.tracer.spans._HAS_OTEL", True),
            patch("provide.foundation.tracer.spans.otel_trace") as mock_otel,
        ):
            mock_tracer = mock_otel.get_tracer.return_value
            mock_span = mock_tracer.start_span.return_value

            span = Span(name="test_op", time_source=self.get_time)

            mock_otel.get_tracer.assert_called_once_with("provide.foundation.tracer.spans")
            mock_tracer.start_span.assert_called_once_with("test_op")
            assert span._otel_span is mock_span

    def test_span_creation_with_otel_error(self) -> None:
        """Test span creation when OpenTelemetry initialization fails."""
        with (
            patch("provide.foundation.tracer.spans._HAS_OTEL", True),
            patch("provide.foundation.tracer.spans.otel_trace") as mock_otel,
        ):
            mock_otel.get_tracer.side_effect = Exception("OTEL setup failed")

            span = Span(name="test_op", time_source=self.get_time)

            assert span._otel_span is None

    def test_set_tag_with_otel_span(self) -> None:
        """Test setting tag when OpenTelemetry span is available."""
        with (
            patch("provide.foundation.tracer.spans._HAS_OTEL", True),
            patch("provide.foundation.tracer.spans.otel_trace") as mock_otel,
        ):
            mock_otel_span = mock_otel.get_tracer.return_value.start_span.return_value

            span = Span(name="test_op", time_source=self.get_time)
            span.set_tag("user_id", "123")

            assert span.tags["user_id"] == "123"
            mock_otel_span.set_attribute.assert_called_once_with("user_id", "123")

    def test_set_tag_with_otel_error(self) -> None:
        """Test setting tag when OpenTelemetry set_attribute fails."""
        with (
            patch("provide.foundation.tracer.spans._HAS_OTEL", True),
            patch("provide.foundation.tracer.spans.otel_trace") as mock_otel,
        ):
            mock_otel_span = mock_otel.get_tracer.return_value.start_span.return_value
            mock_otel_span.set_attribute.side_effect = Exception("Set attribute failed")

            span = Span(name="test_op", time_source=self.get_time)
            span.set_tag("user_id", "123")

            # Should still set local tag even if OTEL fails
            assert span.tags["user_id"] == "123"

    def test_set_error_with_otel_span(self) -> None:
        """Test setting error when OpenTelemetry span is available."""
        with (
            patch("provide.foundation.tracer.spans._HAS_OTEL", True),
            patch("provide.foundation.tracer.spans.otel_trace") as mock_otel,
            patch("provide.foundation.tracer.spans.Status"),
            patch("provide.foundation.tracer.spans.StatusCode"),
        ):
            mock_otel_span = mock_otel.get_tracer.return_value.start_span.return_value

            span = Span(name="test_op", time_source=self.get_time)
            error_msg = "Database error"
            span.set_error(error_msg)

            assert span.status == "error"
            assert span.error == error_msg
            mock_otel_span.set_status.assert_called_once()
            mock_otel_span.record_exception.assert_called_once()

    def test_set_error_with_exception_and_otel(self) -> None:
        """Test setting error with Exception object when OpenTelemetry is available."""
        with (
            patch("provide.foundation.tracer.spans._HAS_OTEL", True),
            patch("provide.foundation.tracer.spans.otel_trace") as mock_otel,
            patch("provide.foundation.tracer.spans.Status"),
            patch("provide.foundation.tracer.spans.StatusCode"),
        ):
            mock_otel_span = mock_otel.get_tracer.return_value.start_span.return_value

            span = Span(name="test_op", time_source=self.get_time)
            error = ValueError("Invalid data")
            span.set_error(error)

            assert span.status == "error"
            assert span.error == "Invalid data"
            mock_otel_span.record_exception.assert_called_once_with(error)

    def test_set_error_with_otel_failure(self) -> None:
        """Test setting error when OpenTelemetry operations fail."""
        with (
            patch("provide.foundation.tracer.spans._HAS_OTEL", True),
            patch("provide.foundation.tracer.spans.otel_trace") as mock_otel,
            patch("provide.foundation.tracer.spans.Status"),
            patch("provide.foundation.tracer.spans.StatusCode"),
        ):
            mock_otel_span = mock_otel.get_tracer.return_value.start_span.return_value
            mock_otel_span.set_status.side_effect = Exception("OTEL error")

            span = Span(name="test_op", time_source=self.get_time)
            span.set_error("Test error")

            # Should still set local error even if OTEL fails
            assert span.status == "error"
            assert span.error == "Test error"

    def test_finish_with_otel_span(self) -> None:
        """Test finishing span when OpenTelemetry span is available."""
        with (
            patch("provide.foundation.tracer.spans._HAS_OTEL", True),
            patch("provide.foundation.tracer.spans.otel_trace") as mock_otel,
        ):
            mock_otel_span = mock_otel.get_tracer.return_value.start_span.return_value

            span = Span(name="test_op", time_source=self.get_time)
            span.finish()

            assert span._active is False
            assert span.end_time is not None
            mock_otel_span.end.assert_called_once()

    def test_finish_with_otel_error(self) -> None:
        """Test finishing span when OpenTelemetry end() fails."""
        with (
            patch("provide.foundation.tracer.spans._HAS_OTEL", True),
            patch("provide.foundation.tracer.spans.otel_trace") as mock_otel,
        ):
            mock_otel_span = mock_otel.get_tracer.return_value.start_span.return_value
            mock_otel_span.end.side_effect = Exception("End failed")

            span = Span(name="test_op", time_source=self.get_time)
            span.finish()

            # Should still finish local span even if OTEL fails
            assert span._active is False
            assert span.end_time is not None


# 🧱🏗️🔚
