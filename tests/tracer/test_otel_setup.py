#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#


from typing import Any

from provide.testkit import FoundationTestCase
from provide.testkit.mocking import Mock, patch
import pytest

from provide.foundation.tracer.otel import (
    _require_otel,
    get_otel_tracer,
    setup_opentelemetry_tracing,
)


class TestRequireOtel(FoundationTestCase):
    """Test _require_otel function."""

    def test_require_otel_available(self) -> None:
        """Test _require_otel when OpenTelemetry is available."""
        with patch("provide.foundation.tracer.otel._HAS_OTEL", True):
            # Should not raise
            _require_otel()

    def test_require_otel_not_available(self) -> None:
        """Test _require_otel when OpenTelemetry is not available."""
        with patch("provide.foundation.tracer.otel._HAS_OTEL", False):
            with pytest.raises(ImportError) as exc_info:
                _require_otel()

            assert "OpenTelemetry features require optional dependencies" in str(exc_info.value)
            assert "uv add 'provide-foundation[opentelemetry]'" in str(exc_info.value)


class TestSetupOpentelemetryTracing(FoundationTestCase):
    """Test setup_opentelemetry_tracing function."""

    def create_mock_config(self, **kwargs: Any) -> Mock:
        """Create a mock TelemetryConfig with defaults."""
        defaults = {
            "tracing_enabled": True,
            "globally_disabled": False,
            "service_name": "test-service",
            "service_version": "1.0.0",
            "trace_sample_rate": 1.0,
            "otlp_endpoint": None,
            "otlp_traces_endpoint": None,
            "otlp_protocol": "grpc",
        }
        defaults.update(kwargs)

        config = Mock()
        for key, value in defaults.items():
            setattr(config, key, value)

        config.get_otlp_headers_dict.return_value = {"x-api-key": "test-key"}
        return config

    def test_setup_tracing_disabled(self) -> None:
        """Test setup when tracing is disabled."""
        config = self.create_mock_config(tracing_enabled=False)

        with patch("provide.foundation.tracer.otel._HAS_OTEL", True):
            # Should return early without setting up tracing
            setup_opentelemetry_tracing(config)
            # No assertions needed - function should return without error

    def test_setup_globally_disabled(self) -> None:
        """Test setup when globally disabled."""
        config = self.create_mock_config(globally_disabled=True)

        with patch("provide.foundation.tracer.otel._HAS_OTEL", True):
            setup_opentelemetry_tracing(config)
            # No assertions needed - function should return without error

    def test_setup_otel_not_available(self) -> None:
        """Test setup when OpenTelemetry is not available."""
        config = self.create_mock_config()

        with patch("provide.foundation.tracer.otel._HAS_OTEL", False):
            setup_opentelemetry_tracing(config)
            # No assertions needed - function should return without error

    def test_setup_basic_without_otlp(self) -> None:
        """Test basic setup without OTLP endpoint."""
        config = self.create_mock_config(
            otlp_endpoint=None,
            otlp_traces_endpoint=None,
        )

        mock_resource = Mock()
        mock_sampler = Mock()
        mock_tracer_provider = Mock()

        with (
            patch("provide.foundation.tracer.otel._HAS_OTEL", True),
            patch("provide.foundation.tracer.otel.Resource") as mock_resource_class,
            patch("provide.foundation.tracer.otel.TraceIdRatioBased") as mock_sampler_class,
            patch("provide.foundation.tracer.otel.TracerProvider") as mock_provider_class,
            patch("provide.foundation.tracer.otel.otel_trace") as mock_trace,
            patch("provide.foundation.tracer.otel.slog"),
        ):
            mock_resource_class.create.return_value = mock_resource
            mock_sampler_class.return_value = mock_sampler
            mock_provider_class.return_value = mock_tracer_provider

            setup_opentelemetry_tracing(config)

            # Verify resource creation
            mock_resource_class.create.assert_called_once_with(
                {
                    "service.name": "test-service",
                    "service.version": "1.0.0",
                }
            )

            # Verify sampler creation
            mock_sampler_class.assert_called_once_with(1.0)

            # Verify tracer provider creation
            mock_provider_class.assert_called_once_with(
                resource=mock_resource,
                sampler=mock_sampler,
            )

            # Verify tracer provider is set
            mock_trace.set_tracer_provider.assert_called_once_with(mock_tracer_provider)

            # Verify logging

    def test_setup_with_grpc_otlp(self) -> None:
        """Test setup with GRPC OTLP exporter."""
        config = self.create_mock_config(
            otlp_endpoint="http://localhost:4317",
            otlp_protocol="grpc",
        )

        mock_resource = Mock()
        mock_sampler = Mock()
        mock_tracer_provider = Mock()
        mock_exporter = Mock()
        mock_processor = Mock()

        with (
            patch("provide.foundation.tracer.otel._HAS_OTEL", True),
            patch("provide.foundation.tracer.otel.Resource") as mock_resource_class,
            patch("provide.foundation.tracer.otel.TraceIdRatioBased") as mock_sampler_class,
            patch("provide.foundation.tracer.otel.TracerProvider") as mock_provider_class,
            patch("provide.foundation.tracer.otel.OTLPGrpcSpanExporter") as mock_exporter_class,
            patch("provide.foundation.tracer.otel.BatchSpanProcessor") as mock_processor_class,
            patch("provide.foundation.tracer.otel.otel_trace"),
            patch("provide.foundation.tracer.otel.slog"),
        ):
            mock_resource_class.create.return_value = mock_resource
            mock_sampler_class.return_value = mock_sampler
            mock_provider_class.return_value = mock_tracer_provider
            mock_exporter_class.return_value = mock_exporter
            mock_processor_class.return_value = mock_processor

            setup_opentelemetry_tracing(config)

            # Verify GRPC exporter creation
            mock_exporter_class.assert_called_once_with(
                endpoint="http://localhost:4317",
                headers={"x-api-key": "test-key"},
            )

            # Verify processor creation
            mock_processor_class.assert_called_once_with(mock_exporter)

            # Verify processor is added to tracer provider
            mock_tracer_provider.add_span_processor.assert_called_once_with(mock_processor)

            # Verify debug logging for OTLP

    def test_setup_with_http_otlp(self) -> None:
        """Test setup with HTTP OTLP exporter."""
        config = self.create_mock_config(
            otlp_traces_endpoint="http://localhost:4318/v1/traces",
            otlp_protocol="http",
        )

        mock_resource = Mock()
        mock_sampler = Mock()
        mock_tracer_provider = Mock()
        mock_exporter = Mock()
        mock_processor = Mock()

        with (
            patch("provide.foundation.tracer.otel._HAS_OTEL", True),
            patch("provide.foundation.tracer.otel.Resource") as mock_resource_class,
            patch("provide.foundation.tracer.otel.TraceIdRatioBased") as mock_sampler_class,
            patch("provide.foundation.tracer.otel.TracerProvider") as mock_provider_class,
            patch("provide.foundation.tracer.otel.OTLPHttpSpanExporter") as mock_exporter_class,
            patch("provide.foundation.tracer.otel.BatchSpanProcessor") as mock_processor_class,
            patch("provide.foundation.tracer.otel.otel_trace"),
            patch("provide.foundation.tracer.otel.slog"),
        ):
            mock_resource_class.create.return_value = mock_resource
            mock_sampler_class.return_value = mock_sampler
            mock_provider_class.return_value = mock_tracer_provider
            mock_exporter_class.return_value = mock_exporter
            mock_processor_class.return_value = mock_processor

            setup_opentelemetry_tracing(config)

            # Verify HTTP exporter creation
            mock_exporter_class.assert_called_once_with(
                endpoint="http://localhost:4318/v1/traces",
                headers={"x-api-key": "test-key"},
            )

            # Verify debug logging for OTLP

    def test_setup_otlp_endpoint_priority(self) -> None:
        """Test that otlp_traces_endpoint takes priority over otlp_endpoint."""
        config = self.create_mock_config(
            otlp_endpoint="http://localhost:4317",
            otlp_traces_endpoint="http://localhost:4318/v1/traces",
            otlp_protocol="http",
        )

        mock_resource = Mock()
        mock_sampler = Mock()
        mock_tracer_provider = Mock()
        mock_exporter = Mock()
        mock_processor = Mock()

        with (
            patch("provide.foundation.tracer.otel._HAS_OTEL", True),
            patch("provide.foundation.tracer.otel.Resource") as mock_resource_class,
            patch("provide.foundation.tracer.otel.TraceIdRatioBased") as mock_sampler_class,
            patch("provide.foundation.tracer.otel.TracerProvider") as mock_provider_class,
            patch("provide.foundation.tracer.otel.OTLPHttpSpanExporter") as mock_exporter_class,
            patch("provide.foundation.tracer.otel.BatchSpanProcessor") as mock_processor_class,
            patch("provide.foundation.tracer.otel.otel_trace"),
            patch("provide.foundation.tracer.otel.slog"),
        ):
            mock_resource_class.create.return_value = mock_resource
            mock_sampler_class.return_value = mock_sampler
            mock_provider_class.return_value = mock_tracer_provider
            mock_exporter_class.return_value = mock_exporter
            mock_processor_class.return_value = mock_processor

            setup_opentelemetry_tracing(config)

            # Verify that otlp_traces_endpoint was used
            mock_exporter_class.assert_called_once_with(
                endpoint="http://localhost:4318/v1/traces",
                headers={"x-api-key": "test-key"},
            )

    def test_setup_minimal_service_info(self) -> None:
        """Test setup with minimal service information."""
        config = self.create_mock_config(
            service_name=None,
            service_version=None,
        )

        mock_resource = Mock()
        mock_sampler = Mock()
        mock_tracer_provider = Mock()

        with (
            patch("provide.foundation.tracer.otel._HAS_OTEL", True),
            patch("provide.foundation.tracer.otel.Resource") as mock_resource_class,
            patch("provide.foundation.tracer.otel.TraceIdRatioBased") as mock_sampler_class,
            patch("provide.foundation.tracer.otel.TracerProvider") as mock_provider_class,
            patch("provide.foundation.tracer.otel.otel_trace"),
            patch("provide.foundation.tracer.otel.slog"),
        ):
            mock_resource_class.create.return_value = mock_resource
            mock_sampler_class.return_value = mock_sampler
            mock_provider_class.return_value = mock_tracer_provider

            setup_opentelemetry_tracing(config)

            # Verify resource creation with empty attributes
            mock_resource_class.create.assert_called_once_with({})


class TestGetOtelTracer(FoundationTestCase):
    """Test get_otel_tracer function."""

    def test_get_tracer_otel_not_available(self) -> None:
        """Test getting tracer when OpenTelemetry is not available."""
        with patch("provide.foundation.tracer.otel._HAS_OTEL", False):
            result = get_otel_tracer("test-tracer")
            assert result is None

    def test_get_tracer_success(self) -> None:
        """Test getting tracer successfully."""
        mock_tracer = Mock()

        with (
            patch("provide.foundation.tracer.otel._HAS_OTEL", True),
            patch("provide.foundation.tracer.otel.otel_trace") as mock_trace,
        ):
            mock_trace.get_tracer.return_value = mock_tracer
            result = get_otel_tracer("test-tracer")

            assert result == mock_tracer
            mock_trace.get_tracer.assert_called_once_with("test-tracer")

    def test_get_tracer_exception(self) -> None:
        """Test getting tracer when an exception occurs."""
        with (
            patch("provide.foundation.tracer.otel._HAS_OTEL", True),
            patch("provide.foundation.tracer.otel.otel_trace") as mock_trace,
        ):
            mock_trace.get_tracer.side_effect = Exception("Tracer error")

            result = get_otel_tracer("test-tracer")

            assert result is None


# 🧱🏗️🔚
