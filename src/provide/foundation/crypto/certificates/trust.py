from __future__ import annotations

"""Certificate trust chain and verification utilities."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from provide.foundation.crypto.certificates.certificate import Certificate

try:
    import cryptography  # noqa: F401

    _HAS_CRYPTO = True
except ImportError:
    _HAS_CRYPTO = False

from provide.foundation import logger
from provide.foundation.crypto.certificates.base import CertificateError
from provide.foundation.crypto.certificates.operations import validate_signature


def verify_trust(
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


def validate_signature_wrapper(signed_cert: Certificate, signing_cert: Certificate) -> bool:
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
