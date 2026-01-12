#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for hashing operations."""

from __future__ import annotations

import hashlib
from io import BytesIO
from pathlib import Path

from provide.testkit import FoundationTestCase
import pytest

from provide.foundation.crypto import (
    hash_data,
    hash_file,
    hash_stream,
    hash_string,
)
from provide.foundation.crypto.hashing import hash_chunks, hash_file_multiple
from provide.foundation.errors.config import ValidationError
from provide.foundation.errors.resources import ResourceError


class TestHashFile(FoundationTestCase):
    """Test hash_file function."""

    def test_hash_file_sha256(self, tmp_path: Path) -> None:
        """Test hashing a file with SHA256."""
        test_file = tmp_path / "test.txt"
        test_content = b"Hello, World!"
        test_file.write_bytes(test_content)

        # Calculate expected hash
        expected = hashlib.sha256(test_content).hexdigest()

        # Hash the file
        result = hash_file(test_file)

        assert result == expected

    def test_hash_file_md5(self, tmp_path: Path) -> None:
        """Test hashing a file with MD5."""
        test_file = tmp_path / "test.txt"
        test_content = b"Test content"
        test_file.write_bytes(test_content)

        # Calculate expected hash
        expected = hashlib.md5(test_content).hexdigest()

        # Hash the file
        result = hash_file(test_file, algorithm="md5")

        assert result == expected

    def test_hash_file_missing(self, tmp_path: Path) -> None:
        """Test hashing a non-existent file."""
        missing_file = tmp_path / "missing.txt"

        with pytest.raises(ResourceError) as exc_info:
            hash_file(missing_file)

        assert "File not found" in str(exc_info.value)

    def test_hash_file_directory(self, tmp_path: Path) -> None:
        """Test hashing a directory (should fail)."""
        with pytest.raises(ResourceError) as exc_info:
            hash_file(tmp_path)

        assert "not a file" in str(exc_info.value)

    def test_hash_file_invalid_algorithm(self, tmp_path: Path) -> None:
        """Test hashing with invalid algorithm."""
        test_file = tmp_path / "test.txt"
        test_file.write_text("test")

        with pytest.raises(ValidationError) as exc_info:
            hash_file(test_file, algorithm="invalid")

        assert "Unsupported hash algorithm" in str(exc_info.value)

    def test_hash_large_file(self, tmp_path: Path) -> None:
        """Test hashing a large file with chunks."""
        test_file = tmp_path / "large.bin"

        # Create a 10MB file
        size = 10 * 1024 * 1024
        test_file.write_bytes(b"x" * size)

        # Hash with small chunk size
        result = hash_file(test_file, chunk_size=1024)

        # Verify it's a valid SHA256 hash
        assert len(result) == 64
        assert all(c in "0123456789abcdef" for c in result)


class TestHashData(FoundationTestCase):
    """Test hash_data function."""

    def test_hash_data_sha256(self) -> None:
        """Test hashing bytes with SHA256."""
        data = b"Hello, World!"
        expected = hashlib.sha256(data).hexdigest()

        result = hash_data(data)

        assert result == expected

    def test_hash_data_empty(self) -> None:
        """Test hashing empty data."""
        data = b""
        expected = hashlib.sha256(data).hexdigest()

        result = hash_data(data)

        assert result == expected

    def test_hash_data_sha512(self) -> None:
        """Test hashing with SHA512."""
        data = b"Test data"
        expected = hashlib.sha512(data).hexdigest()

        result = hash_data(data, algorithm="sha512")

        assert result == expected


class TestHashString(FoundationTestCase):
    """Test hash_string function."""

    def test_hash_string_default(self) -> None:
        """Test hashing a string with default encoding."""
        text = "Hello, World!"
        expected = hashlib.sha256(text.encode("utf-8")).hexdigest()

        result = hash_string(text)

        assert result == expected

    def test_hash_string_different_encoding(self) -> None:
        """Test hashing with different encoding."""
        text = "Hello, 世界"

        # UTF-8 encoding
        result_utf8 = hash_string(text, encoding="utf-8")
        expected_utf8 = hashlib.sha256(text.encode("utf-8")).hexdigest()
        assert result_utf8 == expected_utf8

        # UTF-16 encoding
        result_utf16 = hash_string(text, encoding="utf-16")
        expected_utf16 = hashlib.sha256(text.encode("utf-16")).hexdigest()
        assert result_utf16 == expected_utf16

        # Results should be different
        assert result_utf8 != result_utf16


class TestHashStream(FoundationTestCase):
    """Test hash_stream function."""

    def test_hash_stream_basic(self) -> None:
        """Test hashing a stream."""
        data = b"Stream data"
        stream = BytesIO(data)
        expected = hashlib.sha256(data).hexdigest()

        result = hash_stream(stream)

        assert result == expected

    def test_hash_stream_chunks(self) -> None:
        """Test hashing a stream with small chunks."""
        data = b"x" * 1000
        stream = BytesIO(data)
        expected = hashlib.sha256(data).hexdigest()

        result = hash_stream(stream, chunk_size=10)

        assert result == expected

    def test_hash_stream_empty(self) -> None:
        """Test hashing an empty stream."""
        stream = BytesIO(b"")
        expected = hashlib.sha256(b"").hexdigest()

        result = hash_stream(stream)

        assert result == expected


class TestHashFileMultiple(FoundationTestCase):
    """Test hash_file_multiple function."""

    def test_hash_file_multiple_algorithms(self, tmp_path: Path) -> None:
        """Test hashing a file with multiple algorithms."""
        test_file = tmp_path / "test.txt"
        test_content = b"Multi-hash test"
        test_file.write_bytes(test_content)

        algorithms = ["sha256", "md5", "sha1"]
        result = hash_file_multiple(test_file, algorithms)

        # Verify each hash
        assert result["sha256"] == hashlib.sha256(test_content).hexdigest()
        assert result["md5"] == hashlib.md5(test_content).hexdigest()
        assert result["sha1"] == hashlib.sha1(test_content).hexdigest()

    def test_hash_file_multiple_invalid_algorithm(self, tmp_path: Path) -> None:
        """Test with invalid algorithm in list."""
        test_file = tmp_path / "test.txt"
        test_file.write_text("test")

        with pytest.raises(ValidationError):
            hash_file_multiple(test_file, ["sha256", "invalid"])


class TestHashChunks(FoundationTestCase):
    """Test hash_chunks function."""

    def test_hash_chunks_basic(self) -> None:
        """Test hashing an iterator of chunks."""
        chunks = [b"Hello", b", ", b"World", b"!"]
        full_data = b"".join(chunks)
        expected = hashlib.sha256(full_data).hexdigest()

        result = hash_chunks(iter(chunks))

        assert result == expected

    def test_hash_chunks_empty(self) -> None:
        """Test hashing empty chunks."""
        chunks = []
        expected = hashlib.sha256(b"").hexdigest()

        result = hash_chunks(iter(chunks))

        assert result == expected

    def test_hash_chunks_single(self) -> None:
        """Test hashing a single chunk."""
        chunks = [b"Single chunk"]
        expected = hashlib.sha256(b"Single chunk").hexdigest()

        result = hash_chunks(iter(chunks))

        assert result == expected


# 🧱🏗️🔚
