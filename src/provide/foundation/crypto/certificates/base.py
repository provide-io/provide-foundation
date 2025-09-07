"""Certificate base classes, types, and utilities."""

from datetime import UTC, datetime
from enum import StrEnum, auto
import traceback
from typing import NotRequired, Self, TypeAlias, TypedDict

from attrs import define, field

try:
    from cryptography import x509
    from cryptography.hazmat.backends import default_backend
    from cryptography.hazmat.primitives import hashes, serialization
    from cryptography.hazmat.primitives.asymmetric import ec, rsa
    from cryptography.hazmat.primitives.serialization import load_pem_private_key
    from cryptography.x509 import Certificate as X509Certificate
    from cryptography.x509.oid import ExtendedKeyUsageOID, NameOID

    _HAS_CRYPTO = True
except ImportError:
    # Stub out cryptography types for type hints
    x509 = None
    default_backend = None
    hashes = None
    serialization = None
    ec = None
    rsa = None
    load_pem_private_key = None
    X509Certificate = None
    ExtendedKeyUsageOID = None
    NameOID = None
    _HAS_CRYPTO = False

from provide.foundation import logger
from provide.foundation.crypto.constants import (
    DEFAULT_RSA_KEY_SIZE,
)
from provide.foundation.errors.config import ValidationError


def _require_crypto():
    """Ensure cryptography is available for crypto operations."""
    if not _HAS_CRYPTO:
        raise ImportError(
            "Cryptography features require optional dependencies. Install with: "
            "pip install 'provide-foundation[crypto]'"
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


if _HAS_CRYPTO:
    KeyPair: TypeAlias = rsa.RSAPrivateKey | ec.EllipticCurvePrivateKey
    PublicKey: TypeAlias = rsa.RSAPublicKey | ec.EllipticCurvePublicKey
else:
    KeyPair: TypeAlias = None
    PublicKey: TypeAlias = None


@define(slots=True, frozen=True)
class CertificateBase:
    """Immutable base certificate data."""

    subject: "x509.Name"
    issuer: "x509.Name"
    public_key: "PublicKey"
    not_valid_before: datetime
    not_valid_after: datetime
    serial_number: int

    @classmethod
    def create(cls, config: CertificateConfig) -> tuple[Self, "KeyPair"]:
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
                f"📜⏳✅ CertificateBase.create: Using validity: "
                f"{not_valid_before} to {not_valid_after}"
            )

            private_key: KeyPair
            match config["key_type"]:
                case KeyType.RSA:
                    key_size = config.get("key_size", DEFAULT_RSA_KEY_SIZE)
                    logger.debug(f"📜🔑🚀 Generating RSA key (size: {key_size})")
                    private_key = rsa.generate_private_key(
                        public_exponent=65537, key_size=key_size
                    )
                case KeyType.ECDSA:
                    curve_choice = config.get("curve", CurveType.SECP384R1)
                    logger.debug(f"📜🔑🚀 Generating ECDSA key (curve: {curve_choice})")
                    curve = getattr(ec, curve_choice.name)()
                    private_key = ec.generate_private_key(curve)
                case _:
                    raise ValueError(
                        f"Internal Error: Unsupported key type: {config['key_type']}"
                    )

            subject = cls._create_name(config["common_name"], config["organization"])
            issuer = cls._create_name(config["common_name"], config["organization"])

            serial_number = x509.random_serial_number()
            logger.debug(f"📜🔑✅ Generated serial number: {serial_number}")

            base = cls(
                subject=subject,
                issuer=issuer,
                public_key=private_key.public_key(),
                not_valid_before=not_valid_before,
                not_valid_after=not_valid_after,
                serial_number=serial_number,
            )
            logger.debug("📜📝✅ CertificateBase.create: Base creation complete")
            return base, private_key

        except Exception as e:
            logger.error(
                f"📜❌ CertificateBase.create: Failed: {e}",
                extra={"error": str(e), "trace": traceback.format_exc()},
            )
            raise CertificateError(f"Failed to generate certificate base: {e}") from e

    @staticmethod
    def _create_name(common_name: str, org: str) -> "x509.Name":
        """Helper method to construct an X.509 name."""
        return x509.Name(
            [
                x509.NameAttribute(NameOID.COMMON_NAME, common_name),
                x509.NameAttribute(NameOID.ORGANIZATION_NAME, org),
            ]
        )