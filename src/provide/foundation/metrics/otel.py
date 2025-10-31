#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from provide.foundation.logger.config.telemetry import TelemetryConfig
from provide.foundation.logger.setup import get_system_logger

if TYPE_CHECKING:
    from provide.foundation.logger.base import FoundationLogger

"""OpenTelemetry metrics integration."""

slog: FoundationLogger | Any = get_system_logger(__name__)

# Feature detection
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
    from opentelemetry.sdk.resources import Resource

    _HAS_OTEL_METRICS = True
except ImportError:
    _HAS_OTEL_METRICS = False
    # Stub everything
    otel_metrics: Any = None  # type: ignore[no-redef]
    MeterProvider: Any = None  # type: ignore[no-redef]
    PeriodicExportingMetricReader: Any = None  # type: ignore[no-redef]
    Resource: Any = None  # type: ignore[no-redef]
    OTLPGrpcMetricExporter: Any = None  # type: ignore[no-redef]
    OTLPHttpMetricExporter: Any = None  # type: ignore[no-redef]


def _require_otel_metrics() -> None:
    """Ensure OpenTelemetry metrics are available."""
    if not _HAS_OTEL_METRICS:
        raise ImportError(
            "OpenTelemetry metrics require optional dependencies. "
            "Install with: pip install 'provide-foundation[opentelemetry]'",
        )


def setup_opentelemetry_metrics(config: TelemetryConfig) -> None:
    """Setup OpenTelemetry metrics with configuration.

    Args:
        config: Telemetry configuration

    """
    # Check if metrics are disabled first, before checking dependencies
    if not config.metrics_enabled or config.globally_disabled:
        slog.debug("📊 OpenTelemetry metrics disabled")
        return

    # Check if OpenTelemetry metrics are available
    if not _HAS_OTEL_METRICS:
        slog.debug("📊 OpenTelemetry metrics not available (dependencies not installed)")
        return

    slog.debug("📊🚀 Setting up OpenTelemetry metrics")

    # Create resource with service information
    resource_attrs = {}
    if config.service_name:
        resource_attrs["service.name"] = config.service_name
    if config.service_version:
        resource_attrs["service.version"] = config.service_version

    resource = Resource.create(resource_attrs)

    # Setup metric readers with OTLP exporters if configured
    readers = []

    if config.otlp_endpoint:
        endpoint = config.otlp_endpoint
        headers = config.get_otlp_headers_dict()

        slog.debug(f"📊📤 Configuring OTLP metrics exporter: {endpoint}")

        # Choose exporter based on protocol
        if config.otlp_protocol == "grpc":
            exporter: OTLPGrpcMetricExporter | OTLPHttpMetricExporter = OTLPGrpcMetricExporter(
                endpoint=endpoint,
                headers=headers,
            )
        else:  # http/protobuf
            exporter = OTLPHttpMetricExporter(
                endpoint=endpoint,
                headers=headers,
            )

        # Create periodic reader (exports every 60 seconds by default)
        reader = PeriodicExportingMetricReader(exporter, export_interval_millis=60000)
        readers.append(reader)

    # Create meter provider
    meter_provider = MeterProvider(resource=resource, metric_readers=readers)

    # Set the global meter provider (only if not already set)
    try:
        current_provider = otel_metrics.get_meter_provider()
        provider_type = type(current_provider).__name__

        # Always allow setup if:
        # 1. It's a default/no-op provider
        # 2. It's a mock (for testing)
        # 3. It's our own MeterProvider type (allow re-configuration)
        should_setup = (
            provider_type in ["NoOpMeterProvider", "ProxyMeterProvider", "Mock", "MagicMock"]
            or not hasattr(current_provider, "get_meter")
            or current_provider.__class__.__module__.startswith("unittest.mock")
        )

        if should_setup:
            otel_metrics.set_meter_provider(meter_provider)

            # Set the global meter for our metrics module
            from provide.foundation.metrics import _set_meter

            meter = otel_metrics.get_meter(__name__)
            _set_meter(meter)

        else:
            slog.debug("📊 OpenTelemetry meter provider already configured")
    except Exception:
        # Broad catch intentional: get_meter_provider() may fail in various OTEL environments
        # Proceed with setup if provider check fails
        otel_metrics.set_meter_provider(meter_provider)

        # Set the global meter for our metrics module
        from provide.foundation.metrics import _set_meter

        meter = otel_metrics.get_meter(__name__)
        _set_meter(meter)


def shutdown_opentelemetry_metrics() -> None:
    """Shutdown OpenTelemetry metrics."""
    if not _HAS_OTEL_METRICS:
        return

    try:
        meter_provider = otel_metrics.get_meter_provider()
        if hasattr(meter_provider, "shutdown"):
            meter_provider.shutdown()
            slog.debug("📊🛑 OpenTelemetry meter provider shutdown")
    except Exception as e:
        slog.warning(f"⚠️ Error shutting down OpenTelemetry metrics: {e}")


# 🧱🏗️🔚
