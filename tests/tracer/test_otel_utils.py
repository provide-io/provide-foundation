"""Tests for OpenTelemetry utilities."""

from __future__ import annotations

import sys
from unittest.mock import Mock, patch

from provide.testkit import FoundationTestCase
import pytest

# Import _HAS_OTEL and other needed components
try:
    from provide.foundation.tracer.otel import _HAS_OTEL
except ImportError:
    _HAS_OTEL = False


class TestShutdownOpentelemetry(FoundationTestCase):
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


class TestModuleFeatureDetection(FoundationTestCase):
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
