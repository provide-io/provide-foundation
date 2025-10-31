#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from __future__ import annotations

import hashlib
from typing import Any

from provide.foundation.errors.config import ValidationError

"""Hash algorithm management and validation."""

SUPPORTED_ALGORITHMS = {
    "md5",
    "sha1",
    "sha224",
    "sha256",
    "sha384",
    "sha512",
    "sha3_224",
    "sha3_256",
    "sha3_384",
    "sha3_512",
    "blake2b",
    "blake2s",
}

# Default algorithm for general use
DEFAULT_ALGORITHM = "sha256"

# Algorithms considered cryptographically secure
SECURE_ALGORITHMS = {
    "sha256",
    "sha384",
    "sha512",
    "sha3_256",
    "sha3_384",
    "sha3_512",
    "blake2b",
    "blake2s",
}


def validate_algorithm(algorithm: str) -> None:
    """Validate that a hash algorithm is supported.

    Args:
        algorithm: Hash algorithm name

    Raises:
        ValidationError: If algorithm is not supported

    """
    if algorithm.lower() not in SUPPORTED_ALGORITHMS:
        raise ValidationError(
            f"Unsupported hash algorithm: {algorithm}",
            field="algorithm",
            value=algorithm,
            rule="must be one of: " + ", ".join(sorted(SUPPORTED_ALGORITHMS)),
        )


def get_hasher(algorithm: str) -> Any:
    """Get a hash object for the specified algorithm.

    Args:
        algorithm: Hash algorithm name

    Returns:
        Hash object from hashlib

    Raises:
        ValidationError: If algorithm is not supported

    """
    validate_algorithm(algorithm)

    algorithm_lower = algorithm.lower()

    # Handle special cases
    if algorithm_lower.startswith("sha3_"):
        # sha3_256 -> sha3_256 (hashlib uses underscores)
        return hashlib.new(algorithm_lower)
    if algorithm_lower.startswith("blake2"):
        # blake2b, blake2s
        return hashlib.new(algorithm_lower)
    # Standard algorithms (md5, sha1, sha256, etc.)
    return hashlib.new(algorithm_lower)


def is_secure_algorithm(algorithm: str) -> bool:
    """Check if an algorithm is considered cryptographically secure.

    Args:
        algorithm: Hash algorithm name

    Returns:
        True if algorithm is secure, False otherwise

    """
    return algorithm.lower() in SECURE_ALGORITHMS


def get_digest_size(algorithm: str) -> int:
    """Get the digest size in bytes for an algorithm.

    Args:
        algorithm: Hash algorithm name

    Returns:
        Digest size in bytes

    Raises:
        ValidationError: If algorithm is not supported

    """
    hasher = get_hasher(algorithm)
    return hasher.digest_size


# 🧱🏗️🔚
