from __future__ import annotations

from provide.foundation.archive.base import ArchiveError, BaseArchive
from provide.foundation.archive.bzip2 import Bzip2Compressor
from provide.foundation.archive.gzip import GzipCompressor
from provide.foundation.archive.limits import (
    ArchiveLimits,
    DEFAULT_LIMITS,
    ExtractionTracker,
    get_archive_size,
)
from provide.foundation.archive.operations import ArchiveOperations, OperationChain
from provide.foundation.archive.tar import TarArchive
from provide.foundation.archive.zip import ZipArchive

"""Archive operations for provide-foundation.

This module provides clean, composable archive operations without complex abstractions.
Tools for creating, extracting, and manipulating archives in various formats.
"""

__all__ = [
    "ArchiveError",
    "ArchiveLimits",
    "ArchiveOperations",
    "BaseArchive",
    "Bzip2Compressor",
    "DEFAULT_LIMITS",
    "ExtractionTracker",
    "GzipCompressor",
    "OperationChain",
    "TarArchive",
    "ZipArchive",
    "get_archive_size",
]
