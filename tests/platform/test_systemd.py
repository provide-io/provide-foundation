#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#


from __future__ import annotations

import sys

from provide.testkit import FoundationTestCase
from provide.testkit.mocking import MagicMock, patch
import pytest


class TestSystemdIntegration(FoundationTestCase):
    """Test systemd integration functionality."""

    def setup_method(self) -> None:
        """Set up test environment."""
        super().setup_method()

    def teardown_method(self) -> None:
        """Clean up after test."""
        super().teardown_method()

    def test_has_systemd_returns_bool(self) -> None:
        """Test has_systemd returns boolean."""
        from provide.foundation.platform import has_systemd

        result = has_systemd()
        assert isinstance(result, bool)

    def test_has_systemd_false_on_non_linux(self) -> None:
        """Test has_systemd returns False on non-Linux systems."""
        with patch("provide.foundation.platform.systemd._IS_LINUX", False):
            from provide.foundation.platform.systemd import has_systemd

            result = has_systemd()
            assert result is False

    def test_notify_ready_without_systemd(self) -> None:
        """Test notify_ready returns False when systemd unavailable."""
        with patch("provide.foundation.platform.systemd._HAS_SDNOTIFY", False):
            from provide.foundation.platform import notify_ready

            result = notify_ready()
            assert result is False

    def test_notify_status_without_systemd(self) -> None:
        """Test notify_status returns False when systemd unavailable."""
        with patch("provide.foundation.platform.systemd._HAS_SDNOTIFY", False):
            from provide.foundation.platform import notify_status

            result = notify_status("test status")
            assert result is False

    def test_notify_watchdog_without_systemd(self) -> None:
        """Test notify_watchdog returns False when systemd unavailable."""
        with patch("provide.foundation.platform.systemd._HAS_SDNOTIFY", False):
            from provide.foundation.platform import notify_watchdog

            result = notify_watchdog()
            assert result is False

    def test_notify_reloading_without_systemd(self) -> None:
        """Test notify_reloading returns False when systemd unavailable."""
        with patch("provide.foundation.platform.systemd._HAS_SDNOTIFY", False):
            from provide.foundation.platform import notify_reloading

            result = notify_reloading()
            assert result is False

    def test_notify_stopping_without_systemd(self) -> None:
        """Test notify_stopping returns False when systemd unavailable."""
        with patch("provide.foundation.platform.systemd._HAS_SDNOTIFY", False):
            from provide.foundation.platform import notify_stopping

            result = notify_stopping()
            assert result is False

    def test_notify_error_without_systemd(self) -> None:
        """Test notify_error returns False when systemd unavailable."""
        with patch("provide.foundation.platform.systemd._HAS_SDNOTIFY", False):
            from provide.foundation.platform import notify_error

            result = notify_error(1, "test error")
            assert result is False

    @pytest.mark.skipif(
        not sys.platform.startswith("linux"),
        reason="systemd only available on Linux",
    )
    def test_notify_ready_with_systemd_available(self) -> None:
        """Test notify_ready when systemd is available (Linux only)."""
        from provide.foundation.platform import has_systemd

        if not has_systemd():
            pytest.skip("sdnotify not installed")

        from provide.foundation.platform import notify_ready

        # This may or may not succeed depending on if we're running under systemd
        result = notify_ready()
        assert isinstance(result, bool)

    def test_notify_ready_handles_exception(self) -> None:
        """Test notify_ready handles exceptions gracefully."""
        with patch("provide.foundation.platform.systemd._HAS_SDNOTIFY", True):
            with patch("provide.foundation.platform.systemd._notifier") as mock_notifier:
                mock_notifier.notify = MagicMock(side_effect=RuntimeError("Test error"))

                from provide.foundation.platform import notify_ready

                result = notify_ready()
                assert result is False

    def test_notify_status_handles_exception(self) -> None:
        """Test notify_status handles exceptions gracefully."""
        with patch("provide.foundation.platform.systemd._HAS_SDNOTIFY", True):
            with patch("provide.foundation.platform.systemd._notifier") as mock_notifier:
                mock_notifier.notify = MagicMock(side_effect=RuntimeError("Test error"))

                from provide.foundation.platform import notify_status

                result = notify_status("test")
                assert result is False

    def test_notify_error_with_errno_only(self) -> None:
        """Test notify_error with errno only."""
        with patch("provide.foundation.platform.systemd._HAS_SDNOTIFY", False):
            from provide.foundation.platform import notify_error

            result = notify_error(5)
            assert result is False

    def test_notify_error_with_errno_and_message(self) -> None:
        """Test notify_error with errno and message."""
        with patch("provide.foundation.platform.systemd._HAS_SDNOTIFY", False):
            from provide.foundation.platform import notify_error

            result = notify_error(5, "test error message")
            assert result is False


# 🧱🏗️🔚
