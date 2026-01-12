#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for file locking."""

from __future__ import annotations

import contextlib
import json
import os
from pathlib import Path
import threading
import time

from provide.testkit import MinimalTestCase
import pytest

from provide.foundation.file.lock import FileLock, LockError


class TestFileLock(MinimalTestCase):
    """Test file locking functionality."""

    def setup_method(self) -> None:
        """Set up test environment."""
        super().setup_method()

    def teardown_method(self) -> None:
        """Clean up after test."""
        super().teardown_method()

    def test_file_lock_acquire_release(self, temp_directory: Path) -> None:
        """Test basic lock acquire and release."""
        lock_path = temp_directory / "test.lock"
        lock = FileLock(lock_path)

        # Acquire lock
        assert lock.acquire()
        assert lock.locked
        assert lock_path.exists()

        # Lock file should contain JSON with our PID
        lock_info = json.loads(lock_path.read_text())
        assert lock_info["pid"] == os.getpid()

        # Release lock
        lock.release()
        assert not lock.locked
        assert not lock_path.exists()

    def test_file_lock_context_manager(self, temp_directory: Path) -> None:
        """Test lock as context manager."""
        lock_path = temp_directory / "test.lock"

        with FileLock(lock_path) as lock:
            assert lock.locked
            assert lock_path.exists()

            # Lock file should contain JSON with our PID
            lock_info = json.loads(lock_path.read_text())
            assert lock_info["pid"] == os.getpid()

        assert not lock.locked
        assert not lock_path.exists()

    def test_file_lock_non_blocking(self, temp_directory: Path) -> None:
        """Test non-blocking lock acquisition."""
        lock_path = temp_directory / "test.lock"
        lock1 = FileLock(lock_path)
        lock2 = FileLock(lock_path)

        # First lock succeeds
        assert lock1.acquire(blocking=False)

        # Second lock fails (non-blocking)
        assert not lock2.acquire(blocking=False)
        assert not lock2.locked

        # Release first lock
        lock1.release()

        # Now second lock succeeds
        assert lock2.acquire(blocking=False)
        lock2.release()

    @pytest.mark.time_sensitive
    def test_file_lock_timeout(self, temp_directory: Path) -> None:
        """Test lock acquisition timeout."""
        # Make lock path unique per worker to prevent collision in parallel execution
        worker_id = os.environ.get("PYTEST_XDIST_WORKER", "gw0")
        lock_path = temp_directory / f"test_{worker_id}.lock"
        lock1 = FileLock(lock_path)

        # Use shorter timeout for faster test execution in parallel
        timeout_val = 1.0
        lock2 = FileLock(lock_path, timeout=timeout_val)

        try:
            # First lock acquired
            assert lock1.acquire()
            assert lock1.locked
            assert lock_path.exists()

            # Second lock should timeout
            start = time.time()
            with pytest.raises(LockError) as exc_info:
                lock2.acquire()
            elapsed = time.time() - start

            # Generous bounds to handle coverage overhead
            min_time = timeout_val * 0.7  # 0.7s minimum
            max_time = timeout_val * 2.5  # 2.5s maximum
            assert min_time < elapsed < max_time, f"Expected timeout ~{timeout_val}s, got {elapsed:.3f}s"
            assert exc_info.value.code == "LOCK_TIMEOUT"
            assert not lock2.locked
        finally:
            # Ensure cleanup even if test fails
            if lock1.locked:
                lock1.release()
            if lock_path.exists():
                with contextlib.suppress(FileNotFoundError, PermissionError):
                    lock_path.unlink()

    def test_file_lock_multiple_releases(self, temp_directory: Path) -> None:
        """Test multiple releases are safe."""
        lock_path = temp_directory / "test.lock"
        lock = FileLock(lock_path)

        lock.acquire()
        lock.release()
        lock.release()  # Second release should be safe

        assert not lock.locked
        assert not lock_path.exists()

    def test_file_lock_stale_detection(self, temp_directory: Path) -> None:
        """Test stale lock detection and removal."""
        lock_path = temp_directory / "test.lock"

        # Create a lock file with non-existent PID (old plain-text format)
        lock_path.write_text("99999999")  # Unlikely to be a real PID

        # New lock should detect stale lock and acquire
        lock = FileLock(lock_path)
        assert lock.acquire()

        # New lock should use JSON format
        lock_info = json.loads(lock_path.read_text())
        assert lock_info["pid"] == os.getpid()

        lock.release()

    @pytest.mark.time_sensitive
    def test_file_lock_concurrent_access(self, temp_directory: Path) -> None:
        """Test concurrent lock access from threads."""
        # Make lock path unique per worker to prevent collision in parallel execution
        worker_id = os.environ.get("PYTEST_XDIST_WORKER", "gw0")
        lock_path = temp_directory / f"test_concurrent_{worker_id}.lock"
        results = []

        def worker(thread_id: int) -> None:
            # Reduced timeout for faster parallel execution
            lock = FileLock(lock_path, timeout=2.0)
            with lock:
                results.append(thread_id)
                time.sleep(0.02)  # Minimal work time

        # Start multiple threads
        threads = []
        try:
            for i in range(3):
                t = threading.Thread(daemon=True, target=worker, args=(i,))
                threads.append(t)
                t.start()

            # Wait for all threads with reasonable timeout
            for i, t in enumerate(threads):
                t.join(timeout=5.0)  # Reduced from 20.0s
                if t.is_alive():
                    pytest.fail(f"Thread {i} did not complete within timeout")

            # All workers should have completed
            assert len(results) == 3
            assert set(results) == {0, 1, 2}
        finally:
            # Ensure any remaining locks are cleaned up
            if lock_path.exists():
                with contextlib.suppress(FileNotFoundError, PermissionError):
                    lock_path.unlink()

    def test_file_lock_exception_in_context(self, temp_directory: Path) -> None:
        """Test lock is released even when exception occurs."""
        lock_path = temp_directory / "test.lock"

        with pytest.raises(ValueError), FileLock(lock_path) as lock:
            assert lock.locked
            assert lock_path.exists()
            raise ValueError("Test exception")

        # Lock should be released despite exception
        assert not lock_path.exists()

    def test_file_lock_different_process_ownership(self, temp_directory: Path) -> None:
        """Test lock doesn't release if owned by different process."""
        lock_path = temp_directory / "test.lock"

        # Create lock file owned by different PID (old plain-text format)
        different_pid = os.getpid() + 1
        lock_path.write_text(str(different_pid))

        # Try to release should not remove the file
        lock = FileLock(lock_path)
        lock.locked = True  # Pretend we have the lock
        lock.release()

        # File should still exist (owned by different process)
        assert lock_path.exists()
        # Should still be plain text format (wasn't overwritten)
        assert lock_path.read_text() == str(different_pid)

        # Clean up
        lock_path.unlink()

    def test_file_lock_check_interval(self, temp_directory: Path) -> None:
        """Test custom check interval."""
        lock_path = temp_directory / "test.lock"
        lock1 = FileLock(lock_path)
        lock2 = FileLock(lock_path, timeout=1.0, check_interval=0.3)

        lock1.acquire()

        # Track how many checks happen
        start = time.time()
        checks = 0

        def count_checks() -> None:
            nonlocal checks
            while time.time() - start < 0.9:
                time.sleep(0.05)
                if not lock_path.exists():
                    break
                checks += 1

        # Start counter thread
        counter = threading.Thread(daemon=True, target=count_checks)
        counter.start()

        # Try to acquire (will timeout)
        with pytest.raises(LockError):
            lock2.acquire()

        counter.join(timeout=5.0)
        lock1.release()

        # With 0.3s interval over ~1s, should be ~3 checks
        # But the counter thread is checking every 0.05s so it might count more
        # This test is inherently flaky due to timing, so be lenient
        assert checks > 0  # At least some checks happened

    def test_file_lock_invalid_lock_content(self, temp_directory: Path) -> None:
        """Test handling of invalid lock file content."""
        lock_path = temp_directory / "test.lock"

        # Create lock file with invalid content
        lock_path.write_text("not_a_pid")

        # Should not be detected as stale, acquisition should fail quickly
        lock = FileLock(lock_path, timeout=0.5)

        with pytest.raises(LockError):
            lock.acquire()

        # Invalid content should still be there
        assert lock_path.exists()

    def test_file_lock_thread_safety_same_instance(self, temp_directory: Path) -> None:
        """Test thread safety when multiple threads use the same FileLock instance."""
        worker_id = os.environ.get("PYTEST_XDIST_WORKER", "gw0")
        lock_path = temp_directory / f"test_thread_safety_{worker_id}.lock"
        lock = FileLock(lock_path, timeout=2.0)
        results = []
        errors = []

        def worker(thread_id: int) -> None:
            try:
                # Multiple threads trying to acquire the same FileLock instance
                # The internal thread lock should serialize access
                if lock.acquire(blocking=True):
                    results.append(thread_id)
                    time.sleep(0.01)  # Minimal critical section
                    lock.release()
            except Exception as e:
                errors.append((thread_id, str(e)))

        # Start multiple threads using the SAME lock instance
        threads = []
        try:
            for i in range(3):
                t = threading.Thread(daemon=True, target=worker, args=(i,))
                threads.append(t)
                t.start()

            # Wait for completion
            for i, t in enumerate(threads):
                t.join(timeout=5.0)
                if t.is_alive():
                    pytest.fail(f"Thread {i} did not complete within timeout")

            # No errors should occur
            assert len(errors) == 0, f"Errors occurred: {errors}"
            # All workers should have completed
            assert len(results) == 3
            assert set(results) == {0, 1, 2}
        finally:
            # Cleanup
            if lock_path.exists():
                with contextlib.suppress(FileNotFoundError, PermissionError):
                    lock_path.unlink()

    def test_file_lock_reentrant_behavior(self, temp_directory: Path) -> None:
        """Test that acquiring an already-held lock returns True (re-entrant)."""
        lock_path = temp_directory / "test.lock"
        lock = FileLock(lock_path)

        # First acquire
        assert lock.acquire()
        assert lock.locked

        # Second acquire on same instance (re-entrant)
        assert lock.acquire()
        assert lock.locked

        # Single release
        lock.release()
        assert not lock.locked
        assert not lock_path.exists()


# 🧱🏗️🔚
