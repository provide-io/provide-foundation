#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from __future__ import annotations

from collections import defaultdict
from typing import Any

from provide.foundation.logger import get_logger

"""Simple metrics implementations that work with or without OpenTelemetry."""

log = get_logger(__name__)


class SimpleCounter:
    """Counter metric that increments monotonically."""

    def __init__(self, name: str, otel_counter: Any | None = None) -> None:
        self.name = name
        self._otel_counter = otel_counter
        self._value: float = 0
        self._labels_values: dict[str, float] = defaultdict(float)

    def inc(self, value: float = 1, **labels: Any) -> None:
        """Increment the counter.

        Args:
            value: Amount to increment by (default: 1)
            **labels: Label key-value pairs

        """
        self._value += value

        # Track per-label values for simple mode
        if labels:
            labels_key = ",".join(f"{k}={v}" for k, v in sorted(labels.items()))
            self._labels_values[labels_key] += value

        # Use OpenTelemetry counter if available
        if self._otel_counter:
            try:
                self._otel_counter.add(value, attributes=labels)
            except Exception as e:
                log.debug(f"📊⚠️ Failed to record OpenTelemetry counter: {e}")

    @property
    def value(self) -> float:
        """Get the current counter value."""
        return self._value


class SimpleGauge:
    """Gauge metric that can go up or down."""

    def __init__(self, name: str, otel_gauge: Any | None = None) -> None:
        self.name = name
        self._otel_gauge = otel_gauge
        self._value: float = 0
        self._labels_values: dict[str, float] = defaultdict(float)

    def set(self, value: float, **labels: Any) -> None:
        """Set the gauge value.

        Args:
            value: Value to set
            **labels: Label key-value pairs

        """
        self._value = value

        # Track per-label values for simple mode
        if labels:
            labels_key = ",".join(f"{k}={v}" for k, v in sorted(labels.items()))
            self._labels_values[labels_key] = value

        # Use OpenTelemetry gauge if available
        if self._otel_gauge:
            try:
                self._otel_gauge.add(
                    value
                    - self._labels_values.get(
                        ",".join(f"{k}={v}" for k, v in sorted(labels.items())) if labels else "",
                        0,
                    ),
                    attributes=labels,
                )
            except Exception as e:
                log.debug(f"📊⚠️ Failed to record OpenTelemetry gauge: {e}")

    def inc(self, value: float = 1, **labels: Any) -> None:
        """Increment the gauge value.

        Args:
            value: Amount to increment by
            **labels: Label key-value pairs

        """
        self._value += value

        if labels:
            labels_key = ",".join(f"{k}={v}" for k, v in sorted(labels.items()))
            self._labels_values[labels_key] += value

        if self._otel_gauge:
            try:
                self._otel_gauge.add(value, attributes=labels)
            except Exception as e:
                log.debug(f"📊⚠️ Failed to increment OpenTelemetry gauge: {e}")

    def dec(self, value: float = 1, **labels: Any) -> None:
        """Decrement the gauge value.

        Args:
            value: Amount to decrement by
            **labels: Label key-value pairs

        """
        self.inc(-value, **labels)

    @property
    def value(self) -> float:
        """Get the current gauge value."""
        return self._value


class SimpleHistogram:
    """Histogram metric for recording distributions of values."""

    def __init__(self, name: str, otel_histogram: Any | None = None) -> None:
        self.name = name
        self._otel_histogram = otel_histogram
        self._observations: list[float] = []
        self._labels_observations: dict[str, list[float]] = defaultdict(list)

    def observe(self, value: float, **labels: Any) -> None:
        """Record an observation.

        Args:
            value: Value to observe
            **labels: Label key-value pairs

        """
        self._observations.append(value)

        # Track per-label observations for simple mode
        if labels:
            labels_key = ",".join(f"{k}={v}" for k, v in sorted(labels.items()))
            self._labels_observations[labels_key].append(value)

        # Use OpenTelemetry histogram if available
        if self._otel_histogram:
            try:
                self._otel_histogram.record(value, attributes=labels)
            except Exception as e:
                log.debug(f"📊⚠️ Failed to record OpenTelemetry histogram: {e}")

    @property
    def count(self) -> int:
        """Get the number of observations."""
        return len(self._observations)

    @property
    def sum(self) -> float:
        """Get the sum of all observations."""
        return sum(self._observations)

    @property
    def avg(self) -> float:
        """Get the average of all observations."""
        if not self._observations:
            return 0.0
        return self.sum / self.count


# 🧱🏗️🔚
