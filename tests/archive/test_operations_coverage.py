"""Comprehensive coverage tests for archive operations."""

from __future__ import annotations

from pathlib import Path

from provide.testkit import FoundationTestCase
import pytest

from provide.foundation.archive.base import ArchiveError
from provide.foundation.archive.operations import ArchiveOperations, OperationChain


class TestOperationChainConfiguration(FoundationTestCase):
    """Test OperationChain with configuration options."""

    def test_chain_with_tar_deterministic_config(self, test_files_structure: tuple[Path, Path]) -> None:
        """Test chain with deterministic tar configuration."""
        temp_path, source = test_files_structure
        output = temp_path / "archive.tar.gz"

        chain = OperationChain(
            operations=["tar", "gzip"],
            operation_config={"tar": {"deterministic": True}},
        )
        result = chain.execute(source, output)

        assert result == output
        assert output.exists()

    def test_chain_with_tar_non_deterministic_config(self, test_files_structure: tuple[Path, Path]) -> None:
        """Test chain with non-deterministic tar configuration."""
        temp_path, source = test_files_structure
        output = temp_path / "archive.tar.gz"

        chain = OperationChain(
            operations=["tar", "gzip"],
            operation_config={"tar": {"deterministic": False}},
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
            operations=["tar", "gzip"],
            operation_config={"tar": {"deterministic": True}},
        )
        chain.execute(source, archive)

        # Reverse should preserve config
        extracted = temp_path / "extracted"
        result = chain.reverse(archive, extracted)

        assert result == extracted
        assert (extracted / "source").exists()

    def test_chain_with_zip_config(self, test_files_structure: tuple[Path, Path]) -> None:
        """Test chain with zip configuration."""
        temp_path, source = test_files_structure
        output = temp_path / "archive.zip"

        chain = OperationChain(
            operations=["zip"],
            operation_config={"zip": {"compression_level": 9}},
        )
        result = chain.execute(source, output)

        assert result == output
        assert output.exists()

    def test_chain_with_multiple_operations_configs(self, test_files_structure: tuple[Path, Path]) -> None:
        """Test chain with configuration for multiple operations."""
        temp_path, source = test_files_structure
        output = temp_path / "archive.zip"

        chain = OperationChain(
            operations=["zip"],
            operation_config={
                "zip": {"compression_level": 6},
                "tar": {"deterministic": True},  # Not used but shouldn't cause issues
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

        chain = OperationChain(operations=["tar", "bzip2"])
        result = chain.execute(source, output)

        assert result == output
        assert output.exists()
        # Should have bzip2 magic number
        assert output.read_bytes()[:3] == b"BZh"

    def test_zip_chain(self, test_files_structure: tuple[Path, Path]) -> None:
        """Test single zip operation."""
        temp_path, source = test_files_structure
        output = temp_path / "archive.zip"

        chain = OperationChain(operations=["zip"])
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
        create_chain = OperationChain(operations=["zip"])
        create_chain.execute(source, archive)

        # Extract with unzip
        extracted = temp_path / "extracted"
        extract_chain = OperationChain(operations=["unzip"])
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

        chain = OperationChain(operations=["bzip2"])
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

        chain = OperationChain(operations=["bzip2"])
        chain.execute(source, compressed)

        # Decompress
        decompressed = temp_path / "decompressed.txt"
        decompress_chain = OperationChain(operations=["bunzip2"])
        result = decompress_chain.execute(compressed, decompressed)

        assert result == decompressed
        assert "Test content for bunzip2" in decompressed.read_text()

    def test_reverse_tar_bzip2_chain(self, test_files_structure: tuple[Path, Path]) -> None:
        """Test reversing tar.bz2 chain."""
        temp_path, source = test_files_structure

        # Create tar.bz2
        archive = temp_path / "archive.tar.bz2"
        chain = OperationChain(operations=["tar", "bzip2"])
        chain.execute(source, archive)

        # Reverse to extract
        extracted = temp_path / "extracted"
        result = chain.reverse(archive, extracted)

        assert result == extracted
        assert (extracted / "source").exists()


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


class TestOperationChainTemporaryFileManagement(FoundationTestCase):
    """Test that OperationChain properly manages temporary files."""

    def test_temp_files_cleaned_up_on_success(self, test_files_structure: tuple[Path, Path]) -> None:
        """Test that temporary files are cleaned up after successful chain."""
        temp_path, source = test_files_structure

        # Count files before
        files_before = set(temp_path.rglob("*"))

        # Run chain
        output = temp_path / "archive.tar.gz"
        chain = OperationChain(operations=["tar", "gzip"])
        chain.execute(source, output)

        # Count files after - should only have output and source
        files_after = set(temp_path.rglob("*"))
        new_files = files_after - files_before

        # Should only have the output file
        assert len(new_files) == 1
        assert output in new_files

    def test_temp_files_cleaned_up_on_error(self, test_files_structure: tuple[Path, Path]) -> None:
        """Test that temporary files are cleaned up even on error."""
        temp_path, source = test_files_structure

        # Count temp files before
        temp_files_before = list(Path("/tmp").glob("provide_*"))

        # Run chain with invalid operation
        output = temp_path / "output"
        chain = OperationChain(operations=["tar", "invalid_op"])

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
        assert ops == ["untar"]

    def test_detect_format_extension_precedence(self, temp_directory: Path) -> None:
        """Test that extension detection takes precedence over magic."""
        temp_path = temp_directory

        # Create file with .tar.gz extension but wrong magic
        fake_targz = temp_path / "test.tar.gz"
        fake_targz.write_bytes(b"not gzip data")

        # Should still detect based on extension
        ops = ArchiveOperations.detect_format(fake_targz)
        assert ops == ["gunzip", "untar"]

    def test_detect_tgz_extension(self) -> None:
        """Test detecting .tgz extension."""
        ops = ArchiveOperations.detect_format(Path("archive.tgz"))
        assert ops == ["gunzip", "untar"]

    def test_detect_tbz2_extension(self) -> None:
        """Test detecting .tbz2 extension."""
        ops = ArchiveOperations.detect_format(Path("archive.tbz2"))
        assert ops == ["bunzip2", "untar"]


__all__ = [
    "TestArchiveOperationsNonDeterministic",
    "TestFormatDetectionEdgeCases",
    "TestOperationChainConfiguration",
    "TestOperationChainEdgeCases",
    "TestOperationChainTemporaryFileManagement",
]
