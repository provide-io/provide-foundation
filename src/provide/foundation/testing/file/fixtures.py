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


@pytest.fixture
def temp_named_file():
    """
    Create a named temporary file factory.
    
    Returns:
        Function that creates named temporary files.
    """
    created_files = []
    
    def _make_named_file(
        content: bytes | str = None,
        suffix: str = "",
        prefix: str = "tmp",
        dir: Path | str = None,
        mode: str = 'w+b',
        delete: bool = False
    ) -> Path:
        """
        Create a named temporary file.
        
        Args:
            content: Optional content to write
            suffix: File suffix
            prefix: File prefix
            dir: Directory for the file
            mode: File mode
            delete: Whether to delete on close
            
        Returns:
            Path to the created file
        """
        if isinstance(dir, Path):
            dir = str(dir)
        
        f = tempfile.NamedTemporaryFile(
            mode=mode,
            suffix=suffix,
            prefix=prefix,
            dir=dir,
            delete=delete
        )
        
        if content is not None:
            if isinstance(content, str):
                if 'b' in mode:
                    f.write(content.encode())
                else:
                    f.write(content)
            else:
                f.write(content)
            f.flush()
        
        path = Path(f.name)
        f.close()
        
        if not delete:
            created_files.append(path)
        
        return path
    
    yield _make_named_file
    
    # Cleanup
    for path in created_files:
        path.unlink(missing_ok=True)


@pytest.fixture
def temp_file_with_content():
    """
    Create temporary files with specific content.
    
    Returns:
        Function that creates files with content.
    """
    created_files = []
    
    def _make_file(
        content: str | bytes,
        suffix: str = ".txt",
        encoding: str = "utf-8"
    ) -> Path:
        """
        Create a temporary file with content.
        
        Args:
            content: Content to write
            suffix: File suffix
            encoding: Text encoding (for str content)
            
        Returns:
            Path to created file
        """
        with tempfile.NamedTemporaryFile(
            mode='wb' if isinstance(content, bytes) else 'w',
            suffix=suffix,
            delete=False,
            encoding=None if isinstance(content, bytes) else encoding
        ) as f:
            f.write(content)
            path = Path(f.name)
        
        created_files.append(path)
        return path
    
    yield _make_file
    
    # Cleanup
    for path in created_files:
        path.unlink(missing_ok=True)


@pytest.fixture
def temp_binary_file():
    """
    Create temporary binary files.
    
    Returns:
        Function that creates binary files.
    """
    created_files = []
    
    def _make_binary(
        size: int = 1024,
        pattern: bytes = None,
        suffix: str = ".bin"
    ) -> Path:
        """
        Create a temporary binary file.
        
        Args:
            size: File size in bytes
            pattern: Optional byte pattern to repeat
            suffix: File suffix
            
        Returns:
            Path to created binary file
        """
        if pattern is None:
            # Create pseudo-random binary data
            import random
            content = bytes(random.randint(0, 255) for _ in range(size))
        else:
            # Repeat pattern to reach size
            repetitions = size // len(pattern) + 1
            content = (pattern * repetitions)[:size]
        
        with tempfile.NamedTemporaryFile(
            mode='wb',
            suffix=suffix,
            delete=False
        ) as f:
            f.write(content)
            path = Path(f.name)
        
        created_files.append(path)
        return path
    
    yield _make_binary
    
    # Cleanup
    for path in created_files:
        path.unlink(missing_ok=True)


@pytest.fixture
def temp_csv_file():
    """
    Create temporary CSV files for testing.
    
    Returns:
        Function that creates CSV files.
    """
    import csv
    created_files = []
    
    def _make_csv(
        headers: list[str],
        rows: list[list],
        suffix: str = ".csv"
    ) -> Path:
        """
        Create a temporary CSV file.
        
        Args:
            headers: Column headers
            rows: Data rows
            suffix: File suffix
            
        Returns:
            Path to created CSV file
        """
        with tempfile.NamedTemporaryFile(
            mode='w',
            suffix=suffix,
            delete=False,
            newline=''
        ) as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            writer.writerows(rows)
            path = Path(f.name)
        
        created_files.append(path)
        return path
    
    yield _make_csv
    
    # Cleanup
    for path in created_files:
        path.unlink(missing_ok=True)


@pytest.fixture
def temp_json_file():
    """
    Create temporary JSON files for testing.
    
    Returns:
        Function that creates JSON files.
    """
    import json
    created_files = []
    
    def _make_json(
        data: dict | list,
        suffix: str = ".json",
        indent: int = 2
    ) -> Path:
        """
        Create a temporary JSON file.
        
        Args:
            data: JSON data to write
            suffix: File suffix
            indent: JSON indentation
            
        Returns:
            Path to created JSON file
        """
        with tempfile.NamedTemporaryFile(
            mode='w',
            suffix=suffix,
            delete=False
        ) as f:
            json.dump(data, f, indent=indent)
            path = Path(f.name)
        
        created_files.append(path)
        return path
    
    yield _make_json
    
    # Cleanup
    for path in created_files:
        path.unlink(missing_ok=True)


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
        link.unlink(missing_ok=True)


@pytest.fixture
def temp_executable_file():
    """
    Create temporary executable files for testing.
    
    Returns:
        Function that creates executable files.
    """
    import stat
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
        path.unlink(missing_ok=True)