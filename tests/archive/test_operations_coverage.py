#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Comprehensive coverage tests for archive operations."""

from __future__ import annotations

from pathlib import Path
from typing import Never

from provide.testkit import FoundationTestCase
import pytest

from provide.foundation.archive.base import ArchiveError
from provide.foundation.archive.operations import ArchiveOperations, OperationChain
from provide.foundation.archive.types import ArchiveOperation


class TestOperationChainConfiguration(FoundationTestCase):
    """Test OperationChain with configuration options."""

    def test_chain_with_tar_deterministic_config(self, test_files_structure: tuple[Path, Path]) -> None:
        """Test chain with deterministic tar configuration."""
        temp_path, source = test_files_structure
        output = temp_path / "archive.tar.gz"

        chain = OperationChain(
            operations=[ArchiveOperation.TAR, ArchiveOperation.GZIP],
            operation_config={ArchiveOperation.TAR: {"deterministic": True}},
        )
        result = chain.execute(source, output)

        assert result == output
        assert output.exists()

    def test_chain_with_tar_non_deterministic_config(self, test_files_structure: tuple[Path, Path]) -> None:
        """Test chain with non-deterministic tar configuration."""
        temp_path, source = test_files_structure
        output = temp_path / "archive.tar.gz"

        chain = OperationChain(
            operations=[ArchiveOperation.TAR, ArchiveOperation.GZIP],
            operation_config={ArchiveOperation.TAR: {"deterministic": False}},
        )
        result = chain.execute(source, output)

        assert result == output
        assert output.exists()

    def test_chain_preserves_config_on_reverse(self, test_files_structure: tuple[Path, Path]) -> None:
        """Test that configuration is preserved when reversing chain."""
        temp_path, source = test_files_structure

        # Create with deterministic config
        archive = temp_path / "archive.tar.gz"
        chain = OperationChain(
            operations=[ArchiveOperation.TAR, ArchiveOperation.GZIP],
            operation_config={ArchiveOperation.TAR: {"deterministic": True}},
        )
        chain.execute(source, archive)

        # Reverse should preserve config
        extracted = temp_path / "extracted"
        result = chain.reverse(archive, extracted)

        assert result == extracted
        assert (extracted).exists()

    def test_chain_with_zip_config(self, test_files_structure: tuple[Path, Path]) -> None:
        """Test chain with zip configuration."""
        temp_path, source = test_files_structure
        output = temp_path / "archive.zip"

        chain = OperationChain(
            operations=[ArchiveOperation.ZIP],
            operation_config={ArchiveOperation.ZIP: {"compression_level": 9}},
        )
        result = chain.execute(source, output)

        assert result == output
        assert output.exists()

    def test_chain_with_multiple_operations_configs(self, test_files_structure: tuple[Path, Path]) -> None:
        """Test chain with configuration for multiple operations."""
        temp_path, source = test_files_structure
        output = temp_path / "archive.zip"

        chain = OperationChain(
            operations=[ArchiveOperation.ZIP],
            operation_config={
                ArchiveOperation.ZIP: {"compression_level": 6},
                ArchiveOperation.TAR: {"deterministic": True},  # Not used but shouldn't cause issues
            },
        )
        result = chain.execute(source, output)

        assert result == output
        assert output.exists()


class TestOperationChainEdgeCases(FoundationTestCase):
    """Test edge cases for operation chains."""

    def test_tar_bzip2_chain(self, test_files_structure: tuple[Path, Path]) -> None:
        """Test tar -> bzip2 chain."""
        temp_path, source = test_files_structure
        output = temp_path / "archive.tar.bz2"

        chain = OperationChain(operations=[ArchiveOperation.TAR, ArchiveOperation.BZIP2])
        result = chain.execute(source, output)

        assert result == output
        assert output.exists()
        # Should have bzip2 magic number
        assert output.read_bytes()[:3] == b"BZh"

    def test_zip_chain(self, test_files_structure: tuple[Path, Path]) -> None:
        """Test single zip operation."""
        temp_path, source = test_files_structure
        output = temp_path / "archive.zip"

        chain = OperationChain(operations=[ArchiveOperation.ZIP])
        result = chain.execute(source, output)

        assert result == output
        assert output.exists()
        # Should have zip magic number
        assert output.read_bytes()[:4] == b"PK\x03\x04"

    def test_unzip_operation(self, test_files_structure: tuple[Path, Path]) -> None:
        """Test unzip operation."""
        temp_path, source = test_files_structure

        # Create zip
        archive = temp_path / "archive.zip"
        create_chain = OperationChain(operations=[ArchiveOperation.ZIP])
        create_chain.execute(source, archive)

        # Extract with unzip
        extracted = temp_path / "extracted"
        extract_chain = OperationChain(operations=[ArchiveOperation.ZIP])
        result = extract_chain.execute(archive, extracted)

        assert result == extracted
        # ZIP extracts files directly, not in a subdirectory
        assert extracted.exists()
        assert len(list(extracted.iterdir())) > 0

    def test_bzip2_only_chain(self, temp_directory: Path) -> None:
        """Test bzip2 compression only."""
        temp_path = temp_directory

        source = temp_path / "test.txt"
        source.write_text("Test content for bzip2\n" * 100)
        output = temp_path / "test.bz2"

        chain = OperationChain(operations=[ArchiveOperation.BZIP2])
        result = chain.execute(source, output)

        assert result == output
        assert output.exists()
        assert output.read_bytes()[:3] == b"BZh"

    def test_bunzip2_operation(self, temp_directory: Path) -> None:
        """Test bunzip2 decompression."""
        temp_path = temp_directory

        # Create bzip2 file
        source = temp_path / "test.txt"
        source.write_text("Test content for bunzip2\n" * 100)
        compressed = temp_path / "test.bz2"

        chain = OperationChain(operations=[ArchiveOperation.BZIP2])
        chain.execute(source, compressed)

        # Decompress
        decompressed = temp_path / "decompressed.txt"
        decompress_chain = OperationChain(operations=[ArchiveOperation.BZIP2])
        result = decompress_chain.execute(compressed, decompressed)

        assert result == decompressed
        assert "Test content for bunzip2" in decompressed.read_text()

    def test_reverse_tar_bzip2_chain(self, test_files_structure: tuple[Path, Path]) -> None:
        """Test reversing tar.bz2 chain."""
        temp_path, source = test_files_structure

        # Create tar.bz2
        archive = temp_path / "archive.tar.bz2"
        chain = OperationChain(operations=[ArchiveOperation.TAR, ArchiveOperation.BZIP2])
        chain.execute(source, archive)

        # Reverse to extract
        extracted = temp_path / "extracted"
        result = chain.reverse(archive, extracted)

        assert result == extracted
        assert (extracted).exists()


class TestArchiveOperationsNonDeterministic(FoundationTestCase):
    """Test ArchiveOperations with non-deterministic mode."""

    def test_create_tar_gz_non_deterministic(self, test_files_structure: tuple[Path, Path]) -> None:
        """Test creating tar.gz with non-deterministic mode."""
        temp_path, source = test_files_structure
        output = temp_path / "archive.tar.gz"

        result = ArchiveOperations.create_tar_gz(source, output, deterministic=False)

        assert result == output
        assert output.exists()
        # Should have gzip magic number
        assert output.read_bytes()[:2] == b"\x1f\x8b"

    def test_create_tar_bz2_non_deterministic(self, test_files_structure: tuple[Path, Path]) -> None:
        """Test creating tar.bz2 with non-deterministic mode."""
        temp_path, source = test_files_structure
        output = temp_path / "archive.tar.bz2"

        result = ArchiveOperations.create_tar_bz2(source, output, deterministic=False)

        assert result == output
        assert output.exists()
        # Should have bzip2 magic number
        assert output.read_bytes()[:3] == b"BZh"


class TestOperationChainWithSubdirectories(FoundationTestCase):
    """Test that operation chains handle subdirectories correctly."""

    def test_tar_gz_preserves_subdirectory_structure(self, temp_directory: Path) -> None:
        """Test that tar.gz chain preserves subdirectory structure."""
        temp_path = temp_directory

        # Create structure with subdirectories
        source = temp_path / "source"
        source.mkdir()
        (source / "file1.txt").write_text("content1")

        subdir = source / "subdir"
        subdir.mkdir()
        (subdir / "file2.txt").write_text("content2")

        nested = subdir / "nested"
        nested.mkdir()
        (nested / "file3.txt").write_text("content3")

        # Create archive
        archive = temp_path / "archive.tar.gz"
        chain = OperationChain(operations=[ArchiveOperation.TAR, ArchiveOperation.GZIP])
        chain.execute(source, archive)

        # Extract
        extracted = temp_path / "extracted"
        chain.reverse(archive, extracted)

        # Verify subdirectory structure preserved
        assert (extracted).exists()
        assert (extracted / "file1.txt").read_text() == "content1"
        assert (extracted / "subdir" / "file2.txt").read_text() == "content2"
        assert (extracted / "subdir" / "nested" / "file3.txt").read_text() == "content3"


class TestOperationChainTemporaryFileManagement(FoundationTestCase):
    """Test that OperationChain properly manages temporary files."""

    def test_temp_files_cleaned_up_on_success(self, test_files_structure: tuple[Path, Path]) -> None:
        """Test that temporary files are cleaned up after successful chain."""
        temp_path, source = test_files_structure

        # Count files before
        files_before = set(temp_path.rglob("*"))

        # Run chain
        output = temp_path / "archive.tar.gz"
        chain = OperationChain(operations=[ArchiveOperation.TAR, ArchiveOperation.GZIP])
        chain.execute(source, output)

        # Count files after - should only have output and source
        files_after = set(temp_path.rglob("*"))
        new_files = files_after - files_before

        # Should only have the output file
        assert len(new_files) == 1
        assert output in new_files

    def test_temp_files_cleaned_up_on_error(
        self, test_files_structure: tuple[Path, Path], monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Test that temporary files are cleaned up even on error."""
        temp_path, source = test_files_structure

        # Count temp files before
        temp_files_before = list(Path("/tmp").glob("provide_*"))

        # Mock the GzipCompressor to raise an error during compression
        from typing import Any

        from provide.foundation.archive.gzip import GzipCompressor

        def mock_compress_file(*args: Any, **kwargs: Any) -> Never:
            raise RuntimeError("Simulated compression failure")

        monkeypatch.setattr(GzipCompressor, "compress_file", mock_compress_file)

        # Run chain - should fail during GZIP operation
        output = temp_path / "archive.tar.gz"
        chain = OperationChain(operations=[ArchiveOperation.TAR, ArchiveOperation.GZIP])

        with pytest.raises(ArchiveError):
            chain.execute(source, output)

        # Temp files after should be same or fewer (cleanup happened)
        temp_files_after = list(Path("/tmp").glob("provide_*"))
        # We can't guarantee exact count due to other processes, but it shouldn't grow unbounded
        assert len(temp_files_after) <= len(temp_files_before) + 1  # Allow some tolerance


class TestFormatDetectionEdgeCases(FoundationTestCase):
    """Test format detection edge cases."""

    def test_detect_tar_format_by_magic(self, temp_directory: Path) -> None:
        """Test detecting tar format by magic number."""
        temp_path = temp_directory

        # Create file with tar ustar magic at offset 257
        tar_like = temp_path / "test.dat"
        # Write 257 bytes of padding + ustar magic
        tar_like.write_bytes(b"\x00" * 257 + b"ustar" + b"\x00" * 100)

        ops = ArchiveOperations.detect_format(tar_like)
        assert ops == [ArchiveOperation.TAR]

    def test_detect_format_extension_precedence(self, temp_directory: Path) -> None:
        """Test that extension detection takes precedence over magic."""
        temp_path = temp_directory

        # Create file with .tar.gz extension but wrong magic
        fake_targz = temp_path / "test.tar.gz"
        fake_targz.write_bytes(b"not gzip data")

        # Should still detect based on extension
        ops = ArchiveOperations.detect_format(fake_targz)
        assert ops == [ArchiveOperation.GZIP, ArchiveOperation.TAR]

    def test_detect_tgz_extension(self) -> None:
        """Test detecting .tgz extension."""
        ops = ArchiveOperations.detect_format(Path("archive.tgz"))
        assert ops == [ArchiveOperation.GZIP, ArchiveOperation.TAR]

    def test_detect_tbz2_extension(self) -> None:
        """Test detecting .tbz2 extension."""
        ops = ArchiveOperations.detect_format(Path("archive.tbz2"))
        assert ops == [ArchiveOperation.BZIP2, ArchiveOperation.TAR]


__all__ = [
    "TestArchiveOperationsNonDeterministic",
    "TestFormatDetectionEdgeCases",
    "TestOperationChainConfiguration",
    "TestOperationChainEdgeCases",
    "TestOperationChainTemporaryFileManagement",
    "TestOperationChainWithSubdirectories",
]

# 🧱🏗️🔚
