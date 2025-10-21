# provide/foundation/crypto/certificates/operations.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

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
from inspect import signature as _mutmut_signature
from typing import Annotated
from typing import Callable
from typing import ClassVar


MutantDict = Annotated[dict[str, Callable], "Mutant"]


def _mutmut_trampoline(orig, mutants, call_args, call_kwargs, self_arg = None):
    """Forward call to original or mutated function, depending on the environment"""
    import os
    mutant_under_test = os.environ['MUTANT_UNDER_TEST']
    if mutant_under_test == 'fail':
        from mutmut.__main__ import MutmutProgrammaticFailException
        raise MutmutProgrammaticFailException('Failed programmatically')      
    elif mutant_under_test == 'stats':
        from mutmut.__main__ import record_trampoline_hit
        record_trampoline_hit(orig.__module__ + '.' + orig.__name__)
        result = orig(*call_args, **call_kwargs)
        return result
    prefix = orig.__module__ + '.' + orig.__name__ + '__mutmut_'
    if not mutant_under_test.startswith(prefix):
        result = orig(*call_args, **call_kwargs)
        return result
    mutant_name = mutant_under_test.rpartition('.')[-1]
    if self_arg:
        # call to a class method where self is not bound
        result = mutants[mutant_name](self_arg, *call_args, **call_kwargs)
    else:
        result = mutants[mutant_name](*call_args, **call_kwargs)
    return result


def x_create_x509_certificate__mutmut_orig(
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
            logger.debug(f"📜📝✅ Added SANs: {alt_names or []}")

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
            f"📜📝✅ Added BasicConstraints (is_ca={is_ca}), "
            f"KeyUsage, ExtendedKeyUsage (is_client_cert={is_client_cert})",
        )

        signed_cert = builder.sign(
            private_key=actual_signing_key,
            algorithm=hashes.SHA256(),
        )
        logger.debug("📜📝✅ Certificate signed successfully")
        return signed_cert

    except Exception as e:
        logger.error(
            f"📜❌ create_x509_certificate: Failed: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError("Failed to create X.509 certificate object") from e


def x_create_x509_certificate__mutmut_1(
    base: CertificateBase,
    private_key: KeyPair,
    alt_names: list[str] | None = None,
    issuer_name_override: x509.Name | None = None,
    signing_key_override: KeyPair | None = None,
    is_ca: bool = True,
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
            logger.debug(f"📜📝✅ Added SANs: {alt_names or []}")

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
            f"📜📝✅ Added BasicConstraints (is_ca={is_ca}), "
            f"KeyUsage, ExtendedKeyUsage (is_client_cert={is_client_cert})",
        )

        signed_cert = builder.sign(
            private_key=actual_signing_key,
            algorithm=hashes.SHA256(),
        )
        logger.debug("📜📝✅ Certificate signed successfully")
        return signed_cert

    except Exception as e:
        logger.error(
            f"📜❌ create_x509_certificate: Failed: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError("Failed to create X.509 certificate object") from e


def x_create_x509_certificate__mutmut_2(
    base: CertificateBase,
    private_key: KeyPair,
    alt_names: list[str] | None = None,
    issuer_name_override: x509.Name | None = None,
    signing_key_override: KeyPair | None = None,
    is_ca: bool = False,
    is_client_cert: bool = True,
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
            logger.debug(f"📜📝✅ Added SANs: {alt_names or []}")

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
            f"📜📝✅ Added BasicConstraints (is_ca={is_ca}), "
            f"KeyUsage, ExtendedKeyUsage (is_client_cert={is_client_cert})",
        )

        signed_cert = builder.sign(
            private_key=actual_signing_key,
            algorithm=hashes.SHA256(),
        )
        logger.debug("📜📝✅ Certificate signed successfully")
        return signed_cert

    except Exception as e:
        logger.error(
            f"📜❌ create_x509_certificate: Failed: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError("Failed to create X.509 certificate object") from e


def x_create_x509_certificate__mutmut_3(
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
        logger.debug(None)

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
            logger.debug(f"📜📝✅ Added SANs: {alt_names or []}")

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
            f"📜📝✅ Added BasicConstraints (is_ca={is_ca}), "
            f"KeyUsage, ExtendedKeyUsage (is_client_cert={is_client_cert})",
        )

        signed_cert = builder.sign(
            private_key=actual_signing_key,
            algorithm=hashes.SHA256(),
        )
        logger.debug("📜📝✅ Certificate signed successfully")
        return signed_cert

    except Exception as e:
        logger.error(
            f"📜❌ create_x509_certificate: Failed: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError("Failed to create X.509 certificate object") from e


def x_create_x509_certificate__mutmut_4(
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
        logger.debug("XX📜📝🚀 create_x509_certificate: Building certificateXX")

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
            logger.debug(f"📜📝✅ Added SANs: {alt_names or []}")

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
            f"📜📝✅ Added BasicConstraints (is_ca={is_ca}), "
            f"KeyUsage, ExtendedKeyUsage (is_client_cert={is_client_cert})",
        )

        signed_cert = builder.sign(
            private_key=actual_signing_key,
            algorithm=hashes.SHA256(),
        )
        logger.debug("📜📝✅ Certificate signed successfully")
        return signed_cert

    except Exception as e:
        logger.error(
            f"📜❌ create_x509_certificate: Failed: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError("Failed to create X.509 certificate object") from e


def x_create_x509_certificate__mutmut_5(
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
        logger.debug("📜📝🚀 create_x509_certificate: building certificate")

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
            logger.debug(f"📜📝✅ Added SANs: {alt_names or []}")

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
            f"📜📝✅ Added BasicConstraints (is_ca={is_ca}), "
            f"KeyUsage, ExtendedKeyUsage (is_client_cert={is_client_cert})",
        )

        signed_cert = builder.sign(
            private_key=actual_signing_key,
            algorithm=hashes.SHA256(),
        )
        logger.debug("📜📝✅ Certificate signed successfully")
        return signed_cert

    except Exception as e:
        logger.error(
            f"📜❌ create_x509_certificate: Failed: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError("Failed to create X.509 certificate object") from e


def x_create_x509_certificate__mutmut_6(
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
        logger.debug("📜📝🚀 CREATE_X509_CERTIFICATE: BUILDING CERTIFICATE")

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
            logger.debug(f"📜📝✅ Added SANs: {alt_names or []}")

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
            f"📜📝✅ Added BasicConstraints (is_ca={is_ca}), "
            f"KeyUsage, ExtendedKeyUsage (is_client_cert={is_client_cert})",
        )

        signed_cert = builder.sign(
            private_key=actual_signing_key,
            algorithm=hashes.SHA256(),
        )
        logger.debug("📜📝✅ Certificate signed successfully")
        return signed_cert

    except Exception as e:
        logger.error(
            f"📜❌ create_x509_certificate: Failed: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError("Failed to create X.509 certificate object") from e


def x_create_x509_certificate__mutmut_7(
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

        actual_issuer_name = None
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
            logger.debug(f"📜📝✅ Added SANs: {alt_names or []}")

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
            f"📜📝✅ Added BasicConstraints (is_ca={is_ca}), "
            f"KeyUsage, ExtendedKeyUsage (is_client_cert={is_client_cert})",
        )

        signed_cert = builder.sign(
            private_key=actual_signing_key,
            algorithm=hashes.SHA256(),
        )
        logger.debug("📜📝✅ Certificate signed successfully")
        return signed_cert

    except Exception as e:
        logger.error(
            f"📜❌ create_x509_certificate: Failed: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError("Failed to create X.509 certificate object") from e


def x_create_x509_certificate__mutmut_8(
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
        actual_signing_key = None

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
            logger.debug(f"📜📝✅ Added SANs: {alt_names or []}")

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
            f"📜📝✅ Added BasicConstraints (is_ca={is_ca}), "
            f"KeyUsage, ExtendedKeyUsage (is_client_cert={is_client_cert})",
        )

        signed_cert = builder.sign(
            private_key=actual_signing_key,
            algorithm=hashes.SHA256(),
        )
        logger.debug("📜📝✅ Certificate signed successfully")
        return signed_cert

    except Exception as e:
        logger.error(
            f"📜❌ create_x509_certificate: Failed: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError("Failed to create X.509 certificate object") from e


def x_create_x509_certificate__mutmut_9(
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

        if actual_signing_key:
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
            logger.debug(f"📜📝✅ Added SANs: {alt_names or []}")

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
            f"📜📝✅ Added BasicConstraints (is_ca={is_ca}), "
            f"KeyUsage, ExtendedKeyUsage (is_client_cert={is_client_cert})",
        )

        signed_cert = builder.sign(
            private_key=actual_signing_key,
            algorithm=hashes.SHA256(),
        )
        logger.debug("📜📝✅ Certificate signed successfully")
        return signed_cert

    except Exception as e:
        logger.error(
            f"📜❌ create_x509_certificate: Failed: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError("Failed to create X.509 certificate object") from e


def x_create_x509_certificate__mutmut_10(
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
            raise CertificateError(None)

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
            logger.debug(f"📜📝✅ Added SANs: {alt_names or []}")

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
            f"📜📝✅ Added BasicConstraints (is_ca={is_ca}), "
            f"KeyUsage, ExtendedKeyUsage (is_client_cert={is_client_cert})",
        )

        signed_cert = builder.sign(
            private_key=actual_signing_key,
            algorithm=hashes.SHA256(),
        )
        logger.debug("📜📝✅ Certificate signed successfully")
        return signed_cert

    except Exception as e:
        logger.error(
            f"📜❌ create_x509_certificate: Failed: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError("Failed to create X.509 certificate object") from e


def x_create_x509_certificate__mutmut_11(
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
            raise CertificateError("XXCannot sign certificate without a signing key (either own or override)XX")

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
            logger.debug(f"📜📝✅ Added SANs: {alt_names or []}")

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
            f"📜📝✅ Added BasicConstraints (is_ca={is_ca}), "
            f"KeyUsage, ExtendedKeyUsage (is_client_cert={is_client_cert})",
        )

        signed_cert = builder.sign(
            private_key=actual_signing_key,
            algorithm=hashes.SHA256(),
        )
        logger.debug("📜📝✅ Certificate signed successfully")
        return signed_cert

    except Exception as e:
        logger.error(
            f"📜❌ create_x509_certificate: Failed: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError("Failed to create X.509 certificate object") from e


def x_create_x509_certificate__mutmut_12(
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
            raise CertificateError("cannot sign certificate without a signing key (either own or override)")

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
            logger.debug(f"📜📝✅ Added SANs: {alt_names or []}")

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
            f"📜📝✅ Added BasicConstraints (is_ca={is_ca}), "
            f"KeyUsage, ExtendedKeyUsage (is_client_cert={is_client_cert})",
        )

        signed_cert = builder.sign(
            private_key=actual_signing_key,
            algorithm=hashes.SHA256(),
        )
        logger.debug("📜📝✅ Certificate signed successfully")
        return signed_cert

    except Exception as e:
        logger.error(
            f"📜❌ create_x509_certificate: Failed: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError("Failed to create X.509 certificate object") from e


def x_create_x509_certificate__mutmut_13(
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
            raise CertificateError("CANNOT SIGN CERTIFICATE WITHOUT A SIGNING KEY (EITHER OWN OR OVERRIDE)")

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
            logger.debug(f"📜📝✅ Added SANs: {alt_names or []}")

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
            f"📜📝✅ Added BasicConstraints (is_ca={is_ca}), "
            f"KeyUsage, ExtendedKeyUsage (is_client_cert={is_client_cert})",
        )

        signed_cert = builder.sign(
            private_key=actual_signing_key,
            algorithm=hashes.SHA256(),
        )
        logger.debug("📜📝✅ Certificate signed successfully")
        return signed_cert

    except Exception as e:
        logger.error(
            f"📜❌ create_x509_certificate: Failed: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError("Failed to create X.509 certificate object") from e


def x_create_x509_certificate__mutmut_14(
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

        builder = None

        san_list = [x509.DNSName(name) for name in (alt_names or []) if name]
        if san_list:
            # DNSName is a subtype of GeneralName, but mypy needs help understanding this
            builder = builder.add_extension(x509.SubjectAlternativeName(cast(list, san_list)), critical=False)
            logger.debug(f"📜📝✅ Added SANs: {alt_names or []}")

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
            f"📜📝✅ Added BasicConstraints (is_ca={is_ca}), "
            f"KeyUsage, ExtendedKeyUsage (is_client_cert={is_client_cert})",
        )

        signed_cert = builder.sign(
            private_key=actual_signing_key,
            algorithm=hashes.SHA256(),
        )
        logger.debug("📜📝✅ Certificate signed successfully")
        return signed_cert

    except Exception as e:
        logger.error(
            f"📜❌ create_x509_certificate: Failed: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError("Failed to create X.509 certificate object") from e


def x_create_x509_certificate__mutmut_15(
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
            .not_valid_after(None)
        )

        san_list = [x509.DNSName(name) for name in (alt_names or []) if name]
        if san_list:
            # DNSName is a subtype of GeneralName, but mypy needs help understanding this
            builder = builder.add_extension(x509.SubjectAlternativeName(cast(list, san_list)), critical=False)
            logger.debug(f"📜📝✅ Added SANs: {alt_names or []}")

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
            f"📜📝✅ Added BasicConstraints (is_ca={is_ca}), "
            f"KeyUsage, ExtendedKeyUsage (is_client_cert={is_client_cert})",
        )

        signed_cert = builder.sign(
            private_key=actual_signing_key,
            algorithm=hashes.SHA256(),
        )
        logger.debug("📜📝✅ Certificate signed successfully")
        return signed_cert

    except Exception as e:
        logger.error(
            f"📜❌ create_x509_certificate: Failed: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError("Failed to create X.509 certificate object") from e


def x_create_x509_certificate__mutmut_16(
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
            .not_valid_before(None)
            .not_valid_after(base.not_valid_after)
        )

        san_list = [x509.DNSName(name) for name in (alt_names or []) if name]
        if san_list:
            # DNSName is a subtype of GeneralName, but mypy needs help understanding this
            builder = builder.add_extension(x509.SubjectAlternativeName(cast(list, san_list)), critical=False)
            logger.debug(f"📜📝✅ Added SANs: {alt_names or []}")

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
            f"📜📝✅ Added BasicConstraints (is_ca={is_ca}), "
            f"KeyUsage, ExtendedKeyUsage (is_client_cert={is_client_cert})",
        )

        signed_cert = builder.sign(
            private_key=actual_signing_key,
            algorithm=hashes.SHA256(),
        )
        logger.debug("📜📝✅ Certificate signed successfully")
        return signed_cert

    except Exception as e:
        logger.error(
            f"📜❌ create_x509_certificate: Failed: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError("Failed to create X.509 certificate object") from e


def x_create_x509_certificate__mutmut_17(
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
            .serial_number(None)
            .not_valid_before(base.not_valid_before)
            .not_valid_after(base.not_valid_after)
        )

        san_list = [x509.DNSName(name) for name in (alt_names or []) if name]
        if san_list:
            # DNSName is a subtype of GeneralName, but mypy needs help understanding this
            builder = builder.add_extension(x509.SubjectAlternativeName(cast(list, san_list)), critical=False)
            logger.debug(f"📜📝✅ Added SANs: {alt_names or []}")

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
            f"📜📝✅ Added BasicConstraints (is_ca={is_ca}), "
            f"KeyUsage, ExtendedKeyUsage (is_client_cert={is_client_cert})",
        )

        signed_cert = builder.sign(
            private_key=actual_signing_key,
            algorithm=hashes.SHA256(),
        )
        logger.debug("📜📝✅ Certificate signed successfully")
        return signed_cert

    except Exception as e:
        logger.error(
            f"📜❌ create_x509_certificate: Failed: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError("Failed to create X.509 certificate object") from e


def x_create_x509_certificate__mutmut_18(
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
            .public_key(None)
            .serial_number(base.serial_number)
            .not_valid_before(base.not_valid_before)
            .not_valid_after(base.not_valid_after)
        )

        san_list = [x509.DNSName(name) for name in (alt_names or []) if name]
        if san_list:
            # DNSName is a subtype of GeneralName, but mypy needs help understanding this
            builder = builder.add_extension(x509.SubjectAlternativeName(cast(list, san_list)), critical=False)
            logger.debug(f"📜📝✅ Added SANs: {alt_names or []}")

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
            f"📜📝✅ Added BasicConstraints (is_ca={is_ca}), "
            f"KeyUsage, ExtendedKeyUsage (is_client_cert={is_client_cert})",
        )

        signed_cert = builder.sign(
            private_key=actual_signing_key,
            algorithm=hashes.SHA256(),
        )
        logger.debug("📜📝✅ Certificate signed successfully")
        return signed_cert

    except Exception as e:
        logger.error(
            f"📜❌ create_x509_certificate: Failed: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError("Failed to create X.509 certificate object") from e


def x_create_x509_certificate__mutmut_19(
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
            .issuer_name(None)
            .public_key(base.public_key)
            .serial_number(base.serial_number)
            .not_valid_before(base.not_valid_before)
            .not_valid_after(base.not_valid_after)
        )

        san_list = [x509.DNSName(name) for name in (alt_names or []) if name]
        if san_list:
            # DNSName is a subtype of GeneralName, but mypy needs help understanding this
            builder = builder.add_extension(x509.SubjectAlternativeName(cast(list, san_list)), critical=False)
            logger.debug(f"📜📝✅ Added SANs: {alt_names or []}")

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
            f"📜📝✅ Added BasicConstraints (is_ca={is_ca}), "
            f"KeyUsage, ExtendedKeyUsage (is_client_cert={is_client_cert})",
        )

        signed_cert = builder.sign(
            private_key=actual_signing_key,
            algorithm=hashes.SHA256(),
        )
        logger.debug("📜📝✅ Certificate signed successfully")
        return signed_cert

    except Exception as e:
        logger.error(
            f"📜❌ create_x509_certificate: Failed: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError("Failed to create X.509 certificate object") from e


def x_create_x509_certificate__mutmut_20(
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
            .subject_name(None)
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
            logger.debug(f"📜📝✅ Added SANs: {alt_names or []}")

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
            f"📜📝✅ Added BasicConstraints (is_ca={is_ca}), "
            f"KeyUsage, ExtendedKeyUsage (is_client_cert={is_client_cert})",
        )

        signed_cert = builder.sign(
            private_key=actual_signing_key,
            algorithm=hashes.SHA256(),
        )
        logger.debug("📜📝✅ Certificate signed successfully")
        return signed_cert

    except Exception as e:
        logger.error(
            f"📜❌ create_x509_certificate: Failed: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError("Failed to create X.509 certificate object") from e


def x_create_x509_certificate__mutmut_21(
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

        san_list = None
        if san_list:
            # DNSName is a subtype of GeneralName, but mypy needs help understanding this
            builder = builder.add_extension(x509.SubjectAlternativeName(cast(list, san_list)), critical=False)
            logger.debug(f"📜📝✅ Added SANs: {alt_names or []}")

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
            f"📜📝✅ Added BasicConstraints (is_ca={is_ca}), "
            f"KeyUsage, ExtendedKeyUsage (is_client_cert={is_client_cert})",
        )

        signed_cert = builder.sign(
            private_key=actual_signing_key,
            algorithm=hashes.SHA256(),
        )
        logger.debug("📜📝✅ Certificate signed successfully")
        return signed_cert

    except Exception as e:
        logger.error(
            f"📜❌ create_x509_certificate: Failed: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError("Failed to create X.509 certificate object") from e


def x_create_x509_certificate__mutmut_22(
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

        san_list = [x509.DNSName(None) for name in (alt_names or []) if name]
        if san_list:
            # DNSName is a subtype of GeneralName, but mypy needs help understanding this
            builder = builder.add_extension(x509.SubjectAlternativeName(cast(list, san_list)), critical=False)
            logger.debug(f"📜📝✅ Added SANs: {alt_names or []}")

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
            f"📜📝✅ Added BasicConstraints (is_ca={is_ca}), "
            f"KeyUsage, ExtendedKeyUsage (is_client_cert={is_client_cert})",
        )

        signed_cert = builder.sign(
            private_key=actual_signing_key,
            algorithm=hashes.SHA256(),
        )
        logger.debug("📜📝✅ Certificate signed successfully")
        return signed_cert

    except Exception as e:
        logger.error(
            f"📜❌ create_x509_certificate: Failed: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError("Failed to create X.509 certificate object") from e


def x_create_x509_certificate__mutmut_23(
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

        san_list = [x509.DNSName(name) for name in (alt_names and []) if name]
        if san_list:
            # DNSName is a subtype of GeneralName, but mypy needs help understanding this
            builder = builder.add_extension(x509.SubjectAlternativeName(cast(list, san_list)), critical=False)
            logger.debug(f"📜📝✅ Added SANs: {alt_names or []}")

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
            f"📜📝✅ Added BasicConstraints (is_ca={is_ca}), "
            f"KeyUsage, ExtendedKeyUsage (is_client_cert={is_client_cert})",
        )

        signed_cert = builder.sign(
            private_key=actual_signing_key,
            algorithm=hashes.SHA256(),
        )
        logger.debug("📜📝✅ Certificate signed successfully")
        return signed_cert

    except Exception as e:
        logger.error(
            f"📜❌ create_x509_certificate: Failed: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError("Failed to create X.509 certificate object") from e


def x_create_x509_certificate__mutmut_24(
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
            builder = None
            logger.debug(f"📜📝✅ Added SANs: {alt_names or []}")

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
            f"📜📝✅ Added BasicConstraints (is_ca={is_ca}), "
            f"KeyUsage, ExtendedKeyUsage (is_client_cert={is_client_cert})",
        )

        signed_cert = builder.sign(
            private_key=actual_signing_key,
            algorithm=hashes.SHA256(),
        )
        logger.debug("📜📝✅ Certificate signed successfully")
        return signed_cert

    except Exception as e:
        logger.error(
            f"📜❌ create_x509_certificate: Failed: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError("Failed to create X.509 certificate object") from e


def x_create_x509_certificate__mutmut_25(
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
            builder = builder.add_extension(None, critical=False)
            logger.debug(f"📜📝✅ Added SANs: {alt_names or []}")

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
            f"📜📝✅ Added BasicConstraints (is_ca={is_ca}), "
            f"KeyUsage, ExtendedKeyUsage (is_client_cert={is_client_cert})",
        )

        signed_cert = builder.sign(
            private_key=actual_signing_key,
            algorithm=hashes.SHA256(),
        )
        logger.debug("📜📝✅ Certificate signed successfully")
        return signed_cert

    except Exception as e:
        logger.error(
            f"📜❌ create_x509_certificate: Failed: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError("Failed to create X.509 certificate object") from e


def x_create_x509_certificate__mutmut_26(
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
            builder = builder.add_extension(x509.SubjectAlternativeName(cast(list, san_list)), critical=None)
            logger.debug(f"📜📝✅ Added SANs: {alt_names or []}")

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
            f"📜📝✅ Added BasicConstraints (is_ca={is_ca}), "
            f"KeyUsage, ExtendedKeyUsage (is_client_cert={is_client_cert})",
        )

        signed_cert = builder.sign(
            private_key=actual_signing_key,
            algorithm=hashes.SHA256(),
        )
        logger.debug("📜📝✅ Certificate signed successfully")
        return signed_cert

    except Exception as e:
        logger.error(
            f"📜❌ create_x509_certificate: Failed: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError("Failed to create X.509 certificate object") from e


def x_create_x509_certificate__mutmut_27(
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
            builder = builder.add_extension(critical=False)
            logger.debug(f"📜📝✅ Added SANs: {alt_names or []}")

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
            f"📜📝✅ Added BasicConstraints (is_ca={is_ca}), "
            f"KeyUsage, ExtendedKeyUsage (is_client_cert={is_client_cert})",
        )

        signed_cert = builder.sign(
            private_key=actual_signing_key,
            algorithm=hashes.SHA256(),
        )
        logger.debug("📜📝✅ Certificate signed successfully")
        return signed_cert

    except Exception as e:
        logger.error(
            f"📜❌ create_x509_certificate: Failed: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError("Failed to create X.509 certificate object") from e


def x_create_x509_certificate__mutmut_28(
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
            builder = builder.add_extension(x509.SubjectAlternativeName(cast(list, san_list)), )
            logger.debug(f"📜📝✅ Added SANs: {alt_names or []}")

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
            f"📜📝✅ Added BasicConstraints (is_ca={is_ca}), "
            f"KeyUsage, ExtendedKeyUsage (is_client_cert={is_client_cert})",
        )

        signed_cert = builder.sign(
            private_key=actual_signing_key,
            algorithm=hashes.SHA256(),
        )
        logger.debug("📜📝✅ Certificate signed successfully")
        return signed_cert

    except Exception as e:
        logger.error(
            f"📜❌ create_x509_certificate: Failed: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError("Failed to create X.509 certificate object") from e


def x_create_x509_certificate__mutmut_29(
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
            builder = builder.add_extension(x509.SubjectAlternativeName(None), critical=False)
            logger.debug(f"📜📝✅ Added SANs: {alt_names or []}")

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
            f"📜📝✅ Added BasicConstraints (is_ca={is_ca}), "
            f"KeyUsage, ExtendedKeyUsage (is_client_cert={is_client_cert})",
        )

        signed_cert = builder.sign(
            private_key=actual_signing_key,
            algorithm=hashes.SHA256(),
        )
        logger.debug("📜📝✅ Certificate signed successfully")
        return signed_cert

    except Exception as e:
        logger.error(
            f"📜❌ create_x509_certificate: Failed: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError("Failed to create X.509 certificate object") from e


def x_create_x509_certificate__mutmut_30(
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
            builder = builder.add_extension(x509.SubjectAlternativeName(cast(None, san_list)), critical=False)
            logger.debug(f"📜📝✅ Added SANs: {alt_names or []}")

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
            f"📜📝✅ Added BasicConstraints (is_ca={is_ca}), "
            f"KeyUsage, ExtendedKeyUsage (is_client_cert={is_client_cert})",
        )

        signed_cert = builder.sign(
            private_key=actual_signing_key,
            algorithm=hashes.SHA256(),
        )
        logger.debug("📜📝✅ Certificate signed successfully")
        return signed_cert

    except Exception as e:
        logger.error(
            f"📜❌ create_x509_certificate: Failed: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError("Failed to create X.509 certificate object") from e


def x_create_x509_certificate__mutmut_31(
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
            builder = builder.add_extension(x509.SubjectAlternativeName(cast(list, None)), critical=False)
            logger.debug(f"📜📝✅ Added SANs: {alt_names or []}")

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
            f"📜📝✅ Added BasicConstraints (is_ca={is_ca}), "
            f"KeyUsage, ExtendedKeyUsage (is_client_cert={is_client_cert})",
        )

        signed_cert = builder.sign(
            private_key=actual_signing_key,
            algorithm=hashes.SHA256(),
        )
        logger.debug("📜📝✅ Certificate signed successfully")
        return signed_cert

    except Exception as e:
        logger.error(
            f"📜❌ create_x509_certificate: Failed: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError("Failed to create X.509 certificate object") from e


def x_create_x509_certificate__mutmut_32(
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
            builder = builder.add_extension(x509.SubjectAlternativeName(cast(san_list)), critical=False)
            logger.debug(f"📜📝✅ Added SANs: {alt_names or []}")

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
            f"📜📝✅ Added BasicConstraints (is_ca={is_ca}), "
            f"KeyUsage, ExtendedKeyUsage (is_client_cert={is_client_cert})",
        )

        signed_cert = builder.sign(
            private_key=actual_signing_key,
            algorithm=hashes.SHA256(),
        )
        logger.debug("📜📝✅ Certificate signed successfully")
        return signed_cert

    except Exception as e:
        logger.error(
            f"📜❌ create_x509_certificate: Failed: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError("Failed to create X.509 certificate object") from e


def x_create_x509_certificate__mutmut_33(
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
            builder = builder.add_extension(x509.SubjectAlternativeName(cast(list, )), critical=False)
            logger.debug(f"📜📝✅ Added SANs: {alt_names or []}")

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
            f"📜📝✅ Added BasicConstraints (is_ca={is_ca}), "
            f"KeyUsage, ExtendedKeyUsage (is_client_cert={is_client_cert})",
        )

        signed_cert = builder.sign(
            private_key=actual_signing_key,
            algorithm=hashes.SHA256(),
        )
        logger.debug("📜📝✅ Certificate signed successfully")
        return signed_cert

    except Exception as e:
        logger.error(
            f"📜❌ create_x509_certificate: Failed: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError("Failed to create X.509 certificate object") from e


def x_create_x509_certificate__mutmut_34(
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
            builder = builder.add_extension(x509.SubjectAlternativeName(cast(list, san_list)), critical=True)
            logger.debug(f"📜📝✅ Added SANs: {alt_names or []}")

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
            f"📜📝✅ Added BasicConstraints (is_ca={is_ca}), "
            f"KeyUsage, ExtendedKeyUsage (is_client_cert={is_client_cert})",
        )

        signed_cert = builder.sign(
            private_key=actual_signing_key,
            algorithm=hashes.SHA256(),
        )
        logger.debug("📜📝✅ Certificate signed successfully")
        return signed_cert

    except Exception as e:
        logger.error(
            f"📜❌ create_x509_certificate: Failed: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError("Failed to create X.509 certificate object") from e


def x_create_x509_certificate__mutmut_35(
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
            logger.debug(None)

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
            f"📜📝✅ Added BasicConstraints (is_ca={is_ca}), "
            f"KeyUsage, ExtendedKeyUsage (is_client_cert={is_client_cert})",
        )

        signed_cert = builder.sign(
            private_key=actual_signing_key,
            algorithm=hashes.SHA256(),
        )
        logger.debug("📜📝✅ Certificate signed successfully")
        return signed_cert

    except Exception as e:
        logger.error(
            f"📜❌ create_x509_certificate: Failed: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError("Failed to create X.509 certificate object") from e


def x_create_x509_certificate__mutmut_36(
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
            logger.debug(f"📜📝✅ Added SANs: {alt_names and []}")

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
            f"📜📝✅ Added BasicConstraints (is_ca={is_ca}), "
            f"KeyUsage, ExtendedKeyUsage (is_client_cert={is_client_cert})",
        )

        signed_cert = builder.sign(
            private_key=actual_signing_key,
            algorithm=hashes.SHA256(),
        )
        logger.debug("📜📝✅ Certificate signed successfully")
        return signed_cert

    except Exception as e:
        logger.error(
            f"📜❌ create_x509_certificate: Failed: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError("Failed to create X.509 certificate object") from e


def x_create_x509_certificate__mutmut_37(
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
            logger.debug(f"📜📝✅ Added SANs: {alt_names or []}")

        builder = None

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
            f"📜📝✅ Added BasicConstraints (is_ca={is_ca}), "
            f"KeyUsage, ExtendedKeyUsage (is_client_cert={is_client_cert})",
        )

        signed_cert = builder.sign(
            private_key=actual_signing_key,
            algorithm=hashes.SHA256(),
        )
        logger.debug("📜📝✅ Certificate signed successfully")
        return signed_cert

    except Exception as e:
        logger.error(
            f"📜❌ create_x509_certificate: Failed: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError("Failed to create X.509 certificate object") from e


def x_create_x509_certificate__mutmut_38(
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
            logger.debug(f"📜📝✅ Added SANs: {alt_names or []}")

        builder = builder.add_extension(
            None,
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
            f"📜📝✅ Added BasicConstraints (is_ca={is_ca}), "
            f"KeyUsage, ExtendedKeyUsage (is_client_cert={is_client_cert})",
        )

        signed_cert = builder.sign(
            private_key=actual_signing_key,
            algorithm=hashes.SHA256(),
        )
        logger.debug("📜📝✅ Certificate signed successfully")
        return signed_cert

    except Exception as e:
        logger.error(
            f"📜❌ create_x509_certificate: Failed: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError("Failed to create X.509 certificate object") from e


def x_create_x509_certificate__mutmut_39(
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
            logger.debug(f"📜📝✅ Added SANs: {alt_names or []}")

        builder = builder.add_extension(
            x509.BasicConstraints(ca=is_ca, path_length=None),
            critical=None,
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
            f"📜📝✅ Added BasicConstraints (is_ca={is_ca}), "
            f"KeyUsage, ExtendedKeyUsage (is_client_cert={is_client_cert})",
        )

        signed_cert = builder.sign(
            private_key=actual_signing_key,
            algorithm=hashes.SHA256(),
        )
        logger.debug("📜📝✅ Certificate signed successfully")
        return signed_cert

    except Exception as e:
        logger.error(
            f"📜❌ create_x509_certificate: Failed: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError("Failed to create X.509 certificate object") from e


def x_create_x509_certificate__mutmut_40(
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
            logger.debug(f"📜📝✅ Added SANs: {alt_names or []}")

        builder = builder.add_extension(
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
            f"📜📝✅ Added BasicConstraints (is_ca={is_ca}), "
            f"KeyUsage, ExtendedKeyUsage (is_client_cert={is_client_cert})",
        )

        signed_cert = builder.sign(
            private_key=actual_signing_key,
            algorithm=hashes.SHA256(),
        )
        logger.debug("📜📝✅ Certificate signed successfully")
        return signed_cert

    except Exception as e:
        logger.error(
            f"📜❌ create_x509_certificate: Failed: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError("Failed to create X.509 certificate object") from e


def x_create_x509_certificate__mutmut_41(
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
            logger.debug(f"📜📝✅ Added SANs: {alt_names or []}")

        builder = builder.add_extension(
            x509.BasicConstraints(ca=is_ca, path_length=None),
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
            f"📜📝✅ Added BasicConstraints (is_ca={is_ca}), "
            f"KeyUsage, ExtendedKeyUsage (is_client_cert={is_client_cert})",
        )

        signed_cert = builder.sign(
            private_key=actual_signing_key,
            algorithm=hashes.SHA256(),
        )
        logger.debug("📜📝✅ Certificate signed successfully")
        return signed_cert

    except Exception as e:
        logger.error(
            f"📜❌ create_x509_certificate: Failed: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError("Failed to create X.509 certificate object") from e


def x_create_x509_certificate__mutmut_42(
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
            logger.debug(f"📜📝✅ Added SANs: {alt_names or []}")

        builder = builder.add_extension(
            x509.BasicConstraints(ca=None, path_length=None),
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
            f"📜📝✅ Added BasicConstraints (is_ca={is_ca}), "
            f"KeyUsage, ExtendedKeyUsage (is_client_cert={is_client_cert})",
        )

        signed_cert = builder.sign(
            private_key=actual_signing_key,
            algorithm=hashes.SHA256(),
        )
        logger.debug("📜📝✅ Certificate signed successfully")
        return signed_cert

    except Exception as e:
        logger.error(
            f"📜❌ create_x509_certificate: Failed: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError("Failed to create X.509 certificate object") from e


def x_create_x509_certificate__mutmut_43(
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
            logger.debug(f"📜📝✅ Added SANs: {alt_names or []}")

        builder = builder.add_extension(
            x509.BasicConstraints(path_length=None),
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
            f"📜📝✅ Added BasicConstraints (is_ca={is_ca}), "
            f"KeyUsage, ExtendedKeyUsage (is_client_cert={is_client_cert})",
        )

        signed_cert = builder.sign(
            private_key=actual_signing_key,
            algorithm=hashes.SHA256(),
        )
        logger.debug("📜📝✅ Certificate signed successfully")
        return signed_cert

    except Exception as e:
        logger.error(
            f"📜❌ create_x509_certificate: Failed: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError("Failed to create X.509 certificate object") from e


def x_create_x509_certificate__mutmut_44(
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
            logger.debug(f"📜📝✅ Added SANs: {alt_names or []}")

        builder = builder.add_extension(
            x509.BasicConstraints(ca=is_ca, ),
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
            f"📜📝✅ Added BasicConstraints (is_ca={is_ca}), "
            f"KeyUsage, ExtendedKeyUsage (is_client_cert={is_client_cert})",
        )

        signed_cert = builder.sign(
            private_key=actual_signing_key,
            algorithm=hashes.SHA256(),
        )
        logger.debug("📜📝✅ Certificate signed successfully")
        return signed_cert

    except Exception as e:
        logger.error(
            f"📜❌ create_x509_certificate: Failed: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError("Failed to create X.509 certificate object") from e


def x_create_x509_certificate__mutmut_45(
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
            logger.debug(f"📜📝✅ Added SANs: {alt_names or []}")

        builder = builder.add_extension(
            x509.BasicConstraints(ca=is_ca, path_length=None),
            critical=False,
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
            f"📜📝✅ Added BasicConstraints (is_ca={is_ca}), "
            f"KeyUsage, ExtendedKeyUsage (is_client_cert={is_client_cert})",
        )

        signed_cert = builder.sign(
            private_key=actual_signing_key,
            algorithm=hashes.SHA256(),
        )
        logger.debug("📜📝✅ Certificate signed successfully")
        return signed_cert

    except Exception as e:
        logger.error(
            f"📜❌ create_x509_certificate: Failed: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError("Failed to create X.509 certificate object") from e


def x_create_x509_certificate__mutmut_46(
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
            logger.debug(f"📜📝✅ Added SANs: {alt_names or []}")

        builder = builder.add_extension(
            x509.BasicConstraints(ca=is_ca, path_length=None),
            critical=True,
        )

        if is_ca:
            builder = None
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
            f"📜📝✅ Added BasicConstraints (is_ca={is_ca}), "
            f"KeyUsage, ExtendedKeyUsage (is_client_cert={is_client_cert})",
        )

        signed_cert = builder.sign(
            private_key=actual_signing_key,
            algorithm=hashes.SHA256(),
        )
        logger.debug("📜📝✅ Certificate signed successfully")
        return signed_cert

    except Exception as e:
        logger.error(
            f"📜❌ create_x509_certificate: Failed: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError("Failed to create X.509 certificate object") from e


def x_create_x509_certificate__mutmut_47(
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
            logger.debug(f"📜📝✅ Added SANs: {alt_names or []}")

        builder = builder.add_extension(
            x509.BasicConstraints(ca=is_ca, path_length=None),
            critical=True,
        )

        if is_ca:
            builder = builder.add_extension(
                None,
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
            f"📜📝✅ Added BasicConstraints (is_ca={is_ca}), "
            f"KeyUsage, ExtendedKeyUsage (is_client_cert={is_client_cert})",
        )

        signed_cert = builder.sign(
            private_key=actual_signing_key,
            algorithm=hashes.SHA256(),
        )
        logger.debug("📜📝✅ Certificate signed successfully")
        return signed_cert

    except Exception as e:
        logger.error(
            f"📜❌ create_x509_certificate: Failed: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError("Failed to create X.509 certificate object") from e


def x_create_x509_certificate__mutmut_48(
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
            logger.debug(f"📜📝✅ Added SANs: {alt_names or []}")

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
                critical=None,
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
            f"📜📝✅ Added BasicConstraints (is_ca={is_ca}), "
            f"KeyUsage, ExtendedKeyUsage (is_client_cert={is_client_cert})",
        )

        signed_cert = builder.sign(
            private_key=actual_signing_key,
            algorithm=hashes.SHA256(),
        )
        logger.debug("📜📝✅ Certificate signed successfully")
        return signed_cert

    except Exception as e:
        logger.error(
            f"📜❌ create_x509_certificate: Failed: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError("Failed to create X.509 certificate object") from e


def x_create_x509_certificate__mutmut_49(
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
            logger.debug(f"📜📝✅ Added SANs: {alt_names or []}")

        builder = builder.add_extension(
            x509.BasicConstraints(ca=is_ca, path_length=None),
            critical=True,
        )

        if is_ca:
            builder = builder.add_extension(
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
            f"📜📝✅ Added BasicConstraints (is_ca={is_ca}), "
            f"KeyUsage, ExtendedKeyUsage (is_client_cert={is_client_cert})",
        )

        signed_cert = builder.sign(
            private_key=actual_signing_key,
            algorithm=hashes.SHA256(),
        )
        logger.debug("📜📝✅ Certificate signed successfully")
        return signed_cert

    except Exception as e:
        logger.error(
            f"📜❌ create_x509_certificate: Failed: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError("Failed to create X.509 certificate object") from e


def x_create_x509_certificate__mutmut_50(
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
            logger.debug(f"📜📝✅ Added SANs: {alt_names or []}")

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
            f"📜📝✅ Added BasicConstraints (is_ca={is_ca}), "
            f"KeyUsage, ExtendedKeyUsage (is_client_cert={is_client_cert})",
        )

        signed_cert = builder.sign(
            private_key=actual_signing_key,
            algorithm=hashes.SHA256(),
        )
        logger.debug("📜📝✅ Certificate signed successfully")
        return signed_cert

    except Exception as e:
        logger.error(
            f"📜❌ create_x509_certificate: Failed: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError("Failed to create X.509 certificate object") from e


def x_create_x509_certificate__mutmut_51(
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
            logger.debug(f"📜📝✅ Added SANs: {alt_names or []}")

        builder = builder.add_extension(
            x509.BasicConstraints(ca=is_ca, path_length=None),
            critical=True,
        )

        if is_ca:
            builder = builder.add_extension(
                x509.KeyUsage(
                    digital_signature=None,
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
            f"📜📝✅ Added BasicConstraints (is_ca={is_ca}), "
            f"KeyUsage, ExtendedKeyUsage (is_client_cert={is_client_cert})",
        )

        signed_cert = builder.sign(
            private_key=actual_signing_key,
            algorithm=hashes.SHA256(),
        )
        logger.debug("📜📝✅ Certificate signed successfully")
        return signed_cert

    except Exception as e:
        logger.error(
            f"📜❌ create_x509_certificate: Failed: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError("Failed to create X.509 certificate object") from e


def x_create_x509_certificate__mutmut_52(
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
            logger.debug(f"📜📝✅ Added SANs: {alt_names or []}")

        builder = builder.add_extension(
            x509.BasicConstraints(ca=is_ca, path_length=None),
            critical=True,
        )

        if is_ca:
            builder = builder.add_extension(
                x509.KeyUsage(
                    digital_signature=False,
                    key_encipherment=None,
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
            f"📜📝✅ Added BasicConstraints (is_ca={is_ca}), "
            f"KeyUsage, ExtendedKeyUsage (is_client_cert={is_client_cert})",
        )

        signed_cert = builder.sign(
            private_key=actual_signing_key,
            algorithm=hashes.SHA256(),
        )
        logger.debug("📜📝✅ Certificate signed successfully")
        return signed_cert

    except Exception as e:
        logger.error(
            f"📜❌ create_x509_certificate: Failed: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError("Failed to create X.509 certificate object") from e


def x_create_x509_certificate__mutmut_53(
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
            logger.debug(f"📜📝✅ Added SANs: {alt_names or []}")

        builder = builder.add_extension(
            x509.BasicConstraints(ca=is_ca, path_length=None),
            critical=True,
        )

        if is_ca:
            builder = builder.add_extension(
                x509.KeyUsage(
                    digital_signature=False,
                    key_encipherment=False,
                    key_agreement=None,
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
            f"📜📝✅ Added BasicConstraints (is_ca={is_ca}), "
            f"KeyUsage, ExtendedKeyUsage (is_client_cert={is_client_cert})",
        )

        signed_cert = builder.sign(
            private_key=actual_signing_key,
            algorithm=hashes.SHA256(),
        )
        logger.debug("📜📝✅ Certificate signed successfully")
        return signed_cert

    except Exception as e:
        logger.error(
            f"📜❌ create_x509_certificate: Failed: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError("Failed to create X.509 certificate object") from e


def x_create_x509_certificate__mutmut_54(
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
            logger.debug(f"📜📝✅ Added SANs: {alt_names or []}")

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
                    content_commitment=None,
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
            f"📜📝✅ Added BasicConstraints (is_ca={is_ca}), "
            f"KeyUsage, ExtendedKeyUsage (is_client_cert={is_client_cert})",
        )

        signed_cert = builder.sign(
            private_key=actual_signing_key,
            algorithm=hashes.SHA256(),
        )
        logger.debug("📜📝✅ Certificate signed successfully")
        return signed_cert

    except Exception as e:
        logger.error(
            f"📜❌ create_x509_certificate: Failed: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError("Failed to create X.509 certificate object") from e


def x_create_x509_certificate__mutmut_55(
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
            logger.debug(f"📜📝✅ Added SANs: {alt_names or []}")

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
                    data_encipherment=None,
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
            f"📜📝✅ Added BasicConstraints (is_ca={is_ca}), "
            f"KeyUsage, ExtendedKeyUsage (is_client_cert={is_client_cert})",
        )

        signed_cert = builder.sign(
            private_key=actual_signing_key,
            algorithm=hashes.SHA256(),
        )
        logger.debug("📜📝✅ Certificate signed successfully")
        return signed_cert

    except Exception as e:
        logger.error(
            f"📜❌ create_x509_certificate: Failed: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError("Failed to create X.509 certificate object") from e


def x_create_x509_certificate__mutmut_56(
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
            logger.debug(f"📜📝✅ Added SANs: {alt_names or []}")

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
                    key_cert_sign=None,
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
            f"📜📝✅ Added BasicConstraints (is_ca={is_ca}), "
            f"KeyUsage, ExtendedKeyUsage (is_client_cert={is_client_cert})",
        )

        signed_cert = builder.sign(
            private_key=actual_signing_key,
            algorithm=hashes.SHA256(),
        )
        logger.debug("📜📝✅ Certificate signed successfully")
        return signed_cert

    except Exception as e:
        logger.error(
            f"📜❌ create_x509_certificate: Failed: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError("Failed to create X.509 certificate object") from e


def x_create_x509_certificate__mutmut_57(
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
            logger.debug(f"📜📝✅ Added SANs: {alt_names or []}")

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
                    crl_sign=None,
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
            f"📜📝✅ Added BasicConstraints (is_ca={is_ca}), "
            f"KeyUsage, ExtendedKeyUsage (is_client_cert={is_client_cert})",
        )

        signed_cert = builder.sign(
            private_key=actual_signing_key,
            algorithm=hashes.SHA256(),
        )
        logger.debug("📜📝✅ Certificate signed successfully")
        return signed_cert

    except Exception as e:
        logger.error(
            f"📜❌ create_x509_certificate: Failed: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError("Failed to create X.509 certificate object") from e


def x_create_x509_certificate__mutmut_58(
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
            logger.debug(f"📜📝✅ Added SANs: {alt_names or []}")

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
                    encipher_only=None,
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
            f"📜📝✅ Added BasicConstraints (is_ca={is_ca}), "
            f"KeyUsage, ExtendedKeyUsage (is_client_cert={is_client_cert})",
        )

        signed_cert = builder.sign(
            private_key=actual_signing_key,
            algorithm=hashes.SHA256(),
        )
        logger.debug("📜📝✅ Certificate signed successfully")
        return signed_cert

    except Exception as e:
        logger.error(
            f"📜❌ create_x509_certificate: Failed: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError("Failed to create X.509 certificate object") from e


def x_create_x509_certificate__mutmut_59(
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
            logger.debug(f"📜📝✅ Added SANs: {alt_names or []}")

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
                    decipher_only=None,
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
            f"📜📝✅ Added BasicConstraints (is_ca={is_ca}), "
            f"KeyUsage, ExtendedKeyUsage (is_client_cert={is_client_cert})",
        )

        signed_cert = builder.sign(
            private_key=actual_signing_key,
            algorithm=hashes.SHA256(),
        )
        logger.debug("📜📝✅ Certificate signed successfully")
        return signed_cert

    except Exception as e:
        logger.error(
            f"📜❌ create_x509_certificate: Failed: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError("Failed to create X.509 certificate object") from e


def x_create_x509_certificate__mutmut_60(
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
            logger.debug(f"📜📝✅ Added SANs: {alt_names or []}")

        builder = builder.add_extension(
            x509.BasicConstraints(ca=is_ca, path_length=None),
            critical=True,
        )

        if is_ca:
            builder = builder.add_extension(
                x509.KeyUsage(
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
            f"📜📝✅ Added BasicConstraints (is_ca={is_ca}), "
            f"KeyUsage, ExtendedKeyUsage (is_client_cert={is_client_cert})",
        )

        signed_cert = builder.sign(
            private_key=actual_signing_key,
            algorithm=hashes.SHA256(),
        )
        logger.debug("📜📝✅ Certificate signed successfully")
        return signed_cert

    except Exception as e:
        logger.error(
            f"📜❌ create_x509_certificate: Failed: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError("Failed to create X.509 certificate object") from e


def x_create_x509_certificate__mutmut_61(
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
            logger.debug(f"📜📝✅ Added SANs: {alt_names or []}")

        builder = builder.add_extension(
            x509.BasicConstraints(ca=is_ca, path_length=None),
            critical=True,
        )

        if is_ca:
            builder = builder.add_extension(
                x509.KeyUsage(
                    digital_signature=False,
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
            f"📜📝✅ Added BasicConstraints (is_ca={is_ca}), "
            f"KeyUsage, ExtendedKeyUsage (is_client_cert={is_client_cert})",
        )

        signed_cert = builder.sign(
            private_key=actual_signing_key,
            algorithm=hashes.SHA256(),
        )
        logger.debug("📜📝✅ Certificate signed successfully")
        return signed_cert

    except Exception as e:
        logger.error(
            f"📜❌ create_x509_certificate: Failed: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError("Failed to create X.509 certificate object") from e


def x_create_x509_certificate__mutmut_62(
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
            logger.debug(f"📜📝✅ Added SANs: {alt_names or []}")

        builder = builder.add_extension(
            x509.BasicConstraints(ca=is_ca, path_length=None),
            critical=True,
        )

        if is_ca:
            builder = builder.add_extension(
                x509.KeyUsage(
                    digital_signature=False,
                    key_encipherment=False,
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
            f"📜📝✅ Added BasicConstraints (is_ca={is_ca}), "
            f"KeyUsage, ExtendedKeyUsage (is_client_cert={is_client_cert})",
        )

        signed_cert = builder.sign(
            private_key=actual_signing_key,
            algorithm=hashes.SHA256(),
        )
        logger.debug("📜📝✅ Certificate signed successfully")
        return signed_cert

    except Exception as e:
        logger.error(
            f"📜❌ create_x509_certificate: Failed: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError("Failed to create X.509 certificate object") from e


def x_create_x509_certificate__mutmut_63(
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
            logger.debug(f"📜📝✅ Added SANs: {alt_names or []}")

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
            f"📜📝✅ Added BasicConstraints (is_ca={is_ca}), "
            f"KeyUsage, ExtendedKeyUsage (is_client_cert={is_client_cert})",
        )

        signed_cert = builder.sign(
            private_key=actual_signing_key,
            algorithm=hashes.SHA256(),
        )
        logger.debug("📜📝✅ Certificate signed successfully")
        return signed_cert

    except Exception as e:
        logger.error(
            f"📜❌ create_x509_certificate: Failed: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError("Failed to create X.509 certificate object") from e


def x_create_x509_certificate__mutmut_64(
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
            logger.debug(f"📜📝✅ Added SANs: {alt_names or []}")

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
            f"📜📝✅ Added BasicConstraints (is_ca={is_ca}), "
            f"KeyUsage, ExtendedKeyUsage (is_client_cert={is_client_cert})",
        )

        signed_cert = builder.sign(
            private_key=actual_signing_key,
            algorithm=hashes.SHA256(),
        )
        logger.debug("📜📝✅ Certificate signed successfully")
        return signed_cert

    except Exception as e:
        logger.error(
            f"📜❌ create_x509_certificate: Failed: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError("Failed to create X.509 certificate object") from e


def x_create_x509_certificate__mutmut_65(
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
            logger.debug(f"📜📝✅ Added SANs: {alt_names or []}")

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
            f"📜📝✅ Added BasicConstraints (is_ca={is_ca}), "
            f"KeyUsage, ExtendedKeyUsage (is_client_cert={is_client_cert})",
        )

        signed_cert = builder.sign(
            private_key=actual_signing_key,
            algorithm=hashes.SHA256(),
        )
        logger.debug("📜📝✅ Certificate signed successfully")
        return signed_cert

    except Exception as e:
        logger.error(
            f"📜❌ create_x509_certificate: Failed: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError("Failed to create X.509 certificate object") from e


def x_create_x509_certificate__mutmut_66(
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
            logger.debug(f"📜📝✅ Added SANs: {alt_names or []}")

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
            f"📜📝✅ Added BasicConstraints (is_ca={is_ca}), "
            f"KeyUsage, ExtendedKeyUsage (is_client_cert={is_client_cert})",
        )

        signed_cert = builder.sign(
            private_key=actual_signing_key,
            algorithm=hashes.SHA256(),
        )
        logger.debug("📜📝✅ Certificate signed successfully")
        return signed_cert

    except Exception as e:
        logger.error(
            f"📜❌ create_x509_certificate: Failed: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError("Failed to create X.509 certificate object") from e


def x_create_x509_certificate__mutmut_67(
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
            logger.debug(f"📜📝✅ Added SANs: {alt_names or []}")

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
            f"📜📝✅ Added BasicConstraints (is_ca={is_ca}), "
            f"KeyUsage, ExtendedKeyUsage (is_client_cert={is_client_cert})",
        )

        signed_cert = builder.sign(
            private_key=actual_signing_key,
            algorithm=hashes.SHA256(),
        )
        logger.debug("📜📝✅ Certificate signed successfully")
        return signed_cert

    except Exception as e:
        logger.error(
            f"📜❌ create_x509_certificate: Failed: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError("Failed to create X.509 certificate object") from e


def x_create_x509_certificate__mutmut_68(
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
            logger.debug(f"📜📝✅ Added SANs: {alt_names or []}")

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
            f"📜📝✅ Added BasicConstraints (is_ca={is_ca}), "
            f"KeyUsage, ExtendedKeyUsage (is_client_cert={is_client_cert})",
        )

        signed_cert = builder.sign(
            private_key=actual_signing_key,
            algorithm=hashes.SHA256(),
        )
        logger.debug("📜📝✅ Certificate signed successfully")
        return signed_cert

    except Exception as e:
        logger.error(
            f"📜❌ create_x509_certificate: Failed: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError("Failed to create X.509 certificate object") from e


def x_create_x509_certificate__mutmut_69(
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
            logger.debug(f"📜📝✅ Added SANs: {alt_names or []}")

        builder = builder.add_extension(
            x509.BasicConstraints(ca=is_ca, path_length=None),
            critical=True,
        )

        if is_ca:
            builder = builder.add_extension(
                x509.KeyUsage(
                    digital_signature=True,
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
            f"📜📝✅ Added BasicConstraints (is_ca={is_ca}), "
            f"KeyUsage, ExtendedKeyUsage (is_client_cert={is_client_cert})",
        )

        signed_cert = builder.sign(
            private_key=actual_signing_key,
            algorithm=hashes.SHA256(),
        )
        logger.debug("📜📝✅ Certificate signed successfully")
        return signed_cert

    except Exception as e:
        logger.error(
            f"📜❌ create_x509_certificate: Failed: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError("Failed to create X.509 certificate object") from e


def x_create_x509_certificate__mutmut_70(
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
            logger.debug(f"📜📝✅ Added SANs: {alt_names or []}")

        builder = builder.add_extension(
            x509.BasicConstraints(ca=is_ca, path_length=None),
            critical=True,
        )

        if is_ca:
            builder = builder.add_extension(
                x509.KeyUsage(
                    digital_signature=False,
                    key_encipherment=True,
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
            f"📜📝✅ Added BasicConstraints (is_ca={is_ca}), "
            f"KeyUsage, ExtendedKeyUsage (is_client_cert={is_client_cert})",
        )

        signed_cert = builder.sign(
            private_key=actual_signing_key,
            algorithm=hashes.SHA256(),
        )
        logger.debug("📜📝✅ Certificate signed successfully")
        return signed_cert

    except Exception as e:
        logger.error(
            f"📜❌ create_x509_certificate: Failed: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError("Failed to create X.509 certificate object") from e


def x_create_x509_certificate__mutmut_71(
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
            logger.debug(f"📜📝✅ Added SANs: {alt_names or []}")

        builder = builder.add_extension(
            x509.BasicConstraints(ca=is_ca, path_length=None),
            critical=True,
        )

        if is_ca:
            builder = builder.add_extension(
                x509.KeyUsage(
                    digital_signature=False,
                    key_encipherment=False,
                    key_agreement=True,
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
            f"📜📝✅ Added BasicConstraints (is_ca={is_ca}), "
            f"KeyUsage, ExtendedKeyUsage (is_client_cert={is_client_cert})",
        )

        signed_cert = builder.sign(
            private_key=actual_signing_key,
            algorithm=hashes.SHA256(),
        )
        logger.debug("📜📝✅ Certificate signed successfully")
        return signed_cert

    except Exception as e:
        logger.error(
            f"📜❌ create_x509_certificate: Failed: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError("Failed to create X.509 certificate object") from e


def x_create_x509_certificate__mutmut_72(
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
            logger.debug(f"📜📝✅ Added SANs: {alt_names or []}")

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
                    content_commitment=True,
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
            f"📜📝✅ Added BasicConstraints (is_ca={is_ca}), "
            f"KeyUsage, ExtendedKeyUsage (is_client_cert={is_client_cert})",
        )

        signed_cert = builder.sign(
            private_key=actual_signing_key,
            algorithm=hashes.SHA256(),
        )
        logger.debug("📜📝✅ Certificate signed successfully")
        return signed_cert

    except Exception as e:
        logger.error(
            f"📜❌ create_x509_certificate: Failed: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError("Failed to create X.509 certificate object") from e


def x_create_x509_certificate__mutmut_73(
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
            logger.debug(f"📜📝✅ Added SANs: {alt_names or []}")

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
                    data_encipherment=True,
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
            f"📜📝✅ Added BasicConstraints (is_ca={is_ca}), "
            f"KeyUsage, ExtendedKeyUsage (is_client_cert={is_client_cert})",
        )

        signed_cert = builder.sign(
            private_key=actual_signing_key,
            algorithm=hashes.SHA256(),
        )
        logger.debug("📜📝✅ Certificate signed successfully")
        return signed_cert

    except Exception as e:
        logger.error(
            f"📜❌ create_x509_certificate: Failed: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError("Failed to create X.509 certificate object") from e


def x_create_x509_certificate__mutmut_74(
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
            logger.debug(f"📜📝✅ Added SANs: {alt_names or []}")

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
                    key_cert_sign=False,
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
            f"📜📝✅ Added BasicConstraints (is_ca={is_ca}), "
            f"KeyUsage, ExtendedKeyUsage (is_client_cert={is_client_cert})",
        )

        signed_cert = builder.sign(
            private_key=actual_signing_key,
            algorithm=hashes.SHA256(),
        )
        logger.debug("📜📝✅ Certificate signed successfully")
        return signed_cert

    except Exception as e:
        logger.error(
            f"📜❌ create_x509_certificate: Failed: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError("Failed to create X.509 certificate object") from e


def x_create_x509_certificate__mutmut_75(
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
            logger.debug(f"📜📝✅ Added SANs: {alt_names or []}")

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
                    crl_sign=False,
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
            f"📜📝✅ Added BasicConstraints (is_ca={is_ca}), "
            f"KeyUsage, ExtendedKeyUsage (is_client_cert={is_client_cert})",
        )

        signed_cert = builder.sign(
            private_key=actual_signing_key,
            algorithm=hashes.SHA256(),
        )
        logger.debug("📜📝✅ Certificate signed successfully")
        return signed_cert

    except Exception as e:
        logger.error(
            f"📜❌ create_x509_certificate: Failed: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError("Failed to create X.509 certificate object") from e


def x_create_x509_certificate__mutmut_76(
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
            logger.debug(f"📜📝✅ Added SANs: {alt_names or []}")

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
                    encipher_only=True,
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
            f"📜📝✅ Added BasicConstraints (is_ca={is_ca}), "
            f"KeyUsage, ExtendedKeyUsage (is_client_cert={is_client_cert})",
        )

        signed_cert = builder.sign(
            private_key=actual_signing_key,
            algorithm=hashes.SHA256(),
        )
        logger.debug("📜📝✅ Certificate signed successfully")
        return signed_cert

    except Exception as e:
        logger.error(
            f"📜❌ create_x509_certificate: Failed: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError("Failed to create X.509 certificate object") from e


def x_create_x509_certificate__mutmut_77(
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
            logger.debug(f"📜📝✅ Added SANs: {alt_names or []}")

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
                    decipher_only=True,
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
            f"📜📝✅ Added BasicConstraints (is_ca={is_ca}), "
            f"KeyUsage, ExtendedKeyUsage (is_client_cert={is_client_cert})",
        )

        signed_cert = builder.sign(
            private_key=actual_signing_key,
            algorithm=hashes.SHA256(),
        )
        logger.debug("📜📝✅ Certificate signed successfully")
        return signed_cert

    except Exception as e:
        logger.error(
            f"📜❌ create_x509_certificate: Failed: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError("Failed to create X.509 certificate object") from e


def x_create_x509_certificate__mutmut_78(
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
            logger.debug(f"📜📝✅ Added SANs: {alt_names or []}")

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
                critical=False,
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
            f"📜📝✅ Added BasicConstraints (is_ca={is_ca}), "
            f"KeyUsage, ExtendedKeyUsage (is_client_cert={is_client_cert})",
        )

        signed_cert = builder.sign(
            private_key=actual_signing_key,
            algorithm=hashes.SHA256(),
        )
        logger.debug("📜📝✅ Certificate signed successfully")
        return signed_cert

    except Exception as e:
        logger.error(
            f"📜❌ create_x509_certificate: Failed: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError("Failed to create X.509 certificate object") from e


def x_create_x509_certificate__mutmut_79(
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
            logger.debug(f"📜📝✅ Added SANs: {alt_names or []}")

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
            builder = None
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
            f"📜📝✅ Added BasicConstraints (is_ca={is_ca}), "
            f"KeyUsage, ExtendedKeyUsage (is_client_cert={is_client_cert})",
        )

        signed_cert = builder.sign(
            private_key=actual_signing_key,
            algorithm=hashes.SHA256(),
        )
        logger.debug("📜📝✅ Certificate signed successfully")
        return signed_cert

    except Exception as e:
        logger.error(
            f"📜❌ create_x509_certificate: Failed: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError("Failed to create X.509 certificate object") from e


def x_create_x509_certificate__mutmut_80(
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
            logger.debug(f"📜📝✅ Added SANs: {alt_names or []}")

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
                None,
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
            f"📜📝✅ Added BasicConstraints (is_ca={is_ca}), "
            f"KeyUsage, ExtendedKeyUsage (is_client_cert={is_client_cert})",
        )

        signed_cert = builder.sign(
            private_key=actual_signing_key,
            algorithm=hashes.SHA256(),
        )
        logger.debug("📜📝✅ Certificate signed successfully")
        return signed_cert

    except Exception as e:
        logger.error(
            f"📜❌ create_x509_certificate: Failed: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError("Failed to create X.509 certificate object") from e


def x_create_x509_certificate__mutmut_81(
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
            logger.debug(f"📜📝✅ Added SANs: {alt_names or []}")

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
                critical=None,
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
            f"📜📝✅ Added BasicConstraints (is_ca={is_ca}), "
            f"KeyUsage, ExtendedKeyUsage (is_client_cert={is_client_cert})",
        )

        signed_cert = builder.sign(
            private_key=actual_signing_key,
            algorithm=hashes.SHA256(),
        )
        logger.debug("📜📝✅ Certificate signed successfully")
        return signed_cert

    except Exception as e:
        logger.error(
            f"📜❌ create_x509_certificate: Failed: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError("Failed to create X.509 certificate object") from e


def x_create_x509_certificate__mutmut_82(
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
            logger.debug(f"📜📝✅ Added SANs: {alt_names or []}")

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
            f"📜📝✅ Added BasicConstraints (is_ca={is_ca}), "
            f"KeyUsage, ExtendedKeyUsage (is_client_cert={is_client_cert})",
        )

        signed_cert = builder.sign(
            private_key=actual_signing_key,
            algorithm=hashes.SHA256(),
        )
        logger.debug("📜📝✅ Certificate signed successfully")
        return signed_cert

    except Exception as e:
        logger.error(
            f"📜❌ create_x509_certificate: Failed: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError("Failed to create X.509 certificate object") from e


def x_create_x509_certificate__mutmut_83(
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
            logger.debug(f"📜📝✅ Added SANs: {alt_names or []}")

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
            f"📜📝✅ Added BasicConstraints (is_ca={is_ca}), "
            f"KeyUsage, ExtendedKeyUsage (is_client_cert={is_client_cert})",
        )

        signed_cert = builder.sign(
            private_key=actual_signing_key,
            algorithm=hashes.SHA256(),
        )
        logger.debug("📜📝✅ Certificate signed successfully")
        return signed_cert

    except Exception as e:
        logger.error(
            f"📜❌ create_x509_certificate: Failed: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError("Failed to create X.509 certificate object") from e


def x_create_x509_certificate__mutmut_84(
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
            logger.debug(f"📜📝✅ Added SANs: {alt_names or []}")

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
                    digital_signature=None,
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
            f"📜📝✅ Added BasicConstraints (is_ca={is_ca}), "
            f"KeyUsage, ExtendedKeyUsage (is_client_cert={is_client_cert})",
        )

        signed_cert = builder.sign(
            private_key=actual_signing_key,
            algorithm=hashes.SHA256(),
        )
        logger.debug("📜📝✅ Certificate signed successfully")
        return signed_cert

    except Exception as e:
        logger.error(
            f"📜❌ create_x509_certificate: Failed: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError("Failed to create X.509 certificate object") from e


def x_create_x509_certificate__mutmut_85(
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
            logger.debug(f"📜📝✅ Added SANs: {alt_names or []}")

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
                    key_encipherment=None,
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
            f"📜📝✅ Added BasicConstraints (is_ca={is_ca}), "
            f"KeyUsage, ExtendedKeyUsage (is_client_cert={is_client_cert})",
        )

        signed_cert = builder.sign(
            private_key=actual_signing_key,
            algorithm=hashes.SHA256(),
        )
        logger.debug("📜📝✅ Certificate signed successfully")
        return signed_cert

    except Exception as e:
        logger.error(
            f"📜❌ create_x509_certificate: Failed: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError("Failed to create X.509 certificate object") from e


def x_create_x509_certificate__mutmut_86(
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
            logger.debug(f"📜📝✅ Added SANs: {alt_names or []}")

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
                    key_agreement=None,
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
            f"📜📝✅ Added BasicConstraints (is_ca={is_ca}), "
            f"KeyUsage, ExtendedKeyUsage (is_client_cert={is_client_cert})",
        )

        signed_cert = builder.sign(
            private_key=actual_signing_key,
            algorithm=hashes.SHA256(),
        )
        logger.debug("📜📝✅ Certificate signed successfully")
        return signed_cert

    except Exception as e:
        logger.error(
            f"📜❌ create_x509_certificate: Failed: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError("Failed to create X.509 certificate object") from e


def x_create_x509_certificate__mutmut_87(
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
            logger.debug(f"📜📝✅ Added SANs: {alt_names or []}")

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
                    content_commitment=None,
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
            f"📜📝✅ Added BasicConstraints (is_ca={is_ca}), "
            f"KeyUsage, ExtendedKeyUsage (is_client_cert={is_client_cert})",
        )

        signed_cert = builder.sign(
            private_key=actual_signing_key,
            algorithm=hashes.SHA256(),
        )
        logger.debug("📜📝✅ Certificate signed successfully")
        return signed_cert

    except Exception as e:
        logger.error(
            f"📜❌ create_x509_certificate: Failed: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError("Failed to create X.509 certificate object") from e


def x_create_x509_certificate__mutmut_88(
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
            logger.debug(f"📜📝✅ Added SANs: {alt_names or []}")

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
                    data_encipherment=None,
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
            f"📜📝✅ Added BasicConstraints (is_ca={is_ca}), "
            f"KeyUsage, ExtendedKeyUsage (is_client_cert={is_client_cert})",
        )

        signed_cert = builder.sign(
            private_key=actual_signing_key,
            algorithm=hashes.SHA256(),
        )
        logger.debug("📜📝✅ Certificate signed successfully")
        return signed_cert

    except Exception as e:
        logger.error(
            f"📜❌ create_x509_certificate: Failed: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError("Failed to create X.509 certificate object") from e


def x_create_x509_certificate__mutmut_89(
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
            logger.debug(f"📜📝✅ Added SANs: {alt_names or []}")

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
                    key_cert_sign=None,
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
            f"📜📝✅ Added BasicConstraints (is_ca={is_ca}), "
            f"KeyUsage, ExtendedKeyUsage (is_client_cert={is_client_cert})",
        )

        signed_cert = builder.sign(
            private_key=actual_signing_key,
            algorithm=hashes.SHA256(),
        )
        logger.debug("📜📝✅ Certificate signed successfully")
        return signed_cert

    except Exception as e:
        logger.error(
            f"📜❌ create_x509_certificate: Failed: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError("Failed to create X.509 certificate object") from e


def x_create_x509_certificate__mutmut_90(
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
            logger.debug(f"📜📝✅ Added SANs: {alt_names or []}")

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
                    crl_sign=None,
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
            f"📜📝✅ Added BasicConstraints (is_ca={is_ca}), "
            f"KeyUsage, ExtendedKeyUsage (is_client_cert={is_client_cert})",
        )

        signed_cert = builder.sign(
            private_key=actual_signing_key,
            algorithm=hashes.SHA256(),
        )
        logger.debug("📜📝✅ Certificate signed successfully")
        return signed_cert

    except Exception as e:
        logger.error(
            f"📜❌ create_x509_certificate: Failed: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError("Failed to create X.509 certificate object") from e


def x_create_x509_certificate__mutmut_91(
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
            logger.debug(f"📜📝✅ Added SANs: {alt_names or []}")

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
                    encipher_only=None,
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
            f"📜📝✅ Added BasicConstraints (is_ca={is_ca}), "
            f"KeyUsage, ExtendedKeyUsage (is_client_cert={is_client_cert})",
        )

        signed_cert = builder.sign(
            private_key=actual_signing_key,
            algorithm=hashes.SHA256(),
        )
        logger.debug("📜📝✅ Certificate signed successfully")
        return signed_cert

    except Exception as e:
        logger.error(
            f"📜❌ create_x509_certificate: Failed: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError("Failed to create X.509 certificate object") from e


def x_create_x509_certificate__mutmut_92(
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
            logger.debug(f"📜📝✅ Added SANs: {alt_names or []}")

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
                    decipher_only=None,
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
            f"📜📝✅ Added BasicConstraints (is_ca={is_ca}), "
            f"KeyUsage, ExtendedKeyUsage (is_client_cert={is_client_cert})",
        )

        signed_cert = builder.sign(
            private_key=actual_signing_key,
            algorithm=hashes.SHA256(),
        )
        logger.debug("📜📝✅ Certificate signed successfully")
        return signed_cert

    except Exception as e:
        logger.error(
            f"📜❌ create_x509_certificate: Failed: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError("Failed to create X.509 certificate object") from e


def x_create_x509_certificate__mutmut_93(
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
            logger.debug(f"📜📝✅ Added SANs: {alt_names or []}")

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
            f"📜📝✅ Added BasicConstraints (is_ca={is_ca}), "
            f"KeyUsage, ExtendedKeyUsage (is_client_cert={is_client_cert})",
        )

        signed_cert = builder.sign(
            private_key=actual_signing_key,
            algorithm=hashes.SHA256(),
        )
        logger.debug("📜📝✅ Certificate signed successfully")
        return signed_cert

    except Exception as e:
        logger.error(
            f"📜❌ create_x509_certificate: Failed: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError("Failed to create X.509 certificate object") from e


def x_create_x509_certificate__mutmut_94(
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
            logger.debug(f"📜📝✅ Added SANs: {alt_names or []}")

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
            f"📜📝✅ Added BasicConstraints (is_ca={is_ca}), "
            f"KeyUsage, ExtendedKeyUsage (is_client_cert={is_client_cert})",
        )

        signed_cert = builder.sign(
            private_key=actual_signing_key,
            algorithm=hashes.SHA256(),
        )
        logger.debug("📜📝✅ Certificate signed successfully")
        return signed_cert

    except Exception as e:
        logger.error(
            f"📜❌ create_x509_certificate: Failed: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError("Failed to create X.509 certificate object") from e


def x_create_x509_certificate__mutmut_95(
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
            logger.debug(f"📜📝✅ Added SANs: {alt_names or []}")

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
            f"📜📝✅ Added BasicConstraints (is_ca={is_ca}), "
            f"KeyUsage, ExtendedKeyUsage (is_client_cert={is_client_cert})",
        )

        signed_cert = builder.sign(
            private_key=actual_signing_key,
            algorithm=hashes.SHA256(),
        )
        logger.debug("📜📝✅ Certificate signed successfully")
        return signed_cert

    except Exception as e:
        logger.error(
            f"📜❌ create_x509_certificate: Failed: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError("Failed to create X.509 certificate object") from e


def x_create_x509_certificate__mutmut_96(
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
            logger.debug(f"📜📝✅ Added SANs: {alt_names or []}")

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
            f"📜📝✅ Added BasicConstraints (is_ca={is_ca}), "
            f"KeyUsage, ExtendedKeyUsage (is_client_cert={is_client_cert})",
        )

        signed_cert = builder.sign(
            private_key=actual_signing_key,
            algorithm=hashes.SHA256(),
        )
        logger.debug("📜📝✅ Certificate signed successfully")
        return signed_cert

    except Exception as e:
        logger.error(
            f"📜❌ create_x509_certificate: Failed: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError("Failed to create X.509 certificate object") from e


def x_create_x509_certificate__mutmut_97(
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
            logger.debug(f"📜📝✅ Added SANs: {alt_names or []}")

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
            f"📜📝✅ Added BasicConstraints (is_ca={is_ca}), "
            f"KeyUsage, ExtendedKeyUsage (is_client_cert={is_client_cert})",
        )

        signed_cert = builder.sign(
            private_key=actual_signing_key,
            algorithm=hashes.SHA256(),
        )
        logger.debug("📜📝✅ Certificate signed successfully")
        return signed_cert

    except Exception as e:
        logger.error(
            f"📜❌ create_x509_certificate: Failed: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError("Failed to create X.509 certificate object") from e


def x_create_x509_certificate__mutmut_98(
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
            logger.debug(f"📜📝✅ Added SANs: {alt_names or []}")

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
            f"📜📝✅ Added BasicConstraints (is_ca={is_ca}), "
            f"KeyUsage, ExtendedKeyUsage (is_client_cert={is_client_cert})",
        )

        signed_cert = builder.sign(
            private_key=actual_signing_key,
            algorithm=hashes.SHA256(),
        )
        logger.debug("📜📝✅ Certificate signed successfully")
        return signed_cert

    except Exception as e:
        logger.error(
            f"📜❌ create_x509_certificate: Failed: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError("Failed to create X.509 certificate object") from e


def x_create_x509_certificate__mutmut_99(
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
            logger.debug(f"📜📝✅ Added SANs: {alt_names or []}")

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
            f"📜📝✅ Added BasicConstraints (is_ca={is_ca}), "
            f"KeyUsage, ExtendedKeyUsage (is_client_cert={is_client_cert})",
        )

        signed_cert = builder.sign(
            private_key=actual_signing_key,
            algorithm=hashes.SHA256(),
        )
        logger.debug("📜📝✅ Certificate signed successfully")
        return signed_cert

    except Exception as e:
        logger.error(
            f"📜❌ create_x509_certificate: Failed: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError("Failed to create X.509 certificate object") from e


def x_create_x509_certificate__mutmut_100(
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
            logger.debug(f"📜📝✅ Added SANs: {alt_names or []}")

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
            f"📜📝✅ Added BasicConstraints (is_ca={is_ca}), "
            f"KeyUsage, ExtendedKeyUsage (is_client_cert={is_client_cert})",
        )

        signed_cert = builder.sign(
            private_key=actual_signing_key,
            algorithm=hashes.SHA256(),
        )
        logger.debug("📜📝✅ Certificate signed successfully")
        return signed_cert

    except Exception as e:
        logger.error(
            f"📜❌ create_x509_certificate: Failed: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError("Failed to create X.509 certificate object") from e


def x_create_x509_certificate__mutmut_101(
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
            logger.debug(f"📜📝✅ Added SANs: {alt_names or []}")

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
            f"📜📝✅ Added BasicConstraints (is_ca={is_ca}), "
            f"KeyUsage, ExtendedKeyUsage (is_client_cert={is_client_cert})",
        )

        signed_cert = builder.sign(
            private_key=actual_signing_key,
            algorithm=hashes.SHA256(),
        )
        logger.debug("📜📝✅ Certificate signed successfully")
        return signed_cert

    except Exception as e:
        logger.error(
            f"📜❌ create_x509_certificate: Failed: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError("Failed to create X.509 certificate object") from e


def x_create_x509_certificate__mutmut_102(
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
            logger.debug(f"📜📝✅ Added SANs: {alt_names or []}")

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
                    digital_signature=False,
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
            f"📜📝✅ Added BasicConstraints (is_ca={is_ca}), "
            f"KeyUsage, ExtendedKeyUsage (is_client_cert={is_client_cert})",
        )

        signed_cert = builder.sign(
            private_key=actual_signing_key,
            algorithm=hashes.SHA256(),
        )
        logger.debug("📜📝✅ Certificate signed successfully")
        return signed_cert

    except Exception as e:
        logger.error(
            f"📜❌ create_x509_certificate: Failed: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError("Failed to create X.509 certificate object") from e


def x_create_x509_certificate__mutmut_103(
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
            logger.debug(f"📜📝✅ Added SANs: {alt_names or []}")

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
                        bool(None)
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
            f"📜📝✅ Added BasicConstraints (is_ca={is_ca}), "
            f"KeyUsage, ExtendedKeyUsage (is_client_cert={is_client_cert})",
        )

        signed_cert = builder.sign(
            private_key=actual_signing_key,
            algorithm=hashes.SHA256(),
        )
        logger.debug("📜📝✅ Certificate signed successfully")
        return signed_cert

    except Exception as e:
        logger.error(
            f"📜❌ create_x509_certificate: Failed: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError("Failed to create X.509 certificate object") from e


def x_create_x509_certificate__mutmut_104(
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
            logger.debug(f"📜📝✅ Added SANs: {alt_names or []}")

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
                        bool(not is_client_cert or isinstance(base.public_key, rsa.RSAPublicKey))
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
            f"📜📝✅ Added BasicConstraints (is_ca={is_ca}), "
            f"KeyUsage, ExtendedKeyUsage (is_client_cert={is_client_cert})",
        )

        signed_cert = builder.sign(
            private_key=actual_signing_key,
            algorithm=hashes.SHA256(),
        )
        logger.debug("📜📝✅ Certificate signed successfully")
        return signed_cert

    except Exception as e:
        logger.error(
            f"📜❌ create_x509_certificate: Failed: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError("Failed to create X.509 certificate object") from e


def x_create_x509_certificate__mutmut_105(
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
            logger.debug(f"📜📝✅ Added SANs: {alt_names or []}")

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
                        bool(is_client_cert and isinstance(base.public_key, rsa.RSAPublicKey))
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
            f"📜📝✅ Added BasicConstraints (is_ca={is_ca}), "
            f"KeyUsage, ExtendedKeyUsage (is_client_cert={is_client_cert})",
        )

        signed_cert = builder.sign(
            private_key=actual_signing_key,
            algorithm=hashes.SHA256(),
        )
        logger.debug("📜📝✅ Certificate signed successfully")
        return signed_cert

    except Exception as e:
        logger.error(
            f"📜❌ create_x509_certificate: Failed: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError("Failed to create X.509 certificate object") from e


def x_create_x509_certificate__mutmut_106(
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
            logger.debug(f"📜📝✅ Added SANs: {alt_names or []}")

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
                    key_agreement=(bool(None)),
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
            f"📜📝✅ Added BasicConstraints (is_ca={is_ca}), "
            f"KeyUsage, ExtendedKeyUsage (is_client_cert={is_client_cert})",
        )

        signed_cert = builder.sign(
            private_key=actual_signing_key,
            algorithm=hashes.SHA256(),
        )
        logger.debug("📜📝✅ Certificate signed successfully")
        return signed_cert

    except Exception as e:
        logger.error(
            f"📜❌ create_x509_certificate: Failed: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError("Failed to create X.509 certificate object") from e


def x_create_x509_certificate__mutmut_107(
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
            logger.debug(f"📜📝✅ Added SANs: {alt_names or []}")

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
                    content_commitment=True,
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
            f"📜📝✅ Added BasicConstraints (is_ca={is_ca}), "
            f"KeyUsage, ExtendedKeyUsage (is_client_cert={is_client_cert})",
        )

        signed_cert = builder.sign(
            private_key=actual_signing_key,
            algorithm=hashes.SHA256(),
        )
        logger.debug("📜📝✅ Certificate signed successfully")
        return signed_cert

    except Exception as e:
        logger.error(
            f"📜❌ create_x509_certificate: Failed: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError("Failed to create X.509 certificate object") from e


def x_create_x509_certificate__mutmut_108(
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
            logger.debug(f"📜📝✅ Added SANs: {alt_names or []}")

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
                    data_encipherment=True,
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
            f"📜📝✅ Added BasicConstraints (is_ca={is_ca}), "
            f"KeyUsage, ExtendedKeyUsage (is_client_cert={is_client_cert})",
        )

        signed_cert = builder.sign(
            private_key=actual_signing_key,
            algorithm=hashes.SHA256(),
        )
        logger.debug("📜📝✅ Certificate signed successfully")
        return signed_cert

    except Exception as e:
        logger.error(
            f"📜❌ create_x509_certificate: Failed: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError("Failed to create X.509 certificate object") from e


def x_create_x509_certificate__mutmut_109(
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
            logger.debug(f"📜📝✅ Added SANs: {alt_names or []}")

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
                    key_cert_sign=True,
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
            f"📜📝✅ Added BasicConstraints (is_ca={is_ca}), "
            f"KeyUsage, ExtendedKeyUsage (is_client_cert={is_client_cert})",
        )

        signed_cert = builder.sign(
            private_key=actual_signing_key,
            algorithm=hashes.SHA256(),
        )
        logger.debug("📜📝✅ Certificate signed successfully")
        return signed_cert

    except Exception as e:
        logger.error(
            f"📜❌ create_x509_certificate: Failed: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError("Failed to create X.509 certificate object") from e


def x_create_x509_certificate__mutmut_110(
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
            logger.debug(f"📜📝✅ Added SANs: {alt_names or []}")

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
                    crl_sign=True,
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
            f"📜📝✅ Added BasicConstraints (is_ca={is_ca}), "
            f"KeyUsage, ExtendedKeyUsage (is_client_cert={is_client_cert})",
        )

        signed_cert = builder.sign(
            private_key=actual_signing_key,
            algorithm=hashes.SHA256(),
        )
        logger.debug("📜📝✅ Certificate signed successfully")
        return signed_cert

    except Exception as e:
        logger.error(
            f"📜❌ create_x509_certificate: Failed: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError("Failed to create X.509 certificate object") from e


def x_create_x509_certificate__mutmut_111(
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
            logger.debug(f"📜📝✅ Added SANs: {alt_names or []}")

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
                    encipher_only=True,
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
            f"📜📝✅ Added BasicConstraints (is_ca={is_ca}), "
            f"KeyUsage, ExtendedKeyUsage (is_client_cert={is_client_cert})",
        )

        signed_cert = builder.sign(
            private_key=actual_signing_key,
            algorithm=hashes.SHA256(),
        )
        logger.debug("📜📝✅ Certificate signed successfully")
        return signed_cert

    except Exception as e:
        logger.error(
            f"📜❌ create_x509_certificate: Failed: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError("Failed to create X.509 certificate object") from e


def x_create_x509_certificate__mutmut_112(
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
            logger.debug(f"📜📝✅ Added SANs: {alt_names or []}")

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
                    decipher_only=True,
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
            f"📜📝✅ Added BasicConstraints (is_ca={is_ca}), "
            f"KeyUsage, ExtendedKeyUsage (is_client_cert={is_client_cert})",
        )

        signed_cert = builder.sign(
            private_key=actual_signing_key,
            algorithm=hashes.SHA256(),
        )
        logger.debug("📜📝✅ Certificate signed successfully")
        return signed_cert

    except Exception as e:
        logger.error(
            f"📜❌ create_x509_certificate: Failed: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError("Failed to create X.509 certificate object") from e


def x_create_x509_certificate__mutmut_113(
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
            logger.debug(f"📜📝✅ Added SANs: {alt_names or []}")

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
                critical=False,
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
            f"📜📝✅ Added BasicConstraints (is_ca={is_ca}), "
            f"KeyUsage, ExtendedKeyUsage (is_client_cert={is_client_cert})",
        )

        signed_cert = builder.sign(
            private_key=actual_signing_key,
            algorithm=hashes.SHA256(),
        )
        logger.debug("📜📝✅ Certificate signed successfully")
        return signed_cert

    except Exception as e:
        logger.error(
            f"📜❌ create_x509_certificate: Failed: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError("Failed to create X.509 certificate object") from e


def x_create_x509_certificate__mutmut_114(
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
            logger.debug(f"📜📝✅ Added SANs: {alt_names or []}")

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
            extended_usages = None
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
            f"📜📝✅ Added BasicConstraints (is_ca={is_ca}), "
            f"KeyUsage, ExtendedKeyUsage (is_client_cert={is_client_cert})",
        )

        signed_cert = builder.sign(
            private_key=actual_signing_key,
            algorithm=hashes.SHA256(),
        )
        logger.debug("📜📝✅ Certificate signed successfully")
        return signed_cert

    except Exception as e:
        logger.error(
            f"📜❌ create_x509_certificate: Failed: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError("Failed to create X.509 certificate object") from e


def x_create_x509_certificate__mutmut_115(
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
            logger.debug(f"📜📝✅ Added SANs: {alt_names or []}")

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
                extended_usages.append(None)
            else:
                extended_usages.append(ExtendedKeyUsageOID.SERVER_AUTH)

            if extended_usages:
                builder = builder.add_extension(
                    x509.ExtendedKeyUsage(extended_usages),
                    critical=False,
                )

        logger.debug(
            f"📜📝✅ Added BasicConstraints (is_ca={is_ca}), "
            f"KeyUsage, ExtendedKeyUsage (is_client_cert={is_client_cert})",
        )

        signed_cert = builder.sign(
            private_key=actual_signing_key,
            algorithm=hashes.SHA256(),
        )
        logger.debug("📜📝✅ Certificate signed successfully")
        return signed_cert

    except Exception as e:
        logger.error(
            f"📜❌ create_x509_certificate: Failed: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError("Failed to create X.509 certificate object") from e


def x_create_x509_certificate__mutmut_116(
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
            logger.debug(f"📜📝✅ Added SANs: {alt_names or []}")

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
                extended_usages.append(None)

            if extended_usages:
                builder = builder.add_extension(
                    x509.ExtendedKeyUsage(extended_usages),
                    critical=False,
                )

        logger.debug(
            f"📜📝✅ Added BasicConstraints (is_ca={is_ca}), "
            f"KeyUsage, ExtendedKeyUsage (is_client_cert={is_client_cert})",
        )

        signed_cert = builder.sign(
            private_key=actual_signing_key,
            algorithm=hashes.SHA256(),
        )
        logger.debug("📜📝✅ Certificate signed successfully")
        return signed_cert

    except Exception as e:
        logger.error(
            f"📜❌ create_x509_certificate: Failed: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError("Failed to create X.509 certificate object") from e


def x_create_x509_certificate__mutmut_117(
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
            logger.debug(f"📜📝✅ Added SANs: {alt_names or []}")

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
                builder = None

        logger.debug(
            f"📜📝✅ Added BasicConstraints (is_ca={is_ca}), "
            f"KeyUsage, ExtendedKeyUsage (is_client_cert={is_client_cert})",
        )

        signed_cert = builder.sign(
            private_key=actual_signing_key,
            algorithm=hashes.SHA256(),
        )
        logger.debug("📜📝✅ Certificate signed successfully")
        return signed_cert

    except Exception as e:
        logger.error(
            f"📜❌ create_x509_certificate: Failed: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError("Failed to create X.509 certificate object") from e


def x_create_x509_certificate__mutmut_118(
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
            logger.debug(f"📜📝✅ Added SANs: {alt_names or []}")

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
                    None,
                    critical=False,
                )

        logger.debug(
            f"📜📝✅ Added BasicConstraints (is_ca={is_ca}), "
            f"KeyUsage, ExtendedKeyUsage (is_client_cert={is_client_cert})",
        )

        signed_cert = builder.sign(
            private_key=actual_signing_key,
            algorithm=hashes.SHA256(),
        )
        logger.debug("📜📝✅ Certificate signed successfully")
        return signed_cert

    except Exception as e:
        logger.error(
            f"📜❌ create_x509_certificate: Failed: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError("Failed to create X.509 certificate object") from e


def x_create_x509_certificate__mutmut_119(
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
            logger.debug(f"📜📝✅ Added SANs: {alt_names or []}")

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
                    critical=None,
                )

        logger.debug(
            f"📜📝✅ Added BasicConstraints (is_ca={is_ca}), "
            f"KeyUsage, ExtendedKeyUsage (is_client_cert={is_client_cert})",
        )

        signed_cert = builder.sign(
            private_key=actual_signing_key,
            algorithm=hashes.SHA256(),
        )
        logger.debug("📜📝✅ Certificate signed successfully")
        return signed_cert

    except Exception as e:
        logger.error(
            f"📜❌ create_x509_certificate: Failed: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError("Failed to create X.509 certificate object") from e


def x_create_x509_certificate__mutmut_120(
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
            logger.debug(f"📜📝✅ Added SANs: {alt_names or []}")

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
                    critical=False,
                )

        logger.debug(
            f"📜📝✅ Added BasicConstraints (is_ca={is_ca}), "
            f"KeyUsage, ExtendedKeyUsage (is_client_cert={is_client_cert})",
        )

        signed_cert = builder.sign(
            private_key=actual_signing_key,
            algorithm=hashes.SHA256(),
        )
        logger.debug("📜📝✅ Certificate signed successfully")
        return signed_cert

    except Exception as e:
        logger.error(
            f"📜❌ create_x509_certificate: Failed: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError("Failed to create X.509 certificate object") from e


def x_create_x509_certificate__mutmut_121(
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
            logger.debug(f"📜📝✅ Added SANs: {alt_names or []}")

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
                    )

        logger.debug(
            f"📜📝✅ Added BasicConstraints (is_ca={is_ca}), "
            f"KeyUsage, ExtendedKeyUsage (is_client_cert={is_client_cert})",
        )

        signed_cert = builder.sign(
            private_key=actual_signing_key,
            algorithm=hashes.SHA256(),
        )
        logger.debug("📜📝✅ Certificate signed successfully")
        return signed_cert

    except Exception as e:
        logger.error(
            f"📜❌ create_x509_certificate: Failed: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError("Failed to create X.509 certificate object") from e


def x_create_x509_certificate__mutmut_122(
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
            logger.debug(f"📜📝✅ Added SANs: {alt_names or []}")

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
                    x509.ExtendedKeyUsage(None),
                    critical=False,
                )

        logger.debug(
            f"📜📝✅ Added BasicConstraints (is_ca={is_ca}), "
            f"KeyUsage, ExtendedKeyUsage (is_client_cert={is_client_cert})",
        )

        signed_cert = builder.sign(
            private_key=actual_signing_key,
            algorithm=hashes.SHA256(),
        )
        logger.debug("📜📝✅ Certificate signed successfully")
        return signed_cert

    except Exception as e:
        logger.error(
            f"📜❌ create_x509_certificate: Failed: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError("Failed to create X.509 certificate object") from e


def x_create_x509_certificate__mutmut_123(
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
            logger.debug(f"📜📝✅ Added SANs: {alt_names or []}")

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
                    critical=True,
                )

        logger.debug(
            f"📜📝✅ Added BasicConstraints (is_ca={is_ca}), "
            f"KeyUsage, ExtendedKeyUsage (is_client_cert={is_client_cert})",
        )

        signed_cert = builder.sign(
            private_key=actual_signing_key,
            algorithm=hashes.SHA256(),
        )
        logger.debug("📜📝✅ Certificate signed successfully")
        return signed_cert

    except Exception as e:
        logger.error(
            f"📜❌ create_x509_certificate: Failed: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError("Failed to create X.509 certificate object") from e


def x_create_x509_certificate__mutmut_124(
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
            logger.debug(f"📜📝✅ Added SANs: {alt_names or []}")

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
            None,
        )

        signed_cert = builder.sign(
            private_key=actual_signing_key,
            algorithm=hashes.SHA256(),
        )
        logger.debug("📜📝✅ Certificate signed successfully")
        return signed_cert

    except Exception as e:
        logger.error(
            f"📜❌ create_x509_certificate: Failed: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError("Failed to create X.509 certificate object") from e


def x_create_x509_certificate__mutmut_125(
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
            logger.debug(f"📜📝✅ Added SANs: {alt_names or []}")

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
            f"📜📝✅ Added BasicConstraints (is_ca={is_ca}), "
            f"KeyUsage, ExtendedKeyUsage (is_client_cert={is_client_cert})",
        )

        signed_cert = None
        logger.debug("📜📝✅ Certificate signed successfully")
        return signed_cert

    except Exception as e:
        logger.error(
            f"📜❌ create_x509_certificate: Failed: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError("Failed to create X.509 certificate object") from e


def x_create_x509_certificate__mutmut_126(
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
            logger.debug(f"📜📝✅ Added SANs: {alt_names or []}")

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
            f"📜📝✅ Added BasicConstraints (is_ca={is_ca}), "
            f"KeyUsage, ExtendedKeyUsage (is_client_cert={is_client_cert})",
        )

        signed_cert = builder.sign(
            private_key=None,
            algorithm=hashes.SHA256(),
        )
        logger.debug("📜📝✅ Certificate signed successfully")
        return signed_cert

    except Exception as e:
        logger.error(
            f"📜❌ create_x509_certificate: Failed: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError("Failed to create X.509 certificate object") from e


def x_create_x509_certificate__mutmut_127(
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
            logger.debug(f"📜📝✅ Added SANs: {alt_names or []}")

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
            f"📜📝✅ Added BasicConstraints (is_ca={is_ca}), "
            f"KeyUsage, ExtendedKeyUsage (is_client_cert={is_client_cert})",
        )

        signed_cert = builder.sign(
            private_key=actual_signing_key,
            algorithm=None,
        )
        logger.debug("📜📝✅ Certificate signed successfully")
        return signed_cert

    except Exception as e:
        logger.error(
            f"📜❌ create_x509_certificate: Failed: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError("Failed to create X.509 certificate object") from e


def x_create_x509_certificate__mutmut_128(
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
            logger.debug(f"📜📝✅ Added SANs: {alt_names or []}")

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
            f"📜📝✅ Added BasicConstraints (is_ca={is_ca}), "
            f"KeyUsage, ExtendedKeyUsage (is_client_cert={is_client_cert})",
        )

        signed_cert = builder.sign(
            algorithm=hashes.SHA256(),
        )
        logger.debug("📜📝✅ Certificate signed successfully")
        return signed_cert

    except Exception as e:
        logger.error(
            f"📜❌ create_x509_certificate: Failed: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError("Failed to create X.509 certificate object") from e


def x_create_x509_certificate__mutmut_129(
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
            logger.debug(f"📜📝✅ Added SANs: {alt_names or []}")

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
            f"📜📝✅ Added BasicConstraints (is_ca={is_ca}), "
            f"KeyUsage, ExtendedKeyUsage (is_client_cert={is_client_cert})",
        )

        signed_cert = builder.sign(
            private_key=actual_signing_key,
            )
        logger.debug("📜📝✅ Certificate signed successfully")
        return signed_cert

    except Exception as e:
        logger.error(
            f"📜❌ create_x509_certificate: Failed: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError("Failed to create X.509 certificate object") from e


def x_create_x509_certificate__mutmut_130(
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
            logger.debug(f"📜📝✅ Added SANs: {alt_names or []}")

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
            f"📜📝✅ Added BasicConstraints (is_ca={is_ca}), "
            f"KeyUsage, ExtendedKeyUsage (is_client_cert={is_client_cert})",
        )

        signed_cert = builder.sign(
            private_key=actual_signing_key,
            algorithm=hashes.SHA256(),
        )
        logger.debug(None)
        return signed_cert

    except Exception as e:
        logger.error(
            f"📜❌ create_x509_certificate: Failed: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError("Failed to create X.509 certificate object") from e


def x_create_x509_certificate__mutmut_131(
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
            logger.debug(f"📜📝✅ Added SANs: {alt_names or []}")

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
            f"📜📝✅ Added BasicConstraints (is_ca={is_ca}), "
            f"KeyUsage, ExtendedKeyUsage (is_client_cert={is_client_cert})",
        )

        signed_cert = builder.sign(
            private_key=actual_signing_key,
            algorithm=hashes.SHA256(),
        )
        logger.debug("XX📜📝✅ Certificate signed successfullyXX")
        return signed_cert

    except Exception as e:
        logger.error(
            f"📜❌ create_x509_certificate: Failed: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError("Failed to create X.509 certificate object") from e


def x_create_x509_certificate__mutmut_132(
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
            logger.debug(f"📜📝✅ Added SANs: {alt_names or []}")

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
            f"📜📝✅ Added BasicConstraints (is_ca={is_ca}), "
            f"KeyUsage, ExtendedKeyUsage (is_client_cert={is_client_cert})",
        )

        signed_cert = builder.sign(
            private_key=actual_signing_key,
            algorithm=hashes.SHA256(),
        )
        logger.debug("📜📝✅ certificate signed successfully")
        return signed_cert

    except Exception as e:
        logger.error(
            f"📜❌ create_x509_certificate: Failed: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError("Failed to create X.509 certificate object") from e


def x_create_x509_certificate__mutmut_133(
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
            logger.debug(f"📜📝✅ Added SANs: {alt_names or []}")

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
            f"📜📝✅ Added BasicConstraints (is_ca={is_ca}), "
            f"KeyUsage, ExtendedKeyUsage (is_client_cert={is_client_cert})",
        )

        signed_cert = builder.sign(
            private_key=actual_signing_key,
            algorithm=hashes.SHA256(),
        )
        logger.debug("📜📝✅ CERTIFICATE SIGNED SUCCESSFULLY")
        return signed_cert

    except Exception as e:
        logger.error(
            f"📜❌ create_x509_certificate: Failed: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError("Failed to create X.509 certificate object") from e


def x_create_x509_certificate__mutmut_134(
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
            logger.debug(f"📜📝✅ Added SANs: {alt_names or []}")

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
            f"📜📝✅ Added BasicConstraints (is_ca={is_ca}), "
            f"KeyUsage, ExtendedKeyUsage (is_client_cert={is_client_cert})",
        )

        signed_cert = builder.sign(
            private_key=actual_signing_key,
            algorithm=hashes.SHA256(),
        )
        logger.debug("📜📝✅ Certificate signed successfully")
        return signed_cert

    except Exception as e:
        logger.error(
            None,
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError("Failed to create X.509 certificate object") from e


def x_create_x509_certificate__mutmut_135(
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
            logger.debug(f"📜📝✅ Added SANs: {alt_names or []}")

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
            f"📜📝✅ Added BasicConstraints (is_ca={is_ca}), "
            f"KeyUsage, ExtendedKeyUsage (is_client_cert={is_client_cert})",
        )

        signed_cert = builder.sign(
            private_key=actual_signing_key,
            algorithm=hashes.SHA256(),
        )
        logger.debug("📜📝✅ Certificate signed successfully")
        return signed_cert

    except Exception as e:
        logger.error(
            f"📜❌ create_x509_certificate: Failed: {e}",
            extra=None,
        )
        raise CertificateError("Failed to create X.509 certificate object") from e


def x_create_x509_certificate__mutmut_136(
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
            logger.debug(f"📜📝✅ Added SANs: {alt_names or []}")

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
            f"📜📝✅ Added BasicConstraints (is_ca={is_ca}), "
            f"KeyUsage, ExtendedKeyUsage (is_client_cert={is_client_cert})",
        )

        signed_cert = builder.sign(
            private_key=actual_signing_key,
            algorithm=hashes.SHA256(),
        )
        logger.debug("📜📝✅ Certificate signed successfully")
        return signed_cert

    except Exception as e:
        logger.error(
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError("Failed to create X.509 certificate object") from e


def x_create_x509_certificate__mutmut_137(
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
            logger.debug(f"📜📝✅ Added SANs: {alt_names or []}")

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
            f"📜📝✅ Added BasicConstraints (is_ca={is_ca}), "
            f"KeyUsage, ExtendedKeyUsage (is_client_cert={is_client_cert})",
        )

        signed_cert = builder.sign(
            private_key=actual_signing_key,
            algorithm=hashes.SHA256(),
        )
        logger.debug("📜📝✅ Certificate signed successfully")
        return signed_cert

    except Exception as e:
        logger.error(
            f"📜❌ create_x509_certificate: Failed: {e}",
            )
        raise CertificateError("Failed to create X.509 certificate object") from e


def x_create_x509_certificate__mutmut_138(
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
            logger.debug(f"📜📝✅ Added SANs: {alt_names or []}")

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
            f"📜📝✅ Added BasicConstraints (is_ca={is_ca}), "
            f"KeyUsage, ExtendedKeyUsage (is_client_cert={is_client_cert})",
        )

        signed_cert = builder.sign(
            private_key=actual_signing_key,
            algorithm=hashes.SHA256(),
        )
        logger.debug("📜📝✅ Certificate signed successfully")
        return signed_cert

    except Exception as e:
        logger.error(
            f"📜❌ create_x509_certificate: Failed: {e}",
            extra={"XXerrorXX": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError("Failed to create X.509 certificate object") from e


def x_create_x509_certificate__mutmut_139(
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
            logger.debug(f"📜📝✅ Added SANs: {alt_names or []}")

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
            f"📜📝✅ Added BasicConstraints (is_ca={is_ca}), "
            f"KeyUsage, ExtendedKeyUsage (is_client_cert={is_client_cert})",
        )

        signed_cert = builder.sign(
            private_key=actual_signing_key,
            algorithm=hashes.SHA256(),
        )
        logger.debug("📜📝✅ Certificate signed successfully")
        return signed_cert

    except Exception as e:
        logger.error(
            f"📜❌ create_x509_certificate: Failed: {e}",
            extra={"ERROR": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError("Failed to create X.509 certificate object") from e


def x_create_x509_certificate__mutmut_140(
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
            logger.debug(f"📜📝✅ Added SANs: {alt_names or []}")

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
            f"📜📝✅ Added BasicConstraints (is_ca={is_ca}), "
            f"KeyUsage, ExtendedKeyUsage (is_client_cert={is_client_cert})",
        )

        signed_cert = builder.sign(
            private_key=actual_signing_key,
            algorithm=hashes.SHA256(),
        )
        logger.debug("📜📝✅ Certificate signed successfully")
        return signed_cert

    except Exception as e:
        logger.error(
            f"📜❌ create_x509_certificate: Failed: {e}",
            extra={"error": str(None), "trace": traceback.format_exc()},
        )
        raise CertificateError("Failed to create X.509 certificate object") from e


def x_create_x509_certificate__mutmut_141(
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
            logger.debug(f"📜📝✅ Added SANs: {alt_names or []}")

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
            f"📜📝✅ Added BasicConstraints (is_ca={is_ca}), "
            f"KeyUsage, ExtendedKeyUsage (is_client_cert={is_client_cert})",
        )

        signed_cert = builder.sign(
            private_key=actual_signing_key,
            algorithm=hashes.SHA256(),
        )
        logger.debug("📜📝✅ Certificate signed successfully")
        return signed_cert

    except Exception as e:
        logger.error(
            f"📜❌ create_x509_certificate: Failed: {e}",
            extra={"error": str(e), "XXtraceXX": traceback.format_exc()},
        )
        raise CertificateError("Failed to create X.509 certificate object") from e


def x_create_x509_certificate__mutmut_142(
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
            logger.debug(f"📜📝✅ Added SANs: {alt_names or []}")

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
            f"📜📝✅ Added BasicConstraints (is_ca={is_ca}), "
            f"KeyUsage, ExtendedKeyUsage (is_client_cert={is_client_cert})",
        )

        signed_cert = builder.sign(
            private_key=actual_signing_key,
            algorithm=hashes.SHA256(),
        )
        logger.debug("📜📝✅ Certificate signed successfully")
        return signed_cert

    except Exception as e:
        logger.error(
            f"📜❌ create_x509_certificate: Failed: {e}",
            extra={"error": str(e), "TRACE": traceback.format_exc()},
        )
        raise CertificateError("Failed to create X.509 certificate object") from e


def x_create_x509_certificate__mutmut_143(
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
            logger.debug(f"📜📝✅ Added SANs: {alt_names or []}")

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
            f"📜📝✅ Added BasicConstraints (is_ca={is_ca}), "
            f"KeyUsage, ExtendedKeyUsage (is_client_cert={is_client_cert})",
        )

        signed_cert = builder.sign(
            private_key=actual_signing_key,
            algorithm=hashes.SHA256(),
        )
        logger.debug("📜📝✅ Certificate signed successfully")
        return signed_cert

    except Exception as e:
        logger.error(
            f"📜❌ create_x509_certificate: Failed: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError(None) from e


def x_create_x509_certificate__mutmut_144(
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
            logger.debug(f"📜📝✅ Added SANs: {alt_names or []}")

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
            f"📜📝✅ Added BasicConstraints (is_ca={is_ca}), "
            f"KeyUsage, ExtendedKeyUsage (is_client_cert={is_client_cert})",
        )

        signed_cert = builder.sign(
            private_key=actual_signing_key,
            algorithm=hashes.SHA256(),
        )
        logger.debug("📜📝✅ Certificate signed successfully")
        return signed_cert

    except Exception as e:
        logger.error(
            f"📜❌ create_x509_certificate: Failed: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError("XXFailed to create X.509 certificate objectXX") from e


def x_create_x509_certificate__mutmut_145(
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
            logger.debug(f"📜📝✅ Added SANs: {alt_names or []}")

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
            f"📜📝✅ Added BasicConstraints (is_ca={is_ca}), "
            f"KeyUsage, ExtendedKeyUsage (is_client_cert={is_client_cert})",
        )

        signed_cert = builder.sign(
            private_key=actual_signing_key,
            algorithm=hashes.SHA256(),
        )
        logger.debug("📜📝✅ Certificate signed successfully")
        return signed_cert

    except Exception as e:
        logger.error(
            f"📜❌ create_x509_certificate: Failed: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError("failed to create x.509 certificate object") from e


def x_create_x509_certificate__mutmut_146(
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
            logger.debug(f"📜📝✅ Added SANs: {alt_names or []}")

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
            f"📜📝✅ Added BasicConstraints (is_ca={is_ca}), "
            f"KeyUsage, ExtendedKeyUsage (is_client_cert={is_client_cert})",
        )

        signed_cert = builder.sign(
            private_key=actual_signing_key,
            algorithm=hashes.SHA256(),
        )
        logger.debug("📜📝✅ Certificate signed successfully")
        return signed_cert

    except Exception as e:
        logger.error(
            f"📜❌ create_x509_certificate: Failed: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError("FAILED TO CREATE X.509 CERTIFICATE OBJECT") from e

x_create_x509_certificate__mutmut_mutants : ClassVar[MutantDict] = {
'x_create_x509_certificate__mutmut_1': x_create_x509_certificate__mutmut_1, 
    'x_create_x509_certificate__mutmut_2': x_create_x509_certificate__mutmut_2, 
    'x_create_x509_certificate__mutmut_3': x_create_x509_certificate__mutmut_3, 
    'x_create_x509_certificate__mutmut_4': x_create_x509_certificate__mutmut_4, 
    'x_create_x509_certificate__mutmut_5': x_create_x509_certificate__mutmut_5, 
    'x_create_x509_certificate__mutmut_6': x_create_x509_certificate__mutmut_6, 
    'x_create_x509_certificate__mutmut_7': x_create_x509_certificate__mutmut_7, 
    'x_create_x509_certificate__mutmut_8': x_create_x509_certificate__mutmut_8, 
    'x_create_x509_certificate__mutmut_9': x_create_x509_certificate__mutmut_9, 
    'x_create_x509_certificate__mutmut_10': x_create_x509_certificate__mutmut_10, 
    'x_create_x509_certificate__mutmut_11': x_create_x509_certificate__mutmut_11, 
    'x_create_x509_certificate__mutmut_12': x_create_x509_certificate__mutmut_12, 
    'x_create_x509_certificate__mutmut_13': x_create_x509_certificate__mutmut_13, 
    'x_create_x509_certificate__mutmut_14': x_create_x509_certificate__mutmut_14, 
    'x_create_x509_certificate__mutmut_15': x_create_x509_certificate__mutmut_15, 
    'x_create_x509_certificate__mutmut_16': x_create_x509_certificate__mutmut_16, 
    'x_create_x509_certificate__mutmut_17': x_create_x509_certificate__mutmut_17, 
    'x_create_x509_certificate__mutmut_18': x_create_x509_certificate__mutmut_18, 
    'x_create_x509_certificate__mutmut_19': x_create_x509_certificate__mutmut_19, 
    'x_create_x509_certificate__mutmut_20': x_create_x509_certificate__mutmut_20, 
    'x_create_x509_certificate__mutmut_21': x_create_x509_certificate__mutmut_21, 
    'x_create_x509_certificate__mutmut_22': x_create_x509_certificate__mutmut_22, 
    'x_create_x509_certificate__mutmut_23': x_create_x509_certificate__mutmut_23, 
    'x_create_x509_certificate__mutmut_24': x_create_x509_certificate__mutmut_24, 
    'x_create_x509_certificate__mutmut_25': x_create_x509_certificate__mutmut_25, 
    'x_create_x509_certificate__mutmut_26': x_create_x509_certificate__mutmut_26, 
    'x_create_x509_certificate__mutmut_27': x_create_x509_certificate__mutmut_27, 
    'x_create_x509_certificate__mutmut_28': x_create_x509_certificate__mutmut_28, 
    'x_create_x509_certificate__mutmut_29': x_create_x509_certificate__mutmut_29, 
    'x_create_x509_certificate__mutmut_30': x_create_x509_certificate__mutmut_30, 
    'x_create_x509_certificate__mutmut_31': x_create_x509_certificate__mutmut_31, 
    'x_create_x509_certificate__mutmut_32': x_create_x509_certificate__mutmut_32, 
    'x_create_x509_certificate__mutmut_33': x_create_x509_certificate__mutmut_33, 
    'x_create_x509_certificate__mutmut_34': x_create_x509_certificate__mutmut_34, 
    'x_create_x509_certificate__mutmut_35': x_create_x509_certificate__mutmut_35, 
    'x_create_x509_certificate__mutmut_36': x_create_x509_certificate__mutmut_36, 
    'x_create_x509_certificate__mutmut_37': x_create_x509_certificate__mutmut_37, 
    'x_create_x509_certificate__mutmut_38': x_create_x509_certificate__mutmut_38, 
    'x_create_x509_certificate__mutmut_39': x_create_x509_certificate__mutmut_39, 
    'x_create_x509_certificate__mutmut_40': x_create_x509_certificate__mutmut_40, 
    'x_create_x509_certificate__mutmut_41': x_create_x509_certificate__mutmut_41, 
    'x_create_x509_certificate__mutmut_42': x_create_x509_certificate__mutmut_42, 
    'x_create_x509_certificate__mutmut_43': x_create_x509_certificate__mutmut_43, 
    'x_create_x509_certificate__mutmut_44': x_create_x509_certificate__mutmut_44, 
    'x_create_x509_certificate__mutmut_45': x_create_x509_certificate__mutmut_45, 
    'x_create_x509_certificate__mutmut_46': x_create_x509_certificate__mutmut_46, 
    'x_create_x509_certificate__mutmut_47': x_create_x509_certificate__mutmut_47, 
    'x_create_x509_certificate__mutmut_48': x_create_x509_certificate__mutmut_48, 
    'x_create_x509_certificate__mutmut_49': x_create_x509_certificate__mutmut_49, 
    'x_create_x509_certificate__mutmut_50': x_create_x509_certificate__mutmut_50, 
    'x_create_x509_certificate__mutmut_51': x_create_x509_certificate__mutmut_51, 
    'x_create_x509_certificate__mutmut_52': x_create_x509_certificate__mutmut_52, 
    'x_create_x509_certificate__mutmut_53': x_create_x509_certificate__mutmut_53, 
    'x_create_x509_certificate__mutmut_54': x_create_x509_certificate__mutmut_54, 
    'x_create_x509_certificate__mutmut_55': x_create_x509_certificate__mutmut_55, 
    'x_create_x509_certificate__mutmut_56': x_create_x509_certificate__mutmut_56, 
    'x_create_x509_certificate__mutmut_57': x_create_x509_certificate__mutmut_57, 
    'x_create_x509_certificate__mutmut_58': x_create_x509_certificate__mutmut_58, 
    'x_create_x509_certificate__mutmut_59': x_create_x509_certificate__mutmut_59, 
    'x_create_x509_certificate__mutmut_60': x_create_x509_certificate__mutmut_60, 
    'x_create_x509_certificate__mutmut_61': x_create_x509_certificate__mutmut_61, 
    'x_create_x509_certificate__mutmut_62': x_create_x509_certificate__mutmut_62, 
    'x_create_x509_certificate__mutmut_63': x_create_x509_certificate__mutmut_63, 
    'x_create_x509_certificate__mutmut_64': x_create_x509_certificate__mutmut_64, 
    'x_create_x509_certificate__mutmut_65': x_create_x509_certificate__mutmut_65, 
    'x_create_x509_certificate__mutmut_66': x_create_x509_certificate__mutmut_66, 
    'x_create_x509_certificate__mutmut_67': x_create_x509_certificate__mutmut_67, 
    'x_create_x509_certificate__mutmut_68': x_create_x509_certificate__mutmut_68, 
    'x_create_x509_certificate__mutmut_69': x_create_x509_certificate__mutmut_69, 
    'x_create_x509_certificate__mutmut_70': x_create_x509_certificate__mutmut_70, 
    'x_create_x509_certificate__mutmut_71': x_create_x509_certificate__mutmut_71, 
    'x_create_x509_certificate__mutmut_72': x_create_x509_certificate__mutmut_72, 
    'x_create_x509_certificate__mutmut_73': x_create_x509_certificate__mutmut_73, 
    'x_create_x509_certificate__mutmut_74': x_create_x509_certificate__mutmut_74, 
    'x_create_x509_certificate__mutmut_75': x_create_x509_certificate__mutmut_75, 
    'x_create_x509_certificate__mutmut_76': x_create_x509_certificate__mutmut_76, 
    'x_create_x509_certificate__mutmut_77': x_create_x509_certificate__mutmut_77, 
    'x_create_x509_certificate__mutmut_78': x_create_x509_certificate__mutmut_78, 
    'x_create_x509_certificate__mutmut_79': x_create_x509_certificate__mutmut_79, 
    'x_create_x509_certificate__mutmut_80': x_create_x509_certificate__mutmut_80, 
    'x_create_x509_certificate__mutmut_81': x_create_x509_certificate__mutmut_81, 
    'x_create_x509_certificate__mutmut_82': x_create_x509_certificate__mutmut_82, 
    'x_create_x509_certificate__mutmut_83': x_create_x509_certificate__mutmut_83, 
    'x_create_x509_certificate__mutmut_84': x_create_x509_certificate__mutmut_84, 
    'x_create_x509_certificate__mutmut_85': x_create_x509_certificate__mutmut_85, 
    'x_create_x509_certificate__mutmut_86': x_create_x509_certificate__mutmut_86, 
    'x_create_x509_certificate__mutmut_87': x_create_x509_certificate__mutmut_87, 
    'x_create_x509_certificate__mutmut_88': x_create_x509_certificate__mutmut_88, 
    'x_create_x509_certificate__mutmut_89': x_create_x509_certificate__mutmut_89, 
    'x_create_x509_certificate__mutmut_90': x_create_x509_certificate__mutmut_90, 
    'x_create_x509_certificate__mutmut_91': x_create_x509_certificate__mutmut_91, 
    'x_create_x509_certificate__mutmut_92': x_create_x509_certificate__mutmut_92, 
    'x_create_x509_certificate__mutmut_93': x_create_x509_certificate__mutmut_93, 
    'x_create_x509_certificate__mutmut_94': x_create_x509_certificate__mutmut_94, 
    'x_create_x509_certificate__mutmut_95': x_create_x509_certificate__mutmut_95, 
    'x_create_x509_certificate__mutmut_96': x_create_x509_certificate__mutmut_96, 
    'x_create_x509_certificate__mutmut_97': x_create_x509_certificate__mutmut_97, 
    'x_create_x509_certificate__mutmut_98': x_create_x509_certificate__mutmut_98, 
    'x_create_x509_certificate__mutmut_99': x_create_x509_certificate__mutmut_99, 
    'x_create_x509_certificate__mutmut_100': x_create_x509_certificate__mutmut_100, 
    'x_create_x509_certificate__mutmut_101': x_create_x509_certificate__mutmut_101, 
    'x_create_x509_certificate__mutmut_102': x_create_x509_certificate__mutmut_102, 
    'x_create_x509_certificate__mutmut_103': x_create_x509_certificate__mutmut_103, 
    'x_create_x509_certificate__mutmut_104': x_create_x509_certificate__mutmut_104, 
    'x_create_x509_certificate__mutmut_105': x_create_x509_certificate__mutmut_105, 
    'x_create_x509_certificate__mutmut_106': x_create_x509_certificate__mutmut_106, 
    'x_create_x509_certificate__mutmut_107': x_create_x509_certificate__mutmut_107, 
    'x_create_x509_certificate__mutmut_108': x_create_x509_certificate__mutmut_108, 
    'x_create_x509_certificate__mutmut_109': x_create_x509_certificate__mutmut_109, 
    'x_create_x509_certificate__mutmut_110': x_create_x509_certificate__mutmut_110, 
    'x_create_x509_certificate__mutmut_111': x_create_x509_certificate__mutmut_111, 
    'x_create_x509_certificate__mutmut_112': x_create_x509_certificate__mutmut_112, 
    'x_create_x509_certificate__mutmut_113': x_create_x509_certificate__mutmut_113, 
    'x_create_x509_certificate__mutmut_114': x_create_x509_certificate__mutmut_114, 
    'x_create_x509_certificate__mutmut_115': x_create_x509_certificate__mutmut_115, 
    'x_create_x509_certificate__mutmut_116': x_create_x509_certificate__mutmut_116, 
    'x_create_x509_certificate__mutmut_117': x_create_x509_certificate__mutmut_117, 
    'x_create_x509_certificate__mutmut_118': x_create_x509_certificate__mutmut_118, 
    'x_create_x509_certificate__mutmut_119': x_create_x509_certificate__mutmut_119, 
    'x_create_x509_certificate__mutmut_120': x_create_x509_certificate__mutmut_120, 
    'x_create_x509_certificate__mutmut_121': x_create_x509_certificate__mutmut_121, 
    'x_create_x509_certificate__mutmut_122': x_create_x509_certificate__mutmut_122, 
    'x_create_x509_certificate__mutmut_123': x_create_x509_certificate__mutmut_123, 
    'x_create_x509_certificate__mutmut_124': x_create_x509_certificate__mutmut_124, 
    'x_create_x509_certificate__mutmut_125': x_create_x509_certificate__mutmut_125, 
    'x_create_x509_certificate__mutmut_126': x_create_x509_certificate__mutmut_126, 
    'x_create_x509_certificate__mutmut_127': x_create_x509_certificate__mutmut_127, 
    'x_create_x509_certificate__mutmut_128': x_create_x509_certificate__mutmut_128, 
    'x_create_x509_certificate__mutmut_129': x_create_x509_certificate__mutmut_129, 
    'x_create_x509_certificate__mutmut_130': x_create_x509_certificate__mutmut_130, 
    'x_create_x509_certificate__mutmut_131': x_create_x509_certificate__mutmut_131, 
    'x_create_x509_certificate__mutmut_132': x_create_x509_certificate__mutmut_132, 
    'x_create_x509_certificate__mutmut_133': x_create_x509_certificate__mutmut_133, 
    'x_create_x509_certificate__mutmut_134': x_create_x509_certificate__mutmut_134, 
    'x_create_x509_certificate__mutmut_135': x_create_x509_certificate__mutmut_135, 
    'x_create_x509_certificate__mutmut_136': x_create_x509_certificate__mutmut_136, 
    'x_create_x509_certificate__mutmut_137': x_create_x509_certificate__mutmut_137, 
    'x_create_x509_certificate__mutmut_138': x_create_x509_certificate__mutmut_138, 
    'x_create_x509_certificate__mutmut_139': x_create_x509_certificate__mutmut_139, 
    'x_create_x509_certificate__mutmut_140': x_create_x509_certificate__mutmut_140, 
    'x_create_x509_certificate__mutmut_141': x_create_x509_certificate__mutmut_141, 
    'x_create_x509_certificate__mutmut_142': x_create_x509_certificate__mutmut_142, 
    'x_create_x509_certificate__mutmut_143': x_create_x509_certificate__mutmut_143, 
    'x_create_x509_certificate__mutmut_144': x_create_x509_certificate__mutmut_144, 
    'x_create_x509_certificate__mutmut_145': x_create_x509_certificate__mutmut_145, 
    'x_create_x509_certificate__mutmut_146': x_create_x509_certificate__mutmut_146
}

def create_x509_certificate(*args, **kwargs):
    result = _mutmut_trampoline(x_create_x509_certificate__mutmut_orig, x_create_x509_certificate__mutmut_mutants, args, kwargs)
    return result 

create_x509_certificate.__signature__ = _mutmut_signature(x_create_x509_certificate__mutmut_orig)
x_create_x509_certificate__mutmut_orig.__name__ = 'x_create_x509_certificate'


def x_validate_signature__mutmut_orig(
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


def x_validate_signature__mutmut_1(
    signed_cert_obj: X509Certificate,
    signing_cert_obj: X509Certificate,
    signing_public_key: PublicKey,
) -> bool:
    """Internal helper: Validates signature and issuer/subject match."""
    if signed_cert_obj.issuer == signing_cert_obj.subject:
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


def x_validate_signature__mutmut_2(
    signed_cert_obj: X509Certificate,
    signing_cert_obj: X509Certificate,
    signing_public_key: PublicKey,
) -> bool:
    """Internal helper: Validates signature and issuer/subject match."""
    if signed_cert_obj.issuer != signing_cert_obj.subject:
        logger.debug(
            None,
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


def x_validate_signature__mutmut_3(
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
        return True

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


def x_validate_signature__mutmut_4(
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
        if signing_public_key:
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


def x_validate_signature__mutmut_5(
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
            logger.error(None)
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


def x_validate_signature__mutmut_6(
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
            logger.error("XX📜🔍❌ Cannot validate signature: Signing certificate has no public keyXX")
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


def x_validate_signature__mutmut_7(
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
            logger.error("📜🔍❌ cannot validate signature: signing certificate has no public key")
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


def x_validate_signature__mutmut_8(
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
            logger.error("📜🔍❌ CANNOT VALIDATE SIGNATURE: SIGNING CERTIFICATE HAS NO PUBLIC KEY")
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


def x_validate_signature__mutmut_9(
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
            return True

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


def x_validate_signature__mutmut_10(
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

        signature = None
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


def x_validate_signature__mutmut_11(
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
        tbs_certificate_bytes = None
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


def x_validate_signature__mutmut_12(
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
        signature_hash_algorithm = None

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


def x_validate_signature__mutmut_13(
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

        if signature_hash_algorithm:
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


def x_validate_signature__mutmut_14(
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
            logger.error(None)
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


def x_validate_signature__mutmut_15(
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
            logger.error("XX📜🔍❌ Cannot validate signature: Unknown hash algorithmXX")
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


def x_validate_signature__mutmut_16(
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
            logger.error("📜🔍❌ cannot validate signature: unknown hash algorithm")
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


def x_validate_signature__mutmut_17(
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
            logger.error("📜🔍❌ CANNOT VALIDATE SIGNATURE: UNKNOWN HASH ALGORITHM")
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


def x_validate_signature__mutmut_18(
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
            return True

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


def x_validate_signature__mutmut_19(
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
                None,
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


def x_validate_signature__mutmut_20(
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
                None,
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


def x_validate_signature__mutmut_21(
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
                None,
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


def x_validate_signature__mutmut_22(
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
                None,
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


def x_validate_signature__mutmut_23(
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


def x_validate_signature__mutmut_24(
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


def x_validate_signature__mutmut_25(
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


def x_validate_signature__mutmut_26(
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


def x_validate_signature__mutmut_27(
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
            cast(None, signing_public_key).verify(
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


def x_validate_signature__mutmut_28(
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
            cast("rsa.RSAPublicKey", None).verify(
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


def x_validate_signature__mutmut_29(
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
            cast(signing_public_key).verify(
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


def x_validate_signature__mutmut_30(
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
            cast("rsa.RSAPublicKey", ).verify(
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


def x_validate_signature__mutmut_31(
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
            cast("XXrsa.RSAPublicKeyXX", signing_public_key).verify(
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


def x_validate_signature__mutmut_32(
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
            cast("rsa.rsapublickey", signing_public_key).verify(
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


def x_validate_signature__mutmut_33(
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
            cast("RSA.RSAPUBLICKEY", signing_public_key).verify(
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


def x_validate_signature__mutmut_34(
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
                None,
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


def x_validate_signature__mutmut_35(
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
                None,
                ec.ECDSA(signature_hash_algorithm),
            )
        else:
            logger.error(f"📜🔍❌ Unsupported signing public key type: {type(signing_public_key)}")
            return False

        return True

    except Exception as e:
        logger.debug(f"📜🔍❌ Signature validation failed: {type(e).__name__}: {e}")
        return False


def x_validate_signature__mutmut_36(
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
                None,
            )
        else:
            logger.error(f"📜🔍❌ Unsupported signing public key type: {type(signing_public_key)}")
            return False

        return True

    except Exception as e:
        logger.debug(f"📜🔍❌ Signature validation failed: {type(e).__name__}: {e}")
        return False


def x_validate_signature__mutmut_37(
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


def x_validate_signature__mutmut_38(
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
                ec.ECDSA(signature_hash_algorithm),
            )
        else:
            logger.error(f"📜🔍❌ Unsupported signing public key type: {type(signing_public_key)}")
            return False

        return True

    except Exception as e:
        logger.debug(f"📜🔍❌ Signature validation failed: {type(e).__name__}: {e}")
        return False


def x_validate_signature__mutmut_39(
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
                )
        else:
            logger.error(f"📜🔍❌ Unsupported signing public key type: {type(signing_public_key)}")
            return False

        return True

    except Exception as e:
        logger.debug(f"📜🔍❌ Signature validation failed: {type(e).__name__}: {e}")
        return False


def x_validate_signature__mutmut_40(
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
            cast(None, signing_public_key).verify(
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


def x_validate_signature__mutmut_41(
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
            cast("ec.EllipticCurvePublicKey", None).verify(
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


def x_validate_signature__mutmut_42(
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
            cast(signing_public_key).verify(
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


def x_validate_signature__mutmut_43(
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
            cast("ec.EllipticCurvePublicKey", ).verify(
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


def x_validate_signature__mutmut_44(
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
            cast("XXec.EllipticCurvePublicKeyXX", signing_public_key).verify(
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


def x_validate_signature__mutmut_45(
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
            cast("ec.ellipticcurvepublickey", signing_public_key).verify(
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


def x_validate_signature__mutmut_46(
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
            cast("EC.ELLIPTICCURVEPUBLICKEY", signing_public_key).verify(
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


def x_validate_signature__mutmut_47(
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
                ec.ECDSA(None),
            )
        else:
            logger.error(f"📜🔍❌ Unsupported signing public key type: {type(signing_public_key)}")
            return False

        return True

    except Exception as e:
        logger.debug(f"📜🔍❌ Signature validation failed: {type(e).__name__}: {e}")
        return False


def x_validate_signature__mutmut_48(
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
            logger.error(None)
            return False

        return True

    except Exception as e:
        logger.debug(f"📜🔍❌ Signature validation failed: {type(e).__name__}: {e}")
        return False


def x_validate_signature__mutmut_49(
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
            logger.error(f"📜🔍❌ Unsupported signing public key type: {type(None)}")
            return False

        return True

    except Exception as e:
        logger.debug(f"📜🔍❌ Signature validation failed: {type(e).__name__}: {e}")
        return False


def x_validate_signature__mutmut_50(
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
            return True

        return True

    except Exception as e:
        logger.debug(f"📜🔍❌ Signature validation failed: {type(e).__name__}: {e}")
        return False


def x_validate_signature__mutmut_51(
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

        return False

    except Exception as e:
        logger.debug(f"📜🔍❌ Signature validation failed: {type(e).__name__}: {e}")
        return False


def x_validate_signature__mutmut_52(
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
        logger.debug(None)
        return False


def x_validate_signature__mutmut_53(
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
        logger.debug(f"📜🔍❌ Signature validation failed: {type(None).__name__}: {e}")
        return False


def x_validate_signature__mutmut_54(
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
        return True

x_validate_signature__mutmut_mutants : ClassVar[MutantDict] = {
'x_validate_signature__mutmut_1': x_validate_signature__mutmut_1, 
    'x_validate_signature__mutmut_2': x_validate_signature__mutmut_2, 
    'x_validate_signature__mutmut_3': x_validate_signature__mutmut_3, 
    'x_validate_signature__mutmut_4': x_validate_signature__mutmut_4, 
    'x_validate_signature__mutmut_5': x_validate_signature__mutmut_5, 
    'x_validate_signature__mutmut_6': x_validate_signature__mutmut_6, 
    'x_validate_signature__mutmut_7': x_validate_signature__mutmut_7, 
    'x_validate_signature__mutmut_8': x_validate_signature__mutmut_8, 
    'x_validate_signature__mutmut_9': x_validate_signature__mutmut_9, 
    'x_validate_signature__mutmut_10': x_validate_signature__mutmut_10, 
    'x_validate_signature__mutmut_11': x_validate_signature__mutmut_11, 
    'x_validate_signature__mutmut_12': x_validate_signature__mutmut_12, 
    'x_validate_signature__mutmut_13': x_validate_signature__mutmut_13, 
    'x_validate_signature__mutmut_14': x_validate_signature__mutmut_14, 
    'x_validate_signature__mutmut_15': x_validate_signature__mutmut_15, 
    'x_validate_signature__mutmut_16': x_validate_signature__mutmut_16, 
    'x_validate_signature__mutmut_17': x_validate_signature__mutmut_17, 
    'x_validate_signature__mutmut_18': x_validate_signature__mutmut_18, 
    'x_validate_signature__mutmut_19': x_validate_signature__mutmut_19, 
    'x_validate_signature__mutmut_20': x_validate_signature__mutmut_20, 
    'x_validate_signature__mutmut_21': x_validate_signature__mutmut_21, 
    'x_validate_signature__mutmut_22': x_validate_signature__mutmut_22, 
    'x_validate_signature__mutmut_23': x_validate_signature__mutmut_23, 
    'x_validate_signature__mutmut_24': x_validate_signature__mutmut_24, 
    'x_validate_signature__mutmut_25': x_validate_signature__mutmut_25, 
    'x_validate_signature__mutmut_26': x_validate_signature__mutmut_26, 
    'x_validate_signature__mutmut_27': x_validate_signature__mutmut_27, 
    'x_validate_signature__mutmut_28': x_validate_signature__mutmut_28, 
    'x_validate_signature__mutmut_29': x_validate_signature__mutmut_29, 
    'x_validate_signature__mutmut_30': x_validate_signature__mutmut_30, 
    'x_validate_signature__mutmut_31': x_validate_signature__mutmut_31, 
    'x_validate_signature__mutmut_32': x_validate_signature__mutmut_32, 
    'x_validate_signature__mutmut_33': x_validate_signature__mutmut_33, 
    'x_validate_signature__mutmut_34': x_validate_signature__mutmut_34, 
    'x_validate_signature__mutmut_35': x_validate_signature__mutmut_35, 
    'x_validate_signature__mutmut_36': x_validate_signature__mutmut_36, 
    'x_validate_signature__mutmut_37': x_validate_signature__mutmut_37, 
    'x_validate_signature__mutmut_38': x_validate_signature__mutmut_38, 
    'x_validate_signature__mutmut_39': x_validate_signature__mutmut_39, 
    'x_validate_signature__mutmut_40': x_validate_signature__mutmut_40, 
    'x_validate_signature__mutmut_41': x_validate_signature__mutmut_41, 
    'x_validate_signature__mutmut_42': x_validate_signature__mutmut_42, 
    'x_validate_signature__mutmut_43': x_validate_signature__mutmut_43, 
    'x_validate_signature__mutmut_44': x_validate_signature__mutmut_44, 
    'x_validate_signature__mutmut_45': x_validate_signature__mutmut_45, 
    'x_validate_signature__mutmut_46': x_validate_signature__mutmut_46, 
    'x_validate_signature__mutmut_47': x_validate_signature__mutmut_47, 
    'x_validate_signature__mutmut_48': x_validate_signature__mutmut_48, 
    'x_validate_signature__mutmut_49': x_validate_signature__mutmut_49, 
    'x_validate_signature__mutmut_50': x_validate_signature__mutmut_50, 
    'x_validate_signature__mutmut_51': x_validate_signature__mutmut_51, 
    'x_validate_signature__mutmut_52': x_validate_signature__mutmut_52, 
    'x_validate_signature__mutmut_53': x_validate_signature__mutmut_53, 
    'x_validate_signature__mutmut_54': x_validate_signature__mutmut_54
}

def validate_signature(*args, **kwargs):
    result = _mutmut_trampoline(x_validate_signature__mutmut_orig, x_validate_signature__mutmut_mutants, args, kwargs)
    return result 

validate_signature.__signature__ = _mutmut_signature(x_validate_signature__mutmut_orig)
x_validate_signature__mutmut_orig.__name__ = 'x_validate_signature'


# <3 🧱🤝🔒🪄
