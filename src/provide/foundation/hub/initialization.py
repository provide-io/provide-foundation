from __future__ import annotations

import contextlib
import threading
from typing import Any

from provide.foundation.concurrency.locks import get_lock_manager

"""Simplified, centralized initialization coordinator.

This module consolidates all initialization logic into a single,
thread-safe state machine that uses the LockManager for coordination.
"""


class InitializationState:
    """Thread-safe initialization state tracker."""

    def __init__(self) -> None:
        """Initialize state tracker."""
        self.is_initialized = False
        self.initialization_error: Exception | None = None
        self.config: Any = None
        self.logger_instance: Any = None
        self._event = threading.Event()

    def mark_complete(self, config: Any, logger_instance: Any) -> None:
        """Mark initialization as complete."""
        self.config = config
        self.logger_instance = logger_instance
        self.is_initialized = True
        self._event.set()

    def mark_failed(self, error: Exception) -> None:
        """Mark initialization as failed."""
        self.initialization_error = error
        self._event.set()

    def wait_for_completion(self, timeout: float = 10.0) -> bool:
        """Wait for initialization to complete."""
        return self._event.wait(timeout)

    def reset(self) -> None:
        """Reset state for re-initialization."""
        self.is_initialized = False
        self.initialization_error = None
        self.config = None
        self.logger_instance = None
        self._event.clear()


class InitializationCoordinator:
    """Centralized initialization coordinator using LockManager."""

    def __init__(self) -> None:
        """Initialize coordinator."""
        self._state = InitializationState()
        self._lock_manager = get_lock_manager()

        # Register all foundation locks
        from provide.foundation.concurrency.locks import register_foundation_locks

        with contextlib.suppress(ValueError):
            # Already registered if ValueError raised
            register_foundation_locks()

        # Register initialization locks if not already registered
        with contextlib.suppress(ValueError):
            # Already registered if ValueError raised
            self._lock_manager.register_lock(
                "foundation.init.coordinator", order=200, description="Master initialization lock"
            )

    def initialize_foundation(self, registry: Any, config: Any = None, force: bool = False) -> tuple[Any, Any]:
        """Simplified, single-path initialization.

        Args:
            registry: Component registry
            config: Optional configuration
            force: Force re-initialization

        Returns:
            Tuple of (config, logger_instance)

        Raises:
            RuntimeError: If initialization fails
        """
        # Fast path if already initialized and not forcing
        if self._state.is_initialized and not force:
            return self._state.config, self._state.logger_instance

        # Use lock manager for thread-safe initialization
        with self._lock_manager.acquire("foundation.init.coordinator"):
            # Double-check after acquiring lock
            if self._state.is_initialized and not force:
                return self._state.config, self._state.logger_instance

            if force:
                self._state.reset()

            try:
                # Single initialization path
                actual_config = self._initialize_config(config)
                logger_instance = self._initialize_logger(actual_config, registry)

                # Register with registry
                self._register_components(registry, actual_config, logger_instance)

                # Set up event handlers
                self._setup_event_handlers()

                # Mark complete
                self._state.mark_complete(actual_config, logger_instance)

                return actual_config, logger_instance

            except Exception as e:
                self._state.mark_failed(e)
                raise RuntimeError(f"Foundation initialization failed: {e}") from e

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
        return self._state

    def is_initialized(self) -> bool:
        """Check if foundation is initialized."""
        return self._state.is_initialized

    def reset_state(self) -> None:
        """Reset coordinator state for testing."""
        self._state.reset()


# Global coordinator instance
_coordinator = InitializationCoordinator()


def get_initialization_coordinator() -> InitializationCoordinator:
    """Get the global initialization coordinator."""
    return _coordinator


__all__ = [
    "InitializationCoordinator",
    "InitializationState",
    "get_initialization_coordinator",
]
