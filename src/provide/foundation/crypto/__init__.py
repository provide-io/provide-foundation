"""Cryptographic utilities for Foundation.

Provides hashing, checksum verification, and other cryptographic operations.
"""

from provide.foundation.crypto.algorithms import (
    DEFAULT_ALGORITHM,
    SUPPORTED_ALGORITHMS,
    get_hasher,
    is_secure_algorithm,
    validate_algorithm,
)
from provide.foundation.crypto.checksums import (
    calculate_checksums,
    parse_checksum_file,
    verify_data,
    verify_file,
    write_checksum_file,
)
from provide.foundation.crypto.hashing import (
    hash_data,
    hash_file,
    hash_stream,
    hash_string,
)
from provide.foundation.crypto.utils import (
    compare_hash,
    format_hash,
    hash_name,
    quick_hash,
)

__all__ = [
    "DEFAULT_ALGORITHM",
    # Algorithm management
    "SUPPORTED_ALGORITHMS",
    "calculate_checksums",
    "compare_hash",
    "format_hash",
    "get_hasher",
    "hash_data",
    # Hashing functions
    "hash_file",
    "hash_name",
    "hash_stream",
    "hash_string",
    "is_secure_algorithm",
    "parse_checksum_file",
    # Utility functions
    "quick_hash",
    "validate_algorithm",
    "verify_data",
    # Checksum functions
    "verify_file",
    "write_checksum_file",
]
