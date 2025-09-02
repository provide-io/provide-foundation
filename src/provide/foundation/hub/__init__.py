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
    >>> from provide.foundation.hub import Hub, register_component, register_command
    >>>
    >>> @register_component("my_resource", version="1.0.0")
    >>> class MyResource:
    >>>     pass
    >>>
    >>> @register_command("init")
    >>> def init_command():
    >>>     pass
    >>>
    >>> hub = Hub()
    >>> resource = hub.get_component("my_resource")
    >>> command = hub.get_command("init")
"""

from provide.foundation.hub.commands import (
    build_click_command,
    register_command,
)
from provide.foundation.hub.components import (
    BaseComponent,
    discover_components,
    register_component,
)
from provide.foundation.hub.manager import (
    Hub,
    clear_hub,
    get_hub,
)

__all__ = [
    # Components
    "BaseComponent",
    "register_component",
    "discover_components",
    # Commands
    "register_command",
    "build_click_command",
    # Hub
    "Hub",
    "get_hub",
    "clear_hub",
]
