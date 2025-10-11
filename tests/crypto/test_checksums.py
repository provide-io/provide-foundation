"""Tests for checksum operations."""

from __future__ import annotations

from pathlib import Path

from provide.testkit import FoundationTestCase

from provide.foundation.crypto import (
    calculate_checksums,
    parse_checksum_file,
    verify_data,
    verify_file,
    write_checksum_file,
)
from provide.foundation.crypto.checksums import verify_checksum_file


class TestVerifyFile(FoundationTestCase):
    """Test verify_file function."""

    def test_verify_file_success(self, tmp_path: Path) -> None:
        """Test successful file verification."""
        test_file = tmp_path / "test.txt"
        test_file.write_text("Hello, World!")

        # Pre-calculated SHA256 hash of "Hello, World!"
        expected_hash = "dffd6021bb2bd5b0af676290809ec3a53191dd81c7f70a4b28688a362182986f"

        result = verify_file(test_file, expected_hash)

        assert result is True

    def test_verify_file_failure(self, tmp_path: Path) -> None:
        """Test failed file verification."""
        test_file = tmp_path / "test.txt"
        test_file.write_text("Hello, World!")

        wrong_hash = "0000000000000000000000000000000000000000000000000000000000000000"

        result = verify_file(test_file, wrong_hash)

        assert result is False

    def test_verify_file_case_insensitive(self, tmp_path: Path) -> None:
        """Test case-insensitive hash comparison."""
        test_file = tmp_path / "test.txt"
        test_file.write_text("test")

        # Pre-calculated SHA256 hash of "test"
        lower_hash = "9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08"
        upper_hash = "9F86D081884C7D659A2FEAA0C55AD015A3BF4F1B2B0B822CD15D6C15B0F00A08"

        assert verify_file(test_file, lower_hash) is True
        assert verify_file(test_file, upper_hash) is True

    def test_verify_file_missing(self, tmp_path: Path) -> None:
        """Test verifying a non-existent file."""
        missing_file = tmp_path / "missing.txt"
        some_hash = "abcd1234"

        result = verify_file(missing_file, some_hash)

        assert result is False


class TestVerifyData(FoundationTestCase):
    """Test verify_data function."""

    def test_verify_data_success(self) -> None:
        """Test successful data verification."""
        data = b"Test data"
        # Pre-calculated SHA256 hash
        expected_hash = "e27c8214be8b7cf5bccc7c08247e3cb0c1514a48ee1f63197fe4ef3ef51d7e6f"

        result = verify_data(data, expected_hash)

        assert result is True

    def test_verify_data_failure(self) -> None:
        """Test failed data verification."""
        data = b"Test data"
        wrong_hash = "0000000000000000000000000000000000000000000000000000000000000000"

        result = verify_data(data, wrong_hash)

        assert result is False

    def test_verify_data_md5(self) -> None:
        """Test verification with MD5."""
        data = b"MD5 test"
        # Pre-calculated MD5 hash
        expected_hash = "cc60dda980ccbf65540520703d91b27c"

        result = verify_data(data, expected_hash, algorithm="md5")

        assert result is True


class TestCalculateChecksums(FoundationTestCase):
    """Test calculate_checksums function."""

    def test_calculate_checksums_default(self, tmp_path: Path) -> None:
        """Test calculating default checksums (SHA256 and MD5)."""
        test_file = tmp_path / "test.txt"
        test_file.write_text("Checksum test")

        result = calculate_checksums(test_file)

        assert "sha256" in result
        assert "md5" in result
        assert len(result["sha256"]) == 64  # SHA256 is 64 hex chars
        assert len(result["md5"]) == 32  # MD5 is 32 hex chars

    def test_calculate_checksums_custom(self, tmp_path: Path) -> None:
        """Test calculating custom checksums."""
        test_file = tmp_path / "test.txt"
        test_file.write_text("Custom test")

        algorithms = ["sha1", "sha512", "blake2b"]
        result = calculate_checksums(test_file, algorithms)

        assert len(result) == 3
        assert "sha1" in result
        assert "sha512" in result
        assert "blake2b" in result


class TestChecksumFiles(FoundationTestCase):
    """Test checksum file operations."""

    def test_parse_checksum_file_sha256(self, tmp_path: Path) -> None:
        """Test parsing a SHA256 checksum file."""
        checksum_file = tmp_path / "SHA256SUMS"
        checksum_file.write_text(
            "abc123def456  file1.txt\n"
            "789abcdef012  *file2.bin\n"
            "# Comment line\n"
            "345678901234  subdir/file3.txt\n",
        )

        result = parse_checksum_file(checksum_file)

        assert len(result) == 3
        assert result["file1.txt"] == "abc123def456"
        assert result["file2.bin"] == "789abcdef012"
        assert result["subdir/file3.txt"] == "345678901234"

    def test_parse_checksum_file_empty(self, tmp_path: Path) -> None:
        """Test parsing an empty checksum file."""
        checksum_file = tmp_path / "empty.sum"
        checksum_file.write_text("")

        result = parse_checksum_file(checksum_file)

        assert result == {}

    def test_write_checksum_file(self, tmp_path: Path) -> None:
        """Test writing a checksum file."""
        checksums = {
            "file1.txt": "abc123",
            "file2.bin": "def456",
            "dir/file3.dat": "789012",
        }

        checksum_file = tmp_path / "checksums.txt"
        write_checksum_file(checksums, checksum_file, algorithm="sha256")

        # Read and verify
        content = checksum_file.read_text()
        assert "# SHA256 checksums" in content
        assert "abc123  *file1.txt" in content
        assert "def456  *file2.bin" in content
        assert "789012  *dir/file3.dat" in content

    def test_verify_checksum_file(self, tmp_path: Path) -> None:
        """Test verifying files from a checksum file."""
        # Create test files
        file1 = tmp_path / "file1.txt"
        file2 = tmp_path / "file2.txt"
        file1.write_text("content1")
        file2.write_text("content2")

        # Create checksum file with one correct and one wrong hash
        checksum_file = tmp_path / "checksums.sha256"
        checksum_file.write_text(
            # Correct hash for "content1"
            "d0b425e00e15a0d36b9b361f02bab63563aed6cb4665083905386c55d5b679fa  file1.txt\n"
            # Wrong hash for file2
            "0000000000000000000000000000000000000000000000000000000000000000  file2.txt\n",
        )

        verified, failed = verify_checksum_file(checksum_file, base_dir=tmp_path)

        assert len(verified) == 1
        assert "file1.txt" in verified
        assert len(failed) == 1
        assert "file2.txt" in failed

    def test_verify_checksum_file_stop_on_error(self, tmp_path: Path) -> None:
        """Test stopping verification on first error."""
        # Create test files
        file1 = tmp_path / "file1.txt"
        file2 = tmp_path / "file2.txt"
        file1.write_text("test")
        file2.write_text("test")

        # Create checksum file with wrong hashes
        checksum_file = tmp_path / "checksums.sha256"
        checksum_file.write_text(
            "0000000000000000000000000000000000000000000000000000000000000000  file1.txt\n"
            "0000000000000000000000000000000000000000000000000000000000000000  file2.txt\n",
        )

        verified, failed = verify_checksum_file(
            checksum_file,
            base_dir=tmp_path,
            stop_on_error=True,
        )

        assert len(verified) == 0
        assert len(failed) == 1  # Should stop after first failure


# =============================================================================
# Prefixed Checksum Tests
# =============================================================================


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
        # Adler32 produces 8 hex chars (32-bit value)
        assert len(result.split(":")[1]) == 8

    def test_format_checksum_empty_data(self) -> None:
        """Test formatting checksum of empty data."""
        from provide.foundation.crypto.prefixed import format_checksum

        data = b""
        result = format_checksum(data, "sha256")

        assert result.startswith("sha256:")
        # SHA256 of empty string
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

        data = b"test"

        with self.assertRaises(ValueError):
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

        with self.assertRaises(ValueError) as ctx:
            parse_checksum("")

        assert "Empty checksum string" in str(ctx.exception)

    def test_parse_checksum_missing_prefix(self) -> None:
        """Test error on missing prefix."""
        from provide.foundation.crypto.prefixed import parse_checksum

        with self.assertRaises(ValueError) as ctx:
            parse_checksum("abc123def456")

        assert "algorithm:value" in str(ctx.exception)

    def test_parse_checksum_invalid_format(self) -> None:
        """Test error on invalid format."""
        from provide.foundation.crypto.prefixed import parse_checksum

        with self.assertRaises(ValueError):
            parse_checksum("sha256:")  # Missing value

    def test_parse_checksum_unsupported_algorithm(self) -> None:
        """Test error on unsupported algorithm."""
        from provide.foundation.crypto.prefixed import parse_checksum

        with self.assertRaises(ValueError) as ctx:
            parse_checksum("unsupported:abc123")

        assert "Unknown checksum algorithm" in str(ctx.exception)

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

        # Both should fail (wrong data), but case shouldn't matter
        result1 = verify_checksum(data, checksum_lower)
        result2 = verify_checksum(data, checksum_upper)

        assert result1 == result2  # Same result regardless of case

    def test_verify_checksum_malformed_string(self) -> None:
        """Test verification with malformed checksum string."""
        from provide.foundation.crypto.prefixed import verify_checksum

        data = b"test"

        # Should return False, not raise exception
        assert verify_checksum(data, "malformed") is False
        assert verify_checksum(data, "") is False

    def test_verify_checksum_wrong_algorithm(self) -> None:
        """Test verification with wrong algorithm."""
        from provide.foundation.crypto.prefixed import format_checksum, verify_checksum

        data = b"algorithm test"
        sha256_checksum = format_checksum(data, "sha256")

        # Change algorithm prefix
        sha512_checksum = sha256_checksum.replace("sha256:", "sha512:")

        # Should fail because hash length/value doesn't match SHA512
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

        checksum = "SHA256:ABC123DEF456"
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

        with self.assertRaises(ValueError):
            normalize_checksum("invalid_checksum")

    def test_normalize_checksum_all_algorithms(self) -> None:
        """Test normalization with all algorithms."""
        from provide.foundation.crypto.prefixed import normalize_checksum

        algorithms = ["sha256", "sha512", "blake2b", "blake2s", "md5", "adler32"]

        for algo in algorithms:
            checksum = f"{algo.upper()}:TEST123"
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

        # Should return False, not raise exception
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
