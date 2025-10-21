# provide/foundation/archive/limits.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

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

    def xǁExtractionTrackerǁ__init____mutmut_orig(self, limits: ArchiveLimits) -> None:
        """Initialize tracker with limits.

        Args:
            limits: Archive extraction limits

        """
        self.limits = limits
        self.total_extracted_size = 0
        self.file_count = 0
        self.compressed_size = 0

    def xǁExtractionTrackerǁ__init____mutmut_1(self, limits: ArchiveLimits) -> None:
        """Initialize tracker with limits.

        Args:
            limits: Archive extraction limits

        """
        self.limits = None
        self.total_extracted_size = 0
        self.file_count = 0
        self.compressed_size = 0

    def xǁExtractionTrackerǁ__init____mutmut_2(self, limits: ArchiveLimits) -> None:
        """Initialize tracker with limits.

        Args:
            limits: Archive extraction limits

        """
        self.limits = limits
        self.total_extracted_size = None
        self.file_count = 0
        self.compressed_size = 0

    def xǁExtractionTrackerǁ__init____mutmut_3(self, limits: ArchiveLimits) -> None:
        """Initialize tracker with limits.

        Args:
            limits: Archive extraction limits

        """
        self.limits = limits
        self.total_extracted_size = 1
        self.file_count = 0
        self.compressed_size = 0

    def xǁExtractionTrackerǁ__init____mutmut_4(self, limits: ArchiveLimits) -> None:
        """Initialize tracker with limits.

        Args:
            limits: Archive extraction limits

        """
        self.limits = limits
        self.total_extracted_size = 0
        self.file_count = None
        self.compressed_size = 0

    def xǁExtractionTrackerǁ__init____mutmut_5(self, limits: ArchiveLimits) -> None:
        """Initialize tracker with limits.

        Args:
            limits: Archive extraction limits

        """
        self.limits = limits
        self.total_extracted_size = 0
        self.file_count = 1
        self.compressed_size = 0

    def xǁExtractionTrackerǁ__init____mutmut_6(self, limits: ArchiveLimits) -> None:
        """Initialize tracker with limits.

        Args:
            limits: Archive extraction limits

        """
        self.limits = limits
        self.total_extracted_size = 0
        self.file_count = 0
        self.compressed_size = None

    def xǁExtractionTrackerǁ__init____mutmut_7(self, limits: ArchiveLimits) -> None:
        """Initialize tracker with limits.

        Args:
            limits: Archive extraction limits

        """
        self.limits = limits
        self.total_extracted_size = 0
        self.file_count = 0
        self.compressed_size = 1
    
    xǁExtractionTrackerǁ__init____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁExtractionTrackerǁ__init____mutmut_1': xǁExtractionTrackerǁ__init____mutmut_1, 
        'xǁExtractionTrackerǁ__init____mutmut_2': xǁExtractionTrackerǁ__init____mutmut_2, 
        'xǁExtractionTrackerǁ__init____mutmut_3': xǁExtractionTrackerǁ__init____mutmut_3, 
        'xǁExtractionTrackerǁ__init____mutmut_4': xǁExtractionTrackerǁ__init____mutmut_4, 
        'xǁExtractionTrackerǁ__init____mutmut_5': xǁExtractionTrackerǁ__init____mutmut_5, 
        'xǁExtractionTrackerǁ__init____mutmut_6': xǁExtractionTrackerǁ__init____mutmut_6, 
        'xǁExtractionTrackerǁ__init____mutmut_7': xǁExtractionTrackerǁ__init____mutmut_7
    }
    
    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁExtractionTrackerǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁExtractionTrackerǁ__init____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __init__.__signature__ = _mutmut_signature(xǁExtractionTrackerǁ__init____mutmut_orig)
    xǁExtractionTrackerǁ__init____mutmut_orig.__name__ = 'xǁExtractionTrackerǁ__init__'

    def xǁExtractionTrackerǁcheck_file_count__mutmut_orig(self, count: int = 1) -> None:
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

    def xǁExtractionTrackerǁcheck_file_count__mutmut_1(self, count: int = 2) -> None:
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

    def xǁExtractionTrackerǁcheck_file_count__mutmut_2(self, count: int = 1) -> None:
        """Check if adding files would exceed limit.

        Args:
            count: Number of files to add

        Raises:
            ArchiveError: If file count would exceed limit

        """
        if self.limits.enabled:
            return

        self.file_count += count
        if self.file_count > self.limits.max_file_count:
            raise ArchiveError(
                f"Archive exceeds maximum file count: {self.file_count} > {self.limits.max_file_count}",
                code="MAX_FILE_COUNT_EXCEEDED",
            )

    def xǁExtractionTrackerǁcheck_file_count__mutmut_3(self, count: int = 1) -> None:
        """Check if adding files would exceed limit.

        Args:
            count: Number of files to add

        Raises:
            ArchiveError: If file count would exceed limit

        """
        if not self.limits.enabled:
            return

        self.file_count = count
        if self.file_count > self.limits.max_file_count:
            raise ArchiveError(
                f"Archive exceeds maximum file count: {self.file_count} > {self.limits.max_file_count}",
                code="MAX_FILE_COUNT_EXCEEDED",
            )

    def xǁExtractionTrackerǁcheck_file_count__mutmut_4(self, count: int = 1) -> None:
        """Check if adding files would exceed limit.

        Args:
            count: Number of files to add

        Raises:
            ArchiveError: If file count would exceed limit

        """
        if not self.limits.enabled:
            return

        self.file_count -= count
        if self.file_count > self.limits.max_file_count:
            raise ArchiveError(
                f"Archive exceeds maximum file count: {self.file_count} > {self.limits.max_file_count}",
                code="MAX_FILE_COUNT_EXCEEDED",
            )

    def xǁExtractionTrackerǁcheck_file_count__mutmut_5(self, count: int = 1) -> None:
        """Check if adding files would exceed limit.

        Args:
            count: Number of files to add

        Raises:
            ArchiveError: If file count would exceed limit

        """
        if not self.limits.enabled:
            return

        self.file_count += count
        if self.file_count >= self.limits.max_file_count:
            raise ArchiveError(
                f"Archive exceeds maximum file count: {self.file_count} > {self.limits.max_file_count}",
                code="MAX_FILE_COUNT_EXCEEDED",
            )

    def xǁExtractionTrackerǁcheck_file_count__mutmut_6(self, count: int = 1) -> None:
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
                None,
                code="MAX_FILE_COUNT_EXCEEDED",
            )

    def xǁExtractionTrackerǁcheck_file_count__mutmut_7(self, count: int = 1) -> None:
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
                code=None,
            )

    def xǁExtractionTrackerǁcheck_file_count__mutmut_8(self, count: int = 1) -> None:
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
                code="MAX_FILE_COUNT_EXCEEDED",
            )

    def xǁExtractionTrackerǁcheck_file_count__mutmut_9(self, count: int = 1) -> None:
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
                )

    def xǁExtractionTrackerǁcheck_file_count__mutmut_10(self, count: int = 1) -> None:
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
                code="XXMAX_FILE_COUNT_EXCEEDEDXX",
            )

    def xǁExtractionTrackerǁcheck_file_count__mutmut_11(self, count: int = 1) -> None:
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
                code="max_file_count_exceeded",
            )
    
    xǁExtractionTrackerǁcheck_file_count__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁExtractionTrackerǁcheck_file_count__mutmut_1': xǁExtractionTrackerǁcheck_file_count__mutmut_1, 
        'xǁExtractionTrackerǁcheck_file_count__mutmut_2': xǁExtractionTrackerǁcheck_file_count__mutmut_2, 
        'xǁExtractionTrackerǁcheck_file_count__mutmut_3': xǁExtractionTrackerǁcheck_file_count__mutmut_3, 
        'xǁExtractionTrackerǁcheck_file_count__mutmut_4': xǁExtractionTrackerǁcheck_file_count__mutmut_4, 
        'xǁExtractionTrackerǁcheck_file_count__mutmut_5': xǁExtractionTrackerǁcheck_file_count__mutmut_5, 
        'xǁExtractionTrackerǁcheck_file_count__mutmut_6': xǁExtractionTrackerǁcheck_file_count__mutmut_6, 
        'xǁExtractionTrackerǁcheck_file_count__mutmut_7': xǁExtractionTrackerǁcheck_file_count__mutmut_7, 
        'xǁExtractionTrackerǁcheck_file_count__mutmut_8': xǁExtractionTrackerǁcheck_file_count__mutmut_8, 
        'xǁExtractionTrackerǁcheck_file_count__mutmut_9': xǁExtractionTrackerǁcheck_file_count__mutmut_9, 
        'xǁExtractionTrackerǁcheck_file_count__mutmut_10': xǁExtractionTrackerǁcheck_file_count__mutmut_10, 
        'xǁExtractionTrackerǁcheck_file_count__mutmut_11': xǁExtractionTrackerǁcheck_file_count__mutmut_11
    }
    
    def check_file_count(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁExtractionTrackerǁcheck_file_count__mutmut_orig"), object.__getattribute__(self, "xǁExtractionTrackerǁcheck_file_count__mutmut_mutants"), args, kwargs, self)
        return result 
    
    check_file_count.__signature__ = _mutmut_signature(xǁExtractionTrackerǁcheck_file_count__mutmut_orig)
    xǁExtractionTrackerǁcheck_file_count__mutmut_orig.__name__ = 'xǁExtractionTrackerǁcheck_file_count'

    def xǁExtractionTrackerǁcheck_file_size__mutmut_orig(self, size: int) -> None:
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

    def xǁExtractionTrackerǁcheck_file_size__mutmut_1(self, size: int) -> None:
        """Check if file size exceeds single file limit.

        Args:
            size: File size in bytes

        Raises:
            ArchiveError: If file size exceeds limit

        """
        if self.limits.enabled:
            return

        if size > self.limits.max_single_file_size:
            raise ArchiveError(
                f"File size exceeds maximum: {size} > {self.limits.max_single_file_size}",
                code="MAX_FILE_SIZE_EXCEEDED",
            )

    def xǁExtractionTrackerǁcheck_file_size__mutmut_2(self, size: int) -> None:
        """Check if file size exceeds single file limit.

        Args:
            size: File size in bytes

        Raises:
            ArchiveError: If file size exceeds limit

        """
        if not self.limits.enabled:
            return

        if size >= self.limits.max_single_file_size:
            raise ArchiveError(
                f"File size exceeds maximum: {size} > {self.limits.max_single_file_size}",
                code="MAX_FILE_SIZE_EXCEEDED",
            )

    def xǁExtractionTrackerǁcheck_file_size__mutmut_3(self, size: int) -> None:
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
                None,
                code="MAX_FILE_SIZE_EXCEEDED",
            )

    def xǁExtractionTrackerǁcheck_file_size__mutmut_4(self, size: int) -> None:
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
                code=None,
            )

    def xǁExtractionTrackerǁcheck_file_size__mutmut_5(self, size: int) -> None:
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
                code="MAX_FILE_SIZE_EXCEEDED",
            )

    def xǁExtractionTrackerǁcheck_file_size__mutmut_6(self, size: int) -> None:
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
                )

    def xǁExtractionTrackerǁcheck_file_size__mutmut_7(self, size: int) -> None:
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
                code="XXMAX_FILE_SIZE_EXCEEDEDXX",
            )

    def xǁExtractionTrackerǁcheck_file_size__mutmut_8(self, size: int) -> None:
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
                code="max_file_size_exceeded",
            )
    
    xǁExtractionTrackerǁcheck_file_size__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁExtractionTrackerǁcheck_file_size__mutmut_1': xǁExtractionTrackerǁcheck_file_size__mutmut_1, 
        'xǁExtractionTrackerǁcheck_file_size__mutmut_2': xǁExtractionTrackerǁcheck_file_size__mutmut_2, 
        'xǁExtractionTrackerǁcheck_file_size__mutmut_3': xǁExtractionTrackerǁcheck_file_size__mutmut_3, 
        'xǁExtractionTrackerǁcheck_file_size__mutmut_4': xǁExtractionTrackerǁcheck_file_size__mutmut_4, 
        'xǁExtractionTrackerǁcheck_file_size__mutmut_5': xǁExtractionTrackerǁcheck_file_size__mutmut_5, 
        'xǁExtractionTrackerǁcheck_file_size__mutmut_6': xǁExtractionTrackerǁcheck_file_size__mutmut_6, 
        'xǁExtractionTrackerǁcheck_file_size__mutmut_7': xǁExtractionTrackerǁcheck_file_size__mutmut_7, 
        'xǁExtractionTrackerǁcheck_file_size__mutmut_8': xǁExtractionTrackerǁcheck_file_size__mutmut_8
    }
    
    def check_file_size(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁExtractionTrackerǁcheck_file_size__mutmut_orig"), object.__getattribute__(self, "xǁExtractionTrackerǁcheck_file_size__mutmut_mutants"), args, kwargs, self)
        return result 
    
    check_file_size.__signature__ = _mutmut_signature(xǁExtractionTrackerǁcheck_file_size__mutmut_orig)
    xǁExtractionTrackerǁcheck_file_size__mutmut_orig.__name__ = 'xǁExtractionTrackerǁcheck_file_size'

    def xǁExtractionTrackerǁadd_extracted_size__mutmut_orig(self, size: int) -> None:
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

    def xǁExtractionTrackerǁadd_extracted_size__mutmut_1(self, size: int) -> None:
        """Track extracted size and check total limit.

        Args:
            size: Size of extracted content in bytes

        Raises:
            ArchiveError: If total extracted size exceeds limit

        """
        if self.limits.enabled:
            return

        self.total_extracted_size += size
        if self.total_extracted_size > self.limits.max_total_size:
            raise ArchiveError(
                f"Total extracted size exceeds maximum: {self.total_extracted_size} > {self.limits.max_total_size}",
                code="MAX_TOTAL_SIZE_EXCEEDED",
            )

    def xǁExtractionTrackerǁadd_extracted_size__mutmut_2(self, size: int) -> None:
        """Track extracted size and check total limit.

        Args:
            size: Size of extracted content in bytes

        Raises:
            ArchiveError: If total extracted size exceeds limit

        """
        if not self.limits.enabled:
            return

        self.total_extracted_size = size
        if self.total_extracted_size > self.limits.max_total_size:
            raise ArchiveError(
                f"Total extracted size exceeds maximum: {self.total_extracted_size} > {self.limits.max_total_size}",
                code="MAX_TOTAL_SIZE_EXCEEDED",
            )

    def xǁExtractionTrackerǁadd_extracted_size__mutmut_3(self, size: int) -> None:
        """Track extracted size and check total limit.

        Args:
            size: Size of extracted content in bytes

        Raises:
            ArchiveError: If total extracted size exceeds limit

        """
        if not self.limits.enabled:
            return

        self.total_extracted_size -= size
        if self.total_extracted_size > self.limits.max_total_size:
            raise ArchiveError(
                f"Total extracted size exceeds maximum: {self.total_extracted_size} > {self.limits.max_total_size}",
                code="MAX_TOTAL_SIZE_EXCEEDED",
            )

    def xǁExtractionTrackerǁadd_extracted_size__mutmut_4(self, size: int) -> None:
        """Track extracted size and check total limit.

        Args:
            size: Size of extracted content in bytes

        Raises:
            ArchiveError: If total extracted size exceeds limit

        """
        if not self.limits.enabled:
            return

        self.total_extracted_size += size
        if self.total_extracted_size >= self.limits.max_total_size:
            raise ArchiveError(
                f"Total extracted size exceeds maximum: {self.total_extracted_size} > {self.limits.max_total_size}",
                code="MAX_TOTAL_SIZE_EXCEEDED",
            )

    def xǁExtractionTrackerǁadd_extracted_size__mutmut_5(self, size: int) -> None:
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
                None,
                code="MAX_TOTAL_SIZE_EXCEEDED",
            )

    def xǁExtractionTrackerǁadd_extracted_size__mutmut_6(self, size: int) -> None:
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
                code=None,
            )

    def xǁExtractionTrackerǁadd_extracted_size__mutmut_7(self, size: int) -> None:
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
                code="MAX_TOTAL_SIZE_EXCEEDED",
            )

    def xǁExtractionTrackerǁadd_extracted_size__mutmut_8(self, size: int) -> None:
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
                )

    def xǁExtractionTrackerǁadd_extracted_size__mutmut_9(self, size: int) -> None:
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
                code="XXMAX_TOTAL_SIZE_EXCEEDEDXX",
            )

    def xǁExtractionTrackerǁadd_extracted_size__mutmut_10(self, size: int) -> None:
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
                code="max_total_size_exceeded",
            )
    
    xǁExtractionTrackerǁadd_extracted_size__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁExtractionTrackerǁadd_extracted_size__mutmut_1': xǁExtractionTrackerǁadd_extracted_size__mutmut_1, 
        'xǁExtractionTrackerǁadd_extracted_size__mutmut_2': xǁExtractionTrackerǁadd_extracted_size__mutmut_2, 
        'xǁExtractionTrackerǁadd_extracted_size__mutmut_3': xǁExtractionTrackerǁadd_extracted_size__mutmut_3, 
        'xǁExtractionTrackerǁadd_extracted_size__mutmut_4': xǁExtractionTrackerǁadd_extracted_size__mutmut_4, 
        'xǁExtractionTrackerǁadd_extracted_size__mutmut_5': xǁExtractionTrackerǁadd_extracted_size__mutmut_5, 
        'xǁExtractionTrackerǁadd_extracted_size__mutmut_6': xǁExtractionTrackerǁadd_extracted_size__mutmut_6, 
        'xǁExtractionTrackerǁadd_extracted_size__mutmut_7': xǁExtractionTrackerǁadd_extracted_size__mutmut_7, 
        'xǁExtractionTrackerǁadd_extracted_size__mutmut_8': xǁExtractionTrackerǁadd_extracted_size__mutmut_8, 
        'xǁExtractionTrackerǁadd_extracted_size__mutmut_9': xǁExtractionTrackerǁadd_extracted_size__mutmut_9, 
        'xǁExtractionTrackerǁadd_extracted_size__mutmut_10': xǁExtractionTrackerǁadd_extracted_size__mutmut_10
    }
    
    def add_extracted_size(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁExtractionTrackerǁadd_extracted_size__mutmut_orig"), object.__getattribute__(self, "xǁExtractionTrackerǁadd_extracted_size__mutmut_mutants"), args, kwargs, self)
        return result 
    
    add_extracted_size.__signature__ = _mutmut_signature(xǁExtractionTrackerǁadd_extracted_size__mutmut_orig)
    xǁExtractionTrackerǁadd_extracted_size__mutmut_orig.__name__ = 'xǁExtractionTrackerǁadd_extracted_size'

    def xǁExtractionTrackerǁset_compressed_size__mutmut_orig(self, size: int) -> None:
        """Set the compressed archive size for ratio calculation.

        Args:
            size: Compressed archive size in bytes

        """
        self.compressed_size = size

    def xǁExtractionTrackerǁset_compressed_size__mutmut_1(self, size: int) -> None:
        """Set the compressed archive size for ratio calculation.

        Args:
            size: Compressed archive size in bytes

        """
        self.compressed_size = None
    
    xǁExtractionTrackerǁset_compressed_size__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁExtractionTrackerǁset_compressed_size__mutmut_1': xǁExtractionTrackerǁset_compressed_size__mutmut_1
    }
    
    def set_compressed_size(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁExtractionTrackerǁset_compressed_size__mutmut_orig"), object.__getattribute__(self, "xǁExtractionTrackerǁset_compressed_size__mutmut_mutants"), args, kwargs, self)
        return result 
    
    set_compressed_size.__signature__ = _mutmut_signature(xǁExtractionTrackerǁset_compressed_size__mutmut_orig)
    xǁExtractionTrackerǁset_compressed_size__mutmut_orig.__name__ = 'xǁExtractionTrackerǁset_compressed_size'

    def xǁExtractionTrackerǁcheck_compression_ratio__mutmut_orig(self) -> None:
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

    def xǁExtractionTrackerǁcheck_compression_ratio__mutmut_1(self) -> None:
        """Check if compression ratio exceeds limit.

        Raises:
            ArchiveError: If compression ratio exceeds limit

        """
        if not self.limits.enabled and self.compressed_size == 0:
            return

        ratio = self.total_extracted_size / self.compressed_size
        if ratio > self.limits.max_compression_ratio:
            raise ArchiveError(
                f"Compression ratio exceeds maximum: {ratio:.1f} > {self.limits.max_compression_ratio}",
                code="MAX_COMPRESSION_RATIO_EXCEEDED",
            )

    def xǁExtractionTrackerǁcheck_compression_ratio__mutmut_2(self) -> None:
        """Check if compression ratio exceeds limit.

        Raises:
            ArchiveError: If compression ratio exceeds limit

        """
        if self.limits.enabled or self.compressed_size == 0:
            return

        ratio = self.total_extracted_size / self.compressed_size
        if ratio > self.limits.max_compression_ratio:
            raise ArchiveError(
                f"Compression ratio exceeds maximum: {ratio:.1f} > {self.limits.max_compression_ratio}",
                code="MAX_COMPRESSION_RATIO_EXCEEDED",
            )

    def xǁExtractionTrackerǁcheck_compression_ratio__mutmut_3(self) -> None:
        """Check if compression ratio exceeds limit.

        Raises:
            ArchiveError: If compression ratio exceeds limit

        """
        if not self.limits.enabled or self.compressed_size != 0:
            return

        ratio = self.total_extracted_size / self.compressed_size
        if ratio > self.limits.max_compression_ratio:
            raise ArchiveError(
                f"Compression ratio exceeds maximum: {ratio:.1f} > {self.limits.max_compression_ratio}",
                code="MAX_COMPRESSION_RATIO_EXCEEDED",
            )

    def xǁExtractionTrackerǁcheck_compression_ratio__mutmut_4(self) -> None:
        """Check if compression ratio exceeds limit.

        Raises:
            ArchiveError: If compression ratio exceeds limit

        """
        if not self.limits.enabled or self.compressed_size == 1:
            return

        ratio = self.total_extracted_size / self.compressed_size
        if ratio > self.limits.max_compression_ratio:
            raise ArchiveError(
                f"Compression ratio exceeds maximum: {ratio:.1f} > {self.limits.max_compression_ratio}",
                code="MAX_COMPRESSION_RATIO_EXCEEDED",
            )

    def xǁExtractionTrackerǁcheck_compression_ratio__mutmut_5(self) -> None:
        """Check if compression ratio exceeds limit.

        Raises:
            ArchiveError: If compression ratio exceeds limit

        """
        if not self.limits.enabled or self.compressed_size == 0:
            return

        ratio = None
        if ratio > self.limits.max_compression_ratio:
            raise ArchiveError(
                f"Compression ratio exceeds maximum: {ratio:.1f} > {self.limits.max_compression_ratio}",
                code="MAX_COMPRESSION_RATIO_EXCEEDED",
            )

    def xǁExtractionTrackerǁcheck_compression_ratio__mutmut_6(self) -> None:
        """Check if compression ratio exceeds limit.

        Raises:
            ArchiveError: If compression ratio exceeds limit

        """
        if not self.limits.enabled or self.compressed_size == 0:
            return

        ratio = self.total_extracted_size * self.compressed_size
        if ratio > self.limits.max_compression_ratio:
            raise ArchiveError(
                f"Compression ratio exceeds maximum: {ratio:.1f} > {self.limits.max_compression_ratio}",
                code="MAX_COMPRESSION_RATIO_EXCEEDED",
            )

    def xǁExtractionTrackerǁcheck_compression_ratio__mutmut_7(self) -> None:
        """Check if compression ratio exceeds limit.

        Raises:
            ArchiveError: If compression ratio exceeds limit

        """
        if not self.limits.enabled or self.compressed_size == 0:
            return

        ratio = self.total_extracted_size / self.compressed_size
        if ratio >= self.limits.max_compression_ratio:
            raise ArchiveError(
                f"Compression ratio exceeds maximum: {ratio:.1f} > {self.limits.max_compression_ratio}",
                code="MAX_COMPRESSION_RATIO_EXCEEDED",
            )

    def xǁExtractionTrackerǁcheck_compression_ratio__mutmut_8(self) -> None:
        """Check if compression ratio exceeds limit.

        Raises:
            ArchiveError: If compression ratio exceeds limit

        """
        if not self.limits.enabled or self.compressed_size == 0:
            return

        ratio = self.total_extracted_size / self.compressed_size
        if ratio > self.limits.max_compression_ratio:
            raise ArchiveError(
                None,
                code="MAX_COMPRESSION_RATIO_EXCEEDED",
            )

    def xǁExtractionTrackerǁcheck_compression_ratio__mutmut_9(self) -> None:
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
                code=None,
            )

    def xǁExtractionTrackerǁcheck_compression_ratio__mutmut_10(self) -> None:
        """Check if compression ratio exceeds limit.

        Raises:
            ArchiveError: If compression ratio exceeds limit

        """
        if not self.limits.enabled or self.compressed_size == 0:
            return

        ratio = self.total_extracted_size / self.compressed_size
        if ratio > self.limits.max_compression_ratio:
            raise ArchiveError(
                code="MAX_COMPRESSION_RATIO_EXCEEDED",
            )

    def xǁExtractionTrackerǁcheck_compression_ratio__mutmut_11(self) -> None:
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
                )

    def xǁExtractionTrackerǁcheck_compression_ratio__mutmut_12(self) -> None:
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
                code="XXMAX_COMPRESSION_RATIO_EXCEEDEDXX",
            )

    def xǁExtractionTrackerǁcheck_compression_ratio__mutmut_13(self) -> None:
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
                code="max_compression_ratio_exceeded",
            )
    
    xǁExtractionTrackerǁcheck_compression_ratio__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁExtractionTrackerǁcheck_compression_ratio__mutmut_1': xǁExtractionTrackerǁcheck_compression_ratio__mutmut_1, 
        'xǁExtractionTrackerǁcheck_compression_ratio__mutmut_2': xǁExtractionTrackerǁcheck_compression_ratio__mutmut_2, 
        'xǁExtractionTrackerǁcheck_compression_ratio__mutmut_3': xǁExtractionTrackerǁcheck_compression_ratio__mutmut_3, 
        'xǁExtractionTrackerǁcheck_compression_ratio__mutmut_4': xǁExtractionTrackerǁcheck_compression_ratio__mutmut_4, 
        'xǁExtractionTrackerǁcheck_compression_ratio__mutmut_5': xǁExtractionTrackerǁcheck_compression_ratio__mutmut_5, 
        'xǁExtractionTrackerǁcheck_compression_ratio__mutmut_6': xǁExtractionTrackerǁcheck_compression_ratio__mutmut_6, 
        'xǁExtractionTrackerǁcheck_compression_ratio__mutmut_7': xǁExtractionTrackerǁcheck_compression_ratio__mutmut_7, 
        'xǁExtractionTrackerǁcheck_compression_ratio__mutmut_8': xǁExtractionTrackerǁcheck_compression_ratio__mutmut_8, 
        'xǁExtractionTrackerǁcheck_compression_ratio__mutmut_9': xǁExtractionTrackerǁcheck_compression_ratio__mutmut_9, 
        'xǁExtractionTrackerǁcheck_compression_ratio__mutmut_10': xǁExtractionTrackerǁcheck_compression_ratio__mutmut_10, 
        'xǁExtractionTrackerǁcheck_compression_ratio__mutmut_11': xǁExtractionTrackerǁcheck_compression_ratio__mutmut_11, 
        'xǁExtractionTrackerǁcheck_compression_ratio__mutmut_12': xǁExtractionTrackerǁcheck_compression_ratio__mutmut_12, 
        'xǁExtractionTrackerǁcheck_compression_ratio__mutmut_13': xǁExtractionTrackerǁcheck_compression_ratio__mutmut_13
    }
    
    def check_compression_ratio(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁExtractionTrackerǁcheck_compression_ratio__mutmut_orig"), object.__getattribute__(self, "xǁExtractionTrackerǁcheck_compression_ratio__mutmut_mutants"), args, kwargs, self)
        return result 
    
    check_compression_ratio.__signature__ = _mutmut_signature(xǁExtractionTrackerǁcheck_compression_ratio__mutmut_orig)
    xǁExtractionTrackerǁcheck_compression_ratio__mutmut_orig.__name__ = 'xǁExtractionTrackerǁcheck_compression_ratio'

    def xǁExtractionTrackerǁvalidate_member_size__mutmut_orig(self, member_size: int, compressed_member_size: int | None = None) -> None:
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

    def xǁExtractionTrackerǁvalidate_member_size__mutmut_1(self, member_size: int, compressed_member_size: int | None = None) -> None:
        """Validate a single archive member before extraction.

        Args:
            member_size: Uncompressed size of the member
            compressed_member_size: Optional compressed size for ratio check

        Raises:
            ArchiveError: If member violates any limits

        """
        # Check single file size limit
        self.check_file_size(None)

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

    def xǁExtractionTrackerǁvalidate_member_size__mutmut_2(self, member_size: int, compressed_member_size: int | None = None) -> None:
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
        if self.limits.enabled or (self.total_extracted_size + member_size) > self.limits.max_total_size:
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

    def xǁExtractionTrackerǁvalidate_member_size__mutmut_3(self, member_size: int, compressed_member_size: int | None = None) -> None:
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
        if self.limits.enabled and (self.total_extracted_size - member_size) > self.limits.max_total_size:
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

    def xǁExtractionTrackerǁvalidate_member_size__mutmut_4(self, member_size: int, compressed_member_size: int | None = None) -> None:
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
        if self.limits.enabled and (self.total_extracted_size + member_size) >= self.limits.max_total_size:
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

    def xǁExtractionTrackerǁvalidate_member_size__mutmut_5(self, member_size: int, compressed_member_size: int | None = None) -> None:
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
                None,
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

    def xǁExtractionTrackerǁvalidate_member_size__mutmut_6(self, member_size: int, compressed_member_size: int | None = None) -> None:
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
                code=None,
            )

        # Check individual file compression ratio if available
        if compressed_member_size and compressed_member_size > 0:
            member_ratio = member_size / compressed_member_size
            if self.limits.enabled and member_ratio > self.limits.max_compression_ratio:
                raise ArchiveError(
                    f"File compression ratio exceeds maximum: {member_ratio:.1f} > {self.limits.max_compression_ratio}",
                    code="MAX_COMPRESSION_RATIO_EXCEEDED",
                )

    def xǁExtractionTrackerǁvalidate_member_size__mutmut_7(self, member_size: int, compressed_member_size: int | None = None) -> None:
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

    def xǁExtractionTrackerǁvalidate_member_size__mutmut_8(self, member_size: int, compressed_member_size: int | None = None) -> None:
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
                )

        # Check individual file compression ratio if available
        if compressed_member_size and compressed_member_size > 0:
            member_ratio = member_size / compressed_member_size
            if self.limits.enabled and member_ratio > self.limits.max_compression_ratio:
                raise ArchiveError(
                    f"File compression ratio exceeds maximum: {member_ratio:.1f} > {self.limits.max_compression_ratio}",
                    code="MAX_COMPRESSION_RATIO_EXCEEDED",
                )

    def xǁExtractionTrackerǁvalidate_member_size__mutmut_9(self, member_size: int, compressed_member_size: int | None = None) -> None:
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
                f"{self.total_extracted_size - member_size} > {self.limits.max_total_size}",
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

    def xǁExtractionTrackerǁvalidate_member_size__mutmut_10(self, member_size: int, compressed_member_size: int | None = None) -> None:
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
                code="XXMAX_TOTAL_SIZE_EXCEEDEDXX",
            )

        # Check individual file compression ratio if available
        if compressed_member_size and compressed_member_size > 0:
            member_ratio = member_size / compressed_member_size
            if self.limits.enabled and member_ratio > self.limits.max_compression_ratio:
                raise ArchiveError(
                    f"File compression ratio exceeds maximum: {member_ratio:.1f} > {self.limits.max_compression_ratio}",
                    code="MAX_COMPRESSION_RATIO_EXCEEDED",
                )

    def xǁExtractionTrackerǁvalidate_member_size__mutmut_11(self, member_size: int, compressed_member_size: int | None = None) -> None:
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
                code="max_total_size_exceeded",
            )

        # Check individual file compression ratio if available
        if compressed_member_size and compressed_member_size > 0:
            member_ratio = member_size / compressed_member_size
            if self.limits.enabled and member_ratio > self.limits.max_compression_ratio:
                raise ArchiveError(
                    f"File compression ratio exceeds maximum: {member_ratio:.1f} > {self.limits.max_compression_ratio}",
                    code="MAX_COMPRESSION_RATIO_EXCEEDED",
                )

    def xǁExtractionTrackerǁvalidate_member_size__mutmut_12(self, member_size: int, compressed_member_size: int | None = None) -> None:
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
        if compressed_member_size or compressed_member_size > 0:
            member_ratio = member_size / compressed_member_size
            if self.limits.enabled and member_ratio > self.limits.max_compression_ratio:
                raise ArchiveError(
                    f"File compression ratio exceeds maximum: {member_ratio:.1f} > {self.limits.max_compression_ratio}",
                    code="MAX_COMPRESSION_RATIO_EXCEEDED",
                )

    def xǁExtractionTrackerǁvalidate_member_size__mutmut_13(self, member_size: int, compressed_member_size: int | None = None) -> None:
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
        if compressed_member_size and compressed_member_size >= 0:
            member_ratio = member_size / compressed_member_size
            if self.limits.enabled and member_ratio > self.limits.max_compression_ratio:
                raise ArchiveError(
                    f"File compression ratio exceeds maximum: {member_ratio:.1f} > {self.limits.max_compression_ratio}",
                    code="MAX_COMPRESSION_RATIO_EXCEEDED",
                )

    def xǁExtractionTrackerǁvalidate_member_size__mutmut_14(self, member_size: int, compressed_member_size: int | None = None) -> None:
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
        if compressed_member_size and compressed_member_size > 1:
            member_ratio = member_size / compressed_member_size
            if self.limits.enabled and member_ratio > self.limits.max_compression_ratio:
                raise ArchiveError(
                    f"File compression ratio exceeds maximum: {member_ratio:.1f} > {self.limits.max_compression_ratio}",
                    code="MAX_COMPRESSION_RATIO_EXCEEDED",
                )

    def xǁExtractionTrackerǁvalidate_member_size__mutmut_15(self, member_size: int, compressed_member_size: int | None = None) -> None:
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
            member_ratio = None
            if self.limits.enabled and member_ratio > self.limits.max_compression_ratio:
                raise ArchiveError(
                    f"File compression ratio exceeds maximum: {member_ratio:.1f} > {self.limits.max_compression_ratio}",
                    code="MAX_COMPRESSION_RATIO_EXCEEDED",
                )

    def xǁExtractionTrackerǁvalidate_member_size__mutmut_16(self, member_size: int, compressed_member_size: int | None = None) -> None:
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
            member_ratio = member_size * compressed_member_size
            if self.limits.enabled and member_ratio > self.limits.max_compression_ratio:
                raise ArchiveError(
                    f"File compression ratio exceeds maximum: {member_ratio:.1f} > {self.limits.max_compression_ratio}",
                    code="MAX_COMPRESSION_RATIO_EXCEEDED",
                )

    def xǁExtractionTrackerǁvalidate_member_size__mutmut_17(self, member_size: int, compressed_member_size: int | None = None) -> None:
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
            if self.limits.enabled or member_ratio > self.limits.max_compression_ratio:
                raise ArchiveError(
                    f"File compression ratio exceeds maximum: {member_ratio:.1f} > {self.limits.max_compression_ratio}",
                    code="MAX_COMPRESSION_RATIO_EXCEEDED",
                )

    def xǁExtractionTrackerǁvalidate_member_size__mutmut_18(self, member_size: int, compressed_member_size: int | None = None) -> None:
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
            if self.limits.enabled and member_ratio >= self.limits.max_compression_ratio:
                raise ArchiveError(
                    f"File compression ratio exceeds maximum: {member_ratio:.1f} > {self.limits.max_compression_ratio}",
                    code="MAX_COMPRESSION_RATIO_EXCEEDED",
                )

    def xǁExtractionTrackerǁvalidate_member_size__mutmut_19(self, member_size: int, compressed_member_size: int | None = None) -> None:
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
                    None,
                    code="MAX_COMPRESSION_RATIO_EXCEEDED",
                )

    def xǁExtractionTrackerǁvalidate_member_size__mutmut_20(self, member_size: int, compressed_member_size: int | None = None) -> None:
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
                    code=None,
                )

    def xǁExtractionTrackerǁvalidate_member_size__mutmut_21(self, member_size: int, compressed_member_size: int | None = None) -> None:
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
                    code="MAX_COMPRESSION_RATIO_EXCEEDED",
                )

    def xǁExtractionTrackerǁvalidate_member_size__mutmut_22(self, member_size: int, compressed_member_size: int | None = None) -> None:
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
                    )

    def xǁExtractionTrackerǁvalidate_member_size__mutmut_23(self, member_size: int, compressed_member_size: int | None = None) -> None:
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
                    code="XXMAX_COMPRESSION_RATIO_EXCEEDEDXX",
                )

    def xǁExtractionTrackerǁvalidate_member_size__mutmut_24(self, member_size: int, compressed_member_size: int | None = None) -> None:
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
                    code="max_compression_ratio_exceeded",
                )
    
    xǁExtractionTrackerǁvalidate_member_size__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁExtractionTrackerǁvalidate_member_size__mutmut_1': xǁExtractionTrackerǁvalidate_member_size__mutmut_1, 
        'xǁExtractionTrackerǁvalidate_member_size__mutmut_2': xǁExtractionTrackerǁvalidate_member_size__mutmut_2, 
        'xǁExtractionTrackerǁvalidate_member_size__mutmut_3': xǁExtractionTrackerǁvalidate_member_size__mutmut_3, 
        'xǁExtractionTrackerǁvalidate_member_size__mutmut_4': xǁExtractionTrackerǁvalidate_member_size__mutmut_4, 
        'xǁExtractionTrackerǁvalidate_member_size__mutmut_5': xǁExtractionTrackerǁvalidate_member_size__mutmut_5, 
        'xǁExtractionTrackerǁvalidate_member_size__mutmut_6': xǁExtractionTrackerǁvalidate_member_size__mutmut_6, 
        'xǁExtractionTrackerǁvalidate_member_size__mutmut_7': xǁExtractionTrackerǁvalidate_member_size__mutmut_7, 
        'xǁExtractionTrackerǁvalidate_member_size__mutmut_8': xǁExtractionTrackerǁvalidate_member_size__mutmut_8, 
        'xǁExtractionTrackerǁvalidate_member_size__mutmut_9': xǁExtractionTrackerǁvalidate_member_size__mutmut_9, 
        'xǁExtractionTrackerǁvalidate_member_size__mutmut_10': xǁExtractionTrackerǁvalidate_member_size__mutmut_10, 
        'xǁExtractionTrackerǁvalidate_member_size__mutmut_11': xǁExtractionTrackerǁvalidate_member_size__mutmut_11, 
        'xǁExtractionTrackerǁvalidate_member_size__mutmut_12': xǁExtractionTrackerǁvalidate_member_size__mutmut_12, 
        'xǁExtractionTrackerǁvalidate_member_size__mutmut_13': xǁExtractionTrackerǁvalidate_member_size__mutmut_13, 
        'xǁExtractionTrackerǁvalidate_member_size__mutmut_14': xǁExtractionTrackerǁvalidate_member_size__mutmut_14, 
        'xǁExtractionTrackerǁvalidate_member_size__mutmut_15': xǁExtractionTrackerǁvalidate_member_size__mutmut_15, 
        'xǁExtractionTrackerǁvalidate_member_size__mutmut_16': xǁExtractionTrackerǁvalidate_member_size__mutmut_16, 
        'xǁExtractionTrackerǁvalidate_member_size__mutmut_17': xǁExtractionTrackerǁvalidate_member_size__mutmut_17, 
        'xǁExtractionTrackerǁvalidate_member_size__mutmut_18': xǁExtractionTrackerǁvalidate_member_size__mutmut_18, 
        'xǁExtractionTrackerǁvalidate_member_size__mutmut_19': xǁExtractionTrackerǁvalidate_member_size__mutmut_19, 
        'xǁExtractionTrackerǁvalidate_member_size__mutmut_20': xǁExtractionTrackerǁvalidate_member_size__mutmut_20, 
        'xǁExtractionTrackerǁvalidate_member_size__mutmut_21': xǁExtractionTrackerǁvalidate_member_size__mutmut_21, 
        'xǁExtractionTrackerǁvalidate_member_size__mutmut_22': xǁExtractionTrackerǁvalidate_member_size__mutmut_22, 
        'xǁExtractionTrackerǁvalidate_member_size__mutmut_23': xǁExtractionTrackerǁvalidate_member_size__mutmut_23, 
        'xǁExtractionTrackerǁvalidate_member_size__mutmut_24': xǁExtractionTrackerǁvalidate_member_size__mutmut_24
    }
    
    def validate_member_size(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁExtractionTrackerǁvalidate_member_size__mutmut_orig"), object.__getattribute__(self, "xǁExtractionTrackerǁvalidate_member_size__mutmut_mutants"), args, kwargs, self)
        return result 
    
    validate_member_size.__signature__ = _mutmut_signature(xǁExtractionTrackerǁvalidate_member_size__mutmut_orig)
    xǁExtractionTrackerǁvalidate_member_size__mutmut_orig.__name__ = 'xǁExtractionTrackerǁvalidate_member_size'


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


# <3 🧱🤝📦🪄
