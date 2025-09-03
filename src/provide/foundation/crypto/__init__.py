"""Cryptographic utilities for Foundation.

Provides hashing, checksum verification, and other cryptographic operations.
"""

from provide.foundation.crypto.hashing import (
    hash_file,
    hash_data,
    hash_string,
    hash_stream,
)
from provide.foundation.crypto.checksums import (
    verify_file,
    verify_data,
    calculate_checksums,
    parse_checksum_file,
    write_checksum_file,
)
from provide.foundation.crypto.utils import (
    quick_hash,
    hash_name,
    compare_hash,
    format_hash,
)
from provide.foundation.crypto.algorithms import (
    SUPPORTED_ALGORITHMS,
    DEFAULT_ALGORITHM,
    get_hasher,
    validate_algorithm,
    is_secure_algorithm,
)

__all__ = [
    # Hashing functions
    "hash_file",
    "hash_data",
    "hash_string",
    "hash_stream",
    # Checksum functions
    "verify_file",
    "verify_data",
    "calculate_checksums",
    "parse_checksum_file",
    "write_checksum_file",
    # Utility functions
    "quick_hash",
    "hash_name",
    "compare_hash",
    "format_hash",
    # Algorithm management
    "SUPPORTED_ALGORITHMS",
    "DEFAULT_ALGORITHM",
    "get_hasher",
    "validate_algorithm",
    "is_secure_algorithm",
]