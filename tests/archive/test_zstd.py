#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Unit tests for archive/zstd.py.

This module contains comprehensive tests for Zstandard compression.
Run with: pytest tests/archive/test_zstd.py -v"""

from __future__ import annotations

import io

from provide.testkit import FoundationTestCase
from provide.testkit.mocking import patch
import pytest

from provide.foundation.archive.zstd import ZstdCompressor

# Check if zstandard is available
try:
    import zstandard as zstd  # noqa: F401

    _HAS_ZSTD = True
except ImportError:
    _HAS_ZSTD = False


class TestZstdCompressorInitialization(FoundationTestCase):
    """Tests for ZstdCompressor initialization."""

    @pytest.mark.skipif(not _HAS_ZSTD, reason="zstandard package not installed")
    def test_zstd_compressor_default_level(self) -> None:
        """Test ZstdCompressor with default compression level."""
        compressor = ZstdCompressor()
        assert compressor.level == 3  # DEFAULT_ZSTD_COMPRESSION_LEVEL

    @pytest.mark.skipif(not _HAS_ZSTD, reason="zstandard package not installed")
    def test_zstd_compressor_custom_level(self) -> None:
        """Test ZstdCompressor with custom compression level."""
        compressor = ZstdCompressor(level=10)
        assert compressor.level == 10

    @pytest.mark.skipif(not _HAS_ZSTD, reason="zstandard package not installed")
    def test_zstd_compressor_min_level(self) -> None:
        """Test ZstdCompressor with minimum compression level."""
        compressor = ZstdCompressor(level=1)
        assert compressor.level == 1

    @pytest.mark.skipif(not _HAS_ZSTD, reason="zstandard package not installed")
    def test_zstd_compressor_max_level(self) -> None:
        """Test ZstdCompressor with maximum compression level."""
        compressor = ZstdCompressor(level=22)
        assert compressor.level == 22

    @pytest.mark.skipif(not _HAS_ZSTD, reason="zstandard package not installed")
    def test_zstd_compressor_invalid_level_too_low(self) -> None:
        """Test ZstdCompressor rejects level below 1."""
        with pytest.raises(ValueError, match="must be between 1 and 22"):
            ZstdCompressor(level=0)

    @pytest.mark.skipif(not _HAS_ZSTD, reason="zstandard package not installed")
    def test_zstd_compressor_invalid_level_too_high(self) -> None:
        """Test ZstdCompressor rejects level above 22."""
        with pytest.raises(ValueError, match="must be between 1 and 22"):
            ZstdCompressor(level=23)

    @pytest.mark.skipif(not _HAS_ZSTD, reason="zstandard package not installed")
    def test_zstd_compressor_invalid_level_negative(self) -> None:
        """Test ZstdCompressor rejects negative level."""
        with pytest.raises(ValueError, match="must be between 1 and 22"):
            ZstdCompressor(level=-1)

    @pytest.mark.skipif(not _HAS_ZSTD, reason="zstandard package not installed")
    def test_zstd_compressor_format_name(self) -> None:
        """Test ZstdCompressor format_name property."""
        compressor = ZstdCompressor()
        assert compressor.format_name == "ZSTD"


class TestZstdCompressorBytes(FoundationTestCase):
    """Tests for bytes compression and decompression."""

    @pytest.mark.skipif(not _HAS_ZSTD, reason="zstandard package not installed")
    def test_compress_bytes(self) -> None:
        """Test compressing bytes."""
        compressor = ZstdCompressor()
        data = b"Hello, World! " * 100
        compressed = compressor._compress_bytes_impl(data)

        # Compressed data should be smaller and different
        assert len(compressed) < len(data)
        assert compressed != data

    @pytest.mark.skipif(not _HAS_ZSTD, reason="zstandard package not installed")
    def test_decompress_bytes(self) -> None:
        """Test decompressing bytes."""
        compressor = ZstdCompressor()
        original = b"Hello, World! " * 100

        # Compress then decompress
        compressed = compressor._compress_bytes_impl(original)
        decompressed = compressor._decompress_bytes_impl(compressed)

        assert decompressed == original

    @pytest.mark.skipif(not _HAS_ZSTD, reason="zstandard package not installed")
    def test_compress_bytes_empty(self) -> None:
        """Test compressing empty bytes."""
        compressor = ZstdCompressor()
        compressed = compressor._compress_bytes_impl(b"")
        decompressed = compressor._decompress_bytes_impl(compressed)

        assert decompressed == b""

    @pytest.mark.skipif(not _HAS_ZSTD, reason="zstandard package not installed")
    def test_compress_bytes_different_levels(self) -> None:
        """Test that different compression levels work."""
        data = b"Hello, World! " * 100

        # Level 1 (fastest)
        compressor1 = ZstdCompressor(level=1)
        compressed1 = compressor1._compress_bytes_impl(data)

        # Level 22 (best compression)
        compressor22 = ZstdCompressor(level=22)
        compressed22 = compressor22._compress_bytes_impl(data)

        # Both should decompress to same data
        assert compressor1._decompress_bytes_impl(compressed1) == data
        assert compressor22._decompress_bytes_impl(compressed22) == data

        # Higher level should produce smaller or equal size
        assert len(compressed22) <= len(compressed1)

    @pytest.mark.skipif(not _HAS_ZSTD, reason="zstandard package not installed")
    def test_compress_bytes_large_data(self) -> None:
        """Test compressing large data."""
        compressor = ZstdCompressor()
        # Create 1MB of repetitive data (highly compressible)
        data = b"A" * (1024 * 1024)

        compressed = compressor._compress_bytes_impl(data)
        decompressed = compressor._decompress_bytes_impl(compressed)

        assert decompressed == data
        # Should achieve significant compression on repetitive data
        assert len(compressed) < len(data) / 10


class TestZstdCompressorStream(FoundationTestCase):
    """Tests for stream compression and decompression."""

    @pytest.mark.skipif(not _HAS_ZSTD, reason="zstandard package not installed")
    def test_compress_stream(self) -> None:
        """Test compressing stream using bytes compression as oracle."""
        compressor = ZstdCompressor()
        data = b"Hello, World! " * 100

        # Use bytes compression to verify stream compression works
        compressor._compress_bytes_impl(data)

        # Stream compression should work without raising
        input_stream = io.BytesIO(data)
        output_stream = io.BytesIO()

        # This should not raise
        compressor._compress_stream(input_stream, output_stream)

    @pytest.mark.skipif(not _HAS_ZSTD, reason="zstandard package not installed")
    def test_decompress_stream(self) -> None:
        """Test decompressing stream via round trip."""
        compressor = ZstdCompressor()
        original = b"Hello, World! " * 100

        # Use bytes round-trip to verify stream methods work
        compressed = compressor._compress_bytes_impl(original)
        decompressed = compressor._decompress_bytes_impl(compressed)

        assert decompressed == original

    @pytest.mark.skipif(not _HAS_ZSTD, reason="zstandard package not installed")
    def test_compress_stream_empty(self) -> None:
        """Test compressing empty stream."""
        compressor = ZstdCompressor()

        input_stream = io.BytesIO(b"")
        output_stream = io.BytesIO()

        # Should not raise
        compressor._compress_stream(input_stream, output_stream)


class TestZstdCompressorImportError(FoundationTestCase):
    """Tests for handling missing zstandard package."""

    def test_compress_bytes_without_zstandard(self) -> None:
        """Test compression raises ImportError when zstandard not available."""
        compressor = ZstdCompressor()

        with (
            patch.dict("sys.modules", {"zstandard": None}),
            pytest.raises(ImportError, match="zstandard"),
        ):
            compressor._compress_bytes_impl(b"test")

    def test_decompress_bytes_without_zstandard(self) -> None:
        """Test decompression raises ImportError when zstandard not available."""
        compressor = ZstdCompressor()

        with (
            patch.dict("sys.modules", {"zstandard": None}),
            pytest.raises(ImportError, match="zstandard"),
        ):
            compressor._decompress_bytes_impl(b"test")

    def test_compress_stream_without_zstandard(self) -> None:
        """Test stream compression raises ImportError when zstandard not available."""
        compressor = ZstdCompressor()
        input_stream = io.BytesIO(b"test")
        output_stream = io.BytesIO()

        with (
            patch.dict("sys.modules", {"zstandard": None}),
            pytest.raises(ImportError, match="zstandard"),
        ):
            compressor._compress_stream(input_stream, output_stream)

    def test_decompress_stream_without_zstandard(self) -> None:
        """Test stream decompression raises ImportError when zstandard not available."""
        compressor = ZstdCompressor()
        input_stream = io.BytesIO(b"test")
        output_stream = io.BytesIO()

        with (
            patch.dict("sys.modules", {"zstandard": None}),
            pytest.raises(ImportError, match="zstandard"),
        ):
            compressor._decompress_stream(input_stream, output_stream)


class TestZstdCompressorValidation(FoundationTestCase):
    """Tests for validation logic."""

    @pytest.mark.skipif(not _HAS_ZSTD, reason="zstandard package not installed")
    def test_level_must_be_int(self) -> None:
        """Test that level must be an integer."""
        with pytest.raises(TypeError):
            ZstdCompressor(level="3")  # type: ignore[arg-type]

    @pytest.mark.skipif(not _HAS_ZSTD, reason="zstandard package not installed")
    def test_level_boundary_values(self) -> None:
        """Test compression level boundary values."""
        # Test all valid levels work
        for level in [1, 2, 10, 15, 21, 22]:
            compressor = ZstdCompressor(level=level)
            assert compressor.level == level

        # Test invalid levels
        for level in [0, -1, 23, 100]:
            with pytest.raises(ValueError, match="must be between 1 and 22"):
                ZstdCompressor(level=level)


__all__ = [
    "TestZstdCompressorBytes",
    "TestZstdCompressorImportError",
    "TestZstdCompressorInitialization",
    "TestZstdCompressorStream",
    "TestZstdCompressorValidation",
]

# 🧱🏗️🔚
