#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from __future__ import annotations

# Standard crypto imports (always available - use hashlib)
from provide.foundation.crypto.algorithms import (
    DEFAULT_ALGORITHM,
    SUPPORTED_ALGORITHMS,
    get_hasher,
    is_secure_algorithm,
    validate_algorithm,
)
from provide.foundation.crypto.checksums import (
    calculate_checksums,
    parse_checksum_file,
    verify_data,
    verify_file,
    write_checksum_file,
)

# Optional crypto imports (cryptography package required) - all logic in deps.py
from provide.foundation.crypto.deps import (
    _HAS_CRYPTO,
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
    Certificate,
    CertificateBase,
    CertificateConfig,
    CertificateError,
    CurveType,
    Ed25519Signer,
    Ed25519Verifier,
    KeyType,
    RSASigner,
    RSAVerifier,
    create_ca,
    create_self_signed,
    generate_ec_keypair,
    generate_ed25519_keypair,
    generate_keypair,
    generate_rsa_keypair,
    generate_signing_keypair,
    generate_tls_keypair,
    get_default_hash_algorithm,
    get_default_signature_algorithm,
)
from provide.foundation.crypto.hashing import (
    hash_data,
    hash_file,
    hash_stream,
    hash_string,
)
from provide.foundation.crypto.prefixed import (
    format_checksum,
    is_strong_checksum,
    normalize_checksum,
    parse_checksum,
    verify_checksum,
)
from provide.foundation.crypto.utils import (
    compare_hash,
    format_hash,
    hash_name,
    quick_hash,
)

"""Cryptographic utilities for Foundation.

Provides hashing, checksum verification, digital signatures, key generation,
and X.509 certificate management.
"""


__all__ = [
    "DEFAULT_ALGORITHM",
    "DEFAULT_CERTIFICATE_KEY_TYPE",
    "DEFAULT_CERTIFICATE_VALIDITY_DAYS",
    "DEFAULT_ECDSA_CURVE",
    "DEFAULT_RSA_KEY_SIZE",
    "DEFAULT_SIGNATURE_ALGORITHM",
    "ED25519_PRIVATE_KEY_SIZE",
    "ED25519_PUBLIC_KEY_SIZE",
    "ED25519_SIGNATURE_SIZE",
    "SUPPORTED_ALGORITHMS",
    "SUPPORTED_EC_CURVES",
    "SUPPORTED_KEY_TYPES",
    "SUPPORTED_RSA_SIZES",
    "_HAS_CRYPTO",
    "Certificate",
    "CertificateBase",
    "CertificateConfig",
    "CertificateError",
    "CurveType",
    "Ed25519Signer",
    "Ed25519Verifier",
    "KeyType",
    "RSASigner",
    "RSAVerifier",
    "calculate_checksums",
    "compare_hash",
    "create_ca",
    "create_self_signed",
    "format_checksum",
    "format_hash",
    "generate_ec_keypair",
    "generate_ed25519_keypair",
    "generate_keypair",
    "generate_rsa_keypair",
    "generate_signing_keypair",
    "generate_tls_keypair",
    "get_default_hash_algorithm",
    "get_default_signature_algorithm",
    "get_hasher",
    "hash_data",
    "hash_file",
    "hash_name",
    "hash_stream",
    "hash_string",
    "is_secure_algorithm",
    "is_strong_checksum",
    "normalize_checksum",
    "parse_checksum",
    "parse_checksum_file",
    "quick_hash",
    "validate_algorithm",
    "verify_checksum",
    "verify_data",
    "verify_file",
    "write_checksum_file",
]

# 🧱🏗️🔚
