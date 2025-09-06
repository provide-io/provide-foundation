"""Unified key generation for all cryptographic algorithms."""

from typing import Any, Protocol, Union

from cryptography.hazmat.primitives.asymmetric import ec, rsa

from provide.foundation import logger
from provide.foundation.crypto.constants import (
    DEFAULT_ECDSA_CURVE,
    DEFAULT_RSA_KEY_SIZE,
    SUPPORTED_EC_CURVES,
    SUPPORTED_KEY_TYPES,
    SUPPORTED_RSA_SIZES,
)
from provide.foundation.crypto.signatures import generate_ed25519_keypair


class KeyPair(Protocol):
    """Protocol for key pairs."""

    def public_key(self) -> Any:
        """Get public key."""
        ...


# Type aliases for different key types
RSAKeyPair = tuple[rsa.RSAPublicKey, rsa.RSAPrivateKey]
ECKeyPair = tuple[ec.EllipticCurvePublicKey, ec.EllipticCurvePrivateKey]
Ed25519KeyPair = tuple[bytes, bytes]

KeyPairType = Union[RSAKeyPair, ECKeyPair, Ed25519KeyPair]


def generate_rsa_keypair(key_size: int = DEFAULT_RSA_KEY_SIZE) -> RSAKeyPair:
    """Generate RSA key pair.

    Args:
        key_size: RSA key size in bits (2048, 3072, or 4096)

    Returns:
        tuple: (public_key, private_key)

    Raises:
        ValueError: If key size is not supported
    """
    if key_size not in SUPPORTED_RSA_SIZES:
        raise ValueError(
            f"Unsupported RSA key size: {key_size}. "
            f"Supported sizes: {sorted(SUPPORTED_RSA_SIZES)}"
        )

    logger.debug(f"🔑 Generating RSA key pair (size: {key_size})")

    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=key_size,
    )
    public_key = private_key.public_key()

    logger.debug(f"✅ Generated RSA key pair ({key_size} bits)")
    return public_key, private_key


def generate_ec_keypair(curve: str = DEFAULT_ECDSA_CURVE) -> ECKeyPair:
    """Generate ECDSA key pair.

    Args:
        curve: Elliptic curve name (secp256r1, secp384r1, or secp521r1)

    Returns:
        tuple: (public_key, private_key)

    Raises:
        ValueError: If curve is not supported
        AttributeError: If curve name is invalid
    """
    if curve not in SUPPORTED_EC_CURVES:
        raise ValueError(
            f"Unsupported EC curve: {curve}. "
            f"Supported curves: {sorted(SUPPORTED_EC_CURVES)}"
        )

    logger.debug(f"🔑 Generating ECDSA key pair (curve: {curve})")

    # Map curve name to cryptography curve object
    curve_obj = getattr(ec, curve.upper())()

    private_key = ec.generate_private_key(curve_obj)
    public_key = private_key.public_key()

    logger.debug(f"✅ Generated ECDSA key pair ({curve})")
    return public_key, private_key


def generate_keypair(
    key_type: str,
    key_size: int | None = None,
    curve: str | None = None,
) -> KeyPairType:
    """Generate a key pair of the specified type.

    Args:
        key_type: Type of key to generate ("rsa", "ecdsa", or "ed25519")
        key_size: Key size in bits (required for RSA)
        curve: Curve name (required for ECDSA)

    Returns:
        KeyPair: Generated key pair

    Raises:
        ValueError: If key_type is not supported or required params missing
    """
    key_type_lower = key_type.lower()

    if key_type_lower not in SUPPORTED_KEY_TYPES:
        raise ValueError(
            f"Unsupported key type: {key_type}. "
            f"Supported types: {sorted(SUPPORTED_KEY_TYPES)}"
        )

    match key_type_lower:
        case "rsa":
            if key_size is None:
                key_size = DEFAULT_RSA_KEY_SIZE
                logger.debug(f"🔑 Using default RSA key size: {key_size}")
            return generate_rsa_keypair(key_size)

        case "ecdsa":
            if curve is None:
                curve = DEFAULT_ECDSA_CURVE
                logger.debug(f"🔑 Using default ECDSA curve: {curve}")
            return generate_ec_keypair(curve)

        case "ed25519":
            # Ed25519 has fixed parameters
            if key_size is not None or curve is not None:
                logger.warning(
                    "🔑 Ed25519 has fixed parameters - ignoring key_size/curve"
                )
            return generate_ed25519_keypair()

        case _:
            # This shouldn't happen due to the check above
            raise ValueError(f"Internal error: unhandled key type {key_type}")


# Convenience functions for specific use cases
def generate_signing_keypair() -> Ed25519KeyPair:
    """Generate Ed25519 keypair for digital signatures.

    This is the recommended choice for new digital signature use cases.

    Returns:
        tuple: (private_key_bytes, public_key_bytes)
    """
    return generate_ed25519_keypair()


def generate_tls_keypair(
    key_type: str = "ecdsa",
    curve: str = DEFAULT_ECDSA_CURVE,
) -> ECKeyPair | RSAKeyPair:
    """Generate keypair suitable for TLS/certificates.

    Args:
        key_type: Either "ecdsa" (recommended) or "rsa"
        curve: ECDSA curve (only used if key_type is "ecdsa")

    Returns:
        KeyPair: Generated key pair
    """
    if key_type == "ecdsa":
        return generate_ec_keypair(curve)
    elif key_type == "rsa":
        return generate_rsa_keypair(DEFAULT_RSA_KEY_SIZE)
    else:
        raise ValueError(f"TLS key type must be 'ecdsa' or 'rsa', got {key_type}")


# Legacy compatibility functions (for smooth migration)
def generate_key_pair() -> Ed25519KeyPair:
    """Legacy compatibility function.

    This maintains compatibility with existing flavorpack code.
    New code should use generate_signing_keypair() or generate_keypair().
    """
    logger.debug("🔑 Using legacy generate_key_pair() function")
    return generate_ed25519_keypair()
