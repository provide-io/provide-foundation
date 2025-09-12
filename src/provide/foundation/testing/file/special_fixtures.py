"""
Special file test fixtures.

Fixtures for creating specialized files like binary files, read-only files,
symbolic links, and executable files.
"""

from collections.abc import Generator
from pathlib import Path
import stat

import pytest

from provide.foundation.file import temp_file as foundation_temp_file
from provide.foundation.file.safe import safe_delete


@pytest.fixture
def binary_file() -> Generator[Path, None, None]:
    """
    Create a temporary binary file for testing.

    Yields:
        Path to a binary file containing sample binary data.
    """
    with foundation_temp_file(suffix=".bin", text=False, cleanup=False) as path:
        # Write some binary data
        path.write_bytes(b"\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09" +
                        b"\xff\xfe\xfd\xfc\xfb\xfa\xf9\xf8\xf7\xf6")

    yield path
    safe_delete(path, missing_ok=True)


@pytest.fixture
def readonly_file() -> Generator[Path, None, None]:
    """
    Create a read-only file for permission testing.

    Yields:
        Path to a read-only file.
    """
    with foundation_temp_file(suffix=".txt", text=True, cleanup=False) as path:
        path.write_text("Read-only content")

    # Make file read-only
    path.chmod(0o444)

    yield path

    # Restore write permission for cleanup
    path.chmod(0o644)
    safe_delete(path, missing_ok=True)


@pytest.fixture
def temp_symlink():
    """
    Create temporary symbolic links for testing.

    Returns:
        Function that creates symbolic links.
    """
    created_links = []

    def _make_symlink(target: Path | str, link_name: Path | str = None) -> Path:
        """
        Create a temporary symbolic link.

        Args:
            target: Target path for the symlink
            link_name: Optional link name (auto-generated if None)

        Returns:
            Path to created symlink
        """
        target = Path(target)

        if link_name is None:
            with foundation_temp_file(cleanup=True) as temp_path:
                link_name = Path(str(temp_path) + "_link")
        else:
            link_name = Path(link_name)

        link_name.symlink_to(target)
        created_links.append(link_name)

        return link_name

    yield _make_symlink

    # Cleanup
    for link in created_links:
        safe_delete(link, missing_ok=True)


@pytest.fixture
def temp_executable_file():
    """
    Create temporary executable files for testing.

    Returns:
        Function that creates executable files.
    """
    created_files = []

    def _make_executable(content: str = "#!/bin/sh\necho 'test'\n", suffix: str = ".sh") -> Path:
        """
        Create a temporary executable file.

        Args:
            content: Script content
            suffix: File suffix

        Returns:
            Path to created executable file
        """
        with foundation_temp_file(suffix=suffix, text=True, cleanup=False) as path:
            path.write_text(content)

        # Make executable
        current = path.stat().st_mode
        path.chmod(current | stat.S_IEXEC | stat.S_IXGRP | stat.S_IXOTH)

        created_files.append(path)
        return path

    yield _make_executable

    # Cleanup
    for path in created_files:
        safe_delete(path, missing_ok=True)


__all__ = [
    "binary_file",
    "readonly_file",
    "temp_executable_file",
    "temp_symlink",
]
