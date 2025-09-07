#
# test_file.py
#
"""
Tests for file stream functionality.
"""

import tempfile
from pathlib import Path

import pytest

from provide.foundation.streams.file import configure_file_logging, flush_log_streams, close_log_streams


class TestFileStreams:
    def test_configure_file_logging_success(self):
        """Test successful file logging configuration."""
        with tempfile.TemporaryDirectory() as temp_dir:
            log_file = Path(temp_dir) / "test.log" 
            configure_file_logging(str(log_file))
            
            # Clean up
            close_log_streams()
    
    def test_configure_file_logging_none(self):
        """Test file logging configuration with None path."""
        configure_file_logging(None)
        
        # Clean up
        close_log_streams()
    
    def test_flush_log_streams(self):
        """Test flushing log streams."""
        with tempfile.TemporaryDirectory() as temp_dir:
            log_file = Path(temp_dir) / "test.log"
            configure_file_logging(str(log_file))
            flush_log_streams()
            
            # Clean up
            close_log_streams()
    
    def test_configure_file_logging_invalid_path(self):
        """Test file logging with invalid path."""
        # Try to write to a directory that doesn't exist and can't be created
        invalid_path = "/invalid/nonexistent/path/test.log"
        configure_file_logging(invalid_path)  # Should not raise exception
        
        # Clean up
        close_log_streams()