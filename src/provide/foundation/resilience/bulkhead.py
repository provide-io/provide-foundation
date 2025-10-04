from __future__ import annotations

import asyncio
from collections.abc import Awaitable, Callable
import contextlib
import threading
import time
from typing import Any, TypeVar

from attrs import define, field

from provide.foundation.config.defaults import (
    DEFAULT_BULKHEAD_MAX_CONCURRENT,
    DEFAULT_BULKHEAD_MAX_QUEUE_SIZE,
    DEFAULT_BULKHEAD_TIMEOUT,
)

"""Bulkhead pattern for resource isolation and limiting.

The bulkhead pattern isolates resources to prevent failures in one part of
the system from cascading to other parts. It limits concurrent access to
resources and provides isolation boundaries.
"""

T = TypeVar("T")


@define(kw_only=True, slots=True)
class ResourcePool:
    """Resource pool with limited capacity for isolation.

    Enforces max_concurrent limit across BOTH sync and async contexts.
    Uses a shared atomic counter protected by threading.Lock to prevent oversubscription.
    """

    max_concurrent: int = field(default=DEFAULT_BULKHEAD_MAX_CONCURRENT)
    max_queue_size: int = field(default=DEFAULT_BULKHEAD_MAX_QUEUE_SIZE)
    timeout: float = field(default=DEFAULT_BULKHEAD_TIMEOUT)

    # Internal state - shared atomic counter for true concurrency limit
    _active_count: int = field(default=0, init=False)
    _waiting_count: int = field(default=0, init=False)
    _counter_lock: threading.Lock = field(factory=threading.Lock, init=False)
    _sync_waiters: list[threading.Event] = field(factory=list, init=False)
    _async_waiters: list[asyncio.Event] = field(factory=list, init=False)

    def __attrs_post_init__(self) -> None:
        """Initialize internal state."""
        pass

    @property
    def active_count(self) -> int:
        """Number of currently active operations (across sync and async)."""
        with self._counter_lock:
            return self._active_count

    @property
    def available_capacity(self) -> int:
        """Number of available slots."""
        with self._counter_lock:
            return max(0, self.max_concurrent - self._active_count)

    @property
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
            self._sync_waiters.append(waiter)

        # Wait for signal from release
        try:
            if waiter.wait(timeout=actual_timeout):
                # Successfully signaled, we now have the slot
                return True
            # Timeout - remove from queue
            with self._counter_lock, contextlib.suppress(ValueError):
                self._sync_waiters.remove(waiter)
            return False
        finally:
            with self._counter_lock:
                self._waiting_count -= 1

    def release(self) -> None:
        """Release a resource slot."""
        self._release_and_signal()

    async def acquire_async(self, timeout: float | None = None) -> bool:
        """Acquire a resource slot (async).

        Args:
            timeout: Maximum time to wait (defaults to pool timeout)

        Returns:
            True if acquired, False if timeout

        Raises:
            RuntimeError: If queue is full
        """
        actual_timeout = timeout if timeout is not None else self.timeout

        # Try to acquire immediately using atomic counter access
        waiter = None
        acquired = await asyncio.to_thread(self._try_acquire_or_queue_async)
        if acquired is True:
            return True
        elif isinstance(acquired, asyncio.Event):
            waiter = acquired
        else:
            # Queue is full
            raise RuntimeError(f"Queue is full (max: {self.max_queue_size})")

        # Wait for signal from release
        try:
            await asyncio.wait_for(waiter.wait(), timeout=actual_timeout)
            # Successfully signaled, we now have the slot
            return True
        except TimeoutError:
            # Timeout - remove from queue
            await asyncio.to_thread(self._remove_async_waiter, waiter)
            return False
        finally:
            await asyncio.to_thread(self._decrement_waiting)

    def _try_acquire_or_queue_async(self) -> bool | asyncio.Event | None:
        """Helper for async acquire - returns True if acquired, Event if queued, None if queue full."""
        with self._counter_lock:
            if self._active_count < self.max_concurrent:
                self._active_count += 1
                return True

            # Check queue limit
            if self._waiting_count >= self.max_queue_size:
                return None  # Queue full

            # Add to wait queue
            self._waiting_count += 1
            waiter = asyncio.Event()
            self._async_waiters.append(waiter)
            return waiter

    def _remove_async_waiter(self, waiter: asyncio.Event) -> None:
        """Helper to remove async waiter from queue."""
        with self._counter_lock, contextlib.suppress(ValueError):
            self._async_waiters.remove(waiter)

    def _decrement_waiting(self) -> None:
        """Helper to decrement waiting count."""
        with self._counter_lock:
            self._waiting_count -= 1

    async def release_async(self) -> None:
        """Release a resource slot (async)."""
        await asyncio.to_thread(self._release_and_signal)

    def _release_and_signal(self) -> None:
        """Helper to release slot and signal next waiter atomically."""
        with self._counter_lock:
            if self._active_count > 0:
                self._active_count -= 1

            # Signal next waiter (prefer sync over async for fairness)
            if self._sync_waiters:
                sync_waiter = self._sync_waiters.pop(0)
                self._active_count += 1
                sync_waiter.set()
            elif self._async_waiters:
                async_waiter = self._async_waiters.pop(0)
                self._active_count += 1
                async_waiter.set()

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


@define(kw_only=True, slots=True)
class Bulkhead:
    """Bulkhead isolation pattern for protecting resources."""

    name: str
    pool: ResourcePool = field(factory=ResourcePool)

    def execute(self, func: Callable[..., T], *args: Any, **kwargs: Any) -> T:
        """Execute function with bulkhead protection (sync).

        Args:
            func: Function to execute
            *args: Function arguments
            **kwargs: Function keyword arguments

        Returns:
            Function result

        Raises:
            RuntimeError: If resource cannot be acquired
            Exception: Any exception from the protected function
        """
        if not self.pool.acquire():
            raise RuntimeError(f"Bulkhead '{self.name}' is at capacity")

        try:
            # Emit acquisition event
            self._emit_event("acquired")
            start_time = time.time()

            result = func(*args, **kwargs)

            # Emit success event
            execution_time = time.time() - start_time
            self._emit_event("completed", execution_time=execution_time)

            return result
        except Exception as e:
            # Emit failure event
            execution_time = time.time() - start_time
            self._emit_event("failed", error=str(e), execution_time=execution_time)
            raise
        finally:
            self.pool.release()
            self._emit_event("released")

    async def execute_async(self, func: Callable[..., Awaitable[T]], *args: Any, **kwargs: Any) -> T:
        """Execute async function with bulkhead protection.

        Args:
            func: Async function to execute
            *args: Function arguments
            **kwargs: Function keyword arguments

        Returns:
            Function result

        Raises:
            RuntimeError: If resource cannot be acquired
            Exception: Any exception from the protected function
        """
        if not await self.pool.acquire_async():
            raise RuntimeError(f"Bulkhead '{self.name}' is at capacity")

        try:
            # Emit acquisition event
            self._emit_event("acquired")
            start_time = time.time()

            result = await func(*args, **kwargs)

            # Emit success event
            execution_time = time.time() - start_time
            self._emit_event("completed", execution_time=execution_time)

            return result
        except Exception as e:
            # Emit failure event
            execution_time = time.time() - start_time
            self._emit_event("failed", error=str(e), execution_time=execution_time)
            raise
        finally:
            await self.pool.release_async()
            self._emit_event("released")

    def _emit_event(self, operation: str, **data: Any) -> None:
        """Emit bulkhead event."""
        try:
            from provide.foundation.hub.events import Event, get_event_bus

            get_event_bus().emit(
                Event(
                    name=f"bulkhead.{operation}",
                    data={
                        "bulkhead_name": self.name,
                        "pool_stats": self.pool.get_stats(),
                        **data,
                    },
                    source="bulkhead",
                )
            )
        except ImportError:
            # Events not available, continue without logging
            pass

    def get_status(self) -> dict[str, Any]:
        """Get bulkhead status."""
        return {
            "name": self.name,
            "pool": self.pool.get_stats(),
        }


class BulkheadManager:
    """Manager for multiple bulkheads with different resource pools."""

    def __init__(self) -> None:
        """Initialize bulkhead manager."""
        self._bulkheads: dict[str, Bulkhead] = {}
        self._lock = threading.RLock()

    def create_bulkhead(
        self,
        name: str,
        max_concurrent: int = 10,
        max_queue_size: int = 100,
        timeout: float = 30.0,
    ) -> Bulkhead:
        """Create or get a bulkhead.

        Args:
            name: Bulkhead name
            max_concurrent: Maximum concurrent operations
            max_queue_size: Maximum queue size
            timeout: Operation timeout

        Returns:
            Bulkhead instance
        """
        with self._lock:
            if name not in self._bulkheads:
                pool = ResourcePool(
                    max_concurrent=max_concurrent,
                    max_queue_size=max_queue_size,
                    timeout=timeout,
                )
                self._bulkheads[name] = Bulkhead(name=name, pool=pool)

            return self._bulkheads[name]

    def get_bulkhead(self, name: str) -> Bulkhead | None:
        """Get a bulkhead by name."""
        with self._lock:
            return self._bulkheads.get(name)

    def list_bulkheads(self) -> list[str]:
        """List all bulkhead names."""
        with self._lock:
            return list(self._bulkheads.keys())

    def get_all_status(self) -> dict[str, dict[str, Any]]:
        """Get status of all bulkheads."""
        with self._lock:
            return {name: bulkhead.get_status() for name, bulkhead in self._bulkheads.items()}

    def remove_bulkhead(self, name: str) -> bool:
        """Remove a bulkhead.

        Args:
            name: Bulkhead name

        Returns:
            True if removed, False if not found
        """
        with self._lock:
            if name in self._bulkheads:
                del self._bulkheads[name]
                return True
            return False


# Global bulkhead manager
_bulkhead_manager = BulkheadManager()


def get_bulkhead_manager() -> BulkheadManager:
    """Get the global bulkhead manager."""
    return _bulkhead_manager


__all__ = [
    "Bulkhead",
    "BulkheadManager",
    "ResourcePool",
    "get_bulkhead_manager",
]
