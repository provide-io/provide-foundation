# provide/foundation/file/alignment.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

"""Memory and file alignment utilities for binary I/O and mmap operations.

Provides functions for aligning offsets to power-of-2 boundaries, which is critical for:
- Memory-mapped file operations (mmap requires page alignment)
- Binary file formats and protocols
- Database and index structures
- Network packet alignment
"""

from __future__ import annotations

# Common alignment boundaries
DEFAULT_ALIGNMENT = 16  # 16-byte alignment (cache line on some architectures)
CACHE_LINE_SIZE = 64  # Common cache line size
PAGE_SIZE_4K = 4096  # 4KB page size (common on most systems)
PAGE_SIZE_16K = 16384  # 16KB page size (ARM64, Apple Silicon)
from inspect import signature as _mutmut_signature
from typing import Annotated
from typing import Callable
from typing import ClassVar


MutantDict = Annotated[dict[str, Callable], "Mutant"]


def _mutmut_trampoline(orig, mutants, call_args, call_kwargs, self_arg=None):
    """Forward call to original or mutated function, depending on the environment"""
    import os

    mutant_under_test = os.environ["MUTANT_UNDER_TEST"]
    if mutant_under_test == "fail":
        from mutmut.__main__ import MutmutProgrammaticFailException

        raise MutmutProgrammaticFailException("Failed programmatically")
    elif mutant_under_test == "stats":
        from mutmut.__main__ import record_trampoline_hit

        record_trampoline_hit(orig.__module__ + "." + orig.__name__)
        result = orig(*call_args, **call_kwargs)
        return result
    prefix = orig.__module__ + "." + orig.__name__ + "__mutmut_"
    if not mutant_under_test.startswith(prefix):
        result = orig(*call_args, **call_kwargs)
        return result
    mutant_name = mutant_under_test.rpartition(".")[-1]
    if self_arg:
        # call to a class method where self is not bound
        result = mutants[mutant_name](self_arg, *call_args, **call_kwargs)
    else:
        result = mutants[mutant_name](*call_args, **call_kwargs)
    return result


def x_align_offset__mutmut_orig(offset: int, alignment: int = DEFAULT_ALIGNMENT) -> int:
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


def x_align_offset__mutmut_1(offset: int, alignment: int = DEFAULT_ALIGNMENT) -> int:
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
    if alignment <= 0 and (alignment & (alignment - 1)) != 0:
        raise ValueError(f"Alignment must be a positive power of 2, got {alignment}")

    return (offset + alignment - 1) & ~(alignment - 1)


def x_align_offset__mutmut_2(offset: int, alignment: int = DEFAULT_ALIGNMENT) -> int:
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
    if alignment < 0 or (alignment & (alignment - 1)) != 0:
        raise ValueError(f"Alignment must be a positive power of 2, got {alignment}")

    return (offset + alignment - 1) & ~(alignment - 1)


def x_align_offset__mutmut_3(offset: int, alignment: int = DEFAULT_ALIGNMENT) -> int:
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
    if alignment <= 1 or (alignment & (alignment - 1)) != 0:
        raise ValueError(f"Alignment must be a positive power of 2, got {alignment}")

    return (offset + alignment - 1) & ~(alignment - 1)


def x_align_offset__mutmut_4(offset: int, alignment: int = DEFAULT_ALIGNMENT) -> int:
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
    if alignment <= 0 or (alignment | (alignment - 1)) != 0:
        raise ValueError(f"Alignment must be a positive power of 2, got {alignment}")

    return (offset + alignment - 1) & ~(alignment - 1)


def x_align_offset__mutmut_5(offset: int, alignment: int = DEFAULT_ALIGNMENT) -> int:
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
    if alignment <= 0 or (alignment & (alignment + 1)) != 0:
        raise ValueError(f"Alignment must be a positive power of 2, got {alignment}")

    return (offset + alignment - 1) & ~(alignment - 1)


def x_align_offset__mutmut_6(offset: int, alignment: int = DEFAULT_ALIGNMENT) -> int:
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
    if alignment <= 0 or (alignment & (alignment - 2)) != 0:
        raise ValueError(f"Alignment must be a positive power of 2, got {alignment}")

    return (offset + alignment - 1) & ~(alignment - 1)


def x_align_offset__mutmut_7(offset: int, alignment: int = DEFAULT_ALIGNMENT) -> int:
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
    if alignment <= 0 or (alignment & (alignment - 1)) == 0:
        raise ValueError(f"Alignment must be a positive power of 2, got {alignment}")

    return (offset + alignment - 1) & ~(alignment - 1)


def x_align_offset__mutmut_8(offset: int, alignment: int = DEFAULT_ALIGNMENT) -> int:
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
    if alignment <= 0 or (alignment & (alignment - 1)) != 1:
        raise ValueError(f"Alignment must be a positive power of 2, got {alignment}")

    return (offset + alignment - 1) & ~(alignment - 1)


def x_align_offset__mutmut_9(offset: int, alignment: int = DEFAULT_ALIGNMENT) -> int:
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
        raise ValueError(None)

    return (offset + alignment - 1) & ~(alignment - 1)


def x_align_offset__mutmut_10(offset: int, alignment: int = DEFAULT_ALIGNMENT) -> int:
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

    return (offset + alignment - 1) | ~(alignment - 1)


def x_align_offset__mutmut_11(offset: int, alignment: int = DEFAULT_ALIGNMENT) -> int:
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

    return (offset + alignment + 1) & ~(alignment - 1)


def x_align_offset__mutmut_12(offset: int, alignment: int = DEFAULT_ALIGNMENT) -> int:
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

    return (offset - alignment - 1) & ~(alignment - 1)


def x_align_offset__mutmut_13(offset: int, alignment: int = DEFAULT_ALIGNMENT) -> int:
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

    return (offset + alignment - 2) & ~(alignment - 1)


def x_align_offset__mutmut_14(offset: int, alignment: int = DEFAULT_ALIGNMENT) -> int:
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

    return (offset + alignment - 1) & (alignment - 1)


def x_align_offset__mutmut_15(offset: int, alignment: int = DEFAULT_ALIGNMENT) -> int:
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

    return (offset + alignment - 1) & ~(alignment + 1)


def x_align_offset__mutmut_16(offset: int, alignment: int = DEFAULT_ALIGNMENT) -> int:
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

    return (offset + alignment - 1) & ~(alignment - 2)


x_align_offset__mutmut_mutants: ClassVar[MutantDict] = {
    "x_align_offset__mutmut_1": x_align_offset__mutmut_1,
    "x_align_offset__mutmut_2": x_align_offset__mutmut_2,
    "x_align_offset__mutmut_3": x_align_offset__mutmut_3,
    "x_align_offset__mutmut_4": x_align_offset__mutmut_4,
    "x_align_offset__mutmut_5": x_align_offset__mutmut_5,
    "x_align_offset__mutmut_6": x_align_offset__mutmut_6,
    "x_align_offset__mutmut_7": x_align_offset__mutmut_7,
    "x_align_offset__mutmut_8": x_align_offset__mutmut_8,
    "x_align_offset__mutmut_9": x_align_offset__mutmut_9,
    "x_align_offset__mutmut_10": x_align_offset__mutmut_10,
    "x_align_offset__mutmut_11": x_align_offset__mutmut_11,
    "x_align_offset__mutmut_12": x_align_offset__mutmut_12,
    "x_align_offset__mutmut_13": x_align_offset__mutmut_13,
    "x_align_offset__mutmut_14": x_align_offset__mutmut_14,
    "x_align_offset__mutmut_15": x_align_offset__mutmut_15,
    "x_align_offset__mutmut_16": x_align_offset__mutmut_16,
}


def align_offset(*args, **kwargs):
    result = _mutmut_trampoline(x_align_offset__mutmut_orig, x_align_offset__mutmut_mutants, args, kwargs)
    return result


align_offset.__signature__ = _mutmut_signature(x_align_offset__mutmut_orig)
x_align_offset__mutmut_orig.__name__ = "x_align_offset"


def x_align_to_page__mutmut_orig(offset: int, page_size: int = PAGE_SIZE_4K) -> int:
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


def x_align_to_page__mutmut_1(offset: int, page_size: int = PAGE_SIZE_4K) -> int:
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
    return align_offset(None, page_size)


def x_align_to_page__mutmut_2(offset: int, page_size: int = PAGE_SIZE_4K) -> int:
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
    return align_offset(offset, None)


def x_align_to_page__mutmut_3(offset: int, page_size: int = PAGE_SIZE_4K) -> int:
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
    return align_offset(page_size)


def x_align_to_page__mutmut_4(offset: int, page_size: int = PAGE_SIZE_4K) -> int:
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
    return align_offset(
        offset,
    )


x_align_to_page__mutmut_mutants: ClassVar[MutantDict] = {
    "x_align_to_page__mutmut_1": x_align_to_page__mutmut_1,
    "x_align_to_page__mutmut_2": x_align_to_page__mutmut_2,
    "x_align_to_page__mutmut_3": x_align_to_page__mutmut_3,
    "x_align_to_page__mutmut_4": x_align_to_page__mutmut_4,
}


def align_to_page(*args, **kwargs):
    result = _mutmut_trampoline(x_align_to_page__mutmut_orig, x_align_to_page__mutmut_mutants, args, kwargs)
    return result


align_to_page.__signature__ = _mutmut_signature(x_align_to_page__mutmut_orig)
x_align_to_page__mutmut_orig.__name__ = "x_align_to_page"


def x_is_aligned__mutmut_orig(offset: int, alignment: int = DEFAULT_ALIGNMENT) -> bool:
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


def x_is_aligned__mutmut_1(offset: int, alignment: int = DEFAULT_ALIGNMENT) -> bool:
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
    if alignment <= 0 and (alignment & (alignment - 1)) != 0:
        raise ValueError(f"Alignment must be a positive power of 2, got {alignment}")

    return (offset & (alignment - 1)) == 0


def x_is_aligned__mutmut_2(offset: int, alignment: int = DEFAULT_ALIGNMENT) -> bool:
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
    if alignment < 0 or (alignment & (alignment - 1)) != 0:
        raise ValueError(f"Alignment must be a positive power of 2, got {alignment}")

    return (offset & (alignment - 1)) == 0


def x_is_aligned__mutmut_3(offset: int, alignment: int = DEFAULT_ALIGNMENT) -> bool:
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
    if alignment <= 1 or (alignment & (alignment - 1)) != 0:
        raise ValueError(f"Alignment must be a positive power of 2, got {alignment}")

    return (offset & (alignment - 1)) == 0


def x_is_aligned__mutmut_4(offset: int, alignment: int = DEFAULT_ALIGNMENT) -> bool:
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
    if alignment <= 0 or (alignment | (alignment - 1)) != 0:
        raise ValueError(f"Alignment must be a positive power of 2, got {alignment}")

    return (offset & (alignment - 1)) == 0


def x_is_aligned__mutmut_5(offset: int, alignment: int = DEFAULT_ALIGNMENT) -> bool:
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
    if alignment <= 0 or (alignment & (alignment + 1)) != 0:
        raise ValueError(f"Alignment must be a positive power of 2, got {alignment}")

    return (offset & (alignment - 1)) == 0


def x_is_aligned__mutmut_6(offset: int, alignment: int = DEFAULT_ALIGNMENT) -> bool:
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
    if alignment <= 0 or (alignment & (alignment - 2)) != 0:
        raise ValueError(f"Alignment must be a positive power of 2, got {alignment}")

    return (offset & (alignment - 1)) == 0


def x_is_aligned__mutmut_7(offset: int, alignment: int = DEFAULT_ALIGNMENT) -> bool:
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
    if alignment <= 0 or (alignment & (alignment - 1)) == 0:
        raise ValueError(f"Alignment must be a positive power of 2, got {alignment}")

    return (offset & (alignment - 1)) == 0


def x_is_aligned__mutmut_8(offset: int, alignment: int = DEFAULT_ALIGNMENT) -> bool:
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
    if alignment <= 0 or (alignment & (alignment - 1)) != 1:
        raise ValueError(f"Alignment must be a positive power of 2, got {alignment}")

    return (offset & (alignment - 1)) == 0


def x_is_aligned__mutmut_9(offset: int, alignment: int = DEFAULT_ALIGNMENT) -> bool:
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
        raise ValueError(None)

    return (offset & (alignment - 1)) == 0


def x_is_aligned__mutmut_10(offset: int, alignment: int = DEFAULT_ALIGNMENT) -> bool:
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

    return (offset | (alignment - 1)) == 0


def x_is_aligned__mutmut_11(offset: int, alignment: int = DEFAULT_ALIGNMENT) -> bool:
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

    return (offset & (alignment + 1)) == 0


def x_is_aligned__mutmut_12(offset: int, alignment: int = DEFAULT_ALIGNMENT) -> bool:
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

    return (offset & (alignment - 2)) == 0


def x_is_aligned__mutmut_13(offset: int, alignment: int = DEFAULT_ALIGNMENT) -> bool:
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

    return (offset & (alignment - 1)) != 0


def x_is_aligned__mutmut_14(offset: int, alignment: int = DEFAULT_ALIGNMENT) -> bool:
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

    return (offset & (alignment - 1)) == 1


x_is_aligned__mutmut_mutants: ClassVar[MutantDict] = {
    "x_is_aligned__mutmut_1": x_is_aligned__mutmut_1,
    "x_is_aligned__mutmut_2": x_is_aligned__mutmut_2,
    "x_is_aligned__mutmut_3": x_is_aligned__mutmut_3,
    "x_is_aligned__mutmut_4": x_is_aligned__mutmut_4,
    "x_is_aligned__mutmut_5": x_is_aligned__mutmut_5,
    "x_is_aligned__mutmut_6": x_is_aligned__mutmut_6,
    "x_is_aligned__mutmut_7": x_is_aligned__mutmut_7,
    "x_is_aligned__mutmut_8": x_is_aligned__mutmut_8,
    "x_is_aligned__mutmut_9": x_is_aligned__mutmut_9,
    "x_is_aligned__mutmut_10": x_is_aligned__mutmut_10,
    "x_is_aligned__mutmut_11": x_is_aligned__mutmut_11,
    "x_is_aligned__mutmut_12": x_is_aligned__mutmut_12,
    "x_is_aligned__mutmut_13": x_is_aligned__mutmut_13,
    "x_is_aligned__mutmut_14": x_is_aligned__mutmut_14,
}


def is_aligned(*args, **kwargs):
    result = _mutmut_trampoline(x_is_aligned__mutmut_orig, x_is_aligned__mutmut_mutants, args, kwargs)
    return result


is_aligned.__signature__ = _mutmut_signature(x_is_aligned__mutmut_orig)
x_is_aligned__mutmut_orig.__name__ = "x_is_aligned"


def x_calculate_padding__mutmut_orig(current_offset: int, alignment: int = DEFAULT_ALIGNMENT) -> int:
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


def x_calculate_padding__mutmut_1(current_offset: int, alignment: int = DEFAULT_ALIGNMENT) -> int:
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
    if alignment <= 0 and (alignment & (alignment - 1)) != 0:
        raise ValueError(f"Alignment must be a positive power of 2, got {alignment}")

    aligned = align_offset(current_offset, alignment)
    return aligned - current_offset


def x_calculate_padding__mutmut_2(current_offset: int, alignment: int = DEFAULT_ALIGNMENT) -> int:
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
    if alignment < 0 or (alignment & (alignment - 1)) != 0:
        raise ValueError(f"Alignment must be a positive power of 2, got {alignment}")

    aligned = align_offset(current_offset, alignment)
    return aligned - current_offset


def x_calculate_padding__mutmut_3(current_offset: int, alignment: int = DEFAULT_ALIGNMENT) -> int:
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
    if alignment <= 1 or (alignment & (alignment - 1)) != 0:
        raise ValueError(f"Alignment must be a positive power of 2, got {alignment}")

    aligned = align_offset(current_offset, alignment)
    return aligned - current_offset


def x_calculate_padding__mutmut_4(current_offset: int, alignment: int = DEFAULT_ALIGNMENT) -> int:
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
    if alignment <= 0 or (alignment | (alignment - 1)) != 0:
        raise ValueError(f"Alignment must be a positive power of 2, got {alignment}")

    aligned = align_offset(current_offset, alignment)
    return aligned - current_offset


def x_calculate_padding__mutmut_5(current_offset: int, alignment: int = DEFAULT_ALIGNMENT) -> int:
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
    if alignment <= 0 or (alignment & (alignment + 1)) != 0:
        raise ValueError(f"Alignment must be a positive power of 2, got {alignment}")

    aligned = align_offset(current_offset, alignment)
    return aligned - current_offset


def x_calculate_padding__mutmut_6(current_offset: int, alignment: int = DEFAULT_ALIGNMENT) -> int:
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
    if alignment <= 0 or (alignment & (alignment - 2)) != 0:
        raise ValueError(f"Alignment must be a positive power of 2, got {alignment}")

    aligned = align_offset(current_offset, alignment)
    return aligned - current_offset


def x_calculate_padding__mutmut_7(current_offset: int, alignment: int = DEFAULT_ALIGNMENT) -> int:
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
    if alignment <= 0 or (alignment & (alignment - 1)) == 0:
        raise ValueError(f"Alignment must be a positive power of 2, got {alignment}")

    aligned = align_offset(current_offset, alignment)
    return aligned - current_offset


def x_calculate_padding__mutmut_8(current_offset: int, alignment: int = DEFAULT_ALIGNMENT) -> int:
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
    if alignment <= 0 or (alignment & (alignment - 1)) != 1:
        raise ValueError(f"Alignment must be a positive power of 2, got {alignment}")

    aligned = align_offset(current_offset, alignment)
    return aligned - current_offset


def x_calculate_padding__mutmut_9(current_offset: int, alignment: int = DEFAULT_ALIGNMENT) -> int:
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
        raise ValueError(None)

    aligned = align_offset(current_offset, alignment)
    return aligned - current_offset


def x_calculate_padding__mutmut_10(current_offset: int, alignment: int = DEFAULT_ALIGNMENT) -> int:
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

    aligned = None
    return aligned - current_offset


def x_calculate_padding__mutmut_11(current_offset: int, alignment: int = DEFAULT_ALIGNMENT) -> int:
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

    aligned = align_offset(None, alignment)
    return aligned - current_offset


def x_calculate_padding__mutmut_12(current_offset: int, alignment: int = DEFAULT_ALIGNMENT) -> int:
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

    aligned = align_offset(current_offset, None)
    return aligned - current_offset


def x_calculate_padding__mutmut_13(current_offset: int, alignment: int = DEFAULT_ALIGNMENT) -> int:
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

    aligned = align_offset(alignment)
    return aligned - current_offset


def x_calculate_padding__mutmut_14(current_offset: int, alignment: int = DEFAULT_ALIGNMENT) -> int:
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

    aligned = align_offset(
        current_offset,
    )
    return aligned - current_offset


def x_calculate_padding__mutmut_15(current_offset: int, alignment: int = DEFAULT_ALIGNMENT) -> int:
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
    return aligned + current_offset


x_calculate_padding__mutmut_mutants: ClassVar[MutantDict] = {
    "x_calculate_padding__mutmut_1": x_calculate_padding__mutmut_1,
    "x_calculate_padding__mutmut_2": x_calculate_padding__mutmut_2,
    "x_calculate_padding__mutmut_3": x_calculate_padding__mutmut_3,
    "x_calculate_padding__mutmut_4": x_calculate_padding__mutmut_4,
    "x_calculate_padding__mutmut_5": x_calculate_padding__mutmut_5,
    "x_calculate_padding__mutmut_6": x_calculate_padding__mutmut_6,
    "x_calculate_padding__mutmut_7": x_calculate_padding__mutmut_7,
    "x_calculate_padding__mutmut_8": x_calculate_padding__mutmut_8,
    "x_calculate_padding__mutmut_9": x_calculate_padding__mutmut_9,
    "x_calculate_padding__mutmut_10": x_calculate_padding__mutmut_10,
    "x_calculate_padding__mutmut_11": x_calculate_padding__mutmut_11,
    "x_calculate_padding__mutmut_12": x_calculate_padding__mutmut_12,
    "x_calculate_padding__mutmut_13": x_calculate_padding__mutmut_13,
    "x_calculate_padding__mutmut_14": x_calculate_padding__mutmut_14,
    "x_calculate_padding__mutmut_15": x_calculate_padding__mutmut_15,
}


def calculate_padding(*args, **kwargs):
    result = _mutmut_trampoline(
        x_calculate_padding__mutmut_orig, x_calculate_padding__mutmut_mutants, args, kwargs
    )
    return result


calculate_padding.__signature__ = _mutmut_signature(x_calculate_padding__mutmut_orig)
x_calculate_padding__mutmut_orig.__name__ = "x_calculate_padding"


def x_get_system_page_size__mutmut_orig() -> int:
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


def x_get_system_page_size__mutmut_1() -> int:
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
        return os.sysconf(None)
    except (AttributeError, ValueError, OSError):
        # Fallback to common default
        return PAGE_SIZE_4K


def x_get_system_page_size__mutmut_2() -> int:
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
        return os.sysconf("XXSC_PAGE_SIZEXX")
    except (AttributeError, ValueError, OSError):
        # Fallback to common default
        return PAGE_SIZE_4K


def x_get_system_page_size__mutmut_3() -> int:
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
        return os.sysconf("sc_page_size")
    except (AttributeError, ValueError, OSError):
        # Fallback to common default
        return PAGE_SIZE_4K


x_get_system_page_size__mutmut_mutants: ClassVar[MutantDict] = {
    "x_get_system_page_size__mutmut_1": x_get_system_page_size__mutmut_1,
    "x_get_system_page_size__mutmut_2": x_get_system_page_size__mutmut_2,
    "x_get_system_page_size__mutmut_3": x_get_system_page_size__mutmut_3,
}


def get_system_page_size(*args, **kwargs):
    result = _mutmut_trampoline(
        x_get_system_page_size__mutmut_orig, x_get_system_page_size__mutmut_mutants, args, kwargs
    )
    return result


get_system_page_size.__signature__ = _mutmut_signature(x_get_system_page_size__mutmut_orig)
x_get_system_page_size__mutmut_orig.__name__ = "x_get_system_page_size"


def x_is_power_of_two__mutmut_orig(value: int) -> bool:
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


def x_is_power_of_two__mutmut_1(value: int) -> bool:
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
    return value > 0 or (value & (value - 1)) == 0


def x_is_power_of_two__mutmut_2(value: int) -> bool:
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
    return value >= 0 and (value & (value - 1)) == 0


def x_is_power_of_two__mutmut_3(value: int) -> bool:
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
    return value > 1 and (value & (value - 1)) == 0


def x_is_power_of_two__mutmut_4(value: int) -> bool:
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
    return value > 0 and (value | (value - 1)) == 0


def x_is_power_of_two__mutmut_5(value: int) -> bool:
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
    return value > 0 and (value & (value + 1)) == 0


def x_is_power_of_two__mutmut_6(value: int) -> bool:
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
    return value > 0 and (value & (value - 2)) == 0


def x_is_power_of_two__mutmut_7(value: int) -> bool:
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
    return value > 0 and (value & (value - 1)) != 0


def x_is_power_of_two__mutmut_8(value: int) -> bool:
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
    return value > 0 and (value & (value - 1)) == 1


x_is_power_of_two__mutmut_mutants: ClassVar[MutantDict] = {
    "x_is_power_of_two__mutmut_1": x_is_power_of_two__mutmut_1,
    "x_is_power_of_two__mutmut_2": x_is_power_of_two__mutmut_2,
    "x_is_power_of_two__mutmut_3": x_is_power_of_two__mutmut_3,
    "x_is_power_of_two__mutmut_4": x_is_power_of_two__mutmut_4,
    "x_is_power_of_two__mutmut_5": x_is_power_of_two__mutmut_5,
    "x_is_power_of_two__mutmut_6": x_is_power_of_two__mutmut_6,
    "x_is_power_of_two__mutmut_7": x_is_power_of_two__mutmut_7,
    "x_is_power_of_two__mutmut_8": x_is_power_of_two__mutmut_8,
}


def is_power_of_two(*args, **kwargs):
    result = _mutmut_trampoline(
        x_is_power_of_two__mutmut_orig, x_is_power_of_two__mutmut_mutants, args, kwargs
    )
    return result


is_power_of_two.__signature__ = _mutmut_signature(x_is_power_of_two__mutmut_orig)
x_is_power_of_two__mutmut_orig.__name__ = "x_is_power_of_two"


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


# <3 🧱🤝📄🪄
