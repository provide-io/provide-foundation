#
# tests/core/test_foundation_log_output.py
#
"""
Tests for FOUNDATION_LOG_OUTPUT environment variable functionality.
"""

import io
import os
import sys
from unittest.mock import MagicMock, patch

import pytest
from pytest import CaptureFixture

from provide.foundation.logger.config import LoggingConfig, TelemetryConfig
from provide.foundation.utils.streams import get_foundation_log_stream


class TestFoundationLogOutputEnvironmentVariable:
    """Test FOUNDATION_LOG_OUTPUT environment variable parsing and validation."""

    def test_foundation_log_output_default_stderr(self, monkeypatch) -> None:
        """Test that default value is stderr."""
        # Clear any existing FOUNDATION_LOG_OUTPUT
        monkeypatch.delenv("FOUNDATION_LOG_OUTPUT", raising=False)
        
        config = LoggingConfig.from_env()
        assert config.foundation_log_output == "stderr"

    def test_foundation_log_output_valid_values(self, monkeypatch) -> None:
        """Test that valid values are accepted."""
        valid_values = ["stderr", "stdout", "main"]
        
        for value in valid_values:
            monkeypatch.setenv("FOUNDATION_LOG_OUTPUT", value)
            config = LoggingConfig.from_env()
            assert config.foundation_log_output == value.lower()

    def test_foundation_log_output_case_insensitive(self, monkeypatch) -> None:
        """Test that values are case-insensitive."""
        test_cases = [
            ("STDERR", "stderr"),
            ("Stdout", "stdout"), 
            ("MAIN", "main"),
            ("StdErr", "stderr"),
        ]
        
        for input_value, expected_value in test_cases:
            monkeypatch.setenv("FOUNDATION_LOG_OUTPUT", input_value)
            config = LoggingConfig.from_env()
            assert config.foundation_log_output == expected_value

    def test_foundation_log_output_invalid_value_with_warning(
        self, monkeypatch, capsys: CaptureFixture
    ) -> None:
        """Test that invalid values generate warnings and use default."""
        monkeypatch.setenv("FOUNDATION_LOG_OUTPUT", "invalid_value")
        
        config = LoggingConfig.from_env()
        # Should use default value
        assert config.foundation_log_output == "stderr"
        
        # Should generate warning
        captured = capsys.readouterr()
        assert "[Foundation Config Warning]" in captured.err
        assert "FOUNDATION_LOG_OUTPUT" in captured.err
        assert "invalid_value" in captured.err

    def test_foundation_log_output_non_strict_mode(self, monkeypatch, capsys: CaptureFixture) -> None:
        """Test that non-strict mode doesn't generate warnings for invalid values."""
        monkeypatch.setenv("FOUNDATION_LOG_OUTPUT", "invalid_value")
        
        config = LoggingConfig.from_env(strict=False)
        # Should use default value
        assert config.foundation_log_output == "stderr"
        
        # Should NOT generate warning in non-strict mode
        captured = capsys.readouterr()
        assert "[Foundation Config Warning]" not in captured.err


class TestFoundationLogStreamUtility:
    """Test get_foundation_log_stream() utility function."""

    def test_stderr_setting(self) -> None:
        """Test that stderr setting returns sys.stderr."""
        stream = get_foundation_log_stream("stderr")
        assert stream is sys.stderr

    def test_stdout_setting(self) -> None:
        """Test that stdout setting returns sys.stdout."""
        stream = get_foundation_log_stream("stdout")
        assert stream is sys.stdout

    def test_main_setting_with_provide_stream(self) -> None:
        """Test that main setting returns _PROVIDE_LOG_STREAM."""
        with patch("provide.foundation.core._PROVIDE_LOG_STREAM") as mock_stream:
            mock_stream.__class__ = io.TextIOWrapper
            stream = get_foundation_log_stream("main")
            assert stream is mock_stream

    def test_invalid_setting_warning_and_fallback(self, capsys: CaptureFixture) -> None:
        """Test that invalid setting generates warning and falls back to stderr."""
        stream = get_foundation_log_stream("invalid_setting")
        
        # Should fallback to stderr
        assert stream is sys.stderr
        
        # Should generate warning
        captured = capsys.readouterr()
        assert "[Foundation Config Warning]" in captured.err
        assert "invalid_setting" in captured.err


class TestFoundationLogOutputIntegration:
    """Integration tests for FOUNDATION_LOG_OUTPUT affecting both core setup and config warnings."""

    def test_foundation_log_output_affects_both_loggers(self, monkeypatch, capsys: CaptureFixture) -> None:
        """Test that FOUNDATION_LOG_OUTPUT affects both core setup and config warning loggers."""
        monkeypatch.setenv("FOUNDATION_LOG_OUTPUT", "stdout")
        
        # This should trigger both core setup logger creation and config warning
        monkeypatch.setenv("PROVIDE_LOG_LEVEL", "INVALID_LEVEL")
        
        from provide.foundation.testing import reset_foundation_setup_for_testing
        reset_foundation_setup_for_testing()
        
        # Create config which will trigger warning
        config = TelemetryConfig.from_env()
        
        captured = capsys.readouterr()
        # Config warning should go to stdout (not stderr)
        assert "[Foundation Config Warning]" in captured.out
        assert "[Foundation Config Warning]" not in captured.err

    def test_foundation_log_output_main_with_log_file(self, monkeypatch, tmp_path, capsys: CaptureFixture) -> None:
        """Test FOUNDATION_LOG_OUTPUT=main follows main log file destination."""
        log_file = tmp_path / "test.log"
        
        # Set up main logs to go to file, foundation logs to follow main
        monkeypatch.setenv("PROVIDE_LOG_FILE", str(log_file))
        monkeypatch.setenv("FOUNDATION_LOG_OUTPUT", "main")
        
        # Reset and setup telemetry with file logging
        from provide.foundation.testing import reset_foundation_setup_for_testing, setup_telemetry
        reset_foundation_setup_for_testing()
        
        config = TelemetryConfig.from_env()
        setup_telemetry(config)
        
        # Trigger a config warning
        monkeypatch.setenv("PROVIDE_LOG_LEVEL", "INVALID_LEVEL")
        config = LoggingConfig.from_env()
        
        # Foundation messages should follow main log destination (file)
        # Check that the file was created and has content
        assert log_file.exists()
        log_content = log_file.read_text()
        assert "[Foundation Config Warning]" in log_content

    def test_foundation_log_output_stderr_with_main_to_file(self, monkeypatch, tmp_path, capsys: CaptureFixture) -> None:
        """Test FOUNDATION_LOG_OUTPUT=stderr keeps foundation logs separate from main log file."""
        log_file = tmp_path / "test.log"
        
        # Set up main logs to go to file, but foundation logs stay on stderr  
        monkeypatch.setenv("PROVIDE_LOG_FILE", str(log_file))
        monkeypatch.setenv("FOUNDATION_LOG_OUTPUT", "stderr")
        
        # Reset and setup telemetry
        from provide.foundation.testing import reset_foundation_setup_for_testing, setup_telemetry
        reset_foundation_setup_for_testing()
        
        config = TelemetryConfig.from_env()
        setup_telemetry(config)
        
        # Trigger a config warning
        monkeypatch.setenv("PROVIDE_LOG_LEVEL", "INVALID_LEVEL")
        config = LoggingConfig.from_env()
        
        captured = capsys.readouterr()
        # Foundation warning should go to stderr, not file
        assert "[Foundation Config Warning]" in captured.err
        
        # File should exist but not contain foundation warning
        if log_file.exists():
            log_content = log_file.read_text()
            assert "[Foundation Config Warning]" not in log_content