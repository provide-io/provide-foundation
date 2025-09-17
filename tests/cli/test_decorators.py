"""Tests for CLI decorators."""

from pathlib import Path
import tempfile
from typing import Never

import click
from click.testing import CliRunner
import pytest

from provide.foundation.cli.decorators import (
    config_options,
    error_handler,
    flexible_options,
    logging_options,
    output_options,
    pass_context,
    standard_options,
    version_option,
)
from provide.foundation.context import CLIContext


class TestLoggingOptions:
    """Test logging_options decorator."""

    def test_adds_log_level_option(self) -> None:
        """Test that log-level option is added."""

        @click.command()
        @logging_options
        def cmd(**kwargs) -> None:
            click.echo(f"log_level={kwargs.get('log_level')}")

        runner = CliRunner()
        result = runner.invoke(cmd, ["--log-level", "DEBUG"])
        assert result.exit_code == 0
        assert "log_level=DEBUG" in result.output

    def test_adds_log_file_option(self) -> None:
        """Test that log-file option is added."""
        with tempfile.NamedTemporaryFile(delete=False) as f:
            log_file = f.name

        @click.command()
        @logging_options
        def cmd(**kwargs) -> None:
            click.echo(f"log_file={kwargs.get('log_file')}")

        runner = CliRunner()
        result = runner.invoke(cmd, ["--log-file", log_file])
        assert result.exit_code == 0
        # Path may be resolved to include /private prefix on macOS
        assert log_file in result.output or f"/private{log_file}" in result.output

        Path(log_file).unlink()

    def test_adds_log_format_option(self) -> None:
        """Test that log-format option is added."""

        @click.command()
        @logging_options
        def cmd(**kwargs) -> None:
            click.echo(f"log_format={kwargs.get('log_format')}")

        runner = CliRunner()
        result = runner.invoke(cmd, ["--log-format", "json"])
        assert result.exit_code == 0
        assert "log_format=json" in result.output

    def test_log_level_environment_variable(self) -> None:
        """Test that PROVIDE_LOG_LEVEL env var works."""

        @click.command()
        @logging_options
        def cmd(**kwargs) -> None:
            click.echo(f"log_level={kwargs.get('log_level')}")

        runner = CliRunner()
        with runner.isolated_filesystem():
            result = runner.invoke(cmd, env={"PROVIDE_LOG_LEVEL": "ERROR"})
            assert result.exit_code == 0
            assert "log_level=ERROR" in result.output

    def test_log_format_default(self) -> None:
        """Test that log-format defaults to key_value."""

        @click.command()
        @logging_options
        def cmd(**kwargs) -> None:
            click.echo(f"log_format={kwargs.get('log_format')}")

        runner = CliRunner()
        result = runner.invoke(cmd)
        assert result.exit_code == 0
        assert "log_format=key_value" in result.output

    def test_no_debug_option(self) -> None:
        """Test that --debug option is not added (removed as redundant)."""

        @click.command()
        @logging_options
        def cmd(**kwargs) -> None:
            pass

        runner = CliRunner()
        result = runner.invoke(cmd, ["--help"])
        assert result.exit_code == 0
        assert "--debug" not in result.output


class TestOutputOptions:
    """Test output_options decorator."""

    def test_adds_json_option(self) -> None:
        """Test that --json option is added."""

        @click.command()
        @output_options
        def cmd(**kwargs) -> None:
            click.echo(f"json_output={kwargs.get('json_output')}")

        runner = CliRunner()
        result = runner.invoke(cmd, ["--json"])
        assert result.exit_code == 0
        assert "json_output=True" in result.output

    def test_adds_no_color_option(self) -> None:
        """Test that --no-color option is added."""

        @click.command()
        @output_options
        def cmd(**kwargs) -> None:
            click.echo(f"no_color={kwargs.get('no_color')}")

        runner = CliRunner()
        result = runner.invoke(cmd, ["--no-color"])
        assert result.exit_code == 0
        assert "no_color=True" in result.output

    def test_adds_no_emoji_option(self) -> None:
        """Test that --no-emoji option is added."""

        @click.command()
        @output_options
        def cmd(**kwargs) -> None:
            click.echo(f"no_emoji={kwargs.get('no_emoji')}")

        runner = CliRunner()
        result = runner.invoke(cmd, ["--no-emoji"])
        assert result.exit_code == 0
        assert "no_emoji=True" in result.output

    def test_no_verbose_or_quiet_options(self) -> None:
        """Test that --verbose and --quiet are not added (removed as redundant)."""

        @click.command()
        @output_options
        def cmd(**kwargs) -> None:
            pass

        runner = CliRunner()
        result = runner.invoke(cmd, ["--help"])
        assert result.exit_code == 0
        assert "--verbose" not in result.output
        assert "--quiet" not in result.output


class TestConfigOptions:
    """Test config_options decorator."""

    def test_adds_config_option(self) -> None:
        """Test that --config option is added."""
        with tempfile.NamedTemporaryFile(suffix=".toml", delete=False) as f:
            config_file = f.name
            f.write(b"test = true")

        @click.command()
        @config_options
        def cmd(**kwargs) -> None:
            click.echo(f"config={kwargs.get('config')}")

        runner = CliRunner()
        result = runner.invoke(cmd, ["--config", config_file])
        assert result.exit_code == 0
        # Path may be resolved to include /private prefix on macOS
        assert config_file in result.output or f"/private{config_file}" in result.output

        Path(config_file).unlink()

    def test_adds_profile_option(self) -> None:
        """Test that --profile option is added."""

        @click.command()
        @config_options
        def cmd(**kwargs) -> None:
            click.echo(f"profile={kwargs.get('profile')}")

        runner = CliRunner()
        result = runner.invoke(cmd, ["--profile", "production"])
        assert result.exit_code == 0
        assert "profile=production" in result.output


class TestFlexibleOptions:
    """Test flexible_options decorator."""

    def test_combines_logging_and_config(self) -> None:
        """Test that flexible_options combines logging and config options."""

        @click.command()
        @flexible_options
        def cmd(**kwargs) -> None:
            click.echo(f"log_level={kwargs.get('log_level')}")
            click.echo(f"profile={kwargs.get('profile')}")

        runner = CliRunner()
        result = runner.invoke(cmd, ["--log-level", "INFO", "--profile", "dev"])
        assert result.exit_code == 0
        assert "log_level=INFO" in result.output
        assert "profile=dev" in result.output

    def test_no_output_options(self) -> None:
        """Test that flexible_options doesn't include output options."""

        @click.command()
        @flexible_options
        def cmd(**kwargs) -> None:
            pass

        runner = CliRunner()
        result = runner.invoke(cmd, ["--help"])
        assert result.exit_code == 0
        assert "--log-level" in result.output
        assert "--config" in result.output
        assert "--json" not in result.output  # Output options not included

    def test_can_be_used_on_groups_and_commands(self) -> None:
        """Test that flexible_options works on both groups and commands."""

        @click.group()
        @flexible_options
        def cli(**kwargs) -> None:
            pass

        @cli.command()
        @flexible_options
        def subcommand(**kwargs) -> None:
            click.echo(f"log_level={kwargs.get('log_level')}")

        runner = CliRunner()
        # Test at group level
        result = runner.invoke(cli, ["--log-level", "DEBUG", "subcommand"])
        assert result.exit_code == 0

        # Test at command level
        result = runner.invoke(cli, ["subcommand", "--log-level", "INFO"])
        assert result.exit_code == 0
        assert "log_level=INFO" in result.output


class TestStandardOptions:
    """Test standard_options decorator (for backward compatibility)."""

    def test_includes_all_options(self) -> None:
        """Test that standard_options includes all option groups."""

        @click.command()
        @standard_options
        def cmd(**kwargs) -> None:
            pass

        runner = CliRunner()
        result = runner.invoke(cmd, ["--help"])
        assert result.exit_code == 0
        # Logging options
        assert "--log-level" in result.output
        assert "--log-file" in result.output
        assert "--log-format" in result.output
        # Config options
        assert "--config" in result.output
        assert "--profile" in result.output
        # Output options
        assert "--json" in result.output
        assert "--no-color" in result.output
        assert "--no-emoji" in result.output


class TestPassContext:
    """Test pass_context decorator."""

    def test_creates_context_if_none(self) -> None:
        """Test that CLIContext is created if ctx.obj is None."""

        @click.command()
        @pass_context
        def cmd(ctx: CLIContext) -> None:
            assert isinstance(ctx, CLIContext)
            click.echo("context_created")

        runner = CliRunner()
        result = runner.invoke(cmd)
        assert result.exit_code == 0
        assert "context_created" in result.output

    def test_updates_context_from_options(self) -> None:
        """Test that CLIContext is updated with CLI options."""

        @click.command()
        @logging_options
        @output_options
        @pass_context
        def cmd(ctx: CLIContext, **kwargs) -> None:
            click.echo(f"log_level={getattr(ctx, 'log_level', None)}")
            click.echo(f"log_format={getattr(ctx, 'log_format', None)}")
            click.echo(f"json_output={getattr(ctx, 'json_output', None)}")

        runner = CliRunner()
        result = runner.invoke(
            cmd,
            ["--log-level", "WARNING", "--log-format", "json", "--json"],
        )
        assert result.exit_code == 0
        assert "log_level=WARNING" in result.output
        assert "log_format=json" in result.output
        assert "json_output=True" in result.output

    def test_removes_options_from_kwargs(self) -> None:
        """Test that options are removed from kwargs after processing."""

        @click.command()
        @logging_options
        @pass_context
        def cmd(ctx: CLIContext, **kwargs) -> None:
            # These should have been removed from kwargs
            assert "log_level" not in kwargs
            assert "log_file" not in kwargs
            assert "log_format" not in kwargs
            click.echo("options_removed")

        runner = CliRunner()
        result = runner.invoke(cmd, ["--log-level", "DEBUG"])
        assert result.exit_code == 0
        assert "options_removed" in result.output


class TestErrorHandler:
    """Test error_handler decorator."""

    def test_handles_exceptions_gracefully(self) -> None:
        """Test that exceptions are handled gracefully."""

        @click.command()
        @error_handler
        def cmd(**kwargs) -> Never:
            raise ValueError("Test error")

        runner = CliRunner()
        result = runner.invoke(cmd)
        assert result.exit_code == 1
        assert "Error: Test error" in result.output

    def test_shows_traceback_in_debug_mode(self) -> None:
        """Test that traceback is shown in debug mode."""

        @click.command()
        @click.option("--debug", is_flag=True, default=False)
        @error_handler
        def cmd(debug=False, **kwargs) -> Never:
            raise ValueError("Test error")

        runner = CliRunner()
        # When debug=True, the exception should propagate
        with pytest.raises(ValueError):
            runner.invoke(
                cmd,
                ["--debug"],
                standalone_mode=False,
                catch_exceptions=False,
            )

    def test_handles_keyboard_interrupt(self) -> None:
        """Test that KeyboardInterrupt is handled."""

        @click.command()
        @error_handler
        def cmd(**kwargs) -> Never:
            raise KeyboardInterrupt

        runner = CliRunner()
        result = runner.invoke(cmd)
        assert result.exit_code == 130  # Standard exit code for SIGINT
        assert "Interrupted by user" in result.output


class TestVersionOption:
    """Test version_option decorator."""

    def test_adds_version_option(self) -> None:
        """Test that --version option is added."""

        @click.command()
        @version_option(version="1.2.3", prog_name="test-cli")
        def cmd() -> None:
            pass

        runner = CliRunner()
        result = runner.invoke(cmd, ["--version"])
        assert result.exit_code == 0
        assert "test-cli version 1.2.3" in result.output


class TestOptionInheritance:
    """Test that options can be inherited from parent commands."""

    def test_subcommand_inherits_parent_options(self) -> None:
        """Test that subcommands can access parent command options."""

        @click.group()
        @flexible_options
        @click.pass_context
        def cli(ctx, **kwargs) -> None:
            ctx.ensure_object(dict)
            for key, value in kwargs.items():
                if value is not None:
                    ctx.obj[key] = value

        @cli.command()
        @click.pass_context
        def subcommand(ctx) -> None:
            parent_log_level = ctx.obj.get("log_level")
            click.echo(f"parent_log_level={parent_log_level}")

        runner = CliRunner()
        result = runner.invoke(cli, ["--log-level", "ERROR", "subcommand"])
        assert result.exit_code == 0
        assert "parent_log_level=ERROR" in result.output

    def test_subcommand_can_override_parent_options(self) -> None:
        """Test that subcommands can override parent options."""

        @click.group()
        @flexible_options
        @click.pass_context
        def cli(ctx, **kwargs) -> None:
            ctx.ensure_object(dict)
            ctx.obj["log_level"] = kwargs.get("log_level", "INFO")

        @cli.command()
        @flexible_options
        @click.pass_context
        def subcommand(ctx, **kwargs) -> None:
            # Subcommand's option should take precedence
            log_level = kwargs.get("log_level") or ctx.obj.get("log_level")
            click.echo(f"effective_log_level={log_level}")

        runner = CliRunner()
        # Parent sets INFO, subcommand overrides with DEBUG
        result = runner.invoke(
            cli,
            ["--log-level", "INFO", "subcommand", "--log-level", "DEBUG"],
        )
        assert result.exit_code == 0
        assert "effective_log_level=DEBUG" in result.output


class TestEnvironmentVariables:
    """Test environment variable support."""

    def test_all_options_support_env_vars(self) -> None:
        """Test that all options can be set via environment variables."""

        @click.command()
        @flexible_options
        @output_options
        def cmd(**kwargs) -> None:
            click.echo(f"log_level={kwargs.get('log_level')}")
            click.echo(f"log_format={kwargs.get('log_format')}")
            click.echo(f"profile={kwargs.get('profile')}")
            click.echo(f"json_output={kwargs.get('json_output')}")

        runner = CliRunner()
        env = {
            "PROVIDE_LOG_LEVEL": "WARNING",
            "PROVIDE_LOG_FORMAT": "json",
            "PROVIDE_PROFILE": "production",
            "PROVIDE_JSON_OUTPUT": "true",
        }

        result = runner.invoke(cmd, env=env)
        assert result.exit_code == 0
        assert "log_level=WARNING" in result.output
        assert "log_format=json" in result.output
        assert "profile=production" in result.output
        assert "json_output=True" in result.output

    def test_cli_args_override_env_vars(self) -> None:
        """Test that CLI arguments override environment variables."""

        @click.command()
        @logging_options
        def cmd(**kwargs) -> None:
            click.echo(f"log_level={kwargs.get('log_level')}")

        runner = CliRunner()
        env = {"PROVIDE_LOG_LEVEL": "ERROR"}

        result = runner.invoke(cmd, ["--log-level", "DEBUG"], env=env)
        assert result.exit_code == 0
        assert "log_level=DEBUG" in result.output  # CLI arg wins
