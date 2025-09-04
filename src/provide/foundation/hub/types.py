"""Type definitions for the hub module."""

from typing import Any, Protocol

from attrs import define, field


@define(frozen=True, slots=True)
class RegistryEntry:
    """A single entry in the registry."""

    name: str
    dimension: str
    value: Any
    metadata: dict[str, Any] = field(factory=lambda: {})

    @property
    def key(self) -> tuple[str, str]:
        """Get the registry key for this entry."""
        return (self.dimension, self.name)


class Registrable(Protocol):
    """Protocol for objects that can be registered."""

    __registry_name__: str
    __registry_dimension__: str
    __registry_metadata__: dict[str, Any]
