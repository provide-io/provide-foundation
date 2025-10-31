#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from __future__ import annotations

#
# limiters.py
#
import asyncio
import threading
import time
from typing import Any

"""Rate limiter implementations for Foundation's logging system."""


class SyncRateLimiter:
    """Synchronous token bucket rate limiter for controlling log output rates.
    Thread-safe implementation suitable for synchronous logging operations.
    """

    def __init__(self, capacity: float, refill_rate: float) -> None:
        """Initialize the rate limiter.

        Args:
            capacity: Maximum number of tokens (burst capacity)
            refill_rate: Tokens refilled per second

        """
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        if refill_rate <= 0:
            raise ValueError("Refill rate must be positive")

        self.capacity = float(capacity)
        self.refill_rate = float(refill_rate)
        self.tokens = float(capacity)
        self.last_refill = time.monotonic()
        self.lock = threading.Lock()

        # Track statistics
        self.total_allowed = 0
        self.total_denied = 0
        self.last_denied_time: float | None = None

    def is_allowed(self) -> bool:
        """Check if a log message is allowed based on available tokens.

        Returns:
            True if the log should be allowed, False if rate limited

        """
        with self.lock:
            now = time.monotonic()
            elapsed = now - self.last_refill

            # Refill tokens based on elapsed time
            if elapsed > 0:
                tokens_to_add = elapsed * self.refill_rate
                self.tokens = min(self.capacity, self.tokens + tokens_to_add)
                self.last_refill = now

            # Try to consume a token
            if self.tokens >= 1.0:
                self.tokens -= 1.0
                self.total_allowed += 1
                return True
            self.total_denied += 1
            self.last_denied_time = now
            return False

    def get_stats(self) -> dict[str, Any]:
        """Get rate limiter statistics."""
        with self.lock:
            return {
                "tokens_available": self.tokens,
                "capacity": self.capacity,
                "refill_rate": self.refill_rate,
                "total_allowed": self.total_allowed,
                "total_denied": self.total_denied,
                "last_denied_time": self.last_denied_time,
            }


class AsyncRateLimiter:
    """Asynchronous token bucket rate limiter.
    Uses asyncio.Lock for thread safety in async contexts.
    """

    def __init__(self, capacity: float, refill_rate: float) -> None:
        """Initialize the async rate limiter.

        Args:
            capacity: Maximum number of tokens (burst capacity)
            refill_rate: Tokens refilled per second

        """
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        if refill_rate <= 0:
            raise ValueError("Refill rate must be positive")

        self.capacity = float(capacity)
        self.refill_rate = float(refill_rate)
        self.tokens = float(capacity)
        self.last_refill = time.monotonic()
        self._lock = asyncio.Lock()

        # Track statistics
        self.total_allowed = 0
        self.total_denied = 0
        self.last_denied_time: float | None = None

    async def is_allowed(self) -> bool:
        """Check if a log message is allowed based on available tokens.

        Returns:
            True if the log should be allowed, False if rate limited

        """
        async with self._lock:
            now = time.monotonic()
            elapsed = now - self.last_refill

            # Refill tokens based on elapsed time
            if elapsed > 0:
                tokens_to_add = elapsed * self.refill_rate
                self.tokens = min(self.capacity, self.tokens + tokens_to_add)
                self.last_refill = now

            # Try to consume a token
            if self.tokens >= 1.0:
                self.tokens -= 1.0
                self.total_allowed += 1
                return True
            self.total_denied += 1
            self.last_denied_time = now
            return False

    async def get_stats(self) -> dict[str, Any]:
        """Get rate limiter statistics."""
        async with self._lock:
            return {
                "tokens_available": self.tokens,
                "capacity": self.capacity,
                "refill_rate": self.refill_rate,
                "total_allowed": self.total_allowed,
                "total_denied": self.total_denied,
                "last_denied_time": self.last_denied_time,
            }


class GlobalRateLimiter:
    """Global rate limiter singleton for Foundation's logging system.
    Manages per-logger and global rate limits.
    """

    _instance = None
    _lock = threading.Lock()
    _initialized: bool

    def __new__(cls) -> GlobalRateLimiter:
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance

    def __init__(self) -> None:
        if self._initialized:
            return

        self._initialized = True
        self.global_limiter: Any = None
        self.logger_limiters: dict[str, SyncRateLimiter] = {}
        self.lock = threading.Lock()

        # Default configuration (can be overridden)
        self.global_rate: float | None = None
        self.global_capacity: float | None = None
        self.per_logger_rates: dict[str, tuple[float, float]] = {}

        # Queue configuration
        self.use_buffered = False
        self.max_queue_size = 1000
        self.max_memory_mb: float | None = None
        self.overflow_policy = "drop_oldest"

    def configure(
        self,
        global_rate: float | None = None,
        global_capacity: float | None = None,
        per_logger_rates: dict[str, tuple[float, float]] | None = None,
        use_buffered: bool = False,
        max_queue_size: int = 1000,
        max_memory_mb: float | None = None,
        overflow_policy: str = "drop_oldest",
    ) -> None:
        """Configure the global rate limiter.

        Args:
            global_rate: Global logs per second limit
            global_capacity: Global burst capacity
            per_logger_rates: Dict of logger_name -> (rate, capacity) tuples
            use_buffered: Use buffered rate limiter with tracking
            max_queue_size: Maximum queue size for buffered limiter
            max_memory_mb: Maximum memory for buffered limiter
            overflow_policy: What to do when queue is full

        """
        with self.lock:
            self.use_buffered = use_buffered
            self.max_queue_size = max_queue_size
            self.max_memory_mb = max_memory_mb
            self.overflow_policy = overflow_policy

            if global_rate is not None and global_capacity is not None:
                self.global_rate = global_rate
                self.global_capacity = global_capacity

                if use_buffered:
                    from provide.foundation.logger.ratelimit.queue_limiter import (
                        BufferedRateLimiter,
                    )

                    self.global_limiter = BufferedRateLimiter(
                        capacity=global_capacity,
                        refill_rate=global_rate,
                        buffer_size=max_queue_size,
                        track_dropped=True,
                    )
                else:
                    self.global_limiter = SyncRateLimiter(global_capacity, global_rate)

            if per_logger_rates:
                self.per_logger_rates = per_logger_rates
                # Create rate limiters for configured loggers
                for logger_name, (rate, capacity) in per_logger_rates.items():
                    self.logger_limiters[logger_name] = SyncRateLimiter(capacity, rate)

    def is_allowed(self, logger_name: str, item: Any | None = None) -> tuple[bool, str | None]:
        """Check if a log from a specific logger is allowed.

        Args:
            logger_name: Name of the logger
            item: Optional item for buffered tracking

        Returns:
            Tuple of (allowed, reason) where reason is set if denied

        """
        with self.lock:
            # Check per-logger limit first
            if logger_name in self.logger_limiters and not self.logger_limiters[logger_name].is_allowed():
                return False, f"Logger '{logger_name}' rate limit exceeded"

            # Check global limit
            if self.global_limiter:
                if self.use_buffered:
                    # BufferedRateLimiter returns tuple
                    from provide.foundation.logger.ratelimit.queue_limiter import (
                        BufferedRateLimiter,
                    )

                    if isinstance(self.global_limiter, BufferedRateLimiter):
                        allowed, reason = self.global_limiter.is_allowed(item)
                        if not allowed:
                            return False, reason or "Global rate limit exceeded"
                # SyncRateLimiter returns bool
                elif not self.global_limiter.is_allowed():
                    return False, "Global rate limit exceeded"

            return True, None

    def get_stats(self) -> dict[str, Any]:
        """Get comprehensive rate limiting statistics."""
        with self.lock:
            stats: dict[str, Any] = {
                "global": self.global_limiter.get_stats() if self.global_limiter else None,
                "per_logger": {},
            }

            for logger_name, limiter in self.logger_limiters.items():
                stats["per_logger"][logger_name] = limiter.get_stats()

            return stats


# 🧱🏗️🔚
