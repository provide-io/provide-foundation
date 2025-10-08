"""Provide Foundation Hub - Component and Command Coordination System
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

from __future__ import annotations

from typing import Any

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
from provide.foundation.hub.protocols import (
    AsyncContextResource,
    AsyncDisposable,
    AsyncInitializable,
    AsyncResourceManager,
    Disposable,
    HealthCheckable,
    Initializable,
    ResourceManager,
)
from provide.foundation.hub.registry import (
    Registry,
    RegistryEntry,
)


# CLI features - Delayed import to avoid circular dependency
def build_click_command(name: str, registry: Any = None) -> Any:
    """Build click command (delayed import to avoid circular dependency)."""
    try:
        from provide.foundation.cli.click.commands import build_click_command as real_func

        return real_func(name, registry)
    except ImportError as e:
        if "click" in str(e).lower():
            raise ImportError(
                "CLI command building requires optional dependencies. Install with: "
                "pip install 'provide-foundation[cli]'"
            ) from e
        raise


__all__ = [
    # Resource Management Protocols
    "AsyncContextResource",
    "AsyncDisposable",
    "AsyncInitializable",
    "AsyncResourceManager",
    "ComponentCategory",
    "Disposable",
    "HealthCheckable",
    # Hub
    "Hub",
    "Initializable",
    # Registry
    "Registry",
    "RegistryEntry",
    "ResourceManager",
    # CLI features (stub function if click not available)
    "build_click_command",
    "clear_hub",
    # Components
    "get_component_registry",
    "get_hub",
    # Commands (core)
    "register_command",
]
