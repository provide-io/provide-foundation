"""Type definitions for the hub module."""

from typing import Any, Protocol

# Import RegistryEntry from its canonical location


class Registrable(Protocol):
    """Protocol for objects that can be registered."""

    __registry_name__: str
    __registry_dimension__: str
    __registry_metadata__: dict[str, Any]
