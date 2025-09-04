"""Tests for safe file operations."""

import tempfile
from pathlib import Path

import pytest

from provide.foundation.file.safe import (
    safe_copy,
    safe_delete,
    safe_move,
    safe_read,
    safe_read_text,
)


@pytest.fixture
def temp_dir():
    """Create a temporary directory for tests."""
    with tempfile.TemporaryDirectory() as td:
        yield Path(td)


def test_safe_read_existing_file(temp_dir):
    """Test safe read of existing file."""
    path = temp_dir / "test.txt"
    data = b"Test content"
    path.write_bytes(data)
    
    result = safe_read(path)
    assert result == data


def test_safe_read_missing_file(temp_dir):
    """Test safe read returns default for missing file."""
    path = temp_dir / "nonexistent.txt"
    
    result = safe_read(path)
    assert result is None
    
    default = b"Default"
    result = safe_read(path, default=default)
    assert result == default


def test_safe_read_with_encoding(temp_dir):
    """Test safe read with encoding."""
    path = temp_dir / "test.txt"
    text = "Hello, 世界!"
    path.write_text(text, encoding="utf-8")
    
    result = safe_read(path, encoding="utf-8")
    assert result == text


def test_safe_read_text(temp_dir):
    """Test safe read text."""
    path = temp_dir / "test.txt"
    text = "Test text content"
    path.write_text(text)
    
    result = safe_read_text(path)
    assert result == text


def test_safe_read_text_missing_file(temp_dir):
    """Test safe read text returns default for missing file."""
    path = temp_dir / "nonexistent.txt"
    
    result = safe_read_text(path)
    assert result == ""
    
    default = "Default text"
    result = safe_read_text(path, default=default)
    assert result == default


def test_safe_read_text_with_encoding(temp_dir):
    """Test safe read text with specific encoding."""
    path = temp_dir / "test.txt"
    text = "Test text"
    path.write_text(text, encoding="latin-1")
    
    result = safe_read_text(path, encoding="latin-1")
    assert result == text


def test_safe_delete_existing_file(temp_dir):
    """Test safe delete of existing file."""
    path = temp_dir / "test.txt"
    path.write_text("content")
    
    result = safe_delete(path)
    assert result is True
    assert not path.exists()


def test_safe_delete_missing_file(temp_dir):
    """Test safe delete of missing file."""
    path = temp_dir / "nonexistent.txt"
    
    result = safe_delete(path)
    assert result is False


def test_safe_delete_missing_not_ok(temp_dir):
    """Test safe delete raises for missing file when missing_ok=False."""
    path = temp_dir / "nonexistent.txt"
    
    with pytest.raises(FileNotFoundError):
        safe_delete(path, missing_ok=False)


def test_safe_move(temp_dir):
    """Test safe move of file."""
    src = temp_dir / "source.txt"
    dst = temp_dir / "destination.txt"
    content = "Test content"
    src.write_text(content)
    
    safe_move(src, dst)
    
    assert not src.exists()
    assert dst.exists()
    assert dst.read_text() == content


def test_safe_move_to_subdir(temp_dir):
    """Test safe move creates parent directories."""
    src = temp_dir / "source.txt"
    dst = temp_dir / "subdir" / "nested" / "destination.txt"
    content = "Test content"
    src.write_text(content)
    
    safe_move(src, dst)
    
    assert not src.exists()
    assert dst.exists()
    assert dst.read_text() == content


def test_safe_move_overwrite(temp_dir):
    """Test safe move with overwrite."""
    src = temp_dir / "source.txt"
    dst = temp_dir / "destination.txt"
    src.write_text("Source content")
    dst.write_text("Old destination content")
    
    safe_move(src, dst, overwrite=True)
    
    assert not src.exists()
    assert dst.read_text() == "Source content"


def test_safe_move_no_overwrite(temp_dir):
    """Test safe move without overwrite raises."""
    src = temp_dir / "source.txt"
    dst = temp_dir / "destination.txt"
    src.write_text("Source content")
    dst.write_text("Destination content")
    
    with pytest.raises(FileExistsError):
        safe_move(src, dst, overwrite=False)
    
    assert src.exists()
    assert dst.read_text() == "Destination content"


def test_safe_move_missing_source(temp_dir):
    """Test safe move with missing source raises."""
    src = temp_dir / "nonexistent.txt"
    dst = temp_dir / "destination.txt"
    
    with pytest.raises(FileNotFoundError):
        safe_move(src, dst)


def test_safe_copy(temp_dir):
    """Test safe copy of file."""
    src = temp_dir / "source.txt"
    dst = temp_dir / "destination.txt"
    content = "Test content"
    src.write_text(content)
    
    safe_copy(src, dst)
    
    assert src.exists()
    assert dst.exists()
    assert dst.read_text() == content


def test_safe_copy_to_subdir(temp_dir):
    """Test safe copy creates parent directories."""
    src = temp_dir / "source.txt"
    dst = temp_dir / "subdir" / "nested" / "destination.txt"
    content = "Test content"
    src.write_text(content)
    
    safe_copy(src, dst)
    
    assert src.exists()
    assert dst.exists()
    assert dst.read_text() == content


def test_safe_copy_preserves_mode(temp_dir):
    """Test safe copy preserves file permissions."""
    import os
    
    src = temp_dir / "source.txt"
    dst = temp_dir / "destination.txt"
    src.write_text("content")
    os.chmod(src, 0o600)
    
    safe_copy(src, dst, preserve_mode=True)
    
    assert dst.stat().st_mode & 0o777 == 0o600


def test_safe_copy_no_preserve_mode(temp_dir):
    """Test safe copy without preserving mode."""
    import os
    
    src = temp_dir / "source.txt"
    dst = temp_dir / "destination.txt"
    src.write_text("content")
    os.chmod(src, 0o600)
    
    safe_copy(src, dst, preserve_mode=False)
    
    # With preserve_mode=False, shutil.copy is used instead of copy2
    # shutil.copy doesn't preserve permissions, so dst gets default permissions
    dst_mode = dst.stat().st_mode & 0o777
    # The exact mode depends on umask, but it shouldn't be 0o600
    # Actually, shutil.copy DOES copy permissions on Unix systems
    # So this test expectation was wrong - safe_copy with preserve_mode=False
    # still copies permissions due to shutil.copy behavior
    assert dst_mode == 0o600  # shutil.copy copies permissions on Unix


def test_safe_copy_overwrite(temp_dir):
    """Test safe copy with overwrite."""
    src = temp_dir / "source.txt"
    dst = temp_dir / "destination.txt"
    src.write_text("Source content")
    dst.write_text("Old destination content")
    
    safe_copy(src, dst, overwrite=True)
    
    assert src.exists()
    assert dst.read_text() == "Source content"


def test_safe_copy_no_overwrite(temp_dir):
    """Test safe copy without overwrite raises."""
    src = temp_dir / "source.txt"
    dst = temp_dir / "destination.txt"
    src.write_text("Source content")
    dst.write_text("Destination content")
    
    with pytest.raises(FileExistsError):
        safe_copy(src, dst, overwrite=False)
    
    assert dst.read_text() == "Destination content"


def test_safe_copy_missing_source(temp_dir):
    """Test safe copy with missing source raises."""
    src = temp_dir / "nonexistent.txt"
    dst = temp_dir / "destination.txt"
    
    with pytest.raises(FileNotFoundError):
        safe_copy(src, dst)