#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Unit tests for OpenTelemetry metrics integration.

This module contains unit tests for OTEL metrics setup with mocked dependencies.
Run with: pytest tests/metrics/test_otel_unit.py -v"""

from __future__ import annotations

from provide.testkit import FoundationTestCase
from provide.testkit.mocking import MagicMock, patch

from provide.foundation.logger.config.telemetry import TelemetryConfig


class TestSetupOpenTelemetryMetrics(FoundationTestCase):
    """Tests for setup_opentelemetry_metrics function."""

    def test_setup_metrics_disabled(self) -> None:
        """Test setup when metrics are disabled."""
        config = TelemetryConfig(metrics_enabled=False)

        from provide.foundation.metrics.otel import setup_opentelemetry_metrics

        # Should return early without setting up
        setup_opentelemetry_metrics(config)
        # Just verify no exceptions raised

    def test_setup_globally_disabled(self) -> None:
        """Test setup when telemetry is globally disabled."""
        config = TelemetryConfig(globally_disabled=True, metrics_enabled=True)

        from provide.foundation.metrics.otel import setup_opentelemetry_metrics

        # Should return early even though metrics_enabled is True
        setup_opentelemetry_metrics(config)
        # Just verify no exceptions raised

    def test_setup_without_otel_installed(self) -> None:
        """Test setup when OpenTelemetry dependencies are not installed."""
        config = TelemetryConfig(metrics_enabled=True)

        # Mock _HAS_OTEL_METRICS to False
        with patch("provide.foundation.metrics.otel._HAS_OTEL_METRICS", False):
            from provide.foundation.metrics.otel import setup_opentelemetry_metrics

            # Should log debug message and return
            setup_opentelemetry_metrics(config)
            # Just verify no exceptions raised

    def test_setup_with_grpc_protocol(self) -> None:
        """Test setup with gRPC OTLP protocol."""
        config = TelemetryConfig(
            metrics_enabled=True,
            otlp_endpoint="http://localhost:4317",
            otlp_protocol="grpc",
            service_name="test-service",
            service_version="1.0.0",
        )

        # Mock the OTEL dependencies
        with (
            patch("provide.foundation.metrics.otel._HAS_OTEL_METRICS", True),
            patch("provide.foundation.metrics.otel.Resource") as mock_resource_class,
            patch("provide.foundation.metrics.otel.OTLPGrpcMetricExporter") as mock_grpc_exporter,
            patch("provide.foundation.metrics.otel.PeriodicExportingMetricReader") as mock_reader_class,
            patch("provide.foundation.metrics.otel.MeterProvider") as mock_provider_class,
            patch("provide.foundation.metrics.otel.otel_metrics") as mock_otel_metrics,
        ):
            mock_resource = MagicMock()
            mock_resource_class.create.return_value = mock_resource

            mock_exporter = MagicMock()
            mock_grpc_exporter.return_value = mock_exporter

            mock_reader = MagicMock()
            mock_reader_class.return_value = mock_reader

            mock_provider = MagicMock()
            mock_provider_class.return_value = mock_provider

            # Mock get_meter_provider to return a NoOpMeterProvider
            mock_current_provider = MagicMock()
            mock_current_provider.__class__.__name__ = "NoOpMeterProvider"
            mock_otel_metrics.get_meter_provider.return_value = mock_current_provider

            mock_meter = MagicMock()
            mock_otel_metrics.get_meter.return_value = mock_meter

            from provide.foundation.metrics.otel import setup_opentelemetry_metrics

            setup_opentelemetry_metrics(config)

            # Verify resource created with service info
            mock_resource_class.create.assert_called_once_with(
                {"service.name": "test-service", "service.version": "1.0.0"}
            )

            # Verify gRPC exporter created
            mock_grpc_exporter.assert_called_once()

            # Verify meter provider set
            mock_otel_metrics.set_meter_provider.assert_called_once_with(mock_provider)

    def test_setup_with_http_protocol(self) -> None:
        """Test setup with HTTP OTLP protocol."""
        config = TelemetryConfig(
            metrics_enabled=True,
            otlp_endpoint="http://localhost:4318",
            otlp_protocol="http/protobuf",
            service_name="test-service",
        )

        with (
            patch("provide.foundation.metrics.otel._HAS_OTEL_METRICS", True),
            patch("provide.foundation.metrics.otel.Resource") as mock_resource_class,
            patch("provide.foundation.metrics.otel.OTLPHttpMetricExporter") as mock_http_exporter,
            patch("provide.foundation.metrics.otel.PeriodicExportingMetricReader") as mock_reader_class,
            patch("provide.foundation.metrics.otel.MeterProvider") as mock_provider_class,
            patch("provide.foundation.metrics.otel.otel_metrics") as mock_otel_metrics,
        ):
            mock_resource = MagicMock()
            mock_resource_class.create.return_value = mock_resource

            mock_exporter = MagicMock()
            mock_http_exporter.return_value = mock_exporter

            mock_reader = MagicMock()
            mock_reader_class.return_value = mock_reader

            mock_provider = MagicMock()
            mock_provider_class.return_value = mock_provider

            mock_current_provider = MagicMock()
            mock_current_provider.__class__.__name__ = "NoOpMeterProvider"
            mock_otel_metrics.get_meter_provider.return_value = mock_current_provider

            mock_meter = MagicMock()
            mock_otel_metrics.get_meter.return_value = mock_meter

            from provide.foundation.metrics.otel import setup_opentelemetry_metrics

            setup_opentelemetry_metrics(config)

            # Verify HTTP exporter created
            mock_http_exporter.assert_called_once()

    def test_setup_with_otlp_headers(self) -> None:
        """Test setup with OTLP headers."""
        config = TelemetryConfig(
            metrics_enabled=True,
            otlp_endpoint="http://localhost:4317",
            otlp_protocol="grpc",
            otlp_headers="api-key=secret,x-custom=value",
        )

        with (
            patch("provide.foundation.metrics.otel._HAS_OTEL_METRICS", True),
            patch("provide.foundation.metrics.otel.Resource") as mock_resource_class,
            patch("provide.foundation.metrics.otel.OTLPGrpcMetricExporter") as mock_grpc_exporter,
            patch("provide.foundation.metrics.otel.PeriodicExportingMetricReader"),
            patch("provide.foundation.metrics.otel.MeterProvider"),
            patch("provide.foundation.metrics.otel.otel_metrics") as mock_otel_metrics,
        ):
            mock_resource = MagicMock()
            mock_resource_class.create.return_value = mock_resource

            mock_current_provider = MagicMock()
            mock_current_provider.__class__.__name__ = "NoOpMeterProvider"
            mock_otel_metrics.get_meter_provider.return_value = mock_current_provider

            mock_meter = MagicMock()
            mock_otel_metrics.get_meter.return_value = mock_meter

            from provide.foundation.metrics.otel import setup_opentelemetry_metrics

            setup_opentelemetry_metrics(config)

            # Verify exporter created with headers
            call_args = mock_grpc_exporter.call_args
            assert call_args is not None
            assert "headers" in call_args.kwargs
            headers = call_args.kwargs["headers"]
            assert headers == {"api-key": "secret", "x-custom": "value"}

    def test_setup_without_otlp_endpoint(self) -> None:
        """Test setup without OTLP endpoint."""
        config = TelemetryConfig(
            metrics_enabled=True,
            service_name="test-service",
        )

        with (
            patch("provide.foundation.metrics.otel._HAS_OTEL_METRICS", True),
            patch("provide.foundation.metrics.otel.Resource") as mock_resource_class,
            patch("provide.foundation.metrics.otel.MeterProvider") as mock_provider_class,
            patch("provide.foundation.metrics.otel.otel_metrics") as mock_otel_metrics,
        ):
            mock_resource = MagicMock()
            mock_resource_class.create.return_value = mock_resource

            mock_provider = MagicMock()
            mock_provider_class.return_value = mock_provider

            mock_current_provider = MagicMock()
            mock_current_provider.__class__.__name__ = "NoOpMeterProvider"
            mock_otel_metrics.get_meter_provider.return_value = mock_current_provider

            mock_meter = MagicMock()
            mock_otel_metrics.get_meter.return_value = mock_meter

            from provide.foundation.metrics.otel import setup_opentelemetry_metrics

            setup_opentelemetry_metrics(config)

            # Verify provider created with empty readers list
            call_args = mock_provider_class.call_args
            assert call_args is not None
            assert "metric_readers" in call_args.kwargs
            assert call_args.kwargs["metric_readers"] == []

    def test_setup_already_configured_provider(self) -> None:
        """Test setup when meter provider is already configured."""
        config = TelemetryConfig(
            metrics_enabled=True,
            otlp_endpoint="http://localhost:4317",
        )

        with (
            patch("provide.foundation.metrics.otel._HAS_OTEL_METRICS", True),
            patch("provide.foundation.metrics.otel.Resource") as mock_resource_class,
            patch("provide.foundation.metrics.otel.OTLPGrpcMetricExporter"),
            patch("provide.foundation.metrics.otel.OTLPHttpMetricExporter"),
            patch("provide.foundation.metrics.otel.PeriodicExportingMetricReader"),
            patch("provide.foundation.metrics.otel.MeterProvider"),
            patch("provide.foundation.metrics.otel.otel_metrics") as mock_otel_metrics,
        ):
            mock_resource = MagicMock()
            mock_resource_class.create.return_value = mock_resource

            # Mock an already configured provider (not NoOp)
            mock_current_provider = MagicMock()
            mock_current_provider.__class__.__name__ = "CustomMeterProvider"
            mock_current_provider.__class__.__module__ = "custom.module"
            mock_current_provider.get_meter = MagicMock()
            mock_otel_metrics.get_meter_provider.return_value = mock_current_provider

            from provide.foundation.metrics.otel import setup_opentelemetry_metrics

            setup_opentelemetry_metrics(config)

            # Should not call set_meter_provider again
            mock_otel_metrics.set_meter_provider.assert_not_called()

    def test_setup_exception_in_get_meter_provider(self) -> None:
        """Test setup when get_meter_provider raises exception."""
        config = TelemetryConfig(
            metrics_enabled=True,
            otlp_endpoint="http://localhost:4317",
        )

        with (
            patch("provide.foundation.metrics.otel._HAS_OTEL_METRICS", True),
            patch("provide.foundation.metrics.otel.Resource") as mock_resource_class,
            patch("provide.foundation.metrics.otel.OTLPGrpcMetricExporter"),
            patch("provide.foundation.metrics.otel.OTLPHttpMetricExporter"),
            patch("provide.foundation.metrics.otel.PeriodicExportingMetricReader"),
            patch("provide.foundation.metrics.otel.MeterProvider") as mock_provider_class,
            patch("provide.foundation.metrics.otel.otel_metrics") as mock_otel_metrics,
        ):
            mock_resource = MagicMock()
            mock_resource_class.create.return_value = mock_resource

            mock_provider = MagicMock()
            mock_provider_class.return_value = mock_provider

            # Mock get_meter_provider to raise exception
            mock_otel_metrics.get_meter_provider.side_effect = RuntimeError("OTEL not initialized")

            mock_meter = MagicMock()
            mock_otel_metrics.get_meter.return_value = mock_meter

            from provide.foundation.metrics.otel import setup_opentelemetry_metrics

            # Should handle exception and proceed with setup
            setup_opentelemetry_metrics(config)

            # Verify provider was still set
            mock_otel_metrics.set_meter_provider.assert_called_once_with(mock_provider)


class TestShutdownOpenTelemetryMetrics(FoundationTestCase):
    """Tests for shutdown_opentelemetry_metrics function."""

    def test_shutdown_without_otel_installed(self) -> None:
        """Test shutdown when OpenTelemetry is not installed."""
        with patch("provide.foundation.metrics.otel._HAS_OTEL_METRICS", False):
            from provide.foundation.metrics.otel import shutdown_opentelemetry_metrics

            # Should return early
            shutdown_opentelemetry_metrics()
            # Just verify no exceptions raised

    def test_shutdown_with_meter_provider(self) -> None:
        """Test shutdown with active meter provider."""
        with (
            patch("provide.foundation.metrics.otel._HAS_OTEL_METRICS", True),
            patch("provide.foundation.metrics.otel.otel_metrics") as mock_otel_metrics,
        ):
            mock_provider = MagicMock()
            mock_provider.shutdown = MagicMock()
            mock_otel_metrics.get_meter_provider.return_value = mock_provider

            from provide.foundation.metrics.otel import shutdown_opentelemetry_metrics

            shutdown_opentelemetry_metrics()

            # Verify shutdown was called
            mock_provider.shutdown.assert_called_once()

    def test_shutdown_without_shutdown_method(self) -> None:
        """Test shutdown when provider doesn't have shutdown method."""
        with (
            patch("provide.foundation.metrics.otel._HAS_OTEL_METRICS", True),
            patch("provide.foundation.metrics.otel.otel_metrics") as mock_otel_metrics,
        ):
            mock_provider = MagicMock(spec=[])  # No shutdown method
            mock_otel_metrics.get_meter_provider.return_value = mock_provider

            from provide.foundation.metrics.otel import shutdown_opentelemetry_metrics

            # Should handle gracefully
            shutdown_opentelemetry_metrics()

    def test_shutdown_exception_handling(self) -> None:
        """Test shutdown handles exceptions gracefully."""
        with (
            patch("provide.foundation.metrics.otel._HAS_OTEL_METRICS", True),
            patch("provide.foundation.metrics.otel.otel_metrics") as mock_otel_metrics,
        ):
            mock_provider = MagicMock()
            mock_provider.shutdown.side_effect = RuntimeError("Shutdown failed")
            mock_otel_metrics.get_meter_provider.return_value = mock_provider

            from provide.foundation.metrics.otel import shutdown_opentelemetry_metrics

            # Should handle exception and log warning
            shutdown_opentelemetry_metrics()
            # Just verify no exceptions raised


class TestRequireOtelMetrics(FoundationTestCase):
    """Tests for _require_otel_metrics function."""

    def test_require_otel_metrics_not_installed(self) -> None:
        """Test _require_otel_metrics raises ImportError when not installed."""
        with patch("provide.foundation.metrics.otel._HAS_OTEL_METRICS", False):
            import pytest

            from provide.foundation.metrics.otel import _require_otel_metrics

            with pytest.raises(ImportError, match="OpenTelemetry metrics require optional dependencies"):
                _require_otel_metrics()

    def test_require_otel_metrics_installed(self) -> None:
        """Test _require_otel_metrics succeeds when installed."""
        with patch("provide.foundation.metrics.otel._HAS_OTEL_METRICS", True):
            from provide.foundation.metrics.otel import _require_otel_metrics

            # Should not raise
            _require_otel_metrics()


__all__ = [
    "TestRequireOtelMetrics",
    "TestSetupOpenTelemetryMetrics",
    "TestShutdownOpenTelemetryMetrics",
]

# 🧱🏗️🔚
