#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for CLI decorator context handling."""

from __future__ import annotations

from typing import Never

import click
from click.testing import CliRunner
from provide.testkit import FoundationTestCase
import pytest

from provide.foundation.cli.decorators import (
    error_handler,
    logging_options,
    output_options,
    pass_context,
)
from provide.foundation.context import CLIContext


class TestPassContext(FoundationTestCase):
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


class TestErrorHandler(FoundationTestCase):
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


# 🧱🏗️🔚
