#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from __future__ import annotations

from collections import deque
import contextlib
import threading
from typing import Any

from attrs import define, field

from provide.foundation.resilience.defaults import (
    DEFAULT_BULKHEAD_MAX_CONCURRENT,
    DEFAULT_BULKHEAD_MAX_QUEUE_SIZE,
    DEFAULT_BULKHEAD_TIMEOUT,
)

"""Synchronous bulkhead resource pool implementation.

This module provides a thread-safe resource pool for synchronous contexts only.
For async contexts, use AsyncResourcePool from bulkhead_async.
"""


@define(kw_only=True, slots=True)
class SyncResourcePool:
    """Synchronous resource pool with limited capacity for isolation.

    Thread-safe implementation using threading.Lock and threading.Event.
    For async contexts, use AsyncResourcePool instead.
    """

    max_concurrent: int = field(default=DEFAULT_BULKHEAD_MAX_CONCURRENT)
    max_queue_size: int = field(default=DEFAULT_BULKHEAD_MAX_QUEUE_SIZE)
    timeout: float = field(default=DEFAULT_BULKHEAD_TIMEOUT)

    # Internal state - thread-safe using threading primitives
    _active_count: int = field(default=0, init=False)
    _waiting_count: int = field(default=0, init=False)
    _counter_lock: threading.Lock = field(factory=threading.Lock, init=False)
    # FIFO queue of waiting threads (sync only)
    _waiters: deque[threading.Event] = field(factory=deque, init=False)

    def __attrs_post_init__(self) -> None:
        """Initialize internal state."""
        pass

    def active_count(self) -> int:
        """Number of currently active operations."""
        with self._counter_lock:
            return self._active_count

    def available_capacity(self) -> int:
        """Number of available slots."""
        with self._counter_lock:
            return max(0, self.max_concurrent - self._active_count)

    def queue_size(self) -> int:
        """Current number of waiting operations."""
        with self._counter_lock:
            return self._waiting_count

    def acquire(self, timeout: float | None = None) -> bool:
        """Acquire a resource slot (blocking).

        Args:
            timeout: Maximum time to wait (defaults to pool timeout)

        Returns:
            True if acquired, False if timeout

        Raises:
            RuntimeError: If queue is full
        """
        actual_timeout = timeout if timeout is not None else self.timeout

        # Try to acquire immediately
        with self._counter_lock:
            if self._active_count < self.max_concurrent:
                self._active_count += 1
                return True

            # Check queue limit
            if self._waiting_count >= self.max_queue_size:
                raise RuntimeError(f"Queue is full (max: {self.max_queue_size})")

            # Add to wait queue
            self._waiting_count += 1
            waiter = threading.Event()
            self._waiters.append(waiter)

        # Wait for signal from release
        try:
            if waiter.wait(timeout=actual_timeout):
                # Successfully signaled, we now have the slot
                return True
            # Timeout - remove from queue
            with self._counter_lock, contextlib.suppress(ValueError):
                # Remove from queue if still present (already removed by signal if not found)
                self._waiters.remove(waiter)
            return False
        finally:
            with self._counter_lock:
                self._waiting_count -= 1

    def release(self) -> None:
        """Release a resource slot."""
        with self._counter_lock:
            if self._active_count > 0:
                self._active_count -= 1

            # Signal next waiter in FIFO order
            if self._waiters:
                waiter_event = self._waiters.popleft()
                self._active_count += 1
                waiter_event.set()

    def get_stats(self) -> dict[str, Any]:
        """Get pool statistics."""
        with self._counter_lock:
            return {
                "max_concurrent": self.max_concurrent,
                "active_count": self._active_count,
                "available_capacity": self.max_concurrent - self._active_count,
                "waiting_count": self._waiting_count,
                "max_queue_size": self.max_queue_size,
                "utilization": self._active_count / self.max_concurrent if self.max_concurrent > 0 else 0.0,
            }


__all__ = ["SyncResourcePool"]

# 🧱🏗️🔚
