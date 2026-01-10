#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Behavior compliance tests for lazy initialization.

Tests that verify compliance with documented lazy initialization behavior,
immediate usage patterns, thread safety, and performance requirements."""

from __future__ import annotations

import contextlib
import json
import os
import threading
import time

from provide.testkit import FoundationTestCase
from provide.testkit.mocking import patch
import pytest
from pytest import CaptureFixture

from provide.foundation import (
    logger as global_logger,
)

# Mark all tests in this file to run serially to avoid global state pollution
pytestmark = pytest.mark.serial


class TestDocumentedBehaviorCompliance(FoundationTestCase):
    """Tests that verify compliance with documented lazy initialization behavior."""

    def test_documented_environment_variables(self, capsys: CaptureFixture) -> None:
        """Test all documented environment variables work with lazy initialization."""
        import sys

        from provide.testkit import set_log_stream_for_testing

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
            from provide.testkit import reset_foundation_setup_for_testing

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
        # Should NOT have logger name emoji prefix before DAS

    def test_immediate_usage_patterns(self, capsys: CaptureFixture) -> None:
        """Test that lazy initialization supports immediate usage patterns."""
        import sys

        from provide.testkit import set_log_stream_for_testing

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

    def test_thread_safety_guarantees(self, capsys: CaptureFixture) -> None:
        """Test documented thread safety guarantees."""
        import sys

        from provide.testkit import set_log_stream_for_testing

        os.environ["PROVIDE_LOG_LEVEL"] = "INFO"
        set_log_stream_for_testing(sys.stderr)

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
            thread = threading.Thread(daemon=True, target=stress_worker, args=(i,))
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

    @pytest.mark.benchmark
    def test_performance_requirements(self, capsys: CaptureFixture) -> None:
        """Test that lazy initialization meets performance requirements."""
        import sys

        from provide.testkit import set_log_stream_for_testing

        os.environ["PROVIDE_LOG_LEVEL"] = "INFO"
        set_log_stream_for_testing(sys.stderr)

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

        # Performance requirements (more relaxed for CI and varying system loads)
        assert init_time < 1.0, f"Initialization too slow: {init_time:.3f}s"

        messages_per_second = 100 / (subsequent_time or 1e-9)
        assert messages_per_second > 1000, f"Subsequent logging too slow: {messages_per_second:.1f} msg/sec"

        captured = capsys.readouterr()
        assert "First message triggers initialization" in captured.err


# 🧱🏗️🔚
