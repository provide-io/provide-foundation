# provide/foundation/hub/commands.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

"""Command registration and management for the hub.

This module re-exports from the split modules for convenience.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

# Core hub features (always available)
from provide.foundation.hub.decorators import register_command
from provide.foundation.hub.info import CommandInfo
from provide.foundation.hub.registry import get_command_registry

# Delay CLI imports to avoid circular dependency (cli.click.builder imports hub.registry)
if TYPE_CHECKING:
    pass

# Pattern 1: Check for click at runtime (delayed to avoid circular import)
_HAS_CLICK: bool | None = None
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


def x__check_click__mutmut_orig() -> bool:
    """Check if click is available (cached)."""
    global _HAS_CLICK
    if _HAS_CLICK is None:
        try:
            import click  # noqa: F401

            _HAS_CLICK = True
        except ImportError:
            _HAS_CLICK = False
    return _HAS_CLICK


def x__check_click__mutmut_1() -> bool:
    """Check if click is available (cached)."""
    global _HAS_CLICK
    if _HAS_CLICK is not None:
        try:
            import click  # noqa: F401

            _HAS_CLICK = True
        except ImportError:
            _HAS_CLICK = False
    return _HAS_CLICK


def x__check_click__mutmut_2() -> bool:
    """Check if click is available (cached)."""
    global _HAS_CLICK
    if _HAS_CLICK is None:
        try:
            import click  # noqa: F401

            _HAS_CLICK = None
        except ImportError:
            _HAS_CLICK = False
    return _HAS_CLICK


def x__check_click__mutmut_3() -> bool:
    """Check if click is available (cached)."""
    global _HAS_CLICK
    if _HAS_CLICK is None:
        try:
            import click  # noqa: F401

            _HAS_CLICK = False
        except ImportError:
            _HAS_CLICK = False
    return _HAS_CLICK


def x__check_click__mutmut_4() -> bool:
    """Check if click is available (cached)."""
    global _HAS_CLICK
    if _HAS_CLICK is None:
        try:
            import click  # noqa: F401

            _HAS_CLICK = True
        except ImportError:
            _HAS_CLICK = None
    return _HAS_CLICK


def x__check_click__mutmut_5() -> bool:
    """Check if click is available (cached)."""
    global _HAS_CLICK
    if _HAS_CLICK is None:
        try:
            import click  # noqa: F401

            _HAS_CLICK = True
        except ImportError:
            _HAS_CLICK = True
    return _HAS_CLICK

x__check_click__mutmut_mutants : ClassVar[MutantDict] = {
'x__check_click__mutmut_1': x__check_click__mutmut_1, 
    'x__check_click__mutmut_2': x__check_click__mutmut_2, 
    'x__check_click__mutmut_3': x__check_click__mutmut_3, 
    'x__check_click__mutmut_4': x__check_click__mutmut_4, 
    'x__check_click__mutmut_5': x__check_click__mutmut_5
}

def _check_click(*args, **kwargs):
    result = _mutmut_trampoline(x__check_click__mutmut_orig, x__check_click__mutmut_mutants, args, kwargs)
    return result 

_check_click.__signature__ = _mutmut_signature(x__check_click__mutmut_orig)
x__check_click__mutmut_orig.__name__ = 'x__check_click'


# Pattern 2: Stub functions that import on first call (avoids circular import)
def x_create_command_group__mutmut_orig(
    name: str = "cli",
    commands: list[str] | None = None,
    registry: Any = None,
    **kwargs: Any,
) -> Any:
    """Create command group (imports on first call to avoid circular import)."""
    if not _check_click():
        raise ImportError("CLI feature 'create_command_group' requires: pip install 'provide-foundation[cli]'")
    from provide.foundation.cli.click.builder import create_command_group as real_func

    return real_func(name, commands, registry, **kwargs)


# Pattern 2: Stub functions that import on first call (avoids circular import)
def x_create_command_group__mutmut_1(
    name: str = "XXcliXX",
    commands: list[str] | None = None,
    registry: Any = None,
    **kwargs: Any,
) -> Any:
    """Create command group (imports on first call to avoid circular import)."""
    if not _check_click():
        raise ImportError("CLI feature 'create_command_group' requires: pip install 'provide-foundation[cli]'")
    from provide.foundation.cli.click.builder import create_command_group as real_func

    return real_func(name, commands, registry, **kwargs)


# Pattern 2: Stub functions that import on first call (avoids circular import)
def x_create_command_group__mutmut_2(
    name: str = "CLI",
    commands: list[str] | None = None,
    registry: Any = None,
    **kwargs: Any,
) -> Any:
    """Create command group (imports on first call to avoid circular import)."""
    if not _check_click():
        raise ImportError("CLI feature 'create_command_group' requires: pip install 'provide-foundation[cli]'")
    from provide.foundation.cli.click.builder import create_command_group as real_func

    return real_func(name, commands, registry, **kwargs)


# Pattern 2: Stub functions that import on first call (avoids circular import)
def x_create_command_group__mutmut_3(
    name: str = "cli",
    commands: list[str] | None = None,
    registry: Any = None,
    **kwargs: Any,
) -> Any:
    """Create command group (imports on first call to avoid circular import)."""
    if _check_click():
        raise ImportError("CLI feature 'create_command_group' requires: pip install 'provide-foundation[cli]'")
    from provide.foundation.cli.click.builder import create_command_group as real_func

    return real_func(name, commands, registry, **kwargs)


# Pattern 2: Stub functions that import on first call (avoids circular import)
def x_create_command_group__mutmut_4(
    name: str = "cli",
    commands: list[str] | None = None,
    registry: Any = None,
    **kwargs: Any,
) -> Any:
    """Create command group (imports on first call to avoid circular import)."""
    if not _check_click():
        raise ImportError(None)
    from provide.foundation.cli.click.builder import create_command_group as real_func

    return real_func(name, commands, registry, **kwargs)


# Pattern 2: Stub functions that import on first call (avoids circular import)
def x_create_command_group__mutmut_5(
    name: str = "cli",
    commands: list[str] | None = None,
    registry: Any = None,
    **kwargs: Any,
) -> Any:
    """Create command group (imports on first call to avoid circular import)."""
    if not _check_click():
        raise ImportError("XXCLI feature 'create_command_group' requires: pip install 'provide-foundation[cli]'XX")
    from provide.foundation.cli.click.builder import create_command_group as real_func

    return real_func(name, commands, registry, **kwargs)


# Pattern 2: Stub functions that import on first call (avoids circular import)
def x_create_command_group__mutmut_6(
    name: str = "cli",
    commands: list[str] | None = None,
    registry: Any = None,
    **kwargs: Any,
) -> Any:
    """Create command group (imports on first call to avoid circular import)."""
    if not _check_click():
        raise ImportError("cli feature 'create_command_group' requires: pip install 'provide-foundation[cli]'")
    from provide.foundation.cli.click.builder import create_command_group as real_func

    return real_func(name, commands, registry, **kwargs)


# Pattern 2: Stub functions that import on first call (avoids circular import)
def x_create_command_group__mutmut_7(
    name: str = "cli",
    commands: list[str] | None = None,
    registry: Any = None,
    **kwargs: Any,
) -> Any:
    """Create command group (imports on first call to avoid circular import)."""
    if not _check_click():
        raise ImportError("CLI FEATURE 'CREATE_COMMAND_GROUP' REQUIRES: PIP INSTALL 'PROVIDE-FOUNDATION[CLI]'")
    from provide.foundation.cli.click.builder import create_command_group as real_func

    return real_func(name, commands, registry, **kwargs)


# Pattern 2: Stub functions that import on first call (avoids circular import)
def x_create_command_group__mutmut_8(
    name: str = "cli",
    commands: list[str] | None = None,
    registry: Any = None,
    **kwargs: Any,
) -> Any:
    """Create command group (imports on first call to avoid circular import)."""
    if not _check_click():
        raise ImportError("CLI feature 'create_command_group' requires: pip install 'provide-foundation[cli]'")
    from provide.foundation.cli.click.builder import create_command_group as real_func

    return real_func(None, commands, registry, **kwargs)


# Pattern 2: Stub functions that import on first call (avoids circular import)
def x_create_command_group__mutmut_9(
    name: str = "cli",
    commands: list[str] | None = None,
    registry: Any = None,
    **kwargs: Any,
) -> Any:
    """Create command group (imports on first call to avoid circular import)."""
    if not _check_click():
        raise ImportError("CLI feature 'create_command_group' requires: pip install 'provide-foundation[cli]'")
    from provide.foundation.cli.click.builder import create_command_group as real_func

    return real_func(name, None, registry, **kwargs)


# Pattern 2: Stub functions that import on first call (avoids circular import)
def x_create_command_group__mutmut_10(
    name: str = "cli",
    commands: list[str] | None = None,
    registry: Any = None,
    **kwargs: Any,
) -> Any:
    """Create command group (imports on first call to avoid circular import)."""
    if not _check_click():
        raise ImportError("CLI feature 'create_command_group' requires: pip install 'provide-foundation[cli]'")
    from provide.foundation.cli.click.builder import create_command_group as real_func

    return real_func(name, commands, None, **kwargs)


# Pattern 2: Stub functions that import on first call (avoids circular import)
def x_create_command_group__mutmut_11(
    name: str = "cli",
    commands: list[str] | None = None,
    registry: Any = None,
    **kwargs: Any,
) -> Any:
    """Create command group (imports on first call to avoid circular import)."""
    if not _check_click():
        raise ImportError("CLI feature 'create_command_group' requires: pip install 'provide-foundation[cli]'")
    from provide.foundation.cli.click.builder import create_command_group as real_func

    return real_func(commands, registry, **kwargs)


# Pattern 2: Stub functions that import on first call (avoids circular import)
def x_create_command_group__mutmut_12(
    name: str = "cli",
    commands: list[str] | None = None,
    registry: Any = None,
    **kwargs: Any,
) -> Any:
    """Create command group (imports on first call to avoid circular import)."""
    if not _check_click():
        raise ImportError("CLI feature 'create_command_group' requires: pip install 'provide-foundation[cli]'")
    from provide.foundation.cli.click.builder import create_command_group as real_func

    return real_func(name, registry, **kwargs)


# Pattern 2: Stub functions that import on first call (avoids circular import)
def x_create_command_group__mutmut_13(
    name: str = "cli",
    commands: list[str] | None = None,
    registry: Any = None,
    **kwargs: Any,
) -> Any:
    """Create command group (imports on first call to avoid circular import)."""
    if not _check_click():
        raise ImportError("CLI feature 'create_command_group' requires: pip install 'provide-foundation[cli]'")
    from provide.foundation.cli.click.builder import create_command_group as real_func

    return real_func(name, commands, **kwargs)


# Pattern 2: Stub functions that import on first call (avoids circular import)
def x_create_command_group__mutmut_14(
    name: str = "cli",
    commands: list[str] | None = None,
    registry: Any = None,
    **kwargs: Any,
) -> Any:
    """Create command group (imports on first call to avoid circular import)."""
    if not _check_click():
        raise ImportError("CLI feature 'create_command_group' requires: pip install 'provide-foundation[cli]'")
    from provide.foundation.cli.click.builder import create_command_group as real_func

    return real_func(name, commands, registry, )

x_create_command_group__mutmut_mutants : ClassVar[MutantDict] = {
'x_create_command_group__mutmut_1': x_create_command_group__mutmut_1, 
    'x_create_command_group__mutmut_2': x_create_command_group__mutmut_2, 
    'x_create_command_group__mutmut_3': x_create_command_group__mutmut_3, 
    'x_create_command_group__mutmut_4': x_create_command_group__mutmut_4, 
    'x_create_command_group__mutmut_5': x_create_command_group__mutmut_5, 
    'x_create_command_group__mutmut_6': x_create_command_group__mutmut_6, 
    'x_create_command_group__mutmut_7': x_create_command_group__mutmut_7, 
    'x_create_command_group__mutmut_8': x_create_command_group__mutmut_8, 
    'x_create_command_group__mutmut_9': x_create_command_group__mutmut_9, 
    'x_create_command_group__mutmut_10': x_create_command_group__mutmut_10, 
    'x_create_command_group__mutmut_11': x_create_command_group__mutmut_11, 
    'x_create_command_group__mutmut_12': x_create_command_group__mutmut_12, 
    'x_create_command_group__mutmut_13': x_create_command_group__mutmut_13, 
    'x_create_command_group__mutmut_14': x_create_command_group__mutmut_14
}

def create_command_group(*args, **kwargs):
    result = _mutmut_trampoline(x_create_command_group__mutmut_orig, x_create_command_group__mutmut_mutants, args, kwargs)
    return result 

create_command_group.__signature__ = _mutmut_signature(x_create_command_group__mutmut_orig)
x_create_command_group__mutmut_orig.__name__ = 'x_create_command_group'


__all__ = [
    "CommandInfo",
    "create_command_group",
    "get_command_registry",
    "register_command",
]


# <3 🧱🤝🌐🪄
