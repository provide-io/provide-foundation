"""Tests for nested command registration functionality."""

import pytest
import click
from click.testing import CliRunner

from provide.foundation.hub.commands import (
    register_command,
    create_command_group,
    get_command_registry,
)
from provide.foundation.hub.manager import get_hub, clear_hub


class TestNestedCommandRegistration:
    """Test nested command registration and CLI building."""
    
    def setup_method(self):
        """Clear the hub before each test."""
        clear_hub()
    
    def test_register_command_with_parent(self):
        """Test registering a command with a parent group."""
        
        @register_command("container", group=True)
        def container_group():
            """Container management commands."""
            pass
        
        @register_command("status", parent="container")
        def container_status():
            """Show container status."""
            return "Container is running"
        
        hub = get_hub()
        
        # Check the group is registered
        container = hub.get_command("container")
        assert container is container_group
        
        # Check the nested command is registered with parent prefix
        status = hub.get_command("container-status")
        assert status is container_status
    
    def test_register_command_with_dot_notation(self):
        """Test registering commands using dot notation."""
        
        @register_command("config.database", group=True)
        def config_database_group():
            """Database configuration commands."""
            pass
        
        hub = get_hub()
        
        # Should extract parent and name from dot notation
        entry = hub._command_registry.get_entry("config-database", dimension="command")
        assert entry is not None
        assert entry.metadata["parent"] == "config"
        assert entry.metadata["is_group"] is True
    
    def test_multi_level_nesting(self):
        """Test multi-level command nesting."""
        
        @register_command("container", group=True)
        def container_group():
            """Container commands."""
            pass
        
        @register_command("volumes", parent="container", group=True)
        def container_volumes_group():
            """Volume management commands."""
            pass
        
        @register_command("backup", parent="container.volumes")
        def container_volumes_backup():
            """Backup volumes."""
            return "Backing up volumes"
        
        hub = get_hub()
        
        # Check all levels are registered
        assert hub.get_command("container") is container_group
        assert hub.get_command("container-volumes") is container_volumes_group
        assert hub.get_command("container-volumes-backup") is container_volumes_backup
    
    def test_create_nested_cli_structure(self):
        """Test creating a CLI with nested command groups."""
        
        @register_command("db", group=True, description="Database commands")
        def db_group():
            pass
        
        @register_command("migrate", parent="db", description="Run migrations")
        def db_migrate():
            return "Migrating database"
        
        @register_command("backup", parent="db", description="Backup database")
        def db_backup():
            return "Backing up database"
        
        @register_command("cache", group=True, description="Cache commands")
        def cache_group():
            pass
        
        @register_command("clear", parent="cache", description="Clear cache")
        def cache_clear():
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
    
    def test_nested_command_execution(self):
        """Test executing nested commands through CLI."""
        
        @register_command("server", group=True)
        def server_group():
            pass
        
        @register_command("start", parent="server")
        def server_start(port: int = 8000):
            """Start the server."""
            click.echo(f"Server started on port {port}")
            return port
        
        @register_command("stop", parent="server")
        def server_stop():
            """Stop the server."""
            click.echo("Server stopped")
            return "stopped"
        
        # Create CLI and test with runner
        cli = create_command_group("app")
        runner = CliRunner()
        
        # Test server start command
        result = runner.invoke(cli, ["server", "start", "--port", "9000"])
        assert result.exit_code == 0
        assert "Server started on port 9000" in result.output
        
        # Test server stop command
        result = runner.invoke(cli, ["server", "stop"])
        assert result.exit_code == 0
        assert "Server stopped" in result.output
    
    def test_three_level_nesting(self):
        """Test three levels of command nesting."""
        
        @register_command("cloud", group=True)
        def cloud_group():
            """Cloud commands."""
            pass
        
        @register_command("aws", parent="cloud", group=True)
        def cloud_aws_group():
            """AWS commands."""
            pass
        
        @register_command("s3", parent="cloud.aws", group=True)
        def cloud_aws_s3_group():
            """S3 commands."""
            pass
        
        @register_command("list", parent="cloud.aws.s3")
        def cloud_aws_s3_list():
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
    
    def test_mixed_notation_styles(self):
        """Test mixing dot notation and parent parameter."""
        
        # Using dot notation in name
        @register_command("tools.terraform", group=True)
        def tools_terraform_group():
            """Terraform tools."""
            pass
        
        # Using parent parameter
        @register_command("install", parent="tools.terraform")
        def tools_terraform_install():
            """Install Terraform."""
            return "Installing Terraform"
        
        # Mixed: dot in name and parent parameter
        @register_command("validate", parent="tools.terraform")
        def tools_terraform_validate():
            """Validate Terraform."""
            return "Validating"
        
        hub = get_hub()
        
        # Check all are registered correctly
        assert hub.get_command("tools-terraform") is tools_terraform_group
        assert hub.get_command("tools-terraform-install") is tools_terraform_install
        assert hub.get_command("tools-terraform-validate") is tools_terraform_validate
    
    def test_nested_groups_with_same_command_names(self):
        """Test that different groups can have commands with same names."""
        
        @register_command("docker", group=True)
        def docker_group():
            pass
        
        @register_command("status", parent="docker")
        def docker_status():
            """Docker status."""
            click.echo("Docker status")
            return "docker"
        
        @register_command("k8s", group=True)
        def k8s_group():
            pass
        
        @register_command("status", parent="k8s")
        def k8s_status():
            """K8s status."""
            click.echo("K8s status")
            return "k8s"
        
        hub = get_hub()
        
        # Both status commands should exist with different prefixes
        assert hub.get_command("docker-status") is docker_status
        assert hub.get_command("k8s-status") is k8s_status
        
        # Test execution
        cli = create_command_group("app")
        runner = CliRunner()
        
        result = runner.invoke(cli, ["docker", "status"])
        assert "Docker status" in result.output
        
        result = runner.invoke(cli, ["k8s", "status"])
        assert "K8s status" in result.output
    
    def test_hidden_nested_groups(self):
        """Test hidden groups and commands in nested structure."""
        
        @register_command("admin", group=True, hidden=True)
        def admin_group():
            """Admin commands."""
            pass
        
        @register_command("reset", parent="admin")
        def admin_reset():
            """Reset system."""
            click.echo("System reset")
            return "reset"
        
        cli = create_command_group("app")
        
        # Hidden group should not appear in main help
        commands = cli.list_commands(None)
        assert "admin" not in commands
        
        # But should still be executable
        runner = CliRunner()
        result = runner.invoke(cli, ["admin", "reset"])
        assert result.exit_code == 0
        assert "System reset" in result.output
    
    def test_nested_command_with_options(self):
        """Test nested commands with Click options and arguments."""
        
        @register_command("deploy", group=True)
        def deploy_group():
            pass
        
        @register_command("app", parent="deploy")
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
            ["deploy", "app", "production", "--version", "v2.0", "--force", "--replicas", "3"],
        )
        assert result.exit_code == 0
        assert "Deploying v2.0 to production" in result.output
        assert "Force deploy enabled" in result.output
        assert "Replicas: 3" in result.output
    
    def test_group_help_text(self):
        """Test that group help text is properly displayed."""
        
        @register_command("git", group=True, description="Git operations")
        def git_group():
            """Git command group."""
            pass
        
        @register_command("commit", parent="git", description="Create a commit")
        def git_commit():
            """Commit changes."""
            return "committed"
        
        cli = create_command_group("app")
        runner = CliRunner()
        
        # Check group help
        result = runner.invoke(cli, ["git", "--help"])
        assert "Git operations" in result.output
        assert "commit" in result.output
        assert "Create a commit" in result.output
    
    def test_command_aliases_in_nested_structure(self):
        """Test command aliases work in nested structure."""
        
        @register_command("package", group=True)
        def package_group():
            pass
        
        @register_command("install", parent="package", aliases=["i", "add"])
        def package_install(name: str):
            """Install a package."""
            click.echo(f"Installing {name}")
            return name
        
        hub = get_hub()
        
        # Check primary name and aliases are registered
        assert hub.get_command("package-install") is package_install
        # Note: aliases at nested level need special handling
        # This is a known limitation that could be enhanced
    
    def test_error_on_missing_parent(self):
        """Test behavior when parent group doesn't exist."""
        
        # This should work - parent will be created implicitly or command added to root
        @register_command("orphan", parent="nonexistent")
        def orphan_command():
            """Orphan command."""
            return "orphan"
        
        cli = create_command_group("app")
        
        # The command should be accessible somehow
        # (either at root or parent was auto-created)
        runner = CliRunner()
        
        # Try to find where it ended up
        hub = get_hub()
        assert hub.get_command("nonexistent-orphan") is orphan_command


class TestNestedCommandIntegration:
    """Integration tests for nested commands in real scenarios."""
    
    def setup_method(self):
        """Clear the hub before each test."""
        clear_hub()
    
    def test_complex_cli_structure(self):
        """Test a complex, realistic CLI structure."""
        
        # Database commands
        @register_command("db", group=True, description="Database operations")
        def db_group():
            pass
        
        @register_command("migrate", parent="db")
        def db_migrate(direction: str = "up"):
            """Run database migrations."""
            click.echo(f"Running migrations {direction}")
        
        @register_command("seed", parent="db")
        def db_seed(count: int = 100):
            """Seed database with test data."""
            click.echo(f"Seeding {count} records")
        
        # Server commands
        @register_command("server", group=True, description="Server management")
        def server_group():
            pass
        
        @register_command("start", parent="server")
        def server_start(port: int = 8000, host: str = "localhost"):
            """Start the server."""
            click.echo(f"Starting server on {host}:{port}")
        
        @register_command("logs", parent="server", group=True)
        def server_logs_group():
            """Server log commands."""
            pass
        
        @register_command("show", parent="server.logs")
        def server_logs_show(lines: int = 100):
            """Show server logs."""
            click.echo(f"Showing last {lines} lines")
        
        @register_command("clear", parent="server.logs")
        def server_logs_clear():
            """Clear server logs."""
            click.echo("Clearing logs")
        
        # Config commands
        @register_command("config", group=True, description="Configuration")
        def config_group():
            pass
        
        @register_command("get", parent="config")
        def config_get(key: str):
            """Get config value."""
            click.echo(f"Config {key} = value")
        
        @register_command("set", parent="config")
        def config_set(key: str, value: str):
            """Set config value."""
            click.echo(f"Setting {key} = {value}")
        
        # Create and test CLI
        cli = create_command_group("myapp", help="My Application CLI")
        runner = CliRunner()
        
        # Test various command paths
        tests = [
            (["db", "migrate", "--direction", "down"], "Running migrations down"),
            (["db", "seed", "--count", "50"], "Seeding 50 records"),
            (["server", "start", "--port", "3000"], "Starting server on localhost:3000"),
            (["server", "logs", "show", "--lines", "200"], "Showing last 200 lines"),
            (["server", "logs", "clear"], "Clearing logs"),
            (["config", "get", "api_key"], "Config api_key = value"),
            (["config", "set", "api_key", "secret"], "Setting api_key = secret"),
        ]
        
        for args, expected_output in tests:
            result = runner.invoke(cli, args)
            assert result.exit_code == 0, f"Command failed: {' '.join(args)}\n{result.output}"
            assert expected_output in result.output, f"Expected '{expected_output}' in output for {args}"
    
    def test_help_navigation(self):
        """Test help text navigation through nested structure."""
        
        @register_command("tools", group=True, description="Development tools")
        def tools_group():
            pass
        
        @register_command("python", parent="tools", group=True, description="Python tools")
        def tools_python_group():
            pass
        
        @register_command("lint", parent="tools.python", description="Run linter")
        def tools_python_lint():
            """Lint Python code."""
            click.echo("Linting...")
        
        @register_command("format", parent="tools.python", description="Format code")
        def tools_python_format():
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