#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from __future__ import annotations

import asyncio
from collections.abc import AsyncGenerator
import contextlib
import threading
import time
from typing import Any

from attrs import define, field

from provide.foundation.errors.runtime import RuntimeError as FoundationRuntimeError

"""Async-native centralized lock management for asyncio applications.

This module provides AsyncLockManager that enforces lock ordering and provides
timeout mechanisms for async code without blocking the event loop.
"""


@define(slots=True)
class AsyncLockInfo:
    """Information about a registered async lock."""

    name: str
    lock: asyncio.Lock
    order: int
    description: str = ""
    owner: str | None = field(default=None, init=False)
    acquired_at: float | None = field(default=None, init=False)


class AsyncLockManager:
    """Async-native centralized lock manager to prevent deadlocks.

    Enforces lock ordering and provides timeout mechanisms for async code.
    All async locks should be acquired through this manager to prevent deadlocks.
    """

    def __init__(self) -> None:
        """Initialize async lock manager."""
        self._locks: dict[str, AsyncLockInfo] = {}
        self._manager_lock = asyncio.Lock()
        self._task_local: dict[asyncio.Task[Any], list[AsyncLockInfo]] = {}

    async def register_lock(
        self,
        name: str,
        order: int,
        description: str = "",
        lock: asyncio.Lock | None = None,
    ) -> asyncio.Lock:
        """Register a lock with the manager.

        Args:
            name: Unique name for the lock
            order: Order number for deadlock prevention (acquire in ascending order)
            description: Human-readable description
            lock: Existing lock to register, or None to create new one

        Returns:
            The registered lock

        Raises:
            ValueError: If lock name already exists or order conflicts
        """
        async with self._manager_lock:
            if name in self._locks:
                raise ValueError(f"Lock '{name}' already registered")

            # Check for order conflicts
            for existing_name, lock_info in self._locks.items():
                if lock_info.order == order:
                    raise ValueError(
                        f"Lock order {order} already used by '{existing_name}'. "
                        f"Each lock must have a unique order."
                    )

            actual_lock = lock or asyncio.Lock()
            lock_info = AsyncLockInfo(name=name, lock=actual_lock, order=order, description=description)

            self._locks[name] = lock_info
            return actual_lock

    async def get_lock(self, name: str) -> asyncio.Lock:
        """Get a registered lock by name.

        Args:
            name: Name of the lock

        Returns:
            The lock instance

        Raises:
            KeyError: If lock is not registered
        """
        async with self._manager_lock:
            if name not in self._locks:
                raise KeyError(f"Lock '{name}' not registered")
            return self._locks[name].lock

    async def _prepare_lock_acquisition(self, lock_names: tuple[str, ...]) -> list[AsyncLockInfo]:
        """Prepare locks for acquisition by sorting and validating order."""
        try:
            current_task = asyncio.current_task()
        except RuntimeError:
            current_task = None

        if current_task and current_task not in self._task_local:
            self._task_local[current_task] = []

        # Get lock infos and sort by order
        async with self._manager_lock:
            lock_infos = []
            for name in lock_names:
                if name not in self._locks:
                    raise KeyError(f"Lock '{name}' not registered")
                lock_infos.append(self._locks[name])

        lock_infos.sort(key=lambda x: x.order)

        # Check for ordering violations
        current_max_order = -1
        if current_task and self._task_local.get(current_task):
            current_max_order = max(info.order for info in self._task_local[current_task])

        for lock_info in lock_infos:
            # Allow re-acquiring the same lock
            if current_task and lock_info in self._task_local.get(current_task, []):
                continue

            if lock_info.order <= current_max_order:
                raise FoundationRuntimeError(
                    f"Lock ordering violation: trying to acquire {lock_info.name} "
                    f"(order {lock_info.order}) after higher-order locks. "
                    f"Current max order: {current_max_order}"
                )

        return lock_infos

    async def _acquire_lock_with_timeout(self, lock_info: AsyncLockInfo, remaining_timeout: float) -> None:
        """Acquire a single lock with timeout handling."""
        if remaining_timeout <= 0:
            raise TimeoutError(f"Timeout acquiring lock '{lock_info.name}'")

        try:
            await asyncio.wait_for(lock_info.lock.acquire(), timeout=remaining_timeout)
        except TimeoutError as e:
            raise TimeoutError(f"Timeout acquiring lock '{lock_info.name}'") from e

        # Track acquisition
        try:
            current_task = asyncio.current_task()
            if current_task:
                lock_info.owner = current_task.get_name()
        except RuntimeError:
            lock_info.owner = "unknown"
        lock_info.acquired_at = time.time()

    async def _release_acquired_locks(self, acquired_locks: list[AsyncLockInfo]) -> None:
        """Release all acquired locks in reverse order."""
        try:
            current_task = asyncio.current_task()
        except RuntimeError:
            current_task = None

        for lock_info in reversed(acquired_locks):
            try:
                lock_info.lock.release()
                lock_info.owner = None
                lock_info.acquired_at = None
                if (
                    current_task
                    and current_task in self._task_local
                    and lock_info in self._task_local[current_task]
                ):
                    self._task_local[current_task].remove(lock_info)
                    # Clean up empty task entries to prevent memory leak
                    if not self._task_local[current_task]:
                        del self._task_local[current_task]
            except Exception:
                # Continue releasing other locks even if one fails
                pass

    @contextlib.asynccontextmanager
    async def acquire(self, *lock_names: str, timeout: float = 10.0) -> AsyncGenerator[None, None]:
        """Acquire multiple locks in order to prevent deadlocks.

        Args:
            *lock_names: Names of locks to acquire
            timeout: Timeout in seconds

        Yields:
            None when all locks are acquired

        Raises:
            TimeoutError: If locks cannot be acquired within timeout
            RuntimeError: If deadlock would occur or other lock issues
        """
        if not lock_names:
            yield
            return

        lock_infos = await self._prepare_lock_acquisition(lock_names)
        acquired_locks: list[AsyncLockInfo] = []
        start_time = time.time()

        try:
            current_task = asyncio.current_task()
        except RuntimeError:
            current_task = None

        try:
            for lock_info in lock_infos:
                # Skip locks already in stack
                if current_task and lock_info in self._task_local.get(current_task, []):
                    continue

                remaining_timeout = timeout - (time.time() - start_time)
                await self._acquire_lock_with_timeout(lock_info, remaining_timeout)

                acquired_locks.append(lock_info)
                if current_task:
                    if current_task not in self._task_local:
                        self._task_local[current_task] = []
                    self._task_local[current_task].append(lock_info)

            yield

        finally:
            await self._release_acquired_locks(acquired_locks)

    async def get_lock_status(self) -> dict[str, dict[str, Any]]:
        """Get current status of all locks.

        Returns:
            Dictionary with lock status information
        """
        async with self._manager_lock:
            status = {}
            for name, lock_info in self._locks.items():
                status[name] = {
                    "order": lock_info.order,
                    "description": lock_info.description,
                    "owner": lock_info.owner,
                    "acquired_at": lock_info.acquired_at,
                    "is_locked": lock_info.lock.locked(),
                }
            return status

    async def detect_potential_deadlocks(self) -> list[str]:
        """Detect potential deadlock situations.

        Returns:
            List of warnings about potential deadlocks
        """
        warnings = []

        async with self._manager_lock:
            for name, lock_info in self._locks.items():
                if lock_info.acquired_at and lock_info.owner:
                    hold_time = time.time() - lock_info.acquired_at
                    if hold_time > 30:  # 30 seconds is a long time to hold a lock
                        warnings.append(
                            f"Lock '{name}' held by {lock_info.owner} for {hold_time:.1f}s - "
                            f"potential deadlock or resource leak"
                        )

        return warnings


# Global async lock manager instance
_async_lock_manager: AsyncLockManager | None = None
_async_locks_registered = False
_async_locks_registration_event: threading.Event | None = None  # Thread-safe, loop-agnostic
_async_locks_registration_lock = threading.Lock()  # Thread-safe state machine coordination


async def get_async_lock_manager() -> AsyncLockManager:
    """Get the global async lock manager instance."""
    global _async_lock_manager, _async_locks_registered, _async_locks_registration_event

    if _async_lock_manager is None:
        _async_lock_manager = AsyncLockManager()

    # Fast path: registration already complete
    if _async_locks_registered:
        return _async_lock_manager

    # Coordinate registration with threading lock for state machine
    with _async_locks_registration_lock:
        # Re-check after acquiring lock (another task may have completed it)
        if _async_locks_registered:
            return _async_lock_manager

        # If registration is in progress by another task, get the event
        if _async_locks_registration_event is not None:
            event = _async_locks_registration_event
        else:
            # This task will perform registration - create threading.Event (loop-agnostic)
            _async_locks_registration_event = threading.Event()
            event = None

    # If we're waiting for another task/thread's registration
    if event is not None:
        # Wait on threading.Event in async-friendly way (works across event loops)
        # Use to_thread to avoid blocking the event loop
        await asyncio.to_thread(event.wait)

        # After waking, check if registration succeeded
        if _async_locks_registered:
            return _async_lock_manager
        # Registration failed, retry
        return await get_async_lock_manager()

    # This task performs registration
    try:
        await register_foundation_async_locks()
        _async_locks_registered = True
    except BaseException:
        # Clean up partial registration on failure
        if _async_lock_manager is not None:
            _async_lock_manager._locks.clear()
        raise
    finally:
        # Always unblock waiting tasks/threads and clear event
        if _async_locks_registration_event is not None:
            _async_locks_registration_event.set()
        _async_locks_registration_event = None

    return _async_lock_manager


async def register_foundation_async_locks() -> None:
    """Register all foundation async locks with proper ordering.

    Lock ordering hierarchy (LOWER numbers = MORE fundamental):
    - 0-99: Orchestration (coordinator, hub initialization)
    - 100-199: Early subsystems (logger - needed for debugging)
    - 200-299: Core infrastructure (config, registry, components)
    - 300+: Reserved for future subsystems
    """
    global _async_lock_manager

    # Use global directly - manager is guaranteed to exist because
    # get_async_lock_manager() creates it before calling this function
    if _async_lock_manager is None:
        raise RuntimeError("AsyncLockManager not initialized. Call get_async_lock_manager() first.")

    manager = _async_lock_manager

    # Orchestration (order 0-99) - most fundamental, acquired first
    await manager.register_lock("foundation.async.hub.init", order=0, description="Async hub initialization")
    await manager.register_lock(
        "foundation.async.init.coordinator", order=10, description="Async initialization coordinator"
    )
    await manager.register_lock("foundation.async.stream", order=20, description="Async log stream management")

    # Early subsystems (order 100-199) - needed early for debugging
    await manager.register_lock(
        "foundation.async.logger.lazy", order=100, description="Async lazy logger initialization"
    )
    await manager.register_lock(
        "foundation.async.logger.setup", order=110, description="Async logger setup coordination"
    )

    # Core infrastructure (order 200-299)
    await manager.register_lock("foundation.async.config", order=200, description="Async configuration system")
    await manager.register_lock("foundation.async.registry", order=210, description="Async component registry")
    await manager.register_lock(
        "foundation.async.hub.components", order=220, description="Async hub component management"
    )


__all__ = ["AsyncLockInfo", "AsyncLockManager", "get_async_lock_manager", "register_foundation_async_locks"]

# 🧱🏗️🔚
