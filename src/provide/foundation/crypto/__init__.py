from __future__ import annotations

from typing import TYPE_CHECKING, Any, Never

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

# Provide stub implementations when cryptography is not available
if not _HAS_CRYPTO:
    from provide.foundation.errors import DependencyError

    # Certificate-related stubs
    class Certificate:
        """Stub for Certificate when cryptography is not installed."""

        def __init__(self, *args: Any, **kwargs: Any) -> None:
            raise DependencyError("cryptography", feature="crypto")

        def __new__(cls, *args: Any, **kwargs: Any) -> Never:
            raise DependencyError("cryptography", feature="crypto")

        @classmethod
        def create_self_signed_client_cert(cls, *args: Any, **kwargs: Any) -> Never:
            raise DependencyError("cryptography", feature="crypto")

        @classmethod
        def create_self_signed_server_cert(cls, *args: Any, **kwargs: Any) -> Never:
            raise DependencyError("cryptography", feature="crypto")

    class CertificateBase:
        """Stub for CertificateBase when cryptography is not installed."""

        def __init__(self, *args: Any, **kwargs: Any) -> None:
            raise DependencyError("cryptography", feature="crypto")

    class CertificateConfig:
        """Stub for CertificateConfig when cryptography is not installed."""

        def __init__(self, *args: Any, **kwargs: Any) -> None:
            raise DependencyError("cryptography", feature="crypto")

    class CertificateError(Exception):
        """Stub for CertificateError when cryptography is not installed."""

        pass  # Keep as regular exception for compatibility

    # Enum stubs
    class CurveType:
        """Stub for CurveType when cryptography is not installed."""

        def __init__(self, *args: Any, **kwargs: Any) -> None:
            raise DependencyError("cryptography", feature="crypto")

    class KeyType:
        """Stub for KeyType when cryptography is not installed."""

        def __init__(self, *args: Any, **kwargs: Any) -> None:
            raise DependencyError("cryptography", feature="crypto")

    # Certificate function stubs
    def create_ca(*args: Any, **kwargs: Any) -> Never:
        """Stub for create_ca when cryptography is not installed."""
        raise DependencyError("cryptography", feature="crypto")

    def create_self_signed(*args: Any, **kwargs: Any) -> Never:
        """Stub for create_self_signed when cryptography is not installed."""
        raise DependencyError("cryptography", feature="crypto")

    # Key generation function stubs
    def generate_ec_keypair(*args: Any, **kwargs: Any) -> Never:
        """Stub for generate_ec_keypair when cryptography is not installed."""
        raise DependencyError("cryptography", feature="crypto")

    def generate_ed25519_keypair(*args: Any, **kwargs: Any) -> Never:
        """Stub for generate_ed25519_keypair when cryptography is not installed."""
        raise DependencyError("cryptography", feature="crypto")

    def generate_key_pair(*args: Any, **kwargs: Any) -> Never:
        """Stub for generate_key_pair when cryptography is not installed."""
        raise DependencyError("cryptography", feature="crypto")

    def generate_keypair(*args: Any, **kwargs: Any) -> Never:
        """Stub for generate_keypair when cryptography is not installed."""
        raise DependencyError("cryptography", feature="crypto")

    def generate_rsa_keypair(*args: Any, **kwargs: Any) -> Never:
        """Stub for generate_rsa_keypair when cryptography is not installed."""
        raise DependencyError("cryptography", feature="crypto")

    def generate_signing_keypair(*args: Any, **kwargs: Any) -> Never:
        """Stub for generate_signing_keypair when cryptography is not installed."""
        raise DependencyError("cryptography", feature="crypto")

    def generate_tls_keypair(*args: Any, **kwargs: Any) -> Never:
        """Stub for generate_tls_keypair when cryptography is not installed."""
        raise DependencyError("cryptography", feature="crypto")

    # Signature function stubs
    def sign_data(*args: Any, **kwargs: Any) -> Never:
        """Stub for sign_data when cryptography is not installed."""
        raise DependencyError("cryptography", feature="crypto")

    def verify_signature(*args: Any, **kwargs: Any) -> Never:
        """Stub for verify_signature when cryptography is not installed."""
        raise DependencyError("cryptography", feature="crypto")

    # Import constants from centralized defaults
    from provide.foundation.config.defaults import (
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
    SUPPORTED_EC_CURVES = default_supported_ec_curves()
    SUPPORTED_KEY_TYPES = default_supported_key_types()
    SUPPORTED_RSA_SIZES = default_supported_rsa_sizes()

    def get_default_hash_algorithm() -> Never:
        """Stub for get_default_hash_algorithm when cryptography is not installed."""
        raise DependencyError("cryptography", feature="crypto")

    def get_default_signature_algorithm() -> Never:
        """Stub for get_default_signature_algorithm when cryptography is not installed."""
        raise DependencyError("cryptography", feature="crypto")


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
