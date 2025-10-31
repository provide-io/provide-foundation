#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from __future__ import annotations

from provide.foundation.crypto.certificates.base import (
    _HAS_CRYPTO,
    CertificateBase,
    CertificateConfig,
    CertificateError,
    CurveType,
    KeyPair,
    KeyType,
    PublicKey,
    _require_crypto,
)
from provide.foundation.crypto.certificates.certificate import Certificate
from provide.foundation.crypto.certificates.factory import create_ca, create_self_signed
from provide.foundation.crypto.certificates.operations import (
    create_x509_certificate,
    validate_signature,
)

"""X.509 certificate generation and management."""

# Re-export public types - maintaining exact same API
__all__ = [
    "_HAS_CRYPTO",  # For testing
    "Certificate",
    "CertificateBase",
    "CertificateConfig",
    "CertificateError",
    "CurveType",
    "KeyPair",
    "KeyType",
    "PublicKey",
    "_require_crypto",  # For testing
    "create_ca",
    "create_self_signed",
    "create_x509_certificate",
    "validate_signature",
]

# 🧱🏗️🔚
