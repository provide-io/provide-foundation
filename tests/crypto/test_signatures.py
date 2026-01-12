#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for digital signature operations (moved from flavorpack)."""

from __future__ import annotations

from provide.testkit import FoundationTestCase
import pytest

from provide.foundation.crypto import (
    ED25519_PRIVATE_KEY_SIZE,
    ED25519_PUBLIC_KEY_SIZE,
    ED25519_SIGNATURE_SIZE,
    Ed25519Signer,
    Ed25519Verifier,
    generate_ed25519_keypair,
    generate_signing_keypair,
)
from provide.foundation.errors.crypto import CryptoKeyError


class TestEd25519KeyGeneration(FoundationTestCase):
    """Test Ed25519 key generation (moved from flavorpack security tests)."""

    def test_key_strength(self) -> None:
        """Ensure keys meet minimum strength requirements."""
        private_key, public_key = generate_ed25519_keypair()

        # Ed25519 keys should be 32 bytes
        assert len(public_key) == ED25519_PUBLIC_KEY_SIZE
        assert len(private_key) == ED25519_PRIVATE_KEY_SIZE

    def test_generate_signing_keypair_alias(self) -> None:
        """Test generate_signing_keypair is an alias for Ed25519."""
        private_key, public_key = generate_signing_keypair()

        assert len(public_key) == ED25519_PUBLIC_KEY_SIZE
        assert len(private_key) == ED25519_PRIVATE_KEY_SIZE

    def test_random_seed_quality(self) -> None:
        """Ensure random seeds are cryptographically secure."""
        seeds = set()
        for _ in range(100):
            _, public_key = generate_ed25519_keypair()
            seeds.add(public_key)

        # All keys should be unique
        assert len(seeds) == 100, "Random seed generation is not secure"


class TestEd25519Signatures(FoundationTestCase):
    """Test Ed25519 signature algorithm using OOP API."""

    def test_signature_algorithm(self) -> None:
        """Ensure proper signature algorithm is used."""
        # Generate signer
        signer = Ed25519Signer.generate()
        verifier = Ed25519Verifier(signer.public_key)

        # Create test data
        test_data = b"test data for signature"

        # Create signature
        signature = signer.sign(test_data)

        # Verify signature size
        assert len(signature) == ED25519_SIGNATURE_SIZE

        # Verify signature
        is_valid = verifier.verify(test_data, signature)
        assert is_valid, "Signature should be valid"

        # Test with wrong data
        wrong_data = b"different data"
        is_valid_wrong = verifier.verify(wrong_data, signature)
        assert not is_valid_wrong, "Signature should be invalid for different data"

    def test_sign_invalid_private_key_size(self) -> None:
        """Test signing with invalid private key size."""
        invalid_key = b"too_short"

        with pytest.raises(CryptoKeyError, match="private key must be 32 bytes"):
            Ed25519Signer(private_key=invalid_key)

    def test_verify_invalid_signature_size(self) -> None:
        """Test verification with invalid signature size."""
        signer = Ed25519Signer.generate()
        verifier = Ed25519Verifier(signer.public_key)
        data = b"test message"
        invalid_signature = b"too_short"

        result = verifier.verify(data, invalid_signature)

        assert result is False

    def test_verify_invalid_public_key_size(self) -> None:
        """Test verification with invalid public key size."""
        invalid_public_key = b"invalid"

        with pytest.raises(CryptoKeyError, match="public key must be 32 bytes"):
            Ed25519Verifier(invalid_public_key)


# 🧱🏗️🔚
