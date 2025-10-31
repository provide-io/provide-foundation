#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
import traceback
from typing import TYPE_CHECKING

from provide.foundation import logger
from provide.foundation.crypto.certificates.base import (
    CertificateBase,
    CertificateConfig,
    CertificateError,
    CurveType,
    KeyPair,
    KeyType,
)
from provide.foundation.crypto.certificates.operations import create_x509_certificate
from provide.foundation.crypto.defaults import (
    DEFAULT_CERTIFICATE_CURVE,
    DEFAULT_CERTIFICATE_KEY_TYPE,
    DEFAULT_RSA_KEY_SIZE,
)

"""Certificate generation utilities."""


def _parse_key_type_and_params(
    key_type: str, key_size: int, ecdsa_curve: str
) -> tuple[KeyType, int | None, CurveType | None]:
    """Parse and validate key type parameters.

    Args:
        key_type: Key type string ('rsa' or 'ecdsa')
        key_size: RSA key size
        ecdsa_curve: ECDSA curve name

    Returns:
        Tuple of (KeyType, key_size_or_none, curve_or_none)

    Raises:
        ValueError: For invalid key types or curves
    """
    normalized_key_type_str = key_type.lower()
    match normalized_key_type_str:
        case "rsa":
            return KeyType.RSA, key_size, None
        case "ecdsa":
            try:
                curve = CurveType[ecdsa_curve.upper()]
                return KeyType.ECDSA, None, curve
            except KeyError as e_curve:
                raise ValueError(f"Unsupported ECDSA curve: {ecdsa_curve}") from e_curve
        case _:
            raise ValueError(f"Unsupported key_type string: '{key_type}'. Must be 'rsa' or 'ecdsa'.")


def _build_certificate_config(
    common_name: str,
    organization_name: str,
    not_valid_before: datetime,
    not_valid_after: datetime,
    alt_names: list[str] | None,
    gen_key_type: KeyType,
    gen_key_size: int | None,
    gen_curve: CurveType | None,
) -> CertificateConfig:
    """Build certificate configuration dictionary.

    Args:
        common_name: Certificate common name
        organization_name: Organization name
        not_valid_before: Certificate start validity
        not_valid_after: Certificate end validity
        alt_names: Subject alternative names
        gen_key_type: Key type enum
        gen_key_size: RSA key size (for RSA keys)
        gen_curve: ECDSA curve (for ECDSA keys)

    Returns:
        Certificate configuration dictionary
    """
    conf: CertificateConfig = {
        "common_name": common_name,
        "organization": organization_name,
        "alt_names": alt_names or ["localhost"],
        "key_type": gen_key_type,
        "not_valid_before": not_valid_before,
        "not_valid_after": not_valid_after,
    }
    if gen_curve is not None:
        conf["curve"] = gen_curve
    if gen_key_size is not None:
        conf["key_size"] = gen_key_size
    return conf


def _serialize_to_pem(
    x509_cert: x509.Certificate,
    private_key: KeyPair,
) -> tuple[str, str]:
    """Serialize certificate and private key to PEM format.

    Args:
        x509_cert: X.509 certificate object
        private_key: Private key object

    Returns:
        Tuple of (cert_pem, key_pem)
    """
    cert_pem = x509_cert.public_bytes(serialization.Encoding.PEM).decode("utf-8")
    key_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    ).decode("utf-8")
    return cert_pem, key_pem


if TYPE_CHECKING:
    from cryptography import x509
    from cryptography.hazmat.primitives import serialization

try:
    from cryptography import x509
    from cryptography.hazmat.primitives import serialization

    _HAS_CRYPTO = True
except ImportError:
    _HAS_CRYPTO = False


def generate_certificate(
    common_name: str,
    organization_name: str,
    validity_days: int,
    key_type: str = DEFAULT_CERTIFICATE_KEY_TYPE,
    key_size: int = DEFAULT_RSA_KEY_SIZE,
    ecdsa_curve: str = DEFAULT_CERTIFICATE_CURVE,
    alt_names: list[str] | None = None,
    is_ca: bool = False,
    is_client_cert: bool = False,
) -> tuple[
    CertificateBase,
    x509.Certificate,
    KeyPair,
    str,
    str,
]:
    """Generate a new certificate with a keypair.

    Returns:
        Tuple of (CertificateBase, X509Certificate, private_key, cert_pem, key_pem)

    """
    try:
        logger.debug("📜🔑🚀 Generating new keypair")

        # Calculate validity period
        now = datetime.now(UTC)
        not_valid_before = now - timedelta(days=1)
        not_valid_after = now + timedelta(days=validity_days)

        # Parse and validate key type parameters
        gen_key_type, gen_key_size, gen_curve = _parse_key_type_and_params(key_type, key_size, ecdsa_curve)

        # Build certificate configuration
        conf = _build_certificate_config(
            common_name=common_name,
            organization_name=organization_name,
            not_valid_before=not_valid_before,
            not_valid_after=not_valid_after,
            alt_names=alt_names,
            gen_key_type=gen_key_type,
            gen_key_size=gen_key_size,
            gen_curve=gen_curve,
        )
        logger.debug(f"📜🔑🚀 Generation config: {conf}")

        # Generate base certificate and private key
        base, private_key = CertificateBase.create(conf)

        # Create X.509 certificate
        x509_cert = create_x509_certificate(
            base=base,
            private_key=private_key,
            alt_names=alt_names or ["localhost"],
            is_ca=is_ca,
            is_client_cert=is_client_cert,
        )

        if x509_cert is None:
            raise CertificateError("Certificate object (_cert) is None after creation")

        # Serialize to PEM format
        cert_pem, key_pem = _serialize_to_pem(x509_cert, private_key)

        return base, x509_cert, private_key, cert_pem, key_pem

    except Exception as e:
        logger.error(
            f"📜❌ Failed to generate certificate. Error: {type(e).__name__}: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError(
            f"Failed to initialize certificate. Original error: {type(e).__name__}: {e}"
        ) from e


# 🧱🏗️🔚
