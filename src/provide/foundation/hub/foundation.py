from __future__ import annotations

import threading
from typing import TYPE_CHECKING, Any

from provide.foundation.hub.registry import Registry

"""Foundation system initialization and lifecycle management.

This module provides Foundation-specific functionality for the Hub,
including telemetry configuration and logger initialization.
"""

if TYPE_CHECKING:
    from provide.foundation.logger.base import FoundationLogger
    from provide.foundation.logger.config import TelemetryConfig


class FoundationManager:
    """Manages Foundation system initialization and lifecycle."""

    def __init__(self, registry: Registry) -> None:
        """Initialize Foundation manager.

        Args:
            registry: Component registry for storing Foundation state
        """
        self._registry = registry
        self._initialized = False
        self._config: TelemetryConfig | None = None
        self._logger_instance: FoundationLogger | None = None
        self._init_lock = threading.Lock()

    def initialize_foundation(self, config: Any = None, force: bool = False) -> None:
        """Initialize Foundation system through Hub.

        Single initialization method replacing all setup_* functions.
        Thread-safe and idempotent, unless force=True.

        Args:
            config: Optional TelemetryConfig (defaults to from_env)
            force: If True, force re-initialization even if already initialized

        """
        # Fast path if already initialized and not forcing
        if self._initialized and not force:
            return

        with self._init_lock:
            # Double-check after acquiring lock (unless forcing)
            if self._initialized and not force:
                return

            # Check if config is already locked by explicit config from another Hub
            existing_entry = self._registry.get_entry("foundation.config", "singleton")
            if existing_entry and existing_entry.metadata.get("locked", False) and not force:
                # Use existing locked config instead of reinitializing
                self._config = existing_entry.value
                self._initialized = True
                return

            # Lazy import to avoid circular imports during module loading
            from provide.foundation.logger.config import TelemetryConfig

            # Handle config loading with graceful fallback
            try:
                if config:
                    # Use explicit config as-is to maintain precedence
                    self._config = config
                else:
                    # Load from environment when no explicit config
                    self._config = TelemetryConfig.from_env()
            except Exception:
                # Fallback to minimal default config if loading fails
                self._config = TelemetryConfig()

            # Register Foundation config as singleton
            # Mark explicit configs to prevent environment overrides
            is_explicit_config = config is not None
            self._registry.register(
                name="foundation.config",
                value=self._config,
                dimension="singleton",
                metadata={
                    "initialized": True,
                    "explicit_config": is_explicit_config,
                    "locked": is_explicit_config,  # Lock explicit configs from being replaced
                },
                replace=True,
            )

            # Initialize and register logger instance
            self._initialize_logger()

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

    def _initialize_logger(self) -> None:
        """Initialize the Foundation logger system through Hub."""
        # Lazy import to avoid circular imports during module loading
        from provide.foundation.logger.core import FoundationLogger

        try:
            # Create logger instance with Hub-like interface
            # For now, we'll create a minimal wrapper to avoid circular dependencies
            hub_wrapper = type(
                "HubWrapper", (), {"_component_registry": self._registry, "_foundation_config": self._config}
            )()

            logger_instance = FoundationLogger(hub=hub_wrapper)

            # Setup logger with configuration (self._config is guaranteed to be set by this point)
            if self._config is None:
                raise RuntimeError("Configuration not initialized")
            logger_instance.setup(self._config)

            # Register logger instance as singleton
            self._registry.register(
                name="foundation.logger.instance",
                value=logger_instance,
                dimension="singleton",
                metadata={"initialized": True},
                replace=True,
            )

            self._logger_instance = logger_instance

        except Exception as e:
            # If logger setup fails, continue with emergency fallback
            # This ensures Hub remains functional even if logging fails
            import sys

            print(f"Warning: Foundation logger setup failed: {e}", file=sys.stderr)
            print("Continuing with emergency fallback logger", file=sys.stderr)

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

        return self._registry.get("foundation.config", "singleton")

    def clear_foundation_state(self) -> None:
        """Clear Foundation initialization state."""
        self._initialized = False
        self._config = None
        self._logger_instance = None

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
    if hasattr(hub, "_foundation_manager") and hub._foundation_manager._logger_instance:
        return hub._foundation_manager._logger_instance.get_logger(name)

    # Fallback to direct logger import during bootstrap
    from provide.foundation.logger import logger

    if name:
        return logger.get_logger(name)
    return logger
