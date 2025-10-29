# provide/foundation/metrics/simple.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from collections import defaultdict
from typing import Any

from provide.foundation.logger import get_logger

"""Simple metrics implementations that work with or without OpenTelemetry."""

log = get_logger(__name__)
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


class SimpleCounter:
    """Counter metric that increments monotonically."""

    def xǁSimpleCounterǁ__init____mutmut_orig(self, name: str, otel_counter: Any | None = None) -> None:
        self.name = name
        self._otel_counter = otel_counter
        self._value: float = 0
        self._labels_values: dict[str, float] = defaultdict(float)

    def xǁSimpleCounterǁ__init____mutmut_1(self, name: str, otel_counter: Any | None = None) -> None:
        self.name = None
        self._otel_counter = otel_counter
        self._value: float = 0
        self._labels_values: dict[str, float] = defaultdict(float)

    def xǁSimpleCounterǁ__init____mutmut_2(self, name: str, otel_counter: Any | None = None) -> None:
        self.name = name
        self._otel_counter = None
        self._value: float = 0
        self._labels_values: dict[str, float] = defaultdict(float)

    def xǁSimpleCounterǁ__init____mutmut_3(self, name: str, otel_counter: Any | None = None) -> None:
        self.name = name
        self._otel_counter = otel_counter
        self._value: float = None
        self._labels_values: dict[str, float] = defaultdict(float)

    def xǁSimpleCounterǁ__init____mutmut_4(self, name: str, otel_counter: Any | None = None) -> None:
        self.name = name
        self._otel_counter = otel_counter
        self._value: float = 1
        self._labels_values: dict[str, float] = defaultdict(float)

    def xǁSimpleCounterǁ__init____mutmut_5(self, name: str, otel_counter: Any | None = None) -> None:
        self.name = name
        self._otel_counter = otel_counter
        self._value: float = 0
        self._labels_values: dict[str, float] = None

    def xǁSimpleCounterǁ__init____mutmut_6(self, name: str, otel_counter: Any | None = None) -> None:
        self.name = name
        self._otel_counter = otel_counter
        self._value: float = 0
        self._labels_values: dict[str, float] = defaultdict(None)

    xǁSimpleCounterǁ__init____mutmut_mutants: ClassVar[MutantDict] = {
        "xǁSimpleCounterǁ__init____mutmut_1": xǁSimpleCounterǁ__init____mutmut_1,
        "xǁSimpleCounterǁ__init____mutmut_2": xǁSimpleCounterǁ__init____mutmut_2,
        "xǁSimpleCounterǁ__init____mutmut_3": xǁSimpleCounterǁ__init____mutmut_3,
        "xǁSimpleCounterǁ__init____mutmut_4": xǁSimpleCounterǁ__init____mutmut_4,
        "xǁSimpleCounterǁ__init____mutmut_5": xǁSimpleCounterǁ__init____mutmut_5,
        "xǁSimpleCounterǁ__init____mutmut_6": xǁSimpleCounterǁ__init____mutmut_6,
    }

    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁSimpleCounterǁ__init____mutmut_orig"),
            object.__getattribute__(self, "xǁSimpleCounterǁ__init____mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    __init__.__signature__ = _mutmut_signature(xǁSimpleCounterǁ__init____mutmut_orig)
    xǁSimpleCounterǁ__init____mutmut_orig.__name__ = "xǁSimpleCounterǁ__init__"

    def xǁSimpleCounterǁinc__mutmut_orig(self, value: float = 1, **labels: Any) -> None:
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

    def xǁSimpleCounterǁinc__mutmut_1(self, value: float = 2, **labels: Any) -> None:
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

    def xǁSimpleCounterǁinc__mutmut_2(self, value: float = 1, **labels: Any) -> None:
        """Increment the counter.

        Args:
            value: Amount to increment by (default: 1)
            **labels: Label key-value pairs

        """
        self._value = value

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

    def xǁSimpleCounterǁinc__mutmut_3(self, value: float = 1, **labels: Any) -> None:
        """Increment the counter.

        Args:
            value: Amount to increment by (default: 1)
            **labels: Label key-value pairs

        """
        self._value -= value

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

    def xǁSimpleCounterǁinc__mutmut_4(self, value: float = 1, **labels: Any) -> None:
        """Increment the counter.

        Args:
            value: Amount to increment by (default: 1)
            **labels: Label key-value pairs

        """
        self._value += value

        # Track per-label values for simple mode
        if labels:
            labels_key = None
            self._labels_values[labels_key] += value

        # Use OpenTelemetry counter if available
        if self._otel_counter:
            try:
                self._otel_counter.add(value, attributes=labels)
            except Exception as e:
                log.debug(f"📊⚠️ Failed to record OpenTelemetry counter: {e}")

    def xǁSimpleCounterǁinc__mutmut_5(self, value: float = 1, **labels: Any) -> None:
        """Increment the counter.

        Args:
            value: Amount to increment by (default: 1)
            **labels: Label key-value pairs

        """
        self._value += value

        # Track per-label values for simple mode
        if labels:
            labels_key = ",".join(None)
            self._labels_values[labels_key] += value

        # Use OpenTelemetry counter if available
        if self._otel_counter:
            try:
                self._otel_counter.add(value, attributes=labels)
            except Exception as e:
                log.debug(f"📊⚠️ Failed to record OpenTelemetry counter: {e}")

    def xǁSimpleCounterǁinc__mutmut_6(self, value: float = 1, **labels: Any) -> None:
        """Increment the counter.

        Args:
            value: Amount to increment by (default: 1)
            **labels: Label key-value pairs

        """
        self._value += value

        # Track per-label values for simple mode
        if labels:
            labels_key = "XX,XX".join(f"{k}={v}" for k, v in sorted(labels.items()))
            self._labels_values[labels_key] += value

        # Use OpenTelemetry counter if available
        if self._otel_counter:
            try:
                self._otel_counter.add(value, attributes=labels)
            except Exception as e:
                log.debug(f"📊⚠️ Failed to record OpenTelemetry counter: {e}")

    def xǁSimpleCounterǁinc__mutmut_7(self, value: float = 1, **labels: Any) -> None:
        """Increment the counter.

        Args:
            value: Amount to increment by (default: 1)
            **labels: Label key-value pairs

        """
        self._value += value

        # Track per-label values for simple mode
        if labels:
            labels_key = ",".join(f"{k}={v}" for k, v in sorted(None))
            self._labels_values[labels_key] += value

        # Use OpenTelemetry counter if available
        if self._otel_counter:
            try:
                self._otel_counter.add(value, attributes=labels)
            except Exception as e:
                log.debug(f"📊⚠️ Failed to record OpenTelemetry counter: {e}")

    def xǁSimpleCounterǁinc__mutmut_8(self, value: float = 1, **labels: Any) -> None:
        """Increment the counter.

        Args:
            value: Amount to increment by (default: 1)
            **labels: Label key-value pairs

        """
        self._value += value

        # Track per-label values for simple mode
        if labels:
            labels_key = ",".join(f"{k}={v}" for k, v in sorted(labels.items()))
            self._labels_values[labels_key] = value

        # Use OpenTelemetry counter if available
        if self._otel_counter:
            try:
                self._otel_counter.add(value, attributes=labels)
            except Exception as e:
                log.debug(f"📊⚠️ Failed to record OpenTelemetry counter: {e}")

    def xǁSimpleCounterǁinc__mutmut_9(self, value: float = 1, **labels: Any) -> None:
        """Increment the counter.

        Args:
            value: Amount to increment by (default: 1)
            **labels: Label key-value pairs

        """
        self._value += value

        # Track per-label values for simple mode
        if labels:
            labels_key = ",".join(f"{k}={v}" for k, v in sorted(labels.items()))
            self._labels_values[labels_key] -= value

        # Use OpenTelemetry counter if available
        if self._otel_counter:
            try:
                self._otel_counter.add(value, attributes=labels)
            except Exception as e:
                log.debug(f"📊⚠️ Failed to record OpenTelemetry counter: {e}")

    def xǁSimpleCounterǁinc__mutmut_10(self, value: float = 1, **labels: Any) -> None:
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
                self._otel_counter.add(None, attributes=labels)
            except Exception as e:
                log.debug(f"📊⚠️ Failed to record OpenTelemetry counter: {e}")

    def xǁSimpleCounterǁinc__mutmut_11(self, value: float = 1, **labels: Any) -> None:
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
                self._otel_counter.add(value, attributes=None)
            except Exception as e:
                log.debug(f"📊⚠️ Failed to record OpenTelemetry counter: {e}")

    def xǁSimpleCounterǁinc__mutmut_12(self, value: float = 1, **labels: Any) -> None:
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
                self._otel_counter.add(attributes=labels)
            except Exception as e:
                log.debug(f"📊⚠️ Failed to record OpenTelemetry counter: {e}")

    def xǁSimpleCounterǁinc__mutmut_13(self, value: float = 1, **labels: Any) -> None:
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
                self._otel_counter.add(
                    value,
                )
            except Exception as e:
                log.debug(f"📊⚠️ Failed to record OpenTelemetry counter: {e}")

    def xǁSimpleCounterǁinc__mutmut_14(self, value: float = 1, **labels: Any) -> None:
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
                log.debug(None)

    xǁSimpleCounterǁinc__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁSimpleCounterǁinc__mutmut_1": xǁSimpleCounterǁinc__mutmut_1,
        "xǁSimpleCounterǁinc__mutmut_2": xǁSimpleCounterǁinc__mutmut_2,
        "xǁSimpleCounterǁinc__mutmut_3": xǁSimpleCounterǁinc__mutmut_3,
        "xǁSimpleCounterǁinc__mutmut_4": xǁSimpleCounterǁinc__mutmut_4,
        "xǁSimpleCounterǁinc__mutmut_5": xǁSimpleCounterǁinc__mutmut_5,
        "xǁSimpleCounterǁinc__mutmut_6": xǁSimpleCounterǁinc__mutmut_6,
        "xǁSimpleCounterǁinc__mutmut_7": xǁSimpleCounterǁinc__mutmut_7,
        "xǁSimpleCounterǁinc__mutmut_8": xǁSimpleCounterǁinc__mutmut_8,
        "xǁSimpleCounterǁinc__mutmut_9": xǁSimpleCounterǁinc__mutmut_9,
        "xǁSimpleCounterǁinc__mutmut_10": xǁSimpleCounterǁinc__mutmut_10,
        "xǁSimpleCounterǁinc__mutmut_11": xǁSimpleCounterǁinc__mutmut_11,
        "xǁSimpleCounterǁinc__mutmut_12": xǁSimpleCounterǁinc__mutmut_12,
        "xǁSimpleCounterǁinc__mutmut_13": xǁSimpleCounterǁinc__mutmut_13,
        "xǁSimpleCounterǁinc__mutmut_14": xǁSimpleCounterǁinc__mutmut_14,
    }

    def inc(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁSimpleCounterǁinc__mutmut_orig"),
            object.__getattribute__(self, "xǁSimpleCounterǁinc__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    inc.__signature__ = _mutmut_signature(xǁSimpleCounterǁinc__mutmut_orig)
    xǁSimpleCounterǁinc__mutmut_orig.__name__ = "xǁSimpleCounterǁinc"

    @property
    def value(self) -> float:
        """Get the current counter value."""
        return self._value


class SimpleGauge:
    """Gauge metric that can go up or down."""

    def xǁSimpleGaugeǁ__init____mutmut_orig(self, name: str, otel_gauge: Any | None = None) -> None:
        self.name = name
        self._otel_gauge = otel_gauge
        self._value: float = 0
        self._labels_values: dict[str, float] = defaultdict(float)

    def xǁSimpleGaugeǁ__init____mutmut_1(self, name: str, otel_gauge: Any | None = None) -> None:
        self.name = None
        self._otel_gauge = otel_gauge
        self._value: float = 0
        self._labels_values: dict[str, float] = defaultdict(float)

    def xǁSimpleGaugeǁ__init____mutmut_2(self, name: str, otel_gauge: Any | None = None) -> None:
        self.name = name
        self._otel_gauge = None
        self._value: float = 0
        self._labels_values: dict[str, float] = defaultdict(float)

    def xǁSimpleGaugeǁ__init____mutmut_3(self, name: str, otel_gauge: Any | None = None) -> None:
        self.name = name
        self._otel_gauge = otel_gauge
        self._value: float = None
        self._labels_values: dict[str, float] = defaultdict(float)

    def xǁSimpleGaugeǁ__init____mutmut_4(self, name: str, otel_gauge: Any | None = None) -> None:
        self.name = name
        self._otel_gauge = otel_gauge
        self._value: float = 1
        self._labels_values: dict[str, float] = defaultdict(float)

    def xǁSimpleGaugeǁ__init____mutmut_5(self, name: str, otel_gauge: Any | None = None) -> None:
        self.name = name
        self._otel_gauge = otel_gauge
        self._value: float = 0
        self._labels_values: dict[str, float] = None

    def xǁSimpleGaugeǁ__init____mutmut_6(self, name: str, otel_gauge: Any | None = None) -> None:
        self.name = name
        self._otel_gauge = otel_gauge
        self._value: float = 0
        self._labels_values: dict[str, float] = defaultdict(None)

    xǁSimpleGaugeǁ__init____mutmut_mutants: ClassVar[MutantDict] = {
        "xǁSimpleGaugeǁ__init____mutmut_1": xǁSimpleGaugeǁ__init____mutmut_1,
        "xǁSimpleGaugeǁ__init____mutmut_2": xǁSimpleGaugeǁ__init____mutmut_2,
        "xǁSimpleGaugeǁ__init____mutmut_3": xǁSimpleGaugeǁ__init____mutmut_3,
        "xǁSimpleGaugeǁ__init____mutmut_4": xǁSimpleGaugeǁ__init____mutmut_4,
        "xǁSimpleGaugeǁ__init____mutmut_5": xǁSimpleGaugeǁ__init____mutmut_5,
        "xǁSimpleGaugeǁ__init____mutmut_6": xǁSimpleGaugeǁ__init____mutmut_6,
    }

    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁSimpleGaugeǁ__init____mutmut_orig"),
            object.__getattribute__(self, "xǁSimpleGaugeǁ__init____mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    __init__.__signature__ = _mutmut_signature(xǁSimpleGaugeǁ__init____mutmut_orig)
    xǁSimpleGaugeǁ__init____mutmut_orig.__name__ = "xǁSimpleGaugeǁ__init__"

    def xǁSimpleGaugeǁset__mutmut_orig(self, value: float, **labels: Any) -> None:
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

    def xǁSimpleGaugeǁset__mutmut_1(self, value: float, **labels: Any) -> None:
        """Set the gauge value.

        Args:
            value: Value to set
            **labels: Label key-value pairs

        """
        self._value = None

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

    def xǁSimpleGaugeǁset__mutmut_2(self, value: float, **labels: Any) -> None:
        """Set the gauge value.

        Args:
            value: Value to set
            **labels: Label key-value pairs

        """
        self._value = value

        # Track per-label values for simple mode
        if labels:
            labels_key = None
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

    def xǁSimpleGaugeǁset__mutmut_3(self, value: float, **labels: Any) -> None:
        """Set the gauge value.

        Args:
            value: Value to set
            **labels: Label key-value pairs

        """
        self._value = value

        # Track per-label values for simple mode
        if labels:
            labels_key = ",".join(None)
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

    def xǁSimpleGaugeǁset__mutmut_4(self, value: float, **labels: Any) -> None:
        """Set the gauge value.

        Args:
            value: Value to set
            **labels: Label key-value pairs

        """
        self._value = value

        # Track per-label values for simple mode
        if labels:
            labels_key = "XX,XX".join(f"{k}={v}" for k, v in sorted(labels.items()))
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

    def xǁSimpleGaugeǁset__mutmut_5(self, value: float, **labels: Any) -> None:
        """Set the gauge value.

        Args:
            value: Value to set
            **labels: Label key-value pairs

        """
        self._value = value

        # Track per-label values for simple mode
        if labels:
            labels_key = ",".join(f"{k}={v}" for k, v in sorted(None))
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

    def xǁSimpleGaugeǁset__mutmut_6(self, value: float, **labels: Any) -> None:
        """Set the gauge value.

        Args:
            value: Value to set
            **labels: Label key-value pairs

        """
        self._value = value

        # Track per-label values for simple mode
        if labels:
            labels_key = ",".join(f"{k}={v}" for k, v in sorted(labels.items()))
            self._labels_values[labels_key] = None

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

    def xǁSimpleGaugeǁset__mutmut_7(self, value: float, **labels: Any) -> None:
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
                    None,
                    attributes=labels,
                )
            except Exception as e:
                log.debug(f"📊⚠️ Failed to record OpenTelemetry gauge: {e}")

    def xǁSimpleGaugeǁset__mutmut_8(self, value: float, **labels: Any) -> None:
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
                    attributes=None,
                )
            except Exception as e:
                log.debug(f"📊⚠️ Failed to record OpenTelemetry gauge: {e}")

    def xǁSimpleGaugeǁset__mutmut_9(self, value: float, **labels: Any) -> None:
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
                    attributes=labels,
                )
            except Exception as e:
                log.debug(f"📊⚠️ Failed to record OpenTelemetry gauge: {e}")

    def xǁSimpleGaugeǁset__mutmut_10(self, value: float, **labels: Any) -> None:
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
                )
            except Exception as e:
                log.debug(f"📊⚠️ Failed to record OpenTelemetry gauge: {e}")

    def xǁSimpleGaugeǁset__mutmut_11(self, value: float, **labels: Any) -> None:
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
                    + self._labels_values.get(
                        ",".join(f"{k}={v}" for k, v in sorted(labels.items())) if labels else "",
                        0,
                    ),
                    attributes=labels,
                )
            except Exception as e:
                log.debug(f"📊⚠️ Failed to record OpenTelemetry gauge: {e}")

    def xǁSimpleGaugeǁset__mutmut_12(self, value: float, **labels: Any) -> None:
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
                        None,
                        0,
                    ),
                    attributes=labels,
                )
            except Exception as e:
                log.debug(f"📊⚠️ Failed to record OpenTelemetry gauge: {e}")

    def xǁSimpleGaugeǁset__mutmut_13(self, value: float, **labels: Any) -> None:
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
                        None,
                    ),
                    attributes=labels,
                )
            except Exception as e:
                log.debug(f"📊⚠️ Failed to record OpenTelemetry gauge: {e}")

    def xǁSimpleGaugeǁset__mutmut_14(self, value: float, **labels: Any) -> None:
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
                        0,
                    ),
                    attributes=labels,
                )
            except Exception as e:
                log.debug(f"📊⚠️ Failed to record OpenTelemetry gauge: {e}")

    def xǁSimpleGaugeǁset__mutmut_15(self, value: float, **labels: Any) -> None:
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
                    ),
                    attributes=labels,
                )
            except Exception as e:
                log.debug(f"📊⚠️ Failed to record OpenTelemetry gauge: {e}")

    def xǁSimpleGaugeǁset__mutmut_16(self, value: float, **labels: Any) -> None:
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
                        ",".join(None) if labels else "",
                        0,
                    ),
                    attributes=labels,
                )
            except Exception as e:
                log.debug(f"📊⚠️ Failed to record OpenTelemetry gauge: {e}")

    def xǁSimpleGaugeǁset__mutmut_17(self, value: float, **labels: Any) -> None:
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
                        "XX,XX".join(f"{k}={v}" for k, v in sorted(labels.items())) if labels else "",
                        0,
                    ),
                    attributes=labels,
                )
            except Exception as e:
                log.debug(f"📊⚠️ Failed to record OpenTelemetry gauge: {e}")

    def xǁSimpleGaugeǁset__mutmut_18(self, value: float, **labels: Any) -> None:
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
                        ",".join(f"{k}={v}" for k, v in sorted(None)) if labels else "",
                        0,
                    ),
                    attributes=labels,
                )
            except Exception as e:
                log.debug(f"📊⚠️ Failed to record OpenTelemetry gauge: {e}")

    def xǁSimpleGaugeǁset__mutmut_19(self, value: float, **labels: Any) -> None:
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
                        ",".join(f"{k}={v}" for k, v in sorted(labels.items())) if labels else "XXXX",
                        0,
                    ),
                    attributes=labels,
                )
            except Exception as e:
                log.debug(f"📊⚠️ Failed to record OpenTelemetry gauge: {e}")

    def xǁSimpleGaugeǁset__mutmut_20(self, value: float, **labels: Any) -> None:
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
                        1,
                    ),
                    attributes=labels,
                )
            except Exception as e:
                log.debug(f"📊⚠️ Failed to record OpenTelemetry gauge: {e}")

    def xǁSimpleGaugeǁset__mutmut_21(self, value: float, **labels: Any) -> None:
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
                log.debug(None)

    xǁSimpleGaugeǁset__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁSimpleGaugeǁset__mutmut_1": xǁSimpleGaugeǁset__mutmut_1,
        "xǁSimpleGaugeǁset__mutmut_2": xǁSimpleGaugeǁset__mutmut_2,
        "xǁSimpleGaugeǁset__mutmut_3": xǁSimpleGaugeǁset__mutmut_3,
        "xǁSimpleGaugeǁset__mutmut_4": xǁSimpleGaugeǁset__mutmut_4,
        "xǁSimpleGaugeǁset__mutmut_5": xǁSimpleGaugeǁset__mutmut_5,
        "xǁSimpleGaugeǁset__mutmut_6": xǁSimpleGaugeǁset__mutmut_6,
        "xǁSimpleGaugeǁset__mutmut_7": xǁSimpleGaugeǁset__mutmut_7,
        "xǁSimpleGaugeǁset__mutmut_8": xǁSimpleGaugeǁset__mutmut_8,
        "xǁSimpleGaugeǁset__mutmut_9": xǁSimpleGaugeǁset__mutmut_9,
        "xǁSimpleGaugeǁset__mutmut_10": xǁSimpleGaugeǁset__mutmut_10,
        "xǁSimpleGaugeǁset__mutmut_11": xǁSimpleGaugeǁset__mutmut_11,
        "xǁSimpleGaugeǁset__mutmut_12": xǁSimpleGaugeǁset__mutmut_12,
        "xǁSimpleGaugeǁset__mutmut_13": xǁSimpleGaugeǁset__mutmut_13,
        "xǁSimpleGaugeǁset__mutmut_14": xǁSimpleGaugeǁset__mutmut_14,
        "xǁSimpleGaugeǁset__mutmut_15": xǁSimpleGaugeǁset__mutmut_15,
        "xǁSimpleGaugeǁset__mutmut_16": xǁSimpleGaugeǁset__mutmut_16,
        "xǁSimpleGaugeǁset__mutmut_17": xǁSimpleGaugeǁset__mutmut_17,
        "xǁSimpleGaugeǁset__mutmut_18": xǁSimpleGaugeǁset__mutmut_18,
        "xǁSimpleGaugeǁset__mutmut_19": xǁSimpleGaugeǁset__mutmut_19,
        "xǁSimpleGaugeǁset__mutmut_20": xǁSimpleGaugeǁset__mutmut_20,
        "xǁSimpleGaugeǁset__mutmut_21": xǁSimpleGaugeǁset__mutmut_21,
    }

    def set(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁSimpleGaugeǁset__mutmut_orig"),
            object.__getattribute__(self, "xǁSimpleGaugeǁset__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    set.__signature__ = _mutmut_signature(xǁSimpleGaugeǁset__mutmut_orig)
    xǁSimpleGaugeǁset__mutmut_orig.__name__ = "xǁSimpleGaugeǁset"

    def xǁSimpleGaugeǁinc__mutmut_orig(self, value: float = 1, **labels: Any) -> None:
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

    def xǁSimpleGaugeǁinc__mutmut_1(self, value: float = 2, **labels: Any) -> None:
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

    def xǁSimpleGaugeǁinc__mutmut_2(self, value: float = 1, **labels: Any) -> None:
        """Increment the gauge value.

        Args:
            value: Amount to increment by
            **labels: Label key-value pairs

        """
        self._value = value

        if labels:
            labels_key = ",".join(f"{k}={v}" for k, v in sorted(labels.items()))
            self._labels_values[labels_key] += value

        if self._otel_gauge:
            try:
                self._otel_gauge.add(value, attributes=labels)
            except Exception as e:
                log.debug(f"📊⚠️ Failed to increment OpenTelemetry gauge: {e}")

    def xǁSimpleGaugeǁinc__mutmut_3(self, value: float = 1, **labels: Any) -> None:
        """Increment the gauge value.

        Args:
            value: Amount to increment by
            **labels: Label key-value pairs

        """
        self._value -= value

        if labels:
            labels_key = ",".join(f"{k}={v}" for k, v in sorted(labels.items()))
            self._labels_values[labels_key] += value

        if self._otel_gauge:
            try:
                self._otel_gauge.add(value, attributes=labels)
            except Exception as e:
                log.debug(f"📊⚠️ Failed to increment OpenTelemetry gauge: {e}")

    def xǁSimpleGaugeǁinc__mutmut_4(self, value: float = 1, **labels: Any) -> None:
        """Increment the gauge value.

        Args:
            value: Amount to increment by
            **labels: Label key-value pairs

        """
        self._value += value

        if labels:
            labels_key = None
            self._labels_values[labels_key] += value

        if self._otel_gauge:
            try:
                self._otel_gauge.add(value, attributes=labels)
            except Exception as e:
                log.debug(f"📊⚠️ Failed to increment OpenTelemetry gauge: {e}")

    def xǁSimpleGaugeǁinc__mutmut_5(self, value: float = 1, **labels: Any) -> None:
        """Increment the gauge value.

        Args:
            value: Amount to increment by
            **labels: Label key-value pairs

        """
        self._value += value

        if labels:
            labels_key = ",".join(None)
            self._labels_values[labels_key] += value

        if self._otel_gauge:
            try:
                self._otel_gauge.add(value, attributes=labels)
            except Exception as e:
                log.debug(f"📊⚠️ Failed to increment OpenTelemetry gauge: {e}")

    def xǁSimpleGaugeǁinc__mutmut_6(self, value: float = 1, **labels: Any) -> None:
        """Increment the gauge value.

        Args:
            value: Amount to increment by
            **labels: Label key-value pairs

        """
        self._value += value

        if labels:
            labels_key = "XX,XX".join(f"{k}={v}" for k, v in sorted(labels.items()))
            self._labels_values[labels_key] += value

        if self._otel_gauge:
            try:
                self._otel_gauge.add(value, attributes=labels)
            except Exception as e:
                log.debug(f"📊⚠️ Failed to increment OpenTelemetry gauge: {e}")

    def xǁSimpleGaugeǁinc__mutmut_7(self, value: float = 1, **labels: Any) -> None:
        """Increment the gauge value.

        Args:
            value: Amount to increment by
            **labels: Label key-value pairs

        """
        self._value += value

        if labels:
            labels_key = ",".join(f"{k}={v}" for k, v in sorted(None))
            self._labels_values[labels_key] += value

        if self._otel_gauge:
            try:
                self._otel_gauge.add(value, attributes=labels)
            except Exception as e:
                log.debug(f"📊⚠️ Failed to increment OpenTelemetry gauge: {e}")

    def xǁSimpleGaugeǁinc__mutmut_8(self, value: float = 1, **labels: Any) -> None:
        """Increment the gauge value.

        Args:
            value: Amount to increment by
            **labels: Label key-value pairs

        """
        self._value += value

        if labels:
            labels_key = ",".join(f"{k}={v}" for k, v in sorted(labels.items()))
            self._labels_values[labels_key] = value

        if self._otel_gauge:
            try:
                self._otel_gauge.add(value, attributes=labels)
            except Exception as e:
                log.debug(f"📊⚠️ Failed to increment OpenTelemetry gauge: {e}")

    def xǁSimpleGaugeǁinc__mutmut_9(self, value: float = 1, **labels: Any) -> None:
        """Increment the gauge value.

        Args:
            value: Amount to increment by
            **labels: Label key-value pairs

        """
        self._value += value

        if labels:
            labels_key = ",".join(f"{k}={v}" for k, v in sorted(labels.items()))
            self._labels_values[labels_key] -= value

        if self._otel_gauge:
            try:
                self._otel_gauge.add(value, attributes=labels)
            except Exception as e:
                log.debug(f"📊⚠️ Failed to increment OpenTelemetry gauge: {e}")

    def xǁSimpleGaugeǁinc__mutmut_10(self, value: float = 1, **labels: Any) -> None:
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
                self._otel_gauge.add(None, attributes=labels)
            except Exception as e:
                log.debug(f"📊⚠️ Failed to increment OpenTelemetry gauge: {e}")

    def xǁSimpleGaugeǁinc__mutmut_11(self, value: float = 1, **labels: Any) -> None:
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
                self._otel_gauge.add(value, attributes=None)
            except Exception as e:
                log.debug(f"📊⚠️ Failed to increment OpenTelemetry gauge: {e}")

    def xǁSimpleGaugeǁinc__mutmut_12(self, value: float = 1, **labels: Any) -> None:
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
                self._otel_gauge.add(attributes=labels)
            except Exception as e:
                log.debug(f"📊⚠️ Failed to increment OpenTelemetry gauge: {e}")

    def xǁSimpleGaugeǁinc__mutmut_13(self, value: float = 1, **labels: Any) -> None:
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
                self._otel_gauge.add(
                    value,
                )
            except Exception as e:
                log.debug(f"📊⚠️ Failed to increment OpenTelemetry gauge: {e}")

    def xǁSimpleGaugeǁinc__mutmut_14(self, value: float = 1, **labels: Any) -> None:
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
                log.debug(None)

    xǁSimpleGaugeǁinc__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁSimpleGaugeǁinc__mutmut_1": xǁSimpleGaugeǁinc__mutmut_1,
        "xǁSimpleGaugeǁinc__mutmut_2": xǁSimpleGaugeǁinc__mutmut_2,
        "xǁSimpleGaugeǁinc__mutmut_3": xǁSimpleGaugeǁinc__mutmut_3,
        "xǁSimpleGaugeǁinc__mutmut_4": xǁSimpleGaugeǁinc__mutmut_4,
        "xǁSimpleGaugeǁinc__mutmut_5": xǁSimpleGaugeǁinc__mutmut_5,
        "xǁSimpleGaugeǁinc__mutmut_6": xǁSimpleGaugeǁinc__mutmut_6,
        "xǁSimpleGaugeǁinc__mutmut_7": xǁSimpleGaugeǁinc__mutmut_7,
        "xǁSimpleGaugeǁinc__mutmut_8": xǁSimpleGaugeǁinc__mutmut_8,
        "xǁSimpleGaugeǁinc__mutmut_9": xǁSimpleGaugeǁinc__mutmut_9,
        "xǁSimpleGaugeǁinc__mutmut_10": xǁSimpleGaugeǁinc__mutmut_10,
        "xǁSimpleGaugeǁinc__mutmut_11": xǁSimpleGaugeǁinc__mutmut_11,
        "xǁSimpleGaugeǁinc__mutmut_12": xǁSimpleGaugeǁinc__mutmut_12,
        "xǁSimpleGaugeǁinc__mutmut_13": xǁSimpleGaugeǁinc__mutmut_13,
        "xǁSimpleGaugeǁinc__mutmut_14": xǁSimpleGaugeǁinc__mutmut_14,
    }

    def inc(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁSimpleGaugeǁinc__mutmut_orig"),
            object.__getattribute__(self, "xǁSimpleGaugeǁinc__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    inc.__signature__ = _mutmut_signature(xǁSimpleGaugeǁinc__mutmut_orig)
    xǁSimpleGaugeǁinc__mutmut_orig.__name__ = "xǁSimpleGaugeǁinc"

    def xǁSimpleGaugeǁdec__mutmut_orig(self, value: float = 1, **labels: Any) -> None:
        """Decrement the gauge value.

        Args:
            value: Amount to decrement by
            **labels: Label key-value pairs

        """
        self.inc(-value, **labels)

    def xǁSimpleGaugeǁdec__mutmut_1(self, value: float = 2, **labels: Any) -> None:
        """Decrement the gauge value.

        Args:
            value: Amount to decrement by
            **labels: Label key-value pairs

        """
        self.inc(-value, **labels)

    def xǁSimpleGaugeǁdec__mutmut_2(self, value: float = 1, **labels: Any) -> None:
        """Decrement the gauge value.

        Args:
            value: Amount to decrement by
            **labels: Label key-value pairs

        """
        self.inc(None, **labels)

    def xǁSimpleGaugeǁdec__mutmut_3(self, value: float = 1, **labels: Any) -> None:
        """Decrement the gauge value.

        Args:
            value: Amount to decrement by
            **labels: Label key-value pairs

        """
        self.inc(**labels)

    def xǁSimpleGaugeǁdec__mutmut_4(self, value: float = 1, **labels: Any) -> None:
        """Decrement the gauge value.

        Args:
            value: Amount to decrement by
            **labels: Label key-value pairs

        """
        self.inc(
            -value,
        )

    def xǁSimpleGaugeǁdec__mutmut_5(self, value: float = 1, **labels: Any) -> None:
        """Decrement the gauge value.

        Args:
            value: Amount to decrement by
            **labels: Label key-value pairs

        """
        self.inc(+value, **labels)

    xǁSimpleGaugeǁdec__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁSimpleGaugeǁdec__mutmut_1": xǁSimpleGaugeǁdec__mutmut_1,
        "xǁSimpleGaugeǁdec__mutmut_2": xǁSimpleGaugeǁdec__mutmut_2,
        "xǁSimpleGaugeǁdec__mutmut_3": xǁSimpleGaugeǁdec__mutmut_3,
        "xǁSimpleGaugeǁdec__mutmut_4": xǁSimpleGaugeǁdec__mutmut_4,
        "xǁSimpleGaugeǁdec__mutmut_5": xǁSimpleGaugeǁdec__mutmut_5,
    }

    def dec(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁSimpleGaugeǁdec__mutmut_orig"),
            object.__getattribute__(self, "xǁSimpleGaugeǁdec__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    dec.__signature__ = _mutmut_signature(xǁSimpleGaugeǁdec__mutmut_orig)
    xǁSimpleGaugeǁdec__mutmut_orig.__name__ = "xǁSimpleGaugeǁdec"

    @property
    def value(self) -> float:
        """Get the current gauge value."""
        return self._value


class SimpleHistogram:
    """Histogram metric for recording distributions of values."""

    def xǁSimpleHistogramǁ__init____mutmut_orig(self, name: str, otel_histogram: Any | None = None) -> None:
        self.name = name
        self._otel_histogram = otel_histogram
        self._observations: list[float] = []
        self._labels_observations: dict[str, list[float]] = defaultdict(list)

    def xǁSimpleHistogramǁ__init____mutmut_1(self, name: str, otel_histogram: Any | None = None) -> None:
        self.name = None
        self._otel_histogram = otel_histogram
        self._observations: list[float] = []
        self._labels_observations: dict[str, list[float]] = defaultdict(list)

    def xǁSimpleHistogramǁ__init____mutmut_2(self, name: str, otel_histogram: Any | None = None) -> None:
        self.name = name
        self._otel_histogram = None
        self._observations: list[float] = []
        self._labels_observations: dict[str, list[float]] = defaultdict(list)

    def xǁSimpleHistogramǁ__init____mutmut_3(self, name: str, otel_histogram: Any | None = None) -> None:
        self.name = name
        self._otel_histogram = otel_histogram
        self._observations: list[float] = None
        self._labels_observations: dict[str, list[float]] = defaultdict(list)

    def xǁSimpleHistogramǁ__init____mutmut_4(self, name: str, otel_histogram: Any | None = None) -> None:
        self.name = name
        self._otel_histogram = otel_histogram
        self._observations: list[float] = []
        self._labels_observations: dict[str, list[float]] = None

    def xǁSimpleHistogramǁ__init____mutmut_5(self, name: str, otel_histogram: Any | None = None) -> None:
        self.name = name
        self._otel_histogram = otel_histogram
        self._observations: list[float] = []
        self._labels_observations: dict[str, list[float]] = defaultdict(None)

    xǁSimpleHistogramǁ__init____mutmut_mutants: ClassVar[MutantDict] = {
        "xǁSimpleHistogramǁ__init____mutmut_1": xǁSimpleHistogramǁ__init____mutmut_1,
        "xǁSimpleHistogramǁ__init____mutmut_2": xǁSimpleHistogramǁ__init____mutmut_2,
        "xǁSimpleHistogramǁ__init____mutmut_3": xǁSimpleHistogramǁ__init____mutmut_3,
        "xǁSimpleHistogramǁ__init____mutmut_4": xǁSimpleHistogramǁ__init____mutmut_4,
        "xǁSimpleHistogramǁ__init____mutmut_5": xǁSimpleHistogramǁ__init____mutmut_5,
    }

    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁSimpleHistogramǁ__init____mutmut_orig"),
            object.__getattribute__(self, "xǁSimpleHistogramǁ__init____mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    __init__.__signature__ = _mutmut_signature(xǁSimpleHistogramǁ__init____mutmut_orig)
    xǁSimpleHistogramǁ__init____mutmut_orig.__name__ = "xǁSimpleHistogramǁ__init__"

    def xǁSimpleHistogramǁobserve__mutmut_orig(self, value: float, **labels: Any) -> None:
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

    def xǁSimpleHistogramǁobserve__mutmut_1(self, value: float, **labels: Any) -> None:
        """Record an observation.

        Args:
            value: Value to observe
            **labels: Label key-value pairs

        """
        self._observations.append(None)

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

    def xǁSimpleHistogramǁobserve__mutmut_2(self, value: float, **labels: Any) -> None:
        """Record an observation.

        Args:
            value: Value to observe
            **labels: Label key-value pairs

        """
        self._observations.append(value)

        # Track per-label observations for simple mode
        if labels:
            labels_key = None
            self._labels_observations[labels_key].append(value)

        # Use OpenTelemetry histogram if available
        if self._otel_histogram:
            try:
                self._otel_histogram.record(value, attributes=labels)
            except Exception as e:
                log.debug(f"📊⚠️ Failed to record OpenTelemetry histogram: {e}")

    def xǁSimpleHistogramǁobserve__mutmut_3(self, value: float, **labels: Any) -> None:
        """Record an observation.

        Args:
            value: Value to observe
            **labels: Label key-value pairs

        """
        self._observations.append(value)

        # Track per-label observations for simple mode
        if labels:
            labels_key = ",".join(None)
            self._labels_observations[labels_key].append(value)

        # Use OpenTelemetry histogram if available
        if self._otel_histogram:
            try:
                self._otel_histogram.record(value, attributes=labels)
            except Exception as e:
                log.debug(f"📊⚠️ Failed to record OpenTelemetry histogram: {e}")

    def xǁSimpleHistogramǁobserve__mutmut_4(self, value: float, **labels: Any) -> None:
        """Record an observation.

        Args:
            value: Value to observe
            **labels: Label key-value pairs

        """
        self._observations.append(value)

        # Track per-label observations for simple mode
        if labels:
            labels_key = "XX,XX".join(f"{k}={v}" for k, v in sorted(labels.items()))
            self._labels_observations[labels_key].append(value)

        # Use OpenTelemetry histogram if available
        if self._otel_histogram:
            try:
                self._otel_histogram.record(value, attributes=labels)
            except Exception as e:
                log.debug(f"📊⚠️ Failed to record OpenTelemetry histogram: {e}")

    def xǁSimpleHistogramǁobserve__mutmut_5(self, value: float, **labels: Any) -> None:
        """Record an observation.

        Args:
            value: Value to observe
            **labels: Label key-value pairs

        """
        self._observations.append(value)

        # Track per-label observations for simple mode
        if labels:
            labels_key = ",".join(f"{k}={v}" for k, v in sorted(None))
            self._labels_observations[labels_key].append(value)

        # Use OpenTelemetry histogram if available
        if self._otel_histogram:
            try:
                self._otel_histogram.record(value, attributes=labels)
            except Exception as e:
                log.debug(f"📊⚠️ Failed to record OpenTelemetry histogram: {e}")

    def xǁSimpleHistogramǁobserve__mutmut_6(self, value: float, **labels: Any) -> None:
        """Record an observation.

        Args:
            value: Value to observe
            **labels: Label key-value pairs

        """
        self._observations.append(value)

        # Track per-label observations for simple mode
        if labels:
            labels_key = ",".join(f"{k}={v}" for k, v in sorted(labels.items()))
            self._labels_observations[labels_key].append(None)

        # Use OpenTelemetry histogram if available
        if self._otel_histogram:
            try:
                self._otel_histogram.record(value, attributes=labels)
            except Exception as e:
                log.debug(f"📊⚠️ Failed to record OpenTelemetry histogram: {e}")

    def xǁSimpleHistogramǁobserve__mutmut_7(self, value: float, **labels: Any) -> None:
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
                self._otel_histogram.record(None, attributes=labels)
            except Exception as e:
                log.debug(f"📊⚠️ Failed to record OpenTelemetry histogram: {e}")

    def xǁSimpleHistogramǁobserve__mutmut_8(self, value: float, **labels: Any) -> None:
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
                self._otel_histogram.record(value, attributes=None)
            except Exception as e:
                log.debug(f"📊⚠️ Failed to record OpenTelemetry histogram: {e}")

    def xǁSimpleHistogramǁobserve__mutmut_9(self, value: float, **labels: Any) -> None:
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
                self._otel_histogram.record(attributes=labels)
            except Exception as e:
                log.debug(f"📊⚠️ Failed to record OpenTelemetry histogram: {e}")

    def xǁSimpleHistogramǁobserve__mutmut_10(self, value: float, **labels: Any) -> None:
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
                self._otel_histogram.record(
                    value,
                )
            except Exception as e:
                log.debug(f"📊⚠️ Failed to record OpenTelemetry histogram: {e}")

    def xǁSimpleHistogramǁobserve__mutmut_11(self, value: float, **labels: Any) -> None:
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
                log.debug(None)

    xǁSimpleHistogramǁobserve__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁSimpleHistogramǁobserve__mutmut_1": xǁSimpleHistogramǁobserve__mutmut_1,
        "xǁSimpleHistogramǁobserve__mutmut_2": xǁSimpleHistogramǁobserve__mutmut_2,
        "xǁSimpleHistogramǁobserve__mutmut_3": xǁSimpleHistogramǁobserve__mutmut_3,
        "xǁSimpleHistogramǁobserve__mutmut_4": xǁSimpleHistogramǁobserve__mutmut_4,
        "xǁSimpleHistogramǁobserve__mutmut_5": xǁSimpleHistogramǁobserve__mutmut_5,
        "xǁSimpleHistogramǁobserve__mutmut_6": xǁSimpleHistogramǁobserve__mutmut_6,
        "xǁSimpleHistogramǁobserve__mutmut_7": xǁSimpleHistogramǁobserve__mutmut_7,
        "xǁSimpleHistogramǁobserve__mutmut_8": xǁSimpleHistogramǁobserve__mutmut_8,
        "xǁSimpleHistogramǁobserve__mutmut_9": xǁSimpleHistogramǁobserve__mutmut_9,
        "xǁSimpleHistogramǁobserve__mutmut_10": xǁSimpleHistogramǁobserve__mutmut_10,
        "xǁSimpleHistogramǁobserve__mutmut_11": xǁSimpleHistogramǁobserve__mutmut_11,
    }

    def observe(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁSimpleHistogramǁobserve__mutmut_orig"),
            object.__getattribute__(self, "xǁSimpleHistogramǁobserve__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    observe.__signature__ = _mutmut_signature(xǁSimpleHistogramǁobserve__mutmut_orig)
    xǁSimpleHistogramǁobserve__mutmut_orig.__name__ = "xǁSimpleHistogramǁobserve"

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


# <3 🧱🤝📈🪄
