# provide/foundation/tools/registry.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

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
from inspect import signature as _mutmut_signature
from typing import Annotated
from typing import Callable
from typing import ClassVar


MutantDict = Annotated[dict[str, Callable], "Mutant"]


def _mutmut_trampoline(orig, mutants, call_args, call_kwargs, self_arg = None):
    """Forward call to original or mutated function, depending on the environment"""
    import os
    mutant_under_test = os.environ['MUTANT_UNDER_TEST']
    if mutant_under_test == 'fail':
        from mutmut.__main__ import MutmutProgrammaticFailException
        raise MutmutProgrammaticFailException('Failed programmatically')      
    elif mutant_under_test == 'stats':
        from mutmut.__main__ import record_trampoline_hit
        record_trampoline_hit(orig.__module__ + '.' + orig.__name__)
        result = orig(*call_args, **call_kwargs)
        return result
    prefix = orig.__module__ + '.' + orig.__name__ + '__mutmut_'
    if not mutant_under_test.startswith(prefix):
        result = orig(*call_args, **call_kwargs)
        return result
    mutant_name = mutant_under_test.rpartition('.')[-1]
    if self_arg:
        # call to a class method where self is not bound
        result = mutants[mutant_name](self_arg, *call_args, **call_kwargs)
    else:
        result = mutants[mutant_name](*call_args, **call_kwargs)
    return result


class ToolRegistry:
    """Wrapper around the hub registry for tool management.

    Uses the main hub registry with dimension="tool_manager"
    to avoid namespace pollution while leveraging existing
    registry infrastructure.
    """

    DIMENSION = "tool_manager"

    def xǁToolRegistryǁ__init____mutmut_orig(self) -> None:
        """Initialize the tool registry."""
        self.hub = get_hub()
        self._discover_tools()

    def xǁToolRegistryǁ__init____mutmut_1(self) -> None:
        """Initialize the tool registry."""
        self.hub = None
        self._discover_tools()
    
    xǁToolRegistryǁ__init____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁToolRegistryǁ__init____mutmut_1': xǁToolRegistryǁ__init____mutmut_1
    }
    
    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁToolRegistryǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁToolRegistryǁ__init____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __init__.__signature__ = _mutmut_signature(xǁToolRegistryǁ__init____mutmut_orig)
    xǁToolRegistryǁ__init____mutmut_orig.__name__ = 'xǁToolRegistryǁ__init__'

    def xǁToolRegistryǁ_discover_tools__mutmut_orig(self) -> None:
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

    def xǁToolRegistryǁ_discover_tools__mutmut_1(self) -> None:
        """Auto-discover tool managers via entry points.

        Looks for entry points in the "provide.foundation.tools" group
        and automatically registers them.
        """
        try:
            # Get entry points for tool managers (Python 3.11+)
            eps = None
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

    def xǁToolRegistryǁ_discover_tools__mutmut_2(self) -> None:
        """Auto-discover tool managers via entry points.

        Looks for entry points in the "provide.foundation.tools" group
        and automatically registers them.
        """
        try:
            # Get entry points for tool managers (Python 3.11+)
            eps = importlib.metadata.entry_points()
            group_eps = None

            for ep in group_eps:
                try:
                    manager_class = ep.load()
                    self.register_tool_manager(ep.name, manager_class)
                    log.debug(f"Auto-discovered tool manager: {ep.name}")
                except Exception as e:
                    log.warning(f"Failed to load tool manager {ep.name}: {e}")
        except Exception as e:
            log.debug(f"Entry point discovery not available: {e}")

    def xǁToolRegistryǁ_discover_tools__mutmut_3(self) -> None:
        """Auto-discover tool managers via entry points.

        Looks for entry points in the "provide.foundation.tools" group
        and automatically registers them.
        """
        try:
            # Get entry points for tool managers (Python 3.11+)
            eps = importlib.metadata.entry_points()
            group_eps = eps.select(group=None)

            for ep in group_eps:
                try:
                    manager_class = ep.load()
                    self.register_tool_manager(ep.name, manager_class)
                    log.debug(f"Auto-discovered tool manager: {ep.name}")
                except Exception as e:
                    log.warning(f"Failed to load tool manager {ep.name}: {e}")
        except Exception as e:
            log.debug(f"Entry point discovery not available: {e}")

    def xǁToolRegistryǁ_discover_tools__mutmut_4(self) -> None:
        """Auto-discover tool managers via entry points.

        Looks for entry points in the "provide.foundation.tools" group
        and automatically registers them.
        """
        try:
            # Get entry points for tool managers (Python 3.11+)
            eps = importlib.metadata.entry_points()
            group_eps = eps.select(group="XXprovide.foundation.toolsXX")

            for ep in group_eps:
                try:
                    manager_class = ep.load()
                    self.register_tool_manager(ep.name, manager_class)
                    log.debug(f"Auto-discovered tool manager: {ep.name}")
                except Exception as e:
                    log.warning(f"Failed to load tool manager {ep.name}: {e}")
        except Exception as e:
            log.debug(f"Entry point discovery not available: {e}")

    def xǁToolRegistryǁ_discover_tools__mutmut_5(self) -> None:
        """Auto-discover tool managers via entry points.

        Looks for entry points in the "provide.foundation.tools" group
        and automatically registers them.
        """
        try:
            # Get entry points for tool managers (Python 3.11+)
            eps = importlib.metadata.entry_points()
            group_eps = eps.select(group="PROVIDE.FOUNDATION.TOOLS")

            for ep in group_eps:
                try:
                    manager_class = ep.load()
                    self.register_tool_manager(ep.name, manager_class)
                    log.debug(f"Auto-discovered tool manager: {ep.name}")
                except Exception as e:
                    log.warning(f"Failed to load tool manager {ep.name}: {e}")
        except Exception as e:
            log.debug(f"Entry point discovery not available: {e}")

    def xǁToolRegistryǁ_discover_tools__mutmut_6(self) -> None:
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
                    manager_class = None
                    self.register_tool_manager(ep.name, manager_class)
                    log.debug(f"Auto-discovered tool manager: {ep.name}")
                except Exception as e:
                    log.warning(f"Failed to load tool manager {ep.name}: {e}")
        except Exception as e:
            log.debug(f"Entry point discovery not available: {e}")

    def xǁToolRegistryǁ_discover_tools__mutmut_7(self) -> None:
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
                    self.register_tool_manager(None, manager_class)
                    log.debug(f"Auto-discovered tool manager: {ep.name}")
                except Exception as e:
                    log.warning(f"Failed to load tool manager {ep.name}: {e}")
        except Exception as e:
            log.debug(f"Entry point discovery not available: {e}")

    def xǁToolRegistryǁ_discover_tools__mutmut_8(self) -> None:
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
                    self.register_tool_manager(ep.name, None)
                    log.debug(f"Auto-discovered tool manager: {ep.name}")
                except Exception as e:
                    log.warning(f"Failed to load tool manager {ep.name}: {e}")
        except Exception as e:
            log.debug(f"Entry point discovery not available: {e}")

    def xǁToolRegistryǁ_discover_tools__mutmut_9(self) -> None:
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
                    self.register_tool_manager(manager_class)
                    log.debug(f"Auto-discovered tool manager: {ep.name}")
                except Exception as e:
                    log.warning(f"Failed to load tool manager {ep.name}: {e}")
        except Exception as e:
            log.debug(f"Entry point discovery not available: {e}")

    def xǁToolRegistryǁ_discover_tools__mutmut_10(self) -> None:
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
                    self.register_tool_manager(ep.name, )
                    log.debug(f"Auto-discovered tool manager: {ep.name}")
                except Exception as e:
                    log.warning(f"Failed to load tool manager {ep.name}: {e}")
        except Exception as e:
            log.debug(f"Entry point discovery not available: {e}")

    def xǁToolRegistryǁ_discover_tools__mutmut_11(self) -> None:
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
                    log.debug(None)
                except Exception as e:
                    log.warning(f"Failed to load tool manager {ep.name}: {e}")
        except Exception as e:
            log.debug(f"Entry point discovery not available: {e}")

    def xǁToolRegistryǁ_discover_tools__mutmut_12(self) -> None:
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
                    log.warning(None)
        except Exception as e:
            log.debug(f"Entry point discovery not available: {e}")

    def xǁToolRegistryǁ_discover_tools__mutmut_13(self) -> None:
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
            log.debug(None)
    
    xǁToolRegistryǁ_discover_tools__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁToolRegistryǁ_discover_tools__mutmut_1': xǁToolRegistryǁ_discover_tools__mutmut_1, 
        'xǁToolRegistryǁ_discover_tools__mutmut_2': xǁToolRegistryǁ_discover_tools__mutmut_2, 
        'xǁToolRegistryǁ_discover_tools__mutmut_3': xǁToolRegistryǁ_discover_tools__mutmut_3, 
        'xǁToolRegistryǁ_discover_tools__mutmut_4': xǁToolRegistryǁ_discover_tools__mutmut_4, 
        'xǁToolRegistryǁ_discover_tools__mutmut_5': xǁToolRegistryǁ_discover_tools__mutmut_5, 
        'xǁToolRegistryǁ_discover_tools__mutmut_6': xǁToolRegistryǁ_discover_tools__mutmut_6, 
        'xǁToolRegistryǁ_discover_tools__mutmut_7': xǁToolRegistryǁ_discover_tools__mutmut_7, 
        'xǁToolRegistryǁ_discover_tools__mutmut_8': xǁToolRegistryǁ_discover_tools__mutmut_8, 
        'xǁToolRegistryǁ_discover_tools__mutmut_9': xǁToolRegistryǁ_discover_tools__mutmut_9, 
        'xǁToolRegistryǁ_discover_tools__mutmut_10': xǁToolRegistryǁ_discover_tools__mutmut_10, 
        'xǁToolRegistryǁ_discover_tools__mutmut_11': xǁToolRegistryǁ_discover_tools__mutmut_11, 
        'xǁToolRegistryǁ_discover_tools__mutmut_12': xǁToolRegistryǁ_discover_tools__mutmut_12, 
        'xǁToolRegistryǁ_discover_tools__mutmut_13': xǁToolRegistryǁ_discover_tools__mutmut_13
    }
    
    def _discover_tools(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁToolRegistryǁ_discover_tools__mutmut_orig"), object.__getattribute__(self, "xǁToolRegistryǁ_discover_tools__mutmut_mutants"), args, kwargs, self)
        return result 
    
    _discover_tools.__signature__ = _mutmut_signature(xǁToolRegistryǁ_discover_tools__mutmut_orig)
    xǁToolRegistryǁ_discover_tools__mutmut_orig.__name__ = 'xǁToolRegistryǁ_discover_tools'

    def xǁToolRegistryǁregister_tool_manager__mutmut_orig(
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

    def xǁToolRegistryǁregister_tool_manager__mutmut_1(
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
        metadata = None

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

    def xǁToolRegistryǁregister_tool_manager__mutmut_2(
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
            "XXtool_nameXX": manager_class.tool_name,
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

    def xǁToolRegistryǁregister_tool_manager__mutmut_3(
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
            "TOOL_NAME": manager_class.tool_name,
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

    def xǁToolRegistryǁregister_tool_manager__mutmut_4(
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
            "XXexecutableXX": manager_class.executable_name,
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

    def xǁToolRegistryǁregister_tool_manager__mutmut_5(
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
            "EXECUTABLE": manager_class.executable_name,
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

    def xǁToolRegistryǁregister_tool_manager__mutmut_6(
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
            "XXplatformsXX": manager_class.supported_platforms,
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

    def xǁToolRegistryǁregister_tool_manager__mutmut_7(
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
            "PLATFORMS": manager_class.supported_platforms,
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

    def xǁToolRegistryǁregister_tool_manager__mutmut_8(
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
            name=None,
            value=manager_class,
            dimension=self.DIMENSION,
            metadata=metadata,
            aliases=aliases,
            replace=True,  # Allow re-registration for updates
        )

        log.info(f"Registered tool manager: {name}")

    def xǁToolRegistryǁregister_tool_manager__mutmut_9(
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
            value=None,
            dimension=self.DIMENSION,
            metadata=metadata,
            aliases=aliases,
            replace=True,  # Allow re-registration for updates
        )

        log.info(f"Registered tool manager: {name}")

    def xǁToolRegistryǁregister_tool_manager__mutmut_10(
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
            dimension=None,
            metadata=metadata,
            aliases=aliases,
            replace=True,  # Allow re-registration for updates
        )

        log.info(f"Registered tool manager: {name}")

    def xǁToolRegistryǁregister_tool_manager__mutmut_11(
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
            metadata=None,
            aliases=aliases,
            replace=True,  # Allow re-registration for updates
        )

        log.info(f"Registered tool manager: {name}")

    def xǁToolRegistryǁregister_tool_manager__mutmut_12(
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
            aliases=None,
            replace=True,  # Allow re-registration for updates
        )

        log.info(f"Registered tool manager: {name}")

    def xǁToolRegistryǁregister_tool_manager__mutmut_13(
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
            replace=None,  # Allow re-registration for updates
        )

        log.info(f"Registered tool manager: {name}")

    def xǁToolRegistryǁregister_tool_manager__mutmut_14(
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
            value=manager_class,
            dimension=self.DIMENSION,
            metadata=metadata,
            aliases=aliases,
            replace=True,  # Allow re-registration for updates
        )

        log.info(f"Registered tool manager: {name}")

    def xǁToolRegistryǁregister_tool_manager__mutmut_15(
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
            dimension=self.DIMENSION,
            metadata=metadata,
            aliases=aliases,
            replace=True,  # Allow re-registration for updates
        )

        log.info(f"Registered tool manager: {name}")

    def xǁToolRegistryǁregister_tool_manager__mutmut_16(
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
            metadata=metadata,
            aliases=aliases,
            replace=True,  # Allow re-registration for updates
        )

        log.info(f"Registered tool manager: {name}")

    def xǁToolRegistryǁregister_tool_manager__mutmut_17(
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
            aliases=aliases,
            replace=True,  # Allow re-registration for updates
        )

        log.info(f"Registered tool manager: {name}")

    def xǁToolRegistryǁregister_tool_manager__mutmut_18(
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
            replace=True,  # Allow re-registration for updates
        )

        log.info(f"Registered tool manager: {name}")

    def xǁToolRegistryǁregister_tool_manager__mutmut_19(
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
            )

        log.info(f"Registered tool manager: {name}")

    def xǁToolRegistryǁregister_tool_manager__mutmut_20(
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
            replace=False,  # Allow re-registration for updates
        )

        log.info(f"Registered tool manager: {name}")

    def xǁToolRegistryǁregister_tool_manager__mutmut_21(
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

        log.info(None)
    
    xǁToolRegistryǁregister_tool_manager__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁToolRegistryǁregister_tool_manager__mutmut_1': xǁToolRegistryǁregister_tool_manager__mutmut_1, 
        'xǁToolRegistryǁregister_tool_manager__mutmut_2': xǁToolRegistryǁregister_tool_manager__mutmut_2, 
        'xǁToolRegistryǁregister_tool_manager__mutmut_3': xǁToolRegistryǁregister_tool_manager__mutmut_3, 
        'xǁToolRegistryǁregister_tool_manager__mutmut_4': xǁToolRegistryǁregister_tool_manager__mutmut_4, 
        'xǁToolRegistryǁregister_tool_manager__mutmut_5': xǁToolRegistryǁregister_tool_manager__mutmut_5, 
        'xǁToolRegistryǁregister_tool_manager__mutmut_6': xǁToolRegistryǁregister_tool_manager__mutmut_6, 
        'xǁToolRegistryǁregister_tool_manager__mutmut_7': xǁToolRegistryǁregister_tool_manager__mutmut_7, 
        'xǁToolRegistryǁregister_tool_manager__mutmut_8': xǁToolRegistryǁregister_tool_manager__mutmut_8, 
        'xǁToolRegistryǁregister_tool_manager__mutmut_9': xǁToolRegistryǁregister_tool_manager__mutmut_9, 
        'xǁToolRegistryǁregister_tool_manager__mutmut_10': xǁToolRegistryǁregister_tool_manager__mutmut_10, 
        'xǁToolRegistryǁregister_tool_manager__mutmut_11': xǁToolRegistryǁregister_tool_manager__mutmut_11, 
        'xǁToolRegistryǁregister_tool_manager__mutmut_12': xǁToolRegistryǁregister_tool_manager__mutmut_12, 
        'xǁToolRegistryǁregister_tool_manager__mutmut_13': xǁToolRegistryǁregister_tool_manager__mutmut_13, 
        'xǁToolRegistryǁregister_tool_manager__mutmut_14': xǁToolRegistryǁregister_tool_manager__mutmut_14, 
        'xǁToolRegistryǁregister_tool_manager__mutmut_15': xǁToolRegistryǁregister_tool_manager__mutmut_15, 
        'xǁToolRegistryǁregister_tool_manager__mutmut_16': xǁToolRegistryǁregister_tool_manager__mutmut_16, 
        'xǁToolRegistryǁregister_tool_manager__mutmut_17': xǁToolRegistryǁregister_tool_manager__mutmut_17, 
        'xǁToolRegistryǁregister_tool_manager__mutmut_18': xǁToolRegistryǁregister_tool_manager__mutmut_18, 
        'xǁToolRegistryǁregister_tool_manager__mutmut_19': xǁToolRegistryǁregister_tool_manager__mutmut_19, 
        'xǁToolRegistryǁregister_tool_manager__mutmut_20': xǁToolRegistryǁregister_tool_manager__mutmut_20, 
        'xǁToolRegistryǁregister_tool_manager__mutmut_21': xǁToolRegistryǁregister_tool_manager__mutmut_21
    }
    
    def register_tool_manager(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁToolRegistryǁregister_tool_manager__mutmut_orig"), object.__getattribute__(self, "xǁToolRegistryǁregister_tool_manager__mutmut_mutants"), args, kwargs, self)
        return result 
    
    register_tool_manager.__signature__ = _mutmut_signature(xǁToolRegistryǁregister_tool_manager__mutmut_orig)
    xǁToolRegistryǁregister_tool_manager__mutmut_orig.__name__ = 'xǁToolRegistryǁregister_tool_manager'

    def xǁToolRegistryǁget_tool_manager_class__mutmut_orig(self, name: str) -> type[BaseToolManager] | None:
        """Get a tool manager class by name.

        Args:
            name: Tool name or alias.

        Returns:
            Tool manager class, or None if not found.

        """
        return self.hub._component_registry.get(name, dimension=self.DIMENSION)

    def xǁToolRegistryǁget_tool_manager_class__mutmut_1(self, name: str) -> type[BaseToolManager] | None:
        """Get a tool manager class by name.

        Args:
            name: Tool name or alias.

        Returns:
            Tool manager class, or None if not found.

        """
        return self.hub._component_registry.get(None, dimension=self.DIMENSION)

    def xǁToolRegistryǁget_tool_manager_class__mutmut_2(self, name: str) -> type[BaseToolManager] | None:
        """Get a tool manager class by name.

        Args:
            name: Tool name or alias.

        Returns:
            Tool manager class, or None if not found.

        """
        return self.hub._component_registry.get(name, dimension=None)

    def xǁToolRegistryǁget_tool_manager_class__mutmut_3(self, name: str) -> type[BaseToolManager] | None:
        """Get a tool manager class by name.

        Args:
            name: Tool name or alias.

        Returns:
            Tool manager class, or None if not found.

        """
        return self.hub._component_registry.get(dimension=self.DIMENSION)

    def xǁToolRegistryǁget_tool_manager_class__mutmut_4(self, name: str) -> type[BaseToolManager] | None:
        """Get a tool manager class by name.

        Args:
            name: Tool name or alias.

        Returns:
            Tool manager class, or None if not found.

        """
        return self.hub._component_registry.get(name, )
    
    xǁToolRegistryǁget_tool_manager_class__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁToolRegistryǁget_tool_manager_class__mutmut_1': xǁToolRegistryǁget_tool_manager_class__mutmut_1, 
        'xǁToolRegistryǁget_tool_manager_class__mutmut_2': xǁToolRegistryǁget_tool_manager_class__mutmut_2, 
        'xǁToolRegistryǁget_tool_manager_class__mutmut_3': xǁToolRegistryǁget_tool_manager_class__mutmut_3, 
        'xǁToolRegistryǁget_tool_manager_class__mutmut_4': xǁToolRegistryǁget_tool_manager_class__mutmut_4
    }
    
    def get_tool_manager_class(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁToolRegistryǁget_tool_manager_class__mutmut_orig"), object.__getattribute__(self, "xǁToolRegistryǁget_tool_manager_class__mutmut_mutants"), args, kwargs, self)
        return result 
    
    get_tool_manager_class.__signature__ = _mutmut_signature(xǁToolRegistryǁget_tool_manager_class__mutmut_orig)
    xǁToolRegistryǁget_tool_manager_class__mutmut_orig.__name__ = 'xǁToolRegistryǁget_tool_manager_class'

    def xǁToolRegistryǁcreate_tool_manager__mutmut_orig(self, name: str, config: BaseConfig) -> BaseToolManager | None:
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

    def xǁToolRegistryǁcreate_tool_manager__mutmut_1(self, name: str, config: BaseConfig) -> BaseToolManager | None:
        """Create a tool manager instance.

        Args:
            name: Tool name or alias.
            config: Configuration object.

        Returns:
            Tool manager instance, or None if not found.

        """
        manager_class = None
        if manager_class:
            return manager_class(config)
        return None

    def xǁToolRegistryǁcreate_tool_manager__mutmut_2(self, name: str, config: BaseConfig) -> BaseToolManager | None:
        """Create a tool manager instance.

        Args:
            name: Tool name or alias.
            config: Configuration object.

        Returns:
            Tool manager instance, or None if not found.

        """
        manager_class = self.get_tool_manager_class(None)
        if manager_class:
            return manager_class(config)
        return None

    def xǁToolRegistryǁcreate_tool_manager__mutmut_3(self, name: str, config: BaseConfig) -> BaseToolManager | None:
        """Create a tool manager instance.

        Args:
            name: Tool name or alias.
            config: Configuration object.

        Returns:
            Tool manager instance, or None if not found.

        """
        manager_class = self.get_tool_manager_class(name)
        if manager_class:
            return manager_class(None)
        return None
    
    xǁToolRegistryǁcreate_tool_manager__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁToolRegistryǁcreate_tool_manager__mutmut_1': xǁToolRegistryǁcreate_tool_manager__mutmut_1, 
        'xǁToolRegistryǁcreate_tool_manager__mutmut_2': xǁToolRegistryǁcreate_tool_manager__mutmut_2, 
        'xǁToolRegistryǁcreate_tool_manager__mutmut_3': xǁToolRegistryǁcreate_tool_manager__mutmut_3
    }
    
    def create_tool_manager(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁToolRegistryǁcreate_tool_manager__mutmut_orig"), object.__getattribute__(self, "xǁToolRegistryǁcreate_tool_manager__mutmut_mutants"), args, kwargs, self)
        return result 
    
    create_tool_manager.__signature__ = _mutmut_signature(xǁToolRegistryǁcreate_tool_manager__mutmut_orig)
    xǁToolRegistryǁcreate_tool_manager__mutmut_orig.__name__ = 'xǁToolRegistryǁcreate_tool_manager'

    def xǁToolRegistryǁlist_tools__mutmut_orig(self) -> list[tuple[str, dict[str, Any]]]:
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

    def xǁToolRegistryǁlist_tools__mutmut_1(self) -> list[tuple[str, dict[str, Any]]]:
        """List all registered tools.

        Returns:
            List of (name, metadata) tuples.

        """
        tools = None
        dimension_list = self.hub._component_registry.list_dimension(self.DIMENSION)
        for item in dimension_list:
            name, entry = item  # type: ignore[misc]
            metadata = entry.metadata if hasattr(entry, "metadata") else {}  # type: ignore[has-type]
            tools.append((name, metadata))  # type: ignore[has-type]
        return tools

    def xǁToolRegistryǁlist_tools__mutmut_2(self) -> list[tuple[str, dict[str, Any]]]:
        """List all registered tools.

        Returns:
            List of (name, metadata) tuples.

        """
        tools = []
        dimension_list = None
        for item in dimension_list:
            name, entry = item  # type: ignore[misc]
            metadata = entry.metadata if hasattr(entry, "metadata") else {}  # type: ignore[has-type]
            tools.append((name, metadata))  # type: ignore[has-type]
        return tools

    def xǁToolRegistryǁlist_tools__mutmut_3(self) -> list[tuple[str, dict[str, Any]]]:
        """List all registered tools.

        Returns:
            List of (name, metadata) tuples.

        """
        tools = []
        dimension_list = self.hub._component_registry.list_dimension(None)
        for item in dimension_list:
            name, entry = item  # type: ignore[misc]
            metadata = entry.metadata if hasattr(entry, "metadata") else {}  # type: ignore[has-type]
            tools.append((name, metadata))  # type: ignore[has-type]
        return tools

    def xǁToolRegistryǁlist_tools__mutmut_4(self) -> list[tuple[str, dict[str, Any]]]:
        """List all registered tools.

        Returns:
            List of (name, metadata) tuples.

        """
        tools = []
        dimension_list = self.hub._component_registry.list_dimension(self.DIMENSION)
        for item in dimension_list:
            name, entry = None  # type: ignore[misc]
            metadata = entry.metadata if hasattr(entry, "metadata") else {}  # type: ignore[has-type]
            tools.append((name, metadata))  # type: ignore[has-type]
        return tools

    def xǁToolRegistryǁlist_tools__mutmut_5(self) -> list[tuple[str, dict[str, Any]]]:
        """List all registered tools.

        Returns:
            List of (name, metadata) tuples.

        """
        tools = []
        dimension_list = self.hub._component_registry.list_dimension(self.DIMENSION)
        for item in dimension_list:
            name, entry = item  # type: ignore[misc]
            metadata = None  # type: ignore[has-type]
            tools.append((name, metadata))  # type: ignore[has-type]
        return tools

    def xǁToolRegistryǁlist_tools__mutmut_6(self) -> list[tuple[str, dict[str, Any]]]:
        """List all registered tools.

        Returns:
            List of (name, metadata) tuples.

        """
        tools = []
        dimension_list = self.hub._component_registry.list_dimension(self.DIMENSION)
        for item in dimension_list:
            name, entry = item  # type: ignore[misc]
            metadata = entry.metadata if hasattr(None, "metadata") else {}  # type: ignore[has-type]
            tools.append((name, metadata))  # type: ignore[has-type]
        return tools

    def xǁToolRegistryǁlist_tools__mutmut_7(self) -> list[tuple[str, dict[str, Any]]]:
        """List all registered tools.

        Returns:
            List of (name, metadata) tuples.

        """
        tools = []
        dimension_list = self.hub._component_registry.list_dimension(self.DIMENSION)
        for item in dimension_list:
            name, entry = item  # type: ignore[misc]
            metadata = entry.metadata if hasattr(entry, None) else {}  # type: ignore[has-type]
            tools.append((name, metadata))  # type: ignore[has-type]
        return tools

    def xǁToolRegistryǁlist_tools__mutmut_8(self) -> list[tuple[str, dict[str, Any]]]:
        """List all registered tools.

        Returns:
            List of (name, metadata) tuples.

        """
        tools = []
        dimension_list = self.hub._component_registry.list_dimension(self.DIMENSION)
        for item in dimension_list:
            name, entry = item  # type: ignore[misc]
            metadata = entry.metadata if hasattr("metadata") else {}  # type: ignore[has-type]
            tools.append((name, metadata))  # type: ignore[has-type]
        return tools

    def xǁToolRegistryǁlist_tools__mutmut_9(self) -> list[tuple[str, dict[str, Any]]]:
        """List all registered tools.

        Returns:
            List of (name, metadata) tuples.

        """
        tools = []
        dimension_list = self.hub._component_registry.list_dimension(self.DIMENSION)
        for item in dimension_list:
            name, entry = item  # type: ignore[misc]
            metadata = entry.metadata if hasattr(entry, ) else {}  # type: ignore[has-type]
            tools.append((name, metadata))  # type: ignore[has-type]
        return tools

    def xǁToolRegistryǁlist_tools__mutmut_10(self) -> list[tuple[str, dict[str, Any]]]:
        """List all registered tools.

        Returns:
            List of (name, metadata) tuples.

        """
        tools = []
        dimension_list = self.hub._component_registry.list_dimension(self.DIMENSION)
        for item in dimension_list:
            name, entry = item  # type: ignore[misc]
            metadata = entry.metadata if hasattr(entry, "XXmetadataXX") else {}  # type: ignore[has-type]
            tools.append((name, metadata))  # type: ignore[has-type]
        return tools

    def xǁToolRegistryǁlist_tools__mutmut_11(self) -> list[tuple[str, dict[str, Any]]]:
        """List all registered tools.

        Returns:
            List of (name, metadata) tuples.

        """
        tools = []
        dimension_list = self.hub._component_registry.list_dimension(self.DIMENSION)
        for item in dimension_list:
            name, entry = item  # type: ignore[misc]
            metadata = entry.metadata if hasattr(entry, "METADATA") else {}  # type: ignore[has-type]
            tools.append((name, metadata))  # type: ignore[has-type]
        return tools

    def xǁToolRegistryǁlist_tools__mutmut_12(self) -> list[tuple[str, dict[str, Any]]]:
        """List all registered tools.

        Returns:
            List of (name, metadata) tuples.

        """
        tools = []
        dimension_list = self.hub._component_registry.list_dimension(self.DIMENSION)
        for item in dimension_list:
            name, entry = item  # type: ignore[misc]
            metadata = entry.metadata if hasattr(entry, "metadata") else {}  # type: ignore[has-type]
            tools.append(None)  # type: ignore[has-type]
        return tools
    
    xǁToolRegistryǁlist_tools__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁToolRegistryǁlist_tools__mutmut_1': xǁToolRegistryǁlist_tools__mutmut_1, 
        'xǁToolRegistryǁlist_tools__mutmut_2': xǁToolRegistryǁlist_tools__mutmut_2, 
        'xǁToolRegistryǁlist_tools__mutmut_3': xǁToolRegistryǁlist_tools__mutmut_3, 
        'xǁToolRegistryǁlist_tools__mutmut_4': xǁToolRegistryǁlist_tools__mutmut_4, 
        'xǁToolRegistryǁlist_tools__mutmut_5': xǁToolRegistryǁlist_tools__mutmut_5, 
        'xǁToolRegistryǁlist_tools__mutmut_6': xǁToolRegistryǁlist_tools__mutmut_6, 
        'xǁToolRegistryǁlist_tools__mutmut_7': xǁToolRegistryǁlist_tools__mutmut_7, 
        'xǁToolRegistryǁlist_tools__mutmut_8': xǁToolRegistryǁlist_tools__mutmut_8, 
        'xǁToolRegistryǁlist_tools__mutmut_9': xǁToolRegistryǁlist_tools__mutmut_9, 
        'xǁToolRegistryǁlist_tools__mutmut_10': xǁToolRegistryǁlist_tools__mutmut_10, 
        'xǁToolRegistryǁlist_tools__mutmut_11': xǁToolRegistryǁlist_tools__mutmut_11, 
        'xǁToolRegistryǁlist_tools__mutmut_12': xǁToolRegistryǁlist_tools__mutmut_12
    }
    
    def list_tools(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁToolRegistryǁlist_tools__mutmut_orig"), object.__getattribute__(self, "xǁToolRegistryǁlist_tools__mutmut_mutants"), args, kwargs, self)
        return result 
    
    list_tools.__signature__ = _mutmut_signature(xǁToolRegistryǁlist_tools__mutmut_orig)
    xǁToolRegistryǁlist_tools__mutmut_orig.__name__ = 'xǁToolRegistryǁlist_tools'

    def xǁToolRegistryǁget_tool_info__mutmut_orig(self, name: str) -> dict[str, Any] | None:
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

    def xǁToolRegistryǁget_tool_info__mutmut_1(self, name: str) -> dict[str, Any] | None:
        """Get information about a specific tool.

        Args:
            name: Tool name or alias.

        Returns:
            Tool metadata dictionary, or None if not found.

        """
        entry = None
        if entry and hasattr(entry, "metadata"):
            return entry.metadata
        return None

    def xǁToolRegistryǁget_tool_info__mutmut_2(self, name: str) -> dict[str, Any] | None:
        """Get information about a specific tool.

        Args:
            name: Tool name or alias.

        Returns:
            Tool metadata dictionary, or None if not found.

        """
        entry = self.hub._component_registry.get_entry(None, dimension=self.DIMENSION)
        if entry and hasattr(entry, "metadata"):
            return entry.metadata
        return None

    def xǁToolRegistryǁget_tool_info__mutmut_3(self, name: str) -> dict[str, Any] | None:
        """Get information about a specific tool.

        Args:
            name: Tool name or alias.

        Returns:
            Tool metadata dictionary, or None if not found.

        """
        entry = self.hub._component_registry.get_entry(name, dimension=None)
        if entry and hasattr(entry, "metadata"):
            return entry.metadata
        return None

    def xǁToolRegistryǁget_tool_info__mutmut_4(self, name: str) -> dict[str, Any] | None:
        """Get information about a specific tool.

        Args:
            name: Tool name or alias.

        Returns:
            Tool metadata dictionary, or None if not found.

        """
        entry = self.hub._component_registry.get_entry(dimension=self.DIMENSION)
        if entry and hasattr(entry, "metadata"):
            return entry.metadata
        return None

    def xǁToolRegistryǁget_tool_info__mutmut_5(self, name: str) -> dict[str, Any] | None:
        """Get information about a specific tool.

        Args:
            name: Tool name or alias.

        Returns:
            Tool metadata dictionary, or None if not found.

        """
        entry = self.hub._component_registry.get_entry(name, )
        if entry and hasattr(entry, "metadata"):
            return entry.metadata
        return None

    def xǁToolRegistryǁget_tool_info__mutmut_6(self, name: str) -> dict[str, Any] | None:
        """Get information about a specific tool.

        Args:
            name: Tool name or alias.

        Returns:
            Tool metadata dictionary, or None if not found.

        """
        entry = self.hub._component_registry.get_entry(name, dimension=self.DIMENSION)
        if entry or hasattr(entry, "metadata"):
            return entry.metadata
        return None

    def xǁToolRegistryǁget_tool_info__mutmut_7(self, name: str) -> dict[str, Any] | None:
        """Get information about a specific tool.

        Args:
            name: Tool name or alias.

        Returns:
            Tool metadata dictionary, or None if not found.

        """
        entry = self.hub._component_registry.get_entry(name, dimension=self.DIMENSION)
        if entry and hasattr(None, "metadata"):
            return entry.metadata
        return None

    def xǁToolRegistryǁget_tool_info__mutmut_8(self, name: str) -> dict[str, Any] | None:
        """Get information about a specific tool.

        Args:
            name: Tool name or alias.

        Returns:
            Tool metadata dictionary, or None if not found.

        """
        entry = self.hub._component_registry.get_entry(name, dimension=self.DIMENSION)
        if entry and hasattr(entry, None):
            return entry.metadata
        return None

    def xǁToolRegistryǁget_tool_info__mutmut_9(self, name: str) -> dict[str, Any] | None:
        """Get information about a specific tool.

        Args:
            name: Tool name or alias.

        Returns:
            Tool metadata dictionary, or None if not found.

        """
        entry = self.hub._component_registry.get_entry(name, dimension=self.DIMENSION)
        if entry and hasattr("metadata"):
            return entry.metadata
        return None

    def xǁToolRegistryǁget_tool_info__mutmut_10(self, name: str) -> dict[str, Any] | None:
        """Get information about a specific tool.

        Args:
            name: Tool name or alias.

        Returns:
            Tool metadata dictionary, or None if not found.

        """
        entry = self.hub._component_registry.get_entry(name, dimension=self.DIMENSION)
        if entry and hasattr(entry, ):
            return entry.metadata
        return None

    def xǁToolRegistryǁget_tool_info__mutmut_11(self, name: str) -> dict[str, Any] | None:
        """Get information about a specific tool.

        Args:
            name: Tool name or alias.

        Returns:
            Tool metadata dictionary, or None if not found.

        """
        entry = self.hub._component_registry.get_entry(name, dimension=self.DIMENSION)
        if entry and hasattr(entry, "XXmetadataXX"):
            return entry.metadata
        return None

    def xǁToolRegistryǁget_tool_info__mutmut_12(self, name: str) -> dict[str, Any] | None:
        """Get information about a specific tool.

        Args:
            name: Tool name or alias.

        Returns:
            Tool metadata dictionary, or None if not found.

        """
        entry = self.hub._component_registry.get_entry(name, dimension=self.DIMENSION)
        if entry and hasattr(entry, "METADATA"):
            return entry.metadata
        return None
    
    xǁToolRegistryǁget_tool_info__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁToolRegistryǁget_tool_info__mutmut_1': xǁToolRegistryǁget_tool_info__mutmut_1, 
        'xǁToolRegistryǁget_tool_info__mutmut_2': xǁToolRegistryǁget_tool_info__mutmut_2, 
        'xǁToolRegistryǁget_tool_info__mutmut_3': xǁToolRegistryǁget_tool_info__mutmut_3, 
        'xǁToolRegistryǁget_tool_info__mutmut_4': xǁToolRegistryǁget_tool_info__mutmut_4, 
        'xǁToolRegistryǁget_tool_info__mutmut_5': xǁToolRegistryǁget_tool_info__mutmut_5, 
        'xǁToolRegistryǁget_tool_info__mutmut_6': xǁToolRegistryǁget_tool_info__mutmut_6, 
        'xǁToolRegistryǁget_tool_info__mutmut_7': xǁToolRegistryǁget_tool_info__mutmut_7, 
        'xǁToolRegistryǁget_tool_info__mutmut_8': xǁToolRegistryǁget_tool_info__mutmut_8, 
        'xǁToolRegistryǁget_tool_info__mutmut_9': xǁToolRegistryǁget_tool_info__mutmut_9, 
        'xǁToolRegistryǁget_tool_info__mutmut_10': xǁToolRegistryǁget_tool_info__mutmut_10, 
        'xǁToolRegistryǁget_tool_info__mutmut_11': xǁToolRegistryǁget_tool_info__mutmut_11, 
        'xǁToolRegistryǁget_tool_info__mutmut_12': xǁToolRegistryǁget_tool_info__mutmut_12
    }
    
    def get_tool_info(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁToolRegistryǁget_tool_info__mutmut_orig"), object.__getattribute__(self, "xǁToolRegistryǁget_tool_info__mutmut_mutants"), args, kwargs, self)
        return result 
    
    get_tool_info.__signature__ = _mutmut_signature(xǁToolRegistryǁget_tool_info__mutmut_orig)
    xǁToolRegistryǁget_tool_info__mutmut_orig.__name__ = 'xǁToolRegistryǁget_tool_info'

    def xǁToolRegistryǁis_tool_registered__mutmut_orig(self, name: str) -> bool:
        """Check if a tool is registered.

        Args:
            name: Tool name or alias.

        Returns:
            True if registered, False otherwise.

        """
        return self.get_tool_manager_class(name) is not None

    def xǁToolRegistryǁis_tool_registered__mutmut_1(self, name: str) -> bool:
        """Check if a tool is registered.

        Args:
            name: Tool name or alias.

        Returns:
            True if registered, False otherwise.

        """
        return self.get_tool_manager_class(None) is not None

    def xǁToolRegistryǁis_tool_registered__mutmut_2(self, name: str) -> bool:
        """Check if a tool is registered.

        Args:
            name: Tool name or alias.

        Returns:
            True if registered, False otherwise.

        """
        return self.get_tool_manager_class(name) is None
    
    xǁToolRegistryǁis_tool_registered__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁToolRegistryǁis_tool_registered__mutmut_1': xǁToolRegistryǁis_tool_registered__mutmut_1, 
        'xǁToolRegistryǁis_tool_registered__mutmut_2': xǁToolRegistryǁis_tool_registered__mutmut_2
    }
    
    def is_tool_registered(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁToolRegistryǁis_tool_registered__mutmut_orig"), object.__getattribute__(self, "xǁToolRegistryǁis_tool_registered__mutmut_mutants"), args, kwargs, self)
        return result 
    
    is_tool_registered.__signature__ = _mutmut_signature(xǁToolRegistryǁis_tool_registered__mutmut_orig)
    xǁToolRegistryǁis_tool_registered__mutmut_orig.__name__ = 'xǁToolRegistryǁis_tool_registered'


# Global registry instance
_tool_registry: ToolRegistry | None = None


def x_get_tool_registry__mutmut_orig() -> ToolRegistry:
    """Get the global tool registry instance.

    Returns:
        Tool registry instance.

    """
    global _tool_registry
    if _tool_registry is None:
        _tool_registry = ToolRegistry()
    return _tool_registry


def x_get_tool_registry__mutmut_1() -> ToolRegistry:
    """Get the global tool registry instance.

    Returns:
        Tool registry instance.

    """
    global _tool_registry
    if _tool_registry is not None:
        _tool_registry = ToolRegistry()
    return _tool_registry


def x_get_tool_registry__mutmut_2() -> ToolRegistry:
    """Get the global tool registry instance.

    Returns:
        Tool registry instance.

    """
    global _tool_registry
    if _tool_registry is None:
        _tool_registry = None
    return _tool_registry

x_get_tool_registry__mutmut_mutants : ClassVar[MutantDict] = {
'x_get_tool_registry__mutmut_1': x_get_tool_registry__mutmut_1, 
    'x_get_tool_registry__mutmut_2': x_get_tool_registry__mutmut_2
}

def get_tool_registry(*args, **kwargs):
    result = _mutmut_trampoline(x_get_tool_registry__mutmut_orig, x_get_tool_registry__mutmut_mutants, args, kwargs)
    return result 

get_tool_registry.__signature__ = _mutmut_signature(x_get_tool_registry__mutmut_orig)
x_get_tool_registry__mutmut_orig.__name__ = 'x_get_tool_registry'


def x_register_tool_manager__mutmut_orig(
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


def x_register_tool_manager__mutmut_1(
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
    registry = None
    registry.register_tool_manager(name, manager_class, aliases)


def x_register_tool_manager__mutmut_2(
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
    registry.register_tool_manager(None, manager_class, aliases)


def x_register_tool_manager__mutmut_3(
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
    registry.register_tool_manager(name, None, aliases)


def x_register_tool_manager__mutmut_4(
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
    registry.register_tool_manager(name, manager_class, None)


def x_register_tool_manager__mutmut_5(
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
    registry.register_tool_manager(manager_class, aliases)


def x_register_tool_manager__mutmut_6(
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
    registry.register_tool_manager(name, aliases)


def x_register_tool_manager__mutmut_7(
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
    registry.register_tool_manager(name, manager_class, )

x_register_tool_manager__mutmut_mutants : ClassVar[MutantDict] = {
'x_register_tool_manager__mutmut_1': x_register_tool_manager__mutmut_1, 
    'x_register_tool_manager__mutmut_2': x_register_tool_manager__mutmut_2, 
    'x_register_tool_manager__mutmut_3': x_register_tool_manager__mutmut_3, 
    'x_register_tool_manager__mutmut_4': x_register_tool_manager__mutmut_4, 
    'x_register_tool_manager__mutmut_5': x_register_tool_manager__mutmut_5, 
    'x_register_tool_manager__mutmut_6': x_register_tool_manager__mutmut_6, 
    'x_register_tool_manager__mutmut_7': x_register_tool_manager__mutmut_7
}

def register_tool_manager(*args, **kwargs):
    result = _mutmut_trampoline(x_register_tool_manager__mutmut_orig, x_register_tool_manager__mutmut_mutants, args, kwargs)
    return result 

register_tool_manager.__signature__ = _mutmut_signature(x_register_tool_manager__mutmut_orig)
x_register_tool_manager__mutmut_orig.__name__ = 'x_register_tool_manager'


def x_get_tool_manager__mutmut_orig(name: str, config: BaseConfig) -> BaseToolManager | None:
    """Get a tool manager instance from the global registry.

    Args:
        name: Tool name or alias.
        config: Configuration object.

    Returns:
        Tool manager instance, or None if not found.

    """
    registry = get_tool_registry()
    return registry.create_tool_manager(name, config)


def x_get_tool_manager__mutmut_1(name: str, config: BaseConfig) -> BaseToolManager | None:
    """Get a tool manager instance from the global registry.

    Args:
        name: Tool name or alias.
        config: Configuration object.

    Returns:
        Tool manager instance, or None if not found.

    """
    registry = None
    return registry.create_tool_manager(name, config)


def x_get_tool_manager__mutmut_2(name: str, config: BaseConfig) -> BaseToolManager | None:
    """Get a tool manager instance from the global registry.

    Args:
        name: Tool name or alias.
        config: Configuration object.

    Returns:
        Tool manager instance, or None if not found.

    """
    registry = get_tool_registry()
    return registry.create_tool_manager(None, config)


def x_get_tool_manager__mutmut_3(name: str, config: BaseConfig) -> BaseToolManager | None:
    """Get a tool manager instance from the global registry.

    Args:
        name: Tool name or alias.
        config: Configuration object.

    Returns:
        Tool manager instance, or None if not found.

    """
    registry = get_tool_registry()
    return registry.create_tool_manager(name, None)


def x_get_tool_manager__mutmut_4(name: str, config: BaseConfig) -> BaseToolManager | None:
    """Get a tool manager instance from the global registry.

    Args:
        name: Tool name or alias.
        config: Configuration object.

    Returns:
        Tool manager instance, or None if not found.

    """
    registry = get_tool_registry()
    return registry.create_tool_manager(config)


def x_get_tool_manager__mutmut_5(name: str, config: BaseConfig) -> BaseToolManager | None:
    """Get a tool manager instance from the global registry.

    Args:
        name: Tool name or alias.
        config: Configuration object.

    Returns:
        Tool manager instance, or None if not found.

    """
    registry = get_tool_registry()
    return registry.create_tool_manager(name, )

x_get_tool_manager__mutmut_mutants : ClassVar[MutantDict] = {
'x_get_tool_manager__mutmut_1': x_get_tool_manager__mutmut_1, 
    'x_get_tool_manager__mutmut_2': x_get_tool_manager__mutmut_2, 
    'x_get_tool_manager__mutmut_3': x_get_tool_manager__mutmut_3, 
    'x_get_tool_manager__mutmut_4': x_get_tool_manager__mutmut_4, 
    'x_get_tool_manager__mutmut_5': x_get_tool_manager__mutmut_5
}

def get_tool_manager(*args, **kwargs):
    result = _mutmut_trampoline(x_get_tool_manager__mutmut_orig, x_get_tool_manager__mutmut_mutants, args, kwargs)
    return result 

get_tool_manager.__signature__ = _mutmut_signature(x_get_tool_manager__mutmut_orig)
x_get_tool_manager__mutmut_orig.__name__ = 'x_get_tool_manager'


# <3 🧱🤝🔧🪄
