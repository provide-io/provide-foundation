#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

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
    otel_trace: Any = None  # type: ignore[no-redef]
    TracerProvider: Any = None  # type: ignore[no-redef]
    BatchSpanProcessor: Any = None  # type: ignore[no-redef]
    OTLPGrpcSpanExporter: Any = None  # type: ignore[no-redef]
    OTLPHttpSpanExporter: Any = None  # type: ignore[no-redef]
    _HAS_OTEL = False

__all__ = [
    "_HAS_OTEL",  # For internal use
    "Span",
    "get_current_span",
    "get_current_trace_id",
    "get_trace_context",
    "set_current_span",
    "with_span",
]

# 🧱🏗️🔚
