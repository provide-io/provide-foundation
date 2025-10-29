# provide/foundation/crypto/certificates/generator.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from datetime import UTC, datetime, timedelta
import traceback
from typing import TYPE_CHECKING

from provide.foundation import logger
from provide.foundation.crypto.certificates.base import (
    CertificateBase,
    CertificateConfig,
    CertificateError,
    CurveType,
    KeyPair,
    KeyType,
)
from provide.foundation.crypto.certificates.operations import create_x509_certificate
from provide.foundation.crypto.defaults import (
    DEFAULT_CERTIFICATE_CURVE,
    DEFAULT_CERTIFICATE_KEY_TYPE,
    DEFAULT_RSA_KEY_SIZE,
)

"""Certificate generation utilities."""
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


def x__parse_key_type_and_params__mutmut_orig(
    key_type: str, key_size: int, ecdsa_curve: str
) -> tuple[KeyType, int | None, CurveType | None]:
    """Parse and validate key type parameters.

    Args:
        key_type: Key type string ('rsa' or 'ecdsa')
        key_size: RSA key size
        ecdsa_curve: ECDSA curve name

    Returns:
        Tuple of (KeyType, key_size_or_none, curve_or_none)

    Raises:
        ValueError: For invalid key types or curves
    """
    normalized_key_type_str = key_type.lower()
    match normalized_key_type_str:
        case "rsa":
            return KeyType.RSA, key_size, None
        case "ecdsa":
            try:
                curve = CurveType[ecdsa_curve.upper()]
                return KeyType.ECDSA, None, curve
            except KeyError as e_curve:
                raise ValueError(f"Unsupported ECDSA curve: {ecdsa_curve}") from e_curve
        case _:
            raise ValueError(f"Unsupported key_type string: '{key_type}'. Must be 'rsa' or 'ecdsa'.")


def x__parse_key_type_and_params__mutmut_1(
    key_type: str, key_size: int, ecdsa_curve: str
) -> tuple[KeyType, int | None, CurveType | None]:
    """Parse and validate key type parameters.

    Args:
        key_type: Key type string ('rsa' or 'ecdsa')
        key_size: RSA key size
        ecdsa_curve: ECDSA curve name

    Returns:
        Tuple of (KeyType, key_size_or_none, curve_or_none)

    Raises:
        ValueError: For invalid key types or curves
    """
    normalized_key_type_str = None
    match normalized_key_type_str:
        case "rsa":
            return KeyType.RSA, key_size, None
        case "ecdsa":
            try:
                curve = CurveType[ecdsa_curve.upper()]
                return KeyType.ECDSA, None, curve
            except KeyError as e_curve:
                raise ValueError(f"Unsupported ECDSA curve: {ecdsa_curve}") from e_curve
        case _:
            raise ValueError(f"Unsupported key_type string: '{key_type}'. Must be 'rsa' or 'ecdsa'.")


def x__parse_key_type_and_params__mutmut_2(
    key_type: str, key_size: int, ecdsa_curve: str
) -> tuple[KeyType, int | None, CurveType | None]:
    """Parse and validate key type parameters.

    Args:
        key_type: Key type string ('rsa' or 'ecdsa')
        key_size: RSA key size
        ecdsa_curve: ECDSA curve name

    Returns:
        Tuple of (KeyType, key_size_or_none, curve_or_none)

    Raises:
        ValueError: For invalid key types or curves
    """
    normalized_key_type_str = key_type.upper()
    match normalized_key_type_str:
        case "rsa":
            return KeyType.RSA, key_size, None
        case "ecdsa":
            try:
                curve = CurveType[ecdsa_curve.upper()]
                return KeyType.ECDSA, None, curve
            except KeyError as e_curve:
                raise ValueError(f"Unsupported ECDSA curve: {ecdsa_curve}") from e_curve
        case _:
            raise ValueError(f"Unsupported key_type string: '{key_type}'. Must be 'rsa' or 'ecdsa'.")


def x__parse_key_type_and_params__mutmut_3(
    key_type: str, key_size: int, ecdsa_curve: str
) -> tuple[KeyType, int | None, CurveType | None]:
    """Parse and validate key type parameters.

    Args:
        key_type: Key type string ('rsa' or 'ecdsa')
        key_size: RSA key size
        ecdsa_curve: ECDSA curve name

    Returns:
        Tuple of (KeyType, key_size_or_none, curve_or_none)

    Raises:
        ValueError: For invalid key types or curves
    """
    normalized_key_type_str = key_type.lower()
    match normalized_key_type_str:
        case "ecdsa":
            try:
                curve = CurveType[ecdsa_curve.upper()]
                return KeyType.ECDSA, None, curve
            except KeyError as e_curve:
                raise ValueError(f"Unsupported ECDSA curve: {ecdsa_curve}") from e_curve
        case _:
            raise ValueError(f"Unsupported key_type string: '{key_type}'. Must be 'rsa' or 'ecdsa'.")


def x__parse_key_type_and_params__mutmut_4(
    key_type: str, key_size: int, ecdsa_curve: str
) -> tuple[KeyType, int | None, CurveType | None]:
    """Parse and validate key type parameters.

    Args:
        key_type: Key type string ('rsa' or 'ecdsa')
        key_size: RSA key size
        ecdsa_curve: ECDSA curve name

    Returns:
        Tuple of (KeyType, key_size_or_none, curve_or_none)

    Raises:
        ValueError: For invalid key types or curves
    """
    normalized_key_type_str = key_type.lower()
    match normalized_key_type_str:
        case "rsa":
            return KeyType.RSA, key_size, None
        case _:
            raise ValueError(f"Unsupported key_type string: '{key_type}'. Must be 'rsa' or 'ecdsa'.")


def x__parse_key_type_and_params__mutmut_5(
    key_type: str, key_size: int, ecdsa_curve: str
) -> tuple[KeyType, int | None, CurveType | None]:
    """Parse and validate key type parameters.

    Args:
        key_type: Key type string ('rsa' or 'ecdsa')
        key_size: RSA key size
        ecdsa_curve: ECDSA curve name

    Returns:
        Tuple of (KeyType, key_size_or_none, curve_or_none)

    Raises:
        ValueError: For invalid key types or curves
    """
    normalized_key_type_str = key_type.lower()
    match normalized_key_type_str:
        case "rsa":
            return KeyType.RSA, key_size, None
        case "ecdsa":
            try:
                curve = CurveType[ecdsa_curve.upper()]
                return KeyType.ECDSA, None, curve
            except KeyError as e_curve:
                raise ValueError(f"Unsupported ECDSA curve: {ecdsa_curve}") from e_curve


def x__parse_key_type_and_params__mutmut_6(
    key_type: str, key_size: int, ecdsa_curve: str
) -> tuple[KeyType, int | None, CurveType | None]:
    """Parse and validate key type parameters.

    Args:
        key_type: Key type string ('rsa' or 'ecdsa')
        key_size: RSA key size
        ecdsa_curve: ECDSA curve name

    Returns:
        Tuple of (KeyType, key_size_or_none, curve_or_none)

    Raises:
        ValueError: For invalid key types or curves
    """
    normalized_key_type_str = key_type.lower()
    match normalized_key_type_str:
        case "XXrsaXX":
            return KeyType.RSA, key_size, None
        case "ecdsa":
            try:
                curve = CurveType[ecdsa_curve.upper()]
                return KeyType.ECDSA, None, curve
            except KeyError as e_curve:
                raise ValueError(f"Unsupported ECDSA curve: {ecdsa_curve}") from e_curve
        case _:
            raise ValueError(f"Unsupported key_type string: '{key_type}'. Must be 'rsa' or 'ecdsa'.")


def x__parse_key_type_and_params__mutmut_7(
    key_type: str, key_size: int, ecdsa_curve: str
) -> tuple[KeyType, int | None, CurveType | None]:
    """Parse and validate key type parameters.

    Args:
        key_type: Key type string ('rsa' or 'ecdsa')
        key_size: RSA key size
        ecdsa_curve: ECDSA curve name

    Returns:
        Tuple of (KeyType, key_size_or_none, curve_or_none)

    Raises:
        ValueError: For invalid key types or curves
    """
    normalized_key_type_str = key_type.lower()
    match normalized_key_type_str:
        case "RSA":
            return KeyType.RSA, key_size, None
        case "ecdsa":
            try:
                curve = CurveType[ecdsa_curve.upper()]
                return KeyType.ECDSA, None, curve
            except KeyError as e_curve:
                raise ValueError(f"Unsupported ECDSA curve: {ecdsa_curve}") from e_curve
        case _:
            raise ValueError(f"Unsupported key_type string: '{key_type}'. Must be 'rsa' or 'ecdsa'.")


def x__parse_key_type_and_params__mutmut_8(
    key_type: str, key_size: int, ecdsa_curve: str
) -> tuple[KeyType, int | None, CurveType | None]:
    """Parse and validate key type parameters.

    Args:
        key_type: Key type string ('rsa' or 'ecdsa')
        key_size: RSA key size
        ecdsa_curve: ECDSA curve name

    Returns:
        Tuple of (KeyType, key_size_or_none, curve_or_none)

    Raises:
        ValueError: For invalid key types or curves
    """
    normalized_key_type_str = key_type.lower()
    match normalized_key_type_str:
        case "rsa":
            return KeyType.RSA, key_size, None
        case "XXecdsaXX":
            try:
                curve = CurveType[ecdsa_curve.upper()]
                return KeyType.ECDSA, None, curve
            except KeyError as e_curve:
                raise ValueError(f"Unsupported ECDSA curve: {ecdsa_curve}") from e_curve
        case _:
            raise ValueError(f"Unsupported key_type string: '{key_type}'. Must be 'rsa' or 'ecdsa'.")


def x__parse_key_type_and_params__mutmut_9(
    key_type: str, key_size: int, ecdsa_curve: str
) -> tuple[KeyType, int | None, CurveType | None]:
    """Parse and validate key type parameters.

    Args:
        key_type: Key type string ('rsa' or 'ecdsa')
        key_size: RSA key size
        ecdsa_curve: ECDSA curve name

    Returns:
        Tuple of (KeyType, key_size_or_none, curve_or_none)

    Raises:
        ValueError: For invalid key types or curves
    """
    normalized_key_type_str = key_type.lower()
    match normalized_key_type_str:
        case "rsa":
            return KeyType.RSA, key_size, None
        case "ECDSA":
            try:
                curve = CurveType[ecdsa_curve.upper()]
                return KeyType.ECDSA, None, curve
            except KeyError as e_curve:
                raise ValueError(f"Unsupported ECDSA curve: {ecdsa_curve}") from e_curve
        case _:
            raise ValueError(f"Unsupported key_type string: '{key_type}'. Must be 'rsa' or 'ecdsa'.")


def x__parse_key_type_and_params__mutmut_10(
    key_type: str, key_size: int, ecdsa_curve: str
) -> tuple[KeyType, int | None, CurveType | None]:
    """Parse and validate key type parameters.

    Args:
        key_type: Key type string ('rsa' or 'ecdsa')
        key_size: RSA key size
        ecdsa_curve: ECDSA curve name

    Returns:
        Tuple of (KeyType, key_size_or_none, curve_or_none)

    Raises:
        ValueError: For invalid key types or curves
    """
    normalized_key_type_str = key_type.lower()
    match normalized_key_type_str:
        case "rsa":
            return KeyType.RSA, key_size, None
        case "ecdsa":
            try:
                curve = None
                return KeyType.ECDSA, None, curve
            except KeyError as e_curve:
                raise ValueError(f"Unsupported ECDSA curve: {ecdsa_curve}") from e_curve
        case _:
            raise ValueError(f"Unsupported key_type string: '{key_type}'. Must be 'rsa' or 'ecdsa'.")


def x__parse_key_type_and_params__mutmut_11(
    key_type: str, key_size: int, ecdsa_curve: str
) -> tuple[KeyType, int | None, CurveType | None]:
    """Parse and validate key type parameters.

    Args:
        key_type: Key type string ('rsa' or 'ecdsa')
        key_size: RSA key size
        ecdsa_curve: ECDSA curve name

    Returns:
        Tuple of (KeyType, key_size_or_none, curve_or_none)

    Raises:
        ValueError: For invalid key types or curves
    """
    normalized_key_type_str = key_type.lower()
    match normalized_key_type_str:
        case "rsa":
            return KeyType.RSA, key_size, None
        case "ecdsa":
            try:
                curve = CurveType[ecdsa_curve.lower()]
                return KeyType.ECDSA, None, curve
            except KeyError as e_curve:
                raise ValueError(f"Unsupported ECDSA curve: {ecdsa_curve}") from e_curve
        case _:
            raise ValueError(f"Unsupported key_type string: '{key_type}'. Must be 'rsa' or 'ecdsa'.")


def x__parse_key_type_and_params__mutmut_12(
    key_type: str, key_size: int, ecdsa_curve: str
) -> tuple[KeyType, int | None, CurveType | None]:
    """Parse and validate key type parameters.

    Args:
        key_type: Key type string ('rsa' or 'ecdsa')
        key_size: RSA key size
        ecdsa_curve: ECDSA curve name

    Returns:
        Tuple of (KeyType, key_size_or_none, curve_or_none)

    Raises:
        ValueError: For invalid key types or curves
    """
    normalized_key_type_str = key_type.lower()
    match normalized_key_type_str:
        case "rsa":
            return KeyType.RSA, key_size, None
        case "ecdsa":
            try:
                curve = CurveType[ecdsa_curve.upper()]
                return KeyType.ECDSA, None, curve
            except KeyError as e_curve:
                raise ValueError(None) from e_curve
        case _:
            raise ValueError(f"Unsupported key_type string: '{key_type}'. Must be 'rsa' or 'ecdsa'.")


def x__parse_key_type_and_params__mutmut_13(
    key_type: str, key_size: int, ecdsa_curve: str
) -> tuple[KeyType, int | None, CurveType | None]:
    """Parse and validate key type parameters.

    Args:
        key_type: Key type string ('rsa' or 'ecdsa')
        key_size: RSA key size
        ecdsa_curve: ECDSA curve name

    Returns:
        Tuple of (KeyType, key_size_or_none, curve_or_none)

    Raises:
        ValueError: For invalid key types or curves
    """
    normalized_key_type_str = key_type.lower()
    match normalized_key_type_str:
        case "rsa":
            return KeyType.RSA, key_size, None
        case "ecdsa":
            try:
                curve = CurveType[ecdsa_curve.upper()]
                return KeyType.ECDSA, None, curve
            except KeyError as e_curve:
                raise ValueError(f"Unsupported ECDSA curve: {ecdsa_curve}") from e_curve
        case _:
            raise ValueError(None)


x__parse_key_type_and_params__mutmut_mutants: ClassVar[MutantDict] = {
    "x__parse_key_type_and_params__mutmut_1": x__parse_key_type_and_params__mutmut_1,
    "x__parse_key_type_and_params__mutmut_2": x__parse_key_type_and_params__mutmut_2,
    "x__parse_key_type_and_params__mutmut_3": x__parse_key_type_and_params__mutmut_3,
    "x__parse_key_type_and_params__mutmut_4": x__parse_key_type_and_params__mutmut_4,
    "x__parse_key_type_and_params__mutmut_5": x__parse_key_type_and_params__mutmut_5,
    "x__parse_key_type_and_params__mutmut_6": x__parse_key_type_and_params__mutmut_6,
    "x__parse_key_type_and_params__mutmut_7": x__parse_key_type_and_params__mutmut_7,
    "x__parse_key_type_and_params__mutmut_8": x__parse_key_type_and_params__mutmut_8,
    "x__parse_key_type_and_params__mutmut_9": x__parse_key_type_and_params__mutmut_9,
    "x__parse_key_type_and_params__mutmut_10": x__parse_key_type_and_params__mutmut_10,
    "x__parse_key_type_and_params__mutmut_11": x__parse_key_type_and_params__mutmut_11,
    "x__parse_key_type_and_params__mutmut_12": x__parse_key_type_and_params__mutmut_12,
    "x__parse_key_type_and_params__mutmut_13": x__parse_key_type_and_params__mutmut_13,
}


def _parse_key_type_and_params(*args, **kwargs):
    result = _mutmut_trampoline(
        x__parse_key_type_and_params__mutmut_orig, x__parse_key_type_and_params__mutmut_mutants, args, kwargs
    )
    return result


_parse_key_type_and_params.__signature__ = _mutmut_signature(x__parse_key_type_and_params__mutmut_orig)
x__parse_key_type_and_params__mutmut_orig.__name__ = "x__parse_key_type_and_params"


def x__build_certificate_config__mutmut_orig(
    common_name: str,
    organization_name: str,
    not_valid_before: datetime,
    not_valid_after: datetime,
    alt_names: list[str] | None,
    gen_key_type: KeyType,
    gen_key_size: int | None,
    gen_curve: CurveType | None,
) -> CertificateConfig:
    """Build certificate configuration dictionary.

    Args:
        common_name: Certificate common name
        organization_name: Organization name
        not_valid_before: Certificate start validity
        not_valid_after: Certificate end validity
        alt_names: Subject alternative names
        gen_key_type: Key type enum
        gen_key_size: RSA key size (for RSA keys)
        gen_curve: ECDSA curve (for ECDSA keys)

    Returns:
        Certificate configuration dictionary
    """
    conf: CertificateConfig = {
        "common_name": common_name,
        "organization": organization_name,
        "alt_names": alt_names or ["localhost"],
        "key_type": gen_key_type,
        "not_valid_before": not_valid_before,
        "not_valid_after": not_valid_after,
    }
    if gen_curve is not None:
        conf["curve"] = gen_curve
    if gen_key_size is not None:
        conf["key_size"] = gen_key_size
    return conf


def x__build_certificate_config__mutmut_1(
    common_name: str,
    organization_name: str,
    not_valid_before: datetime,
    not_valid_after: datetime,
    alt_names: list[str] | None,
    gen_key_type: KeyType,
    gen_key_size: int | None,
    gen_curve: CurveType | None,
) -> CertificateConfig:
    """Build certificate configuration dictionary.

    Args:
        common_name: Certificate common name
        organization_name: Organization name
        not_valid_before: Certificate start validity
        not_valid_after: Certificate end validity
        alt_names: Subject alternative names
        gen_key_type: Key type enum
        gen_key_size: RSA key size (for RSA keys)
        gen_curve: ECDSA curve (for ECDSA keys)

    Returns:
        Certificate configuration dictionary
    """
    conf: CertificateConfig = None
    if gen_curve is not None:
        conf["curve"] = gen_curve
    if gen_key_size is not None:
        conf["key_size"] = gen_key_size
    return conf


def x__build_certificate_config__mutmut_2(
    common_name: str,
    organization_name: str,
    not_valid_before: datetime,
    not_valid_after: datetime,
    alt_names: list[str] | None,
    gen_key_type: KeyType,
    gen_key_size: int | None,
    gen_curve: CurveType | None,
) -> CertificateConfig:
    """Build certificate configuration dictionary.

    Args:
        common_name: Certificate common name
        organization_name: Organization name
        not_valid_before: Certificate start validity
        not_valid_after: Certificate end validity
        alt_names: Subject alternative names
        gen_key_type: Key type enum
        gen_key_size: RSA key size (for RSA keys)
        gen_curve: ECDSA curve (for ECDSA keys)

    Returns:
        Certificate configuration dictionary
    """
    conf: CertificateConfig = {
        "XXcommon_nameXX": common_name,
        "organization": organization_name,
        "alt_names": alt_names or ["localhost"],
        "key_type": gen_key_type,
        "not_valid_before": not_valid_before,
        "not_valid_after": not_valid_after,
    }
    if gen_curve is not None:
        conf["curve"] = gen_curve
    if gen_key_size is not None:
        conf["key_size"] = gen_key_size
    return conf


def x__build_certificate_config__mutmut_3(
    common_name: str,
    organization_name: str,
    not_valid_before: datetime,
    not_valid_after: datetime,
    alt_names: list[str] | None,
    gen_key_type: KeyType,
    gen_key_size: int | None,
    gen_curve: CurveType | None,
) -> CertificateConfig:
    """Build certificate configuration dictionary.

    Args:
        common_name: Certificate common name
        organization_name: Organization name
        not_valid_before: Certificate start validity
        not_valid_after: Certificate end validity
        alt_names: Subject alternative names
        gen_key_type: Key type enum
        gen_key_size: RSA key size (for RSA keys)
        gen_curve: ECDSA curve (for ECDSA keys)

    Returns:
        Certificate configuration dictionary
    """
    conf: CertificateConfig = {
        "COMMON_NAME": common_name,
        "organization": organization_name,
        "alt_names": alt_names or ["localhost"],
        "key_type": gen_key_type,
        "not_valid_before": not_valid_before,
        "not_valid_after": not_valid_after,
    }
    if gen_curve is not None:
        conf["curve"] = gen_curve
    if gen_key_size is not None:
        conf["key_size"] = gen_key_size
    return conf


def x__build_certificate_config__mutmut_4(
    common_name: str,
    organization_name: str,
    not_valid_before: datetime,
    not_valid_after: datetime,
    alt_names: list[str] | None,
    gen_key_type: KeyType,
    gen_key_size: int | None,
    gen_curve: CurveType | None,
) -> CertificateConfig:
    """Build certificate configuration dictionary.

    Args:
        common_name: Certificate common name
        organization_name: Organization name
        not_valid_before: Certificate start validity
        not_valid_after: Certificate end validity
        alt_names: Subject alternative names
        gen_key_type: Key type enum
        gen_key_size: RSA key size (for RSA keys)
        gen_curve: ECDSA curve (for ECDSA keys)

    Returns:
        Certificate configuration dictionary
    """
    conf: CertificateConfig = {
        "common_name": common_name,
        "XXorganizationXX": organization_name,
        "alt_names": alt_names or ["localhost"],
        "key_type": gen_key_type,
        "not_valid_before": not_valid_before,
        "not_valid_after": not_valid_after,
    }
    if gen_curve is not None:
        conf["curve"] = gen_curve
    if gen_key_size is not None:
        conf["key_size"] = gen_key_size
    return conf


def x__build_certificate_config__mutmut_5(
    common_name: str,
    organization_name: str,
    not_valid_before: datetime,
    not_valid_after: datetime,
    alt_names: list[str] | None,
    gen_key_type: KeyType,
    gen_key_size: int | None,
    gen_curve: CurveType | None,
) -> CertificateConfig:
    """Build certificate configuration dictionary.

    Args:
        common_name: Certificate common name
        organization_name: Organization name
        not_valid_before: Certificate start validity
        not_valid_after: Certificate end validity
        alt_names: Subject alternative names
        gen_key_type: Key type enum
        gen_key_size: RSA key size (for RSA keys)
        gen_curve: ECDSA curve (for ECDSA keys)

    Returns:
        Certificate configuration dictionary
    """
    conf: CertificateConfig = {
        "common_name": common_name,
        "ORGANIZATION": organization_name,
        "alt_names": alt_names or ["localhost"],
        "key_type": gen_key_type,
        "not_valid_before": not_valid_before,
        "not_valid_after": not_valid_after,
    }
    if gen_curve is not None:
        conf["curve"] = gen_curve
    if gen_key_size is not None:
        conf["key_size"] = gen_key_size
    return conf


def x__build_certificate_config__mutmut_6(
    common_name: str,
    organization_name: str,
    not_valid_before: datetime,
    not_valid_after: datetime,
    alt_names: list[str] | None,
    gen_key_type: KeyType,
    gen_key_size: int | None,
    gen_curve: CurveType | None,
) -> CertificateConfig:
    """Build certificate configuration dictionary.

    Args:
        common_name: Certificate common name
        organization_name: Organization name
        not_valid_before: Certificate start validity
        not_valid_after: Certificate end validity
        alt_names: Subject alternative names
        gen_key_type: Key type enum
        gen_key_size: RSA key size (for RSA keys)
        gen_curve: ECDSA curve (for ECDSA keys)

    Returns:
        Certificate configuration dictionary
    """
    conf: CertificateConfig = {
        "common_name": common_name,
        "organization": organization_name,
        "XXalt_namesXX": alt_names or ["localhost"],
        "key_type": gen_key_type,
        "not_valid_before": not_valid_before,
        "not_valid_after": not_valid_after,
    }
    if gen_curve is not None:
        conf["curve"] = gen_curve
    if gen_key_size is not None:
        conf["key_size"] = gen_key_size
    return conf


def x__build_certificate_config__mutmut_7(
    common_name: str,
    organization_name: str,
    not_valid_before: datetime,
    not_valid_after: datetime,
    alt_names: list[str] | None,
    gen_key_type: KeyType,
    gen_key_size: int | None,
    gen_curve: CurveType | None,
) -> CertificateConfig:
    """Build certificate configuration dictionary.

    Args:
        common_name: Certificate common name
        organization_name: Organization name
        not_valid_before: Certificate start validity
        not_valid_after: Certificate end validity
        alt_names: Subject alternative names
        gen_key_type: Key type enum
        gen_key_size: RSA key size (for RSA keys)
        gen_curve: ECDSA curve (for ECDSA keys)

    Returns:
        Certificate configuration dictionary
    """
    conf: CertificateConfig = {
        "common_name": common_name,
        "organization": organization_name,
        "ALT_NAMES": alt_names or ["localhost"],
        "key_type": gen_key_type,
        "not_valid_before": not_valid_before,
        "not_valid_after": not_valid_after,
    }
    if gen_curve is not None:
        conf["curve"] = gen_curve
    if gen_key_size is not None:
        conf["key_size"] = gen_key_size
    return conf


def x__build_certificate_config__mutmut_8(
    common_name: str,
    organization_name: str,
    not_valid_before: datetime,
    not_valid_after: datetime,
    alt_names: list[str] | None,
    gen_key_type: KeyType,
    gen_key_size: int | None,
    gen_curve: CurveType | None,
) -> CertificateConfig:
    """Build certificate configuration dictionary.

    Args:
        common_name: Certificate common name
        organization_name: Organization name
        not_valid_before: Certificate start validity
        not_valid_after: Certificate end validity
        alt_names: Subject alternative names
        gen_key_type: Key type enum
        gen_key_size: RSA key size (for RSA keys)
        gen_curve: ECDSA curve (for ECDSA keys)

    Returns:
        Certificate configuration dictionary
    """
    conf: CertificateConfig = {
        "common_name": common_name,
        "organization": organization_name,
        "alt_names": alt_names and ["localhost"],
        "key_type": gen_key_type,
        "not_valid_before": not_valid_before,
        "not_valid_after": not_valid_after,
    }
    if gen_curve is not None:
        conf["curve"] = gen_curve
    if gen_key_size is not None:
        conf["key_size"] = gen_key_size
    return conf


def x__build_certificate_config__mutmut_9(
    common_name: str,
    organization_name: str,
    not_valid_before: datetime,
    not_valid_after: datetime,
    alt_names: list[str] | None,
    gen_key_type: KeyType,
    gen_key_size: int | None,
    gen_curve: CurveType | None,
) -> CertificateConfig:
    """Build certificate configuration dictionary.

    Args:
        common_name: Certificate common name
        organization_name: Organization name
        not_valid_before: Certificate start validity
        not_valid_after: Certificate end validity
        alt_names: Subject alternative names
        gen_key_type: Key type enum
        gen_key_size: RSA key size (for RSA keys)
        gen_curve: ECDSA curve (for ECDSA keys)

    Returns:
        Certificate configuration dictionary
    """
    conf: CertificateConfig = {
        "common_name": common_name,
        "organization": organization_name,
        "alt_names": alt_names or ["XXlocalhostXX"],
        "key_type": gen_key_type,
        "not_valid_before": not_valid_before,
        "not_valid_after": not_valid_after,
    }
    if gen_curve is not None:
        conf["curve"] = gen_curve
    if gen_key_size is not None:
        conf["key_size"] = gen_key_size
    return conf


def x__build_certificate_config__mutmut_10(
    common_name: str,
    organization_name: str,
    not_valid_before: datetime,
    not_valid_after: datetime,
    alt_names: list[str] | None,
    gen_key_type: KeyType,
    gen_key_size: int | None,
    gen_curve: CurveType | None,
) -> CertificateConfig:
    """Build certificate configuration dictionary.

    Args:
        common_name: Certificate common name
        organization_name: Organization name
        not_valid_before: Certificate start validity
        not_valid_after: Certificate end validity
        alt_names: Subject alternative names
        gen_key_type: Key type enum
        gen_key_size: RSA key size (for RSA keys)
        gen_curve: ECDSA curve (for ECDSA keys)

    Returns:
        Certificate configuration dictionary
    """
    conf: CertificateConfig = {
        "common_name": common_name,
        "organization": organization_name,
        "alt_names": alt_names or ["LOCALHOST"],
        "key_type": gen_key_type,
        "not_valid_before": not_valid_before,
        "not_valid_after": not_valid_after,
    }
    if gen_curve is not None:
        conf["curve"] = gen_curve
    if gen_key_size is not None:
        conf["key_size"] = gen_key_size
    return conf


def x__build_certificate_config__mutmut_11(
    common_name: str,
    organization_name: str,
    not_valid_before: datetime,
    not_valid_after: datetime,
    alt_names: list[str] | None,
    gen_key_type: KeyType,
    gen_key_size: int | None,
    gen_curve: CurveType | None,
) -> CertificateConfig:
    """Build certificate configuration dictionary.

    Args:
        common_name: Certificate common name
        organization_name: Organization name
        not_valid_before: Certificate start validity
        not_valid_after: Certificate end validity
        alt_names: Subject alternative names
        gen_key_type: Key type enum
        gen_key_size: RSA key size (for RSA keys)
        gen_curve: ECDSA curve (for ECDSA keys)

    Returns:
        Certificate configuration dictionary
    """
    conf: CertificateConfig = {
        "common_name": common_name,
        "organization": organization_name,
        "alt_names": alt_names or ["localhost"],
        "XXkey_typeXX": gen_key_type,
        "not_valid_before": not_valid_before,
        "not_valid_after": not_valid_after,
    }
    if gen_curve is not None:
        conf["curve"] = gen_curve
    if gen_key_size is not None:
        conf["key_size"] = gen_key_size
    return conf


def x__build_certificate_config__mutmut_12(
    common_name: str,
    organization_name: str,
    not_valid_before: datetime,
    not_valid_after: datetime,
    alt_names: list[str] | None,
    gen_key_type: KeyType,
    gen_key_size: int | None,
    gen_curve: CurveType | None,
) -> CertificateConfig:
    """Build certificate configuration dictionary.

    Args:
        common_name: Certificate common name
        organization_name: Organization name
        not_valid_before: Certificate start validity
        not_valid_after: Certificate end validity
        alt_names: Subject alternative names
        gen_key_type: Key type enum
        gen_key_size: RSA key size (for RSA keys)
        gen_curve: ECDSA curve (for ECDSA keys)

    Returns:
        Certificate configuration dictionary
    """
    conf: CertificateConfig = {
        "common_name": common_name,
        "organization": organization_name,
        "alt_names": alt_names or ["localhost"],
        "KEY_TYPE": gen_key_type,
        "not_valid_before": not_valid_before,
        "not_valid_after": not_valid_after,
    }
    if gen_curve is not None:
        conf["curve"] = gen_curve
    if gen_key_size is not None:
        conf["key_size"] = gen_key_size
    return conf


def x__build_certificate_config__mutmut_13(
    common_name: str,
    organization_name: str,
    not_valid_before: datetime,
    not_valid_after: datetime,
    alt_names: list[str] | None,
    gen_key_type: KeyType,
    gen_key_size: int | None,
    gen_curve: CurveType | None,
) -> CertificateConfig:
    """Build certificate configuration dictionary.

    Args:
        common_name: Certificate common name
        organization_name: Organization name
        not_valid_before: Certificate start validity
        not_valid_after: Certificate end validity
        alt_names: Subject alternative names
        gen_key_type: Key type enum
        gen_key_size: RSA key size (for RSA keys)
        gen_curve: ECDSA curve (for ECDSA keys)

    Returns:
        Certificate configuration dictionary
    """
    conf: CertificateConfig = {
        "common_name": common_name,
        "organization": organization_name,
        "alt_names": alt_names or ["localhost"],
        "key_type": gen_key_type,
        "XXnot_valid_beforeXX": not_valid_before,
        "not_valid_after": not_valid_after,
    }
    if gen_curve is not None:
        conf["curve"] = gen_curve
    if gen_key_size is not None:
        conf["key_size"] = gen_key_size
    return conf


def x__build_certificate_config__mutmut_14(
    common_name: str,
    organization_name: str,
    not_valid_before: datetime,
    not_valid_after: datetime,
    alt_names: list[str] | None,
    gen_key_type: KeyType,
    gen_key_size: int | None,
    gen_curve: CurveType | None,
) -> CertificateConfig:
    """Build certificate configuration dictionary.

    Args:
        common_name: Certificate common name
        organization_name: Organization name
        not_valid_before: Certificate start validity
        not_valid_after: Certificate end validity
        alt_names: Subject alternative names
        gen_key_type: Key type enum
        gen_key_size: RSA key size (for RSA keys)
        gen_curve: ECDSA curve (for ECDSA keys)

    Returns:
        Certificate configuration dictionary
    """
    conf: CertificateConfig = {
        "common_name": common_name,
        "organization": organization_name,
        "alt_names": alt_names or ["localhost"],
        "key_type": gen_key_type,
        "NOT_VALID_BEFORE": not_valid_before,
        "not_valid_after": not_valid_after,
    }
    if gen_curve is not None:
        conf["curve"] = gen_curve
    if gen_key_size is not None:
        conf["key_size"] = gen_key_size
    return conf


def x__build_certificate_config__mutmut_15(
    common_name: str,
    organization_name: str,
    not_valid_before: datetime,
    not_valid_after: datetime,
    alt_names: list[str] | None,
    gen_key_type: KeyType,
    gen_key_size: int | None,
    gen_curve: CurveType | None,
) -> CertificateConfig:
    """Build certificate configuration dictionary.

    Args:
        common_name: Certificate common name
        organization_name: Organization name
        not_valid_before: Certificate start validity
        not_valid_after: Certificate end validity
        alt_names: Subject alternative names
        gen_key_type: Key type enum
        gen_key_size: RSA key size (for RSA keys)
        gen_curve: ECDSA curve (for ECDSA keys)

    Returns:
        Certificate configuration dictionary
    """
    conf: CertificateConfig = {
        "common_name": common_name,
        "organization": organization_name,
        "alt_names": alt_names or ["localhost"],
        "key_type": gen_key_type,
        "not_valid_before": not_valid_before,
        "XXnot_valid_afterXX": not_valid_after,
    }
    if gen_curve is not None:
        conf["curve"] = gen_curve
    if gen_key_size is not None:
        conf["key_size"] = gen_key_size
    return conf


def x__build_certificate_config__mutmut_16(
    common_name: str,
    organization_name: str,
    not_valid_before: datetime,
    not_valid_after: datetime,
    alt_names: list[str] | None,
    gen_key_type: KeyType,
    gen_key_size: int | None,
    gen_curve: CurveType | None,
) -> CertificateConfig:
    """Build certificate configuration dictionary.

    Args:
        common_name: Certificate common name
        organization_name: Organization name
        not_valid_before: Certificate start validity
        not_valid_after: Certificate end validity
        alt_names: Subject alternative names
        gen_key_type: Key type enum
        gen_key_size: RSA key size (for RSA keys)
        gen_curve: ECDSA curve (for ECDSA keys)

    Returns:
        Certificate configuration dictionary
    """
    conf: CertificateConfig = {
        "common_name": common_name,
        "organization": organization_name,
        "alt_names": alt_names or ["localhost"],
        "key_type": gen_key_type,
        "not_valid_before": not_valid_before,
        "NOT_VALID_AFTER": not_valid_after,
    }
    if gen_curve is not None:
        conf["curve"] = gen_curve
    if gen_key_size is not None:
        conf["key_size"] = gen_key_size
    return conf


def x__build_certificate_config__mutmut_17(
    common_name: str,
    organization_name: str,
    not_valid_before: datetime,
    not_valid_after: datetime,
    alt_names: list[str] | None,
    gen_key_type: KeyType,
    gen_key_size: int | None,
    gen_curve: CurveType | None,
) -> CertificateConfig:
    """Build certificate configuration dictionary.

    Args:
        common_name: Certificate common name
        organization_name: Organization name
        not_valid_before: Certificate start validity
        not_valid_after: Certificate end validity
        alt_names: Subject alternative names
        gen_key_type: Key type enum
        gen_key_size: RSA key size (for RSA keys)
        gen_curve: ECDSA curve (for ECDSA keys)

    Returns:
        Certificate configuration dictionary
    """
    conf: CertificateConfig = {
        "common_name": common_name,
        "organization": organization_name,
        "alt_names": alt_names or ["localhost"],
        "key_type": gen_key_type,
        "not_valid_before": not_valid_before,
        "not_valid_after": not_valid_after,
    }
    if gen_curve is None:
        conf["curve"] = gen_curve
    if gen_key_size is not None:
        conf["key_size"] = gen_key_size
    return conf


def x__build_certificate_config__mutmut_18(
    common_name: str,
    organization_name: str,
    not_valid_before: datetime,
    not_valid_after: datetime,
    alt_names: list[str] | None,
    gen_key_type: KeyType,
    gen_key_size: int | None,
    gen_curve: CurveType | None,
) -> CertificateConfig:
    """Build certificate configuration dictionary.

    Args:
        common_name: Certificate common name
        organization_name: Organization name
        not_valid_before: Certificate start validity
        not_valid_after: Certificate end validity
        alt_names: Subject alternative names
        gen_key_type: Key type enum
        gen_key_size: RSA key size (for RSA keys)
        gen_curve: ECDSA curve (for ECDSA keys)

    Returns:
        Certificate configuration dictionary
    """
    conf: CertificateConfig = {
        "common_name": common_name,
        "organization": organization_name,
        "alt_names": alt_names or ["localhost"],
        "key_type": gen_key_type,
        "not_valid_before": not_valid_before,
        "not_valid_after": not_valid_after,
    }
    if gen_curve is not None:
        conf["curve"] = None
    if gen_key_size is not None:
        conf["key_size"] = gen_key_size
    return conf


def x__build_certificate_config__mutmut_19(
    common_name: str,
    organization_name: str,
    not_valid_before: datetime,
    not_valid_after: datetime,
    alt_names: list[str] | None,
    gen_key_type: KeyType,
    gen_key_size: int | None,
    gen_curve: CurveType | None,
) -> CertificateConfig:
    """Build certificate configuration dictionary.

    Args:
        common_name: Certificate common name
        organization_name: Organization name
        not_valid_before: Certificate start validity
        not_valid_after: Certificate end validity
        alt_names: Subject alternative names
        gen_key_type: Key type enum
        gen_key_size: RSA key size (for RSA keys)
        gen_curve: ECDSA curve (for ECDSA keys)

    Returns:
        Certificate configuration dictionary
    """
    conf: CertificateConfig = {
        "common_name": common_name,
        "organization": organization_name,
        "alt_names": alt_names or ["localhost"],
        "key_type": gen_key_type,
        "not_valid_before": not_valid_before,
        "not_valid_after": not_valid_after,
    }
    if gen_curve is not None:
        conf["XXcurveXX"] = gen_curve
    if gen_key_size is not None:
        conf["key_size"] = gen_key_size
    return conf


def x__build_certificate_config__mutmut_20(
    common_name: str,
    organization_name: str,
    not_valid_before: datetime,
    not_valid_after: datetime,
    alt_names: list[str] | None,
    gen_key_type: KeyType,
    gen_key_size: int | None,
    gen_curve: CurveType | None,
) -> CertificateConfig:
    """Build certificate configuration dictionary.

    Args:
        common_name: Certificate common name
        organization_name: Organization name
        not_valid_before: Certificate start validity
        not_valid_after: Certificate end validity
        alt_names: Subject alternative names
        gen_key_type: Key type enum
        gen_key_size: RSA key size (for RSA keys)
        gen_curve: ECDSA curve (for ECDSA keys)

    Returns:
        Certificate configuration dictionary
    """
    conf: CertificateConfig = {
        "common_name": common_name,
        "organization": organization_name,
        "alt_names": alt_names or ["localhost"],
        "key_type": gen_key_type,
        "not_valid_before": not_valid_before,
        "not_valid_after": not_valid_after,
    }
    if gen_curve is not None:
        conf["CURVE"] = gen_curve
    if gen_key_size is not None:
        conf["key_size"] = gen_key_size
    return conf


def x__build_certificate_config__mutmut_21(
    common_name: str,
    organization_name: str,
    not_valid_before: datetime,
    not_valid_after: datetime,
    alt_names: list[str] | None,
    gen_key_type: KeyType,
    gen_key_size: int | None,
    gen_curve: CurveType | None,
) -> CertificateConfig:
    """Build certificate configuration dictionary.

    Args:
        common_name: Certificate common name
        organization_name: Organization name
        not_valid_before: Certificate start validity
        not_valid_after: Certificate end validity
        alt_names: Subject alternative names
        gen_key_type: Key type enum
        gen_key_size: RSA key size (for RSA keys)
        gen_curve: ECDSA curve (for ECDSA keys)

    Returns:
        Certificate configuration dictionary
    """
    conf: CertificateConfig = {
        "common_name": common_name,
        "organization": organization_name,
        "alt_names": alt_names or ["localhost"],
        "key_type": gen_key_type,
        "not_valid_before": not_valid_before,
        "not_valid_after": not_valid_after,
    }
    if gen_curve is not None:
        conf["curve"] = gen_curve
    if gen_key_size is None:
        conf["key_size"] = gen_key_size
    return conf


def x__build_certificate_config__mutmut_22(
    common_name: str,
    organization_name: str,
    not_valid_before: datetime,
    not_valid_after: datetime,
    alt_names: list[str] | None,
    gen_key_type: KeyType,
    gen_key_size: int | None,
    gen_curve: CurveType | None,
) -> CertificateConfig:
    """Build certificate configuration dictionary.

    Args:
        common_name: Certificate common name
        organization_name: Organization name
        not_valid_before: Certificate start validity
        not_valid_after: Certificate end validity
        alt_names: Subject alternative names
        gen_key_type: Key type enum
        gen_key_size: RSA key size (for RSA keys)
        gen_curve: ECDSA curve (for ECDSA keys)

    Returns:
        Certificate configuration dictionary
    """
    conf: CertificateConfig = {
        "common_name": common_name,
        "organization": organization_name,
        "alt_names": alt_names or ["localhost"],
        "key_type": gen_key_type,
        "not_valid_before": not_valid_before,
        "not_valid_after": not_valid_after,
    }
    if gen_curve is not None:
        conf["curve"] = gen_curve
    if gen_key_size is not None:
        conf["key_size"] = None
    return conf


def x__build_certificate_config__mutmut_23(
    common_name: str,
    organization_name: str,
    not_valid_before: datetime,
    not_valid_after: datetime,
    alt_names: list[str] | None,
    gen_key_type: KeyType,
    gen_key_size: int | None,
    gen_curve: CurveType | None,
) -> CertificateConfig:
    """Build certificate configuration dictionary.

    Args:
        common_name: Certificate common name
        organization_name: Organization name
        not_valid_before: Certificate start validity
        not_valid_after: Certificate end validity
        alt_names: Subject alternative names
        gen_key_type: Key type enum
        gen_key_size: RSA key size (for RSA keys)
        gen_curve: ECDSA curve (for ECDSA keys)

    Returns:
        Certificate configuration dictionary
    """
    conf: CertificateConfig = {
        "common_name": common_name,
        "organization": organization_name,
        "alt_names": alt_names or ["localhost"],
        "key_type": gen_key_type,
        "not_valid_before": not_valid_before,
        "not_valid_after": not_valid_after,
    }
    if gen_curve is not None:
        conf["curve"] = gen_curve
    if gen_key_size is not None:
        conf["XXkey_sizeXX"] = gen_key_size
    return conf


def x__build_certificate_config__mutmut_24(
    common_name: str,
    organization_name: str,
    not_valid_before: datetime,
    not_valid_after: datetime,
    alt_names: list[str] | None,
    gen_key_type: KeyType,
    gen_key_size: int | None,
    gen_curve: CurveType | None,
) -> CertificateConfig:
    """Build certificate configuration dictionary.

    Args:
        common_name: Certificate common name
        organization_name: Organization name
        not_valid_before: Certificate start validity
        not_valid_after: Certificate end validity
        alt_names: Subject alternative names
        gen_key_type: Key type enum
        gen_key_size: RSA key size (for RSA keys)
        gen_curve: ECDSA curve (for ECDSA keys)

    Returns:
        Certificate configuration dictionary
    """
    conf: CertificateConfig = {
        "common_name": common_name,
        "organization": organization_name,
        "alt_names": alt_names or ["localhost"],
        "key_type": gen_key_type,
        "not_valid_before": not_valid_before,
        "not_valid_after": not_valid_after,
    }
    if gen_curve is not None:
        conf["curve"] = gen_curve
    if gen_key_size is not None:
        conf["KEY_SIZE"] = gen_key_size
    return conf


x__build_certificate_config__mutmut_mutants: ClassVar[MutantDict] = {
    "x__build_certificate_config__mutmut_1": x__build_certificate_config__mutmut_1,
    "x__build_certificate_config__mutmut_2": x__build_certificate_config__mutmut_2,
    "x__build_certificate_config__mutmut_3": x__build_certificate_config__mutmut_3,
    "x__build_certificate_config__mutmut_4": x__build_certificate_config__mutmut_4,
    "x__build_certificate_config__mutmut_5": x__build_certificate_config__mutmut_5,
    "x__build_certificate_config__mutmut_6": x__build_certificate_config__mutmut_6,
    "x__build_certificate_config__mutmut_7": x__build_certificate_config__mutmut_7,
    "x__build_certificate_config__mutmut_8": x__build_certificate_config__mutmut_8,
    "x__build_certificate_config__mutmut_9": x__build_certificate_config__mutmut_9,
    "x__build_certificate_config__mutmut_10": x__build_certificate_config__mutmut_10,
    "x__build_certificate_config__mutmut_11": x__build_certificate_config__mutmut_11,
    "x__build_certificate_config__mutmut_12": x__build_certificate_config__mutmut_12,
    "x__build_certificate_config__mutmut_13": x__build_certificate_config__mutmut_13,
    "x__build_certificate_config__mutmut_14": x__build_certificate_config__mutmut_14,
    "x__build_certificate_config__mutmut_15": x__build_certificate_config__mutmut_15,
    "x__build_certificate_config__mutmut_16": x__build_certificate_config__mutmut_16,
    "x__build_certificate_config__mutmut_17": x__build_certificate_config__mutmut_17,
    "x__build_certificate_config__mutmut_18": x__build_certificate_config__mutmut_18,
    "x__build_certificate_config__mutmut_19": x__build_certificate_config__mutmut_19,
    "x__build_certificate_config__mutmut_20": x__build_certificate_config__mutmut_20,
    "x__build_certificate_config__mutmut_21": x__build_certificate_config__mutmut_21,
    "x__build_certificate_config__mutmut_22": x__build_certificate_config__mutmut_22,
    "x__build_certificate_config__mutmut_23": x__build_certificate_config__mutmut_23,
    "x__build_certificate_config__mutmut_24": x__build_certificate_config__mutmut_24,
}


def _build_certificate_config(*args, **kwargs):
    result = _mutmut_trampoline(
        x__build_certificate_config__mutmut_orig, x__build_certificate_config__mutmut_mutants, args, kwargs
    )
    return result


_build_certificate_config.__signature__ = _mutmut_signature(x__build_certificate_config__mutmut_orig)
x__build_certificate_config__mutmut_orig.__name__ = "x__build_certificate_config"


def x__serialize_to_pem__mutmut_orig(
    x509_cert: x509.Certificate,
    private_key: KeyPair,
) -> tuple[str, str]:
    """Serialize certificate and private key to PEM format.

    Args:
        x509_cert: X.509 certificate object
        private_key: Private key object

    Returns:
        Tuple of (cert_pem, key_pem)
    """
    cert_pem = x509_cert.public_bytes(serialization.Encoding.PEM).decode("utf-8")
    key_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    ).decode("utf-8")
    return cert_pem, key_pem


def x__serialize_to_pem__mutmut_1(
    x509_cert: x509.Certificate,
    private_key: KeyPair,
) -> tuple[str, str]:
    """Serialize certificate and private key to PEM format.

    Args:
        x509_cert: X.509 certificate object
        private_key: Private key object

    Returns:
        Tuple of (cert_pem, key_pem)
    """
    cert_pem = None
    key_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    ).decode("utf-8")
    return cert_pem, key_pem


def x__serialize_to_pem__mutmut_2(
    x509_cert: x509.Certificate,
    private_key: KeyPair,
) -> tuple[str, str]:
    """Serialize certificate and private key to PEM format.

    Args:
        x509_cert: X.509 certificate object
        private_key: Private key object

    Returns:
        Tuple of (cert_pem, key_pem)
    """
    cert_pem = x509_cert.public_bytes(serialization.Encoding.PEM).decode(None)
    key_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    ).decode("utf-8")
    return cert_pem, key_pem


def x__serialize_to_pem__mutmut_3(
    x509_cert: x509.Certificate,
    private_key: KeyPair,
) -> tuple[str, str]:
    """Serialize certificate and private key to PEM format.

    Args:
        x509_cert: X.509 certificate object
        private_key: Private key object

    Returns:
        Tuple of (cert_pem, key_pem)
    """
    cert_pem = x509_cert.public_bytes(None).decode("utf-8")
    key_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    ).decode("utf-8")
    return cert_pem, key_pem


def x__serialize_to_pem__mutmut_4(
    x509_cert: x509.Certificate,
    private_key: KeyPair,
) -> tuple[str, str]:
    """Serialize certificate and private key to PEM format.

    Args:
        x509_cert: X.509 certificate object
        private_key: Private key object

    Returns:
        Tuple of (cert_pem, key_pem)
    """
    cert_pem = x509_cert.public_bytes(serialization.Encoding.PEM).decode("XXutf-8XX")
    key_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    ).decode("utf-8")
    return cert_pem, key_pem


def x__serialize_to_pem__mutmut_5(
    x509_cert: x509.Certificate,
    private_key: KeyPair,
) -> tuple[str, str]:
    """Serialize certificate and private key to PEM format.

    Args:
        x509_cert: X.509 certificate object
        private_key: Private key object

    Returns:
        Tuple of (cert_pem, key_pem)
    """
    cert_pem = x509_cert.public_bytes(serialization.Encoding.PEM).decode("UTF-8")
    key_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    ).decode("utf-8")
    return cert_pem, key_pem


def x__serialize_to_pem__mutmut_6(
    x509_cert: x509.Certificate,
    private_key: KeyPair,
) -> tuple[str, str]:
    """Serialize certificate and private key to PEM format.

    Args:
        x509_cert: X.509 certificate object
        private_key: Private key object

    Returns:
        Tuple of (cert_pem, key_pem)
    """
    cert_pem = x509_cert.public_bytes(serialization.Encoding.PEM).decode("utf-8")
    key_pem = None
    return cert_pem, key_pem


def x__serialize_to_pem__mutmut_7(
    x509_cert: x509.Certificate,
    private_key: KeyPair,
) -> tuple[str, str]:
    """Serialize certificate and private key to PEM format.

    Args:
        x509_cert: X.509 certificate object
        private_key: Private key object

    Returns:
        Tuple of (cert_pem, key_pem)
    """
    cert_pem = x509_cert.public_bytes(serialization.Encoding.PEM).decode("utf-8")
    key_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    ).decode(None)
    return cert_pem, key_pem


def x__serialize_to_pem__mutmut_8(
    x509_cert: x509.Certificate,
    private_key: KeyPair,
) -> tuple[str, str]:
    """Serialize certificate and private key to PEM format.

    Args:
        x509_cert: X.509 certificate object
        private_key: Private key object

    Returns:
        Tuple of (cert_pem, key_pem)
    """
    cert_pem = x509_cert.public_bytes(serialization.Encoding.PEM).decode("utf-8")
    key_pem = private_key.private_bytes(
        encoding=None,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    ).decode("utf-8")
    return cert_pem, key_pem


def x__serialize_to_pem__mutmut_9(
    x509_cert: x509.Certificate,
    private_key: KeyPair,
) -> tuple[str, str]:
    """Serialize certificate and private key to PEM format.

    Args:
        x509_cert: X.509 certificate object
        private_key: Private key object

    Returns:
        Tuple of (cert_pem, key_pem)
    """
    cert_pem = x509_cert.public_bytes(serialization.Encoding.PEM).decode("utf-8")
    key_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=None,
        encryption_algorithm=serialization.NoEncryption(),
    ).decode("utf-8")
    return cert_pem, key_pem


def x__serialize_to_pem__mutmut_10(
    x509_cert: x509.Certificate,
    private_key: KeyPair,
) -> tuple[str, str]:
    """Serialize certificate and private key to PEM format.

    Args:
        x509_cert: X.509 certificate object
        private_key: Private key object

    Returns:
        Tuple of (cert_pem, key_pem)
    """
    cert_pem = x509_cert.public_bytes(serialization.Encoding.PEM).decode("utf-8")
    key_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=None,
    ).decode("utf-8")
    return cert_pem, key_pem


def x__serialize_to_pem__mutmut_11(
    x509_cert: x509.Certificate,
    private_key: KeyPair,
) -> tuple[str, str]:
    """Serialize certificate and private key to PEM format.

    Args:
        x509_cert: X.509 certificate object
        private_key: Private key object

    Returns:
        Tuple of (cert_pem, key_pem)
    """
    cert_pem = x509_cert.public_bytes(serialization.Encoding.PEM).decode("utf-8")
    key_pem = private_key.private_bytes(
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    ).decode("utf-8")
    return cert_pem, key_pem


def x__serialize_to_pem__mutmut_12(
    x509_cert: x509.Certificate,
    private_key: KeyPair,
) -> tuple[str, str]:
    """Serialize certificate and private key to PEM format.

    Args:
        x509_cert: X.509 certificate object
        private_key: Private key object

    Returns:
        Tuple of (cert_pem, key_pem)
    """
    cert_pem = x509_cert.public_bytes(serialization.Encoding.PEM).decode("utf-8")
    key_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        encryption_algorithm=serialization.NoEncryption(),
    ).decode("utf-8")
    return cert_pem, key_pem


def x__serialize_to_pem__mutmut_13(
    x509_cert: x509.Certificate,
    private_key: KeyPair,
) -> tuple[str, str]:
    """Serialize certificate and private key to PEM format.

    Args:
        x509_cert: X.509 certificate object
        private_key: Private key object

    Returns:
        Tuple of (cert_pem, key_pem)
    """
    cert_pem = x509_cert.public_bytes(serialization.Encoding.PEM).decode("utf-8")
    key_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
    ).decode("utf-8")
    return cert_pem, key_pem


def x__serialize_to_pem__mutmut_14(
    x509_cert: x509.Certificate,
    private_key: KeyPair,
) -> tuple[str, str]:
    """Serialize certificate and private key to PEM format.

    Args:
        x509_cert: X.509 certificate object
        private_key: Private key object

    Returns:
        Tuple of (cert_pem, key_pem)
    """
    cert_pem = x509_cert.public_bytes(serialization.Encoding.PEM).decode("utf-8")
    key_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    ).decode("XXutf-8XX")
    return cert_pem, key_pem


def x__serialize_to_pem__mutmut_15(
    x509_cert: x509.Certificate,
    private_key: KeyPair,
) -> tuple[str, str]:
    """Serialize certificate and private key to PEM format.

    Args:
        x509_cert: X.509 certificate object
        private_key: Private key object

    Returns:
        Tuple of (cert_pem, key_pem)
    """
    cert_pem = x509_cert.public_bytes(serialization.Encoding.PEM).decode("utf-8")
    key_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    ).decode("UTF-8")
    return cert_pem, key_pem


x__serialize_to_pem__mutmut_mutants: ClassVar[MutantDict] = {
    "x__serialize_to_pem__mutmut_1": x__serialize_to_pem__mutmut_1,
    "x__serialize_to_pem__mutmut_2": x__serialize_to_pem__mutmut_2,
    "x__serialize_to_pem__mutmut_3": x__serialize_to_pem__mutmut_3,
    "x__serialize_to_pem__mutmut_4": x__serialize_to_pem__mutmut_4,
    "x__serialize_to_pem__mutmut_5": x__serialize_to_pem__mutmut_5,
    "x__serialize_to_pem__mutmut_6": x__serialize_to_pem__mutmut_6,
    "x__serialize_to_pem__mutmut_7": x__serialize_to_pem__mutmut_7,
    "x__serialize_to_pem__mutmut_8": x__serialize_to_pem__mutmut_8,
    "x__serialize_to_pem__mutmut_9": x__serialize_to_pem__mutmut_9,
    "x__serialize_to_pem__mutmut_10": x__serialize_to_pem__mutmut_10,
    "x__serialize_to_pem__mutmut_11": x__serialize_to_pem__mutmut_11,
    "x__serialize_to_pem__mutmut_12": x__serialize_to_pem__mutmut_12,
    "x__serialize_to_pem__mutmut_13": x__serialize_to_pem__mutmut_13,
    "x__serialize_to_pem__mutmut_14": x__serialize_to_pem__mutmut_14,
    "x__serialize_to_pem__mutmut_15": x__serialize_to_pem__mutmut_15,
}


def _serialize_to_pem(*args, **kwargs):
    result = _mutmut_trampoline(
        x__serialize_to_pem__mutmut_orig, x__serialize_to_pem__mutmut_mutants, args, kwargs
    )
    return result


_serialize_to_pem.__signature__ = _mutmut_signature(x__serialize_to_pem__mutmut_orig)
x__serialize_to_pem__mutmut_orig.__name__ = "x__serialize_to_pem"


if TYPE_CHECKING:
    from cryptography import x509
    from cryptography.hazmat.primitives import serialization

try:
    from cryptography import x509
    from cryptography.hazmat.primitives import serialization

    _HAS_CRYPTO = True
except ImportError:
    _HAS_CRYPTO = False


def x_generate_certificate__mutmut_orig(
    common_name: str,
    organization_name: str,
    validity_days: int,
    key_type: str = DEFAULT_CERTIFICATE_KEY_TYPE,
    key_size: int = DEFAULT_RSA_KEY_SIZE,
    ecdsa_curve: str = DEFAULT_CERTIFICATE_CURVE,
    alt_names: list[str] | None = None,
    is_ca: bool = False,
    is_client_cert: bool = False,
) -> tuple[
    CertificateBase,
    x509.Certificate,
    KeyPair,
    str,
    str,
]:
    """Generate a new certificate with a keypair.

    Returns:
        Tuple of (CertificateBase, X509Certificate, private_key, cert_pem, key_pem)

    """
    try:
        logger.debug("📜🔑🚀 Generating new keypair")

        # Calculate validity period
        now = datetime.now(UTC)
        not_valid_before = now - timedelta(days=1)
        not_valid_after = now + timedelta(days=validity_days)

        # Parse and validate key type parameters
        gen_key_type, gen_key_size, gen_curve = _parse_key_type_and_params(key_type, key_size, ecdsa_curve)

        # Build certificate configuration
        conf = _build_certificate_config(
            common_name=common_name,
            organization_name=organization_name,
            not_valid_before=not_valid_before,
            not_valid_after=not_valid_after,
            alt_names=alt_names,
            gen_key_type=gen_key_type,
            gen_key_size=gen_key_size,
            gen_curve=gen_curve,
        )
        logger.debug(f"📜🔑🚀 Generation config: {conf}")

        # Generate base certificate and private key
        base, private_key = CertificateBase.create(conf)

        # Create X.509 certificate
        x509_cert = create_x509_certificate(
            base=base,
            private_key=private_key,
            alt_names=alt_names or ["localhost"],
            is_ca=is_ca,
            is_client_cert=is_client_cert,
        )

        if x509_cert is None:
            raise CertificateError("Certificate object (_cert) is None after creation")

        # Serialize to PEM format
        cert_pem, key_pem = _serialize_to_pem(x509_cert, private_key)

        logger.debug("📜🔑✅ Generated cert and key")

        return base, x509_cert, private_key, cert_pem, key_pem

    except Exception as e:
        logger.error(
            f"📜❌ Failed to generate certificate. Error: {type(e).__name__}: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError(f"Failed to initialize certificate. Original error: {type(e).__name__}") from e


def x_generate_certificate__mutmut_1(
    common_name: str,
    organization_name: str,
    validity_days: int,
    key_type: str = DEFAULT_CERTIFICATE_KEY_TYPE,
    key_size: int = DEFAULT_RSA_KEY_SIZE,
    ecdsa_curve: str = DEFAULT_CERTIFICATE_CURVE,
    alt_names: list[str] | None = None,
    is_ca: bool = True,
    is_client_cert: bool = False,
) -> tuple[
    CertificateBase,
    x509.Certificate,
    KeyPair,
    str,
    str,
]:
    """Generate a new certificate with a keypair.

    Returns:
        Tuple of (CertificateBase, X509Certificate, private_key, cert_pem, key_pem)

    """
    try:
        logger.debug("📜🔑🚀 Generating new keypair")

        # Calculate validity period
        now = datetime.now(UTC)
        not_valid_before = now - timedelta(days=1)
        not_valid_after = now + timedelta(days=validity_days)

        # Parse and validate key type parameters
        gen_key_type, gen_key_size, gen_curve = _parse_key_type_and_params(key_type, key_size, ecdsa_curve)

        # Build certificate configuration
        conf = _build_certificate_config(
            common_name=common_name,
            organization_name=organization_name,
            not_valid_before=not_valid_before,
            not_valid_after=not_valid_after,
            alt_names=alt_names,
            gen_key_type=gen_key_type,
            gen_key_size=gen_key_size,
            gen_curve=gen_curve,
        )
        logger.debug(f"📜🔑🚀 Generation config: {conf}")

        # Generate base certificate and private key
        base, private_key = CertificateBase.create(conf)

        # Create X.509 certificate
        x509_cert = create_x509_certificate(
            base=base,
            private_key=private_key,
            alt_names=alt_names or ["localhost"],
            is_ca=is_ca,
            is_client_cert=is_client_cert,
        )

        if x509_cert is None:
            raise CertificateError("Certificate object (_cert) is None after creation")

        # Serialize to PEM format
        cert_pem, key_pem = _serialize_to_pem(x509_cert, private_key)

        logger.debug("📜🔑✅ Generated cert and key")

        return base, x509_cert, private_key, cert_pem, key_pem

    except Exception as e:
        logger.error(
            f"📜❌ Failed to generate certificate. Error: {type(e).__name__}: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError(f"Failed to initialize certificate. Original error: {type(e).__name__}") from e


def x_generate_certificate__mutmut_2(
    common_name: str,
    organization_name: str,
    validity_days: int,
    key_type: str = DEFAULT_CERTIFICATE_KEY_TYPE,
    key_size: int = DEFAULT_RSA_KEY_SIZE,
    ecdsa_curve: str = DEFAULT_CERTIFICATE_CURVE,
    alt_names: list[str] | None = None,
    is_ca: bool = False,
    is_client_cert: bool = True,
) -> tuple[
    CertificateBase,
    x509.Certificate,
    KeyPair,
    str,
    str,
]:
    """Generate a new certificate with a keypair.

    Returns:
        Tuple of (CertificateBase, X509Certificate, private_key, cert_pem, key_pem)

    """
    try:
        logger.debug("📜🔑🚀 Generating new keypair")

        # Calculate validity period
        now = datetime.now(UTC)
        not_valid_before = now - timedelta(days=1)
        not_valid_after = now + timedelta(days=validity_days)

        # Parse and validate key type parameters
        gen_key_type, gen_key_size, gen_curve = _parse_key_type_and_params(key_type, key_size, ecdsa_curve)

        # Build certificate configuration
        conf = _build_certificate_config(
            common_name=common_name,
            organization_name=organization_name,
            not_valid_before=not_valid_before,
            not_valid_after=not_valid_after,
            alt_names=alt_names,
            gen_key_type=gen_key_type,
            gen_key_size=gen_key_size,
            gen_curve=gen_curve,
        )
        logger.debug(f"📜🔑🚀 Generation config: {conf}")

        # Generate base certificate and private key
        base, private_key = CertificateBase.create(conf)

        # Create X.509 certificate
        x509_cert = create_x509_certificate(
            base=base,
            private_key=private_key,
            alt_names=alt_names or ["localhost"],
            is_ca=is_ca,
            is_client_cert=is_client_cert,
        )

        if x509_cert is None:
            raise CertificateError("Certificate object (_cert) is None after creation")

        # Serialize to PEM format
        cert_pem, key_pem = _serialize_to_pem(x509_cert, private_key)

        logger.debug("📜🔑✅ Generated cert and key")

        return base, x509_cert, private_key, cert_pem, key_pem

    except Exception as e:
        logger.error(
            f"📜❌ Failed to generate certificate. Error: {type(e).__name__}: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError(f"Failed to initialize certificate. Original error: {type(e).__name__}") from e


def x_generate_certificate__mutmut_3(
    common_name: str,
    organization_name: str,
    validity_days: int,
    key_type: str = DEFAULT_CERTIFICATE_KEY_TYPE,
    key_size: int = DEFAULT_RSA_KEY_SIZE,
    ecdsa_curve: str = DEFAULT_CERTIFICATE_CURVE,
    alt_names: list[str] | None = None,
    is_ca: bool = False,
    is_client_cert: bool = False,
) -> tuple[
    CertificateBase,
    x509.Certificate,
    KeyPair,
    str,
    str,
]:
    """Generate a new certificate with a keypair.

    Returns:
        Tuple of (CertificateBase, X509Certificate, private_key, cert_pem, key_pem)

    """
    try:
        logger.debug(None)

        # Calculate validity period
        now = datetime.now(UTC)
        not_valid_before = now - timedelta(days=1)
        not_valid_after = now + timedelta(days=validity_days)

        # Parse and validate key type parameters
        gen_key_type, gen_key_size, gen_curve = _parse_key_type_and_params(key_type, key_size, ecdsa_curve)

        # Build certificate configuration
        conf = _build_certificate_config(
            common_name=common_name,
            organization_name=organization_name,
            not_valid_before=not_valid_before,
            not_valid_after=not_valid_after,
            alt_names=alt_names,
            gen_key_type=gen_key_type,
            gen_key_size=gen_key_size,
            gen_curve=gen_curve,
        )
        logger.debug(f"📜🔑🚀 Generation config: {conf}")

        # Generate base certificate and private key
        base, private_key = CertificateBase.create(conf)

        # Create X.509 certificate
        x509_cert = create_x509_certificate(
            base=base,
            private_key=private_key,
            alt_names=alt_names or ["localhost"],
            is_ca=is_ca,
            is_client_cert=is_client_cert,
        )

        if x509_cert is None:
            raise CertificateError("Certificate object (_cert) is None after creation")

        # Serialize to PEM format
        cert_pem, key_pem = _serialize_to_pem(x509_cert, private_key)

        logger.debug("📜🔑✅ Generated cert and key")

        return base, x509_cert, private_key, cert_pem, key_pem

    except Exception as e:
        logger.error(
            f"📜❌ Failed to generate certificate. Error: {type(e).__name__}: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError(f"Failed to initialize certificate. Original error: {type(e).__name__}") from e


def x_generate_certificate__mutmut_4(
    common_name: str,
    organization_name: str,
    validity_days: int,
    key_type: str = DEFAULT_CERTIFICATE_KEY_TYPE,
    key_size: int = DEFAULT_RSA_KEY_SIZE,
    ecdsa_curve: str = DEFAULT_CERTIFICATE_CURVE,
    alt_names: list[str] | None = None,
    is_ca: bool = False,
    is_client_cert: bool = False,
) -> tuple[
    CertificateBase,
    x509.Certificate,
    KeyPair,
    str,
    str,
]:
    """Generate a new certificate with a keypair.

    Returns:
        Tuple of (CertificateBase, X509Certificate, private_key, cert_pem, key_pem)

    """
    try:
        logger.debug("XX📜🔑🚀 Generating new keypairXX")

        # Calculate validity period
        now = datetime.now(UTC)
        not_valid_before = now - timedelta(days=1)
        not_valid_after = now + timedelta(days=validity_days)

        # Parse and validate key type parameters
        gen_key_type, gen_key_size, gen_curve = _parse_key_type_and_params(key_type, key_size, ecdsa_curve)

        # Build certificate configuration
        conf = _build_certificate_config(
            common_name=common_name,
            organization_name=organization_name,
            not_valid_before=not_valid_before,
            not_valid_after=not_valid_after,
            alt_names=alt_names,
            gen_key_type=gen_key_type,
            gen_key_size=gen_key_size,
            gen_curve=gen_curve,
        )
        logger.debug(f"📜🔑🚀 Generation config: {conf}")

        # Generate base certificate and private key
        base, private_key = CertificateBase.create(conf)

        # Create X.509 certificate
        x509_cert = create_x509_certificate(
            base=base,
            private_key=private_key,
            alt_names=alt_names or ["localhost"],
            is_ca=is_ca,
            is_client_cert=is_client_cert,
        )

        if x509_cert is None:
            raise CertificateError("Certificate object (_cert) is None after creation")

        # Serialize to PEM format
        cert_pem, key_pem = _serialize_to_pem(x509_cert, private_key)

        logger.debug("📜🔑✅ Generated cert and key")

        return base, x509_cert, private_key, cert_pem, key_pem

    except Exception as e:
        logger.error(
            f"📜❌ Failed to generate certificate. Error: {type(e).__name__}: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError(f"Failed to initialize certificate. Original error: {type(e).__name__}") from e


def x_generate_certificate__mutmut_5(
    common_name: str,
    organization_name: str,
    validity_days: int,
    key_type: str = DEFAULT_CERTIFICATE_KEY_TYPE,
    key_size: int = DEFAULT_RSA_KEY_SIZE,
    ecdsa_curve: str = DEFAULT_CERTIFICATE_CURVE,
    alt_names: list[str] | None = None,
    is_ca: bool = False,
    is_client_cert: bool = False,
) -> tuple[
    CertificateBase,
    x509.Certificate,
    KeyPair,
    str,
    str,
]:
    """Generate a new certificate with a keypair.

    Returns:
        Tuple of (CertificateBase, X509Certificate, private_key, cert_pem, key_pem)

    """
    try:
        logger.debug("📜🔑🚀 generating new keypair")

        # Calculate validity period
        now = datetime.now(UTC)
        not_valid_before = now - timedelta(days=1)
        not_valid_after = now + timedelta(days=validity_days)

        # Parse and validate key type parameters
        gen_key_type, gen_key_size, gen_curve = _parse_key_type_and_params(key_type, key_size, ecdsa_curve)

        # Build certificate configuration
        conf = _build_certificate_config(
            common_name=common_name,
            organization_name=organization_name,
            not_valid_before=not_valid_before,
            not_valid_after=not_valid_after,
            alt_names=alt_names,
            gen_key_type=gen_key_type,
            gen_key_size=gen_key_size,
            gen_curve=gen_curve,
        )
        logger.debug(f"📜🔑🚀 Generation config: {conf}")

        # Generate base certificate and private key
        base, private_key = CertificateBase.create(conf)

        # Create X.509 certificate
        x509_cert = create_x509_certificate(
            base=base,
            private_key=private_key,
            alt_names=alt_names or ["localhost"],
            is_ca=is_ca,
            is_client_cert=is_client_cert,
        )

        if x509_cert is None:
            raise CertificateError("Certificate object (_cert) is None after creation")

        # Serialize to PEM format
        cert_pem, key_pem = _serialize_to_pem(x509_cert, private_key)

        logger.debug("📜🔑✅ Generated cert and key")

        return base, x509_cert, private_key, cert_pem, key_pem

    except Exception as e:
        logger.error(
            f"📜❌ Failed to generate certificate. Error: {type(e).__name__}: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError(f"Failed to initialize certificate. Original error: {type(e).__name__}") from e


def x_generate_certificate__mutmut_6(
    common_name: str,
    organization_name: str,
    validity_days: int,
    key_type: str = DEFAULT_CERTIFICATE_KEY_TYPE,
    key_size: int = DEFAULT_RSA_KEY_SIZE,
    ecdsa_curve: str = DEFAULT_CERTIFICATE_CURVE,
    alt_names: list[str] | None = None,
    is_ca: bool = False,
    is_client_cert: bool = False,
) -> tuple[
    CertificateBase,
    x509.Certificate,
    KeyPair,
    str,
    str,
]:
    """Generate a new certificate with a keypair.

    Returns:
        Tuple of (CertificateBase, X509Certificate, private_key, cert_pem, key_pem)

    """
    try:
        logger.debug("📜🔑🚀 GENERATING NEW KEYPAIR")

        # Calculate validity period
        now = datetime.now(UTC)
        not_valid_before = now - timedelta(days=1)
        not_valid_after = now + timedelta(days=validity_days)

        # Parse and validate key type parameters
        gen_key_type, gen_key_size, gen_curve = _parse_key_type_and_params(key_type, key_size, ecdsa_curve)

        # Build certificate configuration
        conf = _build_certificate_config(
            common_name=common_name,
            organization_name=organization_name,
            not_valid_before=not_valid_before,
            not_valid_after=not_valid_after,
            alt_names=alt_names,
            gen_key_type=gen_key_type,
            gen_key_size=gen_key_size,
            gen_curve=gen_curve,
        )
        logger.debug(f"📜🔑🚀 Generation config: {conf}")

        # Generate base certificate and private key
        base, private_key = CertificateBase.create(conf)

        # Create X.509 certificate
        x509_cert = create_x509_certificate(
            base=base,
            private_key=private_key,
            alt_names=alt_names or ["localhost"],
            is_ca=is_ca,
            is_client_cert=is_client_cert,
        )

        if x509_cert is None:
            raise CertificateError("Certificate object (_cert) is None after creation")

        # Serialize to PEM format
        cert_pem, key_pem = _serialize_to_pem(x509_cert, private_key)

        logger.debug("📜🔑✅ Generated cert and key")

        return base, x509_cert, private_key, cert_pem, key_pem

    except Exception as e:
        logger.error(
            f"📜❌ Failed to generate certificate. Error: {type(e).__name__}: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError(f"Failed to initialize certificate. Original error: {type(e).__name__}") from e


def x_generate_certificate__mutmut_7(
    common_name: str,
    organization_name: str,
    validity_days: int,
    key_type: str = DEFAULT_CERTIFICATE_KEY_TYPE,
    key_size: int = DEFAULT_RSA_KEY_SIZE,
    ecdsa_curve: str = DEFAULT_CERTIFICATE_CURVE,
    alt_names: list[str] | None = None,
    is_ca: bool = False,
    is_client_cert: bool = False,
) -> tuple[
    CertificateBase,
    x509.Certificate,
    KeyPair,
    str,
    str,
]:
    """Generate a new certificate with a keypair.

    Returns:
        Tuple of (CertificateBase, X509Certificate, private_key, cert_pem, key_pem)

    """
    try:
        logger.debug("📜🔑🚀 Generating new keypair")

        # Calculate validity period
        now = None
        not_valid_before = now - timedelta(days=1)
        not_valid_after = now + timedelta(days=validity_days)

        # Parse and validate key type parameters
        gen_key_type, gen_key_size, gen_curve = _parse_key_type_and_params(key_type, key_size, ecdsa_curve)

        # Build certificate configuration
        conf = _build_certificate_config(
            common_name=common_name,
            organization_name=organization_name,
            not_valid_before=not_valid_before,
            not_valid_after=not_valid_after,
            alt_names=alt_names,
            gen_key_type=gen_key_type,
            gen_key_size=gen_key_size,
            gen_curve=gen_curve,
        )
        logger.debug(f"📜🔑🚀 Generation config: {conf}")

        # Generate base certificate and private key
        base, private_key = CertificateBase.create(conf)

        # Create X.509 certificate
        x509_cert = create_x509_certificate(
            base=base,
            private_key=private_key,
            alt_names=alt_names or ["localhost"],
            is_ca=is_ca,
            is_client_cert=is_client_cert,
        )

        if x509_cert is None:
            raise CertificateError("Certificate object (_cert) is None after creation")

        # Serialize to PEM format
        cert_pem, key_pem = _serialize_to_pem(x509_cert, private_key)

        logger.debug("📜🔑✅ Generated cert and key")

        return base, x509_cert, private_key, cert_pem, key_pem

    except Exception as e:
        logger.error(
            f"📜❌ Failed to generate certificate. Error: {type(e).__name__}: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError(f"Failed to initialize certificate. Original error: {type(e).__name__}") from e


def x_generate_certificate__mutmut_8(
    common_name: str,
    organization_name: str,
    validity_days: int,
    key_type: str = DEFAULT_CERTIFICATE_KEY_TYPE,
    key_size: int = DEFAULT_RSA_KEY_SIZE,
    ecdsa_curve: str = DEFAULT_CERTIFICATE_CURVE,
    alt_names: list[str] | None = None,
    is_ca: bool = False,
    is_client_cert: bool = False,
) -> tuple[
    CertificateBase,
    x509.Certificate,
    KeyPair,
    str,
    str,
]:
    """Generate a new certificate with a keypair.

    Returns:
        Tuple of (CertificateBase, X509Certificate, private_key, cert_pem, key_pem)

    """
    try:
        logger.debug("📜🔑🚀 Generating new keypair")

        # Calculate validity period
        now = datetime.now(None)
        not_valid_before = now - timedelta(days=1)
        not_valid_after = now + timedelta(days=validity_days)

        # Parse and validate key type parameters
        gen_key_type, gen_key_size, gen_curve = _parse_key_type_and_params(key_type, key_size, ecdsa_curve)

        # Build certificate configuration
        conf = _build_certificate_config(
            common_name=common_name,
            organization_name=organization_name,
            not_valid_before=not_valid_before,
            not_valid_after=not_valid_after,
            alt_names=alt_names,
            gen_key_type=gen_key_type,
            gen_key_size=gen_key_size,
            gen_curve=gen_curve,
        )
        logger.debug(f"📜🔑🚀 Generation config: {conf}")

        # Generate base certificate and private key
        base, private_key = CertificateBase.create(conf)

        # Create X.509 certificate
        x509_cert = create_x509_certificate(
            base=base,
            private_key=private_key,
            alt_names=alt_names or ["localhost"],
            is_ca=is_ca,
            is_client_cert=is_client_cert,
        )

        if x509_cert is None:
            raise CertificateError("Certificate object (_cert) is None after creation")

        # Serialize to PEM format
        cert_pem, key_pem = _serialize_to_pem(x509_cert, private_key)

        logger.debug("📜🔑✅ Generated cert and key")

        return base, x509_cert, private_key, cert_pem, key_pem

    except Exception as e:
        logger.error(
            f"📜❌ Failed to generate certificate. Error: {type(e).__name__}: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError(f"Failed to initialize certificate. Original error: {type(e).__name__}") from e


def x_generate_certificate__mutmut_9(
    common_name: str,
    organization_name: str,
    validity_days: int,
    key_type: str = DEFAULT_CERTIFICATE_KEY_TYPE,
    key_size: int = DEFAULT_RSA_KEY_SIZE,
    ecdsa_curve: str = DEFAULT_CERTIFICATE_CURVE,
    alt_names: list[str] | None = None,
    is_ca: bool = False,
    is_client_cert: bool = False,
) -> tuple[
    CertificateBase,
    x509.Certificate,
    KeyPair,
    str,
    str,
]:
    """Generate a new certificate with a keypair.

    Returns:
        Tuple of (CertificateBase, X509Certificate, private_key, cert_pem, key_pem)

    """
    try:
        logger.debug("📜🔑🚀 Generating new keypair")

        # Calculate validity period
        now = datetime.now(UTC)
        not_valid_before = None
        not_valid_after = now + timedelta(days=validity_days)

        # Parse and validate key type parameters
        gen_key_type, gen_key_size, gen_curve = _parse_key_type_and_params(key_type, key_size, ecdsa_curve)

        # Build certificate configuration
        conf = _build_certificate_config(
            common_name=common_name,
            organization_name=organization_name,
            not_valid_before=not_valid_before,
            not_valid_after=not_valid_after,
            alt_names=alt_names,
            gen_key_type=gen_key_type,
            gen_key_size=gen_key_size,
            gen_curve=gen_curve,
        )
        logger.debug(f"📜🔑🚀 Generation config: {conf}")

        # Generate base certificate and private key
        base, private_key = CertificateBase.create(conf)

        # Create X.509 certificate
        x509_cert = create_x509_certificate(
            base=base,
            private_key=private_key,
            alt_names=alt_names or ["localhost"],
            is_ca=is_ca,
            is_client_cert=is_client_cert,
        )

        if x509_cert is None:
            raise CertificateError("Certificate object (_cert) is None after creation")

        # Serialize to PEM format
        cert_pem, key_pem = _serialize_to_pem(x509_cert, private_key)

        logger.debug("📜🔑✅ Generated cert and key")

        return base, x509_cert, private_key, cert_pem, key_pem

    except Exception as e:
        logger.error(
            f"📜❌ Failed to generate certificate. Error: {type(e).__name__}: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError(f"Failed to initialize certificate. Original error: {type(e).__name__}") from e


def x_generate_certificate__mutmut_10(
    common_name: str,
    organization_name: str,
    validity_days: int,
    key_type: str = DEFAULT_CERTIFICATE_KEY_TYPE,
    key_size: int = DEFAULT_RSA_KEY_SIZE,
    ecdsa_curve: str = DEFAULT_CERTIFICATE_CURVE,
    alt_names: list[str] | None = None,
    is_ca: bool = False,
    is_client_cert: bool = False,
) -> tuple[
    CertificateBase,
    x509.Certificate,
    KeyPair,
    str,
    str,
]:
    """Generate a new certificate with a keypair.

    Returns:
        Tuple of (CertificateBase, X509Certificate, private_key, cert_pem, key_pem)

    """
    try:
        logger.debug("📜🔑🚀 Generating new keypair")

        # Calculate validity period
        now = datetime.now(UTC)
        not_valid_before = now + timedelta(days=1)
        not_valid_after = now + timedelta(days=validity_days)

        # Parse and validate key type parameters
        gen_key_type, gen_key_size, gen_curve = _parse_key_type_and_params(key_type, key_size, ecdsa_curve)

        # Build certificate configuration
        conf = _build_certificate_config(
            common_name=common_name,
            organization_name=organization_name,
            not_valid_before=not_valid_before,
            not_valid_after=not_valid_after,
            alt_names=alt_names,
            gen_key_type=gen_key_type,
            gen_key_size=gen_key_size,
            gen_curve=gen_curve,
        )
        logger.debug(f"📜🔑🚀 Generation config: {conf}")

        # Generate base certificate and private key
        base, private_key = CertificateBase.create(conf)

        # Create X.509 certificate
        x509_cert = create_x509_certificate(
            base=base,
            private_key=private_key,
            alt_names=alt_names or ["localhost"],
            is_ca=is_ca,
            is_client_cert=is_client_cert,
        )

        if x509_cert is None:
            raise CertificateError("Certificate object (_cert) is None after creation")

        # Serialize to PEM format
        cert_pem, key_pem = _serialize_to_pem(x509_cert, private_key)

        logger.debug("📜🔑✅ Generated cert and key")

        return base, x509_cert, private_key, cert_pem, key_pem

    except Exception as e:
        logger.error(
            f"📜❌ Failed to generate certificate. Error: {type(e).__name__}: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError(f"Failed to initialize certificate. Original error: {type(e).__name__}") from e


def x_generate_certificate__mutmut_11(
    common_name: str,
    organization_name: str,
    validity_days: int,
    key_type: str = DEFAULT_CERTIFICATE_KEY_TYPE,
    key_size: int = DEFAULT_RSA_KEY_SIZE,
    ecdsa_curve: str = DEFAULT_CERTIFICATE_CURVE,
    alt_names: list[str] | None = None,
    is_ca: bool = False,
    is_client_cert: bool = False,
) -> tuple[
    CertificateBase,
    x509.Certificate,
    KeyPair,
    str,
    str,
]:
    """Generate a new certificate with a keypair.

    Returns:
        Tuple of (CertificateBase, X509Certificate, private_key, cert_pem, key_pem)

    """
    try:
        logger.debug("📜🔑🚀 Generating new keypair")

        # Calculate validity period
        now = datetime.now(UTC)
        not_valid_before = now - timedelta(days=None)
        not_valid_after = now + timedelta(days=validity_days)

        # Parse and validate key type parameters
        gen_key_type, gen_key_size, gen_curve = _parse_key_type_and_params(key_type, key_size, ecdsa_curve)

        # Build certificate configuration
        conf = _build_certificate_config(
            common_name=common_name,
            organization_name=organization_name,
            not_valid_before=not_valid_before,
            not_valid_after=not_valid_after,
            alt_names=alt_names,
            gen_key_type=gen_key_type,
            gen_key_size=gen_key_size,
            gen_curve=gen_curve,
        )
        logger.debug(f"📜🔑🚀 Generation config: {conf}")

        # Generate base certificate and private key
        base, private_key = CertificateBase.create(conf)

        # Create X.509 certificate
        x509_cert = create_x509_certificate(
            base=base,
            private_key=private_key,
            alt_names=alt_names or ["localhost"],
            is_ca=is_ca,
            is_client_cert=is_client_cert,
        )

        if x509_cert is None:
            raise CertificateError("Certificate object (_cert) is None after creation")

        # Serialize to PEM format
        cert_pem, key_pem = _serialize_to_pem(x509_cert, private_key)

        logger.debug("📜🔑✅ Generated cert and key")

        return base, x509_cert, private_key, cert_pem, key_pem

    except Exception as e:
        logger.error(
            f"📜❌ Failed to generate certificate. Error: {type(e).__name__}: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError(f"Failed to initialize certificate. Original error: {type(e).__name__}") from e


def x_generate_certificate__mutmut_12(
    common_name: str,
    organization_name: str,
    validity_days: int,
    key_type: str = DEFAULT_CERTIFICATE_KEY_TYPE,
    key_size: int = DEFAULT_RSA_KEY_SIZE,
    ecdsa_curve: str = DEFAULT_CERTIFICATE_CURVE,
    alt_names: list[str] | None = None,
    is_ca: bool = False,
    is_client_cert: bool = False,
) -> tuple[
    CertificateBase,
    x509.Certificate,
    KeyPair,
    str,
    str,
]:
    """Generate a new certificate with a keypair.

    Returns:
        Tuple of (CertificateBase, X509Certificate, private_key, cert_pem, key_pem)

    """
    try:
        logger.debug("📜🔑🚀 Generating new keypair")

        # Calculate validity period
        now = datetime.now(UTC)
        not_valid_before = now - timedelta(days=2)
        not_valid_after = now + timedelta(days=validity_days)

        # Parse and validate key type parameters
        gen_key_type, gen_key_size, gen_curve = _parse_key_type_and_params(key_type, key_size, ecdsa_curve)

        # Build certificate configuration
        conf = _build_certificate_config(
            common_name=common_name,
            organization_name=organization_name,
            not_valid_before=not_valid_before,
            not_valid_after=not_valid_after,
            alt_names=alt_names,
            gen_key_type=gen_key_type,
            gen_key_size=gen_key_size,
            gen_curve=gen_curve,
        )
        logger.debug(f"📜🔑🚀 Generation config: {conf}")

        # Generate base certificate and private key
        base, private_key = CertificateBase.create(conf)

        # Create X.509 certificate
        x509_cert = create_x509_certificate(
            base=base,
            private_key=private_key,
            alt_names=alt_names or ["localhost"],
            is_ca=is_ca,
            is_client_cert=is_client_cert,
        )

        if x509_cert is None:
            raise CertificateError("Certificate object (_cert) is None after creation")

        # Serialize to PEM format
        cert_pem, key_pem = _serialize_to_pem(x509_cert, private_key)

        logger.debug("📜🔑✅ Generated cert and key")

        return base, x509_cert, private_key, cert_pem, key_pem

    except Exception as e:
        logger.error(
            f"📜❌ Failed to generate certificate. Error: {type(e).__name__}: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError(f"Failed to initialize certificate. Original error: {type(e).__name__}") from e


def x_generate_certificate__mutmut_13(
    common_name: str,
    organization_name: str,
    validity_days: int,
    key_type: str = DEFAULT_CERTIFICATE_KEY_TYPE,
    key_size: int = DEFAULT_RSA_KEY_SIZE,
    ecdsa_curve: str = DEFAULT_CERTIFICATE_CURVE,
    alt_names: list[str] | None = None,
    is_ca: bool = False,
    is_client_cert: bool = False,
) -> tuple[
    CertificateBase,
    x509.Certificate,
    KeyPair,
    str,
    str,
]:
    """Generate a new certificate with a keypair.

    Returns:
        Tuple of (CertificateBase, X509Certificate, private_key, cert_pem, key_pem)

    """
    try:
        logger.debug("📜🔑🚀 Generating new keypair")

        # Calculate validity period
        now = datetime.now(UTC)
        not_valid_before = now - timedelta(days=1)
        not_valid_after = None

        # Parse and validate key type parameters
        gen_key_type, gen_key_size, gen_curve = _parse_key_type_and_params(key_type, key_size, ecdsa_curve)

        # Build certificate configuration
        conf = _build_certificate_config(
            common_name=common_name,
            organization_name=organization_name,
            not_valid_before=not_valid_before,
            not_valid_after=not_valid_after,
            alt_names=alt_names,
            gen_key_type=gen_key_type,
            gen_key_size=gen_key_size,
            gen_curve=gen_curve,
        )
        logger.debug(f"📜🔑🚀 Generation config: {conf}")

        # Generate base certificate and private key
        base, private_key = CertificateBase.create(conf)

        # Create X.509 certificate
        x509_cert = create_x509_certificate(
            base=base,
            private_key=private_key,
            alt_names=alt_names or ["localhost"],
            is_ca=is_ca,
            is_client_cert=is_client_cert,
        )

        if x509_cert is None:
            raise CertificateError("Certificate object (_cert) is None after creation")

        # Serialize to PEM format
        cert_pem, key_pem = _serialize_to_pem(x509_cert, private_key)

        logger.debug("📜🔑✅ Generated cert and key")

        return base, x509_cert, private_key, cert_pem, key_pem

    except Exception as e:
        logger.error(
            f"📜❌ Failed to generate certificate. Error: {type(e).__name__}: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError(f"Failed to initialize certificate. Original error: {type(e).__name__}") from e


def x_generate_certificate__mutmut_14(
    common_name: str,
    organization_name: str,
    validity_days: int,
    key_type: str = DEFAULT_CERTIFICATE_KEY_TYPE,
    key_size: int = DEFAULT_RSA_KEY_SIZE,
    ecdsa_curve: str = DEFAULT_CERTIFICATE_CURVE,
    alt_names: list[str] | None = None,
    is_ca: bool = False,
    is_client_cert: bool = False,
) -> tuple[
    CertificateBase,
    x509.Certificate,
    KeyPair,
    str,
    str,
]:
    """Generate a new certificate with a keypair.

    Returns:
        Tuple of (CertificateBase, X509Certificate, private_key, cert_pem, key_pem)

    """
    try:
        logger.debug("📜🔑🚀 Generating new keypair")

        # Calculate validity period
        now = datetime.now(UTC)
        not_valid_before = now - timedelta(days=1)
        not_valid_after = now - timedelta(days=validity_days)

        # Parse and validate key type parameters
        gen_key_type, gen_key_size, gen_curve = _parse_key_type_and_params(key_type, key_size, ecdsa_curve)

        # Build certificate configuration
        conf = _build_certificate_config(
            common_name=common_name,
            organization_name=organization_name,
            not_valid_before=not_valid_before,
            not_valid_after=not_valid_after,
            alt_names=alt_names,
            gen_key_type=gen_key_type,
            gen_key_size=gen_key_size,
            gen_curve=gen_curve,
        )
        logger.debug(f"📜🔑🚀 Generation config: {conf}")

        # Generate base certificate and private key
        base, private_key = CertificateBase.create(conf)

        # Create X.509 certificate
        x509_cert = create_x509_certificate(
            base=base,
            private_key=private_key,
            alt_names=alt_names or ["localhost"],
            is_ca=is_ca,
            is_client_cert=is_client_cert,
        )

        if x509_cert is None:
            raise CertificateError("Certificate object (_cert) is None after creation")

        # Serialize to PEM format
        cert_pem, key_pem = _serialize_to_pem(x509_cert, private_key)

        logger.debug("📜🔑✅ Generated cert and key")

        return base, x509_cert, private_key, cert_pem, key_pem

    except Exception as e:
        logger.error(
            f"📜❌ Failed to generate certificate. Error: {type(e).__name__}: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError(f"Failed to initialize certificate. Original error: {type(e).__name__}") from e


def x_generate_certificate__mutmut_15(
    common_name: str,
    organization_name: str,
    validity_days: int,
    key_type: str = DEFAULT_CERTIFICATE_KEY_TYPE,
    key_size: int = DEFAULT_RSA_KEY_SIZE,
    ecdsa_curve: str = DEFAULT_CERTIFICATE_CURVE,
    alt_names: list[str] | None = None,
    is_ca: bool = False,
    is_client_cert: bool = False,
) -> tuple[
    CertificateBase,
    x509.Certificate,
    KeyPair,
    str,
    str,
]:
    """Generate a new certificate with a keypair.

    Returns:
        Tuple of (CertificateBase, X509Certificate, private_key, cert_pem, key_pem)

    """
    try:
        logger.debug("📜🔑🚀 Generating new keypair")

        # Calculate validity period
        now = datetime.now(UTC)
        not_valid_before = now - timedelta(days=1)
        not_valid_after = now + timedelta(days=None)

        # Parse and validate key type parameters
        gen_key_type, gen_key_size, gen_curve = _parse_key_type_and_params(key_type, key_size, ecdsa_curve)

        # Build certificate configuration
        conf = _build_certificate_config(
            common_name=common_name,
            organization_name=organization_name,
            not_valid_before=not_valid_before,
            not_valid_after=not_valid_after,
            alt_names=alt_names,
            gen_key_type=gen_key_type,
            gen_key_size=gen_key_size,
            gen_curve=gen_curve,
        )
        logger.debug(f"📜🔑🚀 Generation config: {conf}")

        # Generate base certificate and private key
        base, private_key = CertificateBase.create(conf)

        # Create X.509 certificate
        x509_cert = create_x509_certificate(
            base=base,
            private_key=private_key,
            alt_names=alt_names or ["localhost"],
            is_ca=is_ca,
            is_client_cert=is_client_cert,
        )

        if x509_cert is None:
            raise CertificateError("Certificate object (_cert) is None after creation")

        # Serialize to PEM format
        cert_pem, key_pem = _serialize_to_pem(x509_cert, private_key)

        logger.debug("📜🔑✅ Generated cert and key")

        return base, x509_cert, private_key, cert_pem, key_pem

    except Exception as e:
        logger.error(
            f"📜❌ Failed to generate certificate. Error: {type(e).__name__}: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError(f"Failed to initialize certificate. Original error: {type(e).__name__}") from e


def x_generate_certificate__mutmut_16(
    common_name: str,
    organization_name: str,
    validity_days: int,
    key_type: str = DEFAULT_CERTIFICATE_KEY_TYPE,
    key_size: int = DEFAULT_RSA_KEY_SIZE,
    ecdsa_curve: str = DEFAULT_CERTIFICATE_CURVE,
    alt_names: list[str] | None = None,
    is_ca: bool = False,
    is_client_cert: bool = False,
) -> tuple[
    CertificateBase,
    x509.Certificate,
    KeyPair,
    str,
    str,
]:
    """Generate a new certificate with a keypair.

    Returns:
        Tuple of (CertificateBase, X509Certificate, private_key, cert_pem, key_pem)

    """
    try:
        logger.debug("📜🔑🚀 Generating new keypair")

        # Calculate validity period
        now = datetime.now(UTC)
        not_valid_before = now - timedelta(days=1)
        not_valid_after = now + timedelta(days=validity_days)

        # Parse and validate key type parameters
        gen_key_type, gen_key_size, gen_curve = None

        # Build certificate configuration
        conf = _build_certificate_config(
            common_name=common_name,
            organization_name=organization_name,
            not_valid_before=not_valid_before,
            not_valid_after=not_valid_after,
            alt_names=alt_names,
            gen_key_type=gen_key_type,
            gen_key_size=gen_key_size,
            gen_curve=gen_curve,
        )
        logger.debug(f"📜🔑🚀 Generation config: {conf}")

        # Generate base certificate and private key
        base, private_key = CertificateBase.create(conf)

        # Create X.509 certificate
        x509_cert = create_x509_certificate(
            base=base,
            private_key=private_key,
            alt_names=alt_names or ["localhost"],
            is_ca=is_ca,
            is_client_cert=is_client_cert,
        )

        if x509_cert is None:
            raise CertificateError("Certificate object (_cert) is None after creation")

        # Serialize to PEM format
        cert_pem, key_pem = _serialize_to_pem(x509_cert, private_key)

        logger.debug("📜🔑✅ Generated cert and key")

        return base, x509_cert, private_key, cert_pem, key_pem

    except Exception as e:
        logger.error(
            f"📜❌ Failed to generate certificate. Error: {type(e).__name__}: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError(f"Failed to initialize certificate. Original error: {type(e).__name__}") from e


def x_generate_certificate__mutmut_17(
    common_name: str,
    organization_name: str,
    validity_days: int,
    key_type: str = DEFAULT_CERTIFICATE_KEY_TYPE,
    key_size: int = DEFAULT_RSA_KEY_SIZE,
    ecdsa_curve: str = DEFAULT_CERTIFICATE_CURVE,
    alt_names: list[str] | None = None,
    is_ca: bool = False,
    is_client_cert: bool = False,
) -> tuple[
    CertificateBase,
    x509.Certificate,
    KeyPair,
    str,
    str,
]:
    """Generate a new certificate with a keypair.

    Returns:
        Tuple of (CertificateBase, X509Certificate, private_key, cert_pem, key_pem)

    """
    try:
        logger.debug("📜🔑🚀 Generating new keypair")

        # Calculate validity period
        now = datetime.now(UTC)
        not_valid_before = now - timedelta(days=1)
        not_valid_after = now + timedelta(days=validity_days)

        # Parse and validate key type parameters
        gen_key_type, gen_key_size, gen_curve = _parse_key_type_and_params(None, key_size, ecdsa_curve)

        # Build certificate configuration
        conf = _build_certificate_config(
            common_name=common_name,
            organization_name=organization_name,
            not_valid_before=not_valid_before,
            not_valid_after=not_valid_after,
            alt_names=alt_names,
            gen_key_type=gen_key_type,
            gen_key_size=gen_key_size,
            gen_curve=gen_curve,
        )
        logger.debug(f"📜🔑🚀 Generation config: {conf}")

        # Generate base certificate and private key
        base, private_key = CertificateBase.create(conf)

        # Create X.509 certificate
        x509_cert = create_x509_certificate(
            base=base,
            private_key=private_key,
            alt_names=alt_names or ["localhost"],
            is_ca=is_ca,
            is_client_cert=is_client_cert,
        )

        if x509_cert is None:
            raise CertificateError("Certificate object (_cert) is None after creation")

        # Serialize to PEM format
        cert_pem, key_pem = _serialize_to_pem(x509_cert, private_key)

        logger.debug("📜🔑✅ Generated cert and key")

        return base, x509_cert, private_key, cert_pem, key_pem

    except Exception as e:
        logger.error(
            f"📜❌ Failed to generate certificate. Error: {type(e).__name__}: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError(f"Failed to initialize certificate. Original error: {type(e).__name__}") from e


def x_generate_certificate__mutmut_18(
    common_name: str,
    organization_name: str,
    validity_days: int,
    key_type: str = DEFAULT_CERTIFICATE_KEY_TYPE,
    key_size: int = DEFAULT_RSA_KEY_SIZE,
    ecdsa_curve: str = DEFAULT_CERTIFICATE_CURVE,
    alt_names: list[str] | None = None,
    is_ca: bool = False,
    is_client_cert: bool = False,
) -> tuple[
    CertificateBase,
    x509.Certificate,
    KeyPair,
    str,
    str,
]:
    """Generate a new certificate with a keypair.

    Returns:
        Tuple of (CertificateBase, X509Certificate, private_key, cert_pem, key_pem)

    """
    try:
        logger.debug("📜🔑🚀 Generating new keypair")

        # Calculate validity period
        now = datetime.now(UTC)
        not_valid_before = now - timedelta(days=1)
        not_valid_after = now + timedelta(days=validity_days)

        # Parse and validate key type parameters
        gen_key_type, gen_key_size, gen_curve = _parse_key_type_and_params(key_type, None, ecdsa_curve)

        # Build certificate configuration
        conf = _build_certificate_config(
            common_name=common_name,
            organization_name=organization_name,
            not_valid_before=not_valid_before,
            not_valid_after=not_valid_after,
            alt_names=alt_names,
            gen_key_type=gen_key_type,
            gen_key_size=gen_key_size,
            gen_curve=gen_curve,
        )
        logger.debug(f"📜🔑🚀 Generation config: {conf}")

        # Generate base certificate and private key
        base, private_key = CertificateBase.create(conf)

        # Create X.509 certificate
        x509_cert = create_x509_certificate(
            base=base,
            private_key=private_key,
            alt_names=alt_names or ["localhost"],
            is_ca=is_ca,
            is_client_cert=is_client_cert,
        )

        if x509_cert is None:
            raise CertificateError("Certificate object (_cert) is None after creation")

        # Serialize to PEM format
        cert_pem, key_pem = _serialize_to_pem(x509_cert, private_key)

        logger.debug("📜🔑✅ Generated cert and key")

        return base, x509_cert, private_key, cert_pem, key_pem

    except Exception as e:
        logger.error(
            f"📜❌ Failed to generate certificate. Error: {type(e).__name__}: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError(f"Failed to initialize certificate. Original error: {type(e).__name__}") from e


def x_generate_certificate__mutmut_19(
    common_name: str,
    organization_name: str,
    validity_days: int,
    key_type: str = DEFAULT_CERTIFICATE_KEY_TYPE,
    key_size: int = DEFAULT_RSA_KEY_SIZE,
    ecdsa_curve: str = DEFAULT_CERTIFICATE_CURVE,
    alt_names: list[str] | None = None,
    is_ca: bool = False,
    is_client_cert: bool = False,
) -> tuple[
    CertificateBase,
    x509.Certificate,
    KeyPair,
    str,
    str,
]:
    """Generate a new certificate with a keypair.

    Returns:
        Tuple of (CertificateBase, X509Certificate, private_key, cert_pem, key_pem)

    """
    try:
        logger.debug("📜🔑🚀 Generating new keypair")

        # Calculate validity period
        now = datetime.now(UTC)
        not_valid_before = now - timedelta(days=1)
        not_valid_after = now + timedelta(days=validity_days)

        # Parse and validate key type parameters
        gen_key_type, gen_key_size, gen_curve = _parse_key_type_and_params(key_type, key_size, None)

        # Build certificate configuration
        conf = _build_certificate_config(
            common_name=common_name,
            organization_name=organization_name,
            not_valid_before=not_valid_before,
            not_valid_after=not_valid_after,
            alt_names=alt_names,
            gen_key_type=gen_key_type,
            gen_key_size=gen_key_size,
            gen_curve=gen_curve,
        )
        logger.debug(f"📜🔑🚀 Generation config: {conf}")

        # Generate base certificate and private key
        base, private_key = CertificateBase.create(conf)

        # Create X.509 certificate
        x509_cert = create_x509_certificate(
            base=base,
            private_key=private_key,
            alt_names=alt_names or ["localhost"],
            is_ca=is_ca,
            is_client_cert=is_client_cert,
        )

        if x509_cert is None:
            raise CertificateError("Certificate object (_cert) is None after creation")

        # Serialize to PEM format
        cert_pem, key_pem = _serialize_to_pem(x509_cert, private_key)

        logger.debug("📜🔑✅ Generated cert and key")

        return base, x509_cert, private_key, cert_pem, key_pem

    except Exception as e:
        logger.error(
            f"📜❌ Failed to generate certificate. Error: {type(e).__name__}: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError(f"Failed to initialize certificate. Original error: {type(e).__name__}") from e


def x_generate_certificate__mutmut_20(
    common_name: str,
    organization_name: str,
    validity_days: int,
    key_type: str = DEFAULT_CERTIFICATE_KEY_TYPE,
    key_size: int = DEFAULT_RSA_KEY_SIZE,
    ecdsa_curve: str = DEFAULT_CERTIFICATE_CURVE,
    alt_names: list[str] | None = None,
    is_ca: bool = False,
    is_client_cert: bool = False,
) -> tuple[
    CertificateBase,
    x509.Certificate,
    KeyPair,
    str,
    str,
]:
    """Generate a new certificate with a keypair.

    Returns:
        Tuple of (CertificateBase, X509Certificate, private_key, cert_pem, key_pem)

    """
    try:
        logger.debug("📜🔑🚀 Generating new keypair")

        # Calculate validity period
        now = datetime.now(UTC)
        not_valid_before = now - timedelta(days=1)
        not_valid_after = now + timedelta(days=validity_days)

        # Parse and validate key type parameters
        gen_key_type, gen_key_size, gen_curve = _parse_key_type_and_params(key_size, ecdsa_curve)

        # Build certificate configuration
        conf = _build_certificate_config(
            common_name=common_name,
            organization_name=organization_name,
            not_valid_before=not_valid_before,
            not_valid_after=not_valid_after,
            alt_names=alt_names,
            gen_key_type=gen_key_type,
            gen_key_size=gen_key_size,
            gen_curve=gen_curve,
        )
        logger.debug(f"📜🔑🚀 Generation config: {conf}")

        # Generate base certificate and private key
        base, private_key = CertificateBase.create(conf)

        # Create X.509 certificate
        x509_cert = create_x509_certificate(
            base=base,
            private_key=private_key,
            alt_names=alt_names or ["localhost"],
            is_ca=is_ca,
            is_client_cert=is_client_cert,
        )

        if x509_cert is None:
            raise CertificateError("Certificate object (_cert) is None after creation")

        # Serialize to PEM format
        cert_pem, key_pem = _serialize_to_pem(x509_cert, private_key)

        logger.debug("📜🔑✅ Generated cert and key")

        return base, x509_cert, private_key, cert_pem, key_pem

    except Exception as e:
        logger.error(
            f"📜❌ Failed to generate certificate. Error: {type(e).__name__}: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError(f"Failed to initialize certificate. Original error: {type(e).__name__}") from e


def x_generate_certificate__mutmut_21(
    common_name: str,
    organization_name: str,
    validity_days: int,
    key_type: str = DEFAULT_CERTIFICATE_KEY_TYPE,
    key_size: int = DEFAULT_RSA_KEY_SIZE,
    ecdsa_curve: str = DEFAULT_CERTIFICATE_CURVE,
    alt_names: list[str] | None = None,
    is_ca: bool = False,
    is_client_cert: bool = False,
) -> tuple[
    CertificateBase,
    x509.Certificate,
    KeyPair,
    str,
    str,
]:
    """Generate a new certificate with a keypair.

    Returns:
        Tuple of (CertificateBase, X509Certificate, private_key, cert_pem, key_pem)

    """
    try:
        logger.debug("📜🔑🚀 Generating new keypair")

        # Calculate validity period
        now = datetime.now(UTC)
        not_valid_before = now - timedelta(days=1)
        not_valid_after = now + timedelta(days=validity_days)

        # Parse and validate key type parameters
        gen_key_type, gen_key_size, gen_curve = _parse_key_type_and_params(key_type, ecdsa_curve)

        # Build certificate configuration
        conf = _build_certificate_config(
            common_name=common_name,
            organization_name=organization_name,
            not_valid_before=not_valid_before,
            not_valid_after=not_valid_after,
            alt_names=alt_names,
            gen_key_type=gen_key_type,
            gen_key_size=gen_key_size,
            gen_curve=gen_curve,
        )
        logger.debug(f"📜🔑🚀 Generation config: {conf}")

        # Generate base certificate and private key
        base, private_key = CertificateBase.create(conf)

        # Create X.509 certificate
        x509_cert = create_x509_certificate(
            base=base,
            private_key=private_key,
            alt_names=alt_names or ["localhost"],
            is_ca=is_ca,
            is_client_cert=is_client_cert,
        )

        if x509_cert is None:
            raise CertificateError("Certificate object (_cert) is None after creation")

        # Serialize to PEM format
        cert_pem, key_pem = _serialize_to_pem(x509_cert, private_key)

        logger.debug("📜🔑✅ Generated cert and key")

        return base, x509_cert, private_key, cert_pem, key_pem

    except Exception as e:
        logger.error(
            f"📜❌ Failed to generate certificate. Error: {type(e).__name__}: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError(f"Failed to initialize certificate. Original error: {type(e).__name__}") from e


def x_generate_certificate__mutmut_22(
    common_name: str,
    organization_name: str,
    validity_days: int,
    key_type: str = DEFAULT_CERTIFICATE_KEY_TYPE,
    key_size: int = DEFAULT_RSA_KEY_SIZE,
    ecdsa_curve: str = DEFAULT_CERTIFICATE_CURVE,
    alt_names: list[str] | None = None,
    is_ca: bool = False,
    is_client_cert: bool = False,
) -> tuple[
    CertificateBase,
    x509.Certificate,
    KeyPair,
    str,
    str,
]:
    """Generate a new certificate with a keypair.

    Returns:
        Tuple of (CertificateBase, X509Certificate, private_key, cert_pem, key_pem)

    """
    try:
        logger.debug("📜🔑🚀 Generating new keypair")

        # Calculate validity period
        now = datetime.now(UTC)
        not_valid_before = now - timedelta(days=1)
        not_valid_after = now + timedelta(days=validity_days)

        # Parse and validate key type parameters
        gen_key_type, gen_key_size, gen_curve = _parse_key_type_and_params(
            key_type,
            key_size,
        )

        # Build certificate configuration
        conf = _build_certificate_config(
            common_name=common_name,
            organization_name=organization_name,
            not_valid_before=not_valid_before,
            not_valid_after=not_valid_after,
            alt_names=alt_names,
            gen_key_type=gen_key_type,
            gen_key_size=gen_key_size,
            gen_curve=gen_curve,
        )
        logger.debug(f"📜🔑🚀 Generation config: {conf}")

        # Generate base certificate and private key
        base, private_key = CertificateBase.create(conf)

        # Create X.509 certificate
        x509_cert = create_x509_certificate(
            base=base,
            private_key=private_key,
            alt_names=alt_names or ["localhost"],
            is_ca=is_ca,
            is_client_cert=is_client_cert,
        )

        if x509_cert is None:
            raise CertificateError("Certificate object (_cert) is None after creation")

        # Serialize to PEM format
        cert_pem, key_pem = _serialize_to_pem(x509_cert, private_key)

        logger.debug("📜🔑✅ Generated cert and key")

        return base, x509_cert, private_key, cert_pem, key_pem

    except Exception as e:
        logger.error(
            f"📜❌ Failed to generate certificate. Error: {type(e).__name__}: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError(f"Failed to initialize certificate. Original error: {type(e).__name__}") from e


def x_generate_certificate__mutmut_23(
    common_name: str,
    organization_name: str,
    validity_days: int,
    key_type: str = DEFAULT_CERTIFICATE_KEY_TYPE,
    key_size: int = DEFAULT_RSA_KEY_SIZE,
    ecdsa_curve: str = DEFAULT_CERTIFICATE_CURVE,
    alt_names: list[str] | None = None,
    is_ca: bool = False,
    is_client_cert: bool = False,
) -> tuple[
    CertificateBase,
    x509.Certificate,
    KeyPair,
    str,
    str,
]:
    """Generate a new certificate with a keypair.

    Returns:
        Tuple of (CertificateBase, X509Certificate, private_key, cert_pem, key_pem)

    """
    try:
        logger.debug("📜🔑🚀 Generating new keypair")

        # Calculate validity period
        now = datetime.now(UTC)
        not_valid_before = now - timedelta(days=1)
        not_valid_after = now + timedelta(days=validity_days)

        # Parse and validate key type parameters
        gen_key_type, gen_key_size, gen_curve = _parse_key_type_and_params(key_type, key_size, ecdsa_curve)

        # Build certificate configuration
        conf = None
        logger.debug(f"📜🔑🚀 Generation config: {conf}")

        # Generate base certificate and private key
        base, private_key = CertificateBase.create(conf)

        # Create X.509 certificate
        x509_cert = create_x509_certificate(
            base=base,
            private_key=private_key,
            alt_names=alt_names or ["localhost"],
            is_ca=is_ca,
            is_client_cert=is_client_cert,
        )

        if x509_cert is None:
            raise CertificateError("Certificate object (_cert) is None after creation")

        # Serialize to PEM format
        cert_pem, key_pem = _serialize_to_pem(x509_cert, private_key)

        logger.debug("📜🔑✅ Generated cert and key")

        return base, x509_cert, private_key, cert_pem, key_pem

    except Exception as e:
        logger.error(
            f"📜❌ Failed to generate certificate. Error: {type(e).__name__}: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError(f"Failed to initialize certificate. Original error: {type(e).__name__}") from e


def x_generate_certificate__mutmut_24(
    common_name: str,
    organization_name: str,
    validity_days: int,
    key_type: str = DEFAULT_CERTIFICATE_KEY_TYPE,
    key_size: int = DEFAULT_RSA_KEY_SIZE,
    ecdsa_curve: str = DEFAULT_CERTIFICATE_CURVE,
    alt_names: list[str] | None = None,
    is_ca: bool = False,
    is_client_cert: bool = False,
) -> tuple[
    CertificateBase,
    x509.Certificate,
    KeyPair,
    str,
    str,
]:
    """Generate a new certificate with a keypair.

    Returns:
        Tuple of (CertificateBase, X509Certificate, private_key, cert_pem, key_pem)

    """
    try:
        logger.debug("📜🔑🚀 Generating new keypair")

        # Calculate validity period
        now = datetime.now(UTC)
        not_valid_before = now - timedelta(days=1)
        not_valid_after = now + timedelta(days=validity_days)

        # Parse and validate key type parameters
        gen_key_type, gen_key_size, gen_curve = _parse_key_type_and_params(key_type, key_size, ecdsa_curve)

        # Build certificate configuration
        conf = _build_certificate_config(
            common_name=None,
            organization_name=organization_name,
            not_valid_before=not_valid_before,
            not_valid_after=not_valid_after,
            alt_names=alt_names,
            gen_key_type=gen_key_type,
            gen_key_size=gen_key_size,
            gen_curve=gen_curve,
        )
        logger.debug(f"📜🔑🚀 Generation config: {conf}")

        # Generate base certificate and private key
        base, private_key = CertificateBase.create(conf)

        # Create X.509 certificate
        x509_cert = create_x509_certificate(
            base=base,
            private_key=private_key,
            alt_names=alt_names or ["localhost"],
            is_ca=is_ca,
            is_client_cert=is_client_cert,
        )

        if x509_cert is None:
            raise CertificateError("Certificate object (_cert) is None after creation")

        # Serialize to PEM format
        cert_pem, key_pem = _serialize_to_pem(x509_cert, private_key)

        logger.debug("📜🔑✅ Generated cert and key")

        return base, x509_cert, private_key, cert_pem, key_pem

    except Exception as e:
        logger.error(
            f"📜❌ Failed to generate certificate. Error: {type(e).__name__}: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError(f"Failed to initialize certificate. Original error: {type(e).__name__}") from e


def x_generate_certificate__mutmut_25(
    common_name: str,
    organization_name: str,
    validity_days: int,
    key_type: str = DEFAULT_CERTIFICATE_KEY_TYPE,
    key_size: int = DEFAULT_RSA_KEY_SIZE,
    ecdsa_curve: str = DEFAULT_CERTIFICATE_CURVE,
    alt_names: list[str] | None = None,
    is_ca: bool = False,
    is_client_cert: bool = False,
) -> tuple[
    CertificateBase,
    x509.Certificate,
    KeyPair,
    str,
    str,
]:
    """Generate a new certificate with a keypair.

    Returns:
        Tuple of (CertificateBase, X509Certificate, private_key, cert_pem, key_pem)

    """
    try:
        logger.debug("📜🔑🚀 Generating new keypair")

        # Calculate validity period
        now = datetime.now(UTC)
        not_valid_before = now - timedelta(days=1)
        not_valid_after = now + timedelta(days=validity_days)

        # Parse and validate key type parameters
        gen_key_type, gen_key_size, gen_curve = _parse_key_type_and_params(key_type, key_size, ecdsa_curve)

        # Build certificate configuration
        conf = _build_certificate_config(
            common_name=common_name,
            organization_name=None,
            not_valid_before=not_valid_before,
            not_valid_after=not_valid_after,
            alt_names=alt_names,
            gen_key_type=gen_key_type,
            gen_key_size=gen_key_size,
            gen_curve=gen_curve,
        )
        logger.debug(f"📜🔑🚀 Generation config: {conf}")

        # Generate base certificate and private key
        base, private_key = CertificateBase.create(conf)

        # Create X.509 certificate
        x509_cert = create_x509_certificate(
            base=base,
            private_key=private_key,
            alt_names=alt_names or ["localhost"],
            is_ca=is_ca,
            is_client_cert=is_client_cert,
        )

        if x509_cert is None:
            raise CertificateError("Certificate object (_cert) is None after creation")

        # Serialize to PEM format
        cert_pem, key_pem = _serialize_to_pem(x509_cert, private_key)

        logger.debug("📜🔑✅ Generated cert and key")

        return base, x509_cert, private_key, cert_pem, key_pem

    except Exception as e:
        logger.error(
            f"📜❌ Failed to generate certificate. Error: {type(e).__name__}: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError(f"Failed to initialize certificate. Original error: {type(e).__name__}") from e


def x_generate_certificate__mutmut_26(
    common_name: str,
    organization_name: str,
    validity_days: int,
    key_type: str = DEFAULT_CERTIFICATE_KEY_TYPE,
    key_size: int = DEFAULT_RSA_KEY_SIZE,
    ecdsa_curve: str = DEFAULT_CERTIFICATE_CURVE,
    alt_names: list[str] | None = None,
    is_ca: bool = False,
    is_client_cert: bool = False,
) -> tuple[
    CertificateBase,
    x509.Certificate,
    KeyPair,
    str,
    str,
]:
    """Generate a new certificate with a keypair.

    Returns:
        Tuple of (CertificateBase, X509Certificate, private_key, cert_pem, key_pem)

    """
    try:
        logger.debug("📜🔑🚀 Generating new keypair")

        # Calculate validity period
        now = datetime.now(UTC)
        not_valid_before = now - timedelta(days=1)
        not_valid_after = now + timedelta(days=validity_days)

        # Parse and validate key type parameters
        gen_key_type, gen_key_size, gen_curve = _parse_key_type_and_params(key_type, key_size, ecdsa_curve)

        # Build certificate configuration
        conf = _build_certificate_config(
            common_name=common_name,
            organization_name=organization_name,
            not_valid_before=None,
            not_valid_after=not_valid_after,
            alt_names=alt_names,
            gen_key_type=gen_key_type,
            gen_key_size=gen_key_size,
            gen_curve=gen_curve,
        )
        logger.debug(f"📜🔑🚀 Generation config: {conf}")

        # Generate base certificate and private key
        base, private_key = CertificateBase.create(conf)

        # Create X.509 certificate
        x509_cert = create_x509_certificate(
            base=base,
            private_key=private_key,
            alt_names=alt_names or ["localhost"],
            is_ca=is_ca,
            is_client_cert=is_client_cert,
        )

        if x509_cert is None:
            raise CertificateError("Certificate object (_cert) is None after creation")

        # Serialize to PEM format
        cert_pem, key_pem = _serialize_to_pem(x509_cert, private_key)

        logger.debug("📜🔑✅ Generated cert and key")

        return base, x509_cert, private_key, cert_pem, key_pem

    except Exception as e:
        logger.error(
            f"📜❌ Failed to generate certificate. Error: {type(e).__name__}: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError(f"Failed to initialize certificate. Original error: {type(e).__name__}") from e


def x_generate_certificate__mutmut_27(
    common_name: str,
    organization_name: str,
    validity_days: int,
    key_type: str = DEFAULT_CERTIFICATE_KEY_TYPE,
    key_size: int = DEFAULT_RSA_KEY_SIZE,
    ecdsa_curve: str = DEFAULT_CERTIFICATE_CURVE,
    alt_names: list[str] | None = None,
    is_ca: bool = False,
    is_client_cert: bool = False,
) -> tuple[
    CertificateBase,
    x509.Certificate,
    KeyPair,
    str,
    str,
]:
    """Generate a new certificate with a keypair.

    Returns:
        Tuple of (CertificateBase, X509Certificate, private_key, cert_pem, key_pem)

    """
    try:
        logger.debug("📜🔑🚀 Generating new keypair")

        # Calculate validity period
        now = datetime.now(UTC)
        not_valid_before = now - timedelta(days=1)
        not_valid_after = now + timedelta(days=validity_days)

        # Parse and validate key type parameters
        gen_key_type, gen_key_size, gen_curve = _parse_key_type_and_params(key_type, key_size, ecdsa_curve)

        # Build certificate configuration
        conf = _build_certificate_config(
            common_name=common_name,
            organization_name=organization_name,
            not_valid_before=not_valid_before,
            not_valid_after=None,
            alt_names=alt_names,
            gen_key_type=gen_key_type,
            gen_key_size=gen_key_size,
            gen_curve=gen_curve,
        )
        logger.debug(f"📜🔑🚀 Generation config: {conf}")

        # Generate base certificate and private key
        base, private_key = CertificateBase.create(conf)

        # Create X.509 certificate
        x509_cert = create_x509_certificate(
            base=base,
            private_key=private_key,
            alt_names=alt_names or ["localhost"],
            is_ca=is_ca,
            is_client_cert=is_client_cert,
        )

        if x509_cert is None:
            raise CertificateError("Certificate object (_cert) is None after creation")

        # Serialize to PEM format
        cert_pem, key_pem = _serialize_to_pem(x509_cert, private_key)

        logger.debug("📜🔑✅ Generated cert and key")

        return base, x509_cert, private_key, cert_pem, key_pem

    except Exception as e:
        logger.error(
            f"📜❌ Failed to generate certificate. Error: {type(e).__name__}: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError(f"Failed to initialize certificate. Original error: {type(e).__name__}") from e


def x_generate_certificate__mutmut_28(
    common_name: str,
    organization_name: str,
    validity_days: int,
    key_type: str = DEFAULT_CERTIFICATE_KEY_TYPE,
    key_size: int = DEFAULT_RSA_KEY_SIZE,
    ecdsa_curve: str = DEFAULT_CERTIFICATE_CURVE,
    alt_names: list[str] | None = None,
    is_ca: bool = False,
    is_client_cert: bool = False,
) -> tuple[
    CertificateBase,
    x509.Certificate,
    KeyPair,
    str,
    str,
]:
    """Generate a new certificate with a keypair.

    Returns:
        Tuple of (CertificateBase, X509Certificate, private_key, cert_pem, key_pem)

    """
    try:
        logger.debug("📜🔑🚀 Generating new keypair")

        # Calculate validity period
        now = datetime.now(UTC)
        not_valid_before = now - timedelta(days=1)
        not_valid_after = now + timedelta(days=validity_days)

        # Parse and validate key type parameters
        gen_key_type, gen_key_size, gen_curve = _parse_key_type_and_params(key_type, key_size, ecdsa_curve)

        # Build certificate configuration
        conf = _build_certificate_config(
            common_name=common_name,
            organization_name=organization_name,
            not_valid_before=not_valid_before,
            not_valid_after=not_valid_after,
            alt_names=None,
            gen_key_type=gen_key_type,
            gen_key_size=gen_key_size,
            gen_curve=gen_curve,
        )
        logger.debug(f"📜🔑🚀 Generation config: {conf}")

        # Generate base certificate and private key
        base, private_key = CertificateBase.create(conf)

        # Create X.509 certificate
        x509_cert = create_x509_certificate(
            base=base,
            private_key=private_key,
            alt_names=alt_names or ["localhost"],
            is_ca=is_ca,
            is_client_cert=is_client_cert,
        )

        if x509_cert is None:
            raise CertificateError("Certificate object (_cert) is None after creation")

        # Serialize to PEM format
        cert_pem, key_pem = _serialize_to_pem(x509_cert, private_key)

        logger.debug("📜🔑✅ Generated cert and key")

        return base, x509_cert, private_key, cert_pem, key_pem

    except Exception as e:
        logger.error(
            f"📜❌ Failed to generate certificate. Error: {type(e).__name__}: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError(f"Failed to initialize certificate. Original error: {type(e).__name__}") from e


def x_generate_certificate__mutmut_29(
    common_name: str,
    organization_name: str,
    validity_days: int,
    key_type: str = DEFAULT_CERTIFICATE_KEY_TYPE,
    key_size: int = DEFAULT_RSA_KEY_SIZE,
    ecdsa_curve: str = DEFAULT_CERTIFICATE_CURVE,
    alt_names: list[str] | None = None,
    is_ca: bool = False,
    is_client_cert: bool = False,
) -> tuple[
    CertificateBase,
    x509.Certificate,
    KeyPair,
    str,
    str,
]:
    """Generate a new certificate with a keypair.

    Returns:
        Tuple of (CertificateBase, X509Certificate, private_key, cert_pem, key_pem)

    """
    try:
        logger.debug("📜🔑🚀 Generating new keypair")

        # Calculate validity period
        now = datetime.now(UTC)
        not_valid_before = now - timedelta(days=1)
        not_valid_after = now + timedelta(days=validity_days)

        # Parse and validate key type parameters
        gen_key_type, gen_key_size, gen_curve = _parse_key_type_and_params(key_type, key_size, ecdsa_curve)

        # Build certificate configuration
        conf = _build_certificate_config(
            common_name=common_name,
            organization_name=organization_name,
            not_valid_before=not_valid_before,
            not_valid_after=not_valid_after,
            alt_names=alt_names,
            gen_key_type=None,
            gen_key_size=gen_key_size,
            gen_curve=gen_curve,
        )
        logger.debug(f"📜🔑🚀 Generation config: {conf}")

        # Generate base certificate and private key
        base, private_key = CertificateBase.create(conf)

        # Create X.509 certificate
        x509_cert = create_x509_certificate(
            base=base,
            private_key=private_key,
            alt_names=alt_names or ["localhost"],
            is_ca=is_ca,
            is_client_cert=is_client_cert,
        )

        if x509_cert is None:
            raise CertificateError("Certificate object (_cert) is None after creation")

        # Serialize to PEM format
        cert_pem, key_pem = _serialize_to_pem(x509_cert, private_key)

        logger.debug("📜🔑✅ Generated cert and key")

        return base, x509_cert, private_key, cert_pem, key_pem

    except Exception as e:
        logger.error(
            f"📜❌ Failed to generate certificate. Error: {type(e).__name__}: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError(f"Failed to initialize certificate. Original error: {type(e).__name__}") from e


def x_generate_certificate__mutmut_30(
    common_name: str,
    organization_name: str,
    validity_days: int,
    key_type: str = DEFAULT_CERTIFICATE_KEY_TYPE,
    key_size: int = DEFAULT_RSA_KEY_SIZE,
    ecdsa_curve: str = DEFAULT_CERTIFICATE_CURVE,
    alt_names: list[str] | None = None,
    is_ca: bool = False,
    is_client_cert: bool = False,
) -> tuple[
    CertificateBase,
    x509.Certificate,
    KeyPair,
    str,
    str,
]:
    """Generate a new certificate with a keypair.

    Returns:
        Tuple of (CertificateBase, X509Certificate, private_key, cert_pem, key_pem)

    """
    try:
        logger.debug("📜🔑🚀 Generating new keypair")

        # Calculate validity period
        now = datetime.now(UTC)
        not_valid_before = now - timedelta(days=1)
        not_valid_after = now + timedelta(days=validity_days)

        # Parse and validate key type parameters
        gen_key_type, gen_key_size, gen_curve = _parse_key_type_and_params(key_type, key_size, ecdsa_curve)

        # Build certificate configuration
        conf = _build_certificate_config(
            common_name=common_name,
            organization_name=organization_name,
            not_valid_before=not_valid_before,
            not_valid_after=not_valid_after,
            alt_names=alt_names,
            gen_key_type=gen_key_type,
            gen_key_size=None,
            gen_curve=gen_curve,
        )
        logger.debug(f"📜🔑🚀 Generation config: {conf}")

        # Generate base certificate and private key
        base, private_key = CertificateBase.create(conf)

        # Create X.509 certificate
        x509_cert = create_x509_certificate(
            base=base,
            private_key=private_key,
            alt_names=alt_names or ["localhost"],
            is_ca=is_ca,
            is_client_cert=is_client_cert,
        )

        if x509_cert is None:
            raise CertificateError("Certificate object (_cert) is None after creation")

        # Serialize to PEM format
        cert_pem, key_pem = _serialize_to_pem(x509_cert, private_key)

        logger.debug("📜🔑✅ Generated cert and key")

        return base, x509_cert, private_key, cert_pem, key_pem

    except Exception as e:
        logger.error(
            f"📜❌ Failed to generate certificate. Error: {type(e).__name__}: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError(f"Failed to initialize certificate. Original error: {type(e).__name__}") from e


def x_generate_certificate__mutmut_31(
    common_name: str,
    organization_name: str,
    validity_days: int,
    key_type: str = DEFAULT_CERTIFICATE_KEY_TYPE,
    key_size: int = DEFAULT_RSA_KEY_SIZE,
    ecdsa_curve: str = DEFAULT_CERTIFICATE_CURVE,
    alt_names: list[str] | None = None,
    is_ca: bool = False,
    is_client_cert: bool = False,
) -> tuple[
    CertificateBase,
    x509.Certificate,
    KeyPair,
    str,
    str,
]:
    """Generate a new certificate with a keypair.

    Returns:
        Tuple of (CertificateBase, X509Certificate, private_key, cert_pem, key_pem)

    """
    try:
        logger.debug("📜🔑🚀 Generating new keypair")

        # Calculate validity period
        now = datetime.now(UTC)
        not_valid_before = now - timedelta(days=1)
        not_valid_after = now + timedelta(days=validity_days)

        # Parse and validate key type parameters
        gen_key_type, gen_key_size, gen_curve = _parse_key_type_and_params(key_type, key_size, ecdsa_curve)

        # Build certificate configuration
        conf = _build_certificate_config(
            common_name=common_name,
            organization_name=organization_name,
            not_valid_before=not_valid_before,
            not_valid_after=not_valid_after,
            alt_names=alt_names,
            gen_key_type=gen_key_type,
            gen_key_size=gen_key_size,
            gen_curve=None,
        )
        logger.debug(f"📜🔑🚀 Generation config: {conf}")

        # Generate base certificate and private key
        base, private_key = CertificateBase.create(conf)

        # Create X.509 certificate
        x509_cert = create_x509_certificate(
            base=base,
            private_key=private_key,
            alt_names=alt_names or ["localhost"],
            is_ca=is_ca,
            is_client_cert=is_client_cert,
        )

        if x509_cert is None:
            raise CertificateError("Certificate object (_cert) is None after creation")

        # Serialize to PEM format
        cert_pem, key_pem = _serialize_to_pem(x509_cert, private_key)

        logger.debug("📜🔑✅ Generated cert and key")

        return base, x509_cert, private_key, cert_pem, key_pem

    except Exception as e:
        logger.error(
            f"📜❌ Failed to generate certificate. Error: {type(e).__name__}: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError(f"Failed to initialize certificate. Original error: {type(e).__name__}") from e


def x_generate_certificate__mutmut_32(
    common_name: str,
    organization_name: str,
    validity_days: int,
    key_type: str = DEFAULT_CERTIFICATE_KEY_TYPE,
    key_size: int = DEFAULT_RSA_KEY_SIZE,
    ecdsa_curve: str = DEFAULT_CERTIFICATE_CURVE,
    alt_names: list[str] | None = None,
    is_ca: bool = False,
    is_client_cert: bool = False,
) -> tuple[
    CertificateBase,
    x509.Certificate,
    KeyPair,
    str,
    str,
]:
    """Generate a new certificate with a keypair.

    Returns:
        Tuple of (CertificateBase, X509Certificate, private_key, cert_pem, key_pem)

    """
    try:
        logger.debug("📜🔑🚀 Generating new keypair")

        # Calculate validity period
        now = datetime.now(UTC)
        not_valid_before = now - timedelta(days=1)
        not_valid_after = now + timedelta(days=validity_days)

        # Parse and validate key type parameters
        gen_key_type, gen_key_size, gen_curve = _parse_key_type_and_params(key_type, key_size, ecdsa_curve)

        # Build certificate configuration
        conf = _build_certificate_config(
            organization_name=organization_name,
            not_valid_before=not_valid_before,
            not_valid_after=not_valid_after,
            alt_names=alt_names,
            gen_key_type=gen_key_type,
            gen_key_size=gen_key_size,
            gen_curve=gen_curve,
        )
        logger.debug(f"📜🔑🚀 Generation config: {conf}")

        # Generate base certificate and private key
        base, private_key = CertificateBase.create(conf)

        # Create X.509 certificate
        x509_cert = create_x509_certificate(
            base=base,
            private_key=private_key,
            alt_names=alt_names or ["localhost"],
            is_ca=is_ca,
            is_client_cert=is_client_cert,
        )

        if x509_cert is None:
            raise CertificateError("Certificate object (_cert) is None after creation")

        # Serialize to PEM format
        cert_pem, key_pem = _serialize_to_pem(x509_cert, private_key)

        logger.debug("📜🔑✅ Generated cert and key")

        return base, x509_cert, private_key, cert_pem, key_pem

    except Exception as e:
        logger.error(
            f"📜❌ Failed to generate certificate. Error: {type(e).__name__}: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError(f"Failed to initialize certificate. Original error: {type(e).__name__}") from e


def x_generate_certificate__mutmut_33(
    common_name: str,
    organization_name: str,
    validity_days: int,
    key_type: str = DEFAULT_CERTIFICATE_KEY_TYPE,
    key_size: int = DEFAULT_RSA_KEY_SIZE,
    ecdsa_curve: str = DEFAULT_CERTIFICATE_CURVE,
    alt_names: list[str] | None = None,
    is_ca: bool = False,
    is_client_cert: bool = False,
) -> tuple[
    CertificateBase,
    x509.Certificate,
    KeyPair,
    str,
    str,
]:
    """Generate a new certificate with a keypair.

    Returns:
        Tuple of (CertificateBase, X509Certificate, private_key, cert_pem, key_pem)

    """
    try:
        logger.debug("📜🔑🚀 Generating new keypair")

        # Calculate validity period
        now = datetime.now(UTC)
        not_valid_before = now - timedelta(days=1)
        not_valid_after = now + timedelta(days=validity_days)

        # Parse and validate key type parameters
        gen_key_type, gen_key_size, gen_curve = _parse_key_type_and_params(key_type, key_size, ecdsa_curve)

        # Build certificate configuration
        conf = _build_certificate_config(
            common_name=common_name,
            not_valid_before=not_valid_before,
            not_valid_after=not_valid_after,
            alt_names=alt_names,
            gen_key_type=gen_key_type,
            gen_key_size=gen_key_size,
            gen_curve=gen_curve,
        )
        logger.debug(f"📜🔑🚀 Generation config: {conf}")

        # Generate base certificate and private key
        base, private_key = CertificateBase.create(conf)

        # Create X.509 certificate
        x509_cert = create_x509_certificate(
            base=base,
            private_key=private_key,
            alt_names=alt_names or ["localhost"],
            is_ca=is_ca,
            is_client_cert=is_client_cert,
        )

        if x509_cert is None:
            raise CertificateError("Certificate object (_cert) is None after creation")

        # Serialize to PEM format
        cert_pem, key_pem = _serialize_to_pem(x509_cert, private_key)

        logger.debug("📜🔑✅ Generated cert and key")

        return base, x509_cert, private_key, cert_pem, key_pem

    except Exception as e:
        logger.error(
            f"📜❌ Failed to generate certificate. Error: {type(e).__name__}: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError(f"Failed to initialize certificate. Original error: {type(e).__name__}") from e


def x_generate_certificate__mutmut_34(
    common_name: str,
    organization_name: str,
    validity_days: int,
    key_type: str = DEFAULT_CERTIFICATE_KEY_TYPE,
    key_size: int = DEFAULT_RSA_KEY_SIZE,
    ecdsa_curve: str = DEFAULT_CERTIFICATE_CURVE,
    alt_names: list[str] | None = None,
    is_ca: bool = False,
    is_client_cert: bool = False,
) -> tuple[
    CertificateBase,
    x509.Certificate,
    KeyPair,
    str,
    str,
]:
    """Generate a new certificate with a keypair.

    Returns:
        Tuple of (CertificateBase, X509Certificate, private_key, cert_pem, key_pem)

    """
    try:
        logger.debug("📜🔑🚀 Generating new keypair")

        # Calculate validity period
        now = datetime.now(UTC)
        not_valid_before = now - timedelta(days=1)
        not_valid_after = now + timedelta(days=validity_days)

        # Parse and validate key type parameters
        gen_key_type, gen_key_size, gen_curve = _parse_key_type_and_params(key_type, key_size, ecdsa_curve)

        # Build certificate configuration
        conf = _build_certificate_config(
            common_name=common_name,
            organization_name=organization_name,
            not_valid_after=not_valid_after,
            alt_names=alt_names,
            gen_key_type=gen_key_type,
            gen_key_size=gen_key_size,
            gen_curve=gen_curve,
        )
        logger.debug(f"📜🔑🚀 Generation config: {conf}")

        # Generate base certificate and private key
        base, private_key = CertificateBase.create(conf)

        # Create X.509 certificate
        x509_cert = create_x509_certificate(
            base=base,
            private_key=private_key,
            alt_names=alt_names or ["localhost"],
            is_ca=is_ca,
            is_client_cert=is_client_cert,
        )

        if x509_cert is None:
            raise CertificateError("Certificate object (_cert) is None after creation")

        # Serialize to PEM format
        cert_pem, key_pem = _serialize_to_pem(x509_cert, private_key)

        logger.debug("📜🔑✅ Generated cert and key")

        return base, x509_cert, private_key, cert_pem, key_pem

    except Exception as e:
        logger.error(
            f"📜❌ Failed to generate certificate. Error: {type(e).__name__}: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError(f"Failed to initialize certificate. Original error: {type(e).__name__}") from e


def x_generate_certificate__mutmut_35(
    common_name: str,
    organization_name: str,
    validity_days: int,
    key_type: str = DEFAULT_CERTIFICATE_KEY_TYPE,
    key_size: int = DEFAULT_RSA_KEY_SIZE,
    ecdsa_curve: str = DEFAULT_CERTIFICATE_CURVE,
    alt_names: list[str] | None = None,
    is_ca: bool = False,
    is_client_cert: bool = False,
) -> tuple[
    CertificateBase,
    x509.Certificate,
    KeyPair,
    str,
    str,
]:
    """Generate a new certificate with a keypair.

    Returns:
        Tuple of (CertificateBase, X509Certificate, private_key, cert_pem, key_pem)

    """
    try:
        logger.debug("📜🔑🚀 Generating new keypair")

        # Calculate validity period
        now = datetime.now(UTC)
        not_valid_before = now - timedelta(days=1)
        not_valid_after = now + timedelta(days=validity_days)

        # Parse and validate key type parameters
        gen_key_type, gen_key_size, gen_curve = _parse_key_type_and_params(key_type, key_size, ecdsa_curve)

        # Build certificate configuration
        conf = _build_certificate_config(
            common_name=common_name,
            organization_name=organization_name,
            not_valid_before=not_valid_before,
            alt_names=alt_names,
            gen_key_type=gen_key_type,
            gen_key_size=gen_key_size,
            gen_curve=gen_curve,
        )
        logger.debug(f"📜🔑🚀 Generation config: {conf}")

        # Generate base certificate and private key
        base, private_key = CertificateBase.create(conf)

        # Create X.509 certificate
        x509_cert = create_x509_certificate(
            base=base,
            private_key=private_key,
            alt_names=alt_names or ["localhost"],
            is_ca=is_ca,
            is_client_cert=is_client_cert,
        )

        if x509_cert is None:
            raise CertificateError("Certificate object (_cert) is None after creation")

        # Serialize to PEM format
        cert_pem, key_pem = _serialize_to_pem(x509_cert, private_key)

        logger.debug("📜🔑✅ Generated cert and key")

        return base, x509_cert, private_key, cert_pem, key_pem

    except Exception as e:
        logger.error(
            f"📜❌ Failed to generate certificate. Error: {type(e).__name__}: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError(f"Failed to initialize certificate. Original error: {type(e).__name__}") from e


def x_generate_certificate__mutmut_36(
    common_name: str,
    organization_name: str,
    validity_days: int,
    key_type: str = DEFAULT_CERTIFICATE_KEY_TYPE,
    key_size: int = DEFAULT_RSA_KEY_SIZE,
    ecdsa_curve: str = DEFAULT_CERTIFICATE_CURVE,
    alt_names: list[str] | None = None,
    is_ca: bool = False,
    is_client_cert: bool = False,
) -> tuple[
    CertificateBase,
    x509.Certificate,
    KeyPair,
    str,
    str,
]:
    """Generate a new certificate with a keypair.

    Returns:
        Tuple of (CertificateBase, X509Certificate, private_key, cert_pem, key_pem)

    """
    try:
        logger.debug("📜🔑🚀 Generating new keypair")

        # Calculate validity period
        now = datetime.now(UTC)
        not_valid_before = now - timedelta(days=1)
        not_valid_after = now + timedelta(days=validity_days)

        # Parse and validate key type parameters
        gen_key_type, gen_key_size, gen_curve = _parse_key_type_and_params(key_type, key_size, ecdsa_curve)

        # Build certificate configuration
        conf = _build_certificate_config(
            common_name=common_name,
            organization_name=organization_name,
            not_valid_before=not_valid_before,
            not_valid_after=not_valid_after,
            gen_key_type=gen_key_type,
            gen_key_size=gen_key_size,
            gen_curve=gen_curve,
        )
        logger.debug(f"📜🔑🚀 Generation config: {conf}")

        # Generate base certificate and private key
        base, private_key = CertificateBase.create(conf)

        # Create X.509 certificate
        x509_cert = create_x509_certificate(
            base=base,
            private_key=private_key,
            alt_names=alt_names or ["localhost"],
            is_ca=is_ca,
            is_client_cert=is_client_cert,
        )

        if x509_cert is None:
            raise CertificateError("Certificate object (_cert) is None after creation")

        # Serialize to PEM format
        cert_pem, key_pem = _serialize_to_pem(x509_cert, private_key)

        logger.debug("📜🔑✅ Generated cert and key")

        return base, x509_cert, private_key, cert_pem, key_pem

    except Exception as e:
        logger.error(
            f"📜❌ Failed to generate certificate. Error: {type(e).__name__}: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError(f"Failed to initialize certificate. Original error: {type(e).__name__}") from e


def x_generate_certificate__mutmut_37(
    common_name: str,
    organization_name: str,
    validity_days: int,
    key_type: str = DEFAULT_CERTIFICATE_KEY_TYPE,
    key_size: int = DEFAULT_RSA_KEY_SIZE,
    ecdsa_curve: str = DEFAULT_CERTIFICATE_CURVE,
    alt_names: list[str] | None = None,
    is_ca: bool = False,
    is_client_cert: bool = False,
) -> tuple[
    CertificateBase,
    x509.Certificate,
    KeyPair,
    str,
    str,
]:
    """Generate a new certificate with a keypair.

    Returns:
        Tuple of (CertificateBase, X509Certificate, private_key, cert_pem, key_pem)

    """
    try:
        logger.debug("📜🔑🚀 Generating new keypair")

        # Calculate validity period
        now = datetime.now(UTC)
        not_valid_before = now - timedelta(days=1)
        not_valid_after = now + timedelta(days=validity_days)

        # Parse and validate key type parameters
        gen_key_type, gen_key_size, gen_curve = _parse_key_type_and_params(key_type, key_size, ecdsa_curve)

        # Build certificate configuration
        conf = _build_certificate_config(
            common_name=common_name,
            organization_name=organization_name,
            not_valid_before=not_valid_before,
            not_valid_after=not_valid_after,
            alt_names=alt_names,
            gen_key_size=gen_key_size,
            gen_curve=gen_curve,
        )
        logger.debug(f"📜🔑🚀 Generation config: {conf}")

        # Generate base certificate and private key
        base, private_key = CertificateBase.create(conf)

        # Create X.509 certificate
        x509_cert = create_x509_certificate(
            base=base,
            private_key=private_key,
            alt_names=alt_names or ["localhost"],
            is_ca=is_ca,
            is_client_cert=is_client_cert,
        )

        if x509_cert is None:
            raise CertificateError("Certificate object (_cert) is None after creation")

        # Serialize to PEM format
        cert_pem, key_pem = _serialize_to_pem(x509_cert, private_key)

        logger.debug("📜🔑✅ Generated cert and key")

        return base, x509_cert, private_key, cert_pem, key_pem

    except Exception as e:
        logger.error(
            f"📜❌ Failed to generate certificate. Error: {type(e).__name__}: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError(f"Failed to initialize certificate. Original error: {type(e).__name__}") from e


def x_generate_certificate__mutmut_38(
    common_name: str,
    organization_name: str,
    validity_days: int,
    key_type: str = DEFAULT_CERTIFICATE_KEY_TYPE,
    key_size: int = DEFAULT_RSA_KEY_SIZE,
    ecdsa_curve: str = DEFAULT_CERTIFICATE_CURVE,
    alt_names: list[str] | None = None,
    is_ca: bool = False,
    is_client_cert: bool = False,
) -> tuple[
    CertificateBase,
    x509.Certificate,
    KeyPair,
    str,
    str,
]:
    """Generate a new certificate with a keypair.

    Returns:
        Tuple of (CertificateBase, X509Certificate, private_key, cert_pem, key_pem)

    """
    try:
        logger.debug("📜🔑🚀 Generating new keypair")

        # Calculate validity period
        now = datetime.now(UTC)
        not_valid_before = now - timedelta(days=1)
        not_valid_after = now + timedelta(days=validity_days)

        # Parse and validate key type parameters
        gen_key_type, gen_key_size, gen_curve = _parse_key_type_and_params(key_type, key_size, ecdsa_curve)

        # Build certificate configuration
        conf = _build_certificate_config(
            common_name=common_name,
            organization_name=organization_name,
            not_valid_before=not_valid_before,
            not_valid_after=not_valid_after,
            alt_names=alt_names,
            gen_key_type=gen_key_type,
            gen_curve=gen_curve,
        )
        logger.debug(f"📜🔑🚀 Generation config: {conf}")

        # Generate base certificate and private key
        base, private_key = CertificateBase.create(conf)

        # Create X.509 certificate
        x509_cert = create_x509_certificate(
            base=base,
            private_key=private_key,
            alt_names=alt_names or ["localhost"],
            is_ca=is_ca,
            is_client_cert=is_client_cert,
        )

        if x509_cert is None:
            raise CertificateError("Certificate object (_cert) is None after creation")

        # Serialize to PEM format
        cert_pem, key_pem = _serialize_to_pem(x509_cert, private_key)

        logger.debug("📜🔑✅ Generated cert and key")

        return base, x509_cert, private_key, cert_pem, key_pem

    except Exception as e:
        logger.error(
            f"📜❌ Failed to generate certificate. Error: {type(e).__name__}: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError(f"Failed to initialize certificate. Original error: {type(e).__name__}") from e


def x_generate_certificate__mutmut_39(
    common_name: str,
    organization_name: str,
    validity_days: int,
    key_type: str = DEFAULT_CERTIFICATE_KEY_TYPE,
    key_size: int = DEFAULT_RSA_KEY_SIZE,
    ecdsa_curve: str = DEFAULT_CERTIFICATE_CURVE,
    alt_names: list[str] | None = None,
    is_ca: bool = False,
    is_client_cert: bool = False,
) -> tuple[
    CertificateBase,
    x509.Certificate,
    KeyPair,
    str,
    str,
]:
    """Generate a new certificate with a keypair.

    Returns:
        Tuple of (CertificateBase, X509Certificate, private_key, cert_pem, key_pem)

    """
    try:
        logger.debug("📜🔑🚀 Generating new keypair")

        # Calculate validity period
        now = datetime.now(UTC)
        not_valid_before = now - timedelta(days=1)
        not_valid_after = now + timedelta(days=validity_days)

        # Parse and validate key type parameters
        gen_key_type, gen_key_size, gen_curve = _parse_key_type_and_params(key_type, key_size, ecdsa_curve)

        # Build certificate configuration
        conf = _build_certificate_config(
            common_name=common_name,
            organization_name=organization_name,
            not_valid_before=not_valid_before,
            not_valid_after=not_valid_after,
            alt_names=alt_names,
            gen_key_type=gen_key_type,
            gen_key_size=gen_key_size,
        )
        logger.debug(f"📜🔑🚀 Generation config: {conf}")

        # Generate base certificate and private key
        base, private_key = CertificateBase.create(conf)

        # Create X.509 certificate
        x509_cert = create_x509_certificate(
            base=base,
            private_key=private_key,
            alt_names=alt_names or ["localhost"],
            is_ca=is_ca,
            is_client_cert=is_client_cert,
        )

        if x509_cert is None:
            raise CertificateError("Certificate object (_cert) is None after creation")

        # Serialize to PEM format
        cert_pem, key_pem = _serialize_to_pem(x509_cert, private_key)

        logger.debug("📜🔑✅ Generated cert and key")

        return base, x509_cert, private_key, cert_pem, key_pem

    except Exception as e:
        logger.error(
            f"📜❌ Failed to generate certificate. Error: {type(e).__name__}: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError(f"Failed to initialize certificate. Original error: {type(e).__name__}") from e


def x_generate_certificate__mutmut_40(
    common_name: str,
    organization_name: str,
    validity_days: int,
    key_type: str = DEFAULT_CERTIFICATE_KEY_TYPE,
    key_size: int = DEFAULT_RSA_KEY_SIZE,
    ecdsa_curve: str = DEFAULT_CERTIFICATE_CURVE,
    alt_names: list[str] | None = None,
    is_ca: bool = False,
    is_client_cert: bool = False,
) -> tuple[
    CertificateBase,
    x509.Certificate,
    KeyPair,
    str,
    str,
]:
    """Generate a new certificate with a keypair.

    Returns:
        Tuple of (CertificateBase, X509Certificate, private_key, cert_pem, key_pem)

    """
    try:
        logger.debug("📜🔑🚀 Generating new keypair")

        # Calculate validity period
        now = datetime.now(UTC)
        not_valid_before = now - timedelta(days=1)
        not_valid_after = now + timedelta(days=validity_days)

        # Parse and validate key type parameters
        gen_key_type, gen_key_size, gen_curve = _parse_key_type_and_params(key_type, key_size, ecdsa_curve)

        # Build certificate configuration
        conf = _build_certificate_config(
            common_name=common_name,
            organization_name=organization_name,
            not_valid_before=not_valid_before,
            not_valid_after=not_valid_after,
            alt_names=alt_names,
            gen_key_type=gen_key_type,
            gen_key_size=gen_key_size,
            gen_curve=gen_curve,
        )
        logger.debug(None)

        # Generate base certificate and private key
        base, private_key = CertificateBase.create(conf)

        # Create X.509 certificate
        x509_cert = create_x509_certificate(
            base=base,
            private_key=private_key,
            alt_names=alt_names or ["localhost"],
            is_ca=is_ca,
            is_client_cert=is_client_cert,
        )

        if x509_cert is None:
            raise CertificateError("Certificate object (_cert) is None after creation")

        # Serialize to PEM format
        cert_pem, key_pem = _serialize_to_pem(x509_cert, private_key)

        logger.debug("📜🔑✅ Generated cert and key")

        return base, x509_cert, private_key, cert_pem, key_pem

    except Exception as e:
        logger.error(
            f"📜❌ Failed to generate certificate. Error: {type(e).__name__}: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError(f"Failed to initialize certificate. Original error: {type(e).__name__}") from e


def x_generate_certificate__mutmut_41(
    common_name: str,
    organization_name: str,
    validity_days: int,
    key_type: str = DEFAULT_CERTIFICATE_KEY_TYPE,
    key_size: int = DEFAULT_RSA_KEY_SIZE,
    ecdsa_curve: str = DEFAULT_CERTIFICATE_CURVE,
    alt_names: list[str] | None = None,
    is_ca: bool = False,
    is_client_cert: bool = False,
) -> tuple[
    CertificateBase,
    x509.Certificate,
    KeyPair,
    str,
    str,
]:
    """Generate a new certificate with a keypair.

    Returns:
        Tuple of (CertificateBase, X509Certificate, private_key, cert_pem, key_pem)

    """
    try:
        logger.debug("📜🔑🚀 Generating new keypair")

        # Calculate validity period
        now = datetime.now(UTC)
        not_valid_before = now - timedelta(days=1)
        not_valid_after = now + timedelta(days=validity_days)

        # Parse and validate key type parameters
        gen_key_type, gen_key_size, gen_curve = _parse_key_type_and_params(key_type, key_size, ecdsa_curve)

        # Build certificate configuration
        conf = _build_certificate_config(
            common_name=common_name,
            organization_name=organization_name,
            not_valid_before=not_valid_before,
            not_valid_after=not_valid_after,
            alt_names=alt_names,
            gen_key_type=gen_key_type,
            gen_key_size=gen_key_size,
            gen_curve=gen_curve,
        )
        logger.debug(f"📜🔑🚀 Generation config: {conf}")

        # Generate base certificate and private key
        base, private_key = None

        # Create X.509 certificate
        x509_cert = create_x509_certificate(
            base=base,
            private_key=private_key,
            alt_names=alt_names or ["localhost"],
            is_ca=is_ca,
            is_client_cert=is_client_cert,
        )

        if x509_cert is None:
            raise CertificateError("Certificate object (_cert) is None after creation")

        # Serialize to PEM format
        cert_pem, key_pem = _serialize_to_pem(x509_cert, private_key)

        logger.debug("📜🔑✅ Generated cert and key")

        return base, x509_cert, private_key, cert_pem, key_pem

    except Exception as e:
        logger.error(
            f"📜❌ Failed to generate certificate. Error: {type(e).__name__}: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError(f"Failed to initialize certificate. Original error: {type(e).__name__}") from e


def x_generate_certificate__mutmut_42(
    common_name: str,
    organization_name: str,
    validity_days: int,
    key_type: str = DEFAULT_CERTIFICATE_KEY_TYPE,
    key_size: int = DEFAULT_RSA_KEY_SIZE,
    ecdsa_curve: str = DEFAULT_CERTIFICATE_CURVE,
    alt_names: list[str] | None = None,
    is_ca: bool = False,
    is_client_cert: bool = False,
) -> tuple[
    CertificateBase,
    x509.Certificate,
    KeyPair,
    str,
    str,
]:
    """Generate a new certificate with a keypair.

    Returns:
        Tuple of (CertificateBase, X509Certificate, private_key, cert_pem, key_pem)

    """
    try:
        logger.debug("📜🔑🚀 Generating new keypair")

        # Calculate validity period
        now = datetime.now(UTC)
        not_valid_before = now - timedelta(days=1)
        not_valid_after = now + timedelta(days=validity_days)

        # Parse and validate key type parameters
        gen_key_type, gen_key_size, gen_curve = _parse_key_type_and_params(key_type, key_size, ecdsa_curve)

        # Build certificate configuration
        conf = _build_certificate_config(
            common_name=common_name,
            organization_name=organization_name,
            not_valid_before=not_valid_before,
            not_valid_after=not_valid_after,
            alt_names=alt_names,
            gen_key_type=gen_key_type,
            gen_key_size=gen_key_size,
            gen_curve=gen_curve,
        )
        logger.debug(f"📜🔑🚀 Generation config: {conf}")

        # Generate base certificate and private key
        base, private_key = CertificateBase.create(None)

        # Create X.509 certificate
        x509_cert = create_x509_certificate(
            base=base,
            private_key=private_key,
            alt_names=alt_names or ["localhost"],
            is_ca=is_ca,
            is_client_cert=is_client_cert,
        )

        if x509_cert is None:
            raise CertificateError("Certificate object (_cert) is None after creation")

        # Serialize to PEM format
        cert_pem, key_pem = _serialize_to_pem(x509_cert, private_key)

        logger.debug("📜🔑✅ Generated cert and key")

        return base, x509_cert, private_key, cert_pem, key_pem

    except Exception as e:
        logger.error(
            f"📜❌ Failed to generate certificate. Error: {type(e).__name__}: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError(f"Failed to initialize certificate. Original error: {type(e).__name__}") from e


def x_generate_certificate__mutmut_43(
    common_name: str,
    organization_name: str,
    validity_days: int,
    key_type: str = DEFAULT_CERTIFICATE_KEY_TYPE,
    key_size: int = DEFAULT_RSA_KEY_SIZE,
    ecdsa_curve: str = DEFAULT_CERTIFICATE_CURVE,
    alt_names: list[str] | None = None,
    is_ca: bool = False,
    is_client_cert: bool = False,
) -> tuple[
    CertificateBase,
    x509.Certificate,
    KeyPair,
    str,
    str,
]:
    """Generate a new certificate with a keypair.

    Returns:
        Tuple of (CertificateBase, X509Certificate, private_key, cert_pem, key_pem)

    """
    try:
        logger.debug("📜🔑🚀 Generating new keypair")

        # Calculate validity period
        now = datetime.now(UTC)
        not_valid_before = now - timedelta(days=1)
        not_valid_after = now + timedelta(days=validity_days)

        # Parse and validate key type parameters
        gen_key_type, gen_key_size, gen_curve = _parse_key_type_and_params(key_type, key_size, ecdsa_curve)

        # Build certificate configuration
        conf = _build_certificate_config(
            common_name=common_name,
            organization_name=organization_name,
            not_valid_before=not_valid_before,
            not_valid_after=not_valid_after,
            alt_names=alt_names,
            gen_key_type=gen_key_type,
            gen_key_size=gen_key_size,
            gen_curve=gen_curve,
        )
        logger.debug(f"📜🔑🚀 Generation config: {conf}")

        # Generate base certificate and private key
        base, private_key = CertificateBase.create(conf)

        # Create X.509 certificate
        x509_cert = None

        if x509_cert is None:
            raise CertificateError("Certificate object (_cert) is None after creation")

        # Serialize to PEM format
        cert_pem, key_pem = _serialize_to_pem(x509_cert, private_key)

        logger.debug("📜🔑✅ Generated cert and key")

        return base, x509_cert, private_key, cert_pem, key_pem

    except Exception as e:
        logger.error(
            f"📜❌ Failed to generate certificate. Error: {type(e).__name__}: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError(f"Failed to initialize certificate. Original error: {type(e).__name__}") from e


def x_generate_certificate__mutmut_44(
    common_name: str,
    organization_name: str,
    validity_days: int,
    key_type: str = DEFAULT_CERTIFICATE_KEY_TYPE,
    key_size: int = DEFAULT_RSA_KEY_SIZE,
    ecdsa_curve: str = DEFAULT_CERTIFICATE_CURVE,
    alt_names: list[str] | None = None,
    is_ca: bool = False,
    is_client_cert: bool = False,
) -> tuple[
    CertificateBase,
    x509.Certificate,
    KeyPair,
    str,
    str,
]:
    """Generate a new certificate with a keypair.

    Returns:
        Tuple of (CertificateBase, X509Certificate, private_key, cert_pem, key_pem)

    """
    try:
        logger.debug("📜🔑🚀 Generating new keypair")

        # Calculate validity period
        now = datetime.now(UTC)
        not_valid_before = now - timedelta(days=1)
        not_valid_after = now + timedelta(days=validity_days)

        # Parse and validate key type parameters
        gen_key_type, gen_key_size, gen_curve = _parse_key_type_and_params(key_type, key_size, ecdsa_curve)

        # Build certificate configuration
        conf = _build_certificate_config(
            common_name=common_name,
            organization_name=organization_name,
            not_valid_before=not_valid_before,
            not_valid_after=not_valid_after,
            alt_names=alt_names,
            gen_key_type=gen_key_type,
            gen_key_size=gen_key_size,
            gen_curve=gen_curve,
        )
        logger.debug(f"📜🔑🚀 Generation config: {conf}")

        # Generate base certificate and private key
        base, private_key = CertificateBase.create(conf)

        # Create X.509 certificate
        x509_cert = create_x509_certificate(
            base=None,
            private_key=private_key,
            alt_names=alt_names or ["localhost"],
            is_ca=is_ca,
            is_client_cert=is_client_cert,
        )

        if x509_cert is None:
            raise CertificateError("Certificate object (_cert) is None after creation")

        # Serialize to PEM format
        cert_pem, key_pem = _serialize_to_pem(x509_cert, private_key)

        logger.debug("📜🔑✅ Generated cert and key")

        return base, x509_cert, private_key, cert_pem, key_pem

    except Exception as e:
        logger.error(
            f"📜❌ Failed to generate certificate. Error: {type(e).__name__}: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError(f"Failed to initialize certificate. Original error: {type(e).__name__}") from e


def x_generate_certificate__mutmut_45(
    common_name: str,
    organization_name: str,
    validity_days: int,
    key_type: str = DEFAULT_CERTIFICATE_KEY_TYPE,
    key_size: int = DEFAULT_RSA_KEY_SIZE,
    ecdsa_curve: str = DEFAULT_CERTIFICATE_CURVE,
    alt_names: list[str] | None = None,
    is_ca: bool = False,
    is_client_cert: bool = False,
) -> tuple[
    CertificateBase,
    x509.Certificate,
    KeyPair,
    str,
    str,
]:
    """Generate a new certificate with a keypair.

    Returns:
        Tuple of (CertificateBase, X509Certificate, private_key, cert_pem, key_pem)

    """
    try:
        logger.debug("📜🔑🚀 Generating new keypair")

        # Calculate validity period
        now = datetime.now(UTC)
        not_valid_before = now - timedelta(days=1)
        not_valid_after = now + timedelta(days=validity_days)

        # Parse and validate key type parameters
        gen_key_type, gen_key_size, gen_curve = _parse_key_type_and_params(key_type, key_size, ecdsa_curve)

        # Build certificate configuration
        conf = _build_certificate_config(
            common_name=common_name,
            organization_name=organization_name,
            not_valid_before=not_valid_before,
            not_valid_after=not_valid_after,
            alt_names=alt_names,
            gen_key_type=gen_key_type,
            gen_key_size=gen_key_size,
            gen_curve=gen_curve,
        )
        logger.debug(f"📜🔑🚀 Generation config: {conf}")

        # Generate base certificate and private key
        base, private_key = CertificateBase.create(conf)

        # Create X.509 certificate
        x509_cert = create_x509_certificate(
            base=base,
            private_key=None,
            alt_names=alt_names or ["localhost"],
            is_ca=is_ca,
            is_client_cert=is_client_cert,
        )

        if x509_cert is None:
            raise CertificateError("Certificate object (_cert) is None after creation")

        # Serialize to PEM format
        cert_pem, key_pem = _serialize_to_pem(x509_cert, private_key)

        logger.debug("📜🔑✅ Generated cert and key")

        return base, x509_cert, private_key, cert_pem, key_pem

    except Exception as e:
        logger.error(
            f"📜❌ Failed to generate certificate. Error: {type(e).__name__}: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError(f"Failed to initialize certificate. Original error: {type(e).__name__}") from e


def x_generate_certificate__mutmut_46(
    common_name: str,
    organization_name: str,
    validity_days: int,
    key_type: str = DEFAULT_CERTIFICATE_KEY_TYPE,
    key_size: int = DEFAULT_RSA_KEY_SIZE,
    ecdsa_curve: str = DEFAULT_CERTIFICATE_CURVE,
    alt_names: list[str] | None = None,
    is_ca: bool = False,
    is_client_cert: bool = False,
) -> tuple[
    CertificateBase,
    x509.Certificate,
    KeyPair,
    str,
    str,
]:
    """Generate a new certificate with a keypair.

    Returns:
        Tuple of (CertificateBase, X509Certificate, private_key, cert_pem, key_pem)

    """
    try:
        logger.debug("📜🔑🚀 Generating new keypair")

        # Calculate validity period
        now = datetime.now(UTC)
        not_valid_before = now - timedelta(days=1)
        not_valid_after = now + timedelta(days=validity_days)

        # Parse and validate key type parameters
        gen_key_type, gen_key_size, gen_curve = _parse_key_type_and_params(key_type, key_size, ecdsa_curve)

        # Build certificate configuration
        conf = _build_certificate_config(
            common_name=common_name,
            organization_name=organization_name,
            not_valid_before=not_valid_before,
            not_valid_after=not_valid_after,
            alt_names=alt_names,
            gen_key_type=gen_key_type,
            gen_key_size=gen_key_size,
            gen_curve=gen_curve,
        )
        logger.debug(f"📜🔑🚀 Generation config: {conf}")

        # Generate base certificate and private key
        base, private_key = CertificateBase.create(conf)

        # Create X.509 certificate
        x509_cert = create_x509_certificate(
            base=base,
            private_key=private_key,
            alt_names=None,
            is_ca=is_ca,
            is_client_cert=is_client_cert,
        )

        if x509_cert is None:
            raise CertificateError("Certificate object (_cert) is None after creation")

        # Serialize to PEM format
        cert_pem, key_pem = _serialize_to_pem(x509_cert, private_key)

        logger.debug("📜🔑✅ Generated cert and key")

        return base, x509_cert, private_key, cert_pem, key_pem

    except Exception as e:
        logger.error(
            f"📜❌ Failed to generate certificate. Error: {type(e).__name__}: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError(f"Failed to initialize certificate. Original error: {type(e).__name__}") from e


def x_generate_certificate__mutmut_47(
    common_name: str,
    organization_name: str,
    validity_days: int,
    key_type: str = DEFAULT_CERTIFICATE_KEY_TYPE,
    key_size: int = DEFAULT_RSA_KEY_SIZE,
    ecdsa_curve: str = DEFAULT_CERTIFICATE_CURVE,
    alt_names: list[str] | None = None,
    is_ca: bool = False,
    is_client_cert: bool = False,
) -> tuple[
    CertificateBase,
    x509.Certificate,
    KeyPair,
    str,
    str,
]:
    """Generate a new certificate with a keypair.

    Returns:
        Tuple of (CertificateBase, X509Certificate, private_key, cert_pem, key_pem)

    """
    try:
        logger.debug("📜🔑🚀 Generating new keypair")

        # Calculate validity period
        now = datetime.now(UTC)
        not_valid_before = now - timedelta(days=1)
        not_valid_after = now + timedelta(days=validity_days)

        # Parse and validate key type parameters
        gen_key_type, gen_key_size, gen_curve = _parse_key_type_and_params(key_type, key_size, ecdsa_curve)

        # Build certificate configuration
        conf = _build_certificate_config(
            common_name=common_name,
            organization_name=organization_name,
            not_valid_before=not_valid_before,
            not_valid_after=not_valid_after,
            alt_names=alt_names,
            gen_key_type=gen_key_type,
            gen_key_size=gen_key_size,
            gen_curve=gen_curve,
        )
        logger.debug(f"📜🔑🚀 Generation config: {conf}")

        # Generate base certificate and private key
        base, private_key = CertificateBase.create(conf)

        # Create X.509 certificate
        x509_cert = create_x509_certificate(
            base=base,
            private_key=private_key,
            alt_names=alt_names or ["localhost"],
            is_ca=None,
            is_client_cert=is_client_cert,
        )

        if x509_cert is None:
            raise CertificateError("Certificate object (_cert) is None after creation")

        # Serialize to PEM format
        cert_pem, key_pem = _serialize_to_pem(x509_cert, private_key)

        logger.debug("📜🔑✅ Generated cert and key")

        return base, x509_cert, private_key, cert_pem, key_pem

    except Exception as e:
        logger.error(
            f"📜❌ Failed to generate certificate. Error: {type(e).__name__}: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError(f"Failed to initialize certificate. Original error: {type(e).__name__}") from e


def x_generate_certificate__mutmut_48(
    common_name: str,
    organization_name: str,
    validity_days: int,
    key_type: str = DEFAULT_CERTIFICATE_KEY_TYPE,
    key_size: int = DEFAULT_RSA_KEY_SIZE,
    ecdsa_curve: str = DEFAULT_CERTIFICATE_CURVE,
    alt_names: list[str] | None = None,
    is_ca: bool = False,
    is_client_cert: bool = False,
) -> tuple[
    CertificateBase,
    x509.Certificate,
    KeyPair,
    str,
    str,
]:
    """Generate a new certificate with a keypair.

    Returns:
        Tuple of (CertificateBase, X509Certificate, private_key, cert_pem, key_pem)

    """
    try:
        logger.debug("📜🔑🚀 Generating new keypair")

        # Calculate validity period
        now = datetime.now(UTC)
        not_valid_before = now - timedelta(days=1)
        not_valid_after = now + timedelta(days=validity_days)

        # Parse and validate key type parameters
        gen_key_type, gen_key_size, gen_curve = _parse_key_type_and_params(key_type, key_size, ecdsa_curve)

        # Build certificate configuration
        conf = _build_certificate_config(
            common_name=common_name,
            organization_name=organization_name,
            not_valid_before=not_valid_before,
            not_valid_after=not_valid_after,
            alt_names=alt_names,
            gen_key_type=gen_key_type,
            gen_key_size=gen_key_size,
            gen_curve=gen_curve,
        )
        logger.debug(f"📜🔑🚀 Generation config: {conf}")

        # Generate base certificate and private key
        base, private_key = CertificateBase.create(conf)

        # Create X.509 certificate
        x509_cert = create_x509_certificate(
            base=base,
            private_key=private_key,
            alt_names=alt_names or ["localhost"],
            is_ca=is_ca,
            is_client_cert=None,
        )

        if x509_cert is None:
            raise CertificateError("Certificate object (_cert) is None after creation")

        # Serialize to PEM format
        cert_pem, key_pem = _serialize_to_pem(x509_cert, private_key)

        logger.debug("📜🔑✅ Generated cert and key")

        return base, x509_cert, private_key, cert_pem, key_pem

    except Exception as e:
        logger.error(
            f"📜❌ Failed to generate certificate. Error: {type(e).__name__}: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError(f"Failed to initialize certificate. Original error: {type(e).__name__}") from e


def x_generate_certificate__mutmut_49(
    common_name: str,
    organization_name: str,
    validity_days: int,
    key_type: str = DEFAULT_CERTIFICATE_KEY_TYPE,
    key_size: int = DEFAULT_RSA_KEY_SIZE,
    ecdsa_curve: str = DEFAULT_CERTIFICATE_CURVE,
    alt_names: list[str] | None = None,
    is_ca: bool = False,
    is_client_cert: bool = False,
) -> tuple[
    CertificateBase,
    x509.Certificate,
    KeyPair,
    str,
    str,
]:
    """Generate a new certificate with a keypair.

    Returns:
        Tuple of (CertificateBase, X509Certificate, private_key, cert_pem, key_pem)

    """
    try:
        logger.debug("📜🔑🚀 Generating new keypair")

        # Calculate validity period
        now = datetime.now(UTC)
        not_valid_before = now - timedelta(days=1)
        not_valid_after = now + timedelta(days=validity_days)

        # Parse and validate key type parameters
        gen_key_type, gen_key_size, gen_curve = _parse_key_type_and_params(key_type, key_size, ecdsa_curve)

        # Build certificate configuration
        conf = _build_certificate_config(
            common_name=common_name,
            organization_name=organization_name,
            not_valid_before=not_valid_before,
            not_valid_after=not_valid_after,
            alt_names=alt_names,
            gen_key_type=gen_key_type,
            gen_key_size=gen_key_size,
            gen_curve=gen_curve,
        )
        logger.debug(f"📜🔑🚀 Generation config: {conf}")

        # Generate base certificate and private key
        base, private_key = CertificateBase.create(conf)

        # Create X.509 certificate
        x509_cert = create_x509_certificate(
            private_key=private_key,
            alt_names=alt_names or ["localhost"],
            is_ca=is_ca,
            is_client_cert=is_client_cert,
        )

        if x509_cert is None:
            raise CertificateError("Certificate object (_cert) is None after creation")

        # Serialize to PEM format
        cert_pem, key_pem = _serialize_to_pem(x509_cert, private_key)

        logger.debug("📜🔑✅ Generated cert and key")

        return base, x509_cert, private_key, cert_pem, key_pem

    except Exception as e:
        logger.error(
            f"📜❌ Failed to generate certificate. Error: {type(e).__name__}: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError(f"Failed to initialize certificate. Original error: {type(e).__name__}") from e


def x_generate_certificate__mutmut_50(
    common_name: str,
    organization_name: str,
    validity_days: int,
    key_type: str = DEFAULT_CERTIFICATE_KEY_TYPE,
    key_size: int = DEFAULT_RSA_KEY_SIZE,
    ecdsa_curve: str = DEFAULT_CERTIFICATE_CURVE,
    alt_names: list[str] | None = None,
    is_ca: bool = False,
    is_client_cert: bool = False,
) -> tuple[
    CertificateBase,
    x509.Certificate,
    KeyPair,
    str,
    str,
]:
    """Generate a new certificate with a keypair.

    Returns:
        Tuple of (CertificateBase, X509Certificate, private_key, cert_pem, key_pem)

    """
    try:
        logger.debug("📜🔑🚀 Generating new keypair")

        # Calculate validity period
        now = datetime.now(UTC)
        not_valid_before = now - timedelta(days=1)
        not_valid_after = now + timedelta(days=validity_days)

        # Parse and validate key type parameters
        gen_key_type, gen_key_size, gen_curve = _parse_key_type_and_params(key_type, key_size, ecdsa_curve)

        # Build certificate configuration
        conf = _build_certificate_config(
            common_name=common_name,
            organization_name=organization_name,
            not_valid_before=not_valid_before,
            not_valid_after=not_valid_after,
            alt_names=alt_names,
            gen_key_type=gen_key_type,
            gen_key_size=gen_key_size,
            gen_curve=gen_curve,
        )
        logger.debug(f"📜🔑🚀 Generation config: {conf}")

        # Generate base certificate and private key
        base, private_key = CertificateBase.create(conf)

        # Create X.509 certificate
        x509_cert = create_x509_certificate(
            base=base,
            alt_names=alt_names or ["localhost"],
            is_ca=is_ca,
            is_client_cert=is_client_cert,
        )

        if x509_cert is None:
            raise CertificateError("Certificate object (_cert) is None after creation")

        # Serialize to PEM format
        cert_pem, key_pem = _serialize_to_pem(x509_cert, private_key)

        logger.debug("📜🔑✅ Generated cert and key")

        return base, x509_cert, private_key, cert_pem, key_pem

    except Exception as e:
        logger.error(
            f"📜❌ Failed to generate certificate. Error: {type(e).__name__}: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError(f"Failed to initialize certificate. Original error: {type(e).__name__}") from e


def x_generate_certificate__mutmut_51(
    common_name: str,
    organization_name: str,
    validity_days: int,
    key_type: str = DEFAULT_CERTIFICATE_KEY_TYPE,
    key_size: int = DEFAULT_RSA_KEY_SIZE,
    ecdsa_curve: str = DEFAULT_CERTIFICATE_CURVE,
    alt_names: list[str] | None = None,
    is_ca: bool = False,
    is_client_cert: bool = False,
) -> tuple[
    CertificateBase,
    x509.Certificate,
    KeyPair,
    str,
    str,
]:
    """Generate a new certificate with a keypair.

    Returns:
        Tuple of (CertificateBase, X509Certificate, private_key, cert_pem, key_pem)

    """
    try:
        logger.debug("📜🔑🚀 Generating new keypair")

        # Calculate validity period
        now = datetime.now(UTC)
        not_valid_before = now - timedelta(days=1)
        not_valid_after = now + timedelta(days=validity_days)

        # Parse and validate key type parameters
        gen_key_type, gen_key_size, gen_curve = _parse_key_type_and_params(key_type, key_size, ecdsa_curve)

        # Build certificate configuration
        conf = _build_certificate_config(
            common_name=common_name,
            organization_name=organization_name,
            not_valid_before=not_valid_before,
            not_valid_after=not_valid_after,
            alt_names=alt_names,
            gen_key_type=gen_key_type,
            gen_key_size=gen_key_size,
            gen_curve=gen_curve,
        )
        logger.debug(f"📜🔑🚀 Generation config: {conf}")

        # Generate base certificate and private key
        base, private_key = CertificateBase.create(conf)

        # Create X.509 certificate
        x509_cert = create_x509_certificate(
            base=base,
            private_key=private_key,
            is_ca=is_ca,
            is_client_cert=is_client_cert,
        )

        if x509_cert is None:
            raise CertificateError("Certificate object (_cert) is None after creation")

        # Serialize to PEM format
        cert_pem, key_pem = _serialize_to_pem(x509_cert, private_key)

        logger.debug("📜🔑✅ Generated cert and key")

        return base, x509_cert, private_key, cert_pem, key_pem

    except Exception as e:
        logger.error(
            f"📜❌ Failed to generate certificate. Error: {type(e).__name__}: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError(f"Failed to initialize certificate. Original error: {type(e).__name__}") from e


def x_generate_certificate__mutmut_52(
    common_name: str,
    organization_name: str,
    validity_days: int,
    key_type: str = DEFAULT_CERTIFICATE_KEY_TYPE,
    key_size: int = DEFAULT_RSA_KEY_SIZE,
    ecdsa_curve: str = DEFAULT_CERTIFICATE_CURVE,
    alt_names: list[str] | None = None,
    is_ca: bool = False,
    is_client_cert: bool = False,
) -> tuple[
    CertificateBase,
    x509.Certificate,
    KeyPair,
    str,
    str,
]:
    """Generate a new certificate with a keypair.

    Returns:
        Tuple of (CertificateBase, X509Certificate, private_key, cert_pem, key_pem)

    """
    try:
        logger.debug("📜🔑🚀 Generating new keypair")

        # Calculate validity period
        now = datetime.now(UTC)
        not_valid_before = now - timedelta(days=1)
        not_valid_after = now + timedelta(days=validity_days)

        # Parse and validate key type parameters
        gen_key_type, gen_key_size, gen_curve = _parse_key_type_and_params(key_type, key_size, ecdsa_curve)

        # Build certificate configuration
        conf = _build_certificate_config(
            common_name=common_name,
            organization_name=organization_name,
            not_valid_before=not_valid_before,
            not_valid_after=not_valid_after,
            alt_names=alt_names,
            gen_key_type=gen_key_type,
            gen_key_size=gen_key_size,
            gen_curve=gen_curve,
        )
        logger.debug(f"📜🔑🚀 Generation config: {conf}")

        # Generate base certificate and private key
        base, private_key = CertificateBase.create(conf)

        # Create X.509 certificate
        x509_cert = create_x509_certificate(
            base=base,
            private_key=private_key,
            alt_names=alt_names or ["localhost"],
            is_client_cert=is_client_cert,
        )

        if x509_cert is None:
            raise CertificateError("Certificate object (_cert) is None after creation")

        # Serialize to PEM format
        cert_pem, key_pem = _serialize_to_pem(x509_cert, private_key)

        logger.debug("📜🔑✅ Generated cert and key")

        return base, x509_cert, private_key, cert_pem, key_pem

    except Exception as e:
        logger.error(
            f"📜❌ Failed to generate certificate. Error: {type(e).__name__}: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError(f"Failed to initialize certificate. Original error: {type(e).__name__}") from e


def x_generate_certificate__mutmut_53(
    common_name: str,
    organization_name: str,
    validity_days: int,
    key_type: str = DEFAULT_CERTIFICATE_KEY_TYPE,
    key_size: int = DEFAULT_RSA_KEY_SIZE,
    ecdsa_curve: str = DEFAULT_CERTIFICATE_CURVE,
    alt_names: list[str] | None = None,
    is_ca: bool = False,
    is_client_cert: bool = False,
) -> tuple[
    CertificateBase,
    x509.Certificate,
    KeyPair,
    str,
    str,
]:
    """Generate a new certificate with a keypair.

    Returns:
        Tuple of (CertificateBase, X509Certificate, private_key, cert_pem, key_pem)

    """
    try:
        logger.debug("📜🔑🚀 Generating new keypair")

        # Calculate validity period
        now = datetime.now(UTC)
        not_valid_before = now - timedelta(days=1)
        not_valid_after = now + timedelta(days=validity_days)

        # Parse and validate key type parameters
        gen_key_type, gen_key_size, gen_curve = _parse_key_type_and_params(key_type, key_size, ecdsa_curve)

        # Build certificate configuration
        conf = _build_certificate_config(
            common_name=common_name,
            organization_name=organization_name,
            not_valid_before=not_valid_before,
            not_valid_after=not_valid_after,
            alt_names=alt_names,
            gen_key_type=gen_key_type,
            gen_key_size=gen_key_size,
            gen_curve=gen_curve,
        )
        logger.debug(f"📜🔑🚀 Generation config: {conf}")

        # Generate base certificate and private key
        base, private_key = CertificateBase.create(conf)

        # Create X.509 certificate
        x509_cert = create_x509_certificate(
            base=base,
            private_key=private_key,
            alt_names=alt_names or ["localhost"],
            is_ca=is_ca,
        )

        if x509_cert is None:
            raise CertificateError("Certificate object (_cert) is None after creation")

        # Serialize to PEM format
        cert_pem, key_pem = _serialize_to_pem(x509_cert, private_key)

        logger.debug("📜🔑✅ Generated cert and key")

        return base, x509_cert, private_key, cert_pem, key_pem

    except Exception as e:
        logger.error(
            f"📜❌ Failed to generate certificate. Error: {type(e).__name__}: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError(f"Failed to initialize certificate. Original error: {type(e).__name__}") from e


def x_generate_certificate__mutmut_54(
    common_name: str,
    organization_name: str,
    validity_days: int,
    key_type: str = DEFAULT_CERTIFICATE_KEY_TYPE,
    key_size: int = DEFAULT_RSA_KEY_SIZE,
    ecdsa_curve: str = DEFAULT_CERTIFICATE_CURVE,
    alt_names: list[str] | None = None,
    is_ca: bool = False,
    is_client_cert: bool = False,
) -> tuple[
    CertificateBase,
    x509.Certificate,
    KeyPair,
    str,
    str,
]:
    """Generate a new certificate with a keypair.

    Returns:
        Tuple of (CertificateBase, X509Certificate, private_key, cert_pem, key_pem)

    """
    try:
        logger.debug("📜🔑🚀 Generating new keypair")

        # Calculate validity period
        now = datetime.now(UTC)
        not_valid_before = now - timedelta(days=1)
        not_valid_after = now + timedelta(days=validity_days)

        # Parse and validate key type parameters
        gen_key_type, gen_key_size, gen_curve = _parse_key_type_and_params(key_type, key_size, ecdsa_curve)

        # Build certificate configuration
        conf = _build_certificate_config(
            common_name=common_name,
            organization_name=organization_name,
            not_valid_before=not_valid_before,
            not_valid_after=not_valid_after,
            alt_names=alt_names,
            gen_key_type=gen_key_type,
            gen_key_size=gen_key_size,
            gen_curve=gen_curve,
        )
        logger.debug(f"📜🔑🚀 Generation config: {conf}")

        # Generate base certificate and private key
        base, private_key = CertificateBase.create(conf)

        # Create X.509 certificate
        x509_cert = create_x509_certificate(
            base=base,
            private_key=private_key,
            alt_names=alt_names and ["localhost"],
            is_ca=is_ca,
            is_client_cert=is_client_cert,
        )

        if x509_cert is None:
            raise CertificateError("Certificate object (_cert) is None after creation")

        # Serialize to PEM format
        cert_pem, key_pem = _serialize_to_pem(x509_cert, private_key)

        logger.debug("📜🔑✅ Generated cert and key")

        return base, x509_cert, private_key, cert_pem, key_pem

    except Exception as e:
        logger.error(
            f"📜❌ Failed to generate certificate. Error: {type(e).__name__}: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError(f"Failed to initialize certificate. Original error: {type(e).__name__}") from e


def x_generate_certificate__mutmut_55(
    common_name: str,
    organization_name: str,
    validity_days: int,
    key_type: str = DEFAULT_CERTIFICATE_KEY_TYPE,
    key_size: int = DEFAULT_RSA_KEY_SIZE,
    ecdsa_curve: str = DEFAULT_CERTIFICATE_CURVE,
    alt_names: list[str] | None = None,
    is_ca: bool = False,
    is_client_cert: bool = False,
) -> tuple[
    CertificateBase,
    x509.Certificate,
    KeyPair,
    str,
    str,
]:
    """Generate a new certificate with a keypair.

    Returns:
        Tuple of (CertificateBase, X509Certificate, private_key, cert_pem, key_pem)

    """
    try:
        logger.debug("📜🔑🚀 Generating new keypair")

        # Calculate validity period
        now = datetime.now(UTC)
        not_valid_before = now - timedelta(days=1)
        not_valid_after = now + timedelta(days=validity_days)

        # Parse and validate key type parameters
        gen_key_type, gen_key_size, gen_curve = _parse_key_type_and_params(key_type, key_size, ecdsa_curve)

        # Build certificate configuration
        conf = _build_certificate_config(
            common_name=common_name,
            organization_name=organization_name,
            not_valid_before=not_valid_before,
            not_valid_after=not_valid_after,
            alt_names=alt_names,
            gen_key_type=gen_key_type,
            gen_key_size=gen_key_size,
            gen_curve=gen_curve,
        )
        logger.debug(f"📜🔑🚀 Generation config: {conf}")

        # Generate base certificate and private key
        base, private_key = CertificateBase.create(conf)

        # Create X.509 certificate
        x509_cert = create_x509_certificate(
            base=base,
            private_key=private_key,
            alt_names=alt_names or ["XXlocalhostXX"],
            is_ca=is_ca,
            is_client_cert=is_client_cert,
        )

        if x509_cert is None:
            raise CertificateError("Certificate object (_cert) is None after creation")

        # Serialize to PEM format
        cert_pem, key_pem = _serialize_to_pem(x509_cert, private_key)

        logger.debug("📜🔑✅ Generated cert and key")

        return base, x509_cert, private_key, cert_pem, key_pem

    except Exception as e:
        logger.error(
            f"📜❌ Failed to generate certificate. Error: {type(e).__name__}: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError(f"Failed to initialize certificate. Original error: {type(e).__name__}") from e


def x_generate_certificate__mutmut_56(
    common_name: str,
    organization_name: str,
    validity_days: int,
    key_type: str = DEFAULT_CERTIFICATE_KEY_TYPE,
    key_size: int = DEFAULT_RSA_KEY_SIZE,
    ecdsa_curve: str = DEFAULT_CERTIFICATE_CURVE,
    alt_names: list[str] | None = None,
    is_ca: bool = False,
    is_client_cert: bool = False,
) -> tuple[
    CertificateBase,
    x509.Certificate,
    KeyPair,
    str,
    str,
]:
    """Generate a new certificate with a keypair.

    Returns:
        Tuple of (CertificateBase, X509Certificate, private_key, cert_pem, key_pem)

    """
    try:
        logger.debug("📜🔑🚀 Generating new keypair")

        # Calculate validity period
        now = datetime.now(UTC)
        not_valid_before = now - timedelta(days=1)
        not_valid_after = now + timedelta(days=validity_days)

        # Parse and validate key type parameters
        gen_key_type, gen_key_size, gen_curve = _parse_key_type_and_params(key_type, key_size, ecdsa_curve)

        # Build certificate configuration
        conf = _build_certificate_config(
            common_name=common_name,
            organization_name=organization_name,
            not_valid_before=not_valid_before,
            not_valid_after=not_valid_after,
            alt_names=alt_names,
            gen_key_type=gen_key_type,
            gen_key_size=gen_key_size,
            gen_curve=gen_curve,
        )
        logger.debug(f"📜🔑🚀 Generation config: {conf}")

        # Generate base certificate and private key
        base, private_key = CertificateBase.create(conf)

        # Create X.509 certificate
        x509_cert = create_x509_certificate(
            base=base,
            private_key=private_key,
            alt_names=alt_names or ["LOCALHOST"],
            is_ca=is_ca,
            is_client_cert=is_client_cert,
        )

        if x509_cert is None:
            raise CertificateError("Certificate object (_cert) is None after creation")

        # Serialize to PEM format
        cert_pem, key_pem = _serialize_to_pem(x509_cert, private_key)

        logger.debug("📜🔑✅ Generated cert and key")

        return base, x509_cert, private_key, cert_pem, key_pem

    except Exception as e:
        logger.error(
            f"📜❌ Failed to generate certificate. Error: {type(e).__name__}: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError(f"Failed to initialize certificate. Original error: {type(e).__name__}") from e


def x_generate_certificate__mutmut_57(
    common_name: str,
    organization_name: str,
    validity_days: int,
    key_type: str = DEFAULT_CERTIFICATE_KEY_TYPE,
    key_size: int = DEFAULT_RSA_KEY_SIZE,
    ecdsa_curve: str = DEFAULT_CERTIFICATE_CURVE,
    alt_names: list[str] | None = None,
    is_ca: bool = False,
    is_client_cert: bool = False,
) -> tuple[
    CertificateBase,
    x509.Certificate,
    KeyPair,
    str,
    str,
]:
    """Generate a new certificate with a keypair.

    Returns:
        Tuple of (CertificateBase, X509Certificate, private_key, cert_pem, key_pem)

    """
    try:
        logger.debug("📜🔑🚀 Generating new keypair")

        # Calculate validity period
        now = datetime.now(UTC)
        not_valid_before = now - timedelta(days=1)
        not_valid_after = now + timedelta(days=validity_days)

        # Parse and validate key type parameters
        gen_key_type, gen_key_size, gen_curve = _parse_key_type_and_params(key_type, key_size, ecdsa_curve)

        # Build certificate configuration
        conf = _build_certificate_config(
            common_name=common_name,
            organization_name=organization_name,
            not_valid_before=not_valid_before,
            not_valid_after=not_valid_after,
            alt_names=alt_names,
            gen_key_type=gen_key_type,
            gen_key_size=gen_key_size,
            gen_curve=gen_curve,
        )
        logger.debug(f"📜🔑🚀 Generation config: {conf}")

        # Generate base certificate and private key
        base, private_key = CertificateBase.create(conf)

        # Create X.509 certificate
        x509_cert = create_x509_certificate(
            base=base,
            private_key=private_key,
            alt_names=alt_names or ["localhost"],
            is_ca=is_ca,
            is_client_cert=is_client_cert,
        )

        if x509_cert is not None:
            raise CertificateError("Certificate object (_cert) is None after creation")

        # Serialize to PEM format
        cert_pem, key_pem = _serialize_to_pem(x509_cert, private_key)

        logger.debug("📜🔑✅ Generated cert and key")

        return base, x509_cert, private_key, cert_pem, key_pem

    except Exception as e:
        logger.error(
            f"📜❌ Failed to generate certificate. Error: {type(e).__name__}: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError(f"Failed to initialize certificate. Original error: {type(e).__name__}") from e


def x_generate_certificate__mutmut_58(
    common_name: str,
    organization_name: str,
    validity_days: int,
    key_type: str = DEFAULT_CERTIFICATE_KEY_TYPE,
    key_size: int = DEFAULT_RSA_KEY_SIZE,
    ecdsa_curve: str = DEFAULT_CERTIFICATE_CURVE,
    alt_names: list[str] | None = None,
    is_ca: bool = False,
    is_client_cert: bool = False,
) -> tuple[
    CertificateBase,
    x509.Certificate,
    KeyPair,
    str,
    str,
]:
    """Generate a new certificate with a keypair.

    Returns:
        Tuple of (CertificateBase, X509Certificate, private_key, cert_pem, key_pem)

    """
    try:
        logger.debug("📜🔑🚀 Generating new keypair")

        # Calculate validity period
        now = datetime.now(UTC)
        not_valid_before = now - timedelta(days=1)
        not_valid_after = now + timedelta(days=validity_days)

        # Parse and validate key type parameters
        gen_key_type, gen_key_size, gen_curve = _parse_key_type_and_params(key_type, key_size, ecdsa_curve)

        # Build certificate configuration
        conf = _build_certificate_config(
            common_name=common_name,
            organization_name=organization_name,
            not_valid_before=not_valid_before,
            not_valid_after=not_valid_after,
            alt_names=alt_names,
            gen_key_type=gen_key_type,
            gen_key_size=gen_key_size,
            gen_curve=gen_curve,
        )
        logger.debug(f"📜🔑🚀 Generation config: {conf}")

        # Generate base certificate and private key
        base, private_key = CertificateBase.create(conf)

        # Create X.509 certificate
        x509_cert = create_x509_certificate(
            base=base,
            private_key=private_key,
            alt_names=alt_names or ["localhost"],
            is_ca=is_ca,
            is_client_cert=is_client_cert,
        )

        if x509_cert is None:
            raise CertificateError(None)

        # Serialize to PEM format
        cert_pem, key_pem = _serialize_to_pem(x509_cert, private_key)

        logger.debug("📜🔑✅ Generated cert and key")

        return base, x509_cert, private_key, cert_pem, key_pem

    except Exception as e:
        logger.error(
            f"📜❌ Failed to generate certificate. Error: {type(e).__name__}: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError(f"Failed to initialize certificate. Original error: {type(e).__name__}") from e


def x_generate_certificate__mutmut_59(
    common_name: str,
    organization_name: str,
    validity_days: int,
    key_type: str = DEFAULT_CERTIFICATE_KEY_TYPE,
    key_size: int = DEFAULT_RSA_KEY_SIZE,
    ecdsa_curve: str = DEFAULT_CERTIFICATE_CURVE,
    alt_names: list[str] | None = None,
    is_ca: bool = False,
    is_client_cert: bool = False,
) -> tuple[
    CertificateBase,
    x509.Certificate,
    KeyPair,
    str,
    str,
]:
    """Generate a new certificate with a keypair.

    Returns:
        Tuple of (CertificateBase, X509Certificate, private_key, cert_pem, key_pem)

    """
    try:
        logger.debug("📜🔑🚀 Generating new keypair")

        # Calculate validity period
        now = datetime.now(UTC)
        not_valid_before = now - timedelta(days=1)
        not_valid_after = now + timedelta(days=validity_days)

        # Parse and validate key type parameters
        gen_key_type, gen_key_size, gen_curve = _parse_key_type_and_params(key_type, key_size, ecdsa_curve)

        # Build certificate configuration
        conf = _build_certificate_config(
            common_name=common_name,
            organization_name=organization_name,
            not_valid_before=not_valid_before,
            not_valid_after=not_valid_after,
            alt_names=alt_names,
            gen_key_type=gen_key_type,
            gen_key_size=gen_key_size,
            gen_curve=gen_curve,
        )
        logger.debug(f"📜🔑🚀 Generation config: {conf}")

        # Generate base certificate and private key
        base, private_key = CertificateBase.create(conf)

        # Create X.509 certificate
        x509_cert = create_x509_certificate(
            base=base,
            private_key=private_key,
            alt_names=alt_names or ["localhost"],
            is_ca=is_ca,
            is_client_cert=is_client_cert,
        )

        if x509_cert is None:
            raise CertificateError("XXCertificate object (_cert) is None after creationXX")

        # Serialize to PEM format
        cert_pem, key_pem = _serialize_to_pem(x509_cert, private_key)

        logger.debug("📜🔑✅ Generated cert and key")

        return base, x509_cert, private_key, cert_pem, key_pem

    except Exception as e:
        logger.error(
            f"📜❌ Failed to generate certificate. Error: {type(e).__name__}: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError(f"Failed to initialize certificate. Original error: {type(e).__name__}") from e


def x_generate_certificate__mutmut_60(
    common_name: str,
    organization_name: str,
    validity_days: int,
    key_type: str = DEFAULT_CERTIFICATE_KEY_TYPE,
    key_size: int = DEFAULT_RSA_KEY_SIZE,
    ecdsa_curve: str = DEFAULT_CERTIFICATE_CURVE,
    alt_names: list[str] | None = None,
    is_ca: bool = False,
    is_client_cert: bool = False,
) -> tuple[
    CertificateBase,
    x509.Certificate,
    KeyPair,
    str,
    str,
]:
    """Generate a new certificate with a keypair.

    Returns:
        Tuple of (CertificateBase, X509Certificate, private_key, cert_pem, key_pem)

    """
    try:
        logger.debug("📜🔑🚀 Generating new keypair")

        # Calculate validity period
        now = datetime.now(UTC)
        not_valid_before = now - timedelta(days=1)
        not_valid_after = now + timedelta(days=validity_days)

        # Parse and validate key type parameters
        gen_key_type, gen_key_size, gen_curve = _parse_key_type_and_params(key_type, key_size, ecdsa_curve)

        # Build certificate configuration
        conf = _build_certificate_config(
            common_name=common_name,
            organization_name=organization_name,
            not_valid_before=not_valid_before,
            not_valid_after=not_valid_after,
            alt_names=alt_names,
            gen_key_type=gen_key_type,
            gen_key_size=gen_key_size,
            gen_curve=gen_curve,
        )
        logger.debug(f"📜🔑🚀 Generation config: {conf}")

        # Generate base certificate and private key
        base, private_key = CertificateBase.create(conf)

        # Create X.509 certificate
        x509_cert = create_x509_certificate(
            base=base,
            private_key=private_key,
            alt_names=alt_names or ["localhost"],
            is_ca=is_ca,
            is_client_cert=is_client_cert,
        )

        if x509_cert is None:
            raise CertificateError("certificate object (_cert) is none after creation")

        # Serialize to PEM format
        cert_pem, key_pem = _serialize_to_pem(x509_cert, private_key)

        logger.debug("📜🔑✅ Generated cert and key")

        return base, x509_cert, private_key, cert_pem, key_pem

    except Exception as e:
        logger.error(
            f"📜❌ Failed to generate certificate. Error: {type(e).__name__}: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError(f"Failed to initialize certificate. Original error: {type(e).__name__}") from e


def x_generate_certificate__mutmut_61(
    common_name: str,
    organization_name: str,
    validity_days: int,
    key_type: str = DEFAULT_CERTIFICATE_KEY_TYPE,
    key_size: int = DEFAULT_RSA_KEY_SIZE,
    ecdsa_curve: str = DEFAULT_CERTIFICATE_CURVE,
    alt_names: list[str] | None = None,
    is_ca: bool = False,
    is_client_cert: bool = False,
) -> tuple[
    CertificateBase,
    x509.Certificate,
    KeyPair,
    str,
    str,
]:
    """Generate a new certificate with a keypair.

    Returns:
        Tuple of (CertificateBase, X509Certificate, private_key, cert_pem, key_pem)

    """
    try:
        logger.debug("📜🔑🚀 Generating new keypair")

        # Calculate validity period
        now = datetime.now(UTC)
        not_valid_before = now - timedelta(days=1)
        not_valid_after = now + timedelta(days=validity_days)

        # Parse and validate key type parameters
        gen_key_type, gen_key_size, gen_curve = _parse_key_type_and_params(key_type, key_size, ecdsa_curve)

        # Build certificate configuration
        conf = _build_certificate_config(
            common_name=common_name,
            organization_name=organization_name,
            not_valid_before=not_valid_before,
            not_valid_after=not_valid_after,
            alt_names=alt_names,
            gen_key_type=gen_key_type,
            gen_key_size=gen_key_size,
            gen_curve=gen_curve,
        )
        logger.debug(f"📜🔑🚀 Generation config: {conf}")

        # Generate base certificate and private key
        base, private_key = CertificateBase.create(conf)

        # Create X.509 certificate
        x509_cert = create_x509_certificate(
            base=base,
            private_key=private_key,
            alt_names=alt_names or ["localhost"],
            is_ca=is_ca,
            is_client_cert=is_client_cert,
        )

        if x509_cert is None:
            raise CertificateError("CERTIFICATE OBJECT (_CERT) IS NONE AFTER CREATION")

        # Serialize to PEM format
        cert_pem, key_pem = _serialize_to_pem(x509_cert, private_key)

        logger.debug("📜🔑✅ Generated cert and key")

        return base, x509_cert, private_key, cert_pem, key_pem

    except Exception as e:
        logger.error(
            f"📜❌ Failed to generate certificate. Error: {type(e).__name__}: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError(f"Failed to initialize certificate. Original error: {type(e).__name__}") from e


def x_generate_certificate__mutmut_62(
    common_name: str,
    organization_name: str,
    validity_days: int,
    key_type: str = DEFAULT_CERTIFICATE_KEY_TYPE,
    key_size: int = DEFAULT_RSA_KEY_SIZE,
    ecdsa_curve: str = DEFAULT_CERTIFICATE_CURVE,
    alt_names: list[str] | None = None,
    is_ca: bool = False,
    is_client_cert: bool = False,
) -> tuple[
    CertificateBase,
    x509.Certificate,
    KeyPair,
    str,
    str,
]:
    """Generate a new certificate with a keypair.

    Returns:
        Tuple of (CertificateBase, X509Certificate, private_key, cert_pem, key_pem)

    """
    try:
        logger.debug("📜🔑🚀 Generating new keypair")

        # Calculate validity period
        now = datetime.now(UTC)
        not_valid_before = now - timedelta(days=1)
        not_valid_after = now + timedelta(days=validity_days)

        # Parse and validate key type parameters
        gen_key_type, gen_key_size, gen_curve = _parse_key_type_and_params(key_type, key_size, ecdsa_curve)

        # Build certificate configuration
        conf = _build_certificate_config(
            common_name=common_name,
            organization_name=organization_name,
            not_valid_before=not_valid_before,
            not_valid_after=not_valid_after,
            alt_names=alt_names,
            gen_key_type=gen_key_type,
            gen_key_size=gen_key_size,
            gen_curve=gen_curve,
        )
        logger.debug(f"📜🔑🚀 Generation config: {conf}")

        # Generate base certificate and private key
        base, private_key = CertificateBase.create(conf)

        # Create X.509 certificate
        x509_cert = create_x509_certificate(
            base=base,
            private_key=private_key,
            alt_names=alt_names or ["localhost"],
            is_ca=is_ca,
            is_client_cert=is_client_cert,
        )

        if x509_cert is None:
            raise CertificateError("Certificate object (_cert) is None after creation")

        # Serialize to PEM format
        cert_pem, key_pem = None

        logger.debug("📜🔑✅ Generated cert and key")

        return base, x509_cert, private_key, cert_pem, key_pem

    except Exception as e:
        logger.error(
            f"📜❌ Failed to generate certificate. Error: {type(e).__name__}: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError(f"Failed to initialize certificate. Original error: {type(e).__name__}") from e


def x_generate_certificate__mutmut_63(
    common_name: str,
    organization_name: str,
    validity_days: int,
    key_type: str = DEFAULT_CERTIFICATE_KEY_TYPE,
    key_size: int = DEFAULT_RSA_KEY_SIZE,
    ecdsa_curve: str = DEFAULT_CERTIFICATE_CURVE,
    alt_names: list[str] | None = None,
    is_ca: bool = False,
    is_client_cert: bool = False,
) -> tuple[
    CertificateBase,
    x509.Certificate,
    KeyPair,
    str,
    str,
]:
    """Generate a new certificate with a keypair.

    Returns:
        Tuple of (CertificateBase, X509Certificate, private_key, cert_pem, key_pem)

    """
    try:
        logger.debug("📜🔑🚀 Generating new keypair")

        # Calculate validity period
        now = datetime.now(UTC)
        not_valid_before = now - timedelta(days=1)
        not_valid_after = now + timedelta(days=validity_days)

        # Parse and validate key type parameters
        gen_key_type, gen_key_size, gen_curve = _parse_key_type_and_params(key_type, key_size, ecdsa_curve)

        # Build certificate configuration
        conf = _build_certificate_config(
            common_name=common_name,
            organization_name=organization_name,
            not_valid_before=not_valid_before,
            not_valid_after=not_valid_after,
            alt_names=alt_names,
            gen_key_type=gen_key_type,
            gen_key_size=gen_key_size,
            gen_curve=gen_curve,
        )
        logger.debug(f"📜🔑🚀 Generation config: {conf}")

        # Generate base certificate and private key
        base, private_key = CertificateBase.create(conf)

        # Create X.509 certificate
        x509_cert = create_x509_certificate(
            base=base,
            private_key=private_key,
            alt_names=alt_names or ["localhost"],
            is_ca=is_ca,
            is_client_cert=is_client_cert,
        )

        if x509_cert is None:
            raise CertificateError("Certificate object (_cert) is None after creation")

        # Serialize to PEM format
        cert_pem, key_pem = _serialize_to_pem(None, private_key)

        logger.debug("📜🔑✅ Generated cert and key")

        return base, x509_cert, private_key, cert_pem, key_pem

    except Exception as e:
        logger.error(
            f"📜❌ Failed to generate certificate. Error: {type(e).__name__}: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError(f"Failed to initialize certificate. Original error: {type(e).__name__}") from e


def x_generate_certificate__mutmut_64(
    common_name: str,
    organization_name: str,
    validity_days: int,
    key_type: str = DEFAULT_CERTIFICATE_KEY_TYPE,
    key_size: int = DEFAULT_RSA_KEY_SIZE,
    ecdsa_curve: str = DEFAULT_CERTIFICATE_CURVE,
    alt_names: list[str] | None = None,
    is_ca: bool = False,
    is_client_cert: bool = False,
) -> tuple[
    CertificateBase,
    x509.Certificate,
    KeyPair,
    str,
    str,
]:
    """Generate a new certificate with a keypair.

    Returns:
        Tuple of (CertificateBase, X509Certificate, private_key, cert_pem, key_pem)

    """
    try:
        logger.debug("📜🔑🚀 Generating new keypair")

        # Calculate validity period
        now = datetime.now(UTC)
        not_valid_before = now - timedelta(days=1)
        not_valid_after = now + timedelta(days=validity_days)

        # Parse and validate key type parameters
        gen_key_type, gen_key_size, gen_curve = _parse_key_type_and_params(key_type, key_size, ecdsa_curve)

        # Build certificate configuration
        conf = _build_certificate_config(
            common_name=common_name,
            organization_name=organization_name,
            not_valid_before=not_valid_before,
            not_valid_after=not_valid_after,
            alt_names=alt_names,
            gen_key_type=gen_key_type,
            gen_key_size=gen_key_size,
            gen_curve=gen_curve,
        )
        logger.debug(f"📜🔑🚀 Generation config: {conf}")

        # Generate base certificate and private key
        base, private_key = CertificateBase.create(conf)

        # Create X.509 certificate
        x509_cert = create_x509_certificate(
            base=base,
            private_key=private_key,
            alt_names=alt_names or ["localhost"],
            is_ca=is_ca,
            is_client_cert=is_client_cert,
        )

        if x509_cert is None:
            raise CertificateError("Certificate object (_cert) is None after creation")

        # Serialize to PEM format
        cert_pem, key_pem = _serialize_to_pem(x509_cert, None)

        logger.debug("📜🔑✅ Generated cert and key")

        return base, x509_cert, private_key, cert_pem, key_pem

    except Exception as e:
        logger.error(
            f"📜❌ Failed to generate certificate. Error: {type(e).__name__}: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError(f"Failed to initialize certificate. Original error: {type(e).__name__}") from e


def x_generate_certificate__mutmut_65(
    common_name: str,
    organization_name: str,
    validity_days: int,
    key_type: str = DEFAULT_CERTIFICATE_KEY_TYPE,
    key_size: int = DEFAULT_RSA_KEY_SIZE,
    ecdsa_curve: str = DEFAULT_CERTIFICATE_CURVE,
    alt_names: list[str] | None = None,
    is_ca: bool = False,
    is_client_cert: bool = False,
) -> tuple[
    CertificateBase,
    x509.Certificate,
    KeyPair,
    str,
    str,
]:
    """Generate a new certificate with a keypair.

    Returns:
        Tuple of (CertificateBase, X509Certificate, private_key, cert_pem, key_pem)

    """
    try:
        logger.debug("📜🔑🚀 Generating new keypair")

        # Calculate validity period
        now = datetime.now(UTC)
        not_valid_before = now - timedelta(days=1)
        not_valid_after = now + timedelta(days=validity_days)

        # Parse and validate key type parameters
        gen_key_type, gen_key_size, gen_curve = _parse_key_type_and_params(key_type, key_size, ecdsa_curve)

        # Build certificate configuration
        conf = _build_certificate_config(
            common_name=common_name,
            organization_name=organization_name,
            not_valid_before=not_valid_before,
            not_valid_after=not_valid_after,
            alt_names=alt_names,
            gen_key_type=gen_key_type,
            gen_key_size=gen_key_size,
            gen_curve=gen_curve,
        )
        logger.debug(f"📜🔑🚀 Generation config: {conf}")

        # Generate base certificate and private key
        base, private_key = CertificateBase.create(conf)

        # Create X.509 certificate
        x509_cert = create_x509_certificate(
            base=base,
            private_key=private_key,
            alt_names=alt_names or ["localhost"],
            is_ca=is_ca,
            is_client_cert=is_client_cert,
        )

        if x509_cert is None:
            raise CertificateError("Certificate object (_cert) is None after creation")

        # Serialize to PEM format
        cert_pem, key_pem = _serialize_to_pem(private_key)

        logger.debug("📜🔑✅ Generated cert and key")

        return base, x509_cert, private_key, cert_pem, key_pem

    except Exception as e:
        logger.error(
            f"📜❌ Failed to generate certificate. Error: {type(e).__name__}: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError(f"Failed to initialize certificate. Original error: {type(e).__name__}") from e


def x_generate_certificate__mutmut_66(
    common_name: str,
    organization_name: str,
    validity_days: int,
    key_type: str = DEFAULT_CERTIFICATE_KEY_TYPE,
    key_size: int = DEFAULT_RSA_KEY_SIZE,
    ecdsa_curve: str = DEFAULT_CERTIFICATE_CURVE,
    alt_names: list[str] | None = None,
    is_ca: bool = False,
    is_client_cert: bool = False,
) -> tuple[
    CertificateBase,
    x509.Certificate,
    KeyPair,
    str,
    str,
]:
    """Generate a new certificate with a keypair.

    Returns:
        Tuple of (CertificateBase, X509Certificate, private_key, cert_pem, key_pem)

    """
    try:
        logger.debug("📜🔑🚀 Generating new keypair")

        # Calculate validity period
        now = datetime.now(UTC)
        not_valid_before = now - timedelta(days=1)
        not_valid_after = now + timedelta(days=validity_days)

        # Parse and validate key type parameters
        gen_key_type, gen_key_size, gen_curve = _parse_key_type_and_params(key_type, key_size, ecdsa_curve)

        # Build certificate configuration
        conf = _build_certificate_config(
            common_name=common_name,
            organization_name=organization_name,
            not_valid_before=not_valid_before,
            not_valid_after=not_valid_after,
            alt_names=alt_names,
            gen_key_type=gen_key_type,
            gen_key_size=gen_key_size,
            gen_curve=gen_curve,
        )
        logger.debug(f"📜🔑🚀 Generation config: {conf}")

        # Generate base certificate and private key
        base, private_key = CertificateBase.create(conf)

        # Create X.509 certificate
        x509_cert = create_x509_certificate(
            base=base,
            private_key=private_key,
            alt_names=alt_names or ["localhost"],
            is_ca=is_ca,
            is_client_cert=is_client_cert,
        )

        if x509_cert is None:
            raise CertificateError("Certificate object (_cert) is None after creation")

        # Serialize to PEM format
        cert_pem, key_pem = _serialize_to_pem(
            x509_cert,
        )

        logger.debug("📜🔑✅ Generated cert and key")

        return base, x509_cert, private_key, cert_pem, key_pem

    except Exception as e:
        logger.error(
            f"📜❌ Failed to generate certificate. Error: {type(e).__name__}: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError(f"Failed to initialize certificate. Original error: {type(e).__name__}") from e


def x_generate_certificate__mutmut_67(
    common_name: str,
    organization_name: str,
    validity_days: int,
    key_type: str = DEFAULT_CERTIFICATE_KEY_TYPE,
    key_size: int = DEFAULT_RSA_KEY_SIZE,
    ecdsa_curve: str = DEFAULT_CERTIFICATE_CURVE,
    alt_names: list[str] | None = None,
    is_ca: bool = False,
    is_client_cert: bool = False,
) -> tuple[
    CertificateBase,
    x509.Certificate,
    KeyPair,
    str,
    str,
]:
    """Generate a new certificate with a keypair.

    Returns:
        Tuple of (CertificateBase, X509Certificate, private_key, cert_pem, key_pem)

    """
    try:
        logger.debug("📜🔑🚀 Generating new keypair")

        # Calculate validity period
        now = datetime.now(UTC)
        not_valid_before = now - timedelta(days=1)
        not_valid_after = now + timedelta(days=validity_days)

        # Parse and validate key type parameters
        gen_key_type, gen_key_size, gen_curve = _parse_key_type_and_params(key_type, key_size, ecdsa_curve)

        # Build certificate configuration
        conf = _build_certificate_config(
            common_name=common_name,
            organization_name=organization_name,
            not_valid_before=not_valid_before,
            not_valid_after=not_valid_after,
            alt_names=alt_names,
            gen_key_type=gen_key_type,
            gen_key_size=gen_key_size,
            gen_curve=gen_curve,
        )
        logger.debug(f"📜🔑🚀 Generation config: {conf}")

        # Generate base certificate and private key
        base, private_key = CertificateBase.create(conf)

        # Create X.509 certificate
        x509_cert = create_x509_certificate(
            base=base,
            private_key=private_key,
            alt_names=alt_names or ["localhost"],
            is_ca=is_ca,
            is_client_cert=is_client_cert,
        )

        if x509_cert is None:
            raise CertificateError("Certificate object (_cert) is None after creation")

        # Serialize to PEM format
        cert_pem, key_pem = _serialize_to_pem(x509_cert, private_key)

        logger.debug(None)

        return base, x509_cert, private_key, cert_pem, key_pem

    except Exception as e:
        logger.error(
            f"📜❌ Failed to generate certificate. Error: {type(e).__name__}: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError(f"Failed to initialize certificate. Original error: {type(e).__name__}") from e


def x_generate_certificate__mutmut_68(
    common_name: str,
    organization_name: str,
    validity_days: int,
    key_type: str = DEFAULT_CERTIFICATE_KEY_TYPE,
    key_size: int = DEFAULT_RSA_KEY_SIZE,
    ecdsa_curve: str = DEFAULT_CERTIFICATE_CURVE,
    alt_names: list[str] | None = None,
    is_ca: bool = False,
    is_client_cert: bool = False,
) -> tuple[
    CertificateBase,
    x509.Certificate,
    KeyPair,
    str,
    str,
]:
    """Generate a new certificate with a keypair.

    Returns:
        Tuple of (CertificateBase, X509Certificate, private_key, cert_pem, key_pem)

    """
    try:
        logger.debug("📜🔑🚀 Generating new keypair")

        # Calculate validity period
        now = datetime.now(UTC)
        not_valid_before = now - timedelta(days=1)
        not_valid_after = now + timedelta(days=validity_days)

        # Parse and validate key type parameters
        gen_key_type, gen_key_size, gen_curve = _parse_key_type_and_params(key_type, key_size, ecdsa_curve)

        # Build certificate configuration
        conf = _build_certificate_config(
            common_name=common_name,
            organization_name=organization_name,
            not_valid_before=not_valid_before,
            not_valid_after=not_valid_after,
            alt_names=alt_names,
            gen_key_type=gen_key_type,
            gen_key_size=gen_key_size,
            gen_curve=gen_curve,
        )
        logger.debug(f"📜🔑🚀 Generation config: {conf}")

        # Generate base certificate and private key
        base, private_key = CertificateBase.create(conf)

        # Create X.509 certificate
        x509_cert = create_x509_certificate(
            base=base,
            private_key=private_key,
            alt_names=alt_names or ["localhost"],
            is_ca=is_ca,
            is_client_cert=is_client_cert,
        )

        if x509_cert is None:
            raise CertificateError("Certificate object (_cert) is None after creation")

        # Serialize to PEM format
        cert_pem, key_pem = _serialize_to_pem(x509_cert, private_key)

        logger.debug("XX📜🔑✅ Generated cert and keyXX")

        return base, x509_cert, private_key, cert_pem, key_pem

    except Exception as e:
        logger.error(
            f"📜❌ Failed to generate certificate. Error: {type(e).__name__}: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError(f"Failed to initialize certificate. Original error: {type(e).__name__}") from e


def x_generate_certificate__mutmut_69(
    common_name: str,
    organization_name: str,
    validity_days: int,
    key_type: str = DEFAULT_CERTIFICATE_KEY_TYPE,
    key_size: int = DEFAULT_RSA_KEY_SIZE,
    ecdsa_curve: str = DEFAULT_CERTIFICATE_CURVE,
    alt_names: list[str] | None = None,
    is_ca: bool = False,
    is_client_cert: bool = False,
) -> tuple[
    CertificateBase,
    x509.Certificate,
    KeyPair,
    str,
    str,
]:
    """Generate a new certificate with a keypair.

    Returns:
        Tuple of (CertificateBase, X509Certificate, private_key, cert_pem, key_pem)

    """
    try:
        logger.debug("📜🔑🚀 Generating new keypair")

        # Calculate validity period
        now = datetime.now(UTC)
        not_valid_before = now - timedelta(days=1)
        not_valid_after = now + timedelta(days=validity_days)

        # Parse and validate key type parameters
        gen_key_type, gen_key_size, gen_curve = _parse_key_type_and_params(key_type, key_size, ecdsa_curve)

        # Build certificate configuration
        conf = _build_certificate_config(
            common_name=common_name,
            organization_name=organization_name,
            not_valid_before=not_valid_before,
            not_valid_after=not_valid_after,
            alt_names=alt_names,
            gen_key_type=gen_key_type,
            gen_key_size=gen_key_size,
            gen_curve=gen_curve,
        )
        logger.debug(f"📜🔑🚀 Generation config: {conf}")

        # Generate base certificate and private key
        base, private_key = CertificateBase.create(conf)

        # Create X.509 certificate
        x509_cert = create_x509_certificate(
            base=base,
            private_key=private_key,
            alt_names=alt_names or ["localhost"],
            is_ca=is_ca,
            is_client_cert=is_client_cert,
        )

        if x509_cert is None:
            raise CertificateError("Certificate object (_cert) is None after creation")

        # Serialize to PEM format
        cert_pem, key_pem = _serialize_to_pem(x509_cert, private_key)

        logger.debug("📜🔑✅ generated cert and key")

        return base, x509_cert, private_key, cert_pem, key_pem

    except Exception as e:
        logger.error(
            f"📜❌ Failed to generate certificate. Error: {type(e).__name__}: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError(f"Failed to initialize certificate. Original error: {type(e).__name__}") from e


def x_generate_certificate__mutmut_70(
    common_name: str,
    organization_name: str,
    validity_days: int,
    key_type: str = DEFAULT_CERTIFICATE_KEY_TYPE,
    key_size: int = DEFAULT_RSA_KEY_SIZE,
    ecdsa_curve: str = DEFAULT_CERTIFICATE_CURVE,
    alt_names: list[str] | None = None,
    is_ca: bool = False,
    is_client_cert: bool = False,
) -> tuple[
    CertificateBase,
    x509.Certificate,
    KeyPair,
    str,
    str,
]:
    """Generate a new certificate with a keypair.

    Returns:
        Tuple of (CertificateBase, X509Certificate, private_key, cert_pem, key_pem)

    """
    try:
        logger.debug("📜🔑🚀 Generating new keypair")

        # Calculate validity period
        now = datetime.now(UTC)
        not_valid_before = now - timedelta(days=1)
        not_valid_after = now + timedelta(days=validity_days)

        # Parse and validate key type parameters
        gen_key_type, gen_key_size, gen_curve = _parse_key_type_and_params(key_type, key_size, ecdsa_curve)

        # Build certificate configuration
        conf = _build_certificate_config(
            common_name=common_name,
            organization_name=organization_name,
            not_valid_before=not_valid_before,
            not_valid_after=not_valid_after,
            alt_names=alt_names,
            gen_key_type=gen_key_type,
            gen_key_size=gen_key_size,
            gen_curve=gen_curve,
        )
        logger.debug(f"📜🔑🚀 Generation config: {conf}")

        # Generate base certificate and private key
        base, private_key = CertificateBase.create(conf)

        # Create X.509 certificate
        x509_cert = create_x509_certificate(
            base=base,
            private_key=private_key,
            alt_names=alt_names or ["localhost"],
            is_ca=is_ca,
            is_client_cert=is_client_cert,
        )

        if x509_cert is None:
            raise CertificateError("Certificate object (_cert) is None after creation")

        # Serialize to PEM format
        cert_pem, key_pem = _serialize_to_pem(x509_cert, private_key)

        logger.debug("📜🔑✅ GENERATED CERT AND KEY")

        return base, x509_cert, private_key, cert_pem, key_pem

    except Exception as e:
        logger.error(
            f"📜❌ Failed to generate certificate. Error: {type(e).__name__}: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError(f"Failed to initialize certificate. Original error: {type(e).__name__}") from e


def x_generate_certificate__mutmut_71(
    common_name: str,
    organization_name: str,
    validity_days: int,
    key_type: str = DEFAULT_CERTIFICATE_KEY_TYPE,
    key_size: int = DEFAULT_RSA_KEY_SIZE,
    ecdsa_curve: str = DEFAULT_CERTIFICATE_CURVE,
    alt_names: list[str] | None = None,
    is_ca: bool = False,
    is_client_cert: bool = False,
) -> tuple[
    CertificateBase,
    x509.Certificate,
    KeyPair,
    str,
    str,
]:
    """Generate a new certificate with a keypair.

    Returns:
        Tuple of (CertificateBase, X509Certificate, private_key, cert_pem, key_pem)

    """
    try:
        logger.debug("📜🔑🚀 Generating new keypair")

        # Calculate validity period
        now = datetime.now(UTC)
        not_valid_before = now - timedelta(days=1)
        not_valid_after = now + timedelta(days=validity_days)

        # Parse and validate key type parameters
        gen_key_type, gen_key_size, gen_curve = _parse_key_type_and_params(key_type, key_size, ecdsa_curve)

        # Build certificate configuration
        conf = _build_certificate_config(
            common_name=common_name,
            organization_name=organization_name,
            not_valid_before=not_valid_before,
            not_valid_after=not_valid_after,
            alt_names=alt_names,
            gen_key_type=gen_key_type,
            gen_key_size=gen_key_size,
            gen_curve=gen_curve,
        )
        logger.debug(f"📜🔑🚀 Generation config: {conf}")

        # Generate base certificate and private key
        base, private_key = CertificateBase.create(conf)

        # Create X.509 certificate
        x509_cert = create_x509_certificate(
            base=base,
            private_key=private_key,
            alt_names=alt_names or ["localhost"],
            is_ca=is_ca,
            is_client_cert=is_client_cert,
        )

        if x509_cert is None:
            raise CertificateError("Certificate object (_cert) is None after creation")

        # Serialize to PEM format
        cert_pem, key_pem = _serialize_to_pem(x509_cert, private_key)

        logger.debug("📜🔑✅ Generated cert and key")

        return base, x509_cert, private_key, cert_pem, key_pem

    except Exception as e:
        logger.error(
            None,
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError(f"Failed to initialize certificate. Original error: {type(e).__name__}") from e


def x_generate_certificate__mutmut_72(
    common_name: str,
    organization_name: str,
    validity_days: int,
    key_type: str = DEFAULT_CERTIFICATE_KEY_TYPE,
    key_size: int = DEFAULT_RSA_KEY_SIZE,
    ecdsa_curve: str = DEFAULT_CERTIFICATE_CURVE,
    alt_names: list[str] | None = None,
    is_ca: bool = False,
    is_client_cert: bool = False,
) -> tuple[
    CertificateBase,
    x509.Certificate,
    KeyPair,
    str,
    str,
]:
    """Generate a new certificate with a keypair.

    Returns:
        Tuple of (CertificateBase, X509Certificate, private_key, cert_pem, key_pem)

    """
    try:
        logger.debug("📜🔑🚀 Generating new keypair")

        # Calculate validity period
        now = datetime.now(UTC)
        not_valid_before = now - timedelta(days=1)
        not_valid_after = now + timedelta(days=validity_days)

        # Parse and validate key type parameters
        gen_key_type, gen_key_size, gen_curve = _parse_key_type_and_params(key_type, key_size, ecdsa_curve)

        # Build certificate configuration
        conf = _build_certificate_config(
            common_name=common_name,
            organization_name=organization_name,
            not_valid_before=not_valid_before,
            not_valid_after=not_valid_after,
            alt_names=alt_names,
            gen_key_type=gen_key_type,
            gen_key_size=gen_key_size,
            gen_curve=gen_curve,
        )
        logger.debug(f"📜🔑🚀 Generation config: {conf}")

        # Generate base certificate and private key
        base, private_key = CertificateBase.create(conf)

        # Create X.509 certificate
        x509_cert = create_x509_certificate(
            base=base,
            private_key=private_key,
            alt_names=alt_names or ["localhost"],
            is_ca=is_ca,
            is_client_cert=is_client_cert,
        )

        if x509_cert is None:
            raise CertificateError("Certificate object (_cert) is None after creation")

        # Serialize to PEM format
        cert_pem, key_pem = _serialize_to_pem(x509_cert, private_key)

        logger.debug("📜🔑✅ Generated cert and key")

        return base, x509_cert, private_key, cert_pem, key_pem

    except Exception as e:
        logger.error(
            f"📜❌ Failed to generate certificate. Error: {type(e).__name__}: {e}",
            extra=None,
        )
        raise CertificateError(f"Failed to initialize certificate. Original error: {type(e).__name__}") from e


def x_generate_certificate__mutmut_73(
    common_name: str,
    organization_name: str,
    validity_days: int,
    key_type: str = DEFAULT_CERTIFICATE_KEY_TYPE,
    key_size: int = DEFAULT_RSA_KEY_SIZE,
    ecdsa_curve: str = DEFAULT_CERTIFICATE_CURVE,
    alt_names: list[str] | None = None,
    is_ca: bool = False,
    is_client_cert: bool = False,
) -> tuple[
    CertificateBase,
    x509.Certificate,
    KeyPair,
    str,
    str,
]:
    """Generate a new certificate with a keypair.

    Returns:
        Tuple of (CertificateBase, X509Certificate, private_key, cert_pem, key_pem)

    """
    try:
        logger.debug("📜🔑🚀 Generating new keypair")

        # Calculate validity period
        now = datetime.now(UTC)
        not_valid_before = now - timedelta(days=1)
        not_valid_after = now + timedelta(days=validity_days)

        # Parse and validate key type parameters
        gen_key_type, gen_key_size, gen_curve = _parse_key_type_and_params(key_type, key_size, ecdsa_curve)

        # Build certificate configuration
        conf = _build_certificate_config(
            common_name=common_name,
            organization_name=organization_name,
            not_valid_before=not_valid_before,
            not_valid_after=not_valid_after,
            alt_names=alt_names,
            gen_key_type=gen_key_type,
            gen_key_size=gen_key_size,
            gen_curve=gen_curve,
        )
        logger.debug(f"📜🔑🚀 Generation config: {conf}")

        # Generate base certificate and private key
        base, private_key = CertificateBase.create(conf)

        # Create X.509 certificate
        x509_cert = create_x509_certificate(
            base=base,
            private_key=private_key,
            alt_names=alt_names or ["localhost"],
            is_ca=is_ca,
            is_client_cert=is_client_cert,
        )

        if x509_cert is None:
            raise CertificateError("Certificate object (_cert) is None after creation")

        # Serialize to PEM format
        cert_pem, key_pem = _serialize_to_pem(x509_cert, private_key)

        logger.debug("📜🔑✅ Generated cert and key")

        return base, x509_cert, private_key, cert_pem, key_pem

    except Exception as e:
        logger.error(
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError(f"Failed to initialize certificate. Original error: {type(e).__name__}") from e


def x_generate_certificate__mutmut_74(
    common_name: str,
    organization_name: str,
    validity_days: int,
    key_type: str = DEFAULT_CERTIFICATE_KEY_TYPE,
    key_size: int = DEFAULT_RSA_KEY_SIZE,
    ecdsa_curve: str = DEFAULT_CERTIFICATE_CURVE,
    alt_names: list[str] | None = None,
    is_ca: bool = False,
    is_client_cert: bool = False,
) -> tuple[
    CertificateBase,
    x509.Certificate,
    KeyPair,
    str,
    str,
]:
    """Generate a new certificate with a keypair.

    Returns:
        Tuple of (CertificateBase, X509Certificate, private_key, cert_pem, key_pem)

    """
    try:
        logger.debug("📜🔑🚀 Generating new keypair")

        # Calculate validity period
        now = datetime.now(UTC)
        not_valid_before = now - timedelta(days=1)
        not_valid_after = now + timedelta(days=validity_days)

        # Parse and validate key type parameters
        gen_key_type, gen_key_size, gen_curve = _parse_key_type_and_params(key_type, key_size, ecdsa_curve)

        # Build certificate configuration
        conf = _build_certificate_config(
            common_name=common_name,
            organization_name=organization_name,
            not_valid_before=not_valid_before,
            not_valid_after=not_valid_after,
            alt_names=alt_names,
            gen_key_type=gen_key_type,
            gen_key_size=gen_key_size,
            gen_curve=gen_curve,
        )
        logger.debug(f"📜🔑🚀 Generation config: {conf}")

        # Generate base certificate and private key
        base, private_key = CertificateBase.create(conf)

        # Create X.509 certificate
        x509_cert = create_x509_certificate(
            base=base,
            private_key=private_key,
            alt_names=alt_names or ["localhost"],
            is_ca=is_ca,
            is_client_cert=is_client_cert,
        )

        if x509_cert is None:
            raise CertificateError("Certificate object (_cert) is None after creation")

        # Serialize to PEM format
        cert_pem, key_pem = _serialize_to_pem(x509_cert, private_key)

        logger.debug("📜🔑✅ Generated cert and key")

        return base, x509_cert, private_key, cert_pem, key_pem

    except Exception as e:
        logger.error(
            f"📜❌ Failed to generate certificate. Error: {type(e).__name__}: {e}",
        )
        raise CertificateError(f"Failed to initialize certificate. Original error: {type(e).__name__}") from e


def x_generate_certificate__mutmut_75(
    common_name: str,
    organization_name: str,
    validity_days: int,
    key_type: str = DEFAULT_CERTIFICATE_KEY_TYPE,
    key_size: int = DEFAULT_RSA_KEY_SIZE,
    ecdsa_curve: str = DEFAULT_CERTIFICATE_CURVE,
    alt_names: list[str] | None = None,
    is_ca: bool = False,
    is_client_cert: bool = False,
) -> tuple[
    CertificateBase,
    x509.Certificate,
    KeyPair,
    str,
    str,
]:
    """Generate a new certificate with a keypair.

    Returns:
        Tuple of (CertificateBase, X509Certificate, private_key, cert_pem, key_pem)

    """
    try:
        logger.debug("📜🔑🚀 Generating new keypair")

        # Calculate validity period
        now = datetime.now(UTC)
        not_valid_before = now - timedelta(days=1)
        not_valid_after = now + timedelta(days=validity_days)

        # Parse and validate key type parameters
        gen_key_type, gen_key_size, gen_curve = _parse_key_type_and_params(key_type, key_size, ecdsa_curve)

        # Build certificate configuration
        conf = _build_certificate_config(
            common_name=common_name,
            organization_name=organization_name,
            not_valid_before=not_valid_before,
            not_valid_after=not_valid_after,
            alt_names=alt_names,
            gen_key_type=gen_key_type,
            gen_key_size=gen_key_size,
            gen_curve=gen_curve,
        )
        logger.debug(f"📜🔑🚀 Generation config: {conf}")

        # Generate base certificate and private key
        base, private_key = CertificateBase.create(conf)

        # Create X.509 certificate
        x509_cert = create_x509_certificate(
            base=base,
            private_key=private_key,
            alt_names=alt_names or ["localhost"],
            is_ca=is_ca,
            is_client_cert=is_client_cert,
        )

        if x509_cert is None:
            raise CertificateError("Certificate object (_cert) is None after creation")

        # Serialize to PEM format
        cert_pem, key_pem = _serialize_to_pem(x509_cert, private_key)

        logger.debug("📜🔑✅ Generated cert and key")

        return base, x509_cert, private_key, cert_pem, key_pem

    except Exception as e:
        logger.error(
            f"📜❌ Failed to generate certificate. Error: {type(None).__name__}: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError(f"Failed to initialize certificate. Original error: {type(e).__name__}") from e


def x_generate_certificate__mutmut_76(
    common_name: str,
    organization_name: str,
    validity_days: int,
    key_type: str = DEFAULT_CERTIFICATE_KEY_TYPE,
    key_size: int = DEFAULT_RSA_KEY_SIZE,
    ecdsa_curve: str = DEFAULT_CERTIFICATE_CURVE,
    alt_names: list[str] | None = None,
    is_ca: bool = False,
    is_client_cert: bool = False,
) -> tuple[
    CertificateBase,
    x509.Certificate,
    KeyPair,
    str,
    str,
]:
    """Generate a new certificate with a keypair.

    Returns:
        Tuple of (CertificateBase, X509Certificate, private_key, cert_pem, key_pem)

    """
    try:
        logger.debug("📜🔑🚀 Generating new keypair")

        # Calculate validity period
        now = datetime.now(UTC)
        not_valid_before = now - timedelta(days=1)
        not_valid_after = now + timedelta(days=validity_days)

        # Parse and validate key type parameters
        gen_key_type, gen_key_size, gen_curve = _parse_key_type_and_params(key_type, key_size, ecdsa_curve)

        # Build certificate configuration
        conf = _build_certificate_config(
            common_name=common_name,
            organization_name=organization_name,
            not_valid_before=not_valid_before,
            not_valid_after=not_valid_after,
            alt_names=alt_names,
            gen_key_type=gen_key_type,
            gen_key_size=gen_key_size,
            gen_curve=gen_curve,
        )
        logger.debug(f"📜🔑🚀 Generation config: {conf}")

        # Generate base certificate and private key
        base, private_key = CertificateBase.create(conf)

        # Create X.509 certificate
        x509_cert = create_x509_certificate(
            base=base,
            private_key=private_key,
            alt_names=alt_names or ["localhost"],
            is_ca=is_ca,
            is_client_cert=is_client_cert,
        )

        if x509_cert is None:
            raise CertificateError("Certificate object (_cert) is None after creation")

        # Serialize to PEM format
        cert_pem, key_pem = _serialize_to_pem(x509_cert, private_key)

        logger.debug("📜🔑✅ Generated cert and key")

        return base, x509_cert, private_key, cert_pem, key_pem

    except Exception as e:
        logger.error(
            f"📜❌ Failed to generate certificate. Error: {type(e).__name__}: {e}",
            extra={"XXerrorXX": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError(f"Failed to initialize certificate. Original error: {type(e).__name__}") from e


def x_generate_certificate__mutmut_77(
    common_name: str,
    organization_name: str,
    validity_days: int,
    key_type: str = DEFAULT_CERTIFICATE_KEY_TYPE,
    key_size: int = DEFAULT_RSA_KEY_SIZE,
    ecdsa_curve: str = DEFAULT_CERTIFICATE_CURVE,
    alt_names: list[str] | None = None,
    is_ca: bool = False,
    is_client_cert: bool = False,
) -> tuple[
    CertificateBase,
    x509.Certificate,
    KeyPair,
    str,
    str,
]:
    """Generate a new certificate with a keypair.

    Returns:
        Tuple of (CertificateBase, X509Certificate, private_key, cert_pem, key_pem)

    """
    try:
        logger.debug("📜🔑🚀 Generating new keypair")

        # Calculate validity period
        now = datetime.now(UTC)
        not_valid_before = now - timedelta(days=1)
        not_valid_after = now + timedelta(days=validity_days)

        # Parse and validate key type parameters
        gen_key_type, gen_key_size, gen_curve = _parse_key_type_and_params(key_type, key_size, ecdsa_curve)

        # Build certificate configuration
        conf = _build_certificate_config(
            common_name=common_name,
            organization_name=organization_name,
            not_valid_before=not_valid_before,
            not_valid_after=not_valid_after,
            alt_names=alt_names,
            gen_key_type=gen_key_type,
            gen_key_size=gen_key_size,
            gen_curve=gen_curve,
        )
        logger.debug(f"📜🔑🚀 Generation config: {conf}")

        # Generate base certificate and private key
        base, private_key = CertificateBase.create(conf)

        # Create X.509 certificate
        x509_cert = create_x509_certificate(
            base=base,
            private_key=private_key,
            alt_names=alt_names or ["localhost"],
            is_ca=is_ca,
            is_client_cert=is_client_cert,
        )

        if x509_cert is None:
            raise CertificateError("Certificate object (_cert) is None after creation")

        # Serialize to PEM format
        cert_pem, key_pem = _serialize_to_pem(x509_cert, private_key)

        logger.debug("📜🔑✅ Generated cert and key")

        return base, x509_cert, private_key, cert_pem, key_pem

    except Exception as e:
        logger.error(
            f"📜❌ Failed to generate certificate. Error: {type(e).__name__}: {e}",
            extra={"ERROR": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError(f"Failed to initialize certificate. Original error: {type(e).__name__}") from e


def x_generate_certificate__mutmut_78(
    common_name: str,
    organization_name: str,
    validity_days: int,
    key_type: str = DEFAULT_CERTIFICATE_KEY_TYPE,
    key_size: int = DEFAULT_RSA_KEY_SIZE,
    ecdsa_curve: str = DEFAULT_CERTIFICATE_CURVE,
    alt_names: list[str] | None = None,
    is_ca: bool = False,
    is_client_cert: bool = False,
) -> tuple[
    CertificateBase,
    x509.Certificate,
    KeyPair,
    str,
    str,
]:
    """Generate a new certificate with a keypair.

    Returns:
        Tuple of (CertificateBase, X509Certificate, private_key, cert_pem, key_pem)

    """
    try:
        logger.debug("📜🔑🚀 Generating new keypair")

        # Calculate validity period
        now = datetime.now(UTC)
        not_valid_before = now - timedelta(days=1)
        not_valid_after = now + timedelta(days=validity_days)

        # Parse and validate key type parameters
        gen_key_type, gen_key_size, gen_curve = _parse_key_type_and_params(key_type, key_size, ecdsa_curve)

        # Build certificate configuration
        conf = _build_certificate_config(
            common_name=common_name,
            organization_name=organization_name,
            not_valid_before=not_valid_before,
            not_valid_after=not_valid_after,
            alt_names=alt_names,
            gen_key_type=gen_key_type,
            gen_key_size=gen_key_size,
            gen_curve=gen_curve,
        )
        logger.debug(f"📜🔑🚀 Generation config: {conf}")

        # Generate base certificate and private key
        base, private_key = CertificateBase.create(conf)

        # Create X.509 certificate
        x509_cert = create_x509_certificate(
            base=base,
            private_key=private_key,
            alt_names=alt_names or ["localhost"],
            is_ca=is_ca,
            is_client_cert=is_client_cert,
        )

        if x509_cert is None:
            raise CertificateError("Certificate object (_cert) is None after creation")

        # Serialize to PEM format
        cert_pem, key_pem = _serialize_to_pem(x509_cert, private_key)

        logger.debug("📜🔑✅ Generated cert and key")

        return base, x509_cert, private_key, cert_pem, key_pem

    except Exception as e:
        logger.error(
            f"📜❌ Failed to generate certificate. Error: {type(e).__name__}: {e}",
            extra={"error": str(None), "trace": traceback.format_exc()},
        )
        raise CertificateError(f"Failed to initialize certificate. Original error: {type(e).__name__}") from e


def x_generate_certificate__mutmut_79(
    common_name: str,
    organization_name: str,
    validity_days: int,
    key_type: str = DEFAULT_CERTIFICATE_KEY_TYPE,
    key_size: int = DEFAULT_RSA_KEY_SIZE,
    ecdsa_curve: str = DEFAULT_CERTIFICATE_CURVE,
    alt_names: list[str] | None = None,
    is_ca: bool = False,
    is_client_cert: bool = False,
) -> tuple[
    CertificateBase,
    x509.Certificate,
    KeyPair,
    str,
    str,
]:
    """Generate a new certificate with a keypair.

    Returns:
        Tuple of (CertificateBase, X509Certificate, private_key, cert_pem, key_pem)

    """
    try:
        logger.debug("📜🔑🚀 Generating new keypair")

        # Calculate validity period
        now = datetime.now(UTC)
        not_valid_before = now - timedelta(days=1)
        not_valid_after = now + timedelta(days=validity_days)

        # Parse and validate key type parameters
        gen_key_type, gen_key_size, gen_curve = _parse_key_type_and_params(key_type, key_size, ecdsa_curve)

        # Build certificate configuration
        conf = _build_certificate_config(
            common_name=common_name,
            organization_name=organization_name,
            not_valid_before=not_valid_before,
            not_valid_after=not_valid_after,
            alt_names=alt_names,
            gen_key_type=gen_key_type,
            gen_key_size=gen_key_size,
            gen_curve=gen_curve,
        )
        logger.debug(f"📜🔑🚀 Generation config: {conf}")

        # Generate base certificate and private key
        base, private_key = CertificateBase.create(conf)

        # Create X.509 certificate
        x509_cert = create_x509_certificate(
            base=base,
            private_key=private_key,
            alt_names=alt_names or ["localhost"],
            is_ca=is_ca,
            is_client_cert=is_client_cert,
        )

        if x509_cert is None:
            raise CertificateError("Certificate object (_cert) is None after creation")

        # Serialize to PEM format
        cert_pem, key_pem = _serialize_to_pem(x509_cert, private_key)

        logger.debug("📜🔑✅ Generated cert and key")

        return base, x509_cert, private_key, cert_pem, key_pem

    except Exception as e:
        logger.error(
            f"📜❌ Failed to generate certificate. Error: {type(e).__name__}: {e}",
            extra={"error": str(e), "XXtraceXX": traceback.format_exc()},
        )
        raise CertificateError(f"Failed to initialize certificate. Original error: {type(e).__name__}") from e


def x_generate_certificate__mutmut_80(
    common_name: str,
    organization_name: str,
    validity_days: int,
    key_type: str = DEFAULT_CERTIFICATE_KEY_TYPE,
    key_size: int = DEFAULT_RSA_KEY_SIZE,
    ecdsa_curve: str = DEFAULT_CERTIFICATE_CURVE,
    alt_names: list[str] | None = None,
    is_ca: bool = False,
    is_client_cert: bool = False,
) -> tuple[
    CertificateBase,
    x509.Certificate,
    KeyPair,
    str,
    str,
]:
    """Generate a new certificate with a keypair.

    Returns:
        Tuple of (CertificateBase, X509Certificate, private_key, cert_pem, key_pem)

    """
    try:
        logger.debug("📜🔑🚀 Generating new keypair")

        # Calculate validity period
        now = datetime.now(UTC)
        not_valid_before = now - timedelta(days=1)
        not_valid_after = now + timedelta(days=validity_days)

        # Parse and validate key type parameters
        gen_key_type, gen_key_size, gen_curve = _parse_key_type_and_params(key_type, key_size, ecdsa_curve)

        # Build certificate configuration
        conf = _build_certificate_config(
            common_name=common_name,
            organization_name=organization_name,
            not_valid_before=not_valid_before,
            not_valid_after=not_valid_after,
            alt_names=alt_names,
            gen_key_type=gen_key_type,
            gen_key_size=gen_key_size,
            gen_curve=gen_curve,
        )
        logger.debug(f"📜🔑🚀 Generation config: {conf}")

        # Generate base certificate and private key
        base, private_key = CertificateBase.create(conf)

        # Create X.509 certificate
        x509_cert = create_x509_certificate(
            base=base,
            private_key=private_key,
            alt_names=alt_names or ["localhost"],
            is_ca=is_ca,
            is_client_cert=is_client_cert,
        )

        if x509_cert is None:
            raise CertificateError("Certificate object (_cert) is None after creation")

        # Serialize to PEM format
        cert_pem, key_pem = _serialize_to_pem(x509_cert, private_key)

        logger.debug("📜🔑✅ Generated cert and key")

        return base, x509_cert, private_key, cert_pem, key_pem

    except Exception as e:
        logger.error(
            f"📜❌ Failed to generate certificate. Error: {type(e).__name__}: {e}",
            extra={"error": str(e), "TRACE": traceback.format_exc()},
        )
        raise CertificateError(f"Failed to initialize certificate. Original error: {type(e).__name__}") from e


def x_generate_certificate__mutmut_81(
    common_name: str,
    organization_name: str,
    validity_days: int,
    key_type: str = DEFAULT_CERTIFICATE_KEY_TYPE,
    key_size: int = DEFAULT_RSA_KEY_SIZE,
    ecdsa_curve: str = DEFAULT_CERTIFICATE_CURVE,
    alt_names: list[str] | None = None,
    is_ca: bool = False,
    is_client_cert: bool = False,
) -> tuple[
    CertificateBase,
    x509.Certificate,
    KeyPair,
    str,
    str,
]:
    """Generate a new certificate with a keypair.

    Returns:
        Tuple of (CertificateBase, X509Certificate, private_key, cert_pem, key_pem)

    """
    try:
        logger.debug("📜🔑🚀 Generating new keypair")

        # Calculate validity period
        now = datetime.now(UTC)
        not_valid_before = now - timedelta(days=1)
        not_valid_after = now + timedelta(days=validity_days)

        # Parse and validate key type parameters
        gen_key_type, gen_key_size, gen_curve = _parse_key_type_and_params(key_type, key_size, ecdsa_curve)

        # Build certificate configuration
        conf = _build_certificate_config(
            common_name=common_name,
            organization_name=organization_name,
            not_valid_before=not_valid_before,
            not_valid_after=not_valid_after,
            alt_names=alt_names,
            gen_key_type=gen_key_type,
            gen_key_size=gen_key_size,
            gen_curve=gen_curve,
        )
        logger.debug(f"📜🔑🚀 Generation config: {conf}")

        # Generate base certificate and private key
        base, private_key = CertificateBase.create(conf)

        # Create X.509 certificate
        x509_cert = create_x509_certificate(
            base=base,
            private_key=private_key,
            alt_names=alt_names or ["localhost"],
            is_ca=is_ca,
            is_client_cert=is_client_cert,
        )

        if x509_cert is None:
            raise CertificateError("Certificate object (_cert) is None after creation")

        # Serialize to PEM format
        cert_pem, key_pem = _serialize_to_pem(x509_cert, private_key)

        logger.debug("📜🔑✅ Generated cert and key")

        return base, x509_cert, private_key, cert_pem, key_pem

    except Exception as e:
        logger.error(
            f"📜❌ Failed to generate certificate. Error: {type(e).__name__}: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError(None) from e


def x_generate_certificate__mutmut_82(
    common_name: str,
    organization_name: str,
    validity_days: int,
    key_type: str = DEFAULT_CERTIFICATE_KEY_TYPE,
    key_size: int = DEFAULT_RSA_KEY_SIZE,
    ecdsa_curve: str = DEFAULT_CERTIFICATE_CURVE,
    alt_names: list[str] | None = None,
    is_ca: bool = False,
    is_client_cert: bool = False,
) -> tuple[
    CertificateBase,
    x509.Certificate,
    KeyPair,
    str,
    str,
]:
    """Generate a new certificate with a keypair.

    Returns:
        Tuple of (CertificateBase, X509Certificate, private_key, cert_pem, key_pem)

    """
    try:
        logger.debug("📜🔑🚀 Generating new keypair")

        # Calculate validity period
        now = datetime.now(UTC)
        not_valid_before = now - timedelta(days=1)
        not_valid_after = now + timedelta(days=validity_days)

        # Parse and validate key type parameters
        gen_key_type, gen_key_size, gen_curve = _parse_key_type_and_params(key_type, key_size, ecdsa_curve)

        # Build certificate configuration
        conf = _build_certificate_config(
            common_name=common_name,
            organization_name=organization_name,
            not_valid_before=not_valid_before,
            not_valid_after=not_valid_after,
            alt_names=alt_names,
            gen_key_type=gen_key_type,
            gen_key_size=gen_key_size,
            gen_curve=gen_curve,
        )
        logger.debug(f"📜🔑🚀 Generation config: {conf}")

        # Generate base certificate and private key
        base, private_key = CertificateBase.create(conf)

        # Create X.509 certificate
        x509_cert = create_x509_certificate(
            base=base,
            private_key=private_key,
            alt_names=alt_names or ["localhost"],
            is_ca=is_ca,
            is_client_cert=is_client_cert,
        )

        if x509_cert is None:
            raise CertificateError("Certificate object (_cert) is None after creation")

        # Serialize to PEM format
        cert_pem, key_pem = _serialize_to_pem(x509_cert, private_key)

        logger.debug("📜🔑✅ Generated cert and key")

        return base, x509_cert, private_key, cert_pem, key_pem

    except Exception as e:
        logger.error(
            f"📜❌ Failed to generate certificate. Error: {type(e).__name__}: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError(
            f"Failed to initialize certificate. Original error: {type(None).__name__}"
        ) from e


x_generate_certificate__mutmut_mutants: ClassVar[MutantDict] = {
    "x_generate_certificate__mutmut_1": x_generate_certificate__mutmut_1,
    "x_generate_certificate__mutmut_2": x_generate_certificate__mutmut_2,
    "x_generate_certificate__mutmut_3": x_generate_certificate__mutmut_3,
    "x_generate_certificate__mutmut_4": x_generate_certificate__mutmut_4,
    "x_generate_certificate__mutmut_5": x_generate_certificate__mutmut_5,
    "x_generate_certificate__mutmut_6": x_generate_certificate__mutmut_6,
    "x_generate_certificate__mutmut_7": x_generate_certificate__mutmut_7,
    "x_generate_certificate__mutmut_8": x_generate_certificate__mutmut_8,
    "x_generate_certificate__mutmut_9": x_generate_certificate__mutmut_9,
    "x_generate_certificate__mutmut_10": x_generate_certificate__mutmut_10,
    "x_generate_certificate__mutmut_11": x_generate_certificate__mutmut_11,
    "x_generate_certificate__mutmut_12": x_generate_certificate__mutmut_12,
    "x_generate_certificate__mutmut_13": x_generate_certificate__mutmut_13,
    "x_generate_certificate__mutmut_14": x_generate_certificate__mutmut_14,
    "x_generate_certificate__mutmut_15": x_generate_certificate__mutmut_15,
    "x_generate_certificate__mutmut_16": x_generate_certificate__mutmut_16,
    "x_generate_certificate__mutmut_17": x_generate_certificate__mutmut_17,
    "x_generate_certificate__mutmut_18": x_generate_certificate__mutmut_18,
    "x_generate_certificate__mutmut_19": x_generate_certificate__mutmut_19,
    "x_generate_certificate__mutmut_20": x_generate_certificate__mutmut_20,
    "x_generate_certificate__mutmut_21": x_generate_certificate__mutmut_21,
    "x_generate_certificate__mutmut_22": x_generate_certificate__mutmut_22,
    "x_generate_certificate__mutmut_23": x_generate_certificate__mutmut_23,
    "x_generate_certificate__mutmut_24": x_generate_certificate__mutmut_24,
    "x_generate_certificate__mutmut_25": x_generate_certificate__mutmut_25,
    "x_generate_certificate__mutmut_26": x_generate_certificate__mutmut_26,
    "x_generate_certificate__mutmut_27": x_generate_certificate__mutmut_27,
    "x_generate_certificate__mutmut_28": x_generate_certificate__mutmut_28,
    "x_generate_certificate__mutmut_29": x_generate_certificate__mutmut_29,
    "x_generate_certificate__mutmut_30": x_generate_certificate__mutmut_30,
    "x_generate_certificate__mutmut_31": x_generate_certificate__mutmut_31,
    "x_generate_certificate__mutmut_32": x_generate_certificate__mutmut_32,
    "x_generate_certificate__mutmut_33": x_generate_certificate__mutmut_33,
    "x_generate_certificate__mutmut_34": x_generate_certificate__mutmut_34,
    "x_generate_certificate__mutmut_35": x_generate_certificate__mutmut_35,
    "x_generate_certificate__mutmut_36": x_generate_certificate__mutmut_36,
    "x_generate_certificate__mutmut_37": x_generate_certificate__mutmut_37,
    "x_generate_certificate__mutmut_38": x_generate_certificate__mutmut_38,
    "x_generate_certificate__mutmut_39": x_generate_certificate__mutmut_39,
    "x_generate_certificate__mutmut_40": x_generate_certificate__mutmut_40,
    "x_generate_certificate__mutmut_41": x_generate_certificate__mutmut_41,
    "x_generate_certificate__mutmut_42": x_generate_certificate__mutmut_42,
    "x_generate_certificate__mutmut_43": x_generate_certificate__mutmut_43,
    "x_generate_certificate__mutmut_44": x_generate_certificate__mutmut_44,
    "x_generate_certificate__mutmut_45": x_generate_certificate__mutmut_45,
    "x_generate_certificate__mutmut_46": x_generate_certificate__mutmut_46,
    "x_generate_certificate__mutmut_47": x_generate_certificate__mutmut_47,
    "x_generate_certificate__mutmut_48": x_generate_certificate__mutmut_48,
    "x_generate_certificate__mutmut_49": x_generate_certificate__mutmut_49,
    "x_generate_certificate__mutmut_50": x_generate_certificate__mutmut_50,
    "x_generate_certificate__mutmut_51": x_generate_certificate__mutmut_51,
    "x_generate_certificate__mutmut_52": x_generate_certificate__mutmut_52,
    "x_generate_certificate__mutmut_53": x_generate_certificate__mutmut_53,
    "x_generate_certificate__mutmut_54": x_generate_certificate__mutmut_54,
    "x_generate_certificate__mutmut_55": x_generate_certificate__mutmut_55,
    "x_generate_certificate__mutmut_56": x_generate_certificate__mutmut_56,
    "x_generate_certificate__mutmut_57": x_generate_certificate__mutmut_57,
    "x_generate_certificate__mutmut_58": x_generate_certificate__mutmut_58,
    "x_generate_certificate__mutmut_59": x_generate_certificate__mutmut_59,
    "x_generate_certificate__mutmut_60": x_generate_certificate__mutmut_60,
    "x_generate_certificate__mutmut_61": x_generate_certificate__mutmut_61,
    "x_generate_certificate__mutmut_62": x_generate_certificate__mutmut_62,
    "x_generate_certificate__mutmut_63": x_generate_certificate__mutmut_63,
    "x_generate_certificate__mutmut_64": x_generate_certificate__mutmut_64,
    "x_generate_certificate__mutmut_65": x_generate_certificate__mutmut_65,
    "x_generate_certificate__mutmut_66": x_generate_certificate__mutmut_66,
    "x_generate_certificate__mutmut_67": x_generate_certificate__mutmut_67,
    "x_generate_certificate__mutmut_68": x_generate_certificate__mutmut_68,
    "x_generate_certificate__mutmut_69": x_generate_certificate__mutmut_69,
    "x_generate_certificate__mutmut_70": x_generate_certificate__mutmut_70,
    "x_generate_certificate__mutmut_71": x_generate_certificate__mutmut_71,
    "x_generate_certificate__mutmut_72": x_generate_certificate__mutmut_72,
    "x_generate_certificate__mutmut_73": x_generate_certificate__mutmut_73,
    "x_generate_certificate__mutmut_74": x_generate_certificate__mutmut_74,
    "x_generate_certificate__mutmut_75": x_generate_certificate__mutmut_75,
    "x_generate_certificate__mutmut_76": x_generate_certificate__mutmut_76,
    "x_generate_certificate__mutmut_77": x_generate_certificate__mutmut_77,
    "x_generate_certificate__mutmut_78": x_generate_certificate__mutmut_78,
    "x_generate_certificate__mutmut_79": x_generate_certificate__mutmut_79,
    "x_generate_certificate__mutmut_80": x_generate_certificate__mutmut_80,
    "x_generate_certificate__mutmut_81": x_generate_certificate__mutmut_81,
    "x_generate_certificate__mutmut_82": x_generate_certificate__mutmut_82,
}


def generate_certificate(*args, **kwargs):
    result = _mutmut_trampoline(
        x_generate_certificate__mutmut_orig, x_generate_certificate__mutmut_mutants, args, kwargs
    )
    return result


generate_certificate.__signature__ = _mutmut_signature(x_generate_certificate__mutmut_orig)
x_generate_certificate__mutmut_orig.__name__ = "x_generate_certificate"


# <3 🧱🤝🔒🪄
