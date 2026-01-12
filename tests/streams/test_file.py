#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#


from __future__ import annotations

from pathlib import Path
import tempfile

from provide.testkit import FoundationTestCase

from provide.foundation.streams.file import (
    close_log_streams,
    configure_file_logging,
    flush_log_streams,
)

#
# test_file.py
#
"""Tests for file stream functionality."""


class TestFileStreams(FoundationTestCase):
    def test_configure_file_logging_success(self) -> None:
        """Test successful file logging configuration."""
        with tempfile.TemporaryDirectory() as temp_dir:
            log_file = Path(temp_dir) / "test.log"
            configure_file_logging(str(log_file))

            # Clean up
            close_log_streams()

    def test_configure_file_logging_none(self) -> None:
        """Test file logging configuration with None path."""
        configure_file_logging(None)

        # Clean up
        close_log_streams()

    def test_flush_log_streams(self) -> None:
        """Test flushing log streams."""
        with tempfile.TemporaryDirectory() as temp_dir:
            log_file = Path(temp_dir) / "test.log"
            configure_file_logging(str(log_file))
            flush_log_streams()

            # Clean up
            close_log_streams()

    def test_configure_file_logging_invalid_path(self) -> None:
        """Test file logging with invalid path."""
        # Try to write to a directory that doesn't exist and can't be created
        invalid_path = "/invalid/nonexistent/path/test.log"
        configure_file_logging(invalid_path)  # Should not raise exception

        # Clean up
        close_log_streams()


# 🧱🏗️🔚
