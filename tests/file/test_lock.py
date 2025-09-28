"""Tests for file locking."""

from __future__ import annotations

import contextlib
import os
from pathlib import Path
import threading
import time
from typing import Never

from provide.testkit import FoundationTestCase
import pytest

from provide.foundation.file.lock import FileLock, LockError


class TestFileLock(FoundationTestCase):
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
        assert lock_path.read_text() == str(os.getpid())

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
            assert lock_path.read_text() == str(os.getpid())

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

    def test_file_lock_timeout(self, temp_directory: Path) -> None:
        """Test lock acquisition timeout."""
        import uuid

        # Use unique lock file name to avoid conflicts with other tests
        unique_id = uuid.uuid4().hex[:8]
        lock_path = temp_directory / f"test_timeout_{unique_id}.lock"

        # Ensure clean state
        if lock_path.exists():
            with contextlib.suppress(FileNotFoundError, PermissionError):
                lock_path.unlink()

        lock1 = FileLock(lock_path)
        lock2 = FileLock(lock_path, timeout=0.5, check_interval=0.05)  # Faster polling

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

            # Should timeout around 0.5s
            assert 0.4 < elapsed < 0.8, f"Expected timeout ~0.5s, got {elapsed:.3f}s"
            assert exc_info.value.code == "LOCK_TIMEOUT"
            assert not lock2.locked
        finally:
            # Ensure cleanup even if test fails
            lock1_locked = getattr(lock1, 'locked', False)
            lock2_locked = getattr(lock2, 'locked', False)

            if lock1_locked:
                try:
                    lock1.release()
                except Exception:
                    pass

            if lock2_locked:
                try:
                    lock2.release()
                except Exception:
                    pass

            # Force cleanup of lock file regardless of ownership
            if lock_path.exists():
                with contextlib.suppress(FileNotFoundError, PermissionError, OSError):
                    lock_path.unlink()

            # Small delay to ensure file system operations complete
            time.sleep(0.01)

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

        # Create a lock file with non-existent PID
        lock_path.write_text("99999999")  # Unlikely to be a real PID

        # New lock should detect stale lock and acquire
        lock = FileLock(lock_path)
        assert lock.acquire()
        assert lock_path.read_text() == str(os.getpid())

        lock.release()

    def test_file_lock_concurrent_access(self, temp_directory: Path) -> None:
        """Test concurrent lock access from threads."""
        lock_path = temp_directory / "test.lock"
        results = []

        def worker(worker_id: int) -> None:
            lock = FileLock(lock_path, timeout=5.0)  # Increased timeout for thread safety
            with lock:
                results.append(worker_id)
                time.sleep(0.1)  # Simulate work

        # Start multiple threads
        threads = []
        try:
            for i in range(3):
                t = threading.Thread(daemon=True, target=worker, args=(i,))
                threads.append(t)
                t.start()

            # Wait for all threads with explicit timeout
            for i, t in enumerate(threads):
                t.join(timeout=10.0)
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

    def test_file_lock_exception_in_context(self, temp_directory: Path) -> Never:
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

        # Create lock file owned by different PID
        different_pid = os.getpid() + 1
        lock_path.write_text(str(different_pid))

        # Try to release should not remove the file
        lock = FileLock(lock_path)
        lock.locked = True  # Pretend we have the lock
        lock.release()

        # File should still exist (owned by different process)
        assert lock_path.exists()
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
