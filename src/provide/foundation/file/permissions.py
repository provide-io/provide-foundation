#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""File permission utilities for Unix-like systems.

Provides safe, cross-platform utilities for working with file permissions including
parsing, formatting, and applying permission modes."""

from __future__ import annotations

from pathlib import Path

from provide.foundation.logger import get_logger

log = get_logger(__name__)

# Default permission constants
DEFAULT_FILE_PERMS = 0o644  # rw-r--r--
DEFAULT_DIR_PERMS = 0o755  # rwxr-xr-x
DEFAULT_EXECUTABLE_PERMS = 0o755  # rwxr-xr-x


def parse_permissions(perms_str: str | None, default: int = DEFAULT_FILE_PERMS) -> int:
    """Parse permission string to octal integer.

    Accepts various permission string formats:
    - Octal with prefix: "0o755", "0755"
    - Octal without prefix: "755"
    - Integer strings: "493" (decimal for 0o755)

    Args:
        perms_str: Permission string (e.g., "0755", "755", "0o755")
        default: Default permissions if parsing fails

    Returns:
        Permission as integer (e.g., 0o755 = 493)

    Examples:
        >>> parse_permissions("0755")
        493
        >>> parse_permissions("0o755")
        493
        >>> parse_permissions("755")
        493
        >>> parse_permissions(None)
        420
        >>> parse_permissions("invalid")
        420
    """
    if not perms_str:
        return default

    try:
        # Remove leading '0o' or '0' prefix if present
        cleaned = perms_str.strip()
        if cleaned.startswith("0o"):
            cleaned = cleaned[2:]
        elif cleaned.startswith("0") and len(cleaned) > 1:
            cleaned = cleaned[1:]

        # Try parsing as octal
        return int(cleaned, 8)
    except (ValueError, TypeError):
        log.warning(
            "Invalid permission string, using default",
            perms_str=perms_str,
            default=oct(default),
        )
        return default


def format_permissions(mode: int) -> str:
    """Format permission bits as octal string.

    Args:
        mode: Permission bits (can include file type bits)

    Returns:
        Formatted string like "0755" (last 3 octal digits only)

    Examples:
        >>> format_permissions(0o755)
        '0755'
        >>> format_permissions(0o644)
        '0644'
        >>> format_permissions(493)  # 0o755 in decimal
        '0755'
    """
    # Mask to only permission bits (last 9 bits = 3 octal digits)
    perms_only = mode & 0o777
    return f"0{perms_only:03o}"


def set_file_permissions(path: Path, mode: int) -> None:
    """Set file permissions safely with error handling.

    Args:
        path: File or directory path
        mode: Unix permission mode (e.g., 0o755)

    Raises:
        OSError: If setting permissions fails on the underlying filesystem

    Examples:
        >>> from pathlib import Path
        >>> p = Path("/tmp/test.txt")
        >>> p.touch()
        >>> set_file_permissions(p, 0o644)
    """
    try:
        Path(path).chmod(mode)
        log.trace(
            "Set file permissions",
            path=str(path),
            mode=format_permissions(mode),
        )
    except OSError as e:
        log.warning(
            "Could not set permissions",
            path=str(path),
            mode=format_permissions(mode),
            error=str(e),
        )
        raise


def get_permissions(path: Path) -> int:
    """Get current file permissions.

    Args:
        path: File or directory path

    Returns:
        Permission bits as integer (0 if file doesn't exist or error)

    Examples:
        >>> from pathlib import Path
        >>> p = Path("/tmp/test.txt")
        >>> p.touch()
        >>> p.chmod(0o644)
        >>> get_permissions(p)
        420
        >>> format_permissions(get_permissions(p))
        '0644'
    """
    try:
        return path.stat().st_mode & 0o777
    except OSError as e:
        log.debug(
            "Could not read permissions",
            path=str(path),
            error=str(e),
        )
        return 0


def ensure_secure_permissions(
    path: Path,
    is_executable: bool = False,
    file_mode: int = DEFAULT_FILE_PERMS,
    dir_mode: int = DEFAULT_DIR_PERMS,
    executable_mode: int = DEFAULT_EXECUTABLE_PERMS,
) -> None:
    """Apply secure default permissions to a file or directory.

    Automatically determines the appropriate permission mode based on whether
    the path is a file, directory, or executable.

    Args:
        path: Path to file or directory
        is_executable: Whether file should be executable (ignored for directories)
        file_mode: Permission mode for regular files
        dir_mode: Permission mode for directories
        executable_mode: Permission mode for executable files

    Examples:
        >>> from pathlib import Path
        >>> # Regular file gets 0o644
        >>> p = Path("/tmp/file.txt")
        >>> p.touch()
        >>> ensure_secure_permissions(p)

        >>> # Executable gets 0o755
        >>> p2 = Path("/tmp/script.sh")
        >>> p2.touch()
        >>> ensure_secure_permissions(p2, is_executable=True)

        >>> # Directory gets 0o755
        >>> d = Path("/tmp/mydir")
        >>> d.mkdir(exist_ok=True)
        >>> ensure_secure_permissions(d)
    """
    if path.is_dir():
        mode = dir_mode
    elif is_executable:
        mode = executable_mode
    else:
        mode = file_mode

    set_file_permissions(path, mode)
    log.trace(
        "Applied secure permissions",
        path=str(path),
        mode=format_permissions(mode),
        is_dir=path.is_dir(),
        is_executable=is_executable,
    )


__all__ = [
    "DEFAULT_DIR_PERMS",
    "DEFAULT_EXECUTABLE_PERMS",
    "DEFAULT_FILE_PERMS",
    "ensure_secure_permissions",
    "format_permissions",
    "get_permissions",
    "parse_permissions",
    "set_file_permissions",
]

# 🧱🏗️🔚
