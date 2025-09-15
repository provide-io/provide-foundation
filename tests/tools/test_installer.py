"""Tests for ToolInstaller class."""

import os
from pathlib import Path
import platform
import tarfile
import tempfile
import zipfile

import pytest

from provide.foundation.tools.base import ToolMetadata
from provide.foundation.tools.installer import InstallError, ToolInstaller


class TestInstallError:
    """Test InstallError exception."""

    def test_inherits_from_foundation_error(self):
        """Test that InstallError inherits from FoundationError."""
        from provide.foundation.errors import FoundationError

        assert issubclass(InstallError, FoundationError)

    def test_can_be_raised_and_caught(self):
        """Test that InstallError can be raised and caught."""
        with pytest.raises(InstallError) as exc_info:
            raise InstallError("Test error")

        assert str(exc_info.value) == "Test error"


class TestToolInstaller:
    """Test ToolInstaller functionality."""

    @pytest.fixture
    def installer(self):
        """Create ToolInstaller instance."""
        return ToolInstaller()

    @pytest.fixture
    def sample_metadata(self):
        """Create sample tool metadata."""
        return ToolMetadata(
            name="testtool",
            version="1.0.0",
            platform="linux",
            arch="amd64",
            executable_name="testtool",
        )

    @pytest.fixture
    def temp_dir(self):
        """Create temporary directory for tests."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            yield Path(tmp_dir)

    @pytest.fixture
    def sample_zip(self, temp_dir):
        """Create sample ZIP file for testing."""
        zip_path = temp_dir / "test.zip"

        with zipfile.ZipFile(zip_path, "w") as zf:
            # Add a binary file
            zf.writestr("bin/testtool", b"#!/bin/bash\necho 'Hello from testtool'\n")
            # Add a text file
            zf.writestr("README.txt", "This is a test tool")
            # Add nested file
            zf.writestr("docs/help.txt", "Help documentation")

        return zip_path

    @pytest.fixture
    def sample_tar_gz(self, temp_dir):
        """Create sample TAR.GZ file for testing."""
        tar_path = temp_dir / "test.tar.gz"

        with tarfile.open(tar_path, "w:gz") as tf:
            # Create temporary files to add
            readme_path = temp_dir / "README.txt"
            readme_path.write_text("This is a test tool")

            bin_dir = temp_dir / "bin"
            bin_dir.mkdir()
            tool_path = bin_dir / "testtool"
            tool_path.write_text("#!/bin/bash\necho 'Hello from testtool'\n")
            tool_path.chmod(0o755)

            # Add files to tar
            tf.add(readme_path, arcname="README.txt")
            tf.add(tool_path, arcname="bin/testtool")

        return tar_path

    @pytest.fixture
    def sample_binary(self, temp_dir):
        """Create sample binary file for testing."""
        binary_path = temp_dir / "testtool"

        # Create a simple ELF-like binary (fake but detectable)
        binary_content = b"\x7fELF\x02\x01\x01\x00" + b"\x00" * 56  # ELF header
        binary_content += b"echo 'Hello from testtool'"

        binary_path.write_bytes(binary_content)
        return binary_path

    def test_install_nonexistent_artifact(self, installer, sample_metadata):
        """Test installing nonexistent artifact raises error."""
        nonexistent = Path("/nonexistent/file.zip")

        with pytest.raises(InstallError, match="Artifact not found"):
            installer.install(nonexistent, sample_metadata)

    def test_get_install_dir_with_metadata_path(self, installer):
        """Test get_install_dir uses metadata install_path if provided."""
        custom_path = Path("/custom/install/path")
        metadata = ToolMetadata(
            name="testtool",
            version="1.0.0",
            platform="linux",
            arch="amd64",
            install_path=custom_path,
        )

        result = installer.get_install_dir(metadata)
        assert result == custom_path

    def test_get_install_dir_default(self, installer, sample_metadata):
        """Test get_install_dir uses default path."""
        result = installer.get_install_dir(sample_metadata)
        expected = Path.home() / ".wrknv" / "tools" / "testtool" / "1.0.0"
        assert result == expected

    def test_extract_zip_success(self, installer, sample_zip, temp_dir):
        """Test successful ZIP extraction."""
        dest_dir = temp_dir / "extracted"

        installer.extract_zip(sample_zip, dest_dir)

        assert dest_dir.exists()
        assert (dest_dir / "bin" / "testtool").exists()
        assert (dest_dir / "README.txt").exists()
        assert (dest_dir / "docs" / "help.txt").exists()

    def test_extract_zip_unsafe_paths(self, installer, temp_dir):
        """Test ZIP extraction with unsafe paths raises error."""
        zip_path = temp_dir / "unsafe.zip"

        with zipfile.ZipFile(zip_path, "w") as zf:
            # Add unsafe paths
            zf.writestr("../../../etc/passwd", "unsafe content")
            zf.writestr("/absolute/path", "unsafe content")

        dest_dir = temp_dir / "extracted"

        with pytest.raises(InstallError, match="Unsafe path in archive"):
            installer.extract_zip(zip_path, dest_dir)

    def test_extract_tar_gz_success(self, installer, sample_tar_gz, temp_dir):
        """Test successful TAR.GZ extraction."""
        dest_dir = temp_dir / "extracted"

        installer.extract_tar(sample_tar_gz, dest_dir)

        assert dest_dir.exists()
        assert (dest_dir / "bin" / "testtool").exists()
        assert (dest_dir / "README.txt").exists()

    def test_extract_tar_unsafe_paths(self, installer, temp_dir):
        """Test TAR extraction with unsafe paths raises error."""
        tar_path = temp_dir / "unsafe.tar.gz"

        with tarfile.open(tar_path, "w:gz") as tf:
            # Create file with unsafe path
            info = tarfile.TarInfo("../../../etc/passwd")
            info.size = 13
            from io import BytesIO
            tf.addfile(info, fileobj=BytesIO(b"unsafe content"))

        dest_dir = temp_dir / "extracted"

        with pytest.raises(InstallError, match="Unsafe path in archive"):
            installer.extract_tar(tar_path, dest_dir)

    def test_extract_tar_different_compressions(self, installer, temp_dir):
        """Test TAR extraction with different compression types."""
        content = "test content"

        # Test different compression types
        compressions = [
            ("test.tar", "w"),
            ("test.tar.bz2", "w:bz2"),
            ("test.tar.xz", "w:xz"),
        ]

        for filename, mode in compressions:
            tar_path = temp_dir / filename
            dest_dir = temp_dir / f"extracted_{filename}"

            with tarfile.open(tar_path, mode) as tf:
                info = tarfile.TarInfo("test.txt")
                info.size = len(content)
                from io import BytesIO
                tf.addfile(info, fileobj=BytesIO(content.encode()))

            installer.extract_tar(tar_path, dest_dir)
            assert (dest_dir / "test.txt").exists()

    def test_is_binary_elf(self, installer):
        """Test binary detection for ELF files."""
        with tempfile.NamedTemporaryFile() as tmp:
            # Write ELF header
            tmp.write(b"\x7fELF\x02\x01\x01\x00")
            tmp.flush()

            result = installer.is_binary(Path(tmp.name))
            assert result is True

    def test_is_binary_windows_pe(self, installer):
        """Test binary detection for Windows PE files."""
        with tempfile.NamedTemporaryFile() as tmp:
            # Write PE header
            tmp.write(b"MZ\x90\x00")
            tmp.flush()

            result = installer.is_binary(Path(tmp.name))
            assert result is True

    def test_is_binary_macos_mach_o(self, installer):
        """Test binary detection for macOS Mach-O files."""
        with tempfile.NamedTemporaryFile() as tmp:
            # Write Mach-O header
            tmp.write(b"\xfe\xed\xfa\xce")
            tmp.flush()

            result = installer.is_binary(Path(tmp.name))
            assert result is True

    def test_is_binary_macos_universal(self, installer):
        """Test binary detection for macOS universal binaries."""
        with tempfile.NamedTemporaryFile() as tmp:
            # Write universal binary header
            tmp.write(b"\xca\xfe\xba\xbe")
            tmp.flush()

            result = installer.is_binary(Path(tmp.name))
            assert result is True

    def test_is_binary_text_file(self, installer):
        """Test binary detection returns False for text files."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt") as tmp:
            tmp.write("This is a text file")
            tmp.flush()

            result = installer.is_binary(Path(tmp.name))
            assert result is False

    def test_is_binary_no_extension(self, installer):
        """Test binary detection for files without extension."""
        with tempfile.NamedTemporaryFile() as tmp:
            tmp.write(b"#!/bin/bash\necho 'Hello'\n")
            tmp.flush()

            # Remove extension from path
            no_ext_path = Path(tmp.name).with_suffix("")
            no_ext_path.write_bytes(b"#!/bin/bash\necho 'Hello'\n")

            result = installer.is_binary(no_ext_path)
            assert result is False  # Not a binary signature

    def test_install_binary_success(self, installer, sample_binary, temp_dir, sample_metadata):
        """Test successful binary installation."""
        dest_dir = temp_dir / "install"

        installer.install_binary(sample_binary, dest_dir, sample_metadata)

        assert dest_dir.exists()
        assert (dest_dir / "bin").exists()
        assert (dest_dir / "bin" / "testtool").exists()

        # Check if file is executable (on Unix systems)
        if platform.system() != "Windows":
            installed_binary = dest_dir / "bin" / "testtool"
            assert os.access(installed_binary, os.X_OK)

    def test_install_binary_custom_name(self, installer, sample_binary, temp_dir):
        """Test binary installation with custom executable name."""
        metadata = ToolMetadata(
            name="testtool",
            version="1.0.0",
            platform="linux",
            arch="amd64",
            executable_name="custom-tool",
        )

        dest_dir = temp_dir / "install"

        installer.install_binary(sample_binary, dest_dir, metadata)

        assert (dest_dir / "bin" / "custom-tool").exists()

    @pytest.mark.skipif(platform.system() == "Windows", reason="Unix permissions test")
    def test_set_permissions_unix(self, installer, temp_dir, sample_metadata):
        """Test permission setting on Unix systems."""
        install_dir = temp_dir / "install"
        bin_dir = install_dir / "bin"
        bin_dir.mkdir(parents=True)

        # Create test executable
        test_exe = bin_dir / "testtool"
        test_exe.write_text("#!/bin/bash\necho hello")
        test_exe.chmod(0o644)  # Set non-executable initially

        installer.set_permissions(install_dir, sample_metadata)

        # Should now be executable
        assert os.access(test_exe, os.X_OK)
        assert oct(test_exe.stat().st_mode)[-3:] == "755"

    @pytest.mark.skipif(platform.system() == "Windows", reason="Unix permissions test")
    def test_set_permissions_root_executable(self, installer, temp_dir):
        """Test permission setting for executable in root directory."""
        install_dir = temp_dir / "install"
        install_dir.mkdir()

        metadata = ToolMetadata(
            name="testtool",
            version="1.0.0",
            platform="linux",
            arch="amd64",
            executable_name="testtool",
        )

        # Create executable in root
        test_exe = install_dir / "testtool"
        test_exe.write_text("#!/bin/bash\necho hello")
        test_exe.chmod(0o644)

        installer.set_permissions(install_dir, metadata)

        assert os.access(test_exe, os.X_OK)

    @pytest.mark.skipif(platform.system() == "Windows", reason="Symlink test")
    def test_create_symlinks_success(self, installer, temp_dir, sample_metadata):
        """Test symlink creation."""
        install_dir = temp_dir / "tools" / "testtool" / "1.0.0"
        install_dir.mkdir(parents=True)

        installer.create_symlinks(install_dir, sample_metadata)

        latest_link = install_dir.parent / "latest"
        assert latest_link.is_symlink()
        # Use samefile to compare since resolve() may add /private prefix on macOS
        assert latest_link.resolve().samefile(install_dir)

    @pytest.mark.skipif(platform.system() == "Windows", reason="Symlink test")
    def test_create_symlinks_replaces_existing(self, installer, temp_dir, sample_metadata):
        """Test symlink creation replaces existing symlink."""
        tools_dir = temp_dir / "tools" / "testtool"
        tools_dir.mkdir(parents=True)

        # Create old version
        old_dir = tools_dir / "0.9.0"
        old_dir.mkdir()

        # Create existing symlink
        latest_link = tools_dir / "latest"
        latest_link.symlink_to(old_dir)

        # Install new version
        new_dir = tools_dir / "1.0.0"
        new_dir.mkdir()

        installer.create_symlinks(new_dir, sample_metadata)

        # Should point to new version
        assert latest_link.resolve().samefile(new_dir)

    def test_install_zip_full_workflow(self, installer, sample_zip, temp_dir, sample_metadata):
        """Test complete installation workflow for ZIP file."""
        # Set install path in metadata
        install_dir = temp_dir / "install"
        sample_metadata.install_path = install_dir

        result = installer.install(sample_zip, sample_metadata)

        assert result == install_dir
        assert install_dir.exists()
        assert (install_dir / "bin" / "testtool").exists()
        assert (install_dir / "README.txt").exists()

    def test_install_tar_full_workflow(self, installer, sample_tar_gz, temp_dir, sample_metadata):
        """Test complete installation workflow for TAR file."""
        install_dir = temp_dir / "install"
        sample_metadata.install_path = install_dir

        result = installer.install(sample_tar_gz, sample_metadata)

        assert result == install_dir
        assert install_dir.exists()
        assert (install_dir / "bin" / "testtool").exists()

    def test_install_binary_full_workflow(self, installer, sample_binary, temp_dir, sample_metadata):
        """Test complete installation workflow for binary file."""
        install_dir = temp_dir / "install"
        sample_metadata.install_path = install_dir

        result = installer.install(sample_binary, sample_metadata)

        assert result == install_dir
        assert (install_dir / "bin" / "testtool").exists()

    def test_install_unknown_format(self, installer, temp_dir, sample_metadata):
        """Test installation of unknown file format raises error."""
        unknown_file = temp_dir / "unknown.xyz"
        unknown_file.write_text("unknown format")

        with pytest.raises(InstallError, match="Unknown artifact type"):
            installer.install(unknown_file, sample_metadata)

    def test_install_reads_file_content_for_binary_detection(self, installer, temp_dir, sample_metadata):
        """Test that installer reads file content for binary detection."""
        # Create file without extension but with binary content
        binary_file = temp_dir / "mytool"
        binary_file.write_bytes(b"\x7fELF\x02\x01\x01\x00" + b"\x00" * 56)

        install_dir = temp_dir / "install"
        sample_metadata.install_path = install_dir

        installer.install(binary_file, sample_metadata)

        # Should be installed as binary
        assert (install_dir / "bin" / "testtool").exists()
