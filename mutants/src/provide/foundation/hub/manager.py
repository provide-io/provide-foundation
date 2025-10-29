# provide/foundation/hub/manager.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from typing import Any

from provide.foundation.concurrency.locks import get_lock_manager
from provide.foundation.context import CLIContext
from provide.foundation.hub.commands import get_command_registry
from provide.foundation.hub.components import get_component_registry
from provide.foundation.hub.core import CoreHub
from provide.foundation.hub.foundation import FoundationManager
from provide.foundation.hub.registry import Registry
from provide.foundation.testmode.detection import should_use_shared_registries

"""Hub manager - the main coordinator for components and commands.

This module provides the Hub class that coordinates component and command
registration, discovery, and access, with Foundation system integration.
"""
from inspect import signature as _mutmut_signature
from typing import Annotated
from typing import Callable
from typing import ClassVar


MutantDict = Annotated[dict[str, Callable], "Mutant"]


def _mutmut_trampoline(orig, mutants, call_args, call_kwargs, self_arg=None):
    """Forward call to original or mutated function, depending on the environment"""
    import os

    mutant_under_test = os.environ["MUTANT_UNDER_TEST"]
    if mutant_under_test == "fail":
        from mutmut.__main__ import MutmutProgrammaticFailException

        raise MutmutProgrammaticFailException("Failed programmatically")
    elif mutant_under_test == "stats":
        from mutmut.__main__ import record_trampoline_hit

        record_trampoline_hit(orig.__module__ + "." + orig.__name__)
        result = orig(*call_args, **call_kwargs)
        return result
    prefix = orig.__module__ + "." + orig.__name__ + "__mutmut_"
    if not mutant_under_test.startswith(prefix):
        result = orig(*call_args, **call_kwargs)
        return result
    mutant_name = mutant_under_test.rpartition(".")[-1]
    if self_arg:
        # call to a class method where self is not bound
        result = mutants[mutant_name](self_arg, *call_args, **call_kwargs)
    else:
        result = mutants[mutant_name](*call_args, **call_kwargs)
    return result


class Hub(CoreHub):
    """Central hub for managing components, commands, and Foundation integration.

    The Hub provides a unified interface for:
    - Registering components and commands
    - Discovering plugins via entry points
    - Creating Click CLI applications
    - Managing component lifecycle
    - Foundation system initialization

    Example:
        >>> hub = Hub()
        >>> hub.add_component(MyResource, "resource")
        >>> hub.add_command(init_cmd, "init")
        >>> hub.initialize_foundation()
        >>>
        >>> # Create CLI with all commands
        >>> cli = hub.create_cli()
        >>> cli()

    """

    def xǁHubǁ__init____mutmut_orig(
        self,
        context: CLIContext | None = None,
        component_registry: Registry | None = None,
        command_registry: Registry | None = None,
        use_shared_registries: bool = False,
    ) -> None:
        """Initialize the hub.

        Args:
            context: Foundation CLIContext for configuration
            component_registry: Custom component registry
            command_registry: Custom command registry
            use_shared_registries: If True, use global shared registries

        """
        # Determine if we should use shared registries
        use_shared = should_use_shared_registries(use_shared_registries, component_registry, command_registry)

        # Setup registries
        if component_registry:
            comp_registry = component_registry
        elif use_shared:
            comp_registry = get_component_registry()
        else:
            comp_registry = Registry()

        if command_registry:
            cmd_registry = command_registry
        elif use_shared:
            cmd_registry = get_command_registry()
        else:
            cmd_registry = Registry()

        # Initialize core hub functionality
        super().__init__(context, comp_registry, cmd_registry)

        # Initialize Foundation management, injecting self
        self._foundation = FoundationManager(hub=self, registry=self._component_registry)

    def xǁHubǁ__init____mutmut_1(
        self,
        context: CLIContext | None = None,
        component_registry: Registry | None = None,
        command_registry: Registry | None = None,
        use_shared_registries: bool = True,
    ) -> None:
        """Initialize the hub.

        Args:
            context: Foundation CLIContext for configuration
            component_registry: Custom component registry
            command_registry: Custom command registry
            use_shared_registries: If True, use global shared registries

        """
        # Determine if we should use shared registries
        use_shared = should_use_shared_registries(use_shared_registries, component_registry, command_registry)

        # Setup registries
        if component_registry:
            comp_registry = component_registry
        elif use_shared:
            comp_registry = get_component_registry()
        else:
            comp_registry = Registry()

        if command_registry:
            cmd_registry = command_registry
        elif use_shared:
            cmd_registry = get_command_registry()
        else:
            cmd_registry = Registry()

        # Initialize core hub functionality
        super().__init__(context, comp_registry, cmd_registry)

        # Initialize Foundation management, injecting self
        self._foundation = FoundationManager(hub=self, registry=self._component_registry)

    def xǁHubǁ__init____mutmut_2(
        self,
        context: CLIContext | None = None,
        component_registry: Registry | None = None,
        command_registry: Registry | None = None,
        use_shared_registries: bool = False,
    ) -> None:
        """Initialize the hub.

        Args:
            context: Foundation CLIContext for configuration
            component_registry: Custom component registry
            command_registry: Custom command registry
            use_shared_registries: If True, use global shared registries

        """
        # Determine if we should use shared registries
        use_shared = None

        # Setup registries
        if component_registry:
            comp_registry = component_registry
        elif use_shared:
            comp_registry = get_component_registry()
        else:
            comp_registry = Registry()

        if command_registry:
            cmd_registry = command_registry
        elif use_shared:
            cmd_registry = get_command_registry()
        else:
            cmd_registry = Registry()

        # Initialize core hub functionality
        super().__init__(context, comp_registry, cmd_registry)

        # Initialize Foundation management, injecting self
        self._foundation = FoundationManager(hub=self, registry=self._component_registry)

    def xǁHubǁ__init____mutmut_3(
        self,
        context: CLIContext | None = None,
        component_registry: Registry | None = None,
        command_registry: Registry | None = None,
        use_shared_registries: bool = False,
    ) -> None:
        """Initialize the hub.

        Args:
            context: Foundation CLIContext for configuration
            component_registry: Custom component registry
            command_registry: Custom command registry
            use_shared_registries: If True, use global shared registries

        """
        # Determine if we should use shared registries
        use_shared = should_use_shared_registries(None, component_registry, command_registry)

        # Setup registries
        if component_registry:
            comp_registry = component_registry
        elif use_shared:
            comp_registry = get_component_registry()
        else:
            comp_registry = Registry()

        if command_registry:
            cmd_registry = command_registry
        elif use_shared:
            cmd_registry = get_command_registry()
        else:
            cmd_registry = Registry()

        # Initialize core hub functionality
        super().__init__(context, comp_registry, cmd_registry)

        # Initialize Foundation management, injecting self
        self._foundation = FoundationManager(hub=self, registry=self._component_registry)

    def xǁHubǁ__init____mutmut_4(
        self,
        context: CLIContext | None = None,
        component_registry: Registry | None = None,
        command_registry: Registry | None = None,
        use_shared_registries: bool = False,
    ) -> None:
        """Initialize the hub.

        Args:
            context: Foundation CLIContext for configuration
            component_registry: Custom component registry
            command_registry: Custom command registry
            use_shared_registries: If True, use global shared registries

        """
        # Determine if we should use shared registries
        use_shared = should_use_shared_registries(use_shared_registries, None, command_registry)

        # Setup registries
        if component_registry:
            comp_registry = component_registry
        elif use_shared:
            comp_registry = get_component_registry()
        else:
            comp_registry = Registry()

        if command_registry:
            cmd_registry = command_registry
        elif use_shared:
            cmd_registry = get_command_registry()
        else:
            cmd_registry = Registry()

        # Initialize core hub functionality
        super().__init__(context, comp_registry, cmd_registry)

        # Initialize Foundation management, injecting self
        self._foundation = FoundationManager(hub=self, registry=self._component_registry)

    def xǁHubǁ__init____mutmut_5(
        self,
        context: CLIContext | None = None,
        component_registry: Registry | None = None,
        command_registry: Registry | None = None,
        use_shared_registries: bool = False,
    ) -> None:
        """Initialize the hub.

        Args:
            context: Foundation CLIContext for configuration
            component_registry: Custom component registry
            command_registry: Custom command registry
            use_shared_registries: If True, use global shared registries

        """
        # Determine if we should use shared registries
        use_shared = should_use_shared_registries(use_shared_registries, component_registry, None)

        # Setup registries
        if component_registry:
            comp_registry = component_registry
        elif use_shared:
            comp_registry = get_component_registry()
        else:
            comp_registry = Registry()

        if command_registry:
            cmd_registry = command_registry
        elif use_shared:
            cmd_registry = get_command_registry()
        else:
            cmd_registry = Registry()

        # Initialize core hub functionality
        super().__init__(context, comp_registry, cmd_registry)

        # Initialize Foundation management, injecting self
        self._foundation = FoundationManager(hub=self, registry=self._component_registry)

    def xǁHubǁ__init____mutmut_6(
        self,
        context: CLIContext | None = None,
        component_registry: Registry | None = None,
        command_registry: Registry | None = None,
        use_shared_registries: bool = False,
    ) -> None:
        """Initialize the hub.

        Args:
            context: Foundation CLIContext for configuration
            component_registry: Custom component registry
            command_registry: Custom command registry
            use_shared_registries: If True, use global shared registries

        """
        # Determine if we should use shared registries
        use_shared = should_use_shared_registries(component_registry, command_registry)

        # Setup registries
        if component_registry:
            comp_registry = component_registry
        elif use_shared:
            comp_registry = get_component_registry()
        else:
            comp_registry = Registry()

        if command_registry:
            cmd_registry = command_registry
        elif use_shared:
            cmd_registry = get_command_registry()
        else:
            cmd_registry = Registry()

        # Initialize core hub functionality
        super().__init__(context, comp_registry, cmd_registry)

        # Initialize Foundation management, injecting self
        self._foundation = FoundationManager(hub=self, registry=self._component_registry)

    def xǁHubǁ__init____mutmut_7(
        self,
        context: CLIContext | None = None,
        component_registry: Registry | None = None,
        command_registry: Registry | None = None,
        use_shared_registries: bool = False,
    ) -> None:
        """Initialize the hub.

        Args:
            context: Foundation CLIContext for configuration
            component_registry: Custom component registry
            command_registry: Custom command registry
            use_shared_registries: If True, use global shared registries

        """
        # Determine if we should use shared registries
        use_shared = should_use_shared_registries(use_shared_registries, command_registry)

        # Setup registries
        if component_registry:
            comp_registry = component_registry
        elif use_shared:
            comp_registry = get_component_registry()
        else:
            comp_registry = Registry()

        if command_registry:
            cmd_registry = command_registry
        elif use_shared:
            cmd_registry = get_command_registry()
        else:
            cmd_registry = Registry()

        # Initialize core hub functionality
        super().__init__(context, comp_registry, cmd_registry)

        # Initialize Foundation management, injecting self
        self._foundation = FoundationManager(hub=self, registry=self._component_registry)

    def xǁHubǁ__init____mutmut_8(
        self,
        context: CLIContext | None = None,
        component_registry: Registry | None = None,
        command_registry: Registry | None = None,
        use_shared_registries: bool = False,
    ) -> None:
        """Initialize the hub.

        Args:
            context: Foundation CLIContext for configuration
            component_registry: Custom component registry
            command_registry: Custom command registry
            use_shared_registries: If True, use global shared registries

        """
        # Determine if we should use shared registries
        use_shared = should_use_shared_registries(
            use_shared_registries,
            component_registry,
        )

        # Setup registries
        if component_registry:
            comp_registry = component_registry
        elif use_shared:
            comp_registry = get_component_registry()
        else:
            comp_registry = Registry()

        if command_registry:
            cmd_registry = command_registry
        elif use_shared:
            cmd_registry = get_command_registry()
        else:
            cmd_registry = Registry()

        # Initialize core hub functionality
        super().__init__(context, comp_registry, cmd_registry)

        # Initialize Foundation management, injecting self
        self._foundation = FoundationManager(hub=self, registry=self._component_registry)

    def xǁHubǁ__init____mutmut_9(
        self,
        context: CLIContext | None = None,
        component_registry: Registry | None = None,
        command_registry: Registry | None = None,
        use_shared_registries: bool = False,
    ) -> None:
        """Initialize the hub.

        Args:
            context: Foundation CLIContext for configuration
            component_registry: Custom component registry
            command_registry: Custom command registry
            use_shared_registries: If True, use global shared registries

        """
        # Determine if we should use shared registries
        use_shared = should_use_shared_registries(use_shared_registries, component_registry, command_registry)

        # Setup registries
        if component_registry:
            comp_registry = None
        elif use_shared:
            comp_registry = get_component_registry()
        else:
            comp_registry = Registry()

        if command_registry:
            cmd_registry = command_registry
        elif use_shared:
            cmd_registry = get_command_registry()
        else:
            cmd_registry = Registry()

        # Initialize core hub functionality
        super().__init__(context, comp_registry, cmd_registry)

        # Initialize Foundation management, injecting self
        self._foundation = FoundationManager(hub=self, registry=self._component_registry)

    def xǁHubǁ__init____mutmut_10(
        self,
        context: CLIContext | None = None,
        component_registry: Registry | None = None,
        command_registry: Registry | None = None,
        use_shared_registries: bool = False,
    ) -> None:
        """Initialize the hub.

        Args:
            context: Foundation CLIContext for configuration
            component_registry: Custom component registry
            command_registry: Custom command registry
            use_shared_registries: If True, use global shared registries

        """
        # Determine if we should use shared registries
        use_shared = should_use_shared_registries(use_shared_registries, component_registry, command_registry)

        # Setup registries
        if component_registry:
            comp_registry = component_registry
        elif use_shared:
            comp_registry = None
        else:
            comp_registry = Registry()

        if command_registry:
            cmd_registry = command_registry
        elif use_shared:
            cmd_registry = get_command_registry()
        else:
            cmd_registry = Registry()

        # Initialize core hub functionality
        super().__init__(context, comp_registry, cmd_registry)

        # Initialize Foundation management, injecting self
        self._foundation = FoundationManager(hub=self, registry=self._component_registry)

    def xǁHubǁ__init____mutmut_11(
        self,
        context: CLIContext | None = None,
        component_registry: Registry | None = None,
        command_registry: Registry | None = None,
        use_shared_registries: bool = False,
    ) -> None:
        """Initialize the hub.

        Args:
            context: Foundation CLIContext for configuration
            component_registry: Custom component registry
            command_registry: Custom command registry
            use_shared_registries: If True, use global shared registries

        """
        # Determine if we should use shared registries
        use_shared = should_use_shared_registries(use_shared_registries, component_registry, command_registry)

        # Setup registries
        if component_registry:
            comp_registry = component_registry
        elif use_shared:
            comp_registry = get_component_registry()
        else:
            comp_registry = None

        if command_registry:
            cmd_registry = command_registry
        elif use_shared:
            cmd_registry = get_command_registry()
        else:
            cmd_registry = Registry()

        # Initialize core hub functionality
        super().__init__(context, comp_registry, cmd_registry)

        # Initialize Foundation management, injecting self
        self._foundation = FoundationManager(hub=self, registry=self._component_registry)

    def xǁHubǁ__init____mutmut_12(
        self,
        context: CLIContext | None = None,
        component_registry: Registry | None = None,
        command_registry: Registry | None = None,
        use_shared_registries: bool = False,
    ) -> None:
        """Initialize the hub.

        Args:
            context: Foundation CLIContext for configuration
            component_registry: Custom component registry
            command_registry: Custom command registry
            use_shared_registries: If True, use global shared registries

        """
        # Determine if we should use shared registries
        use_shared = should_use_shared_registries(use_shared_registries, component_registry, command_registry)

        # Setup registries
        if component_registry:
            comp_registry = component_registry
        elif use_shared:
            comp_registry = get_component_registry()
        else:
            comp_registry = Registry()

        if command_registry:
            cmd_registry = None
        elif use_shared:
            cmd_registry = get_command_registry()
        else:
            cmd_registry = Registry()

        # Initialize core hub functionality
        super().__init__(context, comp_registry, cmd_registry)

        # Initialize Foundation management, injecting self
        self._foundation = FoundationManager(hub=self, registry=self._component_registry)

    def xǁHubǁ__init____mutmut_13(
        self,
        context: CLIContext | None = None,
        component_registry: Registry | None = None,
        command_registry: Registry | None = None,
        use_shared_registries: bool = False,
    ) -> None:
        """Initialize the hub.

        Args:
            context: Foundation CLIContext for configuration
            component_registry: Custom component registry
            command_registry: Custom command registry
            use_shared_registries: If True, use global shared registries

        """
        # Determine if we should use shared registries
        use_shared = should_use_shared_registries(use_shared_registries, component_registry, command_registry)

        # Setup registries
        if component_registry:
            comp_registry = component_registry
        elif use_shared:
            comp_registry = get_component_registry()
        else:
            comp_registry = Registry()

        if command_registry:
            cmd_registry = command_registry
        elif use_shared:
            cmd_registry = None
        else:
            cmd_registry = Registry()

        # Initialize core hub functionality
        super().__init__(context, comp_registry, cmd_registry)

        # Initialize Foundation management, injecting self
        self._foundation = FoundationManager(hub=self, registry=self._component_registry)

    def xǁHubǁ__init____mutmut_14(
        self,
        context: CLIContext | None = None,
        component_registry: Registry | None = None,
        command_registry: Registry | None = None,
        use_shared_registries: bool = False,
    ) -> None:
        """Initialize the hub.

        Args:
            context: Foundation CLIContext for configuration
            component_registry: Custom component registry
            command_registry: Custom command registry
            use_shared_registries: If True, use global shared registries

        """
        # Determine if we should use shared registries
        use_shared = should_use_shared_registries(use_shared_registries, component_registry, command_registry)

        # Setup registries
        if component_registry:
            comp_registry = component_registry
        elif use_shared:
            comp_registry = get_component_registry()
        else:
            comp_registry = Registry()

        if command_registry:
            cmd_registry = command_registry
        elif use_shared:
            cmd_registry = get_command_registry()
        else:
            cmd_registry = None

        # Initialize core hub functionality
        super().__init__(context, comp_registry, cmd_registry)

        # Initialize Foundation management, injecting self
        self._foundation = FoundationManager(hub=self, registry=self._component_registry)

    def xǁHubǁ__init____mutmut_15(
        self,
        context: CLIContext | None = None,
        component_registry: Registry | None = None,
        command_registry: Registry | None = None,
        use_shared_registries: bool = False,
    ) -> None:
        """Initialize the hub.

        Args:
            context: Foundation CLIContext for configuration
            component_registry: Custom component registry
            command_registry: Custom command registry
            use_shared_registries: If True, use global shared registries

        """
        # Determine if we should use shared registries
        use_shared = should_use_shared_registries(use_shared_registries, component_registry, command_registry)

        # Setup registries
        if component_registry:
            comp_registry = component_registry
        elif use_shared:
            comp_registry = get_component_registry()
        else:
            comp_registry = Registry()

        if command_registry:
            cmd_registry = command_registry
        elif use_shared:
            cmd_registry = get_command_registry()
        else:
            cmd_registry = Registry()

        # Initialize core hub functionality
        super().__init__(None, comp_registry, cmd_registry)

        # Initialize Foundation management, injecting self
        self._foundation = FoundationManager(hub=self, registry=self._component_registry)

    def xǁHubǁ__init____mutmut_16(
        self,
        context: CLIContext | None = None,
        component_registry: Registry | None = None,
        command_registry: Registry | None = None,
        use_shared_registries: bool = False,
    ) -> None:
        """Initialize the hub.

        Args:
            context: Foundation CLIContext for configuration
            component_registry: Custom component registry
            command_registry: Custom command registry
            use_shared_registries: If True, use global shared registries

        """
        # Determine if we should use shared registries
        use_shared = should_use_shared_registries(use_shared_registries, component_registry, command_registry)

        # Setup registries
        if component_registry:
            comp_registry = component_registry
        elif use_shared:
            comp_registry = get_component_registry()
        else:
            comp_registry = Registry()

        if command_registry:
            cmd_registry = command_registry
        elif use_shared:
            cmd_registry = get_command_registry()
        else:
            cmd_registry = Registry()

        # Initialize core hub functionality
        super().__init__(context, None, cmd_registry)

        # Initialize Foundation management, injecting self
        self._foundation = FoundationManager(hub=self, registry=self._component_registry)

    def xǁHubǁ__init____mutmut_17(
        self,
        context: CLIContext | None = None,
        component_registry: Registry | None = None,
        command_registry: Registry | None = None,
        use_shared_registries: bool = False,
    ) -> None:
        """Initialize the hub.

        Args:
            context: Foundation CLIContext for configuration
            component_registry: Custom component registry
            command_registry: Custom command registry
            use_shared_registries: If True, use global shared registries

        """
        # Determine if we should use shared registries
        use_shared = should_use_shared_registries(use_shared_registries, component_registry, command_registry)

        # Setup registries
        if component_registry:
            comp_registry = component_registry
        elif use_shared:
            comp_registry = get_component_registry()
        else:
            comp_registry = Registry()

        if command_registry:
            cmd_registry = command_registry
        elif use_shared:
            cmd_registry = get_command_registry()
        else:
            cmd_registry = Registry()

        # Initialize core hub functionality
        super().__init__(context, comp_registry, None)

        # Initialize Foundation management, injecting self
        self._foundation = FoundationManager(hub=self, registry=self._component_registry)

    def xǁHubǁ__init____mutmut_18(
        self,
        context: CLIContext | None = None,
        component_registry: Registry | None = None,
        command_registry: Registry | None = None,
        use_shared_registries: bool = False,
    ) -> None:
        """Initialize the hub.

        Args:
            context: Foundation CLIContext for configuration
            component_registry: Custom component registry
            command_registry: Custom command registry
            use_shared_registries: If True, use global shared registries

        """
        # Determine if we should use shared registries
        use_shared = should_use_shared_registries(use_shared_registries, component_registry, command_registry)

        # Setup registries
        if component_registry:
            comp_registry = component_registry
        elif use_shared:
            comp_registry = get_component_registry()
        else:
            comp_registry = Registry()

        if command_registry:
            cmd_registry = command_registry
        elif use_shared:
            cmd_registry = get_command_registry()
        else:
            cmd_registry = Registry()

        # Initialize core hub functionality
        super().__init__(comp_registry, cmd_registry)

        # Initialize Foundation management, injecting self
        self._foundation = FoundationManager(hub=self, registry=self._component_registry)

    def xǁHubǁ__init____mutmut_19(
        self,
        context: CLIContext | None = None,
        component_registry: Registry | None = None,
        command_registry: Registry | None = None,
        use_shared_registries: bool = False,
    ) -> None:
        """Initialize the hub.

        Args:
            context: Foundation CLIContext for configuration
            component_registry: Custom component registry
            command_registry: Custom command registry
            use_shared_registries: If True, use global shared registries

        """
        # Determine if we should use shared registries
        use_shared = should_use_shared_registries(use_shared_registries, component_registry, command_registry)

        # Setup registries
        if component_registry:
            comp_registry = component_registry
        elif use_shared:
            comp_registry = get_component_registry()
        else:
            comp_registry = Registry()

        if command_registry:
            cmd_registry = command_registry
        elif use_shared:
            cmd_registry = get_command_registry()
        else:
            cmd_registry = Registry()

        # Initialize core hub functionality
        super().__init__(context, cmd_registry)

        # Initialize Foundation management, injecting self
        self._foundation = FoundationManager(hub=self, registry=self._component_registry)

    def xǁHubǁ__init____mutmut_20(
        self,
        context: CLIContext | None = None,
        component_registry: Registry | None = None,
        command_registry: Registry | None = None,
        use_shared_registries: bool = False,
    ) -> None:
        """Initialize the hub.

        Args:
            context: Foundation CLIContext for configuration
            component_registry: Custom component registry
            command_registry: Custom command registry
            use_shared_registries: If True, use global shared registries

        """
        # Determine if we should use shared registries
        use_shared = should_use_shared_registries(use_shared_registries, component_registry, command_registry)

        # Setup registries
        if component_registry:
            comp_registry = component_registry
        elif use_shared:
            comp_registry = get_component_registry()
        else:
            comp_registry = Registry()

        if command_registry:
            cmd_registry = command_registry
        elif use_shared:
            cmd_registry = get_command_registry()
        else:
            cmd_registry = Registry()

        # Initialize core hub functionality
        super().__init__(
            context,
            comp_registry,
        )

        # Initialize Foundation management, injecting self
        self._foundation = FoundationManager(hub=self, registry=self._component_registry)

    def xǁHubǁ__init____mutmut_21(
        self,
        context: CLIContext | None = None,
        component_registry: Registry | None = None,
        command_registry: Registry | None = None,
        use_shared_registries: bool = False,
    ) -> None:
        """Initialize the hub.

        Args:
            context: Foundation CLIContext for configuration
            component_registry: Custom component registry
            command_registry: Custom command registry
            use_shared_registries: If True, use global shared registries

        """
        # Determine if we should use shared registries
        use_shared = should_use_shared_registries(use_shared_registries, component_registry, command_registry)

        # Setup registries
        if component_registry:
            comp_registry = component_registry
        elif use_shared:
            comp_registry = get_component_registry()
        else:
            comp_registry = Registry()

        if command_registry:
            cmd_registry = command_registry
        elif use_shared:
            cmd_registry = get_command_registry()
        else:
            cmd_registry = Registry()

        # Initialize core hub functionality
        super().__init__(context, comp_registry, cmd_registry)

        # Initialize Foundation management, injecting self
        self._foundation = None

    def xǁHubǁ__init____mutmut_22(
        self,
        context: CLIContext | None = None,
        component_registry: Registry | None = None,
        command_registry: Registry | None = None,
        use_shared_registries: bool = False,
    ) -> None:
        """Initialize the hub.

        Args:
            context: Foundation CLIContext for configuration
            component_registry: Custom component registry
            command_registry: Custom command registry
            use_shared_registries: If True, use global shared registries

        """
        # Determine if we should use shared registries
        use_shared = should_use_shared_registries(use_shared_registries, component_registry, command_registry)

        # Setup registries
        if component_registry:
            comp_registry = component_registry
        elif use_shared:
            comp_registry = get_component_registry()
        else:
            comp_registry = Registry()

        if command_registry:
            cmd_registry = command_registry
        elif use_shared:
            cmd_registry = get_command_registry()
        else:
            cmd_registry = Registry()

        # Initialize core hub functionality
        super().__init__(context, comp_registry, cmd_registry)

        # Initialize Foundation management, injecting self
        self._foundation = FoundationManager(hub=None, registry=self._component_registry)

    def xǁHubǁ__init____mutmut_23(
        self,
        context: CLIContext | None = None,
        component_registry: Registry | None = None,
        command_registry: Registry | None = None,
        use_shared_registries: bool = False,
    ) -> None:
        """Initialize the hub.

        Args:
            context: Foundation CLIContext for configuration
            component_registry: Custom component registry
            command_registry: Custom command registry
            use_shared_registries: If True, use global shared registries

        """
        # Determine if we should use shared registries
        use_shared = should_use_shared_registries(use_shared_registries, component_registry, command_registry)

        # Setup registries
        if component_registry:
            comp_registry = component_registry
        elif use_shared:
            comp_registry = get_component_registry()
        else:
            comp_registry = Registry()

        if command_registry:
            cmd_registry = command_registry
        elif use_shared:
            cmd_registry = get_command_registry()
        else:
            cmd_registry = Registry()

        # Initialize core hub functionality
        super().__init__(context, comp_registry, cmd_registry)

        # Initialize Foundation management, injecting self
        self._foundation = FoundationManager(hub=self, registry=None)

    def xǁHubǁ__init____mutmut_24(
        self,
        context: CLIContext | None = None,
        component_registry: Registry | None = None,
        command_registry: Registry | None = None,
        use_shared_registries: bool = False,
    ) -> None:
        """Initialize the hub.

        Args:
            context: Foundation CLIContext for configuration
            component_registry: Custom component registry
            command_registry: Custom command registry
            use_shared_registries: If True, use global shared registries

        """
        # Determine if we should use shared registries
        use_shared = should_use_shared_registries(use_shared_registries, component_registry, command_registry)

        # Setup registries
        if component_registry:
            comp_registry = component_registry
        elif use_shared:
            comp_registry = get_component_registry()
        else:
            comp_registry = Registry()

        if command_registry:
            cmd_registry = command_registry
        elif use_shared:
            cmd_registry = get_command_registry()
        else:
            cmd_registry = Registry()

        # Initialize core hub functionality
        super().__init__(context, comp_registry, cmd_registry)

        # Initialize Foundation management, injecting self
        self._foundation = FoundationManager(registry=self._component_registry)

    def xǁHubǁ__init____mutmut_25(
        self,
        context: CLIContext | None = None,
        component_registry: Registry | None = None,
        command_registry: Registry | None = None,
        use_shared_registries: bool = False,
    ) -> None:
        """Initialize the hub.

        Args:
            context: Foundation CLIContext for configuration
            component_registry: Custom component registry
            command_registry: Custom command registry
            use_shared_registries: If True, use global shared registries

        """
        # Determine if we should use shared registries
        use_shared = should_use_shared_registries(use_shared_registries, component_registry, command_registry)

        # Setup registries
        if component_registry:
            comp_registry = component_registry
        elif use_shared:
            comp_registry = get_component_registry()
        else:
            comp_registry = Registry()

        if command_registry:
            cmd_registry = command_registry
        elif use_shared:
            cmd_registry = get_command_registry()
        else:
            cmd_registry = Registry()

        # Initialize core hub functionality
        super().__init__(context, comp_registry, cmd_registry)

        # Initialize Foundation management, injecting self
        self._foundation = FoundationManager(
            hub=self,
        )

    xǁHubǁ__init____mutmut_mutants: ClassVar[MutantDict] = {
        "xǁHubǁ__init____mutmut_1": xǁHubǁ__init____mutmut_1,
        "xǁHubǁ__init____mutmut_2": xǁHubǁ__init____mutmut_2,
        "xǁHubǁ__init____mutmut_3": xǁHubǁ__init____mutmut_3,
        "xǁHubǁ__init____mutmut_4": xǁHubǁ__init____mutmut_4,
        "xǁHubǁ__init____mutmut_5": xǁHubǁ__init____mutmut_5,
        "xǁHubǁ__init____mutmut_6": xǁHubǁ__init____mutmut_6,
        "xǁHubǁ__init____mutmut_7": xǁHubǁ__init____mutmut_7,
        "xǁHubǁ__init____mutmut_8": xǁHubǁ__init____mutmut_8,
        "xǁHubǁ__init____mutmut_9": xǁHubǁ__init____mutmut_9,
        "xǁHubǁ__init____mutmut_10": xǁHubǁ__init____mutmut_10,
        "xǁHubǁ__init____mutmut_11": xǁHubǁ__init____mutmut_11,
        "xǁHubǁ__init____mutmut_12": xǁHubǁ__init____mutmut_12,
        "xǁHubǁ__init____mutmut_13": xǁHubǁ__init____mutmut_13,
        "xǁHubǁ__init____mutmut_14": xǁHubǁ__init____mutmut_14,
        "xǁHubǁ__init____mutmut_15": xǁHubǁ__init____mutmut_15,
        "xǁHubǁ__init____mutmut_16": xǁHubǁ__init____mutmut_16,
        "xǁHubǁ__init____mutmut_17": xǁHubǁ__init____mutmut_17,
        "xǁHubǁ__init____mutmut_18": xǁHubǁ__init____mutmut_18,
        "xǁHubǁ__init____mutmut_19": xǁHubǁ__init____mutmut_19,
        "xǁHubǁ__init____mutmut_20": xǁHubǁ__init____mutmut_20,
        "xǁHubǁ__init____mutmut_21": xǁHubǁ__init____mutmut_21,
        "xǁHubǁ__init____mutmut_22": xǁHubǁ__init____mutmut_22,
        "xǁHubǁ__init____mutmut_23": xǁHubǁ__init____mutmut_23,
        "xǁHubǁ__init____mutmut_24": xǁHubǁ__init____mutmut_24,
        "xǁHubǁ__init____mutmut_25": xǁHubǁ__init____mutmut_25,
    }

    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁHubǁ__init____mutmut_orig"),
            object.__getattribute__(self, "xǁHubǁ__init____mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    __init__.__signature__ = _mutmut_signature(xǁHubǁ__init____mutmut_orig)
    xǁHubǁ__init____mutmut_orig.__name__ = "xǁHubǁ__init__"

    # Foundation Integration Methods

    def xǁHubǁinitialize_foundation__mutmut_orig(self, config: Any = None, force: bool = False) -> None:
        """Initialize Foundation system through Hub.

        Single initialization method replacing all setup_* functions.
        Thread-safe and idempotent, unless force=True.

        Args:
            config: Optional TelemetryConfig (defaults to from_env)
            force: If True, force re-initialization even if already initialized

        """
        self._foundation.initialize_foundation(config, force)

    # Foundation Integration Methods

    def xǁHubǁinitialize_foundation__mutmut_1(self, config: Any = None, force: bool = True) -> None:
        """Initialize Foundation system through Hub.

        Single initialization method replacing all setup_* functions.
        Thread-safe and idempotent, unless force=True.

        Args:
            config: Optional TelemetryConfig (defaults to from_env)
            force: If True, force re-initialization even if already initialized

        """
        self._foundation.initialize_foundation(config, force)

    # Foundation Integration Methods

    def xǁHubǁinitialize_foundation__mutmut_2(self, config: Any = None, force: bool = False) -> None:
        """Initialize Foundation system through Hub.

        Single initialization method replacing all setup_* functions.
        Thread-safe and idempotent, unless force=True.

        Args:
            config: Optional TelemetryConfig (defaults to from_env)
            force: If True, force re-initialization even if already initialized

        """
        self._foundation.initialize_foundation(None, force)

    # Foundation Integration Methods

    def xǁHubǁinitialize_foundation__mutmut_3(self, config: Any = None, force: bool = False) -> None:
        """Initialize Foundation system through Hub.

        Single initialization method replacing all setup_* functions.
        Thread-safe and idempotent, unless force=True.

        Args:
            config: Optional TelemetryConfig (defaults to from_env)
            force: If True, force re-initialization even if already initialized

        """
        self._foundation.initialize_foundation(config, None)

    # Foundation Integration Methods

    def xǁHubǁinitialize_foundation__mutmut_4(self, config: Any = None, force: bool = False) -> None:
        """Initialize Foundation system through Hub.

        Single initialization method replacing all setup_* functions.
        Thread-safe and idempotent, unless force=True.

        Args:
            config: Optional TelemetryConfig (defaults to from_env)
            force: If True, force re-initialization even if already initialized

        """
        self._foundation.initialize_foundation(force)

    # Foundation Integration Methods

    def xǁHubǁinitialize_foundation__mutmut_5(self, config: Any = None, force: bool = False) -> None:
        """Initialize Foundation system through Hub.

        Single initialization method replacing all setup_* functions.
        Thread-safe and idempotent, unless force=True.

        Args:
            config: Optional TelemetryConfig (defaults to from_env)
            force: If True, force re-initialization even if already initialized

        """
        self._foundation.initialize_foundation(
            config,
        )

    xǁHubǁinitialize_foundation__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁHubǁinitialize_foundation__mutmut_1": xǁHubǁinitialize_foundation__mutmut_1,
        "xǁHubǁinitialize_foundation__mutmut_2": xǁHubǁinitialize_foundation__mutmut_2,
        "xǁHubǁinitialize_foundation__mutmut_3": xǁHubǁinitialize_foundation__mutmut_3,
        "xǁHubǁinitialize_foundation__mutmut_4": xǁHubǁinitialize_foundation__mutmut_4,
        "xǁHubǁinitialize_foundation__mutmut_5": xǁHubǁinitialize_foundation__mutmut_5,
    }

    def initialize_foundation(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁHubǁinitialize_foundation__mutmut_orig"),
            object.__getattribute__(self, "xǁHubǁinitialize_foundation__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    initialize_foundation.__signature__ = _mutmut_signature(xǁHubǁinitialize_foundation__mutmut_orig)
    xǁHubǁinitialize_foundation__mutmut_orig.__name__ = "xǁHubǁinitialize_foundation"

    def xǁHubǁget_foundation_logger__mutmut_orig(self, name: str | None = None) -> Any:
        """Get Foundation logger instance through Hub.

        Auto-initializes Foundation if not already done.
        Thread-safe with fallback behavior.

        Args:
            name: Logger name (e.g., module name)

        Returns:
            Configured logger instance

        """
        return self._foundation.get_foundation_logger(name)

    def xǁHubǁget_foundation_logger__mutmut_1(self, name: str | None = None) -> Any:
        """Get Foundation logger instance through Hub.

        Auto-initializes Foundation if not already done.
        Thread-safe with fallback behavior.

        Args:
            name: Logger name (e.g., module name)

        Returns:
            Configured logger instance

        """
        return self._foundation.get_foundation_logger(None)

    xǁHubǁget_foundation_logger__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁHubǁget_foundation_logger__mutmut_1": xǁHubǁget_foundation_logger__mutmut_1
    }

    def get_foundation_logger(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁHubǁget_foundation_logger__mutmut_orig"),
            object.__getattribute__(self, "xǁHubǁget_foundation_logger__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    get_foundation_logger.__signature__ = _mutmut_signature(xǁHubǁget_foundation_logger__mutmut_orig)
    xǁHubǁget_foundation_logger__mutmut_orig.__name__ = "xǁHubǁget_foundation_logger"

    def is_foundation_initialized(self) -> bool:
        """Check if Foundation system is initialized."""
        return self._foundation.is_foundation_initialized()

    def get_foundation_config(self) -> Any | None:
        """Get the current Foundation configuration."""
        return self._foundation.get_foundation_config()

    def xǁHubǁclear__mutmut_orig(self, dimension: str | None = None) -> None:
        """Clear registrations and dispose of resources properly.

        Args:
            dimension: Optional dimension to clear (None = all)

        """
        # Clear core hub registrations (this will now dispose resources)
        super().clear(dimension)

        # Reset Foundation state when clearing all or foundation-specific dimensions
        if dimension is None or dimension in ("singleton", "foundation"):
            self._foundation.clear_foundation_state()

    def xǁHubǁclear__mutmut_1(self, dimension: str | None = None) -> None:
        """Clear registrations and dispose of resources properly.

        Args:
            dimension: Optional dimension to clear (None = all)

        """
        # Clear core hub registrations (this will now dispose resources)
        super().clear(None)

        # Reset Foundation state when clearing all or foundation-specific dimensions
        if dimension is None or dimension in ("singleton", "foundation"):
            self._foundation.clear_foundation_state()

    def xǁHubǁclear__mutmut_2(self, dimension: str | None = None) -> None:
        """Clear registrations and dispose of resources properly.

        Args:
            dimension: Optional dimension to clear (None = all)

        """
        # Clear core hub registrations (this will now dispose resources)
        super().clear(dimension)

        # Reset Foundation state when clearing all or foundation-specific dimensions
        if dimension is None and dimension in ("singleton", "foundation"):
            self._foundation.clear_foundation_state()

    def xǁHubǁclear__mutmut_3(self, dimension: str | None = None) -> None:
        """Clear registrations and dispose of resources properly.

        Args:
            dimension: Optional dimension to clear (None = all)

        """
        # Clear core hub registrations (this will now dispose resources)
        super().clear(dimension)

        # Reset Foundation state when clearing all or foundation-specific dimensions
        if dimension is not None or dimension in ("singleton", "foundation"):
            self._foundation.clear_foundation_state()

    def xǁHubǁclear__mutmut_4(self, dimension: str | None = None) -> None:
        """Clear registrations and dispose of resources properly.

        Args:
            dimension: Optional dimension to clear (None = all)

        """
        # Clear core hub registrations (this will now dispose resources)
        super().clear(dimension)

        # Reset Foundation state when clearing all or foundation-specific dimensions
        if dimension is None or dimension not in ("singleton", "foundation"):
            self._foundation.clear_foundation_state()

    def xǁHubǁclear__mutmut_5(self, dimension: str | None = None) -> None:
        """Clear registrations and dispose of resources properly.

        Args:
            dimension: Optional dimension to clear (None = all)

        """
        # Clear core hub registrations (this will now dispose resources)
        super().clear(dimension)

        # Reset Foundation state when clearing all or foundation-specific dimensions
        if dimension is None or dimension in ("XXsingletonXX", "foundation"):
            self._foundation.clear_foundation_state()

    def xǁHubǁclear__mutmut_6(self, dimension: str | None = None) -> None:
        """Clear registrations and dispose of resources properly.

        Args:
            dimension: Optional dimension to clear (None = all)

        """
        # Clear core hub registrations (this will now dispose resources)
        super().clear(dimension)

        # Reset Foundation state when clearing all or foundation-specific dimensions
        if dimension is None or dimension in ("SINGLETON", "foundation"):
            self._foundation.clear_foundation_state()

    def xǁHubǁclear__mutmut_7(self, dimension: str | None = None) -> None:
        """Clear registrations and dispose of resources properly.

        Args:
            dimension: Optional dimension to clear (None = all)

        """
        # Clear core hub registrations (this will now dispose resources)
        super().clear(dimension)

        # Reset Foundation state when clearing all or foundation-specific dimensions
        if dimension is None or dimension in ("singleton", "XXfoundationXX"):
            self._foundation.clear_foundation_state()

    def xǁHubǁclear__mutmut_8(self, dimension: str | None = None) -> None:
        """Clear registrations and dispose of resources properly.

        Args:
            dimension: Optional dimension to clear (None = all)

        """
        # Clear core hub registrations (this will now dispose resources)
        super().clear(dimension)

        # Reset Foundation state when clearing all or foundation-specific dimensions
        if dimension is None or dimension in ("singleton", "FOUNDATION"):
            self._foundation.clear_foundation_state()

    xǁHubǁclear__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁHubǁclear__mutmut_1": xǁHubǁclear__mutmut_1,
        "xǁHubǁclear__mutmut_2": xǁHubǁclear__mutmut_2,
        "xǁHubǁclear__mutmut_3": xǁHubǁclear__mutmut_3,
        "xǁHubǁclear__mutmut_4": xǁHubǁclear__mutmut_4,
        "xǁHubǁclear__mutmut_5": xǁHubǁclear__mutmut_5,
        "xǁHubǁclear__mutmut_6": xǁHubǁclear__mutmut_6,
        "xǁHubǁclear__mutmut_7": xǁHubǁclear__mutmut_7,
        "xǁHubǁclear__mutmut_8": xǁHubǁclear__mutmut_8,
    }

    def clear(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁHubǁclear__mutmut_orig"),
            object.__getattribute__(self, "xǁHubǁclear__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    clear.__signature__ = _mutmut_signature(xǁHubǁclear__mutmut_orig)
    xǁHubǁclear__mutmut_orig.__name__ = "xǁHubǁclear"

    def xǁHubǁdispose_all__mutmut_orig(self) -> None:
        """Dispose of all managed resources without clearing registrations."""
        self._component_registry.dispose_all()
        if hasattr(self._command_registry, "dispose_all"):
            self._command_registry.dispose_all()

    def xǁHubǁdispose_all__mutmut_1(self) -> None:
        """Dispose of all managed resources without clearing registrations."""
        self._component_registry.dispose_all()
        if hasattr(None, "dispose_all"):
            self._command_registry.dispose_all()

    def xǁHubǁdispose_all__mutmut_2(self) -> None:
        """Dispose of all managed resources without clearing registrations."""
        self._component_registry.dispose_all()
        if hasattr(self._command_registry, None):
            self._command_registry.dispose_all()

    def xǁHubǁdispose_all__mutmut_3(self) -> None:
        """Dispose of all managed resources without clearing registrations."""
        self._component_registry.dispose_all()
        if hasattr("dispose_all"):
            self._command_registry.dispose_all()

    def xǁHubǁdispose_all__mutmut_4(self) -> None:
        """Dispose of all managed resources without clearing registrations."""
        self._component_registry.dispose_all()
        if hasattr(
            self._command_registry,
        ):
            self._command_registry.dispose_all()

    def xǁHubǁdispose_all__mutmut_5(self) -> None:
        """Dispose of all managed resources without clearing registrations."""
        self._component_registry.dispose_all()
        if hasattr(self._command_registry, "XXdispose_allXX"):
            self._command_registry.dispose_all()

    def xǁHubǁdispose_all__mutmut_6(self) -> None:
        """Dispose of all managed resources without clearing registrations."""
        self._component_registry.dispose_all()
        if hasattr(self._command_registry, "DISPOSE_ALL"):
            self._command_registry.dispose_all()

    xǁHubǁdispose_all__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁHubǁdispose_all__mutmut_1": xǁHubǁdispose_all__mutmut_1,
        "xǁHubǁdispose_all__mutmut_2": xǁHubǁdispose_all__mutmut_2,
        "xǁHubǁdispose_all__mutmut_3": xǁHubǁdispose_all__mutmut_3,
        "xǁHubǁdispose_all__mutmut_4": xǁHubǁdispose_all__mutmut_4,
        "xǁHubǁdispose_all__mutmut_5": xǁHubǁdispose_all__mutmut_5,
        "xǁHubǁdispose_all__mutmut_6": xǁHubǁdispose_all__mutmut_6,
    }

    def dispose_all(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁHubǁdispose_all__mutmut_orig"),
            object.__getattribute__(self, "xǁHubǁdispose_all__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    dispose_all.__signature__ = _mutmut_signature(xǁHubǁdispose_all__mutmut_orig)
    xǁHubǁdispose_all__mutmut_orig.__name__ = "xǁHubǁdispose_all"


# Global hub instance for thread-safe singleton initialization
_global_hub: Hub | None = None


def x_get_hub__mutmut_orig() -> Hub:
    """Get the global shared hub instance (singleton pattern).

    This function acts as the Composition Root for the global singleton instance.
    It is maintained for backward compatibility and convenience.

    **Note:** For building testable and maintainable applications, the recommended
    approach is to use a `Container` or `Hub` instance created at your application's
    entry point for explicit dependency management. This global accessor should be
    avoided in application code.

    Thread-safe: Uses double-checked locking pattern for efficient lazy initialization.

    **Auto-Initialization Behavior:**
    This function automatically initializes the Foundation system on first access.
    The initialization is:
    - **Idempotent**: Safe to call multiple times
    - **Thread-safe**: Uses lock manager for coordination
    - **Lazy**: Only happens on first access

    Returns:
        Global Hub instance (created and initialized if needed)

    Example:
        >>> hub = get_hub()
        >>> hub.register_command("my_command", my_function)

    Note:
        For isolated Hub instances (testing, advanced use cases), use:
        >>> hub = Hub(use_shared_registries=False)

    """
    global _global_hub

    # Fast path: hub already initialized
    if _global_hub is not None:
        return _global_hub

    # Slow path: need to initialize hub
    with get_lock_manager().acquire("foundation.hub.init"):
        # Double-check after acquiring lock
        if _global_hub is None:
            # Global hub uses shared registries by default
            _global_hub = Hub(use_shared_registries=True)

            # Auto-initialize Foundation on first hub access
            _global_hub.initialize_foundation()

            # Bootstrap foundation components now that hub is ready (skip in test mode)
            from provide.foundation.testmode.detection import is_in_test_mode

            if not is_in_test_mode():
                try:
                    from provide.foundation.hub.components import bootstrap_foundation

                    bootstrap_foundation()
                except ImportError:
                    # Bootstrap function might not exist yet, that's okay
                    pass

    return _global_hub


def x_get_hub__mutmut_1() -> Hub:
    """Get the global shared hub instance (singleton pattern).

    This function acts as the Composition Root for the global singleton instance.
    It is maintained for backward compatibility and convenience.

    **Note:** For building testable and maintainable applications, the recommended
    approach is to use a `Container` or `Hub` instance created at your application's
    entry point for explicit dependency management. This global accessor should be
    avoided in application code.

    Thread-safe: Uses double-checked locking pattern for efficient lazy initialization.

    **Auto-Initialization Behavior:**
    This function automatically initializes the Foundation system on first access.
    The initialization is:
    - **Idempotent**: Safe to call multiple times
    - **Thread-safe**: Uses lock manager for coordination
    - **Lazy**: Only happens on first access

    Returns:
        Global Hub instance (created and initialized if needed)

    Example:
        >>> hub = get_hub()
        >>> hub.register_command("my_command", my_function)

    Note:
        For isolated Hub instances (testing, advanced use cases), use:
        >>> hub = Hub(use_shared_registries=False)

    """
    global _global_hub

    # Fast path: hub already initialized
    if _global_hub is None:
        return _global_hub

    # Slow path: need to initialize hub
    with get_lock_manager().acquire("foundation.hub.init"):
        # Double-check after acquiring lock
        if _global_hub is None:
            # Global hub uses shared registries by default
            _global_hub = Hub(use_shared_registries=True)

            # Auto-initialize Foundation on first hub access
            _global_hub.initialize_foundation()

            # Bootstrap foundation components now that hub is ready (skip in test mode)
            from provide.foundation.testmode.detection import is_in_test_mode

            if not is_in_test_mode():
                try:
                    from provide.foundation.hub.components import bootstrap_foundation

                    bootstrap_foundation()
                except ImportError:
                    # Bootstrap function might not exist yet, that's okay
                    pass

    return _global_hub


def x_get_hub__mutmut_2() -> Hub:
    """Get the global shared hub instance (singleton pattern).

    This function acts as the Composition Root for the global singleton instance.
    It is maintained for backward compatibility and convenience.

    **Note:** For building testable and maintainable applications, the recommended
    approach is to use a `Container` or `Hub` instance created at your application's
    entry point for explicit dependency management. This global accessor should be
    avoided in application code.

    Thread-safe: Uses double-checked locking pattern for efficient lazy initialization.

    **Auto-Initialization Behavior:**
    This function automatically initializes the Foundation system on first access.
    The initialization is:
    - **Idempotent**: Safe to call multiple times
    - **Thread-safe**: Uses lock manager for coordination
    - **Lazy**: Only happens on first access

    Returns:
        Global Hub instance (created and initialized if needed)

    Example:
        >>> hub = get_hub()
        >>> hub.register_command("my_command", my_function)

    Note:
        For isolated Hub instances (testing, advanced use cases), use:
        >>> hub = Hub(use_shared_registries=False)

    """
    global _global_hub

    # Fast path: hub already initialized
    if _global_hub is not None:
        return _global_hub

    # Slow path: need to initialize hub
    with get_lock_manager().acquire(None):
        # Double-check after acquiring lock
        if _global_hub is None:
            # Global hub uses shared registries by default
            _global_hub = Hub(use_shared_registries=True)

            # Auto-initialize Foundation on first hub access
            _global_hub.initialize_foundation()

            # Bootstrap foundation components now that hub is ready (skip in test mode)
            from provide.foundation.testmode.detection import is_in_test_mode

            if not is_in_test_mode():
                try:
                    from provide.foundation.hub.components import bootstrap_foundation

                    bootstrap_foundation()
                except ImportError:
                    # Bootstrap function might not exist yet, that's okay
                    pass

    return _global_hub


def x_get_hub__mutmut_3() -> Hub:
    """Get the global shared hub instance (singleton pattern).

    This function acts as the Composition Root for the global singleton instance.
    It is maintained for backward compatibility and convenience.

    **Note:** For building testable and maintainable applications, the recommended
    approach is to use a `Container` or `Hub` instance created at your application's
    entry point for explicit dependency management. This global accessor should be
    avoided in application code.

    Thread-safe: Uses double-checked locking pattern for efficient lazy initialization.

    **Auto-Initialization Behavior:**
    This function automatically initializes the Foundation system on first access.
    The initialization is:
    - **Idempotent**: Safe to call multiple times
    - **Thread-safe**: Uses lock manager for coordination
    - **Lazy**: Only happens on first access

    Returns:
        Global Hub instance (created and initialized if needed)

    Example:
        >>> hub = get_hub()
        >>> hub.register_command("my_command", my_function)

    Note:
        For isolated Hub instances (testing, advanced use cases), use:
        >>> hub = Hub(use_shared_registries=False)

    """
    global _global_hub

    # Fast path: hub already initialized
    if _global_hub is not None:
        return _global_hub

    # Slow path: need to initialize hub
    with get_lock_manager().acquire("XXfoundation.hub.initXX"):
        # Double-check after acquiring lock
        if _global_hub is None:
            # Global hub uses shared registries by default
            _global_hub = Hub(use_shared_registries=True)

            # Auto-initialize Foundation on first hub access
            _global_hub.initialize_foundation()

            # Bootstrap foundation components now that hub is ready (skip in test mode)
            from provide.foundation.testmode.detection import is_in_test_mode

            if not is_in_test_mode():
                try:
                    from provide.foundation.hub.components import bootstrap_foundation

                    bootstrap_foundation()
                except ImportError:
                    # Bootstrap function might not exist yet, that's okay
                    pass

    return _global_hub


def x_get_hub__mutmut_4() -> Hub:
    """Get the global shared hub instance (singleton pattern).

    This function acts as the Composition Root for the global singleton instance.
    It is maintained for backward compatibility and convenience.

    **Note:** For building testable and maintainable applications, the recommended
    approach is to use a `Container` or `Hub` instance created at your application's
    entry point for explicit dependency management. This global accessor should be
    avoided in application code.

    Thread-safe: Uses double-checked locking pattern for efficient lazy initialization.

    **Auto-Initialization Behavior:**
    This function automatically initializes the Foundation system on first access.
    The initialization is:
    - **Idempotent**: Safe to call multiple times
    - **Thread-safe**: Uses lock manager for coordination
    - **Lazy**: Only happens on first access

    Returns:
        Global Hub instance (created and initialized if needed)

    Example:
        >>> hub = get_hub()
        >>> hub.register_command("my_command", my_function)

    Note:
        For isolated Hub instances (testing, advanced use cases), use:
        >>> hub = Hub(use_shared_registries=False)

    """
    global _global_hub

    # Fast path: hub already initialized
    if _global_hub is not None:
        return _global_hub

    # Slow path: need to initialize hub
    with get_lock_manager().acquire("FOUNDATION.HUB.INIT"):
        # Double-check after acquiring lock
        if _global_hub is None:
            # Global hub uses shared registries by default
            _global_hub = Hub(use_shared_registries=True)

            # Auto-initialize Foundation on first hub access
            _global_hub.initialize_foundation()

            # Bootstrap foundation components now that hub is ready (skip in test mode)
            from provide.foundation.testmode.detection import is_in_test_mode

            if not is_in_test_mode():
                try:
                    from provide.foundation.hub.components import bootstrap_foundation

                    bootstrap_foundation()
                except ImportError:
                    # Bootstrap function might not exist yet, that's okay
                    pass

    return _global_hub


def x_get_hub__mutmut_5() -> Hub:
    """Get the global shared hub instance (singleton pattern).

    This function acts as the Composition Root for the global singleton instance.
    It is maintained for backward compatibility and convenience.

    **Note:** For building testable and maintainable applications, the recommended
    approach is to use a `Container` or `Hub` instance created at your application's
    entry point for explicit dependency management. This global accessor should be
    avoided in application code.

    Thread-safe: Uses double-checked locking pattern for efficient lazy initialization.

    **Auto-Initialization Behavior:**
    This function automatically initializes the Foundation system on first access.
    The initialization is:
    - **Idempotent**: Safe to call multiple times
    - **Thread-safe**: Uses lock manager for coordination
    - **Lazy**: Only happens on first access

    Returns:
        Global Hub instance (created and initialized if needed)

    Example:
        >>> hub = get_hub()
        >>> hub.register_command("my_command", my_function)

    Note:
        For isolated Hub instances (testing, advanced use cases), use:
        >>> hub = Hub(use_shared_registries=False)

    """
    global _global_hub

    # Fast path: hub already initialized
    if _global_hub is not None:
        return _global_hub

    # Slow path: need to initialize hub
    with get_lock_manager().acquire("foundation.hub.init"):
        # Double-check after acquiring lock
        if _global_hub is not None:
            # Global hub uses shared registries by default
            _global_hub = Hub(use_shared_registries=True)

            # Auto-initialize Foundation on first hub access
            _global_hub.initialize_foundation()

            # Bootstrap foundation components now that hub is ready (skip in test mode)
            from provide.foundation.testmode.detection import is_in_test_mode

            if not is_in_test_mode():
                try:
                    from provide.foundation.hub.components import bootstrap_foundation

                    bootstrap_foundation()
                except ImportError:
                    # Bootstrap function might not exist yet, that's okay
                    pass

    return _global_hub


def x_get_hub__mutmut_6() -> Hub:
    """Get the global shared hub instance (singleton pattern).

    This function acts as the Composition Root for the global singleton instance.
    It is maintained for backward compatibility and convenience.

    **Note:** For building testable and maintainable applications, the recommended
    approach is to use a `Container` or `Hub` instance created at your application's
    entry point for explicit dependency management. This global accessor should be
    avoided in application code.

    Thread-safe: Uses double-checked locking pattern for efficient lazy initialization.

    **Auto-Initialization Behavior:**
    This function automatically initializes the Foundation system on first access.
    The initialization is:
    - **Idempotent**: Safe to call multiple times
    - **Thread-safe**: Uses lock manager for coordination
    - **Lazy**: Only happens on first access

    Returns:
        Global Hub instance (created and initialized if needed)

    Example:
        >>> hub = get_hub()
        >>> hub.register_command("my_command", my_function)

    Note:
        For isolated Hub instances (testing, advanced use cases), use:
        >>> hub = Hub(use_shared_registries=False)

    """
    global _global_hub

    # Fast path: hub already initialized
    if _global_hub is not None:
        return _global_hub

    # Slow path: need to initialize hub
    with get_lock_manager().acquire("foundation.hub.init"):
        # Double-check after acquiring lock
        if _global_hub is None:
            # Global hub uses shared registries by default
            _global_hub = None

            # Auto-initialize Foundation on first hub access
            _global_hub.initialize_foundation()

            # Bootstrap foundation components now that hub is ready (skip in test mode)
            from provide.foundation.testmode.detection import is_in_test_mode

            if not is_in_test_mode():
                try:
                    from provide.foundation.hub.components import bootstrap_foundation

                    bootstrap_foundation()
                except ImportError:
                    # Bootstrap function might not exist yet, that's okay
                    pass

    return _global_hub


def x_get_hub__mutmut_7() -> Hub:
    """Get the global shared hub instance (singleton pattern).

    This function acts as the Composition Root for the global singleton instance.
    It is maintained for backward compatibility and convenience.

    **Note:** For building testable and maintainable applications, the recommended
    approach is to use a `Container` or `Hub` instance created at your application's
    entry point for explicit dependency management. This global accessor should be
    avoided in application code.

    Thread-safe: Uses double-checked locking pattern for efficient lazy initialization.

    **Auto-Initialization Behavior:**
    This function automatically initializes the Foundation system on first access.
    The initialization is:
    - **Idempotent**: Safe to call multiple times
    - **Thread-safe**: Uses lock manager for coordination
    - **Lazy**: Only happens on first access

    Returns:
        Global Hub instance (created and initialized if needed)

    Example:
        >>> hub = get_hub()
        >>> hub.register_command("my_command", my_function)

    Note:
        For isolated Hub instances (testing, advanced use cases), use:
        >>> hub = Hub(use_shared_registries=False)

    """
    global _global_hub

    # Fast path: hub already initialized
    if _global_hub is not None:
        return _global_hub

    # Slow path: need to initialize hub
    with get_lock_manager().acquire("foundation.hub.init"):
        # Double-check after acquiring lock
        if _global_hub is None:
            # Global hub uses shared registries by default
            _global_hub = Hub(use_shared_registries=None)

            # Auto-initialize Foundation on first hub access
            _global_hub.initialize_foundation()

            # Bootstrap foundation components now that hub is ready (skip in test mode)
            from provide.foundation.testmode.detection import is_in_test_mode

            if not is_in_test_mode():
                try:
                    from provide.foundation.hub.components import bootstrap_foundation

                    bootstrap_foundation()
                except ImportError:
                    # Bootstrap function might not exist yet, that's okay
                    pass

    return _global_hub


def x_get_hub__mutmut_8() -> Hub:
    """Get the global shared hub instance (singleton pattern).

    This function acts as the Composition Root for the global singleton instance.
    It is maintained for backward compatibility and convenience.

    **Note:** For building testable and maintainable applications, the recommended
    approach is to use a `Container` or `Hub` instance created at your application's
    entry point for explicit dependency management. This global accessor should be
    avoided in application code.

    Thread-safe: Uses double-checked locking pattern for efficient lazy initialization.

    **Auto-Initialization Behavior:**
    This function automatically initializes the Foundation system on first access.
    The initialization is:
    - **Idempotent**: Safe to call multiple times
    - **Thread-safe**: Uses lock manager for coordination
    - **Lazy**: Only happens on first access

    Returns:
        Global Hub instance (created and initialized if needed)

    Example:
        >>> hub = get_hub()
        >>> hub.register_command("my_command", my_function)

    Note:
        For isolated Hub instances (testing, advanced use cases), use:
        >>> hub = Hub(use_shared_registries=False)

    """
    global _global_hub

    # Fast path: hub already initialized
    if _global_hub is not None:
        return _global_hub

    # Slow path: need to initialize hub
    with get_lock_manager().acquire("foundation.hub.init"):
        # Double-check after acquiring lock
        if _global_hub is None:
            # Global hub uses shared registries by default
            _global_hub = Hub(use_shared_registries=False)

            # Auto-initialize Foundation on first hub access
            _global_hub.initialize_foundation()

            # Bootstrap foundation components now that hub is ready (skip in test mode)
            from provide.foundation.testmode.detection import is_in_test_mode

            if not is_in_test_mode():
                try:
                    from provide.foundation.hub.components import bootstrap_foundation

                    bootstrap_foundation()
                except ImportError:
                    # Bootstrap function might not exist yet, that's okay
                    pass

    return _global_hub


def x_get_hub__mutmut_9() -> Hub:
    """Get the global shared hub instance (singleton pattern).

    This function acts as the Composition Root for the global singleton instance.
    It is maintained for backward compatibility and convenience.

    **Note:** For building testable and maintainable applications, the recommended
    approach is to use a `Container` or `Hub` instance created at your application's
    entry point for explicit dependency management. This global accessor should be
    avoided in application code.

    Thread-safe: Uses double-checked locking pattern for efficient lazy initialization.

    **Auto-Initialization Behavior:**
    This function automatically initializes the Foundation system on first access.
    The initialization is:
    - **Idempotent**: Safe to call multiple times
    - **Thread-safe**: Uses lock manager for coordination
    - **Lazy**: Only happens on first access

    Returns:
        Global Hub instance (created and initialized if needed)

    Example:
        >>> hub = get_hub()
        >>> hub.register_command("my_command", my_function)

    Note:
        For isolated Hub instances (testing, advanced use cases), use:
        >>> hub = Hub(use_shared_registries=False)

    """
    global _global_hub

    # Fast path: hub already initialized
    if _global_hub is not None:
        return _global_hub

    # Slow path: need to initialize hub
    with get_lock_manager().acquire("foundation.hub.init"):
        # Double-check after acquiring lock
        if _global_hub is None:
            # Global hub uses shared registries by default
            _global_hub = Hub(use_shared_registries=True)

            # Auto-initialize Foundation on first hub access
            _global_hub.initialize_foundation()

            # Bootstrap foundation components now that hub is ready (skip in test mode)
            from provide.foundation.testmode.detection import is_in_test_mode

            if is_in_test_mode():
                try:
                    from provide.foundation.hub.components import bootstrap_foundation

                    bootstrap_foundation()
                except ImportError:
                    # Bootstrap function might not exist yet, that's okay
                    pass

    return _global_hub


x_get_hub__mutmut_mutants: ClassVar[MutantDict] = {
    "x_get_hub__mutmut_1": x_get_hub__mutmut_1,
    "x_get_hub__mutmut_2": x_get_hub__mutmut_2,
    "x_get_hub__mutmut_3": x_get_hub__mutmut_3,
    "x_get_hub__mutmut_4": x_get_hub__mutmut_4,
    "x_get_hub__mutmut_5": x_get_hub__mutmut_5,
    "x_get_hub__mutmut_6": x_get_hub__mutmut_6,
    "x_get_hub__mutmut_7": x_get_hub__mutmut_7,
    "x_get_hub__mutmut_8": x_get_hub__mutmut_8,
    "x_get_hub__mutmut_9": x_get_hub__mutmut_9,
}


def get_hub(*args, **kwargs):
    result = _mutmut_trampoline(x_get_hub__mutmut_orig, x_get_hub__mutmut_mutants, args, kwargs)
    return result


get_hub.__signature__ = _mutmut_signature(x_get_hub__mutmut_orig)
x_get_hub__mutmut_orig.__name__ = "x_get_hub"


def x_clear_hub__mutmut_orig() -> None:
    """Clear the global hub instance.

    This is primarily used for testing to reset Foundation state
    between test runs.

    """
    global _global_hub
    if _global_hub:
        _global_hub.clear()
    _global_hub = None


def x_clear_hub__mutmut_1() -> None:
    """Clear the global hub instance.

    This is primarily used for testing to reset Foundation state
    between test runs.

    """
    global _global_hub
    if _global_hub:
        _global_hub.clear()
    _global_hub = ""


x_clear_hub__mutmut_mutants: ClassVar[MutantDict] = {"x_clear_hub__mutmut_1": x_clear_hub__mutmut_1}


def clear_hub(*args, **kwargs):
    result = _mutmut_trampoline(x_clear_hub__mutmut_orig, x_clear_hub__mutmut_mutants, args, kwargs)
    return result


clear_hub.__signature__ = _mutmut_signature(x_clear_hub__mutmut_orig)
x_clear_hub__mutmut_orig.__name__ = "x_clear_hub"


# <3 🧱🤝🌐🪄
