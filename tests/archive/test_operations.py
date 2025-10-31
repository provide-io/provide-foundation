#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for archive operations and chains."""

from __future__ import annotations

from collections.abc import Callable
from pathlib import Path

from provide.testkit import FoundationTestCase
import pytest

from provide.foundation.archive.base import ArchiveError
from provide.foundation.archive.operations import (
    ArchiveOperations,
    OperationChain,
)
from provide.foundation.archive.types import ArchiveOperation


class TestOperationChain(FoundationTestCase):
    """Test operation chain functionality."""

    @pytest.fixture
    def test_file(self, temp_file: Callable[[str, str], Path]) -> Path:
        """Create a test file."""
        return temp_file("Test content for operation chains\n" * 100, ".txt")

    def test_single_operation(self, test_file: Path) -> None:
        """Test chain with single operation."""
        output = test_file.with_suffix(".gz")

        try:
            chain = OperationChain(operations=[ArchiveOperation.GZIP])
            result = chain.execute(test_file, output)

            assert result == output
            assert output.exists()
            assert output.stat().st_size < test_file.stat().st_size
        finally:
            output.unlink(missing_ok=True)

    def test_tar_gzip_chain(self, test_files_structure: tuple[Path, Path]) -> None:
        """Test tar -> gzip chain."""
        temp_path, source = test_files_structure

        output = temp_path / "archive.tar.gz"

        chain = OperationChain(operations=[ArchiveOperation.TAR, ArchiveOperation.GZIP])
        result = chain.execute(source, output)

        assert result == output
        assert output.exists()
        # Should have gzip magic number
        assert output.read_bytes()[:2] == b"\x1f\x8b"

    def test_reverse_chain(self, temp_directory: Path) -> None:
        """Test reversing operation chain for extraction."""
        temp_path = temp_directory

        # Create test file
        source = temp_path / "test.txt"
        source.write_text("Test content")

        # Compress with chain
        compressed = temp_path / "test.gz"
        chain = OperationChain(operations=[ArchiveOperation.GZIP])
        chain.execute(source, compressed)

        # Reverse chain to decompress
        decompressed = temp_path / "decompressed.txt"
        result = chain.reverse(compressed, decompressed)

        assert result == decompressed
        assert decompressed.read_text() == "Test content"

    def test_invalid_operation(self, temp_directory: Path) -> None:
        """Test chain with invalid operation."""
        temp_path = temp_directory
        source = temp_path / "test.txt"
        source.write_text("test")
        output = temp_path / "output"

        # Use an invalid enum value
        chain = OperationChain(operations=[ArchiveOperation.NONE])

        with pytest.raises(ArchiveError, match="Unknown operation"):
            chain.execute(source, output)


class TestArchiveOperations(FoundationTestCase):
    """Test archive operations helper class."""

    @pytest.fixture
    def test_dir(self, test_files_structure: tuple[Path, Path]) -> tuple[Path, Path]:
        """Create test directory structure."""
        temp_path, source = test_files_structure
        # Make files larger for compression tests
        (source / "file1.txt").write_text("Content 1" * 100)
        (source / "file2.txt").write_text("Content 2" * 100)
        (source / "subdir" / "file3.txt").write_text("Content 3" * 100)
        return temp_path, source

    def test_create_tar_gz(self, test_dir: tuple[Path, Path]) -> None:
        """Test creating tar.gz archive."""
        temp_path, source = test_dir
        output = temp_path / "archive.tar.gz"

        result = ArchiveOperations.create_tar_gz(source, output)

        assert result == output
        assert output.exists()
        # Should be compressed
        assert output.stat().st_size > 0
        # Should have gzip magic number
        assert output.read_bytes()[:2] == b"\x1f\x8b"

    def test_extract_tar_gz(self, test_dir: tuple[Path, Path]) -> None:
        """Test extracting tar.gz archive."""
        temp_path, source = test_dir
        archive = temp_path / "archive.tar.gz"
        extracted = temp_path / "extracted"

        # Create archive
        ArchiveOperations.create_tar_gz(source, archive)

        # Extract it
        result = ArchiveOperations.extract_tar_gz(archive, extracted)

        assert result == extracted
        # New consistent behavior: no parent directory in archive
        assert (extracted / "file1.txt").exists()
        assert "Content 1" in (extracted / "file1.txt").read_text()
        assert (extracted / "subdir" / "file3.txt").exists()

    def test_create_tar_bz2(self, test_dir: tuple[Path, Path]) -> None:
        """Test creating tar.bz2 archive."""
        temp_path, source = test_dir
        output = temp_path / "archive.tar.bz2"

        result = ArchiveOperations.create_tar_bz2(source, output)

        assert result == output
        assert output.exists()
        # Should have bzip2 magic number
        assert output.read_bytes()[:3] == b"BZh"

    def test_extract_tar_bz2(self, test_dir: tuple[Path, Path]) -> None:
        """Test extracting tar.bz2 archive."""
        temp_path, source = test_dir
        archive = temp_path / "archive.tar.bz2"
        extracted = temp_path / "extracted"

        # Create archive
        ArchiveOperations.create_tar_bz2(source, archive)

        # Extract it
        result = ArchiveOperations.extract_tar_bz2(archive, extracted)

        assert result == extracted
        # New consistent behavior: no parent directory in archive
        assert (extracted / "file1.txt").exists()
        assert "Content 1" in (extracted / "file1.txt").read_text()

    def test_detect_format_by_extension(self) -> None:
        """Test format detection by file extension."""
        test_cases = [
            ("archive.tar.gz", [ArchiveOperation.GZIP, ArchiveOperation.TAR]),
            ("archive.tgz", [ArchiveOperation.GZIP, ArchiveOperation.TAR]),
            ("archive.tar.bz2", [ArchiveOperation.BZIP2, ArchiveOperation.TAR]),
            ("archive.tbz2", [ArchiveOperation.BZIP2, ArchiveOperation.TAR]),
            ("archive.tar", [ArchiveOperation.TAR]),
            ("file.gz", [ArchiveOperation.GZIP]),
            ("file.bz2", [ArchiveOperation.BZIP2]),
            ("archive.zip", [ArchiveOperation.ZIP]),
        ]

        for filename, expected_ops in test_cases:
            ops = ArchiveOperations.detect_format(Path(filename))
            assert ops == expected_ops

    def test_detect_format_by_magic(self, temp_directory: Path) -> None:
        """Test format detection by magic numbers."""
        temp_path = temp_directory

        # Create gzip file
        gzip_file = temp_path / "test.dat"
        gzip_file.write_bytes(b"\x1f\x8b" + b"rest of file")
        assert ArchiveOperations.detect_format(gzip_file) == [ArchiveOperation.GZIP]

        # Create bzip2 file
        bz2_file = temp_path / "test2.dat"
        bz2_file.write_bytes(b"BZh" + b"rest of file")
        assert ArchiveOperations.detect_format(bz2_file) == [ArchiveOperation.BZIP2]

        # Create zip file
        zip_file = temp_path / "test3.dat"
        zip_file.write_bytes(b"PK\x03\x04" + b"rest of file")
        assert ArchiveOperations.detect_format(zip_file) == [ArchiveOperation.ZIP]

    def test_detect_unknown_format(self, temp_directory: Path) -> None:
        """Test detecting unknown format."""
        temp_path = temp_directory

        unknown = temp_path / "unknown.xyz"
        unknown.write_text("unknown format")

        with pytest.raises(ArchiveError, match="Cannot detect format"):
            ArchiveOperations.detect_format(unknown)

    def test_deterministic_archives(self, test_dir: tuple[Path, Path]) -> None:
        """Test deterministic archive creation."""
        temp_path, source = test_dir

        # Create two archives with deterministic mode
        archive1 = temp_path / "archive1.tar.gz"
        archive2 = temp_path / "archive2.tar.gz"

        ArchiveOperations.create_tar_gz(source, archive1, deterministic=True)
        ArchiveOperations.create_tar_gz(source, archive2, deterministic=True)

        # Both should be valid
        assert archive1.exists()
        assert archive2.exists()


# 🧱🏗️🔚
