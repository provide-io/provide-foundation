# provide/foundation/hub/decorators.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from collections.abc import Callable
from typing import TYPE_CHECKING, Any, TypeVar, overload

from provide.foundation.hub.categories import ComponentCategory
from provide.foundation.hub.foundation import get_foundation_logger
from provide.foundation.hub.info import CommandInfo
from provide.foundation.hub.registry import Registry, get_command_registry

"""Command registration decorators."""

# Lazy import to avoid circular dependency
if TYPE_CHECKING:
    pass

# Import click lazily to avoid circular imports
_click_module: Any = None
_HAS_CLICK: bool | None = None
from inspect import signature as _mutmut_signature
from typing import Annotated
from typing import Callable
from typing import ClassVar


MutantDict = Annotated[dict[str, Callable], "Mutant"]


def _mutmut_trampoline(orig, mutants, call_args, call_kwargs, self_arg=None):
    """Forward call to original or mutated function, depending on the environment"""
    import os

    mutant_under_test = os.environ["MUTANT_UNDER_TEST"]
    if mutant_under_test == "fail":
        from mutmut.__main__ import MutmutProgrammaticFailException

        raise MutmutProgrammaticFailException("Failed programmatically")
    elif mutant_under_test == "stats":
        from mutmut.__main__ import record_trampoline_hit

        record_trampoline_hit(orig.__module__ + "." + orig.__name__)
        result = orig(*call_args, **call_kwargs)
        return result
    prefix = orig.__module__ + "." + orig.__name__ + "__mutmut_"
    if not mutant_under_test.startswith(prefix):
        result = orig(*call_args, **call_kwargs)
        return result
    mutant_name = mutant_under_test.rpartition(".")[-1]
    if self_arg:
        # call to a class method where self is not bound
        result = mutants[mutant_name](self_arg, *call_args, **call_kwargs)
    else:
        result = mutants[mutant_name](*call_args, **call_kwargs)
    return result


def x__get_click__mutmut_orig() -> tuple[Any, bool]:
    """Get click module and availability flag."""
    global _click_module, _HAS_CLICK
    if _HAS_CLICK is None:
        from provide.foundation.cli.deps import _HAS_CLICK as has_click, click

        _click_module = click
        _HAS_CLICK = has_click
    return _click_module, _HAS_CLICK


def x__get_click__mutmut_1() -> tuple[Any, bool]:
    """Get click module and availability flag."""
    global _click_module, _HAS_CLICK
    if _HAS_CLICK is not None:
        from provide.foundation.cli.deps import _HAS_CLICK as has_click, click

        _click_module = click
        _HAS_CLICK = has_click
    return _click_module, _HAS_CLICK


def x__get_click__mutmut_2() -> tuple[Any, bool]:
    """Get click module and availability flag."""
    global _click_module, _HAS_CLICK
    if _HAS_CLICK is None:
        from provide.foundation.cli.deps import _HAS_CLICK as has_click, click

        _click_module = None
        _HAS_CLICK = has_click
    return _click_module, _HAS_CLICK


def x__get_click__mutmut_3() -> tuple[Any, bool]:
    """Get click module and availability flag."""
    global _click_module, _HAS_CLICK
    if _HAS_CLICK is None:
        from provide.foundation.cli.deps import _HAS_CLICK as has_click, click

        _click_module = click
        _HAS_CLICK = None
    return _click_module, _HAS_CLICK


x__get_click__mutmut_mutants: ClassVar[MutantDict] = {
    "x__get_click__mutmut_1": x__get_click__mutmut_1,
    "x__get_click__mutmut_2": x__get_click__mutmut_2,
    "x__get_click__mutmut_3": x__get_click__mutmut_3,
}


def _get_click(*args, **kwargs):
    result = _mutmut_trampoline(x__get_click__mutmut_orig, x__get_click__mutmut_mutants, args, kwargs)
    return result


_get_click.__signature__ = _mutmut_signature(x__get_click__mutmut_orig)
x__get_click__mutmut_orig.__name__ = "x__get_click"


# Defer click hierarchy import to avoid circular dependency
def x__get_ensure_parent_groups__mutmut_orig() -> Any:
    _, has_click = _get_click()
    if not has_click:
        return None
    from provide.foundation.cli.click.hierarchy import ensure_parent_groups

    return ensure_parent_groups


# Defer click hierarchy import to avoid circular dependency
def x__get_ensure_parent_groups__mutmut_1() -> Any:
    _, has_click = None
    if not has_click:
        return None
    from provide.foundation.cli.click.hierarchy import ensure_parent_groups

    return ensure_parent_groups


# Defer click hierarchy import to avoid circular dependency
def x__get_ensure_parent_groups__mutmut_2() -> Any:
    _, has_click = _get_click()
    if has_click:
        return None
    from provide.foundation.cli.click.hierarchy import ensure_parent_groups

    return ensure_parent_groups


x__get_ensure_parent_groups__mutmut_mutants: ClassVar[MutantDict] = {
    "x__get_ensure_parent_groups__mutmut_1": x__get_ensure_parent_groups__mutmut_1,
    "x__get_ensure_parent_groups__mutmut_2": x__get_ensure_parent_groups__mutmut_2,
}


def _get_ensure_parent_groups(*args, **kwargs):
    result = _mutmut_trampoline(
        x__get_ensure_parent_groups__mutmut_orig, x__get_ensure_parent_groups__mutmut_mutants, args, kwargs
    )
    return result


_get_ensure_parent_groups.__signature__ = _mutmut_signature(x__get_ensure_parent_groups__mutmut_orig)
x__get_ensure_parent_groups__mutmut_orig.__name__ = "x__get_ensure_parent_groups"


F = TypeVar("F", bound=Callable[..., Any])


@overload
def register_command(
    name: str | None = None,
    *,
    description: str | None = None,
    aliases: list[str] | None = None,
    hidden: bool = False,
    category: str | None = None,
    group: bool = False,
    replace: bool = False,
    registry: Registry | None = None,
    **metadata: Any,
) -> Callable[[F], F]: ...


@overload
def register_command(
    func: F,
    /,
) -> F: ...


def x_register_command__mutmut_orig(  # type: ignore[misc]
    name_or_func: str | F | None = None,
    *,
    description: str | None = None,
    aliases: list[str] | None = None,
    hidden: bool = False,
    category: str | None = None,
    group: bool = False,
    replace: bool = False,
    registry: Registry | None = None,
    **metadata: Any,
) -> Any:
    """Register a CLI command in the hub.

    Can be used as a decorator with or without arguments:

        @register_command
        def my_command():
            pass

        @register_command("custom-name", aliases=["cn"], category="utils")
        def my_command():
            pass

        # Nested commands using dot notation - groups are auto-created
        @register_command("container.status")
        def container_status():
            pass

        @register_command("container.volumes.backup")
        def container_volumes_backup():
            pass

        # Explicit group with custom description (optional)
        @register_command("container", group=True, description="Container management")
        def container_group():
            pass

    Args:
        name_or_func: Command name using dot notation for nesting (e.g., "container.status")
        description: Command description (defaults to docstring)
        aliases: Alternative names for the command
        hidden: Whether to hide from help listing
        category: Command category for grouping
        group: Whether this is a command group (not a command)
        replace: Whether to replace existing registration
        force_options: If True, all parameters with defaults become --options
                      (disables Position-Based Hybrid for first parameter)
        registry: Custom registry (defaults to global)
        **metadata: Additional metadata stored in CommandInfo.metadata

    Returns:
        Decorator function or decorated function

    """
    # Handle @register_command (without parens)
    if callable(name_or_func) and not isinstance(name_or_func, str):
        func = name_or_func
        return _register_command_func(
            func,
            name=None,
            description=description,
            aliases=aliases,
            hidden=hidden,
            category=category,
            group=group,
            replace=replace,
            registry=registry,
            **metadata,
        )

    # Handle @register_command(...) (with arguments)
    # At this point, name_or_func must be str | None (not F)
    name_str: str | None = name_or_func if isinstance(name_or_func, str) or name_or_func is None else None

    def decorator(func: F) -> F:
        return _register_command_func(
            func,
            name=name_str,
            description=description,
            aliases=aliases,
            hidden=hidden,
            category=category,
            group=group,
            replace=replace,
            registry=registry,
            **metadata,
        )

    return decorator


def x_register_command__mutmut_1(  # type: ignore[misc]
    name_or_func: str | F | None = None,
    *,
    description: str | None = None,
    aliases: list[str] | None = None,
    hidden: bool = True,
    category: str | None = None,
    group: bool = False,
    replace: bool = False,
    registry: Registry | None = None,
    **metadata: Any,
) -> Any:
    """Register a CLI command in the hub.

    Can be used as a decorator with or without arguments:

        @register_command
        def my_command():
            pass

        @register_command("custom-name", aliases=["cn"], category="utils")
        def my_command():
            pass

        # Nested commands using dot notation - groups are auto-created
        @register_command("container.status")
        def container_status():
            pass

        @register_command("container.volumes.backup")
        def container_volumes_backup():
            pass

        # Explicit group with custom description (optional)
        @register_command("container", group=True, description="Container management")
        def container_group():
            pass

    Args:
        name_or_func: Command name using dot notation for nesting (e.g., "container.status")
        description: Command description (defaults to docstring)
        aliases: Alternative names for the command
        hidden: Whether to hide from help listing
        category: Command category for grouping
        group: Whether this is a command group (not a command)
        replace: Whether to replace existing registration
        force_options: If True, all parameters with defaults become --options
                      (disables Position-Based Hybrid for first parameter)
        registry: Custom registry (defaults to global)
        **metadata: Additional metadata stored in CommandInfo.metadata

    Returns:
        Decorator function or decorated function

    """
    # Handle @register_command (without parens)
    if callable(name_or_func) and not isinstance(name_or_func, str):
        func = name_or_func
        return _register_command_func(
            func,
            name=None,
            description=description,
            aliases=aliases,
            hidden=hidden,
            category=category,
            group=group,
            replace=replace,
            registry=registry,
            **metadata,
        )

    # Handle @register_command(...) (with arguments)
    # At this point, name_or_func must be str | None (not F)
    name_str: str | None = name_or_func if isinstance(name_or_func, str) or name_or_func is None else None

    def decorator(func: F) -> F:
        return _register_command_func(
            func,
            name=name_str,
            description=description,
            aliases=aliases,
            hidden=hidden,
            category=category,
            group=group,
            replace=replace,
            registry=registry,
            **metadata,
        )

    return decorator


def x_register_command__mutmut_2(  # type: ignore[misc]
    name_or_func: str | F | None = None,
    *,
    description: str | None = None,
    aliases: list[str] | None = None,
    hidden: bool = False,
    category: str | None = None,
    group: bool = True,
    replace: bool = False,
    registry: Registry | None = None,
    **metadata: Any,
) -> Any:
    """Register a CLI command in the hub.

    Can be used as a decorator with or without arguments:

        @register_command
        def my_command():
            pass

        @register_command("custom-name", aliases=["cn"], category="utils")
        def my_command():
            pass

        # Nested commands using dot notation - groups are auto-created
        @register_command("container.status")
        def container_status():
            pass

        @register_command("container.volumes.backup")
        def container_volumes_backup():
            pass

        # Explicit group with custom description (optional)
        @register_command("container", group=True, description="Container management")
        def container_group():
            pass

    Args:
        name_or_func: Command name using dot notation for nesting (e.g., "container.status")
        description: Command description (defaults to docstring)
        aliases: Alternative names for the command
        hidden: Whether to hide from help listing
        category: Command category for grouping
        group: Whether this is a command group (not a command)
        replace: Whether to replace existing registration
        force_options: If True, all parameters with defaults become --options
                      (disables Position-Based Hybrid for first parameter)
        registry: Custom registry (defaults to global)
        **metadata: Additional metadata stored in CommandInfo.metadata

    Returns:
        Decorator function or decorated function

    """
    # Handle @register_command (without parens)
    if callable(name_or_func) and not isinstance(name_or_func, str):
        func = name_or_func
        return _register_command_func(
            func,
            name=None,
            description=description,
            aliases=aliases,
            hidden=hidden,
            category=category,
            group=group,
            replace=replace,
            registry=registry,
            **metadata,
        )

    # Handle @register_command(...) (with arguments)
    # At this point, name_or_func must be str | None (not F)
    name_str: str | None = name_or_func if isinstance(name_or_func, str) or name_or_func is None else None

    def decorator(func: F) -> F:
        return _register_command_func(
            func,
            name=name_str,
            description=description,
            aliases=aliases,
            hidden=hidden,
            category=category,
            group=group,
            replace=replace,
            registry=registry,
            **metadata,
        )

    return decorator


def x_register_command__mutmut_3(  # type: ignore[misc]
    name_or_func: str | F | None = None,
    *,
    description: str | None = None,
    aliases: list[str] | None = None,
    hidden: bool = False,
    category: str | None = None,
    group: bool = False,
    replace: bool = True,
    registry: Registry | None = None,
    **metadata: Any,
) -> Any:
    """Register a CLI command in the hub.

    Can be used as a decorator with or without arguments:

        @register_command
        def my_command():
            pass

        @register_command("custom-name", aliases=["cn"], category="utils")
        def my_command():
            pass

        # Nested commands using dot notation - groups are auto-created
        @register_command("container.status")
        def container_status():
            pass

        @register_command("container.volumes.backup")
        def container_volumes_backup():
            pass

        # Explicit group with custom description (optional)
        @register_command("container", group=True, description="Container management")
        def container_group():
            pass

    Args:
        name_or_func: Command name using dot notation for nesting (e.g., "container.status")
        description: Command description (defaults to docstring)
        aliases: Alternative names for the command
        hidden: Whether to hide from help listing
        category: Command category for grouping
        group: Whether this is a command group (not a command)
        replace: Whether to replace existing registration
        force_options: If True, all parameters with defaults become --options
                      (disables Position-Based Hybrid for first parameter)
        registry: Custom registry (defaults to global)
        **metadata: Additional metadata stored in CommandInfo.metadata

    Returns:
        Decorator function or decorated function

    """
    # Handle @register_command (without parens)
    if callable(name_or_func) and not isinstance(name_or_func, str):
        func = name_or_func
        return _register_command_func(
            func,
            name=None,
            description=description,
            aliases=aliases,
            hidden=hidden,
            category=category,
            group=group,
            replace=replace,
            registry=registry,
            **metadata,
        )

    # Handle @register_command(...) (with arguments)
    # At this point, name_or_func must be str | None (not F)
    name_str: str | None = name_or_func if isinstance(name_or_func, str) or name_or_func is None else None

    def decorator(func: F) -> F:
        return _register_command_func(
            func,
            name=name_str,
            description=description,
            aliases=aliases,
            hidden=hidden,
            category=category,
            group=group,
            replace=replace,
            registry=registry,
            **metadata,
        )

    return decorator


def x_register_command__mutmut_4(  # type: ignore[misc]
    name_or_func: str | F | None = None,
    *,
    description: str | None = None,
    aliases: list[str] | None = None,
    hidden: bool = False,
    category: str | None = None,
    group: bool = False,
    replace: bool = False,
    registry: Registry | None = None,
    **metadata: Any,
) -> Any:
    """Register a CLI command in the hub.

    Can be used as a decorator with or without arguments:

        @register_command
        def my_command():
            pass

        @register_command("custom-name", aliases=["cn"], category="utils")
        def my_command():
            pass

        # Nested commands using dot notation - groups are auto-created
        @register_command("container.status")
        def container_status():
            pass

        @register_command("container.volumes.backup")
        def container_volumes_backup():
            pass

        # Explicit group with custom description (optional)
        @register_command("container", group=True, description="Container management")
        def container_group():
            pass

    Args:
        name_or_func: Command name using dot notation for nesting (e.g., "container.status")
        description: Command description (defaults to docstring)
        aliases: Alternative names for the command
        hidden: Whether to hide from help listing
        category: Command category for grouping
        group: Whether this is a command group (not a command)
        replace: Whether to replace existing registration
        force_options: If True, all parameters with defaults become --options
                      (disables Position-Based Hybrid for first parameter)
        registry: Custom registry (defaults to global)
        **metadata: Additional metadata stored in CommandInfo.metadata

    Returns:
        Decorator function or decorated function

    """
    # Handle @register_command (without parens)
    if callable(name_or_func) or not isinstance(name_or_func, str):
        func = name_or_func
        return _register_command_func(
            func,
            name=None,
            description=description,
            aliases=aliases,
            hidden=hidden,
            category=category,
            group=group,
            replace=replace,
            registry=registry,
            **metadata,
        )

    # Handle @register_command(...) (with arguments)
    # At this point, name_or_func must be str | None (not F)
    name_str: str | None = name_or_func if isinstance(name_or_func, str) or name_or_func is None else None

    def decorator(func: F) -> F:
        return _register_command_func(
            func,
            name=name_str,
            description=description,
            aliases=aliases,
            hidden=hidden,
            category=category,
            group=group,
            replace=replace,
            registry=registry,
            **metadata,
        )

    return decorator


def x_register_command__mutmut_5(  # type: ignore[misc]
    name_or_func: str | F | None = None,
    *,
    description: str | None = None,
    aliases: list[str] | None = None,
    hidden: bool = False,
    category: str | None = None,
    group: bool = False,
    replace: bool = False,
    registry: Registry | None = None,
    **metadata: Any,
) -> Any:
    """Register a CLI command in the hub.

    Can be used as a decorator with or without arguments:

        @register_command
        def my_command():
            pass

        @register_command("custom-name", aliases=["cn"], category="utils")
        def my_command():
            pass

        # Nested commands using dot notation - groups are auto-created
        @register_command("container.status")
        def container_status():
            pass

        @register_command("container.volumes.backup")
        def container_volumes_backup():
            pass

        # Explicit group with custom description (optional)
        @register_command("container", group=True, description="Container management")
        def container_group():
            pass

    Args:
        name_or_func: Command name using dot notation for nesting (e.g., "container.status")
        description: Command description (defaults to docstring)
        aliases: Alternative names for the command
        hidden: Whether to hide from help listing
        category: Command category for grouping
        group: Whether this is a command group (not a command)
        replace: Whether to replace existing registration
        force_options: If True, all parameters with defaults become --options
                      (disables Position-Based Hybrid for first parameter)
        registry: Custom registry (defaults to global)
        **metadata: Additional metadata stored in CommandInfo.metadata

    Returns:
        Decorator function or decorated function

    """
    # Handle @register_command (without parens)
    if callable(None) and not isinstance(name_or_func, str):
        func = name_or_func
        return _register_command_func(
            func,
            name=None,
            description=description,
            aliases=aliases,
            hidden=hidden,
            category=category,
            group=group,
            replace=replace,
            registry=registry,
            **metadata,
        )

    # Handle @register_command(...) (with arguments)
    # At this point, name_or_func must be str | None (not F)
    name_str: str | None = name_or_func if isinstance(name_or_func, str) or name_or_func is None else None

    def decorator(func: F) -> F:
        return _register_command_func(
            func,
            name=name_str,
            description=description,
            aliases=aliases,
            hidden=hidden,
            category=category,
            group=group,
            replace=replace,
            registry=registry,
            **metadata,
        )

    return decorator


def x_register_command__mutmut_6(  # type: ignore[misc]
    name_or_func: str | F | None = None,
    *,
    description: str | None = None,
    aliases: list[str] | None = None,
    hidden: bool = False,
    category: str | None = None,
    group: bool = False,
    replace: bool = False,
    registry: Registry | None = None,
    **metadata: Any,
) -> Any:
    """Register a CLI command in the hub.

    Can be used as a decorator with or without arguments:

        @register_command
        def my_command():
            pass

        @register_command("custom-name", aliases=["cn"], category="utils")
        def my_command():
            pass

        # Nested commands using dot notation - groups are auto-created
        @register_command("container.status")
        def container_status():
            pass

        @register_command("container.volumes.backup")
        def container_volumes_backup():
            pass

        # Explicit group with custom description (optional)
        @register_command("container", group=True, description="Container management")
        def container_group():
            pass

    Args:
        name_or_func: Command name using dot notation for nesting (e.g., "container.status")
        description: Command description (defaults to docstring)
        aliases: Alternative names for the command
        hidden: Whether to hide from help listing
        category: Command category for grouping
        group: Whether this is a command group (not a command)
        replace: Whether to replace existing registration
        force_options: If True, all parameters with defaults become --options
                      (disables Position-Based Hybrid for first parameter)
        registry: Custom registry (defaults to global)
        **metadata: Additional metadata stored in CommandInfo.metadata

    Returns:
        Decorator function or decorated function

    """
    # Handle @register_command (without parens)
    if callable(name_or_func) and isinstance(name_or_func, str):
        func = name_or_func
        return _register_command_func(
            func,
            name=None,
            description=description,
            aliases=aliases,
            hidden=hidden,
            category=category,
            group=group,
            replace=replace,
            registry=registry,
            **metadata,
        )

    # Handle @register_command(...) (with arguments)
    # At this point, name_or_func must be str | None (not F)
    name_str: str | None = name_or_func if isinstance(name_or_func, str) or name_or_func is None else None

    def decorator(func: F) -> F:
        return _register_command_func(
            func,
            name=name_str,
            description=description,
            aliases=aliases,
            hidden=hidden,
            category=category,
            group=group,
            replace=replace,
            registry=registry,
            **metadata,
        )

    return decorator


def x_register_command__mutmut_7(  # type: ignore[misc]
    name_or_func: str | F | None = None,
    *,
    description: str | None = None,
    aliases: list[str] | None = None,
    hidden: bool = False,
    category: str | None = None,
    group: bool = False,
    replace: bool = False,
    registry: Registry | None = None,
    **metadata: Any,
) -> Any:
    """Register a CLI command in the hub.

    Can be used as a decorator with or without arguments:

        @register_command
        def my_command():
            pass

        @register_command("custom-name", aliases=["cn"], category="utils")
        def my_command():
            pass

        # Nested commands using dot notation - groups are auto-created
        @register_command("container.status")
        def container_status():
            pass

        @register_command("container.volumes.backup")
        def container_volumes_backup():
            pass

        # Explicit group with custom description (optional)
        @register_command("container", group=True, description="Container management")
        def container_group():
            pass

    Args:
        name_or_func: Command name using dot notation for nesting (e.g., "container.status")
        description: Command description (defaults to docstring)
        aliases: Alternative names for the command
        hidden: Whether to hide from help listing
        category: Command category for grouping
        group: Whether this is a command group (not a command)
        replace: Whether to replace existing registration
        force_options: If True, all parameters with defaults become --options
                      (disables Position-Based Hybrid for first parameter)
        registry: Custom registry (defaults to global)
        **metadata: Additional metadata stored in CommandInfo.metadata

    Returns:
        Decorator function or decorated function

    """
    # Handle @register_command (without parens)
    if callable(name_or_func) and not isinstance(name_or_func, str):
        func = None
        return _register_command_func(
            func,
            name=None,
            description=description,
            aliases=aliases,
            hidden=hidden,
            category=category,
            group=group,
            replace=replace,
            registry=registry,
            **metadata,
        )

    # Handle @register_command(...) (with arguments)
    # At this point, name_or_func must be str | None (not F)
    name_str: str | None = name_or_func if isinstance(name_or_func, str) or name_or_func is None else None

    def decorator(func: F) -> F:
        return _register_command_func(
            func,
            name=name_str,
            description=description,
            aliases=aliases,
            hidden=hidden,
            category=category,
            group=group,
            replace=replace,
            registry=registry,
            **metadata,
        )

    return decorator


def x_register_command__mutmut_8(  # type: ignore[misc]
    name_or_func: str | F | None = None,
    *,
    description: str | None = None,
    aliases: list[str] | None = None,
    hidden: bool = False,
    category: str | None = None,
    group: bool = False,
    replace: bool = False,
    registry: Registry | None = None,
    **metadata: Any,
) -> Any:
    """Register a CLI command in the hub.

    Can be used as a decorator with or without arguments:

        @register_command
        def my_command():
            pass

        @register_command("custom-name", aliases=["cn"], category="utils")
        def my_command():
            pass

        # Nested commands using dot notation - groups are auto-created
        @register_command("container.status")
        def container_status():
            pass

        @register_command("container.volumes.backup")
        def container_volumes_backup():
            pass

        # Explicit group with custom description (optional)
        @register_command("container", group=True, description="Container management")
        def container_group():
            pass

    Args:
        name_or_func: Command name using dot notation for nesting (e.g., "container.status")
        description: Command description (defaults to docstring)
        aliases: Alternative names for the command
        hidden: Whether to hide from help listing
        category: Command category for grouping
        group: Whether this is a command group (not a command)
        replace: Whether to replace existing registration
        force_options: If True, all parameters with defaults become --options
                      (disables Position-Based Hybrid for first parameter)
        registry: Custom registry (defaults to global)
        **metadata: Additional metadata stored in CommandInfo.metadata

    Returns:
        Decorator function or decorated function

    """
    # Handle @register_command (without parens)
    if callable(name_or_func) and not isinstance(name_or_func, str):
        func = name_or_func
        return _register_command_func(
            None,
            name=None,
            description=description,
            aliases=aliases,
            hidden=hidden,
            category=category,
            group=group,
            replace=replace,
            registry=registry,
            **metadata,
        )

    # Handle @register_command(...) (with arguments)
    # At this point, name_or_func must be str | None (not F)
    name_str: str | None = name_or_func if isinstance(name_or_func, str) or name_or_func is None else None

    def decorator(func: F) -> F:
        return _register_command_func(
            func,
            name=name_str,
            description=description,
            aliases=aliases,
            hidden=hidden,
            category=category,
            group=group,
            replace=replace,
            registry=registry,
            **metadata,
        )

    return decorator


def x_register_command__mutmut_9(  # type: ignore[misc]
    name_or_func: str | F | None = None,
    *,
    description: str | None = None,
    aliases: list[str] | None = None,
    hidden: bool = False,
    category: str | None = None,
    group: bool = False,
    replace: bool = False,
    registry: Registry | None = None,
    **metadata: Any,
) -> Any:
    """Register a CLI command in the hub.

    Can be used as a decorator with or without arguments:

        @register_command
        def my_command():
            pass

        @register_command("custom-name", aliases=["cn"], category="utils")
        def my_command():
            pass

        # Nested commands using dot notation - groups are auto-created
        @register_command("container.status")
        def container_status():
            pass

        @register_command("container.volumes.backup")
        def container_volumes_backup():
            pass

        # Explicit group with custom description (optional)
        @register_command("container", group=True, description="Container management")
        def container_group():
            pass

    Args:
        name_or_func: Command name using dot notation for nesting (e.g., "container.status")
        description: Command description (defaults to docstring)
        aliases: Alternative names for the command
        hidden: Whether to hide from help listing
        category: Command category for grouping
        group: Whether this is a command group (not a command)
        replace: Whether to replace existing registration
        force_options: If True, all parameters with defaults become --options
                      (disables Position-Based Hybrid for first parameter)
        registry: Custom registry (defaults to global)
        **metadata: Additional metadata stored in CommandInfo.metadata

    Returns:
        Decorator function or decorated function

    """
    # Handle @register_command (without parens)
    if callable(name_or_func) and not isinstance(name_or_func, str):
        func = name_or_func
        return _register_command_func(
            func,
            name=None,
            description=None,
            aliases=aliases,
            hidden=hidden,
            category=category,
            group=group,
            replace=replace,
            registry=registry,
            **metadata,
        )

    # Handle @register_command(...) (with arguments)
    # At this point, name_or_func must be str | None (not F)
    name_str: str | None = name_or_func if isinstance(name_or_func, str) or name_or_func is None else None

    def decorator(func: F) -> F:
        return _register_command_func(
            func,
            name=name_str,
            description=description,
            aliases=aliases,
            hidden=hidden,
            category=category,
            group=group,
            replace=replace,
            registry=registry,
            **metadata,
        )

    return decorator


def x_register_command__mutmut_10(  # type: ignore[misc]
    name_or_func: str | F | None = None,
    *,
    description: str | None = None,
    aliases: list[str] | None = None,
    hidden: bool = False,
    category: str | None = None,
    group: bool = False,
    replace: bool = False,
    registry: Registry | None = None,
    **metadata: Any,
) -> Any:
    """Register a CLI command in the hub.

    Can be used as a decorator with or without arguments:

        @register_command
        def my_command():
            pass

        @register_command("custom-name", aliases=["cn"], category="utils")
        def my_command():
            pass

        # Nested commands using dot notation - groups are auto-created
        @register_command("container.status")
        def container_status():
            pass

        @register_command("container.volumes.backup")
        def container_volumes_backup():
            pass

        # Explicit group with custom description (optional)
        @register_command("container", group=True, description="Container management")
        def container_group():
            pass

    Args:
        name_or_func: Command name using dot notation for nesting (e.g., "container.status")
        description: Command description (defaults to docstring)
        aliases: Alternative names for the command
        hidden: Whether to hide from help listing
        category: Command category for grouping
        group: Whether this is a command group (not a command)
        replace: Whether to replace existing registration
        force_options: If True, all parameters with defaults become --options
                      (disables Position-Based Hybrid for first parameter)
        registry: Custom registry (defaults to global)
        **metadata: Additional metadata stored in CommandInfo.metadata

    Returns:
        Decorator function or decorated function

    """
    # Handle @register_command (without parens)
    if callable(name_or_func) and not isinstance(name_or_func, str):
        func = name_or_func
        return _register_command_func(
            func,
            name=None,
            description=description,
            aliases=None,
            hidden=hidden,
            category=category,
            group=group,
            replace=replace,
            registry=registry,
            **metadata,
        )

    # Handle @register_command(...) (with arguments)
    # At this point, name_or_func must be str | None (not F)
    name_str: str | None = name_or_func if isinstance(name_or_func, str) or name_or_func is None else None

    def decorator(func: F) -> F:
        return _register_command_func(
            func,
            name=name_str,
            description=description,
            aliases=aliases,
            hidden=hidden,
            category=category,
            group=group,
            replace=replace,
            registry=registry,
            **metadata,
        )

    return decorator


def x_register_command__mutmut_11(  # type: ignore[misc]
    name_or_func: str | F | None = None,
    *,
    description: str | None = None,
    aliases: list[str] | None = None,
    hidden: bool = False,
    category: str | None = None,
    group: bool = False,
    replace: bool = False,
    registry: Registry | None = None,
    **metadata: Any,
) -> Any:
    """Register a CLI command in the hub.

    Can be used as a decorator with or without arguments:

        @register_command
        def my_command():
            pass

        @register_command("custom-name", aliases=["cn"], category="utils")
        def my_command():
            pass

        # Nested commands using dot notation - groups are auto-created
        @register_command("container.status")
        def container_status():
            pass

        @register_command("container.volumes.backup")
        def container_volumes_backup():
            pass

        # Explicit group with custom description (optional)
        @register_command("container", group=True, description="Container management")
        def container_group():
            pass

    Args:
        name_or_func: Command name using dot notation for nesting (e.g., "container.status")
        description: Command description (defaults to docstring)
        aliases: Alternative names for the command
        hidden: Whether to hide from help listing
        category: Command category for grouping
        group: Whether this is a command group (not a command)
        replace: Whether to replace existing registration
        force_options: If True, all parameters with defaults become --options
                      (disables Position-Based Hybrid for first parameter)
        registry: Custom registry (defaults to global)
        **metadata: Additional metadata stored in CommandInfo.metadata

    Returns:
        Decorator function or decorated function

    """
    # Handle @register_command (without parens)
    if callable(name_or_func) and not isinstance(name_or_func, str):
        func = name_or_func
        return _register_command_func(
            func,
            name=None,
            description=description,
            aliases=aliases,
            hidden=None,
            category=category,
            group=group,
            replace=replace,
            registry=registry,
            **metadata,
        )

    # Handle @register_command(...) (with arguments)
    # At this point, name_or_func must be str | None (not F)
    name_str: str | None = name_or_func if isinstance(name_or_func, str) or name_or_func is None else None

    def decorator(func: F) -> F:
        return _register_command_func(
            func,
            name=name_str,
            description=description,
            aliases=aliases,
            hidden=hidden,
            category=category,
            group=group,
            replace=replace,
            registry=registry,
            **metadata,
        )

    return decorator


def x_register_command__mutmut_12(  # type: ignore[misc]
    name_or_func: str | F | None = None,
    *,
    description: str | None = None,
    aliases: list[str] | None = None,
    hidden: bool = False,
    category: str | None = None,
    group: bool = False,
    replace: bool = False,
    registry: Registry | None = None,
    **metadata: Any,
) -> Any:
    """Register a CLI command in the hub.

    Can be used as a decorator with or without arguments:

        @register_command
        def my_command():
            pass

        @register_command("custom-name", aliases=["cn"], category="utils")
        def my_command():
            pass

        # Nested commands using dot notation - groups are auto-created
        @register_command("container.status")
        def container_status():
            pass

        @register_command("container.volumes.backup")
        def container_volumes_backup():
            pass

        # Explicit group with custom description (optional)
        @register_command("container", group=True, description="Container management")
        def container_group():
            pass

    Args:
        name_or_func: Command name using dot notation for nesting (e.g., "container.status")
        description: Command description (defaults to docstring)
        aliases: Alternative names for the command
        hidden: Whether to hide from help listing
        category: Command category for grouping
        group: Whether this is a command group (not a command)
        replace: Whether to replace existing registration
        force_options: If True, all parameters with defaults become --options
                      (disables Position-Based Hybrid for first parameter)
        registry: Custom registry (defaults to global)
        **metadata: Additional metadata stored in CommandInfo.metadata

    Returns:
        Decorator function or decorated function

    """
    # Handle @register_command (without parens)
    if callable(name_or_func) and not isinstance(name_or_func, str):
        func = name_or_func
        return _register_command_func(
            func,
            name=None,
            description=description,
            aliases=aliases,
            hidden=hidden,
            category=None,
            group=group,
            replace=replace,
            registry=registry,
            **metadata,
        )

    # Handle @register_command(...) (with arguments)
    # At this point, name_or_func must be str | None (not F)
    name_str: str | None = name_or_func if isinstance(name_or_func, str) or name_or_func is None else None

    def decorator(func: F) -> F:
        return _register_command_func(
            func,
            name=name_str,
            description=description,
            aliases=aliases,
            hidden=hidden,
            category=category,
            group=group,
            replace=replace,
            registry=registry,
            **metadata,
        )

    return decorator


def x_register_command__mutmut_13(  # type: ignore[misc]
    name_or_func: str | F | None = None,
    *,
    description: str | None = None,
    aliases: list[str] | None = None,
    hidden: bool = False,
    category: str | None = None,
    group: bool = False,
    replace: bool = False,
    registry: Registry | None = None,
    **metadata: Any,
) -> Any:
    """Register a CLI command in the hub.

    Can be used as a decorator with or without arguments:

        @register_command
        def my_command():
            pass

        @register_command("custom-name", aliases=["cn"], category="utils")
        def my_command():
            pass

        # Nested commands using dot notation - groups are auto-created
        @register_command("container.status")
        def container_status():
            pass

        @register_command("container.volumes.backup")
        def container_volumes_backup():
            pass

        # Explicit group with custom description (optional)
        @register_command("container", group=True, description="Container management")
        def container_group():
            pass

    Args:
        name_or_func: Command name using dot notation for nesting (e.g., "container.status")
        description: Command description (defaults to docstring)
        aliases: Alternative names for the command
        hidden: Whether to hide from help listing
        category: Command category for grouping
        group: Whether this is a command group (not a command)
        replace: Whether to replace existing registration
        force_options: If True, all parameters with defaults become --options
                      (disables Position-Based Hybrid for first parameter)
        registry: Custom registry (defaults to global)
        **metadata: Additional metadata stored in CommandInfo.metadata

    Returns:
        Decorator function or decorated function

    """
    # Handle @register_command (without parens)
    if callable(name_or_func) and not isinstance(name_or_func, str):
        func = name_or_func
        return _register_command_func(
            func,
            name=None,
            description=description,
            aliases=aliases,
            hidden=hidden,
            category=category,
            group=None,
            replace=replace,
            registry=registry,
            **metadata,
        )

    # Handle @register_command(...) (with arguments)
    # At this point, name_or_func must be str | None (not F)
    name_str: str | None = name_or_func if isinstance(name_or_func, str) or name_or_func is None else None

    def decorator(func: F) -> F:
        return _register_command_func(
            func,
            name=name_str,
            description=description,
            aliases=aliases,
            hidden=hidden,
            category=category,
            group=group,
            replace=replace,
            registry=registry,
            **metadata,
        )

    return decorator


def x_register_command__mutmut_14(  # type: ignore[misc]
    name_or_func: str | F | None = None,
    *,
    description: str | None = None,
    aliases: list[str] | None = None,
    hidden: bool = False,
    category: str | None = None,
    group: bool = False,
    replace: bool = False,
    registry: Registry | None = None,
    **metadata: Any,
) -> Any:
    """Register a CLI command in the hub.

    Can be used as a decorator with or without arguments:

        @register_command
        def my_command():
            pass

        @register_command("custom-name", aliases=["cn"], category="utils")
        def my_command():
            pass

        # Nested commands using dot notation - groups are auto-created
        @register_command("container.status")
        def container_status():
            pass

        @register_command("container.volumes.backup")
        def container_volumes_backup():
            pass

        # Explicit group with custom description (optional)
        @register_command("container", group=True, description="Container management")
        def container_group():
            pass

    Args:
        name_or_func: Command name using dot notation for nesting (e.g., "container.status")
        description: Command description (defaults to docstring)
        aliases: Alternative names for the command
        hidden: Whether to hide from help listing
        category: Command category for grouping
        group: Whether this is a command group (not a command)
        replace: Whether to replace existing registration
        force_options: If True, all parameters with defaults become --options
                      (disables Position-Based Hybrid for first parameter)
        registry: Custom registry (defaults to global)
        **metadata: Additional metadata stored in CommandInfo.metadata

    Returns:
        Decorator function or decorated function

    """
    # Handle @register_command (without parens)
    if callable(name_or_func) and not isinstance(name_or_func, str):
        func = name_or_func
        return _register_command_func(
            func,
            name=None,
            description=description,
            aliases=aliases,
            hidden=hidden,
            category=category,
            group=group,
            replace=None,
            registry=registry,
            **metadata,
        )

    # Handle @register_command(...) (with arguments)
    # At this point, name_or_func must be str | None (not F)
    name_str: str | None = name_or_func if isinstance(name_or_func, str) or name_or_func is None else None

    def decorator(func: F) -> F:
        return _register_command_func(
            func,
            name=name_str,
            description=description,
            aliases=aliases,
            hidden=hidden,
            category=category,
            group=group,
            replace=replace,
            registry=registry,
            **metadata,
        )

    return decorator


def x_register_command__mutmut_15(  # type: ignore[misc]
    name_or_func: str | F | None = None,
    *,
    description: str | None = None,
    aliases: list[str] | None = None,
    hidden: bool = False,
    category: str | None = None,
    group: bool = False,
    replace: bool = False,
    registry: Registry | None = None,
    **metadata: Any,
) -> Any:
    """Register a CLI command in the hub.

    Can be used as a decorator with or without arguments:

        @register_command
        def my_command():
            pass

        @register_command("custom-name", aliases=["cn"], category="utils")
        def my_command():
            pass

        # Nested commands using dot notation - groups are auto-created
        @register_command("container.status")
        def container_status():
            pass

        @register_command("container.volumes.backup")
        def container_volumes_backup():
            pass

        # Explicit group with custom description (optional)
        @register_command("container", group=True, description="Container management")
        def container_group():
            pass

    Args:
        name_or_func: Command name using dot notation for nesting (e.g., "container.status")
        description: Command description (defaults to docstring)
        aliases: Alternative names for the command
        hidden: Whether to hide from help listing
        category: Command category for grouping
        group: Whether this is a command group (not a command)
        replace: Whether to replace existing registration
        force_options: If True, all parameters with defaults become --options
                      (disables Position-Based Hybrid for first parameter)
        registry: Custom registry (defaults to global)
        **metadata: Additional metadata stored in CommandInfo.metadata

    Returns:
        Decorator function or decorated function

    """
    # Handle @register_command (without parens)
    if callable(name_or_func) and not isinstance(name_or_func, str):
        func = name_or_func
        return _register_command_func(
            func,
            name=None,
            description=description,
            aliases=aliases,
            hidden=hidden,
            category=category,
            group=group,
            replace=replace,
            registry=None,
            **metadata,
        )

    # Handle @register_command(...) (with arguments)
    # At this point, name_or_func must be str | None (not F)
    name_str: str | None = name_or_func if isinstance(name_or_func, str) or name_or_func is None else None

    def decorator(func: F) -> F:
        return _register_command_func(
            func,
            name=name_str,
            description=description,
            aliases=aliases,
            hidden=hidden,
            category=category,
            group=group,
            replace=replace,
            registry=registry,
            **metadata,
        )

    return decorator


def x_register_command__mutmut_16(  # type: ignore[misc]
    name_or_func: str | F | None = None,
    *,
    description: str | None = None,
    aliases: list[str] | None = None,
    hidden: bool = False,
    category: str | None = None,
    group: bool = False,
    replace: bool = False,
    registry: Registry | None = None,
    **metadata: Any,
) -> Any:
    """Register a CLI command in the hub.

    Can be used as a decorator with or without arguments:

        @register_command
        def my_command():
            pass

        @register_command("custom-name", aliases=["cn"], category="utils")
        def my_command():
            pass

        # Nested commands using dot notation - groups are auto-created
        @register_command("container.status")
        def container_status():
            pass

        @register_command("container.volumes.backup")
        def container_volumes_backup():
            pass

        # Explicit group with custom description (optional)
        @register_command("container", group=True, description="Container management")
        def container_group():
            pass

    Args:
        name_or_func: Command name using dot notation for nesting (e.g., "container.status")
        description: Command description (defaults to docstring)
        aliases: Alternative names for the command
        hidden: Whether to hide from help listing
        category: Command category for grouping
        group: Whether this is a command group (not a command)
        replace: Whether to replace existing registration
        force_options: If True, all parameters with defaults become --options
                      (disables Position-Based Hybrid for first parameter)
        registry: Custom registry (defaults to global)
        **metadata: Additional metadata stored in CommandInfo.metadata

    Returns:
        Decorator function or decorated function

    """
    # Handle @register_command (without parens)
    if callable(name_or_func) and not isinstance(name_or_func, str):
        func = name_or_func
        return _register_command_func(
            name=None,
            description=description,
            aliases=aliases,
            hidden=hidden,
            category=category,
            group=group,
            replace=replace,
            registry=registry,
            **metadata,
        )

    # Handle @register_command(...) (with arguments)
    # At this point, name_or_func must be str | None (not F)
    name_str: str | None = name_or_func if isinstance(name_or_func, str) or name_or_func is None else None

    def decorator(func: F) -> F:
        return _register_command_func(
            func,
            name=name_str,
            description=description,
            aliases=aliases,
            hidden=hidden,
            category=category,
            group=group,
            replace=replace,
            registry=registry,
            **metadata,
        )

    return decorator


def x_register_command__mutmut_17(  # type: ignore[misc]
    name_or_func: str | F | None = None,
    *,
    description: str | None = None,
    aliases: list[str] | None = None,
    hidden: bool = False,
    category: str | None = None,
    group: bool = False,
    replace: bool = False,
    registry: Registry | None = None,
    **metadata: Any,
) -> Any:
    """Register a CLI command in the hub.

    Can be used as a decorator with or without arguments:

        @register_command
        def my_command():
            pass

        @register_command("custom-name", aliases=["cn"], category="utils")
        def my_command():
            pass

        # Nested commands using dot notation - groups are auto-created
        @register_command("container.status")
        def container_status():
            pass

        @register_command("container.volumes.backup")
        def container_volumes_backup():
            pass

        # Explicit group with custom description (optional)
        @register_command("container", group=True, description="Container management")
        def container_group():
            pass

    Args:
        name_or_func: Command name using dot notation for nesting (e.g., "container.status")
        description: Command description (defaults to docstring)
        aliases: Alternative names for the command
        hidden: Whether to hide from help listing
        category: Command category for grouping
        group: Whether this is a command group (not a command)
        replace: Whether to replace existing registration
        force_options: If True, all parameters with defaults become --options
                      (disables Position-Based Hybrid for first parameter)
        registry: Custom registry (defaults to global)
        **metadata: Additional metadata stored in CommandInfo.metadata

    Returns:
        Decorator function or decorated function

    """
    # Handle @register_command (without parens)
    if callable(name_or_func) and not isinstance(name_or_func, str):
        func = name_or_func
        return _register_command_func(
            func,
            description=description,
            aliases=aliases,
            hidden=hidden,
            category=category,
            group=group,
            replace=replace,
            registry=registry,
            **metadata,
        )

    # Handle @register_command(...) (with arguments)
    # At this point, name_or_func must be str | None (not F)
    name_str: str | None = name_or_func if isinstance(name_or_func, str) or name_or_func is None else None

    def decorator(func: F) -> F:
        return _register_command_func(
            func,
            name=name_str,
            description=description,
            aliases=aliases,
            hidden=hidden,
            category=category,
            group=group,
            replace=replace,
            registry=registry,
            **metadata,
        )

    return decorator


def x_register_command__mutmut_18(  # type: ignore[misc]
    name_or_func: str | F | None = None,
    *,
    description: str | None = None,
    aliases: list[str] | None = None,
    hidden: bool = False,
    category: str | None = None,
    group: bool = False,
    replace: bool = False,
    registry: Registry | None = None,
    **metadata: Any,
) -> Any:
    """Register a CLI command in the hub.

    Can be used as a decorator with or without arguments:

        @register_command
        def my_command():
            pass

        @register_command("custom-name", aliases=["cn"], category="utils")
        def my_command():
            pass

        # Nested commands using dot notation - groups are auto-created
        @register_command("container.status")
        def container_status():
            pass

        @register_command("container.volumes.backup")
        def container_volumes_backup():
            pass

        # Explicit group with custom description (optional)
        @register_command("container", group=True, description="Container management")
        def container_group():
            pass

    Args:
        name_or_func: Command name using dot notation for nesting (e.g., "container.status")
        description: Command description (defaults to docstring)
        aliases: Alternative names for the command
        hidden: Whether to hide from help listing
        category: Command category for grouping
        group: Whether this is a command group (not a command)
        replace: Whether to replace existing registration
        force_options: If True, all parameters with defaults become --options
                      (disables Position-Based Hybrid for first parameter)
        registry: Custom registry (defaults to global)
        **metadata: Additional metadata stored in CommandInfo.metadata

    Returns:
        Decorator function or decorated function

    """
    # Handle @register_command (without parens)
    if callable(name_or_func) and not isinstance(name_or_func, str):
        func = name_or_func
        return _register_command_func(
            func,
            name=None,
            aliases=aliases,
            hidden=hidden,
            category=category,
            group=group,
            replace=replace,
            registry=registry,
            **metadata,
        )

    # Handle @register_command(...) (with arguments)
    # At this point, name_or_func must be str | None (not F)
    name_str: str | None = name_or_func if isinstance(name_or_func, str) or name_or_func is None else None

    def decorator(func: F) -> F:
        return _register_command_func(
            func,
            name=name_str,
            description=description,
            aliases=aliases,
            hidden=hidden,
            category=category,
            group=group,
            replace=replace,
            registry=registry,
            **metadata,
        )

    return decorator


def x_register_command__mutmut_19(  # type: ignore[misc]
    name_or_func: str | F | None = None,
    *,
    description: str | None = None,
    aliases: list[str] | None = None,
    hidden: bool = False,
    category: str | None = None,
    group: bool = False,
    replace: bool = False,
    registry: Registry | None = None,
    **metadata: Any,
) -> Any:
    """Register a CLI command in the hub.

    Can be used as a decorator with or without arguments:

        @register_command
        def my_command():
            pass

        @register_command("custom-name", aliases=["cn"], category="utils")
        def my_command():
            pass

        # Nested commands using dot notation - groups are auto-created
        @register_command("container.status")
        def container_status():
            pass

        @register_command("container.volumes.backup")
        def container_volumes_backup():
            pass

        # Explicit group with custom description (optional)
        @register_command("container", group=True, description="Container management")
        def container_group():
            pass

    Args:
        name_or_func: Command name using dot notation for nesting (e.g., "container.status")
        description: Command description (defaults to docstring)
        aliases: Alternative names for the command
        hidden: Whether to hide from help listing
        category: Command category for grouping
        group: Whether this is a command group (not a command)
        replace: Whether to replace existing registration
        force_options: If True, all parameters with defaults become --options
                      (disables Position-Based Hybrid for first parameter)
        registry: Custom registry (defaults to global)
        **metadata: Additional metadata stored in CommandInfo.metadata

    Returns:
        Decorator function or decorated function

    """
    # Handle @register_command (without parens)
    if callable(name_or_func) and not isinstance(name_or_func, str):
        func = name_or_func
        return _register_command_func(
            func,
            name=None,
            description=description,
            hidden=hidden,
            category=category,
            group=group,
            replace=replace,
            registry=registry,
            **metadata,
        )

    # Handle @register_command(...) (with arguments)
    # At this point, name_or_func must be str | None (not F)
    name_str: str | None = name_or_func if isinstance(name_or_func, str) or name_or_func is None else None

    def decorator(func: F) -> F:
        return _register_command_func(
            func,
            name=name_str,
            description=description,
            aliases=aliases,
            hidden=hidden,
            category=category,
            group=group,
            replace=replace,
            registry=registry,
            **metadata,
        )

    return decorator


def x_register_command__mutmut_20(  # type: ignore[misc]
    name_or_func: str | F | None = None,
    *,
    description: str | None = None,
    aliases: list[str] | None = None,
    hidden: bool = False,
    category: str | None = None,
    group: bool = False,
    replace: bool = False,
    registry: Registry | None = None,
    **metadata: Any,
) -> Any:
    """Register a CLI command in the hub.

    Can be used as a decorator with or without arguments:

        @register_command
        def my_command():
            pass

        @register_command("custom-name", aliases=["cn"], category="utils")
        def my_command():
            pass

        # Nested commands using dot notation - groups are auto-created
        @register_command("container.status")
        def container_status():
            pass

        @register_command("container.volumes.backup")
        def container_volumes_backup():
            pass

        # Explicit group with custom description (optional)
        @register_command("container", group=True, description="Container management")
        def container_group():
            pass

    Args:
        name_or_func: Command name using dot notation for nesting (e.g., "container.status")
        description: Command description (defaults to docstring)
        aliases: Alternative names for the command
        hidden: Whether to hide from help listing
        category: Command category for grouping
        group: Whether this is a command group (not a command)
        replace: Whether to replace existing registration
        force_options: If True, all parameters with defaults become --options
                      (disables Position-Based Hybrid for first parameter)
        registry: Custom registry (defaults to global)
        **metadata: Additional metadata stored in CommandInfo.metadata

    Returns:
        Decorator function or decorated function

    """
    # Handle @register_command (without parens)
    if callable(name_or_func) and not isinstance(name_or_func, str):
        func = name_or_func
        return _register_command_func(
            func,
            name=None,
            description=description,
            aliases=aliases,
            category=category,
            group=group,
            replace=replace,
            registry=registry,
            **metadata,
        )

    # Handle @register_command(...) (with arguments)
    # At this point, name_or_func must be str | None (not F)
    name_str: str | None = name_or_func if isinstance(name_or_func, str) or name_or_func is None else None

    def decorator(func: F) -> F:
        return _register_command_func(
            func,
            name=name_str,
            description=description,
            aliases=aliases,
            hidden=hidden,
            category=category,
            group=group,
            replace=replace,
            registry=registry,
            **metadata,
        )

    return decorator


def x_register_command__mutmut_21(  # type: ignore[misc]
    name_or_func: str | F | None = None,
    *,
    description: str | None = None,
    aliases: list[str] | None = None,
    hidden: bool = False,
    category: str | None = None,
    group: bool = False,
    replace: bool = False,
    registry: Registry | None = None,
    **metadata: Any,
) -> Any:
    """Register a CLI command in the hub.

    Can be used as a decorator with or without arguments:

        @register_command
        def my_command():
            pass

        @register_command("custom-name", aliases=["cn"], category="utils")
        def my_command():
            pass

        # Nested commands using dot notation - groups are auto-created
        @register_command("container.status")
        def container_status():
            pass

        @register_command("container.volumes.backup")
        def container_volumes_backup():
            pass

        # Explicit group with custom description (optional)
        @register_command("container", group=True, description="Container management")
        def container_group():
            pass

    Args:
        name_or_func: Command name using dot notation for nesting (e.g., "container.status")
        description: Command description (defaults to docstring)
        aliases: Alternative names for the command
        hidden: Whether to hide from help listing
        category: Command category for grouping
        group: Whether this is a command group (not a command)
        replace: Whether to replace existing registration
        force_options: If True, all parameters with defaults become --options
                      (disables Position-Based Hybrid for first parameter)
        registry: Custom registry (defaults to global)
        **metadata: Additional metadata stored in CommandInfo.metadata

    Returns:
        Decorator function or decorated function

    """
    # Handle @register_command (without parens)
    if callable(name_or_func) and not isinstance(name_or_func, str):
        func = name_or_func
        return _register_command_func(
            func,
            name=None,
            description=description,
            aliases=aliases,
            hidden=hidden,
            group=group,
            replace=replace,
            registry=registry,
            **metadata,
        )

    # Handle @register_command(...) (with arguments)
    # At this point, name_or_func must be str | None (not F)
    name_str: str | None = name_or_func if isinstance(name_or_func, str) or name_or_func is None else None

    def decorator(func: F) -> F:
        return _register_command_func(
            func,
            name=name_str,
            description=description,
            aliases=aliases,
            hidden=hidden,
            category=category,
            group=group,
            replace=replace,
            registry=registry,
            **metadata,
        )

    return decorator


def x_register_command__mutmut_22(  # type: ignore[misc]
    name_or_func: str | F | None = None,
    *,
    description: str | None = None,
    aliases: list[str] | None = None,
    hidden: bool = False,
    category: str | None = None,
    group: bool = False,
    replace: bool = False,
    registry: Registry | None = None,
    **metadata: Any,
) -> Any:
    """Register a CLI command in the hub.

    Can be used as a decorator with or without arguments:

        @register_command
        def my_command():
            pass

        @register_command("custom-name", aliases=["cn"], category="utils")
        def my_command():
            pass

        # Nested commands using dot notation - groups are auto-created
        @register_command("container.status")
        def container_status():
            pass

        @register_command("container.volumes.backup")
        def container_volumes_backup():
            pass

        # Explicit group with custom description (optional)
        @register_command("container", group=True, description="Container management")
        def container_group():
            pass

    Args:
        name_or_func: Command name using dot notation for nesting (e.g., "container.status")
        description: Command description (defaults to docstring)
        aliases: Alternative names for the command
        hidden: Whether to hide from help listing
        category: Command category for grouping
        group: Whether this is a command group (not a command)
        replace: Whether to replace existing registration
        force_options: If True, all parameters with defaults become --options
                      (disables Position-Based Hybrid for first parameter)
        registry: Custom registry (defaults to global)
        **metadata: Additional metadata stored in CommandInfo.metadata

    Returns:
        Decorator function or decorated function

    """
    # Handle @register_command (without parens)
    if callable(name_or_func) and not isinstance(name_or_func, str):
        func = name_or_func
        return _register_command_func(
            func,
            name=None,
            description=description,
            aliases=aliases,
            hidden=hidden,
            category=category,
            replace=replace,
            registry=registry,
            **metadata,
        )

    # Handle @register_command(...) (with arguments)
    # At this point, name_or_func must be str | None (not F)
    name_str: str | None = name_or_func if isinstance(name_or_func, str) or name_or_func is None else None

    def decorator(func: F) -> F:
        return _register_command_func(
            func,
            name=name_str,
            description=description,
            aliases=aliases,
            hidden=hidden,
            category=category,
            group=group,
            replace=replace,
            registry=registry,
            **metadata,
        )

    return decorator


def x_register_command__mutmut_23(  # type: ignore[misc]
    name_or_func: str | F | None = None,
    *,
    description: str | None = None,
    aliases: list[str] | None = None,
    hidden: bool = False,
    category: str | None = None,
    group: bool = False,
    replace: bool = False,
    registry: Registry | None = None,
    **metadata: Any,
) -> Any:
    """Register a CLI command in the hub.

    Can be used as a decorator with or without arguments:

        @register_command
        def my_command():
            pass

        @register_command("custom-name", aliases=["cn"], category="utils")
        def my_command():
            pass

        # Nested commands using dot notation - groups are auto-created
        @register_command("container.status")
        def container_status():
            pass

        @register_command("container.volumes.backup")
        def container_volumes_backup():
            pass

        # Explicit group with custom description (optional)
        @register_command("container", group=True, description="Container management")
        def container_group():
            pass

    Args:
        name_or_func: Command name using dot notation for nesting (e.g., "container.status")
        description: Command description (defaults to docstring)
        aliases: Alternative names for the command
        hidden: Whether to hide from help listing
        category: Command category for grouping
        group: Whether this is a command group (not a command)
        replace: Whether to replace existing registration
        force_options: If True, all parameters with defaults become --options
                      (disables Position-Based Hybrid for first parameter)
        registry: Custom registry (defaults to global)
        **metadata: Additional metadata stored in CommandInfo.metadata

    Returns:
        Decorator function or decorated function

    """
    # Handle @register_command (without parens)
    if callable(name_or_func) and not isinstance(name_or_func, str):
        func = name_or_func
        return _register_command_func(
            func,
            name=None,
            description=description,
            aliases=aliases,
            hidden=hidden,
            category=category,
            group=group,
            registry=registry,
            **metadata,
        )

    # Handle @register_command(...) (with arguments)
    # At this point, name_or_func must be str | None (not F)
    name_str: str | None = name_or_func if isinstance(name_or_func, str) or name_or_func is None else None

    def decorator(func: F) -> F:
        return _register_command_func(
            func,
            name=name_str,
            description=description,
            aliases=aliases,
            hidden=hidden,
            category=category,
            group=group,
            replace=replace,
            registry=registry,
            **metadata,
        )

    return decorator


def x_register_command__mutmut_24(  # type: ignore[misc]
    name_or_func: str | F | None = None,
    *,
    description: str | None = None,
    aliases: list[str] | None = None,
    hidden: bool = False,
    category: str | None = None,
    group: bool = False,
    replace: bool = False,
    registry: Registry | None = None,
    **metadata: Any,
) -> Any:
    """Register a CLI command in the hub.

    Can be used as a decorator with or without arguments:

        @register_command
        def my_command():
            pass

        @register_command("custom-name", aliases=["cn"], category="utils")
        def my_command():
            pass

        # Nested commands using dot notation - groups are auto-created
        @register_command("container.status")
        def container_status():
            pass

        @register_command("container.volumes.backup")
        def container_volumes_backup():
            pass

        # Explicit group with custom description (optional)
        @register_command("container", group=True, description="Container management")
        def container_group():
            pass

    Args:
        name_or_func: Command name using dot notation for nesting (e.g., "container.status")
        description: Command description (defaults to docstring)
        aliases: Alternative names for the command
        hidden: Whether to hide from help listing
        category: Command category for grouping
        group: Whether this is a command group (not a command)
        replace: Whether to replace existing registration
        force_options: If True, all parameters with defaults become --options
                      (disables Position-Based Hybrid for first parameter)
        registry: Custom registry (defaults to global)
        **metadata: Additional metadata stored in CommandInfo.metadata

    Returns:
        Decorator function or decorated function

    """
    # Handle @register_command (without parens)
    if callable(name_or_func) and not isinstance(name_or_func, str):
        func = name_or_func
        return _register_command_func(
            func,
            name=None,
            description=description,
            aliases=aliases,
            hidden=hidden,
            category=category,
            group=group,
            replace=replace,
            **metadata,
        )

    # Handle @register_command(...) (with arguments)
    # At this point, name_or_func must be str | None (not F)
    name_str: str | None = name_or_func if isinstance(name_or_func, str) or name_or_func is None else None

    def decorator(func: F) -> F:
        return _register_command_func(
            func,
            name=name_str,
            description=description,
            aliases=aliases,
            hidden=hidden,
            category=category,
            group=group,
            replace=replace,
            registry=registry,
            **metadata,
        )

    return decorator


def x_register_command__mutmut_25(  # type: ignore[misc]
    name_or_func: str | F | None = None,
    *,
    description: str | None = None,
    aliases: list[str] | None = None,
    hidden: bool = False,
    category: str | None = None,
    group: bool = False,
    replace: bool = False,
    registry: Registry | None = None,
    **metadata: Any,
) -> Any:
    """Register a CLI command in the hub.

    Can be used as a decorator with or without arguments:

        @register_command
        def my_command():
            pass

        @register_command("custom-name", aliases=["cn"], category="utils")
        def my_command():
            pass

        # Nested commands using dot notation - groups are auto-created
        @register_command("container.status")
        def container_status():
            pass

        @register_command("container.volumes.backup")
        def container_volumes_backup():
            pass

        # Explicit group with custom description (optional)
        @register_command("container", group=True, description="Container management")
        def container_group():
            pass

    Args:
        name_or_func: Command name using dot notation for nesting (e.g., "container.status")
        description: Command description (defaults to docstring)
        aliases: Alternative names for the command
        hidden: Whether to hide from help listing
        category: Command category for grouping
        group: Whether this is a command group (not a command)
        replace: Whether to replace existing registration
        force_options: If True, all parameters with defaults become --options
                      (disables Position-Based Hybrid for first parameter)
        registry: Custom registry (defaults to global)
        **metadata: Additional metadata stored in CommandInfo.metadata

    Returns:
        Decorator function or decorated function

    """
    # Handle @register_command (without parens)
    if callable(name_or_func) and not isinstance(name_or_func, str):
        func = name_or_func
        return _register_command_func(
            func,
            name=None,
            description=description,
            aliases=aliases,
            hidden=hidden,
            category=category,
            group=group,
            replace=replace,
            registry=registry,
        )

    # Handle @register_command(...) (with arguments)
    # At this point, name_or_func must be str | None (not F)
    name_str: str | None = name_or_func if isinstance(name_or_func, str) or name_or_func is None else None

    def decorator(func: F) -> F:
        return _register_command_func(
            func,
            name=name_str,
            description=description,
            aliases=aliases,
            hidden=hidden,
            category=category,
            group=group,
            replace=replace,
            registry=registry,
            **metadata,
        )

    return decorator


def x_register_command__mutmut_26(  # type: ignore[misc]
    name_or_func: str | F | None = None,
    *,
    description: str | None = None,
    aliases: list[str] | None = None,
    hidden: bool = False,
    category: str | None = None,
    group: bool = False,
    replace: bool = False,
    registry: Registry | None = None,
    **metadata: Any,
) -> Any:
    """Register a CLI command in the hub.

    Can be used as a decorator with or without arguments:

        @register_command
        def my_command():
            pass

        @register_command("custom-name", aliases=["cn"], category="utils")
        def my_command():
            pass

        # Nested commands using dot notation - groups are auto-created
        @register_command("container.status")
        def container_status():
            pass

        @register_command("container.volumes.backup")
        def container_volumes_backup():
            pass

        # Explicit group with custom description (optional)
        @register_command("container", group=True, description="Container management")
        def container_group():
            pass

    Args:
        name_or_func: Command name using dot notation for nesting (e.g., "container.status")
        description: Command description (defaults to docstring)
        aliases: Alternative names for the command
        hidden: Whether to hide from help listing
        category: Command category for grouping
        group: Whether this is a command group (not a command)
        replace: Whether to replace existing registration
        force_options: If True, all parameters with defaults become --options
                      (disables Position-Based Hybrid for first parameter)
        registry: Custom registry (defaults to global)
        **metadata: Additional metadata stored in CommandInfo.metadata

    Returns:
        Decorator function or decorated function

    """
    # Handle @register_command (without parens)
    if callable(name_or_func) and not isinstance(name_or_func, str):
        func = name_or_func
        return _register_command_func(
            func,
            name=None,
            description=description,
            aliases=aliases,
            hidden=hidden,
            category=category,
            group=group,
            replace=replace,
            registry=registry,
            **metadata,
        )

    # Handle @register_command(...) (with arguments)
    # At this point, name_or_func must be str | None (not F)
    name_str: str | None = None

    def decorator(func: F) -> F:
        return _register_command_func(
            func,
            name=name_str,
            description=description,
            aliases=aliases,
            hidden=hidden,
            category=category,
            group=group,
            replace=replace,
            registry=registry,
            **metadata,
        )

    return decorator


def x_register_command__mutmut_27(  # type: ignore[misc]
    name_or_func: str | F | None = None,
    *,
    description: str | None = None,
    aliases: list[str] | None = None,
    hidden: bool = False,
    category: str | None = None,
    group: bool = False,
    replace: bool = False,
    registry: Registry | None = None,
    **metadata: Any,
) -> Any:
    """Register a CLI command in the hub.

    Can be used as a decorator with or without arguments:

        @register_command
        def my_command():
            pass

        @register_command("custom-name", aliases=["cn"], category="utils")
        def my_command():
            pass

        # Nested commands using dot notation - groups are auto-created
        @register_command("container.status")
        def container_status():
            pass

        @register_command("container.volumes.backup")
        def container_volumes_backup():
            pass

        # Explicit group with custom description (optional)
        @register_command("container", group=True, description="Container management")
        def container_group():
            pass

    Args:
        name_or_func: Command name using dot notation for nesting (e.g., "container.status")
        description: Command description (defaults to docstring)
        aliases: Alternative names for the command
        hidden: Whether to hide from help listing
        category: Command category for grouping
        group: Whether this is a command group (not a command)
        replace: Whether to replace existing registration
        force_options: If True, all parameters with defaults become --options
                      (disables Position-Based Hybrid for first parameter)
        registry: Custom registry (defaults to global)
        **metadata: Additional metadata stored in CommandInfo.metadata

    Returns:
        Decorator function or decorated function

    """
    # Handle @register_command (without parens)
    if callable(name_or_func) and not isinstance(name_or_func, str):
        func = name_or_func
        return _register_command_func(
            func,
            name=None,
            description=description,
            aliases=aliases,
            hidden=hidden,
            category=category,
            group=group,
            replace=replace,
            registry=registry,
            **metadata,
        )

    # Handle @register_command(...) (with arguments)
    # At this point, name_or_func must be str | None (not F)
    name_str: str | None = name_or_func if isinstance(name_or_func, str) and name_or_func is None else None

    def decorator(func: F) -> F:
        return _register_command_func(
            func,
            name=name_str,
            description=description,
            aliases=aliases,
            hidden=hidden,
            category=category,
            group=group,
            replace=replace,
            registry=registry,
            **metadata,
        )

    return decorator


def x_register_command__mutmut_28(  # type: ignore[misc]
    name_or_func: str | F | None = None,
    *,
    description: str | None = None,
    aliases: list[str] | None = None,
    hidden: bool = False,
    category: str | None = None,
    group: bool = False,
    replace: bool = False,
    registry: Registry | None = None,
    **metadata: Any,
) -> Any:
    """Register a CLI command in the hub.

    Can be used as a decorator with or without arguments:

        @register_command
        def my_command():
            pass

        @register_command("custom-name", aliases=["cn"], category="utils")
        def my_command():
            pass

        # Nested commands using dot notation - groups are auto-created
        @register_command("container.status")
        def container_status():
            pass

        @register_command("container.volumes.backup")
        def container_volumes_backup():
            pass

        # Explicit group with custom description (optional)
        @register_command("container", group=True, description="Container management")
        def container_group():
            pass

    Args:
        name_or_func: Command name using dot notation for nesting (e.g., "container.status")
        description: Command description (defaults to docstring)
        aliases: Alternative names for the command
        hidden: Whether to hide from help listing
        category: Command category for grouping
        group: Whether this is a command group (not a command)
        replace: Whether to replace existing registration
        force_options: If True, all parameters with defaults become --options
                      (disables Position-Based Hybrid for first parameter)
        registry: Custom registry (defaults to global)
        **metadata: Additional metadata stored in CommandInfo.metadata

    Returns:
        Decorator function or decorated function

    """
    # Handle @register_command (without parens)
    if callable(name_or_func) and not isinstance(name_or_func, str):
        func = name_or_func
        return _register_command_func(
            func,
            name=None,
            description=description,
            aliases=aliases,
            hidden=hidden,
            category=category,
            group=group,
            replace=replace,
            registry=registry,
            **metadata,
        )

    # Handle @register_command(...) (with arguments)
    # At this point, name_or_func must be str | None (not F)
    name_str: str | None = name_or_func if isinstance(name_or_func, str) or name_or_func is not None else None

    def decorator(func: F) -> F:
        return _register_command_func(
            func,
            name=name_str,
            description=description,
            aliases=aliases,
            hidden=hidden,
            category=category,
            group=group,
            replace=replace,
            registry=registry,
            **metadata,
        )

    return decorator


def x_register_command__mutmut_29(  # type: ignore[misc]
    name_or_func: str | F | None = None,
    *,
    description: str | None = None,
    aliases: list[str] | None = None,
    hidden: bool = False,
    category: str | None = None,
    group: bool = False,
    replace: bool = False,
    registry: Registry | None = None,
    **metadata: Any,
) -> Any:
    """Register a CLI command in the hub.

    Can be used as a decorator with or without arguments:

        @register_command
        def my_command():
            pass

        @register_command("custom-name", aliases=["cn"], category="utils")
        def my_command():
            pass

        # Nested commands using dot notation - groups are auto-created
        @register_command("container.status")
        def container_status():
            pass

        @register_command("container.volumes.backup")
        def container_volumes_backup():
            pass

        # Explicit group with custom description (optional)
        @register_command("container", group=True, description="Container management")
        def container_group():
            pass

    Args:
        name_or_func: Command name using dot notation for nesting (e.g., "container.status")
        description: Command description (defaults to docstring)
        aliases: Alternative names for the command
        hidden: Whether to hide from help listing
        category: Command category for grouping
        group: Whether this is a command group (not a command)
        replace: Whether to replace existing registration
        force_options: If True, all parameters with defaults become --options
                      (disables Position-Based Hybrid for first parameter)
        registry: Custom registry (defaults to global)
        **metadata: Additional metadata stored in CommandInfo.metadata

    Returns:
        Decorator function or decorated function

    """
    # Handle @register_command (without parens)
    if callable(name_or_func) and not isinstance(name_or_func, str):
        func = name_or_func
        return _register_command_func(
            func,
            name=None,
            description=description,
            aliases=aliases,
            hidden=hidden,
            category=category,
            group=group,
            replace=replace,
            registry=registry,
            **metadata,
        )

    # Handle @register_command(...) (with arguments)
    # At this point, name_or_func must be str | None (not F)
    name_str: str | None = name_or_func if isinstance(name_or_func, str) or name_or_func is None else None

    def decorator(func: F) -> F:
        return _register_command_func(
            None,
            name=name_str,
            description=description,
            aliases=aliases,
            hidden=hidden,
            category=category,
            group=group,
            replace=replace,
            registry=registry,
            **metadata,
        )

    return decorator


def x_register_command__mutmut_30(  # type: ignore[misc]
    name_or_func: str | F | None = None,
    *,
    description: str | None = None,
    aliases: list[str] | None = None,
    hidden: bool = False,
    category: str | None = None,
    group: bool = False,
    replace: bool = False,
    registry: Registry | None = None,
    **metadata: Any,
) -> Any:
    """Register a CLI command in the hub.

    Can be used as a decorator with or without arguments:

        @register_command
        def my_command():
            pass

        @register_command("custom-name", aliases=["cn"], category="utils")
        def my_command():
            pass

        # Nested commands using dot notation - groups are auto-created
        @register_command("container.status")
        def container_status():
            pass

        @register_command("container.volumes.backup")
        def container_volumes_backup():
            pass

        # Explicit group with custom description (optional)
        @register_command("container", group=True, description="Container management")
        def container_group():
            pass

    Args:
        name_or_func: Command name using dot notation for nesting (e.g., "container.status")
        description: Command description (defaults to docstring)
        aliases: Alternative names for the command
        hidden: Whether to hide from help listing
        category: Command category for grouping
        group: Whether this is a command group (not a command)
        replace: Whether to replace existing registration
        force_options: If True, all parameters with defaults become --options
                      (disables Position-Based Hybrid for first parameter)
        registry: Custom registry (defaults to global)
        **metadata: Additional metadata stored in CommandInfo.metadata

    Returns:
        Decorator function or decorated function

    """
    # Handle @register_command (without parens)
    if callable(name_or_func) and not isinstance(name_or_func, str):
        func = name_or_func
        return _register_command_func(
            func,
            name=None,
            description=description,
            aliases=aliases,
            hidden=hidden,
            category=category,
            group=group,
            replace=replace,
            registry=registry,
            **metadata,
        )

    # Handle @register_command(...) (with arguments)
    # At this point, name_or_func must be str | None (not F)
    name_str: str | None = name_or_func if isinstance(name_or_func, str) or name_or_func is None else None

    def decorator(func: F) -> F:
        return _register_command_func(
            func,
            name=None,
            description=description,
            aliases=aliases,
            hidden=hidden,
            category=category,
            group=group,
            replace=replace,
            registry=registry,
            **metadata,
        )

    return decorator


def x_register_command__mutmut_31(  # type: ignore[misc]
    name_or_func: str | F | None = None,
    *,
    description: str | None = None,
    aliases: list[str] | None = None,
    hidden: bool = False,
    category: str | None = None,
    group: bool = False,
    replace: bool = False,
    registry: Registry | None = None,
    **metadata: Any,
) -> Any:
    """Register a CLI command in the hub.

    Can be used as a decorator with or without arguments:

        @register_command
        def my_command():
            pass

        @register_command("custom-name", aliases=["cn"], category="utils")
        def my_command():
            pass

        # Nested commands using dot notation - groups are auto-created
        @register_command("container.status")
        def container_status():
            pass

        @register_command("container.volumes.backup")
        def container_volumes_backup():
            pass

        # Explicit group with custom description (optional)
        @register_command("container", group=True, description="Container management")
        def container_group():
            pass

    Args:
        name_or_func: Command name using dot notation for nesting (e.g., "container.status")
        description: Command description (defaults to docstring)
        aliases: Alternative names for the command
        hidden: Whether to hide from help listing
        category: Command category for grouping
        group: Whether this is a command group (not a command)
        replace: Whether to replace existing registration
        force_options: If True, all parameters with defaults become --options
                      (disables Position-Based Hybrid for first parameter)
        registry: Custom registry (defaults to global)
        **metadata: Additional metadata stored in CommandInfo.metadata

    Returns:
        Decorator function or decorated function

    """
    # Handle @register_command (without parens)
    if callable(name_or_func) and not isinstance(name_or_func, str):
        func = name_or_func
        return _register_command_func(
            func,
            name=None,
            description=description,
            aliases=aliases,
            hidden=hidden,
            category=category,
            group=group,
            replace=replace,
            registry=registry,
            **metadata,
        )

    # Handle @register_command(...) (with arguments)
    # At this point, name_or_func must be str | None (not F)
    name_str: str | None = name_or_func if isinstance(name_or_func, str) or name_or_func is None else None

    def decorator(func: F) -> F:
        return _register_command_func(
            func,
            name=name_str,
            description=None,
            aliases=aliases,
            hidden=hidden,
            category=category,
            group=group,
            replace=replace,
            registry=registry,
            **metadata,
        )

    return decorator


def x_register_command__mutmut_32(  # type: ignore[misc]
    name_or_func: str | F | None = None,
    *,
    description: str | None = None,
    aliases: list[str] | None = None,
    hidden: bool = False,
    category: str | None = None,
    group: bool = False,
    replace: bool = False,
    registry: Registry | None = None,
    **metadata: Any,
) -> Any:
    """Register a CLI command in the hub.

    Can be used as a decorator with or without arguments:

        @register_command
        def my_command():
            pass

        @register_command("custom-name", aliases=["cn"], category="utils")
        def my_command():
            pass

        # Nested commands using dot notation - groups are auto-created
        @register_command("container.status")
        def container_status():
            pass

        @register_command("container.volumes.backup")
        def container_volumes_backup():
            pass

        # Explicit group with custom description (optional)
        @register_command("container", group=True, description="Container management")
        def container_group():
            pass

    Args:
        name_or_func: Command name using dot notation for nesting (e.g., "container.status")
        description: Command description (defaults to docstring)
        aliases: Alternative names for the command
        hidden: Whether to hide from help listing
        category: Command category for grouping
        group: Whether this is a command group (not a command)
        replace: Whether to replace existing registration
        force_options: If True, all parameters with defaults become --options
                      (disables Position-Based Hybrid for first parameter)
        registry: Custom registry (defaults to global)
        **metadata: Additional metadata stored in CommandInfo.metadata

    Returns:
        Decorator function or decorated function

    """
    # Handle @register_command (without parens)
    if callable(name_or_func) and not isinstance(name_or_func, str):
        func = name_or_func
        return _register_command_func(
            func,
            name=None,
            description=description,
            aliases=aliases,
            hidden=hidden,
            category=category,
            group=group,
            replace=replace,
            registry=registry,
            **metadata,
        )

    # Handle @register_command(...) (with arguments)
    # At this point, name_or_func must be str | None (not F)
    name_str: str | None = name_or_func if isinstance(name_or_func, str) or name_or_func is None else None

    def decorator(func: F) -> F:
        return _register_command_func(
            func,
            name=name_str,
            description=description,
            aliases=None,
            hidden=hidden,
            category=category,
            group=group,
            replace=replace,
            registry=registry,
            **metadata,
        )

    return decorator


def x_register_command__mutmut_33(  # type: ignore[misc]
    name_or_func: str | F | None = None,
    *,
    description: str | None = None,
    aliases: list[str] | None = None,
    hidden: bool = False,
    category: str | None = None,
    group: bool = False,
    replace: bool = False,
    registry: Registry | None = None,
    **metadata: Any,
) -> Any:
    """Register a CLI command in the hub.

    Can be used as a decorator with or without arguments:

        @register_command
        def my_command():
            pass

        @register_command("custom-name", aliases=["cn"], category="utils")
        def my_command():
            pass

        # Nested commands using dot notation - groups are auto-created
        @register_command("container.status")
        def container_status():
            pass

        @register_command("container.volumes.backup")
        def container_volumes_backup():
            pass

        # Explicit group with custom description (optional)
        @register_command("container", group=True, description="Container management")
        def container_group():
            pass

    Args:
        name_or_func: Command name using dot notation for nesting (e.g., "container.status")
        description: Command description (defaults to docstring)
        aliases: Alternative names for the command
        hidden: Whether to hide from help listing
        category: Command category for grouping
        group: Whether this is a command group (not a command)
        replace: Whether to replace existing registration
        force_options: If True, all parameters with defaults become --options
                      (disables Position-Based Hybrid for first parameter)
        registry: Custom registry (defaults to global)
        **metadata: Additional metadata stored in CommandInfo.metadata

    Returns:
        Decorator function or decorated function

    """
    # Handle @register_command (without parens)
    if callable(name_or_func) and not isinstance(name_or_func, str):
        func = name_or_func
        return _register_command_func(
            func,
            name=None,
            description=description,
            aliases=aliases,
            hidden=hidden,
            category=category,
            group=group,
            replace=replace,
            registry=registry,
            **metadata,
        )

    # Handle @register_command(...) (with arguments)
    # At this point, name_or_func must be str | None (not F)
    name_str: str | None = name_or_func if isinstance(name_or_func, str) or name_or_func is None else None

    def decorator(func: F) -> F:
        return _register_command_func(
            func,
            name=name_str,
            description=description,
            aliases=aliases,
            hidden=None,
            category=category,
            group=group,
            replace=replace,
            registry=registry,
            **metadata,
        )

    return decorator


def x_register_command__mutmut_34(  # type: ignore[misc]
    name_or_func: str | F | None = None,
    *,
    description: str | None = None,
    aliases: list[str] | None = None,
    hidden: bool = False,
    category: str | None = None,
    group: bool = False,
    replace: bool = False,
    registry: Registry | None = None,
    **metadata: Any,
) -> Any:
    """Register a CLI command in the hub.

    Can be used as a decorator with or without arguments:

        @register_command
        def my_command():
            pass

        @register_command("custom-name", aliases=["cn"], category="utils")
        def my_command():
            pass

        # Nested commands using dot notation - groups are auto-created
        @register_command("container.status")
        def container_status():
            pass

        @register_command("container.volumes.backup")
        def container_volumes_backup():
            pass

        # Explicit group with custom description (optional)
        @register_command("container", group=True, description="Container management")
        def container_group():
            pass

    Args:
        name_or_func: Command name using dot notation for nesting (e.g., "container.status")
        description: Command description (defaults to docstring)
        aliases: Alternative names for the command
        hidden: Whether to hide from help listing
        category: Command category for grouping
        group: Whether this is a command group (not a command)
        replace: Whether to replace existing registration
        force_options: If True, all parameters with defaults become --options
                      (disables Position-Based Hybrid for first parameter)
        registry: Custom registry (defaults to global)
        **metadata: Additional metadata stored in CommandInfo.metadata

    Returns:
        Decorator function or decorated function

    """
    # Handle @register_command (without parens)
    if callable(name_or_func) and not isinstance(name_or_func, str):
        func = name_or_func
        return _register_command_func(
            func,
            name=None,
            description=description,
            aliases=aliases,
            hidden=hidden,
            category=category,
            group=group,
            replace=replace,
            registry=registry,
            **metadata,
        )

    # Handle @register_command(...) (with arguments)
    # At this point, name_or_func must be str | None (not F)
    name_str: str | None = name_or_func if isinstance(name_or_func, str) or name_or_func is None else None

    def decorator(func: F) -> F:
        return _register_command_func(
            func,
            name=name_str,
            description=description,
            aliases=aliases,
            hidden=hidden,
            category=None,
            group=group,
            replace=replace,
            registry=registry,
            **metadata,
        )

    return decorator


def x_register_command__mutmut_35(  # type: ignore[misc]
    name_or_func: str | F | None = None,
    *,
    description: str | None = None,
    aliases: list[str] | None = None,
    hidden: bool = False,
    category: str | None = None,
    group: bool = False,
    replace: bool = False,
    registry: Registry | None = None,
    **metadata: Any,
) -> Any:
    """Register a CLI command in the hub.

    Can be used as a decorator with or without arguments:

        @register_command
        def my_command():
            pass

        @register_command("custom-name", aliases=["cn"], category="utils")
        def my_command():
            pass

        # Nested commands using dot notation - groups are auto-created
        @register_command("container.status")
        def container_status():
            pass

        @register_command("container.volumes.backup")
        def container_volumes_backup():
            pass

        # Explicit group with custom description (optional)
        @register_command("container", group=True, description="Container management")
        def container_group():
            pass

    Args:
        name_or_func: Command name using dot notation for nesting (e.g., "container.status")
        description: Command description (defaults to docstring)
        aliases: Alternative names for the command
        hidden: Whether to hide from help listing
        category: Command category for grouping
        group: Whether this is a command group (not a command)
        replace: Whether to replace existing registration
        force_options: If True, all parameters with defaults become --options
                      (disables Position-Based Hybrid for first parameter)
        registry: Custom registry (defaults to global)
        **metadata: Additional metadata stored in CommandInfo.metadata

    Returns:
        Decorator function or decorated function

    """
    # Handle @register_command (without parens)
    if callable(name_or_func) and not isinstance(name_or_func, str):
        func = name_or_func
        return _register_command_func(
            func,
            name=None,
            description=description,
            aliases=aliases,
            hidden=hidden,
            category=category,
            group=group,
            replace=replace,
            registry=registry,
            **metadata,
        )

    # Handle @register_command(...) (with arguments)
    # At this point, name_or_func must be str | None (not F)
    name_str: str | None = name_or_func if isinstance(name_or_func, str) or name_or_func is None else None

    def decorator(func: F) -> F:
        return _register_command_func(
            func,
            name=name_str,
            description=description,
            aliases=aliases,
            hidden=hidden,
            category=category,
            group=None,
            replace=replace,
            registry=registry,
            **metadata,
        )

    return decorator


def x_register_command__mutmut_36(  # type: ignore[misc]
    name_or_func: str | F | None = None,
    *,
    description: str | None = None,
    aliases: list[str] | None = None,
    hidden: bool = False,
    category: str | None = None,
    group: bool = False,
    replace: bool = False,
    registry: Registry | None = None,
    **metadata: Any,
) -> Any:
    """Register a CLI command in the hub.

    Can be used as a decorator with or without arguments:

        @register_command
        def my_command():
            pass

        @register_command("custom-name", aliases=["cn"], category="utils")
        def my_command():
            pass

        # Nested commands using dot notation - groups are auto-created
        @register_command("container.status")
        def container_status():
            pass

        @register_command("container.volumes.backup")
        def container_volumes_backup():
            pass

        # Explicit group with custom description (optional)
        @register_command("container", group=True, description="Container management")
        def container_group():
            pass

    Args:
        name_or_func: Command name using dot notation for nesting (e.g., "container.status")
        description: Command description (defaults to docstring)
        aliases: Alternative names for the command
        hidden: Whether to hide from help listing
        category: Command category for grouping
        group: Whether this is a command group (not a command)
        replace: Whether to replace existing registration
        force_options: If True, all parameters with defaults become --options
                      (disables Position-Based Hybrid for first parameter)
        registry: Custom registry (defaults to global)
        **metadata: Additional metadata stored in CommandInfo.metadata

    Returns:
        Decorator function or decorated function

    """
    # Handle @register_command (without parens)
    if callable(name_or_func) and not isinstance(name_or_func, str):
        func = name_or_func
        return _register_command_func(
            func,
            name=None,
            description=description,
            aliases=aliases,
            hidden=hidden,
            category=category,
            group=group,
            replace=replace,
            registry=registry,
            **metadata,
        )

    # Handle @register_command(...) (with arguments)
    # At this point, name_or_func must be str | None (not F)
    name_str: str | None = name_or_func if isinstance(name_or_func, str) or name_or_func is None else None

    def decorator(func: F) -> F:
        return _register_command_func(
            func,
            name=name_str,
            description=description,
            aliases=aliases,
            hidden=hidden,
            category=category,
            group=group,
            replace=None,
            registry=registry,
            **metadata,
        )

    return decorator


def x_register_command__mutmut_37(  # type: ignore[misc]
    name_or_func: str | F | None = None,
    *,
    description: str | None = None,
    aliases: list[str] | None = None,
    hidden: bool = False,
    category: str | None = None,
    group: bool = False,
    replace: bool = False,
    registry: Registry | None = None,
    **metadata: Any,
) -> Any:
    """Register a CLI command in the hub.

    Can be used as a decorator with or without arguments:

        @register_command
        def my_command():
            pass

        @register_command("custom-name", aliases=["cn"], category="utils")
        def my_command():
            pass

        # Nested commands using dot notation - groups are auto-created
        @register_command("container.status")
        def container_status():
            pass

        @register_command("container.volumes.backup")
        def container_volumes_backup():
            pass

        # Explicit group with custom description (optional)
        @register_command("container", group=True, description="Container management")
        def container_group():
            pass

    Args:
        name_or_func: Command name using dot notation for nesting (e.g., "container.status")
        description: Command description (defaults to docstring)
        aliases: Alternative names for the command
        hidden: Whether to hide from help listing
        category: Command category for grouping
        group: Whether this is a command group (not a command)
        replace: Whether to replace existing registration
        force_options: If True, all parameters with defaults become --options
                      (disables Position-Based Hybrid for first parameter)
        registry: Custom registry (defaults to global)
        **metadata: Additional metadata stored in CommandInfo.metadata

    Returns:
        Decorator function or decorated function

    """
    # Handle @register_command (without parens)
    if callable(name_or_func) and not isinstance(name_or_func, str):
        func = name_or_func
        return _register_command_func(
            func,
            name=None,
            description=description,
            aliases=aliases,
            hidden=hidden,
            category=category,
            group=group,
            replace=replace,
            registry=registry,
            **metadata,
        )

    # Handle @register_command(...) (with arguments)
    # At this point, name_or_func must be str | None (not F)
    name_str: str | None = name_or_func if isinstance(name_or_func, str) or name_or_func is None else None

    def decorator(func: F) -> F:
        return _register_command_func(
            func,
            name=name_str,
            description=description,
            aliases=aliases,
            hidden=hidden,
            category=category,
            group=group,
            replace=replace,
            registry=None,
            **metadata,
        )

    return decorator


def x_register_command__mutmut_38(  # type: ignore[misc]
    name_or_func: str | F | None = None,
    *,
    description: str | None = None,
    aliases: list[str] | None = None,
    hidden: bool = False,
    category: str | None = None,
    group: bool = False,
    replace: bool = False,
    registry: Registry | None = None,
    **metadata: Any,
) -> Any:
    """Register a CLI command in the hub.

    Can be used as a decorator with or without arguments:

        @register_command
        def my_command():
            pass

        @register_command("custom-name", aliases=["cn"], category="utils")
        def my_command():
            pass

        # Nested commands using dot notation - groups are auto-created
        @register_command("container.status")
        def container_status():
            pass

        @register_command("container.volumes.backup")
        def container_volumes_backup():
            pass

        # Explicit group with custom description (optional)
        @register_command("container", group=True, description="Container management")
        def container_group():
            pass

    Args:
        name_or_func: Command name using dot notation for nesting (e.g., "container.status")
        description: Command description (defaults to docstring)
        aliases: Alternative names for the command
        hidden: Whether to hide from help listing
        category: Command category for grouping
        group: Whether this is a command group (not a command)
        replace: Whether to replace existing registration
        force_options: If True, all parameters with defaults become --options
                      (disables Position-Based Hybrid for first parameter)
        registry: Custom registry (defaults to global)
        **metadata: Additional metadata stored in CommandInfo.metadata

    Returns:
        Decorator function or decorated function

    """
    # Handle @register_command (without parens)
    if callable(name_or_func) and not isinstance(name_or_func, str):
        func = name_or_func
        return _register_command_func(
            func,
            name=None,
            description=description,
            aliases=aliases,
            hidden=hidden,
            category=category,
            group=group,
            replace=replace,
            registry=registry,
            **metadata,
        )

    # Handle @register_command(...) (with arguments)
    # At this point, name_or_func must be str | None (not F)
    name_str: str | None = name_or_func if isinstance(name_or_func, str) or name_or_func is None else None

    def decorator(func: F) -> F:
        return _register_command_func(
            name=name_str,
            description=description,
            aliases=aliases,
            hidden=hidden,
            category=category,
            group=group,
            replace=replace,
            registry=registry,
            **metadata,
        )

    return decorator


def x_register_command__mutmut_39(  # type: ignore[misc]
    name_or_func: str | F | None = None,
    *,
    description: str | None = None,
    aliases: list[str] | None = None,
    hidden: bool = False,
    category: str | None = None,
    group: bool = False,
    replace: bool = False,
    registry: Registry | None = None,
    **metadata: Any,
) -> Any:
    """Register a CLI command in the hub.

    Can be used as a decorator with or without arguments:

        @register_command
        def my_command():
            pass

        @register_command("custom-name", aliases=["cn"], category="utils")
        def my_command():
            pass

        # Nested commands using dot notation - groups are auto-created
        @register_command("container.status")
        def container_status():
            pass

        @register_command("container.volumes.backup")
        def container_volumes_backup():
            pass

        # Explicit group with custom description (optional)
        @register_command("container", group=True, description="Container management")
        def container_group():
            pass

    Args:
        name_or_func: Command name using dot notation for nesting (e.g., "container.status")
        description: Command description (defaults to docstring)
        aliases: Alternative names for the command
        hidden: Whether to hide from help listing
        category: Command category for grouping
        group: Whether this is a command group (not a command)
        replace: Whether to replace existing registration
        force_options: If True, all parameters with defaults become --options
                      (disables Position-Based Hybrid for first parameter)
        registry: Custom registry (defaults to global)
        **metadata: Additional metadata stored in CommandInfo.metadata

    Returns:
        Decorator function or decorated function

    """
    # Handle @register_command (without parens)
    if callable(name_or_func) and not isinstance(name_or_func, str):
        func = name_or_func
        return _register_command_func(
            func,
            name=None,
            description=description,
            aliases=aliases,
            hidden=hidden,
            category=category,
            group=group,
            replace=replace,
            registry=registry,
            **metadata,
        )

    # Handle @register_command(...) (with arguments)
    # At this point, name_or_func must be str | None (not F)
    name_str: str | None = name_or_func if isinstance(name_or_func, str) or name_or_func is None else None

    def decorator(func: F) -> F:
        return _register_command_func(
            func,
            description=description,
            aliases=aliases,
            hidden=hidden,
            category=category,
            group=group,
            replace=replace,
            registry=registry,
            **metadata,
        )

    return decorator


def x_register_command__mutmut_40(  # type: ignore[misc]
    name_or_func: str | F | None = None,
    *,
    description: str | None = None,
    aliases: list[str] | None = None,
    hidden: bool = False,
    category: str | None = None,
    group: bool = False,
    replace: bool = False,
    registry: Registry | None = None,
    **metadata: Any,
) -> Any:
    """Register a CLI command in the hub.

    Can be used as a decorator with or without arguments:

        @register_command
        def my_command():
            pass

        @register_command("custom-name", aliases=["cn"], category="utils")
        def my_command():
            pass

        # Nested commands using dot notation - groups are auto-created
        @register_command("container.status")
        def container_status():
            pass

        @register_command("container.volumes.backup")
        def container_volumes_backup():
            pass

        # Explicit group with custom description (optional)
        @register_command("container", group=True, description="Container management")
        def container_group():
            pass

    Args:
        name_or_func: Command name using dot notation for nesting (e.g., "container.status")
        description: Command description (defaults to docstring)
        aliases: Alternative names for the command
        hidden: Whether to hide from help listing
        category: Command category for grouping
        group: Whether this is a command group (not a command)
        replace: Whether to replace existing registration
        force_options: If True, all parameters with defaults become --options
                      (disables Position-Based Hybrid for first parameter)
        registry: Custom registry (defaults to global)
        **metadata: Additional metadata stored in CommandInfo.metadata

    Returns:
        Decorator function or decorated function

    """
    # Handle @register_command (without parens)
    if callable(name_or_func) and not isinstance(name_or_func, str):
        func = name_or_func
        return _register_command_func(
            func,
            name=None,
            description=description,
            aliases=aliases,
            hidden=hidden,
            category=category,
            group=group,
            replace=replace,
            registry=registry,
            **metadata,
        )

    # Handle @register_command(...) (with arguments)
    # At this point, name_or_func must be str | None (not F)
    name_str: str | None = name_or_func if isinstance(name_or_func, str) or name_or_func is None else None

    def decorator(func: F) -> F:
        return _register_command_func(
            func,
            name=name_str,
            aliases=aliases,
            hidden=hidden,
            category=category,
            group=group,
            replace=replace,
            registry=registry,
            **metadata,
        )

    return decorator


def x_register_command__mutmut_41(  # type: ignore[misc]
    name_or_func: str | F | None = None,
    *,
    description: str | None = None,
    aliases: list[str] | None = None,
    hidden: bool = False,
    category: str | None = None,
    group: bool = False,
    replace: bool = False,
    registry: Registry | None = None,
    **metadata: Any,
) -> Any:
    """Register a CLI command in the hub.

    Can be used as a decorator with or without arguments:

        @register_command
        def my_command():
            pass

        @register_command("custom-name", aliases=["cn"], category="utils")
        def my_command():
            pass

        # Nested commands using dot notation - groups are auto-created
        @register_command("container.status")
        def container_status():
            pass

        @register_command("container.volumes.backup")
        def container_volumes_backup():
            pass

        # Explicit group with custom description (optional)
        @register_command("container", group=True, description="Container management")
        def container_group():
            pass

    Args:
        name_or_func: Command name using dot notation for nesting (e.g., "container.status")
        description: Command description (defaults to docstring)
        aliases: Alternative names for the command
        hidden: Whether to hide from help listing
        category: Command category for grouping
        group: Whether this is a command group (not a command)
        replace: Whether to replace existing registration
        force_options: If True, all parameters with defaults become --options
                      (disables Position-Based Hybrid for first parameter)
        registry: Custom registry (defaults to global)
        **metadata: Additional metadata stored in CommandInfo.metadata

    Returns:
        Decorator function or decorated function

    """
    # Handle @register_command (without parens)
    if callable(name_or_func) and not isinstance(name_or_func, str):
        func = name_or_func
        return _register_command_func(
            func,
            name=None,
            description=description,
            aliases=aliases,
            hidden=hidden,
            category=category,
            group=group,
            replace=replace,
            registry=registry,
            **metadata,
        )

    # Handle @register_command(...) (with arguments)
    # At this point, name_or_func must be str | None (not F)
    name_str: str | None = name_or_func if isinstance(name_or_func, str) or name_or_func is None else None

    def decorator(func: F) -> F:
        return _register_command_func(
            func,
            name=name_str,
            description=description,
            hidden=hidden,
            category=category,
            group=group,
            replace=replace,
            registry=registry,
            **metadata,
        )

    return decorator


def x_register_command__mutmut_42(  # type: ignore[misc]
    name_or_func: str | F | None = None,
    *,
    description: str | None = None,
    aliases: list[str] | None = None,
    hidden: bool = False,
    category: str | None = None,
    group: bool = False,
    replace: bool = False,
    registry: Registry | None = None,
    **metadata: Any,
) -> Any:
    """Register a CLI command in the hub.

    Can be used as a decorator with or without arguments:

        @register_command
        def my_command():
            pass

        @register_command("custom-name", aliases=["cn"], category="utils")
        def my_command():
            pass

        # Nested commands using dot notation - groups are auto-created
        @register_command("container.status")
        def container_status():
            pass

        @register_command("container.volumes.backup")
        def container_volumes_backup():
            pass

        # Explicit group with custom description (optional)
        @register_command("container", group=True, description="Container management")
        def container_group():
            pass

    Args:
        name_or_func: Command name using dot notation for nesting (e.g., "container.status")
        description: Command description (defaults to docstring)
        aliases: Alternative names for the command
        hidden: Whether to hide from help listing
        category: Command category for grouping
        group: Whether this is a command group (not a command)
        replace: Whether to replace existing registration
        force_options: If True, all parameters with defaults become --options
                      (disables Position-Based Hybrid for first parameter)
        registry: Custom registry (defaults to global)
        **metadata: Additional metadata stored in CommandInfo.metadata

    Returns:
        Decorator function or decorated function

    """
    # Handle @register_command (without parens)
    if callable(name_or_func) and not isinstance(name_or_func, str):
        func = name_or_func
        return _register_command_func(
            func,
            name=None,
            description=description,
            aliases=aliases,
            hidden=hidden,
            category=category,
            group=group,
            replace=replace,
            registry=registry,
            **metadata,
        )

    # Handle @register_command(...) (with arguments)
    # At this point, name_or_func must be str | None (not F)
    name_str: str | None = name_or_func if isinstance(name_or_func, str) or name_or_func is None else None

    def decorator(func: F) -> F:
        return _register_command_func(
            func,
            name=name_str,
            description=description,
            aliases=aliases,
            category=category,
            group=group,
            replace=replace,
            registry=registry,
            **metadata,
        )

    return decorator


def x_register_command__mutmut_43(  # type: ignore[misc]
    name_or_func: str | F | None = None,
    *,
    description: str | None = None,
    aliases: list[str] | None = None,
    hidden: bool = False,
    category: str | None = None,
    group: bool = False,
    replace: bool = False,
    registry: Registry | None = None,
    **metadata: Any,
) -> Any:
    """Register a CLI command in the hub.

    Can be used as a decorator with or without arguments:

        @register_command
        def my_command():
            pass

        @register_command("custom-name", aliases=["cn"], category="utils")
        def my_command():
            pass

        # Nested commands using dot notation - groups are auto-created
        @register_command("container.status")
        def container_status():
            pass

        @register_command("container.volumes.backup")
        def container_volumes_backup():
            pass

        # Explicit group with custom description (optional)
        @register_command("container", group=True, description="Container management")
        def container_group():
            pass

    Args:
        name_or_func: Command name using dot notation for nesting (e.g., "container.status")
        description: Command description (defaults to docstring)
        aliases: Alternative names for the command
        hidden: Whether to hide from help listing
        category: Command category for grouping
        group: Whether this is a command group (not a command)
        replace: Whether to replace existing registration
        force_options: If True, all parameters with defaults become --options
                      (disables Position-Based Hybrid for first parameter)
        registry: Custom registry (defaults to global)
        **metadata: Additional metadata stored in CommandInfo.metadata

    Returns:
        Decorator function or decorated function

    """
    # Handle @register_command (without parens)
    if callable(name_or_func) and not isinstance(name_or_func, str):
        func = name_or_func
        return _register_command_func(
            func,
            name=None,
            description=description,
            aliases=aliases,
            hidden=hidden,
            category=category,
            group=group,
            replace=replace,
            registry=registry,
            **metadata,
        )

    # Handle @register_command(...) (with arguments)
    # At this point, name_or_func must be str | None (not F)
    name_str: str | None = name_or_func if isinstance(name_or_func, str) or name_or_func is None else None

    def decorator(func: F) -> F:
        return _register_command_func(
            func,
            name=name_str,
            description=description,
            aliases=aliases,
            hidden=hidden,
            group=group,
            replace=replace,
            registry=registry,
            **metadata,
        )

    return decorator


def x_register_command__mutmut_44(  # type: ignore[misc]
    name_or_func: str | F | None = None,
    *,
    description: str | None = None,
    aliases: list[str] | None = None,
    hidden: bool = False,
    category: str | None = None,
    group: bool = False,
    replace: bool = False,
    registry: Registry | None = None,
    **metadata: Any,
) -> Any:
    """Register a CLI command in the hub.

    Can be used as a decorator with or without arguments:

        @register_command
        def my_command():
            pass

        @register_command("custom-name", aliases=["cn"], category="utils")
        def my_command():
            pass

        # Nested commands using dot notation - groups are auto-created
        @register_command("container.status")
        def container_status():
            pass

        @register_command("container.volumes.backup")
        def container_volumes_backup():
            pass

        # Explicit group with custom description (optional)
        @register_command("container", group=True, description="Container management")
        def container_group():
            pass

    Args:
        name_or_func: Command name using dot notation for nesting (e.g., "container.status")
        description: Command description (defaults to docstring)
        aliases: Alternative names for the command
        hidden: Whether to hide from help listing
        category: Command category for grouping
        group: Whether this is a command group (not a command)
        replace: Whether to replace existing registration
        force_options: If True, all parameters with defaults become --options
                      (disables Position-Based Hybrid for first parameter)
        registry: Custom registry (defaults to global)
        **metadata: Additional metadata stored in CommandInfo.metadata

    Returns:
        Decorator function or decorated function

    """
    # Handle @register_command (without parens)
    if callable(name_or_func) and not isinstance(name_or_func, str):
        func = name_or_func
        return _register_command_func(
            func,
            name=None,
            description=description,
            aliases=aliases,
            hidden=hidden,
            category=category,
            group=group,
            replace=replace,
            registry=registry,
            **metadata,
        )

    # Handle @register_command(...) (with arguments)
    # At this point, name_or_func must be str | None (not F)
    name_str: str | None = name_or_func if isinstance(name_or_func, str) or name_or_func is None else None

    def decorator(func: F) -> F:
        return _register_command_func(
            func,
            name=name_str,
            description=description,
            aliases=aliases,
            hidden=hidden,
            category=category,
            replace=replace,
            registry=registry,
            **metadata,
        )

    return decorator


def x_register_command__mutmut_45(  # type: ignore[misc]
    name_or_func: str | F | None = None,
    *,
    description: str | None = None,
    aliases: list[str] | None = None,
    hidden: bool = False,
    category: str | None = None,
    group: bool = False,
    replace: bool = False,
    registry: Registry | None = None,
    **metadata: Any,
) -> Any:
    """Register a CLI command in the hub.

    Can be used as a decorator with or without arguments:

        @register_command
        def my_command():
            pass

        @register_command("custom-name", aliases=["cn"], category="utils")
        def my_command():
            pass

        # Nested commands using dot notation - groups are auto-created
        @register_command("container.status")
        def container_status():
            pass

        @register_command("container.volumes.backup")
        def container_volumes_backup():
            pass

        # Explicit group with custom description (optional)
        @register_command("container", group=True, description="Container management")
        def container_group():
            pass

    Args:
        name_or_func: Command name using dot notation for nesting (e.g., "container.status")
        description: Command description (defaults to docstring)
        aliases: Alternative names for the command
        hidden: Whether to hide from help listing
        category: Command category for grouping
        group: Whether this is a command group (not a command)
        replace: Whether to replace existing registration
        force_options: If True, all parameters with defaults become --options
                      (disables Position-Based Hybrid for first parameter)
        registry: Custom registry (defaults to global)
        **metadata: Additional metadata stored in CommandInfo.metadata

    Returns:
        Decorator function or decorated function

    """
    # Handle @register_command (without parens)
    if callable(name_or_func) and not isinstance(name_or_func, str):
        func = name_or_func
        return _register_command_func(
            func,
            name=None,
            description=description,
            aliases=aliases,
            hidden=hidden,
            category=category,
            group=group,
            replace=replace,
            registry=registry,
            **metadata,
        )

    # Handle @register_command(...) (with arguments)
    # At this point, name_or_func must be str | None (not F)
    name_str: str | None = name_or_func if isinstance(name_or_func, str) or name_or_func is None else None

    def decorator(func: F) -> F:
        return _register_command_func(
            func,
            name=name_str,
            description=description,
            aliases=aliases,
            hidden=hidden,
            category=category,
            group=group,
            registry=registry,
            **metadata,
        )

    return decorator


def x_register_command__mutmut_46(  # type: ignore[misc]
    name_or_func: str | F | None = None,
    *,
    description: str | None = None,
    aliases: list[str] | None = None,
    hidden: bool = False,
    category: str | None = None,
    group: bool = False,
    replace: bool = False,
    registry: Registry | None = None,
    **metadata: Any,
) -> Any:
    """Register a CLI command in the hub.

    Can be used as a decorator with or without arguments:

        @register_command
        def my_command():
            pass

        @register_command("custom-name", aliases=["cn"], category="utils")
        def my_command():
            pass

        # Nested commands using dot notation - groups are auto-created
        @register_command("container.status")
        def container_status():
            pass

        @register_command("container.volumes.backup")
        def container_volumes_backup():
            pass

        # Explicit group with custom description (optional)
        @register_command("container", group=True, description="Container management")
        def container_group():
            pass

    Args:
        name_or_func: Command name using dot notation for nesting (e.g., "container.status")
        description: Command description (defaults to docstring)
        aliases: Alternative names for the command
        hidden: Whether to hide from help listing
        category: Command category for grouping
        group: Whether this is a command group (not a command)
        replace: Whether to replace existing registration
        force_options: If True, all parameters with defaults become --options
                      (disables Position-Based Hybrid for first parameter)
        registry: Custom registry (defaults to global)
        **metadata: Additional metadata stored in CommandInfo.metadata

    Returns:
        Decorator function or decorated function

    """
    # Handle @register_command (without parens)
    if callable(name_or_func) and not isinstance(name_or_func, str):
        func = name_or_func
        return _register_command_func(
            func,
            name=None,
            description=description,
            aliases=aliases,
            hidden=hidden,
            category=category,
            group=group,
            replace=replace,
            registry=registry,
            **metadata,
        )

    # Handle @register_command(...) (with arguments)
    # At this point, name_or_func must be str | None (not F)
    name_str: str | None = name_or_func if isinstance(name_or_func, str) or name_or_func is None else None

    def decorator(func: F) -> F:
        return _register_command_func(
            func,
            name=name_str,
            description=description,
            aliases=aliases,
            hidden=hidden,
            category=category,
            group=group,
            replace=replace,
            **metadata,
        )

    return decorator


def x_register_command__mutmut_47(  # type: ignore[misc]
    name_or_func: str | F | None = None,
    *,
    description: str | None = None,
    aliases: list[str] | None = None,
    hidden: bool = False,
    category: str | None = None,
    group: bool = False,
    replace: bool = False,
    registry: Registry | None = None,
    **metadata: Any,
) -> Any:
    """Register a CLI command in the hub.

    Can be used as a decorator with or without arguments:

        @register_command
        def my_command():
            pass

        @register_command("custom-name", aliases=["cn"], category="utils")
        def my_command():
            pass

        # Nested commands using dot notation - groups are auto-created
        @register_command("container.status")
        def container_status():
            pass

        @register_command("container.volumes.backup")
        def container_volumes_backup():
            pass

        # Explicit group with custom description (optional)
        @register_command("container", group=True, description="Container management")
        def container_group():
            pass

    Args:
        name_or_func: Command name using dot notation for nesting (e.g., "container.status")
        description: Command description (defaults to docstring)
        aliases: Alternative names for the command
        hidden: Whether to hide from help listing
        category: Command category for grouping
        group: Whether this is a command group (not a command)
        replace: Whether to replace existing registration
        force_options: If True, all parameters with defaults become --options
                      (disables Position-Based Hybrid for first parameter)
        registry: Custom registry (defaults to global)
        **metadata: Additional metadata stored in CommandInfo.metadata

    Returns:
        Decorator function or decorated function

    """
    # Handle @register_command (without parens)
    if callable(name_or_func) and not isinstance(name_or_func, str):
        func = name_or_func
        return _register_command_func(
            func,
            name=None,
            description=description,
            aliases=aliases,
            hidden=hidden,
            category=category,
            group=group,
            replace=replace,
            registry=registry,
            **metadata,
        )

    # Handle @register_command(...) (with arguments)
    # At this point, name_or_func must be str | None (not F)
    name_str: str | None = name_or_func if isinstance(name_or_func, str) or name_or_func is None else None

    def decorator(func: F) -> F:
        return _register_command_func(
            func,
            name=name_str,
            description=description,
            aliases=aliases,
            hidden=hidden,
            category=category,
            group=group,
            replace=replace,
            registry=registry,
        )

    return decorator


x_register_command__mutmut_mutants: ClassVar[MutantDict] = {
    "x_register_command__mutmut_1": x_register_command__mutmut_1,
    "x_register_command__mutmut_2": x_register_command__mutmut_2,
    "x_register_command__mutmut_3": x_register_command__mutmut_3,
    "x_register_command__mutmut_4": x_register_command__mutmut_4,
    "x_register_command__mutmut_5": x_register_command__mutmut_5,
    "x_register_command__mutmut_6": x_register_command__mutmut_6,
    "x_register_command__mutmut_7": x_register_command__mutmut_7,
    "x_register_command__mutmut_8": x_register_command__mutmut_8,
    "x_register_command__mutmut_9": x_register_command__mutmut_9,
    "x_register_command__mutmut_10": x_register_command__mutmut_10,
    "x_register_command__mutmut_11": x_register_command__mutmut_11,
    "x_register_command__mutmut_12": x_register_command__mutmut_12,
    "x_register_command__mutmut_13": x_register_command__mutmut_13,
    "x_register_command__mutmut_14": x_register_command__mutmut_14,
    "x_register_command__mutmut_15": x_register_command__mutmut_15,
    "x_register_command__mutmut_16": x_register_command__mutmut_16,
    "x_register_command__mutmut_17": x_register_command__mutmut_17,
    "x_register_command__mutmut_18": x_register_command__mutmut_18,
    "x_register_command__mutmut_19": x_register_command__mutmut_19,
    "x_register_command__mutmut_20": x_register_command__mutmut_20,
    "x_register_command__mutmut_21": x_register_command__mutmut_21,
    "x_register_command__mutmut_22": x_register_command__mutmut_22,
    "x_register_command__mutmut_23": x_register_command__mutmut_23,
    "x_register_command__mutmut_24": x_register_command__mutmut_24,
    "x_register_command__mutmut_25": x_register_command__mutmut_25,
    "x_register_command__mutmut_26": x_register_command__mutmut_26,
    "x_register_command__mutmut_27": x_register_command__mutmut_27,
    "x_register_command__mutmut_28": x_register_command__mutmut_28,
    "x_register_command__mutmut_29": x_register_command__mutmut_29,
    "x_register_command__mutmut_30": x_register_command__mutmut_30,
    "x_register_command__mutmut_31": x_register_command__mutmut_31,
    "x_register_command__mutmut_32": x_register_command__mutmut_32,
    "x_register_command__mutmut_33": x_register_command__mutmut_33,
    "x_register_command__mutmut_34": x_register_command__mutmut_34,
    "x_register_command__mutmut_35": x_register_command__mutmut_35,
    "x_register_command__mutmut_36": x_register_command__mutmut_36,
    "x_register_command__mutmut_37": x_register_command__mutmut_37,
    "x_register_command__mutmut_38": x_register_command__mutmut_38,
    "x_register_command__mutmut_39": x_register_command__mutmut_39,
    "x_register_command__mutmut_40": x_register_command__mutmut_40,
    "x_register_command__mutmut_41": x_register_command__mutmut_41,
    "x_register_command__mutmut_42": x_register_command__mutmut_42,
    "x_register_command__mutmut_43": x_register_command__mutmut_43,
    "x_register_command__mutmut_44": x_register_command__mutmut_44,
    "x_register_command__mutmut_45": x_register_command__mutmut_45,
    "x_register_command__mutmut_46": x_register_command__mutmut_46,
    "x_register_command__mutmut_47": x_register_command__mutmut_47,
}


def register_command(*args, **kwargs):
    result = _mutmut_trampoline(
        x_register_command__mutmut_orig, x_register_command__mutmut_mutants, args, kwargs
    )
    return result


register_command.__signature__ = _mutmut_signature(x_register_command__mutmut_orig)
x_register_command__mutmut_orig.__name__ = "x_register_command"


def x__register_command_func__mutmut_orig(
    func: F,
    *,
    name: str | None = None,
    description: str | None = None,
    aliases: list[str] | None = None,
    hidden: bool = False,
    category: str | None = None,
    group: bool = False,
    replace: bool = False,
    registry: Registry | None = None,
    **extra_metadata: Any,
) -> F:
    """Internal function to register a command."""
    reg = registry or get_command_registry()

    # Determine command name and parent from dot notation
    if name:
        parts = name.split(".")
        if len(parts) > 1:
            # Extract parent path and command name
            parent = ".".join(parts[:-1])
            command_name = parts[-1]

            # Auto-create parent groups if they don't exist (click only)
            _, has_click = _get_click()
            if has_click:
                ensure_parent_groups_fn = _get_ensure_parent_groups()
                if ensure_parent_groups_fn:
                    ensure_parent_groups_fn(parent, reg)
        else:
            parent = None
            command_name = name
    else:
        # Use function name as command name
        parent = None
        command_name = getattr(func, "__name__", "<anonymous>")

    # Check if it's already a Click command
    click_cmd = None
    click_module, has_click = _get_click()
    if has_click and isinstance(func, click_module.Command):
        click_cmd = func
        actual_func = func.callback
    else:
        actual_func = func

    # Create command info
    cmd_metadata = {"is_group": group}
    cmd_metadata.update(extra_metadata)

    info = CommandInfo(
        name=command_name,
        func=actual_func,
        description=description or (actual_func.__doc__ if actual_func else None),
        aliases=aliases or [],
        hidden=hidden,
        category=category,
        metadata=cmd_metadata,
        parent=parent,
    )

    # Build full registry key
    full_name = f"{parent}.{command_name}" if parent else command_name

    # Build registry metadata
    reg_metadata = {
        "info": info,
        "description": info.description,
        "aliases": info.aliases,
        "hidden": hidden,
        "category": category,
        "parent": parent,
        "is_group": group,
        "_prebuilt_click_command": click_cmd,  # Use new, clearer name
    }
    reg_metadata.update(extra_metadata)

    # Register in the registry
    reg.register(
        name=full_name,
        value=func,
        dimension=ComponentCategory.COMMAND.value,
        metadata=reg_metadata,
        aliases=aliases,
        replace=replace,
    )

    # Add metadata to the function
    func.__registry_name__ = command_name  # type: ignore[attr-defined]
    func.__registry_dimension__ = ComponentCategory.COMMAND.value  # type: ignore[attr-defined]
    func.__registry_info__ = info  # type: ignore[attr-defined]

    get_foundation_logger().trace(f"Registered command: {full_name}")

    return func


def x__register_command_func__mutmut_1(
    func: F,
    *,
    name: str | None = None,
    description: str | None = None,
    aliases: list[str] | None = None,
    hidden: bool = True,
    category: str | None = None,
    group: bool = False,
    replace: bool = False,
    registry: Registry | None = None,
    **extra_metadata: Any,
) -> F:
    """Internal function to register a command."""
    reg = registry or get_command_registry()

    # Determine command name and parent from dot notation
    if name:
        parts = name.split(".")
        if len(parts) > 1:
            # Extract parent path and command name
            parent = ".".join(parts[:-1])
            command_name = parts[-1]

            # Auto-create parent groups if they don't exist (click only)
            _, has_click = _get_click()
            if has_click:
                ensure_parent_groups_fn = _get_ensure_parent_groups()
                if ensure_parent_groups_fn:
                    ensure_parent_groups_fn(parent, reg)
        else:
            parent = None
            command_name = name
    else:
        # Use function name as command name
        parent = None
        command_name = getattr(func, "__name__", "<anonymous>")

    # Check if it's already a Click command
    click_cmd = None
    click_module, has_click = _get_click()
    if has_click and isinstance(func, click_module.Command):
        click_cmd = func
        actual_func = func.callback
    else:
        actual_func = func

    # Create command info
    cmd_metadata = {"is_group": group}
    cmd_metadata.update(extra_metadata)

    info = CommandInfo(
        name=command_name,
        func=actual_func,
        description=description or (actual_func.__doc__ if actual_func else None),
        aliases=aliases or [],
        hidden=hidden,
        category=category,
        metadata=cmd_metadata,
        parent=parent,
    )

    # Build full registry key
    full_name = f"{parent}.{command_name}" if parent else command_name

    # Build registry metadata
    reg_metadata = {
        "info": info,
        "description": info.description,
        "aliases": info.aliases,
        "hidden": hidden,
        "category": category,
        "parent": parent,
        "is_group": group,
        "_prebuilt_click_command": click_cmd,  # Use new, clearer name
    }
    reg_metadata.update(extra_metadata)

    # Register in the registry
    reg.register(
        name=full_name,
        value=func,
        dimension=ComponentCategory.COMMAND.value,
        metadata=reg_metadata,
        aliases=aliases,
        replace=replace,
    )

    # Add metadata to the function
    func.__registry_name__ = command_name  # type: ignore[attr-defined]
    func.__registry_dimension__ = ComponentCategory.COMMAND.value  # type: ignore[attr-defined]
    func.__registry_info__ = info  # type: ignore[attr-defined]

    get_foundation_logger().trace(f"Registered command: {full_name}")

    return func


def x__register_command_func__mutmut_2(
    func: F,
    *,
    name: str | None = None,
    description: str | None = None,
    aliases: list[str] | None = None,
    hidden: bool = False,
    category: str | None = None,
    group: bool = True,
    replace: bool = False,
    registry: Registry | None = None,
    **extra_metadata: Any,
) -> F:
    """Internal function to register a command."""
    reg = registry or get_command_registry()

    # Determine command name and parent from dot notation
    if name:
        parts = name.split(".")
        if len(parts) > 1:
            # Extract parent path and command name
            parent = ".".join(parts[:-1])
            command_name = parts[-1]

            # Auto-create parent groups if they don't exist (click only)
            _, has_click = _get_click()
            if has_click:
                ensure_parent_groups_fn = _get_ensure_parent_groups()
                if ensure_parent_groups_fn:
                    ensure_parent_groups_fn(parent, reg)
        else:
            parent = None
            command_name = name
    else:
        # Use function name as command name
        parent = None
        command_name = getattr(func, "__name__", "<anonymous>")

    # Check if it's already a Click command
    click_cmd = None
    click_module, has_click = _get_click()
    if has_click and isinstance(func, click_module.Command):
        click_cmd = func
        actual_func = func.callback
    else:
        actual_func = func

    # Create command info
    cmd_metadata = {"is_group": group}
    cmd_metadata.update(extra_metadata)

    info = CommandInfo(
        name=command_name,
        func=actual_func,
        description=description or (actual_func.__doc__ if actual_func else None),
        aliases=aliases or [],
        hidden=hidden,
        category=category,
        metadata=cmd_metadata,
        parent=parent,
    )

    # Build full registry key
    full_name = f"{parent}.{command_name}" if parent else command_name

    # Build registry metadata
    reg_metadata = {
        "info": info,
        "description": info.description,
        "aliases": info.aliases,
        "hidden": hidden,
        "category": category,
        "parent": parent,
        "is_group": group,
        "_prebuilt_click_command": click_cmd,  # Use new, clearer name
    }
    reg_metadata.update(extra_metadata)

    # Register in the registry
    reg.register(
        name=full_name,
        value=func,
        dimension=ComponentCategory.COMMAND.value,
        metadata=reg_metadata,
        aliases=aliases,
        replace=replace,
    )

    # Add metadata to the function
    func.__registry_name__ = command_name  # type: ignore[attr-defined]
    func.__registry_dimension__ = ComponentCategory.COMMAND.value  # type: ignore[attr-defined]
    func.__registry_info__ = info  # type: ignore[attr-defined]

    get_foundation_logger().trace(f"Registered command: {full_name}")

    return func


def x__register_command_func__mutmut_3(
    func: F,
    *,
    name: str | None = None,
    description: str | None = None,
    aliases: list[str] | None = None,
    hidden: bool = False,
    category: str | None = None,
    group: bool = False,
    replace: bool = True,
    registry: Registry | None = None,
    **extra_metadata: Any,
) -> F:
    """Internal function to register a command."""
    reg = registry or get_command_registry()

    # Determine command name and parent from dot notation
    if name:
        parts = name.split(".")
        if len(parts) > 1:
            # Extract parent path and command name
            parent = ".".join(parts[:-1])
            command_name = parts[-1]

            # Auto-create parent groups if they don't exist (click only)
            _, has_click = _get_click()
            if has_click:
                ensure_parent_groups_fn = _get_ensure_parent_groups()
                if ensure_parent_groups_fn:
                    ensure_parent_groups_fn(parent, reg)
        else:
            parent = None
            command_name = name
    else:
        # Use function name as command name
        parent = None
        command_name = getattr(func, "__name__", "<anonymous>")

    # Check if it's already a Click command
    click_cmd = None
    click_module, has_click = _get_click()
    if has_click and isinstance(func, click_module.Command):
        click_cmd = func
        actual_func = func.callback
    else:
        actual_func = func

    # Create command info
    cmd_metadata = {"is_group": group}
    cmd_metadata.update(extra_metadata)

    info = CommandInfo(
        name=command_name,
        func=actual_func,
        description=description or (actual_func.__doc__ if actual_func else None),
        aliases=aliases or [],
        hidden=hidden,
        category=category,
        metadata=cmd_metadata,
        parent=parent,
    )

    # Build full registry key
    full_name = f"{parent}.{command_name}" if parent else command_name

    # Build registry metadata
    reg_metadata = {
        "info": info,
        "description": info.description,
        "aliases": info.aliases,
        "hidden": hidden,
        "category": category,
        "parent": parent,
        "is_group": group,
        "_prebuilt_click_command": click_cmd,  # Use new, clearer name
    }
    reg_metadata.update(extra_metadata)

    # Register in the registry
    reg.register(
        name=full_name,
        value=func,
        dimension=ComponentCategory.COMMAND.value,
        metadata=reg_metadata,
        aliases=aliases,
        replace=replace,
    )

    # Add metadata to the function
    func.__registry_name__ = command_name  # type: ignore[attr-defined]
    func.__registry_dimension__ = ComponentCategory.COMMAND.value  # type: ignore[attr-defined]
    func.__registry_info__ = info  # type: ignore[attr-defined]

    get_foundation_logger().trace(f"Registered command: {full_name}")

    return func


def x__register_command_func__mutmut_4(
    func: F,
    *,
    name: str | None = None,
    description: str | None = None,
    aliases: list[str] | None = None,
    hidden: bool = False,
    category: str | None = None,
    group: bool = False,
    replace: bool = False,
    registry: Registry | None = None,
    **extra_metadata: Any,
) -> F:
    """Internal function to register a command."""
    reg = None

    # Determine command name and parent from dot notation
    if name:
        parts = name.split(".")
        if len(parts) > 1:
            # Extract parent path and command name
            parent = ".".join(parts[:-1])
            command_name = parts[-1]

            # Auto-create parent groups if they don't exist (click only)
            _, has_click = _get_click()
            if has_click:
                ensure_parent_groups_fn = _get_ensure_parent_groups()
                if ensure_parent_groups_fn:
                    ensure_parent_groups_fn(parent, reg)
        else:
            parent = None
            command_name = name
    else:
        # Use function name as command name
        parent = None
        command_name = getattr(func, "__name__", "<anonymous>")

    # Check if it's already a Click command
    click_cmd = None
    click_module, has_click = _get_click()
    if has_click and isinstance(func, click_module.Command):
        click_cmd = func
        actual_func = func.callback
    else:
        actual_func = func

    # Create command info
    cmd_metadata = {"is_group": group}
    cmd_metadata.update(extra_metadata)

    info = CommandInfo(
        name=command_name,
        func=actual_func,
        description=description or (actual_func.__doc__ if actual_func else None),
        aliases=aliases or [],
        hidden=hidden,
        category=category,
        metadata=cmd_metadata,
        parent=parent,
    )

    # Build full registry key
    full_name = f"{parent}.{command_name}" if parent else command_name

    # Build registry metadata
    reg_metadata = {
        "info": info,
        "description": info.description,
        "aliases": info.aliases,
        "hidden": hidden,
        "category": category,
        "parent": parent,
        "is_group": group,
        "_prebuilt_click_command": click_cmd,  # Use new, clearer name
    }
    reg_metadata.update(extra_metadata)

    # Register in the registry
    reg.register(
        name=full_name,
        value=func,
        dimension=ComponentCategory.COMMAND.value,
        metadata=reg_metadata,
        aliases=aliases,
        replace=replace,
    )

    # Add metadata to the function
    func.__registry_name__ = command_name  # type: ignore[attr-defined]
    func.__registry_dimension__ = ComponentCategory.COMMAND.value  # type: ignore[attr-defined]
    func.__registry_info__ = info  # type: ignore[attr-defined]

    get_foundation_logger().trace(f"Registered command: {full_name}")

    return func


def x__register_command_func__mutmut_5(
    func: F,
    *,
    name: str | None = None,
    description: str | None = None,
    aliases: list[str] | None = None,
    hidden: bool = False,
    category: str | None = None,
    group: bool = False,
    replace: bool = False,
    registry: Registry | None = None,
    **extra_metadata: Any,
) -> F:
    """Internal function to register a command."""
    reg = registry and get_command_registry()

    # Determine command name and parent from dot notation
    if name:
        parts = name.split(".")
        if len(parts) > 1:
            # Extract parent path and command name
            parent = ".".join(parts[:-1])
            command_name = parts[-1]

            # Auto-create parent groups if they don't exist (click only)
            _, has_click = _get_click()
            if has_click:
                ensure_parent_groups_fn = _get_ensure_parent_groups()
                if ensure_parent_groups_fn:
                    ensure_parent_groups_fn(parent, reg)
        else:
            parent = None
            command_name = name
    else:
        # Use function name as command name
        parent = None
        command_name = getattr(func, "__name__", "<anonymous>")

    # Check if it's already a Click command
    click_cmd = None
    click_module, has_click = _get_click()
    if has_click and isinstance(func, click_module.Command):
        click_cmd = func
        actual_func = func.callback
    else:
        actual_func = func

    # Create command info
    cmd_metadata = {"is_group": group}
    cmd_metadata.update(extra_metadata)

    info = CommandInfo(
        name=command_name,
        func=actual_func,
        description=description or (actual_func.__doc__ if actual_func else None),
        aliases=aliases or [],
        hidden=hidden,
        category=category,
        metadata=cmd_metadata,
        parent=parent,
    )

    # Build full registry key
    full_name = f"{parent}.{command_name}" if parent else command_name

    # Build registry metadata
    reg_metadata = {
        "info": info,
        "description": info.description,
        "aliases": info.aliases,
        "hidden": hidden,
        "category": category,
        "parent": parent,
        "is_group": group,
        "_prebuilt_click_command": click_cmd,  # Use new, clearer name
    }
    reg_metadata.update(extra_metadata)

    # Register in the registry
    reg.register(
        name=full_name,
        value=func,
        dimension=ComponentCategory.COMMAND.value,
        metadata=reg_metadata,
        aliases=aliases,
        replace=replace,
    )

    # Add metadata to the function
    func.__registry_name__ = command_name  # type: ignore[attr-defined]
    func.__registry_dimension__ = ComponentCategory.COMMAND.value  # type: ignore[attr-defined]
    func.__registry_info__ = info  # type: ignore[attr-defined]

    get_foundation_logger().trace(f"Registered command: {full_name}")

    return func


def x__register_command_func__mutmut_6(
    func: F,
    *,
    name: str | None = None,
    description: str | None = None,
    aliases: list[str] | None = None,
    hidden: bool = False,
    category: str | None = None,
    group: bool = False,
    replace: bool = False,
    registry: Registry | None = None,
    **extra_metadata: Any,
) -> F:
    """Internal function to register a command."""
    reg = registry or get_command_registry()

    # Determine command name and parent from dot notation
    if name:
        parts = None
        if len(parts) > 1:
            # Extract parent path and command name
            parent = ".".join(parts[:-1])
            command_name = parts[-1]

            # Auto-create parent groups if they don't exist (click only)
            _, has_click = _get_click()
            if has_click:
                ensure_parent_groups_fn = _get_ensure_parent_groups()
                if ensure_parent_groups_fn:
                    ensure_parent_groups_fn(parent, reg)
        else:
            parent = None
            command_name = name
    else:
        # Use function name as command name
        parent = None
        command_name = getattr(func, "__name__", "<anonymous>")

    # Check if it's already a Click command
    click_cmd = None
    click_module, has_click = _get_click()
    if has_click and isinstance(func, click_module.Command):
        click_cmd = func
        actual_func = func.callback
    else:
        actual_func = func

    # Create command info
    cmd_metadata = {"is_group": group}
    cmd_metadata.update(extra_metadata)

    info = CommandInfo(
        name=command_name,
        func=actual_func,
        description=description or (actual_func.__doc__ if actual_func else None),
        aliases=aliases or [],
        hidden=hidden,
        category=category,
        metadata=cmd_metadata,
        parent=parent,
    )

    # Build full registry key
    full_name = f"{parent}.{command_name}" if parent else command_name

    # Build registry metadata
    reg_metadata = {
        "info": info,
        "description": info.description,
        "aliases": info.aliases,
        "hidden": hidden,
        "category": category,
        "parent": parent,
        "is_group": group,
        "_prebuilt_click_command": click_cmd,  # Use new, clearer name
    }
    reg_metadata.update(extra_metadata)

    # Register in the registry
    reg.register(
        name=full_name,
        value=func,
        dimension=ComponentCategory.COMMAND.value,
        metadata=reg_metadata,
        aliases=aliases,
        replace=replace,
    )

    # Add metadata to the function
    func.__registry_name__ = command_name  # type: ignore[attr-defined]
    func.__registry_dimension__ = ComponentCategory.COMMAND.value  # type: ignore[attr-defined]
    func.__registry_info__ = info  # type: ignore[attr-defined]

    get_foundation_logger().trace(f"Registered command: {full_name}")

    return func


def x__register_command_func__mutmut_7(
    func: F,
    *,
    name: str | None = None,
    description: str | None = None,
    aliases: list[str] | None = None,
    hidden: bool = False,
    category: str | None = None,
    group: bool = False,
    replace: bool = False,
    registry: Registry | None = None,
    **extra_metadata: Any,
) -> F:
    """Internal function to register a command."""
    reg = registry or get_command_registry()

    # Determine command name and parent from dot notation
    if name:
        parts = name.split(None)
        if len(parts) > 1:
            # Extract parent path and command name
            parent = ".".join(parts[:-1])
            command_name = parts[-1]

            # Auto-create parent groups if they don't exist (click only)
            _, has_click = _get_click()
            if has_click:
                ensure_parent_groups_fn = _get_ensure_parent_groups()
                if ensure_parent_groups_fn:
                    ensure_parent_groups_fn(parent, reg)
        else:
            parent = None
            command_name = name
    else:
        # Use function name as command name
        parent = None
        command_name = getattr(func, "__name__", "<anonymous>")

    # Check if it's already a Click command
    click_cmd = None
    click_module, has_click = _get_click()
    if has_click and isinstance(func, click_module.Command):
        click_cmd = func
        actual_func = func.callback
    else:
        actual_func = func

    # Create command info
    cmd_metadata = {"is_group": group}
    cmd_metadata.update(extra_metadata)

    info = CommandInfo(
        name=command_name,
        func=actual_func,
        description=description or (actual_func.__doc__ if actual_func else None),
        aliases=aliases or [],
        hidden=hidden,
        category=category,
        metadata=cmd_metadata,
        parent=parent,
    )

    # Build full registry key
    full_name = f"{parent}.{command_name}" if parent else command_name

    # Build registry metadata
    reg_metadata = {
        "info": info,
        "description": info.description,
        "aliases": info.aliases,
        "hidden": hidden,
        "category": category,
        "parent": parent,
        "is_group": group,
        "_prebuilt_click_command": click_cmd,  # Use new, clearer name
    }
    reg_metadata.update(extra_metadata)

    # Register in the registry
    reg.register(
        name=full_name,
        value=func,
        dimension=ComponentCategory.COMMAND.value,
        metadata=reg_metadata,
        aliases=aliases,
        replace=replace,
    )

    # Add metadata to the function
    func.__registry_name__ = command_name  # type: ignore[attr-defined]
    func.__registry_dimension__ = ComponentCategory.COMMAND.value  # type: ignore[attr-defined]
    func.__registry_info__ = info  # type: ignore[attr-defined]

    get_foundation_logger().trace(f"Registered command: {full_name}")

    return func


def x__register_command_func__mutmut_8(
    func: F,
    *,
    name: str | None = None,
    description: str | None = None,
    aliases: list[str] | None = None,
    hidden: bool = False,
    category: str | None = None,
    group: bool = False,
    replace: bool = False,
    registry: Registry | None = None,
    **extra_metadata: Any,
) -> F:
    """Internal function to register a command."""
    reg = registry or get_command_registry()

    # Determine command name and parent from dot notation
    if name:
        parts = name.split("XX.XX")
        if len(parts) > 1:
            # Extract parent path and command name
            parent = ".".join(parts[:-1])
            command_name = parts[-1]

            # Auto-create parent groups if they don't exist (click only)
            _, has_click = _get_click()
            if has_click:
                ensure_parent_groups_fn = _get_ensure_parent_groups()
                if ensure_parent_groups_fn:
                    ensure_parent_groups_fn(parent, reg)
        else:
            parent = None
            command_name = name
    else:
        # Use function name as command name
        parent = None
        command_name = getattr(func, "__name__", "<anonymous>")

    # Check if it's already a Click command
    click_cmd = None
    click_module, has_click = _get_click()
    if has_click and isinstance(func, click_module.Command):
        click_cmd = func
        actual_func = func.callback
    else:
        actual_func = func

    # Create command info
    cmd_metadata = {"is_group": group}
    cmd_metadata.update(extra_metadata)

    info = CommandInfo(
        name=command_name,
        func=actual_func,
        description=description or (actual_func.__doc__ if actual_func else None),
        aliases=aliases or [],
        hidden=hidden,
        category=category,
        metadata=cmd_metadata,
        parent=parent,
    )

    # Build full registry key
    full_name = f"{parent}.{command_name}" if parent else command_name

    # Build registry metadata
    reg_metadata = {
        "info": info,
        "description": info.description,
        "aliases": info.aliases,
        "hidden": hidden,
        "category": category,
        "parent": parent,
        "is_group": group,
        "_prebuilt_click_command": click_cmd,  # Use new, clearer name
    }
    reg_metadata.update(extra_metadata)

    # Register in the registry
    reg.register(
        name=full_name,
        value=func,
        dimension=ComponentCategory.COMMAND.value,
        metadata=reg_metadata,
        aliases=aliases,
        replace=replace,
    )

    # Add metadata to the function
    func.__registry_name__ = command_name  # type: ignore[attr-defined]
    func.__registry_dimension__ = ComponentCategory.COMMAND.value  # type: ignore[attr-defined]
    func.__registry_info__ = info  # type: ignore[attr-defined]

    get_foundation_logger().trace(f"Registered command: {full_name}")

    return func


def x__register_command_func__mutmut_9(
    func: F,
    *,
    name: str | None = None,
    description: str | None = None,
    aliases: list[str] | None = None,
    hidden: bool = False,
    category: str | None = None,
    group: bool = False,
    replace: bool = False,
    registry: Registry | None = None,
    **extra_metadata: Any,
) -> F:
    """Internal function to register a command."""
    reg = registry or get_command_registry()

    # Determine command name and parent from dot notation
    if name:
        parts = name.split(".")
        if len(parts) >= 1:
            # Extract parent path and command name
            parent = ".".join(parts[:-1])
            command_name = parts[-1]

            # Auto-create parent groups if they don't exist (click only)
            _, has_click = _get_click()
            if has_click:
                ensure_parent_groups_fn = _get_ensure_parent_groups()
                if ensure_parent_groups_fn:
                    ensure_parent_groups_fn(parent, reg)
        else:
            parent = None
            command_name = name
    else:
        # Use function name as command name
        parent = None
        command_name = getattr(func, "__name__", "<anonymous>")

    # Check if it's already a Click command
    click_cmd = None
    click_module, has_click = _get_click()
    if has_click and isinstance(func, click_module.Command):
        click_cmd = func
        actual_func = func.callback
    else:
        actual_func = func

    # Create command info
    cmd_metadata = {"is_group": group}
    cmd_metadata.update(extra_metadata)

    info = CommandInfo(
        name=command_name,
        func=actual_func,
        description=description or (actual_func.__doc__ if actual_func else None),
        aliases=aliases or [],
        hidden=hidden,
        category=category,
        metadata=cmd_metadata,
        parent=parent,
    )

    # Build full registry key
    full_name = f"{parent}.{command_name}" if parent else command_name

    # Build registry metadata
    reg_metadata = {
        "info": info,
        "description": info.description,
        "aliases": info.aliases,
        "hidden": hidden,
        "category": category,
        "parent": parent,
        "is_group": group,
        "_prebuilt_click_command": click_cmd,  # Use new, clearer name
    }
    reg_metadata.update(extra_metadata)

    # Register in the registry
    reg.register(
        name=full_name,
        value=func,
        dimension=ComponentCategory.COMMAND.value,
        metadata=reg_metadata,
        aliases=aliases,
        replace=replace,
    )

    # Add metadata to the function
    func.__registry_name__ = command_name  # type: ignore[attr-defined]
    func.__registry_dimension__ = ComponentCategory.COMMAND.value  # type: ignore[attr-defined]
    func.__registry_info__ = info  # type: ignore[attr-defined]

    get_foundation_logger().trace(f"Registered command: {full_name}")

    return func


def x__register_command_func__mutmut_10(
    func: F,
    *,
    name: str | None = None,
    description: str | None = None,
    aliases: list[str] | None = None,
    hidden: bool = False,
    category: str | None = None,
    group: bool = False,
    replace: bool = False,
    registry: Registry | None = None,
    **extra_metadata: Any,
) -> F:
    """Internal function to register a command."""
    reg = registry or get_command_registry()

    # Determine command name and parent from dot notation
    if name:
        parts = name.split(".")
        if len(parts) > 2:
            # Extract parent path and command name
            parent = ".".join(parts[:-1])
            command_name = parts[-1]

            # Auto-create parent groups if they don't exist (click only)
            _, has_click = _get_click()
            if has_click:
                ensure_parent_groups_fn = _get_ensure_parent_groups()
                if ensure_parent_groups_fn:
                    ensure_parent_groups_fn(parent, reg)
        else:
            parent = None
            command_name = name
    else:
        # Use function name as command name
        parent = None
        command_name = getattr(func, "__name__", "<anonymous>")

    # Check if it's already a Click command
    click_cmd = None
    click_module, has_click = _get_click()
    if has_click and isinstance(func, click_module.Command):
        click_cmd = func
        actual_func = func.callback
    else:
        actual_func = func

    # Create command info
    cmd_metadata = {"is_group": group}
    cmd_metadata.update(extra_metadata)

    info = CommandInfo(
        name=command_name,
        func=actual_func,
        description=description or (actual_func.__doc__ if actual_func else None),
        aliases=aliases or [],
        hidden=hidden,
        category=category,
        metadata=cmd_metadata,
        parent=parent,
    )

    # Build full registry key
    full_name = f"{parent}.{command_name}" if parent else command_name

    # Build registry metadata
    reg_metadata = {
        "info": info,
        "description": info.description,
        "aliases": info.aliases,
        "hidden": hidden,
        "category": category,
        "parent": parent,
        "is_group": group,
        "_prebuilt_click_command": click_cmd,  # Use new, clearer name
    }
    reg_metadata.update(extra_metadata)

    # Register in the registry
    reg.register(
        name=full_name,
        value=func,
        dimension=ComponentCategory.COMMAND.value,
        metadata=reg_metadata,
        aliases=aliases,
        replace=replace,
    )

    # Add metadata to the function
    func.__registry_name__ = command_name  # type: ignore[attr-defined]
    func.__registry_dimension__ = ComponentCategory.COMMAND.value  # type: ignore[attr-defined]
    func.__registry_info__ = info  # type: ignore[attr-defined]

    get_foundation_logger().trace(f"Registered command: {full_name}")

    return func


def x__register_command_func__mutmut_11(
    func: F,
    *,
    name: str | None = None,
    description: str | None = None,
    aliases: list[str] | None = None,
    hidden: bool = False,
    category: str | None = None,
    group: bool = False,
    replace: bool = False,
    registry: Registry | None = None,
    **extra_metadata: Any,
) -> F:
    """Internal function to register a command."""
    reg = registry or get_command_registry()

    # Determine command name and parent from dot notation
    if name:
        parts = name.split(".")
        if len(parts) > 1:
            # Extract parent path and command name
            parent = None
            command_name = parts[-1]

            # Auto-create parent groups if they don't exist (click only)
            _, has_click = _get_click()
            if has_click:
                ensure_parent_groups_fn = _get_ensure_parent_groups()
                if ensure_parent_groups_fn:
                    ensure_parent_groups_fn(parent, reg)
        else:
            parent = None
            command_name = name
    else:
        # Use function name as command name
        parent = None
        command_name = getattr(func, "__name__", "<anonymous>")

    # Check if it's already a Click command
    click_cmd = None
    click_module, has_click = _get_click()
    if has_click and isinstance(func, click_module.Command):
        click_cmd = func
        actual_func = func.callback
    else:
        actual_func = func

    # Create command info
    cmd_metadata = {"is_group": group}
    cmd_metadata.update(extra_metadata)

    info = CommandInfo(
        name=command_name,
        func=actual_func,
        description=description or (actual_func.__doc__ if actual_func else None),
        aliases=aliases or [],
        hidden=hidden,
        category=category,
        metadata=cmd_metadata,
        parent=parent,
    )

    # Build full registry key
    full_name = f"{parent}.{command_name}" if parent else command_name

    # Build registry metadata
    reg_metadata = {
        "info": info,
        "description": info.description,
        "aliases": info.aliases,
        "hidden": hidden,
        "category": category,
        "parent": parent,
        "is_group": group,
        "_prebuilt_click_command": click_cmd,  # Use new, clearer name
    }
    reg_metadata.update(extra_metadata)

    # Register in the registry
    reg.register(
        name=full_name,
        value=func,
        dimension=ComponentCategory.COMMAND.value,
        metadata=reg_metadata,
        aliases=aliases,
        replace=replace,
    )

    # Add metadata to the function
    func.__registry_name__ = command_name  # type: ignore[attr-defined]
    func.__registry_dimension__ = ComponentCategory.COMMAND.value  # type: ignore[attr-defined]
    func.__registry_info__ = info  # type: ignore[attr-defined]

    get_foundation_logger().trace(f"Registered command: {full_name}")

    return func


def x__register_command_func__mutmut_12(
    func: F,
    *,
    name: str | None = None,
    description: str | None = None,
    aliases: list[str] | None = None,
    hidden: bool = False,
    category: str | None = None,
    group: bool = False,
    replace: bool = False,
    registry: Registry | None = None,
    **extra_metadata: Any,
) -> F:
    """Internal function to register a command."""
    reg = registry or get_command_registry()

    # Determine command name and parent from dot notation
    if name:
        parts = name.split(".")
        if len(parts) > 1:
            # Extract parent path and command name
            parent = ".".join(None)
            command_name = parts[-1]

            # Auto-create parent groups if they don't exist (click only)
            _, has_click = _get_click()
            if has_click:
                ensure_parent_groups_fn = _get_ensure_parent_groups()
                if ensure_parent_groups_fn:
                    ensure_parent_groups_fn(parent, reg)
        else:
            parent = None
            command_name = name
    else:
        # Use function name as command name
        parent = None
        command_name = getattr(func, "__name__", "<anonymous>")

    # Check if it's already a Click command
    click_cmd = None
    click_module, has_click = _get_click()
    if has_click and isinstance(func, click_module.Command):
        click_cmd = func
        actual_func = func.callback
    else:
        actual_func = func

    # Create command info
    cmd_metadata = {"is_group": group}
    cmd_metadata.update(extra_metadata)

    info = CommandInfo(
        name=command_name,
        func=actual_func,
        description=description or (actual_func.__doc__ if actual_func else None),
        aliases=aliases or [],
        hidden=hidden,
        category=category,
        metadata=cmd_metadata,
        parent=parent,
    )

    # Build full registry key
    full_name = f"{parent}.{command_name}" if parent else command_name

    # Build registry metadata
    reg_metadata = {
        "info": info,
        "description": info.description,
        "aliases": info.aliases,
        "hidden": hidden,
        "category": category,
        "parent": parent,
        "is_group": group,
        "_prebuilt_click_command": click_cmd,  # Use new, clearer name
    }
    reg_metadata.update(extra_metadata)

    # Register in the registry
    reg.register(
        name=full_name,
        value=func,
        dimension=ComponentCategory.COMMAND.value,
        metadata=reg_metadata,
        aliases=aliases,
        replace=replace,
    )

    # Add metadata to the function
    func.__registry_name__ = command_name  # type: ignore[attr-defined]
    func.__registry_dimension__ = ComponentCategory.COMMAND.value  # type: ignore[attr-defined]
    func.__registry_info__ = info  # type: ignore[attr-defined]

    get_foundation_logger().trace(f"Registered command: {full_name}")

    return func


def x__register_command_func__mutmut_13(
    func: F,
    *,
    name: str | None = None,
    description: str | None = None,
    aliases: list[str] | None = None,
    hidden: bool = False,
    category: str | None = None,
    group: bool = False,
    replace: bool = False,
    registry: Registry | None = None,
    **extra_metadata: Any,
) -> F:
    """Internal function to register a command."""
    reg = registry or get_command_registry()

    # Determine command name and parent from dot notation
    if name:
        parts = name.split(".")
        if len(parts) > 1:
            # Extract parent path and command name
            parent = "XX.XX".join(parts[:-1])
            command_name = parts[-1]

            # Auto-create parent groups if they don't exist (click only)
            _, has_click = _get_click()
            if has_click:
                ensure_parent_groups_fn = _get_ensure_parent_groups()
                if ensure_parent_groups_fn:
                    ensure_parent_groups_fn(parent, reg)
        else:
            parent = None
            command_name = name
    else:
        # Use function name as command name
        parent = None
        command_name = getattr(func, "__name__", "<anonymous>")

    # Check if it's already a Click command
    click_cmd = None
    click_module, has_click = _get_click()
    if has_click and isinstance(func, click_module.Command):
        click_cmd = func
        actual_func = func.callback
    else:
        actual_func = func

    # Create command info
    cmd_metadata = {"is_group": group}
    cmd_metadata.update(extra_metadata)

    info = CommandInfo(
        name=command_name,
        func=actual_func,
        description=description or (actual_func.__doc__ if actual_func else None),
        aliases=aliases or [],
        hidden=hidden,
        category=category,
        metadata=cmd_metadata,
        parent=parent,
    )

    # Build full registry key
    full_name = f"{parent}.{command_name}" if parent else command_name

    # Build registry metadata
    reg_metadata = {
        "info": info,
        "description": info.description,
        "aliases": info.aliases,
        "hidden": hidden,
        "category": category,
        "parent": parent,
        "is_group": group,
        "_prebuilt_click_command": click_cmd,  # Use new, clearer name
    }
    reg_metadata.update(extra_metadata)

    # Register in the registry
    reg.register(
        name=full_name,
        value=func,
        dimension=ComponentCategory.COMMAND.value,
        metadata=reg_metadata,
        aliases=aliases,
        replace=replace,
    )

    # Add metadata to the function
    func.__registry_name__ = command_name  # type: ignore[attr-defined]
    func.__registry_dimension__ = ComponentCategory.COMMAND.value  # type: ignore[attr-defined]
    func.__registry_info__ = info  # type: ignore[attr-defined]

    get_foundation_logger().trace(f"Registered command: {full_name}")

    return func


def x__register_command_func__mutmut_14(
    func: F,
    *,
    name: str | None = None,
    description: str | None = None,
    aliases: list[str] | None = None,
    hidden: bool = False,
    category: str | None = None,
    group: bool = False,
    replace: bool = False,
    registry: Registry | None = None,
    **extra_metadata: Any,
) -> F:
    """Internal function to register a command."""
    reg = registry or get_command_registry()

    # Determine command name and parent from dot notation
    if name:
        parts = name.split(".")
        if len(parts) > 1:
            # Extract parent path and command name
            parent = ".".join(parts[:+1])
            command_name = parts[-1]

            # Auto-create parent groups if they don't exist (click only)
            _, has_click = _get_click()
            if has_click:
                ensure_parent_groups_fn = _get_ensure_parent_groups()
                if ensure_parent_groups_fn:
                    ensure_parent_groups_fn(parent, reg)
        else:
            parent = None
            command_name = name
    else:
        # Use function name as command name
        parent = None
        command_name = getattr(func, "__name__", "<anonymous>")

    # Check if it's already a Click command
    click_cmd = None
    click_module, has_click = _get_click()
    if has_click and isinstance(func, click_module.Command):
        click_cmd = func
        actual_func = func.callback
    else:
        actual_func = func

    # Create command info
    cmd_metadata = {"is_group": group}
    cmd_metadata.update(extra_metadata)

    info = CommandInfo(
        name=command_name,
        func=actual_func,
        description=description or (actual_func.__doc__ if actual_func else None),
        aliases=aliases or [],
        hidden=hidden,
        category=category,
        metadata=cmd_metadata,
        parent=parent,
    )

    # Build full registry key
    full_name = f"{parent}.{command_name}" if parent else command_name

    # Build registry metadata
    reg_metadata = {
        "info": info,
        "description": info.description,
        "aliases": info.aliases,
        "hidden": hidden,
        "category": category,
        "parent": parent,
        "is_group": group,
        "_prebuilt_click_command": click_cmd,  # Use new, clearer name
    }
    reg_metadata.update(extra_metadata)

    # Register in the registry
    reg.register(
        name=full_name,
        value=func,
        dimension=ComponentCategory.COMMAND.value,
        metadata=reg_metadata,
        aliases=aliases,
        replace=replace,
    )

    # Add metadata to the function
    func.__registry_name__ = command_name  # type: ignore[attr-defined]
    func.__registry_dimension__ = ComponentCategory.COMMAND.value  # type: ignore[attr-defined]
    func.__registry_info__ = info  # type: ignore[attr-defined]

    get_foundation_logger().trace(f"Registered command: {full_name}")

    return func


def x__register_command_func__mutmut_15(
    func: F,
    *,
    name: str | None = None,
    description: str | None = None,
    aliases: list[str] | None = None,
    hidden: bool = False,
    category: str | None = None,
    group: bool = False,
    replace: bool = False,
    registry: Registry | None = None,
    **extra_metadata: Any,
) -> F:
    """Internal function to register a command."""
    reg = registry or get_command_registry()

    # Determine command name and parent from dot notation
    if name:
        parts = name.split(".")
        if len(parts) > 1:
            # Extract parent path and command name
            parent = ".".join(parts[:-2])
            command_name = parts[-1]

            # Auto-create parent groups if they don't exist (click only)
            _, has_click = _get_click()
            if has_click:
                ensure_parent_groups_fn = _get_ensure_parent_groups()
                if ensure_parent_groups_fn:
                    ensure_parent_groups_fn(parent, reg)
        else:
            parent = None
            command_name = name
    else:
        # Use function name as command name
        parent = None
        command_name = getattr(func, "__name__", "<anonymous>")

    # Check if it's already a Click command
    click_cmd = None
    click_module, has_click = _get_click()
    if has_click and isinstance(func, click_module.Command):
        click_cmd = func
        actual_func = func.callback
    else:
        actual_func = func

    # Create command info
    cmd_metadata = {"is_group": group}
    cmd_metadata.update(extra_metadata)

    info = CommandInfo(
        name=command_name,
        func=actual_func,
        description=description or (actual_func.__doc__ if actual_func else None),
        aliases=aliases or [],
        hidden=hidden,
        category=category,
        metadata=cmd_metadata,
        parent=parent,
    )

    # Build full registry key
    full_name = f"{parent}.{command_name}" if parent else command_name

    # Build registry metadata
    reg_metadata = {
        "info": info,
        "description": info.description,
        "aliases": info.aliases,
        "hidden": hidden,
        "category": category,
        "parent": parent,
        "is_group": group,
        "_prebuilt_click_command": click_cmd,  # Use new, clearer name
    }
    reg_metadata.update(extra_metadata)

    # Register in the registry
    reg.register(
        name=full_name,
        value=func,
        dimension=ComponentCategory.COMMAND.value,
        metadata=reg_metadata,
        aliases=aliases,
        replace=replace,
    )

    # Add metadata to the function
    func.__registry_name__ = command_name  # type: ignore[attr-defined]
    func.__registry_dimension__ = ComponentCategory.COMMAND.value  # type: ignore[attr-defined]
    func.__registry_info__ = info  # type: ignore[attr-defined]

    get_foundation_logger().trace(f"Registered command: {full_name}")

    return func


def x__register_command_func__mutmut_16(
    func: F,
    *,
    name: str | None = None,
    description: str | None = None,
    aliases: list[str] | None = None,
    hidden: bool = False,
    category: str | None = None,
    group: bool = False,
    replace: bool = False,
    registry: Registry | None = None,
    **extra_metadata: Any,
) -> F:
    """Internal function to register a command."""
    reg = registry or get_command_registry()

    # Determine command name and parent from dot notation
    if name:
        parts = name.split(".")
        if len(parts) > 1:
            # Extract parent path and command name
            parent = ".".join(parts[:-1])
            command_name = None

            # Auto-create parent groups if they don't exist (click only)
            _, has_click = _get_click()
            if has_click:
                ensure_parent_groups_fn = _get_ensure_parent_groups()
                if ensure_parent_groups_fn:
                    ensure_parent_groups_fn(parent, reg)
        else:
            parent = None
            command_name = name
    else:
        # Use function name as command name
        parent = None
        command_name = getattr(func, "__name__", "<anonymous>")

    # Check if it's already a Click command
    click_cmd = None
    click_module, has_click = _get_click()
    if has_click and isinstance(func, click_module.Command):
        click_cmd = func
        actual_func = func.callback
    else:
        actual_func = func

    # Create command info
    cmd_metadata = {"is_group": group}
    cmd_metadata.update(extra_metadata)

    info = CommandInfo(
        name=command_name,
        func=actual_func,
        description=description or (actual_func.__doc__ if actual_func else None),
        aliases=aliases or [],
        hidden=hidden,
        category=category,
        metadata=cmd_metadata,
        parent=parent,
    )

    # Build full registry key
    full_name = f"{parent}.{command_name}" if parent else command_name

    # Build registry metadata
    reg_metadata = {
        "info": info,
        "description": info.description,
        "aliases": info.aliases,
        "hidden": hidden,
        "category": category,
        "parent": parent,
        "is_group": group,
        "_prebuilt_click_command": click_cmd,  # Use new, clearer name
    }
    reg_metadata.update(extra_metadata)

    # Register in the registry
    reg.register(
        name=full_name,
        value=func,
        dimension=ComponentCategory.COMMAND.value,
        metadata=reg_metadata,
        aliases=aliases,
        replace=replace,
    )

    # Add metadata to the function
    func.__registry_name__ = command_name  # type: ignore[attr-defined]
    func.__registry_dimension__ = ComponentCategory.COMMAND.value  # type: ignore[attr-defined]
    func.__registry_info__ = info  # type: ignore[attr-defined]

    get_foundation_logger().trace(f"Registered command: {full_name}")

    return func


def x__register_command_func__mutmut_17(
    func: F,
    *,
    name: str | None = None,
    description: str | None = None,
    aliases: list[str] | None = None,
    hidden: bool = False,
    category: str | None = None,
    group: bool = False,
    replace: bool = False,
    registry: Registry | None = None,
    **extra_metadata: Any,
) -> F:
    """Internal function to register a command."""
    reg = registry or get_command_registry()

    # Determine command name and parent from dot notation
    if name:
        parts = name.split(".")
        if len(parts) > 1:
            # Extract parent path and command name
            parent = ".".join(parts[:-1])
            command_name = parts[+1]

            # Auto-create parent groups if they don't exist (click only)
            _, has_click = _get_click()
            if has_click:
                ensure_parent_groups_fn = _get_ensure_parent_groups()
                if ensure_parent_groups_fn:
                    ensure_parent_groups_fn(parent, reg)
        else:
            parent = None
            command_name = name
    else:
        # Use function name as command name
        parent = None
        command_name = getattr(func, "__name__", "<anonymous>")

    # Check if it's already a Click command
    click_cmd = None
    click_module, has_click = _get_click()
    if has_click and isinstance(func, click_module.Command):
        click_cmd = func
        actual_func = func.callback
    else:
        actual_func = func

    # Create command info
    cmd_metadata = {"is_group": group}
    cmd_metadata.update(extra_metadata)

    info = CommandInfo(
        name=command_name,
        func=actual_func,
        description=description or (actual_func.__doc__ if actual_func else None),
        aliases=aliases or [],
        hidden=hidden,
        category=category,
        metadata=cmd_metadata,
        parent=parent,
    )

    # Build full registry key
    full_name = f"{parent}.{command_name}" if parent else command_name

    # Build registry metadata
    reg_metadata = {
        "info": info,
        "description": info.description,
        "aliases": info.aliases,
        "hidden": hidden,
        "category": category,
        "parent": parent,
        "is_group": group,
        "_prebuilt_click_command": click_cmd,  # Use new, clearer name
    }
    reg_metadata.update(extra_metadata)

    # Register in the registry
    reg.register(
        name=full_name,
        value=func,
        dimension=ComponentCategory.COMMAND.value,
        metadata=reg_metadata,
        aliases=aliases,
        replace=replace,
    )

    # Add metadata to the function
    func.__registry_name__ = command_name  # type: ignore[attr-defined]
    func.__registry_dimension__ = ComponentCategory.COMMAND.value  # type: ignore[attr-defined]
    func.__registry_info__ = info  # type: ignore[attr-defined]

    get_foundation_logger().trace(f"Registered command: {full_name}")

    return func


def x__register_command_func__mutmut_18(
    func: F,
    *,
    name: str | None = None,
    description: str | None = None,
    aliases: list[str] | None = None,
    hidden: bool = False,
    category: str | None = None,
    group: bool = False,
    replace: bool = False,
    registry: Registry | None = None,
    **extra_metadata: Any,
) -> F:
    """Internal function to register a command."""
    reg = registry or get_command_registry()

    # Determine command name and parent from dot notation
    if name:
        parts = name.split(".")
        if len(parts) > 1:
            # Extract parent path and command name
            parent = ".".join(parts[:-1])
            command_name = parts[-2]

            # Auto-create parent groups if they don't exist (click only)
            _, has_click = _get_click()
            if has_click:
                ensure_parent_groups_fn = _get_ensure_parent_groups()
                if ensure_parent_groups_fn:
                    ensure_parent_groups_fn(parent, reg)
        else:
            parent = None
            command_name = name
    else:
        # Use function name as command name
        parent = None
        command_name = getattr(func, "__name__", "<anonymous>")

    # Check if it's already a Click command
    click_cmd = None
    click_module, has_click = _get_click()
    if has_click and isinstance(func, click_module.Command):
        click_cmd = func
        actual_func = func.callback
    else:
        actual_func = func

    # Create command info
    cmd_metadata = {"is_group": group}
    cmd_metadata.update(extra_metadata)

    info = CommandInfo(
        name=command_name,
        func=actual_func,
        description=description or (actual_func.__doc__ if actual_func else None),
        aliases=aliases or [],
        hidden=hidden,
        category=category,
        metadata=cmd_metadata,
        parent=parent,
    )

    # Build full registry key
    full_name = f"{parent}.{command_name}" if parent else command_name

    # Build registry metadata
    reg_metadata = {
        "info": info,
        "description": info.description,
        "aliases": info.aliases,
        "hidden": hidden,
        "category": category,
        "parent": parent,
        "is_group": group,
        "_prebuilt_click_command": click_cmd,  # Use new, clearer name
    }
    reg_metadata.update(extra_metadata)

    # Register in the registry
    reg.register(
        name=full_name,
        value=func,
        dimension=ComponentCategory.COMMAND.value,
        metadata=reg_metadata,
        aliases=aliases,
        replace=replace,
    )

    # Add metadata to the function
    func.__registry_name__ = command_name  # type: ignore[attr-defined]
    func.__registry_dimension__ = ComponentCategory.COMMAND.value  # type: ignore[attr-defined]
    func.__registry_info__ = info  # type: ignore[attr-defined]

    get_foundation_logger().trace(f"Registered command: {full_name}")

    return func


def x__register_command_func__mutmut_19(
    func: F,
    *,
    name: str | None = None,
    description: str | None = None,
    aliases: list[str] | None = None,
    hidden: bool = False,
    category: str | None = None,
    group: bool = False,
    replace: bool = False,
    registry: Registry | None = None,
    **extra_metadata: Any,
) -> F:
    """Internal function to register a command."""
    reg = registry or get_command_registry()

    # Determine command name and parent from dot notation
    if name:
        parts = name.split(".")
        if len(parts) > 1:
            # Extract parent path and command name
            parent = ".".join(parts[:-1])
            command_name = parts[-1]

            # Auto-create parent groups if they don't exist (click only)
            _, has_click = None
            if has_click:
                ensure_parent_groups_fn = _get_ensure_parent_groups()
                if ensure_parent_groups_fn:
                    ensure_parent_groups_fn(parent, reg)
        else:
            parent = None
            command_name = name
    else:
        # Use function name as command name
        parent = None
        command_name = getattr(func, "__name__", "<anonymous>")

    # Check if it's already a Click command
    click_cmd = None
    click_module, has_click = _get_click()
    if has_click and isinstance(func, click_module.Command):
        click_cmd = func
        actual_func = func.callback
    else:
        actual_func = func

    # Create command info
    cmd_metadata = {"is_group": group}
    cmd_metadata.update(extra_metadata)

    info = CommandInfo(
        name=command_name,
        func=actual_func,
        description=description or (actual_func.__doc__ if actual_func else None),
        aliases=aliases or [],
        hidden=hidden,
        category=category,
        metadata=cmd_metadata,
        parent=parent,
    )

    # Build full registry key
    full_name = f"{parent}.{command_name}" if parent else command_name

    # Build registry metadata
    reg_metadata = {
        "info": info,
        "description": info.description,
        "aliases": info.aliases,
        "hidden": hidden,
        "category": category,
        "parent": parent,
        "is_group": group,
        "_prebuilt_click_command": click_cmd,  # Use new, clearer name
    }
    reg_metadata.update(extra_metadata)

    # Register in the registry
    reg.register(
        name=full_name,
        value=func,
        dimension=ComponentCategory.COMMAND.value,
        metadata=reg_metadata,
        aliases=aliases,
        replace=replace,
    )

    # Add metadata to the function
    func.__registry_name__ = command_name  # type: ignore[attr-defined]
    func.__registry_dimension__ = ComponentCategory.COMMAND.value  # type: ignore[attr-defined]
    func.__registry_info__ = info  # type: ignore[attr-defined]

    get_foundation_logger().trace(f"Registered command: {full_name}")

    return func


def x__register_command_func__mutmut_20(
    func: F,
    *,
    name: str | None = None,
    description: str | None = None,
    aliases: list[str] | None = None,
    hidden: bool = False,
    category: str | None = None,
    group: bool = False,
    replace: bool = False,
    registry: Registry | None = None,
    **extra_metadata: Any,
) -> F:
    """Internal function to register a command."""
    reg = registry or get_command_registry()

    # Determine command name and parent from dot notation
    if name:
        parts = name.split(".")
        if len(parts) > 1:
            # Extract parent path and command name
            parent = ".".join(parts[:-1])
            command_name = parts[-1]

            # Auto-create parent groups if they don't exist (click only)
            _, has_click = _get_click()
            if has_click:
                ensure_parent_groups_fn = None
                if ensure_parent_groups_fn:
                    ensure_parent_groups_fn(parent, reg)
        else:
            parent = None
            command_name = name
    else:
        # Use function name as command name
        parent = None
        command_name = getattr(func, "__name__", "<anonymous>")

    # Check if it's already a Click command
    click_cmd = None
    click_module, has_click = _get_click()
    if has_click and isinstance(func, click_module.Command):
        click_cmd = func
        actual_func = func.callback
    else:
        actual_func = func

    # Create command info
    cmd_metadata = {"is_group": group}
    cmd_metadata.update(extra_metadata)

    info = CommandInfo(
        name=command_name,
        func=actual_func,
        description=description or (actual_func.__doc__ if actual_func else None),
        aliases=aliases or [],
        hidden=hidden,
        category=category,
        metadata=cmd_metadata,
        parent=parent,
    )

    # Build full registry key
    full_name = f"{parent}.{command_name}" if parent else command_name

    # Build registry metadata
    reg_metadata = {
        "info": info,
        "description": info.description,
        "aliases": info.aliases,
        "hidden": hidden,
        "category": category,
        "parent": parent,
        "is_group": group,
        "_prebuilt_click_command": click_cmd,  # Use new, clearer name
    }
    reg_metadata.update(extra_metadata)

    # Register in the registry
    reg.register(
        name=full_name,
        value=func,
        dimension=ComponentCategory.COMMAND.value,
        metadata=reg_metadata,
        aliases=aliases,
        replace=replace,
    )

    # Add metadata to the function
    func.__registry_name__ = command_name  # type: ignore[attr-defined]
    func.__registry_dimension__ = ComponentCategory.COMMAND.value  # type: ignore[attr-defined]
    func.__registry_info__ = info  # type: ignore[attr-defined]

    get_foundation_logger().trace(f"Registered command: {full_name}")

    return func


def x__register_command_func__mutmut_21(
    func: F,
    *,
    name: str | None = None,
    description: str | None = None,
    aliases: list[str] | None = None,
    hidden: bool = False,
    category: str | None = None,
    group: bool = False,
    replace: bool = False,
    registry: Registry | None = None,
    **extra_metadata: Any,
) -> F:
    """Internal function to register a command."""
    reg = registry or get_command_registry()

    # Determine command name and parent from dot notation
    if name:
        parts = name.split(".")
        if len(parts) > 1:
            # Extract parent path and command name
            parent = ".".join(parts[:-1])
            command_name = parts[-1]

            # Auto-create parent groups if they don't exist (click only)
            _, has_click = _get_click()
            if has_click:
                ensure_parent_groups_fn = _get_ensure_parent_groups()
                if ensure_parent_groups_fn:
                    ensure_parent_groups_fn(None, reg)
        else:
            parent = None
            command_name = name
    else:
        # Use function name as command name
        parent = None
        command_name = getattr(func, "__name__", "<anonymous>")

    # Check if it's already a Click command
    click_cmd = None
    click_module, has_click = _get_click()
    if has_click and isinstance(func, click_module.Command):
        click_cmd = func
        actual_func = func.callback
    else:
        actual_func = func

    # Create command info
    cmd_metadata = {"is_group": group}
    cmd_metadata.update(extra_metadata)

    info = CommandInfo(
        name=command_name,
        func=actual_func,
        description=description or (actual_func.__doc__ if actual_func else None),
        aliases=aliases or [],
        hidden=hidden,
        category=category,
        metadata=cmd_metadata,
        parent=parent,
    )

    # Build full registry key
    full_name = f"{parent}.{command_name}" if parent else command_name

    # Build registry metadata
    reg_metadata = {
        "info": info,
        "description": info.description,
        "aliases": info.aliases,
        "hidden": hidden,
        "category": category,
        "parent": parent,
        "is_group": group,
        "_prebuilt_click_command": click_cmd,  # Use new, clearer name
    }
    reg_metadata.update(extra_metadata)

    # Register in the registry
    reg.register(
        name=full_name,
        value=func,
        dimension=ComponentCategory.COMMAND.value,
        metadata=reg_metadata,
        aliases=aliases,
        replace=replace,
    )

    # Add metadata to the function
    func.__registry_name__ = command_name  # type: ignore[attr-defined]
    func.__registry_dimension__ = ComponentCategory.COMMAND.value  # type: ignore[attr-defined]
    func.__registry_info__ = info  # type: ignore[attr-defined]

    get_foundation_logger().trace(f"Registered command: {full_name}")

    return func


def x__register_command_func__mutmut_22(
    func: F,
    *,
    name: str | None = None,
    description: str | None = None,
    aliases: list[str] | None = None,
    hidden: bool = False,
    category: str | None = None,
    group: bool = False,
    replace: bool = False,
    registry: Registry | None = None,
    **extra_metadata: Any,
) -> F:
    """Internal function to register a command."""
    reg = registry or get_command_registry()

    # Determine command name and parent from dot notation
    if name:
        parts = name.split(".")
        if len(parts) > 1:
            # Extract parent path and command name
            parent = ".".join(parts[:-1])
            command_name = parts[-1]

            # Auto-create parent groups if they don't exist (click only)
            _, has_click = _get_click()
            if has_click:
                ensure_parent_groups_fn = _get_ensure_parent_groups()
                if ensure_parent_groups_fn:
                    ensure_parent_groups_fn(parent, None)
        else:
            parent = None
            command_name = name
    else:
        # Use function name as command name
        parent = None
        command_name = getattr(func, "__name__", "<anonymous>")

    # Check if it's already a Click command
    click_cmd = None
    click_module, has_click = _get_click()
    if has_click and isinstance(func, click_module.Command):
        click_cmd = func
        actual_func = func.callback
    else:
        actual_func = func

    # Create command info
    cmd_metadata = {"is_group": group}
    cmd_metadata.update(extra_metadata)

    info = CommandInfo(
        name=command_name,
        func=actual_func,
        description=description or (actual_func.__doc__ if actual_func else None),
        aliases=aliases or [],
        hidden=hidden,
        category=category,
        metadata=cmd_metadata,
        parent=parent,
    )

    # Build full registry key
    full_name = f"{parent}.{command_name}" if parent else command_name

    # Build registry metadata
    reg_metadata = {
        "info": info,
        "description": info.description,
        "aliases": info.aliases,
        "hidden": hidden,
        "category": category,
        "parent": parent,
        "is_group": group,
        "_prebuilt_click_command": click_cmd,  # Use new, clearer name
    }
    reg_metadata.update(extra_metadata)

    # Register in the registry
    reg.register(
        name=full_name,
        value=func,
        dimension=ComponentCategory.COMMAND.value,
        metadata=reg_metadata,
        aliases=aliases,
        replace=replace,
    )

    # Add metadata to the function
    func.__registry_name__ = command_name  # type: ignore[attr-defined]
    func.__registry_dimension__ = ComponentCategory.COMMAND.value  # type: ignore[attr-defined]
    func.__registry_info__ = info  # type: ignore[attr-defined]

    get_foundation_logger().trace(f"Registered command: {full_name}")

    return func


def x__register_command_func__mutmut_23(
    func: F,
    *,
    name: str | None = None,
    description: str | None = None,
    aliases: list[str] | None = None,
    hidden: bool = False,
    category: str | None = None,
    group: bool = False,
    replace: bool = False,
    registry: Registry | None = None,
    **extra_metadata: Any,
) -> F:
    """Internal function to register a command."""
    reg = registry or get_command_registry()

    # Determine command name and parent from dot notation
    if name:
        parts = name.split(".")
        if len(parts) > 1:
            # Extract parent path and command name
            parent = ".".join(parts[:-1])
            command_name = parts[-1]

            # Auto-create parent groups if they don't exist (click only)
            _, has_click = _get_click()
            if has_click:
                ensure_parent_groups_fn = _get_ensure_parent_groups()
                if ensure_parent_groups_fn:
                    ensure_parent_groups_fn(reg)
        else:
            parent = None
            command_name = name
    else:
        # Use function name as command name
        parent = None
        command_name = getattr(func, "__name__", "<anonymous>")

    # Check if it's already a Click command
    click_cmd = None
    click_module, has_click = _get_click()
    if has_click and isinstance(func, click_module.Command):
        click_cmd = func
        actual_func = func.callback
    else:
        actual_func = func

    # Create command info
    cmd_metadata = {"is_group": group}
    cmd_metadata.update(extra_metadata)

    info = CommandInfo(
        name=command_name,
        func=actual_func,
        description=description or (actual_func.__doc__ if actual_func else None),
        aliases=aliases or [],
        hidden=hidden,
        category=category,
        metadata=cmd_metadata,
        parent=parent,
    )

    # Build full registry key
    full_name = f"{parent}.{command_name}" if parent else command_name

    # Build registry metadata
    reg_metadata = {
        "info": info,
        "description": info.description,
        "aliases": info.aliases,
        "hidden": hidden,
        "category": category,
        "parent": parent,
        "is_group": group,
        "_prebuilt_click_command": click_cmd,  # Use new, clearer name
    }
    reg_metadata.update(extra_metadata)

    # Register in the registry
    reg.register(
        name=full_name,
        value=func,
        dimension=ComponentCategory.COMMAND.value,
        metadata=reg_metadata,
        aliases=aliases,
        replace=replace,
    )

    # Add metadata to the function
    func.__registry_name__ = command_name  # type: ignore[attr-defined]
    func.__registry_dimension__ = ComponentCategory.COMMAND.value  # type: ignore[attr-defined]
    func.__registry_info__ = info  # type: ignore[attr-defined]

    get_foundation_logger().trace(f"Registered command: {full_name}")

    return func


def x__register_command_func__mutmut_24(
    func: F,
    *,
    name: str | None = None,
    description: str | None = None,
    aliases: list[str] | None = None,
    hidden: bool = False,
    category: str | None = None,
    group: bool = False,
    replace: bool = False,
    registry: Registry | None = None,
    **extra_metadata: Any,
) -> F:
    """Internal function to register a command."""
    reg = registry or get_command_registry()

    # Determine command name and parent from dot notation
    if name:
        parts = name.split(".")
        if len(parts) > 1:
            # Extract parent path and command name
            parent = ".".join(parts[:-1])
            command_name = parts[-1]

            # Auto-create parent groups if they don't exist (click only)
            _, has_click = _get_click()
            if has_click:
                ensure_parent_groups_fn = _get_ensure_parent_groups()
                if ensure_parent_groups_fn:
                    ensure_parent_groups_fn(
                        parent,
                    )
        else:
            parent = None
            command_name = name
    else:
        # Use function name as command name
        parent = None
        command_name = getattr(func, "__name__", "<anonymous>")

    # Check if it's already a Click command
    click_cmd = None
    click_module, has_click = _get_click()
    if has_click and isinstance(func, click_module.Command):
        click_cmd = func
        actual_func = func.callback
    else:
        actual_func = func

    # Create command info
    cmd_metadata = {"is_group": group}
    cmd_metadata.update(extra_metadata)

    info = CommandInfo(
        name=command_name,
        func=actual_func,
        description=description or (actual_func.__doc__ if actual_func else None),
        aliases=aliases or [],
        hidden=hidden,
        category=category,
        metadata=cmd_metadata,
        parent=parent,
    )

    # Build full registry key
    full_name = f"{parent}.{command_name}" if parent else command_name

    # Build registry metadata
    reg_metadata = {
        "info": info,
        "description": info.description,
        "aliases": info.aliases,
        "hidden": hidden,
        "category": category,
        "parent": parent,
        "is_group": group,
        "_prebuilt_click_command": click_cmd,  # Use new, clearer name
    }
    reg_metadata.update(extra_metadata)

    # Register in the registry
    reg.register(
        name=full_name,
        value=func,
        dimension=ComponentCategory.COMMAND.value,
        metadata=reg_metadata,
        aliases=aliases,
        replace=replace,
    )

    # Add metadata to the function
    func.__registry_name__ = command_name  # type: ignore[attr-defined]
    func.__registry_dimension__ = ComponentCategory.COMMAND.value  # type: ignore[attr-defined]
    func.__registry_info__ = info  # type: ignore[attr-defined]

    get_foundation_logger().trace(f"Registered command: {full_name}")

    return func


def x__register_command_func__mutmut_25(
    func: F,
    *,
    name: str | None = None,
    description: str | None = None,
    aliases: list[str] | None = None,
    hidden: bool = False,
    category: str | None = None,
    group: bool = False,
    replace: bool = False,
    registry: Registry | None = None,
    **extra_metadata: Any,
) -> F:
    """Internal function to register a command."""
    reg = registry or get_command_registry()

    # Determine command name and parent from dot notation
    if name:
        parts = name.split(".")
        if len(parts) > 1:
            # Extract parent path and command name
            parent = ".".join(parts[:-1])
            command_name = parts[-1]

            # Auto-create parent groups if they don't exist (click only)
            _, has_click = _get_click()
            if has_click:
                ensure_parent_groups_fn = _get_ensure_parent_groups()
                if ensure_parent_groups_fn:
                    ensure_parent_groups_fn(parent, reg)
        else:
            parent = ""
            command_name = name
    else:
        # Use function name as command name
        parent = None
        command_name = getattr(func, "__name__", "<anonymous>")

    # Check if it's already a Click command
    click_cmd = None
    click_module, has_click = _get_click()
    if has_click and isinstance(func, click_module.Command):
        click_cmd = func
        actual_func = func.callback
    else:
        actual_func = func

    # Create command info
    cmd_metadata = {"is_group": group}
    cmd_metadata.update(extra_metadata)

    info = CommandInfo(
        name=command_name,
        func=actual_func,
        description=description or (actual_func.__doc__ if actual_func else None),
        aliases=aliases or [],
        hidden=hidden,
        category=category,
        metadata=cmd_metadata,
        parent=parent,
    )

    # Build full registry key
    full_name = f"{parent}.{command_name}" if parent else command_name

    # Build registry metadata
    reg_metadata = {
        "info": info,
        "description": info.description,
        "aliases": info.aliases,
        "hidden": hidden,
        "category": category,
        "parent": parent,
        "is_group": group,
        "_prebuilt_click_command": click_cmd,  # Use new, clearer name
    }
    reg_metadata.update(extra_metadata)

    # Register in the registry
    reg.register(
        name=full_name,
        value=func,
        dimension=ComponentCategory.COMMAND.value,
        metadata=reg_metadata,
        aliases=aliases,
        replace=replace,
    )

    # Add metadata to the function
    func.__registry_name__ = command_name  # type: ignore[attr-defined]
    func.__registry_dimension__ = ComponentCategory.COMMAND.value  # type: ignore[attr-defined]
    func.__registry_info__ = info  # type: ignore[attr-defined]

    get_foundation_logger().trace(f"Registered command: {full_name}")

    return func


def x__register_command_func__mutmut_26(
    func: F,
    *,
    name: str | None = None,
    description: str | None = None,
    aliases: list[str] | None = None,
    hidden: bool = False,
    category: str | None = None,
    group: bool = False,
    replace: bool = False,
    registry: Registry | None = None,
    **extra_metadata: Any,
) -> F:
    """Internal function to register a command."""
    reg = registry or get_command_registry()

    # Determine command name and parent from dot notation
    if name:
        parts = name.split(".")
        if len(parts) > 1:
            # Extract parent path and command name
            parent = ".".join(parts[:-1])
            command_name = parts[-1]

            # Auto-create parent groups if they don't exist (click only)
            _, has_click = _get_click()
            if has_click:
                ensure_parent_groups_fn = _get_ensure_parent_groups()
                if ensure_parent_groups_fn:
                    ensure_parent_groups_fn(parent, reg)
        else:
            parent = None
            command_name = None
    else:
        # Use function name as command name
        parent = None
        command_name = getattr(func, "__name__", "<anonymous>")

    # Check if it's already a Click command
    click_cmd = None
    click_module, has_click = _get_click()
    if has_click and isinstance(func, click_module.Command):
        click_cmd = func
        actual_func = func.callback
    else:
        actual_func = func

    # Create command info
    cmd_metadata = {"is_group": group}
    cmd_metadata.update(extra_metadata)

    info = CommandInfo(
        name=command_name,
        func=actual_func,
        description=description or (actual_func.__doc__ if actual_func else None),
        aliases=aliases or [],
        hidden=hidden,
        category=category,
        metadata=cmd_metadata,
        parent=parent,
    )

    # Build full registry key
    full_name = f"{parent}.{command_name}" if parent else command_name

    # Build registry metadata
    reg_metadata = {
        "info": info,
        "description": info.description,
        "aliases": info.aliases,
        "hidden": hidden,
        "category": category,
        "parent": parent,
        "is_group": group,
        "_prebuilt_click_command": click_cmd,  # Use new, clearer name
    }
    reg_metadata.update(extra_metadata)

    # Register in the registry
    reg.register(
        name=full_name,
        value=func,
        dimension=ComponentCategory.COMMAND.value,
        metadata=reg_metadata,
        aliases=aliases,
        replace=replace,
    )

    # Add metadata to the function
    func.__registry_name__ = command_name  # type: ignore[attr-defined]
    func.__registry_dimension__ = ComponentCategory.COMMAND.value  # type: ignore[attr-defined]
    func.__registry_info__ = info  # type: ignore[attr-defined]

    get_foundation_logger().trace(f"Registered command: {full_name}")

    return func


def x__register_command_func__mutmut_27(
    func: F,
    *,
    name: str | None = None,
    description: str | None = None,
    aliases: list[str] | None = None,
    hidden: bool = False,
    category: str | None = None,
    group: bool = False,
    replace: bool = False,
    registry: Registry | None = None,
    **extra_metadata: Any,
) -> F:
    """Internal function to register a command."""
    reg = registry or get_command_registry()

    # Determine command name and parent from dot notation
    if name:
        parts = name.split(".")
        if len(parts) > 1:
            # Extract parent path and command name
            parent = ".".join(parts[:-1])
            command_name = parts[-1]

            # Auto-create parent groups if they don't exist (click only)
            _, has_click = _get_click()
            if has_click:
                ensure_parent_groups_fn = _get_ensure_parent_groups()
                if ensure_parent_groups_fn:
                    ensure_parent_groups_fn(parent, reg)
        else:
            parent = None
            command_name = name
    else:
        # Use function name as command name
        parent = ""
        command_name = getattr(func, "__name__", "<anonymous>")

    # Check if it's already a Click command
    click_cmd = None
    click_module, has_click = _get_click()
    if has_click and isinstance(func, click_module.Command):
        click_cmd = func
        actual_func = func.callback
    else:
        actual_func = func

    # Create command info
    cmd_metadata = {"is_group": group}
    cmd_metadata.update(extra_metadata)

    info = CommandInfo(
        name=command_name,
        func=actual_func,
        description=description or (actual_func.__doc__ if actual_func else None),
        aliases=aliases or [],
        hidden=hidden,
        category=category,
        metadata=cmd_metadata,
        parent=parent,
    )

    # Build full registry key
    full_name = f"{parent}.{command_name}" if parent else command_name

    # Build registry metadata
    reg_metadata = {
        "info": info,
        "description": info.description,
        "aliases": info.aliases,
        "hidden": hidden,
        "category": category,
        "parent": parent,
        "is_group": group,
        "_prebuilt_click_command": click_cmd,  # Use new, clearer name
    }
    reg_metadata.update(extra_metadata)

    # Register in the registry
    reg.register(
        name=full_name,
        value=func,
        dimension=ComponentCategory.COMMAND.value,
        metadata=reg_metadata,
        aliases=aliases,
        replace=replace,
    )

    # Add metadata to the function
    func.__registry_name__ = command_name  # type: ignore[attr-defined]
    func.__registry_dimension__ = ComponentCategory.COMMAND.value  # type: ignore[attr-defined]
    func.__registry_info__ = info  # type: ignore[attr-defined]

    get_foundation_logger().trace(f"Registered command: {full_name}")

    return func


def x__register_command_func__mutmut_28(
    func: F,
    *,
    name: str | None = None,
    description: str | None = None,
    aliases: list[str] | None = None,
    hidden: bool = False,
    category: str | None = None,
    group: bool = False,
    replace: bool = False,
    registry: Registry | None = None,
    **extra_metadata: Any,
) -> F:
    """Internal function to register a command."""
    reg = registry or get_command_registry()

    # Determine command name and parent from dot notation
    if name:
        parts = name.split(".")
        if len(parts) > 1:
            # Extract parent path and command name
            parent = ".".join(parts[:-1])
            command_name = parts[-1]

            # Auto-create parent groups if they don't exist (click only)
            _, has_click = _get_click()
            if has_click:
                ensure_parent_groups_fn = _get_ensure_parent_groups()
                if ensure_parent_groups_fn:
                    ensure_parent_groups_fn(parent, reg)
        else:
            parent = None
            command_name = name
    else:
        # Use function name as command name
        parent = None
        command_name = None

    # Check if it's already a Click command
    click_cmd = None
    click_module, has_click = _get_click()
    if has_click and isinstance(func, click_module.Command):
        click_cmd = func
        actual_func = func.callback
    else:
        actual_func = func

    # Create command info
    cmd_metadata = {"is_group": group}
    cmd_metadata.update(extra_metadata)

    info = CommandInfo(
        name=command_name,
        func=actual_func,
        description=description or (actual_func.__doc__ if actual_func else None),
        aliases=aliases or [],
        hidden=hidden,
        category=category,
        metadata=cmd_metadata,
        parent=parent,
    )

    # Build full registry key
    full_name = f"{parent}.{command_name}" if parent else command_name

    # Build registry metadata
    reg_metadata = {
        "info": info,
        "description": info.description,
        "aliases": info.aliases,
        "hidden": hidden,
        "category": category,
        "parent": parent,
        "is_group": group,
        "_prebuilt_click_command": click_cmd,  # Use new, clearer name
    }
    reg_metadata.update(extra_metadata)

    # Register in the registry
    reg.register(
        name=full_name,
        value=func,
        dimension=ComponentCategory.COMMAND.value,
        metadata=reg_metadata,
        aliases=aliases,
        replace=replace,
    )

    # Add metadata to the function
    func.__registry_name__ = command_name  # type: ignore[attr-defined]
    func.__registry_dimension__ = ComponentCategory.COMMAND.value  # type: ignore[attr-defined]
    func.__registry_info__ = info  # type: ignore[attr-defined]

    get_foundation_logger().trace(f"Registered command: {full_name}")

    return func


def x__register_command_func__mutmut_29(
    func: F,
    *,
    name: str | None = None,
    description: str | None = None,
    aliases: list[str] | None = None,
    hidden: bool = False,
    category: str | None = None,
    group: bool = False,
    replace: bool = False,
    registry: Registry | None = None,
    **extra_metadata: Any,
) -> F:
    """Internal function to register a command."""
    reg = registry or get_command_registry()

    # Determine command name and parent from dot notation
    if name:
        parts = name.split(".")
        if len(parts) > 1:
            # Extract parent path and command name
            parent = ".".join(parts[:-1])
            command_name = parts[-1]

            # Auto-create parent groups if they don't exist (click only)
            _, has_click = _get_click()
            if has_click:
                ensure_parent_groups_fn = _get_ensure_parent_groups()
                if ensure_parent_groups_fn:
                    ensure_parent_groups_fn(parent, reg)
        else:
            parent = None
            command_name = name
    else:
        # Use function name as command name
        parent = None
        command_name = getattr(None, "__name__", "<anonymous>")

    # Check if it's already a Click command
    click_cmd = None
    click_module, has_click = _get_click()
    if has_click and isinstance(func, click_module.Command):
        click_cmd = func
        actual_func = func.callback
    else:
        actual_func = func

    # Create command info
    cmd_metadata = {"is_group": group}
    cmd_metadata.update(extra_metadata)

    info = CommandInfo(
        name=command_name,
        func=actual_func,
        description=description or (actual_func.__doc__ if actual_func else None),
        aliases=aliases or [],
        hidden=hidden,
        category=category,
        metadata=cmd_metadata,
        parent=parent,
    )

    # Build full registry key
    full_name = f"{parent}.{command_name}" if parent else command_name

    # Build registry metadata
    reg_metadata = {
        "info": info,
        "description": info.description,
        "aliases": info.aliases,
        "hidden": hidden,
        "category": category,
        "parent": parent,
        "is_group": group,
        "_prebuilt_click_command": click_cmd,  # Use new, clearer name
    }
    reg_metadata.update(extra_metadata)

    # Register in the registry
    reg.register(
        name=full_name,
        value=func,
        dimension=ComponentCategory.COMMAND.value,
        metadata=reg_metadata,
        aliases=aliases,
        replace=replace,
    )

    # Add metadata to the function
    func.__registry_name__ = command_name  # type: ignore[attr-defined]
    func.__registry_dimension__ = ComponentCategory.COMMAND.value  # type: ignore[attr-defined]
    func.__registry_info__ = info  # type: ignore[attr-defined]

    get_foundation_logger().trace(f"Registered command: {full_name}")

    return func


def x__register_command_func__mutmut_30(
    func: F,
    *,
    name: str | None = None,
    description: str | None = None,
    aliases: list[str] | None = None,
    hidden: bool = False,
    category: str | None = None,
    group: bool = False,
    replace: bool = False,
    registry: Registry | None = None,
    **extra_metadata: Any,
) -> F:
    """Internal function to register a command."""
    reg = registry or get_command_registry()

    # Determine command name and parent from dot notation
    if name:
        parts = name.split(".")
        if len(parts) > 1:
            # Extract parent path and command name
            parent = ".".join(parts[:-1])
            command_name = parts[-1]

            # Auto-create parent groups if they don't exist (click only)
            _, has_click = _get_click()
            if has_click:
                ensure_parent_groups_fn = _get_ensure_parent_groups()
                if ensure_parent_groups_fn:
                    ensure_parent_groups_fn(parent, reg)
        else:
            parent = None
            command_name = name
    else:
        # Use function name as command name
        parent = None
        command_name = getattr(func, None, "<anonymous>")

    # Check if it's already a Click command
    click_cmd = None
    click_module, has_click = _get_click()
    if has_click and isinstance(func, click_module.Command):
        click_cmd = func
        actual_func = func.callback
    else:
        actual_func = func

    # Create command info
    cmd_metadata = {"is_group": group}
    cmd_metadata.update(extra_metadata)

    info = CommandInfo(
        name=command_name,
        func=actual_func,
        description=description or (actual_func.__doc__ if actual_func else None),
        aliases=aliases or [],
        hidden=hidden,
        category=category,
        metadata=cmd_metadata,
        parent=parent,
    )

    # Build full registry key
    full_name = f"{parent}.{command_name}" if parent else command_name

    # Build registry metadata
    reg_metadata = {
        "info": info,
        "description": info.description,
        "aliases": info.aliases,
        "hidden": hidden,
        "category": category,
        "parent": parent,
        "is_group": group,
        "_prebuilt_click_command": click_cmd,  # Use new, clearer name
    }
    reg_metadata.update(extra_metadata)

    # Register in the registry
    reg.register(
        name=full_name,
        value=func,
        dimension=ComponentCategory.COMMAND.value,
        metadata=reg_metadata,
        aliases=aliases,
        replace=replace,
    )

    # Add metadata to the function
    func.__registry_name__ = command_name  # type: ignore[attr-defined]
    func.__registry_dimension__ = ComponentCategory.COMMAND.value  # type: ignore[attr-defined]
    func.__registry_info__ = info  # type: ignore[attr-defined]

    get_foundation_logger().trace(f"Registered command: {full_name}")

    return func


def x__register_command_func__mutmut_31(
    func: F,
    *,
    name: str | None = None,
    description: str | None = None,
    aliases: list[str] | None = None,
    hidden: bool = False,
    category: str | None = None,
    group: bool = False,
    replace: bool = False,
    registry: Registry | None = None,
    **extra_metadata: Any,
) -> F:
    """Internal function to register a command."""
    reg = registry or get_command_registry()

    # Determine command name and parent from dot notation
    if name:
        parts = name.split(".")
        if len(parts) > 1:
            # Extract parent path and command name
            parent = ".".join(parts[:-1])
            command_name = parts[-1]

            # Auto-create parent groups if they don't exist (click only)
            _, has_click = _get_click()
            if has_click:
                ensure_parent_groups_fn = _get_ensure_parent_groups()
                if ensure_parent_groups_fn:
                    ensure_parent_groups_fn(parent, reg)
        else:
            parent = None
            command_name = name
    else:
        # Use function name as command name
        parent = None
        command_name = getattr(func, "__name__", None)

    # Check if it's already a Click command
    click_cmd = None
    click_module, has_click = _get_click()
    if has_click and isinstance(func, click_module.Command):
        click_cmd = func
        actual_func = func.callback
    else:
        actual_func = func

    # Create command info
    cmd_metadata = {"is_group": group}
    cmd_metadata.update(extra_metadata)

    info = CommandInfo(
        name=command_name,
        func=actual_func,
        description=description or (actual_func.__doc__ if actual_func else None),
        aliases=aliases or [],
        hidden=hidden,
        category=category,
        metadata=cmd_metadata,
        parent=parent,
    )

    # Build full registry key
    full_name = f"{parent}.{command_name}" if parent else command_name

    # Build registry metadata
    reg_metadata = {
        "info": info,
        "description": info.description,
        "aliases": info.aliases,
        "hidden": hidden,
        "category": category,
        "parent": parent,
        "is_group": group,
        "_prebuilt_click_command": click_cmd,  # Use new, clearer name
    }
    reg_metadata.update(extra_metadata)

    # Register in the registry
    reg.register(
        name=full_name,
        value=func,
        dimension=ComponentCategory.COMMAND.value,
        metadata=reg_metadata,
        aliases=aliases,
        replace=replace,
    )

    # Add metadata to the function
    func.__registry_name__ = command_name  # type: ignore[attr-defined]
    func.__registry_dimension__ = ComponentCategory.COMMAND.value  # type: ignore[attr-defined]
    func.__registry_info__ = info  # type: ignore[attr-defined]

    get_foundation_logger().trace(f"Registered command: {full_name}")

    return func


def x__register_command_func__mutmut_32(
    func: F,
    *,
    name: str | None = None,
    description: str | None = None,
    aliases: list[str] | None = None,
    hidden: bool = False,
    category: str | None = None,
    group: bool = False,
    replace: bool = False,
    registry: Registry | None = None,
    **extra_metadata: Any,
) -> F:
    """Internal function to register a command."""
    reg = registry or get_command_registry()

    # Determine command name and parent from dot notation
    if name:
        parts = name.split(".")
        if len(parts) > 1:
            # Extract parent path and command name
            parent = ".".join(parts[:-1])
            command_name = parts[-1]

            # Auto-create parent groups if they don't exist (click only)
            _, has_click = _get_click()
            if has_click:
                ensure_parent_groups_fn = _get_ensure_parent_groups()
                if ensure_parent_groups_fn:
                    ensure_parent_groups_fn(parent, reg)
        else:
            parent = None
            command_name = name
    else:
        # Use function name as command name
        parent = None
        command_name = getattr("__name__", "<anonymous>")

    # Check if it's already a Click command
    click_cmd = None
    click_module, has_click = _get_click()
    if has_click and isinstance(func, click_module.Command):
        click_cmd = func
        actual_func = func.callback
    else:
        actual_func = func

    # Create command info
    cmd_metadata = {"is_group": group}
    cmd_metadata.update(extra_metadata)

    info = CommandInfo(
        name=command_name,
        func=actual_func,
        description=description or (actual_func.__doc__ if actual_func else None),
        aliases=aliases or [],
        hidden=hidden,
        category=category,
        metadata=cmd_metadata,
        parent=parent,
    )

    # Build full registry key
    full_name = f"{parent}.{command_name}" if parent else command_name

    # Build registry metadata
    reg_metadata = {
        "info": info,
        "description": info.description,
        "aliases": info.aliases,
        "hidden": hidden,
        "category": category,
        "parent": parent,
        "is_group": group,
        "_prebuilt_click_command": click_cmd,  # Use new, clearer name
    }
    reg_metadata.update(extra_metadata)

    # Register in the registry
    reg.register(
        name=full_name,
        value=func,
        dimension=ComponentCategory.COMMAND.value,
        metadata=reg_metadata,
        aliases=aliases,
        replace=replace,
    )

    # Add metadata to the function
    func.__registry_name__ = command_name  # type: ignore[attr-defined]
    func.__registry_dimension__ = ComponentCategory.COMMAND.value  # type: ignore[attr-defined]
    func.__registry_info__ = info  # type: ignore[attr-defined]

    get_foundation_logger().trace(f"Registered command: {full_name}")

    return func


def x__register_command_func__mutmut_33(
    func: F,
    *,
    name: str | None = None,
    description: str | None = None,
    aliases: list[str] | None = None,
    hidden: bool = False,
    category: str | None = None,
    group: bool = False,
    replace: bool = False,
    registry: Registry | None = None,
    **extra_metadata: Any,
) -> F:
    """Internal function to register a command."""
    reg = registry or get_command_registry()

    # Determine command name and parent from dot notation
    if name:
        parts = name.split(".")
        if len(parts) > 1:
            # Extract parent path and command name
            parent = ".".join(parts[:-1])
            command_name = parts[-1]

            # Auto-create parent groups if they don't exist (click only)
            _, has_click = _get_click()
            if has_click:
                ensure_parent_groups_fn = _get_ensure_parent_groups()
                if ensure_parent_groups_fn:
                    ensure_parent_groups_fn(parent, reg)
        else:
            parent = None
            command_name = name
    else:
        # Use function name as command name
        parent = None
        command_name = getattr(func, "<anonymous>")

    # Check if it's already a Click command
    click_cmd = None
    click_module, has_click = _get_click()
    if has_click and isinstance(func, click_module.Command):
        click_cmd = func
        actual_func = func.callback
    else:
        actual_func = func

    # Create command info
    cmd_metadata = {"is_group": group}
    cmd_metadata.update(extra_metadata)

    info = CommandInfo(
        name=command_name,
        func=actual_func,
        description=description or (actual_func.__doc__ if actual_func else None),
        aliases=aliases or [],
        hidden=hidden,
        category=category,
        metadata=cmd_metadata,
        parent=parent,
    )

    # Build full registry key
    full_name = f"{parent}.{command_name}" if parent else command_name

    # Build registry metadata
    reg_metadata = {
        "info": info,
        "description": info.description,
        "aliases": info.aliases,
        "hidden": hidden,
        "category": category,
        "parent": parent,
        "is_group": group,
        "_prebuilt_click_command": click_cmd,  # Use new, clearer name
    }
    reg_metadata.update(extra_metadata)

    # Register in the registry
    reg.register(
        name=full_name,
        value=func,
        dimension=ComponentCategory.COMMAND.value,
        metadata=reg_metadata,
        aliases=aliases,
        replace=replace,
    )

    # Add metadata to the function
    func.__registry_name__ = command_name  # type: ignore[attr-defined]
    func.__registry_dimension__ = ComponentCategory.COMMAND.value  # type: ignore[attr-defined]
    func.__registry_info__ = info  # type: ignore[attr-defined]

    get_foundation_logger().trace(f"Registered command: {full_name}")

    return func


def x__register_command_func__mutmut_34(
    func: F,
    *,
    name: str | None = None,
    description: str | None = None,
    aliases: list[str] | None = None,
    hidden: bool = False,
    category: str | None = None,
    group: bool = False,
    replace: bool = False,
    registry: Registry | None = None,
    **extra_metadata: Any,
) -> F:
    """Internal function to register a command."""
    reg = registry or get_command_registry()

    # Determine command name and parent from dot notation
    if name:
        parts = name.split(".")
        if len(parts) > 1:
            # Extract parent path and command name
            parent = ".".join(parts[:-1])
            command_name = parts[-1]

            # Auto-create parent groups if they don't exist (click only)
            _, has_click = _get_click()
            if has_click:
                ensure_parent_groups_fn = _get_ensure_parent_groups()
                if ensure_parent_groups_fn:
                    ensure_parent_groups_fn(parent, reg)
        else:
            parent = None
            command_name = name
    else:
        # Use function name as command name
        parent = None
        command_name = getattr(
            func,
            "__name__",
        )

    # Check if it's already a Click command
    click_cmd = None
    click_module, has_click = _get_click()
    if has_click and isinstance(func, click_module.Command):
        click_cmd = func
        actual_func = func.callback
    else:
        actual_func = func

    # Create command info
    cmd_metadata = {"is_group": group}
    cmd_metadata.update(extra_metadata)

    info = CommandInfo(
        name=command_name,
        func=actual_func,
        description=description or (actual_func.__doc__ if actual_func else None),
        aliases=aliases or [],
        hidden=hidden,
        category=category,
        metadata=cmd_metadata,
        parent=parent,
    )

    # Build full registry key
    full_name = f"{parent}.{command_name}" if parent else command_name

    # Build registry metadata
    reg_metadata = {
        "info": info,
        "description": info.description,
        "aliases": info.aliases,
        "hidden": hidden,
        "category": category,
        "parent": parent,
        "is_group": group,
        "_prebuilt_click_command": click_cmd,  # Use new, clearer name
    }
    reg_metadata.update(extra_metadata)

    # Register in the registry
    reg.register(
        name=full_name,
        value=func,
        dimension=ComponentCategory.COMMAND.value,
        metadata=reg_metadata,
        aliases=aliases,
        replace=replace,
    )

    # Add metadata to the function
    func.__registry_name__ = command_name  # type: ignore[attr-defined]
    func.__registry_dimension__ = ComponentCategory.COMMAND.value  # type: ignore[attr-defined]
    func.__registry_info__ = info  # type: ignore[attr-defined]

    get_foundation_logger().trace(f"Registered command: {full_name}")

    return func


def x__register_command_func__mutmut_35(
    func: F,
    *,
    name: str | None = None,
    description: str | None = None,
    aliases: list[str] | None = None,
    hidden: bool = False,
    category: str | None = None,
    group: bool = False,
    replace: bool = False,
    registry: Registry | None = None,
    **extra_metadata: Any,
) -> F:
    """Internal function to register a command."""
    reg = registry or get_command_registry()

    # Determine command name and parent from dot notation
    if name:
        parts = name.split(".")
        if len(parts) > 1:
            # Extract parent path and command name
            parent = ".".join(parts[:-1])
            command_name = parts[-1]

            # Auto-create parent groups if they don't exist (click only)
            _, has_click = _get_click()
            if has_click:
                ensure_parent_groups_fn = _get_ensure_parent_groups()
                if ensure_parent_groups_fn:
                    ensure_parent_groups_fn(parent, reg)
        else:
            parent = None
            command_name = name
    else:
        # Use function name as command name
        parent = None
        command_name = getattr(func, "XX__name__XX", "<anonymous>")

    # Check if it's already a Click command
    click_cmd = None
    click_module, has_click = _get_click()
    if has_click and isinstance(func, click_module.Command):
        click_cmd = func
        actual_func = func.callback
    else:
        actual_func = func

    # Create command info
    cmd_metadata = {"is_group": group}
    cmd_metadata.update(extra_metadata)

    info = CommandInfo(
        name=command_name,
        func=actual_func,
        description=description or (actual_func.__doc__ if actual_func else None),
        aliases=aliases or [],
        hidden=hidden,
        category=category,
        metadata=cmd_metadata,
        parent=parent,
    )

    # Build full registry key
    full_name = f"{parent}.{command_name}" if parent else command_name

    # Build registry metadata
    reg_metadata = {
        "info": info,
        "description": info.description,
        "aliases": info.aliases,
        "hidden": hidden,
        "category": category,
        "parent": parent,
        "is_group": group,
        "_prebuilt_click_command": click_cmd,  # Use new, clearer name
    }
    reg_metadata.update(extra_metadata)

    # Register in the registry
    reg.register(
        name=full_name,
        value=func,
        dimension=ComponentCategory.COMMAND.value,
        metadata=reg_metadata,
        aliases=aliases,
        replace=replace,
    )

    # Add metadata to the function
    func.__registry_name__ = command_name  # type: ignore[attr-defined]
    func.__registry_dimension__ = ComponentCategory.COMMAND.value  # type: ignore[attr-defined]
    func.__registry_info__ = info  # type: ignore[attr-defined]

    get_foundation_logger().trace(f"Registered command: {full_name}")

    return func


def x__register_command_func__mutmut_36(
    func: F,
    *,
    name: str | None = None,
    description: str | None = None,
    aliases: list[str] | None = None,
    hidden: bool = False,
    category: str | None = None,
    group: bool = False,
    replace: bool = False,
    registry: Registry | None = None,
    **extra_metadata: Any,
) -> F:
    """Internal function to register a command."""
    reg = registry or get_command_registry()

    # Determine command name and parent from dot notation
    if name:
        parts = name.split(".")
        if len(parts) > 1:
            # Extract parent path and command name
            parent = ".".join(parts[:-1])
            command_name = parts[-1]

            # Auto-create parent groups if they don't exist (click only)
            _, has_click = _get_click()
            if has_click:
                ensure_parent_groups_fn = _get_ensure_parent_groups()
                if ensure_parent_groups_fn:
                    ensure_parent_groups_fn(parent, reg)
        else:
            parent = None
            command_name = name
    else:
        # Use function name as command name
        parent = None
        command_name = getattr(func, "__NAME__", "<anonymous>")

    # Check if it's already a Click command
    click_cmd = None
    click_module, has_click = _get_click()
    if has_click and isinstance(func, click_module.Command):
        click_cmd = func
        actual_func = func.callback
    else:
        actual_func = func

    # Create command info
    cmd_metadata = {"is_group": group}
    cmd_metadata.update(extra_metadata)

    info = CommandInfo(
        name=command_name,
        func=actual_func,
        description=description or (actual_func.__doc__ if actual_func else None),
        aliases=aliases or [],
        hidden=hidden,
        category=category,
        metadata=cmd_metadata,
        parent=parent,
    )

    # Build full registry key
    full_name = f"{parent}.{command_name}" if parent else command_name

    # Build registry metadata
    reg_metadata = {
        "info": info,
        "description": info.description,
        "aliases": info.aliases,
        "hidden": hidden,
        "category": category,
        "parent": parent,
        "is_group": group,
        "_prebuilt_click_command": click_cmd,  # Use new, clearer name
    }
    reg_metadata.update(extra_metadata)

    # Register in the registry
    reg.register(
        name=full_name,
        value=func,
        dimension=ComponentCategory.COMMAND.value,
        metadata=reg_metadata,
        aliases=aliases,
        replace=replace,
    )

    # Add metadata to the function
    func.__registry_name__ = command_name  # type: ignore[attr-defined]
    func.__registry_dimension__ = ComponentCategory.COMMAND.value  # type: ignore[attr-defined]
    func.__registry_info__ = info  # type: ignore[attr-defined]

    get_foundation_logger().trace(f"Registered command: {full_name}")

    return func


def x__register_command_func__mutmut_37(
    func: F,
    *,
    name: str | None = None,
    description: str | None = None,
    aliases: list[str] | None = None,
    hidden: bool = False,
    category: str | None = None,
    group: bool = False,
    replace: bool = False,
    registry: Registry | None = None,
    **extra_metadata: Any,
) -> F:
    """Internal function to register a command."""
    reg = registry or get_command_registry()

    # Determine command name and parent from dot notation
    if name:
        parts = name.split(".")
        if len(parts) > 1:
            # Extract parent path and command name
            parent = ".".join(parts[:-1])
            command_name = parts[-1]

            # Auto-create parent groups if they don't exist (click only)
            _, has_click = _get_click()
            if has_click:
                ensure_parent_groups_fn = _get_ensure_parent_groups()
                if ensure_parent_groups_fn:
                    ensure_parent_groups_fn(parent, reg)
        else:
            parent = None
            command_name = name
    else:
        # Use function name as command name
        parent = None
        command_name = getattr(func, "__name__", "XX<anonymous>XX")

    # Check if it's already a Click command
    click_cmd = None
    click_module, has_click = _get_click()
    if has_click and isinstance(func, click_module.Command):
        click_cmd = func
        actual_func = func.callback
    else:
        actual_func = func

    # Create command info
    cmd_metadata = {"is_group": group}
    cmd_metadata.update(extra_metadata)

    info = CommandInfo(
        name=command_name,
        func=actual_func,
        description=description or (actual_func.__doc__ if actual_func else None),
        aliases=aliases or [],
        hidden=hidden,
        category=category,
        metadata=cmd_metadata,
        parent=parent,
    )

    # Build full registry key
    full_name = f"{parent}.{command_name}" if parent else command_name

    # Build registry metadata
    reg_metadata = {
        "info": info,
        "description": info.description,
        "aliases": info.aliases,
        "hidden": hidden,
        "category": category,
        "parent": parent,
        "is_group": group,
        "_prebuilt_click_command": click_cmd,  # Use new, clearer name
    }
    reg_metadata.update(extra_metadata)

    # Register in the registry
    reg.register(
        name=full_name,
        value=func,
        dimension=ComponentCategory.COMMAND.value,
        metadata=reg_metadata,
        aliases=aliases,
        replace=replace,
    )

    # Add metadata to the function
    func.__registry_name__ = command_name  # type: ignore[attr-defined]
    func.__registry_dimension__ = ComponentCategory.COMMAND.value  # type: ignore[attr-defined]
    func.__registry_info__ = info  # type: ignore[attr-defined]

    get_foundation_logger().trace(f"Registered command: {full_name}")

    return func


def x__register_command_func__mutmut_38(
    func: F,
    *,
    name: str | None = None,
    description: str | None = None,
    aliases: list[str] | None = None,
    hidden: bool = False,
    category: str | None = None,
    group: bool = False,
    replace: bool = False,
    registry: Registry | None = None,
    **extra_metadata: Any,
) -> F:
    """Internal function to register a command."""
    reg = registry or get_command_registry()

    # Determine command name and parent from dot notation
    if name:
        parts = name.split(".")
        if len(parts) > 1:
            # Extract parent path and command name
            parent = ".".join(parts[:-1])
            command_name = parts[-1]

            # Auto-create parent groups if they don't exist (click only)
            _, has_click = _get_click()
            if has_click:
                ensure_parent_groups_fn = _get_ensure_parent_groups()
                if ensure_parent_groups_fn:
                    ensure_parent_groups_fn(parent, reg)
        else:
            parent = None
            command_name = name
    else:
        # Use function name as command name
        parent = None
        command_name = getattr(func, "__name__", "<ANONYMOUS>")

    # Check if it's already a Click command
    click_cmd = None
    click_module, has_click = _get_click()
    if has_click and isinstance(func, click_module.Command):
        click_cmd = func
        actual_func = func.callback
    else:
        actual_func = func

    # Create command info
    cmd_metadata = {"is_group": group}
    cmd_metadata.update(extra_metadata)

    info = CommandInfo(
        name=command_name,
        func=actual_func,
        description=description or (actual_func.__doc__ if actual_func else None),
        aliases=aliases or [],
        hidden=hidden,
        category=category,
        metadata=cmd_metadata,
        parent=parent,
    )

    # Build full registry key
    full_name = f"{parent}.{command_name}" if parent else command_name

    # Build registry metadata
    reg_metadata = {
        "info": info,
        "description": info.description,
        "aliases": info.aliases,
        "hidden": hidden,
        "category": category,
        "parent": parent,
        "is_group": group,
        "_prebuilt_click_command": click_cmd,  # Use new, clearer name
    }
    reg_metadata.update(extra_metadata)

    # Register in the registry
    reg.register(
        name=full_name,
        value=func,
        dimension=ComponentCategory.COMMAND.value,
        metadata=reg_metadata,
        aliases=aliases,
        replace=replace,
    )

    # Add metadata to the function
    func.__registry_name__ = command_name  # type: ignore[attr-defined]
    func.__registry_dimension__ = ComponentCategory.COMMAND.value  # type: ignore[attr-defined]
    func.__registry_info__ = info  # type: ignore[attr-defined]

    get_foundation_logger().trace(f"Registered command: {full_name}")

    return func


def x__register_command_func__mutmut_39(
    func: F,
    *,
    name: str | None = None,
    description: str | None = None,
    aliases: list[str] | None = None,
    hidden: bool = False,
    category: str | None = None,
    group: bool = False,
    replace: bool = False,
    registry: Registry | None = None,
    **extra_metadata: Any,
) -> F:
    """Internal function to register a command."""
    reg = registry or get_command_registry()

    # Determine command name and parent from dot notation
    if name:
        parts = name.split(".")
        if len(parts) > 1:
            # Extract parent path and command name
            parent = ".".join(parts[:-1])
            command_name = parts[-1]

            # Auto-create parent groups if they don't exist (click only)
            _, has_click = _get_click()
            if has_click:
                ensure_parent_groups_fn = _get_ensure_parent_groups()
                if ensure_parent_groups_fn:
                    ensure_parent_groups_fn(parent, reg)
        else:
            parent = None
            command_name = name
    else:
        # Use function name as command name
        parent = None
        command_name = getattr(func, "__name__", "<anonymous>")

    # Check if it's already a Click command
    click_cmd = ""
    click_module, has_click = _get_click()
    if has_click and isinstance(func, click_module.Command):
        click_cmd = func
        actual_func = func.callback
    else:
        actual_func = func

    # Create command info
    cmd_metadata = {"is_group": group}
    cmd_metadata.update(extra_metadata)

    info = CommandInfo(
        name=command_name,
        func=actual_func,
        description=description or (actual_func.__doc__ if actual_func else None),
        aliases=aliases or [],
        hidden=hidden,
        category=category,
        metadata=cmd_metadata,
        parent=parent,
    )

    # Build full registry key
    full_name = f"{parent}.{command_name}" if parent else command_name

    # Build registry metadata
    reg_metadata = {
        "info": info,
        "description": info.description,
        "aliases": info.aliases,
        "hidden": hidden,
        "category": category,
        "parent": parent,
        "is_group": group,
        "_prebuilt_click_command": click_cmd,  # Use new, clearer name
    }
    reg_metadata.update(extra_metadata)

    # Register in the registry
    reg.register(
        name=full_name,
        value=func,
        dimension=ComponentCategory.COMMAND.value,
        metadata=reg_metadata,
        aliases=aliases,
        replace=replace,
    )

    # Add metadata to the function
    func.__registry_name__ = command_name  # type: ignore[attr-defined]
    func.__registry_dimension__ = ComponentCategory.COMMAND.value  # type: ignore[attr-defined]
    func.__registry_info__ = info  # type: ignore[attr-defined]

    get_foundation_logger().trace(f"Registered command: {full_name}")

    return func


def x__register_command_func__mutmut_40(
    func: F,
    *,
    name: str | None = None,
    description: str | None = None,
    aliases: list[str] | None = None,
    hidden: bool = False,
    category: str | None = None,
    group: bool = False,
    replace: bool = False,
    registry: Registry | None = None,
    **extra_metadata: Any,
) -> F:
    """Internal function to register a command."""
    reg = registry or get_command_registry()

    # Determine command name and parent from dot notation
    if name:
        parts = name.split(".")
        if len(parts) > 1:
            # Extract parent path and command name
            parent = ".".join(parts[:-1])
            command_name = parts[-1]

            # Auto-create parent groups if they don't exist (click only)
            _, has_click = _get_click()
            if has_click:
                ensure_parent_groups_fn = _get_ensure_parent_groups()
                if ensure_parent_groups_fn:
                    ensure_parent_groups_fn(parent, reg)
        else:
            parent = None
            command_name = name
    else:
        # Use function name as command name
        parent = None
        command_name = getattr(func, "__name__", "<anonymous>")

    # Check if it's already a Click command
    click_cmd = None
    click_module, has_click = None
    if has_click and isinstance(func, click_module.Command):
        click_cmd = func
        actual_func = func.callback
    else:
        actual_func = func

    # Create command info
    cmd_metadata = {"is_group": group}
    cmd_metadata.update(extra_metadata)

    info = CommandInfo(
        name=command_name,
        func=actual_func,
        description=description or (actual_func.__doc__ if actual_func else None),
        aliases=aliases or [],
        hidden=hidden,
        category=category,
        metadata=cmd_metadata,
        parent=parent,
    )

    # Build full registry key
    full_name = f"{parent}.{command_name}" if parent else command_name

    # Build registry metadata
    reg_metadata = {
        "info": info,
        "description": info.description,
        "aliases": info.aliases,
        "hidden": hidden,
        "category": category,
        "parent": parent,
        "is_group": group,
        "_prebuilt_click_command": click_cmd,  # Use new, clearer name
    }
    reg_metadata.update(extra_metadata)

    # Register in the registry
    reg.register(
        name=full_name,
        value=func,
        dimension=ComponentCategory.COMMAND.value,
        metadata=reg_metadata,
        aliases=aliases,
        replace=replace,
    )

    # Add metadata to the function
    func.__registry_name__ = command_name  # type: ignore[attr-defined]
    func.__registry_dimension__ = ComponentCategory.COMMAND.value  # type: ignore[attr-defined]
    func.__registry_info__ = info  # type: ignore[attr-defined]

    get_foundation_logger().trace(f"Registered command: {full_name}")

    return func


def x__register_command_func__mutmut_41(
    func: F,
    *,
    name: str | None = None,
    description: str | None = None,
    aliases: list[str] | None = None,
    hidden: bool = False,
    category: str | None = None,
    group: bool = False,
    replace: bool = False,
    registry: Registry | None = None,
    **extra_metadata: Any,
) -> F:
    """Internal function to register a command."""
    reg = registry or get_command_registry()

    # Determine command name and parent from dot notation
    if name:
        parts = name.split(".")
        if len(parts) > 1:
            # Extract parent path and command name
            parent = ".".join(parts[:-1])
            command_name = parts[-1]

            # Auto-create parent groups if they don't exist (click only)
            _, has_click = _get_click()
            if has_click:
                ensure_parent_groups_fn = _get_ensure_parent_groups()
                if ensure_parent_groups_fn:
                    ensure_parent_groups_fn(parent, reg)
        else:
            parent = None
            command_name = name
    else:
        # Use function name as command name
        parent = None
        command_name = getattr(func, "__name__", "<anonymous>")

    # Check if it's already a Click command
    click_cmd = None
    click_module, has_click = _get_click()
    if has_click or isinstance(func, click_module.Command):
        click_cmd = func
        actual_func = func.callback
    else:
        actual_func = func

    # Create command info
    cmd_metadata = {"is_group": group}
    cmd_metadata.update(extra_metadata)

    info = CommandInfo(
        name=command_name,
        func=actual_func,
        description=description or (actual_func.__doc__ if actual_func else None),
        aliases=aliases or [],
        hidden=hidden,
        category=category,
        metadata=cmd_metadata,
        parent=parent,
    )

    # Build full registry key
    full_name = f"{parent}.{command_name}" if parent else command_name

    # Build registry metadata
    reg_metadata = {
        "info": info,
        "description": info.description,
        "aliases": info.aliases,
        "hidden": hidden,
        "category": category,
        "parent": parent,
        "is_group": group,
        "_prebuilt_click_command": click_cmd,  # Use new, clearer name
    }
    reg_metadata.update(extra_metadata)

    # Register in the registry
    reg.register(
        name=full_name,
        value=func,
        dimension=ComponentCategory.COMMAND.value,
        metadata=reg_metadata,
        aliases=aliases,
        replace=replace,
    )

    # Add metadata to the function
    func.__registry_name__ = command_name  # type: ignore[attr-defined]
    func.__registry_dimension__ = ComponentCategory.COMMAND.value  # type: ignore[attr-defined]
    func.__registry_info__ = info  # type: ignore[attr-defined]

    get_foundation_logger().trace(f"Registered command: {full_name}")

    return func


def x__register_command_func__mutmut_42(
    func: F,
    *,
    name: str | None = None,
    description: str | None = None,
    aliases: list[str] | None = None,
    hidden: bool = False,
    category: str | None = None,
    group: bool = False,
    replace: bool = False,
    registry: Registry | None = None,
    **extra_metadata: Any,
) -> F:
    """Internal function to register a command."""
    reg = registry or get_command_registry()

    # Determine command name and parent from dot notation
    if name:
        parts = name.split(".")
        if len(parts) > 1:
            # Extract parent path and command name
            parent = ".".join(parts[:-1])
            command_name = parts[-1]

            # Auto-create parent groups if they don't exist (click only)
            _, has_click = _get_click()
            if has_click:
                ensure_parent_groups_fn = _get_ensure_parent_groups()
                if ensure_parent_groups_fn:
                    ensure_parent_groups_fn(parent, reg)
        else:
            parent = None
            command_name = name
    else:
        # Use function name as command name
        parent = None
        command_name = getattr(func, "__name__", "<anonymous>")

    # Check if it's already a Click command
    click_cmd = None
    click_module, has_click = _get_click()
    if has_click and isinstance(func, click_module.Command):
        click_cmd = None
        actual_func = func.callback
    else:
        actual_func = func

    # Create command info
    cmd_metadata = {"is_group": group}
    cmd_metadata.update(extra_metadata)

    info = CommandInfo(
        name=command_name,
        func=actual_func,
        description=description or (actual_func.__doc__ if actual_func else None),
        aliases=aliases or [],
        hidden=hidden,
        category=category,
        metadata=cmd_metadata,
        parent=parent,
    )

    # Build full registry key
    full_name = f"{parent}.{command_name}" if parent else command_name

    # Build registry metadata
    reg_metadata = {
        "info": info,
        "description": info.description,
        "aliases": info.aliases,
        "hidden": hidden,
        "category": category,
        "parent": parent,
        "is_group": group,
        "_prebuilt_click_command": click_cmd,  # Use new, clearer name
    }
    reg_metadata.update(extra_metadata)

    # Register in the registry
    reg.register(
        name=full_name,
        value=func,
        dimension=ComponentCategory.COMMAND.value,
        metadata=reg_metadata,
        aliases=aliases,
        replace=replace,
    )

    # Add metadata to the function
    func.__registry_name__ = command_name  # type: ignore[attr-defined]
    func.__registry_dimension__ = ComponentCategory.COMMAND.value  # type: ignore[attr-defined]
    func.__registry_info__ = info  # type: ignore[attr-defined]

    get_foundation_logger().trace(f"Registered command: {full_name}")

    return func


def x__register_command_func__mutmut_43(
    func: F,
    *,
    name: str | None = None,
    description: str | None = None,
    aliases: list[str] | None = None,
    hidden: bool = False,
    category: str | None = None,
    group: bool = False,
    replace: bool = False,
    registry: Registry | None = None,
    **extra_metadata: Any,
) -> F:
    """Internal function to register a command."""
    reg = registry or get_command_registry()

    # Determine command name and parent from dot notation
    if name:
        parts = name.split(".")
        if len(parts) > 1:
            # Extract parent path and command name
            parent = ".".join(parts[:-1])
            command_name = parts[-1]

            # Auto-create parent groups if they don't exist (click only)
            _, has_click = _get_click()
            if has_click:
                ensure_parent_groups_fn = _get_ensure_parent_groups()
                if ensure_parent_groups_fn:
                    ensure_parent_groups_fn(parent, reg)
        else:
            parent = None
            command_name = name
    else:
        # Use function name as command name
        parent = None
        command_name = getattr(func, "__name__", "<anonymous>")

    # Check if it's already a Click command
    click_cmd = None
    click_module, has_click = _get_click()
    if has_click and isinstance(func, click_module.Command):
        click_cmd = func
        actual_func = None
    else:
        actual_func = func

    # Create command info
    cmd_metadata = {"is_group": group}
    cmd_metadata.update(extra_metadata)

    info = CommandInfo(
        name=command_name,
        func=actual_func,
        description=description or (actual_func.__doc__ if actual_func else None),
        aliases=aliases or [],
        hidden=hidden,
        category=category,
        metadata=cmd_metadata,
        parent=parent,
    )

    # Build full registry key
    full_name = f"{parent}.{command_name}" if parent else command_name

    # Build registry metadata
    reg_metadata = {
        "info": info,
        "description": info.description,
        "aliases": info.aliases,
        "hidden": hidden,
        "category": category,
        "parent": parent,
        "is_group": group,
        "_prebuilt_click_command": click_cmd,  # Use new, clearer name
    }
    reg_metadata.update(extra_metadata)

    # Register in the registry
    reg.register(
        name=full_name,
        value=func,
        dimension=ComponentCategory.COMMAND.value,
        metadata=reg_metadata,
        aliases=aliases,
        replace=replace,
    )

    # Add metadata to the function
    func.__registry_name__ = command_name  # type: ignore[attr-defined]
    func.__registry_dimension__ = ComponentCategory.COMMAND.value  # type: ignore[attr-defined]
    func.__registry_info__ = info  # type: ignore[attr-defined]

    get_foundation_logger().trace(f"Registered command: {full_name}")

    return func


def x__register_command_func__mutmut_44(
    func: F,
    *,
    name: str | None = None,
    description: str | None = None,
    aliases: list[str] | None = None,
    hidden: bool = False,
    category: str | None = None,
    group: bool = False,
    replace: bool = False,
    registry: Registry | None = None,
    **extra_metadata: Any,
) -> F:
    """Internal function to register a command."""
    reg = registry or get_command_registry()

    # Determine command name and parent from dot notation
    if name:
        parts = name.split(".")
        if len(parts) > 1:
            # Extract parent path and command name
            parent = ".".join(parts[:-1])
            command_name = parts[-1]

            # Auto-create parent groups if they don't exist (click only)
            _, has_click = _get_click()
            if has_click:
                ensure_parent_groups_fn = _get_ensure_parent_groups()
                if ensure_parent_groups_fn:
                    ensure_parent_groups_fn(parent, reg)
        else:
            parent = None
            command_name = name
    else:
        # Use function name as command name
        parent = None
        command_name = getattr(func, "__name__", "<anonymous>")

    # Check if it's already a Click command
    click_cmd = None
    click_module, has_click = _get_click()
    if has_click and isinstance(func, click_module.Command):
        click_cmd = func
        actual_func = func.callback
    else:
        actual_func = None

    # Create command info
    cmd_metadata = {"is_group": group}
    cmd_metadata.update(extra_metadata)

    info = CommandInfo(
        name=command_name,
        func=actual_func,
        description=description or (actual_func.__doc__ if actual_func else None),
        aliases=aliases or [],
        hidden=hidden,
        category=category,
        metadata=cmd_metadata,
        parent=parent,
    )

    # Build full registry key
    full_name = f"{parent}.{command_name}" if parent else command_name

    # Build registry metadata
    reg_metadata = {
        "info": info,
        "description": info.description,
        "aliases": info.aliases,
        "hidden": hidden,
        "category": category,
        "parent": parent,
        "is_group": group,
        "_prebuilt_click_command": click_cmd,  # Use new, clearer name
    }
    reg_metadata.update(extra_metadata)

    # Register in the registry
    reg.register(
        name=full_name,
        value=func,
        dimension=ComponentCategory.COMMAND.value,
        metadata=reg_metadata,
        aliases=aliases,
        replace=replace,
    )

    # Add metadata to the function
    func.__registry_name__ = command_name  # type: ignore[attr-defined]
    func.__registry_dimension__ = ComponentCategory.COMMAND.value  # type: ignore[attr-defined]
    func.__registry_info__ = info  # type: ignore[attr-defined]

    get_foundation_logger().trace(f"Registered command: {full_name}")

    return func


def x__register_command_func__mutmut_45(
    func: F,
    *,
    name: str | None = None,
    description: str | None = None,
    aliases: list[str] | None = None,
    hidden: bool = False,
    category: str | None = None,
    group: bool = False,
    replace: bool = False,
    registry: Registry | None = None,
    **extra_metadata: Any,
) -> F:
    """Internal function to register a command."""
    reg = registry or get_command_registry()

    # Determine command name and parent from dot notation
    if name:
        parts = name.split(".")
        if len(parts) > 1:
            # Extract parent path and command name
            parent = ".".join(parts[:-1])
            command_name = parts[-1]

            # Auto-create parent groups if they don't exist (click only)
            _, has_click = _get_click()
            if has_click:
                ensure_parent_groups_fn = _get_ensure_parent_groups()
                if ensure_parent_groups_fn:
                    ensure_parent_groups_fn(parent, reg)
        else:
            parent = None
            command_name = name
    else:
        # Use function name as command name
        parent = None
        command_name = getattr(func, "__name__", "<anonymous>")

    # Check if it's already a Click command
    click_cmd = None
    click_module, has_click = _get_click()
    if has_click and isinstance(func, click_module.Command):
        click_cmd = func
        actual_func = func.callback
    else:
        actual_func = func

    # Create command info
    cmd_metadata = None
    cmd_metadata.update(extra_metadata)

    info = CommandInfo(
        name=command_name,
        func=actual_func,
        description=description or (actual_func.__doc__ if actual_func else None),
        aliases=aliases or [],
        hidden=hidden,
        category=category,
        metadata=cmd_metadata,
        parent=parent,
    )

    # Build full registry key
    full_name = f"{parent}.{command_name}" if parent else command_name

    # Build registry metadata
    reg_metadata = {
        "info": info,
        "description": info.description,
        "aliases": info.aliases,
        "hidden": hidden,
        "category": category,
        "parent": parent,
        "is_group": group,
        "_prebuilt_click_command": click_cmd,  # Use new, clearer name
    }
    reg_metadata.update(extra_metadata)

    # Register in the registry
    reg.register(
        name=full_name,
        value=func,
        dimension=ComponentCategory.COMMAND.value,
        metadata=reg_metadata,
        aliases=aliases,
        replace=replace,
    )

    # Add metadata to the function
    func.__registry_name__ = command_name  # type: ignore[attr-defined]
    func.__registry_dimension__ = ComponentCategory.COMMAND.value  # type: ignore[attr-defined]
    func.__registry_info__ = info  # type: ignore[attr-defined]

    get_foundation_logger().trace(f"Registered command: {full_name}")

    return func


def x__register_command_func__mutmut_46(
    func: F,
    *,
    name: str | None = None,
    description: str | None = None,
    aliases: list[str] | None = None,
    hidden: bool = False,
    category: str | None = None,
    group: bool = False,
    replace: bool = False,
    registry: Registry | None = None,
    **extra_metadata: Any,
) -> F:
    """Internal function to register a command."""
    reg = registry or get_command_registry()

    # Determine command name and parent from dot notation
    if name:
        parts = name.split(".")
        if len(parts) > 1:
            # Extract parent path and command name
            parent = ".".join(parts[:-1])
            command_name = parts[-1]

            # Auto-create parent groups if they don't exist (click only)
            _, has_click = _get_click()
            if has_click:
                ensure_parent_groups_fn = _get_ensure_parent_groups()
                if ensure_parent_groups_fn:
                    ensure_parent_groups_fn(parent, reg)
        else:
            parent = None
            command_name = name
    else:
        # Use function name as command name
        parent = None
        command_name = getattr(func, "__name__", "<anonymous>")

    # Check if it's already a Click command
    click_cmd = None
    click_module, has_click = _get_click()
    if has_click and isinstance(func, click_module.Command):
        click_cmd = func
        actual_func = func.callback
    else:
        actual_func = func

    # Create command info
    cmd_metadata = {"XXis_groupXX": group}
    cmd_metadata.update(extra_metadata)

    info = CommandInfo(
        name=command_name,
        func=actual_func,
        description=description or (actual_func.__doc__ if actual_func else None),
        aliases=aliases or [],
        hidden=hidden,
        category=category,
        metadata=cmd_metadata,
        parent=parent,
    )

    # Build full registry key
    full_name = f"{parent}.{command_name}" if parent else command_name

    # Build registry metadata
    reg_metadata = {
        "info": info,
        "description": info.description,
        "aliases": info.aliases,
        "hidden": hidden,
        "category": category,
        "parent": parent,
        "is_group": group,
        "_prebuilt_click_command": click_cmd,  # Use new, clearer name
    }
    reg_metadata.update(extra_metadata)

    # Register in the registry
    reg.register(
        name=full_name,
        value=func,
        dimension=ComponentCategory.COMMAND.value,
        metadata=reg_metadata,
        aliases=aliases,
        replace=replace,
    )

    # Add metadata to the function
    func.__registry_name__ = command_name  # type: ignore[attr-defined]
    func.__registry_dimension__ = ComponentCategory.COMMAND.value  # type: ignore[attr-defined]
    func.__registry_info__ = info  # type: ignore[attr-defined]

    get_foundation_logger().trace(f"Registered command: {full_name}")

    return func


def x__register_command_func__mutmut_47(
    func: F,
    *,
    name: str | None = None,
    description: str | None = None,
    aliases: list[str] | None = None,
    hidden: bool = False,
    category: str | None = None,
    group: bool = False,
    replace: bool = False,
    registry: Registry | None = None,
    **extra_metadata: Any,
) -> F:
    """Internal function to register a command."""
    reg = registry or get_command_registry()

    # Determine command name and parent from dot notation
    if name:
        parts = name.split(".")
        if len(parts) > 1:
            # Extract parent path and command name
            parent = ".".join(parts[:-1])
            command_name = parts[-1]

            # Auto-create parent groups if they don't exist (click only)
            _, has_click = _get_click()
            if has_click:
                ensure_parent_groups_fn = _get_ensure_parent_groups()
                if ensure_parent_groups_fn:
                    ensure_parent_groups_fn(parent, reg)
        else:
            parent = None
            command_name = name
    else:
        # Use function name as command name
        parent = None
        command_name = getattr(func, "__name__", "<anonymous>")

    # Check if it's already a Click command
    click_cmd = None
    click_module, has_click = _get_click()
    if has_click and isinstance(func, click_module.Command):
        click_cmd = func
        actual_func = func.callback
    else:
        actual_func = func

    # Create command info
    cmd_metadata = {"IS_GROUP": group}
    cmd_metadata.update(extra_metadata)

    info = CommandInfo(
        name=command_name,
        func=actual_func,
        description=description or (actual_func.__doc__ if actual_func else None),
        aliases=aliases or [],
        hidden=hidden,
        category=category,
        metadata=cmd_metadata,
        parent=parent,
    )

    # Build full registry key
    full_name = f"{parent}.{command_name}" if parent else command_name

    # Build registry metadata
    reg_metadata = {
        "info": info,
        "description": info.description,
        "aliases": info.aliases,
        "hidden": hidden,
        "category": category,
        "parent": parent,
        "is_group": group,
        "_prebuilt_click_command": click_cmd,  # Use new, clearer name
    }
    reg_metadata.update(extra_metadata)

    # Register in the registry
    reg.register(
        name=full_name,
        value=func,
        dimension=ComponentCategory.COMMAND.value,
        metadata=reg_metadata,
        aliases=aliases,
        replace=replace,
    )

    # Add metadata to the function
    func.__registry_name__ = command_name  # type: ignore[attr-defined]
    func.__registry_dimension__ = ComponentCategory.COMMAND.value  # type: ignore[attr-defined]
    func.__registry_info__ = info  # type: ignore[attr-defined]

    get_foundation_logger().trace(f"Registered command: {full_name}")

    return func


def x__register_command_func__mutmut_48(
    func: F,
    *,
    name: str | None = None,
    description: str | None = None,
    aliases: list[str] | None = None,
    hidden: bool = False,
    category: str | None = None,
    group: bool = False,
    replace: bool = False,
    registry: Registry | None = None,
    **extra_metadata: Any,
) -> F:
    """Internal function to register a command."""
    reg = registry or get_command_registry()

    # Determine command name and parent from dot notation
    if name:
        parts = name.split(".")
        if len(parts) > 1:
            # Extract parent path and command name
            parent = ".".join(parts[:-1])
            command_name = parts[-1]

            # Auto-create parent groups if they don't exist (click only)
            _, has_click = _get_click()
            if has_click:
                ensure_parent_groups_fn = _get_ensure_parent_groups()
                if ensure_parent_groups_fn:
                    ensure_parent_groups_fn(parent, reg)
        else:
            parent = None
            command_name = name
    else:
        # Use function name as command name
        parent = None
        command_name = getattr(func, "__name__", "<anonymous>")

    # Check if it's already a Click command
    click_cmd = None
    click_module, has_click = _get_click()
    if has_click and isinstance(func, click_module.Command):
        click_cmd = func
        actual_func = func.callback
    else:
        actual_func = func

    # Create command info
    cmd_metadata = {"is_group": group}
    cmd_metadata.update(None)

    info = CommandInfo(
        name=command_name,
        func=actual_func,
        description=description or (actual_func.__doc__ if actual_func else None),
        aliases=aliases or [],
        hidden=hidden,
        category=category,
        metadata=cmd_metadata,
        parent=parent,
    )

    # Build full registry key
    full_name = f"{parent}.{command_name}" if parent else command_name

    # Build registry metadata
    reg_metadata = {
        "info": info,
        "description": info.description,
        "aliases": info.aliases,
        "hidden": hidden,
        "category": category,
        "parent": parent,
        "is_group": group,
        "_prebuilt_click_command": click_cmd,  # Use new, clearer name
    }
    reg_metadata.update(extra_metadata)

    # Register in the registry
    reg.register(
        name=full_name,
        value=func,
        dimension=ComponentCategory.COMMAND.value,
        metadata=reg_metadata,
        aliases=aliases,
        replace=replace,
    )

    # Add metadata to the function
    func.__registry_name__ = command_name  # type: ignore[attr-defined]
    func.__registry_dimension__ = ComponentCategory.COMMAND.value  # type: ignore[attr-defined]
    func.__registry_info__ = info  # type: ignore[attr-defined]

    get_foundation_logger().trace(f"Registered command: {full_name}")

    return func


def x__register_command_func__mutmut_49(
    func: F,
    *,
    name: str | None = None,
    description: str | None = None,
    aliases: list[str] | None = None,
    hidden: bool = False,
    category: str | None = None,
    group: bool = False,
    replace: bool = False,
    registry: Registry | None = None,
    **extra_metadata: Any,
) -> F:
    """Internal function to register a command."""
    reg = registry or get_command_registry()

    # Determine command name and parent from dot notation
    if name:
        parts = name.split(".")
        if len(parts) > 1:
            # Extract parent path and command name
            parent = ".".join(parts[:-1])
            command_name = parts[-1]

            # Auto-create parent groups if they don't exist (click only)
            _, has_click = _get_click()
            if has_click:
                ensure_parent_groups_fn = _get_ensure_parent_groups()
                if ensure_parent_groups_fn:
                    ensure_parent_groups_fn(parent, reg)
        else:
            parent = None
            command_name = name
    else:
        # Use function name as command name
        parent = None
        command_name = getattr(func, "__name__", "<anonymous>")

    # Check if it's already a Click command
    click_cmd = None
    click_module, has_click = _get_click()
    if has_click and isinstance(func, click_module.Command):
        click_cmd = func
        actual_func = func.callback
    else:
        actual_func = func

    # Create command info
    cmd_metadata = {"is_group": group}
    cmd_metadata.update(extra_metadata)

    info = None

    # Build full registry key
    full_name = f"{parent}.{command_name}" if parent else command_name

    # Build registry metadata
    reg_metadata = {
        "info": info,
        "description": info.description,
        "aliases": info.aliases,
        "hidden": hidden,
        "category": category,
        "parent": parent,
        "is_group": group,
        "_prebuilt_click_command": click_cmd,  # Use new, clearer name
    }
    reg_metadata.update(extra_metadata)

    # Register in the registry
    reg.register(
        name=full_name,
        value=func,
        dimension=ComponentCategory.COMMAND.value,
        metadata=reg_metadata,
        aliases=aliases,
        replace=replace,
    )

    # Add metadata to the function
    func.__registry_name__ = command_name  # type: ignore[attr-defined]
    func.__registry_dimension__ = ComponentCategory.COMMAND.value  # type: ignore[attr-defined]
    func.__registry_info__ = info  # type: ignore[attr-defined]

    get_foundation_logger().trace(f"Registered command: {full_name}")

    return func


def x__register_command_func__mutmut_50(
    func: F,
    *,
    name: str | None = None,
    description: str | None = None,
    aliases: list[str] | None = None,
    hidden: bool = False,
    category: str | None = None,
    group: bool = False,
    replace: bool = False,
    registry: Registry | None = None,
    **extra_metadata: Any,
) -> F:
    """Internal function to register a command."""
    reg = registry or get_command_registry()

    # Determine command name and parent from dot notation
    if name:
        parts = name.split(".")
        if len(parts) > 1:
            # Extract parent path and command name
            parent = ".".join(parts[:-1])
            command_name = parts[-1]

            # Auto-create parent groups if they don't exist (click only)
            _, has_click = _get_click()
            if has_click:
                ensure_parent_groups_fn = _get_ensure_parent_groups()
                if ensure_parent_groups_fn:
                    ensure_parent_groups_fn(parent, reg)
        else:
            parent = None
            command_name = name
    else:
        # Use function name as command name
        parent = None
        command_name = getattr(func, "__name__", "<anonymous>")

    # Check if it's already a Click command
    click_cmd = None
    click_module, has_click = _get_click()
    if has_click and isinstance(func, click_module.Command):
        click_cmd = func
        actual_func = func.callback
    else:
        actual_func = func

    # Create command info
    cmd_metadata = {"is_group": group}
    cmd_metadata.update(extra_metadata)

    info = CommandInfo(
        name=None,
        func=actual_func,
        description=description or (actual_func.__doc__ if actual_func else None),
        aliases=aliases or [],
        hidden=hidden,
        category=category,
        metadata=cmd_metadata,
        parent=parent,
    )

    # Build full registry key
    full_name = f"{parent}.{command_name}" if parent else command_name

    # Build registry metadata
    reg_metadata = {
        "info": info,
        "description": info.description,
        "aliases": info.aliases,
        "hidden": hidden,
        "category": category,
        "parent": parent,
        "is_group": group,
        "_prebuilt_click_command": click_cmd,  # Use new, clearer name
    }
    reg_metadata.update(extra_metadata)

    # Register in the registry
    reg.register(
        name=full_name,
        value=func,
        dimension=ComponentCategory.COMMAND.value,
        metadata=reg_metadata,
        aliases=aliases,
        replace=replace,
    )

    # Add metadata to the function
    func.__registry_name__ = command_name  # type: ignore[attr-defined]
    func.__registry_dimension__ = ComponentCategory.COMMAND.value  # type: ignore[attr-defined]
    func.__registry_info__ = info  # type: ignore[attr-defined]

    get_foundation_logger().trace(f"Registered command: {full_name}")

    return func


def x__register_command_func__mutmut_51(
    func: F,
    *,
    name: str | None = None,
    description: str | None = None,
    aliases: list[str] | None = None,
    hidden: bool = False,
    category: str | None = None,
    group: bool = False,
    replace: bool = False,
    registry: Registry | None = None,
    **extra_metadata: Any,
) -> F:
    """Internal function to register a command."""
    reg = registry or get_command_registry()

    # Determine command name and parent from dot notation
    if name:
        parts = name.split(".")
        if len(parts) > 1:
            # Extract parent path and command name
            parent = ".".join(parts[:-1])
            command_name = parts[-1]

            # Auto-create parent groups if they don't exist (click only)
            _, has_click = _get_click()
            if has_click:
                ensure_parent_groups_fn = _get_ensure_parent_groups()
                if ensure_parent_groups_fn:
                    ensure_parent_groups_fn(parent, reg)
        else:
            parent = None
            command_name = name
    else:
        # Use function name as command name
        parent = None
        command_name = getattr(func, "__name__", "<anonymous>")

    # Check if it's already a Click command
    click_cmd = None
    click_module, has_click = _get_click()
    if has_click and isinstance(func, click_module.Command):
        click_cmd = func
        actual_func = func.callback
    else:
        actual_func = func

    # Create command info
    cmd_metadata = {"is_group": group}
    cmd_metadata.update(extra_metadata)

    info = CommandInfo(
        name=command_name,
        func=None,
        description=description or (actual_func.__doc__ if actual_func else None),
        aliases=aliases or [],
        hidden=hidden,
        category=category,
        metadata=cmd_metadata,
        parent=parent,
    )

    # Build full registry key
    full_name = f"{parent}.{command_name}" if parent else command_name

    # Build registry metadata
    reg_metadata = {
        "info": info,
        "description": info.description,
        "aliases": info.aliases,
        "hidden": hidden,
        "category": category,
        "parent": parent,
        "is_group": group,
        "_prebuilt_click_command": click_cmd,  # Use new, clearer name
    }
    reg_metadata.update(extra_metadata)

    # Register in the registry
    reg.register(
        name=full_name,
        value=func,
        dimension=ComponentCategory.COMMAND.value,
        metadata=reg_metadata,
        aliases=aliases,
        replace=replace,
    )

    # Add metadata to the function
    func.__registry_name__ = command_name  # type: ignore[attr-defined]
    func.__registry_dimension__ = ComponentCategory.COMMAND.value  # type: ignore[attr-defined]
    func.__registry_info__ = info  # type: ignore[attr-defined]

    get_foundation_logger().trace(f"Registered command: {full_name}")

    return func


def x__register_command_func__mutmut_52(
    func: F,
    *,
    name: str | None = None,
    description: str | None = None,
    aliases: list[str] | None = None,
    hidden: bool = False,
    category: str | None = None,
    group: bool = False,
    replace: bool = False,
    registry: Registry | None = None,
    **extra_metadata: Any,
) -> F:
    """Internal function to register a command."""
    reg = registry or get_command_registry()

    # Determine command name and parent from dot notation
    if name:
        parts = name.split(".")
        if len(parts) > 1:
            # Extract parent path and command name
            parent = ".".join(parts[:-1])
            command_name = parts[-1]

            # Auto-create parent groups if they don't exist (click only)
            _, has_click = _get_click()
            if has_click:
                ensure_parent_groups_fn = _get_ensure_parent_groups()
                if ensure_parent_groups_fn:
                    ensure_parent_groups_fn(parent, reg)
        else:
            parent = None
            command_name = name
    else:
        # Use function name as command name
        parent = None
        command_name = getattr(func, "__name__", "<anonymous>")

    # Check if it's already a Click command
    click_cmd = None
    click_module, has_click = _get_click()
    if has_click and isinstance(func, click_module.Command):
        click_cmd = func
        actual_func = func.callback
    else:
        actual_func = func

    # Create command info
    cmd_metadata = {"is_group": group}
    cmd_metadata.update(extra_metadata)

    info = CommandInfo(
        name=command_name,
        func=actual_func,
        description=None,
        aliases=aliases or [],
        hidden=hidden,
        category=category,
        metadata=cmd_metadata,
        parent=parent,
    )

    # Build full registry key
    full_name = f"{parent}.{command_name}" if parent else command_name

    # Build registry metadata
    reg_metadata = {
        "info": info,
        "description": info.description,
        "aliases": info.aliases,
        "hidden": hidden,
        "category": category,
        "parent": parent,
        "is_group": group,
        "_prebuilt_click_command": click_cmd,  # Use new, clearer name
    }
    reg_metadata.update(extra_metadata)

    # Register in the registry
    reg.register(
        name=full_name,
        value=func,
        dimension=ComponentCategory.COMMAND.value,
        metadata=reg_metadata,
        aliases=aliases,
        replace=replace,
    )

    # Add metadata to the function
    func.__registry_name__ = command_name  # type: ignore[attr-defined]
    func.__registry_dimension__ = ComponentCategory.COMMAND.value  # type: ignore[attr-defined]
    func.__registry_info__ = info  # type: ignore[attr-defined]

    get_foundation_logger().trace(f"Registered command: {full_name}")

    return func


def x__register_command_func__mutmut_53(
    func: F,
    *,
    name: str | None = None,
    description: str | None = None,
    aliases: list[str] | None = None,
    hidden: bool = False,
    category: str | None = None,
    group: bool = False,
    replace: bool = False,
    registry: Registry | None = None,
    **extra_metadata: Any,
) -> F:
    """Internal function to register a command."""
    reg = registry or get_command_registry()

    # Determine command name and parent from dot notation
    if name:
        parts = name.split(".")
        if len(parts) > 1:
            # Extract parent path and command name
            parent = ".".join(parts[:-1])
            command_name = parts[-1]

            # Auto-create parent groups if they don't exist (click only)
            _, has_click = _get_click()
            if has_click:
                ensure_parent_groups_fn = _get_ensure_parent_groups()
                if ensure_parent_groups_fn:
                    ensure_parent_groups_fn(parent, reg)
        else:
            parent = None
            command_name = name
    else:
        # Use function name as command name
        parent = None
        command_name = getattr(func, "__name__", "<anonymous>")

    # Check if it's already a Click command
    click_cmd = None
    click_module, has_click = _get_click()
    if has_click and isinstance(func, click_module.Command):
        click_cmd = func
        actual_func = func.callback
    else:
        actual_func = func

    # Create command info
    cmd_metadata = {"is_group": group}
    cmd_metadata.update(extra_metadata)

    info = CommandInfo(
        name=command_name,
        func=actual_func,
        description=description or (actual_func.__doc__ if actual_func else None),
        aliases=None,
        hidden=hidden,
        category=category,
        metadata=cmd_metadata,
        parent=parent,
    )

    # Build full registry key
    full_name = f"{parent}.{command_name}" if parent else command_name

    # Build registry metadata
    reg_metadata = {
        "info": info,
        "description": info.description,
        "aliases": info.aliases,
        "hidden": hidden,
        "category": category,
        "parent": parent,
        "is_group": group,
        "_prebuilt_click_command": click_cmd,  # Use new, clearer name
    }
    reg_metadata.update(extra_metadata)

    # Register in the registry
    reg.register(
        name=full_name,
        value=func,
        dimension=ComponentCategory.COMMAND.value,
        metadata=reg_metadata,
        aliases=aliases,
        replace=replace,
    )

    # Add metadata to the function
    func.__registry_name__ = command_name  # type: ignore[attr-defined]
    func.__registry_dimension__ = ComponentCategory.COMMAND.value  # type: ignore[attr-defined]
    func.__registry_info__ = info  # type: ignore[attr-defined]

    get_foundation_logger().trace(f"Registered command: {full_name}")

    return func


def x__register_command_func__mutmut_54(
    func: F,
    *,
    name: str | None = None,
    description: str | None = None,
    aliases: list[str] | None = None,
    hidden: bool = False,
    category: str | None = None,
    group: bool = False,
    replace: bool = False,
    registry: Registry | None = None,
    **extra_metadata: Any,
) -> F:
    """Internal function to register a command."""
    reg = registry or get_command_registry()

    # Determine command name and parent from dot notation
    if name:
        parts = name.split(".")
        if len(parts) > 1:
            # Extract parent path and command name
            parent = ".".join(parts[:-1])
            command_name = parts[-1]

            # Auto-create parent groups if they don't exist (click only)
            _, has_click = _get_click()
            if has_click:
                ensure_parent_groups_fn = _get_ensure_parent_groups()
                if ensure_parent_groups_fn:
                    ensure_parent_groups_fn(parent, reg)
        else:
            parent = None
            command_name = name
    else:
        # Use function name as command name
        parent = None
        command_name = getattr(func, "__name__", "<anonymous>")

    # Check if it's already a Click command
    click_cmd = None
    click_module, has_click = _get_click()
    if has_click and isinstance(func, click_module.Command):
        click_cmd = func
        actual_func = func.callback
    else:
        actual_func = func

    # Create command info
    cmd_metadata = {"is_group": group}
    cmd_metadata.update(extra_metadata)

    info = CommandInfo(
        name=command_name,
        func=actual_func,
        description=description or (actual_func.__doc__ if actual_func else None),
        aliases=aliases or [],
        hidden=None,
        category=category,
        metadata=cmd_metadata,
        parent=parent,
    )

    # Build full registry key
    full_name = f"{parent}.{command_name}" if parent else command_name

    # Build registry metadata
    reg_metadata = {
        "info": info,
        "description": info.description,
        "aliases": info.aliases,
        "hidden": hidden,
        "category": category,
        "parent": parent,
        "is_group": group,
        "_prebuilt_click_command": click_cmd,  # Use new, clearer name
    }
    reg_metadata.update(extra_metadata)

    # Register in the registry
    reg.register(
        name=full_name,
        value=func,
        dimension=ComponentCategory.COMMAND.value,
        metadata=reg_metadata,
        aliases=aliases,
        replace=replace,
    )

    # Add metadata to the function
    func.__registry_name__ = command_name  # type: ignore[attr-defined]
    func.__registry_dimension__ = ComponentCategory.COMMAND.value  # type: ignore[attr-defined]
    func.__registry_info__ = info  # type: ignore[attr-defined]

    get_foundation_logger().trace(f"Registered command: {full_name}")

    return func


def x__register_command_func__mutmut_55(
    func: F,
    *,
    name: str | None = None,
    description: str | None = None,
    aliases: list[str] | None = None,
    hidden: bool = False,
    category: str | None = None,
    group: bool = False,
    replace: bool = False,
    registry: Registry | None = None,
    **extra_metadata: Any,
) -> F:
    """Internal function to register a command."""
    reg = registry or get_command_registry()

    # Determine command name and parent from dot notation
    if name:
        parts = name.split(".")
        if len(parts) > 1:
            # Extract parent path and command name
            parent = ".".join(parts[:-1])
            command_name = parts[-1]

            # Auto-create parent groups if they don't exist (click only)
            _, has_click = _get_click()
            if has_click:
                ensure_parent_groups_fn = _get_ensure_parent_groups()
                if ensure_parent_groups_fn:
                    ensure_parent_groups_fn(parent, reg)
        else:
            parent = None
            command_name = name
    else:
        # Use function name as command name
        parent = None
        command_name = getattr(func, "__name__", "<anonymous>")

    # Check if it's already a Click command
    click_cmd = None
    click_module, has_click = _get_click()
    if has_click and isinstance(func, click_module.Command):
        click_cmd = func
        actual_func = func.callback
    else:
        actual_func = func

    # Create command info
    cmd_metadata = {"is_group": group}
    cmd_metadata.update(extra_metadata)

    info = CommandInfo(
        name=command_name,
        func=actual_func,
        description=description or (actual_func.__doc__ if actual_func else None),
        aliases=aliases or [],
        hidden=hidden,
        category=None,
        metadata=cmd_metadata,
        parent=parent,
    )

    # Build full registry key
    full_name = f"{parent}.{command_name}" if parent else command_name

    # Build registry metadata
    reg_metadata = {
        "info": info,
        "description": info.description,
        "aliases": info.aliases,
        "hidden": hidden,
        "category": category,
        "parent": parent,
        "is_group": group,
        "_prebuilt_click_command": click_cmd,  # Use new, clearer name
    }
    reg_metadata.update(extra_metadata)

    # Register in the registry
    reg.register(
        name=full_name,
        value=func,
        dimension=ComponentCategory.COMMAND.value,
        metadata=reg_metadata,
        aliases=aliases,
        replace=replace,
    )

    # Add metadata to the function
    func.__registry_name__ = command_name  # type: ignore[attr-defined]
    func.__registry_dimension__ = ComponentCategory.COMMAND.value  # type: ignore[attr-defined]
    func.__registry_info__ = info  # type: ignore[attr-defined]

    get_foundation_logger().trace(f"Registered command: {full_name}")

    return func


def x__register_command_func__mutmut_56(
    func: F,
    *,
    name: str | None = None,
    description: str | None = None,
    aliases: list[str] | None = None,
    hidden: bool = False,
    category: str | None = None,
    group: bool = False,
    replace: bool = False,
    registry: Registry | None = None,
    **extra_metadata: Any,
) -> F:
    """Internal function to register a command."""
    reg = registry or get_command_registry()

    # Determine command name and parent from dot notation
    if name:
        parts = name.split(".")
        if len(parts) > 1:
            # Extract parent path and command name
            parent = ".".join(parts[:-1])
            command_name = parts[-1]

            # Auto-create parent groups if they don't exist (click only)
            _, has_click = _get_click()
            if has_click:
                ensure_parent_groups_fn = _get_ensure_parent_groups()
                if ensure_parent_groups_fn:
                    ensure_parent_groups_fn(parent, reg)
        else:
            parent = None
            command_name = name
    else:
        # Use function name as command name
        parent = None
        command_name = getattr(func, "__name__", "<anonymous>")

    # Check if it's already a Click command
    click_cmd = None
    click_module, has_click = _get_click()
    if has_click and isinstance(func, click_module.Command):
        click_cmd = func
        actual_func = func.callback
    else:
        actual_func = func

    # Create command info
    cmd_metadata = {"is_group": group}
    cmd_metadata.update(extra_metadata)

    info = CommandInfo(
        name=command_name,
        func=actual_func,
        description=description or (actual_func.__doc__ if actual_func else None),
        aliases=aliases or [],
        hidden=hidden,
        category=category,
        metadata=None,
        parent=parent,
    )

    # Build full registry key
    full_name = f"{parent}.{command_name}" if parent else command_name

    # Build registry metadata
    reg_metadata = {
        "info": info,
        "description": info.description,
        "aliases": info.aliases,
        "hidden": hidden,
        "category": category,
        "parent": parent,
        "is_group": group,
        "_prebuilt_click_command": click_cmd,  # Use new, clearer name
    }
    reg_metadata.update(extra_metadata)

    # Register in the registry
    reg.register(
        name=full_name,
        value=func,
        dimension=ComponentCategory.COMMAND.value,
        metadata=reg_metadata,
        aliases=aliases,
        replace=replace,
    )

    # Add metadata to the function
    func.__registry_name__ = command_name  # type: ignore[attr-defined]
    func.__registry_dimension__ = ComponentCategory.COMMAND.value  # type: ignore[attr-defined]
    func.__registry_info__ = info  # type: ignore[attr-defined]

    get_foundation_logger().trace(f"Registered command: {full_name}")

    return func


def x__register_command_func__mutmut_57(
    func: F,
    *,
    name: str | None = None,
    description: str | None = None,
    aliases: list[str] | None = None,
    hidden: bool = False,
    category: str | None = None,
    group: bool = False,
    replace: bool = False,
    registry: Registry | None = None,
    **extra_metadata: Any,
) -> F:
    """Internal function to register a command."""
    reg = registry or get_command_registry()

    # Determine command name and parent from dot notation
    if name:
        parts = name.split(".")
        if len(parts) > 1:
            # Extract parent path and command name
            parent = ".".join(parts[:-1])
            command_name = parts[-1]

            # Auto-create parent groups if they don't exist (click only)
            _, has_click = _get_click()
            if has_click:
                ensure_parent_groups_fn = _get_ensure_parent_groups()
                if ensure_parent_groups_fn:
                    ensure_parent_groups_fn(parent, reg)
        else:
            parent = None
            command_name = name
    else:
        # Use function name as command name
        parent = None
        command_name = getattr(func, "__name__", "<anonymous>")

    # Check if it's already a Click command
    click_cmd = None
    click_module, has_click = _get_click()
    if has_click and isinstance(func, click_module.Command):
        click_cmd = func
        actual_func = func.callback
    else:
        actual_func = func

    # Create command info
    cmd_metadata = {"is_group": group}
    cmd_metadata.update(extra_metadata)

    info = CommandInfo(
        name=command_name,
        func=actual_func,
        description=description or (actual_func.__doc__ if actual_func else None),
        aliases=aliases or [],
        hidden=hidden,
        category=category,
        metadata=cmd_metadata,
        parent=None,
    )

    # Build full registry key
    full_name = f"{parent}.{command_name}" if parent else command_name

    # Build registry metadata
    reg_metadata = {
        "info": info,
        "description": info.description,
        "aliases": info.aliases,
        "hidden": hidden,
        "category": category,
        "parent": parent,
        "is_group": group,
        "_prebuilt_click_command": click_cmd,  # Use new, clearer name
    }
    reg_metadata.update(extra_metadata)

    # Register in the registry
    reg.register(
        name=full_name,
        value=func,
        dimension=ComponentCategory.COMMAND.value,
        metadata=reg_metadata,
        aliases=aliases,
        replace=replace,
    )

    # Add metadata to the function
    func.__registry_name__ = command_name  # type: ignore[attr-defined]
    func.__registry_dimension__ = ComponentCategory.COMMAND.value  # type: ignore[attr-defined]
    func.__registry_info__ = info  # type: ignore[attr-defined]

    get_foundation_logger().trace(f"Registered command: {full_name}")

    return func


def x__register_command_func__mutmut_58(
    func: F,
    *,
    name: str | None = None,
    description: str | None = None,
    aliases: list[str] | None = None,
    hidden: bool = False,
    category: str | None = None,
    group: bool = False,
    replace: bool = False,
    registry: Registry | None = None,
    **extra_metadata: Any,
) -> F:
    """Internal function to register a command."""
    reg = registry or get_command_registry()

    # Determine command name and parent from dot notation
    if name:
        parts = name.split(".")
        if len(parts) > 1:
            # Extract parent path and command name
            parent = ".".join(parts[:-1])
            command_name = parts[-1]

            # Auto-create parent groups if they don't exist (click only)
            _, has_click = _get_click()
            if has_click:
                ensure_parent_groups_fn = _get_ensure_parent_groups()
                if ensure_parent_groups_fn:
                    ensure_parent_groups_fn(parent, reg)
        else:
            parent = None
            command_name = name
    else:
        # Use function name as command name
        parent = None
        command_name = getattr(func, "__name__", "<anonymous>")

    # Check if it's already a Click command
    click_cmd = None
    click_module, has_click = _get_click()
    if has_click and isinstance(func, click_module.Command):
        click_cmd = func
        actual_func = func.callback
    else:
        actual_func = func

    # Create command info
    cmd_metadata = {"is_group": group}
    cmd_metadata.update(extra_metadata)

    info = CommandInfo(
        func=actual_func,
        description=description or (actual_func.__doc__ if actual_func else None),
        aliases=aliases or [],
        hidden=hidden,
        category=category,
        metadata=cmd_metadata,
        parent=parent,
    )

    # Build full registry key
    full_name = f"{parent}.{command_name}" if parent else command_name

    # Build registry metadata
    reg_metadata = {
        "info": info,
        "description": info.description,
        "aliases": info.aliases,
        "hidden": hidden,
        "category": category,
        "parent": parent,
        "is_group": group,
        "_prebuilt_click_command": click_cmd,  # Use new, clearer name
    }
    reg_metadata.update(extra_metadata)

    # Register in the registry
    reg.register(
        name=full_name,
        value=func,
        dimension=ComponentCategory.COMMAND.value,
        metadata=reg_metadata,
        aliases=aliases,
        replace=replace,
    )

    # Add metadata to the function
    func.__registry_name__ = command_name  # type: ignore[attr-defined]
    func.__registry_dimension__ = ComponentCategory.COMMAND.value  # type: ignore[attr-defined]
    func.__registry_info__ = info  # type: ignore[attr-defined]

    get_foundation_logger().trace(f"Registered command: {full_name}")

    return func


def x__register_command_func__mutmut_59(
    func: F,
    *,
    name: str | None = None,
    description: str | None = None,
    aliases: list[str] | None = None,
    hidden: bool = False,
    category: str | None = None,
    group: bool = False,
    replace: bool = False,
    registry: Registry | None = None,
    **extra_metadata: Any,
) -> F:
    """Internal function to register a command."""
    reg = registry or get_command_registry()

    # Determine command name and parent from dot notation
    if name:
        parts = name.split(".")
        if len(parts) > 1:
            # Extract parent path and command name
            parent = ".".join(parts[:-1])
            command_name = parts[-1]

            # Auto-create parent groups if they don't exist (click only)
            _, has_click = _get_click()
            if has_click:
                ensure_parent_groups_fn = _get_ensure_parent_groups()
                if ensure_parent_groups_fn:
                    ensure_parent_groups_fn(parent, reg)
        else:
            parent = None
            command_name = name
    else:
        # Use function name as command name
        parent = None
        command_name = getattr(func, "__name__", "<anonymous>")

    # Check if it's already a Click command
    click_cmd = None
    click_module, has_click = _get_click()
    if has_click and isinstance(func, click_module.Command):
        click_cmd = func
        actual_func = func.callback
    else:
        actual_func = func

    # Create command info
    cmd_metadata = {"is_group": group}
    cmd_metadata.update(extra_metadata)

    info = CommandInfo(
        name=command_name,
        description=description or (actual_func.__doc__ if actual_func else None),
        aliases=aliases or [],
        hidden=hidden,
        category=category,
        metadata=cmd_metadata,
        parent=parent,
    )

    # Build full registry key
    full_name = f"{parent}.{command_name}" if parent else command_name

    # Build registry metadata
    reg_metadata = {
        "info": info,
        "description": info.description,
        "aliases": info.aliases,
        "hidden": hidden,
        "category": category,
        "parent": parent,
        "is_group": group,
        "_prebuilt_click_command": click_cmd,  # Use new, clearer name
    }
    reg_metadata.update(extra_metadata)

    # Register in the registry
    reg.register(
        name=full_name,
        value=func,
        dimension=ComponentCategory.COMMAND.value,
        metadata=reg_metadata,
        aliases=aliases,
        replace=replace,
    )

    # Add metadata to the function
    func.__registry_name__ = command_name  # type: ignore[attr-defined]
    func.__registry_dimension__ = ComponentCategory.COMMAND.value  # type: ignore[attr-defined]
    func.__registry_info__ = info  # type: ignore[attr-defined]

    get_foundation_logger().trace(f"Registered command: {full_name}")

    return func


def x__register_command_func__mutmut_60(
    func: F,
    *,
    name: str | None = None,
    description: str | None = None,
    aliases: list[str] | None = None,
    hidden: bool = False,
    category: str | None = None,
    group: bool = False,
    replace: bool = False,
    registry: Registry | None = None,
    **extra_metadata: Any,
) -> F:
    """Internal function to register a command."""
    reg = registry or get_command_registry()

    # Determine command name and parent from dot notation
    if name:
        parts = name.split(".")
        if len(parts) > 1:
            # Extract parent path and command name
            parent = ".".join(parts[:-1])
            command_name = parts[-1]

            # Auto-create parent groups if they don't exist (click only)
            _, has_click = _get_click()
            if has_click:
                ensure_parent_groups_fn = _get_ensure_parent_groups()
                if ensure_parent_groups_fn:
                    ensure_parent_groups_fn(parent, reg)
        else:
            parent = None
            command_name = name
    else:
        # Use function name as command name
        parent = None
        command_name = getattr(func, "__name__", "<anonymous>")

    # Check if it's already a Click command
    click_cmd = None
    click_module, has_click = _get_click()
    if has_click and isinstance(func, click_module.Command):
        click_cmd = func
        actual_func = func.callback
    else:
        actual_func = func

    # Create command info
    cmd_metadata = {"is_group": group}
    cmd_metadata.update(extra_metadata)

    info = CommandInfo(
        name=command_name,
        func=actual_func,
        aliases=aliases or [],
        hidden=hidden,
        category=category,
        metadata=cmd_metadata,
        parent=parent,
    )

    # Build full registry key
    full_name = f"{parent}.{command_name}" if parent else command_name

    # Build registry metadata
    reg_metadata = {
        "info": info,
        "description": info.description,
        "aliases": info.aliases,
        "hidden": hidden,
        "category": category,
        "parent": parent,
        "is_group": group,
        "_prebuilt_click_command": click_cmd,  # Use new, clearer name
    }
    reg_metadata.update(extra_metadata)

    # Register in the registry
    reg.register(
        name=full_name,
        value=func,
        dimension=ComponentCategory.COMMAND.value,
        metadata=reg_metadata,
        aliases=aliases,
        replace=replace,
    )

    # Add metadata to the function
    func.__registry_name__ = command_name  # type: ignore[attr-defined]
    func.__registry_dimension__ = ComponentCategory.COMMAND.value  # type: ignore[attr-defined]
    func.__registry_info__ = info  # type: ignore[attr-defined]

    get_foundation_logger().trace(f"Registered command: {full_name}")

    return func


def x__register_command_func__mutmut_61(
    func: F,
    *,
    name: str | None = None,
    description: str | None = None,
    aliases: list[str] | None = None,
    hidden: bool = False,
    category: str | None = None,
    group: bool = False,
    replace: bool = False,
    registry: Registry | None = None,
    **extra_metadata: Any,
) -> F:
    """Internal function to register a command."""
    reg = registry or get_command_registry()

    # Determine command name and parent from dot notation
    if name:
        parts = name.split(".")
        if len(parts) > 1:
            # Extract parent path and command name
            parent = ".".join(parts[:-1])
            command_name = parts[-1]

            # Auto-create parent groups if they don't exist (click only)
            _, has_click = _get_click()
            if has_click:
                ensure_parent_groups_fn = _get_ensure_parent_groups()
                if ensure_parent_groups_fn:
                    ensure_parent_groups_fn(parent, reg)
        else:
            parent = None
            command_name = name
    else:
        # Use function name as command name
        parent = None
        command_name = getattr(func, "__name__", "<anonymous>")

    # Check if it's already a Click command
    click_cmd = None
    click_module, has_click = _get_click()
    if has_click and isinstance(func, click_module.Command):
        click_cmd = func
        actual_func = func.callback
    else:
        actual_func = func

    # Create command info
    cmd_metadata = {"is_group": group}
    cmd_metadata.update(extra_metadata)

    info = CommandInfo(
        name=command_name,
        func=actual_func,
        description=description or (actual_func.__doc__ if actual_func else None),
        hidden=hidden,
        category=category,
        metadata=cmd_metadata,
        parent=parent,
    )

    # Build full registry key
    full_name = f"{parent}.{command_name}" if parent else command_name

    # Build registry metadata
    reg_metadata = {
        "info": info,
        "description": info.description,
        "aliases": info.aliases,
        "hidden": hidden,
        "category": category,
        "parent": parent,
        "is_group": group,
        "_prebuilt_click_command": click_cmd,  # Use new, clearer name
    }
    reg_metadata.update(extra_metadata)

    # Register in the registry
    reg.register(
        name=full_name,
        value=func,
        dimension=ComponentCategory.COMMAND.value,
        metadata=reg_metadata,
        aliases=aliases,
        replace=replace,
    )

    # Add metadata to the function
    func.__registry_name__ = command_name  # type: ignore[attr-defined]
    func.__registry_dimension__ = ComponentCategory.COMMAND.value  # type: ignore[attr-defined]
    func.__registry_info__ = info  # type: ignore[attr-defined]

    get_foundation_logger().trace(f"Registered command: {full_name}")

    return func


def x__register_command_func__mutmut_62(
    func: F,
    *,
    name: str | None = None,
    description: str | None = None,
    aliases: list[str] | None = None,
    hidden: bool = False,
    category: str | None = None,
    group: bool = False,
    replace: bool = False,
    registry: Registry | None = None,
    **extra_metadata: Any,
) -> F:
    """Internal function to register a command."""
    reg = registry or get_command_registry()

    # Determine command name and parent from dot notation
    if name:
        parts = name.split(".")
        if len(parts) > 1:
            # Extract parent path and command name
            parent = ".".join(parts[:-1])
            command_name = parts[-1]

            # Auto-create parent groups if they don't exist (click only)
            _, has_click = _get_click()
            if has_click:
                ensure_parent_groups_fn = _get_ensure_parent_groups()
                if ensure_parent_groups_fn:
                    ensure_parent_groups_fn(parent, reg)
        else:
            parent = None
            command_name = name
    else:
        # Use function name as command name
        parent = None
        command_name = getattr(func, "__name__", "<anonymous>")

    # Check if it's already a Click command
    click_cmd = None
    click_module, has_click = _get_click()
    if has_click and isinstance(func, click_module.Command):
        click_cmd = func
        actual_func = func.callback
    else:
        actual_func = func

    # Create command info
    cmd_metadata = {"is_group": group}
    cmd_metadata.update(extra_metadata)

    info = CommandInfo(
        name=command_name,
        func=actual_func,
        description=description or (actual_func.__doc__ if actual_func else None),
        aliases=aliases or [],
        category=category,
        metadata=cmd_metadata,
        parent=parent,
    )

    # Build full registry key
    full_name = f"{parent}.{command_name}" if parent else command_name

    # Build registry metadata
    reg_metadata = {
        "info": info,
        "description": info.description,
        "aliases": info.aliases,
        "hidden": hidden,
        "category": category,
        "parent": parent,
        "is_group": group,
        "_prebuilt_click_command": click_cmd,  # Use new, clearer name
    }
    reg_metadata.update(extra_metadata)

    # Register in the registry
    reg.register(
        name=full_name,
        value=func,
        dimension=ComponentCategory.COMMAND.value,
        metadata=reg_metadata,
        aliases=aliases,
        replace=replace,
    )

    # Add metadata to the function
    func.__registry_name__ = command_name  # type: ignore[attr-defined]
    func.__registry_dimension__ = ComponentCategory.COMMAND.value  # type: ignore[attr-defined]
    func.__registry_info__ = info  # type: ignore[attr-defined]

    get_foundation_logger().trace(f"Registered command: {full_name}")

    return func


def x__register_command_func__mutmut_63(
    func: F,
    *,
    name: str | None = None,
    description: str | None = None,
    aliases: list[str] | None = None,
    hidden: bool = False,
    category: str | None = None,
    group: bool = False,
    replace: bool = False,
    registry: Registry | None = None,
    **extra_metadata: Any,
) -> F:
    """Internal function to register a command."""
    reg = registry or get_command_registry()

    # Determine command name and parent from dot notation
    if name:
        parts = name.split(".")
        if len(parts) > 1:
            # Extract parent path and command name
            parent = ".".join(parts[:-1])
            command_name = parts[-1]

            # Auto-create parent groups if they don't exist (click only)
            _, has_click = _get_click()
            if has_click:
                ensure_parent_groups_fn = _get_ensure_parent_groups()
                if ensure_parent_groups_fn:
                    ensure_parent_groups_fn(parent, reg)
        else:
            parent = None
            command_name = name
    else:
        # Use function name as command name
        parent = None
        command_name = getattr(func, "__name__", "<anonymous>")

    # Check if it's already a Click command
    click_cmd = None
    click_module, has_click = _get_click()
    if has_click and isinstance(func, click_module.Command):
        click_cmd = func
        actual_func = func.callback
    else:
        actual_func = func

    # Create command info
    cmd_metadata = {"is_group": group}
    cmd_metadata.update(extra_metadata)

    info = CommandInfo(
        name=command_name,
        func=actual_func,
        description=description or (actual_func.__doc__ if actual_func else None),
        aliases=aliases or [],
        hidden=hidden,
        metadata=cmd_metadata,
        parent=parent,
    )

    # Build full registry key
    full_name = f"{parent}.{command_name}" if parent else command_name

    # Build registry metadata
    reg_metadata = {
        "info": info,
        "description": info.description,
        "aliases": info.aliases,
        "hidden": hidden,
        "category": category,
        "parent": parent,
        "is_group": group,
        "_prebuilt_click_command": click_cmd,  # Use new, clearer name
    }
    reg_metadata.update(extra_metadata)

    # Register in the registry
    reg.register(
        name=full_name,
        value=func,
        dimension=ComponentCategory.COMMAND.value,
        metadata=reg_metadata,
        aliases=aliases,
        replace=replace,
    )

    # Add metadata to the function
    func.__registry_name__ = command_name  # type: ignore[attr-defined]
    func.__registry_dimension__ = ComponentCategory.COMMAND.value  # type: ignore[attr-defined]
    func.__registry_info__ = info  # type: ignore[attr-defined]

    get_foundation_logger().trace(f"Registered command: {full_name}")

    return func


def x__register_command_func__mutmut_64(
    func: F,
    *,
    name: str | None = None,
    description: str | None = None,
    aliases: list[str] | None = None,
    hidden: bool = False,
    category: str | None = None,
    group: bool = False,
    replace: bool = False,
    registry: Registry | None = None,
    **extra_metadata: Any,
) -> F:
    """Internal function to register a command."""
    reg = registry or get_command_registry()

    # Determine command name and parent from dot notation
    if name:
        parts = name.split(".")
        if len(parts) > 1:
            # Extract parent path and command name
            parent = ".".join(parts[:-1])
            command_name = parts[-1]

            # Auto-create parent groups if they don't exist (click only)
            _, has_click = _get_click()
            if has_click:
                ensure_parent_groups_fn = _get_ensure_parent_groups()
                if ensure_parent_groups_fn:
                    ensure_parent_groups_fn(parent, reg)
        else:
            parent = None
            command_name = name
    else:
        # Use function name as command name
        parent = None
        command_name = getattr(func, "__name__", "<anonymous>")

    # Check if it's already a Click command
    click_cmd = None
    click_module, has_click = _get_click()
    if has_click and isinstance(func, click_module.Command):
        click_cmd = func
        actual_func = func.callback
    else:
        actual_func = func

    # Create command info
    cmd_metadata = {"is_group": group}
    cmd_metadata.update(extra_metadata)

    info = CommandInfo(
        name=command_name,
        func=actual_func,
        description=description or (actual_func.__doc__ if actual_func else None),
        aliases=aliases or [],
        hidden=hidden,
        category=category,
        parent=parent,
    )

    # Build full registry key
    full_name = f"{parent}.{command_name}" if parent else command_name

    # Build registry metadata
    reg_metadata = {
        "info": info,
        "description": info.description,
        "aliases": info.aliases,
        "hidden": hidden,
        "category": category,
        "parent": parent,
        "is_group": group,
        "_prebuilt_click_command": click_cmd,  # Use new, clearer name
    }
    reg_metadata.update(extra_metadata)

    # Register in the registry
    reg.register(
        name=full_name,
        value=func,
        dimension=ComponentCategory.COMMAND.value,
        metadata=reg_metadata,
        aliases=aliases,
        replace=replace,
    )

    # Add metadata to the function
    func.__registry_name__ = command_name  # type: ignore[attr-defined]
    func.__registry_dimension__ = ComponentCategory.COMMAND.value  # type: ignore[attr-defined]
    func.__registry_info__ = info  # type: ignore[attr-defined]

    get_foundation_logger().trace(f"Registered command: {full_name}")

    return func


def x__register_command_func__mutmut_65(
    func: F,
    *,
    name: str | None = None,
    description: str | None = None,
    aliases: list[str] | None = None,
    hidden: bool = False,
    category: str | None = None,
    group: bool = False,
    replace: bool = False,
    registry: Registry | None = None,
    **extra_metadata: Any,
) -> F:
    """Internal function to register a command."""
    reg = registry or get_command_registry()

    # Determine command name and parent from dot notation
    if name:
        parts = name.split(".")
        if len(parts) > 1:
            # Extract parent path and command name
            parent = ".".join(parts[:-1])
            command_name = parts[-1]

            # Auto-create parent groups if they don't exist (click only)
            _, has_click = _get_click()
            if has_click:
                ensure_parent_groups_fn = _get_ensure_parent_groups()
                if ensure_parent_groups_fn:
                    ensure_parent_groups_fn(parent, reg)
        else:
            parent = None
            command_name = name
    else:
        # Use function name as command name
        parent = None
        command_name = getattr(func, "__name__", "<anonymous>")

    # Check if it's already a Click command
    click_cmd = None
    click_module, has_click = _get_click()
    if has_click and isinstance(func, click_module.Command):
        click_cmd = func
        actual_func = func.callback
    else:
        actual_func = func

    # Create command info
    cmd_metadata = {"is_group": group}
    cmd_metadata.update(extra_metadata)

    info = CommandInfo(
        name=command_name,
        func=actual_func,
        description=description or (actual_func.__doc__ if actual_func else None),
        aliases=aliases or [],
        hidden=hidden,
        category=category,
        metadata=cmd_metadata,
    )

    # Build full registry key
    full_name = f"{parent}.{command_name}" if parent else command_name

    # Build registry metadata
    reg_metadata = {
        "info": info,
        "description": info.description,
        "aliases": info.aliases,
        "hidden": hidden,
        "category": category,
        "parent": parent,
        "is_group": group,
        "_prebuilt_click_command": click_cmd,  # Use new, clearer name
    }
    reg_metadata.update(extra_metadata)

    # Register in the registry
    reg.register(
        name=full_name,
        value=func,
        dimension=ComponentCategory.COMMAND.value,
        metadata=reg_metadata,
        aliases=aliases,
        replace=replace,
    )

    # Add metadata to the function
    func.__registry_name__ = command_name  # type: ignore[attr-defined]
    func.__registry_dimension__ = ComponentCategory.COMMAND.value  # type: ignore[attr-defined]
    func.__registry_info__ = info  # type: ignore[attr-defined]

    get_foundation_logger().trace(f"Registered command: {full_name}")

    return func


def x__register_command_func__mutmut_66(
    func: F,
    *,
    name: str | None = None,
    description: str | None = None,
    aliases: list[str] | None = None,
    hidden: bool = False,
    category: str | None = None,
    group: bool = False,
    replace: bool = False,
    registry: Registry | None = None,
    **extra_metadata: Any,
) -> F:
    """Internal function to register a command."""
    reg = registry or get_command_registry()

    # Determine command name and parent from dot notation
    if name:
        parts = name.split(".")
        if len(parts) > 1:
            # Extract parent path and command name
            parent = ".".join(parts[:-1])
            command_name = parts[-1]

            # Auto-create parent groups if they don't exist (click only)
            _, has_click = _get_click()
            if has_click:
                ensure_parent_groups_fn = _get_ensure_parent_groups()
                if ensure_parent_groups_fn:
                    ensure_parent_groups_fn(parent, reg)
        else:
            parent = None
            command_name = name
    else:
        # Use function name as command name
        parent = None
        command_name = getattr(func, "__name__", "<anonymous>")

    # Check if it's already a Click command
    click_cmd = None
    click_module, has_click = _get_click()
    if has_click and isinstance(func, click_module.Command):
        click_cmd = func
        actual_func = func.callback
    else:
        actual_func = func

    # Create command info
    cmd_metadata = {"is_group": group}
    cmd_metadata.update(extra_metadata)

    info = CommandInfo(
        name=command_name,
        func=actual_func,
        description=description and (actual_func.__doc__ if actual_func else None),
        aliases=aliases or [],
        hidden=hidden,
        category=category,
        metadata=cmd_metadata,
        parent=parent,
    )

    # Build full registry key
    full_name = f"{parent}.{command_name}" if parent else command_name

    # Build registry metadata
    reg_metadata = {
        "info": info,
        "description": info.description,
        "aliases": info.aliases,
        "hidden": hidden,
        "category": category,
        "parent": parent,
        "is_group": group,
        "_prebuilt_click_command": click_cmd,  # Use new, clearer name
    }
    reg_metadata.update(extra_metadata)

    # Register in the registry
    reg.register(
        name=full_name,
        value=func,
        dimension=ComponentCategory.COMMAND.value,
        metadata=reg_metadata,
        aliases=aliases,
        replace=replace,
    )

    # Add metadata to the function
    func.__registry_name__ = command_name  # type: ignore[attr-defined]
    func.__registry_dimension__ = ComponentCategory.COMMAND.value  # type: ignore[attr-defined]
    func.__registry_info__ = info  # type: ignore[attr-defined]

    get_foundation_logger().trace(f"Registered command: {full_name}")

    return func


def x__register_command_func__mutmut_67(
    func: F,
    *,
    name: str | None = None,
    description: str | None = None,
    aliases: list[str] | None = None,
    hidden: bool = False,
    category: str | None = None,
    group: bool = False,
    replace: bool = False,
    registry: Registry | None = None,
    **extra_metadata: Any,
) -> F:
    """Internal function to register a command."""
    reg = registry or get_command_registry()

    # Determine command name and parent from dot notation
    if name:
        parts = name.split(".")
        if len(parts) > 1:
            # Extract parent path and command name
            parent = ".".join(parts[:-1])
            command_name = parts[-1]

            # Auto-create parent groups if they don't exist (click only)
            _, has_click = _get_click()
            if has_click:
                ensure_parent_groups_fn = _get_ensure_parent_groups()
                if ensure_parent_groups_fn:
                    ensure_parent_groups_fn(parent, reg)
        else:
            parent = None
            command_name = name
    else:
        # Use function name as command name
        parent = None
        command_name = getattr(func, "__name__", "<anonymous>")

    # Check if it's already a Click command
    click_cmd = None
    click_module, has_click = _get_click()
    if has_click and isinstance(func, click_module.Command):
        click_cmd = func
        actual_func = func.callback
    else:
        actual_func = func

    # Create command info
    cmd_metadata = {"is_group": group}
    cmd_metadata.update(extra_metadata)

    info = CommandInfo(
        name=command_name,
        func=actual_func,
        description=description or (actual_func.__doc__ if actual_func else None),
        aliases=aliases and [],
        hidden=hidden,
        category=category,
        metadata=cmd_metadata,
        parent=parent,
    )

    # Build full registry key
    full_name = f"{parent}.{command_name}" if parent else command_name

    # Build registry metadata
    reg_metadata = {
        "info": info,
        "description": info.description,
        "aliases": info.aliases,
        "hidden": hidden,
        "category": category,
        "parent": parent,
        "is_group": group,
        "_prebuilt_click_command": click_cmd,  # Use new, clearer name
    }
    reg_metadata.update(extra_metadata)

    # Register in the registry
    reg.register(
        name=full_name,
        value=func,
        dimension=ComponentCategory.COMMAND.value,
        metadata=reg_metadata,
        aliases=aliases,
        replace=replace,
    )

    # Add metadata to the function
    func.__registry_name__ = command_name  # type: ignore[attr-defined]
    func.__registry_dimension__ = ComponentCategory.COMMAND.value  # type: ignore[attr-defined]
    func.__registry_info__ = info  # type: ignore[attr-defined]

    get_foundation_logger().trace(f"Registered command: {full_name}")

    return func


def x__register_command_func__mutmut_68(
    func: F,
    *,
    name: str | None = None,
    description: str | None = None,
    aliases: list[str] | None = None,
    hidden: bool = False,
    category: str | None = None,
    group: bool = False,
    replace: bool = False,
    registry: Registry | None = None,
    **extra_metadata: Any,
) -> F:
    """Internal function to register a command."""
    reg = registry or get_command_registry()

    # Determine command name and parent from dot notation
    if name:
        parts = name.split(".")
        if len(parts) > 1:
            # Extract parent path and command name
            parent = ".".join(parts[:-1])
            command_name = parts[-1]

            # Auto-create parent groups if they don't exist (click only)
            _, has_click = _get_click()
            if has_click:
                ensure_parent_groups_fn = _get_ensure_parent_groups()
                if ensure_parent_groups_fn:
                    ensure_parent_groups_fn(parent, reg)
        else:
            parent = None
            command_name = name
    else:
        # Use function name as command name
        parent = None
        command_name = getattr(func, "__name__", "<anonymous>")

    # Check if it's already a Click command
    click_cmd = None
    click_module, has_click = _get_click()
    if has_click and isinstance(func, click_module.Command):
        click_cmd = func
        actual_func = func.callback
    else:
        actual_func = func

    # Create command info
    cmd_metadata = {"is_group": group}
    cmd_metadata.update(extra_metadata)

    info = CommandInfo(
        name=command_name,
        func=actual_func,
        description=description or (actual_func.__doc__ if actual_func else None),
        aliases=aliases or [],
        hidden=hidden,
        category=category,
        metadata=cmd_metadata,
        parent=parent,
    )

    # Build full registry key
    full_name = None

    # Build registry metadata
    reg_metadata = {
        "info": info,
        "description": info.description,
        "aliases": info.aliases,
        "hidden": hidden,
        "category": category,
        "parent": parent,
        "is_group": group,
        "_prebuilt_click_command": click_cmd,  # Use new, clearer name
    }
    reg_metadata.update(extra_metadata)

    # Register in the registry
    reg.register(
        name=full_name,
        value=func,
        dimension=ComponentCategory.COMMAND.value,
        metadata=reg_metadata,
        aliases=aliases,
        replace=replace,
    )

    # Add metadata to the function
    func.__registry_name__ = command_name  # type: ignore[attr-defined]
    func.__registry_dimension__ = ComponentCategory.COMMAND.value  # type: ignore[attr-defined]
    func.__registry_info__ = info  # type: ignore[attr-defined]

    get_foundation_logger().trace(f"Registered command: {full_name}")

    return func


def x__register_command_func__mutmut_69(
    func: F,
    *,
    name: str | None = None,
    description: str | None = None,
    aliases: list[str] | None = None,
    hidden: bool = False,
    category: str | None = None,
    group: bool = False,
    replace: bool = False,
    registry: Registry | None = None,
    **extra_metadata: Any,
) -> F:
    """Internal function to register a command."""
    reg = registry or get_command_registry()

    # Determine command name and parent from dot notation
    if name:
        parts = name.split(".")
        if len(parts) > 1:
            # Extract parent path and command name
            parent = ".".join(parts[:-1])
            command_name = parts[-1]

            # Auto-create parent groups if they don't exist (click only)
            _, has_click = _get_click()
            if has_click:
                ensure_parent_groups_fn = _get_ensure_parent_groups()
                if ensure_parent_groups_fn:
                    ensure_parent_groups_fn(parent, reg)
        else:
            parent = None
            command_name = name
    else:
        # Use function name as command name
        parent = None
        command_name = getattr(func, "__name__", "<anonymous>")

    # Check if it's already a Click command
    click_cmd = None
    click_module, has_click = _get_click()
    if has_click and isinstance(func, click_module.Command):
        click_cmd = func
        actual_func = func.callback
    else:
        actual_func = func

    # Create command info
    cmd_metadata = {"is_group": group}
    cmd_metadata.update(extra_metadata)

    info = CommandInfo(
        name=command_name,
        func=actual_func,
        description=description or (actual_func.__doc__ if actual_func else None),
        aliases=aliases or [],
        hidden=hidden,
        category=category,
        metadata=cmd_metadata,
        parent=parent,
    )

    # Build full registry key
    full_name = f"{parent}.{command_name}" if parent else command_name

    # Build registry metadata
    reg_metadata = None
    reg_metadata.update(extra_metadata)

    # Register in the registry
    reg.register(
        name=full_name,
        value=func,
        dimension=ComponentCategory.COMMAND.value,
        metadata=reg_metadata,
        aliases=aliases,
        replace=replace,
    )

    # Add metadata to the function
    func.__registry_name__ = command_name  # type: ignore[attr-defined]
    func.__registry_dimension__ = ComponentCategory.COMMAND.value  # type: ignore[attr-defined]
    func.__registry_info__ = info  # type: ignore[attr-defined]

    get_foundation_logger().trace(f"Registered command: {full_name}")

    return func


def x__register_command_func__mutmut_70(
    func: F,
    *,
    name: str | None = None,
    description: str | None = None,
    aliases: list[str] | None = None,
    hidden: bool = False,
    category: str | None = None,
    group: bool = False,
    replace: bool = False,
    registry: Registry | None = None,
    **extra_metadata: Any,
) -> F:
    """Internal function to register a command."""
    reg = registry or get_command_registry()

    # Determine command name and parent from dot notation
    if name:
        parts = name.split(".")
        if len(parts) > 1:
            # Extract parent path and command name
            parent = ".".join(parts[:-1])
            command_name = parts[-1]

            # Auto-create parent groups if they don't exist (click only)
            _, has_click = _get_click()
            if has_click:
                ensure_parent_groups_fn = _get_ensure_parent_groups()
                if ensure_parent_groups_fn:
                    ensure_parent_groups_fn(parent, reg)
        else:
            parent = None
            command_name = name
    else:
        # Use function name as command name
        parent = None
        command_name = getattr(func, "__name__", "<anonymous>")

    # Check if it's already a Click command
    click_cmd = None
    click_module, has_click = _get_click()
    if has_click and isinstance(func, click_module.Command):
        click_cmd = func
        actual_func = func.callback
    else:
        actual_func = func

    # Create command info
    cmd_metadata = {"is_group": group}
    cmd_metadata.update(extra_metadata)

    info = CommandInfo(
        name=command_name,
        func=actual_func,
        description=description or (actual_func.__doc__ if actual_func else None),
        aliases=aliases or [],
        hidden=hidden,
        category=category,
        metadata=cmd_metadata,
        parent=parent,
    )

    # Build full registry key
    full_name = f"{parent}.{command_name}" if parent else command_name

    # Build registry metadata
    reg_metadata = {
        "XXinfoXX": info,
        "description": info.description,
        "aliases": info.aliases,
        "hidden": hidden,
        "category": category,
        "parent": parent,
        "is_group": group,
        "_prebuilt_click_command": click_cmd,  # Use new, clearer name
    }
    reg_metadata.update(extra_metadata)

    # Register in the registry
    reg.register(
        name=full_name,
        value=func,
        dimension=ComponentCategory.COMMAND.value,
        metadata=reg_metadata,
        aliases=aliases,
        replace=replace,
    )

    # Add metadata to the function
    func.__registry_name__ = command_name  # type: ignore[attr-defined]
    func.__registry_dimension__ = ComponentCategory.COMMAND.value  # type: ignore[attr-defined]
    func.__registry_info__ = info  # type: ignore[attr-defined]

    get_foundation_logger().trace(f"Registered command: {full_name}")

    return func


def x__register_command_func__mutmut_71(
    func: F,
    *,
    name: str | None = None,
    description: str | None = None,
    aliases: list[str] | None = None,
    hidden: bool = False,
    category: str | None = None,
    group: bool = False,
    replace: bool = False,
    registry: Registry | None = None,
    **extra_metadata: Any,
) -> F:
    """Internal function to register a command."""
    reg = registry or get_command_registry()

    # Determine command name and parent from dot notation
    if name:
        parts = name.split(".")
        if len(parts) > 1:
            # Extract parent path and command name
            parent = ".".join(parts[:-1])
            command_name = parts[-1]

            # Auto-create parent groups if they don't exist (click only)
            _, has_click = _get_click()
            if has_click:
                ensure_parent_groups_fn = _get_ensure_parent_groups()
                if ensure_parent_groups_fn:
                    ensure_parent_groups_fn(parent, reg)
        else:
            parent = None
            command_name = name
    else:
        # Use function name as command name
        parent = None
        command_name = getattr(func, "__name__", "<anonymous>")

    # Check if it's already a Click command
    click_cmd = None
    click_module, has_click = _get_click()
    if has_click and isinstance(func, click_module.Command):
        click_cmd = func
        actual_func = func.callback
    else:
        actual_func = func

    # Create command info
    cmd_metadata = {"is_group": group}
    cmd_metadata.update(extra_metadata)

    info = CommandInfo(
        name=command_name,
        func=actual_func,
        description=description or (actual_func.__doc__ if actual_func else None),
        aliases=aliases or [],
        hidden=hidden,
        category=category,
        metadata=cmd_metadata,
        parent=parent,
    )

    # Build full registry key
    full_name = f"{parent}.{command_name}" if parent else command_name

    # Build registry metadata
    reg_metadata = {
        "INFO": info,
        "description": info.description,
        "aliases": info.aliases,
        "hidden": hidden,
        "category": category,
        "parent": parent,
        "is_group": group,
        "_prebuilt_click_command": click_cmd,  # Use new, clearer name
    }
    reg_metadata.update(extra_metadata)

    # Register in the registry
    reg.register(
        name=full_name,
        value=func,
        dimension=ComponentCategory.COMMAND.value,
        metadata=reg_metadata,
        aliases=aliases,
        replace=replace,
    )

    # Add metadata to the function
    func.__registry_name__ = command_name  # type: ignore[attr-defined]
    func.__registry_dimension__ = ComponentCategory.COMMAND.value  # type: ignore[attr-defined]
    func.__registry_info__ = info  # type: ignore[attr-defined]

    get_foundation_logger().trace(f"Registered command: {full_name}")

    return func


def x__register_command_func__mutmut_72(
    func: F,
    *,
    name: str | None = None,
    description: str | None = None,
    aliases: list[str] | None = None,
    hidden: bool = False,
    category: str | None = None,
    group: bool = False,
    replace: bool = False,
    registry: Registry | None = None,
    **extra_metadata: Any,
) -> F:
    """Internal function to register a command."""
    reg = registry or get_command_registry()

    # Determine command name and parent from dot notation
    if name:
        parts = name.split(".")
        if len(parts) > 1:
            # Extract parent path and command name
            parent = ".".join(parts[:-1])
            command_name = parts[-1]

            # Auto-create parent groups if they don't exist (click only)
            _, has_click = _get_click()
            if has_click:
                ensure_parent_groups_fn = _get_ensure_parent_groups()
                if ensure_parent_groups_fn:
                    ensure_parent_groups_fn(parent, reg)
        else:
            parent = None
            command_name = name
    else:
        # Use function name as command name
        parent = None
        command_name = getattr(func, "__name__", "<anonymous>")

    # Check if it's already a Click command
    click_cmd = None
    click_module, has_click = _get_click()
    if has_click and isinstance(func, click_module.Command):
        click_cmd = func
        actual_func = func.callback
    else:
        actual_func = func

    # Create command info
    cmd_metadata = {"is_group": group}
    cmd_metadata.update(extra_metadata)

    info = CommandInfo(
        name=command_name,
        func=actual_func,
        description=description or (actual_func.__doc__ if actual_func else None),
        aliases=aliases or [],
        hidden=hidden,
        category=category,
        metadata=cmd_metadata,
        parent=parent,
    )

    # Build full registry key
    full_name = f"{parent}.{command_name}" if parent else command_name

    # Build registry metadata
    reg_metadata = {
        "info": info,
        "XXdescriptionXX": info.description,
        "aliases": info.aliases,
        "hidden": hidden,
        "category": category,
        "parent": parent,
        "is_group": group,
        "_prebuilt_click_command": click_cmd,  # Use new, clearer name
    }
    reg_metadata.update(extra_metadata)

    # Register in the registry
    reg.register(
        name=full_name,
        value=func,
        dimension=ComponentCategory.COMMAND.value,
        metadata=reg_metadata,
        aliases=aliases,
        replace=replace,
    )

    # Add metadata to the function
    func.__registry_name__ = command_name  # type: ignore[attr-defined]
    func.__registry_dimension__ = ComponentCategory.COMMAND.value  # type: ignore[attr-defined]
    func.__registry_info__ = info  # type: ignore[attr-defined]

    get_foundation_logger().trace(f"Registered command: {full_name}")

    return func


def x__register_command_func__mutmut_73(
    func: F,
    *,
    name: str | None = None,
    description: str | None = None,
    aliases: list[str] | None = None,
    hidden: bool = False,
    category: str | None = None,
    group: bool = False,
    replace: bool = False,
    registry: Registry | None = None,
    **extra_metadata: Any,
) -> F:
    """Internal function to register a command."""
    reg = registry or get_command_registry()

    # Determine command name and parent from dot notation
    if name:
        parts = name.split(".")
        if len(parts) > 1:
            # Extract parent path and command name
            parent = ".".join(parts[:-1])
            command_name = parts[-1]

            # Auto-create parent groups if they don't exist (click only)
            _, has_click = _get_click()
            if has_click:
                ensure_parent_groups_fn = _get_ensure_parent_groups()
                if ensure_parent_groups_fn:
                    ensure_parent_groups_fn(parent, reg)
        else:
            parent = None
            command_name = name
    else:
        # Use function name as command name
        parent = None
        command_name = getattr(func, "__name__", "<anonymous>")

    # Check if it's already a Click command
    click_cmd = None
    click_module, has_click = _get_click()
    if has_click and isinstance(func, click_module.Command):
        click_cmd = func
        actual_func = func.callback
    else:
        actual_func = func

    # Create command info
    cmd_metadata = {"is_group": group}
    cmd_metadata.update(extra_metadata)

    info = CommandInfo(
        name=command_name,
        func=actual_func,
        description=description or (actual_func.__doc__ if actual_func else None),
        aliases=aliases or [],
        hidden=hidden,
        category=category,
        metadata=cmd_metadata,
        parent=parent,
    )

    # Build full registry key
    full_name = f"{parent}.{command_name}" if parent else command_name

    # Build registry metadata
    reg_metadata = {
        "info": info,
        "DESCRIPTION": info.description,
        "aliases": info.aliases,
        "hidden": hidden,
        "category": category,
        "parent": parent,
        "is_group": group,
        "_prebuilt_click_command": click_cmd,  # Use new, clearer name
    }
    reg_metadata.update(extra_metadata)

    # Register in the registry
    reg.register(
        name=full_name,
        value=func,
        dimension=ComponentCategory.COMMAND.value,
        metadata=reg_metadata,
        aliases=aliases,
        replace=replace,
    )

    # Add metadata to the function
    func.__registry_name__ = command_name  # type: ignore[attr-defined]
    func.__registry_dimension__ = ComponentCategory.COMMAND.value  # type: ignore[attr-defined]
    func.__registry_info__ = info  # type: ignore[attr-defined]

    get_foundation_logger().trace(f"Registered command: {full_name}")

    return func


def x__register_command_func__mutmut_74(
    func: F,
    *,
    name: str | None = None,
    description: str | None = None,
    aliases: list[str] | None = None,
    hidden: bool = False,
    category: str | None = None,
    group: bool = False,
    replace: bool = False,
    registry: Registry | None = None,
    **extra_metadata: Any,
) -> F:
    """Internal function to register a command."""
    reg = registry or get_command_registry()

    # Determine command name and parent from dot notation
    if name:
        parts = name.split(".")
        if len(parts) > 1:
            # Extract parent path and command name
            parent = ".".join(parts[:-1])
            command_name = parts[-1]

            # Auto-create parent groups if they don't exist (click only)
            _, has_click = _get_click()
            if has_click:
                ensure_parent_groups_fn = _get_ensure_parent_groups()
                if ensure_parent_groups_fn:
                    ensure_parent_groups_fn(parent, reg)
        else:
            parent = None
            command_name = name
    else:
        # Use function name as command name
        parent = None
        command_name = getattr(func, "__name__", "<anonymous>")

    # Check if it's already a Click command
    click_cmd = None
    click_module, has_click = _get_click()
    if has_click and isinstance(func, click_module.Command):
        click_cmd = func
        actual_func = func.callback
    else:
        actual_func = func

    # Create command info
    cmd_metadata = {"is_group": group}
    cmd_metadata.update(extra_metadata)

    info = CommandInfo(
        name=command_name,
        func=actual_func,
        description=description or (actual_func.__doc__ if actual_func else None),
        aliases=aliases or [],
        hidden=hidden,
        category=category,
        metadata=cmd_metadata,
        parent=parent,
    )

    # Build full registry key
    full_name = f"{parent}.{command_name}" if parent else command_name

    # Build registry metadata
    reg_metadata = {
        "info": info,
        "description": info.description,
        "XXaliasesXX": info.aliases,
        "hidden": hidden,
        "category": category,
        "parent": parent,
        "is_group": group,
        "_prebuilt_click_command": click_cmd,  # Use new, clearer name
    }
    reg_metadata.update(extra_metadata)

    # Register in the registry
    reg.register(
        name=full_name,
        value=func,
        dimension=ComponentCategory.COMMAND.value,
        metadata=reg_metadata,
        aliases=aliases,
        replace=replace,
    )

    # Add metadata to the function
    func.__registry_name__ = command_name  # type: ignore[attr-defined]
    func.__registry_dimension__ = ComponentCategory.COMMAND.value  # type: ignore[attr-defined]
    func.__registry_info__ = info  # type: ignore[attr-defined]

    get_foundation_logger().trace(f"Registered command: {full_name}")

    return func


def x__register_command_func__mutmut_75(
    func: F,
    *,
    name: str | None = None,
    description: str | None = None,
    aliases: list[str] | None = None,
    hidden: bool = False,
    category: str | None = None,
    group: bool = False,
    replace: bool = False,
    registry: Registry | None = None,
    **extra_metadata: Any,
) -> F:
    """Internal function to register a command."""
    reg = registry or get_command_registry()

    # Determine command name and parent from dot notation
    if name:
        parts = name.split(".")
        if len(parts) > 1:
            # Extract parent path and command name
            parent = ".".join(parts[:-1])
            command_name = parts[-1]

            # Auto-create parent groups if they don't exist (click only)
            _, has_click = _get_click()
            if has_click:
                ensure_parent_groups_fn = _get_ensure_parent_groups()
                if ensure_parent_groups_fn:
                    ensure_parent_groups_fn(parent, reg)
        else:
            parent = None
            command_name = name
    else:
        # Use function name as command name
        parent = None
        command_name = getattr(func, "__name__", "<anonymous>")

    # Check if it's already a Click command
    click_cmd = None
    click_module, has_click = _get_click()
    if has_click and isinstance(func, click_module.Command):
        click_cmd = func
        actual_func = func.callback
    else:
        actual_func = func

    # Create command info
    cmd_metadata = {"is_group": group}
    cmd_metadata.update(extra_metadata)

    info = CommandInfo(
        name=command_name,
        func=actual_func,
        description=description or (actual_func.__doc__ if actual_func else None),
        aliases=aliases or [],
        hidden=hidden,
        category=category,
        metadata=cmd_metadata,
        parent=parent,
    )

    # Build full registry key
    full_name = f"{parent}.{command_name}" if parent else command_name

    # Build registry metadata
    reg_metadata = {
        "info": info,
        "description": info.description,
        "ALIASES": info.aliases,
        "hidden": hidden,
        "category": category,
        "parent": parent,
        "is_group": group,
        "_prebuilt_click_command": click_cmd,  # Use new, clearer name
    }
    reg_metadata.update(extra_metadata)

    # Register in the registry
    reg.register(
        name=full_name,
        value=func,
        dimension=ComponentCategory.COMMAND.value,
        metadata=reg_metadata,
        aliases=aliases,
        replace=replace,
    )

    # Add metadata to the function
    func.__registry_name__ = command_name  # type: ignore[attr-defined]
    func.__registry_dimension__ = ComponentCategory.COMMAND.value  # type: ignore[attr-defined]
    func.__registry_info__ = info  # type: ignore[attr-defined]

    get_foundation_logger().trace(f"Registered command: {full_name}")

    return func


def x__register_command_func__mutmut_76(
    func: F,
    *,
    name: str | None = None,
    description: str | None = None,
    aliases: list[str] | None = None,
    hidden: bool = False,
    category: str | None = None,
    group: bool = False,
    replace: bool = False,
    registry: Registry | None = None,
    **extra_metadata: Any,
) -> F:
    """Internal function to register a command."""
    reg = registry or get_command_registry()

    # Determine command name and parent from dot notation
    if name:
        parts = name.split(".")
        if len(parts) > 1:
            # Extract parent path and command name
            parent = ".".join(parts[:-1])
            command_name = parts[-1]

            # Auto-create parent groups if they don't exist (click only)
            _, has_click = _get_click()
            if has_click:
                ensure_parent_groups_fn = _get_ensure_parent_groups()
                if ensure_parent_groups_fn:
                    ensure_parent_groups_fn(parent, reg)
        else:
            parent = None
            command_name = name
    else:
        # Use function name as command name
        parent = None
        command_name = getattr(func, "__name__", "<anonymous>")

    # Check if it's already a Click command
    click_cmd = None
    click_module, has_click = _get_click()
    if has_click and isinstance(func, click_module.Command):
        click_cmd = func
        actual_func = func.callback
    else:
        actual_func = func

    # Create command info
    cmd_metadata = {"is_group": group}
    cmd_metadata.update(extra_metadata)

    info = CommandInfo(
        name=command_name,
        func=actual_func,
        description=description or (actual_func.__doc__ if actual_func else None),
        aliases=aliases or [],
        hidden=hidden,
        category=category,
        metadata=cmd_metadata,
        parent=parent,
    )

    # Build full registry key
    full_name = f"{parent}.{command_name}" if parent else command_name

    # Build registry metadata
    reg_metadata = {
        "info": info,
        "description": info.description,
        "aliases": info.aliases,
        "XXhiddenXX": hidden,
        "category": category,
        "parent": parent,
        "is_group": group,
        "_prebuilt_click_command": click_cmd,  # Use new, clearer name
    }
    reg_metadata.update(extra_metadata)

    # Register in the registry
    reg.register(
        name=full_name,
        value=func,
        dimension=ComponentCategory.COMMAND.value,
        metadata=reg_metadata,
        aliases=aliases,
        replace=replace,
    )

    # Add metadata to the function
    func.__registry_name__ = command_name  # type: ignore[attr-defined]
    func.__registry_dimension__ = ComponentCategory.COMMAND.value  # type: ignore[attr-defined]
    func.__registry_info__ = info  # type: ignore[attr-defined]

    get_foundation_logger().trace(f"Registered command: {full_name}")

    return func


def x__register_command_func__mutmut_77(
    func: F,
    *,
    name: str | None = None,
    description: str | None = None,
    aliases: list[str] | None = None,
    hidden: bool = False,
    category: str | None = None,
    group: bool = False,
    replace: bool = False,
    registry: Registry | None = None,
    **extra_metadata: Any,
) -> F:
    """Internal function to register a command."""
    reg = registry or get_command_registry()

    # Determine command name and parent from dot notation
    if name:
        parts = name.split(".")
        if len(parts) > 1:
            # Extract parent path and command name
            parent = ".".join(parts[:-1])
            command_name = parts[-1]

            # Auto-create parent groups if they don't exist (click only)
            _, has_click = _get_click()
            if has_click:
                ensure_parent_groups_fn = _get_ensure_parent_groups()
                if ensure_parent_groups_fn:
                    ensure_parent_groups_fn(parent, reg)
        else:
            parent = None
            command_name = name
    else:
        # Use function name as command name
        parent = None
        command_name = getattr(func, "__name__", "<anonymous>")

    # Check if it's already a Click command
    click_cmd = None
    click_module, has_click = _get_click()
    if has_click and isinstance(func, click_module.Command):
        click_cmd = func
        actual_func = func.callback
    else:
        actual_func = func

    # Create command info
    cmd_metadata = {"is_group": group}
    cmd_metadata.update(extra_metadata)

    info = CommandInfo(
        name=command_name,
        func=actual_func,
        description=description or (actual_func.__doc__ if actual_func else None),
        aliases=aliases or [],
        hidden=hidden,
        category=category,
        metadata=cmd_metadata,
        parent=parent,
    )

    # Build full registry key
    full_name = f"{parent}.{command_name}" if parent else command_name

    # Build registry metadata
    reg_metadata = {
        "info": info,
        "description": info.description,
        "aliases": info.aliases,
        "HIDDEN": hidden,
        "category": category,
        "parent": parent,
        "is_group": group,
        "_prebuilt_click_command": click_cmd,  # Use new, clearer name
    }
    reg_metadata.update(extra_metadata)

    # Register in the registry
    reg.register(
        name=full_name,
        value=func,
        dimension=ComponentCategory.COMMAND.value,
        metadata=reg_metadata,
        aliases=aliases,
        replace=replace,
    )

    # Add metadata to the function
    func.__registry_name__ = command_name  # type: ignore[attr-defined]
    func.__registry_dimension__ = ComponentCategory.COMMAND.value  # type: ignore[attr-defined]
    func.__registry_info__ = info  # type: ignore[attr-defined]

    get_foundation_logger().trace(f"Registered command: {full_name}")

    return func


def x__register_command_func__mutmut_78(
    func: F,
    *,
    name: str | None = None,
    description: str | None = None,
    aliases: list[str] | None = None,
    hidden: bool = False,
    category: str | None = None,
    group: bool = False,
    replace: bool = False,
    registry: Registry | None = None,
    **extra_metadata: Any,
) -> F:
    """Internal function to register a command."""
    reg = registry or get_command_registry()

    # Determine command name and parent from dot notation
    if name:
        parts = name.split(".")
        if len(parts) > 1:
            # Extract parent path and command name
            parent = ".".join(parts[:-1])
            command_name = parts[-1]

            # Auto-create parent groups if they don't exist (click only)
            _, has_click = _get_click()
            if has_click:
                ensure_parent_groups_fn = _get_ensure_parent_groups()
                if ensure_parent_groups_fn:
                    ensure_parent_groups_fn(parent, reg)
        else:
            parent = None
            command_name = name
    else:
        # Use function name as command name
        parent = None
        command_name = getattr(func, "__name__", "<anonymous>")

    # Check if it's already a Click command
    click_cmd = None
    click_module, has_click = _get_click()
    if has_click and isinstance(func, click_module.Command):
        click_cmd = func
        actual_func = func.callback
    else:
        actual_func = func

    # Create command info
    cmd_metadata = {"is_group": group}
    cmd_metadata.update(extra_metadata)

    info = CommandInfo(
        name=command_name,
        func=actual_func,
        description=description or (actual_func.__doc__ if actual_func else None),
        aliases=aliases or [],
        hidden=hidden,
        category=category,
        metadata=cmd_metadata,
        parent=parent,
    )

    # Build full registry key
    full_name = f"{parent}.{command_name}" if parent else command_name

    # Build registry metadata
    reg_metadata = {
        "info": info,
        "description": info.description,
        "aliases": info.aliases,
        "hidden": hidden,
        "XXcategoryXX": category,
        "parent": parent,
        "is_group": group,
        "_prebuilt_click_command": click_cmd,  # Use new, clearer name
    }
    reg_metadata.update(extra_metadata)

    # Register in the registry
    reg.register(
        name=full_name,
        value=func,
        dimension=ComponentCategory.COMMAND.value,
        metadata=reg_metadata,
        aliases=aliases,
        replace=replace,
    )

    # Add metadata to the function
    func.__registry_name__ = command_name  # type: ignore[attr-defined]
    func.__registry_dimension__ = ComponentCategory.COMMAND.value  # type: ignore[attr-defined]
    func.__registry_info__ = info  # type: ignore[attr-defined]

    get_foundation_logger().trace(f"Registered command: {full_name}")

    return func


def x__register_command_func__mutmut_79(
    func: F,
    *,
    name: str | None = None,
    description: str | None = None,
    aliases: list[str] | None = None,
    hidden: bool = False,
    category: str | None = None,
    group: bool = False,
    replace: bool = False,
    registry: Registry | None = None,
    **extra_metadata: Any,
) -> F:
    """Internal function to register a command."""
    reg = registry or get_command_registry()

    # Determine command name and parent from dot notation
    if name:
        parts = name.split(".")
        if len(parts) > 1:
            # Extract parent path and command name
            parent = ".".join(parts[:-1])
            command_name = parts[-1]

            # Auto-create parent groups if they don't exist (click only)
            _, has_click = _get_click()
            if has_click:
                ensure_parent_groups_fn = _get_ensure_parent_groups()
                if ensure_parent_groups_fn:
                    ensure_parent_groups_fn(parent, reg)
        else:
            parent = None
            command_name = name
    else:
        # Use function name as command name
        parent = None
        command_name = getattr(func, "__name__", "<anonymous>")

    # Check if it's already a Click command
    click_cmd = None
    click_module, has_click = _get_click()
    if has_click and isinstance(func, click_module.Command):
        click_cmd = func
        actual_func = func.callback
    else:
        actual_func = func

    # Create command info
    cmd_metadata = {"is_group": group}
    cmd_metadata.update(extra_metadata)

    info = CommandInfo(
        name=command_name,
        func=actual_func,
        description=description or (actual_func.__doc__ if actual_func else None),
        aliases=aliases or [],
        hidden=hidden,
        category=category,
        metadata=cmd_metadata,
        parent=parent,
    )

    # Build full registry key
    full_name = f"{parent}.{command_name}" if parent else command_name

    # Build registry metadata
    reg_metadata = {
        "info": info,
        "description": info.description,
        "aliases": info.aliases,
        "hidden": hidden,
        "CATEGORY": category,
        "parent": parent,
        "is_group": group,
        "_prebuilt_click_command": click_cmd,  # Use new, clearer name
    }
    reg_metadata.update(extra_metadata)

    # Register in the registry
    reg.register(
        name=full_name,
        value=func,
        dimension=ComponentCategory.COMMAND.value,
        metadata=reg_metadata,
        aliases=aliases,
        replace=replace,
    )

    # Add metadata to the function
    func.__registry_name__ = command_name  # type: ignore[attr-defined]
    func.__registry_dimension__ = ComponentCategory.COMMAND.value  # type: ignore[attr-defined]
    func.__registry_info__ = info  # type: ignore[attr-defined]

    get_foundation_logger().trace(f"Registered command: {full_name}")

    return func


def x__register_command_func__mutmut_80(
    func: F,
    *,
    name: str | None = None,
    description: str | None = None,
    aliases: list[str] | None = None,
    hidden: bool = False,
    category: str | None = None,
    group: bool = False,
    replace: bool = False,
    registry: Registry | None = None,
    **extra_metadata: Any,
) -> F:
    """Internal function to register a command."""
    reg = registry or get_command_registry()

    # Determine command name and parent from dot notation
    if name:
        parts = name.split(".")
        if len(parts) > 1:
            # Extract parent path and command name
            parent = ".".join(parts[:-1])
            command_name = parts[-1]

            # Auto-create parent groups if they don't exist (click only)
            _, has_click = _get_click()
            if has_click:
                ensure_parent_groups_fn = _get_ensure_parent_groups()
                if ensure_parent_groups_fn:
                    ensure_parent_groups_fn(parent, reg)
        else:
            parent = None
            command_name = name
    else:
        # Use function name as command name
        parent = None
        command_name = getattr(func, "__name__", "<anonymous>")

    # Check if it's already a Click command
    click_cmd = None
    click_module, has_click = _get_click()
    if has_click and isinstance(func, click_module.Command):
        click_cmd = func
        actual_func = func.callback
    else:
        actual_func = func

    # Create command info
    cmd_metadata = {"is_group": group}
    cmd_metadata.update(extra_metadata)

    info = CommandInfo(
        name=command_name,
        func=actual_func,
        description=description or (actual_func.__doc__ if actual_func else None),
        aliases=aliases or [],
        hidden=hidden,
        category=category,
        metadata=cmd_metadata,
        parent=parent,
    )

    # Build full registry key
    full_name = f"{parent}.{command_name}" if parent else command_name

    # Build registry metadata
    reg_metadata = {
        "info": info,
        "description": info.description,
        "aliases": info.aliases,
        "hidden": hidden,
        "category": category,
        "XXparentXX": parent,
        "is_group": group,
        "_prebuilt_click_command": click_cmd,  # Use new, clearer name
    }
    reg_metadata.update(extra_metadata)

    # Register in the registry
    reg.register(
        name=full_name,
        value=func,
        dimension=ComponentCategory.COMMAND.value,
        metadata=reg_metadata,
        aliases=aliases,
        replace=replace,
    )

    # Add metadata to the function
    func.__registry_name__ = command_name  # type: ignore[attr-defined]
    func.__registry_dimension__ = ComponentCategory.COMMAND.value  # type: ignore[attr-defined]
    func.__registry_info__ = info  # type: ignore[attr-defined]

    get_foundation_logger().trace(f"Registered command: {full_name}")

    return func


def x__register_command_func__mutmut_81(
    func: F,
    *,
    name: str | None = None,
    description: str | None = None,
    aliases: list[str] | None = None,
    hidden: bool = False,
    category: str | None = None,
    group: bool = False,
    replace: bool = False,
    registry: Registry | None = None,
    **extra_metadata: Any,
) -> F:
    """Internal function to register a command."""
    reg = registry or get_command_registry()

    # Determine command name and parent from dot notation
    if name:
        parts = name.split(".")
        if len(parts) > 1:
            # Extract parent path and command name
            parent = ".".join(parts[:-1])
            command_name = parts[-1]

            # Auto-create parent groups if they don't exist (click only)
            _, has_click = _get_click()
            if has_click:
                ensure_parent_groups_fn = _get_ensure_parent_groups()
                if ensure_parent_groups_fn:
                    ensure_parent_groups_fn(parent, reg)
        else:
            parent = None
            command_name = name
    else:
        # Use function name as command name
        parent = None
        command_name = getattr(func, "__name__", "<anonymous>")

    # Check if it's already a Click command
    click_cmd = None
    click_module, has_click = _get_click()
    if has_click and isinstance(func, click_module.Command):
        click_cmd = func
        actual_func = func.callback
    else:
        actual_func = func

    # Create command info
    cmd_metadata = {"is_group": group}
    cmd_metadata.update(extra_metadata)

    info = CommandInfo(
        name=command_name,
        func=actual_func,
        description=description or (actual_func.__doc__ if actual_func else None),
        aliases=aliases or [],
        hidden=hidden,
        category=category,
        metadata=cmd_metadata,
        parent=parent,
    )

    # Build full registry key
    full_name = f"{parent}.{command_name}" if parent else command_name

    # Build registry metadata
    reg_metadata = {
        "info": info,
        "description": info.description,
        "aliases": info.aliases,
        "hidden": hidden,
        "category": category,
        "PARENT": parent,
        "is_group": group,
        "_prebuilt_click_command": click_cmd,  # Use new, clearer name
    }
    reg_metadata.update(extra_metadata)

    # Register in the registry
    reg.register(
        name=full_name,
        value=func,
        dimension=ComponentCategory.COMMAND.value,
        metadata=reg_metadata,
        aliases=aliases,
        replace=replace,
    )

    # Add metadata to the function
    func.__registry_name__ = command_name  # type: ignore[attr-defined]
    func.__registry_dimension__ = ComponentCategory.COMMAND.value  # type: ignore[attr-defined]
    func.__registry_info__ = info  # type: ignore[attr-defined]

    get_foundation_logger().trace(f"Registered command: {full_name}")

    return func


def x__register_command_func__mutmut_82(
    func: F,
    *,
    name: str | None = None,
    description: str | None = None,
    aliases: list[str] | None = None,
    hidden: bool = False,
    category: str | None = None,
    group: bool = False,
    replace: bool = False,
    registry: Registry | None = None,
    **extra_metadata: Any,
) -> F:
    """Internal function to register a command."""
    reg = registry or get_command_registry()

    # Determine command name and parent from dot notation
    if name:
        parts = name.split(".")
        if len(parts) > 1:
            # Extract parent path and command name
            parent = ".".join(parts[:-1])
            command_name = parts[-1]

            # Auto-create parent groups if they don't exist (click only)
            _, has_click = _get_click()
            if has_click:
                ensure_parent_groups_fn = _get_ensure_parent_groups()
                if ensure_parent_groups_fn:
                    ensure_parent_groups_fn(parent, reg)
        else:
            parent = None
            command_name = name
    else:
        # Use function name as command name
        parent = None
        command_name = getattr(func, "__name__", "<anonymous>")

    # Check if it's already a Click command
    click_cmd = None
    click_module, has_click = _get_click()
    if has_click and isinstance(func, click_module.Command):
        click_cmd = func
        actual_func = func.callback
    else:
        actual_func = func

    # Create command info
    cmd_metadata = {"is_group": group}
    cmd_metadata.update(extra_metadata)

    info = CommandInfo(
        name=command_name,
        func=actual_func,
        description=description or (actual_func.__doc__ if actual_func else None),
        aliases=aliases or [],
        hidden=hidden,
        category=category,
        metadata=cmd_metadata,
        parent=parent,
    )

    # Build full registry key
    full_name = f"{parent}.{command_name}" if parent else command_name

    # Build registry metadata
    reg_metadata = {
        "info": info,
        "description": info.description,
        "aliases": info.aliases,
        "hidden": hidden,
        "category": category,
        "parent": parent,
        "XXis_groupXX": group,
        "_prebuilt_click_command": click_cmd,  # Use new, clearer name
    }
    reg_metadata.update(extra_metadata)

    # Register in the registry
    reg.register(
        name=full_name,
        value=func,
        dimension=ComponentCategory.COMMAND.value,
        metadata=reg_metadata,
        aliases=aliases,
        replace=replace,
    )

    # Add metadata to the function
    func.__registry_name__ = command_name  # type: ignore[attr-defined]
    func.__registry_dimension__ = ComponentCategory.COMMAND.value  # type: ignore[attr-defined]
    func.__registry_info__ = info  # type: ignore[attr-defined]

    get_foundation_logger().trace(f"Registered command: {full_name}")

    return func


def x__register_command_func__mutmut_83(
    func: F,
    *,
    name: str | None = None,
    description: str | None = None,
    aliases: list[str] | None = None,
    hidden: bool = False,
    category: str | None = None,
    group: bool = False,
    replace: bool = False,
    registry: Registry | None = None,
    **extra_metadata: Any,
) -> F:
    """Internal function to register a command."""
    reg = registry or get_command_registry()

    # Determine command name and parent from dot notation
    if name:
        parts = name.split(".")
        if len(parts) > 1:
            # Extract parent path and command name
            parent = ".".join(parts[:-1])
            command_name = parts[-1]

            # Auto-create parent groups if they don't exist (click only)
            _, has_click = _get_click()
            if has_click:
                ensure_parent_groups_fn = _get_ensure_parent_groups()
                if ensure_parent_groups_fn:
                    ensure_parent_groups_fn(parent, reg)
        else:
            parent = None
            command_name = name
    else:
        # Use function name as command name
        parent = None
        command_name = getattr(func, "__name__", "<anonymous>")

    # Check if it's already a Click command
    click_cmd = None
    click_module, has_click = _get_click()
    if has_click and isinstance(func, click_module.Command):
        click_cmd = func
        actual_func = func.callback
    else:
        actual_func = func

    # Create command info
    cmd_metadata = {"is_group": group}
    cmd_metadata.update(extra_metadata)

    info = CommandInfo(
        name=command_name,
        func=actual_func,
        description=description or (actual_func.__doc__ if actual_func else None),
        aliases=aliases or [],
        hidden=hidden,
        category=category,
        metadata=cmd_metadata,
        parent=parent,
    )

    # Build full registry key
    full_name = f"{parent}.{command_name}" if parent else command_name

    # Build registry metadata
    reg_metadata = {
        "info": info,
        "description": info.description,
        "aliases": info.aliases,
        "hidden": hidden,
        "category": category,
        "parent": parent,
        "IS_GROUP": group,
        "_prebuilt_click_command": click_cmd,  # Use new, clearer name
    }
    reg_metadata.update(extra_metadata)

    # Register in the registry
    reg.register(
        name=full_name,
        value=func,
        dimension=ComponentCategory.COMMAND.value,
        metadata=reg_metadata,
        aliases=aliases,
        replace=replace,
    )

    # Add metadata to the function
    func.__registry_name__ = command_name  # type: ignore[attr-defined]
    func.__registry_dimension__ = ComponentCategory.COMMAND.value  # type: ignore[attr-defined]
    func.__registry_info__ = info  # type: ignore[attr-defined]

    get_foundation_logger().trace(f"Registered command: {full_name}")

    return func


def x__register_command_func__mutmut_84(
    func: F,
    *,
    name: str | None = None,
    description: str | None = None,
    aliases: list[str] | None = None,
    hidden: bool = False,
    category: str | None = None,
    group: bool = False,
    replace: bool = False,
    registry: Registry | None = None,
    **extra_metadata: Any,
) -> F:
    """Internal function to register a command."""
    reg = registry or get_command_registry()

    # Determine command name and parent from dot notation
    if name:
        parts = name.split(".")
        if len(parts) > 1:
            # Extract parent path and command name
            parent = ".".join(parts[:-1])
            command_name = parts[-1]

            # Auto-create parent groups if they don't exist (click only)
            _, has_click = _get_click()
            if has_click:
                ensure_parent_groups_fn = _get_ensure_parent_groups()
                if ensure_parent_groups_fn:
                    ensure_parent_groups_fn(parent, reg)
        else:
            parent = None
            command_name = name
    else:
        # Use function name as command name
        parent = None
        command_name = getattr(func, "__name__", "<anonymous>")

    # Check if it's already a Click command
    click_cmd = None
    click_module, has_click = _get_click()
    if has_click and isinstance(func, click_module.Command):
        click_cmd = func
        actual_func = func.callback
    else:
        actual_func = func

    # Create command info
    cmd_metadata = {"is_group": group}
    cmd_metadata.update(extra_metadata)

    info = CommandInfo(
        name=command_name,
        func=actual_func,
        description=description or (actual_func.__doc__ if actual_func else None),
        aliases=aliases or [],
        hidden=hidden,
        category=category,
        metadata=cmd_metadata,
        parent=parent,
    )

    # Build full registry key
    full_name = f"{parent}.{command_name}" if parent else command_name

    # Build registry metadata
    reg_metadata = {
        "info": info,
        "description": info.description,
        "aliases": info.aliases,
        "hidden": hidden,
        "category": category,
        "parent": parent,
        "is_group": group,
        "XX_prebuilt_click_commandXX": click_cmd,  # Use new, clearer name
    }
    reg_metadata.update(extra_metadata)

    # Register in the registry
    reg.register(
        name=full_name,
        value=func,
        dimension=ComponentCategory.COMMAND.value,
        metadata=reg_metadata,
        aliases=aliases,
        replace=replace,
    )

    # Add metadata to the function
    func.__registry_name__ = command_name  # type: ignore[attr-defined]
    func.__registry_dimension__ = ComponentCategory.COMMAND.value  # type: ignore[attr-defined]
    func.__registry_info__ = info  # type: ignore[attr-defined]

    get_foundation_logger().trace(f"Registered command: {full_name}")

    return func


def x__register_command_func__mutmut_85(
    func: F,
    *,
    name: str | None = None,
    description: str | None = None,
    aliases: list[str] | None = None,
    hidden: bool = False,
    category: str | None = None,
    group: bool = False,
    replace: bool = False,
    registry: Registry | None = None,
    **extra_metadata: Any,
) -> F:
    """Internal function to register a command."""
    reg = registry or get_command_registry()

    # Determine command name and parent from dot notation
    if name:
        parts = name.split(".")
        if len(parts) > 1:
            # Extract parent path and command name
            parent = ".".join(parts[:-1])
            command_name = parts[-1]

            # Auto-create parent groups if they don't exist (click only)
            _, has_click = _get_click()
            if has_click:
                ensure_parent_groups_fn = _get_ensure_parent_groups()
                if ensure_parent_groups_fn:
                    ensure_parent_groups_fn(parent, reg)
        else:
            parent = None
            command_name = name
    else:
        # Use function name as command name
        parent = None
        command_name = getattr(func, "__name__", "<anonymous>")

    # Check if it's already a Click command
    click_cmd = None
    click_module, has_click = _get_click()
    if has_click and isinstance(func, click_module.Command):
        click_cmd = func
        actual_func = func.callback
    else:
        actual_func = func

    # Create command info
    cmd_metadata = {"is_group": group}
    cmd_metadata.update(extra_metadata)

    info = CommandInfo(
        name=command_name,
        func=actual_func,
        description=description or (actual_func.__doc__ if actual_func else None),
        aliases=aliases or [],
        hidden=hidden,
        category=category,
        metadata=cmd_metadata,
        parent=parent,
    )

    # Build full registry key
    full_name = f"{parent}.{command_name}" if parent else command_name

    # Build registry metadata
    reg_metadata = {
        "info": info,
        "description": info.description,
        "aliases": info.aliases,
        "hidden": hidden,
        "category": category,
        "parent": parent,
        "is_group": group,
        "_PREBUILT_CLICK_COMMAND": click_cmd,  # Use new, clearer name
    }
    reg_metadata.update(extra_metadata)

    # Register in the registry
    reg.register(
        name=full_name,
        value=func,
        dimension=ComponentCategory.COMMAND.value,
        metadata=reg_metadata,
        aliases=aliases,
        replace=replace,
    )

    # Add metadata to the function
    func.__registry_name__ = command_name  # type: ignore[attr-defined]
    func.__registry_dimension__ = ComponentCategory.COMMAND.value  # type: ignore[attr-defined]
    func.__registry_info__ = info  # type: ignore[attr-defined]

    get_foundation_logger().trace(f"Registered command: {full_name}")

    return func


def x__register_command_func__mutmut_86(
    func: F,
    *,
    name: str | None = None,
    description: str | None = None,
    aliases: list[str] | None = None,
    hidden: bool = False,
    category: str | None = None,
    group: bool = False,
    replace: bool = False,
    registry: Registry | None = None,
    **extra_metadata: Any,
) -> F:
    """Internal function to register a command."""
    reg = registry or get_command_registry()

    # Determine command name and parent from dot notation
    if name:
        parts = name.split(".")
        if len(parts) > 1:
            # Extract parent path and command name
            parent = ".".join(parts[:-1])
            command_name = parts[-1]

            # Auto-create parent groups if they don't exist (click only)
            _, has_click = _get_click()
            if has_click:
                ensure_parent_groups_fn = _get_ensure_parent_groups()
                if ensure_parent_groups_fn:
                    ensure_parent_groups_fn(parent, reg)
        else:
            parent = None
            command_name = name
    else:
        # Use function name as command name
        parent = None
        command_name = getattr(func, "__name__", "<anonymous>")

    # Check if it's already a Click command
    click_cmd = None
    click_module, has_click = _get_click()
    if has_click and isinstance(func, click_module.Command):
        click_cmd = func
        actual_func = func.callback
    else:
        actual_func = func

    # Create command info
    cmd_metadata = {"is_group": group}
    cmd_metadata.update(extra_metadata)

    info = CommandInfo(
        name=command_name,
        func=actual_func,
        description=description or (actual_func.__doc__ if actual_func else None),
        aliases=aliases or [],
        hidden=hidden,
        category=category,
        metadata=cmd_metadata,
        parent=parent,
    )

    # Build full registry key
    full_name = f"{parent}.{command_name}" if parent else command_name

    # Build registry metadata
    reg_metadata = {
        "info": info,
        "description": info.description,
        "aliases": info.aliases,
        "hidden": hidden,
        "category": category,
        "parent": parent,
        "is_group": group,
        "_prebuilt_click_command": click_cmd,  # Use new, clearer name
    }
    reg_metadata.update(None)

    # Register in the registry
    reg.register(
        name=full_name,
        value=func,
        dimension=ComponentCategory.COMMAND.value,
        metadata=reg_metadata,
        aliases=aliases,
        replace=replace,
    )

    # Add metadata to the function
    func.__registry_name__ = command_name  # type: ignore[attr-defined]
    func.__registry_dimension__ = ComponentCategory.COMMAND.value  # type: ignore[attr-defined]
    func.__registry_info__ = info  # type: ignore[attr-defined]

    get_foundation_logger().trace(f"Registered command: {full_name}")

    return func


def x__register_command_func__mutmut_87(
    func: F,
    *,
    name: str | None = None,
    description: str | None = None,
    aliases: list[str] | None = None,
    hidden: bool = False,
    category: str | None = None,
    group: bool = False,
    replace: bool = False,
    registry: Registry | None = None,
    **extra_metadata: Any,
) -> F:
    """Internal function to register a command."""
    reg = registry or get_command_registry()

    # Determine command name and parent from dot notation
    if name:
        parts = name.split(".")
        if len(parts) > 1:
            # Extract parent path and command name
            parent = ".".join(parts[:-1])
            command_name = parts[-1]

            # Auto-create parent groups if they don't exist (click only)
            _, has_click = _get_click()
            if has_click:
                ensure_parent_groups_fn = _get_ensure_parent_groups()
                if ensure_parent_groups_fn:
                    ensure_parent_groups_fn(parent, reg)
        else:
            parent = None
            command_name = name
    else:
        # Use function name as command name
        parent = None
        command_name = getattr(func, "__name__", "<anonymous>")

    # Check if it's already a Click command
    click_cmd = None
    click_module, has_click = _get_click()
    if has_click and isinstance(func, click_module.Command):
        click_cmd = func
        actual_func = func.callback
    else:
        actual_func = func

    # Create command info
    cmd_metadata = {"is_group": group}
    cmd_metadata.update(extra_metadata)

    info = CommandInfo(
        name=command_name,
        func=actual_func,
        description=description or (actual_func.__doc__ if actual_func else None),
        aliases=aliases or [],
        hidden=hidden,
        category=category,
        metadata=cmd_metadata,
        parent=parent,
    )

    # Build full registry key
    full_name = f"{parent}.{command_name}" if parent else command_name

    # Build registry metadata
    reg_metadata = {
        "info": info,
        "description": info.description,
        "aliases": info.aliases,
        "hidden": hidden,
        "category": category,
        "parent": parent,
        "is_group": group,
        "_prebuilt_click_command": click_cmd,  # Use new, clearer name
    }
    reg_metadata.update(extra_metadata)

    # Register in the registry
    reg.register(
        name=None,
        value=func,
        dimension=ComponentCategory.COMMAND.value,
        metadata=reg_metadata,
        aliases=aliases,
        replace=replace,
    )

    # Add metadata to the function
    func.__registry_name__ = command_name  # type: ignore[attr-defined]
    func.__registry_dimension__ = ComponentCategory.COMMAND.value  # type: ignore[attr-defined]
    func.__registry_info__ = info  # type: ignore[attr-defined]

    get_foundation_logger().trace(f"Registered command: {full_name}")

    return func


def x__register_command_func__mutmut_88(
    func: F,
    *,
    name: str | None = None,
    description: str | None = None,
    aliases: list[str] | None = None,
    hidden: bool = False,
    category: str | None = None,
    group: bool = False,
    replace: bool = False,
    registry: Registry | None = None,
    **extra_metadata: Any,
) -> F:
    """Internal function to register a command."""
    reg = registry or get_command_registry()

    # Determine command name and parent from dot notation
    if name:
        parts = name.split(".")
        if len(parts) > 1:
            # Extract parent path and command name
            parent = ".".join(parts[:-1])
            command_name = parts[-1]

            # Auto-create parent groups if they don't exist (click only)
            _, has_click = _get_click()
            if has_click:
                ensure_parent_groups_fn = _get_ensure_parent_groups()
                if ensure_parent_groups_fn:
                    ensure_parent_groups_fn(parent, reg)
        else:
            parent = None
            command_name = name
    else:
        # Use function name as command name
        parent = None
        command_name = getattr(func, "__name__", "<anonymous>")

    # Check if it's already a Click command
    click_cmd = None
    click_module, has_click = _get_click()
    if has_click and isinstance(func, click_module.Command):
        click_cmd = func
        actual_func = func.callback
    else:
        actual_func = func

    # Create command info
    cmd_metadata = {"is_group": group}
    cmd_metadata.update(extra_metadata)

    info = CommandInfo(
        name=command_name,
        func=actual_func,
        description=description or (actual_func.__doc__ if actual_func else None),
        aliases=aliases or [],
        hidden=hidden,
        category=category,
        metadata=cmd_metadata,
        parent=parent,
    )

    # Build full registry key
    full_name = f"{parent}.{command_name}" if parent else command_name

    # Build registry metadata
    reg_metadata = {
        "info": info,
        "description": info.description,
        "aliases": info.aliases,
        "hidden": hidden,
        "category": category,
        "parent": parent,
        "is_group": group,
        "_prebuilt_click_command": click_cmd,  # Use new, clearer name
    }
    reg_metadata.update(extra_metadata)

    # Register in the registry
    reg.register(
        name=full_name,
        value=None,
        dimension=ComponentCategory.COMMAND.value,
        metadata=reg_metadata,
        aliases=aliases,
        replace=replace,
    )

    # Add metadata to the function
    func.__registry_name__ = command_name  # type: ignore[attr-defined]
    func.__registry_dimension__ = ComponentCategory.COMMAND.value  # type: ignore[attr-defined]
    func.__registry_info__ = info  # type: ignore[attr-defined]

    get_foundation_logger().trace(f"Registered command: {full_name}")

    return func


def x__register_command_func__mutmut_89(
    func: F,
    *,
    name: str | None = None,
    description: str | None = None,
    aliases: list[str] | None = None,
    hidden: bool = False,
    category: str | None = None,
    group: bool = False,
    replace: bool = False,
    registry: Registry | None = None,
    **extra_metadata: Any,
) -> F:
    """Internal function to register a command."""
    reg = registry or get_command_registry()

    # Determine command name and parent from dot notation
    if name:
        parts = name.split(".")
        if len(parts) > 1:
            # Extract parent path and command name
            parent = ".".join(parts[:-1])
            command_name = parts[-1]

            # Auto-create parent groups if they don't exist (click only)
            _, has_click = _get_click()
            if has_click:
                ensure_parent_groups_fn = _get_ensure_parent_groups()
                if ensure_parent_groups_fn:
                    ensure_parent_groups_fn(parent, reg)
        else:
            parent = None
            command_name = name
    else:
        # Use function name as command name
        parent = None
        command_name = getattr(func, "__name__", "<anonymous>")

    # Check if it's already a Click command
    click_cmd = None
    click_module, has_click = _get_click()
    if has_click and isinstance(func, click_module.Command):
        click_cmd = func
        actual_func = func.callback
    else:
        actual_func = func

    # Create command info
    cmd_metadata = {"is_group": group}
    cmd_metadata.update(extra_metadata)

    info = CommandInfo(
        name=command_name,
        func=actual_func,
        description=description or (actual_func.__doc__ if actual_func else None),
        aliases=aliases or [],
        hidden=hidden,
        category=category,
        metadata=cmd_metadata,
        parent=parent,
    )

    # Build full registry key
    full_name = f"{parent}.{command_name}" if parent else command_name

    # Build registry metadata
    reg_metadata = {
        "info": info,
        "description": info.description,
        "aliases": info.aliases,
        "hidden": hidden,
        "category": category,
        "parent": parent,
        "is_group": group,
        "_prebuilt_click_command": click_cmd,  # Use new, clearer name
    }
    reg_metadata.update(extra_metadata)

    # Register in the registry
    reg.register(
        name=full_name,
        value=func,
        dimension=None,
        metadata=reg_metadata,
        aliases=aliases,
        replace=replace,
    )

    # Add metadata to the function
    func.__registry_name__ = command_name  # type: ignore[attr-defined]
    func.__registry_dimension__ = ComponentCategory.COMMAND.value  # type: ignore[attr-defined]
    func.__registry_info__ = info  # type: ignore[attr-defined]

    get_foundation_logger().trace(f"Registered command: {full_name}")

    return func


def x__register_command_func__mutmut_90(
    func: F,
    *,
    name: str | None = None,
    description: str | None = None,
    aliases: list[str] | None = None,
    hidden: bool = False,
    category: str | None = None,
    group: bool = False,
    replace: bool = False,
    registry: Registry | None = None,
    **extra_metadata: Any,
) -> F:
    """Internal function to register a command."""
    reg = registry or get_command_registry()

    # Determine command name and parent from dot notation
    if name:
        parts = name.split(".")
        if len(parts) > 1:
            # Extract parent path and command name
            parent = ".".join(parts[:-1])
            command_name = parts[-1]

            # Auto-create parent groups if they don't exist (click only)
            _, has_click = _get_click()
            if has_click:
                ensure_parent_groups_fn = _get_ensure_parent_groups()
                if ensure_parent_groups_fn:
                    ensure_parent_groups_fn(parent, reg)
        else:
            parent = None
            command_name = name
    else:
        # Use function name as command name
        parent = None
        command_name = getattr(func, "__name__", "<anonymous>")

    # Check if it's already a Click command
    click_cmd = None
    click_module, has_click = _get_click()
    if has_click and isinstance(func, click_module.Command):
        click_cmd = func
        actual_func = func.callback
    else:
        actual_func = func

    # Create command info
    cmd_metadata = {"is_group": group}
    cmd_metadata.update(extra_metadata)

    info = CommandInfo(
        name=command_name,
        func=actual_func,
        description=description or (actual_func.__doc__ if actual_func else None),
        aliases=aliases or [],
        hidden=hidden,
        category=category,
        metadata=cmd_metadata,
        parent=parent,
    )

    # Build full registry key
    full_name = f"{parent}.{command_name}" if parent else command_name

    # Build registry metadata
    reg_metadata = {
        "info": info,
        "description": info.description,
        "aliases": info.aliases,
        "hidden": hidden,
        "category": category,
        "parent": parent,
        "is_group": group,
        "_prebuilt_click_command": click_cmd,  # Use new, clearer name
    }
    reg_metadata.update(extra_metadata)

    # Register in the registry
    reg.register(
        name=full_name,
        value=func,
        dimension=ComponentCategory.COMMAND.value,
        metadata=None,
        aliases=aliases,
        replace=replace,
    )

    # Add metadata to the function
    func.__registry_name__ = command_name  # type: ignore[attr-defined]
    func.__registry_dimension__ = ComponentCategory.COMMAND.value  # type: ignore[attr-defined]
    func.__registry_info__ = info  # type: ignore[attr-defined]

    get_foundation_logger().trace(f"Registered command: {full_name}")

    return func


def x__register_command_func__mutmut_91(
    func: F,
    *,
    name: str | None = None,
    description: str | None = None,
    aliases: list[str] | None = None,
    hidden: bool = False,
    category: str | None = None,
    group: bool = False,
    replace: bool = False,
    registry: Registry | None = None,
    **extra_metadata: Any,
) -> F:
    """Internal function to register a command."""
    reg = registry or get_command_registry()

    # Determine command name and parent from dot notation
    if name:
        parts = name.split(".")
        if len(parts) > 1:
            # Extract parent path and command name
            parent = ".".join(parts[:-1])
            command_name = parts[-1]

            # Auto-create parent groups if they don't exist (click only)
            _, has_click = _get_click()
            if has_click:
                ensure_parent_groups_fn = _get_ensure_parent_groups()
                if ensure_parent_groups_fn:
                    ensure_parent_groups_fn(parent, reg)
        else:
            parent = None
            command_name = name
    else:
        # Use function name as command name
        parent = None
        command_name = getattr(func, "__name__", "<anonymous>")

    # Check if it's already a Click command
    click_cmd = None
    click_module, has_click = _get_click()
    if has_click and isinstance(func, click_module.Command):
        click_cmd = func
        actual_func = func.callback
    else:
        actual_func = func

    # Create command info
    cmd_metadata = {"is_group": group}
    cmd_metadata.update(extra_metadata)

    info = CommandInfo(
        name=command_name,
        func=actual_func,
        description=description or (actual_func.__doc__ if actual_func else None),
        aliases=aliases or [],
        hidden=hidden,
        category=category,
        metadata=cmd_metadata,
        parent=parent,
    )

    # Build full registry key
    full_name = f"{parent}.{command_name}" if parent else command_name

    # Build registry metadata
    reg_metadata = {
        "info": info,
        "description": info.description,
        "aliases": info.aliases,
        "hidden": hidden,
        "category": category,
        "parent": parent,
        "is_group": group,
        "_prebuilt_click_command": click_cmd,  # Use new, clearer name
    }
    reg_metadata.update(extra_metadata)

    # Register in the registry
    reg.register(
        name=full_name,
        value=func,
        dimension=ComponentCategory.COMMAND.value,
        metadata=reg_metadata,
        aliases=None,
        replace=replace,
    )

    # Add metadata to the function
    func.__registry_name__ = command_name  # type: ignore[attr-defined]
    func.__registry_dimension__ = ComponentCategory.COMMAND.value  # type: ignore[attr-defined]
    func.__registry_info__ = info  # type: ignore[attr-defined]

    get_foundation_logger().trace(f"Registered command: {full_name}")

    return func


def x__register_command_func__mutmut_92(
    func: F,
    *,
    name: str | None = None,
    description: str | None = None,
    aliases: list[str] | None = None,
    hidden: bool = False,
    category: str | None = None,
    group: bool = False,
    replace: bool = False,
    registry: Registry | None = None,
    **extra_metadata: Any,
) -> F:
    """Internal function to register a command."""
    reg = registry or get_command_registry()

    # Determine command name and parent from dot notation
    if name:
        parts = name.split(".")
        if len(parts) > 1:
            # Extract parent path and command name
            parent = ".".join(parts[:-1])
            command_name = parts[-1]

            # Auto-create parent groups if they don't exist (click only)
            _, has_click = _get_click()
            if has_click:
                ensure_parent_groups_fn = _get_ensure_parent_groups()
                if ensure_parent_groups_fn:
                    ensure_parent_groups_fn(parent, reg)
        else:
            parent = None
            command_name = name
    else:
        # Use function name as command name
        parent = None
        command_name = getattr(func, "__name__", "<anonymous>")

    # Check if it's already a Click command
    click_cmd = None
    click_module, has_click = _get_click()
    if has_click and isinstance(func, click_module.Command):
        click_cmd = func
        actual_func = func.callback
    else:
        actual_func = func

    # Create command info
    cmd_metadata = {"is_group": group}
    cmd_metadata.update(extra_metadata)

    info = CommandInfo(
        name=command_name,
        func=actual_func,
        description=description or (actual_func.__doc__ if actual_func else None),
        aliases=aliases or [],
        hidden=hidden,
        category=category,
        metadata=cmd_metadata,
        parent=parent,
    )

    # Build full registry key
    full_name = f"{parent}.{command_name}" if parent else command_name

    # Build registry metadata
    reg_metadata = {
        "info": info,
        "description": info.description,
        "aliases": info.aliases,
        "hidden": hidden,
        "category": category,
        "parent": parent,
        "is_group": group,
        "_prebuilt_click_command": click_cmd,  # Use new, clearer name
    }
    reg_metadata.update(extra_metadata)

    # Register in the registry
    reg.register(
        name=full_name,
        value=func,
        dimension=ComponentCategory.COMMAND.value,
        metadata=reg_metadata,
        aliases=aliases,
        replace=None,
    )

    # Add metadata to the function
    func.__registry_name__ = command_name  # type: ignore[attr-defined]
    func.__registry_dimension__ = ComponentCategory.COMMAND.value  # type: ignore[attr-defined]
    func.__registry_info__ = info  # type: ignore[attr-defined]

    get_foundation_logger().trace(f"Registered command: {full_name}")

    return func


def x__register_command_func__mutmut_93(
    func: F,
    *,
    name: str | None = None,
    description: str | None = None,
    aliases: list[str] | None = None,
    hidden: bool = False,
    category: str | None = None,
    group: bool = False,
    replace: bool = False,
    registry: Registry | None = None,
    **extra_metadata: Any,
) -> F:
    """Internal function to register a command."""
    reg = registry or get_command_registry()

    # Determine command name and parent from dot notation
    if name:
        parts = name.split(".")
        if len(parts) > 1:
            # Extract parent path and command name
            parent = ".".join(parts[:-1])
            command_name = parts[-1]

            # Auto-create parent groups if they don't exist (click only)
            _, has_click = _get_click()
            if has_click:
                ensure_parent_groups_fn = _get_ensure_parent_groups()
                if ensure_parent_groups_fn:
                    ensure_parent_groups_fn(parent, reg)
        else:
            parent = None
            command_name = name
    else:
        # Use function name as command name
        parent = None
        command_name = getattr(func, "__name__", "<anonymous>")

    # Check if it's already a Click command
    click_cmd = None
    click_module, has_click = _get_click()
    if has_click and isinstance(func, click_module.Command):
        click_cmd = func
        actual_func = func.callback
    else:
        actual_func = func

    # Create command info
    cmd_metadata = {"is_group": group}
    cmd_metadata.update(extra_metadata)

    info = CommandInfo(
        name=command_name,
        func=actual_func,
        description=description or (actual_func.__doc__ if actual_func else None),
        aliases=aliases or [],
        hidden=hidden,
        category=category,
        metadata=cmd_metadata,
        parent=parent,
    )

    # Build full registry key
    full_name = f"{parent}.{command_name}" if parent else command_name

    # Build registry metadata
    reg_metadata = {
        "info": info,
        "description": info.description,
        "aliases": info.aliases,
        "hidden": hidden,
        "category": category,
        "parent": parent,
        "is_group": group,
        "_prebuilt_click_command": click_cmd,  # Use new, clearer name
    }
    reg_metadata.update(extra_metadata)

    # Register in the registry
    reg.register(
        value=func,
        dimension=ComponentCategory.COMMAND.value,
        metadata=reg_metadata,
        aliases=aliases,
        replace=replace,
    )

    # Add metadata to the function
    func.__registry_name__ = command_name  # type: ignore[attr-defined]
    func.__registry_dimension__ = ComponentCategory.COMMAND.value  # type: ignore[attr-defined]
    func.__registry_info__ = info  # type: ignore[attr-defined]

    get_foundation_logger().trace(f"Registered command: {full_name}")

    return func


def x__register_command_func__mutmut_94(
    func: F,
    *,
    name: str | None = None,
    description: str | None = None,
    aliases: list[str] | None = None,
    hidden: bool = False,
    category: str | None = None,
    group: bool = False,
    replace: bool = False,
    registry: Registry | None = None,
    **extra_metadata: Any,
) -> F:
    """Internal function to register a command."""
    reg = registry or get_command_registry()

    # Determine command name and parent from dot notation
    if name:
        parts = name.split(".")
        if len(parts) > 1:
            # Extract parent path and command name
            parent = ".".join(parts[:-1])
            command_name = parts[-1]

            # Auto-create parent groups if they don't exist (click only)
            _, has_click = _get_click()
            if has_click:
                ensure_parent_groups_fn = _get_ensure_parent_groups()
                if ensure_parent_groups_fn:
                    ensure_parent_groups_fn(parent, reg)
        else:
            parent = None
            command_name = name
    else:
        # Use function name as command name
        parent = None
        command_name = getattr(func, "__name__", "<anonymous>")

    # Check if it's already a Click command
    click_cmd = None
    click_module, has_click = _get_click()
    if has_click and isinstance(func, click_module.Command):
        click_cmd = func
        actual_func = func.callback
    else:
        actual_func = func

    # Create command info
    cmd_metadata = {"is_group": group}
    cmd_metadata.update(extra_metadata)

    info = CommandInfo(
        name=command_name,
        func=actual_func,
        description=description or (actual_func.__doc__ if actual_func else None),
        aliases=aliases or [],
        hidden=hidden,
        category=category,
        metadata=cmd_metadata,
        parent=parent,
    )

    # Build full registry key
    full_name = f"{parent}.{command_name}" if parent else command_name

    # Build registry metadata
    reg_metadata = {
        "info": info,
        "description": info.description,
        "aliases": info.aliases,
        "hidden": hidden,
        "category": category,
        "parent": parent,
        "is_group": group,
        "_prebuilt_click_command": click_cmd,  # Use new, clearer name
    }
    reg_metadata.update(extra_metadata)

    # Register in the registry
    reg.register(
        name=full_name,
        dimension=ComponentCategory.COMMAND.value,
        metadata=reg_metadata,
        aliases=aliases,
        replace=replace,
    )

    # Add metadata to the function
    func.__registry_name__ = command_name  # type: ignore[attr-defined]
    func.__registry_dimension__ = ComponentCategory.COMMAND.value  # type: ignore[attr-defined]
    func.__registry_info__ = info  # type: ignore[attr-defined]

    get_foundation_logger().trace(f"Registered command: {full_name}")

    return func


def x__register_command_func__mutmut_95(
    func: F,
    *,
    name: str | None = None,
    description: str | None = None,
    aliases: list[str] | None = None,
    hidden: bool = False,
    category: str | None = None,
    group: bool = False,
    replace: bool = False,
    registry: Registry | None = None,
    **extra_metadata: Any,
) -> F:
    """Internal function to register a command."""
    reg = registry or get_command_registry()

    # Determine command name and parent from dot notation
    if name:
        parts = name.split(".")
        if len(parts) > 1:
            # Extract parent path and command name
            parent = ".".join(parts[:-1])
            command_name = parts[-1]

            # Auto-create parent groups if they don't exist (click only)
            _, has_click = _get_click()
            if has_click:
                ensure_parent_groups_fn = _get_ensure_parent_groups()
                if ensure_parent_groups_fn:
                    ensure_parent_groups_fn(parent, reg)
        else:
            parent = None
            command_name = name
    else:
        # Use function name as command name
        parent = None
        command_name = getattr(func, "__name__", "<anonymous>")

    # Check if it's already a Click command
    click_cmd = None
    click_module, has_click = _get_click()
    if has_click and isinstance(func, click_module.Command):
        click_cmd = func
        actual_func = func.callback
    else:
        actual_func = func

    # Create command info
    cmd_metadata = {"is_group": group}
    cmd_metadata.update(extra_metadata)

    info = CommandInfo(
        name=command_name,
        func=actual_func,
        description=description or (actual_func.__doc__ if actual_func else None),
        aliases=aliases or [],
        hidden=hidden,
        category=category,
        metadata=cmd_metadata,
        parent=parent,
    )

    # Build full registry key
    full_name = f"{parent}.{command_name}" if parent else command_name

    # Build registry metadata
    reg_metadata = {
        "info": info,
        "description": info.description,
        "aliases": info.aliases,
        "hidden": hidden,
        "category": category,
        "parent": parent,
        "is_group": group,
        "_prebuilt_click_command": click_cmd,  # Use new, clearer name
    }
    reg_metadata.update(extra_metadata)

    # Register in the registry
    reg.register(
        name=full_name,
        value=func,
        metadata=reg_metadata,
        aliases=aliases,
        replace=replace,
    )

    # Add metadata to the function
    func.__registry_name__ = command_name  # type: ignore[attr-defined]
    func.__registry_dimension__ = ComponentCategory.COMMAND.value  # type: ignore[attr-defined]
    func.__registry_info__ = info  # type: ignore[attr-defined]

    get_foundation_logger().trace(f"Registered command: {full_name}")

    return func


def x__register_command_func__mutmut_96(
    func: F,
    *,
    name: str | None = None,
    description: str | None = None,
    aliases: list[str] | None = None,
    hidden: bool = False,
    category: str | None = None,
    group: bool = False,
    replace: bool = False,
    registry: Registry | None = None,
    **extra_metadata: Any,
) -> F:
    """Internal function to register a command."""
    reg = registry or get_command_registry()

    # Determine command name and parent from dot notation
    if name:
        parts = name.split(".")
        if len(parts) > 1:
            # Extract parent path and command name
            parent = ".".join(parts[:-1])
            command_name = parts[-1]

            # Auto-create parent groups if they don't exist (click only)
            _, has_click = _get_click()
            if has_click:
                ensure_parent_groups_fn = _get_ensure_parent_groups()
                if ensure_parent_groups_fn:
                    ensure_parent_groups_fn(parent, reg)
        else:
            parent = None
            command_name = name
    else:
        # Use function name as command name
        parent = None
        command_name = getattr(func, "__name__", "<anonymous>")

    # Check if it's already a Click command
    click_cmd = None
    click_module, has_click = _get_click()
    if has_click and isinstance(func, click_module.Command):
        click_cmd = func
        actual_func = func.callback
    else:
        actual_func = func

    # Create command info
    cmd_metadata = {"is_group": group}
    cmd_metadata.update(extra_metadata)

    info = CommandInfo(
        name=command_name,
        func=actual_func,
        description=description or (actual_func.__doc__ if actual_func else None),
        aliases=aliases or [],
        hidden=hidden,
        category=category,
        metadata=cmd_metadata,
        parent=parent,
    )

    # Build full registry key
    full_name = f"{parent}.{command_name}" if parent else command_name

    # Build registry metadata
    reg_metadata = {
        "info": info,
        "description": info.description,
        "aliases": info.aliases,
        "hidden": hidden,
        "category": category,
        "parent": parent,
        "is_group": group,
        "_prebuilt_click_command": click_cmd,  # Use new, clearer name
    }
    reg_metadata.update(extra_metadata)

    # Register in the registry
    reg.register(
        name=full_name,
        value=func,
        dimension=ComponentCategory.COMMAND.value,
        aliases=aliases,
        replace=replace,
    )

    # Add metadata to the function
    func.__registry_name__ = command_name  # type: ignore[attr-defined]
    func.__registry_dimension__ = ComponentCategory.COMMAND.value  # type: ignore[attr-defined]
    func.__registry_info__ = info  # type: ignore[attr-defined]

    get_foundation_logger().trace(f"Registered command: {full_name}")

    return func


def x__register_command_func__mutmut_97(
    func: F,
    *,
    name: str | None = None,
    description: str | None = None,
    aliases: list[str] | None = None,
    hidden: bool = False,
    category: str | None = None,
    group: bool = False,
    replace: bool = False,
    registry: Registry | None = None,
    **extra_metadata: Any,
) -> F:
    """Internal function to register a command."""
    reg = registry or get_command_registry()

    # Determine command name and parent from dot notation
    if name:
        parts = name.split(".")
        if len(parts) > 1:
            # Extract parent path and command name
            parent = ".".join(parts[:-1])
            command_name = parts[-1]

            # Auto-create parent groups if they don't exist (click only)
            _, has_click = _get_click()
            if has_click:
                ensure_parent_groups_fn = _get_ensure_parent_groups()
                if ensure_parent_groups_fn:
                    ensure_parent_groups_fn(parent, reg)
        else:
            parent = None
            command_name = name
    else:
        # Use function name as command name
        parent = None
        command_name = getattr(func, "__name__", "<anonymous>")

    # Check if it's already a Click command
    click_cmd = None
    click_module, has_click = _get_click()
    if has_click and isinstance(func, click_module.Command):
        click_cmd = func
        actual_func = func.callback
    else:
        actual_func = func

    # Create command info
    cmd_metadata = {"is_group": group}
    cmd_metadata.update(extra_metadata)

    info = CommandInfo(
        name=command_name,
        func=actual_func,
        description=description or (actual_func.__doc__ if actual_func else None),
        aliases=aliases or [],
        hidden=hidden,
        category=category,
        metadata=cmd_metadata,
        parent=parent,
    )

    # Build full registry key
    full_name = f"{parent}.{command_name}" if parent else command_name

    # Build registry metadata
    reg_metadata = {
        "info": info,
        "description": info.description,
        "aliases": info.aliases,
        "hidden": hidden,
        "category": category,
        "parent": parent,
        "is_group": group,
        "_prebuilt_click_command": click_cmd,  # Use new, clearer name
    }
    reg_metadata.update(extra_metadata)

    # Register in the registry
    reg.register(
        name=full_name,
        value=func,
        dimension=ComponentCategory.COMMAND.value,
        metadata=reg_metadata,
        replace=replace,
    )

    # Add metadata to the function
    func.__registry_name__ = command_name  # type: ignore[attr-defined]
    func.__registry_dimension__ = ComponentCategory.COMMAND.value  # type: ignore[attr-defined]
    func.__registry_info__ = info  # type: ignore[attr-defined]

    get_foundation_logger().trace(f"Registered command: {full_name}")

    return func


def x__register_command_func__mutmut_98(
    func: F,
    *,
    name: str | None = None,
    description: str | None = None,
    aliases: list[str] | None = None,
    hidden: bool = False,
    category: str | None = None,
    group: bool = False,
    replace: bool = False,
    registry: Registry | None = None,
    **extra_metadata: Any,
) -> F:
    """Internal function to register a command."""
    reg = registry or get_command_registry()

    # Determine command name and parent from dot notation
    if name:
        parts = name.split(".")
        if len(parts) > 1:
            # Extract parent path and command name
            parent = ".".join(parts[:-1])
            command_name = parts[-1]

            # Auto-create parent groups if they don't exist (click only)
            _, has_click = _get_click()
            if has_click:
                ensure_parent_groups_fn = _get_ensure_parent_groups()
                if ensure_parent_groups_fn:
                    ensure_parent_groups_fn(parent, reg)
        else:
            parent = None
            command_name = name
    else:
        # Use function name as command name
        parent = None
        command_name = getattr(func, "__name__", "<anonymous>")

    # Check if it's already a Click command
    click_cmd = None
    click_module, has_click = _get_click()
    if has_click and isinstance(func, click_module.Command):
        click_cmd = func
        actual_func = func.callback
    else:
        actual_func = func

    # Create command info
    cmd_metadata = {"is_group": group}
    cmd_metadata.update(extra_metadata)

    info = CommandInfo(
        name=command_name,
        func=actual_func,
        description=description or (actual_func.__doc__ if actual_func else None),
        aliases=aliases or [],
        hidden=hidden,
        category=category,
        metadata=cmd_metadata,
        parent=parent,
    )

    # Build full registry key
    full_name = f"{parent}.{command_name}" if parent else command_name

    # Build registry metadata
    reg_metadata = {
        "info": info,
        "description": info.description,
        "aliases": info.aliases,
        "hidden": hidden,
        "category": category,
        "parent": parent,
        "is_group": group,
        "_prebuilt_click_command": click_cmd,  # Use new, clearer name
    }
    reg_metadata.update(extra_metadata)

    # Register in the registry
    reg.register(
        name=full_name,
        value=func,
        dimension=ComponentCategory.COMMAND.value,
        metadata=reg_metadata,
        aliases=aliases,
    )

    # Add metadata to the function
    func.__registry_name__ = command_name  # type: ignore[attr-defined]
    func.__registry_dimension__ = ComponentCategory.COMMAND.value  # type: ignore[attr-defined]
    func.__registry_info__ = info  # type: ignore[attr-defined]

    get_foundation_logger().trace(f"Registered command: {full_name}")

    return func


def x__register_command_func__mutmut_99(
    func: F,
    *,
    name: str | None = None,
    description: str | None = None,
    aliases: list[str] | None = None,
    hidden: bool = False,
    category: str | None = None,
    group: bool = False,
    replace: bool = False,
    registry: Registry | None = None,
    **extra_metadata: Any,
) -> F:
    """Internal function to register a command."""
    reg = registry or get_command_registry()

    # Determine command name and parent from dot notation
    if name:
        parts = name.split(".")
        if len(parts) > 1:
            # Extract parent path and command name
            parent = ".".join(parts[:-1])
            command_name = parts[-1]

            # Auto-create parent groups if they don't exist (click only)
            _, has_click = _get_click()
            if has_click:
                ensure_parent_groups_fn = _get_ensure_parent_groups()
                if ensure_parent_groups_fn:
                    ensure_parent_groups_fn(parent, reg)
        else:
            parent = None
            command_name = name
    else:
        # Use function name as command name
        parent = None
        command_name = getattr(func, "__name__", "<anonymous>")

    # Check if it's already a Click command
    click_cmd = None
    click_module, has_click = _get_click()
    if has_click and isinstance(func, click_module.Command):
        click_cmd = func
        actual_func = func.callback
    else:
        actual_func = func

    # Create command info
    cmd_metadata = {"is_group": group}
    cmd_metadata.update(extra_metadata)

    info = CommandInfo(
        name=command_name,
        func=actual_func,
        description=description or (actual_func.__doc__ if actual_func else None),
        aliases=aliases or [],
        hidden=hidden,
        category=category,
        metadata=cmd_metadata,
        parent=parent,
    )

    # Build full registry key
    full_name = f"{parent}.{command_name}" if parent else command_name

    # Build registry metadata
    reg_metadata = {
        "info": info,
        "description": info.description,
        "aliases": info.aliases,
        "hidden": hidden,
        "category": category,
        "parent": parent,
        "is_group": group,
        "_prebuilt_click_command": click_cmd,  # Use new, clearer name
    }
    reg_metadata.update(extra_metadata)

    # Register in the registry
    reg.register(
        name=full_name,
        value=func,
        dimension=ComponentCategory.COMMAND.value,
        metadata=reg_metadata,
        aliases=aliases,
        replace=replace,
    )

    # Add metadata to the function
    func.__registry_name__ = None  # type: ignore[attr-defined]
    func.__registry_dimension__ = ComponentCategory.COMMAND.value  # type: ignore[attr-defined]
    func.__registry_info__ = info  # type: ignore[attr-defined]

    get_foundation_logger().trace(f"Registered command: {full_name}")

    return func


def x__register_command_func__mutmut_100(
    func: F,
    *,
    name: str | None = None,
    description: str | None = None,
    aliases: list[str] | None = None,
    hidden: bool = False,
    category: str | None = None,
    group: bool = False,
    replace: bool = False,
    registry: Registry | None = None,
    **extra_metadata: Any,
) -> F:
    """Internal function to register a command."""
    reg = registry or get_command_registry()

    # Determine command name and parent from dot notation
    if name:
        parts = name.split(".")
        if len(parts) > 1:
            # Extract parent path and command name
            parent = ".".join(parts[:-1])
            command_name = parts[-1]

            # Auto-create parent groups if they don't exist (click only)
            _, has_click = _get_click()
            if has_click:
                ensure_parent_groups_fn = _get_ensure_parent_groups()
                if ensure_parent_groups_fn:
                    ensure_parent_groups_fn(parent, reg)
        else:
            parent = None
            command_name = name
    else:
        # Use function name as command name
        parent = None
        command_name = getattr(func, "__name__", "<anonymous>")

    # Check if it's already a Click command
    click_cmd = None
    click_module, has_click = _get_click()
    if has_click and isinstance(func, click_module.Command):
        click_cmd = func
        actual_func = func.callback
    else:
        actual_func = func

    # Create command info
    cmd_metadata = {"is_group": group}
    cmd_metadata.update(extra_metadata)

    info = CommandInfo(
        name=command_name,
        func=actual_func,
        description=description or (actual_func.__doc__ if actual_func else None),
        aliases=aliases or [],
        hidden=hidden,
        category=category,
        metadata=cmd_metadata,
        parent=parent,
    )

    # Build full registry key
    full_name = f"{parent}.{command_name}" if parent else command_name

    # Build registry metadata
    reg_metadata = {
        "info": info,
        "description": info.description,
        "aliases": info.aliases,
        "hidden": hidden,
        "category": category,
        "parent": parent,
        "is_group": group,
        "_prebuilt_click_command": click_cmd,  # Use new, clearer name
    }
    reg_metadata.update(extra_metadata)

    # Register in the registry
    reg.register(
        name=full_name,
        value=func,
        dimension=ComponentCategory.COMMAND.value,
        metadata=reg_metadata,
        aliases=aliases,
        replace=replace,
    )

    # Add metadata to the function
    func.__registry_name__ = command_name  # type: ignore[attr-defined]
    func.__registry_dimension__ = None  # type: ignore[attr-defined]
    func.__registry_info__ = info  # type: ignore[attr-defined]

    get_foundation_logger().trace(f"Registered command: {full_name}")

    return func


def x__register_command_func__mutmut_101(
    func: F,
    *,
    name: str | None = None,
    description: str | None = None,
    aliases: list[str] | None = None,
    hidden: bool = False,
    category: str | None = None,
    group: bool = False,
    replace: bool = False,
    registry: Registry | None = None,
    **extra_metadata: Any,
) -> F:
    """Internal function to register a command."""
    reg = registry or get_command_registry()

    # Determine command name and parent from dot notation
    if name:
        parts = name.split(".")
        if len(parts) > 1:
            # Extract parent path and command name
            parent = ".".join(parts[:-1])
            command_name = parts[-1]

            # Auto-create parent groups if they don't exist (click only)
            _, has_click = _get_click()
            if has_click:
                ensure_parent_groups_fn = _get_ensure_parent_groups()
                if ensure_parent_groups_fn:
                    ensure_parent_groups_fn(parent, reg)
        else:
            parent = None
            command_name = name
    else:
        # Use function name as command name
        parent = None
        command_name = getattr(func, "__name__", "<anonymous>")

    # Check if it's already a Click command
    click_cmd = None
    click_module, has_click = _get_click()
    if has_click and isinstance(func, click_module.Command):
        click_cmd = func
        actual_func = func.callback
    else:
        actual_func = func

    # Create command info
    cmd_metadata = {"is_group": group}
    cmd_metadata.update(extra_metadata)

    info = CommandInfo(
        name=command_name,
        func=actual_func,
        description=description or (actual_func.__doc__ if actual_func else None),
        aliases=aliases or [],
        hidden=hidden,
        category=category,
        metadata=cmd_metadata,
        parent=parent,
    )

    # Build full registry key
    full_name = f"{parent}.{command_name}" if parent else command_name

    # Build registry metadata
    reg_metadata = {
        "info": info,
        "description": info.description,
        "aliases": info.aliases,
        "hidden": hidden,
        "category": category,
        "parent": parent,
        "is_group": group,
        "_prebuilt_click_command": click_cmd,  # Use new, clearer name
    }
    reg_metadata.update(extra_metadata)

    # Register in the registry
    reg.register(
        name=full_name,
        value=func,
        dimension=ComponentCategory.COMMAND.value,
        metadata=reg_metadata,
        aliases=aliases,
        replace=replace,
    )

    # Add metadata to the function
    func.__registry_name__ = command_name  # type: ignore[attr-defined]
    func.__registry_dimension__ = ComponentCategory.COMMAND.value  # type: ignore[attr-defined]
    func.__registry_info__ = None  # type: ignore[attr-defined]

    get_foundation_logger().trace(f"Registered command: {full_name}")

    return func


def x__register_command_func__mutmut_102(
    func: F,
    *,
    name: str | None = None,
    description: str | None = None,
    aliases: list[str] | None = None,
    hidden: bool = False,
    category: str | None = None,
    group: bool = False,
    replace: bool = False,
    registry: Registry | None = None,
    **extra_metadata: Any,
) -> F:
    """Internal function to register a command."""
    reg = registry or get_command_registry()

    # Determine command name and parent from dot notation
    if name:
        parts = name.split(".")
        if len(parts) > 1:
            # Extract parent path and command name
            parent = ".".join(parts[:-1])
            command_name = parts[-1]

            # Auto-create parent groups if they don't exist (click only)
            _, has_click = _get_click()
            if has_click:
                ensure_parent_groups_fn = _get_ensure_parent_groups()
                if ensure_parent_groups_fn:
                    ensure_parent_groups_fn(parent, reg)
        else:
            parent = None
            command_name = name
    else:
        # Use function name as command name
        parent = None
        command_name = getattr(func, "__name__", "<anonymous>")

    # Check if it's already a Click command
    click_cmd = None
    click_module, has_click = _get_click()
    if has_click and isinstance(func, click_module.Command):
        click_cmd = func
        actual_func = func.callback
    else:
        actual_func = func

    # Create command info
    cmd_metadata = {"is_group": group}
    cmd_metadata.update(extra_metadata)

    info = CommandInfo(
        name=command_name,
        func=actual_func,
        description=description or (actual_func.__doc__ if actual_func else None),
        aliases=aliases or [],
        hidden=hidden,
        category=category,
        metadata=cmd_metadata,
        parent=parent,
    )

    # Build full registry key
    full_name = f"{parent}.{command_name}" if parent else command_name

    # Build registry metadata
    reg_metadata = {
        "info": info,
        "description": info.description,
        "aliases": info.aliases,
        "hidden": hidden,
        "category": category,
        "parent": parent,
        "is_group": group,
        "_prebuilt_click_command": click_cmd,  # Use new, clearer name
    }
    reg_metadata.update(extra_metadata)

    # Register in the registry
    reg.register(
        name=full_name,
        value=func,
        dimension=ComponentCategory.COMMAND.value,
        metadata=reg_metadata,
        aliases=aliases,
        replace=replace,
    )

    # Add metadata to the function
    func.__registry_name__ = command_name  # type: ignore[attr-defined]
    func.__registry_dimension__ = ComponentCategory.COMMAND.value  # type: ignore[attr-defined]
    func.__registry_info__ = info  # type: ignore[attr-defined]

    get_foundation_logger().trace(None)

    return func


x__register_command_func__mutmut_mutants: ClassVar[MutantDict] = {
    "x__register_command_func__mutmut_1": x__register_command_func__mutmut_1,
    "x__register_command_func__mutmut_2": x__register_command_func__mutmut_2,
    "x__register_command_func__mutmut_3": x__register_command_func__mutmut_3,
    "x__register_command_func__mutmut_4": x__register_command_func__mutmut_4,
    "x__register_command_func__mutmut_5": x__register_command_func__mutmut_5,
    "x__register_command_func__mutmut_6": x__register_command_func__mutmut_6,
    "x__register_command_func__mutmut_7": x__register_command_func__mutmut_7,
    "x__register_command_func__mutmut_8": x__register_command_func__mutmut_8,
    "x__register_command_func__mutmut_9": x__register_command_func__mutmut_9,
    "x__register_command_func__mutmut_10": x__register_command_func__mutmut_10,
    "x__register_command_func__mutmut_11": x__register_command_func__mutmut_11,
    "x__register_command_func__mutmut_12": x__register_command_func__mutmut_12,
    "x__register_command_func__mutmut_13": x__register_command_func__mutmut_13,
    "x__register_command_func__mutmut_14": x__register_command_func__mutmut_14,
    "x__register_command_func__mutmut_15": x__register_command_func__mutmut_15,
    "x__register_command_func__mutmut_16": x__register_command_func__mutmut_16,
    "x__register_command_func__mutmut_17": x__register_command_func__mutmut_17,
    "x__register_command_func__mutmut_18": x__register_command_func__mutmut_18,
    "x__register_command_func__mutmut_19": x__register_command_func__mutmut_19,
    "x__register_command_func__mutmut_20": x__register_command_func__mutmut_20,
    "x__register_command_func__mutmut_21": x__register_command_func__mutmut_21,
    "x__register_command_func__mutmut_22": x__register_command_func__mutmut_22,
    "x__register_command_func__mutmut_23": x__register_command_func__mutmut_23,
    "x__register_command_func__mutmut_24": x__register_command_func__mutmut_24,
    "x__register_command_func__mutmut_25": x__register_command_func__mutmut_25,
    "x__register_command_func__mutmut_26": x__register_command_func__mutmut_26,
    "x__register_command_func__mutmut_27": x__register_command_func__mutmut_27,
    "x__register_command_func__mutmut_28": x__register_command_func__mutmut_28,
    "x__register_command_func__mutmut_29": x__register_command_func__mutmut_29,
    "x__register_command_func__mutmut_30": x__register_command_func__mutmut_30,
    "x__register_command_func__mutmut_31": x__register_command_func__mutmut_31,
    "x__register_command_func__mutmut_32": x__register_command_func__mutmut_32,
    "x__register_command_func__mutmut_33": x__register_command_func__mutmut_33,
    "x__register_command_func__mutmut_34": x__register_command_func__mutmut_34,
    "x__register_command_func__mutmut_35": x__register_command_func__mutmut_35,
    "x__register_command_func__mutmut_36": x__register_command_func__mutmut_36,
    "x__register_command_func__mutmut_37": x__register_command_func__mutmut_37,
    "x__register_command_func__mutmut_38": x__register_command_func__mutmut_38,
    "x__register_command_func__mutmut_39": x__register_command_func__mutmut_39,
    "x__register_command_func__mutmut_40": x__register_command_func__mutmut_40,
    "x__register_command_func__mutmut_41": x__register_command_func__mutmut_41,
    "x__register_command_func__mutmut_42": x__register_command_func__mutmut_42,
    "x__register_command_func__mutmut_43": x__register_command_func__mutmut_43,
    "x__register_command_func__mutmut_44": x__register_command_func__mutmut_44,
    "x__register_command_func__mutmut_45": x__register_command_func__mutmut_45,
    "x__register_command_func__mutmut_46": x__register_command_func__mutmut_46,
    "x__register_command_func__mutmut_47": x__register_command_func__mutmut_47,
    "x__register_command_func__mutmut_48": x__register_command_func__mutmut_48,
    "x__register_command_func__mutmut_49": x__register_command_func__mutmut_49,
    "x__register_command_func__mutmut_50": x__register_command_func__mutmut_50,
    "x__register_command_func__mutmut_51": x__register_command_func__mutmut_51,
    "x__register_command_func__mutmut_52": x__register_command_func__mutmut_52,
    "x__register_command_func__mutmut_53": x__register_command_func__mutmut_53,
    "x__register_command_func__mutmut_54": x__register_command_func__mutmut_54,
    "x__register_command_func__mutmut_55": x__register_command_func__mutmut_55,
    "x__register_command_func__mutmut_56": x__register_command_func__mutmut_56,
    "x__register_command_func__mutmut_57": x__register_command_func__mutmut_57,
    "x__register_command_func__mutmut_58": x__register_command_func__mutmut_58,
    "x__register_command_func__mutmut_59": x__register_command_func__mutmut_59,
    "x__register_command_func__mutmut_60": x__register_command_func__mutmut_60,
    "x__register_command_func__mutmut_61": x__register_command_func__mutmut_61,
    "x__register_command_func__mutmut_62": x__register_command_func__mutmut_62,
    "x__register_command_func__mutmut_63": x__register_command_func__mutmut_63,
    "x__register_command_func__mutmut_64": x__register_command_func__mutmut_64,
    "x__register_command_func__mutmut_65": x__register_command_func__mutmut_65,
    "x__register_command_func__mutmut_66": x__register_command_func__mutmut_66,
    "x__register_command_func__mutmut_67": x__register_command_func__mutmut_67,
    "x__register_command_func__mutmut_68": x__register_command_func__mutmut_68,
    "x__register_command_func__mutmut_69": x__register_command_func__mutmut_69,
    "x__register_command_func__mutmut_70": x__register_command_func__mutmut_70,
    "x__register_command_func__mutmut_71": x__register_command_func__mutmut_71,
    "x__register_command_func__mutmut_72": x__register_command_func__mutmut_72,
    "x__register_command_func__mutmut_73": x__register_command_func__mutmut_73,
    "x__register_command_func__mutmut_74": x__register_command_func__mutmut_74,
    "x__register_command_func__mutmut_75": x__register_command_func__mutmut_75,
    "x__register_command_func__mutmut_76": x__register_command_func__mutmut_76,
    "x__register_command_func__mutmut_77": x__register_command_func__mutmut_77,
    "x__register_command_func__mutmut_78": x__register_command_func__mutmut_78,
    "x__register_command_func__mutmut_79": x__register_command_func__mutmut_79,
    "x__register_command_func__mutmut_80": x__register_command_func__mutmut_80,
    "x__register_command_func__mutmut_81": x__register_command_func__mutmut_81,
    "x__register_command_func__mutmut_82": x__register_command_func__mutmut_82,
    "x__register_command_func__mutmut_83": x__register_command_func__mutmut_83,
    "x__register_command_func__mutmut_84": x__register_command_func__mutmut_84,
    "x__register_command_func__mutmut_85": x__register_command_func__mutmut_85,
    "x__register_command_func__mutmut_86": x__register_command_func__mutmut_86,
    "x__register_command_func__mutmut_87": x__register_command_func__mutmut_87,
    "x__register_command_func__mutmut_88": x__register_command_func__mutmut_88,
    "x__register_command_func__mutmut_89": x__register_command_func__mutmut_89,
    "x__register_command_func__mutmut_90": x__register_command_func__mutmut_90,
    "x__register_command_func__mutmut_91": x__register_command_func__mutmut_91,
    "x__register_command_func__mutmut_92": x__register_command_func__mutmut_92,
    "x__register_command_func__mutmut_93": x__register_command_func__mutmut_93,
    "x__register_command_func__mutmut_94": x__register_command_func__mutmut_94,
    "x__register_command_func__mutmut_95": x__register_command_func__mutmut_95,
    "x__register_command_func__mutmut_96": x__register_command_func__mutmut_96,
    "x__register_command_func__mutmut_97": x__register_command_func__mutmut_97,
    "x__register_command_func__mutmut_98": x__register_command_func__mutmut_98,
    "x__register_command_func__mutmut_99": x__register_command_func__mutmut_99,
    "x__register_command_func__mutmut_100": x__register_command_func__mutmut_100,
    "x__register_command_func__mutmut_101": x__register_command_func__mutmut_101,
    "x__register_command_func__mutmut_102": x__register_command_func__mutmut_102,
}


def _register_command_func(*args, **kwargs):
    result = _mutmut_trampoline(
        x__register_command_func__mutmut_orig, x__register_command_func__mutmut_mutants, args, kwargs
    )
    return result


_register_command_func.__signature__ = _mutmut_signature(x__register_command_func__mutmut_orig)
x__register_command_func__mutmut_orig.__name__ = "x__register_command_func"


# <3 🧱🤝🌐🪄
