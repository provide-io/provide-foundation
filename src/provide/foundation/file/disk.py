#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Disk space and filesystem utilities.

Provides functions for checking available disk space before performing
operations that may require significant storage."""

from __future__ import annotations

import os
from pathlib import Path

from provide.foundation.logger import get_logger

log = get_logger(__name__)


def get_available_space(path: Path) -> int | None:
    """Get available disk space in bytes for a path.

    Args:
        path: Directory path to check (uses parent if path doesn't exist)

    Returns:
        Available bytes or None if unable to determine

    Examples:
        >>> from pathlib import Path
        >>> space = get_available_space(Path.home())
        >>> space is not None and space > 0
        True

    Notes:
        Uses os.statvfs on Unix-like systems (Linux, macOS, BSD).
        Returns None on Windows or if statvfs is unavailable.
    """
    try:
        # Use the path if it exists, otherwise use parent directory
        check_path = path if path.exists() else path.parent

        # Get filesystem statistics (Unix-like systems only)
        stat_result = os.statvfs(check_path)

        # Calculate available space: blocks available * block size
        available = stat_result.f_bavail * stat_result.f_frsize

        log.trace(
            "Disk space checked",
            path=str(check_path),
            available_bytes=available,
            available_gb=f"{available / (1024**3):.2f}",
        )

        return available

    except (AttributeError, OSError) as e:
        # AttributeError: statvfs not available (Windows)
        # OSError: permission denied or path issues
        log.debug(
            "Could not check disk space",
            path=str(path),
            error=str(e),
            error_type=type(e).__name__,
        )
        return None


def check_disk_space(
    path: Path,
    required_bytes: int,
    raise_on_insufficient: bool = True,
) -> bool:
    """Check if sufficient disk space is available.

    Args:
        path: Directory path to check (or parent if it doesn't exist)
        required_bytes: Number of bytes required
        raise_on_insufficient: Raise OSError if insufficient space (default: True)

    Returns:
        True if sufficient space available, False otherwise

    Raises:
        OSError: If insufficient space and raise_on_insufficient=True

    Examples:
        >>> from pathlib import Path
        >>> # Check if 1GB is available
        >>> check_disk_space(Path.home(), 1024**3, raise_on_insufficient=False)
        True

        >>> # Will raise if insufficient (default behavior)
        >>> check_disk_space(Path.home(), 10**15)  # doctest: +SKIP
        Traceback (most recent call last):
            ...
        OSError: Insufficient disk space...

    Notes:
        On systems where disk space cannot be determined (e.g., Windows
        without proper permissions), this function logs a warning but
        does not fail, returning True to allow the operation to proceed.
    """
    try:
        # Use parent directory if path doesn't exist yet
        check_path = path if path.exists() else path.parent

        # Get available disk space
        available = get_available_space(check_path)

        # If we can't determine space, log warning and allow operation
        if available is None:
            log.warning(
                "Could not determine disk space, operation will proceed",
                path=str(path),
                required_bytes=required_bytes,
            )
            return True

        # Convert to GB for human-readable logging
        required_gb = required_bytes / (1024**3)
        available_gb = available / (1024**3)

        log.debug(
            "Disk space requirement check",
            path=str(check_path),
            required_gb=f"{required_gb:.2f}",
            available_gb=f"{available_gb:.2f}",
            sufficient=available >= required_bytes,
        )

        # Check if sufficient space available
        if available < required_bytes:
            error_msg = (
                f"Insufficient disk space at {check_path}: "
                f"need {required_gb:.2f} GB, have {available_gb:.2f} GB"
            )

            log.error(
                "Insufficient disk space",
                path=str(check_path),
                required_gb=f"{required_gb:.2f}",
                available_gb=f"{available_gb:.2f}",
                shortfall_gb=f"{(required_bytes - available) / (1024**3):.2f}",
            )

            if raise_on_insufficient:
                raise OSError(error_msg)

            return False

        return True

    except OSError:
        # Re-raise OSError from insufficient space check
        raise
    except Exception as e:
        # Unexpected error - log but don't fail
        log.warning(
            "Unexpected error checking disk space, operation will proceed",
            path=str(path),
            error=str(e),
            error_type=type(e).__name__,
        )
        return True


def get_disk_usage(path: Path) -> tuple[int, int, int] | None:
    """Get total, used, and free disk space for a path.

    Args:
        path: Directory path to check

    Returns:
        Tuple of (total, used, free) in bytes, or None if unable to determine

    Examples:
        >>> from pathlib import Path
        >>> usage = get_disk_usage(Path.home())
        >>> if usage:
        ...     total, used, free = usage
        ...     assert total > 0 and used >= 0 and free > 0
        ...     assert total >= used + free  # May have reserved space

    Notes:
        Uses os.statvfs on Unix-like systems.
        Returns None on Windows or if unavailable.
    """
    try:
        check_path = path if path.exists() else path.parent

        stat_result = os.statvfs(check_path)

        # Total space: total blocks * block size
        total = stat_result.f_blocks * stat_result.f_frsize

        # Free space: free blocks * block size
        free = stat_result.f_bfree * stat_result.f_frsize

        # Used space: total - free
        used = total - free

        log.trace(
            "Disk usage retrieved",
            path=str(check_path),
            total_gb=f"{total / (1024**3):.2f}",
            used_gb=f"{used / (1024**3):.2f}",
            free_gb=f"{free / (1024**3):.2f}",
        )

        return (total, used, free)

    except (AttributeError, OSError) as e:
        log.debug(
            "Could not get disk usage",
            path=str(path),
            error=str(e),
        )
        return None


def format_bytes(num_bytes: int) -> str:
    """Format bytes as human-readable string.

    Args:
        num_bytes: Number of bytes

    Returns:
        Formatted string (e.g., "1.50 GB", "256.00 MB")

    Examples:
        >>> format_bytes(1024)
        '1.00 KB'
        >>> format_bytes(1024**2)
        '1.00 MB'
        >>> format_bytes(1536 * 1024**2)
        '1.50 GB'
        >>> format_bytes(500)
        '500 B'
    """
    num_bytes_float: float = float(num_bytes)
    for unit in ["B", "KB", "MB", "GB", "TB", "PB"]:
        if num_bytes_float < 1024.0 or unit == "PB":
            return f"{num_bytes_float:.2f} {unit}"
        num_bytes_float /= 1024.0
    return f"{num_bytes_float:.2f} PB"


__all__ = [
    "check_disk_space",
    "format_bytes",
    "get_available_space",
    "get_disk_usage",
]

# 🧱🏗️🔚
