"""Command information and metadata structures."""

from collections.abc import Callable
from typing import Any

from attrs import define, field

try:
    import click

    _HAS_CLICK = True
except ImportError:
    click = None
    _HAS_CLICK = False


@define(frozen=True, slots=True)
class CommandInfo:
    """Information about a registered command."""

    name: str
    func: Callable[..., Any]
    description: str | None = None
    aliases: list[str] = field(factory=lambda: [])
    hidden: bool = False
    category: str | None = None
    metadata: dict[str, Any] = field(factory=lambda: {})
    click_command: "click.Command | None" = None
    parent: str | None = None  # Parent path extracted from dot notation


__all__ = ["CommandInfo"]
