#!/usr/bin/env python3
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

"""Memray stress test: Config parsing.

Exercises parse_duration(), parse_size(), EnvPrefix._make_name(),
and Foundation initialize/teardown cycles.
"""

from __future__ import annotations

import io
import sys


def warmup() -> None:
    """Warmup phase to separate import-time allocations."""
    from provide.foundation.utils.environment import EnvPrefix
    from provide.foundation.utils.environment.parsers import parse_duration, parse_size

    parse_duration("30s")
    parse_size("10MB")
    env = EnvPrefix("WARMUP")
    env._make_name("test-key")


def run_stress() -> None:
    """Run the config stress test."""
    from provide.foundation import LoggingConfig, TelemetryConfig, get_hub
    from provide.foundation.utils.environment import EnvPrefix
    from provide.foundation.utils.environment.parsers import parse_duration, parse_size
    from provide.testkit import reset_foundation_setup_for_testing, set_log_stream_for_testing

    # Phase 1: parse_duration() — 10K calls with mixed cached/uncached inputs
    duration_count = 10_000
    duration_formats = ["30s", "5m", "2h", "1d", "1h30m", "2d3h", "10s", "45m", "3h15m", "7d"]

    # Clear cache to start fresh
    if hasattr(parse_duration, "cache_clear"):
        parse_duration.cache_clear()

    for i in range(duration_count):
        fmt = duration_formats[i % len(duration_formats)]
        parse_duration(fmt)

    # Phase 2: parse_size() — 10K calls with mixed cached/uncached inputs
    size_count = 10_000
    size_formats = ["1024", "1KB", "10MB", "1GB", "1.5GB", "500MB", "256KB", "2TB", "100B", "50GB"]

    if hasattr(parse_size, "cache_clear"):
        parse_size.cache_clear()

    for i in range(size_count):
        fmt = size_formats[i % len(size_formats)]
        parse_size(fmt)

    # Phase 3: EnvPrefix._make_name() — 10K calls
    name_count = 10_000
    env = EnvPrefix("STRESS_TEST")
    name_formats = [
        "database-url",
        "api.key",
        "debug_mode",
        "max-connections",
        "timeout.seconds",
        "cache.ttl",
        "log-level",
        "worker.count",
        "retry-delay",
        "batch.size",
    ]

    for i in range(name_count):
        name = name_formats[i % len(name_formats)]
        env._make_name(name)

    # Phase 4: Foundation initialize/teardown — 500 cycles
    init_count = 500
    stream = io.StringIO()
    set_log_stream_for_testing(stream)

    for i in range(init_count):
        config = TelemetryConfig(
            logging=LoggingConfig(
                default_level="INFO",
                console_formatter="key_value",
            ),
        )
        hub = get_hub()
        hub.initialize_foundation(config, force=True)
        reset_foundation_setup_for_testing()

    set_log_stream_for_testing(None)

    print(
        f"Config stress complete: {duration_count} duration parses, "
        f"{size_count} size parses, {name_count} name normalizations, "
        f"{init_count} init/teardown cycles",
        file=sys.stderr,
    )


if __name__ == "__main__":
    warmup()
    run_stress()
