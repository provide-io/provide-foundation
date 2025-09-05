# Crypto

::: provide.foundation.crypto

## Overview

The crypto module provides secure cryptographic utilities for hashing, checksums, and data verification. It supports multiple algorithms and provides both low-level and high-level interfaces for common cryptographic operations.

## Key Features

- **Multiple Hash Algorithms**: Support for SHA-256, SHA-512, Blake2b, and more
- **Secure Defaults**: Automatically uses secure algorithms (SHA-256 by default)
- **File and Data Hashing**: Hash files, strings, byte data, or streams
- **Checksum Verification**: Create and verify checksum files
- **Stream Processing**: Memory-efficient hashing of large files

## Quick Start

```python
from provide.foundation.crypto import hash_string, verify_file, calculate_checksums

# Hash a string
digest = hash_string("hello world")
print(f"Hash: {digest}")

# Verify file integrity
is_valid = verify_file("myfile.txt", "expected_hash_here")

# Calculate checksums for multiple files
checksums = calculate_checksums(["file1.txt", "file2.txt"])
```

## API Reference

### Hash Functions

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

#### `hash_file(filepath, algorithm="sha256")`

Hash a file using the specified algorithm.

**Parameters:**
- `filepath` (str | Path): Path to the file to hash
- `algorithm` (str, optional): Hash algorithm to use (default: "sha256")

**Returns:**
- `str`: Hexadecimal digest of the file hash

**Example:**
```python
from provide.foundation.crypto import hash_file

digest = hash_file("myfile.txt")
print(f"File hash: {digest}")
```

#### `hash_data(data, algorithm="sha256")`

Hash bytes data using the specified algorithm.

**Parameters:**
- `data` (bytes): The bytes to hash
- `algorithm` (str, optional): Hash algorithm to use (default: "sha256")

**Returns:**
- `str`: Hexadecimal digest of the hash

**Example:**
```python
from provide.foundation.crypto import hash_data

data = b"binary data here"
digest = hash_data(data)
```

#### `hash_stream(stream, algorithm="sha256")`

Hash data from a stream (file-like object) using the specified algorithm.

**Parameters:**
- `stream`: File-like object to read from
- `algorithm` (str, optional): Hash algorithm to use (default: "sha256")

**Returns:**
- `str`: Hexadecimal digest of the hash

**Example:**
```python
from provide.foundation.crypto import hash_stream
import io

stream = io.BytesIO(b"stream data")
digest = hash_stream(stream)
```

### Checksum Functions

#### `verify_file(filepath, expected_hash, algorithm="sha256")`

Verify a file's integrity against an expected hash.

**Parameters:**
- `filepath` (str | Path): Path to the file to verify
- `expected_hash` (str): Expected hash digest (hexadecimal)
- `algorithm` (str, optional): Hash algorithm to use (default: "sha256")

**Returns:**
- `bool`: True if the file matches the expected hash

**Example:**
```python
from provide.foundation.crypto import verify_file

# Verify file integrity
is_valid = verify_file("document.pdf", "a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3")
if is_valid:
    print("File is valid")
else:
    print("File has been corrupted or modified")
```

#### `verify_data(data, expected_hash, algorithm="sha256")`

Verify data integrity against an expected hash.

**Parameters:**
- `data` (bytes): The data to verify
- `expected_hash` (str): Expected hash digest (hexadecimal)
- `algorithm` (str, optional): Hash algorithm to use (default: "sha256")

**Returns:**
- `bool`: True if the data matches the expected hash

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