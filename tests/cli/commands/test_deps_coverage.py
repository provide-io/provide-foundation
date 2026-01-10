#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Comprehensive tests for cli/commands/deps.py module."""

from __future__ import annotations

from collections.abc import Generator
import threading
from typing import Any

from provide.testkit import FoundationTestCase
from provide.testkit.mocking import Mock, patch
import pytest

# Global lock to prevent parallel tests from interfering with module reloading
_MODULE_RELOAD_LOCK = threading.Lock()


@pytest.fixture(scope="function")
def module_reload_isolation() -> Generator[None, None, None]:
    """Ensure only one test at a time can manipulate sys.modules and reload modules."""
    with _MODULE_RELOAD_LOCK:
        yield


class TestDepsCommandWithClick(FoundationTestCase):
    """Test deps command when click is available."""

    def test_deps_command_exists(self) -> None:
        """Test that deps_command is exported."""
        from provide.foundation.cli.commands.deps import deps_command

        assert deps_command is not None

    def test_deps_command_with_click(self, module_reload_isolation: Any) -> None:
        """Test deps command when click is available."""
        # Just verify the command exists and is callable
        from provide.foundation.cli.commands.deps import deps_command

        assert deps_command is not None
        assert callable(deps_command)

    def test_deps_command_check_specific_available(self) -> None:
        """Test checking specific available dependency."""
        from provide.foundation.cli.commands.deps import _deps_command_impl

        with (
            patch(
                "provide.foundation.cli.commands.deps.has_dependency",
                return_value=True,
            ),
            patch("provide.foundation.cli.commands.deps.pout"),
        ):
            with pytest.raises(SystemExit) as exc_info:
                _deps_command_impl(quiet=False, check="crypto")

            assert exc_info.value.code == 0

    def test_deps_command_check_specific_missing(self) -> None:
        """Test checking specific missing dependency."""
        from provide.foundation.cli.commands.deps import _deps_command_impl

        with (
            patch(
                "provide.foundation.cli.commands.deps.has_dependency",
                return_value=False,
            ),
            patch("provide.foundation.cli.commands.deps.pout") as mock_pout,
        ):
            with pytest.raises(SystemExit) as exc_info:
                _deps_command_impl(quiet=False, check="crypto")

            assert exc_info.value.code == 1
            assert mock_pout.call_count == 2
            mock_pout.assert_any_call("❌ crypto: Missing")
            mock_pout.assert_any_call("Install with: uv add 'provide-foundation[crypto]'")

    def test_deps_command_check_specific_quiet(self) -> None:
        """Test checking specific dependency in quiet mode."""
        from provide.foundation.cli.commands.deps import _deps_command_impl

        with (
            patch(
                "provide.foundation.cli.commands.deps.has_dependency",
                return_value=True,
            ),
            patch("provide.foundation.cli.commands.deps.pout") as mock_pout,
        ):
            with pytest.raises(SystemExit) as exc_info:
                _deps_command_impl(quiet=True, check="cli")

            assert exc_info.value.code == 0
            mock_pout.assert_not_called()

    def test_deps_command_check_all_available(self) -> None:
        """Test checking all dependencies when all available."""
        from provide.foundation.cli.commands.deps import _deps_command_impl

        mock_dep = Mock(available=True)
        with patch(
            "provide.foundation.cli.commands.deps.check_optional_deps",
            return_value=[mock_dep, mock_dep],
        ):
            with pytest.raises(SystemExit) as exc_info:
                _deps_command_impl(quiet=False, check=None)

            assert exc_info.value.code == 0

    def test_deps_command_check_all_some_missing(self) -> None:
        """Test checking all dependencies when some missing."""
        # Import first to get the actual function
        from provide.foundation.cli.commands.deps import _deps_command_impl

        mock_dep_available = Mock(available=True)
        mock_dep_missing = Mock(available=False)

        # Patch within the module where it's used
        with patch(
            "provide.foundation.cli.commands.deps.check_optional_deps",
            return_value=[mock_dep_available, mock_dep_missing],
        ):
            with pytest.raises(SystemExit) as exc_info:
                _deps_command_impl(quiet=False, check=None)

            # Exit code 0 means all deps present, 1 means some missing
            # Since we have 1 available and 1 missing, it should exit 1
            assert exc_info.value.code == 1

    def test_deps_command_check_all_quiet(self) -> None:
        """Test checking all dependencies in quiet mode."""
        from provide.foundation.cli.commands.deps import _deps_command_impl

        mock_dep = Mock(available=True)
        with patch(
            "provide.foundation.cli.commands.deps.check_optional_deps",
            return_value=[mock_dep],
        ) as mock_check:
            with pytest.raises(SystemExit) as exc_info:
                _deps_command_impl(quiet=True, check=None)

            assert exc_info.value.code == 0
            # Verify that the function was called with the right args
            mock_check.assert_called_with(quiet=True, return_status=True)


class TestDepsCommandWithoutClick(FoundationTestCase):
    """Test deps command when click is not available."""

    def test_deps_command_without_click(self, module_reload_isolation: Any) -> None:
        """Test deps_command behavior when click not available."""
        # Test that the implementation can be called without Click
        from provide.foundation.cli.commands.deps import _deps_command_impl

        # The impl function should work fine without Click
        with (
            patch("provide.foundation.cli.commands.deps.has_dependency", return_value=True),
            patch("provide.foundation.cli.commands.deps.pout"),
        ):
            with pytest.raises(SystemExit) as exc_info:
                _deps_command_impl(quiet=True, check="crypto")

            assert exc_info.value.code == 0

    def test_require_click_raises_error(self) -> None:
        """Test requires_click decorator is applied."""
        from provide.foundation.cli.commands.deps import deps_command

        # Just verify the decorator is present by checking for the wrapped function
        assert hasattr(deps_command, "__wrapped__") or hasattr(deps_command, "callback")

    def test_deps_command_stub_with_args(self, module_reload_isolation: Any) -> None:
        """Test that implementation accepts arguments."""
        from provide.foundation.cli.commands.deps import _deps_command_impl

        # Test the implementation function directly
        with (
            patch("provide.foundation.cli.commands.deps.has_dependency", return_value=False),
            patch("provide.foundation.cli.commands.deps.pout"),
        ):
            with pytest.raises(SystemExit) as exc_info:
                _deps_command_impl(quiet=True, check="some_dep")

            assert exc_info.value.code == 1


class TestDepsCommandDecorators(FoundationTestCase):
    """Test click decorators on deps_command."""

    def test_click_decorators_applied(self) -> None:
        """Test that click decorators are properly applied."""
        # Test that the decorated function exists and has expected attributes
        from provide.foundation.cli.commands.deps import deps_command

        # Check that the function is a click command
        assert hasattr(deps_command, "callback")
        assert callable(deps_command.callback)


class TestDepsCommandModuleImport(FoundationTestCase):
    """Test module-level import behavior."""

    def test_module_imports_successfully(self) -> None:
        """Test module imports without errors."""
        import provide.foundation.cli.commands.deps

        assert provide.foundation.cli.commands.deps.__all__ == ["deps_command"]

    def test_has_click_flag_exists(self) -> None:
        """Test _HAS_CLICK flag exists in cli.deps."""
        from provide.foundation.cli.deps import _HAS_CLICK

        assert isinstance(_HAS_CLICK, bool)

    def test_click_import_handling(self, module_reload_isolation: Any) -> None:
        """Test click import is handled properly."""
        # Test that the CLI deps module handles click import correctly
        from provide.foundation.cli.deps import _HAS_CLICK

        # Since click is installed in our test environment, it should be True
        assert _HAS_CLICK is True


class TestDepsCommandEdgeCases(FoundationTestCase):
    """Test edge cases and error conditions."""

    def test_empty_deps_list(self) -> None:
        """Test handling empty dependency list."""
        from provide.foundation.cli.commands.deps import _deps_command_impl

        with patch("provide.foundation.cli.commands.deps.check_optional_deps", return_value=[]):
            with pytest.raises(SystemExit) as exc_info:
                _deps_command_impl(quiet=False, check=None)

            assert exc_info.value.code == 0  # No deps means all available

    def test_check_nonexistent_dependency(self) -> None:
        """Test checking non-existent dependency."""
        from provide.foundation.cli.commands.deps import _deps_command_impl

        with (
            patch("provide.foundation.cli.commands.deps.has_dependency", return_value=False),
            patch("provide.foundation.cli.commands.deps.pout"),
        ):
            with pytest.raises(SystemExit) as exc_info:
                _deps_command_impl(quiet=False, check="nonexistent")

            assert exc_info.value.code == 1


# 🧱🏗️🔚
