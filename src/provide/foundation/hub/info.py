"""Command information and metadata structures."""

from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any

import click


@dataclass(frozen=True, slots=True)
class CommandInfo:
    """Information about a registered command."""

    name: str
    func: Callable[..., Any]
    description: str | None = None
    aliases: list[str] = field(default_factory=list)
    hidden: bool = False
    category: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
    click_command: click.Command | None = None
    parent: str | None = None  # Parent path extracted from dot notation


__all__ = ["CommandInfo"]