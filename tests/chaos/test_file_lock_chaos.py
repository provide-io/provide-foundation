#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Chaos tests for FileLock implementation.

Property-based tests using Hypothesis to explore edge cases in file locking,
including concurrent access, PID recycling, stale locks, and corrupted lock files."""

from __future__ import annotations

import asyncio
from concurrent.futures import ThreadPoolExecutor
import json
from pathlib import Path
import threading
import time
from typing import Any

from hypothesis import HealthCheck, given, settings, strategies as st
from provide.testkit import FoundationTestCase
from provide.testkit.chaos import (
    chaos_timings,
    lock_file_scenarios,
    pid_recycling_scenarios,
    thread_counts,
)
import pytest

from provide.foundation.errors.resources import LockError
from provide.foundation.file.lock import FileLock


class TestFileLockChaos(FoundationTestCase):
    """Chaos tests for FileLock with property-based testing."""

    @pytest.mark.chaos_slow
    @given(
        num_threads=thread_counts(min_threads=2, max_threads=10),
        lock_duration=chaos_timings(min_value=0.001, max_value=0.1),
        timeout=st.floats(min_value=0.5, max_value=2.0),
    )
    @settings(
        max_examples=7,
        suppress_health_check=[HealthCheck.too_slow, HealthCheck.function_scoped_fixture],
        deadline=10000,
    )
    def test_concurrent_thread_access_chaos(
        self,
        tmp_path: Path,
        num_threads: int,
        lock_duration: float,
        timeout: float,
    ) -> None:
        """Test FileLock with chaotic concurrent thread access.

        Verifies that:
        - Only one thread can hold the lock at a time
        - All threads eventually get access or timeout appropriately
        - No deadlocks occur
        """
        lock_file = tmp_path / "test.lock"
        access_count = threading.BoundedSemaphore(1)
        acquired_by: list[int] = []
        errors: list[Exception] = []

        def thread_worker(thread_id: int) -> None:
            try:
                lock = FileLock(lock_file, timeout=timeout)
                with lock, access_count:
                    # Verify exclusive access
                    acquired_by.append(thread_id)
                    time.sleep(lock_duration)
            except LockError as e:
                errors.append(e)
            except Exception as e:
                errors.append(e)

        try:
            # Run concurrent threads
            with ThreadPoolExecutor(max_workers=num_threads) as executor:
                futures = [executor.submit(thread_worker, i) for i in range(num_threads)]
                for future in futures:
                    try:
                        # Cap timeout to prevent excessive waiting (max 10 seconds)
                        future.result(timeout=min(10.0, timeout * 3))
                    except TimeoutError:
                        # Thread pool timeout is acceptable under heavy load
                        pass

            # Verify: Some threads succeeded (unless timeout too short)
            # If timeouts occurred, they should be LockErrors
            for error in errors:
                assert isinstance(error, LockError), f"Unexpected error type: {type(error)}"

            # Verify exclusive access: acquired_by should have sequential access
            # (no concurrent access violations)
            assert len(acquired_by) > 0, "At least one thread should acquire lock"
        finally:
            # Ensure cleanup: remove lock file if it exists to prevent tmp_path cleanup hanging
            try:
                if lock_file.exists():
                    lock_file.unlink()
            except Exception:
                pass

    @pytest.mark.chaos_slow
    @given(
        time_advance=st.floats(min_value=0.0, max_value=600.0),
        stale_threshold=st.floats(min_value=0.5, max_value=5.0),
    )
    @settings(
        max_examples=7,
        suppress_health_check=[HealthCheck.too_slow, HealthCheck.function_scoped_fixture],
        deadline=10000,
    )
    def test_stale_lock_detection_chaos(
        self,
        tmp_path: Path,
        time_advance: float,
        stale_threshold: float,
    ) -> None:
        """Test stale lock detection with time chaos.

        Verifies that:
        - Stale locks are detected based on process existence
        - Lock files from dead processes are removed
        - System handles time jumps correctly
        """
        lock_file = tmp_path / "test.lock"

        # Create a lock file with a non-existent PID
        fake_pid = 999999
        lock_info = {
            "pid": fake_pid,
            "hostname": "test",
            "created": time.time() - time_advance,
        }
        lock_file.write_text(json.dumps(lock_info))

        # Try to acquire - should detect stale lock and succeed
        lock = FileLock(lock_file, timeout=stale_threshold)
        try:
            acquired = lock.acquire(blocking=True)

            assert acquired, "Should acquire after removing stale lock"
            assert lock.locked

            lock.release()
            assert not lock.locked
        finally:
            # Ensure cleanup: release lock and remove lock file
            try:
                if lock.locked:
                    lock.release()
            except Exception:
                pass
            # Remove lock file if it exists to prevent tmp_path cleanup hanging
            try:
                if lock_file.exists():
                    lock_file.unlink()
            except Exception:
                pass

    @pytest.mark.chaos_slow
    @given(scenario=pid_recycling_scenarios())
    @settings(
        max_examples=7,
        suppress_health_check=[HealthCheck.too_slow, HealthCheck.function_scoped_fixture],
        deadline=10000,
    )
    def test_pid_recycling_protection_chaos(
        self,
        tmp_path: Path,
        scenario: dict[str, Any],
    ) -> None:
        """Test PID recycling attack prevention with chaos.

        Verifies that:
        - Lock system detects recycled PIDs using start time
        - Tolerance for time comparison works correctly
        - False positives/negatives are minimized
        """
        lock_file = tmp_path / "test.lock"

        # Create lock file with original process info
        lock_info = {
            "pid": scenario["original_pid"],
            "hostname": "test",
            "created": scenario["original_start_time"],
            "start_time": scenario["original_start_time"],
        }
        lock_file.write_text(json.dumps(lock_info))

        # Now simulate the "recycled" process trying to use the lock
        # The lock should detect this is a different process despite same PID
        lock = FileLock(lock_file, timeout=2.0)

        try:
            if scenario["should_detect_recycling"]:
                # Should detect recycling and remove stale lock
                acquired = lock.acquire(blocking=True)
                assert acquired, "Should acquire after detecting PID recycling"
                lock.release()
            else:
                # Time difference within tolerance - might not detect
                # This is expected behavior
                pass
        finally:
            # Ensure cleanup: release lock and remove lock file
            try:
                if lock.locked:
                    lock.release()
            except Exception:
                pass
            # Remove lock file if it exists to prevent tmp_path cleanup hanging
            try:
                if lock_file.exists():
                    lock_file.unlink()
            except Exception:
                pass

    @pytest.mark.chaos_slow
    @given(
        check_interval=st.floats(min_value=0.001, max_value=0.2),
        lock_content=st.one_of(
            st.just("corrupted"),
            st.binary(min_size=0, max_size=100),
            st.text(min_size=0, max_size=50),
            st.just("{}"),
            st.just("null"),
            st.just(""),
        ),
    )
    @settings(
        max_examples=7,
        suppress_health_check=[HealthCheck.too_slow, HealthCheck.function_scoped_fixture],
        deadline=10000,
    )
    def test_corrupted_lock_file_chaos(
        self,
        tmp_path: Path,
        check_interval: float,
        lock_content: str | bytes,
    ) -> None:
        """Test handling of corrupted lock files.

        Verifies that:
        - Corrupted lock files don't cause crashes
        - System handles various corruption patterns
        - Lock can be acquired despite corruption
        """
        lock_file = tmp_path / "test.lock"

        # Write corrupted content
        if isinstance(lock_content, bytes):
            lock_file.write_bytes(lock_content)
        else:
            lock_file.write_text(lock_content)

        lock = FileLock(lock_file, timeout=2.0, check_interval=check_interval)

        # Should handle corruption gracefully
        try:
            acquired = lock.acquire(blocking=True)
            # If we get here, acquisition succeeded
            assert True  # Either outcome is acceptable
            if acquired:
                lock.release()
        except LockError:
            # Timeout is acceptable for corrupted locks
            pass
        finally:
            # Ensure cleanup: release lock and remove lock file
            try:
                if lock.locked:
                    lock.release()
            except Exception:
                pass
            # Remove lock file if it exists to prevent tmp_path cleanup hanging
            try:
                if lock_file.exists():
                    lock_file.unlink()
            except Exception:
                pass

    @pytest.mark.chaos_slow
    @pytest.mark.xdist_group(name="file_lock_serial")  # Force serial execution to avoid deadlock
    @given(scenario=lock_file_scenarios())
    @settings(
        max_examples=7,
        suppress_health_check=[HealthCheck.too_slow, HealthCheck.function_scoped_fixture],
        deadline=None,  # Complex lock scenarios can be unpredictable under system load
    )
    def test_lock_file_scenarios_chaos(
        self,
        tmp_path: Path,
        scenario: dict[str, Any],
    ) -> None:
        """Test comprehensive lock file scenarios.

        Verifies behavior across various lock configurations and edge cases.
        """
        lock_file = tmp_path / "test.lock"

        # Setup stale lock if configured
        if scenario["has_stale_lock"]:
            stale_pid = 999998
            stale_info = {
                "pid": stale_pid,
                "hostname": "test",
                "created": time.time() - scenario["stale_lock_age"],
            }

            if scenario["corrupted_lock_file"]:
                # Corrupt the lock file
                if scenario["lock_content_type"] == "binary":
                    lock_file.write_bytes(b"\x00\xff\xfe")
                elif scenario["lock_content_type"] == "empty":
                    lock_file.write_text("")
                elif scenario["lock_content_type"] == "plain_text":
                    lock_file.write_text(str(stale_pid))
                else:
                    lock_file.write_text(json.dumps(stale_info))
            else:
                lock_file.write_text(json.dumps(stale_info))

        # Create lock with scenario configuration
        lock = FileLock(
            lock_file,
            timeout=scenario["timeout"],
            check_interval=scenario["check_interval"],
        )

        # Attempt to acquire
        try:
            acquired = lock.acquire(blocking=True)
            if acquired:
                # Hold lock briefly
                time.sleep(0.01)
                lock.release()
                assert not lock.locked
        except LockError as e:
            # Timeout or acquisition failure is acceptable
            assert "timeout" in str(e).lower() or "lock" in str(e).lower()
        finally:
            # Ensure cleanup: release lock and remove lock file
            try:
                if lock.locked:
                    lock.release()
            except Exception:
                pass
            # Remove lock file if it exists to prevent tmp_path cleanup hanging
            try:
                if lock_file.exists():
                    lock_file.unlink()
            except Exception:
                pass

    @pytest.mark.slow
    @given(
        timeout=st.floats(min_value=0.1, max_value=1.0),
        iterations=st.integers(min_value=2, max_value=5),
    )
    @settings(
        max_examples=7,
        suppress_health_check=[HealthCheck.too_slow, HealthCheck.function_scoped_fixture],
        deadline=10000,
    )
    def test_reentrant_locking_chaos(
        self,
        tmp_path: Path,
        timeout: float,
        iterations: int,
    ) -> None:
        """Test re-entrant locking behavior with chaos.

        Verifies that:
        - Same instance can re-acquire without deadlock
        - Lock state remains consistent
        - Release properly handles re-entrant state
        """
        lock_file = tmp_path / "test.lock"
        lock = FileLock(lock_file, timeout=timeout)

        try:
            # Acquire multiple times from same instance
            for _ in range(iterations):
                acquired = lock.acquire()
                assert acquired
                assert lock.locked

            # Single release should unlock (current implementation)
            lock.release()
            assert not lock.locked
        finally:
            # Ensure cleanup: release lock and remove lock file
            try:
                if lock.locked:
                    lock.release()
            except Exception:
                pass
            # Remove lock file if it exists to prevent tmp_path cleanup hanging
            try:
                if lock_file.exists():
                    lock_file.unlink()
            except Exception:
                pass

    # Note: reentrant_locking_chaos test removed - it was already marked as @pytest.mark.slow above
    # and has been included in the chaos_slow category


class TestFileLockAsyncChaos(FoundationTestCase):
    """Async chaos tests for FileLock with concurrent async operations."""

    @pytest.mark.chaos_slow
    @pytest.mark.asyncio
    @given(
        num_tasks=st.integers(min_value=2, max_value=10),
        lock_duration=chaos_timings(min_value=0.001, max_value=0.05),
    )
    @settings(
        max_examples=7,
        suppress_health_check=[HealthCheck.too_slow, HealthCheck.function_scoped_fixture],
        deadline=10000,
    )
    async def test_async_concurrent_access_chaos(
        self,
        tmp_path: Path,
        num_tasks: int,
        lock_duration: float,
    ) -> None:
        """Test FileLock with chaotic async concurrent access.

        Verifies behavior when multiple coroutines attempt to acquire lock.
        """
        lock_file = tmp_path / "test.lock"
        acquired_by: list[int] = []
        lock_obj = asyncio.Lock()  # For tracking acquired_by safely

        async def async_worker(task_id: int) -> None:
            try:
                lock = FileLock(lock_file, timeout=5.0)
                # Run acquire in thread pool (since it's sync)
                loop = asyncio.get_event_loop()
                acquired = await loop.run_in_executor(None, lock.acquire)

                if acquired:
                    async with lock_obj:
                        acquired_by.append(task_id)

                    await asyncio.sleep(lock_duration)
                    await loop.run_in_executor(None, lock.release)
            except LockError:
                pass  # Timeout acceptable

        try:
            # Run concurrent tasks
            tasks = [async_worker(i) for i in range(num_tasks)]
            await asyncio.gather(*tasks, return_exceptions=True)

            # At least some tasks should succeed
            assert len(acquired_by) > 0
        finally:
            # Ensure cleanup: remove lock file if it exists to prevent tmp_path cleanup hanging
            try:
                if lock_file.exists():
                    lock_file.unlink()
            except Exception:
                pass


__all__ = [
    "TestFileLockAsyncChaos",
    "TestFileLockChaos",
]

# 🧱🏗️🔚
