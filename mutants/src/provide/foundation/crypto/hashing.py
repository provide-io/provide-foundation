# provide/foundation/crypto/hashing.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

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
from inspect import signature as _mutmut_signature
from typing import Annotated
from typing import Callable
from typing import ClassVar


MutantDict = Annotated[dict[str, Callable], "Mutant"]


def _mutmut_trampoline(orig, mutants, call_args, call_kwargs, self_arg=None):
    """Forward call to original or mutated function, depending on the environment"""
    import os

    mutant_under_test = os.environ["MUTANT_UNDER_TEST"]
    if mutant_under_test == "fail":
        from mutmut.__main__ import MutmutProgrammaticFailException

        raise MutmutProgrammaticFailException("Failed programmatically")
    elif mutant_under_test == "stats":
        from mutmut.__main__ import record_trampoline_hit

        record_trampoline_hit(orig.__module__ + "." + orig.__name__)
        result = orig(*call_args, **call_kwargs)
        return result
    prefix = orig.__module__ + "." + orig.__name__ + "__mutmut_"
    if not mutant_under_test.startswith(prefix):
        result = orig(*call_args, **call_kwargs)
        return result
    mutant_name = mutant_under_test.rpartition(".")[-1]
    if self_arg:
        # call to a class method where self is not bound
        result = mutants[mutant_name](self_arg, *call_args, **call_kwargs)
    else:
        result = mutants[mutant_name](*call_args, **call_kwargs)
    return result


def x_hash_file__mutmut_orig(
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


def x_hash_file__mutmut_1(
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
        path = None

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


def x_hash_file__mutmut_2(
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
        path = Path(None)

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


def x_hash_file__mutmut_3(
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

    if path.exists():
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


def x_hash_file__mutmut_4(
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
            None,
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


def x_hash_file__mutmut_5(
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
            resource_type=None,
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


def x_hash_file__mutmut_6(
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
            resource_path=None,
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


def x_hash_file__mutmut_7(
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


def x_hash_file__mutmut_8(
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


def x_hash_file__mutmut_9(
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


def x_hash_file__mutmut_10(
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
            resource_type="XXfileXX",
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


def x_hash_file__mutmut_11(
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
            resource_type="FILE",
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


def x_hash_file__mutmut_12(
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
            resource_path=str(None),
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


def x_hash_file__mutmut_13(
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

    if path.is_file():
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


def x_hash_file__mutmut_14(
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
            None,
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


def x_hash_file__mutmut_15(
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
            resource_type=None,
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


def x_hash_file__mutmut_16(
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
            resource_path=None,
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


def x_hash_file__mutmut_17(
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


def x_hash_file__mutmut_18(
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


def x_hash_file__mutmut_19(
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


def x_hash_file__mutmut_20(
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
            resource_type="XXfileXX",
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


def x_hash_file__mutmut_21(
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
            resource_type="FILE",
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


def x_hash_file__mutmut_22(
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
            resource_path=str(None),
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


def x_hash_file__mutmut_23(
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

    validate_algorithm(None)
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


def x_hash_file__mutmut_24(
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
    hasher = None

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


def x_hash_file__mutmut_25(
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
    hasher = get_hasher(None)

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


def x_hash_file__mutmut_26(
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
        with path.open(None) as f:
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


def x_hash_file__mutmut_27(
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
        with path.open("XXrbXX") as f:
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


def x_hash_file__mutmut_28(
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
        with path.open("RB") as f:
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


def x_hash_file__mutmut_29(
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
            while chunk := f.read(None):
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


def x_hash_file__mutmut_30(
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
                hasher.update(None)

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


def x_hash_file__mutmut_31(
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

        hash_value = None
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


def x_hash_file__mutmut_32(
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
            None,
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


def x_hash_file__mutmut_33(
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
            path=None,
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


def x_hash_file__mutmut_34(
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
            algorithm=None,
            hash=hash_value[:16] + "...",
        )
        return hash_value

    except OSError as e:
        raise ResourceError(
            f"Failed to read file: {path}",
            resource_type="file",
            resource_path=str(path),
        ) from e


def x_hash_file__mutmut_35(
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
            hash=None,
        )
        return hash_value

    except OSError as e:
        raise ResourceError(
            f"Failed to read file: {path}",
            resource_type="file",
            resource_path=str(path),
        ) from e


def x_hash_file__mutmut_36(
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


def x_hash_file__mutmut_37(
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


def x_hash_file__mutmut_38(
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
            hash=hash_value[:16] + "...",
        )
        return hash_value

    except OSError as e:
        raise ResourceError(
            f"Failed to read file: {path}",
            resource_type="file",
            resource_path=str(path),
        ) from e


def x_hash_file__mutmut_39(
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
        )
        return hash_value

    except OSError as e:
        raise ResourceError(
            f"Failed to read file: {path}",
            resource_type="file",
            resource_path=str(path),
        ) from e


def x_hash_file__mutmut_40(
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
            "XX🔐 Hashed fileXX",
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


def x_hash_file__mutmut_41(
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
            "🔐 hashed file",
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


def x_hash_file__mutmut_42(
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
            "🔐 HASHED FILE",
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


def x_hash_file__mutmut_43(
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
            path=str(None),
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


def x_hash_file__mutmut_44(
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
            hash=hash_value[:16] - "...",
        )
        return hash_value

    except OSError as e:
        raise ResourceError(
            f"Failed to read file: {path}",
            resource_type="file",
            resource_path=str(path),
        ) from e


def x_hash_file__mutmut_45(
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
            hash=hash_value[:17] + "...",
        )
        return hash_value

    except OSError as e:
        raise ResourceError(
            f"Failed to read file: {path}",
            resource_type="file",
            resource_path=str(path),
        ) from e


def x_hash_file__mutmut_46(
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
            hash=hash_value[:16] + "XX...XX",
        )
        return hash_value

    except OSError as e:
        raise ResourceError(
            f"Failed to read file: {path}",
            resource_type="file",
            resource_path=str(path),
        ) from e


def x_hash_file__mutmut_47(
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
            None,
            resource_type="file",
            resource_path=str(path),
        ) from e


def x_hash_file__mutmut_48(
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
            resource_type=None,
            resource_path=str(path),
        ) from e


def x_hash_file__mutmut_49(
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
            resource_path=None,
        ) from e


def x_hash_file__mutmut_50(
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
            resource_type="file",
            resource_path=str(path),
        ) from e


def x_hash_file__mutmut_51(
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
            resource_path=str(path),
        ) from e


def x_hash_file__mutmut_52(
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
        ) from e


def x_hash_file__mutmut_53(
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
            resource_type="XXfileXX",
            resource_path=str(path),
        ) from e


def x_hash_file__mutmut_54(
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
            resource_type="FILE",
            resource_path=str(path),
        ) from e


def x_hash_file__mutmut_55(
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
            resource_path=str(None),
        ) from e


x_hash_file__mutmut_mutants: ClassVar[MutantDict] = {
    "x_hash_file__mutmut_1": x_hash_file__mutmut_1,
    "x_hash_file__mutmut_2": x_hash_file__mutmut_2,
    "x_hash_file__mutmut_3": x_hash_file__mutmut_3,
    "x_hash_file__mutmut_4": x_hash_file__mutmut_4,
    "x_hash_file__mutmut_5": x_hash_file__mutmut_5,
    "x_hash_file__mutmut_6": x_hash_file__mutmut_6,
    "x_hash_file__mutmut_7": x_hash_file__mutmut_7,
    "x_hash_file__mutmut_8": x_hash_file__mutmut_8,
    "x_hash_file__mutmut_9": x_hash_file__mutmut_9,
    "x_hash_file__mutmut_10": x_hash_file__mutmut_10,
    "x_hash_file__mutmut_11": x_hash_file__mutmut_11,
    "x_hash_file__mutmut_12": x_hash_file__mutmut_12,
    "x_hash_file__mutmut_13": x_hash_file__mutmut_13,
    "x_hash_file__mutmut_14": x_hash_file__mutmut_14,
    "x_hash_file__mutmut_15": x_hash_file__mutmut_15,
    "x_hash_file__mutmut_16": x_hash_file__mutmut_16,
    "x_hash_file__mutmut_17": x_hash_file__mutmut_17,
    "x_hash_file__mutmut_18": x_hash_file__mutmut_18,
    "x_hash_file__mutmut_19": x_hash_file__mutmut_19,
    "x_hash_file__mutmut_20": x_hash_file__mutmut_20,
    "x_hash_file__mutmut_21": x_hash_file__mutmut_21,
    "x_hash_file__mutmut_22": x_hash_file__mutmut_22,
    "x_hash_file__mutmut_23": x_hash_file__mutmut_23,
    "x_hash_file__mutmut_24": x_hash_file__mutmut_24,
    "x_hash_file__mutmut_25": x_hash_file__mutmut_25,
    "x_hash_file__mutmut_26": x_hash_file__mutmut_26,
    "x_hash_file__mutmut_27": x_hash_file__mutmut_27,
    "x_hash_file__mutmut_28": x_hash_file__mutmut_28,
    "x_hash_file__mutmut_29": x_hash_file__mutmut_29,
    "x_hash_file__mutmut_30": x_hash_file__mutmut_30,
    "x_hash_file__mutmut_31": x_hash_file__mutmut_31,
    "x_hash_file__mutmut_32": x_hash_file__mutmut_32,
    "x_hash_file__mutmut_33": x_hash_file__mutmut_33,
    "x_hash_file__mutmut_34": x_hash_file__mutmut_34,
    "x_hash_file__mutmut_35": x_hash_file__mutmut_35,
    "x_hash_file__mutmut_36": x_hash_file__mutmut_36,
    "x_hash_file__mutmut_37": x_hash_file__mutmut_37,
    "x_hash_file__mutmut_38": x_hash_file__mutmut_38,
    "x_hash_file__mutmut_39": x_hash_file__mutmut_39,
    "x_hash_file__mutmut_40": x_hash_file__mutmut_40,
    "x_hash_file__mutmut_41": x_hash_file__mutmut_41,
    "x_hash_file__mutmut_42": x_hash_file__mutmut_42,
    "x_hash_file__mutmut_43": x_hash_file__mutmut_43,
    "x_hash_file__mutmut_44": x_hash_file__mutmut_44,
    "x_hash_file__mutmut_45": x_hash_file__mutmut_45,
    "x_hash_file__mutmut_46": x_hash_file__mutmut_46,
    "x_hash_file__mutmut_47": x_hash_file__mutmut_47,
    "x_hash_file__mutmut_48": x_hash_file__mutmut_48,
    "x_hash_file__mutmut_49": x_hash_file__mutmut_49,
    "x_hash_file__mutmut_50": x_hash_file__mutmut_50,
    "x_hash_file__mutmut_51": x_hash_file__mutmut_51,
    "x_hash_file__mutmut_52": x_hash_file__mutmut_52,
    "x_hash_file__mutmut_53": x_hash_file__mutmut_53,
    "x_hash_file__mutmut_54": x_hash_file__mutmut_54,
    "x_hash_file__mutmut_55": x_hash_file__mutmut_55,
}


def hash_file(*args, **kwargs):
    result = _mutmut_trampoline(x_hash_file__mutmut_orig, x_hash_file__mutmut_mutants, args, kwargs)
    return result


hash_file.__signature__ = _mutmut_signature(x_hash_file__mutmut_orig)
x_hash_file__mutmut_orig.__name__ = "x_hash_file"


def x_hash_data__mutmut_orig(
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


def x_hash_data__mutmut_1(
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
    validate_algorithm(None)
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


def x_hash_data__mutmut_2(
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
    hasher = None
    hasher.update(data)

    hash_value = hasher.hexdigest()
    log.debug(
        "🔐 Hashed data",
        algorithm=algorithm,
        size=len(data),
        hash=hash_value[:16] + "...",
    )
    return hash_value


def x_hash_data__mutmut_3(
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
    hasher = get_hasher(None)
    hasher.update(data)

    hash_value = hasher.hexdigest()
    log.debug(
        "🔐 Hashed data",
        algorithm=algorithm,
        size=len(data),
        hash=hash_value[:16] + "...",
    )
    return hash_value


def x_hash_data__mutmut_4(
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
    hasher.update(None)

    hash_value = hasher.hexdigest()
    log.debug(
        "🔐 Hashed data",
        algorithm=algorithm,
        size=len(data),
        hash=hash_value[:16] + "...",
    )
    return hash_value


def x_hash_data__mutmut_5(
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

    hash_value = None
    log.debug(
        "🔐 Hashed data",
        algorithm=algorithm,
        size=len(data),
        hash=hash_value[:16] + "...",
    )
    return hash_value


def x_hash_data__mutmut_6(
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
        None,
        algorithm=algorithm,
        size=len(data),
        hash=hash_value[:16] + "...",
    )
    return hash_value


def x_hash_data__mutmut_7(
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
        algorithm=None,
        size=len(data),
        hash=hash_value[:16] + "...",
    )
    return hash_value


def x_hash_data__mutmut_8(
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
        size=None,
        hash=hash_value[:16] + "...",
    )
    return hash_value


def x_hash_data__mutmut_9(
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
        hash=None,
    )
    return hash_value


def x_hash_data__mutmut_10(
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
        algorithm=algorithm,
        size=len(data),
        hash=hash_value[:16] + "...",
    )
    return hash_value


def x_hash_data__mutmut_11(
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
        size=len(data),
        hash=hash_value[:16] + "...",
    )
    return hash_value


def x_hash_data__mutmut_12(
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
        hash=hash_value[:16] + "...",
    )
    return hash_value


def x_hash_data__mutmut_13(
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
    )
    return hash_value


def x_hash_data__mutmut_14(
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
        "XX🔐 Hashed dataXX",
        algorithm=algorithm,
        size=len(data),
        hash=hash_value[:16] + "...",
    )
    return hash_value


def x_hash_data__mutmut_15(
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
        "🔐 hashed data",
        algorithm=algorithm,
        size=len(data),
        hash=hash_value[:16] + "...",
    )
    return hash_value


def x_hash_data__mutmut_16(
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
        "🔐 HASHED DATA",
        algorithm=algorithm,
        size=len(data),
        hash=hash_value[:16] + "...",
    )
    return hash_value


def x_hash_data__mutmut_17(
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
        hash=hash_value[:16] - "...",
    )
    return hash_value


def x_hash_data__mutmut_18(
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
        hash=hash_value[:17] + "...",
    )
    return hash_value


def x_hash_data__mutmut_19(
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
        hash=hash_value[:16] + "XX...XX",
    )
    return hash_value


x_hash_data__mutmut_mutants: ClassVar[MutantDict] = {
    "x_hash_data__mutmut_1": x_hash_data__mutmut_1,
    "x_hash_data__mutmut_2": x_hash_data__mutmut_2,
    "x_hash_data__mutmut_3": x_hash_data__mutmut_3,
    "x_hash_data__mutmut_4": x_hash_data__mutmut_4,
    "x_hash_data__mutmut_5": x_hash_data__mutmut_5,
    "x_hash_data__mutmut_6": x_hash_data__mutmut_6,
    "x_hash_data__mutmut_7": x_hash_data__mutmut_7,
    "x_hash_data__mutmut_8": x_hash_data__mutmut_8,
    "x_hash_data__mutmut_9": x_hash_data__mutmut_9,
    "x_hash_data__mutmut_10": x_hash_data__mutmut_10,
    "x_hash_data__mutmut_11": x_hash_data__mutmut_11,
    "x_hash_data__mutmut_12": x_hash_data__mutmut_12,
    "x_hash_data__mutmut_13": x_hash_data__mutmut_13,
    "x_hash_data__mutmut_14": x_hash_data__mutmut_14,
    "x_hash_data__mutmut_15": x_hash_data__mutmut_15,
    "x_hash_data__mutmut_16": x_hash_data__mutmut_16,
    "x_hash_data__mutmut_17": x_hash_data__mutmut_17,
    "x_hash_data__mutmut_18": x_hash_data__mutmut_18,
    "x_hash_data__mutmut_19": x_hash_data__mutmut_19,
}


def hash_data(*args, **kwargs):
    result = _mutmut_trampoline(x_hash_data__mutmut_orig, x_hash_data__mutmut_mutants, args, kwargs)
    return result


hash_data.__signature__ = _mutmut_signature(x_hash_data__mutmut_orig)
x_hash_data__mutmut_orig.__name__ = "x_hash_data"


def x_hash_string__mutmut_orig(
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


def x_hash_string__mutmut_1(
    text: str,
    algorithm: str = DEFAULT_ALGORITHM,
    encoding: str = "XXutf-8XX",
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


def x_hash_string__mutmut_2(
    text: str,
    algorithm: str = DEFAULT_ALGORITHM,
    encoding: str = "UTF-8",
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


def x_hash_string__mutmut_3(
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
    return hash_data(None, algorithm)


def x_hash_string__mutmut_4(
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
    return hash_data(text.encode(encoding), None)


def x_hash_string__mutmut_5(
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
    return hash_data(algorithm)


def x_hash_string__mutmut_6(
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
    return hash_data(
        text.encode(encoding),
    )


def x_hash_string__mutmut_7(
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
    return hash_data(text.encode(None), algorithm)


x_hash_string__mutmut_mutants: ClassVar[MutantDict] = {
    "x_hash_string__mutmut_1": x_hash_string__mutmut_1,
    "x_hash_string__mutmut_2": x_hash_string__mutmut_2,
    "x_hash_string__mutmut_3": x_hash_string__mutmut_3,
    "x_hash_string__mutmut_4": x_hash_string__mutmut_4,
    "x_hash_string__mutmut_5": x_hash_string__mutmut_5,
    "x_hash_string__mutmut_6": x_hash_string__mutmut_6,
    "x_hash_string__mutmut_7": x_hash_string__mutmut_7,
}


def hash_string(*args, **kwargs):
    result = _mutmut_trampoline(x_hash_string__mutmut_orig, x_hash_string__mutmut_mutants, args, kwargs)
    return result


hash_string.__signature__ = _mutmut_signature(x_hash_string__mutmut_orig)
x_hash_string__mutmut_orig.__name__ = "x_hash_string"


def x_hash_stream__mutmut_orig(
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


def x_hash_stream__mutmut_1(
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
    validate_algorithm(None)
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


def x_hash_stream__mutmut_2(
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
    hasher = None

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


def x_hash_stream__mutmut_3(
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
    hasher = get_hasher(None)

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


def x_hash_stream__mutmut_4(
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

    bytes_read = None
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


def x_hash_stream__mutmut_5(
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

    bytes_read = 1
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


def x_hash_stream__mutmut_6(
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
    while chunk := stream.read(None):
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


def x_hash_stream__mutmut_7(
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
        hasher.update(None)
        bytes_read += len(chunk)

    hash_value = hasher.hexdigest()
    log.debug(
        "🔐 Hashed stream",
        algorithm=algorithm,
        bytes_read=bytes_read,
        hash=hash_value[:16] + "...",
    )
    return hash_value


def x_hash_stream__mutmut_8(
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
        bytes_read = len(chunk)

    hash_value = hasher.hexdigest()
    log.debug(
        "🔐 Hashed stream",
        algorithm=algorithm,
        bytes_read=bytes_read,
        hash=hash_value[:16] + "...",
    )
    return hash_value


def x_hash_stream__mutmut_9(
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
        bytes_read -= len(chunk)

    hash_value = hasher.hexdigest()
    log.debug(
        "🔐 Hashed stream",
        algorithm=algorithm,
        bytes_read=bytes_read,
        hash=hash_value[:16] + "...",
    )
    return hash_value


def x_hash_stream__mutmut_10(
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

    hash_value = None
    log.debug(
        "🔐 Hashed stream",
        algorithm=algorithm,
        bytes_read=bytes_read,
        hash=hash_value[:16] + "...",
    )
    return hash_value


def x_hash_stream__mutmut_11(
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
        None,
        algorithm=algorithm,
        bytes_read=bytes_read,
        hash=hash_value[:16] + "...",
    )
    return hash_value


def x_hash_stream__mutmut_12(
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
        algorithm=None,
        bytes_read=bytes_read,
        hash=hash_value[:16] + "...",
    )
    return hash_value


def x_hash_stream__mutmut_13(
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
        bytes_read=None,
        hash=hash_value[:16] + "...",
    )
    return hash_value


def x_hash_stream__mutmut_14(
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
        hash=None,
    )
    return hash_value


def x_hash_stream__mutmut_15(
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
        algorithm=algorithm,
        bytes_read=bytes_read,
        hash=hash_value[:16] + "...",
    )
    return hash_value


def x_hash_stream__mutmut_16(
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
        bytes_read=bytes_read,
        hash=hash_value[:16] + "...",
    )
    return hash_value


def x_hash_stream__mutmut_17(
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
        hash=hash_value[:16] + "...",
    )
    return hash_value


def x_hash_stream__mutmut_18(
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
    )
    return hash_value


def x_hash_stream__mutmut_19(
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
        "XX🔐 Hashed streamXX",
        algorithm=algorithm,
        bytes_read=bytes_read,
        hash=hash_value[:16] + "...",
    )
    return hash_value


def x_hash_stream__mutmut_20(
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
        "🔐 hashed stream",
        algorithm=algorithm,
        bytes_read=bytes_read,
        hash=hash_value[:16] + "...",
    )
    return hash_value


def x_hash_stream__mutmut_21(
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
        "🔐 HASHED STREAM",
        algorithm=algorithm,
        bytes_read=bytes_read,
        hash=hash_value[:16] + "...",
    )
    return hash_value


def x_hash_stream__mutmut_22(
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
        hash=hash_value[:16] - "...",
    )
    return hash_value


def x_hash_stream__mutmut_23(
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
        hash=hash_value[:17] + "...",
    )
    return hash_value


def x_hash_stream__mutmut_24(
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
        hash=hash_value[:16] + "XX...XX",
    )
    return hash_value


x_hash_stream__mutmut_mutants: ClassVar[MutantDict] = {
    "x_hash_stream__mutmut_1": x_hash_stream__mutmut_1,
    "x_hash_stream__mutmut_2": x_hash_stream__mutmut_2,
    "x_hash_stream__mutmut_3": x_hash_stream__mutmut_3,
    "x_hash_stream__mutmut_4": x_hash_stream__mutmut_4,
    "x_hash_stream__mutmut_5": x_hash_stream__mutmut_5,
    "x_hash_stream__mutmut_6": x_hash_stream__mutmut_6,
    "x_hash_stream__mutmut_7": x_hash_stream__mutmut_7,
    "x_hash_stream__mutmut_8": x_hash_stream__mutmut_8,
    "x_hash_stream__mutmut_9": x_hash_stream__mutmut_9,
    "x_hash_stream__mutmut_10": x_hash_stream__mutmut_10,
    "x_hash_stream__mutmut_11": x_hash_stream__mutmut_11,
    "x_hash_stream__mutmut_12": x_hash_stream__mutmut_12,
    "x_hash_stream__mutmut_13": x_hash_stream__mutmut_13,
    "x_hash_stream__mutmut_14": x_hash_stream__mutmut_14,
    "x_hash_stream__mutmut_15": x_hash_stream__mutmut_15,
    "x_hash_stream__mutmut_16": x_hash_stream__mutmut_16,
    "x_hash_stream__mutmut_17": x_hash_stream__mutmut_17,
    "x_hash_stream__mutmut_18": x_hash_stream__mutmut_18,
    "x_hash_stream__mutmut_19": x_hash_stream__mutmut_19,
    "x_hash_stream__mutmut_20": x_hash_stream__mutmut_20,
    "x_hash_stream__mutmut_21": x_hash_stream__mutmut_21,
    "x_hash_stream__mutmut_22": x_hash_stream__mutmut_22,
    "x_hash_stream__mutmut_23": x_hash_stream__mutmut_23,
    "x_hash_stream__mutmut_24": x_hash_stream__mutmut_24,
}


def hash_stream(*args, **kwargs):
    result = _mutmut_trampoline(x_hash_stream__mutmut_orig, x_hash_stream__mutmut_mutants, args, kwargs)
    return result


hash_stream.__signature__ = _mutmut_signature(x_hash_stream__mutmut_orig)
x_hash_stream__mutmut_orig.__name__ = "x_hash_stream"


def x_hash_file_multiple__mutmut_orig(
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


def x_hash_file_multiple__mutmut_1(
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
        path = None

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


def x_hash_file_multiple__mutmut_2(
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
        path = Path(None)

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


def x_hash_file_multiple__mutmut_3(
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

    if path.exists():
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


def x_hash_file_multiple__mutmut_4(
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
            None,
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


def x_hash_file_multiple__mutmut_5(
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
            resource_type=None,
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


def x_hash_file_multiple__mutmut_6(
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
            resource_path=None,
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


def x_hash_file_multiple__mutmut_7(
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


def x_hash_file_multiple__mutmut_8(
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


def x_hash_file_multiple__mutmut_9(
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


def x_hash_file_multiple__mutmut_10(
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
            resource_type="XXfileXX",
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


def x_hash_file_multiple__mutmut_11(
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
            resource_type="FILE",
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


def x_hash_file_multiple__mutmut_12(
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
            resource_path=str(None),
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


def x_hash_file_multiple__mutmut_13(
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
    hashers = None
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


def x_hash_file_multiple__mutmut_14(
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
        validate_algorithm(None)
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


def x_hash_file_multiple__mutmut_15(
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
        hashers[algo] = None

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


def x_hash_file_multiple__mutmut_16(
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
        hashers[algo] = get_hasher(None)

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


def x_hash_file_multiple__mutmut_17(
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
        with path.open(None) as f:
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


def x_hash_file_multiple__mutmut_18(
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
        with path.open("XXrbXX") as f:
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


def x_hash_file_multiple__mutmut_19(
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
        with path.open("RB") as f:
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


def x_hash_file_multiple__mutmut_20(
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
            while chunk := f.read(None):
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


def x_hash_file_multiple__mutmut_21(
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
                    hasher.update(None)

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


def x_hash_file_multiple__mutmut_22(
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
        results = None

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


def x_hash_file_multiple__mutmut_23(
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
            None,
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


def x_hash_file_multiple__mutmut_24(
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
            path=None,
            algorithms=algorithms,
        )

        return results

    except OSError as e:
        raise ResourceError(
            f"Failed to read file: {path}",
            resource_type="file",
            resource_path=str(path),
        ) from e


def x_hash_file_multiple__mutmut_25(
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
            algorithms=None,
        )

        return results

    except OSError as e:
        raise ResourceError(
            f"Failed to read file: {path}",
            resource_type="file",
            resource_path=str(path),
        ) from e


def x_hash_file_multiple__mutmut_26(
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


def x_hash_file_multiple__mutmut_27(
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
            algorithms=algorithms,
        )

        return results

    except OSError as e:
        raise ResourceError(
            f"Failed to read file: {path}",
            resource_type="file",
            resource_path=str(path),
        ) from e


def x_hash_file_multiple__mutmut_28(
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
        )

        return results

    except OSError as e:
        raise ResourceError(
            f"Failed to read file: {path}",
            resource_type="file",
            resource_path=str(path),
        ) from e


def x_hash_file_multiple__mutmut_29(
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
            "XX🔐 Hashed file with multiple algorithmsXX",
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


def x_hash_file_multiple__mutmut_30(
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
            "🔐 hashed file with multiple algorithms",
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


def x_hash_file_multiple__mutmut_31(
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
            "🔐 HASHED FILE WITH MULTIPLE ALGORITHMS",
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


def x_hash_file_multiple__mutmut_32(
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
            path=str(None),
            algorithms=algorithms,
        )

        return results

    except OSError as e:
        raise ResourceError(
            f"Failed to read file: {path}",
            resource_type="file",
            resource_path=str(path),
        ) from e


def x_hash_file_multiple__mutmut_33(
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
            None,
            resource_type="file",
            resource_path=str(path),
        ) from e


def x_hash_file_multiple__mutmut_34(
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
            resource_type=None,
            resource_path=str(path),
        ) from e


def x_hash_file_multiple__mutmut_35(
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
            resource_path=None,
        ) from e


def x_hash_file_multiple__mutmut_36(
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
            resource_type="file",
            resource_path=str(path),
        ) from e


def x_hash_file_multiple__mutmut_37(
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
            resource_path=str(path),
        ) from e


def x_hash_file_multiple__mutmut_38(
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
        ) from e


def x_hash_file_multiple__mutmut_39(
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
            resource_type="XXfileXX",
            resource_path=str(path),
        ) from e


def x_hash_file_multiple__mutmut_40(
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
            resource_type="FILE",
            resource_path=str(path),
        ) from e


def x_hash_file_multiple__mutmut_41(
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
            resource_path=str(None),
        ) from e


x_hash_file_multiple__mutmut_mutants: ClassVar[MutantDict] = {
    "x_hash_file_multiple__mutmut_1": x_hash_file_multiple__mutmut_1,
    "x_hash_file_multiple__mutmut_2": x_hash_file_multiple__mutmut_2,
    "x_hash_file_multiple__mutmut_3": x_hash_file_multiple__mutmut_3,
    "x_hash_file_multiple__mutmut_4": x_hash_file_multiple__mutmut_4,
    "x_hash_file_multiple__mutmut_5": x_hash_file_multiple__mutmut_5,
    "x_hash_file_multiple__mutmut_6": x_hash_file_multiple__mutmut_6,
    "x_hash_file_multiple__mutmut_7": x_hash_file_multiple__mutmut_7,
    "x_hash_file_multiple__mutmut_8": x_hash_file_multiple__mutmut_8,
    "x_hash_file_multiple__mutmut_9": x_hash_file_multiple__mutmut_9,
    "x_hash_file_multiple__mutmut_10": x_hash_file_multiple__mutmut_10,
    "x_hash_file_multiple__mutmut_11": x_hash_file_multiple__mutmut_11,
    "x_hash_file_multiple__mutmut_12": x_hash_file_multiple__mutmut_12,
    "x_hash_file_multiple__mutmut_13": x_hash_file_multiple__mutmut_13,
    "x_hash_file_multiple__mutmut_14": x_hash_file_multiple__mutmut_14,
    "x_hash_file_multiple__mutmut_15": x_hash_file_multiple__mutmut_15,
    "x_hash_file_multiple__mutmut_16": x_hash_file_multiple__mutmut_16,
    "x_hash_file_multiple__mutmut_17": x_hash_file_multiple__mutmut_17,
    "x_hash_file_multiple__mutmut_18": x_hash_file_multiple__mutmut_18,
    "x_hash_file_multiple__mutmut_19": x_hash_file_multiple__mutmut_19,
    "x_hash_file_multiple__mutmut_20": x_hash_file_multiple__mutmut_20,
    "x_hash_file_multiple__mutmut_21": x_hash_file_multiple__mutmut_21,
    "x_hash_file_multiple__mutmut_22": x_hash_file_multiple__mutmut_22,
    "x_hash_file_multiple__mutmut_23": x_hash_file_multiple__mutmut_23,
    "x_hash_file_multiple__mutmut_24": x_hash_file_multiple__mutmut_24,
    "x_hash_file_multiple__mutmut_25": x_hash_file_multiple__mutmut_25,
    "x_hash_file_multiple__mutmut_26": x_hash_file_multiple__mutmut_26,
    "x_hash_file_multiple__mutmut_27": x_hash_file_multiple__mutmut_27,
    "x_hash_file_multiple__mutmut_28": x_hash_file_multiple__mutmut_28,
    "x_hash_file_multiple__mutmut_29": x_hash_file_multiple__mutmut_29,
    "x_hash_file_multiple__mutmut_30": x_hash_file_multiple__mutmut_30,
    "x_hash_file_multiple__mutmut_31": x_hash_file_multiple__mutmut_31,
    "x_hash_file_multiple__mutmut_32": x_hash_file_multiple__mutmut_32,
    "x_hash_file_multiple__mutmut_33": x_hash_file_multiple__mutmut_33,
    "x_hash_file_multiple__mutmut_34": x_hash_file_multiple__mutmut_34,
    "x_hash_file_multiple__mutmut_35": x_hash_file_multiple__mutmut_35,
    "x_hash_file_multiple__mutmut_36": x_hash_file_multiple__mutmut_36,
    "x_hash_file_multiple__mutmut_37": x_hash_file_multiple__mutmut_37,
    "x_hash_file_multiple__mutmut_38": x_hash_file_multiple__mutmut_38,
    "x_hash_file_multiple__mutmut_39": x_hash_file_multiple__mutmut_39,
    "x_hash_file_multiple__mutmut_40": x_hash_file_multiple__mutmut_40,
    "x_hash_file_multiple__mutmut_41": x_hash_file_multiple__mutmut_41,
}


def hash_file_multiple(*args, **kwargs):
    result = _mutmut_trampoline(
        x_hash_file_multiple__mutmut_orig, x_hash_file_multiple__mutmut_mutants, args, kwargs
    )
    return result


hash_file_multiple.__signature__ = _mutmut_signature(x_hash_file_multiple__mutmut_orig)
x_hash_file_multiple__mutmut_orig.__name__ = "x_hash_file_multiple"


def x_hash_chunks__mutmut_orig(
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


def x_hash_chunks__mutmut_1(
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
    validate_algorithm(None)
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


def x_hash_chunks__mutmut_2(
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
    hasher = None

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


def x_hash_chunks__mutmut_3(
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
    hasher = get_hasher(None)

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


def x_hash_chunks__mutmut_4(
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

    bytes_processed = None
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


def x_hash_chunks__mutmut_5(
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

    bytes_processed = 1
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


def x_hash_chunks__mutmut_6(
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
        hasher.update(None)
        bytes_processed += len(chunk)

    hash_value = hasher.hexdigest()
    log.debug(
        "🔐 Hashed chunks",
        algorithm=algorithm,
        bytes_processed=bytes_processed,
        hash=hash_value[:16] + "...",
    )
    return hash_value


def x_hash_chunks__mutmut_7(
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
        bytes_processed = len(chunk)

    hash_value = hasher.hexdigest()
    log.debug(
        "🔐 Hashed chunks",
        algorithm=algorithm,
        bytes_processed=bytes_processed,
        hash=hash_value[:16] + "...",
    )
    return hash_value


def x_hash_chunks__mutmut_8(
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
        bytes_processed -= len(chunk)

    hash_value = hasher.hexdigest()
    log.debug(
        "🔐 Hashed chunks",
        algorithm=algorithm,
        bytes_processed=bytes_processed,
        hash=hash_value[:16] + "...",
    )
    return hash_value


def x_hash_chunks__mutmut_9(
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

    hash_value = None
    log.debug(
        "🔐 Hashed chunks",
        algorithm=algorithm,
        bytes_processed=bytes_processed,
        hash=hash_value[:16] + "...",
    )
    return hash_value


def x_hash_chunks__mutmut_10(
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
        None,
        algorithm=algorithm,
        bytes_processed=bytes_processed,
        hash=hash_value[:16] + "...",
    )
    return hash_value


def x_hash_chunks__mutmut_11(
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
        algorithm=None,
        bytes_processed=bytes_processed,
        hash=hash_value[:16] + "...",
    )
    return hash_value


def x_hash_chunks__mutmut_12(
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
        bytes_processed=None,
        hash=hash_value[:16] + "...",
    )
    return hash_value


def x_hash_chunks__mutmut_13(
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
        hash=None,
    )
    return hash_value


def x_hash_chunks__mutmut_14(
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
        algorithm=algorithm,
        bytes_processed=bytes_processed,
        hash=hash_value[:16] + "...",
    )
    return hash_value


def x_hash_chunks__mutmut_15(
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
        bytes_processed=bytes_processed,
        hash=hash_value[:16] + "...",
    )
    return hash_value


def x_hash_chunks__mutmut_16(
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
        hash=hash_value[:16] + "...",
    )
    return hash_value


def x_hash_chunks__mutmut_17(
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
    )
    return hash_value


def x_hash_chunks__mutmut_18(
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
        "XX🔐 Hashed chunksXX",
        algorithm=algorithm,
        bytes_processed=bytes_processed,
        hash=hash_value[:16] + "...",
    )
    return hash_value


def x_hash_chunks__mutmut_19(
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
        "🔐 hashed chunks",
        algorithm=algorithm,
        bytes_processed=bytes_processed,
        hash=hash_value[:16] + "...",
    )
    return hash_value


def x_hash_chunks__mutmut_20(
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
        "🔐 HASHED CHUNKS",
        algorithm=algorithm,
        bytes_processed=bytes_processed,
        hash=hash_value[:16] + "...",
    )
    return hash_value


def x_hash_chunks__mutmut_21(
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
        hash=hash_value[:16] - "...",
    )
    return hash_value


def x_hash_chunks__mutmut_22(
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
        hash=hash_value[:17] + "...",
    )
    return hash_value


def x_hash_chunks__mutmut_23(
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
        hash=hash_value[:16] + "XX...XX",
    )
    return hash_value


x_hash_chunks__mutmut_mutants: ClassVar[MutantDict] = {
    "x_hash_chunks__mutmut_1": x_hash_chunks__mutmut_1,
    "x_hash_chunks__mutmut_2": x_hash_chunks__mutmut_2,
    "x_hash_chunks__mutmut_3": x_hash_chunks__mutmut_3,
    "x_hash_chunks__mutmut_4": x_hash_chunks__mutmut_4,
    "x_hash_chunks__mutmut_5": x_hash_chunks__mutmut_5,
    "x_hash_chunks__mutmut_6": x_hash_chunks__mutmut_6,
    "x_hash_chunks__mutmut_7": x_hash_chunks__mutmut_7,
    "x_hash_chunks__mutmut_8": x_hash_chunks__mutmut_8,
    "x_hash_chunks__mutmut_9": x_hash_chunks__mutmut_9,
    "x_hash_chunks__mutmut_10": x_hash_chunks__mutmut_10,
    "x_hash_chunks__mutmut_11": x_hash_chunks__mutmut_11,
    "x_hash_chunks__mutmut_12": x_hash_chunks__mutmut_12,
    "x_hash_chunks__mutmut_13": x_hash_chunks__mutmut_13,
    "x_hash_chunks__mutmut_14": x_hash_chunks__mutmut_14,
    "x_hash_chunks__mutmut_15": x_hash_chunks__mutmut_15,
    "x_hash_chunks__mutmut_16": x_hash_chunks__mutmut_16,
    "x_hash_chunks__mutmut_17": x_hash_chunks__mutmut_17,
    "x_hash_chunks__mutmut_18": x_hash_chunks__mutmut_18,
    "x_hash_chunks__mutmut_19": x_hash_chunks__mutmut_19,
    "x_hash_chunks__mutmut_20": x_hash_chunks__mutmut_20,
    "x_hash_chunks__mutmut_21": x_hash_chunks__mutmut_21,
    "x_hash_chunks__mutmut_22": x_hash_chunks__mutmut_22,
    "x_hash_chunks__mutmut_23": x_hash_chunks__mutmut_23,
}


def hash_chunks(*args, **kwargs):
    result = _mutmut_trampoline(x_hash_chunks__mutmut_orig, x_hash_chunks__mutmut_mutants, args, kwargs)
    return result


hash_chunks.__signature__ = _mutmut_signature(x_hash_chunks__mutmut_orig)
x_hash_chunks__mutmut_orig.__name__ = "x_hash_chunks"


# <3 🧱🤝🔒🪄
