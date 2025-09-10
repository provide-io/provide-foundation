"""
Circuit breaker implementation for preventing cascading failures.
"""

import asyncio
import time
from enum import Enum
from typing import Any, Callable, TypeVar

from attrs import define, field

from provide.foundation.logger import logger

T = TypeVar("T")


class CircuitState(Enum):
    """Circuit breaker states."""
    CLOSED = "closed"      # Normal operation
    OPEN = "open"          # Circuit is open, failing fast
    HALF_OPEN = "half_open"  # Testing if service has recovered


@define(kw_only=True, slots=True)
class CircuitBreaker:
    """Circuit breaker pattern for preventing cascading failures.
    
    Tracks failures and opens the circuit when threshold is exceeded.
    Periodically allows test requests to check if service has recovered.
    """
    
    failure_threshold: int = field(default=5)
    recovery_timeout: float = field(default=60.0)  # seconds
    expected_exception: tuple[type[Exception], ...] = field(
        factory=lambda: (Exception,)
    )
    
    # Internal state
    _state: CircuitState = field(default=CircuitState.CLOSED, init=False)
    _failure_count: int = field(default=0, init=False)
    _last_failure_time: float | None = field(default=None, init=False)
    _next_attempt_time: float = field(default=0.0, init=False)
    
    @property
    def state(self) -> CircuitState:
        """Current circuit breaker state."""
        return self._state
    
    @property
    def failure_count(self) -> int:
        """Current failure count."""
        return self._failure_count
    
    def _should_attempt_reset(self) -> bool:
        """Check if we should attempt to reset the circuit."""
        if self._state != CircuitState.OPEN:
            return False
        
        current_time = time.time()
        return current_time >= self._next_attempt_time
    
    def _record_success(self) -> None:
        """Record successful execution."""
        if self._state == CircuitState.HALF_OPEN:
            logger.info(
                "Circuit breaker recovered - closing circuit",
                state="half_open->closed",
                failure_count=self._failure_count
            )
        
        self._failure_count = 0
        self._last_failure_time = None
        self._state = CircuitState.CLOSED
    
    def _record_failure(self, exception: Exception) -> None:
        """Record failed execution."""
        self._failure_count += 1
        self._last_failure_time = time.time()
        
        if self._state == CircuitState.HALF_OPEN:
            # Failed during recovery attempt
            self._state = CircuitState.OPEN
            self._next_attempt_time = self._last_failure_time + self.recovery_timeout
            logger.warning(
                "Circuit breaker recovery failed - opening circuit",
                state="half_open->open",
                failure_count=self._failure_count,
                next_attempt_in=self.recovery_timeout
            )
        elif self._failure_count >= self.failure_threshold:
            # Threshold exceeded, open circuit
            self._state = CircuitState.OPEN
            self._next_attempt_time = self._last_failure_time + self.recovery_timeout
            logger.error(
                "Circuit breaker opened due to failures",
                state="closed->open", 
                failure_count=self._failure_count,
                failure_threshold=self.failure_threshold,
                next_attempt_in=self.recovery_timeout
            )
    
    def call(self, func: Callable[..., T], *args, **kwargs) -> T:
        """Execute function with circuit breaker protection (sync)."""
        # Check if circuit is open
        if self._state == CircuitState.OPEN:
            if self._should_attempt_reset():
                self._state = CircuitState.HALF_OPEN
                logger.info(
                    "Circuit breaker attempting recovery",
                    state="open->half_open",
                    failure_count=self._failure_count
                )
            else:
                raise RuntimeError(
                    f"Circuit breaker is open. Next attempt in "
                    f"{self._next_attempt_time - time.time():.1f} seconds"
                )
        
        try:
            result = func(*args, **kwargs)
            self._record_success()
            return result
        except Exception as e:
            if isinstance(e, self.expected_exception):
                self._record_failure(e)
            raise
    
    async def call_async(self, func: Callable[..., T], *args, **kwargs) -> T:
        """Execute async function with circuit breaker protection."""
        # Check if circuit is open
        if self._state == CircuitState.OPEN:
            if self._should_attempt_reset():
                self._state = CircuitState.HALF_OPEN
                logger.info(
                    "Circuit breaker attempting recovery",
                    state="open->half_open",
                    failure_count=self._failure_count
                )
            else:
                raise RuntimeError(
                    f"Circuit breaker is open. Next attempt in "
                    f"{self._next_attempt_time - time.time():.1f} seconds"
                )
        
        try:
            result = await func(*args, **kwargs)
            self._record_success()
            return result
        except Exception as e:
            if isinstance(e, self.expected_exception):
                self._record_failure(e)
            raise
    
    def reset(self) -> None:
        """Manually reset the circuit breaker."""
        logger.info(
            "Circuit breaker manually reset",
            previous_state=self._state.value,
            failure_count=self._failure_count
        )
        self._state = CircuitState.CLOSED
        self._failure_count = 0
        self._last_failure_time = None
        self._next_attempt_time = 0.0