#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for basic CLI utility functions."""

from __future__ import annotations

import os

from provide.testkit import FoundationTestCase
from provide.testkit.mocking import MagicMock, patch
import pytest

from provide.foundation.cli.utils import (
    assert_cli_error,
    assert_cli_success,
    create_cli_context,
    echo_error,
    echo_info,
    echo_json,
    echo_success,
    echo_warning,
    setup_cli_logging,
)
from provide.foundation.context import CLIContext
from provide.foundation.logger import TelemetryConfig


class TestCliEchoFunctions(FoundationTestCase):
    """Test CLI echo functions."""

    @patch("provide.foundation.cli.utils.pout")
    def test_echo_json(self, mock_pout: MagicMock) -> None:
        """Test JSON output."""
        data = {"key": "value", "number": 42}
        echo_json(data)
        mock_pout.assert_called_once_with(data)

    @patch("provide.foundation.cli.utils.perr")
    def test_echo_error_text(self, mock_perr: MagicMock) -> None:
        """Test error message output."""
        echo_error("Something went wrong")
        mock_perr.assert_called_once()
        call_args = mock_perr.call_args
        assert "Something went wrong" in call_args[0][0]
        assert call_args[1]["color"] == "red"

    @patch("provide.foundation.cli.utils.perr")
    def test_echo_error_json(self, mock_perr: MagicMock) -> None:
        """Test error message as JSON."""
        echo_error("Something went wrong", json_output=True)
        mock_perr.assert_called_once()
        call_args = mock_perr.call_args
        assert call_args[0][0] == "Something went wrong"
        assert call_args[1]["json_key"] == "error"

    @patch("provide.foundation.cli.utils.pout")
    def test_echo_success_text(self, mock_pout: MagicMock) -> None:
        """Test success message output."""
        echo_success("Operation completed")
        mock_pout.assert_called_once()
        call_args = mock_pout.call_args
        assert "Operation completed" in call_args[0][0]
        assert call_args[1]["color"] == "green"

    @patch("provide.foundation.cli.utils.pout")
    def test_echo_success_json(self, mock_pout: MagicMock) -> None:
        """Test success message as JSON."""
        echo_success("Operation completed", json_output=True)
        mock_pout.assert_called_once()
        call_args = mock_pout.call_args
        assert call_args[0][0] == "Operation completed"
        assert call_args[1]["json_key"] == "success"

    @patch("provide.foundation.cli.utils.perr")
    def test_echo_warning_text(self, mock_perr: MagicMock) -> None:
        """Test warning message output."""
        echo_warning("Be careful")
        mock_perr.assert_called_once()
        call_args = mock_perr.call_args
        assert "Be careful" in call_args[0][0]
        assert call_args[1]["color"] == "yellow"

    @patch("provide.foundation.cli.utils.pout")
    def test_echo_info_text(self, mock_pout: MagicMock) -> None:
        """Test info message output."""
        echo_info("FYI")
        mock_pout.assert_called_once()
        call_args = mock_pout.call_args
        assert "FYI" in call_args[0][0]


class TestCliContext(FoundationTestCase):
    """Test CLI context creation."""

    def test_create_cli_context_default(self) -> None:
        """Test creating default CLI context."""
        ctx = create_cli_context()
        assert isinstance(ctx, CLIContext)
        assert ctx.profile == "default"

    def test_create_cli_context_with_overrides(self) -> None:
        """Test creating CLI context with overrides."""
        ctx = create_cli_context(profile="myapp", debug=True)
        assert ctx.profile == "myapp"
        assert ctx.debug is True


class TestCliAssertions(FoundationTestCase):
    """Test CLI assertion helpers."""

    def test_assert_cli_success(self) -> None:
        """Test successful CLI result assertion."""
        result = MagicMock(exit_code=0, output="Success")
        assert_cli_success(result)
        assert_cli_success(result, "Success")

    def test_assert_cli_success_with_wrong_output(self) -> None:
        """Test CLI success assertion with wrong output."""
        result = MagicMock(exit_code=0, output="Actual output")
        with pytest.raises(AssertionError):
            assert_cli_success(result, "Expected output")

    def test_assert_cli_success_with_error_code(self) -> None:
        """Test CLI success assertion with error exit code."""
        result = MagicMock(exit_code=1, output="Error")
        with pytest.raises(AssertionError):
            assert_cli_success(result)

    def test_assert_cli_error(self) -> None:
        """Test CLI error assertion."""
        result = MagicMock(exit_code=1, output="Error occurred")
        assert_cli_error(result, exit_code=1)
        assert_cli_error(result, "Error occurred", exit_code=1)

    def test_assert_cli_error_with_wrong_code(self) -> None:
        """Test CLI error assertion with wrong exit code."""
        result = MagicMock(exit_code=1)
        with pytest.raises(AssertionError):
            assert_cli_error(result, exit_code=2)


class TestCliLogging(FoundationTestCase):
    """Test CLI logging setup."""

    @patch("provide.foundation.cli.utils.get_hub")
    def test_setup_cli_logging_default(self, mock_get_hub: MagicMock) -> None:
        """Test default CLI logging setup."""
        ctx = create_cli_context()
        setup_cli_logging(ctx)
        mock_hub = mock_get_hub.return_value
        mock_hub.initialize_foundation.assert_called_once()
        config_arg = mock_hub.initialize_foundation.call_args.kwargs["config"]
        assert isinstance(config_arg, TelemetryConfig)
        # Default context log level is INFO, unless overridden by environment
        expected_level = os.environ.get("PROVIDE_LOG_LEVEL", "INFO")
        assert config_arg.logging.default_level == expected_level
        assert config_arg.logging.console_formatter == "key_value"

    @patch("provide.foundation.cli.utils.get_hub")
    def test_setup_cli_logging_verbose(self, mock_get_hub: MagicMock) -> None:
        """Test verbose CLI logging setup."""
        ctx = create_cli_context(log_level="DEBUG")
        setup_cli_logging(ctx)
        mock_hub = mock_get_hub.return_value
        mock_hub.initialize_foundation.assert_called_once()
        config_arg = mock_hub.initialize_foundation.call_args.kwargs["config"]
        assert config_arg.logging.default_level == "DEBUG"

    @patch("provide.foundation.cli.utils.get_hub")
    def test_setup_cli_logging_quiet(self, mock_get_hub: MagicMock) -> None:
        """Test quiet CLI logging setup."""
        ctx = create_cli_context(log_level="ERROR")
        setup_cli_logging(ctx)
        mock_hub = mock_get_hub.return_value
        mock_hub.initialize_foundation.assert_called_once()
        config_arg = mock_hub.initialize_foundation.call_args.kwargs["config"]
        assert config_arg.logging.default_level == "ERROR"

    @patch("provide.foundation.cli.utils.get_hub")
    def test_setup_cli_logging_json(self, mock_get_hub: MagicMock) -> None:
        """Test JSON CLI logging setup."""
        ctx = create_cli_context(json_output=True)
        setup_cli_logging(ctx)
        mock_hub = mock_get_hub.return_value
        mock_hub.initialize_foundation.assert_called_once()
        config_arg = mock_hub.initialize_foundation.call_args.kwargs["config"]
        assert config_arg.logging.console_formatter == "json"

    @patch("provide.foundation.cli.utils.get_hub")
    def test_setup_cli_logging_reinit_true(self, mock_get_hub: MagicMock) -> None:
        """Test that reinit_logging=True forces reinitialization."""
        ctx = create_cli_context()
        setup_cli_logging(ctx, reinit_logging=True)
        mock_hub = mock_get_hub.return_value
        mock_hub.initialize_foundation.assert_called_once()
        # Verify force=True was passed
        assert mock_hub.initialize_foundation.call_args.kwargs["force"] is True

    @patch("provide.foundation.cli.utils.get_hub")
    def test_setup_cli_logging_reinit_false(self, mock_get_hub: MagicMock) -> None:
        """Test that reinit_logging=False skips reinitialization."""
        ctx = create_cli_context()
        setup_cli_logging(ctx, reinit_logging=False)
        mock_hub = mock_get_hub.return_value
        mock_hub.initialize_foundation.assert_called_once()
        # Verify force=False was passed
        assert mock_hub.initialize_foundation.call_args.kwargs["force"] is False

    @patch("provide.foundation.cli.utils.get_hub")
    def test_setup_cli_logging_reinit_default(self, mock_get_hub: MagicMock) -> None:
        """Test that reinit_logging defaults to True for backward compatibility."""
        ctx = create_cli_context()
        setup_cli_logging(ctx)  # No reinit_logging parameter
        mock_hub = mock_get_hub.return_value
        mock_hub.initialize_foundation.assert_called_once()
        # Verify force=True by default
        assert mock_hub.initialize_foundation.call_args.kwargs["force"] is True


# 🧱🏗️🔚
