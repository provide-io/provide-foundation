# Certificates

Learn how to generate and manage X.509 certificates.

## Overview

Foundation provides utilities for creating self-signed certificates and certificate signing requests (CSRs).

## Generate Self-Signed Certificate

```python
from provide.foundation.crypto.certificates import generate_self_signed_cert

# Generate certificate
cert, private_key = generate_self_signed_cert(
    common_name="example.com",
    organization="My Company",
    validity_days=365
)

# Save to files
Path("cert.pem").write_text(cert)
Path("key.pem").write_text(private_key)
```

## Certificate with SAN

```python
# Certificate with Subject Alternative Names
cert, key = generate_self_signed_cert(
    common_name="api.example.com",
    subject_alt_names=[
        "api.example.com",
        "www.api.example.com",
        "*.api.example.com"
    ]
)
```

## Next Steps

- **[Key Generation](keys.md)** - Generate keys
- **[Signing & Verification](signing.md)** - Sign data
- **[API Reference: Crypto](../../reference/provide/foundation/crypto/index.md)**
