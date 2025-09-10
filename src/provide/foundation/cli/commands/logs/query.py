"""
Query logs command for Foundation CLI.
"""

try:
    import click

    _HAS_CLICK = True
except ImportError:
    click = None
    _HAS_CLICK = False

from provide.foundation.logger import get_logger

log = get_logger(__name__)


if _HAS_CLICK:

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
    def query_command(
        ctx, sql, current_trace, trace_id, level, service, last, stream, size, format
    ):
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
        from provide.foundation.integrations.openobserve import (
            format_output,
            search_logs,
        )

        client = ctx.obj.get("client")
        if not client:
            click.echo("Error: OpenObserve not configured.", err=True)
            return 1

        # Build SQL query if not provided
        if not sql:
            # Handle current trace
            if current_trace:
                try:
                    # Try OpenTelemetry first
                    from opentelemetry import trace

                    current_span = trace.get_current_span()
                    if current_span and current_span.is_recording():
                        span_context = current_span.get_span_context()
                        trace_id = f"{span_context.trace_id:032x}"
                    else:
                        # Try Foundation tracer
                        from provide.foundation.tracer.context import (
                            get_current_trace_id,
                        )

                        trace_id = get_current_trace_id()
                        if not trace_id:
                            click.echo("No active trace found.", err=True)
                            return 1
                except ImportError:
                    click.echo("Tracing not available.", err=True)
                    return 1

            # Build WHERE clause
            conditions = []
            if trace_id:
                conditions.append(f"trace_id = '{trace_id}'")
            if level:
                conditions.append(f"level = '{level}'")
            if service:
                conditions.append(f"service = '{service}'")

            where_clause = f"WHERE {' AND '.join(conditions)}" if conditions else ""
            sql = f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp DESC LIMIT {size}"

        # Execute query
        try:
            response = search_logs(
                sql=sql,
                start_time=f"-{last}" if last else "-1h",
                end_time="now",
                size=size,
                client=client,
            )

            # Format and display results
            if response.total == 0:
                click.echo("No logs found matching the query.")
            else:
                output = format_output(response, format_type=format)
                click.echo(output)

                # Show summary for non-summary formats
                if format != "summary":
                    click.echo(
                        f"\n📊 Found {response.total} logs, showing {len(response.hits)}"
                    )

        except Exception as e:
            click.echo(f"Query failed: {e}", err=True)
            return 1

else:

    def query_command(*args, **kwargs):
        """Query command stub when click is not available."""
        raise ImportError(
            "CLI commands require optional dependencies. "
            "Install with: pip install 'provide-foundation[cli]'"
        )
