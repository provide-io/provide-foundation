#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Comprehensive initialization tests for improved coverage."""

from __future__ import annotations

from provide.testkit import FoundationTestCase
from provide.testkit.mocking import patch
import pytest

from provide.foundation.errors.runtime import RuntimeError as FoundationRuntimeError
from provide.foundation.hub.initialization import (
    InitEvent,
    InitializationCoordinator,
    InitializationStateMachine,
    InitState,
)
from provide.foundation.hub.registry import Registry
from provide.foundation.logger.config import TelemetryConfig


class TestStateMachineCoverage(FoundationTestCase):
    """Tests for state machine missing coverage."""

    def test_mark_failed_transitions_to_failed(self) -> None:
        """Test mark_failed transitions to FAILED state."""
        machine = InitializationStateMachine()
        machine.transition(InitEvent.START)  # Move to INITIALIZING

        error = ValueError("Test error")
        machine.mark_failed(error)

        assert machine.current_state == InitState.FAILED
        assert machine.state_data.error == error

    def test_wait_for_completion_timeout(self) -> None:
        """Test wait_for_completion with timeout."""
        machine = InitializationStateMachine()
        machine.transition(InitEvent.START)

        # Wait with very short timeout should return False
        result = machine.wait_for_completion(timeout=0.001)
        assert not result


class TestCoordinatorCoverage(FoundationTestCase):
    """Tests for coordinator missing coverage."""

    def test_initialize_foundation_already_initialized_after_lock(self) -> None:
        """Test double-check after acquiring lock."""
        coordinator = InitializationCoordinator()
        registry = Registry()
        config = TelemetryConfig(service_name="test")

        # First initialization
        coordinator.initialize_foundation(registry, config)

        # Second call should hit double-check after lock
        config2, logger2 = coordinator.initialize_foundation(registry, config)
        assert config2 is not None
        assert logger2 is not None

    def test_initialize_foundation_exception_handling(self) -> None:
        """Test exception handling during initialization."""
        coordinator = InitializationCoordinator()
        registry = Registry()

        # Mock _initialize_config to raise an exception
        with (
            patch.object(coordinator, "_initialize_config", side_effect=ValueError("Config error")),
            pytest.raises(FoundationRuntimeError, match="Foundation initialization failed"),
        ):
            coordinator.initialize_foundation(registry)

        # State should be FAILED
        assert coordinator._state_machine.current_state == InitState.FAILED

    def test_update_config_if_default_success(self) -> None:
        """Test update_config_if_default when config has no service_name."""
        coordinator = InitializationCoordinator()
        registry = Registry()

        # Initialize with default config (service_name=None)
        default_config = TelemetryConfig(service_name=None)
        coordinator.initialize_foundation(registry, default_config)

        # Update with explicit config
        new_config = TelemetryConfig(service_name="updated-service")
        result = coordinator.update_config_if_default(registry, new_config)

        assert result is True
        assert coordinator._state_machine.state_data.config == new_config

    def test_update_config_if_default_no_update_needed(self) -> None:
        """Test update_config_if_default when config already has service_name."""
        coordinator = InitializationCoordinator()
        registry = Registry()

        # Initialize with explicit config
        config = TelemetryConfig(service_name="explicit-service")
        coordinator.initialize_foundation(registry, config)

        # Try to update - should return False
        new_config = TelemetryConfig(service_name="new-service")
        result = coordinator.update_config_if_default(registry, new_config)

        assert result is False

    def test_update_config_if_default_not_initialized(self) -> None:
        """Test update_config_if_default when not initialized."""
        coordinator = InitializationCoordinator()
        registry = Registry()

        new_config = TelemetryConfig(service_name="test")
        result = coordinator.update_config_if_default(registry, new_config)

        assert result is False

    def test_initialize_config_import_error_raises(self) -> None:
        """Test _initialize_config raises on import errors."""
        coordinator = InitializationCoordinator()

        # Mock TelemetryConfig.from_env to raise ImportError
        with (
            patch(
                "provide.foundation.logger.config.TelemetryConfig.from_env",
                side_effect=ImportError("Cannot import module"),
            ),
            pytest.raises(ImportError, match="Cannot import module"),
        ):
            coordinator._initialize_config(None)

    def test_initialize_config_non_import_error_falls_back(self) -> None:
        """Test _initialize_config falls back on non-import errors."""
        coordinator = InitializationCoordinator()

        # Mock TelemetryConfig.from_env to raise ValueError
        with patch(
            "provide.foundation.logger.config.TelemetryConfig.from_env",
            side_effect=ValueError("Parse error"),
        ):
            config = coordinator._initialize_config(None)
            # Should return default TelemetryConfig
            assert config is not None

    def test_setup_event_handlers_exception_suppressed(self) -> None:
        """Test _setup_event_handlers suppresses exceptions."""
        coordinator = InitializationCoordinator()

        # Mock setup_event_logging to raise an exception
        with patch(
            "provide.foundation.hub.event_handlers.setup_event_logging",
            side_effect=RuntimeError("Event setup failed"),
        ):
            # Should not raise
            coordinator._setup_event_handlers()

    def test_get_state_returns_state_data(self) -> None:
        """Test get_state returns current state data."""
        coordinator = InitializationCoordinator()
        registry = Registry()

        state_before = coordinator.get_state()
        assert state_before.status == InitState.UNINITIALIZED

        coordinator.initialize_foundation(registry)

        state_after = coordinator.get_state()
        assert state_after.status == InitState.INITIALIZED

    def test_is_initialized_returns_bool(self) -> None:
        """Test is_initialized returns correct boolean."""
        coordinator = InitializationCoordinator()
        registry = Registry()

        assert not coordinator.is_initialized()

        coordinator.initialize_foundation(registry)

        assert coordinator.is_initialized()


if __name__ == "__main__":
    pytest.main([__file__])

# 🧱🏗️🔚
