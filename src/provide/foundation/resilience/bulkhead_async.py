#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from __future__ import annotations

import asyncio
from collections import deque
import contextlib
from typing import Any

from attrs import define, field

from provide.foundation.resilience.defaults import (
    DEFAULT_BULKHEAD_MAX_CONCURRENT,
    DEFAULT_BULKHEAD_MAX_QUEUE_SIZE,
    DEFAULT_BULKHEAD_TIMEOUT,
)

"""Asynchronous bulkhead resource pool implementation.

This module provides an async-safe resource pool for asynchronous contexts only.
For sync contexts, use SyncResourcePool from bulkhead_sync.
"""


@define(kw_only=True, slots=True)
class AsyncResourcePool:
    """Asynchronous resource pool with limited capacity for isolation.

    Async-safe implementation using asyncio.Lock and asyncio.Event.
    For sync contexts, use SyncResourcePool instead.
    """

    max_concurrent: int = field(default=DEFAULT_BULKHEAD_MAX_CONCURRENT)
    max_queue_size: int = field(default=DEFAULT_BULKHEAD_MAX_QUEUE_SIZE)
    timeout: float = field(default=DEFAULT_BULKHEAD_TIMEOUT)

    # Internal state - async-safe using asyncio primitives
    _active_count: int = field(default=0, init=False)
    _waiting_count: int = field(default=0, init=False)
    _lock: asyncio.Lock = field(factory=asyncio.Lock, init=False)
    # FIFO queue of waiting coroutines (async only)
    _waiters: deque[asyncio.Event] = field(factory=deque, init=False)

    def __attrs_post_init__(self) -> None:
        """Initialize internal state."""
        pass

    async def active_count(self) -> int:
        """Number of currently active operations."""
        async with self._lock:
            return self._active_count

    async def available_capacity(self) -> int:
        """Number of available slots."""
        async with self._lock:
            return max(0, self.max_concurrent - self._active_count)

    async def queue_size(self) -> int:
        """Current number of waiting operations."""
        async with self._lock:
            return self._waiting_count

    async def acquire(self, timeout: float | None = None) -> bool:
        """Acquire a resource slot (async).

        Args:
            timeout: Maximum time to wait (defaults to pool timeout)

        Returns:
            True if acquired, False if timeout

        Raises:
            RuntimeError: If queue is full
        """
        actual_timeout = timeout if timeout is not None else self.timeout

        # Try to acquire immediately
        async with self._lock:
            if self._active_count < self.max_concurrent:
                self._active_count += 1
                return True

            # Check queue limit
            if self._waiting_count >= self.max_queue_size:
                raise RuntimeError(f"Queue is full (max: {self.max_queue_size})")

            # Add to wait queue
            self._waiting_count += 1
            waiter = asyncio.Event()
            self._waiters.append(waiter)

        # Wait for signal from release
        try:
            await asyncio.wait_for(waiter.wait(), timeout=actual_timeout)
            # Successfully signaled, we now have the slot
            return True
        except TimeoutError:
            # Timeout - remove from queue
            async with self._lock:
                with contextlib.suppress(ValueError):
                    # Remove from queue if still present (already removed by signal if not found)
                    self._waiters.remove(waiter)
            return False
        finally:
            async with self._lock:
                self._waiting_count -= 1

    async def release(self) -> None:
        """Release a resource slot."""
        async with self._lock:
            if self._active_count > 0:
                self._active_count -= 1

            # Signal next waiter in FIFO order
            if self._waiters:
                waiter_event = self._waiters.popleft()
                self._active_count += 1
                waiter_event.set()

    async def get_stats(self) -> dict[str, Any]:
        """Get pool statistics."""
        async with self._lock:
            return {
                "max_concurrent": self.max_concurrent,
                "active_count": self._active_count,
                "available_capacity": self.max_concurrent - self._active_count,
                "waiting_count": self._waiting_count,
                "max_queue_size": self.max_queue_size,
                "utilization": self._active_count / self.max_concurrent if self.max_concurrent > 0 else 0.0,
            }


__all__ = ["AsyncResourcePool"]

# 🧱🏗️🔚
