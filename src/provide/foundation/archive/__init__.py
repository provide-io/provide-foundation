#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from __future__ import annotations

from provide.foundation.archive.base import (
    ArchiveError,
    ArchiveFormatError,
    ArchiveIOError,
    ArchiveValidationError,
    BaseArchive,
)
from provide.foundation.archive.bzip2 import Bzip2Compressor
from provide.foundation.archive.gzip import GzipCompressor
from provide.foundation.archive.limits import (
    DEFAULT_LIMITS,
    ArchiveLimits,
    ExtractionTracker,
    get_archive_size,
)
from provide.foundation.archive.operations import ArchiveOperations, OperationChain
from provide.foundation.archive.tar import TarArchive, deterministic_filter
from provide.foundation.archive.types import (
    INVERSE_OPERATIONS,
    OPERATION_NAMES,
    ArchiveOperation,
    get_operation_from_string,
)
from provide.foundation.archive.xz import XzCompressor
from provide.foundation.archive.zip import ZipArchive
from provide.foundation.archive.zstd import ZstdCompressor

"""Archive operations for provide-foundation.

This module provides clean, composable archive operations without complex abstractions.
Tools for creating, extracting, and manipulating archives in various formats.
"""

__all__ = [
    "DEFAULT_LIMITS",
    "INVERSE_OPERATIONS",
    "OPERATION_NAMES",
    "ArchiveError",
    "ArchiveFormatError",
    "ArchiveIOError",
    "ArchiveLimits",
    "ArchiveOperation",
    "ArchiveOperations",
    "ArchiveValidationError",
    "BaseArchive",
    "Bzip2Compressor",
    "ExtractionTracker",
    "GzipCompressor",
    "OperationChain",
    "TarArchive",
    "XzCompressor",
    "ZipArchive",
    "ZstdCompressor",
    "deterministic_filter",
    "get_archive_size",
    "get_operation_from_string",
]

# 🧱🏗️🔚
