#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Comprehensive coverage tests for console/output.py module."""

from __future__ import annotations

import os
import sys

from provide.testkit import FoundationTestCase
from provide.testkit.mocking import Mock, patch

from provide.foundation.console.output import (
    _get_context,
    _output_json,
    _should_use_color,
    _should_use_json,
    pout,
)
from provide.foundation.context import CLIContext


class TestGetContext(FoundationTestCase):
    """Test _get_context function."""

    def test_get_context_no_click(self) -> None:
        """Test _get_context when click is not available."""
        with patch("provide.foundation.console.output._HAS_CLICK", False):
            result = _get_context()
            assert result is None

    def test_get_context_click_no_context(self) -> None:
        """Test _get_context when click has no current context."""
        with (
            patch("provide.foundation.console.output._HAS_CLICK", True),
            patch("provide.foundation.console.output.click") as mock_click,
        ):
            mock_click.get_current_context.return_value = None

            result = _get_context()
            assert result is None
            mock_click.get_current_context.assert_called_once_with(silent=True)

    def test_get_context_click_with_context_obj(self) -> None:
        """Test _get_context when click has context with proper obj."""
        with (
            patch("provide.foundation.console.output._HAS_CLICK", True),
            patch("provide.foundation.console.output.click") as mock_click,
        ):
            mock_ctx = Mock()
            mock_context_obj = CLIContext()
            mock_ctx.obj = mock_context_obj
            mock_click.get_current_context.return_value = mock_ctx

            result = _get_context()
            assert result is mock_context_obj

    def test_get_context_click_with_invalid_obj(self) -> None:
        """Test _get_context when click context has invalid obj."""
        with (
            patch("provide.foundation.console.output._HAS_CLICK", True),
            patch("provide.foundation.console.output.click") as mock_click,
        ):
            mock_ctx = Mock()
            mock_ctx.obj = "not a Context object"
            mock_click.get_current_context.return_value = mock_ctx

            result = _get_context()
            assert result is None


class TestShouldUseJson(FoundationTestCase):
    """Test _should_use_json function."""

    def test_should_use_json_with_context_true(self) -> None:
        """Test _should_use_json with context that has json_output=True."""
        mock_ctx = Mock()
        mock_ctx.json_output = True

        result = _should_use_json(mock_ctx)
        assert result is True

    def test_should_use_json_with_context_false(self) -> None:
        """Test _should_use_json with context that has json_output=False."""
        mock_ctx = Mock()
        mock_ctx.json_output = False

        result = _should_use_json(mock_ctx)
        assert result is False

    def test_should_use_json_no_context(self) -> None:
        """Test _should_use_json with no context."""
        result = _should_use_json(None)
        assert result is False

    def test_should_use_json_auto_get_context(self) -> None:
        """Test _should_use_json automatically gets context when not provided."""
        with patch("provide.foundation.console.output._get_context") as mock_get_ctx:
            mock_ctx = Mock()
            mock_ctx.json_output = True
            mock_get_ctx.return_value = mock_ctx

            result = _should_use_json()
            assert result is True
            mock_get_ctx.assert_called_once()


class TestShouldUseColor(FoundationTestCase):
    """Test _should_use_color function."""

    def setup_method(self) -> None:
        """Ensure color environment variables are cleared for tests."""
        self.original_no_color = os.environ.get("NO_COLOR")
        self.original_force_color = os.environ.get("FORCE_COLOR")
        os.environ.pop("NO_COLOR", None)
        os.environ.pop("FORCE_COLOR", None)

    def teardown_method(self) -> None:
        """Restore color environment variables after tests."""
        if self.original_no_color is not None:
            os.environ["NO_COLOR"] = self.original_no_color
        else:
            os.environ.pop("NO_COLOR", None)

        if self.original_force_color is not None:
            os.environ["FORCE_COLOR"] = self.original_force_color
        else:
            os.environ.pop("FORCE_COLOR", None)

    def test_should_use_color_with_stream_tty(self) -> None:
        """Test _should_use_color with a stream that is TTY."""
        mock_stream = Mock()
        mock_stream.isatty.return_value = True

        result = _should_use_color(None, mock_stream)
        assert result is True

    def test_should_use_color_with_stream_not_tty(self) -> None:
        """Test _should_use_color with a stream that is not TTY."""
        mock_stream = Mock()
        mock_stream.isatty.return_value = False

        result = _should_use_color(None, mock_stream)
        assert result is False

    def test_should_use_color_stream_no_isatty(self) -> None:
        """Test _should_use_color with stream that has no isatty method."""
        mock_stream = Mock(spec=[])  # Mock with no isatty method

        result = _should_use_color(None, mock_stream)
        assert result is False  # lambda: False should be called

    def test_should_use_color_no_stream_stdout_tty(self) -> None:
        """Test _should_use_color with no stream, stdout is TTY."""
        with patch("sys.stdout") as mock_stdout, patch("sys.stderr") as mock_stderr:
            mock_stdout.isatty.return_value = True
            mock_stderr.isatty.return_value = False

            result = _should_use_color()
            assert result is True

    def test_should_use_color_no_stream_stderr_tty(self) -> None:
        """Test _should_use_color with no stream, stderr is TTY."""
        with patch("sys.stdout") as mock_stdout, patch("sys.stderr") as mock_stderr:
            mock_stdout.isatty.return_value = False
            mock_stderr.isatty.return_value = True

            result = _should_use_color()
            assert result is True

    def test_should_use_color_no_stream_neither_tty(self) -> None:
        """Test _should_use_color with no stream, neither stdout nor stderr are TTY."""
        with patch("sys.stdout") as mock_stdout, patch("sys.stderr") as mock_stderr:
            mock_stdout.isatty.return_value = False
            mock_stderr.isatty.return_value = False

            result = _should_use_color()
            assert result is False


class TestOutputJson(FoundationTestCase):
    """Test _output_json function."""

    def test_output_json_success(self) -> None:
        """Test _output_json with successful JSON encoding."""
        with patch("provide.foundation.console.output.click") as mock_click:
            data = {"key": "value"}
            mock_stream = Mock()

            _output_json(data, mock_stream)

            mock_click.echo.assert_called_once()
            args, kwargs = mock_click.echo.call_args
            assert "key" in args[0]
            assert "value" in args[0]
            assert kwargs["file"] is mock_stream

    def test_output_json_encoding_error_path(self) -> None:
        """Test that _output_json has error handling path."""
        with patch("provide.foundation.console.output.click") as mock_click:
            # Test the normal successful path
            data = {"key": "value"}
            mock_stream = Mock()

            _output_json(data, mock_stream)

            # Should be called once successfully
            mock_click.echo.assert_called_once()
            args, kwargs = mock_click.echo.call_args
            assert "key" in args[0]
            assert "value" in args[0]
            assert kwargs["file"] is mock_stream

            # Verify the error handling decorator exists in the function
            import inspect

            source = inspect.getsource(_output_json)
            assert "@resilient" in source
            assert "suppress=(TypeError, ValueError, AttributeError)" in source

    def test_output_json_default_stream(self) -> None:
        """Test _output_json with default stdout stream."""
        with patch("provide.foundation.console.output.click") as mock_click:
            data = {"test": True}

            _output_json(data)

            mock_click.echo.assert_called_once()
            _, kwargs = mock_click.echo.call_args
            # Check it's a stdout stream (pytest captures stdout, so can't use identity check)
            assert kwargs["file"].name == "<stdout>"


class TestPoutFunction(FoundationTestCase):
    """Test pout function."""

    def test_pout_simple_message(self) -> None:
        """Test pout with simple string message."""
        with (
            patch("provide.foundation.console.output._HAS_CLICK", True),
            patch("provide.foundation.console.output.click") as mock_click,
            patch(
                "provide.foundation.console.output._get_context",
                return_value=None,
            ),
        ):
            pout("Hello world")

            mock_click.echo.assert_called_once_with("Hello world", nl=True)

    def test_pout_json_mode_with_key(self) -> None:
        """Test pout in JSON mode with json_key."""
        mock_ctx = Mock()
        mock_ctx.json_output = True

        with patch(
            "provide.foundation.console.output._output_json",
        ) as mock_output_json:
            pout("test message", ctx=mock_ctx, json_key="message")

            mock_output_json.assert_called_once_with(
                {"message": "test message"},
                sys.stdout,
            )

    def test_pout_json_mode_no_key(self) -> None:
        """Test pout in JSON mode without json_key."""
        mock_ctx = Mock()
        mock_ctx.json_output = True

        with patch(
            "provide.foundation.console.output._output_json",
        ) as mock_output_json:
            pout({"data": "value"}, ctx=mock_ctx)

            mock_output_json.assert_called_once_with({"data": "value"}, sys.stdout)

    def test_pout_with_prefix(self) -> None:
        """Test pout with prefix option."""
        with (
            patch("provide.foundation.console.output._HAS_CLICK", True),
            patch("provide.foundation.console.output.click") as mock_click,
            patch(
                "provide.foundation.console.output._get_context",
                return_value=None,
            ),
        ):
            pout("message", prefix="INFO:")

            mock_click.echo.assert_called_once_with("INFO: message", nl=True)

    def test_pout_with_colors_and_formatting(self) -> None:
        """Test pout with color and formatting options."""
        mock_ctx = Mock()
        mock_ctx.json_output = False

        with (
            patch("provide.foundation.console.output._HAS_CLICK", True),
            patch("provide.foundation.console.output.click") as mock_click,
            patch(
                "provide.foundation.console.output._should_use_color",
                return_value=True,
            ),
        ):
            pout(
                "colored message",
                ctx=mock_ctx,
                color="red",
                bold=True,
                dim=False,
            )

            mock_click.secho.assert_called_once_with(
                "colored message",
                fg="red",
                bold=True,
                dim=False,
                nl=True,
            )

    def test_pout_no_color_support(self) -> None:
        """Test pout when colors are not supported."""
        mock_ctx = Mock()
        mock_ctx.json_output = False

        with (
            patch("provide.foundation.console.output._HAS_CLICK", True),
            patch("provide.foundation.console.output.click") as mock_click,
            patch(
                "provide.foundation.console.output._should_use_color",
                return_value=False,
            ),
        ):
            pout("message", ctx=mock_ctx, color="red", bold=True)

            mock_click.echo.assert_called_once_with("message", nl=True)

    def test_pout_no_click_fallback(self) -> None:
        """Test pout fallback when click is not available."""
        with (
            patch("provide.foundation.console.output._HAS_CLICK", False),
            patch("builtins.print") as mock_print,
        ):
            pout("fallback message")

            mock_print.assert_called_once_with("fallback message", file=sys.stdout)

    def test_pout_no_click_fallback_no_newline(self) -> None:
        """Test pout fallback without newline when click is not available."""
        with (
            patch("provide.foundation.console.output._HAS_CLICK", False),
            patch("builtins.print") as mock_print,
        ):
            pout("no newline", nl=False)

            mock_print.assert_called_once_with(
                "no newline",
                file=sys.stdout,
                end="",
            )

    def test_pout_newline_aliases(self) -> None:
        """Test pout handles both nl and newline parameters."""
        with (
            patch("provide.foundation.console.output._HAS_CLICK", True),
            patch("provide.foundation.console.output.click") as mock_click,
            patch(
                "provide.foundation.console.output._get_context",
                return_value=None,
            ),
        ):
            # Test with newline=False
            pout("test", newline=False)
            mock_click.echo.assert_called_with("test", nl=False)

            # Test with nl=False (should override newline default)
            mock_click.reset_mock()
            pout("test2", nl=False, newline=True)
            mock_click.echo.assert_called_with("test2", nl=False)


# 🧱🏗️🔚
