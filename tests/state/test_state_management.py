from __future__ import annotations

import threading
import time
from unittest.mock import Mock

import pytest

from provide.foundation.state import (
    CircuitBreakerEvent,
    CircuitBreakerState,
    CircuitBreakerStateMachine,
    ConfigManager,
    ImmutableState,
    LoggerStateManager,
    StateManager,
    VersionedConfig,
)


class TestImmutableState:
    """Test immutable state base class."""

    def test_immutable_state_creation(self) -> None:
        """Test creating immutable state."""
        state = ImmutableState()
        assert state.generation == 0
        assert isinstance(state.created_at, float)

    def test_with_changes_increments_generation(self) -> None:
        """Test that with_changes increments generation."""
        state = ImmutableState()
        new_state = state.with_changes()
        assert new_state.generation == 1
        assert new_state.created_at == state.created_at

    def test_immutability(self) -> None:
        """Test that state objects are immutable."""
        state = ImmutableState()
        # For mypy, this will cause a type error, but we can still test runtime behavior
        try:
            state.generation = 5  # type: ignore[misc]
            pytest.fail("Expected exception for immutable assignment")
        except Exception:
            # attrs raises FrozenInstanceError, which is what we expect
            pass


class TestStateManager:
    """Test state manager functionality."""

    def test_state_manager_creation(self) -> None:
        """Test creating a state manager."""
        initial_state = ImmutableState()
        manager = StateManager(state=initial_state)
        assert manager.current_state is initial_state
        assert manager.generation == 0

    def test_atomic_updates(self) -> None:
        """Test atomic state updates."""
        initial_state = ImmutableState()
        manager = StateManager(state=initial_state)

        new_state = manager.update_state()
        assert new_state.generation == 1
        assert manager.current_state is new_state

    def test_thread_safety(self) -> None:
        """Test thread-safe access to state."""
        initial_state = ImmutableState()
        manager = StateManager(state=initial_state)
        results = []

        def worker() -> None:
            state = manager.current_state
            results.append(state.generation)

        threads = [threading.Thread(target=worker) for _ in range(10)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        # All threads should see the same generation
        assert all(gen == 0 for gen in results)

    def test_observers(self) -> None:
        """Test state change observers."""
        initial_state = ImmutableState()
        manager = StateManager(state=initial_state)

        observer_calls = []

        def observer(old_state: ImmutableState, new_state: ImmutableState) -> None:
            observer_calls.append((old_state.generation, new_state.generation))

        manager.add_observer(observer)
        manager.update_state()

        assert len(observer_calls) == 1
        assert observer_calls[0] == (0, 1)


class TestVersionedConfig:
    """Test versioned configuration."""

    def test_config_creation(self) -> None:
        """Test creating versioned config."""
        config = VersionedConfig(config_name="test")
        assert config.config_name == "test"
        assert config.data == {}
        assert config.generation == 0

    def test_config_get_set(self) -> None:
        """Test getting and setting config values."""
        config = VersionedConfig(config_name="test")
        assert config.get("key", "default") == "default"

        new_config = config.set("key", "value")
        assert new_config.get("key") == "value"
        assert new_config.generation == 1

    def test_config_update(self) -> None:
        """Test updating multiple config values."""
        config = VersionedConfig(config_name="test")
        new_config = config.update({"key1": "value1", "key2": "value2"})

        assert new_config.get("key1") == "value1"
        assert new_config.get("key2") == "value2"
        assert new_config.generation == 1

    def test_config_immutability(self) -> None:
        """Test config immutability."""
        config = VersionedConfig(config_name="test", data={"key": "value"})
        new_config = config.set("key", "new_value")

        # Original config unchanged
        assert config.get("key") == "value"
        assert new_config.get("key") == "new_value"


class TestConfigManager:
    """Test configuration manager."""

    def test_config_registration(self) -> None:
        """Test registering configurations."""
        manager = ConfigManager()
        config = VersionedConfig(config_name="test")

        manager.register_config(config)
        retrieved = manager.get_config("test")
        assert retrieved is not None
        assert retrieved.config_name == "test"

    def test_config_updates(self) -> None:
        """Test updating configurations."""
        manager = ConfigManager()
        config = VersionedConfig(config_name="test")
        manager.register_config(config)

        updated = manager.update_config("test", key="value")
        assert updated.get("key") == "value"
        assert updated.generation == 1

    def test_change_listeners(self) -> None:
        """Test configuration change listeners."""
        manager = ConfigManager()
        config = VersionedConfig(config_name="test")
        manager.register_config(config)

        listener_calls = []

        def listener(old_state: ImmutableState, new_state: ImmutableState) -> None:
            listener_calls.append((old_state.generation, new_state.generation))

        manager.add_change_listener("test", listener)
        manager.update_config("test", key="value")

        assert len(listener_calls) == 1
        assert listener_calls[0] == (0, 1)


class TestCircuitBreakerState:
    """Test circuit breaker state."""

    def test_initial_state(self) -> None:
        """Test initial circuit breaker state."""
        state = CircuitBreakerState()
        assert state.is_closed()
        assert not state.is_open()
        assert not state.is_half_open()
        assert state.failure_count == 0

    def test_record_failure(self) -> None:
        """Test recording failures."""
        state = CircuitBreakerState(failure_threshold=2)

        # First failure - should stay closed
        new_state = state.record_failure()
        assert new_state.is_closed()
        assert new_state.failure_count == 1

        # Second failure - should open
        new_state = new_state.record_failure()
        assert new_state.is_open()
        assert new_state.failure_count == 2

    def test_record_success(self) -> None:
        """Test recording success."""
        # Test success in half-open state
        state = CircuitBreakerState(state="half_open", failure_count=3)
        new_state = state.record_success()

        assert new_state.is_closed()
        assert new_state.failure_count == 0

    def test_should_attempt_reset(self) -> None:
        """Test reset timing logic."""
        current_time = time.time()
        state = CircuitBreakerState(
            state="open",
            next_attempt_time=current_time + 1.0,  # 1 second in future
        )

        assert not state.should_attempt_reset()

        # Simulate time passing
        state = state.with_changes(next_attempt_time=current_time - 1.0)
        assert state.should_attempt_reset()


class TestCircuitBreakerStateMachine:
    """Test circuit breaker state machine."""

    def test_state_machine_creation(self) -> None:
        """Test creating state machine."""
        machine = CircuitBreakerStateMachine()
        assert machine.current_state == "closed"
        assert machine.circuit_state.is_closed()

    def test_failure_transitions(self) -> None:
        """Test failure state transitions."""
        machine = CircuitBreakerStateMachine(failure_threshold=2)

        # First failure - stay closed
        assert machine.transition(CircuitBreakerEvent.FAILURE)
        assert machine.current_state == "closed"
        assert machine.circuit_state.failure_count == 1

        # Second failure - open circuit
        assert machine.transition(CircuitBreakerEvent.FAILURE)
        assert machine.current_state == "open"
        assert machine.circuit_state.failure_count == 2

    def test_recovery_transitions(self) -> None:
        """Test recovery state transitions."""
        machine = CircuitBreakerStateMachine(failure_threshold=2, recovery_timeout=0.001)

        # Force to open state
        machine.transition(CircuitBreakerEvent.FAILURE)
        machine.transition(CircuitBreakerEvent.FAILURE)
        assert machine.current_state == "open"

        # Wait for timeout and transition to half-open
        time.sleep(0.002)
        assert machine.transition(CircuitBreakerEvent.TIMEOUT)
        assert machine.current_state == "half_open"

        # Success in half-open should close circuit
        assert machine.transition(CircuitBreakerEvent.SUCCESS)
        assert machine.current_state == "closed"
        assert machine.circuit_state.failure_count == 0

    def test_reset_functionality(self) -> None:
        """Test manual reset."""
        machine = CircuitBreakerStateMachine(failure_threshold=2)

        # Force to open state
        machine.transition(CircuitBreakerEvent.FAILURE)
        machine.transition(CircuitBreakerEvent.FAILURE)
        assert machine.current_state == "open"

        # Reset should close circuit
        machine.reset()
        assert machine.current_state == "closed"
        assert machine.circuit_state.failure_count == 0



class TestLoggerStateManager:
    """Test logger state manager."""

    def test_logger_state_creation(self) -> None:
        """Test creating logger state manager."""
        manager = LoggerStateManager.create_default()
        assert not manager.is_setup_done
        assert not manager.is_setup_in_progress
        assert manager.setup_error is None

    def test_setup_lifecycle(self) -> None:
        """Test setup lifecycle management."""
        manager = LoggerStateManager.create_default()

        # Start setup
        manager.mark_setup_started()
        assert manager.is_setup_in_progress
        assert not manager.is_setup_done

        # Complete setup
        manager.mark_setup_completed()
        assert not manager.is_setup_in_progress
        assert manager.is_setup_done
        assert manager.is_configured_by_setup

    def test_setup_failure(self) -> None:
        """Test setup failure handling."""
        manager = LoggerStateManager.create_default()
        error = Exception("Setup failed")

        manager.mark_setup_started()
        manager.mark_setup_failed(error)

        assert not manager.is_setup_in_progress
        assert not manager.is_setup_done
        assert manager.setup_error is error
