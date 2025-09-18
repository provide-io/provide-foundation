"""Comprehensive tests for tracer/otel.py module."""

import sys
from unittest.mock import Mock, patch

import pytest

from provide.foundation.tracer.otel import (
    _HAS_OTEL,
    _require_otel,
    get_otel_tracer,
    setup_opentelemetry_tracing,
    shutdown_opentelemetry,
)


class TestRequireOtel:
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
            assert "pip install 'provide-foundation[opentelemetry]'" in str(exc_info.value)


class TestSetupOpentelemetryTracing:
    """Test setup_opentelemetry_tracing function."""

    def create_mock_config(self, **kwargs) -> Mock:
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
            patch("provide.foundation.tracer.otel.slog") as mock_log,
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
            mock_log.info.assert_called_once_with("🔍✅ OpenTelemetry tracing setup complete")

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
            patch("provide.foundation.tracer.otel.slog") as mock_log,
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
            mock_log.debug.assert_called_once_with("✅ OTLP span exporter configured: grpc")

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

        with patch("provide.foundation.tracer.otel._HAS_OTEL", True):
            with patch("provide.foundation.tracer.otel.Resource") as mock_resource_class:
                with patch("provide.foundation.tracer.otel.TraceIdRatioBased") as mock_sampler_class:
                    with patch("provide.foundation.tracer.otel.TracerProvider") as mock_provider_class:
                        with patch(
                            "provide.foundation.tracer.otel.OTLPHttpSpanExporter"
                        ) as mock_exporter_class:
                            with patch(
                                "provide.foundation.tracer.otel.BatchSpanProcessor"
                            ) as mock_processor_class:
                                with patch("provide.foundation.tracer.otel.otel_trace"):
                                    with patch("provide.foundation.tracer.otel.slog") as mock_log:
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
                                        mock_log.debug.assert_called_once_with(
                                            "✅ OTLP span exporter configured: http"
                                        )

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

        with patch("provide.foundation.tracer.otel._HAS_OTEL", True):
            with patch("provide.foundation.tracer.otel.Resource") as mock_resource_class:
                with patch("provide.foundation.tracer.otel.TraceIdRatioBased") as mock_sampler_class:
                    with patch("provide.foundation.tracer.otel.TracerProvider") as mock_provider_class:
                        with patch(
                            "provide.foundation.tracer.otel.OTLPHttpSpanExporter"
                        ) as mock_exporter_class:
                            with patch(
                                "provide.foundation.tracer.otel.BatchSpanProcessor"
                            ) as mock_processor_class:
                                with patch("provide.foundation.tracer.otel.otel_trace"):
                                    with patch("provide.foundation.tracer.otel.slog"):
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

        with patch("provide.foundation.tracer.otel._HAS_OTEL", True):
            with patch("provide.foundation.tracer.otel.Resource") as mock_resource_class:
                with patch("provide.foundation.tracer.otel.TraceIdRatioBased") as mock_sampler_class:
                    with patch("provide.foundation.tracer.otel.TracerProvider") as mock_provider_class:
                        with patch("provide.foundation.tracer.otel.otel_trace"):
                            with patch("provide.foundation.tracer.otel.slog"):
                                mock_resource_class.create.return_value = mock_resource
                                mock_sampler_class.return_value = mock_sampler
                                mock_provider_class.return_value = mock_tracer_provider

                                setup_opentelemetry_tracing(config)

                                # Verify resource creation with empty attributes
                                mock_resource_class.create.assert_called_once_with({})


class TestGetOtelTracer:
    """Test get_otel_tracer function."""

    def test_get_tracer_otel_not_available(self) -> None:
        """Test getting tracer when OpenTelemetry is not available."""
        with patch("provide.foundation.tracer.otel._HAS_OTEL", False):
            result = get_otel_tracer("test-tracer")
            assert result is None

    def test_get_tracer_success(self) -> None:
        """Test getting tracer successfully."""
        mock_tracer = Mock()

        with patch("provide.foundation.tracer.otel._HAS_OTEL", True):
            with patch("provide.foundation.tracer.otel.otel_trace") as mock_trace:
                mock_trace.get_tracer.return_value = mock_tracer

                result = get_otel_tracer("test-tracer")

                assert result == mock_tracer
                mock_trace.get_tracer.assert_called_once_with("test-tracer")

    def test_get_tracer_exception(self) -> None:
        """Test getting tracer when an exception occurs."""
        with patch("provide.foundation.tracer.otel._HAS_OTEL", True):
            with patch("provide.foundation.tracer.otel.otel_trace") as mock_trace:
                mock_trace.get_tracer.side_effect = Exception("Tracer error")

                result = get_otel_tracer("test-tracer")

                assert result is None


class TestShutdownOpentelemetry:
    """Test shutdown_opentelemetry function."""

    def test_shutdown_otel_not_available(self) -> None:
        """Test shutdown when OpenTelemetry is not available."""
        with patch("provide.foundation.tracer.otel._HAS_OTEL", False):
            # Should not raise
            shutdown_opentelemetry()

    def test_shutdown_success(self) -> None:
        """Test successful shutdown."""
        mock_tracer_provider = Mock()
        mock_tracer_provider.shutdown = Mock()

        with patch("provide.foundation.tracer.otel._HAS_OTEL", True):
            with patch("provide.foundation.tracer.otel.otel_trace") as mock_trace:
                with patch("provide.foundation.tracer.otel.slog") as mock_log:
                    mock_trace.get_tracer_provider.return_value = mock_tracer_provider

                    shutdown_opentelemetry()

                    mock_tracer_provider.shutdown.assert_called_once()
                    mock_log.debug.assert_called_once_with("🔍🛑 OpenTelemetry tracer provider shutdown")

    def test_shutdown_no_shutdown_method(self) -> None:
        """Test shutdown when tracer provider has no shutdown method."""
        mock_tracer_provider = Mock(spec=[])  # No shutdown method

        with patch("provide.foundation.tracer.otel._HAS_OTEL", True):
            with patch("provide.foundation.tracer.otel.otel_trace") as mock_trace:
                with patch("provide.foundation.tracer.otel.slog") as mock_log:
                    mock_trace.get_tracer_provider.return_value = mock_tracer_provider

                    shutdown_opentelemetry()

                    # Should not crash, no debug message should be logged
                    mock_log.debug.assert_not_called()

    def test_shutdown_exception(self) -> None:
        """Test shutdown when an exception occurs."""
        with patch("provide.foundation.tracer.otel._HAS_OTEL", True):
            with patch("provide.foundation.tracer.otel.otel_trace") as mock_trace:
                with patch("provide.foundation.tracer.otel.slog") as mock_log:
                    mock_trace.get_tracer_provider.side_effect = Exception("Shutdown error")

                    shutdown_opentelemetry()

                    mock_log.warning.assert_called_once_with(
                        "⚠️ Error shutting down OpenTelemetry: Shutdown error"
                    )


class TestModuleFeatureDetection:
    """Test module-level feature detection."""

    def test_has_otel_detection(self) -> None:
        """Test that _HAS_OTEL is properly detected."""
        # This test verifies the current state - in our test environment,
        # OpenTelemetry might or might not be installed
        assert isinstance(_HAS_OTEL, bool)

    def test_import_stubs_when_otel_missing(self) -> None:
        """Test that import stubs are created when OpenTelemetry is missing."""
        # Simulate missing OpenTelemetry by temporarily removing modules
        original_modules = {}
        otel_modules = [
            "opentelemetry",
            "opentelemetry.trace",
            "opentelemetry.exporter.otlp.proto.grpc.trace_exporter",
            "opentelemetry.exporter.otlp.proto.http.trace_exporter",
            "opentelemetry.sdk.resources",
            "opentelemetry.sdk.trace",
            "opentelemetry.sdk.trace.export",
            "opentelemetry.sdk.trace.sampling",
        ]

        # Remove OpenTelemetry modules temporarily
        for module in otel_modules:
            if module in sys.modules:
                original_modules[module] = sys.modules[module]
                del sys.modules[module]

        try:
            # Force re-import to trigger the ImportError path
            import importlib

            import provide.foundation.tracer.otel as otel_module

            importlib.reload(otel_module)

            # If we reach here and _HAS_OTEL is False, verify stubs are None
            if not otel_module._HAS_OTEL:
                assert otel_module.otel_trace is None
                assert otel_module.TracerProvider is None
                assert otel_module.BatchSpanProcessor is None
                assert otel_module.Resource is None
                assert otel_module.OTLPGrpcSpanExporter is None
                assert otel_module.OTLPHttpSpanExporter is None
                assert otel_module.TraceIdRatioBased is None
        finally:
            # Restore original modules
            for module, original in original_modules.items():
                sys.modules[module] = original

            # Reload the module again to restore its original state
            import provide.foundation.tracer.otel as otel_module

            importlib.reload(otel_module)


class TestIntegration:
    """Integration tests for the otel module."""

    def test_full_otel_workflow_with_mocks(self) -> None:
        """Test complete OpenTelemetry workflow with mocked dependencies."""
        config = Mock()
        config.tracing_enabled = True
        config.globally_disabled = False
        config.service_name = "integration-test"
        config.service_version = "1.0.0"
        config.trace_sample_rate = 0.1
        config.otlp_endpoint = "http://localhost:4317"
        config.otlp_traces_endpoint = None
        config.otlp_protocol = "grpc"
        config.get_otlp_headers_dict.return_value = {"authorization": "Bearer test-token"}

        with patch("provide.foundation.tracer.otel._HAS_OTEL", True):
            with patch("provide.foundation.tracer.otel.Resource") as mock_resource_class:
                with patch("provide.foundation.tracer.otel.TraceIdRatioBased") as mock_sampler_class:
                    with patch("provide.foundation.tracer.otel.TracerProvider") as mock_provider_class:
                        with patch(
                            "provide.foundation.tracer.otel.OTLPGrpcSpanExporter"
                        ) as mock_exporter_class:
                            with patch(
                                "provide.foundation.tracer.otel.BatchSpanProcessor"
                            ) as mock_processor_class:
                                with patch("provide.foundation.tracer.otel.otel_trace") as mock_trace:
                                    # Setup mocks
                                    mock_resource = Mock()
                                    mock_sampler = Mock()
                                    mock_tracer_provider = Mock()
                                    mock_exporter = Mock()
                                    mock_processor = Mock()
                                    mock_tracer = Mock()

                                    mock_resource_class.create.return_value = mock_resource
                                    mock_sampler_class.return_value = mock_sampler
                                    mock_provider_class.return_value = mock_tracer_provider
                                    mock_exporter_class.return_value = mock_exporter
                                    mock_processor_class.return_value = mock_processor
                                    mock_trace.get_tracer.return_value = mock_tracer
                                    mock_trace.get_tracer_provider.return_value = mock_tracer_provider

                                    # Test setup
                                    setup_opentelemetry_tracing(config)

                                    # Test getting tracer
                                    tracer = get_otel_tracer("test-integration")
                                    assert tracer == mock_tracer

                                    # Test shutdown
                                    shutdown_opentelemetry()
                                    mock_tracer_provider.shutdown.assert_called_once()

    def test_graceful_handling_without_otel(self) -> None:
        """Test that all functions handle missing OpenTelemetry gracefully."""
        config = Mock()
        config.tracing_enabled = True
        config.globally_disabled = False

        with patch("provide.foundation.tracer.otel._HAS_OTEL", False):
            # All these should work without error
            setup_opentelemetry_tracing(config)

            tracer = get_otel_tracer("test")
            assert tracer is None

            shutdown_opentelemetry()

            # _require_otel should raise
            with pytest.raises(ImportError):
                _require_otel()
