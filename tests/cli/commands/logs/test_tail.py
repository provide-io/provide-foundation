#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#


from __future__ import annotations

from click.testing import CliRunner
from provide.testkit.mocking import MagicMock, patch
import pytest

from provide.foundation.cli.commands.logs.tail import (
    _parse_filter_string_for_tail,
    tail_command,
)


@pytest.fixture
def runner() -> CliRunner:
    """Provides a Click CLI runner for testing."""
    return CliRunner()


class TestParseFilterString:
    """Tests for the _parse_filter_string_for_tail function."""

    def test_parse_valid_filter(self) -> None:
        """Test parsing of a valid filter string."""
        filter_str = "level='ERROR', service='api'"
        expected = {"level": "ERROR", "service": "api"}
        assert _parse_filter_string_for_tail(filter_str) == expected

    def test_parse_empty_and_none_filter(self) -> None:
        """Test parsing of empty and None filter strings."""
        assert _parse_filter_string_for_tail("") == {}
        assert _parse_filter_string_for_tail(None) == {}

    def test_parse_with_extra_whitespace(self) -> None:
        """Test parsing with varied whitespace and quote types."""
        filter_str = "  key = 'value' ,  another = \"value2\"  "
        expected = {"key": "value", "another": "value2"}
        assert _parse_filter_string_for_tail(filter_str) == expected

    def test_parse_malformed_filter_ignores_invalid_parts(self) -> None:
        """Test that malformed parts of a filter string are ignored."""
        filter_str = "key='value', malformed, another='value2'"
        expected = {"key": "value", "another": "value2"}
        assert _parse_filter_string_for_tail(filter_str) == expected


class TestTailCommand:
    """Tests for the tail_command Click command."""

    @patch("provide.foundation.integrations.openobserve.tail_logs")
    @patch("provide.foundation.integrations.openobserve.format_output")
    def test_tail_logs_success(
        self,
        mock_format_output: MagicMock,
        mock_tail_logs: MagicMock,
        runner: CliRunner,
    ) -> None:
        """Test successful log tailing with default options."""
        mock_client = MagicMock()
        mock_tail_logs.return_value = [{"message": "log1"}, {"message": "log2"}]
        mock_format_output.side_effect = lambda log_entry, format_type: log_entry["message"]

        result = runner.invoke(tail_command, obj={"client": mock_client})

        assert result.exit_code == 0
        assert "Tailing logs" in result.output
        assert "log1" in result.output
        assert "log2" in result.output
        mock_tail_logs.assert_called_once_with(
            stream="default",
            filters={},
            follow=True,
            lines=10,
            client=mock_client,
        )
        assert mock_format_output.call_count == 2

    @patch("provide.foundation.integrations.openobserve.tail_logs")
    def test_tail_logs_no_client_configured(
        self,
        mock_tail_logs: MagicMock,
        runner: CliRunner,
    ) -> None:
        """Test that the command fails gracefully if no client is configured."""
        result = runner.invoke(tail_command, obj={})

        assert result.exit_code == 1
        assert "Error: OpenObserve not configured" in result.output
        mock_tail_logs.assert_not_called()

    @patch("provide.foundation.integrations.openobserve.tail_logs")
    def test_tail_logs_keyboard_interrupt_handling(
        self,
        mock_tail_logs: MagicMock,
        runner: CliRunner,
    ) -> None:
        """Test graceful handling of KeyboardInterrupt."""
        mock_client = MagicMock()
        mock_tail_logs.side_effect = KeyboardInterrupt

        result = runner.invoke(tail_command, obj={"client": mock_client})

        assert result.exit_code == 0
        assert "Stopped tailing logs" in result.output

    @patch("provide.foundation.integrations.openobserve.tail_logs")
    def test_tail_logs_generic_exception_handling(
        self,
        mock_tail_logs: MagicMock,
        runner: CliRunner,
    ) -> None:
        """Test graceful handling of generic exceptions."""
        mock_client = MagicMock()
        mock_tail_logs.side_effect = Exception("Something went wrong")

        result = runner.invoke(tail_command, obj={"client": mock_client})

        assert result.exit_code == 1
        assert "Tail failed: Something went wrong" in result.output

    @patch("provide.foundation.integrations.openobserve.tail_logs")
    def test_tail_logs_with_all_options(
        self,
        mock_tail_logs: MagicMock,
        runner: CliRunner,
    ) -> None:
        """Test that all command-line options are passed correctly."""
        mock_client = MagicMock()
        mock_tail_logs.return_value = []

        runner.invoke(
            tail_command,
            [
                "--stream",
                "my-stream",
                "--filter",
                "level='DEBUG'",
                "--lines",
                "50",
                "--no-follow",
                "--format",
                "json",
            ],
            obj={"client": mock_client},
        )

        mock_tail_logs.assert_called_once_with(
            stream="my-stream",
            filters={"level": "DEBUG"},
            follow=False,
            lines=50,
            client=mock_client,
        )


# 🧱🏗️🔚
