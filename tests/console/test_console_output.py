"""Tests for console output functions."""

import json
import sys

import pytest

from provide.foundation import pout, perr, plog
from provide.foundation.context import Context


class TestConsoleOutput:
    """Test console output functions."""
    
    def test_pout_basic(self, capsys):
        """Test basic pout to stdout."""
        pout("Hello world")
        captured = capsys.readouterr()
        assert captured.out == "Hello world\n"
        assert captured.err == ""
    
    def test_perr_basic(self, capsys):
        """Test basic perr to stderr."""
        perr("Error message")
        captured = capsys.readouterr()
        assert captured.out == ""
        assert captured.err == "Error message\n"
    
    def test_pout_no_newline(self, capsys):
        """Test pout without newline."""
        pout("Hello", nl=False)
        pout(" world")
        captured = capsys.readouterr()
        assert captured.out == "Hello world\n"
    
    def test_perr_no_newline(self, capsys):
        """Test perr without newline."""
        perr("Error", newline=False)
        perr(" occurred")
        captured = capsys.readouterr()
        assert captured.err == "Error occurred\n"
    
    def test_pout_with_dict(self, capsys):
        """Test pout with dictionary (should output as JSON in JSON mode)."""
        pout({"key": "value", "number": 42})
        captured = capsys.readouterr()
        # In non-JSON mode, it should just stringify
        assert "key" in captured.out
        assert "value" in captured.out
    
    def test_pout_with_list(self, capsys):
        """Test pout with list."""
        pout(["item1", "item2", "item3"])
        captured = capsys.readouterr()
        assert "item1" in captured.out
        assert "item2" in captured.out
    
    def test_pout_with_prefix(self, capsys):
        """Test pout with prefix."""
        pout("Success", prefix="✅")
        captured = capsys.readouterr()
        assert captured.out == "✅ Success\n"
    
    def test_perr_with_prefix(self, capsys):
        """Test perr with prefix."""
        perr("Failed", prefix="❌")
        captured = capsys.readouterr()
        assert captured.err == "❌ Failed\n"
    
    def test_plog_is_logger_alias(self):
        """Test that plog is an alias for logger."""
        from provide.foundation import logger
        assert plog is logger
    
    def test_plog_logging(self, captured_stderr_for_foundation):
        """Test plog structured logging."""
        plog.info("Test message", user="alice", action="login")
        output = captured_stderr_for_foundation.getvalue()
        assert "Test message" in output
        assert "user=alice" in output
    
    @pytest.mark.parametrize("color", ["red", "green", "yellow", "blue"])
    def test_colors_non_tty(self, capsys, color):
        """Test that colors are ignored in non-TTY mode."""
        # capsys makes stdout/stderr non-TTY
        pout("Colored text", color=color)
        captured = capsys.readouterr()
        # Should not contain ANSI codes
        assert captured.out == "Colored text\n"
        assert "\033[" not in captured.out
    
    def test_json_mode_with_context(self, capsys, monkeypatch):
        """Test JSON output mode via context."""
        # Create a mock Click context with JSON output enabled
        import click
        
        ctx = click.Context(click.Command("test"))
        ctx.obj = Context(json_output=True)
        
        def mock_get_current_context(*args, **kwargs):
            return ctx
        
        monkeypatch.setattr(click, "get_current_context", mock_get_current_context)
        
        pout({"data": "value"})
        captured = capsys.readouterr()
        
        # Should be valid JSON
        data = json.loads(captured.out)
        assert data == {"data": "value"}
    
    def test_json_mode_with_json_key(self, capsys, monkeypatch):
        """Test JSON output with json_key."""
        import click
        
        ctx = click.Context(click.Command("test"))
        ctx.obj = Context(json_output=True)
        
        def mock_get_current_context(*args, **kwargs):
            return ctx
        
        monkeypatch.setattr(click, "get_current_context", mock_get_current_context)
        
        pout("Success message", json_key="result")
        captured = capsys.readouterr()
        
        data = json.loads(captured.out)
        assert data == {"result": "Success message"}
    
    def test_perr_json_mode(self, capsys, monkeypatch):
        """Test perr in JSON mode."""
        import click
        
        ctx = click.Context(click.Command("test"))
        ctx.obj = Context(json_output=True)
        
        def mock_get_current_context(*args, **kwargs):
            return ctx
        
        monkeypatch.setattr(click, "get_current_context", mock_get_current_context)
        
        perr({"error": "Not found", "code": 404})
        captured = capsys.readouterr()
        
        # Should go to stderr
        assert captured.out == ""
        data = json.loads(captured.err)
        assert data == {"error": "Not found", "code": 404}