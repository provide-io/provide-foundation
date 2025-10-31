#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""RSA digital signature implementation.

RSA-PSS signatures with SHA-256 for compatibility with existing systems.
For new applications, prefer Ed25519 (faster, smaller keys, simpler).

Examples:
    >>> signer = RSASigner.generate(key_size=2048)
    >>> signature = signer.sign(b"message")
    >>> verifier = RSAVerifier(signer.public_key_pem)
    >>> assert verifier.verify(b"message", signature)"""

from __future__ import annotations

from functools import cached_property
from typing import TYPE_CHECKING, Self

from attrs import define, field

from provide.foundation import logger
from provide.foundation.crypto.defaults import DEFAULT_RSA_KEY_SIZE
from provide.foundation.errors.crypto import CryptoKeyError, CryptoSignatureError

if TYPE_CHECKING:
    from cryptography.hazmat.primitives import hashes, serialization
    from cryptography.hazmat.primitives.asymmetric import padding, rsa

try:
    from cryptography.hazmat.primitives import hashes, serialization
    from cryptography.hazmat.primitives.asymmetric import padding, rsa

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


@define(slots=True)
class RSASigner:
    """RSA digital signature signer.

    Stateful signer for RSA-PSS signatures. Use Ed25519Signer for new
    applications; RSA is provided for compatibility with existing systems.

    Examples:
        Generate new keypair:
            >>> signer = RSASigner.generate(key_size=2048)
            >>> signature = signer.sign(b"message")
            >>> public_pem = signer.public_key_pem

        Load existing key:
            >>> signer = RSASigner(private_key_pem=existing_pem)
            >>> signature = signer.sign(b"message")
    """

    private_key_pem: str | None = field(default=None, kw_only=True)
    key_size: int = field(default=DEFAULT_RSA_KEY_SIZE, kw_only=True)
    _private_key_obj: rsa.RSAPrivateKey = field(init=False, repr=False)

    @classmethod
    def generate(cls, key_size: int = DEFAULT_RSA_KEY_SIZE) -> Self:
        """Generate new signer with random RSA keypair.

        Args:
            key_size: RSA key size in bits (2048, 3072, or 4096)

        Returns:
            RSASigner: Signer with newly generated keypair
        """
        _require_crypto()
        logger.debug(f"🔐 Generating new RSA signer ({key_size} bits)")

        private_key_obj = rsa.generate_private_key(
            public_exponent=65537,
            key_size=key_size,
        )

        private_key_pem = private_key_obj.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption(),
        ).decode("utf-8")

        return cls(private_key_pem=private_key_pem, key_size=key_size)

    def __attrs_post_init__(self) -> None:
        """Initialize private key object from PEM."""
        _require_crypto()

        if self.private_key_pem is None:
            raise CryptoKeyError(
                "private_key_pem is required. Use RSASigner.generate() to create new keypair.",
                code="CRYPTO_MISSING_PRIVATE_KEY",
            )

        # Load private key from PEM
        object.__setattr__(
            self,
            "_private_key_obj",
            serialization.load_pem_private_key(
                self.private_key_pem.encode("utf-8"),
                password=None,
            ),
        )

        # Validate it's RSA
        if not isinstance(self._private_key_obj, rsa.RSAPrivateKey):
            raise CryptoKeyError(
                "Private key must be RSA",
                code="CRYPTO_INVALID_KEY_TYPE",
            )

    @cached_property
    def public_key_pem(self) -> str:
        """Get RSA public key in PEM format.

        Returns:
            str: PEM-encoded public key
        """
        public_key_bytes = self._private_key_obj.public_key().public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        )

        logger.debug(f"🔑 Derived RSA public key ({self.key_size} bits)")
        return public_key_bytes.decode("utf-8")

    def sign(self, data: bytes) -> bytes:
        """Sign data with RSA-PSS.

        Uses PSS padding with SHA-256 hash, which is the modern recommended
        RSA signature scheme.

        Args:
            data: Data to sign

        Returns:
            bytes: RSA-PSS signature

        Raises:
            CryptoSignatureError: If signature generation fails
        """
        logger.debug(f"🔏 Signing {len(data)} bytes with RSA-PSS")

        try:
            signature = self._private_key_obj.sign(
                data,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH,
                ),
                hashes.SHA256(),
            )

            return signature
        except Exception as e:
            raise CryptoSignatureError(
                f"RSA signature generation failed: {e}",
                code="CRYPTO_SIGNATURE_FAILED",
            ) from e

    def export_private_key_pem(self) -> str:
        """Export private key in PEM format.

        Returns:
            str: PEM-encoded private key

        Warning:
            Private keys should be stored securely. Consider encryption.
        """
        return self.private_key_pem  # type: ignore


@define(slots=True)
class RSAVerifier:
    """RSA signature verifier.

    Stateful verifier for RSA-PSS signatures.

    Examples:
        >>> signer = RSASigner.generate(key_size=2048)
        >>> verifier = RSAVerifier(signer.public_key_pem)
        >>> signature = signer.sign(b"message")
        >>> assert verifier.verify(b"message", signature)
    """

    public_key_pem: str = field()
    _public_key_obj: rsa.RSAPublicKey = field(init=False, repr=False)

    def __attrs_post_init__(self) -> None:
        """Initialize public key object from PEM."""
        _require_crypto()

        # Load public key from PEM
        object.__setattr__(
            self,
            "_public_key_obj",
            serialization.load_pem_public_key(self.public_key_pem.encode("utf-8")),
        )

        # Validate it's RSA
        if not isinstance(self._public_key_obj, rsa.RSAPublicKey):
            raise CryptoKeyError(
                "Public key must be RSA",
                code="CRYPTO_INVALID_KEY_TYPE",
            )

    def verify(self, data: bytes, signature: bytes) -> bool:
        """Verify RSA-PSS signature.

        Args:
            data: Data that was signed
            signature: RSA-PSS signature

        Returns:
            bool: True if signature is valid, False otherwise
        """
        logger.debug(f"🔍 Verifying RSA-PSS signature for {len(data)} bytes")

        try:
            self._public_key_obj.verify(
                signature,
                data,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH,
                ),
                hashes.SHA256(),
            )
            return True
        except Exception as e:
            logger.debug(f"❌ Invalid RSA-PSS signature: {e}")
            return False


__all__ = [
    "RSASigner",
    "RSAVerifier",
]

# 🧱🏗️🔚
