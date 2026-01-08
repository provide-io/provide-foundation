# Key Generation & Management

Learn how to generate, store, and manage cryptographic keys with Foundation's secure key management utilities.

## Overview

Foundation provides comprehensive utilities for generating and managing cryptographic keys with secure defaults. The crypto module supports modern elliptic curve cryptography (Ed25519, ECDSA) and traditional RSA keys, with built-in security best practices.

**What you'll learn:**
- Generate Ed25519, RSA, and ECDSA keypairs
- Store keys securely with proper file permissions
- Convert between key formats (PEM, DER, raw bytes)
- Implement key rotation strategies
- Use environment-based key management
- Test key generation code
- Apply security best practices

**Key Features:**
- 🔐 **Secure Defaults**: All keys generated with cryptographically secure randomness
- 🎯 **Modern Algorithms**: Ed25519 (recommended), ECDSA, RSA support
- 💾 **Safe Storage**: Atomic writes with restricted file permissions
- 🔄 **Format Flexibility**: PEM, DER, and raw byte formats
- ⚡ **High Performance**: Fast key generation and operations
- 🧪 **Testable**: Easy to mock and test key operations

## Prerequisites

```bash
# Core cryptography support (included by default)
uv add provide-foundation

# For advanced crypto features (optional)
uv add provide-foundation[crypto]
```

## Basic Key Generation

### Ed25519 Keys (Recommended)

Ed25519 provides the best performance and security for most use cases:

```python
from provide.foundation.crypto import generate_ed25519_keypair
from provide.foundation import logger

# Generate a new keypair
public_key, private_key = generate_ed25519_keypair()

logger.info(
    "keypair_generated",
    algorithm="ed25519",
    public_key_size=len(public_key),
    private_key_size=len(private_key)
)

# Keys are returned as bytes
print(f"Public key (hex): {public_key.hex()}")
print(f"Private key (hex): {private_key.hex()}")
```

### RSA Keys

RSA keys are widely supported but slower than Ed25519:

```python
from provide.foundation.crypto import generate_rsa_keypair

# Generate 2048-bit RSA keypair (minimum recommended)
public_key, private_key = generate_rsa_keypair(key_size=2048)

# For higher security, use 4096-bit keys
public_key_4k, private_key_4k = generate_rsa_keypair(key_size=4096)

logger.info(
    "rsa_keypair_generated",
    key_size=4096,
    public_key_format="PKCS#1 PEM"
)
```

### ECDSA Keys

ECDSA provides a good balance of security and compatibility:

```python
from provide.foundation.crypto import generate_ecdsa_keypair

# Generate P-256 ECDSA keypair
public_key, private_key = generate_ecdsa_keypair(curve="P-256")

# Other supported curves
p384_pub, p384_priv = generate_ecdsa_keypair(curve="P-384")  # Higher security
p521_pub, p521_priv = generate_ecdsa_keypair(curve="P-521")  # Maximum security
```

## Secure Key Storage

### Save Keys with Proper Permissions

Always save private keys with restricted file permissions:

```python
from pathlib import Path
from provide.foundation.file import atomic_write
from provide.foundation import logger

def save_keypair(
    public_key: bytes,
    private_key: bytes,
    key_dir: Path
) -> tuple[Path, Path]:
    """Save a keypair securely to disk."""
    key_dir.mkdir(parents=True, exist_ok=True)

    # Save private key with owner-only permissions
    private_path = key_dir / "private_key.pem"
    atomic_write(
        path=private_path,
        content=private_key,
        permissions=0o600  # -rw-------
    )

    # Save public key with standard permissions
    public_path = key_dir / "public_key.pem"
    atomic_write(
        path=public_path,
        content=public_key,
        permissions=0o644  # -rw-r--r--
    )

    logger.info(
        "keypair_saved",
        private_path=str(private_path),
        public_path=str(public_path),
        private_permissions="0600"
    )

    return public_path, private_path

# Usage
public_key, private_key = generate_ed25519_keypair()
save_keypair(public_key, private_key, Path("~/.ssh/myapp").expanduser())
```

### Load Keys from Files

```python
from pathlib import Path
from provide.foundation import logger

def load_keypair(key_dir: Path) -> tuple[bytes, bytes]:
    """Load a keypair from disk."""
    private_path = key_dir / "private_key.pem"
    public_path = key_dir / "public_key.pem"

    # Verify permissions before loading private key
    private_stat = private_path.stat()
    if private_stat.st_mode & 0o077:
        logger.warning(
            "insecure_private_key_permissions",
            path=str(private_path),
            permissions=oct(private_stat.st_mode & 0o777)
        )

    private_key = private_path.read_bytes()
    public_key = public_path.read_bytes()

    logger.debug("keypair_loaded", public_path=str(public_path))

    return public_key, private_key
```

## Advanced Key Management

### Environment-Based Key Loading

Load keys from environment variables for containerized deployments:

```python
import os
from base64 import b64decode
from provide.foundation.utils.environment import get_str, require
from provide.foundation import logger

def load_keys_from_env() -> tuple[bytes, bytes]:
    """Load keys from environment variables."""
    # Support both direct value and file:// prefix
    public_key_value = require("PUBLIC_KEY")
    private_key_value = require("PRIVATE_KEY")

    # Decode base64-encoded keys
    public_key = b64decode(public_key_value)
    private_key = b64decode(private_key_value)

    logger.info("keys_loaded_from_environment")

    return public_key, private_key

# Usage with file:// prefix (reads from secret files)
# export PUBLIC_KEY="file:///run/secrets/public_key"
# export PRIVATE_KEY="file:///run/secrets/private_key"
```

### Key Format Conversion

Convert between PEM, DER, and raw formats:

```python
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ed25519
from provide.foundation import logger

def convert_key_formats(private_key_bytes: bytes) -> dict[str, bytes]:
    """Convert a key to multiple formats."""
    # Load the private key
    private_key = ed25519.Ed25519PrivateKey.from_private_bytes(private_key_bytes)

    # PEM format (text-based, widely compatible)
    pem_private = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )

    # DER format (binary, more compact)
    der_private = private_key.private_bytes(
        encoding=serialization.Encoding.DER,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )

    # Raw format (32 bytes for Ed25519)
    raw_private = private_key.private_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PrivateFormat.Raw,
        encryption_algorithm=serialization.NoEncryption()
    )

    logger.debug(
        "key_formats_generated",
        pem_size=len(pem_private),
        der_size=len(der_private),
        raw_size=len(raw_private)
    )

    return {
        "pem": pem_private,
        "der": der_private,
        "raw": raw_private
    }
```

### Encrypted Private Key Storage

Protect private keys with password-based encryption:

```python
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from provide.foundation.utils.environment import get_str
from provide.foundation import logger

def save_encrypted_private_key(
    private_key: bytes,
    password: str,
    output_path: Path
) -> None:
    """Save a private key encrypted with a password."""
    from provide.foundation.file import atomic_write

    # Convert bytes to key object (example for RSA)
    key_obj = serialization.load_pem_private_key(
        private_key,
        password=None
    )

    # Encrypt with password
    encrypted_pem = key_obj.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.BestAvailableEncryption(
            password.encode()
        )
    )

    # Save with restricted permissions
    atomic_write(
        path=output_path,
        content=encrypted_pem,
        permissions=0o600
    )

    logger.info(
        "encrypted_private_key_saved",
        path=str(output_path),
        encryption="PKCS8"
    )

# Usage
password = get_str("KEY_PASSWORD", required=True)
save_encrypted_private_key(private_key, password, Path("encrypted_key.pem"))
```

## Key Rotation Patterns

### Automatic Key Rotation

Implement periodic key rotation for enhanced security:

```python
from datetime import datetime, timedelta
from pathlib import Path
from provide.foundation.crypto import generate_ed25519_keypair
from provide.foundation.file import atomic_write
from provide.foundation import logger

class KeyRotationManager:
    """Manage automatic key rotation."""

    def __init__(self, key_dir: Path, rotation_days: int = 90):
        self.key_dir = key_dir
        self.rotation_days = rotation_days
        self.key_dir.mkdir(parents=True, exist_ok=True)

    def should_rotate(self) -> bool:
        """Check if keys should be rotated."""
        current_key = self.key_dir / "private_key.pem"

        if not current_key.exists():
            return True

        # Check key age
        key_age = datetime.now() - datetime.fromtimestamp(
            current_key.stat().st_mtime
        )

        should_rotate = key_age > timedelta(days=self.rotation_days)

        logger.debug(
            "key_rotation_check",
            key_age_days=key_age.days,
            rotation_threshold=self.rotation_days,
            should_rotate=should_rotate
        )

        return should_rotate

    def rotate_keys(self) -> tuple[bytes, bytes]:
        """Generate new keys and archive old ones."""
        # Archive existing keys
        current_private = self.key_dir / "private_key.pem"
        current_public = self.key_dir / "public_key.pem"

        if current_private.exists():
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            archive_dir = self.key_dir / "archive"
            archive_dir.mkdir(exist_ok=True)

            current_private.rename(
                archive_dir / f"private_key_{timestamp}.pem"
            )
            current_public.rename(
                archive_dir / f"public_key_{timestamp}.pem"
            )

            logger.info("old_keys_archived", timestamp=timestamp)

        # Generate new keys
        public_key, private_key = generate_ed25519_keypair()

        # Save new keys
        atomic_write(
            path=current_private,
            content=private_key,
            permissions=0o600
        )
        atomic_write(
            path=current_public,
            content=public_key,
            permissions=0o644
        )

        logger.info("keys_rotated", key_dir=str(self.key_dir))

        return public_key, private_key

# Usage
manager = KeyRotationManager(Path("~/.ssh/myapp").expanduser())
if manager.should_rotate():
    public_key, private_key = manager.rotate_keys()
```

### Multi-Key Management

Maintain multiple keys for different purposes:

```python
from enum import Enum
from pathlib import Path
from provide.foundation.crypto import generate_ed25519_keypair
from provide.foundation import logger

class KeyPurpose(Enum):
    """Key usage purposes."""
    SIGNING = "signing"
    ENCRYPTION = "encryption"
    AUTHENTICATION = "authentication"

class MultiKeyManager:
    """Manage multiple keys by purpose."""

    def __init__(self, key_dir: Path):
        self.key_dir = key_dir
        self.key_dir.mkdir(parents=True, exist_ok=True)

    def get_key_path(self, purpose: KeyPurpose, key_type: str) -> Path:
        """Get path for a specific key."""
        return self.key_dir / f"{purpose.value}_{key_type}.pem"

    def generate_keys(self, purpose: KeyPurpose) -> tuple[bytes, bytes]:
        """Generate keys for a specific purpose."""
        public_key, private_key = generate_ed25519_keypair()

        # Save keys
        private_path = self.get_key_path(purpose, "private")
        public_path = self.get_key_path(purpose, "public")

        from provide.foundation.file import atomic_write
        atomic_write(path=private_path, content=private_key, permissions=0o600)
        atomic_write(path=public_path, content=public_key, permissions=0o644)

        logger.info("purpose_keys_generated", purpose=purpose.value)

        return public_key, private_key

    def load_keys(self, purpose: KeyPurpose) -> tuple[bytes, bytes]:
        """Load keys for a specific purpose."""
        private_path = self.get_key_path(purpose, "private")
        public_path = self.get_key_path(purpose, "public")

        if not private_path.exists():
            logger.info(
                "generating_missing_keys",
                purpose=purpose.value
            )
            return self.generate_keys(purpose)

        return public_path.read_bytes(), private_path.read_bytes()

# Usage
manager = MultiKeyManager(Path("~/.keys").expanduser())
signing_pub, signing_priv = manager.load_keys(KeyPurpose.SIGNING)
auth_pub, auth_priv = manager.load_keys(KeyPurpose.AUTHENTICATION)
```

## Common Patterns

### API Key Generation

Generate secure random API keys:

```python
import secrets
from base64 import urlsafe_b64encode
from provide.foundation import logger

def generate_api_key(prefix: str = "pk", length: int = 32) -> str:
    """Generate a secure API key."""
    # Generate cryptographically secure random bytes
    random_bytes = secrets.token_bytes(length)

    # Encode as URL-safe base64
    encoded = urlsafe_b64encode(random_bytes).decode().rstrip("=")

    # Add prefix for identification
    api_key = f"{prefix}_{encoded}"

    logger.info(
        "api_key_generated",
        prefix=prefix,
        length=len(api_key)
    )

    return api_key

# Usage
api_key = generate_api_key(prefix="prod", length=32)
print(f"API Key: {api_key}")
```

### SSH Key Generation

Generate SSH-compatible Ed25519 keys:

```python
from pathlib import Path
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ed25519
from provide.foundation.file import atomic_write
from provide.foundation import logger

def generate_ssh_keypair(
    key_path: Path,
    comment: str = ""
) -> tuple[Path, Path]:
    """Generate SSH-compatible Ed25519 keypair."""
    # Generate keypair
    private_key = ed25519.Ed25519PrivateKey.generate()
    public_key = private_key.public_key()

    # Format private key (OpenSSH format)
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.OpenSSH,
        encryption_algorithm=serialization.NoEncryption()
    )

    # Format public key (OpenSSH format)
    public_ssh = public_key.public_bytes(
        encoding=serialization.Encoding.OpenSSH,
        format=serialization.PublicFormat.OpenSSH
    )

    # Add comment if provided
    if comment:
        public_ssh = public_ssh + f" {comment}".encode()

    # Save keys
    private_path = key_path
    public_path = key_path.with_suffix(".pub")

    atomic_write(path=private_path, content=private_pem, permissions=0o600)
    atomic_write(path=public_path, content=public_ssh, permissions=0o644)

    logger.info(
        "ssh_keypair_generated",
        private_key=str(private_path),
        public_key=str(public_path)
    )

    return public_path, private_path

# Usage
ssh_key_path = Path("~/.ssh/id_ed25519_myapp").expanduser()
generate_ssh_keypair(ssh_key_path, comment="user@host")
```

### Deterministic Key Derivation

Derive keys from a master secret:

```python
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from provide.foundation import logger

def derive_key(
    master_secret: bytes,
    purpose: str,
    key_length: int = 32
) -> bytes:
    """Derive a key from a master secret using HKDF."""
    hkdf = HKDF(
        algorithm=hashes.SHA256(),
        length=key_length,
        salt=None,
        info=purpose.encode()
    )

    derived_key = hkdf.derive(master_secret)

    logger.debug(
        "key_derived",
        purpose=purpose,
        key_length=key_length
    )

    return derived_key

# Usage
master_secret = secrets.token_bytes(32)
signing_key = derive_key(master_secret, "signing-key-v1")
encryption_key = derive_key(master_secret, "encryption-key-v1")
```

## Best Practices

### ✅ DO: Use Modern Algorithms

```python
# ✅ GOOD: Use Ed25519 for new applications
from provide.foundation.crypto import generate_ed25519_keypair

public_key, private_key = generate_ed25519_keypair()
```

### ❌ DON'T: Use Small RSA Keys

```python
# ❌ BAD: RSA keys smaller than 2048 bits are insecure
public_key, private_key = generate_rsa_keypair(key_size=1024)  # Too small!

# ✅ GOOD: Use at least 2048-bit RSA, prefer 4096-bit
public_key, private_key = generate_rsa_keypair(key_size=4096)
```

### ✅ DO: Restrict Private Key Permissions

```python
# ✅ GOOD: Save private keys with 0600 permissions
from provide.foundation.file import atomic_write

atomic_write(
    path="private_key.pem",
    content=private_key,
    permissions=0o600  # Owner read/write only
)
```

### ❌ DON'T: Store Keys in Code

```python
# ❌ BAD: Hardcoded keys in source code
PRIVATE_KEY = b"-----BEGIN PRIVATE KEY-----\n..."  # Never do this!

# ✅ GOOD: Load from environment or secure storage
from provide.foundation.utils.environment import require

private_key = require("PRIVATE_KEY")  # From environment or file://
```

### ✅ DO: Rotate Keys Periodically

```python
# ✅ GOOD: Implement automatic key rotation
manager = KeyRotationManager(key_dir, rotation_days=90)
if manager.should_rotate():
    new_public, new_private = manager.rotate_keys()
```

### ❌ DON'T: Reuse Keys Across Purposes

```python
# ❌ BAD: Using same key for signing and encryption
signing_key = private_key
encryption_key = private_key  # Don't reuse!

# ✅ GOOD: Generate separate keys for different purposes
signing_pub, signing_priv = manager.load_keys(KeyPurpose.SIGNING)
encryption_pub, encryption_priv = manager.load_keys(KeyPurpose.ENCRYPTION)
```

### ✅ DO: Validate Key Permissions

```python
# ✅ GOOD: Check permissions before loading private keys
import stat

key_stat = key_path.stat()
if key_stat.st_mode & stat.S_IRWXG or key_stat.st_mode & stat.S_IRWXO:
    logger.error("insecure_key_permissions", path=str(key_path))
    raise PermissionError("Private key has insecure permissions")
```

### ❌ DON'T: Log Private Keys

```python
# ❌ BAD: Logging sensitive key material
logger.info("key_loaded", private_key=private_key.hex())  # NEVER!

# ✅ GOOD: Log only metadata
logger.info(
    "key_loaded",
    key_type="ed25519",
    key_size=len(private_key)
)
```

### ✅ DO: Use Secure Random Generation

```python
# ✅ GOOD: Use secrets module for randomness
import secrets

api_key = secrets.token_urlsafe(32)

# ❌ BAD: Don't use random module for crypto
import random
api_key = random.randbytes(32)  # Not cryptographically secure!
```

### ❌ DON'T: Store Unencrypted Keys in Version Control

```python
# ❌ BAD: Keys in git repository
# .gitignore should include:
# *.pem
# *.key
# *_key
# secrets/

# ✅ GOOD: Store key paths in config, keys in secure storage
config = {
    "private_key_path": "file:///run/secrets/app_private_key"
}
```

### ✅ DO: Archive Old Keys During Rotation

```python
# ✅ GOOD: Keep old keys for a grace period
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
old_key_path.rename(f"archive/private_key_{timestamp}.pem")

# Allow verification of old signatures during transition
```

### ❌ DON'T: Share Private Keys Between Environments

```python
# ❌ BAD: Same key for dev/staging/prod
key_path = Path("shared_key.pem")

# ✅ GOOD: Separate keys per environment
env = os.getenv("ENVIRONMENT", "dev")
key_path = Path(f"keys/{env}_private_key.pem")
```

### ✅ DO: Use Key Derivation for Related Keys

```python
# ✅ GOOD: Derive multiple keys from one master secret
master = secrets.token_bytes(32)
db_key = derive_key(master, "database-encryption")
api_key = derive_key(master, "api-signing")

# Only need to protect one master secret
```

### ❌ DON'T: Ignore Key Format Errors

```python
# ❌ BAD: Silently failing on invalid keys
try:
    key = load_key(path)
except Exception:
    key = generate_new_key()  # Masks real issues

# ✅ GOOD: Validate and fail fast
try:
    key = load_key(path)
except ValueError as e:
    logger.error("invalid_key_format", path=path, error=str(e))
    raise
```

### ✅ DO: Test Key Operations

```python
# ✅ GOOD: Verify key generation and loading
public_key, private_key = generate_ed25519_keypair()

# Test that keys can be used
from provide.foundation.crypto import sign_ed25519, verify_ed25519
message = b"test"
signature = sign_ed25519(message, private_key)
assert verify_ed25519(message, signature, public_key)
```

## Testing Key Generation

### Unit Testing

```python
import pytest
from pathlib import Path
from provide.foundation.crypto import generate_ed25519_keypair
from provide.foundation.file import atomic_write
from provide.testkit import FoundationTestCase

class TestKeyGeneration(FoundationTestCase):
    """Test key generation and management."""

    def setup_method(self) -> None:
        """Set up test fixtures."""
        super().setup_method()
        self.test_dir = Path("/tmp/test_keys")
        self.test_dir.mkdir(exist_ok=True)

    def teardown_method(self) -> None:
        """Clean up test files."""
        import shutil
        if self.test_dir.exists():
            shutil.rmtree(self.test_dir)
        super().teardown_method()

    def test_ed25519_generation(self) -> None:
        """Test Ed25519 keypair generation."""
        public_key, private_key = generate_ed25519_keypair()

        # Verify key sizes
        assert len(public_key) == 32
        assert len(private_key) == 32

        # Verify keys are different
        assert public_key != private_key

    def test_key_file_permissions(self) -> None:
        """Test that private keys have correct permissions."""
        public_key, private_key = generate_ed25519_keypair()

        private_path = self.test_dir / "private_key.pem"
        atomic_write(
            path=private_path,
            content=private_key,
            permissions=0o600
        )

        # Verify permissions
        import stat
        mode = private_path.stat().st_mode
        assert stat.S_IMODE(mode) == 0o600

    def test_key_rotation(self) -> None:
        """Test key rotation manager."""
        manager = KeyRotationManager(self.test_dir, rotation_days=0)

        # Should rotate on first run
        assert manager.should_rotate()

        # Generate keys
        pub1, priv1 = manager.rotate_keys()

        # Should not rotate immediately
        assert not manager.should_rotate()
```

### Mocking Key Generation

```python
from unittest.mock import patch

def test_with_mock_keys():
    """Test using mocked key generation."""
    mock_public = b"mock_public_key_32bytes_long!!!!"
    mock_private = b"mock_private_key_32bytes_long!!"

    with patch("provide.foundation.crypto.generate_ed25519_keypair") as mock_gen:
        mock_gen.return_value = (mock_public, mock_private)

        # Your test code here
        public, private = generate_ed25519_keypair()
        assert public == mock_public
        assert private == mock_private
```

## Next Steps

### Related Guides
- **[Signing & Verification](signing.md)**: Use keys to sign and verify data
- **[Certificates](certificates.md)**: Generate X.509 certificates from keys
- **[Basic Logging](../logging/basic-logging.md)**: Log key management operations

### Examples
- See `examples/crypto/01_key_generation.py` for key generation examples
- See `examples/crypto/02_key_rotation.py` for rotation patterns
- See `examples/production/05_secret_management.py` for production key management

### API Reference
- **[Crypto Module](../../reference/provide/foundation/crypto/index.md)**: Complete crypto API
- **[File Operations](../../reference/provide/foundation/file/index.md)**: Atomic file writes

---

**Tip**: Prefer Ed25519 for new applications - it's faster, more secure, and has smaller key sizes than RSA. Always store private keys with 0600 permissions and never commit them to version control.
