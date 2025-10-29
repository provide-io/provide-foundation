# provide/foundation/cli/commands/logs/stats.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from provide.foundation.cli.deps import click

"""Statistics printing for log generation."""
from inspect import signature as _mutmut_signature
from typing import Annotated
from typing import Callable
from typing import ClassVar


MutantDict = Annotated[dict[str, Callable], "Mutant"]


def _mutmut_trampoline(orig, mutants, call_args, call_kwargs, self_arg=None):
    """Forward call to original or mutated function, depending on the environment"""
    import os

    mutant_under_test = os.environ["MUTANT_UNDER_TEST"]
    if mutant_under_test == "fail":
        from mutmut.__main__ import MutmutProgrammaticFailException

        raise MutmutProgrammaticFailException("Failed programmatically")
    elif mutant_under_test == "stats":
        from mutmut.__main__ import record_trampoline_hit

        record_trampoline_hit(orig.__module__ + "." + orig.__name__)
        result = orig(*call_args, **call_kwargs)
        return result
    prefix = orig.__module__ + "." + orig.__name__ + "__mutmut_"
    if not mutant_under_test.startswith(prefix):
        result = orig(*call_args, **call_kwargs)
        return result
    mutant_name = mutant_under_test.rpartition(".")[-1]
    if self_arg:
        # call to a class method where self is not bound
        result = mutants[mutant_name](self_arg, *call_args, **call_kwargs)
    else:
        result = mutants[mutant_name](*call_args, **call_kwargs)
    return result


def x_print_generation_config__mutmut_orig(
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


def x_print_generation_config__mutmut_1(
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
    click.echo(None)
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


def x_print_generation_config__mutmut_2(
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
    click.echo("XX🚀 Starting log generation...XX")
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


def x_print_generation_config__mutmut_3(
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
    click.echo("🚀 starting log generation...")
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


def x_print_generation_config__mutmut_4(
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
    click.echo("🚀 STARTING LOG GENERATION...")
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


def x_print_generation_config__mutmut_5(
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
    click.echo(None)
    click.echo(f"   Error rate: {int(error_rate * 100)}%")
    click.echo(f"   Target stream: {stream}")

    if count == 0:
        click.echo(f"   Mode: Continuous at {rate} logs/second")
    else:
        click.echo(f"   Count: {count} logs at {rate} logs/second")

    if enable_rate_limit:
        click.echo(f"   ⚠️ Foundation rate limiting enabled: {rate_limit} logs/s max")

    click.echo("   Press Ctrl+C to stop\n")


def x_print_generation_config__mutmut_6(
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
    click.echo(None)
    click.echo(f"   Target stream: {stream}")

    if count == 0:
        click.echo(f"   Mode: Continuous at {rate} logs/second")
    else:
        click.echo(f"   Count: {count} logs at {rate} logs/second")

    if enable_rate_limit:
        click.echo(f"   ⚠️ Foundation rate limiting enabled: {rate_limit} logs/s max")

    click.echo("   Press Ctrl+C to stop\n")


def x_print_generation_config__mutmut_7(
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
    click.echo(f"   Error rate: {int(None)}%")
    click.echo(f"   Target stream: {stream}")

    if count == 0:
        click.echo(f"   Mode: Continuous at {rate} logs/second")
    else:
        click.echo(f"   Count: {count} logs at {rate} logs/second")

    if enable_rate_limit:
        click.echo(f"   ⚠️ Foundation rate limiting enabled: {rate_limit} logs/s max")

    click.echo("   Press Ctrl+C to stop\n")


def x_print_generation_config__mutmut_8(
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
    click.echo(f"   Error rate: {int(error_rate / 100)}%")
    click.echo(f"   Target stream: {stream}")

    if count == 0:
        click.echo(f"   Mode: Continuous at {rate} logs/second")
    else:
        click.echo(f"   Count: {count} logs at {rate} logs/second")

    if enable_rate_limit:
        click.echo(f"   ⚠️ Foundation rate limiting enabled: {rate_limit} logs/s max")

    click.echo("   Press Ctrl+C to stop\n")


def x_print_generation_config__mutmut_9(
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
    click.echo(f"   Error rate: {int(error_rate * 101)}%")
    click.echo(f"   Target stream: {stream}")

    if count == 0:
        click.echo(f"   Mode: Continuous at {rate} logs/second")
    else:
        click.echo(f"   Count: {count} logs at {rate} logs/second")

    if enable_rate_limit:
        click.echo(f"   ⚠️ Foundation rate limiting enabled: {rate_limit} logs/s max")

    click.echo("   Press Ctrl+C to stop\n")


def x_print_generation_config__mutmut_10(
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
    click.echo(None)

    if count == 0:
        click.echo(f"   Mode: Continuous at {rate} logs/second")
    else:
        click.echo(f"   Count: {count} logs at {rate} logs/second")

    if enable_rate_limit:
        click.echo(f"   ⚠️ Foundation rate limiting enabled: {rate_limit} logs/s max")

    click.echo("   Press Ctrl+C to stop\n")


def x_print_generation_config__mutmut_11(
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

    if count != 0:
        click.echo(f"   Mode: Continuous at {rate} logs/second")
    else:
        click.echo(f"   Count: {count} logs at {rate} logs/second")

    if enable_rate_limit:
        click.echo(f"   ⚠️ Foundation rate limiting enabled: {rate_limit} logs/s max")

    click.echo("   Press Ctrl+C to stop\n")


def x_print_generation_config__mutmut_12(
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

    if count == 1:
        click.echo(f"   Mode: Continuous at {rate} logs/second")
    else:
        click.echo(f"   Count: {count} logs at {rate} logs/second")

    if enable_rate_limit:
        click.echo(f"   ⚠️ Foundation rate limiting enabled: {rate_limit} logs/s max")

    click.echo("   Press Ctrl+C to stop\n")


def x_print_generation_config__mutmut_13(
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
        click.echo(None)
    else:
        click.echo(f"   Count: {count} logs at {rate} logs/second")

    if enable_rate_limit:
        click.echo(f"   ⚠️ Foundation rate limiting enabled: {rate_limit} logs/s max")

    click.echo("   Press Ctrl+C to stop\n")


def x_print_generation_config__mutmut_14(
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
        click.echo(None)

    if enable_rate_limit:
        click.echo(f"   ⚠️ Foundation rate limiting enabled: {rate_limit} logs/s max")

    click.echo("   Press Ctrl+C to stop\n")


def x_print_generation_config__mutmut_15(
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
        click.echo(None)

    click.echo("   Press Ctrl+C to stop\n")


def x_print_generation_config__mutmut_16(
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

    click.echo(None)


def x_print_generation_config__mutmut_17(
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

    click.echo("XX   Press Ctrl+C to stop\nXX")


def x_print_generation_config__mutmut_18(
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

    click.echo("   press ctrl+c to stop\n")


def x_print_generation_config__mutmut_19(
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

    click.echo("   PRESS CTRL+C TO STOP\n")


x_print_generation_config__mutmut_mutants: ClassVar[MutantDict] = {
    "x_print_generation_config__mutmut_1": x_print_generation_config__mutmut_1,
    "x_print_generation_config__mutmut_2": x_print_generation_config__mutmut_2,
    "x_print_generation_config__mutmut_3": x_print_generation_config__mutmut_3,
    "x_print_generation_config__mutmut_4": x_print_generation_config__mutmut_4,
    "x_print_generation_config__mutmut_5": x_print_generation_config__mutmut_5,
    "x_print_generation_config__mutmut_6": x_print_generation_config__mutmut_6,
    "x_print_generation_config__mutmut_7": x_print_generation_config__mutmut_7,
    "x_print_generation_config__mutmut_8": x_print_generation_config__mutmut_8,
    "x_print_generation_config__mutmut_9": x_print_generation_config__mutmut_9,
    "x_print_generation_config__mutmut_10": x_print_generation_config__mutmut_10,
    "x_print_generation_config__mutmut_11": x_print_generation_config__mutmut_11,
    "x_print_generation_config__mutmut_12": x_print_generation_config__mutmut_12,
    "x_print_generation_config__mutmut_13": x_print_generation_config__mutmut_13,
    "x_print_generation_config__mutmut_14": x_print_generation_config__mutmut_14,
    "x_print_generation_config__mutmut_15": x_print_generation_config__mutmut_15,
    "x_print_generation_config__mutmut_16": x_print_generation_config__mutmut_16,
    "x_print_generation_config__mutmut_17": x_print_generation_config__mutmut_17,
    "x_print_generation_config__mutmut_18": x_print_generation_config__mutmut_18,
    "x_print_generation_config__mutmut_19": x_print_generation_config__mutmut_19,
}


def print_generation_config(*args, **kwargs):
    result = _mutmut_trampoline(
        x_print_generation_config__mutmut_orig, x_print_generation_config__mutmut_mutants, args, kwargs
    )
    return result


print_generation_config.__signature__ = _mutmut_signature(x_print_generation_config__mutmut_orig)
x_print_generation_config__mutmut_orig.__name__ = "x_print_generation_config"


def x_print_stats__mutmut_orig(
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


def x_print_stats__mutmut_1(
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
    if current_time + last_stats_time >= 1.0:
        current_rate = (logs_sent - last_stats_sent) / (current_time - last_stats_time)

        status = f"📊 Sent: {logs_sent:,} | Rate: {current_rate:.0f}/s"
        if logs_failed > 0:
            status += f" | Failed: {logs_failed:,}"
        if enable_rate_limit and logs_rate_limited > 0:
            status += f" | ⚠️ Rate limited: {logs_rate_limited:,}"

        click.echo(status)
        return current_time, logs_sent
    return last_stats_time, last_stats_sent


def x_print_stats__mutmut_2(
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
    if current_time - last_stats_time > 1.0:
        current_rate = (logs_sent - last_stats_sent) / (current_time - last_stats_time)

        status = f"📊 Sent: {logs_sent:,} | Rate: {current_rate:.0f}/s"
        if logs_failed > 0:
            status += f" | Failed: {logs_failed:,}"
        if enable_rate_limit and logs_rate_limited > 0:
            status += f" | ⚠️ Rate limited: {logs_rate_limited:,}"

        click.echo(status)
        return current_time, logs_sent
    return last_stats_time, last_stats_sent


def x_print_stats__mutmut_3(
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
    if current_time - last_stats_time >= 2.0:
        current_rate = (logs_sent - last_stats_sent) / (current_time - last_stats_time)

        status = f"📊 Sent: {logs_sent:,} | Rate: {current_rate:.0f}/s"
        if logs_failed > 0:
            status += f" | Failed: {logs_failed:,}"
        if enable_rate_limit and logs_rate_limited > 0:
            status += f" | ⚠️ Rate limited: {logs_rate_limited:,}"

        click.echo(status)
        return current_time, logs_sent
    return last_stats_time, last_stats_sent


def x_print_stats__mutmut_4(
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
        current_rate = None

        status = f"📊 Sent: {logs_sent:,} | Rate: {current_rate:.0f}/s"
        if logs_failed > 0:
            status += f" | Failed: {logs_failed:,}"
        if enable_rate_limit and logs_rate_limited > 0:
            status += f" | ⚠️ Rate limited: {logs_rate_limited:,}"

        click.echo(status)
        return current_time, logs_sent
    return last_stats_time, last_stats_sent


def x_print_stats__mutmut_5(
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
        current_rate = (logs_sent - last_stats_sent) * (current_time - last_stats_time)

        status = f"📊 Sent: {logs_sent:,} | Rate: {current_rate:.0f}/s"
        if logs_failed > 0:
            status += f" | Failed: {logs_failed:,}"
        if enable_rate_limit and logs_rate_limited > 0:
            status += f" | ⚠️ Rate limited: {logs_rate_limited:,}"

        click.echo(status)
        return current_time, logs_sent
    return last_stats_time, last_stats_sent


def x_print_stats__mutmut_6(
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
        current_rate = (logs_sent + last_stats_sent) / (current_time - last_stats_time)

        status = f"📊 Sent: {logs_sent:,} | Rate: {current_rate:.0f}/s"
        if logs_failed > 0:
            status += f" | Failed: {logs_failed:,}"
        if enable_rate_limit and logs_rate_limited > 0:
            status += f" | ⚠️ Rate limited: {logs_rate_limited:,}"

        click.echo(status)
        return current_time, logs_sent
    return last_stats_time, last_stats_sent


def x_print_stats__mutmut_7(
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
        current_rate = (logs_sent - last_stats_sent) / (current_time + last_stats_time)

        status = f"📊 Sent: {logs_sent:,} | Rate: {current_rate:.0f}/s"
        if logs_failed > 0:
            status += f" | Failed: {logs_failed:,}"
        if enable_rate_limit and logs_rate_limited > 0:
            status += f" | ⚠️ Rate limited: {logs_rate_limited:,}"

        click.echo(status)
        return current_time, logs_sent
    return last_stats_time, last_stats_sent


def x_print_stats__mutmut_8(
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

        status = None
        if logs_failed > 0:
            status += f" | Failed: {logs_failed:,}"
        if enable_rate_limit and logs_rate_limited > 0:
            status += f" | ⚠️ Rate limited: {logs_rate_limited:,}"

        click.echo(status)
        return current_time, logs_sent
    return last_stats_time, last_stats_sent


def x_print_stats__mutmut_9(
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
        if logs_failed >= 0:
            status += f" | Failed: {logs_failed:,}"
        if enable_rate_limit and logs_rate_limited > 0:
            status += f" | ⚠️ Rate limited: {logs_rate_limited:,}"

        click.echo(status)
        return current_time, logs_sent
    return last_stats_time, last_stats_sent


def x_print_stats__mutmut_10(
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
        if logs_failed > 1:
            status += f" | Failed: {logs_failed:,}"
        if enable_rate_limit and logs_rate_limited > 0:
            status += f" | ⚠️ Rate limited: {logs_rate_limited:,}"

        click.echo(status)
        return current_time, logs_sent
    return last_stats_time, last_stats_sent


def x_print_stats__mutmut_11(
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
            status = f" | Failed: {logs_failed:,}"
        if enable_rate_limit and logs_rate_limited > 0:
            status += f" | ⚠️ Rate limited: {logs_rate_limited:,}"

        click.echo(status)
        return current_time, logs_sent
    return last_stats_time, last_stats_sent


def x_print_stats__mutmut_12(
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
            status -= f" | Failed: {logs_failed:,}"
        if enable_rate_limit and logs_rate_limited > 0:
            status += f" | ⚠️ Rate limited: {logs_rate_limited:,}"

        click.echo(status)
        return current_time, logs_sent
    return last_stats_time, last_stats_sent


def x_print_stats__mutmut_13(
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
        if enable_rate_limit or logs_rate_limited > 0:
            status += f" | ⚠️ Rate limited: {logs_rate_limited:,}"

        click.echo(status)
        return current_time, logs_sent
    return last_stats_time, last_stats_sent


def x_print_stats__mutmut_14(
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
        if enable_rate_limit and logs_rate_limited >= 0:
            status += f" | ⚠️ Rate limited: {logs_rate_limited:,}"

        click.echo(status)
        return current_time, logs_sent
    return last_stats_time, last_stats_sent


def x_print_stats__mutmut_15(
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
        if enable_rate_limit and logs_rate_limited > 1:
            status += f" | ⚠️ Rate limited: {logs_rate_limited:,}"

        click.echo(status)
        return current_time, logs_sent
    return last_stats_time, last_stats_sent


def x_print_stats__mutmut_16(
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
            status = f" | ⚠️ Rate limited: {logs_rate_limited:,}"

        click.echo(status)
        return current_time, logs_sent
    return last_stats_time, last_stats_sent


def x_print_stats__mutmut_17(
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
            status -= f" | ⚠️ Rate limited: {logs_rate_limited:,}"

        click.echo(status)
        return current_time, logs_sent
    return last_stats_time, last_stats_sent


def x_print_stats__mutmut_18(
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

        click.echo(None)
        return current_time, logs_sent
    return last_stats_time, last_stats_sent


x_print_stats__mutmut_mutants: ClassVar[MutantDict] = {
    "x_print_stats__mutmut_1": x_print_stats__mutmut_1,
    "x_print_stats__mutmut_2": x_print_stats__mutmut_2,
    "x_print_stats__mutmut_3": x_print_stats__mutmut_3,
    "x_print_stats__mutmut_4": x_print_stats__mutmut_4,
    "x_print_stats__mutmut_5": x_print_stats__mutmut_5,
    "x_print_stats__mutmut_6": x_print_stats__mutmut_6,
    "x_print_stats__mutmut_7": x_print_stats__mutmut_7,
    "x_print_stats__mutmut_8": x_print_stats__mutmut_8,
    "x_print_stats__mutmut_9": x_print_stats__mutmut_9,
    "x_print_stats__mutmut_10": x_print_stats__mutmut_10,
    "x_print_stats__mutmut_11": x_print_stats__mutmut_11,
    "x_print_stats__mutmut_12": x_print_stats__mutmut_12,
    "x_print_stats__mutmut_13": x_print_stats__mutmut_13,
    "x_print_stats__mutmut_14": x_print_stats__mutmut_14,
    "x_print_stats__mutmut_15": x_print_stats__mutmut_15,
    "x_print_stats__mutmut_16": x_print_stats__mutmut_16,
    "x_print_stats__mutmut_17": x_print_stats__mutmut_17,
    "x_print_stats__mutmut_18": x_print_stats__mutmut_18,
}


def print_stats(*args, **kwargs):
    result = _mutmut_trampoline(x_print_stats__mutmut_orig, x_print_stats__mutmut_mutants, args, kwargs)
    return result


print_stats.__signature__ = _mutmut_signature(x_print_stats__mutmut_orig)
x_print_stats__mutmut_orig.__name__ = "x_print_stats"


def x_print_final_stats__mutmut_orig(
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


def x_print_final_stats__mutmut_1(
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
    actual_rate = None

    click.echo("\n📊 Generation complete:")
    click.echo(f"   Total sent: {logs_sent} logs")
    click.echo(f"   Total failed: {logs_failed} logs")
    if enable_rate_limit:
        click.echo(f"   ⚠️  Rate limited: {logs_rate_limited} logs")
    click.echo(f"   Time: {total_time:.2f}s")
    click.echo(f"   Target rate: {rate} logs/second")
    click.echo(f"   Actual rate: {actual_rate:.1f} logs/second")


def x_print_final_stats__mutmut_2(
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
    actual_rate = logs_sent * total_time if total_time > 0 else 0

    click.echo("\n📊 Generation complete:")
    click.echo(f"   Total sent: {logs_sent} logs")
    click.echo(f"   Total failed: {logs_failed} logs")
    if enable_rate_limit:
        click.echo(f"   ⚠️  Rate limited: {logs_rate_limited} logs")
    click.echo(f"   Time: {total_time:.2f}s")
    click.echo(f"   Target rate: {rate} logs/second")
    click.echo(f"   Actual rate: {actual_rate:.1f} logs/second")


def x_print_final_stats__mutmut_3(
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
    actual_rate = logs_sent / total_time if total_time >= 0 else 0

    click.echo("\n📊 Generation complete:")
    click.echo(f"   Total sent: {logs_sent} logs")
    click.echo(f"   Total failed: {logs_failed} logs")
    if enable_rate_limit:
        click.echo(f"   ⚠️  Rate limited: {logs_rate_limited} logs")
    click.echo(f"   Time: {total_time:.2f}s")
    click.echo(f"   Target rate: {rate} logs/second")
    click.echo(f"   Actual rate: {actual_rate:.1f} logs/second")


def x_print_final_stats__mutmut_4(
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
    actual_rate = logs_sent / total_time if total_time > 1 else 0

    click.echo("\n📊 Generation complete:")
    click.echo(f"   Total sent: {logs_sent} logs")
    click.echo(f"   Total failed: {logs_failed} logs")
    if enable_rate_limit:
        click.echo(f"   ⚠️  Rate limited: {logs_rate_limited} logs")
    click.echo(f"   Time: {total_time:.2f}s")
    click.echo(f"   Target rate: {rate} logs/second")
    click.echo(f"   Actual rate: {actual_rate:.1f} logs/second")


def x_print_final_stats__mutmut_5(
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
    actual_rate = logs_sent / total_time if total_time > 0 else 1

    click.echo("\n📊 Generation complete:")
    click.echo(f"   Total sent: {logs_sent} logs")
    click.echo(f"   Total failed: {logs_failed} logs")
    if enable_rate_limit:
        click.echo(f"   ⚠️  Rate limited: {logs_rate_limited} logs")
    click.echo(f"   Time: {total_time:.2f}s")
    click.echo(f"   Target rate: {rate} logs/second")
    click.echo(f"   Actual rate: {actual_rate:.1f} logs/second")


def x_print_final_stats__mutmut_6(
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

    click.echo(None)
    click.echo(f"   Total sent: {logs_sent} logs")
    click.echo(f"   Total failed: {logs_failed} logs")
    if enable_rate_limit:
        click.echo(f"   ⚠️  Rate limited: {logs_rate_limited} logs")
    click.echo(f"   Time: {total_time:.2f}s")
    click.echo(f"   Target rate: {rate} logs/second")
    click.echo(f"   Actual rate: {actual_rate:.1f} logs/second")


def x_print_final_stats__mutmut_7(
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

    click.echo("XX\n📊 Generation complete:XX")
    click.echo(f"   Total sent: {logs_sent} logs")
    click.echo(f"   Total failed: {logs_failed} logs")
    if enable_rate_limit:
        click.echo(f"   ⚠️  Rate limited: {logs_rate_limited} logs")
    click.echo(f"   Time: {total_time:.2f}s")
    click.echo(f"   Target rate: {rate} logs/second")
    click.echo(f"   Actual rate: {actual_rate:.1f} logs/second")


def x_print_final_stats__mutmut_8(
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

    click.echo("\n📊 generation complete:")
    click.echo(f"   Total sent: {logs_sent} logs")
    click.echo(f"   Total failed: {logs_failed} logs")
    if enable_rate_limit:
        click.echo(f"   ⚠️  Rate limited: {logs_rate_limited} logs")
    click.echo(f"   Time: {total_time:.2f}s")
    click.echo(f"   Target rate: {rate} logs/second")
    click.echo(f"   Actual rate: {actual_rate:.1f} logs/second")


def x_print_final_stats__mutmut_9(
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

    click.echo("\n📊 GENERATION COMPLETE:")
    click.echo(f"   Total sent: {logs_sent} logs")
    click.echo(f"   Total failed: {logs_failed} logs")
    if enable_rate_limit:
        click.echo(f"   ⚠️  Rate limited: {logs_rate_limited} logs")
    click.echo(f"   Time: {total_time:.2f}s")
    click.echo(f"   Target rate: {rate} logs/second")
    click.echo(f"   Actual rate: {actual_rate:.1f} logs/second")


def x_print_final_stats__mutmut_10(
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
    click.echo(None)
    click.echo(f"   Total failed: {logs_failed} logs")
    if enable_rate_limit:
        click.echo(f"   ⚠️  Rate limited: {logs_rate_limited} logs")
    click.echo(f"   Time: {total_time:.2f}s")
    click.echo(f"   Target rate: {rate} logs/second")
    click.echo(f"   Actual rate: {actual_rate:.1f} logs/second")


def x_print_final_stats__mutmut_11(
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
    click.echo(None)
    if enable_rate_limit:
        click.echo(f"   ⚠️  Rate limited: {logs_rate_limited} logs")
    click.echo(f"   Time: {total_time:.2f}s")
    click.echo(f"   Target rate: {rate} logs/second")
    click.echo(f"   Actual rate: {actual_rate:.1f} logs/second")


def x_print_final_stats__mutmut_12(
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
        click.echo(None)
    click.echo(f"   Time: {total_time:.2f}s")
    click.echo(f"   Target rate: {rate} logs/second")
    click.echo(f"   Actual rate: {actual_rate:.1f} logs/second")


def x_print_final_stats__mutmut_13(
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
    click.echo(None)
    click.echo(f"   Target rate: {rate} logs/second")
    click.echo(f"   Actual rate: {actual_rate:.1f} logs/second")


def x_print_final_stats__mutmut_14(
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
    click.echo(None)
    click.echo(f"   Actual rate: {actual_rate:.1f} logs/second")


def x_print_final_stats__mutmut_15(
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
    click.echo(None)


x_print_final_stats__mutmut_mutants: ClassVar[MutantDict] = {
    "x_print_final_stats__mutmut_1": x_print_final_stats__mutmut_1,
    "x_print_final_stats__mutmut_2": x_print_final_stats__mutmut_2,
    "x_print_final_stats__mutmut_3": x_print_final_stats__mutmut_3,
    "x_print_final_stats__mutmut_4": x_print_final_stats__mutmut_4,
    "x_print_final_stats__mutmut_5": x_print_final_stats__mutmut_5,
    "x_print_final_stats__mutmut_6": x_print_final_stats__mutmut_6,
    "x_print_final_stats__mutmut_7": x_print_final_stats__mutmut_7,
    "x_print_final_stats__mutmut_8": x_print_final_stats__mutmut_8,
    "x_print_final_stats__mutmut_9": x_print_final_stats__mutmut_9,
    "x_print_final_stats__mutmut_10": x_print_final_stats__mutmut_10,
    "x_print_final_stats__mutmut_11": x_print_final_stats__mutmut_11,
    "x_print_final_stats__mutmut_12": x_print_final_stats__mutmut_12,
    "x_print_final_stats__mutmut_13": x_print_final_stats__mutmut_13,
    "x_print_final_stats__mutmut_14": x_print_final_stats__mutmut_14,
    "x_print_final_stats__mutmut_15": x_print_final_stats__mutmut_15,
}


def print_final_stats(*args, **kwargs):
    result = _mutmut_trampoline(
        x_print_final_stats__mutmut_orig, x_print_final_stats__mutmut_mutants, args, kwargs
    )
    return result


print_final_stats.__signature__ = _mutmut_signature(x_print_final_stats__mutmut_orig)
x_print_final_stats__mutmut_orig.__name__ = "x_print_final_stats"


def x_print_progress__mutmut_orig(current: int, total: int) -> None:
    """Print progress for fixed-count generation.

    Args:
        current: Current log index
        total: Total number of logs to generate

    """
    # Print progress every 10%
    if (current + 1) % max(1, total // 10) == 0:
        progress = (current + 1) / total * 100
        click.echo(f"Progress: {progress:.0f}% ({current + 1}/{total})")


def x_print_progress__mutmut_1(current: int, total: int) -> None:
    """Print progress for fixed-count generation.

    Args:
        current: Current log index
        total: Total number of logs to generate

    """
    # Print progress every 10%
    if (current + 1) / max(1, total // 10) == 0:
        progress = (current + 1) / total * 100
        click.echo(f"Progress: {progress:.0f}% ({current + 1}/{total})")


def x_print_progress__mutmut_2(current: int, total: int) -> None:
    """Print progress for fixed-count generation.

    Args:
        current: Current log index
        total: Total number of logs to generate

    """
    # Print progress every 10%
    if (current - 1) % max(1, total // 10) == 0:
        progress = (current + 1) / total * 100
        click.echo(f"Progress: {progress:.0f}% ({current + 1}/{total})")


def x_print_progress__mutmut_3(current: int, total: int) -> None:
    """Print progress for fixed-count generation.

    Args:
        current: Current log index
        total: Total number of logs to generate

    """
    # Print progress every 10%
    if (current + 2) % max(1, total // 10) == 0:
        progress = (current + 1) / total * 100
        click.echo(f"Progress: {progress:.0f}% ({current + 1}/{total})")


def x_print_progress__mutmut_4(current: int, total: int) -> None:
    """Print progress for fixed-count generation.

    Args:
        current: Current log index
        total: Total number of logs to generate

    """
    # Print progress every 10%
    if (current + 1) % max(None, total // 10) == 0:
        progress = (current + 1) / total * 100
        click.echo(f"Progress: {progress:.0f}% ({current + 1}/{total})")


def x_print_progress__mutmut_5(current: int, total: int) -> None:
    """Print progress for fixed-count generation.

    Args:
        current: Current log index
        total: Total number of logs to generate

    """
    # Print progress every 10%
    if (current + 1) % max(1, None) == 0:
        progress = (current + 1) / total * 100
        click.echo(f"Progress: {progress:.0f}% ({current + 1}/{total})")


def x_print_progress__mutmut_6(current: int, total: int) -> None:
    """Print progress for fixed-count generation.

    Args:
        current: Current log index
        total: Total number of logs to generate

    """
    # Print progress every 10%
    if (current + 1) % max(total // 10) == 0:
        progress = (current + 1) / total * 100
        click.echo(f"Progress: {progress:.0f}% ({current + 1}/{total})")


def x_print_progress__mutmut_7(current: int, total: int) -> None:
    """Print progress for fixed-count generation.

    Args:
        current: Current log index
        total: Total number of logs to generate

    """
    # Print progress every 10%
    if (current + 1) % max(
        1,
    ) == 0:
        progress = (current + 1) / total * 100
        click.echo(f"Progress: {progress:.0f}% ({current + 1}/{total})")


def x_print_progress__mutmut_8(current: int, total: int) -> None:
    """Print progress for fixed-count generation.

    Args:
        current: Current log index
        total: Total number of logs to generate

    """
    # Print progress every 10%
    if (current + 1) % max(2, total // 10) == 0:
        progress = (current + 1) / total * 100
        click.echo(f"Progress: {progress:.0f}% ({current + 1}/{total})")


def x_print_progress__mutmut_9(current: int, total: int) -> None:
    """Print progress for fixed-count generation.

    Args:
        current: Current log index
        total: Total number of logs to generate

    """
    # Print progress every 10%
    if (current + 1) % max(1, total / 10) == 0:
        progress = (current + 1) / total * 100
        click.echo(f"Progress: {progress:.0f}% ({current + 1}/{total})")


def x_print_progress__mutmut_10(current: int, total: int) -> None:
    """Print progress for fixed-count generation.

    Args:
        current: Current log index
        total: Total number of logs to generate

    """
    # Print progress every 10%
    if (current + 1) % max(1, total // 11) == 0:
        progress = (current + 1) / total * 100
        click.echo(f"Progress: {progress:.0f}% ({current + 1}/{total})")


def x_print_progress__mutmut_11(current: int, total: int) -> None:
    """Print progress for fixed-count generation.

    Args:
        current: Current log index
        total: Total number of logs to generate

    """
    # Print progress every 10%
    if (current + 1) % max(1, total // 10) != 0:
        progress = (current + 1) / total * 100
        click.echo(f"Progress: {progress:.0f}% ({current + 1}/{total})")


def x_print_progress__mutmut_12(current: int, total: int) -> None:
    """Print progress for fixed-count generation.

    Args:
        current: Current log index
        total: Total number of logs to generate

    """
    # Print progress every 10%
    if (current + 1) % max(1, total // 10) == 1:
        progress = (current + 1) / total * 100
        click.echo(f"Progress: {progress:.0f}% ({current + 1}/{total})")


def x_print_progress__mutmut_13(current: int, total: int) -> None:
    """Print progress for fixed-count generation.

    Args:
        current: Current log index
        total: Total number of logs to generate

    """
    # Print progress every 10%
    if (current + 1) % max(1, total // 10) == 0:
        progress = None
        click.echo(f"Progress: {progress:.0f}% ({current + 1}/{total})")


def x_print_progress__mutmut_14(current: int, total: int) -> None:
    """Print progress for fixed-count generation.

    Args:
        current: Current log index
        total: Total number of logs to generate

    """
    # Print progress every 10%
    if (current + 1) % max(1, total // 10) == 0:
        progress = (current + 1) / total / 100
        click.echo(f"Progress: {progress:.0f}% ({current + 1}/{total})")


def x_print_progress__mutmut_15(current: int, total: int) -> None:
    """Print progress for fixed-count generation.

    Args:
        current: Current log index
        total: Total number of logs to generate

    """
    # Print progress every 10%
    if (current + 1) % max(1, total // 10) == 0:
        progress = (current + 1) * total * 100
        click.echo(f"Progress: {progress:.0f}% ({current + 1}/{total})")


def x_print_progress__mutmut_16(current: int, total: int) -> None:
    """Print progress for fixed-count generation.

    Args:
        current: Current log index
        total: Total number of logs to generate

    """
    # Print progress every 10%
    if (current + 1) % max(1, total // 10) == 0:
        progress = (current - 1) / total * 100
        click.echo(f"Progress: {progress:.0f}% ({current + 1}/{total})")


def x_print_progress__mutmut_17(current: int, total: int) -> None:
    """Print progress for fixed-count generation.

    Args:
        current: Current log index
        total: Total number of logs to generate

    """
    # Print progress every 10%
    if (current + 1) % max(1, total // 10) == 0:
        progress = (current + 2) / total * 100
        click.echo(f"Progress: {progress:.0f}% ({current + 1}/{total})")


def x_print_progress__mutmut_18(current: int, total: int) -> None:
    """Print progress for fixed-count generation.

    Args:
        current: Current log index
        total: Total number of logs to generate

    """
    # Print progress every 10%
    if (current + 1) % max(1, total // 10) == 0:
        progress = (current + 1) / total * 101
        click.echo(f"Progress: {progress:.0f}% ({current + 1}/{total})")


def x_print_progress__mutmut_19(current: int, total: int) -> None:
    """Print progress for fixed-count generation.

    Args:
        current: Current log index
        total: Total number of logs to generate

    """
    # Print progress every 10%
    if (current + 1) % max(1, total // 10) == 0:
        progress = (current + 1) / total * 100
        click.echo(None)


def x_print_progress__mutmut_20(current: int, total: int) -> None:
    """Print progress for fixed-count generation.

    Args:
        current: Current log index
        total: Total number of logs to generate

    """
    # Print progress every 10%
    if (current + 1) % max(1, total // 10) == 0:
        progress = (current + 1) / total * 100
        click.echo(f"Progress: {progress:.0f}% ({current - 1}/{total})")


def x_print_progress__mutmut_21(current: int, total: int) -> None:
    """Print progress for fixed-count generation.

    Args:
        current: Current log index
        total: Total number of logs to generate

    """
    # Print progress every 10%
    if (current + 1) % max(1, total // 10) == 0:
        progress = (current + 1) / total * 100
        click.echo(f"Progress: {progress:.0f}% ({current + 2}/{total})")


x_print_progress__mutmut_mutants: ClassVar[MutantDict] = {
    "x_print_progress__mutmut_1": x_print_progress__mutmut_1,
    "x_print_progress__mutmut_2": x_print_progress__mutmut_2,
    "x_print_progress__mutmut_3": x_print_progress__mutmut_3,
    "x_print_progress__mutmut_4": x_print_progress__mutmut_4,
    "x_print_progress__mutmut_5": x_print_progress__mutmut_5,
    "x_print_progress__mutmut_6": x_print_progress__mutmut_6,
    "x_print_progress__mutmut_7": x_print_progress__mutmut_7,
    "x_print_progress__mutmut_8": x_print_progress__mutmut_8,
    "x_print_progress__mutmut_9": x_print_progress__mutmut_9,
    "x_print_progress__mutmut_10": x_print_progress__mutmut_10,
    "x_print_progress__mutmut_11": x_print_progress__mutmut_11,
    "x_print_progress__mutmut_12": x_print_progress__mutmut_12,
    "x_print_progress__mutmut_13": x_print_progress__mutmut_13,
    "x_print_progress__mutmut_14": x_print_progress__mutmut_14,
    "x_print_progress__mutmut_15": x_print_progress__mutmut_15,
    "x_print_progress__mutmut_16": x_print_progress__mutmut_16,
    "x_print_progress__mutmut_17": x_print_progress__mutmut_17,
    "x_print_progress__mutmut_18": x_print_progress__mutmut_18,
    "x_print_progress__mutmut_19": x_print_progress__mutmut_19,
    "x_print_progress__mutmut_20": x_print_progress__mutmut_20,
    "x_print_progress__mutmut_21": x_print_progress__mutmut_21,
}


def print_progress(*args, **kwargs):
    result = _mutmut_trampoline(x_print_progress__mutmut_orig, x_print_progress__mutmut_mutants, args, kwargs)
    return result


print_progress.__signature__ = _mutmut_signature(x_print_progress__mutmut_orig)
x_print_progress__mutmut_orig.__name__ = "x_print_progress"


# <3 🧱🤝💻🪄
