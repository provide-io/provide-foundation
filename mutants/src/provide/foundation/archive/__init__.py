# provide/foundation/archive/__init__.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

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


# <3 🧱🤝📦🪄
