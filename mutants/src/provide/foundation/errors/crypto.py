# provide/foundation/errors/crypto.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from provide.foundation.errors.base import FoundationError

"""Cryptographic operation exceptions."""
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


class CryptoError(FoundationError):
    """Base exception for cryptographic operations.

    Raised when cryptographic operations fail due to invalid inputs,
    key issues, signature verification failures, or other crypto-related errors.

    Examples:
        >>> raise CryptoError("Invalid key size", code="CRYPTO_INVALID_KEY")
        >>> raise CryptoError("Signature verification failed", code="CRYPTO_VERIFY_FAILED")

    """

    def xǁCryptoErrorǁ_default_code__mutmut_orig(self) -> str:
        """Return default error code for crypto errors."""
        return "CRYPTO_ERROR"

    def xǁCryptoErrorǁ_default_code__mutmut_1(self) -> str:
        """Return default error code for crypto errors."""
        return "XXCRYPTO_ERRORXX"

    def xǁCryptoErrorǁ_default_code__mutmut_2(self) -> str:
        """Return default error code for crypto errors."""
        return "crypto_error"

    xǁCryptoErrorǁ_default_code__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁCryptoErrorǁ_default_code__mutmut_1": xǁCryptoErrorǁ_default_code__mutmut_1,
        "xǁCryptoErrorǁ_default_code__mutmut_2": xǁCryptoErrorǁ_default_code__mutmut_2,
    }

    def _default_code(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁCryptoErrorǁ_default_code__mutmut_orig"),
            object.__getattribute__(self, "xǁCryptoErrorǁ_default_code__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    _default_code.__signature__ = _mutmut_signature(xǁCryptoErrorǁ_default_code__mutmut_orig)
    xǁCryptoErrorǁ_default_code__mutmut_orig.__name__ = "xǁCryptoErrorǁ_default_code"


class CryptoValidationError(CryptoError):
    """Exception for cryptographic validation failures.

    Raised when validation of cryptographic inputs (keys, signatures, data) fails.

    Examples:
        >>> raise CryptoValidationError("Key size must be 32 bytes")
        >>> raise CryptoValidationError("Invalid signature format")

    """

    def xǁCryptoValidationErrorǁ_default_code__mutmut_orig(self) -> str:
        """Return default error code for crypto validation errors."""
        return "CRYPTO_VALIDATION_ERROR"

    def xǁCryptoValidationErrorǁ_default_code__mutmut_1(self) -> str:
        """Return default error code for crypto validation errors."""
        return "XXCRYPTO_VALIDATION_ERRORXX"

    def xǁCryptoValidationErrorǁ_default_code__mutmut_2(self) -> str:
        """Return default error code for crypto validation errors."""
        return "crypto_validation_error"

    xǁCryptoValidationErrorǁ_default_code__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁCryptoValidationErrorǁ_default_code__mutmut_1": xǁCryptoValidationErrorǁ_default_code__mutmut_1,
        "xǁCryptoValidationErrorǁ_default_code__mutmut_2": xǁCryptoValidationErrorǁ_default_code__mutmut_2,
    }

    def _default_code(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁCryptoValidationErrorǁ_default_code__mutmut_orig"),
            object.__getattribute__(self, "xǁCryptoValidationErrorǁ_default_code__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    _default_code.__signature__ = _mutmut_signature(xǁCryptoValidationErrorǁ_default_code__mutmut_orig)
    xǁCryptoValidationErrorǁ_default_code__mutmut_orig.__name__ = "xǁCryptoValidationErrorǁ_default_code"


class CryptoKeyError(CryptoError):
    """Exception for key-related cryptographic errors.

    Raised when key generation, loading, or validation fails.

    Examples:
        >>> raise CryptoKeyError("Private key must be 32 bytes")
        >>> raise CryptoKeyError("Failed to load key from PEM format")

    """

    def xǁCryptoKeyErrorǁ_default_code__mutmut_orig(self) -> str:
        """Return default error code for crypto key errors."""
        return "CRYPTO_KEY_ERROR"

    def xǁCryptoKeyErrorǁ_default_code__mutmut_1(self) -> str:
        """Return default error code for crypto key errors."""
        return "XXCRYPTO_KEY_ERRORXX"

    def xǁCryptoKeyErrorǁ_default_code__mutmut_2(self) -> str:
        """Return default error code for crypto key errors."""
        return "crypto_key_error"

    xǁCryptoKeyErrorǁ_default_code__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁCryptoKeyErrorǁ_default_code__mutmut_1": xǁCryptoKeyErrorǁ_default_code__mutmut_1,
        "xǁCryptoKeyErrorǁ_default_code__mutmut_2": xǁCryptoKeyErrorǁ_default_code__mutmut_2,
    }

    def _default_code(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁCryptoKeyErrorǁ_default_code__mutmut_orig"),
            object.__getattribute__(self, "xǁCryptoKeyErrorǁ_default_code__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    _default_code.__signature__ = _mutmut_signature(xǁCryptoKeyErrorǁ_default_code__mutmut_orig)
    xǁCryptoKeyErrorǁ_default_code__mutmut_orig.__name__ = "xǁCryptoKeyErrorǁ_default_code"


class CryptoSignatureError(CryptoError):
    """Exception for signature-related cryptographic errors.

    Raised when signature operations (signing or verification) fail.

    Examples:
        >>> raise CryptoSignatureError("Signature must be 64 bytes")
        >>> raise CryptoSignatureError("Invalid signature")

    """

    def xǁCryptoSignatureErrorǁ_default_code__mutmut_orig(self) -> str:
        """Return default error code for crypto signature errors."""
        return "CRYPTO_SIGNATURE_ERROR"

    def xǁCryptoSignatureErrorǁ_default_code__mutmut_1(self) -> str:
        """Return default error code for crypto signature errors."""
        return "XXCRYPTO_SIGNATURE_ERRORXX"

    def xǁCryptoSignatureErrorǁ_default_code__mutmut_2(self) -> str:
        """Return default error code for crypto signature errors."""
        return "crypto_signature_error"

    xǁCryptoSignatureErrorǁ_default_code__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁCryptoSignatureErrorǁ_default_code__mutmut_1": xǁCryptoSignatureErrorǁ_default_code__mutmut_1,
        "xǁCryptoSignatureErrorǁ_default_code__mutmut_2": xǁCryptoSignatureErrorǁ_default_code__mutmut_2,
    }

    def _default_code(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁCryptoSignatureErrorǁ_default_code__mutmut_orig"),
            object.__getattribute__(self, "xǁCryptoSignatureErrorǁ_default_code__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    _default_code.__signature__ = _mutmut_signature(xǁCryptoSignatureErrorǁ_default_code__mutmut_orig)
    xǁCryptoSignatureErrorǁ_default_code__mutmut_orig.__name__ = "xǁCryptoSignatureErrorǁ_default_code"


# <3 🧱🤝🐛🪄
