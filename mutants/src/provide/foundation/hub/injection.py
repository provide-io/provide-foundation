# provide/foundation/hub/injection.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

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
from inspect import signature as _mutmut_signature
from typing import Annotated
from typing import Callable
from typing import ClassVar


MutantDict = Annotated[dict[str, Callable], "Mutant"]


def _mutmut_trampoline(orig, mutants, call_args, call_kwargs, self_arg = None):
    """Forward call to original or mutated function, depending on the environment"""
    import os
    mutant_under_test = os.environ['MUTANT_UNDER_TEST']
    if mutant_under_test == 'fail':
        from mutmut.__main__ import MutmutProgrammaticFailException
        raise MutmutProgrammaticFailException('Failed programmatically')      
    elif mutant_under_test == 'stats':
        from mutmut.__main__ import record_trampoline_hit
        record_trampoline_hit(orig.__module__ + '.' + orig.__name__)
        result = orig(*call_args, **call_kwargs)
        return result
    prefix = orig.__module__ + '.' + orig.__name__ + '__mutmut_'
    if not mutant_under_test.startswith(prefix):
        result = orig(*call_args, **call_kwargs)
        return result
    mutant_name = mutant_under_test.rpartition('.')[-1]
    if self_arg:
        # call to a class method where self is not bound
        result = mutants[mutant_name](self_arg, *call_args, **call_kwargs)
    else:
        result = mutants[mutant_name](*call_args, **call_kwargs)
    return result


def x_injectable__mutmut_orig(cls: type[T]) -> type[T]:
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
    # Check if class has custom __init__ (not inherited from object)
    if "__init__" not in cls.__dict__:
        raise ValidationError(
            f"Injectable class {cls.__name__} must define its own __init__ method",
            code="INJECTABLE_NO_INIT",
            class_name=cls.__name__,
        )

    # Get type hints for __init__
    try:
        # Use localns to resolve forward references within the class's module
        import sys

        module = sys.modules.get(cls.__module__)
        localns = vars(module) if module else {}
        get_type_hints(cls.__init__, globalns=None, localns=localns)
    except NameError:
        # Forward reference couldn't be resolved - that's okay for now
        # The actual resolution will happen at runtime
        pass
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
        # Check if parameter has annotation in signature
        if param.annotation == inspect.Parameter.empty:
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


def x_injectable__mutmut_1(cls: type[T]) -> type[T]:
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
    # Check if class has custom __init__ (not inherited from object)
    if "XX__init__XX" not in cls.__dict__:
        raise ValidationError(
            f"Injectable class {cls.__name__} must define its own __init__ method",
            code="INJECTABLE_NO_INIT",
            class_name=cls.__name__,
        )

    # Get type hints for __init__
    try:
        # Use localns to resolve forward references within the class's module
        import sys

        module = sys.modules.get(cls.__module__)
        localns = vars(module) if module else {}
        get_type_hints(cls.__init__, globalns=None, localns=localns)
    except NameError:
        # Forward reference couldn't be resolved - that's okay for now
        # The actual resolution will happen at runtime
        pass
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
        # Check if parameter has annotation in signature
        if param.annotation == inspect.Parameter.empty:
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


def x_injectable__mutmut_2(cls: type[T]) -> type[T]:
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
    # Check if class has custom __init__ (not inherited from object)
    if "__INIT__" not in cls.__dict__:
        raise ValidationError(
            f"Injectable class {cls.__name__} must define its own __init__ method",
            code="INJECTABLE_NO_INIT",
            class_name=cls.__name__,
        )

    # Get type hints for __init__
    try:
        # Use localns to resolve forward references within the class's module
        import sys

        module = sys.modules.get(cls.__module__)
        localns = vars(module) if module else {}
        get_type_hints(cls.__init__, globalns=None, localns=localns)
    except NameError:
        # Forward reference couldn't be resolved - that's okay for now
        # The actual resolution will happen at runtime
        pass
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
        # Check if parameter has annotation in signature
        if param.annotation == inspect.Parameter.empty:
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


def x_injectable__mutmut_3(cls: type[T]) -> type[T]:
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
    # Check if class has custom __init__ (not inherited from object)
    if "__init__" in cls.__dict__:
        raise ValidationError(
            f"Injectable class {cls.__name__} must define its own __init__ method",
            code="INJECTABLE_NO_INIT",
            class_name=cls.__name__,
        )

    # Get type hints for __init__
    try:
        # Use localns to resolve forward references within the class's module
        import sys

        module = sys.modules.get(cls.__module__)
        localns = vars(module) if module else {}
        get_type_hints(cls.__init__, globalns=None, localns=localns)
    except NameError:
        # Forward reference couldn't be resolved - that's okay for now
        # The actual resolution will happen at runtime
        pass
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
        # Check if parameter has annotation in signature
        if param.annotation == inspect.Parameter.empty:
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


def x_injectable__mutmut_4(cls: type[T]) -> type[T]:
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
    # Check if class has custom __init__ (not inherited from object)
    if "__init__" not in cls.__dict__:
        raise ValidationError(
            None,
            code="INJECTABLE_NO_INIT",
            class_name=cls.__name__,
        )

    # Get type hints for __init__
    try:
        # Use localns to resolve forward references within the class's module
        import sys

        module = sys.modules.get(cls.__module__)
        localns = vars(module) if module else {}
        get_type_hints(cls.__init__, globalns=None, localns=localns)
    except NameError:
        # Forward reference couldn't be resolved - that's okay for now
        # The actual resolution will happen at runtime
        pass
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
        # Check if parameter has annotation in signature
        if param.annotation == inspect.Parameter.empty:
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


def x_injectable__mutmut_5(cls: type[T]) -> type[T]:
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
    # Check if class has custom __init__ (not inherited from object)
    if "__init__" not in cls.__dict__:
        raise ValidationError(
            f"Injectable class {cls.__name__} must define its own __init__ method",
            code=None,
            class_name=cls.__name__,
        )

    # Get type hints for __init__
    try:
        # Use localns to resolve forward references within the class's module
        import sys

        module = sys.modules.get(cls.__module__)
        localns = vars(module) if module else {}
        get_type_hints(cls.__init__, globalns=None, localns=localns)
    except NameError:
        # Forward reference couldn't be resolved - that's okay for now
        # The actual resolution will happen at runtime
        pass
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
        # Check if parameter has annotation in signature
        if param.annotation == inspect.Parameter.empty:
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


def x_injectable__mutmut_6(cls: type[T]) -> type[T]:
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
    # Check if class has custom __init__ (not inherited from object)
    if "__init__" not in cls.__dict__:
        raise ValidationError(
            f"Injectable class {cls.__name__} must define its own __init__ method",
            code="INJECTABLE_NO_INIT",
            class_name=None,
        )

    # Get type hints for __init__
    try:
        # Use localns to resolve forward references within the class's module
        import sys

        module = sys.modules.get(cls.__module__)
        localns = vars(module) if module else {}
        get_type_hints(cls.__init__, globalns=None, localns=localns)
    except NameError:
        # Forward reference couldn't be resolved - that's okay for now
        # The actual resolution will happen at runtime
        pass
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
        # Check if parameter has annotation in signature
        if param.annotation == inspect.Parameter.empty:
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


def x_injectable__mutmut_7(cls: type[T]) -> type[T]:
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
    # Check if class has custom __init__ (not inherited from object)
    if "__init__" not in cls.__dict__:
        raise ValidationError(
            code="INJECTABLE_NO_INIT",
            class_name=cls.__name__,
        )

    # Get type hints for __init__
    try:
        # Use localns to resolve forward references within the class's module
        import sys

        module = sys.modules.get(cls.__module__)
        localns = vars(module) if module else {}
        get_type_hints(cls.__init__, globalns=None, localns=localns)
    except NameError:
        # Forward reference couldn't be resolved - that's okay for now
        # The actual resolution will happen at runtime
        pass
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
        # Check if parameter has annotation in signature
        if param.annotation == inspect.Parameter.empty:
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


def x_injectable__mutmut_8(cls: type[T]) -> type[T]:
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
    # Check if class has custom __init__ (not inherited from object)
    if "__init__" not in cls.__dict__:
        raise ValidationError(
            f"Injectable class {cls.__name__} must define its own __init__ method",
            class_name=cls.__name__,
        )

    # Get type hints for __init__
    try:
        # Use localns to resolve forward references within the class's module
        import sys

        module = sys.modules.get(cls.__module__)
        localns = vars(module) if module else {}
        get_type_hints(cls.__init__, globalns=None, localns=localns)
    except NameError:
        # Forward reference couldn't be resolved - that's okay for now
        # The actual resolution will happen at runtime
        pass
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
        # Check if parameter has annotation in signature
        if param.annotation == inspect.Parameter.empty:
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


def x_injectable__mutmut_9(cls: type[T]) -> type[T]:
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
    # Check if class has custom __init__ (not inherited from object)
    if "__init__" not in cls.__dict__:
        raise ValidationError(
            f"Injectable class {cls.__name__} must define its own __init__ method",
            code="INJECTABLE_NO_INIT",
            )

    # Get type hints for __init__
    try:
        # Use localns to resolve forward references within the class's module
        import sys

        module = sys.modules.get(cls.__module__)
        localns = vars(module) if module else {}
        get_type_hints(cls.__init__, globalns=None, localns=localns)
    except NameError:
        # Forward reference couldn't be resolved - that's okay for now
        # The actual resolution will happen at runtime
        pass
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
        # Check if parameter has annotation in signature
        if param.annotation == inspect.Parameter.empty:
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


def x_injectable__mutmut_10(cls: type[T]) -> type[T]:
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
    # Check if class has custom __init__ (not inherited from object)
    if "__init__" not in cls.__dict__:
        raise ValidationError(
            f"Injectable class {cls.__name__} must define its own __init__ method",
            code="XXINJECTABLE_NO_INITXX",
            class_name=cls.__name__,
        )

    # Get type hints for __init__
    try:
        # Use localns to resolve forward references within the class's module
        import sys

        module = sys.modules.get(cls.__module__)
        localns = vars(module) if module else {}
        get_type_hints(cls.__init__, globalns=None, localns=localns)
    except NameError:
        # Forward reference couldn't be resolved - that's okay for now
        # The actual resolution will happen at runtime
        pass
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
        # Check if parameter has annotation in signature
        if param.annotation == inspect.Parameter.empty:
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


def x_injectable__mutmut_11(cls: type[T]) -> type[T]:
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
    # Check if class has custom __init__ (not inherited from object)
    if "__init__" not in cls.__dict__:
        raise ValidationError(
            f"Injectable class {cls.__name__} must define its own __init__ method",
            code="injectable_no_init",
            class_name=cls.__name__,
        )

    # Get type hints for __init__
    try:
        # Use localns to resolve forward references within the class's module
        import sys

        module = sys.modules.get(cls.__module__)
        localns = vars(module) if module else {}
        get_type_hints(cls.__init__, globalns=None, localns=localns)
    except NameError:
        # Forward reference couldn't be resolved - that's okay for now
        # The actual resolution will happen at runtime
        pass
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
        # Check if parameter has annotation in signature
        if param.annotation == inspect.Parameter.empty:
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


def x_injectable__mutmut_12(cls: type[T]) -> type[T]:
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
    # Check if class has custom __init__ (not inherited from object)
    if "__init__" not in cls.__dict__:
        raise ValidationError(
            f"Injectable class {cls.__name__} must define its own __init__ method",
            code="INJECTABLE_NO_INIT",
            class_name=cls.__name__,
        )

    # Get type hints for __init__
    try:
        # Use localns to resolve forward references within the class's module
        import sys

        module = None
        localns = vars(module) if module else {}
        get_type_hints(cls.__init__, globalns=None, localns=localns)
    except NameError:
        # Forward reference couldn't be resolved - that's okay for now
        # The actual resolution will happen at runtime
        pass
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
        # Check if parameter has annotation in signature
        if param.annotation == inspect.Parameter.empty:
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


def x_injectable__mutmut_13(cls: type[T]) -> type[T]:
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
    # Check if class has custom __init__ (not inherited from object)
    if "__init__" not in cls.__dict__:
        raise ValidationError(
            f"Injectable class {cls.__name__} must define its own __init__ method",
            code="INJECTABLE_NO_INIT",
            class_name=cls.__name__,
        )

    # Get type hints for __init__
    try:
        # Use localns to resolve forward references within the class's module
        import sys

        module = sys.modules.get(None)
        localns = vars(module) if module else {}
        get_type_hints(cls.__init__, globalns=None, localns=localns)
    except NameError:
        # Forward reference couldn't be resolved - that's okay for now
        # The actual resolution will happen at runtime
        pass
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
        # Check if parameter has annotation in signature
        if param.annotation == inspect.Parameter.empty:
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


def x_injectable__mutmut_14(cls: type[T]) -> type[T]:
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
    # Check if class has custom __init__ (not inherited from object)
    if "__init__" not in cls.__dict__:
        raise ValidationError(
            f"Injectable class {cls.__name__} must define its own __init__ method",
            code="INJECTABLE_NO_INIT",
            class_name=cls.__name__,
        )

    # Get type hints for __init__
    try:
        # Use localns to resolve forward references within the class's module
        import sys

        module = sys.modules.get(cls.__module__)
        localns = None
        get_type_hints(cls.__init__, globalns=None, localns=localns)
    except NameError:
        # Forward reference couldn't be resolved - that's okay for now
        # The actual resolution will happen at runtime
        pass
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
        # Check if parameter has annotation in signature
        if param.annotation == inspect.Parameter.empty:
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


def x_injectable__mutmut_15(cls: type[T]) -> type[T]:
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
    # Check if class has custom __init__ (not inherited from object)
    if "__init__" not in cls.__dict__:
        raise ValidationError(
            f"Injectable class {cls.__name__} must define its own __init__ method",
            code="INJECTABLE_NO_INIT",
            class_name=cls.__name__,
        )

    # Get type hints for __init__
    try:
        # Use localns to resolve forward references within the class's module
        import sys

        module = sys.modules.get(cls.__module__)
        localns = vars(None) if module else {}
        get_type_hints(cls.__init__, globalns=None, localns=localns)
    except NameError:
        # Forward reference couldn't be resolved - that's okay for now
        # The actual resolution will happen at runtime
        pass
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
        # Check if parameter has annotation in signature
        if param.annotation == inspect.Parameter.empty:
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


def x_injectable__mutmut_16(cls: type[T]) -> type[T]:
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
    # Check if class has custom __init__ (not inherited from object)
    if "__init__" not in cls.__dict__:
        raise ValidationError(
            f"Injectable class {cls.__name__} must define its own __init__ method",
            code="INJECTABLE_NO_INIT",
            class_name=cls.__name__,
        )

    # Get type hints for __init__
    try:
        # Use localns to resolve forward references within the class's module
        import sys

        module = sys.modules.get(cls.__module__)
        localns = vars(module) if module else {}
        get_type_hints(None, globalns=None, localns=localns)
    except NameError:
        # Forward reference couldn't be resolved - that's okay for now
        # The actual resolution will happen at runtime
        pass
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
        # Check if parameter has annotation in signature
        if param.annotation == inspect.Parameter.empty:
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


def x_injectable__mutmut_17(cls: type[T]) -> type[T]:
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
    # Check if class has custom __init__ (not inherited from object)
    if "__init__" not in cls.__dict__:
        raise ValidationError(
            f"Injectable class {cls.__name__} must define its own __init__ method",
            code="INJECTABLE_NO_INIT",
            class_name=cls.__name__,
        )

    # Get type hints for __init__
    try:
        # Use localns to resolve forward references within the class's module
        import sys

        module = sys.modules.get(cls.__module__)
        localns = vars(module) if module else {}
        get_type_hints(cls.__init__, globalns=None, localns=None)
    except NameError:
        # Forward reference couldn't be resolved - that's okay for now
        # The actual resolution will happen at runtime
        pass
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
        # Check if parameter has annotation in signature
        if param.annotation == inspect.Parameter.empty:
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


def x_injectable__mutmut_18(cls: type[T]) -> type[T]:
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
    # Check if class has custom __init__ (not inherited from object)
    if "__init__" not in cls.__dict__:
        raise ValidationError(
            f"Injectable class {cls.__name__} must define its own __init__ method",
            code="INJECTABLE_NO_INIT",
            class_name=cls.__name__,
        )

    # Get type hints for __init__
    try:
        # Use localns to resolve forward references within the class's module
        import sys

        module = sys.modules.get(cls.__module__)
        localns = vars(module) if module else {}
        get_type_hints(globalns=None, localns=localns)
    except NameError:
        # Forward reference couldn't be resolved - that's okay for now
        # The actual resolution will happen at runtime
        pass
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
        # Check if parameter has annotation in signature
        if param.annotation == inspect.Parameter.empty:
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


def x_injectable__mutmut_19(cls: type[T]) -> type[T]:
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
    # Check if class has custom __init__ (not inherited from object)
    if "__init__" not in cls.__dict__:
        raise ValidationError(
            f"Injectable class {cls.__name__} must define its own __init__ method",
            code="INJECTABLE_NO_INIT",
            class_name=cls.__name__,
        )

    # Get type hints for __init__
    try:
        # Use localns to resolve forward references within the class's module
        import sys

        module = sys.modules.get(cls.__module__)
        localns = vars(module) if module else {}
        get_type_hints(cls.__init__, localns=localns)
    except NameError:
        # Forward reference couldn't be resolved - that's okay for now
        # The actual resolution will happen at runtime
        pass
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
        # Check if parameter has annotation in signature
        if param.annotation == inspect.Parameter.empty:
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


def x_injectable__mutmut_20(cls: type[T]) -> type[T]:
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
    # Check if class has custom __init__ (not inherited from object)
    if "__init__" not in cls.__dict__:
        raise ValidationError(
            f"Injectable class {cls.__name__} must define its own __init__ method",
            code="INJECTABLE_NO_INIT",
            class_name=cls.__name__,
        )

    # Get type hints for __init__
    try:
        # Use localns to resolve forward references within the class's module
        import sys

        module = sys.modules.get(cls.__module__)
        localns = vars(module) if module else {}
        get_type_hints(cls.__init__, globalns=None, )
    except NameError:
        # Forward reference couldn't be resolved - that's okay for now
        # The actual resolution will happen at runtime
        pass
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
        # Check if parameter has annotation in signature
        if param.annotation == inspect.Parameter.empty:
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


def x_injectable__mutmut_21(cls: type[T]) -> type[T]:
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
    # Check if class has custom __init__ (not inherited from object)
    if "__init__" not in cls.__dict__:
        raise ValidationError(
            f"Injectable class {cls.__name__} must define its own __init__ method",
            code="INJECTABLE_NO_INIT",
            class_name=cls.__name__,
        )

    # Get type hints for __init__
    try:
        # Use localns to resolve forward references within the class's module
        import sys

        module = sys.modules.get(cls.__module__)
        localns = vars(module) if module else {}
        get_type_hints(cls.__init__, globalns=None, localns=localns)
    except NameError:
        # Forward reference couldn't be resolved - that's okay for now
        # The actual resolution will happen at runtime
        pass
    except Exception as e:
        raise ValidationError(
            None,
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
        # Check if parameter has annotation in signature
        if param.annotation == inspect.Parameter.empty:
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


def x_injectable__mutmut_22(cls: type[T]) -> type[T]:
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
    # Check if class has custom __init__ (not inherited from object)
    if "__init__" not in cls.__dict__:
        raise ValidationError(
            f"Injectable class {cls.__name__} must define its own __init__ method",
            code="INJECTABLE_NO_INIT",
            class_name=cls.__name__,
        )

    # Get type hints for __init__
    try:
        # Use localns to resolve forward references within the class's module
        import sys

        module = sys.modules.get(cls.__module__)
        localns = vars(module) if module else {}
        get_type_hints(cls.__init__, globalns=None, localns=localns)
    except NameError:
        # Forward reference couldn't be resolved - that's okay for now
        # The actual resolution will happen at runtime
        pass
    except Exception as e:
        raise ValidationError(
            f"Failed to get type hints for {cls.__name__}.__init__: {e}",
            code=None,
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
        # Check if parameter has annotation in signature
        if param.annotation == inspect.Parameter.empty:
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


def x_injectable__mutmut_23(cls: type[T]) -> type[T]:
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
    # Check if class has custom __init__ (not inherited from object)
    if "__init__" not in cls.__dict__:
        raise ValidationError(
            f"Injectable class {cls.__name__} must define its own __init__ method",
            code="INJECTABLE_NO_INIT",
            class_name=cls.__name__,
        )

    # Get type hints for __init__
    try:
        # Use localns to resolve forward references within the class's module
        import sys

        module = sys.modules.get(cls.__module__)
        localns = vars(module) if module else {}
        get_type_hints(cls.__init__, globalns=None, localns=localns)
    except NameError:
        # Forward reference couldn't be resolved - that's okay for now
        # The actual resolution will happen at runtime
        pass
    except Exception as e:
        raise ValidationError(
            f"Failed to get type hints for {cls.__name__}.__init__: {e}",
            code="INJECTABLE_TYPE_HINT_ERROR",
            class_name=None,
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
        # Check if parameter has annotation in signature
        if param.annotation == inspect.Parameter.empty:
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


def x_injectable__mutmut_24(cls: type[T]) -> type[T]:
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
    # Check if class has custom __init__ (not inherited from object)
    if "__init__" not in cls.__dict__:
        raise ValidationError(
            f"Injectable class {cls.__name__} must define its own __init__ method",
            code="INJECTABLE_NO_INIT",
            class_name=cls.__name__,
        )

    # Get type hints for __init__
    try:
        # Use localns to resolve forward references within the class's module
        import sys

        module = sys.modules.get(cls.__module__)
        localns = vars(module) if module else {}
        get_type_hints(cls.__init__, globalns=None, localns=localns)
    except NameError:
        # Forward reference couldn't be resolved - that's okay for now
        # The actual resolution will happen at runtime
        pass
    except Exception as e:
        raise ValidationError(
            f"Failed to get type hints for {cls.__name__}.__init__: {e}",
            code="INJECTABLE_TYPE_HINT_ERROR",
            class_name=cls.__name__,
            cause=None,
        ) from e

    # Get signature to check for untyped parameters
    sig = inspect.signature(cls.__init__)
    params = list(sig.parameters.values())[1:]  # Skip 'self'

    # Check each parameter has a type hint (excluding *args, **kwargs)
    untyped_params = []
    for param in params:
        if param.kind in (inspect.Parameter.VAR_POSITIONAL, inspect.Parameter.VAR_KEYWORD):
            continue  # *args and **kwargs are fine without hints
        # Check if parameter has annotation in signature
        if param.annotation == inspect.Parameter.empty:
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


def x_injectable__mutmut_25(cls: type[T]) -> type[T]:
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
    # Check if class has custom __init__ (not inherited from object)
    if "__init__" not in cls.__dict__:
        raise ValidationError(
            f"Injectable class {cls.__name__} must define its own __init__ method",
            code="INJECTABLE_NO_INIT",
            class_name=cls.__name__,
        )

    # Get type hints for __init__
    try:
        # Use localns to resolve forward references within the class's module
        import sys

        module = sys.modules.get(cls.__module__)
        localns = vars(module) if module else {}
        get_type_hints(cls.__init__, globalns=None, localns=localns)
    except NameError:
        # Forward reference couldn't be resolved - that's okay for now
        # The actual resolution will happen at runtime
        pass
    except Exception as e:
        raise ValidationError(
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
        # Check if parameter has annotation in signature
        if param.annotation == inspect.Parameter.empty:
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


def x_injectable__mutmut_26(cls: type[T]) -> type[T]:
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
    # Check if class has custom __init__ (not inherited from object)
    if "__init__" not in cls.__dict__:
        raise ValidationError(
            f"Injectable class {cls.__name__} must define its own __init__ method",
            code="INJECTABLE_NO_INIT",
            class_name=cls.__name__,
        )

    # Get type hints for __init__
    try:
        # Use localns to resolve forward references within the class's module
        import sys

        module = sys.modules.get(cls.__module__)
        localns = vars(module) if module else {}
        get_type_hints(cls.__init__, globalns=None, localns=localns)
    except NameError:
        # Forward reference couldn't be resolved - that's okay for now
        # The actual resolution will happen at runtime
        pass
    except Exception as e:
        raise ValidationError(
            f"Failed to get type hints for {cls.__name__}.__init__: {e}",
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
        # Check if parameter has annotation in signature
        if param.annotation == inspect.Parameter.empty:
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


def x_injectable__mutmut_27(cls: type[T]) -> type[T]:
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
    # Check if class has custom __init__ (not inherited from object)
    if "__init__" not in cls.__dict__:
        raise ValidationError(
            f"Injectable class {cls.__name__} must define its own __init__ method",
            code="INJECTABLE_NO_INIT",
            class_name=cls.__name__,
        )

    # Get type hints for __init__
    try:
        # Use localns to resolve forward references within the class's module
        import sys

        module = sys.modules.get(cls.__module__)
        localns = vars(module) if module else {}
        get_type_hints(cls.__init__, globalns=None, localns=localns)
    except NameError:
        # Forward reference couldn't be resolved - that's okay for now
        # The actual resolution will happen at runtime
        pass
    except Exception as e:
        raise ValidationError(
            f"Failed to get type hints for {cls.__name__}.__init__: {e}",
            code="INJECTABLE_TYPE_HINT_ERROR",
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
        # Check if parameter has annotation in signature
        if param.annotation == inspect.Parameter.empty:
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


def x_injectable__mutmut_28(cls: type[T]) -> type[T]:
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
    # Check if class has custom __init__ (not inherited from object)
    if "__init__" not in cls.__dict__:
        raise ValidationError(
            f"Injectable class {cls.__name__} must define its own __init__ method",
            code="INJECTABLE_NO_INIT",
            class_name=cls.__name__,
        )

    # Get type hints for __init__
    try:
        # Use localns to resolve forward references within the class's module
        import sys

        module = sys.modules.get(cls.__module__)
        localns = vars(module) if module else {}
        get_type_hints(cls.__init__, globalns=None, localns=localns)
    except NameError:
        # Forward reference couldn't be resolved - that's okay for now
        # The actual resolution will happen at runtime
        pass
    except Exception as e:
        raise ValidationError(
            f"Failed to get type hints for {cls.__name__}.__init__: {e}",
            code="INJECTABLE_TYPE_HINT_ERROR",
            class_name=cls.__name__,
            ) from e

    # Get signature to check for untyped parameters
    sig = inspect.signature(cls.__init__)
    params = list(sig.parameters.values())[1:]  # Skip 'self'

    # Check each parameter has a type hint (excluding *args, **kwargs)
    untyped_params = []
    for param in params:
        if param.kind in (inspect.Parameter.VAR_POSITIONAL, inspect.Parameter.VAR_KEYWORD):
            continue  # *args and **kwargs are fine without hints
        # Check if parameter has annotation in signature
        if param.annotation == inspect.Parameter.empty:
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


def x_injectable__mutmut_29(cls: type[T]) -> type[T]:
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
    # Check if class has custom __init__ (not inherited from object)
    if "__init__" not in cls.__dict__:
        raise ValidationError(
            f"Injectable class {cls.__name__} must define its own __init__ method",
            code="INJECTABLE_NO_INIT",
            class_name=cls.__name__,
        )

    # Get type hints for __init__
    try:
        # Use localns to resolve forward references within the class's module
        import sys

        module = sys.modules.get(cls.__module__)
        localns = vars(module) if module else {}
        get_type_hints(cls.__init__, globalns=None, localns=localns)
    except NameError:
        # Forward reference couldn't be resolved - that's okay for now
        # The actual resolution will happen at runtime
        pass
    except Exception as e:
        raise ValidationError(
            f"Failed to get type hints for {cls.__name__}.__init__: {e}",
            code="XXINJECTABLE_TYPE_HINT_ERRORXX",
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
        # Check if parameter has annotation in signature
        if param.annotation == inspect.Parameter.empty:
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


def x_injectable__mutmut_30(cls: type[T]) -> type[T]:
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
    # Check if class has custom __init__ (not inherited from object)
    if "__init__" not in cls.__dict__:
        raise ValidationError(
            f"Injectable class {cls.__name__} must define its own __init__ method",
            code="INJECTABLE_NO_INIT",
            class_name=cls.__name__,
        )

    # Get type hints for __init__
    try:
        # Use localns to resolve forward references within the class's module
        import sys

        module = sys.modules.get(cls.__module__)
        localns = vars(module) if module else {}
        get_type_hints(cls.__init__, globalns=None, localns=localns)
    except NameError:
        # Forward reference couldn't be resolved - that's okay for now
        # The actual resolution will happen at runtime
        pass
    except Exception as e:
        raise ValidationError(
            f"Failed to get type hints for {cls.__name__}.__init__: {e}",
            code="injectable_type_hint_error",
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
        # Check if parameter has annotation in signature
        if param.annotation == inspect.Parameter.empty:
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


def x_injectable__mutmut_31(cls: type[T]) -> type[T]:
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
    # Check if class has custom __init__ (not inherited from object)
    if "__init__" not in cls.__dict__:
        raise ValidationError(
            f"Injectable class {cls.__name__} must define its own __init__ method",
            code="INJECTABLE_NO_INIT",
            class_name=cls.__name__,
        )

    # Get type hints for __init__
    try:
        # Use localns to resolve forward references within the class's module
        import sys

        module = sys.modules.get(cls.__module__)
        localns = vars(module) if module else {}
        get_type_hints(cls.__init__, globalns=None, localns=localns)
    except NameError:
        # Forward reference couldn't be resolved - that's okay for now
        # The actual resolution will happen at runtime
        pass
    except Exception as e:
        raise ValidationError(
            f"Failed to get type hints for {cls.__name__}.__init__: {e}",
            code="INJECTABLE_TYPE_HINT_ERROR",
            class_name=cls.__name__,
            cause=e,
        ) from e

    # Get signature to check for untyped parameters
    sig = None
    params = list(sig.parameters.values())[1:]  # Skip 'self'

    # Check each parameter has a type hint (excluding *args, **kwargs)
    untyped_params = []
    for param in params:
        if param.kind in (inspect.Parameter.VAR_POSITIONAL, inspect.Parameter.VAR_KEYWORD):
            continue  # *args and **kwargs are fine without hints
        # Check if parameter has annotation in signature
        if param.annotation == inspect.Parameter.empty:
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


def x_injectable__mutmut_32(cls: type[T]) -> type[T]:
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
    # Check if class has custom __init__ (not inherited from object)
    if "__init__" not in cls.__dict__:
        raise ValidationError(
            f"Injectable class {cls.__name__} must define its own __init__ method",
            code="INJECTABLE_NO_INIT",
            class_name=cls.__name__,
        )

    # Get type hints for __init__
    try:
        # Use localns to resolve forward references within the class's module
        import sys

        module = sys.modules.get(cls.__module__)
        localns = vars(module) if module else {}
        get_type_hints(cls.__init__, globalns=None, localns=localns)
    except NameError:
        # Forward reference couldn't be resolved - that's okay for now
        # The actual resolution will happen at runtime
        pass
    except Exception as e:
        raise ValidationError(
            f"Failed to get type hints for {cls.__name__}.__init__: {e}",
            code="INJECTABLE_TYPE_HINT_ERROR",
            class_name=cls.__name__,
            cause=e,
        ) from e

    # Get signature to check for untyped parameters
    sig = inspect.signature(None)
    params = list(sig.parameters.values())[1:]  # Skip 'self'

    # Check each parameter has a type hint (excluding *args, **kwargs)
    untyped_params = []
    for param in params:
        if param.kind in (inspect.Parameter.VAR_POSITIONAL, inspect.Parameter.VAR_KEYWORD):
            continue  # *args and **kwargs are fine without hints
        # Check if parameter has annotation in signature
        if param.annotation == inspect.Parameter.empty:
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


def x_injectable__mutmut_33(cls: type[T]) -> type[T]:
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
    # Check if class has custom __init__ (not inherited from object)
    if "__init__" not in cls.__dict__:
        raise ValidationError(
            f"Injectable class {cls.__name__} must define its own __init__ method",
            code="INJECTABLE_NO_INIT",
            class_name=cls.__name__,
        )

    # Get type hints for __init__
    try:
        # Use localns to resolve forward references within the class's module
        import sys

        module = sys.modules.get(cls.__module__)
        localns = vars(module) if module else {}
        get_type_hints(cls.__init__, globalns=None, localns=localns)
    except NameError:
        # Forward reference couldn't be resolved - that's okay for now
        # The actual resolution will happen at runtime
        pass
    except Exception as e:
        raise ValidationError(
            f"Failed to get type hints for {cls.__name__}.__init__: {e}",
            code="INJECTABLE_TYPE_HINT_ERROR",
            class_name=cls.__name__,
            cause=e,
        ) from e

    # Get signature to check for untyped parameters
    sig = inspect.signature(cls.__init__)
    params = None  # Skip 'self'

    # Check each parameter has a type hint (excluding *args, **kwargs)
    untyped_params = []
    for param in params:
        if param.kind in (inspect.Parameter.VAR_POSITIONAL, inspect.Parameter.VAR_KEYWORD):
            continue  # *args and **kwargs are fine without hints
        # Check if parameter has annotation in signature
        if param.annotation == inspect.Parameter.empty:
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


def x_injectable__mutmut_34(cls: type[T]) -> type[T]:
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
    # Check if class has custom __init__ (not inherited from object)
    if "__init__" not in cls.__dict__:
        raise ValidationError(
            f"Injectable class {cls.__name__} must define its own __init__ method",
            code="INJECTABLE_NO_INIT",
            class_name=cls.__name__,
        )

    # Get type hints for __init__
    try:
        # Use localns to resolve forward references within the class's module
        import sys

        module = sys.modules.get(cls.__module__)
        localns = vars(module) if module else {}
        get_type_hints(cls.__init__, globalns=None, localns=localns)
    except NameError:
        # Forward reference couldn't be resolved - that's okay for now
        # The actual resolution will happen at runtime
        pass
    except Exception as e:
        raise ValidationError(
            f"Failed to get type hints for {cls.__name__}.__init__: {e}",
            code="INJECTABLE_TYPE_HINT_ERROR",
            class_name=cls.__name__,
            cause=e,
        ) from e

    # Get signature to check for untyped parameters
    sig = inspect.signature(cls.__init__)
    params = list(None)[1:]  # Skip 'self'

    # Check each parameter has a type hint (excluding *args, **kwargs)
    untyped_params = []
    for param in params:
        if param.kind in (inspect.Parameter.VAR_POSITIONAL, inspect.Parameter.VAR_KEYWORD):
            continue  # *args and **kwargs are fine without hints
        # Check if parameter has annotation in signature
        if param.annotation == inspect.Parameter.empty:
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


def x_injectable__mutmut_35(cls: type[T]) -> type[T]:
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
    # Check if class has custom __init__ (not inherited from object)
    if "__init__" not in cls.__dict__:
        raise ValidationError(
            f"Injectable class {cls.__name__} must define its own __init__ method",
            code="INJECTABLE_NO_INIT",
            class_name=cls.__name__,
        )

    # Get type hints for __init__
    try:
        # Use localns to resolve forward references within the class's module
        import sys

        module = sys.modules.get(cls.__module__)
        localns = vars(module) if module else {}
        get_type_hints(cls.__init__, globalns=None, localns=localns)
    except NameError:
        # Forward reference couldn't be resolved - that's okay for now
        # The actual resolution will happen at runtime
        pass
    except Exception as e:
        raise ValidationError(
            f"Failed to get type hints for {cls.__name__}.__init__: {e}",
            code="INJECTABLE_TYPE_HINT_ERROR",
            class_name=cls.__name__,
            cause=e,
        ) from e

    # Get signature to check for untyped parameters
    sig = inspect.signature(cls.__init__)
    params = list(sig.parameters.values())[2:]  # Skip 'self'

    # Check each parameter has a type hint (excluding *args, **kwargs)
    untyped_params = []
    for param in params:
        if param.kind in (inspect.Parameter.VAR_POSITIONAL, inspect.Parameter.VAR_KEYWORD):
            continue  # *args and **kwargs are fine without hints
        # Check if parameter has annotation in signature
        if param.annotation == inspect.Parameter.empty:
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


def x_injectable__mutmut_36(cls: type[T]) -> type[T]:
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
    # Check if class has custom __init__ (not inherited from object)
    if "__init__" not in cls.__dict__:
        raise ValidationError(
            f"Injectable class {cls.__name__} must define its own __init__ method",
            code="INJECTABLE_NO_INIT",
            class_name=cls.__name__,
        )

    # Get type hints for __init__
    try:
        # Use localns to resolve forward references within the class's module
        import sys

        module = sys.modules.get(cls.__module__)
        localns = vars(module) if module else {}
        get_type_hints(cls.__init__, globalns=None, localns=localns)
    except NameError:
        # Forward reference couldn't be resolved - that's okay for now
        # The actual resolution will happen at runtime
        pass
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
    untyped_params = None
    for param in params:
        if param.kind in (inspect.Parameter.VAR_POSITIONAL, inspect.Parameter.VAR_KEYWORD):
            continue  # *args and **kwargs are fine without hints
        # Check if parameter has annotation in signature
        if param.annotation == inspect.Parameter.empty:
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


def x_injectable__mutmut_37(cls: type[T]) -> type[T]:
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
    # Check if class has custom __init__ (not inherited from object)
    if "__init__" not in cls.__dict__:
        raise ValidationError(
            f"Injectable class {cls.__name__} must define its own __init__ method",
            code="INJECTABLE_NO_INIT",
            class_name=cls.__name__,
        )

    # Get type hints for __init__
    try:
        # Use localns to resolve forward references within the class's module
        import sys

        module = sys.modules.get(cls.__module__)
        localns = vars(module) if module else {}
        get_type_hints(cls.__init__, globalns=None, localns=localns)
    except NameError:
        # Forward reference couldn't be resolved - that's okay for now
        # The actual resolution will happen at runtime
        pass
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
        if param.kind not in (inspect.Parameter.VAR_POSITIONAL, inspect.Parameter.VAR_KEYWORD):
            continue  # *args and **kwargs are fine without hints
        # Check if parameter has annotation in signature
        if param.annotation == inspect.Parameter.empty:
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


def x_injectable__mutmut_38(cls: type[T]) -> type[T]:
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
    # Check if class has custom __init__ (not inherited from object)
    if "__init__" not in cls.__dict__:
        raise ValidationError(
            f"Injectable class {cls.__name__} must define its own __init__ method",
            code="INJECTABLE_NO_INIT",
            class_name=cls.__name__,
        )

    # Get type hints for __init__
    try:
        # Use localns to resolve forward references within the class's module
        import sys

        module = sys.modules.get(cls.__module__)
        localns = vars(module) if module else {}
        get_type_hints(cls.__init__, globalns=None, localns=localns)
    except NameError:
        # Forward reference couldn't be resolved - that's okay for now
        # The actual resolution will happen at runtime
        pass
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
            break  # *args and **kwargs are fine without hints
        # Check if parameter has annotation in signature
        if param.annotation == inspect.Parameter.empty:
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


def x_injectable__mutmut_39(cls: type[T]) -> type[T]:
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
    # Check if class has custom __init__ (not inherited from object)
    if "__init__" not in cls.__dict__:
        raise ValidationError(
            f"Injectable class {cls.__name__} must define its own __init__ method",
            code="INJECTABLE_NO_INIT",
            class_name=cls.__name__,
        )

    # Get type hints for __init__
    try:
        # Use localns to resolve forward references within the class's module
        import sys

        module = sys.modules.get(cls.__module__)
        localns = vars(module) if module else {}
        get_type_hints(cls.__init__, globalns=None, localns=localns)
    except NameError:
        # Forward reference couldn't be resolved - that's okay for now
        # The actual resolution will happen at runtime
        pass
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
        # Check if parameter has annotation in signature
        if param.annotation != inspect.Parameter.empty:
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


def x_injectable__mutmut_40(cls: type[T]) -> type[T]:
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
    # Check if class has custom __init__ (not inherited from object)
    if "__init__" not in cls.__dict__:
        raise ValidationError(
            f"Injectable class {cls.__name__} must define its own __init__ method",
            code="INJECTABLE_NO_INIT",
            class_name=cls.__name__,
        )

    # Get type hints for __init__
    try:
        # Use localns to resolve forward references within the class's module
        import sys

        module = sys.modules.get(cls.__module__)
        localns = vars(module) if module else {}
        get_type_hints(cls.__init__, globalns=None, localns=localns)
    except NameError:
        # Forward reference couldn't be resolved - that's okay for now
        # The actual resolution will happen at runtime
        pass
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
        # Check if parameter has annotation in signature
        if param.annotation == inspect.Parameter.empty:
            untyped_params.append(None)

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


def x_injectable__mutmut_41(cls: type[T]) -> type[T]:
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
    # Check if class has custom __init__ (not inherited from object)
    if "__init__" not in cls.__dict__:
        raise ValidationError(
            f"Injectable class {cls.__name__} must define its own __init__ method",
            code="INJECTABLE_NO_INIT",
            class_name=cls.__name__,
        )

    # Get type hints for __init__
    try:
        # Use localns to resolve forward references within the class's module
        import sys

        module = sys.modules.get(cls.__module__)
        localns = vars(module) if module else {}
        get_type_hints(cls.__init__, globalns=None, localns=localns)
    except NameError:
        # Forward reference couldn't be resolved - that's okay for now
        # The actual resolution will happen at runtime
        pass
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
        # Check if parameter has annotation in signature
        if param.annotation == inspect.Parameter.empty:
            untyped_params.append(param.name)

    if untyped_params:
        raise ValidationError(
            None,
            code="INJECTABLE_UNTYPED_PARAMS",
            class_name=cls.__name__,
            untyped_params=untyped_params,
        )

    # Mark as injectable (for introspection/documentation)
    setattr(cls, _INJECTABLE_MARKER, True)

    return cls


def x_injectable__mutmut_42(cls: type[T]) -> type[T]:
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
    # Check if class has custom __init__ (not inherited from object)
    if "__init__" not in cls.__dict__:
        raise ValidationError(
            f"Injectable class {cls.__name__} must define its own __init__ method",
            code="INJECTABLE_NO_INIT",
            class_name=cls.__name__,
        )

    # Get type hints for __init__
    try:
        # Use localns to resolve forward references within the class's module
        import sys

        module = sys.modules.get(cls.__module__)
        localns = vars(module) if module else {}
        get_type_hints(cls.__init__, globalns=None, localns=localns)
    except NameError:
        # Forward reference couldn't be resolved - that's okay for now
        # The actual resolution will happen at runtime
        pass
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
        # Check if parameter has annotation in signature
        if param.annotation == inspect.Parameter.empty:
            untyped_params.append(param.name)

    if untyped_params:
        raise ValidationError(
            f"Injectable class {cls.__name__}.__init__ has untyped parameters: {untyped_params}. "
            "All constructor parameters must have type hints for dependency injection.",
            code=None,
            class_name=cls.__name__,
            untyped_params=untyped_params,
        )

    # Mark as injectable (for introspection/documentation)
    setattr(cls, _INJECTABLE_MARKER, True)

    return cls


def x_injectable__mutmut_43(cls: type[T]) -> type[T]:
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
    # Check if class has custom __init__ (not inherited from object)
    if "__init__" not in cls.__dict__:
        raise ValidationError(
            f"Injectable class {cls.__name__} must define its own __init__ method",
            code="INJECTABLE_NO_INIT",
            class_name=cls.__name__,
        )

    # Get type hints for __init__
    try:
        # Use localns to resolve forward references within the class's module
        import sys

        module = sys.modules.get(cls.__module__)
        localns = vars(module) if module else {}
        get_type_hints(cls.__init__, globalns=None, localns=localns)
    except NameError:
        # Forward reference couldn't be resolved - that's okay for now
        # The actual resolution will happen at runtime
        pass
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
        # Check if parameter has annotation in signature
        if param.annotation == inspect.Parameter.empty:
            untyped_params.append(param.name)

    if untyped_params:
        raise ValidationError(
            f"Injectable class {cls.__name__}.__init__ has untyped parameters: {untyped_params}. "
            "All constructor parameters must have type hints for dependency injection.",
            code="INJECTABLE_UNTYPED_PARAMS",
            class_name=None,
            untyped_params=untyped_params,
        )

    # Mark as injectable (for introspection/documentation)
    setattr(cls, _INJECTABLE_MARKER, True)

    return cls


def x_injectable__mutmut_44(cls: type[T]) -> type[T]:
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
    # Check if class has custom __init__ (not inherited from object)
    if "__init__" not in cls.__dict__:
        raise ValidationError(
            f"Injectable class {cls.__name__} must define its own __init__ method",
            code="INJECTABLE_NO_INIT",
            class_name=cls.__name__,
        )

    # Get type hints for __init__
    try:
        # Use localns to resolve forward references within the class's module
        import sys

        module = sys.modules.get(cls.__module__)
        localns = vars(module) if module else {}
        get_type_hints(cls.__init__, globalns=None, localns=localns)
    except NameError:
        # Forward reference couldn't be resolved - that's okay for now
        # The actual resolution will happen at runtime
        pass
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
        # Check if parameter has annotation in signature
        if param.annotation == inspect.Parameter.empty:
            untyped_params.append(param.name)

    if untyped_params:
        raise ValidationError(
            f"Injectable class {cls.__name__}.__init__ has untyped parameters: {untyped_params}. "
            "All constructor parameters must have type hints for dependency injection.",
            code="INJECTABLE_UNTYPED_PARAMS",
            class_name=cls.__name__,
            untyped_params=None,
        )

    # Mark as injectable (for introspection/documentation)
    setattr(cls, _INJECTABLE_MARKER, True)

    return cls


def x_injectable__mutmut_45(cls: type[T]) -> type[T]:
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
    # Check if class has custom __init__ (not inherited from object)
    if "__init__" not in cls.__dict__:
        raise ValidationError(
            f"Injectable class {cls.__name__} must define its own __init__ method",
            code="INJECTABLE_NO_INIT",
            class_name=cls.__name__,
        )

    # Get type hints for __init__
    try:
        # Use localns to resolve forward references within the class's module
        import sys

        module = sys.modules.get(cls.__module__)
        localns = vars(module) if module else {}
        get_type_hints(cls.__init__, globalns=None, localns=localns)
    except NameError:
        # Forward reference couldn't be resolved - that's okay for now
        # The actual resolution will happen at runtime
        pass
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
        # Check if parameter has annotation in signature
        if param.annotation == inspect.Parameter.empty:
            untyped_params.append(param.name)

    if untyped_params:
        raise ValidationError(
            code="INJECTABLE_UNTYPED_PARAMS",
            class_name=cls.__name__,
            untyped_params=untyped_params,
        )

    # Mark as injectable (for introspection/documentation)
    setattr(cls, _INJECTABLE_MARKER, True)

    return cls


def x_injectable__mutmut_46(cls: type[T]) -> type[T]:
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
    # Check if class has custom __init__ (not inherited from object)
    if "__init__" not in cls.__dict__:
        raise ValidationError(
            f"Injectable class {cls.__name__} must define its own __init__ method",
            code="INJECTABLE_NO_INIT",
            class_name=cls.__name__,
        )

    # Get type hints for __init__
    try:
        # Use localns to resolve forward references within the class's module
        import sys

        module = sys.modules.get(cls.__module__)
        localns = vars(module) if module else {}
        get_type_hints(cls.__init__, globalns=None, localns=localns)
    except NameError:
        # Forward reference couldn't be resolved - that's okay for now
        # The actual resolution will happen at runtime
        pass
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
        # Check if parameter has annotation in signature
        if param.annotation == inspect.Parameter.empty:
            untyped_params.append(param.name)

    if untyped_params:
        raise ValidationError(
            f"Injectable class {cls.__name__}.__init__ has untyped parameters: {untyped_params}. "
            "All constructor parameters must have type hints for dependency injection.",
            class_name=cls.__name__,
            untyped_params=untyped_params,
        )

    # Mark as injectable (for introspection/documentation)
    setattr(cls, _INJECTABLE_MARKER, True)

    return cls


def x_injectable__mutmut_47(cls: type[T]) -> type[T]:
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
    # Check if class has custom __init__ (not inherited from object)
    if "__init__" not in cls.__dict__:
        raise ValidationError(
            f"Injectable class {cls.__name__} must define its own __init__ method",
            code="INJECTABLE_NO_INIT",
            class_name=cls.__name__,
        )

    # Get type hints for __init__
    try:
        # Use localns to resolve forward references within the class's module
        import sys

        module = sys.modules.get(cls.__module__)
        localns = vars(module) if module else {}
        get_type_hints(cls.__init__, globalns=None, localns=localns)
    except NameError:
        # Forward reference couldn't be resolved - that's okay for now
        # The actual resolution will happen at runtime
        pass
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
        # Check if parameter has annotation in signature
        if param.annotation == inspect.Parameter.empty:
            untyped_params.append(param.name)

    if untyped_params:
        raise ValidationError(
            f"Injectable class {cls.__name__}.__init__ has untyped parameters: {untyped_params}. "
            "All constructor parameters must have type hints for dependency injection.",
            code="INJECTABLE_UNTYPED_PARAMS",
            untyped_params=untyped_params,
        )

    # Mark as injectable (for introspection/documentation)
    setattr(cls, _INJECTABLE_MARKER, True)

    return cls


def x_injectable__mutmut_48(cls: type[T]) -> type[T]:
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
    # Check if class has custom __init__ (not inherited from object)
    if "__init__" not in cls.__dict__:
        raise ValidationError(
            f"Injectable class {cls.__name__} must define its own __init__ method",
            code="INJECTABLE_NO_INIT",
            class_name=cls.__name__,
        )

    # Get type hints for __init__
    try:
        # Use localns to resolve forward references within the class's module
        import sys

        module = sys.modules.get(cls.__module__)
        localns = vars(module) if module else {}
        get_type_hints(cls.__init__, globalns=None, localns=localns)
    except NameError:
        # Forward reference couldn't be resolved - that's okay for now
        # The actual resolution will happen at runtime
        pass
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
        # Check if parameter has annotation in signature
        if param.annotation == inspect.Parameter.empty:
            untyped_params.append(param.name)

    if untyped_params:
        raise ValidationError(
            f"Injectable class {cls.__name__}.__init__ has untyped parameters: {untyped_params}. "
            "All constructor parameters must have type hints for dependency injection.",
            code="INJECTABLE_UNTYPED_PARAMS",
            class_name=cls.__name__,
            )

    # Mark as injectable (for introspection/documentation)
    setattr(cls, _INJECTABLE_MARKER, True)

    return cls


def x_injectable__mutmut_49(cls: type[T]) -> type[T]:
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
    # Check if class has custom __init__ (not inherited from object)
    if "__init__" not in cls.__dict__:
        raise ValidationError(
            f"Injectable class {cls.__name__} must define its own __init__ method",
            code="INJECTABLE_NO_INIT",
            class_name=cls.__name__,
        )

    # Get type hints for __init__
    try:
        # Use localns to resolve forward references within the class's module
        import sys

        module = sys.modules.get(cls.__module__)
        localns = vars(module) if module else {}
        get_type_hints(cls.__init__, globalns=None, localns=localns)
    except NameError:
        # Forward reference couldn't be resolved - that's okay for now
        # The actual resolution will happen at runtime
        pass
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
        # Check if parameter has annotation in signature
        if param.annotation == inspect.Parameter.empty:
            untyped_params.append(param.name)

    if untyped_params:
        raise ValidationError(
            f"Injectable class {cls.__name__}.__init__ has untyped parameters: {untyped_params}. "
            "XXAll constructor parameters must have type hints for dependency injection.XX",
            code="INJECTABLE_UNTYPED_PARAMS",
            class_name=cls.__name__,
            untyped_params=untyped_params,
        )

    # Mark as injectable (for introspection/documentation)
    setattr(cls, _INJECTABLE_MARKER, True)

    return cls


def x_injectable__mutmut_50(cls: type[T]) -> type[T]:
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
    # Check if class has custom __init__ (not inherited from object)
    if "__init__" not in cls.__dict__:
        raise ValidationError(
            f"Injectable class {cls.__name__} must define its own __init__ method",
            code="INJECTABLE_NO_INIT",
            class_name=cls.__name__,
        )

    # Get type hints for __init__
    try:
        # Use localns to resolve forward references within the class's module
        import sys

        module = sys.modules.get(cls.__module__)
        localns = vars(module) if module else {}
        get_type_hints(cls.__init__, globalns=None, localns=localns)
    except NameError:
        # Forward reference couldn't be resolved - that's okay for now
        # The actual resolution will happen at runtime
        pass
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
        # Check if parameter has annotation in signature
        if param.annotation == inspect.Parameter.empty:
            untyped_params.append(param.name)

    if untyped_params:
        raise ValidationError(
            f"Injectable class {cls.__name__}.__init__ has untyped parameters: {untyped_params}. "
            "all constructor parameters must have type hints for dependency injection.",
            code="INJECTABLE_UNTYPED_PARAMS",
            class_name=cls.__name__,
            untyped_params=untyped_params,
        )

    # Mark as injectable (for introspection/documentation)
    setattr(cls, _INJECTABLE_MARKER, True)

    return cls


def x_injectable__mutmut_51(cls: type[T]) -> type[T]:
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
    # Check if class has custom __init__ (not inherited from object)
    if "__init__" not in cls.__dict__:
        raise ValidationError(
            f"Injectable class {cls.__name__} must define its own __init__ method",
            code="INJECTABLE_NO_INIT",
            class_name=cls.__name__,
        )

    # Get type hints for __init__
    try:
        # Use localns to resolve forward references within the class's module
        import sys

        module = sys.modules.get(cls.__module__)
        localns = vars(module) if module else {}
        get_type_hints(cls.__init__, globalns=None, localns=localns)
    except NameError:
        # Forward reference couldn't be resolved - that's okay for now
        # The actual resolution will happen at runtime
        pass
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
        # Check if parameter has annotation in signature
        if param.annotation == inspect.Parameter.empty:
            untyped_params.append(param.name)

    if untyped_params:
        raise ValidationError(
            f"Injectable class {cls.__name__}.__init__ has untyped parameters: {untyped_params}. "
            "ALL CONSTRUCTOR PARAMETERS MUST HAVE TYPE HINTS FOR DEPENDENCY INJECTION.",
            code="INJECTABLE_UNTYPED_PARAMS",
            class_name=cls.__name__,
            untyped_params=untyped_params,
        )

    # Mark as injectable (for introspection/documentation)
    setattr(cls, _INJECTABLE_MARKER, True)

    return cls


def x_injectable__mutmut_52(cls: type[T]) -> type[T]:
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
    # Check if class has custom __init__ (not inherited from object)
    if "__init__" not in cls.__dict__:
        raise ValidationError(
            f"Injectable class {cls.__name__} must define its own __init__ method",
            code="INJECTABLE_NO_INIT",
            class_name=cls.__name__,
        )

    # Get type hints for __init__
    try:
        # Use localns to resolve forward references within the class's module
        import sys

        module = sys.modules.get(cls.__module__)
        localns = vars(module) if module else {}
        get_type_hints(cls.__init__, globalns=None, localns=localns)
    except NameError:
        # Forward reference couldn't be resolved - that's okay for now
        # The actual resolution will happen at runtime
        pass
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
        # Check if parameter has annotation in signature
        if param.annotation == inspect.Parameter.empty:
            untyped_params.append(param.name)

    if untyped_params:
        raise ValidationError(
            f"Injectable class {cls.__name__}.__init__ has untyped parameters: {untyped_params}. "
            "All constructor parameters must have type hints for dependency injection.",
            code="XXINJECTABLE_UNTYPED_PARAMSXX",
            class_name=cls.__name__,
            untyped_params=untyped_params,
        )

    # Mark as injectable (for introspection/documentation)
    setattr(cls, _INJECTABLE_MARKER, True)

    return cls


def x_injectable__mutmut_53(cls: type[T]) -> type[T]:
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
    # Check if class has custom __init__ (not inherited from object)
    if "__init__" not in cls.__dict__:
        raise ValidationError(
            f"Injectable class {cls.__name__} must define its own __init__ method",
            code="INJECTABLE_NO_INIT",
            class_name=cls.__name__,
        )

    # Get type hints for __init__
    try:
        # Use localns to resolve forward references within the class's module
        import sys

        module = sys.modules.get(cls.__module__)
        localns = vars(module) if module else {}
        get_type_hints(cls.__init__, globalns=None, localns=localns)
    except NameError:
        # Forward reference couldn't be resolved - that's okay for now
        # The actual resolution will happen at runtime
        pass
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
        # Check if parameter has annotation in signature
        if param.annotation == inspect.Parameter.empty:
            untyped_params.append(param.name)

    if untyped_params:
        raise ValidationError(
            f"Injectable class {cls.__name__}.__init__ has untyped parameters: {untyped_params}. "
            "All constructor parameters must have type hints for dependency injection.",
            code="injectable_untyped_params",
            class_name=cls.__name__,
            untyped_params=untyped_params,
        )

    # Mark as injectable (for introspection/documentation)
    setattr(cls, _INJECTABLE_MARKER, True)

    return cls


def x_injectable__mutmut_54(cls: type[T]) -> type[T]:
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
    # Check if class has custom __init__ (not inherited from object)
    if "__init__" not in cls.__dict__:
        raise ValidationError(
            f"Injectable class {cls.__name__} must define its own __init__ method",
            code="INJECTABLE_NO_INIT",
            class_name=cls.__name__,
        )

    # Get type hints for __init__
    try:
        # Use localns to resolve forward references within the class's module
        import sys

        module = sys.modules.get(cls.__module__)
        localns = vars(module) if module else {}
        get_type_hints(cls.__init__, globalns=None, localns=localns)
    except NameError:
        # Forward reference couldn't be resolved - that's okay for now
        # The actual resolution will happen at runtime
        pass
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
        # Check if parameter has annotation in signature
        if param.annotation == inspect.Parameter.empty:
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
    setattr(None, _INJECTABLE_MARKER, True)

    return cls


def x_injectable__mutmut_55(cls: type[T]) -> type[T]:
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
    # Check if class has custom __init__ (not inherited from object)
    if "__init__" not in cls.__dict__:
        raise ValidationError(
            f"Injectable class {cls.__name__} must define its own __init__ method",
            code="INJECTABLE_NO_INIT",
            class_name=cls.__name__,
        )

    # Get type hints for __init__
    try:
        # Use localns to resolve forward references within the class's module
        import sys

        module = sys.modules.get(cls.__module__)
        localns = vars(module) if module else {}
        get_type_hints(cls.__init__, globalns=None, localns=localns)
    except NameError:
        # Forward reference couldn't be resolved - that's okay for now
        # The actual resolution will happen at runtime
        pass
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
        # Check if parameter has annotation in signature
        if param.annotation == inspect.Parameter.empty:
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
    setattr(cls, None, True)

    return cls


def x_injectable__mutmut_56(cls: type[T]) -> type[T]:
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
    # Check if class has custom __init__ (not inherited from object)
    if "__init__" not in cls.__dict__:
        raise ValidationError(
            f"Injectable class {cls.__name__} must define its own __init__ method",
            code="INJECTABLE_NO_INIT",
            class_name=cls.__name__,
        )

    # Get type hints for __init__
    try:
        # Use localns to resolve forward references within the class's module
        import sys

        module = sys.modules.get(cls.__module__)
        localns = vars(module) if module else {}
        get_type_hints(cls.__init__, globalns=None, localns=localns)
    except NameError:
        # Forward reference couldn't be resolved - that's okay for now
        # The actual resolution will happen at runtime
        pass
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
        # Check if parameter has annotation in signature
        if param.annotation == inspect.Parameter.empty:
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
    setattr(cls, _INJECTABLE_MARKER, None)

    return cls


def x_injectable__mutmut_57(cls: type[T]) -> type[T]:
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
    # Check if class has custom __init__ (not inherited from object)
    if "__init__" not in cls.__dict__:
        raise ValidationError(
            f"Injectable class {cls.__name__} must define its own __init__ method",
            code="INJECTABLE_NO_INIT",
            class_name=cls.__name__,
        )

    # Get type hints for __init__
    try:
        # Use localns to resolve forward references within the class's module
        import sys

        module = sys.modules.get(cls.__module__)
        localns = vars(module) if module else {}
        get_type_hints(cls.__init__, globalns=None, localns=localns)
    except NameError:
        # Forward reference couldn't be resolved - that's okay for now
        # The actual resolution will happen at runtime
        pass
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
        # Check if parameter has annotation in signature
        if param.annotation == inspect.Parameter.empty:
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
    setattr(_INJECTABLE_MARKER, True)

    return cls


def x_injectable__mutmut_58(cls: type[T]) -> type[T]:
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
    # Check if class has custom __init__ (not inherited from object)
    if "__init__" not in cls.__dict__:
        raise ValidationError(
            f"Injectable class {cls.__name__} must define its own __init__ method",
            code="INJECTABLE_NO_INIT",
            class_name=cls.__name__,
        )

    # Get type hints for __init__
    try:
        # Use localns to resolve forward references within the class's module
        import sys

        module = sys.modules.get(cls.__module__)
        localns = vars(module) if module else {}
        get_type_hints(cls.__init__, globalns=None, localns=localns)
    except NameError:
        # Forward reference couldn't be resolved - that's okay for now
        # The actual resolution will happen at runtime
        pass
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
        # Check if parameter has annotation in signature
        if param.annotation == inspect.Parameter.empty:
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
    setattr(cls, True)

    return cls


def x_injectable__mutmut_59(cls: type[T]) -> type[T]:
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
    # Check if class has custom __init__ (not inherited from object)
    if "__init__" not in cls.__dict__:
        raise ValidationError(
            f"Injectable class {cls.__name__} must define its own __init__ method",
            code="INJECTABLE_NO_INIT",
            class_name=cls.__name__,
        )

    # Get type hints for __init__
    try:
        # Use localns to resolve forward references within the class's module
        import sys

        module = sys.modules.get(cls.__module__)
        localns = vars(module) if module else {}
        get_type_hints(cls.__init__, globalns=None, localns=localns)
    except NameError:
        # Forward reference couldn't be resolved - that's okay for now
        # The actual resolution will happen at runtime
        pass
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
        # Check if parameter has annotation in signature
        if param.annotation == inspect.Parameter.empty:
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
    setattr(cls, _INJECTABLE_MARKER, )

    return cls


def x_injectable__mutmut_60(cls: type[T]) -> type[T]:
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
    # Check if class has custom __init__ (not inherited from object)
    if "__init__" not in cls.__dict__:
        raise ValidationError(
            f"Injectable class {cls.__name__} must define its own __init__ method",
            code="INJECTABLE_NO_INIT",
            class_name=cls.__name__,
        )

    # Get type hints for __init__
    try:
        # Use localns to resolve forward references within the class's module
        import sys

        module = sys.modules.get(cls.__module__)
        localns = vars(module) if module else {}
        get_type_hints(cls.__init__, globalns=None, localns=localns)
    except NameError:
        # Forward reference couldn't be resolved - that's okay for now
        # The actual resolution will happen at runtime
        pass
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
        # Check if parameter has annotation in signature
        if param.annotation == inspect.Parameter.empty:
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
    setattr(cls, _INJECTABLE_MARKER, False)

    return cls

x_injectable__mutmut_mutants : ClassVar[MutantDict] = {
'x_injectable__mutmut_1': x_injectable__mutmut_1, 
    'x_injectable__mutmut_2': x_injectable__mutmut_2, 
    'x_injectable__mutmut_3': x_injectable__mutmut_3, 
    'x_injectable__mutmut_4': x_injectable__mutmut_4, 
    'x_injectable__mutmut_5': x_injectable__mutmut_5, 
    'x_injectable__mutmut_6': x_injectable__mutmut_6, 
    'x_injectable__mutmut_7': x_injectable__mutmut_7, 
    'x_injectable__mutmut_8': x_injectable__mutmut_8, 
    'x_injectable__mutmut_9': x_injectable__mutmut_9, 
    'x_injectable__mutmut_10': x_injectable__mutmut_10, 
    'x_injectable__mutmut_11': x_injectable__mutmut_11, 
    'x_injectable__mutmut_12': x_injectable__mutmut_12, 
    'x_injectable__mutmut_13': x_injectable__mutmut_13, 
    'x_injectable__mutmut_14': x_injectable__mutmut_14, 
    'x_injectable__mutmut_15': x_injectable__mutmut_15, 
    'x_injectable__mutmut_16': x_injectable__mutmut_16, 
    'x_injectable__mutmut_17': x_injectable__mutmut_17, 
    'x_injectable__mutmut_18': x_injectable__mutmut_18, 
    'x_injectable__mutmut_19': x_injectable__mutmut_19, 
    'x_injectable__mutmut_20': x_injectable__mutmut_20, 
    'x_injectable__mutmut_21': x_injectable__mutmut_21, 
    'x_injectable__mutmut_22': x_injectable__mutmut_22, 
    'x_injectable__mutmut_23': x_injectable__mutmut_23, 
    'x_injectable__mutmut_24': x_injectable__mutmut_24, 
    'x_injectable__mutmut_25': x_injectable__mutmut_25, 
    'x_injectable__mutmut_26': x_injectable__mutmut_26, 
    'x_injectable__mutmut_27': x_injectable__mutmut_27, 
    'x_injectable__mutmut_28': x_injectable__mutmut_28, 
    'x_injectable__mutmut_29': x_injectable__mutmut_29, 
    'x_injectable__mutmut_30': x_injectable__mutmut_30, 
    'x_injectable__mutmut_31': x_injectable__mutmut_31, 
    'x_injectable__mutmut_32': x_injectable__mutmut_32, 
    'x_injectable__mutmut_33': x_injectable__mutmut_33, 
    'x_injectable__mutmut_34': x_injectable__mutmut_34, 
    'x_injectable__mutmut_35': x_injectable__mutmut_35, 
    'x_injectable__mutmut_36': x_injectable__mutmut_36, 
    'x_injectable__mutmut_37': x_injectable__mutmut_37, 
    'x_injectable__mutmut_38': x_injectable__mutmut_38, 
    'x_injectable__mutmut_39': x_injectable__mutmut_39, 
    'x_injectable__mutmut_40': x_injectable__mutmut_40, 
    'x_injectable__mutmut_41': x_injectable__mutmut_41, 
    'x_injectable__mutmut_42': x_injectable__mutmut_42, 
    'x_injectable__mutmut_43': x_injectable__mutmut_43, 
    'x_injectable__mutmut_44': x_injectable__mutmut_44, 
    'x_injectable__mutmut_45': x_injectable__mutmut_45, 
    'x_injectable__mutmut_46': x_injectable__mutmut_46, 
    'x_injectable__mutmut_47': x_injectable__mutmut_47, 
    'x_injectable__mutmut_48': x_injectable__mutmut_48, 
    'x_injectable__mutmut_49': x_injectable__mutmut_49, 
    'x_injectable__mutmut_50': x_injectable__mutmut_50, 
    'x_injectable__mutmut_51': x_injectable__mutmut_51, 
    'x_injectable__mutmut_52': x_injectable__mutmut_52, 
    'x_injectable__mutmut_53': x_injectable__mutmut_53, 
    'x_injectable__mutmut_54': x_injectable__mutmut_54, 
    'x_injectable__mutmut_55': x_injectable__mutmut_55, 
    'x_injectable__mutmut_56': x_injectable__mutmut_56, 
    'x_injectable__mutmut_57': x_injectable__mutmut_57, 
    'x_injectable__mutmut_58': x_injectable__mutmut_58, 
    'x_injectable__mutmut_59': x_injectable__mutmut_59, 
    'x_injectable__mutmut_60': x_injectable__mutmut_60
}

def injectable(*args, **kwargs):
    result = _mutmut_trampoline(x_injectable__mutmut_orig, x_injectable__mutmut_mutants, args, kwargs)
    return result 

injectable.__signature__ = _mutmut_signature(x_injectable__mutmut_orig)
x_injectable__mutmut_orig.__name__ = 'x_injectable'


def x_is_injectable__mutmut_orig(cls: type[Any]) -> bool:
    """Check if a class is marked as injectable.

    Args:
        cls: Class to check

    Returns:
        True if class is marked with @injectable decorator
    """
    return getattr(cls, _INJECTABLE_MARKER, False)


def x_is_injectable__mutmut_1(cls: type[Any]) -> bool:
    """Check if a class is marked as injectable.

    Args:
        cls: Class to check

    Returns:
        True if class is marked with @injectable decorator
    """
    return getattr(None, _INJECTABLE_MARKER, False)


def x_is_injectable__mutmut_2(cls: type[Any]) -> bool:
    """Check if a class is marked as injectable.

    Args:
        cls: Class to check

    Returns:
        True if class is marked with @injectable decorator
    """
    return getattr(cls, None, False)


def x_is_injectable__mutmut_3(cls: type[Any]) -> bool:
    """Check if a class is marked as injectable.

    Args:
        cls: Class to check

    Returns:
        True if class is marked with @injectable decorator
    """
    return getattr(cls, _INJECTABLE_MARKER, None)


def x_is_injectable__mutmut_4(cls: type[Any]) -> bool:
    """Check if a class is marked as injectable.

    Args:
        cls: Class to check

    Returns:
        True if class is marked with @injectable decorator
    """
    return getattr(_INJECTABLE_MARKER, False)


def x_is_injectable__mutmut_5(cls: type[Any]) -> bool:
    """Check if a class is marked as injectable.

    Args:
        cls: Class to check

    Returns:
        True if class is marked with @injectable decorator
    """
    return getattr(cls, False)


def x_is_injectable__mutmut_6(cls: type[Any]) -> bool:
    """Check if a class is marked as injectable.

    Args:
        cls: Class to check

    Returns:
        True if class is marked with @injectable decorator
    """
    return getattr(cls, _INJECTABLE_MARKER, )


def x_is_injectable__mutmut_7(cls: type[Any]) -> bool:
    """Check if a class is marked as injectable.

    Args:
        cls: Class to check

    Returns:
        True if class is marked with @injectable decorator
    """
    return getattr(cls, _INJECTABLE_MARKER, True)

x_is_injectable__mutmut_mutants : ClassVar[MutantDict] = {
'x_is_injectable__mutmut_1': x_is_injectable__mutmut_1, 
    'x_is_injectable__mutmut_2': x_is_injectable__mutmut_2, 
    'x_is_injectable__mutmut_3': x_is_injectable__mutmut_3, 
    'x_is_injectable__mutmut_4': x_is_injectable__mutmut_4, 
    'x_is_injectable__mutmut_5': x_is_injectable__mutmut_5, 
    'x_is_injectable__mutmut_6': x_is_injectable__mutmut_6, 
    'x_is_injectable__mutmut_7': x_is_injectable__mutmut_7
}

def is_injectable(*args, **kwargs):
    result = _mutmut_trampoline(x_is_injectable__mutmut_orig, x_is_injectable__mutmut_mutants, args, kwargs)
    return result 

is_injectable.__signature__ = _mutmut_signature(x_is_injectable__mutmut_orig)
x_is_injectable__mutmut_orig.__name__ = 'x_is_injectable'


def x_resolve_dependencies__mutmut_orig(  # noqa: C901
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
        import sys

        module = sys.modules.get(cls.__module__)
        localns = vars(module) if module else {}
        hints = get_type_hints(cls.__init__, globalns=None, localns=localns)
    except NameError:
        # Forward reference error - collect what we can from annotations
        hints = {}
        sig = inspect.signature(cls.__init__)
        for param_name, param in sig.parameters.items():
            if param_name == "self":
                continue
            if param.annotation != inspect.Parameter.empty:
                # Use the annotation directly (may be a string)
                hints[param_name] = param.annotation
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

        # If param_type is a string (forward reference), try to resolve it
        if isinstance(param_type, str):
            # Look up the type in the class's module
            import sys

            module = sys.modules.get(cls.__module__)
            if module and hasattr(module, param_type):
                param_type = getattr(module, param_type)
            else:
                if allow_missing:
                    missing.append(param.name)
                    continue
                raise ValidationError(
                    f"Forward reference '{param_type}' for parameter '{param.name}' could not be resolved",
                    code="RESOLVE_FORWARD_REF_ERROR",
                    class_name=cls.__name__,
                    param_name=param.name,
                    forward_ref=param_type,
                )

        # Try to resolve from registry by type
        # Strategy: Look for registered instance of this type
        instance = registry.get_by_type(param_type)

        if instance is None:
            if allow_missing:
                missing.append(param.name)
                continue
            type_name = getattr(param_type, "__name__", str(param_type))
            raise NotFoundError(
                f"Dependency '{type_name}' required by {cls.__name__} not found in registry",
                code="RESOLVE_DEPENDENCY_NOT_FOUND",
                class_name=cls.__name__,
                param_name=param.name,
                param_type=type_name,
            )

        resolved[param.name] = instance

    return resolved


def x_resolve_dependencies__mutmut_1(  # noqa: C901
    cls: type[T],
    registry: Any,  # Registry type
    allow_missing: bool = True,
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
        import sys

        module = sys.modules.get(cls.__module__)
        localns = vars(module) if module else {}
        hints = get_type_hints(cls.__init__, globalns=None, localns=localns)
    except NameError:
        # Forward reference error - collect what we can from annotations
        hints = {}
        sig = inspect.signature(cls.__init__)
        for param_name, param in sig.parameters.items():
            if param_name == "self":
                continue
            if param.annotation != inspect.Parameter.empty:
                # Use the annotation directly (may be a string)
                hints[param_name] = param.annotation
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

        # If param_type is a string (forward reference), try to resolve it
        if isinstance(param_type, str):
            # Look up the type in the class's module
            import sys

            module = sys.modules.get(cls.__module__)
            if module and hasattr(module, param_type):
                param_type = getattr(module, param_type)
            else:
                if allow_missing:
                    missing.append(param.name)
                    continue
                raise ValidationError(
                    f"Forward reference '{param_type}' for parameter '{param.name}' could not be resolved",
                    code="RESOLVE_FORWARD_REF_ERROR",
                    class_name=cls.__name__,
                    param_name=param.name,
                    forward_ref=param_type,
                )

        # Try to resolve from registry by type
        # Strategy: Look for registered instance of this type
        instance = registry.get_by_type(param_type)

        if instance is None:
            if allow_missing:
                missing.append(param.name)
                continue
            type_name = getattr(param_type, "__name__", str(param_type))
            raise NotFoundError(
                f"Dependency '{type_name}' required by {cls.__name__} not found in registry",
                code="RESOLVE_DEPENDENCY_NOT_FOUND",
                class_name=cls.__name__,
                param_name=param.name,
                param_type=type_name,
            )

        resolved[param.name] = instance

    return resolved


def x_resolve_dependencies__mutmut_2(  # noqa: C901
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
        import sys

        module = None
        localns = vars(module) if module else {}
        hints = get_type_hints(cls.__init__, globalns=None, localns=localns)
    except NameError:
        # Forward reference error - collect what we can from annotations
        hints = {}
        sig = inspect.signature(cls.__init__)
        for param_name, param in sig.parameters.items():
            if param_name == "self":
                continue
            if param.annotation != inspect.Parameter.empty:
                # Use the annotation directly (may be a string)
                hints[param_name] = param.annotation
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

        # If param_type is a string (forward reference), try to resolve it
        if isinstance(param_type, str):
            # Look up the type in the class's module
            import sys

            module = sys.modules.get(cls.__module__)
            if module and hasattr(module, param_type):
                param_type = getattr(module, param_type)
            else:
                if allow_missing:
                    missing.append(param.name)
                    continue
                raise ValidationError(
                    f"Forward reference '{param_type}' for parameter '{param.name}' could not be resolved",
                    code="RESOLVE_FORWARD_REF_ERROR",
                    class_name=cls.__name__,
                    param_name=param.name,
                    forward_ref=param_type,
                )

        # Try to resolve from registry by type
        # Strategy: Look for registered instance of this type
        instance = registry.get_by_type(param_type)

        if instance is None:
            if allow_missing:
                missing.append(param.name)
                continue
            type_name = getattr(param_type, "__name__", str(param_type))
            raise NotFoundError(
                f"Dependency '{type_name}' required by {cls.__name__} not found in registry",
                code="RESOLVE_DEPENDENCY_NOT_FOUND",
                class_name=cls.__name__,
                param_name=param.name,
                param_type=type_name,
            )

        resolved[param.name] = instance

    return resolved


def x_resolve_dependencies__mutmut_3(  # noqa: C901
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
        import sys

        module = sys.modules.get(None)
        localns = vars(module) if module else {}
        hints = get_type_hints(cls.__init__, globalns=None, localns=localns)
    except NameError:
        # Forward reference error - collect what we can from annotations
        hints = {}
        sig = inspect.signature(cls.__init__)
        for param_name, param in sig.parameters.items():
            if param_name == "self":
                continue
            if param.annotation != inspect.Parameter.empty:
                # Use the annotation directly (may be a string)
                hints[param_name] = param.annotation
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

        # If param_type is a string (forward reference), try to resolve it
        if isinstance(param_type, str):
            # Look up the type in the class's module
            import sys

            module = sys.modules.get(cls.__module__)
            if module and hasattr(module, param_type):
                param_type = getattr(module, param_type)
            else:
                if allow_missing:
                    missing.append(param.name)
                    continue
                raise ValidationError(
                    f"Forward reference '{param_type}' for parameter '{param.name}' could not be resolved",
                    code="RESOLVE_FORWARD_REF_ERROR",
                    class_name=cls.__name__,
                    param_name=param.name,
                    forward_ref=param_type,
                )

        # Try to resolve from registry by type
        # Strategy: Look for registered instance of this type
        instance = registry.get_by_type(param_type)

        if instance is None:
            if allow_missing:
                missing.append(param.name)
                continue
            type_name = getattr(param_type, "__name__", str(param_type))
            raise NotFoundError(
                f"Dependency '{type_name}' required by {cls.__name__} not found in registry",
                code="RESOLVE_DEPENDENCY_NOT_FOUND",
                class_name=cls.__name__,
                param_name=param.name,
                param_type=type_name,
            )

        resolved[param.name] = instance

    return resolved


def x_resolve_dependencies__mutmut_4(  # noqa: C901
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
        import sys

        module = sys.modules.get(cls.__module__)
        localns = None
        hints = get_type_hints(cls.__init__, globalns=None, localns=localns)
    except NameError:
        # Forward reference error - collect what we can from annotations
        hints = {}
        sig = inspect.signature(cls.__init__)
        for param_name, param in sig.parameters.items():
            if param_name == "self":
                continue
            if param.annotation != inspect.Parameter.empty:
                # Use the annotation directly (may be a string)
                hints[param_name] = param.annotation
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

        # If param_type is a string (forward reference), try to resolve it
        if isinstance(param_type, str):
            # Look up the type in the class's module
            import sys

            module = sys.modules.get(cls.__module__)
            if module and hasattr(module, param_type):
                param_type = getattr(module, param_type)
            else:
                if allow_missing:
                    missing.append(param.name)
                    continue
                raise ValidationError(
                    f"Forward reference '{param_type}' for parameter '{param.name}' could not be resolved",
                    code="RESOLVE_FORWARD_REF_ERROR",
                    class_name=cls.__name__,
                    param_name=param.name,
                    forward_ref=param_type,
                )

        # Try to resolve from registry by type
        # Strategy: Look for registered instance of this type
        instance = registry.get_by_type(param_type)

        if instance is None:
            if allow_missing:
                missing.append(param.name)
                continue
            type_name = getattr(param_type, "__name__", str(param_type))
            raise NotFoundError(
                f"Dependency '{type_name}' required by {cls.__name__} not found in registry",
                code="RESOLVE_DEPENDENCY_NOT_FOUND",
                class_name=cls.__name__,
                param_name=param.name,
                param_type=type_name,
            )

        resolved[param.name] = instance

    return resolved


def x_resolve_dependencies__mutmut_5(  # noqa: C901
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
        import sys

        module = sys.modules.get(cls.__module__)
        localns = vars(None) if module else {}
        hints = get_type_hints(cls.__init__, globalns=None, localns=localns)
    except NameError:
        # Forward reference error - collect what we can from annotations
        hints = {}
        sig = inspect.signature(cls.__init__)
        for param_name, param in sig.parameters.items():
            if param_name == "self":
                continue
            if param.annotation != inspect.Parameter.empty:
                # Use the annotation directly (may be a string)
                hints[param_name] = param.annotation
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

        # If param_type is a string (forward reference), try to resolve it
        if isinstance(param_type, str):
            # Look up the type in the class's module
            import sys

            module = sys.modules.get(cls.__module__)
            if module and hasattr(module, param_type):
                param_type = getattr(module, param_type)
            else:
                if allow_missing:
                    missing.append(param.name)
                    continue
                raise ValidationError(
                    f"Forward reference '{param_type}' for parameter '{param.name}' could not be resolved",
                    code="RESOLVE_FORWARD_REF_ERROR",
                    class_name=cls.__name__,
                    param_name=param.name,
                    forward_ref=param_type,
                )

        # Try to resolve from registry by type
        # Strategy: Look for registered instance of this type
        instance = registry.get_by_type(param_type)

        if instance is None:
            if allow_missing:
                missing.append(param.name)
                continue
            type_name = getattr(param_type, "__name__", str(param_type))
            raise NotFoundError(
                f"Dependency '{type_name}' required by {cls.__name__} not found in registry",
                code="RESOLVE_DEPENDENCY_NOT_FOUND",
                class_name=cls.__name__,
                param_name=param.name,
                param_type=type_name,
            )

        resolved[param.name] = instance

    return resolved


def x_resolve_dependencies__mutmut_6(  # noqa: C901
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
        import sys

        module = sys.modules.get(cls.__module__)
        localns = vars(module) if module else {}
        hints = None
    except NameError:
        # Forward reference error - collect what we can from annotations
        hints = {}
        sig = inspect.signature(cls.__init__)
        for param_name, param in sig.parameters.items():
            if param_name == "self":
                continue
            if param.annotation != inspect.Parameter.empty:
                # Use the annotation directly (may be a string)
                hints[param_name] = param.annotation
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

        # If param_type is a string (forward reference), try to resolve it
        if isinstance(param_type, str):
            # Look up the type in the class's module
            import sys

            module = sys.modules.get(cls.__module__)
            if module and hasattr(module, param_type):
                param_type = getattr(module, param_type)
            else:
                if allow_missing:
                    missing.append(param.name)
                    continue
                raise ValidationError(
                    f"Forward reference '{param_type}' for parameter '{param.name}' could not be resolved",
                    code="RESOLVE_FORWARD_REF_ERROR",
                    class_name=cls.__name__,
                    param_name=param.name,
                    forward_ref=param_type,
                )

        # Try to resolve from registry by type
        # Strategy: Look for registered instance of this type
        instance = registry.get_by_type(param_type)

        if instance is None:
            if allow_missing:
                missing.append(param.name)
                continue
            type_name = getattr(param_type, "__name__", str(param_type))
            raise NotFoundError(
                f"Dependency '{type_name}' required by {cls.__name__} not found in registry",
                code="RESOLVE_DEPENDENCY_NOT_FOUND",
                class_name=cls.__name__,
                param_name=param.name,
                param_type=type_name,
            )

        resolved[param.name] = instance

    return resolved


def x_resolve_dependencies__mutmut_7(  # noqa: C901
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
        import sys

        module = sys.modules.get(cls.__module__)
        localns = vars(module) if module else {}
        hints = get_type_hints(None, globalns=None, localns=localns)
    except NameError:
        # Forward reference error - collect what we can from annotations
        hints = {}
        sig = inspect.signature(cls.__init__)
        for param_name, param in sig.parameters.items():
            if param_name == "self":
                continue
            if param.annotation != inspect.Parameter.empty:
                # Use the annotation directly (may be a string)
                hints[param_name] = param.annotation
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

        # If param_type is a string (forward reference), try to resolve it
        if isinstance(param_type, str):
            # Look up the type in the class's module
            import sys

            module = sys.modules.get(cls.__module__)
            if module and hasattr(module, param_type):
                param_type = getattr(module, param_type)
            else:
                if allow_missing:
                    missing.append(param.name)
                    continue
                raise ValidationError(
                    f"Forward reference '{param_type}' for parameter '{param.name}' could not be resolved",
                    code="RESOLVE_FORWARD_REF_ERROR",
                    class_name=cls.__name__,
                    param_name=param.name,
                    forward_ref=param_type,
                )

        # Try to resolve from registry by type
        # Strategy: Look for registered instance of this type
        instance = registry.get_by_type(param_type)

        if instance is None:
            if allow_missing:
                missing.append(param.name)
                continue
            type_name = getattr(param_type, "__name__", str(param_type))
            raise NotFoundError(
                f"Dependency '{type_name}' required by {cls.__name__} not found in registry",
                code="RESOLVE_DEPENDENCY_NOT_FOUND",
                class_name=cls.__name__,
                param_name=param.name,
                param_type=type_name,
            )

        resolved[param.name] = instance

    return resolved


def x_resolve_dependencies__mutmut_8(  # noqa: C901
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
        import sys

        module = sys.modules.get(cls.__module__)
        localns = vars(module) if module else {}
        hints = get_type_hints(cls.__init__, globalns=None, localns=None)
    except NameError:
        # Forward reference error - collect what we can from annotations
        hints = {}
        sig = inspect.signature(cls.__init__)
        for param_name, param in sig.parameters.items():
            if param_name == "self":
                continue
            if param.annotation != inspect.Parameter.empty:
                # Use the annotation directly (may be a string)
                hints[param_name] = param.annotation
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

        # If param_type is a string (forward reference), try to resolve it
        if isinstance(param_type, str):
            # Look up the type in the class's module
            import sys

            module = sys.modules.get(cls.__module__)
            if module and hasattr(module, param_type):
                param_type = getattr(module, param_type)
            else:
                if allow_missing:
                    missing.append(param.name)
                    continue
                raise ValidationError(
                    f"Forward reference '{param_type}' for parameter '{param.name}' could not be resolved",
                    code="RESOLVE_FORWARD_REF_ERROR",
                    class_name=cls.__name__,
                    param_name=param.name,
                    forward_ref=param_type,
                )

        # Try to resolve from registry by type
        # Strategy: Look for registered instance of this type
        instance = registry.get_by_type(param_type)

        if instance is None:
            if allow_missing:
                missing.append(param.name)
                continue
            type_name = getattr(param_type, "__name__", str(param_type))
            raise NotFoundError(
                f"Dependency '{type_name}' required by {cls.__name__} not found in registry",
                code="RESOLVE_DEPENDENCY_NOT_FOUND",
                class_name=cls.__name__,
                param_name=param.name,
                param_type=type_name,
            )

        resolved[param.name] = instance

    return resolved


def x_resolve_dependencies__mutmut_9(  # noqa: C901
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
        import sys

        module = sys.modules.get(cls.__module__)
        localns = vars(module) if module else {}
        hints = get_type_hints(globalns=None, localns=localns)
    except NameError:
        # Forward reference error - collect what we can from annotations
        hints = {}
        sig = inspect.signature(cls.__init__)
        for param_name, param in sig.parameters.items():
            if param_name == "self":
                continue
            if param.annotation != inspect.Parameter.empty:
                # Use the annotation directly (may be a string)
                hints[param_name] = param.annotation
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

        # If param_type is a string (forward reference), try to resolve it
        if isinstance(param_type, str):
            # Look up the type in the class's module
            import sys

            module = sys.modules.get(cls.__module__)
            if module and hasattr(module, param_type):
                param_type = getattr(module, param_type)
            else:
                if allow_missing:
                    missing.append(param.name)
                    continue
                raise ValidationError(
                    f"Forward reference '{param_type}' for parameter '{param.name}' could not be resolved",
                    code="RESOLVE_FORWARD_REF_ERROR",
                    class_name=cls.__name__,
                    param_name=param.name,
                    forward_ref=param_type,
                )

        # Try to resolve from registry by type
        # Strategy: Look for registered instance of this type
        instance = registry.get_by_type(param_type)

        if instance is None:
            if allow_missing:
                missing.append(param.name)
                continue
            type_name = getattr(param_type, "__name__", str(param_type))
            raise NotFoundError(
                f"Dependency '{type_name}' required by {cls.__name__} not found in registry",
                code="RESOLVE_DEPENDENCY_NOT_FOUND",
                class_name=cls.__name__,
                param_name=param.name,
                param_type=type_name,
            )

        resolved[param.name] = instance

    return resolved


def x_resolve_dependencies__mutmut_10(  # noqa: C901
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
        import sys

        module = sys.modules.get(cls.__module__)
        localns = vars(module) if module else {}
        hints = get_type_hints(cls.__init__, localns=localns)
    except NameError:
        # Forward reference error - collect what we can from annotations
        hints = {}
        sig = inspect.signature(cls.__init__)
        for param_name, param in sig.parameters.items():
            if param_name == "self":
                continue
            if param.annotation != inspect.Parameter.empty:
                # Use the annotation directly (may be a string)
                hints[param_name] = param.annotation
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

        # If param_type is a string (forward reference), try to resolve it
        if isinstance(param_type, str):
            # Look up the type in the class's module
            import sys

            module = sys.modules.get(cls.__module__)
            if module and hasattr(module, param_type):
                param_type = getattr(module, param_type)
            else:
                if allow_missing:
                    missing.append(param.name)
                    continue
                raise ValidationError(
                    f"Forward reference '{param_type}' for parameter '{param.name}' could not be resolved",
                    code="RESOLVE_FORWARD_REF_ERROR",
                    class_name=cls.__name__,
                    param_name=param.name,
                    forward_ref=param_type,
                )

        # Try to resolve from registry by type
        # Strategy: Look for registered instance of this type
        instance = registry.get_by_type(param_type)

        if instance is None:
            if allow_missing:
                missing.append(param.name)
                continue
            type_name = getattr(param_type, "__name__", str(param_type))
            raise NotFoundError(
                f"Dependency '{type_name}' required by {cls.__name__} not found in registry",
                code="RESOLVE_DEPENDENCY_NOT_FOUND",
                class_name=cls.__name__,
                param_name=param.name,
                param_type=type_name,
            )

        resolved[param.name] = instance

    return resolved


def x_resolve_dependencies__mutmut_11(  # noqa: C901
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
        import sys

        module = sys.modules.get(cls.__module__)
        localns = vars(module) if module else {}
        hints = get_type_hints(cls.__init__, globalns=None, )
    except NameError:
        # Forward reference error - collect what we can from annotations
        hints = {}
        sig = inspect.signature(cls.__init__)
        for param_name, param in sig.parameters.items():
            if param_name == "self":
                continue
            if param.annotation != inspect.Parameter.empty:
                # Use the annotation directly (may be a string)
                hints[param_name] = param.annotation
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

        # If param_type is a string (forward reference), try to resolve it
        if isinstance(param_type, str):
            # Look up the type in the class's module
            import sys

            module = sys.modules.get(cls.__module__)
            if module and hasattr(module, param_type):
                param_type = getattr(module, param_type)
            else:
                if allow_missing:
                    missing.append(param.name)
                    continue
                raise ValidationError(
                    f"Forward reference '{param_type}' for parameter '{param.name}' could not be resolved",
                    code="RESOLVE_FORWARD_REF_ERROR",
                    class_name=cls.__name__,
                    param_name=param.name,
                    forward_ref=param_type,
                )

        # Try to resolve from registry by type
        # Strategy: Look for registered instance of this type
        instance = registry.get_by_type(param_type)

        if instance is None:
            if allow_missing:
                missing.append(param.name)
                continue
            type_name = getattr(param_type, "__name__", str(param_type))
            raise NotFoundError(
                f"Dependency '{type_name}' required by {cls.__name__} not found in registry",
                code="RESOLVE_DEPENDENCY_NOT_FOUND",
                class_name=cls.__name__,
                param_name=param.name,
                param_type=type_name,
            )

        resolved[param.name] = instance

    return resolved


def x_resolve_dependencies__mutmut_12(  # noqa: C901
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
        import sys

        module = sys.modules.get(cls.__module__)
        localns = vars(module) if module else {}
        hints = get_type_hints(cls.__init__, globalns=None, localns=localns)
    except NameError:
        # Forward reference error - collect what we can from annotations
        hints = None
        sig = inspect.signature(cls.__init__)
        for param_name, param in sig.parameters.items():
            if param_name == "self":
                continue
            if param.annotation != inspect.Parameter.empty:
                # Use the annotation directly (may be a string)
                hints[param_name] = param.annotation
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

        # If param_type is a string (forward reference), try to resolve it
        if isinstance(param_type, str):
            # Look up the type in the class's module
            import sys

            module = sys.modules.get(cls.__module__)
            if module and hasattr(module, param_type):
                param_type = getattr(module, param_type)
            else:
                if allow_missing:
                    missing.append(param.name)
                    continue
                raise ValidationError(
                    f"Forward reference '{param_type}' for parameter '{param.name}' could not be resolved",
                    code="RESOLVE_FORWARD_REF_ERROR",
                    class_name=cls.__name__,
                    param_name=param.name,
                    forward_ref=param_type,
                )

        # Try to resolve from registry by type
        # Strategy: Look for registered instance of this type
        instance = registry.get_by_type(param_type)

        if instance is None:
            if allow_missing:
                missing.append(param.name)
                continue
            type_name = getattr(param_type, "__name__", str(param_type))
            raise NotFoundError(
                f"Dependency '{type_name}' required by {cls.__name__} not found in registry",
                code="RESOLVE_DEPENDENCY_NOT_FOUND",
                class_name=cls.__name__,
                param_name=param.name,
                param_type=type_name,
            )

        resolved[param.name] = instance

    return resolved


def x_resolve_dependencies__mutmut_13(  # noqa: C901
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
        import sys

        module = sys.modules.get(cls.__module__)
        localns = vars(module) if module else {}
        hints = get_type_hints(cls.__init__, globalns=None, localns=localns)
    except NameError:
        # Forward reference error - collect what we can from annotations
        hints = {}
        sig = None
        for param_name, param in sig.parameters.items():
            if param_name == "self":
                continue
            if param.annotation != inspect.Parameter.empty:
                # Use the annotation directly (may be a string)
                hints[param_name] = param.annotation
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

        # If param_type is a string (forward reference), try to resolve it
        if isinstance(param_type, str):
            # Look up the type in the class's module
            import sys

            module = sys.modules.get(cls.__module__)
            if module and hasattr(module, param_type):
                param_type = getattr(module, param_type)
            else:
                if allow_missing:
                    missing.append(param.name)
                    continue
                raise ValidationError(
                    f"Forward reference '{param_type}' for parameter '{param.name}' could not be resolved",
                    code="RESOLVE_FORWARD_REF_ERROR",
                    class_name=cls.__name__,
                    param_name=param.name,
                    forward_ref=param_type,
                )

        # Try to resolve from registry by type
        # Strategy: Look for registered instance of this type
        instance = registry.get_by_type(param_type)

        if instance is None:
            if allow_missing:
                missing.append(param.name)
                continue
            type_name = getattr(param_type, "__name__", str(param_type))
            raise NotFoundError(
                f"Dependency '{type_name}' required by {cls.__name__} not found in registry",
                code="RESOLVE_DEPENDENCY_NOT_FOUND",
                class_name=cls.__name__,
                param_name=param.name,
                param_type=type_name,
            )

        resolved[param.name] = instance

    return resolved


def x_resolve_dependencies__mutmut_14(  # noqa: C901
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
        import sys

        module = sys.modules.get(cls.__module__)
        localns = vars(module) if module else {}
        hints = get_type_hints(cls.__init__, globalns=None, localns=localns)
    except NameError:
        # Forward reference error - collect what we can from annotations
        hints = {}
        sig = inspect.signature(None)
        for param_name, param in sig.parameters.items():
            if param_name == "self":
                continue
            if param.annotation != inspect.Parameter.empty:
                # Use the annotation directly (may be a string)
                hints[param_name] = param.annotation
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

        # If param_type is a string (forward reference), try to resolve it
        if isinstance(param_type, str):
            # Look up the type in the class's module
            import sys

            module = sys.modules.get(cls.__module__)
            if module and hasattr(module, param_type):
                param_type = getattr(module, param_type)
            else:
                if allow_missing:
                    missing.append(param.name)
                    continue
                raise ValidationError(
                    f"Forward reference '{param_type}' for parameter '{param.name}' could not be resolved",
                    code="RESOLVE_FORWARD_REF_ERROR",
                    class_name=cls.__name__,
                    param_name=param.name,
                    forward_ref=param_type,
                )

        # Try to resolve from registry by type
        # Strategy: Look for registered instance of this type
        instance = registry.get_by_type(param_type)

        if instance is None:
            if allow_missing:
                missing.append(param.name)
                continue
            type_name = getattr(param_type, "__name__", str(param_type))
            raise NotFoundError(
                f"Dependency '{type_name}' required by {cls.__name__} not found in registry",
                code="RESOLVE_DEPENDENCY_NOT_FOUND",
                class_name=cls.__name__,
                param_name=param.name,
                param_type=type_name,
            )

        resolved[param.name] = instance

    return resolved


def x_resolve_dependencies__mutmut_15(  # noqa: C901
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
        import sys

        module = sys.modules.get(cls.__module__)
        localns = vars(module) if module else {}
        hints = get_type_hints(cls.__init__, globalns=None, localns=localns)
    except NameError:
        # Forward reference error - collect what we can from annotations
        hints = {}
        sig = inspect.signature(cls.__init__)
        for param_name, param in sig.parameters.items():
            if param_name != "self":
                continue
            if param.annotation != inspect.Parameter.empty:
                # Use the annotation directly (may be a string)
                hints[param_name] = param.annotation
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

        # If param_type is a string (forward reference), try to resolve it
        if isinstance(param_type, str):
            # Look up the type in the class's module
            import sys

            module = sys.modules.get(cls.__module__)
            if module and hasattr(module, param_type):
                param_type = getattr(module, param_type)
            else:
                if allow_missing:
                    missing.append(param.name)
                    continue
                raise ValidationError(
                    f"Forward reference '{param_type}' for parameter '{param.name}' could not be resolved",
                    code="RESOLVE_FORWARD_REF_ERROR",
                    class_name=cls.__name__,
                    param_name=param.name,
                    forward_ref=param_type,
                )

        # Try to resolve from registry by type
        # Strategy: Look for registered instance of this type
        instance = registry.get_by_type(param_type)

        if instance is None:
            if allow_missing:
                missing.append(param.name)
                continue
            type_name = getattr(param_type, "__name__", str(param_type))
            raise NotFoundError(
                f"Dependency '{type_name}' required by {cls.__name__} not found in registry",
                code="RESOLVE_DEPENDENCY_NOT_FOUND",
                class_name=cls.__name__,
                param_name=param.name,
                param_type=type_name,
            )

        resolved[param.name] = instance

    return resolved


def x_resolve_dependencies__mutmut_16(  # noqa: C901
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
        import sys

        module = sys.modules.get(cls.__module__)
        localns = vars(module) if module else {}
        hints = get_type_hints(cls.__init__, globalns=None, localns=localns)
    except NameError:
        # Forward reference error - collect what we can from annotations
        hints = {}
        sig = inspect.signature(cls.__init__)
        for param_name, param in sig.parameters.items():
            if param_name == "XXselfXX":
                continue
            if param.annotation != inspect.Parameter.empty:
                # Use the annotation directly (may be a string)
                hints[param_name] = param.annotation
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

        # If param_type is a string (forward reference), try to resolve it
        if isinstance(param_type, str):
            # Look up the type in the class's module
            import sys

            module = sys.modules.get(cls.__module__)
            if module and hasattr(module, param_type):
                param_type = getattr(module, param_type)
            else:
                if allow_missing:
                    missing.append(param.name)
                    continue
                raise ValidationError(
                    f"Forward reference '{param_type}' for parameter '{param.name}' could not be resolved",
                    code="RESOLVE_FORWARD_REF_ERROR",
                    class_name=cls.__name__,
                    param_name=param.name,
                    forward_ref=param_type,
                )

        # Try to resolve from registry by type
        # Strategy: Look for registered instance of this type
        instance = registry.get_by_type(param_type)

        if instance is None:
            if allow_missing:
                missing.append(param.name)
                continue
            type_name = getattr(param_type, "__name__", str(param_type))
            raise NotFoundError(
                f"Dependency '{type_name}' required by {cls.__name__} not found in registry",
                code="RESOLVE_DEPENDENCY_NOT_FOUND",
                class_name=cls.__name__,
                param_name=param.name,
                param_type=type_name,
            )

        resolved[param.name] = instance

    return resolved


def x_resolve_dependencies__mutmut_17(  # noqa: C901
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
        import sys

        module = sys.modules.get(cls.__module__)
        localns = vars(module) if module else {}
        hints = get_type_hints(cls.__init__, globalns=None, localns=localns)
    except NameError:
        # Forward reference error - collect what we can from annotations
        hints = {}
        sig = inspect.signature(cls.__init__)
        for param_name, param in sig.parameters.items():
            if param_name == "SELF":
                continue
            if param.annotation != inspect.Parameter.empty:
                # Use the annotation directly (may be a string)
                hints[param_name] = param.annotation
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

        # If param_type is a string (forward reference), try to resolve it
        if isinstance(param_type, str):
            # Look up the type in the class's module
            import sys

            module = sys.modules.get(cls.__module__)
            if module and hasattr(module, param_type):
                param_type = getattr(module, param_type)
            else:
                if allow_missing:
                    missing.append(param.name)
                    continue
                raise ValidationError(
                    f"Forward reference '{param_type}' for parameter '{param.name}' could not be resolved",
                    code="RESOLVE_FORWARD_REF_ERROR",
                    class_name=cls.__name__,
                    param_name=param.name,
                    forward_ref=param_type,
                )

        # Try to resolve from registry by type
        # Strategy: Look for registered instance of this type
        instance = registry.get_by_type(param_type)

        if instance is None:
            if allow_missing:
                missing.append(param.name)
                continue
            type_name = getattr(param_type, "__name__", str(param_type))
            raise NotFoundError(
                f"Dependency '{type_name}' required by {cls.__name__} not found in registry",
                code="RESOLVE_DEPENDENCY_NOT_FOUND",
                class_name=cls.__name__,
                param_name=param.name,
                param_type=type_name,
            )

        resolved[param.name] = instance

    return resolved


def x_resolve_dependencies__mutmut_18(  # noqa: C901
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
        import sys

        module = sys.modules.get(cls.__module__)
        localns = vars(module) if module else {}
        hints = get_type_hints(cls.__init__, globalns=None, localns=localns)
    except NameError:
        # Forward reference error - collect what we can from annotations
        hints = {}
        sig = inspect.signature(cls.__init__)
        for param_name, param in sig.parameters.items():
            if param_name == "self":
                break
            if param.annotation != inspect.Parameter.empty:
                # Use the annotation directly (may be a string)
                hints[param_name] = param.annotation
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

        # If param_type is a string (forward reference), try to resolve it
        if isinstance(param_type, str):
            # Look up the type in the class's module
            import sys

            module = sys.modules.get(cls.__module__)
            if module and hasattr(module, param_type):
                param_type = getattr(module, param_type)
            else:
                if allow_missing:
                    missing.append(param.name)
                    continue
                raise ValidationError(
                    f"Forward reference '{param_type}' for parameter '{param.name}' could not be resolved",
                    code="RESOLVE_FORWARD_REF_ERROR",
                    class_name=cls.__name__,
                    param_name=param.name,
                    forward_ref=param_type,
                )

        # Try to resolve from registry by type
        # Strategy: Look for registered instance of this type
        instance = registry.get_by_type(param_type)

        if instance is None:
            if allow_missing:
                missing.append(param.name)
                continue
            type_name = getattr(param_type, "__name__", str(param_type))
            raise NotFoundError(
                f"Dependency '{type_name}' required by {cls.__name__} not found in registry",
                code="RESOLVE_DEPENDENCY_NOT_FOUND",
                class_name=cls.__name__,
                param_name=param.name,
                param_type=type_name,
            )

        resolved[param.name] = instance

    return resolved


def x_resolve_dependencies__mutmut_19(  # noqa: C901
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
        import sys

        module = sys.modules.get(cls.__module__)
        localns = vars(module) if module else {}
        hints = get_type_hints(cls.__init__, globalns=None, localns=localns)
    except NameError:
        # Forward reference error - collect what we can from annotations
        hints = {}
        sig = inspect.signature(cls.__init__)
        for param_name, param in sig.parameters.items():
            if param_name == "self":
                continue
            if param.annotation == inspect.Parameter.empty:
                # Use the annotation directly (may be a string)
                hints[param_name] = param.annotation
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

        # If param_type is a string (forward reference), try to resolve it
        if isinstance(param_type, str):
            # Look up the type in the class's module
            import sys

            module = sys.modules.get(cls.__module__)
            if module and hasattr(module, param_type):
                param_type = getattr(module, param_type)
            else:
                if allow_missing:
                    missing.append(param.name)
                    continue
                raise ValidationError(
                    f"Forward reference '{param_type}' for parameter '{param.name}' could not be resolved",
                    code="RESOLVE_FORWARD_REF_ERROR",
                    class_name=cls.__name__,
                    param_name=param.name,
                    forward_ref=param_type,
                )

        # Try to resolve from registry by type
        # Strategy: Look for registered instance of this type
        instance = registry.get_by_type(param_type)

        if instance is None:
            if allow_missing:
                missing.append(param.name)
                continue
            type_name = getattr(param_type, "__name__", str(param_type))
            raise NotFoundError(
                f"Dependency '{type_name}' required by {cls.__name__} not found in registry",
                code="RESOLVE_DEPENDENCY_NOT_FOUND",
                class_name=cls.__name__,
                param_name=param.name,
                param_type=type_name,
            )

        resolved[param.name] = instance

    return resolved


def x_resolve_dependencies__mutmut_20(  # noqa: C901
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
        import sys

        module = sys.modules.get(cls.__module__)
        localns = vars(module) if module else {}
        hints = get_type_hints(cls.__init__, globalns=None, localns=localns)
    except NameError:
        # Forward reference error - collect what we can from annotations
        hints = {}
        sig = inspect.signature(cls.__init__)
        for param_name, param in sig.parameters.items():
            if param_name == "self":
                continue
            if param.annotation != inspect.Parameter.empty:
                # Use the annotation directly (may be a string)
                hints[param_name] = None
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

        # If param_type is a string (forward reference), try to resolve it
        if isinstance(param_type, str):
            # Look up the type in the class's module
            import sys

            module = sys.modules.get(cls.__module__)
            if module and hasattr(module, param_type):
                param_type = getattr(module, param_type)
            else:
                if allow_missing:
                    missing.append(param.name)
                    continue
                raise ValidationError(
                    f"Forward reference '{param_type}' for parameter '{param.name}' could not be resolved",
                    code="RESOLVE_FORWARD_REF_ERROR",
                    class_name=cls.__name__,
                    param_name=param.name,
                    forward_ref=param_type,
                )

        # Try to resolve from registry by type
        # Strategy: Look for registered instance of this type
        instance = registry.get_by_type(param_type)

        if instance is None:
            if allow_missing:
                missing.append(param.name)
                continue
            type_name = getattr(param_type, "__name__", str(param_type))
            raise NotFoundError(
                f"Dependency '{type_name}' required by {cls.__name__} not found in registry",
                code="RESOLVE_DEPENDENCY_NOT_FOUND",
                class_name=cls.__name__,
                param_name=param.name,
                param_type=type_name,
            )

        resolved[param.name] = instance

    return resolved


def x_resolve_dependencies__mutmut_21(  # noqa: C901
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
        import sys

        module = sys.modules.get(cls.__module__)
        localns = vars(module) if module else {}
        hints = get_type_hints(cls.__init__, globalns=None, localns=localns)
    except NameError:
        # Forward reference error - collect what we can from annotations
        hints = {}
        sig = inspect.signature(cls.__init__)
        for param_name, param in sig.parameters.items():
            if param_name == "self":
                continue
            if param.annotation != inspect.Parameter.empty:
                # Use the annotation directly (may be a string)
                hints[param_name] = param.annotation
    except Exception as e:
        raise ValidationError(
            None,
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

        # If param_type is a string (forward reference), try to resolve it
        if isinstance(param_type, str):
            # Look up the type in the class's module
            import sys

            module = sys.modules.get(cls.__module__)
            if module and hasattr(module, param_type):
                param_type = getattr(module, param_type)
            else:
                if allow_missing:
                    missing.append(param.name)
                    continue
                raise ValidationError(
                    f"Forward reference '{param_type}' for parameter '{param.name}' could not be resolved",
                    code="RESOLVE_FORWARD_REF_ERROR",
                    class_name=cls.__name__,
                    param_name=param.name,
                    forward_ref=param_type,
                )

        # Try to resolve from registry by type
        # Strategy: Look for registered instance of this type
        instance = registry.get_by_type(param_type)

        if instance is None:
            if allow_missing:
                missing.append(param.name)
                continue
            type_name = getattr(param_type, "__name__", str(param_type))
            raise NotFoundError(
                f"Dependency '{type_name}' required by {cls.__name__} not found in registry",
                code="RESOLVE_DEPENDENCY_NOT_FOUND",
                class_name=cls.__name__,
                param_name=param.name,
                param_type=type_name,
            )

        resolved[param.name] = instance

    return resolved


def x_resolve_dependencies__mutmut_22(  # noqa: C901
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
        import sys

        module = sys.modules.get(cls.__module__)
        localns = vars(module) if module else {}
        hints = get_type_hints(cls.__init__, globalns=None, localns=localns)
    except NameError:
        # Forward reference error - collect what we can from annotations
        hints = {}
        sig = inspect.signature(cls.__init__)
        for param_name, param in sig.parameters.items():
            if param_name == "self":
                continue
            if param.annotation != inspect.Parameter.empty:
                # Use the annotation directly (may be a string)
                hints[param_name] = param.annotation
    except Exception as e:
        raise ValidationError(
            f"Failed to get type hints for {cls.__name__}.__init__: {e}",
            code=None,
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

        # If param_type is a string (forward reference), try to resolve it
        if isinstance(param_type, str):
            # Look up the type in the class's module
            import sys

            module = sys.modules.get(cls.__module__)
            if module and hasattr(module, param_type):
                param_type = getattr(module, param_type)
            else:
                if allow_missing:
                    missing.append(param.name)
                    continue
                raise ValidationError(
                    f"Forward reference '{param_type}' for parameter '{param.name}' could not be resolved",
                    code="RESOLVE_FORWARD_REF_ERROR",
                    class_name=cls.__name__,
                    param_name=param.name,
                    forward_ref=param_type,
                )

        # Try to resolve from registry by type
        # Strategy: Look for registered instance of this type
        instance = registry.get_by_type(param_type)

        if instance is None:
            if allow_missing:
                missing.append(param.name)
                continue
            type_name = getattr(param_type, "__name__", str(param_type))
            raise NotFoundError(
                f"Dependency '{type_name}' required by {cls.__name__} not found in registry",
                code="RESOLVE_DEPENDENCY_NOT_FOUND",
                class_name=cls.__name__,
                param_name=param.name,
                param_type=type_name,
            )

        resolved[param.name] = instance

    return resolved


def x_resolve_dependencies__mutmut_23(  # noqa: C901
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
        import sys

        module = sys.modules.get(cls.__module__)
        localns = vars(module) if module else {}
        hints = get_type_hints(cls.__init__, globalns=None, localns=localns)
    except NameError:
        # Forward reference error - collect what we can from annotations
        hints = {}
        sig = inspect.signature(cls.__init__)
        for param_name, param in sig.parameters.items():
            if param_name == "self":
                continue
            if param.annotation != inspect.Parameter.empty:
                # Use the annotation directly (may be a string)
                hints[param_name] = param.annotation
    except Exception as e:
        raise ValidationError(
            f"Failed to get type hints for {cls.__name__}.__init__: {e}",
            code="RESOLVE_TYPE_HINT_ERROR",
            class_name=None,
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

        # If param_type is a string (forward reference), try to resolve it
        if isinstance(param_type, str):
            # Look up the type in the class's module
            import sys

            module = sys.modules.get(cls.__module__)
            if module and hasattr(module, param_type):
                param_type = getattr(module, param_type)
            else:
                if allow_missing:
                    missing.append(param.name)
                    continue
                raise ValidationError(
                    f"Forward reference '{param_type}' for parameter '{param.name}' could not be resolved",
                    code="RESOLVE_FORWARD_REF_ERROR",
                    class_name=cls.__name__,
                    param_name=param.name,
                    forward_ref=param_type,
                )

        # Try to resolve from registry by type
        # Strategy: Look for registered instance of this type
        instance = registry.get_by_type(param_type)

        if instance is None:
            if allow_missing:
                missing.append(param.name)
                continue
            type_name = getattr(param_type, "__name__", str(param_type))
            raise NotFoundError(
                f"Dependency '{type_name}' required by {cls.__name__} not found in registry",
                code="RESOLVE_DEPENDENCY_NOT_FOUND",
                class_name=cls.__name__,
                param_name=param.name,
                param_type=type_name,
            )

        resolved[param.name] = instance

    return resolved


def x_resolve_dependencies__mutmut_24(  # noqa: C901
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
        import sys

        module = sys.modules.get(cls.__module__)
        localns = vars(module) if module else {}
        hints = get_type_hints(cls.__init__, globalns=None, localns=localns)
    except NameError:
        # Forward reference error - collect what we can from annotations
        hints = {}
        sig = inspect.signature(cls.__init__)
        for param_name, param in sig.parameters.items():
            if param_name == "self":
                continue
            if param.annotation != inspect.Parameter.empty:
                # Use the annotation directly (may be a string)
                hints[param_name] = param.annotation
    except Exception as e:
        raise ValidationError(
            f"Failed to get type hints for {cls.__name__}.__init__: {e}",
            code="RESOLVE_TYPE_HINT_ERROR",
            class_name=cls.__name__,
            cause=None,
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

        # If param_type is a string (forward reference), try to resolve it
        if isinstance(param_type, str):
            # Look up the type in the class's module
            import sys

            module = sys.modules.get(cls.__module__)
            if module and hasattr(module, param_type):
                param_type = getattr(module, param_type)
            else:
                if allow_missing:
                    missing.append(param.name)
                    continue
                raise ValidationError(
                    f"Forward reference '{param_type}' for parameter '{param.name}' could not be resolved",
                    code="RESOLVE_FORWARD_REF_ERROR",
                    class_name=cls.__name__,
                    param_name=param.name,
                    forward_ref=param_type,
                )

        # Try to resolve from registry by type
        # Strategy: Look for registered instance of this type
        instance = registry.get_by_type(param_type)

        if instance is None:
            if allow_missing:
                missing.append(param.name)
                continue
            type_name = getattr(param_type, "__name__", str(param_type))
            raise NotFoundError(
                f"Dependency '{type_name}' required by {cls.__name__} not found in registry",
                code="RESOLVE_DEPENDENCY_NOT_FOUND",
                class_name=cls.__name__,
                param_name=param.name,
                param_type=type_name,
            )

        resolved[param.name] = instance

    return resolved


def x_resolve_dependencies__mutmut_25(  # noqa: C901
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
        import sys

        module = sys.modules.get(cls.__module__)
        localns = vars(module) if module else {}
        hints = get_type_hints(cls.__init__, globalns=None, localns=localns)
    except NameError:
        # Forward reference error - collect what we can from annotations
        hints = {}
        sig = inspect.signature(cls.__init__)
        for param_name, param in sig.parameters.items():
            if param_name == "self":
                continue
            if param.annotation != inspect.Parameter.empty:
                # Use the annotation directly (may be a string)
                hints[param_name] = param.annotation
    except Exception as e:
        raise ValidationError(
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

        # If param_type is a string (forward reference), try to resolve it
        if isinstance(param_type, str):
            # Look up the type in the class's module
            import sys

            module = sys.modules.get(cls.__module__)
            if module and hasattr(module, param_type):
                param_type = getattr(module, param_type)
            else:
                if allow_missing:
                    missing.append(param.name)
                    continue
                raise ValidationError(
                    f"Forward reference '{param_type}' for parameter '{param.name}' could not be resolved",
                    code="RESOLVE_FORWARD_REF_ERROR",
                    class_name=cls.__name__,
                    param_name=param.name,
                    forward_ref=param_type,
                )

        # Try to resolve from registry by type
        # Strategy: Look for registered instance of this type
        instance = registry.get_by_type(param_type)

        if instance is None:
            if allow_missing:
                missing.append(param.name)
                continue
            type_name = getattr(param_type, "__name__", str(param_type))
            raise NotFoundError(
                f"Dependency '{type_name}' required by {cls.__name__} not found in registry",
                code="RESOLVE_DEPENDENCY_NOT_FOUND",
                class_name=cls.__name__,
                param_name=param.name,
                param_type=type_name,
            )

        resolved[param.name] = instance

    return resolved


def x_resolve_dependencies__mutmut_26(  # noqa: C901
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
        import sys

        module = sys.modules.get(cls.__module__)
        localns = vars(module) if module else {}
        hints = get_type_hints(cls.__init__, globalns=None, localns=localns)
    except NameError:
        # Forward reference error - collect what we can from annotations
        hints = {}
        sig = inspect.signature(cls.__init__)
        for param_name, param in sig.parameters.items():
            if param_name == "self":
                continue
            if param.annotation != inspect.Parameter.empty:
                # Use the annotation directly (may be a string)
                hints[param_name] = param.annotation
    except Exception as e:
        raise ValidationError(
            f"Failed to get type hints for {cls.__name__}.__init__: {e}",
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

        # If param_type is a string (forward reference), try to resolve it
        if isinstance(param_type, str):
            # Look up the type in the class's module
            import sys

            module = sys.modules.get(cls.__module__)
            if module and hasattr(module, param_type):
                param_type = getattr(module, param_type)
            else:
                if allow_missing:
                    missing.append(param.name)
                    continue
                raise ValidationError(
                    f"Forward reference '{param_type}' for parameter '{param.name}' could not be resolved",
                    code="RESOLVE_FORWARD_REF_ERROR",
                    class_name=cls.__name__,
                    param_name=param.name,
                    forward_ref=param_type,
                )

        # Try to resolve from registry by type
        # Strategy: Look for registered instance of this type
        instance = registry.get_by_type(param_type)

        if instance is None:
            if allow_missing:
                missing.append(param.name)
                continue
            type_name = getattr(param_type, "__name__", str(param_type))
            raise NotFoundError(
                f"Dependency '{type_name}' required by {cls.__name__} not found in registry",
                code="RESOLVE_DEPENDENCY_NOT_FOUND",
                class_name=cls.__name__,
                param_name=param.name,
                param_type=type_name,
            )

        resolved[param.name] = instance

    return resolved


def x_resolve_dependencies__mutmut_27(  # noqa: C901
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
        import sys

        module = sys.modules.get(cls.__module__)
        localns = vars(module) if module else {}
        hints = get_type_hints(cls.__init__, globalns=None, localns=localns)
    except NameError:
        # Forward reference error - collect what we can from annotations
        hints = {}
        sig = inspect.signature(cls.__init__)
        for param_name, param in sig.parameters.items():
            if param_name == "self":
                continue
            if param.annotation != inspect.Parameter.empty:
                # Use the annotation directly (may be a string)
                hints[param_name] = param.annotation
    except Exception as e:
        raise ValidationError(
            f"Failed to get type hints for {cls.__name__}.__init__: {e}",
            code="RESOLVE_TYPE_HINT_ERROR",
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

        # If param_type is a string (forward reference), try to resolve it
        if isinstance(param_type, str):
            # Look up the type in the class's module
            import sys

            module = sys.modules.get(cls.__module__)
            if module and hasattr(module, param_type):
                param_type = getattr(module, param_type)
            else:
                if allow_missing:
                    missing.append(param.name)
                    continue
                raise ValidationError(
                    f"Forward reference '{param_type}' for parameter '{param.name}' could not be resolved",
                    code="RESOLVE_FORWARD_REF_ERROR",
                    class_name=cls.__name__,
                    param_name=param.name,
                    forward_ref=param_type,
                )

        # Try to resolve from registry by type
        # Strategy: Look for registered instance of this type
        instance = registry.get_by_type(param_type)

        if instance is None:
            if allow_missing:
                missing.append(param.name)
                continue
            type_name = getattr(param_type, "__name__", str(param_type))
            raise NotFoundError(
                f"Dependency '{type_name}' required by {cls.__name__} not found in registry",
                code="RESOLVE_DEPENDENCY_NOT_FOUND",
                class_name=cls.__name__,
                param_name=param.name,
                param_type=type_name,
            )

        resolved[param.name] = instance

    return resolved


def x_resolve_dependencies__mutmut_28(  # noqa: C901
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
        import sys

        module = sys.modules.get(cls.__module__)
        localns = vars(module) if module else {}
        hints = get_type_hints(cls.__init__, globalns=None, localns=localns)
    except NameError:
        # Forward reference error - collect what we can from annotations
        hints = {}
        sig = inspect.signature(cls.__init__)
        for param_name, param in sig.parameters.items():
            if param_name == "self":
                continue
            if param.annotation != inspect.Parameter.empty:
                # Use the annotation directly (may be a string)
                hints[param_name] = param.annotation
    except Exception as e:
        raise ValidationError(
            f"Failed to get type hints for {cls.__name__}.__init__: {e}",
            code="RESOLVE_TYPE_HINT_ERROR",
            class_name=cls.__name__,
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

        # If param_type is a string (forward reference), try to resolve it
        if isinstance(param_type, str):
            # Look up the type in the class's module
            import sys

            module = sys.modules.get(cls.__module__)
            if module and hasattr(module, param_type):
                param_type = getattr(module, param_type)
            else:
                if allow_missing:
                    missing.append(param.name)
                    continue
                raise ValidationError(
                    f"Forward reference '{param_type}' for parameter '{param.name}' could not be resolved",
                    code="RESOLVE_FORWARD_REF_ERROR",
                    class_name=cls.__name__,
                    param_name=param.name,
                    forward_ref=param_type,
                )

        # Try to resolve from registry by type
        # Strategy: Look for registered instance of this type
        instance = registry.get_by_type(param_type)

        if instance is None:
            if allow_missing:
                missing.append(param.name)
                continue
            type_name = getattr(param_type, "__name__", str(param_type))
            raise NotFoundError(
                f"Dependency '{type_name}' required by {cls.__name__} not found in registry",
                code="RESOLVE_DEPENDENCY_NOT_FOUND",
                class_name=cls.__name__,
                param_name=param.name,
                param_type=type_name,
            )

        resolved[param.name] = instance

    return resolved


def x_resolve_dependencies__mutmut_29(  # noqa: C901
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
        import sys

        module = sys.modules.get(cls.__module__)
        localns = vars(module) if module else {}
        hints = get_type_hints(cls.__init__, globalns=None, localns=localns)
    except NameError:
        # Forward reference error - collect what we can from annotations
        hints = {}
        sig = inspect.signature(cls.__init__)
        for param_name, param in sig.parameters.items():
            if param_name == "self":
                continue
            if param.annotation != inspect.Parameter.empty:
                # Use the annotation directly (may be a string)
                hints[param_name] = param.annotation
    except Exception as e:
        raise ValidationError(
            f"Failed to get type hints for {cls.__name__}.__init__: {e}",
            code="XXRESOLVE_TYPE_HINT_ERRORXX",
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

        # If param_type is a string (forward reference), try to resolve it
        if isinstance(param_type, str):
            # Look up the type in the class's module
            import sys

            module = sys.modules.get(cls.__module__)
            if module and hasattr(module, param_type):
                param_type = getattr(module, param_type)
            else:
                if allow_missing:
                    missing.append(param.name)
                    continue
                raise ValidationError(
                    f"Forward reference '{param_type}' for parameter '{param.name}' could not be resolved",
                    code="RESOLVE_FORWARD_REF_ERROR",
                    class_name=cls.__name__,
                    param_name=param.name,
                    forward_ref=param_type,
                )

        # Try to resolve from registry by type
        # Strategy: Look for registered instance of this type
        instance = registry.get_by_type(param_type)

        if instance is None:
            if allow_missing:
                missing.append(param.name)
                continue
            type_name = getattr(param_type, "__name__", str(param_type))
            raise NotFoundError(
                f"Dependency '{type_name}' required by {cls.__name__} not found in registry",
                code="RESOLVE_DEPENDENCY_NOT_FOUND",
                class_name=cls.__name__,
                param_name=param.name,
                param_type=type_name,
            )

        resolved[param.name] = instance

    return resolved


def x_resolve_dependencies__mutmut_30(  # noqa: C901
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
        import sys

        module = sys.modules.get(cls.__module__)
        localns = vars(module) if module else {}
        hints = get_type_hints(cls.__init__, globalns=None, localns=localns)
    except NameError:
        # Forward reference error - collect what we can from annotations
        hints = {}
        sig = inspect.signature(cls.__init__)
        for param_name, param in sig.parameters.items():
            if param_name == "self":
                continue
            if param.annotation != inspect.Parameter.empty:
                # Use the annotation directly (may be a string)
                hints[param_name] = param.annotation
    except Exception as e:
        raise ValidationError(
            f"Failed to get type hints for {cls.__name__}.__init__: {e}",
            code="resolve_type_hint_error",
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

        # If param_type is a string (forward reference), try to resolve it
        if isinstance(param_type, str):
            # Look up the type in the class's module
            import sys

            module = sys.modules.get(cls.__module__)
            if module and hasattr(module, param_type):
                param_type = getattr(module, param_type)
            else:
                if allow_missing:
                    missing.append(param.name)
                    continue
                raise ValidationError(
                    f"Forward reference '{param_type}' for parameter '{param.name}' could not be resolved",
                    code="RESOLVE_FORWARD_REF_ERROR",
                    class_name=cls.__name__,
                    param_name=param.name,
                    forward_ref=param_type,
                )

        # Try to resolve from registry by type
        # Strategy: Look for registered instance of this type
        instance = registry.get_by_type(param_type)

        if instance is None:
            if allow_missing:
                missing.append(param.name)
                continue
            type_name = getattr(param_type, "__name__", str(param_type))
            raise NotFoundError(
                f"Dependency '{type_name}' required by {cls.__name__} not found in registry",
                code="RESOLVE_DEPENDENCY_NOT_FOUND",
                class_name=cls.__name__,
                param_name=param.name,
                param_type=type_name,
            )

        resolved[param.name] = instance

    return resolved


def x_resolve_dependencies__mutmut_31(  # noqa: C901
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
        import sys

        module = sys.modules.get(cls.__module__)
        localns = vars(module) if module else {}
        hints = get_type_hints(cls.__init__, globalns=None, localns=localns)
    except NameError:
        # Forward reference error - collect what we can from annotations
        hints = {}
        sig = inspect.signature(cls.__init__)
        for param_name, param in sig.parameters.items():
            if param_name == "self":
                continue
            if param.annotation != inspect.Parameter.empty:
                # Use the annotation directly (may be a string)
                hints[param_name] = param.annotation
    except Exception as e:
        raise ValidationError(
            f"Failed to get type hints for {cls.__name__}.__init__: {e}",
            code="RESOLVE_TYPE_HINT_ERROR",
            class_name=cls.__name__,
            cause=e,
        ) from e

    # Get signature
    sig = None
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

        # If param_type is a string (forward reference), try to resolve it
        if isinstance(param_type, str):
            # Look up the type in the class's module
            import sys

            module = sys.modules.get(cls.__module__)
            if module and hasattr(module, param_type):
                param_type = getattr(module, param_type)
            else:
                if allow_missing:
                    missing.append(param.name)
                    continue
                raise ValidationError(
                    f"Forward reference '{param_type}' for parameter '{param.name}' could not be resolved",
                    code="RESOLVE_FORWARD_REF_ERROR",
                    class_name=cls.__name__,
                    param_name=param.name,
                    forward_ref=param_type,
                )

        # Try to resolve from registry by type
        # Strategy: Look for registered instance of this type
        instance = registry.get_by_type(param_type)

        if instance is None:
            if allow_missing:
                missing.append(param.name)
                continue
            type_name = getattr(param_type, "__name__", str(param_type))
            raise NotFoundError(
                f"Dependency '{type_name}' required by {cls.__name__} not found in registry",
                code="RESOLVE_DEPENDENCY_NOT_FOUND",
                class_name=cls.__name__,
                param_name=param.name,
                param_type=type_name,
            )

        resolved[param.name] = instance

    return resolved


def x_resolve_dependencies__mutmut_32(  # noqa: C901
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
        import sys

        module = sys.modules.get(cls.__module__)
        localns = vars(module) if module else {}
        hints = get_type_hints(cls.__init__, globalns=None, localns=localns)
    except NameError:
        # Forward reference error - collect what we can from annotations
        hints = {}
        sig = inspect.signature(cls.__init__)
        for param_name, param in sig.parameters.items():
            if param_name == "self":
                continue
            if param.annotation != inspect.Parameter.empty:
                # Use the annotation directly (may be a string)
                hints[param_name] = param.annotation
    except Exception as e:
        raise ValidationError(
            f"Failed to get type hints for {cls.__name__}.__init__: {e}",
            code="RESOLVE_TYPE_HINT_ERROR",
            class_name=cls.__name__,
            cause=e,
        ) from e

    # Get signature
    sig = inspect.signature(None)
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

        # If param_type is a string (forward reference), try to resolve it
        if isinstance(param_type, str):
            # Look up the type in the class's module
            import sys

            module = sys.modules.get(cls.__module__)
            if module and hasattr(module, param_type):
                param_type = getattr(module, param_type)
            else:
                if allow_missing:
                    missing.append(param.name)
                    continue
                raise ValidationError(
                    f"Forward reference '{param_type}' for parameter '{param.name}' could not be resolved",
                    code="RESOLVE_FORWARD_REF_ERROR",
                    class_name=cls.__name__,
                    param_name=param.name,
                    forward_ref=param_type,
                )

        # Try to resolve from registry by type
        # Strategy: Look for registered instance of this type
        instance = registry.get_by_type(param_type)

        if instance is None:
            if allow_missing:
                missing.append(param.name)
                continue
            type_name = getattr(param_type, "__name__", str(param_type))
            raise NotFoundError(
                f"Dependency '{type_name}' required by {cls.__name__} not found in registry",
                code="RESOLVE_DEPENDENCY_NOT_FOUND",
                class_name=cls.__name__,
                param_name=param.name,
                param_type=type_name,
            )

        resolved[param.name] = instance

    return resolved


def x_resolve_dependencies__mutmut_33(  # noqa: C901
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
        import sys

        module = sys.modules.get(cls.__module__)
        localns = vars(module) if module else {}
        hints = get_type_hints(cls.__init__, globalns=None, localns=localns)
    except NameError:
        # Forward reference error - collect what we can from annotations
        hints = {}
        sig = inspect.signature(cls.__init__)
        for param_name, param in sig.parameters.items():
            if param_name == "self":
                continue
            if param.annotation != inspect.Parameter.empty:
                # Use the annotation directly (may be a string)
                hints[param_name] = param.annotation
    except Exception as e:
        raise ValidationError(
            f"Failed to get type hints for {cls.__name__}.__init__: {e}",
            code="RESOLVE_TYPE_HINT_ERROR",
            class_name=cls.__name__,
            cause=e,
        ) from e

    # Get signature
    sig = inspect.signature(cls.__init__)
    params = None  # Skip 'self'

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

        # If param_type is a string (forward reference), try to resolve it
        if isinstance(param_type, str):
            # Look up the type in the class's module
            import sys

            module = sys.modules.get(cls.__module__)
            if module and hasattr(module, param_type):
                param_type = getattr(module, param_type)
            else:
                if allow_missing:
                    missing.append(param.name)
                    continue
                raise ValidationError(
                    f"Forward reference '{param_type}' for parameter '{param.name}' could not be resolved",
                    code="RESOLVE_FORWARD_REF_ERROR",
                    class_name=cls.__name__,
                    param_name=param.name,
                    forward_ref=param_type,
                )

        # Try to resolve from registry by type
        # Strategy: Look for registered instance of this type
        instance = registry.get_by_type(param_type)

        if instance is None:
            if allow_missing:
                missing.append(param.name)
                continue
            type_name = getattr(param_type, "__name__", str(param_type))
            raise NotFoundError(
                f"Dependency '{type_name}' required by {cls.__name__} not found in registry",
                code="RESOLVE_DEPENDENCY_NOT_FOUND",
                class_name=cls.__name__,
                param_name=param.name,
                param_type=type_name,
            )

        resolved[param.name] = instance

    return resolved


def x_resolve_dependencies__mutmut_34(  # noqa: C901
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
        import sys

        module = sys.modules.get(cls.__module__)
        localns = vars(module) if module else {}
        hints = get_type_hints(cls.__init__, globalns=None, localns=localns)
    except NameError:
        # Forward reference error - collect what we can from annotations
        hints = {}
        sig = inspect.signature(cls.__init__)
        for param_name, param in sig.parameters.items():
            if param_name == "self":
                continue
            if param.annotation != inspect.Parameter.empty:
                # Use the annotation directly (may be a string)
                hints[param_name] = param.annotation
    except Exception as e:
        raise ValidationError(
            f"Failed to get type hints for {cls.__name__}.__init__: {e}",
            code="RESOLVE_TYPE_HINT_ERROR",
            class_name=cls.__name__,
            cause=e,
        ) from e

    # Get signature
    sig = inspect.signature(cls.__init__)
    params = list(None)[1:]  # Skip 'self'

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

        # If param_type is a string (forward reference), try to resolve it
        if isinstance(param_type, str):
            # Look up the type in the class's module
            import sys

            module = sys.modules.get(cls.__module__)
            if module and hasattr(module, param_type):
                param_type = getattr(module, param_type)
            else:
                if allow_missing:
                    missing.append(param.name)
                    continue
                raise ValidationError(
                    f"Forward reference '{param_type}' for parameter '{param.name}' could not be resolved",
                    code="RESOLVE_FORWARD_REF_ERROR",
                    class_name=cls.__name__,
                    param_name=param.name,
                    forward_ref=param_type,
                )

        # Try to resolve from registry by type
        # Strategy: Look for registered instance of this type
        instance = registry.get_by_type(param_type)

        if instance is None:
            if allow_missing:
                missing.append(param.name)
                continue
            type_name = getattr(param_type, "__name__", str(param_type))
            raise NotFoundError(
                f"Dependency '{type_name}' required by {cls.__name__} not found in registry",
                code="RESOLVE_DEPENDENCY_NOT_FOUND",
                class_name=cls.__name__,
                param_name=param.name,
                param_type=type_name,
            )

        resolved[param.name] = instance

    return resolved


def x_resolve_dependencies__mutmut_35(  # noqa: C901
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
        import sys

        module = sys.modules.get(cls.__module__)
        localns = vars(module) if module else {}
        hints = get_type_hints(cls.__init__, globalns=None, localns=localns)
    except NameError:
        # Forward reference error - collect what we can from annotations
        hints = {}
        sig = inspect.signature(cls.__init__)
        for param_name, param in sig.parameters.items():
            if param_name == "self":
                continue
            if param.annotation != inspect.Parameter.empty:
                # Use the annotation directly (may be a string)
                hints[param_name] = param.annotation
    except Exception as e:
        raise ValidationError(
            f"Failed to get type hints for {cls.__name__}.__init__: {e}",
            code="RESOLVE_TYPE_HINT_ERROR",
            class_name=cls.__name__,
            cause=e,
        ) from e

    # Get signature
    sig = inspect.signature(cls.__init__)
    params = list(sig.parameters.values())[2:]  # Skip 'self'

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

        # If param_type is a string (forward reference), try to resolve it
        if isinstance(param_type, str):
            # Look up the type in the class's module
            import sys

            module = sys.modules.get(cls.__module__)
            if module and hasattr(module, param_type):
                param_type = getattr(module, param_type)
            else:
                if allow_missing:
                    missing.append(param.name)
                    continue
                raise ValidationError(
                    f"Forward reference '{param_type}' for parameter '{param.name}' could not be resolved",
                    code="RESOLVE_FORWARD_REF_ERROR",
                    class_name=cls.__name__,
                    param_name=param.name,
                    forward_ref=param_type,
                )

        # Try to resolve from registry by type
        # Strategy: Look for registered instance of this type
        instance = registry.get_by_type(param_type)

        if instance is None:
            if allow_missing:
                missing.append(param.name)
                continue
            type_name = getattr(param_type, "__name__", str(param_type))
            raise NotFoundError(
                f"Dependency '{type_name}' required by {cls.__name__} not found in registry",
                code="RESOLVE_DEPENDENCY_NOT_FOUND",
                class_name=cls.__name__,
                param_name=param.name,
                param_type=type_name,
            )

        resolved[param.name] = instance

    return resolved


def x_resolve_dependencies__mutmut_36(  # noqa: C901
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
        import sys

        module = sys.modules.get(cls.__module__)
        localns = vars(module) if module else {}
        hints = get_type_hints(cls.__init__, globalns=None, localns=localns)
    except NameError:
        # Forward reference error - collect what we can from annotations
        hints = {}
        sig = inspect.signature(cls.__init__)
        for param_name, param in sig.parameters.items():
            if param_name == "self":
                continue
            if param.annotation != inspect.Parameter.empty:
                # Use the annotation directly (may be a string)
                hints[param_name] = param.annotation
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

    resolved = None
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

        # If param_type is a string (forward reference), try to resolve it
        if isinstance(param_type, str):
            # Look up the type in the class's module
            import sys

            module = sys.modules.get(cls.__module__)
            if module and hasattr(module, param_type):
                param_type = getattr(module, param_type)
            else:
                if allow_missing:
                    missing.append(param.name)
                    continue
                raise ValidationError(
                    f"Forward reference '{param_type}' for parameter '{param.name}' could not be resolved",
                    code="RESOLVE_FORWARD_REF_ERROR",
                    class_name=cls.__name__,
                    param_name=param.name,
                    forward_ref=param_type,
                )

        # Try to resolve from registry by type
        # Strategy: Look for registered instance of this type
        instance = registry.get_by_type(param_type)

        if instance is None:
            if allow_missing:
                missing.append(param.name)
                continue
            type_name = getattr(param_type, "__name__", str(param_type))
            raise NotFoundError(
                f"Dependency '{type_name}' required by {cls.__name__} not found in registry",
                code="RESOLVE_DEPENDENCY_NOT_FOUND",
                class_name=cls.__name__,
                param_name=param.name,
                param_type=type_name,
            )

        resolved[param.name] = instance

    return resolved


def x_resolve_dependencies__mutmut_37(  # noqa: C901
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
        import sys

        module = sys.modules.get(cls.__module__)
        localns = vars(module) if module else {}
        hints = get_type_hints(cls.__init__, globalns=None, localns=localns)
    except NameError:
        # Forward reference error - collect what we can from annotations
        hints = {}
        sig = inspect.signature(cls.__init__)
        for param_name, param in sig.parameters.items():
            if param_name == "self":
                continue
            if param.annotation != inspect.Parameter.empty:
                # Use the annotation directly (may be a string)
                hints[param_name] = param.annotation
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
    missing = None

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

        # If param_type is a string (forward reference), try to resolve it
        if isinstance(param_type, str):
            # Look up the type in the class's module
            import sys

            module = sys.modules.get(cls.__module__)
            if module and hasattr(module, param_type):
                param_type = getattr(module, param_type)
            else:
                if allow_missing:
                    missing.append(param.name)
                    continue
                raise ValidationError(
                    f"Forward reference '{param_type}' for parameter '{param.name}' could not be resolved",
                    code="RESOLVE_FORWARD_REF_ERROR",
                    class_name=cls.__name__,
                    param_name=param.name,
                    forward_ref=param_type,
                )

        # Try to resolve from registry by type
        # Strategy: Look for registered instance of this type
        instance = registry.get_by_type(param_type)

        if instance is None:
            if allow_missing:
                missing.append(param.name)
                continue
            type_name = getattr(param_type, "__name__", str(param_type))
            raise NotFoundError(
                f"Dependency '{type_name}' required by {cls.__name__} not found in registry",
                code="RESOLVE_DEPENDENCY_NOT_FOUND",
                class_name=cls.__name__,
                param_name=param.name,
                param_type=type_name,
            )

        resolved[param.name] = instance

    return resolved


def x_resolve_dependencies__mutmut_38(  # noqa: C901
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
        import sys

        module = sys.modules.get(cls.__module__)
        localns = vars(module) if module else {}
        hints = get_type_hints(cls.__init__, globalns=None, localns=localns)
    except NameError:
        # Forward reference error - collect what we can from annotations
        hints = {}
        sig = inspect.signature(cls.__init__)
        for param_name, param in sig.parameters.items():
            if param_name == "self":
                continue
            if param.annotation != inspect.Parameter.empty:
                # Use the annotation directly (may be a string)
                hints[param_name] = param.annotation
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
        if param.kind not in (inspect.Parameter.VAR_POSITIONAL, inspect.Parameter.VAR_KEYWORD):
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

        # If param_type is a string (forward reference), try to resolve it
        if isinstance(param_type, str):
            # Look up the type in the class's module
            import sys

            module = sys.modules.get(cls.__module__)
            if module and hasattr(module, param_type):
                param_type = getattr(module, param_type)
            else:
                if allow_missing:
                    missing.append(param.name)
                    continue
                raise ValidationError(
                    f"Forward reference '{param_type}' for parameter '{param.name}' could not be resolved",
                    code="RESOLVE_FORWARD_REF_ERROR",
                    class_name=cls.__name__,
                    param_name=param.name,
                    forward_ref=param_type,
                )

        # Try to resolve from registry by type
        # Strategy: Look for registered instance of this type
        instance = registry.get_by_type(param_type)

        if instance is None:
            if allow_missing:
                missing.append(param.name)
                continue
            type_name = getattr(param_type, "__name__", str(param_type))
            raise NotFoundError(
                f"Dependency '{type_name}' required by {cls.__name__} not found in registry",
                code="RESOLVE_DEPENDENCY_NOT_FOUND",
                class_name=cls.__name__,
                param_name=param.name,
                param_type=type_name,
            )

        resolved[param.name] = instance

    return resolved


def x_resolve_dependencies__mutmut_39(  # noqa: C901
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
        import sys

        module = sys.modules.get(cls.__module__)
        localns = vars(module) if module else {}
        hints = get_type_hints(cls.__init__, globalns=None, localns=localns)
    except NameError:
        # Forward reference error - collect what we can from annotations
        hints = {}
        sig = inspect.signature(cls.__init__)
        for param_name, param in sig.parameters.items():
            if param_name == "self":
                continue
            if param.annotation != inspect.Parameter.empty:
                # Use the annotation directly (may be a string)
                hints[param_name] = param.annotation
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
            break

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

        # If param_type is a string (forward reference), try to resolve it
        if isinstance(param_type, str):
            # Look up the type in the class's module
            import sys

            module = sys.modules.get(cls.__module__)
            if module and hasattr(module, param_type):
                param_type = getattr(module, param_type)
            else:
                if allow_missing:
                    missing.append(param.name)
                    continue
                raise ValidationError(
                    f"Forward reference '{param_type}' for parameter '{param.name}' could not be resolved",
                    code="RESOLVE_FORWARD_REF_ERROR",
                    class_name=cls.__name__,
                    param_name=param.name,
                    forward_ref=param_type,
                )

        # Try to resolve from registry by type
        # Strategy: Look for registered instance of this type
        instance = registry.get_by_type(param_type)

        if instance is None:
            if allow_missing:
                missing.append(param.name)
                continue
            type_name = getattr(param_type, "__name__", str(param_type))
            raise NotFoundError(
                f"Dependency '{type_name}' required by {cls.__name__} not found in registry",
                code="RESOLVE_DEPENDENCY_NOT_FOUND",
                class_name=cls.__name__,
                param_name=param.name,
                param_type=type_name,
            )

        resolved[param.name] = instance

    return resolved


def x_resolve_dependencies__mutmut_40(  # noqa: C901
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
        import sys

        module = sys.modules.get(cls.__module__)
        localns = vars(module) if module else {}
        hints = get_type_hints(cls.__init__, globalns=None, localns=localns)
    except NameError:
        # Forward reference error - collect what we can from annotations
        hints = {}
        sig = inspect.signature(cls.__init__)
        for param_name, param in sig.parameters.items():
            if param_name == "self":
                continue
            if param.annotation != inspect.Parameter.empty:
                # Use the annotation directly (may be a string)
                hints[param_name] = param.annotation
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
        if param.default == inspect.Parameter.empty:
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

        # If param_type is a string (forward reference), try to resolve it
        if isinstance(param_type, str):
            # Look up the type in the class's module
            import sys

            module = sys.modules.get(cls.__module__)
            if module and hasattr(module, param_type):
                param_type = getattr(module, param_type)
            else:
                if allow_missing:
                    missing.append(param.name)
                    continue
                raise ValidationError(
                    f"Forward reference '{param_type}' for parameter '{param.name}' could not be resolved",
                    code="RESOLVE_FORWARD_REF_ERROR",
                    class_name=cls.__name__,
                    param_name=param.name,
                    forward_ref=param_type,
                )

        # Try to resolve from registry by type
        # Strategy: Look for registered instance of this type
        instance = registry.get_by_type(param_type)

        if instance is None:
            if allow_missing:
                missing.append(param.name)
                continue
            type_name = getattr(param_type, "__name__", str(param_type))
            raise NotFoundError(
                f"Dependency '{type_name}' required by {cls.__name__} not found in registry",
                code="RESOLVE_DEPENDENCY_NOT_FOUND",
                class_name=cls.__name__,
                param_name=param.name,
                param_type=type_name,
            )

        resolved[param.name] = instance

    return resolved


def x_resolve_dependencies__mutmut_41(  # noqa: C901
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
        import sys

        module = sys.modules.get(cls.__module__)
        localns = vars(module) if module else {}
        hints = get_type_hints(cls.__init__, globalns=None, localns=localns)
    except NameError:
        # Forward reference error - collect what we can from annotations
        hints = {}
        sig = inspect.signature(cls.__init__)
        for param_name, param in sig.parameters.items():
            if param_name == "self":
                continue
            if param.annotation != inspect.Parameter.empty:
                # Use the annotation directly (may be a string)
                hints[param_name] = param.annotation
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
            break

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

        # If param_type is a string (forward reference), try to resolve it
        if isinstance(param_type, str):
            # Look up the type in the class's module
            import sys

            module = sys.modules.get(cls.__module__)
            if module and hasattr(module, param_type):
                param_type = getattr(module, param_type)
            else:
                if allow_missing:
                    missing.append(param.name)
                    continue
                raise ValidationError(
                    f"Forward reference '{param_type}' for parameter '{param.name}' could not be resolved",
                    code="RESOLVE_FORWARD_REF_ERROR",
                    class_name=cls.__name__,
                    param_name=param.name,
                    forward_ref=param_type,
                )

        # Try to resolve from registry by type
        # Strategy: Look for registered instance of this type
        instance = registry.get_by_type(param_type)

        if instance is None:
            if allow_missing:
                missing.append(param.name)
                continue
            type_name = getattr(param_type, "__name__", str(param_type))
            raise NotFoundError(
                f"Dependency '{type_name}' required by {cls.__name__} not found in registry",
                code="RESOLVE_DEPENDENCY_NOT_FOUND",
                class_name=cls.__name__,
                param_name=param.name,
                param_type=type_name,
            )

        resolved[param.name] = instance

    return resolved


def x_resolve_dependencies__mutmut_42(  # noqa: C901
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
        import sys

        module = sys.modules.get(cls.__module__)
        localns = vars(module) if module else {}
        hints = get_type_hints(cls.__init__, globalns=None, localns=localns)
    except NameError:
        # Forward reference error - collect what we can from annotations
        hints = {}
        sig = inspect.signature(cls.__init__)
        for param_name, param in sig.parameters.items():
            if param_name == "self":
                continue
            if param.annotation != inspect.Parameter.empty:
                # Use the annotation directly (may be a string)
                hints[param_name] = param.annotation
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
        param_type = None
        if param_type is None:
            if allow_missing:
                continue
            raise ValidationError(
                f"Parameter '{param.name}' of {cls.__name__}.__init__ has no type hint",
                code="RESOLVE_NO_TYPE_HINT",
                class_name=cls.__name__,
                param_name=param.name,
            )

        # If param_type is a string (forward reference), try to resolve it
        if isinstance(param_type, str):
            # Look up the type in the class's module
            import sys

            module = sys.modules.get(cls.__module__)
            if module and hasattr(module, param_type):
                param_type = getattr(module, param_type)
            else:
                if allow_missing:
                    missing.append(param.name)
                    continue
                raise ValidationError(
                    f"Forward reference '{param_type}' for parameter '{param.name}' could not be resolved",
                    code="RESOLVE_FORWARD_REF_ERROR",
                    class_name=cls.__name__,
                    param_name=param.name,
                    forward_ref=param_type,
                )

        # Try to resolve from registry by type
        # Strategy: Look for registered instance of this type
        instance = registry.get_by_type(param_type)

        if instance is None:
            if allow_missing:
                missing.append(param.name)
                continue
            type_name = getattr(param_type, "__name__", str(param_type))
            raise NotFoundError(
                f"Dependency '{type_name}' required by {cls.__name__} not found in registry",
                code="RESOLVE_DEPENDENCY_NOT_FOUND",
                class_name=cls.__name__,
                param_name=param.name,
                param_type=type_name,
            )

        resolved[param.name] = instance

    return resolved


def x_resolve_dependencies__mutmut_43(  # noqa: C901
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
        import sys

        module = sys.modules.get(cls.__module__)
        localns = vars(module) if module else {}
        hints = get_type_hints(cls.__init__, globalns=None, localns=localns)
    except NameError:
        # Forward reference error - collect what we can from annotations
        hints = {}
        sig = inspect.signature(cls.__init__)
        for param_name, param in sig.parameters.items():
            if param_name == "self":
                continue
            if param.annotation != inspect.Parameter.empty:
                # Use the annotation directly (may be a string)
                hints[param_name] = param.annotation
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
        param_type = hints.get(None)
        if param_type is None:
            if allow_missing:
                continue
            raise ValidationError(
                f"Parameter '{param.name}' of {cls.__name__}.__init__ has no type hint",
                code="RESOLVE_NO_TYPE_HINT",
                class_name=cls.__name__,
                param_name=param.name,
            )

        # If param_type is a string (forward reference), try to resolve it
        if isinstance(param_type, str):
            # Look up the type in the class's module
            import sys

            module = sys.modules.get(cls.__module__)
            if module and hasattr(module, param_type):
                param_type = getattr(module, param_type)
            else:
                if allow_missing:
                    missing.append(param.name)
                    continue
                raise ValidationError(
                    f"Forward reference '{param_type}' for parameter '{param.name}' could not be resolved",
                    code="RESOLVE_FORWARD_REF_ERROR",
                    class_name=cls.__name__,
                    param_name=param.name,
                    forward_ref=param_type,
                )

        # Try to resolve from registry by type
        # Strategy: Look for registered instance of this type
        instance = registry.get_by_type(param_type)

        if instance is None:
            if allow_missing:
                missing.append(param.name)
                continue
            type_name = getattr(param_type, "__name__", str(param_type))
            raise NotFoundError(
                f"Dependency '{type_name}' required by {cls.__name__} not found in registry",
                code="RESOLVE_DEPENDENCY_NOT_FOUND",
                class_name=cls.__name__,
                param_name=param.name,
                param_type=type_name,
            )

        resolved[param.name] = instance

    return resolved


def x_resolve_dependencies__mutmut_44(  # noqa: C901
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
        import sys

        module = sys.modules.get(cls.__module__)
        localns = vars(module) if module else {}
        hints = get_type_hints(cls.__init__, globalns=None, localns=localns)
    except NameError:
        # Forward reference error - collect what we can from annotations
        hints = {}
        sig = inspect.signature(cls.__init__)
        for param_name, param in sig.parameters.items():
            if param_name == "self":
                continue
            if param.annotation != inspect.Parameter.empty:
                # Use the annotation directly (may be a string)
                hints[param_name] = param.annotation
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
        if param_type is not None:
            if allow_missing:
                continue
            raise ValidationError(
                f"Parameter '{param.name}' of {cls.__name__}.__init__ has no type hint",
                code="RESOLVE_NO_TYPE_HINT",
                class_name=cls.__name__,
                param_name=param.name,
            )

        # If param_type is a string (forward reference), try to resolve it
        if isinstance(param_type, str):
            # Look up the type in the class's module
            import sys

            module = sys.modules.get(cls.__module__)
            if module and hasattr(module, param_type):
                param_type = getattr(module, param_type)
            else:
                if allow_missing:
                    missing.append(param.name)
                    continue
                raise ValidationError(
                    f"Forward reference '{param_type}' for parameter '{param.name}' could not be resolved",
                    code="RESOLVE_FORWARD_REF_ERROR",
                    class_name=cls.__name__,
                    param_name=param.name,
                    forward_ref=param_type,
                )

        # Try to resolve from registry by type
        # Strategy: Look for registered instance of this type
        instance = registry.get_by_type(param_type)

        if instance is None:
            if allow_missing:
                missing.append(param.name)
                continue
            type_name = getattr(param_type, "__name__", str(param_type))
            raise NotFoundError(
                f"Dependency '{type_name}' required by {cls.__name__} not found in registry",
                code="RESOLVE_DEPENDENCY_NOT_FOUND",
                class_name=cls.__name__,
                param_name=param.name,
                param_type=type_name,
            )

        resolved[param.name] = instance

    return resolved


def x_resolve_dependencies__mutmut_45(  # noqa: C901
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
        import sys

        module = sys.modules.get(cls.__module__)
        localns = vars(module) if module else {}
        hints = get_type_hints(cls.__init__, globalns=None, localns=localns)
    except NameError:
        # Forward reference error - collect what we can from annotations
        hints = {}
        sig = inspect.signature(cls.__init__)
        for param_name, param in sig.parameters.items():
            if param_name == "self":
                continue
            if param.annotation != inspect.Parameter.empty:
                # Use the annotation directly (may be a string)
                hints[param_name] = param.annotation
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
                break
            raise ValidationError(
                f"Parameter '{param.name}' of {cls.__name__}.__init__ has no type hint",
                code="RESOLVE_NO_TYPE_HINT",
                class_name=cls.__name__,
                param_name=param.name,
            )

        # If param_type is a string (forward reference), try to resolve it
        if isinstance(param_type, str):
            # Look up the type in the class's module
            import sys

            module = sys.modules.get(cls.__module__)
            if module and hasattr(module, param_type):
                param_type = getattr(module, param_type)
            else:
                if allow_missing:
                    missing.append(param.name)
                    continue
                raise ValidationError(
                    f"Forward reference '{param_type}' for parameter '{param.name}' could not be resolved",
                    code="RESOLVE_FORWARD_REF_ERROR",
                    class_name=cls.__name__,
                    param_name=param.name,
                    forward_ref=param_type,
                )

        # Try to resolve from registry by type
        # Strategy: Look for registered instance of this type
        instance = registry.get_by_type(param_type)

        if instance is None:
            if allow_missing:
                missing.append(param.name)
                continue
            type_name = getattr(param_type, "__name__", str(param_type))
            raise NotFoundError(
                f"Dependency '{type_name}' required by {cls.__name__} not found in registry",
                code="RESOLVE_DEPENDENCY_NOT_FOUND",
                class_name=cls.__name__,
                param_name=param.name,
                param_type=type_name,
            )

        resolved[param.name] = instance

    return resolved


def x_resolve_dependencies__mutmut_46(  # noqa: C901
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
        import sys

        module = sys.modules.get(cls.__module__)
        localns = vars(module) if module else {}
        hints = get_type_hints(cls.__init__, globalns=None, localns=localns)
    except NameError:
        # Forward reference error - collect what we can from annotations
        hints = {}
        sig = inspect.signature(cls.__init__)
        for param_name, param in sig.parameters.items():
            if param_name == "self":
                continue
            if param.annotation != inspect.Parameter.empty:
                # Use the annotation directly (may be a string)
                hints[param_name] = param.annotation
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
                None,
                code="RESOLVE_NO_TYPE_HINT",
                class_name=cls.__name__,
                param_name=param.name,
            )

        # If param_type is a string (forward reference), try to resolve it
        if isinstance(param_type, str):
            # Look up the type in the class's module
            import sys

            module = sys.modules.get(cls.__module__)
            if module and hasattr(module, param_type):
                param_type = getattr(module, param_type)
            else:
                if allow_missing:
                    missing.append(param.name)
                    continue
                raise ValidationError(
                    f"Forward reference '{param_type}' for parameter '{param.name}' could not be resolved",
                    code="RESOLVE_FORWARD_REF_ERROR",
                    class_name=cls.__name__,
                    param_name=param.name,
                    forward_ref=param_type,
                )

        # Try to resolve from registry by type
        # Strategy: Look for registered instance of this type
        instance = registry.get_by_type(param_type)

        if instance is None:
            if allow_missing:
                missing.append(param.name)
                continue
            type_name = getattr(param_type, "__name__", str(param_type))
            raise NotFoundError(
                f"Dependency '{type_name}' required by {cls.__name__} not found in registry",
                code="RESOLVE_DEPENDENCY_NOT_FOUND",
                class_name=cls.__name__,
                param_name=param.name,
                param_type=type_name,
            )

        resolved[param.name] = instance

    return resolved


def x_resolve_dependencies__mutmut_47(  # noqa: C901
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
        import sys

        module = sys.modules.get(cls.__module__)
        localns = vars(module) if module else {}
        hints = get_type_hints(cls.__init__, globalns=None, localns=localns)
    except NameError:
        # Forward reference error - collect what we can from annotations
        hints = {}
        sig = inspect.signature(cls.__init__)
        for param_name, param in sig.parameters.items():
            if param_name == "self":
                continue
            if param.annotation != inspect.Parameter.empty:
                # Use the annotation directly (may be a string)
                hints[param_name] = param.annotation
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
                code=None,
                class_name=cls.__name__,
                param_name=param.name,
            )

        # If param_type is a string (forward reference), try to resolve it
        if isinstance(param_type, str):
            # Look up the type in the class's module
            import sys

            module = sys.modules.get(cls.__module__)
            if module and hasattr(module, param_type):
                param_type = getattr(module, param_type)
            else:
                if allow_missing:
                    missing.append(param.name)
                    continue
                raise ValidationError(
                    f"Forward reference '{param_type}' for parameter '{param.name}' could not be resolved",
                    code="RESOLVE_FORWARD_REF_ERROR",
                    class_name=cls.__name__,
                    param_name=param.name,
                    forward_ref=param_type,
                )

        # Try to resolve from registry by type
        # Strategy: Look for registered instance of this type
        instance = registry.get_by_type(param_type)

        if instance is None:
            if allow_missing:
                missing.append(param.name)
                continue
            type_name = getattr(param_type, "__name__", str(param_type))
            raise NotFoundError(
                f"Dependency '{type_name}' required by {cls.__name__} not found in registry",
                code="RESOLVE_DEPENDENCY_NOT_FOUND",
                class_name=cls.__name__,
                param_name=param.name,
                param_type=type_name,
            )

        resolved[param.name] = instance

    return resolved


def x_resolve_dependencies__mutmut_48(  # noqa: C901
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
        import sys

        module = sys.modules.get(cls.__module__)
        localns = vars(module) if module else {}
        hints = get_type_hints(cls.__init__, globalns=None, localns=localns)
    except NameError:
        # Forward reference error - collect what we can from annotations
        hints = {}
        sig = inspect.signature(cls.__init__)
        for param_name, param in sig.parameters.items():
            if param_name == "self":
                continue
            if param.annotation != inspect.Parameter.empty:
                # Use the annotation directly (may be a string)
                hints[param_name] = param.annotation
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
                class_name=None,
                param_name=param.name,
            )

        # If param_type is a string (forward reference), try to resolve it
        if isinstance(param_type, str):
            # Look up the type in the class's module
            import sys

            module = sys.modules.get(cls.__module__)
            if module and hasattr(module, param_type):
                param_type = getattr(module, param_type)
            else:
                if allow_missing:
                    missing.append(param.name)
                    continue
                raise ValidationError(
                    f"Forward reference '{param_type}' for parameter '{param.name}' could not be resolved",
                    code="RESOLVE_FORWARD_REF_ERROR",
                    class_name=cls.__name__,
                    param_name=param.name,
                    forward_ref=param_type,
                )

        # Try to resolve from registry by type
        # Strategy: Look for registered instance of this type
        instance = registry.get_by_type(param_type)

        if instance is None:
            if allow_missing:
                missing.append(param.name)
                continue
            type_name = getattr(param_type, "__name__", str(param_type))
            raise NotFoundError(
                f"Dependency '{type_name}' required by {cls.__name__} not found in registry",
                code="RESOLVE_DEPENDENCY_NOT_FOUND",
                class_name=cls.__name__,
                param_name=param.name,
                param_type=type_name,
            )

        resolved[param.name] = instance

    return resolved


def x_resolve_dependencies__mutmut_49(  # noqa: C901
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
        import sys

        module = sys.modules.get(cls.__module__)
        localns = vars(module) if module else {}
        hints = get_type_hints(cls.__init__, globalns=None, localns=localns)
    except NameError:
        # Forward reference error - collect what we can from annotations
        hints = {}
        sig = inspect.signature(cls.__init__)
        for param_name, param in sig.parameters.items():
            if param_name == "self":
                continue
            if param.annotation != inspect.Parameter.empty:
                # Use the annotation directly (may be a string)
                hints[param_name] = param.annotation
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
                param_name=None,
            )

        # If param_type is a string (forward reference), try to resolve it
        if isinstance(param_type, str):
            # Look up the type in the class's module
            import sys

            module = sys.modules.get(cls.__module__)
            if module and hasattr(module, param_type):
                param_type = getattr(module, param_type)
            else:
                if allow_missing:
                    missing.append(param.name)
                    continue
                raise ValidationError(
                    f"Forward reference '{param_type}' for parameter '{param.name}' could not be resolved",
                    code="RESOLVE_FORWARD_REF_ERROR",
                    class_name=cls.__name__,
                    param_name=param.name,
                    forward_ref=param_type,
                )

        # Try to resolve from registry by type
        # Strategy: Look for registered instance of this type
        instance = registry.get_by_type(param_type)

        if instance is None:
            if allow_missing:
                missing.append(param.name)
                continue
            type_name = getattr(param_type, "__name__", str(param_type))
            raise NotFoundError(
                f"Dependency '{type_name}' required by {cls.__name__} not found in registry",
                code="RESOLVE_DEPENDENCY_NOT_FOUND",
                class_name=cls.__name__,
                param_name=param.name,
                param_type=type_name,
            )

        resolved[param.name] = instance

    return resolved


def x_resolve_dependencies__mutmut_50(  # noqa: C901
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
        import sys

        module = sys.modules.get(cls.__module__)
        localns = vars(module) if module else {}
        hints = get_type_hints(cls.__init__, globalns=None, localns=localns)
    except NameError:
        # Forward reference error - collect what we can from annotations
        hints = {}
        sig = inspect.signature(cls.__init__)
        for param_name, param in sig.parameters.items():
            if param_name == "self":
                continue
            if param.annotation != inspect.Parameter.empty:
                # Use the annotation directly (may be a string)
                hints[param_name] = param.annotation
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
                code="RESOLVE_NO_TYPE_HINT",
                class_name=cls.__name__,
                param_name=param.name,
            )

        # If param_type is a string (forward reference), try to resolve it
        if isinstance(param_type, str):
            # Look up the type in the class's module
            import sys

            module = sys.modules.get(cls.__module__)
            if module and hasattr(module, param_type):
                param_type = getattr(module, param_type)
            else:
                if allow_missing:
                    missing.append(param.name)
                    continue
                raise ValidationError(
                    f"Forward reference '{param_type}' for parameter '{param.name}' could not be resolved",
                    code="RESOLVE_FORWARD_REF_ERROR",
                    class_name=cls.__name__,
                    param_name=param.name,
                    forward_ref=param_type,
                )

        # Try to resolve from registry by type
        # Strategy: Look for registered instance of this type
        instance = registry.get_by_type(param_type)

        if instance is None:
            if allow_missing:
                missing.append(param.name)
                continue
            type_name = getattr(param_type, "__name__", str(param_type))
            raise NotFoundError(
                f"Dependency '{type_name}' required by {cls.__name__} not found in registry",
                code="RESOLVE_DEPENDENCY_NOT_FOUND",
                class_name=cls.__name__,
                param_name=param.name,
                param_type=type_name,
            )

        resolved[param.name] = instance

    return resolved


def x_resolve_dependencies__mutmut_51(  # noqa: C901
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
        import sys

        module = sys.modules.get(cls.__module__)
        localns = vars(module) if module else {}
        hints = get_type_hints(cls.__init__, globalns=None, localns=localns)
    except NameError:
        # Forward reference error - collect what we can from annotations
        hints = {}
        sig = inspect.signature(cls.__init__)
        for param_name, param in sig.parameters.items():
            if param_name == "self":
                continue
            if param.annotation != inspect.Parameter.empty:
                # Use the annotation directly (may be a string)
                hints[param_name] = param.annotation
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
                class_name=cls.__name__,
                param_name=param.name,
            )

        # If param_type is a string (forward reference), try to resolve it
        if isinstance(param_type, str):
            # Look up the type in the class's module
            import sys

            module = sys.modules.get(cls.__module__)
            if module and hasattr(module, param_type):
                param_type = getattr(module, param_type)
            else:
                if allow_missing:
                    missing.append(param.name)
                    continue
                raise ValidationError(
                    f"Forward reference '{param_type}' for parameter '{param.name}' could not be resolved",
                    code="RESOLVE_FORWARD_REF_ERROR",
                    class_name=cls.__name__,
                    param_name=param.name,
                    forward_ref=param_type,
                )

        # Try to resolve from registry by type
        # Strategy: Look for registered instance of this type
        instance = registry.get_by_type(param_type)

        if instance is None:
            if allow_missing:
                missing.append(param.name)
                continue
            type_name = getattr(param_type, "__name__", str(param_type))
            raise NotFoundError(
                f"Dependency '{type_name}' required by {cls.__name__} not found in registry",
                code="RESOLVE_DEPENDENCY_NOT_FOUND",
                class_name=cls.__name__,
                param_name=param.name,
                param_type=type_name,
            )

        resolved[param.name] = instance

    return resolved


def x_resolve_dependencies__mutmut_52(  # noqa: C901
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
        import sys

        module = sys.modules.get(cls.__module__)
        localns = vars(module) if module else {}
        hints = get_type_hints(cls.__init__, globalns=None, localns=localns)
    except NameError:
        # Forward reference error - collect what we can from annotations
        hints = {}
        sig = inspect.signature(cls.__init__)
        for param_name, param in sig.parameters.items():
            if param_name == "self":
                continue
            if param.annotation != inspect.Parameter.empty:
                # Use the annotation directly (may be a string)
                hints[param_name] = param.annotation
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
                param_name=param.name,
            )

        # If param_type is a string (forward reference), try to resolve it
        if isinstance(param_type, str):
            # Look up the type in the class's module
            import sys

            module = sys.modules.get(cls.__module__)
            if module and hasattr(module, param_type):
                param_type = getattr(module, param_type)
            else:
                if allow_missing:
                    missing.append(param.name)
                    continue
                raise ValidationError(
                    f"Forward reference '{param_type}' for parameter '{param.name}' could not be resolved",
                    code="RESOLVE_FORWARD_REF_ERROR",
                    class_name=cls.__name__,
                    param_name=param.name,
                    forward_ref=param_type,
                )

        # Try to resolve from registry by type
        # Strategy: Look for registered instance of this type
        instance = registry.get_by_type(param_type)

        if instance is None:
            if allow_missing:
                missing.append(param.name)
                continue
            type_name = getattr(param_type, "__name__", str(param_type))
            raise NotFoundError(
                f"Dependency '{type_name}' required by {cls.__name__} not found in registry",
                code="RESOLVE_DEPENDENCY_NOT_FOUND",
                class_name=cls.__name__,
                param_name=param.name,
                param_type=type_name,
            )

        resolved[param.name] = instance

    return resolved


def x_resolve_dependencies__mutmut_53(  # noqa: C901
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
        import sys

        module = sys.modules.get(cls.__module__)
        localns = vars(module) if module else {}
        hints = get_type_hints(cls.__init__, globalns=None, localns=localns)
    except NameError:
        # Forward reference error - collect what we can from annotations
        hints = {}
        sig = inspect.signature(cls.__init__)
        for param_name, param in sig.parameters.items():
            if param_name == "self":
                continue
            if param.annotation != inspect.Parameter.empty:
                # Use the annotation directly (may be a string)
                hints[param_name] = param.annotation
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
                )

        # If param_type is a string (forward reference), try to resolve it
        if isinstance(param_type, str):
            # Look up the type in the class's module
            import sys

            module = sys.modules.get(cls.__module__)
            if module and hasattr(module, param_type):
                param_type = getattr(module, param_type)
            else:
                if allow_missing:
                    missing.append(param.name)
                    continue
                raise ValidationError(
                    f"Forward reference '{param_type}' for parameter '{param.name}' could not be resolved",
                    code="RESOLVE_FORWARD_REF_ERROR",
                    class_name=cls.__name__,
                    param_name=param.name,
                    forward_ref=param_type,
                )

        # Try to resolve from registry by type
        # Strategy: Look for registered instance of this type
        instance = registry.get_by_type(param_type)

        if instance is None:
            if allow_missing:
                missing.append(param.name)
                continue
            type_name = getattr(param_type, "__name__", str(param_type))
            raise NotFoundError(
                f"Dependency '{type_name}' required by {cls.__name__} not found in registry",
                code="RESOLVE_DEPENDENCY_NOT_FOUND",
                class_name=cls.__name__,
                param_name=param.name,
                param_type=type_name,
            )

        resolved[param.name] = instance

    return resolved


def x_resolve_dependencies__mutmut_54(  # noqa: C901
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
        import sys

        module = sys.modules.get(cls.__module__)
        localns = vars(module) if module else {}
        hints = get_type_hints(cls.__init__, globalns=None, localns=localns)
    except NameError:
        # Forward reference error - collect what we can from annotations
        hints = {}
        sig = inspect.signature(cls.__init__)
        for param_name, param in sig.parameters.items():
            if param_name == "self":
                continue
            if param.annotation != inspect.Parameter.empty:
                # Use the annotation directly (may be a string)
                hints[param_name] = param.annotation
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
                code="XXRESOLVE_NO_TYPE_HINTXX",
                class_name=cls.__name__,
                param_name=param.name,
            )

        # If param_type is a string (forward reference), try to resolve it
        if isinstance(param_type, str):
            # Look up the type in the class's module
            import sys

            module = sys.modules.get(cls.__module__)
            if module and hasattr(module, param_type):
                param_type = getattr(module, param_type)
            else:
                if allow_missing:
                    missing.append(param.name)
                    continue
                raise ValidationError(
                    f"Forward reference '{param_type}' for parameter '{param.name}' could not be resolved",
                    code="RESOLVE_FORWARD_REF_ERROR",
                    class_name=cls.__name__,
                    param_name=param.name,
                    forward_ref=param_type,
                )

        # Try to resolve from registry by type
        # Strategy: Look for registered instance of this type
        instance = registry.get_by_type(param_type)

        if instance is None:
            if allow_missing:
                missing.append(param.name)
                continue
            type_name = getattr(param_type, "__name__", str(param_type))
            raise NotFoundError(
                f"Dependency '{type_name}' required by {cls.__name__} not found in registry",
                code="RESOLVE_DEPENDENCY_NOT_FOUND",
                class_name=cls.__name__,
                param_name=param.name,
                param_type=type_name,
            )

        resolved[param.name] = instance

    return resolved


def x_resolve_dependencies__mutmut_55(  # noqa: C901
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
        import sys

        module = sys.modules.get(cls.__module__)
        localns = vars(module) if module else {}
        hints = get_type_hints(cls.__init__, globalns=None, localns=localns)
    except NameError:
        # Forward reference error - collect what we can from annotations
        hints = {}
        sig = inspect.signature(cls.__init__)
        for param_name, param in sig.parameters.items():
            if param_name == "self":
                continue
            if param.annotation != inspect.Parameter.empty:
                # Use the annotation directly (may be a string)
                hints[param_name] = param.annotation
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
                code="resolve_no_type_hint",
                class_name=cls.__name__,
                param_name=param.name,
            )

        # If param_type is a string (forward reference), try to resolve it
        if isinstance(param_type, str):
            # Look up the type in the class's module
            import sys

            module = sys.modules.get(cls.__module__)
            if module and hasattr(module, param_type):
                param_type = getattr(module, param_type)
            else:
                if allow_missing:
                    missing.append(param.name)
                    continue
                raise ValidationError(
                    f"Forward reference '{param_type}' for parameter '{param.name}' could not be resolved",
                    code="RESOLVE_FORWARD_REF_ERROR",
                    class_name=cls.__name__,
                    param_name=param.name,
                    forward_ref=param_type,
                )

        # Try to resolve from registry by type
        # Strategy: Look for registered instance of this type
        instance = registry.get_by_type(param_type)

        if instance is None:
            if allow_missing:
                missing.append(param.name)
                continue
            type_name = getattr(param_type, "__name__", str(param_type))
            raise NotFoundError(
                f"Dependency '{type_name}' required by {cls.__name__} not found in registry",
                code="RESOLVE_DEPENDENCY_NOT_FOUND",
                class_name=cls.__name__,
                param_name=param.name,
                param_type=type_name,
            )

        resolved[param.name] = instance

    return resolved


def x_resolve_dependencies__mutmut_56(  # noqa: C901
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
        import sys

        module = sys.modules.get(cls.__module__)
        localns = vars(module) if module else {}
        hints = get_type_hints(cls.__init__, globalns=None, localns=localns)
    except NameError:
        # Forward reference error - collect what we can from annotations
        hints = {}
        sig = inspect.signature(cls.__init__)
        for param_name, param in sig.parameters.items():
            if param_name == "self":
                continue
            if param.annotation != inspect.Parameter.empty:
                # Use the annotation directly (may be a string)
                hints[param_name] = param.annotation
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

        # If param_type is a string (forward reference), try to resolve it
        if isinstance(param_type, str):
            # Look up the type in the class's module
            import sys

            module = None
            if module and hasattr(module, param_type):
                param_type = getattr(module, param_type)
            else:
                if allow_missing:
                    missing.append(param.name)
                    continue
                raise ValidationError(
                    f"Forward reference '{param_type}' for parameter '{param.name}' could not be resolved",
                    code="RESOLVE_FORWARD_REF_ERROR",
                    class_name=cls.__name__,
                    param_name=param.name,
                    forward_ref=param_type,
                )

        # Try to resolve from registry by type
        # Strategy: Look for registered instance of this type
        instance = registry.get_by_type(param_type)

        if instance is None:
            if allow_missing:
                missing.append(param.name)
                continue
            type_name = getattr(param_type, "__name__", str(param_type))
            raise NotFoundError(
                f"Dependency '{type_name}' required by {cls.__name__} not found in registry",
                code="RESOLVE_DEPENDENCY_NOT_FOUND",
                class_name=cls.__name__,
                param_name=param.name,
                param_type=type_name,
            )

        resolved[param.name] = instance

    return resolved


def x_resolve_dependencies__mutmut_57(  # noqa: C901
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
        import sys

        module = sys.modules.get(cls.__module__)
        localns = vars(module) if module else {}
        hints = get_type_hints(cls.__init__, globalns=None, localns=localns)
    except NameError:
        # Forward reference error - collect what we can from annotations
        hints = {}
        sig = inspect.signature(cls.__init__)
        for param_name, param in sig.parameters.items():
            if param_name == "self":
                continue
            if param.annotation != inspect.Parameter.empty:
                # Use the annotation directly (may be a string)
                hints[param_name] = param.annotation
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

        # If param_type is a string (forward reference), try to resolve it
        if isinstance(param_type, str):
            # Look up the type in the class's module
            import sys

            module = sys.modules.get(None)
            if module and hasattr(module, param_type):
                param_type = getattr(module, param_type)
            else:
                if allow_missing:
                    missing.append(param.name)
                    continue
                raise ValidationError(
                    f"Forward reference '{param_type}' for parameter '{param.name}' could not be resolved",
                    code="RESOLVE_FORWARD_REF_ERROR",
                    class_name=cls.__name__,
                    param_name=param.name,
                    forward_ref=param_type,
                )

        # Try to resolve from registry by type
        # Strategy: Look for registered instance of this type
        instance = registry.get_by_type(param_type)

        if instance is None:
            if allow_missing:
                missing.append(param.name)
                continue
            type_name = getattr(param_type, "__name__", str(param_type))
            raise NotFoundError(
                f"Dependency '{type_name}' required by {cls.__name__} not found in registry",
                code="RESOLVE_DEPENDENCY_NOT_FOUND",
                class_name=cls.__name__,
                param_name=param.name,
                param_type=type_name,
            )

        resolved[param.name] = instance

    return resolved


def x_resolve_dependencies__mutmut_58(  # noqa: C901
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
        import sys

        module = sys.modules.get(cls.__module__)
        localns = vars(module) if module else {}
        hints = get_type_hints(cls.__init__, globalns=None, localns=localns)
    except NameError:
        # Forward reference error - collect what we can from annotations
        hints = {}
        sig = inspect.signature(cls.__init__)
        for param_name, param in sig.parameters.items():
            if param_name == "self":
                continue
            if param.annotation != inspect.Parameter.empty:
                # Use the annotation directly (may be a string)
                hints[param_name] = param.annotation
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

        # If param_type is a string (forward reference), try to resolve it
        if isinstance(param_type, str):
            # Look up the type in the class's module
            import sys

            module = sys.modules.get(cls.__module__)
            if module or hasattr(module, param_type):
                param_type = getattr(module, param_type)
            else:
                if allow_missing:
                    missing.append(param.name)
                    continue
                raise ValidationError(
                    f"Forward reference '{param_type}' for parameter '{param.name}' could not be resolved",
                    code="RESOLVE_FORWARD_REF_ERROR",
                    class_name=cls.__name__,
                    param_name=param.name,
                    forward_ref=param_type,
                )

        # Try to resolve from registry by type
        # Strategy: Look for registered instance of this type
        instance = registry.get_by_type(param_type)

        if instance is None:
            if allow_missing:
                missing.append(param.name)
                continue
            type_name = getattr(param_type, "__name__", str(param_type))
            raise NotFoundError(
                f"Dependency '{type_name}' required by {cls.__name__} not found in registry",
                code="RESOLVE_DEPENDENCY_NOT_FOUND",
                class_name=cls.__name__,
                param_name=param.name,
                param_type=type_name,
            )

        resolved[param.name] = instance

    return resolved


def x_resolve_dependencies__mutmut_59(  # noqa: C901
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
        import sys

        module = sys.modules.get(cls.__module__)
        localns = vars(module) if module else {}
        hints = get_type_hints(cls.__init__, globalns=None, localns=localns)
    except NameError:
        # Forward reference error - collect what we can from annotations
        hints = {}
        sig = inspect.signature(cls.__init__)
        for param_name, param in sig.parameters.items():
            if param_name == "self":
                continue
            if param.annotation != inspect.Parameter.empty:
                # Use the annotation directly (may be a string)
                hints[param_name] = param.annotation
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

        # If param_type is a string (forward reference), try to resolve it
        if isinstance(param_type, str):
            # Look up the type in the class's module
            import sys

            module = sys.modules.get(cls.__module__)
            if module and hasattr(None, param_type):
                param_type = getattr(module, param_type)
            else:
                if allow_missing:
                    missing.append(param.name)
                    continue
                raise ValidationError(
                    f"Forward reference '{param_type}' for parameter '{param.name}' could not be resolved",
                    code="RESOLVE_FORWARD_REF_ERROR",
                    class_name=cls.__name__,
                    param_name=param.name,
                    forward_ref=param_type,
                )

        # Try to resolve from registry by type
        # Strategy: Look for registered instance of this type
        instance = registry.get_by_type(param_type)

        if instance is None:
            if allow_missing:
                missing.append(param.name)
                continue
            type_name = getattr(param_type, "__name__", str(param_type))
            raise NotFoundError(
                f"Dependency '{type_name}' required by {cls.__name__} not found in registry",
                code="RESOLVE_DEPENDENCY_NOT_FOUND",
                class_name=cls.__name__,
                param_name=param.name,
                param_type=type_name,
            )

        resolved[param.name] = instance

    return resolved


def x_resolve_dependencies__mutmut_60(  # noqa: C901
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
        import sys

        module = sys.modules.get(cls.__module__)
        localns = vars(module) if module else {}
        hints = get_type_hints(cls.__init__, globalns=None, localns=localns)
    except NameError:
        # Forward reference error - collect what we can from annotations
        hints = {}
        sig = inspect.signature(cls.__init__)
        for param_name, param in sig.parameters.items():
            if param_name == "self":
                continue
            if param.annotation != inspect.Parameter.empty:
                # Use the annotation directly (may be a string)
                hints[param_name] = param.annotation
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

        # If param_type is a string (forward reference), try to resolve it
        if isinstance(param_type, str):
            # Look up the type in the class's module
            import sys

            module = sys.modules.get(cls.__module__)
            if module and hasattr(module, None):
                param_type = getattr(module, param_type)
            else:
                if allow_missing:
                    missing.append(param.name)
                    continue
                raise ValidationError(
                    f"Forward reference '{param_type}' for parameter '{param.name}' could not be resolved",
                    code="RESOLVE_FORWARD_REF_ERROR",
                    class_name=cls.__name__,
                    param_name=param.name,
                    forward_ref=param_type,
                )

        # Try to resolve from registry by type
        # Strategy: Look for registered instance of this type
        instance = registry.get_by_type(param_type)

        if instance is None:
            if allow_missing:
                missing.append(param.name)
                continue
            type_name = getattr(param_type, "__name__", str(param_type))
            raise NotFoundError(
                f"Dependency '{type_name}' required by {cls.__name__} not found in registry",
                code="RESOLVE_DEPENDENCY_NOT_FOUND",
                class_name=cls.__name__,
                param_name=param.name,
                param_type=type_name,
            )

        resolved[param.name] = instance

    return resolved


def x_resolve_dependencies__mutmut_61(  # noqa: C901
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
        import sys

        module = sys.modules.get(cls.__module__)
        localns = vars(module) if module else {}
        hints = get_type_hints(cls.__init__, globalns=None, localns=localns)
    except NameError:
        # Forward reference error - collect what we can from annotations
        hints = {}
        sig = inspect.signature(cls.__init__)
        for param_name, param in sig.parameters.items():
            if param_name == "self":
                continue
            if param.annotation != inspect.Parameter.empty:
                # Use the annotation directly (may be a string)
                hints[param_name] = param.annotation
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

        # If param_type is a string (forward reference), try to resolve it
        if isinstance(param_type, str):
            # Look up the type in the class's module
            import sys

            module = sys.modules.get(cls.__module__)
            if module and hasattr(param_type):
                param_type = getattr(module, param_type)
            else:
                if allow_missing:
                    missing.append(param.name)
                    continue
                raise ValidationError(
                    f"Forward reference '{param_type}' for parameter '{param.name}' could not be resolved",
                    code="RESOLVE_FORWARD_REF_ERROR",
                    class_name=cls.__name__,
                    param_name=param.name,
                    forward_ref=param_type,
                )

        # Try to resolve from registry by type
        # Strategy: Look for registered instance of this type
        instance = registry.get_by_type(param_type)

        if instance is None:
            if allow_missing:
                missing.append(param.name)
                continue
            type_name = getattr(param_type, "__name__", str(param_type))
            raise NotFoundError(
                f"Dependency '{type_name}' required by {cls.__name__} not found in registry",
                code="RESOLVE_DEPENDENCY_NOT_FOUND",
                class_name=cls.__name__,
                param_name=param.name,
                param_type=type_name,
            )

        resolved[param.name] = instance

    return resolved


def x_resolve_dependencies__mutmut_62(  # noqa: C901
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
        import sys

        module = sys.modules.get(cls.__module__)
        localns = vars(module) if module else {}
        hints = get_type_hints(cls.__init__, globalns=None, localns=localns)
    except NameError:
        # Forward reference error - collect what we can from annotations
        hints = {}
        sig = inspect.signature(cls.__init__)
        for param_name, param in sig.parameters.items():
            if param_name == "self":
                continue
            if param.annotation != inspect.Parameter.empty:
                # Use the annotation directly (may be a string)
                hints[param_name] = param.annotation
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

        # If param_type is a string (forward reference), try to resolve it
        if isinstance(param_type, str):
            # Look up the type in the class's module
            import sys

            module = sys.modules.get(cls.__module__)
            if module and hasattr(module, ):
                param_type = getattr(module, param_type)
            else:
                if allow_missing:
                    missing.append(param.name)
                    continue
                raise ValidationError(
                    f"Forward reference '{param_type}' for parameter '{param.name}' could not be resolved",
                    code="RESOLVE_FORWARD_REF_ERROR",
                    class_name=cls.__name__,
                    param_name=param.name,
                    forward_ref=param_type,
                )

        # Try to resolve from registry by type
        # Strategy: Look for registered instance of this type
        instance = registry.get_by_type(param_type)

        if instance is None:
            if allow_missing:
                missing.append(param.name)
                continue
            type_name = getattr(param_type, "__name__", str(param_type))
            raise NotFoundError(
                f"Dependency '{type_name}' required by {cls.__name__} not found in registry",
                code="RESOLVE_DEPENDENCY_NOT_FOUND",
                class_name=cls.__name__,
                param_name=param.name,
                param_type=type_name,
            )

        resolved[param.name] = instance

    return resolved


def x_resolve_dependencies__mutmut_63(  # noqa: C901
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
        import sys

        module = sys.modules.get(cls.__module__)
        localns = vars(module) if module else {}
        hints = get_type_hints(cls.__init__, globalns=None, localns=localns)
    except NameError:
        # Forward reference error - collect what we can from annotations
        hints = {}
        sig = inspect.signature(cls.__init__)
        for param_name, param in sig.parameters.items():
            if param_name == "self":
                continue
            if param.annotation != inspect.Parameter.empty:
                # Use the annotation directly (may be a string)
                hints[param_name] = param.annotation
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

        # If param_type is a string (forward reference), try to resolve it
        if isinstance(param_type, str):
            # Look up the type in the class's module
            import sys

            module = sys.modules.get(cls.__module__)
            if module and hasattr(module, param_type):
                param_type = None
            else:
                if allow_missing:
                    missing.append(param.name)
                    continue
                raise ValidationError(
                    f"Forward reference '{param_type}' for parameter '{param.name}' could not be resolved",
                    code="RESOLVE_FORWARD_REF_ERROR",
                    class_name=cls.__name__,
                    param_name=param.name,
                    forward_ref=param_type,
                )

        # Try to resolve from registry by type
        # Strategy: Look for registered instance of this type
        instance = registry.get_by_type(param_type)

        if instance is None:
            if allow_missing:
                missing.append(param.name)
                continue
            type_name = getattr(param_type, "__name__", str(param_type))
            raise NotFoundError(
                f"Dependency '{type_name}' required by {cls.__name__} not found in registry",
                code="RESOLVE_DEPENDENCY_NOT_FOUND",
                class_name=cls.__name__,
                param_name=param.name,
                param_type=type_name,
            )

        resolved[param.name] = instance

    return resolved


def x_resolve_dependencies__mutmut_64(  # noqa: C901
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
        import sys

        module = sys.modules.get(cls.__module__)
        localns = vars(module) if module else {}
        hints = get_type_hints(cls.__init__, globalns=None, localns=localns)
    except NameError:
        # Forward reference error - collect what we can from annotations
        hints = {}
        sig = inspect.signature(cls.__init__)
        for param_name, param in sig.parameters.items():
            if param_name == "self":
                continue
            if param.annotation != inspect.Parameter.empty:
                # Use the annotation directly (may be a string)
                hints[param_name] = param.annotation
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

        # If param_type is a string (forward reference), try to resolve it
        if isinstance(param_type, str):
            # Look up the type in the class's module
            import sys

            module = sys.modules.get(cls.__module__)
            if module and hasattr(module, param_type):
                param_type = getattr(None, param_type)
            else:
                if allow_missing:
                    missing.append(param.name)
                    continue
                raise ValidationError(
                    f"Forward reference '{param_type}' for parameter '{param.name}' could not be resolved",
                    code="RESOLVE_FORWARD_REF_ERROR",
                    class_name=cls.__name__,
                    param_name=param.name,
                    forward_ref=param_type,
                )

        # Try to resolve from registry by type
        # Strategy: Look for registered instance of this type
        instance = registry.get_by_type(param_type)

        if instance is None:
            if allow_missing:
                missing.append(param.name)
                continue
            type_name = getattr(param_type, "__name__", str(param_type))
            raise NotFoundError(
                f"Dependency '{type_name}' required by {cls.__name__} not found in registry",
                code="RESOLVE_DEPENDENCY_NOT_FOUND",
                class_name=cls.__name__,
                param_name=param.name,
                param_type=type_name,
            )

        resolved[param.name] = instance

    return resolved


def x_resolve_dependencies__mutmut_65(  # noqa: C901
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
        import sys

        module = sys.modules.get(cls.__module__)
        localns = vars(module) if module else {}
        hints = get_type_hints(cls.__init__, globalns=None, localns=localns)
    except NameError:
        # Forward reference error - collect what we can from annotations
        hints = {}
        sig = inspect.signature(cls.__init__)
        for param_name, param in sig.parameters.items():
            if param_name == "self":
                continue
            if param.annotation != inspect.Parameter.empty:
                # Use the annotation directly (may be a string)
                hints[param_name] = param.annotation
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

        # If param_type is a string (forward reference), try to resolve it
        if isinstance(param_type, str):
            # Look up the type in the class's module
            import sys

            module = sys.modules.get(cls.__module__)
            if module and hasattr(module, param_type):
                param_type = getattr(module, None)
            else:
                if allow_missing:
                    missing.append(param.name)
                    continue
                raise ValidationError(
                    f"Forward reference '{param_type}' for parameter '{param.name}' could not be resolved",
                    code="RESOLVE_FORWARD_REF_ERROR",
                    class_name=cls.__name__,
                    param_name=param.name,
                    forward_ref=param_type,
                )

        # Try to resolve from registry by type
        # Strategy: Look for registered instance of this type
        instance = registry.get_by_type(param_type)

        if instance is None:
            if allow_missing:
                missing.append(param.name)
                continue
            type_name = getattr(param_type, "__name__", str(param_type))
            raise NotFoundError(
                f"Dependency '{type_name}' required by {cls.__name__} not found in registry",
                code="RESOLVE_DEPENDENCY_NOT_FOUND",
                class_name=cls.__name__,
                param_name=param.name,
                param_type=type_name,
            )

        resolved[param.name] = instance

    return resolved


def x_resolve_dependencies__mutmut_66(  # noqa: C901
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
        import sys

        module = sys.modules.get(cls.__module__)
        localns = vars(module) if module else {}
        hints = get_type_hints(cls.__init__, globalns=None, localns=localns)
    except NameError:
        # Forward reference error - collect what we can from annotations
        hints = {}
        sig = inspect.signature(cls.__init__)
        for param_name, param in sig.parameters.items():
            if param_name == "self":
                continue
            if param.annotation != inspect.Parameter.empty:
                # Use the annotation directly (may be a string)
                hints[param_name] = param.annotation
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

        # If param_type is a string (forward reference), try to resolve it
        if isinstance(param_type, str):
            # Look up the type in the class's module
            import sys

            module = sys.modules.get(cls.__module__)
            if module and hasattr(module, param_type):
                param_type = getattr(param_type)
            else:
                if allow_missing:
                    missing.append(param.name)
                    continue
                raise ValidationError(
                    f"Forward reference '{param_type}' for parameter '{param.name}' could not be resolved",
                    code="RESOLVE_FORWARD_REF_ERROR",
                    class_name=cls.__name__,
                    param_name=param.name,
                    forward_ref=param_type,
                )

        # Try to resolve from registry by type
        # Strategy: Look for registered instance of this type
        instance = registry.get_by_type(param_type)

        if instance is None:
            if allow_missing:
                missing.append(param.name)
                continue
            type_name = getattr(param_type, "__name__", str(param_type))
            raise NotFoundError(
                f"Dependency '{type_name}' required by {cls.__name__} not found in registry",
                code="RESOLVE_DEPENDENCY_NOT_FOUND",
                class_name=cls.__name__,
                param_name=param.name,
                param_type=type_name,
            )

        resolved[param.name] = instance

    return resolved


def x_resolve_dependencies__mutmut_67(  # noqa: C901
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
        import sys

        module = sys.modules.get(cls.__module__)
        localns = vars(module) if module else {}
        hints = get_type_hints(cls.__init__, globalns=None, localns=localns)
    except NameError:
        # Forward reference error - collect what we can from annotations
        hints = {}
        sig = inspect.signature(cls.__init__)
        for param_name, param in sig.parameters.items():
            if param_name == "self":
                continue
            if param.annotation != inspect.Parameter.empty:
                # Use the annotation directly (may be a string)
                hints[param_name] = param.annotation
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

        # If param_type is a string (forward reference), try to resolve it
        if isinstance(param_type, str):
            # Look up the type in the class's module
            import sys

            module = sys.modules.get(cls.__module__)
            if module and hasattr(module, param_type):
                param_type = getattr(module, )
            else:
                if allow_missing:
                    missing.append(param.name)
                    continue
                raise ValidationError(
                    f"Forward reference '{param_type}' for parameter '{param.name}' could not be resolved",
                    code="RESOLVE_FORWARD_REF_ERROR",
                    class_name=cls.__name__,
                    param_name=param.name,
                    forward_ref=param_type,
                )

        # Try to resolve from registry by type
        # Strategy: Look for registered instance of this type
        instance = registry.get_by_type(param_type)

        if instance is None:
            if allow_missing:
                missing.append(param.name)
                continue
            type_name = getattr(param_type, "__name__", str(param_type))
            raise NotFoundError(
                f"Dependency '{type_name}' required by {cls.__name__} not found in registry",
                code="RESOLVE_DEPENDENCY_NOT_FOUND",
                class_name=cls.__name__,
                param_name=param.name,
                param_type=type_name,
            )

        resolved[param.name] = instance

    return resolved


def x_resolve_dependencies__mutmut_68(  # noqa: C901
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
        import sys

        module = sys.modules.get(cls.__module__)
        localns = vars(module) if module else {}
        hints = get_type_hints(cls.__init__, globalns=None, localns=localns)
    except NameError:
        # Forward reference error - collect what we can from annotations
        hints = {}
        sig = inspect.signature(cls.__init__)
        for param_name, param in sig.parameters.items():
            if param_name == "self":
                continue
            if param.annotation != inspect.Parameter.empty:
                # Use the annotation directly (may be a string)
                hints[param_name] = param.annotation
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

        # If param_type is a string (forward reference), try to resolve it
        if isinstance(param_type, str):
            # Look up the type in the class's module
            import sys

            module = sys.modules.get(cls.__module__)
            if module and hasattr(module, param_type):
                param_type = getattr(module, param_type)
            else:
                if allow_missing:
                    missing.append(None)
                    continue
                raise ValidationError(
                    f"Forward reference '{param_type}' for parameter '{param.name}' could not be resolved",
                    code="RESOLVE_FORWARD_REF_ERROR",
                    class_name=cls.__name__,
                    param_name=param.name,
                    forward_ref=param_type,
                )

        # Try to resolve from registry by type
        # Strategy: Look for registered instance of this type
        instance = registry.get_by_type(param_type)

        if instance is None:
            if allow_missing:
                missing.append(param.name)
                continue
            type_name = getattr(param_type, "__name__", str(param_type))
            raise NotFoundError(
                f"Dependency '{type_name}' required by {cls.__name__} not found in registry",
                code="RESOLVE_DEPENDENCY_NOT_FOUND",
                class_name=cls.__name__,
                param_name=param.name,
                param_type=type_name,
            )

        resolved[param.name] = instance

    return resolved


def x_resolve_dependencies__mutmut_69(  # noqa: C901
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
        import sys

        module = sys.modules.get(cls.__module__)
        localns = vars(module) if module else {}
        hints = get_type_hints(cls.__init__, globalns=None, localns=localns)
    except NameError:
        # Forward reference error - collect what we can from annotations
        hints = {}
        sig = inspect.signature(cls.__init__)
        for param_name, param in sig.parameters.items():
            if param_name == "self":
                continue
            if param.annotation != inspect.Parameter.empty:
                # Use the annotation directly (may be a string)
                hints[param_name] = param.annotation
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

        # If param_type is a string (forward reference), try to resolve it
        if isinstance(param_type, str):
            # Look up the type in the class's module
            import sys

            module = sys.modules.get(cls.__module__)
            if module and hasattr(module, param_type):
                param_type = getattr(module, param_type)
            else:
                if allow_missing:
                    missing.append(param.name)
                    break
                raise ValidationError(
                    f"Forward reference '{param_type}' for parameter '{param.name}' could not be resolved",
                    code="RESOLVE_FORWARD_REF_ERROR",
                    class_name=cls.__name__,
                    param_name=param.name,
                    forward_ref=param_type,
                )

        # Try to resolve from registry by type
        # Strategy: Look for registered instance of this type
        instance = registry.get_by_type(param_type)

        if instance is None:
            if allow_missing:
                missing.append(param.name)
                continue
            type_name = getattr(param_type, "__name__", str(param_type))
            raise NotFoundError(
                f"Dependency '{type_name}' required by {cls.__name__} not found in registry",
                code="RESOLVE_DEPENDENCY_NOT_FOUND",
                class_name=cls.__name__,
                param_name=param.name,
                param_type=type_name,
            )

        resolved[param.name] = instance

    return resolved


def x_resolve_dependencies__mutmut_70(  # noqa: C901
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
        import sys

        module = sys.modules.get(cls.__module__)
        localns = vars(module) if module else {}
        hints = get_type_hints(cls.__init__, globalns=None, localns=localns)
    except NameError:
        # Forward reference error - collect what we can from annotations
        hints = {}
        sig = inspect.signature(cls.__init__)
        for param_name, param in sig.parameters.items():
            if param_name == "self":
                continue
            if param.annotation != inspect.Parameter.empty:
                # Use the annotation directly (may be a string)
                hints[param_name] = param.annotation
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

        # If param_type is a string (forward reference), try to resolve it
        if isinstance(param_type, str):
            # Look up the type in the class's module
            import sys

            module = sys.modules.get(cls.__module__)
            if module and hasattr(module, param_type):
                param_type = getattr(module, param_type)
            else:
                if allow_missing:
                    missing.append(param.name)
                    continue
                raise ValidationError(
                    None,
                    code="RESOLVE_FORWARD_REF_ERROR",
                    class_name=cls.__name__,
                    param_name=param.name,
                    forward_ref=param_type,
                )

        # Try to resolve from registry by type
        # Strategy: Look for registered instance of this type
        instance = registry.get_by_type(param_type)

        if instance is None:
            if allow_missing:
                missing.append(param.name)
                continue
            type_name = getattr(param_type, "__name__", str(param_type))
            raise NotFoundError(
                f"Dependency '{type_name}' required by {cls.__name__} not found in registry",
                code="RESOLVE_DEPENDENCY_NOT_FOUND",
                class_name=cls.__name__,
                param_name=param.name,
                param_type=type_name,
            )

        resolved[param.name] = instance

    return resolved


def x_resolve_dependencies__mutmut_71(  # noqa: C901
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
        import sys

        module = sys.modules.get(cls.__module__)
        localns = vars(module) if module else {}
        hints = get_type_hints(cls.__init__, globalns=None, localns=localns)
    except NameError:
        # Forward reference error - collect what we can from annotations
        hints = {}
        sig = inspect.signature(cls.__init__)
        for param_name, param in sig.parameters.items():
            if param_name == "self":
                continue
            if param.annotation != inspect.Parameter.empty:
                # Use the annotation directly (may be a string)
                hints[param_name] = param.annotation
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

        # If param_type is a string (forward reference), try to resolve it
        if isinstance(param_type, str):
            # Look up the type in the class's module
            import sys

            module = sys.modules.get(cls.__module__)
            if module and hasattr(module, param_type):
                param_type = getattr(module, param_type)
            else:
                if allow_missing:
                    missing.append(param.name)
                    continue
                raise ValidationError(
                    f"Forward reference '{param_type}' for parameter '{param.name}' could not be resolved",
                    code=None,
                    class_name=cls.__name__,
                    param_name=param.name,
                    forward_ref=param_type,
                )

        # Try to resolve from registry by type
        # Strategy: Look for registered instance of this type
        instance = registry.get_by_type(param_type)

        if instance is None:
            if allow_missing:
                missing.append(param.name)
                continue
            type_name = getattr(param_type, "__name__", str(param_type))
            raise NotFoundError(
                f"Dependency '{type_name}' required by {cls.__name__} not found in registry",
                code="RESOLVE_DEPENDENCY_NOT_FOUND",
                class_name=cls.__name__,
                param_name=param.name,
                param_type=type_name,
            )

        resolved[param.name] = instance

    return resolved


def x_resolve_dependencies__mutmut_72(  # noqa: C901
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
        import sys

        module = sys.modules.get(cls.__module__)
        localns = vars(module) if module else {}
        hints = get_type_hints(cls.__init__, globalns=None, localns=localns)
    except NameError:
        # Forward reference error - collect what we can from annotations
        hints = {}
        sig = inspect.signature(cls.__init__)
        for param_name, param in sig.parameters.items():
            if param_name == "self":
                continue
            if param.annotation != inspect.Parameter.empty:
                # Use the annotation directly (may be a string)
                hints[param_name] = param.annotation
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

        # If param_type is a string (forward reference), try to resolve it
        if isinstance(param_type, str):
            # Look up the type in the class's module
            import sys

            module = sys.modules.get(cls.__module__)
            if module and hasattr(module, param_type):
                param_type = getattr(module, param_type)
            else:
                if allow_missing:
                    missing.append(param.name)
                    continue
                raise ValidationError(
                    f"Forward reference '{param_type}' for parameter '{param.name}' could not be resolved",
                    code="RESOLVE_FORWARD_REF_ERROR",
                    class_name=None,
                    param_name=param.name,
                    forward_ref=param_type,
                )

        # Try to resolve from registry by type
        # Strategy: Look for registered instance of this type
        instance = registry.get_by_type(param_type)

        if instance is None:
            if allow_missing:
                missing.append(param.name)
                continue
            type_name = getattr(param_type, "__name__", str(param_type))
            raise NotFoundError(
                f"Dependency '{type_name}' required by {cls.__name__} not found in registry",
                code="RESOLVE_DEPENDENCY_NOT_FOUND",
                class_name=cls.__name__,
                param_name=param.name,
                param_type=type_name,
            )

        resolved[param.name] = instance

    return resolved


def x_resolve_dependencies__mutmut_73(  # noqa: C901
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
        import sys

        module = sys.modules.get(cls.__module__)
        localns = vars(module) if module else {}
        hints = get_type_hints(cls.__init__, globalns=None, localns=localns)
    except NameError:
        # Forward reference error - collect what we can from annotations
        hints = {}
        sig = inspect.signature(cls.__init__)
        for param_name, param in sig.parameters.items():
            if param_name == "self":
                continue
            if param.annotation != inspect.Parameter.empty:
                # Use the annotation directly (may be a string)
                hints[param_name] = param.annotation
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

        # If param_type is a string (forward reference), try to resolve it
        if isinstance(param_type, str):
            # Look up the type in the class's module
            import sys

            module = sys.modules.get(cls.__module__)
            if module and hasattr(module, param_type):
                param_type = getattr(module, param_type)
            else:
                if allow_missing:
                    missing.append(param.name)
                    continue
                raise ValidationError(
                    f"Forward reference '{param_type}' for parameter '{param.name}' could not be resolved",
                    code="RESOLVE_FORWARD_REF_ERROR",
                    class_name=cls.__name__,
                    param_name=None,
                    forward_ref=param_type,
                )

        # Try to resolve from registry by type
        # Strategy: Look for registered instance of this type
        instance = registry.get_by_type(param_type)

        if instance is None:
            if allow_missing:
                missing.append(param.name)
                continue
            type_name = getattr(param_type, "__name__", str(param_type))
            raise NotFoundError(
                f"Dependency '{type_name}' required by {cls.__name__} not found in registry",
                code="RESOLVE_DEPENDENCY_NOT_FOUND",
                class_name=cls.__name__,
                param_name=param.name,
                param_type=type_name,
            )

        resolved[param.name] = instance

    return resolved


def x_resolve_dependencies__mutmut_74(  # noqa: C901
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
        import sys

        module = sys.modules.get(cls.__module__)
        localns = vars(module) if module else {}
        hints = get_type_hints(cls.__init__, globalns=None, localns=localns)
    except NameError:
        # Forward reference error - collect what we can from annotations
        hints = {}
        sig = inspect.signature(cls.__init__)
        for param_name, param in sig.parameters.items():
            if param_name == "self":
                continue
            if param.annotation != inspect.Parameter.empty:
                # Use the annotation directly (may be a string)
                hints[param_name] = param.annotation
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

        # If param_type is a string (forward reference), try to resolve it
        if isinstance(param_type, str):
            # Look up the type in the class's module
            import sys

            module = sys.modules.get(cls.__module__)
            if module and hasattr(module, param_type):
                param_type = getattr(module, param_type)
            else:
                if allow_missing:
                    missing.append(param.name)
                    continue
                raise ValidationError(
                    f"Forward reference '{param_type}' for parameter '{param.name}' could not be resolved",
                    code="RESOLVE_FORWARD_REF_ERROR",
                    class_name=cls.__name__,
                    param_name=param.name,
                    forward_ref=None,
                )

        # Try to resolve from registry by type
        # Strategy: Look for registered instance of this type
        instance = registry.get_by_type(param_type)

        if instance is None:
            if allow_missing:
                missing.append(param.name)
                continue
            type_name = getattr(param_type, "__name__", str(param_type))
            raise NotFoundError(
                f"Dependency '{type_name}' required by {cls.__name__} not found in registry",
                code="RESOLVE_DEPENDENCY_NOT_FOUND",
                class_name=cls.__name__,
                param_name=param.name,
                param_type=type_name,
            )

        resolved[param.name] = instance

    return resolved


def x_resolve_dependencies__mutmut_75(  # noqa: C901
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
        import sys

        module = sys.modules.get(cls.__module__)
        localns = vars(module) if module else {}
        hints = get_type_hints(cls.__init__, globalns=None, localns=localns)
    except NameError:
        # Forward reference error - collect what we can from annotations
        hints = {}
        sig = inspect.signature(cls.__init__)
        for param_name, param in sig.parameters.items():
            if param_name == "self":
                continue
            if param.annotation != inspect.Parameter.empty:
                # Use the annotation directly (may be a string)
                hints[param_name] = param.annotation
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

        # If param_type is a string (forward reference), try to resolve it
        if isinstance(param_type, str):
            # Look up the type in the class's module
            import sys

            module = sys.modules.get(cls.__module__)
            if module and hasattr(module, param_type):
                param_type = getattr(module, param_type)
            else:
                if allow_missing:
                    missing.append(param.name)
                    continue
                raise ValidationError(
                    code="RESOLVE_FORWARD_REF_ERROR",
                    class_name=cls.__name__,
                    param_name=param.name,
                    forward_ref=param_type,
                )

        # Try to resolve from registry by type
        # Strategy: Look for registered instance of this type
        instance = registry.get_by_type(param_type)

        if instance is None:
            if allow_missing:
                missing.append(param.name)
                continue
            type_name = getattr(param_type, "__name__", str(param_type))
            raise NotFoundError(
                f"Dependency '{type_name}' required by {cls.__name__} not found in registry",
                code="RESOLVE_DEPENDENCY_NOT_FOUND",
                class_name=cls.__name__,
                param_name=param.name,
                param_type=type_name,
            )

        resolved[param.name] = instance

    return resolved


def x_resolve_dependencies__mutmut_76(  # noqa: C901
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
        import sys

        module = sys.modules.get(cls.__module__)
        localns = vars(module) if module else {}
        hints = get_type_hints(cls.__init__, globalns=None, localns=localns)
    except NameError:
        # Forward reference error - collect what we can from annotations
        hints = {}
        sig = inspect.signature(cls.__init__)
        for param_name, param in sig.parameters.items():
            if param_name == "self":
                continue
            if param.annotation != inspect.Parameter.empty:
                # Use the annotation directly (may be a string)
                hints[param_name] = param.annotation
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

        # If param_type is a string (forward reference), try to resolve it
        if isinstance(param_type, str):
            # Look up the type in the class's module
            import sys

            module = sys.modules.get(cls.__module__)
            if module and hasattr(module, param_type):
                param_type = getattr(module, param_type)
            else:
                if allow_missing:
                    missing.append(param.name)
                    continue
                raise ValidationError(
                    f"Forward reference '{param_type}' for parameter '{param.name}' could not be resolved",
                    class_name=cls.__name__,
                    param_name=param.name,
                    forward_ref=param_type,
                )

        # Try to resolve from registry by type
        # Strategy: Look for registered instance of this type
        instance = registry.get_by_type(param_type)

        if instance is None:
            if allow_missing:
                missing.append(param.name)
                continue
            type_name = getattr(param_type, "__name__", str(param_type))
            raise NotFoundError(
                f"Dependency '{type_name}' required by {cls.__name__} not found in registry",
                code="RESOLVE_DEPENDENCY_NOT_FOUND",
                class_name=cls.__name__,
                param_name=param.name,
                param_type=type_name,
            )

        resolved[param.name] = instance

    return resolved


def x_resolve_dependencies__mutmut_77(  # noqa: C901
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
        import sys

        module = sys.modules.get(cls.__module__)
        localns = vars(module) if module else {}
        hints = get_type_hints(cls.__init__, globalns=None, localns=localns)
    except NameError:
        # Forward reference error - collect what we can from annotations
        hints = {}
        sig = inspect.signature(cls.__init__)
        for param_name, param in sig.parameters.items():
            if param_name == "self":
                continue
            if param.annotation != inspect.Parameter.empty:
                # Use the annotation directly (may be a string)
                hints[param_name] = param.annotation
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

        # If param_type is a string (forward reference), try to resolve it
        if isinstance(param_type, str):
            # Look up the type in the class's module
            import sys

            module = sys.modules.get(cls.__module__)
            if module and hasattr(module, param_type):
                param_type = getattr(module, param_type)
            else:
                if allow_missing:
                    missing.append(param.name)
                    continue
                raise ValidationError(
                    f"Forward reference '{param_type}' for parameter '{param.name}' could not be resolved",
                    code="RESOLVE_FORWARD_REF_ERROR",
                    param_name=param.name,
                    forward_ref=param_type,
                )

        # Try to resolve from registry by type
        # Strategy: Look for registered instance of this type
        instance = registry.get_by_type(param_type)

        if instance is None:
            if allow_missing:
                missing.append(param.name)
                continue
            type_name = getattr(param_type, "__name__", str(param_type))
            raise NotFoundError(
                f"Dependency '{type_name}' required by {cls.__name__} not found in registry",
                code="RESOLVE_DEPENDENCY_NOT_FOUND",
                class_name=cls.__name__,
                param_name=param.name,
                param_type=type_name,
            )

        resolved[param.name] = instance

    return resolved


def x_resolve_dependencies__mutmut_78(  # noqa: C901
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
        import sys

        module = sys.modules.get(cls.__module__)
        localns = vars(module) if module else {}
        hints = get_type_hints(cls.__init__, globalns=None, localns=localns)
    except NameError:
        # Forward reference error - collect what we can from annotations
        hints = {}
        sig = inspect.signature(cls.__init__)
        for param_name, param in sig.parameters.items():
            if param_name == "self":
                continue
            if param.annotation != inspect.Parameter.empty:
                # Use the annotation directly (may be a string)
                hints[param_name] = param.annotation
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

        # If param_type is a string (forward reference), try to resolve it
        if isinstance(param_type, str):
            # Look up the type in the class's module
            import sys

            module = sys.modules.get(cls.__module__)
            if module and hasattr(module, param_type):
                param_type = getattr(module, param_type)
            else:
                if allow_missing:
                    missing.append(param.name)
                    continue
                raise ValidationError(
                    f"Forward reference '{param_type}' for parameter '{param.name}' could not be resolved",
                    code="RESOLVE_FORWARD_REF_ERROR",
                    class_name=cls.__name__,
                    forward_ref=param_type,
                )

        # Try to resolve from registry by type
        # Strategy: Look for registered instance of this type
        instance = registry.get_by_type(param_type)

        if instance is None:
            if allow_missing:
                missing.append(param.name)
                continue
            type_name = getattr(param_type, "__name__", str(param_type))
            raise NotFoundError(
                f"Dependency '{type_name}' required by {cls.__name__} not found in registry",
                code="RESOLVE_DEPENDENCY_NOT_FOUND",
                class_name=cls.__name__,
                param_name=param.name,
                param_type=type_name,
            )

        resolved[param.name] = instance

    return resolved


def x_resolve_dependencies__mutmut_79(  # noqa: C901
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
        import sys

        module = sys.modules.get(cls.__module__)
        localns = vars(module) if module else {}
        hints = get_type_hints(cls.__init__, globalns=None, localns=localns)
    except NameError:
        # Forward reference error - collect what we can from annotations
        hints = {}
        sig = inspect.signature(cls.__init__)
        for param_name, param in sig.parameters.items():
            if param_name == "self":
                continue
            if param.annotation != inspect.Parameter.empty:
                # Use the annotation directly (may be a string)
                hints[param_name] = param.annotation
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

        # If param_type is a string (forward reference), try to resolve it
        if isinstance(param_type, str):
            # Look up the type in the class's module
            import sys

            module = sys.modules.get(cls.__module__)
            if module and hasattr(module, param_type):
                param_type = getattr(module, param_type)
            else:
                if allow_missing:
                    missing.append(param.name)
                    continue
                raise ValidationError(
                    f"Forward reference '{param_type}' for parameter '{param.name}' could not be resolved",
                    code="RESOLVE_FORWARD_REF_ERROR",
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
            type_name = getattr(param_type, "__name__", str(param_type))
            raise NotFoundError(
                f"Dependency '{type_name}' required by {cls.__name__} not found in registry",
                code="RESOLVE_DEPENDENCY_NOT_FOUND",
                class_name=cls.__name__,
                param_name=param.name,
                param_type=type_name,
            )

        resolved[param.name] = instance

    return resolved


def x_resolve_dependencies__mutmut_80(  # noqa: C901
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
        import sys

        module = sys.modules.get(cls.__module__)
        localns = vars(module) if module else {}
        hints = get_type_hints(cls.__init__, globalns=None, localns=localns)
    except NameError:
        # Forward reference error - collect what we can from annotations
        hints = {}
        sig = inspect.signature(cls.__init__)
        for param_name, param in sig.parameters.items():
            if param_name == "self":
                continue
            if param.annotation != inspect.Parameter.empty:
                # Use the annotation directly (may be a string)
                hints[param_name] = param.annotation
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

        # If param_type is a string (forward reference), try to resolve it
        if isinstance(param_type, str):
            # Look up the type in the class's module
            import sys

            module = sys.modules.get(cls.__module__)
            if module and hasattr(module, param_type):
                param_type = getattr(module, param_type)
            else:
                if allow_missing:
                    missing.append(param.name)
                    continue
                raise ValidationError(
                    f"Forward reference '{param_type}' for parameter '{param.name}' could not be resolved",
                    code="XXRESOLVE_FORWARD_REF_ERRORXX",
                    class_name=cls.__name__,
                    param_name=param.name,
                    forward_ref=param_type,
                )

        # Try to resolve from registry by type
        # Strategy: Look for registered instance of this type
        instance = registry.get_by_type(param_type)

        if instance is None:
            if allow_missing:
                missing.append(param.name)
                continue
            type_name = getattr(param_type, "__name__", str(param_type))
            raise NotFoundError(
                f"Dependency '{type_name}' required by {cls.__name__} not found in registry",
                code="RESOLVE_DEPENDENCY_NOT_FOUND",
                class_name=cls.__name__,
                param_name=param.name,
                param_type=type_name,
            )

        resolved[param.name] = instance

    return resolved


def x_resolve_dependencies__mutmut_81(  # noqa: C901
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
        import sys

        module = sys.modules.get(cls.__module__)
        localns = vars(module) if module else {}
        hints = get_type_hints(cls.__init__, globalns=None, localns=localns)
    except NameError:
        # Forward reference error - collect what we can from annotations
        hints = {}
        sig = inspect.signature(cls.__init__)
        for param_name, param in sig.parameters.items():
            if param_name == "self":
                continue
            if param.annotation != inspect.Parameter.empty:
                # Use the annotation directly (may be a string)
                hints[param_name] = param.annotation
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

        # If param_type is a string (forward reference), try to resolve it
        if isinstance(param_type, str):
            # Look up the type in the class's module
            import sys

            module = sys.modules.get(cls.__module__)
            if module and hasattr(module, param_type):
                param_type = getattr(module, param_type)
            else:
                if allow_missing:
                    missing.append(param.name)
                    continue
                raise ValidationError(
                    f"Forward reference '{param_type}' for parameter '{param.name}' could not be resolved",
                    code="resolve_forward_ref_error",
                    class_name=cls.__name__,
                    param_name=param.name,
                    forward_ref=param_type,
                )

        # Try to resolve from registry by type
        # Strategy: Look for registered instance of this type
        instance = registry.get_by_type(param_type)

        if instance is None:
            if allow_missing:
                missing.append(param.name)
                continue
            type_name = getattr(param_type, "__name__", str(param_type))
            raise NotFoundError(
                f"Dependency '{type_name}' required by {cls.__name__} not found in registry",
                code="RESOLVE_DEPENDENCY_NOT_FOUND",
                class_name=cls.__name__,
                param_name=param.name,
                param_type=type_name,
            )

        resolved[param.name] = instance

    return resolved


def x_resolve_dependencies__mutmut_82(  # noqa: C901
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
        import sys

        module = sys.modules.get(cls.__module__)
        localns = vars(module) if module else {}
        hints = get_type_hints(cls.__init__, globalns=None, localns=localns)
    except NameError:
        # Forward reference error - collect what we can from annotations
        hints = {}
        sig = inspect.signature(cls.__init__)
        for param_name, param in sig.parameters.items():
            if param_name == "self":
                continue
            if param.annotation != inspect.Parameter.empty:
                # Use the annotation directly (may be a string)
                hints[param_name] = param.annotation
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

        # If param_type is a string (forward reference), try to resolve it
        if isinstance(param_type, str):
            # Look up the type in the class's module
            import sys

            module = sys.modules.get(cls.__module__)
            if module and hasattr(module, param_type):
                param_type = getattr(module, param_type)
            else:
                if allow_missing:
                    missing.append(param.name)
                    continue
                raise ValidationError(
                    f"Forward reference '{param_type}' for parameter '{param.name}' could not be resolved",
                    code="RESOLVE_FORWARD_REF_ERROR",
                    class_name=cls.__name__,
                    param_name=param.name,
                    forward_ref=param_type,
                )

        # Try to resolve from registry by type
        # Strategy: Look for registered instance of this type
        instance = None

        if instance is None:
            if allow_missing:
                missing.append(param.name)
                continue
            type_name = getattr(param_type, "__name__", str(param_type))
            raise NotFoundError(
                f"Dependency '{type_name}' required by {cls.__name__} not found in registry",
                code="RESOLVE_DEPENDENCY_NOT_FOUND",
                class_name=cls.__name__,
                param_name=param.name,
                param_type=type_name,
            )

        resolved[param.name] = instance

    return resolved


def x_resolve_dependencies__mutmut_83(  # noqa: C901
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
        import sys

        module = sys.modules.get(cls.__module__)
        localns = vars(module) if module else {}
        hints = get_type_hints(cls.__init__, globalns=None, localns=localns)
    except NameError:
        # Forward reference error - collect what we can from annotations
        hints = {}
        sig = inspect.signature(cls.__init__)
        for param_name, param in sig.parameters.items():
            if param_name == "self":
                continue
            if param.annotation != inspect.Parameter.empty:
                # Use the annotation directly (may be a string)
                hints[param_name] = param.annotation
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

        # If param_type is a string (forward reference), try to resolve it
        if isinstance(param_type, str):
            # Look up the type in the class's module
            import sys

            module = sys.modules.get(cls.__module__)
            if module and hasattr(module, param_type):
                param_type = getattr(module, param_type)
            else:
                if allow_missing:
                    missing.append(param.name)
                    continue
                raise ValidationError(
                    f"Forward reference '{param_type}' for parameter '{param.name}' could not be resolved",
                    code="RESOLVE_FORWARD_REF_ERROR",
                    class_name=cls.__name__,
                    param_name=param.name,
                    forward_ref=param_type,
                )

        # Try to resolve from registry by type
        # Strategy: Look for registered instance of this type
        instance = registry.get_by_type(None)

        if instance is None:
            if allow_missing:
                missing.append(param.name)
                continue
            type_name = getattr(param_type, "__name__", str(param_type))
            raise NotFoundError(
                f"Dependency '{type_name}' required by {cls.__name__} not found in registry",
                code="RESOLVE_DEPENDENCY_NOT_FOUND",
                class_name=cls.__name__,
                param_name=param.name,
                param_type=type_name,
            )

        resolved[param.name] = instance

    return resolved


def x_resolve_dependencies__mutmut_84(  # noqa: C901
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
        import sys

        module = sys.modules.get(cls.__module__)
        localns = vars(module) if module else {}
        hints = get_type_hints(cls.__init__, globalns=None, localns=localns)
    except NameError:
        # Forward reference error - collect what we can from annotations
        hints = {}
        sig = inspect.signature(cls.__init__)
        for param_name, param in sig.parameters.items():
            if param_name == "self":
                continue
            if param.annotation != inspect.Parameter.empty:
                # Use the annotation directly (may be a string)
                hints[param_name] = param.annotation
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

        # If param_type is a string (forward reference), try to resolve it
        if isinstance(param_type, str):
            # Look up the type in the class's module
            import sys

            module = sys.modules.get(cls.__module__)
            if module and hasattr(module, param_type):
                param_type = getattr(module, param_type)
            else:
                if allow_missing:
                    missing.append(param.name)
                    continue
                raise ValidationError(
                    f"Forward reference '{param_type}' for parameter '{param.name}' could not be resolved",
                    code="RESOLVE_FORWARD_REF_ERROR",
                    class_name=cls.__name__,
                    param_name=param.name,
                    forward_ref=param_type,
                )

        # Try to resolve from registry by type
        # Strategy: Look for registered instance of this type
        instance = registry.get_by_type(param_type)

        if instance is not None:
            if allow_missing:
                missing.append(param.name)
                continue
            type_name = getattr(param_type, "__name__", str(param_type))
            raise NotFoundError(
                f"Dependency '{type_name}' required by {cls.__name__} not found in registry",
                code="RESOLVE_DEPENDENCY_NOT_FOUND",
                class_name=cls.__name__,
                param_name=param.name,
                param_type=type_name,
            )

        resolved[param.name] = instance

    return resolved


def x_resolve_dependencies__mutmut_85(  # noqa: C901
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
        import sys

        module = sys.modules.get(cls.__module__)
        localns = vars(module) if module else {}
        hints = get_type_hints(cls.__init__, globalns=None, localns=localns)
    except NameError:
        # Forward reference error - collect what we can from annotations
        hints = {}
        sig = inspect.signature(cls.__init__)
        for param_name, param in sig.parameters.items():
            if param_name == "self":
                continue
            if param.annotation != inspect.Parameter.empty:
                # Use the annotation directly (may be a string)
                hints[param_name] = param.annotation
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

        # If param_type is a string (forward reference), try to resolve it
        if isinstance(param_type, str):
            # Look up the type in the class's module
            import sys

            module = sys.modules.get(cls.__module__)
            if module and hasattr(module, param_type):
                param_type = getattr(module, param_type)
            else:
                if allow_missing:
                    missing.append(param.name)
                    continue
                raise ValidationError(
                    f"Forward reference '{param_type}' for parameter '{param.name}' could not be resolved",
                    code="RESOLVE_FORWARD_REF_ERROR",
                    class_name=cls.__name__,
                    param_name=param.name,
                    forward_ref=param_type,
                )

        # Try to resolve from registry by type
        # Strategy: Look for registered instance of this type
        instance = registry.get_by_type(param_type)

        if instance is None:
            if allow_missing:
                missing.append(None)
                continue
            type_name = getattr(param_type, "__name__", str(param_type))
            raise NotFoundError(
                f"Dependency '{type_name}' required by {cls.__name__} not found in registry",
                code="RESOLVE_DEPENDENCY_NOT_FOUND",
                class_name=cls.__name__,
                param_name=param.name,
                param_type=type_name,
            )

        resolved[param.name] = instance

    return resolved


def x_resolve_dependencies__mutmut_86(  # noqa: C901
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
        import sys

        module = sys.modules.get(cls.__module__)
        localns = vars(module) if module else {}
        hints = get_type_hints(cls.__init__, globalns=None, localns=localns)
    except NameError:
        # Forward reference error - collect what we can from annotations
        hints = {}
        sig = inspect.signature(cls.__init__)
        for param_name, param in sig.parameters.items():
            if param_name == "self":
                continue
            if param.annotation != inspect.Parameter.empty:
                # Use the annotation directly (may be a string)
                hints[param_name] = param.annotation
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

        # If param_type is a string (forward reference), try to resolve it
        if isinstance(param_type, str):
            # Look up the type in the class's module
            import sys

            module = sys.modules.get(cls.__module__)
            if module and hasattr(module, param_type):
                param_type = getattr(module, param_type)
            else:
                if allow_missing:
                    missing.append(param.name)
                    continue
                raise ValidationError(
                    f"Forward reference '{param_type}' for parameter '{param.name}' could not be resolved",
                    code="RESOLVE_FORWARD_REF_ERROR",
                    class_name=cls.__name__,
                    param_name=param.name,
                    forward_ref=param_type,
                )

        # Try to resolve from registry by type
        # Strategy: Look for registered instance of this type
        instance = registry.get_by_type(param_type)

        if instance is None:
            if allow_missing:
                missing.append(param.name)
                break
            type_name = getattr(param_type, "__name__", str(param_type))
            raise NotFoundError(
                f"Dependency '{type_name}' required by {cls.__name__} not found in registry",
                code="RESOLVE_DEPENDENCY_NOT_FOUND",
                class_name=cls.__name__,
                param_name=param.name,
                param_type=type_name,
            )

        resolved[param.name] = instance

    return resolved


def x_resolve_dependencies__mutmut_87(  # noqa: C901
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
        import sys

        module = sys.modules.get(cls.__module__)
        localns = vars(module) if module else {}
        hints = get_type_hints(cls.__init__, globalns=None, localns=localns)
    except NameError:
        # Forward reference error - collect what we can from annotations
        hints = {}
        sig = inspect.signature(cls.__init__)
        for param_name, param in sig.parameters.items():
            if param_name == "self":
                continue
            if param.annotation != inspect.Parameter.empty:
                # Use the annotation directly (may be a string)
                hints[param_name] = param.annotation
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

        # If param_type is a string (forward reference), try to resolve it
        if isinstance(param_type, str):
            # Look up the type in the class's module
            import sys

            module = sys.modules.get(cls.__module__)
            if module and hasattr(module, param_type):
                param_type = getattr(module, param_type)
            else:
                if allow_missing:
                    missing.append(param.name)
                    continue
                raise ValidationError(
                    f"Forward reference '{param_type}' for parameter '{param.name}' could not be resolved",
                    code="RESOLVE_FORWARD_REF_ERROR",
                    class_name=cls.__name__,
                    param_name=param.name,
                    forward_ref=param_type,
                )

        # Try to resolve from registry by type
        # Strategy: Look for registered instance of this type
        instance = registry.get_by_type(param_type)

        if instance is None:
            if allow_missing:
                missing.append(param.name)
                continue
            type_name = None
            raise NotFoundError(
                f"Dependency '{type_name}' required by {cls.__name__} not found in registry",
                code="RESOLVE_DEPENDENCY_NOT_FOUND",
                class_name=cls.__name__,
                param_name=param.name,
                param_type=type_name,
            )

        resolved[param.name] = instance

    return resolved


def x_resolve_dependencies__mutmut_88(  # noqa: C901
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
        import sys

        module = sys.modules.get(cls.__module__)
        localns = vars(module) if module else {}
        hints = get_type_hints(cls.__init__, globalns=None, localns=localns)
    except NameError:
        # Forward reference error - collect what we can from annotations
        hints = {}
        sig = inspect.signature(cls.__init__)
        for param_name, param in sig.parameters.items():
            if param_name == "self":
                continue
            if param.annotation != inspect.Parameter.empty:
                # Use the annotation directly (may be a string)
                hints[param_name] = param.annotation
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

        # If param_type is a string (forward reference), try to resolve it
        if isinstance(param_type, str):
            # Look up the type in the class's module
            import sys

            module = sys.modules.get(cls.__module__)
            if module and hasattr(module, param_type):
                param_type = getattr(module, param_type)
            else:
                if allow_missing:
                    missing.append(param.name)
                    continue
                raise ValidationError(
                    f"Forward reference '{param_type}' for parameter '{param.name}' could not be resolved",
                    code="RESOLVE_FORWARD_REF_ERROR",
                    class_name=cls.__name__,
                    param_name=param.name,
                    forward_ref=param_type,
                )

        # Try to resolve from registry by type
        # Strategy: Look for registered instance of this type
        instance = registry.get_by_type(param_type)

        if instance is None:
            if allow_missing:
                missing.append(param.name)
                continue
            type_name = getattr(None, "__name__", str(param_type))
            raise NotFoundError(
                f"Dependency '{type_name}' required by {cls.__name__} not found in registry",
                code="RESOLVE_DEPENDENCY_NOT_FOUND",
                class_name=cls.__name__,
                param_name=param.name,
                param_type=type_name,
            )

        resolved[param.name] = instance

    return resolved


def x_resolve_dependencies__mutmut_89(  # noqa: C901
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
        import sys

        module = sys.modules.get(cls.__module__)
        localns = vars(module) if module else {}
        hints = get_type_hints(cls.__init__, globalns=None, localns=localns)
    except NameError:
        # Forward reference error - collect what we can from annotations
        hints = {}
        sig = inspect.signature(cls.__init__)
        for param_name, param in sig.parameters.items():
            if param_name == "self":
                continue
            if param.annotation != inspect.Parameter.empty:
                # Use the annotation directly (may be a string)
                hints[param_name] = param.annotation
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

        # If param_type is a string (forward reference), try to resolve it
        if isinstance(param_type, str):
            # Look up the type in the class's module
            import sys

            module = sys.modules.get(cls.__module__)
            if module and hasattr(module, param_type):
                param_type = getattr(module, param_type)
            else:
                if allow_missing:
                    missing.append(param.name)
                    continue
                raise ValidationError(
                    f"Forward reference '{param_type}' for parameter '{param.name}' could not be resolved",
                    code="RESOLVE_FORWARD_REF_ERROR",
                    class_name=cls.__name__,
                    param_name=param.name,
                    forward_ref=param_type,
                )

        # Try to resolve from registry by type
        # Strategy: Look for registered instance of this type
        instance = registry.get_by_type(param_type)

        if instance is None:
            if allow_missing:
                missing.append(param.name)
                continue
            type_name = getattr(param_type, None, str(param_type))
            raise NotFoundError(
                f"Dependency '{type_name}' required by {cls.__name__} not found in registry",
                code="RESOLVE_DEPENDENCY_NOT_FOUND",
                class_name=cls.__name__,
                param_name=param.name,
                param_type=type_name,
            )

        resolved[param.name] = instance

    return resolved


def x_resolve_dependencies__mutmut_90(  # noqa: C901
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
        import sys

        module = sys.modules.get(cls.__module__)
        localns = vars(module) if module else {}
        hints = get_type_hints(cls.__init__, globalns=None, localns=localns)
    except NameError:
        # Forward reference error - collect what we can from annotations
        hints = {}
        sig = inspect.signature(cls.__init__)
        for param_name, param in sig.parameters.items():
            if param_name == "self":
                continue
            if param.annotation != inspect.Parameter.empty:
                # Use the annotation directly (may be a string)
                hints[param_name] = param.annotation
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

        # If param_type is a string (forward reference), try to resolve it
        if isinstance(param_type, str):
            # Look up the type in the class's module
            import sys

            module = sys.modules.get(cls.__module__)
            if module and hasattr(module, param_type):
                param_type = getattr(module, param_type)
            else:
                if allow_missing:
                    missing.append(param.name)
                    continue
                raise ValidationError(
                    f"Forward reference '{param_type}' for parameter '{param.name}' could not be resolved",
                    code="RESOLVE_FORWARD_REF_ERROR",
                    class_name=cls.__name__,
                    param_name=param.name,
                    forward_ref=param_type,
                )

        # Try to resolve from registry by type
        # Strategy: Look for registered instance of this type
        instance = registry.get_by_type(param_type)

        if instance is None:
            if allow_missing:
                missing.append(param.name)
                continue
            type_name = getattr(param_type, "__name__", None)
            raise NotFoundError(
                f"Dependency '{type_name}' required by {cls.__name__} not found in registry",
                code="RESOLVE_DEPENDENCY_NOT_FOUND",
                class_name=cls.__name__,
                param_name=param.name,
                param_type=type_name,
            )

        resolved[param.name] = instance

    return resolved


def x_resolve_dependencies__mutmut_91(  # noqa: C901
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
        import sys

        module = sys.modules.get(cls.__module__)
        localns = vars(module) if module else {}
        hints = get_type_hints(cls.__init__, globalns=None, localns=localns)
    except NameError:
        # Forward reference error - collect what we can from annotations
        hints = {}
        sig = inspect.signature(cls.__init__)
        for param_name, param in sig.parameters.items():
            if param_name == "self":
                continue
            if param.annotation != inspect.Parameter.empty:
                # Use the annotation directly (may be a string)
                hints[param_name] = param.annotation
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

        # If param_type is a string (forward reference), try to resolve it
        if isinstance(param_type, str):
            # Look up the type in the class's module
            import sys

            module = sys.modules.get(cls.__module__)
            if module and hasattr(module, param_type):
                param_type = getattr(module, param_type)
            else:
                if allow_missing:
                    missing.append(param.name)
                    continue
                raise ValidationError(
                    f"Forward reference '{param_type}' for parameter '{param.name}' could not be resolved",
                    code="RESOLVE_FORWARD_REF_ERROR",
                    class_name=cls.__name__,
                    param_name=param.name,
                    forward_ref=param_type,
                )

        # Try to resolve from registry by type
        # Strategy: Look for registered instance of this type
        instance = registry.get_by_type(param_type)

        if instance is None:
            if allow_missing:
                missing.append(param.name)
                continue
            type_name = getattr("__name__", str(param_type))
            raise NotFoundError(
                f"Dependency '{type_name}' required by {cls.__name__} not found in registry",
                code="RESOLVE_DEPENDENCY_NOT_FOUND",
                class_name=cls.__name__,
                param_name=param.name,
                param_type=type_name,
            )

        resolved[param.name] = instance

    return resolved


def x_resolve_dependencies__mutmut_92(  # noqa: C901
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
        import sys

        module = sys.modules.get(cls.__module__)
        localns = vars(module) if module else {}
        hints = get_type_hints(cls.__init__, globalns=None, localns=localns)
    except NameError:
        # Forward reference error - collect what we can from annotations
        hints = {}
        sig = inspect.signature(cls.__init__)
        for param_name, param in sig.parameters.items():
            if param_name == "self":
                continue
            if param.annotation != inspect.Parameter.empty:
                # Use the annotation directly (may be a string)
                hints[param_name] = param.annotation
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

        # If param_type is a string (forward reference), try to resolve it
        if isinstance(param_type, str):
            # Look up the type in the class's module
            import sys

            module = sys.modules.get(cls.__module__)
            if module and hasattr(module, param_type):
                param_type = getattr(module, param_type)
            else:
                if allow_missing:
                    missing.append(param.name)
                    continue
                raise ValidationError(
                    f"Forward reference '{param_type}' for parameter '{param.name}' could not be resolved",
                    code="RESOLVE_FORWARD_REF_ERROR",
                    class_name=cls.__name__,
                    param_name=param.name,
                    forward_ref=param_type,
                )

        # Try to resolve from registry by type
        # Strategy: Look for registered instance of this type
        instance = registry.get_by_type(param_type)

        if instance is None:
            if allow_missing:
                missing.append(param.name)
                continue
            type_name = getattr(param_type, str(param_type))
            raise NotFoundError(
                f"Dependency '{type_name}' required by {cls.__name__} not found in registry",
                code="RESOLVE_DEPENDENCY_NOT_FOUND",
                class_name=cls.__name__,
                param_name=param.name,
                param_type=type_name,
            )

        resolved[param.name] = instance

    return resolved


def x_resolve_dependencies__mutmut_93(  # noqa: C901
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
        import sys

        module = sys.modules.get(cls.__module__)
        localns = vars(module) if module else {}
        hints = get_type_hints(cls.__init__, globalns=None, localns=localns)
    except NameError:
        # Forward reference error - collect what we can from annotations
        hints = {}
        sig = inspect.signature(cls.__init__)
        for param_name, param in sig.parameters.items():
            if param_name == "self":
                continue
            if param.annotation != inspect.Parameter.empty:
                # Use the annotation directly (may be a string)
                hints[param_name] = param.annotation
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

        # If param_type is a string (forward reference), try to resolve it
        if isinstance(param_type, str):
            # Look up the type in the class's module
            import sys

            module = sys.modules.get(cls.__module__)
            if module and hasattr(module, param_type):
                param_type = getattr(module, param_type)
            else:
                if allow_missing:
                    missing.append(param.name)
                    continue
                raise ValidationError(
                    f"Forward reference '{param_type}' for parameter '{param.name}' could not be resolved",
                    code="RESOLVE_FORWARD_REF_ERROR",
                    class_name=cls.__name__,
                    param_name=param.name,
                    forward_ref=param_type,
                )

        # Try to resolve from registry by type
        # Strategy: Look for registered instance of this type
        instance = registry.get_by_type(param_type)

        if instance is None:
            if allow_missing:
                missing.append(param.name)
                continue
            type_name = getattr(param_type, "__name__", )
            raise NotFoundError(
                f"Dependency '{type_name}' required by {cls.__name__} not found in registry",
                code="RESOLVE_DEPENDENCY_NOT_FOUND",
                class_name=cls.__name__,
                param_name=param.name,
                param_type=type_name,
            )

        resolved[param.name] = instance

    return resolved


def x_resolve_dependencies__mutmut_94(  # noqa: C901
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
        import sys

        module = sys.modules.get(cls.__module__)
        localns = vars(module) if module else {}
        hints = get_type_hints(cls.__init__, globalns=None, localns=localns)
    except NameError:
        # Forward reference error - collect what we can from annotations
        hints = {}
        sig = inspect.signature(cls.__init__)
        for param_name, param in sig.parameters.items():
            if param_name == "self":
                continue
            if param.annotation != inspect.Parameter.empty:
                # Use the annotation directly (may be a string)
                hints[param_name] = param.annotation
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

        # If param_type is a string (forward reference), try to resolve it
        if isinstance(param_type, str):
            # Look up the type in the class's module
            import sys

            module = sys.modules.get(cls.__module__)
            if module and hasattr(module, param_type):
                param_type = getattr(module, param_type)
            else:
                if allow_missing:
                    missing.append(param.name)
                    continue
                raise ValidationError(
                    f"Forward reference '{param_type}' for parameter '{param.name}' could not be resolved",
                    code="RESOLVE_FORWARD_REF_ERROR",
                    class_name=cls.__name__,
                    param_name=param.name,
                    forward_ref=param_type,
                )

        # Try to resolve from registry by type
        # Strategy: Look for registered instance of this type
        instance = registry.get_by_type(param_type)

        if instance is None:
            if allow_missing:
                missing.append(param.name)
                continue
            type_name = getattr(param_type, "XX__name__XX", str(param_type))
            raise NotFoundError(
                f"Dependency '{type_name}' required by {cls.__name__} not found in registry",
                code="RESOLVE_DEPENDENCY_NOT_FOUND",
                class_name=cls.__name__,
                param_name=param.name,
                param_type=type_name,
            )

        resolved[param.name] = instance

    return resolved


def x_resolve_dependencies__mutmut_95(  # noqa: C901
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
        import sys

        module = sys.modules.get(cls.__module__)
        localns = vars(module) if module else {}
        hints = get_type_hints(cls.__init__, globalns=None, localns=localns)
    except NameError:
        # Forward reference error - collect what we can from annotations
        hints = {}
        sig = inspect.signature(cls.__init__)
        for param_name, param in sig.parameters.items():
            if param_name == "self":
                continue
            if param.annotation != inspect.Parameter.empty:
                # Use the annotation directly (may be a string)
                hints[param_name] = param.annotation
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

        # If param_type is a string (forward reference), try to resolve it
        if isinstance(param_type, str):
            # Look up the type in the class's module
            import sys

            module = sys.modules.get(cls.__module__)
            if module and hasattr(module, param_type):
                param_type = getattr(module, param_type)
            else:
                if allow_missing:
                    missing.append(param.name)
                    continue
                raise ValidationError(
                    f"Forward reference '{param_type}' for parameter '{param.name}' could not be resolved",
                    code="RESOLVE_FORWARD_REF_ERROR",
                    class_name=cls.__name__,
                    param_name=param.name,
                    forward_ref=param_type,
                )

        # Try to resolve from registry by type
        # Strategy: Look for registered instance of this type
        instance = registry.get_by_type(param_type)

        if instance is None:
            if allow_missing:
                missing.append(param.name)
                continue
            type_name = getattr(param_type, "__NAME__", str(param_type))
            raise NotFoundError(
                f"Dependency '{type_name}' required by {cls.__name__} not found in registry",
                code="RESOLVE_DEPENDENCY_NOT_FOUND",
                class_name=cls.__name__,
                param_name=param.name,
                param_type=type_name,
            )

        resolved[param.name] = instance

    return resolved


def x_resolve_dependencies__mutmut_96(  # noqa: C901
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
        import sys

        module = sys.modules.get(cls.__module__)
        localns = vars(module) if module else {}
        hints = get_type_hints(cls.__init__, globalns=None, localns=localns)
    except NameError:
        # Forward reference error - collect what we can from annotations
        hints = {}
        sig = inspect.signature(cls.__init__)
        for param_name, param in sig.parameters.items():
            if param_name == "self":
                continue
            if param.annotation != inspect.Parameter.empty:
                # Use the annotation directly (may be a string)
                hints[param_name] = param.annotation
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

        # If param_type is a string (forward reference), try to resolve it
        if isinstance(param_type, str):
            # Look up the type in the class's module
            import sys

            module = sys.modules.get(cls.__module__)
            if module and hasattr(module, param_type):
                param_type = getattr(module, param_type)
            else:
                if allow_missing:
                    missing.append(param.name)
                    continue
                raise ValidationError(
                    f"Forward reference '{param_type}' for parameter '{param.name}' could not be resolved",
                    code="RESOLVE_FORWARD_REF_ERROR",
                    class_name=cls.__name__,
                    param_name=param.name,
                    forward_ref=param_type,
                )

        # Try to resolve from registry by type
        # Strategy: Look for registered instance of this type
        instance = registry.get_by_type(param_type)

        if instance is None:
            if allow_missing:
                missing.append(param.name)
                continue
            type_name = getattr(param_type, "__name__", str(None))
            raise NotFoundError(
                f"Dependency '{type_name}' required by {cls.__name__} not found in registry",
                code="RESOLVE_DEPENDENCY_NOT_FOUND",
                class_name=cls.__name__,
                param_name=param.name,
                param_type=type_name,
            )

        resolved[param.name] = instance

    return resolved


def x_resolve_dependencies__mutmut_97(  # noqa: C901
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
        import sys

        module = sys.modules.get(cls.__module__)
        localns = vars(module) if module else {}
        hints = get_type_hints(cls.__init__, globalns=None, localns=localns)
    except NameError:
        # Forward reference error - collect what we can from annotations
        hints = {}
        sig = inspect.signature(cls.__init__)
        for param_name, param in sig.parameters.items():
            if param_name == "self":
                continue
            if param.annotation != inspect.Parameter.empty:
                # Use the annotation directly (may be a string)
                hints[param_name] = param.annotation
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

        # If param_type is a string (forward reference), try to resolve it
        if isinstance(param_type, str):
            # Look up the type in the class's module
            import sys

            module = sys.modules.get(cls.__module__)
            if module and hasattr(module, param_type):
                param_type = getattr(module, param_type)
            else:
                if allow_missing:
                    missing.append(param.name)
                    continue
                raise ValidationError(
                    f"Forward reference '{param_type}' for parameter '{param.name}' could not be resolved",
                    code="RESOLVE_FORWARD_REF_ERROR",
                    class_name=cls.__name__,
                    param_name=param.name,
                    forward_ref=param_type,
                )

        # Try to resolve from registry by type
        # Strategy: Look for registered instance of this type
        instance = registry.get_by_type(param_type)

        if instance is None:
            if allow_missing:
                missing.append(param.name)
                continue
            type_name = getattr(param_type, "__name__", str(param_type))
            raise NotFoundError(
                None,
                code="RESOLVE_DEPENDENCY_NOT_FOUND",
                class_name=cls.__name__,
                param_name=param.name,
                param_type=type_name,
            )

        resolved[param.name] = instance

    return resolved


def x_resolve_dependencies__mutmut_98(  # noqa: C901
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
        import sys

        module = sys.modules.get(cls.__module__)
        localns = vars(module) if module else {}
        hints = get_type_hints(cls.__init__, globalns=None, localns=localns)
    except NameError:
        # Forward reference error - collect what we can from annotations
        hints = {}
        sig = inspect.signature(cls.__init__)
        for param_name, param in sig.parameters.items():
            if param_name == "self":
                continue
            if param.annotation != inspect.Parameter.empty:
                # Use the annotation directly (may be a string)
                hints[param_name] = param.annotation
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

        # If param_type is a string (forward reference), try to resolve it
        if isinstance(param_type, str):
            # Look up the type in the class's module
            import sys

            module = sys.modules.get(cls.__module__)
            if module and hasattr(module, param_type):
                param_type = getattr(module, param_type)
            else:
                if allow_missing:
                    missing.append(param.name)
                    continue
                raise ValidationError(
                    f"Forward reference '{param_type}' for parameter '{param.name}' could not be resolved",
                    code="RESOLVE_FORWARD_REF_ERROR",
                    class_name=cls.__name__,
                    param_name=param.name,
                    forward_ref=param_type,
                )

        # Try to resolve from registry by type
        # Strategy: Look for registered instance of this type
        instance = registry.get_by_type(param_type)

        if instance is None:
            if allow_missing:
                missing.append(param.name)
                continue
            type_name = getattr(param_type, "__name__", str(param_type))
            raise NotFoundError(
                f"Dependency '{type_name}' required by {cls.__name__} not found in registry",
                code=None,
                class_name=cls.__name__,
                param_name=param.name,
                param_type=type_name,
            )

        resolved[param.name] = instance

    return resolved


def x_resolve_dependencies__mutmut_99(  # noqa: C901
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
        import sys

        module = sys.modules.get(cls.__module__)
        localns = vars(module) if module else {}
        hints = get_type_hints(cls.__init__, globalns=None, localns=localns)
    except NameError:
        # Forward reference error - collect what we can from annotations
        hints = {}
        sig = inspect.signature(cls.__init__)
        for param_name, param in sig.parameters.items():
            if param_name == "self":
                continue
            if param.annotation != inspect.Parameter.empty:
                # Use the annotation directly (may be a string)
                hints[param_name] = param.annotation
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

        # If param_type is a string (forward reference), try to resolve it
        if isinstance(param_type, str):
            # Look up the type in the class's module
            import sys

            module = sys.modules.get(cls.__module__)
            if module and hasattr(module, param_type):
                param_type = getattr(module, param_type)
            else:
                if allow_missing:
                    missing.append(param.name)
                    continue
                raise ValidationError(
                    f"Forward reference '{param_type}' for parameter '{param.name}' could not be resolved",
                    code="RESOLVE_FORWARD_REF_ERROR",
                    class_name=cls.__name__,
                    param_name=param.name,
                    forward_ref=param_type,
                )

        # Try to resolve from registry by type
        # Strategy: Look for registered instance of this type
        instance = registry.get_by_type(param_type)

        if instance is None:
            if allow_missing:
                missing.append(param.name)
                continue
            type_name = getattr(param_type, "__name__", str(param_type))
            raise NotFoundError(
                f"Dependency '{type_name}' required by {cls.__name__} not found in registry",
                code="RESOLVE_DEPENDENCY_NOT_FOUND",
                class_name=None,
                param_name=param.name,
                param_type=type_name,
            )

        resolved[param.name] = instance

    return resolved


def x_resolve_dependencies__mutmut_100(  # noqa: C901
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
        import sys

        module = sys.modules.get(cls.__module__)
        localns = vars(module) if module else {}
        hints = get_type_hints(cls.__init__, globalns=None, localns=localns)
    except NameError:
        # Forward reference error - collect what we can from annotations
        hints = {}
        sig = inspect.signature(cls.__init__)
        for param_name, param in sig.parameters.items():
            if param_name == "self":
                continue
            if param.annotation != inspect.Parameter.empty:
                # Use the annotation directly (may be a string)
                hints[param_name] = param.annotation
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

        # If param_type is a string (forward reference), try to resolve it
        if isinstance(param_type, str):
            # Look up the type in the class's module
            import sys

            module = sys.modules.get(cls.__module__)
            if module and hasattr(module, param_type):
                param_type = getattr(module, param_type)
            else:
                if allow_missing:
                    missing.append(param.name)
                    continue
                raise ValidationError(
                    f"Forward reference '{param_type}' for parameter '{param.name}' could not be resolved",
                    code="RESOLVE_FORWARD_REF_ERROR",
                    class_name=cls.__name__,
                    param_name=param.name,
                    forward_ref=param_type,
                )

        # Try to resolve from registry by type
        # Strategy: Look for registered instance of this type
        instance = registry.get_by_type(param_type)

        if instance is None:
            if allow_missing:
                missing.append(param.name)
                continue
            type_name = getattr(param_type, "__name__", str(param_type))
            raise NotFoundError(
                f"Dependency '{type_name}' required by {cls.__name__} not found in registry",
                code="RESOLVE_DEPENDENCY_NOT_FOUND",
                class_name=cls.__name__,
                param_name=None,
                param_type=type_name,
            )

        resolved[param.name] = instance

    return resolved


def x_resolve_dependencies__mutmut_101(  # noqa: C901
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
        import sys

        module = sys.modules.get(cls.__module__)
        localns = vars(module) if module else {}
        hints = get_type_hints(cls.__init__, globalns=None, localns=localns)
    except NameError:
        # Forward reference error - collect what we can from annotations
        hints = {}
        sig = inspect.signature(cls.__init__)
        for param_name, param in sig.parameters.items():
            if param_name == "self":
                continue
            if param.annotation != inspect.Parameter.empty:
                # Use the annotation directly (may be a string)
                hints[param_name] = param.annotation
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

        # If param_type is a string (forward reference), try to resolve it
        if isinstance(param_type, str):
            # Look up the type in the class's module
            import sys

            module = sys.modules.get(cls.__module__)
            if module and hasattr(module, param_type):
                param_type = getattr(module, param_type)
            else:
                if allow_missing:
                    missing.append(param.name)
                    continue
                raise ValidationError(
                    f"Forward reference '{param_type}' for parameter '{param.name}' could not be resolved",
                    code="RESOLVE_FORWARD_REF_ERROR",
                    class_name=cls.__name__,
                    param_name=param.name,
                    forward_ref=param_type,
                )

        # Try to resolve from registry by type
        # Strategy: Look for registered instance of this type
        instance = registry.get_by_type(param_type)

        if instance is None:
            if allow_missing:
                missing.append(param.name)
                continue
            type_name = getattr(param_type, "__name__", str(param_type))
            raise NotFoundError(
                f"Dependency '{type_name}' required by {cls.__name__} not found in registry",
                code="RESOLVE_DEPENDENCY_NOT_FOUND",
                class_name=cls.__name__,
                param_name=param.name,
                param_type=None,
            )

        resolved[param.name] = instance

    return resolved


def x_resolve_dependencies__mutmut_102(  # noqa: C901
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
        import sys

        module = sys.modules.get(cls.__module__)
        localns = vars(module) if module else {}
        hints = get_type_hints(cls.__init__, globalns=None, localns=localns)
    except NameError:
        # Forward reference error - collect what we can from annotations
        hints = {}
        sig = inspect.signature(cls.__init__)
        for param_name, param in sig.parameters.items():
            if param_name == "self":
                continue
            if param.annotation != inspect.Parameter.empty:
                # Use the annotation directly (may be a string)
                hints[param_name] = param.annotation
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

        # If param_type is a string (forward reference), try to resolve it
        if isinstance(param_type, str):
            # Look up the type in the class's module
            import sys

            module = sys.modules.get(cls.__module__)
            if module and hasattr(module, param_type):
                param_type = getattr(module, param_type)
            else:
                if allow_missing:
                    missing.append(param.name)
                    continue
                raise ValidationError(
                    f"Forward reference '{param_type}' for parameter '{param.name}' could not be resolved",
                    code="RESOLVE_FORWARD_REF_ERROR",
                    class_name=cls.__name__,
                    param_name=param.name,
                    forward_ref=param_type,
                )

        # Try to resolve from registry by type
        # Strategy: Look for registered instance of this type
        instance = registry.get_by_type(param_type)

        if instance is None:
            if allow_missing:
                missing.append(param.name)
                continue
            type_name = getattr(param_type, "__name__", str(param_type))
            raise NotFoundError(
                code="RESOLVE_DEPENDENCY_NOT_FOUND",
                class_name=cls.__name__,
                param_name=param.name,
                param_type=type_name,
            )

        resolved[param.name] = instance

    return resolved


def x_resolve_dependencies__mutmut_103(  # noqa: C901
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
        import sys

        module = sys.modules.get(cls.__module__)
        localns = vars(module) if module else {}
        hints = get_type_hints(cls.__init__, globalns=None, localns=localns)
    except NameError:
        # Forward reference error - collect what we can from annotations
        hints = {}
        sig = inspect.signature(cls.__init__)
        for param_name, param in sig.parameters.items():
            if param_name == "self":
                continue
            if param.annotation != inspect.Parameter.empty:
                # Use the annotation directly (may be a string)
                hints[param_name] = param.annotation
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

        # If param_type is a string (forward reference), try to resolve it
        if isinstance(param_type, str):
            # Look up the type in the class's module
            import sys

            module = sys.modules.get(cls.__module__)
            if module and hasattr(module, param_type):
                param_type = getattr(module, param_type)
            else:
                if allow_missing:
                    missing.append(param.name)
                    continue
                raise ValidationError(
                    f"Forward reference '{param_type}' for parameter '{param.name}' could not be resolved",
                    code="RESOLVE_FORWARD_REF_ERROR",
                    class_name=cls.__name__,
                    param_name=param.name,
                    forward_ref=param_type,
                )

        # Try to resolve from registry by type
        # Strategy: Look for registered instance of this type
        instance = registry.get_by_type(param_type)

        if instance is None:
            if allow_missing:
                missing.append(param.name)
                continue
            type_name = getattr(param_type, "__name__", str(param_type))
            raise NotFoundError(
                f"Dependency '{type_name}' required by {cls.__name__} not found in registry",
                class_name=cls.__name__,
                param_name=param.name,
                param_type=type_name,
            )

        resolved[param.name] = instance

    return resolved


def x_resolve_dependencies__mutmut_104(  # noqa: C901
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
        import sys

        module = sys.modules.get(cls.__module__)
        localns = vars(module) if module else {}
        hints = get_type_hints(cls.__init__, globalns=None, localns=localns)
    except NameError:
        # Forward reference error - collect what we can from annotations
        hints = {}
        sig = inspect.signature(cls.__init__)
        for param_name, param in sig.parameters.items():
            if param_name == "self":
                continue
            if param.annotation != inspect.Parameter.empty:
                # Use the annotation directly (may be a string)
                hints[param_name] = param.annotation
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

        # If param_type is a string (forward reference), try to resolve it
        if isinstance(param_type, str):
            # Look up the type in the class's module
            import sys

            module = sys.modules.get(cls.__module__)
            if module and hasattr(module, param_type):
                param_type = getattr(module, param_type)
            else:
                if allow_missing:
                    missing.append(param.name)
                    continue
                raise ValidationError(
                    f"Forward reference '{param_type}' for parameter '{param.name}' could not be resolved",
                    code="RESOLVE_FORWARD_REF_ERROR",
                    class_name=cls.__name__,
                    param_name=param.name,
                    forward_ref=param_type,
                )

        # Try to resolve from registry by type
        # Strategy: Look for registered instance of this type
        instance = registry.get_by_type(param_type)

        if instance is None:
            if allow_missing:
                missing.append(param.name)
                continue
            type_name = getattr(param_type, "__name__", str(param_type))
            raise NotFoundError(
                f"Dependency '{type_name}' required by {cls.__name__} not found in registry",
                code="RESOLVE_DEPENDENCY_NOT_FOUND",
                param_name=param.name,
                param_type=type_name,
            )

        resolved[param.name] = instance

    return resolved


def x_resolve_dependencies__mutmut_105(  # noqa: C901
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
        import sys

        module = sys.modules.get(cls.__module__)
        localns = vars(module) if module else {}
        hints = get_type_hints(cls.__init__, globalns=None, localns=localns)
    except NameError:
        # Forward reference error - collect what we can from annotations
        hints = {}
        sig = inspect.signature(cls.__init__)
        for param_name, param in sig.parameters.items():
            if param_name == "self":
                continue
            if param.annotation != inspect.Parameter.empty:
                # Use the annotation directly (may be a string)
                hints[param_name] = param.annotation
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

        # If param_type is a string (forward reference), try to resolve it
        if isinstance(param_type, str):
            # Look up the type in the class's module
            import sys

            module = sys.modules.get(cls.__module__)
            if module and hasattr(module, param_type):
                param_type = getattr(module, param_type)
            else:
                if allow_missing:
                    missing.append(param.name)
                    continue
                raise ValidationError(
                    f"Forward reference '{param_type}' for parameter '{param.name}' could not be resolved",
                    code="RESOLVE_FORWARD_REF_ERROR",
                    class_name=cls.__name__,
                    param_name=param.name,
                    forward_ref=param_type,
                )

        # Try to resolve from registry by type
        # Strategy: Look for registered instance of this type
        instance = registry.get_by_type(param_type)

        if instance is None:
            if allow_missing:
                missing.append(param.name)
                continue
            type_name = getattr(param_type, "__name__", str(param_type))
            raise NotFoundError(
                f"Dependency '{type_name}' required by {cls.__name__} not found in registry",
                code="RESOLVE_DEPENDENCY_NOT_FOUND",
                class_name=cls.__name__,
                param_type=type_name,
            )

        resolved[param.name] = instance

    return resolved


def x_resolve_dependencies__mutmut_106(  # noqa: C901
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
        import sys

        module = sys.modules.get(cls.__module__)
        localns = vars(module) if module else {}
        hints = get_type_hints(cls.__init__, globalns=None, localns=localns)
    except NameError:
        # Forward reference error - collect what we can from annotations
        hints = {}
        sig = inspect.signature(cls.__init__)
        for param_name, param in sig.parameters.items():
            if param_name == "self":
                continue
            if param.annotation != inspect.Parameter.empty:
                # Use the annotation directly (may be a string)
                hints[param_name] = param.annotation
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

        # If param_type is a string (forward reference), try to resolve it
        if isinstance(param_type, str):
            # Look up the type in the class's module
            import sys

            module = sys.modules.get(cls.__module__)
            if module and hasattr(module, param_type):
                param_type = getattr(module, param_type)
            else:
                if allow_missing:
                    missing.append(param.name)
                    continue
                raise ValidationError(
                    f"Forward reference '{param_type}' for parameter '{param.name}' could not be resolved",
                    code="RESOLVE_FORWARD_REF_ERROR",
                    class_name=cls.__name__,
                    param_name=param.name,
                    forward_ref=param_type,
                )

        # Try to resolve from registry by type
        # Strategy: Look for registered instance of this type
        instance = registry.get_by_type(param_type)

        if instance is None:
            if allow_missing:
                missing.append(param.name)
                continue
            type_name = getattr(param_type, "__name__", str(param_type))
            raise NotFoundError(
                f"Dependency '{type_name}' required by {cls.__name__} not found in registry",
                code="RESOLVE_DEPENDENCY_NOT_FOUND",
                class_name=cls.__name__,
                param_name=param.name,
                )

        resolved[param.name] = instance

    return resolved


def x_resolve_dependencies__mutmut_107(  # noqa: C901
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
        import sys

        module = sys.modules.get(cls.__module__)
        localns = vars(module) if module else {}
        hints = get_type_hints(cls.__init__, globalns=None, localns=localns)
    except NameError:
        # Forward reference error - collect what we can from annotations
        hints = {}
        sig = inspect.signature(cls.__init__)
        for param_name, param in sig.parameters.items():
            if param_name == "self":
                continue
            if param.annotation != inspect.Parameter.empty:
                # Use the annotation directly (may be a string)
                hints[param_name] = param.annotation
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

        # If param_type is a string (forward reference), try to resolve it
        if isinstance(param_type, str):
            # Look up the type in the class's module
            import sys

            module = sys.modules.get(cls.__module__)
            if module and hasattr(module, param_type):
                param_type = getattr(module, param_type)
            else:
                if allow_missing:
                    missing.append(param.name)
                    continue
                raise ValidationError(
                    f"Forward reference '{param_type}' for parameter '{param.name}' could not be resolved",
                    code="RESOLVE_FORWARD_REF_ERROR",
                    class_name=cls.__name__,
                    param_name=param.name,
                    forward_ref=param_type,
                )

        # Try to resolve from registry by type
        # Strategy: Look for registered instance of this type
        instance = registry.get_by_type(param_type)

        if instance is None:
            if allow_missing:
                missing.append(param.name)
                continue
            type_name = getattr(param_type, "__name__", str(param_type))
            raise NotFoundError(
                f"Dependency '{type_name}' required by {cls.__name__} not found in registry",
                code="XXRESOLVE_DEPENDENCY_NOT_FOUNDXX",
                class_name=cls.__name__,
                param_name=param.name,
                param_type=type_name,
            )

        resolved[param.name] = instance

    return resolved


def x_resolve_dependencies__mutmut_108(  # noqa: C901
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
        import sys

        module = sys.modules.get(cls.__module__)
        localns = vars(module) if module else {}
        hints = get_type_hints(cls.__init__, globalns=None, localns=localns)
    except NameError:
        # Forward reference error - collect what we can from annotations
        hints = {}
        sig = inspect.signature(cls.__init__)
        for param_name, param in sig.parameters.items():
            if param_name == "self":
                continue
            if param.annotation != inspect.Parameter.empty:
                # Use the annotation directly (may be a string)
                hints[param_name] = param.annotation
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

        # If param_type is a string (forward reference), try to resolve it
        if isinstance(param_type, str):
            # Look up the type in the class's module
            import sys

            module = sys.modules.get(cls.__module__)
            if module and hasattr(module, param_type):
                param_type = getattr(module, param_type)
            else:
                if allow_missing:
                    missing.append(param.name)
                    continue
                raise ValidationError(
                    f"Forward reference '{param_type}' for parameter '{param.name}' could not be resolved",
                    code="RESOLVE_FORWARD_REF_ERROR",
                    class_name=cls.__name__,
                    param_name=param.name,
                    forward_ref=param_type,
                )

        # Try to resolve from registry by type
        # Strategy: Look for registered instance of this type
        instance = registry.get_by_type(param_type)

        if instance is None:
            if allow_missing:
                missing.append(param.name)
                continue
            type_name = getattr(param_type, "__name__", str(param_type))
            raise NotFoundError(
                f"Dependency '{type_name}' required by {cls.__name__} not found in registry",
                code="resolve_dependency_not_found",
                class_name=cls.__name__,
                param_name=param.name,
                param_type=type_name,
            )

        resolved[param.name] = instance

    return resolved


def x_resolve_dependencies__mutmut_109(  # noqa: C901
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
        import sys

        module = sys.modules.get(cls.__module__)
        localns = vars(module) if module else {}
        hints = get_type_hints(cls.__init__, globalns=None, localns=localns)
    except NameError:
        # Forward reference error - collect what we can from annotations
        hints = {}
        sig = inspect.signature(cls.__init__)
        for param_name, param in sig.parameters.items():
            if param_name == "self":
                continue
            if param.annotation != inspect.Parameter.empty:
                # Use the annotation directly (may be a string)
                hints[param_name] = param.annotation
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

        # If param_type is a string (forward reference), try to resolve it
        if isinstance(param_type, str):
            # Look up the type in the class's module
            import sys

            module = sys.modules.get(cls.__module__)
            if module and hasattr(module, param_type):
                param_type = getattr(module, param_type)
            else:
                if allow_missing:
                    missing.append(param.name)
                    continue
                raise ValidationError(
                    f"Forward reference '{param_type}' for parameter '{param.name}' could not be resolved",
                    code="RESOLVE_FORWARD_REF_ERROR",
                    class_name=cls.__name__,
                    param_name=param.name,
                    forward_ref=param_type,
                )

        # Try to resolve from registry by type
        # Strategy: Look for registered instance of this type
        instance = registry.get_by_type(param_type)

        if instance is None:
            if allow_missing:
                missing.append(param.name)
                continue
            type_name = getattr(param_type, "__name__", str(param_type))
            raise NotFoundError(
                f"Dependency '{type_name}' required by {cls.__name__} not found in registry",
                code="RESOLVE_DEPENDENCY_NOT_FOUND",
                class_name=cls.__name__,
                param_name=param.name,
                param_type=type_name,
            )

        resolved[param.name] = None

    return resolved

x_resolve_dependencies__mutmut_mutants : ClassVar[MutantDict] = {
'x_resolve_dependencies__mutmut_1': x_resolve_dependencies__mutmut_1, 
    'x_resolve_dependencies__mutmut_2': x_resolve_dependencies__mutmut_2, 
    'x_resolve_dependencies__mutmut_3': x_resolve_dependencies__mutmut_3, 
    'x_resolve_dependencies__mutmut_4': x_resolve_dependencies__mutmut_4, 
    'x_resolve_dependencies__mutmut_5': x_resolve_dependencies__mutmut_5, 
    'x_resolve_dependencies__mutmut_6': x_resolve_dependencies__mutmut_6, 
    'x_resolve_dependencies__mutmut_7': x_resolve_dependencies__mutmut_7, 
    'x_resolve_dependencies__mutmut_8': x_resolve_dependencies__mutmut_8, 
    'x_resolve_dependencies__mutmut_9': x_resolve_dependencies__mutmut_9, 
    'x_resolve_dependencies__mutmut_10': x_resolve_dependencies__mutmut_10, 
    'x_resolve_dependencies__mutmut_11': x_resolve_dependencies__mutmut_11, 
    'x_resolve_dependencies__mutmut_12': x_resolve_dependencies__mutmut_12, 
    'x_resolve_dependencies__mutmut_13': x_resolve_dependencies__mutmut_13, 
    'x_resolve_dependencies__mutmut_14': x_resolve_dependencies__mutmut_14, 
    'x_resolve_dependencies__mutmut_15': x_resolve_dependencies__mutmut_15, 
    'x_resolve_dependencies__mutmut_16': x_resolve_dependencies__mutmut_16, 
    'x_resolve_dependencies__mutmut_17': x_resolve_dependencies__mutmut_17, 
    'x_resolve_dependencies__mutmut_18': x_resolve_dependencies__mutmut_18, 
    'x_resolve_dependencies__mutmut_19': x_resolve_dependencies__mutmut_19, 
    'x_resolve_dependencies__mutmut_20': x_resolve_dependencies__mutmut_20, 
    'x_resolve_dependencies__mutmut_21': x_resolve_dependencies__mutmut_21, 
    'x_resolve_dependencies__mutmut_22': x_resolve_dependencies__mutmut_22, 
    'x_resolve_dependencies__mutmut_23': x_resolve_dependencies__mutmut_23, 
    'x_resolve_dependencies__mutmut_24': x_resolve_dependencies__mutmut_24, 
    'x_resolve_dependencies__mutmut_25': x_resolve_dependencies__mutmut_25, 
    'x_resolve_dependencies__mutmut_26': x_resolve_dependencies__mutmut_26, 
    'x_resolve_dependencies__mutmut_27': x_resolve_dependencies__mutmut_27, 
    'x_resolve_dependencies__mutmut_28': x_resolve_dependencies__mutmut_28, 
    'x_resolve_dependencies__mutmut_29': x_resolve_dependencies__mutmut_29, 
    'x_resolve_dependencies__mutmut_30': x_resolve_dependencies__mutmut_30, 
    'x_resolve_dependencies__mutmut_31': x_resolve_dependencies__mutmut_31, 
    'x_resolve_dependencies__mutmut_32': x_resolve_dependencies__mutmut_32, 
    'x_resolve_dependencies__mutmut_33': x_resolve_dependencies__mutmut_33, 
    'x_resolve_dependencies__mutmut_34': x_resolve_dependencies__mutmut_34, 
    'x_resolve_dependencies__mutmut_35': x_resolve_dependencies__mutmut_35, 
    'x_resolve_dependencies__mutmut_36': x_resolve_dependencies__mutmut_36, 
    'x_resolve_dependencies__mutmut_37': x_resolve_dependencies__mutmut_37, 
    'x_resolve_dependencies__mutmut_38': x_resolve_dependencies__mutmut_38, 
    'x_resolve_dependencies__mutmut_39': x_resolve_dependencies__mutmut_39, 
    'x_resolve_dependencies__mutmut_40': x_resolve_dependencies__mutmut_40, 
    'x_resolve_dependencies__mutmut_41': x_resolve_dependencies__mutmut_41, 
    'x_resolve_dependencies__mutmut_42': x_resolve_dependencies__mutmut_42, 
    'x_resolve_dependencies__mutmut_43': x_resolve_dependencies__mutmut_43, 
    'x_resolve_dependencies__mutmut_44': x_resolve_dependencies__mutmut_44, 
    'x_resolve_dependencies__mutmut_45': x_resolve_dependencies__mutmut_45, 
    'x_resolve_dependencies__mutmut_46': x_resolve_dependencies__mutmut_46, 
    'x_resolve_dependencies__mutmut_47': x_resolve_dependencies__mutmut_47, 
    'x_resolve_dependencies__mutmut_48': x_resolve_dependencies__mutmut_48, 
    'x_resolve_dependencies__mutmut_49': x_resolve_dependencies__mutmut_49, 
    'x_resolve_dependencies__mutmut_50': x_resolve_dependencies__mutmut_50, 
    'x_resolve_dependencies__mutmut_51': x_resolve_dependencies__mutmut_51, 
    'x_resolve_dependencies__mutmut_52': x_resolve_dependencies__mutmut_52, 
    'x_resolve_dependencies__mutmut_53': x_resolve_dependencies__mutmut_53, 
    'x_resolve_dependencies__mutmut_54': x_resolve_dependencies__mutmut_54, 
    'x_resolve_dependencies__mutmut_55': x_resolve_dependencies__mutmut_55, 
    'x_resolve_dependencies__mutmut_56': x_resolve_dependencies__mutmut_56, 
    'x_resolve_dependencies__mutmut_57': x_resolve_dependencies__mutmut_57, 
    'x_resolve_dependencies__mutmut_58': x_resolve_dependencies__mutmut_58, 
    'x_resolve_dependencies__mutmut_59': x_resolve_dependencies__mutmut_59, 
    'x_resolve_dependencies__mutmut_60': x_resolve_dependencies__mutmut_60, 
    'x_resolve_dependencies__mutmut_61': x_resolve_dependencies__mutmut_61, 
    'x_resolve_dependencies__mutmut_62': x_resolve_dependencies__mutmut_62, 
    'x_resolve_dependencies__mutmut_63': x_resolve_dependencies__mutmut_63, 
    'x_resolve_dependencies__mutmut_64': x_resolve_dependencies__mutmut_64, 
    'x_resolve_dependencies__mutmut_65': x_resolve_dependencies__mutmut_65, 
    'x_resolve_dependencies__mutmut_66': x_resolve_dependencies__mutmut_66, 
    'x_resolve_dependencies__mutmut_67': x_resolve_dependencies__mutmut_67, 
    'x_resolve_dependencies__mutmut_68': x_resolve_dependencies__mutmut_68, 
    'x_resolve_dependencies__mutmut_69': x_resolve_dependencies__mutmut_69, 
    'x_resolve_dependencies__mutmut_70': x_resolve_dependencies__mutmut_70, 
    'x_resolve_dependencies__mutmut_71': x_resolve_dependencies__mutmut_71, 
    'x_resolve_dependencies__mutmut_72': x_resolve_dependencies__mutmut_72, 
    'x_resolve_dependencies__mutmut_73': x_resolve_dependencies__mutmut_73, 
    'x_resolve_dependencies__mutmut_74': x_resolve_dependencies__mutmut_74, 
    'x_resolve_dependencies__mutmut_75': x_resolve_dependencies__mutmut_75, 
    'x_resolve_dependencies__mutmut_76': x_resolve_dependencies__mutmut_76, 
    'x_resolve_dependencies__mutmut_77': x_resolve_dependencies__mutmut_77, 
    'x_resolve_dependencies__mutmut_78': x_resolve_dependencies__mutmut_78, 
    'x_resolve_dependencies__mutmut_79': x_resolve_dependencies__mutmut_79, 
    'x_resolve_dependencies__mutmut_80': x_resolve_dependencies__mutmut_80, 
    'x_resolve_dependencies__mutmut_81': x_resolve_dependencies__mutmut_81, 
    'x_resolve_dependencies__mutmut_82': x_resolve_dependencies__mutmut_82, 
    'x_resolve_dependencies__mutmut_83': x_resolve_dependencies__mutmut_83, 
    'x_resolve_dependencies__mutmut_84': x_resolve_dependencies__mutmut_84, 
    'x_resolve_dependencies__mutmut_85': x_resolve_dependencies__mutmut_85, 
    'x_resolve_dependencies__mutmut_86': x_resolve_dependencies__mutmut_86, 
    'x_resolve_dependencies__mutmut_87': x_resolve_dependencies__mutmut_87, 
    'x_resolve_dependencies__mutmut_88': x_resolve_dependencies__mutmut_88, 
    'x_resolve_dependencies__mutmut_89': x_resolve_dependencies__mutmut_89, 
    'x_resolve_dependencies__mutmut_90': x_resolve_dependencies__mutmut_90, 
    'x_resolve_dependencies__mutmut_91': x_resolve_dependencies__mutmut_91, 
    'x_resolve_dependencies__mutmut_92': x_resolve_dependencies__mutmut_92, 
    'x_resolve_dependencies__mutmut_93': x_resolve_dependencies__mutmut_93, 
    'x_resolve_dependencies__mutmut_94': x_resolve_dependencies__mutmut_94, 
    'x_resolve_dependencies__mutmut_95': x_resolve_dependencies__mutmut_95, 
    'x_resolve_dependencies__mutmut_96': x_resolve_dependencies__mutmut_96, 
    'x_resolve_dependencies__mutmut_97': x_resolve_dependencies__mutmut_97, 
    'x_resolve_dependencies__mutmut_98': x_resolve_dependencies__mutmut_98, 
    'x_resolve_dependencies__mutmut_99': x_resolve_dependencies__mutmut_99, 
    'x_resolve_dependencies__mutmut_100': x_resolve_dependencies__mutmut_100, 
    'x_resolve_dependencies__mutmut_101': x_resolve_dependencies__mutmut_101, 
    'x_resolve_dependencies__mutmut_102': x_resolve_dependencies__mutmut_102, 
    'x_resolve_dependencies__mutmut_103': x_resolve_dependencies__mutmut_103, 
    'x_resolve_dependencies__mutmut_104': x_resolve_dependencies__mutmut_104, 
    'x_resolve_dependencies__mutmut_105': x_resolve_dependencies__mutmut_105, 
    'x_resolve_dependencies__mutmut_106': x_resolve_dependencies__mutmut_106, 
    'x_resolve_dependencies__mutmut_107': x_resolve_dependencies__mutmut_107, 
    'x_resolve_dependencies__mutmut_108': x_resolve_dependencies__mutmut_108, 
    'x_resolve_dependencies__mutmut_109': x_resolve_dependencies__mutmut_109
}

def resolve_dependencies(*args, **kwargs):
    result = _mutmut_trampoline(x_resolve_dependencies__mutmut_orig, x_resolve_dependencies__mutmut_mutants, args, kwargs)
    return result 

resolve_dependencies.__signature__ = _mutmut_signature(x_resolve_dependencies__mutmut_orig)
x_resolve_dependencies__mutmut_orig.__name__ = 'x_resolve_dependencies'


def x_register__mutmut_orig(
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


def x_register__mutmut_1(
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
    registration_name = None
    registry.register_type(type_hint, instance, name=registration_name)


def x_register__mutmut_2(
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
    registration_name = name and type_hint.__name__
    registry.register_type(type_hint, instance, name=registration_name)


def x_register__mutmut_3(
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
    registry.register_type(None, instance, name=registration_name)


def x_register__mutmut_4(
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
    registry.register_type(type_hint, None, name=registration_name)


def x_register__mutmut_5(
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
    registry.register_type(type_hint, instance, name=None)


def x_register__mutmut_6(
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
    registry.register_type(instance, name=registration_name)


def x_register__mutmut_7(
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
    registry.register_type(type_hint, name=registration_name)


def x_register__mutmut_8(
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
    registry.register_type(type_hint, instance, )

x_register__mutmut_mutants : ClassVar[MutantDict] = {
'x_register__mutmut_1': x_register__mutmut_1, 
    'x_register__mutmut_2': x_register__mutmut_2, 
    'x_register__mutmut_3': x_register__mutmut_3, 
    'x_register__mutmut_4': x_register__mutmut_4, 
    'x_register__mutmut_5': x_register__mutmut_5, 
    'x_register__mutmut_6': x_register__mutmut_6, 
    'x_register__mutmut_7': x_register__mutmut_7, 
    'x_register__mutmut_8': x_register__mutmut_8
}

def register(*args, **kwargs):
    result = _mutmut_trampoline(x_register__mutmut_orig, x_register__mutmut_mutants, args, kwargs)
    return result 

register.__signature__ = _mutmut_signature(x_register__mutmut_orig)
x_register__mutmut_orig.__name__ = 'x_register'


def x_create_instance__mutmut_orig(
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
    # Only allow missing if overrides will provide them
    resolved = resolve_dependencies(cls, registry, allow_missing=False)

    # Apply overrides
    resolved.update(overrides)

    # Create instance
    try:
        return cls(**resolved)
    except (ValidationError, NotFoundError):
        # Re-raise DI-related errors without wrapping
        raise
    except Exception as e:
        raise ValidationError(
            f"Failed to create instance of {cls.__name__}: {e}",
            code="CREATE_INSTANCE_ERROR",
            class_name=cls.__name__,
            cause=e,
        ) from e


def x_create_instance__mutmut_1(
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
    # Only allow missing if overrides will provide them
    resolved = None

    # Apply overrides
    resolved.update(overrides)

    # Create instance
    try:
        return cls(**resolved)
    except (ValidationError, NotFoundError):
        # Re-raise DI-related errors without wrapping
        raise
    except Exception as e:
        raise ValidationError(
            f"Failed to create instance of {cls.__name__}: {e}",
            code="CREATE_INSTANCE_ERROR",
            class_name=cls.__name__,
            cause=e,
        ) from e


def x_create_instance__mutmut_2(
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
    # Only allow missing if overrides will provide them
    resolved = resolve_dependencies(None, registry, allow_missing=False)

    # Apply overrides
    resolved.update(overrides)

    # Create instance
    try:
        return cls(**resolved)
    except (ValidationError, NotFoundError):
        # Re-raise DI-related errors without wrapping
        raise
    except Exception as e:
        raise ValidationError(
            f"Failed to create instance of {cls.__name__}: {e}",
            code="CREATE_INSTANCE_ERROR",
            class_name=cls.__name__,
            cause=e,
        ) from e


def x_create_instance__mutmut_3(
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
    # Only allow missing if overrides will provide them
    resolved = resolve_dependencies(cls, None, allow_missing=False)

    # Apply overrides
    resolved.update(overrides)

    # Create instance
    try:
        return cls(**resolved)
    except (ValidationError, NotFoundError):
        # Re-raise DI-related errors without wrapping
        raise
    except Exception as e:
        raise ValidationError(
            f"Failed to create instance of {cls.__name__}: {e}",
            code="CREATE_INSTANCE_ERROR",
            class_name=cls.__name__,
            cause=e,
        ) from e


def x_create_instance__mutmut_4(
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
    # Only allow missing if overrides will provide them
    resolved = resolve_dependencies(cls, registry, allow_missing=None)

    # Apply overrides
    resolved.update(overrides)

    # Create instance
    try:
        return cls(**resolved)
    except (ValidationError, NotFoundError):
        # Re-raise DI-related errors without wrapping
        raise
    except Exception as e:
        raise ValidationError(
            f"Failed to create instance of {cls.__name__}: {e}",
            code="CREATE_INSTANCE_ERROR",
            class_name=cls.__name__,
            cause=e,
        ) from e


def x_create_instance__mutmut_5(
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
    # Only allow missing if overrides will provide them
    resolved = resolve_dependencies(registry, allow_missing=False)

    # Apply overrides
    resolved.update(overrides)

    # Create instance
    try:
        return cls(**resolved)
    except (ValidationError, NotFoundError):
        # Re-raise DI-related errors without wrapping
        raise
    except Exception as e:
        raise ValidationError(
            f"Failed to create instance of {cls.__name__}: {e}",
            code="CREATE_INSTANCE_ERROR",
            class_name=cls.__name__,
            cause=e,
        ) from e


def x_create_instance__mutmut_6(
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
    # Only allow missing if overrides will provide them
    resolved = resolve_dependencies(cls, allow_missing=False)

    # Apply overrides
    resolved.update(overrides)

    # Create instance
    try:
        return cls(**resolved)
    except (ValidationError, NotFoundError):
        # Re-raise DI-related errors without wrapping
        raise
    except Exception as e:
        raise ValidationError(
            f"Failed to create instance of {cls.__name__}: {e}",
            code="CREATE_INSTANCE_ERROR",
            class_name=cls.__name__,
            cause=e,
        ) from e


def x_create_instance__mutmut_7(
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
    # Only allow missing if overrides will provide them
    resolved = resolve_dependencies(cls, registry, )

    # Apply overrides
    resolved.update(overrides)

    # Create instance
    try:
        return cls(**resolved)
    except (ValidationError, NotFoundError):
        # Re-raise DI-related errors without wrapping
        raise
    except Exception as e:
        raise ValidationError(
            f"Failed to create instance of {cls.__name__}: {e}",
            code="CREATE_INSTANCE_ERROR",
            class_name=cls.__name__,
            cause=e,
        ) from e


def x_create_instance__mutmut_8(
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
    # Only allow missing if overrides will provide them
    resolved = resolve_dependencies(cls, registry, allow_missing=True)

    # Apply overrides
    resolved.update(overrides)

    # Create instance
    try:
        return cls(**resolved)
    except (ValidationError, NotFoundError):
        # Re-raise DI-related errors without wrapping
        raise
    except Exception as e:
        raise ValidationError(
            f"Failed to create instance of {cls.__name__}: {e}",
            code="CREATE_INSTANCE_ERROR",
            class_name=cls.__name__,
            cause=e,
        ) from e


def x_create_instance__mutmut_9(
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
    # Only allow missing if overrides will provide them
    resolved = resolve_dependencies(cls, registry, allow_missing=False)

    # Apply overrides
    resolved.update(None)

    # Create instance
    try:
        return cls(**resolved)
    except (ValidationError, NotFoundError):
        # Re-raise DI-related errors without wrapping
        raise
    except Exception as e:
        raise ValidationError(
            f"Failed to create instance of {cls.__name__}: {e}",
            code="CREATE_INSTANCE_ERROR",
            class_name=cls.__name__,
            cause=e,
        ) from e


def x_create_instance__mutmut_10(
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
    # Only allow missing if overrides will provide them
    resolved = resolve_dependencies(cls, registry, allow_missing=False)

    # Apply overrides
    resolved.update(overrides)

    # Create instance
    try:
        return cls(**resolved)
    except (ValidationError, NotFoundError):
        # Re-raise DI-related errors without wrapping
        raise
    except Exception as e:
        raise ValidationError(
            None,
            code="CREATE_INSTANCE_ERROR",
            class_name=cls.__name__,
            cause=e,
        ) from e


def x_create_instance__mutmut_11(
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
    # Only allow missing if overrides will provide them
    resolved = resolve_dependencies(cls, registry, allow_missing=False)

    # Apply overrides
    resolved.update(overrides)

    # Create instance
    try:
        return cls(**resolved)
    except (ValidationError, NotFoundError):
        # Re-raise DI-related errors without wrapping
        raise
    except Exception as e:
        raise ValidationError(
            f"Failed to create instance of {cls.__name__}: {e}",
            code=None,
            class_name=cls.__name__,
            cause=e,
        ) from e


def x_create_instance__mutmut_12(
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
    # Only allow missing if overrides will provide them
    resolved = resolve_dependencies(cls, registry, allow_missing=False)

    # Apply overrides
    resolved.update(overrides)

    # Create instance
    try:
        return cls(**resolved)
    except (ValidationError, NotFoundError):
        # Re-raise DI-related errors without wrapping
        raise
    except Exception as e:
        raise ValidationError(
            f"Failed to create instance of {cls.__name__}: {e}",
            code="CREATE_INSTANCE_ERROR",
            class_name=None,
            cause=e,
        ) from e


def x_create_instance__mutmut_13(
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
    # Only allow missing if overrides will provide them
    resolved = resolve_dependencies(cls, registry, allow_missing=False)

    # Apply overrides
    resolved.update(overrides)

    # Create instance
    try:
        return cls(**resolved)
    except (ValidationError, NotFoundError):
        # Re-raise DI-related errors without wrapping
        raise
    except Exception as e:
        raise ValidationError(
            f"Failed to create instance of {cls.__name__}: {e}",
            code="CREATE_INSTANCE_ERROR",
            class_name=cls.__name__,
            cause=None,
        ) from e


def x_create_instance__mutmut_14(
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
    # Only allow missing if overrides will provide them
    resolved = resolve_dependencies(cls, registry, allow_missing=False)

    # Apply overrides
    resolved.update(overrides)

    # Create instance
    try:
        return cls(**resolved)
    except (ValidationError, NotFoundError):
        # Re-raise DI-related errors without wrapping
        raise
    except Exception as e:
        raise ValidationError(
            code="CREATE_INSTANCE_ERROR",
            class_name=cls.__name__,
            cause=e,
        ) from e


def x_create_instance__mutmut_15(
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
    # Only allow missing if overrides will provide them
    resolved = resolve_dependencies(cls, registry, allow_missing=False)

    # Apply overrides
    resolved.update(overrides)

    # Create instance
    try:
        return cls(**resolved)
    except (ValidationError, NotFoundError):
        # Re-raise DI-related errors without wrapping
        raise
    except Exception as e:
        raise ValidationError(
            f"Failed to create instance of {cls.__name__}: {e}",
            class_name=cls.__name__,
            cause=e,
        ) from e


def x_create_instance__mutmut_16(
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
    # Only allow missing if overrides will provide them
    resolved = resolve_dependencies(cls, registry, allow_missing=False)

    # Apply overrides
    resolved.update(overrides)

    # Create instance
    try:
        return cls(**resolved)
    except (ValidationError, NotFoundError):
        # Re-raise DI-related errors without wrapping
        raise
    except Exception as e:
        raise ValidationError(
            f"Failed to create instance of {cls.__name__}: {e}",
            code="CREATE_INSTANCE_ERROR",
            cause=e,
        ) from e


def x_create_instance__mutmut_17(
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
    # Only allow missing if overrides will provide them
    resolved = resolve_dependencies(cls, registry, allow_missing=False)

    # Apply overrides
    resolved.update(overrides)

    # Create instance
    try:
        return cls(**resolved)
    except (ValidationError, NotFoundError):
        # Re-raise DI-related errors without wrapping
        raise
    except Exception as e:
        raise ValidationError(
            f"Failed to create instance of {cls.__name__}: {e}",
            code="CREATE_INSTANCE_ERROR",
            class_name=cls.__name__,
            ) from e


def x_create_instance__mutmut_18(
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
    # Only allow missing if overrides will provide them
    resolved = resolve_dependencies(cls, registry, allow_missing=False)

    # Apply overrides
    resolved.update(overrides)

    # Create instance
    try:
        return cls(**resolved)
    except (ValidationError, NotFoundError):
        # Re-raise DI-related errors without wrapping
        raise
    except Exception as e:
        raise ValidationError(
            f"Failed to create instance of {cls.__name__}: {e}",
            code="XXCREATE_INSTANCE_ERRORXX",
            class_name=cls.__name__,
            cause=e,
        ) from e


def x_create_instance__mutmut_19(
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
    # Only allow missing if overrides will provide them
    resolved = resolve_dependencies(cls, registry, allow_missing=False)

    # Apply overrides
    resolved.update(overrides)

    # Create instance
    try:
        return cls(**resolved)
    except (ValidationError, NotFoundError):
        # Re-raise DI-related errors without wrapping
        raise
    except Exception as e:
        raise ValidationError(
            f"Failed to create instance of {cls.__name__}: {e}",
            code="create_instance_error",
            class_name=cls.__name__,
            cause=e,
        ) from e

x_create_instance__mutmut_mutants : ClassVar[MutantDict] = {
'x_create_instance__mutmut_1': x_create_instance__mutmut_1, 
    'x_create_instance__mutmut_2': x_create_instance__mutmut_2, 
    'x_create_instance__mutmut_3': x_create_instance__mutmut_3, 
    'x_create_instance__mutmut_4': x_create_instance__mutmut_4, 
    'x_create_instance__mutmut_5': x_create_instance__mutmut_5, 
    'x_create_instance__mutmut_6': x_create_instance__mutmut_6, 
    'x_create_instance__mutmut_7': x_create_instance__mutmut_7, 
    'x_create_instance__mutmut_8': x_create_instance__mutmut_8, 
    'x_create_instance__mutmut_9': x_create_instance__mutmut_9, 
    'x_create_instance__mutmut_10': x_create_instance__mutmut_10, 
    'x_create_instance__mutmut_11': x_create_instance__mutmut_11, 
    'x_create_instance__mutmut_12': x_create_instance__mutmut_12, 
    'x_create_instance__mutmut_13': x_create_instance__mutmut_13, 
    'x_create_instance__mutmut_14': x_create_instance__mutmut_14, 
    'x_create_instance__mutmut_15': x_create_instance__mutmut_15, 
    'x_create_instance__mutmut_16': x_create_instance__mutmut_16, 
    'x_create_instance__mutmut_17': x_create_instance__mutmut_17, 
    'x_create_instance__mutmut_18': x_create_instance__mutmut_18, 
    'x_create_instance__mutmut_19': x_create_instance__mutmut_19
}

def create_instance(*args, **kwargs):
    result = _mutmut_trampoline(x_create_instance__mutmut_orig, x_create_instance__mutmut_mutants, args, kwargs)
    return result 

create_instance.__signature__ = _mutmut_signature(x_create_instance__mutmut_orig)
x_create_instance__mutmut_orig.__name__ = 'x_create_instance'


__all__ = [
    "create_instance",
    "injectable",
    "is_injectable",
    "register",
    "resolve_dependencies",
]


# <3 🧱🤝🌐🪄
