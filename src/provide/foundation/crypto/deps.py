#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from __future__ import annotations

from typing import TYPE_CHECKING

from provide.foundation.utils.optional_deps import OptionalDependency

"""Optional cryptography dependency handling.

This module contains all the logic for handling the optional 'cryptography' package.
When cryptography is not installed, stub implementations are provided that raise
helpful ImportErrors with installation instructions.

This now uses the centralized OptionalDependency utility to eliminate
repetitive try/except ImportError boilerplate.
"""

if TYPE_CHECKING:
    pass  # All certificate types are available at runtime

# Initialize cryptography dependency handler
_crypto_dep = OptionalDependency("cryptography", "crypto")
_HAS_CRYPTO = _crypto_dep.is_available()

# Import certificate-related symbols
(
    Certificate,
    CertificateBase,
    CertificateConfig,
    CertificateError,
    CurveType,
    KeyType,
    create_ca,
    create_self_signed,
) = _crypto_dep.import_symbols(
    "provide.foundation.crypto.certificates",
    [
        "Certificate",
        "CertificateBase",
        "CertificateConfig",
        "CertificateError",
        "CurveType",
        "KeyType",
        "create_ca",
        "create_self_signed",
    ],
)

# Import constants
(
    DEFAULT_CERTIFICATE_KEY_TYPE,
    DEFAULT_CERTIFICATE_VALIDITY_DAYS,
    DEFAULT_ECDSA_CURVE,
    DEFAULT_RSA_KEY_SIZE,
    DEFAULT_SIGNATURE_ALGORITHM,
    ED25519_PRIVATE_KEY_SIZE,
    ED25519_PUBLIC_KEY_SIZE,
    ED25519_SIGNATURE_SIZE,
    SUPPORTED_EC_CURVES,
    SUPPORTED_KEY_TYPES,
    SUPPORTED_RSA_SIZES,
    get_default_hash_algorithm,
    get_default_signature_algorithm,
) = _crypto_dep.import_symbols(
    "provide.foundation.crypto.defaults",
    [
        "DEFAULT_CERTIFICATE_KEY_TYPE",
        "DEFAULT_CERTIFICATE_VALIDITY_DAYS",
        "DEFAULT_ECDSA_CURVE",
        "DEFAULT_RSA_KEY_SIZE",
        "DEFAULT_SIGNATURE_ALGORITHM",
        "ED25519_PRIVATE_KEY_SIZE",
        "ED25519_PUBLIC_KEY_SIZE",
        "ED25519_SIGNATURE_SIZE",
        "SUPPORTED_EC_CURVES",
        "SUPPORTED_KEY_TYPES",
        "SUPPORTED_RSA_SIZES",
        "get_default_hash_algorithm",
        "get_default_signature_algorithm",
    ],
)

# Import Ed25519 signers/verifiers
Ed25519Signer, Ed25519Verifier = _crypto_dep.import_symbols(
    "provide.foundation.crypto.ed25519",
    ["Ed25519Signer", "Ed25519Verifier"],
)

# Import key generation functions
(
    generate_ec_keypair,
    generate_ed25519_keypair,
    generate_keypair,
    generate_rsa_keypair,
    generate_signing_keypair,
    generate_tls_keypair,
) = _crypto_dep.import_symbols(
    "provide.foundation.crypto.keys",
    [
        "generate_ec_keypair",
        "generate_ed25519_keypair",
        "generate_keypair",
        "generate_rsa_keypair",
        "generate_signing_keypair",
        "generate_tls_keypair",
    ],
)

# Import RSA signers/verifiers
RSASigner, RSAVerifier = _crypto_dep.import_symbols(
    "provide.foundation.crypto.rsa",
    ["RSASigner", "RSAVerifier"],
)


__all__ = [
    # Constants
    "DEFAULT_CERTIFICATE_KEY_TYPE",
    "DEFAULT_CERTIFICATE_VALIDITY_DAYS",
    "DEFAULT_ECDSA_CURVE",
    "DEFAULT_RSA_KEY_SIZE",
    "DEFAULT_SIGNATURE_ALGORITHM",
    "ED25519_PRIVATE_KEY_SIZE",
    "ED25519_PUBLIC_KEY_SIZE",
    "ED25519_SIGNATURE_SIZE",
    "SUPPORTED_EC_CURVES",
    "SUPPORTED_KEY_TYPES",
    "SUPPORTED_RSA_SIZES",
    # Internal flag
    "_HAS_CRYPTO",
    # X.509 certificates
    "Certificate",
    "CertificateBase",
    "CertificateConfig",
    "CertificateError",
    # Types
    "CurveType",
    # OOP Signers/Verifiers
    "Ed25519Signer",
    "Ed25519Verifier",
    "KeyType",
    "RSASigner",
    "RSAVerifier",
    # Functions
    "create_ca",
    "create_self_signed",
    "generate_ec_keypair",
    "generate_ed25519_keypair",
    "generate_keypair",
    "generate_rsa_keypair",
    "generate_signing_keypair",
    "generate_tls_keypair",
    "get_default_hash_algorithm",
    "get_default_signature_algorithm",
]

# 🧱🏗️🔚
