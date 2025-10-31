#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Command information and metadata structures."""

from __future__ import annotations

from collections.abc import Callable
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from provide.foundation.hub.introspection import ParameterInfo

from attrs import define, field

__all__ = ["CommandInfo"]


@define(frozen=True, slots=True)
class CommandInfo:
    """Framework-agnostic command information.

    Stores metadata about a registered command without framework-specific
    dependencies. The parameters field contains introspected parameter
    information that can be used by any CLI adapter.

    Attributes:
        name: Command name
        func: Command function/callable
        description: Command description (help text)
        aliases: Alternative names for the command
        hidden: Whether command is hidden from help
        category: Command category for organization
        metadata: Additional custom metadata
        parent: Parent command path (for nested commands)
        parameters: Introspected parameter information (lazy-loaded)

    """

    name: str
    func: Callable[..., Any]
    description: str | None = None
    aliases: list[str] = field(factory=list)
    hidden: bool = False
    category: str | None = None
    metadata: dict[str, Any] = field(factory=dict)
    parent: str | None = None  # Parent path extracted from dot notation
    parameters: list[ParameterInfo] | None = None


# 🧱🏗️🔚
