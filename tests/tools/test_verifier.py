#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Comprehensive tests for tool verifier.

Tests all functionality in tools/verifier.py including checksum verification,
signature verification, and CLI commands."""

from __future__ import annotations

import base64
from pathlib import Path
import sys

from provide.testkit.mocking import Mock, patch
import pytest

from provide.foundation.crypto import Ed25519Signer
from provide.foundation.tools.verifier import (
    ToolVerifier,
    VerificationError,
    _get_data_from_file_or_stdin,
    verify_checksum_with_hash,
    verify_signature_with_key,
)


class TestVerificationError:
    """Tests for VerificationError exception."""

    def test_verification_error_inheritance(self) -> None:
        """Test that VerificationError inherits from FoundationError."""
        from provide.foundation.errors import FoundationError

        error = VerificationError("Test error")
        assert isinstance(error, FoundationError)


class TestToolVerifierInit:
    """Tests for ToolVerifier initialization."""

    def test_verifier_creation(self) -> None:
        """Test that ToolVerifier can be instantiated."""
        verifier = ToolVerifier()
        assert verifier is not None


class TestToolVerifierChecksum:
    """Tests for ToolVerifier.verify_checksum method."""

    def test_verify_checksum_match(self, tmp_path: Path) -> None:
        """Test checksum verification with matching hash."""
        verifier = ToolVerifier()

        file_path = tmp_path / "test.txt"
        file_path.write_text("test content")

        # SHA256 of "test content"
        expected = "sha256:6ae8a75555209fd6c44157c0aed8016e763ff435a19cf186f76863140143ff72"

        result = verifier.verify_checksum(file_path, expected)

        assert result is True

    def test_verify_checksum_match_without_algorithm_prefix(self, tmp_path: Path) -> None:
        """Test checksum without algorithm prefix defaults to sha256."""
        verifier = ToolVerifier()

        file_path = tmp_path / "test.txt"
        file_path.write_text("test content")

        # Hash without prefix should default to sha256
        expected = "6ae8a75555209fd6c44157c0aed8016e763ff435a19cf186f76863140143ff72"

        result = verifier.verify_checksum(file_path, expected)

        assert result is True

    def test_verify_checksum_mismatch(self, tmp_path: Path) -> None:
        """Test checksum verification with non-matching hash."""
        verifier = ToolVerifier()

        file_path = tmp_path / "test.txt"
        file_path.write_text("test content")

        expected = "sha256:0000000000000000000000000000000000000000000000000000000000000000"

        result = verifier.verify_checksum(file_path, expected)

        assert result is False

    def test_verify_checksum_file_not_found(self, tmp_path: Path) -> None:
        """Test that FileNotFoundError is raised for missing file."""
        verifier = ToolVerifier()

        file_path = tmp_path / "nonexistent.txt"
        expected = "sha256:abcd1234"

        with pytest.raises(FileNotFoundError, match="File not found"):
            verifier.verify_checksum(file_path, expected)

    def test_verify_checksum_different_algorithms(self, tmp_path: Path) -> None:
        """Test checksum with different hash algorithms."""
        verifier = ToolVerifier()

        file_path = tmp_path / "test.txt"
        file_path.write_text("test content")

        # SHA256
        sha256_hash = "sha256:6ae8a75555209fd6c44157c0aed8016e763ff435a19cf186f76863140143ff72"
        assert verifier.verify_checksum(file_path, sha256_hash) is True

        # SHA512 of "test content"
        sha512_hash = (
            "sha512:0cbf4caef38047bba9a24e621a961484e5d2a92176a859e7eb27df343dd34eb98d538a6c5f4da1ce"
            "302ec250b821cc001e46cc97a704988297185a4df7e99602"
        )
        assert verifier.verify_checksum(file_path, sha512_hash) is True


class TestGetDataFromFileOrStdin:
    """Tests for _get_data_from_file_or_stdin helper function."""

    def test_get_data_from_file(self, tmp_path: Path) -> None:
        """Test reading data from a file."""
        file_path = tmp_path / "test.txt"
        file_path.write_bytes(b"test content")

        data, error = _get_data_from_file_or_stdin(file_path)

        assert data == b"test content"
        assert error is None

    def test_get_data_from_stdin(self) -> None:
        """Test reading data from stdin."""
        mock_stdin = Mock()
        mock_stdin.buffer.read.return_value = b"stdin content"

        with patch.object(sys, "stdin", mock_stdin):
            data, error = _get_data_from_file_or_stdin(None)

            assert data == b"stdin content"
            assert error is None

    def test_get_data_file_error(self, tmp_path: Path) -> None:
        """Test error handling when file read fails."""
        file_path = tmp_path / "nonexistent.txt"

        data, error = _get_data_from_file_or_stdin(file_path)

        assert data is None
        assert error is not None


class TestVerifyChecksumWithHash:
    """Tests for verify_checksum_with_hash helper function."""

    def test_verify_checksum_with_hash_valid(self) -> None:
        """Test verification with valid checksum."""
        data = b"test content"
        expected_hash = "6ae8a75555209fd6c44157c0aed8016e763ff435a19cf186f76863140143ff72"

        result = verify_checksum_with_hash(data, expected_hash)

        assert result is True

    def test_verify_checksum_with_hash_explicit_algorithm(self) -> None:
        """Test verification with explicitly specified algorithm."""
        data = b"test content"
        expected_hash = "6ae8a75555209fd6c44157c0aed8016e763ff435a19cf186f76863140143ff72"

        result = verify_checksum_with_hash(data, expected_hash, algorithm="sha256")

        assert result is True

    def test_verify_checksum_with_hash_with_prefix(self) -> None:
        """Test verification when hash already has algorithm prefix."""
        data = b"test content"
        expected_hash = "sha256:6ae8a75555209fd6c44157c0aed8016e763ff435a19cf186f76863140143ff72"

        result = verify_checksum_with_hash(data, expected_hash)

        assert result is True

    def test_verify_checksum_with_hash_invalid(self) -> None:
        """Test verification with invalid checksum."""
        data = b"test content"
        expected_hash = "0000000000000000000000000000000000000000000000000000000000000000"

        result = verify_checksum_with_hash(data, expected_hash)

        assert result is False

    def test_verify_checksum_with_hash_raises_on_error(self) -> None:
        """Test that VerificationError is raised on exception."""
        data = b"test content"
        invalid_hash = "invalid-format"

        with pytest.raises(VerificationError, match="Checksum verification failed"):
            verify_checksum_with_hash(data, invalid_hash, algorithm="invalid")


class TestVerifySignatureWithKey:
    """Tests for verify_signature_with_key helper function."""

    def test_verify_signature_with_key_valid(self) -> None:
        """Test signature verification with valid signature."""
        # Generate a keypair
        signer = Ed25519Signer.generate()
        public_key = signer.public_key
        public_key_b64 = base64.b64encode(public_key).decode("ascii")

        # Sign some data
        data = b"test message"
        signature = signer.sign(data)
        signature_b64 = base64.b64encode(signature).decode("ascii")

        # Verify
        result = verify_signature_with_key(data, signature_b64, public_key_b64)

        assert result is True

    def test_verify_signature_with_key_invalid_signature(self) -> None:
        """Test signature verification with invalid signature."""
        signer = Ed25519Signer.generate()
        public_key_b64 = base64.b64encode(signer.public_key).decode("ascii")

        data = b"test message"
        # Create a wrong signature
        wrong_signature_b64 = base64.b64encode(b"\x00" * 64).decode("ascii")

        with pytest.raises(VerificationError, match="Signature verification failed"):
            verify_signature_with_key(data, wrong_signature_b64, public_key_b64)

    def test_verify_signature_with_key_wrong_public_key(self) -> None:
        """Test signature verification with wrong public key."""
        signer = Ed25519Signer.generate()
        other_signer = Ed25519Signer.generate()

        data = b"test message"
        signature = signer.sign(data)
        signature_b64 = base64.b64encode(signature).decode("ascii")

        # Use different public key
        wrong_key_b64 = base64.b64encode(other_signer.public_key).decode("ascii")

        with pytest.raises(VerificationError, match="Signature verification failed"):
            verify_signature_with_key(data, signature_b64, wrong_key_b64)

    def test_verify_signature_with_key_invalid_base64(self) -> None:
        """Test that invalid base64 encoding raises error."""
        data = b"test message"

        with pytest.raises(VerificationError, match="Signature verification failed"):
            verify_signature_with_key(data, "not-valid-base64!!!", "also-invalid!!!")


class TestVerifyChecksumCommand:
    """Tests for verify_checksum_command CLI command."""

    def test_verify_checksum_command_imports(self) -> None:
        """Test that CLI command can be imported."""
        from provide.foundation.tools.verifier import verify_checksum_command

        assert verify_checksum_command is not None

    @patch("provide.foundation.tools.verifier.pout")
    @patch("provide.foundation.tools.verifier._get_data_from_file_or_stdin")
    @patch("provide.foundation.tools.verifier.verify_checksum_with_hash")
    def test_verify_checksum_command_success(
        self,
        mock_verify: Mock,
        mock_get_data: Mock,
        mock_pout: Mock,
        tmp_path: Path,
    ) -> None:
        """Test checksum command with valid checksum."""
        from provide.foundation.tools.verifier import verify_checksum_command

        mock_get_data.return_value = (b"test content", None)
        mock_verify.return_value = True

        file_path = tmp_path / "test.txt"

        verify_checksum_command(
            hash="6ae8a75555209fd6c44157c0aed8016e763ff435a19cf186f76863140143ff72",
            file=file_path,
        )

        mock_pout.assert_called_once()
        assert "OK" in str(mock_pout.call_args)

    @patch("provide.foundation.tools.verifier.perr")
    @patch("provide.foundation.tools.verifier._get_data_from_file_or_stdin")
    def test_verify_checksum_command_read_error(
        self,
        mock_get_data: Mock,
        mock_perr: Mock,
        tmp_path: Path,
    ) -> None:
        """Test checksum command with read error."""
        from provide.foundation.tools.verifier import verify_checksum_command

        mock_get_data.return_value = (None, "File not found")

        file_path = tmp_path / "test.txt"

        verify_checksum_command(hash="abcd1234", file=file_path)

        mock_perr.assert_called_once()
        assert "Error reading input" in str(mock_perr.call_args)

    @patch("provide.foundation.tools.verifier.perr")
    @patch("provide.foundation.tools.verifier._get_data_from_file_or_stdin")
    @patch("provide.foundation.tools.verifier.verify_checksum_with_hash")
    def test_verify_checksum_command_mismatch(
        self,
        mock_verify: Mock,
        mock_get_data: Mock,
        mock_perr: Mock,
    ) -> None:
        """Test checksum command with mismatched checksum."""
        from provide.foundation.tools.verifier import verify_checksum_command

        mock_get_data.return_value = (b"test content", None)
        mock_verify.return_value = False

        verify_checksum_command(hash="wrong-hash")

        mock_perr.assert_called_once()
        assert "MISMATCH" in str(mock_perr.call_args)


class TestVerifySignatureCommand:
    """Tests for verify_signature_command CLI command."""

    def test_verify_signature_command_imports(self) -> None:
        """Test that CLI command can be imported."""
        from provide.foundation.tools.verifier import verify_signature_command

        assert verify_signature_command is not None

    @patch("provide.foundation.tools.verifier.pout")
    @patch("provide.foundation.tools.verifier._get_data_from_file_or_stdin")
    @patch("provide.foundation.tools.verifier.verify_signature_with_key")
    def test_verify_signature_command_success(
        self,
        mock_verify: Mock,
        mock_get_data: Mock,
        mock_pout: Mock,
        tmp_path: Path,
    ) -> None:
        """Test signature command with valid signature."""
        from provide.foundation.tools.verifier import verify_signature_command

        mock_get_data.return_value = (b"test message", None)
        mock_verify.return_value = True

        file_path = tmp_path / "test.txt"

        verify_signature_command(
            signature="fake-signature-base64",
            key="fake-key-base64",
            file=file_path,
        )

        mock_pout.assert_called_once()
        assert "VERIFIED" in str(mock_pout.call_args)

    @patch("provide.foundation.tools.verifier.perr")
    @patch("provide.foundation.tools.verifier._get_data_from_file_or_stdin")
    def test_verify_signature_command_read_error(
        self,
        mock_get_data: Mock,
        mock_perr: Mock,
    ) -> None:
        """Test signature command with read error."""
        from provide.foundation.tools.verifier import verify_signature_command

        mock_get_data.return_value = (None, "File not found")

        verify_signature_command(
            signature="fake-signature",
            key="fake-key",
        )

        mock_perr.assert_called_once()
        assert "Error reading input" in str(mock_perr.call_args)

    @patch("provide.foundation.tools.verifier.perr")
    @patch("provide.foundation.tools.verifier._get_data_from_file_or_stdin")
    @patch("provide.foundation.tools.verifier.verify_signature_with_key")
    def test_verify_signature_command_invalid(
        self,
        mock_verify: Mock,
        mock_get_data: Mock,
        mock_perr: Mock,
    ) -> None:
        """Test signature command with invalid signature."""
        from provide.foundation.tools.verifier import verify_signature_command

        mock_get_data.return_value = (b"test message", None)
        mock_verify.side_effect = VerificationError("Invalid signature")

        verify_signature_command(
            signature="wrong-signature",
            key="some-key",
        )

        mock_perr.assert_called_once()
        assert "INVALID" in str(mock_perr.call_args)


# 🧱🏗️🔚
