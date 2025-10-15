# provide/foundation/archive/operations.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from pathlib import Path

from attrs import define, field

from provide.foundation.archive.base import ArchiveError
from provide.foundation.archive.bzip2 import Bzip2Compressor
from provide.foundation.archive.gzip import GzipCompressor
from provide.foundation.archive.tar import TarArchive
from provide.foundation.archive.types import (
    ArchiveOperation,
)
from provide.foundation.archive.xz import XzCompressor
from provide.foundation.archive.zip import ZipArchive
from provide.foundation.archive.zstd import ZstdCompressor
from provide.foundation.file import ensure_parent_dir, temp_file
from provide.foundation.file.safe import safe_delete
from provide.foundation.logger import get_logger

"""Archive operation chains and helpers."""

log = get_logger(__name__)


@define(slots=True)
class OperationChain:
    """Chain multiple archive operations together.

    Enables complex operations like tar.gz, tar.bz2, etc.
    Operations are executed in order for creation, reversed for extraction.
    """

    operations: list[ArchiveOperation] = field(factory=list)
    operation_config: dict[ArchiveOperation, dict[str, bool]] = field(factory=dict)

    def execute(self, source: Path, output: Path) -> Path:
        """Execute operation chain on source.

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
                    # Use Foundation's temp_file with cleanup=False so we manage it
                    with temp_file(suffix=suffix, cleanup=False) as temp_path:
                        next_output = temp_path
                    temp_files.append(next_output)

                # Execute operation
                current = self._execute_operation(op, current, next_output)
                log.debug(f"Executed operation '{op}': {current}")

            return current

        except Exception as e:
            raise ArchiveError(f"Operation chain failed: {e}") from e
        finally:
            # Clean up temp files using Foundation's safe file operations
            for temp in temp_files:
                safe_delete(temp, missing_ok=True)

    def reverse(self, source: Path, output: Path) -> Path:
        """Reverse operation chain (extract/decompress).

        Args:
            source: Source archive
            output: Final output path

        Returns:
            Path to final output

        Raises:
            ArchiveError: If any operation fails

        """
        # Operations are the same when reversed; the _execute_operation
        # method will handle whether to create or extract based on context
        reversed_chain = OperationChain(
            operations=list(reversed(self.operations)), operation_config=self.operation_config
        )
        return reversed_chain.execute(source, output)

    def _execute_operation(self, operation: ArchiveOperation, source: Path, output: Path) -> Path:
        """Execute a single operation."""
        config = self.operation_config.get(operation, {})

        match operation:
            case ArchiveOperation.TAR:
                tar = TarArchive(**config)
                # Detect if we're creating or extracting based on source type
                if source.is_dir():
                    return tar.create(source, output)
                return tar.extract(source, output)
            case ArchiveOperation.GZIP:
                gzip = GzipCompressor()
                # Detect if we're compressing or decompressing based on source
                if source.suffix == ".gz":
                    return gzip.decompress_file(source, output)
                return gzip.compress_file(source, output)
            case ArchiveOperation.BZIP2:
                bz2 = Bzip2Compressor()
                if source.suffix in (".bz2", ".bzip2"):
                    return bz2.decompress_file(source, output)
                return bz2.compress_file(source, output)
            case ArchiveOperation.XZ:
                xz = XzCompressor()
                if source.suffix == ".xz":
                    return xz.decompress_file(source, output)
                return xz.compress_file(source, output)
            case ArchiveOperation.ZSTD:
                zstd = ZstdCompressor()
                if source.suffix in (".zst", ".zstd"):
                    return zstd.decompress_file(source, output)
                return zstd.compress_file(source, output)
            case ArchiveOperation.ZIP:
                zip_archive = ZipArchive(**config)
                if source.is_dir():
                    return zip_archive.create(source, output)
                return zip_archive.extract(source, output)
            case _:
                raise ArchiveError(f"Unknown operation: {operation}")

    def _get_suffix_for_operation(self, operation: ArchiveOperation) -> str:
        """Get file suffix for operation."""
        suffixes = {
            ArchiveOperation.TAR: ".tar",
            ArchiveOperation.GZIP: ".gz",
            ArchiveOperation.BZIP2: ".bz2",
            ArchiveOperation.ZIP: ".zip",
            ArchiveOperation.XZ: ".xz",
            ArchiveOperation.ZSTD: ".zst",
        }
        return suffixes.get(operation, ".tmp")


class ArchiveOperations:
    """Helper class for common archive operation patterns.

    Provides convenient methods for common archive formats.
    """

    @staticmethod
    def create_tar_gz(source: Path, output: Path, deterministic: bool = True) -> Path:
        """Create .tar.gz archive in one step.

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

        chain = OperationChain(
            operations=[ArchiveOperation.TAR, ArchiveOperation.GZIP],
            operation_config={ArchiveOperation.TAR: {"deterministic": deterministic}},
        )
        return chain.execute(source, output)

    @staticmethod
    def extract_tar_gz(archive: Path, output: Path) -> Path:
        """Extract .tar.gz archive in one step.

        Args:
            archive: Archive path
            output: Output directory

        Returns:
            Path to extraction directory

        Raises:
            ArchiveError: If extraction fails

        """
        output.mkdir(parents=True, exist_ok=True)

        chain = OperationChain(operations=[ArchiveOperation.TAR, ArchiveOperation.GZIP])
        return chain.reverse(archive, output)

    @staticmethod
    def create_tar_bz2(source: Path, output: Path, deterministic: bool = True) -> Path:
        """Create .tar.bz2 archive in one step.

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

        chain = OperationChain(
            operations=[ArchiveOperation.TAR, ArchiveOperation.BZIP2],
            operation_config={ArchiveOperation.TAR: {"deterministic": deterministic}},
        )
        return chain.execute(source, output)

    @staticmethod
    def extract_tar_bz2(archive: Path, output: Path) -> Path:
        """Extract .tar.bz2 archive in one step.

        Args:
            archive: Archive path
            output: Output directory

        Returns:
            Path to extraction directory

        Raises:
            ArchiveError: If extraction fails

        """
        output.mkdir(parents=True, exist_ok=True)

        chain = OperationChain(operations=[ArchiveOperation.TAR, ArchiveOperation.BZIP2])
        return chain.reverse(archive, output)

    @staticmethod
    def _detect_format_by_extension(filename: str) -> list[ArchiveOperation] | None:
        """Detect archive format by file extension."""
        name = filename.lower()

        if name.endswith(".tar.gz") or name.endswith(".tgz"):
            return [ArchiveOperation.GZIP, ArchiveOperation.TAR]
        if name.endswith(".tar.bz2") or name.endswith(".tbz2"):
            return [ArchiveOperation.BZIP2, ArchiveOperation.TAR]
        if name.endswith(".tar.xz") or name.endswith(".txz"):
            return [ArchiveOperation.XZ, ArchiveOperation.TAR]
        if name.endswith(".tar.zst") or name.endswith(".tzst"):
            return [ArchiveOperation.ZSTD, ArchiveOperation.TAR]
        if name.endswith(".tar"):
            return [ArchiveOperation.TAR]
        if name.endswith(".gz"):
            return [ArchiveOperation.GZIP]
        if name.endswith(".bz2"):
            return [ArchiveOperation.BZIP2]
        if name.endswith(".xz"):
            return [ArchiveOperation.XZ]
        if name.endswith(".zst") or name.endswith(".zstd"):
            return [ArchiveOperation.ZSTD]
        if name.endswith(".zip"):
            return [ArchiveOperation.ZIP]

        return None

    @staticmethod
    def _detect_format_by_magic(file: Path) -> list[ArchiveOperation] | None:
        """Detect archive format by magic numbers.

        Note: This method intentionally catches all exceptions and returns None.
        This is NOT an error suppression case - returning None is the expected
        behavior when detection fails, allowing the caller to try fallback methods
        like extension-based detection. Do NOT replace this with @resilient decorator.
        """
        try:
            with file.open("rb") as f:
                # Read first 4 bytes for common formats
                magic = f.read(4)

                # Check common formats first
                if magic[:2] == b"\x1f\x8b":  # gzip
                    return [ArchiveOperation.GZIP]
                if magic[:3] == b"BZh":  # bzip2
                    return [ArchiveOperation.BZIP2]
                if magic[:4] == b"PK\x03\x04":  # zip
                    return [ArchiveOperation.ZIP]

                # Check for tar (ustar magic at offset 257)
                f.seek(257)
                ustar_magic = f.read(5)
                if ustar_magic == b"ustar":
                    return [ArchiveOperation.TAR]
        except Exception:  # nosec B110
            # Generic catch is intentional for robust format detection.
            # Any file access error (FileNotFoundError, PermissionError, IOError, etc.)
            # should result in detection failure (return None), allowing fallback
            # to extension-based detection or final ArchiveError.
            pass

        return None

    @staticmethod
    def detect_format(file: Path) -> list[ArchiveOperation]:
        """Detect archive format and return operation chain.

        Args:
            file: File path to analyze

        Returns:
            List of operations needed to extract

        Raises:
            ArchiveError: If format cannot be detected

        """
        # Try extension-based detection first
        operations = ArchiveOperations._detect_format_by_extension(file.name)
        if operations is not None:
            return operations

        # Fall back to magic number detection
        operations = ArchiveOperations._detect_format_by_magic(file)
        if operations is not None:
            return operations

        raise ArchiveError(f"Cannot detect format of {file}")


# <3 🧱🤝📦🪄
