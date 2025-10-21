# provide/foundation/archive/base.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, BinaryIO

from attrs import Attribute, define, validators

from provide.foundation.config.base import field
from provide.foundation.errors import FoundationError
from provide.foundation.file import ensure_parent_dir
from provide.foundation.logger import get_logger

"""Base classes and interfaces for archive operations."""

log = get_logger(__name__)
from inspect import signature as _mutmut_signature
from typing import Annotated
from typing import Callable
from typing import ClassVar


MutantDict = Annotated[dict[str, Callable], "Mutant"]


def _mutmut_trampoline(orig, mutants, call_args, call_kwargs, self_arg = None):
    """Forward call to original or mutated function, depending on the environment"""
    import os
    mutant_under_test = os.environ['MUTANT_UNDER_TEST']
    if mutant_under_test == 'fail':
        from mutmut.__main__ import MutmutProgrammaticFailException
        raise MutmutProgrammaticFailException('Failed programmatically')      
    elif mutant_under_test == 'stats':
        from mutmut.__main__ import record_trampoline_hit
        record_trampoline_hit(orig.__module__ + '.' + orig.__name__)
        result = orig(*call_args, **call_kwargs)
        return result
    prefix = orig.__module__ + '.' + orig.__name__ + '__mutmut_'
    if not mutant_under_test.startswith(prefix):
        result = orig(*call_args, **call_kwargs)
        return result
    mutant_name = mutant_under_test.rpartition('.')[-1]
    if self_arg:
        # call to a class method where self is not bound
        result = mutants[mutant_name](self_arg, *call_args, **call_kwargs)
    else:
        result = mutants[mutant_name](*call_args, **call_kwargs)
    return result


class ArchiveError(FoundationError):
    """Base exception for archive-related errors."""


class ArchiveValidationError(ArchiveError):
    """Archive validation failed (security checks, malformed paths, etc)."""


class ArchiveFormatError(ArchiveError):
    """Archive format is invalid or corrupted."""


class ArchiveIOError(ArchiveError):
    """I/O operation failed during archive processing."""


def x__validate_compression_level__mutmut_orig(instance: Any, attribute: Attribute[int], value: int) -> None:
    """Validate compression level is between 1 and 9."""
    if not 1 <= value <= 9:
        raise ValueError(f"Compression level must be 1-9, got {value}")


def x__validate_compression_level__mutmut_1(instance: Any, attribute: Attribute[int], value: int) -> None:
    """Validate compression level is between 1 and 9."""
    if 1 <= value <= 9:
        raise ValueError(f"Compression level must be 1-9, got {value}")


def x__validate_compression_level__mutmut_2(instance: Any, attribute: Attribute[int], value: int) -> None:
    """Validate compression level is between 1 and 9."""
    if not 2 <= value <= 9:
        raise ValueError(f"Compression level must be 1-9, got {value}")


def x__validate_compression_level__mutmut_3(instance: Any, attribute: Attribute[int], value: int) -> None:
    """Validate compression level is between 1 and 9."""
    if not 1 < value <= 9:
        raise ValueError(f"Compression level must be 1-9, got {value}")


def x__validate_compression_level__mutmut_4(instance: Any, attribute: Attribute[int], value: int) -> None:
    """Validate compression level is between 1 and 9."""
    if not 1 <= value < 9:
        raise ValueError(f"Compression level must be 1-9, got {value}")


def x__validate_compression_level__mutmut_5(instance: Any, attribute: Attribute[int], value: int) -> None:
    """Validate compression level is between 1 and 9."""
    if not 1 <= value <= 10:
        raise ValueError(f"Compression level must be 1-9, got {value}")


def x__validate_compression_level__mutmut_6(instance: Any, attribute: Attribute[int], value: int) -> None:
    """Validate compression level is between 1 and 9."""
    if not 1 <= value <= 9:
        raise ValueError(None)

x__validate_compression_level__mutmut_mutants : ClassVar[MutantDict] = {
'x__validate_compression_level__mutmut_1': x__validate_compression_level__mutmut_1, 
    'x__validate_compression_level__mutmut_2': x__validate_compression_level__mutmut_2, 
    'x__validate_compression_level__mutmut_3': x__validate_compression_level__mutmut_3, 
    'x__validate_compression_level__mutmut_4': x__validate_compression_level__mutmut_4, 
    'x__validate_compression_level__mutmut_5': x__validate_compression_level__mutmut_5, 
    'x__validate_compression_level__mutmut_6': x__validate_compression_level__mutmut_6
}

def _validate_compression_level(*args, **kwargs):
    result = _mutmut_trampoline(x__validate_compression_level__mutmut_orig, x__validate_compression_level__mutmut_mutants, args, kwargs)
    return result 

_validate_compression_level.__signature__ = _mutmut_signature(x__validate_compression_level__mutmut_orig)
x__validate_compression_level__mutmut_orig.__name__ = 'x__validate_compression_level'


class BaseArchive(ABC):
    """Abstract base class for all archive implementations.

    This defines the common interface that all archive implementations
    must follow, ensuring consistency across different archive formats.
    """

    @abstractmethod
    def create(self, source: Path, output: Path) -> Path:
        """Create an archive from source path.

        Args:
            source: Source file or directory to archive
            output: Output archive file path

        Returns:
            Path to the created archive file

        Raises:
            ArchiveError: If archive creation fails

        """

    @abstractmethod
    def extract(self, archive: Path, output: Path) -> Path:
        """Extract an archive to output path.

        Args:
            archive: Archive file to extract
            output: Output directory for extracted contents

        Returns:
            Path to the extraction directory

        Raises:
            ArchiveError: If extraction fails

        """

    @abstractmethod
    def validate(self, archive: Path) -> bool:
        """Validate that an archive is properly formed.

        Args:
            archive: Archive file to validate

        Returns:
            True if archive is valid, False otherwise

        Raises:
            ArchiveError: If validation cannot be performed

        """


@define(slots=True)
class BaseCompressor(ABC):
    """Abstract base class for compression implementations.

    Provides common compression/decompression interface for stream, file, and bytes operations.
    Subclasses must implement the library-specific compression/decompression methods.
    """

    level: int = field(
        validator=validators.and_(validators.instance_of(int), _validate_compression_level),
    )  # Compression level 1-9 (1=fast, 9=best)

    @property
    @abstractmethod
    def format_name(self) -> str:
        """Return the name of the compression format (e.g., 'GZIP', 'BZIP2')."""

    @abstractmethod
    def _compress_stream(self, input_stream: BinaryIO, output_stream: BinaryIO) -> None:
        """Library-specific stream compression implementation."""

    @abstractmethod
    def _decompress_stream(self, input_stream: BinaryIO, output_stream: BinaryIO) -> None:
        """Library-specific stream decompression implementation."""

    @abstractmethod
    def _compress_bytes_impl(self, data: bytes) -> bytes:
        """Library-specific bytes compression implementation."""

    @abstractmethod
    def _decompress_bytes_impl(self, data: bytes) -> bytes:
        """Library-specific bytes decompression implementation."""

    def compress(self, input_stream: BinaryIO, output_stream: BinaryIO) -> None:
        """Compress data from input stream to output stream.

        Args:
            input_stream: Input binary stream
            output_stream: Output binary stream

        Raises:
            ArchiveError: If compression fails

        """
        try:
            self._compress_stream(input_stream, output_stream)
            log.debug(f"Compressed data with {self.format_name} level {self.level}")
        except (OSError, ValueError) as e:
            raise ArchiveError(f"Failed to compress with {self.format_name}: {e}") from e

    def decompress(self, input_stream: BinaryIO, output_stream: BinaryIO) -> None:
        """Decompress data from input stream to output stream.

        Args:
            input_stream: Input binary stream (compressed)
            output_stream: Output binary stream

        Raises:
            ArchiveError: If decompression fails

        """
        try:
            self._decompress_stream(input_stream, output_stream)
            log.debug(f"Decompressed {self.format_name} data")
        except (OSError, ValueError) as e:
            raise ArchiveError(f"Failed to decompress {self.format_name}: {e}") from e

    def compress_file(self, input_path: Path, output_path: Path) -> Path:
        """Compress a file.

        Args:
            input_path: Input file path
            output_path: Output file path

        Returns:
            Path to compressed file

        Raises:
            ArchiveError: If compression fails

        """
        try:
            ensure_parent_dir(output_path)

            with input_path.open("rb") as f_in, output_path.open("wb") as f_out:
                self._compress_stream(f_in, f_out)

            log.debug(f"Compressed {input_path} to {output_path}")
            return output_path

        except (OSError, ValueError) as e:
            raise ArchiveError(f"Failed to compress file: {e}") from e

    def decompress_file(self, input_path: Path, output_path: Path) -> Path:
        """Decompress a file.

        Args:
            input_path: Input file path (compressed)
            output_path: Output file path

        Returns:
            Path to decompressed file

        Raises:
            ArchiveError: If decompression fails

        """
        try:
            ensure_parent_dir(output_path)

            with input_path.open("rb") as f_in, output_path.open("wb") as f_out:
                self._decompress_stream(f_in, f_out)

            log.debug(f"Decompressed {input_path} to {output_path}")
            return output_path

        except (OSError, ValueError) as e:
            raise ArchiveError(f"Failed to decompress file: {e}") from e

    def compress_bytes(self, data: bytes) -> bytes:
        """Compress bytes data.

        Args:
            data: Input bytes

        Returns:
            Compressed bytes

        Raises:
            ArchiveError: If compression fails

        """
        try:
            return self._compress_bytes_impl(data)
        except (OSError, ValueError) as e:
            raise ArchiveError(f"Failed to compress bytes: {e}") from e

    def decompress_bytes(self, data: bytes) -> bytes:
        """Decompress bytes data.

        Args:
            data: Compressed bytes

        Returns:
            Decompressed bytes

        Raises:
            ArchiveError: If decompression fails

        """
        try:
            return self._decompress_bytes_impl(data)
        except (OSError, ValueError) as e:
            raise ArchiveError(f"Failed to decompress bytes: {e}") from e


# <3 🧱🤝📦🪄
