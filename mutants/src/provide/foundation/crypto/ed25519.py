# provide/foundation/crypto/ed25519.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

"""Ed25519 digital signature implementation.

Ed25519 is the recommended algorithm for new applications: fast, small keys,
deterministic signatures, and modern cryptography.

Examples:
    >>> signer = Ed25519Signer.generate()
    >>> signature = signer.sign(b"message")
    >>> verifier = Ed25519Verifier(signer.public_key)
    >>> assert verifier.verify(b"message", signature)
"""

from __future__ import annotations

from functools import cached_property
from typing import TYPE_CHECKING, Self

from attrs import define, field

from provide.foundation import logger
from provide.foundation.crypto.defaults import (
    ED25519_PRIVATE_KEY_SIZE,
    ED25519_PUBLIC_KEY_SIZE,
    ED25519_SIGNATURE_SIZE,
)
from provide.foundation.errors.crypto import CryptoKeyError, CryptoSignatureError

if TYPE_CHECKING:
    from cryptography.hazmat.primitives import serialization
    from cryptography.hazmat.primitives.asymmetric import ed25519

try:
    from cryptography.hazmat.primitives import serialization
    from cryptography.hazmat.primitives.asymmetric import ed25519

    _HAS_CRYPTO = True
except ImportError:
    _HAS_CRYPTO = False
from inspect import signature as _mutmut_signature
from typing import Annotated
from typing import Callable
from typing import ClassVar


MutantDict = Annotated[dict[str, Callable], "Mutant"]


def _mutmut_trampoline(orig, mutants, call_args, call_kwargs, self_arg=None):
    """Forward call to original or mutated function, depending on the environment"""
    import os

    mutant_under_test = os.environ["MUTANT_UNDER_TEST"]
    if mutant_under_test == "fail":
        from mutmut.__main__ import MutmutProgrammaticFailException

        raise MutmutProgrammaticFailException("Failed programmatically")
    elif mutant_under_test == "stats":
        from mutmut.__main__ import record_trampoline_hit

        record_trampoline_hit(orig.__module__ + "." + orig.__name__)
        result = orig(*call_args, **call_kwargs)
        return result
    prefix = orig.__module__ + "." + orig.__name__ + "__mutmut_"
    if not mutant_under_test.startswith(prefix):
        result = orig(*call_args, **call_kwargs)
        return result
    mutant_name = mutant_under_test.rpartition(".")[-1]
    if self_arg:
        # call to a class method where self is not bound
        result = mutants[mutant_name](self_arg, *call_args, **call_kwargs)
    else:
        result = mutants[mutant_name](*call_args, **call_kwargs)
    return result


def x__require_crypto__mutmut_orig() -> None:
    """Ensure cryptography is available."""
    if not _HAS_CRYPTO:
        raise ImportError(
            "Cryptography features require optional dependencies. "
            "Install with: pip install 'provide-foundation[crypto]'",
        )


def x__require_crypto__mutmut_1() -> None:
    """Ensure cryptography is available."""
    if _HAS_CRYPTO:
        raise ImportError(
            "Cryptography features require optional dependencies. "
            "Install with: pip install 'provide-foundation[crypto]'",
        )


def x__require_crypto__mutmut_2() -> None:
    """Ensure cryptography is available."""
    if not _HAS_CRYPTO:
        raise ImportError(
            None,
        )


def x__require_crypto__mutmut_3() -> None:
    """Ensure cryptography is available."""
    if not _HAS_CRYPTO:
        raise ImportError(
            "XXCryptography features require optional dependencies. XX"
            "Install with: pip install 'provide-foundation[crypto]'",
        )


def x__require_crypto__mutmut_4() -> None:
    """Ensure cryptography is available."""
    if not _HAS_CRYPTO:
        raise ImportError(
            "cryptography features require optional dependencies. "
            "Install with: pip install 'provide-foundation[crypto]'",
        )


def x__require_crypto__mutmut_5() -> None:
    """Ensure cryptography is available."""
    if not _HAS_CRYPTO:
        raise ImportError(
            "CRYPTOGRAPHY FEATURES REQUIRE OPTIONAL DEPENDENCIES. "
            "Install with: pip install 'provide-foundation[crypto]'",
        )


def x__require_crypto__mutmut_6() -> None:
    """Ensure cryptography is available."""
    if not _HAS_CRYPTO:
        raise ImportError(
            "Cryptography features require optional dependencies. "
            "XXInstall with: pip install 'provide-foundation[crypto]'XX",
        )


def x__require_crypto__mutmut_7() -> None:
    """Ensure cryptography is available."""
    if not _HAS_CRYPTO:
        raise ImportError(
            "Cryptography features require optional dependencies. "
            "install with: pip install 'provide-foundation[crypto]'",
        )


def x__require_crypto__mutmut_8() -> None:
    """Ensure cryptography is available."""
    if not _HAS_CRYPTO:
        raise ImportError(
            "Cryptography features require optional dependencies. "
            "INSTALL WITH: PIP INSTALL 'PROVIDE-FOUNDATION[CRYPTO]'",
        )


x__require_crypto__mutmut_mutants: ClassVar[MutantDict] = {
    "x__require_crypto__mutmut_1": x__require_crypto__mutmut_1,
    "x__require_crypto__mutmut_2": x__require_crypto__mutmut_2,
    "x__require_crypto__mutmut_3": x__require_crypto__mutmut_3,
    "x__require_crypto__mutmut_4": x__require_crypto__mutmut_4,
    "x__require_crypto__mutmut_5": x__require_crypto__mutmut_5,
    "x__require_crypto__mutmut_6": x__require_crypto__mutmut_6,
    "x__require_crypto__mutmut_7": x__require_crypto__mutmut_7,
    "x__require_crypto__mutmut_8": x__require_crypto__mutmut_8,
}


def _require_crypto(*args, **kwargs):
    result = _mutmut_trampoline(
        x__require_crypto__mutmut_orig, x__require_crypto__mutmut_mutants, args, kwargs
    )
    return result


_require_crypto.__signature__ = _mutmut_signature(x__require_crypto__mutmut_orig)
x__require_crypto__mutmut_orig.__name__ = "x__require_crypto"


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


__all__ = [
    "Ed25519Signer",
    "Ed25519Verifier",
]


# <3 🧱🤝🔒🪄
