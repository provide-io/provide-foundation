"""Tests for digital signature operations (moved from flavorpack)."""

import pytest

from provide.foundation.crypto import (
    ED25519_PRIVATE_KEY_SIZE,
    ED25519_PUBLIC_KEY_SIZE,
    ED25519_SIGNATURE_SIZE,
    generate_ed25519_keypair,
    generate_signing_keypair,
    sign_data,
    verify_signature,
)


class TestEd25519KeyGeneration:
    """Test Ed25519 key generation (moved from flavorpack security tests)."""

    def test_key_strength(self):
        """Ensure keys meet minimum strength requirements."""
        private_key, public_key = generate_ed25519_keypair()

        # Ed25519 keys should be 32 bytes
        assert len(public_key) == ED25519_PUBLIC_KEY_SIZE
        assert len(private_key) == ED25519_PRIVATE_KEY_SIZE

    def test_generate_signing_keypair_alias(self):
        """Test generate_signing_keypair is an alias for Ed25519."""
        private_key, public_key = generate_signing_keypair()

        assert len(public_key) == ED25519_PUBLIC_KEY_SIZE
        assert len(private_key) == ED25519_PRIVATE_KEY_SIZE

    def test_random_seed_quality(self):
        """Ensure random seeds are cryptographically secure."""
        seeds = set()
        for _ in range(100):
            _, public_key = generate_ed25519_keypair()
            seeds.add(public_key)

        # All keys should be unique
        assert len(seeds) == 100, "Random seed generation is not secure"


class TestEd25519Signatures:
    """Test Ed25519 signature algorithm (moved from flavorpack security tests)."""

    def test_signature_algorithm(self):
        """Ensure proper signature algorithm is used."""
        # Generate keys
        private_key, public_key = generate_ed25519_keypair()

        # Create test data
        test_data = b"test data for signature"

        # Create signature
        signature = sign_data(test_data, private_key)

        # Verify signature size
        assert len(signature) == ED25519_SIGNATURE_SIZE

        # Verify signature
        is_valid = verify_signature(test_data, signature, public_key)
        assert is_valid, "Signature should be valid"

        # Test with wrong data
        wrong_data = b"different data"
        is_valid_wrong = verify_signature(wrong_data, signature, public_key)
        assert not is_valid_wrong, "Signature should be invalid for different data"

    def test_sign_invalid_private_key_size(self):
        """Test signing with invalid private key size."""
        invalid_key = b"too_short"
        data = b"test data"

        with pytest.raises(ValueError, match="Private key must be 32 bytes"):
            sign_data(data, invalid_key)

    def test_verify_invalid_signature_size(self):
        """Test verification with invalid signature size."""
        private_key, public_key = generate_ed25519_keypair()
        data = b"test message"
        invalid_signature = b"too_short"

        result = verify_signature(data, invalid_signature, public_key)

        assert result is False

    def test_verify_invalid_public_key_size(self):
        """Test verification with invalid public key size."""
        private_key, public_key = generate_ed25519_keypair()
        data = b"test message"

        signature = sign_data(data, private_key)
        invalid_public_key = b"invalid"

        result = verify_signature(data, signature, invalid_public_key)

        assert result is False
