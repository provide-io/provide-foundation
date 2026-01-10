#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for Foundation tracer context management."""

import contextvars
from typing import Never

from provide.testkit import FoundationTestCase
import pytest

from provide.foundation.tracer.context import (
    SpanContext,
    _current_span,
    _current_trace_id,
    create_child_span,
    get_current_span,
    get_current_trace_id,
    get_trace_context,
    set_current_span,
    with_span,
)
from provide.foundation.tracer.spans import Span


class TestTraceContext(FoundationTestCase):
    """Test trace context management."""

    def setup_method(self) -> None:
        """Reset context before each test."""
        super().setup_method()  # Call FoundationTestCase setup
        _current_span.set(None)
        _current_trace_id.set(None)

    def test_initial_context_is_empty(self) -> None:
        """Test that initial context has no active span or trace."""
        assert get_current_span() is None
        assert get_current_trace_id() is None

    def test_set_and_get_current_span(self) -> None:
        """Test setting and getting current span."""
        span = Span(name="test_op")

        set_current_span(span)

        assert get_current_span() == span
        assert get_current_trace_id() == span.trace_id

    def test_set_current_span_to_none(self) -> None:
        """Test setting current span to None."""
        span = Span(name="test_op")
        set_current_span(span)

        set_current_span(None)

        assert get_current_span() is None
        # Note: trace_id might still be set in this implementation

    def test_create_child_span_with_parent(self) -> None:
        """Test creating child span with explicit parent."""
        parent_span = Span(name="parent_op")

        child_span = create_child_span("child_op", parent=parent_span)

        assert child_span.name == "child_op"
        assert child_span.parent_id == parent_span.span_id
        assert child_span.trace_id == parent_span.trace_id
        assert child_span.span_id != parent_span.span_id

    def test_create_child_span_with_current_parent(self) -> None:
        """Test creating child span using current span as parent."""
        parent_span = Span(name="parent_op")
        set_current_span(parent_span)

        child_span = create_child_span("child_op")

        assert child_span.name == "child_op"
        assert child_span.parent_id == parent_span.span_id
        assert child_span.trace_id == parent_span.trace_id

    def test_create_child_span_no_parent(self) -> None:
        """Test creating child span when no parent exists."""
        child_span = create_child_span("root_op")

        assert child_span.name == "root_op"
        assert child_span.parent_id is None
        # Should have its own trace_id
        assert child_span.trace_id is not None

    def test_get_trace_context_with_span(self) -> None:
        """Test getting trace context when span is active."""
        span = Span(name="test_op")
        set_current_span(span)

        context = get_trace_context()

        assert context["trace_id"] == span.trace_id
        assert context["span_id"] == span.span_id
        assert context["span_name"] == span.name

    def test_get_trace_context_no_span(self) -> None:
        """Test getting trace context when no span is active."""
        context = get_trace_context()

        assert context["trace_id"] is None
        assert context["span_id"] is None
        assert context["span_name"] is None


class TestSpanContext(FoundationTestCase):
    """Test SpanContext context manager."""

    def setup_method(self) -> None:
        """Reset context before each test."""
        super().setup_method()  # Call FoundationTestCase setup
        _current_span.set(None)
        _current_trace_id.set(None)

    def test_span_context_lifecycle(self) -> None:
        """Test SpanContext lifecycle management."""
        span = Span(name="test_op")

        with SpanContext(span) as active_span:
            assert active_span == span
            assert get_current_span() == span
            assert span._active is True

        # Span should be finished and no longer current
        assert span._active is False
        assert get_current_span() is None

    def test_span_context_with_exception(self) -> Never:
        """Test SpanContext handling exceptions."""
        span = Span(name="test_op")

        with pytest.raises(ValueError), SpanContext(span):
            raise ValueError("Test error")

        assert span._active is False
        assert span.status == "error"
        assert span.error == "ValueError: Test error"

    def test_span_context_restores_previous_span(self) -> None:
        """Test that SpanContext restores previous span."""
        outer_span = Span(name="outer_op")
        set_current_span(outer_span)

        inner_span = Span(name="inner_op")

        with SpanContext(inner_span):
            assert get_current_span() == inner_span

        # Should restore outer span
        assert get_current_span() == outer_span

    def test_span_context_no_previous_span(self) -> None:
        """Test SpanContext when no previous span exists."""
        span = Span(name="test_op")

        with SpanContext(span):
            assert get_current_span() == span

        assert get_current_span() is None


class TestWithSpanHelper(FoundationTestCase):
    """Test with_span helper function."""

    def setup_method(self) -> None:
        """Reset context before each test."""
        super().setup_method()  # Call FoundationTestCase setup
        _current_span.set(None)
        _current_trace_id.set(None)

    def test_with_span_creates_root_span(self) -> None:
        """Test with_span creates root span when no parent exists."""
        with with_span("test_op") as span:
            assert span.name == "test_op"
            assert span.parent_id is None
            assert get_current_span() == span

        assert get_current_span() is None

    def test_with_span_creates_child_span(self) -> None:
        """Test with_span creates child span when parent exists."""
        parent_span = Span(name="parent_op")
        set_current_span(parent_span)

        with with_span("child_op") as child_span:
            assert child_span.name == "child_op"
            assert child_span.parent_id == parent_span.span_id
            assert child_span.trace_id == parent_span.trace_id
            assert get_current_span() == child_span

        # Should restore parent span
        assert get_current_span() == parent_span

    def test_with_span_handles_exception(self) -> Never:
        """Test with_span handling exceptions."""
        with pytest.raises(RuntimeError), with_span("failing_op") as span:
            raise RuntimeError("Operation failed")

        assert span.status == "error"
        assert span.error == "RuntimeError: Operation failed"
        assert get_current_span() is None

    def test_nested_with_span_calls(self) -> None:
        """Test nested with_span calls create proper hierarchy."""
        with with_span("level1") as span1:
            span1.set_tag("level", "1")

            with with_span("level2") as span2:
                span2.set_tag("level", "2")

                assert span2.parent_id == span1.span_id
                assert span2.trace_id == span1.trace_id
                assert get_current_span() == span2

                with with_span("level3") as span3:
                    span3.set_tag("level", "3")

                    assert span3.parent_id == span2.span_id
                    assert span3.trace_id == span1.trace_id
                    assert get_current_span() == span3

                # Should restore span2
                assert get_current_span() == span2

            # Should restore span1
            assert get_current_span() == span1

        # Should clear all spans
        assert get_current_span() is None


class TestContextVarIsolation(FoundationTestCase):
    """Test that context variables are properly isolated across contexts."""

    def test_context_isolation(self) -> None:
        """Test that spans are isolated in different contexts."""
        span1 = Span(name="span1")
        span2 = Span(name="span2")

        # Create a new context
        ctx = contextvars.copy_context()

        # Set span1 in current context
        set_current_span(span1)
        assert get_current_span() == span1

        def set_span2() -> None:
            """Function to run in different context."""
            set_current_span(span2)
            assert get_current_span() == span2

        # Run function in different context
        ctx.run(set_span2)

        # Original context should still have span1
        assert get_current_span() == span1

    def test_with_span_context_isolation(self) -> None:
        """Test with_span in different contexts."""
        results = []

        def worker(name: str) -> None:
            """Worker function for different context."""
            with with_span(f"worker_{name}") as span:
                span.set_tag("worker", name)
                results.append(
                    {"name": span.name, "span_id": span.span_id, "worker": name},
                )

        # Run workers in different contexts
        ctx1 = contextvars.copy_context()
        ctx2 = contextvars.copy_context()

        ctx1.run(worker, "A")
        ctx2.run(worker, "B")

        assert len(results) == 2
        assert results[0]["name"] == "worker_A"
        assert results[1]["name"] == "worker_B"
        assert results[0]["span_id"] != results[1]["span_id"]


class TestTraceContextIntegration(FoundationTestCase):
    """Test integration scenarios with trace context."""

    def setup_method(self) -> None:
        """Reset context before each test."""
        super().setup_method()  # Call FoundationTestCase setup
        _current_span.set(None)
        _current_trace_id.set(None)

    def test_complex_operation_tracing(self) -> None:
        """Test tracing a complex operation with multiple spans."""
        with with_span("http_request") as request_span:
            request_span.set_tag("method", "POST")
            request_span.set_tag("url", "/api/users")

            # Database operation
            with with_span("database_query") as db_span:
                db_span.set_tag("query", "INSERT INTO users")
                db_span.set_tag("duration_ms", 45)

            # External API call
            with with_span("external_api") as api_span:
                api_span.set_tag("service", "auth_service")
                api_span.set_tag("timeout", 5000)

        # Verify span relationships
        assert db_span.parent_id == request_span.span_id
        assert api_span.parent_id == request_span.span_id
        assert db_span.trace_id == request_span.trace_id
        assert api_span.trace_id == request_span.trace_id

        # All spans should be finished
        assert not request_span._active
        assert not db_span._active
        assert not api_span._active

    def test_error_propagation_in_trace(self) -> Never:
        """Test error handling in nested trace context."""
        with pytest.raises(ValueError), with_span("outer_operation") as outer_span:
            outer_span.set_tag("component", "business_logic")

            with with_span("inner_operation") as inner_span:
                inner_span.set_tag("step", "validation")
                raise ValueError("Validation failed")

        # Outer span should be marked as error
        assert outer_span.status == "error"
        assert "ValueError" in outer_span.error

        # Inner span should also be marked as error
        assert inner_span.status == "error"
        assert "ValueError" in inner_span.error


# 🧱🏗️🔚
