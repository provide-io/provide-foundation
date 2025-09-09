"""Archive operations for provide-foundation.

This module provides clean, composable archive operations without complex abstractions.
Tools for creating, extracting, and manipulating archives in various formats.
"""

from provide.foundation.archive.base import ArchiveError, BaseArchive
from provide.foundation.archive.bzip2 import Bzip2Compressor
from provide.foundation.archive.gzip import GzipCompressor
from provide.foundation.archive.operations import ArchiveOperations, OperationChain
from provide.foundation.archive.tar import TarArchive
from provide.foundation.archive.zip import ZipArchive

__all__ = [
    "ArchiveError",
    "ArchiveOperations",
    "BaseArchive",
    "Bzip2Compressor",
    "GzipCompressor",
    "OperationChain",
    "TarArchive",
    "ZipArchive",
]