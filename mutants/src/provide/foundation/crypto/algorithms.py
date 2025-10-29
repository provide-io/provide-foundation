# provide/foundation/crypto/algorithms.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

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


def x_validate_algorithm__mutmut_orig(algorithm: str) -> None:
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


def x_validate_algorithm__mutmut_1(algorithm: str) -> None:
    """Validate that a hash algorithm is supported.

    Args:
        algorithm: Hash algorithm name

    Raises:
        ValidationError: If algorithm is not supported

    """
    if algorithm.upper() not in SUPPORTED_ALGORITHMS:
        raise ValidationError(
            f"Unsupported hash algorithm: {algorithm}",
            field="algorithm",
            value=algorithm,
            rule="must be one of: " + ", ".join(sorted(SUPPORTED_ALGORITHMS)),
        )


def x_validate_algorithm__mutmut_2(algorithm: str) -> None:
    """Validate that a hash algorithm is supported.

    Args:
        algorithm: Hash algorithm name

    Raises:
        ValidationError: If algorithm is not supported

    """
    if algorithm.lower() in SUPPORTED_ALGORITHMS:
        raise ValidationError(
            f"Unsupported hash algorithm: {algorithm}",
            field="algorithm",
            value=algorithm,
            rule="must be one of: " + ", ".join(sorted(SUPPORTED_ALGORITHMS)),
        )


def x_validate_algorithm__mutmut_3(algorithm: str) -> None:
    """Validate that a hash algorithm is supported.

    Args:
        algorithm: Hash algorithm name

    Raises:
        ValidationError: If algorithm is not supported

    """
    if algorithm.lower() not in SUPPORTED_ALGORITHMS:
        raise ValidationError(
            None,
            field="algorithm",
            value=algorithm,
            rule="must be one of: " + ", ".join(sorted(SUPPORTED_ALGORITHMS)),
        )


def x_validate_algorithm__mutmut_4(algorithm: str) -> None:
    """Validate that a hash algorithm is supported.

    Args:
        algorithm: Hash algorithm name

    Raises:
        ValidationError: If algorithm is not supported

    """
    if algorithm.lower() not in SUPPORTED_ALGORITHMS:
        raise ValidationError(
            f"Unsupported hash algorithm: {algorithm}",
            field=None,
            value=algorithm,
            rule="must be one of: " + ", ".join(sorted(SUPPORTED_ALGORITHMS)),
        )


def x_validate_algorithm__mutmut_5(algorithm: str) -> None:
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
            value=None,
            rule="must be one of: " + ", ".join(sorted(SUPPORTED_ALGORITHMS)),
        )


def x_validate_algorithm__mutmut_6(algorithm: str) -> None:
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
            rule=None,
        )


def x_validate_algorithm__mutmut_7(algorithm: str) -> None:
    """Validate that a hash algorithm is supported.

    Args:
        algorithm: Hash algorithm name

    Raises:
        ValidationError: If algorithm is not supported

    """
    if algorithm.lower() not in SUPPORTED_ALGORITHMS:
        raise ValidationError(
            field="algorithm",
            value=algorithm,
            rule="must be one of: " + ", ".join(sorted(SUPPORTED_ALGORITHMS)),
        )


def x_validate_algorithm__mutmut_8(algorithm: str) -> None:
    """Validate that a hash algorithm is supported.

    Args:
        algorithm: Hash algorithm name

    Raises:
        ValidationError: If algorithm is not supported

    """
    if algorithm.lower() not in SUPPORTED_ALGORITHMS:
        raise ValidationError(
            f"Unsupported hash algorithm: {algorithm}",
            value=algorithm,
            rule="must be one of: " + ", ".join(sorted(SUPPORTED_ALGORITHMS)),
        )


def x_validate_algorithm__mutmut_9(algorithm: str) -> None:
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
            rule="must be one of: " + ", ".join(sorted(SUPPORTED_ALGORITHMS)),
        )


def x_validate_algorithm__mutmut_10(algorithm: str) -> None:
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
        )


def x_validate_algorithm__mutmut_11(algorithm: str) -> None:
    """Validate that a hash algorithm is supported.

    Args:
        algorithm: Hash algorithm name

    Raises:
        ValidationError: If algorithm is not supported

    """
    if algorithm.lower() not in SUPPORTED_ALGORITHMS:
        raise ValidationError(
            f"Unsupported hash algorithm: {algorithm}",
            field="XXalgorithmXX",
            value=algorithm,
            rule="must be one of: " + ", ".join(sorted(SUPPORTED_ALGORITHMS)),
        )


def x_validate_algorithm__mutmut_12(algorithm: str) -> None:
    """Validate that a hash algorithm is supported.

    Args:
        algorithm: Hash algorithm name

    Raises:
        ValidationError: If algorithm is not supported

    """
    if algorithm.lower() not in SUPPORTED_ALGORITHMS:
        raise ValidationError(
            f"Unsupported hash algorithm: {algorithm}",
            field="ALGORITHM",
            value=algorithm,
            rule="must be one of: " + ", ".join(sorted(SUPPORTED_ALGORITHMS)),
        )


def x_validate_algorithm__mutmut_13(algorithm: str) -> None:
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
            rule="must be one of: " - ", ".join(sorted(SUPPORTED_ALGORITHMS)),
        )


def x_validate_algorithm__mutmut_14(algorithm: str) -> None:
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
            rule="XXmust be one of: XX" + ", ".join(sorted(SUPPORTED_ALGORITHMS)),
        )


def x_validate_algorithm__mutmut_15(algorithm: str) -> None:
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
            rule="MUST BE ONE OF: " + ", ".join(sorted(SUPPORTED_ALGORITHMS)),
        )


def x_validate_algorithm__mutmut_16(algorithm: str) -> None:
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
            rule="must be one of: " + ", ".join(None),
        )


def x_validate_algorithm__mutmut_17(algorithm: str) -> None:
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
            rule="must be one of: " + "XX, XX".join(sorted(SUPPORTED_ALGORITHMS)),
        )


def x_validate_algorithm__mutmut_18(algorithm: str) -> None:
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
            rule="must be one of: " + ", ".join(sorted(None)),
        )


x_validate_algorithm__mutmut_mutants: ClassVar[MutantDict] = {
    "x_validate_algorithm__mutmut_1": x_validate_algorithm__mutmut_1,
    "x_validate_algorithm__mutmut_2": x_validate_algorithm__mutmut_2,
    "x_validate_algorithm__mutmut_3": x_validate_algorithm__mutmut_3,
    "x_validate_algorithm__mutmut_4": x_validate_algorithm__mutmut_4,
    "x_validate_algorithm__mutmut_5": x_validate_algorithm__mutmut_5,
    "x_validate_algorithm__mutmut_6": x_validate_algorithm__mutmut_6,
    "x_validate_algorithm__mutmut_7": x_validate_algorithm__mutmut_7,
    "x_validate_algorithm__mutmut_8": x_validate_algorithm__mutmut_8,
    "x_validate_algorithm__mutmut_9": x_validate_algorithm__mutmut_9,
    "x_validate_algorithm__mutmut_10": x_validate_algorithm__mutmut_10,
    "x_validate_algorithm__mutmut_11": x_validate_algorithm__mutmut_11,
    "x_validate_algorithm__mutmut_12": x_validate_algorithm__mutmut_12,
    "x_validate_algorithm__mutmut_13": x_validate_algorithm__mutmut_13,
    "x_validate_algorithm__mutmut_14": x_validate_algorithm__mutmut_14,
    "x_validate_algorithm__mutmut_15": x_validate_algorithm__mutmut_15,
    "x_validate_algorithm__mutmut_16": x_validate_algorithm__mutmut_16,
    "x_validate_algorithm__mutmut_17": x_validate_algorithm__mutmut_17,
    "x_validate_algorithm__mutmut_18": x_validate_algorithm__mutmut_18,
}


def validate_algorithm(*args, **kwargs):
    result = _mutmut_trampoline(
        x_validate_algorithm__mutmut_orig, x_validate_algorithm__mutmut_mutants, args, kwargs
    )
    return result


validate_algorithm.__signature__ = _mutmut_signature(x_validate_algorithm__mutmut_orig)
x_validate_algorithm__mutmut_orig.__name__ = "x_validate_algorithm"


def x_get_hasher__mutmut_orig(algorithm: str) -> Any:
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


def x_get_hasher__mutmut_1(algorithm: str) -> Any:
    """Get a hash object for the specified algorithm.

    Args:
        algorithm: Hash algorithm name

    Returns:
        Hash object from hashlib

    Raises:
        ValidationError: If algorithm is not supported

    """
    validate_algorithm(None)

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


def x_get_hasher__mutmut_2(algorithm: str) -> Any:
    """Get a hash object for the specified algorithm.

    Args:
        algorithm: Hash algorithm name

    Returns:
        Hash object from hashlib

    Raises:
        ValidationError: If algorithm is not supported

    """
    validate_algorithm(algorithm)

    algorithm_lower = None

    # Handle special cases
    if algorithm_lower.startswith("sha3_"):
        # sha3_256 -> sha3_256 (hashlib uses underscores)
        return hashlib.new(algorithm_lower)
    if algorithm_lower.startswith("blake2"):
        # blake2b, blake2s
        return hashlib.new(algorithm_lower)
    # Standard algorithms (md5, sha1, sha256, etc.)
    return hashlib.new(algorithm_lower)


def x_get_hasher__mutmut_3(algorithm: str) -> Any:
    """Get a hash object for the specified algorithm.

    Args:
        algorithm: Hash algorithm name

    Returns:
        Hash object from hashlib

    Raises:
        ValidationError: If algorithm is not supported

    """
    validate_algorithm(algorithm)

    algorithm_lower = algorithm.upper()

    # Handle special cases
    if algorithm_lower.startswith("sha3_"):
        # sha3_256 -> sha3_256 (hashlib uses underscores)
        return hashlib.new(algorithm_lower)
    if algorithm_lower.startswith("blake2"):
        # blake2b, blake2s
        return hashlib.new(algorithm_lower)
    # Standard algorithms (md5, sha1, sha256, etc.)
    return hashlib.new(algorithm_lower)


def x_get_hasher__mutmut_4(algorithm: str) -> Any:
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
    if algorithm_lower.startswith(None):
        # sha3_256 -> sha3_256 (hashlib uses underscores)
        return hashlib.new(algorithm_lower)
    if algorithm_lower.startswith("blake2"):
        # blake2b, blake2s
        return hashlib.new(algorithm_lower)
    # Standard algorithms (md5, sha1, sha256, etc.)
    return hashlib.new(algorithm_lower)


def x_get_hasher__mutmut_5(algorithm: str) -> Any:
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
    if algorithm_lower.startswith("XXsha3_XX"):
        # sha3_256 -> sha3_256 (hashlib uses underscores)
        return hashlib.new(algorithm_lower)
    if algorithm_lower.startswith("blake2"):
        # blake2b, blake2s
        return hashlib.new(algorithm_lower)
    # Standard algorithms (md5, sha1, sha256, etc.)
    return hashlib.new(algorithm_lower)


def x_get_hasher__mutmut_6(algorithm: str) -> Any:
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
    if algorithm_lower.startswith("SHA3_"):
        # sha3_256 -> sha3_256 (hashlib uses underscores)
        return hashlib.new(algorithm_lower)
    if algorithm_lower.startswith("blake2"):
        # blake2b, blake2s
        return hashlib.new(algorithm_lower)
    # Standard algorithms (md5, sha1, sha256, etc.)
    return hashlib.new(algorithm_lower)


def x_get_hasher__mutmut_7(algorithm: str) -> Any:
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
        return hashlib.new(None)
    if algorithm_lower.startswith("blake2"):
        # blake2b, blake2s
        return hashlib.new(algorithm_lower)
    # Standard algorithms (md5, sha1, sha256, etc.)
    return hashlib.new(algorithm_lower)


def x_get_hasher__mutmut_8(algorithm: str) -> Any:
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
    if algorithm_lower.startswith(None):
        # blake2b, blake2s
        return hashlib.new(algorithm_lower)
    # Standard algorithms (md5, sha1, sha256, etc.)
    return hashlib.new(algorithm_lower)


def x_get_hasher__mutmut_9(algorithm: str) -> Any:
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
    if algorithm_lower.startswith("XXblake2XX"):
        # blake2b, blake2s
        return hashlib.new(algorithm_lower)
    # Standard algorithms (md5, sha1, sha256, etc.)
    return hashlib.new(algorithm_lower)


def x_get_hasher__mutmut_10(algorithm: str) -> Any:
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
    if algorithm_lower.startswith("BLAKE2"):
        # blake2b, blake2s
        return hashlib.new(algorithm_lower)
    # Standard algorithms (md5, sha1, sha256, etc.)
    return hashlib.new(algorithm_lower)


def x_get_hasher__mutmut_11(algorithm: str) -> Any:
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
        return hashlib.new(None)
    # Standard algorithms (md5, sha1, sha256, etc.)
    return hashlib.new(algorithm_lower)


def x_get_hasher__mutmut_12(algorithm: str) -> Any:
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
    return hashlib.new(None)


x_get_hasher__mutmut_mutants: ClassVar[MutantDict] = {
    "x_get_hasher__mutmut_1": x_get_hasher__mutmut_1,
    "x_get_hasher__mutmut_2": x_get_hasher__mutmut_2,
    "x_get_hasher__mutmut_3": x_get_hasher__mutmut_3,
    "x_get_hasher__mutmut_4": x_get_hasher__mutmut_4,
    "x_get_hasher__mutmut_5": x_get_hasher__mutmut_5,
    "x_get_hasher__mutmut_6": x_get_hasher__mutmut_6,
    "x_get_hasher__mutmut_7": x_get_hasher__mutmut_7,
    "x_get_hasher__mutmut_8": x_get_hasher__mutmut_8,
    "x_get_hasher__mutmut_9": x_get_hasher__mutmut_9,
    "x_get_hasher__mutmut_10": x_get_hasher__mutmut_10,
    "x_get_hasher__mutmut_11": x_get_hasher__mutmut_11,
    "x_get_hasher__mutmut_12": x_get_hasher__mutmut_12,
}


def get_hasher(*args, **kwargs):
    result = _mutmut_trampoline(x_get_hasher__mutmut_orig, x_get_hasher__mutmut_mutants, args, kwargs)
    return result


get_hasher.__signature__ = _mutmut_signature(x_get_hasher__mutmut_orig)
x_get_hasher__mutmut_orig.__name__ = "x_get_hasher"


def x_is_secure_algorithm__mutmut_orig(algorithm: str) -> bool:
    """Check if an algorithm is considered cryptographically secure.

    Args:
        algorithm: Hash algorithm name

    Returns:
        True if algorithm is secure, False otherwise

    """
    return algorithm.lower() in SECURE_ALGORITHMS


def x_is_secure_algorithm__mutmut_1(algorithm: str) -> bool:
    """Check if an algorithm is considered cryptographically secure.

    Args:
        algorithm: Hash algorithm name

    Returns:
        True if algorithm is secure, False otherwise

    """
    return algorithm.upper() in SECURE_ALGORITHMS


def x_is_secure_algorithm__mutmut_2(algorithm: str) -> bool:
    """Check if an algorithm is considered cryptographically secure.

    Args:
        algorithm: Hash algorithm name

    Returns:
        True if algorithm is secure, False otherwise

    """
    return algorithm.lower() not in SECURE_ALGORITHMS


x_is_secure_algorithm__mutmut_mutants: ClassVar[MutantDict] = {
    "x_is_secure_algorithm__mutmut_1": x_is_secure_algorithm__mutmut_1,
    "x_is_secure_algorithm__mutmut_2": x_is_secure_algorithm__mutmut_2,
}


def is_secure_algorithm(*args, **kwargs):
    result = _mutmut_trampoline(
        x_is_secure_algorithm__mutmut_orig, x_is_secure_algorithm__mutmut_mutants, args, kwargs
    )
    return result


is_secure_algorithm.__signature__ = _mutmut_signature(x_is_secure_algorithm__mutmut_orig)
x_is_secure_algorithm__mutmut_orig.__name__ = "x_is_secure_algorithm"


def x_get_digest_size__mutmut_orig(algorithm: str) -> int:
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


def x_get_digest_size__mutmut_1(algorithm: str) -> int:
    """Get the digest size in bytes for an algorithm.

    Args:
        algorithm: Hash algorithm name

    Returns:
        Digest size in bytes

    Raises:
        ValidationError: If algorithm is not supported

    """
    hasher = None
    return hasher.digest_size


def x_get_digest_size__mutmut_2(algorithm: str) -> int:
    """Get the digest size in bytes for an algorithm.

    Args:
        algorithm: Hash algorithm name

    Returns:
        Digest size in bytes

    Raises:
        ValidationError: If algorithm is not supported

    """
    hasher = get_hasher(None)
    return hasher.digest_size


x_get_digest_size__mutmut_mutants: ClassVar[MutantDict] = {
    "x_get_digest_size__mutmut_1": x_get_digest_size__mutmut_1,
    "x_get_digest_size__mutmut_2": x_get_digest_size__mutmut_2,
}


def get_digest_size(*args, **kwargs):
    result = _mutmut_trampoline(
        x_get_digest_size__mutmut_orig, x_get_digest_size__mutmut_mutants, args, kwargs
    )
    return result


get_digest_size.__signature__ = _mutmut_signature(x_get_digest_size__mutmut_orig)
x_get_digest_size__mutmut_orig.__name__ = "x_get_digest_size"


# <3 🧱🤝🔒🪄
