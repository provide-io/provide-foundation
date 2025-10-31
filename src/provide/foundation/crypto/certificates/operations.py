#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from __future__ import annotations

import traceback
from typing import TYPE_CHECKING, cast

from provide.foundation import logger
from provide.foundation.crypto.certificates.base import (
    CertificateBase,
    CertificateError,
    KeyPair,
    PublicKey,
)

"""Certificate operations: CA creation, signing, and trust verification."""

if TYPE_CHECKING:
    from cryptography import x509
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.asymmetric import ec, padding, rsa
    from cryptography.x509 import Certificate as X509Certificate
    from cryptography.x509.oid import ExtendedKeyUsageOID

try:
    from cryptography import x509
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.asymmetric import ec, padding, rsa
    from cryptography.x509 import Certificate as X509Certificate
    from cryptography.x509.oid import ExtendedKeyUsageOID

    _HAS_CRYPTO = True
except ImportError:
    _HAS_CRYPTO = False


def create_x509_certificate(
    base: CertificateBase,
    private_key: KeyPair,
    alt_names: list[str] | None = None,
    issuer_name_override: x509.Name | None = None,
    signing_key_override: KeyPair | None = None,
    is_ca: bool = False,
    is_client_cert: bool = False,
) -> X509Certificate:
    """Internal helper to build and sign the X.509 certificate object."""
    try:
        logger.debug("📜📝🚀 create_x509_certificate: Building certificate")

        actual_issuer_name = issuer_name_override if issuer_name_override else base.issuer
        actual_signing_key = signing_key_override if signing_key_override else private_key

        if not actual_signing_key:
            raise CertificateError("Cannot sign certificate without a signing key (either own or override)")

        builder = (
            x509.CertificateBuilder()
            .subject_name(base.subject)
            .issuer_name(actual_issuer_name)
            .public_key(base.public_key)
            .serial_number(base.serial_number)
            .not_valid_before(base.not_valid_before)
            .not_valid_after(base.not_valid_after)
        )

        san_list = [x509.DNSName(name) for name in (alt_names or []) if name]
        if san_list:
            # DNSName is a subtype of GeneralName, but mypy needs help understanding this
            builder = builder.add_extension(x509.SubjectAlternativeName(cast(list, san_list)), critical=False)

        builder = builder.add_extension(
            x509.BasicConstraints(ca=is_ca, path_length=None),
            critical=True,
        )

        if is_ca:
            builder = builder.add_extension(
                x509.KeyUsage(
                    digital_signature=False,
                    key_encipherment=False,
                    key_agreement=False,
                    content_commitment=False,
                    data_encipherment=False,
                    key_cert_sign=True,
                    crl_sign=True,
                    encipher_only=False,
                    decipher_only=False,
                ),
                critical=True,
            )
        else:
            builder = builder.add_extension(
                x509.KeyUsage(
                    digital_signature=True,
                    key_encipherment=(
                        bool(not is_client_cert and isinstance(base.public_key, rsa.RSAPublicKey))
                    ),
                    key_agreement=(bool(isinstance(base.public_key, ec.EllipticCurvePublicKey))),
                    content_commitment=False,
                    data_encipherment=False,
                    key_cert_sign=False,
                    crl_sign=False,
                    encipher_only=False,
                    decipher_only=False,
                ),
                critical=True,
            )
            extended_usages = []
            if is_client_cert:
                extended_usages.append(ExtendedKeyUsageOID.CLIENT_AUTH)
            else:
                extended_usages.append(ExtendedKeyUsageOID.SERVER_AUTH)

            if extended_usages:
                builder = builder.add_extension(
                    x509.ExtendedKeyUsage(extended_usages),
                    critical=False,
                )

        logger.debug(
            f"KeyUsage, ExtendedKeyUsage (is_client_cert={is_client_cert})",
        )

        signed_cert = builder.sign(
            private_key=actual_signing_key,
            algorithm=hashes.SHA256(),
        )
        return signed_cert

    except Exception as e:
        logger.error(
            f"📜❌ create_x509_certificate: Failed: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError("Failed to create X.509 certificate object") from e


def validate_signature(
    signed_cert_obj: X509Certificate,
    signing_cert_obj: X509Certificate,
    signing_public_key: PublicKey,
) -> bool:
    """Internal helper: Validates signature and issuer/subject match."""
    if signed_cert_obj.issuer != signing_cert_obj.subject:
        logger.debug(
            f"📜🔍❌ Signature validation failed: Issuer/Subject mismatch. "
            f"Signed Issuer='{signed_cert_obj.issuer}', "
            f"Signing Subject='{signing_cert_obj.subject}'",
        )
        return False

    try:
        if not signing_public_key:
            logger.error("📜🔍❌ Cannot validate signature: Signing certificate has no public key")
            return False

        signature = signed_cert_obj.signature
        tbs_certificate_bytes = signed_cert_obj.tbs_certificate_bytes
        signature_hash_algorithm = signed_cert_obj.signature_hash_algorithm

        if not signature_hash_algorithm:
            logger.error("📜🔍❌ Cannot validate signature: Unknown hash algorithm")
            return False

        if isinstance(signing_public_key, rsa.RSAPublicKey):
            cast("rsa.RSAPublicKey", signing_public_key).verify(
                signature,
                tbs_certificate_bytes,
                padding.PKCS1v15(),
                signature_hash_algorithm,
            )
        elif isinstance(signing_public_key, ec.EllipticCurvePublicKey):
            cast("ec.EllipticCurvePublicKey", signing_public_key).verify(
                signature,
                tbs_certificate_bytes,
                ec.ECDSA(signature_hash_algorithm),
            )
        else:
            logger.error(f"📜🔍❌ Unsupported signing public key type: {type(signing_public_key)}")
            return False

        return True

    except Exception as e:
        logger.debug(f"📜🔍❌ Signature validation failed: {type(e).__name__}: {e}")
        return False


# 🧱🏗️🔚
