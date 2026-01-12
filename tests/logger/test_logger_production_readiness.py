#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Production readiness tests for lazy initialization.

Tests that verify production readiness scenarios like high throughput,
memory stability, error resilience, and graceful shutdown."""

from __future__ import annotations

import asyncio
import io
import os
import time

from provide.testkit import FoundationTestCase
import pytest
from pytest import CaptureFixture

from provide.foundation import (
    logger as global_logger,
    shutdown_foundation,
)

# Mark all tests in this file to run serially to avoid global state pollution
pytestmark = pytest.mark.serial


class TestProductionReadinessScenarios(FoundationTestCase):
    """Tests that verify production readiness of lazy initialization."""

    def test_high_throughput_scenario(self, captured_stderr_for_foundation: io.StringIO) -> None:
        """Test lazy initialization under high throughput."""

        os.environ["PROVIDE_LOG_LEVEL"] = "INFO"

        # Simulate high-throughput logging
        start_time = time.time()
        message_count = 1000

        for i in range(message_count):
            global_logger.info(f"High throughput message {i}", iteration=i)

        end_time = time.time()
        duration = end_time - start_time or 1e-9  # Prevent division by zero

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
            await shutdown_foundation()

        # Run shutdown

        asyncio.run(test_shutdown())

        # Log after shutdown (should still work)
        global_logger.info("Message after shutdown")

        captured = capsys.readouterr()
        assert "Application starting with lazy init" in captured.err
        assert "Message after shutdown" in captured.err


# 🧱🏗️🔚
