# provide/foundation/metrics/__init__.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from typing import Any

from provide.foundation.metrics.simple import (
    SimpleCounter,
    SimpleGauge,
    SimpleHistogram,
)

"""Foundation Metrics Module.

Provides metrics collection with optional OpenTelemetry integration.
Falls back to simple metrics when OpenTelemetry is not available.
"""

try:
    from opentelemetry import metrics as otel_metrics
    from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import (
        OTLPMetricExporter as OTLPGrpcMetricExporter,
    )
    from opentelemetry.exporter.otlp.proto.http.metric_exporter import (
        OTLPMetricExporter as OTLPHttpMetricExporter,
    )
    from opentelemetry.sdk.metrics import MeterProvider
    from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader

    _HAS_OTEL_METRICS = True
except ImportError:
    otel_metrics: Any = None  # type: ignore[no-redef]
    MeterProvider: Any = None  # type: ignore[no-redef]
    PeriodicExportingMetricReader: Any = None  # type: ignore[no-redef]
    OTLPGrpcMetricExporter: Any = None  # type: ignore[no-redef]
    OTLPHttpMetricExporter: Any = None  # type: ignore[no-redef]
    _HAS_OTEL_METRICS = False

# Export the main API
__all__ = [
    "_HAS_OTEL_METRICS",  # For internal use
    "counter",
    "gauge",
    "histogram",
]

# Global meter instance (will be set during setup)
_meter = None
from inspect import signature as _mutmut_signature
from typing import Annotated
from typing import Callable
from typing import ClassVar


MutantDict = Annotated[dict[str, Callable], "Mutant"]


def _mutmut_trampoline(orig, mutants, call_args, call_kwargs, self_arg=None):
    """Forward call to original or mutated function, depending on the environment"""
    import os

    mutant_under_test = os.environ["MUTANT_UNDER_TEST"]
    if mutant_under_test == "fail":
        from mutmut.__main__ import MutmutProgrammaticFailException

        raise MutmutProgrammaticFailException("Failed programmatically")
    elif mutant_under_test == "stats":
        from mutmut.__main__ import record_trampoline_hit

        record_trampoline_hit(orig.__module__ + "." + orig.__name__)
        result = orig(*call_args, **call_kwargs)
        return result
    prefix = orig.__module__ + "." + orig.__name__ + "__mutmut_"
    if not mutant_under_test.startswith(prefix):
        result = orig(*call_args, **call_kwargs)
        return result
    mutant_name = mutant_under_test.rpartition(".")[-1]
    if self_arg:
        # call to a class method where self is not bound
        result = mutants[mutant_name](self_arg, *call_args, **call_kwargs)
    else:
        result = mutants[mutant_name](*call_args, **call_kwargs)
    return result


def x_counter__mutmut_orig(name: str, description: str = "", unit: str = "") -> SimpleCounter:
    """Create a counter metric.

    Args:
        name: Name of the counter
        description: Description of what this counter measures
        unit: Unit of measurement

    Returns:
        Counter instance

    """
    if _HAS_OTEL_METRICS and _meter:
        try:
            otel_counter = _meter.create_counter(name=name, description=description, unit=unit)
            return SimpleCounter(name, otel_counter=otel_counter)
        except Exception:
            # Broad catch intentional: OTEL metrics are optional, gracefully fall back to simple counter
            pass

    return SimpleCounter(name)


def x_counter__mutmut_1(name: str, description: str = "XXXX", unit: str = "") -> SimpleCounter:
    """Create a counter metric.

    Args:
        name: Name of the counter
        description: Description of what this counter measures
        unit: Unit of measurement

    Returns:
        Counter instance

    """
    if _HAS_OTEL_METRICS and _meter:
        try:
            otel_counter = _meter.create_counter(name=name, description=description, unit=unit)
            return SimpleCounter(name, otel_counter=otel_counter)
        except Exception:
            # Broad catch intentional: OTEL metrics are optional, gracefully fall back to simple counter
            pass

    return SimpleCounter(name)


def x_counter__mutmut_2(name: str, description: str = "", unit: str = "XXXX") -> SimpleCounter:
    """Create a counter metric.

    Args:
        name: Name of the counter
        description: Description of what this counter measures
        unit: Unit of measurement

    Returns:
        Counter instance

    """
    if _HAS_OTEL_METRICS and _meter:
        try:
            otel_counter = _meter.create_counter(name=name, description=description, unit=unit)
            return SimpleCounter(name, otel_counter=otel_counter)
        except Exception:
            # Broad catch intentional: OTEL metrics are optional, gracefully fall back to simple counter
            pass

    return SimpleCounter(name)


def x_counter__mutmut_3(name: str, description: str = "", unit: str = "") -> SimpleCounter:
    """Create a counter metric.

    Args:
        name: Name of the counter
        description: Description of what this counter measures
        unit: Unit of measurement

    Returns:
        Counter instance

    """
    if _HAS_OTEL_METRICS or _meter:
        try:
            otel_counter = _meter.create_counter(name=name, description=description, unit=unit)
            return SimpleCounter(name, otel_counter=otel_counter)
        except Exception:
            # Broad catch intentional: OTEL metrics are optional, gracefully fall back to simple counter
            pass

    return SimpleCounter(name)


def x_counter__mutmut_4(name: str, description: str = "", unit: str = "") -> SimpleCounter:
    """Create a counter metric.

    Args:
        name: Name of the counter
        description: Description of what this counter measures
        unit: Unit of measurement

    Returns:
        Counter instance

    """
    if _HAS_OTEL_METRICS and _meter:
        try:
            otel_counter = None
            return SimpleCounter(name, otel_counter=otel_counter)
        except Exception:
            # Broad catch intentional: OTEL metrics are optional, gracefully fall back to simple counter
            pass

    return SimpleCounter(name)


def x_counter__mutmut_5(name: str, description: str = "", unit: str = "") -> SimpleCounter:
    """Create a counter metric.

    Args:
        name: Name of the counter
        description: Description of what this counter measures
        unit: Unit of measurement

    Returns:
        Counter instance

    """
    if _HAS_OTEL_METRICS and _meter:
        try:
            otel_counter = _meter.create_counter(name=None, description=description, unit=unit)
            return SimpleCounter(name, otel_counter=otel_counter)
        except Exception:
            # Broad catch intentional: OTEL metrics are optional, gracefully fall back to simple counter
            pass

    return SimpleCounter(name)


def x_counter__mutmut_6(name: str, description: str = "", unit: str = "") -> SimpleCounter:
    """Create a counter metric.

    Args:
        name: Name of the counter
        description: Description of what this counter measures
        unit: Unit of measurement

    Returns:
        Counter instance

    """
    if _HAS_OTEL_METRICS and _meter:
        try:
            otel_counter = _meter.create_counter(name=name, description=None, unit=unit)
            return SimpleCounter(name, otel_counter=otel_counter)
        except Exception:
            # Broad catch intentional: OTEL metrics are optional, gracefully fall back to simple counter
            pass

    return SimpleCounter(name)


def x_counter__mutmut_7(name: str, description: str = "", unit: str = "") -> SimpleCounter:
    """Create a counter metric.

    Args:
        name: Name of the counter
        description: Description of what this counter measures
        unit: Unit of measurement

    Returns:
        Counter instance

    """
    if _HAS_OTEL_METRICS and _meter:
        try:
            otel_counter = _meter.create_counter(name=name, description=description, unit=None)
            return SimpleCounter(name, otel_counter=otel_counter)
        except Exception:
            # Broad catch intentional: OTEL metrics are optional, gracefully fall back to simple counter
            pass

    return SimpleCounter(name)


def x_counter__mutmut_8(name: str, description: str = "", unit: str = "") -> SimpleCounter:
    """Create a counter metric.

    Args:
        name: Name of the counter
        description: Description of what this counter measures
        unit: Unit of measurement

    Returns:
        Counter instance

    """
    if _HAS_OTEL_METRICS and _meter:
        try:
            otel_counter = _meter.create_counter(description=description, unit=unit)
            return SimpleCounter(name, otel_counter=otel_counter)
        except Exception:
            # Broad catch intentional: OTEL metrics are optional, gracefully fall back to simple counter
            pass

    return SimpleCounter(name)


def x_counter__mutmut_9(name: str, description: str = "", unit: str = "") -> SimpleCounter:
    """Create a counter metric.

    Args:
        name: Name of the counter
        description: Description of what this counter measures
        unit: Unit of measurement

    Returns:
        Counter instance

    """
    if _HAS_OTEL_METRICS and _meter:
        try:
            otel_counter = _meter.create_counter(name=name, unit=unit)
            return SimpleCounter(name, otel_counter=otel_counter)
        except Exception:
            # Broad catch intentional: OTEL metrics are optional, gracefully fall back to simple counter
            pass

    return SimpleCounter(name)


def x_counter__mutmut_10(name: str, description: str = "", unit: str = "") -> SimpleCounter:
    """Create a counter metric.

    Args:
        name: Name of the counter
        description: Description of what this counter measures
        unit: Unit of measurement

    Returns:
        Counter instance

    """
    if _HAS_OTEL_METRICS and _meter:
        try:
            otel_counter = _meter.create_counter(
                name=name,
                description=description,
            )
            return SimpleCounter(name, otel_counter=otel_counter)
        except Exception:
            # Broad catch intentional: OTEL metrics are optional, gracefully fall back to simple counter
            pass

    return SimpleCounter(name)


def x_counter__mutmut_11(name: str, description: str = "", unit: str = "") -> SimpleCounter:
    """Create a counter metric.

    Args:
        name: Name of the counter
        description: Description of what this counter measures
        unit: Unit of measurement

    Returns:
        Counter instance

    """
    if _HAS_OTEL_METRICS and _meter:
        try:
            otel_counter = _meter.create_counter(name=name, description=description, unit=unit)
            return SimpleCounter(None, otel_counter=otel_counter)
        except Exception:
            # Broad catch intentional: OTEL metrics are optional, gracefully fall back to simple counter
            pass

    return SimpleCounter(name)


def x_counter__mutmut_12(name: str, description: str = "", unit: str = "") -> SimpleCounter:
    """Create a counter metric.

    Args:
        name: Name of the counter
        description: Description of what this counter measures
        unit: Unit of measurement

    Returns:
        Counter instance

    """
    if _HAS_OTEL_METRICS and _meter:
        try:
            otel_counter = _meter.create_counter(name=name, description=description, unit=unit)
            return SimpleCounter(name, otel_counter=None)
        except Exception:
            # Broad catch intentional: OTEL metrics are optional, gracefully fall back to simple counter
            pass

    return SimpleCounter(name)


def x_counter__mutmut_13(name: str, description: str = "", unit: str = "") -> SimpleCounter:
    """Create a counter metric.

    Args:
        name: Name of the counter
        description: Description of what this counter measures
        unit: Unit of measurement

    Returns:
        Counter instance

    """
    if _HAS_OTEL_METRICS and _meter:
        try:
            otel_counter = _meter.create_counter(name=name, description=description, unit=unit)
            return SimpleCounter(otel_counter=otel_counter)
        except Exception:
            # Broad catch intentional: OTEL metrics are optional, gracefully fall back to simple counter
            pass

    return SimpleCounter(name)


def x_counter__mutmut_14(name: str, description: str = "", unit: str = "") -> SimpleCounter:
    """Create a counter metric.

    Args:
        name: Name of the counter
        description: Description of what this counter measures
        unit: Unit of measurement

    Returns:
        Counter instance

    """
    if _HAS_OTEL_METRICS and _meter:
        try:
            otel_counter = _meter.create_counter(name=name, description=description, unit=unit)
            return SimpleCounter(
                name,
            )
        except Exception:
            # Broad catch intentional: OTEL metrics are optional, gracefully fall back to simple counter
            pass

    return SimpleCounter(name)


def x_counter__mutmut_15(name: str, description: str = "", unit: str = "") -> SimpleCounter:
    """Create a counter metric.

    Args:
        name: Name of the counter
        description: Description of what this counter measures
        unit: Unit of measurement

    Returns:
        Counter instance

    """
    if _HAS_OTEL_METRICS and _meter:
        try:
            otel_counter = _meter.create_counter(name=name, description=description, unit=unit)
            return SimpleCounter(name, otel_counter=otel_counter)
        except Exception:
            # Broad catch intentional: OTEL metrics are optional, gracefully fall back to simple counter
            pass

    return SimpleCounter(None)


x_counter__mutmut_mutants: ClassVar[MutantDict] = {
    "x_counter__mutmut_1": x_counter__mutmut_1,
    "x_counter__mutmut_2": x_counter__mutmut_2,
    "x_counter__mutmut_3": x_counter__mutmut_3,
    "x_counter__mutmut_4": x_counter__mutmut_4,
    "x_counter__mutmut_5": x_counter__mutmut_5,
    "x_counter__mutmut_6": x_counter__mutmut_6,
    "x_counter__mutmut_7": x_counter__mutmut_7,
    "x_counter__mutmut_8": x_counter__mutmut_8,
    "x_counter__mutmut_9": x_counter__mutmut_9,
    "x_counter__mutmut_10": x_counter__mutmut_10,
    "x_counter__mutmut_11": x_counter__mutmut_11,
    "x_counter__mutmut_12": x_counter__mutmut_12,
    "x_counter__mutmut_13": x_counter__mutmut_13,
    "x_counter__mutmut_14": x_counter__mutmut_14,
    "x_counter__mutmut_15": x_counter__mutmut_15,
}


def counter(*args, **kwargs):
    result = _mutmut_trampoline(x_counter__mutmut_orig, x_counter__mutmut_mutants, args, kwargs)
    return result


counter.__signature__ = _mutmut_signature(x_counter__mutmut_orig)
x_counter__mutmut_orig.__name__ = "x_counter"


def x_gauge__mutmut_orig(name: str, description: str = "", unit: str = "") -> SimpleGauge:
    """Create a gauge metric.

    Args:
        name: Name of the gauge
        description: Description of what this gauge measures
        unit: Unit of measurement

    Returns:
        Gauge instance

    """
    if _HAS_OTEL_METRICS and _meter:
        try:
            otel_gauge = _meter.create_up_down_counter(name=name, description=description, unit=unit)
            return SimpleGauge(name, otel_gauge=otel_gauge)
        except Exception:
            # Broad catch intentional: OTEL metrics are optional, gracefully fall back to simple gauge
            pass

    return SimpleGauge(name)


def x_gauge__mutmut_1(name: str, description: str = "XXXX", unit: str = "") -> SimpleGauge:
    """Create a gauge metric.

    Args:
        name: Name of the gauge
        description: Description of what this gauge measures
        unit: Unit of measurement

    Returns:
        Gauge instance

    """
    if _HAS_OTEL_METRICS and _meter:
        try:
            otel_gauge = _meter.create_up_down_counter(name=name, description=description, unit=unit)
            return SimpleGauge(name, otel_gauge=otel_gauge)
        except Exception:
            # Broad catch intentional: OTEL metrics are optional, gracefully fall back to simple gauge
            pass

    return SimpleGauge(name)


def x_gauge__mutmut_2(name: str, description: str = "", unit: str = "XXXX") -> SimpleGauge:
    """Create a gauge metric.

    Args:
        name: Name of the gauge
        description: Description of what this gauge measures
        unit: Unit of measurement

    Returns:
        Gauge instance

    """
    if _HAS_OTEL_METRICS and _meter:
        try:
            otel_gauge = _meter.create_up_down_counter(name=name, description=description, unit=unit)
            return SimpleGauge(name, otel_gauge=otel_gauge)
        except Exception:
            # Broad catch intentional: OTEL metrics are optional, gracefully fall back to simple gauge
            pass

    return SimpleGauge(name)


def x_gauge__mutmut_3(name: str, description: str = "", unit: str = "") -> SimpleGauge:
    """Create a gauge metric.

    Args:
        name: Name of the gauge
        description: Description of what this gauge measures
        unit: Unit of measurement

    Returns:
        Gauge instance

    """
    if _HAS_OTEL_METRICS or _meter:
        try:
            otel_gauge = _meter.create_up_down_counter(name=name, description=description, unit=unit)
            return SimpleGauge(name, otel_gauge=otel_gauge)
        except Exception:
            # Broad catch intentional: OTEL metrics are optional, gracefully fall back to simple gauge
            pass

    return SimpleGauge(name)


def x_gauge__mutmut_4(name: str, description: str = "", unit: str = "") -> SimpleGauge:
    """Create a gauge metric.

    Args:
        name: Name of the gauge
        description: Description of what this gauge measures
        unit: Unit of measurement

    Returns:
        Gauge instance

    """
    if _HAS_OTEL_METRICS and _meter:
        try:
            otel_gauge = None
            return SimpleGauge(name, otel_gauge=otel_gauge)
        except Exception:
            # Broad catch intentional: OTEL metrics are optional, gracefully fall back to simple gauge
            pass

    return SimpleGauge(name)


def x_gauge__mutmut_5(name: str, description: str = "", unit: str = "") -> SimpleGauge:
    """Create a gauge metric.

    Args:
        name: Name of the gauge
        description: Description of what this gauge measures
        unit: Unit of measurement

    Returns:
        Gauge instance

    """
    if _HAS_OTEL_METRICS and _meter:
        try:
            otel_gauge = _meter.create_up_down_counter(name=None, description=description, unit=unit)
            return SimpleGauge(name, otel_gauge=otel_gauge)
        except Exception:
            # Broad catch intentional: OTEL metrics are optional, gracefully fall back to simple gauge
            pass

    return SimpleGauge(name)


def x_gauge__mutmut_6(name: str, description: str = "", unit: str = "") -> SimpleGauge:
    """Create a gauge metric.

    Args:
        name: Name of the gauge
        description: Description of what this gauge measures
        unit: Unit of measurement

    Returns:
        Gauge instance

    """
    if _HAS_OTEL_METRICS and _meter:
        try:
            otel_gauge = _meter.create_up_down_counter(name=name, description=None, unit=unit)
            return SimpleGauge(name, otel_gauge=otel_gauge)
        except Exception:
            # Broad catch intentional: OTEL metrics are optional, gracefully fall back to simple gauge
            pass

    return SimpleGauge(name)


def x_gauge__mutmut_7(name: str, description: str = "", unit: str = "") -> SimpleGauge:
    """Create a gauge metric.

    Args:
        name: Name of the gauge
        description: Description of what this gauge measures
        unit: Unit of measurement

    Returns:
        Gauge instance

    """
    if _HAS_OTEL_METRICS and _meter:
        try:
            otel_gauge = _meter.create_up_down_counter(name=name, description=description, unit=None)
            return SimpleGauge(name, otel_gauge=otel_gauge)
        except Exception:
            # Broad catch intentional: OTEL metrics are optional, gracefully fall back to simple gauge
            pass

    return SimpleGauge(name)


def x_gauge__mutmut_8(name: str, description: str = "", unit: str = "") -> SimpleGauge:
    """Create a gauge metric.

    Args:
        name: Name of the gauge
        description: Description of what this gauge measures
        unit: Unit of measurement

    Returns:
        Gauge instance

    """
    if _HAS_OTEL_METRICS and _meter:
        try:
            otel_gauge = _meter.create_up_down_counter(description=description, unit=unit)
            return SimpleGauge(name, otel_gauge=otel_gauge)
        except Exception:
            # Broad catch intentional: OTEL metrics are optional, gracefully fall back to simple gauge
            pass

    return SimpleGauge(name)


def x_gauge__mutmut_9(name: str, description: str = "", unit: str = "") -> SimpleGauge:
    """Create a gauge metric.

    Args:
        name: Name of the gauge
        description: Description of what this gauge measures
        unit: Unit of measurement

    Returns:
        Gauge instance

    """
    if _HAS_OTEL_METRICS and _meter:
        try:
            otel_gauge = _meter.create_up_down_counter(name=name, unit=unit)
            return SimpleGauge(name, otel_gauge=otel_gauge)
        except Exception:
            # Broad catch intentional: OTEL metrics are optional, gracefully fall back to simple gauge
            pass

    return SimpleGauge(name)


def x_gauge__mutmut_10(name: str, description: str = "", unit: str = "") -> SimpleGauge:
    """Create a gauge metric.

    Args:
        name: Name of the gauge
        description: Description of what this gauge measures
        unit: Unit of measurement

    Returns:
        Gauge instance

    """
    if _HAS_OTEL_METRICS and _meter:
        try:
            otel_gauge = _meter.create_up_down_counter(
                name=name,
                description=description,
            )
            return SimpleGauge(name, otel_gauge=otel_gauge)
        except Exception:
            # Broad catch intentional: OTEL metrics are optional, gracefully fall back to simple gauge
            pass

    return SimpleGauge(name)


def x_gauge__mutmut_11(name: str, description: str = "", unit: str = "") -> SimpleGauge:
    """Create a gauge metric.

    Args:
        name: Name of the gauge
        description: Description of what this gauge measures
        unit: Unit of measurement

    Returns:
        Gauge instance

    """
    if _HAS_OTEL_METRICS and _meter:
        try:
            otel_gauge = _meter.create_up_down_counter(name=name, description=description, unit=unit)
            return SimpleGauge(None, otel_gauge=otel_gauge)
        except Exception:
            # Broad catch intentional: OTEL metrics are optional, gracefully fall back to simple gauge
            pass

    return SimpleGauge(name)


def x_gauge__mutmut_12(name: str, description: str = "", unit: str = "") -> SimpleGauge:
    """Create a gauge metric.

    Args:
        name: Name of the gauge
        description: Description of what this gauge measures
        unit: Unit of measurement

    Returns:
        Gauge instance

    """
    if _HAS_OTEL_METRICS and _meter:
        try:
            otel_gauge = _meter.create_up_down_counter(name=name, description=description, unit=unit)
            return SimpleGauge(name, otel_gauge=None)
        except Exception:
            # Broad catch intentional: OTEL metrics are optional, gracefully fall back to simple gauge
            pass

    return SimpleGauge(name)


def x_gauge__mutmut_13(name: str, description: str = "", unit: str = "") -> SimpleGauge:
    """Create a gauge metric.

    Args:
        name: Name of the gauge
        description: Description of what this gauge measures
        unit: Unit of measurement

    Returns:
        Gauge instance

    """
    if _HAS_OTEL_METRICS and _meter:
        try:
            otel_gauge = _meter.create_up_down_counter(name=name, description=description, unit=unit)
            return SimpleGauge(otel_gauge=otel_gauge)
        except Exception:
            # Broad catch intentional: OTEL metrics are optional, gracefully fall back to simple gauge
            pass

    return SimpleGauge(name)


def x_gauge__mutmut_14(name: str, description: str = "", unit: str = "") -> SimpleGauge:
    """Create a gauge metric.

    Args:
        name: Name of the gauge
        description: Description of what this gauge measures
        unit: Unit of measurement

    Returns:
        Gauge instance

    """
    if _HAS_OTEL_METRICS and _meter:
        try:
            otel_gauge = _meter.create_up_down_counter(name=name, description=description, unit=unit)
            return SimpleGauge(
                name,
            )
        except Exception:
            # Broad catch intentional: OTEL metrics are optional, gracefully fall back to simple gauge
            pass

    return SimpleGauge(name)


def x_gauge__mutmut_15(name: str, description: str = "", unit: str = "") -> SimpleGauge:
    """Create a gauge metric.

    Args:
        name: Name of the gauge
        description: Description of what this gauge measures
        unit: Unit of measurement

    Returns:
        Gauge instance

    """
    if _HAS_OTEL_METRICS and _meter:
        try:
            otel_gauge = _meter.create_up_down_counter(name=name, description=description, unit=unit)
            return SimpleGauge(name, otel_gauge=otel_gauge)
        except Exception:
            # Broad catch intentional: OTEL metrics are optional, gracefully fall back to simple gauge
            pass

    return SimpleGauge(None)


x_gauge__mutmut_mutants: ClassVar[MutantDict] = {
    "x_gauge__mutmut_1": x_gauge__mutmut_1,
    "x_gauge__mutmut_2": x_gauge__mutmut_2,
    "x_gauge__mutmut_3": x_gauge__mutmut_3,
    "x_gauge__mutmut_4": x_gauge__mutmut_4,
    "x_gauge__mutmut_5": x_gauge__mutmut_5,
    "x_gauge__mutmut_6": x_gauge__mutmut_6,
    "x_gauge__mutmut_7": x_gauge__mutmut_7,
    "x_gauge__mutmut_8": x_gauge__mutmut_8,
    "x_gauge__mutmut_9": x_gauge__mutmut_9,
    "x_gauge__mutmut_10": x_gauge__mutmut_10,
    "x_gauge__mutmut_11": x_gauge__mutmut_11,
    "x_gauge__mutmut_12": x_gauge__mutmut_12,
    "x_gauge__mutmut_13": x_gauge__mutmut_13,
    "x_gauge__mutmut_14": x_gauge__mutmut_14,
    "x_gauge__mutmut_15": x_gauge__mutmut_15,
}


def gauge(*args, **kwargs):
    result = _mutmut_trampoline(x_gauge__mutmut_orig, x_gauge__mutmut_mutants, args, kwargs)
    return result


gauge.__signature__ = _mutmut_signature(x_gauge__mutmut_orig)
x_gauge__mutmut_orig.__name__ = "x_gauge"


def x_histogram__mutmut_orig(name: str, description: str = "", unit: str = "") -> SimpleHistogram:
    """Create a histogram metric.

    Args:
        name: Name of the histogram
        description: Description of what this histogram measures
        unit: Unit of measurement

    Returns:
        Histogram instance

    """
    if _HAS_OTEL_METRICS and _meter:
        try:
            otel_histogram = _meter.create_histogram(name=name, description=description, unit=unit)
            return SimpleHistogram(name, otel_histogram=otel_histogram)
        except Exception:
            # Broad catch intentional: OTEL metrics are optional, gracefully fall back to simple histogram
            pass

    return SimpleHistogram(name)


def x_histogram__mutmut_1(name: str, description: str = "XXXX", unit: str = "") -> SimpleHistogram:
    """Create a histogram metric.

    Args:
        name: Name of the histogram
        description: Description of what this histogram measures
        unit: Unit of measurement

    Returns:
        Histogram instance

    """
    if _HAS_OTEL_METRICS and _meter:
        try:
            otel_histogram = _meter.create_histogram(name=name, description=description, unit=unit)
            return SimpleHistogram(name, otel_histogram=otel_histogram)
        except Exception:
            # Broad catch intentional: OTEL metrics are optional, gracefully fall back to simple histogram
            pass

    return SimpleHistogram(name)


def x_histogram__mutmut_2(name: str, description: str = "", unit: str = "XXXX") -> SimpleHistogram:
    """Create a histogram metric.

    Args:
        name: Name of the histogram
        description: Description of what this histogram measures
        unit: Unit of measurement

    Returns:
        Histogram instance

    """
    if _HAS_OTEL_METRICS and _meter:
        try:
            otel_histogram = _meter.create_histogram(name=name, description=description, unit=unit)
            return SimpleHistogram(name, otel_histogram=otel_histogram)
        except Exception:
            # Broad catch intentional: OTEL metrics are optional, gracefully fall back to simple histogram
            pass

    return SimpleHistogram(name)


def x_histogram__mutmut_3(name: str, description: str = "", unit: str = "") -> SimpleHistogram:
    """Create a histogram metric.

    Args:
        name: Name of the histogram
        description: Description of what this histogram measures
        unit: Unit of measurement

    Returns:
        Histogram instance

    """
    if _HAS_OTEL_METRICS or _meter:
        try:
            otel_histogram = _meter.create_histogram(name=name, description=description, unit=unit)
            return SimpleHistogram(name, otel_histogram=otel_histogram)
        except Exception:
            # Broad catch intentional: OTEL metrics are optional, gracefully fall back to simple histogram
            pass

    return SimpleHistogram(name)


def x_histogram__mutmut_4(name: str, description: str = "", unit: str = "") -> SimpleHistogram:
    """Create a histogram metric.

    Args:
        name: Name of the histogram
        description: Description of what this histogram measures
        unit: Unit of measurement

    Returns:
        Histogram instance

    """
    if _HAS_OTEL_METRICS and _meter:
        try:
            otel_histogram = None
            return SimpleHistogram(name, otel_histogram=otel_histogram)
        except Exception:
            # Broad catch intentional: OTEL metrics are optional, gracefully fall back to simple histogram
            pass

    return SimpleHistogram(name)


def x_histogram__mutmut_5(name: str, description: str = "", unit: str = "") -> SimpleHistogram:
    """Create a histogram metric.

    Args:
        name: Name of the histogram
        description: Description of what this histogram measures
        unit: Unit of measurement

    Returns:
        Histogram instance

    """
    if _HAS_OTEL_METRICS and _meter:
        try:
            otel_histogram = _meter.create_histogram(name=None, description=description, unit=unit)
            return SimpleHistogram(name, otel_histogram=otel_histogram)
        except Exception:
            # Broad catch intentional: OTEL metrics are optional, gracefully fall back to simple histogram
            pass

    return SimpleHistogram(name)


def x_histogram__mutmut_6(name: str, description: str = "", unit: str = "") -> SimpleHistogram:
    """Create a histogram metric.

    Args:
        name: Name of the histogram
        description: Description of what this histogram measures
        unit: Unit of measurement

    Returns:
        Histogram instance

    """
    if _HAS_OTEL_METRICS and _meter:
        try:
            otel_histogram = _meter.create_histogram(name=name, description=None, unit=unit)
            return SimpleHistogram(name, otel_histogram=otel_histogram)
        except Exception:
            # Broad catch intentional: OTEL metrics are optional, gracefully fall back to simple histogram
            pass

    return SimpleHistogram(name)


def x_histogram__mutmut_7(name: str, description: str = "", unit: str = "") -> SimpleHistogram:
    """Create a histogram metric.

    Args:
        name: Name of the histogram
        description: Description of what this histogram measures
        unit: Unit of measurement

    Returns:
        Histogram instance

    """
    if _HAS_OTEL_METRICS and _meter:
        try:
            otel_histogram = _meter.create_histogram(name=name, description=description, unit=None)
            return SimpleHistogram(name, otel_histogram=otel_histogram)
        except Exception:
            # Broad catch intentional: OTEL metrics are optional, gracefully fall back to simple histogram
            pass

    return SimpleHistogram(name)


def x_histogram__mutmut_8(name: str, description: str = "", unit: str = "") -> SimpleHistogram:
    """Create a histogram metric.

    Args:
        name: Name of the histogram
        description: Description of what this histogram measures
        unit: Unit of measurement

    Returns:
        Histogram instance

    """
    if _HAS_OTEL_METRICS and _meter:
        try:
            otel_histogram = _meter.create_histogram(description=description, unit=unit)
            return SimpleHistogram(name, otel_histogram=otel_histogram)
        except Exception:
            # Broad catch intentional: OTEL metrics are optional, gracefully fall back to simple histogram
            pass

    return SimpleHistogram(name)


def x_histogram__mutmut_9(name: str, description: str = "", unit: str = "") -> SimpleHistogram:
    """Create a histogram metric.

    Args:
        name: Name of the histogram
        description: Description of what this histogram measures
        unit: Unit of measurement

    Returns:
        Histogram instance

    """
    if _HAS_OTEL_METRICS and _meter:
        try:
            otel_histogram = _meter.create_histogram(name=name, unit=unit)
            return SimpleHistogram(name, otel_histogram=otel_histogram)
        except Exception:
            # Broad catch intentional: OTEL metrics are optional, gracefully fall back to simple histogram
            pass

    return SimpleHistogram(name)


def x_histogram__mutmut_10(name: str, description: str = "", unit: str = "") -> SimpleHistogram:
    """Create a histogram metric.

    Args:
        name: Name of the histogram
        description: Description of what this histogram measures
        unit: Unit of measurement

    Returns:
        Histogram instance

    """
    if _HAS_OTEL_METRICS and _meter:
        try:
            otel_histogram = _meter.create_histogram(
                name=name,
                description=description,
            )
            return SimpleHistogram(name, otel_histogram=otel_histogram)
        except Exception:
            # Broad catch intentional: OTEL metrics are optional, gracefully fall back to simple histogram
            pass

    return SimpleHistogram(name)


def x_histogram__mutmut_11(name: str, description: str = "", unit: str = "") -> SimpleHistogram:
    """Create a histogram metric.

    Args:
        name: Name of the histogram
        description: Description of what this histogram measures
        unit: Unit of measurement

    Returns:
        Histogram instance

    """
    if _HAS_OTEL_METRICS and _meter:
        try:
            otel_histogram = _meter.create_histogram(name=name, description=description, unit=unit)
            return SimpleHistogram(None, otel_histogram=otel_histogram)
        except Exception:
            # Broad catch intentional: OTEL metrics are optional, gracefully fall back to simple histogram
            pass

    return SimpleHistogram(name)


def x_histogram__mutmut_12(name: str, description: str = "", unit: str = "") -> SimpleHistogram:
    """Create a histogram metric.

    Args:
        name: Name of the histogram
        description: Description of what this histogram measures
        unit: Unit of measurement

    Returns:
        Histogram instance

    """
    if _HAS_OTEL_METRICS and _meter:
        try:
            otel_histogram = _meter.create_histogram(name=name, description=description, unit=unit)
            return SimpleHistogram(name, otel_histogram=None)
        except Exception:
            # Broad catch intentional: OTEL metrics are optional, gracefully fall back to simple histogram
            pass

    return SimpleHistogram(name)


def x_histogram__mutmut_13(name: str, description: str = "", unit: str = "") -> SimpleHistogram:
    """Create a histogram metric.

    Args:
        name: Name of the histogram
        description: Description of what this histogram measures
        unit: Unit of measurement

    Returns:
        Histogram instance

    """
    if _HAS_OTEL_METRICS and _meter:
        try:
            otel_histogram = _meter.create_histogram(name=name, description=description, unit=unit)
            return SimpleHistogram(otel_histogram=otel_histogram)
        except Exception:
            # Broad catch intentional: OTEL metrics are optional, gracefully fall back to simple histogram
            pass

    return SimpleHistogram(name)


def x_histogram__mutmut_14(name: str, description: str = "", unit: str = "") -> SimpleHistogram:
    """Create a histogram metric.

    Args:
        name: Name of the histogram
        description: Description of what this histogram measures
        unit: Unit of measurement

    Returns:
        Histogram instance

    """
    if _HAS_OTEL_METRICS and _meter:
        try:
            otel_histogram = _meter.create_histogram(name=name, description=description, unit=unit)
            return SimpleHistogram(
                name,
            )
        except Exception:
            # Broad catch intentional: OTEL metrics are optional, gracefully fall back to simple histogram
            pass

    return SimpleHistogram(name)


def x_histogram__mutmut_15(name: str, description: str = "", unit: str = "") -> SimpleHistogram:
    """Create a histogram metric.

    Args:
        name: Name of the histogram
        description: Description of what this histogram measures
        unit: Unit of measurement

    Returns:
        Histogram instance

    """
    if _HAS_OTEL_METRICS and _meter:
        try:
            otel_histogram = _meter.create_histogram(name=name, description=description, unit=unit)
            return SimpleHistogram(name, otel_histogram=otel_histogram)
        except Exception:
            # Broad catch intentional: OTEL metrics are optional, gracefully fall back to simple histogram
            pass

    return SimpleHistogram(None)


x_histogram__mutmut_mutants: ClassVar[MutantDict] = {
    "x_histogram__mutmut_1": x_histogram__mutmut_1,
    "x_histogram__mutmut_2": x_histogram__mutmut_2,
    "x_histogram__mutmut_3": x_histogram__mutmut_3,
    "x_histogram__mutmut_4": x_histogram__mutmut_4,
    "x_histogram__mutmut_5": x_histogram__mutmut_5,
    "x_histogram__mutmut_6": x_histogram__mutmut_6,
    "x_histogram__mutmut_7": x_histogram__mutmut_7,
    "x_histogram__mutmut_8": x_histogram__mutmut_8,
    "x_histogram__mutmut_9": x_histogram__mutmut_9,
    "x_histogram__mutmut_10": x_histogram__mutmut_10,
    "x_histogram__mutmut_11": x_histogram__mutmut_11,
    "x_histogram__mutmut_12": x_histogram__mutmut_12,
    "x_histogram__mutmut_13": x_histogram__mutmut_13,
    "x_histogram__mutmut_14": x_histogram__mutmut_14,
    "x_histogram__mutmut_15": x_histogram__mutmut_15,
}


def histogram(*args, **kwargs):
    result = _mutmut_trampoline(x_histogram__mutmut_orig, x_histogram__mutmut_mutants, args, kwargs)
    return result


histogram.__signature__ = _mutmut_signature(x_histogram__mutmut_orig)
x_histogram__mutmut_orig.__name__ = "x_histogram"


def x__set_meter__mutmut_orig(meter: object) -> None:
    """Set the global meter instance (internal use only)."""
    global _meter
    _meter = meter


def x__set_meter__mutmut_1(meter: object) -> None:
    """Set the global meter instance (internal use only)."""
    global _meter
    _meter = None


x__set_meter__mutmut_mutants: ClassVar[MutantDict] = {"x__set_meter__mutmut_1": x__set_meter__mutmut_1}


def _set_meter(*args, **kwargs):
    result = _mutmut_trampoline(x__set_meter__mutmut_orig, x__set_meter__mutmut_mutants, args, kwargs)
    return result


_set_meter.__signature__ = _mutmut_signature(x__set_meter__mutmut_orig)
x__set_meter__mutmut_orig.__name__ = "x__set_meter"


# <3 🧱🤝📈🪄
