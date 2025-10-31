#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from __future__ import annotations

from collections.abc import Iterator
from pathlib import Path
from typing import BinaryIO

from provide.foundation.crypto.algorithms import (
    DEFAULT_ALGORITHM,
    get_hasher,
    validate_algorithm,
)
from provide.foundation.errors.resources import ResourceError
from provide.foundation.logger import get_logger

"""Core hashing operations."""

log = get_logger(__name__)

# Default chunk size for file reading (8KB)
DEFAULT_CHUNK_SIZE = 8192


def hash_file(
    path: Path | str,
    algorithm: str = DEFAULT_ALGORITHM,
    chunk_size: int = DEFAULT_CHUNK_SIZE,
) -> str:
    """Hash a file's contents.

    Args:
        path: File path
        algorithm: Hash algorithm (sha256, sha512, md5, etc.)
        chunk_size: Size of chunks to read at a time

    Returns:
        Hex digest of file hash

    Raises:
        ResourceError: If file cannot be read
        ValidationError: If algorithm is not supported

    """
    if isinstance(path, str):
        path = Path(path)

    if not path.exists():
        raise ResourceError(
            f"File not found: {path}",
            resource_type="file",
            resource_path=str(path),
        )

    if not path.is_file():
        raise ResourceError(
            f"Path is not a file: {path}",
            resource_type="file",
            resource_path=str(path),
        )

    validate_algorithm(algorithm)
    hasher = get_hasher(algorithm)

    try:
        with path.open("rb") as f:
            while chunk := f.read(chunk_size):
                hasher.update(chunk)

        hash_value = hasher.hexdigest()
        log.debug(
            "🔐 Hashed file",
            path=str(path),
            algorithm=algorithm,
            hash=hash_value[:16] + "...",
        )
        return hash_value

    except OSError as e:
        raise ResourceError(
            f"Failed to read file: {path}",
            resource_type="file",
            resource_path=str(path),
        ) from e


def hash_data(
    data: bytes,
    algorithm: str = DEFAULT_ALGORITHM,
) -> str:
    """Hash binary data.

    Args:
        data: Data to hash
        algorithm: Hash algorithm

    Returns:
        Hex digest

    Raises:
        ValidationError: If algorithm is not supported

    """
    validate_algorithm(algorithm)
    hasher = get_hasher(algorithm)
    hasher.update(data)

    hash_value = hasher.hexdigest()
    log.debug(
        "🔐 Hashed data",
        algorithm=algorithm,
        size=len(data),
        hash=hash_value[:16] + "...",
    )
    return hash_value


def hash_string(
    text: str,
    algorithm: str = DEFAULT_ALGORITHM,
    encoding: str = "utf-8",
) -> str:
    """Hash a text string.

    Args:
        text: Text to hash
        algorithm: Hash algorithm
        encoding: Text encoding

    Returns:
        Hex digest

    Raises:
        ValidationError: If algorithm is not supported

    """
    return hash_data(text.encode(encoding), algorithm)


def hash_stream(
    stream: BinaryIO,
    algorithm: str = DEFAULT_ALGORITHM,
    chunk_size: int = DEFAULT_CHUNK_SIZE,
) -> str:
    """Hash data from a stream.

    Args:
        stream: Binary stream to read from
        algorithm: Hash algorithm
        chunk_size: Size of chunks to read at a time

    Returns:
        Hex digest

    Raises:
        ValidationError: If algorithm is not supported

    """
    validate_algorithm(algorithm)
    hasher = get_hasher(algorithm)

    bytes_read = 0
    while chunk := stream.read(chunk_size):
        hasher.update(chunk)
        bytes_read += len(chunk)

    hash_value = hasher.hexdigest()
    log.debug(
        "🔐 Hashed stream",
        algorithm=algorithm,
        bytes_read=bytes_read,
        hash=hash_value[:16] + "...",
    )
    return hash_value


def hash_file_multiple(
    path: Path | str,
    algorithms: list[str],
    chunk_size: int = DEFAULT_CHUNK_SIZE,
) -> dict[str, str]:
    """Hash a file with multiple algorithms in a single pass.

    This is more efficient than calling hash_file multiple times.

    Args:
        path: File path
        algorithms: List of hash algorithms
        chunk_size: Size of chunks to read at a time

    Returns:
        Dictionary mapping algorithm name to hex digest

    Raises:
        ResourceError: If file cannot be read
        ValidationError: If any algorithm is not supported

    """
    if isinstance(path, str):
        path = Path(path)

    if not path.exists():
        raise ResourceError(
            f"File not found: {path}",
            resource_type="file",
            resource_path=str(path),
        )

    # Create hashers for all algorithms
    hashers = {}
    for algo in algorithms:
        validate_algorithm(algo)
        hashers[algo] = get_hasher(algo)

    # Read file once and update all hashers
    try:
        with path.open("rb") as f:
            while chunk := f.read(chunk_size):
                for hasher in hashers.values():
                    hasher.update(chunk)

        # Get results
        results = {algo: hasher.hexdigest() for algo, hasher in hashers.items()}

        log.debug(
            "🔐 Hashed file with multiple algorithms",
            path=str(path),
            algorithms=algorithms,
        )

        return results

    except OSError as e:
        raise ResourceError(
            f"Failed to read file: {path}",
            resource_type="file",
            resource_path=str(path),
        ) from e


def hash_chunks(
    chunks: Iterator[bytes],
    algorithm: str = DEFAULT_ALGORITHM,
) -> str:
    """Hash an iterator of byte chunks.

    Useful for hashing data that comes in chunks, like from a network stream.

    Args:
        chunks: Iterator yielding byte chunks
        algorithm: Hash algorithm

    Returns:
        Hex digest

    Raises:
        ValidationError: If algorithm is not supported

    """
    validate_algorithm(algorithm)
    hasher = get_hasher(algorithm)

    bytes_processed = 0
    for chunk in chunks:
        hasher.update(chunk)
        bytes_processed += len(chunk)

    hash_value = hasher.hexdigest()
    log.debug(
        "🔐 Hashed chunks",
        algorithm=algorithm,
        bytes_processed=bytes_processed,
        hash=hash_value[:16] + "...",
    )
    return hash_value


# 🧱🏗️🔚
