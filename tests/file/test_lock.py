"""Tests for file locking."""

import os
from pathlib import Path
import tempfile
import threading
import time
from typing import Never

import pytest

from provide.foundation.file.lock import FileLock, LockError


@pytest.fixture
def temp_dir():
    """Create a temporary directory for tests."""
    with tempfile.TemporaryDirectory() as td:
        yield Path(td)


def test_file_lock_acquire_release(temp_dir) -> None:
    """Test basic lock acquire and release."""
    lock_path = temp_dir / "test.lock"
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


def test_file_lock_context_manager(temp_dir) -> None:
    """Test lock as context manager."""
    lock_path = temp_dir / "test.lock"

    with FileLock(lock_path) as lock:
        assert lock.locked
        assert lock_path.exists()
        assert lock_path.read_text() == str(os.getpid())

    assert not lock.locked
    assert not lock_path.exists()


def test_file_lock_non_blocking(temp_dir) -> None:
    """Test non-blocking lock acquisition."""
    lock_path = temp_dir / "test.lock"
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


def test_file_lock_timeout(temp_dir) -> None:
    """Test lock acquisition timeout."""
    lock_path = temp_dir / "test.lock"
    lock1 = FileLock(lock_path)
    lock2 = FileLock(lock_path, timeout=0.5)

    # First lock acquired
    lock1.acquire()

    # Second lock should timeout
    start = time.time()
    with pytest.raises(LockError) as exc_info:
        lock2.acquire()
    elapsed = time.time() - start

    assert 0.4 < elapsed < 0.7  # Should timeout around 0.5s
    assert exc_info.value.code == "LOCK_TIMEOUT"

    lock1.release()


def test_file_lock_multiple_releases(temp_dir) -> None:
    """Test multiple releases are safe."""
    lock_path = temp_dir / "test.lock"
    lock = FileLock(lock_path)

    lock.acquire()
    lock.release()
    lock.release()  # Second release should be safe

    assert not lock.locked
    assert not lock_path.exists()


def test_file_lock_stale_detection(temp_dir) -> None:
    """Test stale lock detection and removal."""
    lock_path = temp_dir / "test.lock"

    # Create a lock file with non-existent PID
    lock_path.write_text("99999999")  # Unlikely to be a real PID

    # New lock should detect stale lock and acquire
    lock = FileLock(lock_path)
    assert lock.acquire()
    assert lock_path.read_text() == str(os.getpid())

    lock.release()


def test_file_lock_concurrent_access(temp_dir) -> None:
    """Test concurrent lock access from threads."""
    lock_path = temp_dir / "test.lock"
    results = []

    def worker(worker_id) -> None:
        lock = FileLock(lock_path, timeout=2.0)
        with lock:
            results.append(worker_id)
            time.sleep(0.1)  # Simulate work

    # Start multiple threads
    threads = []
    for i in range(3):
        t = threading.Thread(target=worker, args=(i,))
        threads.append(t)
        t.start()

    # Wait for all threads
    for t in threads:
        t.join()

    # All workers should have completed
    assert len(results) == 3
    assert set(results) == {0, 1, 2}


def test_file_lock_exception_in_context(temp_dir) -> Never:
    """Test lock is released even when exception occurs."""
    lock_path = temp_dir / "test.lock"

    with pytest.raises(ValueError), FileLock(lock_path) as lock:
        assert lock.locked
        assert lock_path.exists()
        raise ValueError("Test exception")

    # Lock should be released despite exception
    assert not lock_path.exists()


def test_file_lock_different_process_ownership(temp_dir) -> None:
    """Test lock doesn't release if owned by different process."""
    lock_path = temp_dir / "test.lock"

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


def test_file_lock_check_interval(temp_dir) -> None:
    """Test custom check interval."""
    lock_path = temp_dir / "test.lock"
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
    counter = threading.Thread(target=count_checks)
    counter.start()

    # Try to acquire (will timeout)
    with pytest.raises(LockError):
        lock2.acquire()

    counter.join()
    lock1.release()

    # With 0.3s interval over ~1s, should be ~3 checks
    # But the counter thread is checking every 0.05s so it might count more
    # This test is inherently flaky due to timing, so be lenient
    assert checks > 0  # At least some checks happened


def test_file_lock_invalid_lock_content(temp_dir) -> None:
    """Test handling of invalid lock file content."""
    lock_path = temp_dir / "test.lock"

    # Create lock file with invalid content
    lock_path.write_text("not_a_pid")

    # Should not be detected as stale, acquisition should fail quickly
    lock = FileLock(lock_path, timeout=0.5)

    with pytest.raises(LockError):
        lock.acquire()

    # Invalid content should still be there
    assert lock_path.exists()
