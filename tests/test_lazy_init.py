#
# test_lazy_init.py
#

"""
Comprehensive tests for lazy initialization functionality in Pyvider telemetry.

This test suite verifies that logging works correctly without explicit setup_telemetry()
calls, maintains thread safety, outputs to stderr by default, and handles various
edge cases and error conditions.
"""
import asyncio
import json
import os
import threading
from typing import Never
from unittest.mock import patch

import pytest
from pytest import CaptureFixture

from pyvider.telemetry import (
    LoggingConfig,
    TelemetryConfig,
    logger as global_logger,
    setup_telemetry,
)
from pyvider.telemetry.core import (
    reset_pyvider_setup_for_testing,
)
from pyvider.telemetry.logger.base import (
    _LAZY_SETUP_STATE,  # Changed from _LAZY_SETUP_DONE, _LAZY_SETUP_ERROR
)


class TestLazyInitializationBasics:
    """Tests basic lazy initialization functionality."""

    def test_lazy_initialization_without_setup(self, capsys: CaptureFixture) -> None:
        """Test that logging works immediately without setup_telemetry()."""
        reset_pyvider_setup_for_testing()

        # Verify initial state - not configured by explicit setup
        assert not global_logger._is_configured_by_setup

        # Log without any setup - should trigger lazy initialization
        global_logger.info("Test message without setup")

        # Verify the message was logged to stderr
        captured = capsys.readouterr()
        assert "Test message without setup" in captured.err
        assert captured.out == ""  # Nothing to stdout

        # Verify lazy setup occurred
        assert global_logger._active_config is not None
        # Should still not be marked as configured by explicit setup
        assert not global_logger._is_configured_by_setup

    def test_lazy_initialization_stderr_default(self, capsys: CaptureFixture) -> None:
        """Test that lazy initialization defaults to stderr output."""
        reset_pyvider_setup_for_testing()

        # Clear any environment variables that might affect output
        with patch.dict(os.environ, {}, clear=True):
            os.environ.update({
                "PYVIDER_LOG_LEVEL": "INFO",
                "PYVIDER_LOG_CONSOLE_FORMATTER": "key_value",
            })

            global_logger.warning("Warning message to stderr")

        captured = capsys.readouterr()
        assert "Warning message to stderr" in captured.err
        assert captured.out == ""

    def test_lazy_initialization_with_environment_config(self, capsys: CaptureFixture) -> None:
        """Test lazy initialization respects environment configuration."""
        reset_pyvider_setup_for_testing()

        with patch.dict(os.environ, {
            "PYVIDER_LOG_LEVEL": "DEBUG",
            "PYVIDER_LOG_CONSOLE_FORMATTER": "json",
            "PYVIDER_SERVICE_NAME": "lazy-test-service",
            "PYVIDER_LOG_LOGGER_NAME_EMOJI_ENABLED": "false",
        }):
            global_logger.debug("Debug message with env config")

        captured = capsys.readouterr()

        # Should be JSON format
        log_lines = [line for line in captured.err.splitlines() if line.strip() and not line.startswith("[")]
        assert len(log_lines) >= 1

        # Parse JSON to verify structure
        log_data = json.loads(log_lines[0])
        assert log_data["event"] == "Debug message with env config"
        assert log_data["level"] == "debug"
        assert log_data["service_name"] == "lazy-test-service"

    def test_lazy_initialization_thread_safety(self, capsys: CaptureFixture) -> None:
        """Test that lazy initialization is thread-safe."""
        reset_pyvider_setup_for_testing()

        results: list[bool] = []
        exceptions: list[Exception] = []

        def worker_thread(thread_id: int) -> None:
            try:
                # All threads should be able to log without issues
                global_logger.info(f"Thread {thread_id} message")
                results.append(True)
            except Exception as e:
                exceptions.append(e)
                results.append(False)

        # Create multiple threads that all try to log simultaneously
        threads = []
        thread_count = 10

        for i in range(thread_count):
            thread = threading.Thread(target=worker_thread, args=(i,))
            threads.append(thread)

        # Start all threads at roughly the same time
        for thread in threads:
            thread.start()

        # Wait for all threads to complete
        for thread in threads:
            thread.join(timeout=5.0)
            assert not thread.is_alive(), "Thread did not complete in time"

        # Verify all threads succeeded
        assert len(exceptions) == 0, f"Threads failed with exceptions: {exceptions}"
        assert len(results) == thread_count
        assert all(results), "Some threads failed to log successfully"

        # Verify all messages were logged
        captured = capsys.readouterr()
        for i in range(thread_count):
            assert f"Thread {i} message" in captured.err

    def test_explicit_setup_after_lazy_initialization(self, capsys: CaptureFixture) -> None:
        """Test that explicit setup_telemetry() works after lazy initialization."""
        reset_pyvider_setup_for_testing()

        # First, trigger lazy initialization
        global_logger.info("Message before explicit setup")

        captured_before = capsys.readouterr()
        assert "Message before explicit setup" in captured_before.err
        assert not global_logger._is_configured_by_setup

        # Now call explicit setup with different config
        explicit_config = TelemetryConfig(
            service_name="explicit-service",
            logging=LoggingConfig(
                console_formatter="json",
                logger_name_emoji_prefix_enabled=False,
            )
        )
        setup_telemetry(explicit_config)

        # Verify explicit setup took precedence
        assert global_logger._is_configured_by_setup
        assert global_logger._active_config.service_name == "explicit-service"

        # Log after explicit setup
        global_logger.info("Message after explicit setup")

        captured_after = capsys.readouterr()
        log_lines = [line for line in captured_after.err.splitlines()
                    if line.strip() and not line.startswith("[")]

        # Should be JSON format with service name
        log_data = json.loads(log_lines[-1])  # Get last log line
        assert log_data["event"] == "Message after explicit setup"
        assert log_data["service_name"] == "explicit-service"

    def test_lazy_initialization_with_module_levels(self, capsys: CaptureFixture) -> None:
        """Test lazy initialization with module-specific log levels."""
        reset_pyvider_setup_for_testing()

        with patch.dict(os.environ, {
            "PYVIDER_LOG_LEVEL": "WARNING",
            "PYVIDER_LOG_MODULE_LEVELS": "test.debug:DEBUG,test.error:ERROR",
        }):
            # These should be filtered (below WARNING)
            global_logger.get_logger("test.default").info("Default info - filtered")
            global_logger.get_logger("test.default").debug("Default debug - filtered")

            # This should appear (module override to DEBUG)
            global_logger.get_logger("test.debug").debug("Debug module debug - shown")
            global_logger.get_logger("test.debug").info("Debug module info - shown")

            # This should be filtered (module override to ERROR)
            global_logger.get_logger("test.error").warning("Error module warning - filtered")

            # This should appear (ERROR level)
            global_logger.get_logger("test.error").error("Error module error - shown")

        captured = capsys.readouterr()
        output_lines = captured.err

        # Verify filtering worked correctly
        assert "Default info - filtered" not in output_lines
        assert "Default debug - filtered" not in output_lines
        assert "Debug module debug - shown" in output_lines
        assert "Debug module info - shown" in output_lines
        assert "Error module warning - filtered" not in output_lines
        assert "Error module error - shown" in output_lines


class TestLazyInitializationEdgeCases:
    """Tests edge cases and error conditions in lazy initialization."""

    def test_lazy_initialization_disabled_globally(self, capsys: CaptureFixture) -> None:
        """Test lazy initialization when telemetry is globally disabled."""
        reset_pyvider_setup_for_testing()

        with patch.dict(os.environ, {"PYVIDER_TELEMETRY_DISABLED": "true"}):
            global_logger.info("Message when disabled")
            global_logger.error("Error when disabled")

        captured = capsys.readouterr()
        # When globally disabled, no application logs should appear
        # Only setup messages might appear
        assert "Message when disabled" not in captured.err
        assert "Error when disabled" not in captured.err

    def test_lazy_initialization_config_error_fallback(self, capsys: CaptureFixture) -> None:
        """Test fallback behavior when configuration fails."""
        reset_pyvider_setup_for_testing()

        # Mock TelemetryConfig.from_env to raise an exception
        with patch('pyvider.telemetry.config.TelemetryConfig.from_env') as mock_from_env:
            mock_from_env.side_effect = Exception("Config loading failed")

            # Should still work with fallback configuration
            global_logger.info("Message with config failure")

        captured = capsys.readouterr()
        # Should still log the message using fallback config
        assert "Message with config failure" in captured.err

    def test_lazy_initialization_structlog_config_error_fallback(self, capsys: CaptureFixture) -> None:
        """Test emergency fallback when structlog configuration fails."""
        reset_pyvider_setup_for_testing()

        # Mock _configure_structlog_output to raise an exception
        with patch('pyvider.telemetry.core._configure_structlog_output') as mock_configure:
            mock_configure.side_effect = Exception("Structlog config failed")

            # Should still work with emergency fallback
            global_logger.error("Emergency fallback message")

        captured = capsys.readouterr()
        # Should log via emergency fallback mechanism
        assert "Emergency fallback message" in captured.err or "Pyvider Emergency" in captured.err

    def test_concurrent_lazy_initialization_race_condition(self, capsys: CaptureFixture) -> None:
        """Test race conditions in concurrent lazy initialization."""
        reset_pyvider_setup_for_testing()

        # Use a barrier to synchronize thread starts for maximum contention
        thread_count = 20
        barrier = threading.Barrier(thread_count)
        results: list[str] = []
        lock = threading.Lock()

        def racing_worker(worker_id: int) -> None:
            # All threads wait here until all are ready
            barrier.wait()

            # Now all threads try to initialize simultaneously
            message = f"Concurrent message {worker_id}"
            global_logger.info(message)

            with lock:
                results.append(message)

        threads = []
        for i in range(thread_count):
            thread = threading.Thread(target=racing_worker, args=(i,))
            threads.append(thread)

        # Start all threads nearly simultaneously
        for thread in threads:
            thread.start()

        # Wait for completion
        for thread in threads:
            thread.join(timeout=10.0)
            assert not thread.is_alive()

        # Verify all messages were processed
        assert len(results) == thread_count

        captured = capsys.readouterr()
        for expected_message in results:
            assert expected_message in captured.err

    def test_lazy_initialization_memory_usage(self, capsys: CaptureFixture) -> None:
        """Test that lazy initialization doesn't cause memory leaks."""
        reset_pyvider_setup_for_testing()

        import gc

        # Get initial memory snapshot
        gc.collect()
        initial_objects = len(gc.get_objects())

        # Trigger lazy initialization multiple times with different loggers
        for i in range(100):
            test_logger = global_logger.get_logger(f"memory.test.{i}")
            test_logger.info(f"Memory test message {i}")

        # Force garbage collection
        gc.collect()
        final_objects = len(gc.get_objects())

        # Memory growth should be reasonable (not exponential)
        object_growth = final_objects - initial_objects
        # Allow some growth but not excessive (adjust threshold as needed)
        assert object_growth < 1000, f"Excessive object growth: {object_growth}"

    def test_reset_after_lazy_initialization(self, capsys: CaptureFixture) -> None:
        """Test that reset works correctly after lazy initialization."""
        reset_pyvider_setup_for_testing()

        # Trigger lazy initialization
        global_logger.info("Before reset")

        captured_before = capsys.readouterr()
        assert "Before reset" in captured_before.err

        # Reset should clear lazy initialization state
        reset_pyvider_setup_for_testing()

        # Verify state was reset
        assert not global_logger._is_configured_by_setup

        # Should be able to initialize again
        global_logger.info("After reset")

        captured_after = capsys.readouterr()
        assert "After reset" in captured_after.err


class TestLazyInitializationCompatibility:
    """Tests compatibility between lazy initialization and existing features."""

    def test_trace_logging_with_lazy_initialization(self, capsys: CaptureFixture) -> None:
        """Test TRACE level logging works with lazy initialization."""
        reset_pyvider_setup_for_testing()

        with patch.dict(os.environ, {
            "PYVIDER_LOG_LEVEL": "INFO",
            "PYVIDER_LOG_MODULE_LEVELS": "trace.test:TRACE",
        }):
            # Regular trace should be filtered
            global_logger.trace("Filtered trace message")

            # Module-specific trace should appear
            global_logger.trace("Shown trace message", _pyvider_logger_name="trace.test")

        captured = capsys.readouterr()
        assert "Filtered trace message" not in captured.err
        assert "Shown trace message" in captured.err

    def test_exception_logging_with_lazy_initialization(self, capsys: CaptureFixture) -> None:
        """Test exception logging works with lazy initialization."""
        reset_pyvider_setup_for_testing()

        try:
            raise ValueError("Test exception for lazy init")
        except ValueError:
            global_logger.exception("Exception occurred during lazy init")

        captured = capsys.readouterr()
        assert "Exception occurred during lazy init" in captured.err
        assert "ValueError: Test exception for lazy init" in captured.err
        assert "Traceback" in captured.err

    def test_das_emoji_with_lazy_initialization(self, capsys: CaptureFixture) -> None:
        """Test Domain-Action-Status emojis work with lazy initialization."""
        reset_pyvider_setup_for_testing()

        with patch.dict(os.environ, {
            "PYVIDER_LOG_CONSOLE_FORMATTER": "key_value",
            "PYVIDER_LOG_DAS_EMOJI_ENABLED": "true",
        }):
            global_logger.info(
                "DAS test message",
                domain="auth",
                action="login",
                status="success"
            )

        captured = capsys.readouterr()
        # Should contain DAS emoji prefix [🔑][➡️][✅]
        assert "[🔑][➡️][✅]" in captured.err
        assert "DAS test message" in captured.err

    @pytest.mark.asyncio
    async def test_async_logging_with_lazy_initialization(self, capsys: CaptureFixture) -> None:
        """Test async logging works with lazy initialization."""
        reset_pyvider_setup_for_testing()

        async def async_task(task_id: int) -> None:
            global_logger.info(f"Async task {task_id} started")
            await asyncio.sleep(0.01)  # Simulate async work
            global_logger.info(f"Async task {task_id} completed")

        # Run multiple async tasks
        await asyncio.gather(
            async_task(1),
            async_task(2),
            async_task(3)
        )

        captured = capsys.readouterr()
        for task_id in [1, 2, 3]:
            assert f"Async task {task_id} started" in captured.err
            assert f"Async task {task_id} completed" in captured.err

    def test_service_name_injection_with_lazy_initialization(self, capsys: CaptureFixture) -> None:
        """Test service name injection works with lazy initialization."""
        reset_pyvider_setup_for_testing()

        # FIXED: Explicitly disable emojis for JSON format to match test expectation
        with patch.dict(os.environ, {
            "PYVIDER_SERVICE_NAME": "lazy-service-test",
            "PYVIDER_LOG_CONSOLE_FORMATTER": "json",
            "PYVIDER_LOG_LOGGER_NAME_EMOJI_ENABLED": "false",
            "PYVIDER_LOG_DAS_EMOJI_ENABLED": "false",
        }):
            global_logger.info("Message with service name")

        captured = capsys.readouterr()
        log_lines = [line for line in captured.err.splitlines()
                    if line.strip() and not line.startswith("[")]

        log_data = json.loads(log_lines[0])
        assert log_data["service_name"] == "lazy-service-test"
        # FIXED: Test expects exact message without emoji prefix
        assert log_data["event"] == "Message with service name"


class TestLazyInitializationInternalState:
    """Tests internal state management during lazy initialization."""

    def test_lazy_setup_done_flag(self, capsys: CaptureFixture) -> None:
        """Test that _LAZY_SETUP_DONE flag is managed correctly."""
        reset_pyvider_setup_for_testing()

        # _LAZY_SETUP_STATE is imported directly now
        # Initially should not be done
        assert not _LAZY_SETUP_STATE["done"]
        assert _LAZY_SETUP_STATE["error"] is None

        # Trigger lazy initialization
        global_logger.info("Trigger lazy setup")

        # Now should be done
        assert _LAZY_SETUP_STATE["done"]
        assert _LAZY_SETUP_STATE["error"] is None

    def test_lazy_setup_error_handling(self, capsys: CaptureFixture) -> None:
        """Test error handling in lazy setup."""
        reset_pyvider_setup_for_testing()

        # Import internal state variables
        # No, _LAZY_SETUP_STATE is already imported.
        # from pyvider.telemetry.logger import base as logger_base # This line is not needed if we use the imported _LAZY_SETUP_STATE

        # Mock the lazy setup to fail
        # To access PyviderLogger for patching, we might need logger_base_module still, or patch differently
        from pyvider.telemetry.logger.base import (
            PyviderLogger as PyviderLoggerForPatching,  # Specific import for patching if needed
        )

        def failing_lazy_setup(self) -> Never:
            raise Exception("Simulated lazy setup failure")

        with patch.object(PyviderLoggerForPatching, '_perform_lazy_setup', failing_lazy_setup):
            # Should still work via emergency fallback
            global_logger.error("Message during setup failure")

        captured = capsys.readouterr()
        # Should have some output (either the message or emergency fallback)
        assert len(captured.err) > 0

    def test_multiple_logger_instances_lazy_init(self, capsys: CaptureFixture) -> None:
        """Test that multiple logger instances share lazy initialization state."""
        reset_pyvider_setup_for_testing()

        from pyvider.telemetry.logger.base import PyviderLogger

        # Create multiple logger instances
        logger1 = PyviderLogger()
        logger2 = PyviderLogger()

        # First logger triggers initialization
        logger1.info("Message from logger1")

        # Second logger should use already-initialized state
        logger2.info("Message from logger2")

        captured = capsys.readouterr()
        assert "Message from logger1" in captured.err
        assert "Message from logger2" in captured.err

# 🧪🚀
