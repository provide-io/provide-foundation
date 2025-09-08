"""
Test-driven development tests for ToolVerifier.

Tests for verifying checksums and signatures of downloaded tools.
"""

from pathlib import Path
from unittest.mock import MagicMock, Mock, patch

import pytest

from provide.foundation.tools.verifier import ToolVerifier, VerificationError


class TestToolVerifier:
    """Tests for ToolVerifier class."""
    
    @pytest.fixture
    def verifier(self):
        """Create a ToolVerifier instance."""
        return ToolVerifier()
    
    @pytest.fixture
    def test_file(self, tmp_path):
        """Create a test file with known content."""
        file_path = tmp_path / "test.txt"
        file_path.write_text("test content")
        return file_path
    
    def test_verify_checksum_sha256(self, verifier, test_file):
        """Test SHA256 checksum verification."""
        # SHA256 of "test content"
        expected = "1eebdf4fdc9fc7bf283031b93f9aef3338de9052fde2e59e7563e6aec5c2e290"
        
        assert verifier.verify_checksum(test_file, expected) is True
        assert verifier.verify_checksum(test_file, expected, algo="sha256") is True
        assert verifier.verify_checksum(test_file, "wrong") is False
    
    def test_verify_checksum_sha512(self, verifier, test_file):
        """Test SHA512 checksum verification."""
        # SHA512 of "test content"
        expected = ("7f100b68f4c27d63e82c00ccfafae87021a1a768c583d0f6b42e19286a35e6eb"
                   "c96f3e7b3c8e604ad837e1e62abb3477e8e3a0e7fa3f18e0417e5e2ea1dc98a9")
        
        assert verifier.verify_checksum(test_file, expected, algo="sha512") is True
        assert verifier.verify_checksum(test_file, "wrong", algo="sha512") is False
    
    def test_verify_checksum_md5(self, verifier, test_file):
        """Test MD5 checksum verification."""
        # MD5 of "test content"
        expected = "9d432f0e2607a95f151fa09d26e9f982"
        
        assert verifier.verify_checksum(test_file, expected, algo="md5") is True
        assert verifier.verify_checksum(test_file, "wrong", algo="md5") is False
    
    def test_verify_checksum_blake2b(self, verifier, test_file):
        """Test BLAKE2b checksum verification."""
        # BLAKE2b of "test content"
        expected = ("77a00b8ccdd8c82cf008b5e388c7a357d97c15fe88c088bbeb949ad5c8373e7b"
                   "6e97bb887c3fc59f34e1cc948ca7e024e3f03c93c0e8bf6d3bb8df96e93f0064")
        
        assert verifier.verify_checksum(test_file, expected, algo="blake2b") is True
        assert verifier.verify_checksum(test_file, "wrong", algo="blake2b") is False
    
    def test_verify_checksum_invalid_algo(self, verifier, test_file):
        """Test checksum verification with invalid algorithm."""
        with pytest.raises(ValueError, match="Unsupported hash algorithm"):
            verifier.verify_checksum(test_file, "checksum", algo="invalid")
    
    def test_verify_checksum_nonexistent_file(self, verifier, tmp_path):
        """Test checksum verification with non-existent file."""
        nonexistent = tmp_path / "nonexistent.txt"
        
        with pytest.raises(FileNotFoundError):
            verifier.verify_checksum(nonexistent, "checksum")
    
    def test_verify_checksum_large_file(self, verifier, tmp_path):
        """Test checksum verification with large file (chunked reading)."""
        large_file = tmp_path / "large.bin"
        # Create a 10MB file
        content = b"x" * (10 * 1024 * 1024)
        large_file.write_bytes(content)
        
        # SHA256 of 10MB of 'x'
        expected = "52f5fcafee165dff82421a96187bddb31e32797c6f829a0ad3fb7c625f083279"
        
        assert verifier.verify_checksum(large_file, expected) is True
    
    def test_verify_shasums_file(self, verifier, tmp_path):
        """Test verification using a shasums file."""
        # Create test files
        file1 = tmp_path / "file1.txt"
        file2 = tmp_path / "file2.txt"
        file1.write_text("content1")
        file2.write_text("content2")
        
        # Create shasums file
        shasums = tmp_path / "SHA256SUMS"
        shasums.write_text(
            "7e532e16e41907ffd664331e1f89677b7a2e0c0bc8ed8e87b385bf373f75d2b8  file1.txt\n"
            "c3a1e953f5e04b25c86ff5e4258e295f6e63b6cd8f13b973f87a15b95df8f47c  file2.txt\n"
        )
        
        assert verifier.verify_shasums_file(shasums, file1) is True
        assert verifier.verify_shasums_file(shasums, file2) is True
    
    def test_verify_shasums_file_not_found(self, verifier, tmp_path):
        """Test shasums verification when file not in list."""
        file_path = tmp_path / "notlisted.txt"
        file_path.write_text("content")
        
        shasums = tmp_path / "SHA256SUMS"
        shasums.write_text("abc123  other.txt\n")
        
        assert verifier.verify_shasums_file(shasums, file_path) is False
    
    def test_verify_shasums_file_mismatch(self, verifier, tmp_path):
        """Test shasums verification with wrong checksum."""
        file_path = tmp_path / "file.txt"
        file_path.write_text("actual content")
        
        shasums = tmp_path / "SHA256SUMS"
        shasums.write_text("wrongchecksum  file.txt\n")
        
        assert verifier.verify_shasums_file(shasums, file_path) is False
    
    @patch("provide.foundation.crypto.verify_signature")
    def test_verify_signature_success(self, mock_verify_sig, verifier, test_file):
        """Test signature verification success."""
        mock_verify_sig.return_value = True
        
        result = verifier.verify_signature(
            test_file,
            "signature_data",
            "public_key"
        )
        
        assert result is True
        mock_verify_sig.assert_called_once_with(
            test_file,
            "signature_data",
            "public_key"
        )
    
    @patch("provide.foundation.crypto.verify_signature")
    def test_verify_signature_failure(self, mock_verify_sig, verifier, test_file):
        """Test signature verification failure."""
        mock_verify_sig.return_value = False
        
        result = verifier.verify_signature(
            test_file,
            "bad_signature",
            "public_key"
        )
        
        assert result is False
    
    @patch("provide.foundation.crypto.verify_signature")
    def test_verify_signature_no_public_key(self, mock_verify_sig, verifier, test_file):
        """Test signature verification without public key."""
        mock_verify_sig.return_value = True
        
        result = verifier.verify_signature(test_file, "signature")
        
        assert result is True
        mock_verify_sig.assert_called_once_with(
            test_file,
            "signature",
            None
        )
    
    def test_extract_checksum_from_string(self, verifier):
        """Test extracting checksum from various string formats."""
        # Just the checksum
        assert verifier.extract_checksum("abc123") == "abc123"
        
        # Checksum with filename (common format)
        assert verifier.extract_checksum("abc123  filename.tar.gz") == "abc123"
        assert verifier.extract_checksum("def456 *binary.exe") == "def456"
        
        # With algorithm prefix
        assert verifier.extract_checksum("sha256:abc123") == "abc123"
        assert verifier.extract_checksum("SHA256:def456") == "def456"
        
        # Complex format
        line = "1234567890abcdef  path/to/file.tar.gz"
        assert verifier.extract_checksum(line) == "1234567890abcdef"