"""Tests for archive operations and chains."""

from pathlib import Path

import pytest

from provide.foundation.archive.operations import (
    ArchiveOperations,
    OperationChain,
)
from provide.foundation.archive.base import ArchiveError


class TestOperationChain:
    """Test operation chain functionality."""

    @pytest.fixture
    def test_file(self, temp_file):
        """Create a test file."""
        return temp_file("Test content for operation chains\n" * 100, ".txt")

    def test_single_operation(self, test_file):
        """Test chain with single operation."""
        output = test_file.with_suffix('.gz')
        
        try:
            chain = OperationChain(operations=['gzip'])
            result = chain.execute(test_file, output)
            
            assert result == output
            assert output.exists()
            assert output.stat().st_size < test_file.stat().st_size
        finally:
            output.unlink(missing_ok=True)

    def test_tar_gzip_chain(self, test_files_structure):
        """Test tar -> gzip chain."""
        temp_path, source = test_files_structure
        
        output = temp_path / "archive.tar.gz"
        
        chain = OperationChain(operations=['tar', 'gzip'])
        result = chain.execute(source, output)
        
        assert result == output
        assert output.exists()
        # Should have gzip magic number
        assert output.read_bytes()[:2] == b'\x1f\x8b'

    def test_reverse_chain(self, temp_directory):
        """Test reversing operation chain for extraction."""
        temp_path = temp_directory
        
        # Create test file
        source = temp_path / "test.txt"
        source.write_text("Test content")
        
        # Compress with chain
        compressed = temp_path / "test.gz"
        chain = OperationChain(operations=['gzip'])
        chain.execute(source, compressed)
        
        # Reverse chain to decompress
        decompressed = temp_path / "decompressed.txt"
        result = chain.reverse(compressed, decompressed)
        
        assert result == decompressed
        assert decompressed.read_text() == "Test content"

    def test_invalid_operation(self, temp_directory):
        """Test chain with invalid operation."""
        temp_path = temp_directory
        source = temp_path / "test.txt"
        source.write_text("test")
        output = temp_path / "output"
        
        chain = OperationChain(operations=['invalid_op'])
        
        with pytest.raises(ArchiveError, match="Unknown operation"):
            chain.execute(source, output)


class TestArchiveOperations:
    """Test archive operations helper class."""

    @pytest.fixture
    def test_dir(self, test_files_structure):
        """Create test directory structure."""
        temp_path, source = test_files_structure
        # Make files larger for compression tests
        (source / "file1.txt").write_text("Content 1" * 100)
        (source / "file2.txt").write_text("Content 2" * 100)
        (source / "subdir" / "file3.txt").write_text("Content 3" * 100)
        return temp_path, source

    def test_create_tar_gz(self, test_dir):
        """Test creating tar.gz archive."""
        temp_path, source = test_dir
        output = temp_path / "archive.tar.gz"
        
        result = ArchiveOperations.create_tar_gz(source, output)
        
        assert result == output
        assert output.exists()
        # Should be compressed
        assert output.stat().st_size > 0
        # Should have gzip magic number
        assert output.read_bytes()[:2] == b'\x1f\x8b'

    def test_extract_tar_gz(self, test_dir):
        """Test extracting tar.gz archive."""
        temp_path, source = test_dir
        archive = temp_path / "archive.tar.gz"
        extracted = temp_path / "extracted"
        
        # Create archive
        ArchiveOperations.create_tar_gz(source, archive)
        
        # Extract it
        result = ArchiveOperations.extract_tar_gz(archive, extracted)
        
        assert result == extracted
        assert (extracted / "source" / "file1.txt").exists()
        assert "Content 1" in (extracted / "source" / "file1.txt").read_text()
        assert (extracted / "source" / "subdir" / "file3.txt").exists()

    def test_create_tar_bz2(self, test_dir):
        """Test creating tar.bz2 archive."""
        temp_path, source = test_dir
        output = temp_path / "archive.tar.bz2"
        
        result = ArchiveOperations.create_tar_bz2(source, output)
        
        assert result == output
        assert output.exists()
        # Should have bzip2 magic number
        assert output.read_bytes()[:3] == b'BZh'

    def test_extract_tar_bz2(self, test_dir):
        """Test extracting tar.bz2 archive."""
        temp_path, source = test_dir
        archive = temp_path / "archive.tar.bz2"
        extracted = temp_path / "extracted"
        
        # Create archive
        ArchiveOperations.create_tar_bz2(source, archive)
        
        # Extract it
        result = ArchiveOperations.extract_tar_bz2(archive, extracted)
        
        assert result == extracted
        assert (extracted / "source" / "file1.txt").exists()
        assert "Content 1" in (extracted / "source" / "file1.txt").read_text()

    def test_detect_format_by_extension(self):
        """Test format detection by file extension."""
        test_cases = [
            ("archive.tar.gz", ['gunzip', 'untar']),
            ("archive.tgz", ['gunzip', 'untar']),
            ("archive.tar.bz2", ['bunzip2', 'untar']),
            ("archive.tbz2", ['bunzip2', 'untar']),
            ("archive.tar", ['untar']),
            ("file.gz", ['gunzip']),
            ("file.bz2", ['bunzip2']),
            ("archive.zip", ['unzip']),
        ]
        
        for filename, expected_ops in test_cases:
            ops = ArchiveOperations.detect_format(Path(filename))
            assert ops == expected_ops

    def test_detect_format_by_magic(self, temp_directory):
        """Test format detection by magic numbers."""
        temp_path = temp_directory
        
        # Create gzip file
        gzip_file = temp_path / "test.dat"
        gzip_file.write_bytes(b'\x1f\x8b' + b'rest of file')
        assert ArchiveOperations.detect_format(gzip_file) == ['gunzip']
        
        # Create bzip2 file
        bz2_file = temp_path / "test2.dat"
        bz2_file.write_bytes(b'BZh' + b'rest of file')
        assert ArchiveOperations.detect_format(bz2_file) == ['bunzip2']
        
        # Create zip file
        zip_file = temp_path / "test3.dat"
        zip_file.write_bytes(b'PK\x03\x04' + b'rest of file')
        assert ArchiveOperations.detect_format(zip_file) == ['unzip']

    def test_detect_unknown_format(self, temp_directory):
        """Test detecting unknown format."""
        temp_path = temp_directory
        
        unknown = temp_path / "unknown.xyz"
        unknown.write_text("unknown format")
        
        with pytest.raises(ArchiveError, match="Cannot detect format"):
            ArchiveOperations.detect_format(unknown)

    def test_deterministic_archives(self, test_dir):
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