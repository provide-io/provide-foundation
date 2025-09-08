"""Tests for directory operations."""

import os
from pathlib import Path
from typing import Never

import pytest
from provide.foundation.testing.file import temp_directory
from provide.foundation.file.directory import (
    ensure_dir,
    ensure_parent_dir,
    safe_rmtree,
    temp_dir,
)



def base_temp_dir():
    """Create a base temporary directory for tests."""
    with tempfile.TemporaryDirectory() as td:
        yield Path(td)


def test_ensure_dir_creates_new(base_temp_dir) -> None:
    """Test ensure_dir creates new directory."""
    path = base_temp_dir / "new_dir"

    result = ensure_dir(path)

    assert result == path
    assert path.exists()
    assert path.is_dir()


def test_ensure_dir_existing(base_temp_dir) -> None:
    """Test ensure_dir with existing directory."""
    path = base_temp_dir / "existing_dir"
    path.mkdir()

    result = ensure_dir(path)

    assert result == path
    assert path.exists()
    assert path.is_dir()


def test_ensure_dir_with_parents(base_temp_dir) -> None:
    """Test ensure_dir creates parent directories."""
    path = base_temp_dir / "parent" / "child" / "grandchild"

    result = ensure_dir(path)

    assert result == path
    assert path.exists()
    assert path.is_dir()
    assert path.parent.exists()
    assert path.parent.parent.exists()


def test_ensure_dir_with_mode(base_temp_dir) -> None:
    """Test ensure_dir sets permissions."""
    path = base_temp_dir / "dir_with_mode"
    mode = 0o700

    ensure_dir(path, mode=mode)

    assert path.exists()
    assert path.stat().st_mode & 0o777 == mode


def test_ensure_dir_file_exists(base_temp_dir) -> None:
    """Test ensure_dir raises when path is a file."""
    path = base_temp_dir / "actually_a_file"
    path.write_text("content")

    with pytest.raises(NotADirectoryError):
        ensure_dir(path)


def test_ensure_parent_dir(base_temp_dir) -> None:
    """Test ensure_parent_dir creates parent directory."""
    file_path = base_temp_dir / "subdir" / "file.txt"

    result = ensure_parent_dir(file_path)

    assert result == file_path.parent
    assert file_path.parent.exists()
    assert file_path.parent.is_dir()
    assert not file_path.exists()  # File itself not created


def test_ensure_parent_dir_nested(base_temp_dir) -> None:
    """Test ensure_parent_dir creates nested parents."""
    file_path = base_temp_dir / "a" / "b" / "c" / "file.txt"

    result = ensure_parent_dir(file_path)

    assert result == file_path.parent
    assert file_path.parent.exists()
    assert file_path.parent.parent.exists()
    assert file_path.parent.parent.parent.exists()


def test_ensure_parent_dir_with_mode(base_temp_dir) -> None:
    """Test ensure_parent_dir sets mode."""
    file_path = base_temp_dir / "subdir" / "file.txt"
    mode = 0o700

    ensure_parent_dir(file_path, mode=mode)

    assert file_path.parent.stat().st_mode & 0o777 == mode


def test_ensure_parent_dir_root_file(base_temp_dir) -> None:
    """Test ensure_parent_dir with file in current dir."""
    file_path = Path("file.txt")

    result = ensure_parent_dir(file_path)

    assert result == Path()


def test_temp_dir_creates_and_cleans() -> None:
    """Test temp_directory context manager creates and cleans up."""
    temp_path = None

    with temp_dir(prefix="test_") as td:
        temp_path = td
        assert td.exists()
        assert td.is_dir()
        assert td.name.startswith("test_")

        # Create a file in the temp dir
        test_file = td / "test.txt"
        test_file.write_text("content")
        assert test_file.exists()

    # After context, directory should be gone
    assert not temp_path.exists()


def test_temp_dir_no_cleanup() -> None:
    """Test temp_directory without cleanup."""
    temp_path = None

    with temp_dir(prefix="test_", cleanup=False) as td:
        temp_path = td
        assert td.exists()
        test_file = td / "test.txt"
        test_file.write_text("content")

    # Directory should still exist
    assert temp_path.exists()
    assert (temp_path / "test.txt").exists()

    # Clean up manually
    import shutil

    shutil.rmtree(temp_path)


def test_temp_dir_exception_still_cleans() -> Never:
    """Test temp_directory cleans up even on exception."""
    temp_path = None

    with pytest.raises(ValueError), temp_dir() as td:
        temp_path = td
        assert td.exists()
        raise ValueError("Test exception")

    # Should still be cleaned up
    assert not temp_path.exists()


def test_safe_rmtree(base_temp_dir) -> None:
    """Test safe_rmtree removes directory tree."""
    path = base_temp_dir / "to_remove"
    path.mkdir()
    (path / "subdir").mkdir()
    (path / "file.txt").write_text("content")
    (path / "subdir" / "nested.txt").write_text("nested")

    result = safe_rmtree(path)

    assert result is True
    assert not path.exists()


def test_safe_rmtree_missing_ok(base_temp_dir) -> None:
    """Test safe_rmtree with missing directory."""
    path = base_temp_dir / "nonexistent"

    result = safe_rmtree(path, missing_ok=True)

    assert result is False


def test_safe_rmtree_missing_not_ok(base_temp_dir) -> None:
    """Test safe_rmtree raises for missing directory."""
    path = base_temp_dir / "nonexistent"

    with pytest.raises(FileNotFoundError):
        safe_rmtree(path, missing_ok=False)


def test_safe_rmtree_permission_error() -> None:
    """Test safe_rmtree handles permission errors gracefully."""
    with temp_dir() as td:
        protected = td / "protected"
        protected.mkdir()
        (protected / "file.txt").write_text("content")

        # Make directory read-only
        os.chmod(protected, 0o444)

        # Should raise an error
        with pytest.raises(OSError):
            safe_rmtree(protected)

        # Restore permissions for cleanup
        os.chmod(protected, 0o755)
