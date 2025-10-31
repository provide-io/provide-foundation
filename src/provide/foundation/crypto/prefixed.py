#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from __future__ import annotations

from provide.foundation.crypto.algorithms import DEFAULT_ALGORITHM, validate_algorithm
from provide.foundation.crypto.hashing import hash_data
from provide.foundation.logger import get_logger

"""Prefixed checksum format (algorithm:hexvalue) for self-describing checksums."""

log = get_logger(__name__)


def format_checksum(data: bytes, algorithm: str = DEFAULT_ALGORITHM) -> str:
    """Calculate checksum with algorithm prefix.

    Returns checksums in the format "algorithm:hexdigest" (e.g., "sha256:abc123...").
    This format enables self-describing checksums that include the algorithm used.

    Args:
        data: Data to checksum
        algorithm: Hash algorithm (sha256, sha512, blake2b, blake2s, md5, adler32)

    Returns:
        Prefixed checksum string (e.g., "sha256:abc123...")

    Raises:
        ValueError: If algorithm is not supported

    Example:
        >>> data = b"Hello, World!"
        >>> format_checksum(data, "sha256")
        'sha256:dffd6021bb2bd5b0af676290809ec3a53191dd81c7f70a4b28688a362182986f'
        >>> format_checksum(data, "adler32")
        'adler32:1c49043e'

    """
    if algorithm == "adler32":
        # Special case for adler32 using zlib
        import zlib

        checksum = zlib.adler32(data) & 0xFFFFFFFF
        result = f"adler32:{checksum:08x}"
        log.debug(
            "🔐 Calculated adler32 checksum",
            size=len(data),
            checksum=result,
        )
        return result

    # Use standard hashing for other algorithms
    validate_algorithm(algorithm)
    digest = hash_data(data, algorithm)
    result = f"{algorithm}:{digest}"

    log.debug(
        "🔐 Calculated prefixed checksum",
        algorithm=algorithm,
        size=len(data),
        checksum=result[:40] + "...",
    )

    return result


def parse_checksum(checksum_str: str) -> tuple[str, str]:
    """Parse algorithm and value from a prefixed checksum string.

    Requires prefixed format ("algorithm:hexvalue"). This enables validation
    of both the algorithm and the checksum value.

    Args:
        checksum_str: Prefixed checksum string

    Returns:
        Tuple of (algorithm, hex_value)

    Raises:
        ValueError: If checksum format is invalid or algorithm is unsupported

    Example:
        >>> parse_checksum("sha256:abc123")
        ('sha256', 'abc123')
        >>> parse_checksum("invalid")
        ValueError: Checksum must use prefixed format (algorithm:value)

    """
    if not checksum_str:
        raise ValueError("Empty checksum string")

    if ":" not in checksum_str:
        raise ValueError(f"Checksum must use prefixed format (algorithm:value): {checksum_str}")

    parts = checksum_str.split(":", 1)
    if len(parts) != 2:
        raise ValueError(f"Invalid checksum format: {checksum_str}")

    algorithm, value = parts

    # Validate algorithm
    supported_algorithms = ["sha256", "sha512", "blake2b", "blake2s", "md5", "adler32"]
    if algorithm not in supported_algorithms:
        raise ValueError(
            f"Unknown checksum algorithm: {algorithm}. Supported: {', '.join(supported_algorithms)}"
        )

    log.debug(
        "📋 Parsed prefixed checksum",
        algorithm=algorithm,
        value=value[:16] + "...",
    )

    return algorithm, value


def verify_checksum(data: bytes, checksum_str: str) -> bool:
    """Verify data against a prefixed checksum string.

    Automatically extracts the algorithm from the checksum string and
    performs verification using the appropriate algorithm.

    Args:
        data: Data to verify
        checksum_str: Expected prefixed checksum (e.g., "sha256:abc123...")

    Returns:
        True if checksum matches, False otherwise

    Example:
        >>> data = b"test data"
        >>> checksum = format_checksum(data, "sha256")
        >>> verify_checksum(data, checksum)
        True
        >>> verify_checksum(b"wrong data", checksum)
        False

    """
    try:
        algorithm, expected_value = parse_checksum(checksum_str)
        actual_checksum = format_checksum(data, algorithm)
        actual_value = actual_checksum.split(":", 1)[1]

        matches = actual_value.lower() == expected_value.lower()

        if matches:
            log.debug(
                algorithm=algorithm,
                size=len(data),
            )
        else:
            log.warning(
                "❌ Prefixed checksum mismatch",
                algorithm=algorithm,
                expected=expected_value[:16] + "...",
                actual=actual_value[:16] + "...",
            )

        return matches

    except (ValueError, Exception) as e:
        log.warning(
            "❌ Checksum verification failed",
            error=str(e),
            checksum=checksum_str[:40] + "...",
        )
        return False


def normalize_checksum(checksum_str: str) -> str:
    """Normalize a checksum string to prefixed format.

    Ensures the checksum is in the standard "algorithm:value" format
    and validates both the algorithm and value.

    Args:
        checksum_str: Checksum string to normalize

    Returns:
        Normalized checksum with prefix

    Raises:
        ValueError: If checksum format is invalid

    Example:
        >>> normalize_checksum("sha256:ABC123")
        'sha256:abc123'

    """
    algorithm, value = parse_checksum(checksum_str)
    normalized = f"{algorithm}:{value.lower()}"

    log.debug(
        "🔄 Normalized checksum",
        input=checksum_str[:40] + "...",
        output=normalized[:40] + "...",
    )

    return normalized


def is_strong_checksum(checksum_str: str) -> bool:
    """Check if a checksum uses a cryptographically strong algorithm.

    Strong algorithms are suitable for security-critical applications.
    Weak algorithms like MD5 and Adler32 should only be used for
    non-security purposes like data integrity checks.

    Args:
        checksum_str: Prefixed checksum string

    Returns:
        True if using a strong algorithm (sha256, sha512, blake2b, blake2s)

    Example:
        >>> is_strong_checksum("sha256:abc123")
        True
        >>> is_strong_checksum("md5:abc123")
        False
        >>> is_strong_checksum("adler32:deadbeef")
        False

    """
    try:
        algorithm, _ = parse_checksum(checksum_str)
        strong_algorithms = {"sha256", "sha512", "blake2b", "blake2s"}
        is_strong = algorithm in strong_algorithms

        log.debug(
            "🔒 Checked checksum strength",
            algorithm=algorithm,
            is_strong=is_strong,
        )

        return is_strong

    except ValueError:
        log.warning(
            "⚠️ Cannot determine checksum strength - invalid format",
            checksum=checksum_str[:40] + "...",
        )
        return False


# 🧱🏗️🔚
