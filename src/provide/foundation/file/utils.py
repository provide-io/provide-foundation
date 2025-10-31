#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
import shutil

from provide.foundation.logger import get_logger

"""File utility functions."""

log = get_logger(__name__)


def get_size(path: Path | str) -> int:
    """Get file size in bytes, 0 if not exists.

    Args:
        path: File path

    Returns:
        Size in bytes, or 0 if file doesn't exist

    """
    path = Path(path)

    try:
        return path.stat().st_size
    except FileNotFoundError:
        return 0
    except Exception as e:
        log.warning("Failed to get file size", path=str(path), error=str(e))
        return 0


def get_mtime(path: Path | str) -> float | None:
    """Get modification time, None if not exists.

    Args:
        path: File path

    Returns:
        Modification time as timestamp, or None if doesn't exist

    """
    path = Path(path)

    try:
        return path.stat().st_mtime
    except FileNotFoundError:
        return None
    except Exception as e:
        log.warning("Failed to get modification time", path=str(path), error=str(e))
        return None


def touch(
    path: Path | str,
    mode: int = 0o644,
    exist_ok: bool = True,
) -> None:
    """Create empty file or update timestamp.

    Args:
        path: File path
        mode: File permissions for new files
        exist_ok: If False, raise error if file exists

    Raises:
        FileExistsError: If exist_ok=False and file exists

    """
    path = Path(path)

    if path.exists() and not exist_ok:
        raise FileExistsError(f"File already exists: {path}")

    # Ensure parent directory exists
    path.parent.mkdir(parents=True, exist_ok=True)

    # Touch the file
    path.touch(mode=mode, exist_ok=exist_ok)
    log.debug("Touched file", path=str(path))


def find_files(
    pattern: str,
    root: Path | str = ".",
    recursive: bool = True,
) -> list[Path]:
    """Find files matching pattern.

    Args:
        pattern: Glob pattern (e.g., "*.py", "**/*.json")
        root: Root directory to search from
        recursive: If True, search recursively

    Returns:
        List of matching file paths

    """
    root = Path(root)

    if not root.exists():
        log.warning("Search root doesn't exist", root=str(root))
        return []

    # Use glob or rglob based on recursive flag
    if recursive and "**" not in pattern:
        pattern = f"**/{pattern}"

    try:
        matches = list(root.glob(pattern)) if recursive else list(root.glob(pattern.lstrip("/")))

        # Filter to files only
        files = [p for p in matches if p.is_file()]

        log.debug("Found files", pattern=pattern, root=str(root), count=len(files))
        return files
    except Exception as e:
        log.error("Failed to find files", pattern=pattern, root=str(root), error=str(e))
        return []


def backup_file(
    path: Path | str,
    suffix: str = ".bak",
    timestamp: bool = False,
) -> Path | None:
    """Create backup copy of file.

    Args:
        path: File to backup
        suffix: Backup suffix
        timestamp: If True, add timestamp to backup name

    Returns:
        Path to backup file, or None if source doesn't exist

    """
    path = Path(path)

    if not path.exists():
        log.debug("Source file doesn't exist, no backup created", path=str(path))
        return None

    # Build backup filename
    if timestamp:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = path.with_suffix(f".{ts}{suffix}")
    else:
        backup_path = path.with_suffix(path.suffix + suffix)

        # Find unique name if backup already exists
        counter = 1
        while backup_path.exists():
            backup_path = path.with_suffix(f"{path.suffix}{suffix}.{counter}")
            counter += 1

    try:
        shutil.copy2(str(path), str(backup_path))
        log.debug("Created backup", source=str(path), backup=str(backup_path))
        return backup_path
    except Exception as e:
        log.error("Failed to create backup", path=str(path), error=str(e))
        return None


__all__ = [
    "backup_file",
    "find_files",
    "get_mtime",
    "get_size",
    "touch",
]

# 🧱🏗️🔚
