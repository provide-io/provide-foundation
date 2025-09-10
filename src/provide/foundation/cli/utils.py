"""Common CLI utilities for output, logging, and testing."""

import json
from typing import Any

import click
from click.testing import CliRunner, Result

from provide.foundation.console.output import pout, perr
from provide.foundation.context import CLIContext
from provide.foundation.logger import (
    LoggingConfig,
    TelemetryConfig,
    get_logger,
)
from provide.foundation.setup import setup_telemetry

log = get_logger(__name__)


def echo_json(data: Any, err: bool = False) -> None:
    """
    Output data as JSON.

    Args:
        data: Data to output as JSON
        err: Whether to output to stderr
    """
    if err:
        perr(data)
    else:
        pout(data)


def echo_error(message: str, json_output: bool = False) -> None:
    """
    Output an error message.

    Args:
        message: Error message to output
        json_output: Whether to output as JSON
    """
    if json_output:
        perr(message, json_key="error")
    else:
        perr(f"✗ {message}", color="red")


def echo_success(message: str, json_output: bool = False) -> None:
    """
    Output a success message.

    Args:
        message: Success message to output
        json_output: Whether to output as JSON
    """
    if json_output:
        pout(message, json_key="success")
    else:
        pout(f"✓ {message}", color="green")


def echo_warning(message: str, json_output: bool = False) -> None:
    """
    Output a warning message.

    Args:
        message: Warning message to output
        json_output: Whether to output as JSON
    """
    if json_output:
        perr(message, json_key="warning")
    else:
        perr(f"⚠ {message}", color="yellow")


def echo_info(message: str, json_output: bool = False) -> None:
    """
    Output an informational message.

    Args:
        message: Info message to output
        json_output: Whether to output as JSON
    """
    if json_output:
        pout(message, json_key="info")
    else:
        pout(f"ℹ {message}")


def setup_cli_logging(
    ctx: CLIContext,
) -> None:
    """
    Setup logging for CLI applications using a CLIContext object.

    This function is the designated way to configure logging within a CLI
    application built with foundation. It uses the provided context object
    to construct a full TelemetryConfig and initializes the system.

    Args:
        ctx: The foundation CLIContext, populated by CLI decorators.
    """
    console_formatter = "json" if ctx.json_output else ctx.log_format

    logging_config = LoggingConfig(
        default_level=ctx.log_level,
        console_formatter=console_formatter,
        omit_timestamp=False,
        logger_name_emoji_prefix_enabled=not ctx.no_emoji,
        das_emoji_prefix_enabled=not ctx.no_emoji,
        log_file=ctx.log_file,
    )

    telemetry_config = TelemetryConfig(
        service_name=ctx.profile,
        logging=logging_config,
    )

    setup_telemetry(config=telemetry_config)


def create_cli_context(**kwargs) -> CLIContext:
    """
    Create a CLIContext for CLI usage.

    Loads from environment, then overlays any provided kwargs.

    Args:
        **kwargs: Override values for the context

    Returns:
        Configured CLIContext instance
    """
    ctx = CLIContext.from_env()
    for key, value in kwargs.items():
        if value is not None and hasattr(ctx, key):
            setattr(ctx, key, value)
    return ctx


class CliTestRunner:
    """Test runner for CLI commands using Click's testing facilities."""

    def __init__(self) -> None:
        self.runner = CliRunner()

    def invoke(
        self,
        cli: click.Command | click.Group,
        args: list[str] | None = None,
        input: str | None = None,
        env: dict[str, str] | None = None,
        catch_exceptions: bool = True,
        **kwargs,
    ) -> Result:
        """Invoke a CLI command for testing."""
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
        """
        return self.runner.isolated_filesystem()


def assert_cli_success(result: Result, expected_output: str | None = None) -> None:
    """
    Assert that a CLI command succeeded.
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
    result: Result,
    expected_error: str | None = None,
    exit_code: int | None = None,
) -> None:
    """
    Assert that a CLI command failed.
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
