"""Registration decorators for components and commands."""

from functools import wraps
from typing import Any, Callable, TypeVar

import structlog

from .registry import Registry
from .types import CommandInfo, ComponentInfo, RegistryDimension

log = structlog.get_logger(__name__)

T = TypeVar("T")
F = TypeVar("F", bound=Callable[..., Any])

_global_registry = Registry()


def register_component(
    name: str | None = None,
    dimension: RegistryDimension | str = RegistryDimension.COMPONENT,
    description: str | None = None,
    version: str | None = None,
    metadata: dict[str, Any] | None = None,
    registry: Registry | None = None,
) -> Callable[[type[T]], type[T]]:
    """
    Decorator to register a component class.
    
    Example:
        @register_component("my_resource", dimension=RegistryDimension.RESOURCE)
        class MyResource:
            pass
    """
    def decorator(cls: type[T]) -> type[T]:
        reg = registry or _global_registry
        component_name = name or cls.__name__
        
        info = ComponentInfo(
            name=component_name,
            component_class=cls,
            dimension=dimension,
            description=description or cls.__doc__,
            version=version,
            metadata=metadata or {},
        )
        
        reg.register(
            name=component_name,
            value=cls,
            dimension=dimension,
            metadata={
                "info": info,
                "description": description or cls.__doc__,
                "version": version,
                **(metadata or {}),
            },
        )
        
        cls.__registry_name__ = component_name
        cls.__registry_dimension__ = dimension
        cls.__registry_metadata__ = metadata or {}
        
        log.debug(
            "Registered component",
            name=component_name,
            dimension=str(dimension),
            class_name=cls.__name__,
        )
        
        return cls
    
    return decorator


def register_command(
    name: str | None = None,
    description: str | None = None,
    aliases: list[str] | None = None,
    hidden: bool = False,
    metadata: dict[str, Any] | None = None,
    registry: Registry | None = None,
) -> Callable[[F], F]:
    """
    Decorator to register a CLI command function.
    
    Example:
        @register_command("init", aliases=["initialize", "setup"])
        def init_command(ctx):
            pass
    """
    def decorator(func: F) -> F:
        reg = registry or _global_registry
        command_name = name or func.__name__.replace("_", "-")
        
        info = CommandInfo(
            name=command_name,
            func=func,
            description=description or func.__doc__,
            aliases=aliases or [],
            hidden=hidden,
            metadata=metadata or {},
        )
        
        reg.register(
            name=command_name,
            value=func,
            dimension=RegistryDimension.COMMAND,
            metadata={
                "info": info,
                "description": description or func.__doc__,
                "aliases": aliases or [],
                "hidden": hidden,
                **(metadata or {}),
            },
            aliases=aliases,
        )
        
        func.__registry_name__ = command_name
        func.__registry_dimension__ = RegistryDimension.COMMAND
        func.__registry_metadata__ = metadata or {}
        
        log.debug(
            "Registered command",
            name=command_name,
            aliases=aliases,
            hidden=hidden,
        )
        
        return func
    
    return decorator


def register(
    name: str | None = None,
    dimension: RegistryDimension | str = RegistryDimension.COMPONENT,
    metadata: dict[str, Any] | None = None,
    aliases: list[str] | None = None,
    registry: Registry | None = None,
) -> Callable[[T], T]:
    """
    Generic registration decorator for any type.
    
    Example:
        @register("my_plugin", dimension=RegistryDimension.PLUGIN)
        class MyPlugin:
            pass
            
        @register("helper", dimension="utility")
        def helper_function():
            pass
    """
    def decorator(obj: T) -> T:
        reg = registry or _global_registry
        
        if callable(obj) and not isinstance(obj, type):
            obj_name = name or getattr(obj, "__name__", str(obj))
        elif isinstance(obj, type):
            obj_name = name or obj.__name__
        else:
            obj_name = name or str(obj)
        
        reg.register(
            name=obj_name,
            value=obj,
            dimension=dimension,
            metadata=metadata or {},
            aliases=aliases,
        )
        
        if hasattr(obj, "__dict__"):
            obj.__registry_name__ = obj_name
            obj.__registry_dimension__ = dimension
            obj.__registry_metadata__ = metadata or {}
        
        log.debug(
            "Registered object",
            name=obj_name,
            dimension=str(dimension),
            type=type(obj).__name__,
        )
        
        return obj
    
    return decorator


def discover_entry_points(
    group: str,
    dimension: RegistryDimension | str = RegistryDimension.PLUGIN,
    registry: Registry | None = None,
) -> dict[str, Any]:
    """
    Discover and register components from entry points.
    
    Args:
        group: Entry point group name (e.g., "pyvider.resources")
        dimension: Dimension to register discovered items under
        registry: Registry to use (defaults to global)
        
    Returns:
        Dictionary of discovered items by name
    """
    try:
        from importlib.metadata import entry_points
    except ImportError:
        from importlib_metadata import entry_points
    
    reg = registry or _global_registry
    discovered = {}
    
    eps = entry_points()
    if hasattr(eps, "select"):
        group_eps = eps.select(group=group)
    else:
        group_eps = eps.get(group, [])
    
    for ep in group_eps:
        try:
            obj = ep.load()
            reg.register(
                name=ep.name,
                value=obj,
                dimension=dimension,
                metadata={
                    "entry_point": ep.name,
                    "module": ep.module,
                    "attr": ep.attr,
                    "group": group,
                },
            )
            discovered[ep.name] = obj
            
            log.debug(
                "Discovered entry point",
                name=ep.name,
                group=group,
                dimension=str(dimension),
            )
        except Exception as e:
            log.warning(
                "Failed to load entry point",
                name=ep.name,
                group=group,
                error=str(e),
            )
    
    return discovered


def get_global_registry() -> Registry:
    """Get the global registry instance."""
    return _global_registry