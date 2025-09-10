"""
Special file test fixtures.

Fixtures for creating specialized files like binary files, read-only files,
symbolic links, and executable files.
"""

import stat
import tempfile
from pathlib import Path
from collections.abc import Generator

import pytest

from provide.foundation.file.safe import safe_delete


@pytest.fixture
def binary_file() -> Generator[Path, None, None]:
    """
    Create a temporary binary file for testing.
    
    Yields:
        Path to a binary file containing sample binary data.
    """
    with tempfile.NamedTemporaryFile(mode='wb', suffix='.bin', delete=False) as f:
        # Write some binary data
        f.write(b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09')
        f.write(b'\xFF\xFE\xFD\xFC\xFB\xFA\xF9\xF8\xF7\xF6')
        path = Path(f.name)
    
    yield path
    safe_delete(path, missing_ok=True)


@pytest.fixture
def readonly_file() -> Generator[Path, None, None]:
    """
    Create a read-only file for permission testing.
    
    Yields:
        Path to a read-only file.
    """
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        f.write("Read-only content")
        path = Path(f.name)
    
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
    
    def _make_symlink(
        target: Path | str,
        link_name: Path | str = None
    ) -> Path:
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
            with tempfile.NamedTemporaryFile(delete=True) as f:
                link_name = Path(f.name + "_link")
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
    
    def _make_executable(
        content: str = "#!/bin/sh\necho 'test'\n",
        suffix: str = ".sh"
    ) -> Path:
        """
        Create a temporary executable file.
        
        Args:
            content: Script content
            suffix: File suffix
            
        Returns:
            Path to created executable file
        """
        with tempfile.NamedTemporaryFile(
            mode='w',
            suffix=suffix,
            delete=False
        ) as f:
            f.write(content)
            path = Path(f.name)
        
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
    "temp_symlink",
    "temp_executable_file",
]