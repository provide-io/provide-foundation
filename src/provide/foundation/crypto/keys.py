#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Key generation utilities for Foundation.

Provides functions for generating cryptographic key pairs for various
algorithms and use cases, including TLS and digital signatures."""

from __future__ import annotations

from typing import TYPE_CHECKING, Literal

from provide.foundation.crypto.deps import (
    DEFAULT_ECDSA_CURVE,
    DEFAULT_RSA_KEY_SIZE,
    SUPPORTED_EC_CURVES,
    SUPPORTED_KEY_TYPES,
    SUPPORTED_RSA_SIZES,
    Ed25519Signer,
    KeyType,
)
from provide.foundation.errors import FoundationError

if TYPE_CHECKING:
    from cryptography.hazmat.primitives.asymmetric import ec, rsa

    KeypairTuple = tuple[bytes, bytes]


class KeyGenerationError(FoundationError):
    """Raised when key generation fails."""


def generate_rsa_keypair(
    key_size: int = DEFAULT_RSA_KEY_SIZE,
) -> tuple[rsa.RSAPrivateKey, rsa.RSAPublicKey]:
    """Generate an RSA key pair.

    Args:
        key_size: Key size in bits (2048, 3072, or 4096)

    Returns:
        Tuple of (private_key, public_key)

    Raises:
        KeyGenerationError: If key size is unsupported
    """
    from cryptography.hazmat.backends import default_backend
    from cryptography.hazmat.primitives.asymmetric import rsa

    if key_size not in SUPPORTED_RSA_SIZES:
        raise KeyGenerationError(
            f"Unsupported RSA key size: {key_size}. Must be one of {SUPPORTED_RSA_SIZES}",
            context={"key_size": key_size, "supported_sizes": SUPPORTED_RSA_SIZES},
        )
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=key_size,
        backend=default_backend(),
    )
    return private_key, private_key.public_key()


def generate_ec_keypair(
    curve_name: str = DEFAULT_ECDSA_CURVE,
) -> tuple[ec.EllipticCurvePrivateKey, ec.EllipticCurvePublicKey]:
    """Generate an Elliptic Curve (EC) key pair.

    Args:
        curve_name: Name of the curve (e.g., 'secp256r1')

    Returns:
        Tuple of (private_key, public_key)

    Raises:
        KeyGenerationError: If curve is unsupported
    """
    from cryptography.hazmat.backends import default_backend
    from cryptography.hazmat.primitives.asymmetric import ec

    if curve_name not in SUPPORTED_EC_CURVES:
        raise KeyGenerationError(
            f"Unsupported EC curve: {curve_name}. Must be one of {SUPPORTED_EC_CURVES}",
            context={"curve_name": curve_name, "supported_curves": SUPPORTED_EC_CURVES},
        )

    # Map curve name to cryptography curve object
    curve_obj = getattr(ec, curve_name.upper())()
    private_key = ec.generate_private_key(curve_obj, backend=default_backend())
    return private_key, private_key.public_key()


def generate_ed25519_keypair() -> KeypairTuple:
    """Generate an Ed25519 key pair.

    This is a wrapper around the modern Ed25519Signer class to provide
    raw key bytes for compatibility with legacy systems or specific protocols.

    Returns:
        A tuple containing (private_key_bytes, public_key_bytes).
    """
    signer = Ed25519Signer.generate()
    return signer.export_private_key(), signer.public_key


def generate_keypair(
    key_type: KeyType,
    key_size: int | None = None,
    curve_name: str | None = None,
) -> tuple[bytes, bytes]:
    """Generate a key pair and return serialized keys.

    Args:
        key_type: Type of key ('rsa' or 'ec')
        key_size: RSA key size (for 'rsa' type)
        curve_name: EC curve name (for 'ec' type)

    Returns:
        Tuple of (private_key_pem, public_key_pem)

    Raises:
        KeyGenerationError: If key type is unsupported
    """
    from cryptography.hazmat.primitives import serialization

    if key_type == "rsa":
        priv, pub = generate_rsa_keypair(key_size or DEFAULT_RSA_KEY_SIZE)
    elif key_type == "ec":
        priv, pub = generate_ec_keypair(curve_name or DEFAULT_ECDSA_CURVE)  # type: ignore[assignment]
    else:
        raise KeyGenerationError(
            f"Unsupported key type: {key_type}. Must be one of {SUPPORTED_KEY_TYPES}",
            context={"key_type": key_type, "supported_types": SUPPORTED_KEY_TYPES},
        )

    private_pem = priv.private_bytes(  # type: ignore[attr-defined]
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )
    public_pem = pub.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )
    return private_pem, public_pem


def generate_signing_keypair() -> KeypairTuple:
    """Generate a key pair suitable for digital signatures (Ed25519).

    This is an alias for `generate_ed25519_keypair`.

    Returns:
        A tuple containing (private_key_bytes, public_key_bytes).
    """
    return generate_ed25519_keypair()


def generate_tls_keypair(
    key_type: Literal["rsa", "ec"] = "ec",
) -> tuple[bytes, bytes]:
    """Generate a key pair suitable for TLS.

    Args:
        key_type: Type of key ('rsa' or 'ec')

    Returns:
        Tuple of (private_key_pem, public_key_pem)
    """
    return generate_keypair(key_type)


__all__ = [
    "KeyGenerationError",
    "generate_ec_keypair",
    "generate_ed25519_keypair",
    "generate_keypair",
    "generate_rsa_keypair",
    "generate_signing_keypair",
    "generate_tls_keypair",
]

# 🧱🏗️🔚
