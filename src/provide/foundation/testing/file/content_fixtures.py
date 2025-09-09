"""
Content-based file test fixtures.

Fixtures for creating files with specific content types like text, binary,
CSV, JSON, and other structured data.
"""

import csv
import json
import random
import tempfile
from pathlib import Path

import pytest

from provide.foundation.file.safe import safe_delete


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
        safe_delete(path, missing_ok=True)


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
        safe_delete(path, missing_ok=True)


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
        safe_delete(path, missing_ok=True)


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
        safe_delete(path, missing_ok=True)


@pytest.fixture
def temp_csv_file():
    """
    Create temporary CSV files for testing.
    
    Returns:
        Function that creates CSV files.
    """
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
        safe_delete(path, missing_ok=True)


@pytest.fixture
def temp_json_file():
    """
    Create temporary JSON files for testing.
    
    Returns:
        Function that creates JSON files.
    """
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
        safe_delete(path, missing_ok=True)


__all__ = [
    "temp_file",
    "temp_named_file",
    "temp_file_with_content",
    "temp_binary_file",
    "temp_csv_file",
    "temp_json_file",
]