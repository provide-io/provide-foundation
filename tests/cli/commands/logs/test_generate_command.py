#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#


from __future__ import annotations

import itertools
from typing import Any

from click.testing import CliRunner
from provide.testkit.mocking import MagicMock, patch
import pytest

from provide.foundation.cli.commands.logs.generate import generate_logs_command


@pytest.fixture
def runner() -> CliRunner:
    """Provides a Click CLI runner for testing."""
    return CliRunner()


class TestGenerateLogsCommand:
    """Tests for the generate_logs_command Click command."""

    @patch("provide.foundation.cli.commands.logs.generate.print_generation_config")
    @patch("provide.foundation.cli.commands.logs.generate._configure_rate_limiter")
    @patch("provide.foundation.cli.commands.logs.generator.LogGenerator.generate_fixed_count")
    @patch("provide.foundation.cli.commands.logs.generate.print_final_stats")
    @patch("provide.foundation.logger.processors.otlp.flush_otlp_logs")
    def test_generate_fixed_count_logs(
        self,
        mock_flush_otlp: MagicMock,
        mock_print_final_stats: MagicMock,
        mock_generate_fixed_count: MagicMock,
        mock_configure_limiter: MagicMock,
        mock_print_config: MagicMock,
        runner: CliRunner,
    ) -> None:
        """Test that the command calls the fixed-count generator."""
        mock_generate_fixed_count.return_value = (10, 0, 0)
        result = runner.invoke(
            generate_logs_command,
            ["--count", "10", "--rate", "0"],
            catch_exceptions=False,
            standalone_mode=False,
        )

        assert result.exit_code == 0
        mock_generate_fixed_count.assert_called_once_with(10, 0.0)
        mock_print_final_stats.assert_called_once()

    @patch("provide.foundation.cli.commands.logs.generate.print_generation_config")
    @patch("provide.foundation.cli.commands.logs.generate._configure_rate_limiter")
    @patch("provide.foundation.cli.commands.logs.generator.LogGenerator.generate_continuous")
    @patch("provide.foundation.cli.commands.logs.generate.print_final_stats")
    @patch("provide.foundation.cli.commands.logs.generate.click.echo")
    @patch("provide.foundation.logger.processors.otlp.flush_otlp_logs")
    def test_generate_continuous_logs(
        self,
        mock_flush_otlp: MagicMock,
        mock_echo: MagicMock,
        mock_print_final_stats: MagicMock,
        mock_generate_continuous: MagicMock,
        mock_configure_limiter: MagicMock,
        mock_print_config: MagicMock,
        runner: CliRunner,
    ) -> None:
        """Test that the command calls the continuous generator and handles KeyboardInterrupt."""
        mock_generate_continuous.side_effect = KeyboardInterrupt
        result = runner.invoke(
            generate_logs_command, ["--count", "0"], catch_exceptions=False, standalone_mode=False
        )

        assert result.exit_code == 0
        # Verify the interrupt message was echoed (includes emoji and newlines)
        mock_echo.assert_any_call("\n\n⛔ Generation interrupted by user")
        mock_generate_continuous.assert_called_once()
        mock_print_final_stats.assert_called_once()

    @patch("provide.foundation.cli.commands.logs.stats.click.echo")
    @patch("provide.foundation.cli.commands.logs.generator.time.sleep")
    @patch("provide.foundation.cli.commands.logs.generator.LogGenerator.send_log_entry")
    @patch("provide.foundation.logger.processors.otlp.flush_otlp_logs")
    def test_generate_fixed_count_logs_implementation(
        self,
        mock_flush_otlp: MagicMock,
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

    @patch("provide.foundation.cli.commands.logs.stats.click.echo")
    @patch("provide.foundation.cli.commands.logs.generator.time.time")
    @patch("provide.foundation.cli.commands.logs.generator.time.sleep")
    @patch("provide.foundation.cli.commands.logs.generator.LogGenerator.send_log_entry")
    @patch("provide.foundation.cli.commands.logs.stats.print_stats")
    @patch("provide.foundation.logger.processors.otlp.flush_otlp_logs")
    def test_generate_continuous_logs_implementation(
        self,
        mock_flush_otlp: MagicMock,
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

    @patch("provide.foundation.cli.commands.logs.stats.click.echo")
    @patch("provide.foundation.cli.commands.logs.generator.LogGenerator.send_log_entry")
    @patch("provide.foundation.cli.commands.logs.generate._configure_rate_limiter")
    @patch("provide.foundation.logger.processors.otlp.flush_otlp_logs")
    def test_rate_limit_options(
        self,
        mock_flush_otlp: MagicMock,
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


# 🧱🏗️🔚
