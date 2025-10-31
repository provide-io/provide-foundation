#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from __future__ import annotations

from typing import TYPE_CHECKING

from provide.foundation import logger
from provide.foundation.crypto.certificates.base import (
    CertificateError,
    _require_crypto,
)
from provide.foundation.crypto.certificates.operations import create_x509_certificate
from provide.foundation.crypto.defaults import (
    DEFAULT_CERTIFICATE_CURVE,
    DEFAULT_CERTIFICATE_KEY_TYPE,
    DEFAULT_CERTIFICATE_VALIDITY_DAYS,
    DEFAULT_RSA_KEY_SIZE,
)

"""Certificate factory methods."""

if TYPE_CHECKING:
    from cryptography.hazmat.primitives import serialization

    from provide.foundation.crypto.certificates.certificate import Certificate

try:
    from cryptography.hazmat.primitives import serialization

    _HAS_CRYPTO = True
except ImportError:
    _HAS_CRYPTO = False


def create_ca_certificate(
    common_name: str,
    organization_name: str,
    validity_days: int,
    key_type: str = DEFAULT_CERTIFICATE_KEY_TYPE,
    key_size: int = DEFAULT_RSA_KEY_SIZE,
    ecdsa_curve: str = DEFAULT_CERTIFICATE_CURVE,
) -> Certificate:
    """Creates a new self-signed CA certificate."""
    # Import here to avoid circular dependency
    from provide.foundation.crypto.certificates.certificate import Certificate

    logger.info(f"📜🔑🏭 Creating new CA certificate: CN={common_name}, Org={organization_name}")
    ca_cert_obj = Certificate.generate(
        common_name=common_name,
        organization_name=organization_name,
        validity_days=validity_days,
        key_type=key_type,
        key_size=key_size,
        ecdsa_curve=ecdsa_curve,
        alt_names=[common_name],
        is_ca=False,  # Will be re-signed with is_ca=True below
        is_client_cert=False,
    )
    # Re-sign to ensure CA flags are correctly set for a CA
    logger.info("📜🔑🏭 Re-signing generated CA certificate to ensure is_ca=True")
    actual_ca_x509_cert = create_x509_certificate(
        base=ca_cert_obj._base,
        private_key=ca_cert_obj._private_key,
        alt_names=ca_cert_obj.alt_names,
        is_ca=True,
        is_client_cert=False,
    )
    ca_cert_obj._cert = actual_ca_x509_cert
    ca_cert_obj.cert_pem = actual_ca_x509_cert.public_bytes(serialization.Encoding.PEM).decode("utf-8")
    return ca_cert_obj


def create_signed_certificate(
    ca_certificate: Certificate,
    common_name: str,
    organization_name: str,
    validity_days: int,
    alt_names: list[str] | None = None,
    key_type: str = DEFAULT_CERTIFICATE_KEY_TYPE,
    key_size: int = DEFAULT_RSA_KEY_SIZE,
    ecdsa_curve: str = DEFAULT_CERTIFICATE_CURVE,
    is_client_cert: bool = False,
) -> Certificate:
    """Creates a new certificate signed by the provided CA certificate."""
    # Import here to avoid circular dependency
    from provide.foundation.crypto.certificates.certificate import Certificate

    logger.info(
        f"📜🔑🏭 Creating new certificate signed by CA '{ca_certificate.subject}': "
        f"CN={common_name}, Org={organization_name}, ClientCert={is_client_cert}",
    )
    if not ca_certificate._private_key:
        raise CertificateError(
            message="CA certificate's private key is not available for signing.",
            hint="Ensure the CA certificate object was loaded or created with its private key.",
        )
    if not ca_certificate.is_ca:
        logger.warning(
            f"📜🔑⚠️ Signing certificate (Subject: {ca_certificate.subject}) "
            "is not marked as a CA. This might lead to validation issues.",
        )

    new_cert_obj = Certificate.generate(
        common_name=common_name,
        organization_name=organization_name,
        validity_days=validity_days,
        alt_names=alt_names or [common_name],
        key_type=key_type,
        key_size=key_size,
        ecdsa_curve=ecdsa_curve,
        is_ca=False,
        is_client_cert=is_client_cert,
    )

    signed_x509_cert = create_x509_certificate(
        base=new_cert_obj._base,
        private_key=new_cert_obj._private_key,
        alt_names=new_cert_obj.alt_names,
        issuer_name_override=ca_certificate._base.subject,
        signing_key_override=ca_certificate._private_key,
        is_ca=False,
        is_client_cert=is_client_cert,
    )

    new_cert_obj._cert = signed_x509_cert
    new_cert_obj.cert_pem = signed_x509_cert.public_bytes(serialization.Encoding.PEM).decode("utf-8")

    logger.info(
        f"CN={common_name} by CA='{ca_certificate.subject}'",
    )
    return new_cert_obj


def create_self_signed_server_cert(
    common_name: str,
    organization_name: str,
    validity_days: int,
    alt_names: list[str] | None = None,
    key_type: str = DEFAULT_CERTIFICATE_KEY_TYPE,
    key_size: int = DEFAULT_RSA_KEY_SIZE,
    ecdsa_curve: str = DEFAULT_CERTIFICATE_CURVE,
) -> Certificate:
    """Creates a new self-signed end-entity certificate suitable for a server."""
    # Import here to avoid circular dependency
    from provide.foundation.crypto.certificates.certificate import Certificate

    logger.info(
        f"📜🔑🏭 Creating new self-signed SERVER certificate: CN={common_name}, Org={organization_name}",
    )

    cert_obj = Certificate.generate(
        common_name=common_name,
        organization_name=organization_name,
        validity_days=validity_days,
        alt_names=alt_names or [common_name],
        key_type=key_type,
        key_size=key_size,
        ecdsa_curve=ecdsa_curve,
        is_ca=False,
        is_client_cert=False,
    )

    return cert_obj


def create_self_signed_client_cert(
    common_name: str,
    organization_name: str,
    validity_days: int,
    alt_names: list[str] | None = None,
    key_type: str = DEFAULT_CERTIFICATE_KEY_TYPE,
    key_size: int = DEFAULT_RSA_KEY_SIZE,
    ecdsa_curve: str = DEFAULT_CERTIFICATE_CURVE,
) -> Certificate:
    """Creates a new self-signed end-entity certificate suitable for a client."""
    # Import here to avoid circular dependency
    from provide.foundation.crypto.certificates.certificate import Certificate

    logger.info(
        f"📜🔑🏭 Creating new self-signed CLIENT certificate: CN={common_name}, Org={organization_name}",
    )

    cert_obj = Certificate.generate(
        common_name=common_name,
        organization_name=organization_name,
        validity_days=validity_days,
        alt_names=alt_names or [common_name],
        key_type=key_type,
        key_size=key_size,
        ecdsa_curve=ecdsa_curve,
        is_ca=False,
        is_client_cert=True,  # This is the key difference from server cert
    )

    return cert_obj


# Convenience functions for common use cases
def create_self_signed(
    common_name: str = "localhost",
    alt_names: list[str] | None = None,
    organization: str = "Default Organization",
    validity_days: int = DEFAULT_CERTIFICATE_VALIDITY_DAYS,
    key_type: str = DEFAULT_CERTIFICATE_KEY_TYPE,
) -> Certificate:
    """Create a self-signed certificate (convenience function)."""
    _require_crypto()
    return create_self_signed_server_cert(
        common_name=common_name,
        organization_name=organization,
        validity_days=validity_days,
        alt_names=alt_names or [common_name],
        key_type=key_type,
    )


def create_ca(
    common_name: str,
    organization: str = "Default CA Organization",
    validity_days: int = DEFAULT_CERTIFICATE_VALIDITY_DAYS * 2,  # CAs live longer
    key_type: str = DEFAULT_CERTIFICATE_KEY_TYPE,
) -> Certificate:
    """Create a CA certificate (convenience function)."""
    _require_crypto()
    return create_ca_certificate(
        common_name=common_name,
        organization_name=organization,
        validity_days=validity_days,
        key_type=key_type,
    )


# 🧱🏗️🔚
