#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Comprehensive tests for OOP digital signature API.

Tests Ed25519Signer/Verifier and RSASigner/Verifier classes with ~100% coverage."""

from __future__ import annotations

from provide.testkit import FoundationTestCase
import pytest

from provide.foundation.crypto import (
    DEFAULT_RSA_KEY_SIZE,
    ED25519_PRIVATE_KEY_SIZE,
    ED25519_PUBLIC_KEY_SIZE,
    ED25519_SIGNATURE_SIZE,
    Ed25519Signer,
    Ed25519Verifier,
    RSASigner,
    RSAVerifier,
)
from provide.foundation.errors.crypto import CryptoKeyError


class TestEd25519Signer(FoundationTestCase):
    """Test Ed25519Signer class."""

    def test_generate_creates_valid_signer(self) -> None:
        """Test that generate() creates a valid signer."""
        signer = Ed25519Signer.generate()

        assert signer is not None
        assert signer.private_key is not None
        assert len(signer.private_key) == ED25519_PRIVATE_KEY_SIZE

    def test_generate_creates_unique_signers(self) -> None:
        """Test that generate() creates unique signers."""
        signers = [Ed25519Signer.generate() for _ in range(10)]
        private_keys = {signer.private_key for signer in signers}

        # All keys should be unique
        assert len(private_keys) == 10

    def test_public_key_property(self) -> None:
        """Test public_key property returns correct size."""
        signer = Ed25519Signer.generate()
        public_key = signer.public_key

        assert len(public_key) == ED25519_PUBLIC_KEY_SIZE

    def test_public_key_is_cached(self) -> None:
        """Test that public_key is cached (same object returned)."""
        signer = Ed25519Signer.generate()

        # Access twice and ensure same object
        key1 = signer.public_key
        key2 = signer.public_key

        assert key1 is key2

    def test_sign_creates_valid_signature(self) -> None:
        """Test sign() creates valid Ed25519 signature."""
        signer = Ed25519Signer.generate()
        data = b"test message"

        signature = signer.sign(data)

        assert len(signature) == ED25519_SIGNATURE_SIZE

    def test_sign_different_data_different_signature(self) -> None:
        """Test signing different data produces different signatures."""
        signer = Ed25519Signer.generate()

        sig1 = signer.sign(b"message 1")
        sig2 = signer.sign(b"message 2")

        assert sig1 != sig2

    def test_sign_same_data_deterministic(self) -> None:
        """Test Ed25519 signatures are deterministic."""
        signer = Ed25519Signer.generate()
        data = b"test message"

        sig1 = signer.sign(data)
        sig2 = signer.sign(data)

        # Ed25519 is deterministic - same data = same signature
        assert sig1 == sig2

    def test_load_existing_key(self) -> None:
        """Test loading signer from existing private key."""
        # Generate and export key
        original_signer = Ed25519Signer.generate()
        private_key_bytes = original_signer.export_private_key()

        # Load from exported key
        loaded_signer = Ed25519Signer(private_key=private_key_bytes)

        # Should produce same public key
        assert loaded_signer.public_key == original_signer.public_key

    def test_export_private_key(self) -> None:
        """Test export_private_key returns correct key."""
        signer = Ed25519Signer.generate()

        exported = signer.export_private_key()

        assert exported == signer.private_key
        assert len(exported) == ED25519_PRIVATE_KEY_SIZE

    def test_missing_private_key_raises_error(self) -> None:
        """Test that missing private key raises CryptoKeyError."""
        with pytest.raises(
            CryptoKeyError,
            match=r"private_key is required\. Use Ed25519Signer\.generate",
        ):
            Ed25519Signer(private_key=None)

    def test_invalid_private_key_size_raises_error(self) -> None:
        """Test invalid private key size raises CryptoKeyError."""
        invalid_key = b"too_short"

        with pytest.raises(
            CryptoKeyError,
            match=f"Ed25519 private key must be {ED25519_PRIVATE_KEY_SIZE} bytes",
        ):
            Ed25519Signer(private_key=invalid_key)


class TestEd25519Verifier(FoundationTestCase):
    """Test Ed25519Verifier class."""

    def test_verify_valid_signature(self) -> None:
        """Test verifying valid signature returns True."""
        signer = Ed25519Signer.generate()
        verifier = Ed25519Verifier(signer.public_key)
        data = b"test message"

        signature = signer.sign(data)
        result = verifier.verify(data, signature)

        assert result is True

    def test_verify_invalid_signature_returns_false(self) -> None:
        """Test verifying invalid signature returns False."""
        signer = Ed25519Signer.generate()
        verifier = Ed25519Verifier(signer.public_key)
        data = b"test message"

        # Create signature then corrupt it
        signature = bytearray(signer.sign(data))
        signature[0] ^= 0xFF  # Flip bits

        result = verifier.verify(data, bytes(signature))

        assert result is False

    def test_verify_wrong_data_returns_false(self) -> None:
        """Test verifying with wrong data returns False."""
        signer = Ed25519Signer.generate()
        verifier = Ed25519Verifier(signer.public_key)

        signature = signer.sign(b"original message")
        result = verifier.verify(b"different message", signature)

        assert result is False

    def test_verify_wrong_public_key_returns_false(self) -> None:
        """Test verifying with wrong public key returns False."""
        signer1 = Ed25519Signer.generate()
        signer2 = Ed25519Signer.generate()
        verifier = Ed25519Verifier(signer2.public_key)  # Wrong key

        data = b"test message"
        signature = signer1.sign(data)
        result = verifier.verify(data, signature)

        assert result is False

    def test_verify_invalid_signature_size(self) -> None:
        """Test verifying signature with wrong size returns False."""
        signer = Ed25519Signer.generate()
        verifier = Ed25519Verifier(signer.public_key)
        data = b"test message"

        invalid_signature = b"too_short"
        result = verifier.verify(data, invalid_signature)

        assert result is False

    def test_invalid_public_key_size_raises_error(self) -> None:
        """Test invalid public key size raises CryptoKeyError."""
        invalid_key = b"too_short"

        with pytest.raises(
            CryptoKeyError,
            match=f"Ed25519 public key must be {ED25519_PUBLIC_KEY_SIZE} bytes",
        ):
            Ed25519Verifier(invalid_key)


class TestRSASigner(FoundationTestCase):
    """Test RSASigner class."""

    def test_generate_creates_valid_signer(self) -> None:
        """Test that generate() creates a valid RSA signer."""
        signer = RSASigner.generate(key_size=2048)

        assert signer is not None
        assert signer.private_key_pem is not None
        assert "BEGIN PRIVATE KEY" in signer.private_key_pem
        assert signer.key_size == 2048

    def test_generate_default_key_size(self) -> None:
        """Test generate() uses default key size when not specified."""
        signer = RSASigner.generate()

        assert signer.key_size == DEFAULT_RSA_KEY_SIZE

    def test_generate_different_key_sizes(self) -> None:
        """Test generating RSA keys with different sizes."""
        sizes = [2048, 3072, 4096]

        for size in sizes:
            signer = RSASigner.generate(key_size=size)
            assert signer.key_size == size

    def test_public_key_pem_property(self) -> None:
        """Test public_key_pem property returns PEM format."""
        signer = RSASigner.generate(key_size=2048)
        public_pem = signer.public_key_pem

        assert "BEGIN PUBLIC KEY" in public_pem
        assert "END PUBLIC KEY" in public_pem

    def test_public_key_pem_is_cached(self) -> None:
        """Test that public_key_pem is cached."""
        signer = RSASigner.generate(key_size=2048)

        key1 = signer.public_key_pem
        key2 = signer.public_key_pem

        assert key1 is key2

    def test_sign_creates_valid_signature(self) -> None:
        """Test sign() creates RSA-PSS signature."""
        signer = RSASigner.generate(key_size=2048)
        data = b"test message"

        signature = signer.sign(data)

        # RSA-PSS signature size varies but should be reasonable
        assert len(signature) > 0
        assert isinstance(signature, bytes)

    def test_sign_different_data_different_signature(self) -> None:
        """Test signing different data produces different signatures."""
        signer = RSASigner.generate(key_size=2048)

        sig1 = signer.sign(b"message 1")
        sig2 = signer.sign(b"message 2")

        assert sig1 != sig2

    def test_sign_same_data_nondeterministic(self) -> None:
        """Test RSA-PSS signatures are non-deterministic (random salt)."""
        signer = RSASigner.generate(key_size=2048)
        data = b"test message"

        sig1 = signer.sign(data)
        sig2 = signer.sign(data)

        # RSA-PSS uses random salt - same data = different signature
        assert sig1 != sig2

    def test_load_existing_key(self) -> None:
        """Test loading signer from existing PEM private key."""
        # Generate and export key
        original_signer = RSASigner.generate(key_size=2048)
        private_pem = original_signer.export_private_key_pem()

        # Load from exported key
        loaded_signer = RSASigner(private_key_pem=private_pem, key_size=2048)

        # Should produce same public key
        assert loaded_signer.public_key_pem == original_signer.public_key_pem

    def test_export_private_key_pem(self) -> None:
        """Test export_private_key_pem returns correct PEM."""
        signer = RSASigner.generate(key_size=2048)

        exported = signer.export_private_key_pem()

        assert exported == signer.private_key_pem
        assert "BEGIN PRIVATE KEY" in exported

    def test_missing_private_key_raises_error(self) -> None:
        """Test that missing private key raises CryptoKeyError."""
        with pytest.raises(
            CryptoKeyError,
            match=r"private_key_pem is required\. Use RSASigner\.generate",
        ):
            RSASigner(private_key_pem=None)

    def test_invalid_key_type_raises_error(self) -> None:
        """Test that non-RSA private key raises CryptoKeyError."""
        # Generate Ed25519 key and try to use as RSA (will fail)
        from provide.foundation.crypto import generate_ed25519_keypair

        ed_private, _ = generate_ed25519_keypair()

        # Try to create RSA signer with Ed25519 key bytes
        # This should fail during PEM loading
        with pytest.raises((ValueError, TypeError)):  # Will fail at load_pem_private_key
            RSASigner(private_key_pem=ed_private.hex())


class TestRSAVerifier(FoundationTestCase):
    """Test RSAVerifier class."""

    def test_verify_valid_signature(self) -> None:
        """Test verifying valid RSA-PSS signature returns True."""
        signer = RSASigner.generate(key_size=2048)
        verifier = RSAVerifier(signer.public_key_pem)
        data = b"test message"

        signature = signer.sign(data)
        result = verifier.verify(data, signature)

        assert result is True

    def test_verify_invalid_signature_returns_false(self) -> None:
        """Test verifying invalid signature returns False."""
        signer = RSASigner.generate(key_size=2048)
        verifier = RSAVerifier(signer.public_key_pem)
        data = b"test message"

        # Create signature then corrupt it
        signature = bytearray(signer.sign(data))
        signature[0] ^= 0xFF  # Flip bits

        result = verifier.verify(data, bytes(signature))

        assert result is False

    def test_verify_wrong_data_returns_false(self) -> None:
        """Test verifying with wrong data returns False."""
        signer = RSASigner.generate(key_size=2048)
        verifier = RSAVerifier(signer.public_key_pem)

        signature = signer.sign(b"original message")
        result = verifier.verify(b"different message", signature)

        assert result is False

    def test_verify_wrong_public_key_returns_false(self) -> None:
        """Test verifying with wrong public key returns False."""
        signer1 = RSASigner.generate(key_size=2048)
        signer2 = RSASigner.generate(key_size=2048)
        verifier = RSAVerifier(signer2.public_key_pem)  # Wrong key

        data = b"test message"
        signature = signer1.sign(data)
        result = verifier.verify(data, signature)

        assert result is False

    def test_invalid_public_key_raises_error(self) -> None:
        """Test invalid public key PEM raises CryptoKeyError."""
        invalid_pem = "not a valid PEM"

        with pytest.raises(ValueError):  # Will fail at load_pem_public_key
            RSAVerifier(invalid_pem)


class TestSignerVerifierIntegration(FoundationTestCase):
    """Integration tests for signer/verifier workflows."""

    def test_ed25519_round_trip(self) -> None:
        """Test complete Ed25519 sign/verify workflow."""
        # Generate signer
        signer = Ed25519Signer.generate()

        # Create verifier from signer's public key
        verifier = Ed25519Verifier(signer.public_key)

        # Sign multiple messages
        messages = [b"message 1", b"message 2", b"message 3"]
        for msg in messages:
            signature = signer.sign(msg)
            assert verifier.verify(msg, signature)

    def test_rsa_round_trip(self) -> None:
        """Test complete RSA sign/verify workflow."""
        # Generate signer
        signer = RSASigner.generate(key_size=2048)

        # Create verifier from signer's public key
        verifier = RSAVerifier(signer.public_key_pem)

        # Sign multiple messages
        messages = [b"message 1", b"message 2", b"message 3"]
        for msg in messages:
            signature = signer.sign(msg)
            assert verifier.verify(msg, signature)

    def test_ed25519_key_export_import(self) -> None:
        """Test exporting and importing Ed25519 keys."""
        # Generate original signer
        original = Ed25519Signer.generate()
        private_key_bytes = original.export_private_key()

        # Create new signer from exported key
        imported = Ed25519Signer(private_key=private_key_bytes)

        # Should produce identical signatures (Ed25519 is deterministic)
        data = b"test message"
        assert imported.sign(data) == original.sign(data)

    def test_rsa_key_export_import(self) -> None:
        """Test exporting and importing RSA keys."""
        # Generate original signer
        original = RSASigner.generate(key_size=2048)
        private_pem = original.export_private_key_pem()

        # Create new signer from exported key
        imported = RSASigner(private_key_pem=private_pem, key_size=2048)

        # Should produce same public key
        assert imported.public_key_pem == original.public_key_pem

        # Signatures should verify with each other
        verifier = RSAVerifier(imported.public_key_pem)
        data = b"test message"
        signature = original.sign(data)
        assert verifier.verify(data, signature)

    def test_ed25519_vs_rsa_not_compatible(self) -> None:
        """Test that Ed25519 and RSA signatures are not interchangeable."""
        ed_signer = Ed25519Signer.generate()
        rsa_signer = RSASigner.generate(key_size=2048)

        data = b"test message"

        # Create signatures with both
        ed_signature = ed_signer.sign(data)
        rsa_signature = rsa_signer.sign(data)

        # Ed25519 signature won't verify with RSA
        # (This will fail at verification level, not raise)
        rsa_verifier = RSAVerifier(rsa_signer.public_key_pem)
        assert not rsa_verifier.verify(data, ed_signature)

        # RSA signature won't verify with Ed25519
        ed_verifier = Ed25519Verifier(ed_signer.public_key)
        assert not ed_verifier.verify(data, rsa_signature)


# 🧱🏗️🔚
