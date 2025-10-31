#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from __future__ import annotations

from collections.abc import Generator
import contextlib
import threading
import time
from typing import Any

from attrs import define, field

from provide.foundation.errors.runtime import RuntimeError as FoundationRuntimeError

"""Centralized lock management to prevent deadlocks and coordinate thread safety.

This module provides a LockManager that enforces lock ordering and provides
timeout mechanisms to prevent deadlocks across the entire foundation.
"""


@define(slots=True)
class LockInfo:
    """Information about a registered lock."""

    name: str
    lock: threading.RLock
    order: int
    description: str = ""
    owner: str | None = field(default=None, init=False)
    acquired_at: float | None = field(default=None, init=False)


class LockManager:
    """Centralized lock manager to prevent deadlocks.

    Enforces lock ordering and provides timeout mechanisms.
    All locks must be acquired through this manager to prevent deadlocks.
    """

    def __init__(self) -> None:
        """Initialize lock manager."""
        self._locks: dict[str, LockInfo] = {}
        self._manager_lock = threading.RLock()
        self._thread_local = threading.local()

    def register_lock(
        self,
        name: str,
        order: int,
        description: str = "",
        lock: threading.RLock | None = None,
    ) -> threading.RLock:
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
        with self._manager_lock:
            if name in self._locks:
                raise ValueError(f"Lock '{name}' already registered")

            # Check for order conflicts
            for existing_name, lock_info in self._locks.items():
                if lock_info.order == order:
                    raise ValueError(
                        f"Lock order {order} already used by '{existing_name}'. "
                        f"Each lock must have a unique order."
                    )

            actual_lock = lock or threading.RLock()
            lock_info = LockInfo(name=name, lock=actual_lock, order=order, description=description)

            self._locks[name] = lock_info
            return actual_lock

    def get_lock(self, name: str) -> threading.RLock:
        """Get a registered lock by name.

        Args:
            name: Name of the lock

        Returns:
            The lock instance

        Raises:
            KeyError: If lock is not registered
        """
        with self._manager_lock:
            if name not in self._locks:
                raise KeyError(f"Lock '{name}' not registered")
            return self._locks[name].lock

    def _prepare_lock_acquisition(self, lock_names: tuple[str, ...]) -> list[LockInfo]:
        """Prepare locks for acquisition by sorting and validating order."""
        if not hasattr(self._thread_local, "lock_stack"):
            self._thread_local.lock_stack = []

        # Get lock infos and sort by order
        with self._manager_lock:
            lock_infos = []
            for name in lock_names:
                if name not in self._locks:
                    raise KeyError(f"Lock '{name}' not registered")
                lock_infos.append(self._locks[name])

        lock_infos.sort(key=lambda x: x.order)

        # Check for ordering violations, but allow re-entrant locks
        current_max_order = -1
        if self._thread_local.lock_stack:
            current_max_order = max(info.order for info in self._thread_local.lock_stack)

        for lock_info in lock_infos:
            # Allow re-acquiring the same lock (re-entrant behavior)
            if lock_info in self._thread_local.lock_stack:
                continue

            if lock_info.order <= current_max_order:
                raise FoundationRuntimeError(
                    f"Lock ordering violation: trying to acquire {lock_info.name} "
                    f"(order {lock_info.order}) after higher-order locks. "
                    f"Current max order: {current_max_order}"
                )

        return lock_infos

    def _acquire_lock_with_timeout(
        self, lock_info: LockInfo, remaining_timeout: float, blocking: bool
    ) -> None:
        """Acquire a single lock with timeout handling."""
        if remaining_timeout <= 0:
            raise TimeoutError(f"Timeout acquiring lock '{lock_info.name}'")

        acquired = lock_info.lock.acquire(blocking=blocking, timeout=remaining_timeout if blocking else 0)
        if not acquired:
            if blocking:
                raise TimeoutError(f"Timeout acquiring lock '{lock_info.name}'")
            else:
                raise FoundationRuntimeError(f"Could not acquire lock '{lock_info.name}' immediately")

        # Track acquisition
        lock_info.owner = threading.current_thread().name
        lock_info.acquired_at = time.time()

    def _release_acquired_locks(self, acquired_locks: list[LockInfo]) -> None:
        """Release all acquired locks in reverse order."""
        for lock_info in reversed(acquired_locks):
            try:
                lock_info.lock.release()
                lock_info.owner = None
                lock_info.acquired_at = None
                if lock_info in self._thread_local.lock_stack:
                    self._thread_local.lock_stack.remove(lock_info)
            except Exception:
                # Continue releasing other locks even if one fails
                pass

    @contextlib.contextmanager
    def acquire(
        self, *lock_names: str, timeout: float = 10.0, blocking: bool = True
    ) -> Generator[None, None, None]:
        """Acquire multiple locks in order to prevent deadlocks.

        Args:
            *lock_names: Names of locks to acquire
            timeout: Timeout in seconds
            blocking: Whether to block or raise immediately if locks unavailable

        Yields:
            None when all locks are acquired

        Raises:
            TimeoutError: If locks cannot be acquired within timeout
            RuntimeError: If deadlock would occur or other lock issues
        """
        if not lock_names:
            yield
            return

        lock_infos = self._prepare_lock_acquisition(lock_names)
        acquired_locks: list[LockInfo] = []
        start_time = time.time()

        try:
            for lock_info in lock_infos:
                # Skip locks already in stack (re-entrant behavior)
                if lock_info in self._thread_local.lock_stack:
                    continue

                remaining_timeout = timeout - (time.time() - start_time)
                self._acquire_lock_with_timeout(lock_info, remaining_timeout, blocking)

                acquired_locks.append(lock_info)
                self._thread_local.lock_stack.append(lock_info)

            yield

        finally:
            self._release_acquired_locks(acquired_locks)

    def get_lock_status(self) -> dict[str, dict[str, Any]]:
        """Get current status of all locks.

        Returns:
            Dictionary with lock status information
        """
        with self._manager_lock:
            status = {}
            for name, lock_info in self._locks.items():
                status[name] = {
                    "order": lock_info.order,
                    "description": lock_info.description,
                    "owner": lock_info.owner,
                    "acquired_at": lock_info.acquired_at,
                    "is_locked": lock_info.lock._is_owned() if hasattr(lock_info.lock, "_is_owned") else None,
                }
            return status

    def detect_potential_deadlocks(self) -> list[str]:
        """Detect potential deadlock situations.

        Returns:
            List of warnings about potential deadlocks
        """
        warnings = []

        # Check for lock ordering violations across threads
        # This is a simplified check - real deadlock detection is complex
        with self._manager_lock:
            for name, lock_info in self._locks.items():
                if lock_info.acquired_at and lock_info.owner:
                    hold_time = time.time() - lock_info.acquired_at
                    if hold_time > 30:  # 30 seconds is a long time to hold a lock
                        warnings.append(
                            f"Lock '{name}' held by {lock_info.owner} for {hold_time:.1f}s - "
                            f"potential deadlock or resource leak"
                        )

        return warnings


# Global lock manager instance
_lock_manager = LockManager()
_locks_registered = False
_registration_lock = threading.Lock()


def get_lock_manager() -> LockManager:
    """Get the global lock manager instance."""
    global _locks_registered
    with _registration_lock:
        if not _locks_registered:
            register_foundation_locks()
            _locks_registered = True
    return _lock_manager


def register_foundation_locks() -> None:
    """Register all foundation locks with proper ordering.

    Lock ordering hierarchy (LOWER numbers = MORE fundamental):
    - 0-99: Orchestration (coordinator, hub initialization)
    - 100-199: Early subsystems (logger - needed for debugging)
    - 200-299: Core infrastructure (config, registry, components)
    - 300+: Reserved for future subsystems
    """
    manager = _lock_manager

    # Orchestration (order 0-99) - most fundamental, acquired first
    manager.register_lock("foundation.hub.init", order=0, description="Hub initialization")
    manager.register_lock(
        "foundation.init.coordinator", order=10, description="Master initialization coordinator"
    )
    manager.register_lock("foundation.stream", order=20, description="Log stream management lock")

    # Early subsystems (order 100-199) - needed early for debugging
    manager.register_lock("foundation.logger.lazy", order=100, description="Lazy logger initialization")
    manager.register_lock("foundation.logger.setup", order=110, description="Logger setup coordination")

    # Core infrastructure (order 200-299)
    manager.register_lock("foundation.config", order=200, description="Configuration system lock")
    manager.register_lock("foundation.registry", order=210, description="Component registry lock")
    manager.register_lock("foundation.hub.components", order=220, description="Hub component management")


__all__ = ["LockInfo", "LockManager", "get_lock_manager", "register_foundation_locks"]

# 🧱🏗️🔚
