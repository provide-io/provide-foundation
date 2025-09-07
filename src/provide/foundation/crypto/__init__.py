"""Cryptographic utilities for Foundation.

Provides hashing, checksum verification, digital signatures, key generation,
and X.509 certificate management.
"""

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
    Certificate = None
    CertificateBase = None
    CertificateConfig = None
    CertificateError = None
    CurveType = None
    KeyType = None
    create_ca = None
    create_self_signed = None
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
    # Constants stubs
    DEFAULT_CERTIFICATE_KEY_TYPE = None
    DEFAULT_CERTIFICATE_VALIDITY_DAYS = None
    DEFAULT_ECDSA_CURVE = None
    DEFAULT_RSA_KEY_SIZE = None
    DEFAULT_SIGNATURE_ALGORITHM = None
    ED25519_PRIVATE_KEY_SIZE = None
    ED25519_PUBLIC_KEY_SIZE = None
    ED25519_SIGNATURE_SIZE = None
    SUPPORTED_EC_CURVES = None
    SUPPORTED_KEY_TYPES = None
    SUPPORTED_RSA_SIZES = None
    get_default_hash_algorithm = None
    get_default_signature_algorithm = None
    # Key generation stubs
    generate_ec_keypair = None
    generate_key_pair = None
    generate_keypair = None
    generate_rsa_keypair = None
    generate_tls_keypair = None
    # Signature stubs
    generate_ed25519_keypair = None
    generate_signing_keypair = None
    sign_data = None
    verify_signature = None

# Public API organized by use case frequency
__all__ = [
    # Most common operations (90% of usage)
    "hash_file",
    "hash_data",
    "verify_file",
    "verify_data",
    # Digital signatures (5% of usage)
    "sign_data",
    "verify_signature",
    "generate_signing_keypair",
    # X.509 certificates (5% of usage)
    "Certificate",
    "create_self_signed",
    "create_ca",
    # Key generation
    "generate_keypair",
    "generate_rsa_keypair",
    "generate_ec_keypair",
    "generate_ed25519_keypair",
    "generate_tls_keypair",
    # Existing hashing & checksum functions
    "hash_stream",
    "hash_string",
    "calculate_checksums",
    "parse_checksum_file",
    "write_checksum_file",
    # Algorithm management
    "DEFAULT_ALGORITHM",
    "SUPPORTED_ALGORITHMS",
    "get_hasher",
    "is_secure_algorithm",
    "validate_algorithm",
    "get_default_hash_algorithm",
    "get_default_signature_algorithm",
    # Utility functions
    "compare_hash",
    "format_hash",
    "hash_name",
    "quick_hash",
    # Constants
    "DEFAULT_SIGNATURE_ALGORITHM",
    "DEFAULT_CERTIFICATE_KEY_TYPE",
    "DEFAULT_CERTIFICATE_VALIDITY_DAYS",
    "DEFAULT_RSA_KEY_SIZE",
    "DEFAULT_ECDSA_CURVE",
    "SUPPORTED_KEY_TYPES",
    "SUPPORTED_RSA_SIZES",
    "SUPPORTED_EC_CURVES",
    "ED25519_PRIVATE_KEY_SIZE",
    "ED25519_PUBLIC_KEY_SIZE",
    "ED25519_SIGNATURE_SIZE",
    # Advanced certificate classes
    "CertificateBase",
    "CertificateConfig",
    "CertificateError",
    "KeyType",
    "CurveType",
    # Legacy compatibility
    "generate_key_pair",
    # Internal flags (for tests)
    "_HAS_CRYPTO",
]
