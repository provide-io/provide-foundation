"""Test asyncio debug message suppression via module-level log configuration."""

import asyncio
import logging
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

    def test_asyncio_debug_messages_suppressed(self):
        """Test that asyncio debug messages are suppressed in logging output."""
        # Create a string buffer to capture log output and set up handler
        log_output = StringIO()

        # Configure Foundation logging
        config = TelemetryConfig.from_env()
        configure_structlog_output(config, log_output)

        # Set up handler to capture stdlib logging messages
        asyncio_logger = logging.getLogger("asyncio")
        handler = logging.StreamHandler(log_output)
        handler.setLevel(logging.DEBUG)
        asyncio_logger.addHandler(handler)

        try:
            # Log a debug message that should be suppressed
            asyncio_logger.debug("Using selector: KqueueSelector")

            # Verify no debug message was written (due to module-level filtering)
            captured_output = log_output.getvalue()
            assert "Using selector: KqueueSelector" not in captured_output
            assert "KqueueSelector" not in captured_output

        finally:
            # Clean up handler
            asyncio_logger.removeHandler(handler)

    def test_asyncio_info_messages_still_logged(self):
        """Test that asyncio INFO and higher messages are still logged."""
        # Create a string buffer to capture log output
        log_output = StringIO()

        # Configure with default settings
        config = TelemetryConfig.from_env()
        configure_structlog_output(config, log_output)

        # Get the asyncio logger and log an info message
        asyncio_logger = logging.getLogger("asyncio")
        asyncio_logger.info("Important asyncio information")

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
            other_logger = logging.getLogger("test.module")
            other_logger.debug("Debug message from other module")

            # Verify the debug message was written
            captured_output = log_output.getvalue()
            assert "Debug message from other module" in captured_output

    @pytest.mark.asyncio
    async def test_actual_asyncio_selector_message_suppressed(self):
        """Test suppression with actual asyncio selector events."""
        # Create a string buffer to capture log output
        log_output = StringIO()

        # Configure logging with DEBUG level but asyncio at INFO
        with patch.dict("os.environ", {"PROVIDE_LOG_LEVEL": "DEBUG"}):
            config = TelemetryConfig.from_env()
            configure_structlog_output(config, log_output)

            # Enable asyncio debug mode to trigger selector messages
            asyncio.get_event_loop().set_debug(True)

            try:
                # Create a simple async operation to potentially trigger selector logs
                await asyncio.sleep(0.001)

                # Check that no selector debug messages were captured
                captured_output = log_output.getvalue()
                assert "selector" not in captured_output.lower()
                assert "kqueue" not in captured_output.lower()

            finally:
                # Clean up debug mode
                asyncio.get_event_loop().set_debug(False)

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

            # Get the asyncio logger and attempt to log a debug message
            asyncio_logger = logging.getLogger("asyncio")
            asyncio_logger.debug("Debug selector information")

            # Verify the debug message was written since we overrode to DEBUG
            captured_output = log_output.getvalue()
            assert "Debug selector information" in captured_output