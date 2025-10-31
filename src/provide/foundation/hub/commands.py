#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Command registration and management for the hub.

This module re-exports from the split modules for convenience."""

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


def _check_click() -> bool:
    """Check if click is available (cached)."""
    global _HAS_CLICK
    if _HAS_CLICK is None:
        try:
            import click  # noqa: F401

            _HAS_CLICK = True
        except ImportError:
            _HAS_CLICK = False
    return _HAS_CLICK


# Pattern 2: Stub functions that import on first call (avoids circular import)
def create_command_group(
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


__all__ = [
    "CommandInfo",
    "create_command_group",
    "get_command_registry",
    "register_command",
]

# 🧱🏗️🔚
