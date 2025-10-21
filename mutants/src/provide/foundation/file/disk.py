# provide/foundation/file/disk.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

"""Disk space and filesystem utilities.

Provides functions for checking available disk space before performing
operations that may require significant storage.
"""

from __future__ import annotations

import os
from pathlib import Path

from provide.foundation.logger import get_logger

log = get_logger(__name__)
from inspect import signature as _mutmut_signature
from typing import Annotated
from typing import Callable
from typing import ClassVar


MutantDict = Annotated[dict[str, Callable], "Mutant"]


def _mutmut_trampoline(orig, mutants, call_args, call_kwargs, self_arg = None):
    """Forward call to original or mutated function, depending on the environment"""
    import os
    mutant_under_test = os.environ['MUTANT_UNDER_TEST']
    if mutant_under_test == 'fail':
        from mutmut.__main__ import MutmutProgrammaticFailException
        raise MutmutProgrammaticFailException('Failed programmatically')      
    elif mutant_under_test == 'stats':
        from mutmut.__main__ import record_trampoline_hit
        record_trampoline_hit(orig.__module__ + '.' + orig.__name__)
        result = orig(*call_args, **call_kwargs)
        return result
    prefix = orig.__module__ + '.' + orig.__name__ + '__mutmut_'
    if not mutant_under_test.startswith(prefix):
        result = orig(*call_args, **call_kwargs)
        return result
    mutant_name = mutant_under_test.rpartition('.')[-1]
    if self_arg:
        # call to a class method where self is not bound
        result = mutants[mutant_name](self_arg, *call_args, **call_kwargs)
    else:
        result = mutants[mutant_name](*call_args, **call_kwargs)
    return result


def x_get_available_space__mutmut_orig(path: Path) -> int | None:
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


def x_get_available_space__mutmut_1(path: Path) -> int | None:
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
        check_path = None

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


def x_get_available_space__mutmut_2(path: Path) -> int | None:
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
        stat_result = None

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


def x_get_available_space__mutmut_3(path: Path) -> int | None:
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
        stat_result = os.statvfs(None)

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


def x_get_available_space__mutmut_4(path: Path) -> int | None:
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
        available = None

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


def x_get_available_space__mutmut_5(path: Path) -> int | None:
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
        available = stat_result.f_bavail / stat_result.f_frsize

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


def x_get_available_space__mutmut_6(path: Path) -> int | None:
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
            None,
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


def x_get_available_space__mutmut_7(path: Path) -> int | None:
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
            path=None,
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


def x_get_available_space__mutmut_8(path: Path) -> int | None:
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
            available_bytes=None,
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


def x_get_available_space__mutmut_9(path: Path) -> int | None:
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
            available_gb=None,
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


def x_get_available_space__mutmut_10(path: Path) -> int | None:
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


def x_get_available_space__mutmut_11(path: Path) -> int | None:
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


def x_get_available_space__mutmut_12(path: Path) -> int | None:
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


def x_get_available_space__mutmut_13(path: Path) -> int | None:
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


def x_get_available_space__mutmut_14(path: Path) -> int | None:
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
            "XXDisk space checkedXX",
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


def x_get_available_space__mutmut_15(path: Path) -> int | None:
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
            "disk space checked",
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


def x_get_available_space__mutmut_16(path: Path) -> int | None:
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
            "DISK SPACE CHECKED",
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


def x_get_available_space__mutmut_17(path: Path) -> int | None:
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
            path=str(None),
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


def x_get_available_space__mutmut_18(path: Path) -> int | None:
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
            available_gb=f"{available * (1024**3):.2f}",
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


def x_get_available_space__mutmut_19(path: Path) -> int | None:
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
            available_gb=f"{available / (1024 * 3):.2f}",
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


def x_get_available_space__mutmut_20(path: Path) -> int | None:
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
            available_gb=f"{available / (1025**3):.2f}",
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


def x_get_available_space__mutmut_21(path: Path) -> int | None:
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
            available_gb=f"{available / (1024**4):.2f}",
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


def x_get_available_space__mutmut_22(path: Path) -> int | None:
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
            None,
            path=str(path),
            error=str(e),
            error_type=type(e).__name__,
        )
        return None


def x_get_available_space__mutmut_23(path: Path) -> int | None:
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
            path=None,
            error=str(e),
            error_type=type(e).__name__,
        )
        return None


def x_get_available_space__mutmut_24(path: Path) -> int | None:
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
            error=None,
            error_type=type(e).__name__,
        )
        return None


def x_get_available_space__mutmut_25(path: Path) -> int | None:
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
            error_type=None,
        )
        return None


def x_get_available_space__mutmut_26(path: Path) -> int | None:
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
            path=str(path),
            error=str(e),
            error_type=type(e).__name__,
        )
        return None


def x_get_available_space__mutmut_27(path: Path) -> int | None:
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
            error=str(e),
            error_type=type(e).__name__,
        )
        return None


def x_get_available_space__mutmut_28(path: Path) -> int | None:
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
            error_type=type(e).__name__,
        )
        return None


def x_get_available_space__mutmut_29(path: Path) -> int | None:
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
            )
        return None


def x_get_available_space__mutmut_30(path: Path) -> int | None:
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
            "XXCould not check disk spaceXX",
            path=str(path),
            error=str(e),
            error_type=type(e).__name__,
        )
        return None


def x_get_available_space__mutmut_31(path: Path) -> int | None:
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
            "could not check disk space",
            path=str(path),
            error=str(e),
            error_type=type(e).__name__,
        )
        return None


def x_get_available_space__mutmut_32(path: Path) -> int | None:
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
            "COULD NOT CHECK DISK SPACE",
            path=str(path),
            error=str(e),
            error_type=type(e).__name__,
        )
        return None


def x_get_available_space__mutmut_33(path: Path) -> int | None:
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
            path=str(None),
            error=str(e),
            error_type=type(e).__name__,
        )
        return None


def x_get_available_space__mutmut_34(path: Path) -> int | None:
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
            error=str(None),
            error_type=type(e).__name__,
        )
        return None


def x_get_available_space__mutmut_35(path: Path) -> int | None:
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
            error_type=type(None).__name__,
        )
        return None

x_get_available_space__mutmut_mutants : ClassVar[MutantDict] = {
'x_get_available_space__mutmut_1': x_get_available_space__mutmut_1, 
    'x_get_available_space__mutmut_2': x_get_available_space__mutmut_2, 
    'x_get_available_space__mutmut_3': x_get_available_space__mutmut_3, 
    'x_get_available_space__mutmut_4': x_get_available_space__mutmut_4, 
    'x_get_available_space__mutmut_5': x_get_available_space__mutmut_5, 
    'x_get_available_space__mutmut_6': x_get_available_space__mutmut_6, 
    'x_get_available_space__mutmut_7': x_get_available_space__mutmut_7, 
    'x_get_available_space__mutmut_8': x_get_available_space__mutmut_8, 
    'x_get_available_space__mutmut_9': x_get_available_space__mutmut_9, 
    'x_get_available_space__mutmut_10': x_get_available_space__mutmut_10, 
    'x_get_available_space__mutmut_11': x_get_available_space__mutmut_11, 
    'x_get_available_space__mutmut_12': x_get_available_space__mutmut_12, 
    'x_get_available_space__mutmut_13': x_get_available_space__mutmut_13, 
    'x_get_available_space__mutmut_14': x_get_available_space__mutmut_14, 
    'x_get_available_space__mutmut_15': x_get_available_space__mutmut_15, 
    'x_get_available_space__mutmut_16': x_get_available_space__mutmut_16, 
    'x_get_available_space__mutmut_17': x_get_available_space__mutmut_17, 
    'x_get_available_space__mutmut_18': x_get_available_space__mutmut_18, 
    'x_get_available_space__mutmut_19': x_get_available_space__mutmut_19, 
    'x_get_available_space__mutmut_20': x_get_available_space__mutmut_20, 
    'x_get_available_space__mutmut_21': x_get_available_space__mutmut_21, 
    'x_get_available_space__mutmut_22': x_get_available_space__mutmut_22, 
    'x_get_available_space__mutmut_23': x_get_available_space__mutmut_23, 
    'x_get_available_space__mutmut_24': x_get_available_space__mutmut_24, 
    'x_get_available_space__mutmut_25': x_get_available_space__mutmut_25, 
    'x_get_available_space__mutmut_26': x_get_available_space__mutmut_26, 
    'x_get_available_space__mutmut_27': x_get_available_space__mutmut_27, 
    'x_get_available_space__mutmut_28': x_get_available_space__mutmut_28, 
    'x_get_available_space__mutmut_29': x_get_available_space__mutmut_29, 
    'x_get_available_space__mutmut_30': x_get_available_space__mutmut_30, 
    'x_get_available_space__mutmut_31': x_get_available_space__mutmut_31, 
    'x_get_available_space__mutmut_32': x_get_available_space__mutmut_32, 
    'x_get_available_space__mutmut_33': x_get_available_space__mutmut_33, 
    'x_get_available_space__mutmut_34': x_get_available_space__mutmut_34, 
    'x_get_available_space__mutmut_35': x_get_available_space__mutmut_35
}

def get_available_space(*args, **kwargs):
    result = _mutmut_trampoline(x_get_available_space__mutmut_orig, x_get_available_space__mutmut_mutants, args, kwargs)
    return result 

get_available_space.__signature__ = _mutmut_signature(x_get_available_space__mutmut_orig)
x_get_available_space__mutmut_orig.__name__ = 'x_get_available_space'


def x_check_disk_space__mutmut_orig(
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


def x_check_disk_space__mutmut_1(
    path: Path,
    required_bytes: int,
    raise_on_insufficient: bool = False,
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


def x_check_disk_space__mutmut_2(
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
        check_path = None

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


def x_check_disk_space__mutmut_3(
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
        available = None

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


def x_check_disk_space__mutmut_4(
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
        available = get_available_space(None)

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


def x_check_disk_space__mutmut_5(
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
        if available is not None:
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


def x_check_disk_space__mutmut_6(
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
                None,
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


def x_check_disk_space__mutmut_7(
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
                path=None,
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


def x_check_disk_space__mutmut_8(
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
                required_bytes=None,
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


def x_check_disk_space__mutmut_9(
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


def x_check_disk_space__mutmut_10(
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


def x_check_disk_space__mutmut_11(
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


def x_check_disk_space__mutmut_12(
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
                "XXCould not determine disk space, operation will proceedXX",
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


def x_check_disk_space__mutmut_13(
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
                "could not determine disk space, operation will proceed",
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


def x_check_disk_space__mutmut_14(
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
                "COULD NOT DETERMINE DISK SPACE, OPERATION WILL PROCEED",
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


def x_check_disk_space__mutmut_15(
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
                path=str(None),
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


def x_check_disk_space__mutmut_16(
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
            return False

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


def x_check_disk_space__mutmut_17(
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
        required_gb = None
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


def x_check_disk_space__mutmut_18(
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
        required_gb = required_bytes * (1024**3)
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


def x_check_disk_space__mutmut_19(
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
        required_gb = required_bytes / (1024 * 3)
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


def x_check_disk_space__mutmut_20(
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
        required_gb = required_bytes / (1025**3)
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


def x_check_disk_space__mutmut_21(
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
        required_gb = required_bytes / (1024**4)
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


def x_check_disk_space__mutmut_22(
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
        available_gb = None

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


def x_check_disk_space__mutmut_23(
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
        available_gb = available * (1024**3)

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


def x_check_disk_space__mutmut_24(
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
        available_gb = available / (1024 * 3)

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


def x_check_disk_space__mutmut_25(
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
        available_gb = available / (1025**3)

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


def x_check_disk_space__mutmut_26(
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
        available_gb = available / (1024**4)

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


def x_check_disk_space__mutmut_27(
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
            None,
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


def x_check_disk_space__mutmut_28(
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
            path=None,
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


def x_check_disk_space__mutmut_29(
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
            required_gb=None,
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


def x_check_disk_space__mutmut_30(
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
            available_gb=None,
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


def x_check_disk_space__mutmut_31(
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
            sufficient=None,
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


def x_check_disk_space__mutmut_32(
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


def x_check_disk_space__mutmut_33(
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


def x_check_disk_space__mutmut_34(
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


def x_check_disk_space__mutmut_35(
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


def x_check_disk_space__mutmut_36(
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


def x_check_disk_space__mutmut_37(
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
            "XXDisk space requirement checkXX",
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


def x_check_disk_space__mutmut_38(
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
            "disk space requirement check",
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


def x_check_disk_space__mutmut_39(
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
            "DISK SPACE REQUIREMENT CHECK",
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


def x_check_disk_space__mutmut_40(
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
            path=str(None),
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


def x_check_disk_space__mutmut_41(
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
            sufficient=available > required_bytes,
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


def x_check_disk_space__mutmut_42(
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
        if available <= required_bytes:
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


def x_check_disk_space__mutmut_43(
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
            error_msg = None

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


def x_check_disk_space__mutmut_44(
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
                None,
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


def x_check_disk_space__mutmut_45(
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
                path=None,
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


def x_check_disk_space__mutmut_46(
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
                required_gb=None,
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


def x_check_disk_space__mutmut_47(
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
                available_gb=None,
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


def x_check_disk_space__mutmut_48(
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
                shortfall_gb=None,
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


def x_check_disk_space__mutmut_49(
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


def x_check_disk_space__mutmut_50(
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


def x_check_disk_space__mutmut_51(
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


def x_check_disk_space__mutmut_52(
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


def x_check_disk_space__mutmut_53(
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


def x_check_disk_space__mutmut_54(
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
                "XXInsufficient disk spaceXX",
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


def x_check_disk_space__mutmut_55(
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
                "insufficient disk space",
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


def x_check_disk_space__mutmut_56(
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
                "INSUFFICIENT DISK SPACE",
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


def x_check_disk_space__mutmut_57(
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
                path=str(None),
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


def x_check_disk_space__mutmut_58(
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
                shortfall_gb=f"{(required_bytes - available) * (1024**3):.2f}",
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


def x_check_disk_space__mutmut_59(
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
                shortfall_gb=f"{(required_bytes + available) / (1024**3):.2f}",
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


def x_check_disk_space__mutmut_60(
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
                shortfall_gb=f"{(required_bytes - available) / (1024 * 3):.2f}",
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


def x_check_disk_space__mutmut_61(
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
                shortfall_gb=f"{(required_bytes - available) / (1025**3):.2f}",
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


def x_check_disk_space__mutmut_62(
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
                shortfall_gb=f"{(required_bytes - available) / (1024**4):.2f}",
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


def x_check_disk_space__mutmut_63(
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
                raise OSError(None)

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


def x_check_disk_space__mutmut_64(
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

            return True

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


def x_check_disk_space__mutmut_65(
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

        return False

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


def x_check_disk_space__mutmut_66(
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
            None,
            path=str(path),
            error=str(e),
            error_type=type(e).__name__,
        )
        return True


def x_check_disk_space__mutmut_67(
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
            path=None,
            error=str(e),
            error_type=type(e).__name__,
        )
        return True


def x_check_disk_space__mutmut_68(
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
            error=None,
            error_type=type(e).__name__,
        )
        return True


def x_check_disk_space__mutmut_69(
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
            error_type=None,
        )
        return True


def x_check_disk_space__mutmut_70(
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
            path=str(path),
            error=str(e),
            error_type=type(e).__name__,
        )
        return True


def x_check_disk_space__mutmut_71(
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
            error=str(e),
            error_type=type(e).__name__,
        )
        return True


def x_check_disk_space__mutmut_72(
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
            error_type=type(e).__name__,
        )
        return True


def x_check_disk_space__mutmut_73(
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
            )
        return True


def x_check_disk_space__mutmut_74(
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
            "XXUnexpected error checking disk space, operation will proceedXX",
            path=str(path),
            error=str(e),
            error_type=type(e).__name__,
        )
        return True


def x_check_disk_space__mutmut_75(
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
            "unexpected error checking disk space, operation will proceed",
            path=str(path),
            error=str(e),
            error_type=type(e).__name__,
        )
        return True


def x_check_disk_space__mutmut_76(
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
            "UNEXPECTED ERROR CHECKING DISK SPACE, OPERATION WILL PROCEED",
            path=str(path),
            error=str(e),
            error_type=type(e).__name__,
        )
        return True


def x_check_disk_space__mutmut_77(
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
            path=str(None),
            error=str(e),
            error_type=type(e).__name__,
        )
        return True


def x_check_disk_space__mutmut_78(
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
            error=str(None),
            error_type=type(e).__name__,
        )
        return True


def x_check_disk_space__mutmut_79(
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
            error_type=type(None).__name__,
        )
        return True


def x_check_disk_space__mutmut_80(
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
        return False

x_check_disk_space__mutmut_mutants : ClassVar[MutantDict] = {
'x_check_disk_space__mutmut_1': x_check_disk_space__mutmut_1, 
    'x_check_disk_space__mutmut_2': x_check_disk_space__mutmut_2, 
    'x_check_disk_space__mutmut_3': x_check_disk_space__mutmut_3, 
    'x_check_disk_space__mutmut_4': x_check_disk_space__mutmut_4, 
    'x_check_disk_space__mutmut_5': x_check_disk_space__mutmut_5, 
    'x_check_disk_space__mutmut_6': x_check_disk_space__mutmut_6, 
    'x_check_disk_space__mutmut_7': x_check_disk_space__mutmut_7, 
    'x_check_disk_space__mutmut_8': x_check_disk_space__mutmut_8, 
    'x_check_disk_space__mutmut_9': x_check_disk_space__mutmut_9, 
    'x_check_disk_space__mutmut_10': x_check_disk_space__mutmut_10, 
    'x_check_disk_space__mutmut_11': x_check_disk_space__mutmut_11, 
    'x_check_disk_space__mutmut_12': x_check_disk_space__mutmut_12, 
    'x_check_disk_space__mutmut_13': x_check_disk_space__mutmut_13, 
    'x_check_disk_space__mutmut_14': x_check_disk_space__mutmut_14, 
    'x_check_disk_space__mutmut_15': x_check_disk_space__mutmut_15, 
    'x_check_disk_space__mutmut_16': x_check_disk_space__mutmut_16, 
    'x_check_disk_space__mutmut_17': x_check_disk_space__mutmut_17, 
    'x_check_disk_space__mutmut_18': x_check_disk_space__mutmut_18, 
    'x_check_disk_space__mutmut_19': x_check_disk_space__mutmut_19, 
    'x_check_disk_space__mutmut_20': x_check_disk_space__mutmut_20, 
    'x_check_disk_space__mutmut_21': x_check_disk_space__mutmut_21, 
    'x_check_disk_space__mutmut_22': x_check_disk_space__mutmut_22, 
    'x_check_disk_space__mutmut_23': x_check_disk_space__mutmut_23, 
    'x_check_disk_space__mutmut_24': x_check_disk_space__mutmut_24, 
    'x_check_disk_space__mutmut_25': x_check_disk_space__mutmut_25, 
    'x_check_disk_space__mutmut_26': x_check_disk_space__mutmut_26, 
    'x_check_disk_space__mutmut_27': x_check_disk_space__mutmut_27, 
    'x_check_disk_space__mutmut_28': x_check_disk_space__mutmut_28, 
    'x_check_disk_space__mutmut_29': x_check_disk_space__mutmut_29, 
    'x_check_disk_space__mutmut_30': x_check_disk_space__mutmut_30, 
    'x_check_disk_space__mutmut_31': x_check_disk_space__mutmut_31, 
    'x_check_disk_space__mutmut_32': x_check_disk_space__mutmut_32, 
    'x_check_disk_space__mutmut_33': x_check_disk_space__mutmut_33, 
    'x_check_disk_space__mutmut_34': x_check_disk_space__mutmut_34, 
    'x_check_disk_space__mutmut_35': x_check_disk_space__mutmut_35, 
    'x_check_disk_space__mutmut_36': x_check_disk_space__mutmut_36, 
    'x_check_disk_space__mutmut_37': x_check_disk_space__mutmut_37, 
    'x_check_disk_space__mutmut_38': x_check_disk_space__mutmut_38, 
    'x_check_disk_space__mutmut_39': x_check_disk_space__mutmut_39, 
    'x_check_disk_space__mutmut_40': x_check_disk_space__mutmut_40, 
    'x_check_disk_space__mutmut_41': x_check_disk_space__mutmut_41, 
    'x_check_disk_space__mutmut_42': x_check_disk_space__mutmut_42, 
    'x_check_disk_space__mutmut_43': x_check_disk_space__mutmut_43, 
    'x_check_disk_space__mutmut_44': x_check_disk_space__mutmut_44, 
    'x_check_disk_space__mutmut_45': x_check_disk_space__mutmut_45, 
    'x_check_disk_space__mutmut_46': x_check_disk_space__mutmut_46, 
    'x_check_disk_space__mutmut_47': x_check_disk_space__mutmut_47, 
    'x_check_disk_space__mutmut_48': x_check_disk_space__mutmut_48, 
    'x_check_disk_space__mutmut_49': x_check_disk_space__mutmut_49, 
    'x_check_disk_space__mutmut_50': x_check_disk_space__mutmut_50, 
    'x_check_disk_space__mutmut_51': x_check_disk_space__mutmut_51, 
    'x_check_disk_space__mutmut_52': x_check_disk_space__mutmut_52, 
    'x_check_disk_space__mutmut_53': x_check_disk_space__mutmut_53, 
    'x_check_disk_space__mutmut_54': x_check_disk_space__mutmut_54, 
    'x_check_disk_space__mutmut_55': x_check_disk_space__mutmut_55, 
    'x_check_disk_space__mutmut_56': x_check_disk_space__mutmut_56, 
    'x_check_disk_space__mutmut_57': x_check_disk_space__mutmut_57, 
    'x_check_disk_space__mutmut_58': x_check_disk_space__mutmut_58, 
    'x_check_disk_space__mutmut_59': x_check_disk_space__mutmut_59, 
    'x_check_disk_space__mutmut_60': x_check_disk_space__mutmut_60, 
    'x_check_disk_space__mutmut_61': x_check_disk_space__mutmut_61, 
    'x_check_disk_space__mutmut_62': x_check_disk_space__mutmut_62, 
    'x_check_disk_space__mutmut_63': x_check_disk_space__mutmut_63, 
    'x_check_disk_space__mutmut_64': x_check_disk_space__mutmut_64, 
    'x_check_disk_space__mutmut_65': x_check_disk_space__mutmut_65, 
    'x_check_disk_space__mutmut_66': x_check_disk_space__mutmut_66, 
    'x_check_disk_space__mutmut_67': x_check_disk_space__mutmut_67, 
    'x_check_disk_space__mutmut_68': x_check_disk_space__mutmut_68, 
    'x_check_disk_space__mutmut_69': x_check_disk_space__mutmut_69, 
    'x_check_disk_space__mutmut_70': x_check_disk_space__mutmut_70, 
    'x_check_disk_space__mutmut_71': x_check_disk_space__mutmut_71, 
    'x_check_disk_space__mutmut_72': x_check_disk_space__mutmut_72, 
    'x_check_disk_space__mutmut_73': x_check_disk_space__mutmut_73, 
    'x_check_disk_space__mutmut_74': x_check_disk_space__mutmut_74, 
    'x_check_disk_space__mutmut_75': x_check_disk_space__mutmut_75, 
    'x_check_disk_space__mutmut_76': x_check_disk_space__mutmut_76, 
    'x_check_disk_space__mutmut_77': x_check_disk_space__mutmut_77, 
    'x_check_disk_space__mutmut_78': x_check_disk_space__mutmut_78, 
    'x_check_disk_space__mutmut_79': x_check_disk_space__mutmut_79, 
    'x_check_disk_space__mutmut_80': x_check_disk_space__mutmut_80
}

def check_disk_space(*args, **kwargs):
    result = _mutmut_trampoline(x_check_disk_space__mutmut_orig, x_check_disk_space__mutmut_mutants, args, kwargs)
    return result 

check_disk_space.__signature__ = _mutmut_signature(x_check_disk_space__mutmut_orig)
x_check_disk_space__mutmut_orig.__name__ = 'x_check_disk_space'


def x_get_disk_usage__mutmut_orig(path: Path) -> tuple[int, int, int] | None:
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


def x_get_disk_usage__mutmut_1(path: Path) -> tuple[int, int, int] | None:
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
        check_path = None

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


def x_get_disk_usage__mutmut_2(path: Path) -> tuple[int, int, int] | None:
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

        stat_result = None

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


def x_get_disk_usage__mutmut_3(path: Path) -> tuple[int, int, int] | None:
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

        stat_result = os.statvfs(None)

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


def x_get_disk_usage__mutmut_4(path: Path) -> tuple[int, int, int] | None:
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
        total = None

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


def x_get_disk_usage__mutmut_5(path: Path) -> tuple[int, int, int] | None:
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
        total = stat_result.f_blocks / stat_result.f_frsize

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


def x_get_disk_usage__mutmut_6(path: Path) -> tuple[int, int, int] | None:
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
        free = None

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


def x_get_disk_usage__mutmut_7(path: Path) -> tuple[int, int, int] | None:
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
        free = stat_result.f_bfree / stat_result.f_frsize

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


def x_get_disk_usage__mutmut_8(path: Path) -> tuple[int, int, int] | None:
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
        used = None

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


def x_get_disk_usage__mutmut_9(path: Path) -> tuple[int, int, int] | None:
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
        used = total + free

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


def x_get_disk_usage__mutmut_10(path: Path) -> tuple[int, int, int] | None:
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
            None,
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


def x_get_disk_usage__mutmut_11(path: Path) -> tuple[int, int, int] | None:
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
            path=None,
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


def x_get_disk_usage__mutmut_12(path: Path) -> tuple[int, int, int] | None:
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
            total_gb=None,
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


def x_get_disk_usage__mutmut_13(path: Path) -> tuple[int, int, int] | None:
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
            used_gb=None,
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


def x_get_disk_usage__mutmut_14(path: Path) -> tuple[int, int, int] | None:
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
            free_gb=None,
        )

        return (total, used, free)

    except (AttributeError, OSError) as e:
        log.debug(
            "Could not get disk usage",
            path=str(path),
            error=str(e),
        )
        return None


def x_get_disk_usage__mutmut_15(path: Path) -> tuple[int, int, int] | None:
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


def x_get_disk_usage__mutmut_16(path: Path) -> tuple[int, int, int] | None:
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


def x_get_disk_usage__mutmut_17(path: Path) -> tuple[int, int, int] | None:
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


def x_get_disk_usage__mutmut_18(path: Path) -> tuple[int, int, int] | None:
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


def x_get_disk_usage__mutmut_19(path: Path) -> tuple[int, int, int] | None:
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
            )

        return (total, used, free)

    except (AttributeError, OSError) as e:
        log.debug(
            "Could not get disk usage",
            path=str(path),
            error=str(e),
        )
        return None


def x_get_disk_usage__mutmut_20(path: Path) -> tuple[int, int, int] | None:
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
            "XXDisk usage retrievedXX",
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


def x_get_disk_usage__mutmut_21(path: Path) -> tuple[int, int, int] | None:
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
            "disk usage retrieved",
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


def x_get_disk_usage__mutmut_22(path: Path) -> tuple[int, int, int] | None:
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
            "DISK USAGE RETRIEVED",
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


def x_get_disk_usage__mutmut_23(path: Path) -> tuple[int, int, int] | None:
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
            path=str(None),
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


def x_get_disk_usage__mutmut_24(path: Path) -> tuple[int, int, int] | None:
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
            total_gb=f"{total * (1024**3):.2f}",
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


def x_get_disk_usage__mutmut_25(path: Path) -> tuple[int, int, int] | None:
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
            total_gb=f"{total / (1024 * 3):.2f}",
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


def x_get_disk_usage__mutmut_26(path: Path) -> tuple[int, int, int] | None:
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
            total_gb=f"{total / (1025**3):.2f}",
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


def x_get_disk_usage__mutmut_27(path: Path) -> tuple[int, int, int] | None:
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
            total_gb=f"{total / (1024**4):.2f}",
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


def x_get_disk_usage__mutmut_28(path: Path) -> tuple[int, int, int] | None:
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
            used_gb=f"{used * (1024**3):.2f}",
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


def x_get_disk_usage__mutmut_29(path: Path) -> tuple[int, int, int] | None:
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
            used_gb=f"{used / (1024 * 3):.2f}",
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


def x_get_disk_usage__mutmut_30(path: Path) -> tuple[int, int, int] | None:
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
            used_gb=f"{used / (1025**3):.2f}",
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


def x_get_disk_usage__mutmut_31(path: Path) -> tuple[int, int, int] | None:
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
            used_gb=f"{used / (1024**4):.2f}",
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


def x_get_disk_usage__mutmut_32(path: Path) -> tuple[int, int, int] | None:
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
            free_gb=f"{free * (1024**3):.2f}",
        )

        return (total, used, free)

    except (AttributeError, OSError) as e:
        log.debug(
            "Could not get disk usage",
            path=str(path),
            error=str(e),
        )
        return None


def x_get_disk_usage__mutmut_33(path: Path) -> tuple[int, int, int] | None:
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
            free_gb=f"{free / (1024 * 3):.2f}",
        )

        return (total, used, free)

    except (AttributeError, OSError) as e:
        log.debug(
            "Could not get disk usage",
            path=str(path),
            error=str(e),
        )
        return None


def x_get_disk_usage__mutmut_34(path: Path) -> tuple[int, int, int] | None:
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
            free_gb=f"{free / (1025**3):.2f}",
        )

        return (total, used, free)

    except (AttributeError, OSError) as e:
        log.debug(
            "Could not get disk usage",
            path=str(path),
            error=str(e),
        )
        return None


def x_get_disk_usage__mutmut_35(path: Path) -> tuple[int, int, int] | None:
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
            free_gb=f"{free / (1024**4):.2f}",
        )

        return (total, used, free)

    except (AttributeError, OSError) as e:
        log.debug(
            "Could not get disk usage",
            path=str(path),
            error=str(e),
        )
        return None


def x_get_disk_usage__mutmut_36(path: Path) -> tuple[int, int, int] | None:
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
            None,
            path=str(path),
            error=str(e),
        )
        return None


def x_get_disk_usage__mutmut_37(path: Path) -> tuple[int, int, int] | None:
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
            path=None,
            error=str(e),
        )
        return None


def x_get_disk_usage__mutmut_38(path: Path) -> tuple[int, int, int] | None:
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
            error=None,
        )
        return None


def x_get_disk_usage__mutmut_39(path: Path) -> tuple[int, int, int] | None:
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
            path=str(path),
            error=str(e),
        )
        return None


def x_get_disk_usage__mutmut_40(path: Path) -> tuple[int, int, int] | None:
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
            error=str(e),
        )
        return None


def x_get_disk_usage__mutmut_41(path: Path) -> tuple[int, int, int] | None:
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
            )
        return None


def x_get_disk_usage__mutmut_42(path: Path) -> tuple[int, int, int] | None:
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
            "XXCould not get disk usageXX",
            path=str(path),
            error=str(e),
        )
        return None


def x_get_disk_usage__mutmut_43(path: Path) -> tuple[int, int, int] | None:
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
            "could not get disk usage",
            path=str(path),
            error=str(e),
        )
        return None


def x_get_disk_usage__mutmut_44(path: Path) -> tuple[int, int, int] | None:
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
            "COULD NOT GET DISK USAGE",
            path=str(path),
            error=str(e),
        )
        return None


def x_get_disk_usage__mutmut_45(path: Path) -> tuple[int, int, int] | None:
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
            path=str(None),
            error=str(e),
        )
        return None


def x_get_disk_usage__mutmut_46(path: Path) -> tuple[int, int, int] | None:
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
            error=str(None),
        )
        return None

x_get_disk_usage__mutmut_mutants : ClassVar[MutantDict] = {
'x_get_disk_usage__mutmut_1': x_get_disk_usage__mutmut_1, 
    'x_get_disk_usage__mutmut_2': x_get_disk_usage__mutmut_2, 
    'x_get_disk_usage__mutmut_3': x_get_disk_usage__mutmut_3, 
    'x_get_disk_usage__mutmut_4': x_get_disk_usage__mutmut_4, 
    'x_get_disk_usage__mutmut_5': x_get_disk_usage__mutmut_5, 
    'x_get_disk_usage__mutmut_6': x_get_disk_usage__mutmut_6, 
    'x_get_disk_usage__mutmut_7': x_get_disk_usage__mutmut_7, 
    'x_get_disk_usage__mutmut_8': x_get_disk_usage__mutmut_8, 
    'x_get_disk_usage__mutmut_9': x_get_disk_usage__mutmut_9, 
    'x_get_disk_usage__mutmut_10': x_get_disk_usage__mutmut_10, 
    'x_get_disk_usage__mutmut_11': x_get_disk_usage__mutmut_11, 
    'x_get_disk_usage__mutmut_12': x_get_disk_usage__mutmut_12, 
    'x_get_disk_usage__mutmut_13': x_get_disk_usage__mutmut_13, 
    'x_get_disk_usage__mutmut_14': x_get_disk_usage__mutmut_14, 
    'x_get_disk_usage__mutmut_15': x_get_disk_usage__mutmut_15, 
    'x_get_disk_usage__mutmut_16': x_get_disk_usage__mutmut_16, 
    'x_get_disk_usage__mutmut_17': x_get_disk_usage__mutmut_17, 
    'x_get_disk_usage__mutmut_18': x_get_disk_usage__mutmut_18, 
    'x_get_disk_usage__mutmut_19': x_get_disk_usage__mutmut_19, 
    'x_get_disk_usage__mutmut_20': x_get_disk_usage__mutmut_20, 
    'x_get_disk_usage__mutmut_21': x_get_disk_usage__mutmut_21, 
    'x_get_disk_usage__mutmut_22': x_get_disk_usage__mutmut_22, 
    'x_get_disk_usage__mutmut_23': x_get_disk_usage__mutmut_23, 
    'x_get_disk_usage__mutmut_24': x_get_disk_usage__mutmut_24, 
    'x_get_disk_usage__mutmut_25': x_get_disk_usage__mutmut_25, 
    'x_get_disk_usage__mutmut_26': x_get_disk_usage__mutmut_26, 
    'x_get_disk_usage__mutmut_27': x_get_disk_usage__mutmut_27, 
    'x_get_disk_usage__mutmut_28': x_get_disk_usage__mutmut_28, 
    'x_get_disk_usage__mutmut_29': x_get_disk_usage__mutmut_29, 
    'x_get_disk_usage__mutmut_30': x_get_disk_usage__mutmut_30, 
    'x_get_disk_usage__mutmut_31': x_get_disk_usage__mutmut_31, 
    'x_get_disk_usage__mutmut_32': x_get_disk_usage__mutmut_32, 
    'x_get_disk_usage__mutmut_33': x_get_disk_usage__mutmut_33, 
    'x_get_disk_usage__mutmut_34': x_get_disk_usage__mutmut_34, 
    'x_get_disk_usage__mutmut_35': x_get_disk_usage__mutmut_35, 
    'x_get_disk_usage__mutmut_36': x_get_disk_usage__mutmut_36, 
    'x_get_disk_usage__mutmut_37': x_get_disk_usage__mutmut_37, 
    'x_get_disk_usage__mutmut_38': x_get_disk_usage__mutmut_38, 
    'x_get_disk_usage__mutmut_39': x_get_disk_usage__mutmut_39, 
    'x_get_disk_usage__mutmut_40': x_get_disk_usage__mutmut_40, 
    'x_get_disk_usage__mutmut_41': x_get_disk_usage__mutmut_41, 
    'x_get_disk_usage__mutmut_42': x_get_disk_usage__mutmut_42, 
    'x_get_disk_usage__mutmut_43': x_get_disk_usage__mutmut_43, 
    'x_get_disk_usage__mutmut_44': x_get_disk_usage__mutmut_44, 
    'x_get_disk_usage__mutmut_45': x_get_disk_usage__mutmut_45, 
    'x_get_disk_usage__mutmut_46': x_get_disk_usage__mutmut_46
}

def get_disk_usage(*args, **kwargs):
    result = _mutmut_trampoline(x_get_disk_usage__mutmut_orig, x_get_disk_usage__mutmut_mutants, args, kwargs)
    return result 

get_disk_usage.__signature__ = _mutmut_signature(x_get_disk_usage__mutmut_orig)
x_get_disk_usage__mutmut_orig.__name__ = 'x_get_disk_usage'


def x_format_bytes__mutmut_orig(num_bytes: int) -> str:
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


def x_format_bytes__mutmut_1(num_bytes: int) -> str:
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
    num_bytes_float: float = None
    for unit in ["B", "KB", "MB", "GB", "TB", "PB"]:
        if num_bytes_float < 1024.0 or unit == "PB":
            return f"{num_bytes_float:.2f} {unit}"
        num_bytes_float /= 1024.0
    return f"{num_bytes_float:.2f} PB"


def x_format_bytes__mutmut_2(num_bytes: int) -> str:
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
    num_bytes_float: float = float(None)
    for unit in ["B", "KB", "MB", "GB", "TB", "PB"]:
        if num_bytes_float < 1024.0 or unit == "PB":
            return f"{num_bytes_float:.2f} {unit}"
        num_bytes_float /= 1024.0
    return f"{num_bytes_float:.2f} PB"


def x_format_bytes__mutmut_3(num_bytes: int) -> str:
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
    for unit in ["XXBXX", "KB", "MB", "GB", "TB", "PB"]:
        if num_bytes_float < 1024.0 or unit == "PB":
            return f"{num_bytes_float:.2f} {unit}"
        num_bytes_float /= 1024.0
    return f"{num_bytes_float:.2f} PB"


def x_format_bytes__mutmut_4(num_bytes: int) -> str:
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
    for unit in ["b", "KB", "MB", "GB", "TB", "PB"]:
        if num_bytes_float < 1024.0 or unit == "PB":
            return f"{num_bytes_float:.2f} {unit}"
        num_bytes_float /= 1024.0
    return f"{num_bytes_float:.2f} PB"


def x_format_bytes__mutmut_5(num_bytes: int) -> str:
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
    for unit in ["B", "XXKBXX", "MB", "GB", "TB", "PB"]:
        if num_bytes_float < 1024.0 or unit == "PB":
            return f"{num_bytes_float:.2f} {unit}"
        num_bytes_float /= 1024.0
    return f"{num_bytes_float:.2f} PB"


def x_format_bytes__mutmut_6(num_bytes: int) -> str:
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
    for unit in ["B", "kb", "MB", "GB", "TB", "PB"]:
        if num_bytes_float < 1024.0 or unit == "PB":
            return f"{num_bytes_float:.2f} {unit}"
        num_bytes_float /= 1024.0
    return f"{num_bytes_float:.2f} PB"


def x_format_bytes__mutmut_7(num_bytes: int) -> str:
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
    for unit in ["B", "KB", "XXMBXX", "GB", "TB", "PB"]:
        if num_bytes_float < 1024.0 or unit == "PB":
            return f"{num_bytes_float:.2f} {unit}"
        num_bytes_float /= 1024.0
    return f"{num_bytes_float:.2f} PB"


def x_format_bytes__mutmut_8(num_bytes: int) -> str:
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
    for unit in ["B", "KB", "mb", "GB", "TB", "PB"]:
        if num_bytes_float < 1024.0 or unit == "PB":
            return f"{num_bytes_float:.2f} {unit}"
        num_bytes_float /= 1024.0
    return f"{num_bytes_float:.2f} PB"


def x_format_bytes__mutmut_9(num_bytes: int) -> str:
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
    for unit in ["B", "KB", "MB", "XXGBXX", "TB", "PB"]:
        if num_bytes_float < 1024.0 or unit == "PB":
            return f"{num_bytes_float:.2f} {unit}"
        num_bytes_float /= 1024.0
    return f"{num_bytes_float:.2f} PB"


def x_format_bytes__mutmut_10(num_bytes: int) -> str:
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
    for unit in ["B", "KB", "MB", "gb", "TB", "PB"]:
        if num_bytes_float < 1024.0 or unit == "PB":
            return f"{num_bytes_float:.2f} {unit}"
        num_bytes_float /= 1024.0
    return f"{num_bytes_float:.2f} PB"


def x_format_bytes__mutmut_11(num_bytes: int) -> str:
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
    for unit in ["B", "KB", "MB", "GB", "XXTBXX", "PB"]:
        if num_bytes_float < 1024.0 or unit == "PB":
            return f"{num_bytes_float:.2f} {unit}"
        num_bytes_float /= 1024.0
    return f"{num_bytes_float:.2f} PB"


def x_format_bytes__mutmut_12(num_bytes: int) -> str:
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
    for unit in ["B", "KB", "MB", "GB", "tb", "PB"]:
        if num_bytes_float < 1024.0 or unit == "PB":
            return f"{num_bytes_float:.2f} {unit}"
        num_bytes_float /= 1024.0
    return f"{num_bytes_float:.2f} PB"


def x_format_bytes__mutmut_13(num_bytes: int) -> str:
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
    for unit in ["B", "KB", "MB", "GB", "TB", "XXPBXX"]:
        if num_bytes_float < 1024.0 or unit == "PB":
            return f"{num_bytes_float:.2f} {unit}"
        num_bytes_float /= 1024.0
    return f"{num_bytes_float:.2f} PB"


def x_format_bytes__mutmut_14(num_bytes: int) -> str:
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
    for unit in ["B", "KB", "MB", "GB", "TB", "pb"]:
        if num_bytes_float < 1024.0 or unit == "PB":
            return f"{num_bytes_float:.2f} {unit}"
        num_bytes_float /= 1024.0
    return f"{num_bytes_float:.2f} PB"


def x_format_bytes__mutmut_15(num_bytes: int) -> str:
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
        if num_bytes_float < 1024.0 and unit == "PB":
            return f"{num_bytes_float:.2f} {unit}"
        num_bytes_float /= 1024.0
    return f"{num_bytes_float:.2f} PB"


def x_format_bytes__mutmut_16(num_bytes: int) -> str:
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
        if num_bytes_float <= 1024.0 or unit == "PB":
            return f"{num_bytes_float:.2f} {unit}"
        num_bytes_float /= 1024.0
    return f"{num_bytes_float:.2f} PB"


def x_format_bytes__mutmut_17(num_bytes: int) -> str:
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
        if num_bytes_float < 1025.0 or unit == "PB":
            return f"{num_bytes_float:.2f} {unit}"
        num_bytes_float /= 1024.0
    return f"{num_bytes_float:.2f} PB"


def x_format_bytes__mutmut_18(num_bytes: int) -> str:
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
        if num_bytes_float < 1024.0 or unit != "PB":
            return f"{num_bytes_float:.2f} {unit}"
        num_bytes_float /= 1024.0
    return f"{num_bytes_float:.2f} PB"


def x_format_bytes__mutmut_19(num_bytes: int) -> str:
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
        if num_bytes_float < 1024.0 or unit == "XXPBXX":
            return f"{num_bytes_float:.2f} {unit}"
        num_bytes_float /= 1024.0
    return f"{num_bytes_float:.2f} PB"


def x_format_bytes__mutmut_20(num_bytes: int) -> str:
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
        if num_bytes_float < 1024.0 or unit == "pb":
            return f"{num_bytes_float:.2f} {unit}"
        num_bytes_float /= 1024.0
    return f"{num_bytes_float:.2f} PB"


def x_format_bytes__mutmut_21(num_bytes: int) -> str:
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
        num_bytes_float = 1024.0
    return f"{num_bytes_float:.2f} PB"


def x_format_bytes__mutmut_22(num_bytes: int) -> str:
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
        num_bytes_float *= 1024.0
    return f"{num_bytes_float:.2f} PB"


def x_format_bytes__mutmut_23(num_bytes: int) -> str:
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
        num_bytes_float /= 1025.0
    return f"{num_bytes_float:.2f} PB"

x_format_bytes__mutmut_mutants : ClassVar[MutantDict] = {
'x_format_bytes__mutmut_1': x_format_bytes__mutmut_1, 
    'x_format_bytes__mutmut_2': x_format_bytes__mutmut_2, 
    'x_format_bytes__mutmut_3': x_format_bytes__mutmut_3, 
    'x_format_bytes__mutmut_4': x_format_bytes__mutmut_4, 
    'x_format_bytes__mutmut_5': x_format_bytes__mutmut_5, 
    'x_format_bytes__mutmut_6': x_format_bytes__mutmut_6, 
    'x_format_bytes__mutmut_7': x_format_bytes__mutmut_7, 
    'x_format_bytes__mutmut_8': x_format_bytes__mutmut_8, 
    'x_format_bytes__mutmut_9': x_format_bytes__mutmut_9, 
    'x_format_bytes__mutmut_10': x_format_bytes__mutmut_10, 
    'x_format_bytes__mutmut_11': x_format_bytes__mutmut_11, 
    'x_format_bytes__mutmut_12': x_format_bytes__mutmut_12, 
    'x_format_bytes__mutmut_13': x_format_bytes__mutmut_13, 
    'x_format_bytes__mutmut_14': x_format_bytes__mutmut_14, 
    'x_format_bytes__mutmut_15': x_format_bytes__mutmut_15, 
    'x_format_bytes__mutmut_16': x_format_bytes__mutmut_16, 
    'x_format_bytes__mutmut_17': x_format_bytes__mutmut_17, 
    'x_format_bytes__mutmut_18': x_format_bytes__mutmut_18, 
    'x_format_bytes__mutmut_19': x_format_bytes__mutmut_19, 
    'x_format_bytes__mutmut_20': x_format_bytes__mutmut_20, 
    'x_format_bytes__mutmut_21': x_format_bytes__mutmut_21, 
    'x_format_bytes__mutmut_22': x_format_bytes__mutmut_22, 
    'x_format_bytes__mutmut_23': x_format_bytes__mutmut_23
}

def format_bytes(*args, **kwargs):
    result = _mutmut_trampoline(x_format_bytes__mutmut_orig, x_format_bytes__mutmut_mutants, args, kwargs)
    return result 

format_bytes.__signature__ = _mutmut_signature(x_format_bytes__mutmut_orig)
x_format_bytes__mutmut_orig.__name__ = 'x_format_bytes'


__all__ = [
    "check_disk_space",
    "format_bytes",
    "get_available_space",
    "get_disk_usage",
]


# <3 🧱🤝📄🪄
