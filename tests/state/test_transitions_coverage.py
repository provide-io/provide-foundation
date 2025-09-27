"""Additional tests for state transitions to improve coverage."""

from __future__ import annotations

from typing import TYPE_CHECKING

from provide.testkit import FoundationTestCase

from provide.foundation.state._internal.transitions import (
    CircuitBreakerEvent,
    CircuitBreakerState,
    CircuitBreakerStateMachine,
)

if TYPE_CHECKING:
    from provide.testkit.time.fixtures import TimeMachine


class TestCircuitBreakerStateEdgeCases(FoundationTestCase):
    """Test edge cases in CircuitBreakerState."""

    def test_circuit_breaker_state_creation_with_defaults(self) -> None:
        """Test CircuitBreakerState creation with default values."""
        state = CircuitBreakerState()
        assert state.state == "closed"  # Default from defaults module
        assert state.failure_count == 0  # Default from defaults module
        assert state.last_failure_time is None  # Default from defaults module
        assert state.next_attempt_time == 0.0  # Default from defaults module
        assert state.failure_threshold == 5  # Default from defaults module
        assert state.recovery_timeout == 60.0  # Default from defaults module

    def test_circuit_breaker_state_creation_with_custom_values(self) -> None:
        """Test CircuitBreakerState creation with custom values."""
        state = CircuitBreakerState(
            state="open",
            failure_count=3,
            last_failure_time=123.456,
            next_attempt_time=789.012,
            failure_threshold=10,
            recovery_timeout=120.0,
        )
        assert state.state == "open"
        assert state.failure_count == 3
        assert state.last_failure_time == 123.456
        assert state.next_attempt_time == 789.012
        assert state.failure_threshold == 10
        assert state.recovery_timeout == 120.0

    def test_with_changes_increments_generation(self) -> None:
        """Test that with_changes increments generation automatically."""
        state = CircuitBreakerState()
        initial_generation = state.generation

        new_state = state.with_changes(failure_count=5)
        assert new_state.generation == initial_generation + 1
        assert new_state.failure_count == 5

    def test_with_changes_explicit_generation(self) -> None:
        """Test that explicit generation in with_changes is respected."""
        state = CircuitBreakerState()

        new_state = state.with_changes(failure_count=5, generation=99)
        assert new_state.generation == 99
        assert new_state.failure_count == 5

    def test_state_check_methods(self) -> None:
        """Test state check methods for all states."""
        # Test closed state
        closed_state = CircuitBreakerState(state="closed")
        assert closed_state.is_closed()
        assert not closed_state.is_open()
        assert not closed_state.is_half_open()

        # Test open state
        open_state = CircuitBreakerState(state="open")
        assert not open_state.is_closed()
        assert open_state.is_open()
        assert not open_state.is_half_open()

        # Test half_open state
        half_open_state = CircuitBreakerState(state="half_open")
        assert not half_open_state.is_closed()
        assert not half_open_state.is_open()
        assert half_open_state.is_half_open()

    def test_should_attempt_reset_conditions(self, time_machine: TimeMachine) -> None:
        """Test should_attempt_reset under various conditions."""
        current_time = 1000.0  # Fixed time for test
        time_machine.freeze(current_time)

        # Closed state - should not attempt reset
        closed_state = CircuitBreakerState(state="closed")
        assert not closed_state.should_attempt_reset()

        # Half-open state - should not attempt reset
        half_open_state = CircuitBreakerState(state="half_open")
        assert not half_open_state.should_attempt_reset()

        # Open state - time not yet reached
        open_state_not_ready = CircuitBreakerState(state="open", next_attempt_time=current_time + 100)
        assert not open_state_not_ready.should_attempt_reset()

        # Open state - time has passed
        open_state_ready = CircuitBreakerState(state="open", next_attempt_time=current_time - 1)
        assert open_state_ready.should_attempt_reset()

    def test_record_success_from_different_states(self) -> None:
        """Test record_success behavior from different states."""
        # From half-open state - should close circuit
        half_open_state = CircuitBreakerState(state="half_open", failure_count=3, last_failure_time=123.456)
        new_state = half_open_state.record_success()
        assert new_state.is_closed()
        assert new_state.failure_count == 0
        assert new_state.last_failure_time is None

        # From closed state - should reset failure count
        closed_state = CircuitBreakerState(state="closed", failure_count=2, last_failure_time=123.456)
        new_state = closed_state.record_success()
        assert new_state.is_closed()
        assert new_state.failure_count == 0
        assert new_state.last_failure_time is None

        # From open state - should return unchanged
        open_state = CircuitBreakerState(state="open", failure_count=5)
        new_state = open_state.record_success()
        assert new_state is open_state  # Should be unchanged

    def test_record_failure_from_different_states(self, time_machine: TimeMachine) -> None:
        """Test record_failure behavior from different states."""
        current_time = 1000.0
        time_machine.freeze(current_time)

        # From half-open state - should go back to open
        half_open_state = CircuitBreakerState(state="half_open", failure_count=1, recovery_timeout=60.0)
        new_state = half_open_state.record_failure()
        assert new_state.is_open()
        assert new_state.failure_count == 2
        assert new_state.last_failure_time == current_time
        assert new_state.next_attempt_time == current_time + 60.0

        # From closed state - below threshold
        closed_state = CircuitBreakerState(state="closed", failure_count=1, failure_threshold=5)
        new_state = closed_state.record_failure()
        assert new_state.is_closed()
        assert new_state.failure_count == 2
        assert new_state.last_failure_time == current_time

        # From closed state - reaches threshold
        closed_state_threshold = CircuitBreakerState(
            state="closed", failure_count=4, failure_threshold=5, recovery_timeout=30.0
        )
        new_state = closed_state_threshold.record_failure()
        assert new_state.is_open()
        assert new_state.failure_count == 5
        assert new_state.last_failure_time == current_time
        assert new_state.next_attempt_time == current_time + 30.0

        # From open state - should update failure info
        open_state = CircuitBreakerState(state="open", failure_count=5, recovery_timeout=45.0)
        new_state = open_state.record_failure()
        assert new_state.is_open()
        assert new_state.failure_count == 6
        assert new_state.last_failure_time == current_time
        assert new_state.next_attempt_time == current_time + 45.0

    def test_attempt_reset_conditions(self, time_machine: TimeMachine) -> None:
        """Test attempt_reset under various conditions."""
        current_time = 1000.0  # Fixed time for test
        time_machine.freeze(current_time)

        # Open state ready for reset
        open_state_ready = CircuitBreakerState(state="open", next_attempt_time=current_time - 1)
        new_state = open_state_ready.attempt_reset()
        assert new_state.is_half_open()

        # Open state not ready for reset
        open_state_not_ready = CircuitBreakerState(state="open", next_attempt_time=current_time + 100)
        new_state = open_state_not_ready.attempt_reset()
        assert new_state is open_state_not_ready  # Should be unchanged

        # Closed state - should not reset
        closed_state = CircuitBreakerState(state="closed")
        new_state = closed_state.attempt_reset()
        assert new_state is closed_state  # Should be unchanged

        # Half-open state - should not reset
        half_open_state = CircuitBreakerState(state="half_open")
        new_state = half_open_state.attempt_reset()
        assert new_state is half_open_state  # Should be unchanged

    def test_force_reset(self) -> None:
        """Test force_reset functionality."""
        # From open state with failures
        open_state = CircuitBreakerState(
            state="open",
            failure_count=10,
            last_failure_time=123.456,
            next_attempt_time=789.012,
        )
        new_state = open_state.force_reset()
        assert new_state.is_closed()
        assert new_state.failure_count == 0
        assert new_state.last_failure_time is None
        assert new_state.next_attempt_time == 0.0

        # From half-open state
        half_open_state = CircuitBreakerState(state="half_open", failure_count=3, last_failure_time=123.456)
        new_state = half_open_state.force_reset()
        assert new_state.is_closed()
        assert new_state.failure_count == 0
        assert new_state.last_failure_time is None
        assert new_state.next_attempt_time == 0.0


class TestCircuitBreakerStateMachineEdgeCases(FoundationTestCase):
    """Test edge cases in CircuitBreakerStateMachine."""

    def test_state_machine_initialization_with_custom_params(self) -> None:
        """Test CircuitBreakerStateMachine initialization with custom parameters."""
        machine = CircuitBreakerStateMachine(failure_threshold=10, recovery_timeout=120.0)

        assert machine.current_state == "closed"
        assert machine.circuit_state.failure_threshold == 10
        assert machine.circuit_state.recovery_timeout == 120.0
        assert machine.circuit_state.failure_count == 0

    def test_state_machine_transitions_property_access(self) -> None:
        """Test accessing circuit_state property."""
        machine = CircuitBreakerStateMachine()
        circuit_state = machine.circuit_state

        assert isinstance(circuit_state, CircuitBreakerState)
        assert circuit_state.is_closed()

    def test_guard_function_behavior(self, time_machine: TimeMachine) -> None:
        """Test the guard function behavior."""
        time_machine.freeze()
        machine = CircuitBreakerStateMachine(recovery_timeout=0.1)

        # Make circuit open
        machine.transition(CircuitBreakerEvent.FAILURE)
        machine.transition(CircuitBreakerEvent.FAILURE)
        machine.transition(CircuitBreakerEvent.FAILURE)
        machine.transition(CircuitBreakerEvent.FAILURE)
        machine.transition(CircuitBreakerEvent.FAILURE)

        assert machine.current_state == "open"

        # Guard should return False initially
        assert not machine._should_attempt_reset()

        # Jump past the timeout
        time_machine.jump(0.15)

        # Guard should return True after timeout
        assert machine._should_attempt_reset()

    def test_action_methods_directly(self) -> None:
        """Test action methods can be called directly."""
        machine = CircuitBreakerStateMachine()

        # Test _record_success
        initial_state = machine.circuit_state
        machine._record_success()
        # Should have updated circuit state (generation changed)
        assert machine.circuit_state.generation != initial_state.generation

        # Test _record_failure
        machine._record_failure()
        assert machine.circuit_state.failure_count == 1

        # Test _force_reset
        machine._force_reset()
        assert machine.circuit_state.failure_count == 0
        assert machine.circuit_state.is_closed()

    def test_manual_state_update_in_handle_closed_failure(self) -> None:
        """Test the manual state update in _handle_closed_failure."""
        machine = CircuitBreakerStateMachine(failure_threshold=2)

        # Trigger a failure that should open the circuit
        machine._handle_closed_failure()  # 1st failure
        assert machine.current_state == "closed"

        machine._handle_closed_failure()  # 2nd failure - should open
        assert machine.current_state == "open"
        assert machine.circuit_state.is_open()

    def test_reset_method(self) -> None:
        """Test the reset method."""
        machine = CircuitBreakerStateMachine()

        # Open the circuit
        for _ in range(10):  # Ensure we exceed any reasonable default threshold
            machine.transition(CircuitBreakerEvent.FAILURE)

        assert machine.current_state == "open"

        # Reset using the reset method
        machine.reset()
        assert machine.current_state == "closed"
        assert machine.circuit_state.failure_count == 0

    def test_transitions_from_all_states_to_reset(self, time_machine: TimeMachine) -> None:
        """Test reset transitions work from all states."""
        time_machine.freeze()
        machine = CircuitBreakerStateMachine(recovery_timeout=0.05)  # Short timeout for test

        # Reset from closed
        machine.transition(CircuitBreakerEvent.RESET)
        assert machine.current_state == "closed"

        # Go to open, then reset
        # Use enough failures to trigger open state based on default threshold
        for _ in range(10):  # Ensure we exceed any reasonable default threshold
            machine.transition(CircuitBreakerEvent.FAILURE)
        assert machine.current_state == "open"

        machine.transition(CircuitBreakerEvent.RESET)
        assert machine.current_state == "closed"

        # Go to half-open, then reset
        # Use enough failures to trigger open state based on default threshold
        for _ in range(10):  # Ensure we exceed any reasonable default threshold
            machine.transition(CircuitBreakerEvent.FAILURE)
        assert machine.current_state == "open"

        time_machine.jump(0.1)  # Jump past recovery timeout
        machine.transition(CircuitBreakerEvent.TIMEOUT)
        assert machine.current_state == "half_open"

        machine.transition(CircuitBreakerEvent.RESET)
        assert machine.current_state == "closed"

    def test_attempt_reset_action_method(self, time_machine: TimeMachine) -> None:
        """Test _attempt_reset action method."""
        time_machine.freeze()
        machine = CircuitBreakerStateMachine(recovery_timeout=0.05)

        # Open the circuit
        for _ in range(10):  # Ensure we exceed any reasonable default threshold
            machine.transition(CircuitBreakerEvent.FAILURE)

        assert machine.current_state == "open"

        # Jump past timeout and call _attempt_reset directly
        time_machine.jump(0.1)
        machine._attempt_reset()
        assert machine.circuit_state.is_half_open()

    def test_timeout_transition_guard_prevents_invalid_reset(self) -> None:
        """Test that timeout transition guard prevents reset before timeout."""
        machine = CircuitBreakerStateMachine(recovery_timeout=1.0)  # Long timeout

        # Open the circuit
        for _ in range(10):  # Ensure we exceed any reasonable default threshold
            machine.transition(CircuitBreakerEvent.FAILURE)

        assert machine.current_state == "open"

        # Try to transition with timeout event - should fail guard
        machine.transition(CircuitBreakerEvent.TIMEOUT)
        assert machine.current_state == "open"  # Should remain open


class TestCircuitBreakerEvent(FoundationTestCase):
    """Test CircuitBreakerEvent enum."""

    def test_event_enum_values(self) -> None:
        """Test that all event enum values exist."""
        assert CircuitBreakerEvent.SUCCESS
        assert CircuitBreakerEvent.FAILURE
        assert CircuitBreakerEvent.TIMEOUT
        assert CircuitBreakerEvent.RESET

        # Test that they are distinct
        events = [
            CircuitBreakerEvent.SUCCESS,
            CircuitBreakerEvent.FAILURE,
            CircuitBreakerEvent.TIMEOUT,
            CircuitBreakerEvent.RESET,
        ]
        assert len(set(events)) == 4
