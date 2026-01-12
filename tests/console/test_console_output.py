#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for console output functions."""

from __future__ import annotations

import json

from provide.testkit import FoundationTestCase
import pytest

from provide.foundation import perr, pout
from provide.foundation.context import CLIContext


class TestConsoleOutput(FoundationTestCase):
    """Test console output functions."""

    def test_pout_basic(self, capsys) -> None:
        """Test basic pout to stdout."""
        pout("Hello world")
        captured = capsys.readouterr()
        assert captured.out == "Hello world\n"
        assert captured.err == ""

    def test_perr_basic(self, capsys) -> None:
        """Test basic perr to stderr."""
        perr("Error message")
        captured = capsys.readouterr()
        assert captured.out == ""
        assert captured.err == "Error message\n"

    def test_pout_no_newline(self, capsys) -> None:
        """Test pout without newline."""
        pout("Hello", nl=False)
        pout(" world")
        captured = capsys.readouterr()
        assert captured.out == "Hello world\n"

    def test_perr_no_newline(self, capsys) -> None:
        """Test perr without newline."""
        perr("Error", newline=False)
        perr(" occurred")
        captured = capsys.readouterr()
        assert captured.err == "Error occurred\n"

    def test_pout_with_dict(self, capsys) -> None:
        """Test pout with dictionary (should output as JSON in JSON mode)."""
        pout({"key": "value", "number": 42})
        captured = capsys.readouterr()
        # In non-JSON mode, it should just stringify
        assert "key" in captured.out
        assert "value" in captured.out

    def test_pout_with_list(self, capsys) -> None:
        """Test pout with list."""
        pout(["item1", "item2", "item3"])
        captured = capsys.readouterr()
        assert "item1" in captured.out
        assert "item2" in captured.out

    def test_pout_with_prefix(self, capsys) -> None:
        """Test pout with prefix."""
        capsys.readouterr()

    def test_perr_with_prefix(self, capsys) -> None:
        """Test perr with prefix."""
        perr("Failed", prefix="❌")
        captured = capsys.readouterr()
        assert captured.err == "❌ Failed\n"

    # plog tests removed - plog alias was deprecated and removed from the public API
    # Users should use logger directly instead

    @pytest.mark.parametrize("color", ["red", "green", "yellow", "blue"])
    def test_colors_non_tty(self, capsys, color) -> None:
        """Test that colors are ignored in non-TTY mode."""
        # capsys makes stdout/stderr non-TTY
        pout("Colored text", color=color)
        captured = capsys.readouterr()
        # Should not contain ANSI codes
        assert captured.out == "Colored text\n"
        assert "\033[" not in captured.out

    def test_json_mode_with_context(self, capsys, monkeypatch) -> None:
        """Test JSON output mode via context."""
        # Create a mock Click context with JSON output enabled
        import click

        ctx = click.Context(click.Command("test"))
        ctx.obj = CLIContext(json_output=True)

        def mock_get_current_context(*args, **kwargs):
            return ctx

        monkeypatch.setattr(click, "get_current_context", mock_get_current_context)

        pout({"data": "value"})
        captured = capsys.readouterr()

        # Should be valid JSON
        data = json.loads(captured.out)
        assert data == {"data": "value"}

    def test_json_mode_with_json_key(self, capsys, monkeypatch) -> None:
        """Test JSON output with json_key."""
        import click

        ctx = click.Context(click.Command("test"))
        ctx.obj = CLIContext(json_output=True)

        def mock_get_current_context(*args, **kwargs):
            return ctx

        monkeypatch.setattr(click, "get_current_context", mock_get_current_context)

        pout("Success message", json_key="result")
        captured = capsys.readouterr()

        data = json.loads(captured.out)
        assert data == {"result": "Success message"}

    def test_perr_json_mode(self, capsys, monkeypatch) -> None:
        """Test perr in JSON mode."""
        import click

        ctx = click.Context(click.Command("test"))
        ctx.obj = CLIContext(json_output=True)

        def mock_get_current_context(*args, **kwargs):
            return ctx

        monkeypatch.setattr(click, "get_current_context", mock_get_current_context)

        perr({"error": "Not found", "code": 404})
        captured = capsys.readouterr()

        # Should go to stderr
        assert captured.out == ""
        data = json.loads(captured.err)
        assert data == {"error": "Not found", "code": 404}


# 🧱🏗️🔚
