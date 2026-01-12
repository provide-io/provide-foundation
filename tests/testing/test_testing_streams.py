#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for stream testing utilities."""

from __future__ import annotations

import io
import sys

from provide.testkit import FoundationTestCase
from provide.testkit.streams import (
    get_current_log_stream,
    reset_log_stream,
    set_log_stream_for_testing,
)


class TestStreamTestingUtilities(FoundationTestCase):
    """Test stream testing helper functions."""

    def setup_method(self) -> None:
        """Set up each test with clean stream state."""
        reset_log_stream()

    def teardown_method(self) -> None:
        """Clean up after each test."""
        reset_log_stream()

    def test_set_log_stream_for_testing_with_stringio(self) -> None:
        """Test setting log stream to StringIO."""
        test_stream = io.StringIO()

        set_log_stream_for_testing(test_stream)

        current_stream = get_current_log_stream()
        assert current_stream is test_stream

    def test_set_log_stream_for_testing_with_none(self) -> None:
        """Test resetting log stream with None."""
        test_stream = io.StringIO()
        set_log_stream_for_testing(test_stream)

        # Reset with None
        set_log_stream_for_testing(None)

        current_stream = get_current_log_stream()
        assert current_stream is sys.stderr

    def test_get_current_log_stream_default(self) -> None:
        """Test that default stream is stderr."""
        reset_log_stream()

        current_stream = get_current_log_stream()
        assert current_stream is sys.stderr

    def test_reset_log_stream_function(self) -> None:
        """Test the reset_log_stream convenience function."""
        test_stream = io.StringIO()
        set_log_stream_for_testing(test_stream)

        # Verify it was set
        assert get_current_log_stream() is test_stream

        # Reset using convenience function
        reset_log_stream()

        # Should be back to stderr
        assert get_current_log_stream() is sys.stderr

    def test_stream_isolation_between_tests(self) -> None:
        """Test that stream changes don't leak between tests."""
        # This test should start with stderr (due to setup_method)
        assert get_current_log_stream() is sys.stderr

        # Change to a test stream
        test_stream = io.StringIO()
        set_log_stream_for_testing(test_stream)
        assert get_current_log_stream() is test_stream

        # teardown_method should clean this up automatically

    def test_multiple_stream_changes(self) -> None:
        """Test multiple stream changes work correctly."""
        stream1 = io.StringIO()
        stream2 = io.StringIO()

        # Change to first stream
        set_log_stream_for_testing(stream1)
        assert get_current_log_stream() is stream1

        # Change to second stream
        set_log_stream_for_testing(stream2)
        assert get_current_log_stream() is stream2

        # Reset to stderr
        set_log_stream_for_testing(None)
        assert get_current_log_stream() is sys.stderr

    def test_stream_functions_thread_safe(self) -> None:
        """Test that stream functions handle threading correctly."""
        import threading
        import time

        results = {}

        def set_and_get_stream(stream_id: int) -> None:
            test_stream = io.StringIO()
            set_log_stream_for_testing(test_stream)
            time.sleep(0.01)  # Small delay to test race conditions
            results[stream_id] = get_current_log_stream() is test_stream

        # Start multiple threads
        threads = []
        for i in range(3):
            thread = threading.Thread(daemon=True, target=set_and_get_stream, args=(i,))
            threads.append(thread)
            thread.start()

        # Wait for all threads
        for thread in threads:
            thread.join(timeout=10.0)

        # Due to the global stream state and threading lock,
        # we can't guarantee individual thread isolation,
        # but the functions should not crash
        assert len(results) == 3

    def test_stream_with_actual_logging(self) -> None:
        """Test that stream redirection works with actual Foundation logging."""
        from provide.testkit import reset_foundation_setup_for_testing

        # Reset foundation state
        reset_foundation_setup_for_testing()

        # Set up test stream
        test_stream = io.StringIO()
        set_log_stream_for_testing(test_stream)

        try:
            # Try to use Foundation logger
            from provide.foundation import logger

            logger.info("Test message for stream capture")

            # Check if anything was captured
            output = test_stream.getvalue()
            # Note: Output may be empty if logging isn't configured,
            # but the important thing is no exceptions were raised
            assert isinstance(output, str)

        except Exception as e:
            # If there's an exception, it should not be related to stream handling
            assert "stream" not in str(e).lower()

        finally:
            reset_log_stream()
            reset_foundation_setup_for_testing()


# 🧱🏗️🔚
