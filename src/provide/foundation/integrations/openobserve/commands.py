#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""CLI commands for OpenObserve integration.

These commands are auto-registered by Foundation's command discovery system."""

from __future__ import annotations

from typing import Any

from provide.foundation.console.output import perr, pout
from provide.foundation.logger import get_logger
from provide.foundation.utils.async_helpers import run_async

try:
    import click

    _HAS_CLICK = True
except ImportError:
    click: Any = None  # type: ignore[no-redef]
    _HAS_CLICK = False

log = get_logger(__name__)


def _parse_filter_to_dict(filter_str: str) -> dict[str, str]:
    """Parse simple filter string into dict format.

    Supports formats like:
    - "level=ERROR" → {"level": "ERROR"}
    - "level='ERROR'" → {"level": "ERROR"}
    - "level=ERROR,service=api" → {"level": "ERROR", "service": "api"}

    Args:
        filter_str: Filter string to parse

    Returns:
        Dictionary of key-value pairs

    """
    import re

    filters = {}

    # Split by comma for multiple filters
    parts = filter_str.split(",")

    for part in parts:
        part = part.strip()
        # Match key=value or key='value' or key="value"
        match = re.match(r"^([a-zA-Z0-9_]+)\s*=\s*['\"]?([^'\"]+)['\"]?$", part)
        if match:
            key, value = match.groups()
            filters[key] = value.strip()
        else:
            # Try simple key=value without quotes
            if "=" in part:
                key, value = part.split("=", 1)
                filters[key.strip()] = value.strip()

    return filters


if _HAS_CLICK:
    from provide.foundation.integrations.openobserve import (
        OpenObserveClient,
        format_output,
        search_logs,
        tail_logs,
    )

    @click.group("openobserve", help="Query and manage OpenObserve logs")
    @click.pass_context
    def openobserve_group(ctx: click.Context) -> None:
        """OpenObserve log querying and streaming commands."""
        # Initialize client and store in context
        try:
            client = OpenObserveClient.from_config()
            ctx.obj = client
        except Exception as e:
            perr(f"Failed to initialize OpenObserve client: {e}")
            ctx.obj = None

    @openobserve_group.command("query")
    @click.option(
        "--sql",
        required=True,
        help="SQL query to execute",
    )
    @click.option(
        "--start",
        "-s",
        default="-1h",
        help="Start time (e.g., -1h, -30m, 2024-01-01)",
    )
    @click.option(
        "--end",
        "-e",
        default="now",
        help="End time (e.g., now, -5m, 2024-01-02)",
    )
    @click.option(
        "--size",
        "-n",
        default=100,
        type=int,
        help="Number of results to return",
    )
    @click.option(
        "--format",
        "-f",
        type=click.Choice(["json", "log", "table", "csv", "summary"]),
        default="log",
        help="Output format",
    )
    @click.option(
        "--pretty",
        is_flag=True,
        help="Pretty print JSON output",
    )
    @click.pass_context
    @click.pass_obj
    def query_command(
        client: OpenObserveClient | None,
        ctx: click.Context,
        sql: str,
        start: str,
        end: str,
        size: int,
        format: str,
        pretty: bool,
    ) -> None:
        """Execute SQL query against OpenObserve logs."""
        if client is None:
            click.echo(
                "OpenObserve not configured. Set OPENOBSERVE_URL, OPENOBSERVE_USER, and OPENOBSERVE_PASSWORD.",
                err=True,
            )
            ctx.exit(1)

        try:
            response = run_async(
                search_logs(
                    sql=sql,
                    start_time=start,
                    end_time=end,
                    size=size,
                    client=client,
                )
            )

            output = format_output(response, format_type=format, pretty=pretty)
            click.echo(output)

        except Exception as e:
            click.echo(f"Query failed: {e}", err=True)
            ctx.exit(1)

    @openobserve_group.command("tail")
    @click.option(
        "--stream",
        "-s",
        default="default",
        help="Stream name to tail",
    )
    @click.option(
        "--filter",
        "-f",
        "filter_sql",
        help='Filter condition (e.g., "level=ERROR" or "service=api")',
    )
    @click.option(
        "--lines",
        "-n",
        default=10,
        type=int,
        help="Number of initial lines to show",
    )
    @click.option(
        "--follow",
        "-F",
        type=bool,
        default=True,
        help="Follow mode (like tail -f)",
    )
    @click.option(
        "--format",
        type=click.Choice(["log", "json"]),
        default="log",
        help="Output format",
    )
    @click.pass_context
    @click.pass_obj
    def tail_command(
        client: OpenObserveClient | None,
        ctx: click.Context,
        stream: str,
        filter_sql: str | None,
        lines: int,
        follow: bool,
        format: str,
    ) -> None:
        """Tail logs from OpenObserve (like 'tail -f')."""
        if client is None:
            click.echo(
                "OpenObserve not configured. Set OPENOBSERVE_URL, OPENOBSERVE_USER, and OPENOBSERVE_PASSWORD.",
                err=True,
            )
            ctx.exit(1)

        try:
            pout(f"Tailing logs from stream '{stream}'...")

            # Parse filter_sql into filters dict
            filters = None
            if filter_sql:
                pout(f"Filter: {filter_sql}")
                filters = _parse_filter_to_dict(filter_sql)

            for log_entry in tail_logs(
                stream=stream,
                filters=filters,
                follow=follow,
                lines=lines,
                client=client,
            ):
                # Emit through structlog for consistent formatting, but skip OTLP to prevent feedback loop
                # Extract the message and metadata from the log entry
                message = log_entry.get("message", log_entry.get("body", ""))

                # Get all other fields as context
                context = {k: v for k, v in log_entry.items() if k not in ("message", "body")}
                context["_skip_otlp"] = True  # Prevent sending back to OpenObserve

                # Emit through structlog
                log.info(message, **context)

        except KeyboardInterrupt:
            pout("\nStopped tailing logs.")
        except Exception as e:
            perr(f"Tail failed: {e}")
            ctx.exit(1)

    @openobserve_group.command("errors")
    @click.option(
        "--stream",
        "-s",
        default="default",
        help="Stream name to search",
    )
    @click.option(
        "--start",
        default="-1h",
        help="Start time",
    )
    @click.option(
        "--size",
        "-n",
        default=100,
        type=int,
        help="Number of results",
    )
    @click.option(
        "--format",
        "-f",
        type=click.Choice(["json", "log", "table", "csv", "summary"]),
        default="log",
        help="Output format",
    )
    @click.pass_context
    @click.pass_obj
    def errors_command(
        client: OpenObserveClient | None,
        ctx: click.Context,
        stream: str,
        start: str,
        size: int,
        format: str,
    ) -> None:
        """Search for error logs."""
        if client is None:
            click.echo("OpenObserve not configured.", err=True)
            ctx.exit(1)

        try:
            from provide.foundation.integrations.openobserve import search_errors

            response = run_async(
                search_errors(
                    stream=stream,
                    start_time=start,
                    size=size,
                    client=client,
                )
            )

            if response.total == 0:
                click.echo("No errors found in the specified time range.")
            else:
                output = format_output(response, format_type=format)
                click.echo(output)

        except Exception as e:
            click.echo(f"Search failed: {e}", err=True)
            ctx.exit(1)

    @openobserve_group.command("trace")
    @click.argument("trace_id")
    @click.option(
        "--stream",
        "-s",
        default="default",
        help="Stream name to search",
    )
    @click.option(
        "--format",
        "-f",
        type=click.Choice(["json", "log", "table"]),
        default="log",
        help="Output format",
    )
    @click.pass_context
    @click.pass_obj
    def trace_command(
        client: OpenObserveClient | None,
        ctx: click.Context,
        trace_id: str,
        stream: str,
        format: str,
    ) -> None:
        """Search for logs by trace ID."""
        if client is None:
            click.echo("OpenObserve not configured.", err=True)
            ctx.exit(1)

        try:
            from provide.foundation.integrations.openobserve import search_by_trace_id

            response = run_async(
                search_by_trace_id(
                    trace_id=trace_id,
                    stream=stream,
                    client=client,
                )
            )

            if response.total == 0:
                click.echo(f"No logs found for trace ID: {trace_id}")
            else:
                output = format_output(response, format_type=format)
                click.echo(output)

        except Exception as e:
            click.echo(f"Search failed: {e}", err=True)
            ctx.exit(1)

    @openobserve_group.command("streams")
    @click.pass_context
    @click.pass_obj
    def streams_command(client: OpenObserveClient | None, ctx: click.Context) -> None:
        """List available streams."""
        if client is None:
            click.echo("OpenObserve not configured.", err=True)
            ctx.exit(1)

        try:
            streams = run_async(client.list_streams())

            if not streams:
                click.echo("No streams found.")
            else:
                click.echo("Available streams:")
                for stream in streams:
                    click.echo(f"  - {stream.name} ({stream.stream_type})")
                    if stream.doc_count > 0:
                        click.echo(f"    Documents: {stream.doc_count:,}")
                        click.echo(f"    Size: {stream.original_size:,} bytes")

        except Exception as e:
            click.echo(f"Failed to list streams: {e}", err=True)
            ctx.exit(1)

    @openobserve_group.command("history")
    @click.option(
        "--size",
        "-n",
        default=20,
        type=int,
        help="Number of history entries",
    )
    @click.option(
        "--stream",
        "-s",
        help="Filter by stream name",
    )
    @click.pass_context
    @click.pass_obj
    def history_command(
        client: OpenObserveClient | None, ctx: click.Context, size: int, stream: str | None
    ) -> None:
        """View search history."""
        if client is None:
            click.echo("OpenObserve not configured.", err=True)
            ctx.exit(1)

        try:
            response = run_async(
                client.get_search_history(
                    stream_name=stream,
                    size=size,
                )
            )

            if response.total == 0:
                click.echo("No search history found.")
            else:
                click.echo(f"Search history ({response.total} entries):")
                for hit in response.hits:
                    sql = hit.get("sql", "N/A")
                    took = hit.get("took", 0)
                    records = hit.get("scan_records", 0)
                    click.echo(f"\n  Query: {sql}")
                    click.echo(f"  Time: {took:.2f}ms, Records: {records:,}")

        except Exception as e:
            click.echo(f"Failed to get history: {e}", err=True)
            ctx.exit(1)

    @openobserve_group.command("test")
    @click.pass_context
    @click.pass_obj
    def test_command(client: OpenObserveClient | None, ctx: click.Context) -> None:
        """Test connection to OpenObserve."""
        if client is None:
            click.echo("OpenObserve not configured.", err=True)
            ctx.exit(1)

        click.echo(f"Testing connection to {client.url}...")

        if run_async(client.test_connection()):
            click.echo("✅ Connection successful!")
            click.echo(f"Organization: {client.organization}")
            click.echo(f"User: {client.username}")
        else:
            click.echo("❌ Connection failed!")
            ctx.exit(1)

    # Add metrics subcommand group
    try:
        from provide.foundation.integrations.openobserve.metrics_commands import (
            metrics_group,
        )

        openobserve_group.add_command(metrics_group)
    except ImportError:
        # Metrics commands not available
        pass

    # Export the command group for auto-discovery
    __all__ = ["openobserve_group"]

else:
    # Stub when click is not available
    def openobserve_group(*args: object, **kwargs: object) -> None:  # type: ignore[misc]
        """OpenObserve command stub when click is not available."""
        raise ImportError(
            "CLI commands require optional dependencies. Install with: pip install 'provide-foundation[cli]'",
        )

    __all__ = []

# 🧱🏗️🔚
