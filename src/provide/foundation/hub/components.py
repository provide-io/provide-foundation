#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from __future__ import annotations

from typing import Any, Protocol

from attrs import define, field

from provide.foundation.config.defaults import DEFAULT_COMPONENT_DIMENSION
from provide.foundation.errors.decorators import resilient

# Import ComponentCategory from its own module (no circular deps)
from provide.foundation.hub.categories import ComponentCategory

# Import functions from specialized modules for re-export
from provide.foundation.hub.config import (
    get_config_chain,
    load_all_configs,
    load_config_from_registry,
    resolve_config_value,
)
from provide.foundation.hub.discovery import (
    discover_components,
    resolve_component_dependencies,
)
from provide.foundation.hub.handlers import (
    execute_error_handlers,
    get_handlers_for_exception,
)
from provide.foundation.hub.lifecycle import (
    cleanup_all_components,
    get_or_initialize_component,
    initialize_all_async_components,
    initialize_async_component,
)
from provide.foundation.hub.processors import (
    get_processor_pipeline,
    get_processors_for_stage,
)
from provide.foundation.hub.registry import Registry

"""Registry-based component management system for Foundation.

This module implements Foundation's end-state architecture where all internal
components are managed through the Hub registry system. Provides centralized
component discovery, lifecycle management, and dependency resolution.
"""


@define(frozen=True, slots=True)
class ComponentInfo:
    """Information about a registered component."""

    name: str = field()
    component_class: type[Any] = field()
    dimension: str = field(default=DEFAULT_COMPONENT_DIMENSION)
    version: str | None = field(default=None)
    description: str | None = field(default=None)
    author: str | None = field(default=None)
    tags: list[str] = field(factory=list)
    metadata: dict[str, Any] = field(factory=dict)


class ComponentLifecycle(Protocol):
    """Protocol for components that support lifecycle management."""

    async def initialize(self) -> None:
        """Initialize the component."""
        ...

    async def cleanup(self) -> None:
        """Clean up the component."""
        ...


# Global component registry
_component_registry = Registry()
_initialized_components: dict[tuple[str, str], Any] = {}


def get_component_registry() -> Registry:
    """Get the global component registry."""
    return _component_registry


@resilient(
    fallback={"status": "error"},
    context_provider=lambda: {
        "function": "check_component_health",
        "module": "hub.components",
    },
)
def check_component_health(name: str, dimension: str) -> dict[str, Any]:
    """Check component health status."""
    component = _component_registry.get(name, dimension)

    if not component:
        return {"status": "not_found"}

    entry = _component_registry.get_entry(name, dimension)
    if not entry or not entry.metadata.get("supports_health_check", False):
        return {"status": "no_health_check"}

    if hasattr(component, "health_check"):
        try:
            return component.health_check()
        except Exception as e:
            return {"status": "error", "error": str(e)}

    return {"status": "unknown"}


def get_component_config_schema(name: str, dimension: str) -> dict[str, Any] | None:
    """Get component configuration schema."""
    entry = _component_registry.get_entry(name, dimension)

    if not entry:
        return None

    return entry.metadata.get("config_schema")


def bootstrap_foundation() -> None:
    """Bootstrap Foundation with core registry components."""
    registry = get_component_registry()

    # Check if already bootstrapped
    if registry.get_entry("timestamp", ComponentCategory.PROCESSOR.value):
        return  # Already bootstrapped

    # Register core processors
    def timestamp_processor(logger: object, method_name: str, event_dict: dict[str, Any]) -> dict[str, Any]:
        import time

        event_dict["timestamp"] = time.time()
        return event_dict

    registry.register(
        name="timestamp",
        value=timestamp_processor,
        dimension=ComponentCategory.PROCESSOR.value,
        metadata={"priority": 100, "stage": "pre_format"},
        replace=True,  # Allow replacement for test scenarios
    )

    # Register configuration schemas
    from provide.foundation.config.bootstrap import discover_and_register_configs

    discover_and_register_configs()

    from provide.foundation.hub.foundation import get_foundation_logger

    get_foundation_logger().debug("Foundation bootstrap completed with registry components")


# Bootstrap will happen lazily on first hub access to avoid circular imports
# bootstrap_foundation()


__all__ = [
    "ComponentCategory",
    # Core classes
    "ComponentInfo",
    "ComponentLifecycle",
    # Bootstrap and testing
    "bootstrap_foundation",
    # Health and schema
    "check_component_health",
    "cleanup_all_components",
    "discover_components",
    "execute_error_handlers",
    "get_component_config_schema",
    # Registry access
    "get_component_registry",
    "get_config_chain",
    "get_handlers_for_exception",
    "get_or_initialize_component",
    "get_processor_pipeline",
    "get_processors_for_stage",
    "initialize_all_async_components",
    "initialize_async_component",
    "load_all_configs",
    "load_config_from_registry",
    "resolve_component_dependencies",
    # Re-exported from specialized modules
    "resolve_config_value",
]

# 🧱🏗️🔚
