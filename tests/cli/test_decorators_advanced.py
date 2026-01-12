#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for CLI decorator option inheritance and environment variables."""

from __future__ import annotations

import click
from click.testing import CliRunner
from provide.testkit import FoundationTestCase

from provide.foundation.cli.decorators import (
    flexible_options,
    logging_options,
    output_options,
    version_option,
)


class TestVersionOption(FoundationTestCase):
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


class TestOptionInheritance(FoundationTestCase):
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


class TestEnvironmentVariables(FoundationTestCase):
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


# 🧱🏗️🔚
