# Key Generation

Learn how to generate and manage cryptographic keys with Foundation.

## Overview

Foundation provides utilities for generating Ed25519 and RSA keys with secure defaults.

## Generate Ed25519 Keys

```python
from provide.foundation.crypto import generate_ed25519_keypair

# Generate a new keypair
public_key, private_key = generate_ed25519_keypair()

print(f"Public key: {public_key.hex()}")
print(f"Private key: {private_key.hex()}")
```

## Generate RSA Keys

```python
from provide.foundation.crypto import generate_rsa_keypair

# Generate 2048-bit RSA keypair
public_key, private_key = generate_rsa_keypair(key_size=2048)

# For higher security, use 4096-bit
public_key, private_key = generate_rsa_keypair(key_size=4096)
```

## Save Keys to Files

```python
from pathlib import Path
from provide.foundation.file import atomic_write

# Save private key (with restricted permissions)
atomic_write(
    path="private_key.pem",
    content=private_key.encode(),
    permissions=0o600  # Only owner can read
)

# Save public key
atomic_write(
    path="public_key.pem",
    content=public_key.encode()
)
```

## Load Keys from Files

```python
from pathlib import Path

private_key_data = Path("private_key.pem").read_bytes()
public_key_data = Path("public_key.pem").read_bytes()
```

## Next Steps

- **[Signing & Verification](signing.md)** - Sign and verify data
- **[Certificates](certificates.md)** - X.509 certificates
- **[API Reference: Crypto](../../reference/provide/foundation/crypto/index.md)** - Complete crypto API
