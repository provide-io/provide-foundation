#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from __future__ import annotations

from provide.foundation.cli.deps import click
from provide.foundation.cli.helpers import get_client_from_context, requires_click
from provide.foundation.cli.shutdown import with_cleanup
from provide.foundation.logger import get_logger
from provide.foundation.process import exit_error

"""Tail logs command for Foundation CLI."""

log = get_logger(__name__)


def _parse_filter_string_for_tail(filter_str: str | None) -> dict[str, str]:
    """Parse a filter string like "key='value', key2='value2'" into a dict.

    This version supports quoted values with regex matching, unlike the
    simple comma-separated version in helpers.py.

    Args:
        filter_str: Filter string to parse

    Returns:
        Dictionary of filter key-value pairs

    """
    import re

    if not filter_str:
        return {}

    filters = {}
    # Regex to find key='value' pairs, allowing for spaces and different quote types
    key_value_pattern = re.compile(r"""(\w+)\s*=\s*(['"])(.*?)\2""")
    matches = key_value_pattern.findall(filter_str)

    for key, _quote, value in matches:
        filters[key] = value

    return filters


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
@requires_click
@with_cleanup
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

    # Get client from context
    client, error_code = get_client_from_context(ctx)
    if error_code != 0:
        exit_error("OpenObserve client not configured", code=error_code)

    try:
        filters = _parse_filter_string_for_tail(filter_str)

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
        exit_error("Tail command failed", code=1)

    return None


# 🧱🏗️🔚
