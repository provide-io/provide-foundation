#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Performance benchmarks for caching improvements.

This module demonstrates the performance benefits of caching for
environment variable parsing, name normalization, and regex operations."""

from __future__ import annotations

from typing import Any

import pytest

# Check if pytest-benchmark is available
try:
    import pytest_benchmark  # noqa: F401

    HAS_BENCHMARK = True
except ImportError:
    HAS_BENCHMARK = False

pytestmark = pytest.mark.skipif(not HAS_BENCHMARK, reason="pytest-benchmark not installed")

from provide.testkit import FoundationTestCase

from provide.foundation.utils.environment import EnvPrefix
from provide.foundation.utils.environment.parsers import parse_duration, parse_size


class TestParserCachingBenchmarks(FoundationTestCase):
    """Benchmark parsing performance with caching."""

    def test_parse_duration_uncached_baseline(self, benchmark: Any) -> None:
        """Baseline: Parse duration without caching (first call).

        This measures the cost of regex compilation and matching
        on every call without any caching benefits.
        """

        def parse_multiple_durations() -> None:
            """Parse various duration formats."""
            # Clear cache before each benchmark run
            if hasattr(parse_duration, "cache_clear"):
                parse_duration.cache_clear()

            # Different inputs to avoid caching
            formats = ["30s", "5m", "2h", "1d", "1h30m", "2d3h", "10s", "45m", "3h15m", "7d"]
            for fmt in formats:
                parse_duration(fmt)

        benchmark(parse_multiple_durations)

    def test_parse_duration_cached(self, benchmark: Any) -> None:
        """Benchmark: Parse duration with caching (repeated calls).

        Expected: 10-50x faster than uncached baseline.
        """
        # Prime the cache with common formats
        common_formats = ["30s", "5m", "2h", "1d", "1h30m"]
        for fmt in common_formats:
            parse_duration(fmt)

        def parse_cached_durations() -> None:
            """Parse duration strings that are already cached."""
            for fmt in common_formats:
                parse_duration(fmt)

        benchmark(parse_cached_durations)

    def test_parse_size_cached(self, benchmark: Any) -> None:
        """Benchmark: Parse size with caching (repeated calls).

        Expected: 10-50x faster than uncached baseline.
        """
        # Prime the cache
        common_formats = ["1KB", "10MB", "1GB", "1.5GB", "500MB"]
        for fmt in common_formats:
            parse_size(fmt)

        def parse_cached_sizes() -> None:
            """Parse size strings that are already cached."""
            for fmt in common_formats:
                parse_size(fmt)

        benchmark(parse_cached_sizes)


class TestEnvPrefixCachingBenchmarks(FoundationTestCase):
    """Benchmark EnvPrefix name normalization with caching."""

    def test_env_prefix_cached(self, benchmark: Any) -> None:
        """Benchmark: Name normalization with caching (repeated access).

        Expected: 5-20x faster than uncached baseline.
        """
        env = EnvPrefix("APP")

        # Prime the cache
        common_names = ["database-url", "api.key", "debug_mode", "max-connections", "timeout.seconds"]
        for name in common_names:
            env._make_name(name)

        def normalize_cached_names() -> None:
            """Normalize names that are already cached."""
            for name in common_names:
                env._make_name(name)

        benchmark(normalize_cached_names)


class TestRealWorldScenarios(FoundationTestCase):
    """Benchmark real-world configuration loading scenarios."""

    def test_config_loading_cached(self, benchmark: Any) -> None:
        """Benchmark: Load configuration with caching (second load).

        Expected: 3-10x faster than uncached baseline.
        """
        # Prime all caches with first load
        parse_duration("30s")
        parse_size("10MB")
        parse_duration("5m")
        parse_size("1GB")
        parse_duration("1h")
        parse_size("500MB")

        env = EnvPrefix("APP")
        env._make_name("database-url")
        env._make_name("api.timeout")
        env._make_name("max-connections")

        def load_cached_config() -> None:
            """Load configuration with all values cached."""
            parse_duration("30s")
            parse_size("10MB")
            parse_duration("5m")
            parse_size("1GB")
            parse_duration("1h")
            parse_size("500MB")

            env._make_name("database-url")
            env._make_name("api.timeout")
            env._make_name("max-connections")

        benchmark(load_cached_config)

    def test_hot_path_repeated_parsing(self, benchmark: Any) -> None:
        """Benchmark: Hot path with repeated parsing (cached).

        Expected: 20-100x faster than uncached baseline.
        """
        # Prime cache
        parse_duration("30s")

        def hot_path() -> None:
            """Repeatedly parse the same value (simulates hot path)."""
            for _ in range(100):
                parse_duration("30s")

        benchmark(hot_path)


# 🧱🏗️🔚
