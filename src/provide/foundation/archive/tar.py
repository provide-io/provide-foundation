"""TAR archive implementation."""

import tarfile
from pathlib import Path

from attrs import define, field

from provide.foundation.archive.base import BaseArchive, ArchiveError
from provide.foundation.file import ensure_parent_dir
from provide.foundation.logger import get_logger

logger = get_logger(__name__)


@define(slots=True)
class TarArchive(BaseArchive):
    """
    TAR archive implementation.
    
    Creates and extracts TAR archives with optional metadata preservation
    and deterministic output for reproducible builds.
    """
    
    deterministic: bool = field(default=True)
    preserve_metadata: bool = field(default=True)
    preserve_permissions: bool = field(default=True)
    
    def create(self, source: Path, output: Path) -> Path:
        """
        Create TAR archive from source.
        
        Args:
            source: Source file or directory to archive
            output: Output TAR file path
            
        Returns:
            Path to created archive
            
        Raises:
            ArchiveError: If archive creation fails
        """
        try:
            ensure_parent_dir(output)
            
            with tarfile.open(output, "w") as tar:
                if source.is_dir():
                    # Add all files in directory
                    for item in sorted(source.rglob("*")):
                        if item.is_file():
                            arcname = item.relative_to(source.parent)
                            self._add_file(tar, item, arcname)
                else:
                    # Add single file
                    self._add_file(tar, source, source.name)
            
            logger.debug(f"Created TAR archive: {output}")
            return output
            
        except Exception as e:
            raise ArchiveError(f"Failed to create TAR archive: {e}") from e

    def extract(self, archive: Path, output: Path) -> Path:
        """
        Extract TAR archive to output directory.
        
        Args:
            archive: TAR archive file path
            output: Output directory path
            
        Returns:
            Path to extraction directory
            
        Raises:
            ArchiveError: If extraction fails
        """
        try:
            output.mkdir(parents=True, exist_ok=True)
            
            with tarfile.open(archive, "r") as tar:
                # Security check - prevent path traversal
                for member in tar.getmembers():
                    if member.name.startswith("/") or ".." in member.name:
                        raise ArchiveError(f"Unsafe path in archive: {member.name}")
                
                # Extract all
                tar.extractall(output)
            
            logger.debug(f"Extracted TAR archive to: {output}")
            return output
            
        except Exception as e:
            raise ArchiveError(f"Failed to extract TAR archive: {e}") from e

    def validate(self, archive: Path) -> bool:
        """
        Validate TAR archive integrity.
        
        Args:
            archive: TAR archive file path
            
        Returns:
            True if archive is valid, False otherwise
        """
        try:
            with tarfile.open(archive, "r") as tar:
                # Try to read all members
                for member in tar.getmembers():
                    # Just checking we can read the metadata
                    pass
            return True
        except Exception:
            return False
    
    def list_contents(self, archive: Path) -> list[str]:
        """
        List contents of TAR archive.
        
        Args:
            archive: TAR archive file path
            
        Returns:
            List of file paths in archive
            
        Raises:
            ArchiveError: If listing fails
        """
        try:
            contents = []
            with tarfile.open(archive, "r") as tar:
                for member in tar.getmembers():
                    if member.isfile():
                        contents.append(member.name)
            return sorted(contents)
        except Exception as e:
            raise ArchiveError(f"Failed to list TAR contents: {e}") from e
    
    def _add_file(self, tar: tarfile.TarFile, file_path: Path, arcname: str | Path) -> None:
        """
        Add single file to TAR archive.
        
        Args:
            tar: Open TarFile object
            file_path: Path to file to add
            arcname: Name in archive
        """
        tarinfo = tar.gettarinfo(str(file_path), str(arcname))
        
        if self.deterministic:
            # Set consistent metadata for reproducible archives
            tarinfo.uid = 0
            tarinfo.gid = 0
            tarinfo.uname = ""
            tarinfo.gname = ""
            tarinfo.mtime = 0
        
        if not self.preserve_permissions:
            # Normalize permissions
            if tarinfo.isfile():
                tarinfo.mode = 0o644
            elif tarinfo.isdir():
                tarinfo.mode = 0o755
        
        with open(file_path, "rb") as f:
            tar.addfile(tarinfo, f)