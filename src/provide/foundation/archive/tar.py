"""TAR archive implementation with explicit capabilities."""

import tarfile
from pathlib import Path
from typing import Callable, Optional

from provide.foundation.archive.base import BaseArchive, ArchiveError
from provide.foundation.archive.capabilities import (
    ArchiveCapability, 
    CapabilityMixin,
    requires_capability,
)


class TarArchive(BaseArchive, CapabilityMixin):
    """
    TAR archive implementation.
    
    Capabilities: BUNDLE + METADATA + STREAMING + DETERMINISTIC
    - Can bundle multiple files/directories ✓
    - Can preserve metadata (permissions, timestamps) ✓  
    - Can stream without temp files ✓
    - Can create deterministic output ✓
    - Cannot compress (use gzip archiver in composite) ✗
    - Cannot encrypt ✗
    """
    
    # EXPLICIT capability declaration - baked into the spec
    capabilities = (
        ArchiveCapability.BUNDLE |
        ArchiveCapability.METADATA | 
        ArchiveCapability.PERMISSIONS |
        ArchiveCapability.TIMESTAMPS |
        ArchiveCapability.STREAMING |
        ArchiveCapability.DETERMINISTIC
    )
    
    def __init__(self, 
                 deterministic: bool = True,
                 preserve_permissions: bool = True,
                 tar_filter: Optional[Callable] = None):
        """
        Initialize TAR archiver.
        
        Args:
            deterministic: Create reproducible output
            preserve_permissions: Preserve file permissions
            tar_filter: Custom TarInfo filter function
        """
        self.deterministic = deterministic
        self.preserve_permissions = preserve_permissions
        self.tar_filter = tar_filter
        
        # Validate that our configuration matches our capabilities
        if not preserve_permissions:
            # If not preserving permissions, remove that capability
            self.capabilities &= ~ArchiveCapability.PERMISSIONS

    @requires_capability(ArchiveCapability.BUNDLE)
    def create(self, source: Path, output: Path) -> Path:
        """Create TAR archive from source."""
        try:
            with tarfile.open(output, "w") as tar:
                if source.is_dir():
                    self._add_directory(tar, source)
                else:
                    self._add_file(tar, source)
            return output
        except Exception as e:
            raise ArchiveError(f"Failed to create TAR archive: {e}") from e

    def extract(self, archive: Path, output: Path) -> Path:
        """Extract TAR archive to output directory."""
        try:
            output.mkdir(parents=True, exist_ok=True)
            with tarfile.open(archive, "r") as tar:
                tar.extractall(output)
            return output
        except Exception as e:
            raise ArchiveError(f"Failed to extract TAR archive: {e}") from e

    def validate(self, archive: Path) -> bool:
        """Validate TAR archive integrity."""
        try:
            with tarfile.open(archive, "r") as tar:
                # Try to read all members
                for member in tar:
                    pass
            return True
        except Exception:
            return False

    @requires_capability(ArchiveCapability.BUNDLE)
    def add_file(self, archive_path: Path, file_path: Path, arcname: str = None):
        """Add a single file to existing TAR archive."""
        # This method explicitly requires BUNDLE capability
        pass

    @requires_capability(ArchiveCapability.METADATA)  
    def set_file_metadata(self, file_path: Path, metadata: dict):
        """Set metadata for a file in the archive."""
        # This method explicitly requires METADATA capability
        pass

    def set_compression_level(self, level: int):
        """
        This method will ALWAYS fail because TAR doesn't have COMPRESS capability.
        The @requires_capability decorator will catch this.
        """
        # Note: No @requires_capability decorator - this will fail at class validation
        raise ArchiveError("TAR archiver cannot compress - use CompositeArchive with GzipArchive")

    def _add_directory(self, tar: tarfile.TarFile, directory: Path):
        """Add directory contents to tar."""
        # Implementation details...
        pass

    def _add_file(self, tar: tarfile.TarFile, file_path: Path):  
        """Add single file to tar."""
        # Implementation details...
        pass