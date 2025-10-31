#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from __future__ import annotations

from typing import TYPE_CHECKING

from provide.foundation.console.output import perr, pout
from provide.foundation.errors.decorators import resilient
from provide.foundation.hub.decorators import register_command
from provide.foundation.hub.manager import get_hub

if TYPE_CHECKING:
    from provide.foundation.context import CLIContext
    from provide.foundation.hub.manager import Hub

"""CLI commands for profiling metrics display.

Provides Foundation-native CLI commands for displaying and managing
profiling metrics with proper formatting and JSON support.
"""


@resilient(
    fallback=None,
    context_provider=lambda: {"command": "profile"},
)
def show_profile_metrics(ctx: CLIContext) -> None:
    """Display current profiling metrics.

    Args:
        ctx: CLI context with output preferences

    Example:
        $ foundation profile
        📊 Performance Metrics
          📨 Messages/sec: 14523
          ⏱️  Avg latency: 0.07ms
          🎨 Emoji overhead: 3.2%

    """
    hub = get_hub()
    profiler = hub.get_component("profiler")

    if not profiler:
        perr("❌ Profiling not enabled", color="red", ctx=ctx)
        perr("   Enable with: profiler.enable()", color="yellow", ctx=ctx)
        return

    metrics = profiler.get_metrics()

    if ctx.json_output:
        # JSON output for monitoring systems
        pout(metrics.to_dict(), json_key="metrics")
    else:
        # Human-readable output with Foundation emoji patterns
        pout("📊 Performance Metrics", bold=True, color="cyan")

        # Main metrics
        pout(f"  📨 Messages/sec: {metrics.messages_per_second:.0f}")
        pout(f"  ⏱️  Avg latency: {metrics.avg_latency_ms:.2f}ms")
        pout(f"  🎨 Emoji overhead: {metrics.emoji_overhead_percent:.1f}%")

        # Additional details
        pout(f"  📈 Total messages: {metrics.message_count:,}")
        pout(f"  🎭 Emoji messages: {metrics.emoji_message_count:,}")
        pout(f"  📊 Avg fields/msg: {metrics.avg_fields_per_message:.1f}")

        # Show uptime
        uptime = metrics.to_dict()["uptime_seconds"]
        if uptime < 60:
            pout(f"  ⏰ Uptime: {uptime:.0f}s")
        elif uptime < 3600:
            pout(f"  ⏰ Uptime: {uptime / 60:.1f}m")
        else:
            pout(f"  ⏰ Uptime: {uptime / 3600:.1f}h")

        # Warnings for dropped messages
        if metrics.dropped_count > 0:
            perr(f"  ⚠️  Dropped: {metrics.dropped_count:,}", color="yellow")

        # Status indicator
        if not profiler.enabled:
            perr("  ⚠️  Status: Disabled", color="yellow")
        else:
            sample_rate = profiler.processor.sample_rate * 100
            pout(f"  📊 Sample rate: {sample_rate:.0f}%")


@register_command("profile")
def profile_command(ctx: CLIContext) -> None:
    """Show profiling metrics for Foundation telemetry.

    Displays real-time performance metrics including throughput,
    latency, and emoji processing overhead.

    Examples:
        foundation profile              # Human-readable output
        foundation profile --json       # JSON output for monitoring

    """
    show_profile_metrics(ctx)


def register_profile_command(hub: Hub) -> None:
    """Register the profile command with the Hub.

    Args:
        hub: Hub instance to register with

    """
    # The @register_command decorator handles registration automatically
    # This function exists for explicit registration if needed
    pass


# 🧱🏗️🔚
