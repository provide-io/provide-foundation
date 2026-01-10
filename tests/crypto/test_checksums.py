#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

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


# 🧱🏗️🔚
