"""Command registration and management for the hub.

This module now re-exports from the split modules for backward compatibility.
"""

from __future__ import annotations

from typing import Any

# Core hub features (always available)
from provide.foundation.hub.decorators import register_command
from provide.foundation.hub.info import CommandInfo
from provide.foundation.hub.registry import get_command_registry


# CLI features (require click) - lazy loaded
def __getattr__(name: str) -> Any:
    """Support lazy loading of CLI-dependent features."""
    if name in ("build_click_command", "create_command_group"):
        try:
            from provide.foundation.hub.click_builder import (
                build_click_command,
                create_command_group,
            )

            if name == "build_click_command":
                return build_click_command
            if name == "create_command_group":
                return create_command_group
        except ImportError as e:
            if "click" in str(e):
                raise ImportError(
                    f"CLI feature '{name}' requires: pip install 'provide-foundation[cli]'",
                ) from e
            raise
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")


__all__ = [
    "CommandInfo",
    "build_click_command",  # noqa: F822
    "create_command_group",  # noqa: F822
    "get_command_registry",
    "register_command",
]
