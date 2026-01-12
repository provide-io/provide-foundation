#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for OpenTelemetry utilities."""

from __future__ import annotations

import sys

from provide.testkit import FoundationTestCase
from provide.testkit.mocking import Mock, patch

# Import _HAS_OTEL and other needed components
try:
    from provide.foundation.tracer.otel import (
        _HAS_OTEL,
        get_otel_tracer,
        setup_opentelemetry_tracing,
        shutdown_opentelemetry,
    )
except ImportError:
    _HAS_OTEL = False
    get_otel_tracer = None  # type: ignore
    setup_opentelemetry_tracing = None  # type: ignore
    shutdown_opentelemetry = None  # type: ignore


class TestShutdownOpentelemetry(FoundationTestCase):
    """Test shutdown_opentelemetry function."""

    def test_shutdown_otel_not_available(self) -> None:
        """Test shutdown when OpenTelemetry is not available."""
        with patch("provide.foundation.tracer.otel._HAS_OTEL", False):
            # Should not raise, just return None
            result = shutdown_opentelemetry()
            assert result is None

    def test_shutdown_success(self) -> None:
        """Test successful shutdown."""
        with (
            patch("provide.foundation.tracer.otel._HAS_OTEL", True),
            patch("provide.foundation.tracer.otel.otel_trace") as mock_trace,
        ):
            mock_provider = Mock()
            mock_trace.get_tracer_provider.return_value = mock_provider
            shutdown_opentelemetry()
            mock_provider.shutdown.assert_called_once()

    def test_shutdown_no_shutdown_method(self) -> None:
        """Test shutdown when provider has no shutdown method."""
        with (
            patch("provide.foundation.tracer.otel._HAS_OTEL", True),
            patch("provide.foundation.tracer.otel.otel_trace") as mock_trace,
        ):
            mock_provider = Mock(spec=[])  # No shutdown method
            mock_trace.get_tracer_provider.return_value = mock_provider
            # Should not raise
            result = shutdown_opentelemetry()
            assert result is None

    def test_shutdown_exception(self) -> None:
        """Test shutdown handles exceptions gracefully."""
        with (
            patch("provide.foundation.tracer.otel._HAS_OTEL", True),
            patch("provide.foundation.tracer.otel.otel_trace") as mock_trace,
        ):
            mock_provider = Mock()
            mock_provider.shutdown.side_effect = Exception("Shutdown error")
            mock_trace.get_tracer_provider.return_value = mock_provider
            # Should not raise
            result = shutdown_opentelemetry()
            assert result is None


class TestModuleFeatureDetection(FoundationTestCase):
    """Test module-level feature detection."""

    def test_has_otel_detection(self) -> None:
        """Test that _HAS_OTEL is properly detected."""
        # This test just verifies the import works
        assert isinstance(_HAS_OTEL, bool)

    def test_import_stubs_when_otel_missing(self) -> None:
        """Test that missing OpenTelemetry imports are handled."""
        # Temporarily remove opentelemetry from sys.modules
        otel_modules = {k: v for k, v in sys.modules.items() if "opentelemetry" in k}
        for mod in otel_modules:
            del sys.modules[mod]

        # Should be able to import without error
        try:
            from provide.foundation.tracer import otel as otel_module

            assert hasattr(otel_module, "_HAS_OTEL")
        finally:
            # Restore modules
            sys.modules.update(otel_modules)


class TestIntegration:
    """Integration tests for OpenTelemetry functionality."""

    def test_full_otel_workflow_with_mocks(self) -> None:
        """Test full OpenTelemetry workflow with mocked components."""
        with (
            patch("provide.foundation.tracer.otel._HAS_OTEL", True),
            patch("provide.foundation.tracer.otel.TracerProvider") as mock_tp,
            patch("provide.foundation.tracer.otel.Resource"),
            patch("provide.foundation.tracer.otel.otel_trace") as mock_trace,
            patch("provide.foundation.tracer.otel.TraceIdRatioBased") as mock_sampler,
            patch("provide.foundation.tracer.otel.BatchSpanProcessor"),
        ):
            mock_provider = Mock()
            mock_tp.return_value = mock_provider
            mock_trace.get_tracer_provider.return_value = mock_provider
            mock_sampler.return_value = Mock()

            # Setup
            from provide.foundation.logger.config.telemetry import TelemetryConfig

            config = TelemetryConfig(service_name="test-service")
            setup_opentelemetry_tracing(config)

            # Get tracer
            tracer = get_otel_tracer("test")
            assert tracer is not None

            # Shutdown
            shutdown_opentelemetry()
            mock_provider.shutdown.assert_called_once()

    def test_graceful_handling_without_otel(self) -> None:
        """Test graceful handling when OpenTelemetry is not available."""
        with patch("provide.foundation.tracer.otel._HAS_OTEL", False):
            # Setup should not raise
            from provide.foundation.logger.config.telemetry import TelemetryConfig

            config = TelemetryConfig(service_name="test-service")
            result = setup_opentelemetry_tracing(config)
            assert result is None

            # Get tracer should return None
            tracer = get_otel_tracer("test")
            assert tracer is None

            # Shutdown should not raise
            result = shutdown_opentelemetry()
            assert result is None


# 🧱🏗️🔚
