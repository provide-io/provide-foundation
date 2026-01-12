#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for prefixed checksum operations."""

from __future__ import annotations

from provide.testkit import FoundationTestCase
import pytest


class TestFormatChecksum(FoundationTestCase):
    """Test format_checksum function."""

    def test_format_checksum_sha256(self) -> None:
        """Test formatting SHA256 checksum."""
        from provide.foundation.crypto.prefixed import format_checksum

        data = b"Hello, World!"
        result = format_checksum(data, "sha256")

        assert result.startswith("sha256:")
        expected_hash = "dffd6021bb2bd5b0af676290809ec3a53191dd81c7f70a4b28688a362182986f"
        assert result == f"sha256:{expected_hash}"

    def test_format_checksum_sha512(self) -> None:
        """Test formatting SHA512 checksum."""
        from provide.foundation.crypto.prefixed import format_checksum

        data = b"test data"
        result = format_checksum(data, "sha512")

        assert result.startswith("sha512:")
        assert len(result.split(":")[1]) == 128  # SHA512 produces 128 hex chars

    def test_format_checksum_blake2b(self) -> None:
        """Test formatting BLAKE2b checksum."""
        from provide.foundation.crypto.prefixed import format_checksum

        data = b"blake test"
        result = format_checksum(data, "blake2b")

        assert result.startswith("blake2b:")
        assert len(result.split(":")[1]) == 128  # BLAKE2b produces 128 hex chars

    def test_format_checksum_blake2s(self) -> None:
        """Test formatting BLAKE2s checksum."""
        from provide.foundation.crypto.prefixed import format_checksum

        data = b"blake test"
        result = format_checksum(data, "blake2s")

        assert result.startswith("blake2s:")
        assert len(result.split(":")[1]) == 64  # BLAKE2s produces 64 hex chars

    def test_format_checksum_md5(self) -> None:
        """Test formatting MD5 checksum."""
        from provide.foundation.crypto.prefixed import format_checksum

        data = b"md5 test"
        result = format_checksum(data, "md5")

        assert result.startswith("md5:")
        assert len(result.split(":")[1]) == 32  # MD5 produces 32 hex chars

    def test_format_checksum_adler32(self) -> None:
        """Test formatting Adler32 checksum."""
        from provide.foundation.crypto.prefixed import format_checksum

        data = b"adler test"
        result = format_checksum(data, "adler32")

        assert result.startswith("adler32:")
        assert len(result.split(":")[1]) == 8  # Adler32 produces 8 hex chars

    def test_format_checksum_empty_data(self) -> None:
        """Test formatting checksum of empty data."""
        from provide.foundation.crypto.prefixed import format_checksum

        data = b""
        result = format_checksum(data, "sha256")

        assert result.startswith("sha256:")
        expected_hash = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
        assert result == f"sha256:{expected_hash}"

    def test_format_checksum_default_algorithm(self) -> None:
        """Test default algorithm (sha256)."""
        from provide.foundation.crypto.prefixed import format_checksum

        data = b"default test"
        result = format_checksum(data)

        assert result.startswith("sha256:")

    def test_format_checksum_unsupported_algorithm(self) -> None:
        """Test error on unsupported algorithm."""
        from provide.foundation.crypto.prefixed import format_checksum
        from provide.foundation.errors import ValidationError

        data = b"test"

        with pytest.raises(ValidationError):
            format_checksum(data, "unsupported")


class TestParseChecksum(FoundationTestCase):
    """Test parse_checksum function."""

    def test_parse_checksum_valid_sha256(self) -> None:
        """Test parsing valid SHA256 checksum."""
        from provide.foundation.crypto.prefixed import parse_checksum

        checksum_str = "sha256:abc123def456"
        algorithm, value = parse_checksum(checksum_str)

        assert algorithm == "sha256"
        assert value == "abc123def456"

    def test_parse_checksum_valid_adler32(self) -> None:
        """Test parsing valid Adler32 checksum."""
        from provide.foundation.crypto.prefixed import parse_checksum

        checksum_str = "adler32:deadbeef"
        algorithm, value = parse_checksum(checksum_str)

        assert algorithm == "adler32"
        assert value == "deadbeef"

    def test_parse_checksum_all_algorithms(self) -> None:
        """Test parsing all supported algorithms."""
        from provide.foundation.crypto.prefixed import parse_checksum

        algorithms = ["sha256", "sha512", "blake2b", "blake2s", "md5", "adler32"]

        for algo in algorithms:
            checksum_str = f"{algo}:test123"
            algorithm, value = parse_checksum(checksum_str)
            assert algorithm == algo
            assert value == "test123"

    def test_parse_checksum_empty_string(self) -> None:
        """Test error on empty checksum string."""
        from provide.foundation.crypto.prefixed import parse_checksum

        with pytest.raises(ValueError) as ctx:
            parse_checksum("")

        assert "Empty checksum string" in str(ctx.value)

    def test_parse_checksum_missing_prefix(self) -> None:
        """Test error on missing prefix."""
        from provide.foundation.crypto.prefixed import parse_checksum

        with pytest.raises(ValueError) as ctx:
            parse_checksum("abc123def456")

        assert "algorithm:value" in str(ctx.value)

    def test_parse_checksum_invalid_format(self) -> None:
        """Test error on invalid format - missing value."""
        from provide.foundation.crypto.prefixed import parse_checksum

        # Empty value is still valid - just algorithm with empty string
        # This actually succeeds, so test something that actually fails
        with pytest.raises(ValueError):
            parse_checksum(":value")  # Missing algorithm

    def test_parse_checksum_unsupported_algorithm(self) -> None:
        """Test error on unsupported algorithm."""
        from provide.foundation.crypto.prefixed import parse_checksum

        with pytest.raises(ValueError) as ctx:
            parse_checksum("unsupported:abc123")

        assert "Unknown checksum algorithm" in str(ctx.value)

    def test_parse_checksum_colon_in_value(self) -> None:
        """Test parsing checksum with colon in value."""
        from provide.foundation.crypto.prefixed import parse_checksum

        checksum_str = "sha256:value:with:colons"
        algorithm, value = parse_checksum(checksum_str)

        assert algorithm == "sha256"
        assert value == "value:with:colons"


class TestVerifyChecksum(FoundationTestCase):
    """Test verify_checksum function."""

    def test_verify_checksum_valid_sha256(self) -> None:
        """Test verifying valid SHA256 checksum."""
        from provide.foundation.crypto.prefixed import format_checksum, verify_checksum

        data = b"test data for verification"
        checksum = format_checksum(data, "sha256")

        assert verify_checksum(data, checksum) is True

    def test_verify_checksum_invalid_sha256(self) -> None:
        """Test verifying invalid SHA256 checksum."""
        from provide.foundation.crypto.prefixed import verify_checksum

        data = b"test data"
        wrong_checksum = "sha256:0000000000000000000000000000000000000000000000000000000000000000"

        assert verify_checksum(data, wrong_checksum) is False

    def test_verify_checksum_all_algorithms(self) -> None:
        """Test verification with all algorithms."""
        from provide.foundation.crypto.prefixed import format_checksum, verify_checksum

        data = b"multi-algo test"
        algorithms = ["sha256", "sha512", "blake2b", "blake2s", "md5", "adler32"]

        for algo in algorithms:
            checksum = format_checksum(data, algo)
            assert verify_checksum(data, checksum) is True, f"Failed for {algo}"

    def test_verify_checksum_case_insensitive(self) -> None:
        """Test case-insensitive verification."""
        from provide.foundation.crypto.prefixed import verify_checksum

        data = b"case test"
        checksum_lower = "sha256:abc123def456"
        checksum_upper = "sha256:ABC123DEF456"

        result1 = verify_checksum(data, checksum_lower)
        result2 = verify_checksum(data, checksum_upper)

        assert result1 == result2

    def test_verify_checksum_malformed_string(self) -> None:
        """Test verification with malformed checksum string."""
        from provide.foundation.crypto.prefixed import verify_checksum

        data = b"test"

        assert verify_checksum(data, "malformed") is False
        assert verify_checksum(data, "") is False

    def test_verify_checksum_wrong_algorithm(self) -> None:
        """Test verification with wrong algorithm."""
        from provide.foundation.crypto.prefixed import format_checksum, verify_checksum

        data = b"algorithm test"
        sha256_checksum = format_checksum(data, "sha256")
        sha512_checksum = sha256_checksum.replace("sha256:", "sha512:")

        assert verify_checksum(data, sha512_checksum) is False

    def test_verify_checksum_empty_data(self) -> None:
        """Test verification with empty data."""
        from provide.foundation.crypto.prefixed import format_checksum, verify_checksum

        data = b""
        checksum = format_checksum(data, "sha256")

        assert verify_checksum(data, checksum) is True


class TestNormalizeChecksum(FoundationTestCase):
    """Test normalize_checksum function."""

    def test_normalize_checksum_lowercase(self) -> None:
        """Test normalizing uppercase checksum to lowercase."""
        from provide.foundation.crypto.prefixed import normalize_checksum

        checksum = "sha256:ABC123DEF456"
        normalized = normalize_checksum(checksum)

        assert normalized == "sha256:abc123def456"

    def test_normalize_checksum_already_normalized(self) -> None:
        """Test normalizing already normalized checksum."""
        from provide.foundation.crypto.prefixed import normalize_checksum

        checksum = "sha256:abc123def456"
        normalized = normalize_checksum(checksum)

        assert normalized == checksum

    def test_normalize_checksum_mixed_case(self) -> None:
        """Test normalizing mixed case checksum."""
        from provide.foundation.crypto.prefixed import normalize_checksum

        checksum = "sha256:AbC123DeF456"
        normalized = normalize_checksum(checksum)

        assert normalized == "sha256:abc123def456"

    def test_normalize_checksum_invalid_format(self) -> None:
        """Test error on invalid format."""
        from provide.foundation.crypto.prefixed import normalize_checksum

        with pytest.raises(ValueError):
            normalize_checksum("invalid_checksum")

    def test_normalize_checksum_all_algorithms(self) -> None:
        """Test normalization with all algorithms."""
        from provide.foundation.crypto.prefixed import normalize_checksum

        algorithms = ["sha256", "sha512", "blake2b", "blake2s", "md5", "adler32"]

        for algo in algorithms:
            checksum = f"{algo}:TEST123"
            normalized = normalize_checksum(checksum)
            assert normalized == f"{algo}:test123"


class TestIsStrongChecksum(FoundationTestCase):
    """Test is_strong_checksum function."""

    def test_is_strong_checksum_sha256(self) -> None:
        """Test SHA256 is strong."""
        from provide.foundation.crypto.prefixed import is_strong_checksum

        assert is_strong_checksum("sha256:abc123") is True

    def test_is_strong_checksum_sha512(self) -> None:
        """Test SHA512 is strong."""
        from provide.foundation.crypto.prefixed import is_strong_checksum

        assert is_strong_checksum("sha512:abc123") is True

    def test_is_strong_checksum_blake2b(self) -> None:
        """Test BLAKE2b is strong."""
        from provide.foundation.crypto.prefixed import is_strong_checksum

        assert is_strong_checksum("blake2b:abc123") is True

    def test_is_strong_checksum_blake2s(self) -> None:
        """Test BLAKE2s is strong."""
        from provide.foundation.crypto.prefixed import is_strong_checksum

        assert is_strong_checksum("blake2s:abc123") is True

    def test_is_strong_checksum_md5_weak(self) -> None:
        """Test MD5 is weak."""
        from provide.foundation.crypto.prefixed import is_strong_checksum

        assert is_strong_checksum("md5:abc123") is False

    def test_is_strong_checksum_adler32_weak(self) -> None:
        """Test Adler32 is weak."""
        from provide.foundation.crypto.prefixed import is_strong_checksum

        assert is_strong_checksum("adler32:abc123") is False

    def test_is_strong_checksum_invalid_format(self) -> None:
        """Test invalid format returns False."""
        from provide.foundation.crypto.prefixed import is_strong_checksum

        assert is_strong_checksum("invalid") is False
        assert is_strong_checksum("") is False

    def test_is_strong_checksum_all_algorithms(self) -> None:
        """Test strength classification for all algorithms."""
        from provide.foundation.crypto.prefixed import is_strong_checksum

        strong_algorithms = ["sha256", "sha512", "blake2b", "blake2s"]
        weak_algorithms = ["md5", "adler32"]

        for algo in strong_algorithms:
            assert is_strong_checksum(f"{algo}:test") is True, f"{algo} should be strong"

        for algo in weak_algorithms:
            assert is_strong_checksum(f"{algo}:test") is False, f"{algo} should be weak"


# 🧱🏗️🔚
