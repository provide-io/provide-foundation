# provide/foundation/crypto/utils.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import hashlib

"""Utility functions for hashing and cryptographic operations."""
from inspect import signature as _mutmut_signature
from typing import Annotated
from typing import Callable
from typing import ClassVar


MutantDict = Annotated[dict[str, Callable], "Mutant"]


def _mutmut_trampoline(orig, mutants, call_args, call_kwargs, self_arg = None):
    """Forward call to original or mutated function, depending on the environment"""
    import os
    mutant_under_test = os.environ['MUTANT_UNDER_TEST']
    if mutant_under_test == 'fail':
        from mutmut.__main__ import MutmutProgrammaticFailException
        raise MutmutProgrammaticFailException('Failed programmatically')      
    elif mutant_under_test == 'stats':
        from mutmut.__main__ import record_trampoline_hit
        record_trampoline_hit(orig.__module__ + '.' + orig.__name__)
        result = orig(*call_args, **call_kwargs)
        return result
    prefix = orig.__module__ + '.' + orig.__name__ + '__mutmut_'
    if not mutant_under_test.startswith(prefix):
        result = orig(*call_args, **call_kwargs)
        return result
    mutant_name = mutant_under_test.rpartition('.')[-1]
    if self_arg:
        # call to a class method where self is not bound
        result = mutants[mutant_name](self_arg, *call_args, **call_kwargs)
    else:
        result = mutants[mutant_name](*call_args, **call_kwargs)
    return result


def x_quick_hash__mutmut_orig(data: bytes) -> int:
    """Generate a quick non-cryptographic hash for lookups.

    This uses Python's built-in hash function which is fast but not
    cryptographically secure. Use only for hash tables and caching.

    Args:
        data: Data to hash

    Returns:
        32-bit hash value

    """
    # Use Python's built-in hash for speed, mask to 32 bits
    return hash(data) & 0xFFFFFFFF


def x_quick_hash__mutmut_1(data: bytes) -> int:
    """Generate a quick non-cryptographic hash for lookups.

    This uses Python's built-in hash function which is fast but not
    cryptographically secure. Use only for hash tables and caching.

    Args:
        data: Data to hash

    Returns:
        32-bit hash value

    """
    # Use Python's built-in hash for speed, mask to 32 bits
    return hash(data) | 0xFFFFFFFF


def x_quick_hash__mutmut_2(data: bytes) -> int:
    """Generate a quick non-cryptographic hash for lookups.

    This uses Python's built-in hash function which is fast but not
    cryptographically secure. Use only for hash tables and caching.

    Args:
        data: Data to hash

    Returns:
        32-bit hash value

    """
    # Use Python's built-in hash for speed, mask to 32 bits
    return hash(None) & 0xFFFFFFFF


def x_quick_hash__mutmut_3(data: bytes) -> int:
    """Generate a quick non-cryptographic hash for lookups.

    This uses Python's built-in hash function which is fast but not
    cryptographically secure. Use only for hash tables and caching.

    Args:
        data: Data to hash

    Returns:
        32-bit hash value

    """
    # Use Python's built-in hash for speed, mask to 32 bits
    return hash(data) & 4294967296

x_quick_hash__mutmut_mutants : ClassVar[MutantDict] = {
'x_quick_hash__mutmut_1': x_quick_hash__mutmut_1, 
    'x_quick_hash__mutmut_2': x_quick_hash__mutmut_2, 
    'x_quick_hash__mutmut_3': x_quick_hash__mutmut_3
}

def quick_hash(*args, **kwargs):
    result = _mutmut_trampoline(x_quick_hash__mutmut_orig, x_quick_hash__mutmut_mutants, args, kwargs)
    return result 

quick_hash.__signature__ = _mutmut_signature(x_quick_hash__mutmut_orig)
x_quick_hash__mutmut_orig.__name__ = 'x_quick_hash'


def x_hash_name__mutmut_orig(name: str) -> int:
    """Generate a 64-bit hash of a string for fast lookup.

    This is useful for creating numeric identifiers from strings.

    Args:
        name: String to hash

    Returns:
        64-bit integer hash

    """
    # Use first 8 bytes of SHA256 for good distribution
    hash_bytes = hashlib.sha256(name.encode("utf-8")).digest()[:8]
    return int.from_bytes(hash_bytes, byteorder="little")


def x_hash_name__mutmut_1(name: str) -> int:
    """Generate a 64-bit hash of a string for fast lookup.

    This is useful for creating numeric identifiers from strings.

    Args:
        name: String to hash

    Returns:
        64-bit integer hash

    """
    # Use first 8 bytes of SHA256 for good distribution
    hash_bytes = None
    return int.from_bytes(hash_bytes, byteorder="little")


def x_hash_name__mutmut_2(name: str) -> int:
    """Generate a 64-bit hash of a string for fast lookup.

    This is useful for creating numeric identifiers from strings.

    Args:
        name: String to hash

    Returns:
        64-bit integer hash

    """
    # Use first 8 bytes of SHA256 for good distribution
    hash_bytes = hashlib.sha256(None).digest()[:8]
    return int.from_bytes(hash_bytes, byteorder="little")


def x_hash_name__mutmut_3(name: str) -> int:
    """Generate a 64-bit hash of a string for fast lookup.

    This is useful for creating numeric identifiers from strings.

    Args:
        name: String to hash

    Returns:
        64-bit integer hash

    """
    # Use first 8 bytes of SHA256 for good distribution
    hash_bytes = hashlib.sha256(name.encode(None)).digest()[:8]
    return int.from_bytes(hash_bytes, byteorder="little")


def x_hash_name__mutmut_4(name: str) -> int:
    """Generate a 64-bit hash of a string for fast lookup.

    This is useful for creating numeric identifiers from strings.

    Args:
        name: String to hash

    Returns:
        64-bit integer hash

    """
    # Use first 8 bytes of SHA256 for good distribution
    hash_bytes = hashlib.sha256(name.encode("XXutf-8XX")).digest()[:8]
    return int.from_bytes(hash_bytes, byteorder="little")


def x_hash_name__mutmut_5(name: str) -> int:
    """Generate a 64-bit hash of a string for fast lookup.

    This is useful for creating numeric identifiers from strings.

    Args:
        name: String to hash

    Returns:
        64-bit integer hash

    """
    # Use first 8 bytes of SHA256 for good distribution
    hash_bytes = hashlib.sha256(name.encode("UTF-8")).digest()[:8]
    return int.from_bytes(hash_bytes, byteorder="little")


def x_hash_name__mutmut_6(name: str) -> int:
    """Generate a 64-bit hash of a string for fast lookup.

    This is useful for creating numeric identifiers from strings.

    Args:
        name: String to hash

    Returns:
        64-bit integer hash

    """
    # Use first 8 bytes of SHA256 for good distribution
    hash_bytes = hashlib.sha256(name.encode("utf-8")).digest()[:9]
    return int.from_bytes(hash_bytes, byteorder="little")


def x_hash_name__mutmut_7(name: str) -> int:
    """Generate a 64-bit hash of a string for fast lookup.

    This is useful for creating numeric identifiers from strings.

    Args:
        name: String to hash

    Returns:
        64-bit integer hash

    """
    # Use first 8 bytes of SHA256 for good distribution
    hash_bytes = hashlib.sha256(name.encode("utf-8")).digest()[:8]
    return int.from_bytes(None, byteorder="little")


def x_hash_name__mutmut_8(name: str) -> int:
    """Generate a 64-bit hash of a string for fast lookup.

    This is useful for creating numeric identifiers from strings.

    Args:
        name: String to hash

    Returns:
        64-bit integer hash

    """
    # Use first 8 bytes of SHA256 for good distribution
    hash_bytes = hashlib.sha256(name.encode("utf-8")).digest()[:8]
    return int.from_bytes(hash_bytes, byteorder=None)


def x_hash_name__mutmut_9(name: str) -> int:
    """Generate a 64-bit hash of a string for fast lookup.

    This is useful for creating numeric identifiers from strings.

    Args:
        name: String to hash

    Returns:
        64-bit integer hash

    """
    # Use first 8 bytes of SHA256 for good distribution
    hash_bytes = hashlib.sha256(name.encode("utf-8")).digest()[:8]
    return int.from_bytes(byteorder="little")


def x_hash_name__mutmut_10(name: str) -> int:
    """Generate a 64-bit hash of a string for fast lookup.

    This is useful for creating numeric identifiers from strings.

    Args:
        name: String to hash

    Returns:
        64-bit integer hash

    """
    # Use first 8 bytes of SHA256 for good distribution
    hash_bytes = hashlib.sha256(name.encode("utf-8")).digest()[:8]
    return int.from_bytes(hash_bytes, )


def x_hash_name__mutmut_11(name: str) -> int:
    """Generate a 64-bit hash of a string for fast lookup.

    This is useful for creating numeric identifiers from strings.

    Args:
        name: String to hash

    Returns:
        64-bit integer hash

    """
    # Use first 8 bytes of SHA256 for good distribution
    hash_bytes = hashlib.sha256(name.encode("utf-8")).digest()[:8]
    return int.from_bytes(hash_bytes, byteorder="XXlittleXX")


def x_hash_name__mutmut_12(name: str) -> int:
    """Generate a 64-bit hash of a string for fast lookup.

    This is useful for creating numeric identifiers from strings.

    Args:
        name: String to hash

    Returns:
        64-bit integer hash

    """
    # Use first 8 bytes of SHA256 for good distribution
    hash_bytes = hashlib.sha256(name.encode("utf-8")).digest()[:8]
    return int.from_bytes(hash_bytes, byteorder="LITTLE")

x_hash_name__mutmut_mutants : ClassVar[MutantDict] = {
'x_hash_name__mutmut_1': x_hash_name__mutmut_1, 
    'x_hash_name__mutmut_2': x_hash_name__mutmut_2, 
    'x_hash_name__mutmut_3': x_hash_name__mutmut_3, 
    'x_hash_name__mutmut_4': x_hash_name__mutmut_4, 
    'x_hash_name__mutmut_5': x_hash_name__mutmut_5, 
    'x_hash_name__mutmut_6': x_hash_name__mutmut_6, 
    'x_hash_name__mutmut_7': x_hash_name__mutmut_7, 
    'x_hash_name__mutmut_8': x_hash_name__mutmut_8, 
    'x_hash_name__mutmut_9': x_hash_name__mutmut_9, 
    'x_hash_name__mutmut_10': x_hash_name__mutmut_10, 
    'x_hash_name__mutmut_11': x_hash_name__mutmut_11, 
    'x_hash_name__mutmut_12': x_hash_name__mutmut_12
}

def hash_name(*args, **kwargs):
    result = _mutmut_trampoline(x_hash_name__mutmut_orig, x_hash_name__mutmut_mutants, args, kwargs)
    return result 

hash_name.__signature__ = _mutmut_signature(x_hash_name__mutmut_orig)
x_hash_name__mutmut_orig.__name__ = 'x_hash_name'


def x_compare_hash__mutmut_orig(hash1: str, hash2: str) -> bool:
    """Compare two hash values in a case-insensitive manner.

    Args:
        hash1: First hash value
        hash2: Second hash value

    Returns:
        True if hashes match (case-insensitive)

    """
    return hash1.lower() == hash2.lower()


def x_compare_hash__mutmut_1(hash1: str, hash2: str) -> bool:
    """Compare two hash values in a case-insensitive manner.

    Args:
        hash1: First hash value
        hash2: Second hash value

    Returns:
        True if hashes match (case-insensitive)

    """
    return hash1.upper() == hash2.lower()


def x_compare_hash__mutmut_2(hash1: str, hash2: str) -> bool:
    """Compare two hash values in a case-insensitive manner.

    Args:
        hash1: First hash value
        hash2: Second hash value

    Returns:
        True if hashes match (case-insensitive)

    """
    return hash1.lower() != hash2.lower()


def x_compare_hash__mutmut_3(hash1: str, hash2: str) -> bool:
    """Compare two hash values in a case-insensitive manner.

    Args:
        hash1: First hash value
        hash2: Second hash value

    Returns:
        True if hashes match (case-insensitive)

    """
    return hash1.lower() == hash2.upper()

x_compare_hash__mutmut_mutants : ClassVar[MutantDict] = {
'x_compare_hash__mutmut_1': x_compare_hash__mutmut_1, 
    'x_compare_hash__mutmut_2': x_compare_hash__mutmut_2, 
    'x_compare_hash__mutmut_3': x_compare_hash__mutmut_3
}

def compare_hash(*args, **kwargs):
    result = _mutmut_trampoline(x_compare_hash__mutmut_orig, x_compare_hash__mutmut_mutants, args, kwargs)
    return result 

compare_hash.__signature__ = _mutmut_signature(x_compare_hash__mutmut_orig)
x_compare_hash__mutmut_orig.__name__ = 'x_compare_hash'


def x_format_hash__mutmut_orig(
    hash_value: str,
    group_size: int = 8,
    groups: int = 0,
    separator: str = " ",
) -> str:
    """Format a hash value for display.

    Args:
        hash_value: Hash value to format
        group_size: Number of characters per group
        groups: Number of groups to show (0 for all)
        separator: Separator between groups

    Returns:
        Formatted hash string

    Examples:
        >>> format_hash("abc123def456", group_size=4, separator="-")
        "abc1-23de-f456"
        >>> format_hash("abc123def456", group_size=4, groups=2)
        "abc1 23de"

    """
    if group_size <= 0:
        return hash_value

    formatted_parts = []
    for i in range(0, len(hash_value), group_size):
        formatted_parts.append(hash_value[i : i + group_size])
        if groups > 0 and len(formatted_parts) >= groups:
            break

    return separator.join(formatted_parts)


def x_format_hash__mutmut_1(
    hash_value: str,
    group_size: int = 9,
    groups: int = 0,
    separator: str = " ",
) -> str:
    """Format a hash value for display.

    Args:
        hash_value: Hash value to format
        group_size: Number of characters per group
        groups: Number of groups to show (0 for all)
        separator: Separator between groups

    Returns:
        Formatted hash string

    Examples:
        >>> format_hash("abc123def456", group_size=4, separator="-")
        "abc1-23de-f456"
        >>> format_hash("abc123def456", group_size=4, groups=2)
        "abc1 23de"

    """
    if group_size <= 0:
        return hash_value

    formatted_parts = []
    for i in range(0, len(hash_value), group_size):
        formatted_parts.append(hash_value[i : i + group_size])
        if groups > 0 and len(formatted_parts) >= groups:
            break

    return separator.join(formatted_parts)


def x_format_hash__mutmut_2(
    hash_value: str,
    group_size: int = 8,
    groups: int = 1,
    separator: str = " ",
) -> str:
    """Format a hash value for display.

    Args:
        hash_value: Hash value to format
        group_size: Number of characters per group
        groups: Number of groups to show (0 for all)
        separator: Separator between groups

    Returns:
        Formatted hash string

    Examples:
        >>> format_hash("abc123def456", group_size=4, separator="-")
        "abc1-23de-f456"
        >>> format_hash("abc123def456", group_size=4, groups=2)
        "abc1 23de"

    """
    if group_size <= 0:
        return hash_value

    formatted_parts = []
    for i in range(0, len(hash_value), group_size):
        formatted_parts.append(hash_value[i : i + group_size])
        if groups > 0 and len(formatted_parts) >= groups:
            break

    return separator.join(formatted_parts)


def x_format_hash__mutmut_3(
    hash_value: str,
    group_size: int = 8,
    groups: int = 0,
    separator: str = "XX XX",
) -> str:
    """Format a hash value for display.

    Args:
        hash_value: Hash value to format
        group_size: Number of characters per group
        groups: Number of groups to show (0 for all)
        separator: Separator between groups

    Returns:
        Formatted hash string

    Examples:
        >>> format_hash("abc123def456", group_size=4, separator="-")
        "abc1-23de-f456"
        >>> format_hash("abc123def456", group_size=4, groups=2)
        "abc1 23de"

    """
    if group_size <= 0:
        return hash_value

    formatted_parts = []
    for i in range(0, len(hash_value), group_size):
        formatted_parts.append(hash_value[i : i + group_size])
        if groups > 0 and len(formatted_parts) >= groups:
            break

    return separator.join(formatted_parts)


def x_format_hash__mutmut_4(
    hash_value: str,
    group_size: int = 8,
    groups: int = 0,
    separator: str = " ",
) -> str:
    """Format a hash value for display.

    Args:
        hash_value: Hash value to format
        group_size: Number of characters per group
        groups: Number of groups to show (0 for all)
        separator: Separator between groups

    Returns:
        Formatted hash string

    Examples:
        >>> format_hash("abc123def456", group_size=4, separator="-")
        "abc1-23de-f456"
        >>> format_hash("abc123def456", group_size=4, groups=2)
        "abc1 23de"

    """
    if group_size < 0:
        return hash_value

    formatted_parts = []
    for i in range(0, len(hash_value), group_size):
        formatted_parts.append(hash_value[i : i + group_size])
        if groups > 0 and len(formatted_parts) >= groups:
            break

    return separator.join(formatted_parts)


def x_format_hash__mutmut_5(
    hash_value: str,
    group_size: int = 8,
    groups: int = 0,
    separator: str = " ",
) -> str:
    """Format a hash value for display.

    Args:
        hash_value: Hash value to format
        group_size: Number of characters per group
        groups: Number of groups to show (0 for all)
        separator: Separator between groups

    Returns:
        Formatted hash string

    Examples:
        >>> format_hash("abc123def456", group_size=4, separator="-")
        "abc1-23de-f456"
        >>> format_hash("abc123def456", group_size=4, groups=2)
        "abc1 23de"

    """
    if group_size <= 1:
        return hash_value

    formatted_parts = []
    for i in range(0, len(hash_value), group_size):
        formatted_parts.append(hash_value[i : i + group_size])
        if groups > 0 and len(formatted_parts) >= groups:
            break

    return separator.join(formatted_parts)


def x_format_hash__mutmut_6(
    hash_value: str,
    group_size: int = 8,
    groups: int = 0,
    separator: str = " ",
) -> str:
    """Format a hash value for display.

    Args:
        hash_value: Hash value to format
        group_size: Number of characters per group
        groups: Number of groups to show (0 for all)
        separator: Separator between groups

    Returns:
        Formatted hash string

    Examples:
        >>> format_hash("abc123def456", group_size=4, separator="-")
        "abc1-23de-f456"
        >>> format_hash("abc123def456", group_size=4, groups=2)
        "abc1 23de"

    """
    if group_size <= 0:
        return hash_value

    formatted_parts = None
    for i in range(0, len(hash_value), group_size):
        formatted_parts.append(hash_value[i : i + group_size])
        if groups > 0 and len(formatted_parts) >= groups:
            break

    return separator.join(formatted_parts)


def x_format_hash__mutmut_7(
    hash_value: str,
    group_size: int = 8,
    groups: int = 0,
    separator: str = " ",
) -> str:
    """Format a hash value for display.

    Args:
        hash_value: Hash value to format
        group_size: Number of characters per group
        groups: Number of groups to show (0 for all)
        separator: Separator between groups

    Returns:
        Formatted hash string

    Examples:
        >>> format_hash("abc123def456", group_size=4, separator="-")
        "abc1-23de-f456"
        >>> format_hash("abc123def456", group_size=4, groups=2)
        "abc1 23de"

    """
    if group_size <= 0:
        return hash_value

    formatted_parts = []
    for i in range(None, len(hash_value), group_size):
        formatted_parts.append(hash_value[i : i + group_size])
        if groups > 0 and len(formatted_parts) >= groups:
            break

    return separator.join(formatted_parts)


def x_format_hash__mutmut_8(
    hash_value: str,
    group_size: int = 8,
    groups: int = 0,
    separator: str = " ",
) -> str:
    """Format a hash value for display.

    Args:
        hash_value: Hash value to format
        group_size: Number of characters per group
        groups: Number of groups to show (0 for all)
        separator: Separator between groups

    Returns:
        Formatted hash string

    Examples:
        >>> format_hash("abc123def456", group_size=4, separator="-")
        "abc1-23de-f456"
        >>> format_hash("abc123def456", group_size=4, groups=2)
        "abc1 23de"

    """
    if group_size <= 0:
        return hash_value

    formatted_parts = []
    for i in range(0, None, group_size):
        formatted_parts.append(hash_value[i : i + group_size])
        if groups > 0 and len(formatted_parts) >= groups:
            break

    return separator.join(formatted_parts)


def x_format_hash__mutmut_9(
    hash_value: str,
    group_size: int = 8,
    groups: int = 0,
    separator: str = " ",
) -> str:
    """Format a hash value for display.

    Args:
        hash_value: Hash value to format
        group_size: Number of characters per group
        groups: Number of groups to show (0 for all)
        separator: Separator between groups

    Returns:
        Formatted hash string

    Examples:
        >>> format_hash("abc123def456", group_size=4, separator="-")
        "abc1-23de-f456"
        >>> format_hash("abc123def456", group_size=4, groups=2)
        "abc1 23de"

    """
    if group_size <= 0:
        return hash_value

    formatted_parts = []
    for i in range(0, len(hash_value), None):
        formatted_parts.append(hash_value[i : i + group_size])
        if groups > 0 and len(formatted_parts) >= groups:
            break

    return separator.join(formatted_parts)


def x_format_hash__mutmut_10(
    hash_value: str,
    group_size: int = 8,
    groups: int = 0,
    separator: str = " ",
) -> str:
    """Format a hash value for display.

    Args:
        hash_value: Hash value to format
        group_size: Number of characters per group
        groups: Number of groups to show (0 for all)
        separator: Separator between groups

    Returns:
        Formatted hash string

    Examples:
        >>> format_hash("abc123def456", group_size=4, separator="-")
        "abc1-23de-f456"
        >>> format_hash("abc123def456", group_size=4, groups=2)
        "abc1 23de"

    """
    if group_size <= 0:
        return hash_value

    formatted_parts = []
    for i in range(len(hash_value), group_size):
        formatted_parts.append(hash_value[i : i + group_size])
        if groups > 0 and len(formatted_parts) >= groups:
            break

    return separator.join(formatted_parts)


def x_format_hash__mutmut_11(
    hash_value: str,
    group_size: int = 8,
    groups: int = 0,
    separator: str = " ",
) -> str:
    """Format a hash value for display.

    Args:
        hash_value: Hash value to format
        group_size: Number of characters per group
        groups: Number of groups to show (0 for all)
        separator: Separator between groups

    Returns:
        Formatted hash string

    Examples:
        >>> format_hash("abc123def456", group_size=4, separator="-")
        "abc1-23de-f456"
        >>> format_hash("abc123def456", group_size=4, groups=2)
        "abc1 23de"

    """
    if group_size <= 0:
        return hash_value

    formatted_parts = []
    for i in range(0, group_size):
        formatted_parts.append(hash_value[i : i + group_size])
        if groups > 0 and len(formatted_parts) >= groups:
            break

    return separator.join(formatted_parts)


def x_format_hash__mutmut_12(
    hash_value: str,
    group_size: int = 8,
    groups: int = 0,
    separator: str = " ",
) -> str:
    """Format a hash value for display.

    Args:
        hash_value: Hash value to format
        group_size: Number of characters per group
        groups: Number of groups to show (0 for all)
        separator: Separator between groups

    Returns:
        Formatted hash string

    Examples:
        >>> format_hash("abc123def456", group_size=4, separator="-")
        "abc1-23de-f456"
        >>> format_hash("abc123def456", group_size=4, groups=2)
        "abc1 23de"

    """
    if group_size <= 0:
        return hash_value

    formatted_parts = []
    for i in range(0, len(hash_value), ):
        formatted_parts.append(hash_value[i : i + group_size])
        if groups > 0 and len(formatted_parts) >= groups:
            break

    return separator.join(formatted_parts)


def x_format_hash__mutmut_13(
    hash_value: str,
    group_size: int = 8,
    groups: int = 0,
    separator: str = " ",
) -> str:
    """Format a hash value for display.

    Args:
        hash_value: Hash value to format
        group_size: Number of characters per group
        groups: Number of groups to show (0 for all)
        separator: Separator between groups

    Returns:
        Formatted hash string

    Examples:
        >>> format_hash("abc123def456", group_size=4, separator="-")
        "abc1-23de-f456"
        >>> format_hash("abc123def456", group_size=4, groups=2)
        "abc1 23de"

    """
    if group_size <= 0:
        return hash_value

    formatted_parts = []
    for i in range(1, len(hash_value), group_size):
        formatted_parts.append(hash_value[i : i + group_size])
        if groups > 0 and len(formatted_parts) >= groups:
            break

    return separator.join(formatted_parts)


def x_format_hash__mutmut_14(
    hash_value: str,
    group_size: int = 8,
    groups: int = 0,
    separator: str = " ",
) -> str:
    """Format a hash value for display.

    Args:
        hash_value: Hash value to format
        group_size: Number of characters per group
        groups: Number of groups to show (0 for all)
        separator: Separator between groups

    Returns:
        Formatted hash string

    Examples:
        >>> format_hash("abc123def456", group_size=4, separator="-")
        "abc1-23de-f456"
        >>> format_hash("abc123def456", group_size=4, groups=2)
        "abc1 23de"

    """
    if group_size <= 0:
        return hash_value

    formatted_parts = []
    for i in range(0, len(hash_value), group_size):
        formatted_parts.append(None)
        if groups > 0 and len(formatted_parts) >= groups:
            break

    return separator.join(formatted_parts)


def x_format_hash__mutmut_15(
    hash_value: str,
    group_size: int = 8,
    groups: int = 0,
    separator: str = " ",
) -> str:
    """Format a hash value for display.

    Args:
        hash_value: Hash value to format
        group_size: Number of characters per group
        groups: Number of groups to show (0 for all)
        separator: Separator between groups

    Returns:
        Formatted hash string

    Examples:
        >>> format_hash("abc123def456", group_size=4, separator="-")
        "abc1-23de-f456"
        >>> format_hash("abc123def456", group_size=4, groups=2)
        "abc1 23de"

    """
    if group_size <= 0:
        return hash_value

    formatted_parts = []
    for i in range(0, len(hash_value), group_size):
        formatted_parts.append(hash_value[i : i - group_size])
        if groups > 0 and len(formatted_parts) >= groups:
            break

    return separator.join(formatted_parts)


def x_format_hash__mutmut_16(
    hash_value: str,
    group_size: int = 8,
    groups: int = 0,
    separator: str = " ",
) -> str:
    """Format a hash value for display.

    Args:
        hash_value: Hash value to format
        group_size: Number of characters per group
        groups: Number of groups to show (0 for all)
        separator: Separator between groups

    Returns:
        Formatted hash string

    Examples:
        >>> format_hash("abc123def456", group_size=4, separator="-")
        "abc1-23de-f456"
        >>> format_hash("abc123def456", group_size=4, groups=2)
        "abc1 23de"

    """
    if group_size <= 0:
        return hash_value

    formatted_parts = []
    for i in range(0, len(hash_value), group_size):
        formatted_parts.append(hash_value[i : i + group_size])
        if groups > 0 or len(formatted_parts) >= groups:
            break

    return separator.join(formatted_parts)


def x_format_hash__mutmut_17(
    hash_value: str,
    group_size: int = 8,
    groups: int = 0,
    separator: str = " ",
) -> str:
    """Format a hash value for display.

    Args:
        hash_value: Hash value to format
        group_size: Number of characters per group
        groups: Number of groups to show (0 for all)
        separator: Separator between groups

    Returns:
        Formatted hash string

    Examples:
        >>> format_hash("abc123def456", group_size=4, separator="-")
        "abc1-23de-f456"
        >>> format_hash("abc123def456", group_size=4, groups=2)
        "abc1 23de"

    """
    if group_size <= 0:
        return hash_value

    formatted_parts = []
    for i in range(0, len(hash_value), group_size):
        formatted_parts.append(hash_value[i : i + group_size])
        if groups >= 0 and len(formatted_parts) >= groups:
            break

    return separator.join(formatted_parts)


def x_format_hash__mutmut_18(
    hash_value: str,
    group_size: int = 8,
    groups: int = 0,
    separator: str = " ",
) -> str:
    """Format a hash value for display.

    Args:
        hash_value: Hash value to format
        group_size: Number of characters per group
        groups: Number of groups to show (0 for all)
        separator: Separator between groups

    Returns:
        Formatted hash string

    Examples:
        >>> format_hash("abc123def456", group_size=4, separator="-")
        "abc1-23de-f456"
        >>> format_hash("abc123def456", group_size=4, groups=2)
        "abc1 23de"

    """
    if group_size <= 0:
        return hash_value

    formatted_parts = []
    for i in range(0, len(hash_value), group_size):
        formatted_parts.append(hash_value[i : i + group_size])
        if groups > 1 and len(formatted_parts) >= groups:
            break

    return separator.join(formatted_parts)


def x_format_hash__mutmut_19(
    hash_value: str,
    group_size: int = 8,
    groups: int = 0,
    separator: str = " ",
) -> str:
    """Format a hash value for display.

    Args:
        hash_value: Hash value to format
        group_size: Number of characters per group
        groups: Number of groups to show (0 for all)
        separator: Separator between groups

    Returns:
        Formatted hash string

    Examples:
        >>> format_hash("abc123def456", group_size=4, separator="-")
        "abc1-23de-f456"
        >>> format_hash("abc123def456", group_size=4, groups=2)
        "abc1 23de"

    """
    if group_size <= 0:
        return hash_value

    formatted_parts = []
    for i in range(0, len(hash_value), group_size):
        formatted_parts.append(hash_value[i : i + group_size])
        if groups > 0 and len(formatted_parts) > groups:
            break

    return separator.join(formatted_parts)


def x_format_hash__mutmut_20(
    hash_value: str,
    group_size: int = 8,
    groups: int = 0,
    separator: str = " ",
) -> str:
    """Format a hash value for display.

    Args:
        hash_value: Hash value to format
        group_size: Number of characters per group
        groups: Number of groups to show (0 for all)
        separator: Separator between groups

    Returns:
        Formatted hash string

    Examples:
        >>> format_hash("abc123def456", group_size=4, separator="-")
        "abc1-23de-f456"
        >>> format_hash("abc123def456", group_size=4, groups=2)
        "abc1 23de"

    """
    if group_size <= 0:
        return hash_value

    formatted_parts = []
    for i in range(0, len(hash_value), group_size):
        formatted_parts.append(hash_value[i : i + group_size])
        if groups > 0 and len(formatted_parts) >= groups:
            return

    return separator.join(formatted_parts)


def x_format_hash__mutmut_21(
    hash_value: str,
    group_size: int = 8,
    groups: int = 0,
    separator: str = " ",
) -> str:
    """Format a hash value for display.

    Args:
        hash_value: Hash value to format
        group_size: Number of characters per group
        groups: Number of groups to show (0 for all)
        separator: Separator between groups

    Returns:
        Formatted hash string

    Examples:
        >>> format_hash("abc123def456", group_size=4, separator="-")
        "abc1-23de-f456"
        >>> format_hash("abc123def456", group_size=4, groups=2)
        "abc1 23de"

    """
    if group_size <= 0:
        return hash_value

    formatted_parts = []
    for i in range(0, len(hash_value), group_size):
        formatted_parts.append(hash_value[i : i + group_size])
        if groups > 0 and len(formatted_parts) >= groups:
            break

    return separator.join(None)

x_format_hash__mutmut_mutants : ClassVar[MutantDict] = {
'x_format_hash__mutmut_1': x_format_hash__mutmut_1, 
    'x_format_hash__mutmut_2': x_format_hash__mutmut_2, 
    'x_format_hash__mutmut_3': x_format_hash__mutmut_3, 
    'x_format_hash__mutmut_4': x_format_hash__mutmut_4, 
    'x_format_hash__mutmut_5': x_format_hash__mutmut_5, 
    'x_format_hash__mutmut_6': x_format_hash__mutmut_6, 
    'x_format_hash__mutmut_7': x_format_hash__mutmut_7, 
    'x_format_hash__mutmut_8': x_format_hash__mutmut_8, 
    'x_format_hash__mutmut_9': x_format_hash__mutmut_9, 
    'x_format_hash__mutmut_10': x_format_hash__mutmut_10, 
    'x_format_hash__mutmut_11': x_format_hash__mutmut_11, 
    'x_format_hash__mutmut_12': x_format_hash__mutmut_12, 
    'x_format_hash__mutmut_13': x_format_hash__mutmut_13, 
    'x_format_hash__mutmut_14': x_format_hash__mutmut_14, 
    'x_format_hash__mutmut_15': x_format_hash__mutmut_15, 
    'x_format_hash__mutmut_16': x_format_hash__mutmut_16, 
    'x_format_hash__mutmut_17': x_format_hash__mutmut_17, 
    'x_format_hash__mutmut_18': x_format_hash__mutmut_18, 
    'x_format_hash__mutmut_19': x_format_hash__mutmut_19, 
    'x_format_hash__mutmut_20': x_format_hash__mutmut_20, 
    'x_format_hash__mutmut_21': x_format_hash__mutmut_21
}

def format_hash(*args, **kwargs):
    result = _mutmut_trampoline(x_format_hash__mutmut_orig, x_format_hash__mutmut_mutants, args, kwargs)
    return result 

format_hash.__signature__ = _mutmut_signature(x_format_hash__mutmut_orig)
x_format_hash__mutmut_orig.__name__ = 'x_format_hash'


def x_truncate_hash__mutmut_orig(hash_value: str, length: int = 16, suffix: str = "...") -> str:
    """Truncate a hash for display purposes.

    Args:
        hash_value: Hash value to truncate
        length: Number of characters to keep
        suffix: Suffix to append

    Returns:
        Truncated hash string

    Examples:
        >>> truncate_hash("abc123def456789", length=8)
        "abc123de..."

    """
    if len(hash_value) <= length:
        return hash_value
    return hash_value[:length] + suffix


def x_truncate_hash__mutmut_1(hash_value: str, length: int = 17, suffix: str = "...") -> str:
    """Truncate a hash for display purposes.

    Args:
        hash_value: Hash value to truncate
        length: Number of characters to keep
        suffix: Suffix to append

    Returns:
        Truncated hash string

    Examples:
        >>> truncate_hash("abc123def456789", length=8)
        "abc123de..."

    """
    if len(hash_value) <= length:
        return hash_value
    return hash_value[:length] + suffix


def x_truncate_hash__mutmut_2(hash_value: str, length: int = 16, suffix: str = "XX...XX") -> str:
    """Truncate a hash for display purposes.

    Args:
        hash_value: Hash value to truncate
        length: Number of characters to keep
        suffix: Suffix to append

    Returns:
        Truncated hash string

    Examples:
        >>> truncate_hash("abc123def456789", length=8)
        "abc123de..."

    """
    if len(hash_value) <= length:
        return hash_value
    return hash_value[:length] + suffix


def x_truncate_hash__mutmut_3(hash_value: str, length: int = 16, suffix: str = "...") -> str:
    """Truncate a hash for display purposes.

    Args:
        hash_value: Hash value to truncate
        length: Number of characters to keep
        suffix: Suffix to append

    Returns:
        Truncated hash string

    Examples:
        >>> truncate_hash("abc123def456789", length=8)
        "abc123de..."

    """
    if len(hash_value) < length:
        return hash_value
    return hash_value[:length] + suffix


def x_truncate_hash__mutmut_4(hash_value: str, length: int = 16, suffix: str = "...") -> str:
    """Truncate a hash for display purposes.

    Args:
        hash_value: Hash value to truncate
        length: Number of characters to keep
        suffix: Suffix to append

    Returns:
        Truncated hash string

    Examples:
        >>> truncate_hash("abc123def456789", length=8)
        "abc123de..."

    """
    if len(hash_value) <= length:
        return hash_value
    return hash_value[:length] - suffix

x_truncate_hash__mutmut_mutants : ClassVar[MutantDict] = {
'x_truncate_hash__mutmut_1': x_truncate_hash__mutmut_1, 
    'x_truncate_hash__mutmut_2': x_truncate_hash__mutmut_2, 
    'x_truncate_hash__mutmut_3': x_truncate_hash__mutmut_3, 
    'x_truncate_hash__mutmut_4': x_truncate_hash__mutmut_4
}

def truncate_hash(*args, **kwargs):
    result = _mutmut_trampoline(x_truncate_hash__mutmut_orig, x_truncate_hash__mutmut_mutants, args, kwargs)
    return result 

truncate_hash.__signature__ = _mutmut_signature(x_truncate_hash__mutmut_orig)
x_truncate_hash__mutmut_orig.__name__ = 'x_truncate_hash'


def x_hash_to_int__mutmut_orig(hash_value: str) -> int:
    """Convert a hex hash string to an integer.

    Args:
        hash_value: Hex hash string

    Returns:
        Integer representation of the hash

    """
    return int(hash_value, 16)


def x_hash_to_int__mutmut_1(hash_value: str) -> int:
    """Convert a hex hash string to an integer.

    Args:
        hash_value: Hex hash string

    Returns:
        Integer representation of the hash

    """
    return int(None, 16)


def x_hash_to_int__mutmut_2(hash_value: str) -> int:
    """Convert a hex hash string to an integer.

    Args:
        hash_value: Hex hash string

    Returns:
        Integer representation of the hash

    """
    return int(hash_value, None)


def x_hash_to_int__mutmut_3(hash_value: str) -> int:
    """Convert a hex hash string to an integer.

    Args:
        hash_value: Hex hash string

    Returns:
        Integer representation of the hash

    """
    return int(16)


def x_hash_to_int__mutmut_4(hash_value: str) -> int:
    """Convert a hex hash string to an integer.

    Args:
        hash_value: Hex hash string

    Returns:
        Integer representation of the hash

    """
    return int(hash_value, )


def x_hash_to_int__mutmut_5(hash_value: str) -> int:
    """Convert a hex hash string to an integer.

    Args:
        hash_value: Hex hash string

    Returns:
        Integer representation of the hash

    """
    return int(hash_value, 17)

x_hash_to_int__mutmut_mutants : ClassVar[MutantDict] = {
'x_hash_to_int__mutmut_1': x_hash_to_int__mutmut_1, 
    'x_hash_to_int__mutmut_2': x_hash_to_int__mutmut_2, 
    'x_hash_to_int__mutmut_3': x_hash_to_int__mutmut_3, 
    'x_hash_to_int__mutmut_4': x_hash_to_int__mutmut_4, 
    'x_hash_to_int__mutmut_5': x_hash_to_int__mutmut_5
}

def hash_to_int(*args, **kwargs):
    result = _mutmut_trampoline(x_hash_to_int__mutmut_orig, x_hash_to_int__mutmut_mutants, args, kwargs)
    return result 

hash_to_int.__signature__ = _mutmut_signature(x_hash_to_int__mutmut_orig)
x_hash_to_int__mutmut_orig.__name__ = 'x_hash_to_int'


def x_int_to_hash__mutmut_orig(value: int, length: int | None = None) -> str:
    """Convert an integer to a hex hash string.

    Args:
        value: Integer value
        length: Desired length (will pad with zeros)

    Returns:
        Hex string representation

    """
    hex_str = format(value, "x")
    if length and len(hex_str) < length:
        hex_str = hex_str.zfill(length)
    return hex_str


def x_int_to_hash__mutmut_1(value: int, length: int | None = None) -> str:
    """Convert an integer to a hex hash string.

    Args:
        value: Integer value
        length: Desired length (will pad with zeros)

    Returns:
        Hex string representation

    """
    hex_str = None
    if length and len(hex_str) < length:
        hex_str = hex_str.zfill(length)
    return hex_str


def x_int_to_hash__mutmut_2(value: int, length: int | None = None) -> str:
    """Convert an integer to a hex hash string.

    Args:
        value: Integer value
        length: Desired length (will pad with zeros)

    Returns:
        Hex string representation

    """
    hex_str = format(None, "x")
    if length and len(hex_str) < length:
        hex_str = hex_str.zfill(length)
    return hex_str


def x_int_to_hash__mutmut_3(value: int, length: int | None = None) -> str:
    """Convert an integer to a hex hash string.

    Args:
        value: Integer value
        length: Desired length (will pad with zeros)

    Returns:
        Hex string representation

    """
    hex_str = format(value, None)
    if length and len(hex_str) < length:
        hex_str = hex_str.zfill(length)
    return hex_str


def x_int_to_hash__mutmut_4(value: int, length: int | None = None) -> str:
    """Convert an integer to a hex hash string.

    Args:
        value: Integer value
        length: Desired length (will pad with zeros)

    Returns:
        Hex string representation

    """
    hex_str = format("x")
    if length and len(hex_str) < length:
        hex_str = hex_str.zfill(length)
    return hex_str


def x_int_to_hash__mutmut_5(value: int, length: int | None = None) -> str:
    """Convert an integer to a hex hash string.

    Args:
        value: Integer value
        length: Desired length (will pad with zeros)

    Returns:
        Hex string representation

    """
    hex_str = format(value, )
    if length and len(hex_str) < length:
        hex_str = hex_str.zfill(length)
    return hex_str


def x_int_to_hash__mutmut_6(value: int, length: int | None = None) -> str:
    """Convert an integer to a hex hash string.

    Args:
        value: Integer value
        length: Desired length (will pad with zeros)

    Returns:
        Hex string representation

    """
    hex_str = format(value, "XXxXX")
    if length and len(hex_str) < length:
        hex_str = hex_str.zfill(length)
    return hex_str


def x_int_to_hash__mutmut_7(value: int, length: int | None = None) -> str:
    """Convert an integer to a hex hash string.

    Args:
        value: Integer value
        length: Desired length (will pad with zeros)

    Returns:
        Hex string representation

    """
    hex_str = format(value, "X")
    if length and len(hex_str) < length:
        hex_str = hex_str.zfill(length)
    return hex_str


def x_int_to_hash__mutmut_8(value: int, length: int | None = None) -> str:
    """Convert an integer to a hex hash string.

    Args:
        value: Integer value
        length: Desired length (will pad with zeros)

    Returns:
        Hex string representation

    """
    hex_str = format(value, "x")
    if length or len(hex_str) < length:
        hex_str = hex_str.zfill(length)
    return hex_str


def x_int_to_hash__mutmut_9(value: int, length: int | None = None) -> str:
    """Convert an integer to a hex hash string.

    Args:
        value: Integer value
        length: Desired length (will pad with zeros)

    Returns:
        Hex string representation

    """
    hex_str = format(value, "x")
    if length and len(hex_str) <= length:
        hex_str = hex_str.zfill(length)
    return hex_str


def x_int_to_hash__mutmut_10(value: int, length: int | None = None) -> str:
    """Convert an integer to a hex hash string.

    Args:
        value: Integer value
        length: Desired length (will pad with zeros)

    Returns:
        Hex string representation

    """
    hex_str = format(value, "x")
    if length and len(hex_str) < length:
        hex_str = None
    return hex_str


def x_int_to_hash__mutmut_11(value: int, length: int | None = None) -> str:
    """Convert an integer to a hex hash string.

    Args:
        value: Integer value
        length: Desired length (will pad with zeros)

    Returns:
        Hex string representation

    """
    hex_str = format(value, "x")
    if length and len(hex_str) < length:
        hex_str = hex_str.zfill(None)
    return hex_str

x_int_to_hash__mutmut_mutants : ClassVar[MutantDict] = {
'x_int_to_hash__mutmut_1': x_int_to_hash__mutmut_1, 
    'x_int_to_hash__mutmut_2': x_int_to_hash__mutmut_2, 
    'x_int_to_hash__mutmut_3': x_int_to_hash__mutmut_3, 
    'x_int_to_hash__mutmut_4': x_int_to_hash__mutmut_4, 
    'x_int_to_hash__mutmut_5': x_int_to_hash__mutmut_5, 
    'x_int_to_hash__mutmut_6': x_int_to_hash__mutmut_6, 
    'x_int_to_hash__mutmut_7': x_int_to_hash__mutmut_7, 
    'x_int_to_hash__mutmut_8': x_int_to_hash__mutmut_8, 
    'x_int_to_hash__mutmut_9': x_int_to_hash__mutmut_9, 
    'x_int_to_hash__mutmut_10': x_int_to_hash__mutmut_10, 
    'x_int_to_hash__mutmut_11': x_int_to_hash__mutmut_11
}

def int_to_hash(*args, **kwargs):
    result = _mutmut_trampoline(x_int_to_hash__mutmut_orig, x_int_to_hash__mutmut_mutants, args, kwargs)
    return result 

int_to_hash.__signature__ = _mutmut_signature(x_int_to_hash__mutmut_orig)
x_int_to_hash__mutmut_orig.__name__ = 'x_int_to_hash'


def x_is_valid_hash__mutmut_orig(hash_value: str, algorithm: str | None = None) -> bool:
    """Check if a string is a valid hash value.

    Args:
        hash_value: String to check
        algorithm: Optional algorithm to validate length against

    Returns:
        True if string appears to be a valid hash

    """
    # Check if it's a valid hex string
    try:
        int(hash_value, 16)
    except ValueError:
        return False

    # If algorithm specified, check length
    if algorithm:
        from provide.foundation.crypto.algorithms import (
            get_digest_size,
            validate_algorithm,
        )

        try:
            validate_algorithm(algorithm)
            expected_length = get_digest_size(algorithm) * 2  # hex is 2 chars per byte
            return len(hash_value) == expected_length
        except Exception:
            return False

    return True


def x_is_valid_hash__mutmut_1(hash_value: str, algorithm: str | None = None) -> bool:
    """Check if a string is a valid hash value.

    Args:
        hash_value: String to check
        algorithm: Optional algorithm to validate length against

    Returns:
        True if string appears to be a valid hash

    """
    # Check if it's a valid hex string
    try:
        int(None, 16)
    except ValueError:
        return False

    # If algorithm specified, check length
    if algorithm:
        from provide.foundation.crypto.algorithms import (
            get_digest_size,
            validate_algorithm,
        )

        try:
            validate_algorithm(algorithm)
            expected_length = get_digest_size(algorithm) * 2  # hex is 2 chars per byte
            return len(hash_value) == expected_length
        except Exception:
            return False

    return True


def x_is_valid_hash__mutmut_2(hash_value: str, algorithm: str | None = None) -> bool:
    """Check if a string is a valid hash value.

    Args:
        hash_value: String to check
        algorithm: Optional algorithm to validate length against

    Returns:
        True if string appears to be a valid hash

    """
    # Check if it's a valid hex string
    try:
        int(hash_value, None)
    except ValueError:
        return False

    # If algorithm specified, check length
    if algorithm:
        from provide.foundation.crypto.algorithms import (
            get_digest_size,
            validate_algorithm,
        )

        try:
            validate_algorithm(algorithm)
            expected_length = get_digest_size(algorithm) * 2  # hex is 2 chars per byte
            return len(hash_value) == expected_length
        except Exception:
            return False

    return True


def x_is_valid_hash__mutmut_3(hash_value: str, algorithm: str | None = None) -> bool:
    """Check if a string is a valid hash value.

    Args:
        hash_value: String to check
        algorithm: Optional algorithm to validate length against

    Returns:
        True if string appears to be a valid hash

    """
    # Check if it's a valid hex string
    try:
        int(16)
    except ValueError:
        return False

    # If algorithm specified, check length
    if algorithm:
        from provide.foundation.crypto.algorithms import (
            get_digest_size,
            validate_algorithm,
        )

        try:
            validate_algorithm(algorithm)
            expected_length = get_digest_size(algorithm) * 2  # hex is 2 chars per byte
            return len(hash_value) == expected_length
        except Exception:
            return False

    return True


def x_is_valid_hash__mutmut_4(hash_value: str, algorithm: str | None = None) -> bool:
    """Check if a string is a valid hash value.

    Args:
        hash_value: String to check
        algorithm: Optional algorithm to validate length against

    Returns:
        True if string appears to be a valid hash

    """
    # Check if it's a valid hex string
    try:
        int(hash_value, )
    except ValueError:
        return False

    # If algorithm specified, check length
    if algorithm:
        from provide.foundation.crypto.algorithms import (
            get_digest_size,
            validate_algorithm,
        )

        try:
            validate_algorithm(algorithm)
            expected_length = get_digest_size(algorithm) * 2  # hex is 2 chars per byte
            return len(hash_value) == expected_length
        except Exception:
            return False

    return True


def x_is_valid_hash__mutmut_5(hash_value: str, algorithm: str | None = None) -> bool:
    """Check if a string is a valid hash value.

    Args:
        hash_value: String to check
        algorithm: Optional algorithm to validate length against

    Returns:
        True if string appears to be a valid hash

    """
    # Check if it's a valid hex string
    try:
        int(hash_value, 17)
    except ValueError:
        return False

    # If algorithm specified, check length
    if algorithm:
        from provide.foundation.crypto.algorithms import (
            get_digest_size,
            validate_algorithm,
        )

        try:
            validate_algorithm(algorithm)
            expected_length = get_digest_size(algorithm) * 2  # hex is 2 chars per byte
            return len(hash_value) == expected_length
        except Exception:
            return False

    return True


def x_is_valid_hash__mutmut_6(hash_value: str, algorithm: str | None = None) -> bool:
    """Check if a string is a valid hash value.

    Args:
        hash_value: String to check
        algorithm: Optional algorithm to validate length against

    Returns:
        True if string appears to be a valid hash

    """
    # Check if it's a valid hex string
    try:
        int(hash_value, 16)
    except ValueError:
        return True

    # If algorithm specified, check length
    if algorithm:
        from provide.foundation.crypto.algorithms import (
            get_digest_size,
            validate_algorithm,
        )

        try:
            validate_algorithm(algorithm)
            expected_length = get_digest_size(algorithm) * 2  # hex is 2 chars per byte
            return len(hash_value) == expected_length
        except Exception:
            return False

    return True


def x_is_valid_hash__mutmut_7(hash_value: str, algorithm: str | None = None) -> bool:
    """Check if a string is a valid hash value.

    Args:
        hash_value: String to check
        algorithm: Optional algorithm to validate length against

    Returns:
        True if string appears to be a valid hash

    """
    # Check if it's a valid hex string
    try:
        int(hash_value, 16)
    except ValueError:
        return False

    # If algorithm specified, check length
    if algorithm:
        from provide.foundation.crypto.algorithms import (
            get_digest_size,
            validate_algorithm,
        )

        try:
            validate_algorithm(None)
            expected_length = get_digest_size(algorithm) * 2  # hex is 2 chars per byte
            return len(hash_value) == expected_length
        except Exception:
            return False

    return True


def x_is_valid_hash__mutmut_8(hash_value: str, algorithm: str | None = None) -> bool:
    """Check if a string is a valid hash value.

    Args:
        hash_value: String to check
        algorithm: Optional algorithm to validate length against

    Returns:
        True if string appears to be a valid hash

    """
    # Check if it's a valid hex string
    try:
        int(hash_value, 16)
    except ValueError:
        return False

    # If algorithm specified, check length
    if algorithm:
        from provide.foundation.crypto.algorithms import (
            get_digest_size,
            validate_algorithm,
        )

        try:
            validate_algorithm(algorithm)
            expected_length = None  # hex is 2 chars per byte
            return len(hash_value) == expected_length
        except Exception:
            return False

    return True


def x_is_valid_hash__mutmut_9(hash_value: str, algorithm: str | None = None) -> bool:
    """Check if a string is a valid hash value.

    Args:
        hash_value: String to check
        algorithm: Optional algorithm to validate length against

    Returns:
        True if string appears to be a valid hash

    """
    # Check if it's a valid hex string
    try:
        int(hash_value, 16)
    except ValueError:
        return False

    # If algorithm specified, check length
    if algorithm:
        from provide.foundation.crypto.algorithms import (
            get_digest_size,
            validate_algorithm,
        )

        try:
            validate_algorithm(algorithm)
            expected_length = get_digest_size(algorithm) / 2  # hex is 2 chars per byte
            return len(hash_value) == expected_length
        except Exception:
            return False

    return True


def x_is_valid_hash__mutmut_10(hash_value: str, algorithm: str | None = None) -> bool:
    """Check if a string is a valid hash value.

    Args:
        hash_value: String to check
        algorithm: Optional algorithm to validate length against

    Returns:
        True if string appears to be a valid hash

    """
    # Check if it's a valid hex string
    try:
        int(hash_value, 16)
    except ValueError:
        return False

    # If algorithm specified, check length
    if algorithm:
        from provide.foundation.crypto.algorithms import (
            get_digest_size,
            validate_algorithm,
        )

        try:
            validate_algorithm(algorithm)
            expected_length = get_digest_size(None) * 2  # hex is 2 chars per byte
            return len(hash_value) == expected_length
        except Exception:
            return False

    return True


def x_is_valid_hash__mutmut_11(hash_value: str, algorithm: str | None = None) -> bool:
    """Check if a string is a valid hash value.

    Args:
        hash_value: String to check
        algorithm: Optional algorithm to validate length against

    Returns:
        True if string appears to be a valid hash

    """
    # Check if it's a valid hex string
    try:
        int(hash_value, 16)
    except ValueError:
        return False

    # If algorithm specified, check length
    if algorithm:
        from provide.foundation.crypto.algorithms import (
            get_digest_size,
            validate_algorithm,
        )

        try:
            validate_algorithm(algorithm)
            expected_length = get_digest_size(algorithm) * 3  # hex is 2 chars per byte
            return len(hash_value) == expected_length
        except Exception:
            return False

    return True


def x_is_valid_hash__mutmut_12(hash_value: str, algorithm: str | None = None) -> bool:
    """Check if a string is a valid hash value.

    Args:
        hash_value: String to check
        algorithm: Optional algorithm to validate length against

    Returns:
        True if string appears to be a valid hash

    """
    # Check if it's a valid hex string
    try:
        int(hash_value, 16)
    except ValueError:
        return False

    # If algorithm specified, check length
    if algorithm:
        from provide.foundation.crypto.algorithms import (
            get_digest_size,
            validate_algorithm,
        )

        try:
            validate_algorithm(algorithm)
            expected_length = get_digest_size(algorithm) * 2  # hex is 2 chars per byte
            return len(hash_value) != expected_length
        except Exception:
            return False

    return True


def x_is_valid_hash__mutmut_13(hash_value: str, algorithm: str | None = None) -> bool:
    """Check if a string is a valid hash value.

    Args:
        hash_value: String to check
        algorithm: Optional algorithm to validate length against

    Returns:
        True if string appears to be a valid hash

    """
    # Check if it's a valid hex string
    try:
        int(hash_value, 16)
    except ValueError:
        return False

    # If algorithm specified, check length
    if algorithm:
        from provide.foundation.crypto.algorithms import (
            get_digest_size,
            validate_algorithm,
        )

        try:
            validate_algorithm(algorithm)
            expected_length = get_digest_size(algorithm) * 2  # hex is 2 chars per byte
            return len(hash_value) == expected_length
        except Exception:
            return True

    return True


def x_is_valid_hash__mutmut_14(hash_value: str, algorithm: str | None = None) -> bool:
    """Check if a string is a valid hash value.

    Args:
        hash_value: String to check
        algorithm: Optional algorithm to validate length against

    Returns:
        True if string appears to be a valid hash

    """
    # Check if it's a valid hex string
    try:
        int(hash_value, 16)
    except ValueError:
        return False

    # If algorithm specified, check length
    if algorithm:
        from provide.foundation.crypto.algorithms import (
            get_digest_size,
            validate_algorithm,
        )

        try:
            validate_algorithm(algorithm)
            expected_length = get_digest_size(algorithm) * 2  # hex is 2 chars per byte
            return len(hash_value) == expected_length
        except Exception:
            return False

    return False

x_is_valid_hash__mutmut_mutants : ClassVar[MutantDict] = {
'x_is_valid_hash__mutmut_1': x_is_valid_hash__mutmut_1, 
    'x_is_valid_hash__mutmut_2': x_is_valid_hash__mutmut_2, 
    'x_is_valid_hash__mutmut_3': x_is_valid_hash__mutmut_3, 
    'x_is_valid_hash__mutmut_4': x_is_valid_hash__mutmut_4, 
    'x_is_valid_hash__mutmut_5': x_is_valid_hash__mutmut_5, 
    'x_is_valid_hash__mutmut_6': x_is_valid_hash__mutmut_6, 
    'x_is_valid_hash__mutmut_7': x_is_valid_hash__mutmut_7, 
    'x_is_valid_hash__mutmut_8': x_is_valid_hash__mutmut_8, 
    'x_is_valid_hash__mutmut_9': x_is_valid_hash__mutmut_9, 
    'x_is_valid_hash__mutmut_10': x_is_valid_hash__mutmut_10, 
    'x_is_valid_hash__mutmut_11': x_is_valid_hash__mutmut_11, 
    'x_is_valid_hash__mutmut_12': x_is_valid_hash__mutmut_12, 
    'x_is_valid_hash__mutmut_13': x_is_valid_hash__mutmut_13, 
    'x_is_valid_hash__mutmut_14': x_is_valid_hash__mutmut_14
}

def is_valid_hash(*args, **kwargs):
    result = _mutmut_trampoline(x_is_valid_hash__mutmut_orig, x_is_valid_hash__mutmut_mutants, args, kwargs)
    return result 

is_valid_hash.__signature__ = _mutmut_signature(x_is_valid_hash__mutmut_orig)
x_is_valid_hash__mutmut_orig.__name__ = 'x_is_valid_hash'


# <3 🧱🤝🔒🪄
