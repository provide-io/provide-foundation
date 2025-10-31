#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from __future__ import annotations

import gzip
import shutil
from typing import BinaryIO

from attrs import define, validators

from provide.foundation.archive.base import BaseCompressor, _validate_compression_level
from provide.foundation.archive.defaults import DEFAULT_GZIP_COMPRESSION_LEVEL
from provide.foundation.config.base import field

"""GZIP compression implementation."""


@define(slots=True)
class GzipCompressor(BaseCompressor):
    """GZIP compression implementation.

    Provides GZIP compression and decompression for single files.
    Does not handle bundling - use with TarArchive for .tar.gz files.
    """

    level: int = field(
        default=DEFAULT_GZIP_COMPRESSION_LEVEL,
        validator=validators.and_(validators.instance_of(int), _validate_compression_level),
    )

    @property
    def format_name(self) -> str:
        """Return the name of the compression format."""
        return "GZIP"

    def _compress_stream(self, input_stream: BinaryIO, output_stream: BinaryIO) -> None:
        """Library-specific stream compression implementation."""
        with gzip.GzipFile(fileobj=output_stream, mode="wb", compresslevel=self.level) as gz:
            shutil.copyfileobj(input_stream, gz)

    def _decompress_stream(self, input_stream: BinaryIO, output_stream: BinaryIO) -> None:
        """Library-specific stream decompression implementation."""
        with gzip.GzipFile(fileobj=input_stream, mode="rb") as gz:
            shutil.copyfileobj(gz, output_stream)

    def _compress_bytes_impl(self, data: bytes) -> bytes:
        """Library-specific bytes compression implementation."""
        return gzip.compress(data, compresslevel=self.level)

    def _decompress_bytes_impl(self, data: bytes) -> bytes:
        """Library-specific bytes decompression implementation."""
        return gzip.decompress(data)


# 🧱🏗️🔚
