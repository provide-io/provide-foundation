"""Type definitions for the hub module."""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Protocol, TypeAlias

ComponentType: TypeAlias = type[Any]
CommandType: TypeAlias = Callable[..., Any]
RegistryKey: TypeAlias = tuple[str, ...]


class RegistryDimension(str, Enum):
    """Standard registry dimensions."""
    
    COMPONENT = "component"
    COMMAND = "command"
    RESOURCE = "resource"
    DATA_SOURCE = "data_source"
    PROVIDER = "provider"
    PLUGIN = "plugin"
    EXTENSION = "extension"


@dataclass(frozen=True, slots=True)
class RegistryEntry:
    """A single entry in the registry."""
    
    name: str
    dimension: RegistryDimension | str
    value: Any
    metadata: dict[str, Any] = field(default_factory=dict)
    
    @property
    def key(self) -> RegistryKey:
        """Get the registry key for this entry."""
        return (str(self.dimension), self.name)


class Registrable(Protocol):
    """Protocol for objects that can be registered."""
    
    __registry_name__: str
    __registry_dimension__: RegistryDimension | str
    __registry_metadata__: dict[str, Any]


@dataclass(frozen=True, slots=True)
class CommandInfo:
    """Information about a registered CLI command."""
    
    name: str
    func: Callable[..., Any]
    description: str | None = None
    aliases: list[str] = field(default_factory=list)
    hidden: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class ComponentInfo:
    """Information about a registered component."""
    
    name: str
    component_class: type[Any]
    dimension: RegistryDimension | str
    description: str | None = None
    version: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)