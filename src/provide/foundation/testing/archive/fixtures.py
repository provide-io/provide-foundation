"""
Archive Testing Fixtures.

Fixtures specific to testing archive operations like tar, zip, gzip, bzip2.
Builds on top of file fixtures for archive-specific test scenarios.
"""

from pathlib import Path
from collections.abc import Generator

import pytest

from provide.foundation.testing.file.fixtures import temp_directory


@pytest.fixture
def archive_test_content() -> Generator[tuple[Path, dict[str, str]], None, None]:
    """
    Create a standard set of files for archive testing.
    
    Creates multiple files with different types of content to ensure
    proper compression and extraction testing.
    
    Yields:
        Tuple of (source_dir, content_map) where content_map maps
        relative paths to their expected content.
    """
    with temp_directory() as temp_dir:
        source = temp_dir / "archive_source"
        source.mkdir()
        
        content_map = {
            "text_file.txt": "This is a text file for archive testing.\n" * 10,
            "data.json": '{"test": "data", "array": [1, 2, 3]}',
            "script.py": "#!/usr/bin/env python\nprint('Hello from archive')\n",
            "nested/dir/file.md": "# Nested File\nContent in nested directory",
            "binary.dat": "Binary\x00\x01\x02\x03\xFF\xFE data",
            "empty.txt": "",
        }
        
        # Create all files
        for rel_path, content in content_map.items():
            file_path = source / rel_path
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
            if isinstance(content, str):
                file_path.write_text(content)
            else:
                file_path.write_bytes(content.encode() if isinstance(content, str) else content)
        
        yield source, content_map


@pytest.fixture
def large_file_for_compression() -> Generator[Path, None, None]:
    """
    Create a large file suitable for compression testing.
    
    The file contains repetitive content that compresses well.
    
    Yields:
        Path to a large file with compressible content.
    """
    with temp_directory() as temp_dir:
        large_file = temp_dir / "large_compressible.txt"
        
        # Create 10MB of highly compressible content
        content = "This is a line of text that will be repeated many times.\n" * 100
        large_content = content * 1000  # ~6MB of repetitive text
        
        large_file.write_text(large_content)
        yield large_file


@pytest.fixture
def multi_format_archives() -> Generator[dict[str, Path], None, None]:
    """
    Create sample archives in different formats for format detection testing.
    
    Yields:
        Dict mapping format names to paths of sample archives.
    """
    with temp_directory() as temp_dir:
        archives = {}
        
        # Create minimal valid archives in different formats
        # Note: These are minimal headers, not full valid archives
        
        # GZIP file (magic: 1f 8b)
        gzip_file = temp_dir / "sample.gz"
        gzip_file.write_bytes(b'\x1f\x8b\x08\x00\x00\x00\x00\x00\x00\x03' + b'compressed data')
        archives["gzip"] = gzip_file
        
        # BZIP2 file (magic: BZh)
        bzip2_file = temp_dir / "sample.bz2"
        bzip2_file.write_bytes(b'BZh91AY&SY' + b'compressed data')
        archives["bzip2"] = bzip2_file
        
        # ZIP file (magic: PK\x03\x04)
        zip_file = temp_dir / "sample.zip"
        zip_file.write_bytes(b'PK\x03\x04' + b'\x00' * 16 + b'zipfile')
        archives["zip"] = zip_file
        
        # TAR file (has specific header structure)
        tar_file = temp_dir / "sample.tar"
        # Minimal tar header (512 bytes)
        tar_header = b'testfile.txt' + b'\x00' * 88  # name
        tar_header += b'0000644\x00'  # mode
        tar_header += b'0000000\x00'  # uid
        tar_header += b'0000000\x00'  # gid
        tar_header += b'00000000000\x00'  # size
        tar_header += b'00000000000\x00'  # mtime
        tar_header += b'        '  # checksum placeholder
        tar_header += b'0'  # typeflag
        tar_header += b'\x00' * 355  # padding to 512 bytes
        tar_file.write_bytes(tar_header[:512])
        archives["tar"] = tar_file
        
        yield archives


@pytest.fixture
def archive_with_permissions() -> Generator[Path, None, None]:
    """
    Create files with specific permissions for archive permission testing.
    
    Yields:
        Path to directory containing files with various permission modes.
    """
    with temp_directory() as temp_dir:
        source = temp_dir / "permissions_test"
        source.mkdir()
        
        # Regular file
        regular = source / "regular.txt"
        regular.write_text("Regular file")
        regular.chmod(0o644)
        
        # Executable file
        executable = source / "script.sh"
        executable.write_text("#!/bin/bash\necho 'Hello'")
        executable.chmod(0o755)
        
        # Read-only file
        readonly = source / "readonly.txt"
        readonly.write_text("Read only content")
        readonly.chmod(0o444)
        
        # Directory with specific permissions
        special_dir = source / "special"
        special_dir.mkdir()
        special_dir.chmod(0o700)
        
        yield source


@pytest.fixture
def corrupted_archives() -> Generator[dict[str, Path], None, None]:
    """
    Create corrupted archive files for error handling testing.
    
    Yields:
        Dict mapping format names to paths of corrupted archives.
    """
    with temp_directory() as temp_dir:
        corrupted = {}
        
        # Corrupted GZIP (invalid header)
        bad_gzip = temp_dir / "corrupted.gz"
        bad_gzip.write_bytes(b'\x1f\x8c' + b'not really gzip data')
        corrupted["gzip"] = bad_gzip
        
        # Corrupted ZIP (incomplete header)
        bad_zip = temp_dir / "corrupted.zip"
        bad_zip.write_bytes(b'PK\x03')  # Incomplete magic
        corrupted["zip"] = bad_zip
        
        # Corrupted BZIP2 (wrong magic)
        bad_bzip2 = temp_dir / "corrupted.bz2"
        bad_bzip2.write_bytes(b'BZX' + b'not bzip2')
        corrupted["bzip2"] = bad_bzip2
        
        # Empty file claiming to be archive
        empty_archive = temp_dir / "empty.tar.gz"
        empty_archive.write_bytes(b'')
        corrupted["empty"] = empty_archive
        
        yield corrupted


@pytest.fixture
def archive_stress_test_files() -> Generator[Path, None, None]:
    """
    Create a large number of files for stress testing archive operations.
    
    Yields:
        Path to directory with many files for stress testing.
    """
    with temp_directory() as temp_dir:
        stress_dir = temp_dir / "stress_test"
        stress_dir.mkdir()
        
        # Create 100 files in various subdirectories
        for i in range(10):
            subdir = stress_dir / f"subdir_{i}"
            subdir.mkdir()
            
            for j in range(10):
                file_path = subdir / f"file_{j}.txt"
                file_path.write_text(f"Content of file {i}_{j}\n" * 10)
        
        # Add some binary files
        for i in range(5):
            bin_file = stress_dir / f"binary_{i}.dat"
            bin_file.write_bytes(bytes(range(256)) * 10)
        
        yield stress_dir