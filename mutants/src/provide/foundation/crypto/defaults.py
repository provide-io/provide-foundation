# provide/foundation/crypto/defaults.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from typing import Final

"""Crypto configuration defaults and constants for Foundation.

This module contains all cryptographic defaults, constants, and configuration
values for the crypto subsystem.
"""

# =================================
# Ed25519 Constants
# =================================
ED25519_PRIVATE_KEY_SIZE: Final[int] = 32
ED25519_PUBLIC_KEY_SIZE: Final[int] = 32
ED25519_SIGNATURE_SIZE: Final[int] = 64

# =================================
# RSA Defaults and Constants
# =================================
DEFAULT_RSA_KEY_SIZE: Final[int] = 2048
SUPPORTED_RSA_SIZES: Final[set[int]] = {2048, 3072, 4096}

# =================================
# ECDSA Defaults and Constants
# =================================
DEFAULT_ECDSA_CURVE: Final[str] = "secp384r1"
SUPPORTED_EC_CURVES: Final[set[str]] = {
    "secp256r1",
    "secp384r1",
    "secp521r1",
}

# =================================
# Key Type Constants
# =================================
SUPPORTED_KEY_TYPES: Final[set[str]] = {"rsa", "ecdsa", "ed25519"}

# =================================
# Algorithm Defaults
# =================================
DEFAULT_SIGNATURE_ALGORITHM: Final[str] = "ed25519"  # Modern default for new code
DEFAULT_CERTIFICATE_KEY_TYPE: Final[str] = "ecdsa"  # Good balance for TLS/PKI
DEFAULT_CERTIFICATE_CURVE: Final[str] = DEFAULT_ECDSA_CURVE

# =================================
# Certificate Defaults
# =================================
DEFAULT_CERTIFICATE_VALIDITY_DAYS: Final[int] = 365
MIN_CERTIFICATE_VALIDITY_DAYS: Final[int] = 1
MAX_CERTIFICATE_VALIDITY_DAYS: Final[int] = 3650  # 10 years
DEFAULT_CERTIFICATE_COMMON_NAME: Final[str] = "localhost"
DEFAULT_CERTIFICATE_ORGANIZATION_NAME: Final[str] = "Default Organization"
DEFAULT_CERTIFICATE_GENERATE_KEYPAIR: Final[bool] = False
from inspect import signature as _mutmut_signature
from typing import Annotated
from typing import Callable
from typing import ClassVar


MutantDict = Annotated[dict[str, Callable], "Mutant"]


def _mutmut_trampoline(orig, mutants, call_args, call_kwargs, self_arg = None):
    """Forward call to original or mutated function, depending on the environment"""
    import os
    mutant_under_test = os.environ['MUTANT_UNDER_TEST']
    if mutant_under_test == 'fail':
        from mutmut.__main__ import MutmutProgrammaticFailException
        raise MutmutProgrammaticFailException('Failed programmatically')      
    elif mutant_under_test == 'stats':
        from mutmut.__main__ import record_trampoline_hit
        record_trampoline_hit(orig.__module__ + '.' + orig.__name__)
        result = orig(*call_args, **call_kwargs)
        return result
    prefix = orig.__module__ + '.' + orig.__name__ + '__mutmut_'
    if not mutant_under_test.startswith(prefix):
        result = orig(*call_args, **call_kwargs)
        return result
    mutant_name = mutant_under_test.rpartition('.')[-1]
    if self_arg:
        # call to a class method where self is not bound
        result = mutants[mutant_name](self_arg, *call_args, **call_kwargs)
    else:
        result = mutants[mutant_name](*call_args, **call_kwargs)
    return result

# =================================
# Factory Functions
# =================================


def x_default_certificate_alt_names__mutmut_orig() -> list[str]:
    """Factory for default certificate alternative names."""
    return ["localhost"]

# =================================
# Factory Functions
# =================================


def x_default_certificate_alt_names__mutmut_1() -> list[str]:
    """Factory for default certificate alternative names."""
    return ["XXlocalhostXX"]

# =================================
# Factory Functions
# =================================


def x_default_certificate_alt_names__mutmut_2() -> list[str]:
    """Factory for default certificate alternative names."""
    return ["LOCALHOST"]

x_default_certificate_alt_names__mutmut_mutants : ClassVar[MutantDict] = {
'x_default_certificate_alt_names__mutmut_1': x_default_certificate_alt_names__mutmut_1, 
    'x_default_certificate_alt_names__mutmut_2': x_default_certificate_alt_names__mutmut_2
}

def default_certificate_alt_names(*args, **kwargs):
    result = _mutmut_trampoline(x_default_certificate_alt_names__mutmut_orig, x_default_certificate_alt_names__mutmut_mutants, args, kwargs)
    return result 

default_certificate_alt_names.__signature__ = _mutmut_signature(x_default_certificate_alt_names__mutmut_orig)
x_default_certificate_alt_names__mutmut_orig.__name__ = 'x_default_certificate_alt_names'


def default_supported_ec_curves() -> set[str]:
    """Factory for supported EC curves set."""
    return SUPPORTED_EC_CURVES.copy()


def default_supported_key_types() -> set[str]:
    """Factory for supported key types set."""
    return SUPPORTED_KEY_TYPES.copy()


def default_supported_rsa_sizes() -> set[int]:
    """Factory for supported RSA sizes set."""
    return SUPPORTED_RSA_SIZES.copy()


# =================================
# Config Integration
# =================================


def x__get_config_value__mutmut_orig(key: str, default: str | int) -> str | int:
    """Get crypto config value with fallback to default."""
    try:
        from provide.foundation.config import get_config

        config = get_config(f"crypto.{key}")
        if config is not None and hasattr(config, "value"):
            value = config.value
            # Cast to str | int based on default type
            if isinstance(default, int):
                return int(value) if isinstance(value, (int, str)) else default
            return str(value) if value is not None else default
        return default
    except ImportError:
        # Config system not available, use defaults
        return default


# =================================
# Config Integration
# =================================


def x__get_config_value__mutmut_1(key: str, default: str | int) -> str | int:
    """Get crypto config value with fallback to default."""
    try:
        from provide.foundation.config import get_config

        config = None
        if config is not None and hasattr(config, "value"):
            value = config.value
            # Cast to str | int based on default type
            if isinstance(default, int):
                return int(value) if isinstance(value, (int, str)) else default
            return str(value) if value is not None else default
        return default
    except ImportError:
        # Config system not available, use defaults
        return default


# =================================
# Config Integration
# =================================


def x__get_config_value__mutmut_2(key: str, default: str | int) -> str | int:
    """Get crypto config value with fallback to default."""
    try:
        from provide.foundation.config import get_config

        config = get_config(None)
        if config is not None and hasattr(config, "value"):
            value = config.value
            # Cast to str | int based on default type
            if isinstance(default, int):
                return int(value) if isinstance(value, (int, str)) else default
            return str(value) if value is not None else default
        return default
    except ImportError:
        # Config system not available, use defaults
        return default


# =================================
# Config Integration
# =================================


def x__get_config_value__mutmut_3(key: str, default: str | int) -> str | int:
    """Get crypto config value with fallback to default."""
    try:
        from provide.foundation.config import get_config

        config = get_config(f"crypto.{key}")
        if config is not None or hasattr(config, "value"):
            value = config.value
            # Cast to str | int based on default type
            if isinstance(default, int):
                return int(value) if isinstance(value, (int, str)) else default
            return str(value) if value is not None else default
        return default
    except ImportError:
        # Config system not available, use defaults
        return default


# =================================
# Config Integration
# =================================


def x__get_config_value__mutmut_4(key: str, default: str | int) -> str | int:
    """Get crypto config value with fallback to default."""
    try:
        from provide.foundation.config import get_config

        config = get_config(f"crypto.{key}")
        if config is None and hasattr(config, "value"):
            value = config.value
            # Cast to str | int based on default type
            if isinstance(default, int):
                return int(value) if isinstance(value, (int, str)) else default
            return str(value) if value is not None else default
        return default
    except ImportError:
        # Config system not available, use defaults
        return default


# =================================
# Config Integration
# =================================


def x__get_config_value__mutmut_5(key: str, default: str | int) -> str | int:
    """Get crypto config value with fallback to default."""
    try:
        from provide.foundation.config import get_config

        config = get_config(f"crypto.{key}")
        if config is not None and hasattr(None, "value"):
            value = config.value
            # Cast to str | int based on default type
            if isinstance(default, int):
                return int(value) if isinstance(value, (int, str)) else default
            return str(value) if value is not None else default
        return default
    except ImportError:
        # Config system not available, use defaults
        return default


# =================================
# Config Integration
# =================================


def x__get_config_value__mutmut_6(key: str, default: str | int) -> str | int:
    """Get crypto config value with fallback to default."""
    try:
        from provide.foundation.config import get_config

        config = get_config(f"crypto.{key}")
        if config is not None and hasattr(config, None):
            value = config.value
            # Cast to str | int based on default type
            if isinstance(default, int):
                return int(value) if isinstance(value, (int, str)) else default
            return str(value) if value is not None else default
        return default
    except ImportError:
        # Config system not available, use defaults
        return default


# =================================
# Config Integration
# =================================


def x__get_config_value__mutmut_7(key: str, default: str | int) -> str | int:
    """Get crypto config value with fallback to default."""
    try:
        from provide.foundation.config import get_config

        config = get_config(f"crypto.{key}")
        if config is not None and hasattr("value"):
            value = config.value
            # Cast to str | int based on default type
            if isinstance(default, int):
                return int(value) if isinstance(value, (int, str)) else default
            return str(value) if value is not None else default
        return default
    except ImportError:
        # Config system not available, use defaults
        return default


# =================================
# Config Integration
# =================================


def x__get_config_value__mutmut_8(key: str, default: str | int) -> str | int:
    """Get crypto config value with fallback to default."""
    try:
        from provide.foundation.config import get_config

        config = get_config(f"crypto.{key}")
        if config is not None and hasattr(config, ):
            value = config.value
            # Cast to str | int based on default type
            if isinstance(default, int):
                return int(value) if isinstance(value, (int, str)) else default
            return str(value) if value is not None else default
        return default
    except ImportError:
        # Config system not available, use defaults
        return default


# =================================
# Config Integration
# =================================


def x__get_config_value__mutmut_9(key: str, default: str | int) -> str | int:
    """Get crypto config value with fallback to default."""
    try:
        from provide.foundation.config import get_config

        config = get_config(f"crypto.{key}")
        if config is not None and hasattr(config, "XXvalueXX"):
            value = config.value
            # Cast to str | int based on default type
            if isinstance(default, int):
                return int(value) if isinstance(value, (int, str)) else default
            return str(value) if value is not None else default
        return default
    except ImportError:
        # Config system not available, use defaults
        return default


# =================================
# Config Integration
# =================================


def x__get_config_value__mutmut_10(key: str, default: str | int) -> str | int:
    """Get crypto config value with fallback to default."""
    try:
        from provide.foundation.config import get_config

        config = get_config(f"crypto.{key}")
        if config is not None and hasattr(config, "VALUE"):
            value = config.value
            # Cast to str | int based on default type
            if isinstance(default, int):
                return int(value) if isinstance(value, (int, str)) else default
            return str(value) if value is not None else default
        return default
    except ImportError:
        # Config system not available, use defaults
        return default


# =================================
# Config Integration
# =================================


def x__get_config_value__mutmut_11(key: str, default: str | int) -> str | int:
    """Get crypto config value with fallback to default."""
    try:
        from provide.foundation.config import get_config

        config = get_config(f"crypto.{key}")
        if config is not None and hasattr(config, "value"):
            value = None
            # Cast to str | int based on default type
            if isinstance(default, int):
                return int(value) if isinstance(value, (int, str)) else default
            return str(value) if value is not None else default
        return default
    except ImportError:
        # Config system not available, use defaults
        return default


# =================================
# Config Integration
# =================================


def x__get_config_value__mutmut_12(key: str, default: str | int) -> str | int:
    """Get crypto config value with fallback to default."""
    try:
        from provide.foundation.config import get_config

        config = get_config(f"crypto.{key}")
        if config is not None and hasattr(config, "value"):
            value = config.value
            # Cast to str | int based on default type
            if isinstance(default, int):
                return int(None) if isinstance(value, (int, str)) else default
            return str(value) if value is not None else default
        return default
    except ImportError:
        # Config system not available, use defaults
        return default


# =================================
# Config Integration
# =================================


def x__get_config_value__mutmut_13(key: str, default: str | int) -> str | int:
    """Get crypto config value with fallback to default."""
    try:
        from provide.foundation.config import get_config

        config = get_config(f"crypto.{key}")
        if config is not None and hasattr(config, "value"):
            value = config.value
            # Cast to str | int based on default type
            if isinstance(default, int):
                return int(value) if isinstance(value, (int, str)) else default
            return str(None) if value is not None else default
        return default
    except ImportError:
        # Config system not available, use defaults
        return default


# =================================
# Config Integration
# =================================


def x__get_config_value__mutmut_14(key: str, default: str | int) -> str | int:
    """Get crypto config value with fallback to default."""
    try:
        from provide.foundation.config import get_config

        config = get_config(f"crypto.{key}")
        if config is not None and hasattr(config, "value"):
            value = config.value
            # Cast to str | int based on default type
            if isinstance(default, int):
                return int(value) if isinstance(value, (int, str)) else default
            return str(value) if value is None else default
        return default
    except ImportError:
        # Config system not available, use defaults
        return default

x__get_config_value__mutmut_mutants : ClassVar[MutantDict] = {
'x__get_config_value__mutmut_1': x__get_config_value__mutmut_1, 
    'x__get_config_value__mutmut_2': x__get_config_value__mutmut_2, 
    'x__get_config_value__mutmut_3': x__get_config_value__mutmut_3, 
    'x__get_config_value__mutmut_4': x__get_config_value__mutmut_4, 
    'x__get_config_value__mutmut_5': x__get_config_value__mutmut_5, 
    'x__get_config_value__mutmut_6': x__get_config_value__mutmut_6, 
    'x__get_config_value__mutmut_7': x__get_config_value__mutmut_7, 
    'x__get_config_value__mutmut_8': x__get_config_value__mutmut_8, 
    'x__get_config_value__mutmut_9': x__get_config_value__mutmut_9, 
    'x__get_config_value__mutmut_10': x__get_config_value__mutmut_10, 
    'x__get_config_value__mutmut_11': x__get_config_value__mutmut_11, 
    'x__get_config_value__mutmut_12': x__get_config_value__mutmut_12, 
    'x__get_config_value__mutmut_13': x__get_config_value__mutmut_13, 
    'x__get_config_value__mutmut_14': x__get_config_value__mutmut_14
}

def _get_config_value(*args, **kwargs):
    result = _mutmut_trampoline(x__get_config_value__mutmut_orig, x__get_config_value__mutmut_mutants, args, kwargs)
    return result 

_get_config_value.__signature__ = _mutmut_signature(x__get_config_value__mutmut_orig)
x__get_config_value__mutmut_orig.__name__ = 'x__get_config_value'


def x_get_default_hash_algorithm__mutmut_orig() -> str:
    """Get default hash algorithm from config or fallback."""
    from provide.foundation.crypto.algorithms import DEFAULT_ALGORITHM

    return str(_get_config_value("hash_algorithm", DEFAULT_ALGORITHM))


def x_get_default_hash_algorithm__mutmut_1() -> str:
    """Get default hash algorithm from config or fallback."""
    from provide.foundation.crypto.algorithms import DEFAULT_ALGORITHM

    return str(None)


def x_get_default_hash_algorithm__mutmut_2() -> str:
    """Get default hash algorithm from config or fallback."""
    from provide.foundation.crypto.algorithms import DEFAULT_ALGORITHM

    return str(_get_config_value(None, DEFAULT_ALGORITHM))


def x_get_default_hash_algorithm__mutmut_3() -> str:
    """Get default hash algorithm from config or fallback."""
    from provide.foundation.crypto.algorithms import DEFAULT_ALGORITHM

    return str(_get_config_value("hash_algorithm", None))


def x_get_default_hash_algorithm__mutmut_4() -> str:
    """Get default hash algorithm from config or fallback."""
    from provide.foundation.crypto.algorithms import DEFAULT_ALGORITHM

    return str(_get_config_value(DEFAULT_ALGORITHM))


def x_get_default_hash_algorithm__mutmut_5() -> str:
    """Get default hash algorithm from config or fallback."""
    from provide.foundation.crypto.algorithms import DEFAULT_ALGORITHM

    return str(_get_config_value("hash_algorithm", ))


def x_get_default_hash_algorithm__mutmut_6() -> str:
    """Get default hash algorithm from config or fallback."""
    from provide.foundation.crypto.algorithms import DEFAULT_ALGORITHM

    return str(_get_config_value("XXhash_algorithmXX", DEFAULT_ALGORITHM))


def x_get_default_hash_algorithm__mutmut_7() -> str:
    """Get default hash algorithm from config or fallback."""
    from provide.foundation.crypto.algorithms import DEFAULT_ALGORITHM

    return str(_get_config_value("HASH_ALGORITHM", DEFAULT_ALGORITHM))

x_get_default_hash_algorithm__mutmut_mutants : ClassVar[MutantDict] = {
'x_get_default_hash_algorithm__mutmut_1': x_get_default_hash_algorithm__mutmut_1, 
    'x_get_default_hash_algorithm__mutmut_2': x_get_default_hash_algorithm__mutmut_2, 
    'x_get_default_hash_algorithm__mutmut_3': x_get_default_hash_algorithm__mutmut_3, 
    'x_get_default_hash_algorithm__mutmut_4': x_get_default_hash_algorithm__mutmut_4, 
    'x_get_default_hash_algorithm__mutmut_5': x_get_default_hash_algorithm__mutmut_5, 
    'x_get_default_hash_algorithm__mutmut_6': x_get_default_hash_algorithm__mutmut_6, 
    'x_get_default_hash_algorithm__mutmut_7': x_get_default_hash_algorithm__mutmut_7
}

def get_default_hash_algorithm(*args, **kwargs):
    result = _mutmut_trampoline(x_get_default_hash_algorithm__mutmut_orig, x_get_default_hash_algorithm__mutmut_mutants, args, kwargs)
    return result 

get_default_hash_algorithm.__signature__ = _mutmut_signature(x_get_default_hash_algorithm__mutmut_orig)
x_get_default_hash_algorithm__mutmut_orig.__name__ = 'x_get_default_hash_algorithm'


def x_get_default_signature_algorithm__mutmut_orig() -> str:
    """Get default signature algorithm from config or fallback."""
    return str(_get_config_value("signature_algorithm", DEFAULT_SIGNATURE_ALGORITHM))


def x_get_default_signature_algorithm__mutmut_1() -> str:
    """Get default signature algorithm from config or fallback."""
    return str(None)


def x_get_default_signature_algorithm__mutmut_2() -> str:
    """Get default signature algorithm from config or fallback."""
    return str(_get_config_value(None, DEFAULT_SIGNATURE_ALGORITHM))


def x_get_default_signature_algorithm__mutmut_3() -> str:
    """Get default signature algorithm from config or fallback."""
    return str(_get_config_value("signature_algorithm", None))


def x_get_default_signature_algorithm__mutmut_4() -> str:
    """Get default signature algorithm from config or fallback."""
    return str(_get_config_value(DEFAULT_SIGNATURE_ALGORITHM))


def x_get_default_signature_algorithm__mutmut_5() -> str:
    """Get default signature algorithm from config or fallback."""
    return str(_get_config_value("signature_algorithm", ))


def x_get_default_signature_algorithm__mutmut_6() -> str:
    """Get default signature algorithm from config or fallback."""
    return str(_get_config_value("XXsignature_algorithmXX", DEFAULT_SIGNATURE_ALGORITHM))


def x_get_default_signature_algorithm__mutmut_7() -> str:
    """Get default signature algorithm from config or fallback."""
    return str(_get_config_value("SIGNATURE_ALGORITHM", DEFAULT_SIGNATURE_ALGORITHM))

x_get_default_signature_algorithm__mutmut_mutants : ClassVar[MutantDict] = {
'x_get_default_signature_algorithm__mutmut_1': x_get_default_signature_algorithm__mutmut_1, 
    'x_get_default_signature_algorithm__mutmut_2': x_get_default_signature_algorithm__mutmut_2, 
    'x_get_default_signature_algorithm__mutmut_3': x_get_default_signature_algorithm__mutmut_3, 
    'x_get_default_signature_algorithm__mutmut_4': x_get_default_signature_algorithm__mutmut_4, 
    'x_get_default_signature_algorithm__mutmut_5': x_get_default_signature_algorithm__mutmut_5, 
    'x_get_default_signature_algorithm__mutmut_6': x_get_default_signature_algorithm__mutmut_6, 
    'x_get_default_signature_algorithm__mutmut_7': x_get_default_signature_algorithm__mutmut_7
}

def get_default_signature_algorithm(*args, **kwargs):
    result = _mutmut_trampoline(x_get_default_signature_algorithm__mutmut_orig, x_get_default_signature_algorithm__mutmut_mutants, args, kwargs)
    return result 

get_default_signature_algorithm.__signature__ = _mutmut_signature(x_get_default_signature_algorithm__mutmut_orig)
x_get_default_signature_algorithm__mutmut_orig.__name__ = 'x_get_default_signature_algorithm'


__all__ = [
    "DEFAULT_CERTIFICATE_COMMON_NAME",
    "DEFAULT_CERTIFICATE_CURVE",
    "DEFAULT_CERTIFICATE_GENERATE_KEYPAIR",
    "DEFAULT_CERTIFICATE_KEY_TYPE",
    "DEFAULT_CERTIFICATE_ORGANIZATION_NAME",
    # Certificates
    "DEFAULT_CERTIFICATE_VALIDITY_DAYS",
    # ECDSA
    "DEFAULT_ECDSA_CURVE",
    # RSA
    "DEFAULT_RSA_KEY_SIZE",
    # Algorithms
    "DEFAULT_SIGNATURE_ALGORITHM",
    # Ed25519 constants
    "ED25519_PRIVATE_KEY_SIZE",
    "ED25519_PUBLIC_KEY_SIZE",
    "ED25519_SIGNATURE_SIZE",
    "MAX_CERTIFICATE_VALIDITY_DAYS",
    "MIN_CERTIFICATE_VALIDITY_DAYS",
    "SUPPORTED_EC_CURVES",
    # Key types
    "SUPPORTED_KEY_TYPES",
    "SUPPORTED_RSA_SIZES",
    # Factory functions
    "default_certificate_alt_names",
    "default_supported_ec_curves",
    "default_supported_key_types",
    "default_supported_rsa_sizes",
    # Config integration
    "get_default_hash_algorithm",
    "get_default_signature_algorithm",
]


# <3 🧱🤝🔒🪄
