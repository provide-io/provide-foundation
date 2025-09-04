"""Atomic and safe file operations utilities.

This module provides atomic file operations to ensure data integrity
during file writes and replacements.
"""

import os
import tempfile
from pathlib import Path

from provide.foundation import logger


def atomic_write(
    path: Path | str,
    data: bytes,
    mode: int | None = None,
) -> None:
    """Write file atomically using temporary file and rename.
    
    Args:
        path: Target file path
        data: Binary data to write
        mode: Optional file permissions (e.g., 0o644)
        
    Raises:
        OSError: If file operation fails
    """
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    
    # Create temp file in same directory for atomic rename
    fd, temp_path = tempfile.mkstemp(
        dir=path.parent,
        prefix=f".{path.name}.",
        suffix=".tmp"
    )
    
    try:
        with os.fdopen(fd, "wb") as f:
            f.write(data)
            f.flush()
            os.fsync(f.fileno())
        
        # Set permissions if specified
        if mode is not None:
            os.chmod(temp_path, mode)
        
        # Atomic rename
        os.replace(temp_path, path)
        
        logger.debug(
            "Atomically wrote file",
            path=str(path),
            size=len(data),
            mode=oct(mode) if mode else None
        )
    except Exception:
        # Clean up temp file on error
        try:
            os.unlink(temp_path)
        except OSError:
            pass
        raise


def atomic_write_text(
    path: Path | str,
    text: str,
    encoding: str = "utf-8",
    mode: int | None = None,
) -> None:
    """Write text file atomically.
    
    Args:
        path: Target file path
        text: Text content to write
        encoding: Text encoding (default: utf-8)
        mode: Optional file permissions
        
    Raises:
        OSError: If file operation fails
        UnicodeEncodeError: If text cannot be encoded
    """
    data = text.encode(encoding)
    atomic_write(path, data, mode)


def atomic_replace(
    path: Path | str,
    data: bytes,
    backup: bool = False,
) -> None:
    """Replace existing file atomically.
    
    Args:
        path: Target file path (must exist)
        data: Binary data to write
        backup: Whether to create backup of original
        
    Raises:
        FileNotFoundError: If target file doesn't exist
        OSError: If file operation fails
    """
    path = Path(path)
    
    if not path.exists():
        raise FileNotFoundError(f"File to replace not found: {path}")
    
    # Create backup if requested
    if backup:
        backup_path = path.with_suffix(path.suffix + ".bak")
        try:
            os.replace(path, backup_path)
            logger.debug("Created backup", original=str(path), backup=str(backup_path))
        except Exception:
            logger.warning("Failed to create backup", path=str(path))
    
    # Get original file permissions
    original_mode = path.stat().st_mode & 0o777
    
    # Write atomically with original permissions
    atomic_write(path, data, mode=original_mode)


def safe_unlink(path: Path | str) -> bool:
    """Safely delete file, returning success status.
    
    Args:
        path: File path to delete
        
    Returns:
        True if file was deleted, False if it didn't exist
    """
    path = Path(path)
    
    try:
        path.unlink()
        logger.debug("Deleted file", path=str(path))
        return True
    except FileNotFoundError:
        logger.debug("File already absent", path=str(path))
        return False
    except Exception as e:
        logger.error(
            "Failed to delete file",
            path=str(path),
            error=str(e)
        )
        raise


def ensure_directory(
    path: Path | str,
    mode: int | None = None,
) -> Path:
    """Ensure directory exists with proper permissions.
    
    Args:
        path: Directory path to create
        mode: Optional directory permissions
        
    Returns:
        Path object for the directory
        
    Raises:
        OSError: If directory creation fails
    """
    path = Path(path)
    
    if path.exists():
        if not path.is_dir():
            raise NotADirectoryError(f"Path exists but is not a directory: {path}")
        return path
    
    path.mkdir(parents=True, exist_ok=True)
    
    if mode is not None:
        os.chmod(path, mode)
    
    logger.debug(
        "Ensured directory exists",
        path=str(path),
        mode=oct(mode) if mode else None
    )
    
    return path


def read_file_safely(
    path: Path | str,
    default: bytes | None = None,
) -> bytes | None:
    """Read file safely, returning default if not found.
    
    Args:
        path: File path to read
        default: Default value if file doesn't exist
        
    Returns:
        File contents or default value
        
    Raises:
        OSError: If file exists but cannot be read
    """
    path = Path(path)
    
    try:
        return path.read_bytes()
    except FileNotFoundError:
        logger.debug("File not found, using default", path=str(path))
        return default
    except Exception as e:
        logger.error("Failed to read file", path=str(path), error=str(e))
        raise


def read_text_safely(
    path: Path | str,
    default: str | None = None,
    encoding: str = "utf-8",
) -> str | None:
    """Read text file safely, returning default if not found.
    
    Args:
        path: File path to read
        default: Default value if file doesn't exist
        encoding: Text encoding
        
    Returns:
        File contents or default value
        
    Raises:
        OSError: If file exists but cannot be read
        UnicodeDecodeError: If file cannot be decoded
    """
    data = read_file_safely(path, None)
    if data is None:
        return default
    return data.decode(encoding)


__all__ = [
    "atomic_write",
    "atomic_write_text",
    "atomic_replace",
    "safe_unlink",
    "ensure_directory",
    "read_file_safely",
    "read_text_safely",
]