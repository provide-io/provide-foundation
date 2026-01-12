#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for directory operations."""

from __future__ import annotations

from pathlib import Path
from typing import Never

from provide.testkit import FoundationTestCase
import pytest

from provide.foundation.file import temp_dir
from provide.foundation.file.directory import (
    ensure_dir,
    ensure_parent_dir,
    safe_rmtree,
)


class TestDirectoryOperations(FoundationTestCase):
    """Test directory operations."""

    def setup_method(self) -> None:
        """Set up test environment."""
        super().setup_method()

    def teardown_method(self) -> None:
        """Clean up after test."""
        super().teardown_method()

    def test_ensure_dir_creates_new(self, temp_directory: Path) -> None:
        """Test ensure_dir creates new directory."""
        path = temp_directory / "new_dir"

        result = ensure_dir(path)

        assert result == path
        assert path.exists()
        assert path.is_dir()

    def test_ensure_dir_existing(self, temp_directory: Path) -> None:
        """Test ensure_dir with existing directory."""
        path = temp_directory / "existing_dir"
        path.mkdir()

        result = ensure_dir(path)

        assert result == path
        assert path.exists()
        assert path.is_dir()

    def test_ensure_dir_with_parents(self, temp_directory: Path) -> None:
        """Test ensure_dir creates parent directories."""
        path = temp_directory / "parent" / "child" / "grandchild"

        result = ensure_dir(path)

        assert result == path
        assert path.exists()
        assert path.is_dir()
        assert path.parent.exists()
        assert path.parent.parent.exists()

    def test_ensure_dir_with_mode(self, temp_directory: Path) -> None:
        """Test ensure_dir sets permissions."""
        path = temp_directory / "dir_with_mode"
        mode = 0o700

        ensure_dir(path, mode=mode)

        assert path.exists()
        assert path.stat().st_mode & 0o777 == mode

    def test_ensure_dir_file_exists(self, temp_directory: Path) -> None:
        """Test ensure_dir raises when path is a file."""

        path = temp_directory / "actually_a_file"
        path.write_text("content")

        with pytest.raises(NotADirectoryError):
            ensure_dir(path)

    def test_ensure_parent_dir(self, temp_directory: Path) -> None:
        """Test ensure_parent_dir creates parent directory."""

        file_path = temp_directory / "subdir" / "file.txt"

        result = ensure_parent_dir(file_path)

        assert result == file_path.parent
        assert file_path.parent.exists()
        assert file_path.parent.is_dir()
        assert not file_path.exists()  # File itself not created

    def test_ensure_parent_dir_nested(self, temp_directory: Path) -> None:
        """Test ensure_parent_dir creates nested parents."""

        file_path = temp_directory / "a" / "b" / "c" / "file.txt"

        result = ensure_parent_dir(file_path)

        assert result == file_path.parent
        assert file_path.parent.exists()
        assert file_path.parent.parent.exists()
        assert file_path.parent.parent.parent.exists()

    def test_ensure_parent_dir_with_mode(self, temp_directory: Path) -> None:
        """Test ensure_parent_dir sets mode."""

        file_path = temp_directory / "subdir" / "file.txt"
        mode = 0o700

        ensure_parent_dir(file_path, mode=mode)

        assert file_path.parent.stat().st_mode & 0o777 == mode

    def test_ensure_parent_dir_root_file(self, temp_directory: Path) -> None:
        """Test ensure_parent_dir with file in current dir."""

        file_path = Path("file.txt")

        result = ensure_parent_dir(file_path)

        assert result == Path()

    def test_temp_dir_creates_and_cleans(self) -> None:
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

    def test_temp_dir_no_cleanup(self) -> None:
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

    def test_temp_dir_exception_still_cleans(self) -> Never:
        """Test temp_directory cleans up even on exception."""

        temp_path = None

        with pytest.raises(ValueError), temp_dir() as td:
            temp_path = td
            assert td.exists()
            raise ValueError("Test exception")

        # Should still be cleaned up
        assert not temp_path.exists()

    def test_safe_rmtree(self, temp_directory: Path) -> None:
        """Test safe_rmtree removes directory tree."""

        path = temp_directory / "to_remove"
        path.mkdir()
        (path / "subdir").mkdir()
        (path / "file.txt").write_text("content")
        (path / "subdir" / "nested.txt").write_text("nested")

        result = safe_rmtree(path)

        assert result is True
        assert not path.exists()

    def test_safe_rmtree_missing_ok(self, temp_directory: Path) -> None:
        """Test safe_rmtree with missing directory."""

        path = temp_directory / "nonexistent"

        result = safe_rmtree(path, missing_ok=True)

        assert result is False

    def test_safe_rmtree_missing_not_ok(self, temp_directory: Path) -> None:
        """Test safe_rmtree raises for missing directory."""

        path = temp_directory / "nonexistent"

        with pytest.raises(FileNotFoundError):
            safe_rmtree(path, missing_ok=False)

    def test_safe_rmtree_permission_error(self) -> None:
        """Test safe_rmtree handles permission errors gracefully."""

        with temp_dir() as td:
            protected = td / "protected"
            protected.mkdir()
            (protected / "file.txt").write_text("content")

            # Make directory read-only
            protected.chmod(0o444)

            # Should raise an error
            with pytest.raises(OSError):
                safe_rmtree(protected)

            # Restore permissions for cleanup
            protected.chmod(0o755)


# 🧱🏗️🔚
