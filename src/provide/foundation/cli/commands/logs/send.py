#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from __future__ import annotations

import sys
from typing import Any

from provide.foundation.cli.deps import click
from provide.foundation.cli.helpers import (
    build_attributes_from_args,
    get_message_from_stdin,
    requires_click,
)
from provide.foundation.cli.shutdown import with_cleanup
from provide.foundation.console.output import perr, pout
from provide.foundation.logger import get_logger
from provide.foundation.process import exit_error, exit_success

"""Send logs command for Foundation CLI."""


def _get_message_from_input(message: str | None) -> tuple[str | None, int]:
    """Get message from argument or stdin. Returns (message, error_code)."""
    if message:
        return message, 0

    # Try to read from stdin using shared helper
    stdin_message, error_code = get_message_from_stdin()

    # If stdin is TTY (no piped input), show helpful error
    if error_code != 0 and sys.stdin.isatty():
        click.echo("Error: No message provided. Use -m or pipe input.", err=True)

    return stdin_message, error_code


def _send_log_entry(
    message: str,
    level: str,
    service_name: str | None,
    attributes: dict[str, Any],
    trace_id: str | None,
    span_id: str | None,
) -> int:
    """Send the log entry using the main FoundationLogger."""
    try:
        # Get a logger instance, optionally scoped to the service name
        logger = get_logger(service_name or "cli.send")

        # Add trace context to attributes if provided
        if trace_id:
            attributes["trace_id"] = trace_id
        if span_id:
            attributes["span_id"] = span_id

        # Get the appropriate log method (info, error, etc.)
        log_method = getattr(logger, level.lower(), logger.info)

        # Emit the log
        log_method(message, **attributes)

        pout("✓ Log sent successfully", color="green")
        return 0
    except Exception as e:
        perr(f"✗ Failed to send log: {e}", color="red")
        return 1


@click.command("send")
@click.option(
    "--message",
    "-m",
    help="Log message to send (reads from stdin if not provided)",
)
@click.option(
    "--level",
    "-l",
    type=click.Choice(["TRACE", "DEBUG", "INFO", "WARN", "ERROR", "CRITICAL"]),
    default="INFO",
    help="Log level",
)
@click.option(
    "--service",
    "-s",
    "service_name",
    help="Service name (uses config default if not provided)",
)
@click.option(
    "--json",
    "-j",
    "json_attrs",
    help="Additional attributes as JSON",
)
@click.option(
    "--attr",
    "-a",
    multiple=True,
    help="Additional attributes as key=value pairs",
)
@click.option(
    "--trace-id",
    help="Explicit trace ID to use",
)
@click.option(
    "--span-id",
    help="Explicit span ID to use",
)
@click.pass_context
@requires_click
@with_cleanup
def send_command(
    ctx: click.Context,
    message: str | None,
    level: str,
    service_name: str | None,
    json_attrs: str | None,
    attr: tuple[str, ...],
    trace_id: str | None,
    span_id: str | None,
) -> int | None:
    """Send a log entry to OpenObserve.

    Examples:
        # Send a simple log
        foundation logs send -m "User logged in" -l INFO

        # Send with attributes
        foundation logs send -m "Payment processed" --attr user_id=123 --attr amount=99.99

        # Send from stdin
        echo "Application started" | foundation logs send -l INFO

        # Send with JSON attributes
        foundation logs send -m "Error occurred" -j '{"error_code": 500, "path": "/api/users"}'

    """
    # Get message from input
    final_message, error_code = _get_message_from_input(message)
    if error_code != 0:
        exit_error("No message provided", code=error_code)

    # Build attributes using shared helper
    attributes, error_code = build_attributes_from_args(json_attrs, attr)
    if error_code != 0:
        exit_error("Invalid attributes", code=error_code)

    # Send the log entry
    result = _send_log_entry(
        final_message,  # type: ignore[arg-type]
        level,
        service_name,
        attributes,
        trace_id,
        span_id,
    )

    if result == 0:
        exit_success()
    else:
        exit_error("Failed to send log", code=result)

    return None


# 🧱🏗️🔚
