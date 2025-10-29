# provide/foundation/crypto/checksums.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from pathlib import Path

from provide.foundation.crypto.algorithms import DEFAULT_ALGORITHM
from provide.foundation.crypto.hashing import hash_data, hash_file
from provide.foundation.crypto.utils import compare_hash
from provide.foundation.errors.resources import ResourceError
from provide.foundation.logger import get_logger

"""Checksum verification and management."""

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


def x_verify_file__mutmut_orig(
    path: Path | str,
    expected_hash: str,
    algorithm: str = DEFAULT_ALGORITHM,
) -> bool:
    """Verify a file matches an expected hash.

    Args:
        path: File path
        expected_hash: Expected hash value
        algorithm: Hash algorithm

    Returns:
        True if hash matches, False otherwise

    Raises:
        ResourceError: If file cannot be read
        ValidationError: If algorithm is not supported

    """
    if isinstance(path, str):
        path = Path(path)

    try:
        actual_hash = hash_file(path, algorithm)
        matches = compare_hash(actual_hash, expected_hash)

        if matches:
            log.debug(
                "✅ Checksum verified",
                path=str(path),
                algorithm=algorithm,
            )
        else:
            log.warning(
                "❌ Checksum mismatch",
                path=str(path),
                algorithm=algorithm,
                expected=expected_hash[:16] + "...",
                actual=actual_hash[:16] + "...",
            )

        return matches

    except ResourceError:
        log.error(
            "❌ Failed to verify checksum - file not found",
            path=str(path),
        )
        return False


def x_verify_file__mutmut_1(
    path: Path | str,
    expected_hash: str,
    algorithm: str = DEFAULT_ALGORITHM,
) -> bool:
    """Verify a file matches an expected hash.

    Args:
        path: File path
        expected_hash: Expected hash value
        algorithm: Hash algorithm

    Returns:
        True if hash matches, False otherwise

    Raises:
        ResourceError: If file cannot be read
        ValidationError: If algorithm is not supported

    """
    if isinstance(path, str):
        path = None

    try:
        actual_hash = hash_file(path, algorithm)
        matches = compare_hash(actual_hash, expected_hash)

        if matches:
            log.debug(
                "✅ Checksum verified",
                path=str(path),
                algorithm=algorithm,
            )
        else:
            log.warning(
                "❌ Checksum mismatch",
                path=str(path),
                algorithm=algorithm,
                expected=expected_hash[:16] + "...",
                actual=actual_hash[:16] + "...",
            )

        return matches

    except ResourceError:
        log.error(
            "❌ Failed to verify checksum - file not found",
            path=str(path),
        )
        return False


def x_verify_file__mutmut_2(
    path: Path | str,
    expected_hash: str,
    algorithm: str = DEFAULT_ALGORITHM,
) -> bool:
    """Verify a file matches an expected hash.

    Args:
        path: File path
        expected_hash: Expected hash value
        algorithm: Hash algorithm

    Returns:
        True if hash matches, False otherwise

    Raises:
        ResourceError: If file cannot be read
        ValidationError: If algorithm is not supported

    """
    if isinstance(path, str):
        path = Path(None)

    try:
        actual_hash = hash_file(path, algorithm)
        matches = compare_hash(actual_hash, expected_hash)

        if matches:
            log.debug(
                "✅ Checksum verified",
                path=str(path),
                algorithm=algorithm,
            )
        else:
            log.warning(
                "❌ Checksum mismatch",
                path=str(path),
                algorithm=algorithm,
                expected=expected_hash[:16] + "...",
                actual=actual_hash[:16] + "...",
            )

        return matches

    except ResourceError:
        log.error(
            "❌ Failed to verify checksum - file not found",
            path=str(path),
        )
        return False


def x_verify_file__mutmut_3(
    path: Path | str,
    expected_hash: str,
    algorithm: str = DEFAULT_ALGORITHM,
) -> bool:
    """Verify a file matches an expected hash.

    Args:
        path: File path
        expected_hash: Expected hash value
        algorithm: Hash algorithm

    Returns:
        True if hash matches, False otherwise

    Raises:
        ResourceError: If file cannot be read
        ValidationError: If algorithm is not supported

    """
    if isinstance(path, str):
        path = Path(path)

    try:
        actual_hash = None
        matches = compare_hash(actual_hash, expected_hash)

        if matches:
            log.debug(
                "✅ Checksum verified",
                path=str(path),
                algorithm=algorithm,
            )
        else:
            log.warning(
                "❌ Checksum mismatch",
                path=str(path),
                algorithm=algorithm,
                expected=expected_hash[:16] + "...",
                actual=actual_hash[:16] + "...",
            )

        return matches

    except ResourceError:
        log.error(
            "❌ Failed to verify checksum - file not found",
            path=str(path),
        )
        return False


def x_verify_file__mutmut_4(
    path: Path | str,
    expected_hash: str,
    algorithm: str = DEFAULT_ALGORITHM,
) -> bool:
    """Verify a file matches an expected hash.

    Args:
        path: File path
        expected_hash: Expected hash value
        algorithm: Hash algorithm

    Returns:
        True if hash matches, False otherwise

    Raises:
        ResourceError: If file cannot be read
        ValidationError: If algorithm is not supported

    """
    if isinstance(path, str):
        path = Path(path)

    try:
        actual_hash = hash_file(None, algorithm)
        matches = compare_hash(actual_hash, expected_hash)

        if matches:
            log.debug(
                "✅ Checksum verified",
                path=str(path),
                algorithm=algorithm,
            )
        else:
            log.warning(
                "❌ Checksum mismatch",
                path=str(path),
                algorithm=algorithm,
                expected=expected_hash[:16] + "...",
                actual=actual_hash[:16] + "...",
            )

        return matches

    except ResourceError:
        log.error(
            "❌ Failed to verify checksum - file not found",
            path=str(path),
        )
        return False


def x_verify_file__mutmut_5(
    path: Path | str,
    expected_hash: str,
    algorithm: str = DEFAULT_ALGORITHM,
) -> bool:
    """Verify a file matches an expected hash.

    Args:
        path: File path
        expected_hash: Expected hash value
        algorithm: Hash algorithm

    Returns:
        True if hash matches, False otherwise

    Raises:
        ResourceError: If file cannot be read
        ValidationError: If algorithm is not supported

    """
    if isinstance(path, str):
        path = Path(path)

    try:
        actual_hash = hash_file(path, None)
        matches = compare_hash(actual_hash, expected_hash)

        if matches:
            log.debug(
                "✅ Checksum verified",
                path=str(path),
                algorithm=algorithm,
            )
        else:
            log.warning(
                "❌ Checksum mismatch",
                path=str(path),
                algorithm=algorithm,
                expected=expected_hash[:16] + "...",
                actual=actual_hash[:16] + "...",
            )

        return matches

    except ResourceError:
        log.error(
            "❌ Failed to verify checksum - file not found",
            path=str(path),
        )
        return False


def x_verify_file__mutmut_6(
    path: Path | str,
    expected_hash: str,
    algorithm: str = DEFAULT_ALGORITHM,
) -> bool:
    """Verify a file matches an expected hash.

    Args:
        path: File path
        expected_hash: Expected hash value
        algorithm: Hash algorithm

    Returns:
        True if hash matches, False otherwise

    Raises:
        ResourceError: If file cannot be read
        ValidationError: If algorithm is not supported

    """
    if isinstance(path, str):
        path = Path(path)

    try:
        actual_hash = hash_file(algorithm)
        matches = compare_hash(actual_hash, expected_hash)

        if matches:
            log.debug(
                "✅ Checksum verified",
                path=str(path),
                algorithm=algorithm,
            )
        else:
            log.warning(
                "❌ Checksum mismatch",
                path=str(path),
                algorithm=algorithm,
                expected=expected_hash[:16] + "...",
                actual=actual_hash[:16] + "...",
            )

        return matches

    except ResourceError:
        log.error(
            "❌ Failed to verify checksum - file not found",
            path=str(path),
        )
        return False


def x_verify_file__mutmut_7(
    path: Path | str,
    expected_hash: str,
    algorithm: str = DEFAULT_ALGORITHM,
) -> bool:
    """Verify a file matches an expected hash.

    Args:
        path: File path
        expected_hash: Expected hash value
        algorithm: Hash algorithm

    Returns:
        True if hash matches, False otherwise

    Raises:
        ResourceError: If file cannot be read
        ValidationError: If algorithm is not supported

    """
    if isinstance(path, str):
        path = Path(path)

    try:
        actual_hash = hash_file(
            path,
        )
        matches = compare_hash(actual_hash, expected_hash)

        if matches:
            log.debug(
                "✅ Checksum verified",
                path=str(path),
                algorithm=algorithm,
            )
        else:
            log.warning(
                "❌ Checksum mismatch",
                path=str(path),
                algorithm=algorithm,
                expected=expected_hash[:16] + "...",
                actual=actual_hash[:16] + "...",
            )

        return matches

    except ResourceError:
        log.error(
            "❌ Failed to verify checksum - file not found",
            path=str(path),
        )
        return False


def x_verify_file__mutmut_8(
    path: Path | str,
    expected_hash: str,
    algorithm: str = DEFAULT_ALGORITHM,
) -> bool:
    """Verify a file matches an expected hash.

    Args:
        path: File path
        expected_hash: Expected hash value
        algorithm: Hash algorithm

    Returns:
        True if hash matches, False otherwise

    Raises:
        ResourceError: If file cannot be read
        ValidationError: If algorithm is not supported

    """
    if isinstance(path, str):
        path = Path(path)

    try:
        actual_hash = hash_file(path, algorithm)
        matches = None

        if matches:
            log.debug(
                "✅ Checksum verified",
                path=str(path),
                algorithm=algorithm,
            )
        else:
            log.warning(
                "❌ Checksum mismatch",
                path=str(path),
                algorithm=algorithm,
                expected=expected_hash[:16] + "...",
                actual=actual_hash[:16] + "...",
            )

        return matches

    except ResourceError:
        log.error(
            "❌ Failed to verify checksum - file not found",
            path=str(path),
        )
        return False


def x_verify_file__mutmut_9(
    path: Path | str,
    expected_hash: str,
    algorithm: str = DEFAULT_ALGORITHM,
) -> bool:
    """Verify a file matches an expected hash.

    Args:
        path: File path
        expected_hash: Expected hash value
        algorithm: Hash algorithm

    Returns:
        True if hash matches, False otherwise

    Raises:
        ResourceError: If file cannot be read
        ValidationError: If algorithm is not supported

    """
    if isinstance(path, str):
        path = Path(path)

    try:
        actual_hash = hash_file(path, algorithm)
        matches = compare_hash(None, expected_hash)

        if matches:
            log.debug(
                "✅ Checksum verified",
                path=str(path),
                algorithm=algorithm,
            )
        else:
            log.warning(
                "❌ Checksum mismatch",
                path=str(path),
                algorithm=algorithm,
                expected=expected_hash[:16] + "...",
                actual=actual_hash[:16] + "...",
            )

        return matches

    except ResourceError:
        log.error(
            "❌ Failed to verify checksum - file not found",
            path=str(path),
        )
        return False


def x_verify_file__mutmut_10(
    path: Path | str,
    expected_hash: str,
    algorithm: str = DEFAULT_ALGORITHM,
) -> bool:
    """Verify a file matches an expected hash.

    Args:
        path: File path
        expected_hash: Expected hash value
        algorithm: Hash algorithm

    Returns:
        True if hash matches, False otherwise

    Raises:
        ResourceError: If file cannot be read
        ValidationError: If algorithm is not supported

    """
    if isinstance(path, str):
        path = Path(path)

    try:
        actual_hash = hash_file(path, algorithm)
        matches = compare_hash(actual_hash, None)

        if matches:
            log.debug(
                "✅ Checksum verified",
                path=str(path),
                algorithm=algorithm,
            )
        else:
            log.warning(
                "❌ Checksum mismatch",
                path=str(path),
                algorithm=algorithm,
                expected=expected_hash[:16] + "...",
                actual=actual_hash[:16] + "...",
            )

        return matches

    except ResourceError:
        log.error(
            "❌ Failed to verify checksum - file not found",
            path=str(path),
        )
        return False


def x_verify_file__mutmut_11(
    path: Path | str,
    expected_hash: str,
    algorithm: str = DEFAULT_ALGORITHM,
) -> bool:
    """Verify a file matches an expected hash.

    Args:
        path: File path
        expected_hash: Expected hash value
        algorithm: Hash algorithm

    Returns:
        True if hash matches, False otherwise

    Raises:
        ResourceError: If file cannot be read
        ValidationError: If algorithm is not supported

    """
    if isinstance(path, str):
        path = Path(path)

    try:
        actual_hash = hash_file(path, algorithm)
        matches = compare_hash(expected_hash)

        if matches:
            log.debug(
                "✅ Checksum verified",
                path=str(path),
                algorithm=algorithm,
            )
        else:
            log.warning(
                "❌ Checksum mismatch",
                path=str(path),
                algorithm=algorithm,
                expected=expected_hash[:16] + "...",
                actual=actual_hash[:16] + "...",
            )

        return matches

    except ResourceError:
        log.error(
            "❌ Failed to verify checksum - file not found",
            path=str(path),
        )
        return False


def x_verify_file__mutmut_12(
    path: Path | str,
    expected_hash: str,
    algorithm: str = DEFAULT_ALGORITHM,
) -> bool:
    """Verify a file matches an expected hash.

    Args:
        path: File path
        expected_hash: Expected hash value
        algorithm: Hash algorithm

    Returns:
        True if hash matches, False otherwise

    Raises:
        ResourceError: If file cannot be read
        ValidationError: If algorithm is not supported

    """
    if isinstance(path, str):
        path = Path(path)

    try:
        actual_hash = hash_file(path, algorithm)
        matches = compare_hash(
            actual_hash,
        )

        if matches:
            log.debug(
                "✅ Checksum verified",
                path=str(path),
                algorithm=algorithm,
            )
        else:
            log.warning(
                "❌ Checksum mismatch",
                path=str(path),
                algorithm=algorithm,
                expected=expected_hash[:16] + "...",
                actual=actual_hash[:16] + "...",
            )

        return matches

    except ResourceError:
        log.error(
            "❌ Failed to verify checksum - file not found",
            path=str(path),
        )
        return False


def x_verify_file__mutmut_13(
    path: Path | str,
    expected_hash: str,
    algorithm: str = DEFAULT_ALGORITHM,
) -> bool:
    """Verify a file matches an expected hash.

    Args:
        path: File path
        expected_hash: Expected hash value
        algorithm: Hash algorithm

    Returns:
        True if hash matches, False otherwise

    Raises:
        ResourceError: If file cannot be read
        ValidationError: If algorithm is not supported

    """
    if isinstance(path, str):
        path = Path(path)

    try:
        actual_hash = hash_file(path, algorithm)
        matches = compare_hash(actual_hash, expected_hash)

        if matches:
            log.debug(
                None,
                path=str(path),
                algorithm=algorithm,
            )
        else:
            log.warning(
                "❌ Checksum mismatch",
                path=str(path),
                algorithm=algorithm,
                expected=expected_hash[:16] + "...",
                actual=actual_hash[:16] + "...",
            )

        return matches

    except ResourceError:
        log.error(
            "❌ Failed to verify checksum - file not found",
            path=str(path),
        )
        return False


def x_verify_file__mutmut_14(
    path: Path | str,
    expected_hash: str,
    algorithm: str = DEFAULT_ALGORITHM,
) -> bool:
    """Verify a file matches an expected hash.

    Args:
        path: File path
        expected_hash: Expected hash value
        algorithm: Hash algorithm

    Returns:
        True if hash matches, False otherwise

    Raises:
        ResourceError: If file cannot be read
        ValidationError: If algorithm is not supported

    """
    if isinstance(path, str):
        path = Path(path)

    try:
        actual_hash = hash_file(path, algorithm)
        matches = compare_hash(actual_hash, expected_hash)

        if matches:
            log.debug(
                "✅ Checksum verified",
                path=None,
                algorithm=algorithm,
            )
        else:
            log.warning(
                "❌ Checksum mismatch",
                path=str(path),
                algorithm=algorithm,
                expected=expected_hash[:16] + "...",
                actual=actual_hash[:16] + "...",
            )

        return matches

    except ResourceError:
        log.error(
            "❌ Failed to verify checksum - file not found",
            path=str(path),
        )
        return False


def x_verify_file__mutmut_15(
    path: Path | str,
    expected_hash: str,
    algorithm: str = DEFAULT_ALGORITHM,
) -> bool:
    """Verify a file matches an expected hash.

    Args:
        path: File path
        expected_hash: Expected hash value
        algorithm: Hash algorithm

    Returns:
        True if hash matches, False otherwise

    Raises:
        ResourceError: If file cannot be read
        ValidationError: If algorithm is not supported

    """
    if isinstance(path, str):
        path = Path(path)

    try:
        actual_hash = hash_file(path, algorithm)
        matches = compare_hash(actual_hash, expected_hash)

        if matches:
            log.debug(
                "✅ Checksum verified",
                path=str(path),
                algorithm=None,
            )
        else:
            log.warning(
                "❌ Checksum mismatch",
                path=str(path),
                algorithm=algorithm,
                expected=expected_hash[:16] + "...",
                actual=actual_hash[:16] + "...",
            )

        return matches

    except ResourceError:
        log.error(
            "❌ Failed to verify checksum - file not found",
            path=str(path),
        )
        return False


def x_verify_file__mutmut_16(
    path: Path | str,
    expected_hash: str,
    algorithm: str = DEFAULT_ALGORITHM,
) -> bool:
    """Verify a file matches an expected hash.

    Args:
        path: File path
        expected_hash: Expected hash value
        algorithm: Hash algorithm

    Returns:
        True if hash matches, False otherwise

    Raises:
        ResourceError: If file cannot be read
        ValidationError: If algorithm is not supported

    """
    if isinstance(path, str):
        path = Path(path)

    try:
        actual_hash = hash_file(path, algorithm)
        matches = compare_hash(actual_hash, expected_hash)

        if matches:
            log.debug(
                path=str(path),
                algorithm=algorithm,
            )
        else:
            log.warning(
                "❌ Checksum mismatch",
                path=str(path),
                algorithm=algorithm,
                expected=expected_hash[:16] + "...",
                actual=actual_hash[:16] + "...",
            )

        return matches

    except ResourceError:
        log.error(
            "❌ Failed to verify checksum - file not found",
            path=str(path),
        )
        return False


def x_verify_file__mutmut_17(
    path: Path | str,
    expected_hash: str,
    algorithm: str = DEFAULT_ALGORITHM,
) -> bool:
    """Verify a file matches an expected hash.

    Args:
        path: File path
        expected_hash: Expected hash value
        algorithm: Hash algorithm

    Returns:
        True if hash matches, False otherwise

    Raises:
        ResourceError: If file cannot be read
        ValidationError: If algorithm is not supported

    """
    if isinstance(path, str):
        path = Path(path)

    try:
        actual_hash = hash_file(path, algorithm)
        matches = compare_hash(actual_hash, expected_hash)

        if matches:
            log.debug(
                "✅ Checksum verified",
                algorithm=algorithm,
            )
        else:
            log.warning(
                "❌ Checksum mismatch",
                path=str(path),
                algorithm=algorithm,
                expected=expected_hash[:16] + "...",
                actual=actual_hash[:16] + "...",
            )

        return matches

    except ResourceError:
        log.error(
            "❌ Failed to verify checksum - file not found",
            path=str(path),
        )
        return False


def x_verify_file__mutmut_18(
    path: Path | str,
    expected_hash: str,
    algorithm: str = DEFAULT_ALGORITHM,
) -> bool:
    """Verify a file matches an expected hash.

    Args:
        path: File path
        expected_hash: Expected hash value
        algorithm: Hash algorithm

    Returns:
        True if hash matches, False otherwise

    Raises:
        ResourceError: If file cannot be read
        ValidationError: If algorithm is not supported

    """
    if isinstance(path, str):
        path = Path(path)

    try:
        actual_hash = hash_file(path, algorithm)
        matches = compare_hash(actual_hash, expected_hash)

        if matches:
            log.debug(
                "✅ Checksum verified",
                path=str(path),
            )
        else:
            log.warning(
                "❌ Checksum mismatch",
                path=str(path),
                algorithm=algorithm,
                expected=expected_hash[:16] + "...",
                actual=actual_hash[:16] + "...",
            )

        return matches

    except ResourceError:
        log.error(
            "❌ Failed to verify checksum - file not found",
            path=str(path),
        )
        return False


def x_verify_file__mutmut_19(
    path: Path | str,
    expected_hash: str,
    algorithm: str = DEFAULT_ALGORITHM,
) -> bool:
    """Verify a file matches an expected hash.

    Args:
        path: File path
        expected_hash: Expected hash value
        algorithm: Hash algorithm

    Returns:
        True if hash matches, False otherwise

    Raises:
        ResourceError: If file cannot be read
        ValidationError: If algorithm is not supported

    """
    if isinstance(path, str):
        path = Path(path)

    try:
        actual_hash = hash_file(path, algorithm)
        matches = compare_hash(actual_hash, expected_hash)

        if matches:
            log.debug(
                "XX✅ Checksum verifiedXX",
                path=str(path),
                algorithm=algorithm,
            )
        else:
            log.warning(
                "❌ Checksum mismatch",
                path=str(path),
                algorithm=algorithm,
                expected=expected_hash[:16] + "...",
                actual=actual_hash[:16] + "...",
            )

        return matches

    except ResourceError:
        log.error(
            "❌ Failed to verify checksum - file not found",
            path=str(path),
        )
        return False


def x_verify_file__mutmut_20(
    path: Path | str,
    expected_hash: str,
    algorithm: str = DEFAULT_ALGORITHM,
) -> bool:
    """Verify a file matches an expected hash.

    Args:
        path: File path
        expected_hash: Expected hash value
        algorithm: Hash algorithm

    Returns:
        True if hash matches, False otherwise

    Raises:
        ResourceError: If file cannot be read
        ValidationError: If algorithm is not supported

    """
    if isinstance(path, str):
        path = Path(path)

    try:
        actual_hash = hash_file(path, algorithm)
        matches = compare_hash(actual_hash, expected_hash)

        if matches:
            log.debug(
                "✅ checksum verified",
                path=str(path),
                algorithm=algorithm,
            )
        else:
            log.warning(
                "❌ Checksum mismatch",
                path=str(path),
                algorithm=algorithm,
                expected=expected_hash[:16] + "...",
                actual=actual_hash[:16] + "...",
            )

        return matches

    except ResourceError:
        log.error(
            "❌ Failed to verify checksum - file not found",
            path=str(path),
        )
        return False


def x_verify_file__mutmut_21(
    path: Path | str,
    expected_hash: str,
    algorithm: str = DEFAULT_ALGORITHM,
) -> bool:
    """Verify a file matches an expected hash.

    Args:
        path: File path
        expected_hash: Expected hash value
        algorithm: Hash algorithm

    Returns:
        True if hash matches, False otherwise

    Raises:
        ResourceError: If file cannot be read
        ValidationError: If algorithm is not supported

    """
    if isinstance(path, str):
        path = Path(path)

    try:
        actual_hash = hash_file(path, algorithm)
        matches = compare_hash(actual_hash, expected_hash)

        if matches:
            log.debug(
                "✅ CHECKSUM VERIFIED",
                path=str(path),
                algorithm=algorithm,
            )
        else:
            log.warning(
                "❌ Checksum mismatch",
                path=str(path),
                algorithm=algorithm,
                expected=expected_hash[:16] + "...",
                actual=actual_hash[:16] + "...",
            )

        return matches

    except ResourceError:
        log.error(
            "❌ Failed to verify checksum - file not found",
            path=str(path),
        )
        return False


def x_verify_file__mutmut_22(
    path: Path | str,
    expected_hash: str,
    algorithm: str = DEFAULT_ALGORITHM,
) -> bool:
    """Verify a file matches an expected hash.

    Args:
        path: File path
        expected_hash: Expected hash value
        algorithm: Hash algorithm

    Returns:
        True if hash matches, False otherwise

    Raises:
        ResourceError: If file cannot be read
        ValidationError: If algorithm is not supported

    """
    if isinstance(path, str):
        path = Path(path)

    try:
        actual_hash = hash_file(path, algorithm)
        matches = compare_hash(actual_hash, expected_hash)

        if matches:
            log.debug(
                "✅ Checksum verified",
                path=str(None),
                algorithm=algorithm,
            )
        else:
            log.warning(
                "❌ Checksum mismatch",
                path=str(path),
                algorithm=algorithm,
                expected=expected_hash[:16] + "...",
                actual=actual_hash[:16] + "...",
            )

        return matches

    except ResourceError:
        log.error(
            "❌ Failed to verify checksum - file not found",
            path=str(path),
        )
        return False


def x_verify_file__mutmut_23(
    path: Path | str,
    expected_hash: str,
    algorithm: str = DEFAULT_ALGORITHM,
) -> bool:
    """Verify a file matches an expected hash.

    Args:
        path: File path
        expected_hash: Expected hash value
        algorithm: Hash algorithm

    Returns:
        True if hash matches, False otherwise

    Raises:
        ResourceError: If file cannot be read
        ValidationError: If algorithm is not supported

    """
    if isinstance(path, str):
        path = Path(path)

    try:
        actual_hash = hash_file(path, algorithm)
        matches = compare_hash(actual_hash, expected_hash)

        if matches:
            log.debug(
                "✅ Checksum verified",
                path=str(path),
                algorithm=algorithm,
            )
        else:
            log.warning(
                None,
                path=str(path),
                algorithm=algorithm,
                expected=expected_hash[:16] + "...",
                actual=actual_hash[:16] + "...",
            )

        return matches

    except ResourceError:
        log.error(
            "❌ Failed to verify checksum - file not found",
            path=str(path),
        )
        return False


def x_verify_file__mutmut_24(
    path: Path | str,
    expected_hash: str,
    algorithm: str = DEFAULT_ALGORITHM,
) -> bool:
    """Verify a file matches an expected hash.

    Args:
        path: File path
        expected_hash: Expected hash value
        algorithm: Hash algorithm

    Returns:
        True if hash matches, False otherwise

    Raises:
        ResourceError: If file cannot be read
        ValidationError: If algorithm is not supported

    """
    if isinstance(path, str):
        path = Path(path)

    try:
        actual_hash = hash_file(path, algorithm)
        matches = compare_hash(actual_hash, expected_hash)

        if matches:
            log.debug(
                "✅ Checksum verified",
                path=str(path),
                algorithm=algorithm,
            )
        else:
            log.warning(
                "❌ Checksum mismatch",
                path=None,
                algorithm=algorithm,
                expected=expected_hash[:16] + "...",
                actual=actual_hash[:16] + "...",
            )

        return matches

    except ResourceError:
        log.error(
            "❌ Failed to verify checksum - file not found",
            path=str(path),
        )
        return False


def x_verify_file__mutmut_25(
    path: Path | str,
    expected_hash: str,
    algorithm: str = DEFAULT_ALGORITHM,
) -> bool:
    """Verify a file matches an expected hash.

    Args:
        path: File path
        expected_hash: Expected hash value
        algorithm: Hash algorithm

    Returns:
        True if hash matches, False otherwise

    Raises:
        ResourceError: If file cannot be read
        ValidationError: If algorithm is not supported

    """
    if isinstance(path, str):
        path = Path(path)

    try:
        actual_hash = hash_file(path, algorithm)
        matches = compare_hash(actual_hash, expected_hash)

        if matches:
            log.debug(
                "✅ Checksum verified",
                path=str(path),
                algorithm=algorithm,
            )
        else:
            log.warning(
                "❌ Checksum mismatch",
                path=str(path),
                algorithm=None,
                expected=expected_hash[:16] + "...",
                actual=actual_hash[:16] + "...",
            )

        return matches

    except ResourceError:
        log.error(
            "❌ Failed to verify checksum - file not found",
            path=str(path),
        )
        return False


def x_verify_file__mutmut_26(
    path: Path | str,
    expected_hash: str,
    algorithm: str = DEFAULT_ALGORITHM,
) -> bool:
    """Verify a file matches an expected hash.

    Args:
        path: File path
        expected_hash: Expected hash value
        algorithm: Hash algorithm

    Returns:
        True if hash matches, False otherwise

    Raises:
        ResourceError: If file cannot be read
        ValidationError: If algorithm is not supported

    """
    if isinstance(path, str):
        path = Path(path)

    try:
        actual_hash = hash_file(path, algorithm)
        matches = compare_hash(actual_hash, expected_hash)

        if matches:
            log.debug(
                "✅ Checksum verified",
                path=str(path),
                algorithm=algorithm,
            )
        else:
            log.warning(
                "❌ Checksum mismatch",
                path=str(path),
                algorithm=algorithm,
                expected=None,
                actual=actual_hash[:16] + "...",
            )

        return matches

    except ResourceError:
        log.error(
            "❌ Failed to verify checksum - file not found",
            path=str(path),
        )
        return False


def x_verify_file__mutmut_27(
    path: Path | str,
    expected_hash: str,
    algorithm: str = DEFAULT_ALGORITHM,
) -> bool:
    """Verify a file matches an expected hash.

    Args:
        path: File path
        expected_hash: Expected hash value
        algorithm: Hash algorithm

    Returns:
        True if hash matches, False otherwise

    Raises:
        ResourceError: If file cannot be read
        ValidationError: If algorithm is not supported

    """
    if isinstance(path, str):
        path = Path(path)

    try:
        actual_hash = hash_file(path, algorithm)
        matches = compare_hash(actual_hash, expected_hash)

        if matches:
            log.debug(
                "✅ Checksum verified",
                path=str(path),
                algorithm=algorithm,
            )
        else:
            log.warning(
                "❌ Checksum mismatch",
                path=str(path),
                algorithm=algorithm,
                expected=expected_hash[:16] + "...",
                actual=None,
            )

        return matches

    except ResourceError:
        log.error(
            "❌ Failed to verify checksum - file not found",
            path=str(path),
        )
        return False


def x_verify_file__mutmut_28(
    path: Path | str,
    expected_hash: str,
    algorithm: str = DEFAULT_ALGORITHM,
) -> bool:
    """Verify a file matches an expected hash.

    Args:
        path: File path
        expected_hash: Expected hash value
        algorithm: Hash algorithm

    Returns:
        True if hash matches, False otherwise

    Raises:
        ResourceError: If file cannot be read
        ValidationError: If algorithm is not supported

    """
    if isinstance(path, str):
        path = Path(path)

    try:
        actual_hash = hash_file(path, algorithm)
        matches = compare_hash(actual_hash, expected_hash)

        if matches:
            log.debug(
                "✅ Checksum verified",
                path=str(path),
                algorithm=algorithm,
            )
        else:
            log.warning(
                path=str(path),
                algorithm=algorithm,
                expected=expected_hash[:16] + "...",
                actual=actual_hash[:16] + "...",
            )

        return matches

    except ResourceError:
        log.error(
            "❌ Failed to verify checksum - file not found",
            path=str(path),
        )
        return False


def x_verify_file__mutmut_29(
    path: Path | str,
    expected_hash: str,
    algorithm: str = DEFAULT_ALGORITHM,
) -> bool:
    """Verify a file matches an expected hash.

    Args:
        path: File path
        expected_hash: Expected hash value
        algorithm: Hash algorithm

    Returns:
        True if hash matches, False otherwise

    Raises:
        ResourceError: If file cannot be read
        ValidationError: If algorithm is not supported

    """
    if isinstance(path, str):
        path = Path(path)

    try:
        actual_hash = hash_file(path, algorithm)
        matches = compare_hash(actual_hash, expected_hash)

        if matches:
            log.debug(
                "✅ Checksum verified",
                path=str(path),
                algorithm=algorithm,
            )
        else:
            log.warning(
                "❌ Checksum mismatch",
                algorithm=algorithm,
                expected=expected_hash[:16] + "...",
                actual=actual_hash[:16] + "...",
            )

        return matches

    except ResourceError:
        log.error(
            "❌ Failed to verify checksum - file not found",
            path=str(path),
        )
        return False


def x_verify_file__mutmut_30(
    path: Path | str,
    expected_hash: str,
    algorithm: str = DEFAULT_ALGORITHM,
) -> bool:
    """Verify a file matches an expected hash.

    Args:
        path: File path
        expected_hash: Expected hash value
        algorithm: Hash algorithm

    Returns:
        True if hash matches, False otherwise

    Raises:
        ResourceError: If file cannot be read
        ValidationError: If algorithm is not supported

    """
    if isinstance(path, str):
        path = Path(path)

    try:
        actual_hash = hash_file(path, algorithm)
        matches = compare_hash(actual_hash, expected_hash)

        if matches:
            log.debug(
                "✅ Checksum verified",
                path=str(path),
                algorithm=algorithm,
            )
        else:
            log.warning(
                "❌ Checksum mismatch",
                path=str(path),
                expected=expected_hash[:16] + "...",
                actual=actual_hash[:16] + "...",
            )

        return matches

    except ResourceError:
        log.error(
            "❌ Failed to verify checksum - file not found",
            path=str(path),
        )
        return False


def x_verify_file__mutmut_31(
    path: Path | str,
    expected_hash: str,
    algorithm: str = DEFAULT_ALGORITHM,
) -> bool:
    """Verify a file matches an expected hash.

    Args:
        path: File path
        expected_hash: Expected hash value
        algorithm: Hash algorithm

    Returns:
        True if hash matches, False otherwise

    Raises:
        ResourceError: If file cannot be read
        ValidationError: If algorithm is not supported

    """
    if isinstance(path, str):
        path = Path(path)

    try:
        actual_hash = hash_file(path, algorithm)
        matches = compare_hash(actual_hash, expected_hash)

        if matches:
            log.debug(
                "✅ Checksum verified",
                path=str(path),
                algorithm=algorithm,
            )
        else:
            log.warning(
                "❌ Checksum mismatch",
                path=str(path),
                algorithm=algorithm,
                actual=actual_hash[:16] + "...",
            )

        return matches

    except ResourceError:
        log.error(
            "❌ Failed to verify checksum - file not found",
            path=str(path),
        )
        return False


def x_verify_file__mutmut_32(
    path: Path | str,
    expected_hash: str,
    algorithm: str = DEFAULT_ALGORITHM,
) -> bool:
    """Verify a file matches an expected hash.

    Args:
        path: File path
        expected_hash: Expected hash value
        algorithm: Hash algorithm

    Returns:
        True if hash matches, False otherwise

    Raises:
        ResourceError: If file cannot be read
        ValidationError: If algorithm is not supported

    """
    if isinstance(path, str):
        path = Path(path)

    try:
        actual_hash = hash_file(path, algorithm)
        matches = compare_hash(actual_hash, expected_hash)

        if matches:
            log.debug(
                "✅ Checksum verified",
                path=str(path),
                algorithm=algorithm,
            )
        else:
            log.warning(
                "❌ Checksum mismatch",
                path=str(path),
                algorithm=algorithm,
                expected=expected_hash[:16] + "...",
            )

        return matches

    except ResourceError:
        log.error(
            "❌ Failed to verify checksum - file not found",
            path=str(path),
        )
        return False


def x_verify_file__mutmut_33(
    path: Path | str,
    expected_hash: str,
    algorithm: str = DEFAULT_ALGORITHM,
) -> bool:
    """Verify a file matches an expected hash.

    Args:
        path: File path
        expected_hash: Expected hash value
        algorithm: Hash algorithm

    Returns:
        True if hash matches, False otherwise

    Raises:
        ResourceError: If file cannot be read
        ValidationError: If algorithm is not supported

    """
    if isinstance(path, str):
        path = Path(path)

    try:
        actual_hash = hash_file(path, algorithm)
        matches = compare_hash(actual_hash, expected_hash)

        if matches:
            log.debug(
                "✅ Checksum verified",
                path=str(path),
                algorithm=algorithm,
            )
        else:
            log.warning(
                "XX❌ Checksum mismatchXX",
                path=str(path),
                algorithm=algorithm,
                expected=expected_hash[:16] + "...",
                actual=actual_hash[:16] + "...",
            )

        return matches

    except ResourceError:
        log.error(
            "❌ Failed to verify checksum - file not found",
            path=str(path),
        )
        return False


def x_verify_file__mutmut_34(
    path: Path | str,
    expected_hash: str,
    algorithm: str = DEFAULT_ALGORITHM,
) -> bool:
    """Verify a file matches an expected hash.

    Args:
        path: File path
        expected_hash: Expected hash value
        algorithm: Hash algorithm

    Returns:
        True if hash matches, False otherwise

    Raises:
        ResourceError: If file cannot be read
        ValidationError: If algorithm is not supported

    """
    if isinstance(path, str):
        path = Path(path)

    try:
        actual_hash = hash_file(path, algorithm)
        matches = compare_hash(actual_hash, expected_hash)

        if matches:
            log.debug(
                "✅ Checksum verified",
                path=str(path),
                algorithm=algorithm,
            )
        else:
            log.warning(
                "❌ checksum mismatch",
                path=str(path),
                algorithm=algorithm,
                expected=expected_hash[:16] + "...",
                actual=actual_hash[:16] + "...",
            )

        return matches

    except ResourceError:
        log.error(
            "❌ Failed to verify checksum - file not found",
            path=str(path),
        )
        return False


def x_verify_file__mutmut_35(
    path: Path | str,
    expected_hash: str,
    algorithm: str = DEFAULT_ALGORITHM,
) -> bool:
    """Verify a file matches an expected hash.

    Args:
        path: File path
        expected_hash: Expected hash value
        algorithm: Hash algorithm

    Returns:
        True if hash matches, False otherwise

    Raises:
        ResourceError: If file cannot be read
        ValidationError: If algorithm is not supported

    """
    if isinstance(path, str):
        path = Path(path)

    try:
        actual_hash = hash_file(path, algorithm)
        matches = compare_hash(actual_hash, expected_hash)

        if matches:
            log.debug(
                "✅ Checksum verified",
                path=str(path),
                algorithm=algorithm,
            )
        else:
            log.warning(
                "❌ CHECKSUM MISMATCH",
                path=str(path),
                algorithm=algorithm,
                expected=expected_hash[:16] + "...",
                actual=actual_hash[:16] + "...",
            )

        return matches

    except ResourceError:
        log.error(
            "❌ Failed to verify checksum - file not found",
            path=str(path),
        )
        return False


def x_verify_file__mutmut_36(
    path: Path | str,
    expected_hash: str,
    algorithm: str = DEFAULT_ALGORITHM,
) -> bool:
    """Verify a file matches an expected hash.

    Args:
        path: File path
        expected_hash: Expected hash value
        algorithm: Hash algorithm

    Returns:
        True if hash matches, False otherwise

    Raises:
        ResourceError: If file cannot be read
        ValidationError: If algorithm is not supported

    """
    if isinstance(path, str):
        path = Path(path)

    try:
        actual_hash = hash_file(path, algorithm)
        matches = compare_hash(actual_hash, expected_hash)

        if matches:
            log.debug(
                "✅ Checksum verified",
                path=str(path),
                algorithm=algorithm,
            )
        else:
            log.warning(
                "❌ Checksum mismatch",
                path=str(None),
                algorithm=algorithm,
                expected=expected_hash[:16] + "...",
                actual=actual_hash[:16] + "...",
            )

        return matches

    except ResourceError:
        log.error(
            "❌ Failed to verify checksum - file not found",
            path=str(path),
        )
        return False


def x_verify_file__mutmut_37(
    path: Path | str,
    expected_hash: str,
    algorithm: str = DEFAULT_ALGORITHM,
) -> bool:
    """Verify a file matches an expected hash.

    Args:
        path: File path
        expected_hash: Expected hash value
        algorithm: Hash algorithm

    Returns:
        True if hash matches, False otherwise

    Raises:
        ResourceError: If file cannot be read
        ValidationError: If algorithm is not supported

    """
    if isinstance(path, str):
        path = Path(path)

    try:
        actual_hash = hash_file(path, algorithm)
        matches = compare_hash(actual_hash, expected_hash)

        if matches:
            log.debug(
                "✅ Checksum verified",
                path=str(path),
                algorithm=algorithm,
            )
        else:
            log.warning(
                "❌ Checksum mismatch",
                path=str(path),
                algorithm=algorithm,
                expected=expected_hash[:16] - "...",
                actual=actual_hash[:16] + "...",
            )

        return matches

    except ResourceError:
        log.error(
            "❌ Failed to verify checksum - file not found",
            path=str(path),
        )
        return False


def x_verify_file__mutmut_38(
    path: Path | str,
    expected_hash: str,
    algorithm: str = DEFAULT_ALGORITHM,
) -> bool:
    """Verify a file matches an expected hash.

    Args:
        path: File path
        expected_hash: Expected hash value
        algorithm: Hash algorithm

    Returns:
        True if hash matches, False otherwise

    Raises:
        ResourceError: If file cannot be read
        ValidationError: If algorithm is not supported

    """
    if isinstance(path, str):
        path = Path(path)

    try:
        actual_hash = hash_file(path, algorithm)
        matches = compare_hash(actual_hash, expected_hash)

        if matches:
            log.debug(
                "✅ Checksum verified",
                path=str(path),
                algorithm=algorithm,
            )
        else:
            log.warning(
                "❌ Checksum mismatch",
                path=str(path),
                algorithm=algorithm,
                expected=expected_hash[:17] + "...",
                actual=actual_hash[:16] + "...",
            )

        return matches

    except ResourceError:
        log.error(
            "❌ Failed to verify checksum - file not found",
            path=str(path),
        )
        return False


def x_verify_file__mutmut_39(
    path: Path | str,
    expected_hash: str,
    algorithm: str = DEFAULT_ALGORITHM,
) -> bool:
    """Verify a file matches an expected hash.

    Args:
        path: File path
        expected_hash: Expected hash value
        algorithm: Hash algorithm

    Returns:
        True if hash matches, False otherwise

    Raises:
        ResourceError: If file cannot be read
        ValidationError: If algorithm is not supported

    """
    if isinstance(path, str):
        path = Path(path)

    try:
        actual_hash = hash_file(path, algorithm)
        matches = compare_hash(actual_hash, expected_hash)

        if matches:
            log.debug(
                "✅ Checksum verified",
                path=str(path),
                algorithm=algorithm,
            )
        else:
            log.warning(
                "❌ Checksum mismatch",
                path=str(path),
                algorithm=algorithm,
                expected=expected_hash[:16] + "XX...XX",
                actual=actual_hash[:16] + "...",
            )

        return matches

    except ResourceError:
        log.error(
            "❌ Failed to verify checksum - file not found",
            path=str(path),
        )
        return False


def x_verify_file__mutmut_40(
    path: Path | str,
    expected_hash: str,
    algorithm: str = DEFAULT_ALGORITHM,
) -> bool:
    """Verify a file matches an expected hash.

    Args:
        path: File path
        expected_hash: Expected hash value
        algorithm: Hash algorithm

    Returns:
        True if hash matches, False otherwise

    Raises:
        ResourceError: If file cannot be read
        ValidationError: If algorithm is not supported

    """
    if isinstance(path, str):
        path = Path(path)

    try:
        actual_hash = hash_file(path, algorithm)
        matches = compare_hash(actual_hash, expected_hash)

        if matches:
            log.debug(
                "✅ Checksum verified",
                path=str(path),
                algorithm=algorithm,
            )
        else:
            log.warning(
                "❌ Checksum mismatch",
                path=str(path),
                algorithm=algorithm,
                expected=expected_hash[:16] + "...",
                actual=actual_hash[:16] - "...",
            )

        return matches

    except ResourceError:
        log.error(
            "❌ Failed to verify checksum - file not found",
            path=str(path),
        )
        return False


def x_verify_file__mutmut_41(
    path: Path | str,
    expected_hash: str,
    algorithm: str = DEFAULT_ALGORITHM,
) -> bool:
    """Verify a file matches an expected hash.

    Args:
        path: File path
        expected_hash: Expected hash value
        algorithm: Hash algorithm

    Returns:
        True if hash matches, False otherwise

    Raises:
        ResourceError: If file cannot be read
        ValidationError: If algorithm is not supported

    """
    if isinstance(path, str):
        path = Path(path)

    try:
        actual_hash = hash_file(path, algorithm)
        matches = compare_hash(actual_hash, expected_hash)

        if matches:
            log.debug(
                "✅ Checksum verified",
                path=str(path),
                algorithm=algorithm,
            )
        else:
            log.warning(
                "❌ Checksum mismatch",
                path=str(path),
                algorithm=algorithm,
                expected=expected_hash[:16] + "...",
                actual=actual_hash[:17] + "...",
            )

        return matches

    except ResourceError:
        log.error(
            "❌ Failed to verify checksum - file not found",
            path=str(path),
        )
        return False


def x_verify_file__mutmut_42(
    path: Path | str,
    expected_hash: str,
    algorithm: str = DEFAULT_ALGORITHM,
) -> bool:
    """Verify a file matches an expected hash.

    Args:
        path: File path
        expected_hash: Expected hash value
        algorithm: Hash algorithm

    Returns:
        True if hash matches, False otherwise

    Raises:
        ResourceError: If file cannot be read
        ValidationError: If algorithm is not supported

    """
    if isinstance(path, str):
        path = Path(path)

    try:
        actual_hash = hash_file(path, algorithm)
        matches = compare_hash(actual_hash, expected_hash)

        if matches:
            log.debug(
                "✅ Checksum verified",
                path=str(path),
                algorithm=algorithm,
            )
        else:
            log.warning(
                "❌ Checksum mismatch",
                path=str(path),
                algorithm=algorithm,
                expected=expected_hash[:16] + "...",
                actual=actual_hash[:16] + "XX...XX",
            )

        return matches

    except ResourceError:
        log.error(
            "❌ Failed to verify checksum - file not found",
            path=str(path),
        )
        return False


def x_verify_file__mutmut_43(
    path: Path | str,
    expected_hash: str,
    algorithm: str = DEFAULT_ALGORITHM,
) -> bool:
    """Verify a file matches an expected hash.

    Args:
        path: File path
        expected_hash: Expected hash value
        algorithm: Hash algorithm

    Returns:
        True if hash matches, False otherwise

    Raises:
        ResourceError: If file cannot be read
        ValidationError: If algorithm is not supported

    """
    if isinstance(path, str):
        path = Path(path)

    try:
        actual_hash = hash_file(path, algorithm)
        matches = compare_hash(actual_hash, expected_hash)

        if matches:
            log.debug(
                "✅ Checksum verified",
                path=str(path),
                algorithm=algorithm,
            )
        else:
            log.warning(
                "❌ Checksum mismatch",
                path=str(path),
                algorithm=algorithm,
                expected=expected_hash[:16] + "...",
                actual=actual_hash[:16] + "...",
            )

        return matches

    except ResourceError:
        log.error(
            None,
            path=str(path),
        )
        return False


def x_verify_file__mutmut_44(
    path: Path | str,
    expected_hash: str,
    algorithm: str = DEFAULT_ALGORITHM,
) -> bool:
    """Verify a file matches an expected hash.

    Args:
        path: File path
        expected_hash: Expected hash value
        algorithm: Hash algorithm

    Returns:
        True if hash matches, False otherwise

    Raises:
        ResourceError: If file cannot be read
        ValidationError: If algorithm is not supported

    """
    if isinstance(path, str):
        path = Path(path)

    try:
        actual_hash = hash_file(path, algorithm)
        matches = compare_hash(actual_hash, expected_hash)

        if matches:
            log.debug(
                "✅ Checksum verified",
                path=str(path),
                algorithm=algorithm,
            )
        else:
            log.warning(
                "❌ Checksum mismatch",
                path=str(path),
                algorithm=algorithm,
                expected=expected_hash[:16] + "...",
                actual=actual_hash[:16] + "...",
            )

        return matches

    except ResourceError:
        log.error(
            "❌ Failed to verify checksum - file not found",
            path=None,
        )
        return False


def x_verify_file__mutmut_45(
    path: Path | str,
    expected_hash: str,
    algorithm: str = DEFAULT_ALGORITHM,
) -> bool:
    """Verify a file matches an expected hash.

    Args:
        path: File path
        expected_hash: Expected hash value
        algorithm: Hash algorithm

    Returns:
        True if hash matches, False otherwise

    Raises:
        ResourceError: If file cannot be read
        ValidationError: If algorithm is not supported

    """
    if isinstance(path, str):
        path = Path(path)

    try:
        actual_hash = hash_file(path, algorithm)
        matches = compare_hash(actual_hash, expected_hash)

        if matches:
            log.debug(
                "✅ Checksum verified",
                path=str(path),
                algorithm=algorithm,
            )
        else:
            log.warning(
                "❌ Checksum mismatch",
                path=str(path),
                algorithm=algorithm,
                expected=expected_hash[:16] + "...",
                actual=actual_hash[:16] + "...",
            )

        return matches

    except ResourceError:
        log.error(
            path=str(path),
        )
        return False


def x_verify_file__mutmut_46(
    path: Path | str,
    expected_hash: str,
    algorithm: str = DEFAULT_ALGORITHM,
) -> bool:
    """Verify a file matches an expected hash.

    Args:
        path: File path
        expected_hash: Expected hash value
        algorithm: Hash algorithm

    Returns:
        True if hash matches, False otherwise

    Raises:
        ResourceError: If file cannot be read
        ValidationError: If algorithm is not supported

    """
    if isinstance(path, str):
        path = Path(path)

    try:
        actual_hash = hash_file(path, algorithm)
        matches = compare_hash(actual_hash, expected_hash)

        if matches:
            log.debug(
                "✅ Checksum verified",
                path=str(path),
                algorithm=algorithm,
            )
        else:
            log.warning(
                "❌ Checksum mismatch",
                path=str(path),
                algorithm=algorithm,
                expected=expected_hash[:16] + "...",
                actual=actual_hash[:16] + "...",
            )

        return matches

    except ResourceError:
        log.error(
            "❌ Failed to verify checksum - file not found",
        )
        return False


def x_verify_file__mutmut_47(
    path: Path | str,
    expected_hash: str,
    algorithm: str = DEFAULT_ALGORITHM,
) -> bool:
    """Verify a file matches an expected hash.

    Args:
        path: File path
        expected_hash: Expected hash value
        algorithm: Hash algorithm

    Returns:
        True if hash matches, False otherwise

    Raises:
        ResourceError: If file cannot be read
        ValidationError: If algorithm is not supported

    """
    if isinstance(path, str):
        path = Path(path)

    try:
        actual_hash = hash_file(path, algorithm)
        matches = compare_hash(actual_hash, expected_hash)

        if matches:
            log.debug(
                "✅ Checksum verified",
                path=str(path),
                algorithm=algorithm,
            )
        else:
            log.warning(
                "❌ Checksum mismatch",
                path=str(path),
                algorithm=algorithm,
                expected=expected_hash[:16] + "...",
                actual=actual_hash[:16] + "...",
            )

        return matches

    except ResourceError:
        log.error(
            "XX❌ Failed to verify checksum - file not foundXX",
            path=str(path),
        )
        return False


def x_verify_file__mutmut_48(
    path: Path | str,
    expected_hash: str,
    algorithm: str = DEFAULT_ALGORITHM,
) -> bool:
    """Verify a file matches an expected hash.

    Args:
        path: File path
        expected_hash: Expected hash value
        algorithm: Hash algorithm

    Returns:
        True if hash matches, False otherwise

    Raises:
        ResourceError: If file cannot be read
        ValidationError: If algorithm is not supported

    """
    if isinstance(path, str):
        path = Path(path)

    try:
        actual_hash = hash_file(path, algorithm)
        matches = compare_hash(actual_hash, expected_hash)

        if matches:
            log.debug(
                "✅ Checksum verified",
                path=str(path),
                algorithm=algorithm,
            )
        else:
            log.warning(
                "❌ Checksum mismatch",
                path=str(path),
                algorithm=algorithm,
                expected=expected_hash[:16] + "...",
                actual=actual_hash[:16] + "...",
            )

        return matches

    except ResourceError:
        log.error(
            "❌ failed to verify checksum - file not found",
            path=str(path),
        )
        return False


def x_verify_file__mutmut_49(
    path: Path | str,
    expected_hash: str,
    algorithm: str = DEFAULT_ALGORITHM,
) -> bool:
    """Verify a file matches an expected hash.

    Args:
        path: File path
        expected_hash: Expected hash value
        algorithm: Hash algorithm

    Returns:
        True if hash matches, False otherwise

    Raises:
        ResourceError: If file cannot be read
        ValidationError: If algorithm is not supported

    """
    if isinstance(path, str):
        path = Path(path)

    try:
        actual_hash = hash_file(path, algorithm)
        matches = compare_hash(actual_hash, expected_hash)

        if matches:
            log.debug(
                "✅ Checksum verified",
                path=str(path),
                algorithm=algorithm,
            )
        else:
            log.warning(
                "❌ Checksum mismatch",
                path=str(path),
                algorithm=algorithm,
                expected=expected_hash[:16] + "...",
                actual=actual_hash[:16] + "...",
            )

        return matches

    except ResourceError:
        log.error(
            "❌ FAILED TO VERIFY CHECKSUM - FILE NOT FOUND",
            path=str(path),
        )
        return False


def x_verify_file__mutmut_50(
    path: Path | str,
    expected_hash: str,
    algorithm: str = DEFAULT_ALGORITHM,
) -> bool:
    """Verify a file matches an expected hash.

    Args:
        path: File path
        expected_hash: Expected hash value
        algorithm: Hash algorithm

    Returns:
        True if hash matches, False otherwise

    Raises:
        ResourceError: If file cannot be read
        ValidationError: If algorithm is not supported

    """
    if isinstance(path, str):
        path = Path(path)

    try:
        actual_hash = hash_file(path, algorithm)
        matches = compare_hash(actual_hash, expected_hash)

        if matches:
            log.debug(
                "✅ Checksum verified",
                path=str(path),
                algorithm=algorithm,
            )
        else:
            log.warning(
                "❌ Checksum mismatch",
                path=str(path),
                algorithm=algorithm,
                expected=expected_hash[:16] + "...",
                actual=actual_hash[:16] + "...",
            )

        return matches

    except ResourceError:
        log.error(
            "❌ Failed to verify checksum - file not found",
            path=str(None),
        )
        return False


def x_verify_file__mutmut_51(
    path: Path | str,
    expected_hash: str,
    algorithm: str = DEFAULT_ALGORITHM,
) -> bool:
    """Verify a file matches an expected hash.

    Args:
        path: File path
        expected_hash: Expected hash value
        algorithm: Hash algorithm

    Returns:
        True if hash matches, False otherwise

    Raises:
        ResourceError: If file cannot be read
        ValidationError: If algorithm is not supported

    """
    if isinstance(path, str):
        path = Path(path)

    try:
        actual_hash = hash_file(path, algorithm)
        matches = compare_hash(actual_hash, expected_hash)

        if matches:
            log.debug(
                "✅ Checksum verified",
                path=str(path),
                algorithm=algorithm,
            )
        else:
            log.warning(
                "❌ Checksum mismatch",
                path=str(path),
                algorithm=algorithm,
                expected=expected_hash[:16] + "...",
                actual=actual_hash[:16] + "...",
            )

        return matches

    except ResourceError:
        log.error(
            "❌ Failed to verify checksum - file not found",
            path=str(path),
        )
        return True


x_verify_file__mutmut_mutants: ClassVar[MutantDict] = {
    "x_verify_file__mutmut_1": x_verify_file__mutmut_1,
    "x_verify_file__mutmut_2": x_verify_file__mutmut_2,
    "x_verify_file__mutmut_3": x_verify_file__mutmut_3,
    "x_verify_file__mutmut_4": x_verify_file__mutmut_4,
    "x_verify_file__mutmut_5": x_verify_file__mutmut_5,
    "x_verify_file__mutmut_6": x_verify_file__mutmut_6,
    "x_verify_file__mutmut_7": x_verify_file__mutmut_7,
    "x_verify_file__mutmut_8": x_verify_file__mutmut_8,
    "x_verify_file__mutmut_9": x_verify_file__mutmut_9,
    "x_verify_file__mutmut_10": x_verify_file__mutmut_10,
    "x_verify_file__mutmut_11": x_verify_file__mutmut_11,
    "x_verify_file__mutmut_12": x_verify_file__mutmut_12,
    "x_verify_file__mutmut_13": x_verify_file__mutmut_13,
    "x_verify_file__mutmut_14": x_verify_file__mutmut_14,
    "x_verify_file__mutmut_15": x_verify_file__mutmut_15,
    "x_verify_file__mutmut_16": x_verify_file__mutmut_16,
    "x_verify_file__mutmut_17": x_verify_file__mutmut_17,
    "x_verify_file__mutmut_18": x_verify_file__mutmut_18,
    "x_verify_file__mutmut_19": x_verify_file__mutmut_19,
    "x_verify_file__mutmut_20": x_verify_file__mutmut_20,
    "x_verify_file__mutmut_21": x_verify_file__mutmut_21,
    "x_verify_file__mutmut_22": x_verify_file__mutmut_22,
    "x_verify_file__mutmut_23": x_verify_file__mutmut_23,
    "x_verify_file__mutmut_24": x_verify_file__mutmut_24,
    "x_verify_file__mutmut_25": x_verify_file__mutmut_25,
    "x_verify_file__mutmut_26": x_verify_file__mutmut_26,
    "x_verify_file__mutmut_27": x_verify_file__mutmut_27,
    "x_verify_file__mutmut_28": x_verify_file__mutmut_28,
    "x_verify_file__mutmut_29": x_verify_file__mutmut_29,
    "x_verify_file__mutmut_30": x_verify_file__mutmut_30,
    "x_verify_file__mutmut_31": x_verify_file__mutmut_31,
    "x_verify_file__mutmut_32": x_verify_file__mutmut_32,
    "x_verify_file__mutmut_33": x_verify_file__mutmut_33,
    "x_verify_file__mutmut_34": x_verify_file__mutmut_34,
    "x_verify_file__mutmut_35": x_verify_file__mutmut_35,
    "x_verify_file__mutmut_36": x_verify_file__mutmut_36,
    "x_verify_file__mutmut_37": x_verify_file__mutmut_37,
    "x_verify_file__mutmut_38": x_verify_file__mutmut_38,
    "x_verify_file__mutmut_39": x_verify_file__mutmut_39,
    "x_verify_file__mutmut_40": x_verify_file__mutmut_40,
    "x_verify_file__mutmut_41": x_verify_file__mutmut_41,
    "x_verify_file__mutmut_42": x_verify_file__mutmut_42,
    "x_verify_file__mutmut_43": x_verify_file__mutmut_43,
    "x_verify_file__mutmut_44": x_verify_file__mutmut_44,
    "x_verify_file__mutmut_45": x_verify_file__mutmut_45,
    "x_verify_file__mutmut_46": x_verify_file__mutmut_46,
    "x_verify_file__mutmut_47": x_verify_file__mutmut_47,
    "x_verify_file__mutmut_48": x_verify_file__mutmut_48,
    "x_verify_file__mutmut_49": x_verify_file__mutmut_49,
    "x_verify_file__mutmut_50": x_verify_file__mutmut_50,
    "x_verify_file__mutmut_51": x_verify_file__mutmut_51,
}


def verify_file(*args, **kwargs):
    result = _mutmut_trampoline(x_verify_file__mutmut_orig, x_verify_file__mutmut_mutants, args, kwargs)
    return result


verify_file.__signature__ = _mutmut_signature(x_verify_file__mutmut_orig)
x_verify_file__mutmut_orig.__name__ = "x_verify_file"


def x_verify_data__mutmut_orig(
    data: bytes,
    expected_hash: str,
    algorithm: str = DEFAULT_ALGORITHM,
) -> bool:
    """Verify data matches an expected hash.

    Args:
        data: Data to verify
        expected_hash: Expected hash value
        algorithm: Hash algorithm

    Returns:
        True if hash matches, False otherwise

    Raises:
        ValidationError: If algorithm is not supported

    """
    actual_hash = hash_data(data, algorithm)
    matches = compare_hash(actual_hash, expected_hash)

    if matches:
        log.debug(
            "✅ Data checksum verified",
            algorithm=algorithm,
            size=len(data),
        )
    else:
        log.warning(
            "❌ Data checksum mismatch",
            algorithm=algorithm,
            expected=expected_hash[:16] + "...",
            actual=actual_hash[:16] + "...",
        )

    return matches


def x_verify_data__mutmut_1(
    data: bytes,
    expected_hash: str,
    algorithm: str = DEFAULT_ALGORITHM,
) -> bool:
    """Verify data matches an expected hash.

    Args:
        data: Data to verify
        expected_hash: Expected hash value
        algorithm: Hash algorithm

    Returns:
        True if hash matches, False otherwise

    Raises:
        ValidationError: If algorithm is not supported

    """
    actual_hash = None
    matches = compare_hash(actual_hash, expected_hash)

    if matches:
        log.debug(
            "✅ Data checksum verified",
            algorithm=algorithm,
            size=len(data),
        )
    else:
        log.warning(
            "❌ Data checksum mismatch",
            algorithm=algorithm,
            expected=expected_hash[:16] + "...",
            actual=actual_hash[:16] + "...",
        )

    return matches


def x_verify_data__mutmut_2(
    data: bytes,
    expected_hash: str,
    algorithm: str = DEFAULT_ALGORITHM,
) -> bool:
    """Verify data matches an expected hash.

    Args:
        data: Data to verify
        expected_hash: Expected hash value
        algorithm: Hash algorithm

    Returns:
        True if hash matches, False otherwise

    Raises:
        ValidationError: If algorithm is not supported

    """
    actual_hash = hash_data(None, algorithm)
    matches = compare_hash(actual_hash, expected_hash)

    if matches:
        log.debug(
            "✅ Data checksum verified",
            algorithm=algorithm,
            size=len(data),
        )
    else:
        log.warning(
            "❌ Data checksum mismatch",
            algorithm=algorithm,
            expected=expected_hash[:16] + "...",
            actual=actual_hash[:16] + "...",
        )

    return matches


def x_verify_data__mutmut_3(
    data: bytes,
    expected_hash: str,
    algorithm: str = DEFAULT_ALGORITHM,
) -> bool:
    """Verify data matches an expected hash.

    Args:
        data: Data to verify
        expected_hash: Expected hash value
        algorithm: Hash algorithm

    Returns:
        True if hash matches, False otherwise

    Raises:
        ValidationError: If algorithm is not supported

    """
    actual_hash = hash_data(data, None)
    matches = compare_hash(actual_hash, expected_hash)

    if matches:
        log.debug(
            "✅ Data checksum verified",
            algorithm=algorithm,
            size=len(data),
        )
    else:
        log.warning(
            "❌ Data checksum mismatch",
            algorithm=algorithm,
            expected=expected_hash[:16] + "...",
            actual=actual_hash[:16] + "...",
        )

    return matches


def x_verify_data__mutmut_4(
    data: bytes,
    expected_hash: str,
    algorithm: str = DEFAULT_ALGORITHM,
) -> bool:
    """Verify data matches an expected hash.

    Args:
        data: Data to verify
        expected_hash: Expected hash value
        algorithm: Hash algorithm

    Returns:
        True if hash matches, False otherwise

    Raises:
        ValidationError: If algorithm is not supported

    """
    actual_hash = hash_data(algorithm)
    matches = compare_hash(actual_hash, expected_hash)

    if matches:
        log.debug(
            "✅ Data checksum verified",
            algorithm=algorithm,
            size=len(data),
        )
    else:
        log.warning(
            "❌ Data checksum mismatch",
            algorithm=algorithm,
            expected=expected_hash[:16] + "...",
            actual=actual_hash[:16] + "...",
        )

    return matches


def x_verify_data__mutmut_5(
    data: bytes,
    expected_hash: str,
    algorithm: str = DEFAULT_ALGORITHM,
) -> bool:
    """Verify data matches an expected hash.

    Args:
        data: Data to verify
        expected_hash: Expected hash value
        algorithm: Hash algorithm

    Returns:
        True if hash matches, False otherwise

    Raises:
        ValidationError: If algorithm is not supported

    """
    actual_hash = hash_data(
        data,
    )
    matches = compare_hash(actual_hash, expected_hash)

    if matches:
        log.debug(
            "✅ Data checksum verified",
            algorithm=algorithm,
            size=len(data),
        )
    else:
        log.warning(
            "❌ Data checksum mismatch",
            algorithm=algorithm,
            expected=expected_hash[:16] + "...",
            actual=actual_hash[:16] + "...",
        )

    return matches


def x_verify_data__mutmut_6(
    data: bytes,
    expected_hash: str,
    algorithm: str = DEFAULT_ALGORITHM,
) -> bool:
    """Verify data matches an expected hash.

    Args:
        data: Data to verify
        expected_hash: Expected hash value
        algorithm: Hash algorithm

    Returns:
        True if hash matches, False otherwise

    Raises:
        ValidationError: If algorithm is not supported

    """
    actual_hash = hash_data(data, algorithm)
    matches = None

    if matches:
        log.debug(
            "✅ Data checksum verified",
            algorithm=algorithm,
            size=len(data),
        )
    else:
        log.warning(
            "❌ Data checksum mismatch",
            algorithm=algorithm,
            expected=expected_hash[:16] + "...",
            actual=actual_hash[:16] + "...",
        )

    return matches


def x_verify_data__mutmut_7(
    data: bytes,
    expected_hash: str,
    algorithm: str = DEFAULT_ALGORITHM,
) -> bool:
    """Verify data matches an expected hash.

    Args:
        data: Data to verify
        expected_hash: Expected hash value
        algorithm: Hash algorithm

    Returns:
        True if hash matches, False otherwise

    Raises:
        ValidationError: If algorithm is not supported

    """
    actual_hash = hash_data(data, algorithm)
    matches = compare_hash(None, expected_hash)

    if matches:
        log.debug(
            "✅ Data checksum verified",
            algorithm=algorithm,
            size=len(data),
        )
    else:
        log.warning(
            "❌ Data checksum mismatch",
            algorithm=algorithm,
            expected=expected_hash[:16] + "...",
            actual=actual_hash[:16] + "...",
        )

    return matches


def x_verify_data__mutmut_8(
    data: bytes,
    expected_hash: str,
    algorithm: str = DEFAULT_ALGORITHM,
) -> bool:
    """Verify data matches an expected hash.

    Args:
        data: Data to verify
        expected_hash: Expected hash value
        algorithm: Hash algorithm

    Returns:
        True if hash matches, False otherwise

    Raises:
        ValidationError: If algorithm is not supported

    """
    actual_hash = hash_data(data, algorithm)
    matches = compare_hash(actual_hash, None)

    if matches:
        log.debug(
            "✅ Data checksum verified",
            algorithm=algorithm,
            size=len(data),
        )
    else:
        log.warning(
            "❌ Data checksum mismatch",
            algorithm=algorithm,
            expected=expected_hash[:16] + "...",
            actual=actual_hash[:16] + "...",
        )

    return matches


def x_verify_data__mutmut_9(
    data: bytes,
    expected_hash: str,
    algorithm: str = DEFAULT_ALGORITHM,
) -> bool:
    """Verify data matches an expected hash.

    Args:
        data: Data to verify
        expected_hash: Expected hash value
        algorithm: Hash algorithm

    Returns:
        True if hash matches, False otherwise

    Raises:
        ValidationError: If algorithm is not supported

    """
    actual_hash = hash_data(data, algorithm)
    matches = compare_hash(expected_hash)

    if matches:
        log.debug(
            "✅ Data checksum verified",
            algorithm=algorithm,
            size=len(data),
        )
    else:
        log.warning(
            "❌ Data checksum mismatch",
            algorithm=algorithm,
            expected=expected_hash[:16] + "...",
            actual=actual_hash[:16] + "...",
        )

    return matches


def x_verify_data__mutmut_10(
    data: bytes,
    expected_hash: str,
    algorithm: str = DEFAULT_ALGORITHM,
) -> bool:
    """Verify data matches an expected hash.

    Args:
        data: Data to verify
        expected_hash: Expected hash value
        algorithm: Hash algorithm

    Returns:
        True if hash matches, False otherwise

    Raises:
        ValidationError: If algorithm is not supported

    """
    actual_hash = hash_data(data, algorithm)
    matches = compare_hash(
        actual_hash,
    )

    if matches:
        log.debug(
            "✅ Data checksum verified",
            algorithm=algorithm,
            size=len(data),
        )
    else:
        log.warning(
            "❌ Data checksum mismatch",
            algorithm=algorithm,
            expected=expected_hash[:16] + "...",
            actual=actual_hash[:16] + "...",
        )

    return matches


def x_verify_data__mutmut_11(
    data: bytes,
    expected_hash: str,
    algorithm: str = DEFAULT_ALGORITHM,
) -> bool:
    """Verify data matches an expected hash.

    Args:
        data: Data to verify
        expected_hash: Expected hash value
        algorithm: Hash algorithm

    Returns:
        True if hash matches, False otherwise

    Raises:
        ValidationError: If algorithm is not supported

    """
    actual_hash = hash_data(data, algorithm)
    matches = compare_hash(actual_hash, expected_hash)

    if matches:
        log.debug(
            None,
            algorithm=algorithm,
            size=len(data),
        )
    else:
        log.warning(
            "❌ Data checksum mismatch",
            algorithm=algorithm,
            expected=expected_hash[:16] + "...",
            actual=actual_hash[:16] + "...",
        )

    return matches


def x_verify_data__mutmut_12(
    data: bytes,
    expected_hash: str,
    algorithm: str = DEFAULT_ALGORITHM,
) -> bool:
    """Verify data matches an expected hash.

    Args:
        data: Data to verify
        expected_hash: Expected hash value
        algorithm: Hash algorithm

    Returns:
        True if hash matches, False otherwise

    Raises:
        ValidationError: If algorithm is not supported

    """
    actual_hash = hash_data(data, algorithm)
    matches = compare_hash(actual_hash, expected_hash)

    if matches:
        log.debug(
            "✅ Data checksum verified",
            algorithm=None,
            size=len(data),
        )
    else:
        log.warning(
            "❌ Data checksum mismatch",
            algorithm=algorithm,
            expected=expected_hash[:16] + "...",
            actual=actual_hash[:16] + "...",
        )

    return matches


def x_verify_data__mutmut_13(
    data: bytes,
    expected_hash: str,
    algorithm: str = DEFAULT_ALGORITHM,
) -> bool:
    """Verify data matches an expected hash.

    Args:
        data: Data to verify
        expected_hash: Expected hash value
        algorithm: Hash algorithm

    Returns:
        True if hash matches, False otherwise

    Raises:
        ValidationError: If algorithm is not supported

    """
    actual_hash = hash_data(data, algorithm)
    matches = compare_hash(actual_hash, expected_hash)

    if matches:
        log.debug(
            "✅ Data checksum verified",
            algorithm=algorithm,
            size=None,
        )
    else:
        log.warning(
            "❌ Data checksum mismatch",
            algorithm=algorithm,
            expected=expected_hash[:16] + "...",
            actual=actual_hash[:16] + "...",
        )

    return matches


def x_verify_data__mutmut_14(
    data: bytes,
    expected_hash: str,
    algorithm: str = DEFAULT_ALGORITHM,
) -> bool:
    """Verify data matches an expected hash.

    Args:
        data: Data to verify
        expected_hash: Expected hash value
        algorithm: Hash algorithm

    Returns:
        True if hash matches, False otherwise

    Raises:
        ValidationError: If algorithm is not supported

    """
    actual_hash = hash_data(data, algorithm)
    matches = compare_hash(actual_hash, expected_hash)

    if matches:
        log.debug(
            algorithm=algorithm,
            size=len(data),
        )
    else:
        log.warning(
            "❌ Data checksum mismatch",
            algorithm=algorithm,
            expected=expected_hash[:16] + "...",
            actual=actual_hash[:16] + "...",
        )

    return matches


def x_verify_data__mutmut_15(
    data: bytes,
    expected_hash: str,
    algorithm: str = DEFAULT_ALGORITHM,
) -> bool:
    """Verify data matches an expected hash.

    Args:
        data: Data to verify
        expected_hash: Expected hash value
        algorithm: Hash algorithm

    Returns:
        True if hash matches, False otherwise

    Raises:
        ValidationError: If algorithm is not supported

    """
    actual_hash = hash_data(data, algorithm)
    matches = compare_hash(actual_hash, expected_hash)

    if matches:
        log.debug(
            "✅ Data checksum verified",
            size=len(data),
        )
    else:
        log.warning(
            "❌ Data checksum mismatch",
            algorithm=algorithm,
            expected=expected_hash[:16] + "...",
            actual=actual_hash[:16] + "...",
        )

    return matches


def x_verify_data__mutmut_16(
    data: bytes,
    expected_hash: str,
    algorithm: str = DEFAULT_ALGORITHM,
) -> bool:
    """Verify data matches an expected hash.

    Args:
        data: Data to verify
        expected_hash: Expected hash value
        algorithm: Hash algorithm

    Returns:
        True if hash matches, False otherwise

    Raises:
        ValidationError: If algorithm is not supported

    """
    actual_hash = hash_data(data, algorithm)
    matches = compare_hash(actual_hash, expected_hash)

    if matches:
        log.debug(
            "✅ Data checksum verified",
            algorithm=algorithm,
        )
    else:
        log.warning(
            "❌ Data checksum mismatch",
            algorithm=algorithm,
            expected=expected_hash[:16] + "...",
            actual=actual_hash[:16] + "...",
        )

    return matches


def x_verify_data__mutmut_17(
    data: bytes,
    expected_hash: str,
    algorithm: str = DEFAULT_ALGORITHM,
) -> bool:
    """Verify data matches an expected hash.

    Args:
        data: Data to verify
        expected_hash: Expected hash value
        algorithm: Hash algorithm

    Returns:
        True if hash matches, False otherwise

    Raises:
        ValidationError: If algorithm is not supported

    """
    actual_hash = hash_data(data, algorithm)
    matches = compare_hash(actual_hash, expected_hash)

    if matches:
        log.debug(
            "XX✅ Data checksum verifiedXX",
            algorithm=algorithm,
            size=len(data),
        )
    else:
        log.warning(
            "❌ Data checksum mismatch",
            algorithm=algorithm,
            expected=expected_hash[:16] + "...",
            actual=actual_hash[:16] + "...",
        )

    return matches


def x_verify_data__mutmut_18(
    data: bytes,
    expected_hash: str,
    algorithm: str = DEFAULT_ALGORITHM,
) -> bool:
    """Verify data matches an expected hash.

    Args:
        data: Data to verify
        expected_hash: Expected hash value
        algorithm: Hash algorithm

    Returns:
        True if hash matches, False otherwise

    Raises:
        ValidationError: If algorithm is not supported

    """
    actual_hash = hash_data(data, algorithm)
    matches = compare_hash(actual_hash, expected_hash)

    if matches:
        log.debug(
            "✅ data checksum verified",
            algorithm=algorithm,
            size=len(data),
        )
    else:
        log.warning(
            "❌ Data checksum mismatch",
            algorithm=algorithm,
            expected=expected_hash[:16] + "...",
            actual=actual_hash[:16] + "...",
        )

    return matches


def x_verify_data__mutmut_19(
    data: bytes,
    expected_hash: str,
    algorithm: str = DEFAULT_ALGORITHM,
) -> bool:
    """Verify data matches an expected hash.

    Args:
        data: Data to verify
        expected_hash: Expected hash value
        algorithm: Hash algorithm

    Returns:
        True if hash matches, False otherwise

    Raises:
        ValidationError: If algorithm is not supported

    """
    actual_hash = hash_data(data, algorithm)
    matches = compare_hash(actual_hash, expected_hash)

    if matches:
        log.debug(
            "✅ DATA CHECKSUM VERIFIED",
            algorithm=algorithm,
            size=len(data),
        )
    else:
        log.warning(
            "❌ Data checksum mismatch",
            algorithm=algorithm,
            expected=expected_hash[:16] + "...",
            actual=actual_hash[:16] + "...",
        )

    return matches


def x_verify_data__mutmut_20(
    data: bytes,
    expected_hash: str,
    algorithm: str = DEFAULT_ALGORITHM,
) -> bool:
    """Verify data matches an expected hash.

    Args:
        data: Data to verify
        expected_hash: Expected hash value
        algorithm: Hash algorithm

    Returns:
        True if hash matches, False otherwise

    Raises:
        ValidationError: If algorithm is not supported

    """
    actual_hash = hash_data(data, algorithm)
    matches = compare_hash(actual_hash, expected_hash)

    if matches:
        log.debug(
            "✅ Data checksum verified",
            algorithm=algorithm,
            size=len(data),
        )
    else:
        log.warning(
            None,
            algorithm=algorithm,
            expected=expected_hash[:16] + "...",
            actual=actual_hash[:16] + "...",
        )

    return matches


def x_verify_data__mutmut_21(
    data: bytes,
    expected_hash: str,
    algorithm: str = DEFAULT_ALGORITHM,
) -> bool:
    """Verify data matches an expected hash.

    Args:
        data: Data to verify
        expected_hash: Expected hash value
        algorithm: Hash algorithm

    Returns:
        True if hash matches, False otherwise

    Raises:
        ValidationError: If algorithm is not supported

    """
    actual_hash = hash_data(data, algorithm)
    matches = compare_hash(actual_hash, expected_hash)

    if matches:
        log.debug(
            "✅ Data checksum verified",
            algorithm=algorithm,
            size=len(data),
        )
    else:
        log.warning(
            "❌ Data checksum mismatch",
            algorithm=None,
            expected=expected_hash[:16] + "...",
            actual=actual_hash[:16] + "...",
        )

    return matches


def x_verify_data__mutmut_22(
    data: bytes,
    expected_hash: str,
    algorithm: str = DEFAULT_ALGORITHM,
) -> bool:
    """Verify data matches an expected hash.

    Args:
        data: Data to verify
        expected_hash: Expected hash value
        algorithm: Hash algorithm

    Returns:
        True if hash matches, False otherwise

    Raises:
        ValidationError: If algorithm is not supported

    """
    actual_hash = hash_data(data, algorithm)
    matches = compare_hash(actual_hash, expected_hash)

    if matches:
        log.debug(
            "✅ Data checksum verified",
            algorithm=algorithm,
            size=len(data),
        )
    else:
        log.warning(
            "❌ Data checksum mismatch",
            algorithm=algorithm,
            expected=None,
            actual=actual_hash[:16] + "...",
        )

    return matches


def x_verify_data__mutmut_23(
    data: bytes,
    expected_hash: str,
    algorithm: str = DEFAULT_ALGORITHM,
) -> bool:
    """Verify data matches an expected hash.

    Args:
        data: Data to verify
        expected_hash: Expected hash value
        algorithm: Hash algorithm

    Returns:
        True if hash matches, False otherwise

    Raises:
        ValidationError: If algorithm is not supported

    """
    actual_hash = hash_data(data, algorithm)
    matches = compare_hash(actual_hash, expected_hash)

    if matches:
        log.debug(
            "✅ Data checksum verified",
            algorithm=algorithm,
            size=len(data),
        )
    else:
        log.warning(
            "❌ Data checksum mismatch",
            algorithm=algorithm,
            expected=expected_hash[:16] + "...",
            actual=None,
        )

    return matches


def x_verify_data__mutmut_24(
    data: bytes,
    expected_hash: str,
    algorithm: str = DEFAULT_ALGORITHM,
) -> bool:
    """Verify data matches an expected hash.

    Args:
        data: Data to verify
        expected_hash: Expected hash value
        algorithm: Hash algorithm

    Returns:
        True if hash matches, False otherwise

    Raises:
        ValidationError: If algorithm is not supported

    """
    actual_hash = hash_data(data, algorithm)
    matches = compare_hash(actual_hash, expected_hash)

    if matches:
        log.debug(
            "✅ Data checksum verified",
            algorithm=algorithm,
            size=len(data),
        )
    else:
        log.warning(
            algorithm=algorithm,
            expected=expected_hash[:16] + "...",
            actual=actual_hash[:16] + "...",
        )

    return matches


def x_verify_data__mutmut_25(
    data: bytes,
    expected_hash: str,
    algorithm: str = DEFAULT_ALGORITHM,
) -> bool:
    """Verify data matches an expected hash.

    Args:
        data: Data to verify
        expected_hash: Expected hash value
        algorithm: Hash algorithm

    Returns:
        True if hash matches, False otherwise

    Raises:
        ValidationError: If algorithm is not supported

    """
    actual_hash = hash_data(data, algorithm)
    matches = compare_hash(actual_hash, expected_hash)

    if matches:
        log.debug(
            "✅ Data checksum verified",
            algorithm=algorithm,
            size=len(data),
        )
    else:
        log.warning(
            "❌ Data checksum mismatch",
            expected=expected_hash[:16] + "...",
            actual=actual_hash[:16] + "...",
        )

    return matches


def x_verify_data__mutmut_26(
    data: bytes,
    expected_hash: str,
    algorithm: str = DEFAULT_ALGORITHM,
) -> bool:
    """Verify data matches an expected hash.

    Args:
        data: Data to verify
        expected_hash: Expected hash value
        algorithm: Hash algorithm

    Returns:
        True if hash matches, False otherwise

    Raises:
        ValidationError: If algorithm is not supported

    """
    actual_hash = hash_data(data, algorithm)
    matches = compare_hash(actual_hash, expected_hash)

    if matches:
        log.debug(
            "✅ Data checksum verified",
            algorithm=algorithm,
            size=len(data),
        )
    else:
        log.warning(
            "❌ Data checksum mismatch",
            algorithm=algorithm,
            actual=actual_hash[:16] + "...",
        )

    return matches


def x_verify_data__mutmut_27(
    data: bytes,
    expected_hash: str,
    algorithm: str = DEFAULT_ALGORITHM,
) -> bool:
    """Verify data matches an expected hash.

    Args:
        data: Data to verify
        expected_hash: Expected hash value
        algorithm: Hash algorithm

    Returns:
        True if hash matches, False otherwise

    Raises:
        ValidationError: If algorithm is not supported

    """
    actual_hash = hash_data(data, algorithm)
    matches = compare_hash(actual_hash, expected_hash)

    if matches:
        log.debug(
            "✅ Data checksum verified",
            algorithm=algorithm,
            size=len(data),
        )
    else:
        log.warning(
            "❌ Data checksum mismatch",
            algorithm=algorithm,
            expected=expected_hash[:16] + "...",
        )

    return matches


def x_verify_data__mutmut_28(
    data: bytes,
    expected_hash: str,
    algorithm: str = DEFAULT_ALGORITHM,
) -> bool:
    """Verify data matches an expected hash.

    Args:
        data: Data to verify
        expected_hash: Expected hash value
        algorithm: Hash algorithm

    Returns:
        True if hash matches, False otherwise

    Raises:
        ValidationError: If algorithm is not supported

    """
    actual_hash = hash_data(data, algorithm)
    matches = compare_hash(actual_hash, expected_hash)

    if matches:
        log.debug(
            "✅ Data checksum verified",
            algorithm=algorithm,
            size=len(data),
        )
    else:
        log.warning(
            "XX❌ Data checksum mismatchXX",
            algorithm=algorithm,
            expected=expected_hash[:16] + "...",
            actual=actual_hash[:16] + "...",
        )

    return matches


def x_verify_data__mutmut_29(
    data: bytes,
    expected_hash: str,
    algorithm: str = DEFAULT_ALGORITHM,
) -> bool:
    """Verify data matches an expected hash.

    Args:
        data: Data to verify
        expected_hash: Expected hash value
        algorithm: Hash algorithm

    Returns:
        True if hash matches, False otherwise

    Raises:
        ValidationError: If algorithm is not supported

    """
    actual_hash = hash_data(data, algorithm)
    matches = compare_hash(actual_hash, expected_hash)

    if matches:
        log.debug(
            "✅ Data checksum verified",
            algorithm=algorithm,
            size=len(data),
        )
    else:
        log.warning(
            "❌ data checksum mismatch",
            algorithm=algorithm,
            expected=expected_hash[:16] + "...",
            actual=actual_hash[:16] + "...",
        )

    return matches


def x_verify_data__mutmut_30(
    data: bytes,
    expected_hash: str,
    algorithm: str = DEFAULT_ALGORITHM,
) -> bool:
    """Verify data matches an expected hash.

    Args:
        data: Data to verify
        expected_hash: Expected hash value
        algorithm: Hash algorithm

    Returns:
        True if hash matches, False otherwise

    Raises:
        ValidationError: If algorithm is not supported

    """
    actual_hash = hash_data(data, algorithm)
    matches = compare_hash(actual_hash, expected_hash)

    if matches:
        log.debug(
            "✅ Data checksum verified",
            algorithm=algorithm,
            size=len(data),
        )
    else:
        log.warning(
            "❌ DATA CHECKSUM MISMATCH",
            algorithm=algorithm,
            expected=expected_hash[:16] + "...",
            actual=actual_hash[:16] + "...",
        )

    return matches


def x_verify_data__mutmut_31(
    data: bytes,
    expected_hash: str,
    algorithm: str = DEFAULT_ALGORITHM,
) -> bool:
    """Verify data matches an expected hash.

    Args:
        data: Data to verify
        expected_hash: Expected hash value
        algorithm: Hash algorithm

    Returns:
        True if hash matches, False otherwise

    Raises:
        ValidationError: If algorithm is not supported

    """
    actual_hash = hash_data(data, algorithm)
    matches = compare_hash(actual_hash, expected_hash)

    if matches:
        log.debug(
            "✅ Data checksum verified",
            algorithm=algorithm,
            size=len(data),
        )
    else:
        log.warning(
            "❌ Data checksum mismatch",
            algorithm=algorithm,
            expected=expected_hash[:16] - "...",
            actual=actual_hash[:16] + "...",
        )

    return matches


def x_verify_data__mutmut_32(
    data: bytes,
    expected_hash: str,
    algorithm: str = DEFAULT_ALGORITHM,
) -> bool:
    """Verify data matches an expected hash.

    Args:
        data: Data to verify
        expected_hash: Expected hash value
        algorithm: Hash algorithm

    Returns:
        True if hash matches, False otherwise

    Raises:
        ValidationError: If algorithm is not supported

    """
    actual_hash = hash_data(data, algorithm)
    matches = compare_hash(actual_hash, expected_hash)

    if matches:
        log.debug(
            "✅ Data checksum verified",
            algorithm=algorithm,
            size=len(data),
        )
    else:
        log.warning(
            "❌ Data checksum mismatch",
            algorithm=algorithm,
            expected=expected_hash[:17] + "...",
            actual=actual_hash[:16] + "...",
        )

    return matches


def x_verify_data__mutmut_33(
    data: bytes,
    expected_hash: str,
    algorithm: str = DEFAULT_ALGORITHM,
) -> bool:
    """Verify data matches an expected hash.

    Args:
        data: Data to verify
        expected_hash: Expected hash value
        algorithm: Hash algorithm

    Returns:
        True if hash matches, False otherwise

    Raises:
        ValidationError: If algorithm is not supported

    """
    actual_hash = hash_data(data, algorithm)
    matches = compare_hash(actual_hash, expected_hash)

    if matches:
        log.debug(
            "✅ Data checksum verified",
            algorithm=algorithm,
            size=len(data),
        )
    else:
        log.warning(
            "❌ Data checksum mismatch",
            algorithm=algorithm,
            expected=expected_hash[:16] + "XX...XX",
            actual=actual_hash[:16] + "...",
        )

    return matches


def x_verify_data__mutmut_34(
    data: bytes,
    expected_hash: str,
    algorithm: str = DEFAULT_ALGORITHM,
) -> bool:
    """Verify data matches an expected hash.

    Args:
        data: Data to verify
        expected_hash: Expected hash value
        algorithm: Hash algorithm

    Returns:
        True if hash matches, False otherwise

    Raises:
        ValidationError: If algorithm is not supported

    """
    actual_hash = hash_data(data, algorithm)
    matches = compare_hash(actual_hash, expected_hash)

    if matches:
        log.debug(
            "✅ Data checksum verified",
            algorithm=algorithm,
            size=len(data),
        )
    else:
        log.warning(
            "❌ Data checksum mismatch",
            algorithm=algorithm,
            expected=expected_hash[:16] + "...",
            actual=actual_hash[:16] - "...",
        )

    return matches


def x_verify_data__mutmut_35(
    data: bytes,
    expected_hash: str,
    algorithm: str = DEFAULT_ALGORITHM,
) -> bool:
    """Verify data matches an expected hash.

    Args:
        data: Data to verify
        expected_hash: Expected hash value
        algorithm: Hash algorithm

    Returns:
        True if hash matches, False otherwise

    Raises:
        ValidationError: If algorithm is not supported

    """
    actual_hash = hash_data(data, algorithm)
    matches = compare_hash(actual_hash, expected_hash)

    if matches:
        log.debug(
            "✅ Data checksum verified",
            algorithm=algorithm,
            size=len(data),
        )
    else:
        log.warning(
            "❌ Data checksum mismatch",
            algorithm=algorithm,
            expected=expected_hash[:16] + "...",
            actual=actual_hash[:17] + "...",
        )

    return matches


def x_verify_data__mutmut_36(
    data: bytes,
    expected_hash: str,
    algorithm: str = DEFAULT_ALGORITHM,
) -> bool:
    """Verify data matches an expected hash.

    Args:
        data: Data to verify
        expected_hash: Expected hash value
        algorithm: Hash algorithm

    Returns:
        True if hash matches, False otherwise

    Raises:
        ValidationError: If algorithm is not supported

    """
    actual_hash = hash_data(data, algorithm)
    matches = compare_hash(actual_hash, expected_hash)

    if matches:
        log.debug(
            "✅ Data checksum verified",
            algorithm=algorithm,
            size=len(data),
        )
    else:
        log.warning(
            "❌ Data checksum mismatch",
            algorithm=algorithm,
            expected=expected_hash[:16] + "...",
            actual=actual_hash[:16] + "XX...XX",
        )

    return matches


x_verify_data__mutmut_mutants: ClassVar[MutantDict] = {
    "x_verify_data__mutmut_1": x_verify_data__mutmut_1,
    "x_verify_data__mutmut_2": x_verify_data__mutmut_2,
    "x_verify_data__mutmut_3": x_verify_data__mutmut_3,
    "x_verify_data__mutmut_4": x_verify_data__mutmut_4,
    "x_verify_data__mutmut_5": x_verify_data__mutmut_5,
    "x_verify_data__mutmut_6": x_verify_data__mutmut_6,
    "x_verify_data__mutmut_7": x_verify_data__mutmut_7,
    "x_verify_data__mutmut_8": x_verify_data__mutmut_8,
    "x_verify_data__mutmut_9": x_verify_data__mutmut_9,
    "x_verify_data__mutmut_10": x_verify_data__mutmut_10,
    "x_verify_data__mutmut_11": x_verify_data__mutmut_11,
    "x_verify_data__mutmut_12": x_verify_data__mutmut_12,
    "x_verify_data__mutmut_13": x_verify_data__mutmut_13,
    "x_verify_data__mutmut_14": x_verify_data__mutmut_14,
    "x_verify_data__mutmut_15": x_verify_data__mutmut_15,
    "x_verify_data__mutmut_16": x_verify_data__mutmut_16,
    "x_verify_data__mutmut_17": x_verify_data__mutmut_17,
    "x_verify_data__mutmut_18": x_verify_data__mutmut_18,
    "x_verify_data__mutmut_19": x_verify_data__mutmut_19,
    "x_verify_data__mutmut_20": x_verify_data__mutmut_20,
    "x_verify_data__mutmut_21": x_verify_data__mutmut_21,
    "x_verify_data__mutmut_22": x_verify_data__mutmut_22,
    "x_verify_data__mutmut_23": x_verify_data__mutmut_23,
    "x_verify_data__mutmut_24": x_verify_data__mutmut_24,
    "x_verify_data__mutmut_25": x_verify_data__mutmut_25,
    "x_verify_data__mutmut_26": x_verify_data__mutmut_26,
    "x_verify_data__mutmut_27": x_verify_data__mutmut_27,
    "x_verify_data__mutmut_28": x_verify_data__mutmut_28,
    "x_verify_data__mutmut_29": x_verify_data__mutmut_29,
    "x_verify_data__mutmut_30": x_verify_data__mutmut_30,
    "x_verify_data__mutmut_31": x_verify_data__mutmut_31,
    "x_verify_data__mutmut_32": x_verify_data__mutmut_32,
    "x_verify_data__mutmut_33": x_verify_data__mutmut_33,
    "x_verify_data__mutmut_34": x_verify_data__mutmut_34,
    "x_verify_data__mutmut_35": x_verify_data__mutmut_35,
    "x_verify_data__mutmut_36": x_verify_data__mutmut_36,
}


def verify_data(*args, **kwargs):
    result = _mutmut_trampoline(x_verify_data__mutmut_orig, x_verify_data__mutmut_mutants, args, kwargs)
    return result


verify_data.__signature__ = _mutmut_signature(x_verify_data__mutmut_orig)
x_verify_data__mutmut_orig.__name__ = "x_verify_data"


def x_calculate_checksums__mutmut_orig(
    path: Path | str,
    algorithms: list[str] | None = None,
) -> dict[str, str]:
    """Calculate multiple checksums for a file.

    Args:
        path: File path
        algorithms: List of algorithms (defaults to sha256 and md5)

    Returns:
        Dictionary mapping algorithm name to hex digest

    Raises:
        ResourceError: If file cannot be read
        ValidationError: If any algorithm is not supported

    """
    if algorithms is None:
        algorithms = ["sha256", "md5"]

    from provide.foundation.crypto.hashing import hash_file_multiple

    checksums = hash_file_multiple(path, algorithms)

    log.debug(
        "📝 Calculated checksums",
        path=str(path),
        algorithms=algorithms,
    )

    return checksums


def x_calculate_checksums__mutmut_1(
    path: Path | str,
    algorithms: list[str] | None = None,
) -> dict[str, str]:
    """Calculate multiple checksums for a file.

    Args:
        path: File path
        algorithms: List of algorithms (defaults to sha256 and md5)

    Returns:
        Dictionary mapping algorithm name to hex digest

    Raises:
        ResourceError: If file cannot be read
        ValidationError: If any algorithm is not supported

    """
    if algorithms is not None:
        algorithms = ["sha256", "md5"]

    from provide.foundation.crypto.hashing import hash_file_multiple

    checksums = hash_file_multiple(path, algorithms)

    log.debug(
        "📝 Calculated checksums",
        path=str(path),
        algorithms=algorithms,
    )

    return checksums


def x_calculate_checksums__mutmut_2(
    path: Path | str,
    algorithms: list[str] | None = None,
) -> dict[str, str]:
    """Calculate multiple checksums for a file.

    Args:
        path: File path
        algorithms: List of algorithms (defaults to sha256 and md5)

    Returns:
        Dictionary mapping algorithm name to hex digest

    Raises:
        ResourceError: If file cannot be read
        ValidationError: If any algorithm is not supported

    """
    if algorithms is None:
        algorithms = None

    from provide.foundation.crypto.hashing import hash_file_multiple

    checksums = hash_file_multiple(path, algorithms)

    log.debug(
        "📝 Calculated checksums",
        path=str(path),
        algorithms=algorithms,
    )

    return checksums


def x_calculate_checksums__mutmut_3(
    path: Path | str,
    algorithms: list[str] | None = None,
) -> dict[str, str]:
    """Calculate multiple checksums for a file.

    Args:
        path: File path
        algorithms: List of algorithms (defaults to sha256 and md5)

    Returns:
        Dictionary mapping algorithm name to hex digest

    Raises:
        ResourceError: If file cannot be read
        ValidationError: If any algorithm is not supported

    """
    if algorithms is None:
        algorithms = ["XXsha256XX", "md5"]

    from provide.foundation.crypto.hashing import hash_file_multiple

    checksums = hash_file_multiple(path, algorithms)

    log.debug(
        "📝 Calculated checksums",
        path=str(path),
        algorithms=algorithms,
    )

    return checksums


def x_calculate_checksums__mutmut_4(
    path: Path | str,
    algorithms: list[str] | None = None,
) -> dict[str, str]:
    """Calculate multiple checksums for a file.

    Args:
        path: File path
        algorithms: List of algorithms (defaults to sha256 and md5)

    Returns:
        Dictionary mapping algorithm name to hex digest

    Raises:
        ResourceError: If file cannot be read
        ValidationError: If any algorithm is not supported

    """
    if algorithms is None:
        algorithms = ["SHA256", "md5"]

    from provide.foundation.crypto.hashing import hash_file_multiple

    checksums = hash_file_multiple(path, algorithms)

    log.debug(
        "📝 Calculated checksums",
        path=str(path),
        algorithms=algorithms,
    )

    return checksums


def x_calculate_checksums__mutmut_5(
    path: Path | str,
    algorithms: list[str] | None = None,
) -> dict[str, str]:
    """Calculate multiple checksums for a file.

    Args:
        path: File path
        algorithms: List of algorithms (defaults to sha256 and md5)

    Returns:
        Dictionary mapping algorithm name to hex digest

    Raises:
        ResourceError: If file cannot be read
        ValidationError: If any algorithm is not supported

    """
    if algorithms is None:
        algorithms = ["sha256", "XXmd5XX"]

    from provide.foundation.crypto.hashing import hash_file_multiple

    checksums = hash_file_multiple(path, algorithms)

    log.debug(
        "📝 Calculated checksums",
        path=str(path),
        algorithms=algorithms,
    )

    return checksums


def x_calculate_checksums__mutmut_6(
    path: Path | str,
    algorithms: list[str] | None = None,
) -> dict[str, str]:
    """Calculate multiple checksums for a file.

    Args:
        path: File path
        algorithms: List of algorithms (defaults to sha256 and md5)

    Returns:
        Dictionary mapping algorithm name to hex digest

    Raises:
        ResourceError: If file cannot be read
        ValidationError: If any algorithm is not supported

    """
    if algorithms is None:
        algorithms = ["sha256", "MD5"]

    from provide.foundation.crypto.hashing import hash_file_multiple

    checksums = hash_file_multiple(path, algorithms)

    log.debug(
        "📝 Calculated checksums",
        path=str(path),
        algorithms=algorithms,
    )

    return checksums


def x_calculate_checksums__mutmut_7(
    path: Path | str,
    algorithms: list[str] | None = None,
) -> dict[str, str]:
    """Calculate multiple checksums for a file.

    Args:
        path: File path
        algorithms: List of algorithms (defaults to sha256 and md5)

    Returns:
        Dictionary mapping algorithm name to hex digest

    Raises:
        ResourceError: If file cannot be read
        ValidationError: If any algorithm is not supported

    """
    if algorithms is None:
        algorithms = ["sha256", "md5"]

    from provide.foundation.crypto.hashing import hash_file_multiple

    checksums = None

    log.debug(
        "📝 Calculated checksums",
        path=str(path),
        algorithms=algorithms,
    )

    return checksums


def x_calculate_checksums__mutmut_8(
    path: Path | str,
    algorithms: list[str] | None = None,
) -> dict[str, str]:
    """Calculate multiple checksums for a file.

    Args:
        path: File path
        algorithms: List of algorithms (defaults to sha256 and md5)

    Returns:
        Dictionary mapping algorithm name to hex digest

    Raises:
        ResourceError: If file cannot be read
        ValidationError: If any algorithm is not supported

    """
    if algorithms is None:
        algorithms = ["sha256", "md5"]

    from provide.foundation.crypto.hashing import hash_file_multiple

    checksums = hash_file_multiple(None, algorithms)

    log.debug(
        "📝 Calculated checksums",
        path=str(path),
        algorithms=algorithms,
    )

    return checksums


def x_calculate_checksums__mutmut_9(
    path: Path | str,
    algorithms: list[str] | None = None,
) -> dict[str, str]:
    """Calculate multiple checksums for a file.

    Args:
        path: File path
        algorithms: List of algorithms (defaults to sha256 and md5)

    Returns:
        Dictionary mapping algorithm name to hex digest

    Raises:
        ResourceError: If file cannot be read
        ValidationError: If any algorithm is not supported

    """
    if algorithms is None:
        algorithms = ["sha256", "md5"]

    from provide.foundation.crypto.hashing import hash_file_multiple

    checksums = hash_file_multiple(path, None)

    log.debug(
        "📝 Calculated checksums",
        path=str(path),
        algorithms=algorithms,
    )

    return checksums


def x_calculate_checksums__mutmut_10(
    path: Path | str,
    algorithms: list[str] | None = None,
) -> dict[str, str]:
    """Calculate multiple checksums for a file.

    Args:
        path: File path
        algorithms: List of algorithms (defaults to sha256 and md5)

    Returns:
        Dictionary mapping algorithm name to hex digest

    Raises:
        ResourceError: If file cannot be read
        ValidationError: If any algorithm is not supported

    """
    if algorithms is None:
        algorithms = ["sha256", "md5"]

    from provide.foundation.crypto.hashing import hash_file_multiple

    checksums = hash_file_multiple(algorithms)

    log.debug(
        "📝 Calculated checksums",
        path=str(path),
        algorithms=algorithms,
    )

    return checksums


def x_calculate_checksums__mutmut_11(
    path: Path | str,
    algorithms: list[str] | None = None,
) -> dict[str, str]:
    """Calculate multiple checksums for a file.

    Args:
        path: File path
        algorithms: List of algorithms (defaults to sha256 and md5)

    Returns:
        Dictionary mapping algorithm name to hex digest

    Raises:
        ResourceError: If file cannot be read
        ValidationError: If any algorithm is not supported

    """
    if algorithms is None:
        algorithms = ["sha256", "md5"]

    from provide.foundation.crypto.hashing import hash_file_multiple

    checksums = hash_file_multiple(
        path,
    )

    log.debug(
        "📝 Calculated checksums",
        path=str(path),
        algorithms=algorithms,
    )

    return checksums


def x_calculate_checksums__mutmut_12(
    path: Path | str,
    algorithms: list[str] | None = None,
) -> dict[str, str]:
    """Calculate multiple checksums for a file.

    Args:
        path: File path
        algorithms: List of algorithms (defaults to sha256 and md5)

    Returns:
        Dictionary mapping algorithm name to hex digest

    Raises:
        ResourceError: If file cannot be read
        ValidationError: If any algorithm is not supported

    """
    if algorithms is None:
        algorithms = ["sha256", "md5"]

    from provide.foundation.crypto.hashing import hash_file_multiple

    checksums = hash_file_multiple(path, algorithms)

    log.debug(
        None,
        path=str(path),
        algorithms=algorithms,
    )

    return checksums


def x_calculate_checksums__mutmut_13(
    path: Path | str,
    algorithms: list[str] | None = None,
) -> dict[str, str]:
    """Calculate multiple checksums for a file.

    Args:
        path: File path
        algorithms: List of algorithms (defaults to sha256 and md5)

    Returns:
        Dictionary mapping algorithm name to hex digest

    Raises:
        ResourceError: If file cannot be read
        ValidationError: If any algorithm is not supported

    """
    if algorithms is None:
        algorithms = ["sha256", "md5"]

    from provide.foundation.crypto.hashing import hash_file_multiple

    checksums = hash_file_multiple(path, algorithms)

    log.debug(
        "📝 Calculated checksums",
        path=None,
        algorithms=algorithms,
    )

    return checksums


def x_calculate_checksums__mutmut_14(
    path: Path | str,
    algorithms: list[str] | None = None,
) -> dict[str, str]:
    """Calculate multiple checksums for a file.

    Args:
        path: File path
        algorithms: List of algorithms (defaults to sha256 and md5)

    Returns:
        Dictionary mapping algorithm name to hex digest

    Raises:
        ResourceError: If file cannot be read
        ValidationError: If any algorithm is not supported

    """
    if algorithms is None:
        algorithms = ["sha256", "md5"]

    from provide.foundation.crypto.hashing import hash_file_multiple

    checksums = hash_file_multiple(path, algorithms)

    log.debug(
        "📝 Calculated checksums",
        path=str(path),
        algorithms=None,
    )

    return checksums


def x_calculate_checksums__mutmut_15(
    path: Path | str,
    algorithms: list[str] | None = None,
) -> dict[str, str]:
    """Calculate multiple checksums for a file.

    Args:
        path: File path
        algorithms: List of algorithms (defaults to sha256 and md5)

    Returns:
        Dictionary mapping algorithm name to hex digest

    Raises:
        ResourceError: If file cannot be read
        ValidationError: If any algorithm is not supported

    """
    if algorithms is None:
        algorithms = ["sha256", "md5"]

    from provide.foundation.crypto.hashing import hash_file_multiple

    checksums = hash_file_multiple(path, algorithms)

    log.debug(
        path=str(path),
        algorithms=algorithms,
    )

    return checksums


def x_calculate_checksums__mutmut_16(
    path: Path | str,
    algorithms: list[str] | None = None,
) -> dict[str, str]:
    """Calculate multiple checksums for a file.

    Args:
        path: File path
        algorithms: List of algorithms (defaults to sha256 and md5)

    Returns:
        Dictionary mapping algorithm name to hex digest

    Raises:
        ResourceError: If file cannot be read
        ValidationError: If any algorithm is not supported

    """
    if algorithms is None:
        algorithms = ["sha256", "md5"]

    from provide.foundation.crypto.hashing import hash_file_multiple

    checksums = hash_file_multiple(path, algorithms)

    log.debug(
        "📝 Calculated checksums",
        algorithms=algorithms,
    )

    return checksums


def x_calculate_checksums__mutmut_17(
    path: Path | str,
    algorithms: list[str] | None = None,
) -> dict[str, str]:
    """Calculate multiple checksums for a file.

    Args:
        path: File path
        algorithms: List of algorithms (defaults to sha256 and md5)

    Returns:
        Dictionary mapping algorithm name to hex digest

    Raises:
        ResourceError: If file cannot be read
        ValidationError: If any algorithm is not supported

    """
    if algorithms is None:
        algorithms = ["sha256", "md5"]

    from provide.foundation.crypto.hashing import hash_file_multiple

    checksums = hash_file_multiple(path, algorithms)

    log.debug(
        "📝 Calculated checksums",
        path=str(path),
    )

    return checksums


def x_calculate_checksums__mutmut_18(
    path: Path | str,
    algorithms: list[str] | None = None,
) -> dict[str, str]:
    """Calculate multiple checksums for a file.

    Args:
        path: File path
        algorithms: List of algorithms (defaults to sha256 and md5)

    Returns:
        Dictionary mapping algorithm name to hex digest

    Raises:
        ResourceError: If file cannot be read
        ValidationError: If any algorithm is not supported

    """
    if algorithms is None:
        algorithms = ["sha256", "md5"]

    from provide.foundation.crypto.hashing import hash_file_multiple

    checksums = hash_file_multiple(path, algorithms)

    log.debug(
        "XX📝 Calculated checksumsXX",
        path=str(path),
        algorithms=algorithms,
    )

    return checksums


def x_calculate_checksums__mutmut_19(
    path: Path | str,
    algorithms: list[str] | None = None,
) -> dict[str, str]:
    """Calculate multiple checksums for a file.

    Args:
        path: File path
        algorithms: List of algorithms (defaults to sha256 and md5)

    Returns:
        Dictionary mapping algorithm name to hex digest

    Raises:
        ResourceError: If file cannot be read
        ValidationError: If any algorithm is not supported

    """
    if algorithms is None:
        algorithms = ["sha256", "md5"]

    from provide.foundation.crypto.hashing import hash_file_multiple

    checksums = hash_file_multiple(path, algorithms)

    log.debug(
        "📝 calculated checksums",
        path=str(path),
        algorithms=algorithms,
    )

    return checksums


def x_calculate_checksums__mutmut_20(
    path: Path | str,
    algorithms: list[str] | None = None,
) -> dict[str, str]:
    """Calculate multiple checksums for a file.

    Args:
        path: File path
        algorithms: List of algorithms (defaults to sha256 and md5)

    Returns:
        Dictionary mapping algorithm name to hex digest

    Raises:
        ResourceError: If file cannot be read
        ValidationError: If any algorithm is not supported

    """
    if algorithms is None:
        algorithms = ["sha256", "md5"]

    from provide.foundation.crypto.hashing import hash_file_multiple

    checksums = hash_file_multiple(path, algorithms)

    log.debug(
        "📝 CALCULATED CHECKSUMS",
        path=str(path),
        algorithms=algorithms,
    )

    return checksums


def x_calculate_checksums__mutmut_21(
    path: Path | str,
    algorithms: list[str] | None = None,
) -> dict[str, str]:
    """Calculate multiple checksums for a file.

    Args:
        path: File path
        algorithms: List of algorithms (defaults to sha256 and md5)

    Returns:
        Dictionary mapping algorithm name to hex digest

    Raises:
        ResourceError: If file cannot be read
        ValidationError: If any algorithm is not supported

    """
    if algorithms is None:
        algorithms = ["sha256", "md5"]

    from provide.foundation.crypto.hashing import hash_file_multiple

    checksums = hash_file_multiple(path, algorithms)

    log.debug(
        "📝 Calculated checksums",
        path=str(None),
        algorithms=algorithms,
    )

    return checksums


x_calculate_checksums__mutmut_mutants: ClassVar[MutantDict] = {
    "x_calculate_checksums__mutmut_1": x_calculate_checksums__mutmut_1,
    "x_calculate_checksums__mutmut_2": x_calculate_checksums__mutmut_2,
    "x_calculate_checksums__mutmut_3": x_calculate_checksums__mutmut_3,
    "x_calculate_checksums__mutmut_4": x_calculate_checksums__mutmut_4,
    "x_calculate_checksums__mutmut_5": x_calculate_checksums__mutmut_5,
    "x_calculate_checksums__mutmut_6": x_calculate_checksums__mutmut_6,
    "x_calculate_checksums__mutmut_7": x_calculate_checksums__mutmut_7,
    "x_calculate_checksums__mutmut_8": x_calculate_checksums__mutmut_8,
    "x_calculate_checksums__mutmut_9": x_calculate_checksums__mutmut_9,
    "x_calculate_checksums__mutmut_10": x_calculate_checksums__mutmut_10,
    "x_calculate_checksums__mutmut_11": x_calculate_checksums__mutmut_11,
    "x_calculate_checksums__mutmut_12": x_calculate_checksums__mutmut_12,
    "x_calculate_checksums__mutmut_13": x_calculate_checksums__mutmut_13,
    "x_calculate_checksums__mutmut_14": x_calculate_checksums__mutmut_14,
    "x_calculate_checksums__mutmut_15": x_calculate_checksums__mutmut_15,
    "x_calculate_checksums__mutmut_16": x_calculate_checksums__mutmut_16,
    "x_calculate_checksums__mutmut_17": x_calculate_checksums__mutmut_17,
    "x_calculate_checksums__mutmut_18": x_calculate_checksums__mutmut_18,
    "x_calculate_checksums__mutmut_19": x_calculate_checksums__mutmut_19,
    "x_calculate_checksums__mutmut_20": x_calculate_checksums__mutmut_20,
    "x_calculate_checksums__mutmut_21": x_calculate_checksums__mutmut_21,
}


def calculate_checksums(*args, **kwargs):
    result = _mutmut_trampoline(
        x_calculate_checksums__mutmut_orig, x_calculate_checksums__mutmut_mutants, args, kwargs
    )
    return result


calculate_checksums.__signature__ = _mutmut_signature(x_calculate_checksums__mutmut_orig)
x_calculate_checksums__mutmut_orig.__name__ = "x_calculate_checksums"


def x_parse_checksum_file__mutmut_orig(
    path: Path | str,
    algorithm: str | None = None,
) -> dict[str, str]:
    """Parse a checksum file and return filename to hash mapping.

    Supports common checksum file formats:
    - SHA256: "hash  filename" or "hash filename"
    - MD5: "hash  filename" or "hash filename"
    - SHA256SUMS: "hash  filename"
    - MD5SUMS: "hash  filename"

    Args:
        path: Path to checksum file
        algorithm: Expected algorithm (for validation)

    Returns:
        Dictionary mapping filename to hash

    Raises:
        ResourceError: If file cannot be read

    """
    if isinstance(path, str):
        path = Path(path)

    if not path.exists():
        raise ResourceError(
            f"Checksum file not found: {path}",
            resource_type="file",
            resource_path=str(path),
        )

    checksums = {}

    try:
        from provide.foundation.file.safe import safe_read_text

        content = safe_read_text(path, default="", encoding="utf-8")

        for line in content.splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            # Split on whitespace (handle both single and double space)
            parts = line.split(None, 1)
            if len(parts) == 2:
                hash_value, filename = parts
                # Remove any leading asterisk (binary mode indicator)
                filename = filename.removeprefix("*")
                checksums[filename] = hash_value.lower()

        log.debug(
            "📄 Parsed checksum file",
            path=str(path),
            entries=len(checksums),
            algorithm=algorithm,
        )

        return checksums

    except OSError as e:
        raise ResourceError(
            f"Failed to read checksum file: {path}",
            resource_type="file",
            resource_path=str(path),
        ) from e


def x_parse_checksum_file__mutmut_1(
    path: Path | str,
    algorithm: str | None = None,
) -> dict[str, str]:
    """Parse a checksum file and return filename to hash mapping.

    Supports common checksum file formats:
    - SHA256: "hash  filename" or "hash filename"
    - MD5: "hash  filename" or "hash filename"
    - SHA256SUMS: "hash  filename"
    - MD5SUMS: "hash  filename"

    Args:
        path: Path to checksum file
        algorithm: Expected algorithm (for validation)

    Returns:
        Dictionary mapping filename to hash

    Raises:
        ResourceError: If file cannot be read

    """
    if isinstance(path, str):
        path = None

    if not path.exists():
        raise ResourceError(
            f"Checksum file not found: {path}",
            resource_type="file",
            resource_path=str(path),
        )

    checksums = {}

    try:
        from provide.foundation.file.safe import safe_read_text

        content = safe_read_text(path, default="", encoding="utf-8")

        for line in content.splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            # Split on whitespace (handle both single and double space)
            parts = line.split(None, 1)
            if len(parts) == 2:
                hash_value, filename = parts
                # Remove any leading asterisk (binary mode indicator)
                filename = filename.removeprefix("*")
                checksums[filename] = hash_value.lower()

        log.debug(
            "📄 Parsed checksum file",
            path=str(path),
            entries=len(checksums),
            algorithm=algorithm,
        )

        return checksums

    except OSError as e:
        raise ResourceError(
            f"Failed to read checksum file: {path}",
            resource_type="file",
            resource_path=str(path),
        ) from e


def x_parse_checksum_file__mutmut_2(
    path: Path | str,
    algorithm: str | None = None,
) -> dict[str, str]:
    """Parse a checksum file and return filename to hash mapping.

    Supports common checksum file formats:
    - SHA256: "hash  filename" or "hash filename"
    - MD5: "hash  filename" or "hash filename"
    - SHA256SUMS: "hash  filename"
    - MD5SUMS: "hash  filename"

    Args:
        path: Path to checksum file
        algorithm: Expected algorithm (for validation)

    Returns:
        Dictionary mapping filename to hash

    Raises:
        ResourceError: If file cannot be read

    """
    if isinstance(path, str):
        path = Path(None)

    if not path.exists():
        raise ResourceError(
            f"Checksum file not found: {path}",
            resource_type="file",
            resource_path=str(path),
        )

    checksums = {}

    try:
        from provide.foundation.file.safe import safe_read_text

        content = safe_read_text(path, default="", encoding="utf-8")

        for line in content.splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            # Split on whitespace (handle both single and double space)
            parts = line.split(None, 1)
            if len(parts) == 2:
                hash_value, filename = parts
                # Remove any leading asterisk (binary mode indicator)
                filename = filename.removeprefix("*")
                checksums[filename] = hash_value.lower()

        log.debug(
            "📄 Parsed checksum file",
            path=str(path),
            entries=len(checksums),
            algorithm=algorithm,
        )

        return checksums

    except OSError as e:
        raise ResourceError(
            f"Failed to read checksum file: {path}",
            resource_type="file",
            resource_path=str(path),
        ) from e


def x_parse_checksum_file__mutmut_3(
    path: Path | str,
    algorithm: str | None = None,
) -> dict[str, str]:
    """Parse a checksum file and return filename to hash mapping.

    Supports common checksum file formats:
    - SHA256: "hash  filename" or "hash filename"
    - MD5: "hash  filename" or "hash filename"
    - SHA256SUMS: "hash  filename"
    - MD5SUMS: "hash  filename"

    Args:
        path: Path to checksum file
        algorithm: Expected algorithm (for validation)

    Returns:
        Dictionary mapping filename to hash

    Raises:
        ResourceError: If file cannot be read

    """
    if isinstance(path, str):
        path = Path(path)

    if path.exists():
        raise ResourceError(
            f"Checksum file not found: {path}",
            resource_type="file",
            resource_path=str(path),
        )

    checksums = {}

    try:
        from provide.foundation.file.safe import safe_read_text

        content = safe_read_text(path, default="", encoding="utf-8")

        for line in content.splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            # Split on whitespace (handle both single and double space)
            parts = line.split(None, 1)
            if len(parts) == 2:
                hash_value, filename = parts
                # Remove any leading asterisk (binary mode indicator)
                filename = filename.removeprefix("*")
                checksums[filename] = hash_value.lower()

        log.debug(
            "📄 Parsed checksum file",
            path=str(path),
            entries=len(checksums),
            algorithm=algorithm,
        )

        return checksums

    except OSError as e:
        raise ResourceError(
            f"Failed to read checksum file: {path}",
            resource_type="file",
            resource_path=str(path),
        ) from e


def x_parse_checksum_file__mutmut_4(
    path: Path | str,
    algorithm: str | None = None,
) -> dict[str, str]:
    """Parse a checksum file and return filename to hash mapping.

    Supports common checksum file formats:
    - SHA256: "hash  filename" or "hash filename"
    - MD5: "hash  filename" or "hash filename"
    - SHA256SUMS: "hash  filename"
    - MD5SUMS: "hash  filename"

    Args:
        path: Path to checksum file
        algorithm: Expected algorithm (for validation)

    Returns:
        Dictionary mapping filename to hash

    Raises:
        ResourceError: If file cannot be read

    """
    if isinstance(path, str):
        path = Path(path)

    if not path.exists():
        raise ResourceError(
            None,
            resource_type="file",
            resource_path=str(path),
        )

    checksums = {}

    try:
        from provide.foundation.file.safe import safe_read_text

        content = safe_read_text(path, default="", encoding="utf-8")

        for line in content.splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            # Split on whitespace (handle both single and double space)
            parts = line.split(None, 1)
            if len(parts) == 2:
                hash_value, filename = parts
                # Remove any leading asterisk (binary mode indicator)
                filename = filename.removeprefix("*")
                checksums[filename] = hash_value.lower()

        log.debug(
            "📄 Parsed checksum file",
            path=str(path),
            entries=len(checksums),
            algorithm=algorithm,
        )

        return checksums

    except OSError as e:
        raise ResourceError(
            f"Failed to read checksum file: {path}",
            resource_type="file",
            resource_path=str(path),
        ) from e


def x_parse_checksum_file__mutmut_5(
    path: Path | str,
    algorithm: str | None = None,
) -> dict[str, str]:
    """Parse a checksum file and return filename to hash mapping.

    Supports common checksum file formats:
    - SHA256: "hash  filename" or "hash filename"
    - MD5: "hash  filename" or "hash filename"
    - SHA256SUMS: "hash  filename"
    - MD5SUMS: "hash  filename"

    Args:
        path: Path to checksum file
        algorithm: Expected algorithm (for validation)

    Returns:
        Dictionary mapping filename to hash

    Raises:
        ResourceError: If file cannot be read

    """
    if isinstance(path, str):
        path = Path(path)

    if not path.exists():
        raise ResourceError(
            f"Checksum file not found: {path}",
            resource_type=None,
            resource_path=str(path),
        )

    checksums = {}

    try:
        from provide.foundation.file.safe import safe_read_text

        content = safe_read_text(path, default="", encoding="utf-8")

        for line in content.splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            # Split on whitespace (handle both single and double space)
            parts = line.split(None, 1)
            if len(parts) == 2:
                hash_value, filename = parts
                # Remove any leading asterisk (binary mode indicator)
                filename = filename.removeprefix("*")
                checksums[filename] = hash_value.lower()

        log.debug(
            "📄 Parsed checksum file",
            path=str(path),
            entries=len(checksums),
            algorithm=algorithm,
        )

        return checksums

    except OSError as e:
        raise ResourceError(
            f"Failed to read checksum file: {path}",
            resource_type="file",
            resource_path=str(path),
        ) from e


def x_parse_checksum_file__mutmut_6(
    path: Path | str,
    algorithm: str | None = None,
) -> dict[str, str]:
    """Parse a checksum file and return filename to hash mapping.

    Supports common checksum file formats:
    - SHA256: "hash  filename" or "hash filename"
    - MD5: "hash  filename" or "hash filename"
    - SHA256SUMS: "hash  filename"
    - MD5SUMS: "hash  filename"

    Args:
        path: Path to checksum file
        algorithm: Expected algorithm (for validation)

    Returns:
        Dictionary mapping filename to hash

    Raises:
        ResourceError: If file cannot be read

    """
    if isinstance(path, str):
        path = Path(path)

    if not path.exists():
        raise ResourceError(
            f"Checksum file not found: {path}",
            resource_type="file",
            resource_path=None,
        )

    checksums = {}

    try:
        from provide.foundation.file.safe import safe_read_text

        content = safe_read_text(path, default="", encoding="utf-8")

        for line in content.splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            # Split on whitespace (handle both single and double space)
            parts = line.split(None, 1)
            if len(parts) == 2:
                hash_value, filename = parts
                # Remove any leading asterisk (binary mode indicator)
                filename = filename.removeprefix("*")
                checksums[filename] = hash_value.lower()

        log.debug(
            "📄 Parsed checksum file",
            path=str(path),
            entries=len(checksums),
            algorithm=algorithm,
        )

        return checksums

    except OSError as e:
        raise ResourceError(
            f"Failed to read checksum file: {path}",
            resource_type="file",
            resource_path=str(path),
        ) from e


def x_parse_checksum_file__mutmut_7(
    path: Path | str,
    algorithm: str | None = None,
) -> dict[str, str]:
    """Parse a checksum file and return filename to hash mapping.

    Supports common checksum file formats:
    - SHA256: "hash  filename" or "hash filename"
    - MD5: "hash  filename" or "hash filename"
    - SHA256SUMS: "hash  filename"
    - MD5SUMS: "hash  filename"

    Args:
        path: Path to checksum file
        algorithm: Expected algorithm (for validation)

    Returns:
        Dictionary mapping filename to hash

    Raises:
        ResourceError: If file cannot be read

    """
    if isinstance(path, str):
        path = Path(path)

    if not path.exists():
        raise ResourceError(
            resource_type="file",
            resource_path=str(path),
        )

    checksums = {}

    try:
        from provide.foundation.file.safe import safe_read_text

        content = safe_read_text(path, default="", encoding="utf-8")

        for line in content.splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            # Split on whitespace (handle both single and double space)
            parts = line.split(None, 1)
            if len(parts) == 2:
                hash_value, filename = parts
                # Remove any leading asterisk (binary mode indicator)
                filename = filename.removeprefix("*")
                checksums[filename] = hash_value.lower()

        log.debug(
            "📄 Parsed checksum file",
            path=str(path),
            entries=len(checksums),
            algorithm=algorithm,
        )

        return checksums

    except OSError as e:
        raise ResourceError(
            f"Failed to read checksum file: {path}",
            resource_type="file",
            resource_path=str(path),
        ) from e


def x_parse_checksum_file__mutmut_8(
    path: Path | str,
    algorithm: str | None = None,
) -> dict[str, str]:
    """Parse a checksum file and return filename to hash mapping.

    Supports common checksum file formats:
    - SHA256: "hash  filename" or "hash filename"
    - MD5: "hash  filename" or "hash filename"
    - SHA256SUMS: "hash  filename"
    - MD5SUMS: "hash  filename"

    Args:
        path: Path to checksum file
        algorithm: Expected algorithm (for validation)

    Returns:
        Dictionary mapping filename to hash

    Raises:
        ResourceError: If file cannot be read

    """
    if isinstance(path, str):
        path = Path(path)

    if not path.exists():
        raise ResourceError(
            f"Checksum file not found: {path}",
            resource_path=str(path),
        )

    checksums = {}

    try:
        from provide.foundation.file.safe import safe_read_text

        content = safe_read_text(path, default="", encoding="utf-8")

        for line in content.splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            # Split on whitespace (handle both single and double space)
            parts = line.split(None, 1)
            if len(parts) == 2:
                hash_value, filename = parts
                # Remove any leading asterisk (binary mode indicator)
                filename = filename.removeprefix("*")
                checksums[filename] = hash_value.lower()

        log.debug(
            "📄 Parsed checksum file",
            path=str(path),
            entries=len(checksums),
            algorithm=algorithm,
        )

        return checksums

    except OSError as e:
        raise ResourceError(
            f"Failed to read checksum file: {path}",
            resource_type="file",
            resource_path=str(path),
        ) from e


def x_parse_checksum_file__mutmut_9(
    path: Path | str,
    algorithm: str | None = None,
) -> dict[str, str]:
    """Parse a checksum file and return filename to hash mapping.

    Supports common checksum file formats:
    - SHA256: "hash  filename" or "hash filename"
    - MD5: "hash  filename" or "hash filename"
    - SHA256SUMS: "hash  filename"
    - MD5SUMS: "hash  filename"

    Args:
        path: Path to checksum file
        algorithm: Expected algorithm (for validation)

    Returns:
        Dictionary mapping filename to hash

    Raises:
        ResourceError: If file cannot be read

    """
    if isinstance(path, str):
        path = Path(path)

    if not path.exists():
        raise ResourceError(
            f"Checksum file not found: {path}",
            resource_type="file",
        )

    checksums = {}

    try:
        from provide.foundation.file.safe import safe_read_text

        content = safe_read_text(path, default="", encoding="utf-8")

        for line in content.splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            # Split on whitespace (handle both single and double space)
            parts = line.split(None, 1)
            if len(parts) == 2:
                hash_value, filename = parts
                # Remove any leading asterisk (binary mode indicator)
                filename = filename.removeprefix("*")
                checksums[filename] = hash_value.lower()

        log.debug(
            "📄 Parsed checksum file",
            path=str(path),
            entries=len(checksums),
            algorithm=algorithm,
        )

        return checksums

    except OSError as e:
        raise ResourceError(
            f"Failed to read checksum file: {path}",
            resource_type="file",
            resource_path=str(path),
        ) from e


def x_parse_checksum_file__mutmut_10(
    path: Path | str,
    algorithm: str | None = None,
) -> dict[str, str]:
    """Parse a checksum file and return filename to hash mapping.

    Supports common checksum file formats:
    - SHA256: "hash  filename" or "hash filename"
    - MD5: "hash  filename" or "hash filename"
    - SHA256SUMS: "hash  filename"
    - MD5SUMS: "hash  filename"

    Args:
        path: Path to checksum file
        algorithm: Expected algorithm (for validation)

    Returns:
        Dictionary mapping filename to hash

    Raises:
        ResourceError: If file cannot be read

    """
    if isinstance(path, str):
        path = Path(path)

    if not path.exists():
        raise ResourceError(
            f"Checksum file not found: {path}",
            resource_type="XXfileXX",
            resource_path=str(path),
        )

    checksums = {}

    try:
        from provide.foundation.file.safe import safe_read_text

        content = safe_read_text(path, default="", encoding="utf-8")

        for line in content.splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            # Split on whitespace (handle both single and double space)
            parts = line.split(None, 1)
            if len(parts) == 2:
                hash_value, filename = parts
                # Remove any leading asterisk (binary mode indicator)
                filename = filename.removeprefix("*")
                checksums[filename] = hash_value.lower()

        log.debug(
            "📄 Parsed checksum file",
            path=str(path),
            entries=len(checksums),
            algorithm=algorithm,
        )

        return checksums

    except OSError as e:
        raise ResourceError(
            f"Failed to read checksum file: {path}",
            resource_type="file",
            resource_path=str(path),
        ) from e


def x_parse_checksum_file__mutmut_11(
    path: Path | str,
    algorithm: str | None = None,
) -> dict[str, str]:
    """Parse a checksum file and return filename to hash mapping.

    Supports common checksum file formats:
    - SHA256: "hash  filename" or "hash filename"
    - MD5: "hash  filename" or "hash filename"
    - SHA256SUMS: "hash  filename"
    - MD5SUMS: "hash  filename"

    Args:
        path: Path to checksum file
        algorithm: Expected algorithm (for validation)

    Returns:
        Dictionary mapping filename to hash

    Raises:
        ResourceError: If file cannot be read

    """
    if isinstance(path, str):
        path = Path(path)

    if not path.exists():
        raise ResourceError(
            f"Checksum file not found: {path}",
            resource_type="FILE",
            resource_path=str(path),
        )

    checksums = {}

    try:
        from provide.foundation.file.safe import safe_read_text

        content = safe_read_text(path, default="", encoding="utf-8")

        for line in content.splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            # Split on whitespace (handle both single and double space)
            parts = line.split(None, 1)
            if len(parts) == 2:
                hash_value, filename = parts
                # Remove any leading asterisk (binary mode indicator)
                filename = filename.removeprefix("*")
                checksums[filename] = hash_value.lower()

        log.debug(
            "📄 Parsed checksum file",
            path=str(path),
            entries=len(checksums),
            algorithm=algorithm,
        )

        return checksums

    except OSError as e:
        raise ResourceError(
            f"Failed to read checksum file: {path}",
            resource_type="file",
            resource_path=str(path),
        ) from e


def x_parse_checksum_file__mutmut_12(
    path: Path | str,
    algorithm: str | None = None,
) -> dict[str, str]:
    """Parse a checksum file and return filename to hash mapping.

    Supports common checksum file formats:
    - SHA256: "hash  filename" or "hash filename"
    - MD5: "hash  filename" or "hash filename"
    - SHA256SUMS: "hash  filename"
    - MD5SUMS: "hash  filename"

    Args:
        path: Path to checksum file
        algorithm: Expected algorithm (for validation)

    Returns:
        Dictionary mapping filename to hash

    Raises:
        ResourceError: If file cannot be read

    """
    if isinstance(path, str):
        path = Path(path)

    if not path.exists():
        raise ResourceError(
            f"Checksum file not found: {path}",
            resource_type="file",
            resource_path=str(None),
        )

    checksums = {}

    try:
        from provide.foundation.file.safe import safe_read_text

        content = safe_read_text(path, default="", encoding="utf-8")

        for line in content.splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            # Split on whitespace (handle both single and double space)
            parts = line.split(None, 1)
            if len(parts) == 2:
                hash_value, filename = parts
                # Remove any leading asterisk (binary mode indicator)
                filename = filename.removeprefix("*")
                checksums[filename] = hash_value.lower()

        log.debug(
            "📄 Parsed checksum file",
            path=str(path),
            entries=len(checksums),
            algorithm=algorithm,
        )

        return checksums

    except OSError as e:
        raise ResourceError(
            f"Failed to read checksum file: {path}",
            resource_type="file",
            resource_path=str(path),
        ) from e


def x_parse_checksum_file__mutmut_13(
    path: Path | str,
    algorithm: str | None = None,
) -> dict[str, str]:
    """Parse a checksum file and return filename to hash mapping.

    Supports common checksum file formats:
    - SHA256: "hash  filename" or "hash filename"
    - MD5: "hash  filename" or "hash filename"
    - SHA256SUMS: "hash  filename"
    - MD5SUMS: "hash  filename"

    Args:
        path: Path to checksum file
        algorithm: Expected algorithm (for validation)

    Returns:
        Dictionary mapping filename to hash

    Raises:
        ResourceError: If file cannot be read

    """
    if isinstance(path, str):
        path = Path(path)

    if not path.exists():
        raise ResourceError(
            f"Checksum file not found: {path}",
            resource_type="file",
            resource_path=str(path),
        )

    checksums = None

    try:
        from provide.foundation.file.safe import safe_read_text

        content = safe_read_text(path, default="", encoding="utf-8")

        for line in content.splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            # Split on whitespace (handle both single and double space)
            parts = line.split(None, 1)
            if len(parts) == 2:
                hash_value, filename = parts
                # Remove any leading asterisk (binary mode indicator)
                filename = filename.removeprefix("*")
                checksums[filename] = hash_value.lower()

        log.debug(
            "📄 Parsed checksum file",
            path=str(path),
            entries=len(checksums),
            algorithm=algorithm,
        )

        return checksums

    except OSError as e:
        raise ResourceError(
            f"Failed to read checksum file: {path}",
            resource_type="file",
            resource_path=str(path),
        ) from e


def x_parse_checksum_file__mutmut_14(
    path: Path | str,
    algorithm: str | None = None,
) -> dict[str, str]:
    """Parse a checksum file and return filename to hash mapping.

    Supports common checksum file formats:
    - SHA256: "hash  filename" or "hash filename"
    - MD5: "hash  filename" or "hash filename"
    - SHA256SUMS: "hash  filename"
    - MD5SUMS: "hash  filename"

    Args:
        path: Path to checksum file
        algorithm: Expected algorithm (for validation)

    Returns:
        Dictionary mapping filename to hash

    Raises:
        ResourceError: If file cannot be read

    """
    if isinstance(path, str):
        path = Path(path)

    if not path.exists():
        raise ResourceError(
            f"Checksum file not found: {path}",
            resource_type="file",
            resource_path=str(path),
        )

    checksums = {}

    try:
        from provide.foundation.file.safe import safe_read_text

        content = None

        for line in content.splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            # Split on whitespace (handle both single and double space)
            parts = line.split(None, 1)
            if len(parts) == 2:
                hash_value, filename = parts
                # Remove any leading asterisk (binary mode indicator)
                filename = filename.removeprefix("*")
                checksums[filename] = hash_value.lower()

        log.debug(
            "📄 Parsed checksum file",
            path=str(path),
            entries=len(checksums),
            algorithm=algorithm,
        )

        return checksums

    except OSError as e:
        raise ResourceError(
            f"Failed to read checksum file: {path}",
            resource_type="file",
            resource_path=str(path),
        ) from e


def x_parse_checksum_file__mutmut_15(
    path: Path | str,
    algorithm: str | None = None,
) -> dict[str, str]:
    """Parse a checksum file and return filename to hash mapping.

    Supports common checksum file formats:
    - SHA256: "hash  filename" or "hash filename"
    - MD5: "hash  filename" or "hash filename"
    - SHA256SUMS: "hash  filename"
    - MD5SUMS: "hash  filename"

    Args:
        path: Path to checksum file
        algorithm: Expected algorithm (for validation)

    Returns:
        Dictionary mapping filename to hash

    Raises:
        ResourceError: If file cannot be read

    """
    if isinstance(path, str):
        path = Path(path)

    if not path.exists():
        raise ResourceError(
            f"Checksum file not found: {path}",
            resource_type="file",
            resource_path=str(path),
        )

    checksums = {}

    try:
        from provide.foundation.file.safe import safe_read_text

        content = safe_read_text(None, default="", encoding="utf-8")

        for line in content.splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            # Split on whitespace (handle both single and double space)
            parts = line.split(None, 1)
            if len(parts) == 2:
                hash_value, filename = parts
                # Remove any leading asterisk (binary mode indicator)
                filename = filename.removeprefix("*")
                checksums[filename] = hash_value.lower()

        log.debug(
            "📄 Parsed checksum file",
            path=str(path),
            entries=len(checksums),
            algorithm=algorithm,
        )

        return checksums

    except OSError as e:
        raise ResourceError(
            f"Failed to read checksum file: {path}",
            resource_type="file",
            resource_path=str(path),
        ) from e


def x_parse_checksum_file__mutmut_16(
    path: Path | str,
    algorithm: str | None = None,
) -> dict[str, str]:
    """Parse a checksum file and return filename to hash mapping.

    Supports common checksum file formats:
    - SHA256: "hash  filename" or "hash filename"
    - MD5: "hash  filename" or "hash filename"
    - SHA256SUMS: "hash  filename"
    - MD5SUMS: "hash  filename"

    Args:
        path: Path to checksum file
        algorithm: Expected algorithm (for validation)

    Returns:
        Dictionary mapping filename to hash

    Raises:
        ResourceError: If file cannot be read

    """
    if isinstance(path, str):
        path = Path(path)

    if not path.exists():
        raise ResourceError(
            f"Checksum file not found: {path}",
            resource_type="file",
            resource_path=str(path),
        )

    checksums = {}

    try:
        from provide.foundation.file.safe import safe_read_text

        content = safe_read_text(path, default=None, encoding="utf-8")

        for line in content.splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            # Split on whitespace (handle both single and double space)
            parts = line.split(None, 1)
            if len(parts) == 2:
                hash_value, filename = parts
                # Remove any leading asterisk (binary mode indicator)
                filename = filename.removeprefix("*")
                checksums[filename] = hash_value.lower()

        log.debug(
            "📄 Parsed checksum file",
            path=str(path),
            entries=len(checksums),
            algorithm=algorithm,
        )

        return checksums

    except OSError as e:
        raise ResourceError(
            f"Failed to read checksum file: {path}",
            resource_type="file",
            resource_path=str(path),
        ) from e


def x_parse_checksum_file__mutmut_17(
    path: Path | str,
    algorithm: str | None = None,
) -> dict[str, str]:
    """Parse a checksum file and return filename to hash mapping.

    Supports common checksum file formats:
    - SHA256: "hash  filename" or "hash filename"
    - MD5: "hash  filename" or "hash filename"
    - SHA256SUMS: "hash  filename"
    - MD5SUMS: "hash  filename"

    Args:
        path: Path to checksum file
        algorithm: Expected algorithm (for validation)

    Returns:
        Dictionary mapping filename to hash

    Raises:
        ResourceError: If file cannot be read

    """
    if isinstance(path, str):
        path = Path(path)

    if not path.exists():
        raise ResourceError(
            f"Checksum file not found: {path}",
            resource_type="file",
            resource_path=str(path),
        )

    checksums = {}

    try:
        from provide.foundation.file.safe import safe_read_text

        content = safe_read_text(path, default="", encoding=None)

        for line in content.splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            # Split on whitespace (handle both single and double space)
            parts = line.split(None, 1)
            if len(parts) == 2:
                hash_value, filename = parts
                # Remove any leading asterisk (binary mode indicator)
                filename = filename.removeprefix("*")
                checksums[filename] = hash_value.lower()

        log.debug(
            "📄 Parsed checksum file",
            path=str(path),
            entries=len(checksums),
            algorithm=algorithm,
        )

        return checksums

    except OSError as e:
        raise ResourceError(
            f"Failed to read checksum file: {path}",
            resource_type="file",
            resource_path=str(path),
        ) from e


def x_parse_checksum_file__mutmut_18(
    path: Path | str,
    algorithm: str | None = None,
) -> dict[str, str]:
    """Parse a checksum file and return filename to hash mapping.

    Supports common checksum file formats:
    - SHA256: "hash  filename" or "hash filename"
    - MD5: "hash  filename" or "hash filename"
    - SHA256SUMS: "hash  filename"
    - MD5SUMS: "hash  filename"

    Args:
        path: Path to checksum file
        algorithm: Expected algorithm (for validation)

    Returns:
        Dictionary mapping filename to hash

    Raises:
        ResourceError: If file cannot be read

    """
    if isinstance(path, str):
        path = Path(path)

    if not path.exists():
        raise ResourceError(
            f"Checksum file not found: {path}",
            resource_type="file",
            resource_path=str(path),
        )

    checksums = {}

    try:
        from provide.foundation.file.safe import safe_read_text

        content = safe_read_text(default="", encoding="utf-8")

        for line in content.splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            # Split on whitespace (handle both single and double space)
            parts = line.split(None, 1)
            if len(parts) == 2:
                hash_value, filename = parts
                # Remove any leading asterisk (binary mode indicator)
                filename = filename.removeprefix("*")
                checksums[filename] = hash_value.lower()

        log.debug(
            "📄 Parsed checksum file",
            path=str(path),
            entries=len(checksums),
            algorithm=algorithm,
        )

        return checksums

    except OSError as e:
        raise ResourceError(
            f"Failed to read checksum file: {path}",
            resource_type="file",
            resource_path=str(path),
        ) from e


def x_parse_checksum_file__mutmut_19(
    path: Path | str,
    algorithm: str | None = None,
) -> dict[str, str]:
    """Parse a checksum file and return filename to hash mapping.

    Supports common checksum file formats:
    - SHA256: "hash  filename" or "hash filename"
    - MD5: "hash  filename" or "hash filename"
    - SHA256SUMS: "hash  filename"
    - MD5SUMS: "hash  filename"

    Args:
        path: Path to checksum file
        algorithm: Expected algorithm (for validation)

    Returns:
        Dictionary mapping filename to hash

    Raises:
        ResourceError: If file cannot be read

    """
    if isinstance(path, str):
        path = Path(path)

    if not path.exists():
        raise ResourceError(
            f"Checksum file not found: {path}",
            resource_type="file",
            resource_path=str(path),
        )

    checksums = {}

    try:
        from provide.foundation.file.safe import safe_read_text

        content = safe_read_text(path, encoding="utf-8")

        for line in content.splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            # Split on whitespace (handle both single and double space)
            parts = line.split(None, 1)
            if len(parts) == 2:
                hash_value, filename = parts
                # Remove any leading asterisk (binary mode indicator)
                filename = filename.removeprefix("*")
                checksums[filename] = hash_value.lower()

        log.debug(
            "📄 Parsed checksum file",
            path=str(path),
            entries=len(checksums),
            algorithm=algorithm,
        )

        return checksums

    except OSError as e:
        raise ResourceError(
            f"Failed to read checksum file: {path}",
            resource_type="file",
            resource_path=str(path),
        ) from e


def x_parse_checksum_file__mutmut_20(
    path: Path | str,
    algorithm: str | None = None,
) -> dict[str, str]:
    """Parse a checksum file and return filename to hash mapping.

    Supports common checksum file formats:
    - SHA256: "hash  filename" or "hash filename"
    - MD5: "hash  filename" or "hash filename"
    - SHA256SUMS: "hash  filename"
    - MD5SUMS: "hash  filename"

    Args:
        path: Path to checksum file
        algorithm: Expected algorithm (for validation)

    Returns:
        Dictionary mapping filename to hash

    Raises:
        ResourceError: If file cannot be read

    """
    if isinstance(path, str):
        path = Path(path)

    if not path.exists():
        raise ResourceError(
            f"Checksum file not found: {path}",
            resource_type="file",
            resource_path=str(path),
        )

    checksums = {}

    try:
        from provide.foundation.file.safe import safe_read_text

        content = safe_read_text(
            path,
            default="",
        )

        for line in content.splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            # Split on whitespace (handle both single and double space)
            parts = line.split(None, 1)
            if len(parts) == 2:
                hash_value, filename = parts
                # Remove any leading asterisk (binary mode indicator)
                filename = filename.removeprefix("*")
                checksums[filename] = hash_value.lower()

        log.debug(
            "📄 Parsed checksum file",
            path=str(path),
            entries=len(checksums),
            algorithm=algorithm,
        )

        return checksums

    except OSError as e:
        raise ResourceError(
            f"Failed to read checksum file: {path}",
            resource_type="file",
            resource_path=str(path),
        ) from e


def x_parse_checksum_file__mutmut_21(
    path: Path | str,
    algorithm: str | None = None,
) -> dict[str, str]:
    """Parse a checksum file and return filename to hash mapping.

    Supports common checksum file formats:
    - SHA256: "hash  filename" or "hash filename"
    - MD5: "hash  filename" or "hash filename"
    - SHA256SUMS: "hash  filename"
    - MD5SUMS: "hash  filename"

    Args:
        path: Path to checksum file
        algorithm: Expected algorithm (for validation)

    Returns:
        Dictionary mapping filename to hash

    Raises:
        ResourceError: If file cannot be read

    """
    if isinstance(path, str):
        path = Path(path)

    if not path.exists():
        raise ResourceError(
            f"Checksum file not found: {path}",
            resource_type="file",
            resource_path=str(path),
        )

    checksums = {}

    try:
        from provide.foundation.file.safe import safe_read_text

        content = safe_read_text(path, default="XXXX", encoding="utf-8")

        for line in content.splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            # Split on whitespace (handle both single and double space)
            parts = line.split(None, 1)
            if len(parts) == 2:
                hash_value, filename = parts
                # Remove any leading asterisk (binary mode indicator)
                filename = filename.removeprefix("*")
                checksums[filename] = hash_value.lower()

        log.debug(
            "📄 Parsed checksum file",
            path=str(path),
            entries=len(checksums),
            algorithm=algorithm,
        )

        return checksums

    except OSError as e:
        raise ResourceError(
            f"Failed to read checksum file: {path}",
            resource_type="file",
            resource_path=str(path),
        ) from e


def x_parse_checksum_file__mutmut_22(
    path: Path | str,
    algorithm: str | None = None,
) -> dict[str, str]:
    """Parse a checksum file and return filename to hash mapping.

    Supports common checksum file formats:
    - SHA256: "hash  filename" or "hash filename"
    - MD5: "hash  filename" or "hash filename"
    - SHA256SUMS: "hash  filename"
    - MD5SUMS: "hash  filename"

    Args:
        path: Path to checksum file
        algorithm: Expected algorithm (for validation)

    Returns:
        Dictionary mapping filename to hash

    Raises:
        ResourceError: If file cannot be read

    """
    if isinstance(path, str):
        path = Path(path)

    if not path.exists():
        raise ResourceError(
            f"Checksum file not found: {path}",
            resource_type="file",
            resource_path=str(path),
        )

    checksums = {}

    try:
        from provide.foundation.file.safe import safe_read_text

        content = safe_read_text(path, default="", encoding="XXutf-8XX")

        for line in content.splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            # Split on whitespace (handle both single and double space)
            parts = line.split(None, 1)
            if len(parts) == 2:
                hash_value, filename = parts
                # Remove any leading asterisk (binary mode indicator)
                filename = filename.removeprefix("*")
                checksums[filename] = hash_value.lower()

        log.debug(
            "📄 Parsed checksum file",
            path=str(path),
            entries=len(checksums),
            algorithm=algorithm,
        )

        return checksums

    except OSError as e:
        raise ResourceError(
            f"Failed to read checksum file: {path}",
            resource_type="file",
            resource_path=str(path),
        ) from e


def x_parse_checksum_file__mutmut_23(
    path: Path | str,
    algorithm: str | None = None,
) -> dict[str, str]:
    """Parse a checksum file and return filename to hash mapping.

    Supports common checksum file formats:
    - SHA256: "hash  filename" or "hash filename"
    - MD5: "hash  filename" or "hash filename"
    - SHA256SUMS: "hash  filename"
    - MD5SUMS: "hash  filename"

    Args:
        path: Path to checksum file
        algorithm: Expected algorithm (for validation)

    Returns:
        Dictionary mapping filename to hash

    Raises:
        ResourceError: If file cannot be read

    """
    if isinstance(path, str):
        path = Path(path)

    if not path.exists():
        raise ResourceError(
            f"Checksum file not found: {path}",
            resource_type="file",
            resource_path=str(path),
        )

    checksums = {}

    try:
        from provide.foundation.file.safe import safe_read_text

        content = safe_read_text(path, default="", encoding="UTF-8")

        for line in content.splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            # Split on whitespace (handle both single and double space)
            parts = line.split(None, 1)
            if len(parts) == 2:
                hash_value, filename = parts
                # Remove any leading asterisk (binary mode indicator)
                filename = filename.removeprefix("*")
                checksums[filename] = hash_value.lower()

        log.debug(
            "📄 Parsed checksum file",
            path=str(path),
            entries=len(checksums),
            algorithm=algorithm,
        )

        return checksums

    except OSError as e:
        raise ResourceError(
            f"Failed to read checksum file: {path}",
            resource_type="file",
            resource_path=str(path),
        ) from e


def x_parse_checksum_file__mutmut_24(
    path: Path | str,
    algorithm: str | None = None,
) -> dict[str, str]:
    """Parse a checksum file and return filename to hash mapping.

    Supports common checksum file formats:
    - SHA256: "hash  filename" or "hash filename"
    - MD5: "hash  filename" or "hash filename"
    - SHA256SUMS: "hash  filename"
    - MD5SUMS: "hash  filename"

    Args:
        path: Path to checksum file
        algorithm: Expected algorithm (for validation)

    Returns:
        Dictionary mapping filename to hash

    Raises:
        ResourceError: If file cannot be read

    """
    if isinstance(path, str):
        path = Path(path)

    if not path.exists():
        raise ResourceError(
            f"Checksum file not found: {path}",
            resource_type="file",
            resource_path=str(path),
        )

    checksums = {}

    try:
        from provide.foundation.file.safe import safe_read_text

        content = safe_read_text(path, default="", encoding="utf-8")

        for line in content.splitlines():
            line = None
            if not line or line.startswith("#"):
                continue

            # Split on whitespace (handle both single and double space)
            parts = line.split(None, 1)
            if len(parts) == 2:
                hash_value, filename = parts
                # Remove any leading asterisk (binary mode indicator)
                filename = filename.removeprefix("*")
                checksums[filename] = hash_value.lower()

        log.debug(
            "📄 Parsed checksum file",
            path=str(path),
            entries=len(checksums),
            algorithm=algorithm,
        )

        return checksums

    except OSError as e:
        raise ResourceError(
            f"Failed to read checksum file: {path}",
            resource_type="file",
            resource_path=str(path),
        ) from e


def x_parse_checksum_file__mutmut_25(
    path: Path | str,
    algorithm: str | None = None,
) -> dict[str, str]:
    """Parse a checksum file and return filename to hash mapping.

    Supports common checksum file formats:
    - SHA256: "hash  filename" or "hash filename"
    - MD5: "hash  filename" or "hash filename"
    - SHA256SUMS: "hash  filename"
    - MD5SUMS: "hash  filename"

    Args:
        path: Path to checksum file
        algorithm: Expected algorithm (for validation)

    Returns:
        Dictionary mapping filename to hash

    Raises:
        ResourceError: If file cannot be read

    """
    if isinstance(path, str):
        path = Path(path)

    if not path.exists():
        raise ResourceError(
            f"Checksum file not found: {path}",
            resource_type="file",
            resource_path=str(path),
        )

    checksums = {}

    try:
        from provide.foundation.file.safe import safe_read_text

        content = safe_read_text(path, default="", encoding="utf-8")

        for line in content.splitlines():
            line = line.strip()
            if not line and line.startswith("#"):
                continue

            # Split on whitespace (handle both single and double space)
            parts = line.split(None, 1)
            if len(parts) == 2:
                hash_value, filename = parts
                # Remove any leading asterisk (binary mode indicator)
                filename = filename.removeprefix("*")
                checksums[filename] = hash_value.lower()

        log.debug(
            "📄 Parsed checksum file",
            path=str(path),
            entries=len(checksums),
            algorithm=algorithm,
        )

        return checksums

    except OSError as e:
        raise ResourceError(
            f"Failed to read checksum file: {path}",
            resource_type="file",
            resource_path=str(path),
        ) from e


def x_parse_checksum_file__mutmut_26(
    path: Path | str,
    algorithm: str | None = None,
) -> dict[str, str]:
    """Parse a checksum file and return filename to hash mapping.

    Supports common checksum file formats:
    - SHA256: "hash  filename" or "hash filename"
    - MD5: "hash  filename" or "hash filename"
    - SHA256SUMS: "hash  filename"
    - MD5SUMS: "hash  filename"

    Args:
        path: Path to checksum file
        algorithm: Expected algorithm (for validation)

    Returns:
        Dictionary mapping filename to hash

    Raises:
        ResourceError: If file cannot be read

    """
    if isinstance(path, str):
        path = Path(path)

    if not path.exists():
        raise ResourceError(
            f"Checksum file not found: {path}",
            resource_type="file",
            resource_path=str(path),
        )

    checksums = {}

    try:
        from provide.foundation.file.safe import safe_read_text

        content = safe_read_text(path, default="", encoding="utf-8")

        for line in content.splitlines():
            line = line.strip()
            if line or line.startswith("#"):
                continue

            # Split on whitespace (handle both single and double space)
            parts = line.split(None, 1)
            if len(parts) == 2:
                hash_value, filename = parts
                # Remove any leading asterisk (binary mode indicator)
                filename = filename.removeprefix("*")
                checksums[filename] = hash_value.lower()

        log.debug(
            "📄 Parsed checksum file",
            path=str(path),
            entries=len(checksums),
            algorithm=algorithm,
        )

        return checksums

    except OSError as e:
        raise ResourceError(
            f"Failed to read checksum file: {path}",
            resource_type="file",
            resource_path=str(path),
        ) from e


def x_parse_checksum_file__mutmut_27(
    path: Path | str,
    algorithm: str | None = None,
) -> dict[str, str]:
    """Parse a checksum file and return filename to hash mapping.

    Supports common checksum file formats:
    - SHA256: "hash  filename" or "hash filename"
    - MD5: "hash  filename" or "hash filename"
    - SHA256SUMS: "hash  filename"
    - MD5SUMS: "hash  filename"

    Args:
        path: Path to checksum file
        algorithm: Expected algorithm (for validation)

    Returns:
        Dictionary mapping filename to hash

    Raises:
        ResourceError: If file cannot be read

    """
    if isinstance(path, str):
        path = Path(path)

    if not path.exists():
        raise ResourceError(
            f"Checksum file not found: {path}",
            resource_type="file",
            resource_path=str(path),
        )

    checksums = {}

    try:
        from provide.foundation.file.safe import safe_read_text

        content = safe_read_text(path, default="", encoding="utf-8")

        for line in content.splitlines():
            line = line.strip()
            if not line or line.startswith(None):
                continue

            # Split on whitespace (handle both single and double space)
            parts = line.split(None, 1)
            if len(parts) == 2:
                hash_value, filename = parts
                # Remove any leading asterisk (binary mode indicator)
                filename = filename.removeprefix("*")
                checksums[filename] = hash_value.lower()

        log.debug(
            "📄 Parsed checksum file",
            path=str(path),
            entries=len(checksums),
            algorithm=algorithm,
        )

        return checksums

    except OSError as e:
        raise ResourceError(
            f"Failed to read checksum file: {path}",
            resource_type="file",
            resource_path=str(path),
        ) from e


def x_parse_checksum_file__mutmut_28(
    path: Path | str,
    algorithm: str | None = None,
) -> dict[str, str]:
    """Parse a checksum file and return filename to hash mapping.

    Supports common checksum file formats:
    - SHA256: "hash  filename" or "hash filename"
    - MD5: "hash  filename" or "hash filename"
    - SHA256SUMS: "hash  filename"
    - MD5SUMS: "hash  filename"

    Args:
        path: Path to checksum file
        algorithm: Expected algorithm (for validation)

    Returns:
        Dictionary mapping filename to hash

    Raises:
        ResourceError: If file cannot be read

    """
    if isinstance(path, str):
        path = Path(path)

    if not path.exists():
        raise ResourceError(
            f"Checksum file not found: {path}",
            resource_type="file",
            resource_path=str(path),
        )

    checksums = {}

    try:
        from provide.foundation.file.safe import safe_read_text

        content = safe_read_text(path, default="", encoding="utf-8")

        for line in content.splitlines():
            line = line.strip()
            if not line or line.startswith("XX#XX"):
                continue

            # Split on whitespace (handle both single and double space)
            parts = line.split(None, 1)
            if len(parts) == 2:
                hash_value, filename = parts
                # Remove any leading asterisk (binary mode indicator)
                filename = filename.removeprefix("*")
                checksums[filename] = hash_value.lower()

        log.debug(
            "📄 Parsed checksum file",
            path=str(path),
            entries=len(checksums),
            algorithm=algorithm,
        )

        return checksums

    except OSError as e:
        raise ResourceError(
            f"Failed to read checksum file: {path}",
            resource_type="file",
            resource_path=str(path),
        ) from e


def x_parse_checksum_file__mutmut_29(
    path: Path | str,
    algorithm: str | None = None,
) -> dict[str, str]:
    """Parse a checksum file and return filename to hash mapping.

    Supports common checksum file formats:
    - SHA256: "hash  filename" or "hash filename"
    - MD5: "hash  filename" or "hash filename"
    - SHA256SUMS: "hash  filename"
    - MD5SUMS: "hash  filename"

    Args:
        path: Path to checksum file
        algorithm: Expected algorithm (for validation)

    Returns:
        Dictionary mapping filename to hash

    Raises:
        ResourceError: If file cannot be read

    """
    if isinstance(path, str):
        path = Path(path)

    if not path.exists():
        raise ResourceError(
            f"Checksum file not found: {path}",
            resource_type="file",
            resource_path=str(path),
        )

    checksums = {}

    try:
        from provide.foundation.file.safe import safe_read_text

        content = safe_read_text(path, default="", encoding="utf-8")

        for line in content.splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                break

            # Split on whitespace (handle both single and double space)
            parts = line.split(None, 1)
            if len(parts) == 2:
                hash_value, filename = parts
                # Remove any leading asterisk (binary mode indicator)
                filename = filename.removeprefix("*")
                checksums[filename] = hash_value.lower()

        log.debug(
            "📄 Parsed checksum file",
            path=str(path),
            entries=len(checksums),
            algorithm=algorithm,
        )

        return checksums

    except OSError as e:
        raise ResourceError(
            f"Failed to read checksum file: {path}",
            resource_type="file",
            resource_path=str(path),
        ) from e


def x_parse_checksum_file__mutmut_30(
    path: Path | str,
    algorithm: str | None = None,
) -> dict[str, str]:
    """Parse a checksum file and return filename to hash mapping.

    Supports common checksum file formats:
    - SHA256: "hash  filename" or "hash filename"
    - MD5: "hash  filename" or "hash filename"
    - SHA256SUMS: "hash  filename"
    - MD5SUMS: "hash  filename"

    Args:
        path: Path to checksum file
        algorithm: Expected algorithm (for validation)

    Returns:
        Dictionary mapping filename to hash

    Raises:
        ResourceError: If file cannot be read

    """
    if isinstance(path, str):
        path = Path(path)

    if not path.exists():
        raise ResourceError(
            f"Checksum file not found: {path}",
            resource_type="file",
            resource_path=str(path),
        )

    checksums = {}

    try:
        from provide.foundation.file.safe import safe_read_text

        content = safe_read_text(path, default="", encoding="utf-8")

        for line in content.splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            # Split on whitespace (handle both single and double space)
            parts = None
            if len(parts) == 2:
                hash_value, filename = parts
                # Remove any leading asterisk (binary mode indicator)
                filename = filename.removeprefix("*")
                checksums[filename] = hash_value.lower()

        log.debug(
            "📄 Parsed checksum file",
            path=str(path),
            entries=len(checksums),
            algorithm=algorithm,
        )

        return checksums

    except OSError as e:
        raise ResourceError(
            f"Failed to read checksum file: {path}",
            resource_type="file",
            resource_path=str(path),
        ) from e


def x_parse_checksum_file__mutmut_31(
    path: Path | str,
    algorithm: str | None = None,
) -> dict[str, str]:
    """Parse a checksum file and return filename to hash mapping.

    Supports common checksum file formats:
    - SHA256: "hash  filename" or "hash filename"
    - MD5: "hash  filename" or "hash filename"
    - SHA256SUMS: "hash  filename"
    - MD5SUMS: "hash  filename"

    Args:
        path: Path to checksum file
        algorithm: Expected algorithm (for validation)

    Returns:
        Dictionary mapping filename to hash

    Raises:
        ResourceError: If file cannot be read

    """
    if isinstance(path, str):
        path = Path(path)

    if not path.exists():
        raise ResourceError(
            f"Checksum file not found: {path}",
            resource_type="file",
            resource_path=str(path),
        )

    checksums = {}

    try:
        from provide.foundation.file.safe import safe_read_text

        content = safe_read_text(path, default="", encoding="utf-8")

        for line in content.splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            # Split on whitespace (handle both single and double space)
            parts = line.split(None, None)
            if len(parts) == 2:
                hash_value, filename = parts
                # Remove any leading asterisk (binary mode indicator)
                filename = filename.removeprefix("*")
                checksums[filename] = hash_value.lower()

        log.debug(
            "📄 Parsed checksum file",
            path=str(path),
            entries=len(checksums),
            algorithm=algorithm,
        )

        return checksums

    except OSError as e:
        raise ResourceError(
            f"Failed to read checksum file: {path}",
            resource_type="file",
            resource_path=str(path),
        ) from e


def x_parse_checksum_file__mutmut_32(
    path: Path | str,
    algorithm: str | None = None,
) -> dict[str, str]:
    """Parse a checksum file and return filename to hash mapping.

    Supports common checksum file formats:
    - SHA256: "hash  filename" or "hash filename"
    - MD5: "hash  filename" or "hash filename"
    - SHA256SUMS: "hash  filename"
    - MD5SUMS: "hash  filename"

    Args:
        path: Path to checksum file
        algorithm: Expected algorithm (for validation)

    Returns:
        Dictionary mapping filename to hash

    Raises:
        ResourceError: If file cannot be read

    """
    if isinstance(path, str):
        path = Path(path)

    if not path.exists():
        raise ResourceError(
            f"Checksum file not found: {path}",
            resource_type="file",
            resource_path=str(path),
        )

    checksums = {}

    try:
        from provide.foundation.file.safe import safe_read_text

        content = safe_read_text(path, default="", encoding="utf-8")

        for line in content.splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            # Split on whitespace (handle both single and double space)
            parts = line.split(1)
            if len(parts) == 2:
                hash_value, filename = parts
                # Remove any leading asterisk (binary mode indicator)
                filename = filename.removeprefix("*")
                checksums[filename] = hash_value.lower()

        log.debug(
            "📄 Parsed checksum file",
            path=str(path),
            entries=len(checksums),
            algorithm=algorithm,
        )

        return checksums

    except OSError as e:
        raise ResourceError(
            f"Failed to read checksum file: {path}",
            resource_type="file",
            resource_path=str(path),
        ) from e


def x_parse_checksum_file__mutmut_33(
    path: Path | str,
    algorithm: str | None = None,
) -> dict[str, str]:
    """Parse a checksum file and return filename to hash mapping.

    Supports common checksum file formats:
    - SHA256: "hash  filename" or "hash filename"
    - MD5: "hash  filename" or "hash filename"
    - SHA256SUMS: "hash  filename"
    - MD5SUMS: "hash  filename"

    Args:
        path: Path to checksum file
        algorithm: Expected algorithm (for validation)

    Returns:
        Dictionary mapping filename to hash

    Raises:
        ResourceError: If file cannot be read

    """
    if isinstance(path, str):
        path = Path(path)

    if not path.exists():
        raise ResourceError(
            f"Checksum file not found: {path}",
            resource_type="file",
            resource_path=str(path),
        )

    checksums = {}

    try:
        from provide.foundation.file.safe import safe_read_text

        content = safe_read_text(path, default="", encoding="utf-8")

        for line in content.splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            # Split on whitespace (handle both single and double space)
            parts = line.split(
                None,
            )
            if len(parts) == 2:
                hash_value, filename = parts
                # Remove any leading asterisk (binary mode indicator)
                filename = filename.removeprefix("*")
                checksums[filename] = hash_value.lower()

        log.debug(
            "📄 Parsed checksum file",
            path=str(path),
            entries=len(checksums),
            algorithm=algorithm,
        )

        return checksums

    except OSError as e:
        raise ResourceError(
            f"Failed to read checksum file: {path}",
            resource_type="file",
            resource_path=str(path),
        ) from e


def x_parse_checksum_file__mutmut_34(
    path: Path | str,
    algorithm: str | None = None,
) -> dict[str, str]:
    """Parse a checksum file and return filename to hash mapping.

    Supports common checksum file formats:
    - SHA256: "hash  filename" or "hash filename"
    - MD5: "hash  filename" or "hash filename"
    - SHA256SUMS: "hash  filename"
    - MD5SUMS: "hash  filename"

    Args:
        path: Path to checksum file
        algorithm: Expected algorithm (for validation)

    Returns:
        Dictionary mapping filename to hash

    Raises:
        ResourceError: If file cannot be read

    """
    if isinstance(path, str):
        path = Path(path)

    if not path.exists():
        raise ResourceError(
            f"Checksum file not found: {path}",
            resource_type="file",
            resource_path=str(path),
        )

    checksums = {}

    try:
        from provide.foundation.file.safe import safe_read_text

        content = safe_read_text(path, default="", encoding="utf-8")

        for line in content.splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            # Split on whitespace (handle both single and double space)
            parts = line.rsplit(None, 1)
            if len(parts) == 2:
                hash_value, filename = parts
                # Remove any leading asterisk (binary mode indicator)
                filename = filename.removeprefix("*")
                checksums[filename] = hash_value.lower()

        log.debug(
            "📄 Parsed checksum file",
            path=str(path),
            entries=len(checksums),
            algorithm=algorithm,
        )

        return checksums

    except OSError as e:
        raise ResourceError(
            f"Failed to read checksum file: {path}",
            resource_type="file",
            resource_path=str(path),
        ) from e


def x_parse_checksum_file__mutmut_35(
    path: Path | str,
    algorithm: str | None = None,
) -> dict[str, str]:
    """Parse a checksum file and return filename to hash mapping.

    Supports common checksum file formats:
    - SHA256: "hash  filename" or "hash filename"
    - MD5: "hash  filename" or "hash filename"
    - SHA256SUMS: "hash  filename"
    - MD5SUMS: "hash  filename"

    Args:
        path: Path to checksum file
        algorithm: Expected algorithm (for validation)

    Returns:
        Dictionary mapping filename to hash

    Raises:
        ResourceError: If file cannot be read

    """
    if isinstance(path, str):
        path = Path(path)

    if not path.exists():
        raise ResourceError(
            f"Checksum file not found: {path}",
            resource_type="file",
            resource_path=str(path),
        )

    checksums = {}

    try:
        from provide.foundation.file.safe import safe_read_text

        content = safe_read_text(path, default="", encoding="utf-8")

        for line in content.splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            # Split on whitespace (handle both single and double space)
            parts = line.split(None, 2)
            if len(parts) == 2:
                hash_value, filename = parts
                # Remove any leading asterisk (binary mode indicator)
                filename = filename.removeprefix("*")
                checksums[filename] = hash_value.lower()

        log.debug(
            "📄 Parsed checksum file",
            path=str(path),
            entries=len(checksums),
            algorithm=algorithm,
        )

        return checksums

    except OSError as e:
        raise ResourceError(
            f"Failed to read checksum file: {path}",
            resource_type="file",
            resource_path=str(path),
        ) from e


def x_parse_checksum_file__mutmut_36(
    path: Path | str,
    algorithm: str | None = None,
) -> dict[str, str]:
    """Parse a checksum file and return filename to hash mapping.

    Supports common checksum file formats:
    - SHA256: "hash  filename" or "hash filename"
    - MD5: "hash  filename" or "hash filename"
    - SHA256SUMS: "hash  filename"
    - MD5SUMS: "hash  filename"

    Args:
        path: Path to checksum file
        algorithm: Expected algorithm (for validation)

    Returns:
        Dictionary mapping filename to hash

    Raises:
        ResourceError: If file cannot be read

    """
    if isinstance(path, str):
        path = Path(path)

    if not path.exists():
        raise ResourceError(
            f"Checksum file not found: {path}",
            resource_type="file",
            resource_path=str(path),
        )

    checksums = {}

    try:
        from provide.foundation.file.safe import safe_read_text

        content = safe_read_text(path, default="", encoding="utf-8")

        for line in content.splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            # Split on whitespace (handle both single and double space)
            parts = line.split(None, 1)
            if len(parts) != 2:
                hash_value, filename = parts
                # Remove any leading asterisk (binary mode indicator)
                filename = filename.removeprefix("*")
                checksums[filename] = hash_value.lower()

        log.debug(
            "📄 Parsed checksum file",
            path=str(path),
            entries=len(checksums),
            algorithm=algorithm,
        )

        return checksums

    except OSError as e:
        raise ResourceError(
            f"Failed to read checksum file: {path}",
            resource_type="file",
            resource_path=str(path),
        ) from e


def x_parse_checksum_file__mutmut_37(
    path: Path | str,
    algorithm: str | None = None,
) -> dict[str, str]:
    """Parse a checksum file and return filename to hash mapping.

    Supports common checksum file formats:
    - SHA256: "hash  filename" or "hash filename"
    - MD5: "hash  filename" or "hash filename"
    - SHA256SUMS: "hash  filename"
    - MD5SUMS: "hash  filename"

    Args:
        path: Path to checksum file
        algorithm: Expected algorithm (for validation)

    Returns:
        Dictionary mapping filename to hash

    Raises:
        ResourceError: If file cannot be read

    """
    if isinstance(path, str):
        path = Path(path)

    if not path.exists():
        raise ResourceError(
            f"Checksum file not found: {path}",
            resource_type="file",
            resource_path=str(path),
        )

    checksums = {}

    try:
        from provide.foundation.file.safe import safe_read_text

        content = safe_read_text(path, default="", encoding="utf-8")

        for line in content.splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            # Split on whitespace (handle both single and double space)
            parts = line.split(None, 1)
            if len(parts) == 3:
                hash_value, filename = parts
                # Remove any leading asterisk (binary mode indicator)
                filename = filename.removeprefix("*")
                checksums[filename] = hash_value.lower()

        log.debug(
            "📄 Parsed checksum file",
            path=str(path),
            entries=len(checksums),
            algorithm=algorithm,
        )

        return checksums

    except OSError as e:
        raise ResourceError(
            f"Failed to read checksum file: {path}",
            resource_type="file",
            resource_path=str(path),
        ) from e


def x_parse_checksum_file__mutmut_38(
    path: Path | str,
    algorithm: str | None = None,
) -> dict[str, str]:
    """Parse a checksum file and return filename to hash mapping.

    Supports common checksum file formats:
    - SHA256: "hash  filename" or "hash filename"
    - MD5: "hash  filename" or "hash filename"
    - SHA256SUMS: "hash  filename"
    - MD5SUMS: "hash  filename"

    Args:
        path: Path to checksum file
        algorithm: Expected algorithm (for validation)

    Returns:
        Dictionary mapping filename to hash

    Raises:
        ResourceError: If file cannot be read

    """
    if isinstance(path, str):
        path = Path(path)

    if not path.exists():
        raise ResourceError(
            f"Checksum file not found: {path}",
            resource_type="file",
            resource_path=str(path),
        )

    checksums = {}

    try:
        from provide.foundation.file.safe import safe_read_text

        content = safe_read_text(path, default="", encoding="utf-8")

        for line in content.splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            # Split on whitespace (handle both single and double space)
            parts = line.split(None, 1)
            if len(parts) == 2:
                hash_value, filename = None
                # Remove any leading asterisk (binary mode indicator)
                filename = filename.removeprefix("*")
                checksums[filename] = hash_value.lower()

        log.debug(
            "📄 Parsed checksum file",
            path=str(path),
            entries=len(checksums),
            algorithm=algorithm,
        )

        return checksums

    except OSError as e:
        raise ResourceError(
            f"Failed to read checksum file: {path}",
            resource_type="file",
            resource_path=str(path),
        ) from e


def x_parse_checksum_file__mutmut_39(
    path: Path | str,
    algorithm: str | None = None,
) -> dict[str, str]:
    """Parse a checksum file and return filename to hash mapping.

    Supports common checksum file formats:
    - SHA256: "hash  filename" or "hash filename"
    - MD5: "hash  filename" or "hash filename"
    - SHA256SUMS: "hash  filename"
    - MD5SUMS: "hash  filename"

    Args:
        path: Path to checksum file
        algorithm: Expected algorithm (for validation)

    Returns:
        Dictionary mapping filename to hash

    Raises:
        ResourceError: If file cannot be read

    """
    if isinstance(path, str):
        path = Path(path)

    if not path.exists():
        raise ResourceError(
            f"Checksum file not found: {path}",
            resource_type="file",
            resource_path=str(path),
        )

    checksums = {}

    try:
        from provide.foundation.file.safe import safe_read_text

        content = safe_read_text(path, default="", encoding="utf-8")

        for line in content.splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            # Split on whitespace (handle both single and double space)
            parts = line.split(None, 1)
            if len(parts) == 2:
                hash_value, filename = parts
                # Remove any leading asterisk (binary mode indicator)
                filename = None
                checksums[filename] = hash_value.lower()

        log.debug(
            "📄 Parsed checksum file",
            path=str(path),
            entries=len(checksums),
            algorithm=algorithm,
        )

        return checksums

    except OSError as e:
        raise ResourceError(
            f"Failed to read checksum file: {path}",
            resource_type="file",
            resource_path=str(path),
        ) from e


def x_parse_checksum_file__mutmut_40(
    path: Path | str,
    algorithm: str | None = None,
) -> dict[str, str]:
    """Parse a checksum file and return filename to hash mapping.

    Supports common checksum file formats:
    - SHA256: "hash  filename" or "hash filename"
    - MD5: "hash  filename" or "hash filename"
    - SHA256SUMS: "hash  filename"
    - MD5SUMS: "hash  filename"

    Args:
        path: Path to checksum file
        algorithm: Expected algorithm (for validation)

    Returns:
        Dictionary mapping filename to hash

    Raises:
        ResourceError: If file cannot be read

    """
    if isinstance(path, str):
        path = Path(path)

    if not path.exists():
        raise ResourceError(
            f"Checksum file not found: {path}",
            resource_type="file",
            resource_path=str(path),
        )

    checksums = {}

    try:
        from provide.foundation.file.safe import safe_read_text

        content = safe_read_text(path, default="", encoding="utf-8")

        for line in content.splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            # Split on whitespace (handle both single and double space)
            parts = line.split(None, 1)
            if len(parts) == 2:
                hash_value, filename = parts
                # Remove any leading asterisk (binary mode indicator)
                filename = filename.removeprefix(None)
                checksums[filename] = hash_value.lower()

        log.debug(
            "📄 Parsed checksum file",
            path=str(path),
            entries=len(checksums),
            algorithm=algorithm,
        )

        return checksums

    except OSError as e:
        raise ResourceError(
            f"Failed to read checksum file: {path}",
            resource_type="file",
            resource_path=str(path),
        ) from e


def x_parse_checksum_file__mutmut_41(
    path: Path | str,
    algorithm: str | None = None,
) -> dict[str, str]:
    """Parse a checksum file and return filename to hash mapping.

    Supports common checksum file formats:
    - SHA256: "hash  filename" or "hash filename"
    - MD5: "hash  filename" or "hash filename"
    - SHA256SUMS: "hash  filename"
    - MD5SUMS: "hash  filename"

    Args:
        path: Path to checksum file
        algorithm: Expected algorithm (for validation)

    Returns:
        Dictionary mapping filename to hash

    Raises:
        ResourceError: If file cannot be read

    """
    if isinstance(path, str):
        path = Path(path)

    if not path.exists():
        raise ResourceError(
            f"Checksum file not found: {path}",
            resource_type="file",
            resource_path=str(path),
        )

    checksums = {}

    try:
        from provide.foundation.file.safe import safe_read_text

        content = safe_read_text(path, default="", encoding="utf-8")

        for line in content.splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            # Split on whitespace (handle both single and double space)
            parts = line.split(None, 1)
            if len(parts) == 2:
                hash_value, filename = parts
                # Remove any leading asterisk (binary mode indicator)
                filename = filename.removesuffix("*")
                checksums[filename] = hash_value.lower()

        log.debug(
            "📄 Parsed checksum file",
            path=str(path),
            entries=len(checksums),
            algorithm=algorithm,
        )

        return checksums

    except OSError as e:
        raise ResourceError(
            f"Failed to read checksum file: {path}",
            resource_type="file",
            resource_path=str(path),
        ) from e


def x_parse_checksum_file__mutmut_42(
    path: Path | str,
    algorithm: str | None = None,
) -> dict[str, str]:
    """Parse a checksum file and return filename to hash mapping.

    Supports common checksum file formats:
    - SHA256: "hash  filename" or "hash filename"
    - MD5: "hash  filename" or "hash filename"
    - SHA256SUMS: "hash  filename"
    - MD5SUMS: "hash  filename"

    Args:
        path: Path to checksum file
        algorithm: Expected algorithm (for validation)

    Returns:
        Dictionary mapping filename to hash

    Raises:
        ResourceError: If file cannot be read

    """
    if isinstance(path, str):
        path = Path(path)

    if not path.exists():
        raise ResourceError(
            f"Checksum file not found: {path}",
            resource_type="file",
            resource_path=str(path),
        )

    checksums = {}

    try:
        from provide.foundation.file.safe import safe_read_text

        content = safe_read_text(path, default="", encoding="utf-8")

        for line in content.splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            # Split on whitespace (handle both single and double space)
            parts = line.split(None, 1)
            if len(parts) == 2:
                hash_value, filename = parts
                # Remove any leading asterisk (binary mode indicator)
                filename = filename.removeprefix("XX*XX")
                checksums[filename] = hash_value.lower()

        log.debug(
            "📄 Parsed checksum file",
            path=str(path),
            entries=len(checksums),
            algorithm=algorithm,
        )

        return checksums

    except OSError as e:
        raise ResourceError(
            f"Failed to read checksum file: {path}",
            resource_type="file",
            resource_path=str(path),
        ) from e


def x_parse_checksum_file__mutmut_43(
    path: Path | str,
    algorithm: str | None = None,
) -> dict[str, str]:
    """Parse a checksum file and return filename to hash mapping.

    Supports common checksum file formats:
    - SHA256: "hash  filename" or "hash filename"
    - MD5: "hash  filename" or "hash filename"
    - SHA256SUMS: "hash  filename"
    - MD5SUMS: "hash  filename"

    Args:
        path: Path to checksum file
        algorithm: Expected algorithm (for validation)

    Returns:
        Dictionary mapping filename to hash

    Raises:
        ResourceError: If file cannot be read

    """
    if isinstance(path, str):
        path = Path(path)

    if not path.exists():
        raise ResourceError(
            f"Checksum file not found: {path}",
            resource_type="file",
            resource_path=str(path),
        )

    checksums = {}

    try:
        from provide.foundation.file.safe import safe_read_text

        content = safe_read_text(path, default="", encoding="utf-8")

        for line in content.splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            # Split on whitespace (handle both single and double space)
            parts = line.split(None, 1)
            if len(parts) == 2:
                hash_value, filename = parts
                # Remove any leading asterisk (binary mode indicator)
                filename = filename.removeprefix("*")
                checksums[filename] = None

        log.debug(
            "📄 Parsed checksum file",
            path=str(path),
            entries=len(checksums),
            algorithm=algorithm,
        )

        return checksums

    except OSError as e:
        raise ResourceError(
            f"Failed to read checksum file: {path}",
            resource_type="file",
            resource_path=str(path),
        ) from e


def x_parse_checksum_file__mutmut_44(
    path: Path | str,
    algorithm: str | None = None,
) -> dict[str, str]:
    """Parse a checksum file and return filename to hash mapping.

    Supports common checksum file formats:
    - SHA256: "hash  filename" or "hash filename"
    - MD5: "hash  filename" or "hash filename"
    - SHA256SUMS: "hash  filename"
    - MD5SUMS: "hash  filename"

    Args:
        path: Path to checksum file
        algorithm: Expected algorithm (for validation)

    Returns:
        Dictionary mapping filename to hash

    Raises:
        ResourceError: If file cannot be read

    """
    if isinstance(path, str):
        path = Path(path)

    if not path.exists():
        raise ResourceError(
            f"Checksum file not found: {path}",
            resource_type="file",
            resource_path=str(path),
        )

    checksums = {}

    try:
        from provide.foundation.file.safe import safe_read_text

        content = safe_read_text(path, default="", encoding="utf-8")

        for line in content.splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            # Split on whitespace (handle both single and double space)
            parts = line.split(None, 1)
            if len(parts) == 2:
                hash_value, filename = parts
                # Remove any leading asterisk (binary mode indicator)
                filename = filename.removeprefix("*")
                checksums[filename] = hash_value.upper()

        log.debug(
            "📄 Parsed checksum file",
            path=str(path),
            entries=len(checksums),
            algorithm=algorithm,
        )

        return checksums

    except OSError as e:
        raise ResourceError(
            f"Failed to read checksum file: {path}",
            resource_type="file",
            resource_path=str(path),
        ) from e


def x_parse_checksum_file__mutmut_45(
    path: Path | str,
    algorithm: str | None = None,
) -> dict[str, str]:
    """Parse a checksum file and return filename to hash mapping.

    Supports common checksum file formats:
    - SHA256: "hash  filename" or "hash filename"
    - MD5: "hash  filename" or "hash filename"
    - SHA256SUMS: "hash  filename"
    - MD5SUMS: "hash  filename"

    Args:
        path: Path to checksum file
        algorithm: Expected algorithm (for validation)

    Returns:
        Dictionary mapping filename to hash

    Raises:
        ResourceError: If file cannot be read

    """
    if isinstance(path, str):
        path = Path(path)

    if not path.exists():
        raise ResourceError(
            f"Checksum file not found: {path}",
            resource_type="file",
            resource_path=str(path),
        )

    checksums = {}

    try:
        from provide.foundation.file.safe import safe_read_text

        content = safe_read_text(path, default="", encoding="utf-8")

        for line in content.splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            # Split on whitespace (handle both single and double space)
            parts = line.split(None, 1)
            if len(parts) == 2:
                hash_value, filename = parts
                # Remove any leading asterisk (binary mode indicator)
                filename = filename.removeprefix("*")
                checksums[filename] = hash_value.lower()

        log.debug(
            None,
            path=str(path),
            entries=len(checksums),
            algorithm=algorithm,
        )

        return checksums

    except OSError as e:
        raise ResourceError(
            f"Failed to read checksum file: {path}",
            resource_type="file",
            resource_path=str(path),
        ) from e


def x_parse_checksum_file__mutmut_46(
    path: Path | str,
    algorithm: str | None = None,
) -> dict[str, str]:
    """Parse a checksum file and return filename to hash mapping.

    Supports common checksum file formats:
    - SHA256: "hash  filename" or "hash filename"
    - MD5: "hash  filename" or "hash filename"
    - SHA256SUMS: "hash  filename"
    - MD5SUMS: "hash  filename"

    Args:
        path: Path to checksum file
        algorithm: Expected algorithm (for validation)

    Returns:
        Dictionary mapping filename to hash

    Raises:
        ResourceError: If file cannot be read

    """
    if isinstance(path, str):
        path = Path(path)

    if not path.exists():
        raise ResourceError(
            f"Checksum file not found: {path}",
            resource_type="file",
            resource_path=str(path),
        )

    checksums = {}

    try:
        from provide.foundation.file.safe import safe_read_text

        content = safe_read_text(path, default="", encoding="utf-8")

        for line in content.splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            # Split on whitespace (handle both single and double space)
            parts = line.split(None, 1)
            if len(parts) == 2:
                hash_value, filename = parts
                # Remove any leading asterisk (binary mode indicator)
                filename = filename.removeprefix("*")
                checksums[filename] = hash_value.lower()

        log.debug(
            "📄 Parsed checksum file",
            path=None,
            entries=len(checksums),
            algorithm=algorithm,
        )

        return checksums

    except OSError as e:
        raise ResourceError(
            f"Failed to read checksum file: {path}",
            resource_type="file",
            resource_path=str(path),
        ) from e


def x_parse_checksum_file__mutmut_47(
    path: Path | str,
    algorithm: str | None = None,
) -> dict[str, str]:
    """Parse a checksum file and return filename to hash mapping.

    Supports common checksum file formats:
    - SHA256: "hash  filename" or "hash filename"
    - MD5: "hash  filename" or "hash filename"
    - SHA256SUMS: "hash  filename"
    - MD5SUMS: "hash  filename"

    Args:
        path: Path to checksum file
        algorithm: Expected algorithm (for validation)

    Returns:
        Dictionary mapping filename to hash

    Raises:
        ResourceError: If file cannot be read

    """
    if isinstance(path, str):
        path = Path(path)

    if not path.exists():
        raise ResourceError(
            f"Checksum file not found: {path}",
            resource_type="file",
            resource_path=str(path),
        )

    checksums = {}

    try:
        from provide.foundation.file.safe import safe_read_text

        content = safe_read_text(path, default="", encoding="utf-8")

        for line in content.splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            # Split on whitespace (handle both single and double space)
            parts = line.split(None, 1)
            if len(parts) == 2:
                hash_value, filename = parts
                # Remove any leading asterisk (binary mode indicator)
                filename = filename.removeprefix("*")
                checksums[filename] = hash_value.lower()

        log.debug(
            "📄 Parsed checksum file",
            path=str(path),
            entries=None,
            algorithm=algorithm,
        )

        return checksums

    except OSError as e:
        raise ResourceError(
            f"Failed to read checksum file: {path}",
            resource_type="file",
            resource_path=str(path),
        ) from e


def x_parse_checksum_file__mutmut_48(
    path: Path | str,
    algorithm: str | None = None,
) -> dict[str, str]:
    """Parse a checksum file and return filename to hash mapping.

    Supports common checksum file formats:
    - SHA256: "hash  filename" or "hash filename"
    - MD5: "hash  filename" or "hash filename"
    - SHA256SUMS: "hash  filename"
    - MD5SUMS: "hash  filename"

    Args:
        path: Path to checksum file
        algorithm: Expected algorithm (for validation)

    Returns:
        Dictionary mapping filename to hash

    Raises:
        ResourceError: If file cannot be read

    """
    if isinstance(path, str):
        path = Path(path)

    if not path.exists():
        raise ResourceError(
            f"Checksum file not found: {path}",
            resource_type="file",
            resource_path=str(path),
        )

    checksums = {}

    try:
        from provide.foundation.file.safe import safe_read_text

        content = safe_read_text(path, default="", encoding="utf-8")

        for line in content.splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            # Split on whitespace (handle both single and double space)
            parts = line.split(None, 1)
            if len(parts) == 2:
                hash_value, filename = parts
                # Remove any leading asterisk (binary mode indicator)
                filename = filename.removeprefix("*")
                checksums[filename] = hash_value.lower()

        log.debug(
            "📄 Parsed checksum file",
            path=str(path),
            entries=len(checksums),
            algorithm=None,
        )

        return checksums

    except OSError as e:
        raise ResourceError(
            f"Failed to read checksum file: {path}",
            resource_type="file",
            resource_path=str(path),
        ) from e


def x_parse_checksum_file__mutmut_49(
    path: Path | str,
    algorithm: str | None = None,
) -> dict[str, str]:
    """Parse a checksum file and return filename to hash mapping.

    Supports common checksum file formats:
    - SHA256: "hash  filename" or "hash filename"
    - MD5: "hash  filename" or "hash filename"
    - SHA256SUMS: "hash  filename"
    - MD5SUMS: "hash  filename"

    Args:
        path: Path to checksum file
        algorithm: Expected algorithm (for validation)

    Returns:
        Dictionary mapping filename to hash

    Raises:
        ResourceError: If file cannot be read

    """
    if isinstance(path, str):
        path = Path(path)

    if not path.exists():
        raise ResourceError(
            f"Checksum file not found: {path}",
            resource_type="file",
            resource_path=str(path),
        )

    checksums = {}

    try:
        from provide.foundation.file.safe import safe_read_text

        content = safe_read_text(path, default="", encoding="utf-8")

        for line in content.splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            # Split on whitespace (handle both single and double space)
            parts = line.split(None, 1)
            if len(parts) == 2:
                hash_value, filename = parts
                # Remove any leading asterisk (binary mode indicator)
                filename = filename.removeprefix("*")
                checksums[filename] = hash_value.lower()

        log.debug(
            path=str(path),
            entries=len(checksums),
            algorithm=algorithm,
        )

        return checksums

    except OSError as e:
        raise ResourceError(
            f"Failed to read checksum file: {path}",
            resource_type="file",
            resource_path=str(path),
        ) from e


def x_parse_checksum_file__mutmut_50(
    path: Path | str,
    algorithm: str | None = None,
) -> dict[str, str]:
    """Parse a checksum file and return filename to hash mapping.

    Supports common checksum file formats:
    - SHA256: "hash  filename" or "hash filename"
    - MD5: "hash  filename" or "hash filename"
    - SHA256SUMS: "hash  filename"
    - MD5SUMS: "hash  filename"

    Args:
        path: Path to checksum file
        algorithm: Expected algorithm (for validation)

    Returns:
        Dictionary mapping filename to hash

    Raises:
        ResourceError: If file cannot be read

    """
    if isinstance(path, str):
        path = Path(path)

    if not path.exists():
        raise ResourceError(
            f"Checksum file not found: {path}",
            resource_type="file",
            resource_path=str(path),
        )

    checksums = {}

    try:
        from provide.foundation.file.safe import safe_read_text

        content = safe_read_text(path, default="", encoding="utf-8")

        for line in content.splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            # Split on whitespace (handle both single and double space)
            parts = line.split(None, 1)
            if len(parts) == 2:
                hash_value, filename = parts
                # Remove any leading asterisk (binary mode indicator)
                filename = filename.removeprefix("*")
                checksums[filename] = hash_value.lower()

        log.debug(
            "📄 Parsed checksum file",
            entries=len(checksums),
            algorithm=algorithm,
        )

        return checksums

    except OSError as e:
        raise ResourceError(
            f"Failed to read checksum file: {path}",
            resource_type="file",
            resource_path=str(path),
        ) from e


def x_parse_checksum_file__mutmut_51(
    path: Path | str,
    algorithm: str | None = None,
) -> dict[str, str]:
    """Parse a checksum file and return filename to hash mapping.

    Supports common checksum file formats:
    - SHA256: "hash  filename" or "hash filename"
    - MD5: "hash  filename" or "hash filename"
    - SHA256SUMS: "hash  filename"
    - MD5SUMS: "hash  filename"

    Args:
        path: Path to checksum file
        algorithm: Expected algorithm (for validation)

    Returns:
        Dictionary mapping filename to hash

    Raises:
        ResourceError: If file cannot be read

    """
    if isinstance(path, str):
        path = Path(path)

    if not path.exists():
        raise ResourceError(
            f"Checksum file not found: {path}",
            resource_type="file",
            resource_path=str(path),
        )

    checksums = {}

    try:
        from provide.foundation.file.safe import safe_read_text

        content = safe_read_text(path, default="", encoding="utf-8")

        for line in content.splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            # Split on whitespace (handle both single and double space)
            parts = line.split(None, 1)
            if len(parts) == 2:
                hash_value, filename = parts
                # Remove any leading asterisk (binary mode indicator)
                filename = filename.removeprefix("*")
                checksums[filename] = hash_value.lower()

        log.debug(
            "📄 Parsed checksum file",
            path=str(path),
            algorithm=algorithm,
        )

        return checksums

    except OSError as e:
        raise ResourceError(
            f"Failed to read checksum file: {path}",
            resource_type="file",
            resource_path=str(path),
        ) from e


def x_parse_checksum_file__mutmut_52(
    path: Path | str,
    algorithm: str | None = None,
) -> dict[str, str]:
    """Parse a checksum file and return filename to hash mapping.

    Supports common checksum file formats:
    - SHA256: "hash  filename" or "hash filename"
    - MD5: "hash  filename" or "hash filename"
    - SHA256SUMS: "hash  filename"
    - MD5SUMS: "hash  filename"

    Args:
        path: Path to checksum file
        algorithm: Expected algorithm (for validation)

    Returns:
        Dictionary mapping filename to hash

    Raises:
        ResourceError: If file cannot be read

    """
    if isinstance(path, str):
        path = Path(path)

    if not path.exists():
        raise ResourceError(
            f"Checksum file not found: {path}",
            resource_type="file",
            resource_path=str(path),
        )

    checksums = {}

    try:
        from provide.foundation.file.safe import safe_read_text

        content = safe_read_text(path, default="", encoding="utf-8")

        for line in content.splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            # Split on whitespace (handle both single and double space)
            parts = line.split(None, 1)
            if len(parts) == 2:
                hash_value, filename = parts
                # Remove any leading asterisk (binary mode indicator)
                filename = filename.removeprefix("*")
                checksums[filename] = hash_value.lower()

        log.debug(
            "📄 Parsed checksum file",
            path=str(path),
            entries=len(checksums),
        )

        return checksums

    except OSError as e:
        raise ResourceError(
            f"Failed to read checksum file: {path}",
            resource_type="file",
            resource_path=str(path),
        ) from e


def x_parse_checksum_file__mutmut_53(
    path: Path | str,
    algorithm: str | None = None,
) -> dict[str, str]:
    """Parse a checksum file and return filename to hash mapping.

    Supports common checksum file formats:
    - SHA256: "hash  filename" or "hash filename"
    - MD5: "hash  filename" or "hash filename"
    - SHA256SUMS: "hash  filename"
    - MD5SUMS: "hash  filename"

    Args:
        path: Path to checksum file
        algorithm: Expected algorithm (for validation)

    Returns:
        Dictionary mapping filename to hash

    Raises:
        ResourceError: If file cannot be read

    """
    if isinstance(path, str):
        path = Path(path)

    if not path.exists():
        raise ResourceError(
            f"Checksum file not found: {path}",
            resource_type="file",
            resource_path=str(path),
        )

    checksums = {}

    try:
        from provide.foundation.file.safe import safe_read_text

        content = safe_read_text(path, default="", encoding="utf-8")

        for line in content.splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            # Split on whitespace (handle both single and double space)
            parts = line.split(None, 1)
            if len(parts) == 2:
                hash_value, filename = parts
                # Remove any leading asterisk (binary mode indicator)
                filename = filename.removeprefix("*")
                checksums[filename] = hash_value.lower()

        log.debug(
            "XX📄 Parsed checksum fileXX",
            path=str(path),
            entries=len(checksums),
            algorithm=algorithm,
        )

        return checksums

    except OSError as e:
        raise ResourceError(
            f"Failed to read checksum file: {path}",
            resource_type="file",
            resource_path=str(path),
        ) from e


def x_parse_checksum_file__mutmut_54(
    path: Path | str,
    algorithm: str | None = None,
) -> dict[str, str]:
    """Parse a checksum file and return filename to hash mapping.

    Supports common checksum file formats:
    - SHA256: "hash  filename" or "hash filename"
    - MD5: "hash  filename" or "hash filename"
    - SHA256SUMS: "hash  filename"
    - MD5SUMS: "hash  filename"

    Args:
        path: Path to checksum file
        algorithm: Expected algorithm (for validation)

    Returns:
        Dictionary mapping filename to hash

    Raises:
        ResourceError: If file cannot be read

    """
    if isinstance(path, str):
        path = Path(path)

    if not path.exists():
        raise ResourceError(
            f"Checksum file not found: {path}",
            resource_type="file",
            resource_path=str(path),
        )

    checksums = {}

    try:
        from provide.foundation.file.safe import safe_read_text

        content = safe_read_text(path, default="", encoding="utf-8")

        for line in content.splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            # Split on whitespace (handle both single and double space)
            parts = line.split(None, 1)
            if len(parts) == 2:
                hash_value, filename = parts
                # Remove any leading asterisk (binary mode indicator)
                filename = filename.removeprefix("*")
                checksums[filename] = hash_value.lower()

        log.debug(
            "📄 parsed checksum file",
            path=str(path),
            entries=len(checksums),
            algorithm=algorithm,
        )

        return checksums

    except OSError as e:
        raise ResourceError(
            f"Failed to read checksum file: {path}",
            resource_type="file",
            resource_path=str(path),
        ) from e


def x_parse_checksum_file__mutmut_55(
    path: Path | str,
    algorithm: str | None = None,
) -> dict[str, str]:
    """Parse a checksum file and return filename to hash mapping.

    Supports common checksum file formats:
    - SHA256: "hash  filename" or "hash filename"
    - MD5: "hash  filename" or "hash filename"
    - SHA256SUMS: "hash  filename"
    - MD5SUMS: "hash  filename"

    Args:
        path: Path to checksum file
        algorithm: Expected algorithm (for validation)

    Returns:
        Dictionary mapping filename to hash

    Raises:
        ResourceError: If file cannot be read

    """
    if isinstance(path, str):
        path = Path(path)

    if not path.exists():
        raise ResourceError(
            f"Checksum file not found: {path}",
            resource_type="file",
            resource_path=str(path),
        )

    checksums = {}

    try:
        from provide.foundation.file.safe import safe_read_text

        content = safe_read_text(path, default="", encoding="utf-8")

        for line in content.splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            # Split on whitespace (handle both single and double space)
            parts = line.split(None, 1)
            if len(parts) == 2:
                hash_value, filename = parts
                # Remove any leading asterisk (binary mode indicator)
                filename = filename.removeprefix("*")
                checksums[filename] = hash_value.lower()

        log.debug(
            "📄 PARSED CHECKSUM FILE",
            path=str(path),
            entries=len(checksums),
            algorithm=algorithm,
        )

        return checksums

    except OSError as e:
        raise ResourceError(
            f"Failed to read checksum file: {path}",
            resource_type="file",
            resource_path=str(path),
        ) from e


def x_parse_checksum_file__mutmut_56(
    path: Path | str,
    algorithm: str | None = None,
) -> dict[str, str]:
    """Parse a checksum file and return filename to hash mapping.

    Supports common checksum file formats:
    - SHA256: "hash  filename" or "hash filename"
    - MD5: "hash  filename" or "hash filename"
    - SHA256SUMS: "hash  filename"
    - MD5SUMS: "hash  filename"

    Args:
        path: Path to checksum file
        algorithm: Expected algorithm (for validation)

    Returns:
        Dictionary mapping filename to hash

    Raises:
        ResourceError: If file cannot be read

    """
    if isinstance(path, str):
        path = Path(path)

    if not path.exists():
        raise ResourceError(
            f"Checksum file not found: {path}",
            resource_type="file",
            resource_path=str(path),
        )

    checksums = {}

    try:
        from provide.foundation.file.safe import safe_read_text

        content = safe_read_text(path, default="", encoding="utf-8")

        for line in content.splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            # Split on whitespace (handle both single and double space)
            parts = line.split(None, 1)
            if len(parts) == 2:
                hash_value, filename = parts
                # Remove any leading asterisk (binary mode indicator)
                filename = filename.removeprefix("*")
                checksums[filename] = hash_value.lower()

        log.debug(
            "📄 Parsed checksum file",
            path=str(None),
            entries=len(checksums),
            algorithm=algorithm,
        )

        return checksums

    except OSError as e:
        raise ResourceError(
            f"Failed to read checksum file: {path}",
            resource_type="file",
            resource_path=str(path),
        ) from e


def x_parse_checksum_file__mutmut_57(
    path: Path | str,
    algorithm: str | None = None,
) -> dict[str, str]:
    """Parse a checksum file and return filename to hash mapping.

    Supports common checksum file formats:
    - SHA256: "hash  filename" or "hash filename"
    - MD5: "hash  filename" or "hash filename"
    - SHA256SUMS: "hash  filename"
    - MD5SUMS: "hash  filename"

    Args:
        path: Path to checksum file
        algorithm: Expected algorithm (for validation)

    Returns:
        Dictionary mapping filename to hash

    Raises:
        ResourceError: If file cannot be read

    """
    if isinstance(path, str):
        path = Path(path)

    if not path.exists():
        raise ResourceError(
            f"Checksum file not found: {path}",
            resource_type="file",
            resource_path=str(path),
        )

    checksums = {}

    try:
        from provide.foundation.file.safe import safe_read_text

        content = safe_read_text(path, default="", encoding="utf-8")

        for line in content.splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            # Split on whitespace (handle both single and double space)
            parts = line.split(None, 1)
            if len(parts) == 2:
                hash_value, filename = parts
                # Remove any leading asterisk (binary mode indicator)
                filename = filename.removeprefix("*")
                checksums[filename] = hash_value.lower()

        log.debug(
            "📄 Parsed checksum file",
            path=str(path),
            entries=len(checksums),
            algorithm=algorithm,
        )

        return checksums

    except OSError as e:
        raise ResourceError(
            None,
            resource_type="file",
            resource_path=str(path),
        ) from e


def x_parse_checksum_file__mutmut_58(
    path: Path | str,
    algorithm: str | None = None,
) -> dict[str, str]:
    """Parse a checksum file and return filename to hash mapping.

    Supports common checksum file formats:
    - SHA256: "hash  filename" or "hash filename"
    - MD5: "hash  filename" or "hash filename"
    - SHA256SUMS: "hash  filename"
    - MD5SUMS: "hash  filename"

    Args:
        path: Path to checksum file
        algorithm: Expected algorithm (for validation)

    Returns:
        Dictionary mapping filename to hash

    Raises:
        ResourceError: If file cannot be read

    """
    if isinstance(path, str):
        path = Path(path)

    if not path.exists():
        raise ResourceError(
            f"Checksum file not found: {path}",
            resource_type="file",
            resource_path=str(path),
        )

    checksums = {}

    try:
        from provide.foundation.file.safe import safe_read_text

        content = safe_read_text(path, default="", encoding="utf-8")

        for line in content.splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            # Split on whitespace (handle both single and double space)
            parts = line.split(None, 1)
            if len(parts) == 2:
                hash_value, filename = parts
                # Remove any leading asterisk (binary mode indicator)
                filename = filename.removeprefix("*")
                checksums[filename] = hash_value.lower()

        log.debug(
            "📄 Parsed checksum file",
            path=str(path),
            entries=len(checksums),
            algorithm=algorithm,
        )

        return checksums

    except OSError as e:
        raise ResourceError(
            f"Failed to read checksum file: {path}",
            resource_type=None,
            resource_path=str(path),
        ) from e


def x_parse_checksum_file__mutmut_59(
    path: Path | str,
    algorithm: str | None = None,
) -> dict[str, str]:
    """Parse a checksum file and return filename to hash mapping.

    Supports common checksum file formats:
    - SHA256: "hash  filename" or "hash filename"
    - MD5: "hash  filename" or "hash filename"
    - SHA256SUMS: "hash  filename"
    - MD5SUMS: "hash  filename"

    Args:
        path: Path to checksum file
        algorithm: Expected algorithm (for validation)

    Returns:
        Dictionary mapping filename to hash

    Raises:
        ResourceError: If file cannot be read

    """
    if isinstance(path, str):
        path = Path(path)

    if not path.exists():
        raise ResourceError(
            f"Checksum file not found: {path}",
            resource_type="file",
            resource_path=str(path),
        )

    checksums = {}

    try:
        from provide.foundation.file.safe import safe_read_text

        content = safe_read_text(path, default="", encoding="utf-8")

        for line in content.splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            # Split on whitespace (handle both single and double space)
            parts = line.split(None, 1)
            if len(parts) == 2:
                hash_value, filename = parts
                # Remove any leading asterisk (binary mode indicator)
                filename = filename.removeprefix("*")
                checksums[filename] = hash_value.lower()

        log.debug(
            "📄 Parsed checksum file",
            path=str(path),
            entries=len(checksums),
            algorithm=algorithm,
        )

        return checksums

    except OSError as e:
        raise ResourceError(
            f"Failed to read checksum file: {path}",
            resource_type="file",
            resource_path=None,
        ) from e


def x_parse_checksum_file__mutmut_60(
    path: Path | str,
    algorithm: str | None = None,
) -> dict[str, str]:
    """Parse a checksum file and return filename to hash mapping.

    Supports common checksum file formats:
    - SHA256: "hash  filename" or "hash filename"
    - MD5: "hash  filename" or "hash filename"
    - SHA256SUMS: "hash  filename"
    - MD5SUMS: "hash  filename"

    Args:
        path: Path to checksum file
        algorithm: Expected algorithm (for validation)

    Returns:
        Dictionary mapping filename to hash

    Raises:
        ResourceError: If file cannot be read

    """
    if isinstance(path, str):
        path = Path(path)

    if not path.exists():
        raise ResourceError(
            f"Checksum file not found: {path}",
            resource_type="file",
            resource_path=str(path),
        )

    checksums = {}

    try:
        from provide.foundation.file.safe import safe_read_text

        content = safe_read_text(path, default="", encoding="utf-8")

        for line in content.splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            # Split on whitespace (handle both single and double space)
            parts = line.split(None, 1)
            if len(parts) == 2:
                hash_value, filename = parts
                # Remove any leading asterisk (binary mode indicator)
                filename = filename.removeprefix("*")
                checksums[filename] = hash_value.lower()

        log.debug(
            "📄 Parsed checksum file",
            path=str(path),
            entries=len(checksums),
            algorithm=algorithm,
        )

        return checksums

    except OSError as e:
        raise ResourceError(
            resource_type="file",
            resource_path=str(path),
        ) from e


def x_parse_checksum_file__mutmut_61(
    path: Path | str,
    algorithm: str | None = None,
) -> dict[str, str]:
    """Parse a checksum file and return filename to hash mapping.

    Supports common checksum file formats:
    - SHA256: "hash  filename" or "hash filename"
    - MD5: "hash  filename" or "hash filename"
    - SHA256SUMS: "hash  filename"
    - MD5SUMS: "hash  filename"

    Args:
        path: Path to checksum file
        algorithm: Expected algorithm (for validation)

    Returns:
        Dictionary mapping filename to hash

    Raises:
        ResourceError: If file cannot be read

    """
    if isinstance(path, str):
        path = Path(path)

    if not path.exists():
        raise ResourceError(
            f"Checksum file not found: {path}",
            resource_type="file",
            resource_path=str(path),
        )

    checksums = {}

    try:
        from provide.foundation.file.safe import safe_read_text

        content = safe_read_text(path, default="", encoding="utf-8")

        for line in content.splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            # Split on whitespace (handle both single and double space)
            parts = line.split(None, 1)
            if len(parts) == 2:
                hash_value, filename = parts
                # Remove any leading asterisk (binary mode indicator)
                filename = filename.removeprefix("*")
                checksums[filename] = hash_value.lower()

        log.debug(
            "📄 Parsed checksum file",
            path=str(path),
            entries=len(checksums),
            algorithm=algorithm,
        )

        return checksums

    except OSError as e:
        raise ResourceError(
            f"Failed to read checksum file: {path}",
            resource_path=str(path),
        ) from e


def x_parse_checksum_file__mutmut_62(
    path: Path | str,
    algorithm: str | None = None,
) -> dict[str, str]:
    """Parse a checksum file and return filename to hash mapping.

    Supports common checksum file formats:
    - SHA256: "hash  filename" or "hash filename"
    - MD5: "hash  filename" or "hash filename"
    - SHA256SUMS: "hash  filename"
    - MD5SUMS: "hash  filename"

    Args:
        path: Path to checksum file
        algorithm: Expected algorithm (for validation)

    Returns:
        Dictionary mapping filename to hash

    Raises:
        ResourceError: If file cannot be read

    """
    if isinstance(path, str):
        path = Path(path)

    if not path.exists():
        raise ResourceError(
            f"Checksum file not found: {path}",
            resource_type="file",
            resource_path=str(path),
        )

    checksums = {}

    try:
        from provide.foundation.file.safe import safe_read_text

        content = safe_read_text(path, default="", encoding="utf-8")

        for line in content.splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            # Split on whitespace (handle both single and double space)
            parts = line.split(None, 1)
            if len(parts) == 2:
                hash_value, filename = parts
                # Remove any leading asterisk (binary mode indicator)
                filename = filename.removeprefix("*")
                checksums[filename] = hash_value.lower()

        log.debug(
            "📄 Parsed checksum file",
            path=str(path),
            entries=len(checksums),
            algorithm=algorithm,
        )

        return checksums

    except OSError as e:
        raise ResourceError(
            f"Failed to read checksum file: {path}",
            resource_type="file",
        ) from e


def x_parse_checksum_file__mutmut_63(
    path: Path | str,
    algorithm: str | None = None,
) -> dict[str, str]:
    """Parse a checksum file and return filename to hash mapping.

    Supports common checksum file formats:
    - SHA256: "hash  filename" or "hash filename"
    - MD5: "hash  filename" or "hash filename"
    - SHA256SUMS: "hash  filename"
    - MD5SUMS: "hash  filename"

    Args:
        path: Path to checksum file
        algorithm: Expected algorithm (for validation)

    Returns:
        Dictionary mapping filename to hash

    Raises:
        ResourceError: If file cannot be read

    """
    if isinstance(path, str):
        path = Path(path)

    if not path.exists():
        raise ResourceError(
            f"Checksum file not found: {path}",
            resource_type="file",
            resource_path=str(path),
        )

    checksums = {}

    try:
        from provide.foundation.file.safe import safe_read_text

        content = safe_read_text(path, default="", encoding="utf-8")

        for line in content.splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            # Split on whitespace (handle both single and double space)
            parts = line.split(None, 1)
            if len(parts) == 2:
                hash_value, filename = parts
                # Remove any leading asterisk (binary mode indicator)
                filename = filename.removeprefix("*")
                checksums[filename] = hash_value.lower()

        log.debug(
            "📄 Parsed checksum file",
            path=str(path),
            entries=len(checksums),
            algorithm=algorithm,
        )

        return checksums

    except OSError as e:
        raise ResourceError(
            f"Failed to read checksum file: {path}",
            resource_type="XXfileXX",
            resource_path=str(path),
        ) from e


def x_parse_checksum_file__mutmut_64(
    path: Path | str,
    algorithm: str | None = None,
) -> dict[str, str]:
    """Parse a checksum file and return filename to hash mapping.

    Supports common checksum file formats:
    - SHA256: "hash  filename" or "hash filename"
    - MD5: "hash  filename" or "hash filename"
    - SHA256SUMS: "hash  filename"
    - MD5SUMS: "hash  filename"

    Args:
        path: Path to checksum file
        algorithm: Expected algorithm (for validation)

    Returns:
        Dictionary mapping filename to hash

    Raises:
        ResourceError: If file cannot be read

    """
    if isinstance(path, str):
        path = Path(path)

    if not path.exists():
        raise ResourceError(
            f"Checksum file not found: {path}",
            resource_type="file",
            resource_path=str(path),
        )

    checksums = {}

    try:
        from provide.foundation.file.safe import safe_read_text

        content = safe_read_text(path, default="", encoding="utf-8")

        for line in content.splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            # Split on whitespace (handle both single and double space)
            parts = line.split(None, 1)
            if len(parts) == 2:
                hash_value, filename = parts
                # Remove any leading asterisk (binary mode indicator)
                filename = filename.removeprefix("*")
                checksums[filename] = hash_value.lower()

        log.debug(
            "📄 Parsed checksum file",
            path=str(path),
            entries=len(checksums),
            algorithm=algorithm,
        )

        return checksums

    except OSError as e:
        raise ResourceError(
            f"Failed to read checksum file: {path}",
            resource_type="FILE",
            resource_path=str(path),
        ) from e


def x_parse_checksum_file__mutmut_65(
    path: Path | str,
    algorithm: str | None = None,
) -> dict[str, str]:
    """Parse a checksum file and return filename to hash mapping.

    Supports common checksum file formats:
    - SHA256: "hash  filename" or "hash filename"
    - MD5: "hash  filename" or "hash filename"
    - SHA256SUMS: "hash  filename"
    - MD5SUMS: "hash  filename"

    Args:
        path: Path to checksum file
        algorithm: Expected algorithm (for validation)

    Returns:
        Dictionary mapping filename to hash

    Raises:
        ResourceError: If file cannot be read

    """
    if isinstance(path, str):
        path = Path(path)

    if not path.exists():
        raise ResourceError(
            f"Checksum file not found: {path}",
            resource_type="file",
            resource_path=str(path),
        )

    checksums = {}

    try:
        from provide.foundation.file.safe import safe_read_text

        content = safe_read_text(path, default="", encoding="utf-8")

        for line in content.splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            # Split on whitespace (handle both single and double space)
            parts = line.split(None, 1)
            if len(parts) == 2:
                hash_value, filename = parts
                # Remove any leading asterisk (binary mode indicator)
                filename = filename.removeprefix("*")
                checksums[filename] = hash_value.lower()

        log.debug(
            "📄 Parsed checksum file",
            path=str(path),
            entries=len(checksums),
            algorithm=algorithm,
        )

        return checksums

    except OSError as e:
        raise ResourceError(
            f"Failed to read checksum file: {path}",
            resource_type="file",
            resource_path=str(None),
        ) from e


x_parse_checksum_file__mutmut_mutants: ClassVar[MutantDict] = {
    "x_parse_checksum_file__mutmut_1": x_parse_checksum_file__mutmut_1,
    "x_parse_checksum_file__mutmut_2": x_parse_checksum_file__mutmut_2,
    "x_parse_checksum_file__mutmut_3": x_parse_checksum_file__mutmut_3,
    "x_parse_checksum_file__mutmut_4": x_parse_checksum_file__mutmut_4,
    "x_parse_checksum_file__mutmut_5": x_parse_checksum_file__mutmut_5,
    "x_parse_checksum_file__mutmut_6": x_parse_checksum_file__mutmut_6,
    "x_parse_checksum_file__mutmut_7": x_parse_checksum_file__mutmut_7,
    "x_parse_checksum_file__mutmut_8": x_parse_checksum_file__mutmut_8,
    "x_parse_checksum_file__mutmut_9": x_parse_checksum_file__mutmut_9,
    "x_parse_checksum_file__mutmut_10": x_parse_checksum_file__mutmut_10,
    "x_parse_checksum_file__mutmut_11": x_parse_checksum_file__mutmut_11,
    "x_parse_checksum_file__mutmut_12": x_parse_checksum_file__mutmut_12,
    "x_parse_checksum_file__mutmut_13": x_parse_checksum_file__mutmut_13,
    "x_parse_checksum_file__mutmut_14": x_parse_checksum_file__mutmut_14,
    "x_parse_checksum_file__mutmut_15": x_parse_checksum_file__mutmut_15,
    "x_parse_checksum_file__mutmut_16": x_parse_checksum_file__mutmut_16,
    "x_parse_checksum_file__mutmut_17": x_parse_checksum_file__mutmut_17,
    "x_parse_checksum_file__mutmut_18": x_parse_checksum_file__mutmut_18,
    "x_parse_checksum_file__mutmut_19": x_parse_checksum_file__mutmut_19,
    "x_parse_checksum_file__mutmut_20": x_parse_checksum_file__mutmut_20,
    "x_parse_checksum_file__mutmut_21": x_parse_checksum_file__mutmut_21,
    "x_parse_checksum_file__mutmut_22": x_parse_checksum_file__mutmut_22,
    "x_parse_checksum_file__mutmut_23": x_parse_checksum_file__mutmut_23,
    "x_parse_checksum_file__mutmut_24": x_parse_checksum_file__mutmut_24,
    "x_parse_checksum_file__mutmut_25": x_parse_checksum_file__mutmut_25,
    "x_parse_checksum_file__mutmut_26": x_parse_checksum_file__mutmut_26,
    "x_parse_checksum_file__mutmut_27": x_parse_checksum_file__mutmut_27,
    "x_parse_checksum_file__mutmut_28": x_parse_checksum_file__mutmut_28,
    "x_parse_checksum_file__mutmut_29": x_parse_checksum_file__mutmut_29,
    "x_parse_checksum_file__mutmut_30": x_parse_checksum_file__mutmut_30,
    "x_parse_checksum_file__mutmut_31": x_parse_checksum_file__mutmut_31,
    "x_parse_checksum_file__mutmut_32": x_parse_checksum_file__mutmut_32,
    "x_parse_checksum_file__mutmut_33": x_parse_checksum_file__mutmut_33,
    "x_parse_checksum_file__mutmut_34": x_parse_checksum_file__mutmut_34,
    "x_parse_checksum_file__mutmut_35": x_parse_checksum_file__mutmut_35,
    "x_parse_checksum_file__mutmut_36": x_parse_checksum_file__mutmut_36,
    "x_parse_checksum_file__mutmut_37": x_parse_checksum_file__mutmut_37,
    "x_parse_checksum_file__mutmut_38": x_parse_checksum_file__mutmut_38,
    "x_parse_checksum_file__mutmut_39": x_parse_checksum_file__mutmut_39,
    "x_parse_checksum_file__mutmut_40": x_parse_checksum_file__mutmut_40,
    "x_parse_checksum_file__mutmut_41": x_parse_checksum_file__mutmut_41,
    "x_parse_checksum_file__mutmut_42": x_parse_checksum_file__mutmut_42,
    "x_parse_checksum_file__mutmut_43": x_parse_checksum_file__mutmut_43,
    "x_parse_checksum_file__mutmut_44": x_parse_checksum_file__mutmut_44,
    "x_parse_checksum_file__mutmut_45": x_parse_checksum_file__mutmut_45,
    "x_parse_checksum_file__mutmut_46": x_parse_checksum_file__mutmut_46,
    "x_parse_checksum_file__mutmut_47": x_parse_checksum_file__mutmut_47,
    "x_parse_checksum_file__mutmut_48": x_parse_checksum_file__mutmut_48,
    "x_parse_checksum_file__mutmut_49": x_parse_checksum_file__mutmut_49,
    "x_parse_checksum_file__mutmut_50": x_parse_checksum_file__mutmut_50,
    "x_parse_checksum_file__mutmut_51": x_parse_checksum_file__mutmut_51,
    "x_parse_checksum_file__mutmut_52": x_parse_checksum_file__mutmut_52,
    "x_parse_checksum_file__mutmut_53": x_parse_checksum_file__mutmut_53,
    "x_parse_checksum_file__mutmut_54": x_parse_checksum_file__mutmut_54,
    "x_parse_checksum_file__mutmut_55": x_parse_checksum_file__mutmut_55,
    "x_parse_checksum_file__mutmut_56": x_parse_checksum_file__mutmut_56,
    "x_parse_checksum_file__mutmut_57": x_parse_checksum_file__mutmut_57,
    "x_parse_checksum_file__mutmut_58": x_parse_checksum_file__mutmut_58,
    "x_parse_checksum_file__mutmut_59": x_parse_checksum_file__mutmut_59,
    "x_parse_checksum_file__mutmut_60": x_parse_checksum_file__mutmut_60,
    "x_parse_checksum_file__mutmut_61": x_parse_checksum_file__mutmut_61,
    "x_parse_checksum_file__mutmut_62": x_parse_checksum_file__mutmut_62,
    "x_parse_checksum_file__mutmut_63": x_parse_checksum_file__mutmut_63,
    "x_parse_checksum_file__mutmut_64": x_parse_checksum_file__mutmut_64,
    "x_parse_checksum_file__mutmut_65": x_parse_checksum_file__mutmut_65,
}


def parse_checksum_file(*args, **kwargs):
    result = _mutmut_trampoline(
        x_parse_checksum_file__mutmut_orig, x_parse_checksum_file__mutmut_mutants, args, kwargs
    )
    return result


parse_checksum_file.__signature__ = _mutmut_signature(x_parse_checksum_file__mutmut_orig)
x_parse_checksum_file__mutmut_orig.__name__ = "x_parse_checksum_file"


def x_write_checksum_file__mutmut_orig(
    checksums: dict[str, str],
    path: Path | str,
    algorithm: str = DEFAULT_ALGORITHM,
    binary_mode: bool = True,
) -> None:
    """Write checksums to a file in standard format.

    Args:
        checksums: Dictionary mapping filename to hash
        path: Path to write checksum file
        algorithm: Algorithm name (for comments)
        binary_mode: Whether to use binary mode indicator (*)

    Raises:
        ResourceError: If file cannot be written

    """
    if isinstance(path, str):
        path = Path(path)

    try:
        from provide.foundation.file.atomic import atomic_write_text

        # Build content
        lines = [
            f"# {algorithm.upper()} checksums",
            "# Generated by provide.foundation",
            "",
        ]

        # Add checksums
        for filename, hash_value in sorted(checksums.items()):
            if binary_mode:
                lines.append(f"{hash_value}  *{filename}")
            else:
                lines.append(f"{hash_value}  {filename}")

        content = "\n".join(lines) + "\n"
        atomic_write_text(path, content, encoding="utf-8")

        log.debug(
            "📝 Wrote checksum file",
            path=str(path),
            entries=len(checksums),
            algorithm=algorithm,
        )

    except OSError as e:
        raise ResourceError(
            f"Failed to write checksum file: {path}",
            resource_type="file",
            resource_path=str(path),
        ) from e


def x_write_checksum_file__mutmut_1(
    checksums: dict[str, str],
    path: Path | str,
    algorithm: str = DEFAULT_ALGORITHM,
    binary_mode: bool = False,
) -> None:
    """Write checksums to a file in standard format.

    Args:
        checksums: Dictionary mapping filename to hash
        path: Path to write checksum file
        algorithm: Algorithm name (for comments)
        binary_mode: Whether to use binary mode indicator (*)

    Raises:
        ResourceError: If file cannot be written

    """
    if isinstance(path, str):
        path = Path(path)

    try:
        from provide.foundation.file.atomic import atomic_write_text

        # Build content
        lines = [
            f"# {algorithm.upper()} checksums",
            "# Generated by provide.foundation",
            "",
        ]

        # Add checksums
        for filename, hash_value in sorted(checksums.items()):
            if binary_mode:
                lines.append(f"{hash_value}  *{filename}")
            else:
                lines.append(f"{hash_value}  {filename}")

        content = "\n".join(lines) + "\n"
        atomic_write_text(path, content, encoding="utf-8")

        log.debug(
            "📝 Wrote checksum file",
            path=str(path),
            entries=len(checksums),
            algorithm=algorithm,
        )

    except OSError as e:
        raise ResourceError(
            f"Failed to write checksum file: {path}",
            resource_type="file",
            resource_path=str(path),
        ) from e


def x_write_checksum_file__mutmut_2(
    checksums: dict[str, str],
    path: Path | str,
    algorithm: str = DEFAULT_ALGORITHM,
    binary_mode: bool = True,
) -> None:
    """Write checksums to a file in standard format.

    Args:
        checksums: Dictionary mapping filename to hash
        path: Path to write checksum file
        algorithm: Algorithm name (for comments)
        binary_mode: Whether to use binary mode indicator (*)

    Raises:
        ResourceError: If file cannot be written

    """
    if isinstance(path, str):
        path = None

    try:
        from provide.foundation.file.atomic import atomic_write_text

        # Build content
        lines = [
            f"# {algorithm.upper()} checksums",
            "# Generated by provide.foundation",
            "",
        ]

        # Add checksums
        for filename, hash_value in sorted(checksums.items()):
            if binary_mode:
                lines.append(f"{hash_value}  *{filename}")
            else:
                lines.append(f"{hash_value}  {filename}")

        content = "\n".join(lines) + "\n"
        atomic_write_text(path, content, encoding="utf-8")

        log.debug(
            "📝 Wrote checksum file",
            path=str(path),
            entries=len(checksums),
            algorithm=algorithm,
        )

    except OSError as e:
        raise ResourceError(
            f"Failed to write checksum file: {path}",
            resource_type="file",
            resource_path=str(path),
        ) from e


def x_write_checksum_file__mutmut_3(
    checksums: dict[str, str],
    path: Path | str,
    algorithm: str = DEFAULT_ALGORITHM,
    binary_mode: bool = True,
) -> None:
    """Write checksums to a file in standard format.

    Args:
        checksums: Dictionary mapping filename to hash
        path: Path to write checksum file
        algorithm: Algorithm name (for comments)
        binary_mode: Whether to use binary mode indicator (*)

    Raises:
        ResourceError: If file cannot be written

    """
    if isinstance(path, str):
        path = Path(None)

    try:
        from provide.foundation.file.atomic import atomic_write_text

        # Build content
        lines = [
            f"# {algorithm.upper()} checksums",
            "# Generated by provide.foundation",
            "",
        ]

        # Add checksums
        for filename, hash_value in sorted(checksums.items()):
            if binary_mode:
                lines.append(f"{hash_value}  *{filename}")
            else:
                lines.append(f"{hash_value}  {filename}")

        content = "\n".join(lines) + "\n"
        atomic_write_text(path, content, encoding="utf-8")

        log.debug(
            "📝 Wrote checksum file",
            path=str(path),
            entries=len(checksums),
            algorithm=algorithm,
        )

    except OSError as e:
        raise ResourceError(
            f"Failed to write checksum file: {path}",
            resource_type="file",
            resource_path=str(path),
        ) from e


def x_write_checksum_file__mutmut_4(
    checksums: dict[str, str],
    path: Path | str,
    algorithm: str = DEFAULT_ALGORITHM,
    binary_mode: bool = True,
) -> None:
    """Write checksums to a file in standard format.

    Args:
        checksums: Dictionary mapping filename to hash
        path: Path to write checksum file
        algorithm: Algorithm name (for comments)
        binary_mode: Whether to use binary mode indicator (*)

    Raises:
        ResourceError: If file cannot be written

    """
    if isinstance(path, str):
        path = Path(path)

    try:
        from provide.foundation.file.atomic import atomic_write_text

        # Build content
        lines = None

        # Add checksums
        for filename, hash_value in sorted(checksums.items()):
            if binary_mode:
                lines.append(f"{hash_value}  *{filename}")
            else:
                lines.append(f"{hash_value}  {filename}")

        content = "\n".join(lines) + "\n"
        atomic_write_text(path, content, encoding="utf-8")

        log.debug(
            "📝 Wrote checksum file",
            path=str(path),
            entries=len(checksums),
            algorithm=algorithm,
        )

    except OSError as e:
        raise ResourceError(
            f"Failed to write checksum file: {path}",
            resource_type="file",
            resource_path=str(path),
        ) from e


def x_write_checksum_file__mutmut_5(
    checksums: dict[str, str],
    path: Path | str,
    algorithm: str = DEFAULT_ALGORITHM,
    binary_mode: bool = True,
) -> None:
    """Write checksums to a file in standard format.

    Args:
        checksums: Dictionary mapping filename to hash
        path: Path to write checksum file
        algorithm: Algorithm name (for comments)
        binary_mode: Whether to use binary mode indicator (*)

    Raises:
        ResourceError: If file cannot be written

    """
    if isinstance(path, str):
        path = Path(path)

    try:
        from provide.foundation.file.atomic import atomic_write_text

        # Build content
        lines = [
            f"# {algorithm.lower()} checksums",
            "# Generated by provide.foundation",
            "",
        ]

        # Add checksums
        for filename, hash_value in sorted(checksums.items()):
            if binary_mode:
                lines.append(f"{hash_value}  *{filename}")
            else:
                lines.append(f"{hash_value}  {filename}")

        content = "\n".join(lines) + "\n"
        atomic_write_text(path, content, encoding="utf-8")

        log.debug(
            "📝 Wrote checksum file",
            path=str(path),
            entries=len(checksums),
            algorithm=algorithm,
        )

    except OSError as e:
        raise ResourceError(
            f"Failed to write checksum file: {path}",
            resource_type="file",
            resource_path=str(path),
        ) from e


def x_write_checksum_file__mutmut_6(
    checksums: dict[str, str],
    path: Path | str,
    algorithm: str = DEFAULT_ALGORITHM,
    binary_mode: bool = True,
) -> None:
    """Write checksums to a file in standard format.

    Args:
        checksums: Dictionary mapping filename to hash
        path: Path to write checksum file
        algorithm: Algorithm name (for comments)
        binary_mode: Whether to use binary mode indicator (*)

    Raises:
        ResourceError: If file cannot be written

    """
    if isinstance(path, str):
        path = Path(path)

    try:
        from provide.foundation.file.atomic import atomic_write_text

        # Build content
        lines = [
            f"# {algorithm.upper()} checksums",
            "XX# Generated by provide.foundationXX",
            "",
        ]

        # Add checksums
        for filename, hash_value in sorted(checksums.items()):
            if binary_mode:
                lines.append(f"{hash_value}  *{filename}")
            else:
                lines.append(f"{hash_value}  {filename}")

        content = "\n".join(lines) + "\n"
        atomic_write_text(path, content, encoding="utf-8")

        log.debug(
            "📝 Wrote checksum file",
            path=str(path),
            entries=len(checksums),
            algorithm=algorithm,
        )

    except OSError as e:
        raise ResourceError(
            f"Failed to write checksum file: {path}",
            resource_type="file",
            resource_path=str(path),
        ) from e


def x_write_checksum_file__mutmut_7(
    checksums: dict[str, str],
    path: Path | str,
    algorithm: str = DEFAULT_ALGORITHM,
    binary_mode: bool = True,
) -> None:
    """Write checksums to a file in standard format.

    Args:
        checksums: Dictionary mapping filename to hash
        path: Path to write checksum file
        algorithm: Algorithm name (for comments)
        binary_mode: Whether to use binary mode indicator (*)

    Raises:
        ResourceError: If file cannot be written

    """
    if isinstance(path, str):
        path = Path(path)

    try:
        from provide.foundation.file.atomic import atomic_write_text

        # Build content
        lines = [
            f"# {algorithm.upper()} checksums",
            "# generated by provide.foundation",
            "",
        ]

        # Add checksums
        for filename, hash_value in sorted(checksums.items()):
            if binary_mode:
                lines.append(f"{hash_value}  *{filename}")
            else:
                lines.append(f"{hash_value}  {filename}")

        content = "\n".join(lines) + "\n"
        atomic_write_text(path, content, encoding="utf-8")

        log.debug(
            "📝 Wrote checksum file",
            path=str(path),
            entries=len(checksums),
            algorithm=algorithm,
        )

    except OSError as e:
        raise ResourceError(
            f"Failed to write checksum file: {path}",
            resource_type="file",
            resource_path=str(path),
        ) from e


def x_write_checksum_file__mutmut_8(
    checksums: dict[str, str],
    path: Path | str,
    algorithm: str = DEFAULT_ALGORITHM,
    binary_mode: bool = True,
) -> None:
    """Write checksums to a file in standard format.

    Args:
        checksums: Dictionary mapping filename to hash
        path: Path to write checksum file
        algorithm: Algorithm name (for comments)
        binary_mode: Whether to use binary mode indicator (*)

    Raises:
        ResourceError: If file cannot be written

    """
    if isinstance(path, str):
        path = Path(path)

    try:
        from provide.foundation.file.atomic import atomic_write_text

        # Build content
        lines = [
            f"# {algorithm.upper()} checksums",
            "# GENERATED BY PROVIDE.FOUNDATION",
            "",
        ]

        # Add checksums
        for filename, hash_value in sorted(checksums.items()):
            if binary_mode:
                lines.append(f"{hash_value}  *{filename}")
            else:
                lines.append(f"{hash_value}  {filename}")

        content = "\n".join(lines) + "\n"
        atomic_write_text(path, content, encoding="utf-8")

        log.debug(
            "📝 Wrote checksum file",
            path=str(path),
            entries=len(checksums),
            algorithm=algorithm,
        )

    except OSError as e:
        raise ResourceError(
            f"Failed to write checksum file: {path}",
            resource_type="file",
            resource_path=str(path),
        ) from e


def x_write_checksum_file__mutmut_9(
    checksums: dict[str, str],
    path: Path | str,
    algorithm: str = DEFAULT_ALGORITHM,
    binary_mode: bool = True,
) -> None:
    """Write checksums to a file in standard format.

    Args:
        checksums: Dictionary mapping filename to hash
        path: Path to write checksum file
        algorithm: Algorithm name (for comments)
        binary_mode: Whether to use binary mode indicator (*)

    Raises:
        ResourceError: If file cannot be written

    """
    if isinstance(path, str):
        path = Path(path)

    try:
        from provide.foundation.file.atomic import atomic_write_text

        # Build content
        lines = [
            f"# {algorithm.upper()} checksums",
            "# Generated by provide.foundation",
            "XXXX",
        ]

        # Add checksums
        for filename, hash_value in sorted(checksums.items()):
            if binary_mode:
                lines.append(f"{hash_value}  *{filename}")
            else:
                lines.append(f"{hash_value}  {filename}")

        content = "\n".join(lines) + "\n"
        atomic_write_text(path, content, encoding="utf-8")

        log.debug(
            "📝 Wrote checksum file",
            path=str(path),
            entries=len(checksums),
            algorithm=algorithm,
        )

    except OSError as e:
        raise ResourceError(
            f"Failed to write checksum file: {path}",
            resource_type="file",
            resource_path=str(path),
        ) from e


def x_write_checksum_file__mutmut_10(
    checksums: dict[str, str],
    path: Path | str,
    algorithm: str = DEFAULT_ALGORITHM,
    binary_mode: bool = True,
) -> None:
    """Write checksums to a file in standard format.

    Args:
        checksums: Dictionary mapping filename to hash
        path: Path to write checksum file
        algorithm: Algorithm name (for comments)
        binary_mode: Whether to use binary mode indicator (*)

    Raises:
        ResourceError: If file cannot be written

    """
    if isinstance(path, str):
        path = Path(path)

    try:
        from provide.foundation.file.atomic import atomic_write_text

        # Build content
        lines = [
            f"# {algorithm.upper()} checksums",
            "# Generated by provide.foundation",
            "",
        ]

        # Add checksums
        for filename, hash_value in sorted(None):
            if binary_mode:
                lines.append(f"{hash_value}  *{filename}")
            else:
                lines.append(f"{hash_value}  {filename}")

        content = "\n".join(lines) + "\n"
        atomic_write_text(path, content, encoding="utf-8")

        log.debug(
            "📝 Wrote checksum file",
            path=str(path),
            entries=len(checksums),
            algorithm=algorithm,
        )

    except OSError as e:
        raise ResourceError(
            f"Failed to write checksum file: {path}",
            resource_type="file",
            resource_path=str(path),
        ) from e


def x_write_checksum_file__mutmut_11(
    checksums: dict[str, str],
    path: Path | str,
    algorithm: str = DEFAULT_ALGORITHM,
    binary_mode: bool = True,
) -> None:
    """Write checksums to a file in standard format.

    Args:
        checksums: Dictionary mapping filename to hash
        path: Path to write checksum file
        algorithm: Algorithm name (for comments)
        binary_mode: Whether to use binary mode indicator (*)

    Raises:
        ResourceError: If file cannot be written

    """
    if isinstance(path, str):
        path = Path(path)

    try:
        from provide.foundation.file.atomic import atomic_write_text

        # Build content
        lines = [
            f"# {algorithm.upper()} checksums",
            "# Generated by provide.foundation",
            "",
        ]

        # Add checksums
        for filename, hash_value in sorted(checksums.items()):
            if binary_mode:
                lines.append(None)
            else:
                lines.append(f"{hash_value}  {filename}")

        content = "\n".join(lines) + "\n"
        atomic_write_text(path, content, encoding="utf-8")

        log.debug(
            "📝 Wrote checksum file",
            path=str(path),
            entries=len(checksums),
            algorithm=algorithm,
        )

    except OSError as e:
        raise ResourceError(
            f"Failed to write checksum file: {path}",
            resource_type="file",
            resource_path=str(path),
        ) from e


def x_write_checksum_file__mutmut_12(
    checksums: dict[str, str],
    path: Path | str,
    algorithm: str = DEFAULT_ALGORITHM,
    binary_mode: bool = True,
) -> None:
    """Write checksums to a file in standard format.

    Args:
        checksums: Dictionary mapping filename to hash
        path: Path to write checksum file
        algorithm: Algorithm name (for comments)
        binary_mode: Whether to use binary mode indicator (*)

    Raises:
        ResourceError: If file cannot be written

    """
    if isinstance(path, str):
        path = Path(path)

    try:
        from provide.foundation.file.atomic import atomic_write_text

        # Build content
        lines = [
            f"# {algorithm.upper()} checksums",
            "# Generated by provide.foundation",
            "",
        ]

        # Add checksums
        for filename, hash_value in sorted(checksums.items()):
            if binary_mode:
                lines.append(f"{hash_value}  *{filename}")
            else:
                lines.append(None)

        content = "\n".join(lines) + "\n"
        atomic_write_text(path, content, encoding="utf-8")

        log.debug(
            "📝 Wrote checksum file",
            path=str(path),
            entries=len(checksums),
            algorithm=algorithm,
        )

    except OSError as e:
        raise ResourceError(
            f"Failed to write checksum file: {path}",
            resource_type="file",
            resource_path=str(path),
        ) from e


def x_write_checksum_file__mutmut_13(
    checksums: dict[str, str],
    path: Path | str,
    algorithm: str = DEFAULT_ALGORITHM,
    binary_mode: bool = True,
) -> None:
    """Write checksums to a file in standard format.

    Args:
        checksums: Dictionary mapping filename to hash
        path: Path to write checksum file
        algorithm: Algorithm name (for comments)
        binary_mode: Whether to use binary mode indicator (*)

    Raises:
        ResourceError: If file cannot be written

    """
    if isinstance(path, str):
        path = Path(path)

    try:
        from provide.foundation.file.atomic import atomic_write_text

        # Build content
        lines = [
            f"# {algorithm.upper()} checksums",
            "# Generated by provide.foundation",
            "",
        ]

        # Add checksums
        for filename, hash_value in sorted(checksums.items()):
            if binary_mode:
                lines.append(f"{hash_value}  *{filename}")
            else:
                lines.append(f"{hash_value}  {filename}")

        content = None
        atomic_write_text(path, content, encoding="utf-8")

        log.debug(
            "📝 Wrote checksum file",
            path=str(path),
            entries=len(checksums),
            algorithm=algorithm,
        )

    except OSError as e:
        raise ResourceError(
            f"Failed to write checksum file: {path}",
            resource_type="file",
            resource_path=str(path),
        ) from e


def x_write_checksum_file__mutmut_14(
    checksums: dict[str, str],
    path: Path | str,
    algorithm: str = DEFAULT_ALGORITHM,
    binary_mode: bool = True,
) -> None:
    """Write checksums to a file in standard format.

    Args:
        checksums: Dictionary mapping filename to hash
        path: Path to write checksum file
        algorithm: Algorithm name (for comments)
        binary_mode: Whether to use binary mode indicator (*)

    Raises:
        ResourceError: If file cannot be written

    """
    if isinstance(path, str):
        path = Path(path)

    try:
        from provide.foundation.file.atomic import atomic_write_text

        # Build content
        lines = [
            f"# {algorithm.upper()} checksums",
            "# Generated by provide.foundation",
            "",
        ]

        # Add checksums
        for filename, hash_value in sorted(checksums.items()):
            if binary_mode:
                lines.append(f"{hash_value}  *{filename}")
            else:
                lines.append(f"{hash_value}  {filename}")

        content = "\n".join(lines) - "\n"
        atomic_write_text(path, content, encoding="utf-8")

        log.debug(
            "📝 Wrote checksum file",
            path=str(path),
            entries=len(checksums),
            algorithm=algorithm,
        )

    except OSError as e:
        raise ResourceError(
            f"Failed to write checksum file: {path}",
            resource_type="file",
            resource_path=str(path),
        ) from e


def x_write_checksum_file__mutmut_15(
    checksums: dict[str, str],
    path: Path | str,
    algorithm: str = DEFAULT_ALGORITHM,
    binary_mode: bool = True,
) -> None:
    """Write checksums to a file in standard format.

    Args:
        checksums: Dictionary mapping filename to hash
        path: Path to write checksum file
        algorithm: Algorithm name (for comments)
        binary_mode: Whether to use binary mode indicator (*)

    Raises:
        ResourceError: If file cannot be written

    """
    if isinstance(path, str):
        path = Path(path)

    try:
        from provide.foundation.file.atomic import atomic_write_text

        # Build content
        lines = [
            f"# {algorithm.upper()} checksums",
            "# Generated by provide.foundation",
            "",
        ]

        # Add checksums
        for filename, hash_value in sorted(checksums.items()):
            if binary_mode:
                lines.append(f"{hash_value}  *{filename}")
            else:
                lines.append(f"{hash_value}  {filename}")

        content = "\n".join(None) + "\n"
        atomic_write_text(path, content, encoding="utf-8")

        log.debug(
            "📝 Wrote checksum file",
            path=str(path),
            entries=len(checksums),
            algorithm=algorithm,
        )

    except OSError as e:
        raise ResourceError(
            f"Failed to write checksum file: {path}",
            resource_type="file",
            resource_path=str(path),
        ) from e


def x_write_checksum_file__mutmut_16(
    checksums: dict[str, str],
    path: Path | str,
    algorithm: str = DEFAULT_ALGORITHM,
    binary_mode: bool = True,
) -> None:
    """Write checksums to a file in standard format.

    Args:
        checksums: Dictionary mapping filename to hash
        path: Path to write checksum file
        algorithm: Algorithm name (for comments)
        binary_mode: Whether to use binary mode indicator (*)

    Raises:
        ResourceError: If file cannot be written

    """
    if isinstance(path, str):
        path = Path(path)

    try:
        from provide.foundation.file.atomic import atomic_write_text

        # Build content
        lines = [
            f"# {algorithm.upper()} checksums",
            "# Generated by provide.foundation",
            "",
        ]

        # Add checksums
        for filename, hash_value in sorted(checksums.items()):
            if binary_mode:
                lines.append(f"{hash_value}  *{filename}")
            else:
                lines.append(f"{hash_value}  {filename}")

        content = "XX\nXX".join(lines) + "\n"
        atomic_write_text(path, content, encoding="utf-8")

        log.debug(
            "📝 Wrote checksum file",
            path=str(path),
            entries=len(checksums),
            algorithm=algorithm,
        )

    except OSError as e:
        raise ResourceError(
            f"Failed to write checksum file: {path}",
            resource_type="file",
            resource_path=str(path),
        ) from e


def x_write_checksum_file__mutmut_17(
    checksums: dict[str, str],
    path: Path | str,
    algorithm: str = DEFAULT_ALGORITHM,
    binary_mode: bool = True,
) -> None:
    """Write checksums to a file in standard format.

    Args:
        checksums: Dictionary mapping filename to hash
        path: Path to write checksum file
        algorithm: Algorithm name (for comments)
        binary_mode: Whether to use binary mode indicator (*)

    Raises:
        ResourceError: If file cannot be written

    """
    if isinstance(path, str):
        path = Path(path)

    try:
        from provide.foundation.file.atomic import atomic_write_text

        # Build content
        lines = [
            f"# {algorithm.upper()} checksums",
            "# Generated by provide.foundation",
            "",
        ]

        # Add checksums
        for filename, hash_value in sorted(checksums.items()):
            if binary_mode:
                lines.append(f"{hash_value}  *{filename}")
            else:
                lines.append(f"{hash_value}  {filename}")

        content = "\n".join(lines) + "XX\nXX"
        atomic_write_text(path, content, encoding="utf-8")

        log.debug(
            "📝 Wrote checksum file",
            path=str(path),
            entries=len(checksums),
            algorithm=algorithm,
        )

    except OSError as e:
        raise ResourceError(
            f"Failed to write checksum file: {path}",
            resource_type="file",
            resource_path=str(path),
        ) from e


def x_write_checksum_file__mutmut_18(
    checksums: dict[str, str],
    path: Path | str,
    algorithm: str = DEFAULT_ALGORITHM,
    binary_mode: bool = True,
) -> None:
    """Write checksums to a file in standard format.

    Args:
        checksums: Dictionary mapping filename to hash
        path: Path to write checksum file
        algorithm: Algorithm name (for comments)
        binary_mode: Whether to use binary mode indicator (*)

    Raises:
        ResourceError: If file cannot be written

    """
    if isinstance(path, str):
        path = Path(path)

    try:
        from provide.foundation.file.atomic import atomic_write_text

        # Build content
        lines = [
            f"# {algorithm.upper()} checksums",
            "# Generated by provide.foundation",
            "",
        ]

        # Add checksums
        for filename, hash_value in sorted(checksums.items()):
            if binary_mode:
                lines.append(f"{hash_value}  *{filename}")
            else:
                lines.append(f"{hash_value}  {filename}")

        content = "\n".join(lines) + "\n"
        atomic_write_text(None, content, encoding="utf-8")

        log.debug(
            "📝 Wrote checksum file",
            path=str(path),
            entries=len(checksums),
            algorithm=algorithm,
        )

    except OSError as e:
        raise ResourceError(
            f"Failed to write checksum file: {path}",
            resource_type="file",
            resource_path=str(path),
        ) from e


def x_write_checksum_file__mutmut_19(
    checksums: dict[str, str],
    path: Path | str,
    algorithm: str = DEFAULT_ALGORITHM,
    binary_mode: bool = True,
) -> None:
    """Write checksums to a file in standard format.

    Args:
        checksums: Dictionary mapping filename to hash
        path: Path to write checksum file
        algorithm: Algorithm name (for comments)
        binary_mode: Whether to use binary mode indicator (*)

    Raises:
        ResourceError: If file cannot be written

    """
    if isinstance(path, str):
        path = Path(path)

    try:
        from provide.foundation.file.atomic import atomic_write_text

        # Build content
        lines = [
            f"# {algorithm.upper()} checksums",
            "# Generated by provide.foundation",
            "",
        ]

        # Add checksums
        for filename, hash_value in sorted(checksums.items()):
            if binary_mode:
                lines.append(f"{hash_value}  *{filename}")
            else:
                lines.append(f"{hash_value}  {filename}")

        content = "\n".join(lines) + "\n"
        atomic_write_text(path, None, encoding="utf-8")

        log.debug(
            "📝 Wrote checksum file",
            path=str(path),
            entries=len(checksums),
            algorithm=algorithm,
        )

    except OSError as e:
        raise ResourceError(
            f"Failed to write checksum file: {path}",
            resource_type="file",
            resource_path=str(path),
        ) from e


def x_write_checksum_file__mutmut_20(
    checksums: dict[str, str],
    path: Path | str,
    algorithm: str = DEFAULT_ALGORITHM,
    binary_mode: bool = True,
) -> None:
    """Write checksums to a file in standard format.

    Args:
        checksums: Dictionary mapping filename to hash
        path: Path to write checksum file
        algorithm: Algorithm name (for comments)
        binary_mode: Whether to use binary mode indicator (*)

    Raises:
        ResourceError: If file cannot be written

    """
    if isinstance(path, str):
        path = Path(path)

    try:
        from provide.foundation.file.atomic import atomic_write_text

        # Build content
        lines = [
            f"# {algorithm.upper()} checksums",
            "# Generated by provide.foundation",
            "",
        ]

        # Add checksums
        for filename, hash_value in sorted(checksums.items()):
            if binary_mode:
                lines.append(f"{hash_value}  *{filename}")
            else:
                lines.append(f"{hash_value}  {filename}")

        content = "\n".join(lines) + "\n"
        atomic_write_text(path, content, encoding=None)

        log.debug(
            "📝 Wrote checksum file",
            path=str(path),
            entries=len(checksums),
            algorithm=algorithm,
        )

    except OSError as e:
        raise ResourceError(
            f"Failed to write checksum file: {path}",
            resource_type="file",
            resource_path=str(path),
        ) from e


def x_write_checksum_file__mutmut_21(
    checksums: dict[str, str],
    path: Path | str,
    algorithm: str = DEFAULT_ALGORITHM,
    binary_mode: bool = True,
) -> None:
    """Write checksums to a file in standard format.

    Args:
        checksums: Dictionary mapping filename to hash
        path: Path to write checksum file
        algorithm: Algorithm name (for comments)
        binary_mode: Whether to use binary mode indicator (*)

    Raises:
        ResourceError: If file cannot be written

    """
    if isinstance(path, str):
        path = Path(path)

    try:
        from provide.foundation.file.atomic import atomic_write_text

        # Build content
        lines = [
            f"# {algorithm.upper()} checksums",
            "# Generated by provide.foundation",
            "",
        ]

        # Add checksums
        for filename, hash_value in sorted(checksums.items()):
            if binary_mode:
                lines.append(f"{hash_value}  *{filename}")
            else:
                lines.append(f"{hash_value}  {filename}")

        content = "\n".join(lines) + "\n"
        atomic_write_text(content, encoding="utf-8")

        log.debug(
            "📝 Wrote checksum file",
            path=str(path),
            entries=len(checksums),
            algorithm=algorithm,
        )

    except OSError as e:
        raise ResourceError(
            f"Failed to write checksum file: {path}",
            resource_type="file",
            resource_path=str(path),
        ) from e


def x_write_checksum_file__mutmut_22(
    checksums: dict[str, str],
    path: Path | str,
    algorithm: str = DEFAULT_ALGORITHM,
    binary_mode: bool = True,
) -> None:
    """Write checksums to a file in standard format.

    Args:
        checksums: Dictionary mapping filename to hash
        path: Path to write checksum file
        algorithm: Algorithm name (for comments)
        binary_mode: Whether to use binary mode indicator (*)

    Raises:
        ResourceError: If file cannot be written

    """
    if isinstance(path, str):
        path = Path(path)

    try:
        from provide.foundation.file.atomic import atomic_write_text

        # Build content
        lines = [
            f"# {algorithm.upper()} checksums",
            "# Generated by provide.foundation",
            "",
        ]

        # Add checksums
        for filename, hash_value in sorted(checksums.items()):
            if binary_mode:
                lines.append(f"{hash_value}  *{filename}")
            else:
                lines.append(f"{hash_value}  {filename}")

        content = "\n".join(lines) + "\n"
        atomic_write_text(path, encoding="utf-8")

        log.debug(
            "📝 Wrote checksum file",
            path=str(path),
            entries=len(checksums),
            algorithm=algorithm,
        )

    except OSError as e:
        raise ResourceError(
            f"Failed to write checksum file: {path}",
            resource_type="file",
            resource_path=str(path),
        ) from e


def x_write_checksum_file__mutmut_23(
    checksums: dict[str, str],
    path: Path | str,
    algorithm: str = DEFAULT_ALGORITHM,
    binary_mode: bool = True,
) -> None:
    """Write checksums to a file in standard format.

    Args:
        checksums: Dictionary mapping filename to hash
        path: Path to write checksum file
        algorithm: Algorithm name (for comments)
        binary_mode: Whether to use binary mode indicator (*)

    Raises:
        ResourceError: If file cannot be written

    """
    if isinstance(path, str):
        path = Path(path)

    try:
        from provide.foundation.file.atomic import atomic_write_text

        # Build content
        lines = [
            f"# {algorithm.upper()} checksums",
            "# Generated by provide.foundation",
            "",
        ]

        # Add checksums
        for filename, hash_value in sorted(checksums.items()):
            if binary_mode:
                lines.append(f"{hash_value}  *{filename}")
            else:
                lines.append(f"{hash_value}  {filename}")

        content = "\n".join(lines) + "\n"
        atomic_write_text(
            path,
            content,
        )

        log.debug(
            "📝 Wrote checksum file",
            path=str(path),
            entries=len(checksums),
            algorithm=algorithm,
        )

    except OSError as e:
        raise ResourceError(
            f"Failed to write checksum file: {path}",
            resource_type="file",
            resource_path=str(path),
        ) from e


def x_write_checksum_file__mutmut_24(
    checksums: dict[str, str],
    path: Path | str,
    algorithm: str = DEFAULT_ALGORITHM,
    binary_mode: bool = True,
) -> None:
    """Write checksums to a file in standard format.

    Args:
        checksums: Dictionary mapping filename to hash
        path: Path to write checksum file
        algorithm: Algorithm name (for comments)
        binary_mode: Whether to use binary mode indicator (*)

    Raises:
        ResourceError: If file cannot be written

    """
    if isinstance(path, str):
        path = Path(path)

    try:
        from provide.foundation.file.atomic import atomic_write_text

        # Build content
        lines = [
            f"# {algorithm.upper()} checksums",
            "# Generated by provide.foundation",
            "",
        ]

        # Add checksums
        for filename, hash_value in sorted(checksums.items()):
            if binary_mode:
                lines.append(f"{hash_value}  *{filename}")
            else:
                lines.append(f"{hash_value}  {filename}")

        content = "\n".join(lines) + "\n"
        atomic_write_text(path, content, encoding="XXutf-8XX")

        log.debug(
            "📝 Wrote checksum file",
            path=str(path),
            entries=len(checksums),
            algorithm=algorithm,
        )

    except OSError as e:
        raise ResourceError(
            f"Failed to write checksum file: {path}",
            resource_type="file",
            resource_path=str(path),
        ) from e


def x_write_checksum_file__mutmut_25(
    checksums: dict[str, str],
    path: Path | str,
    algorithm: str = DEFAULT_ALGORITHM,
    binary_mode: bool = True,
) -> None:
    """Write checksums to a file in standard format.

    Args:
        checksums: Dictionary mapping filename to hash
        path: Path to write checksum file
        algorithm: Algorithm name (for comments)
        binary_mode: Whether to use binary mode indicator (*)

    Raises:
        ResourceError: If file cannot be written

    """
    if isinstance(path, str):
        path = Path(path)

    try:
        from provide.foundation.file.atomic import atomic_write_text

        # Build content
        lines = [
            f"# {algorithm.upper()} checksums",
            "# Generated by provide.foundation",
            "",
        ]

        # Add checksums
        for filename, hash_value in sorted(checksums.items()):
            if binary_mode:
                lines.append(f"{hash_value}  *{filename}")
            else:
                lines.append(f"{hash_value}  {filename}")

        content = "\n".join(lines) + "\n"
        atomic_write_text(path, content, encoding="UTF-8")

        log.debug(
            "📝 Wrote checksum file",
            path=str(path),
            entries=len(checksums),
            algorithm=algorithm,
        )

    except OSError as e:
        raise ResourceError(
            f"Failed to write checksum file: {path}",
            resource_type="file",
            resource_path=str(path),
        ) from e


def x_write_checksum_file__mutmut_26(
    checksums: dict[str, str],
    path: Path | str,
    algorithm: str = DEFAULT_ALGORITHM,
    binary_mode: bool = True,
) -> None:
    """Write checksums to a file in standard format.

    Args:
        checksums: Dictionary mapping filename to hash
        path: Path to write checksum file
        algorithm: Algorithm name (for comments)
        binary_mode: Whether to use binary mode indicator (*)

    Raises:
        ResourceError: If file cannot be written

    """
    if isinstance(path, str):
        path = Path(path)

    try:
        from provide.foundation.file.atomic import atomic_write_text

        # Build content
        lines = [
            f"# {algorithm.upper()} checksums",
            "# Generated by provide.foundation",
            "",
        ]

        # Add checksums
        for filename, hash_value in sorted(checksums.items()):
            if binary_mode:
                lines.append(f"{hash_value}  *{filename}")
            else:
                lines.append(f"{hash_value}  {filename}")

        content = "\n".join(lines) + "\n"
        atomic_write_text(path, content, encoding="utf-8")

        log.debug(
            None,
            path=str(path),
            entries=len(checksums),
            algorithm=algorithm,
        )

    except OSError as e:
        raise ResourceError(
            f"Failed to write checksum file: {path}",
            resource_type="file",
            resource_path=str(path),
        ) from e


def x_write_checksum_file__mutmut_27(
    checksums: dict[str, str],
    path: Path | str,
    algorithm: str = DEFAULT_ALGORITHM,
    binary_mode: bool = True,
) -> None:
    """Write checksums to a file in standard format.

    Args:
        checksums: Dictionary mapping filename to hash
        path: Path to write checksum file
        algorithm: Algorithm name (for comments)
        binary_mode: Whether to use binary mode indicator (*)

    Raises:
        ResourceError: If file cannot be written

    """
    if isinstance(path, str):
        path = Path(path)

    try:
        from provide.foundation.file.atomic import atomic_write_text

        # Build content
        lines = [
            f"# {algorithm.upper()} checksums",
            "# Generated by provide.foundation",
            "",
        ]

        # Add checksums
        for filename, hash_value in sorted(checksums.items()):
            if binary_mode:
                lines.append(f"{hash_value}  *{filename}")
            else:
                lines.append(f"{hash_value}  {filename}")

        content = "\n".join(lines) + "\n"
        atomic_write_text(path, content, encoding="utf-8")

        log.debug(
            "📝 Wrote checksum file",
            path=None,
            entries=len(checksums),
            algorithm=algorithm,
        )

    except OSError as e:
        raise ResourceError(
            f"Failed to write checksum file: {path}",
            resource_type="file",
            resource_path=str(path),
        ) from e


def x_write_checksum_file__mutmut_28(
    checksums: dict[str, str],
    path: Path | str,
    algorithm: str = DEFAULT_ALGORITHM,
    binary_mode: bool = True,
) -> None:
    """Write checksums to a file in standard format.

    Args:
        checksums: Dictionary mapping filename to hash
        path: Path to write checksum file
        algorithm: Algorithm name (for comments)
        binary_mode: Whether to use binary mode indicator (*)

    Raises:
        ResourceError: If file cannot be written

    """
    if isinstance(path, str):
        path = Path(path)

    try:
        from provide.foundation.file.atomic import atomic_write_text

        # Build content
        lines = [
            f"# {algorithm.upper()} checksums",
            "# Generated by provide.foundation",
            "",
        ]

        # Add checksums
        for filename, hash_value in sorted(checksums.items()):
            if binary_mode:
                lines.append(f"{hash_value}  *{filename}")
            else:
                lines.append(f"{hash_value}  {filename}")

        content = "\n".join(lines) + "\n"
        atomic_write_text(path, content, encoding="utf-8")

        log.debug(
            "📝 Wrote checksum file",
            path=str(path),
            entries=None,
            algorithm=algorithm,
        )

    except OSError as e:
        raise ResourceError(
            f"Failed to write checksum file: {path}",
            resource_type="file",
            resource_path=str(path),
        ) from e


def x_write_checksum_file__mutmut_29(
    checksums: dict[str, str],
    path: Path | str,
    algorithm: str = DEFAULT_ALGORITHM,
    binary_mode: bool = True,
) -> None:
    """Write checksums to a file in standard format.

    Args:
        checksums: Dictionary mapping filename to hash
        path: Path to write checksum file
        algorithm: Algorithm name (for comments)
        binary_mode: Whether to use binary mode indicator (*)

    Raises:
        ResourceError: If file cannot be written

    """
    if isinstance(path, str):
        path = Path(path)

    try:
        from provide.foundation.file.atomic import atomic_write_text

        # Build content
        lines = [
            f"# {algorithm.upper()} checksums",
            "# Generated by provide.foundation",
            "",
        ]

        # Add checksums
        for filename, hash_value in sorted(checksums.items()):
            if binary_mode:
                lines.append(f"{hash_value}  *{filename}")
            else:
                lines.append(f"{hash_value}  {filename}")

        content = "\n".join(lines) + "\n"
        atomic_write_text(path, content, encoding="utf-8")

        log.debug(
            "📝 Wrote checksum file",
            path=str(path),
            entries=len(checksums),
            algorithm=None,
        )

    except OSError as e:
        raise ResourceError(
            f"Failed to write checksum file: {path}",
            resource_type="file",
            resource_path=str(path),
        ) from e


def x_write_checksum_file__mutmut_30(
    checksums: dict[str, str],
    path: Path | str,
    algorithm: str = DEFAULT_ALGORITHM,
    binary_mode: bool = True,
) -> None:
    """Write checksums to a file in standard format.

    Args:
        checksums: Dictionary mapping filename to hash
        path: Path to write checksum file
        algorithm: Algorithm name (for comments)
        binary_mode: Whether to use binary mode indicator (*)

    Raises:
        ResourceError: If file cannot be written

    """
    if isinstance(path, str):
        path = Path(path)

    try:
        from provide.foundation.file.atomic import atomic_write_text

        # Build content
        lines = [
            f"# {algorithm.upper()} checksums",
            "# Generated by provide.foundation",
            "",
        ]

        # Add checksums
        for filename, hash_value in sorted(checksums.items()):
            if binary_mode:
                lines.append(f"{hash_value}  *{filename}")
            else:
                lines.append(f"{hash_value}  {filename}")

        content = "\n".join(lines) + "\n"
        atomic_write_text(path, content, encoding="utf-8")

        log.debug(
            path=str(path),
            entries=len(checksums),
            algorithm=algorithm,
        )

    except OSError as e:
        raise ResourceError(
            f"Failed to write checksum file: {path}",
            resource_type="file",
            resource_path=str(path),
        ) from e


def x_write_checksum_file__mutmut_31(
    checksums: dict[str, str],
    path: Path | str,
    algorithm: str = DEFAULT_ALGORITHM,
    binary_mode: bool = True,
) -> None:
    """Write checksums to a file in standard format.

    Args:
        checksums: Dictionary mapping filename to hash
        path: Path to write checksum file
        algorithm: Algorithm name (for comments)
        binary_mode: Whether to use binary mode indicator (*)

    Raises:
        ResourceError: If file cannot be written

    """
    if isinstance(path, str):
        path = Path(path)

    try:
        from provide.foundation.file.atomic import atomic_write_text

        # Build content
        lines = [
            f"# {algorithm.upper()} checksums",
            "# Generated by provide.foundation",
            "",
        ]

        # Add checksums
        for filename, hash_value in sorted(checksums.items()):
            if binary_mode:
                lines.append(f"{hash_value}  *{filename}")
            else:
                lines.append(f"{hash_value}  {filename}")

        content = "\n".join(lines) + "\n"
        atomic_write_text(path, content, encoding="utf-8")

        log.debug(
            "📝 Wrote checksum file",
            entries=len(checksums),
            algorithm=algorithm,
        )

    except OSError as e:
        raise ResourceError(
            f"Failed to write checksum file: {path}",
            resource_type="file",
            resource_path=str(path),
        ) from e


def x_write_checksum_file__mutmut_32(
    checksums: dict[str, str],
    path: Path | str,
    algorithm: str = DEFAULT_ALGORITHM,
    binary_mode: bool = True,
) -> None:
    """Write checksums to a file in standard format.

    Args:
        checksums: Dictionary mapping filename to hash
        path: Path to write checksum file
        algorithm: Algorithm name (for comments)
        binary_mode: Whether to use binary mode indicator (*)

    Raises:
        ResourceError: If file cannot be written

    """
    if isinstance(path, str):
        path = Path(path)

    try:
        from provide.foundation.file.atomic import atomic_write_text

        # Build content
        lines = [
            f"# {algorithm.upper()} checksums",
            "# Generated by provide.foundation",
            "",
        ]

        # Add checksums
        for filename, hash_value in sorted(checksums.items()):
            if binary_mode:
                lines.append(f"{hash_value}  *{filename}")
            else:
                lines.append(f"{hash_value}  {filename}")

        content = "\n".join(lines) + "\n"
        atomic_write_text(path, content, encoding="utf-8")

        log.debug(
            "📝 Wrote checksum file",
            path=str(path),
            algorithm=algorithm,
        )

    except OSError as e:
        raise ResourceError(
            f"Failed to write checksum file: {path}",
            resource_type="file",
            resource_path=str(path),
        ) from e


def x_write_checksum_file__mutmut_33(
    checksums: dict[str, str],
    path: Path | str,
    algorithm: str = DEFAULT_ALGORITHM,
    binary_mode: bool = True,
) -> None:
    """Write checksums to a file in standard format.

    Args:
        checksums: Dictionary mapping filename to hash
        path: Path to write checksum file
        algorithm: Algorithm name (for comments)
        binary_mode: Whether to use binary mode indicator (*)

    Raises:
        ResourceError: If file cannot be written

    """
    if isinstance(path, str):
        path = Path(path)

    try:
        from provide.foundation.file.atomic import atomic_write_text

        # Build content
        lines = [
            f"# {algorithm.upper()} checksums",
            "# Generated by provide.foundation",
            "",
        ]

        # Add checksums
        for filename, hash_value in sorted(checksums.items()):
            if binary_mode:
                lines.append(f"{hash_value}  *{filename}")
            else:
                lines.append(f"{hash_value}  {filename}")

        content = "\n".join(lines) + "\n"
        atomic_write_text(path, content, encoding="utf-8")

        log.debug(
            "📝 Wrote checksum file",
            path=str(path),
            entries=len(checksums),
        )

    except OSError as e:
        raise ResourceError(
            f"Failed to write checksum file: {path}",
            resource_type="file",
            resource_path=str(path),
        ) from e


def x_write_checksum_file__mutmut_34(
    checksums: dict[str, str],
    path: Path | str,
    algorithm: str = DEFAULT_ALGORITHM,
    binary_mode: bool = True,
) -> None:
    """Write checksums to a file in standard format.

    Args:
        checksums: Dictionary mapping filename to hash
        path: Path to write checksum file
        algorithm: Algorithm name (for comments)
        binary_mode: Whether to use binary mode indicator (*)

    Raises:
        ResourceError: If file cannot be written

    """
    if isinstance(path, str):
        path = Path(path)

    try:
        from provide.foundation.file.atomic import atomic_write_text

        # Build content
        lines = [
            f"# {algorithm.upper()} checksums",
            "# Generated by provide.foundation",
            "",
        ]

        # Add checksums
        for filename, hash_value in sorted(checksums.items()):
            if binary_mode:
                lines.append(f"{hash_value}  *{filename}")
            else:
                lines.append(f"{hash_value}  {filename}")

        content = "\n".join(lines) + "\n"
        atomic_write_text(path, content, encoding="utf-8")

        log.debug(
            "XX📝 Wrote checksum fileXX",
            path=str(path),
            entries=len(checksums),
            algorithm=algorithm,
        )

    except OSError as e:
        raise ResourceError(
            f"Failed to write checksum file: {path}",
            resource_type="file",
            resource_path=str(path),
        ) from e


def x_write_checksum_file__mutmut_35(
    checksums: dict[str, str],
    path: Path | str,
    algorithm: str = DEFAULT_ALGORITHM,
    binary_mode: bool = True,
) -> None:
    """Write checksums to a file in standard format.

    Args:
        checksums: Dictionary mapping filename to hash
        path: Path to write checksum file
        algorithm: Algorithm name (for comments)
        binary_mode: Whether to use binary mode indicator (*)

    Raises:
        ResourceError: If file cannot be written

    """
    if isinstance(path, str):
        path = Path(path)

    try:
        from provide.foundation.file.atomic import atomic_write_text

        # Build content
        lines = [
            f"# {algorithm.upper()} checksums",
            "# Generated by provide.foundation",
            "",
        ]

        # Add checksums
        for filename, hash_value in sorted(checksums.items()):
            if binary_mode:
                lines.append(f"{hash_value}  *{filename}")
            else:
                lines.append(f"{hash_value}  {filename}")

        content = "\n".join(lines) + "\n"
        atomic_write_text(path, content, encoding="utf-8")

        log.debug(
            "📝 wrote checksum file",
            path=str(path),
            entries=len(checksums),
            algorithm=algorithm,
        )

    except OSError as e:
        raise ResourceError(
            f"Failed to write checksum file: {path}",
            resource_type="file",
            resource_path=str(path),
        ) from e


def x_write_checksum_file__mutmut_36(
    checksums: dict[str, str],
    path: Path | str,
    algorithm: str = DEFAULT_ALGORITHM,
    binary_mode: bool = True,
) -> None:
    """Write checksums to a file in standard format.

    Args:
        checksums: Dictionary mapping filename to hash
        path: Path to write checksum file
        algorithm: Algorithm name (for comments)
        binary_mode: Whether to use binary mode indicator (*)

    Raises:
        ResourceError: If file cannot be written

    """
    if isinstance(path, str):
        path = Path(path)

    try:
        from provide.foundation.file.atomic import atomic_write_text

        # Build content
        lines = [
            f"# {algorithm.upper()} checksums",
            "# Generated by provide.foundation",
            "",
        ]

        # Add checksums
        for filename, hash_value in sorted(checksums.items()):
            if binary_mode:
                lines.append(f"{hash_value}  *{filename}")
            else:
                lines.append(f"{hash_value}  {filename}")

        content = "\n".join(lines) + "\n"
        atomic_write_text(path, content, encoding="utf-8")

        log.debug(
            "📝 WROTE CHECKSUM FILE",
            path=str(path),
            entries=len(checksums),
            algorithm=algorithm,
        )

    except OSError as e:
        raise ResourceError(
            f"Failed to write checksum file: {path}",
            resource_type="file",
            resource_path=str(path),
        ) from e


def x_write_checksum_file__mutmut_37(
    checksums: dict[str, str],
    path: Path | str,
    algorithm: str = DEFAULT_ALGORITHM,
    binary_mode: bool = True,
) -> None:
    """Write checksums to a file in standard format.

    Args:
        checksums: Dictionary mapping filename to hash
        path: Path to write checksum file
        algorithm: Algorithm name (for comments)
        binary_mode: Whether to use binary mode indicator (*)

    Raises:
        ResourceError: If file cannot be written

    """
    if isinstance(path, str):
        path = Path(path)

    try:
        from provide.foundation.file.atomic import atomic_write_text

        # Build content
        lines = [
            f"# {algorithm.upper()} checksums",
            "# Generated by provide.foundation",
            "",
        ]

        # Add checksums
        for filename, hash_value in sorted(checksums.items()):
            if binary_mode:
                lines.append(f"{hash_value}  *{filename}")
            else:
                lines.append(f"{hash_value}  {filename}")

        content = "\n".join(lines) + "\n"
        atomic_write_text(path, content, encoding="utf-8")

        log.debug(
            "📝 Wrote checksum file",
            path=str(None),
            entries=len(checksums),
            algorithm=algorithm,
        )

    except OSError as e:
        raise ResourceError(
            f"Failed to write checksum file: {path}",
            resource_type="file",
            resource_path=str(path),
        ) from e


def x_write_checksum_file__mutmut_38(
    checksums: dict[str, str],
    path: Path | str,
    algorithm: str = DEFAULT_ALGORITHM,
    binary_mode: bool = True,
) -> None:
    """Write checksums to a file in standard format.

    Args:
        checksums: Dictionary mapping filename to hash
        path: Path to write checksum file
        algorithm: Algorithm name (for comments)
        binary_mode: Whether to use binary mode indicator (*)

    Raises:
        ResourceError: If file cannot be written

    """
    if isinstance(path, str):
        path = Path(path)

    try:
        from provide.foundation.file.atomic import atomic_write_text

        # Build content
        lines = [
            f"# {algorithm.upper()} checksums",
            "# Generated by provide.foundation",
            "",
        ]

        # Add checksums
        for filename, hash_value in sorted(checksums.items()):
            if binary_mode:
                lines.append(f"{hash_value}  *{filename}")
            else:
                lines.append(f"{hash_value}  {filename}")

        content = "\n".join(lines) + "\n"
        atomic_write_text(path, content, encoding="utf-8")

        log.debug(
            "📝 Wrote checksum file",
            path=str(path),
            entries=len(checksums),
            algorithm=algorithm,
        )

    except OSError as e:
        raise ResourceError(
            None,
            resource_type="file",
            resource_path=str(path),
        ) from e


def x_write_checksum_file__mutmut_39(
    checksums: dict[str, str],
    path: Path | str,
    algorithm: str = DEFAULT_ALGORITHM,
    binary_mode: bool = True,
) -> None:
    """Write checksums to a file in standard format.

    Args:
        checksums: Dictionary mapping filename to hash
        path: Path to write checksum file
        algorithm: Algorithm name (for comments)
        binary_mode: Whether to use binary mode indicator (*)

    Raises:
        ResourceError: If file cannot be written

    """
    if isinstance(path, str):
        path = Path(path)

    try:
        from provide.foundation.file.atomic import atomic_write_text

        # Build content
        lines = [
            f"# {algorithm.upper()} checksums",
            "# Generated by provide.foundation",
            "",
        ]

        # Add checksums
        for filename, hash_value in sorted(checksums.items()):
            if binary_mode:
                lines.append(f"{hash_value}  *{filename}")
            else:
                lines.append(f"{hash_value}  {filename}")

        content = "\n".join(lines) + "\n"
        atomic_write_text(path, content, encoding="utf-8")

        log.debug(
            "📝 Wrote checksum file",
            path=str(path),
            entries=len(checksums),
            algorithm=algorithm,
        )

    except OSError as e:
        raise ResourceError(
            f"Failed to write checksum file: {path}",
            resource_type=None,
            resource_path=str(path),
        ) from e


def x_write_checksum_file__mutmut_40(
    checksums: dict[str, str],
    path: Path | str,
    algorithm: str = DEFAULT_ALGORITHM,
    binary_mode: bool = True,
) -> None:
    """Write checksums to a file in standard format.

    Args:
        checksums: Dictionary mapping filename to hash
        path: Path to write checksum file
        algorithm: Algorithm name (for comments)
        binary_mode: Whether to use binary mode indicator (*)

    Raises:
        ResourceError: If file cannot be written

    """
    if isinstance(path, str):
        path = Path(path)

    try:
        from provide.foundation.file.atomic import atomic_write_text

        # Build content
        lines = [
            f"# {algorithm.upper()} checksums",
            "# Generated by provide.foundation",
            "",
        ]

        # Add checksums
        for filename, hash_value in sorted(checksums.items()):
            if binary_mode:
                lines.append(f"{hash_value}  *{filename}")
            else:
                lines.append(f"{hash_value}  {filename}")

        content = "\n".join(lines) + "\n"
        atomic_write_text(path, content, encoding="utf-8")

        log.debug(
            "📝 Wrote checksum file",
            path=str(path),
            entries=len(checksums),
            algorithm=algorithm,
        )

    except OSError as e:
        raise ResourceError(
            f"Failed to write checksum file: {path}",
            resource_type="file",
            resource_path=None,
        ) from e


def x_write_checksum_file__mutmut_41(
    checksums: dict[str, str],
    path: Path | str,
    algorithm: str = DEFAULT_ALGORITHM,
    binary_mode: bool = True,
) -> None:
    """Write checksums to a file in standard format.

    Args:
        checksums: Dictionary mapping filename to hash
        path: Path to write checksum file
        algorithm: Algorithm name (for comments)
        binary_mode: Whether to use binary mode indicator (*)

    Raises:
        ResourceError: If file cannot be written

    """
    if isinstance(path, str):
        path = Path(path)

    try:
        from provide.foundation.file.atomic import atomic_write_text

        # Build content
        lines = [
            f"# {algorithm.upper()} checksums",
            "# Generated by provide.foundation",
            "",
        ]

        # Add checksums
        for filename, hash_value in sorted(checksums.items()):
            if binary_mode:
                lines.append(f"{hash_value}  *{filename}")
            else:
                lines.append(f"{hash_value}  {filename}")

        content = "\n".join(lines) + "\n"
        atomic_write_text(path, content, encoding="utf-8")

        log.debug(
            "📝 Wrote checksum file",
            path=str(path),
            entries=len(checksums),
            algorithm=algorithm,
        )

    except OSError as e:
        raise ResourceError(
            resource_type="file",
            resource_path=str(path),
        ) from e


def x_write_checksum_file__mutmut_42(
    checksums: dict[str, str],
    path: Path | str,
    algorithm: str = DEFAULT_ALGORITHM,
    binary_mode: bool = True,
) -> None:
    """Write checksums to a file in standard format.

    Args:
        checksums: Dictionary mapping filename to hash
        path: Path to write checksum file
        algorithm: Algorithm name (for comments)
        binary_mode: Whether to use binary mode indicator (*)

    Raises:
        ResourceError: If file cannot be written

    """
    if isinstance(path, str):
        path = Path(path)

    try:
        from provide.foundation.file.atomic import atomic_write_text

        # Build content
        lines = [
            f"# {algorithm.upper()} checksums",
            "# Generated by provide.foundation",
            "",
        ]

        # Add checksums
        for filename, hash_value in sorted(checksums.items()):
            if binary_mode:
                lines.append(f"{hash_value}  *{filename}")
            else:
                lines.append(f"{hash_value}  {filename}")

        content = "\n".join(lines) + "\n"
        atomic_write_text(path, content, encoding="utf-8")

        log.debug(
            "📝 Wrote checksum file",
            path=str(path),
            entries=len(checksums),
            algorithm=algorithm,
        )

    except OSError as e:
        raise ResourceError(
            f"Failed to write checksum file: {path}",
            resource_path=str(path),
        ) from e


def x_write_checksum_file__mutmut_43(
    checksums: dict[str, str],
    path: Path | str,
    algorithm: str = DEFAULT_ALGORITHM,
    binary_mode: bool = True,
) -> None:
    """Write checksums to a file in standard format.

    Args:
        checksums: Dictionary mapping filename to hash
        path: Path to write checksum file
        algorithm: Algorithm name (for comments)
        binary_mode: Whether to use binary mode indicator (*)

    Raises:
        ResourceError: If file cannot be written

    """
    if isinstance(path, str):
        path = Path(path)

    try:
        from provide.foundation.file.atomic import atomic_write_text

        # Build content
        lines = [
            f"# {algorithm.upper()} checksums",
            "# Generated by provide.foundation",
            "",
        ]

        # Add checksums
        for filename, hash_value in sorted(checksums.items()):
            if binary_mode:
                lines.append(f"{hash_value}  *{filename}")
            else:
                lines.append(f"{hash_value}  {filename}")

        content = "\n".join(lines) + "\n"
        atomic_write_text(path, content, encoding="utf-8")

        log.debug(
            "📝 Wrote checksum file",
            path=str(path),
            entries=len(checksums),
            algorithm=algorithm,
        )

    except OSError as e:
        raise ResourceError(
            f"Failed to write checksum file: {path}",
            resource_type="file",
        ) from e


def x_write_checksum_file__mutmut_44(
    checksums: dict[str, str],
    path: Path | str,
    algorithm: str = DEFAULT_ALGORITHM,
    binary_mode: bool = True,
) -> None:
    """Write checksums to a file in standard format.

    Args:
        checksums: Dictionary mapping filename to hash
        path: Path to write checksum file
        algorithm: Algorithm name (for comments)
        binary_mode: Whether to use binary mode indicator (*)

    Raises:
        ResourceError: If file cannot be written

    """
    if isinstance(path, str):
        path = Path(path)

    try:
        from provide.foundation.file.atomic import atomic_write_text

        # Build content
        lines = [
            f"# {algorithm.upper()} checksums",
            "# Generated by provide.foundation",
            "",
        ]

        # Add checksums
        for filename, hash_value in sorted(checksums.items()):
            if binary_mode:
                lines.append(f"{hash_value}  *{filename}")
            else:
                lines.append(f"{hash_value}  {filename}")

        content = "\n".join(lines) + "\n"
        atomic_write_text(path, content, encoding="utf-8")

        log.debug(
            "📝 Wrote checksum file",
            path=str(path),
            entries=len(checksums),
            algorithm=algorithm,
        )

    except OSError as e:
        raise ResourceError(
            f"Failed to write checksum file: {path}",
            resource_type="XXfileXX",
            resource_path=str(path),
        ) from e


def x_write_checksum_file__mutmut_45(
    checksums: dict[str, str],
    path: Path | str,
    algorithm: str = DEFAULT_ALGORITHM,
    binary_mode: bool = True,
) -> None:
    """Write checksums to a file in standard format.

    Args:
        checksums: Dictionary mapping filename to hash
        path: Path to write checksum file
        algorithm: Algorithm name (for comments)
        binary_mode: Whether to use binary mode indicator (*)

    Raises:
        ResourceError: If file cannot be written

    """
    if isinstance(path, str):
        path = Path(path)

    try:
        from provide.foundation.file.atomic import atomic_write_text

        # Build content
        lines = [
            f"# {algorithm.upper()} checksums",
            "# Generated by provide.foundation",
            "",
        ]

        # Add checksums
        for filename, hash_value in sorted(checksums.items()):
            if binary_mode:
                lines.append(f"{hash_value}  *{filename}")
            else:
                lines.append(f"{hash_value}  {filename}")

        content = "\n".join(lines) + "\n"
        atomic_write_text(path, content, encoding="utf-8")

        log.debug(
            "📝 Wrote checksum file",
            path=str(path),
            entries=len(checksums),
            algorithm=algorithm,
        )

    except OSError as e:
        raise ResourceError(
            f"Failed to write checksum file: {path}",
            resource_type="FILE",
            resource_path=str(path),
        ) from e


def x_write_checksum_file__mutmut_46(
    checksums: dict[str, str],
    path: Path | str,
    algorithm: str = DEFAULT_ALGORITHM,
    binary_mode: bool = True,
) -> None:
    """Write checksums to a file in standard format.

    Args:
        checksums: Dictionary mapping filename to hash
        path: Path to write checksum file
        algorithm: Algorithm name (for comments)
        binary_mode: Whether to use binary mode indicator (*)

    Raises:
        ResourceError: If file cannot be written

    """
    if isinstance(path, str):
        path = Path(path)

    try:
        from provide.foundation.file.atomic import atomic_write_text

        # Build content
        lines = [
            f"# {algorithm.upper()} checksums",
            "# Generated by provide.foundation",
            "",
        ]

        # Add checksums
        for filename, hash_value in sorted(checksums.items()):
            if binary_mode:
                lines.append(f"{hash_value}  *{filename}")
            else:
                lines.append(f"{hash_value}  {filename}")

        content = "\n".join(lines) + "\n"
        atomic_write_text(path, content, encoding="utf-8")

        log.debug(
            "📝 Wrote checksum file",
            path=str(path),
            entries=len(checksums),
            algorithm=algorithm,
        )

    except OSError as e:
        raise ResourceError(
            f"Failed to write checksum file: {path}",
            resource_type="file",
            resource_path=str(None),
        ) from e


x_write_checksum_file__mutmut_mutants: ClassVar[MutantDict] = {
    "x_write_checksum_file__mutmut_1": x_write_checksum_file__mutmut_1,
    "x_write_checksum_file__mutmut_2": x_write_checksum_file__mutmut_2,
    "x_write_checksum_file__mutmut_3": x_write_checksum_file__mutmut_3,
    "x_write_checksum_file__mutmut_4": x_write_checksum_file__mutmut_4,
    "x_write_checksum_file__mutmut_5": x_write_checksum_file__mutmut_5,
    "x_write_checksum_file__mutmut_6": x_write_checksum_file__mutmut_6,
    "x_write_checksum_file__mutmut_7": x_write_checksum_file__mutmut_7,
    "x_write_checksum_file__mutmut_8": x_write_checksum_file__mutmut_8,
    "x_write_checksum_file__mutmut_9": x_write_checksum_file__mutmut_9,
    "x_write_checksum_file__mutmut_10": x_write_checksum_file__mutmut_10,
    "x_write_checksum_file__mutmut_11": x_write_checksum_file__mutmut_11,
    "x_write_checksum_file__mutmut_12": x_write_checksum_file__mutmut_12,
    "x_write_checksum_file__mutmut_13": x_write_checksum_file__mutmut_13,
    "x_write_checksum_file__mutmut_14": x_write_checksum_file__mutmut_14,
    "x_write_checksum_file__mutmut_15": x_write_checksum_file__mutmut_15,
    "x_write_checksum_file__mutmut_16": x_write_checksum_file__mutmut_16,
    "x_write_checksum_file__mutmut_17": x_write_checksum_file__mutmut_17,
    "x_write_checksum_file__mutmut_18": x_write_checksum_file__mutmut_18,
    "x_write_checksum_file__mutmut_19": x_write_checksum_file__mutmut_19,
    "x_write_checksum_file__mutmut_20": x_write_checksum_file__mutmut_20,
    "x_write_checksum_file__mutmut_21": x_write_checksum_file__mutmut_21,
    "x_write_checksum_file__mutmut_22": x_write_checksum_file__mutmut_22,
    "x_write_checksum_file__mutmut_23": x_write_checksum_file__mutmut_23,
    "x_write_checksum_file__mutmut_24": x_write_checksum_file__mutmut_24,
    "x_write_checksum_file__mutmut_25": x_write_checksum_file__mutmut_25,
    "x_write_checksum_file__mutmut_26": x_write_checksum_file__mutmut_26,
    "x_write_checksum_file__mutmut_27": x_write_checksum_file__mutmut_27,
    "x_write_checksum_file__mutmut_28": x_write_checksum_file__mutmut_28,
    "x_write_checksum_file__mutmut_29": x_write_checksum_file__mutmut_29,
    "x_write_checksum_file__mutmut_30": x_write_checksum_file__mutmut_30,
    "x_write_checksum_file__mutmut_31": x_write_checksum_file__mutmut_31,
    "x_write_checksum_file__mutmut_32": x_write_checksum_file__mutmut_32,
    "x_write_checksum_file__mutmut_33": x_write_checksum_file__mutmut_33,
    "x_write_checksum_file__mutmut_34": x_write_checksum_file__mutmut_34,
    "x_write_checksum_file__mutmut_35": x_write_checksum_file__mutmut_35,
    "x_write_checksum_file__mutmut_36": x_write_checksum_file__mutmut_36,
    "x_write_checksum_file__mutmut_37": x_write_checksum_file__mutmut_37,
    "x_write_checksum_file__mutmut_38": x_write_checksum_file__mutmut_38,
    "x_write_checksum_file__mutmut_39": x_write_checksum_file__mutmut_39,
    "x_write_checksum_file__mutmut_40": x_write_checksum_file__mutmut_40,
    "x_write_checksum_file__mutmut_41": x_write_checksum_file__mutmut_41,
    "x_write_checksum_file__mutmut_42": x_write_checksum_file__mutmut_42,
    "x_write_checksum_file__mutmut_43": x_write_checksum_file__mutmut_43,
    "x_write_checksum_file__mutmut_44": x_write_checksum_file__mutmut_44,
    "x_write_checksum_file__mutmut_45": x_write_checksum_file__mutmut_45,
    "x_write_checksum_file__mutmut_46": x_write_checksum_file__mutmut_46,
}


def write_checksum_file(*args, **kwargs):
    result = _mutmut_trampoline(
        x_write_checksum_file__mutmut_orig, x_write_checksum_file__mutmut_mutants, args, kwargs
    )
    return result


write_checksum_file.__signature__ = _mutmut_signature(x_write_checksum_file__mutmut_orig)
x_write_checksum_file__mutmut_orig.__name__ = "x_write_checksum_file"


def x_verify_checksum_file__mutmut_orig(
    checksum_file: Path | str,
    base_dir: Path | str | None = None,
    algorithm: str = DEFAULT_ALGORITHM,
    stop_on_error: bool = False,
) -> tuple[list[str], list[str]]:
    """Verify all files listed in a checksum file.

    Args:
        checksum_file: Path to checksum file
        base_dir: Base directory for relative paths (defaults to checksum file dir)
        algorithm: Hash algorithm to use
        stop_on_error: Whether to stop on first verification failure

    Returns:
        Tuple of (verified_files, failed_files)

    Raises:
        ResourceError: If checksum file cannot be read

    """
    if isinstance(checksum_file, str):
        checksum_file = Path(checksum_file)

    if base_dir is None:
        base_dir = checksum_file.parent
    elif isinstance(base_dir, str):
        base_dir = Path(base_dir)

    checksums = parse_checksum_file(checksum_file, algorithm)

    verified = []
    failed = []

    for filename, expected_hash in checksums.items():
        file_path = base_dir / filename

        if verify_file(file_path, expected_hash, algorithm):
            verified.append(filename)
        else:
            failed.append(filename)
            if stop_on_error:
                break

    log.info(
        "📊 Checksum verification complete",
        verified=len(verified),
        failed=len(failed),
        total=len(checksums),
    )

    return verified, failed


def x_verify_checksum_file__mutmut_1(
    checksum_file: Path | str,
    base_dir: Path | str | None = None,
    algorithm: str = DEFAULT_ALGORITHM,
    stop_on_error: bool = True,
) -> tuple[list[str], list[str]]:
    """Verify all files listed in a checksum file.

    Args:
        checksum_file: Path to checksum file
        base_dir: Base directory for relative paths (defaults to checksum file dir)
        algorithm: Hash algorithm to use
        stop_on_error: Whether to stop on first verification failure

    Returns:
        Tuple of (verified_files, failed_files)

    Raises:
        ResourceError: If checksum file cannot be read

    """
    if isinstance(checksum_file, str):
        checksum_file = Path(checksum_file)

    if base_dir is None:
        base_dir = checksum_file.parent
    elif isinstance(base_dir, str):
        base_dir = Path(base_dir)

    checksums = parse_checksum_file(checksum_file, algorithm)

    verified = []
    failed = []

    for filename, expected_hash in checksums.items():
        file_path = base_dir / filename

        if verify_file(file_path, expected_hash, algorithm):
            verified.append(filename)
        else:
            failed.append(filename)
            if stop_on_error:
                break

    log.info(
        "📊 Checksum verification complete",
        verified=len(verified),
        failed=len(failed),
        total=len(checksums),
    )

    return verified, failed


def x_verify_checksum_file__mutmut_2(
    checksum_file: Path | str,
    base_dir: Path | str | None = None,
    algorithm: str = DEFAULT_ALGORITHM,
    stop_on_error: bool = False,
) -> tuple[list[str], list[str]]:
    """Verify all files listed in a checksum file.

    Args:
        checksum_file: Path to checksum file
        base_dir: Base directory for relative paths (defaults to checksum file dir)
        algorithm: Hash algorithm to use
        stop_on_error: Whether to stop on first verification failure

    Returns:
        Tuple of (verified_files, failed_files)

    Raises:
        ResourceError: If checksum file cannot be read

    """
    if isinstance(checksum_file, str):
        checksum_file = None

    if base_dir is None:
        base_dir = checksum_file.parent
    elif isinstance(base_dir, str):
        base_dir = Path(base_dir)

    checksums = parse_checksum_file(checksum_file, algorithm)

    verified = []
    failed = []

    for filename, expected_hash in checksums.items():
        file_path = base_dir / filename

        if verify_file(file_path, expected_hash, algorithm):
            verified.append(filename)
        else:
            failed.append(filename)
            if stop_on_error:
                break

    log.info(
        "📊 Checksum verification complete",
        verified=len(verified),
        failed=len(failed),
        total=len(checksums),
    )

    return verified, failed


def x_verify_checksum_file__mutmut_3(
    checksum_file: Path | str,
    base_dir: Path | str | None = None,
    algorithm: str = DEFAULT_ALGORITHM,
    stop_on_error: bool = False,
) -> tuple[list[str], list[str]]:
    """Verify all files listed in a checksum file.

    Args:
        checksum_file: Path to checksum file
        base_dir: Base directory for relative paths (defaults to checksum file dir)
        algorithm: Hash algorithm to use
        stop_on_error: Whether to stop on first verification failure

    Returns:
        Tuple of (verified_files, failed_files)

    Raises:
        ResourceError: If checksum file cannot be read

    """
    if isinstance(checksum_file, str):
        checksum_file = Path(None)

    if base_dir is None:
        base_dir = checksum_file.parent
    elif isinstance(base_dir, str):
        base_dir = Path(base_dir)

    checksums = parse_checksum_file(checksum_file, algorithm)

    verified = []
    failed = []

    for filename, expected_hash in checksums.items():
        file_path = base_dir / filename

        if verify_file(file_path, expected_hash, algorithm):
            verified.append(filename)
        else:
            failed.append(filename)
            if stop_on_error:
                break

    log.info(
        "📊 Checksum verification complete",
        verified=len(verified),
        failed=len(failed),
        total=len(checksums),
    )

    return verified, failed


def x_verify_checksum_file__mutmut_4(
    checksum_file: Path | str,
    base_dir: Path | str | None = None,
    algorithm: str = DEFAULT_ALGORITHM,
    stop_on_error: bool = False,
) -> tuple[list[str], list[str]]:
    """Verify all files listed in a checksum file.

    Args:
        checksum_file: Path to checksum file
        base_dir: Base directory for relative paths (defaults to checksum file dir)
        algorithm: Hash algorithm to use
        stop_on_error: Whether to stop on first verification failure

    Returns:
        Tuple of (verified_files, failed_files)

    Raises:
        ResourceError: If checksum file cannot be read

    """
    if isinstance(checksum_file, str):
        checksum_file = Path(checksum_file)

    if base_dir is not None:
        base_dir = checksum_file.parent
    elif isinstance(base_dir, str):
        base_dir = Path(base_dir)

    checksums = parse_checksum_file(checksum_file, algorithm)

    verified = []
    failed = []

    for filename, expected_hash in checksums.items():
        file_path = base_dir / filename

        if verify_file(file_path, expected_hash, algorithm):
            verified.append(filename)
        else:
            failed.append(filename)
            if stop_on_error:
                break

    log.info(
        "📊 Checksum verification complete",
        verified=len(verified),
        failed=len(failed),
        total=len(checksums),
    )

    return verified, failed


def x_verify_checksum_file__mutmut_5(
    checksum_file: Path | str,
    base_dir: Path | str | None = None,
    algorithm: str = DEFAULT_ALGORITHM,
    stop_on_error: bool = False,
) -> tuple[list[str], list[str]]:
    """Verify all files listed in a checksum file.

    Args:
        checksum_file: Path to checksum file
        base_dir: Base directory for relative paths (defaults to checksum file dir)
        algorithm: Hash algorithm to use
        stop_on_error: Whether to stop on first verification failure

    Returns:
        Tuple of (verified_files, failed_files)

    Raises:
        ResourceError: If checksum file cannot be read

    """
    if isinstance(checksum_file, str):
        checksum_file = Path(checksum_file)

    if base_dir is None:
        base_dir = None
    elif isinstance(base_dir, str):
        base_dir = Path(base_dir)

    checksums = parse_checksum_file(checksum_file, algorithm)

    verified = []
    failed = []

    for filename, expected_hash in checksums.items():
        file_path = base_dir / filename

        if verify_file(file_path, expected_hash, algorithm):
            verified.append(filename)
        else:
            failed.append(filename)
            if stop_on_error:
                break

    log.info(
        "📊 Checksum verification complete",
        verified=len(verified),
        failed=len(failed),
        total=len(checksums),
    )

    return verified, failed


def x_verify_checksum_file__mutmut_6(
    checksum_file: Path | str,
    base_dir: Path | str | None = None,
    algorithm: str = DEFAULT_ALGORITHM,
    stop_on_error: bool = False,
) -> tuple[list[str], list[str]]:
    """Verify all files listed in a checksum file.

    Args:
        checksum_file: Path to checksum file
        base_dir: Base directory for relative paths (defaults to checksum file dir)
        algorithm: Hash algorithm to use
        stop_on_error: Whether to stop on first verification failure

    Returns:
        Tuple of (verified_files, failed_files)

    Raises:
        ResourceError: If checksum file cannot be read

    """
    if isinstance(checksum_file, str):
        checksum_file = Path(checksum_file)

    if base_dir is None:
        base_dir = checksum_file.parent
    elif isinstance(base_dir, str):
        base_dir = None

    checksums = parse_checksum_file(checksum_file, algorithm)

    verified = []
    failed = []

    for filename, expected_hash in checksums.items():
        file_path = base_dir / filename

        if verify_file(file_path, expected_hash, algorithm):
            verified.append(filename)
        else:
            failed.append(filename)
            if stop_on_error:
                break

    log.info(
        "📊 Checksum verification complete",
        verified=len(verified),
        failed=len(failed),
        total=len(checksums),
    )

    return verified, failed


def x_verify_checksum_file__mutmut_7(
    checksum_file: Path | str,
    base_dir: Path | str | None = None,
    algorithm: str = DEFAULT_ALGORITHM,
    stop_on_error: bool = False,
) -> tuple[list[str], list[str]]:
    """Verify all files listed in a checksum file.

    Args:
        checksum_file: Path to checksum file
        base_dir: Base directory for relative paths (defaults to checksum file dir)
        algorithm: Hash algorithm to use
        stop_on_error: Whether to stop on first verification failure

    Returns:
        Tuple of (verified_files, failed_files)

    Raises:
        ResourceError: If checksum file cannot be read

    """
    if isinstance(checksum_file, str):
        checksum_file = Path(checksum_file)

    if base_dir is None:
        base_dir = checksum_file.parent
    elif isinstance(base_dir, str):
        base_dir = Path(None)

    checksums = parse_checksum_file(checksum_file, algorithm)

    verified = []
    failed = []

    for filename, expected_hash in checksums.items():
        file_path = base_dir / filename

        if verify_file(file_path, expected_hash, algorithm):
            verified.append(filename)
        else:
            failed.append(filename)
            if stop_on_error:
                break

    log.info(
        "📊 Checksum verification complete",
        verified=len(verified),
        failed=len(failed),
        total=len(checksums),
    )

    return verified, failed


def x_verify_checksum_file__mutmut_8(
    checksum_file: Path | str,
    base_dir: Path | str | None = None,
    algorithm: str = DEFAULT_ALGORITHM,
    stop_on_error: bool = False,
) -> tuple[list[str], list[str]]:
    """Verify all files listed in a checksum file.

    Args:
        checksum_file: Path to checksum file
        base_dir: Base directory for relative paths (defaults to checksum file dir)
        algorithm: Hash algorithm to use
        stop_on_error: Whether to stop on first verification failure

    Returns:
        Tuple of (verified_files, failed_files)

    Raises:
        ResourceError: If checksum file cannot be read

    """
    if isinstance(checksum_file, str):
        checksum_file = Path(checksum_file)

    if base_dir is None:
        base_dir = checksum_file.parent
    elif isinstance(base_dir, str):
        base_dir = Path(base_dir)

    checksums = None

    verified = []
    failed = []

    for filename, expected_hash in checksums.items():
        file_path = base_dir / filename

        if verify_file(file_path, expected_hash, algorithm):
            verified.append(filename)
        else:
            failed.append(filename)
            if stop_on_error:
                break

    log.info(
        "📊 Checksum verification complete",
        verified=len(verified),
        failed=len(failed),
        total=len(checksums),
    )

    return verified, failed


def x_verify_checksum_file__mutmut_9(
    checksum_file: Path | str,
    base_dir: Path | str | None = None,
    algorithm: str = DEFAULT_ALGORITHM,
    stop_on_error: bool = False,
) -> tuple[list[str], list[str]]:
    """Verify all files listed in a checksum file.

    Args:
        checksum_file: Path to checksum file
        base_dir: Base directory for relative paths (defaults to checksum file dir)
        algorithm: Hash algorithm to use
        stop_on_error: Whether to stop on first verification failure

    Returns:
        Tuple of (verified_files, failed_files)

    Raises:
        ResourceError: If checksum file cannot be read

    """
    if isinstance(checksum_file, str):
        checksum_file = Path(checksum_file)

    if base_dir is None:
        base_dir = checksum_file.parent
    elif isinstance(base_dir, str):
        base_dir = Path(base_dir)

    checksums = parse_checksum_file(None, algorithm)

    verified = []
    failed = []

    for filename, expected_hash in checksums.items():
        file_path = base_dir / filename

        if verify_file(file_path, expected_hash, algorithm):
            verified.append(filename)
        else:
            failed.append(filename)
            if stop_on_error:
                break

    log.info(
        "📊 Checksum verification complete",
        verified=len(verified),
        failed=len(failed),
        total=len(checksums),
    )

    return verified, failed


def x_verify_checksum_file__mutmut_10(
    checksum_file: Path | str,
    base_dir: Path | str | None = None,
    algorithm: str = DEFAULT_ALGORITHM,
    stop_on_error: bool = False,
) -> tuple[list[str], list[str]]:
    """Verify all files listed in a checksum file.

    Args:
        checksum_file: Path to checksum file
        base_dir: Base directory for relative paths (defaults to checksum file dir)
        algorithm: Hash algorithm to use
        stop_on_error: Whether to stop on first verification failure

    Returns:
        Tuple of (verified_files, failed_files)

    Raises:
        ResourceError: If checksum file cannot be read

    """
    if isinstance(checksum_file, str):
        checksum_file = Path(checksum_file)

    if base_dir is None:
        base_dir = checksum_file.parent
    elif isinstance(base_dir, str):
        base_dir = Path(base_dir)

    checksums = parse_checksum_file(checksum_file, None)

    verified = []
    failed = []

    for filename, expected_hash in checksums.items():
        file_path = base_dir / filename

        if verify_file(file_path, expected_hash, algorithm):
            verified.append(filename)
        else:
            failed.append(filename)
            if stop_on_error:
                break

    log.info(
        "📊 Checksum verification complete",
        verified=len(verified),
        failed=len(failed),
        total=len(checksums),
    )

    return verified, failed


def x_verify_checksum_file__mutmut_11(
    checksum_file: Path | str,
    base_dir: Path | str | None = None,
    algorithm: str = DEFAULT_ALGORITHM,
    stop_on_error: bool = False,
) -> tuple[list[str], list[str]]:
    """Verify all files listed in a checksum file.

    Args:
        checksum_file: Path to checksum file
        base_dir: Base directory for relative paths (defaults to checksum file dir)
        algorithm: Hash algorithm to use
        stop_on_error: Whether to stop on first verification failure

    Returns:
        Tuple of (verified_files, failed_files)

    Raises:
        ResourceError: If checksum file cannot be read

    """
    if isinstance(checksum_file, str):
        checksum_file = Path(checksum_file)

    if base_dir is None:
        base_dir = checksum_file.parent
    elif isinstance(base_dir, str):
        base_dir = Path(base_dir)

    checksums = parse_checksum_file(algorithm)

    verified = []
    failed = []

    for filename, expected_hash in checksums.items():
        file_path = base_dir / filename

        if verify_file(file_path, expected_hash, algorithm):
            verified.append(filename)
        else:
            failed.append(filename)
            if stop_on_error:
                break

    log.info(
        "📊 Checksum verification complete",
        verified=len(verified),
        failed=len(failed),
        total=len(checksums),
    )

    return verified, failed


def x_verify_checksum_file__mutmut_12(
    checksum_file: Path | str,
    base_dir: Path | str | None = None,
    algorithm: str = DEFAULT_ALGORITHM,
    stop_on_error: bool = False,
) -> tuple[list[str], list[str]]:
    """Verify all files listed in a checksum file.

    Args:
        checksum_file: Path to checksum file
        base_dir: Base directory for relative paths (defaults to checksum file dir)
        algorithm: Hash algorithm to use
        stop_on_error: Whether to stop on first verification failure

    Returns:
        Tuple of (verified_files, failed_files)

    Raises:
        ResourceError: If checksum file cannot be read

    """
    if isinstance(checksum_file, str):
        checksum_file = Path(checksum_file)

    if base_dir is None:
        base_dir = checksum_file.parent
    elif isinstance(base_dir, str):
        base_dir = Path(base_dir)

    checksums = parse_checksum_file(
        checksum_file,
    )

    verified = []
    failed = []

    for filename, expected_hash in checksums.items():
        file_path = base_dir / filename

        if verify_file(file_path, expected_hash, algorithm):
            verified.append(filename)
        else:
            failed.append(filename)
            if stop_on_error:
                break

    log.info(
        "📊 Checksum verification complete",
        verified=len(verified),
        failed=len(failed),
        total=len(checksums),
    )

    return verified, failed


def x_verify_checksum_file__mutmut_13(
    checksum_file: Path | str,
    base_dir: Path | str | None = None,
    algorithm: str = DEFAULT_ALGORITHM,
    stop_on_error: bool = False,
) -> tuple[list[str], list[str]]:
    """Verify all files listed in a checksum file.

    Args:
        checksum_file: Path to checksum file
        base_dir: Base directory for relative paths (defaults to checksum file dir)
        algorithm: Hash algorithm to use
        stop_on_error: Whether to stop on first verification failure

    Returns:
        Tuple of (verified_files, failed_files)

    Raises:
        ResourceError: If checksum file cannot be read

    """
    if isinstance(checksum_file, str):
        checksum_file = Path(checksum_file)

    if base_dir is None:
        base_dir = checksum_file.parent
    elif isinstance(base_dir, str):
        base_dir = Path(base_dir)

    checksums = parse_checksum_file(checksum_file, algorithm)

    verified = None
    failed = []

    for filename, expected_hash in checksums.items():
        file_path = base_dir / filename

        if verify_file(file_path, expected_hash, algorithm):
            verified.append(filename)
        else:
            failed.append(filename)
            if stop_on_error:
                break

    log.info(
        "📊 Checksum verification complete",
        verified=len(verified),
        failed=len(failed),
        total=len(checksums),
    )

    return verified, failed


def x_verify_checksum_file__mutmut_14(
    checksum_file: Path | str,
    base_dir: Path | str | None = None,
    algorithm: str = DEFAULT_ALGORITHM,
    stop_on_error: bool = False,
) -> tuple[list[str], list[str]]:
    """Verify all files listed in a checksum file.

    Args:
        checksum_file: Path to checksum file
        base_dir: Base directory for relative paths (defaults to checksum file dir)
        algorithm: Hash algorithm to use
        stop_on_error: Whether to stop on first verification failure

    Returns:
        Tuple of (verified_files, failed_files)

    Raises:
        ResourceError: If checksum file cannot be read

    """
    if isinstance(checksum_file, str):
        checksum_file = Path(checksum_file)

    if base_dir is None:
        base_dir = checksum_file.parent
    elif isinstance(base_dir, str):
        base_dir = Path(base_dir)

    checksums = parse_checksum_file(checksum_file, algorithm)

    verified = []
    failed = None

    for filename, expected_hash in checksums.items():
        file_path = base_dir / filename

        if verify_file(file_path, expected_hash, algorithm):
            verified.append(filename)
        else:
            failed.append(filename)
            if stop_on_error:
                break

    log.info(
        "📊 Checksum verification complete",
        verified=len(verified),
        failed=len(failed),
        total=len(checksums),
    )

    return verified, failed


def x_verify_checksum_file__mutmut_15(
    checksum_file: Path | str,
    base_dir: Path | str | None = None,
    algorithm: str = DEFAULT_ALGORITHM,
    stop_on_error: bool = False,
) -> tuple[list[str], list[str]]:
    """Verify all files listed in a checksum file.

    Args:
        checksum_file: Path to checksum file
        base_dir: Base directory for relative paths (defaults to checksum file dir)
        algorithm: Hash algorithm to use
        stop_on_error: Whether to stop on first verification failure

    Returns:
        Tuple of (verified_files, failed_files)

    Raises:
        ResourceError: If checksum file cannot be read

    """
    if isinstance(checksum_file, str):
        checksum_file = Path(checksum_file)

    if base_dir is None:
        base_dir = checksum_file.parent
    elif isinstance(base_dir, str):
        base_dir = Path(base_dir)

    checksums = parse_checksum_file(checksum_file, algorithm)

    verified = []
    failed = []

    for filename, expected_hash in checksums.items():
        file_path = None

        if verify_file(file_path, expected_hash, algorithm):
            verified.append(filename)
        else:
            failed.append(filename)
            if stop_on_error:
                break

    log.info(
        "📊 Checksum verification complete",
        verified=len(verified),
        failed=len(failed),
        total=len(checksums),
    )

    return verified, failed


def x_verify_checksum_file__mutmut_16(
    checksum_file: Path | str,
    base_dir: Path | str | None = None,
    algorithm: str = DEFAULT_ALGORITHM,
    stop_on_error: bool = False,
) -> tuple[list[str], list[str]]:
    """Verify all files listed in a checksum file.

    Args:
        checksum_file: Path to checksum file
        base_dir: Base directory for relative paths (defaults to checksum file dir)
        algorithm: Hash algorithm to use
        stop_on_error: Whether to stop on first verification failure

    Returns:
        Tuple of (verified_files, failed_files)

    Raises:
        ResourceError: If checksum file cannot be read

    """
    if isinstance(checksum_file, str):
        checksum_file = Path(checksum_file)

    if base_dir is None:
        base_dir = checksum_file.parent
    elif isinstance(base_dir, str):
        base_dir = Path(base_dir)

    checksums = parse_checksum_file(checksum_file, algorithm)

    verified = []
    failed = []

    for filename, expected_hash in checksums.items():
        file_path = base_dir * filename

        if verify_file(file_path, expected_hash, algorithm):
            verified.append(filename)
        else:
            failed.append(filename)
            if stop_on_error:
                break

    log.info(
        "📊 Checksum verification complete",
        verified=len(verified),
        failed=len(failed),
        total=len(checksums),
    )

    return verified, failed


def x_verify_checksum_file__mutmut_17(
    checksum_file: Path | str,
    base_dir: Path | str | None = None,
    algorithm: str = DEFAULT_ALGORITHM,
    stop_on_error: bool = False,
) -> tuple[list[str], list[str]]:
    """Verify all files listed in a checksum file.

    Args:
        checksum_file: Path to checksum file
        base_dir: Base directory for relative paths (defaults to checksum file dir)
        algorithm: Hash algorithm to use
        stop_on_error: Whether to stop on first verification failure

    Returns:
        Tuple of (verified_files, failed_files)

    Raises:
        ResourceError: If checksum file cannot be read

    """
    if isinstance(checksum_file, str):
        checksum_file = Path(checksum_file)

    if base_dir is None:
        base_dir = checksum_file.parent
    elif isinstance(base_dir, str):
        base_dir = Path(base_dir)

    checksums = parse_checksum_file(checksum_file, algorithm)

    verified = []
    failed = []

    for filename, expected_hash in checksums.items():
        file_path = base_dir / filename

        if verify_file(None, expected_hash, algorithm):
            verified.append(filename)
        else:
            failed.append(filename)
            if stop_on_error:
                break

    log.info(
        "📊 Checksum verification complete",
        verified=len(verified),
        failed=len(failed),
        total=len(checksums),
    )

    return verified, failed


def x_verify_checksum_file__mutmut_18(
    checksum_file: Path | str,
    base_dir: Path | str | None = None,
    algorithm: str = DEFAULT_ALGORITHM,
    stop_on_error: bool = False,
) -> tuple[list[str], list[str]]:
    """Verify all files listed in a checksum file.

    Args:
        checksum_file: Path to checksum file
        base_dir: Base directory for relative paths (defaults to checksum file dir)
        algorithm: Hash algorithm to use
        stop_on_error: Whether to stop on first verification failure

    Returns:
        Tuple of (verified_files, failed_files)

    Raises:
        ResourceError: If checksum file cannot be read

    """
    if isinstance(checksum_file, str):
        checksum_file = Path(checksum_file)

    if base_dir is None:
        base_dir = checksum_file.parent
    elif isinstance(base_dir, str):
        base_dir = Path(base_dir)

    checksums = parse_checksum_file(checksum_file, algorithm)

    verified = []
    failed = []

    for filename, expected_hash in checksums.items():
        file_path = base_dir / filename

        if verify_file(file_path, None, algorithm):
            verified.append(filename)
        else:
            failed.append(filename)
            if stop_on_error:
                break

    log.info(
        "📊 Checksum verification complete",
        verified=len(verified),
        failed=len(failed),
        total=len(checksums),
    )

    return verified, failed


def x_verify_checksum_file__mutmut_19(
    checksum_file: Path | str,
    base_dir: Path | str | None = None,
    algorithm: str = DEFAULT_ALGORITHM,
    stop_on_error: bool = False,
) -> tuple[list[str], list[str]]:
    """Verify all files listed in a checksum file.

    Args:
        checksum_file: Path to checksum file
        base_dir: Base directory for relative paths (defaults to checksum file dir)
        algorithm: Hash algorithm to use
        stop_on_error: Whether to stop on first verification failure

    Returns:
        Tuple of (verified_files, failed_files)

    Raises:
        ResourceError: If checksum file cannot be read

    """
    if isinstance(checksum_file, str):
        checksum_file = Path(checksum_file)

    if base_dir is None:
        base_dir = checksum_file.parent
    elif isinstance(base_dir, str):
        base_dir = Path(base_dir)

    checksums = parse_checksum_file(checksum_file, algorithm)

    verified = []
    failed = []

    for filename, expected_hash in checksums.items():
        file_path = base_dir / filename

        if verify_file(file_path, expected_hash, None):
            verified.append(filename)
        else:
            failed.append(filename)
            if stop_on_error:
                break

    log.info(
        "📊 Checksum verification complete",
        verified=len(verified),
        failed=len(failed),
        total=len(checksums),
    )

    return verified, failed


def x_verify_checksum_file__mutmut_20(
    checksum_file: Path | str,
    base_dir: Path | str | None = None,
    algorithm: str = DEFAULT_ALGORITHM,
    stop_on_error: bool = False,
) -> tuple[list[str], list[str]]:
    """Verify all files listed in a checksum file.

    Args:
        checksum_file: Path to checksum file
        base_dir: Base directory for relative paths (defaults to checksum file dir)
        algorithm: Hash algorithm to use
        stop_on_error: Whether to stop on first verification failure

    Returns:
        Tuple of (verified_files, failed_files)

    Raises:
        ResourceError: If checksum file cannot be read

    """
    if isinstance(checksum_file, str):
        checksum_file = Path(checksum_file)

    if base_dir is None:
        base_dir = checksum_file.parent
    elif isinstance(base_dir, str):
        base_dir = Path(base_dir)

    checksums = parse_checksum_file(checksum_file, algorithm)

    verified = []
    failed = []

    for filename, expected_hash in checksums.items():
        file_path = base_dir / filename

        if verify_file(expected_hash, algorithm):
            verified.append(filename)
        else:
            failed.append(filename)
            if stop_on_error:
                break

    log.info(
        "📊 Checksum verification complete",
        verified=len(verified),
        failed=len(failed),
        total=len(checksums),
    )

    return verified, failed


def x_verify_checksum_file__mutmut_21(
    checksum_file: Path | str,
    base_dir: Path | str | None = None,
    algorithm: str = DEFAULT_ALGORITHM,
    stop_on_error: bool = False,
) -> tuple[list[str], list[str]]:
    """Verify all files listed in a checksum file.

    Args:
        checksum_file: Path to checksum file
        base_dir: Base directory for relative paths (defaults to checksum file dir)
        algorithm: Hash algorithm to use
        stop_on_error: Whether to stop on first verification failure

    Returns:
        Tuple of (verified_files, failed_files)

    Raises:
        ResourceError: If checksum file cannot be read

    """
    if isinstance(checksum_file, str):
        checksum_file = Path(checksum_file)

    if base_dir is None:
        base_dir = checksum_file.parent
    elif isinstance(base_dir, str):
        base_dir = Path(base_dir)

    checksums = parse_checksum_file(checksum_file, algorithm)

    verified = []
    failed = []

    for filename, expected_hash in checksums.items():
        file_path = base_dir / filename

        if verify_file(file_path, algorithm):
            verified.append(filename)
        else:
            failed.append(filename)
            if stop_on_error:
                break

    log.info(
        "📊 Checksum verification complete",
        verified=len(verified),
        failed=len(failed),
        total=len(checksums),
    )

    return verified, failed


def x_verify_checksum_file__mutmut_22(
    checksum_file: Path | str,
    base_dir: Path | str | None = None,
    algorithm: str = DEFAULT_ALGORITHM,
    stop_on_error: bool = False,
) -> tuple[list[str], list[str]]:
    """Verify all files listed in a checksum file.

    Args:
        checksum_file: Path to checksum file
        base_dir: Base directory for relative paths (defaults to checksum file dir)
        algorithm: Hash algorithm to use
        stop_on_error: Whether to stop on first verification failure

    Returns:
        Tuple of (verified_files, failed_files)

    Raises:
        ResourceError: If checksum file cannot be read

    """
    if isinstance(checksum_file, str):
        checksum_file = Path(checksum_file)

    if base_dir is None:
        base_dir = checksum_file.parent
    elif isinstance(base_dir, str):
        base_dir = Path(base_dir)

    checksums = parse_checksum_file(checksum_file, algorithm)

    verified = []
    failed = []

    for filename, expected_hash in checksums.items():
        file_path = base_dir / filename

        if verify_file(
            file_path,
            expected_hash,
        ):
            verified.append(filename)
        else:
            failed.append(filename)
            if stop_on_error:
                break

    log.info(
        "📊 Checksum verification complete",
        verified=len(verified),
        failed=len(failed),
        total=len(checksums),
    )

    return verified, failed


def x_verify_checksum_file__mutmut_23(
    checksum_file: Path | str,
    base_dir: Path | str | None = None,
    algorithm: str = DEFAULT_ALGORITHM,
    stop_on_error: bool = False,
) -> tuple[list[str], list[str]]:
    """Verify all files listed in a checksum file.

    Args:
        checksum_file: Path to checksum file
        base_dir: Base directory for relative paths (defaults to checksum file dir)
        algorithm: Hash algorithm to use
        stop_on_error: Whether to stop on first verification failure

    Returns:
        Tuple of (verified_files, failed_files)

    Raises:
        ResourceError: If checksum file cannot be read

    """
    if isinstance(checksum_file, str):
        checksum_file = Path(checksum_file)

    if base_dir is None:
        base_dir = checksum_file.parent
    elif isinstance(base_dir, str):
        base_dir = Path(base_dir)

    checksums = parse_checksum_file(checksum_file, algorithm)

    verified = []
    failed = []

    for filename, expected_hash in checksums.items():
        file_path = base_dir / filename

        if verify_file(file_path, expected_hash, algorithm):
            verified.append(None)
        else:
            failed.append(filename)
            if stop_on_error:
                break

    log.info(
        "📊 Checksum verification complete",
        verified=len(verified),
        failed=len(failed),
        total=len(checksums),
    )

    return verified, failed


def x_verify_checksum_file__mutmut_24(
    checksum_file: Path | str,
    base_dir: Path | str | None = None,
    algorithm: str = DEFAULT_ALGORITHM,
    stop_on_error: bool = False,
) -> tuple[list[str], list[str]]:
    """Verify all files listed in a checksum file.

    Args:
        checksum_file: Path to checksum file
        base_dir: Base directory for relative paths (defaults to checksum file dir)
        algorithm: Hash algorithm to use
        stop_on_error: Whether to stop on first verification failure

    Returns:
        Tuple of (verified_files, failed_files)

    Raises:
        ResourceError: If checksum file cannot be read

    """
    if isinstance(checksum_file, str):
        checksum_file = Path(checksum_file)

    if base_dir is None:
        base_dir = checksum_file.parent
    elif isinstance(base_dir, str):
        base_dir = Path(base_dir)

    checksums = parse_checksum_file(checksum_file, algorithm)

    verified = []
    failed = []

    for filename, expected_hash in checksums.items():
        file_path = base_dir / filename

        if verify_file(file_path, expected_hash, algorithm):
            verified.append(filename)
        else:
            failed.append(None)
            if stop_on_error:
                break

    log.info(
        "📊 Checksum verification complete",
        verified=len(verified),
        failed=len(failed),
        total=len(checksums),
    )

    return verified, failed


def x_verify_checksum_file__mutmut_25(
    checksum_file: Path | str,
    base_dir: Path | str | None = None,
    algorithm: str = DEFAULT_ALGORITHM,
    stop_on_error: bool = False,
) -> tuple[list[str], list[str]]:
    """Verify all files listed in a checksum file.

    Args:
        checksum_file: Path to checksum file
        base_dir: Base directory for relative paths (defaults to checksum file dir)
        algorithm: Hash algorithm to use
        stop_on_error: Whether to stop on first verification failure

    Returns:
        Tuple of (verified_files, failed_files)

    Raises:
        ResourceError: If checksum file cannot be read

    """
    if isinstance(checksum_file, str):
        checksum_file = Path(checksum_file)

    if base_dir is None:
        base_dir = checksum_file.parent
    elif isinstance(base_dir, str):
        base_dir = Path(base_dir)

    checksums = parse_checksum_file(checksum_file, algorithm)

    verified = []
    failed = []

    for filename, expected_hash in checksums.items():
        file_path = base_dir / filename

        if verify_file(file_path, expected_hash, algorithm):
            verified.append(filename)
        else:
            failed.append(filename)
            if stop_on_error:
                return

    log.info(
        "📊 Checksum verification complete",
        verified=len(verified),
        failed=len(failed),
        total=len(checksums),
    )

    return verified, failed


def x_verify_checksum_file__mutmut_26(
    checksum_file: Path | str,
    base_dir: Path | str | None = None,
    algorithm: str = DEFAULT_ALGORITHM,
    stop_on_error: bool = False,
) -> tuple[list[str], list[str]]:
    """Verify all files listed in a checksum file.

    Args:
        checksum_file: Path to checksum file
        base_dir: Base directory for relative paths (defaults to checksum file dir)
        algorithm: Hash algorithm to use
        stop_on_error: Whether to stop on first verification failure

    Returns:
        Tuple of (verified_files, failed_files)

    Raises:
        ResourceError: If checksum file cannot be read

    """
    if isinstance(checksum_file, str):
        checksum_file = Path(checksum_file)

    if base_dir is None:
        base_dir = checksum_file.parent
    elif isinstance(base_dir, str):
        base_dir = Path(base_dir)

    checksums = parse_checksum_file(checksum_file, algorithm)

    verified = []
    failed = []

    for filename, expected_hash in checksums.items():
        file_path = base_dir / filename

        if verify_file(file_path, expected_hash, algorithm):
            verified.append(filename)
        else:
            failed.append(filename)
            if stop_on_error:
                break

    log.info(
        None,
        verified=len(verified),
        failed=len(failed),
        total=len(checksums),
    )

    return verified, failed


def x_verify_checksum_file__mutmut_27(
    checksum_file: Path | str,
    base_dir: Path | str | None = None,
    algorithm: str = DEFAULT_ALGORITHM,
    stop_on_error: bool = False,
) -> tuple[list[str], list[str]]:
    """Verify all files listed in a checksum file.

    Args:
        checksum_file: Path to checksum file
        base_dir: Base directory for relative paths (defaults to checksum file dir)
        algorithm: Hash algorithm to use
        stop_on_error: Whether to stop on first verification failure

    Returns:
        Tuple of (verified_files, failed_files)

    Raises:
        ResourceError: If checksum file cannot be read

    """
    if isinstance(checksum_file, str):
        checksum_file = Path(checksum_file)

    if base_dir is None:
        base_dir = checksum_file.parent
    elif isinstance(base_dir, str):
        base_dir = Path(base_dir)

    checksums = parse_checksum_file(checksum_file, algorithm)

    verified = []
    failed = []

    for filename, expected_hash in checksums.items():
        file_path = base_dir / filename

        if verify_file(file_path, expected_hash, algorithm):
            verified.append(filename)
        else:
            failed.append(filename)
            if stop_on_error:
                break

    log.info(
        "📊 Checksum verification complete",
        verified=None,
        failed=len(failed),
        total=len(checksums),
    )

    return verified, failed


def x_verify_checksum_file__mutmut_28(
    checksum_file: Path | str,
    base_dir: Path | str | None = None,
    algorithm: str = DEFAULT_ALGORITHM,
    stop_on_error: bool = False,
) -> tuple[list[str], list[str]]:
    """Verify all files listed in a checksum file.

    Args:
        checksum_file: Path to checksum file
        base_dir: Base directory for relative paths (defaults to checksum file dir)
        algorithm: Hash algorithm to use
        stop_on_error: Whether to stop on first verification failure

    Returns:
        Tuple of (verified_files, failed_files)

    Raises:
        ResourceError: If checksum file cannot be read

    """
    if isinstance(checksum_file, str):
        checksum_file = Path(checksum_file)

    if base_dir is None:
        base_dir = checksum_file.parent
    elif isinstance(base_dir, str):
        base_dir = Path(base_dir)

    checksums = parse_checksum_file(checksum_file, algorithm)

    verified = []
    failed = []

    for filename, expected_hash in checksums.items():
        file_path = base_dir / filename

        if verify_file(file_path, expected_hash, algorithm):
            verified.append(filename)
        else:
            failed.append(filename)
            if stop_on_error:
                break

    log.info(
        "📊 Checksum verification complete",
        verified=len(verified),
        failed=None,
        total=len(checksums),
    )

    return verified, failed


def x_verify_checksum_file__mutmut_29(
    checksum_file: Path | str,
    base_dir: Path | str | None = None,
    algorithm: str = DEFAULT_ALGORITHM,
    stop_on_error: bool = False,
) -> tuple[list[str], list[str]]:
    """Verify all files listed in a checksum file.

    Args:
        checksum_file: Path to checksum file
        base_dir: Base directory for relative paths (defaults to checksum file dir)
        algorithm: Hash algorithm to use
        stop_on_error: Whether to stop on first verification failure

    Returns:
        Tuple of (verified_files, failed_files)

    Raises:
        ResourceError: If checksum file cannot be read

    """
    if isinstance(checksum_file, str):
        checksum_file = Path(checksum_file)

    if base_dir is None:
        base_dir = checksum_file.parent
    elif isinstance(base_dir, str):
        base_dir = Path(base_dir)

    checksums = parse_checksum_file(checksum_file, algorithm)

    verified = []
    failed = []

    for filename, expected_hash in checksums.items():
        file_path = base_dir / filename

        if verify_file(file_path, expected_hash, algorithm):
            verified.append(filename)
        else:
            failed.append(filename)
            if stop_on_error:
                break

    log.info(
        "📊 Checksum verification complete",
        verified=len(verified),
        failed=len(failed),
        total=None,
    )

    return verified, failed


def x_verify_checksum_file__mutmut_30(
    checksum_file: Path | str,
    base_dir: Path | str | None = None,
    algorithm: str = DEFAULT_ALGORITHM,
    stop_on_error: bool = False,
) -> tuple[list[str], list[str]]:
    """Verify all files listed in a checksum file.

    Args:
        checksum_file: Path to checksum file
        base_dir: Base directory for relative paths (defaults to checksum file dir)
        algorithm: Hash algorithm to use
        stop_on_error: Whether to stop on first verification failure

    Returns:
        Tuple of (verified_files, failed_files)

    Raises:
        ResourceError: If checksum file cannot be read

    """
    if isinstance(checksum_file, str):
        checksum_file = Path(checksum_file)

    if base_dir is None:
        base_dir = checksum_file.parent
    elif isinstance(base_dir, str):
        base_dir = Path(base_dir)

    checksums = parse_checksum_file(checksum_file, algorithm)

    verified = []
    failed = []

    for filename, expected_hash in checksums.items():
        file_path = base_dir / filename

        if verify_file(file_path, expected_hash, algorithm):
            verified.append(filename)
        else:
            failed.append(filename)
            if stop_on_error:
                break

    log.info(
        verified=len(verified),
        failed=len(failed),
        total=len(checksums),
    )

    return verified, failed


def x_verify_checksum_file__mutmut_31(
    checksum_file: Path | str,
    base_dir: Path | str | None = None,
    algorithm: str = DEFAULT_ALGORITHM,
    stop_on_error: bool = False,
) -> tuple[list[str], list[str]]:
    """Verify all files listed in a checksum file.

    Args:
        checksum_file: Path to checksum file
        base_dir: Base directory for relative paths (defaults to checksum file dir)
        algorithm: Hash algorithm to use
        stop_on_error: Whether to stop on first verification failure

    Returns:
        Tuple of (verified_files, failed_files)

    Raises:
        ResourceError: If checksum file cannot be read

    """
    if isinstance(checksum_file, str):
        checksum_file = Path(checksum_file)

    if base_dir is None:
        base_dir = checksum_file.parent
    elif isinstance(base_dir, str):
        base_dir = Path(base_dir)

    checksums = parse_checksum_file(checksum_file, algorithm)

    verified = []
    failed = []

    for filename, expected_hash in checksums.items():
        file_path = base_dir / filename

        if verify_file(file_path, expected_hash, algorithm):
            verified.append(filename)
        else:
            failed.append(filename)
            if stop_on_error:
                break

    log.info(
        "📊 Checksum verification complete",
        failed=len(failed),
        total=len(checksums),
    )

    return verified, failed


def x_verify_checksum_file__mutmut_32(
    checksum_file: Path | str,
    base_dir: Path | str | None = None,
    algorithm: str = DEFAULT_ALGORITHM,
    stop_on_error: bool = False,
) -> tuple[list[str], list[str]]:
    """Verify all files listed in a checksum file.

    Args:
        checksum_file: Path to checksum file
        base_dir: Base directory for relative paths (defaults to checksum file dir)
        algorithm: Hash algorithm to use
        stop_on_error: Whether to stop on first verification failure

    Returns:
        Tuple of (verified_files, failed_files)

    Raises:
        ResourceError: If checksum file cannot be read

    """
    if isinstance(checksum_file, str):
        checksum_file = Path(checksum_file)

    if base_dir is None:
        base_dir = checksum_file.parent
    elif isinstance(base_dir, str):
        base_dir = Path(base_dir)

    checksums = parse_checksum_file(checksum_file, algorithm)

    verified = []
    failed = []

    for filename, expected_hash in checksums.items():
        file_path = base_dir / filename

        if verify_file(file_path, expected_hash, algorithm):
            verified.append(filename)
        else:
            failed.append(filename)
            if stop_on_error:
                break

    log.info(
        "📊 Checksum verification complete",
        verified=len(verified),
        total=len(checksums),
    )

    return verified, failed


def x_verify_checksum_file__mutmut_33(
    checksum_file: Path | str,
    base_dir: Path | str | None = None,
    algorithm: str = DEFAULT_ALGORITHM,
    stop_on_error: bool = False,
) -> tuple[list[str], list[str]]:
    """Verify all files listed in a checksum file.

    Args:
        checksum_file: Path to checksum file
        base_dir: Base directory for relative paths (defaults to checksum file dir)
        algorithm: Hash algorithm to use
        stop_on_error: Whether to stop on first verification failure

    Returns:
        Tuple of (verified_files, failed_files)

    Raises:
        ResourceError: If checksum file cannot be read

    """
    if isinstance(checksum_file, str):
        checksum_file = Path(checksum_file)

    if base_dir is None:
        base_dir = checksum_file.parent
    elif isinstance(base_dir, str):
        base_dir = Path(base_dir)

    checksums = parse_checksum_file(checksum_file, algorithm)

    verified = []
    failed = []

    for filename, expected_hash in checksums.items():
        file_path = base_dir / filename

        if verify_file(file_path, expected_hash, algorithm):
            verified.append(filename)
        else:
            failed.append(filename)
            if stop_on_error:
                break

    log.info(
        "📊 Checksum verification complete",
        verified=len(verified),
        failed=len(failed),
    )

    return verified, failed


def x_verify_checksum_file__mutmut_34(
    checksum_file: Path | str,
    base_dir: Path | str | None = None,
    algorithm: str = DEFAULT_ALGORITHM,
    stop_on_error: bool = False,
) -> tuple[list[str], list[str]]:
    """Verify all files listed in a checksum file.

    Args:
        checksum_file: Path to checksum file
        base_dir: Base directory for relative paths (defaults to checksum file dir)
        algorithm: Hash algorithm to use
        stop_on_error: Whether to stop on first verification failure

    Returns:
        Tuple of (verified_files, failed_files)

    Raises:
        ResourceError: If checksum file cannot be read

    """
    if isinstance(checksum_file, str):
        checksum_file = Path(checksum_file)

    if base_dir is None:
        base_dir = checksum_file.parent
    elif isinstance(base_dir, str):
        base_dir = Path(base_dir)

    checksums = parse_checksum_file(checksum_file, algorithm)

    verified = []
    failed = []

    for filename, expected_hash in checksums.items():
        file_path = base_dir / filename

        if verify_file(file_path, expected_hash, algorithm):
            verified.append(filename)
        else:
            failed.append(filename)
            if stop_on_error:
                break

    log.info(
        "XX📊 Checksum verification completeXX",
        verified=len(verified),
        failed=len(failed),
        total=len(checksums),
    )

    return verified, failed


def x_verify_checksum_file__mutmut_35(
    checksum_file: Path | str,
    base_dir: Path | str | None = None,
    algorithm: str = DEFAULT_ALGORITHM,
    stop_on_error: bool = False,
) -> tuple[list[str], list[str]]:
    """Verify all files listed in a checksum file.

    Args:
        checksum_file: Path to checksum file
        base_dir: Base directory for relative paths (defaults to checksum file dir)
        algorithm: Hash algorithm to use
        stop_on_error: Whether to stop on first verification failure

    Returns:
        Tuple of (verified_files, failed_files)

    Raises:
        ResourceError: If checksum file cannot be read

    """
    if isinstance(checksum_file, str):
        checksum_file = Path(checksum_file)

    if base_dir is None:
        base_dir = checksum_file.parent
    elif isinstance(base_dir, str):
        base_dir = Path(base_dir)

    checksums = parse_checksum_file(checksum_file, algorithm)

    verified = []
    failed = []

    for filename, expected_hash in checksums.items():
        file_path = base_dir / filename

        if verify_file(file_path, expected_hash, algorithm):
            verified.append(filename)
        else:
            failed.append(filename)
            if stop_on_error:
                break

    log.info(
        "📊 checksum verification complete",
        verified=len(verified),
        failed=len(failed),
        total=len(checksums),
    )

    return verified, failed


def x_verify_checksum_file__mutmut_36(
    checksum_file: Path | str,
    base_dir: Path | str | None = None,
    algorithm: str = DEFAULT_ALGORITHM,
    stop_on_error: bool = False,
) -> tuple[list[str], list[str]]:
    """Verify all files listed in a checksum file.

    Args:
        checksum_file: Path to checksum file
        base_dir: Base directory for relative paths (defaults to checksum file dir)
        algorithm: Hash algorithm to use
        stop_on_error: Whether to stop on first verification failure

    Returns:
        Tuple of (verified_files, failed_files)

    Raises:
        ResourceError: If checksum file cannot be read

    """
    if isinstance(checksum_file, str):
        checksum_file = Path(checksum_file)

    if base_dir is None:
        base_dir = checksum_file.parent
    elif isinstance(base_dir, str):
        base_dir = Path(base_dir)

    checksums = parse_checksum_file(checksum_file, algorithm)

    verified = []
    failed = []

    for filename, expected_hash in checksums.items():
        file_path = base_dir / filename

        if verify_file(file_path, expected_hash, algorithm):
            verified.append(filename)
        else:
            failed.append(filename)
            if stop_on_error:
                break

    log.info(
        "📊 CHECKSUM VERIFICATION COMPLETE",
        verified=len(verified),
        failed=len(failed),
        total=len(checksums),
    )

    return verified, failed


x_verify_checksum_file__mutmut_mutants: ClassVar[MutantDict] = {
    "x_verify_checksum_file__mutmut_1": x_verify_checksum_file__mutmut_1,
    "x_verify_checksum_file__mutmut_2": x_verify_checksum_file__mutmut_2,
    "x_verify_checksum_file__mutmut_3": x_verify_checksum_file__mutmut_3,
    "x_verify_checksum_file__mutmut_4": x_verify_checksum_file__mutmut_4,
    "x_verify_checksum_file__mutmut_5": x_verify_checksum_file__mutmut_5,
    "x_verify_checksum_file__mutmut_6": x_verify_checksum_file__mutmut_6,
    "x_verify_checksum_file__mutmut_7": x_verify_checksum_file__mutmut_7,
    "x_verify_checksum_file__mutmut_8": x_verify_checksum_file__mutmut_8,
    "x_verify_checksum_file__mutmut_9": x_verify_checksum_file__mutmut_9,
    "x_verify_checksum_file__mutmut_10": x_verify_checksum_file__mutmut_10,
    "x_verify_checksum_file__mutmut_11": x_verify_checksum_file__mutmut_11,
    "x_verify_checksum_file__mutmut_12": x_verify_checksum_file__mutmut_12,
    "x_verify_checksum_file__mutmut_13": x_verify_checksum_file__mutmut_13,
    "x_verify_checksum_file__mutmut_14": x_verify_checksum_file__mutmut_14,
    "x_verify_checksum_file__mutmut_15": x_verify_checksum_file__mutmut_15,
    "x_verify_checksum_file__mutmut_16": x_verify_checksum_file__mutmut_16,
    "x_verify_checksum_file__mutmut_17": x_verify_checksum_file__mutmut_17,
    "x_verify_checksum_file__mutmut_18": x_verify_checksum_file__mutmut_18,
    "x_verify_checksum_file__mutmut_19": x_verify_checksum_file__mutmut_19,
    "x_verify_checksum_file__mutmut_20": x_verify_checksum_file__mutmut_20,
    "x_verify_checksum_file__mutmut_21": x_verify_checksum_file__mutmut_21,
    "x_verify_checksum_file__mutmut_22": x_verify_checksum_file__mutmut_22,
    "x_verify_checksum_file__mutmut_23": x_verify_checksum_file__mutmut_23,
    "x_verify_checksum_file__mutmut_24": x_verify_checksum_file__mutmut_24,
    "x_verify_checksum_file__mutmut_25": x_verify_checksum_file__mutmut_25,
    "x_verify_checksum_file__mutmut_26": x_verify_checksum_file__mutmut_26,
    "x_verify_checksum_file__mutmut_27": x_verify_checksum_file__mutmut_27,
    "x_verify_checksum_file__mutmut_28": x_verify_checksum_file__mutmut_28,
    "x_verify_checksum_file__mutmut_29": x_verify_checksum_file__mutmut_29,
    "x_verify_checksum_file__mutmut_30": x_verify_checksum_file__mutmut_30,
    "x_verify_checksum_file__mutmut_31": x_verify_checksum_file__mutmut_31,
    "x_verify_checksum_file__mutmut_32": x_verify_checksum_file__mutmut_32,
    "x_verify_checksum_file__mutmut_33": x_verify_checksum_file__mutmut_33,
    "x_verify_checksum_file__mutmut_34": x_verify_checksum_file__mutmut_34,
    "x_verify_checksum_file__mutmut_35": x_verify_checksum_file__mutmut_35,
    "x_verify_checksum_file__mutmut_36": x_verify_checksum_file__mutmut_36,
}


def verify_checksum_file(*args, **kwargs):
    result = _mutmut_trampoline(
        x_verify_checksum_file__mutmut_orig, x_verify_checksum_file__mutmut_mutants, args, kwargs
    )
    return result


verify_checksum_file.__signature__ = _mutmut_signature(x_verify_checksum_file__mutmut_orig)
x_verify_checksum_file__mutmut_orig.__name__ = "x_verify_checksum_file"


# <3 🧱🤝🔒🪄
