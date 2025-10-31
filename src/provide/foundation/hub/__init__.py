#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

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
    >>> command = hub.get_command("init")"""

from __future__ import annotations

# Core hub components (always available)
from provide.foundation.hub.components import (
    ComponentCategory,
    get_component_registry,
)
from provide.foundation.hub.container import (
    Container,
    create_container,
)
from provide.foundation.hub.decorators import register_command
from provide.foundation.hub.injection import (
    injectable,
    is_injectable,
)
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

__all__ = [
    # Resource Management Protocols
    "AsyncContextResource",
    "AsyncDisposable",
    "AsyncInitializable",
    "AsyncResourceManager",
    "ComponentCategory",
    # Dependency Injection
    "Container",
    "Disposable",
    "HealthCheckable",
    # Hub
    "Hub",
    "Initializable",
    # Registry
    "Registry",
    "RegistryEntry",
    "ResourceManager",
    "clear_hub",
    "create_container",
    # Components
    "get_component_registry",
    "get_hub",
    "injectable",
    "is_injectable",
    # Commands (core)
    "register_command",
]

# 🧱🏗️🔚
