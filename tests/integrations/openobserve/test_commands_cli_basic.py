#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Unit tests for OpenObserve CLI commands.

Tests all CLI command functionality with mocked dependencies.
Requires click to be installed."""

from __future__ import annotations

from provide.testkit import FoundationTestCase
from provide.testkit.mocking import MagicMock, patch

# Import _HAS_CLICK to check if click is available
try:
    from provide.foundation.integrations.openobserve.commands import _HAS_CLICK
except ImportError:
    _HAS_CLICK = False

# Only test CLI commands if click is available
if _HAS_CLICK:
    from click.testing import CliRunner

    from provide.foundation.integrations.openobserve.commands import openobserve_group


if _HAS_CLICK:
    from provide.foundation.integrations.openobserve.commands import openobserve_group

    class TestOpenObserveGroupCommand(FoundationTestCase):
        """Tests for openobserve CLI group command."""

        def test_openobserve_group_initialization_success(self) -> None:
            """Test openobserve group initializes client successfully."""
            runner = CliRunner()

            with patch(
                "provide.foundation.integrations.openobserve.commands.OpenObserveClient.from_config"
            ) as mock_from_config:
                mock_client = MagicMock()
                mock_from_config.return_value = mock_client

                result = runner.invoke(openobserve_group, ["--help"])

                assert result.exit_code == 0
                assert "Query and manage OpenObserve logs" in result.output

        def test_openobserve_group_initialization_failure(self) -> None:
            """Test openobserve group handles client initialization failure."""
            runner = CliRunner()

            with patch(
                "provide.foundation.integrations.openobserve.commands.OpenObserveClient.from_config"
            ) as mock_from_config:
                mock_from_config.side_effect = ValueError("Config error")

                # Help should still work even if client init fails
                result = runner.invoke(openobserve_group, ["--help"])
                assert result.exit_code == 0

    class TestQueryCommand(FoundationTestCase):
        """Tests for query command."""

        def test_query_command_success(self) -> None:
            """Test successful query execution."""
            runner = CliRunner()

            mock_client = MagicMock()
            mock_response = MagicMock()
            mock_response.hits = [{"message": "test log"}]
            mock_response.total = 1

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
                    return_value="formatted output",
                ),
            ):
                result = runner.invoke(
                    openobserve_group,
                    ["query", "--sql", "SELECT * FROM logs"],
                )

                assert result.exit_code == 0
                assert "formatted output" in result.output

        def test_query_command_no_client(self) -> None:
            """Test query command when client is not configured."""
            runner = CliRunner()

            with patch(
                "provide.foundation.integrations.openobserve.commands.OpenObserveClient.from_config"
            ) as mock_from_config:
                mock_from_config.side_effect = ValueError("Config error")

                result = runner.invoke(
                    openobserve_group,
                    ["query", "--sql", "SELECT * FROM logs"],
                )

                assert result.exit_code == 1
                assert "not configured" in result.output

        def test_query_command_failure(self) -> None:
            """Test query command when query fails."""
            runner = CliRunner()

            mock_client = MagicMock()

            with (
                patch(
                    "provide.foundation.integrations.openobserve.commands.OpenObserveClient.from_config",
                    return_value=mock_client,
                ),
                patch("provide.foundation.integrations.openobserve.commands.run_async") as mock_run_async,
            ):
                mock_run_async.side_effect = ValueError("Query failed")

                result = runner.invoke(
                    openobserve_group,
                    ["query", "--sql", "SELECT * FROM logs"],
                )

                assert result.exit_code == 1
                assert "Query failed" in result.output

    class TestTailCommand(FoundationTestCase):
        """Tests for tail command."""

        def test_tail_command_success(self) -> None:
            """Test successful tail execution."""
            runner = CliRunner()

            mock_client = MagicMock()

            def mock_tail_logs(*args: object, **kwargs: object) -> list[dict]:
                return [{"message": "log1"}, {"message": "log2"}]

            with (
                patch(
                    "provide.foundation.integrations.openobserve.commands.OpenObserveClient.from_config",
                    return_value=mock_client,
                ),
                patch(
                    "provide.foundation.integrations.openobserve.commands.tail_logs",
                    side_effect=mock_tail_logs,
                ),
            ):
                result = runner.invoke(
                    openobserve_group,
                    ["tail", "--stream", "default", "--follow=False"],
                )

                assert result.exit_code == 0

        def test_tail_command_with_filter(self) -> None:
            """Test tail command with filter."""
            runner = CliRunner()

            mock_client = MagicMock()

            def mock_tail_logs(*args: object, **kwargs: object) -> list[dict]:
                return []

            with (
                patch(
                    "provide.foundation.integrations.openobserve.commands.OpenObserveClient.from_config",
                    return_value=mock_client,
                ),
                patch(
                    "provide.foundation.integrations.openobserve.commands.tail_logs",
                    side_effect=mock_tail_logs,
                ),
            ):
                result = runner.invoke(
                    openobserve_group,
                    [
                        "tail",
                        "--stream",
                        "default",
                        "--filter",
                        "level=ERROR",
                        "--follow=False",
                    ],
                )

                assert result.exit_code == 0

        def test_tail_command_keyboard_interrupt(self) -> None:
            """Test tail command handles keyboard interrupt."""
            runner = CliRunner()

            mock_client = MagicMock()

            def mock_tail_logs(*args: object, **kwargs: object) -> None:
                raise KeyboardInterrupt()
                if False:  # Make it a generator
                    yield {}

            with (
                patch(
                    "provide.foundation.integrations.openobserve.commands.OpenObserveClient.from_config",
                    return_value=mock_client,
                ),
                patch(
                    "provide.foundation.integrations.openobserve.commands.tail_logs",
                    side_effect=mock_tail_logs,
                ),
            ):
                result = runner.invoke(
                    openobserve_group,
                    ["tail", "--stream", "default"],
                )

                assert result.exit_code == 0
                assert "Stopped tailing" in result.output

# 🧱🏗️🔚
