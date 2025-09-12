"""Comprehensive tests for CLI testing utilities to improve code coverage."""

import json
import os
from pathlib import Path
import sys
import tempfile
from unittest.mock import Mock, patch

import click
from click.testing import CliRunner
import pytest

from provide.testkit import (
    CliTestCase,
    MockContext,
    create_test_cli,
    isolated_cli_runner,
    temp_config_file,
)


class TestMockContext:
    """Test MockContext functionality."""

    def test_mock_context_initialization(self):
        """Test MockContext initializes with tracking."""
        mock_ctx = MockContext()
        assert mock_ctx.calls == []
        assert mock_ctx.saved_configs == []
        assert mock_ctx.loaded_configs == []

    def test_mock_context_save_config_tracking(self):
        """Test MockContext tracks save_config calls."""
        mock_ctx = MockContext()
        test_path = Path("/test/config.json")

        with patch.object(MockContext.__bases__[0], "save_config") as mock_super_save:
            mock_ctx.save_config(test_path)

        assert test_path in mock_ctx.saved_configs
        mock_super_save.assert_called_once_with(test_path)

    def test_mock_context_load_config_tracking(self):
        """Test MockContext tracks load_config calls."""
        mock_ctx = MockContext()
        test_path = Path("/test/config.json")

        with patch.object(MockContext.__bases__[0], "load_config") as mock_super_load:
            mock_ctx.load_config(test_path)

        assert test_path in mock_ctx.loaded_configs
        mock_super_load.assert_called_once_with(test_path)

    def test_mock_context_save_config_with_string_path(self):
        """Test MockContext save_config with string path."""
        mock_ctx = MockContext()
        test_path = "/test/config.json"

        with patch.object(MockContext.__bases__[0], "save_config") as mock_super_save:
            mock_ctx.save_config(test_path)

        assert test_path in mock_ctx.saved_configs

    def test_mock_context_load_config_with_string_path(self):
        """Test MockContext load_config with string path."""
        mock_ctx = MockContext()
        test_path = "/test/config.json"

        with patch.object(MockContext.__bases__[0], "load_config") as mock_super_load:
            mock_ctx.load_config(test_path)

        assert test_path in mock_ctx.loaded_configs


class TestIsolatedCliRunner:
    """Test isolated_cli_runner context manager."""

    def test_isolated_cli_runner_basic(self):
        """Test isolated_cli_runner basic functionality."""
        with isolated_cli_runner() as runner:
            assert isinstance(runner, CliRunner)

    def test_isolated_cli_runner_with_env_variables(self):
        """Test isolated_cli_runner with environment variables."""
        test_env = {"TEST_CLI_VAR": "test_value", "ANOTHER_VAR": "another_value"}

        with isolated_cli_runner(env=test_env):
            assert os.environ.get("TEST_CLI_VAR") == "test_value"
            assert os.environ.get("ANOTHER_VAR") == "another_value"

        # Variables should be restored
        assert os.environ.get("TEST_CLI_VAR") is None
        assert os.environ.get("ANOTHER_VAR") is None

    def test_isolated_cli_runner_preserves_existing_env(self):
        """Test isolated_cli_runner preserves existing environment variables."""
        # Set existing variable
        os.environ["EXISTING_VAR"] = "original_value"
        test_env = {"EXISTING_VAR": "modified_value"}

        try:
            with isolated_cli_runner(env=test_env):
                assert os.environ.get("EXISTING_VAR") == "modified_value"

            # Should be restored to original
            assert os.environ.get("EXISTING_VAR") == "original_value"
        finally:
            # Clean up
            os.environ.pop("EXISTING_VAR", None)

    def test_isolated_cli_runner_handles_missing_original_env(self):
        """Test isolated_cli_runner handles missing original environment variables."""
        # Ensure variable doesn't exist initially
        os.environ.pop("NON_EXISTENT_VAR", None)
        test_env = {"NON_EXISTENT_VAR": "new_value"}

        with isolated_cli_runner(env=test_env):
            assert os.environ.get("NON_EXISTENT_VAR") == "new_value"

        # Should be removed since it didn't exist originally
        assert os.environ.get("NON_EXISTENT_VAR") is None


class TestTempConfigFile:
    """Test temp_config_file context manager."""

    def test_temp_config_file_json_dict(self):
        """Test temp_config_file with JSON dict content."""
        config_data = {"key1": "value1", "key2": 42, "key3": True}

        with temp_config_file(config_data, "json") as config_path:
            assert config_path.exists()
            assert config_path.suffix == ".json"

            with open(config_path) as f:
                loaded_data = json.load(f)
            assert loaded_data == config_data

        # File should be cleaned up
        assert not config_path.exists()

    def test_temp_config_file_json_string(self):
        """Test temp_config_file with JSON string content."""
        config_string = '{"test": "json string"}'

        with temp_config_file(config_string, "json") as config_path:
            assert config_path.exists()
            assert config_path.suffix == ".json"

            with open(config_path) as f:
                content = f.read()
            assert content == config_string

    def test_temp_config_file_toml_dict_with_tomli_w(self):
        """Test temp_config_file with TOML dict content using tomli_w."""
        config_data = {"key1": "value1", "key2": 42}

        mock_tomli_w = Mock()
        mock_tomli_w.dumps.return_value = 'key1 = "value1"\nkey2 = 42\n'
        
        with patch.dict("sys.modules", {"tomli_w": mock_tomli_w}):
            with temp_config_file(config_data, "toml") as config_path:
                assert config_path.exists()
                assert config_path.suffix == ".toml"
                
                # Verify content was written
                content = config_path.read_text()
                assert 'key1 = "value1"' in content
                assert 'key2 = 42' in content

    def test_temp_config_file_toml_dict_fallback(self):
        """Test temp_config_file with TOML dict content using fallback."""
        config_data = {"string_key": "value1", "int_key": 42, "bool_key": True}

        # Remove tomli_w from sys.modules to simulate it not being installed
        import sys
        tomli_w_backup = sys.modules.pop('tomli_w', None)
        try:
            with temp_config_file(config_data, "toml") as config_path:
                assert config_path.exists()
                assert config_path.suffix == ".toml"

                with open(config_path) as f:
                    content = f.read()

                # Check fallback format
                assert 'string_key = "value1"' in content
                assert "int_key = 42" in content
                assert "bool_key = true" in content  # TOML uses lowercase for booleans
        finally:
            if tomli_w_backup is not None:
                sys.modules['tomli_w'] = tomli_w_backup

    def test_temp_config_file_yaml_dict_with_yaml(self):
        """Test temp_config_file with YAML dict content using PyYAML."""
        config_data = {"key1": "value1", "key2": [1, 2, 3]}

        mock_yaml = Mock()
        # Mock safe_dump to write something
        def mock_safe_dump(data, file):
            file.write("key1: value1\nkey2:\n- 1\n- 2\n- 3\n")
        mock_yaml.safe_dump = mock_safe_dump
        
        with patch.dict("sys.modules", {"yaml": mock_yaml}):
            with temp_config_file(config_data, "yaml") as config_path:
                assert config_path.exists()
                assert config_path.suffix == ".yaml"
                
                # Verify some content was written
                content = config_path.read_text()
                assert len(content) > 0

    def test_temp_config_file_yaml_dict_no_yaml_import_error(self):
        """Test temp_config_file with YAML dict content raises ImportError without PyYAML."""
        config_data = {"key1": "value1"}

        # Mock the import to raise ImportError
        import sys
        import builtins
        original_import = builtins.__import__
        
        def mock_import(name, *args, **kwargs):
            if name == 'yaml':
                raise ImportError("No module named 'yaml'")
            return original_import(name, *args, **kwargs)
        
        with patch('builtins.__import__', side_effect=mock_import):
            with pytest.raises(ImportError, match="PyYAML required for YAML testing"):
                with temp_config_file(config_data, "yaml") as config_path:
                    pass

    def test_temp_config_file_cleanup_on_exception(self):
        """Test temp_config_file cleans up file even on exception."""
        config_data = {"test": "data"}
        config_path = None

        try:
            with temp_config_file(config_data, "json") as path:
                config_path = path
                assert config_path.exists()
                raise ValueError("Test exception")
        except ValueError:
            pass

        # File should still be cleaned up
        assert config_path is not None
        assert not config_path.exists()


class TestCreateTestCli:
    """Test create_test_cli function."""

    def test_create_test_cli_basic(self):
        """Test create_test_cli basic functionality."""
        cli = create_test_cli()
        assert isinstance(cli, click.Group)
        assert cli.name == "test-cli"

    def test_create_test_cli_custom_name_version(self):
        """Test create_test_cli with custom name and version."""
        cli = create_test_cli(name="custom-cli", version="2.0.0")
        assert cli.name == "custom-cli"

    def test_create_test_cli_with_commands(self):
        """Test create_test_cli with additional commands."""

        @click.command()
        def test_cmd():
            """Test command."""
            click.echo("test command")

        @click.command()
        def another_cmd():
            """Another test command."""
            click.echo("another command")

        commands = [test_cmd, another_cmd]
        cli = create_test_cli(commands=commands)

        # Click normalizes command names - underscores become hyphens, but function names are used
        assert "test" in cli.commands or "test-cmd" in cli.commands
        assert "another" in cli.commands or "another-cmd" in cli.commands

    def test_create_test_cli_context_creation(self):
        """Test create_test_cli creates proper context."""
        cli = create_test_cli()
        runner = CliRunner()

        # Test that the CLI runs without error
        result = runner.invoke(cli, ["--help"])
        assert result.exit_code == 0

    def test_create_test_cli_no_commands(self):
        """Test create_test_cli with no additional commands."""
        cli = create_test_cli(commands=None)
        assert isinstance(cli, click.Group)
        # Should have no additional commands beyond the base group
        # (standard_options may add some options but not commands)


class TestMockLogger:
    """Test mock_logger function."""

    def test_mock_logger_creation(self, mock_logger):
        """Test mock_logger creates proper mock."""
        assert hasattr(mock_logger, "debug")
        assert hasattr(mock_logger, "info")
        assert hasattr(mock_logger, "warning")
        assert hasattr(mock_logger, "error")
        assert hasattr(mock_logger, "critical")

    def test_mock_logger_methods_callable(self, mock_logger):
        """Test mock_logger methods are callable."""
        # Should not raise exceptions
        mock_logger.debug("test message")
        mock_logger.info("test message")
        mock_logger.warning("test message")
        mock_logger.error("test message")
        mock_logger.critical("test message")

    def test_mock_logger_call_tracking(self, mock_logger):
        """Test mock_logger methods track calls."""

        mock_logger.debug("debug message")
        mock_logger.info("info message", extra="data")

        mock_logger.debug.assert_called_once_with("debug message")
        mock_logger.info.assert_called_once_with("info message", extra="data")


class TestCliTestCase:
    """Test CliTestCase base class."""

    def test_cli_test_case_setup(self):
        """Test CliTestCase setup_method."""
        test_case = CliTestCase()
        test_case.setup_method()

        assert isinstance(test_case.runner, CliRunner)
        assert test_case.temp_files == []

    def test_cli_test_case_teardown(self):
        """Test CliTestCase teardown_method."""
        test_case = CliTestCase()
        test_case.setup_method()

        # Create a real temporary file
        with tempfile.NamedTemporaryFile(delete=False) as f:
            temp_path = Path(f.name)

        test_case.temp_files.append(temp_path)
        assert temp_path.exists()

        test_case.teardown_method()
        assert not temp_path.exists()

    def test_cli_test_case_teardown_handles_missing_files(self):
        """Test CliTestCase teardown_method handles missing files."""
        test_case = CliTestCase()
        test_case.setup_method()

        # Add non-existent file to temp_files
        non_existent_path = Path("/tmp/non_existent_file_12345")
        test_case.temp_files.append(non_existent_path)

        # Should not raise exception
        test_case.teardown_method()

    def test_cli_test_case_invoke(self):
        """Test CliTestCase invoke method."""
        test_case = CliTestCase()
        test_case.setup_method()

        @click.command()
        def test_cmd():
            click.echo("hello")

        result = test_case.invoke(test_cmd)
        assert result.output.strip() == "hello"

    def test_cli_test_case_create_temp_file(self):
        """Test CliTestCase create_temp_file method."""
        test_case = CliTestCase()
        test_case.setup_method()

        content = "test file content"
        temp_path = test_case.create_temp_file(content=content, suffix=".txt")

        assert temp_path.exists()
        assert temp_path.suffix == ".txt"
        assert temp_path in test_case.temp_files

        with open(temp_path) as f:
            assert f.read() == content

    def test_cli_test_case_create_temp_file_empty_content(self):
        """Test CliTestCase create_temp_file with empty content."""
        test_case = CliTestCase()
        test_case.setup_method()

        temp_path = test_case.create_temp_file()
        assert temp_path.exists()

        with open(temp_path) as f:
            assert f.read() == ""

    def test_cli_test_case_assert_json_output_valid(self):
        """Test CliTestCase assert_json_output with valid JSON."""
        test_case = CliTestCase()

        # Mock result object
        mock_result = Mock()
        mock_result.output = '{"key1": "value1", "key2": 42}'

        expected = {"key1": "value1", "key2": 42}

        # Should not raise
        test_case.assert_json_output(mock_result, expected)

    def test_cli_test_case_assert_json_output_partial_match(self):
        """Test CliTestCase assert_json_output with partial expected data."""
        test_case = CliTestCase()

        mock_result = Mock()
        mock_result.output = '{"key1": "value1", "key2": 42, "key3": "extra"}'

        expected = {"key1": "value1", "key2": 42}

        # Should not raise - only checks expected keys
        test_case.assert_json_output(mock_result, expected)

    def test_cli_test_case_assert_json_output_invalid_json(self):
        """Test CliTestCase assert_json_output with invalid JSON."""
        test_case = CliTestCase()

        mock_result = Mock()
        mock_result.output = "not valid json"

        expected = {"key": "value"}

        with pytest.raises(AssertionError, match="Output is not valid JSON"):
            test_case.assert_json_output(mock_result, expected)

    def test_cli_test_case_assert_json_output_missing_key(self):
        """Test CliTestCase assert_json_output with missing key."""
        test_case = CliTestCase()

        mock_result = Mock()
        mock_result.output = '{"key1": "value1"}'

        expected = {"key1": "value1", "missing_key": "value"}

        with pytest.raises(AssertionError, match="Key 'missing_key' not in output"):
            test_case.assert_json_output(mock_result, expected)

    def test_cli_test_case_assert_json_output_value_mismatch(self):
        """Test CliTestCase assert_json_output with value mismatch."""
        test_case = CliTestCase()

        mock_result = Mock()
        mock_result.output = '{"key1": "wrong_value"}'

        expected = {"key1": "expected_value"}

        with pytest.raises(AssertionError, match="Value mismatch for 'key1'"):
            test_case.assert_json_output(mock_result, expected)
