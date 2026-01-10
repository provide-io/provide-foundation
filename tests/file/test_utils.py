#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for file utility functions."""

from __future__ import annotations

from pathlib import Path
import time

from provide.testkit import FoundationTestCase
import pytest

from provide.foundation.file.utils import (
    backup_file,
    find_files,
    get_mtime,
    get_size,
    touch,
)


class TestFileUtils(FoundationTestCase):
    """Test file utility functions."""

    def setup_method(self) -> None:
        """Set up test environment."""
        super().setup_method()

    def teardown_method(self) -> None:
        """Clean up after test."""
        super().teardown_method()

    def test_get_size_existing_file(self, temp_directory: Path) -> None:
        """Test getting size of existing file."""
        path = temp_directory / "test.txt"
        content = b"Hello, World!"
        path.write_bytes(content)

        size = get_size(path)
        assert size == len(content)

    def test_get_size_missing_file(self, temp_directory: Path) -> None:
        """Test getting size of missing file returns 0."""

        path = temp_directory / "nonexistent.txt"

        size = get_size(path)
        assert size == 0

    def test_get_size_empty_file(self, temp_directory: Path) -> None:
        """Test getting size of empty file."""

        path = temp_directory / "empty.txt"
        path.touch()

        size = get_size(path)
        assert size == 0

    def test_get_size_with_string_path(self, temp_directory: Path) -> None:
        """Test get_size accepts string path."""

        path = temp_directory / "test.txt"
        path.write_bytes(b"test")

        size = get_size(str(path))
        assert size == 4

    def test_get_mtime_existing_file(self, temp_directory: Path) -> None:
        """Test getting modification time of existing file."""

        path = temp_directory / "test.txt"
        path.write_text("content")

        mtime = get_mtime(path)
        assert mtime is not None
        # Verify mtime is a reasonable value (within last 10 seconds and not in the future)
        now = time.time()
        assert now - 10.0 <= mtime <= now + 1.0, f"mtime {mtime} is not within reasonable range of now {now}"

    def test_get_mtime_missing_file(self, temp_directory: Path) -> None:
        """Test getting mtime of missing file returns None."""

        path = temp_directory / "nonexistent.txt"

        mtime = get_mtime(path)
        assert mtime is None

    def test_get_mtime_with_string_path(self, temp_directory: Path) -> None:
        """Test get_mtime accepts string path."""

        path = temp_directory / "test.txt"
        path.write_text("test")

        mtime = get_mtime(str(path))
        assert mtime is not None

    def test_touch_creates_file(self, temp_directory: Path) -> None:
        """Test touch creates new file."""

        path = temp_directory / "new.txt"

        touch(path)

        assert path.exists()
        assert path.is_file()
        assert path.stat().st_size == 0

    def test_touch_updates_existing_file(self, temp_directory: Path) -> None:
        """Test touch updates timestamp of existing file."""

        path = temp_directory / "existing.txt"
        path.write_text("content")

        # Get original mtime
        original_mtime = path.stat().st_mtime

        # Wait a bit and touch
        time.sleep(0.01)
        touch(path)

        # mtime should be updated
        new_mtime = path.stat().st_mtime
        assert new_mtime > original_mtime

        # Content should be preserved
        assert path.read_text() == "content"

    def test_touch_with_mode(self, temp_directory: Path) -> None:
        """Test touch creates file with specific mode."""

        path = temp_directory / "test.txt"
        mode = 0o600

        touch(path, mode=mode)

        assert path.exists()
        assert path.stat().st_mode & 0o777 == mode

    def test_touch_exist_not_ok(self, temp_directory: Path) -> None:
        """Test touch raises when exist_ok=False."""

        path = temp_directory / "test.txt"
        path.write_text("content")

        with pytest.raises(FileExistsError):
            touch(path, exist_ok=False)

    def test_touch_creates_parent_dirs(self, temp_directory: Path) -> None:
        """Test touch creates parent directories."""

        path = temp_directory / "subdir" / "nested" / "file.txt"

        touch(path)

        assert path.exists()
        assert path.parent.exists()
        assert path.parent.parent.exists()

    def test_find_files_basic(self, temp_directory: Path) -> None:
        """Test finding files with basic pattern."""

        # Create test files
        (temp_directory / "test1.py").write_text("code")
        (temp_directory / "test2.py").write_text("code")
        (temp_directory / "test.txt").write_text("text")
        (temp_directory / "subdir").mkdir()
        (temp_directory / "subdir" / "test3.py").write_text("code")

        # Find Python files
        files = find_files("*.py", root=temp_directory)

        assert len(files) == 3
        names = {f.name for f in files}
        assert names == {"test1.py", "test2.py", "test3.py"}

    def test_find_files_non_recursive(self, temp_directory: Path) -> None:
        """Test non-recursive file finding."""

        # Create test files
        (temp_directory / "test1.py").write_text("code")
        (temp_directory / "test2.py").write_text("code")
        (temp_directory / "subdir").mkdir()
        (temp_directory / "subdir" / "test3.py").write_text("code")

        # Find Python files non-recursively
        files = find_files("*.py", root=temp_directory, recursive=False)

        assert len(files) == 2
        names = {f.name for f in files}
        assert names == {"test1.py", "test2.py"}

    def test_find_files_nested_pattern(self, temp_directory: Path) -> None:
        """Test finding files with nested pattern."""

        # Create test structure
        (temp_directory / "src").mkdir()
        (temp_directory / "src" / "main.py").write_text("code")
        (temp_directory / "tests").mkdir()
        (temp_directory / "tests" / "test_main.py").write_text("test")
        (temp_directory / "docs").mkdir()
        (temp_directory / "docs" / "readme.md").write_text("docs")

        # Find files in tests directory
        files = find_files("tests/*.py", root=temp_directory)

        assert len(files) == 1
        assert files[0].name == "test_main.py"

    def test_find_files_missing_root(self, temp_directory: Path) -> None:
        """Test find_files with non-existent root."""

        root = temp_directory / "nonexistent"

        files = find_files("*.py", root=root)

        assert files == []

    def test_find_files_excludes_directories(self, temp_directory: Path) -> None:
        """Test find_files excludes directories."""

        # Create files and directories
        (temp_directory / "file.txt").write_text("content")
        (temp_directory / "dir.txt").mkdir()  # Directory with .txt name

        files = find_files("*.txt", root=temp_directory)

        assert len(files) == 1
        assert files[0].name == "file.txt"

    def test_backup_file_basic(self, temp_directory: Path) -> None:
        """Test basic file backup."""

        path = temp_directory / "test.txt"
        content = "Original content"
        path.write_text(content)

        backup_path = backup_file(path)

        assert backup_path is not None
        assert backup_path.exists()
        assert backup_path.name == "test.txt.bak"
        assert backup_path.read_text() == content
        assert path.exists()  # Original still exists

    def test_backup_file_with_timestamp(self, temp_directory: Path) -> None:
        """Test backup with timestamp."""

        path = temp_directory / "test.txt"
        content = "Original content"
        path.write_text(content)

        backup_path = backup_file(path, timestamp=True)

        assert backup_path is not None
        assert backup_path.exists()
        # Should have format like test.20231225_143022.bak
        assert backup_path.name.startswith("test.")
        assert backup_path.name.endswith(".bak")
        assert len(backup_path.name) > len("test..bak")  # Has timestamp
        assert backup_path.read_text() == content

    def test_backup_file_custom_suffix(self, temp_directory: Path) -> None:
        """Test backup with custom suffix."""

        path = temp_directory / "test.txt"
        path.write_text("content")

        backup_path = backup_file(path, suffix=".backup")

        assert backup_path is not None
        assert backup_path.name == "test.txt.backup"

    def test_backup_file_multiple_backups(self, temp_directory: Path) -> None:
        """Test creating multiple backups."""

        path = temp_directory / "test.txt"
        path.write_text("version 1")

        # First backup
        backup1 = backup_file(path)
        assert backup1 is not None
        assert backup1.name == "test.txt.bak"

        # Modify original
        path.write_text("version 2")

        # Second backup should get a different name
        backup2 = backup_file(path)
        assert backup2 is not None
        assert backup2.name == "test.txt.bak.1"

        # Third backup
        path.write_text("version 3")
        backup3 = backup_file(path)
        assert backup3 is not None
        assert backup3.name == "test.txt.bak.2"

        # Check all backups exist
        assert backup1.exists()
        assert backup2.exists()
        assert backup3.exists()

    def test_backup_file_missing_source(self, temp_directory: Path) -> None:
        """Test backup of non-existent file returns None."""

        path = temp_directory / "nonexistent.txt"

        backup_path = backup_file(path)

        assert backup_path is None

    def test_backup_file_preserves_metadata(self, temp_directory: Path) -> None:
        """Test backup preserves file metadata."""

        path = temp_directory / "test.txt"
        path.write_text("content")
        path.chmod(0o600)

        backup_path = backup_file(path)

        assert backup_path is not None
        # shutil.copy2 should preserve permissions
        assert backup_path.stat().st_mode & 0o777 == 0o600


# 🧱🏗️🔚
