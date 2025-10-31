#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from __future__ import annotations

import threading
import time
from typing import Any

"""Performance metrics collection for Foundation profiling.

Provides thread-safe metrics collection and calculation for monitoring
Foundation's logging and telemetry performance.
"""


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

    def __init__(self) -> None:
        """Initialize metrics with zero values and current timestamp."""
        self._lock = threading.Lock()
        self.reset()

    def record_message(
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

    def reset(self) -> None:
        """Reset all metrics to initial values with new start time."""
        with self._lock:
            self.message_count = 0
            self.total_duration_ns = 0
            self.emoji_message_count = 0
            self.dropped_count = 0
            self.start_time = time.time()
            self._total_field_count = 0

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

    def to_dict(self) -> dict[str, Any]:
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


# 🧱🏗️🔚
