#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Documentation examples tests for lazy initialization.

Tests that verify examples from documentation work correctly,
including basic usage, named loggers, environment configuration, and migration."""

from __future__ import annotations

import contextlib
import json
import os

from provide.testkit import FoundationTestCase
from provide.testkit.mocking import patch
import pytest
from pytest import CaptureFixture

from provide.foundation import (
    LoggingConfig,
    TelemetryConfig,
    get_hub,
)

# Mark all tests in this file to run serially to avoid global state pollution
pytestmark = pytest.mark.serial


class TestLazyInitializationDocumentation(FoundationTestCase):
    """Tests that verify examples from documentation work correctly."""

    def test_basic_usage_example(self, capsys: CaptureFixture) -> None:
        """Test the basic usage example from documentation."""
        import sys

        from provide.testkit import set_log_stream_for_testing

        os.environ["PROVIDE_LOG_LEVEL"] = "INFO"

        # Set up Foundation to log to stderr so capsys can capture it
        set_log_stream_for_testing(sys.stderr)

        # Example from docs: immediate logging without setup
        from provide.foundation import logger

        logger.info("Application started", version="1.0.0")
        logger.debug("Debug information", component="main")
        logger.warning("This is a warning", code="W001")
        logger.error("An error occurred", error_code="E123")

        captured = capsys.readouterr()
        assert "Application started" in captured.err
        assert "This is a warning" in captured.err
        assert "An error occurred" in captured.err
        # Debug might be filtered depending on default level

    def test_named_logger_example(self, capsys: CaptureFixture) -> None:
        """Test the named logger example from documentation."""
        import sys

        from provide.testkit import set_log_stream_for_testing

        os.environ["PROVIDE_LOG_LEVEL"] = "INFO"
        set_log_stream_for_testing(sys.stderr)

        # Example from docs: component-specific loggers
        from provide.foundation import logger

        auth_logger = logger.get_logger("auth.service")
        db_logger = logger.get_logger("database.connection")
        api_logger = logger.get_logger("api.handlers")

        auth_logger.info("User authentication successful", user_id=12345)
        db_logger.warning("Connection timeout", host="localhost", timeout_ms=5000)
        api_logger.debug("Request processed", endpoint="/api/users", duration_ms=23)

        captured = capsys.readouterr()
        assert "User authentication successful" in captured.err
        assert "Connection timeout" in captured.err

    def test_environment_config_example(self, capsys: CaptureFixture) -> None:
        """Test the environment configuration example from documentation."""
        import sys

        from provide.testkit import set_log_stream_for_testing

        os.environ["PROVIDE_LOG_LEVEL"] = "INFO"
        set_log_stream_for_testing(sys.stderr)

        # Example from docs: environment-based configuration
        with patch.dict(
            os.environ,
            {
                "PROVIDE_SERVICE_NAME": "my-service",
                "PROVIDE_LOG_LEVEL": "INFO",
                "PROVIDE_LOG_CONSOLE_FORMATTER": "json",
                "PROVIDE_LOG_MODULE_LEVELS": "auth:DEBUG,db:ERROR",
                "PROVIDE_LOG_SANITIZATION_ENABLED": "false",  # Disable to avoid masking test messages
            },
        ):
            # Force re-initialization with new environment variables
            from provide.testkit import reset_foundation_setup_for_testing

            reset_foundation_setup_for_testing()
            set_log_stream_for_testing(sys.stderr)

            from provide.foundation import logger

            logger.info("Service started")

            auth_logger = logger.get_logger("auth")
            auth_logger.debug("Auth debug message")  # Should appear

            db_logger = logger.get_logger("db")
            db_logger.warning("DB warning")  # Should be filtered
            db_logger.error("DB error")  # Should appear

        captured = capsys.readouterr()

        # Parse JSON output
        json_lines = []
        for line in captured.err.splitlines():
            if line.strip() and not line.startswith("["):
                with contextlib.suppress(json.JSONDecodeError):
                    json_lines.append(json.loads(line))

        # Verify example worked as documented
        service_logs = [log for log in json_lines if "service_name" in log]
        assert all(log["service_name"] == "my-service" for log in service_logs)

        assert any("Auth debug message" in log.get("event", "") for log in json_lines)
        assert not any("DB warning" in log.get("event", "") for log in json_lines)
        assert any("DB error" in log.get("event", "") for log in json_lines)

    def test_migration_example(self, capsys: CaptureFixture) -> None:
        """Test the migration example from documentation."""
        import sys

        from provide.testkit import set_log_stream_for_testing

        os.environ["PROVIDE_LOG_LEVEL"] = "INFO"
        set_log_stream_for_testing(sys.stderr)

        # Example from docs: gradual migration
        from provide.foundation import (
            logger,
        )

        # Old code: works immediately without setup
        logger.info("Legacy code logging")

        # New code: explicit setup still works
        config = TelemetryConfig(
            service_name="migrated-service",
            logging=LoggingConfig(
                default_level="INFO",
                console_formatter="json",
            ),
        )
        hub = get_hub()
        hub.initialize_foundation(config, force=True)

        # Both old and new code work together
        logger.info("After explicit setup")

        captured = capsys.readouterr()
        assert "Legacy code logging" in captured.err
        assert "After explicit setup" in captured.err

        # After explicit setup, should be JSON format
        json_lines = [
            line
            for line in captured.err.splitlines()
            if line.strip() and not line.startswith("[") and "After explicit setup" in line
        ]
        assert len(json_lines) > 0

        log_data = json.loads(json_lines[0])
        assert log_data["service_name"] == "migrated-service"


# 🧱🏗️🔚
