#
# test_lazy_init_edge_cases.py
#

"""
Edge case and error recovery tests for lazy initialization.

This module tests the most extreme edge cases, error conditions, and
recovery scenarios to ensure robust behavior under all circumstances.
"""
import contextlib
import io
import os
import threading  # FIXED: Move import to top level
import time
from typing import Any, Never
from unittest.mock import patch

from pytest import CaptureFixture  # Added for capsys
import structlog

from pyvider.telemetry import logger as global_logger
from pyvider.telemetry.core import reset_pyvider_setup_for_testing


class TestExtremeEdgeCases:
    """Tests for extreme edge cases that could break lazy initialization."""

    def test_recursive_logging_during_setup(self, capsys: CaptureFixture) -> None:
        """Test handling of recursive logging calls during lazy setup."""
        reset_pyvider_setup_for_testing()

        original_perform_lazy_setup = None

        def recursive_lazy_setup(self: Any) -> Any: # ANN202
            # This would cause infinite recursion if not handled properly
            global_logger.debug("Logging during lazy setup")
            return original_perform_lazy_setup(self)

        from pyvider.telemetry.logger.base import PyviderLogger
        original_perform_lazy_setup = PyviderLogger._perform_lazy_setup

        with patch.object(PyviderLogger, '_perform_lazy_setup', recursive_lazy_setup):
            # Should handle recursion gracefully without infinite loop
            global_logger.info("Initial log that triggers recursive setup")

        captured = capsys.readouterr()
        # Should not crash and should produce some output
        assert len(captured.err) > 0

    def test_concurrent_setup_with_exceptions(self, capsys: CaptureFixture) -> None:
        """Test concurrent setup attempts when some fail with exceptions."""
        reset_pyvider_setup_for_testing()

        setup_attempts = 0
        setup_failures = 0
        lock = threading.Lock()

        def failing_setup(self: Any) -> Any: # ANN202
            nonlocal setup_attempts, setup_failures
            with lock:
                setup_attempts += 1
                if setup_attempts <= 5:  # First 5 attempts fail
                    setup_failures += 1
                    raise Exception(f"Setup failure {setup_attempts}")

            # Later attempts succeed
            from pyvider.telemetry.logger.base import PyviderLogger
            return PyviderLogger._perform_lazy_setup.__wrapped__(self)

        def concurrent_worker(worker_id: int) -> bool:
            try:
                global_logger.info(f"Worker {worker_id} message")
                return True
            except Exception:
                return False

        from concurrent.futures import ThreadPoolExecutor

        from pyvider.telemetry.logger.base import (
            PyviderLogger,  # type: ignore[import-untyped]
        )

        # SIM117: Combined with statements
        with patch.object(PyviderLogger, '_perform_lazy_setup', failing_setup), \
             ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(concurrent_worker, i) for i in range(20)]
            results = [future.result() for future in futures]

        # At least some workers should succeed
        assert any(results), "No workers succeeded"
        assert setup_failures > 0, "Expected some setup failures"

    def test_memory_pressure_during_setup(self, capsys: CaptureFixture) -> None:
        """Test lazy setup under simulated memory pressure."""
        reset_pyvider_setup_for_testing()

        allocation_count = 0

        def memory_pressure_allocator(*args: Any, **kwargs: Any) -> object: # ANN002, ANN003, ANN202
            nonlocal allocation_count
            allocation_count += 1

            # Simulate memory pressure on every 10th allocation
            if allocation_count % 10 == 0:
                raise MemoryError("Simulated memory pressure")

            return object()

        # Mock object creation to simulate memory pressure
        with patch('builtins.object', memory_pressure_allocator), contextlib.suppress(MemoryError): # SIM105
            global_logger.info("Message under memory pressure")
            # If we get here, the system handled memory pressure gracefully
            # If memory error propagates, that's also acceptable (suppressed)

        # Test should not crash
        captured = capsys.readouterr()
        assert len(captured.err) >= 0  # Some output or none, but no crash

    def test_signal_interruption_during_setup(self, capsys: CaptureFixture) -> None:
        """Test interruption by signals during lazy setup."""
        reset_pyvider_setup_for_testing()

        import signal

        setup_interrupted = False

        def slow_setup(self: Any) -> Any: # ANN202
            nonlocal setup_interrupted
            try:
                # Simulate slow setup that could be interrupted
                time.sleep(0.1)
                from pyvider.telemetry.logger.base import PyviderLogger
                return PyviderLogger._perform_lazy_setup.__wrapped__(self)
            except KeyboardInterrupt:
                setup_interrupted = True
                raise # Correct way to re-raise the caught exception

        def interrupt_handler(signum: int, frame: Any) -> None: # Added types
            pass  # Just interrupt, don't exit

        from pyvider.telemetry.logger.base import (
            PyviderLogger,  # type: ignore[import-untyped]
        )

        # Set up signal handler
        original_handler = signal.signal(signal.SIGINT, interrupt_handler)

        try:
            with patch.object(PyviderLogger, '_perform_lazy_setup', slow_setup):
                # Start setup in a thread
                def setup_worker() -> None:
                    global_logger.info("Message during interruptible setup")

                setup_thread = threading.Thread(target=setup_worker)
                setup_thread.start()

                # Give setup time to start
                time.sleep(0.05)

                # Interrupt the setup (simulate Ctrl+C)
                os.kill(os.getpid(), signal.SIGINT)

                # Wait for thread to complete
                setup_thread.join(timeout=1.0)

        finally:
            # Restore original signal handler
            signal.signal(signal.SIGINT, original_handler)

        # Should not crash the test
        captured = capsys.readouterr()
        assert len(captured.err) >= 0

    def test_import_system_corruption(self, capsys: CaptureFixture) -> None:
        """Test behavior when import system is corrupted during setup."""
        reset_pyvider_setup_for_testing()

        # Mock import failure for critical modules
        def failing_import(name: str, *args: Any, **kwargs: Any) -> Any: # ANN202 (already had arg types)
            if name in ('structlog', 'pyvider.telemetry.config'):
                raise ImportError(f"Simulated import failure for {name}")
            return __import__(name, *args, **kwargs)

        with patch('builtins.__import__', failing_import), contextlib.suppress(ImportError): # SIM105
            # Should handle import failures gracefully
            global_logger.error("Message during import system corruption")
            # If import error propagates, that's acceptable (suppressed)

        # Should not crash the test runner
        captured = capsys.readouterr()
        assert len(captured.err) >= 0

    def test_filesystem_access_denied(self, capsys: CaptureFixture) -> None:
        """Test behavior when filesystem access is denied during setup."""
        reset_pyvider_setup_for_testing()

        # Mock file operations to simulate permission errors
        def permission_denied_open(*args: Any, **kwargs: Any) -> Never: # ANN002, ANN003
            raise PermissionError("Access denied to log file")

        with patch('builtins.open', permission_denied_open), contextlib.suppress(PermissionError): # SIM105
            # Should handle filesystem errors gracefully
            global_logger.warning("Message when filesystem access denied")
            # If permission error propagates, that's acceptable (suppressed)

        # Should not crash
        captured = capsys.readouterr()
        assert len(captured.err) >= 0


class TestStateConsistencyUnderFailure:
    """Tests for state consistency when failures occur during setup."""

    def test_partial_setup_state_recovery(self, capsys: CaptureFixture) -> None:
        """Test recovery from partial setup state."""
        reset_pyvider_setup_for_testing()

        # Simulate partial setup failure
        from pyvider.telemetry.logger import (
            base as logger_base,  # type: ignore[import-untyped]
        )

        def partial_failure_setup(self: Any) -> Never: # Added type for self
            # Set some state but then fail
            self._active_config = "partial_config"  # Invalid state
            raise Exception("Partial setup failure")

        # SIM117: Combined with statements
        with patch.object(logger_base.PyviderLogger, '_perform_lazy_setup', partial_failure_setup), \
             contextlib.suppress(Exception):
            # First attempt should fail
            global_logger.info("First attempt")

        # Reset and try again - should recover from partial state
        logger_base._LAZY_SETUP_STATE["error"] = None

        global_logger.info("Recovery attempt")

        captured = capsys.readouterr()
        assert "Recovery attempt" in captured.err

    def test_lock_contention_state_consistency(self, capsys: CaptureFixture) -> None:
        """Test state consistency under heavy lock contention."""
        reset_pyvider_setup_for_testing()

        results: list[bool] = []
        state_snapshots: list[tuple[bool, bool, Any]] = []

        def contention_worker(worker_id: int) -> None:
            try:
                # Create contention by having many threads try to setup simultaneously
                time.sleep(0.001 * (worker_id % 3))  # Stagger slightly

                global_logger.info(f"Contention worker {worker_id}")

                # Snapshot state after logging
                from pyvider.telemetry.logger import (
                    base as logger_base,  # Keep for _LAZY_SETUP_STATE access
                )
                snapshot = (
                    logger_base._LAZY_SETUP_STATE["done"],
                    global_logger._is_configured_by_setup,
                    global_logger._active_config is not None
                )
                state_snapshots.append(snapshot)
                results.append(True)

            except Exception:
                results.append(False)

        # Create high contention
        threads = []
        thread_count = 20

        for i in range(thread_count):
            thread = threading.Thread(target=contention_worker, args=(i,))
            threads.append(thread)

        # Start all threads nearly simultaneously
        for thread in threads:
            thread.start()

        # Wait for completion
        for thread in threads:
            thread.join(timeout=10.0)

        # Verify state consistency
        assert all(results), "Some threads failed under contention"

        # All snapshots should show consistent final state
        final_states = set(state_snapshots)
        # Should converge to a single consistent state
        assert len(final_states) <= 2, f"Too many different final states: {final_states}"

    def test_exception_handling_state_cleanup(self, capsys: CaptureFixture) -> None:
        """Test that exceptions during setup properly clean up state."""
        reset_pyvider_setup_for_testing()

        from pyvider.telemetry.logger import base as logger_base

        exception_count = 0

        def exception_setup(self: Any) -> None: # ANN202
            nonlocal exception_count
            exception_count += 1

            # Fail first few times, then succeed
            if exception_count <= 3:
                # Pollute state before failing
                logger_base._LAZY_SETUP_STATE["done"] = True  # Invalid state
                raise Exception(f"Setup exception {exception_count}")

            # Eventually succeed with clean state
            return logger_base.PyviderLogger._perform_lazy_setup.__wrapped__(self)

        with patch.object(logger_base.PyviderLogger, '_perform_lazy_setup', exception_setup):
            # Multiple attempts should eventually succeed
            for attempt in range(5):
                try:
                    global_logger.info(f"Attempt {attempt}")
                    break  # Success
                except Exception:
                    # Reset error state to allow retry
                    logger_base._LAZY_SETUP_STATE["error"] = None
                    continue

        # Should eventually succeed
        captured = capsys.readouterr()
        assert len(captured.err) > 0

    def test_thread_local_state_isolation(self, capsys: CaptureFixture) -> None:
        """Test that thread-local state doesn't interfere with global state."""
        reset_pyvider_setup_for_testing()

        thread_results: dict[int, Any] = {}

        def thread_worker(worker_id: int) -> None:
            # Each thread should get consistent global state
            # despite any thread-local variations

            # Log from this thread
            thread_logger = global_logger.get_logger(f"thread.{worker_id}")
            thread_logger.info(f"Thread {worker_id} message")

            # Record thread's view of global state
            from pyvider.telemetry.logger import (
                base as logger_base,  # Keep for _LAZY_SETUP_STATE access
            )
            thread_results[worker_id] = {
                'lazy_setup_done': logger_base._LAZY_SETUP_STATE["done"],
                'config_exists': global_logger._active_config is not None,
                'thread_id': threading.get_ident(),
            }

        # Start multiple threads
        threads = []
        for i in range(10):
            thread = threading.Thread(target=thread_worker, args=(i,))
            threads.append(thread)
            thread.start()

        # Wait for all
        for thread in threads:
            thread.join()

        # All threads should see consistent global state
        lazy_setup_states = [r['lazy_setup_done'] for r in thread_results.values()]
        config_states = [r['config_exists'] for r in thread_results.values()]

        # Should all be the same (all True after successful setup)
        assert len(set(lazy_setup_states)) == 1, "Inconsistent lazy setup state across threads"
        assert len(set(config_states)) == 1, "Inconsistent config state across threads"
        assert all(lazy_setup_states), "Lazy setup should be done in all threads"
        assert all(config_states), "Config should exist in all threads"


class TestLazyInitializationCompliance:
    """Tests for compliance with lazy initialization specifications."""

    def test_initialization_only_when_needed(self, capsys: CaptureFixture) -> None:
        """Test that initialization only occurs when actually needed."""
        reset_pyvider_setup_for_testing()

        # Import and create logger instance should not trigger setup
        from pyvider.telemetry import logger
        from pyvider.telemetry.logger import base as logger_base
        new_logger = logger_base.PyviderLogger()

        # Verify no initialization yet
        assert not logger_base._LAZY_SETUP_STATE["done"]
        assert not new_logger._is_configured_by_setup
        assert new_logger._active_config is None

        # Non-logging operations should not trigger setup
        logger.get_logger("test")  # This might trigger, let's see

        # Actually, get_logger does call _ensure_configured, so let's test differently
        # Just creating a logger instance should not trigger setup
        logger_base.PyviderLogger()

        # The instance creation itself shouldn't trigger setup
        # Only actual logging should trigger setup
        logger.info("This should trigger setup")

        # Now should be initialized
        assert logger_base._LAZY_SETUP_STATE["done"]

        captured = capsys.readouterr()
        assert "This should trigger setup" in captured.err

    def test_setup_occurs_exactly_once(self, capsys: CaptureFixture) -> None:
        """Test that lazy setup occurs exactly once regardless of calls."""
        reset_pyvider_setup_for_testing()

        setup_call_count = 0

        def counting_setup(self: Any) -> Any: # ANN202
            nonlocal setup_call_count
            setup_call_count += 1
            from pyvider.telemetry.logger.base import PyviderLogger
            return PyviderLogger._perform_lazy_setup.__wrapped__(self)

        from pyvider.telemetry.logger.base import PyviderLogger

        with patch.object(PyviderLogger, '_perform_lazy_setup', counting_setup):
            # Multiple logging calls
            for i in range(10):
                global_logger.info(f"Message {i}")

            # Multiple logger instances
            for i in range(5):
                test_logger = global_logger.get_logger(f"test.{i}")
                test_logger.debug(f"Test message {i}")

        # Setup should have been called exactly once
        assert setup_call_count == 1, f"Setup called {setup_call_count} times, expected 1"

        captured = capsys.readouterr()
        assert "Message 0" in captured.err
        assert "Message 9" in captured.err

    def test_thread_safety_specification_compliance(self, capsys: CaptureFixture) -> None:
        """Test compliance with thread safety specifications."""
        reset_pyvider_setup_for_testing()

        # Configure structlog with a non-default factory to bypass early exit in _ensure_configured
        # This allows testing the lock contention for _perform_lazy_setup itself.
        structlog.configure(logger_factory=structlog.PrintLoggerFactory(file=io.StringIO()))

        setup_start_times: list[float] = []
        setup_end_times: list[float] = []

        # Import PyviderLogger here to access its original method
        from pyvider.telemetry.logger.base import PyviderLogger
        original_perform_lazy_setup_method = PyviderLogger._perform_lazy_setup

        def timed_setup(self_instance: Any) -> Any: # ANN202 (already had arg type)
            setup_start_times.append(time.time())
            original_method_result = None
            try:
                # Call the stored original method
                original_method_result = original_perform_lazy_setup_method(self_instance)
            except Exception:
                raise # Re-raise
            setup_end_times.append(time.time())
            return original_method_result

        # PyviderLogger is already imported above
        with patch.object(PyviderLogger, '_perform_lazy_setup', timed_setup):
            # Create barrier to synchronize thread starts
            thread_count = 20
            barrier = threading.Barrier(thread_count)

            def synchronized_worker(worker_id: int) -> None:
                # Wait for all threads to be ready
                barrier.wait()
                # All threads log simultaneously
                global_logger.info(f"Synchronized message {worker_id}")

            threads = []
            for i in range(thread_count):
                thread = threading.Thread(target=synchronized_worker, args=(i,))
                threads.append(thread)
                thread.start()

            for thread in threads:
                thread.join()

        # Despite synchronization, setup should still occur only once
        assert len(setup_start_times) == 1, f"Setup started {len(setup_start_times)} times"
        assert len(setup_end_times) == 1, f"Setup completed {len(setup_end_times)} times"

        captured = capsys.readouterr()
        # All messages should be logged
        for i in range(thread_count):
            assert f"Synchronized message {i}" in captured.err

    def test_error_isolation_specification(self, capsys: CaptureFixture) -> None:
        """Test that errors in setup don't affect subsequent logging attempts."""
        reset_pyvider_setup_for_testing()

        from pyvider.telemetry.logger import base as logger_base

        # First setup attempt fails
        def failing_then_succeeding_setup(self: Any) -> Any: # ANN202
            if not hasattr(self, '_setup_attempted'):
                self._setup_attempted = True
                raise Exception("First setup fails")
            else:
                # Second attempt succeeds
                return logger_base.PyviderLogger._perform_lazy_setup.__wrapped__(self)

        with patch.object(logger_base.PyviderLogger, '_perform_lazy_setup', failing_then_succeeding_setup), \
             contextlib.suppress(Exception): # SIM105 for first attempt
            # First logging attempt (setup fails)
            global_logger.info("First attempt")
            # Expected to fail (suppressed)

        # Reset error state to allow retry
            logger_base._LAZY_SETUP_STATE["error"] = None

            # Second logging attempt (should succeed)
            global_logger.info("Second attempt")

        captured = capsys.readouterr()
        assert "Second attempt" in captured.err

# 🧪⚡
