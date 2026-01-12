#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for OpenObserve CLI advanced commands."""

from __future__ import annotations

from provide.testkit import FoundationTestCase
from provide.testkit.mocking import MagicMock, patch

try:
    from provide.foundation.integrations.openobserve.commands import _HAS_CLICK
except ImportError:
    _HAS_CLICK = False

if _HAS_CLICK:
    from click.testing import CliRunner

    from provide.foundation.integrations.openobserve.commands import openobserve_group

    class TestErrorsCommand(FoundationTestCase):
        """Tests for errors command."""

        def test_errors_command_success(self) -> None:
            """Test successful errors search."""
            runner = CliRunner()

            mock_client = MagicMock()
            mock_response = MagicMock()
            mock_response.total = 5

            with (
                patch(
                    "provide.foundation.integrations.openobserve.commands.OpenObserveClient.from_config",
                    return_value=mock_client,
                ),
                patch(
                    "provide.foundation.integrations.openobserve.commands.run_async",
                    return_value=mock_response,
                ),
                patch(
                    "provide.foundation.integrations.openobserve.commands.format_output",
                    return_value="error logs",
                ),
            ):
                result = runner.invoke(openobserve_group, ["errors"])

                assert result.exit_code == 0

        def test_errors_command_no_errors(self) -> None:
            """Test errors command when no errors found."""
            runner = CliRunner()

            mock_client = MagicMock()
            mock_response = MagicMock()
            mock_response.total = 0

            with (
                patch(
                    "provide.foundation.integrations.openobserve.commands.OpenObserveClient.from_config",
                    return_value=mock_client,
                ),
                patch(
                    "provide.foundation.integrations.openobserve.commands.run_async",
                    return_value=mock_response,
                ),
            ):
                result = runner.invoke(openobserve_group, ["errors"])

                assert result.exit_code == 0
                assert "No errors found" in result.output

    class TestTraceCommand(FoundationTestCase):
        """Tests for trace command."""

        def test_trace_command_success(self) -> None:
            """Test successful trace search."""
            runner = CliRunner()

            mock_client = MagicMock()
            mock_response = MagicMock()
            mock_response.total = 3

            with (
                patch(
                    "provide.foundation.integrations.openobserve.commands.OpenObserveClient.from_config",
                    return_value=mock_client,
                ),
                patch(
                    "provide.foundation.integrations.openobserve.commands.run_async",
                    return_value=mock_response,
                ),
                patch(
                    "provide.foundation.integrations.openobserve.commands.format_output",
                    return_value="trace logs",
                ),
            ):
                result = runner.invoke(
                    openobserve_group,
                    ["trace", "abc123"],
                )

                assert result.exit_code == 0

        def test_trace_command_not_found(self) -> None:
            """Test trace command when trace not found."""
            runner = CliRunner()

            mock_client = MagicMock()
            mock_response = MagicMock()
            mock_response.total = 0

            with (
                patch(
                    "provide.foundation.integrations.openobserve.commands.OpenObserveClient.from_config",
                    return_value=mock_client,
                ),
                patch(
                    "provide.foundation.integrations.openobserve.commands.run_async",
                    return_value=mock_response,
                ),
            ):
                result = runner.invoke(
                    openobserve_group,
                    ["trace", "abc123"],
                )

                assert result.exit_code == 0
                assert "No logs found" in result.output


else:
    # Placeholder when click is not available
    class TestCommandsNotAvailable(FoundationTestCase):
        """Test that commands are not available when click is missing."""

        def test_commands_require_click(self) -> None:
            """Test that click is required for CLI commands."""
            # Just verify that the module doesn't crash without click
            assert not _HAS_CLICK


__all__: list[str] = []

# 🧱🏗️🔚
