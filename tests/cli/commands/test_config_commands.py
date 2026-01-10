#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for CLI config commands."""

from __future__ import annotations

import json
from pathlib import Path

from provide.testkit import FoundationTestCase
import pytest

from provide.foundation.config.bootstrap import discover_and_register_configs


class TestConfigCommandImport(FoundationTestCase):
    """Test config command can be imported."""

    def setup_method(self) -> None:
        """Set up test environment."""
        super().setup_method()
        # Register configs after Foundation reset
        discover_and_register_configs()

    def test_config_command_imports(self) -> None:
        """Test that config command module can be imported."""
        from provide.foundation.cli.commands import config

        assert config is not None

    def test_config_group_exists(self) -> None:
        """Test config group exists."""
        from provide.foundation.cli.commands.config import config_group

        assert config_group is not None


class TestConfigSchemaCommand(FoundationTestCase):
    """Test config schema command."""

    def setup_method(self) -> None:
        """Set up test environment."""
        super().setup_method()
        # Register configs after Foundation reset
        discover_and_register_configs()

    def test_schema_command_help(self) -> None:
        """Test that schema command help works."""
        try:
            from click.testing import CliRunner

            from provide.foundation.cli.commands.config import config_group

            runner = CliRunner()
            result = runner.invoke(config_group, ["schema", "--help"])

            assert result.exit_code == 0
            assert "Display all available configuration options" in result.output
        except ImportError:
            pytest.skip("Click not available")

    def test_schema_command_default_format(self) -> None:
        """Test schema command with default (human) format."""
        try:
            from click.testing import CliRunner

            from provide.foundation.cli.commands.config import config_group

            runner = CliRunner()
            result = runner.invoke(config_group, ["schema"])

            # Should succeed
            assert result.exit_code == 0
            # Should have human-readable output
            assert "FOUNDATION CONFIGURATION SCHEMA" in result.output
        except ImportError:
            pytest.skip("Click not available")

    def test_schema_command_json_format(self) -> None:
        """Test schema command with JSON format."""
        try:
            from click.testing import CliRunner

            from provide.foundation.cli.commands.config import config_group

            runner = CliRunner()
            result = runner.invoke(config_group, ["schema", "--format", "json"])

            assert result.exit_code == 0
            # Should be valid JSON
            data = json.loads(result.output)
            assert "version" in data
            assert "configs" in data
        except ImportError:
            pytest.skip("Click not available")

    def test_schema_command_yaml_format(self) -> None:
        """Test schema command with YAML format."""
        try:
            from click.testing import CliRunner

            from provide.foundation.cli.commands.config import config_group

            runner = CliRunner()
            result = runner.invoke(config_group, ["schema", "--format", "yaml"])

            assert result.exit_code == 0
            # Should have YAML markers
            assert "version:" in result.output
            assert "configs:" in result.output
        except ImportError:
            pytest.skip("Click not available")

    def test_schema_command_markdown_format(self) -> None:
        """Test schema command with Markdown format."""
        try:
            from click.testing import CliRunner

            from provide.foundation.cli.commands.config import config_group

            runner = CliRunner()
            result = runner.invoke(config_group, ["schema", "--format", "markdown"])

            assert result.exit_code == 0
            # Should have markdown markers
            assert "#" in result.output
            assert "|" in result.output
        except ImportError:
            pytest.skip("Click not available")

    def test_schema_command_env_only(self) -> None:
        """Test schema command with env-only flag."""
        try:
            from click.testing import CliRunner

            from provide.foundation.cli.commands.config import config_group

            runner = CliRunner()
            result = runner.invoke(config_group, ["schema", "--env-only", "--format", "json"])

            assert result.exit_code == 0
            data = json.loads(result.output)
            # All fields should have env_var
            for config_data in data["configs"].values():
                for field_data in config_data["fields"].values():
                    assert "env_var" in field_data
        except ImportError:
            pytest.skip("Click not available")

    def test_schema_command_category_filter(self) -> None:
        """Test schema command with category filter."""
        try:
            from click.testing import CliRunner

            from provide.foundation.cli.commands.config import config_group

            runner = CliRunner()
            result = runner.invoke(config_group, ["schema", "--category", "logger"])

            assert result.exit_code == 0
            # Should mention logger
            assert "logger" in result.output.lower() or "Logger" in result.output
        except ImportError:
            pytest.skip("Click not available")

    def test_schema_command_output_file(self, tmp_path: Path) -> None:
        """Test schema command with output file."""
        try:
            from click.testing import CliRunner

            from provide.foundation.cli.commands.config import config_group

            output_file = tmp_path / "schema.txt"
            runner = CliRunner()
            result = runner.invoke(config_group, ["schema", "--output", str(output_file)])

            assert result.exit_code == 0
            # Should have success message
            assert "written to" in result.output.lower() or output_file.name in result.output

            # File should exist
            assert output_file.exists()
            # File should have content
            content = output_file.read_text()
            assert len(content) > 0
            assert "FOUNDATION CONFIGURATION SCHEMA" in content
        except ImportError:
            pytest.skip("Click not available")

    def test_schema_command_output_json_file(self, tmp_path: Path) -> None:
        """Test schema command with JSON output file."""
        try:
            from click.testing import CliRunner

            from provide.foundation.cli.commands.config import config_group

            output_file = tmp_path / "schema.json"
            runner = CliRunner()
            result = runner.invoke(config_group, ["schema", "--format", "json", "--output", str(output_file)])

            assert result.exit_code == 0
            assert output_file.exists()

            # Should be valid JSON
            content = output_file.read_text()
            data = json.loads(content)
            assert "version" in data
        except ImportError:
            pytest.skip("Click not available")

    def test_schema_command_combined_options(self) -> None:
        """Test schema command with multiple options combined."""
        try:
            from click.testing import CliRunner

            from provide.foundation.cli.commands.config import config_group

            runner = CliRunner()
            result = runner.invoke(
                config_group,
                [
                    "schema",
                    "--format",
                    "json",
                    "--category",
                    "logger",
                    "--env-only",
                    "--show-sensitive",
                ],
            )

            assert result.exit_code == 0
            data = json.loads(result.output)
            assert isinstance(data, dict)
        except ImportError:
            pytest.skip("Click not available")


class TestConfigCommandRegistration(FoundationTestCase):
    """Test config command is registered with main CLI."""

    def setup_method(self) -> None:
        """Set up test environment."""
        super().setup_method()
        # Register configs after Foundation reset
        discover_and_register_configs()

    def test_config_command_registered_in_main_cli(self) -> None:
        """Test that config command is registered in main CLI."""
        try:
            from click.testing import CliRunner

            from provide.foundation.cli.main import cli

            runner = CliRunner()
            result = runner.invoke(cli, ["--help"])

            # Should have config in help
            assert "config" in result.output.lower()
        except ImportError:
            pytest.skip("Click not available")

    def test_config_schema_available_in_main_cli(self) -> None:
        """Test that config schema subcommand is available."""
        try:
            from click.testing import CliRunner

            from provide.foundation.cli.main import cli

            runner = CliRunner()
            result = runner.invoke(cli, ["config", "schema", "--help"])

            assert result.exit_code == 0
            assert "Display all available configuration options" in result.output
        except ImportError:
            pytest.skip("Click not available")

    def test_config_schema_executes_from_main_cli(self) -> None:
        """Test executing config schema from main CLI."""
        try:
            from click.testing import CliRunner

            from provide.foundation.cli.main import cli

            runner = CliRunner()
            result = runner.invoke(cli, ["config", "schema", "--format", "json"])

            assert result.exit_code == 0
            data = json.loads(result.output)
            assert "version" in data
        except ImportError:
            pytest.skip("Click not available")


# 🧱🏗️🔚
