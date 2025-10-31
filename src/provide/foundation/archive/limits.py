#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from __future__ import annotations

from pathlib import Path

from attrs import define, field

from provide.foundation.archive.base import ArchiveError
from provide.foundation.archive.defaults import (
    DEFAULT_ARCHIVE_LIMITS_ENABLED,
    DEFAULT_ARCHIVE_MAX_COMPRESSION_RATIO,
    DEFAULT_ARCHIVE_MAX_FILE_COUNT,
    DEFAULT_ARCHIVE_MAX_SINGLE_FILE_SIZE,
    DEFAULT_ARCHIVE_MAX_TOTAL_SIZE,
)

"""Archive extraction limits for decompression bomb protection."""


@define(slots=True)
class ArchiveLimits:
    """Configurable limits for archive extraction to prevent decompression bombs.

    Attributes:
        max_total_size: Maximum total extracted size in bytes (default: 1GB)
        max_file_count: Maximum number of files in archive (default: 10,000)
        max_compression_ratio: Maximum compression ratio (default: 100:1)
        max_single_file_size: Maximum size of any single file (default: 100MB)
        enabled: Whether to enforce limits (default: True)

    """

    max_total_size: int = field(default=DEFAULT_ARCHIVE_MAX_TOTAL_SIZE)
    max_file_count: int = field(default=DEFAULT_ARCHIVE_MAX_FILE_COUNT)
    max_compression_ratio: float = field(default=DEFAULT_ARCHIVE_MAX_COMPRESSION_RATIO)
    max_single_file_size: int = field(default=DEFAULT_ARCHIVE_MAX_SINGLE_FILE_SIZE)
    enabled: bool = field(default=DEFAULT_ARCHIVE_LIMITS_ENABLED)


# Global default limits instance
DEFAULT_LIMITS = ArchiveLimits()


class ExtractionTracker:
    """Track extraction progress to enforce limits."""

    def __init__(self, limits: ArchiveLimits) -> None:
        """Initialize tracker with limits.

        Args:
            limits: Archive extraction limits

        """
        self.limits = limits
        self.total_extracted_size = 0
        self.file_count = 0
        self.compressed_size = 0

    def check_file_count(self, count: int = 1) -> None:
        """Check if adding files would exceed limit.

        Args:
            count: Number of files to add

        Raises:
            ArchiveError: If file count would exceed limit

        """
        if not self.limits.enabled:
            return

        self.file_count += count
        if self.file_count > self.limits.max_file_count:
            raise ArchiveError(
                f"Archive exceeds maximum file count: {self.file_count} > {self.limits.max_file_count}",
                code="MAX_FILE_COUNT_EXCEEDED",
            )

    def check_file_size(self, size: int) -> None:
        """Check if file size exceeds single file limit.

        Args:
            size: File size in bytes

        Raises:
            ArchiveError: If file size exceeds limit

        """
        if not self.limits.enabled:
            return

        if size > self.limits.max_single_file_size:
            raise ArchiveError(
                f"File size exceeds maximum: {size} > {self.limits.max_single_file_size}",
                code="MAX_FILE_SIZE_EXCEEDED",
            )

    def add_extracted_size(self, size: int) -> None:
        """Track extracted size and check total limit.

        Args:
            size: Size of extracted content in bytes

        Raises:
            ArchiveError: If total extracted size exceeds limit

        """
        if not self.limits.enabled:
            return

        self.total_extracted_size += size
        if self.total_extracted_size > self.limits.max_total_size:
            raise ArchiveError(
                f"Total extracted size exceeds maximum: {self.total_extracted_size} > {self.limits.max_total_size}",
                code="MAX_TOTAL_SIZE_EXCEEDED",
            )

    def set_compressed_size(self, size: int) -> None:
        """Set the compressed archive size for ratio calculation.

        Args:
            size: Compressed archive size in bytes

        """
        self.compressed_size = size

    def check_compression_ratio(self) -> None:
        """Check if compression ratio exceeds limit.

        Raises:
            ArchiveError: If compression ratio exceeds limit

        """
        if not self.limits.enabled or self.compressed_size == 0:
            return

        ratio = self.total_extracted_size / self.compressed_size
        if ratio > self.limits.max_compression_ratio:
            raise ArchiveError(
                f"Compression ratio exceeds maximum: {ratio:.1f} > {self.limits.max_compression_ratio}",
                code="MAX_COMPRESSION_RATIO_EXCEEDED",
            )

    def validate_member_size(self, member_size: int, compressed_member_size: int | None = None) -> None:
        """Validate a single archive member before extraction.

        Args:
            member_size: Uncompressed size of the member
            compressed_member_size: Optional compressed size for ratio check

        Raises:
            ArchiveError: If member violates any limits

        """
        # Check single file size limit
        self.check_file_size(member_size)

        # Check that adding this file won't exceed total size
        if self.limits.enabled and (self.total_extracted_size + member_size) > self.limits.max_total_size:
            raise ArchiveError(
                f"Extracting this file would exceed total size limit: "
                f"{self.total_extracted_size + member_size} > {self.limits.max_total_size}",
                code="MAX_TOTAL_SIZE_EXCEEDED",
            )

        # Check individual file compression ratio if available
        if compressed_member_size and compressed_member_size > 0:
            member_ratio = member_size / compressed_member_size
            if self.limits.enabled and member_ratio > self.limits.max_compression_ratio:
                raise ArchiveError(
                    f"File compression ratio exceeds maximum: {member_ratio:.1f} > {self.limits.max_compression_ratio}",
                    code="MAX_COMPRESSION_RATIO_EXCEEDED",
                )


def get_archive_size(archive_path: Path) -> int:
    """Get the size of an archive file.

    Args:
        archive_path: Path to archive file

    Returns:
        Size in bytes

    """
    return archive_path.stat().st_size


__all__ = [
    "DEFAULT_LIMITS",
    "ArchiveLimits",
    "ExtractionTracker",
    "get_archive_size",
]

# 🧱🏗️🔚
