#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from __future__ import annotations

from typing import Any

from provide.foundation.concurrency.locks import get_lock_manager
from provide.foundation.context import CLIContext
from provide.foundation.hub.commands import get_command_registry
from provide.foundation.hub.components import get_component_registry
from provide.foundation.hub.core import CoreHub
from provide.foundation.hub.foundation import FoundationManager
from provide.foundation.hub.registry import Registry
from provide.foundation.testmode.detection import should_use_shared_registries

"""Hub manager - the main coordinator for components and commands.

This module provides the Hub class that coordinates component and command
registration, discovery, and access, with Foundation system integration.
"""


class Hub(CoreHub):
    """Central hub for managing components, commands, and Foundation integration.

    The Hub provides a unified interface for:
    - Registering components and commands
    - Discovering plugins via entry points
    - Creating Click CLI applications
    - Managing component lifecycle
    - Foundation system initialization

    Example:
        >>> hub = Hub()
        >>> hub.add_component(MyResource, "resource")
        >>> hub.add_command(init_cmd, "init")
        >>> hub.initialize_foundation()
        >>>
        >>> # Create CLI with all commands
        >>> cli = hub.create_cli()
        >>> cli()

    """

    def __init__(
        self,
        context: CLIContext | None = None,
        component_registry: Registry | None = None,
        command_registry: Registry | None = None,
        use_shared_registries: bool = False,
    ) -> None:
        """Initialize the hub.

        Args:
            context: Foundation CLIContext for configuration
            component_registry: Custom component registry
            command_registry: Custom command registry
            use_shared_registries: If True, use global shared registries

        """
        # Determine if we should use shared registries
        use_shared = should_use_shared_registries(use_shared_registries, component_registry, command_registry)

        # Setup registries
        if component_registry:
            comp_registry = component_registry
        elif use_shared:
            comp_registry = get_component_registry()
        else:
            comp_registry = Registry()

        if command_registry:
            cmd_registry = command_registry
        elif use_shared:
            cmd_registry = get_command_registry()
        else:
            cmd_registry = Registry()

        # Initialize core hub functionality
        super().__init__(context, comp_registry, cmd_registry)

        # Initialize Foundation management, injecting self
        self._foundation = FoundationManager(hub=self, registry=self._component_registry)

    # Foundation Integration Methods

    def initialize_foundation(self, config: Any = None, force: bool = False) -> None:
        """Initialize Foundation system through Hub.

        Single initialization method replacing all setup_* functions.
        Thread-safe and idempotent, unless force=True.

        Args:
            config: Optional TelemetryConfig (defaults to from_env)
            force: If True, force re-initialization even if already initialized

        """
        self._foundation.initialize_foundation(config, force)

    def get_foundation_logger(self, name: str | None = None) -> Any:
        """Get Foundation logger instance through Hub.

        Auto-initializes Foundation if not already done.
        Thread-safe with fallback behavior.

        Args:
            name: Logger name (e.g., module name)

        Returns:
            Configured logger instance

        """
        return self._foundation.get_foundation_logger(name)

    def is_foundation_initialized(self) -> bool:
        """Check if Foundation system is initialized."""
        return self._foundation.is_foundation_initialized()

    def get_foundation_config(self) -> Any | None:
        """Get the current Foundation configuration."""
        return self._foundation.get_foundation_config()

    def clear(self, dimension: str | None = None) -> None:
        """Clear registrations and dispose of resources properly.

        Args:
            dimension: Optional dimension to clear (None = all)

        """
        # Clear core hub registrations (this will now dispose resources)
        super().clear(dimension)

        # Reset Foundation state when clearing all or foundation-specific dimensions
        if dimension is None or dimension in ("singleton", "foundation"):
            self._foundation.clear_foundation_state()

    def dispose_all(self) -> None:
        """Dispose of all managed resources without clearing registrations."""
        self._component_registry.dispose_all()
        if hasattr(self._command_registry, "dispose_all"):
            self._command_registry.dispose_all()


# Global hub instance for thread-safe singleton initialization
_global_hub: Hub | None = None


def get_hub() -> Hub:
    """Get the global shared hub instance (singleton pattern).

    This function acts as the Composition Root for the global singleton instance.
    It is maintained for backward compatibility and convenience.

    **Note:** For building testable and maintainable applications, the recommended
    approach is to use a `Container` or `Hub` instance created at your application's
    entry point for explicit dependency management. This global accessor should be
    avoided in application code.

    Thread-safe: Uses double-checked locking pattern for efficient lazy initialization.

    **Auto-Initialization Behavior:**
    This function automatically initializes the Foundation system on first access.
    The initialization is:
    - **Idempotent**: Safe to call multiple times
    - **Thread-safe**: Uses lock manager for coordination
    - **Lazy**: Only happens on first access

    Returns:
        Global Hub instance (created and initialized if needed)

    Example:
        >>> hub = get_hub()
        >>> hub.register_command("my_command", my_function)

    Note:
        For isolated Hub instances (testing, advanced use cases), use:
        >>> hub = Hub(use_shared_registries=False)

    """
    global _global_hub

    # Fast path: hub already initialized
    if _global_hub is not None:
        return _global_hub

    # Slow path: need to initialize hub
    with get_lock_manager().acquire("foundation.hub.init"):
        # Double-check after acquiring lock
        if _global_hub is None:
            # Global hub uses shared registries by default
            _global_hub = Hub(use_shared_registries=True)

            # Auto-initialize Foundation on first hub access
            _global_hub.initialize_foundation()

            # Bootstrap foundation components now that hub is ready (skip in test mode)
            from provide.foundation.testmode.detection import is_in_test_mode

            if not is_in_test_mode():
                try:
                    from provide.foundation.hub.components import bootstrap_foundation

                    bootstrap_foundation()
                except ImportError:
                    # Bootstrap function might not exist yet, that's okay
                    pass

    return _global_hub


def clear_hub() -> None:
    """Clear the global hub instance.

    This is primarily used for testing to reset Foundation state
    between test runs.

    """
    global _global_hub
    if _global_hub:
        _global_hub.clear()
    _global_hub = None


# 🧱🏗️🔚
