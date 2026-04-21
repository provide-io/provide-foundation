# Digital Signatures & Verification

Learn how to sign data and verify signatures using cryptographic keys with Foundation's signing utilities.

## Overview

Digital signatures provide cryptographic proof of authenticity and integrity. Foundation supports multiple signature algorithms including Ed25519 (recommended), RSA, and ECDSA, with simple APIs for signing messages, files, and structured data.

**What you'll learn:**
- Sign and verify data with Ed25519, RSA, and ECDSA
- Sign files and verify file integrity
- Implement detached signatures
- Create and verify JWT tokens
- Build multi-signature schemes
- Apply timestamping to signatures
- Test signature code
- Follow security best practices

**Key Features:**
- 🔐 **Multiple Algorithms**: Ed25519, RSA, ECDSA support
- ⚡ **High Performance**: Fast signature generation and verification
- 📝 **Message Signing**: Sign arbitrary data and messages
- 📄 **File Signing**: Built-in file integrity verification
- 🎯 **JWT Support**: Create and verify JSON Web Tokens
- 🔒 **Detached Signatures**: Separate signature files for large data
- 🧪 **Testable**: Easy to mock and test signature operations

## Prerequisites

```bash
# Core cryptography support (included by default)
uv add provide-foundation

# For JWT support (optional)
uv add provide-foundation[jwt]
```

## Basic Signing & Verification

### Ed25519 Signatures (Recommended)

Ed25519 provides the fastest and most secure signatures:

```python
from provide.foundation.crypto import (
    generate_ed25519_keypair,
    sign_ed25519,
    verify_ed25519
)
from provide.foundation import logger

# Generate keypair
public_key, private_key = generate_ed25519_keypair()

# Sign a message
message = b"Important data to sign"
signature = sign_ed25519(message, private_key)

logger.info(
    "message_signed",
    algorithm="ed25519",
    message_size=len(message),
    signature_size=len(signature)
)

# Verify signature
is_valid = verify_ed25519(message, signature, public_key)
logger.info("signature_verified", valid=is_valid)

print(f"Signature valid: {is_valid}")  # True
```

### RSA Signatures

RSA signatures are widely supported but slower:

```python
from provide.foundation.crypto import (
    generate_rsa_keypair,
    sign_rsa,
    verify_rsa
)

# Generate RSA keypair
public_key, private_key = generate_rsa_keypair(key_size=4096)

# Sign data
message = b"Important message"
signature = sign_rsa(message, private_key)

# Verify signature
is_valid = verify_rsa(message, signature, public_key)

logger.info(
    "rsa_signature_verified",
    key_size=4096,
    valid=is_valid
)
```

### ECDSA Signatures

ECDSA provides good balance of security and performance:

```python
from provide.foundation.crypto import (
    generate_ecdsa_keypair,
    sign_ecdsa,
    verify_ecdsa
)

# Generate ECDSA keypair (P-256 curve)
public_key, private_key = generate_ecdsa_keypair(curve="P-256")

# Sign message
message = b"Data to sign"
signature = sign_ecdsa(message, private_key)

# Verify signature
is_valid = verify_ecdsa(message, signature, public_key)
```

## File Signing

### Sign and Verify Files

Sign files to ensure integrity and authenticity:

```python
from pathlib import Path
from provide.foundation.crypto import sign_ed25519, verify_ed25519
from provide.foundation import logger

def sign_file(file_path: Path, private_key: bytes) -> bytes:
    """Sign a file's contents."""
    data = file_path.read_bytes()
    signature = sign_ed25519(data, private_key)

    logger.info(
        "file_signed",
        file=str(file_path),
        file_size=len(data),
        signature_size=len(signature)
    )

    return signature

def verify_file(
    file_path: Path,
    signature: bytes,
    public_key: bytes
) -> bool:
    """Verify a file's signature."""
    data = file_path.read_bytes()
    is_valid = verify_ed25519(data, signature, public_key)

    logger.info(
        "file_verification",
        file=str(file_path),
        valid=is_valid
    )

    return is_valid

# Usage
file_path = Path("document.pdf")
signature = sign_file(file_path, private_key)

# Later, verify the file hasn't changed
if verify_file(file_path, signature, public_key):
    print("File is authentic and unmodified")
else:
    print("File has been tampered with!")
```

### Detached Signature Files

Store signatures separately for large files:

```python
from pathlib import Path
from provide.foundation.crypto import sign_ed25519, verify_ed25519
from provide.foundation.file import atomic_write
from provide.foundation import logger

def create_detached_signature(
    file_path: Path,
    private_key: bytes
) -> Path:
    """Create a detached signature file."""
    # Sign the file
    data = file_path.read_bytes()
    signature = sign_ed25519(data, private_key)

    # Save signature to .sig file
    sig_path = file_path.with_suffix(file_path.suffix + ".sig")
    atomic_write(path=sig_path, content=signature)

    logger.info(
        "detached_signature_created",
        file=str(file_path),
        signature_file=str(sig_path)
    )

    return sig_path

def verify_detached_signature(
    file_path: Path,
    public_key: bytes
) -> bool:
    """Verify a detached signature file."""
    sig_path = file_path.with_suffix(file_path.suffix + ".sig")

    if not sig_path.exists():
        logger.warning("signature_file_missing", file=str(file_path))
        return False

    # Read file and signature
    data = file_path.read_bytes()
    signature = sig_path.read_bytes()

    # Verify
    is_valid = verify_ed25519(data, signature, public_key)

    logger.info(
        "detached_signature_verified",
        file=str(file_path),
        valid=is_valid
    )

    return is_valid

# Usage
file_path = Path("release.tar.gz")
sig_path = create_detached_signature(file_path, private_key)

# Verify later
if verify_detached_signature(file_path, public_key):
    print("Release package is authentic")
```

## JSON Web Tokens (JWT)

### Create JWT Tokens

Sign structured data as JWT tokens:

```python
import json
from datetime import datetime, timedelta
from base64 import urlsafe_b64encode, urlsafe_b64decode
from provide.foundation.crypto import sign_ed25519, verify_ed25519
from provide.foundation import logger

def create_jwt(
    payload: dict,
    private_key: bytes,
    expires_in: timedelta = timedelta(hours=1)
) -> str:
    """Create a JWT token."""
    # Add standard claims
    now = datetime.utcnow()
    payload["iat"] = int(now.timestamp())
    payload["exp"] = int((now + expires_in).timestamp())

    # Encode header and payload
    header = {"alg": "EdDSA", "typ": "JWT"}
    header_b64 = urlsafe_b64encode(
        json.dumps(header).encode()
    ).decode().rstrip("=")
    payload_b64 = urlsafe_b64encode(
        json.dumps(payload).encode()
    ).decode().rstrip("=")

    # Create signing input
    message = f"{header_b64}.{payload_b64}".encode()

    # Sign
    signature = sign_ed25519(message, private_key)
    signature_b64 = urlsafe_b64encode(signature).decode().rstrip("=")

    # Combine into JWT
    jwt_token = f"{header_b64}.{payload_b64}.{signature_b64}"

    logger.info(
        "jwt_created",
        subject=payload.get("sub"),
        expires_in=expires_in.total_seconds()
    )

    return jwt_token

def verify_jwt(token: str, public_key: bytes) -> dict | None:
    """Verify and decode a JWT token."""
    try:
        # Split token
        parts = token.split(".")
        if len(parts) != 3:
            logger.warning("invalid_jwt_format")
            return None

        header_b64, payload_b64, signature_b64 = parts

        # Verify signature
        message = f"{header_b64}.{payload_b64}".encode()
        signature = urlsafe_b64decode(signature_b64 + "==")

        if not verify_ed25519(message, signature, public_key):
            logger.warning("jwt_signature_invalid")
            return None

        # Decode payload
        payload_json = urlsafe_b64decode(payload_b64 + "==")
        payload = json.loads(payload_json)

        # Check expiration
        if "exp" in payload:
            exp = datetime.fromtimestamp(payload["exp"])
            if datetime.utcnow() > exp:
                logger.warning("jwt_expired", exp=payload["exp"])
                return None

        logger.info("jwt_verified", subject=payload.get("sub"))
        return payload

    except Exception as e:
        logger.error("jwt_verification_failed", error=str(e))
        return None

# Usage
payload = {
    "sub": "user123",
    "name": "Alice",
    "admin": True
}
token = create_jwt(payload, private_key, expires_in=timedelta(hours=24))

# Later, verify the token
verified_payload = verify_jwt(token, public_key)
if verified_payload:
    print(f"Token valid for user: {verified_payload['name']}")
```

## Advanced Signature Patterns

### Multi-Signature Verification

Require multiple signatures for critical operations:

```python
from provide.foundation.crypto import sign_ed25519, verify_ed25519
from provide.foundation import logger

class MultiSignature:
    """Manage multi-signature verification."""

    def __init__(self, threshold: int):
        self.threshold = threshold
        self.signatures: list[tuple[bytes, bytes]] = []  # (public_key, signature)

    def add_signature(self, public_key: bytes, signature: bytes) -> None:
        """Add a signature from a signer."""
        self.signatures.append((public_key, signature))
        logger.debug(
            "signature_added",
            total_signatures=len(self.signatures),
            threshold=self.threshold
        )

    def verify(self, message: bytes) -> bool:
        """Verify that threshold of signatures is valid."""
        valid_count = 0

        for public_key, signature in self.signatures:
            if verify_ed25519(message, signature, public_key):
                valid_count += 1

        is_valid = valid_count >= self.threshold

        logger.info(
            "multisig_verification",
            valid_signatures=valid_count,
            threshold=self.threshold,
            valid=is_valid
        )

        return is_valid

# Usage: Require 2 of 3 signatures
message = b"Transfer $1,000,000"

# Three signers
pub1, priv1 = generate_ed25519_keypair()
pub2, priv2 = generate_ed25519_keypair()
pub3, priv3 = generate_ed25519_keypair()

# Create multi-signature
multisig = MultiSignature(threshold=2)
multisig.add_signature(pub1, sign_ed25519(message, priv1))
multisig.add_signature(pub2, sign_ed25519(message, priv2))

# Verify (2 signatures meets threshold)
if multisig.verify(message):
    print("Transaction approved by quorum")
```

### Timestamped Signatures

Include timestamps to prevent replay attacks:

```python
import time
from datetime import datetime, timedelta
from provide.foundation.crypto import sign_ed25519, verify_ed25519
from provide.foundation import logger

def create_timestamped_signature(
    message: bytes,
    private_key: bytes
) -> tuple[bytes, int]:
    """Create a signature with timestamp."""
    timestamp = int(time.time())

    # Include timestamp in signed data
    data_to_sign = message + timestamp.to_bytes(8, 'big')
    signature = sign_ed25519(data_to_sign, private_key)

    logger.info("timestamped_signature_created", timestamp=timestamp)

    return signature, timestamp

def verify_timestamped_signature(
    message: bytes,
    signature: bytes,
    timestamp: int,
    public_key: bytes,
    max_age: timedelta = timedelta(minutes=5)
) -> bool:
    """Verify a timestamped signature."""
    # Check timestamp freshness
    now = int(time.time())
    age = now - timestamp

    if age > max_age.total_seconds():
        logger.warning(
            "signature_expired",
            age_seconds=age,
            max_age_seconds=max_age.total_seconds()
        )
        return False

    if age < 0:
        logger.warning("signature_from_future", timestamp=timestamp)
        return False

    # Verify signature with timestamp
    data_to_verify = message + timestamp.to_bytes(8, 'big')
    is_valid = verify_ed25519(data_to_verify, signature, public_key)

    logger.info(
        "timestamped_signature_verified",
        valid=is_valid,
        age_seconds=age
    )

    return is_valid

# Usage
message = b"API request"
signature, timestamp = create_timestamped_signature(message, private_key)

# Verify with 5-minute window
if verify_timestamped_signature(message, signature, timestamp, public_key):
    print("Signature is fresh and valid")
```

### Signature with Metadata

Include additional context in signatures:

```python
import json
from provide.foundation.crypto import sign_ed25519, verify_ed25519
from provide.foundation import logger

class SignedMessage:
    """Message with signature and metadata."""

    def __init__(
        self,
        message: bytes,
        metadata: dict,
        signature: bytes,
        public_key: bytes
    ):
        self.message = message
        self.metadata = metadata
        self.signature = signature
        self.public_key = public_key

    @classmethod
    def create(
        cls,
        message: bytes,
        private_key: bytes,
        public_key: bytes,
        **metadata
    ) -> "SignedMessage":
        """Create a signed message with metadata."""
        # Add default metadata
        metadata.setdefault("timestamp", int(time.time()))
        metadata.setdefault("version", "1.0")

        # Create signing payload
        payload = {
            "message": message.hex(),
            "metadata": metadata
        }
        payload_bytes = json.dumps(payload, sort_keys=True).encode()

        # Sign
        signature = sign_ed25519(payload_bytes, private_key)

        logger.info("signed_message_created", metadata=metadata)

        return cls(message, metadata, signature, public_key)

    def verify(self) -> bool:
        """Verify the signature."""
        # Reconstruct payload
        payload = {
            "message": self.message.hex(),
            "metadata": self.metadata
        }
        payload_bytes = json.dumps(payload, sort_keys=True).encode()

        # Verify
        is_valid = verify_ed25519(payload_bytes, self.signature, self.public_key)

        logger.info(
            "signed_message_verified",
            valid=is_valid,
            metadata=self.metadata
        )

        return is_valid

# Usage
signed_msg = SignedMessage.create(
    message=b"Important announcement",
    private_key=private_key,
    public_key=public_key,
    author="alice@example.com",
    purpose="announcement"
)

if signed_msg.verify():
    print(f"Message from {signed_msg.metadata['author']} is authentic")
```

## Common Patterns

### API Request Signing

Sign API requests for authentication:

```python
import hashlib
import hmac
from datetime import datetime
from provide.foundation.crypto import sign_ed25519
from provide.foundation import logger

def sign_api_request(
    method: str,
    path: str,
    body: bytes,
    private_key: bytes
) -> dict[str, str]:
    """Create signature headers for API request."""
    timestamp = datetime.utcnow().isoformat()

    # Create canonical request
    canonical = f"{method}\n{path}\n{timestamp}\n{hashlib.sha256(body).hexdigest()}"

    # Sign
    signature = sign_ed25519(canonical.encode(), private_key)

    headers = {
        "X-Signature": signature.hex(),
        "X-Timestamp": timestamp,
        "X-Algorithm": "EdDSA"
    }

    logger.info("api_request_signed", method=method, path=path)

    return headers

# Usage
headers = sign_api_request(
    method="POST",
    path="/api/transfers",
    body=b'{"amount": 100}',
    private_key=private_key
)
```

### Code Signing

Sign code releases for distribution:

```python
from pathlib import Path
import tarfile
from provide.foundation.crypto import sign_ed25519
from provide.foundation.file import atomic_write
from provide.foundation import logger

def sign_release(
    release_dir: Path,
    version: str,
    private_key: bytes
) -> Path:
    """Sign a code release package."""
    # Create tarball
    tarball_path = release_dir.parent / f"release-{version}.tar.gz"

    with tarfile.open(tarball_path, "w:gz") as tar:
        tar.add(release_dir, arcname=f"release-{version}")

    # Sign the tarball
    tarball_data = tarball_path.read_bytes()
    signature = sign_ed25519(tarball_data, private_key)

    # Save signature
    sig_path = tarball_path.with_suffix(".tar.gz.sig")
    atomic_write(path=sig_path, content=signature)

    # Create manifest
    manifest = {
        "version": version,
        "file": tarball_path.name,
        "signature": sig_path.name,
        "sha256": hashlib.sha256(tarball_data).hexdigest()
    }
    manifest_path = tarball_path.parent / f"release-{version}.manifest.json"
    atomic_write(
        path=manifest_path,
        content=json.dumps(manifest, indent=2).encode()
    )

    logger.info(
        "release_signed",
        version=version,
        tarball=str(tarball_path),
        signature=str(sig_path)
    )

    return tarball_path

# Usage
release_path = sign_release(
    release_dir=Path("dist/myapp"),
    version="1.0.0",
    private_key=private_key
)
```

### Document Signing

Sign documents with verification metadata:

```python
from datetime import datetime
from provide.foundation.crypto import sign_ed25519, verify_ed25519
from provide.foundation import logger

class DocumentSignature:
    """Signed document with verification info."""

    def __init__(
        self,
        document: bytes,
        signature: bytes,
        signer: str,
        timestamp: datetime
    ):
        self.document = document
        self.signature = signature
        self.signer = signer
        self.timestamp = timestamp

    @classmethod
    def sign_document(
        cls,
        document: bytes,
        private_key: bytes,
        signer: str
    ) -> "DocumentSignature":
        """Sign a document."""
        signature = sign_ed25519(document, private_key)
        timestamp = datetime.utcnow()

        logger.info("document_signed", signer=signer)

        return cls(document, signature, signer, timestamp)

    def verify(self, public_key: bytes) -> bool:
        """Verify the document signature."""
        is_valid = verify_ed25519(self.document, self.signature, public_key)

        logger.info(
            "document_verified",
            valid=is_valid,
            signer=self.signer,
            timestamp=self.timestamp.isoformat()
        )

        return is_valid

    def to_dict(self) -> dict:
        """Export signature info."""
        return {
            "signer": self.signer,
            "timestamp": self.timestamp.isoformat(),
            "signature": self.signature.hex(),
            "document_hash": hashlib.sha256(self.document).hexdigest()
        }

# Usage
doc = Path("contract.pdf").read_bytes()
signed_doc = DocumentSignature.sign_document(
    document=doc,
    private_key=private_key,
    signer="alice@company.com"
)

if signed_doc.verify(public_key):
    print(f"Document signed by {signed_doc.signer} at {signed_doc.timestamp}")
```

## Best Practices

### ✅ DO: Use Ed25519 for New Applications

```python
# ✅ GOOD: Ed25519 is fast and secure
from provide.foundation.crypto import sign_ed25519, verify_ed25519

signature = sign_ed25519(message, private_key)
```

### ❌ DON'T: Use MD5 or SHA1 for Signatures

```python
# ❌ BAD: MD5 and SHA1 are cryptographically broken
import hashlib
signature = hashlib.md5(message).hexdigest()  # NEVER!

# ✅ GOOD: Use proper signature algorithms
from provide.foundation.crypto import sign_ed25519
signature = sign_ed25519(message, private_key)
```

### ✅ DO: Verify Signatures Before Trusting Data

```python
# ✅ GOOD: Always verify before using data
if verify_ed25519(message, signature, public_key):
    # Process trusted data
    process_message(message)
else:
    logger.error("signature_verification_failed")
    raise ValueError("Invalid signature")
```

### ❌ DON'T: Sign Sensitive Data Directly

```python
# ❌ BAD: Signing reveals the data
signature = sign_ed25519(password, private_key)  # Don't sign secrets!

# ✅ GOOD: Sign a hash of sensitive data
import hashlib
password_hash = hashlib.sha256(password).digest()
signature = sign_ed25519(password_hash, private_key)
```

### ✅ DO: Include Context in Signed Data

```python
# ✅ GOOD: Include purpose to prevent signature reuse
context = f"transfer:amount={amount}:to={recipient}".encode()
signature = sign_ed25519(context, private_key)

# Prevents using signature for different purpose
```

### ❌ DON'T: Reuse Signatures

```python
# ❌ BAD: Signature reuse across different data
signature = sign_ed25519(message1, private_key)
# Later using same signature for message2... NEVER!

# ✅ GOOD: Generate fresh signature for each message
sig1 = sign_ed25519(message1, private_key)
sig2 = sign_ed25519(message2, private_key)
```

### ✅ DO: Use Detached Signatures for Large Files

```python
# ✅ GOOD: Separate signature file for large data
signature = sign_file(large_file, private_key)
sig_path.write_bytes(signature)

# Allows distributing signature separately
```

### ❌ DON'T: Ignore Signature Verification Failures

```python
# ❌ BAD: Silently proceeding on verification failure
try:
    if not verify_ed25519(msg, sig, pub_key):
        pass  # Oops, data could be tampered!
except Exception:
    pass

# ✅ GOOD: Fail fast on verification failure
if not verify_ed25519(message, signature, public_key):
    logger.error("signature_invalid")
    raise SecurityError("Signature verification failed")
```

### ✅ DO: Include Timestamps to Prevent Replay

```python
# ✅ GOOD: Timestamp prevents reusing old signatures
timestamp = int(time.time())
data = message + timestamp.to_bytes(8, 'big')
signature = sign_ed25519(data, private_key)
```

### ❌ DON'T: Sign Untrusted User Input Directly

```python
# ❌ BAD: Signing arbitrary user data
user_input = request.get("data")
signature = sign_ed25519(user_input.encode(), private_key)

# ✅ GOOD: Validate and sanitize first
validated_data = validate_user_input(user_input)
signature = sign_ed25519(validated_data.encode(), private_key)
```

### ✅ DO: Use Different Keys for Different Purposes

```python
# ✅ GOOD: Separate signing and encryption keys
signing_pub, signing_priv = generate_ed25519_keypair()
encryption_pub, encryption_priv = generate_ed25519_keypair()

# Sign with signing key only
signature = sign_ed25519(message, signing_priv)
```

### ❌ DON'T: Expose Signatures Without Rate Limiting

```python
# ❌ BAD: Unlimited signature generation
@app.route("/sign")
def sign_endpoint():
    data = request.json["data"]
    return sign_ed25519(data.encode(), private_key).hex()

# ✅ GOOD: Rate limit signature operations
from provide.foundation.resilience import rate_limit

@rate_limit(max_calls=10, period=60)
def sign_data(data: bytes) -> bytes:
    return sign_ed25519(data, private_key)
```

### ✅ DO: Verify Signature Before Parsing Payload

```python
# ✅ GOOD: Verify signature first
if not verify_ed25519(payload, signature, public_key):
    raise ValueError("Invalid signature")

# Now safe to parse
data = json.loads(payload)
```

### ❌ DON'T: Log Signatures Carelessly

```python
# ❌ BAD: Logging signatures could aid attackers
logger.info("signature", sig=signature.hex())

# ✅ GOOD: Log only verification result
logger.info("signature_verification", valid=is_valid)
```

### ✅ DO: Test Signature Roundtrips

```python
# ✅ GOOD: Always test sign/verify cycle
message = b"test"
signature = sign_ed25519(message, private_key)
assert verify_ed25519(message, signature, public_key)

# Verify tampering is detected
assert not verify_ed25519(b"different", signature, public_key)
```

## Testing Signature Operations

### Unit Testing

```python
import pytest
from provide.foundation.crypto import (
    generate_ed25519_keypair,
    sign_ed25519,
    verify_ed25519
)
from provide.testkit import FoundationTestCase

class TestSignatures(FoundationTestCase):
    """Test signature operations."""

    def setup_method(self) -> None:
        """Set up test fixtures."""
        super().setup_method()
        self.public_key, self.private_key = generate_ed25519_keypair()

    def test_sign_and_verify(self) -> None:
        """Test basic signing and verification."""
        message = b"test message"
        signature = sign_ed25519(message, self.private_key)

        # Should verify with correct key
        assert verify_ed25519(message, signature, self.public_key)

        # Should fail with different message
        assert not verify_ed25519(b"different", signature, self.public_key)

    def test_signature_tampering_detection(self) -> None:
        """Test that tampering is detected."""
        message = b"original message"
        signature = sign_ed25519(message, self.private_key)

        # Tamper with signature
        tampered_sig = bytearray(signature)
        tampered_sig[0] ^= 1  # Flip one bit

        # Verification should fail
        assert not verify_ed25519(message, bytes(tampered_sig), self.public_key)

    def test_timestamped_signature(self) -> None:
        """Test timestamped signatures."""
        message = b"time-sensitive data"
        signature, timestamp = create_timestamped_signature(
            message,
            self.private_key
        )

        # Should verify within time window
        assert verify_timestamped_signature(
            message,
            signature,
            timestamp,
            self.public_key,
            max_age=timedelta(minutes=5)
        )
```

### Integration Testing

```python
def test_api_request_signing():
    """Test end-to-end API request signing."""
    # Create signed request
    headers = sign_api_request(
        method="POST",
        path="/api/data",
        body=b'{"key": "value"}',
        private_key=private_key
    )

    # Simulate server-side verification
    assert "X-Signature" in headers
    assert "X-Timestamp" in headers

    # Server would verify the signature
    # (implementation omitted for brevity)
```

## Next Steps

### Related Guides
- **[Key Generation](keys.md)**: Generate cryptographic keys for signing
- **[Certificates](certificates.md)**: X.509 certificates and PKI
- **[Basic Logging](../logging/basic-logging.md)**: Log signature operations

### Examples
- See `examples/crypto/03_digital_signatures.py` for signature examples
- See `examples/crypto/04_jwt_signing.py` for JWT patterns
- See `examples/production/06_api_signing.py` for API authentication

### API Reference
- **[Crypto Module](../../reference/provide/foundation/crypto/index.md)**: Complete crypto API
- **[Ed25519 Functions](../../reference/provide/foundation/crypto/ed25519.md)**: Ed25519 signatures
- **[RSA Functions](../../reference/provide/foundation/crypto/rsa.md)**: RSA signatures

---

**Tip**: Prefer Ed25519 signatures for new applications - they're faster and more secure than RSA while providing smaller signature sizes. Always verify signatures before trusting data, and include timestamps or nonces to prevent replay attacks.
