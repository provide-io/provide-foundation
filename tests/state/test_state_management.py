import time

from attrs import define
import pytest

from provide.foundation.state import (
    ImmutableState,
    StateManager,
)
from provide.foundation.state._internal.transitions import (
    CircuitBreakerEvent,
    CircuitBreakerStateMachine,
)


class TestImmutableState:
    def test_initial_state(self) -> None:
        state = ImmutableState()
        assert state.generation == 0
        assert isinstance(state.created_at, float)

    def test_with_changes(self) -> None:
        state1 = ImmutableState()
        state2 = state1.with_changes(generation=5)  # Deliberately setting generation
        assert state2.generation == 5
        assert state1.generation == 0  # Original is unchanged

    def test_with_changes_increments_generation(self) -> None:
        @define(frozen=True, slots=True)
        class CustomState(ImmutableState):
            value: int = 0

        state1 = CustomState()
        state2 = state1.with_changes(value=10)
        assert state2.generation == 1
        assert state2.value == 10
        assert state1.generation == 0
        assert state1.value == 0


class TestStateManager:
    def test_initial_state(self) -> None:
        initial = ImmutableState()
        manager = StateManager(state=initial)
        assert manager.current_state is initial
        assert manager.generation == 0

    def test_update_state(self) -> None:
        manager = StateManager(state=ImmutableState())
        old_state = manager.current_state
        new_state = manager.update_state(generation=10)
        assert manager.current_state is new_state
        assert new_state.generation == 10
        assert old_state.generation == 0


class TestCircuitBreaker:
    @pytest.fixture
    def machine(self):
        return CircuitBreakerStateMachine(failure_threshold=2, recovery_timeout=0.1)

    def test_initial_state_is_closed(self, machine) -> None:
        assert machine.current_state == "closed"
        assert machine.circuit_state.is_closed()

    def test_failure_below_threshold(self, machine) -> None:
        machine.transition(CircuitBreakerEvent.FAILURE)
        assert machine.current_state == "closed"
        assert machine.circuit_state.failure_count == 1

    def test_failure_reaches_threshold(self, machine) -> None:
        machine.transition(CircuitBreakerEvent.FAILURE)
        machine.transition(CircuitBreakerEvent.FAILURE)
        assert machine.current_state == "open"
        assert machine.circuit_state.is_open()
        assert machine.circuit_state.failure_count == 2

    def test_success_resets_failure_count(self, machine) -> None:
        machine.transition(CircuitBreakerEvent.FAILURE)
        machine.transition(CircuitBreakerEvent.SUCCESS)
        assert machine.current_state == "closed"
        assert machine.circuit_state.failure_count == 0

    def test_open_to_half_open_after_timeout(self, machine) -> None:
        machine.transition(CircuitBreakerEvent.FAILURE)
        machine.transition(CircuitBreakerEvent.FAILURE)
        assert machine.current_state == "open"
        time.sleep(0.15)
        assert machine._should_attempt_reset() is True
        machine.transition(CircuitBreakerEvent.TIMEOUT)
        assert machine.current_state == "half_open"

    def test_half_open_success_closes_circuit(self, machine) -> None:
        machine.transition(CircuitBreakerEvent.FAILURE)
        machine.transition(CircuitBreakerEvent.FAILURE)
        time.sleep(0.15)
        machine.transition(CircuitBreakerEvent.TIMEOUT)
        assert machine.current_state == "half_open"
        machine.transition(CircuitBreakerEvent.SUCCESS)
        assert machine.current_state == "closed"
        assert machine.circuit_state.failure_count == 0

    def test_half_open_failure_reopens_circuit(self, machine) -> None:
        machine.transition(CircuitBreakerEvent.FAILURE)
        machine.transition(CircuitBreakerEvent.FAILURE)
        time.sleep(0.15)
        machine.transition(CircuitBreakerEvent.TIMEOUT)
        assert machine.current_state == "half_open"
        machine.transition(CircuitBreakerEvent.FAILURE)
        assert machine.current_state == "open"
        assert machine.circuit_state.failure_count > 0

    def test_reset_event_from_open(self, machine) -> None:
        machine.transition(CircuitBreakerEvent.FAILURE)
        machine.transition(CircuitBreakerEvent.FAILURE)
        assert machine.current_state == "open"
        machine.transition(CircuitBreakerEvent.RESET)
        assert machine.current_state == "closed"
        assert machine.circuit_state.failure_count == 0
