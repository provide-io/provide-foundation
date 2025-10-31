#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from __future__ import annotations

from collections.abc import Awaitable, Callable
import threading
import time
from typing import Any, TypeVar

from attrs import define, field

from provide.foundation.resilience.bulkhead_async import AsyncResourcePool
from provide.foundation.resilience.bulkhead_sync import SyncResourcePool

"""Bulkhead pattern for resource isolation and limiting.

The bulkhead pattern isolates resources to prevent failures in one part of
the system from cascading to other parts. It limits concurrent access to
resources and provides isolation boundaries.
"""

T = TypeVar("T")


@define(kw_only=True, slots=True)
class Bulkhead:
    """Bulkhead isolation pattern for protecting resources.

    Can use either SyncResourcePool or AsyncResourcePool depending on use case.
    """

    name: str
    pool: SyncResourcePool | AsyncResourcePool = field(factory=SyncResourcePool)

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
        # Must use SyncResourcePool for sync execution
        if not isinstance(self.pool, SyncResourcePool):
            raise TypeError("Sync execution requires SyncResourcePool")

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
        # Must use AsyncResourcePool for async execution
        if not isinstance(self.pool, AsyncResourcePool):
            raise TypeError("Async execution requires AsyncResourcePool")

        if not await self.pool.acquire():
            raise RuntimeError(f"Bulkhead '{self.name}' is at capacity")

        try:
            # Emit acquisition event
            await self._emit_event_async("acquired")
            start_time = time.time()

            result = await func(*args, **kwargs)

            # Emit success event
            execution_time = time.time() - start_time
            await self._emit_event_async("completed", execution_time=execution_time)

            return result
        except Exception as e:
            # Emit failure event
            execution_time = time.time() - start_time
            await self._emit_event_async("failed", error=str(e), execution_time=execution_time)
            raise
        finally:
            await self.pool.release()
            await self._emit_event_async("released")

    def _emit_event(self, operation: str, **data: Any) -> None:
        """Emit bulkhead event (sync)."""
        try:
            from provide.foundation.hub.events import Event, get_event_bus

            # Get pool stats synchronously
            pool_stats = self.pool.get_stats() if isinstance(self.pool, SyncResourcePool) else {}

            get_event_bus().emit(
                Event(
                    name=f"bulkhead.{operation}",
                    data={
                        "bulkhead_name": self.name,
                        "pool_stats": pool_stats,
                        **data,
                    },
                    source="bulkhead",
                )
            )
        except ImportError:
            # Events not available, continue without logging
            pass

    async def _emit_event_async(self, operation: str, **data: Any) -> None:
        """Emit bulkhead event (async)."""
        try:
            from provide.foundation.hub.events import Event, get_event_bus

            # Get pool stats asynchronously
            pool_stats = await self.pool.get_stats() if isinstance(self.pool, AsyncResourcePool) else {}

            get_event_bus().emit(
                Event(
                    name=f"bulkhead.{operation}",
                    data={
                        "bulkhead_name": self.name,
                        "pool_stats": pool_stats,
                        **data,
                    },
                    source="bulkhead",
                )
            )
        except ImportError:
            # Events not available, continue without logging
            pass

    def get_status(self) -> dict[str, Any]:
        """Get bulkhead status (sync only)."""
        if isinstance(self.pool, SyncResourcePool):
            return {
                "name": self.name,
                "pool": self.pool.get_stats(),
            }
        # Can't get async pool stats in sync context
        return {
            "name": self.name,
            "pool": {},
        }

    async def get_status_async(self) -> dict[str, Any]:
        """Get bulkhead status (async)."""
        if isinstance(self.pool, AsyncResourcePool):
            return {
                "name": self.name,
                "pool": await self.pool.get_stats(),
            }
        # Can get sync pool stats from async context via threading
        return {
            "name": self.name,
            "pool": self.pool.get_stats() if isinstance(self.pool, SyncResourcePool) else {},
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
        use_async_pool: bool = False,
    ) -> Bulkhead:
        """Create or get a bulkhead.

        Args:
            name: Bulkhead name
            max_concurrent: Maximum concurrent operations
            max_queue_size: Maximum queue size
            timeout: Operation timeout
            use_async_pool: If True, create AsyncResourcePool; otherwise SyncResourcePool

        Returns:
            Bulkhead instance
        """
        with self._lock:
            if name not in self._bulkheads:
                pool: SyncResourcePool | AsyncResourcePool
                if use_async_pool:
                    pool = AsyncResourcePool(
                        max_concurrent=max_concurrent,
                        max_queue_size=max_queue_size,
                        timeout=timeout,
                    )
                else:
                    pool = SyncResourcePool(
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
    "AsyncResourcePool",
    "Bulkhead",
    "BulkheadManager",
    "SyncResourcePool",
    "get_bulkhead_manager",
]

# 🧱🏗️🔚
