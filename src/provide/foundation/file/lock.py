#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from __future__ import annotations

import os
from pathlib import Path
import socket
import threading
import time

from provide.foundation.config.defaults import DEFAULT_FILE_LOCK_TIMEOUT
from provide.foundation.errors.resources import LockError
from provide.foundation.logger import get_logger
from provide.foundation.serialization import json_dumps, json_loads

"""File-based locking for concurrent access control.

Uses psutil (optional) for robust process validation to prevent PID recycling attacks.
When psutil is not available, falls back to basic PID existence checking.
Thread-safe for concurrent access within a single process.
"""

log = get_logger(__name__)

# Try to import psutil for PID recycling protection
try:
    import psutil

    _HAS_PSUTIL = True
except ImportError:
    _HAS_PSUTIL = False
    log.debug(
        "psutil not available, using basic PID validation",
        hint="For PID recycling protection, install with: pip install provide-foundation[process]",
    )


class FileLock:
    """File-based lock for concurrent access control.

    Uses exclusive file creation as the locking mechanism.
    The lock file contains the PID of the process holding the lock.

    Thread-safe: Multiple threads can safely use the same FileLock instance.
    The internal thread lock protects instance state while the file lock
    provides inter-process synchronization.

    Example:
        with FileLock("/tmp/myapp.lock"):
            # Exclusive access to resource
            do_something()

    """

    def __init__(
        self,
        path: Path | str,
        timeout: float = DEFAULT_FILE_LOCK_TIMEOUT,
        check_interval: float = 0.1,
    ) -> None:
        """Initialize file lock.

        Args:
            path: Lock file path
            timeout: Max seconds to wait for lock
            check_interval: Seconds between lock checks

        """
        self.path = Path(path)
        self.timeout = timeout
        self.check_interval = check_interval
        self.locked = False
        self.pid = os.getpid()
        self._thread_lock = threading.RLock()  # Protect instance state from concurrent threads

    def acquire(self, blocking: bool = True) -> bool:  # noqa: C901
        """Acquire the lock.

        Args:
            blocking: If True, wait for lock. If False, return immediately.

        Returns:
            True if lock acquired, False if not (non-blocking mode only)

        Raises:
            LockError: If timeout exceeded (blocking mode)

        """
        with self._thread_lock:
            if self.timeout <= 0:
                raise LockError("Timeout must be positive", code="INVALID_TIMEOUT", path=str(self.path))

            # If already locked by this instance, treat as re-entrant
            if self.locked:
                return True

            # Use a finite loop with hard limits to prevent any possibility of hanging
            start_time = time.time()
            end_time = start_time + self.timeout
            max_iterations = 1000  # Hard limit regardless of timeout
            iteration = 0

            while iteration < max_iterations:
                iteration += 1
                current_time = time.time()

                # Hard timeout check - exit immediately if time is up
                if current_time >= end_time:
                    elapsed = current_time - start_time
                    raise LockError(
                        f"Failed to acquire lock within {self.timeout}s (elapsed: {elapsed:.3f}s, iterations: {iteration})",
                        code="LOCK_TIMEOUT",
                        path=str(self.path),
                    ) from None

                try:
                    # Try to create lock file exclusively
                    fd = os.open(str(self.path), os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o644)
                    try:
                        # Write lock metadata as JSON for robust validation
                        lock_info = {
                            "pid": self.pid,
                            "hostname": socket.gethostname(),
                            "created": current_time,
                        }
                        # Add process start time for PID recycling protection (if psutil available)
                        if _HAS_PSUTIL:
                            try:
                                proc = psutil.Process(self.pid)
                                lock_info["start_time"] = proc.create_time()
                            except (psutil.NoSuchProcess, psutil.AccessDenied):
                                pass
                        os.write(fd, json_dumps(lock_info).encode())
                    finally:
                        os.close(fd)

                    self.locked = True
                    elapsed = current_time - start_time
                    log.debug(
                        "Acquired lock",
                        path=str(self.path),
                        pid=self.pid,
                        iterations=iteration,
                        elapsed=elapsed,
                    )
                    return True

                except FileExistsError:
                    # Lock file exists, check if holder is still alive
                    if self._check_stale_lock():
                        continue  # Retry after removing stale lock

                    if not blocking:
                        log.debug("Lock unavailable (non-blocking)", path=str(self.path))
                        return False

                    # Calculate remaining time
                    remaining = end_time - current_time
                    if remaining <= 0:
                        # Time is up
                        break

                    # Sleep for a small fixed interval or remaining time, whichever is smaller
                    sleep_time = min(0.01, remaining * 0.5)  # Never sleep more than 10ms
                    if sleep_time > 0:
                        time.sleep(sleep_time)

            # If we exit the loop without acquiring the lock
            elapsed = time.time() - start_time
            raise LockError(
                f"Failed to acquire lock within {self.timeout}s (elapsed: {elapsed:.3f}s, iterations: {iteration})",
                code="LOCK_TIMEOUT",
                path=str(self.path),
            ) from None

    def release(self) -> None:
        """Release the lock.

        Only removes the lock file if we own it.
        """
        with self._thread_lock:
            if not self.locked:
                return

            try:
                # Verify we own the lock before removing
                if self.path.exists():
                    try:
                        content = self.path.read_text().strip()
                        try:
                            lock_info = json_loads(content)
                            if isinstance(lock_info, dict):
                                owner_pid = lock_info.get("pid")
                            else:
                                owner_pid = lock_info if isinstance(lock_info, int) else None
                        except (ValueError, Exception):
                            owner_pid = int(content) if content.isdigit() else None

                        if owner_pid == self.pid:
                            self.path.unlink()
                            log.debug("Released lock", path=str(self.path), pid=self.pid)
                        else:
                            log.warning(
                                "Lock owned by different process",
                                path=str(self.path),
                                owner_pid=owner_pid,
                                our_pid=self.pid,
                            )
                    except Exception as e:
                        log.warning(
                            "Error checking lock ownership",
                            path=str(self.path),
                            error=str(e),
                        )
                        # Still try to remove if we think we own it
                        if self.locked:
                            self.path.unlink()
            except FileNotFoundError:
                pass  # Lock already released
            except (OSError, PermissionError) as e:
                # Failed to unlink lock file due to permission or filesystem error
                log.error("Failed to release lock", path=str(self.path), error=str(e))
            finally:
                self.locked = False

    def _check_stale_lock(self) -> bool:  # noqa: C901
        """Check if lock file is stale and remove if so.

        Uses psutil to validate process start time, preventing PID recycling attacks.
        Falls back to simple PID check for backward compatibility with old lock files.

        Returns:
            True if stale lock was removed, False otherwise

        Note:
            Complexity is intentionally high to handle all security-critical cases
            (PID recycling, format compatibility, error handling).

        """
        try:
            # Quick existence check first
            if not self.path.exists():
                return False

            # Read content with a fallback to prevent hanging on I/O
            try:
                content = self.path.read_text().strip()
            except (OSError, PermissionError, UnicodeDecodeError):
                # OSError/PermissionError: Can't read file
                # UnicodeDecodeError: File has invalid encoding
                # If we can't read the file, assume it's not stale
                return False

            lock_pid = None
            lock_start_time = None
            try:
                lock_info = json_loads(content)
                if isinstance(lock_info, dict):
                    lock_pid = lock_info.get("pid")
                    lock_start_time = lock_info.get("start_time")
                elif isinstance(lock_info, int):
                    lock_pid = lock_info
                else:
                    log.debug("Invalid lock file content", path=str(self.path), content=content[:50])
                    return False
            except (ValueError, Exception):
                if content.isdigit():
                    lock_pid = int(content)
                else:
                    log.debug("Invalid lock file content", path=str(self.path), content=content[:50])
                    return False

            if lock_pid is None:
                log.debug("No PID in lock file", path=str(self.path))
                return False

            # Validate process - use psutil if available for PID recycling protection
            if _HAS_PSUTIL:
                # Full validation with PID recycling protection
                try:
                    proc = psutil.Process(lock_pid)

                    # Call a method to trigger NoSuchProcess if PID doesn't exist
                    # This is needed because Process.__init__ is lazy
                    proc_start_time = proc.create_time()

                    # If we have start_time, validate it matches to prevent PID recycling
                    # Allow 1 second tolerance for timestamp precision differences
                    if lock_start_time is not None and abs(proc_start_time - lock_start_time) > 1.0:
                        log.warning(
                            "PID recycling detected - removing stale lock",
                            path=str(self.path),
                            lock_pid=lock_pid,
                            lock_start=lock_start_time,
                            proc_start=proc_start_time,
                        )
                        try:
                            self.path.unlink()
                            return True
                        except FileNotFoundError:
                            return True
                        except (OSError, PermissionError):
                            # Failed to remove stale lock (permission denied, etc.)
                            return False

                    # Process exists and start time matches (or no start time available)
                    return False

                except psutil.NoSuchProcess:
                    # Process doesn't exist - lock is stale
                    log.warning(
                        "Removing stale lock - process not found", path=str(self.path), stale_pid=lock_pid
                    )
                    try:
                        self.path.unlink()
                        return True
                    except FileNotFoundError:
                        return True
                    except (OSError, PermissionError):
                        # Failed to remove stale lock (permission denied, etc.)
                        return False

                except psutil.AccessDenied:
                    # Can't check process - assume it's valid to be safe
                    return False
            else:
                # Fallback: Basic PID existence check using os.kill(pid, 0)
                # WARNING: This does NOT protect against PID recycling
                try:
                    os.kill(lock_pid, 0)  # Signal 0 just checks if process exists
                    # Process exists - lock is valid
                    return False
                except OSError:
                    # Process doesn't exist - lock is stale
                    log.warning(
                        "Removing stale lock - process not found (basic check)",
                        path=str(self.path),
                        stale_pid=lock_pid,
                        hint="For PID recycling protection, install psutil: pip install provide-foundation[process]",
                    )
                    try:
                        self.path.unlink()
                        return True
                    except FileNotFoundError:
                        return True
                    except (OSError, PermissionError):
                        # Failed to remove stale lock (permission denied, etc.)
                        return False

        except Exception as e:
            # Generic catch intentional: Safety net for security-critical lock validation.
            # Catches any unexpected errors (psutil errors, filesystem issues, etc.)
            # Fail-safe: return False to assume lock is valid rather than risk corruption.
            log.debug("Error checking stale lock", path=str(self.path), error=str(e))
            return False

        return False

    def __enter__(self) -> FileLock:
        """Context manager entry."""
        self.acquire()
        return self

    def __exit__(self, exc_type: object, exc_val: object, exc_tb: object) -> None:
        """Context manager exit."""
        self.release()


__all__ = [
    "FileLock",
    "LockError",
]

# 🧱🏗️🔚
