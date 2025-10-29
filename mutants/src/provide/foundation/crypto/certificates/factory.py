# provide/foundation/crypto/certificates/factory.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

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


def x_create_ca_certificate__mutmut_orig(
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


def x_create_ca_certificate__mutmut_1(
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

    logger.info(None)
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


def x_create_ca_certificate__mutmut_2(
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
    ca_cert_obj = None
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


def x_create_ca_certificate__mutmut_3(
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
        common_name=None,
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


def x_create_ca_certificate__mutmut_4(
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
        organization_name=None,
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


def x_create_ca_certificate__mutmut_5(
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
        validity_days=None,
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


def x_create_ca_certificate__mutmut_6(
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
        key_type=None,
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


def x_create_ca_certificate__mutmut_7(
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
        key_size=None,
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


def x_create_ca_certificate__mutmut_8(
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
        ecdsa_curve=None,
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


def x_create_ca_certificate__mutmut_9(
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
        alt_names=None,
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


def x_create_ca_certificate__mutmut_10(
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
        is_ca=None,  # Will be re-signed with is_ca=True below
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


def x_create_ca_certificate__mutmut_11(
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
        is_client_cert=None,
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


def x_create_ca_certificate__mutmut_12(
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


def x_create_ca_certificate__mutmut_13(
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


def x_create_ca_certificate__mutmut_14(
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


def x_create_ca_certificate__mutmut_15(
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


def x_create_ca_certificate__mutmut_16(
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


def x_create_ca_certificate__mutmut_17(
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


def x_create_ca_certificate__mutmut_18(
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


def x_create_ca_certificate__mutmut_19(
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


def x_create_ca_certificate__mutmut_20(
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


def x_create_ca_certificate__mutmut_21(
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
        is_ca=True,  # Will be re-signed with is_ca=True below
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


def x_create_ca_certificate__mutmut_22(
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
        is_client_cert=True,
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


def x_create_ca_certificate__mutmut_23(
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
    logger.info(None)
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


def x_create_ca_certificate__mutmut_24(
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
    logger.info("XX📜🔑🏭 Re-signing generated CA certificate to ensure is_ca=TrueXX")
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


def x_create_ca_certificate__mutmut_25(
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
    logger.info("📜🔑🏭 re-signing generated ca certificate to ensure is_ca=true")
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


def x_create_ca_certificate__mutmut_26(
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
    logger.info("📜🔑🏭 RE-SIGNING GENERATED CA CERTIFICATE TO ENSURE IS_CA=TRUE")
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


def x_create_ca_certificate__mutmut_27(
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
    actual_ca_x509_cert = None
    ca_cert_obj._cert = actual_ca_x509_cert
    ca_cert_obj.cert_pem = actual_ca_x509_cert.public_bytes(serialization.Encoding.PEM).decode("utf-8")
    return ca_cert_obj


def x_create_ca_certificate__mutmut_28(
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
        base=None,
        private_key=ca_cert_obj._private_key,
        alt_names=ca_cert_obj.alt_names,
        is_ca=True,
        is_client_cert=False,
    )
    ca_cert_obj._cert = actual_ca_x509_cert
    ca_cert_obj.cert_pem = actual_ca_x509_cert.public_bytes(serialization.Encoding.PEM).decode("utf-8")
    return ca_cert_obj


def x_create_ca_certificate__mutmut_29(
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
        private_key=None,
        alt_names=ca_cert_obj.alt_names,
        is_ca=True,
        is_client_cert=False,
    )
    ca_cert_obj._cert = actual_ca_x509_cert
    ca_cert_obj.cert_pem = actual_ca_x509_cert.public_bytes(serialization.Encoding.PEM).decode("utf-8")
    return ca_cert_obj


def x_create_ca_certificate__mutmut_30(
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
        alt_names=None,
        is_ca=True,
        is_client_cert=False,
    )
    ca_cert_obj._cert = actual_ca_x509_cert
    ca_cert_obj.cert_pem = actual_ca_x509_cert.public_bytes(serialization.Encoding.PEM).decode("utf-8")
    return ca_cert_obj


def x_create_ca_certificate__mutmut_31(
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
        is_ca=None,
        is_client_cert=False,
    )
    ca_cert_obj._cert = actual_ca_x509_cert
    ca_cert_obj.cert_pem = actual_ca_x509_cert.public_bytes(serialization.Encoding.PEM).decode("utf-8")
    return ca_cert_obj


def x_create_ca_certificate__mutmut_32(
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
        is_client_cert=None,
    )
    ca_cert_obj._cert = actual_ca_x509_cert
    ca_cert_obj.cert_pem = actual_ca_x509_cert.public_bytes(serialization.Encoding.PEM).decode("utf-8")
    return ca_cert_obj


def x_create_ca_certificate__mutmut_33(
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
        private_key=ca_cert_obj._private_key,
        alt_names=ca_cert_obj.alt_names,
        is_ca=True,
        is_client_cert=False,
    )
    ca_cert_obj._cert = actual_ca_x509_cert
    ca_cert_obj.cert_pem = actual_ca_x509_cert.public_bytes(serialization.Encoding.PEM).decode("utf-8")
    return ca_cert_obj


def x_create_ca_certificate__mutmut_34(
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
        alt_names=ca_cert_obj.alt_names,
        is_ca=True,
        is_client_cert=False,
    )
    ca_cert_obj._cert = actual_ca_x509_cert
    ca_cert_obj.cert_pem = actual_ca_x509_cert.public_bytes(serialization.Encoding.PEM).decode("utf-8")
    return ca_cert_obj


def x_create_ca_certificate__mutmut_35(
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
        is_ca=True,
        is_client_cert=False,
    )
    ca_cert_obj._cert = actual_ca_x509_cert
    ca_cert_obj.cert_pem = actual_ca_x509_cert.public_bytes(serialization.Encoding.PEM).decode("utf-8")
    return ca_cert_obj


def x_create_ca_certificate__mutmut_36(
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
        is_client_cert=False,
    )
    ca_cert_obj._cert = actual_ca_x509_cert
    ca_cert_obj.cert_pem = actual_ca_x509_cert.public_bytes(serialization.Encoding.PEM).decode("utf-8")
    return ca_cert_obj


def x_create_ca_certificate__mutmut_37(
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
    )
    ca_cert_obj._cert = actual_ca_x509_cert
    ca_cert_obj.cert_pem = actual_ca_x509_cert.public_bytes(serialization.Encoding.PEM).decode("utf-8")
    return ca_cert_obj


def x_create_ca_certificate__mutmut_38(
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
        is_ca=False,
        is_client_cert=False,
    )
    ca_cert_obj._cert = actual_ca_x509_cert
    ca_cert_obj.cert_pem = actual_ca_x509_cert.public_bytes(serialization.Encoding.PEM).decode("utf-8")
    return ca_cert_obj


def x_create_ca_certificate__mutmut_39(
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
        is_client_cert=True,
    )
    ca_cert_obj._cert = actual_ca_x509_cert
    ca_cert_obj.cert_pem = actual_ca_x509_cert.public_bytes(serialization.Encoding.PEM).decode("utf-8")
    return ca_cert_obj


def x_create_ca_certificate__mutmut_40(
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
    ca_cert_obj._cert = None
    ca_cert_obj.cert_pem = actual_ca_x509_cert.public_bytes(serialization.Encoding.PEM).decode("utf-8")
    return ca_cert_obj


def x_create_ca_certificate__mutmut_41(
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
    ca_cert_obj.cert_pem = None
    return ca_cert_obj


def x_create_ca_certificate__mutmut_42(
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
    ca_cert_obj.cert_pem = actual_ca_x509_cert.public_bytes(serialization.Encoding.PEM).decode(None)
    return ca_cert_obj


def x_create_ca_certificate__mutmut_43(
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
    ca_cert_obj.cert_pem = actual_ca_x509_cert.public_bytes(None).decode("utf-8")
    return ca_cert_obj


def x_create_ca_certificate__mutmut_44(
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
    ca_cert_obj.cert_pem = actual_ca_x509_cert.public_bytes(serialization.Encoding.PEM).decode("XXutf-8XX")
    return ca_cert_obj


def x_create_ca_certificate__mutmut_45(
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
    ca_cert_obj.cert_pem = actual_ca_x509_cert.public_bytes(serialization.Encoding.PEM).decode("UTF-8")
    return ca_cert_obj


x_create_ca_certificate__mutmut_mutants: ClassVar[MutantDict] = {
    "x_create_ca_certificate__mutmut_1": x_create_ca_certificate__mutmut_1,
    "x_create_ca_certificate__mutmut_2": x_create_ca_certificate__mutmut_2,
    "x_create_ca_certificate__mutmut_3": x_create_ca_certificate__mutmut_3,
    "x_create_ca_certificate__mutmut_4": x_create_ca_certificate__mutmut_4,
    "x_create_ca_certificate__mutmut_5": x_create_ca_certificate__mutmut_5,
    "x_create_ca_certificate__mutmut_6": x_create_ca_certificate__mutmut_6,
    "x_create_ca_certificate__mutmut_7": x_create_ca_certificate__mutmut_7,
    "x_create_ca_certificate__mutmut_8": x_create_ca_certificate__mutmut_8,
    "x_create_ca_certificate__mutmut_9": x_create_ca_certificate__mutmut_9,
    "x_create_ca_certificate__mutmut_10": x_create_ca_certificate__mutmut_10,
    "x_create_ca_certificate__mutmut_11": x_create_ca_certificate__mutmut_11,
    "x_create_ca_certificate__mutmut_12": x_create_ca_certificate__mutmut_12,
    "x_create_ca_certificate__mutmut_13": x_create_ca_certificate__mutmut_13,
    "x_create_ca_certificate__mutmut_14": x_create_ca_certificate__mutmut_14,
    "x_create_ca_certificate__mutmut_15": x_create_ca_certificate__mutmut_15,
    "x_create_ca_certificate__mutmut_16": x_create_ca_certificate__mutmut_16,
    "x_create_ca_certificate__mutmut_17": x_create_ca_certificate__mutmut_17,
    "x_create_ca_certificate__mutmut_18": x_create_ca_certificate__mutmut_18,
    "x_create_ca_certificate__mutmut_19": x_create_ca_certificate__mutmut_19,
    "x_create_ca_certificate__mutmut_20": x_create_ca_certificate__mutmut_20,
    "x_create_ca_certificate__mutmut_21": x_create_ca_certificate__mutmut_21,
    "x_create_ca_certificate__mutmut_22": x_create_ca_certificate__mutmut_22,
    "x_create_ca_certificate__mutmut_23": x_create_ca_certificate__mutmut_23,
    "x_create_ca_certificate__mutmut_24": x_create_ca_certificate__mutmut_24,
    "x_create_ca_certificate__mutmut_25": x_create_ca_certificate__mutmut_25,
    "x_create_ca_certificate__mutmut_26": x_create_ca_certificate__mutmut_26,
    "x_create_ca_certificate__mutmut_27": x_create_ca_certificate__mutmut_27,
    "x_create_ca_certificate__mutmut_28": x_create_ca_certificate__mutmut_28,
    "x_create_ca_certificate__mutmut_29": x_create_ca_certificate__mutmut_29,
    "x_create_ca_certificate__mutmut_30": x_create_ca_certificate__mutmut_30,
    "x_create_ca_certificate__mutmut_31": x_create_ca_certificate__mutmut_31,
    "x_create_ca_certificate__mutmut_32": x_create_ca_certificate__mutmut_32,
    "x_create_ca_certificate__mutmut_33": x_create_ca_certificate__mutmut_33,
    "x_create_ca_certificate__mutmut_34": x_create_ca_certificate__mutmut_34,
    "x_create_ca_certificate__mutmut_35": x_create_ca_certificate__mutmut_35,
    "x_create_ca_certificate__mutmut_36": x_create_ca_certificate__mutmut_36,
    "x_create_ca_certificate__mutmut_37": x_create_ca_certificate__mutmut_37,
    "x_create_ca_certificate__mutmut_38": x_create_ca_certificate__mutmut_38,
    "x_create_ca_certificate__mutmut_39": x_create_ca_certificate__mutmut_39,
    "x_create_ca_certificate__mutmut_40": x_create_ca_certificate__mutmut_40,
    "x_create_ca_certificate__mutmut_41": x_create_ca_certificate__mutmut_41,
    "x_create_ca_certificate__mutmut_42": x_create_ca_certificate__mutmut_42,
    "x_create_ca_certificate__mutmut_43": x_create_ca_certificate__mutmut_43,
    "x_create_ca_certificate__mutmut_44": x_create_ca_certificate__mutmut_44,
    "x_create_ca_certificate__mutmut_45": x_create_ca_certificate__mutmut_45,
}


def create_ca_certificate(*args, **kwargs):
    result = _mutmut_trampoline(
        x_create_ca_certificate__mutmut_orig, x_create_ca_certificate__mutmut_mutants, args, kwargs
    )
    return result


create_ca_certificate.__signature__ = _mutmut_signature(x_create_ca_certificate__mutmut_orig)
x_create_ca_certificate__mutmut_orig.__name__ = "x_create_ca_certificate"


def x_create_signed_certificate__mutmut_orig(
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
        f"📜🔑✅ Successfully created and signed certificate for "
        f"CN={common_name} by CA='{ca_certificate.subject}'",
    )
    return new_cert_obj


def x_create_signed_certificate__mutmut_1(
    ca_certificate: Certificate,
    common_name: str,
    organization_name: str,
    validity_days: int,
    alt_names: list[str] | None = None,
    key_type: str = DEFAULT_CERTIFICATE_KEY_TYPE,
    key_size: int = DEFAULT_RSA_KEY_SIZE,
    ecdsa_curve: str = DEFAULT_CERTIFICATE_CURVE,
    is_client_cert: bool = True,
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
        f"📜🔑✅ Successfully created and signed certificate for "
        f"CN={common_name} by CA='{ca_certificate.subject}'",
    )
    return new_cert_obj


def x_create_signed_certificate__mutmut_2(
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
        None,
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
        f"📜🔑✅ Successfully created and signed certificate for "
        f"CN={common_name} by CA='{ca_certificate.subject}'",
    )
    return new_cert_obj


def x_create_signed_certificate__mutmut_3(
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
    if ca_certificate._private_key:
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
        f"📜🔑✅ Successfully created and signed certificate for "
        f"CN={common_name} by CA='{ca_certificate.subject}'",
    )
    return new_cert_obj


def x_create_signed_certificate__mutmut_4(
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
            message=None,
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
        f"📜🔑✅ Successfully created and signed certificate for "
        f"CN={common_name} by CA='{ca_certificate.subject}'",
    )
    return new_cert_obj


def x_create_signed_certificate__mutmut_5(
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
            hint=None,
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
        f"📜🔑✅ Successfully created and signed certificate for "
        f"CN={common_name} by CA='{ca_certificate.subject}'",
    )
    return new_cert_obj


def x_create_signed_certificate__mutmut_6(
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
        f"📜🔑✅ Successfully created and signed certificate for "
        f"CN={common_name} by CA='{ca_certificate.subject}'",
    )
    return new_cert_obj


def x_create_signed_certificate__mutmut_7(
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
        f"📜🔑✅ Successfully created and signed certificate for "
        f"CN={common_name} by CA='{ca_certificate.subject}'",
    )
    return new_cert_obj


def x_create_signed_certificate__mutmut_8(
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
            message="XXCA certificate's private key is not available for signing.XX",
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
        f"📜🔑✅ Successfully created and signed certificate for "
        f"CN={common_name} by CA='{ca_certificate.subject}'",
    )
    return new_cert_obj


def x_create_signed_certificate__mutmut_9(
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
            message="ca certificate's private key is not available for signing.",
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
        f"📜🔑✅ Successfully created and signed certificate for "
        f"CN={common_name} by CA='{ca_certificate.subject}'",
    )
    return new_cert_obj


def x_create_signed_certificate__mutmut_10(
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
            message="CA CERTIFICATE'S PRIVATE KEY IS NOT AVAILABLE FOR SIGNING.",
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
        f"📜🔑✅ Successfully created and signed certificate for "
        f"CN={common_name} by CA='{ca_certificate.subject}'",
    )
    return new_cert_obj


def x_create_signed_certificate__mutmut_11(
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
            hint="XXEnsure the CA certificate object was loaded or created with its private key.XX",
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
        f"📜🔑✅ Successfully created and signed certificate for "
        f"CN={common_name} by CA='{ca_certificate.subject}'",
    )
    return new_cert_obj


def x_create_signed_certificate__mutmut_12(
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
            hint="ensure the ca certificate object was loaded or created with its private key.",
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
        f"📜🔑✅ Successfully created and signed certificate for "
        f"CN={common_name} by CA='{ca_certificate.subject}'",
    )
    return new_cert_obj


def x_create_signed_certificate__mutmut_13(
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
            hint="ENSURE THE CA CERTIFICATE OBJECT WAS LOADED OR CREATED WITH ITS PRIVATE KEY.",
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
        f"📜🔑✅ Successfully created and signed certificate for "
        f"CN={common_name} by CA='{ca_certificate.subject}'",
    )
    return new_cert_obj


def x_create_signed_certificate__mutmut_14(
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
    if ca_certificate.is_ca:
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
        f"📜🔑✅ Successfully created and signed certificate for "
        f"CN={common_name} by CA='{ca_certificate.subject}'",
    )
    return new_cert_obj


def x_create_signed_certificate__mutmut_15(
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
            None,
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
        f"📜🔑✅ Successfully created and signed certificate for "
        f"CN={common_name} by CA='{ca_certificate.subject}'",
    )
    return new_cert_obj


def x_create_signed_certificate__mutmut_16(
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
            "XXis not marked as a CA. This might lead to validation issues.XX",
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
        f"📜🔑✅ Successfully created and signed certificate for "
        f"CN={common_name} by CA='{ca_certificate.subject}'",
    )
    return new_cert_obj


def x_create_signed_certificate__mutmut_17(
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
            "is not marked as a ca. this might lead to validation issues.",
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
        f"📜🔑✅ Successfully created and signed certificate for "
        f"CN={common_name} by CA='{ca_certificate.subject}'",
    )
    return new_cert_obj


def x_create_signed_certificate__mutmut_18(
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
            "IS NOT MARKED AS A CA. THIS MIGHT LEAD TO VALIDATION ISSUES.",
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
        f"📜🔑✅ Successfully created and signed certificate for "
        f"CN={common_name} by CA='{ca_certificate.subject}'",
    )
    return new_cert_obj


def x_create_signed_certificate__mutmut_19(
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

    new_cert_obj = None

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
        f"📜🔑✅ Successfully created and signed certificate for "
        f"CN={common_name} by CA='{ca_certificate.subject}'",
    )
    return new_cert_obj


def x_create_signed_certificate__mutmut_20(
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
        common_name=None,
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
        f"📜🔑✅ Successfully created and signed certificate for "
        f"CN={common_name} by CA='{ca_certificate.subject}'",
    )
    return new_cert_obj


def x_create_signed_certificate__mutmut_21(
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
        organization_name=None,
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
        f"📜🔑✅ Successfully created and signed certificate for "
        f"CN={common_name} by CA='{ca_certificate.subject}'",
    )
    return new_cert_obj


def x_create_signed_certificate__mutmut_22(
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
        validity_days=None,
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
        f"📜🔑✅ Successfully created and signed certificate for "
        f"CN={common_name} by CA='{ca_certificate.subject}'",
    )
    return new_cert_obj


def x_create_signed_certificate__mutmut_23(
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
        alt_names=None,
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
        f"📜🔑✅ Successfully created and signed certificate for "
        f"CN={common_name} by CA='{ca_certificate.subject}'",
    )
    return new_cert_obj


def x_create_signed_certificate__mutmut_24(
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
        key_type=None,
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
        f"📜🔑✅ Successfully created and signed certificate for "
        f"CN={common_name} by CA='{ca_certificate.subject}'",
    )
    return new_cert_obj


def x_create_signed_certificate__mutmut_25(
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
        key_size=None,
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
        f"📜🔑✅ Successfully created and signed certificate for "
        f"CN={common_name} by CA='{ca_certificate.subject}'",
    )
    return new_cert_obj


def x_create_signed_certificate__mutmut_26(
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
        ecdsa_curve=None,
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
        f"📜🔑✅ Successfully created and signed certificate for "
        f"CN={common_name} by CA='{ca_certificate.subject}'",
    )
    return new_cert_obj


def x_create_signed_certificate__mutmut_27(
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
        is_ca=None,
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
        f"📜🔑✅ Successfully created and signed certificate for "
        f"CN={common_name} by CA='{ca_certificate.subject}'",
    )
    return new_cert_obj


def x_create_signed_certificate__mutmut_28(
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
        is_client_cert=None,
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
        f"📜🔑✅ Successfully created and signed certificate for "
        f"CN={common_name} by CA='{ca_certificate.subject}'",
    )
    return new_cert_obj


def x_create_signed_certificate__mutmut_29(
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
        f"📜🔑✅ Successfully created and signed certificate for "
        f"CN={common_name} by CA='{ca_certificate.subject}'",
    )
    return new_cert_obj


def x_create_signed_certificate__mutmut_30(
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
        f"📜🔑✅ Successfully created and signed certificate for "
        f"CN={common_name} by CA='{ca_certificate.subject}'",
    )
    return new_cert_obj


def x_create_signed_certificate__mutmut_31(
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
        f"📜🔑✅ Successfully created and signed certificate for "
        f"CN={common_name} by CA='{ca_certificate.subject}'",
    )
    return new_cert_obj


def x_create_signed_certificate__mutmut_32(
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
        f"📜🔑✅ Successfully created and signed certificate for "
        f"CN={common_name} by CA='{ca_certificate.subject}'",
    )
    return new_cert_obj


def x_create_signed_certificate__mutmut_33(
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
        f"📜🔑✅ Successfully created and signed certificate for "
        f"CN={common_name} by CA='{ca_certificate.subject}'",
    )
    return new_cert_obj


def x_create_signed_certificate__mutmut_34(
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
        f"📜🔑✅ Successfully created and signed certificate for "
        f"CN={common_name} by CA='{ca_certificate.subject}'",
    )
    return new_cert_obj


def x_create_signed_certificate__mutmut_35(
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
        f"📜🔑✅ Successfully created and signed certificate for "
        f"CN={common_name} by CA='{ca_certificate.subject}'",
    )
    return new_cert_obj


def x_create_signed_certificate__mutmut_36(
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
        f"📜🔑✅ Successfully created and signed certificate for "
        f"CN={common_name} by CA='{ca_certificate.subject}'",
    )
    return new_cert_obj


def x_create_signed_certificate__mutmut_37(
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
        f"📜🔑✅ Successfully created and signed certificate for "
        f"CN={common_name} by CA='{ca_certificate.subject}'",
    )
    return new_cert_obj


def x_create_signed_certificate__mutmut_38(
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
        alt_names=alt_names and [common_name],
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
        f"📜🔑✅ Successfully created and signed certificate for "
        f"CN={common_name} by CA='{ca_certificate.subject}'",
    )
    return new_cert_obj


def x_create_signed_certificate__mutmut_39(
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
        is_ca=True,
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
        f"📜🔑✅ Successfully created and signed certificate for "
        f"CN={common_name} by CA='{ca_certificate.subject}'",
    )
    return new_cert_obj


def x_create_signed_certificate__mutmut_40(
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

    signed_x509_cert = None

    new_cert_obj._cert = signed_x509_cert
    new_cert_obj.cert_pem = signed_x509_cert.public_bytes(serialization.Encoding.PEM).decode("utf-8")

    logger.info(
        f"📜🔑✅ Successfully created and signed certificate for "
        f"CN={common_name} by CA='{ca_certificate.subject}'",
    )
    return new_cert_obj


def x_create_signed_certificate__mutmut_41(
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
        base=None,
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
        f"📜🔑✅ Successfully created and signed certificate for "
        f"CN={common_name} by CA='{ca_certificate.subject}'",
    )
    return new_cert_obj


def x_create_signed_certificate__mutmut_42(
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
        private_key=None,
        alt_names=new_cert_obj.alt_names,
        issuer_name_override=ca_certificate._base.subject,
        signing_key_override=ca_certificate._private_key,
        is_ca=False,
        is_client_cert=is_client_cert,
    )

    new_cert_obj._cert = signed_x509_cert
    new_cert_obj.cert_pem = signed_x509_cert.public_bytes(serialization.Encoding.PEM).decode("utf-8")

    logger.info(
        f"📜🔑✅ Successfully created and signed certificate for "
        f"CN={common_name} by CA='{ca_certificate.subject}'",
    )
    return new_cert_obj


def x_create_signed_certificate__mutmut_43(
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
        alt_names=None,
        issuer_name_override=ca_certificate._base.subject,
        signing_key_override=ca_certificate._private_key,
        is_ca=False,
        is_client_cert=is_client_cert,
    )

    new_cert_obj._cert = signed_x509_cert
    new_cert_obj.cert_pem = signed_x509_cert.public_bytes(serialization.Encoding.PEM).decode("utf-8")

    logger.info(
        f"📜🔑✅ Successfully created and signed certificate for "
        f"CN={common_name} by CA='{ca_certificate.subject}'",
    )
    return new_cert_obj


def x_create_signed_certificate__mutmut_44(
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
        issuer_name_override=None,
        signing_key_override=ca_certificate._private_key,
        is_ca=False,
        is_client_cert=is_client_cert,
    )

    new_cert_obj._cert = signed_x509_cert
    new_cert_obj.cert_pem = signed_x509_cert.public_bytes(serialization.Encoding.PEM).decode("utf-8")

    logger.info(
        f"📜🔑✅ Successfully created and signed certificate for "
        f"CN={common_name} by CA='{ca_certificate.subject}'",
    )
    return new_cert_obj


def x_create_signed_certificate__mutmut_45(
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
        signing_key_override=None,
        is_ca=False,
        is_client_cert=is_client_cert,
    )

    new_cert_obj._cert = signed_x509_cert
    new_cert_obj.cert_pem = signed_x509_cert.public_bytes(serialization.Encoding.PEM).decode("utf-8")

    logger.info(
        f"📜🔑✅ Successfully created and signed certificate for "
        f"CN={common_name} by CA='{ca_certificate.subject}'",
    )
    return new_cert_obj


def x_create_signed_certificate__mutmut_46(
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
        is_ca=None,
        is_client_cert=is_client_cert,
    )

    new_cert_obj._cert = signed_x509_cert
    new_cert_obj.cert_pem = signed_x509_cert.public_bytes(serialization.Encoding.PEM).decode("utf-8")

    logger.info(
        f"📜🔑✅ Successfully created and signed certificate for "
        f"CN={common_name} by CA='{ca_certificate.subject}'",
    )
    return new_cert_obj


def x_create_signed_certificate__mutmut_47(
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
        is_client_cert=None,
    )

    new_cert_obj._cert = signed_x509_cert
    new_cert_obj.cert_pem = signed_x509_cert.public_bytes(serialization.Encoding.PEM).decode("utf-8")

    logger.info(
        f"📜🔑✅ Successfully created and signed certificate for "
        f"CN={common_name} by CA='{ca_certificate.subject}'",
    )
    return new_cert_obj


def x_create_signed_certificate__mutmut_48(
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
        f"📜🔑✅ Successfully created and signed certificate for "
        f"CN={common_name} by CA='{ca_certificate.subject}'",
    )
    return new_cert_obj


def x_create_signed_certificate__mutmut_49(
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
        alt_names=new_cert_obj.alt_names,
        issuer_name_override=ca_certificate._base.subject,
        signing_key_override=ca_certificate._private_key,
        is_ca=False,
        is_client_cert=is_client_cert,
    )

    new_cert_obj._cert = signed_x509_cert
    new_cert_obj.cert_pem = signed_x509_cert.public_bytes(serialization.Encoding.PEM).decode("utf-8")

    logger.info(
        f"📜🔑✅ Successfully created and signed certificate for "
        f"CN={common_name} by CA='{ca_certificate.subject}'",
    )
    return new_cert_obj


def x_create_signed_certificate__mutmut_50(
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
        issuer_name_override=ca_certificate._base.subject,
        signing_key_override=ca_certificate._private_key,
        is_ca=False,
        is_client_cert=is_client_cert,
    )

    new_cert_obj._cert = signed_x509_cert
    new_cert_obj.cert_pem = signed_x509_cert.public_bytes(serialization.Encoding.PEM).decode("utf-8")

    logger.info(
        f"📜🔑✅ Successfully created and signed certificate for "
        f"CN={common_name} by CA='{ca_certificate.subject}'",
    )
    return new_cert_obj


def x_create_signed_certificate__mutmut_51(
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
        signing_key_override=ca_certificate._private_key,
        is_ca=False,
        is_client_cert=is_client_cert,
    )

    new_cert_obj._cert = signed_x509_cert
    new_cert_obj.cert_pem = signed_x509_cert.public_bytes(serialization.Encoding.PEM).decode("utf-8")

    logger.info(
        f"📜🔑✅ Successfully created and signed certificate for "
        f"CN={common_name} by CA='{ca_certificate.subject}'",
    )
    return new_cert_obj


def x_create_signed_certificate__mutmut_52(
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
        is_ca=False,
        is_client_cert=is_client_cert,
    )

    new_cert_obj._cert = signed_x509_cert
    new_cert_obj.cert_pem = signed_x509_cert.public_bytes(serialization.Encoding.PEM).decode("utf-8")

    logger.info(
        f"📜🔑✅ Successfully created and signed certificate for "
        f"CN={common_name} by CA='{ca_certificate.subject}'",
    )
    return new_cert_obj


def x_create_signed_certificate__mutmut_53(
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
        is_client_cert=is_client_cert,
    )

    new_cert_obj._cert = signed_x509_cert
    new_cert_obj.cert_pem = signed_x509_cert.public_bytes(serialization.Encoding.PEM).decode("utf-8")

    logger.info(
        f"📜🔑✅ Successfully created and signed certificate for "
        f"CN={common_name} by CA='{ca_certificate.subject}'",
    )
    return new_cert_obj


def x_create_signed_certificate__mutmut_54(
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
    )

    new_cert_obj._cert = signed_x509_cert
    new_cert_obj.cert_pem = signed_x509_cert.public_bytes(serialization.Encoding.PEM).decode("utf-8")

    logger.info(
        f"📜🔑✅ Successfully created and signed certificate for "
        f"CN={common_name} by CA='{ca_certificate.subject}'",
    )
    return new_cert_obj


def x_create_signed_certificate__mutmut_55(
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
        is_ca=True,
        is_client_cert=is_client_cert,
    )

    new_cert_obj._cert = signed_x509_cert
    new_cert_obj.cert_pem = signed_x509_cert.public_bytes(serialization.Encoding.PEM).decode("utf-8")

    logger.info(
        f"📜🔑✅ Successfully created and signed certificate for "
        f"CN={common_name} by CA='{ca_certificate.subject}'",
    )
    return new_cert_obj


def x_create_signed_certificate__mutmut_56(
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

    new_cert_obj._cert = None
    new_cert_obj.cert_pem = signed_x509_cert.public_bytes(serialization.Encoding.PEM).decode("utf-8")

    logger.info(
        f"📜🔑✅ Successfully created and signed certificate for "
        f"CN={common_name} by CA='{ca_certificate.subject}'",
    )
    return new_cert_obj


def x_create_signed_certificate__mutmut_57(
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
    new_cert_obj.cert_pem = None

    logger.info(
        f"📜🔑✅ Successfully created and signed certificate for "
        f"CN={common_name} by CA='{ca_certificate.subject}'",
    )
    return new_cert_obj


def x_create_signed_certificate__mutmut_58(
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
    new_cert_obj.cert_pem = signed_x509_cert.public_bytes(serialization.Encoding.PEM).decode(None)

    logger.info(
        f"📜🔑✅ Successfully created and signed certificate for "
        f"CN={common_name} by CA='{ca_certificate.subject}'",
    )
    return new_cert_obj


def x_create_signed_certificate__mutmut_59(
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
    new_cert_obj.cert_pem = signed_x509_cert.public_bytes(None).decode("utf-8")

    logger.info(
        f"📜🔑✅ Successfully created and signed certificate for "
        f"CN={common_name} by CA='{ca_certificate.subject}'",
    )
    return new_cert_obj


def x_create_signed_certificate__mutmut_60(
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
    new_cert_obj.cert_pem = signed_x509_cert.public_bytes(serialization.Encoding.PEM).decode("XXutf-8XX")

    logger.info(
        f"📜🔑✅ Successfully created and signed certificate for "
        f"CN={common_name} by CA='{ca_certificate.subject}'",
    )
    return new_cert_obj


def x_create_signed_certificate__mutmut_61(
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
    new_cert_obj.cert_pem = signed_x509_cert.public_bytes(serialization.Encoding.PEM).decode("UTF-8")

    logger.info(
        f"📜🔑✅ Successfully created and signed certificate for "
        f"CN={common_name} by CA='{ca_certificate.subject}'",
    )
    return new_cert_obj


def x_create_signed_certificate__mutmut_62(
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
        None,
    )
    return new_cert_obj


x_create_signed_certificate__mutmut_mutants: ClassVar[MutantDict] = {
    "x_create_signed_certificate__mutmut_1": x_create_signed_certificate__mutmut_1,
    "x_create_signed_certificate__mutmut_2": x_create_signed_certificate__mutmut_2,
    "x_create_signed_certificate__mutmut_3": x_create_signed_certificate__mutmut_3,
    "x_create_signed_certificate__mutmut_4": x_create_signed_certificate__mutmut_4,
    "x_create_signed_certificate__mutmut_5": x_create_signed_certificate__mutmut_5,
    "x_create_signed_certificate__mutmut_6": x_create_signed_certificate__mutmut_6,
    "x_create_signed_certificate__mutmut_7": x_create_signed_certificate__mutmut_7,
    "x_create_signed_certificate__mutmut_8": x_create_signed_certificate__mutmut_8,
    "x_create_signed_certificate__mutmut_9": x_create_signed_certificate__mutmut_9,
    "x_create_signed_certificate__mutmut_10": x_create_signed_certificate__mutmut_10,
    "x_create_signed_certificate__mutmut_11": x_create_signed_certificate__mutmut_11,
    "x_create_signed_certificate__mutmut_12": x_create_signed_certificate__mutmut_12,
    "x_create_signed_certificate__mutmut_13": x_create_signed_certificate__mutmut_13,
    "x_create_signed_certificate__mutmut_14": x_create_signed_certificate__mutmut_14,
    "x_create_signed_certificate__mutmut_15": x_create_signed_certificate__mutmut_15,
    "x_create_signed_certificate__mutmut_16": x_create_signed_certificate__mutmut_16,
    "x_create_signed_certificate__mutmut_17": x_create_signed_certificate__mutmut_17,
    "x_create_signed_certificate__mutmut_18": x_create_signed_certificate__mutmut_18,
    "x_create_signed_certificate__mutmut_19": x_create_signed_certificate__mutmut_19,
    "x_create_signed_certificate__mutmut_20": x_create_signed_certificate__mutmut_20,
    "x_create_signed_certificate__mutmut_21": x_create_signed_certificate__mutmut_21,
    "x_create_signed_certificate__mutmut_22": x_create_signed_certificate__mutmut_22,
    "x_create_signed_certificate__mutmut_23": x_create_signed_certificate__mutmut_23,
    "x_create_signed_certificate__mutmut_24": x_create_signed_certificate__mutmut_24,
    "x_create_signed_certificate__mutmut_25": x_create_signed_certificate__mutmut_25,
    "x_create_signed_certificate__mutmut_26": x_create_signed_certificate__mutmut_26,
    "x_create_signed_certificate__mutmut_27": x_create_signed_certificate__mutmut_27,
    "x_create_signed_certificate__mutmut_28": x_create_signed_certificate__mutmut_28,
    "x_create_signed_certificate__mutmut_29": x_create_signed_certificate__mutmut_29,
    "x_create_signed_certificate__mutmut_30": x_create_signed_certificate__mutmut_30,
    "x_create_signed_certificate__mutmut_31": x_create_signed_certificate__mutmut_31,
    "x_create_signed_certificate__mutmut_32": x_create_signed_certificate__mutmut_32,
    "x_create_signed_certificate__mutmut_33": x_create_signed_certificate__mutmut_33,
    "x_create_signed_certificate__mutmut_34": x_create_signed_certificate__mutmut_34,
    "x_create_signed_certificate__mutmut_35": x_create_signed_certificate__mutmut_35,
    "x_create_signed_certificate__mutmut_36": x_create_signed_certificate__mutmut_36,
    "x_create_signed_certificate__mutmut_37": x_create_signed_certificate__mutmut_37,
    "x_create_signed_certificate__mutmut_38": x_create_signed_certificate__mutmut_38,
    "x_create_signed_certificate__mutmut_39": x_create_signed_certificate__mutmut_39,
    "x_create_signed_certificate__mutmut_40": x_create_signed_certificate__mutmut_40,
    "x_create_signed_certificate__mutmut_41": x_create_signed_certificate__mutmut_41,
    "x_create_signed_certificate__mutmut_42": x_create_signed_certificate__mutmut_42,
    "x_create_signed_certificate__mutmut_43": x_create_signed_certificate__mutmut_43,
    "x_create_signed_certificate__mutmut_44": x_create_signed_certificate__mutmut_44,
    "x_create_signed_certificate__mutmut_45": x_create_signed_certificate__mutmut_45,
    "x_create_signed_certificate__mutmut_46": x_create_signed_certificate__mutmut_46,
    "x_create_signed_certificate__mutmut_47": x_create_signed_certificate__mutmut_47,
    "x_create_signed_certificate__mutmut_48": x_create_signed_certificate__mutmut_48,
    "x_create_signed_certificate__mutmut_49": x_create_signed_certificate__mutmut_49,
    "x_create_signed_certificate__mutmut_50": x_create_signed_certificate__mutmut_50,
    "x_create_signed_certificate__mutmut_51": x_create_signed_certificate__mutmut_51,
    "x_create_signed_certificate__mutmut_52": x_create_signed_certificate__mutmut_52,
    "x_create_signed_certificate__mutmut_53": x_create_signed_certificate__mutmut_53,
    "x_create_signed_certificate__mutmut_54": x_create_signed_certificate__mutmut_54,
    "x_create_signed_certificate__mutmut_55": x_create_signed_certificate__mutmut_55,
    "x_create_signed_certificate__mutmut_56": x_create_signed_certificate__mutmut_56,
    "x_create_signed_certificate__mutmut_57": x_create_signed_certificate__mutmut_57,
    "x_create_signed_certificate__mutmut_58": x_create_signed_certificate__mutmut_58,
    "x_create_signed_certificate__mutmut_59": x_create_signed_certificate__mutmut_59,
    "x_create_signed_certificate__mutmut_60": x_create_signed_certificate__mutmut_60,
    "x_create_signed_certificate__mutmut_61": x_create_signed_certificate__mutmut_61,
    "x_create_signed_certificate__mutmut_62": x_create_signed_certificate__mutmut_62,
}


def create_signed_certificate(*args, **kwargs):
    result = _mutmut_trampoline(
        x_create_signed_certificate__mutmut_orig, x_create_signed_certificate__mutmut_mutants, args, kwargs
    )
    return result


create_signed_certificate.__signature__ = _mutmut_signature(x_create_signed_certificate__mutmut_orig)
x_create_signed_certificate__mutmut_orig.__name__ = "x_create_signed_certificate"


def x_create_self_signed_server_cert__mutmut_orig(
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

    logger.info(f"📜🔑✅ Successfully created self-signed SERVER certificate for CN={common_name}")
    return cert_obj


def x_create_self_signed_server_cert__mutmut_1(
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
        None,
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

    logger.info(f"📜🔑✅ Successfully created self-signed SERVER certificate for CN={common_name}")
    return cert_obj


def x_create_self_signed_server_cert__mutmut_2(
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

    cert_obj = None

    logger.info(f"📜🔑✅ Successfully created self-signed SERVER certificate for CN={common_name}")
    return cert_obj


def x_create_self_signed_server_cert__mutmut_3(
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
        common_name=None,
        organization_name=organization_name,
        validity_days=validity_days,
        alt_names=alt_names or [common_name],
        key_type=key_type,
        key_size=key_size,
        ecdsa_curve=ecdsa_curve,
        is_ca=False,
        is_client_cert=False,
    )

    logger.info(f"📜🔑✅ Successfully created self-signed SERVER certificate for CN={common_name}")
    return cert_obj


def x_create_self_signed_server_cert__mutmut_4(
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
        organization_name=None,
        validity_days=validity_days,
        alt_names=alt_names or [common_name],
        key_type=key_type,
        key_size=key_size,
        ecdsa_curve=ecdsa_curve,
        is_ca=False,
        is_client_cert=False,
    )

    logger.info(f"📜🔑✅ Successfully created self-signed SERVER certificate for CN={common_name}")
    return cert_obj


def x_create_self_signed_server_cert__mutmut_5(
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
        validity_days=None,
        alt_names=alt_names or [common_name],
        key_type=key_type,
        key_size=key_size,
        ecdsa_curve=ecdsa_curve,
        is_ca=False,
        is_client_cert=False,
    )

    logger.info(f"📜🔑✅ Successfully created self-signed SERVER certificate for CN={common_name}")
    return cert_obj


def x_create_self_signed_server_cert__mutmut_6(
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
        alt_names=None,
        key_type=key_type,
        key_size=key_size,
        ecdsa_curve=ecdsa_curve,
        is_ca=False,
        is_client_cert=False,
    )

    logger.info(f"📜🔑✅ Successfully created self-signed SERVER certificate for CN={common_name}")
    return cert_obj


def x_create_self_signed_server_cert__mutmut_7(
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
        key_type=None,
        key_size=key_size,
        ecdsa_curve=ecdsa_curve,
        is_ca=False,
        is_client_cert=False,
    )

    logger.info(f"📜🔑✅ Successfully created self-signed SERVER certificate for CN={common_name}")
    return cert_obj


def x_create_self_signed_server_cert__mutmut_8(
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
        key_size=None,
        ecdsa_curve=ecdsa_curve,
        is_ca=False,
        is_client_cert=False,
    )

    logger.info(f"📜🔑✅ Successfully created self-signed SERVER certificate for CN={common_name}")
    return cert_obj


def x_create_self_signed_server_cert__mutmut_9(
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
        ecdsa_curve=None,
        is_ca=False,
        is_client_cert=False,
    )

    logger.info(f"📜🔑✅ Successfully created self-signed SERVER certificate for CN={common_name}")
    return cert_obj


def x_create_self_signed_server_cert__mutmut_10(
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
        is_ca=None,
        is_client_cert=False,
    )

    logger.info(f"📜🔑✅ Successfully created self-signed SERVER certificate for CN={common_name}")
    return cert_obj


def x_create_self_signed_server_cert__mutmut_11(
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
        is_client_cert=None,
    )

    logger.info(f"📜🔑✅ Successfully created self-signed SERVER certificate for CN={common_name}")
    return cert_obj


def x_create_self_signed_server_cert__mutmut_12(
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
        organization_name=organization_name,
        validity_days=validity_days,
        alt_names=alt_names or [common_name],
        key_type=key_type,
        key_size=key_size,
        ecdsa_curve=ecdsa_curve,
        is_ca=False,
        is_client_cert=False,
    )

    logger.info(f"📜🔑✅ Successfully created self-signed SERVER certificate for CN={common_name}")
    return cert_obj


def x_create_self_signed_server_cert__mutmut_13(
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
        validity_days=validity_days,
        alt_names=alt_names or [common_name],
        key_type=key_type,
        key_size=key_size,
        ecdsa_curve=ecdsa_curve,
        is_ca=False,
        is_client_cert=False,
    )

    logger.info(f"📜🔑✅ Successfully created self-signed SERVER certificate for CN={common_name}")
    return cert_obj


def x_create_self_signed_server_cert__mutmut_14(
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
        alt_names=alt_names or [common_name],
        key_type=key_type,
        key_size=key_size,
        ecdsa_curve=ecdsa_curve,
        is_ca=False,
        is_client_cert=False,
    )

    logger.info(f"📜🔑✅ Successfully created self-signed SERVER certificate for CN={common_name}")
    return cert_obj


def x_create_self_signed_server_cert__mutmut_15(
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
        key_type=key_type,
        key_size=key_size,
        ecdsa_curve=ecdsa_curve,
        is_ca=False,
        is_client_cert=False,
    )

    logger.info(f"📜🔑✅ Successfully created self-signed SERVER certificate for CN={common_name}")
    return cert_obj


def x_create_self_signed_server_cert__mutmut_16(
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
        key_size=key_size,
        ecdsa_curve=ecdsa_curve,
        is_ca=False,
        is_client_cert=False,
    )

    logger.info(f"📜🔑✅ Successfully created self-signed SERVER certificate for CN={common_name}")
    return cert_obj


def x_create_self_signed_server_cert__mutmut_17(
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
        ecdsa_curve=ecdsa_curve,
        is_ca=False,
        is_client_cert=False,
    )

    logger.info(f"📜🔑✅ Successfully created self-signed SERVER certificate for CN={common_name}")
    return cert_obj


def x_create_self_signed_server_cert__mutmut_18(
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
        is_ca=False,
        is_client_cert=False,
    )

    logger.info(f"📜🔑✅ Successfully created self-signed SERVER certificate for CN={common_name}")
    return cert_obj


def x_create_self_signed_server_cert__mutmut_19(
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
        is_client_cert=False,
    )

    logger.info(f"📜🔑✅ Successfully created self-signed SERVER certificate for CN={common_name}")
    return cert_obj


def x_create_self_signed_server_cert__mutmut_20(
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
    )

    logger.info(f"📜🔑✅ Successfully created self-signed SERVER certificate for CN={common_name}")
    return cert_obj


def x_create_self_signed_server_cert__mutmut_21(
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
        alt_names=alt_names and [common_name],
        key_type=key_type,
        key_size=key_size,
        ecdsa_curve=ecdsa_curve,
        is_ca=False,
        is_client_cert=False,
    )

    logger.info(f"📜🔑✅ Successfully created self-signed SERVER certificate for CN={common_name}")
    return cert_obj


def x_create_self_signed_server_cert__mutmut_22(
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
        is_ca=True,
        is_client_cert=False,
    )

    logger.info(f"📜🔑✅ Successfully created self-signed SERVER certificate for CN={common_name}")
    return cert_obj


def x_create_self_signed_server_cert__mutmut_23(
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
        is_client_cert=True,
    )

    logger.info(f"📜🔑✅ Successfully created self-signed SERVER certificate for CN={common_name}")
    return cert_obj


def x_create_self_signed_server_cert__mutmut_24(
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

    logger.info(None)
    return cert_obj


x_create_self_signed_server_cert__mutmut_mutants: ClassVar[MutantDict] = {
    "x_create_self_signed_server_cert__mutmut_1": x_create_self_signed_server_cert__mutmut_1,
    "x_create_self_signed_server_cert__mutmut_2": x_create_self_signed_server_cert__mutmut_2,
    "x_create_self_signed_server_cert__mutmut_3": x_create_self_signed_server_cert__mutmut_3,
    "x_create_self_signed_server_cert__mutmut_4": x_create_self_signed_server_cert__mutmut_4,
    "x_create_self_signed_server_cert__mutmut_5": x_create_self_signed_server_cert__mutmut_5,
    "x_create_self_signed_server_cert__mutmut_6": x_create_self_signed_server_cert__mutmut_6,
    "x_create_self_signed_server_cert__mutmut_7": x_create_self_signed_server_cert__mutmut_7,
    "x_create_self_signed_server_cert__mutmut_8": x_create_self_signed_server_cert__mutmut_8,
    "x_create_self_signed_server_cert__mutmut_9": x_create_self_signed_server_cert__mutmut_9,
    "x_create_self_signed_server_cert__mutmut_10": x_create_self_signed_server_cert__mutmut_10,
    "x_create_self_signed_server_cert__mutmut_11": x_create_self_signed_server_cert__mutmut_11,
    "x_create_self_signed_server_cert__mutmut_12": x_create_self_signed_server_cert__mutmut_12,
    "x_create_self_signed_server_cert__mutmut_13": x_create_self_signed_server_cert__mutmut_13,
    "x_create_self_signed_server_cert__mutmut_14": x_create_self_signed_server_cert__mutmut_14,
    "x_create_self_signed_server_cert__mutmut_15": x_create_self_signed_server_cert__mutmut_15,
    "x_create_self_signed_server_cert__mutmut_16": x_create_self_signed_server_cert__mutmut_16,
    "x_create_self_signed_server_cert__mutmut_17": x_create_self_signed_server_cert__mutmut_17,
    "x_create_self_signed_server_cert__mutmut_18": x_create_self_signed_server_cert__mutmut_18,
    "x_create_self_signed_server_cert__mutmut_19": x_create_self_signed_server_cert__mutmut_19,
    "x_create_self_signed_server_cert__mutmut_20": x_create_self_signed_server_cert__mutmut_20,
    "x_create_self_signed_server_cert__mutmut_21": x_create_self_signed_server_cert__mutmut_21,
    "x_create_self_signed_server_cert__mutmut_22": x_create_self_signed_server_cert__mutmut_22,
    "x_create_self_signed_server_cert__mutmut_23": x_create_self_signed_server_cert__mutmut_23,
    "x_create_self_signed_server_cert__mutmut_24": x_create_self_signed_server_cert__mutmut_24,
}


def create_self_signed_server_cert(*args, **kwargs):
    result = _mutmut_trampoline(
        x_create_self_signed_server_cert__mutmut_orig,
        x_create_self_signed_server_cert__mutmut_mutants,
        args,
        kwargs,
    )
    return result


create_self_signed_server_cert.__signature__ = _mutmut_signature(x_create_self_signed_server_cert__mutmut_orig)
x_create_self_signed_server_cert__mutmut_orig.__name__ = "x_create_self_signed_server_cert"


def x_create_self_signed_client_cert__mutmut_orig(
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

    logger.info(f"📜🔑✅ Successfully created self-signed CLIENT certificate for CN={common_name}")
    return cert_obj


def x_create_self_signed_client_cert__mutmut_1(
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
        None,
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

    logger.info(f"📜🔑✅ Successfully created self-signed CLIENT certificate for CN={common_name}")
    return cert_obj


def x_create_self_signed_client_cert__mutmut_2(
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

    cert_obj = None

    logger.info(f"📜🔑✅ Successfully created self-signed CLIENT certificate for CN={common_name}")
    return cert_obj


def x_create_self_signed_client_cert__mutmut_3(
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
        common_name=None,
        organization_name=organization_name,
        validity_days=validity_days,
        alt_names=alt_names or [common_name],
        key_type=key_type,
        key_size=key_size,
        ecdsa_curve=ecdsa_curve,
        is_ca=False,
        is_client_cert=True,  # This is the key difference from server cert
    )

    logger.info(f"📜🔑✅ Successfully created self-signed CLIENT certificate for CN={common_name}")
    return cert_obj


def x_create_self_signed_client_cert__mutmut_4(
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
        organization_name=None,
        validity_days=validity_days,
        alt_names=alt_names or [common_name],
        key_type=key_type,
        key_size=key_size,
        ecdsa_curve=ecdsa_curve,
        is_ca=False,
        is_client_cert=True,  # This is the key difference from server cert
    )

    logger.info(f"📜🔑✅ Successfully created self-signed CLIENT certificate for CN={common_name}")
    return cert_obj


def x_create_self_signed_client_cert__mutmut_5(
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
        validity_days=None,
        alt_names=alt_names or [common_name],
        key_type=key_type,
        key_size=key_size,
        ecdsa_curve=ecdsa_curve,
        is_ca=False,
        is_client_cert=True,  # This is the key difference from server cert
    )

    logger.info(f"📜🔑✅ Successfully created self-signed CLIENT certificate for CN={common_name}")
    return cert_obj


def x_create_self_signed_client_cert__mutmut_6(
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
        alt_names=None,
        key_type=key_type,
        key_size=key_size,
        ecdsa_curve=ecdsa_curve,
        is_ca=False,
        is_client_cert=True,  # This is the key difference from server cert
    )

    logger.info(f"📜🔑✅ Successfully created self-signed CLIENT certificate for CN={common_name}")
    return cert_obj


def x_create_self_signed_client_cert__mutmut_7(
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
        key_type=None,
        key_size=key_size,
        ecdsa_curve=ecdsa_curve,
        is_ca=False,
        is_client_cert=True,  # This is the key difference from server cert
    )

    logger.info(f"📜🔑✅ Successfully created self-signed CLIENT certificate for CN={common_name}")
    return cert_obj


def x_create_self_signed_client_cert__mutmut_8(
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
        key_size=None,
        ecdsa_curve=ecdsa_curve,
        is_ca=False,
        is_client_cert=True,  # This is the key difference from server cert
    )

    logger.info(f"📜🔑✅ Successfully created self-signed CLIENT certificate for CN={common_name}")
    return cert_obj


def x_create_self_signed_client_cert__mutmut_9(
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
        ecdsa_curve=None,
        is_ca=False,
        is_client_cert=True,  # This is the key difference from server cert
    )

    logger.info(f"📜🔑✅ Successfully created self-signed CLIENT certificate for CN={common_name}")
    return cert_obj


def x_create_self_signed_client_cert__mutmut_10(
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
        is_ca=None,
        is_client_cert=True,  # This is the key difference from server cert
    )

    logger.info(f"📜🔑✅ Successfully created self-signed CLIENT certificate for CN={common_name}")
    return cert_obj


def x_create_self_signed_client_cert__mutmut_11(
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
        is_client_cert=None,  # This is the key difference from server cert
    )

    logger.info(f"📜🔑✅ Successfully created self-signed CLIENT certificate for CN={common_name}")
    return cert_obj


def x_create_self_signed_client_cert__mutmut_12(
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
        organization_name=organization_name,
        validity_days=validity_days,
        alt_names=alt_names or [common_name],
        key_type=key_type,
        key_size=key_size,
        ecdsa_curve=ecdsa_curve,
        is_ca=False,
        is_client_cert=True,  # This is the key difference from server cert
    )

    logger.info(f"📜🔑✅ Successfully created self-signed CLIENT certificate for CN={common_name}")
    return cert_obj


def x_create_self_signed_client_cert__mutmut_13(
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
        validity_days=validity_days,
        alt_names=alt_names or [common_name],
        key_type=key_type,
        key_size=key_size,
        ecdsa_curve=ecdsa_curve,
        is_ca=False,
        is_client_cert=True,  # This is the key difference from server cert
    )

    logger.info(f"📜🔑✅ Successfully created self-signed CLIENT certificate for CN={common_name}")
    return cert_obj


def x_create_self_signed_client_cert__mutmut_14(
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
        alt_names=alt_names or [common_name],
        key_type=key_type,
        key_size=key_size,
        ecdsa_curve=ecdsa_curve,
        is_ca=False,
        is_client_cert=True,  # This is the key difference from server cert
    )

    logger.info(f"📜🔑✅ Successfully created self-signed CLIENT certificate for CN={common_name}")
    return cert_obj


def x_create_self_signed_client_cert__mutmut_15(
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
        key_type=key_type,
        key_size=key_size,
        ecdsa_curve=ecdsa_curve,
        is_ca=False,
        is_client_cert=True,  # This is the key difference from server cert
    )

    logger.info(f"📜🔑✅ Successfully created self-signed CLIENT certificate for CN={common_name}")
    return cert_obj


def x_create_self_signed_client_cert__mutmut_16(
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
        key_size=key_size,
        ecdsa_curve=ecdsa_curve,
        is_ca=False,
        is_client_cert=True,  # This is the key difference from server cert
    )

    logger.info(f"📜🔑✅ Successfully created self-signed CLIENT certificate for CN={common_name}")
    return cert_obj


def x_create_self_signed_client_cert__mutmut_17(
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
        ecdsa_curve=ecdsa_curve,
        is_ca=False,
        is_client_cert=True,  # This is the key difference from server cert
    )

    logger.info(f"📜🔑✅ Successfully created self-signed CLIENT certificate for CN={common_name}")
    return cert_obj


def x_create_self_signed_client_cert__mutmut_18(
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
        is_ca=False,
        is_client_cert=True,  # This is the key difference from server cert
    )

    logger.info(f"📜🔑✅ Successfully created self-signed CLIENT certificate for CN={common_name}")
    return cert_obj


def x_create_self_signed_client_cert__mutmut_19(
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
        is_client_cert=True,  # This is the key difference from server cert
    )

    logger.info(f"📜🔑✅ Successfully created self-signed CLIENT certificate for CN={common_name}")
    return cert_obj


def x_create_self_signed_client_cert__mutmut_20(
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
    )

    logger.info(f"📜🔑✅ Successfully created self-signed CLIENT certificate for CN={common_name}")
    return cert_obj


def x_create_self_signed_client_cert__mutmut_21(
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
        alt_names=alt_names and [common_name],
        key_type=key_type,
        key_size=key_size,
        ecdsa_curve=ecdsa_curve,
        is_ca=False,
        is_client_cert=True,  # This is the key difference from server cert
    )

    logger.info(f"📜🔑✅ Successfully created self-signed CLIENT certificate for CN={common_name}")
    return cert_obj


def x_create_self_signed_client_cert__mutmut_22(
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
        is_ca=True,
        is_client_cert=True,  # This is the key difference from server cert
    )

    logger.info(f"📜🔑✅ Successfully created self-signed CLIENT certificate for CN={common_name}")
    return cert_obj


def x_create_self_signed_client_cert__mutmut_23(
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
        is_client_cert=False,  # This is the key difference from server cert
    )

    logger.info(f"📜🔑✅ Successfully created self-signed CLIENT certificate for CN={common_name}")
    return cert_obj


def x_create_self_signed_client_cert__mutmut_24(
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

    logger.info(None)
    return cert_obj


x_create_self_signed_client_cert__mutmut_mutants: ClassVar[MutantDict] = {
    "x_create_self_signed_client_cert__mutmut_1": x_create_self_signed_client_cert__mutmut_1,
    "x_create_self_signed_client_cert__mutmut_2": x_create_self_signed_client_cert__mutmut_2,
    "x_create_self_signed_client_cert__mutmut_3": x_create_self_signed_client_cert__mutmut_3,
    "x_create_self_signed_client_cert__mutmut_4": x_create_self_signed_client_cert__mutmut_4,
    "x_create_self_signed_client_cert__mutmut_5": x_create_self_signed_client_cert__mutmut_5,
    "x_create_self_signed_client_cert__mutmut_6": x_create_self_signed_client_cert__mutmut_6,
    "x_create_self_signed_client_cert__mutmut_7": x_create_self_signed_client_cert__mutmut_7,
    "x_create_self_signed_client_cert__mutmut_8": x_create_self_signed_client_cert__mutmut_8,
    "x_create_self_signed_client_cert__mutmut_9": x_create_self_signed_client_cert__mutmut_9,
    "x_create_self_signed_client_cert__mutmut_10": x_create_self_signed_client_cert__mutmut_10,
    "x_create_self_signed_client_cert__mutmut_11": x_create_self_signed_client_cert__mutmut_11,
    "x_create_self_signed_client_cert__mutmut_12": x_create_self_signed_client_cert__mutmut_12,
    "x_create_self_signed_client_cert__mutmut_13": x_create_self_signed_client_cert__mutmut_13,
    "x_create_self_signed_client_cert__mutmut_14": x_create_self_signed_client_cert__mutmut_14,
    "x_create_self_signed_client_cert__mutmut_15": x_create_self_signed_client_cert__mutmut_15,
    "x_create_self_signed_client_cert__mutmut_16": x_create_self_signed_client_cert__mutmut_16,
    "x_create_self_signed_client_cert__mutmut_17": x_create_self_signed_client_cert__mutmut_17,
    "x_create_self_signed_client_cert__mutmut_18": x_create_self_signed_client_cert__mutmut_18,
    "x_create_self_signed_client_cert__mutmut_19": x_create_self_signed_client_cert__mutmut_19,
    "x_create_self_signed_client_cert__mutmut_20": x_create_self_signed_client_cert__mutmut_20,
    "x_create_self_signed_client_cert__mutmut_21": x_create_self_signed_client_cert__mutmut_21,
    "x_create_self_signed_client_cert__mutmut_22": x_create_self_signed_client_cert__mutmut_22,
    "x_create_self_signed_client_cert__mutmut_23": x_create_self_signed_client_cert__mutmut_23,
    "x_create_self_signed_client_cert__mutmut_24": x_create_self_signed_client_cert__mutmut_24,
}


def create_self_signed_client_cert(*args, **kwargs):
    result = _mutmut_trampoline(
        x_create_self_signed_client_cert__mutmut_orig,
        x_create_self_signed_client_cert__mutmut_mutants,
        args,
        kwargs,
    )
    return result


create_self_signed_client_cert.__signature__ = _mutmut_signature(x_create_self_signed_client_cert__mutmut_orig)
x_create_self_signed_client_cert__mutmut_orig.__name__ = "x_create_self_signed_client_cert"


# Convenience functions for common use cases
def x_create_self_signed__mutmut_orig(
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


# Convenience functions for common use cases
def x_create_self_signed__mutmut_1(
    common_name: str = "XXlocalhostXX",
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


# Convenience functions for common use cases
def x_create_self_signed__mutmut_2(
    common_name: str = "LOCALHOST",
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


# Convenience functions for common use cases
def x_create_self_signed__mutmut_3(
    common_name: str = "localhost",
    alt_names: list[str] | None = None,
    organization: str = "XXDefault OrganizationXX",
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


# Convenience functions for common use cases
def x_create_self_signed__mutmut_4(
    common_name: str = "localhost",
    alt_names: list[str] | None = None,
    organization: str = "default organization",
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


# Convenience functions for common use cases
def x_create_self_signed__mutmut_5(
    common_name: str = "localhost",
    alt_names: list[str] | None = None,
    organization: str = "DEFAULT ORGANIZATION",
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


# Convenience functions for common use cases
def x_create_self_signed__mutmut_6(
    common_name: str = "localhost",
    alt_names: list[str] | None = None,
    organization: str = "Default Organization",
    validity_days: int = DEFAULT_CERTIFICATE_VALIDITY_DAYS,
    key_type: str = DEFAULT_CERTIFICATE_KEY_TYPE,
) -> Certificate:
    """Create a self-signed certificate (convenience function)."""
    _require_crypto()
    return create_self_signed_server_cert(
        common_name=None,
        organization_name=organization,
        validity_days=validity_days,
        alt_names=alt_names or [common_name],
        key_type=key_type,
    )


# Convenience functions for common use cases
def x_create_self_signed__mutmut_7(
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
        organization_name=None,
        validity_days=validity_days,
        alt_names=alt_names or [common_name],
        key_type=key_type,
    )


# Convenience functions for common use cases
def x_create_self_signed__mutmut_8(
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
        validity_days=None,
        alt_names=alt_names or [common_name],
        key_type=key_type,
    )


# Convenience functions for common use cases
def x_create_self_signed__mutmut_9(
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
        alt_names=None,
        key_type=key_type,
    )


# Convenience functions for common use cases
def x_create_self_signed__mutmut_10(
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
        key_type=None,
    )


# Convenience functions for common use cases
def x_create_self_signed__mutmut_11(
    common_name: str = "localhost",
    alt_names: list[str] | None = None,
    organization: str = "Default Organization",
    validity_days: int = DEFAULT_CERTIFICATE_VALIDITY_DAYS,
    key_type: str = DEFAULT_CERTIFICATE_KEY_TYPE,
) -> Certificate:
    """Create a self-signed certificate (convenience function)."""
    _require_crypto()
    return create_self_signed_server_cert(
        organization_name=organization,
        validity_days=validity_days,
        alt_names=alt_names or [common_name],
        key_type=key_type,
    )


# Convenience functions for common use cases
def x_create_self_signed__mutmut_12(
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
        validity_days=validity_days,
        alt_names=alt_names or [common_name],
        key_type=key_type,
    )


# Convenience functions for common use cases
def x_create_self_signed__mutmut_13(
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
        alt_names=alt_names or [common_name],
        key_type=key_type,
    )


# Convenience functions for common use cases
def x_create_self_signed__mutmut_14(
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
        key_type=key_type,
    )


# Convenience functions for common use cases
def x_create_self_signed__mutmut_15(
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
    )


# Convenience functions for common use cases
def x_create_self_signed__mutmut_16(
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
        alt_names=alt_names and [common_name],
        key_type=key_type,
    )


x_create_self_signed__mutmut_mutants: ClassVar[MutantDict] = {
    "x_create_self_signed__mutmut_1": x_create_self_signed__mutmut_1,
    "x_create_self_signed__mutmut_2": x_create_self_signed__mutmut_2,
    "x_create_self_signed__mutmut_3": x_create_self_signed__mutmut_3,
    "x_create_self_signed__mutmut_4": x_create_self_signed__mutmut_4,
    "x_create_self_signed__mutmut_5": x_create_self_signed__mutmut_5,
    "x_create_self_signed__mutmut_6": x_create_self_signed__mutmut_6,
    "x_create_self_signed__mutmut_7": x_create_self_signed__mutmut_7,
    "x_create_self_signed__mutmut_8": x_create_self_signed__mutmut_8,
    "x_create_self_signed__mutmut_9": x_create_self_signed__mutmut_9,
    "x_create_self_signed__mutmut_10": x_create_self_signed__mutmut_10,
    "x_create_self_signed__mutmut_11": x_create_self_signed__mutmut_11,
    "x_create_self_signed__mutmut_12": x_create_self_signed__mutmut_12,
    "x_create_self_signed__mutmut_13": x_create_self_signed__mutmut_13,
    "x_create_self_signed__mutmut_14": x_create_self_signed__mutmut_14,
    "x_create_self_signed__mutmut_15": x_create_self_signed__mutmut_15,
    "x_create_self_signed__mutmut_16": x_create_self_signed__mutmut_16,
}


def create_self_signed(*args, **kwargs):
    result = _mutmut_trampoline(
        x_create_self_signed__mutmut_orig, x_create_self_signed__mutmut_mutants, args, kwargs
    )
    return result


create_self_signed.__signature__ = _mutmut_signature(x_create_self_signed__mutmut_orig)
x_create_self_signed__mutmut_orig.__name__ = "x_create_self_signed"


def x_create_ca__mutmut_orig(
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


def x_create_ca__mutmut_1(
    common_name: str,
    organization: str = "XXDefault CA OrganizationXX",
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


def x_create_ca__mutmut_2(
    common_name: str,
    organization: str = "default ca organization",
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


def x_create_ca__mutmut_3(
    common_name: str,
    organization: str = "DEFAULT CA ORGANIZATION",
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


def x_create_ca__mutmut_4(
    common_name: str,
    organization: str = "Default CA Organization",
    validity_days: int = DEFAULT_CERTIFICATE_VALIDITY_DAYS * 2,  # CAs live longer
    key_type: str = DEFAULT_CERTIFICATE_KEY_TYPE,
) -> Certificate:
    """Create a CA certificate (convenience function)."""
    _require_crypto()
    return create_ca_certificate(
        common_name=None,
        organization_name=organization,
        validity_days=validity_days,
        key_type=key_type,
    )


def x_create_ca__mutmut_5(
    common_name: str,
    organization: str = "Default CA Organization",
    validity_days: int = DEFAULT_CERTIFICATE_VALIDITY_DAYS * 2,  # CAs live longer
    key_type: str = DEFAULT_CERTIFICATE_KEY_TYPE,
) -> Certificate:
    """Create a CA certificate (convenience function)."""
    _require_crypto()
    return create_ca_certificate(
        common_name=common_name,
        organization_name=None,
        validity_days=validity_days,
        key_type=key_type,
    )


def x_create_ca__mutmut_6(
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
        validity_days=None,
        key_type=key_type,
    )


def x_create_ca__mutmut_7(
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
        key_type=None,
    )


def x_create_ca__mutmut_8(
    common_name: str,
    organization: str = "Default CA Organization",
    validity_days: int = DEFAULT_CERTIFICATE_VALIDITY_DAYS * 2,  # CAs live longer
    key_type: str = DEFAULT_CERTIFICATE_KEY_TYPE,
) -> Certificate:
    """Create a CA certificate (convenience function)."""
    _require_crypto()
    return create_ca_certificate(
        organization_name=organization,
        validity_days=validity_days,
        key_type=key_type,
    )


def x_create_ca__mutmut_9(
    common_name: str,
    organization: str = "Default CA Organization",
    validity_days: int = DEFAULT_CERTIFICATE_VALIDITY_DAYS * 2,  # CAs live longer
    key_type: str = DEFAULT_CERTIFICATE_KEY_TYPE,
) -> Certificate:
    """Create a CA certificate (convenience function)."""
    _require_crypto()
    return create_ca_certificate(
        common_name=common_name,
        validity_days=validity_days,
        key_type=key_type,
    )


def x_create_ca__mutmut_10(
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
        key_type=key_type,
    )


def x_create_ca__mutmut_11(
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
    )


x_create_ca__mutmut_mutants: ClassVar[MutantDict] = {
    "x_create_ca__mutmut_1": x_create_ca__mutmut_1,
    "x_create_ca__mutmut_2": x_create_ca__mutmut_2,
    "x_create_ca__mutmut_3": x_create_ca__mutmut_3,
    "x_create_ca__mutmut_4": x_create_ca__mutmut_4,
    "x_create_ca__mutmut_5": x_create_ca__mutmut_5,
    "x_create_ca__mutmut_6": x_create_ca__mutmut_6,
    "x_create_ca__mutmut_7": x_create_ca__mutmut_7,
    "x_create_ca__mutmut_8": x_create_ca__mutmut_8,
    "x_create_ca__mutmut_9": x_create_ca__mutmut_9,
    "x_create_ca__mutmut_10": x_create_ca__mutmut_10,
    "x_create_ca__mutmut_11": x_create_ca__mutmut_11,
}


def create_ca(*args, **kwargs):
    result = _mutmut_trampoline(x_create_ca__mutmut_orig, x_create_ca__mutmut_mutants, args, kwargs)
    return result


create_ca.__signature__ = _mutmut_signature(x_create_ca__mutmut_orig)
x_create_ca__mutmut_orig.__name__ = "x_create_ca"


# <3 🧱🤝🔒🪄
