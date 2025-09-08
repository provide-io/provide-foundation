#
# tests/test_lazy_initialization_integration.py
#

"""
Production readiness, compliance, and documentation tests for lazy initialization.

This module tests production-ready scenarios, documented behavior compliance,
and performance requirements for lazy initialization functionality.
"""

import asyncio
from concurrent.futures import ThreadPoolExecutor, as_completed
import contextlib
import json
import os
import threading
import time
from typing import Any
from unittest.mock import patch

import pytest
from pytest import CaptureFixture  # Added for capsys

from provide.foundation import (
    LoggingConfig,
    TelemetryConfig,
    logger as global_logger,
    setup_telemetry,
    shutdown_foundation_telemetry,
)
from provide.foundation.testing import reset_foundation_setup_for_testing
from tests.utils import TestEnvironment


class TestProductionReadinessScenarios:
    """Tests that verify production readiness of lazy initialization."""

    def test_high_throughput_scenario(self, capsys: CaptureFixture) -> None:
        """Test lazy initialization under high throughput."""
        from provide.foundation.testing import set_log_stream_for_testing
        import sys

        reset_foundation_setup_for_testing()
        set_log_stream_for_testing(sys.stderr)

        # Simulate high-throughput logging
        start_time = time.time()
        message_count = 1000

        for i in range(message_count):
            global_logger.info(f"High throughput message {i}", iteration=i)

        end_time = time.time()
        duration = end_time - start_time

        captured = capsys.readouterr()

        # Verify all messages were logged
        log_lines = [
            line
            for line in captured.err.splitlines()
            if "High throughput message" in line
        ]
        assert len(log_lines) == message_count

        # Verify reasonable performance
        messages_per_second = message_count / duration
        assert messages_per_second > 100, f"Too slow: {messages_per_second:.1f} msg/sec"

    def test_memory_stability_scenario(self, capsys: CaptureFixture) -> None:
        """Test memory stability with lazy initialization over time."""
        from provide.foundation.testing import set_log_stream_for_testing
        import sys

        reset_foundation_setup_for_testing()
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
        from provide.foundation.testing import set_log_stream_for_testing
        import sys

        reset_foundation_setup_for_testing()
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
        from provide.foundation.testing import set_log_stream_for_testing
        import sys

        reset_foundation_setup_for_testing()
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
        import asyncio

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
        from provide.foundation.testing import set_log_stream_for_testing
        import sys

        reset_foundation_setup_for_testing()
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
            # Test each documented feature
            global_logger.debug("Debug message")  # Should appear (DEBUG level)

            # Test module-specific level
            test_logger = global_logger.get_logger("test.module")
            test_logger.warning(
                "Module warning"
            )  # Should be filtered (ERROR level only)
            test_logger.error("Module error")  # Should appear

            # Test DAS with disabled logger name emoji
            global_logger.info(
                "DAS test", domain="auth", action="login", status="success"
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
        assert all("timestamp" not in log for log in json_lines), (
            "Timestamps should be omitted"
        )

        # Verify module filtering
        assert not any("Module warning" in log.get("event", "") for log in json_lines)
        assert any("Module error" in log.get("event", "") for log in json_lines)

        # Verify DAS emoji without logger name emoji
        das_logs = [log for log in json_lines if "DAS test" in log.get("event", "")]
        assert len(das_logs) == 1
        assert "[🔑][➡️][✅]" in das_logs[0]["event"]
        # Should NOT have logger name emoji prefix before DAS

    def test_backward_compatibility_promise(self, capsys: CaptureFixture) -> None:
        """Test that lazy initialization maintains backward compatibility."""
        from provide.foundation.testing import set_log_stream_for_testing
        import sys

        reset_foundation_setup_for_testing()
        set_log_stream_for_testing(sys.stderr)

        # Old code pattern: immediate logging without setup
        global_logger.info("Legacy immediate logging")

        # Old code pattern: named logger creation
        legacy_logger = global_logger.get_logger("legacy.component")
        legacy_logger.warning("Legacy component warning")

        # Old code pattern: exception logging
        try:
            raise RuntimeError("Legacy exception")
        except RuntimeError:
            legacy_logger.exception("Legacy exception handling")

        # Should work exactly as before
        captured = capsys.readouterr()
        assert "Legacy immediate logging" in captured.err
        assert "Legacy component warning" in captured.err
        assert "Legacy exception handling" in captured.err
        assert "RuntimeError: Legacy exception" in captured.err

    def test_thread_safety_guarantees(self, capsys: CaptureFixture) -> None:
        """Test documented thread safety guarantees."""
        from provide.foundation.testing import set_log_stream_for_testing
        import sys

        reset_foundation_setup_for_testing()
        set_log_stream_for_testing(sys.stderr)

        import time

        # Stress test with many threads starting simultaneously
        thread_count = 50
        barrier = threading.Barrier(thread_count)
        results: dict[int, bool] = {}
        errors: list[Exception] = []

        def stress_worker(worker_id: int) -> None:
            try:
                # Synchronize start time for maximum contention
                barrier.wait()

                # Each thread creates its own logger and logs
                worker_logger = global_logger.get_logger(f"stress.worker.{worker_id}")

                for i in range(10):
                    worker_logger.info(f"Worker {worker_id} message {i}")
                    time.sleep(0.001)  # Small delay to increase contention

                results[worker_id] = True

            except Exception as e:
                errors.append(e)
                results[worker_id] = False

        # Start all threads
        threads = []
        for i in range(thread_count):
            thread = threading.Thread(target=stress_worker, args=(i,))
            threads.append(thread)
            thread.start()

        # Wait for completion
        for thread in threads:
            thread.join(timeout=30.0)
            assert not thread.is_alive(), "Thread failed to complete"

        # Verify thread safety
        assert len(errors) == 0, f"Thread safety violated with errors: {errors}"
        assert len(results) == thread_count
        assert all(results.values()), "Some threads failed"

        # Verify all messages were logged
        captured = capsys.readouterr()
        for worker_id in range(thread_count):
            for i in range(10):
                assert f"Worker {worker_id} message {i}" in captured.err

    def test_performance_requirements(self, capsys: CaptureFixture) -> None:
        """Test that lazy initialization meets performance requirements."""
        from provide.foundation.testing import set_log_stream_for_testing
        import sys

        reset_foundation_setup_for_testing()
        set_log_stream_for_testing(sys.stderr)

        import time

        # Test initialization overhead
        start_time = time.time()

        # First log should include initialization time
        global_logger.info("First message triggers initialization")

        init_time = time.time() - start_time

        # Subsequent logs should be fast
        start_time = time.time()

        for i in range(100):
            global_logger.info(f"Performance test message {i}")

        subsequent_time = time.time() - start_time

        # Performance requirements
        assert init_time < 0.1, f"Initialization too slow: {init_time:.3f}s"

        messages_per_second = 100 / subsequent_time
        assert messages_per_second > 1000, (
            f"Subsequent logging too slow: {messages_per_second:.1f} msg/sec"
        )

        captured = capsys.readouterr()
        assert "First message triggers initialization" in captured.err


class TestLazyInitializationDocumentation:
    """Tests that verify examples from documentation work correctly."""

    def test_basic_usage_example(self, capsys: CaptureFixture) -> None:
        """Test the basic usage example from documentation."""
        from provide.foundation.testing import set_log_stream_for_testing
        import sys

        reset_foundation_setup_for_testing()

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
        from provide.foundation.testing import set_log_stream_for_testing
        import sys

        reset_foundation_setup_for_testing()
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
        from provide.foundation.testing import set_log_stream_for_testing
        import sys

        reset_foundation_setup_for_testing()
        set_log_stream_for_testing(sys.stderr)

        # Example from docs: environment-based configuration
        with patch.dict(
            os.environ,
            {
                "PROVIDE_SERVICE_NAME": "my-service",
                "PROVIDE_LOG_LEVEL": "INFO",
                "PROVIDE_LOG_CONSOLE_FORMATTER": "json",
                "PROVIDE_LOG_MODULE_LEVELS": "auth:DEBUG,db:ERROR",
            },
        ):
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
        from provide.foundation.testing import set_log_stream_for_testing
        import sys

        reset_foundation_setup_for_testing()
        set_log_stream_for_testing(sys.stderr)

        # Example from docs: gradual migration
        from provide.foundation import (
            LoggingConfig,
            TelemetryConfig,
            logger,
            setup_telemetry,
        )

        # Old code: works immediately without setup
        logger.info("Legacy code logging")

        # New code: explicit setup still works
        config = TelemetryConfig(
            service_name="migrated-service",
            logging=LoggingConfig(console_formatter="json"),
        )
        setup_telemetry(config)

        # Both old and new code work together
        logger.info("After explicit setup")

        captured = capsys.readouterr()
        assert "Legacy code logging" in captured.err
        assert "After explicit setup" in captured.err

        # After explicit setup, should be JSON format
        json_lines = [
            line
            for line in captured.err.splitlines()
            if line.strip()
            and not line.startswith("[")
            and "After explicit setup" in line
        ]
        assert len(json_lines) > 0

        log_data = json.loads(json_lines[0])
        assert log_data["service_name"] == "migrated-service"


# 🧪🎯