#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from __future__ import annotations

import random
import time
from typing import Any

import structlog

from provide.foundation.errors.profiling import SamplingError
from provide.foundation.profiling.defaults import DEFAULT_PROFILING_SAMPLE_RATE
from provide.foundation.profiling.metrics import ProfileMetrics

"""Structlog processor for collecting performance metrics.

Provides a processor that can be added to the structlog processor chain
to collect real-time performance metrics with minimal overhead.
"""


class ProfilingProcessor:
    """Structlog processor that collects performance metrics via sampling.

    This processor integrates into Foundation's existing structlog pipeline
    to collect metrics about message processing performance, emoji overhead,
    and throughput with configurable sampling to minimize performance impact.

    Example:
        >>> processor = ProfilingProcessor(sample_rate=0.01)  # 1% sampling
        >>> # Add to structlog processor chain
        >>> processors.append(processor)

        >>> # Later, get metrics
        >>> metrics = processor.get_metrics()
        >>> print(f"Processing {metrics.messages_per_second:.0f} msg/sec")

    """

    def __init__(self, sample_rate: float = DEFAULT_PROFILING_SAMPLE_RATE) -> None:
        """Initialize profiling processor with sampling configuration.

        Args:
            sample_rate: Fraction of messages to sample (0.0 to 1.0)
                        0.01 = 1% sampling for minimal overhead

        """
        if not 0.0 <= sample_rate <= 1.0:
            raise SamplingError("Sample rate must be between 0.0 and 1.0", sample_rate=sample_rate)

        self.sample_rate = sample_rate
        self.metrics = ProfileMetrics()
        self._enabled = True

    def __call__(
        self,
        logger: Any,
        method_name: str,
        event_dict: structlog.types.EventDict,
    ) -> structlog.types.EventDict:
        """Process log event and optionally collect metrics.

        This is the main entry point called by structlog for each log message.
        Uses sampling to minimize performance overhead.

        Args:
            logger: The logger instance (unused)
            method_name: The logging method name (unused)
            event_dict: The event dictionary to process

        Returns:
            The event_dict unchanged (pass-through processor)

        """
        # Always return event_dict unchanged - we're just observing
        if not self._enabled:
            return event_dict

        # Use sampling to reduce overhead
        if random.random() > self.sample_rate:
            return event_dict

        # Measure processing time for this event
        start_time = time.perf_counter_ns()

        try:
            # Analyze event characteristics
            has_emoji = self._detect_emoji_processing(event_dict)
            field_count = len(event_dict)

            # Record metrics (very fast operation)
            processing_time = time.perf_counter_ns() - start_time
            self.metrics.record_message(
                duration_ns=processing_time,
                has_emoji=has_emoji,
                field_count=field_count,
            )

        except Exception:
            # Never let profiling break the logging pipeline
            # Silently ignore any profiling errors
            pass

        return event_dict

    def _detect_emoji_processing(self, event_dict: structlog.types.EventDict) -> bool:
        """Detect if this log event involved emoji processing.

        Args:
            event_dict: The structlog event dictionary

        Returns:
            True if emoji processing was involved

        """
        # Check for emoji-related fields that Foundation adds
        emoji_indicators = ["emoji", "emoji_prefix", "logger_name_emoji"]

        return any(key in event_dict for key in emoji_indicators)

    def enable(self) -> None:
        """Enable metrics collection."""
        self._enabled = True

    def disable(self) -> None:
        """Disable metrics collection."""
        self._enabled = False

    def reset(self) -> None:
        """Reset collected metrics."""
        self.metrics.reset()

    def get_metrics(self) -> ProfileMetrics:
        """Get current metrics.

        Returns:
            Current ProfileMetrics instance

        """
        return self.metrics


# 🧱🏗️🔚
