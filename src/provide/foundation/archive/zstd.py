#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from __future__ import annotations

import shutil
from typing import Any, BinaryIO

from attrs import Attribute, define, validators

from provide.foundation.archive.base import BaseCompressor
from provide.foundation.archive.defaults import DEFAULT_ZSTD_COMPRESSION_LEVEL
from provide.foundation.config.base import field

"""Zstandard compression implementation (requires zstandard package)."""


def _validate_zstd_level(instance: Any, attribute: Attribute[int], value: int) -> None:
    """Validate ZSTD compression level (1-22)."""
    if not (1 <= value <= 22):
        raise ValueError(f"ZSTD compression level must be between 1 and 22, got {value}")


@define(slots=True)
class ZstdCompressor(BaseCompressor):
    """Zstandard compression implementation.

    Provides ZSTD compression and decompression using the zstandard package.
    Does not handle bundling - use with TarArchive for .tar.zst files.

    ZSTD level range: 1-22
    - 1: Fastest compression, lower ratio
    - 3: Default balanced setting
    - 22: Best compression, much slower

    Note: Requires the 'zstandard' package to be installed.
          Install with: pip install provide-foundation[compression]
    """

    level: int = field(
        default=DEFAULT_ZSTD_COMPRESSION_LEVEL,
        validator=validators.and_(validators.instance_of(int), _validate_zstd_level),
    )

    @property
    def format_name(self) -> str:
        """Return the name of the compression format."""
        return "ZSTD"

    def _compress_stream(self, input_stream: BinaryIO, output_stream: BinaryIO) -> None:
        """Library-specific stream compression implementation."""
        try:
            import zstandard as zstd
        except ImportError as e:
            raise ImportError(
                "ZSTD compression requires 'zstandard' package. "
                "Install with: pip install provide-foundation[compression]"
            ) from e

        cctx = zstd.ZstdCompressor(level=self.level)
        with cctx.stream_writer(output_stream) as compressor:
            shutil.copyfileobj(input_stream, compressor)

    def _decompress_stream(self, input_stream: BinaryIO, output_stream: BinaryIO) -> None:
        """Library-specific stream decompression implementation."""
        try:
            import zstandard as zstd
        except ImportError as e:
            raise ImportError(
                "ZSTD decompression requires 'zstandard' package. "
                "Install with: pip install provide-foundation[compression]"
            ) from e

        dctx = zstd.ZstdDecompressor()
        with dctx.stream_reader(input_stream) as decompressor:
            shutil.copyfileobj(decompressor, output_stream)

    def _compress_bytes_impl(self, data: bytes) -> bytes:
        """Library-specific bytes compression implementation."""
        try:
            import zstandard as zstd
        except ImportError as e:
            raise ImportError(
                "ZSTD compression requires 'zstandard' package. "
                "Install with: pip install provide-foundation[compression]"
            ) from e

        cctx = zstd.ZstdCompressor(level=self.level)
        return cctx.compress(data)

    def _decompress_bytes_impl(self, data: bytes) -> bytes:
        """Library-specific bytes decompression implementation."""
        try:
            import zstandard as zstd
        except ImportError as e:
            raise ImportError(
                "ZSTD decompression requires 'zstandard' package. "
                "Install with: pip install provide-foundation[compression]"
            ) from e

        dctx = zstd.ZstdDecompressor()
        return dctx.decompress(data)


# 🧱🏗️🔚
