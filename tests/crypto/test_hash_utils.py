#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for crypto hash utilities."""

from __future__ import annotations

from provide.testkit import FoundationTestCase

from provide.foundation.crypto.utils import (
    compare_hash,
    format_hash,
    hash_name,
    hash_to_int,
    int_to_hash,
    is_valid_hash,
    quick_hash,
    truncate_hash,
)


class TestHashUtils(FoundationTestCase):
    """Test hash utility functions."""

    def test_quick_hash(self) -> None:
        """Test quick hash generation."""
        hash1 = quick_hash(b"test")
        hash2 = quick_hash(b"test")
        hash3 = quick_hash(b"different")

        # Same input should give same hash
        assert hash1 == hash2
        # Different input should give different hash
        assert hash1 != hash3
        # Should be 32-bit value
        assert 0 <= hash1 <= 0xFFFFFFFF

    def test_hash_name(self) -> None:
        """Test name hashing."""
        hash1 = hash_name("test")
        hash2 = hash_name("test")
        hash3 = hash_name("different")

        assert hash1 == hash2
        assert hash1 != hash3
        # Should be 64-bit value
        assert 0 <= hash1 <= 0xFFFFFFFFFFFFFFFF

    def test_compare_hash(self) -> None:
        """Test hash comparison."""
        assert compare_hash("ABC123", "abc123") is True
        assert compare_hash("ABC123", "ABC123") is True
        assert compare_hash("abc123", "def456") is False

    def test_format_hash(self) -> None:
        """Test hash formatting."""
        hash_val = "abc123def456"

        # Default formatting
        formatted = format_hash(hash_val)
        assert formatted == "abc123de f456"

        # Custom group size and separator
        formatted = format_hash(hash_val, group_size=4, separator="-")
        assert formatted == "abc1-23de-f456"

        # Limited groups
        formatted = format_hash(hash_val, group_size=4, groups=2)
        assert formatted == "abc1 23de"

        # No grouping
        formatted = format_hash(hash_val, group_size=0)
        assert formatted == hash_val

    def test_truncate_hash(self) -> None:
        """Test hash truncation."""
        hash_val = "abc123def456789"

        # Default truncation
        truncated = truncate_hash(hash_val)
        assert truncated == "abc123def456789"  # Not truncated if <= length

        # With truncation
        truncated = truncate_hash(hash_val, length=8)
        assert truncated == "abc123de..."

        # Custom suffix
        truncated = truncate_hash(hash_val, length=8, suffix="[...]")
        assert truncated == "abc123de[...]"

        # No truncation needed
        truncated = truncate_hash("short", length=10)
        assert truncated == "short"

    def test_hash_to_int(self) -> None:
        """Test hash to integer conversion."""
        assert hash_to_int("ff") == 255
        assert hash_to_int("100") == 256
        assert hash_to_int("abc123") == 0xABC123

    def test_int_to_hash(self) -> None:
        """Test integer to hash conversion."""
        assert int_to_hash(255) == "ff"
        assert int_to_hash(256) == "100"
        assert int_to_hash(0xABC123) == "abc123"

        # With padding
        assert int_to_hash(15, length=4) == "000f"
        assert int_to_hash(255, length=6) == "0000ff"

    def test_is_valid_hash(self) -> None:
        """Test hash validation."""
        # Valid hex strings
        assert is_valid_hash("abc123") is True
        assert is_valid_hash("0123456789abcdef") is True
        assert is_valid_hash("ABCDEF") is True

        # Invalid hex strings
        assert is_valid_hash("xyz") is False
        assert is_valid_hash("12g3") is False
        assert is_valid_hash("") is False

        # With algorithm validation
        sha256_hash = "a" * 64  # SHA256 is 64 hex chars
        assert is_valid_hash(sha256_hash, "sha256") is True
        assert is_valid_hash("a" * 32, "sha256") is False  # Wrong length

        # Invalid algorithm
        assert is_valid_hash("abc", "invalid_algo") is False


# 🧱🏗️🔚
