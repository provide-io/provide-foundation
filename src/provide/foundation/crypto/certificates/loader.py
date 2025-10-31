#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from __future__ import annotations

from datetime import UTC
import os
from pathlib import Path
import traceback
from typing import TYPE_CHECKING

from provide.foundation import logger
from provide.foundation.crypto.certificates.base import (
    CertificateBase,
    CertificateError,
)

"""Certificate loading utilities."""

if TYPE_CHECKING:
    from cryptography import x509
    from cryptography.hazmat.primitives.asymmetric import ec, rsa
    from cryptography.hazmat.primitives.serialization import load_pem_private_key

try:
    from cryptography import x509
    from cryptography.hazmat.primitives.asymmetric import ec, rsa
    from cryptography.hazmat.primitives.serialization import load_pem_private_key

    _HAS_CRYPTO = True
except ImportError:
    _HAS_CRYPTO = False


def load_from_uri_or_pem(data: str) -> str:
    """Load PEM data either directly from a string or from a file URI."""
    try:
        if data.startswith("file://"):
            path_str = data.removeprefix("file://")
            if os.name == "nt" and path_str.startswith("//"):
                path = Path(path_str)
            else:
                path_str = path_str.lstrip("/")
                if os.name != "nt" and data.startswith("file:///"):
                    path_str = "/" + path_str
                path = Path(path_str)

            logger.debug(f"📜📂🚀 Loading data from file: {path}")
            with path.open("r", encoding="utf-8") as f:
                loaded_data = f.read().strip()
            return loaded_data

        loaded_data = data.strip()
        if not loaded_data.startswith("-----BEGIN"):
            logger.warning("📜📂⚠️ Data doesn't look like PEM format")
        return loaded_data
    except Exception as e:
        logger.error(f"📜📂❌ Failed to load data: {e}", extra={"error": str(e)})
        raise CertificateError(f"Failed to load data: {e}") from e


def load_certificate_from_pem(
    cert_pem_or_uri: str,
    key_pem_or_uri: str | None = None,
) -> tuple[
    CertificateBase,
    x509.Certificate,
    rsa.RSAPrivateKey | ec.EllipticCurvePrivateKey | None,
    str,
    str | None,
]:
    """Load a certificate and optionally its private key from PEM data or file URIs.

    Returns:
        Tuple of (CertificateBase, X509Certificate, private_key, cert_pem, key_pem)

    """
    try:
        logger.debug("📜🔑🚀 Loading certificate from provided data")
        cert_data = load_from_uri_or_pem(cert_pem_or_uri)

        logger.debug("📜🔑🔍 Loading X.509 certificate from PEM data")
        x509_cert = x509.load_pem_x509_certificate(cert_data.encode("utf-8"))

        private_key = None
        key_data = None

        if key_pem_or_uri:
            logger.debug("📜🔑🚀 Loading private key")
            key_data = load_from_uri_or_pem(key_pem_or_uri)

            loaded_priv_key = load_pem_private_key(key_data.encode("utf-8"), password=None)
            if not isinstance(
                loaded_priv_key,
                rsa.RSAPrivateKey | ec.EllipticCurvePrivateKey,
            ):
                raise CertificateError(
                    f"Loaded private key is of unsupported type: {type(loaded_priv_key)}. "
                    "Expected RSA or ECDSA private key.",
                )
            private_key = loaded_priv_key

        # Extract certificate details for CertificateBase
        loaded_not_valid_before = x509_cert.not_valid_before_utc  # type: ignore[attr-defined]
        loaded_not_valid_after = x509_cert.not_valid_after_utc  # type: ignore[attr-defined]
        if loaded_not_valid_before.tzinfo is None:
            loaded_not_valid_before = loaded_not_valid_before.replace(tzinfo=UTC)
        if loaded_not_valid_after.tzinfo is None:
            loaded_not_valid_after = loaded_not_valid_after.replace(tzinfo=UTC)

        cert_public_key = x509_cert.public_key()
        if not isinstance(cert_public_key, rsa.RSAPublicKey | ec.EllipticCurvePublicKey):
            raise CertificateError(
                f"Certificate's public key is of unsupported type: {type(cert_public_key)}. "
                "Expected RSA or ECDSA public key.",
            )

        base = CertificateBase(
            subject=x509_cert.subject,
            issuer=x509_cert.issuer,
            public_key=cert_public_key,
            not_valid_before=loaded_not_valid_before,
            not_valid_after=loaded_not_valid_after,
            serial_number=x509_cert.serial_number,
        )

        return base, x509_cert, private_key, cert_data, key_data

    except Exception as e:
        logger.error(
            f"📜❌ Failed to load certificate. Error: {type(e).__name__}: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError(f"Failed to initialize certificate. Original error: {type(e).__name__}") from e


# 🧱🏗️🔚
