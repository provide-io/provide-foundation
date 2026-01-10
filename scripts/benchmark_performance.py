#!/usr/bin/env python3
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

"""Performance benchmark validation for provide-foundation."""

from __future__ import annotations

import time


def benchmark_logger_performance() -> None:
    """Benchmark logger initialization and basic operations."""
    from provide.foundation import logger

    # Benchmark: Quick initialization check
    start = time.perf_counter()
    logger.info("Benchmark started")
    init_time = time.perf_counter() - start

    # Performance threshold: 100ms for cold start
    if init_time > 0.1:
        print(f"Warning: Logger initialization took {init_time:.3f}s (threshold: 0.1s)")

    # Benchmark: Message throughput
    msg_count = 100
    start = time.perf_counter()
    for i in range(msg_count):
        logger.debug("Benchmark message", count=i)
    throughput_time = time.perf_counter() - start

    msgs_per_sec = msg_count / throughput_time if throughput_time > 0 else float("inf")
    print(f"Logger throughput: {msgs_per_sec:.0f} msgs/sec ({msg_count} messages in {throughput_time:.3f}s)")

    # Minimum threshold: 1000 msgs/sec
    if msgs_per_sec < 1000:
        print(f"Warning: Logger throughput below threshold ({msgs_per_sec:.0f} < 1000 msgs/sec)")


def main() -> None:
    """Run all benchmarks."""
    print("=" * 60)
    print("provide-foundation Performance Benchmarks")
    print("=" * 60)

    benchmark_logger_performance()

    print("=" * 60)
    print("Benchmarks completed successfully")
    print("=" * 60)


if __name__ == "__main__":
    main()
