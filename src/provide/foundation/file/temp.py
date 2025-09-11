"""Temporary file and directory utilities."""

from collections.abc import Generator
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

log = get_logger(__name__)


def get_temp_dir() -> Path:
    """Get the system temporary directory.

    Returns:
        Path to the system temp directory

    Example:
        >>> temp_path = get_temp_dir()
        >>> print(temp_path)  # e.g., /tmp or C:\\Users\\...\\Temp
    """
    return Path(tempfile.gettempdir())


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
            suffix=suffix, prefix=prefix, dir=dir, delete=False, mode="w" if text else "wb"
        ) as f:
            temp_path = Path(f.name)

        log.debug("Created temp file", path=str(temp_path))
        yield temp_path

    finally:
        if cleanup and temp_path and temp_path.exists():
            with error_boundary(Exception, reraise=False):
                safe_delete(temp_path, missing_ok=True)
                log.debug("Cleaned up temp file", path=str(temp_path))


def temp_file_with_content(
    content: bytes | str,
    suffix: str = DEFAULT_TEMP_SUFFIX,
    prefix: str = DEFAULT_TEMP_PREFIX,
    dir: Path | str | None = None,
    cleanup: bool = DEFAULT_TEMP_CLEANUP,
) -> Generator[Path, None, None]:
    """Create a temporary file with initial content.

    Args:
        content: Content to write to the file
        suffix: File suffix (e.g., '.txt', '.json')
        prefix: File name prefix
        dir: Directory for the temp file (None = system temp)
        cleanup: Whether to remove file on exit

    Yields:
        Path object for the temporary file with content

    Example:
        >>> with temp_file_with_content('{"key": "value"}', suffix='.json') as tmp:
        ...     data = json.loads(tmp.read_text())
        ...     process_data(data)
    """
    with temp_file(suffix=suffix, prefix=prefix, dir=dir, text=isinstance(content, str), cleanup=cleanup) as tmp:
        if isinstance(content, str):
            tmp.write_text(content)
        else:
            tmp.write_bytes(content)
        yield tmp


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
                log.debug("Cleaned up temp directory", path=str(temp_path))