#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from __future__ import annotations

from collections.abc import Generator
import contextlib
from contextlib import contextmanager
from pathlib import Path
import shutil
import tempfile

from provide.foundation.config.defaults import (
    DEFAULT_TEMP_CLEANUP,
    DEFAULT_TEMP_PREFIX,
    DEFAULT_TEMP_SUFFIX,
    DEFAULT_TEMP_TEXT_MODE,
)
from provide.foundation.errors.handlers import error_boundary
from provide.foundation.file.safe import safe_delete
from provide.foundation.logger import get_logger

"""Temporary file and directory utilities."""

log = get_logger(__name__)


def system_temp_dir() -> Path:
    """Get the operating system's temporary directory.

    Returns:
        Path to the OS temp directory

    Example:
        >>> temp_path = system_temp_dir()
        >>> print(temp_path)  # e.g., /tmp or C:\\Users\\...\\Temp

    """
    return Path(tempfile.gettempdir())


def secure_temp_file(
    suffix: str = DEFAULT_TEMP_SUFFIX,
    prefix: str = DEFAULT_TEMP_PREFIX,
    dir: Path | str | None = None,
) -> tuple[int, Path]:
    """Create a secure temporary file with restricted permissions.

    This is similar to tempfile.mkstemp but uses Foundation's defaults.
    The file is created with permissions 0o600 (owner read/write only).

    Use this when you need:
    - Direct file descriptor access (for os.fdopen, os.fsync, etc.)
    - Atomic file operations
    - Maximum security (restricted permissions)

    Args:
        suffix: File suffix
        prefix: File name prefix
        dir: Directory for the temp file (None = system temp)

    Returns:
        Tuple of (file_descriptor, Path) - caller must close the fd

    Example:
        >>> fd, path = secure_temp_file(suffix='.tmp')
        >>> try:
        ...     with os.fdopen(fd, 'wb') as f:
        ...         f.write(b'data')
        ...         os.fsync(f.fileno())
        ... finally:
        ...     path.unlink(missing_ok=True)

    """
    if dir and isinstance(dir, Path):
        dir = str(dir)

    fd, temp_path = tempfile.mkstemp(suffix=suffix, prefix=prefix, dir=dir)
    return fd, Path(temp_path)


@contextmanager
def temp_file(
    suffix: str = DEFAULT_TEMP_SUFFIX,
    prefix: str = DEFAULT_TEMP_PREFIX,
    dir: Path | str | None = None,
    text: bool = DEFAULT_TEMP_TEXT_MODE,
    cleanup: bool = DEFAULT_TEMP_CLEANUP,
) -> Generator[Path, None, None]:
    """Create a temporary file with automatic cleanup.

    Args:
        suffix: File suffix (e.g., '.txt', '.json')
        prefix: File name prefix
        dir: Directory for the temp file (None = system temp)
        text: Whether to open in text mode
        cleanup: Whether to remove file on exit

    Yields:
        Path object for the temporary file

    Example:
        >>> with temp_file(suffix='.json') as tmp:
        ...     tmp.write_text('{"key": "value"}')
        ...     process_file(tmp)

    """
    temp_path = None
    try:
        if dir and isinstance(dir, Path):
            dir = str(dir)

        # Create temp file and immediately close it
        with tempfile.NamedTemporaryFile(
            suffix=suffix,
            prefix=prefix,
            dir=dir,
            delete=False,
            mode="w" if text else "wb",
        ) as f:
            temp_path = Path(f.name)

        log.debug("Created temp file", path=str(temp_path))
        yield temp_path

    finally:
        if cleanup and temp_path and temp_path.exists():
            with error_boundary(Exception, reraise=False):
                safe_delete(temp_path, missing_ok=True)
                # Safe logging - catch ValueError/OSError for closed file streams during test teardown
                with contextlib.suppress(ValueError, OSError):
                    log.debug("Cleaned up temp file", path=str(temp_path))


@contextmanager
def temp_dir(
    prefix: str = DEFAULT_TEMP_PREFIX,
    cleanup: bool = DEFAULT_TEMP_CLEANUP,
) -> Generator[Path, None, None]:
    """Create temporary directory with automatic cleanup.

    Args:
        prefix: Directory name prefix
        cleanup: Whether to remove directory on exit

    Yields:
        Path object for the temporary directory

    Example:
        >>> with temp_dir() as tmpdir:
        ...     (tmpdir / 'data.txt').write_text('content')
        ...     process_directory(tmpdir)

    """
    temp_path = None
    try:
        temp_path = Path(tempfile.mkdtemp(prefix=prefix))
        log.debug("Created temp directory", path=str(temp_path))
        yield temp_path
    finally:
        if cleanup and temp_path and temp_path.exists():
            with error_boundary(Exception, reraise=False):
                shutil.rmtree(temp_path)
                # Safe logging - catch ValueError/OSError for closed file streams during test teardown
                with contextlib.suppress(ValueError, OSError):
                    log.debug("Cleaned up temp directory", path=str(temp_path))


# 🧱🏗️🔚
