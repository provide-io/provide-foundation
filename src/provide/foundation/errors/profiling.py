#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from __future__ import annotations

from typing import Any

from provide.foundation.errors.base import FoundationError

"""Profiling-related exceptions."""


class ProfilingError(FoundationError):
    """Raised when profiling operations fail.

    Args:
        message: Error message describing the profiling issue.
        component: Optional profiling component that caused the error.
        sample_rate: Optional sample rate when the error occurred.
        **kwargs: Additional context passed to FoundationError.

    Examples:
        >>> raise ProfilingError("Profiling initialization failed")
        >>> raise ProfilingError("Invalid sample rate", sample_rate=1.5)

    """

    def __init__(
        self,
        message: str,
        *,
        component: str | None = None,
        sample_rate: float | None = None,
        **kwargs: Any,
    ) -> None:
        if component:
            kwargs.setdefault("context", {})["profiling.component"] = component
        if sample_rate is not None:
            kwargs.setdefault("context", {})["profiling.sample_rate"] = sample_rate
        super().__init__(message, **kwargs)

    def _default_code(self) -> str:
        return "PROFILING_ERROR"


class SamplingError(ProfilingError):
    """Raised when sampling operations fail.

    Args:
        message: Sampling error message.
        sample_rate: The sample rate that caused the error.
        samples_processed: Optional number of samples processed.
        **kwargs: Additional context passed to ProfilingError.

    Examples:
        >>> raise SamplingError("Invalid sample rate", sample_rate=1.5)
        >>> raise SamplingError("Sampling buffer overflow", samples_processed=1000)

    """

    def __init__(
        self,
        message: str,
        *,
        sample_rate: float | None = None,
        samples_processed: int | None = None,
        **kwargs: Any,
    ) -> None:
        if sample_rate is not None:
            kwargs.setdefault("context", {})["sampling.rate"] = sample_rate
        if samples_processed is not None:
            kwargs.setdefault("context", {})["sampling.processed"] = samples_processed
        super().__init__(message, **kwargs)

    def _default_code(self) -> str:
        return "SAMPLING_ERROR"


class ExporterError(ProfilingError):
    """Raised when metric export operations fail.

    Args:
        message: Export error message.
        exporter_name: Optional name of the exporter that failed.
        endpoint: Optional endpoint URL that failed.
        retry_count: Optional number of retries attempted.
        **kwargs: Additional context passed to ProfilingError.

    Examples:
        >>> raise ExporterError("Failed to connect to Prometheus")
        >>> raise ExporterError("Export timeout", exporter_name="datadog", retry_count=3)

    """

    def __init__(
        self,
        message: str,
        *,
        exporter_name: str | None = None,
        endpoint: str | None = None,
        retry_count: int | None = None,
        **kwargs: Any,
    ) -> None:
        if exporter_name:
            kwargs.setdefault("context", {})["exporter.name"] = exporter_name
        if endpoint:
            kwargs.setdefault("context", {})["exporter.endpoint"] = endpoint
        if retry_count is not None:
            kwargs.setdefault("context", {})["exporter.retry_count"] = retry_count
        super().__init__(message, **kwargs)

    def _default_code(self) -> str:
        return "EXPORTER_ERROR"


class MetricsError(ProfilingError):
    """Raised when metrics collection operations fail.

    Args:
        message: Metrics error message.
        metric_name: Optional name of the metric that failed.
        metric_value: Optional value that caused the error.
        **kwargs: Additional context passed to ProfilingError.

    Examples:
        >>> raise MetricsError("Invalid metric value")
        >>> raise MetricsError("Metric overflow", metric_name="latency_ms")

    """

    def __init__(
        self,
        message: str,
        *,
        metric_name: str | None = None,
        metric_value: Any = None,
        **kwargs: Any,
    ) -> None:
        if metric_name:
            kwargs.setdefault("context", {})["metrics.name"] = metric_name
        if metric_value is not None:
            kwargs.setdefault("context", {})["metrics.value"] = metric_value
        super().__init__(message, **kwargs)

    def _default_code(self) -> str:
        return "METRICS_ERROR"


# 🧱🏗️🔚
