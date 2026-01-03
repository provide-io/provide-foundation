# X.509 Certificates

Learn how to generate and manage X.509 certificates for secure communication.

## Overview

X.509 certificates are digital documents that bind a public key to an identity. Foundation provides utilities for creating self-signed certificates, certificate signing requests (CSRs), and managing certificate chains.

**Common use cases:**
- Development TLS/SSL certificates
- Internal service authentication
- Client certificates for mutual TLS
- Code signing certificates

## Prerequisites

Install crypto extras:
```bash
uv add provide-foundation[crypto]
```

## Generate Self-Signed Certificate

Create a self-signed certificate for development or testing:

```python
from provide.foundation.crypto.certificates import generate_self_signed_cert
from pathlib import Path

# Generate certificate
cert_pem, private_key_pem = generate_self_signed_cert(
    common_name="example.com",
    organization="My Company",
    validity_days=365
)

# Save to files
Path("cert.pem").write_text(cert_pem)
Path("key.pem").write_text(private_key_pem)
```

**Output:**
- `cert.pem`: Public certificate in PEM format
- `key.pem`: Private key in PEM format

## Certificate with Subject Alternative Names (SAN)

Create certificates valid for multiple domains:

```python
from provide.foundation.crypto.certificates import generate_self_signed_cert

# Certificate valid for multiple domains
cert_pem, key_pem = generate_self_signed_cert(
    common_name="api.example.com",
    organization="Example Corp",
    subject_alt_names=[
        "api.example.com",
        "www.api.example.com",
        "*.api.example.com",  # Wildcard
        "192.168.1.100",      # IP address
    ],
    validity_days=365
)
```

**When to use SAN:**
- Multiple subdomains on same certificate
- Load balancers with multiple backends
- Development environments with various hostnames
- Microservices with service discovery

## Certificate Configuration

### Organizational Details

Provide complete organizational information:

```python
cert_pem, key_pem = generate_self_signed_cert(
    common_name="services.mycompany.com",
    organization="My Company Inc",
    organizational_unit="Engineering",
    country="US",
    state="California",
    locality="San Francisco",
    email="admin@mycompany.com",
    validity_days=730,  # 2 years
)
```

### Key Size and Algorithm

Specify cryptographic parameters:

```python
from provide.foundation.crypto.certificates import generate_self_signed_cert

# RSA 4096-bit key
cert_pem, key_pem = generate_self_signed_cert(
    common_name="secure.example.com",
    key_size=4096,  # Default is 2048
    algorithm="RSA",
    validity_days=365,
)

# ED25519 (faster, smaller keys)
cert_pem, key_pem = generate_self_signed_cert(
    common_name="fast.example.com",
    algorithm="ED25519",
    validity_days=365,
)
```

**Algorithm comparison:**

| Algorithm | Key Size | Speed | Security | Use Case |
|-----------|----------|-------|----------|----------|
| RSA-2048  | 2048 bits | Medium | High | Standard web servers |
| RSA-4096  | 4096 bits | Slow | Very High | High-security applications |
| ED25519   | 256 bits | Very Fast | High | Modern applications, IoT |

## Certificate Signing Request (CSR)

Generate a CSR for submission to a Certificate Authority:

```python
from provide.foundation.crypto.certificates import generate_csr

# Generate private key and CSR
csr_pem, private_key_pem = generate_csr(
    common_name="www.example.com",
    organization="Example Inc",
    country="US",
    state="California",
    locality="San Francisco",
    email="admin@example.com",
)

# Save CSR for submission to CA
Path("request.csr").write_text(csr_pem)
Path("private.key").write_text(private_key_pem)
```

**Next steps with CSR:**
1. Submit CSR to Certificate Authority (Let's Encrypt, DigiCert, etc.)
2. Complete domain validation
3. Receive signed certificate from CA
4. Use signed certificate with your private key

## Certificate Chain

Work with certificate chains (certificate + intermediate + root):

```python
from provide.foundation.crypto.certificates import load_certificate_chain

# Load certificate chain
chain = load_certificate_chain("fullchain.pem")

print(f"Chain contains {len(chain)} certificates")
for i, cert in enumerate(chain):
    print(f"Certificate {i}: {cert.subject}")
    print(f"  Issuer: {cert.issuer}")
    print(f"  Valid until: {cert.not_valid_after}")
```

### Create Certificate Chain

Combine certificates into a chain:

```python
from pathlib import Path

# Read individual certificates
server_cert = Path("server.crt").read_text()
intermediate_cert = Path("intermediate.crt").read_text()
root_cert = Path("root.crt").read_text()

# Create full chain
full_chain = server_cert + intermediate_cert + root_cert

# Save full chain
Path("fullchain.pem").write_text(full_chain)
```

## Certificate Verification

Verify certificate validity and properties:

```python
from provide.foundation.crypto.certificates import verify_certificate
from datetime import datetime

# Load and verify certificate
cert = load_certificate("cert.pem")

# Check expiration
if cert.not_valid_after < datetime.now():
    print("⚠️ Certificate has expired!")
else:
    days_remaining = (cert.not_valid_after - datetime.now()).days
    print(f"✅ Certificate valid for {days_remaining} more days")

# Verify hostname
if verify_hostname(cert, "example.com"):
    print("✅ Certificate valid for example.com")
else:
    print("❌ Certificate not valid for this hostname")
```

### Extract Certificate Information

Get certificate details programmatically:

```python
from provide.foundation.crypto.certificates import get_certificate_info

# Load certificate
info = get_certificate_info("cert.pem")

print(f"Subject: {info['subject']}")
print(f"Issuer: {info['issuer']}")
print(f"Valid from: {info['not_before']}")
print(f"Valid until: {info['not_after']}")
print(f"Serial number: {info['serial_number']}")
print(f"Key algorithm: {info['key_algorithm']}")
print(f"Key size: {info['key_size']} bits")
print(f"SAN: {info['subject_alt_names']}")
```

## Common Patterns

### Development TLS Server

Create certificates for local HTTPS development:

```python
from provide.foundation.crypto.certificates import generate_self_signed_cert
from pathlib import Path

def setup_dev_tls():
    """Set up TLS certificates for local development."""
    cert_dir = Path("certs")
    cert_dir.mkdir(exist_ok=True)

    # Generate cert for localhost
    cert_pem, key_pem = generate_self_signed_cert(
        common_name="localhost",
        organization="Development",
        subject_alt_names=[
            "localhost",
            "127.0.0.1",
            "::1",
            "*.localhost",  # For subdomains
        ],
        validity_days=365,
    )

    # Save certificates
    cert_file = cert_dir / "localhost.crt"
    key_file = cert_dir / "localhost.key"

    cert_file.write_text(cert_pem)
    key_file.write_text(key_pem)

    print(f"✅ Development certificates created:")
    print(f"   Certificate: {cert_file}")
    print(f"   Private key: {key_file}")

    return cert_file, key_file

# Use with web server
cert_file, key_file = setup_dev_tls()

# Example with uvicorn (FastAPI)
# uvicorn main:app --ssl-keyfile=certs/localhost.key --ssl-certfile=certs/localhost.crt
```

### Client Certificate Authentication

Generate client certificates for mutual TLS:

```python
from provide.foundation.crypto.certificates import generate_client_cert

def create_client_cert(client_name):
    """Create client certificate for mutual TLS."""
    cert_pem, key_pem = generate_client_cert(
        common_name=client_name,
        organization="Client Services",
        email=f"{client_name}@example.com",
        validity_days=365,
    )

    # Save client credentials
    Path(f"{client_name}.crt").write_text(cert_pem)
    Path(f"{client_name}.key").write_text(key_pem)

    return cert_pem, key_pem

# Create certificates for different clients
create_client_cert("service-a")
create_client_cert("service-b")
create_client_cert("mobile-app")
```

### Certificate Rotation

Automate certificate renewal:

```python
from provide.foundation.crypto.certificates import (
    generate_self_signed_cert,
    load_certificate,
)
from datetime import datetime, timedelta
from pathlib import Path

def rotate_certificate_if_needed(cert_path, key_path, days_before_expiry=30):
    """Rotate certificate if it's expiring soon."""
    try:
        cert = load_certificate(cert_path)
        days_remaining = (cert.not_valid_after - datetime.now()).days

        if days_remaining > days_before_expiry:
            print(f"✅ Certificate valid for {days_remaining} days")
            return False

        print(f"⚠️ Certificate expiring in {days_remaining} days, rotating...")

    except FileNotFoundError:
        print("⚠️ Certificate not found, generating new one...")

    # Generate new certificate
    cert_pem, key_pem = generate_self_signed_cert(
        common_name="example.com",
        organization="Example Inc",
        validity_days=365,
    )

    # Save new certificate
    Path(cert_path).write_text(cert_pem)
    Path(key_path).write_text(key_pem)

    print("✅ Certificate rotated successfully")
    return True

# Check and rotate if needed
rotate_certificate_if_needed("server.crt", "server.key")
```

### Certificate for Service Mesh

Generate certificates for microservices:

```python
from provide.foundation.crypto.certificates import generate_service_cert

def setup_service_mesh_certs(service_name, namespace="default"):
    """Generate certificates for Kubernetes service mesh."""
    # Generate certificate with proper SAN for k8s DNS
    cert_pem, key_pem = generate_service_cert(
        common_name=f"{service_name}.{namespace}.svc.cluster.local",
        organization="Service Mesh",
        subject_alt_names=[
            f"{service_name}",
            f"{service_name}.{namespace}",
            f"{service_name}.{namespace}.svc",
            f"{service_name}.{namespace}.svc.cluster.local",
        ],
        validity_days=90,  # Shorter validity for security
    )

    # Save as Kubernetes secret format
    import base64
    secret_manifest = f"""
apiVersion: v1
kind: Secret
metadata:
  name: {service_name}-tls
  namespace: {namespace}
type: kubernetes.io/tls
data:
  tls.crt: {base64.b64encode(cert_pem.encode()).decode()}
  tls.key: {base64.b64encode(key_pem.encode()).decode()}
"""

    Path(f"{service_name}-secret.yaml").write_text(secret_manifest)
    print(f"✅ Generated certificate secret for {service_name}")

# Generate certs for services
setup_service_mesh_certs("user-service")
setup_service_mesh_certs("payment-service")
setup_service_mesh_certs("inventory-service")
```

## Converting Certificate Formats

### PEM to DER

Convert from PEM (text) to DER (binary):

```python
from provide.foundation.crypto.certificates import pem_to_der
from pathlib import Path

# Load PEM certificate
pem_cert = Path("cert.pem").read_text()

# Convert to DER
der_cert = pem_to_der(pem_cert)

# Save DER certificate
Path("cert.der").write_bytes(der_cert)
```

### Create PKCS#12 Bundle

Create a PKCS#12 (.p12/.pfx) file with certificate and private key:

```python
from provide.foundation.crypto.certificates import create_pkcs12

# Create PKCS#12 bundle
p12_data = create_pkcs12(
    certificate_pem=cert_pem,
    private_key_pem=key_pem,
    passphrase="secret-password",
    friendly_name="My Certificate",
)

# Save to file
Path("certificate.p12").write_bytes(p12_data)
```

## Best Practices

### ✅ DO: Use Appropriate Validity Periods

```python
# ✅ Good: Reasonable validity periods
# Development
cert = generate_self_signed_cert(
    common_name="dev.local",
    validity_days=90,  # 3 months for dev
)

# Production (with proper CA)
cert = generate_self_signed_cert(
    common_name="prod.example.com",
    validity_days=365,  # 1 year max
)

# ❌ Bad: Too long validity
cert = generate_self_signed_cert(
    common_name="example.com",
    validity_days=3650,  # 10 years - security risk!
)
```

### ✅ DO: Protect Private Keys

```python
# ✅ Good: Secure file permissions
import os
from pathlib import Path

key_file = Path("private.key")
key_file.write_text(private_key_pem)
os.chmod(key_file, 0o600)  # Read/write for owner only

# ✅ Good: Never log private keys
logger.info("Certificate generated", cert_path=cert_path)  # OK
# ❌ Never do this:
# logger.info("Key generated", key=private_key_pem)  # NEVER!
```

### ✅ DO: Use SAN for Multiple Hostnames

```python
# ✅ Good: Proper SAN usage
cert = generate_self_signed_cert(
    common_name="api.example.com",
    subject_alt_names=[
        "api.example.com",
        "www.api.example.com",
        "api-staging.example.com",
    ],
)

# ❌ Bad: Creating separate certs for each hostname
# More certs = more to manage and rotate
```

### ✅ DO: Monitor Certificate Expiration

```python
# ✅ Good: Automated monitoring
from datetime import datetime, timedelta

def check_certificate_expiration(cert_path, warn_days=30):
    """Monitor certificate expiration."""
    cert = load_certificate(cert_path)
    expires = cert.not_valid_after
    days_remaining = (expires - datetime.now()).days

    if days_remaining < 0:
        logger.critical("Certificate expired", cert_path=cert_path)
    elif days_remaining < warn_days:
        logger.warning(
            "Certificate expiring soon",
            cert_path=cert_path,
            days_remaining=days_remaining,
        )
    else:
        logger.info(
            "Certificate valid",
            cert_path=cert_path,
            days_remaining=days_remaining,
        )

    return days_remaining
```

### ❌ DON'T: Use Self-Signed Certs in Production

```python
# ❌ Bad: Self-signed in production
cert = generate_self_signed_cert(
    common_name="production.example.com",  # Don't!
)

# ✅ Good: Use proper CA for production
# - Let's Encrypt (free, automated)
# - DigiCert, GlobalSign, etc. (commercial)
# - Internal CA for private services
```

### ❌ DON'T: Commit Private Keys to Version Control

```python
# ✅ Good: .gitignore
"""
*.key
*.pem
*.p12
*.pfx
certs/
"""

# ❌ Bad: Committing keys
# git add private.key  # NEVER!
```

## Certificate Management Tools

### List Certificates

Get information about multiple certificates:

```python
from provide.foundation.crypto.certificates import list_certificates
from pathlib import Path

def audit_certificates(cert_dir):
    """Audit all certificates in directory."""
    cert_dir = Path(cert_dir)

    for cert_file in cert_dir.glob("*.crt"):
        info = get_certificate_info(cert_file)

        print(f"\n📄 {cert_file.name}")
        print(f"   Subject: {info['subject']}")
        print(f"   Expires: {info['not_after']}")

        # Check expiration
        days = (info['not_after'] - datetime.now()).days
        if days < 30:
            print(f"   ⚠️ Expiring in {days} days!")
        else:
            print(f"   ✅ Valid for {days} days")

audit_certificates("certs/")
```

### Validate Certificate Chain

Verify a certificate chain is valid:

```python
from provide.foundation.crypto.certificates import validate_chain

def verify_cert_chain(server_cert, intermediate_cert, root_cert):
    """Verify certificate chain is valid."""
    try:
        is_valid = validate_chain(
            server_cert=server_cert,
            intermediate_cert=intermediate_cert,
            root_cert=root_cert,
        )

        if is_valid:
            print("✅ Certificate chain is valid")
        else:
            print("❌ Certificate chain is invalid")

        return is_valid
    except Exception as e:
        logger.exception("Chain validation failed")
        return False
```

## Next Steps

### Related Guides
- **[Key Generation](keys.md)**: Generate cryptographic keys
- **[Signing & Verification](signing.md)**: Sign and verify data

### Examples
- See `examples/crypto/` for certificate examples
- See `examples/production/` for TLS configuration patterns

### API Reference
- **[API Reference: Crypto](../../reference/provide/foundation/crypto/index.md)**: Complete API documentation

---

**Tip**: For development, self-signed certificates are fine. For production, always use certificates from a trusted CA like Let's Encrypt (free and automated) or a commercial provider.
