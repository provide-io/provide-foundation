"""
Command registration and management for the hub.

This module now re-exports from the split modules for backward compatibility.
"""

# Re-export from new modules
from provide.foundation.hub.click_builder import (
    build_click_command,
    create_command_group,
)
from provide.foundation.hub.decorators import register_command
from provide.foundation.hub.info import CommandInfo
from provide.foundation.hub.registry import get_command_registry

__all__ = [
    "CommandInfo",
    "register_command",
    "build_click_command",
    "create_command_group",
    "get_command_registry",
]