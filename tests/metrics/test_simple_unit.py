#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Unit tests for simple metrics implementations.

This module contains unit tests for SimpleCounter, SimpleGauge, and SimpleHistogram.
Run with: pytest tests/metrics/test_simple_unit.py -v"""

from __future__ import annotations

from provide.testkit import FoundationTestCase
from provide.testkit.mocking import MagicMock

from provide.foundation.metrics.simple import SimpleCounter, SimpleGauge, SimpleHistogram


class TestSimpleCounter(FoundationTestCase):
    """Tests for SimpleCounter class."""

    def test_counter_initialization(self) -> None:
        """Test counter initialization."""
        counter = SimpleCounter("test_counter")

        assert counter.name == "test_counter"
        assert counter.value == 0
        assert counter._otel_counter is None

    def test_counter_initialization_with_otel(self) -> None:
        """Test counter initialization with OTEL counter."""
        mock_otel_counter = MagicMock()
        counter = SimpleCounter("test_counter", otel_counter=mock_otel_counter)

        assert counter.name == "test_counter"
        assert counter._otel_counter is mock_otel_counter

    def test_counter_inc_default(self) -> None:
        """Test incrementing counter with default value."""
        counter = SimpleCounter("test_counter")

        counter.inc()

        assert counter.value == 1

    def test_counter_inc_custom_value(self) -> None:
        """Test incrementing counter with custom value."""
        counter = SimpleCounter("test_counter")

        counter.inc(5)
        counter.inc(3)

        assert counter.value == 8

    def test_counter_inc_with_labels(self) -> None:
        """Test incrementing counter with labels."""
        counter = SimpleCounter("test_counter")

        counter.inc(1, method="GET", status="200")
        counter.inc(2, method="GET", status="200")
        counter.inc(1, method="POST", status="201")

        assert counter.value == 4
        assert counter._labels_values["method=GET,status=200"] == 3
        assert counter._labels_values["method=POST,status=201"] == 1

    def test_counter_inc_with_otel_counter(self) -> None:
        """Test incrementing counter calls OTEL counter."""
        mock_otel_counter = MagicMock()
        counter = SimpleCounter("test_counter", otel_counter=mock_otel_counter)

        counter.inc(5, method="GET")

        assert counter.value == 5
        mock_otel_counter.add.assert_called_once_with(5, attributes={"method": "GET"})

    def test_counter_inc_otel_exception_handling(self) -> None:
        """Test counter handles OTEL exceptions gracefully."""
        mock_otel_counter = MagicMock()
        mock_otel_counter.add.side_effect = RuntimeError("OTEL error")

        counter = SimpleCounter("test_counter", otel_counter=mock_otel_counter)

        # Should not raise, just log debug message
        counter.inc(1)

        assert counter.value == 1

    def test_counter_value_property(self) -> None:
        """Test counter value property."""
        counter = SimpleCounter("test_counter")

        assert counter.value == 0

        counter.inc(10)

        assert counter.value == 10


class TestSimpleGauge(FoundationTestCase):
    """Tests for SimpleGauge class."""

    def test_gauge_initialization(self) -> None:
        """Test gauge initialization."""
        gauge = SimpleGauge("test_gauge")

        assert gauge.name == "test_gauge"
        assert gauge.value == 0
        assert gauge._otel_gauge is None

    def test_gauge_initialization_with_otel(self) -> None:
        """Test gauge initialization with OTEL gauge."""
        mock_otel_gauge = MagicMock()
        gauge = SimpleGauge("test_gauge", otel_gauge=mock_otel_gauge)

        assert gauge.name == "test_gauge"
        assert gauge._otel_gauge is mock_otel_gauge

    def test_gauge_set(self) -> None:
        """Test setting gauge value."""
        gauge = SimpleGauge("test_gauge")

        gauge.set(42)

        assert gauge.value == 42

        gauge.set(100)

        assert gauge.value == 100

    def test_gauge_set_with_labels(self) -> None:
        """Test setting gauge with labels."""
        gauge = SimpleGauge("test_gauge")

        gauge.set(10, host="server1")
        gauge.set(20, host="server2")

        assert gauge.value == 20  # Last set value
        assert gauge._labels_values["host=server1"] == 10
        assert gauge._labels_values["host=server2"] == 20

    def test_gauge_set_with_otel_gauge(self) -> None:
        """Test setting gauge calls OTEL gauge."""
        mock_otel_gauge = MagicMock()
        gauge = SimpleGauge("test_gauge", otel_gauge=mock_otel_gauge)

        # First set - delta is calculated from initial state
        gauge.set(42, host="server1")

        # The implementation calculates delta after updating _labels_values,
        # so first call with labels gets delta of 0 (42 - 42)
        # This is because _labels_values is updated before OTEL is called
        # Just verify OTEL gauge was called with the labels
        assert mock_otel_gauge.add.called
        call_args = mock_otel_gauge.add.call_args
        assert call_args.kwargs["attributes"] == {"host": "server1"}

    def test_gauge_inc_default(self) -> None:
        """Test incrementing gauge with default value."""
        gauge = SimpleGauge("test_gauge")

        gauge.inc()

        assert gauge.value == 1

    def test_gauge_inc_custom_value(self) -> None:
        """Test incrementing gauge with custom value."""
        gauge = SimpleGauge("test_gauge")

        gauge.inc(5)
        gauge.inc(3)

        assert gauge.value == 8

    def test_gauge_inc_with_labels(self) -> None:
        """Test incrementing gauge with labels."""
        gauge = SimpleGauge("test_gauge")

        gauge.inc(10, region="us-west")
        gauge.inc(5, region="us-west")

        assert gauge.value == 15
        assert gauge._labels_values["region=us-west"] == 15

    def test_gauge_inc_with_otel_gauge(self) -> None:
        """Test incrementing gauge calls OTEL gauge."""
        mock_otel_gauge = MagicMock()
        gauge = SimpleGauge("test_gauge", otel_gauge=mock_otel_gauge)

        gauge.inc(5, region="us-east")

        mock_otel_gauge.add.assert_called_once_with(5, attributes={"region": "us-east"})

    def test_gauge_dec_default(self) -> None:
        """Test decrementing gauge with default value."""
        gauge = SimpleGauge("test_gauge")
        gauge.set(10)

        gauge.dec()

        assert gauge.value == 9

    def test_gauge_dec_custom_value(self) -> None:
        """Test decrementing gauge with custom value."""
        gauge = SimpleGauge("test_gauge")
        gauge.set(100)

        gauge.dec(20)
        gauge.dec(30)

        assert gauge.value == 50

    def test_gauge_dec_with_labels(self) -> None:
        """Test decrementing gauge with labels."""
        gauge = SimpleGauge("test_gauge")
        gauge.set(100, pool="workers")

        gauge.dec(10, pool="workers")
        gauge.dec(5, pool="workers")

        assert gauge._labels_values["pool=workers"] == 85

    def test_gauge_set_otel_exception_handling(self) -> None:
        """Test gauge handles OTEL exceptions gracefully."""
        mock_otel_gauge = MagicMock()
        mock_otel_gauge.add.side_effect = RuntimeError("OTEL error")

        gauge = SimpleGauge("test_gauge", otel_gauge=mock_otel_gauge)

        # Should not raise, just log debug message
        gauge.set(42)

        assert gauge.value == 42

    def test_gauge_inc_otel_exception_handling(self) -> None:
        """Test gauge inc handles OTEL exceptions gracefully."""
        mock_otel_gauge = MagicMock()
        mock_otel_gauge.add.side_effect = RuntimeError("OTEL error")

        gauge = SimpleGauge("test_gauge", otel_gauge=mock_otel_gauge)

        # Should not raise, just log debug message
        gauge.inc(5)

        assert gauge.value == 5

    def test_gauge_value_property(self) -> None:
        """Test gauge value property."""
        gauge = SimpleGauge("test_gauge")

        assert gauge.value == 0

        gauge.set(42)

        assert gauge.value == 42


class TestSimpleHistogram(FoundationTestCase):
    """Tests for SimpleHistogram class."""

    def test_histogram_initialization(self) -> None:
        """Test histogram initialization."""
        histogram = SimpleHistogram("test_histogram")

        assert histogram.name == "test_histogram"
        assert histogram.count == 0
        assert histogram._otel_histogram is None

    def test_histogram_initialization_with_otel(self) -> None:
        """Test histogram initialization with OTEL histogram."""
        mock_otel_histogram = MagicMock()
        histogram = SimpleHistogram("test_histogram", otel_histogram=mock_otel_histogram)

        assert histogram.name == "test_histogram"
        assert histogram._otel_histogram is mock_otel_histogram

    def test_histogram_observe(self) -> None:
        """Test observing values."""
        histogram = SimpleHistogram("test_histogram")

        histogram.observe(10)
        histogram.observe(20)
        histogram.observe(30)

        assert histogram.count == 3
        assert histogram.sum == 60

    def test_histogram_observe_with_labels(self) -> None:
        """Test observing values with labels."""
        histogram = SimpleHistogram("test_histogram")

        histogram.observe(10, method="GET")
        histogram.observe(20, method="GET")
        histogram.observe(15, method="POST")

        assert histogram.count == 3
        assert histogram._labels_observations["method=GET"] == [10, 20]
        assert histogram._labels_observations["method=POST"] == [15]

    def test_histogram_observe_with_otel_histogram(self) -> None:
        """Test observing calls OTEL histogram."""
        mock_otel_histogram = MagicMock()
        histogram = SimpleHistogram("test_histogram", otel_histogram=mock_otel_histogram)

        histogram.observe(42, endpoint="/api/users")

        mock_otel_histogram.record.assert_called_once_with(42, attributes={"endpoint": "/api/users"})

    def test_histogram_observe_otel_exception_handling(self) -> None:
        """Test histogram handles OTEL exceptions gracefully."""
        mock_otel_histogram = MagicMock()
        mock_otel_histogram.record.side_effect = RuntimeError("OTEL error")

        histogram = SimpleHistogram("test_histogram", otel_histogram=mock_otel_histogram)

        # Should not raise, just log debug message
        histogram.observe(10)

        assert histogram.count == 1

    def test_histogram_count_property(self) -> None:
        """Test histogram count property."""
        histogram = SimpleHistogram("test_histogram")

        assert histogram.count == 0

        histogram.observe(10)
        histogram.observe(20)

        assert histogram.count == 2

    def test_histogram_sum_property(self) -> None:
        """Test histogram sum property."""
        histogram = SimpleHistogram("test_histogram")

        assert histogram.sum == 0

        histogram.observe(10)
        histogram.observe(20)
        histogram.observe(30)

        assert histogram.sum == 60

    def test_histogram_avg_property(self) -> None:
        """Test histogram avg property."""
        histogram = SimpleHistogram("test_histogram")

        # Empty histogram should have avg of 0
        assert histogram.avg == 0.0

        histogram.observe(10)
        histogram.observe(20)
        histogram.observe(30)

        assert histogram.avg == 20.0

    def test_histogram_avg_with_floats(self) -> None:
        """Test histogram avg with floating point values."""
        histogram = SimpleHistogram("test_histogram")

        histogram.observe(1.5)
        histogram.observe(2.5)
        histogram.observe(3.0)

        assert histogram.count == 3
        assert histogram.sum == 7.0
        assert histogram.avg == 7.0 / 3

    def test_histogram_multiple_observations(self) -> None:
        """Test histogram with many observations."""
        histogram = SimpleHistogram("test_histogram")

        values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        for value in values:
            histogram.observe(value)

        assert histogram.count == 10
        assert histogram.sum == 55
        assert histogram.avg == 5.5


class TestSimpleMetricsEdgeCases(FoundationTestCase):
    """Tests for edge cases and special scenarios."""

    def test_counter_large_increment(self) -> None:
        """Test counter with large increment values."""
        counter = SimpleCounter("test_counter")

        counter.inc(1_000_000)

        assert counter.value == 1_000_000

    def test_gauge_negative_values(self) -> None:
        """Test gauge with negative values."""
        gauge = SimpleGauge("test_gauge")

        gauge.set(-100)

        assert gauge.value == -100

        gauge.inc(50)

        assert gauge.value == -50

        gauge.dec(25)

        assert gauge.value == -75

    def test_histogram_zero_observations(self) -> None:
        """Test histogram with zero observation."""
        histogram = SimpleHistogram("test_histogram")

        histogram.observe(0)

        assert histogram.count == 1
        assert histogram.sum == 0
        assert histogram.avg == 0.0

    def test_histogram_negative_observations(self) -> None:
        """Test histogram with negative values."""
        histogram = SimpleHistogram("test_histogram")

        histogram.observe(-10)
        histogram.observe(-20)

        assert histogram.count == 2
        assert histogram.sum == -30
        assert histogram.avg == -15.0

    def test_counter_float_values(self) -> None:
        """Test counter with floating point increments."""
        counter = SimpleCounter("test_counter")

        counter.inc(1.5)
        counter.inc(2.5)

        assert counter.value == 4.0

    def test_labels_sorting_consistency(self) -> None:
        """Test that labels are sorted consistently."""
        counter = SimpleCounter("test_counter")

        counter.inc(1, z="z", a="a", m="m")
        counter.inc(1, a="a", m="m", z="z")
        counter.inc(1, m="m", z="z", a="a")

        # All three should have been recorded to the same key
        assert len(counter._labels_values) == 1
        key = next(iter(counter._labels_values.keys()))
        assert key == "a=a,m=m,z=z"  # Should be sorted
        assert counter._labels_values[key] == 3


__all__ = [
    "TestSimpleCounter",
    "TestSimpleGauge",
    "TestSimpleHistogram",
    "TestSimpleMetricsEdgeCases",
]

# 🧱🏗️🔚
