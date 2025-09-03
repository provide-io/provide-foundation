"""Atomic file operations using temp file + rename pattern."""

import contextlib
import os
from pathlib import Path
import tempfile

from provide.foundation.logger import get_logger

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

    # Create temp file in same directory for atomic rename
    # Note: mkstemp creates files with 0o600 by default for security
    fd, temp_path = tempfile.mkstemp(
        dir=path.parent, prefix=f".{path.name}.", suffix=".tmp"
    )

    try:
        with os.fdopen(fd, "wb") as f:
            f.write(data)
            f.flush()
            os.fsync(f.fileno())

        # Set permissions if specified
        if mode is not None:
            os.chmod(temp_path, mode)
        elif preserve_mode and path.exists():
            # Preserve existing permissions if requested
            try:
                existing_mode = path.stat().st_mode
                os.chmod(temp_path, existing_mode)
            except OSError:
                pass
        elif not preserve_mode:
            # When not preserving, set to standard default permissions
            # mkstemp creates with 0o600, but we want standard defaults
            # Apply umask manually since os.chmod doesn't respect it
            default_mode = 0o666
            current_umask = os.umask(0)  # Get current umask
            os.umask(current_umask)  # Restore it
            os.chmod(temp_path, default_mode & ~current_umask)

        # Atomic rename
        os.replace(temp_path, path)

        log.debug(
            "Atomically wrote file",
            path=str(path),
            size=len(data),
            mode=oct(mode) if mode else None,
        )
    except Exception:
        # Clean up temp file on error
        with contextlib.suppress(OSError):
            os.unlink(temp_path)
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
