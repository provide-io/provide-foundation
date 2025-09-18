"""Command information and metadata structures."""

from __future__ import annotations

from collections.abc import Callable
from types import ModuleType
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    pass

from attrs import define, field

try:
    import click

    _HAS_CLICK = True
    _click_module: ModuleType | None = click
except ImportError:
    _HAS_CLICK = False
    _click_module = None


@define(frozen=True, slots=True)
class CommandInfo:
    """Information about a registered command."""

    name: str
    func: Callable[..., Any]
    description: str | None = None
    aliases: list[str] = field(factory=list)
    hidden: bool = False
    category: str | None = None
    metadata: dict[str, Any] = field(factory=dict)
    click_command: click.Command | None = None
    parent: str | None = None  # Parent path extracted from dot notation


__all__ = ["CommandInfo"]
