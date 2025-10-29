# provide/foundation/crypto/certificates/trust.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from typing import TYPE_CHECKING

from provide.foundation import logger
from provide.foundation.crypto.certificates.base import CertificateError
from provide.foundation.crypto.certificates.operations import validate_signature

"""Certificate trust chain and verification utilities."""

if TYPE_CHECKING:
    from provide.foundation.crypto.certificates.certificate import Certificate

try:
    import cryptography  # noqa: F401

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


def x_verify_trust__mutmut_orig(
    cert: Certificate,
    other_cert: Certificate,
    trust_chain: list[Certificate],
) -> bool:
    """Verifies if the other_cert is trusted based on this certificate's trust chain.

    Args:
        cert: The certificate doing the verification
        other_cert: The certificate to verify
        trust_chain: List of trusted certificates

    Returns:
        True if the certificate is trusted, False otherwise

    """
    if other_cert is None:
        raise CertificateError("Cannot verify trust: other_cert is None")

    logger.debug(
        f"📜🔍🚀 Verifying trust for cert S/N {other_cert.serial_number} "
        f"against chain of S/N {cert.serial_number}",
    )

    if not other_cert.is_valid:
        logger.debug("📜🔍⚠️ Trust verification failed: Other certificate is not valid")
        return False
    if not other_cert.public_key:
        raise CertificateError("Cannot verify trust: Other certificate has no public key")

    if cert == other_cert:
        logger.debug("📜🔍✅ Trust verified: Certificates are identical (based on subject/serial)")
        return True

    if other_cert in trust_chain:
        logger.debug("📜🔍✅ Trust verified: Other certificate found in trust chain")
        return True

    for trusted_cert in trust_chain:
        logger.debug(f"📜🔍🔁 Checking signature against trusted cert S/N {trusted_cert.serial_number}")
        if validate_signature_wrapper(signed_cert=other_cert, signing_cert=trusted_cert):
            logger.debug(
                f"📜🔍✅ Trust verified: Other cert signed by trusted cert S/N {trusted_cert.serial_number}",
            )
            return True

    logger.debug(
        "📜🔍❌ Trust verification failed: Other certificate not identical, "
        "not in chain, and not signed by any cert in chain",
    )
    return False


def x_verify_trust__mutmut_1(
    cert: Certificate,
    other_cert: Certificate,
    trust_chain: list[Certificate],
) -> bool:
    """Verifies if the other_cert is trusted based on this certificate's trust chain.

    Args:
        cert: The certificate doing the verification
        other_cert: The certificate to verify
        trust_chain: List of trusted certificates

    Returns:
        True if the certificate is trusted, False otherwise

    """
    if other_cert is not None:
        raise CertificateError("Cannot verify trust: other_cert is None")

    logger.debug(
        f"📜🔍🚀 Verifying trust for cert S/N {other_cert.serial_number} "
        f"against chain of S/N {cert.serial_number}",
    )

    if not other_cert.is_valid:
        logger.debug("📜🔍⚠️ Trust verification failed: Other certificate is not valid")
        return False
    if not other_cert.public_key:
        raise CertificateError("Cannot verify trust: Other certificate has no public key")

    if cert == other_cert:
        logger.debug("📜🔍✅ Trust verified: Certificates are identical (based on subject/serial)")
        return True

    if other_cert in trust_chain:
        logger.debug("📜🔍✅ Trust verified: Other certificate found in trust chain")
        return True

    for trusted_cert in trust_chain:
        logger.debug(f"📜🔍🔁 Checking signature against trusted cert S/N {trusted_cert.serial_number}")
        if validate_signature_wrapper(signed_cert=other_cert, signing_cert=trusted_cert):
            logger.debug(
                f"📜🔍✅ Trust verified: Other cert signed by trusted cert S/N {trusted_cert.serial_number}",
            )
            return True

    logger.debug(
        "📜🔍❌ Trust verification failed: Other certificate not identical, "
        "not in chain, and not signed by any cert in chain",
    )
    return False


def x_verify_trust__mutmut_2(
    cert: Certificate,
    other_cert: Certificate,
    trust_chain: list[Certificate],
) -> bool:
    """Verifies if the other_cert is trusted based on this certificate's trust chain.

    Args:
        cert: The certificate doing the verification
        other_cert: The certificate to verify
        trust_chain: List of trusted certificates

    Returns:
        True if the certificate is trusted, False otherwise

    """
    if other_cert is None:
        raise CertificateError(None)

    logger.debug(
        f"📜🔍🚀 Verifying trust for cert S/N {other_cert.serial_number} "
        f"against chain of S/N {cert.serial_number}",
    )

    if not other_cert.is_valid:
        logger.debug("📜🔍⚠️ Trust verification failed: Other certificate is not valid")
        return False
    if not other_cert.public_key:
        raise CertificateError("Cannot verify trust: Other certificate has no public key")

    if cert == other_cert:
        logger.debug("📜🔍✅ Trust verified: Certificates are identical (based on subject/serial)")
        return True

    if other_cert in trust_chain:
        logger.debug("📜🔍✅ Trust verified: Other certificate found in trust chain")
        return True

    for trusted_cert in trust_chain:
        logger.debug(f"📜🔍🔁 Checking signature against trusted cert S/N {trusted_cert.serial_number}")
        if validate_signature_wrapper(signed_cert=other_cert, signing_cert=trusted_cert):
            logger.debug(
                f"📜🔍✅ Trust verified: Other cert signed by trusted cert S/N {trusted_cert.serial_number}",
            )
            return True

    logger.debug(
        "📜🔍❌ Trust verification failed: Other certificate not identical, "
        "not in chain, and not signed by any cert in chain",
    )
    return False


def x_verify_trust__mutmut_3(
    cert: Certificate,
    other_cert: Certificate,
    trust_chain: list[Certificate],
) -> bool:
    """Verifies if the other_cert is trusted based on this certificate's trust chain.

    Args:
        cert: The certificate doing the verification
        other_cert: The certificate to verify
        trust_chain: List of trusted certificates

    Returns:
        True if the certificate is trusted, False otherwise

    """
    if other_cert is None:
        raise CertificateError("XXCannot verify trust: other_cert is NoneXX")

    logger.debug(
        f"📜🔍🚀 Verifying trust for cert S/N {other_cert.serial_number} "
        f"against chain of S/N {cert.serial_number}",
    )

    if not other_cert.is_valid:
        logger.debug("📜🔍⚠️ Trust verification failed: Other certificate is not valid")
        return False
    if not other_cert.public_key:
        raise CertificateError("Cannot verify trust: Other certificate has no public key")

    if cert == other_cert:
        logger.debug("📜🔍✅ Trust verified: Certificates are identical (based on subject/serial)")
        return True

    if other_cert in trust_chain:
        logger.debug("📜🔍✅ Trust verified: Other certificate found in trust chain")
        return True

    for trusted_cert in trust_chain:
        logger.debug(f"📜🔍🔁 Checking signature against trusted cert S/N {trusted_cert.serial_number}")
        if validate_signature_wrapper(signed_cert=other_cert, signing_cert=trusted_cert):
            logger.debug(
                f"📜🔍✅ Trust verified: Other cert signed by trusted cert S/N {trusted_cert.serial_number}",
            )
            return True

    logger.debug(
        "📜🔍❌ Trust verification failed: Other certificate not identical, "
        "not in chain, and not signed by any cert in chain",
    )
    return False


def x_verify_trust__mutmut_4(
    cert: Certificate,
    other_cert: Certificate,
    trust_chain: list[Certificate],
) -> bool:
    """Verifies if the other_cert is trusted based on this certificate's trust chain.

    Args:
        cert: The certificate doing the verification
        other_cert: The certificate to verify
        trust_chain: List of trusted certificates

    Returns:
        True if the certificate is trusted, False otherwise

    """
    if other_cert is None:
        raise CertificateError("cannot verify trust: other_cert is none")

    logger.debug(
        f"📜🔍🚀 Verifying trust for cert S/N {other_cert.serial_number} "
        f"against chain of S/N {cert.serial_number}",
    )

    if not other_cert.is_valid:
        logger.debug("📜🔍⚠️ Trust verification failed: Other certificate is not valid")
        return False
    if not other_cert.public_key:
        raise CertificateError("Cannot verify trust: Other certificate has no public key")

    if cert == other_cert:
        logger.debug("📜🔍✅ Trust verified: Certificates are identical (based on subject/serial)")
        return True

    if other_cert in trust_chain:
        logger.debug("📜🔍✅ Trust verified: Other certificate found in trust chain")
        return True

    for trusted_cert in trust_chain:
        logger.debug(f"📜🔍🔁 Checking signature against trusted cert S/N {trusted_cert.serial_number}")
        if validate_signature_wrapper(signed_cert=other_cert, signing_cert=trusted_cert):
            logger.debug(
                f"📜🔍✅ Trust verified: Other cert signed by trusted cert S/N {trusted_cert.serial_number}",
            )
            return True

    logger.debug(
        "📜🔍❌ Trust verification failed: Other certificate not identical, "
        "not in chain, and not signed by any cert in chain",
    )
    return False


def x_verify_trust__mutmut_5(
    cert: Certificate,
    other_cert: Certificate,
    trust_chain: list[Certificate],
) -> bool:
    """Verifies if the other_cert is trusted based on this certificate's trust chain.

    Args:
        cert: The certificate doing the verification
        other_cert: The certificate to verify
        trust_chain: List of trusted certificates

    Returns:
        True if the certificate is trusted, False otherwise

    """
    if other_cert is None:
        raise CertificateError("CANNOT VERIFY TRUST: OTHER_CERT IS NONE")

    logger.debug(
        f"📜🔍🚀 Verifying trust for cert S/N {other_cert.serial_number} "
        f"against chain of S/N {cert.serial_number}",
    )

    if not other_cert.is_valid:
        logger.debug("📜🔍⚠️ Trust verification failed: Other certificate is not valid")
        return False
    if not other_cert.public_key:
        raise CertificateError("Cannot verify trust: Other certificate has no public key")

    if cert == other_cert:
        logger.debug("📜🔍✅ Trust verified: Certificates are identical (based on subject/serial)")
        return True

    if other_cert in trust_chain:
        logger.debug("📜🔍✅ Trust verified: Other certificate found in trust chain")
        return True

    for trusted_cert in trust_chain:
        logger.debug(f"📜🔍🔁 Checking signature against trusted cert S/N {trusted_cert.serial_number}")
        if validate_signature_wrapper(signed_cert=other_cert, signing_cert=trusted_cert):
            logger.debug(
                f"📜🔍✅ Trust verified: Other cert signed by trusted cert S/N {trusted_cert.serial_number}",
            )
            return True

    logger.debug(
        "📜🔍❌ Trust verification failed: Other certificate not identical, "
        "not in chain, and not signed by any cert in chain",
    )
    return False


def x_verify_trust__mutmut_6(
    cert: Certificate,
    other_cert: Certificate,
    trust_chain: list[Certificate],
) -> bool:
    """Verifies if the other_cert is trusted based on this certificate's trust chain.

    Args:
        cert: The certificate doing the verification
        other_cert: The certificate to verify
        trust_chain: List of trusted certificates

    Returns:
        True if the certificate is trusted, False otherwise

    """
    if other_cert is None:
        raise CertificateError("Cannot verify trust: other_cert is None")

    logger.debug(
        None,
    )

    if not other_cert.is_valid:
        logger.debug("📜🔍⚠️ Trust verification failed: Other certificate is not valid")
        return False
    if not other_cert.public_key:
        raise CertificateError("Cannot verify trust: Other certificate has no public key")

    if cert == other_cert:
        logger.debug("📜🔍✅ Trust verified: Certificates are identical (based on subject/serial)")
        return True

    if other_cert in trust_chain:
        logger.debug("📜🔍✅ Trust verified: Other certificate found in trust chain")
        return True

    for trusted_cert in trust_chain:
        logger.debug(f"📜🔍🔁 Checking signature against trusted cert S/N {trusted_cert.serial_number}")
        if validate_signature_wrapper(signed_cert=other_cert, signing_cert=trusted_cert):
            logger.debug(
                f"📜🔍✅ Trust verified: Other cert signed by trusted cert S/N {trusted_cert.serial_number}",
            )
            return True

    logger.debug(
        "📜🔍❌ Trust verification failed: Other certificate not identical, "
        "not in chain, and not signed by any cert in chain",
    )
    return False


def x_verify_trust__mutmut_7(
    cert: Certificate,
    other_cert: Certificate,
    trust_chain: list[Certificate],
) -> bool:
    """Verifies if the other_cert is trusted based on this certificate's trust chain.

    Args:
        cert: The certificate doing the verification
        other_cert: The certificate to verify
        trust_chain: List of trusted certificates

    Returns:
        True if the certificate is trusted, False otherwise

    """
    if other_cert is None:
        raise CertificateError("Cannot verify trust: other_cert is None")

    logger.debug(
        f"📜🔍🚀 Verifying trust for cert S/N {other_cert.serial_number} "
        f"against chain of S/N {cert.serial_number}",
    )

    if other_cert.is_valid:
        logger.debug("📜🔍⚠️ Trust verification failed: Other certificate is not valid")
        return False
    if not other_cert.public_key:
        raise CertificateError("Cannot verify trust: Other certificate has no public key")

    if cert == other_cert:
        logger.debug("📜🔍✅ Trust verified: Certificates are identical (based on subject/serial)")
        return True

    if other_cert in trust_chain:
        logger.debug("📜🔍✅ Trust verified: Other certificate found in trust chain")
        return True

    for trusted_cert in trust_chain:
        logger.debug(f"📜🔍🔁 Checking signature against trusted cert S/N {trusted_cert.serial_number}")
        if validate_signature_wrapper(signed_cert=other_cert, signing_cert=trusted_cert):
            logger.debug(
                f"📜🔍✅ Trust verified: Other cert signed by trusted cert S/N {trusted_cert.serial_number}",
            )
            return True

    logger.debug(
        "📜🔍❌ Trust verification failed: Other certificate not identical, "
        "not in chain, and not signed by any cert in chain",
    )
    return False


def x_verify_trust__mutmut_8(
    cert: Certificate,
    other_cert: Certificate,
    trust_chain: list[Certificate],
) -> bool:
    """Verifies if the other_cert is trusted based on this certificate's trust chain.

    Args:
        cert: The certificate doing the verification
        other_cert: The certificate to verify
        trust_chain: List of trusted certificates

    Returns:
        True if the certificate is trusted, False otherwise

    """
    if other_cert is None:
        raise CertificateError("Cannot verify trust: other_cert is None")

    logger.debug(
        f"📜🔍🚀 Verifying trust for cert S/N {other_cert.serial_number} "
        f"against chain of S/N {cert.serial_number}",
    )

    if not other_cert.is_valid:
        logger.debug(None)
        return False
    if not other_cert.public_key:
        raise CertificateError("Cannot verify trust: Other certificate has no public key")

    if cert == other_cert:
        logger.debug("📜🔍✅ Trust verified: Certificates are identical (based on subject/serial)")
        return True

    if other_cert in trust_chain:
        logger.debug("📜🔍✅ Trust verified: Other certificate found in trust chain")
        return True

    for trusted_cert in trust_chain:
        logger.debug(f"📜🔍🔁 Checking signature against trusted cert S/N {trusted_cert.serial_number}")
        if validate_signature_wrapper(signed_cert=other_cert, signing_cert=trusted_cert):
            logger.debug(
                f"📜🔍✅ Trust verified: Other cert signed by trusted cert S/N {trusted_cert.serial_number}",
            )
            return True

    logger.debug(
        "📜🔍❌ Trust verification failed: Other certificate not identical, "
        "not in chain, and not signed by any cert in chain",
    )
    return False


def x_verify_trust__mutmut_9(
    cert: Certificate,
    other_cert: Certificate,
    trust_chain: list[Certificate],
) -> bool:
    """Verifies if the other_cert is trusted based on this certificate's trust chain.

    Args:
        cert: The certificate doing the verification
        other_cert: The certificate to verify
        trust_chain: List of trusted certificates

    Returns:
        True if the certificate is trusted, False otherwise

    """
    if other_cert is None:
        raise CertificateError("Cannot verify trust: other_cert is None")

    logger.debug(
        f"📜🔍🚀 Verifying trust for cert S/N {other_cert.serial_number} "
        f"against chain of S/N {cert.serial_number}",
    )

    if not other_cert.is_valid:
        logger.debug("XX📜🔍⚠️ Trust verification failed: Other certificate is not validXX")
        return False
    if not other_cert.public_key:
        raise CertificateError("Cannot verify trust: Other certificate has no public key")

    if cert == other_cert:
        logger.debug("📜🔍✅ Trust verified: Certificates are identical (based on subject/serial)")
        return True

    if other_cert in trust_chain:
        logger.debug("📜🔍✅ Trust verified: Other certificate found in trust chain")
        return True

    for trusted_cert in trust_chain:
        logger.debug(f"📜🔍🔁 Checking signature against trusted cert S/N {trusted_cert.serial_number}")
        if validate_signature_wrapper(signed_cert=other_cert, signing_cert=trusted_cert):
            logger.debug(
                f"📜🔍✅ Trust verified: Other cert signed by trusted cert S/N {trusted_cert.serial_number}",
            )
            return True

    logger.debug(
        "📜🔍❌ Trust verification failed: Other certificate not identical, "
        "not in chain, and not signed by any cert in chain",
    )
    return False


def x_verify_trust__mutmut_10(
    cert: Certificate,
    other_cert: Certificate,
    trust_chain: list[Certificate],
) -> bool:
    """Verifies if the other_cert is trusted based on this certificate's trust chain.

    Args:
        cert: The certificate doing the verification
        other_cert: The certificate to verify
        trust_chain: List of trusted certificates

    Returns:
        True if the certificate is trusted, False otherwise

    """
    if other_cert is None:
        raise CertificateError("Cannot verify trust: other_cert is None")

    logger.debug(
        f"📜🔍🚀 Verifying trust for cert S/N {other_cert.serial_number} "
        f"against chain of S/N {cert.serial_number}",
    )

    if not other_cert.is_valid:
        logger.debug("📜🔍⚠️ trust verification failed: other certificate is not valid")
        return False
    if not other_cert.public_key:
        raise CertificateError("Cannot verify trust: Other certificate has no public key")

    if cert == other_cert:
        logger.debug("📜🔍✅ Trust verified: Certificates are identical (based on subject/serial)")
        return True

    if other_cert in trust_chain:
        logger.debug("📜🔍✅ Trust verified: Other certificate found in trust chain")
        return True

    for trusted_cert in trust_chain:
        logger.debug(f"📜🔍🔁 Checking signature against trusted cert S/N {trusted_cert.serial_number}")
        if validate_signature_wrapper(signed_cert=other_cert, signing_cert=trusted_cert):
            logger.debug(
                f"📜🔍✅ Trust verified: Other cert signed by trusted cert S/N {trusted_cert.serial_number}",
            )
            return True

    logger.debug(
        "📜🔍❌ Trust verification failed: Other certificate not identical, "
        "not in chain, and not signed by any cert in chain",
    )
    return False


def x_verify_trust__mutmut_11(
    cert: Certificate,
    other_cert: Certificate,
    trust_chain: list[Certificate],
) -> bool:
    """Verifies if the other_cert is trusted based on this certificate's trust chain.

    Args:
        cert: The certificate doing the verification
        other_cert: The certificate to verify
        trust_chain: List of trusted certificates

    Returns:
        True if the certificate is trusted, False otherwise

    """
    if other_cert is None:
        raise CertificateError("Cannot verify trust: other_cert is None")

    logger.debug(
        f"📜🔍🚀 Verifying trust for cert S/N {other_cert.serial_number} "
        f"against chain of S/N {cert.serial_number}",
    )

    if not other_cert.is_valid:
        logger.debug("📜🔍⚠️ TRUST VERIFICATION FAILED: OTHER CERTIFICATE IS NOT VALID")
        return False
    if not other_cert.public_key:
        raise CertificateError("Cannot verify trust: Other certificate has no public key")

    if cert == other_cert:
        logger.debug("📜🔍✅ Trust verified: Certificates are identical (based on subject/serial)")
        return True

    if other_cert in trust_chain:
        logger.debug("📜🔍✅ Trust verified: Other certificate found in trust chain")
        return True

    for trusted_cert in trust_chain:
        logger.debug(f"📜🔍🔁 Checking signature against trusted cert S/N {trusted_cert.serial_number}")
        if validate_signature_wrapper(signed_cert=other_cert, signing_cert=trusted_cert):
            logger.debug(
                f"📜🔍✅ Trust verified: Other cert signed by trusted cert S/N {trusted_cert.serial_number}",
            )
            return True

    logger.debug(
        "📜🔍❌ Trust verification failed: Other certificate not identical, "
        "not in chain, and not signed by any cert in chain",
    )
    return False


def x_verify_trust__mutmut_12(
    cert: Certificate,
    other_cert: Certificate,
    trust_chain: list[Certificate],
) -> bool:
    """Verifies if the other_cert is trusted based on this certificate's trust chain.

    Args:
        cert: The certificate doing the verification
        other_cert: The certificate to verify
        trust_chain: List of trusted certificates

    Returns:
        True if the certificate is trusted, False otherwise

    """
    if other_cert is None:
        raise CertificateError("Cannot verify trust: other_cert is None")

    logger.debug(
        f"📜🔍🚀 Verifying trust for cert S/N {other_cert.serial_number} "
        f"against chain of S/N {cert.serial_number}",
    )

    if not other_cert.is_valid:
        logger.debug("📜🔍⚠️ Trust verification failed: Other certificate is not valid")
        return True
    if not other_cert.public_key:
        raise CertificateError("Cannot verify trust: Other certificate has no public key")

    if cert == other_cert:
        logger.debug("📜🔍✅ Trust verified: Certificates are identical (based on subject/serial)")
        return True

    if other_cert in trust_chain:
        logger.debug("📜🔍✅ Trust verified: Other certificate found in trust chain")
        return True

    for trusted_cert in trust_chain:
        logger.debug(f"📜🔍🔁 Checking signature against trusted cert S/N {trusted_cert.serial_number}")
        if validate_signature_wrapper(signed_cert=other_cert, signing_cert=trusted_cert):
            logger.debug(
                f"📜🔍✅ Trust verified: Other cert signed by trusted cert S/N {trusted_cert.serial_number}",
            )
            return True

    logger.debug(
        "📜🔍❌ Trust verification failed: Other certificate not identical, "
        "not in chain, and not signed by any cert in chain",
    )
    return False


def x_verify_trust__mutmut_13(
    cert: Certificate,
    other_cert: Certificate,
    trust_chain: list[Certificate],
) -> bool:
    """Verifies if the other_cert is trusted based on this certificate's trust chain.

    Args:
        cert: The certificate doing the verification
        other_cert: The certificate to verify
        trust_chain: List of trusted certificates

    Returns:
        True if the certificate is trusted, False otherwise

    """
    if other_cert is None:
        raise CertificateError("Cannot verify trust: other_cert is None")

    logger.debug(
        f"📜🔍🚀 Verifying trust for cert S/N {other_cert.serial_number} "
        f"against chain of S/N {cert.serial_number}",
    )

    if not other_cert.is_valid:
        logger.debug("📜🔍⚠️ Trust verification failed: Other certificate is not valid")
        return False
    if other_cert.public_key:
        raise CertificateError("Cannot verify trust: Other certificate has no public key")

    if cert == other_cert:
        logger.debug("📜🔍✅ Trust verified: Certificates are identical (based on subject/serial)")
        return True

    if other_cert in trust_chain:
        logger.debug("📜🔍✅ Trust verified: Other certificate found in trust chain")
        return True

    for trusted_cert in trust_chain:
        logger.debug(f"📜🔍🔁 Checking signature against trusted cert S/N {trusted_cert.serial_number}")
        if validate_signature_wrapper(signed_cert=other_cert, signing_cert=trusted_cert):
            logger.debug(
                f"📜🔍✅ Trust verified: Other cert signed by trusted cert S/N {trusted_cert.serial_number}",
            )
            return True

    logger.debug(
        "📜🔍❌ Trust verification failed: Other certificate not identical, "
        "not in chain, and not signed by any cert in chain",
    )
    return False


def x_verify_trust__mutmut_14(
    cert: Certificate,
    other_cert: Certificate,
    trust_chain: list[Certificate],
) -> bool:
    """Verifies if the other_cert is trusted based on this certificate's trust chain.

    Args:
        cert: The certificate doing the verification
        other_cert: The certificate to verify
        trust_chain: List of trusted certificates

    Returns:
        True if the certificate is trusted, False otherwise

    """
    if other_cert is None:
        raise CertificateError("Cannot verify trust: other_cert is None")

    logger.debug(
        f"📜🔍🚀 Verifying trust for cert S/N {other_cert.serial_number} "
        f"against chain of S/N {cert.serial_number}",
    )

    if not other_cert.is_valid:
        logger.debug("📜🔍⚠️ Trust verification failed: Other certificate is not valid")
        return False
    if not other_cert.public_key:
        raise CertificateError(None)

    if cert == other_cert:
        logger.debug("📜🔍✅ Trust verified: Certificates are identical (based on subject/serial)")
        return True

    if other_cert in trust_chain:
        logger.debug("📜🔍✅ Trust verified: Other certificate found in trust chain")
        return True

    for trusted_cert in trust_chain:
        logger.debug(f"📜🔍🔁 Checking signature against trusted cert S/N {trusted_cert.serial_number}")
        if validate_signature_wrapper(signed_cert=other_cert, signing_cert=trusted_cert):
            logger.debug(
                f"📜🔍✅ Trust verified: Other cert signed by trusted cert S/N {trusted_cert.serial_number}",
            )
            return True

    logger.debug(
        "📜🔍❌ Trust verification failed: Other certificate not identical, "
        "not in chain, and not signed by any cert in chain",
    )
    return False


def x_verify_trust__mutmut_15(
    cert: Certificate,
    other_cert: Certificate,
    trust_chain: list[Certificate],
) -> bool:
    """Verifies if the other_cert is trusted based on this certificate's trust chain.

    Args:
        cert: The certificate doing the verification
        other_cert: The certificate to verify
        trust_chain: List of trusted certificates

    Returns:
        True if the certificate is trusted, False otherwise

    """
    if other_cert is None:
        raise CertificateError("Cannot verify trust: other_cert is None")

    logger.debug(
        f"📜🔍🚀 Verifying trust for cert S/N {other_cert.serial_number} "
        f"against chain of S/N {cert.serial_number}",
    )

    if not other_cert.is_valid:
        logger.debug("📜🔍⚠️ Trust verification failed: Other certificate is not valid")
        return False
    if not other_cert.public_key:
        raise CertificateError("XXCannot verify trust: Other certificate has no public keyXX")

    if cert == other_cert:
        logger.debug("📜🔍✅ Trust verified: Certificates are identical (based on subject/serial)")
        return True

    if other_cert in trust_chain:
        logger.debug("📜🔍✅ Trust verified: Other certificate found in trust chain")
        return True

    for trusted_cert in trust_chain:
        logger.debug(f"📜🔍🔁 Checking signature against trusted cert S/N {trusted_cert.serial_number}")
        if validate_signature_wrapper(signed_cert=other_cert, signing_cert=trusted_cert):
            logger.debug(
                f"📜🔍✅ Trust verified: Other cert signed by trusted cert S/N {trusted_cert.serial_number}",
            )
            return True

    logger.debug(
        "📜🔍❌ Trust verification failed: Other certificate not identical, "
        "not in chain, and not signed by any cert in chain",
    )
    return False


def x_verify_trust__mutmut_16(
    cert: Certificate,
    other_cert: Certificate,
    trust_chain: list[Certificate],
) -> bool:
    """Verifies if the other_cert is trusted based on this certificate's trust chain.

    Args:
        cert: The certificate doing the verification
        other_cert: The certificate to verify
        trust_chain: List of trusted certificates

    Returns:
        True if the certificate is trusted, False otherwise

    """
    if other_cert is None:
        raise CertificateError("Cannot verify trust: other_cert is None")

    logger.debug(
        f"📜🔍🚀 Verifying trust for cert S/N {other_cert.serial_number} "
        f"against chain of S/N {cert.serial_number}",
    )

    if not other_cert.is_valid:
        logger.debug("📜🔍⚠️ Trust verification failed: Other certificate is not valid")
        return False
    if not other_cert.public_key:
        raise CertificateError("cannot verify trust: other certificate has no public key")

    if cert == other_cert:
        logger.debug("📜🔍✅ Trust verified: Certificates are identical (based on subject/serial)")
        return True

    if other_cert in trust_chain:
        logger.debug("📜🔍✅ Trust verified: Other certificate found in trust chain")
        return True

    for trusted_cert in trust_chain:
        logger.debug(f"📜🔍🔁 Checking signature against trusted cert S/N {trusted_cert.serial_number}")
        if validate_signature_wrapper(signed_cert=other_cert, signing_cert=trusted_cert):
            logger.debug(
                f"📜🔍✅ Trust verified: Other cert signed by trusted cert S/N {trusted_cert.serial_number}",
            )
            return True

    logger.debug(
        "📜🔍❌ Trust verification failed: Other certificate not identical, "
        "not in chain, and not signed by any cert in chain",
    )
    return False


def x_verify_trust__mutmut_17(
    cert: Certificate,
    other_cert: Certificate,
    trust_chain: list[Certificate],
) -> bool:
    """Verifies if the other_cert is trusted based on this certificate's trust chain.

    Args:
        cert: The certificate doing the verification
        other_cert: The certificate to verify
        trust_chain: List of trusted certificates

    Returns:
        True if the certificate is trusted, False otherwise

    """
    if other_cert is None:
        raise CertificateError("Cannot verify trust: other_cert is None")

    logger.debug(
        f"📜🔍🚀 Verifying trust for cert S/N {other_cert.serial_number} "
        f"against chain of S/N {cert.serial_number}",
    )

    if not other_cert.is_valid:
        logger.debug("📜🔍⚠️ Trust verification failed: Other certificate is not valid")
        return False
    if not other_cert.public_key:
        raise CertificateError("CANNOT VERIFY TRUST: OTHER CERTIFICATE HAS NO PUBLIC KEY")

    if cert == other_cert:
        logger.debug("📜🔍✅ Trust verified: Certificates are identical (based on subject/serial)")
        return True

    if other_cert in trust_chain:
        logger.debug("📜🔍✅ Trust verified: Other certificate found in trust chain")
        return True

    for trusted_cert in trust_chain:
        logger.debug(f"📜🔍🔁 Checking signature against trusted cert S/N {trusted_cert.serial_number}")
        if validate_signature_wrapper(signed_cert=other_cert, signing_cert=trusted_cert):
            logger.debug(
                f"📜🔍✅ Trust verified: Other cert signed by trusted cert S/N {trusted_cert.serial_number}",
            )
            return True

    logger.debug(
        "📜🔍❌ Trust verification failed: Other certificate not identical, "
        "not in chain, and not signed by any cert in chain",
    )
    return False


def x_verify_trust__mutmut_18(
    cert: Certificate,
    other_cert: Certificate,
    trust_chain: list[Certificate],
) -> bool:
    """Verifies if the other_cert is trusted based on this certificate's trust chain.

    Args:
        cert: The certificate doing the verification
        other_cert: The certificate to verify
        trust_chain: List of trusted certificates

    Returns:
        True if the certificate is trusted, False otherwise

    """
    if other_cert is None:
        raise CertificateError("Cannot verify trust: other_cert is None")

    logger.debug(
        f"📜🔍🚀 Verifying trust for cert S/N {other_cert.serial_number} "
        f"against chain of S/N {cert.serial_number}",
    )

    if not other_cert.is_valid:
        logger.debug("📜🔍⚠️ Trust verification failed: Other certificate is not valid")
        return False
    if not other_cert.public_key:
        raise CertificateError("Cannot verify trust: Other certificate has no public key")

    if cert != other_cert:
        logger.debug("📜🔍✅ Trust verified: Certificates are identical (based on subject/serial)")
        return True

    if other_cert in trust_chain:
        logger.debug("📜🔍✅ Trust verified: Other certificate found in trust chain")
        return True

    for trusted_cert in trust_chain:
        logger.debug(f"📜🔍🔁 Checking signature against trusted cert S/N {trusted_cert.serial_number}")
        if validate_signature_wrapper(signed_cert=other_cert, signing_cert=trusted_cert):
            logger.debug(
                f"📜🔍✅ Trust verified: Other cert signed by trusted cert S/N {trusted_cert.serial_number}",
            )
            return True

    logger.debug(
        "📜🔍❌ Trust verification failed: Other certificate not identical, "
        "not in chain, and not signed by any cert in chain",
    )
    return False


def x_verify_trust__mutmut_19(
    cert: Certificate,
    other_cert: Certificate,
    trust_chain: list[Certificate],
) -> bool:
    """Verifies if the other_cert is trusted based on this certificate's trust chain.

    Args:
        cert: The certificate doing the verification
        other_cert: The certificate to verify
        trust_chain: List of trusted certificates

    Returns:
        True if the certificate is trusted, False otherwise

    """
    if other_cert is None:
        raise CertificateError("Cannot verify trust: other_cert is None")

    logger.debug(
        f"📜🔍🚀 Verifying trust for cert S/N {other_cert.serial_number} "
        f"against chain of S/N {cert.serial_number}",
    )

    if not other_cert.is_valid:
        logger.debug("📜🔍⚠️ Trust verification failed: Other certificate is not valid")
        return False
    if not other_cert.public_key:
        raise CertificateError("Cannot verify trust: Other certificate has no public key")

    if cert == other_cert:
        logger.debug(None)
        return True

    if other_cert in trust_chain:
        logger.debug("📜🔍✅ Trust verified: Other certificate found in trust chain")
        return True

    for trusted_cert in trust_chain:
        logger.debug(f"📜🔍🔁 Checking signature against trusted cert S/N {trusted_cert.serial_number}")
        if validate_signature_wrapper(signed_cert=other_cert, signing_cert=trusted_cert):
            logger.debug(
                f"📜🔍✅ Trust verified: Other cert signed by trusted cert S/N {trusted_cert.serial_number}",
            )
            return True

    logger.debug(
        "📜🔍❌ Trust verification failed: Other certificate not identical, "
        "not in chain, and not signed by any cert in chain",
    )
    return False


def x_verify_trust__mutmut_20(
    cert: Certificate,
    other_cert: Certificate,
    trust_chain: list[Certificate],
) -> bool:
    """Verifies if the other_cert is trusted based on this certificate's trust chain.

    Args:
        cert: The certificate doing the verification
        other_cert: The certificate to verify
        trust_chain: List of trusted certificates

    Returns:
        True if the certificate is trusted, False otherwise

    """
    if other_cert is None:
        raise CertificateError("Cannot verify trust: other_cert is None")

    logger.debug(
        f"📜🔍🚀 Verifying trust for cert S/N {other_cert.serial_number} "
        f"against chain of S/N {cert.serial_number}",
    )

    if not other_cert.is_valid:
        logger.debug("📜🔍⚠️ Trust verification failed: Other certificate is not valid")
        return False
    if not other_cert.public_key:
        raise CertificateError("Cannot verify trust: Other certificate has no public key")

    if cert == other_cert:
        logger.debug("XX📜🔍✅ Trust verified: Certificates are identical (based on subject/serial)XX")
        return True

    if other_cert in trust_chain:
        logger.debug("📜🔍✅ Trust verified: Other certificate found in trust chain")
        return True

    for trusted_cert in trust_chain:
        logger.debug(f"📜🔍🔁 Checking signature against trusted cert S/N {trusted_cert.serial_number}")
        if validate_signature_wrapper(signed_cert=other_cert, signing_cert=trusted_cert):
            logger.debug(
                f"📜🔍✅ Trust verified: Other cert signed by trusted cert S/N {trusted_cert.serial_number}",
            )
            return True

    logger.debug(
        "📜🔍❌ Trust verification failed: Other certificate not identical, "
        "not in chain, and not signed by any cert in chain",
    )
    return False


def x_verify_trust__mutmut_21(
    cert: Certificate,
    other_cert: Certificate,
    trust_chain: list[Certificate],
) -> bool:
    """Verifies if the other_cert is trusted based on this certificate's trust chain.

    Args:
        cert: The certificate doing the verification
        other_cert: The certificate to verify
        trust_chain: List of trusted certificates

    Returns:
        True if the certificate is trusted, False otherwise

    """
    if other_cert is None:
        raise CertificateError("Cannot verify trust: other_cert is None")

    logger.debug(
        f"📜🔍🚀 Verifying trust for cert S/N {other_cert.serial_number} "
        f"against chain of S/N {cert.serial_number}",
    )

    if not other_cert.is_valid:
        logger.debug("📜🔍⚠️ Trust verification failed: Other certificate is not valid")
        return False
    if not other_cert.public_key:
        raise CertificateError("Cannot verify trust: Other certificate has no public key")

    if cert == other_cert:
        logger.debug("📜🔍✅ trust verified: certificates are identical (based on subject/serial)")
        return True

    if other_cert in trust_chain:
        logger.debug("📜🔍✅ Trust verified: Other certificate found in trust chain")
        return True

    for trusted_cert in trust_chain:
        logger.debug(f"📜🔍🔁 Checking signature against trusted cert S/N {trusted_cert.serial_number}")
        if validate_signature_wrapper(signed_cert=other_cert, signing_cert=trusted_cert):
            logger.debug(
                f"📜🔍✅ Trust verified: Other cert signed by trusted cert S/N {trusted_cert.serial_number}",
            )
            return True

    logger.debug(
        "📜🔍❌ Trust verification failed: Other certificate not identical, "
        "not in chain, and not signed by any cert in chain",
    )
    return False


def x_verify_trust__mutmut_22(
    cert: Certificate,
    other_cert: Certificate,
    trust_chain: list[Certificate],
) -> bool:
    """Verifies if the other_cert is trusted based on this certificate's trust chain.

    Args:
        cert: The certificate doing the verification
        other_cert: The certificate to verify
        trust_chain: List of trusted certificates

    Returns:
        True if the certificate is trusted, False otherwise

    """
    if other_cert is None:
        raise CertificateError("Cannot verify trust: other_cert is None")

    logger.debug(
        f"📜🔍🚀 Verifying trust for cert S/N {other_cert.serial_number} "
        f"against chain of S/N {cert.serial_number}",
    )

    if not other_cert.is_valid:
        logger.debug("📜🔍⚠️ Trust verification failed: Other certificate is not valid")
        return False
    if not other_cert.public_key:
        raise CertificateError("Cannot verify trust: Other certificate has no public key")

    if cert == other_cert:
        logger.debug("📜🔍✅ TRUST VERIFIED: CERTIFICATES ARE IDENTICAL (BASED ON SUBJECT/SERIAL)")
        return True

    if other_cert in trust_chain:
        logger.debug("📜🔍✅ Trust verified: Other certificate found in trust chain")
        return True

    for trusted_cert in trust_chain:
        logger.debug(f"📜🔍🔁 Checking signature against trusted cert S/N {trusted_cert.serial_number}")
        if validate_signature_wrapper(signed_cert=other_cert, signing_cert=trusted_cert):
            logger.debug(
                f"📜🔍✅ Trust verified: Other cert signed by trusted cert S/N {trusted_cert.serial_number}",
            )
            return True

    logger.debug(
        "📜🔍❌ Trust verification failed: Other certificate not identical, "
        "not in chain, and not signed by any cert in chain",
    )
    return False


def x_verify_trust__mutmut_23(
    cert: Certificate,
    other_cert: Certificate,
    trust_chain: list[Certificate],
) -> bool:
    """Verifies if the other_cert is trusted based on this certificate's trust chain.

    Args:
        cert: The certificate doing the verification
        other_cert: The certificate to verify
        trust_chain: List of trusted certificates

    Returns:
        True if the certificate is trusted, False otherwise

    """
    if other_cert is None:
        raise CertificateError("Cannot verify trust: other_cert is None")

    logger.debug(
        f"📜🔍🚀 Verifying trust for cert S/N {other_cert.serial_number} "
        f"against chain of S/N {cert.serial_number}",
    )

    if not other_cert.is_valid:
        logger.debug("📜🔍⚠️ Trust verification failed: Other certificate is not valid")
        return False
    if not other_cert.public_key:
        raise CertificateError("Cannot verify trust: Other certificate has no public key")

    if cert == other_cert:
        logger.debug("📜🔍✅ Trust verified: Certificates are identical (based on subject/serial)")
        return False

    if other_cert in trust_chain:
        logger.debug("📜🔍✅ Trust verified: Other certificate found in trust chain")
        return True

    for trusted_cert in trust_chain:
        logger.debug(f"📜🔍🔁 Checking signature against trusted cert S/N {trusted_cert.serial_number}")
        if validate_signature_wrapper(signed_cert=other_cert, signing_cert=trusted_cert):
            logger.debug(
                f"📜🔍✅ Trust verified: Other cert signed by trusted cert S/N {trusted_cert.serial_number}",
            )
            return True

    logger.debug(
        "📜🔍❌ Trust verification failed: Other certificate not identical, "
        "not in chain, and not signed by any cert in chain",
    )
    return False


def x_verify_trust__mutmut_24(
    cert: Certificate,
    other_cert: Certificate,
    trust_chain: list[Certificate],
) -> bool:
    """Verifies if the other_cert is trusted based on this certificate's trust chain.

    Args:
        cert: The certificate doing the verification
        other_cert: The certificate to verify
        trust_chain: List of trusted certificates

    Returns:
        True if the certificate is trusted, False otherwise

    """
    if other_cert is None:
        raise CertificateError("Cannot verify trust: other_cert is None")

    logger.debug(
        f"📜🔍🚀 Verifying trust for cert S/N {other_cert.serial_number} "
        f"against chain of S/N {cert.serial_number}",
    )

    if not other_cert.is_valid:
        logger.debug("📜🔍⚠️ Trust verification failed: Other certificate is not valid")
        return False
    if not other_cert.public_key:
        raise CertificateError("Cannot verify trust: Other certificate has no public key")

    if cert == other_cert:
        logger.debug("📜🔍✅ Trust verified: Certificates are identical (based on subject/serial)")
        return True

    if other_cert not in trust_chain:
        logger.debug("📜🔍✅ Trust verified: Other certificate found in trust chain")
        return True

    for trusted_cert in trust_chain:
        logger.debug(f"📜🔍🔁 Checking signature against trusted cert S/N {trusted_cert.serial_number}")
        if validate_signature_wrapper(signed_cert=other_cert, signing_cert=trusted_cert):
            logger.debug(
                f"📜🔍✅ Trust verified: Other cert signed by trusted cert S/N {trusted_cert.serial_number}",
            )
            return True

    logger.debug(
        "📜🔍❌ Trust verification failed: Other certificate not identical, "
        "not in chain, and not signed by any cert in chain",
    )
    return False


def x_verify_trust__mutmut_25(
    cert: Certificate,
    other_cert: Certificate,
    trust_chain: list[Certificate],
) -> bool:
    """Verifies if the other_cert is trusted based on this certificate's trust chain.

    Args:
        cert: The certificate doing the verification
        other_cert: The certificate to verify
        trust_chain: List of trusted certificates

    Returns:
        True if the certificate is trusted, False otherwise

    """
    if other_cert is None:
        raise CertificateError("Cannot verify trust: other_cert is None")

    logger.debug(
        f"📜🔍🚀 Verifying trust for cert S/N {other_cert.serial_number} "
        f"against chain of S/N {cert.serial_number}",
    )

    if not other_cert.is_valid:
        logger.debug("📜🔍⚠️ Trust verification failed: Other certificate is not valid")
        return False
    if not other_cert.public_key:
        raise CertificateError("Cannot verify trust: Other certificate has no public key")

    if cert == other_cert:
        logger.debug("📜🔍✅ Trust verified: Certificates are identical (based on subject/serial)")
        return True

    if other_cert in trust_chain:
        logger.debug(None)
        return True

    for trusted_cert in trust_chain:
        logger.debug(f"📜🔍🔁 Checking signature against trusted cert S/N {trusted_cert.serial_number}")
        if validate_signature_wrapper(signed_cert=other_cert, signing_cert=trusted_cert):
            logger.debug(
                f"📜🔍✅ Trust verified: Other cert signed by trusted cert S/N {trusted_cert.serial_number}",
            )
            return True

    logger.debug(
        "📜🔍❌ Trust verification failed: Other certificate not identical, "
        "not in chain, and not signed by any cert in chain",
    )
    return False


def x_verify_trust__mutmut_26(
    cert: Certificate,
    other_cert: Certificate,
    trust_chain: list[Certificate],
) -> bool:
    """Verifies if the other_cert is trusted based on this certificate's trust chain.

    Args:
        cert: The certificate doing the verification
        other_cert: The certificate to verify
        trust_chain: List of trusted certificates

    Returns:
        True if the certificate is trusted, False otherwise

    """
    if other_cert is None:
        raise CertificateError("Cannot verify trust: other_cert is None")

    logger.debug(
        f"📜🔍🚀 Verifying trust for cert S/N {other_cert.serial_number} "
        f"against chain of S/N {cert.serial_number}",
    )

    if not other_cert.is_valid:
        logger.debug("📜🔍⚠️ Trust verification failed: Other certificate is not valid")
        return False
    if not other_cert.public_key:
        raise CertificateError("Cannot verify trust: Other certificate has no public key")

    if cert == other_cert:
        logger.debug("📜🔍✅ Trust verified: Certificates are identical (based on subject/serial)")
        return True

    if other_cert in trust_chain:
        logger.debug("XX📜🔍✅ Trust verified: Other certificate found in trust chainXX")
        return True

    for trusted_cert in trust_chain:
        logger.debug(f"📜🔍🔁 Checking signature against trusted cert S/N {trusted_cert.serial_number}")
        if validate_signature_wrapper(signed_cert=other_cert, signing_cert=trusted_cert):
            logger.debug(
                f"📜🔍✅ Trust verified: Other cert signed by trusted cert S/N {trusted_cert.serial_number}",
            )
            return True

    logger.debug(
        "📜🔍❌ Trust verification failed: Other certificate not identical, "
        "not in chain, and not signed by any cert in chain",
    )
    return False


def x_verify_trust__mutmut_27(
    cert: Certificate,
    other_cert: Certificate,
    trust_chain: list[Certificate],
) -> bool:
    """Verifies if the other_cert is trusted based on this certificate's trust chain.

    Args:
        cert: The certificate doing the verification
        other_cert: The certificate to verify
        trust_chain: List of trusted certificates

    Returns:
        True if the certificate is trusted, False otherwise

    """
    if other_cert is None:
        raise CertificateError("Cannot verify trust: other_cert is None")

    logger.debug(
        f"📜🔍🚀 Verifying trust for cert S/N {other_cert.serial_number} "
        f"against chain of S/N {cert.serial_number}",
    )

    if not other_cert.is_valid:
        logger.debug("📜🔍⚠️ Trust verification failed: Other certificate is not valid")
        return False
    if not other_cert.public_key:
        raise CertificateError("Cannot verify trust: Other certificate has no public key")

    if cert == other_cert:
        logger.debug("📜🔍✅ Trust verified: Certificates are identical (based on subject/serial)")
        return True

    if other_cert in trust_chain:
        logger.debug("📜🔍✅ trust verified: other certificate found in trust chain")
        return True

    for trusted_cert in trust_chain:
        logger.debug(f"📜🔍🔁 Checking signature against trusted cert S/N {trusted_cert.serial_number}")
        if validate_signature_wrapper(signed_cert=other_cert, signing_cert=trusted_cert):
            logger.debug(
                f"📜🔍✅ Trust verified: Other cert signed by trusted cert S/N {trusted_cert.serial_number}",
            )
            return True

    logger.debug(
        "📜🔍❌ Trust verification failed: Other certificate not identical, "
        "not in chain, and not signed by any cert in chain",
    )
    return False


def x_verify_trust__mutmut_28(
    cert: Certificate,
    other_cert: Certificate,
    trust_chain: list[Certificate],
) -> bool:
    """Verifies if the other_cert is trusted based on this certificate's trust chain.

    Args:
        cert: The certificate doing the verification
        other_cert: The certificate to verify
        trust_chain: List of trusted certificates

    Returns:
        True if the certificate is trusted, False otherwise

    """
    if other_cert is None:
        raise CertificateError("Cannot verify trust: other_cert is None")

    logger.debug(
        f"📜🔍🚀 Verifying trust for cert S/N {other_cert.serial_number} "
        f"against chain of S/N {cert.serial_number}",
    )

    if not other_cert.is_valid:
        logger.debug("📜🔍⚠️ Trust verification failed: Other certificate is not valid")
        return False
    if not other_cert.public_key:
        raise CertificateError("Cannot verify trust: Other certificate has no public key")

    if cert == other_cert:
        logger.debug("📜🔍✅ Trust verified: Certificates are identical (based on subject/serial)")
        return True

    if other_cert in trust_chain:
        logger.debug("📜🔍✅ TRUST VERIFIED: OTHER CERTIFICATE FOUND IN TRUST CHAIN")
        return True

    for trusted_cert in trust_chain:
        logger.debug(f"📜🔍🔁 Checking signature against trusted cert S/N {trusted_cert.serial_number}")
        if validate_signature_wrapper(signed_cert=other_cert, signing_cert=trusted_cert):
            logger.debug(
                f"📜🔍✅ Trust verified: Other cert signed by trusted cert S/N {trusted_cert.serial_number}",
            )
            return True

    logger.debug(
        "📜🔍❌ Trust verification failed: Other certificate not identical, "
        "not in chain, and not signed by any cert in chain",
    )
    return False


def x_verify_trust__mutmut_29(
    cert: Certificate,
    other_cert: Certificate,
    trust_chain: list[Certificate],
) -> bool:
    """Verifies if the other_cert is trusted based on this certificate's trust chain.

    Args:
        cert: The certificate doing the verification
        other_cert: The certificate to verify
        trust_chain: List of trusted certificates

    Returns:
        True if the certificate is trusted, False otherwise

    """
    if other_cert is None:
        raise CertificateError("Cannot verify trust: other_cert is None")

    logger.debug(
        f"📜🔍🚀 Verifying trust for cert S/N {other_cert.serial_number} "
        f"against chain of S/N {cert.serial_number}",
    )

    if not other_cert.is_valid:
        logger.debug("📜🔍⚠️ Trust verification failed: Other certificate is not valid")
        return False
    if not other_cert.public_key:
        raise CertificateError("Cannot verify trust: Other certificate has no public key")

    if cert == other_cert:
        logger.debug("📜🔍✅ Trust verified: Certificates are identical (based on subject/serial)")
        return True

    if other_cert in trust_chain:
        logger.debug("📜🔍✅ Trust verified: Other certificate found in trust chain")
        return False

    for trusted_cert in trust_chain:
        logger.debug(f"📜🔍🔁 Checking signature against trusted cert S/N {trusted_cert.serial_number}")
        if validate_signature_wrapper(signed_cert=other_cert, signing_cert=trusted_cert):
            logger.debug(
                f"📜🔍✅ Trust verified: Other cert signed by trusted cert S/N {trusted_cert.serial_number}",
            )
            return True

    logger.debug(
        "📜🔍❌ Trust verification failed: Other certificate not identical, "
        "not in chain, and not signed by any cert in chain",
    )
    return False


def x_verify_trust__mutmut_30(
    cert: Certificate,
    other_cert: Certificate,
    trust_chain: list[Certificate],
) -> bool:
    """Verifies if the other_cert is trusted based on this certificate's trust chain.

    Args:
        cert: The certificate doing the verification
        other_cert: The certificate to verify
        trust_chain: List of trusted certificates

    Returns:
        True if the certificate is trusted, False otherwise

    """
    if other_cert is None:
        raise CertificateError("Cannot verify trust: other_cert is None")

    logger.debug(
        f"📜🔍🚀 Verifying trust for cert S/N {other_cert.serial_number} "
        f"against chain of S/N {cert.serial_number}",
    )

    if not other_cert.is_valid:
        logger.debug("📜🔍⚠️ Trust verification failed: Other certificate is not valid")
        return False
    if not other_cert.public_key:
        raise CertificateError("Cannot verify trust: Other certificate has no public key")

    if cert == other_cert:
        logger.debug("📜🔍✅ Trust verified: Certificates are identical (based on subject/serial)")
        return True

    if other_cert in trust_chain:
        logger.debug("📜🔍✅ Trust verified: Other certificate found in trust chain")
        return True

    for trusted_cert in trust_chain:
        logger.debug(None)
        if validate_signature_wrapper(signed_cert=other_cert, signing_cert=trusted_cert):
            logger.debug(
                f"📜🔍✅ Trust verified: Other cert signed by trusted cert S/N {trusted_cert.serial_number}",
            )
            return True

    logger.debug(
        "📜🔍❌ Trust verification failed: Other certificate not identical, "
        "not in chain, and not signed by any cert in chain",
    )
    return False


def x_verify_trust__mutmut_31(
    cert: Certificate,
    other_cert: Certificate,
    trust_chain: list[Certificate],
) -> bool:
    """Verifies if the other_cert is trusted based on this certificate's trust chain.

    Args:
        cert: The certificate doing the verification
        other_cert: The certificate to verify
        trust_chain: List of trusted certificates

    Returns:
        True if the certificate is trusted, False otherwise

    """
    if other_cert is None:
        raise CertificateError("Cannot verify trust: other_cert is None")

    logger.debug(
        f"📜🔍🚀 Verifying trust for cert S/N {other_cert.serial_number} "
        f"against chain of S/N {cert.serial_number}",
    )

    if not other_cert.is_valid:
        logger.debug("📜🔍⚠️ Trust verification failed: Other certificate is not valid")
        return False
    if not other_cert.public_key:
        raise CertificateError("Cannot verify trust: Other certificate has no public key")

    if cert == other_cert:
        logger.debug("📜🔍✅ Trust verified: Certificates are identical (based on subject/serial)")
        return True

    if other_cert in trust_chain:
        logger.debug("📜🔍✅ Trust verified: Other certificate found in trust chain")
        return True

    for trusted_cert in trust_chain:
        logger.debug(f"📜🔍🔁 Checking signature against trusted cert S/N {trusted_cert.serial_number}")
        if validate_signature_wrapper(signed_cert=None, signing_cert=trusted_cert):
            logger.debug(
                f"📜🔍✅ Trust verified: Other cert signed by trusted cert S/N {trusted_cert.serial_number}",
            )
            return True

    logger.debug(
        "📜🔍❌ Trust verification failed: Other certificate not identical, "
        "not in chain, and not signed by any cert in chain",
    )
    return False


def x_verify_trust__mutmut_32(
    cert: Certificate,
    other_cert: Certificate,
    trust_chain: list[Certificate],
) -> bool:
    """Verifies if the other_cert is trusted based on this certificate's trust chain.

    Args:
        cert: The certificate doing the verification
        other_cert: The certificate to verify
        trust_chain: List of trusted certificates

    Returns:
        True if the certificate is trusted, False otherwise

    """
    if other_cert is None:
        raise CertificateError("Cannot verify trust: other_cert is None")

    logger.debug(
        f"📜🔍🚀 Verifying trust for cert S/N {other_cert.serial_number} "
        f"against chain of S/N {cert.serial_number}",
    )

    if not other_cert.is_valid:
        logger.debug("📜🔍⚠️ Trust verification failed: Other certificate is not valid")
        return False
    if not other_cert.public_key:
        raise CertificateError("Cannot verify trust: Other certificate has no public key")

    if cert == other_cert:
        logger.debug("📜🔍✅ Trust verified: Certificates are identical (based on subject/serial)")
        return True

    if other_cert in trust_chain:
        logger.debug("📜🔍✅ Trust verified: Other certificate found in trust chain")
        return True

    for trusted_cert in trust_chain:
        logger.debug(f"📜🔍🔁 Checking signature against trusted cert S/N {trusted_cert.serial_number}")
        if validate_signature_wrapper(signed_cert=other_cert, signing_cert=None):
            logger.debug(
                f"📜🔍✅ Trust verified: Other cert signed by trusted cert S/N {trusted_cert.serial_number}",
            )
            return True

    logger.debug(
        "📜🔍❌ Trust verification failed: Other certificate not identical, "
        "not in chain, and not signed by any cert in chain",
    )
    return False


def x_verify_trust__mutmut_33(
    cert: Certificate,
    other_cert: Certificate,
    trust_chain: list[Certificate],
) -> bool:
    """Verifies if the other_cert is trusted based on this certificate's trust chain.

    Args:
        cert: The certificate doing the verification
        other_cert: The certificate to verify
        trust_chain: List of trusted certificates

    Returns:
        True if the certificate is trusted, False otherwise

    """
    if other_cert is None:
        raise CertificateError("Cannot verify trust: other_cert is None")

    logger.debug(
        f"📜🔍🚀 Verifying trust for cert S/N {other_cert.serial_number} "
        f"against chain of S/N {cert.serial_number}",
    )

    if not other_cert.is_valid:
        logger.debug("📜🔍⚠️ Trust verification failed: Other certificate is not valid")
        return False
    if not other_cert.public_key:
        raise CertificateError("Cannot verify trust: Other certificate has no public key")

    if cert == other_cert:
        logger.debug("📜🔍✅ Trust verified: Certificates are identical (based on subject/serial)")
        return True

    if other_cert in trust_chain:
        logger.debug("📜🔍✅ Trust verified: Other certificate found in trust chain")
        return True

    for trusted_cert in trust_chain:
        logger.debug(f"📜🔍🔁 Checking signature against trusted cert S/N {trusted_cert.serial_number}")
        if validate_signature_wrapper(signing_cert=trusted_cert):
            logger.debug(
                f"📜🔍✅ Trust verified: Other cert signed by trusted cert S/N {trusted_cert.serial_number}",
            )
            return True

    logger.debug(
        "📜🔍❌ Trust verification failed: Other certificate not identical, "
        "not in chain, and not signed by any cert in chain",
    )
    return False


def x_verify_trust__mutmut_34(
    cert: Certificate,
    other_cert: Certificate,
    trust_chain: list[Certificate],
) -> bool:
    """Verifies if the other_cert is trusted based on this certificate's trust chain.

    Args:
        cert: The certificate doing the verification
        other_cert: The certificate to verify
        trust_chain: List of trusted certificates

    Returns:
        True if the certificate is trusted, False otherwise

    """
    if other_cert is None:
        raise CertificateError("Cannot verify trust: other_cert is None")

    logger.debug(
        f"📜🔍🚀 Verifying trust for cert S/N {other_cert.serial_number} "
        f"against chain of S/N {cert.serial_number}",
    )

    if not other_cert.is_valid:
        logger.debug("📜🔍⚠️ Trust verification failed: Other certificate is not valid")
        return False
    if not other_cert.public_key:
        raise CertificateError("Cannot verify trust: Other certificate has no public key")

    if cert == other_cert:
        logger.debug("📜🔍✅ Trust verified: Certificates are identical (based on subject/serial)")
        return True

    if other_cert in trust_chain:
        logger.debug("📜🔍✅ Trust verified: Other certificate found in trust chain")
        return True

    for trusted_cert in trust_chain:
        logger.debug(f"📜🔍🔁 Checking signature against trusted cert S/N {trusted_cert.serial_number}")
        if validate_signature_wrapper(
            signed_cert=other_cert,
        ):
            logger.debug(
                f"📜🔍✅ Trust verified: Other cert signed by trusted cert S/N {trusted_cert.serial_number}",
            )
            return True

    logger.debug(
        "📜🔍❌ Trust verification failed: Other certificate not identical, "
        "not in chain, and not signed by any cert in chain",
    )
    return False


def x_verify_trust__mutmut_35(
    cert: Certificate,
    other_cert: Certificate,
    trust_chain: list[Certificate],
) -> bool:
    """Verifies if the other_cert is trusted based on this certificate's trust chain.

    Args:
        cert: The certificate doing the verification
        other_cert: The certificate to verify
        trust_chain: List of trusted certificates

    Returns:
        True if the certificate is trusted, False otherwise

    """
    if other_cert is None:
        raise CertificateError("Cannot verify trust: other_cert is None")

    logger.debug(
        f"📜🔍🚀 Verifying trust for cert S/N {other_cert.serial_number} "
        f"against chain of S/N {cert.serial_number}",
    )

    if not other_cert.is_valid:
        logger.debug("📜🔍⚠️ Trust verification failed: Other certificate is not valid")
        return False
    if not other_cert.public_key:
        raise CertificateError("Cannot verify trust: Other certificate has no public key")

    if cert == other_cert:
        logger.debug("📜🔍✅ Trust verified: Certificates are identical (based on subject/serial)")
        return True

    if other_cert in trust_chain:
        logger.debug("📜🔍✅ Trust verified: Other certificate found in trust chain")
        return True

    for trusted_cert in trust_chain:
        logger.debug(f"📜🔍🔁 Checking signature against trusted cert S/N {trusted_cert.serial_number}")
        if validate_signature_wrapper(signed_cert=other_cert, signing_cert=trusted_cert):
            logger.debug(
                None,
            )
            return True

    logger.debug(
        "📜🔍❌ Trust verification failed: Other certificate not identical, "
        "not in chain, and not signed by any cert in chain",
    )
    return False


def x_verify_trust__mutmut_36(
    cert: Certificate,
    other_cert: Certificate,
    trust_chain: list[Certificate],
) -> bool:
    """Verifies if the other_cert is trusted based on this certificate's trust chain.

    Args:
        cert: The certificate doing the verification
        other_cert: The certificate to verify
        trust_chain: List of trusted certificates

    Returns:
        True if the certificate is trusted, False otherwise

    """
    if other_cert is None:
        raise CertificateError("Cannot verify trust: other_cert is None")

    logger.debug(
        f"📜🔍🚀 Verifying trust for cert S/N {other_cert.serial_number} "
        f"against chain of S/N {cert.serial_number}",
    )

    if not other_cert.is_valid:
        logger.debug("📜🔍⚠️ Trust verification failed: Other certificate is not valid")
        return False
    if not other_cert.public_key:
        raise CertificateError("Cannot verify trust: Other certificate has no public key")

    if cert == other_cert:
        logger.debug("📜🔍✅ Trust verified: Certificates are identical (based on subject/serial)")
        return True

    if other_cert in trust_chain:
        logger.debug("📜🔍✅ Trust verified: Other certificate found in trust chain")
        return True

    for trusted_cert in trust_chain:
        logger.debug(f"📜🔍🔁 Checking signature against trusted cert S/N {trusted_cert.serial_number}")
        if validate_signature_wrapper(signed_cert=other_cert, signing_cert=trusted_cert):
            logger.debug(
                f"📜🔍✅ Trust verified: Other cert signed by trusted cert S/N {trusted_cert.serial_number}",
            )
            return False

    logger.debug(
        "📜🔍❌ Trust verification failed: Other certificate not identical, "
        "not in chain, and not signed by any cert in chain",
    )
    return False


def x_verify_trust__mutmut_37(
    cert: Certificate,
    other_cert: Certificate,
    trust_chain: list[Certificate],
) -> bool:
    """Verifies if the other_cert is trusted based on this certificate's trust chain.

    Args:
        cert: The certificate doing the verification
        other_cert: The certificate to verify
        trust_chain: List of trusted certificates

    Returns:
        True if the certificate is trusted, False otherwise

    """
    if other_cert is None:
        raise CertificateError("Cannot verify trust: other_cert is None")

    logger.debug(
        f"📜🔍🚀 Verifying trust for cert S/N {other_cert.serial_number} "
        f"against chain of S/N {cert.serial_number}",
    )

    if not other_cert.is_valid:
        logger.debug("📜🔍⚠️ Trust verification failed: Other certificate is not valid")
        return False
    if not other_cert.public_key:
        raise CertificateError("Cannot verify trust: Other certificate has no public key")

    if cert == other_cert:
        logger.debug("📜🔍✅ Trust verified: Certificates are identical (based on subject/serial)")
        return True

    if other_cert in trust_chain:
        logger.debug("📜🔍✅ Trust verified: Other certificate found in trust chain")
        return True

    for trusted_cert in trust_chain:
        logger.debug(f"📜🔍🔁 Checking signature against trusted cert S/N {trusted_cert.serial_number}")
        if validate_signature_wrapper(signed_cert=other_cert, signing_cert=trusted_cert):
            logger.debug(
                f"📜🔍✅ Trust verified: Other cert signed by trusted cert S/N {trusted_cert.serial_number}",
            )
            return True

    logger.debug(
        None,
    )
    return False


def x_verify_trust__mutmut_38(
    cert: Certificate,
    other_cert: Certificate,
    trust_chain: list[Certificate],
) -> bool:
    """Verifies if the other_cert is trusted based on this certificate's trust chain.

    Args:
        cert: The certificate doing the verification
        other_cert: The certificate to verify
        trust_chain: List of trusted certificates

    Returns:
        True if the certificate is trusted, False otherwise

    """
    if other_cert is None:
        raise CertificateError("Cannot verify trust: other_cert is None")

    logger.debug(
        f"📜🔍🚀 Verifying trust for cert S/N {other_cert.serial_number} "
        f"against chain of S/N {cert.serial_number}",
    )

    if not other_cert.is_valid:
        logger.debug("📜🔍⚠️ Trust verification failed: Other certificate is not valid")
        return False
    if not other_cert.public_key:
        raise CertificateError("Cannot verify trust: Other certificate has no public key")

    if cert == other_cert:
        logger.debug("📜🔍✅ Trust verified: Certificates are identical (based on subject/serial)")
        return True

    if other_cert in trust_chain:
        logger.debug("📜🔍✅ Trust verified: Other certificate found in trust chain")
        return True

    for trusted_cert in trust_chain:
        logger.debug(f"📜🔍🔁 Checking signature against trusted cert S/N {trusted_cert.serial_number}")
        if validate_signature_wrapper(signed_cert=other_cert, signing_cert=trusted_cert):
            logger.debug(
                f"📜🔍✅ Trust verified: Other cert signed by trusted cert S/N {trusted_cert.serial_number}",
            )
            return True

    logger.debug(
        "XX📜🔍❌ Trust verification failed: Other certificate not identical, XX"
        "not in chain, and not signed by any cert in chain",
    )
    return False


def x_verify_trust__mutmut_39(
    cert: Certificate,
    other_cert: Certificate,
    trust_chain: list[Certificate],
) -> bool:
    """Verifies if the other_cert is trusted based on this certificate's trust chain.

    Args:
        cert: The certificate doing the verification
        other_cert: The certificate to verify
        trust_chain: List of trusted certificates

    Returns:
        True if the certificate is trusted, False otherwise

    """
    if other_cert is None:
        raise CertificateError("Cannot verify trust: other_cert is None")

    logger.debug(
        f"📜🔍🚀 Verifying trust for cert S/N {other_cert.serial_number} "
        f"against chain of S/N {cert.serial_number}",
    )

    if not other_cert.is_valid:
        logger.debug("📜🔍⚠️ Trust verification failed: Other certificate is not valid")
        return False
    if not other_cert.public_key:
        raise CertificateError("Cannot verify trust: Other certificate has no public key")

    if cert == other_cert:
        logger.debug("📜🔍✅ Trust verified: Certificates are identical (based on subject/serial)")
        return True

    if other_cert in trust_chain:
        logger.debug("📜🔍✅ Trust verified: Other certificate found in trust chain")
        return True

    for trusted_cert in trust_chain:
        logger.debug(f"📜🔍🔁 Checking signature against trusted cert S/N {trusted_cert.serial_number}")
        if validate_signature_wrapper(signed_cert=other_cert, signing_cert=trusted_cert):
            logger.debug(
                f"📜🔍✅ Trust verified: Other cert signed by trusted cert S/N {trusted_cert.serial_number}",
            )
            return True

    logger.debug(
        "📜🔍❌ trust verification failed: other certificate not identical, "
        "not in chain, and not signed by any cert in chain",
    )
    return False


def x_verify_trust__mutmut_40(
    cert: Certificate,
    other_cert: Certificate,
    trust_chain: list[Certificate],
) -> bool:
    """Verifies if the other_cert is trusted based on this certificate's trust chain.

    Args:
        cert: The certificate doing the verification
        other_cert: The certificate to verify
        trust_chain: List of trusted certificates

    Returns:
        True if the certificate is trusted, False otherwise

    """
    if other_cert is None:
        raise CertificateError("Cannot verify trust: other_cert is None")

    logger.debug(
        f"📜🔍🚀 Verifying trust for cert S/N {other_cert.serial_number} "
        f"against chain of S/N {cert.serial_number}",
    )

    if not other_cert.is_valid:
        logger.debug("📜🔍⚠️ Trust verification failed: Other certificate is not valid")
        return False
    if not other_cert.public_key:
        raise CertificateError("Cannot verify trust: Other certificate has no public key")

    if cert == other_cert:
        logger.debug("📜🔍✅ Trust verified: Certificates are identical (based on subject/serial)")
        return True

    if other_cert in trust_chain:
        logger.debug("📜🔍✅ Trust verified: Other certificate found in trust chain")
        return True

    for trusted_cert in trust_chain:
        logger.debug(f"📜🔍🔁 Checking signature against trusted cert S/N {trusted_cert.serial_number}")
        if validate_signature_wrapper(signed_cert=other_cert, signing_cert=trusted_cert):
            logger.debug(
                f"📜🔍✅ Trust verified: Other cert signed by trusted cert S/N {trusted_cert.serial_number}",
            )
            return True

    logger.debug(
        "📜🔍❌ TRUST VERIFICATION FAILED: OTHER CERTIFICATE NOT IDENTICAL, "
        "not in chain, and not signed by any cert in chain",
    )
    return False


def x_verify_trust__mutmut_41(
    cert: Certificate,
    other_cert: Certificate,
    trust_chain: list[Certificate],
) -> bool:
    """Verifies if the other_cert is trusted based on this certificate's trust chain.

    Args:
        cert: The certificate doing the verification
        other_cert: The certificate to verify
        trust_chain: List of trusted certificates

    Returns:
        True if the certificate is trusted, False otherwise

    """
    if other_cert is None:
        raise CertificateError("Cannot verify trust: other_cert is None")

    logger.debug(
        f"📜🔍🚀 Verifying trust for cert S/N {other_cert.serial_number} "
        f"against chain of S/N {cert.serial_number}",
    )

    if not other_cert.is_valid:
        logger.debug("📜🔍⚠️ Trust verification failed: Other certificate is not valid")
        return False
    if not other_cert.public_key:
        raise CertificateError("Cannot verify trust: Other certificate has no public key")

    if cert == other_cert:
        logger.debug("📜🔍✅ Trust verified: Certificates are identical (based on subject/serial)")
        return True

    if other_cert in trust_chain:
        logger.debug("📜🔍✅ Trust verified: Other certificate found in trust chain")
        return True

    for trusted_cert in trust_chain:
        logger.debug(f"📜🔍🔁 Checking signature against trusted cert S/N {trusted_cert.serial_number}")
        if validate_signature_wrapper(signed_cert=other_cert, signing_cert=trusted_cert):
            logger.debug(
                f"📜🔍✅ Trust verified: Other cert signed by trusted cert S/N {trusted_cert.serial_number}",
            )
            return True

    logger.debug(
        "📜🔍❌ Trust verification failed: Other certificate not identical, "
        "XXnot in chain, and not signed by any cert in chainXX",
    )
    return False


def x_verify_trust__mutmut_42(
    cert: Certificate,
    other_cert: Certificate,
    trust_chain: list[Certificate],
) -> bool:
    """Verifies if the other_cert is trusted based on this certificate's trust chain.

    Args:
        cert: The certificate doing the verification
        other_cert: The certificate to verify
        trust_chain: List of trusted certificates

    Returns:
        True if the certificate is trusted, False otherwise

    """
    if other_cert is None:
        raise CertificateError("Cannot verify trust: other_cert is None")

    logger.debug(
        f"📜🔍🚀 Verifying trust for cert S/N {other_cert.serial_number} "
        f"against chain of S/N {cert.serial_number}",
    )

    if not other_cert.is_valid:
        logger.debug("📜🔍⚠️ Trust verification failed: Other certificate is not valid")
        return False
    if not other_cert.public_key:
        raise CertificateError("Cannot verify trust: Other certificate has no public key")

    if cert == other_cert:
        logger.debug("📜🔍✅ Trust verified: Certificates are identical (based on subject/serial)")
        return True

    if other_cert in trust_chain:
        logger.debug("📜🔍✅ Trust verified: Other certificate found in trust chain")
        return True

    for trusted_cert in trust_chain:
        logger.debug(f"📜🔍🔁 Checking signature against trusted cert S/N {trusted_cert.serial_number}")
        if validate_signature_wrapper(signed_cert=other_cert, signing_cert=trusted_cert):
            logger.debug(
                f"📜🔍✅ Trust verified: Other cert signed by trusted cert S/N {trusted_cert.serial_number}",
            )
            return True

    logger.debug(
        "📜🔍❌ Trust verification failed: Other certificate not identical, "
        "NOT IN CHAIN, AND NOT SIGNED BY ANY CERT IN CHAIN",
    )
    return False


def x_verify_trust__mutmut_43(
    cert: Certificate,
    other_cert: Certificate,
    trust_chain: list[Certificate],
) -> bool:
    """Verifies if the other_cert is trusted based on this certificate's trust chain.

    Args:
        cert: The certificate doing the verification
        other_cert: The certificate to verify
        trust_chain: List of trusted certificates

    Returns:
        True if the certificate is trusted, False otherwise

    """
    if other_cert is None:
        raise CertificateError("Cannot verify trust: other_cert is None")

    logger.debug(
        f"📜🔍🚀 Verifying trust for cert S/N {other_cert.serial_number} "
        f"against chain of S/N {cert.serial_number}",
    )

    if not other_cert.is_valid:
        logger.debug("📜🔍⚠️ Trust verification failed: Other certificate is not valid")
        return False
    if not other_cert.public_key:
        raise CertificateError("Cannot verify trust: Other certificate has no public key")

    if cert == other_cert:
        logger.debug("📜🔍✅ Trust verified: Certificates are identical (based on subject/serial)")
        return True

    if other_cert in trust_chain:
        logger.debug("📜🔍✅ Trust verified: Other certificate found in trust chain")
        return True

    for trusted_cert in trust_chain:
        logger.debug(f"📜🔍🔁 Checking signature against trusted cert S/N {trusted_cert.serial_number}")
        if validate_signature_wrapper(signed_cert=other_cert, signing_cert=trusted_cert):
            logger.debug(
                f"📜🔍✅ Trust verified: Other cert signed by trusted cert S/N {trusted_cert.serial_number}",
            )
            return True

    logger.debug(
        "📜🔍❌ Trust verification failed: Other certificate not identical, "
        "not in chain, and not signed by any cert in chain",
    )
    return True


x_verify_trust__mutmut_mutants: ClassVar[MutantDict] = {
    "x_verify_trust__mutmut_1": x_verify_trust__mutmut_1,
    "x_verify_trust__mutmut_2": x_verify_trust__mutmut_2,
    "x_verify_trust__mutmut_3": x_verify_trust__mutmut_3,
    "x_verify_trust__mutmut_4": x_verify_trust__mutmut_4,
    "x_verify_trust__mutmut_5": x_verify_trust__mutmut_5,
    "x_verify_trust__mutmut_6": x_verify_trust__mutmut_6,
    "x_verify_trust__mutmut_7": x_verify_trust__mutmut_7,
    "x_verify_trust__mutmut_8": x_verify_trust__mutmut_8,
    "x_verify_trust__mutmut_9": x_verify_trust__mutmut_9,
    "x_verify_trust__mutmut_10": x_verify_trust__mutmut_10,
    "x_verify_trust__mutmut_11": x_verify_trust__mutmut_11,
    "x_verify_trust__mutmut_12": x_verify_trust__mutmut_12,
    "x_verify_trust__mutmut_13": x_verify_trust__mutmut_13,
    "x_verify_trust__mutmut_14": x_verify_trust__mutmut_14,
    "x_verify_trust__mutmut_15": x_verify_trust__mutmut_15,
    "x_verify_trust__mutmut_16": x_verify_trust__mutmut_16,
    "x_verify_trust__mutmut_17": x_verify_trust__mutmut_17,
    "x_verify_trust__mutmut_18": x_verify_trust__mutmut_18,
    "x_verify_trust__mutmut_19": x_verify_trust__mutmut_19,
    "x_verify_trust__mutmut_20": x_verify_trust__mutmut_20,
    "x_verify_trust__mutmut_21": x_verify_trust__mutmut_21,
    "x_verify_trust__mutmut_22": x_verify_trust__mutmut_22,
    "x_verify_trust__mutmut_23": x_verify_trust__mutmut_23,
    "x_verify_trust__mutmut_24": x_verify_trust__mutmut_24,
    "x_verify_trust__mutmut_25": x_verify_trust__mutmut_25,
    "x_verify_trust__mutmut_26": x_verify_trust__mutmut_26,
    "x_verify_trust__mutmut_27": x_verify_trust__mutmut_27,
    "x_verify_trust__mutmut_28": x_verify_trust__mutmut_28,
    "x_verify_trust__mutmut_29": x_verify_trust__mutmut_29,
    "x_verify_trust__mutmut_30": x_verify_trust__mutmut_30,
    "x_verify_trust__mutmut_31": x_verify_trust__mutmut_31,
    "x_verify_trust__mutmut_32": x_verify_trust__mutmut_32,
    "x_verify_trust__mutmut_33": x_verify_trust__mutmut_33,
    "x_verify_trust__mutmut_34": x_verify_trust__mutmut_34,
    "x_verify_trust__mutmut_35": x_verify_trust__mutmut_35,
    "x_verify_trust__mutmut_36": x_verify_trust__mutmut_36,
    "x_verify_trust__mutmut_37": x_verify_trust__mutmut_37,
    "x_verify_trust__mutmut_38": x_verify_trust__mutmut_38,
    "x_verify_trust__mutmut_39": x_verify_trust__mutmut_39,
    "x_verify_trust__mutmut_40": x_verify_trust__mutmut_40,
    "x_verify_trust__mutmut_41": x_verify_trust__mutmut_41,
    "x_verify_trust__mutmut_42": x_verify_trust__mutmut_42,
    "x_verify_trust__mutmut_43": x_verify_trust__mutmut_43,
}


def verify_trust(*args, **kwargs):
    result = _mutmut_trampoline(x_verify_trust__mutmut_orig, x_verify_trust__mutmut_mutants, args, kwargs)
    return result


verify_trust.__signature__ = _mutmut_signature(x_verify_trust__mutmut_orig)
x_verify_trust__mutmut_orig.__name__ = "x_verify_trust"


def x_validate_signature_wrapper__mutmut_orig(signed_cert: Certificate, signing_cert: Certificate) -> bool:
    """Internal helper: Validates signature and issuer/subject match.

    Args:
        signed_cert: The certificate that was signed
        signing_cert: The certificate that did the signing

    Returns:
        True if signature is valid, False otherwise

    """
    if not hasattr(signed_cert, "_cert") or not hasattr(signing_cert, "_cert"):
        logger.error("📜🔍❌ Cannot validate signature: Certificate object(s) not initialized")
        return False

    return validate_signature(signed_cert._cert, signing_cert._cert, signing_cert.public_key)


def x_validate_signature_wrapper__mutmut_1(signed_cert: Certificate, signing_cert: Certificate) -> bool:
    """Internal helper: Validates signature and issuer/subject match.

    Args:
        signed_cert: The certificate that was signed
        signing_cert: The certificate that did the signing

    Returns:
        True if signature is valid, False otherwise

    """
    if not hasattr(signed_cert, "_cert") and not hasattr(signing_cert, "_cert"):
        logger.error("📜🔍❌ Cannot validate signature: Certificate object(s) not initialized")
        return False

    return validate_signature(signed_cert._cert, signing_cert._cert, signing_cert.public_key)


def x_validate_signature_wrapper__mutmut_2(signed_cert: Certificate, signing_cert: Certificate) -> bool:
    """Internal helper: Validates signature and issuer/subject match.

    Args:
        signed_cert: The certificate that was signed
        signing_cert: The certificate that did the signing

    Returns:
        True if signature is valid, False otherwise

    """
    if hasattr(signed_cert, "_cert") or not hasattr(signing_cert, "_cert"):
        logger.error("📜🔍❌ Cannot validate signature: Certificate object(s) not initialized")
        return False

    return validate_signature(signed_cert._cert, signing_cert._cert, signing_cert.public_key)


def x_validate_signature_wrapper__mutmut_3(signed_cert: Certificate, signing_cert: Certificate) -> bool:
    """Internal helper: Validates signature and issuer/subject match.

    Args:
        signed_cert: The certificate that was signed
        signing_cert: The certificate that did the signing

    Returns:
        True if signature is valid, False otherwise

    """
    if not hasattr(None, "_cert") or not hasattr(signing_cert, "_cert"):
        logger.error("📜🔍❌ Cannot validate signature: Certificate object(s) not initialized")
        return False

    return validate_signature(signed_cert._cert, signing_cert._cert, signing_cert.public_key)


def x_validate_signature_wrapper__mutmut_4(signed_cert: Certificate, signing_cert: Certificate) -> bool:
    """Internal helper: Validates signature and issuer/subject match.

    Args:
        signed_cert: The certificate that was signed
        signing_cert: The certificate that did the signing

    Returns:
        True if signature is valid, False otherwise

    """
    if not hasattr(signed_cert, None) or not hasattr(signing_cert, "_cert"):
        logger.error("📜🔍❌ Cannot validate signature: Certificate object(s) not initialized")
        return False

    return validate_signature(signed_cert._cert, signing_cert._cert, signing_cert.public_key)


def x_validate_signature_wrapper__mutmut_5(signed_cert: Certificate, signing_cert: Certificate) -> bool:
    """Internal helper: Validates signature and issuer/subject match.

    Args:
        signed_cert: The certificate that was signed
        signing_cert: The certificate that did the signing

    Returns:
        True if signature is valid, False otherwise

    """
    if not hasattr("_cert") or not hasattr(signing_cert, "_cert"):
        logger.error("📜🔍❌ Cannot validate signature: Certificate object(s) not initialized")
        return False

    return validate_signature(signed_cert._cert, signing_cert._cert, signing_cert.public_key)


def x_validate_signature_wrapper__mutmut_6(signed_cert: Certificate, signing_cert: Certificate) -> bool:
    """Internal helper: Validates signature and issuer/subject match.

    Args:
        signed_cert: The certificate that was signed
        signing_cert: The certificate that did the signing

    Returns:
        True if signature is valid, False otherwise

    """
    if not hasattr(
        signed_cert,
    ) or not hasattr(signing_cert, "_cert"):
        logger.error("📜🔍❌ Cannot validate signature: Certificate object(s) not initialized")
        return False

    return validate_signature(signed_cert._cert, signing_cert._cert, signing_cert.public_key)


def x_validate_signature_wrapper__mutmut_7(signed_cert: Certificate, signing_cert: Certificate) -> bool:
    """Internal helper: Validates signature and issuer/subject match.

    Args:
        signed_cert: The certificate that was signed
        signing_cert: The certificate that did the signing

    Returns:
        True if signature is valid, False otherwise

    """
    if not hasattr(signed_cert, "XX_certXX") or not hasattr(signing_cert, "_cert"):
        logger.error("📜🔍❌ Cannot validate signature: Certificate object(s) not initialized")
        return False

    return validate_signature(signed_cert._cert, signing_cert._cert, signing_cert.public_key)


def x_validate_signature_wrapper__mutmut_8(signed_cert: Certificate, signing_cert: Certificate) -> bool:
    """Internal helper: Validates signature and issuer/subject match.

    Args:
        signed_cert: The certificate that was signed
        signing_cert: The certificate that did the signing

    Returns:
        True if signature is valid, False otherwise

    """
    if not hasattr(signed_cert, "_CERT") or not hasattr(signing_cert, "_cert"):
        logger.error("📜🔍❌ Cannot validate signature: Certificate object(s) not initialized")
        return False

    return validate_signature(signed_cert._cert, signing_cert._cert, signing_cert.public_key)


def x_validate_signature_wrapper__mutmut_9(signed_cert: Certificate, signing_cert: Certificate) -> bool:
    """Internal helper: Validates signature and issuer/subject match.

    Args:
        signed_cert: The certificate that was signed
        signing_cert: The certificate that did the signing

    Returns:
        True if signature is valid, False otherwise

    """
    if not hasattr(signed_cert, "_cert") or hasattr(signing_cert, "_cert"):
        logger.error("📜🔍❌ Cannot validate signature: Certificate object(s) not initialized")
        return False

    return validate_signature(signed_cert._cert, signing_cert._cert, signing_cert.public_key)


def x_validate_signature_wrapper__mutmut_10(signed_cert: Certificate, signing_cert: Certificate) -> bool:
    """Internal helper: Validates signature and issuer/subject match.

    Args:
        signed_cert: The certificate that was signed
        signing_cert: The certificate that did the signing

    Returns:
        True if signature is valid, False otherwise

    """
    if not hasattr(signed_cert, "_cert") or not hasattr(None, "_cert"):
        logger.error("📜🔍❌ Cannot validate signature: Certificate object(s) not initialized")
        return False

    return validate_signature(signed_cert._cert, signing_cert._cert, signing_cert.public_key)


def x_validate_signature_wrapper__mutmut_11(signed_cert: Certificate, signing_cert: Certificate) -> bool:
    """Internal helper: Validates signature and issuer/subject match.

    Args:
        signed_cert: The certificate that was signed
        signing_cert: The certificate that did the signing

    Returns:
        True if signature is valid, False otherwise

    """
    if not hasattr(signed_cert, "_cert") or not hasattr(signing_cert, None):
        logger.error("📜🔍❌ Cannot validate signature: Certificate object(s) not initialized")
        return False

    return validate_signature(signed_cert._cert, signing_cert._cert, signing_cert.public_key)


def x_validate_signature_wrapper__mutmut_12(signed_cert: Certificate, signing_cert: Certificate) -> bool:
    """Internal helper: Validates signature and issuer/subject match.

    Args:
        signed_cert: The certificate that was signed
        signing_cert: The certificate that did the signing

    Returns:
        True if signature is valid, False otherwise

    """
    if not hasattr(signed_cert, "_cert") or not hasattr("_cert"):
        logger.error("📜🔍❌ Cannot validate signature: Certificate object(s) not initialized")
        return False

    return validate_signature(signed_cert._cert, signing_cert._cert, signing_cert.public_key)


def x_validate_signature_wrapper__mutmut_13(signed_cert: Certificate, signing_cert: Certificate) -> bool:
    """Internal helper: Validates signature and issuer/subject match.

    Args:
        signed_cert: The certificate that was signed
        signing_cert: The certificate that did the signing

    Returns:
        True if signature is valid, False otherwise

    """
    if not hasattr(signed_cert, "_cert") or not hasattr(
        signing_cert,
    ):
        logger.error("📜🔍❌ Cannot validate signature: Certificate object(s) not initialized")
        return False

    return validate_signature(signed_cert._cert, signing_cert._cert, signing_cert.public_key)


def x_validate_signature_wrapper__mutmut_14(signed_cert: Certificate, signing_cert: Certificate) -> bool:
    """Internal helper: Validates signature and issuer/subject match.

    Args:
        signed_cert: The certificate that was signed
        signing_cert: The certificate that did the signing

    Returns:
        True if signature is valid, False otherwise

    """
    if not hasattr(signed_cert, "_cert") or not hasattr(signing_cert, "XX_certXX"):
        logger.error("📜🔍❌ Cannot validate signature: Certificate object(s) not initialized")
        return False

    return validate_signature(signed_cert._cert, signing_cert._cert, signing_cert.public_key)


def x_validate_signature_wrapper__mutmut_15(signed_cert: Certificate, signing_cert: Certificate) -> bool:
    """Internal helper: Validates signature and issuer/subject match.

    Args:
        signed_cert: The certificate that was signed
        signing_cert: The certificate that did the signing

    Returns:
        True if signature is valid, False otherwise

    """
    if not hasattr(signed_cert, "_cert") or not hasattr(signing_cert, "_CERT"):
        logger.error("📜🔍❌ Cannot validate signature: Certificate object(s) not initialized")
        return False

    return validate_signature(signed_cert._cert, signing_cert._cert, signing_cert.public_key)


def x_validate_signature_wrapper__mutmut_16(signed_cert: Certificate, signing_cert: Certificate) -> bool:
    """Internal helper: Validates signature and issuer/subject match.

    Args:
        signed_cert: The certificate that was signed
        signing_cert: The certificate that did the signing

    Returns:
        True if signature is valid, False otherwise

    """
    if not hasattr(signed_cert, "_cert") or not hasattr(signing_cert, "_cert"):
        logger.error(None)
        return False

    return validate_signature(signed_cert._cert, signing_cert._cert, signing_cert.public_key)


def x_validate_signature_wrapper__mutmut_17(signed_cert: Certificate, signing_cert: Certificate) -> bool:
    """Internal helper: Validates signature and issuer/subject match.

    Args:
        signed_cert: The certificate that was signed
        signing_cert: The certificate that did the signing

    Returns:
        True if signature is valid, False otherwise

    """
    if not hasattr(signed_cert, "_cert") or not hasattr(signing_cert, "_cert"):
        logger.error("XX📜🔍❌ Cannot validate signature: Certificate object(s) not initializedXX")
        return False

    return validate_signature(signed_cert._cert, signing_cert._cert, signing_cert.public_key)


def x_validate_signature_wrapper__mutmut_18(signed_cert: Certificate, signing_cert: Certificate) -> bool:
    """Internal helper: Validates signature and issuer/subject match.

    Args:
        signed_cert: The certificate that was signed
        signing_cert: The certificate that did the signing

    Returns:
        True if signature is valid, False otherwise

    """
    if not hasattr(signed_cert, "_cert") or not hasattr(signing_cert, "_cert"):
        logger.error("📜🔍❌ cannot validate signature: certificate object(s) not initialized")
        return False

    return validate_signature(signed_cert._cert, signing_cert._cert, signing_cert.public_key)


def x_validate_signature_wrapper__mutmut_19(signed_cert: Certificate, signing_cert: Certificate) -> bool:
    """Internal helper: Validates signature and issuer/subject match.

    Args:
        signed_cert: The certificate that was signed
        signing_cert: The certificate that did the signing

    Returns:
        True if signature is valid, False otherwise

    """
    if not hasattr(signed_cert, "_cert") or not hasattr(signing_cert, "_cert"):
        logger.error("📜🔍❌ CANNOT VALIDATE SIGNATURE: CERTIFICATE OBJECT(S) NOT INITIALIZED")
        return False

    return validate_signature(signed_cert._cert, signing_cert._cert, signing_cert.public_key)


def x_validate_signature_wrapper__mutmut_20(signed_cert: Certificate, signing_cert: Certificate) -> bool:
    """Internal helper: Validates signature and issuer/subject match.

    Args:
        signed_cert: The certificate that was signed
        signing_cert: The certificate that did the signing

    Returns:
        True if signature is valid, False otherwise

    """
    if not hasattr(signed_cert, "_cert") or not hasattr(signing_cert, "_cert"):
        logger.error("📜🔍❌ Cannot validate signature: Certificate object(s) not initialized")
        return True

    return validate_signature(signed_cert._cert, signing_cert._cert, signing_cert.public_key)


def x_validate_signature_wrapper__mutmut_21(signed_cert: Certificate, signing_cert: Certificate) -> bool:
    """Internal helper: Validates signature and issuer/subject match.

    Args:
        signed_cert: The certificate that was signed
        signing_cert: The certificate that did the signing

    Returns:
        True if signature is valid, False otherwise

    """
    if not hasattr(signed_cert, "_cert") or not hasattr(signing_cert, "_cert"):
        logger.error("📜🔍❌ Cannot validate signature: Certificate object(s) not initialized")
        return False

    return validate_signature(None, signing_cert._cert, signing_cert.public_key)


def x_validate_signature_wrapper__mutmut_22(signed_cert: Certificate, signing_cert: Certificate) -> bool:
    """Internal helper: Validates signature and issuer/subject match.

    Args:
        signed_cert: The certificate that was signed
        signing_cert: The certificate that did the signing

    Returns:
        True if signature is valid, False otherwise

    """
    if not hasattr(signed_cert, "_cert") or not hasattr(signing_cert, "_cert"):
        logger.error("📜🔍❌ Cannot validate signature: Certificate object(s) not initialized")
        return False

    return validate_signature(signed_cert._cert, None, signing_cert.public_key)


def x_validate_signature_wrapper__mutmut_23(signed_cert: Certificate, signing_cert: Certificate) -> bool:
    """Internal helper: Validates signature and issuer/subject match.

    Args:
        signed_cert: The certificate that was signed
        signing_cert: The certificate that did the signing

    Returns:
        True if signature is valid, False otherwise

    """
    if not hasattr(signed_cert, "_cert") or not hasattr(signing_cert, "_cert"):
        logger.error("📜🔍❌ Cannot validate signature: Certificate object(s) not initialized")
        return False

    return validate_signature(signed_cert._cert, signing_cert._cert, None)


def x_validate_signature_wrapper__mutmut_24(signed_cert: Certificate, signing_cert: Certificate) -> bool:
    """Internal helper: Validates signature and issuer/subject match.

    Args:
        signed_cert: The certificate that was signed
        signing_cert: The certificate that did the signing

    Returns:
        True if signature is valid, False otherwise

    """
    if not hasattr(signed_cert, "_cert") or not hasattr(signing_cert, "_cert"):
        logger.error("📜🔍❌ Cannot validate signature: Certificate object(s) not initialized")
        return False

    return validate_signature(signing_cert._cert, signing_cert.public_key)


def x_validate_signature_wrapper__mutmut_25(signed_cert: Certificate, signing_cert: Certificate) -> bool:
    """Internal helper: Validates signature and issuer/subject match.

    Args:
        signed_cert: The certificate that was signed
        signing_cert: The certificate that did the signing

    Returns:
        True if signature is valid, False otherwise

    """
    if not hasattr(signed_cert, "_cert") or not hasattr(signing_cert, "_cert"):
        logger.error("📜🔍❌ Cannot validate signature: Certificate object(s) not initialized")
        return False

    return validate_signature(signed_cert._cert, signing_cert.public_key)


def x_validate_signature_wrapper__mutmut_26(signed_cert: Certificate, signing_cert: Certificate) -> bool:
    """Internal helper: Validates signature and issuer/subject match.

    Args:
        signed_cert: The certificate that was signed
        signing_cert: The certificate that did the signing

    Returns:
        True if signature is valid, False otherwise

    """
    if not hasattr(signed_cert, "_cert") or not hasattr(signing_cert, "_cert"):
        logger.error("📜🔍❌ Cannot validate signature: Certificate object(s) not initialized")
        return False

    return validate_signature(
        signed_cert._cert,
        signing_cert._cert,
    )


x_validate_signature_wrapper__mutmut_mutants: ClassVar[MutantDict] = {
    "x_validate_signature_wrapper__mutmut_1": x_validate_signature_wrapper__mutmut_1,
    "x_validate_signature_wrapper__mutmut_2": x_validate_signature_wrapper__mutmut_2,
    "x_validate_signature_wrapper__mutmut_3": x_validate_signature_wrapper__mutmut_3,
    "x_validate_signature_wrapper__mutmut_4": x_validate_signature_wrapper__mutmut_4,
    "x_validate_signature_wrapper__mutmut_5": x_validate_signature_wrapper__mutmut_5,
    "x_validate_signature_wrapper__mutmut_6": x_validate_signature_wrapper__mutmut_6,
    "x_validate_signature_wrapper__mutmut_7": x_validate_signature_wrapper__mutmut_7,
    "x_validate_signature_wrapper__mutmut_8": x_validate_signature_wrapper__mutmut_8,
    "x_validate_signature_wrapper__mutmut_9": x_validate_signature_wrapper__mutmut_9,
    "x_validate_signature_wrapper__mutmut_10": x_validate_signature_wrapper__mutmut_10,
    "x_validate_signature_wrapper__mutmut_11": x_validate_signature_wrapper__mutmut_11,
    "x_validate_signature_wrapper__mutmut_12": x_validate_signature_wrapper__mutmut_12,
    "x_validate_signature_wrapper__mutmut_13": x_validate_signature_wrapper__mutmut_13,
    "x_validate_signature_wrapper__mutmut_14": x_validate_signature_wrapper__mutmut_14,
    "x_validate_signature_wrapper__mutmut_15": x_validate_signature_wrapper__mutmut_15,
    "x_validate_signature_wrapper__mutmut_16": x_validate_signature_wrapper__mutmut_16,
    "x_validate_signature_wrapper__mutmut_17": x_validate_signature_wrapper__mutmut_17,
    "x_validate_signature_wrapper__mutmut_18": x_validate_signature_wrapper__mutmut_18,
    "x_validate_signature_wrapper__mutmut_19": x_validate_signature_wrapper__mutmut_19,
    "x_validate_signature_wrapper__mutmut_20": x_validate_signature_wrapper__mutmut_20,
    "x_validate_signature_wrapper__mutmut_21": x_validate_signature_wrapper__mutmut_21,
    "x_validate_signature_wrapper__mutmut_22": x_validate_signature_wrapper__mutmut_22,
    "x_validate_signature_wrapper__mutmut_23": x_validate_signature_wrapper__mutmut_23,
    "x_validate_signature_wrapper__mutmut_24": x_validate_signature_wrapper__mutmut_24,
    "x_validate_signature_wrapper__mutmut_25": x_validate_signature_wrapper__mutmut_25,
    "x_validate_signature_wrapper__mutmut_26": x_validate_signature_wrapper__mutmut_26,
}


def validate_signature_wrapper(*args, **kwargs):
    result = _mutmut_trampoline(
        x_validate_signature_wrapper__mutmut_orig, x_validate_signature_wrapper__mutmut_mutants, args, kwargs
    )
    return result


validate_signature_wrapper.__signature__ = _mutmut_signature(x_validate_signature_wrapper__mutmut_orig)
x_validate_signature_wrapper__mutmut_orig.__name__ = "x_validate_signature_wrapper"


# <3 🧱🤝🔒🪄
