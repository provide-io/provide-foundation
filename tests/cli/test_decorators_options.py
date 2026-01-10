#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for CLI decorators."""

from __future__ import annotations

from pathlib import Path
import tempfile

import click
from click.testing import CliRunner
from provide.testkit import FoundationTestCase

from provide.foundation.cli.decorators import (
    config_options,
    logging_options,
    output_options,
)


class TestLoggingOptions(FoundationTestCase):
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


class TestOutputOptions(FoundationTestCase):
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


class TestConfigOptions(FoundationTestCase):
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


# 🧱🏗️🔚
