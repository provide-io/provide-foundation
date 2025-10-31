#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

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

# 🧱🏗️🔚
