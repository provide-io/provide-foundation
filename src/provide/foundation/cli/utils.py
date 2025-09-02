"""Common CLI utilities for output, logging, and testing."""

import json
from pathlib import Path
from typing import Any

import click

from provide.foundation.context import Context
from provide.foundation.logger import get_logger, setup_logging

log = get_logger(__name__)


def echo_json(data: Any, err: bool = False) -> None:
    """
    Output data as JSON.

    Args:
        data: Data to output as JSON
        err: Whether to output to stderr
    """
    click.echo(json.dumps(data, indent=2, default=str), err=err)


def echo_error(message: str, json_output: bool = False) -> None:
    """
    Output an error message.

    Args:
        message: Error message to output
        json_output: Whether to output as JSON
    """
    if json_output:
        echo_json({"error": message}, err=True)
    else:
        click.secho(f"✗ {message}", fg="red", err=True)


def echo_success(message: str, json_output: bool = False) -> None:
    """
    Output a success message.

    Args:
        message: Success message to output
        json_output: Whether to output as JSON
    """
    if json_output:
        echo_json({"success": message})
    else:
        click.secho(f"✓ {message}", fg="green")


def echo_warning(message: str, json_output: bool = False) -> None:
    """
    Output a warning message.

    Args:
        message: Warning message to output
        json_output: Whether to output as JSON
    """
    if json_output:
        echo_json({"warning": message}, err=True)
    else:
        click.secho(f"⚠ {message}", fg="yellow", err=True)


def echo_info(message: str, json_output: bool = False) -> None:
    """
    Output an informational message.

    Args:
        message: Info message to output
        json_output: Whether to output as JSON
    """
    if json_output:
        echo_json({"info": message})
    else:
        click.echo(f"ℹ {message}")


def setup_cli_logging(
    ctx: Context | None = None,
    log_level: str | None = None,
    log_file: str | Path | None = None,
    json_logs: bool = False,
) -> None:
    """
    Setup logging for CLI applications.

    Args:
        ctx: Optional Context to get settings from
        log_level: Override log level
        log_file: Override log file path
        json_logs: Whether to output logs as JSON
    """
    if ctx:
        log_level = log_level or ctx.log_level
        log_file = log_file or ctx.log_file
        json_logs = json_logs or ctx.json_output

    setup_logging(
        level=log_level or "INFO",
        json_logs=json_logs,
        log_file=str(log_file) if log_file else None,
    )


def create_cli_context(**kwargs) -> Context:
    """
    Create a Context for CLI usage.

    Loads from environment, then overlays any provided kwargs.

    Args:
        **kwargs: Override values for the context

    Returns:
        Configured Context instance
    """
    # Start with environment
    ctx = Context.from_env()

    # Apply any overrides
    for key, value in kwargs.items():
        if value is not None and hasattr(ctx, key):
            setattr(ctx, key, value)

    return ctx


# Testing utilities


class CliTestRunner:
    """Test runner for CLI commands using Click's testing facilities."""

    def __init__(self, mix_stderr: bool = False):
        """
        Initialize the test runner.

        Args:
            mix_stderr: Whether to mix stderr with stdout in output
        """
        from click.testing import CliRunner

        self.runner = CliRunner(mix_stderr=mix_stderr)

    def invoke(
        self,
        cli: click.Command | click.Group,
        args: list[str] | None = None,
        input: str | None = None,
        env: dict[str, str] | None = None,
        catch_exceptions: bool = True,
        **kwargs,
    ):
        """
        Invoke a CLI command for testing.

        Args:
            cli: The Click command or group to invoke
            args: Command line arguments
            input: Optional input to provide
            env: Environment variables to set
            catch_exceptions: Whether to catch exceptions
            **kwargs: Additional arguments for CliRunner.invoke

        Returns:
            Click Result object with exit_code, output, etc.
        """
        return self.runner.invoke(
            cli,
            args=args,
            input=input,
            env=env,
            catch_exceptions=catch_exceptions,
            **kwargs,
        )

    def isolated_filesystem(self):
        """
        Context manager for isolated filesystem.

        Creates a temporary directory and changes to it,
        cleaning up on exit.
        """
        return self.runner.isolated_filesystem()


def assert_cli_success(result, expected_output: str | None = None) -> None:
    """
    Assert that a CLI command succeeded.

    Args:
        result: Click Result object from invoke
        expected_output: Optional expected output substring
    """
    if result.exit_code != 0:
        raise AssertionError(
            f"Command failed with exit code {result.exit_code}\n"
            f"Output: {result.output}\n"
            f"Exception: {result.exception}"
        )

    if expected_output and expected_output not in result.output:
        raise AssertionError(
            f"Expected output not found.\n"
            f"Expected: {expected_output}\n"
            f"Actual: {result.output}"
        )


def assert_cli_error(
    result,
    expected_error: str | None = None,
    exit_code: int | None = None,
) -> None:
    """
    Assert that a CLI command failed.

    Args:
        result: Click Result object from invoke
        expected_error: Optional expected error substring
        exit_code: Expected exit code (default: any non-zero)
    """
    if result.exit_code == 0:
        raise AssertionError(f"Command succeeded unexpectedly\nOutput: {result.output}")

    if exit_code is not None and result.exit_code != exit_code:
        raise AssertionError(
            f"Wrong exit code.\nExpected: {exit_code}\nActual: {result.exit_code}"
        )

    if expected_error and expected_error not in result.output:
        raise AssertionError(
            f"Expected error not found.\n"
            f"Expected: {expected_error}\n"
            f"Actual: {result.output}"
        )
