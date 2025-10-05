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

        # Initialize Foundation management
        self._foundation = FoundationManager(self._component_registry)

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


# Global hub instance for thread-safe initialization (deprecated)
_global_hub: Hub | None = None


def get_hub() -> Hub:
    """Get an isolated Hub instance (new default behavior).

    **Breaking Change (Phase 2):**
    This function now returns an isolated Hub instance by default, NOT a global singleton.
    Each call creates a new, independent Hub with its own registries.

    For the old singleton behavior, use `get_shared_hub()` instead.

    **Benefits of Isolated Instances:**
    - Better testability (no global state to reset)
    - Parallel test execution without interference
    - Explicit dependency management
    - No memory leaks from lingering global state

    Example (Recommended):
        >>> hub = get_hub()  # New isolated instance
        >>> hub.initialize_foundation()
        >>> cli = hub.create_cli()

    For shared/global behavior:
        >>> hub = get_shared_hub()  # Old singleton behavior

    Returns:
        New isolated Hub instance (not auto-initialized)

    """
    # Return new isolated instance
    return Hub(use_shared_registries=False)


def get_shared_hub() -> Hub:
    """Get the global shared hub instance.

    .. deprecated:: 2.0
       Use `get_hub()` for isolated instances (recommended) or create
       `Hub(use_shared_registries=True)` explicitly for shared state.

    Thread-safe: Uses double-checked locking pattern for efficient lazy initialization.

    **Auto-Initialization Behavior:**
    This function automatically initializes the Foundation system on first access.
    The initialization is:
    - **Idempotent**: Safe to call multiple times
    - **Thread-safe**: Uses lock manager for coordination
    - **Lazy**: Only happens on first access

    Returns:
        Global Hub instance (created and initialized if needed)

    Warning:
        Global singletons complicate testing and parallel execution.
        Prefer isolated instances via `get_hub()` for better testability.

    """
    import warnings

    warnings.warn(
        "get_shared_hub() is deprecated. Use get_hub() for isolated instances "
        "or Hub(use_shared_registries=True) for explicit shared state.",
        DeprecationWarning,
        stacklevel=2,
    )

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

    .. deprecated:: 2.0
       Use `clear_shared_hub()` for the global singleton.
       Isolated instances from `get_hub()` don't need manual clearing.

    """
    import warnings

    warnings.warn(
        "clear_hub() is deprecated. Use clear_shared_hub() for global singleton, "
        "or let isolated instances from get_hub() be garbage collected.",
        DeprecationWarning,
        stacklevel=2,
    )
    clear_shared_hub()


def clear_shared_hub() -> None:
    """Clear the global shared hub instance."""
    global _global_hub
    if _global_hub:
        _global_hub.clear()
    _global_hub = None
