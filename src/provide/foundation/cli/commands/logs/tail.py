from __future__ import annotations

import re
from typing import TYPE_CHECKING, Any

from provide.foundation.logger import get_logger

"""Tail logs command for Foundation CLI."""

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


def _parse_filter_string(filter_str: str | None) -> dict[str, str]:
    """Parse a filter string like "key='value', key2='value2'" into a dict."""
    if not filter_str:
        return {}

    filters = {}
    # Regex to find key='value' pairs, allowing for spaces and different quote types
    pattern = re.compile(r"""(\w+)\s*=\s*(['"])(.*?)\2""")
    matches = pattern.findall(filter_str)

    for key, _quote, value in matches:
        filters[key] = value

    return filters


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
        "filter_str",
        help="Filter logs using key='value' pairs (e.g., \"level='ERROR', service='api'\")",
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
    def tail_command(
        ctx: click.Context,
        stream: str,
        filter_str: str | None,
        lines: int,
        follow: bool,
        format: str,
    ) -> int | None:
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
            filters = _parse_filter_string(filter_str)

            click.echo(f"📡 Tailing logs from stream '{stream}'...")
            if filters:
                click.echo(f"   Filter: {filters}")
            click.echo("   Press Ctrl+C to stop\n")

            # Tail logs
            for log_entry in tail_logs(
                stream=stream,
                filters=filters,
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

    def tail_command(*args: object, **kwargs: object) -> None:
        """Tail command stub when click is not available."""
        raise ImportError(
            "CLI commands require optional dependencies. Install with: pip install 'provide-foundation[cli]'",
        )
