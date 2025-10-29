# provide/foundation/archive/defaults.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import zipfile

"""Archive defaults for Foundation configuration."""

# =================================
# Archive Defaults
# =================================
DEFAULT_ARCHIVE_DETERMINISTIC = True
DEFAULT_ARCHIVE_PRESERVE_METADATA = True
DEFAULT_ARCHIVE_PRESERVE_PERMISSIONS = True

# =================================
# Compression Level Defaults
# =================================
DEFAULT_BZIP2_COMPRESSION_LEVEL = 9
DEFAULT_GZIP_COMPRESSION_LEVEL = 6
DEFAULT_XZ_COMPRESSION_LEVEL = 6  # XZ preset range: 0-9
DEFAULT_ZSTD_COMPRESSION_LEVEL = 3  # ZSTD level range: 1-22 (3 is balanced)
DEFAULT_ZIP_COMPRESSION_LEVEL = 6
DEFAULT_ZIP_COMPRESSION_TYPE = zipfile.ZIP_DEFLATED
DEFAULT_ZIP_PASSWORD = None

# =================================
# Archive Extraction Limits (Decompression Bomb Protection)
# =================================
DEFAULT_ARCHIVE_MAX_TOTAL_SIZE = 1_000_000_000  # 1GB
DEFAULT_ARCHIVE_MAX_FILE_COUNT = 10_000
DEFAULT_ARCHIVE_MAX_COMPRESSION_RATIO = 100.0
DEFAULT_ARCHIVE_MAX_SINGLE_FILE_SIZE = 100_000_000  # 100MB
DEFAULT_ARCHIVE_LIMITS_ENABLED = True

__all__ = [
    "DEFAULT_ARCHIVE_DETERMINISTIC",
    "DEFAULT_ARCHIVE_LIMITS_ENABLED",
    "DEFAULT_ARCHIVE_MAX_COMPRESSION_RATIO",
    "DEFAULT_ARCHIVE_MAX_FILE_COUNT",
    "DEFAULT_ARCHIVE_MAX_SINGLE_FILE_SIZE",
    "DEFAULT_ARCHIVE_MAX_TOTAL_SIZE",
    "DEFAULT_ARCHIVE_PRESERVE_METADATA",
    "DEFAULT_ARCHIVE_PRESERVE_PERMISSIONS",
    "DEFAULT_BZIP2_COMPRESSION_LEVEL",
    "DEFAULT_GZIP_COMPRESSION_LEVEL",
    "DEFAULT_XZ_COMPRESSION_LEVEL",
    "DEFAULT_ZIP_COMPRESSION_LEVEL",
    "DEFAULT_ZIP_COMPRESSION_TYPE",
    "DEFAULT_ZIP_PASSWORD",
    "DEFAULT_ZSTD_COMPRESSION_LEVEL",
]
from inspect import signature as _mutmut_signature
from typing import Annotated
from typing import Callable
from typing import ClassVar


MutantDict = Annotated[dict[str, Callable], "Mutant"]


def _mutmut_trampoline(orig, mutants, call_args, call_kwargs, self_arg=None):
    """Forward call to original or mutated function, depending on the environment"""
    import os

    mutant_under_test = os.environ["MUTANT_UNDER_TEST"]
    if mutant_under_test == "fail":
        from mutmut.__main__ import MutmutProgrammaticFailException

        raise MutmutProgrammaticFailException("Failed programmatically")
    elif mutant_under_test == "stats":
        from mutmut.__main__ import record_trampoline_hit

        record_trampoline_hit(orig.__module__ + "." + orig.__name__)
        result = orig(*call_args, **call_kwargs)
        return result
    prefix = orig.__module__ + "." + orig.__name__ + "__mutmut_"
    if not mutant_under_test.startswith(prefix):
        result = orig(*call_args, **call_kwargs)
        return result
    mutant_name = mutant_under_test.rpartition(".")[-1]
    if self_arg:
        # call to a class method where self is not bound
        result = mutants[mutant_name](self_arg, *call_args, **call_kwargs)
    else:
        result = mutants[mutant_name](*call_args, **call_kwargs)
    return result


# <3 🧱🤝📦🪄
