# provide/foundation/crypto/certificates/base.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

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
from inspect import signature as _mutmut_signature
from typing import Annotated
from typing import Callable
from typing import ClassVar


MutantDict = Annotated[dict[str, Callable], "Mutant"]


def _mutmut_trampoline(orig, mutants, call_args, call_kwargs, self_arg=None):
    """Forward call to original or mutated function, depending on the environment"""
    import os

    mutant_under_test = os.environ["MUTANT_UNDER_TEST"]
    if mutant_under_test == "fail":
        from mutmut.__main__ import MutmutProgrammaticFailException

        raise MutmutProgrammaticFailException("Failed programmatically")
    elif mutant_under_test == "stats":
        from mutmut.__main__ import record_trampoline_hit

        record_trampoline_hit(orig.__module__ + "." + orig.__name__)
        result = orig(*call_args, **call_kwargs)
        return result
    prefix = orig.__module__ + "." + orig.__name__ + "__mutmut_"
    if not mutant_under_test.startswith(prefix):
        result = orig(*call_args, **call_kwargs)
        return result
    mutant_name = mutant_under_test.rpartition(".")[-1]
    if self_arg:
        # call to a class method where self is not bound
        result = mutants[mutant_name](self_arg, *call_args, **call_kwargs)
    else:
        result = mutants[mutant_name](*call_args, **call_kwargs)
    return result


def x__require_crypto__mutmut_orig() -> None:
    """Ensure cryptography is available for crypto operations."""
    if not _HAS_CRYPTO:
        raise ImportError(
            "Cryptography features require optional dependencies. Install with: "
            "pip install 'provide-foundation[crypto]'",
        )


def x__require_crypto__mutmut_1() -> None:
    """Ensure cryptography is available for crypto operations."""
    if _HAS_CRYPTO:
        raise ImportError(
            "Cryptography features require optional dependencies. Install with: "
            "pip install 'provide-foundation[crypto]'",
        )


def x__require_crypto__mutmut_2() -> None:
    """Ensure cryptography is available for crypto operations."""
    if not _HAS_CRYPTO:
        raise ImportError(
            None,
        )


def x__require_crypto__mutmut_3() -> None:
    """Ensure cryptography is available for crypto operations."""
    if not _HAS_CRYPTO:
        raise ImportError(
            "XXCryptography features require optional dependencies. Install with: XX"
            "pip install 'provide-foundation[crypto]'",
        )


def x__require_crypto__mutmut_4() -> None:
    """Ensure cryptography is available for crypto operations."""
    if not _HAS_CRYPTO:
        raise ImportError(
            "cryptography features require optional dependencies. install with: "
            "pip install 'provide-foundation[crypto]'",
        )


def x__require_crypto__mutmut_5() -> None:
    """Ensure cryptography is available for crypto operations."""
    if not _HAS_CRYPTO:
        raise ImportError(
            "CRYPTOGRAPHY FEATURES REQUIRE OPTIONAL DEPENDENCIES. INSTALL WITH: "
            "pip install 'provide-foundation[crypto]'",
        )


def x__require_crypto__mutmut_6() -> None:
    """Ensure cryptography is available for crypto operations."""
    if not _HAS_CRYPTO:
        raise ImportError(
            "Cryptography features require optional dependencies. Install with: "
            "XXpip install 'provide-foundation[crypto]'XX",
        )


def x__require_crypto__mutmut_7() -> None:
    """Ensure cryptography is available for crypto operations."""
    if not _HAS_CRYPTO:
        raise ImportError(
            "Cryptography features require optional dependencies. Install with: "
            "PIP INSTALL 'PROVIDE-FOUNDATION[CRYPTO]'",
        )


x__require_crypto__mutmut_mutants: ClassVar[MutantDict] = {
    "x__require_crypto__mutmut_1": x__require_crypto__mutmut_1,
    "x__require_crypto__mutmut_2": x__require_crypto__mutmut_2,
    "x__require_crypto__mutmut_3": x__require_crypto__mutmut_3,
    "x__require_crypto__mutmut_4": x__require_crypto__mutmut_4,
    "x__require_crypto__mutmut_5": x__require_crypto__mutmut_5,
    "x__require_crypto__mutmut_6": x__require_crypto__mutmut_6,
    "x__require_crypto__mutmut_7": x__require_crypto__mutmut_7,
}


def _require_crypto(*args, **kwargs):
    result = _mutmut_trampoline(
        x__require_crypto__mutmut_orig, x__require_crypto__mutmut_mutants, args, kwargs
    )
    return result


_require_crypto.__signature__ = _mutmut_signature(x__require_crypto__mutmut_orig)
x__require_crypto__mutmut_orig.__name__ = "x__require_crypto"


class CertificateError(ValidationError):
    """Certificate-related errors."""

    def xǁCertificateErrorǁ__init____mutmut_orig(self, message: str, hint: str | None = None) -> None:
        super().__init__(
            message=message,
            field="certificate",
            value=None,
            rule=hint or "Certificate operation failed",
        )

    def xǁCertificateErrorǁ__init____mutmut_1(self, message: str, hint: str | None = None) -> None:
        super().__init__(
            message=None,
            field="certificate",
            value=None,
            rule=hint or "Certificate operation failed",
        )

    def xǁCertificateErrorǁ__init____mutmut_2(self, message: str, hint: str | None = None) -> None:
        super().__init__(
            message=message,
            field=None,
            value=None,
            rule=hint or "Certificate operation failed",
        )

    def xǁCertificateErrorǁ__init____mutmut_3(self, message: str, hint: str | None = None) -> None:
        super().__init__(
            message=message,
            field="certificate",
            value=None,
            rule=None,
        )

    def xǁCertificateErrorǁ__init____mutmut_4(self, message: str, hint: str | None = None) -> None:
        super().__init__(
            field="certificate",
            value=None,
            rule=hint or "Certificate operation failed",
        )

    def xǁCertificateErrorǁ__init____mutmut_5(self, message: str, hint: str | None = None) -> None:
        super().__init__(
            message=message,
            value=None,
            rule=hint or "Certificate operation failed",
        )

    def xǁCertificateErrorǁ__init____mutmut_6(self, message: str, hint: str | None = None) -> None:
        super().__init__(
            message=message,
            field="certificate",
            rule=hint or "Certificate operation failed",
        )

    def xǁCertificateErrorǁ__init____mutmut_7(self, message: str, hint: str | None = None) -> None:
        super().__init__(
            message=message,
            field="certificate",
            value=None,
        )

    def xǁCertificateErrorǁ__init____mutmut_8(self, message: str, hint: str | None = None) -> None:
        super().__init__(
            message=message,
            field="XXcertificateXX",
            value=None,
            rule=hint or "Certificate operation failed",
        )

    def xǁCertificateErrorǁ__init____mutmut_9(self, message: str, hint: str | None = None) -> None:
        super().__init__(
            message=message,
            field="CERTIFICATE",
            value=None,
            rule=hint or "Certificate operation failed",
        )

    def xǁCertificateErrorǁ__init____mutmut_10(self, message: str, hint: str | None = None) -> None:
        super().__init__(
            message=message,
            field="certificate",
            value=None,
            rule=hint and "Certificate operation failed",
        )

    def xǁCertificateErrorǁ__init____mutmut_11(self, message: str, hint: str | None = None) -> None:
        super().__init__(
            message=message,
            field="certificate",
            value=None,
            rule=hint or "XXCertificate operation failedXX",
        )

    def xǁCertificateErrorǁ__init____mutmut_12(self, message: str, hint: str | None = None) -> None:
        super().__init__(
            message=message,
            field="certificate",
            value=None,
            rule=hint or "certificate operation failed",
        )

    def xǁCertificateErrorǁ__init____mutmut_13(self, message: str, hint: str | None = None) -> None:
        super().__init__(
            message=message,
            field="certificate",
            value=None,
            rule=hint or "CERTIFICATE OPERATION FAILED",
        )

    xǁCertificateErrorǁ__init____mutmut_mutants: ClassVar[MutantDict] = {
        "xǁCertificateErrorǁ__init____mutmut_1": xǁCertificateErrorǁ__init____mutmut_1,
        "xǁCertificateErrorǁ__init____mutmut_2": xǁCertificateErrorǁ__init____mutmut_2,
        "xǁCertificateErrorǁ__init____mutmut_3": xǁCertificateErrorǁ__init____mutmut_3,
        "xǁCertificateErrorǁ__init____mutmut_4": xǁCertificateErrorǁ__init____mutmut_4,
        "xǁCertificateErrorǁ__init____mutmut_5": xǁCertificateErrorǁ__init____mutmut_5,
        "xǁCertificateErrorǁ__init____mutmut_6": xǁCertificateErrorǁ__init____mutmut_6,
        "xǁCertificateErrorǁ__init____mutmut_7": xǁCertificateErrorǁ__init____mutmut_7,
        "xǁCertificateErrorǁ__init____mutmut_8": xǁCertificateErrorǁ__init____mutmut_8,
        "xǁCertificateErrorǁ__init____mutmut_9": xǁCertificateErrorǁ__init____mutmut_9,
        "xǁCertificateErrorǁ__init____mutmut_10": xǁCertificateErrorǁ__init____mutmut_10,
        "xǁCertificateErrorǁ__init____mutmut_11": xǁCertificateErrorǁ__init____mutmut_11,
        "xǁCertificateErrorǁ__init____mutmut_12": xǁCertificateErrorǁ__init____mutmut_12,
        "xǁCertificateErrorǁ__init____mutmut_13": xǁCertificateErrorǁ__init____mutmut_13,
    }

    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁCertificateErrorǁ__init____mutmut_orig"),
            object.__getattribute__(self, "xǁCertificateErrorǁ__init____mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    __init__.__signature__ = _mutmut_signature(xǁCertificateErrorǁ__init____mutmut_orig)
    xǁCertificateErrorǁ__init____mutmut_orig.__name__ = "xǁCertificateErrorǁ__init__"


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
                f"📜⏳✅ CertificateBase.create: Using validity: {not_valid_before} to {not_valid_after}",
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
    def _create_name(common_name: str, org: str) -> x509.Name:
        """Helper method to construct an X.509 name."""
        return x509.Name(
            [
                x509.NameAttribute(NameOID.COMMON_NAME, common_name),
                x509.NameAttribute(NameOID.ORGANIZATION_NAME, org),
            ],
        )


# <3 🧱🤝🔒🪄
