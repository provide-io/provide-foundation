"""Cryptographic constants and configuration."""

from typing import Final

# Ed25519 constants
ED25519_PRIVATE_KEY_SIZE: Final[int] = 32
ED25519_PUBLIC_KEY_SIZE: Final[int] = 32
ED25519_SIGNATURE_SIZE: Final[int] = 64

# RSA key sizes
DEFAULT_RSA_KEY_SIZE: Final[int] = 2048
SUPPORTED_RSA_SIZES: Final[set[int]] = {2048, 3072, 4096}

# ECDSA curves
DEFAULT_ECDSA_CURVE: Final[str] = "secp384r1"
SUPPORTED_EC_CURVES: Final[set[str]] = {
    "secp256r1",
    "secp384r1",
    "secp521r1",
}

# Key types
SUPPORTED_KEY_TYPES: Final[set[str]] = {"rsa", "ecdsa", "ed25519"}

# Default algorithms for different use cases
DEFAULT_SIGNATURE_ALGORITHM: Final[str] = "ed25519"  # Modern default for new code
DEFAULT_CERTIFICATE_KEY_TYPE: Final[str] = "ecdsa"  # Good balance for TLS/PKI
DEFAULT_CERTIFICATE_CURVE: Final[str] = DEFAULT_ECDSA_CURVE

# Certificate defaults
DEFAULT_CERTIFICATE_VALIDITY_DAYS: Final[int] = 365
MIN_CERTIFICATE_VALIDITY_DAYS: Final[int] = 1
MAX_CERTIFICATE_VALIDITY_DAYS: Final[int] = 3650  # 10 years


# Optional config integration
def _get_config_value(key: str, default: str | int) -> str | int:
    """Get crypto config value with fallback to default."""
    try:
        from provide.foundation.config import get_config

        return get_config(f"crypto.{key}", default)
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
