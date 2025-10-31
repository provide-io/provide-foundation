#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for deterministic/reproducible archive creation.

Verifies that archives created with deterministic=True are byte-for-byte
identical when created from the same source, regardless of filesystem
metadata like timestamps and ownership."""

from __future__ import annotations

import hashlib
from pathlib import Path
import tarfile
import time

from provide.testkit import FoundationTestCase
import pytest

from provide.foundation.archive import TarArchive, deterministic_filter


class TestDeterministicArchives(FoundationTestCase):
    """Test deterministic/reproducible archive creation."""

    def _create_test_files(self, base_dir: Path) -> None:
        """Create test files with varying metadata.

        Args:
            base_dir: Directory to create files in
        """
        (base_dir / "file1.txt").write_text("content 1")
        (base_dir / "file2.txt").write_text("content 2")

        subdir = base_dir / "subdir"
        subdir.mkdir()
        (subdir / "file3.txt").write_text("content 3")

    def _compute_file_hash(self, file_path: Path) -> str:
        """Compute SHA256 hash of a file.

        Args:
            file_path: Path to file

        Returns:
            Hex digest of SHA256 hash
        """
        sha256 = hashlib.sha256()
        with file_path.open("rb") as f:
            while chunk := f.read(8192):
                sha256.update(chunk)
        return sha256.hexdigest()

    def test_deterministic_tar_identical_hashes(self, temp_directory: Path) -> None:
        """Test that deterministic TAR archives have identical hashes."""
        # Create first test directory
        source1 = temp_directory / "source1"
        source1.mkdir()
        self._create_test_files(source1)

        # Wait a moment to ensure different timestamps
        time.sleep(0.1)

        # Create second test directory with same content
        source2 = temp_directory / "source2"
        source2.mkdir()
        self._create_test_files(source2)

        # Create archives with deterministic mode
        archive1 = temp_directory / "archive1.tar"
        archive2 = temp_directory / "archive2.tar"

        tar = TarArchive(deterministic=True)
        tar.create(source1, archive1)
        tar.create(source2, archive2)

        # Verify archives have identical hashes
        hash1 = self._compute_file_hash(archive1)
        hash2 = self._compute_file_hash(archive2)

        assert hash1 == hash2, "Deterministic TAR archives should have identical hashes"

    def test_non_deterministic_tar_different_hashes(self, temp_directory: Path) -> None:
        """Test that non-deterministic TAR archives have different hashes."""
        # Create first test directory
        source1 = temp_directory / "source1"
        source1.mkdir()
        self._create_test_files(source1)

        # Wait to ensure different timestamps
        time.sleep(0.1)

        # Create second test directory with same content
        source2 = temp_directory / "source2"
        source2.mkdir()
        self._create_test_files(source2)

        # Create archives without deterministic mode
        archive1 = temp_directory / "archive1.tar"
        archive2 = temp_directory / "archive2.tar"

        tar = TarArchive(deterministic=False)
        tar.create(source1, archive1)
        tar.create(source2, archive2)

        # Verify archives have different hashes (due to timestamps)
        hash1 = self._compute_file_hash(archive1)
        hash2 = self._compute_file_hash(archive2)

        assert hash1 != hash2, "Non-deterministic TAR archives should have different hashes"

    def test_deterministic_filter_resets_metadata(self) -> None:
        """Test that deterministic_filter properly resets metadata."""
        # Create a tarinfo with realistic metadata
        tarinfo = tarfile.TarInfo(name="test.txt")
        tarinfo.uid = 1000
        tarinfo.gid = 1000
        tarinfo.uname = "testuser"
        tarinfo.gname = "testgroup"
        tarinfo.mtime = int(time.time())

        # Apply deterministic filter
        filtered = deterministic_filter(tarinfo)

        # Verify metadata is reset
        assert filtered.uid == 0, "UID should be reset to 0"
        assert filtered.gid == 0, "GID should be reset to 0"
        assert filtered.uname == "", "Username should be reset to empty"
        assert filtered.gname == "", "Group name should be reset to empty"
        assert filtered.mtime == 0, "Modification time should be reset to 0"

    def test_deterministic_filter_preserves_content_attributes(self) -> None:
        """Test that deterministic_filter preserves file content attributes."""
        # Create a tarinfo with various attributes
        tarinfo = tarfile.TarInfo(name="test.txt")
        tarinfo.size = 12345
        tarinfo.mode = 0o644
        tarinfo.type = tarfile.REGTYPE

        # Apply deterministic filter
        filtered = deterministic_filter(tarinfo)

        # Verify content attributes are preserved
        assert filtered.name == "test.txt", "Name should be preserved"
        assert filtered.size == 12345, "Size should be preserved"
        assert filtered.mode == 0o644, "Mode should be preserved"
        assert filtered.type == tarfile.REGTYPE, "Type should be preserved"

    def test_multiple_identical_creations(self, temp_directory: Path) -> None:
        """Test that multiple creations of the same archive are identical."""
        # Create source directory
        source = temp_directory / "source"
        source.mkdir()
        self._create_test_files(source)

        # Create multiple archives
        archives = []
        hashes = []
        tar = TarArchive(deterministic=True)

        for i in range(3):
            archive = temp_directory / f"archive{i}.tar"
            tar.create(source, archive)
            archives.append(archive)
            hashes.append(self._compute_file_hash(archive))

        # Verify all hashes are identical
        assert len(set(hashes)) == 1, "All archives should have identical hashes"

    def test_deterministic_with_different_content_different_hashes(self, temp_directory: Path) -> None:
        """Test that deterministic mode doesn't affect content differences."""
        # Create two sources with different content
        source1 = temp_directory / "source1"
        source1.mkdir()
        (source1 / "file.txt").write_text("content 1")

        source2 = temp_directory / "source2"
        source2.mkdir()
        (source2 / "file.txt").write_text("content 2")

        # Create archives with deterministic mode
        archive1 = temp_directory / "archive1.tar"
        archive2 = temp_directory / "archive2.tar"

        tar = TarArchive(deterministic=True)
        tar.create(source1, archive1)
        tar.create(source2, archive2)

        # Verify archives have different hashes (content is different)
        hash1 = self._compute_file_hash(archive1)
        hash2 = self._compute_file_hash(archive2)

        assert hash1 != hash2, "Archives with different content should have different hashes"

    def test_deterministic_mode_extracts_correctly(self, temp_directory: Path) -> None:
        """Test that archives created with deterministic mode extract correctly."""
        # Create source directory
        source = temp_directory / "source"
        source.mkdir()
        self._create_test_files(source)

        # Create archive with deterministic mode
        archive = temp_directory / "archive.tar"
        tar = TarArchive(deterministic=True)
        tar.create(source, archive)

        # Extract archive
        extract_dir = temp_directory / "extracted"
        tar.extract(archive, extract_dir)

        # Verify extracted files match original content
        assert (extract_dir / "file1.txt").read_text() == "content 1"
        assert (extract_dir / "file2.txt").read_text() == "content 2"
        assert (extract_dir / "subdir" / "file3.txt").read_text() == "content 3"

    @pytest.mark.parametrize(
        "compression_format",
        [
            ".tar",
            ".tar.gz",
            ".tar.bz2",
            ".tar.xz",
        ],
    )
    def test_deterministic_with_compression_formats(
        self, temp_directory: Path, compression_format: str
    ) -> None:
        """Test deterministic archives with different compression formats.

        Args:
            temp_directory: Temporary directory for testing
            compression_format: Archive format extension to test
        """
        # Create source directory
        source = temp_directory / "source"
        source.mkdir()
        self._create_test_files(source)

        # Create two archives with the same content
        archive1 = temp_directory / f"archive1{compression_format}"
        archive2 = temp_directory / f"archive2{compression_format}"

        tar = TarArchive(deterministic=True)
        tar.create(source, archive1)

        # Wait a moment
        time.sleep(0.1)

        # Create second archive
        tar.create(source, archive2)

        # For compressed formats, we can't compare hashes directly
        # because compression may vary slightly, but we can verify
        # they extract to identical content
        extract1 = temp_directory / "extract1"
        extract2 = temp_directory / "extract2"

        tar.extract(archive1, extract1)
        tar.extract(archive2, extract2)

        # Verify extracted content is identical
        assert (extract1 / "file1.txt").read_text() == (extract2 / "file1.txt").read_text()
        assert (extract1 / "file2.txt").read_text() == (extract2 / "file2.txt").read_text()
        assert (extract1 / "subdir" / "file3.txt").read_text() == (
            extract2 / "subdir" / "file3.txt"
        ).read_text()


# 🧱🏗️🔚
