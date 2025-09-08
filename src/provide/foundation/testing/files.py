"""
File and Directory Test Fixtures.

Common fixtures for testing file operations, creating temporary directories,
and standard test file structures used across the provide-io ecosystem.
"""

import tempfile
from pathlib import Path
from collections.abc import Generator

import pytest


@pytest.fixture
def temp_directory() -> Generator[Path, None, None]:
    """
    Create a temporary directory that's cleaned up after test.
    
    Yields:
        Path to the temporary directory.
    """
    with tempfile.TemporaryDirectory() as temp_dir:
        yield Path(temp_dir)


@pytest.fixture
def test_files_structure() -> Generator[tuple[Path, Path], None, None]:
    """
    Create standard test file structure with files and subdirectories.
    
    Creates:
        - source/
            - file1.txt (contains "Content 1")
            - file2.txt (contains "Content 2")
            - subdir/
                - file3.txt (contains "Content 3")
    
    Yields:
        Tuple of (temp_path, source_path)
    """
    with tempfile.TemporaryDirectory() as temp_dir:
        path = Path(temp_dir)
        source = path / "source"
        source.mkdir()
        
        # Create test files
        (source / "file1.txt").write_text("Content 1")
        (source / "file2.txt").write_text("Content 2")
        
        # Create subdirectory with files
        subdir = source / "subdir"
        subdir.mkdir()
        (subdir / "file3.txt").write_text("Content 3")
        
        yield path, source


@pytest.fixture
def temp_file():
    """
    Create a temporary file factory with optional content.
    
    Returns:
        A function that creates temporary files with specified content and suffix.
    """
    created_files = []
    
    def _make_temp_file(content: str = "test content", suffix: str = ".txt") -> Path:
        """
        Create a temporary file.
        
        Args:
            content: Content to write to the file
            suffix: File suffix/extension
            
        Returns:
            Path to the created temporary file
        """
        with tempfile.NamedTemporaryFile(mode='w', suffix=suffix, delete=False) as f:
            f.write(content)
            path = Path(f.name)
        created_files.append(path)
        return path
    
    yield _make_temp_file
    
    # Cleanup all created files
    for path in created_files:
        path.unlink(missing_ok=True)


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
    path.unlink(missing_ok=True)


@pytest.fixture
def nested_directory_structure() -> Generator[Path, None, None]:
    """
    Create a deeply nested directory structure for testing.
    
    Creates:
        - level1/
            - level2/
                - level3/
                    - deep_file.txt
            - file_l2.txt
        - file_l1.txt
    
    Yields:
        Path to the root of the structure.
    """
    with tempfile.TemporaryDirectory() as temp_dir:
        root = Path(temp_dir)
        
        # Create nested structure
        deep_dir = root / "level1" / "level2" / "level3"
        deep_dir.mkdir(parents=True)
        
        # Add files at different levels
        (root / "file_l1.txt").write_text("Level 1 file")
        (root / "level1" / "file_l2.txt").write_text("Level 2 file")
        (deep_dir / "deep_file.txt").write_text("Deep file")
        
        yield root


@pytest.fixture
def empty_directory() -> Generator[Path, None, None]:
    """
    Create an empty temporary directory.
    
    Yields:
        Path to an empty directory.
    """
    with tempfile.TemporaryDirectory() as temp_dir:
        yield Path(temp_dir)


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
    path.unlink(missing_ok=True)