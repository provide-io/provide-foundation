"""Centralized attrs imports and utilities for provide.foundation.

This module provides a single source of truth for all attrs functionality,
making it easier to maintain and potentially migrate in the future.
"""

from __future__ import annotations

from typing import Any, Callable

# Re-export all commonly used attrs components
from attrs import (
    NOTHING,
    Attribute,
    Factory,
    define,
    field,
    fields,
    validators,
)

# Type aliases for better documentation
AttrsField = Attribute[Any]
AttrsValidator = Callable[[Any, Attribute[Any], Any], None]

# Custom field helpers for common patterns

def private_field(*, default: Any = NOTHING, factory: Any = NOTHING) -> Any:
    """Create a private field that's not included in init or repr.

    Args:
        default: Default value for the field
        factory: Factory function for the field

    Returns:
        Field configured as init=False, repr=False
    """
    kwargs = {"init": False, "repr": False}
    if default is not NOTHING:
        kwargs["default"] = default
    elif factory is not NOTHING:
        kwargs["factory"] = factory
    return field(**kwargs)


def factory_field(factory_func: Callable[[], Any], *, repr: bool = True) -> Any:
    """Create a field with a default factory function.

    Args:
        factory_func: Function to call to create default value
        repr: Whether to include in repr (default: True)

    Returns:
        Field with the specified factory
    """
    return field(default_factory=factory_func, repr=repr)


def kw_only_field(
    *,
    default: Any = NOTHING,
    factory: Any = NOTHING,
    validator: AttrsValidator | list[AttrsValidator] | None = None
) -> Any:
    """Create a keyword-only field.

    Args:
        default: Default value for the field
        factory: Factory function for the field
        validator: Validator(s) for the field

    Returns:
        Field configured as kw_only=True
    """
    kwargs = {"kw_only": True}
    if default is not NOTHING:
        kwargs["default"] = default
    elif factory is not NOTHING:
        kwargs["factory"] = factory
    if validator is not None:
        kwargs["validator"] = validator
    return field(**kwargs)


# Export everything for easy importing
__all__ = [
    # Core attrs components
    "define",
    "field",
    "fields",
    "validators",
    "Factory",
    "NOTHING",
    "Attribute",
    # Type aliases
    "AttrsField",
    "AttrsValidator",
    # Custom helpers
    "private_field",
    "factory_field",
    "kw_only_field",
]