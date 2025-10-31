#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from __future__ import annotations

import contextlib
import threading
from typing import TYPE_CHECKING, Any

from provide.foundation.hub.registry import Registry

"""Foundation system initialization and lifecycle management.

This module provides Foundation-specific functionality for the Hub,
including telemetry configuration and logger initialization.
"""

if TYPE_CHECKING:
    from provide.foundation.hub.manager import Hub
    from provide.foundation.logger.base import FoundationLogger
    from provide.foundation.logger.config import TelemetryConfig


class FoundationManager:
    """Manages Foundation system initialization and lifecycle."""

    def __init__(self, hub: Hub, registry: Registry) -> None:
        """Initialize Foundation manager.

        Args:
            hub: The parent Hub instance for context
            registry: Component registry for storing Foundation state
        """
        self._hub = hub
        self._registry = registry
        self._initialized = False
        self._config: TelemetryConfig | None = None
        self._logger_instance: FoundationLogger | None = None
        self._init_lock = threading.Lock()

    def initialize_foundation(self, config: Any = None, force: bool = False) -> None:
        """Initialize Foundation system through Hub.

        Single initialization method replacing all setup_* functions.
        Thread-safe and idempotent, unless force=True.

        Smart initialization: If explicit config is provided and Foundation
        was auto-initialized with defaults, automatically upgrades to force=True
        to ensure explicit config takes precedence.

        Args:
            config: Optional TelemetryConfig (defaults to from_env)
            force: If True, force re-initialization even if already initialized

        """
        # Smart initialization: Try lightweight config update OR force re-init when explicit
        # config is provided but Foundation is already auto-initialized with defaults
        if (
            config is not None  # Explicit config provided
            and self._initialized  # Already initialized (likely auto-init)
            and not force  # User didn't explicitly set force
            and self._config is not None  # Have existing config to check
            and getattr(self._config, "service_name", "not-none") is None  # Auto-init indicator
        ):
            # Check if OTLP is configured - if so, we MUST do full re-init to recreate LoggerProvider
            # The LoggerProvider bakes service_name into its Resource during creation, so we can't
            # just update the config - we need to recreate it
            otlp_configured = (
                getattr(self._config, "otlp_endpoint", None) is not None
                or getattr(config, "otlp_endpoint", None) is not None
            )

            # Use system logger for init-time logging (safe during Foundation setup)
            from provide.foundation.logger.setup.coordinator import get_system_logger

            setup_log = get_system_logger("provide.foundation.hub.init")

            if otlp_configured:
                # Force full re-initialization to recreate LoggerProvider with new service_name
                force = True
                setup_log.info(  # type: ignore[attr-defined]
                    "Foundation: Re-initializing with OTLP (explicit service_name overriding auto-init)"
                )
            else:
                # Try lightweight config update (avoids expensive re-initialization)
                from provide.foundation.hub.initialization import get_initialization_coordinator

                coordinator = get_initialization_coordinator()

                if coordinator.update_config_if_default(self._registry, config):
                    # Config updated successfully - no need to re-initialize
                    self._config = config
                    setup_log.info(  # type: ignore[attr-defined]
                        "Foundation: Updated config (explicit service_name overriding auto-init default)"
                    )
                    return
                # If lightweight update failed, fall through to normal initialization

        # Use the new simplified coordinator
        from provide.foundation.hub.initialization import get_initialization_coordinator

        coordinator = get_initialization_coordinator()

        actual_config, logger_instance = coordinator.initialize_foundation(
            registry=self._registry, config=config, force=force
        )

        # Update our local state
        self._config = actual_config
        self._logger_instance = logger_instance
        self._initialized = True

        # Log initialization success (avoid test interference)
        import os

        if not os.environ.get("PYTEST_CURRENT_TEST"):
            logger = self._get_logger()
            if logger:
                logger.info(
                    "Foundation initialized through Hub",
                    config_source="explicit" if config else "environment",
                )

    def get_foundation_logger(self, name: str | None = None) -> Any:
        """Get Foundation logger instance through Hub.

        Auto-initializes Foundation if not already done.
        Thread-safe with fallback behavior.

        Args:
            name: Logger name (e.g., module name)

        Returns:
            Configured logger instance

        """
        # Ensure Foundation is initialized
        if not self._initialized:
            self.initialize_foundation()

        # Get logger instance from registry
        logger_instance = self._registry.get("foundation.logger.instance", "singleton")

        if logger_instance:
            return logger_instance.get_logger(name)

        # Emergency fallback if logger instance not available
        import structlog

        return structlog.get_logger(name or "fallback")

    def is_foundation_initialized(self) -> bool:
        """Check if Foundation system is initialized."""
        return self._initialized

    def get_foundation_config(self) -> Any | None:
        """Get the current Foundation configuration."""
        if not self._initialized:
            self.initialize_foundation()

        # Return the local config if available
        if self._config:
            return self._config

        # Otherwise get from registry
        return self._registry.get("foundation.config", "singleton")

    def clear_foundation_state(self) -> None:
        """Clear Foundation initialization state."""
        self._initialized = False
        self._config = None
        self._logger_instance = None

        # Clear Foundation config from registry to prevent stale state
        if hasattr(self, "_registry") and self._registry:
            # Remove foundation config entries that might have stale state (entry might not exist)
            with contextlib.suppress(Exception):
                self._registry.remove("foundation.config", "singleton")
            with contextlib.suppress(Exception):
                self._registry.remove("foundation.logger.instance", "singleton")

        # Reset global coordinator state only in test mode
        from provide.foundation.testmode.detection import is_in_test_mode

        if is_in_test_mode():
            from provide.foundation.testmode.internal import reset_global_coordinator

            reset_global_coordinator()

    def _get_logger(self) -> Any | None:
        """Get logger for internal use."""
        if self._logger_instance:
            return self._logger_instance.get_logger(__name__)

        # Fallback during initialization
        import structlog

        return structlog.get_logger(__name__)


def get_foundation_logger(name: str | None = None) -> Any:
    """Get a logger from the Foundation system.

    This is the preferred way to get loggers instead of using _get_logger()
    patterns that create circular import issues.

    Args:
        name: Logger name (defaults to calling module)

    Returns:
        Logger instance
    """
    from provide.foundation.hub.manager import get_hub

    hub = get_hub()
    if hasattr(hub, "_foundation") and hub._foundation._logger_instance:
        return hub._foundation._logger_instance.get_logger(name)

    # Fallback to direct logger import during bootstrap
    from provide.foundation.logger import logger

    if name:
        return logger.get_logger(name)
    return logger


# 🧱🏗️🔚
