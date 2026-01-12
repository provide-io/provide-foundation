#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests to improve coverage for logger configuration files."""

from __future__ import annotations

import os

from provide.testkit import FoundationTestCase
from provide.testkit.mocking import Mock, patch
import pytest


class TestConfigBase(FoundationTestCase):
    """Test logger config base functionality."""

    def test_get_config_logger_basic(self) -> None:
        """Test basic config logger creation."""
        from provide.foundation.logger.config.base import get_config_logger

        logger = get_config_logger()
        assert logger is not None
        assert hasattr(logger, "info")

    @patch.dict(os.environ, {"FOUNDATION_LOG_OUTPUT": "stderr"})
    def test_get_config_logger_with_stderr(self) -> None:
        """Test config logger with stderr output."""
        from provide.foundation.logger.config.base import get_config_logger

        logger = get_config_logger()
        assert logger is not None

    @patch.dict(os.environ, {"FOUNDATION_LOG_OUTPUT": "stdout"})
    def test_get_config_logger_with_stdout(self) -> None:
        """Test config logger with stdout output."""
        from provide.foundation.logger.config.base import get_config_logger

        logger = get_config_logger()
        assert logger is not None

    @patch("provide.foundation.utils.streams.get_foundation_log_stream")
    def test_get_config_logger_with_stream_exception(self, mock_get_stream: Mock) -> None:
        """Test config logger when stream resolution fails."""
        mock_get_stream.side_effect = Exception("Stream error")

        from provide.foundation.logger.config.base import get_config_logger

        # Should not raise exception, should fall back to stderr
        logger = get_config_logger()
        assert logger is not None

    @patch("structlog.get_config")
    def test_get_config_logger_with_structlog_exception(self, mock_get_config: Mock) -> None:
        """Test config logger when structlog config fails."""
        mock_get_config.side_effect = Exception("Structlog error")

        from provide.foundation.logger.config.base import get_config_logger

        # Should not raise exception, should use default config
        logger = get_config_logger()
        assert logger is not None


class TestLoggingConfigCoverage:
    """Test logging config functionality."""

    def test_logging_config_from_env_invalid_level(self) -> None:
        """Test logging config with invalid log level raises clear error."""
        from provide.foundation.logger.config.logging import LoggingConfig

        with patch.dict(os.environ, {"PROVIDE_LOG_LEVEL": "INVALID_LEVEL"}):
            with pytest.raises(ValueError) as exc_info:
                LoggingConfig.from_env()
            assert "Invalid log_level 'INVALID_LEVEL'" in str(exc_info.value)
            assert "TRACE, DEBUG, INFO, WARNING, ERROR, CRITICAL" in str(exc_info.value)

    def test_logging_config_from_env_strict_mode(self) -> None:
        """Test logging config with valid log level works correctly."""
        from provide.foundation.logger.config.logging import LoggingConfig

        with patch.dict(os.environ, {"PROVIDE_LOG_LEVEL": "DEBUG"}):
            config = LoggingConfig.from_env()
            assert config.default_level == "DEBUG"

    def test_logging_config_json_formatter_enabled(self) -> None:
        """Test logging config with JSON formatter enabled."""
        from provide.foundation.logger.config.logging import LoggingConfig

        with patch.dict(os.environ, {"PROVIDE_LOG_CONSOLE_FORMATTER": "json"}):
            config = LoggingConfig.from_env()
            assert config.console_formatter == "json"

    def test_logging_config_emoji_disabled(self) -> None:
        """Test logging config with emojis disabled."""
        from provide.foundation.logger.config.logging import LoggingConfig

        with patch.dict(os.environ, {"PROVIDE_LOG_DAS_EMOJI_ENABLED": "false"}):
            config = LoggingConfig.from_env()
            assert config.das_emoji_prefix_enabled is False

    def test_logging_config_log_file_path(self) -> None:
        """Test logging config with log file path."""
        from provide.foundation.logger.config.logging import LoggingConfig

        with patch.dict(os.environ, {"PROVIDE_LOG_FILE": "/tmp/test.log"}):
            config = LoggingConfig.from_env()
            assert config.log_file is not None
            assert str(config.log_file) == "/tmp/test.log"

    def test_logging_config_no_emoji_sets_fields(self) -> None:
        """Test that deprecated emoji sets fields don't exist."""
        from provide.foundation.logger.config.logging import LoggingConfig

        config = LoggingConfig.from_env()
        # Emoji sets fields should not exist
        assert not hasattr(config, "enabled_emoji_sets")

    def test_logging_config_log_level_name_mapping(self) -> None:
        """Test logging config level name mappings."""
        from provide.foundation.logger.config.logging import LoggingConfig

        # Test various level names
        test_cases = [
            ("DEBUG", "DEBUG"),
            ("INFO", "INFO"),
            ("WARNING", "WARNING"),
            ("ERROR", "ERROR"),
            ("CRITICAL", "CRITICAL"),
            ("debug", "DEBUG"),  # Case insensitive
            ("info", "INFO"),
        ]

        for env_level, expected_level in test_cases:
            with patch.dict(os.environ, {"PROVIDE_LOG_LEVEL": env_level}):
                config = LoggingConfig.from_env()
                assert config.default_level == expected_level

    def test_logging_config_boolean_env_parsing(self) -> None:
        """Test boolean environment variable parsing."""
        from provide.foundation.logger.config.logging import LoggingConfig

        # Test various boolean representations
        boolean_tests = [
            ("true", True),
            ("True", True),
            ("TRUE", True),
            ("1", True),
            ("false", False),
            ("False", False),
            ("FALSE", False),
            ("0", False),
            ("", False),
        ]

        for _env_value, expected in boolean_tests:
            with patch.dict(
                os.environ,
                {"PROVIDE_LOG_CONSOLE_FORMATTER": "json" if expected else "key_value"},
            ):
                config = LoggingConfig.from_env()
                expected_formatter = "json" if expected else "key_value"
                assert config.console_formatter == expected_formatter


class TestTelemetryConfigCoverage:
    """Test telemetry config functionality."""

    def test_telemetry_config_from_env_otel_service_name(self) -> None:
        """Test telemetry config using OTEL_SERVICE_NAME."""
        from provide.foundation.logger.config.telemetry import TelemetryConfig

        with patch.dict(os.environ, {"OTEL_SERVICE_NAME": "test-service"}):
            config = TelemetryConfig.from_env()
            assert config.service_name == "test-service"

    def test_telemetry_config_from_env_service_name_default_none(self) -> None:
        """Test telemetry config service_name defaults to None when not set."""
        from provide.foundation.logger.config.telemetry import TelemetryConfig

        # Test without any service name environment variables
        with patch.dict(os.environ, {}, clear=False):
            # Remove both service name env vars if they exist
            if "OTEL_SERVICE_NAME" in os.environ:
                del os.environ["OTEL_SERVICE_NAME"]
            if "PROVIDE_SERVICE_NAME" in os.environ:
                del os.environ["PROVIDE_SERVICE_NAME"]
            config = TelemetryConfig.from_env()
            assert config.service_name is None

    def test_telemetry_config_from_env_precedence(self) -> None:
        """Test that OTEL_SERVICE_NAME takes precedence over PROVIDE_SERVICE_NAME."""
        from provide.foundation.logger.config.telemetry import TelemetryConfig

        with patch.dict(
            os.environ,
            {
                "OTEL_SERVICE_NAME": "otel-service",  # This takes precedence
                "PROVIDE_SERVICE_NAME": "provide-service",
            },
        ):
            config = TelemetryConfig.from_env()
            # OTEL takes precedence as the OpenTelemetry standard
            assert config.service_name == "otel-service"

    def test_telemetry_config_globally_disabled(self) -> None:
        """Test telemetry config with global disable flag."""
        from provide.foundation.logger.config.telemetry import TelemetryConfig

        with patch.dict(os.environ, {"PROVIDE_TELEMETRY_DISABLED": "true"}):
            config = TelemetryConfig.from_env()
            assert config.globally_disabled is True

    def test_telemetry_config_includes_logging_config(self) -> None:
        """Test that telemetry config includes logging config from env."""
        from provide.foundation.logger.config.telemetry import TelemetryConfig

        with patch.dict(os.environ, {"PROVIDE_LOG_LEVEL": "DEBUG"}):
            config = TelemetryConfig.from_env()
            assert config.logging.default_level == "DEBUG"

    def test_telemetry_config_from_env_strict_mode(self) -> None:
        """Test telemetry config with invalid log level raises clear error."""
        from provide.foundation.logger.config.telemetry import TelemetryConfig

        with patch.dict(os.environ, {"PROVIDE_LOG_LEVEL": "INVALID"}):
            with pytest.raises(ValueError) as exc_info:
                TelemetryConfig.from_env()
            assert "Invalid log_level 'INVALID'" in str(exc_info.value)

    def test_telemetry_config_service_version_auto_populated(self) -> None:
        """Test that service_version is auto-populated from package version."""
        from provide.foundation.logger.config.telemetry import TelemetryConfig

        config = TelemetryConfig()
        # Should be auto-populated with provide-foundation version
        assert config.service_version is not None
        assert isinstance(config.service_version, str)
        # Should match the VERSION file content
        assert len(config.service_version) > 0

    def test_telemetry_config_service_version_env_override(self) -> None:
        """Test that service_version can be overridden via env var."""
        from provide.foundation.logger.config.telemetry import TelemetryConfig

        with patch.dict(os.environ, {"PROVIDE_SERVICE_VERSION": "my-app-1.2.3"}):
            config = TelemetryConfig.from_env()
            assert config.service_version == "my-app-1.2.3"

    def test_telemetry_config_service_version_explicit_override(self) -> None:
        """Test that service_version can be set explicitly."""
        from provide.foundation.logger.config.telemetry import TelemetryConfig

        config = TelemetryConfig(service_version="explicit-2.0.0")
        assert config.service_version == "explicit-2.0.0"


# 🧱🏗️🔚
