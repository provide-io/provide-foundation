"""Tests for ZIP archive implementation."""

import tempfile
from pathlib import Path

import pytest

from provide.foundation.archive.zip import ZipArchive
from provide.foundation.archive.base import ArchiveError


class TestZipArchive:
    """Test ZIP archive functionality."""

    @pytest.fixture
    def zip_archive(self):
        """Create a ZIP archive instance."""
        return ZipArchive()

    @pytest.fixture
    def test_files(self):
        """Create test files in a temporary directory."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            # Create test directory structure
            source = temp_path / "source"
            source.mkdir()
            
            # Create test files
            (source / "file1.txt").write_text("Content 1")
            (source / "file2.txt").write_text("Content 2")
            
            # Create subdirectory with files
            subdir = source / "subdir"
            subdir.mkdir()
            (subdir / "file3.txt").write_text("Content 3")
            
            yield temp_path, source

    def test_create_zip_archive(self, zip_archive, test_files):
        """Test creating a ZIP archive."""
        temp_path, source = test_files
        output = temp_path / "test.zip"
        
        result = zip_archive.create(source, output)
        
        assert result == output
        assert output.exists()
        assert output.stat().st_size > 0

    def test_extract_zip_archive(self, zip_archive, test_files):
        """Test extracting a ZIP archive."""
        temp_path, source = test_files
        archive = temp_path / "test.zip"
        output = temp_path / "extracted"
        
        # Create archive first
        zip_archive.create(source, archive)
        
        # Extract it
        result = zip_archive.extract(archive, output)
        
        assert result == output
        assert output.exists()
        assert (output / "file1.txt").exists()
        assert (output / "file1.txt").read_text() == "Content 1"
        assert (output / "subdir" / "file3.txt").exists()

    def test_validate_zip_archive(self, zip_archive, test_files):
        """Test validating a ZIP archive."""
        temp_path, source = test_files
        archive = temp_path / "test.zip"
        
        # Create valid archive
        zip_archive.create(source, archive)
        assert zip_archive.validate(archive) is True
        
        # Test invalid archive
        invalid = temp_path / "invalid.zip"
        invalid.write_text("not a zip file")
        assert zip_archive.validate(invalid) is False
        
        # Test non-existent file
        assert zip_archive.validate(temp_path / "nonexistent.zip") is False

    def test_add_file_to_archive(self, test_files):
        """Test adding individual files to archive."""
        temp_path, source = test_files
        archive = temp_path / "test.zip"
        
        zip_archive = ZipArchive()
        
        # Create empty archive first
        empty_dir = temp_path / "empty"
        empty_dir.mkdir()
        zip_archive.create(empty_dir, archive)
        
        # Add files one by one
        zip_archive.add_file(archive, source / "file1.txt", "added1.txt")
        zip_archive.add_file(archive, source / "file2.txt", "added2.txt")
        
        # Extract and verify
        output = temp_path / "extracted"
        zip_archive.extract(archive, output)
        
        assert (output / "added1.txt").exists()
        assert (output / "added1.txt").read_text() == "Content 1"
        assert (output / "added2.txt").read_text() == "Content 2"

    def test_extract_single_file(self, test_files):
        """Test extracting a single file from archive."""
        temp_path, source = test_files
        archive = temp_path / "test.zip"
        
        zip_archive = ZipArchive()
        
        # Create archive
        zip_archive.create(source, archive)
        
        # Extract single file
        output_file = temp_path / "single.txt"
        zip_archive.extract_file(archive, "file1.txt", output_file)
        
        assert output_file.exists()
        assert output_file.read_text() == "Content 1"

    def test_compression_levels(self, test_files):
        """Test different compression levels."""
        temp_path, source = test_files
        
        # Create large test file for better compression test
        large_file = source / "large.txt"
        large_file.write_text("Test content for compression\n" * 1000)
        
        # No compression
        zip_stored = ZipArchive(compression_level=0)
        archive_stored = temp_path / "stored.zip"
        zip_stored.create(source, archive_stored)
        
        # Max compression
        zip_compressed = ZipArchive(compression_level=9)
        archive_compressed = temp_path / "compressed.zip"
        zip_compressed.create(source, archive_compressed)
        
        # Compressed should be smaller
        assert archive_compressed.stat().st_size < archive_stored.stat().st_size

    def test_password_protected_archive(self, test_files):
        """Test creating and extracting password-protected archives."""
        temp_path, source = test_files
        
        # Create password-protected archive
        zip_archive = ZipArchive(password=b"secret123")
        archive = temp_path / "protected.zip"
        zip_archive.create(source, archive)
        
        # Extract with correct password
        zip_with_pass = ZipArchive(password=b"secret123")
        output = temp_path / "extracted"
        result = zip_with_pass.extract(archive, output)
        
        assert result == output
        assert (output / "file1.txt").read_text() == "Content 1"
        
        # Try to extract without password - may extract corrupt data
        # Note: Python's zipfile doesn't always raise an error for missing password
        # It may extract corrupted data instead
        zip_no_pass = ZipArchive()
        output2 = temp_path / "extracted2"
        
        try:
            zip_no_pass.extract(archive, output2)
            # If no error, check if data is corrupted
            # (password-protected zips may extract but with corrupted content)
            content = (output2 / "file1.txt").read_text()
            # The content should not match if password was needed
            assert content != "Content 1", "Expected corrupted data without password"
        except (ArchiveError, UnicodeDecodeError):
            # This is expected - either ArchiveError or corrupted data
            pass

    def test_error_handling(self, zip_archive):
        """Test error handling in ZIP operations."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            # Test creating archive from non-existent source
            with pytest.raises(ArchiveError):
                zip_archive.create(temp_path / "nonexistent", temp_path / "test.zip")
            
            # Test extracting non-existent archive
            with pytest.raises(ArchiveError):
                zip_archive.extract(temp_path / "nonexistent.zip", temp_path / "output")
            
            # Test extracting non-existent file from archive
            test_archive = temp_path / "test.zip"
            empty_dir = temp_path / "empty"
            empty_dir.mkdir()
            zip_archive.create(empty_dir, test_archive)
            
            with pytest.raises(ArchiveError):
                zip_archive.extract_file(test_archive, "nonexistent.txt", temp_path / "out.txt")