from __future__ import annotations

import time
from enum import Enum, auto

from attrs import define, field, frozen

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

    state: str = field(default="CLOSED")  # CLOSED, OPEN, HALF_OPEN
    failure_count: int = field(default=0)
    last_failure_time: float | None = field(default=None)
    next_attempt_time: float = field(default=0.0)
    failure_threshold: int = field(default=5)
    recovery_timeout: float = field(default=60.0)

    def is_closed(self) -> bool:
        """Check if circuit is closed (normal operation)."""
        return self.state == "CLOSED"

    def is_open(self) -> bool:
        """Check if circuit is open (failing fast)."""
        return self.state == "OPEN"

    def is_half_open(self) -> bool:
        """Check if circuit is half-open (testing recovery)."""
        return self.state == "HALF_OPEN"

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
                state="CLOSED",
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
                state="OPEN",
                failure_count=new_failure_count,
                last_failure_time=current_time,
                next_attempt_time=current_time + self.recovery_timeout,
            )
        elif self.is_closed():
            # Check if we should open the circuit
            if new_failure_count >= self.failure_threshold:
                return self.with_changes(
                    state="OPEN",
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
            return self.with_changes(state="HALF_OPEN")
        return self

    def force_reset(self) -> CircuitBreakerState:
        """Force reset to closed state."""
        return self.with_changes(
            state="CLOSED",
            failure_count=0,
            last_failure_time=None,
            next_attempt_time=0.0,
        )


@define(kw_only=True, slots=True)
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
        # CLOSED -> OPEN (on threshold failures)
        self.add_transition(
            StateTransition(
                from_state="CLOSED",
                event=CircuitBreakerEvent.FAILURE,
                to_state="OPEN",
                guard=self._should_open_on_failure,
                action=self._record_failure,
            )
        )

        # CLOSED -> CLOSED (on failure below threshold)
        self.add_transition(
            StateTransition(
                from_state="CLOSED",
                event=CircuitBreakerEvent.FAILURE,
                to_state="CLOSED",
                guard=self._should_stay_closed_on_failure,
                action=self._record_failure,
            )
        )

        # CLOSED -> CLOSED (on success)
        self.add_transition(
            StateTransition(
                from_state="CLOSED",
                event=CircuitBreakerEvent.SUCCESS,
                to_state="CLOSED",
                action=self._record_success,
            )
        )

        # OPEN -> HALF_OPEN (on timeout)
        self.add_transition(
            StateTransition(
                from_state="OPEN",
                event=CircuitBreakerEvent.TIMEOUT,
                to_state="HALF_OPEN",
                guard=self._should_attempt_reset,
                action=self._attempt_reset,
            )
        )

        # HALF_OPEN -> CLOSED (on success)
        self.add_transition(
            StateTransition(
                from_state="HALF_OPEN",
                event=CircuitBreakerEvent.SUCCESS,
                to_state="CLOSED",
                action=self._record_success,
            )
        )

        # HALF_OPEN -> OPEN (on failure)
        self.add_transition(
            StateTransition(
                from_state="HALF_OPEN",
                event=CircuitBreakerEvent.FAILURE,
                to_state="OPEN",
                action=self._record_failure,
            )
        )

        # Any state -> CLOSED (on reset)
        for state in ["CLOSED", "OPEN", "HALF_OPEN"]:
            self.add_transition(
                StateTransition(
                    from_state=state,
                    event=CircuitBreakerEvent.RESET,
                    to_state="CLOSED",
                    action=self._force_reset,
                )
            )

    @property
    def circuit_state(self) -> CircuitBreakerState:
        """Get the current circuit breaker state."""
        return self._circuit_state

    def _should_open_on_failure(self) -> bool:
        """Guard: should circuit open on this failure?"""
        return self._circuit_state.failure_count + 1 >= self._circuit_state.failure_threshold

    def _should_stay_closed_on_failure(self) -> bool:
        """Guard: should circuit stay closed on this failure?"""
        return self._circuit_state.failure_count + 1 < self._circuit_state.failure_threshold

    def _should_attempt_reset(self) -> bool:
        """Guard: should circuit attempt reset?"""
        return self._circuit_state.should_attempt_reset()

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
