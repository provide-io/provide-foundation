#
# tests/test_lazy_initialization_integration.py
#

"""Production readiness, compliance, and documentation tests for lazy initialization.

This module tests production-ready scenarios, documented behavior compliance,
and performance requirements for lazy initialization functionality.
"""

import asyncio
import contextlib
import json
import os
import threading
import time
from unittest.mock import patch

from provide.testkit import TestEnvironment, reset_foundation_setup_for_testing
import pytest
from pytest import CaptureFixture  # Added for capsys

from provide.foundation import (
    LoggingConfig,
    TelemetryConfig,
    get_hub,
    logger as global_logger,
    shutdown_foundation_telemetry,
)


class TestProductionReadinessScenarios:
    """Tests that verify production readiness of lazy initialization."""

    def test_high_throughput_scenario(self, captured_stderr_for_foundation) -> None:
        """Test lazy initialization under high throughput."""

        os.environ["PROVIDE_LOG_LEVEL"] = "INFO"
        reset_foundation_setup_for_testing()

        # Simulate high-throughput logging
        start_time = time.time()
        message_count = 1000

        for i in range(message_count):
            global_logger.info(f"High throughput message {i}", iteration=i)

        end_time = time.time()
        duration = end_time - start_time

        # Get captured output from our fixture
        captured_stderr_for_foundation.seek(0)
        captured_content = captured_stderr_for_foundation.getvalue()

        # Verify all messages were logged
        log_lines = [line for line in captured_content.splitlines() if "High throughput message" in line]
        assert len(log_lines) == message_count

        # Verify reasonable performance
        messages_per_second = message_count / duration
        assert messages_per_second > 100, f"Too slow: {messages_per_second:.1f} msg/sec"

    def test_memory_stability_scenario(self, capsys: CaptureFixture) -> None:
        """Test memory stability with lazy initialization over time."""
        import sys

        from provide.testkit import set_log_stream_for_testing

        reset_foundation_setup_for_testing()
        os.environ["PROVIDE_LOG_LEVEL"] = "INFO"
        set_log_stream_for_testing(sys.stderr)

        import gc

        # Baseline memory
        gc.collect()
        initial_objects = len(gc.get_objects())

        # Create many logger instances and log messages
        for i in range(100):
            logger_instance = global_logger.get_logger(f"memory.test.{i}")
            logger_instance.info(f"Memory test message {i}")

            # Periodically force garbage collection
            if i % 20 == 0:
                gc.collect()

        # Final memory check
        gc.collect()
        final_objects = len(gc.get_objects())

        object_growth = final_objects - initial_objects

        # Growth should be reasonable (not linear with logger count)
        assert object_growth < 500, f"Excessive memory growth: {object_growth} objects"

    def test_error_resilience_scenario(self, capsys: CaptureFixture) -> None:
        """Test error resilience in production-like conditions."""
        import sys

        from provide.testkit import set_log_stream_for_testing

        reset_foundation_setup_for_testing()
        os.environ["PROVIDE_LOG_LEVEL"] = "INFO"
        set_log_stream_for_testing(sys.stderr)

        # Simulate various error conditions
        error_scenarios = [
            ("network_error", ConnectionError("Network unavailable")),
            ("data_error", ValueError("Invalid data format")),
            ("permission_error", PermissionError("Access denied")),
            ("system_error", OSError("System resource unavailable")),
        ]

        for error_name, exception in error_scenarios:
            try:
                raise exception
            except Exception:
                global_logger.exception(
                    f"Handling {error_name}",
                    error_type=error_name,
                    domain="system",
                    action="error_handling",
                    status="handled",
                )

        # Continue normal logging after errors
        global_logger.info("System recovered after error handling")

        captured = capsys.readouterr()

        # Verify all errors were logged with tracebacks
        for error_name, _ in error_scenarios:
            assert f"Handling {error_name}" in captured.err
            assert "Traceback" in captured.err

        assert "System recovered after error handling" in captured.err

    def test_graceful_shutdown_scenario(self, capsys: CaptureFixture) -> None:
        """Test graceful shutdown with lazy initialization."""
        import sys

        from provide.testkit import set_log_stream_for_testing

        reset_foundation_setup_for_testing()
        os.environ["PROVIDE_LOG_LEVEL"] = "INFO"
        set_log_stream_for_testing(sys.stderr)

        # Simulate application lifecycle
        global_logger.info("Application starting with lazy init")

        # Simulate some work
        for i in range(5):
            worker_logger = global_logger.get_logger(f"worker.{i}")
            worker_logger.info(f"Worker {i} processing")

        # Test graceful shutdown
        async def test_shutdown() -> None:
            await shutdown_foundation_telemetry()

        # Run shutdown

        asyncio.run(test_shutdown())

        # Log after shutdown (should still work)
        global_logger.info("Message after shutdown")

        captured = capsys.readouterr()
        assert "Application starting with lazy init" in captured.err
        assert "Message after shutdown" in captured.err


class TestDocumentedBehaviorCompliance:
    """Tests that verify compliance with documented lazy initialization behavior."""

    def test_documented_environment_variables(self, capsys: CaptureFixture) -> None:
        """Test all documented environment variables work with lazy initialization."""
        import sys

        from provide.testkit import set_log_stream_for_testing

        reset_foundation_setup_for_testing()
        os.environ["PROVIDE_LOG_LEVEL"] = "INFO"
        set_log_stream_for_testing(sys.stderr)

        documented_env_vars = {
            "PROVIDE_LOG_LEVEL": "DEBUG",
            "PROVIDE_LOG_CONSOLE_FORMATTER": "json",
            "PROVIDE_LOG_LOGGER_NAME_EMOJI_ENABLED": "false",
            "PROVIDE_LOG_DAS_EMOJI_ENABLED": "true",
            "PROVIDE_LOG_OMIT_TIMESTAMP": "true",
            "PROVIDE_LOG_MODULE_LEVELS": "test.module:ERROR",
            "PROVIDE_SERVICE_NAME": "documented-service",
            "PROVIDE_TELEMETRY_DISABLED": "false",
        }

        with patch.dict(os.environ, documented_env_vars):
            # Force re-initialization with new environment variables
            reset_foundation_setup_for_testing()
            set_log_stream_for_testing(sys.stderr)

            # Test each documented feature
            global_logger.debug("Debug message")  # Should appear (DEBUG level)

            # Test module-specific level
            test_logger = global_logger.get_logger("test.module")
            test_logger.warning(
                "Module warning",
            )  # Should be filtered (ERROR level only)
            test_logger.error("Module error")  # Should appear

            # Test DAS with disabled logger name emoji
            global_logger.info(
                "DAS test",
                domain="auth",
                action="login",
                status="success",
            )

        captured = capsys.readouterr()

        # Parse JSON output
        json_lines = []
        for line in captured.err.splitlines():
            if line.strip() and not line.startswith("["):
                with contextlib.suppress(json.JSONDecodeError):
                    json_lines.append(json.loads(line))

        # Verify documented behavior
        debug_logs = [log for log in json_lines if log.get("level") == "debug"]
        assert len(debug_logs) > 0, "DEBUG level should appear"

        # Verify service name injection
        service_logs = [log for log in json_lines if "service_name" in log]
        assert all(log["service_name"] == "documented-service" for log in service_logs)

        # Verify timestamp omission
        assert all("timestamp" not in log for log in json_lines), "Timestamps should be omitted"

        # Verify module filtering
        assert not any("Module warning" in log.get("event", "") for log in json_lines)
        assert any("Module error" in log.get("event", "") for log in json_lines)

        # Verify DAS emoji without logger name emoji
        das_logs = [log for log in json_lines if "DAS test" in log.get("event", "")]
        assert len(das_logs) == 1
        assert "[🔑][➡️][✅]" in das_logs[0]["event"]
        # Should NOT have logger name emoji prefix before DAS

    def test_immediate_usage_patterns(self, capsys: CaptureFixture) -> None:
        """Test that lazy initialization supports immediate usage patterns."""
        import sys

        from provide.testkit import set_log_stream_for_testing

        reset_foundation_setup_for_testing()
        os.environ["PROVIDE_LOG_LEVEL"] = "INFO"
        set_log_stream_for_testing(sys.stderr)

        # Immediate logging without explicit setup
        global_logger.info("Immediate logging works")

        # Named logger creation
        component_logger = global_logger.get_logger("component.service")
        component_logger.warning("Component service warning")

        # Exception logging
        try:
            raise RuntimeError("Test exception")
        except RuntimeError:
            component_logger.exception("Exception handling")

        # Verify all patterns work with lazy initialization
        captured = capsys.readouterr()
        assert "Immediate logging works" in captured.err
        assert "Component service warning" in captured.err
        assert "Exception handling" in captured.err
        # Check for exception details (more flexible pattern matching)
        assert "RuntimeError: Test exception" in captured.err or "Test exception" in captured.err, (
            f"Exception details not found in: {captured.err}"
        )

    def test_thread_safety_gu
