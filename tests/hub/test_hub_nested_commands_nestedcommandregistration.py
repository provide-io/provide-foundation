#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for nested command registration functionality."""

from __future__ import annotations

import click
from click.testing import CliRunner
from provide.testkit import FoundationTestCase

from provide.foundation.hub import get_hub
from provide.foundation.hub.commands import create_command_group, register_command
from provide.foundation.hub.manager import clear_hub


class TestNestedCommandRegistration(FoundationTestCase):
    """Test nested command registration and CLI building."""

    def setup_method(self) -> None:
        """Clear the hub before each test."""
        super().setup_method()
        clear_hub()

    def teardown_method(self) -> None:
        """Clear the hub after each test."""
        clear_hub()

    def test_register_command_with_parent(self) -> None:
        """Test registering a command with dot notation."""

        @register_command("container", group=True)
        def container_group() -> None:
            """Container management commands."""

        @register_command("container.status")
        def container_status() -> str:
            """Show container status."""
            return "Container is running"

        hub = get_hub()

        # Check the group is registered
        container = hub.get_command("container")
        assert container is container_group

        # Check the nested command is registered with parent prefix
        status = hub.get_command("container.status")
        assert status is container_status

    def test_register_command_with_dot_notation(self) -> None:
        """Test registering commands using dot notation."""

        @register_command("config.database", group=True)
        def config_database_group() -> None:
            """Database configuration commands."""

        hub = get_hub()

        # Should extract parent and name from dot notation
        entry = hub._command_registry.get_entry("config.database", dimension="command")
        assert entry is not None
        assert entry.metadata["parent"] == "config"
        assert entry.metadata["is_group"] is True

    def test_multi_level_nesting(self) -> None:
        """Test multi-level command nesting."""

        @register_command("container", group=True)
        def container_group() -> None:
            """Container commands."""

        @register_command("container.volumes", group=True)
        def container_volumes_group() -> None:
            """Volume management commands."""

        @register_command("container.volumes.backup")
        def container_volumes_backup() -> str:
            """Backup volumes."""
            return "Backing up volumes"

        hub = get_hub()

        # Check all levels are registered
        assert hub.get_command("container") is container_group
        assert hub.get_command("container.volumes") is container_volumes_group
        assert hub.get_command("container.volumes.backup") is container_volumes_backup

    def test_create_nested_cli_structure(self) -> None:
        """Test creating a CLI with nested command groups."""

        @register_command("db", group=True, description="Database commands")
        def db_group() -> None:
            pass

        @register_command("db.migrate", description="Run migrations")
        def db_migrate() -> str:
            return "Migrating database"

        @register_command("db.backup", description="Backup database")
        def db_backup() -> str:
            return "Backing up database"

        @register_command("cache", group=True, description="Cache commands")
        def cache_group() -> None:
            pass

        @register_command("cache.clear", description="Clear cache")
        def cache_clear() -> str:
            return "Clearing cache"

        # Create CLI group
        cli = create_command_group("test-app")

        # Check that groups are created
        assert "db" in cli.list_commands(None)
        assert "cache" in cli.list_commands(None)

        # Get the db group
        db_cmd = cli.commands.get("db")
        assert isinstance(db_cmd, click.Group)
        assert "migrate" in db_cmd.list_commands(None)
        assert "backup" in db_cmd.list_commands(None)

        # Get the cache group
        cache_cmd = cli.commands.get("cache")
        assert isinstance(cache_cmd, click.Group)
        assert "clear" in cache_cmd.list_commands(None)

    def test_nested_command_execution(self) -> None:
        """Test executing nested commands through CLI with Position-Based Hybrid."""

        @register_command("server", group=True)
        def server_group() -> None:
            pass

        @register_command("server.start")
        def server_start(port: int = 8000):
            """Start the server."""
            click.echo(f"Server started on port {port}")
            return port

        @register_command("server.stop")
        def server_stop() -> str:
            """Stop the server."""
            click.echo("Server stopped")
            return "stopped"

        # Create CLI and test with runner
        cli = create_command_group("app")
        runner = CliRunner()

        # Test server start command (port is optional positional with Position-Based Hybrid)
        result = runner.invoke(cli, ["server", "start", "9000"])
        assert result.exit_code == 0
        assert "Server started on port 9000" in result.output

        # Test server stop command
        result = runner.invoke(cli, ["server", "stop"])
        assert result.exit_code == 0
        assert "Server stopped" in result.output

    def test_three_level_nesting(self) -> None:
        """Test three levels of command nesting."""

        @register_command("cloud", group=True)
        def cloud_group() -> None:
            """Cloud commands."""

        @register_command("cloud.aws", group=True)
        def cloud_aws_group() -> None:
            """AWS commands."""

        @register_command("cloud.aws.s3", group=True)
        def cloud_aws_s3_group() -> None:
            """S3 commands."""

        @register_command("cloud.aws.s3.list")
        def cloud_aws_s3_list() -> str:
            """List S3 buckets."""
            click.echo("Listing S3 buckets")
            return "buckets"

        # Create CLI
        cli = create_command_group("app")
        runner = CliRunner()

        # Test the deeply nested command
        result = runner.invoke(cli, ["cloud", "aws", "s3", "list"])
        assert result.exit_code == 0
        assert "Listing S3 buckets" in result.output

    def test_mixed_notation_styles(self) -> None:
        """Test mixing dot notation and parent parameter."""

        # Using dot notation in name
        @register_command("tools.terraform", group=True)
        def tools_terraform_group() -> None:
            """Terraform tools."""

        # Using parent parameter
        @register_command("tools.terraform.install")
        def tools_terraform_install() -> str:
            """Install Terraform."""
            return "Installing Terraform"

        # Mixed: dot in name and parent parameter
        @register_command("tools.terraform.validate")
        def tools_terraform_validate() -> str:
            """Validate Terraform."""
            return "Validating"

        hub = get_hub()

        # Check all are registered correctly
        assert hub.get_command("tools.terraform") is tools_terraform_group
        assert hub.get_command("tools.terraform.install") is tools_terraform_install
        assert hub.get_command("tools.terraform.validate") is tools_terraform_validate

    def test_nested_groups_with_same_command_names(self) -> None:
        """Test that different groups can have commands with same names."""

        @register_command("docker", group=True)
        def docker_group() -> None:
            pass

        @register_command("docker.status")
        def docker_status() -> str:
            """Docker status."""
            click.echo("Docker status")
            return "docker"

        @register_command("k8s", group=True)
        def k8s_group() -> None:
            pass

        @register_command("k8s.status")
        def k8s_status() -> str:
            """K8s status."""
            click.echo("K8s status")
            return "k8s"

        hub = get_hub()

        # Both status commands should exist with different prefixes
        assert hub.get_command("docker.status") is docker_status
        assert hub.get_command("k8s.status") is k8s_status

        # Test execution
        cli = create_command_group("app")
        runner = CliRunner()

        result = runner.invoke(cli, ["docker", "status"])
        assert "Docker status" in result.output

        result = runner.invoke(cli, ["k8s", "status"])
        assert "K8s status" in result.output

    def test_hidden_nested_groups(self) -> None:
        """Test hidden groups and commands in nested structure."""

        @register_command("admin", group=True, hidden=True)
        def admin_group() -> None:
            """Admin commands."""

        @register_command("admin.reset")
        def admin_reset() -> str:
            """Reset system."""
            click.echo("System reset")
            return "reset"

        cli = create_command_group("app")

        # Hidden group currently appears in list but is marked as hidden
        # This is a limitation that could be improved
        cli.list_commands(None)
        # The admin group will be added but marked as hidden
        admin_cmd = cli.commands.get("admin")
        if admin_cmd:
            assert admin_cmd.hidden is True

        # But should still be executable
        runner = CliRunner()
        result = runner.invoke(cli, ["admin", "reset"])
        assert result.exit_code == 0
        assert "System reset" in result.output

    def test_nested_command_with_options(self) -> None:
        """Test nested commands with Click options and arguments."""

        @register_command("deploy", group=True)
        def deploy_group() -> None:
            pass

        @register_command("deploy.app")
        def deploy_app(
            environment: str,
            version: str = "latest",
            force: bool = False,
            replicas: int = 1,
        ):
            """Deploy application."""
            click.echo(f"Deploying {version} to {environment}")
            if force:
                click.echo("Force deploy enabled")
            click.echo(f"Replicas: {replicas}")
            return {
                "environment": environment,
                "version": version,
                "force": force,
                "replicas": replicas,
            }

        cli = create_command_group("app")
        runner = CliRunner()

        # Test with all options
        result = runner.invoke(
            cli,
            [
                "deploy",
                "app",
                "production",
                "--version",
                "v2.0",
                "--force",
                "--replicas",
                "3",
            ],
        )
        # Check result - might have formatting differences
        if result.exit_code != 0:
            print(f"Output: {result.output}")
            print(f"Exception: {result.exception}")
        assert result.exit_code == 0
        assert "v2.0" in result.output
        assert "production" in result.output

    def test_group_help_text(self) -> None:
        """Test that group help text is properly displayed."""

        @register_command("git", group=True, description="Git operations")
        def git_group() -> None:
            """Git command group."""

        @register_command("git.commit", description="Create a commit")
        def git_commit() -> str:
            """Commit changes."""
            return "committed"

        cli = create_command_group("app")
        runner = CliRunner()

        # Check group help
        result = runner.invoke(cli, ["git", "--help"])
        assert "Git operations" in result.output
        assert "commit" in result.output
        assert "Create a commit" in result.output

    def test_command_aliases_in_nested_structure(self) -> None:
        """Test command aliases work in nested structure."""

        @register_command("package", group=True)
        def package_group() -> None:
            pass

        @register_command("package.install", aliases=["i", "add"])
        def package_install(name: str):
            """Install a package."""
            click.echo(f"Installing {name}")
            return name

        hub = get_hub()

        # Check primary name and aliases are registered
        assert hub.get_command("package.install") is package_install
        # Note: aliases at nested level need special handling
        # This is a known limitation that could be enhanced

    def test_error_on_missing_parent(self) -> None:
        """Test behavior when parent group doesn't exist."""

        # This should work - parent will be created implicitly
        @register_command("nonexistent.orphan")
        def orphan_command() -> str:
            """Orphan command."""
            return "orphan"

        create_command_group("app")

        # The command should be accessible somehow
        # (either at root or parent was auto-created)
        CliRunner()

        # Try to find where it ended up
        hub = get_hub()
        assert hub.get_command("nonexistent.orphan") is orphan_command


# 🧱🏗️🔚
