from __future__ import annotations

import contextlib
from collections.abc import Generator
import threading
import time
from typing import Any
import weakref

from attrs import define, field

from provide.foundation.errors.runtime import RuntimeError as FoundationRuntimeError

"""Centralized lock management to prevent deadlocks and coordinate thread safety.

This module provides a LockManager that enforces lock ordering and provides
timeout mechanisms to prevent deadlocks across the entire foundation.
"""


@define
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
            lock_info = LockInfo(
                name=name,
                lock=actual_lock,
                order=order,
                description=description
            )

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

    @contextlib.contextmanager
    def acquire(
        self,
        *lock_names: str,
        timeout: float = 10.0,
        blocking: bool = True
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

        # Get current thread's lock stack
        if not hasattr(self._thread_local, 'lock_stack'):
            self._thread_local.lock_stack = []

        # Sort locks by order to prevent deadlocks
        with self._manager_lock:
            lock_infos = []
            for name in lock_names:
                if name not in self._locks:
                    raise KeyError(f"Lock '{name}' not registered")
                lock_infos.append(self._locks[name])

        # Sort by order for consistent acquisition
        lock_infos.sort(key=lambda x: x.order)

        # Check for ordering violations with current thread's locks
        current_max_order = -1
        if self._thread_local.lock_stack:
            current_max_order = max(info.order for info in self._thread_local.lock_stack)

        for lock_info in lock_infos:
            if lock_info.order <= current_max_order:
                raise FoundationRuntimeError(
                    f"Lock ordering violation: trying to acquire {lock_info.name} "
                    f"(order {lock_info.order}) after higher-order locks. "
                    f"Current max order: {current_max_order}"
                )

        # Acquire locks in order
        acquired_locks: list[LockInfo] = []
        start_time = time.time()

        try:
            for lock_info in lock_infos:
                remaining_timeout = timeout - (time.time() - start_time)
                if remaining_timeout <= 0:
                    raise TimeoutError(f"Timeout acquiring locks: {[info.name for info in lock_infos]}")

                acquired = lock_info.lock.acquire(blocking=blocking, timeout=remaining_timeout if blocking else 0)
                if not acquired:
                    if blocking:
                        raise TimeoutError(f"Timeout acquiring lock '{lock_info.name}'")
                    else:
                        raise FoundationRuntimeError(f"Could not acquire lock '{lock_info.name}' immediately")

                # Track acquisition
                lock_info.owner = threading.current_thread().name
                lock_info.acquired_at = time.time()
                acquired_locks.append(lock_info)
                self._thread_local.lock_stack.append(lock_info)

            yield

        finally:
            # Release locks in reverse order
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
                    "is_locked": lock_info.lock._is_owned() if hasattr(lock_info.lock, '_is_owned') else None,
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


def get_lock_manager() -> LockManager:
    """Get the global lock manager instance."""
    return _lock_manager


def register_foundation_locks() -> None:
    """Register all foundation locks with proper ordering."""
    manager = get_lock_manager()

    # Register locks in order of dependency (lowest to highest)
    # Lower numbers are acquired first to prevent deadlocks

    # Core system locks (order 1-99)
    manager.register_lock(
        "foundation.config",
        order=10,
        description="Configuration system lock"
    )

    manager.register_lock(
        "foundation.registry",
        order=20,
        description="Component registry lock"
    )

    # Logger system locks (order 100-199)
    manager.register_lock(
        "foundation.logger.setup",
        order=100,
        description="Logger setup coordination"
    )

    manager.register_lock(
        "foundation.logger.lazy",
        order=110,
        description="Lazy logger initialization"
    )

    # Hub system locks (order 200-299)
    manager.register_lock(
        "foundation.hub.init",
        order=200,
        description="Hub initialization"
    )

    manager.register_lock(
        "foundation.hub.components",
        order=210,
        description="Hub component management"
    )


__all__ = ["LockInfo", "LockManager", "get_lock_manager", "register_foundation_locks"]