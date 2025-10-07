"""Click CLI framework adapter.

Provides Click-specific implementation of the CLIAdapter protocol.
"""

from __future__ import annotations

from provide.foundation.cli.click.adapter import ClickAdapter
from provide.foundation.cli.click.builder import create_command_group
from provide.foundation.cli.click.commands import build_click_command
from provide.foundation.cli.click.hierarchy import ensure_parent_groups

__all__ = [
    "ClickAdapter",
    "build_click_command",
    "create_command_group",
    "ensure_parent_groups",
]
