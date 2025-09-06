#
# __init__.py
#
"""
Foundation Tracer Module.

Provides basic distributed tracing functionality without external dependencies.
Simple, lightweight tracing for operation timing and context tracking.
"""

from provide.foundation.tracer.context import (
    get_current_span,
    get_current_trace_id,
    get_trace_context,
    set_current_span,
    with_span,
)
from provide.foundation.tracer.spans import Span

__all__ = [
    "Span",
    "get_current_span", 
    "get_current_trace_id",
    "get_trace_context",
    "set_current_span",
    "with_span",
]