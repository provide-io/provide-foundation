#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Test asyncio debug message suppression via module-level log configuration."""

from __future__ import annotations

from io import StringIO

from provide.testkit import FoundationTestCase
from provide.testkit.mocking import patch
import structlog

from provide.foundation.logger.config import TelemetryConfig
from provide.foundation.logger.setup.processors import configure_structlog_output


class TestAsyncioDebugSuppression(FoundationTestCase):
    """Test that asyncio debug messages are properly suppressed."""

    def test_default_module_levels_includes_asyncio(self) -> None:
        """Test that default configuration includes asyncio at INFO level."""
        config = TelemetryConfig.from_env()
        assert "asyncio" in config.logging.module_levels
        assert config.logging.module_levels["asyncio"] == "INFO"

    def test_structlog_asyncio_debug_messages_suppressed(self) -> None:
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

    def test_structlog_asyncio_info_messages_still_logged(self) -> None:
        """Test that structlog asyncio INFO and higher messages are still logged."""
        # Create a string buffer to capture log output
        log_output = StringIO()

        # Configure with INFO overall level so INFO messages from asyncio should pass through
        with patch.dict("os.environ", {"PROVIDE_LOG_LEVEL": "INFO"}):
            config = TelemetryConfig.from_env()
            configure_structlog_output(config, log_output)

            # Get a structlog logger for asyncio namespace
            logger = structlog.get_logger("asyncio")

            # Log an info message that should pass through
            logger.info("Important asyncio information")

            # Verify the info message was written
            captured_output = log_output.getvalue()
            assert "Important asyncio information" in captured_output

    def test_other_modules_debug_messages_not_affected(self) -> None:
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

    def test_env_var_override_allows_asyncio_debug(self) -> None:
        """Test that environment variable can override asyncio suppression."""
        # Create a string buffer to capture log output
        log_output = StringIO()

        # Override via environment to allow asyncio DEBUG messages
        with patch.dict(
            "os.environ", {"PROVIDE_LOG_LEVEL": "DEBUG", "PROVIDE_LOG_MODULE_LEVELS": "asyncio:DEBUG"}
        ):
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

    def test_module_levels_parsing_with_multiple_modules(self) -> None:
        """Test that multiple module levels can be configured via environment."""
        with patch.dict(
            "os.environ", {"PROVIDE_LOG_MODULE_LEVELS": "asyncio:WARNING,urllib3:ERROR,requests:INFO"}
        ):
            config = TelemetryConfig.from_env()

            assert config.logging.module_levels["asyncio"] == "WARNING"
            assert config.logging.module_levels["urllib3"] == "ERROR"
            assert config.logging.module_levels["requests"] == "INFO"

    def test_asyncio_module_hierarchy_filtering(self) -> None:
        """Test that asyncio.* submodules are properly filtered."""
        # Test configuration includes asyncio at INFO level
        config = TelemetryConfig.from_env()
        assert config.logging.module_levels["asyncio"] == "INFO"

        # Test that hierarchical module names should match
        # asyncio.selector_events should be covered by "asyncio" prefix
        module_name = "asyncio.selector_events"
        assert module_name.startswith("asyncio"), "Module hierarchy test should match asyncio prefix"

        # Test that the filtering logic handles hierarchical names correctly
        from provide.foundation.logger.constants import LEVEL_TO_NUMERIC
        from provide.foundation.logger.custom_processors import filter_by_level_custom

        filter_func = filter_by_level_custom(
            config.logging.default_level, config.logging.module_levels, LEVEL_TO_NUMERIC
        )

        # asyncio.selector_events should get the asyncio threshold
        for prefix in filter_func.sorted_module_paths:
            if module_name.startswith(prefix):
                expected_threshold = filter_func.module_numeric_levels[prefix]
                assert expected_threshold == 20, (
                    f"asyncio modules should have INFO level (20), got {expected_threshold}"
                )
                break


# 🧱🏗️🔚
