"""Test asyncio debug message suppression via module-level log configuration."""

import asyncio
import os
from io import StringIO
from unittest.mock import patch

import pytest
import structlog

from provide.foundation.logger.config import TelemetryConfig
from provide.foundation.logger.setup.processors import configure_structlog_output


class TestAsyncioDebugSuppression:
    """Test that asyncio debug messages are properly suppressed."""

    def test_default_module_levels_includes_asyncio(self):
        """Test that default configuration includes asyncio at INFO level."""
        config = TelemetryConfig.from_env()
        assert "asyncio" in config.logging.module_levels
        assert config.logging.module_levels["asyncio"] == "INFO"

    def test_structlog_asyncio_debug_messages_suppressed(self):
        """Test that structlog asyncio debug messages are suppressed."""
        # Create a string buffer to capture log output
        log_output = StringIO()

        # Configure Foundation logging with WARNING overall level (higher than asyncio's INFO)
        # so that the module-level filtering is the limiting factor
        with patch.dict("os.environ", {"PROVIDE_LOG_LEVEL": "WARNING"}):
            config = TelemetryConfig.from_env()
            configure_structlog_output(config, log_output)

            # Get a structlog logger for asyncio namespace
            logger = structlog.get_logger("asyncio")

            # Log a debug message that should be suppressed
            logger.debug("Using selector: KqueueSelector")

            # Verify no debug message was written (due to module-level filtering)
            captured_output = log_output.getvalue()
            assert "Using selector: KqueueSelector" not in captured_output
            assert "KqueueSelector" not in captured_output

    def test_structlog_asyncio_info_messages_still_logged(self):
        """Test that structlog asyncio INFO and higher messages are still logged."""
        # Create a string buffer to capture log output
        log_output = StringIO()

        # Configure with default settings
        config = TelemetryConfig.from_env()
        configure_structlog_output(config, log_output)

        # Get a structlog logger for asyncio namespace
        logger = structlog.get_logger("asyncio")

        # Log an info message that should pass through
        logger.info("Important asyncio information")

        # Verify the info message was written
        captured_output = log_output.getvalue()
        assert "Important asyncio information" in captured_output

    def test_other_modules_debug_messages_not_affected(self):
        """Test that debug messages from other modules are not suppressed."""
        # Create a string buffer to capture log output
        log_output = StringIO()

        # Configure with default settings but set overall level to DEBUG
        with patch.dict("os.environ", {"PROVIDE_LOG_LEVEL": "DEBUG"}):
            config = TelemetryConfig.from_env()
            configure_structlog_output(config, log_output)

            # Get a non-asyncio logger and log a debug message
            logger = structlog.get_logger("test.module")
            logger.debug("Debug message from other module")

            # Verify the debug message was written
            captured_output = log_output.getvalue()
            assert "Debug message from other module" in captured_output

    def test_env_var_override_allows_asyncio_debug(self):
        """Test that environment variable can override asyncio suppression."""
        # Create a string buffer to capture log output
        log_output = StringIO()

        # Override via environment to allow asyncio DEBUG messages
        with patch.dict("os.environ", {
            "PROVIDE_LOG_LEVEL": "DEBUG",
            "PROVIDE_LOG_MODULE_LEVELS": "asyncio:DEBUG"
        }):
            config = TelemetryConfig.from_env()
            configure_structlog_output(config, log_output)

            # Verify asyncio is set to DEBUG level
            assert config.logging.module_levels["asyncio"] == "DEBUG"

            # Get a structlog logger for asyncio namespace
            logger = structlog.get_logger("asyncio")
            logger.debug("Debug selector information")

            # Verify the debug message was written since we overrode to DEBUG
            captured_output = log_output.getvalue()
            assert "Debug selector information" in captured_output

    def test_module_levels_parsing_with_multiple_modules(self):
        """Test that multiple module levels can be configured via environment."""
        with patch.dict("os.environ", {
            "PROVIDE_LOG_MODULE_LEVELS": "asyncio:WARNING,urllib3:ERROR,requests:INFO"
        }):
            config = TelemetryConfig.from_env()

            assert config.logging.module_levels["asyncio"] == "WARNING"
            assert config.logging.module_levels["urllib3"] == "ERROR"
            assert config.logging.module_levels["requests"] == "INFO"

    @pytest.mark.asyncio
    async def test_real_asyncio_integration_example(self):
        """Integration test showing how asyncio debug suppression works in practice."""
        # Create a string buffer to capture log output
        log_output = StringIO()

        # Use DEBUG overall level but asyncio at INFO level to test module-specific filtering
        with patch.dict("os.environ", {"PROVIDE_LOG_LEVEL": "DEBUG"}):
            # Clear structlog configuration to ensure clean test
            structlog.reset_defaults()

            config = TelemetryConfig.from_env()
            configure_structlog_output(config, log_output)

            # Simulate what would happen if asyncio itself logged through Foundation
            # (This is more of a demonstration of the filtering mechanism)
            asyncio_logger = structlog.get_logger("asyncio.selector_events")

            # These debug messages should be suppressed
            asyncio_logger.debug("Using selector: KqueueSelector", file="selector_events.py", line=54)
            asyncio_logger.debug("Selector timeout: 1.0", file="selector_events.py", line=67)

            # This info message should pass through
            asyncio_logger.info("Event loop started", file="base_events.py", line=123)

            captured_output = log_output.getvalue()

            # Verify debug messages are suppressed but info messages pass through
            assert "KqueueSelector" not in captured_output
            assert "Selector timeout" not in captured_output
            assert "Event loop started" in captured_output