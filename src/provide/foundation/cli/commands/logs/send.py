from __future__ import annotations

import json
import sys
import time
from typing import TYPE_CHECKING, Any, NoReturn

from provide.foundation.logger import get_logger

"""Send logs command for Foundation CLI."""

if TYPE_CHECKING:
    import click

# Click feature detection
try:
    import click

    _HAS_CLICK = True
except ImportError:
    click: Any = None
    _HAS_CLICK = False

log = get_logger(__name__)


def _get_message_from_input(message: str | None) -> tuple[str | None, int]:
    """Get message from argument or stdin. Returns (message, error_code)."""
    if message:
        return message, 0

    if sys.stdin.isatty():
        click.echo("Error: No message provided. Use -m or pipe input.", err=True)
        return None, 1

    stdin_message = sys.stdin.read().strip()
    if not stdin_message:
        click.echo("Error: Empty message from stdin.", err=True)
        return None, 1

    return stdin_message, 0


def _build_attributes(json_attrs: str | None, attr: tuple[str, ...]) -> tuple[dict[str, Any], int]:
    """Build attributes dict from JSON and key=value pairs. Returns (attributes, error_code)."""
    attributes = {}

    # Add JSON attributes
    if json_attrs:
        try:
            attributes.update(json.loads(json_attrs))
        except json.JSONDecodeError as e:
            click.echo(f"Error: Invalid JSON attributes: {e}", err=True)
            return {}, 1

    # Add key=value attributes
    for kv_pair in attr:
        try:
            key, value = kv_pair.split("=", 1)
            # Try to parse as number, boolean, or keep as string
            if value.lower() in ("true", "false"):
                attributes[key] = value.lower() == "true"
            elif value.isdigit():
                attributes[key] = int(value)
            elif "." in value and value.replace(".", "").replace("-", "").isdigit():
                attributes[key] = float(value)
            else:
                attributes[key] = value
        except ValueError:
            click.echo(f"Error: Invalid attribute format '{kv_pair}'. Use key=value.", err=True)
            return {}, 1

    return attributes, 0


def _send_log_entry(
    message: str,
    level: str,
    service: str | None,
    attributes: dict[str, Any],
    trace_id: str | None,
    span_id: str | None,
    use_otlp: bool,
) -> int:
    """Send the log entry using appropriate method."""
    from provide.foundation.integrations.openobserve.otlp import send_log

    try:
        if use_otlp:
            # Send via OTLP
            send_log(
                message=message,
                level=level,
                service_name=service,
                attributes=attributes,
                trace_id=trace_id,
                span_id=span_id,
            )
            click.echo("✓ Log sent via OTLP")
        else:
            # Send via HTTP API
            from provide.foundation.integrations.openobserve import ingest_logs

            # Build log record
            log_record = {
                "timestamp": int(time.time() * 1000000),  # microseconds
                "message": message,
                "level": level,
                **attributes,
            }

            if service:
                log_record["service"] = service
            if trace_id:
                log_record["trace_id"] = trace_id
            if span_id:
                log_record["span_id"] = span_id

            ingest_logs([log_record])
            click.echo("✓ Log sent via HTTP API")

        return 0
    except Exception as e:
        click.echo(f"✗ Failed to send log: {e}", err=True)
        return 1


if _HAS_CLICK:

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
    @click.option(
        "--otlp/--bulk",
        "use_otlp",
        default=True,
        help="Use OTLP (default) or bulk API",
    )
    @click.pass_context
    def send_command(
        ctx: click.Context,
        message: str | None,
        level: str,
        service: str | None,
        json_attrs: str | None,
        attr: tuple[str, ...],
        trace_id: str | None,
        span_id: str | None,
        use_otlp: bool,
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
            return error_code

        # Build attributes
        attributes, error_code = _build_attributes(json_attrs, attr)
        if error_code != 0:
            return error_code

        # Send the log entry
        return _send_log_entry(final_message, level, service, attributes, trace_id, span_id, use_otlp)

else:

    def send_command(*args: object, **kwargs: object) -> NoReturn:
        """Send command stub when click is not available."""
        raise ImportError(
            "CLI commands require optional dependencies. Install with: pip install 'provide-foundation[cli]'",
        )
