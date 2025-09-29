from __future__ import annotations

import os
from pathlib import Path
import time

from provide.foundation.config.defaults import DEFAULT_FILE_LOCK_TIMEOUT
from provide.foundation.errors.resources import LockError
from provide.foundation.logger import get_logger

"""File-based locking for concurrent access control."""

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

        start_time = time.time()
        attempts = 0
        max_attempts = max(1, int(self.timeout / self.check_interval)) + 10  # Safety margin

        while True:
            attempts += 1
            current_time = time.time()
            elapsed = current_time - start_time

            # Multiple timeout checks to prevent any chance of infinite loop
            if elapsed >= self.timeout or attempts > max_attempts:
                raise LockError(
                    f"Failed to acquire lock within {self.timeout}s (elapsed: {elapsed:.3f}s, attempts: {attempts})",
                    code="LOCK_TIMEOUT",
                    path=str(self.path),
                ) from None

            try:
                # Try to create lock file exclusively
                fd = os.open(str(self.path), os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o644)
                try:
                    # Write our PID to the lock file
                    os.write(fd, str(self.pid).encode())
                finally:
                    os.close(fd)

                self.locked = True
                log.debug(
                    "Acquired lock", path=str(self.path), pid=self.pid, attempts=attempts, elapsed=elapsed
                )
                return True

            except FileExistsError:
                # Lock file exists, check if holder is still alive
                if self._check_stale_lock():
                    continue  # Retry after removing stale lock

                if not blocking:
                    log.debug("Lock unavailable (non-blocking)", path=str(self.path))
                    return False

                # Calculate remaining time with extra safety checks
                remaining = self.timeout - elapsed
                if remaining <= 0.001:  # Give 1ms grace period
                    # Time is essentially up
                    continue

                # Sleep for a safe amount, never more than remaining time
                sleep_time = min(self.check_interval, remaining * 0.9)  # Use 90% of remaining
                if sleep_time > 0.001:  # Only sleep if meaningful time left
                    time.sleep(sleep_time)

                # Emergency timeout check after sleep
                if time.time() - start_time >= self.timeout:
                    break

        # Final timeout raise if we exit the loop
        raise LockError(
            f"Failed to acquire lock within {self.timeout}s",
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
                    if content == str(self.pid):
                        self.path.unlink()
                        log.debug("Released lock", path=str(self.path), pid=self.pid)
                    else:
                        log.warning(
                            "Lock owned by different process",
                            path=str(self.path),
                            owner_pid=content,
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

    def _check_stale_lock(self) -> bool:
        """Check if lock file is stale and remove if so.

        Returns:
            True if stale lock was removed, False otherwise

        """
        try:
            if not self.path.exists():
                return False

            content = self.path.read_text().strip()
            if content.isdigit():
                lock_pid = int(content)

                # Check if process is still alive
                try:
                    os.kill(lock_pid, 0)
                    # Process exists
                    return False
                except ProcessLookupError:
                    # Process doesn't exist, lock is stale
                    log.warning("Removing stale lock", path=str(self.path), stale_pid=lock_pid)
                    try:
                        self.path.unlink()
                        return True
                    except FileNotFoundError:
                        # Someone else removed it, that's fine
                        return True
            else:
                # Invalid lock file content, don't remove it as we can't be sure
                log.debug("Invalid lock file content", path=str(self.path), content=content)
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
