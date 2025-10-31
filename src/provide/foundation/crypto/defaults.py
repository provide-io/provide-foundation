#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from __future__ import annotations

from typing import Final

"""Crypto configuration defaults and constants for Foundation.

This module contains all cryptographic defaults, constants, and configuration
values for the crypto subsystem.
"""

# =================================
# Ed25519 Constants
# =================================
ED25519_PRIVATE_KEY_SIZE: Final[int] = 32
ED25519_PUBLIC_KEY_SIZE: Final[int] = 32
ED25519_SIGNATURE_SIZE: Final[int] = 64

# =================================
# RSA Defaults and Constants
# =================================
DEFAULT_RSA_KEY_SIZE: Final[int] = 2048
SUPPORTED_RSA_SIZES: Final[set[int]] = {2048, 3072, 4096}

# =================================
# ECDSA Defaults and Constants
# =================================
DEFAULT_ECDSA_CURVE: Final[str] = "secp384r1"
SUPPORTED_EC_CURVES: Final[set[str]] = {
    "secp256r1",
    "secp384r1",
    "secp521r1",
}

# =================================
# Key Type Constants
# =================================
SUPPORTED_KEY_TYPES: Final[set[str]] = {"rsa", "ecdsa", "ed25519"}

# =================================
# Algorithm Defaults
# =================================
DEFAULT_SIGNATURE_ALGORITHM: Final[str] = "ed25519"  # Modern default for new code
DEFAULT_CERTIFICATE_KEY_TYPE: Final[str] = "ecdsa"  # Good balance for TLS/PKI
DEFAULT_CERTIFICATE_CURVE: Final[str] = DEFAULT_ECDSA_CURVE

# =================================
# Certificate Defaults
# =================================
DEFAULT_CERTIFICATE_VALIDITY_DAYS: Final[int] = 365
MIN_CERTIFICATE_VALIDITY_DAYS: Final[int] = 1
MAX_CERTIFICATE_VALIDITY_DAYS: Final[int] = 3650  # 10 years
DEFAULT_CERTIFICATE_COMMON_NAME: Final[str] = "localhost"
DEFAULT_CERTIFICATE_ORGANIZATION_NAME: Final[str] = "Default Organization"
DEFAULT_CERTIFICATE_GENERATE_KEYPAIR: Final[bool] = False

# =================================
# Factory Functions
# =================================


def default_certificate_alt_names() -> list[str]:
    """Factory for default certificate alternative names."""
    return ["localhost"]


def default_supported_ec_curves() -> set[str]:
    """Factory for supported EC curves set."""
    return SUPPORTED_EC_CURVES.copy()


def default_supported_key_types() -> set[str]:
    """Factory for supported key types set."""
    return SUPPORTED_KEY_TYPES.copy()


def default_supported_rsa_sizes() -> set[int]:
    """Factory for supported RSA sizes set."""
    return SUPPORTED_RSA_SIZES.copy()


# =================================
# Config Integration
# =================================


def _get_config_value(key: str, default: str | int) -> str | int:
    """Get crypto config value with fallback to default."""
    try:
        from provide.foundation.config import get_config

        config = get_config(f"crypto.{key}")
        if config is not None and hasattr(config, "value"):
            value = config.value
            # Cast to str | int based on default type
            if isinstance(default, int):
                return int(value) if isinstance(value, (int, str)) else default
            return str(value) if value is not None else default
        return default
    except ImportError:
        # Config system not available, use defaults
        return default


def get_default_hash_algorithm() -> str:
    """Get default hash algorithm from config or fallback."""
    from provide.foundation.crypto.algorithms import DEFAULT_ALGORITHM

    return str(_get_config_value("hash_algorithm", DEFAULT_ALGORITHM))


def get_default_signature_algorithm() -> str:
    """Get default signature algorithm from config or fallback."""
    return str(_get_config_value("signature_algorithm", DEFAULT_SIGNATURE_ALGORITHM))


__all__ = [
    "DEFAULT_CERTIFICATE_COMMON_NAME",
    "DEFAULT_CERTIFICATE_CURVE",
    "DEFAULT_CERTIFICATE_GENERATE_KEYPAIR",
    "DEFAULT_CERTIFICATE_KEY_TYPE",
    "DEFAULT_CERTIFICATE_ORGANIZATION_NAME",
    # Certificates
    "DEFAULT_CERTIFICATE_VALIDITY_DAYS",
    # ECDSA
    "DEFAULT_ECDSA_CURVE",
    # RSA
    "DEFAULT_RSA_KEY_SIZE",
    # Algorithms
    "DEFAULT_SIGNATURE_ALGORITHM",
    # Ed25519 constants
    "ED25519_PRIVATE_KEY_SIZE",
    "ED25519_PUBLIC_KEY_SIZE",
    "ED25519_SIGNATURE_SIZE",
    "MAX_CERTIFICATE_VALIDITY_DAYS",
    "MIN_CERTIFICATE_VALIDITY_DAYS",
    "SUPPORTED_EC_CURVES",
    # Key types
    "SUPPORTED_KEY_TYPES",
    "SUPPORTED_RSA_SIZES",
    # Factory functions
    "default_certificate_alt_names",
    "default_supported_ec_curves",
    "default_supported_key_types",
    "default_supported_rsa_sizes",
    # Config integration
    "get_default_hash_algorithm",
    "get_default_signature_algorithm",
]

# 🧱🏗️🔚
