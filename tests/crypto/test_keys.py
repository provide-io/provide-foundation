"""Tests for unified key generation."""

import pytest

from unittest import mock

import time

from cryptography.hazmat.primitives.asymmetric import rsa, ec

from provide.foundation.crypto import (
    Certificate,
    generate_rsa_keypair,
    generate_ec_keypair,
    generate_keypair,
)

# Constants for compatibility
KEY_TYPE_RSA = "rsa"
KEY_TYPE_ECDSA = "ecdsa"


@pytest.mark.asyncio
async def test_generate_keypair_returns_keypair() -> None:
    """Ensure generate_keypair() returns correct type"""
    rsa_key_pair = generate_keypair(KEY_TYPE_RSA, key_size=2048)  # Added key_size
    ec_key_pair = generate_keypair(
        KEY_TYPE_ECDSA, curve="secp256r1"
    )  # Added curve for consistency

    # Check tuple and key types for RSA
    assert isinstance(rsa_key_pair, tuple)
    assert len(rsa_key_pair) == 2
    assert isinstance(rsa_key_pair[0], rsa.RSAPublicKey)
    assert isinstance(rsa_key_pair[1], rsa.RSAPrivateKey)

    # Check tuple and key types for ECDSA
    assert isinstance(ec_key_pair, tuple)
    assert len(ec_key_pair) == 2
    assert isinstance(ec_key_pair[0], ec.EllipticCurvePublicKey)
    assert isinstance(ec_key_pair[1], ec.EllipticCurvePrivateKey)


@pytest.mark.asyncio
async def test_generate_keypair_invalid_type() -> None:
    """Ensure an error is raised when an invalid key type is provided."""
    with pytest.raises(ValueError, match="Unsupported key type"):
        generate_keypair("invalid_type")


@pytest.mark.asyncio
async def test_generate_rsa_keypair() -> None:
    """Test RSA keypair generation with a valid size."""
    public_key, private_key = generate_rsa_keypair(2048)
    assert isinstance(public_key, rsa.RSAPublicKey)
    assert isinstance(private_key, rsa.RSAPrivateKey)
    assert private_key.key_size == 2048


@pytest.mark.asyncio
async def test_generate_rsa_keypair_backend_failure() -> None:
    """Ensure RSA key generation fails if the cryptography backend encounters an issue."""
    with mock.patch(
        "cryptography.hazmat.primitives.asymmetric.rsa.generate_private_key",
        side_effect=Exception("Backend failure"),
    ):
        with pytest.raises(Exception, match="Backend failure"):
            generate_rsa_keypair(2048)


@pytest.mark.asyncio
async def test_generate_invalid_rsa_key_size() -> None:
    """Test RSA key generation fails with an invalid key size."""
    with pytest.raises(ValueError, match="Unsupported RSA key size"):
        generate_keypair(key_type=KEY_TYPE_RSA, key_size=1024)


@pytest.mark.asyncio
async def test_generate_ec_keypair() -> None:
    """Test ECDSA keypair generation with a valid curve."""
    public_key, private_key = generate_keypair(
        key_type=KEY_TYPE_ECDSA, curve="secp256r1"
    )
    assert isinstance(public_key, ec.EllipticCurvePublicKey)
    assert isinstance(private_key, ec.EllipticCurvePrivateKey)
    assert private_key.curve.name == "secp256r1"


@pytest.mark.asyncio
async def test_generate_ec_keypair_invalid_curve() -> None:
    """Cover error path in generate_ec_keypair"""
    with pytest.raises(
        ValueError, match="Unsupported EC curve"
    ):  # Changed expected exception and added match
        generate_ec_keypair("invalid_curve")


@pytest.mark.asyncio
async def test_generate_ec_keypair_backend_failure() -> None:
    """Ensure EC key generation fails if the cryptography backend encounters an issue."""
    with mock.patch(
        "cryptography.hazmat.primitives.asymmetric.ec.generate_private_key",
        side_effect=Exception("Backend failure"),
    ):
        with pytest.raises(Exception, match="Backend failure"):
            generate_ec_keypair("secp256r1")


@pytest.mark.asyncio
async def test_generate_invalid_ec_curve() -> None:
    """Test ECDSA key generation fails with an invalid curve name."""
    with pytest.raises(ValueError, match="Unsupported EC curve"):
        generate_keypair(key_type=KEY_TYPE_ECDSA, curve="invalid_curve")


@pytest.mark.asyncio
async def test_generate_unsupported_key_type() -> None:
    """Test unsupported key type raises an error."""
    with pytest.raises(ValueError, match="Unsupported key type"):
        generate_keypair(key_type="unsupported_type")


# long-running
@pytest.mark.asyncio
async def test_key_generation_performance() -> None:
    start_time = time.time()
    Certificate(generate_keypair=True, key_type=KEY_TYPE_RSA, key_size=2048)
    generation_time = time.time() - start_time
    assert generation_time < 1.0  # Should complete within 1 second


### 🐍🏗🧪️


# 🐍🔌🧪🪄
