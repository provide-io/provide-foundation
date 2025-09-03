"""Tests for atomic file operations."""

import os
import tempfile
from pathlib import Path

import pytest

from provide.foundation.file.atomic import (
    atomic_replace,
    atomic_write,
    atomic_write_text,
)


@pytest.fixture
def temp_dir():
    """Create a temporary directory for tests."""
    with tempfile.TemporaryDirectory() as td:
        yield Path(td)


def test_atomic_write_creates_file(temp_dir):
    """Test atomic write creates new file."""
    path = temp_dir / "test.txt"
    data = b"Hello, World!"
    
    atomic_write(path, data)
    
    assert path.exists()
    assert path.read_bytes() == data


def test_atomic_write_overwrites_file(temp_dir):
    """Test atomic write overwrites existing file."""
    path = temp_dir / "test.txt"
    path.write_bytes(b"Old content")
    
    new_data = b"New content"
    atomic_write(path, new_data)
    
    assert path.read_bytes() == new_data


def test_atomic_write_with_mode(temp_dir):
    """Test atomic write sets file permissions."""
    path = temp_dir / "test.txt"
    data = b"Test data"
    mode = 0o600
    
    atomic_write(path, data, mode=mode)
    
    assert path.exists()
    assert path.stat().st_mode & 0o777 == mode


def test_atomic_write_with_backup(temp_dir):
    """Test atomic write creates backup."""
    path = temp_dir / "test.txt"
    original_data = b"Original content"
    path.write_bytes(original_data)
    
    new_data = b"New content"
    atomic_write(path, new_data, backup=True)
    
    backup_path = path.with_suffix(".txt.bak")
    assert backup_path.exists()
    assert backup_path.read_bytes() == original_data
    assert path.read_bytes() == new_data


def test_atomic_write_creates_parent_dirs(temp_dir):
    """Test atomic write creates parent directories."""
    path = temp_dir / "subdir" / "nested" / "test.txt"
    data = b"Test data"
    
    atomic_write(path, data)
    
    assert path.exists()
    assert path.read_bytes() == data


def test_atomic_write_text(temp_dir):
    """Test atomic text write."""
    path = temp_dir / "test.txt"
    text = "Hello, 世界! 🚀"
    
    atomic_write_text(path, text)
    
    assert path.exists()
    assert path.read_text(encoding="utf-8") == text


def test_atomic_write_text_with_encoding(temp_dir):
    """Test atomic text write with different encoding."""
    path = temp_dir / "test.txt"
    text = "Hello, World!"
    
    atomic_write_text(path, text, encoding="latin-1")
    
    assert path.exists()
    assert path.read_text(encoding="latin-1") == text


def test_atomic_replace(temp_dir):
    """Test atomic replace of existing file."""
    path = temp_dir / "test.txt"
    original_data = b"Original"
    path.write_bytes(original_data)
    original_mode = path.stat().st_mode
    
    new_data = b"Replaced"
    atomic_replace(path, new_data)
    
    assert path.read_bytes() == new_data
    assert path.stat().st_mode == original_mode


def test_atomic_replace_missing_file(temp_dir):
    """Test atomic replace raises for missing file."""
    path = temp_dir / "nonexistent.txt"
    
    with pytest.raises(FileNotFoundError):
        atomic_replace(path, b"Data")


def test_atomic_replace_without_preserve_mode(temp_dir):
    """Test atomic replace without preserving mode."""
    path = temp_dir / "test.txt"
    path.write_bytes(b"Original")
    os.chmod(path, 0o600)
    
    new_data = b"Replaced"
    atomic_replace(path, new_data, preserve_mode=False)
    
    assert path.read_bytes() == new_data
    # Mode should be default (not necessarily 0o600)
    assert path.stat().st_mode & 0o777 != 0o600 or path.stat().st_mode & 0o777 == 0o644


def test_atomic_write_handles_errors(temp_dir):
    """Test atomic write cleans up on error."""
    # Create a directory where we expect a file
    path = temp_dir / "actually_a_dir"
    path.mkdir()
    
    with pytest.raises(OSError):
        atomic_write(path, b"Data")
    
    # Check no temp files left behind
    temp_files = list(temp_dir.glob(".actually_a_dir.*.tmp"))
    assert len(temp_files) == 0


def test_atomic_write_preserves_permissions(temp_dir):
    """Test atomic write preserves existing file permissions."""
    path = temp_dir / "test.txt"
    path.write_bytes(b"Original")
    os.chmod(path, 0o600)
    
    atomic_write(path, b"New content")
    
    assert path.stat().st_mode & 0o777 == 0o600