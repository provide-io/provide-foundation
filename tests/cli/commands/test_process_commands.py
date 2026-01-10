#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for CLI process commands."""

from __future__ import annotations

from provide.testkit import FoundationTestCase
from provide.testkit.mocking import patch


class TestProcessCommandsWithSetproctitle(FoundationTestCase):
    """Test process commands when setproctitle is available."""

    def test_set_title_implementation(self) -> None:
        """Test set-title command implementation."""
        from provide.foundation.cli.commands.process import _set_title_impl

        with (
            patch(
                "provide.foundation.cli.commands.process.has_setproctitle",
                return_value=True,
            ),
            patch("provide.foundation.cli.commands.process.set_process_title") as mock_set,
            patch("provide.foundation.cli.commands.process.pout"),
        ):
            _set_title_impl("test-app")

            mock_set.assert_called_once_with("test-app")

    def test_set_title_without_setproctitle(self) -> None:
        """Test set-title command when setproctitle not available."""
        from provide.foundation.cli.commands.process import _set_title_impl

        with (
            patch(
                "provide.foundation.cli.commands.process.has_setproctitle",
                return_value=False,
            ),
            patch("provide.foundation.cli.commands.process.perr") as mock_perr,
        ):
            _set_title_impl("test-app")

            assert mock_perr.call_count == 2
            mock_perr.assert_any_call("⚠️  Process title support not available")
            mock_perr.assert_any_call("Install with: uv add 'provide-foundation[process]'")

    def test_get_title_implementation(self) -> None:
        """Test get-title command implementation."""
        from provide.foundation.cli.commands.process import _get_title_impl

        with (
            patch(
                "provide.foundation.cli.commands.process.has_setproctitle",
                return_value=True,
            ),
            patch(
                "provide.foundation.cli.commands.process.get_process_title",
                return_value="current-title",
            ) as mock_get,
            patch("provide.foundation.cli.commands.process.pout") as mock_pout,
        ):
            _get_title_impl()

            mock_get.assert_called_once()
            mock_pout.assert_called_once_with("Current process title: current-title")

    def test_get_title_without_setproctitle(self) -> None:
        """Test get-title command when setproctitle not available."""
        from provide.foundation.cli.commands.process import _get_title_impl

        with (
            patch(
                "provide.foundation.cli.commands.process.has_setproctitle",
                return_value=False,
            ),
            patch("provide.foundation.cli.commands.process.perr") as mock_perr,
        ):
            _get_title_impl()

            assert mock_perr.call_count == 2
            mock_perr.assert_any_call("⚠️  Process title support not available")

    def test_info_implementation_available(self) -> None:
        """Test info command when setproctitle is available."""
        from provide.foundation.cli.commands.process import _info_impl

        with (
            patch(
                "provide.foundation.cli.commands.process.has_setproctitle",
                return_value=True,
            ),
            patch(
                "provide.foundation.cli.commands.process.get_process_title",
                return_value="info-test",
            ),
            patch("provide.foundation.cli.commands.process.pout") as mock_pout,
        ):
            _info_impl()

            mock_pout.assert_called_once_with("Current title: info-test")

    def test_info_implementation_not_available(self) -> None:
        """Test info command when setproctitle is not available."""
        from provide.foundation.cli.commands.process import _info_impl

        with (
            patch(
                "provide.foundation.cli.commands.process.has_setproctitle",
                return_value=False,
            ),
            patch("provide.foundation.cli.commands.process.pout") as mock_pout,
        ):
            _info_impl()

            assert mock_pout.call_count == 2
            mock_pout.assert_any_call("⚠️  Process title support: Not available")
            mock_pout.assert_any_call("Install with: uv add 'provide-foundation[process]'")

    def test_process_group_exists(self) -> None:
        """Test that process_group command group exists."""
        from provide.foundation.cli.commands.process import process_group

        assert process_group is not None
        assert callable(process_group)

    def test_set_title_command_exists(self) -> None:
        """Test that set-title command exists."""
        from provide.foundation.cli.commands.process import set_title_command

        assert set_title_command is not None
        assert callable(set_title_command)

    def test_get_title_command_exists(self) -> None:
        """Test that get-title command exists."""
        from provide.foundation.cli.commands.process import get_title_command

        assert get_title_command is not None
        assert callable(get_title_command)

    def test_info_command_exists(self) -> None:
        """Test that info command exists."""
        from provide.foundation.cli.commands.process import info_command

        assert info_command is not None
        assert callable(info_command)


class TestProcessCommandsEdgeCases(FoundationTestCase):
    """Test edge cases for process commands."""

    def test_set_title_with_special_characters(self) -> None:
        """Test setting title with special characters."""
        from provide.foundation.cli.commands.process import _set_title_impl

        special_title = "my-app_worker:123"

        with (
            patch(
                "provide.foundation.cli.commands.process.has_setproctitle",
                return_value=True,
            ),
            patch("provide.foundation.cli.commands.process.set_process_title") as mock_set,
            patch("provide.foundation.cli.commands.process.pout"),
        ):
            _set_title_impl(special_title)

            mock_set.assert_called_once_with(special_title)

    def test_set_title_with_unicode(self) -> None:
        """Test setting title with unicode characters."""
        from provide.foundation.cli.commands.process import _set_title_impl

        unicode_title = "my-app-✨"

        with (
            patch(
                "provide.foundation.cli.commands.process.has_setproctitle",
                return_value=True,
            ),
            patch("provide.foundation.cli.commands.process.set_process_title") as mock_set,
            patch("provide.foundation.cli.commands.process.pout"),
        ):
            _set_title_impl(unicode_title)

            mock_set.assert_called_once_with(unicode_title)

    def test_set_title_empty_string(self) -> None:
        """Test setting empty string as title."""
        from provide.foundation.cli.commands.process import _set_title_impl

        with (
            patch(
                "provide.foundation.cli.commands.process.has_setproctitle",
                return_value=True,
            ),
            patch("provide.foundation.cli.commands.process.set_process_title") as mock_set,
            patch("provide.foundation.cli.commands.process.pout"),
        ):
            _set_title_impl("")

            mock_set.assert_called_once_with("")

    def test_get_title_returns_none(self) -> None:
        """Test get-title when process title is None."""
        from provide.foundation.cli.commands.process import _get_title_impl

        with (
            patch(
                "provide.foundation.cli.commands.process.has_setproctitle",
                return_value=True,
            ),
            patch(
                "provide.foundation.cli.commands.process.get_process_title",
                return_value=None,
            ),
            patch("provide.foundation.cli.commands.process.pout") as mock_pout,
        ):
            _get_title_impl()

            mock_pout.assert_called_once_with("Current process title: None")


class TestProcessCommandsIntegration(FoundationTestCase):
    """Integration tests for process commands with actual functions."""

    def test_set_and_get_title_flow(self) -> None:
        """Test the flow of setting and getting process title."""
        from provide.foundation.cli.commands.process import (
            _get_title_impl,
            _set_title_impl,
        )

        with (
            patch(
                "provide.foundation.cli.commands.process.has_setproctitle",
                return_value=True,
            ),
            patch("provide.foundation.cli.commands.process.set_process_title") as mock_set,
            patch(
                "provide.foundation.cli.commands.process.get_process_title",
                return_value="integration-test",
            ) as mock_get,
            patch("provide.foundation.cli.commands.process.pout") as mock_pout,
        ):
            # Set title
            _set_title_impl("integration-test")
            mock_set.assert_called_once_with("integration-test")

            # Get title
            _get_title_impl()
            mock_get.assert_called_once()

            # Verify output - only get_title outputs to user
            mock_pout.assert_called_once_with("Current process title: integration-test")


# 🧱🏗️🔚
