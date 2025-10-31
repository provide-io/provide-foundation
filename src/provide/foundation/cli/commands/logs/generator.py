#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from __future__ import annotations

import random
import threading
import time
from typing import Any

from attrs import define, field

from provide.foundation.cli.commands.logs.constants import (
    ACTIONS,
    BURROUGHS_PHRASES,
    DOMAINS,
    ERROR_CODES,
    ERROR_TYPES,
    MAX_DURATION_MS,
    MIN_DURATION_MS,
    NON_ERROR_LEVELS,
    NORMAL_OBJECTS,
    NORMAL_OPERATIONS,
    OPERATIONS,
    SERVICE_NAMES,
    STATUSES,
)
from provide.foundation.logger import get_logger

"""Log generator for testing and development."""


@define(slots=True)
class LogGenerator:
    """Generates log entries for testing OpenObserve integration.

    This class encapsulates log generation logic with support for:
    - Multiple message styles (normal, Burroughs-inspired)
    - Configurable error rates
    - Thread-safe trace and span ID generation
    - Rate-controlled log emission
    """

    style: str = field(default="normal")
    error_rate: float = field(default=0.1)

    # Internal counters
    _trace_counter: int = field(default=0, init=False, repr=False)
    _span_counter: int = field(default=0, init=False, repr=False)
    _trace_lock: threading.Lock = field(factory=threading.Lock, init=False, repr=False)

    def generate_trace_id(self) -> str:
        """Generate a unique trace ID.

        Returns:
            Formatted trace ID string

        """
        with self._trace_lock:
            trace_id = f"trace_{self._trace_counter:08d}"
            self._trace_counter += 1
        return trace_id

    def generate_span_id(self) -> str:
        """Generate a unique span ID.

        Returns:
            Formatted span ID string

        """
        with self._trace_lock:
            span_id = f"span_{self._span_counter:08d}"
            self._span_counter += 1
        return span_id

    def _generate_message(self) -> str:
        """Generate a log message based on configured style.

        Returns:
            Generated message string

        """
        if self.style == "burroughs":
            return random.choice(BURROUGHS_PHRASES)  # nosec B311 - Test data generation

        # Normal tech-style messages
        operation = random.choice(NORMAL_OPERATIONS)  # nosec B311 - Test data
        obj = random.choice(NORMAL_OBJECTS)  # nosec B311 - Test data
        return f"Successfully {operation} {obj}"

    def generate_log_entry(self, index: int) -> dict[str, Any]:
        """Generate a single log entry with optional error simulation.

        Args:
            index: Log entry index

        Returns:
            Dict containing log entry data

        """
        message = self._generate_message()
        is_error = random.random() < self.error_rate  # nosec B311 - Test data generation

        # Determine trace ID (new trace every 10 entries)
        trace_id = self.generate_trace_id() if index % 10 == 0 else f"trace_{self._trace_counter - 1:08d}"

        # Base entry
        entry = {
            "message": message,
            "service": random.choice(SERVICE_NAMES),  # nosec B311 - Test data
            "operation": random.choice(OPERATIONS),  # nosec B311 - Test data
            "iteration": index,
            "trace_id": trace_id,
            "span_id": self.generate_span_id(),
            "duration_ms": random.randint(MIN_DURATION_MS, MAX_DURATION_MS),  # nosec B311 - Test data
        }

        # Add error fields if this is an error
        if is_error:
            entry["level"] = "error"
            entry["error_code"] = random.choice(ERROR_CODES)  # nosec B311 - Test data
            entry["error_type"] = random.choice(ERROR_TYPES)  # nosec B311 - Test data
        else:
            # Random log level for non-errors
            entry["level"] = random.choice(NON_ERROR_LEVELS)  # nosec B311 - Test data

        # Add domain/action/status for DAS emoji system
        entry["domain"] = random.choice(DOMAINS)  # nosec B311 - Test data
        entry["action"] = random.choice(ACTIONS)  # nosec B311 - Test data
        entry["status"] = "error" if is_error else random.choice(STATUSES)  # nosec B311 - Test data

        return entry

    def send_log_entry(
        self, entry: dict[str, Any], logs_sent: int, logs_failed: int, logs_rate_limited: int
    ) -> tuple[int, int, int]:
        """Send a log entry and update counters.

        Args:
            entry: Log entry dictionary to send
            logs_sent: Current count of successfully sent logs
            logs_failed: Current count of failed logs
            logs_rate_limited: Current count of rate-limited logs

        Returns:
            Updated counters tuple (logs_sent, logs_failed, logs_rate_limited)

        """
        try:
            service_logger = get_logger(f"generated.{entry['service']}")
            level = entry.pop("level", "info")
            message = entry.pop("message")
            getattr(service_logger, level)(message, **entry)
            logs_sent += 1
        except Exception as e:
            from provide.foundation.errors import RateLimitExceededError

            logs_failed += 1
            if isinstance(e, RateLimitExceededError):
                logs_rate_limited += 1
        return logs_sent, logs_failed, logs_rate_limited

    def generate_continuous(
        self, rate: float, enable_rate_limit: bool, logs_rate_limited: int
    ) -> tuple[int, int, int]:
        """Generate logs in continuous mode.

        Args:
            rate: Target logs per second
            enable_rate_limit: Whether rate limiting is enabled
            logs_rate_limited: Initial rate-limited counter

        Returns:
            Final counters tuple (logs_sent, logs_failed, logs_rate_limited)

        """
        logs_sent = 0
        logs_failed = 0
        start_time = time.time()
        last_stats_time = start_time
        last_stats_sent = 0
        index = 0

        while True:
            current_time = time.time()

            # Generate and send log entry
            entry = self.generate_log_entry(index)
            index += 1
            logs_sent, logs_failed, logs_rate_limited = self.send_log_entry(
                entry, logs_sent, logs_failed, logs_rate_limited
            )

            # Control rate
            elapsed = current_time - start_time
            expected_count = int(elapsed * rate)

            if logs_sent >= expected_count:
                next_time = start_time + (logs_sent / rate)
                sleep_time = next_time - time.time()
                if sleep_time > 0:
                    time.sleep(sleep_time)

            # Print stats
            from provide.foundation.cli.commands.logs.stats import print_stats

            last_stats_time, last_stats_sent = print_stats(
                current_time,
                last_stats_time,
                logs_sent,
                last_stats_sent,
                logs_failed,
                enable_rate_limit,
                logs_rate_limited,
            )

    def generate_fixed_count(self, count: int, rate: float) -> tuple[int, int, int]:
        """Generate a fixed number of logs.

        Args:
            count: Number of logs to generate
            rate: Target logs per second (0 for unlimited)

        Returns:
            Final counters tuple (logs_sent, logs_failed, logs_rate_limited)

        """
        logs_sent = 0
        logs_failed = 0
        logs_rate_limited = 0

        for i in range(count):
            entry = self.generate_log_entry(i)
            logs_sent, logs_failed, logs_rate_limited = self.send_log_entry(
                entry, logs_sent, logs_failed, logs_rate_limited
            )

            # Control rate
            if rate > 0:
                time.sleep(1.0 / rate)

            # Print progress
            from provide.foundation.cli.commands.logs.stats import print_progress

            print_progress(i, count)

        return logs_sent, logs_failed, logs_rate_limited


# 🧱🏗️🔚
