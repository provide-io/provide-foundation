#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for combined CLI decorators."""

from __future__ import annotations

import click
from click.testing import CliRunner
from provide.testkit import FoundationTestCase

from provide.foundation.cli.decorators import flexible_options, standard_options


class TestFlexibleOptions(FoundationTestCase):
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


class TestStandardOptions(FoundationTestCase):
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


# 🧱🏗️🔚
