#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for unified key generation."""

from __future__ import annotations

import time

from cryptography.hazmat.primitives.asymmetric import ec, rsa
from provide.testkit import FoundationTestCase
from provide.testkit.mocking import patch
import pytest

from provide.foundation.crypto import (
    Certificate,
    generate_ec_keypair,
    generate_keypair,
    generate_rsa_keypair,
)
from provide.foundation.crypto.keys import KeyGenerationError

# Constants for compatibility
KEY_TYPE_RSA = "rsa"
KEY_TYPE_ECDSA = "ec"  # Changed from "ecdsa" to "ec" to match implementation


class TestKeys(FoundationTestCase):
    """Test key generation functionality."""

    @pytest.mark.asyncio
    async def test_generate_keypair_returns_keypair(self) -> None:
        """Ensure generate_keypair() returns PEM bytes"""
        rsa_key_pair = generate_keypair(KEY_TYPE_RSA, key_size=2048)
        ec_key_pair = generate_keypair(KEY_TYPE_ECDSA, curve_name="secp256r1")

        # Check tuple and that they are bytes for RSA
        assert isinstance(rsa_key_pair, tuple)
        assert len(rsa_key_pair) == 2
        assert isinstance(rsa_key_pair[0], bytes)
        assert isinstance(rsa_key_pair[1], bytes)
        assert b"BEGIN PRIVATE KEY" in rsa_key_pair[0]
        assert b"BEGIN PUBLIC KEY" in rsa_key_pair[1]

        # Check tuple and that they are bytes for EC
        assert isinstance(ec_key_pair, tuple)
        assert len(ec_key_pair) == 2
        assert isinstance(ec_key_pair[0], bytes)
        assert isinstance(ec_key_pair[1], bytes)
        assert b"BEGIN PRIVATE KEY" in ec_key_pair[0]
        assert b"BEGIN PUBLIC KEY" in ec_key_pair[1]

    @pytest.mark.asyncio
    async def test_generate_keypair_invalid_type(self) -> None:
        """Ensure an error is raised when an invalid key type is provided."""
        with pytest.raises(KeyGenerationError, match="Unsupported key type"):
            generate_keypair("invalid_type")

    @pytest.mark.asyncio
    async def test_generate_rsa_keypair(self) -> None:
        """Test RSA keypair generation with a valid size."""
        private_key, public_key = generate_rsa_keypair(2048)
        assert isinstance(private_key, rsa.RSAPrivateKey)
        assert isinstance(public_key, rsa.RSAPublicKey)
        assert private_key.key_size == 2048

    @pytest.mark.asyncio
    async def test_generate_rsa_keypair_backend_failure(self) -> None:
        """Ensure RSA key generation fails if the cryptography backend encounters an issue."""
        with (
            patch(
                "cryptography.hazmat.primitives.asymmetric.rsa.generate_private_key",
                side_effect=Exception("Backend failure"),
            ),
            pytest.raises(Exception, match="Backend failure"),
        ):
            generate_rsa_keypair(2048)

    @pytest.mark.asyncio
    async def test_generate_invalid_rsa_key_size(self) -> None:
        """Test RSA key generation fails with an invalid key size."""
        with pytest.raises(KeyGenerationError, match="Unsupported RSA key size"):
            generate_rsa_keypair(key_size=1024)

    @pytest.mark.asyncio
    async def test_generate_ec_keypair(self) -> None:
        """Test ECDSA keypair generation with a valid curve."""
        private_key, public_key = generate_ec_keypair(curve_name="secp256r1")
        assert isinstance(private_key, ec.EllipticCurvePrivateKey)
        assert isinstance(public_key, ec.EllipticCurvePublicKey)
        assert private_key.curve.name == "secp256r1"

    @pytest.mark.asyncio
    async def test_generate_ec_keypair_invalid_curve(self) -> None:
        """Cover error path in generate_ec_keypair"""
        with pytest.raises(KeyGenerationError, match="Unsupported EC curve"):
            generate_ec_keypair("invalid_curve")

    @pytest.mark.asyncio
    async def test_generate_ec_keypair_backend_failure(self) -> None:
        """Ensure EC key generation fails if the cryptography backend encounters an issue."""
        with (
            patch(
                "cryptography.hazmat.primitives.asymmetric.ec.generate_private_key",
                side_effect=Exception("Backend failure"),
            ),
            pytest.raises(Exception, match="Backend failure"),
        ):
            generate_ec_keypair("secp256r1")

    @pytest.mark.asyncio
    async def test_generate_invalid_ec_curve(self) -> None:
        """Test ECDSA key generation fails with an invalid curve name."""
        with pytest.raises(KeyGenerationError, match="Unsupported EC curve"):
            generate_ec_keypair(curve_name="invalid_curve")

    @pytest.mark.asyncio
    async def test_generate_unsupported_key_type(self) -> None:
        """Test unsupported key type raises an error."""
        with pytest.raises(KeyGenerationError, match="Unsupported key type"):
            generate_keypair(key_type="unsupported_type")

    # long-running
    @pytest.mark.asyncio
    async def test_key_generation_performance(self) -> None:
        start_time = time.time()
        Certificate.generate(key_type=KEY_TYPE_RSA, key_size=2048)
        generation_time = time.time() - start_time
        assert generation_time < 1.0  # Should complete within 1 second


# 🧱🏗️🔚
