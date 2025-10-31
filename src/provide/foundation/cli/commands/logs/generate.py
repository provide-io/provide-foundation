#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from __future__ import annotations

import time

from provide.foundation.cli.commands.logs.generator import LogGenerator
from provide.foundation.cli.commands.logs.stats import (
    print_final_stats,
    print_generation_config,
)
from provide.foundation.cli.deps import click
from provide.foundation.cli.helpers import requires_click
from provide.foundation.cli.shutdown import with_cleanup

"""Command to generate logs for testing OpenObserve integration with Foundation's rate limiting."""

__all__ = ["generate_logs_command"]


def _configure_rate_limiter(enable_rate_limit: bool, rate_limit: float) -> None:
    """Configure Foundation's rate limiting if enabled.

    Args:
        enable_rate_limit: Whether to enable rate limiting
        rate_limit: Rate limit value (logs/s)

    """
    if enable_rate_limit:
        from provide.foundation.logger.ratelimit import GlobalRateLimiter

        limiter = GlobalRateLimiter()
        limiter.configure(
            global_rate=rate_limit,
            global_capacity=rate_limit * 2,  # Allow burst up to 2x the rate
        )


@click.command(name="generate")
@click.option("-n", "--count", default=100, help="Number of logs to generate (0 for continuous)")
@click.option("-r", "--rate", default=10.0, help="Logs per second rate")
@click.option("-s", "--stream", default="default", help="Target stream name")
@click.option(
    "--style",
    type=click.Choice(["normal", "burroughs"]),
    default="normal",
    help="Message generation style",
)
@click.option("-e", "--error-rate", default=0.1, help="Error rate (0.0 to 1.0)")
@click.option("--enable-rate-limit", is_flag=True, help="Enable Foundation's rate limiting")
@click.option("--rate-limit", default=100.0, help="Rate limit (logs/s) when enabled")
@requires_click
@with_cleanup
def generate_logs_command(
    count: int,
    rate: float,
    stream: str,
    style: str,
    error_rate: float,
    enable_rate_limit: bool,
    rate_limit: float,
) -> None:
    """Generate logs to test OpenObserve integration with Foundation's rate limiting.

    Args:
        count: Number of logs to generate (0 for continuous mode)
        rate: Target logs per second
        stream: Target stream name (currently unused)
        style: Message generation style ("normal" or "burroughs")
        error_rate: Probability of generating error logs (0.0 to 1.0)
        enable_rate_limit: Whether to enable Foundation's rate limiting
        rate_limit: Rate limit value (logs/s) when enabled

    """
    print_generation_config(count, rate, stream, style, error_rate, enable_rate_limit, rate_limit)
    _configure_rate_limiter(enable_rate_limit, rate_limit)

    # Create log generator
    generator = LogGenerator(style=style, error_rate=error_rate)

    start_time = time.time()
    logs_sent = logs_failed = logs_rate_limited = 0

    try:
        if count == 0:
            logs_sent, logs_failed, logs_rate_limited = generator.generate_continuous(
                rate,
                enable_rate_limit,
                logs_rate_limited,
            )
        else:
            logs_sent, logs_failed, logs_rate_limited = generator.generate_fixed_count(
                count,
                rate,
            )
    except KeyboardInterrupt:
        click.echo("\n\n⛔ Generation interrupted by user")
    finally:
        # Print final stats before cleanup
        # (OTLP flush handled by @with_cleanup decorator)
        total_time = time.time() - start_time
        print_final_stats(logs_sent, logs_failed, logs_rate_limited, total_time, rate, enable_rate_limit)


# 🧱🏗️🔚
