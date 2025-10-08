from __future__ import annotations

import itertools
from typing import Any
from unittest.mock import MagicMock, patch

from click.testing import CliRunner
import pytest

from provide.foundation.cli.commands.logs.generate import generate_logs_command


@pytest.fixture
def runner() -> CliRunner:
    """Provides a Click CLI runner for testing."""
    return CliRunner()


@patch("provide.foundation.cli.commands.logs.generate._HAS_CLICK", True)
class TestGenerateLogsCommand:
    """Tests for the generate_logs_command Click command."""

    @patch("provide.foundation.cli.commands.logs.generate.click.echo")
    @patch("provide.foundation.cli.commands.logs.generate._generate_fixed_count_logs")
    @patch("provide.foundation.cli.commands.logs.generate._print_final_stats")
    def test_generate_fixed_count_logs(
        self,
        mock_print_final_stats: MagicMock,
        mock_generate_fixed_count: MagicMock,
        mock_echo: MagicMock,
        runner: CliRunner,
    ) -> None:
        """Test that the command calls the fixed-count generator."""
        mock_generate_fixed_count.return_value = (10, 0, 0)
        result = runner.invoke(generate_logs_command, ["--count", "10", "--rate", "0"])

        assert result.exit_code == 0
        mock_generate_fixed_count.assert_called_once_with(10, 0.0, "normal", 0.1)
        mock_print_final_stats.assert_called_once()

    @patch("provide.foundation.cli.commands.logs.generate.click.echo")
    @patch("provide.foundation.cli.commands.logs.generate._generate_continuous_logs")
    @patch("provide.foundation.cli.commands.logs.generate._print_final_stats")
    def test_generate_continuous_logs(
        self,
        mock_print_final_stats: MagicMock,
        mock_generate_continuous: MagicMock,
        mock_echo: MagicMock,
        runner: CliRunner,
    ) -> None:
        """Test that the command calls the continuous generator and handles KeyboardInterrupt."""
        mock_generate_continuous.side_effect = KeyboardInterrupt
        result = runner.invoke(generate_logs_command, ["--count", "0"])

        assert result.exit_code == 0
        # Verify the interrupt message was echoed (includes emoji and newlines)
        mock_echo.assert_any_call("\n\n⛔ Generation interrupted by user")
        mock_generate_continuous.assert_called_once()
        mock_print_final_stats.assert_called_once()

    @patch("provide.foundation.cli.commands.logs.generate.click.echo")
    @patch("provide.foundation.cli.commands.logs.generate.time.sleep")
    @patch("provide.foundation.cli.commands.logs.generate._send_log_entry")
    def test_generate_fixed_count_logs_implementation(
        self,
        mock_send_log_entry: MagicMock,
        mock_sleep: MagicMock,
        mock_echo: MagicMock,
        runner: CliRunner,
    ) -> None:
        """Test the implementation of the fixed-count log generation."""

        def send_log_entry_side_effect(
            entry: dict[str, Any], logs_sent: int, logs_failed: int, logs_rate_limited: int
        ) -> tuple[int, int, int]:
            return logs_sent + 1, logs_failed, logs_rate_limited

        mock_send_log_entry.side_effect = send_log_entry_side_effect

        result = runner.invoke(
            generate_logs_command,
            ["--count", "5", "--rate", "10"],
        )

        assert result.exit_code == 0
        assert mock_send_log_entry.call_count == 5
        mock_sleep.assert_called_with(0.1)

        # Check that echo was called with expected messages
        echo_calls = [str(call) for call in mock_echo.call_args_list]
        assert any("Generation complete" in str(call) for call in echo_calls)
        assert any("Total sent: 5 logs" in str(call) for call in echo_calls)

    @patch("provide.foundation.cli.commands.logs.generate.click.echo")
    @patch("provide.foundation.cli.commands.logs.generate.time.time")
    @patch("provide.foundation.cli.commands.logs.generate.time.sleep")
    @patch("provide.foundation.cli.commands.logs.generate._send_log_entry")
    @patch("provide.foundation.cli.commands.logs.generate._print_stats")
    def test_generate_continuous_logs_implementation(
        self,
        mock_print_stats: MagicMock,
        mock_send_log_entry: MagicMock,
        mock_sleep: MagicMock,
        mock_time: MagicMock,
        mock_echo: MagicMock,
        runner: CliRunner,
    ) -> None:
        """Test the implementation of continuous log generation."""

        call_counter = {"count": 0}

        def send_log_entry_side_effect(
            entry: dict[str, Any], logs_sent: int, logs_failed: int, logs_rate_limited: int
        ) -> tuple[int, int, int]:
            call_counter["count"] += 1
            if call_counter["count"] >= 3:
                raise KeyboardInterrupt
            return logs_sent + 1, logs_failed, logs_rate_limited

        mock_send_log_entry.side_effect = send_log_entry_side_effect
        mock_time.side_effect = itertools.count(start=0, step=1.0)

        def print_stats_side_effect(
            current_time: float,
            last_stats_time: float,
            logs_sent: int,
            last_stats_sent: int,
            logs_failed: int,
            enable_rate_limit: bool,
            logs_rate_limited: int,
        ) -> tuple[float, int]:
            return current_time, logs_sent

        mock_print_stats.side_effect = print_stats_side_effect

        result = runner.invoke(
            generate_logs_command,
            ["--count", "0", "--rate", "1"],
        )

        assert result.exit_code == 0
        assert mock_send_log_entry.call_count == 3

        # Check that echo was called with the interrupt message
        echo_calls = [str(call) for call in mock_echo.call_args_list]
        assert any("Generation interrupted by user" in str(call) for call in echo_calls)

    @patch("provide.foundation.cli.commands.logs.generate.click.echo")
    @patch("provide.foundation.cli.commands.logs.generate._send_log_entry")
    @patch("provide.foundation.cli.commands.logs.generate._configure_rate_limiter")
    def test_rate_limit_options(
        self,
        mock_configure_limiter: MagicMock,
        mock_send_log_entry: MagicMock,
        mock_echo: MagicMock,
        runner: CliRunner,
    ) -> None:
        """Test that rate limiting options are correctly passed."""
        # Mock send_log_entry to prevent actual logging
        mock_send_log_entry.return_value = (1, 0, 0)

        runner.invoke(
            generate_logs_command,
            ["--count", "1", "--enable-rate-limit", "--rate-limit", "50"],
        )
        mock_configure_limiter.assert_called_once_with(True, 50.0)


def test_generate_command_raises_importerror_if_click_is_missing() -> None:
    """Test that generate_logs_command stub raises ImportError if Click is not installed.

    Note: This test can only verify the stub exists. The actual Click import check
    happens at module load time, so we cannot properly test Click being missing
    when Click is actually installed in the test environment.
    """
    from provide.foundation.cli.commands.logs import generate

    # Verify the module has the _HAS_CLICK flag
    assert hasattr(generate, "_HAS_CLICK")

    # Verify it's True in our test environment (Click is installed)
    assert generate._HAS_CLICK is True

    # The else branch (stub function) cannot be tested when Click is installed,
    # as it's defined at module load time based on import success
