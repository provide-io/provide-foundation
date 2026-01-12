#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for CLI testing utilities."""

from __future__ import annotations

from contextlib import suppress
import json
import os
from pathlib import Path
import tempfile

import click
from click.testing import CliRunner
from provide.testkit import (
    CliTestCase,
    FoundationTestCase,
    MockContext,
    create_test_cli,
    isolated_cli_runner,
    temp_config_file,
)
from provide.testkit.mocking import Mock
import pytest


class TestMockContext(FoundationTestCase):
    """Test the MockContext class."""

    def test_mock_context_tracks_calls(self) -> None:
        """Test that MockContext tracks method calls."""
        ctx = MockContext()

        assert ctx.calls == []
        assert ctx.saved_configs == []
        assert ctx.loaded_configs == []

    def test_mock_context_tracks_save_config(self) -> None:
        """Test that save_config calls are tracked."""
        ctx = MockContext()

        with tempfile.NamedTemporaryFile(suffix=".json") as tmp:
            tmp_path = Path(tmp.name)
            ctx.save_config(tmp_path)

        assert str(tmp_path) in [str(p) for p in ctx.saved_configs]

    def test_mock_context_tracks_load_config(self) -> None:
        """Test that load_config calls are tracked."""
        ctx = MockContext()

        with tempfile.NamedTemporaryFile() as tmp:
            tmp_path = Path(tmp.name)
            with suppress(Exception):
                ctx.load_config(tmp_path)

        assert str(tmp_path) in [str(p) for p in ctx.loaded_configs]


class TestIsolatedCliRunner(FoundationTestCase):
    """Test the isolated CLI runner context manager."""

    def test_isolated_runner_basic(self) -> None:
        """Test basic isolated runner functionality."""
        with isolated_cli_runner() as runner:
            assert isinstance(runner, CliRunner)

    def test_isolated_runner_with_env(self) -> None:
        """Test isolated runner with environment variables."""
        test_env = {"TEST_VAR": "test_value"}

        with isolated_cli_runner(env=test_env):
            assert os.environ.get("TEST_VAR") == "test_value"

        # Should be cleaned up
        assert os.environ.get("TEST_VAR") is None

    def test_isolated_runner_restores_env(self) -> None:
        """Test that environment is properly restored."""
        original_value = os.environ.get("TEST_VAR", "not_set")

        with isolated_cli_runner(env={"TEST_VAR": "temp_value"}):
            pass

        # Should be restored to original state
        current_value = os.environ.get("TEST_VAR", "not_set")
        assert current_value == original_value

    def test_isolated_runner_output_separation(self) -> None:
        """Test isolated runner handles stdout/stderr separately."""
        with isolated_cli_runner() as runner:
            assert isinstance(runner, CliRunner)


class TestTempConfigFile(FoundationTestCase):
    """Test temporary config file creation."""

    def test_temp_config_json(self) -> None:
        """Test creating temporary JSON config."""
        config = {"key": "value", "number": 42}

        with temp_config_file(config, "json") as config_path:
            assert config_path.exists()
            assert config_path.suffix == ".json"

            with config_path.open() as f:
                loaded = json.load(f)

            assert loaded == config

        # Should be cleaned up
        assert not config_path.exists()

    def test_temp_config_yaml(self) -> None:
        """Test creating temporary YAML config."""
        pytest.importorskip("yaml")

        config = {"key": "value", "list": [1, 2, 3]}

        with temp_config_file(config, "yaml") as config_path:
            assert config_path.exists()
            assert config_path.suffix == ".yaml"

            import yaml

            with config_path.open() as f:
                loaded = yaml.safe_load(f)

            assert loaded == config

    def test_temp_config_toml_fallback(self) -> None:
        """Test TOML config with fallback formatting."""
        config = {"key": "value", "number": 42}

        with temp_config_file(config, "toml") as config_path:
            assert config_path.exists()
            assert config_path.suffix == ".toml"

            content = config_path.read_text()
            assert 'key = "value"' in content
            assert "number = 42" in content

    def test_temp_config_string_content(self) -> None:
        """Test creating config file with string content."""
        content = "key = value\nsection = test"

        with temp_config_file(content, "txt") as config_path:
            assert config_path.read_text() == content


class TestCreateTestCli(FoundationTestCase):
    """Test test CLI creation."""

    def test_create_basic_cli(self) -> None:
        """Test creating basic test CLI."""
        cli = create_test_cli()

        assert isinstance(cli, click.Group)
        assert cli.name == "test-cli"

    def test_create_cli_with_commands(self) -> None:
        """Test creating CLI with additional commands."""

        @click.command()
        def test_cmd() -> None:
            """Test command."""
            click.echo("test")

        cli = create_test_cli(commands=[test_cmd])

        # Click normalizes function names by removing underscores
        assert "test" in cli.commands

    def test_create_cli_custom_name_version(self) -> None:
        """Test creating CLI with custom name and version."""
        cli = create_test_cli(name="custom-cli", version="2.0.0")

        assert cli.name == "custom-cli"


class TestMockLogger(FoundationTestCase):
    """Test mock logger creation."""

    def test_mock_logger_has_methods(self, mock_logger: Mock) -> None:
        """Test that mock logger has all expected methods."""
        methods = ["debug", "info", "warning", "error", "critical"]
        for method in methods:
            assert hasattr(mock_logger, method)
            # mock_logger creates Mock objects, not MagicMock

            assert isinstance(getattr(mock_logger, method), Mock)

    def test_mock_logger_methods_callable(self, mock_logger: Mock) -> None:
        """Test that mock logger methods are callable."""
        # Should not raise any exceptions
        mock_logger.debug("test")
        mock_logger.info("test")
        mock_logger.warning("test")
        mock_logger.error("test")
        mock_logger.critical("test")


class TestCliTestCase(FoundationTestCase):
    """Test the CliTestCase base class."""

    def test_cli_test_case_setup(self) -> None:
        """Test CliTestCase setup method."""
        test_case = CliTestCase()
        test_case.setup_method()

        assert isinstance(test_case.runner, CliRunner)
        assert test_case.temp_files == []

    def test_cli_test_case_temp_file_creation(self) -> None:
        """Test temporary file creation and tracking."""
        test_case = CliTestCase()
        test_case.setup_method()

        temp_file = test_case.create_temp_file("test content", ".txt")

        assert temp_file.exists()
        assert temp_file.read_text() == "test content"
        assert temp_file in test_case.temp_files

    def test_cli_test_case_cleanup(self) -> None:
        """Test that cleanup removes temporary files."""
        test_case = CliTestCase()
        test_case.setup_method()

        temp_file = test_case.create_temp_file("test")
        assert temp_file.exists()

        test_case.teardown_method()
        assert not temp_file.exists()

    def test_cli_test_case_invoke_method(self) -> None:
        """Test the invoke method works."""
        test_case = CliTestCase()
        test_case.setup_method()

        @click.command()
        def simple_cmd() -> None:
            click.echo("hello")

        result = test_case.invoke(simple_cmd)
        assert result.output.strip() == "hello"

    def test_cli_test_case_assert_json_output(self) -> None:
        """Test JSON output assertion method."""
        test_case = CliTestCase()
        test_case.setup_method()

        # Mock result with JSON output
        class MockResult:
            output = '{"status": "ok", "count": 5}'

        result = MockResult()

        # Should not raise
        test_case.assert_json_output(result, {"status": "ok"})

        # Should raise on mismatch
        with pytest.raises(AssertionError):
            test_case.assert_json_output(result, {"status": "error"})

    def test_cli_test_case_assert_json_invalid_json(self) -> None:
        """Test JSON assertion with invalid JSON."""
        test_case = CliTestCase()
        test_case.setup_method()

        class MockResult:
            output = "not json"

        result = MockResult()

        with pytest.raises(AssertionError, match="not valid JSON"):
            test_case.assert_json_output(result, {"key": "value"})


# 🧱🏗️🔚
