#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from __future__ import annotations

import contextlib
from enum import Enum, auto
import threading
from typing import Any

from attrs import define

from provide.foundation.concurrency.locks import get_lock_manager
from provide.foundation.errors.runtime import RuntimeError as FoundationRuntimeError
from provide.foundation.state.base import ImmutableState, StateMachine, StateTransition

"""Simplified, centralized initialization coordinator.

This module consolidates all initialization logic into a single,
thread-safe state machine that uses the LockManager for coordination.
"""


class InitState(Enum):
    """Initialization states."""

    UNINITIALIZED = auto()
    INITIALIZING = auto()
    INITIALIZED = auto()
    FAILED = auto()


class InitEvent(Enum):
    """Initialization events."""

    START = auto()
    COMPLETE = auto()
    FAIL = auto()
    RESET = auto()


@define(frozen=True, slots=True, kw_only=True)
class InitializationState(ImmutableState):
    """Immutable initialization state."""

    status: InitState = InitState.UNINITIALIZED
    config: Any = None
    logger_instance: Any = None
    error: Exception | None = None


class InitializationStateMachine(StateMachine[InitState, InitEvent]):
    """State machine for Foundation initialization.

    States:
    - UNINITIALIZED: Initial state, no initialization attempted
    - INITIALIZING: Initialization in progress
    - INITIALIZED: Successfully initialized
    - FAILED: Initialization failed

    Events:
    - START: Begin initialization
    - COMPLETE: Mark initialization complete
    - FAIL: Mark initialization failed
    - RESET: Reset to uninitialized state
    """

    def __init__(self) -> None:
        """Initialize the state machine."""
        super().__init__(InitState.UNINITIALIZED)
        self._state_data = InitializationState()
        self._event = threading.Event()

        # Define transitions
        self.add_transition(
            StateTransition(
                from_state=InitState.UNINITIALIZED,
                event=InitEvent.START,
                to_state=InitState.INITIALIZING,
            )
        )
        self.add_transition(
            StateTransition(
                from_state=InitState.INITIALIZING,
                event=InitEvent.COMPLETE,
                to_state=InitState.INITIALIZED,
                action=self._event.set,
            )
        )
        self.add_transition(
            StateTransition(
                from_state=InitState.INITIALIZING,
                event=InitEvent.FAIL,
                to_state=InitState.FAILED,
                action=self._event.set,
            )
        )
        # Allow reset from any state
        for state in [InitState.INITIALIZED, InitState.FAILED, InitState.INITIALIZING]:
            self.add_transition(
                StateTransition(
                    from_state=state,
                    event=InitEvent.RESET,
                    to_state=InitState.UNINITIALIZED,
                    action=self._event.clear,
                )
            )

    @property
    def state_data(self) -> InitializationState:
        """Get the current state data."""
        with self._lock:
            return self._state_data

    def mark_complete(self, config: Any, logger_instance: Any) -> None:
        """Mark initialization as complete."""
        with self._lock:
            # Type ignore needed because with_changes returns ImmutableState
            # but we know it's actually InitializationState
            self._state_data = self._state_data.with_changes(  # type: ignore[assignment]
                status=InitState.INITIALIZED,
                config=config,
                logger_instance=logger_instance,
                error=None,
            )
        self.transition(InitEvent.COMPLETE)

    def mark_failed(self, error: Exception) -> None:
        """Mark initialization as failed."""
        with self._lock:
            # Type ignore needed because with_changes returns ImmutableState
            # but we know it's actually InitializationState
            self._state_data = self._state_data.with_changes(  # type: ignore[assignment]
                status=InitState.FAILED,
                error=error,
            )
        self.transition(InitEvent.FAIL)

    def wait_for_completion(self, timeout: float = 10.0) -> bool:
        """Wait for initialization to complete."""
        return self._event.wait(timeout)

    def reset(self) -> None:
        """Reset the state machine to uninitialized."""
        with self._lock:
            self._state_data = InitializationState()
        self.transition(InitEvent.RESET)


class InitializationCoordinator:
    """Centralized initialization coordinator using state machine."""

    def __init__(self) -> None:
        """Initialize coordinator."""
        self._state_machine = InitializationStateMachine()
        self._lock_manager = get_lock_manager()

        # Register all foundation locks (includes coordinator lock)
        from provide.foundation.concurrency.locks import register_foundation_locks

        with contextlib.suppress(ValueError):
            # Already registered if ValueError raised
            register_foundation_locks()

    def initialize_foundation(self, registry: Any, config: Any = None, force: bool = False) -> tuple[Any, Any]:
        """Simplified, single-path initialization.

        Args:
            registry: Component registry
            config: Optional configuration (TelemetryConfig)
            force: Force re-initialization

        Returns:
            Tuple of (config, logger_instance)

        Raises:
            RuntimeError: If initialization fails
        """
        # Fast path if already initialized and not forcing
        state_data = self._state_machine.state_data
        if self._state_machine.current_state == InitState.INITIALIZED and not force:
            return state_data.config, state_data.logger_instance

        # Use lock manager for thread-safe initialization
        with self._lock_manager.acquire("foundation.init.coordinator"):
            # Double-check after acquiring lock
            state_data = self._state_machine.state_data
            if self._state_machine.current_state == InitState.INITIALIZED and not force:
                return state_data.config, state_data.logger_instance

            if force:
                self._state_machine.reset()

            # Transition to INITIALIZING state
            self._state_machine.transition(InitEvent.START)

            try:
                # Get foundation internal logger for timing
                from provide.foundation.logger.setup.coordinator import (
                    create_foundation_internal_logger,
                )
                from provide.foundation.utils.timing import timed_block

                setup_logger = create_foundation_internal_logger()

                # Single initialization path with performance monitoring
                with timed_block(setup_logger, "Foundation config initialization"):
                    actual_config = self._initialize_config(config)

                with timed_block(setup_logger, "Foundation logger initialization"):
                    logger_instance = self._initialize_logger(actual_config, registry)

                with timed_block(setup_logger, "Foundation component registration"):
                    # Register with registry
                    self._register_components(registry, actual_config, logger_instance)

                with timed_block(setup_logger, "Foundation event handler setup"):
                    # Set up event handlers
                    self._setup_event_handlers()

                # Mark complete (transitions to INITIALIZED)
                self._state_machine.mark_complete(actual_config, logger_instance)

                return actual_config, logger_instance

            except Exception as e:
                self._state_machine.mark_failed(e)
                raise FoundationRuntimeError(
                    f"Foundation initialization failed: {e}",
                    code="FOUNDATION_INIT_FAILED",
                    cause=e,
                    initialization_phase="config_and_logger",
                ) from e

    def update_config_if_default(self, registry: Any, new_config: Any) -> bool:
        """Update config in-place if current config is from auto-init (service_name=None).

        This provides a lightweight alternative to force re-initialization when
        applications want to override default auto-init config with explicit config.

        Args:
            registry: Component registry
            new_config: New configuration to use

        Returns:
            True if config was updated, False if no update needed
        """
        state_data = self._state_machine.state_data

        # Only update if initialized and current config has no service_name (auto-init indicator)
        if (
            self._state_machine.current_state == InitState.INITIALIZED
            and state_data.config is not None
            and getattr(state_data.config, "service_name", "not-none") is None
        ):
            # Update state machine config
            with self._state_machine._lock:
                self._state_machine._state_data = state_data.with_changes(config=new_config)  # type: ignore[assignment]

            # Update registry config
            registry.register(
                name="foundation.config",
                value=new_config,
                dimension="singleton",
                metadata={"initialized": True},
                replace=True,
            )

            return True

        return False

    def _initialize_config(self, config: Any) -> Any:
        """Initialize configuration."""
        if config:
            return config

        # Load from environment
        from provide.foundation.logger.config import TelemetryConfig

        try:
            return TelemetryConfig.from_env()
        except Exception as e:
            # Only fallback for config parsing errors, not import errors
            if "import" in str(e).lower():
                raise
            # Fallback to minimal config for environment parsing issues
            return TelemetryConfig()

    def _initialize_logger(self, config: Any, registry: Any) -> Any:
        """Initialize logger instance."""
        from provide.foundation.logger.core import FoundationLogger

        # Create hub wrapper for logger
        hub_wrapper = type("HubWrapper", (), {"_component_registry": registry, "_foundation_config": config})()

        logger_instance = FoundationLogger(hub=hub_wrapper)
        logger_instance.setup(config)

        return logger_instance

    def _register_components(self, registry: Any, config: Any, logger_instance: Any) -> None:
        """Register components in registry."""
        # Register config
        registry.register(
            name="foundation.config",
            value=config,
            dimension="singleton",
            metadata={"initialized": True},
            replace=True,
        )

        # Register logger
        registry.register(
            name="foundation.logger.instance",
            value=logger_instance,
            dimension="singleton",
            metadata={"initialized": True},
            replace=True,
        )

    def _setup_event_handlers(self) -> None:
        """Set up event handlers."""
        try:
            from provide.foundation.hub.event_handlers import setup_event_logging

            setup_event_logging()
        except Exception:
            # If event handler setup fails, continue without it
            pass

    def get_state(self) -> InitializationState:
        """Get current initialization state."""
        return self._state_machine.state_data

    def is_initialized(self) -> bool:
        """Check if foundation is initialized."""
        return self._state_machine.current_state == InitState.INITIALIZED

    def reset_state(self) -> None:
        """Reset coordinator state for testing."""
        self._state_machine.reset()


# Global coordinator instance
_coordinator = InitializationCoordinator()


def get_initialization_coordinator() -> InitializationCoordinator:
    """Get the global initialization coordinator."""
    return _coordinator


__all__ = [
    "InitEvent",
    "InitState",
    "InitializationCoordinator",
    "InitializationState",
    "InitializationStateMachine",
    "get_initialization_coordinator",
]

# 🧱🏗️🔚
