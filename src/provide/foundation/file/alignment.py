#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Memory and file alignment utilities for binary I/O and mmap operations.

Provides functions for aligning offsets to power-of-2 boundaries, which is critical for:
- Memory-mapped file operations (mmap requires page alignment)
- Binary file formats and protocols
- Database and index structures
- Network packet alignment"""

from __future__ import annotations

# Common alignment boundaries
DEFAULT_ALIGNMENT = 16  # 16-byte alignment (cache line on some architectures)
CACHE_LINE_SIZE = 64  # Common cache line size
PAGE_SIZE_4K = 4096  # 4KB page size (common on most systems)
PAGE_SIZE_16K = 16384  # 16KB page size (ARM64, Apple Silicon)


def align_offset(offset: int, alignment: int = DEFAULT_ALIGNMENT) -> int:
    """Align offset to specified boundary.

    Aligns an offset up to the next boundary. The alignment must be a power of 2.

    Args:
        offset: The offset to align (in bytes)
        alignment: Alignment boundary in bytes (must be power of 2)

    Returns:
        Aligned offset (>= input offset)

    Raises:
        ValueError: If alignment is not a power of 2 or is <= 0

    Examples:
        >>> align_offset(10, 16)
        16
        >>> align_offset(16, 16)
        16
        >>> align_offset(17, 16)
        32
        >>> align_offset(0, 16)
        0

    Notes:
        Uses bit manipulation for efficiency:
        aligned = (offset + alignment - 1) & ~(alignment - 1)
    """
    if alignment <= 0 or (alignment & (alignment - 1)) != 0:
        raise ValueError(f"Alignment must be a positive power of 2, got {alignment}")

    return (offset + alignment - 1) & ~(alignment - 1)


def align_to_page(offset: int, page_size: int = PAGE_SIZE_4K) -> int:
    """Align offset to page boundary for optimal mmap performance.

    Page alignment is required for memory-mapped file operations on most systems.
    Common page sizes:
    - 4KB (4096 bytes): Most x86_64 systems, Linux, Windows
    - 16KB (16384 bytes): Apple Silicon (M1/M2/M3), some ARM64 systems

    Args:
        offset: The offset to align (in bytes)
        page_size: Page size in bytes (default: 4096)

    Returns:
        Page-aligned offset (>= input offset)

    Raises:
        ValueError: If page_size is not a power of 2

    Examples:
        >>> align_to_page(100)
        4096
        >>> align_to_page(4096)
        4096
        >>> align_to_page(4097)
        8192
        >>> align_to_page(100, page_size=16384)
        16384

    See Also:
        get_system_page_size() for detecting the system's page size
    """
    return align_offset(offset, page_size)


def is_aligned(offset: int, alignment: int = DEFAULT_ALIGNMENT) -> bool:
    """Check if offset is aligned to boundary.

    Args:
        offset: The offset to check (in bytes)
        alignment: Alignment boundary in bytes

    Returns:
        True if offset is aligned to the boundary

    Raises:
        ValueError: If alignment is not a power of 2 or is <= 0

    Examples:
        >>> is_aligned(16, 16)
        True
        >>> is_aligned(17, 16)
        False
        >>> is_aligned(0, 16)
        True
        >>> is_aligned(4096, 4096)
        True

    Notes:
        Uses bit manipulation for efficiency:
        is_aligned = (offset & (alignment - 1)) == 0
    """
    if alignment <= 0 or (alignment & (alignment - 1)) != 0:
        raise ValueError(f"Alignment must be a positive power of 2, got {alignment}")

    return (offset & (alignment - 1)) == 0


def calculate_padding(current_offset: int, alignment: int = DEFAULT_ALIGNMENT) -> int:
    """Calculate padding bytes needed to align to boundary.

    Args:
        current_offset: Current offset position (in bytes)
        alignment: Desired alignment boundary (in bytes)

    Returns:
        Number of padding bytes needed (0 if already aligned)

    Raises:
        ValueError: If alignment is not a power of 2 or is <= 0

    Examples:
        >>> calculate_padding(10, 16)
        6
        >>> calculate_padding(16, 16)
        0
        >>> calculate_padding(17, 16)
        15
        >>> calculate_padding(100, 64)
        28

    Notes:
        This is useful when writing binary formats where you need to insert
        padding bytes to maintain alignment.
    """
    if alignment <= 0 or (alignment & (alignment - 1)) != 0:
        raise ValueError(f"Alignment must be a positive power of 2, got {alignment}")

    aligned = align_offset(current_offset, alignment)
    return aligned - current_offset


def get_system_page_size() -> int:
    """Get the system's page size.

    Returns:
        Page size in bytes (typically 4096 or 16384)

    Examples:
        >>> size = get_system_page_size()
        >>> size in (4096, 16384, 8192, 65536)
        True

    Notes:
        Uses os.sysconf('SC_PAGE_SIZE') on Unix-like systems.
        Falls back to PAGE_SIZE_4K if detection fails.
    """
    import os

    try:
        # Unix-like systems
        return os.sysconf("SC_PAGE_SIZE")
    except (AttributeError, ValueError, OSError):
        # Fallback to common default
        return PAGE_SIZE_4K


def is_power_of_two(value: int) -> bool:
    """Check if a value is a power of 2.

    Args:
        value: Value to check

    Returns:
        True if value is a power of 2

    Examples:
        >>> is_power_of_two(16)
        True
        >>> is_power_of_two(17)
        False
        >>> is_power_of_two(4096)
        True
        >>> is_power_of_two(0)
        False

    Notes:
        Uses bit manipulation: (value & (value - 1)) == 0
    """
    return value > 0 and (value & (value - 1)) == 0


__all__ = [
    "CACHE_LINE_SIZE",
    "DEFAULT_ALIGNMENT",
    "PAGE_SIZE_4K",
    "PAGE_SIZE_16K",
    "align_offset",
    "align_to_page",
    "calculate_padding",
    "get_system_page_size",
    "is_aligned",
    "is_power_of_two",
]

# 🧱🏗️🔚
