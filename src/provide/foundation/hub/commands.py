"""Command registration and management for the hub.

This module re-exports from the split modules for convenience.
"""

from __future__ import annotations

from typing import Any

# Core hub features (always available)
from provide.foundation.hub.decorators import register_command
from provide.foundation.hub.info import CommandInfo
from provide.foundation.hub.registry import get_command_registry

# CLI features (require click) - Pattern 2: stub functions with helpful errors
try:
    from provide.foundation.cli.click.builder import (
        build_click_command,
        create_command_group,
    )

    _HAS_CLICK = True
except ImportError:
    _HAS_CLICK = False

    def build_click_command(*args: Any, **kwargs: Any) -> Any:
        raise ImportError("CLI feature 'build_click_command' requires: pip install 'provide-foundation[cli]'")

    def create_command_group(*args: Any, **kwargs: Any) -> Any:
        raise ImportError("CLI feature 'create_command_group' requires: pip install 'provide-foundation[cli]'")


__all__ = [
    "CommandInfo",
    "build_click_command",
    "create_command_group",
    "get_command_registry",
    "register_command",
]
