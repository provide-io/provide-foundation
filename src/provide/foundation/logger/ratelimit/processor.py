#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from __future__ import annotations

#
# processor.py
#
import time
from typing import Any

import structlog

from provide.foundation.logger.ratelimit.limiters import GlobalRateLimiter

"""Structlog processor for rate limiting log messages."""


class RateLimiterProcessor:
    """Structlog processor that applies rate limiting to log messages.
    Can be configured with global and per-logger rate limits.
    """

    def __init__(
        self,
        emit_warning_on_limit: bool = True,
        warning_interval_seconds: float = 60.0,
        summary_interval_seconds: float = 5.0,
    ) -> None:
        """Initialize the rate limiter processor.

        Args:
            emit_warning_on_limit: Whether to emit a warning when rate limited
            warning_interval_seconds: Minimum seconds between rate limit warnings
            summary_interval_seconds: Interval for rate limit summary reports

        """
        self.rate_limiter = GlobalRateLimiter()
        self.emit_warning_on_limit = emit_warning_on_limit
        self.warning_interval_seconds = warning_interval_seconds

        # Track last warning time per logger
        self.last_warning_times: dict[str, float] = {}

        # Track suppressed message counts
        self.suppressed_counts: dict[str, int] = {}
        self.last_summary_time = time.monotonic()
        self.summary_interval = summary_interval_seconds  # Emit summary periodically

    def __call__(
        self,
        logger: Any,
        method_name: str,
        event_dict: structlog.types.EventDict,
    ) -> structlog.types.EventDict:
        """Process a log event, applying rate limiting.

        Args:
            logger: The logger instance
            method_name: The log method name (debug, info, etc.)
            event_dict: The event dictionary

        Returns:
            The event dictionary if allowed, or raises DropEvent if rate limited

        """
        logger_name = event_dict.get("logger_name", "unknown")

        # Check if this log is allowed (pass event_dict for tracking)
        allowed, reason = self.rate_limiter.is_allowed(logger_name, event_dict)

        if not allowed:
            # Track suppressed count
            if logger_name not in self.suppressed_counts:
                self.suppressed_counts[logger_name] = 0
            self.suppressed_counts[logger_name] += 1

            # Optionally emit a warning about rate limiting
            if self.emit_warning_on_limit:
                now = time.monotonic()
                last_warning = self.last_warning_times.get(logger_name, 0)

                if now - last_warning >= self.warning_interval_seconds:
                    # Create a rate limit warning event
                    self.last_warning_times[logger_name] = now

                    # Return a modified event indicating rate limiting
                    return {
                        "event": f"⚠️ Rate limit: {reason}",
                        "level": "warning",
                        "logger_name": "provide.foundation.ratelimit",
                        "suppressed_count": self.suppressed_counts[logger_name],
                        "original_logger": logger_name,
                        "_rate_limit_warning": True,
                    }

            # Drop the event
            raise structlog.DropEvent

        # Check if we should emit a summary
        now = time.monotonic()
        if now - self.last_summary_time >= self.summary_interval:
            # Always check and emit summary if there's been any rate limiting
            self._emit_summary()
            self.last_summary_time = now

        return event_dict

    def _emit_summary(self) -> None:
        """Emit a summary of rate-limited messages."""
        # Get current stats first to check if any rate limiting has occurred
        stats = self.rate_limiter.get_stats()

        # Check if there's been any rate limiting activity
        global_stats = stats.get("global") or {}
        total_denied = global_stats.get("total_denied", 0)

        if not self.suppressed_counts and total_denied == 0:
            return  # No rate limiting activity to report

        total_suppressed = sum(self.suppressed_counts.values())

        # Get a logger for rate limit summaries
        try:
            from provide.foundation.logger import get_logger

            summary_logger = get_logger("provide.foundation.ratelimit.summary")

            # Calculate rate limiting percentage
            total_allowed = global_stats.get("total_allowed", 0)
            total_attempts = total_allowed + total_denied
            denial_rate = total_denied / total_attempts * 100 if total_attempts > 0 else 0

            # Format the summary message
            summary_logger.warning(
                f"⚠️ Rate limiting active: {total_suppressed:,} logs dropped in last {self.summary_interval}s | "
                f"Denial rate: {denial_rate:.1f}% | "
                f"Tokens: {global_stats.get('tokens_available', 0):.0f}/{global_stats.get('capacity', 0):.0f}",
                suppressed_by_logger=dict(self.suppressed_counts) if self.suppressed_counts else {},
                total_suppressed=total_suppressed,
                total_denied_overall=total_denied,
                total_allowed_overall=total_allowed,
                denial_rate_percent=denial_rate,
                tokens_available=global_stats.get("tokens_available", 0),
                capacity=global_stats.get("capacity", 0),
                refill_rate=global_stats.get("refill_rate", 0),
            )

            # Reset counts after summary
            self.suppressed_counts.clear()
        except Exception:
            # If we can't log the summary, just clear counts
            self.suppressed_counts.clear()


def create_rate_limiter_processor(
    global_rate: float | None = None,
    global_capacity: float | None = None,
    per_logger_rates: dict[str, tuple[float, float]] | None = None,
    emit_warnings: bool = True,
    summary_interval: float = 5.0,
    max_queue_size: int = 1000,
    max_memory_mb: float | None = None,
    overflow_policy: str = "drop_oldest",
) -> RateLimiterProcessor:
    """Factory function to create and configure a rate limiter processor.

    Args:
        global_rate: Global logs per second limit
        global_capacity: Global burst capacity
        per_logger_rates: Dict of logger_name -> (rate, capacity) tuples
        emit_warnings: Whether to emit warnings when rate limited
        summary_interval: Seconds between rate limit summary reports
        max_queue_size: Maximum queue size when buffering
        max_memory_mb: Maximum memory for buffered logs
        overflow_policy: Policy when queue is full

    Returns:
        Configured RateLimiterProcessor instance

    """
    processor = RateLimiterProcessor(
        emit_warning_on_limit=emit_warnings,
        summary_interval_seconds=summary_interval,
    )

    # Determine if we should use buffered rate limiting
    use_buffered = max_queue_size > 0 and overflow_policy in (
        "drop_oldest",
        "drop_newest",
    )

    # Configure the global rate limiter
    processor.rate_limiter.configure(
        global_rate=global_rate,
        global_capacity=global_capacity,
        per_logger_rates=per_logger_rates,
        use_buffered=use_buffered,
        max_queue_size=max_queue_size,
        max_memory_mb=max_memory_mb,
        overflow_policy=overflow_policy,
    )

    return processor


# 🧱🏗️🔚
