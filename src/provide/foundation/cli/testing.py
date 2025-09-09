"""Testing utilities specifically for CLI applications."""

from contextlib import contextmanager
import json
import os
from pathlib import Path
import tempfile
from typing import Any
from unittest.mock import MagicMock

import click
from click.testing import CliRunner

from provide.foundation.context import CLIContext
from provide.foundation.logger import get_logger

log = get_logger(__name__)




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

                    tomli_w.dump(content, f)
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
