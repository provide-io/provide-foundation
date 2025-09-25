from __future__ import annotations

import asyncio
from collections.abc import Callable
from enum import Enum, auto
from functools import wraps
from threading import RLock
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
    ) -> None:
        """Initialize the circuit breaker."""
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.expected_exception = expected_exception
        self._lock = RLock()
        self.reset()

    @property
    def state(self) -> CircuitState:
        """Get the current state of the circuit breaker."""
        with self._lock:
            if self._state == CircuitState.OPEN and self._can_attempt_recovery():
                # This is a view of the state; the actual transition happens in call()
                return CircuitState.HALF_OPEN
            return self._state

    @property
    def failure_count(self) -> int:
        """Get the current failure count."""
        with self._lock:
            return self._failure_count

    def _can_attempt_recovery(self) -> bool:
        """Check if the circuit can attempt recovery."""
        return time.time() >= (self._last_failure_time or 0) + self.recovery_timeout

    def call(self, func: Callable, *args: Any, **kwargs: Any) -> Any:
        """Execute a synchronous function through the circuit breaker."""
        with self._lock:
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
        with self._lock:
            current_state = self.state
            if current_state == CircuitState.OPEN:
                raise RuntimeError("Circuit breaker is open")
            # If HALF_OPEN, we proceed with the call

        try:
            result = await func(*args, **kwargs)
            self._on_success()
            return result
        except self.expected_exception as e:
            self._on_failure()
            raise e

    def _on_success(self) -> None:
        """Handle a successful call."""
        with self._lock:
            # Success in either CLOSED or HALF_OPEN state resets the breaker.
            self.reset()

    def _on_failure(self) -> None:
        """Handle a failed call."""
        with self._lock:
            self._failure_count += 1
            if self._failure_count >= self.failure_threshold:
                # This transition happens for failures in CLOSED state
                # or for the single attempt in HALF_OPEN state.
                self._state = CircuitState.OPEN
                self._last_failure_time = time.time()

    def reset(self) -> None:
        """Reset the circuit breaker to its initial state."""
        with self._lock:
            self._state = CircuitState.CLOSED
            self._failure_count = 0
            self._last_failure_time: float | None = None


def circuit_breaker(
    failure_threshold: int = 5,
    recovery_timeout: float = 30.0,
    expected_exception: type[Exception] | tuple[type[Exception], ...] = FoundationError,
) -> Callable:
    """A decorator to apply the circuit breaker pattern to a function."""
    breaker = CircuitBreaker(
        failure_threshold=failure_threshold,
        recovery_timeout=recovery_timeout,
        expected_exception=expected_exception,
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
