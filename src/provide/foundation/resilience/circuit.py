from __future__ import annotations

import asyncio
from collections.abc import Callable
from enum import Enum, auto
from functools import wraps
import threading
import time
from typing import Any

from provide.foundation.errors import FoundationError


class CircuitState(Enum):
    """Represents the state of the circuit breaker."""

    CLOSED = auto()
    OPEN = auto()
    HALF_OPEN = auto()


class CircuitBreaker:
    """Implements the Circuit Breaker pattern for resilience."""

    def __init__(
        self,
        failure_threshold: int = 5,
        recovery_timeout: float = 30.0,
        expected_exception: type[Exception] | tuple[type[Exception], ...] = Exception,
        time_source: Callable[[], float] | None = None,
    ) -> None:
        """Initialize the circuit breaker.

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
        self._sync_lock = threading.RLock()
        self._async_lock: asyncio.Lock | None = None
        self._async_init_lock = threading.Lock()
        # Initialize state attributes (will be set properly in reset())
        self._state: CircuitState
        self._failure_count: int
        self._last_failure_time: float | None
        self.reset()

    def _get_async_lock(self) -> asyncio.Lock:
        """Get or create the async lock (lazy initialization)."""
        if self._async_lock is None:
            with self._async_init_lock:
                if self._async_lock is None:
                    try:
                        self._async_lock = asyncio.Lock()
                    except RuntimeError:
                        # No event loop running, create without loop
                        loop = asyncio.new_event_loop()
                        asyncio.set_event_loop(loop)
                        self._async_lock = asyncio.Lock()
        return self._async_lock

    @property
    def state(self) -> CircuitState:
        """Get the current state of the circuit breaker."""
        with self._sync_lock:
            if self._state == CircuitState.OPEN and self._can_attempt_recovery():
                # This is a view of the state; the actual transition happens in call()
                return CircuitState.HALF_OPEN
            return self._state

    @property
    def failure_count(self) -> int:
        """Get the current failure count."""
        with self._sync_lock:
            return self._failure_count

    def _can_attempt_recovery(self) -> bool:
        """Check if the circuit can attempt recovery."""
        return self._time_source() >= (self._last_failure_time or 0) + self.recovery_timeout

    def call(self, func: Callable, *args: Any, **kwargs: Any) -> Any:
        """Execute a synchronous function through the circuit breaker."""
        with self._sync_lock:
            current_state = self.state
            if current_state == CircuitState.OPEN:
                raise RuntimeError("Circuit breaker is open")
            # If HALF_OPEN, we proceed with the call

        try:
            result = func(*args, **kwargs)
            self._on_success()
            return result
        except self.expected_exception as e:
            self._on_failure()
            raise e

    async def call_async(self, func: Callable, *args: Any, **kwargs: Any) -> Any:
        """Execute an asynchronous function through the circuit breaker."""
        async with self._get_async_lock():
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

    def _on_success(self) -> None:
        """Handle a successful call."""
        with self._sync_lock:
            # Success in either CLOSED or HALF_OPEN state resets the breaker.
            self._state = CircuitState.CLOSED
            self._failure_count = 0
            self._last_failure_time = None

    def _on_failure(self) -> None:
        """Handle a failed call."""
        with self._sync_lock:
            self._failure_count += 1
            if self._failure_count >= self.failure_threshold:
                # This transition happens for failures in CLOSED state
                # or for the single attempt in HALF_OPEN state.
                self._state = CircuitState.OPEN
                self._last_failure_time = self._time_source()

    def reset(self) -> None:
        """Reset the circuit breaker to its initial state."""
        with self._sync_lock:
            self._state = CircuitState.CLOSED
            self._failure_count = 0
            self._last_failure_time = None

    async def _on_success_async(self) -> None:
        """Handle a successful call (async version)."""
        async with self._get_async_lock():
            self._state = CircuitState.CLOSED
            self._failure_count = 0
            self._last_failure_time = None

    async def _on_failure_async(self) -> None:
        """Handle a failed call (async version)."""
        async with self._get_async_lock():
            self._failure_count += 1
            if self._failure_count >= self.failure_threshold:
                self._state = CircuitState.OPEN
                self._last_failure_time = self._time_source()


def circuit_breaker(
    failure_threshold: int = 5,
    recovery_timeout: float = 30.0,
    expected_exception: type[Exception] | tuple[type[Exception], ...] = FoundationError,
    time_source: Callable[[], float] | None = None,
) -> Callable:
    """A decorator to apply the circuit breaker pattern to a function.

    Args:
        failure_threshold: Number of failures before opening circuit
        recovery_timeout: Seconds to wait before attempting recovery
        expected_exception: Exception type(s) to catch
        time_source: Optional callable that returns current time (for testing).
                    Defaults to time.time() for production use.

    Returns:
        Decorated function with circuit breaker protection
    """
    breaker = CircuitBreaker(
        failure_threshold=failure_threshold,
        recovery_timeout=recovery_timeout,
        expected_exception=expected_exception,
        time_source=time_source,
    )

    def decorator(func: Callable) -> Callable:
        if asyncio.iscoroutinefunction(func):

            @wraps(func)
            async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
                return await breaker.call_async(func, *args, **kwargs)

            return async_wrapper
        else:

            @wraps(func)
            def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
                return breaker.call(func, *args, **kwargs)

            return sync_wrapper

    return decorator
