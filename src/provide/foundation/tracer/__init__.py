#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#


from __future__ import annotations

#
# __init__.py
#
from typing import TYPE_CHECKING, Any

from provide.foundation.tracer.context import (
    get_current_span,
    get_current_trace_id,
    get_trace_context,
    set_current_span,
    with_span,
)
from provide.foundation.tracer.spans import Span

"""Foundation Tracer Module.

Provides distributed tracing functionality with optional OpenTelemetry integration.
Falls back to simple, lightweight tracing when OpenTelemetry is not available.

OpenTelemetry imports are lazy-loaded on first access (~18ms saved at import time).
"""

if TYPE_CHECKING:
    from opentelemetry import trace as otel_trace
    from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import (
        OTLPSpanExporter as OTLPGrpcSpanExporter,
    )
    from opentelemetry.exporter.otlp.proto.http.trace_exporter import (
        OTLPSpanExporter as OTLPHttpSpanExporter,
    )
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import BatchSpanProcessor

# Lazy-load state for OpenTelemetry
_otel_loaded: bool = False
_otel_available: bool = False
_otel_cache: dict[str, Any] = {}


def _ensure_otel_available() -> bool:
    """Lazy-load OpenTelemetry dependencies on first use (~18ms saved at import)."""
    global _otel_loaded, _otel_available
    if _otel_loaded:
        return _otel_available
    _otel_loaded = True
    try:
        from opentelemetry import trace as _trace
        from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import (
            OTLPSpanExporter as _GrpcExporter,
        )
        from opentelemetry.exporter.otlp.proto.http.trace_exporter import (
            OTLPSpanExporter as _HttpExporter,
        )
        from opentelemetry.sdk.trace import TracerProvider as _TP
        from opentelemetry.sdk.trace.export import BatchSpanProcessor as _BSP

        _otel_cache.update({
            "otel_trace": _trace,
            "TracerProvider": _TP,
            "BatchSpanProcessor": _BSP,
            "OTLPGrpcSpanExporter": _GrpcExporter,
            "OTLPHttpSpanExporter": _HttpExporter,
        })
        _otel_available = True
    except ImportError:
        _otel_available = False
    return _otel_available


def __getattr__(name: str) -> Any:
    """Module-level __getattr__ for lazy-loading OpenTelemetry symbols."""
    if name == "_HAS_OTEL":
        return _ensure_otel_available()
    otel_names = {
        "otel_trace", "TracerProvider", "BatchSpanProcessor",
        "OTLPGrpcSpanExporter", "OTLPHttpSpanExporter",
    }
    if name in otel_names:
        _ensure_otel_available()
        return _otel_cache.get(name)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


__all__ = [
    "_HAS_OTEL",  # For internal use
    "_ensure_otel_available",
    "Span",
    "get_current_span",
    "get_current_trace_id",
    "get_trace_context",
    "set_current_span",
    "with_span",
]

# 🧱🏗️🔚
