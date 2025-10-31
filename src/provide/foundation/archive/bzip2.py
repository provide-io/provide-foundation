#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from __future__ import annotations

import bz2
import shutil
from typing import BinaryIO

from attrs import define, validators

from provide.foundation.archive.base import BaseCompressor, _validate_compression_level
from provide.foundation.archive.defaults import DEFAULT_BZIP2_COMPRESSION_LEVEL
from provide.foundation.config.base import field

"""BZIP2 compression implementation."""


@define(slots=True)
class Bzip2Compressor(BaseCompressor):
    """BZIP2 compression implementation.

    Provides BZIP2 compression and decompression for single files.
    Does not handle bundling - use with TarArchive for .tar.bz2 files.
    """

    level: int = field(
        default=DEFAULT_BZIP2_COMPRESSION_LEVEL,
        validator=validators.and_(validators.instance_of(int), _validate_compression_level),
    )

    @property
    def format_name(self) -> str:
        """Return the name of the compression format."""
        return "BZIP2"

    def _compress_stream(self, input_stream: BinaryIO, output_stream: BinaryIO) -> None:
        """Library-specific stream compression implementation."""
        with bz2.BZ2File(output_stream, "wb", compresslevel=self.level) as bz:
            shutil.copyfileobj(input_stream, bz)

    def _decompress_stream(self, input_stream: BinaryIO, output_stream: BinaryIO) -> None:
        """Library-specific stream decompression implementation."""
        with bz2.BZ2File(input_stream, "rb") as bz:
            shutil.copyfileobj(bz, output_stream)

    def _compress_bytes_impl(self, data: bytes) -> bytes:
        """Library-specific bytes compression implementation."""
        return bz2.compress(data, compresslevel=self.level)

    def _decompress_bytes_impl(self, data: bytes) -> bytes:
        """Library-specific bytes decompression implementation."""
        return bz2.decompress(data)


# 🧱🏗️🔚
