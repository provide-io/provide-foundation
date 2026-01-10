#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#


from __future__ import annotations

import json
import os
from pathlib import Path
import socket
import time

from provide.testkit import MinimalTestCase
from provide.testkit.mocking import MagicMock, patch
import psutil
import pytest

from provide.foundation.file.lock import FileLock, LockError

"""Tests for PID recycling protection in file locks."""


class TestFileLockPIDRecycling(MinimalTestCase):
    """Test PID recycling protection with psutil."""

    def setup_method(self) -> None:
        """Set up test environment."""
        super().setup_method()

    def teardown_method(self) -> None:
        """Clean up after test."""
        super().teardown_method()

    def test_lock_file_json_format(self, temp_directory: Path) -> None:
        """Test lock file is written in JSON format with metadata."""
        lock_path = temp_directory / "test.lock"
        lock = FileLock(lock_path)

        lock.acquire()

        # Lock file should exist and contain JSON
        assert lock_path.exists()
        content = lock_path.read_text()
        lock_info = json.loads(content)

        # Verify required fields
        assert lock_info["pid"] == os.getpid()
        assert "hostname" in lock_info
        assert lock_info["hostname"] == socket.gethostname()
        assert "created" in lock_info
        assert isinstance(lock_info["created"], (int, float))

        # Should have start_time since psutil is available
        assert "start_time" in lock_info
        assert isinstance(lock_info["start_time"], (int, float))

        lock.release()

    def test_lock_file_contains_process_start_time(self, temp_directory: Path) -> None:
        """Test lock file contains process start time for PID recycling protection."""
        lock_path = temp_directory / "test.lock"
        lock = FileLock(lock_path)

        lock.acquire()

        # Read lock info
        lock_info = json.loads(lock_path.read_text())
        lock_start_time = lock_info["start_time"]

        # Verify start time matches current process
        proc = psutil.Process(os.getpid())
        actual_start_time = proc.create_time()

        # Times should match within 1 second tolerance
        assert abs(lock_start_time - actual_start_time) < 1.0

        lock.release()

    def test_stale_lock_with_json_format(self, temp_directory: Path) -> None:
        """Test stale lock detection with JSON format."""
        lock_path = temp_directory / "test.lock"

        # Create a stale lock with non-existent PID
        stale_info = {
            "pid": 99999999,
            "hostname": socket.gethostname(),
            "created": time.time(),
            "start_time": time.time() - 3600,
        }
        lock_path.write_text(json.dumps(stale_info))

        # New lock should detect stale lock and acquire
        lock = FileLock(lock_path)
        assert lock.acquire()

        # Lock file should now have our PID
        lock_info = json.loads(lock_path.read_text())
        assert lock_info["pid"] == os.getpid()

        lock.release()

    def test_pid_recycling_detection(self, temp_directory: Path) -> None:
        """Test detection of PID recycling attack."""
        lock_path = temp_directory / "test.lock"

        # Create a lock file with current PID but different start time
        # This simulates PID recycling where the OS reused our PID
        recycled_info = {
            "pid": os.getpid(),
            "hostname": socket.gethostname(),
            "created": time.time() - 3600,
            "start_time": time.time() - 7200,  # Much older start time
        }
        lock_path.write_text(json.dumps(recycled_info))

        # Lock should detect PID recycling and remove stale lock
        lock = FileLock(lock_path)
        assert lock.acquire()

        # Lock file should have correct start time now
        lock_info = json.loads(lock_path.read_text())
        proc = psutil.Process(os.getpid())
        assert abs(lock_info["start_time"] - proc.create_time()) < 1.0

        lock.release()

    def test_backward_compatibility_plain_text_pid(self, temp_directory: Path) -> None:
        """Test backward compatibility with old plain-text PID format."""
        lock_path = temp_directory / "test.lock"

        # Create old-format lock file with just PID
        lock_path.write_text("99999999")

        # Lock should handle old format and detect stale lock
        lock = FileLock(lock_path)
        assert lock.acquire()

        # New lock should use JSON format
        lock_info = json.loads(lock_path.read_text())
        assert lock_info["pid"] == os.getpid()

        lock.release()

    def test_release_with_json_format(self, temp_directory: Path) -> None:
        """Test lock release with JSON format."""
        lock_path = temp_directory / "test.lock"
        lock = FileLock(lock_path)

        lock.acquire()
        assert lock_path.exists()

        lock.release()
        assert not lock_path.exists()

    def test_release_with_plain_text_format(self, temp_directory: Path) -> None:
        """Test lock release works with old plain-text format."""
        lock_path = temp_directory / "test.lock"

        # Create old-format lock with our PID
        lock_path.write_text(str(os.getpid()))

        # Simulate having acquired the lock
        lock = FileLock(lock_path)
        lock.locked = True

        # Release should work with old format
        lock.release()
        assert not lock_path.exists()

    def test_concurrent_lock_with_json_format(self, temp_directory: Path) -> None:
        """Test concurrent locking with JSON format."""
        lock_path = temp_directory / "test.lock"
        lock1 = FileLock(lock_path)
        lock2 = FileLock(lock_path, timeout=0.5)

        # First lock acquires
        assert lock1.acquire()

        # Verify JSON format
        lock_info = json.loads(lock_path.read_text())
        assert lock_info["pid"] == os.getpid()

        # Second lock should timeout
        with pytest.raises(LockError):
            lock2.acquire()

        # Release first lock
        lock1.release()

        # Second lock can now acquire
        assert lock2.acquire()
        lock2.release()

    def test_valid_lock_not_removed(self, temp_directory: Path) -> None:
        """Test that valid locks are not removed."""
        lock_path = temp_directory / "test.lock"

        # Create a valid lock for our process
        proc = psutil.Process(os.getpid())
        valid_info = {
            "pid": os.getpid(),
            "hostname": socket.gethostname(),
            "created": time.time(),
            "start_time": proc.create_time(),
        }
        lock_path.write_text(json.dumps(valid_info))

        # Try to acquire with a very short timeout
        lock = FileLock(lock_path, timeout=0.3)

        # Should timeout, not remove the valid lock
        with pytest.raises(LockError):
            lock.acquire()

        # Lock file should still exist with original content
        assert lock_path.exists()
        lock_info = json.loads(lock_path.read_text())
        assert lock_info["pid"] == os.getpid()
        assert abs(lock_info["start_time"] - valid_info["start_time"]) < 0.1

        # Clean up
        lock_path.unlink()

    def test_missing_start_time_in_json(self, temp_directory: Path) -> None:
        """Test handling of JSON lock without start_time field."""
        lock_path = temp_directory / "test.lock"

        # Create a valid lock without start_time (maybe from partial write)
        partial_info = {
            "pid": os.getpid(),
            "hostname": socket.gethostname(),
            "created": time.time(),
        }
        lock_path.write_text(json.dumps(partial_info))

        # Lock should not be removed (process exists, no recycling detection)
        lock = FileLock(lock_path, timeout=0.3)

        with pytest.raises(LockError):
            lock.acquire()

        # Lock should still exist
        assert lock_path.exists()

        # Clean up
        lock_path.unlink()

    def test_different_hostname_lock(self, temp_directory: Path) -> None:
        """Test lock from different hostname is removed as stale."""
        lock_path = temp_directory / "test.lock"

        # Create a lock with different hostname (simulating network filesystem)
        # Since we can't validate remote processes, this will be treated as stale
        remote_info = {
            "pid": 12345,
            "hostname": "remote-machine.example.com",
            "created": time.time(),
            "start_time": time.time() - 60,
        }
        lock_path.write_text(json.dumps(remote_info))

        # Lock should be removed as stale (can't validate remote process)
        lock = FileLock(lock_path)
        assert lock.acquire()

        # Verify our lock replaced the remote one
        lock_info = json.loads(lock_path.read_text())
        assert lock_info["pid"] == os.getpid()
        assert lock_info["hostname"] == socket.gethostname()

        lock.release()

    def test_lock_with_psutil_access_denied(self, temp_directory: Path) -> None:
        """Test handling when psutil.AccessDenied is raised."""
        lock_path = temp_directory / "test.lock"

        # Create a lock file
        lock_info = {
            "pid": 1,  # System process that we might not have access to
            "hostname": socket.gethostname(),
            "created": time.time(),
            "start_time": time.time(),
        }
        lock_path.write_text(json.dumps(lock_info))

        # Mock psutil.Process to raise AccessDenied
        with patch("provide.foundation.file.lock.psutil.Process") as mock_process:
            mock_instance = MagicMock()
            mock_instance.create_time.side_effect = psutil.AccessDenied(pid=1)
            mock_process.return_value = mock_instance

            # Lock should assume it's valid and not remove it
            lock = FileLock(lock_path, timeout=0.3)

            with pytest.raises(LockError):
                lock.acquire()

        # Lock should still exist (err on side of caution)
        assert lock_path.exists()

        # Clean up
        lock_path.unlink()

    def test_lock_with_psutil_no_such_process(self, temp_directory: Path) -> None:
        """Test handling when process doesn't exist."""
        lock_path = temp_directory / "test.lock"

        # Create lock with non-existent PID
        stale_info = {
            "pid": 99999999,
            "hostname": socket.gethostname(),
            "created": time.time(),
            "start_time": time.time() - 3600,
        }
        lock_path.write_text(json.dumps(stale_info))

        # Lock should detect process doesn't exist and remove stale lock
        lock = FileLock(lock_path)
        assert lock.acquire()

        # Verify new lock has our PID
        lock_info = json.loads(lock_path.read_text())
        assert lock_info["pid"] == os.getpid()

        lock.release()

    def test_lock_release_wrong_owner(self, temp_directory: Path) -> None:
        """Test lock release doesn't remove file owned by different process."""
        lock_path = temp_directory / "test.lock"

        # Create lock owned by different PID
        other_info = {
            "pid": os.getpid() + 1,
            "hostname": socket.gethostname(),
            "created": time.time(),
            "start_time": time.time(),
        }
        lock_path.write_text(json.dumps(other_info))

        # Try to release
        lock = FileLock(lock_path)
        lock.locked = True  # Pretend we have it
        lock.release()

        # File should still exist
        assert lock_path.exists()
        lock_info = json.loads(lock_path.read_text())
        assert lock_info["pid"] == os.getpid() + 1

        # Clean up
        lock_path.unlink()

    def test_lock_with_corrupted_json(self, temp_directory: Path) -> None:
        """Test handling of corrupted JSON in lock file."""
        lock_path = temp_directory / "test.lock"

        # Create lock file with invalid JSON
        lock_path.write_text("{invalid json content")

        # Should timeout (can't determine if stale)
        lock = FileLock(lock_path, timeout=0.3)

        with pytest.raises(LockError):
            lock.acquire()

        # File should still exist
        assert lock_path.exists()

        # Clean up
        lock_path.unlink()

    def test_lock_creation_timestamp(self, temp_directory: Path) -> None:
        """Test lock file includes creation timestamp."""
        lock_path = temp_directory / "test.lock"
        before_time = time.time()

        lock = FileLock(lock_path)
        lock.acquire()

        after_time = time.time()

        # Verify creation timestamp is reasonable
        lock_info = json.loads(lock_path.read_text())
        assert "created" in lock_info
        assert before_time <= lock_info["created"] <= after_time

        lock.release()


class TestFileLockPIDRecyclingEdgeCases(MinimalTestCase):
    """Test edge cases in PID recycling protection."""

    def setup_method(self) -> None:
        """Set up test environment."""
        super().setup_method()

    def teardown_method(self) -> None:
        """Clean up after test."""
        super().teardown_method()

    def test_lock_with_missing_json_fields(self, temp_directory: Path) -> None:
        """Test handling of JSON with missing fields."""
        lock_path = temp_directory / "test.lock"

        # Create lock with minimal info
        minimal_info = {"pid": 99999999}
        lock_path.write_text(json.dumps(minimal_info))

        # Should detect stale (PID doesn't exist)
        lock = FileLock(lock_path)
        assert lock.acquire()

        lock.release()

    def test_lock_with_null_pid(self, temp_directory: Path) -> None:
        """Test handling of JSON with null PID."""
        lock_path = temp_directory / "test.lock"

        # Create lock with null PID
        null_info = {"pid": None, "hostname": "test", "created": time.time()}
        lock_path.write_text(json.dumps(null_info))

        # Should timeout (invalid lock)
        lock = FileLock(lock_path, timeout=0.3)

        with pytest.raises(LockError):
            lock.acquire()

        # Clean up
        lock_path.unlink()

    def test_lock_start_time_tolerance(self, temp_directory: Path) -> None:
        """Test start time comparison has proper tolerance."""
        lock_path = temp_directory / "test.lock"

        # Create lock with start time slightly off (within 1 second tolerance)
        proc = psutil.Process(os.getpid())
        actual_start = proc.create_time()
        valid_info = {
            "pid": os.getpid(),
            "hostname": socket.gethostname(),
            "created": time.time(),
            "start_time": actual_start + 0.5,  # 0.5 second difference
        }
        lock_path.write_text(json.dumps(valid_info))

        # Lock should not be removed (within tolerance)
        lock = FileLock(lock_path, timeout=0.3)

        with pytest.raises(LockError):
            lock.acquire()

        # Lock should still exist
        assert lock_path.exists()

        # Clean up
        lock_path.unlink()

    @pytest.mark.time_sensitive
    def test_lock_start_time_out_of_tolerance(self, temp_directory: Path) -> None:
        """Test start time difference beyond tolerance is detected."""
        lock_path = temp_directory / "test.lock"

        # Create lock with start time significantly different
        recycled_info = {
            "pid": os.getpid(),
            "hostname": socket.gethostname(),
            "created": time.time(),
            "start_time": time.time() - 10,  # 10 seconds difference
        }
        lock_path.write_text(json.dumps(recycled_info))

        # Lock should detect PID recycling and acquire
        lock = FileLock(lock_path)
        assert lock.acquire()

        # Verify new lock has correct start time
        lock_info = json.loads(lock_path.read_text())
        proc = psutil.Process(os.getpid())
        assert abs(lock_info["start_time"] - proc.create_time()) < 1.0

        lock.release()


# 🧱🏗️🔚
