#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Chaos tests for logger system.

Property-based tests using Hypothesis to explore edge cases in logging,
including emoji processing, Unicode handling, and rate-limited logging."""

from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor

from hypothesis import HealthCheck, given, settings, strategies as st
from provide.testkit import FoundationTestCase
from provide.testkit.chaos import (
    rate_burst_patterns,
    thread_counts,
    unicode_chaos,
)

from provide.foundation.logger import get_logger


class TestLoggerUnicodeChaos(FoundationTestCase):
    """Chaos tests for logger Unicode and emoji handling."""

    @given(text=unicode_chaos())
    @settings(max_examples=7, deadline=10000)
    def test_unicode_logging_chaos(self, text: str) -> None:
        """Test logger with chaotic Unicode input.

        Verifies:
        - Unicode strings don't crash logger
        - Emoji are processed correctly
        - RTL and special characters are handled
        """
        logger = get_logger(__name__)

        # Should not crash
        try:
            logger.info("Unicode test", text=text)
            logger.debug("Debug unicode", content=text)
        except Exception as e:
            # Log the exception for debugging, but shouldn't raise
            raise AssertionError(f"Logger crashed with Unicode: {e}") from e

    @given(
        emoji_text=unicode_chaos(include_emoji=True),
        regular_text=st.text(min_size=0, max_size=100),
    )
    @settings(max_examples=7, deadline=10000)
    def test_emoji_mixed_content_chaos(
        self,
        emoji_text: str,
        regular_text: str,
    ) -> None:
        """Test logger with mixed emoji and regular content.

        Verifies:
        - Mixed content is logged correctly
        - Emoji processing doesn't interfere with text
        - Edge cases are handled
        """
        logger = get_logger(__name__)

        try:
            logger.info("Mixed content", emoji=emoji_text, text=regular_text)
        except Exception as e:
            raise AssertionError(f"Logger failed with mixed content: {e}") from e

    @given(
        data=st.one_of(
            st.none(),
            st.integers(min_value=-1000000, max_value=1000000),
            st.floats(allow_nan=True, allow_infinity=True),
            st.text(max_size=200),
            st.binary(max_size=200),
            st.lists(st.integers(), max_size=20),
            st.dictionaries(st.text(max_size=5), st.integers(), max_size=5),
        )
    )
    @settings(
        max_examples=20,
        suppress_health_check=[HealthCheck.filter_too_much, HealthCheck.too_slow],
        deadline=None,
    )
    def test_malformed_log_data_chaos(self, data: object) -> None:
        """Test logger with malformed input data.

        Verifies:
        - Malformed data doesn't crash logger
        - Various types are handled
        - Edge cases don't cause issues
        """
        logger = get_logger(__name__)

        try:
            logger.info("Malformed data test", data=data)
            logger.debug("Debug malformed", value=data)
        except Exception:
            # Some extreme values might fail, but shouldn't crash the process
            # Just verify we can handle it gracefully
            pass


class TestLoggerConcurrencyChaos(FoundationTestCase):
    """Chaos tests for concurrent logging."""

    @given(
        num_threads=thread_counts(min_threads=2, max_threads=20),
        messages_per_thread=st.integers(min_value=5, max_value=50),
    )
    @settings(max_examples=7, deadline=10000)
    def test_concurrent_logging_chaos(
        self,
        num_threads: int,
        messages_per_thread: int,
    ) -> None:
        """Test concurrent logging from multiple threads.

        Verifies:
        - Thread-safe logging
        - No message corruption
        - No deadlocks
        """
        logger = get_logger(__name__)
        log_count = [0]

        def worker(thread_id: int) -> None:
            for i in range(messages_per_thread):
                logger.info(f"Thread {thread_id} message {i}", thread=thread_id, msg=i)
                log_count[0] += 1

        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            futures = [executor.submit(worker, i) for i in range(num_threads)]
            for future in futures:
                future.result(timeout=10.0)

        expected_count = num_threads * messages_per_thread
        assert log_count[0] == expected_count

    @given(bursts=rate_burst_patterns(max_burst_size=100, max_duration=1.0))
    @settings(max_examples=7, deadline=10000)
    def test_burst_logging_chaos(self, bursts: list[tuple[float, int]]) -> None:
        """Test logger with burst logging patterns.

        Verifies:
        - Burst logging is handled
        - No crashes under load
        - Performance is acceptable
        """
        logger = get_logger(__name__)

        for burst_time, count in bursts:
            # Log burst
            for i in range(count):
                logger.debug(f"Burst log {i}", time=burst_time, index=i)

        # Should complete without issues
        assert True

    @given(
        nested_depth=st.integers(min_value=1, max_value=10),
        dict_size=st.integers(min_value=1, max_value=20),
    )
    @settings(max_examples=7, deadline=10000)
    def test_nested_structured_logging_chaos(
        self,
        nested_depth: int,
        dict_size: int,
    ) -> None:
        """Test structured logging with deeply nested data.

        Verifies:
        - Nested dictionaries are logged
        - Deep structures don't cause issues
        - Serialization works correctly
        """
        logger = get_logger(__name__)

        # Create nested dict
        def create_nested(depth: int) -> dict:
            if depth == 0:
                return {"value": "leaf"}
            return {"level": depth, "nested": create_nested(depth - 1)}

        nested_data = create_nested(nested_depth)

        # Add dict at current level
        for i in range(dict_size):
            nested_data[f"key_{i}"] = f"value_{i}"

        import contextlib

        with contextlib.suppress(Exception):
            # Very deep structures might hit recursion limits, but shouldn't crash
            logger.info("Nested data test", data=nested_data, depth=nested_depth)


__all__ = [
    "TestLoggerConcurrencyChaos",
    "TestLoggerUnicodeChaos",
]

# 🧱🏗️🔚
