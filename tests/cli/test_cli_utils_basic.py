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
        assert ctx is not None
        # Context doesn't have a 'name' attribute in current implementation
        assert ctx.profile == "default"  # Check default profile instead

    def test_create_cli_context_with_name(self) -> None:
        """Test creating CLI context with custom profile."""
        ctx = create_cli_context(profile="myapp")
        assert ctx.profile == "myapp"  # Use profile instead of non-existent name

    def test_create_cli_context_with_metadata(self) -> None:
        """Test creating CLI context with debug flag."""
        ctx = create_cli_context(debug=True)
        # Context doesn't have metadata, but has debug flag
        assert ctx.debug is True


class TestCliAssertions:
    """Test CLI assertion helpers."""

    def test_assert_cli_success(self) -> None:
        """Test successful CLI result assertion."""
        # Mock a successful result
        result = MagicMock()
        result.exit_code = 0
        result.output = "Success"

        # Should not raise
        assert_cli_success(result)
        assert_cli_success(result, "Success")

    def test_assert_cli_success_with_wrong_output(self) -> None:
        """Test CLI success assertion with wrong output."""
        result = MagicMock()
        result.exit_code = 0
        result.output = "Actual output"

        with pytest.raises(AssertionError):
            assert_cli_success(result, "Expected output")

    def test_assert_cli_success_with_error_code(self) -> None:
        """Test CLI success assertion with error exit code."""
        result = MagicMock()
        result.exit_code = 1
        result.output = "Error"

        with pytest.raises(AssertionError):
            assert_cli_success(result)

    def test_assert_cli_error(self) -> None:
        """Test CLI error assertion."""
        result = MagicMock()
        result.exit_code = 1
        result.output = "Error occurred"

        # Should not raise
        assert_cli_error(result, exit_code=1)
        assert_cli_error(result, "Error occurred", exit_code=1)

    def test_assert_cli_error_with_wrong_code(self) -> None:
        """Test CLI error assertion with wrong exit code."""
        result = MagicMock()
        result.exit_code = 1

        with pytest.raises(AssertionError):
            assert_cli_error(result, exit_code=2)


class TestCliLogging:
    """Test CLI logging setup."""

    @patch("provide.foundation.cli.utils.setup_logging")
    def test_setup_cli_logging_default(self, mock_setup: MagicMock) -> None:
        """Test default CLI logging setup."""
        setup_cli_logging()
        mock_setup.assert_called_once()

    @patch("provide.foundation.cli.utils.setup_logging")
    def test_setup_cli_logging_verbose(self, mock_setup: MagicMock) -> None:
        """Test verbose CLI logging setup."""
        setup_cli_logging(log_level="DEBUG")
        mock_setup.assert_called_once_with(level="DEBUG", json_logs=False, log_file=None)

    @patch("provide.foundation.cli.utils.setup_logging")
    def test_setup_cli_logging_quiet(self, mock_setup: MagicMock) -> None:
        """Test quiet CLI logging setup."""
        setup_cli_logging(log_level="ERROR")
        mock_setup.assert_called_once_with(level="ERROR", json_logs=False, log_file=None)

    @patch("provide.foundation.cli.utils.setup_logging")
    def test_setup_cli_logging_json(self, mock_setup: MagicMock) -> None:
        """Test JSON CLI logging setup."""
        setup_cli_logging(log_format="json")
        mock_setup.assert_called_once_with(level="INFO", json_logs=True, log_file=None)