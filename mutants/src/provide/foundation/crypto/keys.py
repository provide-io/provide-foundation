# provide/foundation/crypto/keys.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

"""Key generation utilities for Foundation.

Provides functions for generating cryptographic key pairs for various
algorithms and use cases, including TLS and digital signatures.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Literal

from provide.foundation.crypto.deps import (
    DEFAULT_ECDSA_CURVE,
    DEFAULT_RSA_KEY_SIZE,
    SUPPORTED_EC_CURVES,
    SUPPORTED_KEY_TYPES,
    SUPPORTED_RSA_SIZES,
    Ed25519Signer,
    KeyType,
)
from provide.foundation.errors import FoundationError

if TYPE_CHECKING:
    from cryptography.hazmat.primitives.asymmetric import ec, rsa

    KeypairTuple = tuple[bytes, bytes]
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


class KeyGenerationError(FoundationError):
    """Raised when key generation fails."""


def x_generate_rsa_keypair__mutmut_orig(
    key_size: int = DEFAULT_RSA_KEY_SIZE,
) -> tuple[rsa.RSAPrivateKey, rsa.RSAPublicKey]:
    """Generate an RSA key pair.

    Args:
        key_size: Key size in bits (2048, 3072, or 4096)

    Returns:
        Tuple of (private_key, public_key)

    Raises:
        KeyGenerationError: If key size is unsupported
    """
    from cryptography.hazmat.backends import default_backend
    from cryptography.hazmat.primitives.asymmetric import rsa

    if key_size not in SUPPORTED_RSA_SIZES:
        raise KeyGenerationError(
            f"Unsupported RSA key size: {key_size}. Must be one of {SUPPORTED_RSA_SIZES}",
            context={"key_size": key_size, "supported_sizes": SUPPORTED_RSA_SIZES},
        )
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=key_size,
        backend=default_backend(),
    )
    return private_key, private_key.public_key()


def x_generate_rsa_keypair__mutmut_1(
    key_size: int = DEFAULT_RSA_KEY_SIZE,
) -> tuple[rsa.RSAPrivateKey, rsa.RSAPublicKey]:
    """Generate an RSA key pair.

    Args:
        key_size: Key size in bits (2048, 3072, or 4096)

    Returns:
        Tuple of (private_key, public_key)

    Raises:
        KeyGenerationError: If key size is unsupported
    """
    from cryptography.hazmat.backends import default_backend
    from cryptography.hazmat.primitives.asymmetric import rsa

    if key_size in SUPPORTED_RSA_SIZES:
        raise KeyGenerationError(
            f"Unsupported RSA key size: {key_size}. Must be one of {SUPPORTED_RSA_SIZES}",
            context={"key_size": key_size, "supported_sizes": SUPPORTED_RSA_SIZES},
        )
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=key_size,
        backend=default_backend(),
    )
    return private_key, private_key.public_key()


def x_generate_rsa_keypair__mutmut_2(
    key_size: int = DEFAULT_RSA_KEY_SIZE,
) -> tuple[rsa.RSAPrivateKey, rsa.RSAPublicKey]:
    """Generate an RSA key pair.

    Args:
        key_size: Key size in bits (2048, 3072, or 4096)

    Returns:
        Tuple of (private_key, public_key)

    Raises:
        KeyGenerationError: If key size is unsupported
    """
    from cryptography.hazmat.backends import default_backend
    from cryptography.hazmat.primitives.asymmetric import rsa

    if key_size not in SUPPORTED_RSA_SIZES:
        raise KeyGenerationError(
            None,
            context={"key_size": key_size, "supported_sizes": SUPPORTED_RSA_SIZES},
        )
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=key_size,
        backend=default_backend(),
    )
    return private_key, private_key.public_key()


def x_generate_rsa_keypair__mutmut_3(
    key_size: int = DEFAULT_RSA_KEY_SIZE,
) -> tuple[rsa.RSAPrivateKey, rsa.RSAPublicKey]:
    """Generate an RSA key pair.

    Args:
        key_size: Key size in bits (2048, 3072, or 4096)

    Returns:
        Tuple of (private_key, public_key)

    Raises:
        KeyGenerationError: If key size is unsupported
    """
    from cryptography.hazmat.backends import default_backend
    from cryptography.hazmat.primitives.asymmetric import rsa

    if key_size not in SUPPORTED_RSA_SIZES:
        raise KeyGenerationError(
            f"Unsupported RSA key size: {key_size}. Must be one of {SUPPORTED_RSA_SIZES}",
            context=None,
        )
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=key_size,
        backend=default_backend(),
    )
    return private_key, private_key.public_key()


def x_generate_rsa_keypair__mutmut_4(
    key_size: int = DEFAULT_RSA_KEY_SIZE,
) -> tuple[rsa.RSAPrivateKey, rsa.RSAPublicKey]:
    """Generate an RSA key pair.

    Args:
        key_size: Key size in bits (2048, 3072, or 4096)

    Returns:
        Tuple of (private_key, public_key)

    Raises:
        KeyGenerationError: If key size is unsupported
    """
    from cryptography.hazmat.backends import default_backend
    from cryptography.hazmat.primitives.asymmetric import rsa

    if key_size not in SUPPORTED_RSA_SIZES:
        raise KeyGenerationError(
            context={"key_size": key_size, "supported_sizes": SUPPORTED_RSA_SIZES},
        )
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=key_size,
        backend=default_backend(),
    )
    return private_key, private_key.public_key()


def x_generate_rsa_keypair__mutmut_5(
    key_size: int = DEFAULT_RSA_KEY_SIZE,
) -> tuple[rsa.RSAPrivateKey, rsa.RSAPublicKey]:
    """Generate an RSA key pair.

    Args:
        key_size: Key size in bits (2048, 3072, or 4096)

    Returns:
        Tuple of (private_key, public_key)

    Raises:
        KeyGenerationError: If key size is unsupported
    """
    from cryptography.hazmat.backends import default_backend
    from cryptography.hazmat.primitives.asymmetric import rsa

    if key_size not in SUPPORTED_RSA_SIZES:
        raise KeyGenerationError(
            f"Unsupported RSA key size: {key_size}. Must be one of {SUPPORTED_RSA_SIZES}",
        )
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=key_size,
        backend=default_backend(),
    )
    return private_key, private_key.public_key()


def x_generate_rsa_keypair__mutmut_6(
    key_size: int = DEFAULT_RSA_KEY_SIZE,
) -> tuple[rsa.RSAPrivateKey, rsa.RSAPublicKey]:
    """Generate an RSA key pair.

    Args:
        key_size: Key size in bits (2048, 3072, or 4096)

    Returns:
        Tuple of (private_key, public_key)

    Raises:
        KeyGenerationError: If key size is unsupported
    """
    from cryptography.hazmat.backends import default_backend
    from cryptography.hazmat.primitives.asymmetric import rsa

    if key_size not in SUPPORTED_RSA_SIZES:
        raise KeyGenerationError(
            f"Unsupported RSA key size: {key_size}. Must be one of {SUPPORTED_RSA_SIZES}",
            context={"XXkey_sizeXX": key_size, "supported_sizes": SUPPORTED_RSA_SIZES},
        )
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=key_size,
        backend=default_backend(),
    )
    return private_key, private_key.public_key()


def x_generate_rsa_keypair__mutmut_7(
    key_size: int = DEFAULT_RSA_KEY_SIZE,
) -> tuple[rsa.RSAPrivateKey, rsa.RSAPublicKey]:
    """Generate an RSA key pair.

    Args:
        key_size: Key size in bits (2048, 3072, or 4096)

    Returns:
        Tuple of (private_key, public_key)

    Raises:
        KeyGenerationError: If key size is unsupported
    """
    from cryptography.hazmat.backends import default_backend
    from cryptography.hazmat.primitives.asymmetric import rsa

    if key_size not in SUPPORTED_RSA_SIZES:
        raise KeyGenerationError(
            f"Unsupported RSA key size: {key_size}. Must be one of {SUPPORTED_RSA_SIZES}",
            context={"KEY_SIZE": key_size, "supported_sizes": SUPPORTED_RSA_SIZES},
        )
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=key_size,
        backend=default_backend(),
    )
    return private_key, private_key.public_key()


def x_generate_rsa_keypair__mutmut_8(
    key_size: int = DEFAULT_RSA_KEY_SIZE,
) -> tuple[rsa.RSAPrivateKey, rsa.RSAPublicKey]:
    """Generate an RSA key pair.

    Args:
        key_size: Key size in bits (2048, 3072, or 4096)

    Returns:
        Tuple of (private_key, public_key)

    Raises:
        KeyGenerationError: If key size is unsupported
    """
    from cryptography.hazmat.backends import default_backend
    from cryptography.hazmat.primitives.asymmetric import rsa

    if key_size not in SUPPORTED_RSA_SIZES:
        raise KeyGenerationError(
            f"Unsupported RSA key size: {key_size}. Must be one of {SUPPORTED_RSA_SIZES}",
            context={"key_size": key_size, "XXsupported_sizesXX": SUPPORTED_RSA_SIZES},
        )
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=key_size,
        backend=default_backend(),
    )
    return private_key, private_key.public_key()


def x_generate_rsa_keypair__mutmut_9(
    key_size: int = DEFAULT_RSA_KEY_SIZE,
) -> tuple[rsa.RSAPrivateKey, rsa.RSAPublicKey]:
    """Generate an RSA key pair.

    Args:
        key_size: Key size in bits (2048, 3072, or 4096)

    Returns:
        Tuple of (private_key, public_key)

    Raises:
        KeyGenerationError: If key size is unsupported
    """
    from cryptography.hazmat.backends import default_backend
    from cryptography.hazmat.primitives.asymmetric import rsa

    if key_size not in SUPPORTED_RSA_SIZES:
        raise KeyGenerationError(
            f"Unsupported RSA key size: {key_size}. Must be one of {SUPPORTED_RSA_SIZES}",
            context={"key_size": key_size, "SUPPORTED_SIZES": SUPPORTED_RSA_SIZES},
        )
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=key_size,
        backend=default_backend(),
    )
    return private_key, private_key.public_key()


def x_generate_rsa_keypair__mutmut_10(
    key_size: int = DEFAULT_RSA_KEY_SIZE,
) -> tuple[rsa.RSAPrivateKey, rsa.RSAPublicKey]:
    """Generate an RSA key pair.

    Args:
        key_size: Key size in bits (2048, 3072, or 4096)

    Returns:
        Tuple of (private_key, public_key)

    Raises:
        KeyGenerationError: If key size is unsupported
    """
    from cryptography.hazmat.backends import default_backend
    from cryptography.hazmat.primitives.asymmetric import rsa

    if key_size not in SUPPORTED_RSA_SIZES:
        raise KeyGenerationError(
            f"Unsupported RSA key size: {key_size}. Must be one of {SUPPORTED_RSA_SIZES}",
            context={"key_size": key_size, "supported_sizes": SUPPORTED_RSA_SIZES},
        )
    private_key = None
    return private_key, private_key.public_key()


def x_generate_rsa_keypair__mutmut_11(
    key_size: int = DEFAULT_RSA_KEY_SIZE,
) -> tuple[rsa.RSAPrivateKey, rsa.RSAPublicKey]:
    """Generate an RSA key pair.

    Args:
        key_size: Key size in bits (2048, 3072, or 4096)

    Returns:
        Tuple of (private_key, public_key)

    Raises:
        KeyGenerationError: If key size is unsupported
    """
    from cryptography.hazmat.backends import default_backend
    from cryptography.hazmat.primitives.asymmetric import rsa

    if key_size not in SUPPORTED_RSA_SIZES:
        raise KeyGenerationError(
            f"Unsupported RSA key size: {key_size}. Must be one of {SUPPORTED_RSA_SIZES}",
            context={"key_size": key_size, "supported_sizes": SUPPORTED_RSA_SIZES},
        )
    private_key = rsa.generate_private_key(
        public_exponent=None,
        key_size=key_size,
        backend=default_backend(),
    )
    return private_key, private_key.public_key()


def x_generate_rsa_keypair__mutmut_12(
    key_size: int = DEFAULT_RSA_KEY_SIZE,
) -> tuple[rsa.RSAPrivateKey, rsa.RSAPublicKey]:
    """Generate an RSA key pair.

    Args:
        key_size: Key size in bits (2048, 3072, or 4096)

    Returns:
        Tuple of (private_key, public_key)

    Raises:
        KeyGenerationError: If key size is unsupported
    """
    from cryptography.hazmat.backends import default_backend
    from cryptography.hazmat.primitives.asymmetric import rsa

    if key_size not in SUPPORTED_RSA_SIZES:
        raise KeyGenerationError(
            f"Unsupported RSA key size: {key_size}. Must be one of {SUPPORTED_RSA_SIZES}",
            context={"key_size": key_size, "supported_sizes": SUPPORTED_RSA_SIZES},
        )
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=None,
        backend=default_backend(),
    )
    return private_key, private_key.public_key()


def x_generate_rsa_keypair__mutmut_13(
    key_size: int = DEFAULT_RSA_KEY_SIZE,
) -> tuple[rsa.RSAPrivateKey, rsa.RSAPublicKey]:
    """Generate an RSA key pair.

    Args:
        key_size: Key size in bits (2048, 3072, or 4096)

    Returns:
        Tuple of (private_key, public_key)

    Raises:
        KeyGenerationError: If key size is unsupported
    """
    from cryptography.hazmat.backends import default_backend
    from cryptography.hazmat.primitives.asymmetric import rsa

    if key_size not in SUPPORTED_RSA_SIZES:
        raise KeyGenerationError(
            f"Unsupported RSA key size: {key_size}. Must be one of {SUPPORTED_RSA_SIZES}",
            context={"key_size": key_size, "supported_sizes": SUPPORTED_RSA_SIZES},
        )
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=key_size,
        backend=None,
    )
    return private_key, private_key.public_key()


def x_generate_rsa_keypair__mutmut_14(
    key_size: int = DEFAULT_RSA_KEY_SIZE,
) -> tuple[rsa.RSAPrivateKey, rsa.RSAPublicKey]:
    """Generate an RSA key pair.

    Args:
        key_size: Key size in bits (2048, 3072, or 4096)

    Returns:
        Tuple of (private_key, public_key)

    Raises:
        KeyGenerationError: If key size is unsupported
    """
    from cryptography.hazmat.backends import default_backend
    from cryptography.hazmat.primitives.asymmetric import rsa

    if key_size not in SUPPORTED_RSA_SIZES:
        raise KeyGenerationError(
            f"Unsupported RSA key size: {key_size}. Must be one of {SUPPORTED_RSA_SIZES}",
            context={"key_size": key_size, "supported_sizes": SUPPORTED_RSA_SIZES},
        )
    private_key = rsa.generate_private_key(
        key_size=key_size,
        backend=default_backend(),
    )
    return private_key, private_key.public_key()


def x_generate_rsa_keypair__mutmut_15(
    key_size: int = DEFAULT_RSA_KEY_SIZE,
) -> tuple[rsa.RSAPrivateKey, rsa.RSAPublicKey]:
    """Generate an RSA key pair.

    Args:
        key_size: Key size in bits (2048, 3072, or 4096)

    Returns:
        Tuple of (private_key, public_key)

    Raises:
        KeyGenerationError: If key size is unsupported
    """
    from cryptography.hazmat.backends import default_backend
    from cryptography.hazmat.primitives.asymmetric import rsa

    if key_size not in SUPPORTED_RSA_SIZES:
        raise KeyGenerationError(
            f"Unsupported RSA key size: {key_size}. Must be one of {SUPPORTED_RSA_SIZES}",
            context={"key_size": key_size, "supported_sizes": SUPPORTED_RSA_SIZES},
        )
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        backend=default_backend(),
    )
    return private_key, private_key.public_key()


def x_generate_rsa_keypair__mutmut_16(
    key_size: int = DEFAULT_RSA_KEY_SIZE,
) -> tuple[rsa.RSAPrivateKey, rsa.RSAPublicKey]:
    """Generate an RSA key pair.

    Args:
        key_size: Key size in bits (2048, 3072, or 4096)

    Returns:
        Tuple of (private_key, public_key)

    Raises:
        KeyGenerationError: If key size is unsupported
    """
    from cryptography.hazmat.backends import default_backend
    from cryptography.hazmat.primitives.asymmetric import rsa

    if key_size not in SUPPORTED_RSA_SIZES:
        raise KeyGenerationError(
            f"Unsupported RSA key size: {key_size}. Must be one of {SUPPORTED_RSA_SIZES}",
            context={"key_size": key_size, "supported_sizes": SUPPORTED_RSA_SIZES},
        )
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=key_size,
    )
    return private_key, private_key.public_key()


def x_generate_rsa_keypair__mutmut_17(
    key_size: int = DEFAULT_RSA_KEY_SIZE,
) -> tuple[rsa.RSAPrivateKey, rsa.RSAPublicKey]:
    """Generate an RSA key pair.

    Args:
        key_size: Key size in bits (2048, 3072, or 4096)

    Returns:
        Tuple of (private_key, public_key)

    Raises:
        KeyGenerationError: If key size is unsupported
    """
    from cryptography.hazmat.backends import default_backend
    from cryptography.hazmat.primitives.asymmetric import rsa

    if key_size not in SUPPORTED_RSA_SIZES:
        raise KeyGenerationError(
            f"Unsupported RSA key size: {key_size}. Must be one of {SUPPORTED_RSA_SIZES}",
            context={"key_size": key_size, "supported_sizes": SUPPORTED_RSA_SIZES},
        )
    private_key = rsa.generate_private_key(
        public_exponent=65538,
        key_size=key_size,
        backend=default_backend(),
    )
    return private_key, private_key.public_key()


x_generate_rsa_keypair__mutmut_mutants: ClassVar[MutantDict] = {
    "x_generate_rsa_keypair__mutmut_1": x_generate_rsa_keypair__mutmut_1,
    "x_generate_rsa_keypair__mutmut_2": x_generate_rsa_keypair__mutmut_2,
    "x_generate_rsa_keypair__mutmut_3": x_generate_rsa_keypair__mutmut_3,
    "x_generate_rsa_keypair__mutmut_4": x_generate_rsa_keypair__mutmut_4,
    "x_generate_rsa_keypair__mutmut_5": x_generate_rsa_keypair__mutmut_5,
    "x_generate_rsa_keypair__mutmut_6": x_generate_rsa_keypair__mutmut_6,
    "x_generate_rsa_keypair__mutmut_7": x_generate_rsa_keypair__mutmut_7,
    "x_generate_rsa_keypair__mutmut_8": x_generate_rsa_keypair__mutmut_8,
    "x_generate_rsa_keypair__mutmut_9": x_generate_rsa_keypair__mutmut_9,
    "x_generate_rsa_keypair__mutmut_10": x_generate_rsa_keypair__mutmut_10,
    "x_generate_rsa_keypair__mutmut_11": x_generate_rsa_keypair__mutmut_11,
    "x_generate_rsa_keypair__mutmut_12": x_generate_rsa_keypair__mutmut_12,
    "x_generate_rsa_keypair__mutmut_13": x_generate_rsa_keypair__mutmut_13,
    "x_generate_rsa_keypair__mutmut_14": x_generate_rsa_keypair__mutmut_14,
    "x_generate_rsa_keypair__mutmut_15": x_generate_rsa_keypair__mutmut_15,
    "x_generate_rsa_keypair__mutmut_16": x_generate_rsa_keypair__mutmut_16,
    "x_generate_rsa_keypair__mutmut_17": x_generate_rsa_keypair__mutmut_17,
}


def generate_rsa_keypair(*args, **kwargs):
    result = _mutmut_trampoline(
        x_generate_rsa_keypair__mutmut_orig, x_generate_rsa_keypair__mutmut_mutants, args, kwargs
    )
    return result


generate_rsa_keypair.__signature__ = _mutmut_signature(x_generate_rsa_keypair__mutmut_orig)
x_generate_rsa_keypair__mutmut_orig.__name__ = "x_generate_rsa_keypair"


def x_generate_ec_keypair__mutmut_orig(
    curve_name: str = DEFAULT_ECDSA_CURVE,
) -> tuple[ec.EllipticCurvePrivateKey, ec.EllipticCurvePublicKey]:
    """Generate an Elliptic Curve (EC) key pair.

    Args:
        curve_name: Name of the curve (e.g., 'secp256r1')

    Returns:
        Tuple of (private_key, public_key)

    Raises:
        KeyGenerationError: If curve is unsupported
    """
    from cryptography.hazmat.backends import default_backend
    from cryptography.hazmat.primitives.asymmetric import ec

    if curve_name not in SUPPORTED_EC_CURVES:
        raise KeyGenerationError(
            f"Unsupported EC curve: {curve_name}. Must be one of {SUPPORTED_EC_CURVES}",
            context={"curve_name": curve_name, "supported_curves": SUPPORTED_EC_CURVES},
        )

    # Map curve name to cryptography curve object
    curve_obj = getattr(ec, curve_name.upper())()
    private_key = ec.generate_private_key(curve_obj, backend=default_backend())
    return private_key, private_key.public_key()


def x_generate_ec_keypair__mutmut_1(
    curve_name: str = DEFAULT_ECDSA_CURVE,
) -> tuple[ec.EllipticCurvePrivateKey, ec.EllipticCurvePublicKey]:
    """Generate an Elliptic Curve (EC) key pair.

    Args:
        curve_name: Name of the curve (e.g., 'secp256r1')

    Returns:
        Tuple of (private_key, public_key)

    Raises:
        KeyGenerationError: If curve is unsupported
    """
    from cryptography.hazmat.backends import default_backend
    from cryptography.hazmat.primitives.asymmetric import ec

    if curve_name in SUPPORTED_EC_CURVES:
        raise KeyGenerationError(
            f"Unsupported EC curve: {curve_name}. Must be one of {SUPPORTED_EC_CURVES}",
            context={"curve_name": curve_name, "supported_curves": SUPPORTED_EC_CURVES},
        )

    # Map curve name to cryptography curve object
    curve_obj = getattr(ec, curve_name.upper())()
    private_key = ec.generate_private_key(curve_obj, backend=default_backend())
    return private_key, private_key.public_key()


def x_generate_ec_keypair__mutmut_2(
    curve_name: str = DEFAULT_ECDSA_CURVE,
) -> tuple[ec.EllipticCurvePrivateKey, ec.EllipticCurvePublicKey]:
    """Generate an Elliptic Curve (EC) key pair.

    Args:
        curve_name: Name of the curve (e.g., 'secp256r1')

    Returns:
        Tuple of (private_key, public_key)

    Raises:
        KeyGenerationError: If curve is unsupported
    """
    from cryptography.hazmat.backends import default_backend
    from cryptography.hazmat.primitives.asymmetric import ec

    if curve_name not in SUPPORTED_EC_CURVES:
        raise KeyGenerationError(
            None,
            context={"curve_name": curve_name, "supported_curves": SUPPORTED_EC_CURVES},
        )

    # Map curve name to cryptography curve object
    curve_obj = getattr(ec, curve_name.upper())()
    private_key = ec.generate_private_key(curve_obj, backend=default_backend())
    return private_key, private_key.public_key()


def x_generate_ec_keypair__mutmut_3(
    curve_name: str = DEFAULT_ECDSA_CURVE,
) -> tuple[ec.EllipticCurvePrivateKey, ec.EllipticCurvePublicKey]:
    """Generate an Elliptic Curve (EC) key pair.

    Args:
        curve_name: Name of the curve (e.g., 'secp256r1')

    Returns:
        Tuple of (private_key, public_key)

    Raises:
        KeyGenerationError: If curve is unsupported
    """
    from cryptography.hazmat.backends import default_backend
    from cryptography.hazmat.primitives.asymmetric import ec

    if curve_name not in SUPPORTED_EC_CURVES:
        raise KeyGenerationError(
            f"Unsupported EC curve: {curve_name}. Must be one of {SUPPORTED_EC_CURVES}",
            context=None,
        )

    # Map curve name to cryptography curve object
    curve_obj = getattr(ec, curve_name.upper())()
    private_key = ec.generate_private_key(curve_obj, backend=default_backend())
    return private_key, private_key.public_key()


def x_generate_ec_keypair__mutmut_4(
    curve_name: str = DEFAULT_ECDSA_CURVE,
) -> tuple[ec.EllipticCurvePrivateKey, ec.EllipticCurvePublicKey]:
    """Generate an Elliptic Curve (EC) key pair.

    Args:
        curve_name: Name of the curve (e.g., 'secp256r1')

    Returns:
        Tuple of (private_key, public_key)

    Raises:
        KeyGenerationError: If curve is unsupported
    """
    from cryptography.hazmat.backends import default_backend
    from cryptography.hazmat.primitives.asymmetric import ec

    if curve_name not in SUPPORTED_EC_CURVES:
        raise KeyGenerationError(
            context={"curve_name": curve_name, "supported_curves": SUPPORTED_EC_CURVES},
        )

    # Map curve name to cryptography curve object
    curve_obj = getattr(ec, curve_name.upper())()
    private_key = ec.generate_private_key(curve_obj, backend=default_backend())
    return private_key, private_key.public_key()


def x_generate_ec_keypair__mutmut_5(
    curve_name: str = DEFAULT_ECDSA_CURVE,
) -> tuple[ec.EllipticCurvePrivateKey, ec.EllipticCurvePublicKey]:
    """Generate an Elliptic Curve (EC) key pair.

    Args:
        curve_name: Name of the curve (e.g., 'secp256r1')

    Returns:
        Tuple of (private_key, public_key)

    Raises:
        KeyGenerationError: If curve is unsupported
    """
    from cryptography.hazmat.backends import default_backend
    from cryptography.hazmat.primitives.asymmetric import ec

    if curve_name not in SUPPORTED_EC_CURVES:
        raise KeyGenerationError(
            f"Unsupported EC curve: {curve_name}. Must be one of {SUPPORTED_EC_CURVES}",
        )

    # Map curve name to cryptography curve object
    curve_obj = getattr(ec, curve_name.upper())()
    private_key = ec.generate_private_key(curve_obj, backend=default_backend())
    return private_key, private_key.public_key()


def x_generate_ec_keypair__mutmut_6(
    curve_name: str = DEFAULT_ECDSA_CURVE,
) -> tuple[ec.EllipticCurvePrivateKey, ec.EllipticCurvePublicKey]:
    """Generate an Elliptic Curve (EC) key pair.

    Args:
        curve_name: Name of the curve (e.g., 'secp256r1')

    Returns:
        Tuple of (private_key, public_key)

    Raises:
        KeyGenerationError: If curve is unsupported
    """
    from cryptography.hazmat.backends import default_backend
    from cryptography.hazmat.primitives.asymmetric import ec

    if curve_name not in SUPPORTED_EC_CURVES:
        raise KeyGenerationError(
            f"Unsupported EC curve: {curve_name}. Must be one of {SUPPORTED_EC_CURVES}",
            context={"XXcurve_nameXX": curve_name, "supported_curves": SUPPORTED_EC_CURVES},
        )

    # Map curve name to cryptography curve object
    curve_obj = getattr(ec, curve_name.upper())()
    private_key = ec.generate_private_key(curve_obj, backend=default_backend())
    return private_key, private_key.public_key()


def x_generate_ec_keypair__mutmut_7(
    curve_name: str = DEFAULT_ECDSA_CURVE,
) -> tuple[ec.EllipticCurvePrivateKey, ec.EllipticCurvePublicKey]:
    """Generate an Elliptic Curve (EC) key pair.

    Args:
        curve_name: Name of the curve (e.g., 'secp256r1')

    Returns:
        Tuple of (private_key, public_key)

    Raises:
        KeyGenerationError: If curve is unsupported
    """
    from cryptography.hazmat.backends import default_backend
    from cryptography.hazmat.primitives.asymmetric import ec

    if curve_name not in SUPPORTED_EC_CURVES:
        raise KeyGenerationError(
            f"Unsupported EC curve: {curve_name}. Must be one of {SUPPORTED_EC_CURVES}",
            context={"CURVE_NAME": curve_name, "supported_curves": SUPPORTED_EC_CURVES},
        )

    # Map curve name to cryptography curve object
    curve_obj = getattr(ec, curve_name.upper())()
    private_key = ec.generate_private_key(curve_obj, backend=default_backend())
    return private_key, private_key.public_key()


def x_generate_ec_keypair__mutmut_8(
    curve_name: str = DEFAULT_ECDSA_CURVE,
) -> tuple[ec.EllipticCurvePrivateKey, ec.EllipticCurvePublicKey]:
    """Generate an Elliptic Curve (EC) key pair.

    Args:
        curve_name: Name of the curve (e.g., 'secp256r1')

    Returns:
        Tuple of (private_key, public_key)

    Raises:
        KeyGenerationError: If curve is unsupported
    """
    from cryptography.hazmat.backends import default_backend
    from cryptography.hazmat.primitives.asymmetric import ec

    if curve_name not in SUPPORTED_EC_CURVES:
        raise KeyGenerationError(
            f"Unsupported EC curve: {curve_name}. Must be one of {SUPPORTED_EC_CURVES}",
            context={"curve_name": curve_name, "XXsupported_curvesXX": SUPPORTED_EC_CURVES},
        )

    # Map curve name to cryptography curve object
    curve_obj = getattr(ec, curve_name.upper())()
    private_key = ec.generate_private_key(curve_obj, backend=default_backend())
    return private_key, private_key.public_key()


def x_generate_ec_keypair__mutmut_9(
    curve_name: str = DEFAULT_ECDSA_CURVE,
) -> tuple[ec.EllipticCurvePrivateKey, ec.EllipticCurvePublicKey]:
    """Generate an Elliptic Curve (EC) key pair.

    Args:
        curve_name: Name of the curve (e.g., 'secp256r1')

    Returns:
        Tuple of (private_key, public_key)

    Raises:
        KeyGenerationError: If curve is unsupported
    """
    from cryptography.hazmat.backends import default_backend
    from cryptography.hazmat.primitives.asymmetric import ec

    if curve_name not in SUPPORTED_EC_CURVES:
        raise KeyGenerationError(
            f"Unsupported EC curve: {curve_name}. Must be one of {SUPPORTED_EC_CURVES}",
            context={"curve_name": curve_name, "SUPPORTED_CURVES": SUPPORTED_EC_CURVES},
        )

    # Map curve name to cryptography curve object
    curve_obj = getattr(ec, curve_name.upper())()
    private_key = ec.generate_private_key(curve_obj, backend=default_backend())
    return private_key, private_key.public_key()


def x_generate_ec_keypair__mutmut_10(
    curve_name: str = DEFAULT_ECDSA_CURVE,
) -> tuple[ec.EllipticCurvePrivateKey, ec.EllipticCurvePublicKey]:
    """Generate an Elliptic Curve (EC) key pair.

    Args:
        curve_name: Name of the curve (e.g., 'secp256r1')

    Returns:
        Tuple of (private_key, public_key)

    Raises:
        KeyGenerationError: If curve is unsupported
    """
    from cryptography.hazmat.backends import default_backend
    from cryptography.hazmat.primitives.asymmetric import ec

    if curve_name not in SUPPORTED_EC_CURVES:
        raise KeyGenerationError(
            f"Unsupported EC curve: {curve_name}. Must be one of {SUPPORTED_EC_CURVES}",
            context={"curve_name": curve_name, "supported_curves": SUPPORTED_EC_CURVES},
        )

    # Map curve name to cryptography curve object
    curve_obj = None
    private_key = ec.generate_private_key(curve_obj, backend=default_backend())
    return private_key, private_key.public_key()


def x_generate_ec_keypair__mutmut_11(
    curve_name: str = DEFAULT_ECDSA_CURVE,
) -> tuple[ec.EllipticCurvePrivateKey, ec.EllipticCurvePublicKey]:
    """Generate an Elliptic Curve (EC) key pair.

    Args:
        curve_name: Name of the curve (e.g., 'secp256r1')

    Returns:
        Tuple of (private_key, public_key)

    Raises:
        KeyGenerationError: If curve is unsupported
    """
    from cryptography.hazmat.backends import default_backend
    from cryptography.hazmat.primitives.asymmetric import ec

    if curve_name not in SUPPORTED_EC_CURVES:
        raise KeyGenerationError(
            f"Unsupported EC curve: {curve_name}. Must be one of {SUPPORTED_EC_CURVES}",
            context={"curve_name": curve_name, "supported_curves": SUPPORTED_EC_CURVES},
        )

    # Map curve name to cryptography curve object
    curve_obj = getattr(None, curve_name.upper())()
    private_key = ec.generate_private_key(curve_obj, backend=default_backend())
    return private_key, private_key.public_key()


def x_generate_ec_keypair__mutmut_12(
    curve_name: str = DEFAULT_ECDSA_CURVE,
) -> tuple[ec.EllipticCurvePrivateKey, ec.EllipticCurvePublicKey]:
    """Generate an Elliptic Curve (EC) key pair.

    Args:
        curve_name: Name of the curve (e.g., 'secp256r1')

    Returns:
        Tuple of (private_key, public_key)

    Raises:
        KeyGenerationError: If curve is unsupported
    """
    from cryptography.hazmat.backends import default_backend
    from cryptography.hazmat.primitives.asymmetric import ec

    if curve_name not in SUPPORTED_EC_CURVES:
        raise KeyGenerationError(
            f"Unsupported EC curve: {curve_name}. Must be one of {SUPPORTED_EC_CURVES}",
            context={"curve_name": curve_name, "supported_curves": SUPPORTED_EC_CURVES},
        )

    # Map curve name to cryptography curve object
    curve_obj = getattr(ec, None)()
    private_key = ec.generate_private_key(curve_obj, backend=default_backend())
    return private_key, private_key.public_key()


def x_generate_ec_keypair__mutmut_13(
    curve_name: str = DEFAULT_ECDSA_CURVE,
) -> tuple[ec.EllipticCurvePrivateKey, ec.EllipticCurvePublicKey]:
    """Generate an Elliptic Curve (EC) key pair.

    Args:
        curve_name: Name of the curve (e.g., 'secp256r1')

    Returns:
        Tuple of (private_key, public_key)

    Raises:
        KeyGenerationError: If curve is unsupported
    """
    from cryptography.hazmat.backends import default_backend
    from cryptography.hazmat.primitives.asymmetric import ec

    if curve_name not in SUPPORTED_EC_CURVES:
        raise KeyGenerationError(
            f"Unsupported EC curve: {curve_name}. Must be one of {SUPPORTED_EC_CURVES}",
            context={"curve_name": curve_name, "supported_curves": SUPPORTED_EC_CURVES},
        )

    # Map curve name to cryptography curve object
    curve_obj = getattr(curve_name.upper())()
    private_key = ec.generate_private_key(curve_obj, backend=default_backend())
    return private_key, private_key.public_key()


def x_generate_ec_keypair__mutmut_14(
    curve_name: str = DEFAULT_ECDSA_CURVE,
) -> tuple[ec.EllipticCurvePrivateKey, ec.EllipticCurvePublicKey]:
    """Generate an Elliptic Curve (EC) key pair.

    Args:
        curve_name: Name of the curve (e.g., 'secp256r1')

    Returns:
        Tuple of (private_key, public_key)

    Raises:
        KeyGenerationError: If curve is unsupported
    """
    from cryptography.hazmat.backends import default_backend
    from cryptography.hazmat.primitives.asymmetric import ec

    if curve_name not in SUPPORTED_EC_CURVES:
        raise KeyGenerationError(
            f"Unsupported EC curve: {curve_name}. Must be one of {SUPPORTED_EC_CURVES}",
            context={"curve_name": curve_name, "supported_curves": SUPPORTED_EC_CURVES},
        )

    # Map curve name to cryptography curve object
    curve_obj = getattr(
        ec,
    )()
    private_key = ec.generate_private_key(curve_obj, backend=default_backend())
    return private_key, private_key.public_key()


def x_generate_ec_keypair__mutmut_15(
    curve_name: str = DEFAULT_ECDSA_CURVE,
) -> tuple[ec.EllipticCurvePrivateKey, ec.EllipticCurvePublicKey]:
    """Generate an Elliptic Curve (EC) key pair.

    Args:
        curve_name: Name of the curve (e.g., 'secp256r1')

    Returns:
        Tuple of (private_key, public_key)

    Raises:
        KeyGenerationError: If curve is unsupported
    """
    from cryptography.hazmat.backends import default_backend
    from cryptography.hazmat.primitives.asymmetric import ec

    if curve_name not in SUPPORTED_EC_CURVES:
        raise KeyGenerationError(
            f"Unsupported EC curve: {curve_name}. Must be one of {SUPPORTED_EC_CURVES}",
            context={"curve_name": curve_name, "supported_curves": SUPPORTED_EC_CURVES},
        )

    # Map curve name to cryptography curve object
    curve_obj = getattr(ec, curve_name.lower())()
    private_key = ec.generate_private_key(curve_obj, backend=default_backend())
    return private_key, private_key.public_key()


def x_generate_ec_keypair__mutmut_16(
    curve_name: str = DEFAULT_ECDSA_CURVE,
) -> tuple[ec.EllipticCurvePrivateKey, ec.EllipticCurvePublicKey]:
    """Generate an Elliptic Curve (EC) key pair.

    Args:
        curve_name: Name of the curve (e.g., 'secp256r1')

    Returns:
        Tuple of (private_key, public_key)

    Raises:
        KeyGenerationError: If curve is unsupported
    """
    from cryptography.hazmat.backends import default_backend
    from cryptography.hazmat.primitives.asymmetric import ec

    if curve_name not in SUPPORTED_EC_CURVES:
        raise KeyGenerationError(
            f"Unsupported EC curve: {curve_name}. Must be one of {SUPPORTED_EC_CURVES}",
            context={"curve_name": curve_name, "supported_curves": SUPPORTED_EC_CURVES},
        )

    # Map curve name to cryptography curve object
    curve_obj = getattr(ec, curve_name.upper())()
    private_key = None
    return private_key, private_key.public_key()


def x_generate_ec_keypair__mutmut_17(
    curve_name: str = DEFAULT_ECDSA_CURVE,
) -> tuple[ec.EllipticCurvePrivateKey, ec.EllipticCurvePublicKey]:
    """Generate an Elliptic Curve (EC) key pair.

    Args:
        curve_name: Name of the curve (e.g., 'secp256r1')

    Returns:
        Tuple of (private_key, public_key)

    Raises:
        KeyGenerationError: If curve is unsupported
    """
    from cryptography.hazmat.backends import default_backend
    from cryptography.hazmat.primitives.asymmetric import ec

    if curve_name not in SUPPORTED_EC_CURVES:
        raise KeyGenerationError(
            f"Unsupported EC curve: {curve_name}. Must be one of {SUPPORTED_EC_CURVES}",
            context={"curve_name": curve_name, "supported_curves": SUPPORTED_EC_CURVES},
        )

    # Map curve name to cryptography curve object
    curve_obj = getattr(ec, curve_name.upper())()
    private_key = ec.generate_private_key(None, backend=default_backend())
    return private_key, private_key.public_key()


def x_generate_ec_keypair__mutmut_18(
    curve_name: str = DEFAULT_ECDSA_CURVE,
) -> tuple[ec.EllipticCurvePrivateKey, ec.EllipticCurvePublicKey]:
    """Generate an Elliptic Curve (EC) key pair.

    Args:
        curve_name: Name of the curve (e.g., 'secp256r1')

    Returns:
        Tuple of (private_key, public_key)

    Raises:
        KeyGenerationError: If curve is unsupported
    """
    from cryptography.hazmat.backends import default_backend
    from cryptography.hazmat.primitives.asymmetric import ec

    if curve_name not in SUPPORTED_EC_CURVES:
        raise KeyGenerationError(
            f"Unsupported EC curve: {curve_name}. Must be one of {SUPPORTED_EC_CURVES}",
            context={"curve_name": curve_name, "supported_curves": SUPPORTED_EC_CURVES},
        )

    # Map curve name to cryptography curve object
    curve_obj = getattr(ec, curve_name.upper())()
    private_key = ec.generate_private_key(curve_obj, backend=None)
    return private_key, private_key.public_key()


def x_generate_ec_keypair__mutmut_19(
    curve_name: str = DEFAULT_ECDSA_CURVE,
) -> tuple[ec.EllipticCurvePrivateKey, ec.EllipticCurvePublicKey]:
    """Generate an Elliptic Curve (EC) key pair.

    Args:
        curve_name: Name of the curve (e.g., 'secp256r1')

    Returns:
        Tuple of (private_key, public_key)

    Raises:
        KeyGenerationError: If curve is unsupported
    """
    from cryptography.hazmat.backends import default_backend
    from cryptography.hazmat.primitives.asymmetric import ec

    if curve_name not in SUPPORTED_EC_CURVES:
        raise KeyGenerationError(
            f"Unsupported EC curve: {curve_name}. Must be one of {SUPPORTED_EC_CURVES}",
            context={"curve_name": curve_name, "supported_curves": SUPPORTED_EC_CURVES},
        )

    # Map curve name to cryptography curve object
    curve_obj = getattr(ec, curve_name.upper())()
    private_key = ec.generate_private_key(backend=default_backend())
    return private_key, private_key.public_key()


def x_generate_ec_keypair__mutmut_20(
    curve_name: str = DEFAULT_ECDSA_CURVE,
) -> tuple[ec.EllipticCurvePrivateKey, ec.EllipticCurvePublicKey]:
    """Generate an Elliptic Curve (EC) key pair.

    Args:
        curve_name: Name of the curve (e.g., 'secp256r1')

    Returns:
        Tuple of (private_key, public_key)

    Raises:
        KeyGenerationError: If curve is unsupported
    """
    from cryptography.hazmat.backends import default_backend
    from cryptography.hazmat.primitives.asymmetric import ec

    if curve_name not in SUPPORTED_EC_CURVES:
        raise KeyGenerationError(
            f"Unsupported EC curve: {curve_name}. Must be one of {SUPPORTED_EC_CURVES}",
            context={"curve_name": curve_name, "supported_curves": SUPPORTED_EC_CURVES},
        )

    # Map curve name to cryptography curve object
    curve_obj = getattr(ec, curve_name.upper())()
    private_key = ec.generate_private_key(
        curve_obj,
    )
    return private_key, private_key.public_key()


x_generate_ec_keypair__mutmut_mutants: ClassVar[MutantDict] = {
    "x_generate_ec_keypair__mutmut_1": x_generate_ec_keypair__mutmut_1,
    "x_generate_ec_keypair__mutmut_2": x_generate_ec_keypair__mutmut_2,
    "x_generate_ec_keypair__mutmut_3": x_generate_ec_keypair__mutmut_3,
    "x_generate_ec_keypair__mutmut_4": x_generate_ec_keypair__mutmut_4,
    "x_generate_ec_keypair__mutmut_5": x_generate_ec_keypair__mutmut_5,
    "x_generate_ec_keypair__mutmut_6": x_generate_ec_keypair__mutmut_6,
    "x_generate_ec_keypair__mutmut_7": x_generate_ec_keypair__mutmut_7,
    "x_generate_ec_keypair__mutmut_8": x_generate_ec_keypair__mutmut_8,
    "x_generate_ec_keypair__mutmut_9": x_generate_ec_keypair__mutmut_9,
    "x_generate_ec_keypair__mutmut_10": x_generate_ec_keypair__mutmut_10,
    "x_generate_ec_keypair__mutmut_11": x_generate_ec_keypair__mutmut_11,
    "x_generate_ec_keypair__mutmut_12": x_generate_ec_keypair__mutmut_12,
    "x_generate_ec_keypair__mutmut_13": x_generate_ec_keypair__mutmut_13,
    "x_generate_ec_keypair__mutmut_14": x_generate_ec_keypair__mutmut_14,
    "x_generate_ec_keypair__mutmut_15": x_generate_ec_keypair__mutmut_15,
    "x_generate_ec_keypair__mutmut_16": x_generate_ec_keypair__mutmut_16,
    "x_generate_ec_keypair__mutmut_17": x_generate_ec_keypair__mutmut_17,
    "x_generate_ec_keypair__mutmut_18": x_generate_ec_keypair__mutmut_18,
    "x_generate_ec_keypair__mutmut_19": x_generate_ec_keypair__mutmut_19,
    "x_generate_ec_keypair__mutmut_20": x_generate_ec_keypair__mutmut_20,
}


def generate_ec_keypair(*args, **kwargs):
    result = _mutmut_trampoline(
        x_generate_ec_keypair__mutmut_orig, x_generate_ec_keypair__mutmut_mutants, args, kwargs
    )
    return result


generate_ec_keypair.__signature__ = _mutmut_signature(x_generate_ec_keypair__mutmut_orig)
x_generate_ec_keypair__mutmut_orig.__name__ = "x_generate_ec_keypair"


def x_generate_ed25519_keypair__mutmut_orig() -> KeypairTuple:
    """Generate an Ed25519 key pair.

    This is a wrapper around the modern Ed25519Signer class to provide
    raw key bytes for compatibility with legacy systems or specific protocols.

    Returns:
        A tuple containing (private_key_bytes, public_key_bytes).
    """
    signer = Ed25519Signer.generate()
    return signer.export_private_key(), signer.public_key


def x_generate_ed25519_keypair__mutmut_1() -> KeypairTuple:
    """Generate an Ed25519 key pair.

    This is a wrapper around the modern Ed25519Signer class to provide
    raw key bytes for compatibility with legacy systems or specific protocols.

    Returns:
        A tuple containing (private_key_bytes, public_key_bytes).
    """
    signer = None
    return signer.export_private_key(), signer.public_key


x_generate_ed25519_keypair__mutmut_mutants: ClassVar[MutantDict] = {
    "x_generate_ed25519_keypair__mutmut_1": x_generate_ed25519_keypair__mutmut_1
}


def generate_ed25519_keypair(*args, **kwargs):
    result = _mutmut_trampoline(
        x_generate_ed25519_keypair__mutmut_orig, x_generate_ed25519_keypair__mutmut_mutants, args, kwargs
    )
    return result


generate_ed25519_keypair.__signature__ = _mutmut_signature(x_generate_ed25519_keypair__mutmut_orig)
x_generate_ed25519_keypair__mutmut_orig.__name__ = "x_generate_ed25519_keypair"


def x_generate_keypair__mutmut_orig(
    key_type: KeyType,
    key_size: int | None = None,
    curve_name: str | None = None,
) -> tuple[bytes, bytes]:
    """Generate a key pair and return serialized keys.

    Args:
        key_type: Type of key ('rsa' or 'ec')
        key_size: RSA key size (for 'rsa' type)
        curve_name: EC curve name (for 'ec' type)

    Returns:
        Tuple of (private_key_pem, public_key_pem)

    Raises:
        KeyGenerationError: If key type is unsupported
    """
    from cryptography.hazmat.primitives import serialization

    if key_type == "rsa":
        priv, pub = generate_rsa_keypair(key_size or DEFAULT_RSA_KEY_SIZE)
    elif key_type == "ec":
        priv, pub = generate_ec_keypair(curve_name or DEFAULT_ECDSA_CURVE)  # type: ignore[assignment]
    else:
        raise KeyGenerationError(
            f"Unsupported key type: {key_type}. Must be one of {SUPPORTED_KEY_TYPES}",
            context={"key_type": key_type, "supported_types": SUPPORTED_KEY_TYPES},
        )

    private_pem = priv.private_bytes(  # type: ignore[attr-defined]
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )
    public_pem = pub.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )
    return private_pem, public_pem


def x_generate_keypair__mutmut_1(
    key_type: KeyType,
    key_size: int | None = None,
    curve_name: str | None = None,
) -> tuple[bytes, bytes]:
    """Generate a key pair and return serialized keys.

    Args:
        key_type: Type of key ('rsa' or 'ec')
        key_size: RSA key size (for 'rsa' type)
        curve_name: EC curve name (for 'ec' type)

    Returns:
        Tuple of (private_key_pem, public_key_pem)

    Raises:
        KeyGenerationError: If key type is unsupported
    """
    from cryptography.hazmat.primitives import serialization

    if key_type != "rsa":
        priv, pub = generate_rsa_keypair(key_size or DEFAULT_RSA_KEY_SIZE)
    elif key_type == "ec":
        priv, pub = generate_ec_keypair(curve_name or DEFAULT_ECDSA_CURVE)  # type: ignore[assignment]
    else:
        raise KeyGenerationError(
            f"Unsupported key type: {key_type}. Must be one of {SUPPORTED_KEY_TYPES}",
            context={"key_type": key_type, "supported_types": SUPPORTED_KEY_TYPES},
        )

    private_pem = priv.private_bytes(  # type: ignore[attr-defined]
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )
    public_pem = pub.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )
    return private_pem, public_pem


def x_generate_keypair__mutmut_2(
    key_type: KeyType,
    key_size: int | None = None,
    curve_name: str | None = None,
) -> tuple[bytes, bytes]:
    """Generate a key pair and return serialized keys.

    Args:
        key_type: Type of key ('rsa' or 'ec')
        key_size: RSA key size (for 'rsa' type)
        curve_name: EC curve name (for 'ec' type)

    Returns:
        Tuple of (private_key_pem, public_key_pem)

    Raises:
        KeyGenerationError: If key type is unsupported
    """
    from cryptography.hazmat.primitives import serialization

    if key_type == "XXrsaXX":
        priv, pub = generate_rsa_keypair(key_size or DEFAULT_RSA_KEY_SIZE)
    elif key_type == "ec":
        priv, pub = generate_ec_keypair(curve_name or DEFAULT_ECDSA_CURVE)  # type: ignore[assignment]
    else:
        raise KeyGenerationError(
            f"Unsupported key type: {key_type}. Must be one of {SUPPORTED_KEY_TYPES}",
            context={"key_type": key_type, "supported_types": SUPPORTED_KEY_TYPES},
        )

    private_pem = priv.private_bytes(  # type: ignore[attr-defined]
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )
    public_pem = pub.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )
    return private_pem, public_pem


def x_generate_keypair__mutmut_3(
    key_type: KeyType,
    key_size: int | None = None,
    curve_name: str | None = None,
) -> tuple[bytes, bytes]:
    """Generate a key pair and return serialized keys.

    Args:
        key_type: Type of key ('rsa' or 'ec')
        key_size: RSA key size (for 'rsa' type)
        curve_name: EC curve name (for 'ec' type)

    Returns:
        Tuple of (private_key_pem, public_key_pem)

    Raises:
        KeyGenerationError: If key type is unsupported
    """
    from cryptography.hazmat.primitives import serialization

    if key_type == "RSA":
        priv, pub = generate_rsa_keypair(key_size or DEFAULT_RSA_KEY_SIZE)
    elif key_type == "ec":
        priv, pub = generate_ec_keypair(curve_name or DEFAULT_ECDSA_CURVE)  # type: ignore[assignment]
    else:
        raise KeyGenerationError(
            f"Unsupported key type: {key_type}. Must be one of {SUPPORTED_KEY_TYPES}",
            context={"key_type": key_type, "supported_types": SUPPORTED_KEY_TYPES},
        )

    private_pem = priv.private_bytes(  # type: ignore[attr-defined]
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )
    public_pem = pub.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )
    return private_pem, public_pem


def x_generate_keypair__mutmut_4(
    key_type: KeyType,
    key_size: int | None = None,
    curve_name: str | None = None,
) -> tuple[bytes, bytes]:
    """Generate a key pair and return serialized keys.

    Args:
        key_type: Type of key ('rsa' or 'ec')
        key_size: RSA key size (for 'rsa' type)
        curve_name: EC curve name (for 'ec' type)

    Returns:
        Tuple of (private_key_pem, public_key_pem)

    Raises:
        KeyGenerationError: If key type is unsupported
    """
    from cryptography.hazmat.primitives import serialization

    if key_type == "rsa":
        priv, pub = None
    elif key_type == "ec":
        priv, pub = generate_ec_keypair(curve_name or DEFAULT_ECDSA_CURVE)  # type: ignore[assignment]
    else:
        raise KeyGenerationError(
            f"Unsupported key type: {key_type}. Must be one of {SUPPORTED_KEY_TYPES}",
            context={"key_type": key_type, "supported_types": SUPPORTED_KEY_TYPES},
        )

    private_pem = priv.private_bytes(  # type: ignore[attr-defined]
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )
    public_pem = pub.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )
    return private_pem, public_pem


def x_generate_keypair__mutmut_5(
    key_type: KeyType,
    key_size: int | None = None,
    curve_name: str | None = None,
) -> tuple[bytes, bytes]:
    """Generate a key pair and return serialized keys.

    Args:
        key_type: Type of key ('rsa' or 'ec')
        key_size: RSA key size (for 'rsa' type)
        curve_name: EC curve name (for 'ec' type)

    Returns:
        Tuple of (private_key_pem, public_key_pem)

    Raises:
        KeyGenerationError: If key type is unsupported
    """
    from cryptography.hazmat.primitives import serialization

    if key_type == "rsa":
        priv, pub = generate_rsa_keypair(None)
    elif key_type == "ec":
        priv, pub = generate_ec_keypair(curve_name or DEFAULT_ECDSA_CURVE)  # type: ignore[assignment]
    else:
        raise KeyGenerationError(
            f"Unsupported key type: {key_type}. Must be one of {SUPPORTED_KEY_TYPES}",
            context={"key_type": key_type, "supported_types": SUPPORTED_KEY_TYPES},
        )

    private_pem = priv.private_bytes(  # type: ignore[attr-defined]
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )
    public_pem = pub.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )
    return private_pem, public_pem


def x_generate_keypair__mutmut_6(
    key_type: KeyType,
    key_size: int | None = None,
    curve_name: str | None = None,
) -> tuple[bytes, bytes]:
    """Generate a key pair and return serialized keys.

    Args:
        key_type: Type of key ('rsa' or 'ec')
        key_size: RSA key size (for 'rsa' type)
        curve_name: EC curve name (for 'ec' type)

    Returns:
        Tuple of (private_key_pem, public_key_pem)

    Raises:
        KeyGenerationError: If key type is unsupported
    """
    from cryptography.hazmat.primitives import serialization

    if key_type == "rsa":
        priv, pub = generate_rsa_keypair(key_size and DEFAULT_RSA_KEY_SIZE)
    elif key_type == "ec":
        priv, pub = generate_ec_keypair(curve_name or DEFAULT_ECDSA_CURVE)  # type: ignore[assignment]
    else:
        raise KeyGenerationError(
            f"Unsupported key type: {key_type}. Must be one of {SUPPORTED_KEY_TYPES}",
            context={"key_type": key_type, "supported_types": SUPPORTED_KEY_TYPES},
        )

    private_pem = priv.private_bytes(  # type: ignore[attr-defined]
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )
    public_pem = pub.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )
    return private_pem, public_pem


def x_generate_keypair__mutmut_7(
    key_type: KeyType,
    key_size: int | None = None,
    curve_name: str | None = None,
) -> tuple[bytes, bytes]:
    """Generate a key pair and return serialized keys.

    Args:
        key_type: Type of key ('rsa' or 'ec')
        key_size: RSA key size (for 'rsa' type)
        curve_name: EC curve name (for 'ec' type)

    Returns:
        Tuple of (private_key_pem, public_key_pem)

    Raises:
        KeyGenerationError: If key type is unsupported
    """
    from cryptography.hazmat.primitives import serialization

    if key_type == "rsa":
        priv, pub = generate_rsa_keypair(key_size or DEFAULT_RSA_KEY_SIZE)
    elif key_type != "ec":
        priv, pub = generate_ec_keypair(curve_name or DEFAULT_ECDSA_CURVE)  # type: ignore[assignment]
    else:
        raise KeyGenerationError(
            f"Unsupported key type: {key_type}. Must be one of {SUPPORTED_KEY_TYPES}",
            context={"key_type": key_type, "supported_types": SUPPORTED_KEY_TYPES},
        )

    private_pem = priv.private_bytes(  # type: ignore[attr-defined]
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )
    public_pem = pub.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )
    return private_pem, public_pem


def x_generate_keypair__mutmut_8(
    key_type: KeyType,
    key_size: int | None = None,
    curve_name: str | None = None,
) -> tuple[bytes, bytes]:
    """Generate a key pair and return serialized keys.

    Args:
        key_type: Type of key ('rsa' or 'ec')
        key_size: RSA key size (for 'rsa' type)
        curve_name: EC curve name (for 'ec' type)

    Returns:
        Tuple of (private_key_pem, public_key_pem)

    Raises:
        KeyGenerationError: If key type is unsupported
    """
    from cryptography.hazmat.primitives import serialization

    if key_type == "rsa":
        priv, pub = generate_rsa_keypair(key_size or DEFAULT_RSA_KEY_SIZE)
    elif key_type == "XXecXX":
        priv, pub = generate_ec_keypair(curve_name or DEFAULT_ECDSA_CURVE)  # type: ignore[assignment]
    else:
        raise KeyGenerationError(
            f"Unsupported key type: {key_type}. Must be one of {SUPPORTED_KEY_TYPES}",
            context={"key_type": key_type, "supported_types": SUPPORTED_KEY_TYPES},
        )

    private_pem = priv.private_bytes(  # type: ignore[attr-defined]
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )
    public_pem = pub.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )
    return private_pem, public_pem


def x_generate_keypair__mutmut_9(
    key_type: KeyType,
    key_size: int | None = None,
    curve_name: str | None = None,
) -> tuple[bytes, bytes]:
    """Generate a key pair and return serialized keys.

    Args:
        key_type: Type of key ('rsa' or 'ec')
        key_size: RSA key size (for 'rsa' type)
        curve_name: EC curve name (for 'ec' type)

    Returns:
        Tuple of (private_key_pem, public_key_pem)

    Raises:
        KeyGenerationError: If key type is unsupported
    """
    from cryptography.hazmat.primitives import serialization

    if key_type == "rsa":
        priv, pub = generate_rsa_keypair(key_size or DEFAULT_RSA_KEY_SIZE)
    elif key_type == "EC":
        priv, pub = generate_ec_keypair(curve_name or DEFAULT_ECDSA_CURVE)  # type: ignore[assignment]
    else:
        raise KeyGenerationError(
            f"Unsupported key type: {key_type}. Must be one of {SUPPORTED_KEY_TYPES}",
            context={"key_type": key_type, "supported_types": SUPPORTED_KEY_TYPES},
        )

    private_pem = priv.private_bytes(  # type: ignore[attr-defined]
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )
    public_pem = pub.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )
    return private_pem, public_pem


def x_generate_keypair__mutmut_10(
    key_type: KeyType,
    key_size: int | None = None,
    curve_name: str | None = None,
) -> tuple[bytes, bytes]:
    """Generate a key pair and return serialized keys.

    Args:
        key_type: Type of key ('rsa' or 'ec')
        key_size: RSA key size (for 'rsa' type)
        curve_name: EC curve name (for 'ec' type)

    Returns:
        Tuple of (private_key_pem, public_key_pem)

    Raises:
        KeyGenerationError: If key type is unsupported
    """
    from cryptography.hazmat.primitives import serialization

    if key_type == "rsa":
        priv, pub = generate_rsa_keypair(key_size or DEFAULT_RSA_KEY_SIZE)
    elif key_type == "ec":
        priv, pub = None  # type: ignore[assignment]
    else:
        raise KeyGenerationError(
            f"Unsupported key type: {key_type}. Must be one of {SUPPORTED_KEY_TYPES}",
            context={"key_type": key_type, "supported_types": SUPPORTED_KEY_TYPES},
        )

    private_pem = priv.private_bytes(  # type: ignore[attr-defined]
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )
    public_pem = pub.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )
    return private_pem, public_pem


def x_generate_keypair__mutmut_11(
    key_type: KeyType,
    key_size: int | None = None,
    curve_name: str | None = None,
) -> tuple[bytes, bytes]:
    """Generate a key pair and return serialized keys.

    Args:
        key_type: Type of key ('rsa' or 'ec')
        key_size: RSA key size (for 'rsa' type)
        curve_name: EC curve name (for 'ec' type)

    Returns:
        Tuple of (private_key_pem, public_key_pem)

    Raises:
        KeyGenerationError: If key type is unsupported
    """
    from cryptography.hazmat.primitives import serialization

    if key_type == "rsa":
        priv, pub = generate_rsa_keypair(key_size or DEFAULT_RSA_KEY_SIZE)
    elif key_type == "ec":
        priv, pub = generate_ec_keypair(None)  # type: ignore[assignment]
    else:
        raise KeyGenerationError(
            f"Unsupported key type: {key_type}. Must be one of {SUPPORTED_KEY_TYPES}",
            context={"key_type": key_type, "supported_types": SUPPORTED_KEY_TYPES},
        )

    private_pem = priv.private_bytes(  # type: ignore[attr-defined]
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )
    public_pem = pub.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )
    return private_pem, public_pem


def x_generate_keypair__mutmut_12(
    key_type: KeyType,
    key_size: int | None = None,
    curve_name: str | None = None,
) -> tuple[bytes, bytes]:
    """Generate a key pair and return serialized keys.

    Args:
        key_type: Type of key ('rsa' or 'ec')
        key_size: RSA key size (for 'rsa' type)
        curve_name: EC curve name (for 'ec' type)

    Returns:
        Tuple of (private_key_pem, public_key_pem)

    Raises:
        KeyGenerationError: If key type is unsupported
    """
    from cryptography.hazmat.primitives import serialization

    if key_type == "rsa":
        priv, pub = generate_rsa_keypair(key_size or DEFAULT_RSA_KEY_SIZE)
    elif key_type == "ec":
        priv, pub = generate_ec_keypair(curve_name and DEFAULT_ECDSA_CURVE)  # type: ignore[assignment]
    else:
        raise KeyGenerationError(
            f"Unsupported key type: {key_type}. Must be one of {SUPPORTED_KEY_TYPES}",
            context={"key_type": key_type, "supported_types": SUPPORTED_KEY_TYPES},
        )

    private_pem = priv.private_bytes(  # type: ignore[attr-defined]
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )
    public_pem = pub.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )
    return private_pem, public_pem


def x_generate_keypair__mutmut_13(
    key_type: KeyType,
    key_size: int | None = None,
    curve_name: str | None = None,
) -> tuple[bytes, bytes]:
    """Generate a key pair and return serialized keys.

    Args:
        key_type: Type of key ('rsa' or 'ec')
        key_size: RSA key size (for 'rsa' type)
        curve_name: EC curve name (for 'ec' type)

    Returns:
        Tuple of (private_key_pem, public_key_pem)

    Raises:
        KeyGenerationError: If key type is unsupported
    """
    from cryptography.hazmat.primitives import serialization

    if key_type == "rsa":
        priv, pub = generate_rsa_keypair(key_size or DEFAULT_RSA_KEY_SIZE)
    elif key_type == "ec":
        priv, pub = generate_ec_keypair(curve_name or DEFAULT_ECDSA_CURVE)  # type: ignore[assignment]
    else:
        raise KeyGenerationError(
            None,
            context={"key_type": key_type, "supported_types": SUPPORTED_KEY_TYPES},
        )

    private_pem = priv.private_bytes(  # type: ignore[attr-defined]
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )
    public_pem = pub.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )
    return private_pem, public_pem


def x_generate_keypair__mutmut_14(
    key_type: KeyType,
    key_size: int | None = None,
    curve_name: str | None = None,
) -> tuple[bytes, bytes]:
    """Generate a key pair and return serialized keys.

    Args:
        key_type: Type of key ('rsa' or 'ec')
        key_size: RSA key size (for 'rsa' type)
        curve_name: EC curve name (for 'ec' type)

    Returns:
        Tuple of (private_key_pem, public_key_pem)

    Raises:
        KeyGenerationError: If key type is unsupported
    """
    from cryptography.hazmat.primitives import serialization

    if key_type == "rsa":
        priv, pub = generate_rsa_keypair(key_size or DEFAULT_RSA_KEY_SIZE)
    elif key_type == "ec":
        priv, pub = generate_ec_keypair(curve_name or DEFAULT_ECDSA_CURVE)  # type: ignore[assignment]
    else:
        raise KeyGenerationError(
            f"Unsupported key type: {key_type}. Must be one of {SUPPORTED_KEY_TYPES}",
            context=None,
        )

    private_pem = priv.private_bytes(  # type: ignore[attr-defined]
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )
    public_pem = pub.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )
    return private_pem, public_pem


def x_generate_keypair__mutmut_15(
    key_type: KeyType,
    key_size: int | None = None,
    curve_name: str | None = None,
) -> tuple[bytes, bytes]:
    """Generate a key pair and return serialized keys.

    Args:
        key_type: Type of key ('rsa' or 'ec')
        key_size: RSA key size (for 'rsa' type)
        curve_name: EC curve name (for 'ec' type)

    Returns:
        Tuple of (private_key_pem, public_key_pem)

    Raises:
        KeyGenerationError: If key type is unsupported
    """
    from cryptography.hazmat.primitives import serialization

    if key_type == "rsa":
        priv, pub = generate_rsa_keypair(key_size or DEFAULT_RSA_KEY_SIZE)
    elif key_type == "ec":
        priv, pub = generate_ec_keypair(curve_name or DEFAULT_ECDSA_CURVE)  # type: ignore[assignment]
    else:
        raise KeyGenerationError(
            context={"key_type": key_type, "supported_types": SUPPORTED_KEY_TYPES},
        )

    private_pem = priv.private_bytes(  # type: ignore[attr-defined]
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )
    public_pem = pub.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )
    return private_pem, public_pem


def x_generate_keypair__mutmut_16(
    key_type: KeyType,
    key_size: int | None = None,
    curve_name: str | None = None,
) -> tuple[bytes, bytes]:
    """Generate a key pair and return serialized keys.

    Args:
        key_type: Type of key ('rsa' or 'ec')
        key_size: RSA key size (for 'rsa' type)
        curve_name: EC curve name (for 'ec' type)

    Returns:
        Tuple of (private_key_pem, public_key_pem)

    Raises:
        KeyGenerationError: If key type is unsupported
    """
    from cryptography.hazmat.primitives import serialization

    if key_type == "rsa":
        priv, pub = generate_rsa_keypair(key_size or DEFAULT_RSA_KEY_SIZE)
    elif key_type == "ec":
        priv, pub = generate_ec_keypair(curve_name or DEFAULT_ECDSA_CURVE)  # type: ignore[assignment]
    else:
        raise KeyGenerationError(
            f"Unsupported key type: {key_type}. Must be one of {SUPPORTED_KEY_TYPES}",
        )

    private_pem = priv.private_bytes(  # type: ignore[attr-defined]
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )
    public_pem = pub.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )
    return private_pem, public_pem


def x_generate_keypair__mutmut_17(
    key_type: KeyType,
    key_size: int | None = None,
    curve_name: str | None = None,
) -> tuple[bytes, bytes]:
    """Generate a key pair and return serialized keys.

    Args:
        key_type: Type of key ('rsa' or 'ec')
        key_size: RSA key size (for 'rsa' type)
        curve_name: EC curve name (for 'ec' type)

    Returns:
        Tuple of (private_key_pem, public_key_pem)

    Raises:
        KeyGenerationError: If key type is unsupported
    """
    from cryptography.hazmat.primitives import serialization

    if key_type == "rsa":
        priv, pub = generate_rsa_keypair(key_size or DEFAULT_RSA_KEY_SIZE)
    elif key_type == "ec":
        priv, pub = generate_ec_keypair(curve_name or DEFAULT_ECDSA_CURVE)  # type: ignore[assignment]
    else:
        raise KeyGenerationError(
            f"Unsupported key type: {key_type}. Must be one of {SUPPORTED_KEY_TYPES}",
            context={"XXkey_typeXX": key_type, "supported_types": SUPPORTED_KEY_TYPES},
        )

    private_pem = priv.private_bytes(  # type: ignore[attr-defined]
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )
    public_pem = pub.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )
    return private_pem, public_pem


def x_generate_keypair__mutmut_18(
    key_type: KeyType,
    key_size: int | None = None,
    curve_name: str | None = None,
) -> tuple[bytes, bytes]:
    """Generate a key pair and return serialized keys.

    Args:
        key_type: Type of key ('rsa' or 'ec')
        key_size: RSA key size (for 'rsa' type)
        curve_name: EC curve name (for 'ec' type)

    Returns:
        Tuple of (private_key_pem, public_key_pem)

    Raises:
        KeyGenerationError: If key type is unsupported
    """
    from cryptography.hazmat.primitives import serialization

    if key_type == "rsa":
        priv, pub = generate_rsa_keypair(key_size or DEFAULT_RSA_KEY_SIZE)
    elif key_type == "ec":
        priv, pub = generate_ec_keypair(curve_name or DEFAULT_ECDSA_CURVE)  # type: ignore[assignment]
    else:
        raise KeyGenerationError(
            f"Unsupported key type: {key_type}. Must be one of {SUPPORTED_KEY_TYPES}",
            context={"KEY_TYPE": key_type, "supported_types": SUPPORTED_KEY_TYPES},
        )

    private_pem = priv.private_bytes(  # type: ignore[attr-defined]
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )
    public_pem = pub.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )
    return private_pem, public_pem


def x_generate_keypair__mutmut_19(
    key_type: KeyType,
    key_size: int | None = None,
    curve_name: str | None = None,
) -> tuple[bytes, bytes]:
    """Generate a key pair and return serialized keys.

    Args:
        key_type: Type of key ('rsa' or 'ec')
        key_size: RSA key size (for 'rsa' type)
        curve_name: EC curve name (for 'ec' type)

    Returns:
        Tuple of (private_key_pem, public_key_pem)

    Raises:
        KeyGenerationError: If key type is unsupported
    """
    from cryptography.hazmat.primitives import serialization

    if key_type == "rsa":
        priv, pub = generate_rsa_keypair(key_size or DEFAULT_RSA_KEY_SIZE)
    elif key_type == "ec":
        priv, pub = generate_ec_keypair(curve_name or DEFAULT_ECDSA_CURVE)  # type: ignore[assignment]
    else:
        raise KeyGenerationError(
            f"Unsupported key type: {key_type}. Must be one of {SUPPORTED_KEY_TYPES}",
            context={"key_type": key_type, "XXsupported_typesXX": SUPPORTED_KEY_TYPES},
        )

    private_pem = priv.private_bytes(  # type: ignore[attr-defined]
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )
    public_pem = pub.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )
    return private_pem, public_pem


def x_generate_keypair__mutmut_20(
    key_type: KeyType,
    key_size: int | None = None,
    curve_name: str | None = None,
) -> tuple[bytes, bytes]:
    """Generate a key pair and return serialized keys.

    Args:
        key_type: Type of key ('rsa' or 'ec')
        key_size: RSA key size (for 'rsa' type)
        curve_name: EC curve name (for 'ec' type)

    Returns:
        Tuple of (private_key_pem, public_key_pem)

    Raises:
        KeyGenerationError: If key type is unsupported
    """
    from cryptography.hazmat.primitives import serialization

    if key_type == "rsa":
        priv, pub = generate_rsa_keypair(key_size or DEFAULT_RSA_KEY_SIZE)
    elif key_type == "ec":
        priv, pub = generate_ec_keypair(curve_name or DEFAULT_ECDSA_CURVE)  # type: ignore[assignment]
    else:
        raise KeyGenerationError(
            f"Unsupported key type: {key_type}. Must be one of {SUPPORTED_KEY_TYPES}",
            context={"key_type": key_type, "SUPPORTED_TYPES": SUPPORTED_KEY_TYPES},
        )

    private_pem = priv.private_bytes(  # type: ignore[attr-defined]
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )
    public_pem = pub.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )
    return private_pem, public_pem


def x_generate_keypair__mutmut_21(
    key_type: KeyType,
    key_size: int | None = None,
    curve_name: str | None = None,
) -> tuple[bytes, bytes]:
    """Generate a key pair and return serialized keys.

    Args:
        key_type: Type of key ('rsa' or 'ec')
        key_size: RSA key size (for 'rsa' type)
        curve_name: EC curve name (for 'ec' type)

    Returns:
        Tuple of (private_key_pem, public_key_pem)

    Raises:
        KeyGenerationError: If key type is unsupported
    """
    from cryptography.hazmat.primitives import serialization

    if key_type == "rsa":
        priv, pub = generate_rsa_keypair(key_size or DEFAULT_RSA_KEY_SIZE)
    elif key_type == "ec":
        priv, pub = generate_ec_keypair(curve_name or DEFAULT_ECDSA_CURVE)  # type: ignore[assignment]
    else:
        raise KeyGenerationError(
            f"Unsupported key type: {key_type}. Must be one of {SUPPORTED_KEY_TYPES}",
            context={"key_type": key_type, "supported_types": SUPPORTED_KEY_TYPES},
        )

    private_pem = None
    public_pem = pub.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )
    return private_pem, public_pem


def x_generate_keypair__mutmut_22(
    key_type: KeyType,
    key_size: int | None = None,
    curve_name: str | None = None,
) -> tuple[bytes, bytes]:
    """Generate a key pair and return serialized keys.

    Args:
        key_type: Type of key ('rsa' or 'ec')
        key_size: RSA key size (for 'rsa' type)
        curve_name: EC curve name (for 'ec' type)

    Returns:
        Tuple of (private_key_pem, public_key_pem)

    Raises:
        KeyGenerationError: If key type is unsupported
    """
    from cryptography.hazmat.primitives import serialization

    if key_type == "rsa":
        priv, pub = generate_rsa_keypair(key_size or DEFAULT_RSA_KEY_SIZE)
    elif key_type == "ec":
        priv, pub = generate_ec_keypair(curve_name or DEFAULT_ECDSA_CURVE)  # type: ignore[assignment]
    else:
        raise KeyGenerationError(
            f"Unsupported key type: {key_type}. Must be one of {SUPPORTED_KEY_TYPES}",
            context={"key_type": key_type, "supported_types": SUPPORTED_KEY_TYPES},
        )

    private_pem = priv.private_bytes(  # type: ignore[attr-defined]
        encoding=None,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )
    public_pem = pub.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )
    return private_pem, public_pem


def x_generate_keypair__mutmut_23(
    key_type: KeyType,
    key_size: int | None = None,
    curve_name: str | None = None,
) -> tuple[bytes, bytes]:
    """Generate a key pair and return serialized keys.

    Args:
        key_type: Type of key ('rsa' or 'ec')
        key_size: RSA key size (for 'rsa' type)
        curve_name: EC curve name (for 'ec' type)

    Returns:
        Tuple of (private_key_pem, public_key_pem)

    Raises:
        KeyGenerationError: If key type is unsupported
    """
    from cryptography.hazmat.primitives import serialization

    if key_type == "rsa":
        priv, pub = generate_rsa_keypair(key_size or DEFAULT_RSA_KEY_SIZE)
    elif key_type == "ec":
        priv, pub = generate_ec_keypair(curve_name or DEFAULT_ECDSA_CURVE)  # type: ignore[assignment]
    else:
        raise KeyGenerationError(
            f"Unsupported key type: {key_type}. Must be one of {SUPPORTED_KEY_TYPES}",
            context={"key_type": key_type, "supported_types": SUPPORTED_KEY_TYPES},
        )

    private_pem = priv.private_bytes(  # type: ignore[attr-defined]
        encoding=serialization.Encoding.PEM,
        format=None,
        encryption_algorithm=serialization.NoEncryption(),
    )
    public_pem = pub.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )
    return private_pem, public_pem


def x_generate_keypair__mutmut_24(
    key_type: KeyType,
    key_size: int | None = None,
    curve_name: str | None = None,
) -> tuple[bytes, bytes]:
    """Generate a key pair and return serialized keys.

    Args:
        key_type: Type of key ('rsa' or 'ec')
        key_size: RSA key size (for 'rsa' type)
        curve_name: EC curve name (for 'ec' type)

    Returns:
        Tuple of (private_key_pem, public_key_pem)

    Raises:
        KeyGenerationError: If key type is unsupported
    """
    from cryptography.hazmat.primitives import serialization

    if key_type == "rsa":
        priv, pub = generate_rsa_keypair(key_size or DEFAULT_RSA_KEY_SIZE)
    elif key_type == "ec":
        priv, pub = generate_ec_keypair(curve_name or DEFAULT_ECDSA_CURVE)  # type: ignore[assignment]
    else:
        raise KeyGenerationError(
            f"Unsupported key type: {key_type}. Must be one of {SUPPORTED_KEY_TYPES}",
            context={"key_type": key_type, "supported_types": SUPPORTED_KEY_TYPES},
        )

    private_pem = priv.private_bytes(  # type: ignore[attr-defined]
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=None,
    )
    public_pem = pub.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )
    return private_pem, public_pem


def x_generate_keypair__mutmut_25(
    key_type: KeyType,
    key_size: int | None = None,
    curve_name: str | None = None,
) -> tuple[bytes, bytes]:
    """Generate a key pair and return serialized keys.

    Args:
        key_type: Type of key ('rsa' or 'ec')
        key_size: RSA key size (for 'rsa' type)
        curve_name: EC curve name (for 'ec' type)

    Returns:
        Tuple of (private_key_pem, public_key_pem)

    Raises:
        KeyGenerationError: If key type is unsupported
    """
    from cryptography.hazmat.primitives import serialization

    if key_type == "rsa":
        priv, pub = generate_rsa_keypair(key_size or DEFAULT_RSA_KEY_SIZE)
    elif key_type == "ec":
        priv, pub = generate_ec_keypair(curve_name or DEFAULT_ECDSA_CURVE)  # type: ignore[assignment]
    else:
        raise KeyGenerationError(
            f"Unsupported key type: {key_type}. Must be one of {SUPPORTED_KEY_TYPES}",
            context={"key_type": key_type, "supported_types": SUPPORTED_KEY_TYPES},
        )

    private_pem = priv.private_bytes(  # type: ignore[attr-defined]
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )
    public_pem = pub.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )
    return private_pem, public_pem


def x_generate_keypair__mutmut_26(
    key_type: KeyType,
    key_size: int | None = None,
    curve_name: str | None = None,
) -> tuple[bytes, bytes]:
    """Generate a key pair and return serialized keys.

    Args:
        key_type: Type of key ('rsa' or 'ec')
        key_size: RSA key size (for 'rsa' type)
        curve_name: EC curve name (for 'ec' type)

    Returns:
        Tuple of (private_key_pem, public_key_pem)

    Raises:
        KeyGenerationError: If key type is unsupported
    """
    from cryptography.hazmat.primitives import serialization

    if key_type == "rsa":
        priv, pub = generate_rsa_keypair(key_size or DEFAULT_RSA_KEY_SIZE)
    elif key_type == "ec":
        priv, pub = generate_ec_keypair(curve_name or DEFAULT_ECDSA_CURVE)  # type: ignore[assignment]
    else:
        raise KeyGenerationError(
            f"Unsupported key type: {key_type}. Must be one of {SUPPORTED_KEY_TYPES}",
            context={"key_type": key_type, "supported_types": SUPPORTED_KEY_TYPES},
        )

    private_pem = priv.private_bytes(  # type: ignore[attr-defined]
        encoding=serialization.Encoding.PEM,
        encryption_algorithm=serialization.NoEncryption(),
    )
    public_pem = pub.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )
    return private_pem, public_pem


def x_generate_keypair__mutmut_27(
    key_type: KeyType,
    key_size: int | None = None,
    curve_name: str | None = None,
) -> tuple[bytes, bytes]:
    """Generate a key pair and return serialized keys.

    Args:
        key_type: Type of key ('rsa' or 'ec')
        key_size: RSA key size (for 'rsa' type)
        curve_name: EC curve name (for 'ec' type)

    Returns:
        Tuple of (private_key_pem, public_key_pem)

    Raises:
        KeyGenerationError: If key type is unsupported
    """
    from cryptography.hazmat.primitives import serialization

    if key_type == "rsa":
        priv, pub = generate_rsa_keypair(key_size or DEFAULT_RSA_KEY_SIZE)
    elif key_type == "ec":
        priv, pub = generate_ec_keypair(curve_name or DEFAULT_ECDSA_CURVE)  # type: ignore[assignment]
    else:
        raise KeyGenerationError(
            f"Unsupported key type: {key_type}. Must be one of {SUPPORTED_KEY_TYPES}",
            context={"key_type": key_type, "supported_types": SUPPORTED_KEY_TYPES},
        )

    private_pem = priv.private_bytes(  # type: ignore[attr-defined]
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
    )
    public_pem = pub.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )
    return private_pem, public_pem


def x_generate_keypair__mutmut_28(
    key_type: KeyType,
    key_size: int | None = None,
    curve_name: str | None = None,
) -> tuple[bytes, bytes]:
    """Generate a key pair and return serialized keys.

    Args:
        key_type: Type of key ('rsa' or 'ec')
        key_size: RSA key size (for 'rsa' type)
        curve_name: EC curve name (for 'ec' type)

    Returns:
        Tuple of (private_key_pem, public_key_pem)

    Raises:
        KeyGenerationError: If key type is unsupported
    """
    from cryptography.hazmat.primitives import serialization

    if key_type == "rsa":
        priv, pub = generate_rsa_keypair(key_size or DEFAULT_RSA_KEY_SIZE)
    elif key_type == "ec":
        priv, pub = generate_ec_keypair(curve_name or DEFAULT_ECDSA_CURVE)  # type: ignore[assignment]
    else:
        raise KeyGenerationError(
            f"Unsupported key type: {key_type}. Must be one of {SUPPORTED_KEY_TYPES}",
            context={"key_type": key_type, "supported_types": SUPPORTED_KEY_TYPES},
        )

    private_pem = priv.private_bytes(  # type: ignore[attr-defined]
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )
    public_pem = None
    return private_pem, public_pem


def x_generate_keypair__mutmut_29(
    key_type: KeyType,
    key_size: int | None = None,
    curve_name: str | None = None,
) -> tuple[bytes, bytes]:
    """Generate a key pair and return serialized keys.

    Args:
        key_type: Type of key ('rsa' or 'ec')
        key_size: RSA key size (for 'rsa' type)
        curve_name: EC curve name (for 'ec' type)

    Returns:
        Tuple of (private_key_pem, public_key_pem)

    Raises:
        KeyGenerationError: If key type is unsupported
    """
    from cryptography.hazmat.primitives import serialization

    if key_type == "rsa":
        priv, pub = generate_rsa_keypair(key_size or DEFAULT_RSA_KEY_SIZE)
    elif key_type == "ec":
        priv, pub = generate_ec_keypair(curve_name or DEFAULT_ECDSA_CURVE)  # type: ignore[assignment]
    else:
        raise KeyGenerationError(
            f"Unsupported key type: {key_type}. Must be one of {SUPPORTED_KEY_TYPES}",
            context={"key_type": key_type, "supported_types": SUPPORTED_KEY_TYPES},
        )

    private_pem = priv.private_bytes(  # type: ignore[attr-defined]
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )
    public_pem = pub.public_bytes(
        encoding=None,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )
    return private_pem, public_pem


def x_generate_keypair__mutmut_30(
    key_type: KeyType,
    key_size: int | None = None,
    curve_name: str | None = None,
) -> tuple[bytes, bytes]:
    """Generate a key pair and return serialized keys.

    Args:
        key_type: Type of key ('rsa' or 'ec')
        key_size: RSA key size (for 'rsa' type)
        curve_name: EC curve name (for 'ec' type)

    Returns:
        Tuple of (private_key_pem, public_key_pem)

    Raises:
        KeyGenerationError: If key type is unsupported
    """
    from cryptography.hazmat.primitives import serialization

    if key_type == "rsa":
        priv, pub = generate_rsa_keypair(key_size or DEFAULT_RSA_KEY_SIZE)
    elif key_type == "ec":
        priv, pub = generate_ec_keypair(curve_name or DEFAULT_ECDSA_CURVE)  # type: ignore[assignment]
    else:
        raise KeyGenerationError(
            f"Unsupported key type: {key_type}. Must be one of {SUPPORTED_KEY_TYPES}",
            context={"key_type": key_type, "supported_types": SUPPORTED_KEY_TYPES},
        )

    private_pem = priv.private_bytes(  # type: ignore[attr-defined]
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )
    public_pem = pub.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=None,
    )
    return private_pem, public_pem


def x_generate_keypair__mutmut_31(
    key_type: KeyType,
    key_size: int | None = None,
    curve_name: str | None = None,
) -> tuple[bytes, bytes]:
    """Generate a key pair and return serialized keys.

    Args:
        key_type: Type of key ('rsa' or 'ec')
        key_size: RSA key size (for 'rsa' type)
        curve_name: EC curve name (for 'ec' type)

    Returns:
        Tuple of (private_key_pem, public_key_pem)

    Raises:
        KeyGenerationError: If key type is unsupported
    """
    from cryptography.hazmat.primitives import serialization

    if key_type == "rsa":
        priv, pub = generate_rsa_keypair(key_size or DEFAULT_RSA_KEY_SIZE)
    elif key_type == "ec":
        priv, pub = generate_ec_keypair(curve_name or DEFAULT_ECDSA_CURVE)  # type: ignore[assignment]
    else:
        raise KeyGenerationError(
            f"Unsupported key type: {key_type}. Must be one of {SUPPORTED_KEY_TYPES}",
            context={"key_type": key_type, "supported_types": SUPPORTED_KEY_TYPES},
        )

    private_pem = priv.private_bytes(  # type: ignore[attr-defined]
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )
    public_pem = pub.public_bytes(
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )
    return private_pem, public_pem


def x_generate_keypair__mutmut_32(
    key_type: KeyType,
    key_size: int | None = None,
    curve_name: str | None = None,
) -> tuple[bytes, bytes]:
    """Generate a key pair and return serialized keys.

    Args:
        key_type: Type of key ('rsa' or 'ec')
        key_size: RSA key size (for 'rsa' type)
        curve_name: EC curve name (for 'ec' type)

    Returns:
        Tuple of (private_key_pem, public_key_pem)

    Raises:
        KeyGenerationError: If key type is unsupported
    """
    from cryptography.hazmat.primitives import serialization

    if key_type == "rsa":
        priv, pub = generate_rsa_keypair(key_size or DEFAULT_RSA_KEY_SIZE)
    elif key_type == "ec":
        priv, pub = generate_ec_keypair(curve_name or DEFAULT_ECDSA_CURVE)  # type: ignore[assignment]
    else:
        raise KeyGenerationError(
            f"Unsupported key type: {key_type}. Must be one of {SUPPORTED_KEY_TYPES}",
            context={"key_type": key_type, "supported_types": SUPPORTED_KEY_TYPES},
        )

    private_pem = priv.private_bytes(  # type: ignore[attr-defined]
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )
    public_pem = pub.public_bytes(
        encoding=serialization.Encoding.PEM,
    )
    return private_pem, public_pem


x_generate_keypair__mutmut_mutants: ClassVar[MutantDict] = {
    "x_generate_keypair__mutmut_1": x_generate_keypair__mutmut_1,
    "x_generate_keypair__mutmut_2": x_generate_keypair__mutmut_2,
    "x_generate_keypair__mutmut_3": x_generate_keypair__mutmut_3,
    "x_generate_keypair__mutmut_4": x_generate_keypair__mutmut_4,
    "x_generate_keypair__mutmut_5": x_generate_keypair__mutmut_5,
    "x_generate_keypair__mutmut_6": x_generate_keypair__mutmut_6,
    "x_generate_keypair__mutmut_7": x_generate_keypair__mutmut_7,
    "x_generate_keypair__mutmut_8": x_generate_keypair__mutmut_8,
    "x_generate_keypair__mutmut_9": x_generate_keypair__mutmut_9,
    "x_generate_keypair__mutmut_10": x_generate_keypair__mutmut_10,
    "x_generate_keypair__mutmut_11": x_generate_keypair__mutmut_11,
    "x_generate_keypair__mutmut_12": x_generate_keypair__mutmut_12,
    "x_generate_keypair__mutmut_13": x_generate_keypair__mutmut_13,
    "x_generate_keypair__mutmut_14": x_generate_keypair__mutmut_14,
    "x_generate_keypair__mutmut_15": x_generate_keypair__mutmut_15,
    "x_generate_keypair__mutmut_16": x_generate_keypair__mutmut_16,
    "x_generate_keypair__mutmut_17": x_generate_keypair__mutmut_17,
    "x_generate_keypair__mutmut_18": x_generate_keypair__mutmut_18,
    "x_generate_keypair__mutmut_19": x_generate_keypair__mutmut_19,
    "x_generate_keypair__mutmut_20": x_generate_keypair__mutmut_20,
    "x_generate_keypair__mutmut_21": x_generate_keypair__mutmut_21,
    "x_generate_keypair__mutmut_22": x_generate_keypair__mutmut_22,
    "x_generate_keypair__mutmut_23": x_generate_keypair__mutmut_23,
    "x_generate_keypair__mutmut_24": x_generate_keypair__mutmut_24,
    "x_generate_keypair__mutmut_25": x_generate_keypair__mutmut_25,
    "x_generate_keypair__mutmut_26": x_generate_keypair__mutmut_26,
    "x_generate_keypair__mutmut_27": x_generate_keypair__mutmut_27,
    "x_generate_keypair__mutmut_28": x_generate_keypair__mutmut_28,
    "x_generate_keypair__mutmut_29": x_generate_keypair__mutmut_29,
    "x_generate_keypair__mutmut_30": x_generate_keypair__mutmut_30,
    "x_generate_keypair__mutmut_31": x_generate_keypair__mutmut_31,
    "x_generate_keypair__mutmut_32": x_generate_keypair__mutmut_32,
}


def generate_keypair(*args, **kwargs):
    result = _mutmut_trampoline(
        x_generate_keypair__mutmut_orig, x_generate_keypair__mutmut_mutants, args, kwargs
    )
    return result


generate_keypair.__signature__ = _mutmut_signature(x_generate_keypair__mutmut_orig)
x_generate_keypair__mutmut_orig.__name__ = "x_generate_keypair"


def generate_signing_keypair() -> KeypairTuple:
    """Generate a key pair suitable for digital signatures (Ed25519).

    This is an alias for `generate_ed25519_keypair`.

    Returns:
        A tuple containing (private_key_bytes, public_key_bytes).
    """
    return generate_ed25519_keypair()


def x_generate_tls_keypair__mutmut_orig(
    key_type: Literal["rsa", "ec"] = "ec",
) -> tuple[bytes, bytes]:
    """Generate a key pair suitable for TLS.

    Args:
        key_type: Type of key ('rsa' or 'ec')

    Returns:
        Tuple of (private_key_pem, public_key_pem)
    """
    return generate_keypair(key_type)


def x_generate_tls_keypair__mutmut_1(
    key_type: Literal["rsa", "ec"] = "XXecXX",
) -> tuple[bytes, bytes]:
    """Generate a key pair suitable for TLS.

    Args:
        key_type: Type of key ('rsa' or 'ec')

    Returns:
        Tuple of (private_key_pem, public_key_pem)
    """
    return generate_keypair(key_type)


def x_generate_tls_keypair__mutmut_2(
    key_type: Literal["rsa", "ec"] = "EC",
) -> tuple[bytes, bytes]:
    """Generate a key pair suitable for TLS.

    Args:
        key_type: Type of key ('rsa' or 'ec')

    Returns:
        Tuple of (private_key_pem, public_key_pem)
    """
    return generate_keypair(key_type)


def x_generate_tls_keypair__mutmut_3(
    key_type: Literal["rsa", "ec"] = "ec",
) -> tuple[bytes, bytes]:
    """Generate a key pair suitable for TLS.

    Args:
        key_type: Type of key ('rsa' or 'ec')

    Returns:
        Tuple of (private_key_pem, public_key_pem)
    """
    return generate_keypair(None)


x_generate_tls_keypair__mutmut_mutants: ClassVar[MutantDict] = {
    "x_generate_tls_keypair__mutmut_1": x_generate_tls_keypair__mutmut_1,
    "x_generate_tls_keypair__mutmut_2": x_generate_tls_keypair__mutmut_2,
    "x_generate_tls_keypair__mutmut_3": x_generate_tls_keypair__mutmut_3,
}


def generate_tls_keypair(*args, **kwargs):
    result = _mutmut_trampoline(
        x_generate_tls_keypair__mutmut_orig, x_generate_tls_keypair__mutmut_mutants, args, kwargs
    )
    return result


generate_tls_keypair.__signature__ = _mutmut_signature(x_generate_tls_keypair__mutmut_orig)
x_generate_tls_keypair__mutmut_orig.__name__ = "x_generate_tls_keypair"


__all__ = [
    "KeyGenerationError",
    "generate_ec_keypair",
    "generate_ed25519_keypair",
    "generate_keypair",
    "generate_rsa_keypair",
    "generate_signing_keypair",
    "generate_tls_keypair",
]


# <3 🧱🤝🔒🪄
