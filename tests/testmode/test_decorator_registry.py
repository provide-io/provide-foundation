#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#


from __future__ import annotations

from provide.testkit import FoundationTestCase


class TestDecoratorRegistry(FoundationTestCase):
    """Test the test-unsafe feature registry system."""

    def setup_method(self) -> None:
        """Set up test environment."""
        super().setup_method()

    def teardown_method(self) -> None:
        """Clean up after test."""
        super().teardown_method()

    def test_skip_in_test_mode_decorator_exists(self) -> None:
        """Test that skip_in_test_mode decorator is available."""
        from provide.foundation.testmode import skip_in_test_mode

        assert callable(skip_in_test_mode)

    def test_get_test_unsafe_features_returns_registry(self) -> None:
        """Test that get_test_unsafe_features returns the registry."""
        from provide.foundation.testmode import get_test_unsafe_features

        registry = get_test_unsafe_features()
        assert isinstance(registry, dict)

    def test_process_title_functions_are_registered(self) -> None:
        """Test that process title functions are registered as test-unsafe."""
        from provide.foundation.testmode import get_test_unsafe_features

        registry = get_test_unsafe_features()

        # Check set_process_title is registered (full module path)
        assert "provide.foundation.process.title.set_process_title" in registry
        set_title_entry = registry["provide.foundation.process.title.set_process_title"]
        assert set_title_entry["return_value"] is True
        assert "interfere with test isolation" in set_title_entry["reason"].lower()

        # Check get_process_title is registered
        assert "provide.foundation.process.title.get_process_title" in registry
        get_title_entry = registry["provide.foundation.process.title.get_process_title"]
        assert get_title_entry["return_value"] is None

    def test_systemd_functions_are_registered(self) -> None:
        """Test that systemd notify functions are registered as test-unsafe."""
        from provide.foundation.testmode import get_test_unsafe_features

        registry = get_test_unsafe_features()

        # All systemd notify functions should be registered (full module paths)
        expected_systemd_functions = [
            "provide.foundation.platform.systemd.notify_ready",
            "provide.foundation.platform.systemd.notify_status",
            "provide.foundation.platform.systemd.notify_watchdog",
            "provide.foundation.platform.systemd.notify_reloading",
            "provide.foundation.platform.systemd.notify_stopping",
            "provide.foundation.platform.systemd.notify_error",
        ]

        for func_id in expected_systemd_functions:
            assert func_id in registry, f"{func_id} should be registered as test-unsafe"
            entry = registry[func_id]
            assert entry["return_value"] is False  # All systemd functions return False when skipped
            assert "not meaningful in tests" in entry["reason"].lower()

    def test_is_test_unsafe_returns_true_for_decorated_functions(self) -> None:
        """Test that is_test_unsafe correctly identifies decorated functions."""
        from provide.foundation.process import set_process_title
        from provide.foundation.testmode import is_test_unsafe

        assert is_test_unsafe(set_process_title) is True

    def test_is_test_unsafe_returns_false_for_undecorated_functions(self) -> None:
        """Test that is_test_unsafe returns False for undecorated functions."""
        from provide.foundation.process import has_setproctitle
        from provide.foundation.testmode import is_test_unsafe

        # has_setproctitle is NOT decorated
        assert is_test_unsafe(has_setproctitle) is False

    def test_decorated_functions_skip_in_test_mode(self) -> None:
        """Test that decorated functions actually skip execution in test mode."""
        from provide.foundation.process import set_process_title

        # We're in test mode, so this should return True (skipped) immediately
        result = set_process_title("test-title-should-be-skipped")
        assert result is True  # Skipped successfully

    def test_all_registered_functions_have_required_metadata(self) -> None:
        """Test that all registered functions have complete metadata."""
        from provide.foundation.testmode import get_test_unsafe_features

        registry = get_test_unsafe_features()

        for func_id, metadata in registry.items():
            # Every registered function must have these fields
            assert "function" in metadata, f"{func_id} missing 'function' field"
            assert "return_value" in metadata, f"{func_id} missing 'return_value' field"
            assert "reason" in metadata, f"{func_id} missing 'reason' field"

            # Function should be callable
            assert callable(metadata["function"]), f"{func_id} function is not callable"

            # Reason should be a non-empty string
            assert isinstance(metadata["reason"], str), f"{func_id} reason is not a string"
            assert len(metadata["reason"]) > 0, f"{func_id} reason is empty"

    def test_registry_count_matches_expected_test_unsafe_features(self) -> None:
        """Test that we have the expected number of test-unsafe features registered."""
        from provide.foundation.testmode import get_test_unsafe_features

        registry = get_test_unsafe_features()

        # Current expected test-unsafe features:
        # - process.title: set_process_title, get_process_title, set_process_title_from_argv (3)
        # - platform.systemd: notify_ready, notify_status, notify_watchdog,
        #                     notify_reloading, notify_stopping, notify_error (6)
        # Total: 9 functions
        expected_count = 9
        actual_count = len(registry)

        assert actual_count == expected_count, (
            f"Expected {expected_count} test-unsafe features, but found {actual_count}. "
            f"Registered functions: {list(registry.keys())}"
        )


# 🧱🏗️🔚
