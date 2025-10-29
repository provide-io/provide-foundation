# provide/foundation/cli/click/adapter.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

"""Click CLI adapter implementation."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from provide.foundation.cli.click.builder import create_command_group
from provide.foundation.cli.click.commands import build_click_command_from_info
from provide.foundation.cli.click.hierarchy import ensure_parent_groups

if TYPE_CHECKING:
    import click as click_types

    from provide.foundation.hub.info import CommandInfo
    from provide.foundation.hub.registry import Registry

__all__ = ["ClickAdapter"]
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


class ClickAdapter:
    """Click framework adapter.

    Implements the CLIAdapter protocol for the Click framework,
    converting framework-agnostic CommandInfo objects to Click
    commands and groups.

    Examples:
        >>> adapter = ClickAdapter()
        >>> command = adapter.build_command(command_info)
        >>> isinstance(command, click.Command)
        True

    """

    def xǁClickAdapterǁbuild_command__mutmut_orig(self, info: CommandInfo) -> click_types.Command:
        """Build Click command from CommandInfo.

        Args:
            info: Framework-agnostic command information

        Returns:
            Click Command object

        Raises:
            CLIBuildError: If command building fails

        """
        return build_click_command_from_info(info)

    def xǁClickAdapterǁbuild_command__mutmut_1(self, info: CommandInfo) -> click_types.Command:
        """Build Click command from CommandInfo.

        Args:
            info: Framework-agnostic command information

        Returns:
            Click Command object

        Raises:
            CLIBuildError: If command building fails

        """
        return build_click_command_from_info(None)

    xǁClickAdapterǁbuild_command__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁClickAdapterǁbuild_command__mutmut_1": xǁClickAdapterǁbuild_command__mutmut_1
    }

    def build_command(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁClickAdapterǁbuild_command__mutmut_orig"),
            object.__getattribute__(self, "xǁClickAdapterǁbuild_command__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    build_command.__signature__ = _mutmut_signature(xǁClickAdapterǁbuild_command__mutmut_orig)
    xǁClickAdapterǁbuild_command__mutmut_orig.__name__ = "xǁClickAdapterǁbuild_command"

    def xǁClickAdapterǁbuild_group__mutmut_orig(
        self,
        name: str,
        commands: list[CommandInfo] | None = None,
        registry: Registry | None = None,
        **kwargs: Any,
    ) -> click_types.Group:
        """Build Click group with commands.

        Args:
            name: Group name
            commands: List of CommandInfo objects (or None to use registry)
            registry: Command registry
            **kwargs: Additional Click Group options

        Returns:
            Click Group object

        Raises:
            CLIBuildError: If group building fails

        """
        # If commands is a list of CommandInfo, extract names
        command_names = None
        if commands:
            command_names = [cmd.name for cmd in commands]

        return create_command_group(
            name=name,
            commands=command_names,
            registry=registry,
            **kwargs,
        )

    def xǁClickAdapterǁbuild_group__mutmut_1(
        self,
        name: str,
        commands: list[CommandInfo] | None = None,
        registry: Registry | None = None,
        **kwargs: Any,
    ) -> click_types.Group:
        """Build Click group with commands.

        Args:
            name: Group name
            commands: List of CommandInfo objects (or None to use registry)
            registry: Command registry
            **kwargs: Additional Click Group options

        Returns:
            Click Group object

        Raises:
            CLIBuildError: If group building fails

        """
        # If commands is a list of CommandInfo, extract names
        command_names = ""
        if commands:
            command_names = [cmd.name for cmd in commands]

        return create_command_group(
            name=name,
            commands=command_names,
            registry=registry,
            **kwargs,
        )

    def xǁClickAdapterǁbuild_group__mutmut_2(
        self,
        name: str,
        commands: list[CommandInfo] | None = None,
        registry: Registry | None = None,
        **kwargs: Any,
    ) -> click_types.Group:
        """Build Click group with commands.

        Args:
            name: Group name
            commands: List of CommandInfo objects (or None to use registry)
            registry: Command registry
            **kwargs: Additional Click Group options

        Returns:
            Click Group object

        Raises:
            CLIBuildError: If group building fails

        """
        # If commands is a list of CommandInfo, extract names
        command_names = None
        if commands:
            command_names = None

        return create_command_group(
            name=name,
            commands=command_names,
            registry=registry,
            **kwargs,
        )

    def xǁClickAdapterǁbuild_group__mutmut_3(
        self,
        name: str,
        commands: list[CommandInfo] | None = None,
        registry: Registry | None = None,
        **kwargs: Any,
    ) -> click_types.Group:
        """Build Click group with commands.

        Args:
            name: Group name
            commands: List of CommandInfo objects (or None to use registry)
            registry: Command registry
            **kwargs: Additional Click Group options

        Returns:
            Click Group object

        Raises:
            CLIBuildError: If group building fails

        """
        # If commands is a list of CommandInfo, extract names
        command_names = None
        if commands:
            command_names = [cmd.name for cmd in commands]

        return create_command_group(
            name=None,
            commands=command_names,
            registry=registry,
            **kwargs,
        )

    def xǁClickAdapterǁbuild_group__mutmut_4(
        self,
        name: str,
        commands: list[CommandInfo] | None = None,
        registry: Registry | None = None,
        **kwargs: Any,
    ) -> click_types.Group:
        """Build Click group with commands.

        Args:
            name: Group name
            commands: List of CommandInfo objects (or None to use registry)
            registry: Command registry
            **kwargs: Additional Click Group options

        Returns:
            Click Group object

        Raises:
            CLIBuildError: If group building fails

        """
        # If commands is a list of CommandInfo, extract names
        command_names = None
        if commands:
            command_names = [cmd.name for cmd in commands]

        return create_command_group(
            name=name,
            commands=None,
            registry=registry,
            **kwargs,
        )

    def xǁClickAdapterǁbuild_group__mutmut_5(
        self,
        name: str,
        commands: list[CommandInfo] | None = None,
        registry: Registry | None = None,
        **kwargs: Any,
    ) -> click_types.Group:
        """Build Click group with commands.

        Args:
            name: Group name
            commands: List of CommandInfo objects (or None to use registry)
            registry: Command registry
            **kwargs: Additional Click Group options

        Returns:
            Click Group object

        Raises:
            CLIBuildError: If group building fails

        """
        # If commands is a list of CommandInfo, extract names
        command_names = None
        if commands:
            command_names = [cmd.name for cmd in commands]

        return create_command_group(
            name=name,
            commands=command_names,
            registry=None,
            **kwargs,
        )

    def xǁClickAdapterǁbuild_group__mutmut_6(
        self,
        name: str,
        commands: list[CommandInfo] | None = None,
        registry: Registry | None = None,
        **kwargs: Any,
    ) -> click_types.Group:
        """Build Click group with commands.

        Args:
            name: Group name
            commands: List of CommandInfo objects (or None to use registry)
            registry: Command registry
            **kwargs: Additional Click Group options

        Returns:
            Click Group object

        Raises:
            CLIBuildError: If group building fails

        """
        # If commands is a list of CommandInfo, extract names
        command_names = None
        if commands:
            command_names = [cmd.name for cmd in commands]

        return create_command_group(
            commands=command_names,
            registry=registry,
            **kwargs,
        )

    def xǁClickAdapterǁbuild_group__mutmut_7(
        self,
        name: str,
        commands: list[CommandInfo] | None = None,
        registry: Registry | None = None,
        **kwargs: Any,
    ) -> click_types.Group:
        """Build Click group with commands.

        Args:
            name: Group name
            commands: List of CommandInfo objects (or None to use registry)
            registry: Command registry
            **kwargs: Additional Click Group options

        Returns:
            Click Group object

        Raises:
            CLIBuildError: If group building fails

        """
        # If commands is a list of CommandInfo, extract names
        command_names = None
        if commands:
            command_names = [cmd.name for cmd in commands]

        return create_command_group(
            name=name,
            registry=registry,
            **kwargs,
        )

    def xǁClickAdapterǁbuild_group__mutmut_8(
        self,
        name: str,
        commands: list[CommandInfo] | None = None,
        registry: Registry | None = None,
        **kwargs: Any,
    ) -> click_types.Group:
        """Build Click group with commands.

        Args:
            name: Group name
            commands: List of CommandInfo objects (or None to use registry)
            registry: Command registry
            **kwargs: Additional Click Group options

        Returns:
            Click Group object

        Raises:
            CLIBuildError: If group building fails

        """
        # If commands is a list of CommandInfo, extract names
        command_names = None
        if commands:
            command_names = [cmd.name for cmd in commands]

        return create_command_group(
            name=name,
            commands=command_names,
            **kwargs,
        )

    def xǁClickAdapterǁbuild_group__mutmut_9(
        self,
        name: str,
        commands: list[CommandInfo] | None = None,
        registry: Registry | None = None,
        **kwargs: Any,
    ) -> click_types.Group:
        """Build Click group with commands.

        Args:
            name: Group name
            commands: List of CommandInfo objects (or None to use registry)
            registry: Command registry
            **kwargs: Additional Click Group options

        Returns:
            Click Group object

        Raises:
            CLIBuildError: If group building fails

        """
        # If commands is a list of CommandInfo, extract names
        command_names = None
        if commands:
            command_names = [cmd.name for cmd in commands]

        return create_command_group(
            name=name,
            commands=command_names,
            registry=registry,
        )

    xǁClickAdapterǁbuild_group__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁClickAdapterǁbuild_group__mutmut_1": xǁClickAdapterǁbuild_group__mutmut_1,
        "xǁClickAdapterǁbuild_group__mutmut_2": xǁClickAdapterǁbuild_group__mutmut_2,
        "xǁClickAdapterǁbuild_group__mutmut_3": xǁClickAdapterǁbuild_group__mutmut_3,
        "xǁClickAdapterǁbuild_group__mutmut_4": xǁClickAdapterǁbuild_group__mutmut_4,
        "xǁClickAdapterǁbuild_group__mutmut_5": xǁClickAdapterǁbuild_group__mutmut_5,
        "xǁClickAdapterǁbuild_group__mutmut_6": xǁClickAdapterǁbuild_group__mutmut_6,
        "xǁClickAdapterǁbuild_group__mutmut_7": xǁClickAdapterǁbuild_group__mutmut_7,
        "xǁClickAdapterǁbuild_group__mutmut_8": xǁClickAdapterǁbuild_group__mutmut_8,
        "xǁClickAdapterǁbuild_group__mutmut_9": xǁClickAdapterǁbuild_group__mutmut_9,
    }

    def build_group(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁClickAdapterǁbuild_group__mutmut_orig"),
            object.__getattribute__(self, "xǁClickAdapterǁbuild_group__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    build_group.__signature__ = _mutmut_signature(xǁClickAdapterǁbuild_group__mutmut_orig)
    xǁClickAdapterǁbuild_group__mutmut_orig.__name__ = "xǁClickAdapterǁbuild_group"

    def xǁClickAdapterǁensure_parent_groups__mutmut_orig(self, parent_path: str, registry: Registry) -> None:
        """Ensure all parent groups in path exist.

        Args:
            parent_path: Dot-notation path (e.g., "db.migrate")
            registry: Command registry to update

        """
        ensure_parent_groups(parent_path, registry)

    def xǁClickAdapterǁensure_parent_groups__mutmut_1(self, parent_path: str, registry: Registry) -> None:
        """Ensure all parent groups in path exist.

        Args:
            parent_path: Dot-notation path (e.g., "db.migrate")
            registry: Command registry to update

        """
        ensure_parent_groups(None, registry)

    def xǁClickAdapterǁensure_parent_groups__mutmut_2(self, parent_path: str, registry: Registry) -> None:
        """Ensure all parent groups in path exist.

        Args:
            parent_path: Dot-notation path (e.g., "db.migrate")
            registry: Command registry to update

        """
        ensure_parent_groups(parent_path, None)

    def xǁClickAdapterǁensure_parent_groups__mutmut_3(self, parent_path: str, registry: Registry) -> None:
        """Ensure all parent groups in path exist.

        Args:
            parent_path: Dot-notation path (e.g., "db.migrate")
            registry: Command registry to update

        """
        ensure_parent_groups(registry)

    def xǁClickAdapterǁensure_parent_groups__mutmut_4(self, parent_path: str, registry: Registry) -> None:
        """Ensure all parent groups in path exist.

        Args:
            parent_path: Dot-notation path (e.g., "db.migrate")
            registry: Command registry to update

        """
        ensure_parent_groups(
            parent_path,
        )

    xǁClickAdapterǁensure_parent_groups__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁClickAdapterǁensure_parent_groups__mutmut_1": xǁClickAdapterǁensure_parent_groups__mutmut_1,
        "xǁClickAdapterǁensure_parent_groups__mutmut_2": xǁClickAdapterǁensure_parent_groups__mutmut_2,
        "xǁClickAdapterǁensure_parent_groups__mutmut_3": xǁClickAdapterǁensure_parent_groups__mutmut_3,
        "xǁClickAdapterǁensure_parent_groups__mutmut_4": xǁClickAdapterǁensure_parent_groups__mutmut_4,
    }

    def ensure_parent_groups(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁClickAdapterǁensure_parent_groups__mutmut_orig"),
            object.__getattribute__(self, "xǁClickAdapterǁensure_parent_groups__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    ensure_parent_groups.__signature__ = _mutmut_signature(xǁClickAdapterǁensure_parent_groups__mutmut_orig)
    xǁClickAdapterǁensure_parent_groups__mutmut_orig.__name__ = "xǁClickAdapterǁensure_parent_groups"


# <3 🧱🤝💻🪄
