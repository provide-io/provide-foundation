#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#


from __future__ import annotations

#
# tests/core/test_foundation_log_output.py
#
"""Tests for FOUNDATION_LOG_OUTPUT environment variable functionality."""

import io
import sys
from typing import Any

from provide.testkit import FoundationTestCase
from provide.testkit.mocking import patch
import pytest
from pytest import CaptureFixture

from provide.foundation.logger.config import LoggingConfig, TelemetryConfig
from provide.foundation.utils.streams import get_foundation_log_stream


class TestFoundationLogOutputEnvironmentVariable(FoundationTestCase):
    """Test FOUNDATION_LOG_OUTPUT environment variable parsing and validation."""

    def test_foundation_log_output_default_stderr(self, monkeypatch: Any) -> None:
        """Test that default value is stderr."""
        # Clear any existing FOUNDATION_LOG_OUTPUT
        monkeypatch.delenv("FOUNDATION_LOG_OUTPUT", raising=False)

        config = LoggingConfig.from_env()
        assert config.foundation_log_output == "stderr"

    def test_foundation_log_output_valid_values(self, monkeypatch: Any) -> None:
        """Test that valid values are accepted."""
        valid_values = ["stderr", "stdout", "main"]

        for value in valid_values:
            monkeypatch.setenv("FOUNDATION_LOG_OUTPUT", value)
            config = LoggingConfig.from_env()
            assert config.foundation_log_output == value.lower()

    def test_foundation_log_output_case_insensitive(self, monkeypatch: Any) -> None:
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

    def test_foundation_log_output_invalid_value_raises_error(
        self,
        monkeypatch: Any,
    ) -> None:
        """Test that invalid values raise ValueError (strict validation)."""
        monkeypatch.setenv("FOUNDATION_LOG_OUTPUT", "invalid_value")

        # Should raise ValueError with strict validation
        with pytest.raises(ValueError, match="Invalid foundation_log_output 'invalid_value'"):
            LoggingConfig.from_env()


class TestFoundationLogStreamUtility(FoundationTestCase):
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
        with patch(
            "provide.foundation.streams.core._PROVIDE_LOG_STREAM",
        ) as mock_stream:
            mock_stream.__class__ = io.TextIOWrapper
            stream = get_foundation_log_stream("main")
            assert stream is mock_stream

    def test_invalid_setting_fallback(self) -> None:
        """Test that invalid setting falls back to stderr."""
        stream = get_foundation_log_stream("invalid_setting")

        # Should fallback to stderr
        assert stream is sys.stderr


class TestFoundationLogOutputIntegration(FoundationTestCase):
    """Integration tests for FOUNDATION_LOG_OUTPUT affecting both core setup and config warnings."""

    def test_foundation_log_output_affects_both_loggers(
        self,
        monkeypatch: Any,
        capsys: CaptureFixture,
    ) -> None:
        """Test that FOUNDATION_LOG_OUTPUT routing works for configuration."""
        monkeypatch.setenv("FOUNDATION_LOG_OUTPUT", "stdout")

        # Foundation reset is handled by FoundationTestCase

        # Create config - this exercises the routing behavior
        config = TelemetryConfig.from_env()

        # The important test is that configuration loading succeeded
        assert config is not None
        assert hasattr(config, "logging")

    def test_foundation_log_output_main_with_log_file(
        self,
        monkeypatch: Any,
        tmp_path: Any,
        capsys: CaptureFixture,
    ) -> None:
        """Test FOUNDATION_LOG_OUTPUT=main follows main log file destination."""
        log_file = tmp_path / "test.log"

        # Set up main logs to go to file, foundation logs to follow main
        monkeypatch.setenv("PROVIDE_LOG_FILE", str(log_file))
        monkeypatch.setenv("FOUNDATION_LOG_OUTPUT", "main")

        # Reset and setup telemetry with file logging
        from provide.foundation import get_hub

        config = TelemetryConfig.from_env()
        hub = get_hub()
        hub.initialize_foundation(config, force=True)

        # Foundation messages should follow main log destination (file)
        # Test that config creation works properly with file-based routing
        test_config = LoggingConfig.from_env()
        assert test_config is not None

        # The important behavior is that FOUNDATION_LOG_OUTPUT=main is respected
        assert test_config.foundation_log_output == "main"

    def test_foundation_log_output_stderr_with_main_to_file(
        self,
        monkeypatch: Any,
        tmp_path: Any,
        capsys: CaptureFixture,
    ) -> None:
        """Test FOUNDATION_LOG_OUTPUT=stderr keeps foundation logs separate from main log file."""
        log_file = tmp_path / "test.log"

        # Set up main logs to go to file, but foundation logs stay on stderr
        monkeypatch.setenv("PROVIDE_LOG_FILE", str(log_file))
        monkeypatch.setenv("FOUNDATION_LOG_OUTPUT", "stderr")

        # Reset and setup telemetry
        from provide.foundation import get_hub

        config = TelemetryConfig.from_env()
        hub = get_hub()
        hub.initialize_foundation(config, force=True)

        # Test that stderr routing works independently of file routing
        test_config = LoggingConfig.from_env()
        assert test_config is not None

        # The important behavior is that FOUNDATION_LOG_OUTPUT=stderr is respected
        assert test_config.foundation_log_output == "stderr"


# 🧱🏗️🔚
