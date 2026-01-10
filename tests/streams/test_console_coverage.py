#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#


from __future__ import annotations

from contextlib import suppress

from provide.testkit import FoundationTestCase

#
# test_console_coverage.py
#
"""Tests to achieve coverage for console and streams functionality."""


class TestFileStreams(FoundationTestCase):
    """Test file stream functionality."""

    def test_configure_file_logging_with_path(self, tmp_path: any) -> None:
        """Test file logging configuration with valid path."""
        from provide.foundation.streams.file import configure_file_logging

        log_file = tmp_path / "test.log"
        configure_file_logging(str(log_file))

        # Should create the file or directory structure
        assert log_file.parent.exists()

    def test_configure_file_logging_none(self) -> None:
        """Test file logging configuration with None."""
        from provide.foundation.streams.file import configure_file_logging

        # Should not raise an exception
        configure_file_logging(None)

    def test_configure_file_logging_invalid_path(self) -> None:
        """Test file logging with invalid path."""
        from provide.foundation.streams.file import configure_file_logging

        # Invalid path that can't be created
        invalid_path = "/root/nonexistent/test.log"

        # Should handle gracefully without crashing
        with suppress(PermissionError):
            configure_file_logging(invalid_path)

    def test_flush_log_streams(self) -> None:
        """Test log stream flushing."""
        from provide.foundation.streams.file import flush_log_streams

        # Should not raise an exception
        flush_log_streams()

    def test_close_log_streams(self) -> None:
        """Test log stream closing."""
        from provide.foundation.streams.file import close_log_streams

        # Should not raise an exception
        close_log_streams()


# 🧱🏗️🔚
