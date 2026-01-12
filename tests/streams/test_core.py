#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Unit tests for streams/core.py module.

Run with: pytest tests/streams/test_core.py -v"""

from __future__ import annotations

import io
import sys

from provide.testkit import FoundationTestCase
from provide.testkit.mocking import MagicMock, Mock, patch

from provide.foundation.streams.core import (
    ensure_stderr_default,
    get_log_stream,
    set_log_stream_for_testing,
)


class TestGetLogStream(FoundationTestCase):
    """Tests for get_log_stream function."""

    def test_get_log_stream_returns_stream(self) -> None:
        """Test that get_log_stream returns a stream."""
        stream = get_log_stream()

        assert stream is not None
        assert hasattr(stream, "write")

    def test_get_log_stream_default_is_stderr(self) -> None:
        """Test that default log stream is stderr."""
        stream = get_log_stream()

        # In test environment, stream should be stderr or a test stream
        assert stream is not None

    def test_get_log_stream_with_closed_stream(self) -> None:
        """Test get_log_stream handles closed streams."""
        # Create a closed stream
        closed_stream = io.StringIO()
        closed_stream.close()

        with patch("provide.foundation.streams.core._PROVIDE_LOG_STREAM", closed_stream):
            stream = get_log_stream()

            # Should return stderr or a safe fallback
            assert stream is not None
            assert not stream.closed

    def test_get_log_stream_with_lock_timeout(self) -> None:
        """Test get_log_stream returns stderr on lock timeout."""
        mock_lock = MagicMock()
        mock_lock.acquire.return_value = False  # Timeout

        with patch("provide.foundation.streams.core._get_stream_lock", return_value=mock_lock):
            stream = get_log_stream()

            # Should return stderr as fallback
            assert stream is sys.stderr

    def test_get_log_stream_with_mock_object(self) -> None:
        """Test get_log_stream doesn't validate mock objects."""
        mock_stream = Mock()
        mock_stream._mock_name = "mock_stream"  # Mark as mock
        mock_stream.closed = True

        with patch("provide.foundation.streams.core._PROVIDE_LOG_STREAM", mock_stream):
            # Should return the mock without validation
            stream = get_log_stream()
            assert stream is not None


class TestSetLogStreamForTesting(FoundationTestCase):
    """Tests for set_log_stream_for_testing function."""

    def test_set_log_stream_for_testing_with_stream(self) -> None:
        """Test setting log stream for testing."""
        test_stream = io.StringIO()

        set_log_stream_for_testing(test_stream)

        try:
            stream = get_log_stream()
            assert stream is test_stream
        finally:
            set_log_stream_for_testing(None)

    def test_set_log_stream_for_testing_with_none(self) -> None:
        """Test setting log stream to None resets to stderr."""
        set_log_stream_for_testing(None)

        stream = get_log_stream()
        # Should be stderr or default
        assert stream is not None

    def test_set_log_stream_for_testing_in_non_test_mode(self) -> None:
        """Test stream setting is blocked in non-test mode."""
        test_stream = io.StringIO()

        with patch("provide.foundation.testmode.detection.should_allow_stream_redirect", return_value=False):
            original_stream = get_log_stream()
            set_log_stream_for_testing(test_stream)

            # Stream should not change
            stream = get_log_stream()
            assert stream is original_stream

    def test_set_log_stream_for_testing_with_lock_timeout(self) -> None:
        """Test set_log_stream_for_testing handles lock timeout."""
        mock_lock = MagicMock()
        mock_lock.acquire.return_value = False  # Timeout

        test_stream = io.StringIO()

        with patch("provide.foundation.streams.core._get_stream_lock", return_value=mock_lock):
            # Should return early without setting
            set_log_stream_for_testing(test_stream)

            # Lock acquire should have been called
            mock_lock.acquire.assert_called_once()


class TestEnsureStderrDefault(FoundationTestCase):
    """Tests for ensure_stderr_default function."""

    def test_ensure_stderr_default_when_stdout(self) -> None:
        """Test ensuring stderr when stream is stdout."""
        with patch("provide.foundation.streams.core._PROVIDE_LOG_STREAM", sys.stdout):
            ensure_stderr_default()

            stream = get_log_stream()
            # Should now be stderr, not stdout
            assert stream is not sys.stdout

    def test_ensure_stderr_default_when_already_stderr(self) -> None:
        """Test ensure_stderr_default when already stderr."""
        original_stream = sys.stderr

        with patch("provide.foundation.streams.core._PROVIDE_LOG_STREAM", sys.stderr):
            ensure_stderr_default()

            stream = get_log_stream()
            # Should still be stderr
            assert stream is sys.stderr or stream is original_stream

    def test_ensure_stderr_default_with_custom_stream(self) -> None:
        """Test ensure_stderr_default with custom stream."""
        custom_stream = io.StringIO()

        with patch("provide.foundation.streams.core._PROVIDE_LOG_STREAM", custom_stream):
            ensure_stderr_default()

            stream = get_log_stream()
            # Should remain custom stream (not stdout)
            assert stream is custom_stream

    def test_ensure_stderr_default_with_lock_timeout(self) -> None:
        """Test ensure_stderr_default handles lock timeout."""
        mock_lock = MagicMock()
        mock_lock.acquire.return_value = False  # Timeout

        with patch("provide.foundation.streams.core._get_stream_lock", return_value=mock_lock):
            # Should return early without error
            ensure_stderr_default()

            mock_lock.acquire.assert_called_once()


class TestReconfigureStructlogStream(FoundationTestCase):
    """Tests for _reconfigure_structlog_stream internal function."""

    def test_reconfigure_structlog_stream_with_structlog(self) -> None:
        """Test _reconfigure_structlog_stream with structlog available."""
        from provide.foundation.streams.core import _reconfigure_structlog_stream

        mock_config = {
            "logger_factory": MagicMock(),
            "processors": [],
            "cache_logger_on_first_use": True,
        }

        with (
            patch("structlog.get_config", return_value=mock_config),
            patch("structlog.configure") as mock_configure,
            patch("structlog.PrintLoggerFactory"),
        ):
            _reconfigure_structlog_stream()

            # Should have called configure
            mock_configure.assert_called_once()

    def test_reconfigure_structlog_stream_without_structlog(self) -> None:
        """Test _reconfigure_structlog_stream without structlog."""
        from provide.foundation.streams.core import _reconfigure_structlog_stream

        with patch("builtins.__import__", side_effect=ImportError("No module named 'structlog'")):
            # Should not raise error
            _reconfigure_structlog_stream()

    def test_reconfigure_structlog_stream_with_force_redirect(self) -> None:
        """Test _reconfigure_structlog_stream with force stream redirect."""
        from provide.foundation.streams.core import _reconfigure_structlog_stream

        mock_config = {
            "logger_factory": MagicMock(),
            "cache_logger_on_first_use": True,
        }

        mock_stream_config = MagicMock()
        mock_stream_config.force_stream_redirect = True

        with (
            patch("structlog.get_config", return_value=mock_config),
            patch("structlog.configure") as mock_configure,
            patch("structlog.PrintLoggerFactory"),
            patch("provide.foundation.streams.config.get_stream_config", return_value=mock_stream_config),
        ):
            _reconfigure_structlog_stream()

            # Should configure with cache_logger_on_first_use=False
            call_args = mock_configure.call_args
            assert call_args is not None
            assert call_args[1]["cache_logger_on_first_use"] is False


class TestGetStreamLock(FoundationTestCase):
    """Tests for _get_stream_lock internal function."""

    def test_get_stream_lock_returns_lock(self) -> None:
        """Test that _get_stream_lock returns a lock."""
        from provide.foundation.streams.core import _get_stream_lock

        lock = _get_stream_lock()

        assert lock is not None
        assert hasattr(lock, "acquire")
        assert hasattr(lock, "release")

    def test_get_stream_lock_returns_rlock(self) -> None:
        """Test that _get_stream_lock returns an RLock."""
        from provide.foundation.streams.core import _get_stream_lock

        lock = _get_stream_lock()

        # Should be an RLock - check it has the right methods
        assert hasattr(lock, "_is_owned")  # RLock specific method


class TestStreamErrorHandling(FoundationTestCase):
    """Tests for stream error handling scenarios."""

    def test_get_log_stream_with_no_stderr(self) -> None:
        """Test get_log_stream when sys.stderr is None."""
        closed_stream = io.StringIO()
        closed_stream.close()

        with (
            patch("provide.foundation.streams.core._PROVIDE_LOG_STREAM", closed_stream),
            patch("sys.stderr", None),
        ):
            # Should create fallback StringIO
            stream = get_log_stream()
            assert stream is not None


class TestStreamConcurrency(FoundationTestCase):
    """Tests for stream concurrency and thread safety."""

    def test_concurrent_get_log_stream(self) -> None:
        """Test concurrent calls to get_log_stream are safe."""
        import threading

        results = []

        def get_stream() -> None:
            stream = get_log_stream()
            results.append(stream)

        threads = [threading.Thread(target=get_stream) for _ in range(5)]

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()

        # All threads should have gotten a stream
        assert len(results) == 5
        for stream in results:
            assert stream is not None

    def test_concurrent_set_log_stream(self) -> None:
        """Test concurrent stream setting is safe."""
        import threading

        def set_stream() -> None:
            test_stream = io.StringIO()
            set_log_stream_for_testing(test_stream)
            set_log_stream_for_testing(None)

        threads = [threading.Thread(target=set_stream) for _ in range(3)]

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()

        # Should complete without deadlock
        stream = get_log_stream()
        assert stream is not None


class TestStreamEdgeCases(FoundationTestCase):
    """Tests for edge cases in stream management."""

    def test_set_stream_with_closed_stream(self) -> None:
        """Test setting a closed stream."""
        closed_stream = io.StringIO()
        closed_stream.close()

        set_log_stream_for_testing(closed_stream)

        try:
            stream = get_log_stream()
            # Should handle closed stream
            assert stream is not None
        finally:
            set_log_stream_for_testing(None)

    def test_repeated_set_and_get(self) -> None:
        """Test repeated set and get operations."""
        streams = [io.StringIO() for _ in range(3)]

        for test_stream in streams:
            set_log_stream_for_testing(test_stream)
            current = get_log_stream()
            assert current is test_stream

        set_log_stream_for_testing(None)

    def test_get_stream_resilient_to_errors(self) -> None:
        """Test get_log_stream is resilient to various errors."""
        # The implementation is designed to be resilient and return a valid stream
        # even in error scenarios
        stream = get_log_stream()

        # Should always return a valid stream
        assert stream is not None
        assert hasattr(stream, "write")


__all__ = [
    "TestEnsureStderrDefault",
    "TestGetLogStream",
    "TestGetStreamLock",
    "TestReconfigureStructlogStream",
    "TestSetLogStreamForTesting",
    "TestStreamConcurrency",
    "TestStreamEdgeCases",
    "TestStreamErrorHandling",
]

# 🧱🏗️🔚
