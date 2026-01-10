#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Comprehensive coverage tests for console/output.py module."""

from __future__ import annotations

import json
import sys

from provide.testkit import FoundationTestCase
from provide.testkit.mocking import Mock, patch

from provide.foundation.console.output import (
    _get_context,
    _output_json,
    perr,
    pout,
)


class TestPerrFunction(FoundationTestCase):
    """Test perr function."""

    def test_perr_simple_message(self) -> None:
        """Test perr with simple string message."""
        with (
            patch("provide.foundation.console.output._HAS_CLICK", True),
            patch("provide.foundation.console.output.click") as mock_click,
            patch(
                "provide.foundation.console.output._get_context",
                return_value=None,
            ),
        ):
            perr("Error message")

            mock_click.echo.assert_called_once_with(
                "Error message",
                err=True,
                nl=True,
            )

    def test_perr_json_mode_with_key(self) -> None:
        """Test perr in JSON mode with json_key."""
        mock_ctx = Mock()
        mock_ctx.json_output = True

        with patch(
            "provide.foundation.console.output._output_json",
        ) as mock_output_json:
            perr("error occurred", ctx=mock_ctx, json_key="error")

            mock_output_json.assert_called_once_with(
                {"error": "error occurred"},
                sys.stderr,
            )

    def test_perr_json_mode_no_key(self) -> None:
        """Test perr in JSON mode without json_key."""
        mock_ctx = Mock()
        mock_ctx.json_output = True

        with patch(
            "provide.foundation.console.output._output_json",
        ) as mock_output_json:
            perr({"error": "details"}, ctx=mock_ctx)

            mock_output_json.assert_called_once_with({"error": "details"}, sys.stderr)

    def test_perr_with_colors_and_formatting(self) -> None:
        """Test perr with color and formatting options."""
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
            perr("error message", ctx=mock_ctx, color="red", bold=True)

            mock_click.secho.assert_called_once_with(
                "error message",
                fg="red",
                bold=True,
                dim=False,
                err=True,
                nl=True,
            )

    def test_perr_no_click_fallback(self) -> None:
        """Test perr fallback when click is not available."""
        with (
            patch("provide.foundation.console.output._HAS_CLICK", False),
            patch("builtins.print") as mock_print,
        ):
            perr("error fallback")

            mock_print.assert_called_once_with("error fallback", file=sys.stderr)

    def test_perr_no_click_fallback_no_newline(self) -> None:
        """Test perr fallback without newline when click is not available."""
        with (
            patch("provide.foundation.console.output._HAS_CLICK", False),
            patch("builtins.print") as mock_print,
        ):
            perr("no newline error", nl=False)

            mock_print.assert_called_once_with(
                "no newline error",
                file=sys.stderr,
                end="",
            )


class TestEdgeCases(FoundationTestCase):
    """Test edge cases and error conditions."""

    def test_click_import_error_handling(self) -> None:
        """Test that the module handles click import errors gracefully."""
        # This tests the import error handling at lines 15-17
        with (
            patch("provide.foundation.console.output._HAS_CLICK", False),
            patch("provide.foundation.console.output.click", None),
        ):
            # Should not raise errors
            result = _get_context()
            assert result is None

            # Functions should still work
            with patch("builtins.print") as mock_print:
                pout("test message")
                mock_print.assert_called_once()

    def test_json_encoding_successful_path(self) -> None:
        """Test successful JSON encoding and verify error handling exists."""
        with patch("provide.foundation.console.output.click") as mock_click:
            # Test normal case works
            _output_json({"test": "data"})

            mock_click.echo.assert_called_once()
            args, _ = mock_click.echo.call_args
            output = json.loads(args[0])
            assert output["test"] == "data"

            # Verify the error handling decorator exists in the source
            import inspect

            source = inspect.getsource(_output_json)
            assert "@resilient" in source
            assert "suppress=(TypeError, ValueError, AttributeError)" in source

    def test_context_auto_retrieval_in_functions(self) -> None:
        """Test that pout and perr retrieve context automatically."""
        mock_ctx = Mock()
        mock_ctx.json_output = False

        with (
            patch(
                "provide.foundation.console.output._get_context",
                return_value=mock_ctx,
            ) as mock_get_ctx,
            patch("provide.foundation.console.output._HAS_CLICK", True),
            patch("provide.foundation.console.output.click") as mock_click,
        ):
            # Don't pass ctx explicitly
            pout("test")

            # Should call _get_context
            mock_get_ctx.assert_called()
            mock_click.echo.assert_called_once()

    def test_multiple_formatting_options(self) -> None:
        """Test multiple formatting options together."""
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
                "complex message",
                ctx=mock_ctx,
                color="blue",
                bold=True,
                dim=True,
                prefix="[INFO]",
                nl=False,
            )

            mock_click.secho.assert_called_once_with(
                "[INFO] complex message",
                fg="blue",
                bold=True,
                dim=True,
                nl=False,
            )


# 🧱🏗️🔚
