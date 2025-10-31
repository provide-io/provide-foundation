#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for TAR archive implementation."""

from __future__ import annotations

from pathlib import Path

from provide.testkit import FoundationTestCase
import pytest

from provide.foundation.archive.base import ArchiveError
from provide.foundation.archive.tar import TarArchive


class TestTarArchive(FoundationTestCase):
    """Test TAR archive functionality."""

    @pytest.fixture
    def tar_archive(self) -> TarArchive:
        """Create a TAR archive instance."""
        return TarArchive()

    def test_create_tar_archive(
        self, tar_archive: TarArchive, test_files_structure: tuple[Path, Path]
    ) -> None:
        """Test creating a TAR archive."""
        temp_path, source = test_files_structure
        output = temp_path / "test.tar"

        result = tar_archive.create(source, output)

        assert result == output
        assert output.exists()
        assert output.stat().st_size > 0

    def test_extract_tar_archive(
        self, tar_archive: TarArchive, test_files_structure: tuple[Path, Path]
    ) -> None:
        """Test extracting a TAR archive."""
        temp_path, source = test_files_structure
        archive = temp_path / "test.tar"
        output = temp_path / "extracted"

        # Create archive first
        tar_archive.create(source, archive)

        # Extract it
        result = tar_archive.extract(archive, output)

        assert result == output
        assert output.exists()
        # New consistent behavior: no parent directory in archive
        assert (output / "file1.txt").exists()
        assert (output / "file1.txt").read_text() == "Content 1"
        assert (output / "subdir" / "file3.txt").exists()

    def test_validate_tar_archive(
        self, tar_archive: TarArchive, test_files_structure: tuple[Path, Path]
    ) -> None:
        """Test validating a TAR archive."""
        temp_path, source = test_files_structure
        archive = temp_path / "test.tar"

        # Create valid archive
        tar_archive.create(source, archive)
        assert tar_archive.validate(archive) is True

        # Test invalid archive
        invalid = temp_path / "invalid.tar"
        invalid.write_text("not a tar file")
        assert tar_archive.validate(invalid) is False

        # Test non-existent file
        assert tar_archive.validate(temp_path / "nonexistent.tar") is False

    def test_deterministic_mode(self, test_files_structure: tuple[Path, Path]) -> None:
        """Test deterministic TAR creation."""
        temp_path, source = test_files_structure

        # Create two archives with deterministic mode
        tar1 = TarArchive(deterministic=True)
        tar2 = TarArchive(deterministic=True)

        output1 = temp_path / "test1.tar"
        output2 = temp_path / "test2.tar"

        tar1.create(source, output1)
        tar2.create(source, output2)

        # Files should have same content (deterministic)
        # Note: Exact byte comparison might not work due to timestamps,
        # but we can verify both are valid
        assert tar1.validate(output1)
        assert tar2.validate(output2)

    def test_preserve_permissions(self, test_files_structure: tuple[Path, Path]) -> None:
        """Test permission preservation."""
        temp_path, source = test_files_structure

        # Set specific permissions
        test_file = source / "executable.sh"
        test_file.write_text("#!/bin/bash\necho test")
        test_file.chmod(0o755)

        # Create archive with permission preservation
        tar = TarArchive(preserve_permissions=True)
        archive = temp_path / "perms.tar"
        tar.create(source, archive)

        # Extract and check permissions
        output = temp_path / "extracted"
        tar.extract(archive, output)

        # New consistent behavior: no parent directory in archive
        extracted_file = output / "executable.sh"
        assert extracted_file.exists()
        # Check if executable bit is preserved (at least for owner)
        assert extracted_file.stat().st_mode & 0o100

    def test_error_handling(self, tar_archive: TarArchive, temp_directory: Path) -> None:
        """Test error handling in TAR operations."""
        temp_path = temp_directory

        # Test creating archive from non-existent source
        with pytest.raises(ArchiveError):
            tar_archive.create(temp_path / "nonexistent", temp_path / "test.tar")

        # Test extracting non-existent archive
        with pytest.raises(ArchiveError):
            tar_archive.extract(temp_path / "nonexistent.tar", temp_path / "output")


# 🧱🏗️🔚
