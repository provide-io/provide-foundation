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

from provide.testkit.mocking import Mock, patch
import pytest

from provide.foundation.tools.base import ToolMetadata
from provide.foundation.tools.installer import InstallError, ToolInstaller


class TestSetPermissions:
    """Tests for set_permissions method."""

    @pytest.mark.skipif(platform.system() == "Windows", reason="Permissions not applicable on Windows")
    def test_set_permissions_bin_directory(self, tmp_path: Path) -> None:
        """Test that executables in bin/ are made executable."""
        installer = ToolInstaller()

        install_dir = tmp_path / "install"
        bin_dir = install_dir / "bin"
        bin_dir.mkdir(parents=True)

        exe = bin_dir / "mytool"
        exe.write_text("#!/bin/sh\necho hello")
        exe.chmod(0o644)  # Not executable

        metadata = ToolMetadata(name="test-tool", version="1.0.0", platform="linux", arch="amd64")

        installer.set_permissions(install_dir, metadata)

        # Should now be executable
        assert exe.stat().st_mode & 0o111

    @pytest.mark.skipif(platform.system() == "Windows", reason="Permissions not applicable on Windows")
    def test_set_permissions_executable_name(self, tmp_path: Path) -> None:
        """Test that named executable is made executable."""
        installer = ToolInstaller()

        install_dir = tmp_path / "install"
        install_dir.mkdir()

        exe = install_dir / "mytool"
        exe.write_text("#!/bin/sh\necho hello")
        exe.chmod(0o644)

        metadata = ToolMetadata(
            name="test-tool",
            version="1.0.0",
            platform="linux",
            arch="amd64",
            executable_name="mytool",
        )

        installer.set_permissions(install_dir, metadata)

        assert exe.stat().st_mode & 0o111

    @pytest.mark.skipif(platform.system() != "Windows", reason="Windows-specific test")
    def test_set_permissions_windows_noop(self, tmp_path: Path) -> None:
        """Test that set_permissions is no-op on Windows."""
        installer = ToolInstaller()

        install_dir = tmp_path / "install"
        install_dir.mkdir()

        metadata = ToolMetadata(name="test-tool", version="1.0.0", platform="linux", arch="amd64")

        # Should not raise
        installer.set_permissions(install_dir, metadata)


class TestCreateSymlinks:
    """Tests for create_symlinks method."""

    @pytest.mark.skipif(platform.system() == "Windows", reason="Symlinks not supported on Windows")
    def test_create_symlinks_basic(self, tmp_path: Path) -> None:
        """Test basic symlink creation."""
        installer = ToolInstaller()

        install_dir = tmp_path / "tools" / "mytool" / "1.0.0"
        install_dir.mkdir(parents=True)

        metadata = ToolMetadata(name="mytool", version="1.0.0", platform="linux", arch="amd64")

        installer.create_symlinks(install_dir, metadata)

        latest_link = tmp_path / "tools" / "mytool" / "latest"
        assert latest_link.is_symlink()
        assert latest_link.resolve() == install_dir.resolve()

    @pytest.mark.skipif(platform.system() == "Windows", reason="Symlinks not supported on Windows")
    def test_create_symlinks_replaces_existing(self, tmp_path: Path) -> None:
        """Test that existing symlink is replaced."""
        installer = ToolInstaller()

        parent = tmp_path / "tools" / "mytool"
        parent.mkdir(parents=True)

        old_dir = parent / "0.9.0"
        old_dir.mkdir()

        latest_link = parent / "latest"
        latest_link.symlink_to(old_dir)

        new_dir = parent / "1.0.0"
        new_dir.mkdir()

        metadata = ToolMetadata(name="mytool", version="1.0.0", platform="linux", arch="amd64")

        installer.create_symlinks(new_dir, metadata)

        assert latest_link.is_symlink()
        assert latest_link.resolve() == new_dir.resolve()

    @pytest.mark.skipif(platform.system() != "Windows", reason="Windows-specific test")
    def test_create_symlinks_windows_noop(self, tmp_path: Path) -> None:
        """Test that create_symlinks is no-op on Windows."""
        installer = ToolInstaller()

        install_dir = tmp_path / "install"
        install_dir.mkdir()

        metadata = ToolMetadata(name="mytool", version="1.0.0", platform="linux", arch="amd64")

        # Should not raise
        installer.create_symlinks(install_dir, metadata)


class TestInstall:
    """Tests for main install method."""

    def test_install_artifact_not_found(self, tmp_path: Path) -> None:
        """Test that install raises error if artifact doesn't exist."""
        installer = ToolInstaller()

        artifact = tmp_path / "nonexistent.zip"
        metadata = ToolMetadata(name="test-tool", version="1.0.0", platform="linux", arch="amd64")

        with pytest.raises(InstallError, match="Artifact not found"):
            installer.install(artifact, metadata)

    def test_install_zip_artifact(self, tmp_path: Path) -> None:
        """Test installation from ZIP artifact."""
        installer = ToolInstaller()

        # Create ZIP artifact
        zip_path = tmp_path / "test.zip"
        with zipfile.ZipFile(zip_path, "w") as zf:
            zf.writestr("file.txt", "content")

        metadata = ToolMetadata(
            name="test-tool",
            version="1.0.0",
            platform="linux",
            arch="amd64",
            install_path=tmp_path / "install",
        )

        result = installer.install(zip_path, metadata)

        assert result == tmp_path / "install"
        assert (result / "file.txt").exists()

    def test_install_tar_artifact(self, tmp_path: Path) -> None:
        """Test installation from TAR artifact."""
        installer = ToolInstaller()

        # Create TAR artifact
        tar_path = tmp_path / "test.tar"
        with tarfile.open(tar_path, "w") as tf:
            file1 = tarfile.TarInfo(name="file.txt")
            file1.size = len(b"content")
            tf.addfile(file1, io.BytesIO(b"content"))

        metadata = ToolMetadata(
            name="test-tool",
            version="1.0.0",
            platform="linux",
            arch="amd64",
            install_path=tmp_path / "install",
        )

        result = installer.install(tar_path, metadata)

        assert result == tmp_path / "install"

    def test_install_binary_artifact(self, tmp_path: Path) -> None:
        """Test installation from binary artifact."""
        installer = ToolInstaller()

        # Create binary artifact
        binary = tmp_path / "mybinary"
        binary.write_bytes(b"\x7fELF" + b"\x00" * 100)

        metadata = ToolMetadata(
            name="test-tool",
            version="1.0.0",
            platform="linux",
            arch="amd64",
            install_path=tmp_path / "install",
        )

        result = installer.install(binary, metadata)

        assert result == tmp_path / "install"
        assert (result / "bin" / "mybinary").exists()

    def test_install_unknown_artifact_type(self, tmp_path: Path) -> None:
        """Test that unknown artifact types raise error."""
        installer = ToolInstaller()

        artifact = tmp_path / "test.unknown"
        artifact.write_text("content")

        metadata = ToolMetadata(name="test-tool", version="1.0.0", platform="linux", arch="amd64")

        with pytest.raises(InstallError, match="Unknown artifact type"):
            installer.install(artifact, metadata)

    @patch("provide.foundation.tools.installer.ToolInstaller.set_permissions")
    @patch("provide.foundation.tools.installer.ToolInstaller.create_symlinks")
    def test_install_calls_post_install_steps(
        self,
        mock_symlinks: Mock,
        mock_permissions: Mock,
        tmp_path: Path,
    ) -> None:
        """Test that install calls set_permissions and create_symlinks."""
        installer = ToolInstaller()

        zip_path = tmp_path / "test.zip"
        with zipfile.ZipFile(zip_path, "w") as zf:
            zf.writestr("file.txt", "content")

        metadata = ToolMetadata(
            name="test-tool",
            version="1.0.0",
            platform="linux",
            arch="amd64",
            install_path=tmp_path / "install",
        )

        installer.install(zip_path, metadata)

        mock_permissions.assert_called_once()
        mock_symlinks.assert_called_once()


# 🧱🏗️🔚
