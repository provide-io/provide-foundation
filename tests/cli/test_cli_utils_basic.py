"""Tests for basic CLI utility functions."""

import json
from unittest.mock import MagicMock, patch

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
from provide.foundation.cli.context import Context
from provide.foundation.logger import TelemetryConfig


class TestCliEchoFunctions:
    """Test CLI echo functions."""

    @patch("click.echo")
    def test_echo_json(self, mock_echo: MagicMock) -> None:
        """Test JSON output."""
        data = {"key": "value", "number": 42}
        echo_json(data)
        mock_echo.assert_called_once()
        output = mock_echo.call_args[0][0]
        parsed = json.loads(output)
        assert parsed == data

    @patch("click.secho")
    def test_echo_error_text(self, mock_secho: MagicMock) -> None:
        """Test error message output."""
        echo_error("Something went wrong")
        mock_secho.assert_called_once()
        output = mock_secho.call_args[0][0]
        assert "Something went wrong" in output
        assert mock_secho.call_args[1]["err"] is True

    @patch("click.echo")
    def test_echo_error_json(self, mock_echo: MagicMock) -> None:
        """Test error message as JSON."""
        echo_error("Something went wrong", json_output=True)
        mock_echo.assert_called_once()
        output = mock_echo.call_args[0][0]
        parsed = json.loads(output)
        assert parsed["error"] == "Something went wrong"

    @patch("click.secho")
    def test_echo_success_text(self, mock_secho: MagicMock) -> None:
        """Test success message output."""
        echo_success("Operation completed")
        mock_secho.assert_called_once()
        output = mock_secho.call_args[0][0]
        assert "Operation completed" in output

    @patch("click.echo")
    def test_echo_success_json(self, mock_echo: MagicMock) -> None:
        """Test success message as JSON."""
        echo_success("Operation completed", json_output=True)
        mock_echo.assert_called_once()
        output = mock_echo.call_args[0][0]
        parsed = json.loads(output)
        assert parsed["success"] == "Operation completed"

    @patch("click.secho")
    def test_echo_warning_text(self, mock_secho: MagicMock) -> None:
        """Test warning message output."""
        echo_warning("Be careful")
        mock_secho.assert_called_once()
        output = mock_secho.call_args[0][0]
        assert "Be careful" in output

    @patch("click.echo")
    def test_echo_info_text(self, mock_echo: MagicMock) -> None:
        """Test info message output."""
        echo_info("FYI")
        mock_echo.assert_called_once()
        output = mock_echo.call_args[0][0]
        assert "FYI" in output


class TestCliContext:
    """Test CLI context creation."""

    def test_create_cli_context_default(self) -> None:
        """Test creating default CLI context."""
        ctx = create_cli_context()
        assert isinstance(ctx, Context)
        assert ctx.profile == "default"

    def test_create_cli_context_with_overrides(self) -> None:
        """Test creating CLI context with overrides."""
        ctx = create_cli_context(profile="myapp", debug=True)
        assert ctx.profile == "myapp"
        assert ctx.debug is True


class TestCliAssertions:
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


class TestCliLogging:
    """Test CLI logging setup."""

    @patch("provide.foundation.cli.utils.setup_telemetry")
    def test_setup_cli_logging_default(self, mock_setup_telemetry: MagicMock) -> None:
        """Test default CLI logging setup."""
        ctx = create_cli_context()
        setup_cli_logging(ctx)
        mock_setup_telemetry.assert_called_once()
        config_arg = mock_setup_telemetry.call_args.kwargs["config"]
        assert isinstance(config_arg, TelemetryConfig)
        assert config_arg.logging.default_level == "INFO"
        assert config_arg.logging.console_formatter == "key_value"

    @patch("provide.foundation.cli.utils.setup_telemetry")
    def test_setup_cli_logging_verbose(self, mock_setup_telemetry: MagicMock) -> None:
        """Test verbose CLI logging setup."""
        ctx = create_cli_context(log_level="DEBUG")
        setup_cli_logging(ctx)
        mock_setup_telemetry.assert_called_once()
        config_arg = mock_setup_telemetry.call_args.kwargs["config"]
        assert config_arg.logging.default_level == "DEBUG"

    @patch("provide.foundation.cli.utils.setup_telemetry")
    def test_setup_cli_logging_quiet(self, mock_setup_telemetry: MagicMock) -> None:
        """Test quiet CLI logging setup."""
        ctx = create_cli_context(log_level="ERROR")
        setup_cli_logging(ctx)
        mock_setup_telemetry.assert_called_once()
        config_arg = mock_setup_telemetry.call_args.kwargs["config"]
        assert config_arg.logging.default_level == "ERROR"

    @patch("provide.foundation.cli.utils.setup_telemetry")
    def test_setup_cli_logging_json(self, mock_setup_telemetry: MagicMock) -> None:
        """Test JSON CLI logging setup."""
        ctx = create_cli_context(json_output=True)
        setup_cli_logging(ctx)
        mock_setup_telemetry.assert_called_once()
        config_arg = mock_setup_telemetry.call_args.kwargs["config"]
        assert config_arg.logging.console_formatter == "json"
