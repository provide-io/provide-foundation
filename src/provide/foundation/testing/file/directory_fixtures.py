"""
Directory-specific test fixtures.

Fixtures for creating temporary directories, nested structures, 
and standard test directory layouts.
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


__all__ = [
    "temp_directory",
    "test_files_structure", 
    "nested_directory_structure",
    "empty_directory",
]