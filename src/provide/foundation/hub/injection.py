from __future__ import annotations

import inspect
from typing import Any, TypeVar, get_type_hints

from provide.foundation.errors.config import ValidationError
from provide.foundation.errors.resources import NotFoundError

"""Dependency injection support for the Hub.

This module provides tools for explicit dependency injection patterns,
complementing the existing Service Locator pattern. This allows users
to choose the pattern that best fits their needs:

- Service Locator: Simple, global access (get_hub())
- Dependency Injection: Explicit, testable dependencies

Example:
    >>> from provide.foundation.hub import injectable
    >>>
    >>> @injectable
    >>> class MyService:
    ...     def __init__(self, db: DatabaseClient, logger: Logger):
    ...         self.db = db
    ...         self.logger = logger
    >>>
    >>> # In main.py (Composition Root)
    >>> hub = Hub()
    >>> hub.register(DatabaseClient, db_instance)
    >>> hub.register(Logger, logger_instance)
    >>> service = hub.resolve(MyService)  # Auto-injects
"""

T = TypeVar("T")

# Marker for injectable classes
_INJECTABLE_MARKER = "__provide_injectable__"


def injectable(cls: type[T]) -> type[T]:
    """Mark a class as injectable for dependency injection.

    This decorator indicates that the class follows DI patterns and
    can be automatically instantiated by the Hub's resolve() method.

    The decorator:
    - Validates that __init__ has type hints for all parameters
    - Marks the class as injectable for documentation purposes
    - Does not modify the class behavior (zero runtime overhead)

    Args:
        cls: Class to mark as injectable

    Returns:
        The same class, marked as injectable

    Raises:
        ValidationError: If __init__ lacks proper type hints

    Example:
        >>> @injectable
        >>> class UserService:
        ...     def __init__(self, db: Database, cache: Cache):
        ...         self.db = db
        ...         self.cache = cache
    """
    # Validate __init__ signature
    if not hasattr(cls, "__init__"):
        raise ValidationError(
            f"Injectable class {cls.__name__} must have __init__ method",
            code="INJECTABLE_NO_INIT",
            class_name=cls.__name__,
        )

    # Get type hints for __init__
    try:
        hints = get_type_hints(cls.__init__)
    except Exception as e:
        raise ValidationError(
            f"Failed to get type hints for {cls.__name__}.__init__: {e}",
            code="INJECTABLE_TYPE_HINT_ERROR",
            class_name=cls.__name__,
            cause=e,
        ) from e

    # Get signature to check for untyped parameters
    sig = inspect.signature(cls.__init__)
    params = list(sig.parameters.values())[1:]  # Skip 'self'

    # Check each parameter has a type hint (excluding *args, **kwargs)
    untyped_params = []
    for param in params:
        if param.kind in (inspect.Parameter.VAR_POSITIONAL, inspect.Parameter.VAR_KEYWORD):
            continue  # *args and **kwargs are fine without hints
        if param.name not in hints:
            untyped_params.append(param.name)

    if untyped_params:
        raise ValidationError(
            f"Injectable class {cls.__name__}.__init__ has untyped parameters: {untyped_params}. "
            "All constructor parameters must have type hints for dependency injection.",
            code="INJECTABLE_UNTYPED_PARAMS",
            class_name=cls.__name__,
            untyped_params=untyped_params,
        )

    # Mark as injectable (for introspection/documentation)
    setattr(cls, _INJECTABLE_MARKER, True)

    return cls


def is_injectable(cls: type[Any]) -> bool:
    """Check if a class is marked as injectable.

    Args:
        cls: Class to check

    Returns:
        True if class is marked with @injectable decorator
    """
    return getattr(cls, _INJECTABLE_MARKER, False)


def resolve_dependencies(
    cls: type[T],
    registry: Any,  # Registry type
    allow_missing: bool = False,
) -> dict[str, Any]:
    """Resolve constructor dependencies from registry.

    Inspects the class __init__ signature and attempts to resolve
    each typed parameter from the registry.

    Args:
        cls: Class to resolve dependencies for
        registry: Registry containing registered dependencies
        allow_missing: If True, skip missing dependencies instead of raising

    Returns:
        Dictionary mapping parameter names to resolved instances

    Raises:
        NotFoundError: If a required dependency is not registered
        ValidationError: If dependency resolution fails

    Example:
        >>> deps = resolve_dependencies(MyService, hub._component_registry)
        >>> {'db': <DatabaseClient>, 'logger': <Logger>}
    """
    # Get type hints for __init__
    try:
        hints = get_type_hints(cls.__init__)
    except Exception as e:
        raise ValidationError(
            f"Failed to get type hints for {cls.__name__}.__init__: {e}",
            code="RESOLVE_TYPE_HINT_ERROR",
            class_name=cls.__name__,
            cause=e,
        ) from e

    # Get signature
    sig = inspect.signature(cls.__init__)
    params = list(sig.parameters.values())[1:]  # Skip 'self'

    resolved = {}
    missing = []

    for param in params:
        # Skip *args and **kwargs
        if param.kind in (inspect.Parameter.VAR_POSITIONAL, inspect.Parameter.VAR_KEYWORD):
            continue

        # Skip parameters with defaults
        if param.default != inspect.Parameter.empty:
            continue

        # Get type hint
        param_type = hints.get(param.name)
        if param_type is None:
            if allow_missing:
                continue
            raise ValidationError(
                f"Parameter '{param.name}' of {cls.__name__}.__init__ has no type hint",
                code="RESOLVE_NO_TYPE_HINT",
                class_name=cls.__name__,
                param_name=param.name,
            )

        # Try to resolve from registry by type
        # Strategy: Look for registered instance of this type
        instance = registry.get_by_type(param_type)

        if instance is None:
            if allow_missing:
                missing.append(param.name)
                continue
            raise NotFoundError(
                f"Dependency '{param_type.__name__}' required by {cls.__name__} not found in registry",
                code="RESOLVE_DEPENDENCY_NOT_FOUND",
                class_name=cls.__name__,
                param_name=param.name,
                param_type=param_type.__name__,
            )

        resolved[param.name] = instance

    return resolved


def register(
    registry: Any,
    type_hint: type[T],
    instance: T,
    name: str | None = None,
) -> None:
    """Register a dependency in the registry by type.

    This is a convenience function for type-based registration,
    which is essential for dependency injection.

    Args:
        registry: Registry to register in
        type_hint: Type to register under
        instance: Instance to register
        name: Optional name (defaults to type name)
    """
    registration_name = name or type_hint.__name__
    registry.register_type(type_hint, instance, name=registration_name)


def create_instance(
    cls: type[T],
    registry: Any,
    **overrides: Any,
) -> T:
    """Create an instance with dependency injection.

    Resolves constructor dependencies from the registry and
    instantiates the class. Allows overriding specific dependencies.

    Args:
        cls: Class to instantiate
        registry: Registry containing dependencies
        **overrides: Explicitly provided dependencies (override registry)

    Returns:
        New instance of cls

    Example:
        >>> service = create_instance(MyService, hub._component_registry)
        >>> # Or with overrides:
        >>> service = create_instance(
        ...     MyService,
        ...     hub._component_registry,
        ...     logger=custom_logger
        ... )
    """
    # Resolve dependencies
    resolved = resolve_dependencies(cls, registry, allow_missing=True)

    # Apply overrides
    resolved.update(overrides)

    # Create instance
    try:
        return cls(**resolved)
    except Exception as e:
        raise ValidationError(
            f"Failed to create instance of {cls.__name__}: {e}",
            code="CREATE_INSTANCE_ERROR",
            class_name=cls.__name__,
            cause=e,
        ) from e


__all__ = [
    "create_instance",
    "injectable",
    "is_injectable",
    "register",
    "resolve_dependencies",
]
