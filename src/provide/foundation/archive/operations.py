"""Archive operation chains and helpers."""

import tempfile
from pathlib import Path
from typing import Callable

from attrs import define, field

from provide.foundation.archive.base import ArchiveError
from provide.foundation.archive.tar import TarArchive
from provide.foundation.archive.gzip import GzipCompressor
from provide.foundation.archive.bzip2 import Bzip2Compressor
from provide.foundation.archive.zip import ZipArchive
from provide.foundation.file import ensure_parent_dir
from provide.foundation.file.safe import safe_delete
from provide.foundation.logger import get_logger

logger = get_logger(__name__)


@define(slots=True)
class OperationChain:
    """
    Chain multiple archive operations together.
    
    Enables complex operations like tar.gz, tar.bz2, etc.
    Operations are executed in order for creation, reversed for extraction.
    """
    
    operations: list[str] = field(factory=list)
    
    def execute(self, source: Path, output: Path) -> Path:
        """
        Execute operation chain on source.
        
        Args:
            source: Source file or directory
            output: Final output path
            
        Returns:
            Path to final output
            
        Raises:
            ArchiveError: If any operation fails
        """
        current = source
        temp_files = []
        
        try:
            for i, op in enumerate(self.operations):
                # Determine output for this operation
                if i == len(self.operations) - 1:
                    # Last operation, use final output
                    next_output = output
                else:
                    # Intermediate operation, use temp file
                    suffix = self._get_suffix_for_operation(op)
                    temp = tempfile.NamedTemporaryFile(suffix=suffix, delete=False)
                    temp.close()
                    next_output = Path(temp.name)
                    temp_files.append(next_output)
                
                # Execute operation
                current = self._execute_operation(op, current, next_output)
                logger.debug(f"Executed operation '{op}': {current}")
            
            return current
            
        except Exception as e:
            raise ArchiveError(f"Operation chain failed: {e}") from e
        finally:
            # Clean up temp files using Foundation's safe file operations
            for temp in temp_files:
                safe_delete(temp, missing_ok=True)
    
    def reverse(self, source: Path, output: Path) -> Path:
        """
        Reverse operation chain (extract/decompress).
        
        Args:
            source: Source archive
            output: Final output path
            
        Returns:
            Path to final output
            
        Raises:
            ArchiveError: If any operation fails
        """
        # Reverse the operations and invert them
        reverse_map = {
            'tar': 'untar',
            'untar': 'tar',
            'gzip': 'gunzip', 
            'gunzip': 'gzip',
            'bzip2': 'bunzip2',
            'bunzip2': 'bzip2',
            'zip': 'unzip',
            'unzip': 'zip',
        }
        
        reversed_ops = []
        for op in reversed(self.operations):
            reversed_op = reverse_map.get(op.lower(), op)
            reversed_ops.append(reversed_op)
        
        reversed_chain = OperationChain(operations=reversed_ops)
        return reversed_chain.execute(source, output)
    
    def _execute_operation(self, operation: str, source: Path, output: Path) -> Path:
        """Execute a single operation."""
        match operation.lower():
            case "tar":
                tar = TarArchive()
                return tar.create(source, output)
            case "untar":
                tar = TarArchive()
                return tar.extract(source, output)
            case "gzip":
                gzip = GzipCompressor()
                return gzip.compress_file(source, output)
            case "gunzip":
                gzip = GzipCompressor()
                return gzip.decompress_file(source, output)
            case "bzip2":
                bz2 = Bzip2Compressor()
                return bz2.compress_file(source, output)
            case "bunzip2":
                bz2 = Bzip2Compressor()
                return bz2.decompress_file(source, output)
            case "zip":
                zip_archive = ZipArchive()
                return zip_archive.create(source, output)
            case "unzip":
                zip_archive = ZipArchive()
                return zip_archive.extract(source, output)
            case _:
                raise ArchiveError(f"Unknown operation: {operation}")
    
    def _get_suffix_for_operation(self, operation: str) -> str:
        """Get file suffix for operation."""
        suffixes = {
            "tar": ".tar",
            "gzip": ".gz",
            "bzip2": ".bz2",
            "zip": ".zip",
        }
        return suffixes.get(operation.lower(), ".tmp")


class ArchiveOperations:
    """
    Helper class for common archive operation patterns.
    
    Provides convenient methods for common archive formats.
    """
    
    @staticmethod
    def create_tar_gz(source: Path, output: Path, deterministic: bool = True) -> Path:
        """
        Create .tar.gz archive in one step.
        
        Args:
            source: Source file or directory
            output: Output path (should end with .tar.gz)
            deterministic: Create reproducible archive
            
        Returns:
            Path to created archive
            
        Raises:
            ArchiveError: If creation fails
        """
        ensure_parent_dir(output)
        
        # Create temp tar file
        temp_tar = output.with_suffix('.tar')
        try:
            tar = TarArchive(deterministic=deterministic)
            tar.create(source, temp_tar)
            
            # Compress to final output
            gzip = GzipCompressor()
            return gzip.compress_file(temp_tar, output)
        finally:
            # Clean up temp file
            if temp_tar.exists():
                temp_tar.unlink()
    
    @staticmethod
    def extract_tar_gz(archive: Path, output: Path) -> Path:
        """
        Extract .tar.gz archive in one step.
        
        Args:
            archive: Archive path
            output: Output directory
            
        Returns:
            Path to extraction directory
            
        Raises:
            ArchiveError: If extraction fails
        """
        output.mkdir(parents=True, exist_ok=True)
        
        # Decompress to temp file
        with tempfile.NamedTemporaryFile(suffix='.tar', delete=False) as temp:
            temp_tar = Path(temp.name)
        
        try:
            gzip = GzipCompressor()
            gzip.decompress_file(archive, temp_tar)
            
            # Extract tar
            tar = TarArchive()
            return tar.extract(temp_tar, output)
        finally:
            # Clean up temp file
            if temp_tar.exists():
                temp_tar.unlink()
    
    @staticmethod
    def create_tar_bz2(source: Path, output: Path, deterministic: bool = True) -> Path:
        """
        Create .tar.bz2 archive in one step.
        
        Args:
            source: Source file or directory
            output: Output path (should end with .tar.bz2)
            deterministic: Create reproducible archive
            
        Returns:
            Path to created archive
            
        Raises:
            ArchiveError: If creation fails
        """
        ensure_parent_dir(output)
        
        # Create temp tar file
        temp_tar = output.with_suffix('.tar')
        try:
            tar = TarArchive(deterministic=deterministic)
            tar.create(source, temp_tar)
            
            # Compress to final output
            bz2 = Bzip2Compressor()
            return bz2.compress_file(temp_tar, output)
        finally:
            # Clean up temp file
            if temp_tar.exists():
                temp_tar.unlink()
    
    @staticmethod
    def extract_tar_bz2(archive: Path, output: Path) -> Path:
        """
        Extract .tar.bz2 archive in one step.
        
        Args:
            archive: Archive path
            output: Output directory
            
        Returns:
            Path to extraction directory
            
        Raises:
            ArchiveError: If extraction fails
        """
        output.mkdir(parents=True, exist_ok=True)
        
        # Decompress to temp file
        with tempfile.NamedTemporaryFile(suffix='.tar', delete=False) as temp:
            temp_tar = Path(temp.name)
        
        try:
            bz2 = Bzip2Compressor()
            bz2.decompress_file(archive, temp_tar)
            
            # Extract tar
            tar = TarArchive()
            return tar.extract(temp_tar, output)
        finally:
            # Clean up temp file
            if temp_tar.exists():
                temp_tar.unlink()
    
    @staticmethod
    def detect_format(file: Path) -> list[str]:
        """
        Detect archive format and return operation chain.
        
        Args:
            file: File path to analyze
            
        Returns:
            List of operations needed to extract
            
        Raises:
            ArchiveError: If format cannot be detected
        """
        name = file.name.lower()
        
        # Check by extension
        if name.endswith('.tar.gz') or name.endswith('.tgz'):
            return ['gunzip', 'untar']
        elif name.endswith('.tar.bz2') or name.endswith('.tbz2'):
            return ['bunzip2', 'untar']
        elif name.endswith('.tar'):
            return ['untar']
        elif name.endswith('.gz'):
            return ['gunzip']
        elif name.endswith('.bz2'):
            return ['bunzip2']
        elif name.endswith('.zip'):
            return ['unzip']
        
        # Check by magic numbers
        try:
            with open(file, 'rb') as f:
                magic = f.read(4)
                
            if magic[:2] == b'\x1f\x8b':  # gzip
                return ['gunzip']
            elif magic[:3] == b'BZh':  # bzip2
                return ['bunzip2']
            elif magic[:4] == b'PK\x03\x04':  # zip
                return ['unzip']
            elif magic[:3] == b'ustar':  # tar (at offset 257)
                return ['untar']
        except Exception:
            pass
        
        raise ArchiveError(f"Cannot detect format of {file}")