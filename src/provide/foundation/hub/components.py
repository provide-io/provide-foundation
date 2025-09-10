"""
Registry-based component management system for Foundation.

This module implements Foundation's end-state architecture where all internal
components are managed through the Hub registry system. Provides centralized
component discovery, lifecycle management, and dependency resolution.
"""

import threading
from enum import Enum
from typing import Any, Protocol

from attrs import define, field

from provide.foundation.errors.decorators import with_error_handling
from provide.foundation.hub.registry import Registry
from provide.foundation.logger import get_logger

log = get_logger(__name__)


@define(frozen=True, slots=True)
class ComponentInfo:
    """Information about a registered component."""

    name: str = field()
    component_class: type[Any] = field()
    dimension: str = field(default="component")
    version: str | None = field(default=None)
    description: str | None = field(default=None)
    author: str | None = field(default=None)
    tags: list[str] = field(factory=lambda: [])
    metadata: dict[str, Any] = field(factory=lambda: {})


class ComponentCategory(Enum):
    """Predefined component categories for Foundation."""

    CONFIG_SOURCE = "config_source"
    PROCESSOR = "processor"
    ERROR_HANDLER = "error_handler"
    FORMATTER = "formatter"
    FILTER = "filter"
    TRANSPORT = "transport"
    TRANSPORT_MIDDLEWARE = "transport.middleware"
    TRANSPORT_AUTH = "transport.auth"
    TRANSPORT_CACHE = "transport.cache"
    EVENT_SET = "eventset"


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
_registry_lock = threading.RLock()
_initialized_components: dict[tuple[str, str], Any] = {}


def get_component_registry() -> Registry:
    """Get the global component registry."""
    return _component_registry


@with_error_handling(
    fallback={"status": "error"},
    context_provider=lambda: {"function": "check_component_health", "module": "hub.components"}
)
def check_component_health(name: str, dimension: str) -> dict[str, Any]:
    """Check component health status."""
    with _registry_lock:
        component = _component_registry.get(name, dimension)

        if not component:
            return {"status": "not_found"}

        entry = _component_registry.get_entry(name, dimension)
        if not entry.metadata.get("supports_health_check", False):
            return {"status": "no_health_check"}

        if hasattr(component, "health_check"):
            try:
                return component.health_check()
            except Exception as e:
                return {"status": "error", "error": str(e)}

        return {"status": "unknown"}


def get_component_config_schema(name: str, dimension: str) -> dict[str, Any] | None:
    """Get component configuration schema."""
    with _registry_lock:
        entry = _component_registry.get_entry(name, dimension)

        if not entry:
            return None

        return entry.metadata.get("config_schema")


def bootstrap_foundation() -> None:
    """Bootstrap Foundation with core registry components."""
    registry = get_component_registry()

    # Register core processors
    def timestamp_processor(logger, method_name, event_dict):
        import time

        event_dict["timestamp"] = time.time()
        return event_dict

    registry.register(
        name="timestamp",
        value=timestamp_processor,
        dimension=ComponentCategory.PROCESSOR.value,
        metadata={"priority": 100, "stage": "pre_format"},
    )

    log.debug("Foundation bootstrap completed with registry components")


def reset_registry_for_tests() -> None:
    """Reset registry state for testing."""
    global _initialized_components
    with _registry_lock:
        _component_registry.clear()
        _initialized_components.clear()


# Import and re-export functions from specialized modules
from provide.foundation.hub.config import (
    resolve_config_value,
    get_config_chain,
    load_all_configs,
    load_config_from_registry,
)

from provide.foundation.hub.handlers import (
    get_handlers_for_exception,
    execute_error_handlers,
)

from provide.foundation.hub.lifecycle import (
    get_or_initialize_component,
    initialize_async_component,
    cleanup_all_components,
    initialize_all_async_components,
)

from provide.foundation.hub.processors import (
    get_processor_pipeline,
    get_processors_for_stage,
)

from provide.foundation.hub.discovery import (
    resolve_component_dependencies,
    discover_components,
)


# Bootstrap on module import
bootstrap_foundation()


__all__ = [
    # Core classes
    "ComponentInfo",
    "ComponentCategory", 
    "ComponentLifecycle",
    # Registry access
    "get_component_registry",
    # Health and schema
    "check_component_health",
    "get_component_config_schema",
    # Bootstrap and testing
    "bootstrap_foundation",
    "reset_registry_for_tests",
    # Re-exported from specialized modules
    "resolve_config_value",
    "get_config_chain",
    "load_all_configs",
    "load_config_from_registry",
    "get_handlers_for_exception", 
    "execute_error_handlers",
    "get_or_initialize_component",
    "initialize_async_component",
    "cleanup_all_components",
    "initialize_all_async_components",
    "get_processor_pipeline",
    "get_processors_for_stage",
    "resolve_component_dependencies",
    "discover_components",
]