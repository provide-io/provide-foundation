# Cryptographic Utilities API

The `provide.foundation.crypto` module provides comprehensive cryptographic operations including hashing, digital signatures, key generation, and X.509 certificate management.

## Overview

The crypto module is organized around common use cases:
- **File & Data Hashing** - SHA-256, SHA-512, Blake2b with verification
- **Digital Signatures** - Ed25519, ECDSA, RSA signing and verification
- **Key Generation** - Secure key pair generation for multiple algorithms
- **X.509 Certificates** - Certificate creation and management
- **Checksum Operations** - Multi-algorithm checksum files

## Key Features

- **Comprehensive Hashing**: SHA-256, SHA-512, Blake2b with file/stream support
- **Digital Signatures**: Ed25519, ECDSA, RSA signing and verification
- **Key Management**: Secure key generation for multiple algorithms
- **X.509 Certificates**: Self-signed and CA certificate creation
- **Checksum Operations**: Multi-algorithm checksum file support
- **Security Focus**: Secure defaults with algorithm validation
- **Performance**: Memory-efficient streaming for large files

## Quick Start

```python
from provide.foundation.crypto import hash_file, verify_file, sign_data

# Hash a file
result = hash_file("document.pdf")
print(f"SHA-256: {result.hex_digest}")

# Verify against known hash
is_valid = verify_file("document.pdf", "abc123...")

# Digital signatures
from provide.foundation.crypto import generate_signing_keypair
private_key, public_key = generate_signing_keypair("ed25519")
signature = sign_data(b"message", private_key)
```

## API Reference

## Core Functions

### File & Data Hashing

#### `hash_file(path, algorithm="sha256")`

Calculate hash of a file with memory-efficient streaming.

**Parameters:**
- `path` (str | Path): Path to file
- `algorithm` (str): Hash algorithm ("sha256", "sha512", "blake2b")

**Returns:** `HashResult` with hex_digest, algorithm, and metadata

```python
from provide.foundation.crypto import hash_file

result = hash_file("large_file.zip", algorithm="sha512")
print(f"Hash: {result.hex_digest}")
print(f"Size: {result.file_size} bytes")
```

#### `hash_data(data, algorithm="sha256")`

Hash bytes or string data directly.

```python
from provide.foundation.crypto import hash_data

# Hash bytes
result = hash_data(b"Hello, World!")

# Hash string (auto-encoded as UTF-8)
result = hash_data("Hello, World!")
print(result.hex_digest)
```

#### `hash_stream(stream, algorithm="sha256")`

Hash data from a stream (file-like object).

```python
import io
from provide.foundation.crypto import hash_stream

stream = io.BytesIO(b"stream data")
result = hash_stream(stream)
```

#### `hash_string(data, algorithm="sha256")`

Hash a string using the specified algorithm.

**Parameters:**
- `data` (str): The string to hash
- `algorithm` (str, optional): Hash algorithm to use (default: "sha256")

**Returns:**
- `str`: Hexadecimal digest of the hash

**Example:**
```python
from provide.foundation.crypto import hash_string

# Basic usage
digest = hash_string("hello")
print(digest)  # a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3

# Using different algorithm
digest = hash_string("hello", algorithm="blake2b")
```

### File Verification

#### `verify_file(path, expected_hash, algorithm="sha256")`

Verify a file against an expected hash.

**Returns:** `bool` - True if hash matches

```python
from provide.foundation.crypto import verify_file

is_valid = verify_file("document.pdf", "abc123...", "sha256")
if is_valid:
    print("File integrity verified")
```

#### `verify_data(data, expected_hash, algorithm="sha256")`

Verify data against an expected hash.

```python
from provide.foundation.crypto import verify_data

is_valid = verify_data(b"data", "expected_hash")
```

### Digital Signatures

#### `generate_signing_keypair(algorithm="ed25519")`

Generate a key pair for digital signatures.

**Parameters:**
- `algorithm` (str): "ed25519", "ecdsa", or "rsa"

**Returns:** Tuple of (private_key, public_key)

```python
from provide.foundation.crypto import generate_signing_keypair

# Ed25519 (recommended - fast, secure)
private_key, public_key = generate_signing_keypair("ed25519")

# ECDSA with P-256 curve
private_key, public_key = generate_signing_keypair("ecdsa")

# RSA with 2048-bit key
private_key, public_key = generate_signing_keypair("rsa")
```

#### `sign_data(data, private_key, algorithm=None)`

Sign data with a private key.

```python
from provide.foundation.crypto import sign_data

signature = sign_data(b"message to sign", private_key)
```

#### `verify_signature(data, signature, public_key, algorithm=None)`

Verify a signature against data and public key.

**Returns:** `bool` - True if signature is valid

```python
from provide.foundation.crypto import verify_signature

is_valid = verify_signature(b"message", signature, public_key)
```

### X.509 Certificates

#### `create_self_signed(common_name, **kwargs)`

Create a self-signed X.509 certificate.

**Parameters:**
- `common_name` (str): Certificate subject common name
- `key_size` (int): RSA key size (default: 2048)
- `valid_days` (int): Certificate validity period (default: 365)
- `san_list` (list[str]): Subject Alternative Names

**Returns:** Tuple of (certificate, private_key)

```python
from provide.foundation.crypto import create_self_signed

cert, key = create_self_signed(
    "example.com",
    key_size=2048,
    valid_days=365,
    san_list=["www.example.com", "api.example.com"]
)

# Save certificate
with open("cert.pem", "wb") as f:
    f.write(cert.certificate_bytes)
```

#### `create_ca(common_name, **kwargs)`

Create a Certificate Authority (CA) certificate.

```python
from provide.foundation.crypto import create_ca

ca_cert, ca_key = create_ca("My CA", valid_days=3650)
```

### Key Generation

#### `generate_keypair(algorithm, **kwargs)`

General key pair generation function.

```python
from provide.foundation.crypto import generate_keypair

# RSA key pair
private_key, public_key = generate_keypair("rsa", key_size=2048)

# ECDSA key pair
private_key, public_key = generate_keypair("ecdsa", curve="secp256r1")

# Ed25519 key pair
private_key, public_key = generate_keypair("ed25519")
```

#### Specialized Key Generation

```python
from provide.foundation.crypto import (
    generate_rsa_keypair,
    generate_ec_keypair,
    generate_ed25519_keypair,
    generate_tls_keypair
)

# RSA for encryption/signing
rsa_private, rsa_public = generate_rsa_keypair(key_size=2048)

# Elliptic curve for signing
ec_private, ec_public = generate_ec_keypair(curve="secp256r1")

# Ed25519 for signing (fastest, most secure)
ed_private, ed_public = generate_ed25519_keypair()

# TLS-compatible key pair
tls_private, tls_public = generate_tls_keypair()
```

### Checksum Operations

#### `calculate_checksums(filepaths, algorithm="sha256")`

Calculate checksums for multiple files.

**Parameters:**
- `filepaths` (list[str | Path]): List of file paths to process
- `algorithm` (str, optional): Hash algorithm to use (default: "sha256")

**Returns:**
- `dict[str, str]`: Mapping of file paths to their hash digests

**Example:**
```python
from provide.foundation.crypto import calculate_checksums

files = ["config.json", "data.txt", "script.py"]
checksums = calculate_checksums(files)

for filepath, digest in checksums.items():
    print(f"{filepath}: {digest}")
```

#### `write_checksum_file(checksums, output_path, algorithm="sha256")`

Write checksums to a checksum file in standard format.

**Parameters:**
- `checksums` (dict[str, str]): Mapping of file paths to digests
- `output_path` (str | Path): Path where to write the checksum file
- `algorithm` (str, optional): Algorithm name to include in file

**Example:**
```python
from provide.foundation.crypto import calculate_checksums, write_checksum_file

# Calculate checksums and save to file
checksums = calculate_checksums(["file1.txt", "file2.txt"])
write_checksum_file(checksums, "checksums.sha256")
```

#### `parse_checksum_file(checksum_file)`

Parse a checksum file and return the checksums.

**Parameters:**
- `checksum_file` (str | Path): Path to the checksum file

**Returns:**
- `dict[str, str]`: Mapping of file paths to their expected digests

**Example:**
```python
from provide.foundation.crypto import parse_checksum_file

# Parse existing checksum file
expected = parse_checksum_file("checksums.sha256")
print(expected)
```

### Algorithm Management

#### `validate_algorithm(algorithm)`

Validate that an algorithm is supported.

**Parameters:**
- `algorithm` (str): Algorithm name to validate

**Raises:**
- `ValueError`: If the algorithm is not supported

#### `is_secure_algorithm(algorithm)`

Check if an algorithm is considered cryptographically secure.

**Parameters:**
- `algorithm` (str): Algorithm name to check

**Returns:**
- `bool`: True if the algorithm is secure

**Example:**
```python
from provide.foundation.crypto import is_secure_algorithm

print(is_secure_algorithm("sha256"))    # True
print(is_secure_algorithm("md5"))       # False
```

#### `get_hasher(algorithm="sha256")`

Get a hasher instance for the specified algorithm.

**Parameters:**
- `algorithm` (str, optional): Algorithm name (default: "sha256")

**Returns:**
- Hash object from hashlib

### Utility Functions

#### `quick_hash(data, length=8)`

Generate a short hash for debugging or display purposes.

**Parameters:**
- `data` (str | bytes): Data to hash
- `length` (int, optional): Length of output hash (default: 8)

**Returns:**
- `str`: Short hash digest

**Example:**
```python
from provide.foundation.crypto import quick_hash

short_hash = quick_hash("some data", length=6)
print(short_hash)  # e.g., "a1b2c3"
```

#### `compare_hash(hash1, hash2)`

Securely compare two hash digests using constant-time comparison.

**Parameters:**
- `hash1` (str): First hash digest
- `hash2` (str): Second hash digest

**Returns:**
- `bool`: True if hashes match

#### `format_hash(digest, algorithm)`

Format a hash digest with algorithm prefix.

**Parameters:**
- `digest` (str): Hash digest
- `algorithm` (str): Algorithm name

**Returns:**
- `str`: Formatted hash string

## Algorithm Support

| Algorithm | Status | Secure | Notes |
|-----------|---------|---------|-------|
| `sha256` | ✅ Supported | ✅ Yes | Default, recommended |
| `sha512` | ✅ Supported | ✅ Yes | Slower but more secure |
| `blake2b` | ✅ Supported | ✅ Yes | Fast and secure |
| `sha1` | ✅ Supported | ❌ No | Deprecated, avoid |
| `md5` | ✅ Supported | ❌ No | Insecure, avoid |

## Constants

- `DEFAULT_ALGORITHM`: The default algorithm used ("sha256")
- `SUPPORTED_ALGORITHMS`: Set of all supported algorithm names

## Security Best Practices

1. **Use Secure Algorithms**: Prefer SHA-256, SHA-512, or Blake2b
2. **Verify Important Data**: Always verify checksums for critical files
3. **Constant-Time Comparison**: Use `compare_hash()` for hash verification
4. **Handle Errors**: Wrap crypto operations in try-catch blocks
5. **Stream Large Files**: Use `hash_stream()` for memory efficiency

## Error Handling

All functions may raise:
- `ValueError`: For invalid algorithms or parameters
- `FileNotFoundError`: When specified files don't exist
- `IOError`: For file reading/writing errors
- `OSError`: For system-level errors

## Examples

### Complete File Verification Workflow

```python
from provide.foundation.crypto import calculate_checksums, write_checksum_file, parse_checksum_file, verify_file

# Step 1: Calculate checksums for your files
files = ["config.json", "data.csv", "script.py"]
checksums = calculate_checksums(files, algorithm="sha256")

# Step 2: Save checksums to file
write_checksum_file(checksums, "project.sha256")

# Step 3: Later, verify file integrity
expected_checksums = parse_checksum_file("project.sha256")
for filepath, expected_hash in expected_checksums.items():
    is_valid = verify_file(filepath, expected_hash)
    if is_valid:
        print(f"✅ {filepath} is valid")
    else:
        print(f"❌ {filepath} has been modified")
```

### Memory-Efficient Large File Hashing

```python
from provide.foundation.crypto import hash_stream

def hash_large_file(filepath):
    """Hash a large file without loading it entirely into memory."""
    with open(filepath, "rb") as f:
        return hash_stream(f)

# Hash a multi-gigabyte file efficiently  
large_file_hash = hash_large_file("database_dump.sql")
```

## See Also

- [File Module](../file/index.md) - For secure file operations
- [Utils Guide](../../guide/utilities/index.md) - General utility patterns
- [Security Guide](../../guide/security/index.md) - Security best practices