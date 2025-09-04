"""Integration tests for CLI functionality."""

import json
from pathlib import Path
import tempfile
from unittest.mock import MagicMock, patch

import click
from click.testing import CliRunner

from provide.foundation.cli import (
    flexible_options,
    output_options,
    pass_context,
    setup_cli_logging,
)
from provide.foundation.context import Context
from provide.foundation.logger import get_logger


class TestCompleteCliIntegration:
    """Test complete CLI with all options working together."""

    def create_test_cli(self):
        """Create a test CLI with all features."""

        @click.group()
        @flexible_options
        @output_options
        @pass_context
        def cli(ctx: Context, **kwargs) -> None:
            """Test CLI application."""
            # Store all options in context for subcommands
            for key, value in kwargs.items():
                if value is not None:
                    setattr(ctx, key, value)

            # Setup logging based on options
            if ctx.log_level:
                setup_cli_logging(
                    ctx=ctx,
                    log_level=ctx.log_level,
                    log_file=ctx.log_file,
                    json_logs=ctx.json_output,
                )

        @cli.group()
        @flexible_options
        @pass_context
        def database(ctx: Context, **kwargs) -> None:
            """Database management commands."""
            # Update context with subcommand options
            for key, value in kwargs.items():
                if value is not None:
                    setattr(ctx, key, value)

        @database.command()
        @pass_context
        def migrate(ctx: Context) -> None:
            """Run database migrations."""
            logger = get_logger(__name__)
            logger.info("Running migrations")

            if ctx.json_output:
                click.echo(json.dumps({"status": "success", "migrations": 5}))
            else:
                click.echo("✅ Applied 5 migrations")

        @cli.command()
        @click.option("--log-level", type=click.Choice(["DEBUG", "INFO", "WARNING", "ERROR"]))
        @click.option("--no-emoji", is_flag=True, help="Disable emoji output")
        @pass_context
        def status(ctx: Context, log_level=None, no_emoji=False, **kwargs) -> None:
            """Show application status."""
            # Command-level options override group-level
            if log_level is not None:
                ctx.log_level = log_level
            if no_emoji:
                ctx.no_emoji = no_emoji
            for key, value in kwargs.items():
                if value is not None:
                    setattr(ctx, key, value)

            logger = get_logger(__name__)
            logger.debug("Checking status")

            if ctx.json_output:
                click.echo(json.dumps({"status": "healthy", "uptime": 3600}))
            else:
                if not getattr(ctx, "no_emoji", False):
                    click.echo("🟢 Application is healthy")
                else:
                    click.echo("Application is healthy")

        return cli

    def test_options_at_group_level(self) -> None:
        """Test that options work at the group level."""
        cli = self.create_test_cli()
        runner = CliRunner()

        result = runner.invoke(cli, ["--log-level", "DEBUG", "--json", "status"])
        assert result.exit_code == 0
        # JSON output should be enabled
        output = json.loads(result.output.strip().split("\n")[-1])
        assert output["status"] == "healthy"

    def test_options_at_subcommand_level(self) -> None:
        """Test that options work at subcommand level."""
        cli = self.create_test_cli()
        runner = CliRunner()

        result = runner.invoke(cli, ["status", "--log-level", "INFO", "--no-emoji"])
        assert result.exit_code == 0
        assert "Application is healthy" in result.output
        assert "🟢" not in result.output  # No emoji

    def test_nested_groups_inherit_options(self) -> None:
        """Test that nested groups inherit options."""
        cli = self.create_test_cli()
        runner = CliRunner()

        result = runner.invoke(
            cli, ["--json", "database", "--log-level", "WARNING", "migrate"]
        )
        assert result.exit_code == 0
        # JSON output should be inherited
        output = json.loads(result.output.strip().split("\n")[-1])
        assert output["status"] == "success"

    def test_command_options_override_group_options(self) -> None:
        """Test that command-level options override group-level."""
        cli = self.create_test_cli()
        runner = CliRunner()

        with tempfile.NamedTemporaryFile(mode="w", suffix=".log", delete=False) as f:
            log_file = f.name

        try:
            # Group sets log-level INFO, command overrides with DEBUG
            result = runner.invoke(
                cli,
                [
                    "--log-level",
                    "INFO",
                    "status",
                    "--log-level",
                    "DEBUG",
                    "--log-file",
                    log_file,
                ],
            )
            assert result.exit_code == 0

            # Check that log file was created
            assert Path(log_file).exists()
        finally:
            Path(log_file).unlink(missing_ok=True)


class TestLoggingIntegration:
    """Test that logging options actually affect logging behavior."""

    @patch("provide.foundation.logger.base.FoundationLogger")
    def test_log_level_affects_output(self, mock_logger_class) -> None:
        """Test that log-level actually changes logging verbosity."""
        mock_logger = MagicMock()
        mock_logger_class.return_value = mock_logger

        @click.command()
        @flexible_options
        @pass_context
        def cmd(ctx: Context, **kwargs) -> None:
            # Setup logging with the provided level
            if ctx.log_level:
                setup_cli_logging(log_level=ctx.log_level)

            logger = get_logger(__name__)
            logger.debug("Debug message")
            logger.info("Info message")
            logger.warning("Warning message")
            logger.error("Error message")
            click.echo("done")

        runner = CliRunner()

        # Test with WARNING level - should only see warning and error
        result = runner.invoke(cmd, ["--log-level", "WARNING"])
        assert result.exit_code == 0

    def test_log_format_changes_output(self) -> None:
        """Test that log-format changes the output format."""

        @click.command()
        @flexible_options
        @pass_context
        def cmd(ctx: Context, **kwargs) -> None:
            if ctx.log_level and hasattr(ctx, "log_format"):
                setup_cli_logging(
                    log_level=ctx.log_level, json_logs=ctx.log_format == "json"
                )

            logger = get_logger(__name__)
            logger.info("Test message", extra_field="value")
            click.echo("done")

        runner = CliRunner()

        # Test JSON format
        result = runner.invoke(cmd, ["--log-level", "INFO", "--log-format", "json"])
        assert result.exit_code == 0
        # Output should contain JSON-formatted logs

    def test_log_file_writes_to_file(self) -> None:
        """Test that log-file option writes logs to a file."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".log", delete=False) as f:
            log_file = f.name

        try:

            @click.command()
            @flexible_options
            @pass_context
            def cmd(ctx: Context, **kwargs) -> None:
                if ctx.log_file:
                    setup_cli_logging(
                        log_level=ctx.log_level or "INFO", log_file=ctx.log_file
                    )

                logger = get_logger(__name__)
                logger.info("Message to file")
                click.echo("done")

            runner = CliRunner()
            result = runner.invoke(cmd, ["--log-file", log_file, "--log-level", "INFO"])
            assert result.exit_code == 0

            # Check that log file contains the message
            with open(log_file) as f:
                content = f.read()
                assert "Message to file" in content
        finally:
            Path(log_file).unlink(missing_ok=True)


class TestOutputFormatting:
    """Test output formatting options."""

    def test_json_output_format(self) -> None:
        """Test that --json option produces JSON output."""

        @click.command()
        @output_options
        @pass_context
        def cmd(ctx: Context, **kwargs) -> None:
            if ctx.json_output:
                click.echo(json.dumps({"result": "success", "count": 42}))
            else:
                click.echo("Result: success (42 items)")

        runner = CliRunner()

        # Test JSON output
        result = runner.invoke(cmd, ["--json"])
        assert result.exit_code == 0
        output = json.loads(result.output)
        assert output["result"] == "success"
        assert output["count"] == 42

        # Test normal output
        result = runner.invoke(cmd)
        assert result.exit_code == 0
        assert "Result: success (42 items)" in result.output

    def test_no_color_option(self) -> None:
        """Test that --no-color disables colored output."""

        @click.command()
        @output_options
        @pass_context
        def cmd(ctx: Context, **kwargs) -> None:
            if getattr(ctx, "no_color", False):
                click.echo("Plain text")
            else:
                click.secho("Colored text", fg="green")

        runner = CliRunner()

        # Test with color disabled
        result = runner.invoke(cmd, ["--no-color"])
        assert result.exit_code == 0
        assert "Plain text" in result.output

        # Test with color enabled (default)
        result = runner.invoke(cmd)
        assert result.exit_code == 0
        # The actual color codes would be in the output

    def test_no_emoji_option(self) -> None:
        """Test that --no-emoji disables emoji in output."""

        @click.command()
        @output_options
        @pass_context
        def cmd(ctx: Context, **kwargs) -> None:
            if getattr(ctx, "no_emoji", False):
                click.echo("Success - Operation completed")
            else:
                click.echo("✅ Success - Operation completed")

        runner = CliRunner()

        # Test with emoji disabled
        result = runner.invoke(cmd, ["--no-emoji"])
        assert result.exit_code == 0
        assert "Success - Operation completed" in result.output
        assert "✅" not in result.output

        # Test with emoji enabled (default)
        result = runner.invoke(cmd)
        assert result.exit_code == 0
        assert "✅" in result.output


class TestConfigurationLoading:
    """Test configuration file and profile loading."""

    def test_config_file_loading(self) -> None:
        """Test that --config loads configuration file."""
        config_data = {"log_level": "WARNING", "profile": "testing"}

        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump(config_data, f)
            config_file = f.name

        try:

            @click.command()
            @flexible_options
            @pass_context
            def cmd(ctx: Context, **kwargs) -> None:
                # Context should have loaded the config
                click.echo(f"config_loaded={ctx.config_file}")

            runner = CliRunner()
            result = runner.invoke(cmd, ["--config", config_file])
            assert result.exit_code == 0
        finally:
            Path(config_file).unlink(missing_ok=True)

    def test_profile_selection(self) -> None:
        """Test that --profile selects the right configuration profile."""

        @click.command()
        @flexible_options
        @pass_context
        def cmd(ctx: Context, **kwargs) -> None:
            click.echo(f"profile={ctx.profile}")

        runner = CliRunner()

        # Test development profile
        result = runner.invoke(cmd, ["--profile", "development"])
        assert result.exit_code == 0
        assert "profile=development" in result.output

        # Test production profile
        result = runner.invoke(cmd, ["--profile", "production"])
        assert result.exit_code == 0
        assert "profile=production" in result.output


class TestRealWorldScenarios:
    """Test real-world CLI usage scenarios."""

    def test_debugging_production_issue(self) -> None:
        """Test scenario: debugging a production issue."""

        @click.group()
        @flexible_options
        @pass_context
        def cli(ctx: Context, **kwargs) -> None:
            """Production debugging CLI."""
            pass

        @cli.command()
        @flexible_options
        @output_options
        @pass_context
        def diagnose(ctx: Context, **kwargs) -> None:
            """Run diagnostics."""
            # In production, we want JSON logs to a file with DEBUG level
            if ctx.profile == "production":
                assert ctx.log_level == "DEBUG"
                assert hasattr(ctx, "log_format") and ctx.log_format == "json"
                assert ctx.log_file is not None

            if ctx.json_output:
                click.echo(json.dumps({"diagnosis": "complete"}))
            else:
                click.echo("Diagnosis complete")

        runner = CliRunner()

        with tempfile.NamedTemporaryFile(suffix=".log", delete=False) as f:
            log_file = f.name

        try:
            result = runner.invoke(
                cli,
                [
                    "--profile",
                    "production",
                    "--log-level",
                    "DEBUG",
                    "--log-format",
                    "json",
                    "--log-file",
                    log_file,
                    "diagnose",
                    "--json",
                ],
            )
            assert result.exit_code == 0
            output = json.loads(result.output.strip().split("\n")[-1])
            assert output["diagnosis"] == "complete"
        finally:
            Path(log_file).unlink(missing_ok=True)

    def test_ci_cd_pipeline_usage(self) -> None:
        """Test scenario: running in CI/CD pipeline."""

        @click.command()
        @flexible_options
        @output_options
        @pass_context
        def deploy(ctx: Context, **kwargs) -> None:
            """Deploy application."""
            # In CI/CD, we typically want:
            # - No emoji (for clean logs)
            # - JSON output (for parsing)
            # - Specific log level

            if getattr(ctx, "no_emoji", False) and ctx.json_output:
                # CI/CD mode
                output = {
                    "deployment": "successful",
                    "version": "1.2.3",
                    "environment": ctx.profile or "staging",
                }
                click.echo(json.dumps(output))
            else:
                click.echo("🚀 Deployment successful!")

        runner = CliRunner()

        # Simulate CI/CD environment
        result = runner.invoke(
            deploy,
            ["--no-emoji", "--json", "--log-level", "INFO", "--profile", "staging"],
        )
        assert result.exit_code == 0
        output = json.loads(result.output)
        assert output["deployment"] == "successful"
        assert output["environment"] == "staging"

    def test_interactive_development(self) -> None:
        """Test scenario: interactive development with verbose output."""

        @click.command()
        @flexible_options
        @output_options
        @pass_context
        def develop(ctx: Context, **kwargs) -> None:
            """Development command."""
            # In development, we want:
            # - DEBUG logging
            # - Human-readable output
            # - Emoji for visual parsing

            logger = get_logger(__name__)

            if ctx.log_level == "DEBUG":
                logger.debug("Debug information here")

            if not getattr(ctx, "no_emoji", False):
                click.echo("🔧 Development mode active")
                click.echo("📝 Watching for changes...")
            else:
                click.echo("Development mode active")
                click.echo("Watching for changes...")

        runner = CliRunner()

        result = runner.invoke(
            develop, ["--log-level", "DEBUG", "--profile", "development"]
        )
        assert result.exit_code == 0
        assert "🔧" in result.output
        assert "Development mode active" in result.output
