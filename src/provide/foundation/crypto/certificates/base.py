#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from __future__ import annotations

from datetime import UTC, datetime
from enum import StrEnum, auto
import traceback
from typing import TYPE_CHECKING, Any, NotRequired, Self, TypeAlias, TypedDict

from attrs import define

from provide.foundation import logger
from provide.foundation.crypto.defaults import (
    DEFAULT_RSA_KEY_SIZE,
)
from provide.foundation.errors.config import ValidationError

"""Certificate base classes, types, and utilities."""

if TYPE_CHECKING:
    from cryptography import x509
    from cryptography.hazmat.primitives.asymmetric import ec, rsa
    from cryptography.x509.oid import NameOID

try:
    from cryptography import x509
    from cryptography.hazmat.primitives.asymmetric import ec, rsa
    from cryptography.x509.oid import NameOID

    _HAS_CRYPTO = True
except ImportError:
    _HAS_CRYPTO = False


def _require_crypto() -> None:
    """Ensure cryptography is available for crypto operations."""
    if not _HAS_CRYPTO:
        raise ImportError(
            "Cryptography features require optional dependencies. Install with: "
            "pip install 'provide-foundation[crypto]'",
        )


class CertificateError(ValidationError):
    """Certificate-related errors."""

    def __init__(self, message: str, hint: str | None = None) -> None:
        super().__init__(
            message=message,
            field="certificate",
            value=None,
            rule=hint or "Certificate operation failed",
        )


class KeyType(StrEnum):
    RSA = auto()
    ECDSA = auto()


class CurveType(StrEnum):
    SECP256R1 = auto()
    SECP384R1 = auto()
    SECP521R1 = auto()


class CertificateConfig(TypedDict):
    common_name: str
    organization: str
    alt_names: list[str]
    key_type: KeyType
    not_valid_before: datetime
    not_valid_after: datetime
    # Optional key generation parameters
    key_size: NotRequired[int]
    curve: NotRequired[CurveType]


# Type aliases must be defined outside conditional for mypy
KeyPair: TypeAlias = Any
PublicKey: TypeAlias = Any

if _HAS_CRYPTO:
    # Override with specific types when crypto is available
    KeyPair = rsa.RSAPrivateKey | ec.EllipticCurvePrivateKey  # type: ignore[misc]
    PublicKey = rsa.RSAPublicKey | ec.EllipticCurvePublicKey  # type: ignore[misc]


@define(slots=True, frozen=True)
class CertificateBase:
    """Immutable base certificate data."""

    subject: x509.Name
    issuer: x509.Name
    public_key: PublicKey
    not_valid_before: datetime
    not_valid_after: datetime
    serial_number: int

    @classmethod
    def create(cls, config: CertificateConfig) -> tuple[Self, KeyPair]:
        """Create a new certificate base and private key."""
        _require_crypto()
        try:
            logger.debug("📜📝🚀 CertificateBase.create: Starting base creation")
            not_valid_before = config["not_valid_before"]
            not_valid_after = config["not_valid_after"]

            if not_valid_before.tzinfo is None:
                not_valid_before = not_valid_before.replace(tzinfo=UTC)
            if not_valid_after.tzinfo is None:
                not_valid_after = not_valid_after.replace(tzinfo=UTC)

            logger.debug(
                "📜📅 Certificate validity dates configured",
                not_valid_before=not_valid_before.isoformat(),
                not_valid_after=not_valid_after.isoformat(),
            )

            private_key: KeyPair
            match config["key_type"]:
                case KeyType.RSA:
                    key_size = config.get("key_size", DEFAULT_RSA_KEY_SIZE)
                    logger.debug(f"📜🔑🚀 Generating RSA key (size: {key_size})")
                    private_key = rsa.generate_private_key(public_exponent=65537, key_size=key_size)
                case KeyType.ECDSA:
                    curve_choice = config.get("curve", CurveType.SECP384R1)
                    logger.debug(f"📜🔑🚀 Generating ECDSA key (curve: {curve_choice})")
                    curve = getattr(ec, curve_choice.name)()
                    private_key = ec.generate_private_key(curve)
                case _:
                    raise ValueError(f"Internal Error: Unsupported key type: {config['key_type']}")

            subject = cls._create_name(config["common_name"], config["organization"])
            issuer = cls._create_name(config["common_name"], config["organization"])

            serial_number = x509.random_serial_number()

            base = cls(
                subject=subject,
                issuer=issuer,
                public_key=private_key.public_key(),
                not_valid_before=not_valid_before,
                not_valid_after=not_valid_after,
                serial_number=serial_number,
            )
            return base, private_key

        except Exception as e:
            logger.error(
                f"📜❌ CertificateBase.create: Failed: {e}",
                extra={"error": str(e), "trace": traceback.format_exc()},
            )
            raise CertificateError(f"Failed to generate certificate base: {e}") from e

    @staticmethod
    def _create_name(common_name: str, org: str) -> x509.Name:
        """Helper method to construct an X.509 name."""
        return x509.Name(
            [
                x509.NameAttribute(NameOID.COMMON_NAME, common_name),
                x509.NameAttribute(NameOID.ORGANIZATION_NAME, org),
            ],
        )


# 🧱🏗️🔚
