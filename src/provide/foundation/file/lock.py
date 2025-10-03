from __future__ import annotations

import json
import os
from pathlib import Path
import socket
import time

import psutil

from provide.foundation.config.defaults import DEFAULT_FILE_LOCK_TIMEOUT
from provide.foundation.errors.resources import LockError
from provide.foundation.logger import get_logger

"""File-based locking for concurrent access control.

Uses psutil for robust process validation to prevent PID recycling attacks.
"""

log = get_logger(__name__)


class FileLock:
    """File-based lock for concurrent access control.

    Uses exclusive file creation as the locking mechanism.
    The lock file contains the PID of the process holding the lock.

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

    def acquire(self, blocking: bool = True) -> bool:
        """Acquire the lock.

        Args:
            blocking: If True, wait for lock. If False, return immediately.

        Returns:
            True if lock acquired, False if not (non-blocking mode only)

        Raises:
            LockError: If timeout exceeded (blocking mode)

        """
        if self.timeout <= 0:
            raise LockError("Timeout must be positive", code="INVALID_TIMEOUT", path=str(self.path))

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
                    # Add process start time for PID recycling protection
                    try:
                        proc = psutil.Process(self.pid)
                        lock_info["start_time"] = proc.create_time()
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        pass
                    os.write(fd, json.dumps(lock_info).encode())
                finally:
                    os.close(fd)

                self.locked = True
                elapsed = current_time - start_time
                log.debug(
                    "Acquired lock", path=str(self.path), pid=self.pid, iterations=iteration, elapsed=elapsed
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
        if not self.locked:
            return

        try:
            # Verify we own the lock before removing
            if self.path.exists():
                try:
                    content = self.path.read_text().strip()
                    # Try parsing as JSON first (new format)
                    try:
                        lock_info = json.loads(content)
                        owner_pid = lock_info.get("pid")
                    except (json.JSONDecodeError, ValueError):
                        # Fall back to plain PID format (old format)
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
        except Exception as e:
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
            except Exception:
                # If we can't read the file, assume it's not stale
                return False

            # Try parsing as JSON first (new format with start_time)
            lock_pid = None
            lock_start_time = None
            try:
                lock_info = json.loads(content)
                lock_pid = lock_info.get("pid")
                lock_start_time = lock_info.get("start_time")
            except (json.JSONDecodeError, ValueError):
                # Fall back to plain PID format (old format)
                if content.isdigit():
                    lock_pid = int(content)
                else:
                    log.debug("Invalid lock file content", path=str(self.path), content=content[:50])
                    return False

            if lock_pid is None:
                log.debug("No PID in lock file", path=str(self.path))
                return False

            # Validate process with psutil for robust PID recycling protection
            try:
                proc = psutil.Process(lock_pid)

                # If we have start_time, validate it matches to prevent PID recycling
                if lock_start_time is not None:
                    proc_start_time = proc.create_time()
                    # Allow 1 second tolerance for timestamp precision differences
                    if abs(proc_start_time - lock_start_time) > 1.0:
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
                        except Exception:
                            return False

                # Process exists and start time matches (or no start time available)
                return False

            except psutil.NoSuchProcess:
                # Process doesn't exist - lock is stale
                log.warning("Removing stale lock - process not found", path=str(self.path), stale_pid=lock_pid)
                try:
                    self.path.unlink()
                    return True
                except FileNotFoundError:
                    return True
                except Exception:
                    return False

            except psutil.AccessDenied:
                # Can't check process - assume it's valid to be safe
                return False

        except Exception as e:
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
