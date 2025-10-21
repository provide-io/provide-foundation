# provide/foundation/crypto/rsa.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

"""RSA digital signature implementation.

RSA-PSS signatures with SHA-256 for compatibility with existing systems.
For new applications, prefer Ed25519 (faster, smaller keys, simpler).

Examples:
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
from inspect import signature as _mutmut_signature
from typing import Annotated
from typing import Callable
from typing import ClassVar


MutantDict = Annotated[dict[str, Callable], "Mutant"]


def _mutmut_trampoline(orig, mutants, call_args, call_kwargs, self_arg = None):
    """Forward call to original or mutated function, depending on the environment"""
    import os
    mutant_under_test = os.environ['MUTANT_UNDER_TEST']
    if mutant_under_test == 'fail':
        from mutmut.__main__ import MutmutProgrammaticFailException
        raise MutmutProgrammaticFailException('Failed programmatically')      
    elif mutant_under_test == 'stats':
        from mutmut.__main__ import record_trampoline_hit
        record_trampoline_hit(orig.__module__ + '.' + orig.__name__)
        result = orig(*call_args, **call_kwargs)
        return result
    prefix = orig.__module__ + '.' + orig.__name__ + '__mutmut_'
    if not mutant_under_test.startswith(prefix):
        result = orig(*call_args, **call_kwargs)
        return result
    mutant_name = mutant_under_test.rpartition('.')[-1]
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

x__require_crypto__mutmut_mutants : ClassVar[MutantDict] = {
'x__require_crypto__mutmut_1': x__require_crypto__mutmut_1, 
    'x__require_crypto__mutmut_2': x__require_crypto__mutmut_2, 
    'x__require_crypto__mutmut_3': x__require_crypto__mutmut_3, 
    'x__require_crypto__mutmut_4': x__require_crypto__mutmut_4, 
    'x__require_crypto__mutmut_5': x__require_crypto__mutmut_5, 
    'x__require_crypto__mutmut_6': x__require_crypto__mutmut_6, 
    'x__require_crypto__mutmut_7': x__require_crypto__mutmut_7, 
    'x__require_crypto__mutmut_8': x__require_crypto__mutmut_8
}

def _require_crypto(*args, **kwargs):
    result = _mutmut_trampoline(x__require_crypto__mutmut_orig, x__require_crypto__mutmut_mutants, args, kwargs)
    return result 

_require_crypto.__signature__ = _mutmut_signature(x__require_crypto__mutmut_orig)
x__require_crypto__mutmut_orig.__name__ = 'x__require_crypto'


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
    "RSASigner",
    "RSAVerifier",
]


# <3 🧱🤝🔒🪄
