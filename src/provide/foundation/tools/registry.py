#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from __future__ import annotations

import importlib.metadata
from typing import Any

from provide.foundation.config import BaseConfig
from provide.foundation.hub import get_hub
from provide.foundation.logger import get_logger
from provide.foundation.tools.base import BaseToolManager

"""Tool registry management using the foundation hub.

Provides registration and discovery of tool managers using
the main hub registry with proper dimension separation.
"""

log = get_logger(__name__)


class ToolRegistry:
    """Wrapper around the hub registry for tool management.

    Uses the main hub registry with dimension="tool_manager"
    to avoid namespace pollution while leveraging existing
    registry infrastructure.
    """

    DIMENSION = "tool_manager"

    def __init__(self) -> None:
        """Initialize the tool registry."""
        self.hub = get_hub()
        self._discover_tools()

    def _discover_tools(self) -> None:
        """Auto-discover tool managers via entry points.

        Looks for entry points in the "provide.foundation.tools" group
        and automatically registers them.
        """
        try:
            # Get entry points for tool managers (Python 3.11+)
            eps = importlib.metadata.entry_points()
            group_eps = eps.select(group="provide.foundation.tools")

            for ep in group_eps:
                try:
                    manager_class = ep.load()
                    self.register_tool_manager(ep.name, manager_class)
                    log.debug(f"Auto-discovered tool manager: {ep.name}")
                except Exception as e:
                    log.warning(f"Failed to load tool manager {ep.name}: {e}")
        except Exception as e:
            log.debug(f"Entry point discovery not available: {e}")

    def register_tool_manager(
        self,
        name: str,
        manager_class: type[BaseToolManager],
        aliases: list[str] | None = None,
    ) -> None:
        """Register a tool manager with the hub.

        Args:
            name: Tool name (e.g., "terraform").
            manager_class: Tool manager class.
            aliases: Optional aliases for the tool.

        """
        # Prepare metadata
        metadata = {
            "tool_name": manager_class.tool_name,
            "executable": manager_class.executable_name,
            "platforms": manager_class.supported_platforms,
        }

        # Register with hub
        self.hub._component_registry.register(
            name=name,
            value=manager_class,
            dimension=self.DIMENSION,
            metadata=metadata,
            aliases=aliases,
            replace=True,  # Allow re-registration for updates
        )

        log.info(f"Registered tool manager: {name}")

    def get_tool_manager_class(self, name: str) -> type[BaseToolManager] | None:
        """Get a tool manager class by name.

        Args:
            name: Tool name or alias.

        Returns:
            Tool manager class, or None if not found.

        """
        return self.hub._component_registry.get(name, dimension=self.DIMENSION)

    def create_tool_manager(self, name: str, config: BaseConfig) -> BaseToolManager | None:
        """Create a tool manager instance.

        Args:
            name: Tool name or alias.
            config: Configuration object.

        Returns:
            Tool manager instance, or None if not found.

        """
        manager_class = self.get_tool_manager_class(name)
        if manager_class:
            return manager_class(config)
        return None

    def list_tools(self) -> list[tuple[str, dict[str, Any]]]:
        """List all registered tools.

        Returns:
            List of (name, metadata) tuples.

        """
        tools = []
        dimension_list = self.hub._component_registry.list_dimension(self.DIMENSION)
        for item in dimension_list:
            name, entry = item  # type: ignore[misc]
            metadata = entry.metadata if hasattr(entry, "metadata") else {}  # type: ignore[has-type]
            tools.append((name, metadata))  # type: ignore[has-type]
        return tools

    def get_tool_info(self, name: str) -> dict[str, Any] | None:
        """Get information about a specific tool.

        Args:
            name: Tool name or alias.

        Returns:
            Tool metadata dictionary, or None if not found.

        """
        entry = self.hub._component_registry.get_entry(name, dimension=self.DIMENSION)
        if entry and hasattr(entry, "metadata"):
            return entry.metadata
        return None

    def is_tool_registered(self, name: str) -> bool:
        """Check if a tool is registered.

        Args:
            name: Tool name or alias.

        Returns:
            True if registered, False otherwise.

        """
        return self.get_tool_manager_class(name) is not None


# Global registry instance
_tool_registry: ToolRegistry | None = None


def get_tool_registry() -> ToolRegistry:
    """Get the global tool registry instance.

    Returns:
        Tool registry instance.

    """
    global _tool_registry
    if _tool_registry is None:
        _tool_registry = ToolRegistry()
    return _tool_registry


def register_tool_manager(
    name: str,
    manager_class: type[BaseToolManager],
    aliases: list[str] | None = None,
) -> None:
    """Register a tool manager with the global registry.

    Args:
        name: Tool name.
        manager_class: Tool manager class.
        aliases: Optional aliases.

    """
    registry = get_tool_registry()
    registry.register_tool_manager(name, manager_class, aliases)


def get_tool_manager(name: str, config: BaseConfig) -> BaseToolManager | None:
    """Get a tool manager instance from the global registry.

    Args:
        name: Tool name or alias.
        config: Configuration object.

    Returns:
        Tool manager instance, or None if not found.

    """
    registry = get_tool_registry()
    return registry.create_tool_manager(name, config)


# 🧱🏗️🔚
