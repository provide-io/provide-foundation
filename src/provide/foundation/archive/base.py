"""Base classes and interfaces for archive operations."""

from abc import ABC, abstractmethod
from pathlib import Path

from provide.foundation.errors import FoundationError


class ArchiveError(FoundationError):
    """Base exception for archive-related errors."""
    pass


class BaseArchive(ABC):
    """
    Abstract base class for all archive implementations.
    
    This defines the common interface that all archive implementations
    must follow, ensuring consistency across different archive formats.
    """
    
    @abstractmethod
    def create(self, source: Path, output: Path) -> Path:
        """
        Create an archive from source path.
        
        Args:
            source: Source file or directory to archive
            output: Output archive file path
            
        Returns:
            Path to the created archive file
            
        Raises:
            ArchiveError: If archive creation fails
        """
        pass
    
    @abstractmethod
    def extract(self, archive: Path, output: Path) -> Path:
        """
        Extract an archive to output path.
        
        Args:
            archive: Archive file to extract
            output: Output directory for extracted contents
            
        Returns:
            Path to the extraction directory
            
        Raises:
            ArchiveError: If extraction fails
        """
        pass
    
    @abstractmethod
    def validate(self, archive: Path) -> bool:
        """
        Validate that an archive is properly formed.
        
        Args:
            archive: Archive file to validate
            
        Returns:
            True if archive is valid, False otherwise
            
        Raises:
            ArchiveError: If validation cannot be performed
        """
        pass