from __future__ import annotations

from typing import TYPE_CHECKING

from provide.foundation import logger
from provide.foundation.crypto.constants import (
    ED25519_PRIVATE_KEY_SIZE,
    ED25519_PUBLIC_KEY_SIZE,
    ED25519_SIGNATURE_SIZE,
)

"""Digital signature operations using Ed25519."""

if TYPE_CHECKING:
    from cryptography.exceptions import InvalidSignature
    from cryptography.hazmat.primitives import serialization
    from cryptography.hazmat.primitives.asymmetric import ed25519

try:
    from cryptography.exceptions import InvalidSignature
    from cryptography.hazmat.primitives import serialization
    from cryptography.hazmat.primitives.asymmetric import ed25519

    _HAS_CRYPTO = True
except ImportError:
    _HAS_CRYPTO = False


def _require_crypto() -> None:
    """Ensure cryptography is available."""
    if not _HAS_CRYPTO:
        raise ImportError(
            "Cryptography features require optional dependencies. "
            "Install with: pip install 'provide-foundation[crypto]'",
        )


def generate_ed25519_keypair() -> tuple[bytes, bytes]:
    """Generate Ed25519 key pair for digital signatures.

    Returns:
        tuple: (private_key_bytes, public_key_bytes)
            - private_key_bytes: 32-byte Ed25519 private key seed
            - public_key_bytes: 32-byte Ed25519 public key

    """
    _require_crypto()
    logger.debug("🔐 Generating Ed25519 key pair")

    # Generate a new Ed25519 private key
    private_key = ed25519.Ed25519PrivateKey.generate()

    # Get the raw bytes for compatibility with other implementations
    private_key_bytes = private_key.private_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PrivateFormat.Raw,
        encryption_algorithm=serialization.NoEncryption(),
    )
    public_key_bytes = private_key.public_key().public_bytes(
        encoding=serialization.Encoding.Raw, format=serialization.PublicFormat.Raw
    )

    # Validate key sizes
    if len(private_key_bytes) != ED25519_PRIVATE_KEY_SIZE:
        raise ValueError(
            f"Invalid private key size: expected {ED25519_PRIVATE_KEY_SIZE} bytes, got {len(private_key_bytes)}"
        )
    if len(public_key_bytes) != ED25519_PUBLIC_KEY_SIZE:
        raise ValueError(
            f"Invalid public key size: expected {ED25519_PUBLIC_KEY_SIZE} bytes, got {len(public_key_bytes)}"
        )

    logger.debug(f"✅ Generated Ed25519 key pair (public: {len(public_key_bytes)} bytes)")
    return private_key_bytes, public_key_bytes


def sign_data(data: bytes, private_key: bytes) -> bytes:
    """Sign data with Ed25519 private key.

    Args:
        data: The data to sign
        private_key: 32-byte Ed25519 private key seed

    Returns:
        bytes: 64-byte Ed25519 signature

    Raises:
        ValueError: If private key is wrong size

    """
    _require_crypto()
    if len(private_key) != ED25519_PRIVATE_KEY_SIZE:
        raise ValueError(f"Private key must be {ED25519_PRIVATE_KEY_SIZE} bytes, got {len(private_key)}")

    logger.debug(f"🔏 Signing {len(data)} bytes of data with Ed25519")

    # Reconstruct the private key from the seed bytes
    private_key_obj = ed25519.Ed25519PrivateKey.from_private_bytes(private_key)

    # Sign the data
    signature = private_key_obj.sign(data)

    # Validate signature size
    if len(signature) != ED25519_SIGNATURE_SIZE:
        raise ValueError(
            f"Invalid signature size: expected {ED25519_SIGNATURE_SIZE} bytes, got {len(signature)}"
        )

    logger.debug(f"✅ Created Ed25519 signature ({len(signature)} bytes)")
    return signature


def verify_signature(data: bytes, signature: bytes, public_key: bytes) -> bool:
    """Verify Ed25519 signature.

    Args:
        data: The data that was signed
        signature: 64-byte Ed25519 signature
        public_key: 32-byte Ed25519 public key

    Returns:
        bool: True if signature is valid, False otherwise

    """
    _require_crypto()
    if len(signature) != ED25519_SIGNATURE_SIZE:
        logger.warning(f"❌ Invalid signature size: expected {ED25519_SIGNATURE_SIZE}, got {len(signature)}")
        return False

    if len(public_key) != ED25519_PUBLIC_KEY_SIZE:
        logger.warning(
            f"❌ Invalid public key size: expected {ED25519_PUBLIC_KEY_SIZE}, got {len(public_key)}",
        )
        return False

    logger.debug(f"🔍 Verifying Ed25519 signature for {len(data)} bytes of data")

    try:
        public_key_obj = ed25519.Ed25519PublicKey.from_public_bytes(public_key)
        public_key_obj.verify(signature, data)
        logger.debug("✅ Ed25519 signature verification successful")
        return True
    except InvalidSignature:
        logger.debug("❌ Invalid Ed25519 signature")
        return False
    except Exception as e:
        logger.error(f"❌ Ed25519 signature verification error: {e}")
        return False


# Convenience function for generating signing keypairs
def generate_signing_keypair() -> tuple[bytes, bytes]:
    """Generate Ed25519 keypair for signing (convenience function).

    This is an alias for generate_ed25519_keypair() that makes intent clear.

    Returns:
        tuple: (private_key_bytes, public_key_bytes)

    """
    _require_crypto()
    return generate_ed25519_keypair()
