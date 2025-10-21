# provide/foundation/integrations/openobserve/auth.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import base64

from provide.foundation.integrations.openobserve.exceptions import (
    OpenObserveAuthenticationError,
)

"""Authentication handling for OpenObserve."""
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


def x_encode_basic_auth__mutmut_orig(username: str, password: str) -> str:
    """Encode username and password for Basic authentication.

    Args:
        username: OpenObserve username
        password: OpenObserve password

    Returns:
        Base64 encoded auth string

    """
    credentials = f"{username}:{password}"
    encoded = base64.b64encode(credentials.encode()).decode()
    return encoded


def x_encode_basic_auth__mutmut_1(username: str, password: str) -> str:
    """Encode username and password for Basic authentication.

    Args:
        username: OpenObserve username
        password: OpenObserve password

    Returns:
        Base64 encoded auth string

    """
    credentials = None
    encoded = base64.b64encode(credentials.encode()).decode()
    return encoded


def x_encode_basic_auth__mutmut_2(username: str, password: str) -> str:
    """Encode username and password for Basic authentication.

    Args:
        username: OpenObserve username
        password: OpenObserve password

    Returns:
        Base64 encoded auth string

    """
    credentials = f"{username}:{password}"
    encoded = None
    return encoded


def x_encode_basic_auth__mutmut_3(username: str, password: str) -> str:
    """Encode username and password for Basic authentication.

    Args:
        username: OpenObserve username
        password: OpenObserve password

    Returns:
        Base64 encoded auth string

    """
    credentials = f"{username}:{password}"
    encoded = base64.b64encode(None).decode()
    return encoded

x_encode_basic_auth__mutmut_mutants : ClassVar[MutantDict] = {
'x_encode_basic_auth__mutmut_1': x_encode_basic_auth__mutmut_1, 
    'x_encode_basic_auth__mutmut_2': x_encode_basic_auth__mutmut_2, 
    'x_encode_basic_auth__mutmut_3': x_encode_basic_auth__mutmut_3
}

def encode_basic_auth(*args, **kwargs):
    result = _mutmut_trampoline(x_encode_basic_auth__mutmut_orig, x_encode_basic_auth__mutmut_mutants, args, kwargs)
    return result 

encode_basic_auth.__signature__ = _mutmut_signature(x_encode_basic_auth__mutmut_orig)
x_encode_basic_auth__mutmut_orig.__name__ = 'x_encode_basic_auth'


def x_get_auth_headers__mutmut_orig(username: str | None, password: str | None) -> dict[str, str]:
    """Get authentication headers for OpenObserve API.

    Args:
        username: OpenObserve username
        password: OpenObserve password

    Returns:
        Dictionary with Authorization header

    Raises:
        OpenObserveAuthenticationError: If credentials are missing

    """
    if not username or not password:
        raise OpenObserveAuthenticationError(
            "OpenObserve credentials not configured. "
            "Set OPENOBSERVE_USER and OPENOBSERVE_PASSWORD environment variables.",
        )

    auth_token = encode_basic_auth(username, password)
    return {
        "Authorization": f"Basic {auth_token}",
        "Content-Type": "application/json",
    }


def x_get_auth_headers__mutmut_1(username: str | None, password: str | None) -> dict[str, str]:
    """Get authentication headers for OpenObserve API.

    Args:
        username: OpenObserve username
        password: OpenObserve password

    Returns:
        Dictionary with Authorization header

    Raises:
        OpenObserveAuthenticationError: If credentials are missing

    """
    if not username and not password:
        raise OpenObserveAuthenticationError(
            "OpenObserve credentials not configured. "
            "Set OPENOBSERVE_USER and OPENOBSERVE_PASSWORD environment variables.",
        )

    auth_token = encode_basic_auth(username, password)
    return {
        "Authorization": f"Basic {auth_token}",
        "Content-Type": "application/json",
    }


def x_get_auth_headers__mutmut_2(username: str | None, password: str | None) -> dict[str, str]:
    """Get authentication headers for OpenObserve API.

    Args:
        username: OpenObserve username
        password: OpenObserve password

    Returns:
        Dictionary with Authorization header

    Raises:
        OpenObserveAuthenticationError: If credentials are missing

    """
    if username or not password:
        raise OpenObserveAuthenticationError(
            "OpenObserve credentials not configured. "
            "Set OPENOBSERVE_USER and OPENOBSERVE_PASSWORD environment variables.",
        )

    auth_token = encode_basic_auth(username, password)
    return {
        "Authorization": f"Basic {auth_token}",
        "Content-Type": "application/json",
    }


def x_get_auth_headers__mutmut_3(username: str | None, password: str | None) -> dict[str, str]:
    """Get authentication headers for OpenObserve API.

    Args:
        username: OpenObserve username
        password: OpenObserve password

    Returns:
        Dictionary with Authorization header

    Raises:
        OpenObserveAuthenticationError: If credentials are missing

    """
    if not username or password:
        raise OpenObserveAuthenticationError(
            "OpenObserve credentials not configured. "
            "Set OPENOBSERVE_USER and OPENOBSERVE_PASSWORD environment variables.",
        )

    auth_token = encode_basic_auth(username, password)
    return {
        "Authorization": f"Basic {auth_token}",
        "Content-Type": "application/json",
    }


def x_get_auth_headers__mutmut_4(username: str | None, password: str | None) -> dict[str, str]:
    """Get authentication headers for OpenObserve API.

    Args:
        username: OpenObserve username
        password: OpenObserve password

    Returns:
        Dictionary with Authorization header

    Raises:
        OpenObserveAuthenticationError: If credentials are missing

    """
    if not username or not password:
        raise OpenObserveAuthenticationError(
            None,
        )

    auth_token = encode_basic_auth(username, password)
    return {
        "Authorization": f"Basic {auth_token}",
        "Content-Type": "application/json",
    }


def x_get_auth_headers__mutmut_5(username: str | None, password: str | None) -> dict[str, str]:
    """Get authentication headers for OpenObserve API.

    Args:
        username: OpenObserve username
        password: OpenObserve password

    Returns:
        Dictionary with Authorization header

    Raises:
        OpenObserveAuthenticationError: If credentials are missing

    """
    if not username or not password:
        raise OpenObserveAuthenticationError(
            "XXOpenObserve credentials not configured. XX"
            "Set OPENOBSERVE_USER and OPENOBSERVE_PASSWORD environment variables.",
        )

    auth_token = encode_basic_auth(username, password)
    return {
        "Authorization": f"Basic {auth_token}",
        "Content-Type": "application/json",
    }


def x_get_auth_headers__mutmut_6(username: str | None, password: str | None) -> dict[str, str]:
    """Get authentication headers for OpenObserve API.

    Args:
        username: OpenObserve username
        password: OpenObserve password

    Returns:
        Dictionary with Authorization header

    Raises:
        OpenObserveAuthenticationError: If credentials are missing

    """
    if not username or not password:
        raise OpenObserveAuthenticationError(
            "openobserve credentials not configured. "
            "Set OPENOBSERVE_USER and OPENOBSERVE_PASSWORD environment variables.",
        )

    auth_token = encode_basic_auth(username, password)
    return {
        "Authorization": f"Basic {auth_token}",
        "Content-Type": "application/json",
    }


def x_get_auth_headers__mutmut_7(username: str | None, password: str | None) -> dict[str, str]:
    """Get authentication headers for OpenObserve API.

    Args:
        username: OpenObserve username
        password: OpenObserve password

    Returns:
        Dictionary with Authorization header

    Raises:
        OpenObserveAuthenticationError: If credentials are missing

    """
    if not username or not password:
        raise OpenObserveAuthenticationError(
            "OPENOBSERVE CREDENTIALS NOT CONFIGURED. "
            "Set OPENOBSERVE_USER and OPENOBSERVE_PASSWORD environment variables.",
        )

    auth_token = encode_basic_auth(username, password)
    return {
        "Authorization": f"Basic {auth_token}",
        "Content-Type": "application/json",
    }


def x_get_auth_headers__mutmut_8(username: str | None, password: str | None) -> dict[str, str]:
    """Get authentication headers for OpenObserve API.

    Args:
        username: OpenObserve username
        password: OpenObserve password

    Returns:
        Dictionary with Authorization header

    Raises:
        OpenObserveAuthenticationError: If credentials are missing

    """
    if not username or not password:
        raise OpenObserveAuthenticationError(
            "OpenObserve credentials not configured. "
            "XXSet OPENOBSERVE_USER and OPENOBSERVE_PASSWORD environment variables.XX",
        )

    auth_token = encode_basic_auth(username, password)
    return {
        "Authorization": f"Basic {auth_token}",
        "Content-Type": "application/json",
    }


def x_get_auth_headers__mutmut_9(username: str | None, password: str | None) -> dict[str, str]:
    """Get authentication headers for OpenObserve API.

    Args:
        username: OpenObserve username
        password: OpenObserve password

    Returns:
        Dictionary with Authorization header

    Raises:
        OpenObserveAuthenticationError: If credentials are missing

    """
    if not username or not password:
        raise OpenObserveAuthenticationError(
            "OpenObserve credentials not configured. "
            "set openobserve_user and openobserve_password environment variables.",
        )

    auth_token = encode_basic_auth(username, password)
    return {
        "Authorization": f"Basic {auth_token}",
        "Content-Type": "application/json",
    }


def x_get_auth_headers__mutmut_10(username: str | None, password: str | None) -> dict[str, str]:
    """Get authentication headers for OpenObserve API.

    Args:
        username: OpenObserve username
        password: OpenObserve password

    Returns:
        Dictionary with Authorization header

    Raises:
        OpenObserveAuthenticationError: If credentials are missing

    """
    if not username or not password:
        raise OpenObserveAuthenticationError(
            "OpenObserve credentials not configured. "
            "SET OPENOBSERVE_USER AND OPENOBSERVE_PASSWORD ENVIRONMENT VARIABLES.",
        )

    auth_token = encode_basic_auth(username, password)
    return {
        "Authorization": f"Basic {auth_token}",
        "Content-Type": "application/json",
    }


def x_get_auth_headers__mutmut_11(username: str | None, password: str | None) -> dict[str, str]:
    """Get authentication headers for OpenObserve API.

    Args:
        username: OpenObserve username
        password: OpenObserve password

    Returns:
        Dictionary with Authorization header

    Raises:
        OpenObserveAuthenticationError: If credentials are missing

    """
    if not username or not password:
        raise OpenObserveAuthenticationError(
            "OpenObserve credentials not configured. "
            "Set OPENOBSERVE_USER and OPENOBSERVE_PASSWORD environment variables.",
        )

    auth_token = None
    return {
        "Authorization": f"Basic {auth_token}",
        "Content-Type": "application/json",
    }


def x_get_auth_headers__mutmut_12(username: str | None, password: str | None) -> dict[str, str]:
    """Get authentication headers for OpenObserve API.

    Args:
        username: OpenObserve username
        password: OpenObserve password

    Returns:
        Dictionary with Authorization header

    Raises:
        OpenObserveAuthenticationError: If credentials are missing

    """
    if not username or not password:
        raise OpenObserveAuthenticationError(
            "OpenObserve credentials not configured. "
            "Set OPENOBSERVE_USER and OPENOBSERVE_PASSWORD environment variables.",
        )

    auth_token = encode_basic_auth(None, password)
    return {
        "Authorization": f"Basic {auth_token}",
        "Content-Type": "application/json",
    }


def x_get_auth_headers__mutmut_13(username: str | None, password: str | None) -> dict[str, str]:
    """Get authentication headers for OpenObserve API.

    Args:
        username: OpenObserve username
        password: OpenObserve password

    Returns:
        Dictionary with Authorization header

    Raises:
        OpenObserveAuthenticationError: If credentials are missing

    """
    if not username or not password:
        raise OpenObserveAuthenticationError(
            "OpenObserve credentials not configured. "
            "Set OPENOBSERVE_USER and OPENOBSERVE_PASSWORD environment variables.",
        )

    auth_token = encode_basic_auth(username, None)
    return {
        "Authorization": f"Basic {auth_token}",
        "Content-Type": "application/json",
    }


def x_get_auth_headers__mutmut_14(username: str | None, password: str | None) -> dict[str, str]:
    """Get authentication headers for OpenObserve API.

    Args:
        username: OpenObserve username
        password: OpenObserve password

    Returns:
        Dictionary with Authorization header

    Raises:
        OpenObserveAuthenticationError: If credentials are missing

    """
    if not username or not password:
        raise OpenObserveAuthenticationError(
            "OpenObserve credentials not configured. "
            "Set OPENOBSERVE_USER and OPENOBSERVE_PASSWORD environment variables.",
        )

    auth_token = encode_basic_auth(password)
    return {
        "Authorization": f"Basic {auth_token}",
        "Content-Type": "application/json",
    }


def x_get_auth_headers__mutmut_15(username: str | None, password: str | None) -> dict[str, str]:
    """Get authentication headers for OpenObserve API.

    Args:
        username: OpenObserve username
        password: OpenObserve password

    Returns:
        Dictionary with Authorization header

    Raises:
        OpenObserveAuthenticationError: If credentials are missing

    """
    if not username or not password:
        raise OpenObserveAuthenticationError(
            "OpenObserve credentials not configured. "
            "Set OPENOBSERVE_USER and OPENOBSERVE_PASSWORD environment variables.",
        )

    auth_token = encode_basic_auth(username, )
    return {
        "Authorization": f"Basic {auth_token}",
        "Content-Type": "application/json",
    }


def x_get_auth_headers__mutmut_16(username: str | None, password: str | None) -> dict[str, str]:
    """Get authentication headers for OpenObserve API.

    Args:
        username: OpenObserve username
        password: OpenObserve password

    Returns:
        Dictionary with Authorization header

    Raises:
        OpenObserveAuthenticationError: If credentials are missing

    """
    if not username or not password:
        raise OpenObserveAuthenticationError(
            "OpenObserve credentials not configured. "
            "Set OPENOBSERVE_USER and OPENOBSERVE_PASSWORD environment variables.",
        )

    auth_token = encode_basic_auth(username, password)
    return {
        "XXAuthorizationXX": f"Basic {auth_token}",
        "Content-Type": "application/json",
    }


def x_get_auth_headers__mutmut_17(username: str | None, password: str | None) -> dict[str, str]:
    """Get authentication headers for OpenObserve API.

    Args:
        username: OpenObserve username
        password: OpenObserve password

    Returns:
        Dictionary with Authorization header

    Raises:
        OpenObserveAuthenticationError: If credentials are missing

    """
    if not username or not password:
        raise OpenObserveAuthenticationError(
            "OpenObserve credentials not configured. "
            "Set OPENOBSERVE_USER and OPENOBSERVE_PASSWORD environment variables.",
        )

    auth_token = encode_basic_auth(username, password)
    return {
        "authorization": f"Basic {auth_token}",
        "Content-Type": "application/json",
    }


def x_get_auth_headers__mutmut_18(username: str | None, password: str | None) -> dict[str, str]:
    """Get authentication headers for OpenObserve API.

    Args:
        username: OpenObserve username
        password: OpenObserve password

    Returns:
        Dictionary with Authorization header

    Raises:
        OpenObserveAuthenticationError: If credentials are missing

    """
    if not username or not password:
        raise OpenObserveAuthenticationError(
            "OpenObserve credentials not configured. "
            "Set OPENOBSERVE_USER and OPENOBSERVE_PASSWORD environment variables.",
        )

    auth_token = encode_basic_auth(username, password)
    return {
        "AUTHORIZATION": f"Basic {auth_token}",
        "Content-Type": "application/json",
    }


def x_get_auth_headers__mutmut_19(username: str | None, password: str | None) -> dict[str, str]:
    """Get authentication headers for OpenObserve API.

    Args:
        username: OpenObserve username
        password: OpenObserve password

    Returns:
        Dictionary with Authorization header

    Raises:
        OpenObserveAuthenticationError: If credentials are missing

    """
    if not username or not password:
        raise OpenObserveAuthenticationError(
            "OpenObserve credentials not configured. "
            "Set OPENOBSERVE_USER and OPENOBSERVE_PASSWORD environment variables.",
        )

    auth_token = encode_basic_auth(username, password)
    return {
        "Authorization": f"Basic {auth_token}",
        "XXContent-TypeXX": "application/json",
    }


def x_get_auth_headers__mutmut_20(username: str | None, password: str | None) -> dict[str, str]:
    """Get authentication headers for OpenObserve API.

    Args:
        username: OpenObserve username
        password: OpenObserve password

    Returns:
        Dictionary with Authorization header

    Raises:
        OpenObserveAuthenticationError: If credentials are missing

    """
    if not username or not password:
        raise OpenObserveAuthenticationError(
            "OpenObserve credentials not configured. "
            "Set OPENOBSERVE_USER and OPENOBSERVE_PASSWORD environment variables.",
        )

    auth_token = encode_basic_auth(username, password)
    return {
        "Authorization": f"Basic {auth_token}",
        "content-type": "application/json",
    }


def x_get_auth_headers__mutmut_21(username: str | None, password: str | None) -> dict[str, str]:
    """Get authentication headers for OpenObserve API.

    Args:
        username: OpenObserve username
        password: OpenObserve password

    Returns:
        Dictionary with Authorization header

    Raises:
        OpenObserveAuthenticationError: If credentials are missing

    """
    if not username or not password:
        raise OpenObserveAuthenticationError(
            "OpenObserve credentials not configured. "
            "Set OPENOBSERVE_USER and OPENOBSERVE_PASSWORD environment variables.",
        )

    auth_token = encode_basic_auth(username, password)
    return {
        "Authorization": f"Basic {auth_token}",
        "CONTENT-TYPE": "application/json",
    }


def x_get_auth_headers__mutmut_22(username: str | None, password: str | None) -> dict[str, str]:
    """Get authentication headers for OpenObserve API.

    Args:
        username: OpenObserve username
        password: OpenObserve password

    Returns:
        Dictionary with Authorization header

    Raises:
        OpenObserveAuthenticationError: If credentials are missing

    """
    if not username or not password:
        raise OpenObserveAuthenticationError(
            "OpenObserve credentials not configured. "
            "Set OPENOBSERVE_USER and OPENOBSERVE_PASSWORD environment variables.",
        )

    auth_token = encode_basic_auth(username, password)
    return {
        "Authorization": f"Basic {auth_token}",
        "Content-Type": "XXapplication/jsonXX",
    }


def x_get_auth_headers__mutmut_23(username: str | None, password: str | None) -> dict[str, str]:
    """Get authentication headers for OpenObserve API.

    Args:
        username: OpenObserve username
        password: OpenObserve password

    Returns:
        Dictionary with Authorization header

    Raises:
        OpenObserveAuthenticationError: If credentials are missing

    """
    if not username or not password:
        raise OpenObserveAuthenticationError(
            "OpenObserve credentials not configured. "
            "Set OPENOBSERVE_USER and OPENOBSERVE_PASSWORD environment variables.",
        )

    auth_token = encode_basic_auth(username, password)
    return {
        "Authorization": f"Basic {auth_token}",
        "Content-Type": "APPLICATION/JSON",
    }

x_get_auth_headers__mutmut_mutants : ClassVar[MutantDict] = {
'x_get_auth_headers__mutmut_1': x_get_auth_headers__mutmut_1, 
    'x_get_auth_headers__mutmut_2': x_get_auth_headers__mutmut_2, 
    'x_get_auth_headers__mutmut_3': x_get_auth_headers__mutmut_3, 
    'x_get_auth_headers__mutmut_4': x_get_auth_headers__mutmut_4, 
    'x_get_auth_headers__mutmut_5': x_get_auth_headers__mutmut_5, 
    'x_get_auth_headers__mutmut_6': x_get_auth_headers__mutmut_6, 
    'x_get_auth_headers__mutmut_7': x_get_auth_headers__mutmut_7, 
    'x_get_auth_headers__mutmut_8': x_get_auth_headers__mutmut_8, 
    'x_get_auth_headers__mutmut_9': x_get_auth_headers__mutmut_9, 
    'x_get_auth_headers__mutmut_10': x_get_auth_headers__mutmut_10, 
    'x_get_auth_headers__mutmut_11': x_get_auth_headers__mutmut_11, 
    'x_get_auth_headers__mutmut_12': x_get_auth_headers__mutmut_12, 
    'x_get_auth_headers__mutmut_13': x_get_auth_headers__mutmut_13, 
    'x_get_auth_headers__mutmut_14': x_get_auth_headers__mutmut_14, 
    'x_get_auth_headers__mutmut_15': x_get_auth_headers__mutmut_15, 
    'x_get_auth_headers__mutmut_16': x_get_auth_headers__mutmut_16, 
    'x_get_auth_headers__mutmut_17': x_get_auth_headers__mutmut_17, 
    'x_get_auth_headers__mutmut_18': x_get_auth_headers__mutmut_18, 
    'x_get_auth_headers__mutmut_19': x_get_auth_headers__mutmut_19, 
    'x_get_auth_headers__mutmut_20': x_get_auth_headers__mutmut_20, 
    'x_get_auth_headers__mutmut_21': x_get_auth_headers__mutmut_21, 
    'x_get_auth_headers__mutmut_22': x_get_auth_headers__mutmut_22, 
    'x_get_auth_headers__mutmut_23': x_get_auth_headers__mutmut_23
}

def get_auth_headers(*args, **kwargs):
    result = _mutmut_trampoline(x_get_auth_headers__mutmut_orig, x_get_auth_headers__mutmut_mutants, args, kwargs)
    return result 

get_auth_headers.__signature__ = _mutmut_signature(x_get_auth_headers__mutmut_orig)
x_get_auth_headers__mutmut_orig.__name__ = 'x_get_auth_headers'


def x_validate_credentials__mutmut_orig(username: str | None, password: str | None) -> tuple[str, str]:
    """Validate and return OpenObserve credentials.

    Args:
        username: OpenObserve username
        password: OpenObserve password

    Returns:
        Tuple of (username, password)

    Raises:
        OpenObserveAuthenticationError: If credentials are invalid

    """
    if not username:
        raise OpenObserveAuthenticationError("OpenObserve username is required")

    if not password:
        raise OpenObserveAuthenticationError("OpenObserve password is required")

    return username, password


def x_validate_credentials__mutmut_1(username: str | None, password: str | None) -> tuple[str, str]:
    """Validate and return OpenObserve credentials.

    Args:
        username: OpenObserve username
        password: OpenObserve password

    Returns:
        Tuple of (username, password)

    Raises:
        OpenObserveAuthenticationError: If credentials are invalid

    """
    if username:
        raise OpenObserveAuthenticationError("OpenObserve username is required")

    if not password:
        raise OpenObserveAuthenticationError("OpenObserve password is required")

    return username, password


def x_validate_credentials__mutmut_2(username: str | None, password: str | None) -> tuple[str, str]:
    """Validate and return OpenObserve credentials.

    Args:
        username: OpenObserve username
        password: OpenObserve password

    Returns:
        Tuple of (username, password)

    Raises:
        OpenObserveAuthenticationError: If credentials are invalid

    """
    if not username:
        raise OpenObserveAuthenticationError(None)

    if not password:
        raise OpenObserveAuthenticationError("OpenObserve password is required")

    return username, password


def x_validate_credentials__mutmut_3(username: str | None, password: str | None) -> tuple[str, str]:
    """Validate and return OpenObserve credentials.

    Args:
        username: OpenObserve username
        password: OpenObserve password

    Returns:
        Tuple of (username, password)

    Raises:
        OpenObserveAuthenticationError: If credentials are invalid

    """
    if not username:
        raise OpenObserveAuthenticationError("XXOpenObserve username is requiredXX")

    if not password:
        raise OpenObserveAuthenticationError("OpenObserve password is required")

    return username, password


def x_validate_credentials__mutmut_4(username: str | None, password: str | None) -> tuple[str, str]:
    """Validate and return OpenObserve credentials.

    Args:
        username: OpenObserve username
        password: OpenObserve password

    Returns:
        Tuple of (username, password)

    Raises:
        OpenObserveAuthenticationError: If credentials are invalid

    """
    if not username:
        raise OpenObserveAuthenticationError("openobserve username is required")

    if not password:
        raise OpenObserveAuthenticationError("OpenObserve password is required")

    return username, password


def x_validate_credentials__mutmut_5(username: str | None, password: str | None) -> tuple[str, str]:
    """Validate and return OpenObserve credentials.

    Args:
        username: OpenObserve username
        password: OpenObserve password

    Returns:
        Tuple of (username, password)

    Raises:
        OpenObserveAuthenticationError: If credentials are invalid

    """
    if not username:
        raise OpenObserveAuthenticationError("OPENOBSERVE USERNAME IS REQUIRED")

    if not password:
        raise OpenObserveAuthenticationError("OpenObserve password is required")

    return username, password


def x_validate_credentials__mutmut_6(username: str | None, password: str | None) -> tuple[str, str]:
    """Validate and return OpenObserve credentials.

    Args:
        username: OpenObserve username
        password: OpenObserve password

    Returns:
        Tuple of (username, password)

    Raises:
        OpenObserveAuthenticationError: If credentials are invalid

    """
    if not username:
        raise OpenObserveAuthenticationError("OpenObserve username is required")

    if password:
        raise OpenObserveAuthenticationError("OpenObserve password is required")

    return username, password


def x_validate_credentials__mutmut_7(username: str | None, password: str | None) -> tuple[str, str]:
    """Validate and return OpenObserve credentials.

    Args:
        username: OpenObserve username
        password: OpenObserve password

    Returns:
        Tuple of (username, password)

    Raises:
        OpenObserveAuthenticationError: If credentials are invalid

    """
    if not username:
        raise OpenObserveAuthenticationError("OpenObserve username is required")

    if not password:
        raise OpenObserveAuthenticationError(None)

    return username, password


def x_validate_credentials__mutmut_8(username: str | None, password: str | None) -> tuple[str, str]:
    """Validate and return OpenObserve credentials.

    Args:
        username: OpenObserve username
        password: OpenObserve password

    Returns:
        Tuple of (username, password)

    Raises:
        OpenObserveAuthenticationError: If credentials are invalid

    """
    if not username:
        raise OpenObserveAuthenticationError("OpenObserve username is required")

    if not password:
        raise OpenObserveAuthenticationError("XXOpenObserve password is requiredXX")

    return username, password


def x_validate_credentials__mutmut_9(username: str | None, password: str | None) -> tuple[str, str]:
    """Validate and return OpenObserve credentials.

    Args:
        username: OpenObserve username
        password: OpenObserve password

    Returns:
        Tuple of (username, password)

    Raises:
        OpenObserveAuthenticationError: If credentials are invalid

    """
    if not username:
        raise OpenObserveAuthenticationError("OpenObserve username is required")

    if not password:
        raise OpenObserveAuthenticationError("openobserve password is required")

    return username, password


def x_validate_credentials__mutmut_10(username: str | None, password: str | None) -> tuple[str, str]:
    """Validate and return OpenObserve credentials.

    Args:
        username: OpenObserve username
        password: OpenObserve password

    Returns:
        Tuple of (username, password)

    Raises:
        OpenObserveAuthenticationError: If credentials are invalid

    """
    if not username:
        raise OpenObserveAuthenticationError("OpenObserve username is required")

    if not password:
        raise OpenObserveAuthenticationError("OPENOBSERVE PASSWORD IS REQUIRED")

    return username, password

x_validate_credentials__mutmut_mutants : ClassVar[MutantDict] = {
'x_validate_credentials__mutmut_1': x_validate_credentials__mutmut_1, 
    'x_validate_credentials__mutmut_2': x_validate_credentials__mutmut_2, 
    'x_validate_credentials__mutmut_3': x_validate_credentials__mutmut_3, 
    'x_validate_credentials__mutmut_4': x_validate_credentials__mutmut_4, 
    'x_validate_credentials__mutmut_5': x_validate_credentials__mutmut_5, 
    'x_validate_credentials__mutmut_6': x_validate_credentials__mutmut_6, 
    'x_validate_credentials__mutmut_7': x_validate_credentials__mutmut_7, 
    'x_validate_credentials__mutmut_8': x_validate_credentials__mutmut_8, 
    'x_validate_credentials__mutmut_9': x_validate_credentials__mutmut_9, 
    'x_validate_credentials__mutmut_10': x_validate_credentials__mutmut_10
}

def validate_credentials(*args, **kwargs):
    result = _mutmut_trampoline(x_validate_credentials__mutmut_orig, x_validate_credentials__mutmut_mutants, args, kwargs)
    return result 

validate_credentials.__signature__ = _mutmut_signature(x_validate_credentials__mutmut_orig)
x_validate_credentials__mutmut_orig.__name__ = 'x_validate_credentials'


# <3 🧱🤝🔌🪄
