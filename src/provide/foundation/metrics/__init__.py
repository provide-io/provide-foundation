#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from __future__ import annotations

from typing import Any

from provide.foundation.metrics.simple import (
    SimpleCounter,
    SimpleGauge,
    SimpleHistogram,
)

"""Foundation Metrics Module.

Provides metrics collection with optional OpenTelemetry integration.
Falls back to simple metrics when OpenTelemetry is not available.
"""

try:
    from opentelemetry import metrics as otel_metrics
    from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import (
        OTLPMetricExporter as OTLPGrpcMetricExporter,
    )
    from opentelemetry.exporter.otlp.proto.http.metric_exporter import (
        OTLPMetricExporter as OTLPHttpMetricExporter,
    )
    from opentelemetry.sdk.metrics import MeterProvider
    from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader

    _HAS_OTEL_METRICS = True
except ImportError:
    otel_metrics: Any = None  # type: ignore[no-redef]
    MeterProvider: Any = None  # type: ignore[no-redef]
    PeriodicExportingMetricReader: Any = None  # type: ignore[no-redef]
    OTLPGrpcMetricExporter: Any = None  # type: ignore[no-redef]
    OTLPHttpMetricExporter: Any = None  # type: ignore[no-redef]
    _HAS_OTEL_METRICS = False

# Export the main API
__all__ = [
    "_HAS_OTEL_METRICS",  # For internal use
    "counter",
    "gauge",
    "histogram",
]

# Global meter instance (will be set during setup)
_meter = None


def counter(name: str, description: str = "", unit: str = "") -> SimpleCounter:
    """Create a counter metric.

    Args:
        name: Name of the counter
        description: Description of what this counter measures
        unit: Unit of measurement

    Returns:
        Counter instance

    """
    if _HAS_OTEL_METRICS and _meter:
        try:
            otel_counter = _meter.create_counter(name=name, description=description, unit=unit)
            return SimpleCounter(name, otel_counter=otel_counter)
        except Exception:
            # Broad catch intentional: OTEL metrics are optional, gracefully fall back to simple counter
            pass

    return SimpleCounter(name)


def gauge(name: str, description: str = "", unit: str = "") -> SimpleGauge:
    """Create a gauge metric.

    Args:
        name: Name of the gauge
        description: Description of what this gauge measures
        unit: Unit of measurement

    Returns:
        Gauge instance

    """
    if _HAS_OTEL_METRICS and _meter:
        try:
            otel_gauge = _meter.create_up_down_counter(name=name, description=description, unit=unit)
            return SimpleGauge(name, otel_gauge=otel_gauge)
        except Exception:
            # Broad catch intentional: OTEL metrics are optional, gracefully fall back to simple gauge
            pass

    return SimpleGauge(name)


def histogram(name: str, description: str = "", unit: str = "") -> SimpleHistogram:
    """Create a histogram metric.

    Args:
        name: Name of the histogram
        description: Description of what this histogram measures
        unit: Unit of measurement

    Returns:
        Histogram instance

    """
    if _HAS_OTEL_METRICS and _meter:
        try:
            otel_histogram = _meter.create_histogram(name=name, description=description, unit=unit)
            return SimpleHistogram(name, otel_histogram=otel_histogram)
        except Exception:
            # Broad catch intentional: OTEL metrics are optional, gracefully fall back to simple histogram
            pass

    return SimpleHistogram(name)


def _set_meter(meter: object) -> None:
    """Set the global meter instance (internal use only)."""
    global _meter
    _meter = meter


# 🧱🏗️🔚
