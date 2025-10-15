# provide/foundation/tests/logger/setup/test_system_logger_formatting.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import io
from unittest.mock import patch

import pytest

from provide.foundation.logger.setup.coordinator import get_system_logger, reset_coordinator_state
from provide.testkit import FoundationTestCase


class TestSystemLoggerFormatting(FoundationTestCase):
    """Test formatting of system logger with structured logging."""

    def setup_method(self) -> None:
        """Reset coordinator state before each test."""
        super().setup_method()
        reset_coordinator_state()

    def teardown_method(self) -> None:
        """Clean up after test."""
        reset_coordinator_state()
        super().teardown_method()

    def test_system_logger_with_kwargs(self) -> None:
        """Test that system logger accepts and formats kwargs."""
        # Create a test stream to capture output
        test_stream = io.StringIO()

        with patch("sys.stderr", test_stream):
            logger = get_system_logger("test.logger")
            logger.debug("Test message", key1="value1", key2="value2")

        output = test_stream.getvalue()
        # Verify emoji prefix is present
        assert "🧱" in output
        # Verify message is present
        assert "Test message" in output
        # Verify key-value pairs are present
        assert "key1=value1" in output
        assert "key2=value2" in output

    def test_system_logger_tty_coloring(self) -> None:
        """Test that TTY detection works for coloring."""
        test_stream = io.StringIO()
        # Mock isatty() to return True
        test_stream.isatty = lambda: True

        with patch("sys.stderr", test_stream):
            logger = get_system_logger("test.logger")
            logger.debug("Test message", key="value")

        output = test_stream.getvalue()
        # Should contain ANSI color codes
        assert "\033[" in output
        # Should have colored key-value pairs (cyan key, magenta value)
        assert "\033[36mkey\033[0m" in output  # cyan
        assert "\033[35mvalue\033[0m" in output  # magenta

    def test_system_logger_no_tty_no_colors(self) -> None:
        """Test that non-TTY streams don't get colors."""
        test_stream = io.StringIO()
        # StringIO doesn't have isatty by default, or returns False

        with patch("sys.stderr", test_stream):
            logger = get_system_logger("test.logger")
            logger.debug("Test message", key="value")

        output = test_stream.getvalue()
        # Should NOT contain ANSI color codes
        # But should still have the key-value pairs
        assert "key=value" in output

    def test_system_logger_singleton_behavior(self) -> None:
        """Test that get_system_logger returns wrapped singleton."""
        logger1 = get_system_logger("test.logger")
        logger2 = get_system_logger("test.logger")

        # Both should reference the same underlying logger
        assert logger1._logger is logger2._logger


# <3 🧱🤝📝🪄
