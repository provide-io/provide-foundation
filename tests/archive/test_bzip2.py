#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for BZIP2 compression implementation."""

from __future__ import annotations

from collections.abc import Callable
from io import BytesIO
from pathlib import Path

from provide.testkit import FoundationTestCase
import pytest

from provide.foundation.archive.base import ArchiveError
from provide.foundation.archive.bzip2 import Bzip2Compressor


class TestBzip2Compressor(FoundationTestCase):
    """Test BZIP2 compression functionality."""

    @pytest.fixture
    def bzip2_compressor(self) -> Bzip2Compressor:
        """Create a BZIP2 compressor instance."""
        return Bzip2Compressor()

    @pytest.fixture
    def test_file(self, temp_file: Callable[[str, str], Path]) -> Path:
        """Create a test file."""
        return temp_file("This is test content for BZIP2 compression.\n" * 100, ".txt")

    def test_compress_file(self, bzip2_compressor: Bzip2Compressor, test_file: Path) -> None:
        """Test compressing a file."""
        output = test_file.with_suffix(".txt.bz2")

        try:
            result = bzip2_compressor.compress_file(test_file, output)

            assert result == output
            assert output.exists()
            # Compressed file should be smaller than original
            assert output.stat().st_size < test_file.stat().st_size
        finally:
            output.unlink(missing_ok=True)

    def test_decompress_file(self, bzip2_compressor: Bzip2Compressor, test_file: Path) -> None:
        """Test decompressing a file."""
        compressed = test_file.with_suffix(".txt.bz2")
        decompressed = test_file.with_suffix(".txt.decompressed")

        try:
            # Compress first
            bzip2_compressor.compress_file(test_file, compressed)

            # Then decompress
            result = bzip2_compressor.decompress_file(compressed, decompressed)

            assert result == decompressed
            assert decompressed.exists()
            # Content should match original
            assert decompressed.read_text() == test_file.read_text()
        finally:
            compressed.unlink(missing_ok=True)
            decompressed.unlink(missing_ok=True)

    def test_compress_bytes(self, bzip2_compressor: Bzip2Compressor) -> None:
        """Test compressing bytes data."""
        data = b"Test data for BZIP2 compression" * 100

        compressed = bzip2_compressor.compress_bytes(data)

        assert isinstance(compressed, bytes)
        assert len(compressed) < len(data)
        # Check BZIP2 magic number
        assert compressed[:3] == b"BZh"

    def test_decompress_bytes(self, bzip2_compressor: Bzip2Compressor) -> None:
        """Test decompressing bytes data."""
        original = b"Test data for BZIP2 compression" * 100

        compressed = bzip2_compressor.compress_bytes(original)
        decompressed = bzip2_compressor.decompress_bytes(compressed)

        assert decompressed == original

    def test_compress_stream(self, bzip2_compressor: Bzip2Compressor) -> None:
        """Test compressing from stream to stream."""
        input_data = b"Stream BZIP2 compression test data" * 100
        input_stream = BytesIO(input_data)
        output_stream = BytesIO()

        bzip2_compressor.compress(input_stream, output_stream)

        compressed = output_stream.getvalue()
        assert len(compressed) < len(input_data)
        assert compressed[:3] == b"BZh"

    def test_decompress_stream(self, bzip2_compressor: Bzip2Compressor) -> None:
        """Test decompressing from stream to stream."""
        original = b"Stream BZIP2 decompression test data" * 100

        # Compress first
        compressed = bzip2_compressor.compress_bytes(original)

        # Decompress using streams
        input_stream = BytesIO(compressed)
        output_stream = BytesIO()

        bzip2_compressor.decompress(input_stream, output_stream)

        decompressed = output_stream.getvalue()
        assert decompressed == original

    def test_compression_levels(self) -> None:
        """Test different compression levels."""
        data = b"Test data" * 1000

        # Test minimum compression
        compressor_fast = Bzip2Compressor(level=1)
        compressed_fast = compressor_fast.compress_bytes(data)

        # Test maximum compression
        compressor_best = Bzip2Compressor(level=9)
        compressed_best = compressor_best.compress_bytes(data)

        # Both should compress
        assert len(compressed_fast) < len(data)
        assert len(compressed_best) < len(data)
        # Best compression might be smaller (not guaranteed for small data)

    def test_invalid_compression_level(self) -> None:
        """Test invalid compression levels."""
        with pytest.raises(ValueError):
            Bzip2Compressor(level=0)

        with pytest.raises(ValueError):
            Bzip2Compressor(level=10)

    def test_error_handling(self, bzip2_compressor: Bzip2Compressor, temp_directory: Path) -> None:
        """Test error handling in BZIP2 operations."""
        temp_path = temp_directory

        # Test compressing non-existent file
        with pytest.raises(ArchiveError):
            bzip2_compressor.compress_file(
                temp_path / "nonexistent.txt",
                temp_path / "output.bz2",
            )

        # Test decompressing invalid data
        invalid_file = temp_path / "invalid.bz2"
        invalid_file.write_text("not bzip2 data")

        with pytest.raises(ArchiveError):
            bzip2_compressor.decompress_file(
                invalid_file,
                temp_path / "output.txt",
            )

        # Test decompressing invalid bytes
        with pytest.raises(ArchiveError):
            bzip2_compressor.decompress_bytes(b"not bzip2 data")


# 🧱🏗️🔚
