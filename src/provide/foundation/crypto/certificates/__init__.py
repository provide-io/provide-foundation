"""X.509 certificate generation and management."""

# Import from submodules using absolute imports
from provide.foundation.crypto.certificates.base import (
    CertificateBase,
    CertificateConfig,
    CertificateError,
    CurveType,
    KeyPair,
    KeyType,
    PublicKey,
    _HAS_CRYPTO,
    _require_crypto,
)
from provide.foundation.crypto.certificates.certificate import Certificate
from provide.foundation.crypto.certificates.factory import create_ca, create_self_signed
from provide.foundation.crypto.certificates.operations import (
    create_x509_certificate,
    validate_signature,
)

# Re-export public types - maintaining exact same API
__all__ = [
    "Certificate",
    "CertificateBase",
    "CertificateConfig",
    "CertificateError",
    "CurveType",
    "KeyType",
    "create_self_signed",
    "create_ca",
    "_HAS_CRYPTO",  # For testing
    "_require_crypto",  # For testing
]