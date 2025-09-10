"""Certificate generation utilities."""

from datetime import UTC, datetime, timedelta
import traceback

try:
    from cryptography import x509
    from cryptography.hazmat.primitives import serialization
    from cryptography.hazmat.primitives.asymmetric import ec, rsa
    
    _HAS_CRYPTO = True
except ImportError:
    x509 = None
    serialization = None
    ec = None
    rsa = None
    _HAS_CRYPTO = False

from provide.foundation import logger
from provide.foundation.crypto.certificates.base import (
    CertificateBase,
    CertificateConfig,
    CertificateError,
    CurveType,
    KeyType,
)
from provide.foundation.crypto.certificates.operations import create_x509_certificate
from provide.foundation.crypto.constants import (
    DEFAULT_CERTIFICATE_CURVE,
    DEFAULT_CERTIFICATE_KEY_TYPE,
    DEFAULT_CERTIFICATE_VALIDITY_DAYS,
    DEFAULT_RSA_KEY_SIZE,
)


def generate_certificate(
    common_name: str,
    organization_name: str,
    validity_days: int,
    key_type: str = DEFAULT_CERTIFICATE_KEY_TYPE,
    key_size: int = DEFAULT_RSA_KEY_SIZE,
    ecdsa_curve: str = DEFAULT_CERTIFICATE_CURVE,
    alt_names: list[str] | None = None,
    is_ca: bool = False,
    is_client_cert: bool = False,
) -> tuple[CertificateBase, "x509.Certificate", "rsa.RSAPrivateKey | ec.EllipticCurvePrivateKey", str, str]:
    """
    Generate a new certificate with a keypair.
    
    Returns:
        Tuple of (CertificateBase, X509Certificate, private_key, cert_pem, key_pem)
    """
    try:
        logger.debug("📜🔑🚀 Generating new keypair")
        
        now = datetime.now(UTC)
        not_valid_before = now - timedelta(days=1)
        not_valid_after = now + timedelta(days=validity_days)
        
        # Parse key type
        normalized_key_type_str = key_type.lower()
        match normalized_key_type_str:
            case "rsa":
                gen_key_type = KeyType.RSA
            case "ecdsa":
                gen_key_type = KeyType.ECDSA
            case _:
                raise ValueError(
                    f"Unsupported key_type string: '{key_type}'. "
                    "Must be 'rsa' or 'ecdsa'."
                )
        
        # Configure key parameters
        gen_curve: CurveType | None = None
        gen_key_size = None
        
        if gen_key_type == KeyType.ECDSA:
            try:
                gen_curve = CurveType[ecdsa_curve.upper()]
            except KeyError as e_curve:
                raise ValueError(
                    f"Unsupported ECDSA curve: {ecdsa_curve}"
                ) from e_curve
        else:  # RSA
            gen_key_size = key_size
        
        # Build configuration
        conf: CertificateConfig = {
            "common_name": common_name,
            "organization": organization_name,
            "alt_names": alt_names or ["localhost"],
            "key_type": gen_key_type,
            "not_valid_before": not_valid_before,
            "not_valid_after": not_valid_after,
        }
        if gen_curve is not None:
            conf["curve"] = gen_curve
        if gen_key_size is not None:
            conf["key_size"] = gen_key_size
        logger.debug(f"📜🔑🚀 Generation config: {conf}")
        
        # Generate base certificate and private key
        base, private_key = CertificateBase.create(conf)
        
        # Create X.509 certificate
        x509_cert = create_x509_certificate(
            base=base,
            private_key=private_key,
            alt_names=alt_names or ["localhost"],
            is_ca=is_ca,
            is_client_cert=is_client_cert,
        )
        
        if x509_cert is None:
            raise CertificateError(
                "Certificate object (_cert) is None after creation"
            )
        
        # Convert to PEM format
        cert_pem = x509_cert.public_bytes(serialization.Encoding.PEM).decode("utf-8")
        key_pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption(),
        ).decode("utf-8")
        
        logger.debug("📜🔑✅ Generated cert and key")
        
        return base, x509_cert, private_key, cert_pem, key_pem
        
    except Exception as e:
        logger.error(
            f"📜❌ Failed to generate certificate. Error: {type(e).__name__}: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError(
            f"Failed to initialize certificate. Original error: {type(e).__name__}"
        ) from e