#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from __future__ import annotations

from provide.foundation.errors.base import FoundationError

"""Cryptographic operation exceptions."""


class CryptoError(FoundationError):
    """Base exception for cryptographic operations.

    Raised when cryptographic operations fail due to invalid inputs,
    key issues, signature verification failures, or other crypto-related errors.

    Examples:
        >>> raise CryptoError("Invalid key size", code="CRYPTO_INVALID_KEY")
        >>> raise CryptoError("Signature verification failed", code="CRYPTO_VERIFY_FAILED")

    """

    def _default_code(self) -> str:
        """Return default error code for crypto errors."""
        return "CRYPTO_ERROR"


class CryptoValidationError(CryptoError):
    """Exception for cryptographic validation failures.

    Raised when validation of cryptographic inputs (keys, signatures, data) fails.

    Examples:
        >>> raise CryptoValidationError("Key size must be 32 bytes")
        >>> raise CryptoValidationError("Invalid signature format")

    """

    def _default_code(self) -> str:
        """Return default error code for crypto validation errors."""
        return "CRYPTO_VALIDATION_ERROR"


class CryptoKeyError(CryptoError):
    """Exception for key-related cryptographic errors.

    Raised when key generation, loading, or validation fails.

    Examples:
        >>> raise CryptoKeyError("Private key must be 32 bytes")
        >>> raise CryptoKeyError("Failed to load key from PEM format")

    """

    def _default_code(self) -> str:
        """Return default error code for crypto key errors."""
        return "CRYPTO_KEY_ERROR"


class CryptoSignatureError(CryptoError):
    """Exception for signature-related cryptographic errors.

    Raised when signature operations (signing or verification) fail.

    Examples:
        >>> raise CryptoSignatureError("Signature must be 64 bytes")
        >>> raise CryptoSignatureError("Invalid signature")

    """

    def _default_code(self) -> str:
        """Return default error code for crypto signature errors."""
        return "CRYPTO_SIGNATURE_ERROR"


# 🧱🏗️🔚
