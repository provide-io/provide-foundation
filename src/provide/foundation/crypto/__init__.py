from __future__ import annotations

from typing import TYPE_CHECKING

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

"""Cryptographic utilities for Foundation.

Provides hashing, checksum verification, digital signatures, key generation,
and X.509 certificate management.
"""

if TYPE_CHECKING:
    pass  # All certificate types are available at runtime

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

# Standard imports (always available) - already imported above

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
    from provide.foundation.crypto.signers import (
        Ed25519Signer,
        Ed25519Verifier,
        RSASigner,
        RSAVerifier,
    )

    if not _HAS_CRYPTO:
        _HAS_CRYPTO = True
except ImportError:
    pass

# Provide stub implementations when cryptography is not available
if not _HAS_CRYPTO:
    from provide.foundation.utils.stubs import create_dependency_stub, create_function_stub

    # Certificate-related stubs
    Certificate = create_dependency_stub("cryptography", "crypto")  # type: ignore[assignment,misc]
    CertificateBase = create_dependency_stub("cryptography", "crypto")  # type: ignore[assignment,misc]
    CertificateConfig = create_dependency_stub("cryptography", "crypto")  # type: ignore[assignment,misc]

    # Exception stub (keep as regular exception for compatibility)
    class CertificateError(Exception):  # type: ignore[no-redef]
        """Stub for CertificateError when cryptography is not installed."""

        pass

    # Enum stubs
    CurveType = create_dependency_stub("cryptography", "crypto")  # type: ignore[assignment,misc]
    KeyType = create_dependency_stub("cryptography", "crypto")  # type: ignore[assignment,misc]

    # Function stubs
    create_ca = create_function_stub("cryptography", "crypto")
    create_self_signed = create_function_stub("cryptography", "crypto")
    generate_ec_keypair = create_function_stub("cryptography", "crypto")
    generate_ed25519_keypair = create_function_stub("cryptography", "crypto")
    generate_keypair = create_function_stub("cryptography", "crypto")
    generate_rsa_keypair = create_function_stub("cryptography", "crypto")
    generate_signing_keypair = create_function_stub("cryptography", "crypto")
    generate_tls_keypair = create_function_stub("cryptography", "crypto")
    sign_data = create_function_stub("cryptography", "crypto")
    verify_signature = create_function_stub("cryptography", "crypto")

    # OOP Signer/Verifier stubs
    Ed25519Signer = create_dependency_stub("cryptography", "crypto")  # type: ignore[assignment,misc]
    Ed25519Verifier = create_dependency_stub("cryptography", "crypto")  # type: ignore[assignment,misc]
    RSASigner = create_dependency_stub("cryptography", "crypto")  # type: ignore[assignment,misc]
    RSAVerifier = create_dependency_stub("cryptography", "crypto")  # type: ignore[assignment,misc]

    # Import constants from centralized defaults
    from provide.foundation.config.defaults import (  # type: ignore[assignment]
        DEFAULT_CERTIFICATE_KEY_TYPE,
        DEFAULT_CERTIFICATE_VALIDITY_DAYS,
        DEFAULT_ECDSA_CURVE,
        DEFAULT_ED25519_PRIVATE_KEY_SIZE as ED25519_PRIVATE_KEY_SIZE,
        DEFAULT_ED25519_PUBLIC_KEY_SIZE as ED25519_PUBLIC_KEY_SIZE,
        DEFAULT_ED25519_SIGNATURE_SIZE as ED25519_SIGNATURE_SIZE,
        DEFAULT_RSA_KEY_SIZE,
        DEFAULT_SIGNATURE_ALGORITHM,
        default_supported_ec_curves,
        default_supported_key_types,
        default_supported_rsa_sizes,
    )

    # Call factory functions to get mutable defaults
    SUPPORTED_EC_CURVES = default_supported_ec_curves()  # type: ignore[misc]
    SUPPORTED_KEY_TYPES = default_supported_key_types()  # type: ignore[misc]
    SUPPORTED_RSA_SIZES = default_supported_rsa_sizes()  # type: ignore[misc]

    # Algorithm getter stubs
    get_default_hash_algorithm = create_function_stub("cryptography", "crypto")
    get_default_signature_algorithm = create_function_stub("cryptography", "crypto")


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
    # OOP Signers/Verifiers (modern API)
    "Ed25519Signer",
    "Ed25519Verifier",
    "KeyType",
    "RSASigner",
    "RSAVerifier",
    "calculate_checksums",
    # Utility functions
    "compare_hash",
    "create_ca",
    "create_self_signed",
    "format_hash",
    "generate_ec_keypair",
    "generate_ed25519_keypair",
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
