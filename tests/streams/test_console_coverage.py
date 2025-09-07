#
# test_console_coverage.py
#
"""
Tests to achieve coverage for console and streams functionality.
"""

import sys
from io import StringIO
from unittest.mock import patch, Mock
import pytest


class TestConsoleStreams:
    """Test console stream functionality."""
    
    def test_get_console_width_normal(self):
        """Test console width detection."""
        from provide.foundation.streams.console import get_console_width
        
        width = get_console_width()
        assert isinstance(width, int)
        assert width > 0
    
    @patch('shutil.get_terminal_size')
    def test_get_console_width_fallback(self, mock_get_terminal_size):
        """Test console width fallback when detection fails."""
        from provide.foundation.streams.console import get_console_width
        
        mock_get_terminal_size.side_effect = OSError("Terminal size unavailable")
        
        width = get_console_width()
        assert isinstance(width, int)
        assert width == 80  # Default fallback
    
    def test_is_interactive_terminal(self):
        """Test interactive terminal detection."""
        from provide.foundation.streams.console import is_interactive_terminal
        
        # Test with real streams
        result = is_interactive_terminal(sys.stdout)
        assert isinstance(result, bool)
        
        result = is_interactive_terminal(sys.stderr)
        assert isinstance(result, bool)
    
    def test_is_interactive_terminal_stringio(self):
        """Test interactive detection with StringIO (not interactive)."""
        from provide.foundation.streams.console import is_interactive_terminal
        
        fake_stream = StringIO()
        result = is_interactive_terminal(fake_stream)
        assert result is False
    
    def test_supports_ansi_colors(self):
        """Test ANSI color support detection."""
        from provide.foundation.streams.console import supports_ansi_colors
        
        result = supports_ansi_colors()
        assert isinstance(result, bool)
    
    @patch.dict('os.environ', {'NO_COLOR': '1'})
    def test_supports_ansi_colors_no_color(self):
        """Test ANSI color support with NO_COLOR env var."""
        from provide.foundation.streams.console import supports_ansi_colors
        
        result = supports_ansi_colors()
        assert result is False
    
    @patch.dict('os.environ', {'FORCE_COLOR': '1'})
    def test_supports_ansi_colors_force_color(self):
        """Test ANSI color support with FORCE_COLOR env var."""
        from provide.foundation.streams.console import supports_ansi_colors
        
        result = supports_ansi_colors()
        assert result is True
    
    def test_format_console_line(self):
        """Test console line formatting."""
        from provide.foundation.streams.console import format_console_line
        
        # Test basic formatting
        result = format_console_line("Hello, World!", width=20)
        assert isinstance(result, str)
        assert len(result) <= 20
    
    def test_format_console_line_with_colors(self):
        """Test console line formatting with color codes."""
        from provide.foundation.streams.console import format_console_line
        
        colored_text = "\033[31mRed Text\033[0m"
        result = format_console_line(colored_text, width=20)
        assert isinstance(result, str)
    
    def test_wrap_console_text(self):
        """Test console text wrapping."""
        from provide.foundation.streams.console import wrap_console_text
        
        long_text = "This is a very long line that should be wrapped"
        result = wrap_console_text(long_text, width=20)
        
        assert isinstance(result, list)
        assert len(result) > 1
        for line in result:
            assert len(line) <= 20
    
    def test_center_console_text(self):
        """Test console text centering."""
        from provide.foundation.streams.console import center_console_text
        
        text = "Hello"
        result = center_console_text(text, width=20)
        
        assert isinstance(result, str)
        assert len(result) == 20
        assert text in result
    
    def test_truncate_console_line(self):
        """Test console line truncation."""
        from provide.foundation.streams.console import truncate_console_line
        
        long_text = "This is a very long line that should be truncated"
        result = truncate_console_line(long_text, width=20)
        
        assert isinstance(result, str)
        assert len(result) <= 20
        if len(long_text) > 20:
            assert result.endswith("...")


class TestFileStreams:
    """Test file stream functionality."""
    
    def test_configure_file_logging_with_path(self, tmp_path):
        """Test file logging configuration with valid path."""
        from provide.foundation.streams.file import configure_file_logging
        
        log_file = tmp_path / "test.log"
        configure_file_logging(str(log_file))
        
        # Should create the file or directory structure
        assert log_file.parent.exists()
    
    def test_configure_file_logging_none(self):
        """Test file logging configuration with None."""
        from provide.foundation.streams.file import configure_file_logging
        
        # Should not raise an exception
        configure_file_logging(None)
    
    def test_configure_file_logging_invalid_path(self):
        """Test file logging with invalid path."""
        from provide.foundation.streams.file import configure_file_logging
        
        # Invalid path that can't be created
        invalid_path = "/root/nonexistent/test.log"
        
        # Should handle gracefully without crashing
        try:
            configure_file_logging(invalid_path)
        except PermissionError:
            pass  # Expected for protected directories
    
    def test_flush_log_streams(self):
        """Test log stream flushing."""
        from provide.foundation.streams.file import flush_log_streams
        
        # Should not raise an exception
        flush_log_streams()
    
    def test_close_log_streams(self):
        """Test log stream closing."""
        from provide.foundation.streams.file import close_log_streams
        
        # Should not raise an exception
        close_log_streams()
    
    def test_get_log_file_handler(self):
        """Test getting log file handler."""
        from provide.foundation.streams.file import get_log_file_handler
        
        handler = get_log_file_handler()
        # May return None if no file handler is configured
        assert handler is None or hasattr(handler, 'flush')


class TestColorUtils:
    """Test color utility functions."""
    
    def test_strip_ansi_codes(self):
        """Test ANSI color code stripping."""
        from provide.foundation.utils.formatting import strip_ansi_codes
        
        colored_text = "\033[31mRed Text\033[0m"
        result = strip_ansi_codes(colored_text)
        
        assert result == "Red Text"
        assert "\033" not in result
    
    def test_strip_ansi_codes_no_codes(self):
        """Test ANSI stripping with no color codes."""
        from provide.foundation.utils.formatting import strip_ansi_codes
        
        plain_text = "Plain text"
        result = strip_ansi_codes(plain_text)
        
        assert result == plain_text
    
    def test_get_text_width(self):
        """Test text width calculation ignoring ANSI codes."""
        from provide.foundation.utils.formatting import get_text_width
        
        colored_text = "\033[31mRed\033[0m"
        result = get_text_width(colored_text)
        
        assert result == 3  # Only counts visible characters
    
    def test_get_text_width_plain(self):
        """Test text width with plain text."""
        from provide.foundation.utils.formatting import get_text_width
        
        plain_text = "Hello"
        result = get_text_width(plain_text)
        
        assert result == 5


class TestProgressDisplay:
    """Test progress display utilities."""
    
    def test_create_progress_bar(self):
        """Test progress bar creation."""
        from provide.foundation.streams.console import create_progress_bar
        
        progress = create_progress_bar(current=50, total=100, width=20)
        
        assert isinstance(progress, str)
        assert len(progress.strip()) > 0
    
    def test_create_progress_bar_zero_total(self):
        """Test progress bar with zero total."""
        from provide.foundation.streams.console import create_progress_bar
        
        progress = create_progress_bar(current=0, total=0, width=20)
        
        assert isinstance(progress, str)
    
    def test_create_progress_bar_over_100_percent(self):
        """Test progress bar with over 100% completion."""
        from provide.foundation.streams.console import create_progress_bar
        
        progress = create_progress_bar(current=150, total=100, width=20)
        
        assert isinstance(progress, str)
    
    def test_format_percentage(self):
        """Test percentage formatting."""
        from provide.foundation.streams.console import format_percentage
        
        result = format_percentage(0.75)
        assert "75" in result
        assert "%" in result
    
    def test_format_percentage_edge_cases(self):
        """Test percentage formatting edge cases."""
        from provide.foundation.streams.console import format_percentage
        
        # Test 0%
        result = format_percentage(0.0)
        assert "0" in result
        
        # Test 100%
        result = format_percentage(1.0)
        assert "100" in result
        
        # Test over 100%
        result = format_percentage(1.5)
        assert isinstance(result, str)


class TestStreamBuffering:
    """Test stream buffering functionality."""
    
    def test_buffer_console_output(self):
        """Test console output buffering."""
        from provide.foundation.streams.console import BufferedConsoleWriter
        
        buffer = StringIO()
        writer = BufferedConsoleWriter(buffer)
        
        writer.write("Hello")
        writer.write(" World")
        writer.flush()
        
        result = buffer.getvalue()
        assert "Hello World" in result
    
    def test_auto_flush_buffer(self):
        """Test automatic buffer flushing."""
        from provide.foundation.streams.console import BufferedConsoleWriter
        
        buffer = StringIO()
        writer = BufferedConsoleWriter(buffer, auto_flush_size=5)
        
        writer.write("123456789")  # Should trigger auto-flush
        
        result = buffer.getvalue()
        assert len(result) > 0