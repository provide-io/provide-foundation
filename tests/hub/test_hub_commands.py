#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for command registration functionality."""

from __future__ import annotations

from typing import Never

import click
from provide.testkit import FoundationTestCase
import pytest

from provide.foundation.hub.commands import (
    create_command_group,
    register_command,
)
from provide.foundation.hub.manager import clear_hub, get_hub


class TestCommandRegistration(FoundationTestCase):
    """Test command registration and CLI building."""

    def setup_method(self) -> None:
        """Clear the hub before each test."""
        super().setup_method()
        clear_hub()

    def test_register_command_decorator(self) -> None:
        """Test the @register_command decorator."""

        @register_command("hello")
        def hello_command() -> str:
            """Say hello."""
            return "Hello, World!"

        hub = get_hub()
        command = hub.get_command("hello")

        assert command is hello_command
        assert hasattr(hello_command, "__registry_name__")
        assert hello_command.__registry_name__ == "hello"
        assert hasattr(hello_command, "__registry_dimension__")
        assert hello_command.__registry_dimension__ == "command"

    def test_register_command_auto_name(self) -> None:
        """Test command registration with auto-generated name."""

        @register_command()
        def my_special_command() -> None:
            """Auto-named command."""

        hub = get_hub()
        # The function name is used as the command name
        command = hub.get_command("my_special_command")

        assert command is my_special_command

    def test_register_command_with_aliases(self) -> None:
        """Test command registration with aliases."""

        @register_command("initialize", aliases=["init", "setup"])
        def init_command() -> None:
            """Initialize the system."""

        hub = get_hub()

        # Should be accessible by primary name and aliases
        assert hub.get_command("initialize") is init_command
        assert hub.get_command("init") is init_command
        assert hub.get_command("setup") is init_command

    def test_register_command_with_metadata(self) -> None:
        """Test command registration with metadata."""

        @register_command(
            "deploy",
            category="deployment",
            requires_auth=True,
            environments=["staging", "production"],
        )
        def deploy_command() -> None:
            """Deploy the application."""

        hub = get_hub()
        entry = hub._command_registry.get_entry("deploy", dimension="command")

        assert entry is not None
        assert entry.metadata["category"] == "deployment"
        assert entry.metadata["requires_auth"] is True
        assert entry.metadata["environments"] == ["staging", "production"]

    def test_register_hidden_command(self) -> None:
        """Test registering a hidden command."""

        @register_command("secret", hidden=True)
        def secret_command() -> None:
            """Hidden command."""

        hub = get_hub()
        entry = hub._command_registry.get_entry("secret", dimension="command")

        assert entry is not None
        assert entry.metadata["hidden"] is True

        info = entry.metadata.get("info")
        assert info.hidden is True

    def test_command_info_stored(self) -> None:
        """Test that CommandInfo is properly stored."""

        @register_command("info-cmd", description="Custom description")
        def info_command() -> None:
            """Docstring description."""

        hub = get_hub()
        entry = hub._command_registry.get_entry("info-cmd", dimension="command")
        info = entry.metadata.get("info")

        assert info is not None
        assert info.name == "info-cmd"
        assert info.func is info_command
        assert info.description == "Custom description"  # Overrides docstring

    def test_register_click_command(self) -> None:
        """Test registering a Click command directly."""

        @click.command()
        @click.option("--name", default="World")
        def greet(name) -> None:
            """Greet someone."""
            click.echo(f"Hello, {name}!")

        hub = get_hub()
        hub.add_command(greet, name="greet")

        command = hub.get_command("greet")
        assert command is greet

        entry = hub._command_registry.get_entry("greet", dimension="command")
        assert entry.metadata.get("click_command") is greet

    def test_create_cli_group_with_commands(self) -> None:
        """Test creating a CLI group with registered commands."""

        @register_command("cmd1")
        def command1() -> str:
            """First command."""
            return "cmd1"

        @register_command("cmd2")
        def command2() -> str:
            """Second command."""
            return "cmd2"

        @register_command("hidden", hidden=True)
        def hidden_command() -> str:
            """Hidden command."""
            return "hidden"

        hub = get_hub()
        cli_group = hub.create_cli("test-cli")

        assert isinstance(cli_group, click.Group)
        assert cli_group.name == "test-cli"

        # Check commands are added (hidden should not be)
        commands = cli_group.list_commands(None)
        assert "cmd1" in commands
        assert "cmd2" in commands
        assert "hidden" not in commands  # Hidden

    def test_command_with_context(self) -> None:
        """Test command that uses Click context."""

        @register_command("with-context")
        @click.pass_context
        def context_command(ctx):
            """Command that uses context."""
            return ctx.obj

        hub = get_hub()
        command = hub.get_command("with-context")

        assert command is context_command
        # The @click.pass_context decorator should be preserved
        # pass_context doesn't add __click_params__, it wraps the function
        # We can test that it works by creating a Click command and invoking it
        from click.testing import CliRunner

        cli = create_command_group("test")
        runner = CliRunner()
        result = runner.invoke(cli, ["with-context"], obj={"test": "value"})
        # If pass_context worked, the command should have access to ctx.obj
        assert result.exit_code == 0

    def test_command_group_hierarchy(self) -> None:
        """Test building command group hierarchy."""

        @register_command("parent.child1")
        def child1() -> None:
            """Child command 1."""

        @register_command("parent.child2")
        def child2() -> None:
            """Child command 2."""

        hub = get_hub()

        # Commands are registered and stored with dot notation
        assert hub.get_command("parent.child1") is child1
        assert hub.get_command("parent.child2") is child2

    def test_list_commands(self) -> None:
        """Test listing all registered commands."""

        @register_command("alpha")
        def alpha() -> None:
            pass

        @register_command("beta")
        def beta() -> None:
            pass

        @register_command("gamma")
        def gamma() -> None:
            pass

        hub = get_hub()
        commands = hub.list_commands()

        assert set(commands) == {"alpha", "beta", "gamma"}

    def test_command_execution_wrapper(self) -> None:
        """Test wrapping command execution with logging/error handling."""

        @register_command("wrapped")
        def wrapped_command() -> Never:
            """Command to be wrapped."""
            raise ValueError("Test error")

        hub = get_hub()

        # Get the command and wrap it
        command = hub.get_command("wrapped")

        # Direct execution should raise
        with pytest.raises(ValueError, match="Test error"):
            command()

    def test_async_command_registration(self) -> None:
        """Test registering async commands."""

        @register_command("async-cmd")
        async def async_command() -> str:
            """Async command."""
            return "async result"

        hub = get_hub()
        command = hub.get_command("async-cmd")

        assert command is async_command

        import asyncio

        result = asyncio.run(command())
        assert result == "async result"

    def test_command_replace(self) -> None:
        """Test replacing existing command."""

        @register_command("replaceable")
        def old_command() -> str:
            return "old"

        @register_command("replaceable", replace=True)
        def new_command() -> str:
            return "new"

        hub = get_hub()
        command = hub.get_command("replaceable")

        assert command is new_command
        assert command() == "new"


# 🧱🏗️🔚
