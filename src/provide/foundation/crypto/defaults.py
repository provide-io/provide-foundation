from __future__ import annotations

"""Crypto defaults for Foundation configuration."""

# =================================
# Certificate Defaults
# =================================
DEFAULT_CERTIFICATE_KEY_TYPE = None
DEFAULT_CERTIFICATE_VALIDITY_DAYS = 365
DEFAULT_CERTIFICATE_COMMON_NAME = "localhost"
DEFAULT_CERTIFICATE_GENERATE_KEYPAIR = False
DEFAULT_CERTIFICATE_ORGANIZATION_NAME = "Default Organization"

# =================================
# Key Defaults
# =================================
DEFAULT_ECDSA_CURVE = None
DEFAULT_RSA_KEY_SIZE = 2048
DEFAULT_SIGNATURE_ALGORITHM = None

# =================================
# Ed25519 Defaults
# =================================
DEFAULT_ED25519_PRIVATE_KEY_SIZE = 32
DEFAULT_ED25519_PUBLIC_KEY_SIZE = 32
DEFAULT_ED25519_SIGNATURE_SIZE = 64

# =================================
# Factory Functions
# =================================


def default_certificate_alt_names() -> list[str]:
    """Factory for default certificate alternative names."""
    return ["localhost"]


def default_supported_ec_curves() -> set[str]:
    """Factory for supported EC curves set."""
    return set()


def default_supported_key_types() -> set[str]:
    """Factory for supported key types set."""
    return set()


def default_supported_rsa_sizes() -> set[int]:
    """Factory for supported RSA sizes set."""
    return set()


__all__ = [
    "DEFAULT_CERTIFICATE_COMMON_NAME",
    "DEFAULT_CERTIFICATE_GENERATE_KEYPAIR",
    "DEFAULT_CERTIFICATE_KEY_TYPE",
    "DEFAULT_CERTIFICATE_ORGANIZATION_NAME",
    "DEFAULT_CERTIFICATE_VALIDITY_DAYS",
    "DEFAULT_ECDSA_CURVE",
    "DEFAULT_ED25519_PRIVATE_KEY_SIZE",
    "DEFAULT_ED25519_PUBLIC_KEY_SIZE",
    "DEFAULT_ED25519_SIGNATURE_SIZE",
    "DEFAULT_RSA_KEY_SIZE",
    "DEFAULT_SIGNATURE_ALGORITHM",
    "default_certificate_alt_names",
    "default_supported_ec_curves",
    "default_supported_key_types",
    "default_supported_rsa_sizes",
]
