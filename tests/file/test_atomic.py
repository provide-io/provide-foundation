#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for atomic file operations."""

from __future__ import annotations

from pathlib import Path

from provide.testkit import FoundationTestCase
import pytest

from provide.foundation.file.atomic import (
    atomic_replace,
    atomic_write,
    atomic_write_text,
)


class TestAtomicFileOperations(FoundationTestCase):
    """Test atomic file operations."""

    def setup_method(self) -> None:
        """Set up test environment."""
        super().setup_method()

    def teardown_method(self) -> None:
        """Clean up after test."""
        super().teardown_method()

    def test_atomic_write_creates_file(self, temp_directory: Path) -> None:
        """Test atomic write creates new file."""
        path = temp_directory / "test.txt"
        data = b"Hello, World!"

        atomic_write(path, data)

        assert path.exists()
        assert path.read_bytes() == data

    def test_atomic_write_overwrites_file(self, temp_directory: Path) -> None:
        """Test atomic write overwrites existing file."""
        path = temp_directory / "test.txt"
        path.write_bytes(b"Old content")

        new_data = b"New content"
        atomic_write(path, new_data)

        assert path.read_bytes() == new_data

    def test_atomic_write_with_mode(self, temp_directory: Path) -> None:
        """Test atomic write sets file permissions."""
        path = temp_directory / "test.txt"
        data = b"Test data"
        mode = 0o600

        atomic_write(path, data, mode=mode)

        assert path.exists()
        assert path.stat().st_mode & 0o777 == mode

    def test_atomic_write_with_backup(self, temp_directory: Path) -> None:
        """Test atomic write creates backup."""
        path = temp_directory / "test.txt"
        original_data = b"Original content"
        path.write_bytes(original_data)

        new_data = b"New content"
        atomic_write(path, new_data, backup=True)

        backup_path = path.with_suffix(".txt.bak")
        assert backup_path.exists()
        assert backup_path.read_bytes() == original_data
        assert path.read_bytes() == new_data

    def test_atomic_write_creates_parent_dirs(self, temp_directory: Path) -> None:
        """Test atomic write creates parent directories."""
        path = temp_directory / "subdir" / "nested" / "test.txt"
        data = b"Test data"

        atomic_write(path, data)

        assert path.exists()
        assert path.read_bytes() == data

    def test_atomic_write_text(self, temp_directory: Path) -> None:
        """Test atomic text write."""
        path = temp_directory / "test.txt"
        text = "Hello, 世界! 🚀"

        atomic_write_text(path, text)

        assert path.exists()
        assert path.read_text(encoding="utf-8") == text

    def test_atomic_write_text_with_encoding(self, temp_directory: Path) -> None:
        """Test atomic text write with different encoding."""
        path = temp_directory / "test.txt"
        text = "Hello, World!"

        atomic_write_text(path, text, encoding="latin-1")

        assert path.exists()
        assert path.read_text(encoding="latin-1") == text

    def test_atomic_replace(self, temp_directory: Path) -> None:
        """Test atomic replace of existing file."""
        path = temp_directory / "test.txt"
        original_data = b"Original"
        path.write_bytes(original_data)
        original_mode = path.stat().st_mode

        new_data = b"Replaced"
        atomic_replace(path, new_data)

        assert path.read_bytes() == new_data
        assert path.stat().st_mode == original_mode

    def test_atomic_replace_missing_file(self, temp_directory: Path) -> None:
        """Test atomic replace raises for missing file."""
        path = temp_directory / "nonexistent.txt"

        with pytest.raises(FileNotFoundError):
            atomic_replace(path, b"Data")

    def test_atomic_replace_without_preserve_mode(self, temp_directory: Path) -> None:
        """Test atomic replace without preserving mode."""
        path = temp_directory / "test.txt"
        path.write_bytes(b"Original")
        path.chmod(0o600)

        new_data = b"Replaced"
        atomic_replace(path, new_data, preserve_mode=False)

        assert path.read_bytes() == new_data
        # When preserve_mode=False, the file gets default permissions
        # based on umask. It should not keep the 0o600 permissions.
        # Default is usually 0o644 or 0o664
        mode = path.stat().st_mode & 0o777
        assert mode != 0o600  # Should not preserve the restricted mode
        assert mode >= 0o644  # Should have at least read permissions for owner/group

    def test_atomic_write_handles_errors(self, temp_directory: Path) -> None:
        """Test atomic write cleans up on error."""
        # Create a directory where we expect a file
        path = temp_directory / "actually_a_dir"
        path.mkdir()

        with pytest.raises(OSError):
            atomic_write(path, b"Data")

        # Check no temp files left behind
        temp_files = list(temp_directory.glob(".actually_a_dir.*.tmp"))
        assert len(temp_files) == 0

    def test_atomic_write_preserves_permissions(self, temp_directory: Path) -> None:
        """Test atomic write preserves existing file permissions by default."""
        path = temp_directory / "test.txt"
        path.write_bytes(b"Original")
        path.chmod(0o600)

        atomic_write(path, b"New content")  # preserve_mode=True by default

        assert path.stat().st_mode & 0o777 == 0o600

    def test_atomic_write_no_preserve_permissions(self, temp_directory: Path) -> None:
        """Test atomic write without preserving permissions."""
        path = temp_directory / "test.txt"
        path.write_bytes(b"Original")
        path.chmod(0o600)

        atomic_write(path, b"New content", preserve_mode=False)

        # Should not preserve 0o600
        mode = path.stat().st_mode & 0o777
        assert mode != 0o600
        assert mode >= 0o644  # Should have at least standard read permissions


# 🧱🏗️🔚
