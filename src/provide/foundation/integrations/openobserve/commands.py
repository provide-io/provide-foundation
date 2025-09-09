"""
CLI commands for OpenObserve integration.

These commands are auto-registered by Foundation's command discovery system.
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
    from provide.foundation.integrations.openobserve import (
        OpenObserveClient,
        format_output,
        search_logs,
        tail_logs,
    )

    @click.group("openobserve", help="Query and manage OpenObserve logs")
    @click.pass_context
    def openobserve_group(ctx):
        """OpenObserve log querying and streaming commands."""
        # Initialize client and store in context
        try:
            client = OpenObserveClient.from_config()
            ctx.obj = client
        except Exception as e:
            log.warning(f"Failed to initialize OpenObserve client: {e}")
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
    @click.pass_obj
    def query_command(client, sql, start, end, size, format, pretty):
        """Execute SQL query against OpenObserve logs."""
        if client is None:
            click.echo(
                "OpenObserve not configured. Set OPENOBSERVE_URL, OPENOBSERVE_USER, and OPENOBSERVE_PASSWORD.",
                err=True,
            )
            return 1

        try:
            response = search_logs(
                sql=sql,
                start_time=start,
                end_time=end,
                size=size,
                client=client,
            )

            output = format_output(response, format_type=format, pretty=pretty)
            click.echo(output)

        except Exception as e:
            click.echo(f"Query failed: {e}", err=True)
            return 1

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
        help="SQL WHERE clause for filtering (e.g., \"level='ERROR'\")",
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
        is_flag=True,
        default=True,
        help="Follow mode (like tail -f)",
    )
    @click.option(
        "--format",
        type=click.Choice(["log", "json"]),
        default="log",
        help="Output format",
    )
    @click.pass_obj
    def tail_command(client, stream, filter_sql, lines, follow, format):
        """Tail logs from OpenObserve (like 'tail -f')."""
        if client is None:
            click.echo(
                "OpenObserve not configured. Set OPENOBSERVE_URL, OPENOBSERVE_USER, and OPENOBSERVE_PASSWORD.",
                err=True,
            )
            return 1

        try:
            click.echo(f"Tailing logs from stream '{stream}'...")
            if filter_sql:
                click.echo(f"Filter: {filter_sql}")

            for log_entry in tail_logs(
                stream=stream,
                filter_sql=filter_sql,
                follow=follow,
                lines=lines,
                client=client,
            ):
                output = format_output(log_entry, format_type=format)
                click.echo(output)

        except KeyboardInterrupt:
            click.echo("\nStopped tailing logs.")
        except Exception as e:
            click.echo(f"Tail failed: {e}", err=True)
            return 1

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
    @click.pass_obj
    def errors_command(client, stream, start, size, format):
        """Search for error logs."""
        if client is None:
            click.echo("OpenObserve not configured.", err=True)
            return 1

        try:
            from provide.foundation.integrations.openobserve import search_errors

            response = search_errors(
                stream=stream,
                start_time=start,
                size=size,
                client=client,
            )

            if response.total == 0:
                click.echo("No errors found in the specified time range.")
            else:
                output = format_output(response, format_type=format)
                click.echo(output)

        except Exception as e:
            click.echo(f"Search failed: {e}", err=True)
            return 1

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
    @click.pass_obj
    def trace_command(client, trace_id, stream, format):
        """Search for logs by trace ID."""
        if client is None:
            click.echo("OpenObserve not configured.", err=True)
            return 1

        try:
            from provide.foundation.integrations.openobserve import search_by_trace_id

            response = search_by_trace_id(
                trace_id=trace_id,
                stream=stream,
                client=client,
            )

            if response.total == 0:
                click.echo(f"No logs found for trace ID: {trace_id}")
            else:
                output = format_output(response, format_type=format)
                click.echo(output)

        except Exception as e:
            click.echo(f"Search failed: {e}", err=True)
            return 1

    @openobserve_group.command("streams")
    @click.pass_obj
    def streams_command(client):
        """List available streams."""
        if client is None:
            click.echo("OpenObserve not configured.", err=True)
            return 1

        try:
            streams = client.list_streams()

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
            return 1

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
    @click.pass_obj
    def history_command(client, size, stream):
        """View search history."""
        if client is None:
            click.echo("OpenObserve not configured.", err=True)
            return 1

        try:
            response = client.get_search_history(
                stream_name=stream,
                size=size,
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
            return 1

    @openobserve_group.command("test")
    @click.pass_obj
    def test_command(client):
        """Test connection to OpenObserve."""
        if client is None:
            click.echo("OpenObserve not configured.", err=True)
            return 1

        click.echo(f"Testing connection to {client.url}...")

        if client.test_connection():
            click.echo("✅ Connection successful!")
            click.echo(f"Organization: {client.organization}")
            click.echo(f"User: {client.username}")
        else:
            click.echo("❌ Connection failed!")
            return 1

    # Export the command group for auto-discovery
    __all__ = ["openobserve_group"]

else:
    # Stub when click is not available
    def openobserve_group(*args, **kwargs):
        """OpenObserve command stub when click is not available."""
        raise ImportError(
            "CLI commands require optional dependencies. "
            "Install with: pip install 'provide-foundation[cli]'"
        )

    __all__ = []
