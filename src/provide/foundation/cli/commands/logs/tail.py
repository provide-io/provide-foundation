"""
Tail logs command for Foundation CLI.
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

    @click.command("tail")
    @click.option(
        "--stream",
        "-s",
        default="default",
        help="Stream to tail",
    )
    @click.option(
        "--filter",
        "-f",
        "filter_sql",
        help="SQL WHERE clause for filtering",
    )
    @click.option(
        "--lines",
        "-n",
        type=int,
        default=10,
        help="Number of initial lines to show",
    )
    @click.option(
        "--follow/--no-follow",
        "-F/-N",
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
    def tail_command(ctx, stream, filter_sql, lines, follow, format):
        """Tail logs in real-time (like 'tail -f').

        Examples:
            # Tail all logs
            foundation logs tail

            # Tail error logs only
            foundation logs tail --filter "level='ERROR'"

            # Tail specific service
            foundation logs tail --filter "service='auth-service'"

            # Show last 20 lines and exit
            foundation logs tail -n 20 --no-follow

            # Tail with JSON output
            foundation logs tail --format json
        """
        from provide.foundation.integrations.openobserve import (
            format_output,
            tail_logs,
        )

        client = ctx.obj.get("client")
        if not client:
            click.echo("Error: OpenObserve not configured.", err=True)
            return 1

        try:
            click.echo(f"📡 Tailing logs from stream '{stream}'...")
            if filter_sql:
                click.echo(f"   Filter: {filter_sql}")
            click.echo("   Press Ctrl+C to stop\n")

            # Tail logs
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
            click.echo("\n✋ Stopped tailing logs.")
        except Exception as e:
            click.echo(f"Tail failed: {e}", err=True)
            return 1

else:

    def tail_command(*args, **kwargs):
        """Tail command stub when click is not available."""
        raise ImportError(
            "CLI commands require optional dependencies. "
            "Install with: pip install 'provide-foundation[cli]'"
        )
