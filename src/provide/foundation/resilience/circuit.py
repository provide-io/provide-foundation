from __future__ import annotations

from collections.abc import Awaitable, Callable
import time
from typing import Any, TypeVar

from attrs import define, field

from provide.foundation.resilience.types import CircuitState
from provide.foundation.state import (
    CircuitBreakerEvent,
    CircuitBreakerStateMachine,
)

"""Circuit breaker implementation using immutable state management."""

T = TypeVar("T")

# Global registry for all CircuitBreaker instances (for test reset)
_all_circuit_breakers: list["CircuitBreaker"] = []


@define(kw_only=True, slots=True)
class CircuitBreaker:
    """Circuit breaker pattern for preventing cascading failures.

    Uses immutable state management for thread-safe, predictable behavior.
    Tracks failures and opens the circuit when threshold is exceeded.
    Periodically allows test requests to check if service has recovered.
    """

    failure_threshold: int = field(default=5)
    recovery_timeout: float = field(default=60.0)  # seconds
    expected_exception: tuple[type[Exception], ...] = field(factory=lambda: (Exception,))

    # State machine for immutable state management
    _state_machine: CircuitBreakerStateMachine = field(init=False)

    def __attrs_post_init__(self) -> None:
        """Initialize state machine after attrs initialization."""
        object.__setattr__(
            self,
            "_state_machine",
            CircuitBreakerStateMachine(
                failure_threshold=self.failure_threshold,
                recovery_timeout=self.recovery_timeout,
            ),
        )

        # Register this instance for global reset during testing
        _all_circuit_breakers.append(self)

    @property
    def state(self) -> CircuitState:
        """Current circuit breaker state."""
        circuit_state = self._state_machine.circuit_state
        if circuit_state.is_closed():
            return CircuitState.CLOSED
        elif circuit_state.is_open():
            return CircuitState.OPEN
        else:
            return CircuitState.HALF_OPEN

    @property
    def failure_count(self) -> int:
        """Current failure count."""
        return self._state_machine.circuit_state.failure_count

    def _emit_event(self, name: str, data: dict[str, Any]) -> None:
        """Emit circuit breaker event."""
        try:
            from provide.foundation.hub.events import Event, get_event_bus

            get_event_bus().emit(
                Event(
                    name=name,
                    data=data,
                    source="circuit_breaker",
                )
            )
        except ImportError:
            # Event system not available, skip
            pass

    def _check_and_transition_state(self) -> None:
        """Check if state should transition and handle it."""
        circuit_state = self._state_machine.circuit_state

        if (
            circuit_state.is_open()
            and circuit_state.should_attempt_reset()
            and self._state_machine.transition(CircuitBreakerEvent.TIMEOUT)
        ):
            self._emit_event(
                "circuit_breaker.attempting_recovery",
                {
                    "state": "open->half_open",
                    "failure_count": circuit_state.failure_count,
                },
            )

    def call(self, func: Callable[..., T], *args: Any, **kwargs: Any) -> T:
        """Execute function with circuit breaker protection (sync)."""
        self._check_and_transition_state()

        circuit_state = self._state_machine.circuit_state
        if circuit_state.is_open():
            raise RuntimeError(
                f"Circuit breaker is open. Next attempt in "
                f"{circuit_state.next_attempt_time - time.time():.1f} seconds"
            )

        try:
            result = func(*args, **kwargs)
            self._record_success()
            return result
        except Exception as e:
            if isinstance(e, self.expected_exception):
                self._record_failure()
            raise

    async def call_async(self, func: Callable[..., Awaitable[T]], *args: Any, **kwargs: Any) -> T:
        """Execute async function with circuit breaker protection."""
        self._check_and_transition_state()

        circuit_state = self._state_machine.circuit_state
        if circuit_state.is_open():
            raise RuntimeError(
                f"Circuit breaker is open. Next attempt in "
                f"{circuit_state.next_attempt_time - time.time():.1f} seconds"
            )

        try:
            result = await func(*args, **kwargs)
            self._record_success()
            return result
        except Exception as e:
            if isinstance(e, self.expected_exception):
                self._record_failure()
            raise

    def _record_success(self) -> None:
        """Record successful execution."""
        old_state = self._state_machine.circuit_state
        if self._state_machine.transition(CircuitBreakerEvent.SUCCESS):
            new_state = self._state_machine.circuit_state

            if old_state.is_half_open() and new_state.is_closed():
                self._emit_event(
                    "circuit_breaker.recovered",
                    {
                        "state": "half_open->closed",
                        "failure_count": old_state.failure_count,
                    },
                )

    def _record_failure(self) -> None:
        """Record failed execution."""
        old_state = self._state_machine.circuit_state
        if self._state_machine.transition(CircuitBreakerEvent.FAILURE):
            new_state = self._state_machine.circuit_state

            if old_state.is_half_open() and new_state.is_open():
                self._emit_event(
                    "circuit_breaker.recovery_failed",
                    {
                        "state": "half_open->open",
                        "failure_count": new_state.failure_count,
                        "next_attempt_in": self.recovery_timeout,
                    },
                )
            elif old_state.is_closed() and new_state.is_open():
                self._emit_event(
                    "circuit_breaker.opened",
                    {
                        "state": "closed->open",
                        "failure_count": new_state.failure_count,
                        "failure_threshold": self.failure_threshold,
                        "next_attempt_in": self.recovery_timeout,
                    },
                )

    def reset(self) -> None:
        """Manually reset the circuit breaker."""
        old_state = self._state_machine.circuit_state
        if self._state_machine.transition(CircuitBreakerEvent.RESET):
            self._emit_event(
                "circuit_breaker.reset",
                {
                    "state": f"{old_state.state}->closed",
                    "previous_failure_count": old_state.failure_count,
                },
            )


def reset_all_circuit_breakers_for_testing() -> None:
    """Reset all CircuitBreaker instances to default state for testing.

    This function resets all CircuitBreaker instances that have been created,
    whether through decorators or direct instantiation, ensuring proper
    test isolation.
    """
    for breaker in _all_circuit_breakers:
        breaker.reset()


def clear_circuit_breaker_registry_for_testing() -> None:
    """Clear the global circuit breaker registry for testing.

    This should only be called during test cleanup to prevent
    memory leaks in long-running test suites.
    """
    _all_circuit_breakers.clear()
