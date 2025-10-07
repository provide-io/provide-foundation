"""Tests for CLI builder decoupling from registry.

This module tests that CLI commands can be built directly from CommandInfo
objects without requiring global registry access.
"""

from __future__ import annotations

from typing import Annotated

import click
from provide.testkit import CliTestRunner, FoundationTestCase
import pytest

from provide.foundation.cli.click.adapter import ClickAdapter
from provide.foundation.cli.click.commands import build_click_command_from_info
from provide.foundation.cli.errors import CLIBuildError
from provide.foundation.hub.info import CommandInfo
from provide.foundation.hub.introspection import ParameterInfo


class TestBuildClickCommandFromInfo(FoundationTestCase):
    """Test pure builder function build_click_command_from_info."""

    def setup_method(self) -> None:
        """Set up test environment."""
        super().setup_method()

    def teardown_method(self) -> None:
        """Clean up after test."""
        super().teardown_method()

    def test_build_simple_command(self) -> None:
        """Build command from CommandInfo without registry."""

        def greet(name: str = "World") -> None:
            """Greet someone."""
            click.echo(f"Hello, {name}!")

        info = CommandInfo(
            name="greet",
            func=greet,
            description="Greet someone",
        )

        cmd = build_click_command_from_info(info)

        assert isinstance(cmd, click.Command)
        assert cmd.name == "greet"
        assert cmd.help == "Greet someone"
        assert not cmd.hidden

        # Test execution
        runner = CliTestRunner()
        result = runner.invoke(cmd, [])
        assert result.exit_code == 0
        assert "Hello, World!" in result.output

    def test_build_command_with_argument(self) -> None:
        """Build command with positional argument."""

        def deploy(environment: str) -> None:
            """Deploy to environment."""
            click.echo(f"Deploying to {environment}")

        info = CommandInfo(
            name="deploy",
            func=deploy,
            description="Deploy to environment",
        )

        cmd = build_click_command_from_info(info)

        runner = CliTestRunner()
        result = runner.invoke(cmd, ["production"])
        assert result.exit_code == 0
        assert "Deploying to production" in result.output

    def test_build_command_with_option(self) -> None:
        """Build command with keyword option."""

        def status(verbose: bool = False) -> None:
            """Show status."""
            if verbose:
                click.echo("Status: OK (verbose)")
            else:
                click.echo("Status: OK")

        info = CommandInfo(
            name="status",
            func=status,
            description="Show status",
        )

        cmd = build_click_command_from_info(info)

        runner = CliTestRunner()

        # Without option
        result = runner.invoke(cmd, [])
        assert result.exit_code == 0
        assert "Status: OK" in result.output
        assert "verbose" not in result.output

        # With option
        result = runner.invoke(cmd, ["--verbose"])
        assert result.exit_code == 0
        assert "Status: OK (verbose)" in result.output

    def test_build_command_with_annotated_argument(self) -> None:
        """Build command with Annotated type hint for argument."""

        def process(file: Annotated[str, "argument"]) -> None:
            """Process a file."""
            click.echo(f"Processing {file}")

        info = CommandInfo(
            name="process",
            func=process,
            description="Process a file",
        )

        cmd = build_click_command_from_info(info)

        runner = CliTestRunner()
        result = runner.invoke(cmd, ["data.txt"])
        assert result.exit_code == 0
        assert "Processing data.txt" in result.output

    def test_build_command_with_annotated_option(self) -> None:
        """Build command with Annotated type hint for option."""

        def connect(host: Annotated[str, "option"] = "localhost") -> None:
            """Connect to host."""
            click.echo(f"Connecting to {host}")

        info = CommandInfo(
            name="connect",
            func=connect,
            description="Connect to host",
        )

        cmd = build_click_command_from_info(info)

        runner = CliTestRunner()

        # Default value
        result = runner.invoke(cmd, [])
        assert result.exit_code == 0
        assert "Connecting to localhost" in result.output

        # Custom value
        result = runner.invoke(cmd, ["--host", "remote.example.com"])
        assert result.exit_code == 0
        assert "Connecting to remote.example.com" in result.output

    def test_build_command_with_multiple_parameters(self) -> None:
        """Build command with mixed arguments and options."""

        def migrate(
            target: str,
            database: str = "default",
            dry_run: bool = False,
        ) -> None:
            """Run database migration."""
            mode = "DRY RUN" if dry_run else "LIVE"
            click.echo(f"Migrating {database} to {target} ({mode})")

        info = CommandInfo(
            name="migrate",
            func=migrate,
            description="Run database migration",
        )

        cmd = build_click_command_from_info(info)

        runner = CliTestRunner()
        result = runner.invoke(cmd, ["v2.0", "--database", "users", "--dry-run"])
        assert result.exit_code == 0
        assert "Migrating users to v2.0 (DRY RUN)" in result.output

    def test_build_hidden_command(self) -> None:
        """Build hidden command."""

        def secret() -> None:
            """Secret command."""
            click.echo("Secret!")

        info = CommandInfo(
            name="secret",
            func=secret,
            description="Secret command",
            hidden=True,
        )

        cmd = build_click_command_from_info(info)

        assert cmd.hidden is True

    def test_build_command_with_metadata(self) -> None:
        """Build command with metadata (metadata not used in Click command)."""

        def admin() -> None:
            """Admin command."""
            click.echo("Admin action")

        info = CommandInfo(
            name="admin",
            func=admin,
            description="Admin command",
            metadata={"requires_auth": True, "category": "system"},
        )

        cmd = build_click_command_from_info(info)

        # Metadata doesn't affect Click command building
        assert isinstance(cmd, click.Command)
        assert cmd.name == "admin"

    def test_build_command_with_provided_parameters(self) -> None:
        """Build command when parameters are pre-introspected."""

        def execute(target: str, timeout: int = 30) -> None:
            """Execute a task."""
            click.echo(f"Executing {target} (timeout: {timeout}s)")

        # Pre-introspect parameters
        params = [
            ParameterInfo(name="target", annotation=str, kind="positional"),
            ParameterInfo(name="timeout", annotation=int, kind="keyword", default=30),
        ]

        info = CommandInfo(
            name="execute",
            func=execute,
            description="Execute a task",
            parameters=params,
        )

        cmd = build_click_command_from_info(info)

        runner = CliTestRunner()
        result = runner.invoke(cmd, ["task1", "--timeout", "60"])
        assert result.exit_code == 0
        assert "Executing task1 (timeout: 60s)" in result.output

    def test_build_command_failure_handling(self) -> None:
        """Test that building failures are properly wrapped in CLIBuildError."""

        # Create a function that will cause issues during parameter introspection
        def bad_func() -> None:
            """This should work fine."""
            pass

        # Simulate error by passing invalid info
        info = CommandInfo(
            name="bad",
            func=None,  # This will cause an error
            description="Bad command",
        )

        with pytest.raises(CLIBuildError, match="Failed to build Click command 'bad'"):
            build_click_command_from_info(info)


class TestClickAdapterDecoupling(FoundationTestCase):
    """Test that ClickAdapter works without registry dependency."""

    def setup_method(self) -> None:
        """Set up test environment."""
        super().setup_method()
        self.adapter = ClickAdapter()

    def teardown_method(self) -> None:
        """Clean up after test."""
        super().teardown_method()

    def test_adapter_build_command_without_registry(self) -> None:
        """ClickAdapter should build commands without registry lookup."""

        def hello(name: str = "World") -> None:
            """Say hello."""
            click.echo(f"Hello, {name}!")

        info = CommandInfo(
            name="hello",
            func=hello,
            description="Say hello",
        )

        # Build using adapter - should NOT require registry
        cmd = self.adapter.build_command(info)

        assert isinstance(cmd, click.Command)
        assert cmd.name == "hello"
        assert cmd.help == "Say hello"

        # Test execution
        runner = CliTestRunner()
        result = runner.invoke(cmd, ["--name", "Alice"])
        assert result.exit_code == 0
        assert "Hello, Alice!" in result.output

    def test_adapter_build_complex_command(self) -> None:
        """Adapter should handle complex commands."""

        def deploy(
            environment: str,
            version: str = "latest",
            force: bool = False,
        ) -> None:
            """Deploy application."""
            mode = "FORCE" if force else "NORMAL"
            click.echo(f"Deploying {version} to {environment} ({mode})")

        info = CommandInfo(
            name="deploy",
            func=deploy,
            description="Deploy application",
        )

        cmd = self.adapter.build_command(info)

        runner = CliTestRunner()
        result = runner.invoke(cmd, ["production", "--version", "v2.0", "--force"])
        assert result.exit_code == 0
        assert "Deploying v2.0 to production (FORCE)" in result.output

    def test_adapter_build_command_with_aliases(self) -> None:
        """Adapter should handle commands with aliases."""

        def initialize() -> None:
            """Initialize the system."""
            click.echo("System initialized")

        info = CommandInfo(
            name="initialize",
            func=initialize,
            description="Initialize the system",
            aliases=["init", "setup"],
        )

        cmd = self.adapter.build_command(info)

        # Click command doesn't use aliases directly, but shouldn't fail
        assert isinstance(cmd, click.Command)
        assert cmd.name == "initialize"

    def test_adapter_build_command_error_handling(self) -> None:
        """Adapter should propagate CLIBuildError."""

        info = CommandInfo(
            name="bad",
            func=None,  # This will cause an error
            description="Bad command",
        )

        with pytest.raises(CLIBuildError, match="Failed to build Click command 'bad'"):
            self.adapter.build_command(info)


class TestBuilderConsistency(FoundationTestCase):
    """Test that builder functions produce consistent results."""

    def setup_method(self) -> None:
        """Set up test environment."""
        super().setup_method()

    def teardown_method(self) -> None:
        """Clean up after test."""
        super().teardown_method()

    def test_pure_builder_and_adapter_consistency(self) -> None:
        """Pure builder and adapter should produce equivalent commands."""

        def status(verbose: bool = False) -> None:
            """Show status."""
            click.echo(f"Status: {'verbose' if verbose else 'simple'}")

        info = CommandInfo(
            name="status",
            func=status,
            description="Show status",
        )

        # Build using pure function
        cmd1 = build_click_command_from_info(info)

        # Build using adapter
        adapter = ClickAdapter()
        cmd2 = adapter.build_command(info)

        # Both should produce equivalent commands
        assert cmd1.name == cmd2.name
        assert cmd1.help == cmd2.help
        assert cmd1.hidden == cmd2.hidden
        assert len(cmd1.params) == len(cmd2.params)

        # Both should execute identically
        runner = CliTestRunner()

        result1 = runner.invoke(cmd1, ["--verbose"])
        result2 = runner.invoke(cmd2, ["--verbose"])

        assert result1.exit_code == result2.exit_code
        assert result1.output == result2.output


__all__ = [
    "TestBuildClickCommandFromInfo",
    "TestBuilderConsistency",
    "TestClickAdapterDecoupling",
]
