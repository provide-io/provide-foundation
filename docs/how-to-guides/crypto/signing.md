# Signing & Verification

Learn how to sign data and verify signatures using cryptographic keys.

## Overview

Digital signatures provide authenticity and integrity verification for data.

## Sign Data with Ed25519

```python
from provide.foundation.crypto import (
    generate_ed25519_keypair,
    sign_ed25519,
    verify_ed25519
)

# Generate keypair
public_key, private_key = generate_ed25519_keypair()

# Sign data
message = b"Important data to sign"
signature = sign_ed25519(message, private_key)

# Verify signature
is_valid = verify_ed25519(message, signature, public_key)
print(f"Signature valid: {is_valid}")  # True
```

## Sign Data with RSA

```python
from provide.foundation.crypto import (
    generate_rsa_keypair,
    sign_rsa,
    verify_rsa
)

# Generate RSA keypair
public_key, private_key = generate_rsa_keypair()

# Sign data
message = b"Important message"
signature = sign_rsa(message, private_key)

# Verify
is_valid = verify_rsa(message, signature, public_key)
```

## Sign Files

```python
from pathlib import Path

def sign_file(file_path: Path, private_key: bytes) -> bytes:
    """Sign a file's contents."""
    data = file_path.read_bytes()
    return sign_ed25519(data, private_key)

def verify_file(file_path: Path, signature: bytes, public_key: bytes) -> bool:
    """Verify a file's signature."""
    data = file_path.read_bytes()
    return verify_ed25519(data, signature, public_key)
```

## Next Steps

- **[Key Generation](keys.md)** - Generate keys
- **[Certificates](certificates.md)** - X.509 certificates
