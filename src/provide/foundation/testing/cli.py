"""
CLI Testing Utilities for Foundation.

Provides comprehensive testing support for CLI applications including
context mocking, isolated runners, and configuration helpers.
"""

from contextlib import contextmanager
import json
import os
from pathlib import Path
import tempfile
from typing import Any
from unittest.mock import MagicMock

import click
from click.testing import CliRunner
import pytest

from provide.foundation.context import CLIContext
from provide.foundation.logger import get_logger

log = get_logger(__name__)


class MockContext(CLIContext):
    """Mock context for testing that tracks method calls."""

    def __init__(self, **kwargs) -> None:
        """Initialize mock context with tracking."""
        super().__init__(**kwargs)
        self.calls = []
        self.saved_configs = []
        self.loaded_configs = []

    def save_config(self, path: str | Path) -> None:
        """Track save_config calls."""
        self.saved_configs.append(path)
        super().save_config(path)

    def load_config(self, path: str | Path) -> None:
        """Track load_config calls."""
        self.loaded_configs.append(path)
        super().load_config(path)


@contextmanager
def isolated_cli_runner(
    env: dict[str, str] | None = None,
):
    """
    Create an isolated test environment for CLI testing.

    Args:
        env: Environment variables to set

    Yields:
        CliRunner instance in isolated filesystem
    """
    runner = CliRunner()

    with runner.isolated_filesystem():
        # Set up environment
        old_env = {}
        if env:
            for key, value in env.items():
                old_env[key] = os.environ.get(key)
                os.environ[key] = value

        try:
            yield runner
        finally:
            # Restore environment
            for key, old_value in old_env.items():
                if old_value is None:
                    os.environ.pop(key, None)
                else:
                    os.environ[key] = old_value


@contextmanager
def temp_config_file(
    content: dict[str, Any] | str,
    format: str = "json",
) -> Path:
    """
    Create a temporary configuration file for testing.

    Args:
        content: Configuration content (dict or string)
        format: File format (json, toml, yaml)

    Yields:
        Path to temporary config file
    """
    suffix = f".{format}"

    with tempfile.NamedTemporaryFile(
        mode="w",
        suffix=suffix,
        delete=False,
    ) as f:
        if isinstance(content, dict):
            if format == "json":
                json.dump(content, f, indent=2)
            elif format == "toml":
                try:
                    import tomli_w

                    # tomli_w needs the content as a string, not written to file handle
                    toml_content = tomli_w.dumps(content)
                    f.write(toml_content)
                except ImportError:
                    # Fall back to manual formatting
                    for key, value in content.items():
                        if isinstance(value, str):
                            f.write(f'{key} = "{value}"\n')
                        else:
                            f.write(f"{key} = {value}\n")
            elif format == "yaml":
                try:
                    import yaml

                    yaml.safe_dump(content, f)
                except ImportError:
                    raise ImportError("PyYAML required for YAML testing")
        else:
            f.write(content)

        config_path = Path(f.name)

    try:
        yield config_path
    finally:
        config_path.unlink(missing_ok=True)


def create_test_cli(
    name: str = "test-cli",
    version: str = "1.0.0",
    commands: list[click.Command] | None = None,
) -> click.Group:
    """
    Create a test CLI group with standard options.

    Args:
        name: CLI name
        version: CLI version
        commands: Optional list of commands to add

    Returns:
        Click Group configured for testing
    """
    from provide.foundation.cli.decorators import standard_options

    @click.group(name=name)
    @standard_options
    @click.pass_context
    def cli(ctx, **kwargs) -> None:
        """Test CLI for testing."""
        ctx.obj = CLIContext(**{k: v for k, v in kwargs.items() if v is not None})

    if commands:
        for cmd in commands:
            cli.add_command(cmd)

    return cli




class CliTestCase:
    """Base class for CLI test cases with common utilities."""

    def setup_method(self) -> None:
        """Set up test case."""
        self.runner = CliRunner()
        self.temp_files = []

    def teardown_method(self) -> None:
        """Clean up test case."""
        for path in self.temp_files:
            if path.exists():
                path.unlink()

    def invoke(self, *args, **kwargs):
        """Invoke CLI command."""
        return self.runner.invoke(*args, **kwargs)

    def create_temp_file(self, content: str = "", suffix: str = "") -> Path:
        """Create a temporary file that will be cleaned up."""
        with tempfile.NamedTemporaryFile(
            mode="w",
            suffix=suffix,
            delete=False,
        ) as f:
            f.write(content)
            path = Path(f.name)

        self.temp_files.append(path)
        return path

    def assert_json_output(self, result, expected: dict[str, Any]) -> None:
        """Assert that output is valid JSON matching expected."""
        try:
            output = json.loads(result.output)
        except json.JSONDecodeError as e:
            raise AssertionError(f"Output is not valid JSON: {e}\n{result.output}")

        for key, value in expected.items():
            assert key in output, f"Key '{key}' not in output"
            assert output[key] == value, (
                f"Value mismatch for '{key}': {output[key]} != {value}"
            )


@pytest.fixture
def click_testing_mode():
    """
    Pytest fixture to enable Click testing mode.
    
    Sets CLICK_TESTING=1 environment variable for the duration of the test,
    then restores the original value. This fixture makes it easy to enable
    Click testing mode without manual environment variable management.
    
    Usage:
        def test_my_cli(click_testing_mode):
            # Test CLI code here - CLICK_TESTING is automatically set
            pass
    """
    original_value = os.environ.get("CLICK_TESTING")
    os.environ["CLICK_TESTING"] = "1"
    
    try:
        yield
    finally:
        if original_value is None:
            os.environ.pop("CLICK_TESTING", None)
        else:
            os.environ["CLICK_TESTING"] = original_value
