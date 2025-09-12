"""
Directory-specific test fixtures.

Fixtures for creating temporary directories, nested structures,
and standard test directory layouts.
"""

from collections.abc import Generator
from pathlib import Path

import pytest

from provide.foundation.file import temp_dir as foundation_temp_dir


@pytest.fixture
def temp_directory() -> Generator[Path, None, None]:
    """
    Create a temporary directory that's cleaned up after test.

    Yields:
        Path to the temporary directory.
    """
    with foundation_temp_dir() as temp_dir:
        yield temp_dir


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
    with foundation_temp_dir() as path:
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
    with foundation_temp_dir() as root:

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
    with foundation_temp_dir() as temp_dir:
        yield temp_dir


__all__ = [
    "empty_directory",
    "nested_directory_structure",
    "temp_directory",
    "test_files_structure",
]
