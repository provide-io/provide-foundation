#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from __future__ import annotations

from typing import Any

from provide.foundation.cli.deps import click
from provide.foundation.cli.helpers import get_client_from_context, requires_click
from provide.foundation.cli.shutdown import with_cleanup
from provide.foundation.logger import get_logger
from provide.foundation.process import exit_error

"""Query logs command for Foundation CLI."""

log = get_logger(__name__)


def _get_trace_id_if_needed(current_trace: bool, trace_id: str | None) -> str | None:
    """Get trace ID from current trace context if needed."""
    if not current_trace:
        return trace_id

    try:
        # Try OpenTelemetry first
        from opentelemetry import trace

        current_span = trace.get_current_span()
        if current_span and current_span.is_recording():
            span_context = current_span.get_span_context()
            return f"{span_context.trace_id:032x}"
        # Try Foundation tracer
        from provide.foundation.tracer.context import get_current_trace_id

        found_trace_id = get_current_trace_id()
        if not found_trace_id:
            click.echo("No active trace found.", err=True)
            return None
        return found_trace_id
    except ImportError:
        click.echo("Tracing not available.", err=True)
        return None


def _build_query_sql(
    trace_id: str | None,
    level: str | None,
    service: str | None,
    stream: str,
    size: int,
) -> str:
    """Build SQL query with WHERE conditions."""
    import re

    # Sanitize stream name - only allow alphanumeric and underscores
    if not re.match(r"^[a-zA-Z0-9_]+$", stream):
        raise ValueError(f"Invalid stream name: {stream}")

    # Sanitize size parameter
    if not isinstance(size, int) or size <= 0 or size > 10000:
        raise ValueError(f"Invalid size parameter: {size}")

    conditions = []
    if trace_id:
        # Sanitize trace_id - should be hex string or UUID format
        if not re.match(r"^[a-fA-F0-9\-]+$", trace_id):
            raise ValueError(f"Invalid trace_id format: {trace_id}")
        conditions.append(f"trace_id = '{trace_id}'")

    if level:
        # Sanitize level using Foundation's existing validation
        from provide.foundation.parsers.errors import _VALID_LOG_LEVEL_TUPLE

        if level not in _VALID_LOG_LEVEL_TUPLE:
            raise ValueError(f"Invalid log level: {level}")
        conditions.append(f"level = '{level}'")

    if service:
        # Sanitize service name - allow alphanumeric, hyphens, underscores, dots
        if not re.match(r"^[a-zA-Z0-9_\-\.]+$", service):
            raise ValueError(f"Invalid service name: {service}")
        conditions.append(f"service = '{service}'")

    where_clause = f"WHERE {' AND '.join(conditions)}" if conditions else ""
    # All parameters are sanitized above with regex validation
    return f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp DESC LIMIT {size}"  # nosec B608


def _execute_and_display_query(sql: str, last: str, size: int, format: str, client: Any) -> int:
    """Execute query and display results."""
    from provide.foundation.integrations.openobserve import format_output, search_logs
    from provide.foundation.utils.async_helpers import run_async

    try:
        response = run_async(
            search_logs(
                sql=sql,
                start_time=f"-{last}" if last else "-1h",
                end_time="now",
                size=size,
                client=client,
            )
        )

        # Format and display results
        if response.total == 0:
            click.echo("No logs found matching the query.")
        else:
            output = format_output(response, format_type=format)
            click.echo(output)

            # Show summary for non-summary formats
            if format != "summary":
                click.echo(f"\n📊 Found {response.total} logs, showing {len(response.hits)}")

        return 0
    except Exception as e:
        click.echo(f"Query failed: {e}", err=True)
        return 1


@click.command("query")
@click.option(
    "--sql",
    help="SQL query to execute (if not provided, builds from other options)",
)
@click.option(
    "--current-trace",
    is_flag=True,
    help="Query logs for the current active trace",
)
@click.option(
    "--trace-id",
    help="Query logs for a specific trace ID",
)
@click.option(
    "--level",
    type=click.Choice(["TRACE", "DEBUG", "INFO", "WARN", "ERROR", "CRITICAL"]),
    help="Filter by log level",
)
@click.option(
    "--service",
    help="Filter by service name",
)
@click.option(
    "--last",
    help="Time range (e.g., 1h, 30m, 5m)",
    default="1h",
)
@click.option(
    "--stream",
    default="default",
    help="Stream to query",
)
@click.option(
    "--size",
    "-n",
    type=int,
    default=100,
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
@requires_click
@with_cleanup
def query_command(
    ctx: click.Context,
    sql: str | None,
    current_trace: bool,
    trace_id: str | None,
    level: str | None,
    service: str | None,
    last: str,
    stream: str,
    size: int,
    format: str,
) -> int | None:
    """Query logs from OpenObserve.

    Examples:
        # Query recent logs
        foundation logs query --last 30m

        # Query errors
        foundation logs query --level ERROR --last 1h

        # Query by current trace
        foundation logs query --current-trace

        # Query by specific trace
        foundation logs query --trace-id abc123def456

        # Query by service
        foundation logs query --service auth-service --last 15m

        # Custom SQL query
        foundation logs query --sql "SELECT * FROM default WHERE duration_ms > 1000"

    """
    # Get client from context using shared helper
    client, error_code = get_client_from_context(ctx)
    if error_code != 0:
        exit_error("OpenObserve client not configured", code=error_code)

    # Build SQL query if not provided
    if not sql:
        trace_id_result = _get_trace_id_if_needed(current_trace, trace_id)
        if trace_id_result is None:
            exit_error("Trace ID not available", code=1)
        if trace_id_result:
            trace_id = trace_id_result

        sql = _build_query_sql(trace_id, level, service, stream, size)

    # Execute query and display results
    result = _execute_and_display_query(sql, last, size, format, client)
    if result != 0:
        exit_error("Query execution failed", code=result)

    return None


# 🧱🏗️🔚
