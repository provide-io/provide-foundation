"""Object-oriented digital signature API for Ed25519 and RSA.

Provides stateful Signer and Verifier classes as an alternative to the
functional signature API. Supports both Ed25519 (modern, fast) and RSA
(widely compatible) algorithms.

Examples:
    Ed25519 (recommended for new applications):
        >>> signer = Ed25519Signer.generate()
        >>> signature = signer.sign(b"message")
        >>> verifier = Ed25519Verifier(signer.public_key)
        >>> assert verifier.verify(b"message", signature)

    RSA (for compatibility):
        >>> signer = RSASigner.generate(key_size=2048)
        >>> signature = signer.sign(b"message")
        >>> verifier = RSAVerifier(signer.public_key_pem)
        >>> assert verifier.verify(b"message", signature)
"""

from __future__ import annotations

from functools import cached_property
from typing import TYPE_CHECKING, Self

from attrs import define, field

from provide.foundation import logger
from provide.foundation.crypto.constants import (
    DEFAULT_RSA_KEY_SIZE,
    ED25519_PRIVATE_KEY_SIZE,
    ED25519_PUBLIC_KEY_SIZE,
    ED25519_SIGNATURE_SIZE,
)
from provide.foundation.errors.crypto import CryptoKeyError, CryptoSignatureError

if TYPE_CHECKING:
    from cryptography.hazmat.primitives import hashes, serialization
    from cryptography.hazmat.primitives.asymmetric import ed25519, padding, rsa

try:
    from cryptography.hazmat.primitives import hashes, serialization
    from cryptography.hazmat.primitives.asymmetric import ed25519, padding, rsa

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


# =============================================================================
# Ed25519 (Modern, Recommended)
# =============================================================================


@define(slots=True)
class Ed25519Signer:
    """Ed25519 digital signature signer.

    Stateful signer that holds private key and provides signing operations.
    Ed25519 is the recommended choice for new applications: fast, small keys,
    deterministic signatures.

    Examples:
        Generate new keypair:
            >>> signer = Ed25519Signer.generate()
            >>> signature = signer.sign(b"message")
            >>> public_key = signer.public_key

        Load existing key:
            >>> signer = Ed25519Signer(private_key=existing_32_byte_seed)
            >>> signature = signer.sign(b"message")
    """

    private_key: bytes | None = field(default=None, kw_only=True)
    _private_key_obj: ed25519.Ed25519PrivateKey = field(init=False, repr=False)

    @classmethod
    def generate(cls) -> Self:
        """Generate new signer with random Ed25519 keypair.

        Returns:
            Ed25519Signer: Signer with newly generated keypair
        """
        _require_crypto()
        logger.debug("🔐 Generating new Ed25519 signer")

        private_key_obj = ed25519.Ed25519PrivateKey.generate()
        private_key_bytes = private_key_obj.private_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PrivateFormat.Raw,
            encryption_algorithm=serialization.NoEncryption(),
        )

        return cls(private_key=private_key_bytes)

    def __attrs_post_init__(self) -> None:
        """Initialize private key object from bytes."""
        _require_crypto()

        if self.private_key is None:
            raise CryptoKeyError(
                "private_key is required. Use Ed25519Signer.generate() to create new keypair.",
                code="CRYPTO_MISSING_PRIVATE_KEY",
            )

        if len(self.private_key) != ED25519_PRIVATE_KEY_SIZE:
            raise CryptoKeyError(
                f"Ed25519 private key must be {ED25519_PRIVATE_KEY_SIZE} bytes, got {len(self.private_key)}",
                code="CRYPTO_INVALID_PRIVATE_KEY_SIZE",
            )

        # Reconstruct private key object from seed bytes
        object.__setattr__(
            self,
            "_private_key_obj",
            ed25519.Ed25519PrivateKey.from_private_bytes(self.private_key),
        )

    @cached_property
    def public_key(self) -> bytes:
        """Get 32-byte Ed25519 public key.

        Returns:
            bytes: 32-byte public key
        """
        public_key_bytes = self._private_key_obj.public_key().public_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PublicFormat.Raw,
        )

        if len(public_key_bytes) != ED25519_PUBLIC_KEY_SIZE:
            raise CryptoKeyError(
                f"Invalid public key size: expected {ED25519_PUBLIC_KEY_SIZE} bytes, got {len(public_key_bytes)}",
                code="CRYPTO_INVALID_PUBLIC_KEY_SIZE",
            )

        logger.debug(f"🔑 Derived Ed25519 public key ({len(public_key_bytes)} bytes)")
        return public_key_bytes

    def sign(self, data: bytes) -> bytes:
        """Sign data with Ed25519 private key.

        Args:
            data: Data to sign

        Returns:
            bytes: 64-byte Ed25519 signature

        Raises:
            CryptoSignatureError: If signature generation fails
        """
        logger.debug(f"🔏 Signing {len(data)} bytes with Ed25519")

        signature = self._private_key_obj.sign(data)

        if len(signature) != ED25519_SIGNATURE_SIZE:
            raise CryptoSignatureError(
                f"Invalid signature size: expected {ED25519_SIGNATURE_SIZE} bytes, got {len(signature)}",
                code="CRYPTO_INVALID_SIGNATURE_SIZE",
            )

        logger.debug(f"✅ Created Ed25519 signature ({len(signature)} bytes)")
        return signature

    def export_private_key(self) -> bytes:
        """Export 32-byte private key seed.

        Returns:
            bytes: 32-byte Ed25519 private key seed

        Warning:
            Private keys should be stored securely. Consider encryption.
        """
        return self.private_key  # type: ignore


@define(slots=True)
class Ed25519Verifier:
    """Ed25519 signature verifier.

    Stateful verifier that holds public key and provides verification operations.

    Examples:
        >>> signer = Ed25519Signer.generate()
        >>> verifier = Ed25519Verifier(signer.public_key)
        >>> signature = signer.sign(b"message")
        >>> assert verifier.verify(b"message", signature)
    """

    public_key: bytes = field()
    _public_key_obj: ed25519.Ed25519PublicKey = field(init=False, repr=False)

    def __attrs_post_init__(self) -> None:
        """Initialize public key object from bytes."""
        _require_crypto()

        if len(self.public_key) != ED25519_PUBLIC_KEY_SIZE:
            raise CryptoKeyError(
                f"Ed25519 public key must be {ED25519_PUBLIC_KEY_SIZE} bytes, got {len(self.public_key)}",
                code="CRYPTO_INVALID_PUBLIC_KEY_SIZE",
            )

        # Reconstruct public key object from bytes
        object.__setattr__(
            self,
            "_public_key_obj",
            ed25519.Ed25519PublicKey.from_public_bytes(self.public_key),
        )

    def verify(self, data: bytes, signature: bytes) -> bool:
        """Verify Ed25519 signature.

        Args:
            data: Data that was signed
            signature: 64-byte Ed25519 signature

        Returns:
            bool: True if signature is valid, False otherwise
        """
        if len(signature) != ED25519_SIGNATURE_SIZE:
            logger.warning(
                f"❌ Invalid signature size: expected {ED25519_SIGNATURE_SIZE}, got {len(signature)}",
            )
            return False

        logger.debug(f"🔍 Verifying Ed25519 signature for {len(data)} bytes")

        try:
            self._public_key_obj.verify(signature, data)
            logger.debug("✅ Ed25519 signature verification successful")
            return True
        except Exception as e:
            logger.debug(f"❌ Invalid Ed25519 signature: {e}")
            return False


# =============================================================================
# RSA (Widely Compatible)
# =============================================================================


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

            logger.debug(f"✅ Created RSA-PSS signature ({len(signature)} bytes)")
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
            logger.debug("✅ RSA-PSS signature verification successful")
            return True
        except Exception as e:
            logger.debug(f"❌ Invalid RSA-PSS signature: {e}")
            return False


__all__ = [
    "Ed25519Signer",
    "Ed25519Verifier",
    "RSASigner",
    "RSAVerifier",
]
