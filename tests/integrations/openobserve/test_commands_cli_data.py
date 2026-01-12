#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for OpenObserve CLI data commands."""

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

    class TestStreamsCommand(FoundationTestCase):
        """Tests for streams command."""

        def test_streams_command_success(self) -> None:
            """Test successful streams listing."""
            runner = CliRunner()

            mock_client = MagicMock()
            mock_stream = MagicMock()
            mock_stream.name = "test_stream"
            mock_stream.stream_type = "logs"
            mock_stream.doc_count = 100
            mock_stream.original_size = 1024

            with (
                patch(
                    "provide.foundation.integrations.openobserve.commands.OpenObserveClient.from_config",
                    return_value=mock_client,
                ),
                patch(
                    "provide.foundation.integrations.openobserve.commands.run_async",
                    return_value=[mock_stream],
                ),
            ):
                result = runner.invoke(openobserve_group, ["streams"])

                assert result.exit_code == 0
                assert "Available streams" in result.output
                assert "test_stream" in result.output

        def test_streams_command_no_streams(self) -> None:
            """Test streams command when no streams exist."""
            runner = CliRunner()

            mock_client = MagicMock()

            with (
                patch(
                    "provide.foundation.integrations.openobserve.commands.OpenObserveClient.from_config",
                    return_value=mock_client,
                ),
                patch(
                    "provide.foundation.integrations.openobserve.commands.run_async",
                    return_value=[],
                ),
            ):
                result = runner.invoke(openobserve_group, ["streams"])

                assert result.exit_code == 0
                assert "No streams found" in result.output

    class TestTestCommand(FoundationTestCase):
        """Tests for test command."""

        def test_test_command_success(self) -> None:
            """Test successful connection test."""
            runner = CliRunner()

            mock_client = MagicMock()
            mock_client.url = "http://localhost:5080"
            mock_client.organization = "default"
            mock_client.username = "test@example.com"

            with (
                patch(
                    "provide.foundation.integrations.openobserve.commands.OpenObserveClient.from_config",
                    return_value=mock_client,
                ),
                patch(
                    "provide.foundation.integrations.openobserve.commands.run_async",
                    return_value=True,
                ),
            ):
                result = runner.invoke(openobserve_group, ["test"])

                assert result.exit_code == 0
                assert "Connection successful" in result.output

        def test_test_command_failure(self) -> None:
            """Test failed connection test."""
            runner = CliRunner()

            mock_client = MagicMock()
            mock_client.url = "http://localhost:5080"

            with (
                patch(
                    "provide.foundation.integrations.openobserve.commands.OpenObserveClient.from_config",
                    return_value=mock_client,
                ),
                patch(
                    "provide.foundation.integrations.openobserve.commands.run_async",
                    return_value=False,
                ),
            ):
                result = runner.invoke(openobserve_group, ["test"])

                assert result.exit_code == 1
                assert "Connection failed" in result.output

    class TestHistoryCommand(FoundationTestCase):
        """Tests for history command."""

        def test_history_command_success(self) -> None:
            """Test successful history retrieval."""
            runner = CliRunner()

            mock_client = MagicMock()
            mock_response = MagicMock()
            mock_response.total = 2
            mock_response.hits = [
                {"sql": "SELECT * FROM logs", "took": 10.5, "scan_records": 100},
                {"sql": "SELECT * FROM errors", "took": 5.2, "scan_records": 50},
            ]

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
                result = runner.invoke(openobserve_group, ["history"])

                assert result.exit_code == 0
                assert "Search history" in result.output

        def test_history_command_no_history(self) -> None:
            """Test history command when no history exists."""
            runner = CliRunner()

            mock_client = MagicMock()
            mock_response = MagicMock()
            mock_response.total = 0
            mock_response.hits = []

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
                result = runner.invoke(openobserve_group, ["history"])

                assert result.exit_code == 0
                assert "No search history found" in result.output

# 🧱🏗️🔚
