#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from __future__ import annotations

from provide.foundation.cli.deps import click

"""Statistics printing for log generation."""


def print_generation_config(
    count: int,
    rate: float,
    stream: str,
    style: str,
    error_rate: float,
    enable_rate_limit: bool,
    rate_limit: float,
) -> None:
    """Print the configuration for log generation.

    Args:
        count: Number of logs to generate (0 for continuous)
        rate: Target logs per second
        stream: Target stream name
        style: Message generation style
        error_rate: Error rate (0.0 to 1.0)
        enable_rate_limit: Whether rate limiting is enabled
        rate_limit: Rate limit value (logs/s)

    """
    click.echo("🚀 Starting log generation...")
    click.echo(f"   Style: {style}")
    click.echo(f"   Error rate: {int(error_rate * 100)}%")
    click.echo(f"   Target stream: {stream}")

    if count == 0:
        click.echo(f"   Mode: Continuous at {rate} logs/second")
    else:
        click.echo(f"   Count: {count} logs at {rate} logs/second")

    if enable_rate_limit:
        click.echo(f"   ⚠️ Foundation rate limiting enabled: {rate_limit} logs/s max")

    click.echo("   Press Ctrl+C to stop\n")


def print_stats(
    current_time: float,
    last_stats_time: float,
    logs_sent: int,
    last_stats_sent: int,
    logs_failed: int,
    enable_rate_limit: bool,
    logs_rate_limited: int,
) -> tuple[float, int]:
    """Print generation statistics and return updated tracking values.

    Args:
        current_time: Current timestamp
        last_stats_time: Last time stats were printed
        logs_sent: Total logs sent
        last_stats_sent: Logs sent at last stats print
        logs_failed: Total logs failed
        enable_rate_limit: Whether rate limiting is enabled
        logs_rate_limited: Total logs rate-limited

    Returns:
        Updated (last_stats_time, last_stats_sent) tuple

    """
    if current_time - last_stats_time >= 1.0:
        current_rate = (logs_sent - last_stats_sent) / (current_time - last_stats_time)

        status = f"📊 Sent: {logs_sent:,} | Rate: {current_rate:.0f}/s"
        if logs_failed > 0:
            status += f" | Failed: {logs_failed:,}"
        if enable_rate_limit and logs_rate_limited > 0:
            status += f" | ⚠️ Rate limited: {logs_rate_limited:,}"

        click.echo(status)
        return current_time, logs_sent
    return last_stats_time, last_stats_sent


def print_final_stats(
    logs_sent: int,
    logs_failed: int,
    logs_rate_limited: int,
    total_time: float,
    rate: float,
    enable_rate_limit: bool,
) -> None:
    """Print final generation statistics.

    Args:
        logs_sent: Total logs sent
        logs_failed: Total logs failed
        logs_rate_limited: Total logs rate-limited
        total_time: Total time elapsed
        rate: Target rate (logs/s)
        enable_rate_limit: Whether rate limiting was enabled

    """
    actual_rate = logs_sent / total_time if total_time > 0 else 0

    click.echo("\n📊 Generation complete:")
    click.echo(f"   Total sent: {logs_sent} logs")
    click.echo(f"   Total failed: {logs_failed} logs")
    if enable_rate_limit:
        click.echo(f"   ⚠️  Rate limited: {logs_rate_limited} logs")
    click.echo(f"   Time: {total_time:.2f}s")
    click.echo(f"   Target rate: {rate} logs/second")
    click.echo(f"   Actual rate: {actual_rate:.1f} logs/second")


def print_progress(current: int, total: int) -> None:
    """Print progress for fixed-count generation.

    Args:
        current: Current log index
        total: Total number of logs to generate

    """
    # Print progress every 10%
    if (current + 1) % max(1, total // 10) == 0:
        progress = (current + 1) / total * 100
        click.echo(f"Progress: {progress:.0f}% ({current + 1}/{total})")


# 🧱🏗️🔚
