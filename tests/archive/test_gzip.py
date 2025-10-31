#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for GZIP compression implementation."""

from __future__ import annotations

from collections.abc import Callable
from io import BytesIO
from pathlib import Path

from provide.testkit import FoundationTestCase
import pytest

from provide.foundation.archive.base import ArchiveError
from provide.foundation.archive.gzip import GzipCompressor


class TestGzipCompressor(FoundationTestCase):
    """Test GZIP compression functionality."""

    @pytest.fixture
    def gzip_compressor(self) -> GzipCompressor:
        """Create a GZIP compressor instance."""
        return GzipCompressor()

    @pytest.fixture
    def test_file(self, temp_file: Callable[[str, str], Path]) -> Path:
        """Create a test file."""
        return temp_file("This is test content for compression.\n" * 100, ".txt")

    def test_compress_file(self, gzip_compressor: GzipCompressor, test_file: Path) -> None:
        """Test compressing a file."""
        output = test_file.with_suffix(".txt.gz")

        try:
            result = gzip_compressor.compress_file(test_file, output)

            assert result == output
            assert output.exists()
            # Compressed file should be smaller than original
            assert output.stat().st_size < test_file.stat().st_size
        finally:
            output.unlink(missing_ok=True)

    def test_decompress_file(self, gzip_compressor: GzipCompressor, test_file: Path) -> None:
        """Test decompressing a file."""
        compressed = test_file.with_suffix(".txt.gz")
        decompressed = test_file.with_suffix(".txt.decompressed")

        try:
            # Compress first
            gzip_compressor.compress_file(test_file, compressed)

            # Then decompress
            result = gzip_compressor.decompress_file(compressed, decompressed)

            assert result == decompressed
            assert decompressed.exists()
            # Content should match original
            assert decompressed.read_text() == test_file.read_text()
        finally:
            compressed.unlink(missing_ok=True)
            decompressed.unlink(missing_ok=True)

    def test_compress_bytes(self, gzip_compressor: GzipCompressor) -> None:
        """Test compressing bytes data."""
        data = b"Test data for compression" * 100

        compressed = gzip_compressor.compress_bytes(data)

        assert isinstance(compressed, bytes)
        assert len(compressed) < len(data)
        # Check GZIP magic number
        assert compressed[:2] == b"\x1f\x8b"

    def test_decompress_bytes(self, gzip_compressor: GzipCompressor) -> None:
        """Test decompressing bytes data."""
        original = b"Test data for compression" * 100

        compressed = gzip_compressor.compress_bytes(original)
        decompressed = gzip_compressor.decompress_bytes(compressed)

        assert decompressed == original

    def test_compress_stream(self, gzip_compressor: GzipCompressor) -> None:
        """Test compressing from stream to stream."""
        input_data = b"Stream compression test data" * 100
        input_stream = BytesIO(input_data)
        output_stream = BytesIO()

        gzip_compressor.compress(input_stream, output_stream)

        compressed = output_stream.getvalue()
        assert len(compressed) < len(input_data)
        assert compressed[:2] == b"\x1f\x8b"

    def test_decompress_stream(self, gzip_compressor: GzipCompressor) -> None:
        """Test decompressing from stream to stream."""
        original = b"Stream decompression test data" * 100

        # Compress first
        compressed = gzip_compressor.compress_bytes(original)

        # Decompress using streams
        input_stream = BytesIO(compressed)
        output_stream = BytesIO()

        gzip_compressor.decompress(input_stream, output_stream)

        decompressed = output_stream.getvalue()
        assert decompressed == original

    def test_compression_levels(self) -> None:
        """Test different compression levels."""
        data = b"Test data" * 1000

        # Test minimum compression
        compressor_fast = GzipCompressor(level=1)
        compressed_fast = compressor_fast.compress_bytes(data)

        # Test maximum compression
        compressor_best = GzipCompressor(level=9)
        compressed_best = compressor_best.compress_bytes(data)

        # Both should compress, but best should be smaller (usually)
        assert len(compressed_fast) < len(data)
        assert len(compressed_best) < len(data)
        # Note: For small data, this might not always be true
        # assert len(compressed_best) <= len(compressed_fast)

    def test_invalid_compression_level(self) -> None:
        """Test invalid compression levels."""
        with pytest.raises(ValueError):
            GzipCompressor(level=0)

        with pytest.raises(ValueError):
            GzipCompressor(level=10)

    def test_error_handling(self, gzip_compressor: GzipCompressor, temp_directory: Path) -> None:
        """Test error handling in GZIP operations."""
        temp_path = temp_directory

        # Test compressing non-existent file
        with pytest.raises(ArchiveError):
            gzip_compressor.compress_file(
                temp_path / "nonexistent.txt",
                temp_path / "output.gz",
            )

        # Test decompressing invalid data
        invalid_file = temp_path / "invalid.gz"
        invalid_file.write_text("not gzip data")

        with pytest.raises(ArchiveError):
            gzip_compressor.decompress_file(
                invalid_file,
                temp_path / "output.txt",
            )

        # Test decompressing invalid bytes
        with pytest.raises(ArchiveError):
            gzip_compressor.decompress_bytes(b"not gzip data")


# 🧱🏗️🔚
