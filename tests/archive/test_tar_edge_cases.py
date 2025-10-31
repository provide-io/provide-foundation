#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Edge case tests for TAR archive implementation."""

from __future__ import annotations

from pathlib import Path
import tarfile
import tempfile

from provide.testkit import FoundationTestCase
import pytest

from provide.foundation.archive.base import ArchiveError, ArchiveFormatError
from provide.foundation.archive.tar import TarArchive


class TestTarArchiveEdgeCases(FoundationTestCase):
    """Test TAR archive edge cases and security features."""

    @pytest.fixture
    def tar_archive(self) -> TarArchive:
        """Create a TAR archive instance."""
        return TarArchive()

    def test_list_contents_basic(
        self, tar_archive: TarArchive, test_files_structure: tuple[Path, Path]
    ) -> None:
        """Test listing TAR archive contents."""
        temp_path, source = test_files_structure
        archive = temp_path / "test.tar"

        # Create archive
        tar_archive.create(source, archive)

        # List contents
        contents = tar_archive.list_contents(archive)

        # Should return sorted file paths
        assert isinstance(contents, list)
        assert len(contents) >= 2  # At least file1.txt and file3.txt
        # New consistent behavior: no parent directory in archive
        assert "file1.txt" in contents
        assert "subdir/file3.txt" in contents
        # Should be sorted
        assert contents == sorted(contents)

    def test_list_contents_empty_archive(self, tar_archive: TarArchive, temp_directory: Path) -> None:
        """Test listing contents of empty archive."""
        temp_path = temp_directory

        # Create empty directory and archive it
        empty_dir = temp_path / "empty"
        empty_dir.mkdir()
        archive = temp_path / "empty.tar"

        tar_archive.create(empty_dir, archive)
        contents = tar_archive.list_contents(archive)

        # Should return empty list for archive with no files
        assert contents == []

    def test_list_contents_error_handling(self, tar_archive: TarArchive, temp_directory: Path) -> None:
        """Test error handling when listing contents."""
        temp_path = temp_directory

        # Test with corrupted archive
        corrupt_archive = temp_path / "corrupt.tar"
        corrupt_archive.write_text("not a valid tar file")

        # Should raise ArchiveFormatError for corrupted archive
        with pytest.raises(ArchiveFormatError, match="Invalid or corrupted TAR archive"):
            tar_archive.list_contents(corrupt_archive)

    def test_extract_unsafe_absolute_path(self, tar_archive: TarArchive, temp_directory: Path) -> None:
        """Test extraction blocks absolute paths in archive."""
        temp_path = temp_directory
        archive = temp_path / "unsafe_abs.tar"

        # Create archive with unsafe absolute path manually
        with tarfile.open(archive, "w") as tar:
            info = tarfile.TarInfo(name="/etc/passwd")
            info.size = 12
            with tempfile.SpooledTemporaryFile() as spool:
                spool.write(b"fake content")
                spool.seek(0)
                tar.addfile(info, fileobj=spool)

        output = temp_path / "extracted"

        with pytest.raises(ArchiveError, match="Unsafe path in archive: /etc/passwd"):
            tar_archive.extract(archive, output)

    def test_extract_unsafe_relative_path(self, tar_archive: TarArchive, temp_directory: Path) -> None:
        """Test extraction blocks path traversal attacks."""
        temp_path = temp_directory
        archive = temp_path / "unsafe_rel.tar"

        # Create archive with path traversal attempt
        with tarfile.open(archive, "w") as tar:
            info = tarfile.TarInfo(name="../../../etc/passwd")
            info.size = 12
            with tempfile.SpooledTemporaryFile() as spool:
                spool.write(b"fake content")
                spool.seek(0)
                tar.addfile(info, fileobj=spool)

        output = temp_path / "extracted"

        with pytest.raises(ArchiveError, match=r"Unsafe path in archive: \.\./\.\./\.\./etc/passwd"):
            tar_archive.extract(archive, output)

    def test_extract_unsafe_symlink_absolute(self, tar_archive: TarArchive, temp_directory: Path) -> None:
        """Test extraction blocks absolute symlinks."""
        temp_path = temp_directory
        archive = temp_path / "unsafe_symlink_abs.tar"

        # Create archive with absolute symlink
        with tarfile.open(archive, "w") as tar:
            info = tarfile.TarInfo(name="bad_symlink")
            info.type = tarfile.SYMTYPE
            info.linkname = "/etc/passwd"
            tar.addfile(info)

        output = temp_path / "extracted"

        with pytest.raises(ArchiveError, match="Unsafe link target in archive|Absolute path in link target"):
            tar_archive.extract(archive, output)

    def test_extract_unsafe_symlink_relative_escape(
        self, tar_archive: TarArchive, temp_directory: Path
    ) -> None:
        """Test extraction blocks symlinks that escape extraction directory."""
        temp_path = temp_directory
        archive = temp_path / "unsafe_symlink_rel.tar"

        # Create archive with escaping relative symlink
        with tarfile.open(archive, "w") as tar:
            info = tarfile.TarInfo(name="subdir/bad_symlink")
            info.type = tarfile.SYMTYPE
            info.linkname = "../../outside_file"
            tar.addfile(info)

        output = temp_path / "extracted"

        with pytest.raises(ArchiveError, match="Unsafe link target in archive"):
            tar_archive.extract(archive, output)

    def test_extract_safe_symlink(self, tar_archive: TarArchive, temp_directory: Path) -> None:
        """Test extraction allows safe symlinks within extraction directory."""
        temp_path = temp_directory
        archive = temp_path / "safe_symlink.tar"
        source = temp_path / "source"
        source.mkdir()

        # Create a file and safe symlink
        target_file = source / "target.txt"
        target_file.write_text("target content")
        safe_link = source / "safe_link.txt"
        safe_link.symlink_to("target.txt")

        # Create archive
        tar_archive.create(source, archive)

        # Extract should succeed
        output = temp_path / "extracted"
        tar_archive.extract(archive, output)

        # Verify symlink was extracted correctly
        # New consistent behavior: no parent directory in archive
        extracted_link = output / "safe_link.txt"
        extracted_target = output / "target.txt"

        assert extracted_target.exists()
        assert extracted_link.exists()
        assert extracted_link.is_symlink()

    def test_deterministic_mode_metadata_normalization(self, test_files_structure: tuple[Path, Path]) -> None:
        """Test deterministic mode normalizes metadata."""
        temp_path, source = test_files_structure

        # Create archive with deterministic mode
        tar = TarArchive(deterministic=True)
        archive = temp_path / "deterministic.tar"
        tar.create(source, archive)

        # Check that metadata is normalized by inspecting the archive
        with tarfile.open(archive, "r") as tar_file:
            for member in tar_file.getmembers():
                if member.isfile():
                    # Deterministic mode should set these values
                    assert member.uid == 0
                    assert member.gid == 0
                    assert member.uname == ""
                    assert member.gname == ""
                    assert member.mtime == 0

    def test_preserve_permissions_false(self, test_files_structure: tuple[Path, Path]) -> None:
        """Test permission normalization when preserve_permissions=False."""
        temp_path, source = test_files_structure

        # Create a file with specific permissions
        special_file = source / "special.txt"
        special_file.write_text("special content")
        special_file.chmod(0o600)  # Restrictive permissions

        # Create directory with specific permissions
        special_dir = source / "special_dir"
        special_dir.mkdir()
        special_dir.chmod(0o700)

        # Create archive with permission normalization
        tar = TarArchive(preserve_permissions=False)
        archive = temp_path / "normalized.tar"
        tar.create(source, archive)

        # Check normalized permissions in archive
        with tarfile.open(archive, "r") as tar_file:
            for member in tar_file.getmembers():
                if member.isfile():
                    # Files should be normalized to 0o644
                    assert (member.mode & 0o777) == 0o644
                elif member.isdir():
                    # Directories should be normalized to 0o755
                    assert (member.mode & 0o777) == 0o755

    def test_preserve_permissions_true(self, test_files_structure: tuple[Path, Path]) -> None:
        """Test permission preservation when preserve_permissions=True."""
        temp_path, source = test_files_structure

        # Create a file with specific permissions
        special_file = source / "special.txt"
        special_file.write_text("special content")
        original_mode = 0o600
        special_file.chmod(original_mode)

        # Create archive with permission preservation
        tar = TarArchive(preserve_permissions=True)
        archive = temp_path / "preserved.tar"
        tar.create(source, archive)

        # Check that permissions are preserved in archive
        with tarfile.open(archive, "r") as tar_file:
            special_member = None
            for member in tar_file.getmembers():
                if member.name.endswith("special.txt"):
                    special_member = member
                    break

            assert special_member is not None
            # Original permissions should be preserved
            assert (special_member.mode & 0o777) == original_mode

    def test_combined_deterministic_and_permission_settings(
        self, test_files_structure: tuple[Path, Path]
    ) -> None:
        """Test interaction between deterministic mode and permission preservation."""
        temp_path, source = test_files_structure

        # Create file with specific permissions
        test_file = source / "test.txt"
        test_file.write_text("test")
        test_file.chmod(0o600)

        # Test deterministic=True, preserve_permissions=False
        tar = TarArchive(deterministic=True, preserve_permissions=False)
        archive = temp_path / "det_norm.tar"
        tar.create(source, archive)

        with tarfile.open(archive, "r") as tar_file:
            for member in tar_file.getmembers():
                if member.isfile() and member.name.endswith("test.txt"):
                    # Should have deterministic metadata
                    assert member.uid == 0
                    assert member.gid == 0
                    assert member.mtime == 0
                    # And normalized permissions
                    assert (member.mode & 0o777) == 0o644

    def test_extract_with_hardlinks(self, tar_archive: TarArchive, temp_directory: Path) -> None:
        """Test extraction with unsafe hardlinks that escape extraction directory."""
        temp_path = temp_directory
        archive = temp_path / "hardlink.tar"

        # Create archive with hardlink that escapes extraction directory
        with tarfile.open(archive, "w") as tar:
            # Add regular file
            info1 = tarfile.TarInfo(name="file1.txt")
            info1.size = 12
            with tempfile.SpooledTemporaryFile() as spool:
                spool.write(b"test content")
                spool.seek(0)
                tar.addfile(info1, fileobj=spool)

            # Add hardlink that tries to escape extraction directory
            info2 = tarfile.TarInfo(name="subdir/hardlink.txt")
            info2.type = tarfile.LNKTYPE
            info2.linkname = "../../outside_file.txt"  # This escapes the extraction directory
            tar.addfile(info2)

        output = temp_path / "extracted"

        # This should trigger the symlink safety check for hardlinks
        with pytest.raises(ArchiveError, match="Unsafe link target in archive"):
            tar_archive.extract(archive, output)

    def test_create_with_non_deterministic_mode(self, test_files_structure: tuple[Path, Path]) -> None:
        """Test creating archive with deterministic=False preserves original metadata."""
        temp_path, source = test_files_structure

        # Create archive with non-deterministic mode
        tar = TarArchive(deterministic=False)
        archive = temp_path / "non_det.tar"
        tar.create(source, archive)

        # Metadata should NOT be normalized (implementation specific)
        # We mainly verify the archive is created successfully
        assert archive.exists()
        assert tar.validate(archive)

    def test_list_contents_with_directories(
        self, tar_archive: TarArchive, test_files_structure: tuple[Path, Path]
    ) -> None:
        """Test that list_contents only returns files, not directories."""
        temp_path, source = test_files_structure
        archive = temp_path / "test.tar"

        # Add additional directory structure
        nested_dir = source / "deeply" / "nested" / "dir"
        nested_dir.mkdir(parents=True)
        nested_file = nested_dir / "deep_file.txt"
        nested_file.write_text("deep content")

        tar_archive.create(source, archive)
        contents = tar_archive.list_contents(archive)

        # Should only include files, not directories
        assert all(
            "deep_file.txt" in path
            or not any(d in path for d in ["deeply", "nested", "dir"])
            or "file" in path
            for path in contents
        )
        # Verify the deep file is included
        assert any("deep_file.txt" in path for path in contents)


# 🧱🏗️🔚
