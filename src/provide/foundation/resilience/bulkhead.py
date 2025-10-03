from __future__ import annotations

import asyncio
from collections.abc import Awaitable, Callable
import threading
import time
from typing import Any, TypeVar

from attrs import define, field

from provide.foundation.concurrency.locks import DualLock

"""Bulkhead pattern for resource isolation and limiting.

The bulkhead pattern isolates resources to prevent failures in one part of
the system from cascading to other parts. It limits concurrent access to
resources and provides isolation boundaries.
"""

T = TypeVar("T")


@define(kw_only=True, slots=True)
class ResourcePool:
    """Resource pool with limited capacity for isolation."""

    max_concurrent: int = field(default=10)
    max_queue_size: int = field(default=100)
    timeout: float = field(default=30.0)  # seconds

    # Internal state
    _semaphore: threading.Semaphore = field(init=False)
    _async_semaphore: asyncio.Semaphore | None = field(default=None, init=False)
    _active_count: int = field(default=0, init=False)
    _queue_size: int = field(default=0, init=False)
    _lock: DualLock = field(factory=DualLock, init=False)

    def __attrs_post_init__(self) -> None:
        """Initialize semaphores after object creation."""
        self._semaphore = threading.Semaphore(self.max_concurrent)

    @property
    def active_count(self) -> int:
        """Number of currently active operations."""
        with self._lock.sync():
            return self._active_count

    @property
    def available_capacity(self) -> int:
        """Number of available slots."""
        with self._lock.sync():
            return self.max_concurrent - self._active_count

    @property
    def queue_size(self) -> int:
        """Current queue size."""
        with self._lock.sync():
            return self._queue_size

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

        with self._lock.sync():
            if self._queue_size >= self.max_queue_size:
                raise RuntimeError(f"Queue is full (max: {self.max_queue_size})")
            self._queue_size += 1

        try:
            acquired = self._semaphore.acquire(timeout=actual_timeout)
            if acquired:
                with self._lock.sync():
                    self._active_count += 1
            return acquired
        finally:
            with self._lock.sync():
                self._queue_size -= 1

    def release(self) -> None:
        """Release a resource slot."""
        with self._lock.sync():
            if self._active_count > 0:
                self._active_count -= 1
        self._semaphore.release()

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

        # Initialize async semaphore on first use
        if self._async_semaphore is None:
            self._async_semaphore = asyncio.Semaphore(self.max_concurrent)

        async with self._lock.async_():
            if self._queue_size >= self.max_queue_size:
                raise RuntimeError(f"Queue is full (max: {self.max_queue_size})")
            self._queue_size += 1

        try:
            acquired = await asyncio.wait_for(self._async_semaphore.acquire(), timeout=actual_timeout)
            if acquired:
                async with self._lock.async_():
                    self._active_count += 1
            return True
        except TimeoutError:
            return False
        finally:
            async with self._lock.async_():
                self._queue_size -= 1

    async def release_async(self) -> None:
        """Release a resource slot (async)."""
        async with self._lock.async_():
            if self._active_count > 0:
                self._active_count -= 1

        if self._async_semaphore is not None:
            self._async_semaphore.release()

    def get_stats(self) -> dict[str, Any]:
        """Get pool statistics."""
        with self._lock.sync():
            return {
                "max_concurrent": self.max_concurrent,
                "active_count": self._active_count,
                "available_capacity": self.max_concurrent - self._active_count,
                "queue_size": self._queue_size,
                "max_queue_size": self.max_queue_size,
                "utilization": self._active_count / self.max_concurrent,
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
