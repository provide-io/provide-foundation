# provide/foundation/cli/commands/logs/generate.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

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
from inspect import signature as _mutmut_signature
from typing import Annotated
from typing import Callable
from typing import ClassVar


MutantDict = Annotated[dict[str, Callable], "Mutant"]


def _mutmut_trampoline(orig, mutants, call_args, call_kwargs, self_arg = None):
    """Forward call to original or mutated function, depending on the environment"""
    import os
    mutant_under_test = os.environ['MUTANT_UNDER_TEST']
    if mutant_under_test == 'fail':
        from mutmut.__main__ import MutmutProgrammaticFailException
        raise MutmutProgrammaticFailException('Failed programmatically')      
    elif mutant_under_test == 'stats':
        from mutmut.__main__ import record_trampoline_hit
        record_trampoline_hit(orig.__module__ + '.' + orig.__name__)
        result = orig(*call_args, **call_kwargs)
        return result
    prefix = orig.__module__ + '.' + orig.__name__ + '__mutmut_'
    if not mutant_under_test.startswith(prefix):
        result = orig(*call_args, **call_kwargs)
        return result
    mutant_name = mutant_under_test.rpartition('.')[-1]
    if self_arg:
        # call to a class method where self is not bound
        result = mutants[mutant_name](self_arg, *call_args, **call_kwargs)
    else:
        result = mutants[mutant_name](*call_args, **call_kwargs)
    return result


def x__configure_rate_limiter__mutmut_orig(enable_rate_limit: bool, rate_limit: float) -> None:
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


def x__configure_rate_limiter__mutmut_1(enable_rate_limit: bool, rate_limit: float) -> None:
    """Configure Foundation's rate limiting if enabled.

    Args:
        enable_rate_limit: Whether to enable rate limiting
        rate_limit: Rate limit value (logs/s)

    """
    if enable_rate_limit:
        from provide.foundation.logger.ratelimit import GlobalRateLimiter

        limiter = None
        limiter.configure(
            global_rate=rate_limit,
            global_capacity=rate_limit * 2,  # Allow burst up to 2x the rate
        )


def x__configure_rate_limiter__mutmut_2(enable_rate_limit: bool, rate_limit: float) -> None:
    """Configure Foundation's rate limiting if enabled.

    Args:
        enable_rate_limit: Whether to enable rate limiting
        rate_limit: Rate limit value (logs/s)

    """
    if enable_rate_limit:
        from provide.foundation.logger.ratelimit import GlobalRateLimiter

        limiter = GlobalRateLimiter()
        limiter.configure(
            global_rate=None,
            global_capacity=rate_limit * 2,  # Allow burst up to 2x the rate
        )


def x__configure_rate_limiter__mutmut_3(enable_rate_limit: bool, rate_limit: float) -> None:
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
            global_capacity=None,  # Allow burst up to 2x the rate
        )


def x__configure_rate_limiter__mutmut_4(enable_rate_limit: bool, rate_limit: float) -> None:
    """Configure Foundation's rate limiting if enabled.

    Args:
        enable_rate_limit: Whether to enable rate limiting
        rate_limit: Rate limit value (logs/s)

    """
    if enable_rate_limit:
        from provide.foundation.logger.ratelimit import GlobalRateLimiter

        limiter = GlobalRateLimiter()
        limiter.configure(
            global_capacity=rate_limit * 2,  # Allow burst up to 2x the rate
        )


def x__configure_rate_limiter__mutmut_5(enable_rate_limit: bool, rate_limit: float) -> None:
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
            )


def x__configure_rate_limiter__mutmut_6(enable_rate_limit: bool, rate_limit: float) -> None:
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
            global_capacity=rate_limit / 2,  # Allow burst up to 2x the rate
        )


def x__configure_rate_limiter__mutmut_7(enable_rate_limit: bool, rate_limit: float) -> None:
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
            global_capacity=rate_limit * 3,  # Allow burst up to 2x the rate
        )

x__configure_rate_limiter__mutmut_mutants : ClassVar[MutantDict] = {
'x__configure_rate_limiter__mutmut_1': x__configure_rate_limiter__mutmut_1, 
    'x__configure_rate_limiter__mutmut_2': x__configure_rate_limiter__mutmut_2, 
    'x__configure_rate_limiter__mutmut_3': x__configure_rate_limiter__mutmut_3, 
    'x__configure_rate_limiter__mutmut_4': x__configure_rate_limiter__mutmut_4, 
    'x__configure_rate_limiter__mutmut_5': x__configure_rate_limiter__mutmut_5, 
    'x__configure_rate_limiter__mutmut_6': x__configure_rate_limiter__mutmut_6, 
    'x__configure_rate_limiter__mutmut_7': x__configure_rate_limiter__mutmut_7
}

def _configure_rate_limiter(*args, **kwargs):
    result = _mutmut_trampoline(x__configure_rate_limiter__mutmut_orig, x__configure_rate_limiter__mutmut_mutants, args, kwargs)
    return result 

_configure_rate_limiter.__signature__ = _mutmut_signature(x__configure_rate_limiter__mutmut_orig)
x__configure_rate_limiter__mutmut_orig.__name__ = 'x__configure_rate_limiter'


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


# <3 🧱🤝💻🪄
