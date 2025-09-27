from __future__ import annotations

from enum import Enum, auto
import time
from typing import Any

from attrs import field, frozen

from provide.foundation.config.defaults import (
    DEFAULT_CIRCUIT_BREAKER_FAILURE_COUNT,
    DEFAULT_CIRCUIT_BREAKER_FAILURE_THRESHOLD,
    DEFAULT_CIRCUIT_BREAKER_LAST_FAILURE_TIME,
    DEFAULT_CIRCUIT_BREAKER_NEXT_ATTEMPT_TIME,
    DEFAULT_CIRCUIT_BREAKER_RECOVERY_TIMEOUT,
    DEFAULT_CIRCUIT_BREAKER_STATE,
)
from provide.foundation.state.base import ImmutableState, StateMachine, StateTransition

"""State transitions for Foundation components."""


class CircuitBreakerEvent(Enum):
    """Events that can trigger circuit breaker state transitions."""

    SUCCESS = auto()
    FAILURE = auto()
    TIMEOUT = auto()
    RESET = auto()


@frozen
class CircuitBreakerState(ImmutableState):
    """Immutable circuit breaker state."""

    state: str = field(default=DEFAULT_CIRCUIT_BREAKER_STATE)  # closed, open, half_open
    failure_count: int = field(default=DEFAULT_CIRCUIT_BREAKER_FAILURE_COUNT)
    last_failure_time: float | None = field(default=DEFAULT_CIRCUIT_BREAKER_LAST_FAILURE_TIME)
    next_attempt_time: float = field(default=DEFAULT_CIRCUIT_BREAKER_NEXT_ATTEMPT_TIME)
    failure_threshold: int = field(default=DEFAULT_CIRCUIT_BREAKER_FAILURE_THRESHOLD)
    recovery_timeout: float = field(default=DEFAULT_CIRCUIT_BREAKER_RECOVERY_TIMEOUT)

    def with_changes(self, **changes: Any) -> CircuitBreakerState:
        """Create a new state instance with the specified changes.

        Args:
            **changes: Field updates to apply

        Returns:
            New state instance with updated generation
        """
        # Increment generation for change tracking
        if "generation" not in changes:
            changes["generation"] = self.generation + 1

        # For attrs classes with slots, use attrs.evolve instead of __dict__
        import attrs

        return attrs.evolve(self, **changes)

    def is_closed(self) -> bool:
        """Check if circuit is closed (normal operation)."""
        return self.state == "closed"

    def is_open(self) -> bool:
        """Check if circuit is open (failing fast)."""
        return self.state == "open"

    def is_half_open(self) -> bool:
        """Check if circuit is half-open (testing recovery)."""
        return self.state == "half_open"

    def should_attempt_reset(self) -> bool:
        """Check if circuit should attempt reset."""
        if not self.is_open():
            return False
        current_time = time.time()
        return current_time >= self.next_attempt_time

    def record_success(self) -> CircuitBreakerState:
        """Record a successful operation."""
        if self.is_half_open():
            # Recovery successful - close circuit
            return self.with_changes(
                state="closed",
                failure_count=0,
                last_failure_time=None,
            )
        elif self.is_closed():
            # Already closed, just ensure failure count is reset
            return self.with_changes(failure_count=0, last_failure_time=None)
        else:
            # Open circuit - shouldn't reach here, but return unchanged
            return self

    def record_failure(self) -> CircuitBreakerState:
        """Record a failed operation."""
        current_time = time.time()
        new_failure_count = self.failure_count + 1

        if self.is_half_open():
            # Failed during recovery - go back to open
            return self.with_changes(
                state="open",
                failure_count=new_failure_count,
                last_failure_time=current_time,
                next_attempt_time=current_time + self.recovery_timeout,
            )
        elif self.is_closed():
            # Check if we should open the circuit
            if new_failure_count >= self.failure_threshold:
                return self.with_changes(
                    state="open",
                    failure_count=new_failure_count,
                    last_failure_time=current_time,
                    next_attempt_time=current_time + self.recovery_timeout,
                )
            else:
                # Stay closed but increment failure count
                return self.with_changes(
                    failure_count=new_failure_count,
                    last_failure_time=current_time,
                )
        else:
            # Already open - shouldn't reach here, but update failure info
            return self.with_changes(
                failure_count=new_failure_count,
                last_failure_time=current_time,
                next_attempt_time=current_time + self.recovery_timeout,
            )

    def attempt_reset(self) -> CircuitBreakerState:
        """Attempt to reset from open to half-open."""
        if self.is_open() and self.should_attempt_reset():
            return self.with_changes(state="half_open")
        return self

    def force_reset(self) -> CircuitBreakerState:
        """Force reset to closed state."""
        return self.with_changes(
            state="closed",
            failure_count=0,
            last_failure_time=None,
            next_attempt_time=0.0,
        )


class CircuitBreakerStateMachine(StateMachine[str, CircuitBreakerEvent]):
    """State machine for circuit breaker operations."""

    def __init__(
        self,
        failure_threshold: int = 5,
        recovery_timeout: float = 60.0,
    ) -> None:
        # Create initial state
        initial_state = CircuitBreakerState(
            failure_threshold=failure_threshold,
            recovery_timeout=recovery_timeout,
        )

        super().__init__(initial_state.state)

        # Store the circuit breaker state separately
        self._circuit_state = initial_state

        # Define state transitions
        self._setup_transitions()

    def _setup_transitions(self) -> None:
        """Set up all possible state transitions."""
        # closed state transitions
        self.add_transition(
            StateTransition(
                from_state="closed",
                event=CircuitBreakerEvent.FAILURE,
                to_state="closed",  # Will be updated by action if threshold reached
                action=self._handle_closed_failure,
            )
        )
        self.add_transition(
            StateTransition(
                from_state="closed",
                event=CircuitBreakerEvent.SUCCESS,
                to_state="closed",
                action=self._record_success,
            )
        )

        # open state transitions
        self.add_transition(
            StateTransition(
                from_state="open",
                event=CircuitBreakerEvent.TIMEOUT,
                to_state="half_open",
                guard=self._should_attempt_reset,
                action=self._attempt_reset,
            )
        )

        # half_open state transitions
        self.add_transition(
            StateTransition(
                from_state="half_open",
                event=CircuitBreakerEvent.SUCCESS,
                to_state="closed",
                action=self._record_success,
            )
        )
        self.add_transition(
            StateTransition(
                from_state="half_open",
                event=CircuitBreakerEvent.FAILURE,
                to_state="open",
                action=self._record_failure,
            )
        )

        # reset transitions
        for state in ["closed", "open", "half_open"]:
            self.add_transition(
                StateTransition(
                    from_state=state,
                    event=CircuitBreakerEvent.RESET,
                    to_state="closed",
                    action=self._force_reset,
                )
            )

    @property
    def circuit_state(self) -> CircuitBreakerState:
        """Get the current circuit breaker state."""
        return self._circuit_state

    def _should_attempt_reset(self) -> bool:
        """Guard: should circuit attempt reset?"""
        return self._circuit_state.should_attempt_reset()

    def _handle_closed_failure(self) -> None:
        """Action: handle failure in closed state - may open circuit."""
        old_state = self._circuit_state
        self._circuit_state = old_state.record_failure()

        # If circuit opened, update the state machine's current state manually
        if self._circuit_state.is_open():
            self._current_state = "open"

    def _record_failure(self) -> None:
        """Action: record a failure."""
        self._circuit_state = self._circuit_state.record_failure()

    def _record_success(self) -> None:
        """Action: record a success."""
        self._circuit_state = self._circuit_state.record_success()

    def _attempt_reset(self) -> None:
        """Action: attempt reset to half-open."""
        self._circuit_state = self._circuit_state.attempt_reset()

    def _force_reset(self) -> None:
        """Action: force reset to closed."""
        self._circuit_state = self._circuit_state.force_reset()

    def reset(self) -> None:
        """Reset the state machine to its initial state."""
        self.transition(CircuitBreakerEvent.RESET)
