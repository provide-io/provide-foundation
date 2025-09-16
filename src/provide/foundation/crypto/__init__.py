from __future__ import annotations

"""Cryptographic utilities for Foundation.

Provides hashing, checksum verification, digital signatures, key generation,
and X.509 certificate management.
"""

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    # Import certificate types only for type checking
    from provide.foundation.crypto.certificates import (
        Certificate as CertificateType,
        CertificateBase as CertificateBaseType,
        CertificateConfig as CertificateConfigType,
        CertificateError as CertificateErrorType,
        CurveType as CurveTypeType,
        KeyType as KeyTypeType,
        create_ca as create_ca_type,
        create_self_signed as create_self_signed_type,
    )

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

# Cryptography-dependent imports (require optional dependency)
try:
    from provide.foundation.crypto.certificates import (
        Certificate,
        CertificateBase,
        CertificateConfig,
        CertificateError,
        CurveType,
        KeyType,
        create_ca,
        create_self_signed,
    )

    _HAS_CRYPTO = True
except ImportError:
    _HAS_CRYPTO = False

# Standard imports (always available)
from provide.foundation.crypto.hashing import (
    hash_data,
    hash_file,
    hash_stream,
    hash_string,
)
from provide.foundation.crypto.utils import (
    compare_hash,
    format_hash,
    hash_name,
    quick_hash,
)

# More cryptography-dependent imports
try:
    from provide.foundation.crypto.constants import (
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
    )
    from provide.foundation.crypto.keys import (
        generate_ec_keypair,
        generate_key_pair,
        generate_keypair,
        generate_rsa_keypair,
        generate_tls_keypair,
    )
    from provide.foundation.crypto.signatures import (
        generate_ed25519_keypair,
        generate_signing_keypair,
        sign_data,
        verify_signature,
    )

    if not _HAS_CRYPTO:
        _HAS_CRYPTO = True
except ImportError:
    pass

# Public API organized by use case frequency
__all__ = [
    # Algorithm management
    "DEFAULT_ALGORITHM",
    "DEFAULT_CERTIFICATE_KEY_TYPE",
    "DEFAULT_CERTIFICATE_VALIDITY_DAYS",
    "DEFAULT_ECDSA_CURVE",
    "DEFAULT_RSA_KEY_SIZE",
    # Constants
    "DEFAULT_SIGNATURE_ALGORITHM",
    "ED25519_PRIVATE_KEY_SIZE",
    "ED25519_PUBLIC_KEY_SIZE",
    "ED25519_SIGNATURE_SIZE",
    "SUPPORTED_ALGORITHMS",
    "SUPPORTED_EC_CURVES",
    "SUPPORTED_KEY_TYPES",
    "SUPPORTED_RSA_SIZES",
    # Internal flags (for tests)
    "_HAS_CRYPTO",
    # X.509 certificates (5% of usage)
    "Certificate",
    # Advanced certificate classes
    "CertificateBase",
    "CertificateConfig",
    "CertificateError",
    "CurveType",
    "KeyType",
    "calculate_checksums",
    # Utility functions
    "compare_hash",
    "create_ca",
    "create_self_signed",
    "format_hash",
    "generate_ec_keypair",
    "generate_ed25519_keypair",
    # Legacy compatibility
    "generate_key_pair",
    # Key generation
    "generate_keypair",
    "generate_rsa_keypair",
    "generate_signing_keypair",
    "generate_tls_keypair",
    "get_default_hash_algorithm",
    "get_default_signature_algorithm",
    "get_hasher",
    "hash_data",
    # Most common operations (90% of usage)
    "hash_file",
    "hash_name",
    # Existing hashing & checksum functions
    "hash_stream",
    "hash_string",
    "is_secure_algorithm",
    "parse_checksum_file",
    "quick_hash",
    # Digital signatures (5% of usage)
    "sign_data",
    "validate_algorithm",
    "verify_data",
    "verify_file",
    "verify_signature",
    "write_checksum_file",
]
