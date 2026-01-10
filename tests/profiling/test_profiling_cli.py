#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for profiling CLI commands."""

from __future__ import annotations

from provide.testkit import FoundationTestCase
from provide.testkit.mocking import Mock, patch

from provide.foundation.context import CLIContext


class TestProfilingCLI(FoundationTestCase):
    """Test profiling CLI functionality."""

    @patch("provide.foundation.profiling.cli.get_hub")
    @patch("provide.foundation.profiling.cli.perr")
    def test_show_profile_metrics_no_profiler_text_mode(self, mock_perr: Mock, mock_get_hub: Mock) -> None:
        """Test profiling output when profiler not enabled in text mode."""
        # Setup: No profiler available
        mock_hub = mock_get_hub.return_value
        mock_hub.get_component.return_value = None

        # Create context in text mode (not JSON)
        ctx = CLIContext(json_output=False)

        from provide.foundation.profiling.cli import show_profile_metrics

        show_profile_metrics(ctx)

        # Verify perr was called with context (enables proper JSON handling)
        assert mock_perr.call_count == 2
        # Check that ctx was passed to both calls
        assert mock_perr.call_args_list[0].kwargs.get("ctx") == ctx
        assert mock_perr.call_args_list[1].kwargs.get("ctx") == ctx
        # Verify color was specified for text mode
        assert mock_perr.call_args_list[0].kwargs.get("color") == "red"
        assert mock_perr.call_args_list[1].kwargs.get("color") == "yellow"

    @patch("provide.foundation.profiling.cli.get_hub")
    @patch("provide.foundation.profiling.cli.perr")
    def test_show_profile_metrics_no_profiler_json_mode(self, mock_perr: Mock, mock_get_hub: Mock) -> None:
        """Test profiling output when profiler not enabled in JSON mode."""
        # Setup: No profiler available
        mock_hub = mock_get_hub.return_value
        mock_hub.get_component.return_value = None

        # Create context in JSON mode
        ctx = CLIContext(json_output=True)

        from provide.foundation.profiling.cli import show_profile_metrics

        show_profile_metrics(ctx)

        # Verify perr was called with context
        assert mock_perr.call_count == 2
        # Check that ctx was passed - this allows perr to suppress colors in JSON mode
        assert mock_perr.call_args_list[0].kwargs.get("ctx") == ctx
        assert mock_perr.call_args_list[1].kwargs.get("ctx") == ctx

    @patch("provide.foundation.profiling.cli.get_hub")
    @patch("provide.foundation.profiling.cli.pout")
    @patch("provide.foundation.profiling.cli.perr")
    def test_show_profile_metrics_with_profiler_text_mode(
        self, mock_perr: Mock, mock_pout: Mock, mock_get_hub: Mock
    ) -> None:
        """Test profiling output with profiler enabled in text mode."""
        # Setup: Profiler available with mock metrics
        mock_profiler = Mock()
        mock_profiler.enabled = True
        mock_profiler.processor = Mock()
        mock_profiler.processor.sample_rate = 1.0

        mock_metrics = Mock()
        mock_metrics.messages_per_second = 14523.0
        mock_metrics.avg_latency_ms = 0.07
        mock_metrics.emoji_overhead_percent = 3.2
        mock_metrics.message_count = 10000
        mock_metrics.emoji_message_count = 5000
        mock_metrics.avg_fields_per_message = 3.5
        mock_metrics.dropped_count = 0
        mock_metrics.to_dict.return_value = {"uptime_seconds": 45.0}

        mock_profiler.get_metrics.return_value = mock_metrics
        mock_hub = mock_get_hub.return_value
        mock_hub.get_component.return_value = mock_profiler

        ctx = CLIContext(json_output=False)

        from provide.foundation.profiling.cli import show_profile_metrics

        show_profile_metrics(ctx)

        # Verify pout was called multiple times for output
        assert mock_pout.call_count > 0

    @patch("provide.foundation.profiling.cli.get_hub")
    @patch("provide.foundation.profiling.cli.pout")
    def test_show_profile_metrics_with_profiler_json_mode(self, mock_pout: Mock, mock_get_hub: Mock) -> None:
        """Test profiling output with profiler enabled in JSON mode."""
        # Setup: Profiler available with mock metrics
        mock_profiler = Mock()
        mock_metrics = Mock()
        mock_metrics.to_dict.return_value = {
            "messages_per_second": 14523.0,
            "avg_latency_ms": 0.07,
            "emoji_overhead_percent": 3.2,
        }

        mock_profiler.get_metrics.return_value = mock_metrics
        mock_hub = mock_get_hub.return_value
        mock_hub.get_component.return_value = mock_profiler

        ctx = CLIContext(json_output=True)

        from provide.foundation.profiling.cli import show_profile_metrics

        show_profile_metrics(ctx)

        # In JSON mode, should call pout with json_key
        assert mock_pout.call_count > 0
        # Verify first call has json_key="metrics"
        assert mock_pout.call_args_list[0].kwargs.get("json_key") == "metrics"


# 🧱🏗️🔚
