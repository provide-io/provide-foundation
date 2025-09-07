#
# __init__.py
#
"""
Foundation Tracer Module.

Provides distributed tracing functionality with optional OpenTelemetry integration.
Falls back to simple, lightweight tracing when OpenTelemetry is not available.
"""

# OpenTelemetry feature detection
try:
    from opentelemetry import trace as otel_trace
    from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import (
        OTLPSpanExporter as OTLPGrpcSpanExporter,
    )
    from opentelemetry.exporter.otlp.proto.http.trace_exporter import (
        OTLPSpanExporter as OTLPHttpSpanExporter,
    )
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import BatchSpanProcessor

    _HAS_OTEL = True
except ImportError:
    otel_trace = None
    TracerProvider = None
    BatchSpanProcessor = None
    OTLPGrpcSpanExporter = None
    OTLPHttpSpanExporter = None
    _HAS_OTEL = False

from provide.foundation.tracer.context import (
    get_current_span,
    get_current_trace_id,
    get_trace_context,
    set_current_span,
    with_span,
)
from provide.foundation.tracer.spans import Span

__all__ = [
    "_HAS_OTEL",  # For internal use
    "Span",
    "get_current_span",
    "get_current_trace_id",
    "get_trace_context",
    "set_current_span",
    "with_span",
]
