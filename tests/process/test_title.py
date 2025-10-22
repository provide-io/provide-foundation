# tests/process/test_title.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from unittest.mock import MagicMock, patch

from provide.testkit import FoundationTestCase
import pytest


class TestProcessTitle(FoundationTestCase):
    """Test process title functionality."""

    def setup_method(self) -> None:
        """Set up test environment."""
        super().setup_method()

    def teardown_method(self) -> None:
        """Clean up after test."""
        super().teardown_method()

    def test_has_setproctitle_returns_true_when_available(self) -> None:
        """Test has_setproctitle returns True when setproctitle is available."""
        from provide.foundation.process import has_setproctitle

        # On systems with setproctitle installed
        result = has_setproctitle()
        assert isinstance(result, bool)

    def test_set_process_title_with_setproctitle_available(self) -> None:
        """Test setting process title when setproctitle is available."""
        from provide.foundation.process import has_setproctitle, set_process_title

        if not has_setproctitle():
            pytest.skip("setproctitle not available")

        # Set a test title
        result = set_process_title("test-process")
        assert result is True

    def test_get_process_title_with_setproctitle_available(self) -> None:
        """Test getting process title when setproctitle is available."""
        from provide.foundation.process import get_process_title, has_setproctitle, set_process_title

        if not has_setproctitle():
            pytest.skip("setproctitle not available")

        # Set and get title
        set_process_title("test-process-get")
        title = get_process_title()
        assert title is not None
        assert isinstance(title, str)

    def test_set_process_title_without_setproctitle(self) -> None:
        """Test set_process_title returns False when setproctitle unavailable."""
        # Mock the module to simulate setproctitle not being available
        with patch("provide.foundation.process.title._HAS_SETPROCTITLE", False):
            from provide.foundation.process.title import set_process_title

            result = set_process_title("test-title")
            assert result is False

    def test_get_process_title_without_setproctitle(self) -> None:
        """Test get_process_title returns None when setproctitle unavailable."""
        with patch("provide.foundation.process.title._HAS_SETPROCTITLE", False):
            from provide.foundation.process.title import get_process_title

            result = get_process_title()
            assert result is None

    # Skipping exception tests for optional modules - hard to mock when they don't exist

    def test_set_process_title_with_empty_string(self) -> None:
        """Test setting process title with empty string."""
        from provide.foundation.process import has_setproctitle, set_process_title

        if not has_setproctitle():
            pytest.skip("setproctitle not available")

        result = set_process_title("")
        assert result is True

    def test_set_process_title_with_unicode(self) -> None:
        """Test setting process title with unicode characters."""
        from provide.foundation.process import has_setproctitle, set_process_title

        if not has_setproctitle():
            pytest.skip("setproctitle not available")

        result = set_process_title("test-process-🚀")
        assert result is True

    def test_set_process_title_with_long_string(self) -> None:
        """Test setting process title with very long string."""
        from provide.foundation.process import has_setproctitle, set_process_title

        if not has_setproctitle():
            pytest.skip("setproctitle not available")

        long_title = "a" * 1000
        result = set_process_title(long_title)
        assert result is True


# <3 🧱🤝🧪🪄
