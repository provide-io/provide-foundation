# provide/foundation/profiling/metrics.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import threading
import time
from typing import Any

"""Performance metrics collection for Foundation profiling.

Provides thread-safe metrics collection and calculation for monitoring
Foundation's logging and telemetry performance.
"""
from inspect import signature as _mutmut_signature
from typing import Annotated
from typing import Callable
from typing import ClassVar


MutantDict = Annotated[dict[str, Callable], "Mutant"]


def _mutmut_trampoline(orig, mutants, call_args, call_kwargs, self_arg = None):
    """Forward call to original or mutated function, depending on the environment"""
    import os
    mutant_under_test = os.environ['MUTANT_UNDER_TEST']
    if mutant_under_test == 'fail':
        from mutmut.__main__ import MutmutProgrammaticFailException
        raise MutmutProgrammaticFailException('Failed programmatically')      
    elif mutant_under_test == 'stats':
        from mutmut.__main__ import record_trampoline_hit
        record_trampoline_hit(orig.__module__ + '.' + orig.__name__)
        result = orig(*call_args, **call_kwargs)
        return result
    prefix = orig.__module__ + '.' + orig.__name__ + '__mutmut_'
    if not mutant_under_test.startswith(prefix):
        result = orig(*call_args, **call_kwargs)
        return result
    mutant_name = mutant_under_test.rpartition('.')[-1]
    if self_arg:
        # call to a class method where self is not bound
        result = mutants[mutant_name](self_arg, *call_args, **call_kwargs)
    else:
        result = mutants[mutant_name](*call_args, **call_kwargs)
    return result


class ProfileMetrics:
    """Thread-safe metrics collection for profiling Foundation performance.

    Tracks message processing performance, emoji overhead, and throughput
    metrics for Foundation's logging infrastructure.

    Example:
        >>> metrics = ProfileMetrics()
        >>> metrics.record_message(duration_ns=1500000, has_emoji=True, field_count=5)
        >>> print(f"Avg latency: {metrics.avg_latency_ms:.2f}ms")
        >>> print(f"Throughput: {metrics.messages_per_second:.0f} msg/sec")

    """

    def xǁProfileMetricsǁ__init____mutmut_orig(self) -> None:
        """Initialize metrics with zero values and current timestamp."""
        self._lock = threading.Lock()
        self.reset()

    def xǁProfileMetricsǁ__init____mutmut_1(self) -> None:
        """Initialize metrics with zero values and current timestamp."""
        self._lock = None
        self.reset()
    
    xǁProfileMetricsǁ__init____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁProfileMetricsǁ__init____mutmut_1': xǁProfileMetricsǁ__init____mutmut_1
    }
    
    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁProfileMetricsǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁProfileMetricsǁ__init____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __init__.__signature__ = _mutmut_signature(xǁProfileMetricsǁ__init____mutmut_orig)
    xǁProfileMetricsǁ__init____mutmut_orig.__name__ = 'xǁProfileMetricsǁ__init__'

    def xǁProfileMetricsǁrecord_message__mutmut_orig(
        self,
        duration_ns: int,
        has_emoji: bool,
        field_count: int,
    ) -> None:
        """Record a processed message with timing and metadata.

        Args:
            duration_ns: Processing duration in nanoseconds
            has_emoji: Whether the message contained emoji processing
            field_count: Number of fields in the log event

        """
        with self._lock:
            self.message_count += 1
            self.total_duration_ns += duration_ns

            if has_emoji:
                self.emoji_message_count += 1

            # Track field complexity (for future analysis)
            self._total_field_count += field_count

    def xǁProfileMetricsǁrecord_message__mutmut_1(
        self,
        duration_ns: int,
        has_emoji: bool,
        field_count: int,
    ) -> None:
        """Record a processed message with timing and metadata.

        Args:
            duration_ns: Processing duration in nanoseconds
            has_emoji: Whether the message contained emoji processing
            field_count: Number of fields in the log event

        """
        with self._lock:
            self.message_count = 1
            self.total_duration_ns += duration_ns

            if has_emoji:
                self.emoji_message_count += 1

            # Track field complexity (for future analysis)
            self._total_field_count += field_count

    def xǁProfileMetricsǁrecord_message__mutmut_2(
        self,
        duration_ns: int,
        has_emoji: bool,
        field_count: int,
    ) -> None:
        """Record a processed message with timing and metadata.

        Args:
            duration_ns: Processing duration in nanoseconds
            has_emoji: Whether the message contained emoji processing
            field_count: Number of fields in the log event

        """
        with self._lock:
            self.message_count -= 1
            self.total_duration_ns += duration_ns

            if has_emoji:
                self.emoji_message_count += 1

            # Track field complexity (for future analysis)
            self._total_field_count += field_count

    def xǁProfileMetricsǁrecord_message__mutmut_3(
        self,
        duration_ns: int,
        has_emoji: bool,
        field_count: int,
    ) -> None:
        """Record a processed message with timing and metadata.

        Args:
            duration_ns: Processing duration in nanoseconds
            has_emoji: Whether the message contained emoji processing
            field_count: Number of fields in the log event

        """
        with self._lock:
            self.message_count += 2
            self.total_duration_ns += duration_ns

            if has_emoji:
                self.emoji_message_count += 1

            # Track field complexity (for future analysis)
            self._total_field_count += field_count

    def xǁProfileMetricsǁrecord_message__mutmut_4(
        self,
        duration_ns: int,
        has_emoji: bool,
        field_count: int,
    ) -> None:
        """Record a processed message with timing and metadata.

        Args:
            duration_ns: Processing duration in nanoseconds
            has_emoji: Whether the message contained emoji processing
            field_count: Number of fields in the log event

        """
        with self._lock:
            self.message_count += 1
            self.total_duration_ns = duration_ns

            if has_emoji:
                self.emoji_message_count += 1

            # Track field complexity (for future analysis)
            self._total_field_count += field_count

    def xǁProfileMetricsǁrecord_message__mutmut_5(
        self,
        duration_ns: int,
        has_emoji: bool,
        field_count: int,
    ) -> None:
        """Record a processed message with timing and metadata.

        Args:
            duration_ns: Processing duration in nanoseconds
            has_emoji: Whether the message contained emoji processing
            field_count: Number of fields in the log event

        """
        with self._lock:
            self.message_count += 1
            self.total_duration_ns -= duration_ns

            if has_emoji:
                self.emoji_message_count += 1

            # Track field complexity (for future analysis)
            self._total_field_count += field_count

    def xǁProfileMetricsǁrecord_message__mutmut_6(
        self,
        duration_ns: int,
        has_emoji: bool,
        field_count: int,
    ) -> None:
        """Record a processed message with timing and metadata.

        Args:
            duration_ns: Processing duration in nanoseconds
            has_emoji: Whether the message contained emoji processing
            field_count: Number of fields in the log event

        """
        with self._lock:
            self.message_count += 1
            self.total_duration_ns += duration_ns

            if has_emoji:
                self.emoji_message_count = 1

            # Track field complexity (for future analysis)
            self._total_field_count += field_count

    def xǁProfileMetricsǁrecord_message__mutmut_7(
        self,
        duration_ns: int,
        has_emoji: bool,
        field_count: int,
    ) -> None:
        """Record a processed message with timing and metadata.

        Args:
            duration_ns: Processing duration in nanoseconds
            has_emoji: Whether the message contained emoji processing
            field_count: Number of fields in the log event

        """
        with self._lock:
            self.message_count += 1
            self.total_duration_ns += duration_ns

            if has_emoji:
                self.emoji_message_count -= 1

            # Track field complexity (for future analysis)
            self._total_field_count += field_count

    def xǁProfileMetricsǁrecord_message__mutmut_8(
        self,
        duration_ns: int,
        has_emoji: bool,
        field_count: int,
    ) -> None:
        """Record a processed message with timing and metadata.

        Args:
            duration_ns: Processing duration in nanoseconds
            has_emoji: Whether the message contained emoji processing
            field_count: Number of fields in the log event

        """
        with self._lock:
            self.message_count += 1
            self.total_duration_ns += duration_ns

            if has_emoji:
                self.emoji_message_count += 2

            # Track field complexity (for future analysis)
            self._total_field_count += field_count

    def xǁProfileMetricsǁrecord_message__mutmut_9(
        self,
        duration_ns: int,
        has_emoji: bool,
        field_count: int,
    ) -> None:
        """Record a processed message with timing and metadata.

        Args:
            duration_ns: Processing duration in nanoseconds
            has_emoji: Whether the message contained emoji processing
            field_count: Number of fields in the log event

        """
        with self._lock:
            self.message_count += 1
            self.total_duration_ns += duration_ns

            if has_emoji:
                self.emoji_message_count += 1

            # Track field complexity (for future analysis)
            self._total_field_count = field_count

    def xǁProfileMetricsǁrecord_message__mutmut_10(
        self,
        duration_ns: int,
        has_emoji: bool,
        field_count: int,
    ) -> None:
        """Record a processed message with timing and metadata.

        Args:
            duration_ns: Processing duration in nanoseconds
            has_emoji: Whether the message contained emoji processing
            field_count: Number of fields in the log event

        """
        with self._lock:
            self.message_count += 1
            self.total_duration_ns += duration_ns

            if has_emoji:
                self.emoji_message_count += 1

            # Track field complexity (for future analysis)
            self._total_field_count -= field_count
    
    xǁProfileMetricsǁrecord_message__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁProfileMetricsǁrecord_message__mutmut_1': xǁProfileMetricsǁrecord_message__mutmut_1, 
        'xǁProfileMetricsǁrecord_message__mutmut_2': xǁProfileMetricsǁrecord_message__mutmut_2, 
        'xǁProfileMetricsǁrecord_message__mutmut_3': xǁProfileMetricsǁrecord_message__mutmut_3, 
        'xǁProfileMetricsǁrecord_message__mutmut_4': xǁProfileMetricsǁrecord_message__mutmut_4, 
        'xǁProfileMetricsǁrecord_message__mutmut_5': xǁProfileMetricsǁrecord_message__mutmut_5, 
        'xǁProfileMetricsǁrecord_message__mutmut_6': xǁProfileMetricsǁrecord_message__mutmut_6, 
        'xǁProfileMetricsǁrecord_message__mutmut_7': xǁProfileMetricsǁrecord_message__mutmut_7, 
        'xǁProfileMetricsǁrecord_message__mutmut_8': xǁProfileMetricsǁrecord_message__mutmut_8, 
        'xǁProfileMetricsǁrecord_message__mutmut_9': xǁProfileMetricsǁrecord_message__mutmut_9, 
        'xǁProfileMetricsǁrecord_message__mutmut_10': xǁProfileMetricsǁrecord_message__mutmut_10
    }
    
    def record_message(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁProfileMetricsǁrecord_message__mutmut_orig"), object.__getattribute__(self, "xǁProfileMetricsǁrecord_message__mutmut_mutants"), args, kwargs, self)
        return result 
    
    record_message.__signature__ = _mutmut_signature(xǁProfileMetricsǁrecord_message__mutmut_orig)
    xǁProfileMetricsǁrecord_message__mutmut_orig.__name__ = 'xǁProfileMetricsǁrecord_message'

    def xǁProfileMetricsǁreset__mutmut_orig(self) -> None:
        """Reset all metrics to initial values with new start time."""
        with self._lock:
            self.message_count = 0
            self.total_duration_ns = 0
            self.emoji_message_count = 0
            self.dropped_count = 0
            self.start_time = time.time()
            self._total_field_count = 0

    def xǁProfileMetricsǁreset__mutmut_1(self) -> None:
        """Reset all metrics to initial values with new start time."""
        with self._lock:
            self.message_count = None
            self.total_duration_ns = 0
            self.emoji_message_count = 0
            self.dropped_count = 0
            self.start_time = time.time()
            self._total_field_count = 0

    def xǁProfileMetricsǁreset__mutmut_2(self) -> None:
        """Reset all metrics to initial values with new start time."""
        with self._lock:
            self.message_count = 1
            self.total_duration_ns = 0
            self.emoji_message_count = 0
            self.dropped_count = 0
            self.start_time = time.time()
            self._total_field_count = 0

    def xǁProfileMetricsǁreset__mutmut_3(self) -> None:
        """Reset all metrics to initial values with new start time."""
        with self._lock:
            self.message_count = 0
            self.total_duration_ns = None
            self.emoji_message_count = 0
            self.dropped_count = 0
            self.start_time = time.time()
            self._total_field_count = 0

    def xǁProfileMetricsǁreset__mutmut_4(self) -> None:
        """Reset all metrics to initial values with new start time."""
        with self._lock:
            self.message_count = 0
            self.total_duration_ns = 1
            self.emoji_message_count = 0
            self.dropped_count = 0
            self.start_time = time.time()
            self._total_field_count = 0

    def xǁProfileMetricsǁreset__mutmut_5(self) -> None:
        """Reset all metrics to initial values with new start time."""
        with self._lock:
            self.message_count = 0
            self.total_duration_ns = 0
            self.emoji_message_count = None
            self.dropped_count = 0
            self.start_time = time.time()
            self._total_field_count = 0

    def xǁProfileMetricsǁreset__mutmut_6(self) -> None:
        """Reset all metrics to initial values with new start time."""
        with self._lock:
            self.message_count = 0
            self.total_duration_ns = 0
            self.emoji_message_count = 1
            self.dropped_count = 0
            self.start_time = time.time()
            self._total_field_count = 0

    def xǁProfileMetricsǁreset__mutmut_7(self) -> None:
        """Reset all metrics to initial values with new start time."""
        with self._lock:
            self.message_count = 0
            self.total_duration_ns = 0
            self.emoji_message_count = 0
            self.dropped_count = None
            self.start_time = time.time()
            self._total_field_count = 0

    def xǁProfileMetricsǁreset__mutmut_8(self) -> None:
        """Reset all metrics to initial values with new start time."""
        with self._lock:
            self.message_count = 0
            self.total_duration_ns = 0
            self.emoji_message_count = 0
            self.dropped_count = 1
            self.start_time = time.time()
            self._total_field_count = 0

    def xǁProfileMetricsǁreset__mutmut_9(self) -> None:
        """Reset all metrics to initial values with new start time."""
        with self._lock:
            self.message_count = 0
            self.total_duration_ns = 0
            self.emoji_message_count = 0
            self.dropped_count = 0
            self.start_time = None
            self._total_field_count = 0

    def xǁProfileMetricsǁreset__mutmut_10(self) -> None:
        """Reset all metrics to initial values with new start time."""
        with self._lock:
            self.message_count = 0
            self.total_duration_ns = 0
            self.emoji_message_count = 0
            self.dropped_count = 0
            self.start_time = time.time()
            self._total_field_count = None

    def xǁProfileMetricsǁreset__mutmut_11(self) -> None:
        """Reset all metrics to initial values with new start time."""
        with self._lock:
            self.message_count = 0
            self.total_duration_ns = 0
            self.emoji_message_count = 0
            self.dropped_count = 0
            self.start_time = time.time()
            self._total_field_count = 1
    
    xǁProfileMetricsǁreset__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁProfileMetricsǁreset__mutmut_1': xǁProfileMetricsǁreset__mutmut_1, 
        'xǁProfileMetricsǁreset__mutmut_2': xǁProfileMetricsǁreset__mutmut_2, 
        'xǁProfileMetricsǁreset__mutmut_3': xǁProfileMetricsǁreset__mutmut_3, 
        'xǁProfileMetricsǁreset__mutmut_4': xǁProfileMetricsǁreset__mutmut_4, 
        'xǁProfileMetricsǁreset__mutmut_5': xǁProfileMetricsǁreset__mutmut_5, 
        'xǁProfileMetricsǁreset__mutmut_6': xǁProfileMetricsǁreset__mutmut_6, 
        'xǁProfileMetricsǁreset__mutmut_7': xǁProfileMetricsǁreset__mutmut_7, 
        'xǁProfileMetricsǁreset__mutmut_8': xǁProfileMetricsǁreset__mutmut_8, 
        'xǁProfileMetricsǁreset__mutmut_9': xǁProfileMetricsǁreset__mutmut_9, 
        'xǁProfileMetricsǁreset__mutmut_10': xǁProfileMetricsǁreset__mutmut_10, 
        'xǁProfileMetricsǁreset__mutmut_11': xǁProfileMetricsǁreset__mutmut_11
    }
    
    def reset(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁProfileMetricsǁreset__mutmut_orig"), object.__getattribute__(self, "xǁProfileMetricsǁreset__mutmut_mutants"), args, kwargs, self)
        return result 
    
    reset.__signature__ = _mutmut_signature(xǁProfileMetricsǁreset__mutmut_orig)
    xǁProfileMetricsǁreset__mutmut_orig.__name__ = 'xǁProfileMetricsǁreset'

    @property
    def messages_per_second(self) -> float:
        """Calculate messages per second since start time."""
        with self._lock:
            elapsed = time.time() - self.start_time
            if elapsed <= 0:
                return 0.0
            return self.message_count / elapsed

    @property
    def avg_latency_ms(self) -> float:
        """Calculate average processing latency in milliseconds."""
        with self._lock:
            if self.message_count == 0:
                return 0.0
            return (self.total_duration_ns / self.message_count) / 1_000_000

    @property
    def emoji_overhead_percent(self) -> float:
        """Calculate percentage of messages with emoji processing."""
        with self._lock:
            if self.message_count == 0:
                return 0.0
            return (self.emoji_message_count / self.message_count) * 100

    @property
    def avg_fields_per_message(self) -> float:
        """Calculate average number of fields per message."""
        with self._lock:
            if self.message_count == 0:
                return 0.0
            return self._total_field_count / self.message_count

    def xǁProfileMetricsǁto_dict__mutmut_orig(self) -> dict[str, Any]:
        """Serialize metrics to dictionary for JSON output.

        Returns:
            Dictionary containing all current metrics

        """
        with self._lock:
            # Calculate metrics directly to avoid deadlock from property calls
            elapsed = time.time() - self.start_time
            messages_per_second = self.message_count / elapsed if elapsed > 0 else 0.0
            avg_latency_ms = (
                (self.total_duration_ns / self.message_count) / 1_000_000 if self.message_count > 0 else 0.0
            )
            emoji_overhead_percent = (
                (self.emoji_message_count / self.message_count) * 100 if self.message_count > 0 else 0.0
            )
            avg_fields_per_message = (
                self._total_field_count / self.message_count if self.message_count > 0 else 0.0
            )

            return {
                "messages_per_second": round(messages_per_second, 2),
                "avg_latency_ms": round(avg_latency_ms, 4),
                "emoji_overhead_percent": round(emoji_overhead_percent, 1),
                "total_messages": self.message_count,
                "emoji_messages": self.emoji_message_count,
                "dropped_messages": self.dropped_count,
                "avg_fields_per_message": round(avg_fields_per_message, 1),
                "uptime_seconds": round(elapsed, 1),
            }

    def xǁProfileMetricsǁto_dict__mutmut_1(self) -> dict[str, Any]:
        """Serialize metrics to dictionary for JSON output.

        Returns:
            Dictionary containing all current metrics

        """
        with self._lock:
            # Calculate metrics directly to avoid deadlock from property calls
            elapsed = None
            messages_per_second = self.message_count / elapsed if elapsed > 0 else 0.0
            avg_latency_ms = (
                (self.total_duration_ns / self.message_count) / 1_000_000 if self.message_count > 0 else 0.0
            )
            emoji_overhead_percent = (
                (self.emoji_message_count / self.message_count) * 100 if self.message_count > 0 else 0.0
            )
            avg_fields_per_message = (
                self._total_field_count / self.message_count if self.message_count > 0 else 0.0
            )

            return {
                "messages_per_second": round(messages_per_second, 2),
                "avg_latency_ms": round(avg_latency_ms, 4),
                "emoji_overhead_percent": round(emoji_overhead_percent, 1),
                "total_messages": self.message_count,
                "emoji_messages": self.emoji_message_count,
                "dropped_messages": self.dropped_count,
                "avg_fields_per_message": round(avg_fields_per_message, 1),
                "uptime_seconds": round(elapsed, 1),
            }

    def xǁProfileMetricsǁto_dict__mutmut_2(self) -> dict[str, Any]:
        """Serialize metrics to dictionary for JSON output.

        Returns:
            Dictionary containing all current metrics

        """
        with self._lock:
            # Calculate metrics directly to avoid deadlock from property calls
            elapsed = time.time() + self.start_time
            messages_per_second = self.message_count / elapsed if elapsed > 0 else 0.0
            avg_latency_ms = (
                (self.total_duration_ns / self.message_count) / 1_000_000 if self.message_count > 0 else 0.0
            )
            emoji_overhead_percent = (
                (self.emoji_message_count / self.message_count) * 100 if self.message_count > 0 else 0.0
            )
            avg_fields_per_message = (
                self._total_field_count / self.message_count if self.message_count > 0 else 0.0
            )

            return {
                "messages_per_second": round(messages_per_second, 2),
                "avg_latency_ms": round(avg_latency_ms, 4),
                "emoji_overhead_percent": round(emoji_overhead_percent, 1),
                "total_messages": self.message_count,
                "emoji_messages": self.emoji_message_count,
                "dropped_messages": self.dropped_count,
                "avg_fields_per_message": round(avg_fields_per_message, 1),
                "uptime_seconds": round(elapsed, 1),
            }

    def xǁProfileMetricsǁto_dict__mutmut_3(self) -> dict[str, Any]:
        """Serialize metrics to dictionary for JSON output.

        Returns:
            Dictionary containing all current metrics

        """
        with self._lock:
            # Calculate metrics directly to avoid deadlock from property calls
            elapsed = time.time() - self.start_time
            messages_per_second = None
            avg_latency_ms = (
                (self.total_duration_ns / self.message_count) / 1_000_000 if self.message_count > 0 else 0.0
            )
            emoji_overhead_percent = (
                (self.emoji_message_count / self.message_count) * 100 if self.message_count > 0 else 0.0
            )
            avg_fields_per_message = (
                self._total_field_count / self.message_count if self.message_count > 0 else 0.0
            )

            return {
                "messages_per_second": round(messages_per_second, 2),
                "avg_latency_ms": round(avg_latency_ms, 4),
                "emoji_overhead_percent": round(emoji_overhead_percent, 1),
                "total_messages": self.message_count,
                "emoji_messages": self.emoji_message_count,
                "dropped_messages": self.dropped_count,
                "avg_fields_per_message": round(avg_fields_per_message, 1),
                "uptime_seconds": round(elapsed, 1),
            }

    def xǁProfileMetricsǁto_dict__mutmut_4(self) -> dict[str, Any]:
        """Serialize metrics to dictionary for JSON output.

        Returns:
            Dictionary containing all current metrics

        """
        with self._lock:
            # Calculate metrics directly to avoid deadlock from property calls
            elapsed = time.time() - self.start_time
            messages_per_second = self.message_count * elapsed if elapsed > 0 else 0.0
            avg_latency_ms = (
                (self.total_duration_ns / self.message_count) / 1_000_000 if self.message_count > 0 else 0.0
            )
            emoji_overhead_percent = (
                (self.emoji_message_count / self.message_count) * 100 if self.message_count > 0 else 0.0
            )
            avg_fields_per_message = (
                self._total_field_count / self.message_count if self.message_count > 0 else 0.0
            )

            return {
                "messages_per_second": round(messages_per_second, 2),
                "avg_latency_ms": round(avg_latency_ms, 4),
                "emoji_overhead_percent": round(emoji_overhead_percent, 1),
                "total_messages": self.message_count,
                "emoji_messages": self.emoji_message_count,
                "dropped_messages": self.dropped_count,
                "avg_fields_per_message": round(avg_fields_per_message, 1),
                "uptime_seconds": round(elapsed, 1),
            }

    def xǁProfileMetricsǁto_dict__mutmut_5(self) -> dict[str, Any]:
        """Serialize metrics to dictionary for JSON output.

        Returns:
            Dictionary containing all current metrics

        """
        with self._lock:
            # Calculate metrics directly to avoid deadlock from property calls
            elapsed = time.time() - self.start_time
            messages_per_second = self.message_count / elapsed if elapsed >= 0 else 0.0
            avg_latency_ms = (
                (self.total_duration_ns / self.message_count) / 1_000_000 if self.message_count > 0 else 0.0
            )
            emoji_overhead_percent = (
                (self.emoji_message_count / self.message_count) * 100 if self.message_count > 0 else 0.0
            )
            avg_fields_per_message = (
                self._total_field_count / self.message_count if self.message_count > 0 else 0.0
            )

            return {
                "messages_per_second": round(messages_per_second, 2),
                "avg_latency_ms": round(avg_latency_ms, 4),
                "emoji_overhead_percent": round(emoji_overhead_percent, 1),
                "total_messages": self.message_count,
                "emoji_messages": self.emoji_message_count,
                "dropped_messages": self.dropped_count,
                "avg_fields_per_message": round(avg_fields_per_message, 1),
                "uptime_seconds": round(elapsed, 1),
            }

    def xǁProfileMetricsǁto_dict__mutmut_6(self) -> dict[str, Any]:
        """Serialize metrics to dictionary for JSON output.

        Returns:
            Dictionary containing all current metrics

        """
        with self._lock:
            # Calculate metrics directly to avoid deadlock from property calls
            elapsed = time.time() - self.start_time
            messages_per_second = self.message_count / elapsed if elapsed > 1 else 0.0
            avg_latency_ms = (
                (self.total_duration_ns / self.message_count) / 1_000_000 if self.message_count > 0 else 0.0
            )
            emoji_overhead_percent = (
                (self.emoji_message_count / self.message_count) * 100 if self.message_count > 0 else 0.0
            )
            avg_fields_per_message = (
                self._total_field_count / self.message_count if self.message_count > 0 else 0.0
            )

            return {
                "messages_per_second": round(messages_per_second, 2),
                "avg_latency_ms": round(avg_latency_ms, 4),
                "emoji_overhead_percent": round(emoji_overhead_percent, 1),
                "total_messages": self.message_count,
                "emoji_messages": self.emoji_message_count,
                "dropped_messages": self.dropped_count,
                "avg_fields_per_message": round(avg_fields_per_message, 1),
                "uptime_seconds": round(elapsed, 1),
            }

    def xǁProfileMetricsǁto_dict__mutmut_7(self) -> dict[str, Any]:
        """Serialize metrics to dictionary for JSON output.

        Returns:
            Dictionary containing all current metrics

        """
        with self._lock:
            # Calculate metrics directly to avoid deadlock from property calls
            elapsed = time.time() - self.start_time
            messages_per_second = self.message_count / elapsed if elapsed > 0 else 1.0
            avg_latency_ms = (
                (self.total_duration_ns / self.message_count) / 1_000_000 if self.message_count > 0 else 0.0
            )
            emoji_overhead_percent = (
                (self.emoji_message_count / self.message_count) * 100 if self.message_count > 0 else 0.0
            )
            avg_fields_per_message = (
                self._total_field_count / self.message_count if self.message_count > 0 else 0.0
            )

            return {
                "messages_per_second": round(messages_per_second, 2),
                "avg_latency_ms": round(avg_latency_ms, 4),
                "emoji_overhead_percent": round(emoji_overhead_percent, 1),
                "total_messages": self.message_count,
                "emoji_messages": self.emoji_message_count,
                "dropped_messages": self.dropped_count,
                "avg_fields_per_message": round(avg_fields_per_message, 1),
                "uptime_seconds": round(elapsed, 1),
            }

    def xǁProfileMetricsǁto_dict__mutmut_8(self) -> dict[str, Any]:
        """Serialize metrics to dictionary for JSON output.

        Returns:
            Dictionary containing all current metrics

        """
        with self._lock:
            # Calculate metrics directly to avoid deadlock from property calls
            elapsed = time.time() - self.start_time
            messages_per_second = self.message_count / elapsed if elapsed > 0 else 0.0
            avg_latency_ms = None
            emoji_overhead_percent = (
                (self.emoji_message_count / self.message_count) * 100 if self.message_count > 0 else 0.0
            )
            avg_fields_per_message = (
                self._total_field_count / self.message_count if self.message_count > 0 else 0.0
            )

            return {
                "messages_per_second": round(messages_per_second, 2),
                "avg_latency_ms": round(avg_latency_ms, 4),
                "emoji_overhead_percent": round(emoji_overhead_percent, 1),
                "total_messages": self.message_count,
                "emoji_messages": self.emoji_message_count,
                "dropped_messages": self.dropped_count,
                "avg_fields_per_message": round(avg_fields_per_message, 1),
                "uptime_seconds": round(elapsed, 1),
            }

    def xǁProfileMetricsǁto_dict__mutmut_9(self) -> dict[str, Any]:
        """Serialize metrics to dictionary for JSON output.

        Returns:
            Dictionary containing all current metrics

        """
        with self._lock:
            # Calculate metrics directly to avoid deadlock from property calls
            elapsed = time.time() - self.start_time
            messages_per_second = self.message_count / elapsed if elapsed > 0 else 0.0
            avg_latency_ms = (
                (self.total_duration_ns / self.message_count) * 1_000_000 if self.message_count > 0 else 0.0
            )
            emoji_overhead_percent = (
                (self.emoji_message_count / self.message_count) * 100 if self.message_count > 0 else 0.0
            )
            avg_fields_per_message = (
                self._total_field_count / self.message_count if self.message_count > 0 else 0.0
            )

            return {
                "messages_per_second": round(messages_per_second, 2),
                "avg_latency_ms": round(avg_latency_ms, 4),
                "emoji_overhead_percent": round(emoji_overhead_percent, 1),
                "total_messages": self.message_count,
                "emoji_messages": self.emoji_message_count,
                "dropped_messages": self.dropped_count,
                "avg_fields_per_message": round(avg_fields_per_message, 1),
                "uptime_seconds": round(elapsed, 1),
            }

    def xǁProfileMetricsǁto_dict__mutmut_10(self) -> dict[str, Any]:
        """Serialize metrics to dictionary for JSON output.

        Returns:
            Dictionary containing all current metrics

        """
        with self._lock:
            # Calculate metrics directly to avoid deadlock from property calls
            elapsed = time.time() - self.start_time
            messages_per_second = self.message_count / elapsed if elapsed > 0 else 0.0
            avg_latency_ms = (
                (self.total_duration_ns * self.message_count) / 1_000_000 if self.message_count > 0 else 0.0
            )
            emoji_overhead_percent = (
                (self.emoji_message_count / self.message_count) * 100 if self.message_count > 0 else 0.0
            )
            avg_fields_per_message = (
                self._total_field_count / self.message_count if self.message_count > 0 else 0.0
            )

            return {
                "messages_per_second": round(messages_per_second, 2),
                "avg_latency_ms": round(avg_latency_ms, 4),
                "emoji_overhead_percent": round(emoji_overhead_percent, 1),
                "total_messages": self.message_count,
                "emoji_messages": self.emoji_message_count,
                "dropped_messages": self.dropped_count,
                "avg_fields_per_message": round(avg_fields_per_message, 1),
                "uptime_seconds": round(elapsed, 1),
            }

    def xǁProfileMetricsǁto_dict__mutmut_11(self) -> dict[str, Any]:
        """Serialize metrics to dictionary for JSON output.

        Returns:
            Dictionary containing all current metrics

        """
        with self._lock:
            # Calculate metrics directly to avoid deadlock from property calls
            elapsed = time.time() - self.start_time
            messages_per_second = self.message_count / elapsed if elapsed > 0 else 0.0
            avg_latency_ms = (
                (self.total_duration_ns / self.message_count) / 1000001 if self.message_count > 0 else 0.0
            )
            emoji_overhead_percent = (
                (self.emoji_message_count / self.message_count) * 100 if self.message_count > 0 else 0.0
            )
            avg_fields_per_message = (
                self._total_field_count / self.message_count if self.message_count > 0 else 0.0
            )

            return {
                "messages_per_second": round(messages_per_second, 2),
                "avg_latency_ms": round(avg_latency_ms, 4),
                "emoji_overhead_percent": round(emoji_overhead_percent, 1),
                "total_messages": self.message_count,
                "emoji_messages": self.emoji_message_count,
                "dropped_messages": self.dropped_count,
                "avg_fields_per_message": round(avg_fields_per_message, 1),
                "uptime_seconds": round(elapsed, 1),
            }

    def xǁProfileMetricsǁto_dict__mutmut_12(self) -> dict[str, Any]:
        """Serialize metrics to dictionary for JSON output.

        Returns:
            Dictionary containing all current metrics

        """
        with self._lock:
            # Calculate metrics directly to avoid deadlock from property calls
            elapsed = time.time() - self.start_time
            messages_per_second = self.message_count / elapsed if elapsed > 0 else 0.0
            avg_latency_ms = (
                (self.total_duration_ns / self.message_count) / 1_000_000 if self.message_count >= 0 else 0.0
            )
            emoji_overhead_percent = (
                (self.emoji_message_count / self.message_count) * 100 if self.message_count > 0 else 0.0
            )
            avg_fields_per_message = (
                self._total_field_count / self.message_count if self.message_count > 0 else 0.0
            )

            return {
                "messages_per_second": round(messages_per_second, 2),
                "avg_latency_ms": round(avg_latency_ms, 4),
                "emoji_overhead_percent": round(emoji_overhead_percent, 1),
                "total_messages": self.message_count,
                "emoji_messages": self.emoji_message_count,
                "dropped_messages": self.dropped_count,
                "avg_fields_per_message": round(avg_fields_per_message, 1),
                "uptime_seconds": round(elapsed, 1),
            }

    def xǁProfileMetricsǁto_dict__mutmut_13(self) -> dict[str, Any]:
        """Serialize metrics to dictionary for JSON output.

        Returns:
            Dictionary containing all current metrics

        """
        with self._lock:
            # Calculate metrics directly to avoid deadlock from property calls
            elapsed = time.time() - self.start_time
            messages_per_second = self.message_count / elapsed if elapsed > 0 else 0.0
            avg_latency_ms = (
                (self.total_duration_ns / self.message_count) / 1_000_000 if self.message_count > 1 else 0.0
            )
            emoji_overhead_percent = (
                (self.emoji_message_count / self.message_count) * 100 if self.message_count > 0 else 0.0
            )
            avg_fields_per_message = (
                self._total_field_count / self.message_count if self.message_count > 0 else 0.0
            )

            return {
                "messages_per_second": round(messages_per_second, 2),
                "avg_latency_ms": round(avg_latency_ms, 4),
                "emoji_overhead_percent": round(emoji_overhead_percent, 1),
                "total_messages": self.message_count,
                "emoji_messages": self.emoji_message_count,
                "dropped_messages": self.dropped_count,
                "avg_fields_per_message": round(avg_fields_per_message, 1),
                "uptime_seconds": round(elapsed, 1),
            }

    def xǁProfileMetricsǁto_dict__mutmut_14(self) -> dict[str, Any]:
        """Serialize metrics to dictionary for JSON output.

        Returns:
            Dictionary containing all current metrics

        """
        with self._lock:
            # Calculate metrics directly to avoid deadlock from property calls
            elapsed = time.time() - self.start_time
            messages_per_second = self.message_count / elapsed if elapsed > 0 else 0.0
            avg_latency_ms = (
                (self.total_duration_ns / self.message_count) / 1_000_000 if self.message_count > 0 else 1.0
            )
            emoji_overhead_percent = (
                (self.emoji_message_count / self.message_count) * 100 if self.message_count > 0 else 0.0
            )
            avg_fields_per_message = (
                self._total_field_count / self.message_count if self.message_count > 0 else 0.0
            )

            return {
                "messages_per_second": round(messages_per_second, 2),
                "avg_latency_ms": round(avg_latency_ms, 4),
                "emoji_overhead_percent": round(emoji_overhead_percent, 1),
                "total_messages": self.message_count,
                "emoji_messages": self.emoji_message_count,
                "dropped_messages": self.dropped_count,
                "avg_fields_per_message": round(avg_fields_per_message, 1),
                "uptime_seconds": round(elapsed, 1),
            }

    def xǁProfileMetricsǁto_dict__mutmut_15(self) -> dict[str, Any]:
        """Serialize metrics to dictionary for JSON output.

        Returns:
            Dictionary containing all current metrics

        """
        with self._lock:
            # Calculate metrics directly to avoid deadlock from property calls
            elapsed = time.time() - self.start_time
            messages_per_second = self.message_count / elapsed if elapsed > 0 else 0.0
            avg_latency_ms = (
                (self.total_duration_ns / self.message_count) / 1_000_000 if self.message_count > 0 else 0.0
            )
            emoji_overhead_percent = None
            avg_fields_per_message = (
                self._total_field_count / self.message_count if self.message_count > 0 else 0.0
            )

            return {
                "messages_per_second": round(messages_per_second, 2),
                "avg_latency_ms": round(avg_latency_ms, 4),
                "emoji_overhead_percent": round(emoji_overhead_percent, 1),
                "total_messages": self.message_count,
                "emoji_messages": self.emoji_message_count,
                "dropped_messages": self.dropped_count,
                "avg_fields_per_message": round(avg_fields_per_message, 1),
                "uptime_seconds": round(elapsed, 1),
            }

    def xǁProfileMetricsǁto_dict__mutmut_16(self) -> dict[str, Any]:
        """Serialize metrics to dictionary for JSON output.

        Returns:
            Dictionary containing all current metrics

        """
        with self._lock:
            # Calculate metrics directly to avoid deadlock from property calls
            elapsed = time.time() - self.start_time
            messages_per_second = self.message_count / elapsed if elapsed > 0 else 0.0
            avg_latency_ms = (
                (self.total_duration_ns / self.message_count) / 1_000_000 if self.message_count > 0 else 0.0
            )
            emoji_overhead_percent = (
                (self.emoji_message_count / self.message_count) / 100 if self.message_count > 0 else 0.0
            )
            avg_fields_per_message = (
                self._total_field_count / self.message_count if self.message_count > 0 else 0.0
            )

            return {
                "messages_per_second": round(messages_per_second, 2),
                "avg_latency_ms": round(avg_latency_ms, 4),
                "emoji_overhead_percent": round(emoji_overhead_percent, 1),
                "total_messages": self.message_count,
                "emoji_messages": self.emoji_message_count,
                "dropped_messages": self.dropped_count,
                "avg_fields_per_message": round(avg_fields_per_message, 1),
                "uptime_seconds": round(elapsed, 1),
            }

    def xǁProfileMetricsǁto_dict__mutmut_17(self) -> dict[str, Any]:
        """Serialize metrics to dictionary for JSON output.

        Returns:
            Dictionary containing all current metrics

        """
        with self._lock:
            # Calculate metrics directly to avoid deadlock from property calls
            elapsed = time.time() - self.start_time
            messages_per_second = self.message_count / elapsed if elapsed > 0 else 0.0
            avg_latency_ms = (
                (self.total_duration_ns / self.message_count) / 1_000_000 if self.message_count > 0 else 0.0
            )
            emoji_overhead_percent = (
                (self.emoji_message_count * self.message_count) * 100 if self.message_count > 0 else 0.0
            )
            avg_fields_per_message = (
                self._total_field_count / self.message_count if self.message_count > 0 else 0.0
            )

            return {
                "messages_per_second": round(messages_per_second, 2),
                "avg_latency_ms": round(avg_latency_ms, 4),
                "emoji_overhead_percent": round(emoji_overhead_percent, 1),
                "total_messages": self.message_count,
                "emoji_messages": self.emoji_message_count,
                "dropped_messages": self.dropped_count,
                "avg_fields_per_message": round(avg_fields_per_message, 1),
                "uptime_seconds": round(elapsed, 1),
            }

    def xǁProfileMetricsǁto_dict__mutmut_18(self) -> dict[str, Any]:
        """Serialize metrics to dictionary for JSON output.

        Returns:
            Dictionary containing all current metrics

        """
        with self._lock:
            # Calculate metrics directly to avoid deadlock from property calls
            elapsed = time.time() - self.start_time
            messages_per_second = self.message_count / elapsed if elapsed > 0 else 0.0
            avg_latency_ms = (
                (self.total_duration_ns / self.message_count) / 1_000_000 if self.message_count > 0 else 0.0
            )
            emoji_overhead_percent = (
                (self.emoji_message_count / self.message_count) * 101 if self.message_count > 0 else 0.0
            )
            avg_fields_per_message = (
                self._total_field_count / self.message_count if self.message_count > 0 else 0.0
            )

            return {
                "messages_per_second": round(messages_per_second, 2),
                "avg_latency_ms": round(avg_latency_ms, 4),
                "emoji_overhead_percent": round(emoji_overhead_percent, 1),
                "total_messages": self.message_count,
                "emoji_messages": self.emoji_message_count,
                "dropped_messages": self.dropped_count,
                "avg_fields_per_message": round(avg_fields_per_message, 1),
                "uptime_seconds": round(elapsed, 1),
            }

    def xǁProfileMetricsǁto_dict__mutmut_19(self) -> dict[str, Any]:
        """Serialize metrics to dictionary for JSON output.

        Returns:
            Dictionary containing all current metrics

        """
        with self._lock:
            # Calculate metrics directly to avoid deadlock from property calls
            elapsed = time.time() - self.start_time
            messages_per_second = self.message_count / elapsed if elapsed > 0 else 0.0
            avg_latency_ms = (
                (self.total_duration_ns / self.message_count) / 1_000_000 if self.message_count > 0 else 0.0
            )
            emoji_overhead_percent = (
                (self.emoji_message_count / self.message_count) * 100 if self.message_count >= 0 else 0.0
            )
            avg_fields_per_message = (
                self._total_field_count / self.message_count if self.message_count > 0 else 0.0
            )

            return {
                "messages_per_second": round(messages_per_second, 2),
                "avg_latency_ms": round(avg_latency_ms, 4),
                "emoji_overhead_percent": round(emoji_overhead_percent, 1),
                "total_messages": self.message_count,
                "emoji_messages": self.emoji_message_count,
                "dropped_messages": self.dropped_count,
                "avg_fields_per_message": round(avg_fields_per_message, 1),
                "uptime_seconds": round(elapsed, 1),
            }

    def xǁProfileMetricsǁto_dict__mutmut_20(self) -> dict[str, Any]:
        """Serialize metrics to dictionary for JSON output.

        Returns:
            Dictionary containing all current metrics

        """
        with self._lock:
            # Calculate metrics directly to avoid deadlock from property calls
            elapsed = time.time() - self.start_time
            messages_per_second = self.message_count / elapsed if elapsed > 0 else 0.0
            avg_latency_ms = (
                (self.total_duration_ns / self.message_count) / 1_000_000 if self.message_count > 0 else 0.0
            )
            emoji_overhead_percent = (
                (self.emoji_message_count / self.message_count) * 100 if self.message_count > 1 else 0.0
            )
            avg_fields_per_message = (
                self._total_field_count / self.message_count if self.message_count > 0 else 0.0
            )

            return {
                "messages_per_second": round(messages_per_second, 2),
                "avg_latency_ms": round(avg_latency_ms, 4),
                "emoji_overhead_percent": round(emoji_overhead_percent, 1),
                "total_messages": self.message_count,
                "emoji_messages": self.emoji_message_count,
                "dropped_messages": self.dropped_count,
                "avg_fields_per_message": round(avg_fields_per_message, 1),
                "uptime_seconds": round(elapsed, 1),
            }

    def xǁProfileMetricsǁto_dict__mutmut_21(self) -> dict[str, Any]:
        """Serialize metrics to dictionary for JSON output.

        Returns:
            Dictionary containing all current metrics

        """
        with self._lock:
            # Calculate metrics directly to avoid deadlock from property calls
            elapsed = time.time() - self.start_time
            messages_per_second = self.message_count / elapsed if elapsed > 0 else 0.0
            avg_latency_ms = (
                (self.total_duration_ns / self.message_count) / 1_000_000 if self.message_count > 0 else 0.0
            )
            emoji_overhead_percent = (
                (self.emoji_message_count / self.message_count) * 100 if self.message_count > 0 else 1.0
            )
            avg_fields_per_message = (
                self._total_field_count / self.message_count if self.message_count > 0 else 0.0
            )

            return {
                "messages_per_second": round(messages_per_second, 2),
                "avg_latency_ms": round(avg_latency_ms, 4),
                "emoji_overhead_percent": round(emoji_overhead_percent, 1),
                "total_messages": self.message_count,
                "emoji_messages": self.emoji_message_count,
                "dropped_messages": self.dropped_count,
                "avg_fields_per_message": round(avg_fields_per_message, 1),
                "uptime_seconds": round(elapsed, 1),
            }

    def xǁProfileMetricsǁto_dict__mutmut_22(self) -> dict[str, Any]:
        """Serialize metrics to dictionary for JSON output.

        Returns:
            Dictionary containing all current metrics

        """
        with self._lock:
            # Calculate metrics directly to avoid deadlock from property calls
            elapsed = time.time() - self.start_time
            messages_per_second = self.message_count / elapsed if elapsed > 0 else 0.0
            avg_latency_ms = (
                (self.total_duration_ns / self.message_count) / 1_000_000 if self.message_count > 0 else 0.0
            )
            emoji_overhead_percent = (
                (self.emoji_message_count / self.message_count) * 100 if self.message_count > 0 else 0.0
            )
            avg_fields_per_message = None

            return {
                "messages_per_second": round(messages_per_second, 2),
                "avg_latency_ms": round(avg_latency_ms, 4),
                "emoji_overhead_percent": round(emoji_overhead_percent, 1),
                "total_messages": self.message_count,
                "emoji_messages": self.emoji_message_count,
                "dropped_messages": self.dropped_count,
                "avg_fields_per_message": round(avg_fields_per_message, 1),
                "uptime_seconds": round(elapsed, 1),
            }

    def xǁProfileMetricsǁto_dict__mutmut_23(self) -> dict[str, Any]:
        """Serialize metrics to dictionary for JSON output.

        Returns:
            Dictionary containing all current metrics

        """
        with self._lock:
            # Calculate metrics directly to avoid deadlock from property calls
            elapsed = time.time() - self.start_time
            messages_per_second = self.message_count / elapsed if elapsed > 0 else 0.0
            avg_latency_ms = (
                (self.total_duration_ns / self.message_count) / 1_000_000 if self.message_count > 0 else 0.0
            )
            emoji_overhead_percent = (
                (self.emoji_message_count / self.message_count) * 100 if self.message_count > 0 else 0.0
            )
            avg_fields_per_message = (
                self._total_field_count * self.message_count if self.message_count > 0 else 0.0
            )

            return {
                "messages_per_second": round(messages_per_second, 2),
                "avg_latency_ms": round(avg_latency_ms, 4),
                "emoji_overhead_percent": round(emoji_overhead_percent, 1),
                "total_messages": self.message_count,
                "emoji_messages": self.emoji_message_count,
                "dropped_messages": self.dropped_count,
                "avg_fields_per_message": round(avg_fields_per_message, 1),
                "uptime_seconds": round(elapsed, 1),
            }

    def xǁProfileMetricsǁto_dict__mutmut_24(self) -> dict[str, Any]:
        """Serialize metrics to dictionary for JSON output.

        Returns:
            Dictionary containing all current metrics

        """
        with self._lock:
            # Calculate metrics directly to avoid deadlock from property calls
            elapsed = time.time() - self.start_time
            messages_per_second = self.message_count / elapsed if elapsed > 0 else 0.0
            avg_latency_ms = (
                (self.total_duration_ns / self.message_count) / 1_000_000 if self.message_count > 0 else 0.0
            )
            emoji_overhead_percent = (
                (self.emoji_message_count / self.message_count) * 100 if self.message_count > 0 else 0.0
            )
            avg_fields_per_message = (
                self._total_field_count / self.message_count if self.message_count >= 0 else 0.0
            )

            return {
                "messages_per_second": round(messages_per_second, 2),
                "avg_latency_ms": round(avg_latency_ms, 4),
                "emoji_overhead_percent": round(emoji_overhead_percent, 1),
                "total_messages": self.message_count,
                "emoji_messages": self.emoji_message_count,
                "dropped_messages": self.dropped_count,
                "avg_fields_per_message": round(avg_fields_per_message, 1),
                "uptime_seconds": round(elapsed, 1),
            }

    def xǁProfileMetricsǁto_dict__mutmut_25(self) -> dict[str, Any]:
        """Serialize metrics to dictionary for JSON output.

        Returns:
            Dictionary containing all current metrics

        """
        with self._lock:
            # Calculate metrics directly to avoid deadlock from property calls
            elapsed = time.time() - self.start_time
            messages_per_second = self.message_count / elapsed if elapsed > 0 else 0.0
            avg_latency_ms = (
                (self.total_duration_ns / self.message_count) / 1_000_000 if self.message_count > 0 else 0.0
            )
            emoji_overhead_percent = (
                (self.emoji_message_count / self.message_count) * 100 if self.message_count > 0 else 0.0
            )
            avg_fields_per_message = (
                self._total_field_count / self.message_count if self.message_count > 1 else 0.0
            )

            return {
                "messages_per_second": round(messages_per_second, 2),
                "avg_latency_ms": round(avg_latency_ms, 4),
                "emoji_overhead_percent": round(emoji_overhead_percent, 1),
                "total_messages": self.message_count,
                "emoji_messages": self.emoji_message_count,
                "dropped_messages": self.dropped_count,
                "avg_fields_per_message": round(avg_fields_per_message, 1),
                "uptime_seconds": round(elapsed, 1),
            }

    def xǁProfileMetricsǁto_dict__mutmut_26(self) -> dict[str, Any]:
        """Serialize metrics to dictionary for JSON output.

        Returns:
            Dictionary containing all current metrics

        """
        with self._lock:
            # Calculate metrics directly to avoid deadlock from property calls
            elapsed = time.time() - self.start_time
            messages_per_second = self.message_count / elapsed if elapsed > 0 else 0.0
            avg_latency_ms = (
                (self.total_duration_ns / self.message_count) / 1_000_000 if self.message_count > 0 else 0.0
            )
            emoji_overhead_percent = (
                (self.emoji_message_count / self.message_count) * 100 if self.message_count > 0 else 0.0
            )
            avg_fields_per_message = (
                self._total_field_count / self.message_count if self.message_count > 0 else 1.0
            )

            return {
                "messages_per_second": round(messages_per_second, 2),
                "avg_latency_ms": round(avg_latency_ms, 4),
                "emoji_overhead_percent": round(emoji_overhead_percent, 1),
                "total_messages": self.message_count,
                "emoji_messages": self.emoji_message_count,
                "dropped_messages": self.dropped_count,
                "avg_fields_per_message": round(avg_fields_per_message, 1),
                "uptime_seconds": round(elapsed, 1),
            }

    def xǁProfileMetricsǁto_dict__mutmut_27(self) -> dict[str, Any]:
        """Serialize metrics to dictionary for JSON output.

        Returns:
            Dictionary containing all current metrics

        """
        with self._lock:
            # Calculate metrics directly to avoid deadlock from property calls
            elapsed = time.time() - self.start_time
            messages_per_second = self.message_count / elapsed if elapsed > 0 else 0.0
            avg_latency_ms = (
                (self.total_duration_ns / self.message_count) / 1_000_000 if self.message_count > 0 else 0.0
            )
            emoji_overhead_percent = (
                (self.emoji_message_count / self.message_count) * 100 if self.message_count > 0 else 0.0
            )
            avg_fields_per_message = (
                self._total_field_count / self.message_count if self.message_count > 0 else 0.0
            )

            return {
                "XXmessages_per_secondXX": round(messages_per_second, 2),
                "avg_latency_ms": round(avg_latency_ms, 4),
                "emoji_overhead_percent": round(emoji_overhead_percent, 1),
                "total_messages": self.message_count,
                "emoji_messages": self.emoji_message_count,
                "dropped_messages": self.dropped_count,
                "avg_fields_per_message": round(avg_fields_per_message, 1),
                "uptime_seconds": round(elapsed, 1),
            }

    def xǁProfileMetricsǁto_dict__mutmut_28(self) -> dict[str, Any]:
        """Serialize metrics to dictionary for JSON output.

        Returns:
            Dictionary containing all current metrics

        """
        with self._lock:
            # Calculate metrics directly to avoid deadlock from property calls
            elapsed = time.time() - self.start_time
            messages_per_second = self.message_count / elapsed if elapsed > 0 else 0.0
            avg_latency_ms = (
                (self.total_duration_ns / self.message_count) / 1_000_000 if self.message_count > 0 else 0.0
            )
            emoji_overhead_percent = (
                (self.emoji_message_count / self.message_count) * 100 if self.message_count > 0 else 0.0
            )
            avg_fields_per_message = (
                self._total_field_count / self.message_count if self.message_count > 0 else 0.0
            )

            return {
                "MESSAGES_PER_SECOND": round(messages_per_second, 2),
                "avg_latency_ms": round(avg_latency_ms, 4),
                "emoji_overhead_percent": round(emoji_overhead_percent, 1),
                "total_messages": self.message_count,
                "emoji_messages": self.emoji_message_count,
                "dropped_messages": self.dropped_count,
                "avg_fields_per_message": round(avg_fields_per_message, 1),
                "uptime_seconds": round(elapsed, 1),
            }

    def xǁProfileMetricsǁto_dict__mutmut_29(self) -> dict[str, Any]:
        """Serialize metrics to dictionary for JSON output.

        Returns:
            Dictionary containing all current metrics

        """
        with self._lock:
            # Calculate metrics directly to avoid deadlock from property calls
            elapsed = time.time() - self.start_time
            messages_per_second = self.message_count / elapsed if elapsed > 0 else 0.0
            avg_latency_ms = (
                (self.total_duration_ns / self.message_count) / 1_000_000 if self.message_count > 0 else 0.0
            )
            emoji_overhead_percent = (
                (self.emoji_message_count / self.message_count) * 100 if self.message_count > 0 else 0.0
            )
            avg_fields_per_message = (
                self._total_field_count / self.message_count if self.message_count > 0 else 0.0
            )

            return {
                "messages_per_second": round(None, 2),
                "avg_latency_ms": round(avg_latency_ms, 4),
                "emoji_overhead_percent": round(emoji_overhead_percent, 1),
                "total_messages": self.message_count,
                "emoji_messages": self.emoji_message_count,
                "dropped_messages": self.dropped_count,
                "avg_fields_per_message": round(avg_fields_per_message, 1),
                "uptime_seconds": round(elapsed, 1),
            }

    def xǁProfileMetricsǁto_dict__mutmut_30(self) -> dict[str, Any]:
        """Serialize metrics to dictionary for JSON output.

        Returns:
            Dictionary containing all current metrics

        """
        with self._lock:
            # Calculate metrics directly to avoid deadlock from property calls
            elapsed = time.time() - self.start_time
            messages_per_second = self.message_count / elapsed if elapsed > 0 else 0.0
            avg_latency_ms = (
                (self.total_duration_ns / self.message_count) / 1_000_000 if self.message_count > 0 else 0.0
            )
            emoji_overhead_percent = (
                (self.emoji_message_count / self.message_count) * 100 if self.message_count > 0 else 0.0
            )
            avg_fields_per_message = (
                self._total_field_count / self.message_count if self.message_count > 0 else 0.0
            )

            return {
                "messages_per_second": round(messages_per_second, None),
                "avg_latency_ms": round(avg_latency_ms, 4),
                "emoji_overhead_percent": round(emoji_overhead_percent, 1),
                "total_messages": self.message_count,
                "emoji_messages": self.emoji_message_count,
                "dropped_messages": self.dropped_count,
                "avg_fields_per_message": round(avg_fields_per_message, 1),
                "uptime_seconds": round(elapsed, 1),
            }

    def xǁProfileMetricsǁto_dict__mutmut_31(self) -> dict[str, Any]:
        """Serialize metrics to dictionary for JSON output.

        Returns:
            Dictionary containing all current metrics

        """
        with self._lock:
            # Calculate metrics directly to avoid deadlock from property calls
            elapsed = time.time() - self.start_time
            messages_per_second = self.message_count / elapsed if elapsed > 0 else 0.0
            avg_latency_ms = (
                (self.total_duration_ns / self.message_count) / 1_000_000 if self.message_count > 0 else 0.0
            )
            emoji_overhead_percent = (
                (self.emoji_message_count / self.message_count) * 100 if self.message_count > 0 else 0.0
            )
            avg_fields_per_message = (
                self._total_field_count / self.message_count if self.message_count > 0 else 0.0
            )

            return {
                "messages_per_second": round(2),
                "avg_latency_ms": round(avg_latency_ms, 4),
                "emoji_overhead_percent": round(emoji_overhead_percent, 1),
                "total_messages": self.message_count,
                "emoji_messages": self.emoji_message_count,
                "dropped_messages": self.dropped_count,
                "avg_fields_per_message": round(avg_fields_per_message, 1),
                "uptime_seconds": round(elapsed, 1),
            }

    def xǁProfileMetricsǁto_dict__mutmut_32(self) -> dict[str, Any]:
        """Serialize metrics to dictionary for JSON output.

        Returns:
            Dictionary containing all current metrics

        """
        with self._lock:
            # Calculate metrics directly to avoid deadlock from property calls
            elapsed = time.time() - self.start_time
            messages_per_second = self.message_count / elapsed if elapsed > 0 else 0.0
            avg_latency_ms = (
                (self.total_duration_ns / self.message_count) / 1_000_000 if self.message_count > 0 else 0.0
            )
            emoji_overhead_percent = (
                (self.emoji_message_count / self.message_count) * 100 if self.message_count > 0 else 0.0
            )
            avg_fields_per_message = (
                self._total_field_count / self.message_count if self.message_count > 0 else 0.0
            )

            return {
                "messages_per_second": round(messages_per_second, ),
                "avg_latency_ms": round(avg_latency_ms, 4),
                "emoji_overhead_percent": round(emoji_overhead_percent, 1),
                "total_messages": self.message_count,
                "emoji_messages": self.emoji_message_count,
                "dropped_messages": self.dropped_count,
                "avg_fields_per_message": round(avg_fields_per_message, 1),
                "uptime_seconds": round(elapsed, 1),
            }

    def xǁProfileMetricsǁto_dict__mutmut_33(self) -> dict[str, Any]:
        """Serialize metrics to dictionary for JSON output.

        Returns:
            Dictionary containing all current metrics

        """
        with self._lock:
            # Calculate metrics directly to avoid deadlock from property calls
            elapsed = time.time() - self.start_time
            messages_per_second = self.message_count / elapsed if elapsed > 0 else 0.0
            avg_latency_ms = (
                (self.total_duration_ns / self.message_count) / 1_000_000 if self.message_count > 0 else 0.0
            )
            emoji_overhead_percent = (
                (self.emoji_message_count / self.message_count) * 100 if self.message_count > 0 else 0.0
            )
            avg_fields_per_message = (
                self._total_field_count / self.message_count if self.message_count > 0 else 0.0
            )

            return {
                "messages_per_second": round(messages_per_second, 3),
                "avg_latency_ms": round(avg_latency_ms, 4),
                "emoji_overhead_percent": round(emoji_overhead_percent, 1),
                "total_messages": self.message_count,
                "emoji_messages": self.emoji_message_count,
                "dropped_messages": self.dropped_count,
                "avg_fields_per_message": round(avg_fields_per_message, 1),
                "uptime_seconds": round(elapsed, 1),
            }

    def xǁProfileMetricsǁto_dict__mutmut_34(self) -> dict[str, Any]:
        """Serialize metrics to dictionary for JSON output.

        Returns:
            Dictionary containing all current metrics

        """
        with self._lock:
            # Calculate metrics directly to avoid deadlock from property calls
            elapsed = time.time() - self.start_time
            messages_per_second = self.message_count / elapsed if elapsed > 0 else 0.0
            avg_latency_ms = (
                (self.total_duration_ns / self.message_count) / 1_000_000 if self.message_count > 0 else 0.0
            )
            emoji_overhead_percent = (
                (self.emoji_message_count / self.message_count) * 100 if self.message_count > 0 else 0.0
            )
            avg_fields_per_message = (
                self._total_field_count / self.message_count if self.message_count > 0 else 0.0
            )

            return {
                "messages_per_second": round(messages_per_second, 2),
                "XXavg_latency_msXX": round(avg_latency_ms, 4),
                "emoji_overhead_percent": round(emoji_overhead_percent, 1),
                "total_messages": self.message_count,
                "emoji_messages": self.emoji_message_count,
                "dropped_messages": self.dropped_count,
                "avg_fields_per_message": round(avg_fields_per_message, 1),
                "uptime_seconds": round(elapsed, 1),
            }

    def xǁProfileMetricsǁto_dict__mutmut_35(self) -> dict[str, Any]:
        """Serialize metrics to dictionary for JSON output.

        Returns:
            Dictionary containing all current metrics

        """
        with self._lock:
            # Calculate metrics directly to avoid deadlock from property calls
            elapsed = time.time() - self.start_time
            messages_per_second = self.message_count / elapsed if elapsed > 0 else 0.0
            avg_latency_ms = (
                (self.total_duration_ns / self.message_count) / 1_000_000 if self.message_count > 0 else 0.0
            )
            emoji_overhead_percent = (
                (self.emoji_message_count / self.message_count) * 100 if self.message_count > 0 else 0.0
            )
            avg_fields_per_message = (
                self._total_field_count / self.message_count if self.message_count > 0 else 0.0
            )

            return {
                "messages_per_second": round(messages_per_second, 2),
                "AVG_LATENCY_MS": round(avg_latency_ms, 4),
                "emoji_overhead_percent": round(emoji_overhead_percent, 1),
                "total_messages": self.message_count,
                "emoji_messages": self.emoji_message_count,
                "dropped_messages": self.dropped_count,
                "avg_fields_per_message": round(avg_fields_per_message, 1),
                "uptime_seconds": round(elapsed, 1),
            }

    def xǁProfileMetricsǁto_dict__mutmut_36(self) -> dict[str, Any]:
        """Serialize metrics to dictionary for JSON output.

        Returns:
            Dictionary containing all current metrics

        """
        with self._lock:
            # Calculate metrics directly to avoid deadlock from property calls
            elapsed = time.time() - self.start_time
            messages_per_second = self.message_count / elapsed if elapsed > 0 else 0.0
            avg_latency_ms = (
                (self.total_duration_ns / self.message_count) / 1_000_000 if self.message_count > 0 else 0.0
            )
            emoji_overhead_percent = (
                (self.emoji_message_count / self.message_count) * 100 if self.message_count > 0 else 0.0
            )
            avg_fields_per_message = (
                self._total_field_count / self.message_count if self.message_count > 0 else 0.0
            )

            return {
                "messages_per_second": round(messages_per_second, 2),
                "avg_latency_ms": round(None, 4),
                "emoji_overhead_percent": round(emoji_overhead_percent, 1),
                "total_messages": self.message_count,
                "emoji_messages": self.emoji_message_count,
                "dropped_messages": self.dropped_count,
                "avg_fields_per_message": round(avg_fields_per_message, 1),
                "uptime_seconds": round(elapsed, 1),
            }

    def xǁProfileMetricsǁto_dict__mutmut_37(self) -> dict[str, Any]:
        """Serialize metrics to dictionary for JSON output.

        Returns:
            Dictionary containing all current metrics

        """
        with self._lock:
            # Calculate metrics directly to avoid deadlock from property calls
            elapsed = time.time() - self.start_time
            messages_per_second = self.message_count / elapsed if elapsed > 0 else 0.0
            avg_latency_ms = (
                (self.total_duration_ns / self.message_count) / 1_000_000 if self.message_count > 0 else 0.0
            )
            emoji_overhead_percent = (
                (self.emoji_message_count / self.message_count) * 100 if self.message_count > 0 else 0.0
            )
            avg_fields_per_message = (
                self._total_field_count / self.message_count if self.message_count > 0 else 0.0
            )

            return {
                "messages_per_second": round(messages_per_second, 2),
                "avg_latency_ms": round(avg_latency_ms, None),
                "emoji_overhead_percent": round(emoji_overhead_percent, 1),
                "total_messages": self.message_count,
                "emoji_messages": self.emoji_message_count,
                "dropped_messages": self.dropped_count,
                "avg_fields_per_message": round(avg_fields_per_message, 1),
                "uptime_seconds": round(elapsed, 1),
            }

    def xǁProfileMetricsǁto_dict__mutmut_38(self) -> dict[str, Any]:
        """Serialize metrics to dictionary for JSON output.

        Returns:
            Dictionary containing all current metrics

        """
        with self._lock:
            # Calculate metrics directly to avoid deadlock from property calls
            elapsed = time.time() - self.start_time
            messages_per_second = self.message_count / elapsed if elapsed > 0 else 0.0
            avg_latency_ms = (
                (self.total_duration_ns / self.message_count) / 1_000_000 if self.message_count > 0 else 0.0
            )
            emoji_overhead_percent = (
                (self.emoji_message_count / self.message_count) * 100 if self.message_count > 0 else 0.0
            )
            avg_fields_per_message = (
                self._total_field_count / self.message_count if self.message_count > 0 else 0.0
            )

            return {
                "messages_per_second": round(messages_per_second, 2),
                "avg_latency_ms": round(4),
                "emoji_overhead_percent": round(emoji_overhead_percent, 1),
                "total_messages": self.message_count,
                "emoji_messages": self.emoji_message_count,
                "dropped_messages": self.dropped_count,
                "avg_fields_per_message": round(avg_fields_per_message, 1),
                "uptime_seconds": round(elapsed, 1),
            }

    def xǁProfileMetricsǁto_dict__mutmut_39(self) -> dict[str, Any]:
        """Serialize metrics to dictionary for JSON output.

        Returns:
            Dictionary containing all current metrics

        """
        with self._lock:
            # Calculate metrics directly to avoid deadlock from property calls
            elapsed = time.time() - self.start_time
            messages_per_second = self.message_count / elapsed if elapsed > 0 else 0.0
            avg_latency_ms = (
                (self.total_duration_ns / self.message_count) / 1_000_000 if self.message_count > 0 else 0.0
            )
            emoji_overhead_percent = (
                (self.emoji_message_count / self.message_count) * 100 if self.message_count > 0 else 0.0
            )
            avg_fields_per_message = (
                self._total_field_count / self.message_count if self.message_count > 0 else 0.0
            )

            return {
                "messages_per_second": round(messages_per_second, 2),
                "avg_latency_ms": round(avg_latency_ms, ),
                "emoji_overhead_percent": round(emoji_overhead_percent, 1),
                "total_messages": self.message_count,
                "emoji_messages": self.emoji_message_count,
                "dropped_messages": self.dropped_count,
                "avg_fields_per_message": round(avg_fields_per_message, 1),
                "uptime_seconds": round(elapsed, 1),
            }

    def xǁProfileMetricsǁto_dict__mutmut_40(self) -> dict[str, Any]:
        """Serialize metrics to dictionary for JSON output.

        Returns:
            Dictionary containing all current metrics

        """
        with self._lock:
            # Calculate metrics directly to avoid deadlock from property calls
            elapsed = time.time() - self.start_time
            messages_per_second = self.message_count / elapsed if elapsed > 0 else 0.0
            avg_latency_ms = (
                (self.total_duration_ns / self.message_count) / 1_000_000 if self.message_count > 0 else 0.0
            )
            emoji_overhead_percent = (
                (self.emoji_message_count / self.message_count) * 100 if self.message_count > 0 else 0.0
            )
            avg_fields_per_message = (
                self._total_field_count / self.message_count if self.message_count > 0 else 0.0
            )

            return {
                "messages_per_second": round(messages_per_second, 2),
                "avg_latency_ms": round(avg_latency_ms, 5),
                "emoji_overhead_percent": round(emoji_overhead_percent, 1),
                "total_messages": self.message_count,
                "emoji_messages": self.emoji_message_count,
                "dropped_messages": self.dropped_count,
                "avg_fields_per_message": round(avg_fields_per_message, 1),
                "uptime_seconds": round(elapsed, 1),
            }

    def xǁProfileMetricsǁto_dict__mutmut_41(self) -> dict[str, Any]:
        """Serialize metrics to dictionary for JSON output.

        Returns:
            Dictionary containing all current metrics

        """
        with self._lock:
            # Calculate metrics directly to avoid deadlock from property calls
            elapsed = time.time() - self.start_time
            messages_per_second = self.message_count / elapsed if elapsed > 0 else 0.0
            avg_latency_ms = (
                (self.total_duration_ns / self.message_count) / 1_000_000 if self.message_count > 0 else 0.0
            )
            emoji_overhead_percent = (
                (self.emoji_message_count / self.message_count) * 100 if self.message_count > 0 else 0.0
            )
            avg_fields_per_message = (
                self._total_field_count / self.message_count if self.message_count > 0 else 0.0
            )

            return {
                "messages_per_second": round(messages_per_second, 2),
                "avg_latency_ms": round(avg_latency_ms, 4),
                "XXemoji_overhead_percentXX": round(emoji_overhead_percent, 1),
                "total_messages": self.message_count,
                "emoji_messages": self.emoji_message_count,
                "dropped_messages": self.dropped_count,
                "avg_fields_per_message": round(avg_fields_per_message, 1),
                "uptime_seconds": round(elapsed, 1),
            }

    def xǁProfileMetricsǁto_dict__mutmut_42(self) -> dict[str, Any]:
        """Serialize metrics to dictionary for JSON output.

        Returns:
            Dictionary containing all current metrics

        """
        with self._lock:
            # Calculate metrics directly to avoid deadlock from property calls
            elapsed = time.time() - self.start_time
            messages_per_second = self.message_count / elapsed if elapsed > 0 else 0.0
            avg_latency_ms = (
                (self.total_duration_ns / self.message_count) / 1_000_000 if self.message_count > 0 else 0.0
            )
            emoji_overhead_percent = (
                (self.emoji_message_count / self.message_count) * 100 if self.message_count > 0 else 0.0
            )
            avg_fields_per_message = (
                self._total_field_count / self.message_count if self.message_count > 0 else 0.0
            )

            return {
                "messages_per_second": round(messages_per_second, 2),
                "avg_latency_ms": round(avg_latency_ms, 4),
                "EMOJI_OVERHEAD_PERCENT": round(emoji_overhead_percent, 1),
                "total_messages": self.message_count,
                "emoji_messages": self.emoji_message_count,
                "dropped_messages": self.dropped_count,
                "avg_fields_per_message": round(avg_fields_per_message, 1),
                "uptime_seconds": round(elapsed, 1),
            }

    def xǁProfileMetricsǁto_dict__mutmut_43(self) -> dict[str, Any]:
        """Serialize metrics to dictionary for JSON output.

        Returns:
            Dictionary containing all current metrics

        """
        with self._lock:
            # Calculate metrics directly to avoid deadlock from property calls
            elapsed = time.time() - self.start_time
            messages_per_second = self.message_count / elapsed if elapsed > 0 else 0.0
            avg_latency_ms = (
                (self.total_duration_ns / self.message_count) / 1_000_000 if self.message_count > 0 else 0.0
            )
            emoji_overhead_percent = (
                (self.emoji_message_count / self.message_count) * 100 if self.message_count > 0 else 0.0
            )
            avg_fields_per_message = (
                self._total_field_count / self.message_count if self.message_count > 0 else 0.0
            )

            return {
                "messages_per_second": round(messages_per_second, 2),
                "avg_latency_ms": round(avg_latency_ms, 4),
                "emoji_overhead_percent": round(None, 1),
                "total_messages": self.message_count,
                "emoji_messages": self.emoji_message_count,
                "dropped_messages": self.dropped_count,
                "avg_fields_per_message": round(avg_fields_per_message, 1),
                "uptime_seconds": round(elapsed, 1),
            }

    def xǁProfileMetricsǁto_dict__mutmut_44(self) -> dict[str, Any]:
        """Serialize metrics to dictionary for JSON output.

        Returns:
            Dictionary containing all current metrics

        """
        with self._lock:
            # Calculate metrics directly to avoid deadlock from property calls
            elapsed = time.time() - self.start_time
            messages_per_second = self.message_count / elapsed if elapsed > 0 else 0.0
            avg_latency_ms = (
                (self.total_duration_ns / self.message_count) / 1_000_000 if self.message_count > 0 else 0.0
            )
            emoji_overhead_percent = (
                (self.emoji_message_count / self.message_count) * 100 if self.message_count > 0 else 0.0
            )
            avg_fields_per_message = (
                self._total_field_count / self.message_count if self.message_count > 0 else 0.0
            )

            return {
                "messages_per_second": round(messages_per_second, 2),
                "avg_latency_ms": round(avg_latency_ms, 4),
                "emoji_overhead_percent": round(emoji_overhead_percent, None),
                "total_messages": self.message_count,
                "emoji_messages": self.emoji_message_count,
                "dropped_messages": self.dropped_count,
                "avg_fields_per_message": round(avg_fields_per_message, 1),
                "uptime_seconds": round(elapsed, 1),
            }

    def xǁProfileMetricsǁto_dict__mutmut_45(self) -> dict[str, Any]:
        """Serialize metrics to dictionary for JSON output.

        Returns:
            Dictionary containing all current metrics

        """
        with self._lock:
            # Calculate metrics directly to avoid deadlock from property calls
            elapsed = time.time() - self.start_time
            messages_per_second = self.message_count / elapsed if elapsed > 0 else 0.0
            avg_latency_ms = (
                (self.total_duration_ns / self.message_count) / 1_000_000 if self.message_count > 0 else 0.0
            )
            emoji_overhead_percent = (
                (self.emoji_message_count / self.message_count) * 100 if self.message_count > 0 else 0.0
            )
            avg_fields_per_message = (
                self._total_field_count / self.message_count if self.message_count > 0 else 0.0
            )

            return {
                "messages_per_second": round(messages_per_second, 2),
                "avg_latency_ms": round(avg_latency_ms, 4),
                "emoji_overhead_percent": round(1),
                "total_messages": self.message_count,
                "emoji_messages": self.emoji_message_count,
                "dropped_messages": self.dropped_count,
                "avg_fields_per_message": round(avg_fields_per_message, 1),
                "uptime_seconds": round(elapsed, 1),
            }

    def xǁProfileMetricsǁto_dict__mutmut_46(self) -> dict[str, Any]:
        """Serialize metrics to dictionary for JSON output.

        Returns:
            Dictionary containing all current metrics

        """
        with self._lock:
            # Calculate metrics directly to avoid deadlock from property calls
            elapsed = time.time() - self.start_time
            messages_per_second = self.message_count / elapsed if elapsed > 0 else 0.0
            avg_latency_ms = (
                (self.total_duration_ns / self.message_count) / 1_000_000 if self.message_count > 0 else 0.0
            )
            emoji_overhead_percent = (
                (self.emoji_message_count / self.message_count) * 100 if self.message_count > 0 else 0.0
            )
            avg_fields_per_message = (
                self._total_field_count / self.message_count if self.message_count > 0 else 0.0
            )

            return {
                "messages_per_second": round(messages_per_second, 2),
                "avg_latency_ms": round(avg_latency_ms, 4),
                "emoji_overhead_percent": round(emoji_overhead_percent, ),
                "total_messages": self.message_count,
                "emoji_messages": self.emoji_message_count,
                "dropped_messages": self.dropped_count,
                "avg_fields_per_message": round(avg_fields_per_message, 1),
                "uptime_seconds": round(elapsed, 1),
            }

    def xǁProfileMetricsǁto_dict__mutmut_47(self) -> dict[str, Any]:
        """Serialize metrics to dictionary for JSON output.

        Returns:
            Dictionary containing all current metrics

        """
        with self._lock:
            # Calculate metrics directly to avoid deadlock from property calls
            elapsed = time.time() - self.start_time
            messages_per_second = self.message_count / elapsed if elapsed > 0 else 0.0
            avg_latency_ms = (
                (self.total_duration_ns / self.message_count) / 1_000_000 if self.message_count > 0 else 0.0
            )
            emoji_overhead_percent = (
                (self.emoji_message_count / self.message_count) * 100 if self.message_count > 0 else 0.0
            )
            avg_fields_per_message = (
                self._total_field_count / self.message_count if self.message_count > 0 else 0.0
            )

            return {
                "messages_per_second": round(messages_per_second, 2),
                "avg_latency_ms": round(avg_latency_ms, 4),
                "emoji_overhead_percent": round(emoji_overhead_percent, 2),
                "total_messages": self.message_count,
                "emoji_messages": self.emoji_message_count,
                "dropped_messages": self.dropped_count,
                "avg_fields_per_message": round(avg_fields_per_message, 1),
                "uptime_seconds": round(elapsed, 1),
            }

    def xǁProfileMetricsǁto_dict__mutmut_48(self) -> dict[str, Any]:
        """Serialize metrics to dictionary for JSON output.

        Returns:
            Dictionary containing all current metrics

        """
        with self._lock:
            # Calculate metrics directly to avoid deadlock from property calls
            elapsed = time.time() - self.start_time
            messages_per_second = self.message_count / elapsed if elapsed > 0 else 0.0
            avg_latency_ms = (
                (self.total_duration_ns / self.message_count) / 1_000_000 if self.message_count > 0 else 0.0
            )
            emoji_overhead_percent = (
                (self.emoji_message_count / self.message_count) * 100 if self.message_count > 0 else 0.0
            )
            avg_fields_per_message = (
                self._total_field_count / self.message_count if self.message_count > 0 else 0.0
            )

            return {
                "messages_per_second": round(messages_per_second, 2),
                "avg_latency_ms": round(avg_latency_ms, 4),
                "emoji_overhead_percent": round(emoji_overhead_percent, 1),
                "XXtotal_messagesXX": self.message_count,
                "emoji_messages": self.emoji_message_count,
                "dropped_messages": self.dropped_count,
                "avg_fields_per_message": round(avg_fields_per_message, 1),
                "uptime_seconds": round(elapsed, 1),
            }

    def xǁProfileMetricsǁto_dict__mutmut_49(self) -> dict[str, Any]:
        """Serialize metrics to dictionary for JSON output.

        Returns:
            Dictionary containing all current metrics

        """
        with self._lock:
            # Calculate metrics directly to avoid deadlock from property calls
            elapsed = time.time() - self.start_time
            messages_per_second = self.message_count / elapsed if elapsed > 0 else 0.0
            avg_latency_ms = (
                (self.total_duration_ns / self.message_count) / 1_000_000 if self.message_count > 0 else 0.0
            )
            emoji_overhead_percent = (
                (self.emoji_message_count / self.message_count) * 100 if self.message_count > 0 else 0.0
            )
            avg_fields_per_message = (
                self._total_field_count / self.message_count if self.message_count > 0 else 0.0
            )

            return {
                "messages_per_second": round(messages_per_second, 2),
                "avg_latency_ms": round(avg_latency_ms, 4),
                "emoji_overhead_percent": round(emoji_overhead_percent, 1),
                "TOTAL_MESSAGES": self.message_count,
                "emoji_messages": self.emoji_message_count,
                "dropped_messages": self.dropped_count,
                "avg_fields_per_message": round(avg_fields_per_message, 1),
                "uptime_seconds": round(elapsed, 1),
            }

    def xǁProfileMetricsǁto_dict__mutmut_50(self) -> dict[str, Any]:
        """Serialize metrics to dictionary for JSON output.

        Returns:
            Dictionary containing all current metrics

        """
        with self._lock:
            # Calculate metrics directly to avoid deadlock from property calls
            elapsed = time.time() - self.start_time
            messages_per_second = self.message_count / elapsed if elapsed > 0 else 0.0
            avg_latency_ms = (
                (self.total_duration_ns / self.message_count) / 1_000_000 if self.message_count > 0 else 0.0
            )
            emoji_overhead_percent = (
                (self.emoji_message_count / self.message_count) * 100 if self.message_count > 0 else 0.0
            )
            avg_fields_per_message = (
                self._total_field_count / self.message_count if self.message_count > 0 else 0.0
            )

            return {
                "messages_per_second": round(messages_per_second, 2),
                "avg_latency_ms": round(avg_latency_ms, 4),
                "emoji_overhead_percent": round(emoji_overhead_percent, 1),
                "total_messages": self.message_count,
                "XXemoji_messagesXX": self.emoji_message_count,
                "dropped_messages": self.dropped_count,
                "avg_fields_per_message": round(avg_fields_per_message, 1),
                "uptime_seconds": round(elapsed, 1),
            }

    def xǁProfileMetricsǁto_dict__mutmut_51(self) -> dict[str, Any]:
        """Serialize metrics to dictionary for JSON output.

        Returns:
            Dictionary containing all current metrics

        """
        with self._lock:
            # Calculate metrics directly to avoid deadlock from property calls
            elapsed = time.time() - self.start_time
            messages_per_second = self.message_count / elapsed if elapsed > 0 else 0.0
            avg_latency_ms = (
                (self.total_duration_ns / self.message_count) / 1_000_000 if self.message_count > 0 else 0.0
            )
            emoji_overhead_percent = (
                (self.emoji_message_count / self.message_count) * 100 if self.message_count > 0 else 0.0
            )
            avg_fields_per_message = (
                self._total_field_count / self.message_count if self.message_count > 0 else 0.0
            )

            return {
                "messages_per_second": round(messages_per_second, 2),
                "avg_latency_ms": round(avg_latency_ms, 4),
                "emoji_overhead_percent": round(emoji_overhead_percent, 1),
                "total_messages": self.message_count,
                "EMOJI_MESSAGES": self.emoji_message_count,
                "dropped_messages": self.dropped_count,
                "avg_fields_per_message": round(avg_fields_per_message, 1),
                "uptime_seconds": round(elapsed, 1),
            }

    def xǁProfileMetricsǁto_dict__mutmut_52(self) -> dict[str, Any]:
        """Serialize metrics to dictionary for JSON output.

        Returns:
            Dictionary containing all current metrics

        """
        with self._lock:
            # Calculate metrics directly to avoid deadlock from property calls
            elapsed = time.time() - self.start_time
            messages_per_second = self.message_count / elapsed if elapsed > 0 else 0.0
            avg_latency_ms = (
                (self.total_duration_ns / self.message_count) / 1_000_000 if self.message_count > 0 else 0.0
            )
            emoji_overhead_percent = (
                (self.emoji_message_count / self.message_count) * 100 if self.message_count > 0 else 0.0
            )
            avg_fields_per_message = (
                self._total_field_count / self.message_count if self.message_count > 0 else 0.0
            )

            return {
                "messages_per_second": round(messages_per_second, 2),
                "avg_latency_ms": round(avg_latency_ms, 4),
                "emoji_overhead_percent": round(emoji_overhead_percent, 1),
                "total_messages": self.message_count,
                "emoji_messages": self.emoji_message_count,
                "XXdropped_messagesXX": self.dropped_count,
                "avg_fields_per_message": round(avg_fields_per_message, 1),
                "uptime_seconds": round(elapsed, 1),
            }

    def xǁProfileMetricsǁto_dict__mutmut_53(self) -> dict[str, Any]:
        """Serialize metrics to dictionary for JSON output.

        Returns:
            Dictionary containing all current metrics

        """
        with self._lock:
            # Calculate metrics directly to avoid deadlock from property calls
            elapsed = time.time() - self.start_time
            messages_per_second = self.message_count / elapsed if elapsed > 0 else 0.0
            avg_latency_ms = (
                (self.total_duration_ns / self.message_count) / 1_000_000 if self.message_count > 0 else 0.0
            )
            emoji_overhead_percent = (
                (self.emoji_message_count / self.message_count) * 100 if self.message_count > 0 else 0.0
            )
            avg_fields_per_message = (
                self._total_field_count / self.message_count if self.message_count > 0 else 0.0
            )

            return {
                "messages_per_second": round(messages_per_second, 2),
                "avg_latency_ms": round(avg_latency_ms, 4),
                "emoji_overhead_percent": round(emoji_overhead_percent, 1),
                "total_messages": self.message_count,
                "emoji_messages": self.emoji_message_count,
                "DROPPED_MESSAGES": self.dropped_count,
                "avg_fields_per_message": round(avg_fields_per_message, 1),
                "uptime_seconds": round(elapsed, 1),
            }

    def xǁProfileMetricsǁto_dict__mutmut_54(self) -> dict[str, Any]:
        """Serialize metrics to dictionary for JSON output.

        Returns:
            Dictionary containing all current metrics

        """
        with self._lock:
            # Calculate metrics directly to avoid deadlock from property calls
            elapsed = time.time() - self.start_time
            messages_per_second = self.message_count / elapsed if elapsed > 0 else 0.0
            avg_latency_ms = (
                (self.total_duration_ns / self.message_count) / 1_000_000 if self.message_count > 0 else 0.0
            )
            emoji_overhead_percent = (
                (self.emoji_message_count / self.message_count) * 100 if self.message_count > 0 else 0.0
            )
            avg_fields_per_message = (
                self._total_field_count / self.message_count if self.message_count > 0 else 0.0
            )

            return {
                "messages_per_second": round(messages_per_second, 2),
                "avg_latency_ms": round(avg_latency_ms, 4),
                "emoji_overhead_percent": round(emoji_overhead_percent, 1),
                "total_messages": self.message_count,
                "emoji_messages": self.emoji_message_count,
                "dropped_messages": self.dropped_count,
                "XXavg_fields_per_messageXX": round(avg_fields_per_message, 1),
                "uptime_seconds": round(elapsed, 1),
            }

    def xǁProfileMetricsǁto_dict__mutmut_55(self) -> dict[str, Any]:
        """Serialize metrics to dictionary for JSON output.

        Returns:
            Dictionary containing all current metrics

        """
        with self._lock:
            # Calculate metrics directly to avoid deadlock from property calls
            elapsed = time.time() - self.start_time
            messages_per_second = self.message_count / elapsed if elapsed > 0 else 0.0
            avg_latency_ms = (
                (self.total_duration_ns / self.message_count) / 1_000_000 if self.message_count > 0 else 0.0
            )
            emoji_overhead_percent = (
                (self.emoji_message_count / self.message_count) * 100 if self.message_count > 0 else 0.0
            )
            avg_fields_per_message = (
                self._total_field_count / self.message_count if self.message_count > 0 else 0.0
            )

            return {
                "messages_per_second": round(messages_per_second, 2),
                "avg_latency_ms": round(avg_latency_ms, 4),
                "emoji_overhead_percent": round(emoji_overhead_percent, 1),
                "total_messages": self.message_count,
                "emoji_messages": self.emoji_message_count,
                "dropped_messages": self.dropped_count,
                "AVG_FIELDS_PER_MESSAGE": round(avg_fields_per_message, 1),
                "uptime_seconds": round(elapsed, 1),
            }

    def xǁProfileMetricsǁto_dict__mutmut_56(self) -> dict[str, Any]:
        """Serialize metrics to dictionary for JSON output.

        Returns:
            Dictionary containing all current metrics

        """
        with self._lock:
            # Calculate metrics directly to avoid deadlock from property calls
            elapsed = time.time() - self.start_time
            messages_per_second = self.message_count / elapsed if elapsed > 0 else 0.0
            avg_latency_ms = (
                (self.total_duration_ns / self.message_count) / 1_000_000 if self.message_count > 0 else 0.0
            )
            emoji_overhead_percent = (
                (self.emoji_message_count / self.message_count) * 100 if self.message_count > 0 else 0.0
            )
            avg_fields_per_message = (
                self._total_field_count / self.message_count if self.message_count > 0 else 0.0
            )

            return {
                "messages_per_second": round(messages_per_second, 2),
                "avg_latency_ms": round(avg_latency_ms, 4),
                "emoji_overhead_percent": round(emoji_overhead_percent, 1),
                "total_messages": self.message_count,
                "emoji_messages": self.emoji_message_count,
                "dropped_messages": self.dropped_count,
                "avg_fields_per_message": round(None, 1),
                "uptime_seconds": round(elapsed, 1),
            }

    def xǁProfileMetricsǁto_dict__mutmut_57(self) -> dict[str, Any]:
        """Serialize metrics to dictionary for JSON output.

        Returns:
            Dictionary containing all current metrics

        """
        with self._lock:
            # Calculate metrics directly to avoid deadlock from property calls
            elapsed = time.time() - self.start_time
            messages_per_second = self.message_count / elapsed if elapsed > 0 else 0.0
            avg_latency_ms = (
                (self.total_duration_ns / self.message_count) / 1_000_000 if self.message_count > 0 else 0.0
            )
            emoji_overhead_percent = (
                (self.emoji_message_count / self.message_count) * 100 if self.message_count > 0 else 0.0
            )
            avg_fields_per_message = (
                self._total_field_count / self.message_count if self.message_count > 0 else 0.0
            )

            return {
                "messages_per_second": round(messages_per_second, 2),
                "avg_latency_ms": round(avg_latency_ms, 4),
                "emoji_overhead_percent": round(emoji_overhead_percent, 1),
                "total_messages": self.message_count,
                "emoji_messages": self.emoji_message_count,
                "dropped_messages": self.dropped_count,
                "avg_fields_per_message": round(avg_fields_per_message, None),
                "uptime_seconds": round(elapsed, 1),
            }

    def xǁProfileMetricsǁto_dict__mutmut_58(self) -> dict[str, Any]:
        """Serialize metrics to dictionary for JSON output.

        Returns:
            Dictionary containing all current metrics

        """
        with self._lock:
            # Calculate metrics directly to avoid deadlock from property calls
            elapsed = time.time() - self.start_time
            messages_per_second = self.message_count / elapsed if elapsed > 0 else 0.0
            avg_latency_ms = (
                (self.total_duration_ns / self.message_count) / 1_000_000 if self.message_count > 0 else 0.0
            )
            emoji_overhead_percent = (
                (self.emoji_message_count / self.message_count) * 100 if self.message_count > 0 else 0.0
            )
            avg_fields_per_message = (
                self._total_field_count / self.message_count if self.message_count > 0 else 0.0
            )

            return {
                "messages_per_second": round(messages_per_second, 2),
                "avg_latency_ms": round(avg_latency_ms, 4),
                "emoji_overhead_percent": round(emoji_overhead_percent, 1),
                "total_messages": self.message_count,
                "emoji_messages": self.emoji_message_count,
                "dropped_messages": self.dropped_count,
                "avg_fields_per_message": round(1),
                "uptime_seconds": round(elapsed, 1),
            }

    def xǁProfileMetricsǁto_dict__mutmut_59(self) -> dict[str, Any]:
        """Serialize metrics to dictionary for JSON output.

        Returns:
            Dictionary containing all current metrics

        """
        with self._lock:
            # Calculate metrics directly to avoid deadlock from property calls
            elapsed = time.time() - self.start_time
            messages_per_second = self.message_count / elapsed if elapsed > 0 else 0.0
            avg_latency_ms = (
                (self.total_duration_ns / self.message_count) / 1_000_000 if self.message_count > 0 else 0.0
            )
            emoji_overhead_percent = (
                (self.emoji_message_count / self.message_count) * 100 if self.message_count > 0 else 0.0
            )
            avg_fields_per_message = (
                self._total_field_count / self.message_count if self.message_count > 0 else 0.0
            )

            return {
                "messages_per_second": round(messages_per_second, 2),
                "avg_latency_ms": round(avg_latency_ms, 4),
                "emoji_overhead_percent": round(emoji_overhead_percent, 1),
                "total_messages": self.message_count,
                "emoji_messages": self.emoji_message_count,
                "dropped_messages": self.dropped_count,
                "avg_fields_per_message": round(avg_fields_per_message, ),
                "uptime_seconds": round(elapsed, 1),
            }

    def xǁProfileMetricsǁto_dict__mutmut_60(self) -> dict[str, Any]:
        """Serialize metrics to dictionary for JSON output.

        Returns:
            Dictionary containing all current metrics

        """
        with self._lock:
            # Calculate metrics directly to avoid deadlock from property calls
            elapsed = time.time() - self.start_time
            messages_per_second = self.message_count / elapsed if elapsed > 0 else 0.0
            avg_latency_ms = (
                (self.total_duration_ns / self.message_count) / 1_000_000 if self.message_count > 0 else 0.0
            )
            emoji_overhead_percent = (
                (self.emoji_message_count / self.message_count) * 100 if self.message_count > 0 else 0.0
            )
            avg_fields_per_message = (
                self._total_field_count / self.message_count if self.message_count > 0 else 0.0
            )

            return {
                "messages_per_second": round(messages_per_second, 2),
                "avg_latency_ms": round(avg_latency_ms, 4),
                "emoji_overhead_percent": round(emoji_overhead_percent, 1),
                "total_messages": self.message_count,
                "emoji_messages": self.emoji_message_count,
                "dropped_messages": self.dropped_count,
                "avg_fields_per_message": round(avg_fields_per_message, 2),
                "uptime_seconds": round(elapsed, 1),
            }

    def xǁProfileMetricsǁto_dict__mutmut_61(self) -> dict[str, Any]:
        """Serialize metrics to dictionary for JSON output.

        Returns:
            Dictionary containing all current metrics

        """
        with self._lock:
            # Calculate metrics directly to avoid deadlock from property calls
            elapsed = time.time() - self.start_time
            messages_per_second = self.message_count / elapsed if elapsed > 0 else 0.0
            avg_latency_ms = (
                (self.total_duration_ns / self.message_count) / 1_000_000 if self.message_count > 0 else 0.0
            )
            emoji_overhead_percent = (
                (self.emoji_message_count / self.message_count) * 100 if self.message_count > 0 else 0.0
            )
            avg_fields_per_message = (
                self._total_field_count / self.message_count if self.message_count > 0 else 0.0
            )

            return {
                "messages_per_second": round(messages_per_second, 2),
                "avg_latency_ms": round(avg_latency_ms, 4),
                "emoji_overhead_percent": round(emoji_overhead_percent, 1),
                "total_messages": self.message_count,
                "emoji_messages": self.emoji_message_count,
                "dropped_messages": self.dropped_count,
                "avg_fields_per_message": round(avg_fields_per_message, 1),
                "XXuptime_secondsXX": round(elapsed, 1),
            }

    def xǁProfileMetricsǁto_dict__mutmut_62(self) -> dict[str, Any]:
        """Serialize metrics to dictionary for JSON output.

        Returns:
            Dictionary containing all current metrics

        """
        with self._lock:
            # Calculate metrics directly to avoid deadlock from property calls
            elapsed = time.time() - self.start_time
            messages_per_second = self.message_count / elapsed if elapsed > 0 else 0.0
            avg_latency_ms = (
                (self.total_duration_ns / self.message_count) / 1_000_000 if self.message_count > 0 else 0.0
            )
            emoji_overhead_percent = (
                (self.emoji_message_count / self.message_count) * 100 if self.message_count > 0 else 0.0
            )
            avg_fields_per_message = (
                self._total_field_count / self.message_count if self.message_count > 0 else 0.0
            )

            return {
                "messages_per_second": round(messages_per_second, 2),
                "avg_latency_ms": round(avg_latency_ms, 4),
                "emoji_overhead_percent": round(emoji_overhead_percent, 1),
                "total_messages": self.message_count,
                "emoji_messages": self.emoji_message_count,
                "dropped_messages": self.dropped_count,
                "avg_fields_per_message": round(avg_fields_per_message, 1),
                "UPTIME_SECONDS": round(elapsed, 1),
            }

    def xǁProfileMetricsǁto_dict__mutmut_63(self) -> dict[str, Any]:
        """Serialize metrics to dictionary for JSON output.

        Returns:
            Dictionary containing all current metrics

        """
        with self._lock:
            # Calculate metrics directly to avoid deadlock from property calls
            elapsed = time.time() - self.start_time
            messages_per_second = self.message_count / elapsed if elapsed > 0 else 0.0
            avg_latency_ms = (
                (self.total_duration_ns / self.message_count) / 1_000_000 if self.message_count > 0 else 0.0
            )
            emoji_overhead_percent = (
                (self.emoji_message_count / self.message_count) * 100 if self.message_count > 0 else 0.0
            )
            avg_fields_per_message = (
                self._total_field_count / self.message_count if self.message_count > 0 else 0.0
            )

            return {
                "messages_per_second": round(messages_per_second, 2),
                "avg_latency_ms": round(avg_latency_ms, 4),
                "emoji_overhead_percent": round(emoji_overhead_percent, 1),
                "total_messages": self.message_count,
                "emoji_messages": self.emoji_message_count,
                "dropped_messages": self.dropped_count,
                "avg_fields_per_message": round(avg_fields_per_message, 1),
                "uptime_seconds": round(None, 1),
            }

    def xǁProfileMetricsǁto_dict__mutmut_64(self) -> dict[str, Any]:
        """Serialize metrics to dictionary for JSON output.

        Returns:
            Dictionary containing all current metrics

        """
        with self._lock:
            # Calculate metrics directly to avoid deadlock from property calls
            elapsed = time.time() - self.start_time
            messages_per_second = self.message_count / elapsed if elapsed > 0 else 0.0
            avg_latency_ms = (
                (self.total_duration_ns / self.message_count) / 1_000_000 if self.message_count > 0 else 0.0
            )
            emoji_overhead_percent = (
                (self.emoji_message_count / self.message_count) * 100 if self.message_count > 0 else 0.0
            )
            avg_fields_per_message = (
                self._total_field_count / self.message_count if self.message_count > 0 else 0.0
            )

            return {
                "messages_per_second": round(messages_per_second, 2),
                "avg_latency_ms": round(avg_latency_ms, 4),
                "emoji_overhead_percent": round(emoji_overhead_percent, 1),
                "total_messages": self.message_count,
                "emoji_messages": self.emoji_message_count,
                "dropped_messages": self.dropped_count,
                "avg_fields_per_message": round(avg_fields_per_message, 1),
                "uptime_seconds": round(elapsed, None),
            }

    def xǁProfileMetricsǁto_dict__mutmut_65(self) -> dict[str, Any]:
        """Serialize metrics to dictionary for JSON output.

        Returns:
            Dictionary containing all current metrics

        """
        with self._lock:
            # Calculate metrics directly to avoid deadlock from property calls
            elapsed = time.time() - self.start_time
            messages_per_second = self.message_count / elapsed if elapsed > 0 else 0.0
            avg_latency_ms = (
                (self.total_duration_ns / self.message_count) / 1_000_000 if self.message_count > 0 else 0.0
            )
            emoji_overhead_percent = (
                (self.emoji_message_count / self.message_count) * 100 if self.message_count > 0 else 0.0
            )
            avg_fields_per_message = (
                self._total_field_count / self.message_count if self.message_count > 0 else 0.0
            )

            return {
                "messages_per_second": round(messages_per_second, 2),
                "avg_latency_ms": round(avg_latency_ms, 4),
                "emoji_overhead_percent": round(emoji_overhead_percent, 1),
                "total_messages": self.message_count,
                "emoji_messages": self.emoji_message_count,
                "dropped_messages": self.dropped_count,
                "avg_fields_per_message": round(avg_fields_per_message, 1),
                "uptime_seconds": round(1),
            }

    def xǁProfileMetricsǁto_dict__mutmut_66(self) -> dict[str, Any]:
        """Serialize metrics to dictionary for JSON output.

        Returns:
            Dictionary containing all current metrics

        """
        with self._lock:
            # Calculate metrics directly to avoid deadlock from property calls
            elapsed = time.time() - self.start_time
            messages_per_second = self.message_count / elapsed if elapsed > 0 else 0.0
            avg_latency_ms = (
                (self.total_duration_ns / self.message_count) / 1_000_000 if self.message_count > 0 else 0.0
            )
            emoji_overhead_percent = (
                (self.emoji_message_count / self.message_count) * 100 if self.message_count > 0 else 0.0
            )
            avg_fields_per_message = (
                self._total_field_count / self.message_count if self.message_count > 0 else 0.0
            )

            return {
                "messages_per_second": round(messages_per_second, 2),
                "avg_latency_ms": round(avg_latency_ms, 4),
                "emoji_overhead_percent": round(emoji_overhead_percent, 1),
                "total_messages": self.message_count,
                "emoji_messages": self.emoji_message_count,
                "dropped_messages": self.dropped_count,
                "avg_fields_per_message": round(avg_fields_per_message, 1),
                "uptime_seconds": round(elapsed, ),
            }

    def xǁProfileMetricsǁto_dict__mutmut_67(self) -> dict[str, Any]:
        """Serialize metrics to dictionary for JSON output.

        Returns:
            Dictionary containing all current metrics

        """
        with self._lock:
            # Calculate metrics directly to avoid deadlock from property calls
            elapsed = time.time() - self.start_time
            messages_per_second = self.message_count / elapsed if elapsed > 0 else 0.0
            avg_latency_ms = (
                (self.total_duration_ns / self.message_count) / 1_000_000 if self.message_count > 0 else 0.0
            )
            emoji_overhead_percent = (
                (self.emoji_message_count / self.message_count) * 100 if self.message_count > 0 else 0.0
            )
            avg_fields_per_message = (
                self._total_field_count / self.message_count if self.message_count > 0 else 0.0
            )

            return {
                "messages_per_second": round(messages_per_second, 2),
                "avg_latency_ms": round(avg_latency_ms, 4),
                "emoji_overhead_percent": round(emoji_overhead_percent, 1),
                "total_messages": self.message_count,
                "emoji_messages": self.emoji_message_count,
                "dropped_messages": self.dropped_count,
                "avg_fields_per_message": round(avg_fields_per_message, 1),
                "uptime_seconds": round(elapsed, 2),
            }
    
    xǁProfileMetricsǁto_dict__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁProfileMetricsǁto_dict__mutmut_1': xǁProfileMetricsǁto_dict__mutmut_1, 
        'xǁProfileMetricsǁto_dict__mutmut_2': xǁProfileMetricsǁto_dict__mutmut_2, 
        'xǁProfileMetricsǁto_dict__mutmut_3': xǁProfileMetricsǁto_dict__mutmut_3, 
        'xǁProfileMetricsǁto_dict__mutmut_4': xǁProfileMetricsǁto_dict__mutmut_4, 
        'xǁProfileMetricsǁto_dict__mutmut_5': xǁProfileMetricsǁto_dict__mutmut_5, 
        'xǁProfileMetricsǁto_dict__mutmut_6': xǁProfileMetricsǁto_dict__mutmut_6, 
        'xǁProfileMetricsǁto_dict__mutmut_7': xǁProfileMetricsǁto_dict__mutmut_7, 
        'xǁProfileMetricsǁto_dict__mutmut_8': xǁProfileMetricsǁto_dict__mutmut_8, 
        'xǁProfileMetricsǁto_dict__mutmut_9': xǁProfileMetricsǁto_dict__mutmut_9, 
        'xǁProfileMetricsǁto_dict__mutmut_10': xǁProfileMetricsǁto_dict__mutmut_10, 
        'xǁProfileMetricsǁto_dict__mutmut_11': xǁProfileMetricsǁto_dict__mutmut_11, 
        'xǁProfileMetricsǁto_dict__mutmut_12': xǁProfileMetricsǁto_dict__mutmut_12, 
        'xǁProfileMetricsǁto_dict__mutmut_13': xǁProfileMetricsǁto_dict__mutmut_13, 
        'xǁProfileMetricsǁto_dict__mutmut_14': xǁProfileMetricsǁto_dict__mutmut_14, 
        'xǁProfileMetricsǁto_dict__mutmut_15': xǁProfileMetricsǁto_dict__mutmut_15, 
        'xǁProfileMetricsǁto_dict__mutmut_16': xǁProfileMetricsǁto_dict__mutmut_16, 
        'xǁProfileMetricsǁto_dict__mutmut_17': xǁProfileMetricsǁto_dict__mutmut_17, 
        'xǁProfileMetricsǁto_dict__mutmut_18': xǁProfileMetricsǁto_dict__mutmut_18, 
        'xǁProfileMetricsǁto_dict__mutmut_19': xǁProfileMetricsǁto_dict__mutmut_19, 
        'xǁProfileMetricsǁto_dict__mutmut_20': xǁProfileMetricsǁto_dict__mutmut_20, 
        'xǁProfileMetricsǁto_dict__mutmut_21': xǁProfileMetricsǁto_dict__mutmut_21, 
        'xǁProfileMetricsǁto_dict__mutmut_22': xǁProfileMetricsǁto_dict__mutmut_22, 
        'xǁProfileMetricsǁto_dict__mutmut_23': xǁProfileMetricsǁto_dict__mutmut_23, 
        'xǁProfileMetricsǁto_dict__mutmut_24': xǁProfileMetricsǁto_dict__mutmut_24, 
        'xǁProfileMetricsǁto_dict__mutmut_25': xǁProfileMetricsǁto_dict__mutmut_25, 
        'xǁProfileMetricsǁto_dict__mutmut_26': xǁProfileMetricsǁto_dict__mutmut_26, 
        'xǁProfileMetricsǁto_dict__mutmut_27': xǁProfileMetricsǁto_dict__mutmut_27, 
        'xǁProfileMetricsǁto_dict__mutmut_28': xǁProfileMetricsǁto_dict__mutmut_28, 
        'xǁProfileMetricsǁto_dict__mutmut_29': xǁProfileMetricsǁto_dict__mutmut_29, 
        'xǁProfileMetricsǁto_dict__mutmut_30': xǁProfileMetricsǁto_dict__mutmut_30, 
        'xǁProfileMetricsǁto_dict__mutmut_31': xǁProfileMetricsǁto_dict__mutmut_31, 
        'xǁProfileMetricsǁto_dict__mutmut_32': xǁProfileMetricsǁto_dict__mutmut_32, 
        'xǁProfileMetricsǁto_dict__mutmut_33': xǁProfileMetricsǁto_dict__mutmut_33, 
        'xǁProfileMetricsǁto_dict__mutmut_34': xǁProfileMetricsǁto_dict__mutmut_34, 
        'xǁProfileMetricsǁto_dict__mutmut_35': xǁProfileMetricsǁto_dict__mutmut_35, 
        'xǁProfileMetricsǁto_dict__mutmut_36': xǁProfileMetricsǁto_dict__mutmut_36, 
        'xǁProfileMetricsǁto_dict__mutmut_37': xǁProfileMetricsǁto_dict__mutmut_37, 
        'xǁProfileMetricsǁto_dict__mutmut_38': xǁProfileMetricsǁto_dict__mutmut_38, 
        'xǁProfileMetricsǁto_dict__mutmut_39': xǁProfileMetricsǁto_dict__mutmut_39, 
        'xǁProfileMetricsǁto_dict__mutmut_40': xǁProfileMetricsǁto_dict__mutmut_40, 
        'xǁProfileMetricsǁto_dict__mutmut_41': xǁProfileMetricsǁto_dict__mutmut_41, 
        'xǁProfileMetricsǁto_dict__mutmut_42': xǁProfileMetricsǁto_dict__mutmut_42, 
        'xǁProfileMetricsǁto_dict__mutmut_43': xǁProfileMetricsǁto_dict__mutmut_43, 
        'xǁProfileMetricsǁto_dict__mutmut_44': xǁProfileMetricsǁto_dict__mutmut_44, 
        'xǁProfileMetricsǁto_dict__mutmut_45': xǁProfileMetricsǁto_dict__mutmut_45, 
        'xǁProfileMetricsǁto_dict__mutmut_46': xǁProfileMetricsǁto_dict__mutmut_46, 
        'xǁProfileMetricsǁto_dict__mutmut_47': xǁProfileMetricsǁto_dict__mutmut_47, 
        'xǁProfileMetricsǁto_dict__mutmut_48': xǁProfileMetricsǁto_dict__mutmut_48, 
        'xǁProfileMetricsǁto_dict__mutmut_49': xǁProfileMetricsǁto_dict__mutmut_49, 
        'xǁProfileMetricsǁto_dict__mutmut_50': xǁProfileMetricsǁto_dict__mutmut_50, 
        'xǁProfileMetricsǁto_dict__mutmut_51': xǁProfileMetricsǁto_dict__mutmut_51, 
        'xǁProfileMetricsǁto_dict__mutmut_52': xǁProfileMetricsǁto_dict__mutmut_52, 
        'xǁProfileMetricsǁto_dict__mutmut_53': xǁProfileMetricsǁto_dict__mutmut_53, 
        'xǁProfileMetricsǁto_dict__mutmut_54': xǁProfileMetricsǁto_dict__mutmut_54, 
        'xǁProfileMetricsǁto_dict__mutmut_55': xǁProfileMetricsǁto_dict__mutmut_55, 
        'xǁProfileMetricsǁto_dict__mutmut_56': xǁProfileMetricsǁto_dict__mutmut_56, 
        'xǁProfileMetricsǁto_dict__mutmut_57': xǁProfileMetricsǁto_dict__mutmut_57, 
        'xǁProfileMetricsǁto_dict__mutmut_58': xǁProfileMetricsǁto_dict__mutmut_58, 
        'xǁProfileMetricsǁto_dict__mutmut_59': xǁProfileMetricsǁto_dict__mutmut_59, 
        'xǁProfileMetricsǁto_dict__mutmut_60': xǁProfileMetricsǁto_dict__mutmut_60, 
        'xǁProfileMetricsǁto_dict__mutmut_61': xǁProfileMetricsǁto_dict__mutmut_61, 
        'xǁProfileMetricsǁto_dict__mutmut_62': xǁProfileMetricsǁto_dict__mutmut_62, 
        'xǁProfileMetricsǁto_dict__mutmut_63': xǁProfileMetricsǁto_dict__mutmut_63, 
        'xǁProfileMetricsǁto_dict__mutmut_64': xǁProfileMetricsǁto_dict__mutmut_64, 
        'xǁProfileMetricsǁto_dict__mutmut_65': xǁProfileMetricsǁto_dict__mutmut_65, 
        'xǁProfileMetricsǁto_dict__mutmut_66': xǁProfileMetricsǁto_dict__mutmut_66, 
        'xǁProfileMetricsǁto_dict__mutmut_67': xǁProfileMetricsǁto_dict__mutmut_67
    }
    
    def to_dict(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁProfileMetricsǁto_dict__mutmut_orig"), object.__getattribute__(self, "xǁProfileMetricsǁto_dict__mutmut_mutants"), args, kwargs, self)
        return result 
    
    to_dict.__signature__ = _mutmut_signature(xǁProfileMetricsǁto_dict__mutmut_orig)
    xǁProfileMetricsǁto_dict__mutmut_orig.__name__ = 'xǁProfileMetricsǁto_dict'


# <3 🧱🤝⏱️🪄
