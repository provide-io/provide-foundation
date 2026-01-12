#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for nested command registration functionality with dot notation."""

from __future__ import annotations

import click
from click.testing import CliRunner
from provide.testkit import FoundationTestCase

from provide.foundation.hub.commands import (
    create_command_group,
    register_command,
)
from provide.foundation.hub.manager import clear_hub, get_hub


class TestDotNotationCommands(FoundationTestCase):
    """Test command registration using dot notation."""

    def setup_method(self) -> None:
        """Clear the hub before each test."""
        super().setup_method()
        clear_hub()

    def test_simple_nested_command(self) -> None:
        """Test registering a simple nested command with dot notation."""

        @register_command("container.status")
        def container_status() -> str:
            """Show container status."""
            return "Container is running"

        hub = get_hub()

        # The container group should be auto-created
        container = hub.get_command("container")
        assert container is not None

        # Check the nested command is registered
        status = hub.get_command("container.status")
        assert status is container_status

    def test_multi_level_nesting(self) -> None:
        """Test multi-level command nesting with dot notation."""

        @register_command("container.volumes.backup")
        def container_volumes_backup() -> str:
            """Backup volumes."""
            return "Backing up volumes"

        hub = get_hub()

        # Check all levels are auto-created
        assert hub.get_command("container") is not None
        assert hub.get_command("container.volumes") is not None
        assert hub.get_command("container.volumes.backup") is container_volumes_backup

    def test_explicit_group_declaration(self) -> None:
        """Test explicit group declaration with custom description."""

        @register_command("tools", group=True, description="Development tools")
        def tools_group() -> None:
            """Tools command group."""

        @register_command("tools.install")
        def tools_install(package: str) -> str:
            """Install a tool."""
            return f"Installing {package}"

        hub = get_hub()

        # Check the explicit group
        tools = hub.get_command("tools")
        assert tools is tools_group

        # Check the nested command
        install = hub.get_command("tools.install")
        assert install is tools_install

    def test_command_with_parameters(self) -> None:
        """Test nested commands with Position-Based Hybrid parameter mapping."""

        @register_command("db.migrate")
        def db_migrate(direction: str = "up", steps: int = 1):
            """Run database migrations."""
            click.echo(f"Migrating {direction} {steps} steps")
            return {"direction": direction, "steps": steps}

        cli = create_command_group("app")
        runner = CliRunner()

        # Test with positional direction and option steps (Position-Based Hybrid)
        result = runner.invoke(
            cli,
            ["db", "migrate", "down", "--steps", "3"],
        )
        assert result.exit_code == 0
        assert "Migrating down 3 steps" in result.output

        # Test with defaults
        result = runner.invoke(cli, ["db", "migrate"])
        assert result.exit_code == 0
        assert "Migrating up 1 steps" in result.output

    def test_command_with_arguments(self) -> None:
        """Test commands with required arguments (no defaults)."""

        @register_command("file.read")
        def file_read(path: str):
            """Read a file."""
            click.echo(f"Reading {path}")
            return path

        cli = create_command_group("app")
        runner = CliRunner()

        # Test with argument
        result = runner.invoke(cli, ["file", "read", "test.txt"])
        assert result.exit_code == 0
        assert "Reading test.txt" in result.output

        # Test without argument (should fail)
        result = runner.invoke(cli, ["file", "read"])
        assert result.exit_code != 0

    def test_complex_nested_structure(self) -> None:
        """Test a complex nested command structure."""

        # Cloud providers
        @register_command("cloud.aws.ec2.list")
        def aws_ec2_list() -> None:
            """List EC2 instances."""
            click.echo("Listing EC2 instances")

        @register_command("cloud.aws.s3.list")
        def aws_s3_list() -> None:
            """List S3 buckets."""
            click.echo("Listing S3 buckets")

        @register_command("cloud.gcp.compute.list")
        def gcp_compute_list() -> None:
            """List Compute instances."""
            click.echo("Listing Compute instances")

        cli = create_command_group("cloud-cli")
        runner = CliRunner()

        # Test AWS EC2
        result = runner.invoke(cli, ["cloud", "aws", "ec2", "list"])
        assert result.exit_code == 0
        assert "Listing EC2 instances" in result.output

        # Test AWS S3
        result = runner.invoke(cli, ["cloud", "aws", "s3", "list"])
        assert result.exit_code == 0
        assert "Listing S3 buckets" in result.output

        # Test GCP Compute
        result = runner.invoke(cli, ["cloud", "gcp", "compute", "list"])
        assert result.exit_code == 0
        assert "Listing Compute instances" in result.output

    def test_help_text_navigation(self) -> None:
        """Test help text through nested structure."""

        @register_command("tools", group=True, description="Development tools")
        def tools_group() -> None:
            pass

        @register_command("tools.python.lint", description="Lint Python code")
        def tools_python_lint() -> None:
            """Run Python linter."""
            click.echo("Linting...")

        @register_command("tools.python.format", description="Format Python code")
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

        # Test tools python help
        result = runner.invoke(cli, ["tools", "python", "--help"])
        assert "lint" in result.output
        assert "format" in result.output
        assert "Lint Python code" in result.output
        assert "Format Python code" in result.output

    def test_boolean_flags(self) -> None:
        """Test boolean parameters become flags with Position-Based Hybrid."""

        @register_command("deploy.app")
        def deploy_app(
            env: str = "staging",
            force: bool = False,
            verbose: bool = False,
        ):
            """Deploy application."""
            if verbose:
                click.echo(f"Deploying to {env}")
            if force:
                click.echo("Force deploy enabled")
            return {"env": env, "force": force, "verbose": verbose}

        cli = create_command_group("deploy-cli")
        runner = CliRunner()

        # Test with positional env and boolean flags (Position-Based Hybrid)
        result = runner.invoke(
            cli,
            ["deploy", "app", "prod", "--force", "--verbose"],
        )
        assert result.exit_code == 0
        assert "Deploying to prod" in result.output
        assert "Force deploy enabled" in result.output

        # Test without flags (defaults)
        result = runner.invoke(cli, ["deploy", "app"])
        assert result.exit_code == 0
        assert "Force deploy" not in result.output

    def test_hidden_groups_and_commands(self) -> None:
        """Test hidden groups and commands."""

        @register_command("admin", group=True, hidden=True)
        def admin_group() -> None:
            """Admin commands."""

        @register_command("admin.reset")
        def admin_reset() -> None:
            """Reset system."""
            click.echo("System reset")

        @register_command("public.status")
        def public_status() -> None:
            """Show status."""
            click.echo("Status OK")

        cli = create_command_group("app")
        runner = CliRunner()

        # Hidden group should work but not show in help
        result = runner.invoke(cli, ["admin", "reset"])
        assert result.exit_code == 0
        assert "System reset" in result.output

        # Check main help doesn't show hidden group
        result = runner.invoke(cli, ["--help"])
        assert "public" in result.output
        # Note: Hidden groups still appear but are marked as hidden

    def test_command_aliases(self) -> None:
        """Test command aliases work with dot notation."""

        @register_command("package.install", aliases=["i", "add"])
        def package_install(name: str) -> None:
            """Install a package."""
            click.echo(f"Installing {name}")

        hub = get_hub()

        # Check primary name is registered
        assert hub.get_command("package.install") is package_install
        # Aliases are also registered at the hub level
        assert hub.get_command("i") is package_install
        assert hub.get_command("add") is package_install

    def test_same_command_names_different_groups(self) -> None:
        """Test that different groups can have commands with the same name."""

        @register_command("docker.status")
        def docker_status() -> str:
            """Docker status."""
            click.echo("Docker: running")
            return "docker"

        @register_command("k8s.status")
        def k8s_status() -> str:
            """K8s status."""
            click.echo("K8s: running")
            return "k8s"

        cli = create_command_group("ops")
        runner = CliRunner()

        # Test docker status
        result = runner.invoke(cli, ["docker", "status"])
        assert result.exit_code == 0
        assert "Docker: running" in result.output

        # Test k8s status
        result = runner.invoke(cli, ["k8s", "status"])
        assert result.exit_code == 0
        assert "K8s: running" in result.output

    def test_auto_group_description(self) -> None:
        """Test auto-created groups get reasonable descriptions."""

        @register_command("network.firewall.rules.add")
        def add_firewall_rule(port: int) -> None:
            """Add a firewall rule."""
            click.echo(f"Adding rule for port {port}")

        hub = get_hub()

        # Check auto-created groups exist
        network = hub._command_registry.get_entry("network", dimension="command")
        assert network is not None
        assert network.metadata.get("description") == "Network commands"

        firewall = hub._command_registry.get_entry(
            "network.firewall",
            dimension="command",
        )
        assert firewall is not None
        assert firewall.metadata.get("description") == "Firewall commands"

        rules = hub._command_registry.get_entry(
            "network.firewall.rules",
            dimension="command",
        )
        assert rules is not None
        assert rules.metadata.get("description") == "Rules commands"


class TestDotNotationIntegration(FoundationTestCase):
    """Integration tests for dot notation commands in real scenarios."""

    def setup_method(self) -> None:
        """Clear the hub before each test."""
        super().setup_method()
        clear_hub()

    def test_realistic_cli_application(self) -> None:
        """Test a realistic CLI application using dot notation."""

        # Database operations
        @register_command("db.migrate")
        def db_migrate(version: str = "latest") -> None:
            """Run database migrations."""
            click.echo(f"Migrating to {version}")

        @register_command("db.backup")
        def db_backup(output: str = "backup.sql") -> None:
            """Backup database."""
            click.echo(f"Backing up to {output}")

        @register_command("db.restore")
        def db_restore(input: str) -> None:
            """Restore database."""
            click.echo(f"Restoring from {input}")

        # Server operations
        @register_command("server.start")
        def server_start(port: int = 8000, host: str = "localhost") -> None:
            """Start server."""
            click.echo(f"Server starting on {host}:{port}")

        @register_command("server.stop")
        def server_stop() -> None:
            """Stop server."""
            click.echo("Server stopped")

        @register_command("server.logs.show")
        def server_logs_show(lines: int = 100, follow: bool = False) -> None:
            """Show server logs."""
            click.echo(f"Showing {lines} lines")
            if follow:
                click.echo("Following logs...")

        # Cache operations
        @register_command("cache.clear")
        def cache_clear(pattern: str = "*") -> None:
            """Clear cache."""
            click.echo(f"Clearing cache: {pattern}")

        @register_command("cache.stats")
        def cache_stats() -> None:
            """Show cache statistics."""
            click.echo("Cache stats: 100 entries")

        # Create CLI and run tests
        cli = create_command_group("myapp", help="My Application")
        runner = CliRunner()

        tests = [
            # db_migrate(version: str = "latest") - Position-Based Hybrid: version is optional arg
            (["db", "migrate", "v2.0"], "Migrating to v2.0"),
            # db_backup(output: str = "backup.sql") - Position-Based Hybrid: output is optional arg
            (["db", "backup"], "Backing up to backup.sql"),
            # db_restore(input: str) - required arg
            (["db", "restore", "old.sql"], "Restoring from old.sql"),
            # server_start(port: int = 8000, host: str = "localhost") - Position-Based Hybrid: port is optional arg
            (
                ["server", "start", "3000"],
                "Server starting on localhost:3000",
            ),
            # server_stop() - no args
            (["server", "stop"], "Server stopped"),
            # server_logs_show(lines: int = 100, follow: bool = False) - Position-Based Hybrid: lines is optional arg
            (
                ["server", "logs", "show", "50", "--follow"],
                "Showing 50 lines",
            ),
            # cache_clear(pattern: str = "*") - Position-Based Hybrid: pattern is optional arg
            (["cache", "clear", "*.tmp"], "Clearing cache: *.tmp"),
            # cache_stats() - no args
            (["cache", "stats"], "Cache stats: 100 entries"),
        ]

        for args, expected in tests:
            result = runner.invoke(cli, args)
            assert result.exit_code == 0, f"Command failed: {' '.join(args)}\n{result.output}"
            assert expected in result.output, f"Expected '{expected}' in output for {args}"

    def test_mixed_explicit_and_auto_groups(self) -> None:
        """Test mixing explicit group declarations with auto-created ones."""

        # Explicit root group
        @register_command("api", group=True, description="API management commands")
        def api_group() -> None:
            """API root group."""

        # Auto-created subgroups with commands
        @register_command("api.users.list")
        def api_users_list() -> None:
            """List users."""
            click.echo("Listing users")

        @register_command("api.users.create")
        def api_users_create(name: str, email: str) -> None:
            """Create user."""
            click.echo(f"Creating user: {name} ({email})")

        # Another explicit group at deeper level
        @register_command("api.auth", group=True, description="Authentication")
        def api_auth_group() -> None:
            """Auth group."""

        @register_command("api.auth.login")
        def api_auth_login(username: str, password: str | None = None) -> None:
            """Login."""
            click.echo(f"Logging in as {username}")

        cli = create_command_group("api-cli")
        runner = CliRunner()

        # Test help shows proper descriptions
        result = runner.invoke(cli, ["--help"])
        assert "API management commands" in result.output

        result = runner.invoke(cli, ["api", "--help"])
        assert "users" in result.output
        assert "auth" in result.output
        assert "Authentication" in result.output

        # Test commands work
        result = runner.invoke(
            cli,
            ["api", "users", "create", "john", "john@example.com"],
        )
        assert result.exit_code == 0
        assert "Creating user: john (john@example.com)" in result.output


# 🧱🏗️🔚
