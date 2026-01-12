#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Comprehensive tests for tool installer.

Tests all functionality in tools/installer.py including archive extraction,
binary installation, and security validations."""

from __future__ import annotations

import io
from pathlib import Path
import platform
import tarfile
import zipfile

import pytest

from provide.foundation.tools.base import ToolMetadata
from provide.foundation.tools.installer import InstallError, ToolInstaller


class TestInstallError:
    """Tests for InstallError exception."""

    def test_install_error_inheritance(self) -> None:
        """Test that InstallError inherits from FoundationError."""
        from provide.foundation.errors import FoundationError

        error = InstallError("Test error")
        assert isinstance(error, FoundationError)


class TestToolInstallerInit:
    """Tests for ToolInstaller initialization."""

    def test_installer_creation(self) -> None:
        """Test that ToolInstaller can be instantiated."""
        installer = ToolInstaller()
        assert installer is not None


class TestGetInstallDir:
    """Tests for get_install_dir method."""

    def test_get_install_dir_with_explicit_path(self, tmp_path: Path) -> None:
        """Test installation directory when metadata has install_path."""
        installer = ToolInstaller()
        install_path = tmp_path / "custom-install"
        metadata = ToolMetadata(
            name="test-tool",
            version="1.0.0",
            platform="linux",
            arch="amd64",
            install_path=install_path,
        )

        result = installer.get_install_dir(metadata)

        assert result == install_path

    def test_get_install_dir_default_path(self) -> None:
        """Test default installation directory path."""
        installer = ToolInstaller()
        metadata = ToolMetadata(
            name="test-tool",
            version="1.0.0",
            platform="linux",
            arch="amd64",
        )

        result = installer.get_install_dir(metadata)

        expected = Path.home() / ".provide-foundation" / "tools" / "test-tool" / "1.0.0"
        assert result == expected


class TestIsBinary:
    """Tests for is_binary method."""

    def test_is_binary_elf_linux(self, tmp_path: Path) -> None:
        """Test detection of Linux ELF binary."""
        installer = ToolInstaller()
        binary = tmp_path / "test-elf"
        binary.write_bytes(b"\x7fELF" + b"\x00" * 100)

        assert installer.is_binary(binary) is True

    def test_is_binary_windows_pe(self, tmp_path: Path) -> None:
        """Test detection of Windows PE binary."""
        installer = ToolInstaller()
        binary = tmp_path / "test.exe"
        binary.write_bytes(b"MZ" + b"\x00" * 100)

        assert installer.is_binary(binary) is True

    def test_is_binary_macos_macho(self, tmp_path: Path) -> None:
        """Test detection of macOS Mach-O binary."""
        installer = ToolInstaller()
        binary = tmp_path / "test-macho"
        binary.write_bytes(b"\xfe\xed\xfa" + b"\x00" * 100)

        assert installer.is_binary(binary) is True

    def test_is_binary_macos_universal(self, tmp_path: Path) -> None:
        """Test detection of macOS universal binary."""
        installer = ToolInstaller()
        binary = tmp_path / "test-universal"
        binary.write_bytes(b"\xca\xfe\xba\xbe" + b"\x00" * 100)

        assert installer.is_binary(binary) is True

    def test_is_binary_non_binary_file(self, tmp_path: Path) -> None:
        """Test that text files are not detected as binaries."""
        installer = ToolInstaller()
        text_file = tmp_path / "test.txt"
        text_file.write_text("This is a text file")

        assert installer.is_binary(text_file) is False

    def test_is_binary_with_extension(self, tmp_path: Path) -> None:
        """Test that files with extensions are generally not binaries."""
        installer = ToolInstaller()
        text_file = tmp_path / "test.json"
        text_file.write_text("{}")

        assert installer.is_binary(text_file) is False

    def test_is_binary_bin_extension(self, tmp_path: Path) -> None:
        """Test that .bin extension is checked for binary signatures."""
        installer = ToolInstaller()
        binary = tmp_path / "test.bin"
        binary.write_bytes(b"\x7fELF" + b"\x00" * 100)

        assert installer.is_binary(binary) is True


class TestExtractZip:
    """Tests for extract_zip method."""

    def test_extract_zip_basic(self, tmp_path: Path) -> None:
        """Test basic ZIP extraction."""
        installer = ToolInstaller()

        # Create a ZIP archive
        zip_path = tmp_path / "test.zip"
        dest = tmp_path / "extracted"

        with zipfile.ZipFile(zip_path, "w") as zf:
            zf.writestr("file1.txt", "content1")
            zf.writestr("dir/file2.txt", "content2")

        installer.extract_zip(zip_path, dest)

        assert (dest / "file1.txt").exists()
        assert (dest / "file1.txt").read_text() == "content1"
        assert (dest / "dir" / "file2.txt").exists()
        assert (dest / "dir" / "file2.txt").read_text() == "content2"

    def test_extract_zip_creates_dest(self, tmp_path: Path) -> None:
        """Test that extract_zip creates destination directory."""
        installer = ToolInstaller()

        zip_path = tmp_path / "test.zip"
        dest = tmp_path / "new-dir" / "extracted"

        with zipfile.ZipFile(zip_path, "w") as zf:
            zf.writestr("file.txt", "content")

        installer.extract_zip(zip_path, dest)

        assert dest.exists()
        assert (dest / "file.txt").exists()

    def test_extract_zip_unsafe_absolute_path(self, tmp_path: Path) -> None:
        """Test that absolute paths in ZIP are rejected."""
        installer = ToolInstaller()

        zip_path = tmp_path / "test.zip"
        dest = tmp_path / "extracted"

        with zipfile.ZipFile(zip_path, "w") as zf:
            zf.writestr("/etc/passwd", "malicious")

        with pytest.raises(InstallError, match="Unsafe path in archive"):
            installer.extract_zip(zip_path, dest)

    def test_extract_zip_unsafe_parent_traversal(self, tmp_path: Path) -> None:
        """Test that parent directory traversal is rejected."""
        installer = ToolInstaller()

        zip_path = tmp_path / "test.zip"
        dest = tmp_path / "extracted"

        with zipfile.ZipFile(zip_path, "w") as zf:
            zf.writestr("../../../etc/passwd", "malicious")

        with pytest.raises(InstallError, match="Unsafe path in archive"):
            installer.extract_zip(zip_path, dest)


class TestExtractTar:
    """Tests for extract_tar method."""

    def test_extract_tar_basic(self, tmp_path: Path) -> None:
        """Test basic TAR extraction."""
        installer = ToolInstaller()

        # Create a TAR archive
        tar_path = tmp_path / "test.tar"
        dest = tmp_path / "extracted"

        with tarfile.open(tar_path, "w") as tf:
            # Create files in memory
            file1 = tarfile.TarInfo(name="file1.txt")
            file1.size = len(b"content1")
            tf.addfile(file1, io.BytesIO(b"content1"))

        installer.extract_tar(tar_path, dest)

        assert (dest / "file1.txt").exists()

    def test_extract_tar_gz(self, tmp_path: Path) -> None:
        """Test extraction of gzipped TAR archive."""
        installer = ToolInstaller()

        tar_path = tmp_path / "test.tar.gz"
        dest = tmp_path / "extracted"

        with tarfile.open(tar_path, "w:gz") as tf:
            file1 = tarfile.TarInfo(name="file1.txt")
            file1.size = len(b"content1")
            tf.addfile(file1, io.BytesIO(b"content1"))

        installer.extract_tar(tar_path, dest)

        assert (dest / "file1.txt").exists()

    def test_extract_tar_bz2(self, tmp_path: Path) -> None:
        """Test extraction of bzip2 TAR archive."""
        installer = ToolInstaller()

        tar_path = tmp_path / "test.tar.bz2"
        dest = tmp_path / "extracted"

        with tarfile.open(tar_path, "w:bz2") as tf:
            file1 = tarfile.TarInfo(name="file1.txt")
            file1.size = len(b"content1")
            tf.addfile(file1, io.BytesIO(b"content1"))

        installer.extract_tar(tar_path, dest)

        assert (dest / "file1.txt").exists()

    def test_extract_tar_xz(self, tmp_path: Path) -> None:
        """Test extraction of xz TAR archive."""
        installer = ToolInstaller()

        tar_path = tmp_path / "test.tar.xz"
        dest = tmp_path / "extracted"

        with tarfile.open(tar_path, "w:xz") as tf:
            file1 = tarfile.TarInfo(name="file1.txt")
            file1.size = len(b"content1")
            tf.addfile(file1, io.BytesIO(b"content1"))

        installer.extract_tar(tar_path, dest)

        assert (dest / "file1.txt").exists()

    def test_extract_tar_creates_dest(self, tmp_path: Path) -> None:
        """Test that extract_tar creates destination directory."""
        installer = ToolInstaller()

        tar_path = tmp_path / "test.tar"
        dest = tmp_path / "new-dir" / "extracted"

        with tarfile.open(tar_path, "w") as tf:
            file1 = tarfile.TarInfo(name="file.txt")
            file1.size = len(b"content")
            tf.addfile(file1, io.BytesIO(b"content"))

        installer.extract_tar(tar_path, dest)

        assert dest.exists()

    def test_extract_tar_unsafe_absolute_path(self, tmp_path: Path) -> None:
        """Test that absolute paths in TAR are rejected."""
        installer = ToolInstaller()

        tar_path = tmp_path / "test.tar"
        dest = tmp_path / "extracted"

        with tarfile.open(tar_path, "w") as tf:
            file1 = tarfile.TarInfo(name="/etc/passwd")
            file1.size = len(b"malicious")
            tf.addfile(file1, io.BytesIO(b"malicious"))

        with pytest.raises(InstallError, match="Unsafe path in archive"):
            installer.extract_tar(tar_path, dest)

    def test_extract_tar_unsafe_parent_traversal(self, tmp_path: Path) -> None:
        """Test that parent directory traversal is rejected."""
        installer = ToolInstaller()

        tar_path = tmp_path / "test.tar"
        dest = tmp_path / "extracted"

        with tarfile.open(tar_path, "w") as tf:
            file1 = tarfile.TarInfo(name="../../../etc/passwd")
            file1.size = len(b"malicious")
            tf.addfile(file1, io.BytesIO(b"malicious"))

        with pytest.raises(InstallError, match="Unsafe path in archive"):
            installer.extract_tar(tar_path, dest)


class TestInstallBinary:
    """Tests for install_binary method."""

    def test_install_binary_basic(self, tmp_path: Path) -> None:
        """Test basic binary installation."""
        installer = ToolInstaller()

        binary = tmp_path / "mybinary"
        binary.write_bytes(b"\x7fELF" + b"\x00" * 100)

        dest = tmp_path / "install"
        metadata = ToolMetadata(name="test-tool", version="1.0.0", platform="linux", arch="amd64")

        installer.install_binary(binary, dest, metadata)

        assert (dest / "bin" / "mybinary").exists()
        # Check that file is executable (on Unix systems)
        if platform.system() != "Windows":
            assert (dest / "bin" / "mybinary").stat().st_mode & 0o111

    def test_install_binary_custom_name(self, tmp_path: Path) -> None:
        """Test binary installation with custom executable name."""
        installer = ToolInstaller()

        binary = tmp_path / "downloaded-binary"
        binary.write_bytes(b"content")

        dest = tmp_path / "install"
        metadata = ToolMetadata(
            name="test-tool",
            version="1.0.0",
            platform="linux",
            arch="amd64",
            executable_name="custom-name",
        )

        installer.install_binary(binary, dest, metadata)

        assert (dest / "bin" / "custom-name").exists()
        assert not (dest / "bin" / "downloaded-binary").exists()

    def test_install_binary_creates_directories(self, tmp_path: Path) -> None:
        """Test that install_binary creates necessary directories."""
        installer = ToolInstaller()

        binary = tmp_path / "mybinary"
        binary.write_bytes(b"content")

        dest = tmp_path / "new-path" / "install"
        metadata = ToolMetadata(name="test-tool", version="1.0.0", platform="linux", arch="amd64")

        installer.install_binary(binary, dest, metadata)

        assert dest.exists()
        assert (dest / "bin").exists()


# 🧱🏗️🔚
