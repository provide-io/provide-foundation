"""Cryptographic utilities for Foundation.

Provides hashing, checksum verification, digital signatures, key generation,
and X.509 certificate management.
"""

# Existing exports (hashing, checksums, algorithms, utils)
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

# New consolidated exports
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
from provide.foundation.crypto.signatures import (
    generate_ed25519_keypair,
    generate_signing_keypair,
    sign_data,
    verify_signature,
)
from provide.foundation.crypto.keys import (
    generate_keypair,
    generate_rsa_keypair,
    generate_ec_keypair,
    generate_tls_keypair,
    # Legacy compatibility
    generate_key_pair,
)
from provide.foundation.crypto.certificates import (
    Certificate,
    CertificateBase,
    CertificateConfig,
    CertificateError,
    create_ca,
    create_self_signed,
)

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
    
    # Legacy compatibility
    "generate_key_pair",
]
