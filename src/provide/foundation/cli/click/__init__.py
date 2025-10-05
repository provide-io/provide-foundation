"""Click CLI framework adapter.

Provides Click-specific implementation of the CLIAdapter protocol.
"""

from __future__ import annotations

from provide.foundation.cli.click.adapter import ClickAdapter
from provide.foundation.cli.click.builder import (
    build_click_command,
    create_command_group,
    ensure_parent_groups,
)

__all__ = [
    "ClickAdapter",
    "build_click_command",
    "create_command_group",
    "ensure_parent_groups",
]
