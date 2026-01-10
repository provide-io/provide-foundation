#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Unit tests for metrics module API.

This module contains unit tests for the metrics module API (counter, gauge, histogram).
Run with: pytest tests/metrics/test_metrics_api_unit.py -v"""

from __future__ import annotations

from provide.testkit import FoundationTestCase
from provide.testkit.mocking import MagicMock, patch


class TestCounterAPI(FoundationTestCase):
    """Tests for counter() function."""

    def test_counter_without_otel(self) -> None:
        """Test counter creation without OpenTelemetry."""
        with patch("provide.foundation.metrics._HAS_OTEL_METRICS", False):
            from provide.foundation.metrics import counter

            c = counter("test_counter")

            assert c.name == "test_counter"
            assert c._otel_counter is None

    def test_counter_with_otel_no_meter(self) -> None:
        """Test counter creation with OTEL available but no meter set."""
        with (
            patch("provide.foundation.metrics._HAS_OTEL_METRICS", True),
            patch("provide.foundation.metrics._meter", None),
        ):
            from provide.foundation.metrics import counter

            c = counter("test_counter", description="Test counter", unit="requests")

            assert c.name == "test_counter"
            assert c._otel_counter is None

    def test_counter_with_otel_and_meter(self) -> None:
        """Test counter creation with OpenTelemetry meter."""
        mock_meter = MagicMock()
        mock_otel_counter = MagicMock()
        mock_meter.create_counter.return_value = mock_otel_counter

        with (
            patch("provide.foundation.metrics._HAS_OTEL_METRICS", True),
            patch("provide.foundation.metrics._meter", mock_meter),
        ):
            from provide.foundation.metrics import counter

            c = counter("test_counter", description="Test counter", unit="requests")

            assert c.name == "test_counter"
            assert c._otel_counter is mock_otel_counter
            mock_meter.create_counter.assert_called_once_with(
                name="test_counter",
                description="Test counter",
                unit="requests",
            )

    def test_counter_otel_exception_fallback(self) -> None:
        """Test counter falls back to simple counter if OTEL fails."""
        mock_meter = MagicMock()
        mock_meter.create_counter.side_effect = RuntimeError("OTEL error")

        with (
            patch("provide.foundation.metrics._HAS_OTEL_METRICS", True),
            patch("provide.foundation.metrics._meter", mock_meter),
        ):
            from provide.foundation.metrics import counter

            c = counter("test_counter")

            # Should fall back to simple counter without OTEL
            assert c.name == "test_counter"
            assert c._otel_counter is None


class TestGaugeAPI(FoundationTestCase):
    """Tests for gauge() function."""

    def test_gauge_without_otel(self) -> None:
        """Test gauge creation without OpenTelemetry."""
        with patch("provide.foundation.metrics._HAS_OTEL_METRICS", False):
            from provide.foundation.metrics import gauge

            g = gauge("test_gauge")

            assert g.name == "test_gauge"
            assert g._otel_gauge is None

    def test_gauge_with_otel_no_meter(self) -> None:
        """Test gauge creation with OTEL available but no meter set."""
        with (
            patch("provide.foundation.metrics._HAS_OTEL_METRICS", True),
            patch("provide.foundation.metrics._meter", None),
        ):
            from provide.foundation.metrics import gauge

            g = gauge("test_gauge", description="Test gauge", unit="connections")

            assert g.name == "test_gauge"
            assert g._otel_gauge is None

    def test_gauge_with_otel_and_meter(self) -> None:
        """Test gauge creation with OpenTelemetry meter."""
        mock_meter = MagicMock()
        mock_otel_gauge = MagicMock()
        mock_meter.create_up_down_counter.return_value = mock_otel_gauge

        with (
            patch("provide.foundation.metrics._HAS_OTEL_METRICS", True),
            patch("provide.foundation.metrics._meter", mock_meter),
        ):
            from provide.foundation.metrics import gauge

            g = gauge("test_gauge", description="Test gauge", unit="connections")

            assert g.name == "test_gauge"
            assert g._otel_gauge is mock_otel_gauge
            mock_meter.create_up_down_counter.assert_called_once_with(
                name="test_gauge",
                description="Test gauge",
                unit="connections",
            )

    def test_gauge_otel_exception_fallback(self) -> None:
        """Test gauge falls back to simple gauge if OTEL fails."""
        mock_meter = MagicMock()
        mock_meter.create_up_down_counter.side_effect = RuntimeError("OTEL error")

        with (
            patch("provide.foundation.metrics._HAS_OTEL_METRICS", True),
            patch("provide.foundation.metrics._meter", mock_meter),
        ):
            from provide.foundation.metrics import gauge

            g = gauge("test_gauge")

            # Should fall back to simple gauge without OTEL
            assert g.name == "test_gauge"
            assert g._otel_gauge is None


class TestHistogramAPI(FoundationTestCase):
    """Tests for histogram() function."""

    def test_histogram_without_otel(self) -> None:
        """Test histogram creation without OpenTelemetry."""
        with patch("provide.foundation.metrics._HAS_OTEL_METRICS", False):
            from provide.foundation.metrics import histogram

            h = histogram("test_histogram")

            assert h.name == "test_histogram"
            assert h._otel_histogram is None

    def test_histogram_with_otel_no_meter(self) -> None:
        """Test histogram creation with OTEL available but no meter set."""
        with (
            patch("provide.foundation.metrics._HAS_OTEL_METRICS", True),
            patch("provide.foundation.metrics._meter", None),
        ):
            from provide.foundation.metrics import histogram

            h = histogram("test_histogram", description="Test histogram", unit="ms")

            assert h.name == "test_histogram"
            assert h._otel_histogram is None

    def test_histogram_with_otel_and_meter(self) -> None:
        """Test histogram creation with OpenTelemetry meter."""
        mock_meter = MagicMock()
        mock_otel_histogram = MagicMock()
        mock_meter.create_histogram.return_value = mock_otel_histogram

        with (
            patch("provide.foundation.metrics._HAS_OTEL_METRICS", True),
            patch("provide.foundation.metrics._meter", mock_meter),
        ):
            from provide.foundation.metrics import histogram

            h = histogram("test_histogram", description="Test histogram", unit="ms")

            assert h.name == "test_histogram"
            assert h._otel_histogram is mock_otel_histogram
            mock_meter.create_histogram.assert_called_once_with(
                name="test_histogram",
                description="Test histogram",
                unit="ms",
            )

    def test_histogram_otel_exception_fallback(self) -> None:
        """Test histogram falls back to simple histogram if OTEL fails."""
        mock_meter = MagicMock()
        mock_meter.create_histogram.side_effect = RuntimeError("OTEL error")

        with (
            patch("provide.foundation.metrics._HAS_OTEL_METRICS", True),
            patch("provide.foundation.metrics._meter", mock_meter),
        ):
            from provide.foundation.metrics import histogram

            h = histogram("test_histogram")

            # Should fall back to simple histogram without OTEL
            assert h.name == "test_histogram"
            assert h._otel_histogram is None


class TestSetMeter(FoundationTestCase):
    """Tests for _set_meter() function."""

    def test_set_meter(self) -> None:
        """Test setting global meter instance."""
        from provide.foundation.metrics import _set_meter

        mock_meter = MagicMock()

        _set_meter(mock_meter)

        # Verify the global meter was set
        import provide.foundation.metrics

        assert provide.foundation.metrics._meter is mock_meter

    def test_set_meter_none(self) -> None:
        """Test setting meter to None."""
        from provide.foundation.metrics import _set_meter

        _set_meter(None)

        # Verify the global meter was set to None
        import provide.foundation.metrics

        assert provide.foundation.metrics._meter is None


class TestModuleConstants(FoundationTestCase):
    """Tests for module-level constants and exports."""

    def test_has_otel_metrics_import_success(self) -> None:
        """Test _HAS_OTEL_METRICS when imports succeed."""
        # This test depends on whether OTEL is actually installed
        # We'll just verify the flag exists and is a boolean
        from provide.foundation.metrics import _HAS_OTEL_METRICS

        assert isinstance(_HAS_OTEL_METRICS, bool)

    def test_module_exports(self) -> None:
        """Test that module exports expected API."""
        from provide.foundation.metrics import __all__, counter, gauge, histogram

        assert "counter" in __all__
        assert "gauge" in __all__
        assert "histogram" in __all__
        assert callable(counter)
        assert callable(gauge)
        assert callable(histogram)


__all__ = [
    "TestCounterAPI",
    "TestGaugeAPI",
    "TestHistogramAPI",
    "TestModuleConstants",
    "TestSetMeter",
]

# 🧱🏗️🔚
