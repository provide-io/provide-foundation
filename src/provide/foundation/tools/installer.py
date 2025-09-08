"""
Tool installation manager for various archive formats.

Handles extraction and installation of tools from different
archive formats (zip, tar, gz, etc.) and binary files.
"""

import shutil
import tarfile
import tempfile
import zipfile
from pathlib import Path

from provide.foundation.errors import FoundationError
from provide.foundation.logger import get_logger
from provide.foundation.tools.base import ToolMetadata

log = get_logger(__name__)


class InstallError(FoundationError):
    """Raised when installation fails."""
    
    pass


class ToolInstaller:
    """
    Handle tool installation from various artifact formats.
    
    Supports:
    - ZIP archives
    - TAR archives (with compression)
    - Single binary files
    - Platform-specific installation patterns
    """
    
    def install(self, artifact: Path, metadata: ToolMetadata) -> Path:
        """
        Install tool from artifact.
        
        Args:
            artifact: Path to downloaded artifact.
            metadata: Tool metadata with installation info.
            
        Returns:
            Path to installed tool directory.
            
        Raises:
            InstallError: If installation fails.
        """
        if not artifact.exists():
            raise InstallError(f"Artifact not found: {artifact}")
        
        # Determine install directory
        install_dir = self.get_install_dir(metadata)
        
        log.info(f"Installing {metadata.name} {metadata.version} to {install_dir}")
        
        # Extract based on file type
        suffix = artifact.suffix.lower()
        if suffix == ".zip":
            self.extract_zip(artifact, install_dir)
        elif suffix in [".tar", ".gz", ".tgz", ".bz2", ".xz"]:
            self.extract_tar(artifact, install_dir)
        elif self.is_binary(artifact):
            self.install_binary(artifact, install_dir, metadata)
        else:
            raise InstallError(f"Unknown artifact type: {suffix}")
        
        # Set permissions
        self.set_permissions(install_dir, metadata)
        
        # Create symlinks if needed
        self.create_symlinks(install_dir, metadata)
        
        log.info(f"Successfully installed {metadata.name} to {install_dir}")
        return install_dir
    
    def get_install_dir(self, metadata: ToolMetadata) -> Path:
        """
        Get installation directory for tool.
        
        Args:
            metadata: Tool metadata.
            
        Returns:
            Installation directory path.
        """
        if metadata.install_path:
            return metadata.install_path
        
        # Default to ~/.wrknv/tools/<name>/<version>
        base = Path.home() / ".wrknv" / "tools"
        return base / metadata.name / metadata.version
    
    def extract_zip(self, archive: Path, dest: Path) -> None:
        """
        Extract ZIP archive.
        
        Args:
            archive: Path to ZIP file.
            dest: Destination directory.
        """
        log.debug(f"Extracting ZIP {archive} to {dest}")
        
        dest.mkdir(parents=True, exist_ok=True)
        
        with zipfile.ZipFile(archive, "r") as zf:
            # Check for unsafe paths
            for member in zf.namelist():
                if member.startswith("/") or ".." in member:
                    raise InstallError(f"Unsafe path in archive: {member}")
            
            zf.extractall(dest)
    
    def extract_tar(self, archive: Path, dest: Path) -> None:
        """
        Extract tar archive (with optional compression).
        
        Args:
            archive: Path to tar file.
            dest: Destination directory.
        """
        log.debug(f"Extracting tar {archive} to {dest}")
        
        dest.mkdir(parents=True, exist_ok=True)
        
        # Determine mode based on extension
        mode = "r"
        if archive.suffix in [".gz", ".tgz"]:
            mode = "r:gz"
        elif archive.suffix == ".bz2":
            mode = "r:bz2"
        elif archive.suffix == ".xz":
            mode = "r:xz"
        
        with tarfile.open(archive, mode) as tf:
            # Check for unsafe paths
            for member in tf.getmembers():
                if member.name.startswith("/") or ".." in member.name:
                    raise InstallError(f"Unsafe path in archive: {member.name}")
            
            tf.extractall(dest)
    
    def is_binary(self, file_path: Path) -> bool:
        """
        Check if file is a binary executable.
        
        Args:
            file_path: Path to check.
            
        Returns:
            True if file appears to be binary.
        """
        # Check if file has no extension or common binary extensions
        if not file_path.suffix or file_path.suffix in [".exe", ".bin"]:
            # Try to read first few bytes
            try:
                with file_path.open("rb") as f:
                    header = f.read(4)
                    # Check for common binary signatures
                    if header.startswith(b"\x7fELF"):  # Linux ELF
                        return True
                    if header.startswith(b"MZ"):  # Windows PE
                        return True
                    if header.startswith(b"\xfe\xed\xfa"):  # macOS Mach-O
                        return True
                    if header.startswith(b"\xca\xfe\xba\xbe"):  # macOS universal
                        return True
            except Exception:
                pass
        
        return False
    
    def install_binary(
        self,
        binary: Path,
        dest: Path,
        metadata: ToolMetadata
    ) -> None:
        """
        Install single binary file.
        
        Args:
            binary: Path to binary file.
            dest: Destination directory.
            metadata: Tool metadata.
        """
        log.debug(f"Installing binary {binary} to {dest}")
        
        dest.mkdir(parents=True, exist_ok=True)
        bin_dir = dest / "bin"
        bin_dir.mkdir(exist_ok=True)
        
        # Determine target name
        target_name = metadata.executable_name or binary.name
        target = bin_dir / target_name
        
        # Copy binary
        shutil.copy2(binary, target)
        
        # Make executable
        target.chmod(0o755)
    
    def set_permissions(self, install_dir: Path, metadata: ToolMetadata) -> None:
        """
        Set appropriate permissions on installed files.
        
        Args:
            install_dir: Installation directory.
            metadata: Tool metadata.
        """
        import platform
        
        if platform.system() == "Windows":
            return  # Windows handles permissions differently
        
        # Find executables and make them executable
        bin_dir = install_dir / "bin"
        if bin_dir.exists():
            for file in bin_dir.iterdir():
                if file.is_file():
                    file.chmod(0o755)
        
        # Check for executable name in root
        if metadata.executable_name:
            exe_path = install_dir / metadata.executable_name
            if exe_path.exists():
                exe_path.chmod(0o755)
    
    def create_symlinks(self, install_dir: Path, metadata: ToolMetadata) -> None:
        """
        Create symlinks for easier access.
        
        Args:
            install_dir: Installation directory.
            metadata: Tool metadata.
        """
        import platform
        
        if platform.system() == "Windows":
            return  # Windows doesn't support symlinks easily
        
        # Create version-less symlink
        if metadata.name and metadata.version:
            parent = install_dir.parent
            latest_link = parent / "latest"
            
            if latest_link.exists() or latest_link.is_symlink():
                latest_link.unlink()
            
            latest_link.symlink_to(install_dir)
            log.debug(f"Created symlink {latest_link} -> {install_dir}")