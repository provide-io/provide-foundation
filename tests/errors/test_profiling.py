#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Unit tests for errors/profiling.py.

This module contains comprehensive tests for profiling-related exception classes.
Run with: pytest tests/errors/test_profiling.py -v"""

from __future__ import annotations

from provide.testkit import FoundationTestCase
import pytest

from provide.foundation.errors.profiling import (
    ExporterError,
    MetricsError,
    ProfilingError,
    SamplingError,
)


class TestProfilingError(FoundationTestCase):
    """Tests for ProfilingError exception class."""

    def test_profiling_error_basic(self) -> None:
        """Test basic ProfilingError creation."""
        error = ProfilingError("Test profiling error")
        assert str(error) == "Test profiling error"
        assert error.code == "PROFILING_ERROR"

    def test_profiling_error_with_component(self) -> None:
        """Test ProfilingError with component context."""
        error = ProfilingError("Profiling failed", component="cpu_profiler")
        assert "profiling.component" in error.context
        assert error.context["profiling.component"] == "cpu_profiler"

    def test_profiling_error_with_sample_rate(self) -> None:
        """Test ProfilingError with sample rate context."""
        error = ProfilingError("Invalid sample rate", sample_rate=0.75)
        assert "profiling.sample_rate" in error.context
        assert error.context["profiling.sample_rate"] == 0.75

    def test_profiling_error_with_all_params(self) -> None:
        """Test ProfilingError with all parameters."""
        error = ProfilingError(
            "Comprehensive error",
            component="memory_profiler",
            sample_rate=0.5,
        )
        assert error.context["profiling.component"] == "memory_profiler"
        assert error.context["profiling.sample_rate"] == 0.5

    def test_profiling_error_with_additional_context(self) -> None:
        """Test ProfilingError with additional context."""
        error = ProfilingError(
            "Error with extra context",
            component="profiler",
            context={"extra_key": "extra_value"},
        )
        assert error.context["profiling.component"] == "profiler"
        assert error.context["extra_key"] == "extra_value"

    def test_profiling_error_default_code(self) -> None:
        """Test ProfilingError has correct default code."""
        error = ProfilingError("Test")
        assert error._default_code() == "PROFILING_ERROR"

    def test_profiling_error_with_zero_sample_rate(self) -> None:
        """Test ProfilingError handles zero sample rate."""
        error = ProfilingError("Zero rate", sample_rate=0.0)
        assert error.context["profiling.sample_rate"] == 0.0

    def test_profiling_error_with_negative_sample_rate(self) -> None:
        """Test ProfilingError accepts negative sample rate."""
        error = ProfilingError("Negative rate", sample_rate=-1.0)
        assert error.context["profiling.sample_rate"] == -1.0


class TestSamplingError(FoundationTestCase):
    """Tests for SamplingError exception class."""

    def test_sampling_error_basic(self) -> None:
        """Test basic SamplingError creation."""
        error = SamplingError("Sampling failed")
        assert str(error) == "Sampling failed"
        assert error.code == "SAMPLING_ERROR"

    def test_sampling_error_with_sample_rate(self) -> None:
        """Test SamplingError with sample rate."""
        error = SamplingError("Invalid rate", sample_rate=1.5)
        assert "sampling.rate" in error.context
        assert error.context["sampling.rate"] == 1.5

    def test_sampling_error_with_samples_processed(self) -> None:
        """Test SamplingError with samples processed count."""
        error = SamplingError("Buffer overflow", samples_processed=10000)
        assert "sampling.processed" in error.context
        assert error.context["sampling.processed"] == 10000

    def test_sampling_error_with_all_params(self) -> None:
        """Test SamplingError with all parameters."""
        error = SamplingError(
            "Sampling issue",
            sample_rate=0.25,
            samples_processed=500,
        )
        assert error.context["sampling.rate"] == 0.25
        assert error.context["sampling.processed"] == 500

    def test_sampling_error_default_code(self) -> None:
        """Test SamplingError has correct default code."""
        error = SamplingError("Test")
        assert error._default_code() == "SAMPLING_ERROR"

    def test_sampling_error_inherits_from_profiling_error(self) -> None:
        """Test SamplingError is a subclass of ProfilingError."""
        error = SamplingError("Test")
        assert isinstance(error, ProfilingError)

    def test_sampling_error_with_zero_samples(self) -> None:
        """Test SamplingError with zero samples processed."""
        error = SamplingError("No samples", samples_processed=0)
        assert error.context["sampling.processed"] == 0

    def test_sampling_error_with_component(self) -> None:
        """Test SamplingError can use component from parent."""
        error = SamplingError("Test", component="sampler", sample_rate=0.5)
        assert error.context["profiling.component"] == "sampler"
        assert error.context["sampling.rate"] == 0.5


class TestExporterError(FoundationTestCase):
    """Tests for ExporterError exception class."""

    def test_exporter_error_basic(self) -> None:
        """Test basic ExporterError creation."""
        error = ExporterError("Export failed")
        assert str(error) == "Export failed"
        assert error.code == "EXPORTER_ERROR"

    def test_exporter_error_with_exporter_name(self) -> None:
        """Test ExporterError with exporter name."""
        error = ExporterError("Failed to export", exporter_name="prometheus")
        assert "exporter.name" in error.context
        assert error.context["exporter.name"] == "prometheus"

    def test_exporter_error_with_endpoint(self) -> None:
        """Test ExporterError with endpoint."""
        error = ExporterError("Connection failed", endpoint="http://localhost:9090")
        assert "exporter.endpoint" in error.context
        assert error.context["exporter.endpoint"] == "http://localhost:9090"

    def test_exporter_error_with_retry_count(self) -> None:
        """Test ExporterError with retry count."""
        error = ExporterError("Max retries exceeded", retry_count=3)
        assert "exporter.retry_count" in error.context
        assert error.context["exporter.retry_count"] == 3

    def test_exporter_error_with_all_params(self) -> None:
        """Test ExporterError with all parameters."""
        error = ExporterError(
            "Export timeout",
            exporter_name="datadog",
            endpoint="https://api.datadoghq.com",
            retry_count=5,
        )
        assert error.context["exporter.name"] == "datadog"
        assert error.context["exporter.endpoint"] == "https://api.datadoghq.com"
        assert error.context["exporter.retry_count"] == 5

    def test_exporter_error_default_code(self) -> None:
        """Test ExporterError has correct default code."""
        error = ExporterError("Test")
        assert error._default_code() == "EXPORTER_ERROR"

    def test_exporter_error_inherits_from_profiling_error(self) -> None:
        """Test ExporterError is a subclass of ProfilingError."""
        error = ExporterError("Test")
        assert isinstance(error, ProfilingError)

    def test_exporter_error_with_zero_retries(self) -> None:
        """Test ExporterError with zero retries."""
        error = ExporterError("Failed immediately", retry_count=0)
        assert error.context["exporter.retry_count"] == 0


class TestMetricsError(FoundationTestCase):
    """Tests for MetricsError exception class."""

    def test_metrics_error_basic(self) -> None:
        """Test basic MetricsError creation."""
        error = MetricsError("Metrics collection failed")
        assert str(error) == "Metrics collection failed"
        assert error.code == "METRICS_ERROR"

    def test_metrics_error_with_metric_name(self) -> None:
        """Test MetricsError with metric name."""
        error = MetricsError("Invalid metric", metric_name="latency_ms")
        assert "metrics.name" in error.context
        assert error.context["metrics.name"] == "latency_ms"

    def test_metrics_error_with_metric_value(self) -> None:
        """Test MetricsError with metric value."""
        error = MetricsError("Value out of range", metric_value=999999)
        assert "metrics.value" in error.context
        assert error.context["metrics.value"] == 999999

    def test_metrics_error_with_all_params(self) -> None:
        """Test MetricsError with all parameters."""
        error = MetricsError(
            "Metric overflow",
            metric_name="request_count",
            metric_value=1000000,
        )
        assert error.context["metrics.name"] == "request_count"
        assert error.context["metrics.value"] == 1000000

    def test_metrics_error_default_code(self) -> None:
        """Test MetricsError has correct default code."""
        error = MetricsError("Test")
        assert error._default_code() == "METRICS_ERROR"

    def test_metrics_error_inherits_from_profiling_error(self) -> None:
        """Test MetricsError is a subclass of ProfilingError."""
        error = MetricsError("Test")
        assert isinstance(error, ProfilingError)

    def test_metrics_error_with_none_metric_value(self) -> None:
        """Test MetricsError with None metric value."""
        # None should not be added to context (only if not None)
        error = MetricsError("Missing value", metric_value=None)
        assert "metrics.value" not in error.context

    def test_metrics_error_with_zero_value(self) -> None:
        """Test MetricsError with zero metric value."""
        error = MetricsError("Zero value", metric_value=0)
        assert error.context["metrics.value"] == 0

    def test_metrics_error_with_negative_value(self) -> None:
        """Test MetricsError with negative metric value."""
        error = MetricsError("Negative value", metric_value=-100)
        assert error.context["metrics.value"] == -100

    def test_metrics_error_with_float_value(self) -> None:
        """Test MetricsError with float metric value."""
        error = MetricsError("Float value", metric_value=123.45)
        assert error.context["metrics.value"] == 123.45

    def test_metrics_error_with_string_value(self) -> None:
        """Test MetricsError with string metric value."""
        error = MetricsError("String value", metric_value="invalid")
        assert error.context["metrics.value"] == "invalid"


class TestProfilingErrorExceptionHierarchy(FoundationTestCase):
    """Tests for exception hierarchy and catching."""

    def test_catch_profiling_error_base(self) -> None:
        """Test catching all profiling errors via base class."""
        with pytest.raises(ProfilingError):
            raise SamplingError("Test")

        with pytest.raises(ProfilingError):
            raise ExporterError("Test")

        with pytest.raises(ProfilingError):
            raise MetricsError("Test")

    def test_specific_error_catching(self) -> None:
        """Test catching specific error types."""
        with pytest.raises(SamplingError):
            raise SamplingError("Test")

        with pytest.raises(ExporterError):
            raise ExporterError("Test")

        with pytest.raises(MetricsError):
            raise MetricsError("Test")

    def test_error_context_preservation(self) -> None:
        """Test that error context is preserved when caught."""
        try:
            raise MetricsError("Test", metric_name="test_metric", metric_value=100)
        except ProfilingError as e:
            # Should be catchable as ProfilingError
            assert isinstance(e, MetricsError)
            assert e.context["metrics.name"] == "test_metric"
            assert e.context["metrics.value"] == 100


__all__ = [
    "TestExporterError",
    "TestMetricsError",
    "TestProfilingError",
    "TestProfilingErrorExceptionHierarchy",
    "TestSamplingError",
]

# 🧱🏗️🔚
