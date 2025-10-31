#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from __future__ import annotations

import contextlib
import os
from pathlib import Path
import sys

from provide.foundation.logger import get_logger

"""Atomic file operations using temp file + rename pattern."""

log = get_logger(__name__)


def atomic_write(
    path: Path | str,
    data: bytes,
    mode: int | None = None,
    backup: bool = False,
    preserve_mode: bool = True,
) -> None:
    """Write file atomically using temp file + rename.

    This ensures that the file is either fully written or not written at all,
    preventing partial writes or corruption.

    Args:
        path: Target file path
        data: Binary data to write
        mode: Optional file permissions (e.g., 0o644)
        backup: Create .bak file before overwrite
        preserve_mode: Whether to preserve existing file permissions when mode is None

    Raises:
        OSError: If file operation fails

    """
    path = Path(path)

    # Create backup if requested and file exists
    if backup and path.exists():
        backup_path = path.with_suffix(path.suffix + ".bak")
        try:
            path.rename(backup_path)
            log.debug("Created backup", backup=str(backup_path))
        except OSError as e:
            log.warning("Failed to create backup", error=str(e))

    # Ensure parent directory exists
    path.parent.mkdir(parents=True, exist_ok=True)

    # Determine final permissions before creating file (avoid race condition)
    final_mode = None
    if mode is not None:
        final_mode = mode
    elif preserve_mode and path.exists():
        # Get existing permissions
        with contextlib.suppress(OSError):
            final_mode = path.stat().st_mode

    if final_mode is None:
        # Default permissions (respecting umask on Unix, simplified on Windows)
        default_mode = 0o666
        if sys.platform == "win32":
            # Windows doesn't support umask; use default mode
            final_mode = default_mode
        else:
            # Unix: Respect umask
            current_umask = os.umask(0)
            os.umask(current_umask)
            final_mode = default_mode & ~current_umask

    # Create temp file with final permissions in a single operation (no race)
    # Use os.open() instead of secure_temp_file for atomic permission setting
    import tempfile

    temp_fd, temp_path = tempfile.mkstemp(
        dir=path.parent,
        prefix=f".{path.name}.",
        suffix=".tmp",
    )

    try:
        # Set permissions immediately on the file descriptor (atomic)
        # On Windows, fchmod has limited effect (only read-only bit)
        if sys.platform != "win32":
            os.fchmod(temp_fd, final_mode)

        # Write data
        with os.fdopen(temp_fd, "wb") as f:
            f.write(data)
            f.flush()
            os.fsync(f.fileno())

        # Atomic rename
        Path(temp_path).replace(path)

        log.debug(
            "Atomically wrote file",
            path=str(path),
            size=len(data),
            mode=oct(mode) if mode else None,
        )
    except (OSError, PermissionError) as e:
        # Clean up temp file on error
        log.error(
            "Atomic write failed, cleaning up temp file",
            path=str(path),
            temp_path=temp_path,
            error=str(e),
        )
        with contextlib.suppress(OSError):
            Path(temp_path).unlink()
        raise


def atomic_write_text(
    path: Path | str,
    text: str,
    encoding: str = "utf-8",
    mode: int | None = None,
    backup: bool = False,
    preserve_mode: bool = True,
) -> None:
    """Write text file atomically.

    Args:
        path: Target file path
        text: Text content to write
        encoding: Text encoding (default: utf-8)
        mode: Optional file permissions
        backup: Create .bak file before overwrite
        preserve_mode: Whether to preserve existing file permissions when mode is None

    Raises:
        OSError: If file operation fails
        UnicodeEncodeError: If text cannot be encoded

    """
    data = text.encode(encoding)
    atomic_write(path, data, mode=mode, backup=backup, preserve_mode=preserve_mode)


def atomic_replace(
    path: Path | str,
    data: bytes,
    preserve_mode: bool = True,
) -> None:
    """Replace existing file atomically, preserving permissions.

    Args:
        path: Target file path (must exist)
        data: Binary data to write
        preserve_mode: Whether to preserve file permissions

    Raises:
        FileNotFoundError: If file doesn't exist
        OSError: If file operation fails

    """
    path = Path(path)

    if not path.exists():
        raise FileNotFoundError(f"File does not exist: {path}")

    mode = None
    if preserve_mode:
        with contextlib.suppress(OSError):
            mode = path.stat().st_mode

    # When preserve_mode is False, we explicitly pass preserve_mode=False to atomic_write
    # and let it handle the non-preservation (atomic_write won't preserve even if file exists)
    atomic_write(path, data, mode=mode, backup=False, preserve_mode=preserve_mode)


__all__ = [
    "atomic_replace",
    "atomic_write",
    "atomic_write_text",
]

# 🧱🏗️🔚
