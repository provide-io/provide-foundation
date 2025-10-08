from __future__ import annotations

import asyncio
from collections.abc import Callable
import time
from typing import Any

from provide.foundation.resilience.circuit_sync import CircuitState

"""Asynchronous circuit breaker implementation."""


class AsyncCircuitBreaker:
    """Asynchronous circuit breaker for resilience patterns.

    Uses asyncio.Lock for async-safe state management.
    For synchronous code, use SyncCircuitBreaker instead.
    """

    def __init__(
        self,
        failure_threshold: int = 5,
        recovery_timeout: float = 30.0,
        expected_exception: type[Exception] | tuple[type[Exception], ...] = Exception,
        time_source: Callable[[], float] | None = None,
    ) -> None:
        """Initialize the asynchronous circuit breaker.

        Args:
            failure_threshold: Number of failures before opening circuit
            recovery_timeout: Seconds to wait before attempting recovery
            expected_exception: Exception type(s) to catch
            time_source: Optional callable that returns current time (for testing).
                        Defaults to time.time() for production use.
        """
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.expected_exception = expected_exception
        self._time_source = time_source or time.time
        self._lock: asyncio.Lock | None = None
        # Initialize state attributes (will be set properly in reset())
        self._state: CircuitState
        self._failure_count: int
        self._last_failure_time: float | None
        # Synchronously initialize the state
        self._state = CircuitState.CLOSED
        self._failure_count = 0
        self._last_failure_time = None

    def _get_lock(self) -> asyncio.Lock:
        """Get or create the async lock (lazy initialization)."""
        if self._lock is None:
            try:
                self._lock = asyncio.Lock()
            except RuntimeError:
                # No event loop running, create without loop
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                self._lock = asyncio.Lock()
        return self._lock

    async def get_state(self) -> CircuitState:
        """Get the current state of the circuit breaker.

        Returns:
            Current circuit state
        """
        async with self._get_lock():
            if self._state == CircuitState.OPEN and self._can_attempt_recovery():
                # This is a view of the state; the actual transition happens in call_async()
                return CircuitState.HALF_OPEN
            return self._state

    @property
    def state(self) -> CircuitState:
        """Get current state (synchronous property, may not reflect half-open state).

        Note: This property does not acquire the lock and returns the raw state.
        Use get_state() for the full state including half-open transitions.
        """
        return self._state

    async def get_failure_count(self) -> int:
        """Get the current failure count.

        Returns:
            Current failure count
        """
        async with self._get_lock():
            return self._failure_count

    @property
    def failure_count(self) -> int:
        """Get failure count (synchronous property).

        Note: This property does not acquire the lock. Use get_failure_count() for
        thread-safe access in async contexts.
        """
        return self._failure_count

    def _can_attempt_recovery(self) -> bool:
        """Check if the circuit can attempt recovery."""
        return self._time_source() >= (self._last_failure_time or 0) + self.recovery_timeout

    async def call_async(self, func: Callable, *args: Any, **kwargs: Any) -> Any:
        """Execute an asynchronous function through the circuit breaker.

        Args:
            func: Async callable to execute
            *args: Positional arguments for func
            **kwargs: Keyword arguments for func

        Returns:
            Result from func

        Raises:
            RuntimeError: If circuit is open
            Exception: Whatever exception func raises
        """
        async with self._get_lock():
            # Check state directly to avoid deadlock
            if self._state == CircuitState.OPEN and not self._can_attempt_recovery():
                raise RuntimeError("Circuit breaker is open")
            # If HALF_OPEN or recovery possible, we proceed with the call

        try:
            result = await func(*args, **kwargs)
            await self._on_success_async()
            return result
        except self.expected_exception as e:
            await self._on_failure_async()
            raise e

    async def _on_success_async(self) -> None:
        """Handle a successful call."""
        async with self._get_lock():
            # Success in either CLOSED or HALF_OPEN state resets the breaker.
            self._state = CircuitState.CLOSED
            self._failure_count = 0
            self._last_failure_time = None

    async def _on_failure_async(self) -> None:
        """Handle a failed call."""
        async with self._get_lock():
            self._failure_count += 1
            if self._failure_count >= self.failure_threshold:
                # This transition happens for failures in CLOSED state
                # or for the single attempt in HALF_OPEN state.
                self._state = CircuitState.OPEN
                self._last_failure_time = self._time_source()

    async def reset_async(self) -> None:
        """Reset the circuit breaker to its initial state (async version)."""
        async with self._get_lock():
            self._state = CircuitState.CLOSED
            self._failure_count = 0
            self._last_failure_time = None

    def reset(self) -> None:
        """Reset the circuit breaker to its initial state (sync version).

        Note: This is a convenience method that doesn't acquire the lock.
        For async contexts, use reset_async() instead.
        """
        self._state = CircuitState.CLOSED
        self._failure_count = 0
        self._last_failure_time = None
