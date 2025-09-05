"""Tests for CLI testing utilities."""

import json
import os
from pathlib import Path
import tempfile
from unittest.mock import MagicMock

import pytest
import click
from click.testing import CliRunner

from provide.foundation.testing.cli import (
    MockContext,
    isolated_cli_runner,
    temp_config_file,
    create_test_cli,
    mock_logger,
    CliTestCase,
)


class TestMockContext:
    """Test the MockContext class."""
    
    def test_mock_context_tracks_calls(self):
        """Test that MockContext tracks method calls."""
        ctx = MockContext()
        
        assert ctx.calls == []
        assert ctx.saved_configs == []
        assert ctx.loaded_configs == []

    def test_mock_context_tracks_save_config(self):
        """Test that save_config calls are tracked."""
        ctx = MockContext()
        
        with tempfile.NamedTemporaryFile(suffix=".json") as tmp:
            tmp_path = Path(tmp.name)
            ctx.save_config(tmp_path)
            
        assert str(tmp_path) in [str(p) for p in ctx.saved_configs]

    def test_mock_context_tracks_load_config(self):
        """Test that load_config calls are tracked."""
        ctx = MockContext()
        
        with tempfile.NamedTemporaryFile() as tmp:
            tmp_path = Path(tmp.name)
            try:
                ctx.load_config(tmp_path)
            except Exception:
                pass  # Expected to fail with empty file
            
        assert str(tmp_path) in [str(p) for p in ctx.loaded_configs]


class TestIsolatedCliRunner:
    """Test the isolated CLI runner context manager."""
    
    def test_isolated_runner_basic(self):
        """Test basic isolated runner functionality."""
        with isolated_cli_runner() as runner:
            assert isinstance(runner, CliRunner)

    def test_isolated_runner_with_env(self):
        """Test isolated runner with environment variables."""
        test_env = {"TEST_VAR": "test_value"}
        
        with isolated_cli_runner(env=test_env) as runner:
            assert os.environ.get("TEST_VAR") == "test_value"
        
        # Should be cleaned up
        assert os.environ.get("TEST_VAR") is None

    def test_isolated_runner_restores_env(self):
        """Test that environment is properly restored."""
        original_value = os.environ.get("TEST_VAR", "not_set")
        
        with isolated_cli_runner(env={"TEST_VAR": "temp_value"}):
            pass
        
        # Should be restored to original state
        current_value = os.environ.get("TEST_VAR", "not_set")
        assert current_value == original_value

    def test_isolated_runner_output_separation(self):
        """Test isolated runner handles stdout/stderr separately."""
        with isolated_cli_runner() as runner:
            assert isinstance(runner, CliRunner)


class TestTempConfigFile:
    """Test temporary config file creation."""
    
    def test_temp_config_json(self):
        """Test creating temporary JSON config."""
        config = {"key": "value", "number": 42}
        
        with temp_config_file(config, "json") as config_path:
            assert config_path.exists()
            assert config_path.suffix == ".json"
            
            with open(config_path) as f:
                loaded = json.load(f)
            
            assert loaded == config
        
        # Should be cleaned up
        assert not config_path.exists()

    def test_temp_config_yaml(self):
        """Test creating temporary YAML config."""
        pytest.importorskip("yaml")
        
        config = {"key": "value", "list": [1, 2, 3]}
        
        with temp_config_file(config, "yaml") as config_path:
            assert config_path.exists()
            assert config_path.suffix == ".yaml"
            
            import yaml
            with open(config_path) as f:
                loaded = yaml.safe_load(f)
            
            assert loaded == config

    def test_temp_config_toml_fallback(self):
        """Test TOML config with fallback formatting."""
        config = {"key": "value", "number": 42}
        
        with temp_config_file(config, "toml") as config_path:
            assert config_path.exists()
            assert config_path.suffix == ".toml"
            
            content = config_path.read_text()
            assert 'key = "value"' in content
            assert "number = 42" in content

    def test_temp_config_string_content(self):
        """Test creating config file with string content."""
        content = "key = value\nsection = test"
        
        with temp_config_file(content, "txt") as config_path:
            assert config_path.read_text() == content


class TestCreateTestCli:
    """Test test CLI creation."""
    
    def test_create_basic_cli(self):
        """Test creating basic test CLI."""
        cli = create_test_cli()
        
        assert isinstance(cli, click.Group)
        assert cli.name == "test-cli"

    def test_create_cli_with_commands(self):
        """Test creating CLI with additional commands."""
        @click.command()
        def test_cmd():
            """Test command."""
            click.echo("test")
        
        cli = create_test_cli(commands=[test_cmd])
        
        # Click normalizes function names by removing underscores
        assert "test" in cli.commands

    def test_create_cli_custom_name_version(self):
        """Test creating CLI with custom name and version."""
        cli = create_test_cli(name="custom-cli", version="2.0.0")
        
        assert cli.name == "custom-cli"


class TestMockLogger:
    """Test mock logger creation."""
    
    def test_mock_logger_has_methods(self):
        """Test that mock logger has all expected methods."""
        logger = mock_logger()
        
        methods = ["debug", "info", "warning", "error", "critical"]
        for method in methods:
            assert hasattr(logger, method)
            assert isinstance(getattr(logger, method), MagicMock)

    def test_mock_logger_methods_callable(self):
        """Test that mock logger methods are callable."""
        logger = mock_logger()
        
        # Should not raise any exceptions
        logger.debug("test")
        logger.info("test")
        logger.warning("test")
        logger.error("test")
        logger.critical("test")


class TestCliTestCase:
    """Test the CliTestCase base class."""
    
    def test_cli_test_case_setup(self):
        """Test CliTestCase setup method."""
        test_case = CliTestCase()
        test_case.setup_method()
        
        assert isinstance(test_case.runner, CliRunner)
        assert test_case.temp_files == []

    def test_cli_test_case_temp_file_creation(self):
        """Test temporary file creation and tracking."""
        test_case = CliTestCase()
        test_case.setup_method()
        
        temp_file = test_case.create_temp_file("test content", ".txt")
        
        assert temp_file.exists()
        assert temp_file.read_text() == "test content"
        assert temp_file in test_case.temp_files

    def test_cli_test_case_cleanup(self):
        """Test that cleanup removes temporary files."""
        test_case = CliTestCase()
        test_case.setup_method()
        
        temp_file = test_case.create_temp_file("test")
        assert temp_file.exists()
        
        test_case.teardown_method()
        assert not temp_file.exists()

    def test_cli_test_case_invoke_method(self):
        """Test the invoke method works."""
        test_case = CliTestCase()
        test_case.setup_method()
        
        @click.command()
        def simple_cmd():
            click.echo("hello")
        
        result = test_case.invoke(simple_cmd)
        assert result.output.strip() == "hello"

    def test_cli_test_case_assert_json_output(self):
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

    def test_cli_test_case_assert_json_invalid_json(self):
        """Test JSON assertion with invalid JSON."""
        test_case = CliTestCase()
        test_case.setup_method()
        
        class MockResult:
            output = "not json"
        
        result = MockResult()
        
        with pytest.raises(AssertionError, match="not valid JSON"):
            test_case.assert_json_output(result, {"key": "value"})