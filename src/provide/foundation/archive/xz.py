#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from __future__ import annotations

import lzma
import shutil
from typing import BinaryIO

from attrs import define, validators

from provide.foundation.archive.base import BaseCompressor, _validate_compression_level
from provide.foundation.archive.defaults import DEFAULT_XZ_COMPRESSION_LEVEL
from provide.foundation.config.base import field

"""XZ/LZMA2 compression implementation using Python stdlib."""


@define(slots=True)
class XzCompressor(BaseCompressor):
    """XZ/LZMA2 compression implementation.

    Provides XZ compression and decompression using Python's stdlib lzma module.
    Does not handle bundling - use with TarArchive for .tar.xz files.

    XZ preset range: 0-9
    - 0: Fastest compression, lower ratio
    - 6: Default balanced setting
    - 9: Best compression, slower
    """

    level: int = field(
        default=DEFAULT_XZ_COMPRESSION_LEVEL,
        validator=validators.and_(validators.instance_of(int), _validate_compression_level),
    )

    @property
    def format_name(self) -> str:
        """Return the name of the compression format."""
        return "XZ"

    def _compress_stream(self, input_stream: BinaryIO, output_stream: BinaryIO) -> None:
        """Library-specific stream compression implementation."""
        with lzma.LZMAFile(output_stream, "wb", preset=self.level) as xz:
            shutil.copyfileobj(input_stream, xz)

    def _decompress_stream(self, input_stream: BinaryIO, output_stream: BinaryIO) -> None:
        """Library-specific stream decompression implementation."""
        with lzma.LZMAFile(input_stream, "rb") as xz:
            shutil.copyfileobj(xz, output_stream)

    def _compress_bytes_impl(self, data: bytes) -> bytes:
        """Library-specific bytes compression implementation."""
        return lzma.compress(data, preset=self.level)

    def _decompress_bytes_impl(self, data: bytes) -> bytes:
        """Library-specific bytes decompression implementation."""
        return lzma.decompress(data)


# 🧱🏗️🔚
