#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#


from __future__ import annotations

import os
import sys

from provide.testkit import FoundationTestCase
from provide.testkit.mocking import Mock, patch

from provide.foundation.streams.console import (
    get_console_stream,
    is_tty,
    supports_color,
    write_to_console,
)

#
# test_console.py
#
"""Tests for Foundation streams console module."""


class TestGetConsoleStream(FoundationTestCase):
    """Test get_console_stream function."""

    def test_returns_log_stream(self) -> None:
        """Test that get_console_stream returns the current log stream."""
        from provide.foundation.streams.core import get_log_stream

        # Should return the same as get_log_stream
        console_stream = get_console_stream()
        log_stream = get_log_stream()

        assert console_stream is log_stream


class TestIsTTY(FoundationTestCase):
    """Test is_tty function."""

    def test_is_tty_with_tty_stream(self) -> None:
        """Test is_tty with a TTY stream."""
        from provide.foundation.streams.core import set_log_stream_for_testing

        # Create mock TTY stream
        mock_stream = Mock()
        mock_stream.isatty.return_value = True

        set_log_stream_for_testing(mock_stream)

        try:
            assert is_tty() is True
            mock_stream.isatty.assert_called_once()
        finally:
            set_log_stream_for_testing(None)

    def test_is_tty_with_non_tty_stream(self) -> None:
        """Test is_tty with a non-TTY stream."""
        from provide.foundation.streams.core import set_log_stream_for_testing

        # Create mock non-TTY stream
        mock_stream = Mock()
        mock_stream.isatty.return_value = False

        set_log_stream_for_testing(mock_stream)

        try:
            assert is_tty() is False
            mock_stream.isatty.assert_called_once()
        finally:
            set_log_stream_for_testing(None)

    def test_is_tty_with_stream_without_isatty(self) -> None:
        """Test is_tty with a stream that doesn't have isatty method."""
        from provide.foundation.streams.core import set_log_stream_for_testing

        # Create stream without isatty method
        mock_stream = Mock()
        del mock_stream.isatty  # Remove isatty attribute

        set_log_stream_for_testing(mock_stream)

        try:
            assert is_tty() is False
        finally:
            set_log_stream_for_testing(None)


class TestSupportsColor(FoundationTestCase):
    """Test supports_color function."""

    def setup_method(self) -> None:
        """Clean up environment variables before each test."""
        from provide.foundation.streams.config import reset_stream_config

        # Store original values
        self.original_no_color = os.environ.get("NO_COLOR")
        self.original_force_color = os.environ.get("FORCE_COLOR")

        # Clean up
        os.environ.pop("NO_COLOR", None)
        os.environ.pop("FORCE_COLOR", None)

        # Reset cached stream config
        reset_stream_config()

    def teardown_method(self) -> None:
        """Restore environment variables after each test."""
        from provide.foundation.streams.config import reset_stream_config

        # Restore original values
        if self.original_no_color is not None:
            os.environ["NO_COLOR"] = self.original_no_color
        else:
            os.environ.pop("NO_COLOR", None)

        if self.original_force_color is not None:
            os.environ["FORCE_COLOR"] = self.original_force_color
        else:
            os.environ.pop("FORCE_COLOR", None)

        # Reset stream config to pick up restored environment
        reset_stream_config()

    def test_no_color_environment_disables_color(self) -> None:
        """Test that NO_COLOR environment variable disables color."""
        from provide.foundation.streams.config import reset_stream_config

        os.environ["NO_COLOR"] = "1"
        reset_stream_config()  # Reset to pick up new env var

        assert supports_color() is False

    def test_force_color_environment_enables_color(self) -> None:
        """Test that FORCE_COLOR environment variable enables color."""
        from provide.foundation.streams.config import reset_stream_config

        os.environ["FORCE_COLOR"] = "1"
        reset_stream_config()  # Reset to pick up new env var

        assert supports_color() is True

    def test_force_color_overrides_tty_check(self) -> None:
        """Test that FORCE_COLOR works even with non-TTY."""
        from provide.foundation.streams.config import reset_stream_config
        from provide.foundation.streams.core import set_log_stream_for_testing

        os.environ["FORCE_COLOR"] = "1"
        reset_stream_config()  # Reset to pick up new env var

        # Create non-TTY stream
        mock_stream = Mock()
        mock_stream.isatty.return_value = False

        set_log_stream_for_testing(mock_stream)

        try:
            assert supports_color() is True
        finally:
            set_log_stream_for_testing(None)

    def test_no_color_overrides_force_color(self) -> None:
        """Test that NO_COLOR takes precedence over FORCE_COLOR."""
        os.environ["NO_COLOR"] = "1"
        os.environ["FORCE_COLOR"] = "1"

        assert supports_color() is False

    def test_supports_color_falls_back_to_tty_check(self) -> None:
        """Test that supports_color falls back to TTY check when no env vars set."""
        from provide.foundation.streams.core import set_log_stream_for_testing

        # Create TTY stream
        mock_tty_stream = Mock()
        mock_tty_stream.isatty.return_value = True

        set_log_stream_for_testing(mock_tty_stream)

        try:
            assert supports_color() is True
        finally:
            set_log_stream_for_testing(None)

        # Create non-TTY stream
        mock_non_tty_stream = Mock()
        mock_non_tty_stream.isatty.return_value = False

        set_log_stream_for_testing(mock_non_tty_stream)

        try:
            assert supports_color() is False
        finally:
            set_log_stream_for_testing(None)


class TestWriteToConsole(FoundationTestCase):
    """Test write_to_console function."""

    def test_write_to_default_console_stream(self) -> None:
        """Test writing to default console stream."""
        from provide.foundation.streams.core import set_log_stream_for_testing

        mock_stream = Mock()
        set_log_stream_for_testing(mock_stream)

        try:
            write_to_console("test message")

            mock_stream.write.assert_called_once_with("test message")
            mock_stream.flush.assert_called_once()
        finally:
            set_log_stream_for_testing(None)

    def test_write_to_specific_stream(self) -> None:
        """Test writing to a specific stream."""
        mock_stream = Mock()

        write_to_console("test message", stream=mock_stream)

        mock_stream.write.assert_called_once_with("test message")
        mock_stream.flush.assert_called_once()

    def test_write_to_console_with_exception_fallback(self) -> None:
        """Test write_to_console with exception falling back to stderr."""
        from provide.foundation.streams.core import set_log_stream_for_testing

        # Create stream that raises exception on write
        mock_stream = Mock()
        mock_stream.write.side_effect = Exception("Write failed")

        set_log_stream_for_testing(mock_stream)

        with (
            patch.object(sys.stderr, "write") as mock_stderr_write,
            patch.object(sys.stderr, "flush") as mock_stderr_flush,
            patch("provide.foundation.hub.foundation.get_foundation_logger") as mock_get_logger,
        ):
            # Ensure logger is available for debug logging
            mock_logger = Mock()
            mock_get_logger.return_value = mock_logger

            try:
                # Call write_to_console and expect it to handle the exception gracefully
                write_to_console("test message")

                # Should have tried the original stream
                mock_stream.write.assert_called_once_with("test message")

                # Logger should have been called for debug message
                mock_logger.debug.assert_called_once()

                # Should have fallen back to stderr for final message
                mock_stderr_write.assert_called_once_with("test message")
                mock_stderr_flush.assert_called_once()
            finally:
                set_log_stream_for_testing(None)

    def test_write_to_console_with_flush_exception_fallback(self) -> None:
        """Test write_to_console with flush exception falling back to stderr."""
        from provide.foundation.streams.core import set_log_stream_for_testing

        # Create stream that raises exception on flush
        mock_stream = Mock()
        mock_stream.flush.side_effect = Exception("Flush failed")

        set_log_stream_for_testing(mock_stream)

        with (
            patch.object(sys.stderr, "write") as mock_stderr_write,
            patch.object(sys.stderr, "flush") as mock_stderr_flush,
            patch("provide.foundation.hub.foundation.get_foundation_logger") as mock_get_logger,
        ):
            # Ensure logger is available for debug logging
            mock_logger = Mock()
            mock_get_logger.return_value = mock_logger

            try:
                # Call write_to_console and expect it to handle the exception gracefully
                write_to_console("test message")

                # Should have written to original stream then failed on flush
                mock_stream.write.assert_called_once_with("test message")
                mock_stream.flush.assert_called_once()

                # Logger should have been called for debug message
                mock_logger.debug.assert_called_once()

                # Should have fallen back to stderr for final message
                mock_stderr_write.assert_called_once_with("test message")
                mock_stderr_flush.assert_called_once()
            finally:
                set_log_stream_for_testing(None)

    def test_write_to_specific_stream_with_exception_fallback(self) -> None:
        """Test write_to_console with specific stream that fails."""
        mock_failing_stream = Mock()
        mock_failing_stream.write.side_effect = Exception("Write failed")

        with (
            patch.object(sys.stderr, "write") as mock_stderr_write,
            patch.object(sys.stderr, "flush") as mock_stderr_flush,
            patch("provide.foundation.hub.foundation.get_foundation_logger") as mock_get_logger,
        ):
            # Ensure logger is available for debug logging
            mock_logger = Mock()
            mock_get_logger.return_value = mock_logger

            write_to_console("test message", stream=mock_failing_stream)

            # Should have tried the specific stream
            mock_failing_stream.write.assert_called_once_with("test message")

            # Logger should have been called for debug message
            mock_logger.debug.assert_called_once()

            # Should have fallen back to stderr for final message
            mock_stderr_write.assert_called_once_with("test message")
            mock_stderr_flush.assert_called_once()

    def test_write_to_console_with_logging_failure_fallback(self) -> None:
        """Test write_to_console when both stream and Foundation logger fail."""
        from provide.testkit.mocking import patch

        from provide.foundation.streams.core import set_log_stream_for_testing

        # Create stream that raises exception on write
        mock_stream = Mock()
        mock_stream.write.side_effect = Exception("Write failed")

        set_log_stream_for_testing(mock_stream)

        with (
            patch.object(sys.stderr, "write") as mock_stderr_write,
            patch.object(sys.stderr, "flush") as mock_stderr_flush,
            patch("provide.foundation.hub.foundation.get_foundation_logger") as mock_logger,
        ):
            # Make the Foundation logger also fail
            mock_logger.side_effect = Exception("Logger failed")

            try:
                # Should handle both failures gracefully and log to stderr directly
                write_to_console("test message")

                # Should have tried the original stream
                mock_stream.write.assert_called_once_with("test message")

                # Should have fallen back to stderr for both the message and debug info
                assert mock_stderr_write.call_count >= 2  # Main message + debug info
                assert mock_stderr_flush.call_count >= 2

                # Check that stderr received both the main message and debug info
                stderr_calls = [str(call) for call in mock_stderr_write.call_args_list]
                assert any("test message" in call for call in stderr_calls), (
                    f"Main message not found in {stderr_calls}"
                )
                assert any("Console write failed" in call for call in stderr_calls), (
                    f"Debug info not found in {stderr_calls}"
                )
            finally:
                set_log_stream_for_testing(None)


class TestConsoleIntegration(FoundationTestCase):
    """Test integration scenarios for console functions."""

    def setup_method(self) -> None:
        """Ensure color environment variables are cleared for tests."""
        self.original_no_color = os.environ.get("NO_COLOR")
        self.original_force_color = os.environ.get("FORCE_COLOR")
        os.environ.pop("NO_COLOR", None)
        os.environ.pop("FORCE_COLOR", None)

    def teardown_method(self) -> None:
        """Restore color environment variables after tests."""
        if self.original_no_color is not None:
            os.environ["NO_COLOR"] = self.original_no_color
        else:
            os.environ.pop("NO_COLOR", None)

        if self.original_force_color is not None:
            os.environ["FORCE_COLOR"] = self.original_force_color
        else:
            os.environ.pop("FORCE_COLOR", None)

    def test_write_to_console_respects_log_stream_changes(self) -> None:
        """Test that write_to_console respects log stream changes."""
        from provide.foundation.streams.core import set_log_stream_for_testing

        # Create two different streams
        stream1 = Mock()
        stream2 = Mock()

        # Write with first stream
        set_log_stream_for_testing(stream1)
        write_to_console("message 1")

        # Change stream and write again
        set_log_stream_for_testing(stream2)
        write_to_console("message 2")

        try:
            # Verify correct streams were used
            stream1.write.assert_called_once_with("message 1")
            stream2.write.assert_called_once_with("message 2")
        finally:
            set_log_stream_for_testing(None)

    def test_color_support_and_tty_integration(self) -> None:
        """Test integration between color support and TTY detection."""
        from provide.foundation.streams.core import set_log_stream_for_testing

        # Create TTY stream
        tty_stream = Mock()
        tty_stream.isatty.return_value = True

        set_log_stream_for_testing(tty_stream)

        try:
            # Both should return True for TTY
            assert is_tty() is True
            assert supports_color() is True
        finally:
            set_log_stream_for_testing(None)

        # Create non-TTY stream
        non_tty_stream = Mock()
        non_tty_stream.isatty.return_value = False

        set_log_stream_for_testing(non_tty_stream)

        try:
            # Both should return False for non-TTY
            assert is_tty() is False
            assert supports_color() is False
        finally:
            set_log_stream_for_testing(None)


# 🧱🏗️🔚
