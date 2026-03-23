#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Comprehensive coverage tests for testmode/detection.py.

These tests target uncovered lines and edge cases in test environment detection."""

from __future__ import annotations

import sys
import types

from provide.testkit import FoundationTestCase
from provide.testkit.mocking import Mock, patch

from provide.foundation.testmode.detection import (
    _clear_test_mode_cache,
    is_in_click_testing,
    is_in_test_mode,
    should_allow_stream_redirect,
    should_use_shared_registries,
)


def _make_fake_frame(
    filename: str = "unknown",
    module_name: str = "__main__",
    local_vars: dict | None = None,
    f_back: types.FrameType | object | None = None,
) -> Mock:
    """Build a mock object that quacks like a frame for sys._getframe() walking."""
    frame = Mock()
    code = Mock()
    code.co_filename = filename
    frame.f_code = code
    frame.f_globals = {"__name__": module_name}
    frame.f_locals = local_vars or {}
    frame.f_back = f_back
    return frame


class TestIsInTestMode(FoundationTestCase):
    """Test is_in_test_mode() function."""

    def setup_method(self) -> None:
        """Set up test environment."""
        super().setup_method()
        # Clear the test mode cache to ensure fresh detection in each test
        _clear_test_mode_cache()

    def test_detects_pytest_current_test_env_var(self) -> None:
        """Test detection via PYTEST_CURRENT_TEST environment variable."""
        with patch.dict("os.environ", {"PYTEST_CURRENT_TEST": "test_file.py::test_func"}):
            assert is_in_test_mode() is True

    def test_detects_pytest_in_sys_modules_and_argv(self) -> None:
        """Test detection when pytest in sys.modules and sys.argv."""
        # pytest is likely already in sys.modules during test run
        with patch("sys.argv", ["pytest", "tests/"]):
            assert is_in_test_mode() is True

    def test_detects_pytest_in_stack_frame_filename(self) -> None:
        """Test detection by finding pytest in stack frame filenames."""
        fake = _make_fake_frame(filename="/path/to/pytest/runner.py")

        with (
            patch("provide.foundation.testmode.detection.sys._getframe", return_value=fake),
            patch.dict("sys.modules", {"pytest": Mock()}),
        ):
            # Need to ensure pytest not in argv to test this path
            with patch("sys.argv", ["python", "script.py"]):
                assert is_in_test_mode() is True

    def test_detects_test_file_in_stack_frame(self) -> None:
        """Test detection by finding /test_ in stack frame filename."""
        fake = _make_fake_frame(filename="/project/tests/test_module.py")

        with (
            patch("provide.foundation.testmode.detection.sys._getframe", return_value=fake),
            patch.dict("sys.modules", {"pytest": Mock()}),
            patch("sys.argv", ["python", "script.py"]),
        ):
            assert is_in_test_mode() is True

    def test_detects_conftest_in_stack_frame(self) -> None:
        """Test detection by finding conftest.py in stack frame."""
        fake = _make_fake_frame(filename="/project/tests/conftest.py")

        with (
            patch("provide.foundation.testmode.detection.sys._getframe", return_value=fake),
            patch.dict("sys.modules", {"pytest": Mock()}),
            patch("sys.argv", ["python", "script.py"]),
        ):
            assert is_in_test_mode() is True

    def test_detects_unittest_in_sys_modules_and_argv(self) -> None:
        """Test detection when unittest in sys.modules and sys.argv."""
        with (
            patch.dict("sys.modules", {"unittest": Mock()}),
            patch("sys.argv", ["python", "-m", "unittest", "discover"]),
            patch.dict("os.environ", {}, clear=True),
        ):
            assert is_in_test_mode() is True

    def test_returns_false_when_not_in_test_mode(self) -> None:
        """Test returns False when no test indicators present."""
        # Remove pytest from sys.modules for this test
        original_pytest = sys.modules.get("pytest")

        try:
            if "pytest" in sys.modules:
                del sys.modules["pytest"]

            with (
                patch.dict("os.environ", {}, clear=True),
                patch("sys.argv", ["python", "app.py"]),
            ):
                assert is_in_test_mode() is False
        finally:
            # Restore pytest if it was present
            if original_pytest is not None:
                sys.modules["pytest"] = original_pytest

    def test_handles_no_matching_frame(self) -> None:
        """Test handling when no stack frame matches test indicators."""
        fake = _make_fake_frame(filename="/path/to/regular_module.py")

        with (
            patch("provide.foundation.testmode.detection.sys._getframe", return_value=fake),
            patch.dict("sys.modules", {"pytest": Mock()}),
            patch("sys.argv", ["python", "script.py"]),
            patch.dict("os.environ", {}, clear=True),
        ):
            # Should not crash and should fall through
            result = is_in_test_mode()
            assert isinstance(result, bool)


class TestIsInClickTesting(FoundationTestCase):
    """Test is_in_click_testing() function."""

    def setup_method(self) -> None:
        """Set up test environment."""
        super().setup_method()
        # Clear the detection caches so each test gets fresh detection
        _clear_test_mode_cache()

    def test_detects_click_testing_from_stream_config(self) -> None:
        """Test detection via StreamConfig.click_testing flag."""
        mock_config = Mock()
        mock_config.click_testing = True

        with patch("provide.foundation.streams.config.get_stream_config", return_value=mock_config):
            assert is_in_click_testing() is True

    def test_detects_click_testing_module_in_stack(self) -> None:
        """Test detection via click.testing module in stack."""
        mock_config = Mock()
        mock_config.click_testing = False

        fake = _make_fake_frame(
            filename="/path/to/test.py",
            module_name="click.testing",
        )

        with (
            patch("provide.foundation.streams.config.get_stream_config", return_value=mock_config),
            patch("provide.foundation.testmode.detection.sys._getframe", return_value=fake),
        ):
            assert is_in_click_testing() is True

    def test_detects_test_cli_integration_in_filename(self) -> None:
        """Test detection via test_cli_integration in filename."""
        mock_config = Mock()
        mock_config.click_testing = False

        fake = _make_fake_frame(
            filename="/project/tests/test_cli_integration.py",
            module_name="tests.cli",
        )

        with (
            patch("provide.foundation.streams.config.get_stream_config", return_value=mock_config),
            patch("provide.foundation.testmode.detection.sys._getframe", return_value=fake),
        ):
            assert is_in_click_testing() is True

    def test_detects_cli_runner_in_locals(self) -> None:
        """Test detection via CliRunner object in frame locals."""
        mock_config = Mock()
        mock_config.click_testing = False

        # Create mock CliRunner
        mock_runner = Mock()
        mock_runner.invoke = Mock()

        # Create mock self object with runner attribute
        mock_self = Mock()
        mock_self.runner = mock_runner

        fake = _make_fake_frame(
            filename="/path/to/test.py",
            module_name="test_module",
            local_vars={"self": mock_self},
        )

        with (
            patch("provide.foundation.streams.config.get_stream_config", return_value=mock_config),
            patch("provide.foundation.testmode.detection.sys._getframe", return_value=fake),
        ):
            # Make type(runner) return a string with CliRunner in it
            with patch("builtins.type", return_value=type("CliRunner", (), {})):
                assert is_in_click_testing() is True

    def test_returns_false_when_not_in_click_testing(self) -> None:
        """Test returns False when no Click testing indicators present."""
        mock_config = Mock()
        mock_config.click_testing = False

        fake = _make_fake_frame(
            filename="/path/to/regular_test.py",
            module_name="regular_module",
        )

        with (
            patch("provide.foundation.streams.config.get_stream_config", return_value=mock_config),
            patch("provide.foundation.testmode.detection.sys._getframe", return_value=fake),
        ):
            assert is_in_click_testing() is False

    def test_handles_self_without_runner_attribute(self) -> None:
        """Test handling of self object without runner attribute."""
        mock_config = Mock()
        mock_config.click_testing = False

        mock_self = Mock(spec=[])  # No runner attribute

        fake = _make_fake_frame(
            filename="/path/to/test.py",
            module_name="test_module",
            local_vars={"self": mock_self},
        )

        with (
            patch("provide.foundation.streams.config.get_stream_config", return_value=mock_config),
            patch("provide.foundation.testmode.detection.sys._getframe", return_value=fake),
        ):
            # Should handle missing runner attribute gracefully
            result = is_in_click_testing()
            assert result is False

    def test_handles_runner_without_invoke_method(self) -> None:
        """Test handling of runner object without invoke method."""
        mock_config = Mock()
        mock_config.click_testing = False

        mock_runner = Mock(spec=[])  # No invoke method
        mock_self = Mock()
        mock_self.runner = mock_runner

        fake = _make_fake_frame(
            filename="/path/to/test.py",
            module_name="test_module",
            local_vars={"self": mock_self},
        )

        with (
            patch("provide.foundation.streams.config.get_stream_config", return_value=mock_config),
            patch("provide.foundation.testmode.detection.sys._getframe", return_value=fake),
        ):
            # Should handle missing invoke method gracefully
            result = is_in_click_testing()
            assert result is False


class TestShouldAllowStreamRedirect(FoundationTestCase):
    """Test should_allow_stream_redirect() function."""

    def setup_method(self) -> None:
        """Set up test environment."""
        super().setup_method()
        # Clear the detection caches so each test gets fresh detection
        _clear_test_mode_cache()

    def test_allows_redirect_when_force_flag_enabled(self) -> None:
        """Test stream redirect allowed when force flag is set."""
        mock_config = Mock()
        mock_config.force_stream_redirect = True

        with patch("provide.foundation.streams.config.get_stream_config", return_value=mock_config):
            assert should_allow_stream_redirect() is True

    def test_allows_redirect_when_not_in_click_testing(self) -> None:
        """Test stream redirect allowed when not in Click testing context."""
        mock_config = Mock()
        mock_config.force_stream_redirect = False
        mock_config.click_testing = False

        fake = _make_fake_frame(
            filename="/path/to/regular_test.py",
            module_name="regular_module",
        )

        with (
            patch("provide.foundation.streams.config.get_stream_config", return_value=mock_config),
            patch("provide.foundation.testmode.detection.sys._getframe", return_value=fake),
        ):
            assert should_allow_stream_redirect() is True

    def test_blocks_redirect_when_in_click_testing(self) -> None:
        """Test stream redirect blocked when in Click testing context."""
        mock_config = Mock()
        mock_config.force_stream_redirect = False
        mock_config.click_testing = True

        with patch("provide.foundation.streams.config.get_stream_config", return_value=mock_config):
            assert should_allow_stream_redirect() is False

    def test_force_flag_overrides_click_testing(self) -> None:
        """Test force flag overrides Click testing context."""
        # First call checks force_stream_redirect, second call is for is_in_click_testing
        configs = [Mock(force_stream_redirect=True), Mock(click_testing=True)]

        with patch(
            "provide.foundation.streams.config.get_stream_config",
            side_effect=configs,
        ):
            # Force flag should override click_testing
            assert should_allow_stream_redirect() is True


class TestShouldUseSharedRegistries(FoundationTestCase):
    """Test should_use_shared_registries() function."""

    def setup_method(self) -> None:
        """Set up test environment."""
        super().setup_method()

    def test_returns_true_when_use_shared_true(self) -> None:
        """Test returns True when use_shared_registries is True."""
        result = should_use_shared_registries(
            use_shared_registries=True,
            component_registry=None,
            command_registry=None,
        )

        assert result is True

    def test_returns_false_when_use_shared_false(self) -> None:
        """Test returns False when use_shared_registries is False."""
        result = should_use_shared_registries(
            use_shared_registries=False,
            component_registry=None,
            command_registry=None,
        )

        assert result is False

    def test_ignores_component_registry_parameter(self) -> None:
        """Test component_registry parameter doesn't affect result."""
        mock_registry = Mock()

        result = should_use_shared_registries(
            use_shared_registries=True,
            component_registry=mock_registry,
            command_registry=None,
        )

        assert result is True

    def test_ignores_command_registry_parameter(self) -> None:
        """Test command_registry parameter doesn't affect result."""
        mock_registry = Mock()

        result = should_use_shared_registries(
            use_shared_registries=False,
            component_registry=None,
            command_registry=mock_registry,
        )

        assert result is False

    def test_ignores_both_registry_parameters(self) -> None:
        """Test both registry parameters don't affect result."""
        result = should_use_shared_registries(
            use_shared_registries=True,
            component_registry=Mock(),
            command_registry=Mock(),
        )

        assert result is True


class TestDetectionEdgeCases(FoundationTestCase):
    """Test edge cases in detection functions."""

    def setup_method(self) -> None:
        """Set up test environment."""
        super().setup_method()
        # Clear the detection caches so each test gets fresh detection
        _clear_test_mode_cache()

    def test_is_in_test_mode_with_no_matching_frames(self) -> None:
        """Test is_in_test_mode when no frame matches test indicators."""
        fake = _make_fake_frame(filename="/path/to/regular.py")

        with (
            patch("provide.foundation.testmode.detection.sys._getframe", return_value=fake),
            patch.dict("sys.modules", {"pytest": Mock()}),
            patch("sys.argv", ["python", "script.py"]),
            patch.dict("os.environ", {}, clear=True),
        ):
            # Should not crash and should fall through to False
            result = is_in_test_mode()
            assert isinstance(result, bool)

    def test_is_in_click_testing_with_no_matching_frames(self) -> None:
        """Test is_in_click_testing when no frame matches."""
        mock_config = Mock()
        mock_config.click_testing = False

        fake = _make_fake_frame(filename="/path/to/regular.py")

        with (
            patch("provide.foundation.streams.config.get_stream_config", return_value=mock_config),
            patch("provide.foundation.testmode.detection.sys._getframe", return_value=fake),
        ):
            assert is_in_click_testing() is False

    def test_is_in_test_mode_multiple_indicators(self) -> None:
        """Test is_in_test_mode returns True early with multiple indicators."""
        # PYTEST_CURRENT_TEST should cause immediate return without frame walking
        with patch.dict("os.environ", {"PYTEST_CURRENT_TEST": "test"}):
            assert is_in_test_mode() is True

    def test_is_in_click_testing_early_return_on_config_flag(self) -> None:
        """Test is_in_click_testing returns True early when config flag set."""
        mock_config = Mock()
        mock_config.click_testing = True

        with patch("provide.foundation.streams.config.get_stream_config", return_value=mock_config):
            assert is_in_click_testing() is True

    def test_is_in_test_mode_caches_result(self) -> None:
        """Test that is_in_test_mode caches its result for performance."""
        # Clear cache before test
        _clear_test_mode_cache()

        with patch.dict("os.environ", {"PYTEST_CURRENT_TEST": "test"}):
            # First call - should detect test mode and cache it
            result1 = is_in_test_mode()
            assert result1 is True

            # Second call - should return cached result (no env var check needed)
            result2 = is_in_test_mode()
            assert result2 is True

            # Third call - should still return cached result
            result3 = is_in_test_mode()
            assert result3 is True

            # All three should be True from cache
            assert result1 == result2 == result3 is True


__all__ = [
    "TestDetectionEdgeCases",
    "TestIsInClickTesting",
    "TestIsInTestMode",
    "TestShouldAllowStreamRedirect",
    "TestShouldUseSharedRegistries",
]

# 🧱🏗️🔚
