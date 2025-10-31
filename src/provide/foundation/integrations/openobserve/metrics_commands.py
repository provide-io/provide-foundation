#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""CLI commands for OpenObserve metrics integration.

These commands are auto-registered by Foundation's command discovery system."""

from __future__ import annotations

from typing import Any

from provide.foundation.console.output import perr
from provide.foundation.logger import get_logger
from provide.foundation.utils.async_helpers import run_async

try:
    import click

    _HAS_CLICK = True
except ImportError:
    click: Any = None  # type: ignore[no-redef]
    _HAS_CLICK = False

log = get_logger(__name__)


if _HAS_CLICK:
    from provide.foundation.integrations.openobserve import OpenObserveClient
    from provide.foundation.integrations.openobserve.metrics_formatters import (
        format_label_values,
        format_labels,
        format_metric_metadata,
        format_metric_output,
        format_metrics_list,
    )

    @click.group("metrics", help="Query and manage OpenObserve metrics")
    @click.pass_context
    def metrics_group(ctx: click.Context) -> None:
        """OpenObserve metrics querying commands."""
        # Get or create client from parent context
        if ctx.parent and hasattr(ctx.parent, "obj"):
            ctx.obj = ctx.parent.obj
        else:
            # Initialize client if not provided
            try:
                client = OpenObserveClient.from_config()
                ctx.obj = client
            except Exception as e:
                perr(f"Failed to initialize OpenObserve client: {e}")
                ctx.obj = None

    @metrics_group.command("list")
    @click.option(
        "--format",
        "-f",
        type=click.Choice(["table", "json"]),
        default="table",
        help="Output format",
    )
    @click.pass_context
    @click.pass_obj
    def list_command(client: OpenObserveClient | None, ctx: click.Context, format: str) -> None:
        """List all available metrics."""
        if client is None:
            click.echo(
                "OpenObserve not configured. Set OPENOBSERVE_URL, OPENOBSERVE_USER, and OPENOBSERVE_PASSWORD.",
                err=True,
            )
            ctx.exit(1)

        try:
            metrics = run_async(client.list_metrics())

            if format == "json":
                import json

                click.echo(json.dumps(metrics, indent=2))
            else:
                output = format_metrics_list(metrics)
                click.echo(output)

        except Exception as e:
            click.echo(f"Failed to list metrics: {e}", err=True)
            ctx.exit(1)

    @metrics_group.command("query")
    @click.argument("promql")
    @click.option(
        "--time",
        "-t",
        help="Evaluation time (Unix timestamp or RFC3339, defaults to now)",
    )
    @click.option(
        "--format",
        "-f",
        type=click.Choice(["table", "json", "csv", "summary"]),
        default="table",
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
        promql: str,
        time: str | None,
        format: str,
        pretty: bool,
    ) -> None:
        """Execute instant PromQL query.

        Examples:
            foundation openobserve metrics query "up"
            foundation openobserve metrics query "rate(http_requests_total[5m])"
            foundation openobserve metrics query "up" --format json --pretty
        """
        if client is None:
            click.echo("OpenObserve not configured.", err=True)
            ctx.exit(1)

        try:
            result = run_async(client.query_promql(query=promql, time=time))

            output = format_metric_output(result, format_type=format, pretty=pretty)
            click.echo(output)

        except Exception as e:
            click.echo(f"Query failed: {e}", err=True)
            ctx.exit(1)

    @metrics_group.command("query-range")
    @click.argument("promql")
    @click.option(
        "--start",
        "-s",
        required=True,
        help="Start time (Unix timestamp or RFC3339)",
    )
    @click.option(
        "--end",
        "-e",
        required=True,
        help="End time (Unix timestamp or RFC3339)",
    )
    @click.option(
        "--step",
        required=True,
        help="Query resolution step (e.g., '15s', '1m', or seconds as int)",
    )
    @click.option(
        "--format",
        "-f",
        type=click.Choice(["table", "json", "csv", "chart", "summary"]),
        default="table",
        help="Output format",
    )
    @click.option(
        "--pretty",
        is_flag=True,
        help="Pretty print JSON output",
    )
    @click.pass_context
    @click.pass_obj
    def query_range_command(
        client: OpenObserveClient | None,
        ctx: click.Context,
        promql: str,
        start: str,
        end: str,
        step: str,
        format: str,
        pretty: bool,
    ) -> None:
        """Execute PromQL range query over a time period.

        Examples:
            foundation openobserve metrics query-range "up" --start 1234567890 --end 1234567900 --step 10
            foundation openobserve metrics query-range "rate(http_requests[5m])" -s "2024-01-01T00:00:00Z" -e "2024-01-01T01:00:00Z" --step "1m"
        """
        if client is None:
            click.echo("OpenObserve not configured.", err=True)
            ctx.exit(1)

        try:
            result = run_async(client.query_range_promql(query=promql, start=start, end=end, step=step))

            output = format_metric_output(result, format_type=format, pretty=pretty)
            click.echo(output)

        except Exception as e:
            click.echo(f"Range query failed: {e}", err=True)
            ctx.exit(1)

    @metrics_group.command("info")
    @click.argument("metric_name", required=False)
    @click.option(
        "--format",
        "-f",
        type=click.Choice(["table", "json"]),
        default="table",
        help="Output format",
    )
    @click.pass_context
    @click.pass_obj
    def info_command(
        client: OpenObserveClient | None,
        ctx: click.Context,
        metric_name: str | None,
        format: str,
    ) -> None:
        """Get metadata about metrics.

        If metric_name is provided, shows metadata for that specific metric.
        Otherwise, shows metadata for all metrics.

        Examples:
            foundation openobserve metrics info
            foundation openobserve metrics info http_requests_total
        """
        if client is None:
            click.echo("OpenObserve not configured.", err=True)
            ctx.exit(1)

        try:
            metadata = run_async(client.get_metric_metadata(metric=metric_name))

            if not metadata:
                if metric_name:
                    click.echo(f"No metadata found for metric: {metric_name}")
                else:
                    click.echo("No metric metadata available.")
                return

            if format == "json":
                import json

                click.echo(json.dumps(metadata, indent=2))
            else:
                output = format_metric_metadata(metadata)
                click.echo(output)

        except Exception as e:
            click.echo(f"Failed to get metric metadata: {e}", err=True)
            ctx.exit(1)

    @metrics_group.command("labels")
    @click.argument("metric_name", required=False)
    @click.option(
        "--format",
        "-f",
        type=click.Choice(["table", "json"]),
        default="table",
        help="Output format",
    )
    @click.pass_context
    @click.pass_obj
    def labels_command(
        client: OpenObserveClient | None,
        ctx: click.Context,
        metric_name: str | None,
        format: str,
    ) -> None:
        """List label names for metrics.

        If metric_name is provided, shows labels for that specific metric.
        Otherwise, shows all label names across all metrics.

        Examples:
            foundation openobserve metrics labels
            foundation openobserve metrics labels http_requests_total
        """
        if client is None:
            click.echo("OpenObserve not configured.", err=True)
            ctx.exit(1)

        try:
            labels = run_async(client.get_metric_labels(metric_name=metric_name))

            if not labels:
                if metric_name:
                    click.echo(f"No labels found for metric: {metric_name}")
                else:
                    click.echo("No labels available.")
                return

            if format == "json":
                import json

                click.echo(json.dumps(labels, indent=2))
            else:
                output = format_labels(labels)
                click.echo(output)

        except Exception as e:
            click.echo(f"Failed to get labels: {e}", err=True)
            ctx.exit(1)

    @metrics_group.command("values")
    @click.argument("label_name")
    @click.option(
        "--format",
        "-f",
        type=click.Choice(["table", "json"]),
        default="table",
        help="Output format",
    )
    @click.pass_context
    @click.pass_obj
    def values_command(
        client: OpenObserveClient | None,
        ctx: click.Context,
        label_name: str,
        format: str,
    ) -> None:
        """List values for a specific label.

        Examples:
            foundation openobserve metrics values job
            foundation openobserve metrics values instance
            foundation openobserve metrics values __name__
        """
        if client is None:
            click.echo("OpenObserve not configured.", err=True)
            ctx.exit(1)

        try:
            values = run_async(client.get_label_values(label_name=label_name))

            if not values:
                click.echo(f"No values found for label: {label_name}")
                return

            if format == "json":
                import json

                click.echo(json.dumps(values, indent=2))
            else:
                output = format_label_values(label_name, values)
                click.echo(output)

        except Exception as e:
            click.echo(f"Failed to get label values: {e}", err=True)
            ctx.exit(1)

    # Export the command group for auto-discovery
    __all__ = ["metrics_group"]

else:
    # Stub when click is not available
    def metrics_group(*args: object, **kwargs: object) -> None:  # type: ignore[misc]
        """Metrics command stub when click is not available."""
        raise ImportError(
            "CLI commands require optional dependencies. Install with: pip install 'provide-foundation[cli]'",
        )

    __all__ = []

# 🧱🏗️🔚
