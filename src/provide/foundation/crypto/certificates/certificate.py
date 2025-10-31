#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from __future__ import annotations

from datetime import UTC, datetime
from functools import cached_property
from typing import TYPE_CHECKING, Self

from attrs import define, field

if TYPE_CHECKING:
    from cryptography import x509
    from cryptography.hazmat.primitives.asymmetric import ec, rsa
    from cryptography.x509 import Certificate as X509Certificate

try:
    from cryptography import x509
    from cryptography.hazmat.primitives.asymmetric import ec, rsa
    from cryptography.x509 import Certificate as X509Certificate

    _HAS_CRYPTO = True
except ImportError:
    _HAS_CRYPTO = False

from provide.foundation import logger
from provide.foundation.crypto.certificates.base import (
    CertificateBase,
    PublicKey,
)
from provide.foundation.crypto.certificates.generator import generate_certificate
from provide.foundation.crypto.certificates.loader import load_certificate_from_pem
from provide.foundation.crypto.certificates.operations import create_x509_certificate
from provide.foundation.crypto.certificates.trust import (
    verify_trust as verify_trust_impl,
)
from provide.foundation.crypto.defaults import (
    DEFAULT_CERTIFICATE_COMMON_NAME,
    DEFAULT_CERTIFICATE_CURVE,
    DEFAULT_CERTIFICATE_KEY_TYPE,
    DEFAULT_CERTIFICATE_ORGANIZATION_NAME,
    DEFAULT_CERTIFICATE_VALIDITY_DAYS,
    DEFAULT_RSA_KEY_SIZE,
    default_certificate_alt_names,
)

"""Main Certificate class."""

# Type alias for keypair types
if TYPE_CHECKING:
    from typing import TypeAlias

    KeyPair: TypeAlias = rsa.RSAPrivateKey | ec.EllipticCurvePrivateKey | None
elif _HAS_CRYPTO:
    KeyPair = rsa.RSAPrivateKey | ec.EllipticCurvePrivateKey | None  # type: ignore[misc]
else:
    KeyPair = None  # type: ignore[misc,assignment]


@define(slots=True, eq=False, hash=False, repr=False)
class Certificate:
    """X.509 certificate management using attrs.

    This class should be instantiated via factory methods:
    - Certificate.from_pem() - Load from PEM strings
    - Certificate.generate() - Generate new certificate
    - Certificate.create_ca() - Generate CA certificate
    - Certificate.create_signed_certificate() - Generate signed certificate
    - Certificate.create_self_signed_server_cert() - Generate self-signed server cert
    - Certificate.create_self_signed_client_cert() - Generate self-signed client cert
    """

    # Core certificate components - required for initialization
    _base: CertificateBase = field(repr=False, alias="_base")
    _cert: X509Certificate = field(repr=False, alias="_cert")
    _private_key: KeyPair | None = field(repr=False, alias="_private_key")
    cert_pem: str = field(repr=True)
    key_pem: str | None = field(repr=False)

    # Certificate metadata
    common_name: str = field(kw_only=True)
    organization_name: str = field(kw_only=True)
    validity_days: int = field(kw_only=True)
    key_type: str = field(kw_only=True)
    key_size: int = field(default=DEFAULT_RSA_KEY_SIZE, kw_only=True)
    ecdsa_curve: str = field(default=DEFAULT_CERTIFICATE_CURVE, kw_only=True)
    alt_names: list[str] | None = field(default=None, kw_only=True)

    # Trust chain
    _trust_chain: list[Certificate] = field(init=False, factory=list, repr=False)

    # Properties
    @property
    def trust_chain(self) -> list[Certificate]:
        """Returns the list of trusted certificates associated with this one."""
        return self._trust_chain

    @trust_chain.setter
    def trust_chain(self, value: list[Certificate]) -> None:
        """Sets the list of trusted certificates."""
        self._trust_chain = value

    @cached_property
    def is_valid(self) -> bool:
        """Checks if the certificate is currently valid based on its dates."""
        if not hasattr(self, "_base"):
            return False
        now = datetime.now(UTC)
        valid = self._base.not_valid_before <= now <= self._base.not_valid_after
        return valid

    @property
    def is_ca(self) -> bool:
        """Checks if the certificate has the Basic Constraints CA flag set to True."""
        if not hasattr(self, "_cert"):
            return False
        try:
            ext = self._cert.extensions.get_extension_for_oid(x509.oid.ExtensionOID.BASIC_CONSTRAINTS)
            if isinstance(ext.value, x509.BasicConstraints):
                return ext.value.ca
            return False
        except x509.ExtensionNotFound:
            logger.debug("📜🔍⚠️ is_ca: Basic Constraints extension not found")
            return False

    @property
    def subject(self) -> str:
        """Returns the certificate subject as an RFC4514 string."""
        if not hasattr(self, "_base"):
            return "SubjectNotInitialized"
        return self._base.subject.rfc4514_string()

    @property
    def issuer(self) -> str:
        """Returns the certificate issuer as an RFC4514 string."""
        if not hasattr(self, "_base"):
            return "IssuerNotInitialized"
        return self._base.issuer.rfc4514_string()

    @property
    def public_key(self) -> PublicKey | None:
        """Returns the public key object from the certificate."""
        if not hasattr(self, "_base"):
            return None
        return self._base.public_key

    @property
    def serial_number(self) -> int | None:
        """Returns the certificate serial number."""
        if not hasattr(self, "_base"):
            return None
        return self._base.serial_number

    # Primary factory methods for explicit initialization
    @classmethod
    def from_pem(cls, cert_pem: str, key_pem: str | None = None) -> Certificate:
        """Load certificate from PEM strings.

        Args:
            cert_pem: Certificate in PEM format (string or URI)
            key_pem: Optional private key in PEM format (string or URI)

        Returns:
            Certificate instance

        Raises:
            CertificateError: If loading fails

        Example:
            >>> cert = Certificate.from_pem(cert_pem_string, key_pem_string)
            >>> assert cert.is_valid
        """
        base, x509_cert, private_key, cert_pem_str, key_pem_str = load_certificate_from_pem(
            cert_pem,
            key_pem,
        )

        # Extract metadata from x509 cert subject
        try:
            cn_attr = x509_cert.subject.get_attributes_for_oid(x509.oid.NameOID.COMMON_NAME)[0]
            common_name = cn_attr.value
        except (IndexError, AttributeError):
            common_name = "Unknown"

        try:
            org_attr = x509_cert.subject.get_attributes_for_oid(x509.oid.NameOID.ORGANIZATION_NAME)[0]
            organization_name = org_attr.value
        except (IndexError, AttributeError):
            organization_name = "Unknown"

        # Calculate validity days from certificate dates
        validity_delta = base.not_valid_after - base.not_valid_before
        validity_days = validity_delta.days

        # Determine key type from public key
        if isinstance(base.public_key, rsa.RSAPublicKey):
            key_type = "rsa"
        elif isinstance(base.public_key, ec.EllipticCurvePublicKey):
            key_type = "ecdsa"
        else:
            key_type = "unknown"

        return cls(
            _base=base,
            _cert=x509_cert,
            _private_key=private_key,
            cert_pem=cert_pem_str,
            key_pem=key_pem_str,
            common_name=common_name,
            organization_name=organization_name,
            validity_days=validity_days,
            key_type=key_type,
        )

    @classmethod
    def generate(
        cls,
        common_name: str = DEFAULT_CERTIFICATE_COMMON_NAME,
        organization_name: str = DEFAULT_CERTIFICATE_ORGANIZATION_NAME,
        validity_days: int = DEFAULT_CERTIFICATE_VALIDITY_DAYS,
        key_type: str = DEFAULT_CERTIFICATE_KEY_TYPE,
        key_size: int = DEFAULT_RSA_KEY_SIZE,
        ecdsa_curve: str = DEFAULT_CERTIFICATE_CURVE,
        alt_names: list[str] | None = None,
        is_ca: bool = False,
        is_client_cert: bool = True,
    ) -> Certificate:
        """Generate a new certificate with a new keypair.

        Args:
            common_name: Certificate common name
            organization_name: Organization name
            validity_days: Number of days certificate is valid
            key_type: Key type ("rsa" or "ecdsa")
            key_size: RSA key size in bits
            ecdsa_curve: ECDSA curve name
            alt_names: Subject alternative names
            is_ca: Whether this is a CA certificate
            is_client_cert: Whether this is a client certificate

        Returns:
            New Certificate instance

        Example:
            >>> cert = Certificate.generate(
            ...     common_name="example.com",
            ...     organization_name="Example Corp",
            ... )
            >>> assert cert._private_key is not None
        """
        alt_names = alt_names or default_certificate_alt_names()

        base, x509_cert, private_key, cert_pem, key_pem = generate_certificate(
            common_name=common_name,
            organization_name=organization_name,
            validity_days=validity_days,
            key_type=key_type,
            key_size=key_size,
            ecdsa_curve=ecdsa_curve,
            alt_names=alt_names,
            is_ca=is_ca,
            is_client_cert=is_client_cert,
        )

        return cls(
            _base=base,
            _cert=x509_cert,
            _private_key=private_key,
            cert_pem=cert_pem,
            key_pem=key_pem,
            common_name=common_name,
            organization_name=organization_name,
            validity_days=validity_days,
            key_type=key_type,
            key_size=key_size,
            ecdsa_curve=ecdsa_curve,
            alt_names=alt_names,
        )

    # Factory methods - delegates to factory.py
    @classmethod
    def create_ca(
        cls,
        common_name: str,
        organization_name: str,
        validity_days: int,
        key_type: str = DEFAULT_CERTIFICATE_KEY_TYPE,
        key_size: int = DEFAULT_RSA_KEY_SIZE,
        ecdsa_curve: str = DEFAULT_CERTIFICATE_CURVE,
    ) -> Certificate:
        """Creates a new self-signed CA certificate."""
        from provide.foundation.crypto.certificates.factory import create_ca_certificate

        return create_ca_certificate(
            common_name,
            organization_name,
            validity_days,
            key_type,
            key_size,
            ecdsa_curve,
        )

    @classmethod
    def create_signed_certificate(
        cls,
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
        from provide.foundation.crypto.certificates.factory import (
            create_signed_certificate,
        )

        return create_signed_certificate(
            ca_certificate,
            common_name,
            organization_name,
            validity_days,
            alt_names,
            key_type,
            key_size,
            ecdsa_curve,
            is_client_cert,
        )

    @classmethod
    def create_self_signed_server_cert(
        cls,
        common_name: str,
        organization_name: str,
        validity_days: int,
        alt_names: list[str] | None = None,
        key_type: str = DEFAULT_CERTIFICATE_KEY_TYPE,
        key_size: int = DEFAULT_RSA_KEY_SIZE,
        ecdsa_curve: str = DEFAULT_CERTIFICATE_CURVE,
    ) -> Certificate:
        """Creates a new self-signed end-entity certificate suitable for a server."""
        from provide.foundation.crypto.certificates.factory import (
            create_self_signed_server_cert,
        )

        return create_self_signed_server_cert(
            common_name,
            organization_name,
            validity_days,
            alt_names,
            key_type,
            key_size,
            ecdsa_curve,
        )

    @classmethod
    def create_self_signed_client_cert(
        cls,
        common_name: str,
        organization_name: str,
        validity_days: int,
        alt_names: list[str] | None = None,
        key_type: str = DEFAULT_CERTIFICATE_KEY_TYPE,
        key_size: int = DEFAULT_RSA_KEY_SIZE,
        ecdsa_curve: str = DEFAULT_CERTIFICATE_CURVE,
    ) -> Certificate:
        """Creates a new self-signed end-entity certificate suitable for a client."""
        from provide.foundation.crypto.certificates.factory import (
            create_self_signed_client_cert,
        )

        return create_self_signed_client_cert(
            common_name,
            organization_name,
            validity_days,
            alt_names,
            key_type,
            key_size,
            ecdsa_curve,
        )

    def verify_trust(self, other_cert: Self) -> bool:
        """Verifies if the `other_cert` is trusted based on this certificate's trust chain."""
        return verify_trust_impl(self, other_cert, self._trust_chain)

    def _create_x509_certificate(
        self,
        issuer_name_override: x509.Name | None = None,
        signing_key_override: KeyPair | None = None,
        is_ca: bool = False,
        is_client_cert: bool = False,
    ) -> X509Certificate:
        """Internal helper to build and sign the X.509 certificate object."""
        return create_x509_certificate(
            base=self._base,
            private_key=self._private_key,
            alt_names=self.alt_names,
            issuer_name_override=issuer_name_override,
            signing_key_override=signing_key_override,
            is_ca=is_ca,
            is_client_cert=is_client_cert,
        )

    def _validate_signature(self, signed_cert: Certificate, signing_cert: Certificate) -> bool:
        """Internal helper: Validates signature and issuer/subject match."""
        from provide.foundation.crypto.certificates.trust import (
            validate_signature_wrapper,
        )

        return validate_signature_wrapper(signed_cert, signing_cert)

    def __eq__(self, other: object) -> bool:
        """Custom equality based on subject and serial number."""
        if not isinstance(other, Certificate):
            return NotImplemented
        if not hasattr(self, "_base") or not hasattr(other, "_base"):
            return False
        eq = (
            self._base.subject == other._base.subject and self._base.serial_number == other._base.serial_number
        )
        return eq

    def __hash__(self) -> int:
        """Custom hash based on subject and serial number."""
        if not hasattr(self, "_base"):
            logger.warning("📜🔍⚠️ __hash__ called before _base initialized")
            return hash((None, None))

        h = hash((self._base.subject, self._base.serial_number))
        return h

    def __repr__(self) -> str:
        try:
            subject_str = self.subject
            issuer_str = self.issuer
            valid_str = str(self.is_valid)
            ca_str = str(self.is_ca)
        except AttributeError:
            subject_str = "PartiallyInitialized"
            issuer_str = "PartiallyInitialized"
            valid_str = "Unknown"
            ca_str = "Unknown"

        return (
            f"Certificate(subject='{subject_str}', issuer='{issuer_str}', "
            f"common_name='{self.common_name}', valid={valid_str}, ca={ca_str}, "
            f"key_type='{self.key_type}')"
        )


# 🧱🏗️🔚
