"""
Provide Foundation Hub - Component and Command Coordination System
===================================================================

The hub module provides a unified system for registering, discovering, and
managing components and CLI commands across the provide-io ecosystem.

Key Features:
- Multi-dimensional component registry
- CLI command registration and discovery
- Entry point discovery
- Integration with Click framework
- Type-safe decorators using Python 3.11+ features

Example Usage:
    >>> from provide.foundation.hub import Hub, register_command
    >>>
    >>> class MyResource:
    >>>     def __init__(self, name: str):
    >>>         self.name = name
    >>>
    >>> @register_command("init")
    >>> def init_command():
    >>>     pass
    >>>
    >>> hub = Hub()
    >>> hub.add_component(MyResource, name="my_resource", version="1.0.0")
    >>> resource_class = hub.get_component("my_resource")
    >>> command = hub.get_command("init")
"""

# Core hub components (always available)
from provide.foundation.hub.components import (
    ComponentCategory,
    get_component_registry,
)
from provide.foundation.hub.decorators import register_command
from provide.foundation.hub.manager import (
    Hub,
    clear_hub,
    get_hub,
)


# CLI features (require click) - lazy loaded
def get_click_commands():
    """
    Get CLI command building functions.

    Returns:
        Module with click command building functionality.

    Raises:
        ImportError: If click is not available.
    """
    try:
        from provide.foundation.hub.commands import build_click_command

        return {"build_click_command": build_click_command}
    except ImportError as e:
        if "click" in str(e):
            raise ImportError(
                "CLI command building requires optional dependencies. Install with: "
                "pip install 'provide-foundation[cli]'"
            ) from e
        raise


def __getattr__(name: str):
    """Support lazy loading of CLI-dependent features."""
    if name == "build_click_command":
        return get_click_commands()["build_click_command"]
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")


__all__ = [
    # Components
    "get_component_registry",
    "ComponentCategory",
    # Hub
    "Hub",
    "clear_hub",
    "get_hub",
    # Commands (core)
    "register_command",
    # CLI features (lazy loaded)
    "get_click_commands",
]
