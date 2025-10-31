#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from __future__ import annotations

import hashlib

"""Utility functions for hashing and cryptographic operations."""


def quick_hash(data: bytes) -> int:
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


def hash_name(name: str) -> int:
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


def compare_hash(hash1: str, hash2: str) -> bool:
    """Compare two hash values in a case-insensitive manner.

    Args:
        hash1: First hash value
        hash2: Second hash value

    Returns:
        True if hashes match (case-insensitive)

    """
    return hash1.lower() == hash2.lower()


def format_hash(
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


def truncate_hash(hash_value: str, length: int = 16, suffix: str = "...") -> str:
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


def hash_to_int(hash_value: str) -> int:
    """Convert a hex hash string to an integer.

    Args:
        hash_value: Hex hash string

    Returns:
        Integer representation of the hash

    """
    return int(hash_value, 16)


def int_to_hash(value: int, length: int | None = None) -> str:
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


def is_valid_hash(hash_value: str, algorithm: str | None = None) -> bool:
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


# 🧱🏗️🔚
