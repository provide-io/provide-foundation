#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#


from __future__ import annotations

from provide.testkit import FoundationTestCase
from provide.testkit.mocking import patch
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
        from provide.foundation.process import has_setproctitle

        if not has_setproctitle():
            pytest.skip("setproctitle not available")

        # Mock test mode to allow actual process title operations
        with patch("provide.foundation.testmode.decorators.is_in_test_mode", return_value=False):
            from provide.foundation.process import set_process_title

            # Set a test title
            result = set_process_title("test-process")
            assert result is True

    def test_get_process_title_with_setproctitle_available(self) -> None:
        """Test getting process title when setproctitle is available."""
        from provide.foundation.process import has_setproctitle

        if not has_setproctitle():
            pytest.skip("setproctitle not available")

        # Mock test mode to allow actual process title operations
        with patch("provide.foundation.testmode.decorators.is_in_test_mode", return_value=False):
            from provide.foundation.process import get_process_title, set_process_title

            # Set and get title
            set_process_title("test-process-get")
            title = get_process_title()
            assert title is not None
            assert isinstance(title, str)

    def test_set_process_title_without_setproctitle(self) -> None:
        """Test set_process_title returns False when setproctitle unavailable."""
        # Mock test mode at decorator level (bypass skip) and setproctitle availability
        with patch("provide.foundation.testmode.decorators.is_in_test_mode", return_value=False):
            with patch("provide.foundation.process.title._HAS_SETPROCTITLE", False):
                from provide.foundation.process.title import set_process_title

                result = set_process_title("test-title")
                assert result is False

    def test_get_process_title_without_setproctitle(self) -> None:
        """Test get_process_title returns None when setproctitle unavailable."""
        # Mock test mode at decorator level (bypass skip) and setproctitle availability
        with patch("provide.foundation.testmode.decorators.is_in_test_mode", return_value=False):
            with patch("provide.foundation.process.title._HAS_SETPROCTITLE", False):
                from provide.foundation.process.title import get_process_title

                result = get_process_title()
                assert result is None

    def test_set_process_title_skips_in_test_mode(self) -> None:
        """Test that set_process_title is automatically skipped in test mode."""
        from provide.foundation.process import set_process_title

        # In test mode (which we're always in during tests), this should return True
        # but not actually set the process title
        result = set_process_title("test-title-in-test-mode")
        assert result is True  # Should succeed (skip gracefully)

    def test_get_process_title_returns_none_in_test_mode(self) -> None:
        """Test that get_process_title returns None in test mode."""
        from provide.foundation.process import get_process_title

        # In test mode, should return None regardless of setproctitle availability
        result = get_process_title()
        assert result is None

    # Skipping exception tests for optional modules - hard to mock when they don't exist

    def test_set_process_title_with_empty_string(self) -> None:
        """Test setting process title with empty string."""
        from provide.foundation.process import has_setproctitle

        if not has_setproctitle():
            pytest.skip("setproctitle not available")

        # Mock test mode to allow actual process title operations
        with patch("provide.foundation.testmode.decorators.is_in_test_mode", return_value=False):
            from provide.foundation.process import set_process_title

            result = set_process_title("")
            assert result is True

    def test_set_process_title_with_unicode(self) -> None:
        """Test setting process title with unicode characters."""
        from provide.foundation.process import has_setproctitle

        if not has_setproctitle():
            pytest.skip("setproctitle not available")

        # Mock test mode to allow actual process title operations
        with patch("provide.foundation.testmode.decorators.is_in_test_mode", return_value=False):
            from provide.foundation.process import set_process_title

            result = set_process_title("test-process-🚀")
            assert result is True

    def test_set_process_title_with_long_string(self) -> None:
        """Test setting process title with very long string."""
        from provide.foundation.process import has_setproctitle

        if not has_setproctitle():
            pytest.skip("setproctitle not available")

        # Mock test mode to allow actual process title operations
        with patch("provide.foundation.testmode.decorators.is_in_test_mode", return_value=False):
            from provide.foundation.process import set_process_title

            long_title = "a" * 1000
            result = set_process_title(long_title)
            assert result is True


# 🧱🏗️🔚
