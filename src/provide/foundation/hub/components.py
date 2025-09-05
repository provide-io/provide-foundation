"""
Registry-based component management system for Foundation.

This module implements Foundation's end-state architecture where all internal
components are managed through the Hub registry system. Provides centralized
component discovery, lifecycle management, and dependency resolution.
"""

import asyncio
from collections.abc import Callable, Iterator
from enum import Enum
import inspect
import threading
from typing import Any, Protocol, TypeVar

from provide.foundation.config.base import BaseConfig
from provide.foundation.hub.registry import Registry, RegistryEntry
from provide.foundation.logger import get_logger
from provide.foundation.logger.emoji_matrix import EmojiSet

log = get_logger(__name__)

T = TypeVar("T")


class ComponentCategory(Enum):
    """Predefined component categories for Foundation."""
    
    EMOJI_SET = "emoji_set"
    CONFIG_SOURCE = "config_source" 
    PROCESSOR = "processor"
    ERROR_HANDLER = "error_handler"
    SEMANTIC_LAYER = "semantic_layer"
    FORMATTER = "formatter"
    FILTER = "filter"


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


@overload
def register_component(
    name: str | None = None,
    *,
    dimension: str = "component",
    version: str | None = None,
    description: str | None = None,
    author: str | None = None,
    tags: list[str] | None = None,
    replace: bool = False,
    registry: Registry | None = None,
) -> type[T]: ...


@overload
def register_component(
    cls: type[T],
    /,
) -> type[T]: ...


def register_component(
    name_or_cls: str | type[T] | None = None,
    *,
    dimension: str = "component",
    version: str | None = None,
    description: str | None = None,
    author: str | None = None,
    tags: list[str] | None = None,
    replace: bool = False,
    registry: Registry | None = None,
) -> Any:
    """
    Register a component class in the hub.

    Can be used as a decorator with or without arguments:

        @register_component
        class MyComponent:
            pass

        @register_component("custom_name", version="1.0.0")
        class MyComponent:
            pass

    Args:
        name_or_cls: Component name or class (when used without parens)
        dimension: Registry dimension (default: "component")
        version: Component version
        description: Component description
        author: Component author
        tags: List of tags for categorization
        replace: Whether to replace existing registration
        registry: Custom registry (defaults to global)

    Returns:
        Decorator function or decorated class
    """
    # Handle @register_component (without parens)
    if isinstance(name_or_cls, type):
        cls = name_or_cls
        return _register_component_class(
            cls,
            name=None,
            dimension=dimension,
            version=version,
            description=description,
            author=author,
            tags=tags,
            replace=replace,
            registry=registry,
        )

    # Handle @register_component(...) (with arguments)
    def decorator(cls: type[T]) -> type[T]:
        return _register_component_class(
            cls,
            name=name_or_cls,
            dimension=dimension,
            version=version,
            description=description,
            author=author,
            tags=tags,
            replace=replace,
            registry=registry,
        )

    return decorator


def _register_component_class(
    cls: type[T],
    *,
    name: str | None = None,
    dimension: str = "component",
    version: str | None = None,
    description: str | None = None,
    author: str | None = None,
    tags: list[str] | None = None,
    replace: bool = False,
    registry: Registry | None = None,
) -> type[T]:
    """Internal function to register a component class."""
    reg = registry or _component_registry
    component_name = name or cls.__name__

    # Create component info
    info = ComponentInfo(
        name=component_name,
        component_class=cls,
        dimension=dimension,
        version=version,
        description=description or cls.__doc__,
        author=author,
        tags=tags or [],
        metadata={},
    )

    # Register in the registry
    reg.register(
        name=component_name,
        value=cls,
        dimension=dimension,
        metadata={
            "info": info,
            "version": version,
            "description": description or cls.__doc__,
            "author": author,
            "tags": tags or [],
        },
        replace=replace,
    )

    # Add metadata to the class
    cls.__registry_name__ = component_name
    cls.__registry_dimension__ = dimension
    cls.__registry_info__ = info

    log.info(
        "Registered component",
        name=component_name,
        dimension=dimension,
        version=version,
        class_name=cls.__name__,
    )

    return cls


def discover_components(
    group: str,
    dimension: str = "component",
    registry: Registry | None = None,
) -> dict[str, type[Any]]:
    """
    Discover and register components from entry points.

    This function uses Python's entry points mechanism to discover
    components installed by other packages.

    Args:
        group: Entry point group name (e.g., "provide.components")
        dimension: Registry dimension for discovered components
        registry: Custom registry (defaults to global)

    Returns:
        Dictionary mapping component names to classes

    Example:
        >>> discovered = discover_components("provide.resources")
        >>> for name, cls in discovered.items():
        >>>     print(f"Found {name}: {cls}")
    """
    try:
        from importlib.metadata import entry_points
    except ImportError:
        from importlib_metadata import entry_points

    reg = registry or _component_registry
    discovered: dict[str, type[Any]] = {}

    # Get entry points for the group
    eps = entry_points()
    if hasattr(eps, "select"):
        # Python 3.10+
        group_eps = eps.select(group=group)
    else:
        # Python 3.9
        group_eps = eps.get(group, [])

    for ep in group_eps:
        try:
            # Load the entry point
            obj = ep.load()

            # Register it
            reg.register(
                name=ep.name,
                value=obj,
                dimension=dimension,
                metadata={
                    "entry_point": ep.name,
                    "module": ep.module if hasattr(ep, "module") else None,
                    "group": group,
                    "discovered": True,
                },
            )

            discovered[ep.name] = obj

            log.debug(
                "Discovered component from entry point",
                name=ep.name,
                group=group,
                dimension=dimension,
            )

        except Exception as e:
            log.warning(
                "Failed to load entry point",
                name=ep.name,
                group=group,
                error=str(e),
            )

    log.info(
        "Component discovery complete",
        group=group,
        discovered_count=len(discovered),
    )

    return discovered


def get_component_registry() -> Registry:
    """Get the global component registry."""
    return _component_registry
