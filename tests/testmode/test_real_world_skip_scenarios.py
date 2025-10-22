# tests/testmode/test_real_world_skip_scenarios.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from io import StringIO

from provide.testkit import FoundationTestCase
from provide.testkit.mocking import patch


class TestRealWorldSkipScenarios(FoundationTestCase):
    """Test real-world scenarios for skip_in_test_mode decorator."""

    def setup_method(self) -> None:
        """Set up test environment."""
        super().setup_method()

    def teardown_method(self) -> None:
        """Clean up after test."""
        super().teardown_method()

    def test_process_title_functions_skip_gracefully_in_tests(self) -> None:
        """Test that process title functions skip gracefully in test mode."""
        from provide.foundation.process import get_process_title, set_process_title

        # In test mode, set_process_title should return True (success/skip)
        result = set_process_title("test-process-title")
        assert result is True

        # In test mode, get_process_title should return None
        title = get_process_title()
        assert title is None

    def test_systemd_functions_skip_gracefully_in_tests(self) -> None:
        """Test that systemd functions skip gracefully in test mode."""
        from provide.foundation.platform import (
            notify_error,
            notify_ready,
            notify_reloading,
            notify_status,
            notify_stopping,
            notify_watchdog,
        )

        # All systemd notify functions should return False in test mode
        assert notify_ready() is False
        assert notify_status("test status") is False
        assert notify_watchdog() is False
        assert notify_reloading() is False
        assert notify_stopping() is False
        assert notify_error(1, "test error") is False

    def test_decorator_logs_skip_message(self) -> None:
        """Test that decorator logs skip message when skipping."""
        from provide.foundation.logger import logger
        from provide.foundation.process import set_process_title

        # Capture logs
        log_stream = StringIO()
        from provide.foundation.streams import configure_stream

        configure_stream("test", stream=log_stream, formatter="json")

        # Call function that should be skipped
        set_process_title("test-skip-logging")

        # Check log output
        log_output = log_stream.getvalue()
        assert "Skipping set_process_title in test mode" in log_output

    def test_decorator_can_be_bypassed_for_actual_testing(self) -> None:
        """Test that decorator can be bypassed when we need to test actual functionality."""
        from provide.foundation.process.title import set_process_title

        # Mock is_in_test_mode to return False
        with patch("provide.foundation.testmode.decorators.is_in_test_mode", return_value=False):
            # Also mock setproctitle availability to test the code path
            with patch("provide.foundation.process.title._HAS_SETPROCTITLE", True):
                with patch("provide.foundation.process.title.setproctitle") as mock_setproctitle:
                    mock_setproctitle.setproctitle = lambda x: None
                    mock_setproctitle.getproctitle = lambda: "test"

                    # Now the function should actually try to execute
                    # This demonstrates how we can test the actual implementation
                    # even when the decorator would normally skip it
                    result = set_process_title("actual-test")

                    # Since we mocked setproctitle to exist but not throw errors,
                    # it should attempt to call it
                    assert result is True

    def test_multiple_decorated_functions_all_skip_in_test_mode(self) -> None:
        """Test that multiple decorated functions all skip correctly."""
        from provide.foundation.platform import notify_ready, notify_status
        from provide.foundation.process import get_process_title, set_process_title

        # All should skip and return their configured return values
        assert set_process_title("test-1") is True
        assert get_process_title() is None
        assert notify_ready() is False
        assert notify_status("test") is False

    def test_registry_accessible_for_introspection(self) -> None:
        """Test that registry is accessible for runtime introspection."""
        from provide.foundation.testmode import get_test_unsafe_features

        registry = get_test_unsafe_features()

        # Should contain all our decorated functions
        assert len(registry) == 8  # 2 process.title + 6 platform.systemd

        # Each entry should have complete metadata
        for func_id, metadata in registry.items():
            assert "function" in metadata
            assert "return_value" in metadata
            assert "reason" in metadata
            assert callable(metadata["function"])


# <3 🧱🤝🧪🪄
