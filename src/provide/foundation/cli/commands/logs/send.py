"""
Send logs command for Foundation CLI.
"""

import json
import sys

try:
    import click

    _HAS_CLICK = True
except ImportError:
    click = None
    _HAS_CLICK = False

from provide.foundation.logger import get_logger

log = get_logger(__name__)


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
        ctx, message, level, service, json_attrs, attr, trace_id, span_id, use_otlp
    ):
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
        from provide.foundation.integrations.openobserve.otlp import send_log

        # Get message from stdin if not provided
        if not message:
            if sys.stdin.isatty():
                click.echo(
                    "Error: No message provided. Use -m or pipe input.", err=True
                )
                return 1
            message = sys.stdin.read().strip()
            if not message:
                click.echo("Error: Empty message from stdin.", err=True)
                return 1

        # Build attributes
        attributes = {}

        # Add JSON attributes
        if json_attrs:
            try:
                attributes.update(json.loads(json_attrs))
            except json.JSONDecodeError as e:
                click.echo(f"Error: Invalid JSON attributes: {e}", err=True)
                return 1

        # Add key=value attributes
        for kv in attr:
            if "=" not in kv:
                click.echo(
                    f"Error: Invalid attribute format '{kv}'. Use key=value.", err=True
                )
                return 1
            key, value = kv.split("=", 1)
            # Try to parse value as number
            try:
                if "." in value:
                    value = float(value)
                else:
                    value = int(value)
            except ValueError:
                pass  # Keep as string
            attributes[key] = value

        # Add explicit trace/span IDs if provided
        if trace_id:
            attributes["trace_id"] = trace_id
        if span_id:
            attributes["span_id"] = span_id

        # Send the log
        try:
            client = ctx.obj.get("client")
            success = send_log(
                message=message,
                level=level,
                service=service,
                attributes=attributes if attributes else None,
                prefer_otlp=use_otlp,
                client=client,
            )

            if success:
                click.echo(
                    f"✅ Log sent successfully via {'OTLP' if use_otlp else 'bulk API'}"
                )
            else:
                click.echo("❌ Failed to send log", err=True)
                return 1

        except Exception as e:
            click.echo(f"Error: {e}", err=True)
            return 1

else:

    def send_command(*args, **kwargs):
        """Send command stub when click is not available."""
        raise ImportError(
            "CLI commands require optional dependencies. "
            "Install with: pip install 'provide-foundation[cli]'"
        )
