#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from __future__ import annotations

from pathlib import Path
import shutil

"""Safe file operations with error handling and defaults."""

_logger = None


def safe_read(
    path: Path | str,
    default: bytes | None = None,
    encoding: str | None = None,
) -> bytes | str | None:
    """Read file safely, returning default if not found.

    Args:
        path: File to read
        default: Value to return if file doesn't exist
        encoding: If provided, decode bytes to str

    Returns:
        File contents or default value

    """
    path = Path(path)

    try:
        data = path.read_bytes()
        if encoding:
            return data.decode(encoding)
        return data
    except FileNotFoundError:
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().debug("File not found, returning default", path=str(path))
        if default is not None and encoding:
            return default.decode(encoding) if isinstance(default, bytes) else default
        return default
    except Exception as e:
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().warning("Failed to read file", path=str(path), error=str(e))
        return default


def safe_read_text(
    path: Path | str,
    default: str = "",
    encoding: str = "utf-8",
) -> str:
    """Read text file safely with default.

    Args:
        path: File to read
        default: Default text if file doesn't exist
        encoding: Text encoding

    Returns:
        File contents or default text

    """
    result = safe_read(path, default=default.encode(encoding), encoding=encoding)
    return result if isinstance(result, str) else default


def safe_delete(
    path: Path | str,
    missing_ok: bool = True,
) -> bool:
    """Delete file safely.

    Args:
        path: File to delete
        missing_ok: If True, don't raise error if file doesn't exist

    Returns:
        True if deleted, False if didn't exist

    Raises:
        OSError: If deletion fails and file exists

    """
    path = Path(path)

    try:
        path.unlink()
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().debug("Deleted file", path=str(path))
        return True
    except FileNotFoundError:
        if missing_ok:
            from provide.foundation.hub.foundation import get_foundation_logger

            get_foundation_logger().debug("File already absent", path=str(path))
            return False
        raise
    except Exception as e:
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().error("Failed to delete file", path=str(path), error=str(e))
        raise


def safe_move(
    src: Path | str,
    dst: Path | str,
    overwrite: bool = False,
) -> None:
    """Move file safely with optional overwrite.

    Args:
        src: Source file path
        dst: Destination file path
        overwrite: Whether to overwrite existing destination

    Raises:
        FileNotFoundError: If source doesn't exist
        FileExistsError: If destination exists and overwrite=False
        OSError: If move operation fails

    """
    src = Path(src)
    dst = Path(dst)

    if not src.exists():
        raise FileNotFoundError(f"Source file does not exist: {src}")

    if dst.exists() and not overwrite:
        raise FileExistsError(f"Destination already exists: {dst}")

    # Ensure destination directory exists
    dst.parent.mkdir(parents=True, exist_ok=True)

    try:
        shutil.move(str(src), str(dst))
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().debug("Moved file", src=str(src), dst=str(dst))
    except Exception as e:
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().error("Failed to move file", src=str(src), dst=str(dst), error=str(e))
        raise


def safe_copy(
    src: Path | str,
    dst: Path | str,
    overwrite: bool = False,
    preserve_mode: bool = True,
) -> None:
    """Copy file safely with metadata preservation.

    Args:
        src: Source file path
        dst: Destination file path
        overwrite: Whether to overwrite existing destination
        preserve_mode: Whether to preserve file permissions

    Raises:
        FileNotFoundError: If source doesn't exist
        FileExistsError: If destination exists and overwrite=False
        OSError: If copy operation fails

    """
    src = Path(src)
    dst = Path(dst)

    if not src.exists():
        raise FileNotFoundError(f"Source file does not exist: {src}")

    if dst.exists() and not overwrite:
        raise FileExistsError(f"Destination already exists: {dst}")

    # Ensure destination directory exists
    dst.parent.mkdir(parents=True, exist_ok=True)

    try:
        if preserve_mode:
            shutil.copy2(str(src), str(dst))
        else:
            shutil.copy(str(src), str(dst))
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().debug("Copied file", src=str(src), dst=str(dst))
    except Exception as e:
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().error("Failed to copy file", src=str(src), dst=str(dst), error=str(e))
        raise


__all__ = [
    "safe_copy",
    "safe_delete",
    "safe_move",
    "safe_read",
    "safe_read_text",
]

# 🧱🏗️🔚
