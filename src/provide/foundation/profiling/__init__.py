#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from __future__ import annotations

from provide.foundation.errors.profiling import (
    ExporterError,
    MetricsError,
    ProfilingError,
    SamplingError,
)
from provide.foundation.profiling.component import ProfilingComponent, register_profiling
from provide.foundation.profiling.metrics import ProfileMetrics
from provide.foundation.profiling.processor import ProfilingProcessor

"""Performance profiling hooks for Foundation telemetry.

Provides lightweight metrics collection and monitoring capabilities
for Foundation's logging and telemetry infrastructure.

Example:
    >>> from provide.foundation.profiling import register_profiling
    >>> from provide.foundation.hub import Hub
    >>>
    >>> hub = Hub()
    >>> register_profiling(hub)
    >>> profiler = hub.get_component("profiler")
    >>> profiler.enable()
    >>>
    >>> # Metrics are automatically collected
    >>> metrics = profiler.get_metrics()
    >>> print(f"Processing {metrics.messages_per_second:.0f} msg/sec")

"""

__all__ = [
    "ExporterError",
    "MetricsError",
    # Core components
    "ProfileMetrics",
    "ProfilingComponent",
    # Error classes
    "ProfilingError",
    "ProfilingProcessor",
    "SamplingError",
    "register_profiling",
]

# 🧱🏗️🔚
