"""Directory operations and utilities."""

from contextlib import contextmanager
from typing import Generator
from pathlib import Path
import shutil
import tempfile

from provide.foundation.errors.decorators import with_error_handling
from provide.foundation.errors.handlers import error_boundary
from provide.foundation.logger import get_logger

log = get_logger(__name__)


def ensure_dir(
    path: Path | str,
    mode: int = 0o755,
    parents: bool = True,
) -> Path:
    """Ensure directory exists with proper permissions.

    Args:
        path: Directory path
        mode: Directory permissions
        parents: Create parent directories if needed

    Returns:
        Path object for the directory
    """
    path = Path(path)

    if not path.exists():
        path.mkdir(mode=mode, parents=parents, exist_ok=True)
        log.debug("Created directory", path=str(path), mode=oct(mode))
    elif not path.is_dir():
        raise NotADirectoryError(f"Path exists but is not a directory: {path}")

    return path


def ensure_parent_dir(
    file_path: Path | str,
    mode: int = 0o755,
) -> Path:
    """Ensure parent directory of file exists.

    Args:
        file_path: File path whose parent to ensure
        mode: Directory permissions

    Returns:
        Path object for the parent directory
    """
    file_path = Path(file_path)
    parent = file_path.parent

    if parent and parent != Path():
        return ensure_dir(parent, mode=mode, parents=True)

    return parent


@contextmanager
def temp_dir(
    prefix: str = "provide_",
    cleanup: bool = True,
) -> Generator[Path, None, None]:
    """Create temporary directory with automatic cleanup.

    Args:
        prefix: Directory name prefix
        cleanup: Whether to remove directory on exit

    Yields:
        Path object for the temporary directory
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
                log.debug("Cleaned up temp directory", path=str(temp_path))


@with_error_handling(fallback=False, suppress=(FileNotFoundError,) if False else ())
def safe_rmtree(
    path: Path | str,
    missing_ok: bool = True,
) -> bool:
    """Remove directory tree safely.

    Args:
        path: Directory to remove
        missing_ok: If True, don't raise error if doesn't exist

    Returns:
        True if removed, False if didn't exist

    Raises:
        OSError: If removal fails and directory exists
    """
    path = Path(path)

    if path.exists():
        shutil.rmtree(path)
        log.debug("Removed directory tree", path=str(path))
        return True
    elif missing_ok:
        log.debug("Directory already absent", path=str(path))
        return False
    else:
        raise FileNotFoundError(f"Directory does not exist: {path}")


__all__ = [
    "ensure_dir",
    "ensure_parent_dir",
    "safe_rmtree",
    "temp_dir",
]
