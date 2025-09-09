"""GZIP compression implementation."""

import gzip
import shutil
from io import BytesIO
from pathlib import Path
from typing import BinaryIO

from attrs import define, field

from provide.foundation.archive.base import ArchiveError
from provide.foundation.file import ensure_parent_dir
from provide.foundation.file.utils import get_size
from provide.foundation.logger import get_logger

logger = get_logger(__name__)


@define(slots=True)
class GzipCompressor:
    """
    GZIP compression implementation.
    
    Provides GZIP compression and decompression for single files.
    Does not handle bundling - use with TarArchive for .tar.gz files.
    """
    
    level: int = field(default=6)  # Compression level 1-9 (1=fast, 9=best)
    
    @level.validator
    def _validate_level(self, attribute, value):
        if not 1 <= value <= 9:
            raise ValueError(f"Compression level must be 1-9, got {value}")
    
    def compress(self, input_stream: BinaryIO, output_stream: BinaryIO) -> None:
        """
        Compress data from input stream to output stream.
        
        Args:
            input_stream: Input binary stream
            output_stream: Output binary stream
            
        Raises:
            ArchiveError: If compression fails
        """
        try:
            with gzip.GzipFile(fileobj=output_stream, mode='wb', compresslevel=self.level) as gz:
                shutil.copyfileobj(input_stream, gz)
            logger.debug(f"Compressed data with GZIP level {self.level}")
        except Exception as e:
            raise ArchiveError(f"Failed to compress with GZIP: {e}") from e
    
    def decompress(self, input_stream: BinaryIO, output_stream: BinaryIO) -> None:
        """
        Decompress data from input stream to output stream.
        
        Args:
            input_stream: Input binary stream (gzipped)
            output_stream: Output binary stream
            
        Raises:
            ArchiveError: If decompression fails
        """
        try:
            with gzip.GzipFile(fileobj=input_stream, mode='rb') as gz:
                shutil.copyfileobj(gz, output_stream)
            logger.debug("Decompressed GZIP data")
        except Exception as e:
            raise ArchiveError(f"Failed to decompress GZIP: {e}") from e
    
    def compress_file(self, input_path: Path, output_path: Path) -> Path:
        """
        Compress a file.
        
        Args:
            input_path: Input file path
            output_path: Output file path (should end with .gz)
            
        Returns:
            Path to compressed file
            
        Raises:
            ArchiveError: If compression fails
        """
        try:
            ensure_parent_dir(output_path)
            
            with open(input_path, 'rb') as f_in:
                with gzip.open(output_path, 'wb', compresslevel=self.level) as f_out:
                    shutil.copyfileobj(f_in, f_out)
            
            logger.debug(f"Compressed {input_path} to {output_path}")
            return output_path
            
        except Exception as e:
            raise ArchiveError(f"Failed to compress file: {e}") from e
    
    def decompress_file(self, input_path: Path, output_path: Path) -> Path:
        """
        Decompress a file.
        
        Args:
            input_path: Input file path (gzipped)
            output_path: Output file path
            
        Returns:
            Path to decompressed file
            
        Raises:
            ArchiveError: If decompression fails
        """
        try:
            ensure_parent_dir(output_path)
            
            with gzip.open(input_path, 'rb') as f_in:
                with open(output_path, 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
            
            logger.debug(f"Decompressed {input_path} to {output_path}")
            return output_path
            
        except Exception as e:
            raise ArchiveError(f"Failed to decompress file: {e}") from e
    
    def compress_bytes(self, data: bytes) -> bytes:
        """
        Compress bytes data.
        
        Args:
            data: Input bytes
            
        Returns:
            Compressed bytes
            
        Raises:
            ArchiveError: If compression fails
        """
        try:
            return gzip.compress(data, compresslevel=self.level)
        except Exception as e:
            raise ArchiveError(f"Failed to compress bytes: {e}") from e
    
    def decompress_bytes(self, data: bytes) -> bytes:
        """
        Decompress bytes data.
        
        Args:
            data: Compressed bytes
            
        Returns:
            Decompressed bytes
            
        Raises:
            ArchiveError: If decompression fails
        """
        try:
            return gzip.decompress(data)
        except Exception as e:
            raise ArchiveError(f"Failed to decompress bytes: {e}") from e