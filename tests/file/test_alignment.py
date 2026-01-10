#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for memory/file alignment utilities."""

from __future__ import annotations

import pytest

from provide.foundation.file.alignment import (
    CACHE_LINE_SIZE,
    DEFAULT_ALIGNMENT,
    PAGE_SIZE_4K,
    PAGE_SIZE_16K,
    align_offset,
    align_to_page,
    calculate_padding,
    get_system_page_size,
    is_aligned,
    is_power_of_two,
)


class TestAlignOffset:
    """Tests for align_offset function."""

    def test_align_already_aligned(self) -> None:
        """Should return same value if already aligned."""
        assert align_offset(16, 16) == 16
        assert align_offset(32, 16) == 32
        assert align_offset(0, 16) == 0

    def test_align_offset_up(self) -> None:
        """Should align offset up to next boundary."""
        assert align_offset(10, 16) == 16
        assert align_offset(17, 16) == 32
        assert align_offset(1, 16) == 16

    def test_align_different_boundaries(self) -> None:
        """Should work with different alignment boundaries."""
        assert align_offset(100, 64) == 128
        assert align_offset(100, 32) == 128
        assert align_offset(100, 16) == 112

    def test_align_large_values(self) -> None:
        """Should handle large offset values."""
        assert align_offset(1_000_000, 4096) == 1_003_520  # 245 * 4096
        assert align_offset(1_048_576, 4096) == 1_048_576  # Already aligned (256 * 4096)

    def test_align_zero_offset(self) -> None:
        """Should handle zero offset correctly."""
        assert align_offset(0, 16) == 0
        assert align_offset(0, 4096) == 0

    def test_align_with_default_alignment(self) -> None:
        """Should use DEFAULT_ALIGNMENT when not specified."""
        assert align_offset(10) == align_offset(10, DEFAULT_ALIGNMENT)

    def test_align_invalid_alignment_zero(self) -> None:
        """Should raise ValueError for zero alignment."""
        with pytest.raises(ValueError, match="power of 2"):
            align_offset(100, 0)

    def test_align_invalid_alignment_negative(self) -> None:
        """Should raise ValueError for negative alignment."""
        with pytest.raises(ValueError, match="power of 2"):
            align_offset(100, -16)

    def test_align_invalid_alignment_not_power_of_two(self) -> None:
        """Should raise ValueError for non-power-of-2 alignment."""
        with pytest.raises(ValueError, match="power of 2"):
            align_offset(100, 15)
        with pytest.raises(ValueError, match="power of 2"):
            align_offset(100, 100)


class TestAlignToPage:
    """Tests for align_to_page function."""

    def test_align_to_4k_page(self) -> None:
        """Should align to 4KB page boundary by default."""
        assert align_to_page(100) == 4096
        assert align_to_page(4096) == 4096
        assert align_to_page(4097) == 8192

    def test_align_to_16k_page(self) -> None:
        """Should align to 16KB page when specified."""
        assert align_to_page(100, page_size=PAGE_SIZE_16K) == 16384
        assert align_to_page(16384, page_size=PAGE_SIZE_16K) == 16384
        assert align_to_page(16385, page_size=PAGE_SIZE_16K) == 32768

    def test_align_to_custom_page_size(self) -> None:
        """Should work with custom page sizes."""
        assert align_to_page(100, page_size=8192) == 8192
        assert align_to_page(8192, page_size=8192) == 8192

    def test_align_zero_to_page(self) -> None:
        """Should handle zero offset."""
        assert align_to_page(0) == 0

    def test_align_invalid_page_size(self) -> None:
        """Should raise ValueError for invalid page size."""
        with pytest.raises(ValueError, match="power of 2"):
            align_to_page(100, page_size=4000)


class TestIsAligned:
    """Tests for is_aligned function."""

    def test_is_aligned_true(self) -> None:
        """Should return True for aligned values."""
        assert is_aligned(16, 16) is True
        assert is_aligned(32, 16) is True
        assert is_aligned(0, 16) is True
        assert is_aligned(4096, 4096) is True

    def test_is_aligned_false(self) -> None:
        """Should return False for unaligned values."""
        assert is_aligned(17, 16) is False
        assert is_aligned(10, 16) is False
        assert is_aligned(4097, 4096) is False

    def test_is_aligned_different_boundaries(self) -> None:
        """Should check alignment against different boundaries."""
        value = 128
        assert is_aligned(value, 64) is True
        assert is_aligned(value, 128) is True
        assert is_aligned(value, 256) is False

    def test_is_aligned_with_default(self) -> None:
        """Should use DEFAULT_ALIGNMENT when not specified."""
        assert is_aligned(16) == is_aligned(16, DEFAULT_ALIGNMENT)

    def test_is_aligned_invalid_alignment(self) -> None:
        """Should raise ValueError for invalid alignment."""
        with pytest.raises(ValueError, match="power of 2"):
            is_aligned(100, 15)


class TestCalculatePadding:
    """Tests for calculate_padding function."""

    def test_calculate_padding_needed(self) -> None:
        """Should calculate padding needed to reach alignment."""
        assert calculate_padding(10, 16) == 6
        assert calculate_padding(17, 16) == 15
        assert calculate_padding(100, 64) == 28

    def test_calculate_padding_already_aligned(self) -> None:
        """Should return 0 when already aligned."""
        assert calculate_padding(16, 16) == 0
        assert calculate_padding(32, 16) == 0
        assert calculate_padding(4096, 4096) == 0

    def test_calculate_padding_zero_offset(self) -> None:
        """Should return 0 for zero offset."""
        assert calculate_padding(0, 16) == 0

    def test_calculate_padding_with_default(self) -> None:
        """Should use DEFAULT_ALIGNMENT when not specified."""
        assert calculate_padding(10) == calculate_padding(10, DEFAULT_ALIGNMENT)

    def test_calculate_padding_invalid_alignment(self) -> None:
        """Should raise ValueError for invalid alignment."""
        with pytest.raises(ValueError, match="power of 2"):
            calculate_padding(100, 15)


class TestGetSystemPageSize:
    """Tests for get_system_page_size function."""

    def test_get_system_page_size(self) -> None:
        """Should return a valid page size."""
        page_size = get_system_page_size()
        assert page_size > 0
        assert is_power_of_two(page_size)

    def test_get_system_page_size_common_values(self) -> None:
        """Should return one of the common page sizes."""
        page_size = get_system_page_size()
        common_sizes = [4096, 8192, 16384, 65536]
        assert page_size in common_sizes


class TestIsPowerOfTwo:
    """Tests for is_power_of_two function."""

    def test_is_power_of_two_true(self) -> None:
        """Should return True for powers of 2."""
        assert is_power_of_two(1) is True
        assert is_power_of_two(2) is True
        assert is_power_of_two(4) is True
        assert is_power_of_two(8) is True
        assert is_power_of_two(16) is True
        assert is_power_of_two(1024) is True
        assert is_power_of_two(4096) is True
        assert is_power_of_two(16384) is True

    def test_is_power_of_two_false(self) -> None:
        """Should return False for non-powers of 2."""
        assert is_power_of_two(3) is False
        assert is_power_of_two(5) is False
        assert is_power_of_two(15) is False
        assert is_power_of_two(100) is False
        assert is_power_of_two(4095) is False

    def test_is_power_of_two_edge_cases(self) -> None:
        """Should handle edge cases correctly."""
        assert is_power_of_two(0) is False
        assert is_power_of_two(-1) is False
        assert is_power_of_two(-16) is False


class TestAlignmentConstants:
    """Tests for alignment constants."""

    def test_default_alignment_is_power_of_two(self) -> None:
        """DEFAULT_ALIGNMENT should be a power of 2."""
        assert is_power_of_two(DEFAULT_ALIGNMENT)

    def test_cache_line_size_is_power_of_two(self) -> None:
        """CACHE_LINE_SIZE should be a power of 2."""
        assert is_power_of_two(CACHE_LINE_SIZE)

    def test_page_sizes_are_powers_of_two(self) -> None:
        """Page size constants should be powers of 2."""
        assert is_power_of_two(PAGE_SIZE_4K)
        assert is_power_of_two(PAGE_SIZE_16K)

    def test_page_size_values(self) -> None:
        """Page size constants should have expected values."""
        assert PAGE_SIZE_4K == 4096
        assert PAGE_SIZE_16K == 16384


class TestAlignmentIntegration:
    """Integration tests combining multiple alignment functions."""

    def test_align_then_check(self) -> None:
        """Should be able to align and then verify alignment."""
        offset = 100
        alignment = 64

        aligned = align_offset(offset, alignment)
        assert is_aligned(aligned, alignment)

    def test_padding_produces_alignment(self) -> None:
        """Should be able to add padding and verify alignment."""
        offset = 100
        alignment = 64

        padding = calculate_padding(offset, alignment)
        aligned_offset = offset + padding

        assert is_aligned(aligned_offset, alignment)
        assert aligned_offset == align_offset(offset, alignment)

    def test_page_alignment_workflow(self) -> None:
        """Test complete page alignment workflow."""
        # Get system page size
        page_size = get_system_page_size()

        # Align an offset
        offset = 1234
        aligned = align_to_page(offset, page_size=page_size)

        # Verify alignment
        assert is_aligned(aligned, page_size)

        # Calculate padding
        padding = calculate_padding(offset, page_size)
        assert offset + padding == aligned

    def test_multiple_alignments(self) -> None:
        """Test aligning to multiple boundaries."""
        offset = 100

        # Align to different boundaries
        align_16 = align_offset(offset, 16)
        align_32 = align_offset(offset, 32)
        align_64 = align_offset(offset, 64)

        # Verify all are aligned to their respective boundaries
        assert is_aligned(align_16, 16)
        assert is_aligned(align_32, 32)
        assert is_aligned(align_64, 64)

        # Verify relative ordering
        assert align_16 <= align_32 <= align_64


class TestAlignmentEdgeCases:
    """Tests for edge cases and boundary conditions."""

    def test_very_large_offset(self) -> None:
        """Should handle very large offset values."""
        large_offset = 10**15
        aligned = align_offset(large_offset, 4096)
        assert is_aligned(aligned, 4096)

    def test_alignment_larger_than_offset(self) -> None:
        """Should work when alignment is larger than offset."""
        offset = 100
        alignment = 4096
        aligned = align_offset(offset, alignment)
        assert aligned == 4096

    def test_offset_equal_to_alignment(self) -> None:
        """Should handle case where offset equals alignment."""
        offset = 4096
        aligned = align_offset(offset, 4096)
        assert aligned == 4096

    def test_sequential_alignments(self) -> None:
        """Test aligning sequential offsets."""
        alignment = 64
        offsets = [0, 1, 63, 64, 65, 127, 128]

        for offset in offsets:
            aligned = align_offset(offset, alignment)
            assert is_aligned(aligned, alignment)
            assert aligned >= offset


# 🧱🏗️🔚
