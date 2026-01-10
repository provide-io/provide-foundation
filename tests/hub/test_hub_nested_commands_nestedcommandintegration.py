#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for nested command registration functionality."""

from __future__ import annotations

import click
from click.testing import CliRunner
from provide.testkit import FoundationTestCase

from provide.foundation.hub.commands import create_command_group, register_command
from provide.foundation.hub.manager import clear_hub


class TestNestedCommandIntegration(FoundationTestCase):
    """Integration tests for nested commands in real scenarios."""

    def setup_method(self) -> None:
        """Clear the hub before each test."""
        super().setup_method()
        clear_hub()

    def teardown_method(self) -> None:
        """Clear the hub after each test."""
        clear_hub()

    def test_complex_cli_structure(self) -> None:
        """Test a complex, realistic CLI structure."""

        # Database commands
        @register_command("db", group=True, description="Database operations")
        def db_group() -> None:
            pass

        @register_command("db.migrate")
        def db_migrate(direction: str = "up") -> None:
            """Run database migrations."""
            click.echo(f"Running migrations {direction}")

        @register_command("db.seed")
        def db_seed(count: int = 100) -> None:
            """Seed database with test data."""
            click.echo(f"Seeding {count} records")

        # Server commands
        @register_command("server", group=True, description="Server management")
        def server_group() -> None:
            pass

        @register_command("server.start")
        def server_start(port: int = 8000, host: str = "localhost") -> None:
            """Start the server."""
            click.echo(f"Starting server on {host}:{port}")

        @register_command("server.logs", group=True)
        def server_logs_group() -> None:
            """Server log commands."""

        @register_command("server.logs.show")
        def server_logs_show(lines: int = 100) -> None:
            """Show server logs."""
            click.echo(f"Showing last {lines} lines")

        @register_command("server.logs.clear")
        def server_logs_clear() -> None:
            """Clear server logs."""
            click.echo("Clearing logs")

        # Config commands
        @register_command("config", group=True, description="Configuration")
        def config_group() -> None:
            pass

        @register_command("config.get")
        def config_get(key: str) -> None:
            """Get config value."""
            click.echo(f"Config {key} = value")

        @register_command("config.set")
        def config_set(key: str, value: str) -> None:
            """Set config value."""
            click.echo(f"Setting {key} = {value}")

        # Create and test CLI
        cli = create_command_group("myapp", help="My Application CLI")
        runner = CliRunner()

        # Test various command paths with Position-Based Hybrid mapping
        tests = [
            # db_migrate(direction: str = "up") - Position-Based Hybrid: direction is optional arg
            (["db", "migrate"], "Running migrations up"),  # Using default direction
            # db_seed(count: int = 100) - Position-Based Hybrid: count is optional arg
            (["db", "seed", "50"], "Seeding 50 records"),
            # server_start(port: int = 8000, host: str = "localhost") - Position-Based Hybrid: port is optional arg
            (
                ["server", "start", "3000"],
                "Starting server on localhost:3000",
            ),
            # server_logs_show(lines: int = 100) - Position-Based Hybrid: lines is optional arg
            (["server", "logs", "show", "200"], "Showing last 200 lines"),
            # server_logs_clear() - no args
            (["server", "logs", "clear"], "Clearing logs"),
            # config_get(key: str) - required arg
            (["config", "get", "api_key"], "Config api_key = value"),
            # config_set(key: str, value: str) - required args
            (["config", "set", "api_key", "secret"], "Setting api_key = secret"),
        ]

        for args, expected_output in tests:
            result = runner.invoke(cli, args)
            assert result.exit_code == 0, f"Command failed: {' '.join(args)}\n{result.output}"
            assert expected_output in result.output, f"Expected '{expected_output}' in output for {args}"

    def test_help_navigation(self) -> None:
        """Test help text navigation through nested structure."""

        @register_command("tools", group=True, description="Development tools")
        def tools_group() -> None:
            pass

        @register_command("tools.python", group=True, description="Python tools")
        def tools_python_group() -> None:
            pass

        @register_command("tools.python.lint", description="Run linter")
        def tools_python_lint() -> None:
            """Lint Python code."""
            click.echo("Linting...")

        @register_command("tools.python.format", description="Format code")
        def tools_python_format() -> None:
            """Format Python code."""
            click.echo("Formatting...")

        cli = create_command_group("dev")
        runner = CliRunner()

        # Test main help
        result = runner.invoke(cli, ["--help"])
        assert "tools" in result.output
        assert "Development tools" in result.output

        # Test tools help
        result = runner.invoke(cli, ["tools", "--help"])
        assert "python" in result.output
        assert "Python tools" in result.output

        # Test tools python help
        result = runner.invoke(cli, ["tools", "python", "--help"])
        assert "lint" in result.output
        assert "format" in result.output
        assert "Run linter" in result.output
        assert "Format code" in result.output


# 🧱🏗️🔚
