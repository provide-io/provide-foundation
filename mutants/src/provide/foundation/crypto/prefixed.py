# provide/foundation/crypto/prefixed.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from provide.foundation.crypto.algorithms import DEFAULT_ALGORITHM, validate_algorithm
from provide.foundation.crypto.hashing import hash_data
from provide.foundation.logger import get_logger

"""Prefixed checksum format (algorithm:hexvalue) for self-describing checksums."""

log = get_logger(__name__)
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


def x_format_checksum__mutmut_orig(data: bytes, algorithm: str = DEFAULT_ALGORITHM) -> str:
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


def x_format_checksum__mutmut_1(data: bytes, algorithm: str = DEFAULT_ALGORITHM) -> str:
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
    if algorithm != "adler32":
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


def x_format_checksum__mutmut_2(data: bytes, algorithm: str = DEFAULT_ALGORITHM) -> str:
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
    if algorithm == "XXadler32XX":
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


def x_format_checksum__mutmut_3(data: bytes, algorithm: str = DEFAULT_ALGORITHM) -> str:
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
    if algorithm == "ADLER32":
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


def x_format_checksum__mutmut_4(data: bytes, algorithm: str = DEFAULT_ALGORITHM) -> str:
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

        checksum = None
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


def x_format_checksum__mutmut_5(data: bytes, algorithm: str = DEFAULT_ALGORITHM) -> str:
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

        checksum = zlib.adler32(data) | 0xFFFFFFFF
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


def x_format_checksum__mutmut_6(data: bytes, algorithm: str = DEFAULT_ALGORITHM) -> str:
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

        checksum = zlib.adler32(None) & 0xFFFFFFFF
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


def x_format_checksum__mutmut_7(data: bytes, algorithm: str = DEFAULT_ALGORITHM) -> str:
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

        checksum = zlib.adler32(data) & 4294967296
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


def x_format_checksum__mutmut_8(data: bytes, algorithm: str = DEFAULT_ALGORITHM) -> str:
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
        result = None
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


def x_format_checksum__mutmut_9(data: bytes, algorithm: str = DEFAULT_ALGORITHM) -> str:
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
            None,
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


def x_format_checksum__mutmut_10(data: bytes, algorithm: str = DEFAULT_ALGORITHM) -> str:
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
            size=None,
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


def x_format_checksum__mutmut_11(data: bytes, algorithm: str = DEFAULT_ALGORITHM) -> str:
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
            checksum=None,
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


def x_format_checksum__mutmut_12(data: bytes, algorithm: str = DEFAULT_ALGORITHM) -> str:
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


def x_format_checksum__mutmut_13(data: bytes, algorithm: str = DEFAULT_ALGORITHM) -> str:
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


def x_format_checksum__mutmut_14(data: bytes, algorithm: str = DEFAULT_ALGORITHM) -> str:
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


def x_format_checksum__mutmut_15(data: bytes, algorithm: str = DEFAULT_ALGORITHM) -> str:
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
            "XX🔐 Calculated adler32 checksumXX",
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


def x_format_checksum__mutmut_16(data: bytes, algorithm: str = DEFAULT_ALGORITHM) -> str:
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
            "🔐 calculated adler32 checksum",
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


def x_format_checksum__mutmut_17(data: bytes, algorithm: str = DEFAULT_ALGORITHM) -> str:
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
            "🔐 CALCULATED ADLER32 CHECKSUM",
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


def x_format_checksum__mutmut_18(data: bytes, algorithm: str = DEFAULT_ALGORITHM) -> str:
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
    validate_algorithm(None)
    digest = hash_data(data, algorithm)
    result = f"{algorithm}:{digest}"

    log.debug(
        "🔐 Calculated prefixed checksum",
        algorithm=algorithm,
        size=len(data),
        checksum=result[:40] + "...",
    )

    return result


def x_format_checksum__mutmut_19(data: bytes, algorithm: str = DEFAULT_ALGORITHM) -> str:
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
    digest = None
    result = f"{algorithm}:{digest}"

    log.debug(
        "🔐 Calculated prefixed checksum",
        algorithm=algorithm,
        size=len(data),
        checksum=result[:40] + "...",
    )

    return result


def x_format_checksum__mutmut_20(data: bytes, algorithm: str = DEFAULT_ALGORITHM) -> str:
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
    digest = hash_data(None, algorithm)
    result = f"{algorithm}:{digest}"

    log.debug(
        "🔐 Calculated prefixed checksum",
        algorithm=algorithm,
        size=len(data),
        checksum=result[:40] + "...",
    )

    return result


def x_format_checksum__mutmut_21(data: bytes, algorithm: str = DEFAULT_ALGORITHM) -> str:
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
    digest = hash_data(data, None)
    result = f"{algorithm}:{digest}"

    log.debug(
        "🔐 Calculated prefixed checksum",
        algorithm=algorithm,
        size=len(data),
        checksum=result[:40] + "...",
    )

    return result


def x_format_checksum__mutmut_22(data: bytes, algorithm: str = DEFAULT_ALGORITHM) -> str:
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
    digest = hash_data(algorithm)
    result = f"{algorithm}:{digest}"

    log.debug(
        "🔐 Calculated prefixed checksum",
        algorithm=algorithm,
        size=len(data),
        checksum=result[:40] + "...",
    )

    return result


def x_format_checksum__mutmut_23(data: bytes, algorithm: str = DEFAULT_ALGORITHM) -> str:
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
    digest = hash_data(
        data,
    )
    result = f"{algorithm}:{digest}"

    log.debug(
        "🔐 Calculated prefixed checksum",
        algorithm=algorithm,
        size=len(data),
        checksum=result[:40] + "...",
    )

    return result


def x_format_checksum__mutmut_24(data: bytes, algorithm: str = DEFAULT_ALGORITHM) -> str:
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
    result = None

    log.debug(
        "🔐 Calculated prefixed checksum",
        algorithm=algorithm,
        size=len(data),
        checksum=result[:40] + "...",
    )

    return result


def x_format_checksum__mutmut_25(data: bytes, algorithm: str = DEFAULT_ALGORITHM) -> str:
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
        None,
        algorithm=algorithm,
        size=len(data),
        checksum=result[:40] + "...",
    )

    return result


def x_format_checksum__mutmut_26(data: bytes, algorithm: str = DEFAULT_ALGORITHM) -> str:
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
        algorithm=None,
        size=len(data),
        checksum=result[:40] + "...",
    )

    return result


def x_format_checksum__mutmut_27(data: bytes, algorithm: str = DEFAULT_ALGORITHM) -> str:
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
        size=None,
        checksum=result[:40] + "...",
    )

    return result


def x_format_checksum__mutmut_28(data: bytes, algorithm: str = DEFAULT_ALGORITHM) -> str:
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
        checksum=None,
    )

    return result


def x_format_checksum__mutmut_29(data: bytes, algorithm: str = DEFAULT_ALGORITHM) -> str:
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
        algorithm=algorithm,
        size=len(data),
        checksum=result[:40] + "...",
    )

    return result


def x_format_checksum__mutmut_30(data: bytes, algorithm: str = DEFAULT_ALGORITHM) -> str:
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
        size=len(data),
        checksum=result[:40] + "...",
    )

    return result


def x_format_checksum__mutmut_31(data: bytes, algorithm: str = DEFAULT_ALGORITHM) -> str:
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
        checksum=result[:40] + "...",
    )

    return result


def x_format_checksum__mutmut_32(data: bytes, algorithm: str = DEFAULT_ALGORITHM) -> str:
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
    )

    return result


def x_format_checksum__mutmut_33(data: bytes, algorithm: str = DEFAULT_ALGORITHM) -> str:
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
        "XX🔐 Calculated prefixed checksumXX",
        algorithm=algorithm,
        size=len(data),
        checksum=result[:40] + "...",
    )

    return result


def x_format_checksum__mutmut_34(data: bytes, algorithm: str = DEFAULT_ALGORITHM) -> str:
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
        "🔐 calculated prefixed checksum",
        algorithm=algorithm,
        size=len(data),
        checksum=result[:40] + "...",
    )

    return result


def x_format_checksum__mutmut_35(data: bytes, algorithm: str = DEFAULT_ALGORITHM) -> str:
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
        "🔐 CALCULATED PREFIXED CHECKSUM",
        algorithm=algorithm,
        size=len(data),
        checksum=result[:40] + "...",
    )

    return result


def x_format_checksum__mutmut_36(data: bytes, algorithm: str = DEFAULT_ALGORITHM) -> str:
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
        checksum=result[:40] - "...",
    )

    return result


def x_format_checksum__mutmut_37(data: bytes, algorithm: str = DEFAULT_ALGORITHM) -> str:
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
        checksum=result[:41] + "...",
    )

    return result


def x_format_checksum__mutmut_38(data: bytes, algorithm: str = DEFAULT_ALGORITHM) -> str:
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
        checksum=result[:40] + "XX...XX",
    )

    return result


x_format_checksum__mutmut_mutants: ClassVar[MutantDict] = {
    "x_format_checksum__mutmut_1": x_format_checksum__mutmut_1,
    "x_format_checksum__mutmut_2": x_format_checksum__mutmut_2,
    "x_format_checksum__mutmut_3": x_format_checksum__mutmut_3,
    "x_format_checksum__mutmut_4": x_format_checksum__mutmut_4,
    "x_format_checksum__mutmut_5": x_format_checksum__mutmut_5,
    "x_format_checksum__mutmut_6": x_format_checksum__mutmut_6,
    "x_format_checksum__mutmut_7": x_format_checksum__mutmut_7,
    "x_format_checksum__mutmut_8": x_format_checksum__mutmut_8,
    "x_format_checksum__mutmut_9": x_format_checksum__mutmut_9,
    "x_format_checksum__mutmut_10": x_format_checksum__mutmut_10,
    "x_format_checksum__mutmut_11": x_format_checksum__mutmut_11,
    "x_format_checksum__mutmut_12": x_format_checksum__mutmut_12,
    "x_format_checksum__mutmut_13": x_format_checksum__mutmut_13,
    "x_format_checksum__mutmut_14": x_format_checksum__mutmut_14,
    "x_format_checksum__mutmut_15": x_format_checksum__mutmut_15,
    "x_format_checksum__mutmut_16": x_format_checksum__mutmut_16,
    "x_format_checksum__mutmut_17": x_format_checksum__mutmut_17,
    "x_format_checksum__mutmut_18": x_format_checksum__mutmut_18,
    "x_format_checksum__mutmut_19": x_format_checksum__mutmut_19,
    "x_format_checksum__mutmut_20": x_format_checksum__mutmut_20,
    "x_format_checksum__mutmut_21": x_format_checksum__mutmut_21,
    "x_format_checksum__mutmut_22": x_format_checksum__mutmut_22,
    "x_format_checksum__mutmut_23": x_format_checksum__mutmut_23,
    "x_format_checksum__mutmut_24": x_format_checksum__mutmut_24,
    "x_format_checksum__mutmut_25": x_format_checksum__mutmut_25,
    "x_format_checksum__mutmut_26": x_format_checksum__mutmut_26,
    "x_format_checksum__mutmut_27": x_format_checksum__mutmut_27,
    "x_format_checksum__mutmut_28": x_format_checksum__mutmut_28,
    "x_format_checksum__mutmut_29": x_format_checksum__mutmut_29,
    "x_format_checksum__mutmut_30": x_format_checksum__mutmut_30,
    "x_format_checksum__mutmut_31": x_format_checksum__mutmut_31,
    "x_format_checksum__mutmut_32": x_format_checksum__mutmut_32,
    "x_format_checksum__mutmut_33": x_format_checksum__mutmut_33,
    "x_format_checksum__mutmut_34": x_format_checksum__mutmut_34,
    "x_format_checksum__mutmut_35": x_format_checksum__mutmut_35,
    "x_format_checksum__mutmut_36": x_format_checksum__mutmut_36,
    "x_format_checksum__mutmut_37": x_format_checksum__mutmut_37,
    "x_format_checksum__mutmut_38": x_format_checksum__mutmut_38,
}


def format_checksum(*args, **kwargs):
    result = _mutmut_trampoline(
        x_format_checksum__mutmut_orig, x_format_checksum__mutmut_mutants, args, kwargs
    )
    return result


format_checksum.__signature__ = _mutmut_signature(x_format_checksum__mutmut_orig)
x_format_checksum__mutmut_orig.__name__ = "x_format_checksum"


def x_parse_checksum__mutmut_orig(checksum_str: str) -> tuple[str, str]:
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


def x_parse_checksum__mutmut_1(checksum_str: str) -> tuple[str, str]:
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
    if checksum_str:
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


def x_parse_checksum__mutmut_2(checksum_str: str) -> tuple[str, str]:
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
        raise ValueError(None)

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


def x_parse_checksum__mutmut_3(checksum_str: str) -> tuple[str, str]:
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
        raise ValueError("XXEmpty checksum stringXX")

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


def x_parse_checksum__mutmut_4(checksum_str: str) -> tuple[str, str]:
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
        raise ValueError("empty checksum string")

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


def x_parse_checksum__mutmut_5(checksum_str: str) -> tuple[str, str]:
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
        raise ValueError("EMPTY CHECKSUM STRING")

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


def x_parse_checksum__mutmut_6(checksum_str: str) -> tuple[str, str]:
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

    if "XX:XX" not in checksum_str:
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


def x_parse_checksum__mutmut_7(checksum_str: str) -> tuple[str, str]:
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

    if ":" in checksum_str:
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


def x_parse_checksum__mutmut_8(checksum_str: str) -> tuple[str, str]:
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
        raise ValueError(None)

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


def x_parse_checksum__mutmut_9(checksum_str: str) -> tuple[str, str]:
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

    parts = None
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


def x_parse_checksum__mutmut_10(checksum_str: str) -> tuple[str, str]:
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

    parts = checksum_str.split(None, 1)
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


def x_parse_checksum__mutmut_11(checksum_str: str) -> tuple[str, str]:
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

    parts = checksum_str.split(":", None)
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


def x_parse_checksum__mutmut_12(checksum_str: str) -> tuple[str, str]:
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

    parts = checksum_str.split(1)
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


def x_parse_checksum__mutmut_13(checksum_str: str) -> tuple[str, str]:
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

    parts = checksum_str.split(
        ":",
    )
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


def x_parse_checksum__mutmut_14(checksum_str: str) -> tuple[str, str]:
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

    parts = checksum_str.rsplit(":", 1)
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


def x_parse_checksum__mutmut_15(checksum_str: str) -> tuple[str, str]:
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

    parts = checksum_str.split("XX:XX", 1)
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


def x_parse_checksum__mutmut_16(checksum_str: str) -> tuple[str, str]:
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

    parts = checksum_str.split(":", 2)
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


def x_parse_checksum__mutmut_17(checksum_str: str) -> tuple[str, str]:
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
    if len(parts) == 2:
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


def x_parse_checksum__mutmut_18(checksum_str: str) -> tuple[str, str]:
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
    if len(parts) != 3:
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


def x_parse_checksum__mutmut_19(checksum_str: str) -> tuple[str, str]:
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
        raise ValueError(None)

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


def x_parse_checksum__mutmut_20(checksum_str: str) -> tuple[str, str]:
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

    algorithm, value = None

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


def x_parse_checksum__mutmut_21(checksum_str: str) -> tuple[str, str]:
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
    supported_algorithms = None
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


def x_parse_checksum__mutmut_22(checksum_str: str) -> tuple[str, str]:
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
    supported_algorithms = ["XXsha256XX", "sha512", "blake2b", "blake2s", "md5", "adler32"]
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


def x_parse_checksum__mutmut_23(checksum_str: str) -> tuple[str, str]:
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
    supported_algorithms = ["SHA256", "sha512", "blake2b", "blake2s", "md5", "adler32"]
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


def x_parse_checksum__mutmut_24(checksum_str: str) -> tuple[str, str]:
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
    supported_algorithms = ["sha256", "XXsha512XX", "blake2b", "blake2s", "md5", "adler32"]
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


def x_parse_checksum__mutmut_25(checksum_str: str) -> tuple[str, str]:
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
    supported_algorithms = ["sha256", "SHA512", "blake2b", "blake2s", "md5", "adler32"]
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


def x_parse_checksum__mutmut_26(checksum_str: str) -> tuple[str, str]:
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
    supported_algorithms = ["sha256", "sha512", "XXblake2bXX", "blake2s", "md5", "adler32"]
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


def x_parse_checksum__mutmut_27(checksum_str: str) -> tuple[str, str]:
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
    supported_algorithms = ["sha256", "sha512", "BLAKE2B", "blake2s", "md5", "adler32"]
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


def x_parse_checksum__mutmut_28(checksum_str: str) -> tuple[str, str]:
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
    supported_algorithms = ["sha256", "sha512", "blake2b", "XXblake2sXX", "md5", "adler32"]
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


def x_parse_checksum__mutmut_29(checksum_str: str) -> tuple[str, str]:
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
    supported_algorithms = ["sha256", "sha512", "blake2b", "BLAKE2S", "md5", "adler32"]
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


def x_parse_checksum__mutmut_30(checksum_str: str) -> tuple[str, str]:
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
    supported_algorithms = ["sha256", "sha512", "blake2b", "blake2s", "XXmd5XX", "adler32"]
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


def x_parse_checksum__mutmut_31(checksum_str: str) -> tuple[str, str]:
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
    supported_algorithms = ["sha256", "sha512", "blake2b", "blake2s", "MD5", "adler32"]
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


def x_parse_checksum__mutmut_32(checksum_str: str) -> tuple[str, str]:
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
    supported_algorithms = ["sha256", "sha512", "blake2b", "blake2s", "md5", "XXadler32XX"]
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


def x_parse_checksum__mutmut_33(checksum_str: str) -> tuple[str, str]:
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
    supported_algorithms = ["sha256", "sha512", "blake2b", "blake2s", "md5", "ADLER32"]
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


def x_parse_checksum__mutmut_34(checksum_str: str) -> tuple[str, str]:
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
    if algorithm in supported_algorithms:
        raise ValueError(
            f"Unknown checksum algorithm: {algorithm}. Supported: {', '.join(supported_algorithms)}"
        )

    log.debug(
        "📋 Parsed prefixed checksum",
        algorithm=algorithm,
        value=value[:16] + "...",
    )

    return algorithm, value


def x_parse_checksum__mutmut_35(checksum_str: str) -> tuple[str, str]:
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
        raise ValueError(None)

    log.debug(
        "📋 Parsed prefixed checksum",
        algorithm=algorithm,
        value=value[:16] + "...",
    )

    return algorithm, value


def x_parse_checksum__mutmut_36(checksum_str: str) -> tuple[str, str]:
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
        raise ValueError(f"Unknown checksum algorithm: {algorithm}. Supported: {', '.join(None)}")

    log.debug(
        "📋 Parsed prefixed checksum",
        algorithm=algorithm,
        value=value[:16] + "...",
    )

    return algorithm, value


def x_parse_checksum__mutmut_37(checksum_str: str) -> tuple[str, str]:
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
            f"Unknown checksum algorithm: {algorithm}. Supported: {'XX, XX'.join(supported_algorithms)}"
        )

    log.debug(
        "📋 Parsed prefixed checksum",
        algorithm=algorithm,
        value=value[:16] + "...",
    )

    return algorithm, value


def x_parse_checksum__mutmut_38(checksum_str: str) -> tuple[str, str]:
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
        None,
        algorithm=algorithm,
        value=value[:16] + "...",
    )

    return algorithm, value


def x_parse_checksum__mutmut_39(checksum_str: str) -> tuple[str, str]:
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
        algorithm=None,
        value=value[:16] + "...",
    )

    return algorithm, value


def x_parse_checksum__mutmut_40(checksum_str: str) -> tuple[str, str]:
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
        value=None,
    )

    return algorithm, value


def x_parse_checksum__mutmut_41(checksum_str: str) -> tuple[str, str]:
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
        algorithm=algorithm,
        value=value[:16] + "...",
    )

    return algorithm, value


def x_parse_checksum__mutmut_42(checksum_str: str) -> tuple[str, str]:
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
        value=value[:16] + "...",
    )

    return algorithm, value


def x_parse_checksum__mutmut_43(checksum_str: str) -> tuple[str, str]:
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
    )

    return algorithm, value


def x_parse_checksum__mutmut_44(checksum_str: str) -> tuple[str, str]:
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
        "XX📋 Parsed prefixed checksumXX",
        algorithm=algorithm,
        value=value[:16] + "...",
    )

    return algorithm, value


def x_parse_checksum__mutmut_45(checksum_str: str) -> tuple[str, str]:
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
        "📋 parsed prefixed checksum",
        algorithm=algorithm,
        value=value[:16] + "...",
    )

    return algorithm, value


def x_parse_checksum__mutmut_46(checksum_str: str) -> tuple[str, str]:
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
        "📋 PARSED PREFIXED CHECKSUM",
        algorithm=algorithm,
        value=value[:16] + "...",
    )

    return algorithm, value


def x_parse_checksum__mutmut_47(checksum_str: str) -> tuple[str, str]:
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
        value=value[:16] - "...",
    )

    return algorithm, value


def x_parse_checksum__mutmut_48(checksum_str: str) -> tuple[str, str]:
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
        value=value[:17] + "...",
    )

    return algorithm, value


def x_parse_checksum__mutmut_49(checksum_str: str) -> tuple[str, str]:
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
        value=value[:16] + "XX...XX",
    )

    return algorithm, value


x_parse_checksum__mutmut_mutants: ClassVar[MutantDict] = {
    "x_parse_checksum__mutmut_1": x_parse_checksum__mutmut_1,
    "x_parse_checksum__mutmut_2": x_parse_checksum__mutmut_2,
    "x_parse_checksum__mutmut_3": x_parse_checksum__mutmut_3,
    "x_parse_checksum__mutmut_4": x_parse_checksum__mutmut_4,
    "x_parse_checksum__mutmut_5": x_parse_checksum__mutmut_5,
    "x_parse_checksum__mutmut_6": x_parse_checksum__mutmut_6,
    "x_parse_checksum__mutmut_7": x_parse_checksum__mutmut_7,
    "x_parse_checksum__mutmut_8": x_parse_checksum__mutmut_8,
    "x_parse_checksum__mutmut_9": x_parse_checksum__mutmut_9,
    "x_parse_checksum__mutmut_10": x_parse_checksum__mutmut_10,
    "x_parse_checksum__mutmut_11": x_parse_checksum__mutmut_11,
    "x_parse_checksum__mutmut_12": x_parse_checksum__mutmut_12,
    "x_parse_checksum__mutmut_13": x_parse_checksum__mutmut_13,
    "x_parse_checksum__mutmut_14": x_parse_checksum__mutmut_14,
    "x_parse_checksum__mutmut_15": x_parse_checksum__mutmut_15,
    "x_parse_checksum__mutmut_16": x_parse_checksum__mutmut_16,
    "x_parse_checksum__mutmut_17": x_parse_checksum__mutmut_17,
    "x_parse_checksum__mutmut_18": x_parse_checksum__mutmut_18,
    "x_parse_checksum__mutmut_19": x_parse_checksum__mutmut_19,
    "x_parse_checksum__mutmut_20": x_parse_checksum__mutmut_20,
    "x_parse_checksum__mutmut_21": x_parse_checksum__mutmut_21,
    "x_parse_checksum__mutmut_22": x_parse_checksum__mutmut_22,
    "x_parse_checksum__mutmut_23": x_parse_checksum__mutmut_23,
    "x_parse_checksum__mutmut_24": x_parse_checksum__mutmut_24,
    "x_parse_checksum__mutmut_25": x_parse_checksum__mutmut_25,
    "x_parse_checksum__mutmut_26": x_parse_checksum__mutmut_26,
    "x_parse_checksum__mutmut_27": x_parse_checksum__mutmut_27,
    "x_parse_checksum__mutmut_28": x_parse_checksum__mutmut_28,
    "x_parse_checksum__mutmut_29": x_parse_checksum__mutmut_29,
    "x_parse_checksum__mutmut_30": x_parse_checksum__mutmut_30,
    "x_parse_checksum__mutmut_31": x_parse_checksum__mutmut_31,
    "x_parse_checksum__mutmut_32": x_parse_checksum__mutmut_32,
    "x_parse_checksum__mutmut_33": x_parse_checksum__mutmut_33,
    "x_parse_checksum__mutmut_34": x_parse_checksum__mutmut_34,
    "x_parse_checksum__mutmut_35": x_parse_checksum__mutmut_35,
    "x_parse_checksum__mutmut_36": x_parse_checksum__mutmut_36,
    "x_parse_checksum__mutmut_37": x_parse_checksum__mutmut_37,
    "x_parse_checksum__mutmut_38": x_parse_checksum__mutmut_38,
    "x_parse_checksum__mutmut_39": x_parse_checksum__mutmut_39,
    "x_parse_checksum__mutmut_40": x_parse_checksum__mutmut_40,
    "x_parse_checksum__mutmut_41": x_parse_checksum__mutmut_41,
    "x_parse_checksum__mutmut_42": x_parse_checksum__mutmut_42,
    "x_parse_checksum__mutmut_43": x_parse_checksum__mutmut_43,
    "x_parse_checksum__mutmut_44": x_parse_checksum__mutmut_44,
    "x_parse_checksum__mutmut_45": x_parse_checksum__mutmut_45,
    "x_parse_checksum__mutmut_46": x_parse_checksum__mutmut_46,
    "x_parse_checksum__mutmut_47": x_parse_checksum__mutmut_47,
    "x_parse_checksum__mutmut_48": x_parse_checksum__mutmut_48,
    "x_parse_checksum__mutmut_49": x_parse_checksum__mutmut_49,
}


def parse_checksum(*args, **kwargs):
    result = _mutmut_trampoline(x_parse_checksum__mutmut_orig, x_parse_checksum__mutmut_mutants, args, kwargs)
    return result


parse_checksum.__signature__ = _mutmut_signature(x_parse_checksum__mutmut_orig)
x_parse_checksum__mutmut_orig.__name__ = "x_parse_checksum"


def x_verify_checksum__mutmut_orig(data: bytes, checksum_str: str) -> bool:
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
                "✅ Prefixed checksum verified",
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


def x_verify_checksum__mutmut_1(data: bytes, checksum_str: str) -> bool:
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
        algorithm, expected_value = None
        actual_checksum = format_checksum(data, algorithm)
        actual_value = actual_checksum.split(":", 1)[1]

        matches = actual_value.lower() == expected_value.lower()

        if matches:
            log.debug(
                "✅ Prefixed checksum verified",
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


def x_verify_checksum__mutmut_2(data: bytes, checksum_str: str) -> bool:
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
        algorithm, expected_value = parse_checksum(None)
        actual_checksum = format_checksum(data, algorithm)
        actual_value = actual_checksum.split(":", 1)[1]

        matches = actual_value.lower() == expected_value.lower()

        if matches:
            log.debug(
                "✅ Prefixed checksum verified",
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


def x_verify_checksum__mutmut_3(data: bytes, checksum_str: str) -> bool:
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
        actual_checksum = None
        actual_value = actual_checksum.split(":", 1)[1]

        matches = actual_value.lower() == expected_value.lower()

        if matches:
            log.debug(
                "✅ Prefixed checksum verified",
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


def x_verify_checksum__mutmut_4(data: bytes, checksum_str: str) -> bool:
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
        actual_checksum = format_checksum(None, algorithm)
        actual_value = actual_checksum.split(":", 1)[1]

        matches = actual_value.lower() == expected_value.lower()

        if matches:
            log.debug(
                "✅ Prefixed checksum verified",
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


def x_verify_checksum__mutmut_5(data: bytes, checksum_str: str) -> bool:
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
        actual_checksum = format_checksum(data, None)
        actual_value = actual_checksum.split(":", 1)[1]

        matches = actual_value.lower() == expected_value.lower()

        if matches:
            log.debug(
                "✅ Prefixed checksum verified",
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


def x_verify_checksum__mutmut_6(data: bytes, checksum_str: str) -> bool:
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
        actual_checksum = format_checksum(algorithm)
        actual_value = actual_checksum.split(":", 1)[1]

        matches = actual_value.lower() == expected_value.lower()

        if matches:
            log.debug(
                "✅ Prefixed checksum verified",
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


def x_verify_checksum__mutmut_7(data: bytes, checksum_str: str) -> bool:
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
        actual_checksum = format_checksum(
            data,
        )
        actual_value = actual_checksum.split(":", 1)[1]

        matches = actual_value.lower() == expected_value.lower()

        if matches:
            log.debug(
                "✅ Prefixed checksum verified",
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


def x_verify_checksum__mutmut_8(data: bytes, checksum_str: str) -> bool:
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
        actual_value = None

        matches = actual_value.lower() == expected_value.lower()

        if matches:
            log.debug(
                "✅ Prefixed checksum verified",
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


def x_verify_checksum__mutmut_9(data: bytes, checksum_str: str) -> bool:
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
        actual_value = actual_checksum.split(None, 1)[1]

        matches = actual_value.lower() == expected_value.lower()

        if matches:
            log.debug(
                "✅ Prefixed checksum verified",
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


def x_verify_checksum__mutmut_10(data: bytes, checksum_str: str) -> bool:
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
        actual_value = actual_checksum.split(":", None)[1]

        matches = actual_value.lower() == expected_value.lower()

        if matches:
            log.debug(
                "✅ Prefixed checksum verified",
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


def x_verify_checksum__mutmut_11(data: bytes, checksum_str: str) -> bool:
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
        actual_value = actual_checksum.split(1)[1]

        matches = actual_value.lower() == expected_value.lower()

        if matches:
            log.debug(
                "✅ Prefixed checksum verified",
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


def x_verify_checksum__mutmut_12(data: bytes, checksum_str: str) -> bool:
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
        actual_value = actual_checksum.split(
            ":",
        )[1]

        matches = actual_value.lower() == expected_value.lower()

        if matches:
            log.debug(
                "✅ Prefixed checksum verified",
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


def x_verify_checksum__mutmut_13(data: bytes, checksum_str: str) -> bool:
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
        actual_value = actual_checksum.rsplit(":", 1)[1]

        matches = actual_value.lower() == expected_value.lower()

        if matches:
            log.debug(
                "✅ Prefixed checksum verified",
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


def x_verify_checksum__mutmut_14(data: bytes, checksum_str: str) -> bool:
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
        actual_value = actual_checksum.split("XX:XX", 1)[1]

        matches = actual_value.lower() == expected_value.lower()

        if matches:
            log.debug(
                "✅ Prefixed checksum verified",
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


def x_verify_checksum__mutmut_15(data: bytes, checksum_str: str) -> bool:
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
        actual_value = actual_checksum.split(":", 2)[1]

        matches = actual_value.lower() == expected_value.lower()

        if matches:
            log.debug(
                "✅ Prefixed checksum verified",
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


def x_verify_checksum__mutmut_16(data: bytes, checksum_str: str) -> bool:
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
        actual_value = actual_checksum.split(":", 1)[2]

        matches = actual_value.lower() == expected_value.lower()

        if matches:
            log.debug(
                "✅ Prefixed checksum verified",
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


def x_verify_checksum__mutmut_17(data: bytes, checksum_str: str) -> bool:
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

        matches = None

        if matches:
            log.debug(
                "✅ Prefixed checksum verified",
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


def x_verify_checksum__mutmut_18(data: bytes, checksum_str: str) -> bool:
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

        matches = actual_value.upper() == expected_value.lower()

        if matches:
            log.debug(
                "✅ Prefixed checksum verified",
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


def x_verify_checksum__mutmut_19(data: bytes, checksum_str: str) -> bool:
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

        matches = actual_value.lower() != expected_value.lower()

        if matches:
            log.debug(
                "✅ Prefixed checksum verified",
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


def x_verify_checksum__mutmut_20(data: bytes, checksum_str: str) -> bool:
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

        matches = actual_value.lower() == expected_value.upper()

        if matches:
            log.debug(
                "✅ Prefixed checksum verified",
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


def x_verify_checksum__mutmut_21(data: bytes, checksum_str: str) -> bool:
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
                None,
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


def x_verify_checksum__mutmut_22(data: bytes, checksum_str: str) -> bool:
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
                "✅ Prefixed checksum verified",
                algorithm=None,
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


def x_verify_checksum__mutmut_23(data: bytes, checksum_str: str) -> bool:
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
                "✅ Prefixed checksum verified",
                algorithm=algorithm,
                size=None,
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


def x_verify_checksum__mutmut_24(data: bytes, checksum_str: str) -> bool:
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


def x_verify_checksum__mutmut_25(data: bytes, checksum_str: str) -> bool:
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
                "✅ Prefixed checksum verified",
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


def x_verify_checksum__mutmut_26(data: bytes, checksum_str: str) -> bool:
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
                "✅ Prefixed checksum verified",
                algorithm=algorithm,
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


def x_verify_checksum__mutmut_27(data: bytes, checksum_str: str) -> bool:
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
                "XX✅ Prefixed checksum verifiedXX",
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


def x_verify_checksum__mutmut_28(data: bytes, checksum_str: str) -> bool:
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
                "✅ prefixed checksum verified",
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


def x_verify_checksum__mutmut_29(data: bytes, checksum_str: str) -> bool:
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
                "✅ PREFIXED CHECKSUM VERIFIED",
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


def x_verify_checksum__mutmut_30(data: bytes, checksum_str: str) -> bool:
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
                "✅ Prefixed checksum verified",
                algorithm=algorithm,
                size=len(data),
            )
        else:
            log.warning(
                None,
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


def x_verify_checksum__mutmut_31(data: bytes, checksum_str: str) -> bool:
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
                "✅ Prefixed checksum verified",
                algorithm=algorithm,
                size=len(data),
            )
        else:
            log.warning(
                "❌ Prefixed checksum mismatch",
                algorithm=None,
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


def x_verify_checksum__mutmut_32(data: bytes, checksum_str: str) -> bool:
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
                "✅ Prefixed checksum verified",
                algorithm=algorithm,
                size=len(data),
            )
        else:
            log.warning(
                "❌ Prefixed checksum mismatch",
                algorithm=algorithm,
                expected=None,
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


def x_verify_checksum__mutmut_33(data: bytes, checksum_str: str) -> bool:
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
                "✅ Prefixed checksum verified",
                algorithm=algorithm,
                size=len(data),
            )
        else:
            log.warning(
                "❌ Prefixed checksum mismatch",
                algorithm=algorithm,
                expected=expected_value[:16] + "...",
                actual=None,
            )

        return matches

    except (ValueError, Exception) as e:
        log.warning(
            "❌ Checksum verification failed",
            error=str(e),
            checksum=checksum_str[:40] + "...",
        )
        return False


def x_verify_checksum__mutmut_34(data: bytes, checksum_str: str) -> bool:
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
                "✅ Prefixed checksum verified",
                algorithm=algorithm,
                size=len(data),
            )
        else:
            log.warning(
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


def x_verify_checksum__mutmut_35(data: bytes, checksum_str: str) -> bool:
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
                "✅ Prefixed checksum verified",
                algorithm=algorithm,
                size=len(data),
            )
        else:
            log.warning(
                "❌ Prefixed checksum mismatch",
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


def x_verify_checksum__mutmut_36(data: bytes, checksum_str: str) -> bool:
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
                "✅ Prefixed checksum verified",
                algorithm=algorithm,
                size=len(data),
            )
        else:
            log.warning(
                "❌ Prefixed checksum mismatch",
                algorithm=algorithm,
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


def x_verify_checksum__mutmut_37(data: bytes, checksum_str: str) -> bool:
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
                "✅ Prefixed checksum verified",
                algorithm=algorithm,
                size=len(data),
            )
        else:
            log.warning(
                "❌ Prefixed checksum mismatch",
                algorithm=algorithm,
                expected=expected_value[:16] + "...",
            )

        return matches

    except (ValueError, Exception) as e:
        log.warning(
            "❌ Checksum verification failed",
            error=str(e),
            checksum=checksum_str[:40] + "...",
        )
        return False


def x_verify_checksum__mutmut_38(data: bytes, checksum_str: str) -> bool:
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
                "✅ Prefixed checksum verified",
                algorithm=algorithm,
                size=len(data),
            )
        else:
            log.warning(
                "XX❌ Prefixed checksum mismatchXX",
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


def x_verify_checksum__mutmut_39(data: bytes, checksum_str: str) -> bool:
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
                "✅ Prefixed checksum verified",
                algorithm=algorithm,
                size=len(data),
            )
        else:
            log.warning(
                "❌ prefixed checksum mismatch",
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


def x_verify_checksum__mutmut_40(data: bytes, checksum_str: str) -> bool:
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
                "✅ Prefixed checksum verified",
                algorithm=algorithm,
                size=len(data),
            )
        else:
            log.warning(
                "❌ PREFIXED CHECKSUM MISMATCH",
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


def x_verify_checksum__mutmut_41(data: bytes, checksum_str: str) -> bool:
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
                "✅ Prefixed checksum verified",
                algorithm=algorithm,
                size=len(data),
            )
        else:
            log.warning(
                "❌ Prefixed checksum mismatch",
                algorithm=algorithm,
                expected=expected_value[:16] - "...",
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


def x_verify_checksum__mutmut_42(data: bytes, checksum_str: str) -> bool:
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
                "✅ Prefixed checksum verified",
                algorithm=algorithm,
                size=len(data),
            )
        else:
            log.warning(
                "❌ Prefixed checksum mismatch",
                algorithm=algorithm,
                expected=expected_value[:17] + "...",
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


def x_verify_checksum__mutmut_43(data: bytes, checksum_str: str) -> bool:
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
                "✅ Prefixed checksum verified",
                algorithm=algorithm,
                size=len(data),
            )
        else:
            log.warning(
                "❌ Prefixed checksum mismatch",
                algorithm=algorithm,
                expected=expected_value[:16] + "XX...XX",
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


def x_verify_checksum__mutmut_44(data: bytes, checksum_str: str) -> bool:
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
                "✅ Prefixed checksum verified",
                algorithm=algorithm,
                size=len(data),
            )
        else:
            log.warning(
                "❌ Prefixed checksum mismatch",
                algorithm=algorithm,
                expected=expected_value[:16] + "...",
                actual=actual_value[:16] - "...",
            )

        return matches

    except (ValueError, Exception) as e:
        log.warning(
            "❌ Checksum verification failed",
            error=str(e),
            checksum=checksum_str[:40] + "...",
        )
        return False


def x_verify_checksum__mutmut_45(data: bytes, checksum_str: str) -> bool:
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
                "✅ Prefixed checksum verified",
                algorithm=algorithm,
                size=len(data),
            )
        else:
            log.warning(
                "❌ Prefixed checksum mismatch",
                algorithm=algorithm,
                expected=expected_value[:16] + "...",
                actual=actual_value[:17] + "...",
            )

        return matches

    except (ValueError, Exception) as e:
        log.warning(
            "❌ Checksum verification failed",
            error=str(e),
            checksum=checksum_str[:40] + "...",
        )
        return False


def x_verify_checksum__mutmut_46(data: bytes, checksum_str: str) -> bool:
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
                "✅ Prefixed checksum verified",
                algorithm=algorithm,
                size=len(data),
            )
        else:
            log.warning(
                "❌ Prefixed checksum mismatch",
                algorithm=algorithm,
                expected=expected_value[:16] + "...",
                actual=actual_value[:16] + "XX...XX",
            )

        return matches

    except (ValueError, Exception) as e:
        log.warning(
            "❌ Checksum verification failed",
            error=str(e),
            checksum=checksum_str[:40] + "...",
        )
        return False


def x_verify_checksum__mutmut_47(data: bytes, checksum_str: str) -> bool:
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
                "✅ Prefixed checksum verified",
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
            None,
            error=str(e),
            checksum=checksum_str[:40] + "...",
        )
        return False


def x_verify_checksum__mutmut_48(data: bytes, checksum_str: str) -> bool:
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
                "✅ Prefixed checksum verified",
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
            error=None,
            checksum=checksum_str[:40] + "...",
        )
        return False


def x_verify_checksum__mutmut_49(data: bytes, checksum_str: str) -> bool:
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
                "✅ Prefixed checksum verified",
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
            checksum=None,
        )
        return False


def x_verify_checksum__mutmut_50(data: bytes, checksum_str: str) -> bool:
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
                "✅ Prefixed checksum verified",
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
            error=str(e),
            checksum=checksum_str[:40] + "...",
        )
        return False


def x_verify_checksum__mutmut_51(data: bytes, checksum_str: str) -> bool:
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
                "✅ Prefixed checksum verified",
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
            checksum=checksum_str[:40] + "...",
        )
        return False


def x_verify_checksum__mutmut_52(data: bytes, checksum_str: str) -> bool:
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
                "✅ Prefixed checksum verified",
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
        )
        return False


def x_verify_checksum__mutmut_53(data: bytes, checksum_str: str) -> bool:
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
                "✅ Prefixed checksum verified",
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
            "XX❌ Checksum verification failedXX",
            error=str(e),
            checksum=checksum_str[:40] + "...",
        )
        return False


def x_verify_checksum__mutmut_54(data: bytes, checksum_str: str) -> bool:
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
                "✅ Prefixed checksum verified",
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
            "❌ checksum verification failed",
            error=str(e),
            checksum=checksum_str[:40] + "...",
        )
        return False


def x_verify_checksum__mutmut_55(data: bytes, checksum_str: str) -> bool:
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
                "✅ Prefixed checksum verified",
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
            "❌ CHECKSUM VERIFICATION FAILED",
            error=str(e),
            checksum=checksum_str[:40] + "...",
        )
        return False


def x_verify_checksum__mutmut_56(data: bytes, checksum_str: str) -> bool:
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
                "✅ Prefixed checksum verified",
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
            error=str(None),
            checksum=checksum_str[:40] + "...",
        )
        return False


def x_verify_checksum__mutmut_57(data: bytes, checksum_str: str) -> bool:
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
                "✅ Prefixed checksum verified",
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
            checksum=checksum_str[:40] - "...",
        )
        return False


def x_verify_checksum__mutmut_58(data: bytes, checksum_str: str) -> bool:
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
                "✅ Prefixed checksum verified",
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
            checksum=checksum_str[:41] + "...",
        )
        return False


def x_verify_checksum__mutmut_59(data: bytes, checksum_str: str) -> bool:
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
                "✅ Prefixed checksum verified",
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
            checksum=checksum_str[:40] + "XX...XX",
        )
        return False


def x_verify_checksum__mutmut_60(data: bytes, checksum_str: str) -> bool:
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
                "✅ Prefixed checksum verified",
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
        return True


x_verify_checksum__mutmut_mutants: ClassVar[MutantDict] = {
    "x_verify_checksum__mutmut_1": x_verify_checksum__mutmut_1,
    "x_verify_checksum__mutmut_2": x_verify_checksum__mutmut_2,
    "x_verify_checksum__mutmut_3": x_verify_checksum__mutmut_3,
    "x_verify_checksum__mutmut_4": x_verify_checksum__mutmut_4,
    "x_verify_checksum__mutmut_5": x_verify_checksum__mutmut_5,
    "x_verify_checksum__mutmut_6": x_verify_checksum__mutmut_6,
    "x_verify_checksum__mutmut_7": x_verify_checksum__mutmut_7,
    "x_verify_checksum__mutmut_8": x_verify_checksum__mutmut_8,
    "x_verify_checksum__mutmut_9": x_verify_checksum__mutmut_9,
    "x_verify_checksum__mutmut_10": x_verify_checksum__mutmut_10,
    "x_verify_checksum__mutmut_11": x_verify_checksum__mutmut_11,
    "x_verify_checksum__mutmut_12": x_verify_checksum__mutmut_12,
    "x_verify_checksum__mutmut_13": x_verify_checksum__mutmut_13,
    "x_verify_checksum__mutmut_14": x_verify_checksum__mutmut_14,
    "x_verify_checksum__mutmut_15": x_verify_checksum__mutmut_15,
    "x_verify_checksum__mutmut_16": x_verify_checksum__mutmut_16,
    "x_verify_checksum__mutmut_17": x_verify_checksum__mutmut_17,
    "x_verify_checksum__mutmut_18": x_verify_checksum__mutmut_18,
    "x_verify_checksum__mutmut_19": x_verify_checksum__mutmut_19,
    "x_verify_checksum__mutmut_20": x_verify_checksum__mutmut_20,
    "x_verify_checksum__mutmut_21": x_verify_checksum__mutmut_21,
    "x_verify_checksum__mutmut_22": x_verify_checksum__mutmut_22,
    "x_verify_checksum__mutmut_23": x_verify_checksum__mutmut_23,
    "x_verify_checksum__mutmut_24": x_verify_checksum__mutmut_24,
    "x_verify_checksum__mutmut_25": x_verify_checksum__mutmut_25,
    "x_verify_checksum__mutmut_26": x_verify_checksum__mutmut_26,
    "x_verify_checksum__mutmut_27": x_verify_checksum__mutmut_27,
    "x_verify_checksum__mutmut_28": x_verify_checksum__mutmut_28,
    "x_verify_checksum__mutmut_29": x_verify_checksum__mutmut_29,
    "x_verify_checksum__mutmut_30": x_verify_checksum__mutmut_30,
    "x_verify_checksum__mutmut_31": x_verify_checksum__mutmut_31,
    "x_verify_checksum__mutmut_32": x_verify_checksum__mutmut_32,
    "x_verify_checksum__mutmut_33": x_verify_checksum__mutmut_33,
    "x_verify_checksum__mutmut_34": x_verify_checksum__mutmut_34,
    "x_verify_checksum__mutmut_35": x_verify_checksum__mutmut_35,
    "x_verify_checksum__mutmut_36": x_verify_checksum__mutmut_36,
    "x_verify_checksum__mutmut_37": x_verify_checksum__mutmut_37,
    "x_verify_checksum__mutmut_38": x_verify_checksum__mutmut_38,
    "x_verify_checksum__mutmut_39": x_verify_checksum__mutmut_39,
    "x_verify_checksum__mutmut_40": x_verify_checksum__mutmut_40,
    "x_verify_checksum__mutmut_41": x_verify_checksum__mutmut_41,
    "x_verify_checksum__mutmut_42": x_verify_checksum__mutmut_42,
    "x_verify_checksum__mutmut_43": x_verify_checksum__mutmut_43,
    "x_verify_checksum__mutmut_44": x_verify_checksum__mutmut_44,
    "x_verify_checksum__mutmut_45": x_verify_checksum__mutmut_45,
    "x_verify_checksum__mutmut_46": x_verify_checksum__mutmut_46,
    "x_verify_checksum__mutmut_47": x_verify_checksum__mutmut_47,
    "x_verify_checksum__mutmut_48": x_verify_checksum__mutmut_48,
    "x_verify_checksum__mutmut_49": x_verify_checksum__mutmut_49,
    "x_verify_checksum__mutmut_50": x_verify_checksum__mutmut_50,
    "x_verify_checksum__mutmut_51": x_verify_checksum__mutmut_51,
    "x_verify_checksum__mutmut_52": x_verify_checksum__mutmut_52,
    "x_verify_checksum__mutmut_53": x_verify_checksum__mutmut_53,
    "x_verify_checksum__mutmut_54": x_verify_checksum__mutmut_54,
    "x_verify_checksum__mutmut_55": x_verify_checksum__mutmut_55,
    "x_verify_checksum__mutmut_56": x_verify_checksum__mutmut_56,
    "x_verify_checksum__mutmut_57": x_verify_checksum__mutmut_57,
    "x_verify_checksum__mutmut_58": x_verify_checksum__mutmut_58,
    "x_verify_checksum__mutmut_59": x_verify_checksum__mutmut_59,
    "x_verify_checksum__mutmut_60": x_verify_checksum__mutmut_60,
}


def verify_checksum(*args, **kwargs):
    result = _mutmut_trampoline(
        x_verify_checksum__mutmut_orig, x_verify_checksum__mutmut_mutants, args, kwargs
    )
    return result


verify_checksum.__signature__ = _mutmut_signature(x_verify_checksum__mutmut_orig)
x_verify_checksum__mutmut_orig.__name__ = "x_verify_checksum"


def x_normalize_checksum__mutmut_orig(checksum_str: str) -> str:
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


def x_normalize_checksum__mutmut_1(checksum_str: str) -> str:
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
    algorithm, value = None
    normalized = f"{algorithm}:{value.lower()}"

    log.debug(
        "🔄 Normalized checksum",
        input=checksum_str[:40] + "...",
        output=normalized[:40] + "...",
    )

    return normalized


def x_normalize_checksum__mutmut_2(checksum_str: str) -> str:
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
    algorithm, value = parse_checksum(None)
    normalized = f"{algorithm}:{value.lower()}"

    log.debug(
        "🔄 Normalized checksum",
        input=checksum_str[:40] + "...",
        output=normalized[:40] + "...",
    )

    return normalized


def x_normalize_checksum__mutmut_3(checksum_str: str) -> str:
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
    normalized = None

    log.debug(
        "🔄 Normalized checksum",
        input=checksum_str[:40] + "...",
        output=normalized[:40] + "...",
    )

    return normalized


def x_normalize_checksum__mutmut_4(checksum_str: str) -> str:
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
    normalized = f"{algorithm}:{value.upper()}"

    log.debug(
        "🔄 Normalized checksum",
        input=checksum_str[:40] + "...",
        output=normalized[:40] + "...",
    )

    return normalized


def x_normalize_checksum__mutmut_5(checksum_str: str) -> str:
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
        None,
        input=checksum_str[:40] + "...",
        output=normalized[:40] + "...",
    )

    return normalized


def x_normalize_checksum__mutmut_6(checksum_str: str) -> str:
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
        input=None,
        output=normalized[:40] + "...",
    )

    return normalized


def x_normalize_checksum__mutmut_7(checksum_str: str) -> str:
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
        output=None,
    )

    return normalized


def x_normalize_checksum__mutmut_8(checksum_str: str) -> str:
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
        input=checksum_str[:40] + "...",
        output=normalized[:40] + "...",
    )

    return normalized


def x_normalize_checksum__mutmut_9(checksum_str: str) -> str:
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
        output=normalized[:40] + "...",
    )

    return normalized


def x_normalize_checksum__mutmut_10(checksum_str: str) -> str:
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
    )

    return normalized


def x_normalize_checksum__mutmut_11(checksum_str: str) -> str:
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
        "XX🔄 Normalized checksumXX",
        input=checksum_str[:40] + "...",
        output=normalized[:40] + "...",
    )

    return normalized


def x_normalize_checksum__mutmut_12(checksum_str: str) -> str:
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
        "🔄 normalized checksum",
        input=checksum_str[:40] + "...",
        output=normalized[:40] + "...",
    )

    return normalized


def x_normalize_checksum__mutmut_13(checksum_str: str) -> str:
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
        "🔄 NORMALIZED CHECKSUM",
        input=checksum_str[:40] + "...",
        output=normalized[:40] + "...",
    )

    return normalized


def x_normalize_checksum__mutmut_14(checksum_str: str) -> str:
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
        input=checksum_str[:40] - "...",
        output=normalized[:40] + "...",
    )

    return normalized


def x_normalize_checksum__mutmut_15(checksum_str: str) -> str:
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
        input=checksum_str[:41] + "...",
        output=normalized[:40] + "...",
    )

    return normalized


def x_normalize_checksum__mutmut_16(checksum_str: str) -> str:
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
        input=checksum_str[:40] + "XX...XX",
        output=normalized[:40] + "...",
    )

    return normalized


def x_normalize_checksum__mutmut_17(checksum_str: str) -> str:
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
        output=normalized[:40] - "...",
    )

    return normalized


def x_normalize_checksum__mutmut_18(checksum_str: str) -> str:
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
        output=normalized[:41] + "...",
    )

    return normalized


def x_normalize_checksum__mutmut_19(checksum_str: str) -> str:
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
        output=normalized[:40] + "XX...XX",
    )

    return normalized


x_normalize_checksum__mutmut_mutants: ClassVar[MutantDict] = {
    "x_normalize_checksum__mutmut_1": x_normalize_checksum__mutmut_1,
    "x_normalize_checksum__mutmut_2": x_normalize_checksum__mutmut_2,
    "x_normalize_checksum__mutmut_3": x_normalize_checksum__mutmut_3,
    "x_normalize_checksum__mutmut_4": x_normalize_checksum__mutmut_4,
    "x_normalize_checksum__mutmut_5": x_normalize_checksum__mutmut_5,
    "x_normalize_checksum__mutmut_6": x_normalize_checksum__mutmut_6,
    "x_normalize_checksum__mutmut_7": x_normalize_checksum__mutmut_7,
    "x_normalize_checksum__mutmut_8": x_normalize_checksum__mutmut_8,
    "x_normalize_checksum__mutmut_9": x_normalize_checksum__mutmut_9,
    "x_normalize_checksum__mutmut_10": x_normalize_checksum__mutmut_10,
    "x_normalize_checksum__mutmut_11": x_normalize_checksum__mutmut_11,
    "x_normalize_checksum__mutmut_12": x_normalize_checksum__mutmut_12,
    "x_normalize_checksum__mutmut_13": x_normalize_checksum__mutmut_13,
    "x_normalize_checksum__mutmut_14": x_normalize_checksum__mutmut_14,
    "x_normalize_checksum__mutmut_15": x_normalize_checksum__mutmut_15,
    "x_normalize_checksum__mutmut_16": x_normalize_checksum__mutmut_16,
    "x_normalize_checksum__mutmut_17": x_normalize_checksum__mutmut_17,
    "x_normalize_checksum__mutmut_18": x_normalize_checksum__mutmut_18,
    "x_normalize_checksum__mutmut_19": x_normalize_checksum__mutmut_19,
}


def normalize_checksum(*args, **kwargs):
    result = _mutmut_trampoline(
        x_normalize_checksum__mutmut_orig, x_normalize_checksum__mutmut_mutants, args, kwargs
    )
    return result


normalize_checksum.__signature__ = _mutmut_signature(x_normalize_checksum__mutmut_orig)
x_normalize_checksum__mutmut_orig.__name__ = "x_normalize_checksum"


def x_is_strong_checksum__mutmut_orig(checksum_str: str) -> bool:
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


def x_is_strong_checksum__mutmut_1(checksum_str: str) -> bool:
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
        algorithm, _ = None
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


def x_is_strong_checksum__mutmut_2(checksum_str: str) -> bool:
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
        algorithm, _ = parse_checksum(None)
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


def x_is_strong_checksum__mutmut_3(checksum_str: str) -> bool:
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
        strong_algorithms = None
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


def x_is_strong_checksum__mutmut_4(checksum_str: str) -> bool:
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
        strong_algorithms = {"XXsha256XX", "sha512", "blake2b", "blake2s"}
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


def x_is_strong_checksum__mutmut_5(checksum_str: str) -> bool:
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
        strong_algorithms = {"SHA256", "sha512", "blake2b", "blake2s"}
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


def x_is_strong_checksum__mutmut_6(checksum_str: str) -> bool:
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
        strong_algorithms = {"sha256", "XXsha512XX", "blake2b", "blake2s"}
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


def x_is_strong_checksum__mutmut_7(checksum_str: str) -> bool:
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
        strong_algorithms = {"sha256", "SHA512", "blake2b", "blake2s"}
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


def x_is_strong_checksum__mutmut_8(checksum_str: str) -> bool:
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
        strong_algorithms = {"sha256", "sha512", "XXblake2bXX", "blake2s"}
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


def x_is_strong_checksum__mutmut_9(checksum_str: str) -> bool:
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
        strong_algorithms = {"sha256", "sha512", "BLAKE2B", "blake2s"}
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


def x_is_strong_checksum__mutmut_10(checksum_str: str) -> bool:
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
        strong_algorithms = {"sha256", "sha512", "blake2b", "XXblake2sXX"}
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


def x_is_strong_checksum__mutmut_11(checksum_str: str) -> bool:
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
        strong_algorithms = {"sha256", "sha512", "blake2b", "BLAKE2S"}
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


def x_is_strong_checksum__mutmut_12(checksum_str: str) -> bool:
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
        is_strong = None

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


def x_is_strong_checksum__mutmut_13(checksum_str: str) -> bool:
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
        is_strong = algorithm not in strong_algorithms

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


def x_is_strong_checksum__mutmut_14(checksum_str: str) -> bool:
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
            None,
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


def x_is_strong_checksum__mutmut_15(checksum_str: str) -> bool:
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
            algorithm=None,
            is_strong=is_strong,
        )

        return is_strong

    except ValueError:
        log.warning(
            "⚠️ Cannot determine checksum strength - invalid format",
            checksum=checksum_str[:40] + "...",
        )
        return False


def x_is_strong_checksum__mutmut_16(checksum_str: str) -> bool:
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
            is_strong=None,
        )

        return is_strong

    except ValueError:
        log.warning(
            "⚠️ Cannot determine checksum strength - invalid format",
            checksum=checksum_str[:40] + "...",
        )
        return False


def x_is_strong_checksum__mutmut_17(checksum_str: str) -> bool:
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


def x_is_strong_checksum__mutmut_18(checksum_str: str) -> bool:
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
            is_strong=is_strong,
        )

        return is_strong

    except ValueError:
        log.warning(
            "⚠️ Cannot determine checksum strength - invalid format",
            checksum=checksum_str[:40] + "...",
        )
        return False


def x_is_strong_checksum__mutmut_19(checksum_str: str) -> bool:
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
        )

        return is_strong

    except ValueError:
        log.warning(
            "⚠️ Cannot determine checksum strength - invalid format",
            checksum=checksum_str[:40] + "...",
        )
        return False


def x_is_strong_checksum__mutmut_20(checksum_str: str) -> bool:
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
            "XX🔒 Checked checksum strengthXX",
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


def x_is_strong_checksum__mutmut_21(checksum_str: str) -> bool:
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
            "🔒 checked checksum strength",
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


def x_is_strong_checksum__mutmut_22(checksum_str: str) -> bool:
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
            "🔒 CHECKED CHECKSUM STRENGTH",
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


def x_is_strong_checksum__mutmut_23(checksum_str: str) -> bool:
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
            None,
            checksum=checksum_str[:40] + "...",
        )
        return False


def x_is_strong_checksum__mutmut_24(checksum_str: str) -> bool:
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
            checksum=None,
        )
        return False


def x_is_strong_checksum__mutmut_25(checksum_str: str) -> bool:
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
            checksum=checksum_str[:40] + "...",
        )
        return False


def x_is_strong_checksum__mutmut_26(checksum_str: str) -> bool:
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
        )
        return False


def x_is_strong_checksum__mutmut_27(checksum_str: str) -> bool:
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
            "XX⚠️ Cannot determine checksum strength - invalid formatXX",
            checksum=checksum_str[:40] + "...",
        )
        return False


def x_is_strong_checksum__mutmut_28(checksum_str: str) -> bool:
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
            "⚠️ cannot determine checksum strength - invalid format",
            checksum=checksum_str[:40] + "...",
        )
        return False


def x_is_strong_checksum__mutmut_29(checksum_str: str) -> bool:
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
            "⚠️ CANNOT DETERMINE CHECKSUM STRENGTH - INVALID FORMAT",
            checksum=checksum_str[:40] + "...",
        )
        return False


def x_is_strong_checksum__mutmut_30(checksum_str: str) -> bool:
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
            checksum=checksum_str[:40] - "...",
        )
        return False


def x_is_strong_checksum__mutmut_31(checksum_str: str) -> bool:
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
            checksum=checksum_str[:41] + "...",
        )
        return False


def x_is_strong_checksum__mutmut_32(checksum_str: str) -> bool:
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
            checksum=checksum_str[:40] + "XX...XX",
        )
        return False


def x_is_strong_checksum__mutmut_33(checksum_str: str) -> bool:
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
        return True


x_is_strong_checksum__mutmut_mutants: ClassVar[MutantDict] = {
    "x_is_strong_checksum__mutmut_1": x_is_strong_checksum__mutmut_1,
    "x_is_strong_checksum__mutmut_2": x_is_strong_checksum__mutmut_2,
    "x_is_strong_checksum__mutmut_3": x_is_strong_checksum__mutmut_3,
    "x_is_strong_checksum__mutmut_4": x_is_strong_checksum__mutmut_4,
    "x_is_strong_checksum__mutmut_5": x_is_strong_checksum__mutmut_5,
    "x_is_strong_checksum__mutmut_6": x_is_strong_checksum__mutmut_6,
    "x_is_strong_checksum__mutmut_7": x_is_strong_checksum__mutmut_7,
    "x_is_strong_checksum__mutmut_8": x_is_strong_checksum__mutmut_8,
    "x_is_strong_checksum__mutmut_9": x_is_strong_checksum__mutmut_9,
    "x_is_strong_checksum__mutmut_10": x_is_strong_checksum__mutmut_10,
    "x_is_strong_checksum__mutmut_11": x_is_strong_checksum__mutmut_11,
    "x_is_strong_checksum__mutmut_12": x_is_strong_checksum__mutmut_12,
    "x_is_strong_checksum__mutmut_13": x_is_strong_checksum__mutmut_13,
    "x_is_strong_checksum__mutmut_14": x_is_strong_checksum__mutmut_14,
    "x_is_strong_checksum__mutmut_15": x_is_strong_checksum__mutmut_15,
    "x_is_strong_checksum__mutmut_16": x_is_strong_checksum__mutmut_16,
    "x_is_strong_checksum__mutmut_17": x_is_strong_checksum__mutmut_17,
    "x_is_strong_checksum__mutmut_18": x_is_strong_checksum__mutmut_18,
    "x_is_strong_checksum__mutmut_19": x_is_strong_checksum__mutmut_19,
    "x_is_strong_checksum__mutmut_20": x_is_strong_checksum__mutmut_20,
    "x_is_strong_checksum__mutmut_21": x_is_strong_checksum__mutmut_21,
    "x_is_strong_checksum__mutmut_22": x_is_strong_checksum__mutmut_22,
    "x_is_strong_checksum__mutmut_23": x_is_strong_checksum__mutmut_23,
    "x_is_strong_checksum__mutmut_24": x_is_strong_checksum__mutmut_24,
    "x_is_strong_checksum__mutmut_25": x_is_strong_checksum__mutmut_25,
    "x_is_strong_checksum__mutmut_26": x_is_strong_checksum__mutmut_26,
    "x_is_strong_checksum__mutmut_27": x_is_strong_checksum__mutmut_27,
    "x_is_strong_checksum__mutmut_28": x_is_strong_checksum__mutmut_28,
    "x_is_strong_checksum__mutmut_29": x_is_strong_checksum__mutmut_29,
    "x_is_strong_checksum__mutmut_30": x_is_strong_checksum__mutmut_30,
    "x_is_strong_checksum__mutmut_31": x_is_strong_checksum__mutmut_31,
    "x_is_strong_checksum__mutmut_32": x_is_strong_checksum__mutmut_32,
    "x_is_strong_checksum__mutmut_33": x_is_strong_checksum__mutmut_33,
}


def is_strong_checksum(*args, **kwargs):
    result = _mutmut_trampoline(
        x_is_strong_checksum__mutmut_orig, x_is_strong_checksum__mutmut_mutants, args, kwargs
    )
    return result


is_strong_checksum.__signature__ = _mutmut_signature(x_is_strong_checksum__mutmut_orig)
x_is_strong_checksum__mutmut_orig.__name__ = "x_is_strong_checksum"


# <3 🧱🤝🔒🪄
