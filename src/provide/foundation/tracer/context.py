#
# context.py
#
"""
Trace context management for Foundation tracer.
Manages trace context and span hierarchy.
"""

import contextvars
from typing import Any

from provide.foundation.tracer.spans import Span

# Context variable to track the current span
_current_span: contextvars.ContextVar[Span | None] = contextvars.ContextVar(
    "current_span", default=None
)

# Context variable to track the current trace ID
_current_trace_id: contextvars.ContextVar[str | None] = contextvars.ContextVar(
    "current_trace_id", default=None
)


def get_current_span() -> Span | None:
    """Get the currently active span."""
    return _current_span.get()


def get_current_trace_id() -> str | None:
    """Get the current trace ID."""
    return _current_trace_id.get()


def set_current_span(span: Span | None) -> None:
    """Set the current active span."""
    _current_span.set(span)
    if span:
        _current_trace_id.set(span.trace_id)


def create_child_span(name: str, parent: Span | None = None) -> Span:
    """
    Create a child span.

    Args:
        name: Name of the span
        parent: Parent span, defaults to current span

    Returns:
        New child span
    """
    if parent is None:
        parent = get_current_span()

    if parent:
        return Span(name=name, parent_id=parent.span_id, trace_id=parent.trace_id)
    else:
        return Span(name=name)


class SpanContext:
    """
    Context manager for managing span lifecycle.

    Automatically sets and clears the current span.
    """

    def __init__(self, span: Span):
        self.span = span
        self.previous_span: Span | None = None

    def __enter__(self) -> Span:
        """Enter the span context."""
        self.previous_span = get_current_span()
        set_current_span(self.span)
        return self.span

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit the span context."""
        if exc_type is not None:
            self.span.set_error(f"{exc_type.__name__}: {exc_val}")
        self.span.finish()
        set_current_span(self.previous_span)


def with_span(name: str) -> SpanContext:
    """
    Create a new span context.

    Args:
        name: Name of the span

    Returns:
        SpanContext that can be used as a context manager
    """
    span = create_child_span(name)
    return SpanContext(span)


def get_trace_context() -> dict[str, Any]:
    """
    Get the current trace context information.

    Returns:
        Dictionary with trace context information
    """
    current_span = get_current_span()
    trace_id = get_current_trace_id()

    return {
        "trace_id": trace_id,
        "span_id": current_span.span_id if current_span else None,
        "span_name": current_span.name if current_span else None,
    }
