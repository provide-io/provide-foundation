# provide/foundation/security/sanitization.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from collections.abc import Mapping
from typing import Any
from urllib.parse import parse_qs, urlencode, urlparse, urlunparse

from provide.foundation.security.defaults import (
    DEFAULT_SENSITIVE_HEADERS,
    DEFAULT_SENSITIVE_PARAMS,
    REDACTED_VALUE,
)

"""Sanitization utilities for sensitive data redaction in logs and outputs."""
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


def x_sanitize_headers__mutmut_orig(
    headers: Mapping[str, Any],
    sensitive_headers: list[str] | None = None,
    redacted: str = REDACTED_VALUE,
) -> dict[str, Any]:
    """Sanitize sensitive headers for safe logging.

    Args:
        headers: Headers dictionary to sanitize
        sensitive_headers: List of header names to redact (case-insensitive)
        redacted: Replacement value for redacted headers

    Returns:
        Sanitized headers dictionary

    """
    if sensitive_headers is None:
        sensitive_headers = DEFAULT_SENSITIVE_HEADERS

    # Convert sensitive headers to lowercase for case-insensitive matching
    sensitive_lower = {h.lower() for h in sensitive_headers}

    sanitized = {}
    for key, value in headers.items():
        if key.lower() in sensitive_lower:
            sanitized[key] = redacted
        else:
            sanitized[key] = value

    return sanitized


def x_sanitize_headers__mutmut_1(
    headers: Mapping[str, Any],
    sensitive_headers: list[str] | None = None,
    redacted: str = REDACTED_VALUE,
) -> dict[str, Any]:
    """Sanitize sensitive headers for safe logging.

    Args:
        headers: Headers dictionary to sanitize
        sensitive_headers: List of header names to redact (case-insensitive)
        redacted: Replacement value for redacted headers

    Returns:
        Sanitized headers dictionary

    """
    if sensitive_headers is not None:
        sensitive_headers = DEFAULT_SENSITIVE_HEADERS

    # Convert sensitive headers to lowercase for case-insensitive matching
    sensitive_lower = {h.lower() for h in sensitive_headers}

    sanitized = {}
    for key, value in headers.items():
        if key.lower() in sensitive_lower:
            sanitized[key] = redacted
        else:
            sanitized[key] = value

    return sanitized


def x_sanitize_headers__mutmut_2(
    headers: Mapping[str, Any],
    sensitive_headers: list[str] | None = None,
    redacted: str = REDACTED_VALUE,
) -> dict[str, Any]:
    """Sanitize sensitive headers for safe logging.

    Args:
        headers: Headers dictionary to sanitize
        sensitive_headers: List of header names to redact (case-insensitive)
        redacted: Replacement value for redacted headers

    Returns:
        Sanitized headers dictionary

    """
    if sensitive_headers is None:
        sensitive_headers = None

    # Convert sensitive headers to lowercase for case-insensitive matching
    sensitive_lower = {h.lower() for h in sensitive_headers}

    sanitized = {}
    for key, value in headers.items():
        if key.lower() in sensitive_lower:
            sanitized[key] = redacted
        else:
            sanitized[key] = value

    return sanitized


def x_sanitize_headers__mutmut_3(
    headers: Mapping[str, Any],
    sensitive_headers: list[str] | None = None,
    redacted: str = REDACTED_VALUE,
) -> dict[str, Any]:
    """Sanitize sensitive headers for safe logging.

    Args:
        headers: Headers dictionary to sanitize
        sensitive_headers: List of header names to redact (case-insensitive)
        redacted: Replacement value for redacted headers

    Returns:
        Sanitized headers dictionary

    """
    if sensitive_headers is None:
        sensitive_headers = DEFAULT_SENSITIVE_HEADERS

    # Convert sensitive headers to lowercase for case-insensitive matching
    sensitive_lower = None

    sanitized = {}
    for key, value in headers.items():
        if key.lower() in sensitive_lower:
            sanitized[key] = redacted
        else:
            sanitized[key] = value

    return sanitized


def x_sanitize_headers__mutmut_4(
    headers: Mapping[str, Any],
    sensitive_headers: list[str] | None = None,
    redacted: str = REDACTED_VALUE,
) -> dict[str, Any]:
    """Sanitize sensitive headers for safe logging.

    Args:
        headers: Headers dictionary to sanitize
        sensitive_headers: List of header names to redact (case-insensitive)
        redacted: Replacement value for redacted headers

    Returns:
        Sanitized headers dictionary

    """
    if sensitive_headers is None:
        sensitive_headers = DEFAULT_SENSITIVE_HEADERS

    # Convert sensitive headers to lowercase for case-insensitive matching
    sensitive_lower = {h.upper() for h in sensitive_headers}

    sanitized = {}
    for key, value in headers.items():
        if key.lower() in sensitive_lower:
            sanitized[key] = redacted
        else:
            sanitized[key] = value

    return sanitized


def x_sanitize_headers__mutmut_5(
    headers: Mapping[str, Any],
    sensitive_headers: list[str] | None = None,
    redacted: str = REDACTED_VALUE,
) -> dict[str, Any]:
    """Sanitize sensitive headers for safe logging.

    Args:
        headers: Headers dictionary to sanitize
        sensitive_headers: List of header names to redact (case-insensitive)
        redacted: Replacement value for redacted headers

    Returns:
        Sanitized headers dictionary

    """
    if sensitive_headers is None:
        sensitive_headers = DEFAULT_SENSITIVE_HEADERS

    # Convert sensitive headers to lowercase for case-insensitive matching
    sensitive_lower = {h.lower() for h in sensitive_headers}

    sanitized = None
    for key, value in headers.items():
        if key.lower() in sensitive_lower:
            sanitized[key] = redacted
        else:
            sanitized[key] = value

    return sanitized


def x_sanitize_headers__mutmut_6(
    headers: Mapping[str, Any],
    sensitive_headers: list[str] | None = None,
    redacted: str = REDACTED_VALUE,
) -> dict[str, Any]:
    """Sanitize sensitive headers for safe logging.

    Args:
        headers: Headers dictionary to sanitize
        sensitive_headers: List of header names to redact (case-insensitive)
        redacted: Replacement value for redacted headers

    Returns:
        Sanitized headers dictionary

    """
    if sensitive_headers is None:
        sensitive_headers = DEFAULT_SENSITIVE_HEADERS

    # Convert sensitive headers to lowercase for case-insensitive matching
    sensitive_lower = {h.lower() for h in sensitive_headers}

    sanitized = {}
    for key, value in headers.items():
        if key.upper() in sensitive_lower:
            sanitized[key] = redacted
        else:
            sanitized[key] = value

    return sanitized


def x_sanitize_headers__mutmut_7(
    headers: Mapping[str, Any],
    sensitive_headers: list[str] | None = None,
    redacted: str = REDACTED_VALUE,
) -> dict[str, Any]:
    """Sanitize sensitive headers for safe logging.

    Args:
        headers: Headers dictionary to sanitize
        sensitive_headers: List of header names to redact (case-insensitive)
        redacted: Replacement value for redacted headers

    Returns:
        Sanitized headers dictionary

    """
    if sensitive_headers is None:
        sensitive_headers = DEFAULT_SENSITIVE_HEADERS

    # Convert sensitive headers to lowercase for case-insensitive matching
    sensitive_lower = {h.lower() for h in sensitive_headers}

    sanitized = {}
    for key, value in headers.items():
        if key.lower() not in sensitive_lower:
            sanitized[key] = redacted
        else:
            sanitized[key] = value

    return sanitized


def x_sanitize_headers__mutmut_8(
    headers: Mapping[str, Any],
    sensitive_headers: list[str] | None = None,
    redacted: str = REDACTED_VALUE,
) -> dict[str, Any]:
    """Sanitize sensitive headers for safe logging.

    Args:
        headers: Headers dictionary to sanitize
        sensitive_headers: List of header names to redact (case-insensitive)
        redacted: Replacement value for redacted headers

    Returns:
        Sanitized headers dictionary

    """
    if sensitive_headers is None:
        sensitive_headers = DEFAULT_SENSITIVE_HEADERS

    # Convert sensitive headers to lowercase for case-insensitive matching
    sensitive_lower = {h.lower() for h in sensitive_headers}

    sanitized = {}
    for key, value in headers.items():
        if key.lower() in sensitive_lower:
            sanitized[key] = None
        else:
            sanitized[key] = value

    return sanitized


def x_sanitize_headers__mutmut_9(
    headers: Mapping[str, Any],
    sensitive_headers: list[str] | None = None,
    redacted: str = REDACTED_VALUE,
) -> dict[str, Any]:
    """Sanitize sensitive headers for safe logging.

    Args:
        headers: Headers dictionary to sanitize
        sensitive_headers: List of header names to redact (case-insensitive)
        redacted: Replacement value for redacted headers

    Returns:
        Sanitized headers dictionary

    """
    if sensitive_headers is None:
        sensitive_headers = DEFAULT_SENSITIVE_HEADERS

    # Convert sensitive headers to lowercase for case-insensitive matching
    sensitive_lower = {h.lower() for h in sensitive_headers}

    sanitized = {}
    for key, value in headers.items():
        if key.lower() in sensitive_lower:
            sanitized[key] = redacted
        else:
            sanitized[key] = None

    return sanitized

x_sanitize_headers__mutmut_mutants : ClassVar[MutantDict] = {
'x_sanitize_headers__mutmut_1': x_sanitize_headers__mutmut_1, 
    'x_sanitize_headers__mutmut_2': x_sanitize_headers__mutmut_2, 
    'x_sanitize_headers__mutmut_3': x_sanitize_headers__mutmut_3, 
    'x_sanitize_headers__mutmut_4': x_sanitize_headers__mutmut_4, 
    'x_sanitize_headers__mutmut_5': x_sanitize_headers__mutmut_5, 
    'x_sanitize_headers__mutmut_6': x_sanitize_headers__mutmut_6, 
    'x_sanitize_headers__mutmut_7': x_sanitize_headers__mutmut_7, 
    'x_sanitize_headers__mutmut_8': x_sanitize_headers__mutmut_8, 
    'x_sanitize_headers__mutmut_9': x_sanitize_headers__mutmut_9
}

def sanitize_headers(*args, **kwargs):
    result = _mutmut_trampoline(x_sanitize_headers__mutmut_orig, x_sanitize_headers__mutmut_mutants, args, kwargs)
    return result 

sanitize_headers.__signature__ = _mutmut_signature(x_sanitize_headers__mutmut_orig)
x_sanitize_headers__mutmut_orig.__name__ = 'x_sanitize_headers'


def x_sanitize_uri__mutmut_orig(
    uri: str,
    sensitive_params: list[str] | None = None,
    redacted: str = REDACTED_VALUE,
) -> str:
    """Sanitize sensitive query parameters in URI for safe logging.

    Args:
        uri: URI to sanitize
        sensitive_params: List of parameter names to redact (case-insensitive)
        redacted: Replacement value for redacted parameters

    Returns:
        Sanitized URI string

    """
    if sensitive_params is None:
        sensitive_params = DEFAULT_SENSITIVE_PARAMS

    # Parse URI
    parsed = urlparse(uri)

    # If no query string, return as-is
    if not parsed.query:
        return uri

    # Parse query parameters
    params = parse_qs(parsed.query, keep_blank_values=True)

    # Convert sensitive params to lowercase for case-insensitive matching
    sensitive_lower = {p.lower() for p in sensitive_params}

    # Sanitize sensitive parameters
    sanitized_params = {}
    for key, values in params.items():
        if key.lower() in sensitive_lower:
            # Redact all values for this parameter
            sanitized_params[key] = [redacted] * len(values)
        else:
            sanitized_params[key] = values

    # Rebuild query string
    new_query = urlencode(sanitized_params, doseq=True)

    # Rebuild URI
    return urlunparse((parsed.scheme, parsed.netloc, parsed.path, parsed.params, new_query, parsed.fragment))


def x_sanitize_uri__mutmut_1(
    uri: str,
    sensitive_params: list[str] | None = None,
    redacted: str = REDACTED_VALUE,
) -> str:
    """Sanitize sensitive query parameters in URI for safe logging.

    Args:
        uri: URI to sanitize
        sensitive_params: List of parameter names to redact (case-insensitive)
        redacted: Replacement value for redacted parameters

    Returns:
        Sanitized URI string

    """
    if sensitive_params is not None:
        sensitive_params = DEFAULT_SENSITIVE_PARAMS

    # Parse URI
    parsed = urlparse(uri)

    # If no query string, return as-is
    if not parsed.query:
        return uri

    # Parse query parameters
    params = parse_qs(parsed.query, keep_blank_values=True)

    # Convert sensitive params to lowercase for case-insensitive matching
    sensitive_lower = {p.lower() for p in sensitive_params}

    # Sanitize sensitive parameters
    sanitized_params = {}
    for key, values in params.items():
        if key.lower() in sensitive_lower:
            # Redact all values for this parameter
            sanitized_params[key] = [redacted] * len(values)
        else:
            sanitized_params[key] = values

    # Rebuild query string
    new_query = urlencode(sanitized_params, doseq=True)

    # Rebuild URI
    return urlunparse((parsed.scheme, parsed.netloc, parsed.path, parsed.params, new_query, parsed.fragment))


def x_sanitize_uri__mutmut_2(
    uri: str,
    sensitive_params: list[str] | None = None,
    redacted: str = REDACTED_VALUE,
) -> str:
    """Sanitize sensitive query parameters in URI for safe logging.

    Args:
        uri: URI to sanitize
        sensitive_params: List of parameter names to redact (case-insensitive)
        redacted: Replacement value for redacted parameters

    Returns:
        Sanitized URI string

    """
    if sensitive_params is None:
        sensitive_params = None

    # Parse URI
    parsed = urlparse(uri)

    # If no query string, return as-is
    if not parsed.query:
        return uri

    # Parse query parameters
    params = parse_qs(parsed.query, keep_blank_values=True)

    # Convert sensitive params to lowercase for case-insensitive matching
    sensitive_lower = {p.lower() for p in sensitive_params}

    # Sanitize sensitive parameters
    sanitized_params = {}
    for key, values in params.items():
        if key.lower() in sensitive_lower:
            # Redact all values for this parameter
            sanitized_params[key] = [redacted] * len(values)
        else:
            sanitized_params[key] = values

    # Rebuild query string
    new_query = urlencode(sanitized_params, doseq=True)

    # Rebuild URI
    return urlunparse((parsed.scheme, parsed.netloc, parsed.path, parsed.params, new_query, parsed.fragment))


def x_sanitize_uri__mutmut_3(
    uri: str,
    sensitive_params: list[str] | None = None,
    redacted: str = REDACTED_VALUE,
) -> str:
    """Sanitize sensitive query parameters in URI for safe logging.

    Args:
        uri: URI to sanitize
        sensitive_params: List of parameter names to redact (case-insensitive)
        redacted: Replacement value for redacted parameters

    Returns:
        Sanitized URI string

    """
    if sensitive_params is None:
        sensitive_params = DEFAULT_SENSITIVE_PARAMS

    # Parse URI
    parsed = None

    # If no query string, return as-is
    if not parsed.query:
        return uri

    # Parse query parameters
    params = parse_qs(parsed.query, keep_blank_values=True)

    # Convert sensitive params to lowercase for case-insensitive matching
    sensitive_lower = {p.lower() for p in sensitive_params}

    # Sanitize sensitive parameters
    sanitized_params = {}
    for key, values in params.items():
        if key.lower() in sensitive_lower:
            # Redact all values for this parameter
            sanitized_params[key] = [redacted] * len(values)
        else:
            sanitized_params[key] = values

    # Rebuild query string
    new_query = urlencode(sanitized_params, doseq=True)

    # Rebuild URI
    return urlunparse((parsed.scheme, parsed.netloc, parsed.path, parsed.params, new_query, parsed.fragment))


def x_sanitize_uri__mutmut_4(
    uri: str,
    sensitive_params: list[str] | None = None,
    redacted: str = REDACTED_VALUE,
) -> str:
    """Sanitize sensitive query parameters in URI for safe logging.

    Args:
        uri: URI to sanitize
        sensitive_params: List of parameter names to redact (case-insensitive)
        redacted: Replacement value for redacted parameters

    Returns:
        Sanitized URI string

    """
    if sensitive_params is None:
        sensitive_params = DEFAULT_SENSITIVE_PARAMS

    # Parse URI
    parsed = urlparse(None)

    # If no query string, return as-is
    if not parsed.query:
        return uri

    # Parse query parameters
    params = parse_qs(parsed.query, keep_blank_values=True)

    # Convert sensitive params to lowercase for case-insensitive matching
    sensitive_lower = {p.lower() for p in sensitive_params}

    # Sanitize sensitive parameters
    sanitized_params = {}
    for key, values in params.items():
        if key.lower() in sensitive_lower:
            # Redact all values for this parameter
            sanitized_params[key] = [redacted] * len(values)
        else:
            sanitized_params[key] = values

    # Rebuild query string
    new_query = urlencode(sanitized_params, doseq=True)

    # Rebuild URI
    return urlunparse((parsed.scheme, parsed.netloc, parsed.path, parsed.params, new_query, parsed.fragment))


def x_sanitize_uri__mutmut_5(
    uri: str,
    sensitive_params: list[str] | None = None,
    redacted: str = REDACTED_VALUE,
) -> str:
    """Sanitize sensitive query parameters in URI for safe logging.

    Args:
        uri: URI to sanitize
        sensitive_params: List of parameter names to redact (case-insensitive)
        redacted: Replacement value for redacted parameters

    Returns:
        Sanitized URI string

    """
    if sensitive_params is None:
        sensitive_params = DEFAULT_SENSITIVE_PARAMS

    # Parse URI
    parsed = urlparse(uri)

    # If no query string, return as-is
    if parsed.query:
        return uri

    # Parse query parameters
    params = parse_qs(parsed.query, keep_blank_values=True)

    # Convert sensitive params to lowercase for case-insensitive matching
    sensitive_lower = {p.lower() for p in sensitive_params}

    # Sanitize sensitive parameters
    sanitized_params = {}
    for key, values in params.items():
        if key.lower() in sensitive_lower:
            # Redact all values for this parameter
            sanitized_params[key] = [redacted] * len(values)
        else:
            sanitized_params[key] = values

    # Rebuild query string
    new_query = urlencode(sanitized_params, doseq=True)

    # Rebuild URI
    return urlunparse((parsed.scheme, parsed.netloc, parsed.path, parsed.params, new_query, parsed.fragment))


def x_sanitize_uri__mutmut_6(
    uri: str,
    sensitive_params: list[str] | None = None,
    redacted: str = REDACTED_VALUE,
) -> str:
    """Sanitize sensitive query parameters in URI for safe logging.

    Args:
        uri: URI to sanitize
        sensitive_params: List of parameter names to redact (case-insensitive)
        redacted: Replacement value for redacted parameters

    Returns:
        Sanitized URI string

    """
    if sensitive_params is None:
        sensitive_params = DEFAULT_SENSITIVE_PARAMS

    # Parse URI
    parsed = urlparse(uri)

    # If no query string, return as-is
    if not parsed.query:
        return uri

    # Parse query parameters
    params = None

    # Convert sensitive params to lowercase for case-insensitive matching
    sensitive_lower = {p.lower() for p in sensitive_params}

    # Sanitize sensitive parameters
    sanitized_params = {}
    for key, values in params.items():
        if key.lower() in sensitive_lower:
            # Redact all values for this parameter
            sanitized_params[key] = [redacted] * len(values)
        else:
            sanitized_params[key] = values

    # Rebuild query string
    new_query = urlencode(sanitized_params, doseq=True)

    # Rebuild URI
    return urlunparse((parsed.scheme, parsed.netloc, parsed.path, parsed.params, new_query, parsed.fragment))


def x_sanitize_uri__mutmut_7(
    uri: str,
    sensitive_params: list[str] | None = None,
    redacted: str = REDACTED_VALUE,
) -> str:
    """Sanitize sensitive query parameters in URI for safe logging.

    Args:
        uri: URI to sanitize
        sensitive_params: List of parameter names to redact (case-insensitive)
        redacted: Replacement value for redacted parameters

    Returns:
        Sanitized URI string

    """
    if sensitive_params is None:
        sensitive_params = DEFAULT_SENSITIVE_PARAMS

    # Parse URI
    parsed = urlparse(uri)

    # If no query string, return as-is
    if not parsed.query:
        return uri

    # Parse query parameters
    params = parse_qs(None, keep_blank_values=True)

    # Convert sensitive params to lowercase for case-insensitive matching
    sensitive_lower = {p.lower() for p in sensitive_params}

    # Sanitize sensitive parameters
    sanitized_params = {}
    for key, values in params.items():
        if key.lower() in sensitive_lower:
            # Redact all values for this parameter
            sanitized_params[key] = [redacted] * len(values)
        else:
            sanitized_params[key] = values

    # Rebuild query string
    new_query = urlencode(sanitized_params, doseq=True)

    # Rebuild URI
    return urlunparse((parsed.scheme, parsed.netloc, parsed.path, parsed.params, new_query, parsed.fragment))


def x_sanitize_uri__mutmut_8(
    uri: str,
    sensitive_params: list[str] | None = None,
    redacted: str = REDACTED_VALUE,
) -> str:
    """Sanitize sensitive query parameters in URI for safe logging.

    Args:
        uri: URI to sanitize
        sensitive_params: List of parameter names to redact (case-insensitive)
        redacted: Replacement value for redacted parameters

    Returns:
        Sanitized URI string

    """
    if sensitive_params is None:
        sensitive_params = DEFAULT_SENSITIVE_PARAMS

    # Parse URI
    parsed = urlparse(uri)

    # If no query string, return as-is
    if not parsed.query:
        return uri

    # Parse query parameters
    params = parse_qs(parsed.query, keep_blank_values=None)

    # Convert sensitive params to lowercase for case-insensitive matching
    sensitive_lower = {p.lower() for p in sensitive_params}

    # Sanitize sensitive parameters
    sanitized_params = {}
    for key, values in params.items():
        if key.lower() in sensitive_lower:
            # Redact all values for this parameter
            sanitized_params[key] = [redacted] * len(values)
        else:
            sanitized_params[key] = values

    # Rebuild query string
    new_query = urlencode(sanitized_params, doseq=True)

    # Rebuild URI
    return urlunparse((parsed.scheme, parsed.netloc, parsed.path, parsed.params, new_query, parsed.fragment))


def x_sanitize_uri__mutmut_9(
    uri: str,
    sensitive_params: list[str] | None = None,
    redacted: str = REDACTED_VALUE,
) -> str:
    """Sanitize sensitive query parameters in URI for safe logging.

    Args:
        uri: URI to sanitize
        sensitive_params: List of parameter names to redact (case-insensitive)
        redacted: Replacement value for redacted parameters

    Returns:
        Sanitized URI string

    """
    if sensitive_params is None:
        sensitive_params = DEFAULT_SENSITIVE_PARAMS

    # Parse URI
    parsed = urlparse(uri)

    # If no query string, return as-is
    if not parsed.query:
        return uri

    # Parse query parameters
    params = parse_qs(keep_blank_values=True)

    # Convert sensitive params to lowercase for case-insensitive matching
    sensitive_lower = {p.lower() for p in sensitive_params}

    # Sanitize sensitive parameters
    sanitized_params = {}
    for key, values in params.items():
        if key.lower() in sensitive_lower:
            # Redact all values for this parameter
            sanitized_params[key] = [redacted] * len(values)
        else:
            sanitized_params[key] = values

    # Rebuild query string
    new_query = urlencode(sanitized_params, doseq=True)

    # Rebuild URI
    return urlunparse((parsed.scheme, parsed.netloc, parsed.path, parsed.params, new_query, parsed.fragment))


def x_sanitize_uri__mutmut_10(
    uri: str,
    sensitive_params: list[str] | None = None,
    redacted: str = REDACTED_VALUE,
) -> str:
    """Sanitize sensitive query parameters in URI for safe logging.

    Args:
        uri: URI to sanitize
        sensitive_params: List of parameter names to redact (case-insensitive)
        redacted: Replacement value for redacted parameters

    Returns:
        Sanitized URI string

    """
    if sensitive_params is None:
        sensitive_params = DEFAULT_SENSITIVE_PARAMS

    # Parse URI
    parsed = urlparse(uri)

    # If no query string, return as-is
    if not parsed.query:
        return uri

    # Parse query parameters
    params = parse_qs(parsed.query, )

    # Convert sensitive params to lowercase for case-insensitive matching
    sensitive_lower = {p.lower() for p in sensitive_params}

    # Sanitize sensitive parameters
    sanitized_params = {}
    for key, values in params.items():
        if key.lower() in sensitive_lower:
            # Redact all values for this parameter
            sanitized_params[key] = [redacted] * len(values)
        else:
            sanitized_params[key] = values

    # Rebuild query string
    new_query = urlencode(sanitized_params, doseq=True)

    # Rebuild URI
    return urlunparse((parsed.scheme, parsed.netloc, parsed.path, parsed.params, new_query, parsed.fragment))


def x_sanitize_uri__mutmut_11(
    uri: str,
    sensitive_params: list[str] | None = None,
    redacted: str = REDACTED_VALUE,
) -> str:
    """Sanitize sensitive query parameters in URI for safe logging.

    Args:
        uri: URI to sanitize
        sensitive_params: List of parameter names to redact (case-insensitive)
        redacted: Replacement value for redacted parameters

    Returns:
        Sanitized URI string

    """
    if sensitive_params is None:
        sensitive_params = DEFAULT_SENSITIVE_PARAMS

    # Parse URI
    parsed = urlparse(uri)

    # If no query string, return as-is
    if not parsed.query:
        return uri

    # Parse query parameters
    params = parse_qs(parsed.query, keep_blank_values=False)

    # Convert sensitive params to lowercase for case-insensitive matching
    sensitive_lower = {p.lower() for p in sensitive_params}

    # Sanitize sensitive parameters
    sanitized_params = {}
    for key, values in params.items():
        if key.lower() in sensitive_lower:
            # Redact all values for this parameter
            sanitized_params[key] = [redacted] * len(values)
        else:
            sanitized_params[key] = values

    # Rebuild query string
    new_query = urlencode(sanitized_params, doseq=True)

    # Rebuild URI
    return urlunparse((parsed.scheme, parsed.netloc, parsed.path, parsed.params, new_query, parsed.fragment))


def x_sanitize_uri__mutmut_12(
    uri: str,
    sensitive_params: list[str] | None = None,
    redacted: str = REDACTED_VALUE,
) -> str:
    """Sanitize sensitive query parameters in URI for safe logging.

    Args:
        uri: URI to sanitize
        sensitive_params: List of parameter names to redact (case-insensitive)
        redacted: Replacement value for redacted parameters

    Returns:
        Sanitized URI string

    """
    if sensitive_params is None:
        sensitive_params = DEFAULT_SENSITIVE_PARAMS

    # Parse URI
    parsed = urlparse(uri)

    # If no query string, return as-is
    if not parsed.query:
        return uri

    # Parse query parameters
    params = parse_qs(parsed.query, keep_blank_values=True)

    # Convert sensitive params to lowercase for case-insensitive matching
    sensitive_lower = None

    # Sanitize sensitive parameters
    sanitized_params = {}
    for key, values in params.items():
        if key.lower() in sensitive_lower:
            # Redact all values for this parameter
            sanitized_params[key] = [redacted] * len(values)
        else:
            sanitized_params[key] = values

    # Rebuild query string
    new_query = urlencode(sanitized_params, doseq=True)

    # Rebuild URI
    return urlunparse((parsed.scheme, parsed.netloc, parsed.path, parsed.params, new_query, parsed.fragment))


def x_sanitize_uri__mutmut_13(
    uri: str,
    sensitive_params: list[str] | None = None,
    redacted: str = REDACTED_VALUE,
) -> str:
    """Sanitize sensitive query parameters in URI for safe logging.

    Args:
        uri: URI to sanitize
        sensitive_params: List of parameter names to redact (case-insensitive)
        redacted: Replacement value for redacted parameters

    Returns:
        Sanitized URI string

    """
    if sensitive_params is None:
        sensitive_params = DEFAULT_SENSITIVE_PARAMS

    # Parse URI
    parsed = urlparse(uri)

    # If no query string, return as-is
    if not parsed.query:
        return uri

    # Parse query parameters
    params = parse_qs(parsed.query, keep_blank_values=True)

    # Convert sensitive params to lowercase for case-insensitive matching
    sensitive_lower = {p.upper() for p in sensitive_params}

    # Sanitize sensitive parameters
    sanitized_params = {}
    for key, values in params.items():
        if key.lower() in sensitive_lower:
            # Redact all values for this parameter
            sanitized_params[key] = [redacted] * len(values)
        else:
            sanitized_params[key] = values

    # Rebuild query string
    new_query = urlencode(sanitized_params, doseq=True)

    # Rebuild URI
    return urlunparse((parsed.scheme, parsed.netloc, parsed.path, parsed.params, new_query, parsed.fragment))


def x_sanitize_uri__mutmut_14(
    uri: str,
    sensitive_params: list[str] | None = None,
    redacted: str = REDACTED_VALUE,
) -> str:
    """Sanitize sensitive query parameters in URI for safe logging.

    Args:
        uri: URI to sanitize
        sensitive_params: List of parameter names to redact (case-insensitive)
        redacted: Replacement value for redacted parameters

    Returns:
        Sanitized URI string

    """
    if sensitive_params is None:
        sensitive_params = DEFAULT_SENSITIVE_PARAMS

    # Parse URI
    parsed = urlparse(uri)

    # If no query string, return as-is
    if not parsed.query:
        return uri

    # Parse query parameters
    params = parse_qs(parsed.query, keep_blank_values=True)

    # Convert sensitive params to lowercase for case-insensitive matching
    sensitive_lower = {p.lower() for p in sensitive_params}

    # Sanitize sensitive parameters
    sanitized_params = None
    for key, values in params.items():
        if key.lower() in sensitive_lower:
            # Redact all values for this parameter
            sanitized_params[key] = [redacted] * len(values)
        else:
            sanitized_params[key] = values

    # Rebuild query string
    new_query = urlencode(sanitized_params, doseq=True)

    # Rebuild URI
    return urlunparse((parsed.scheme, parsed.netloc, parsed.path, parsed.params, new_query, parsed.fragment))


def x_sanitize_uri__mutmut_15(
    uri: str,
    sensitive_params: list[str] | None = None,
    redacted: str = REDACTED_VALUE,
) -> str:
    """Sanitize sensitive query parameters in URI for safe logging.

    Args:
        uri: URI to sanitize
        sensitive_params: List of parameter names to redact (case-insensitive)
        redacted: Replacement value for redacted parameters

    Returns:
        Sanitized URI string

    """
    if sensitive_params is None:
        sensitive_params = DEFAULT_SENSITIVE_PARAMS

    # Parse URI
    parsed = urlparse(uri)

    # If no query string, return as-is
    if not parsed.query:
        return uri

    # Parse query parameters
    params = parse_qs(parsed.query, keep_blank_values=True)

    # Convert sensitive params to lowercase for case-insensitive matching
    sensitive_lower = {p.lower() for p in sensitive_params}

    # Sanitize sensitive parameters
    sanitized_params = {}
    for key, values in params.items():
        if key.upper() in sensitive_lower:
            # Redact all values for this parameter
            sanitized_params[key] = [redacted] * len(values)
        else:
            sanitized_params[key] = values

    # Rebuild query string
    new_query = urlencode(sanitized_params, doseq=True)

    # Rebuild URI
    return urlunparse((parsed.scheme, parsed.netloc, parsed.path, parsed.params, new_query, parsed.fragment))


def x_sanitize_uri__mutmut_16(
    uri: str,
    sensitive_params: list[str] | None = None,
    redacted: str = REDACTED_VALUE,
) -> str:
    """Sanitize sensitive query parameters in URI for safe logging.

    Args:
        uri: URI to sanitize
        sensitive_params: List of parameter names to redact (case-insensitive)
        redacted: Replacement value for redacted parameters

    Returns:
        Sanitized URI string

    """
    if sensitive_params is None:
        sensitive_params = DEFAULT_SENSITIVE_PARAMS

    # Parse URI
    parsed = urlparse(uri)

    # If no query string, return as-is
    if not parsed.query:
        return uri

    # Parse query parameters
    params = parse_qs(parsed.query, keep_blank_values=True)

    # Convert sensitive params to lowercase for case-insensitive matching
    sensitive_lower = {p.lower() for p in sensitive_params}

    # Sanitize sensitive parameters
    sanitized_params = {}
    for key, values in params.items():
        if key.lower() not in sensitive_lower:
            # Redact all values for this parameter
            sanitized_params[key] = [redacted] * len(values)
        else:
            sanitized_params[key] = values

    # Rebuild query string
    new_query = urlencode(sanitized_params, doseq=True)

    # Rebuild URI
    return urlunparse((parsed.scheme, parsed.netloc, parsed.path, parsed.params, new_query, parsed.fragment))


def x_sanitize_uri__mutmut_17(
    uri: str,
    sensitive_params: list[str] | None = None,
    redacted: str = REDACTED_VALUE,
) -> str:
    """Sanitize sensitive query parameters in URI for safe logging.

    Args:
        uri: URI to sanitize
        sensitive_params: List of parameter names to redact (case-insensitive)
        redacted: Replacement value for redacted parameters

    Returns:
        Sanitized URI string

    """
    if sensitive_params is None:
        sensitive_params = DEFAULT_SENSITIVE_PARAMS

    # Parse URI
    parsed = urlparse(uri)

    # If no query string, return as-is
    if not parsed.query:
        return uri

    # Parse query parameters
    params = parse_qs(parsed.query, keep_blank_values=True)

    # Convert sensitive params to lowercase for case-insensitive matching
    sensitive_lower = {p.lower() for p in sensitive_params}

    # Sanitize sensitive parameters
    sanitized_params = {}
    for key, values in params.items():
        if key.lower() in sensitive_lower:
            # Redact all values for this parameter
            sanitized_params[key] = None
        else:
            sanitized_params[key] = values

    # Rebuild query string
    new_query = urlencode(sanitized_params, doseq=True)

    # Rebuild URI
    return urlunparse((parsed.scheme, parsed.netloc, parsed.path, parsed.params, new_query, parsed.fragment))


def x_sanitize_uri__mutmut_18(
    uri: str,
    sensitive_params: list[str] | None = None,
    redacted: str = REDACTED_VALUE,
) -> str:
    """Sanitize sensitive query parameters in URI for safe logging.

    Args:
        uri: URI to sanitize
        sensitive_params: List of parameter names to redact (case-insensitive)
        redacted: Replacement value for redacted parameters

    Returns:
        Sanitized URI string

    """
    if sensitive_params is None:
        sensitive_params = DEFAULT_SENSITIVE_PARAMS

    # Parse URI
    parsed = urlparse(uri)

    # If no query string, return as-is
    if not parsed.query:
        return uri

    # Parse query parameters
    params = parse_qs(parsed.query, keep_blank_values=True)

    # Convert sensitive params to lowercase for case-insensitive matching
    sensitive_lower = {p.lower() for p in sensitive_params}

    # Sanitize sensitive parameters
    sanitized_params = {}
    for key, values in params.items():
        if key.lower() in sensitive_lower:
            # Redact all values for this parameter
            sanitized_params[key] = [redacted] / len(values)
        else:
            sanitized_params[key] = values

    # Rebuild query string
    new_query = urlencode(sanitized_params, doseq=True)

    # Rebuild URI
    return urlunparse((parsed.scheme, parsed.netloc, parsed.path, parsed.params, new_query, parsed.fragment))


def x_sanitize_uri__mutmut_19(
    uri: str,
    sensitive_params: list[str] | None = None,
    redacted: str = REDACTED_VALUE,
) -> str:
    """Sanitize sensitive query parameters in URI for safe logging.

    Args:
        uri: URI to sanitize
        sensitive_params: List of parameter names to redact (case-insensitive)
        redacted: Replacement value for redacted parameters

    Returns:
        Sanitized URI string

    """
    if sensitive_params is None:
        sensitive_params = DEFAULT_SENSITIVE_PARAMS

    # Parse URI
    parsed = urlparse(uri)

    # If no query string, return as-is
    if not parsed.query:
        return uri

    # Parse query parameters
    params = parse_qs(parsed.query, keep_blank_values=True)

    # Convert sensitive params to lowercase for case-insensitive matching
    sensitive_lower = {p.lower() for p in sensitive_params}

    # Sanitize sensitive parameters
    sanitized_params = {}
    for key, values in params.items():
        if key.lower() in sensitive_lower:
            # Redact all values for this parameter
            sanitized_params[key] = [redacted] * len(values)
        else:
            sanitized_params[key] = None

    # Rebuild query string
    new_query = urlencode(sanitized_params, doseq=True)

    # Rebuild URI
    return urlunparse((parsed.scheme, parsed.netloc, parsed.path, parsed.params, new_query, parsed.fragment))


def x_sanitize_uri__mutmut_20(
    uri: str,
    sensitive_params: list[str] | None = None,
    redacted: str = REDACTED_VALUE,
) -> str:
    """Sanitize sensitive query parameters in URI for safe logging.

    Args:
        uri: URI to sanitize
        sensitive_params: List of parameter names to redact (case-insensitive)
        redacted: Replacement value for redacted parameters

    Returns:
        Sanitized URI string

    """
    if sensitive_params is None:
        sensitive_params = DEFAULT_SENSITIVE_PARAMS

    # Parse URI
    parsed = urlparse(uri)

    # If no query string, return as-is
    if not parsed.query:
        return uri

    # Parse query parameters
    params = parse_qs(parsed.query, keep_blank_values=True)

    # Convert sensitive params to lowercase for case-insensitive matching
    sensitive_lower = {p.lower() for p in sensitive_params}

    # Sanitize sensitive parameters
    sanitized_params = {}
    for key, values in params.items():
        if key.lower() in sensitive_lower:
            # Redact all values for this parameter
            sanitized_params[key] = [redacted] * len(values)
        else:
            sanitized_params[key] = values

    # Rebuild query string
    new_query = None

    # Rebuild URI
    return urlunparse((parsed.scheme, parsed.netloc, parsed.path, parsed.params, new_query, parsed.fragment))


def x_sanitize_uri__mutmut_21(
    uri: str,
    sensitive_params: list[str] | None = None,
    redacted: str = REDACTED_VALUE,
) -> str:
    """Sanitize sensitive query parameters in URI for safe logging.

    Args:
        uri: URI to sanitize
        sensitive_params: List of parameter names to redact (case-insensitive)
        redacted: Replacement value for redacted parameters

    Returns:
        Sanitized URI string

    """
    if sensitive_params is None:
        sensitive_params = DEFAULT_SENSITIVE_PARAMS

    # Parse URI
    parsed = urlparse(uri)

    # If no query string, return as-is
    if not parsed.query:
        return uri

    # Parse query parameters
    params = parse_qs(parsed.query, keep_blank_values=True)

    # Convert sensitive params to lowercase for case-insensitive matching
    sensitive_lower = {p.lower() for p in sensitive_params}

    # Sanitize sensitive parameters
    sanitized_params = {}
    for key, values in params.items():
        if key.lower() in sensitive_lower:
            # Redact all values for this parameter
            sanitized_params[key] = [redacted] * len(values)
        else:
            sanitized_params[key] = values

    # Rebuild query string
    new_query = urlencode(None, doseq=True)

    # Rebuild URI
    return urlunparse((parsed.scheme, parsed.netloc, parsed.path, parsed.params, new_query, parsed.fragment))


def x_sanitize_uri__mutmut_22(
    uri: str,
    sensitive_params: list[str] | None = None,
    redacted: str = REDACTED_VALUE,
) -> str:
    """Sanitize sensitive query parameters in URI for safe logging.

    Args:
        uri: URI to sanitize
        sensitive_params: List of parameter names to redact (case-insensitive)
        redacted: Replacement value for redacted parameters

    Returns:
        Sanitized URI string

    """
    if sensitive_params is None:
        sensitive_params = DEFAULT_SENSITIVE_PARAMS

    # Parse URI
    parsed = urlparse(uri)

    # If no query string, return as-is
    if not parsed.query:
        return uri

    # Parse query parameters
    params = parse_qs(parsed.query, keep_blank_values=True)

    # Convert sensitive params to lowercase for case-insensitive matching
    sensitive_lower = {p.lower() for p in sensitive_params}

    # Sanitize sensitive parameters
    sanitized_params = {}
    for key, values in params.items():
        if key.lower() in sensitive_lower:
            # Redact all values for this parameter
            sanitized_params[key] = [redacted] * len(values)
        else:
            sanitized_params[key] = values

    # Rebuild query string
    new_query = urlencode(sanitized_params, doseq=None)

    # Rebuild URI
    return urlunparse((parsed.scheme, parsed.netloc, parsed.path, parsed.params, new_query, parsed.fragment))


def x_sanitize_uri__mutmut_23(
    uri: str,
    sensitive_params: list[str] | None = None,
    redacted: str = REDACTED_VALUE,
) -> str:
    """Sanitize sensitive query parameters in URI for safe logging.

    Args:
        uri: URI to sanitize
        sensitive_params: List of parameter names to redact (case-insensitive)
        redacted: Replacement value for redacted parameters

    Returns:
        Sanitized URI string

    """
    if sensitive_params is None:
        sensitive_params = DEFAULT_SENSITIVE_PARAMS

    # Parse URI
    parsed = urlparse(uri)

    # If no query string, return as-is
    if not parsed.query:
        return uri

    # Parse query parameters
    params = parse_qs(parsed.query, keep_blank_values=True)

    # Convert sensitive params to lowercase for case-insensitive matching
    sensitive_lower = {p.lower() for p in sensitive_params}

    # Sanitize sensitive parameters
    sanitized_params = {}
    for key, values in params.items():
        if key.lower() in sensitive_lower:
            # Redact all values for this parameter
            sanitized_params[key] = [redacted] * len(values)
        else:
            sanitized_params[key] = values

    # Rebuild query string
    new_query = urlencode(doseq=True)

    # Rebuild URI
    return urlunparse((parsed.scheme, parsed.netloc, parsed.path, parsed.params, new_query, parsed.fragment))


def x_sanitize_uri__mutmut_24(
    uri: str,
    sensitive_params: list[str] | None = None,
    redacted: str = REDACTED_VALUE,
) -> str:
    """Sanitize sensitive query parameters in URI for safe logging.

    Args:
        uri: URI to sanitize
        sensitive_params: List of parameter names to redact (case-insensitive)
        redacted: Replacement value for redacted parameters

    Returns:
        Sanitized URI string

    """
    if sensitive_params is None:
        sensitive_params = DEFAULT_SENSITIVE_PARAMS

    # Parse URI
    parsed = urlparse(uri)

    # If no query string, return as-is
    if not parsed.query:
        return uri

    # Parse query parameters
    params = parse_qs(parsed.query, keep_blank_values=True)

    # Convert sensitive params to lowercase for case-insensitive matching
    sensitive_lower = {p.lower() for p in sensitive_params}

    # Sanitize sensitive parameters
    sanitized_params = {}
    for key, values in params.items():
        if key.lower() in sensitive_lower:
            # Redact all values for this parameter
            sanitized_params[key] = [redacted] * len(values)
        else:
            sanitized_params[key] = values

    # Rebuild query string
    new_query = urlencode(sanitized_params, )

    # Rebuild URI
    return urlunparse((parsed.scheme, parsed.netloc, parsed.path, parsed.params, new_query, parsed.fragment))


def x_sanitize_uri__mutmut_25(
    uri: str,
    sensitive_params: list[str] | None = None,
    redacted: str = REDACTED_VALUE,
) -> str:
    """Sanitize sensitive query parameters in URI for safe logging.

    Args:
        uri: URI to sanitize
        sensitive_params: List of parameter names to redact (case-insensitive)
        redacted: Replacement value for redacted parameters

    Returns:
        Sanitized URI string

    """
    if sensitive_params is None:
        sensitive_params = DEFAULT_SENSITIVE_PARAMS

    # Parse URI
    parsed = urlparse(uri)

    # If no query string, return as-is
    if not parsed.query:
        return uri

    # Parse query parameters
    params = parse_qs(parsed.query, keep_blank_values=True)

    # Convert sensitive params to lowercase for case-insensitive matching
    sensitive_lower = {p.lower() for p in sensitive_params}

    # Sanitize sensitive parameters
    sanitized_params = {}
    for key, values in params.items():
        if key.lower() in sensitive_lower:
            # Redact all values for this parameter
            sanitized_params[key] = [redacted] * len(values)
        else:
            sanitized_params[key] = values

    # Rebuild query string
    new_query = urlencode(sanitized_params, doseq=False)

    # Rebuild URI
    return urlunparse((parsed.scheme, parsed.netloc, parsed.path, parsed.params, new_query, parsed.fragment))


def x_sanitize_uri__mutmut_26(
    uri: str,
    sensitive_params: list[str] | None = None,
    redacted: str = REDACTED_VALUE,
) -> str:
    """Sanitize sensitive query parameters in URI for safe logging.

    Args:
        uri: URI to sanitize
        sensitive_params: List of parameter names to redact (case-insensitive)
        redacted: Replacement value for redacted parameters

    Returns:
        Sanitized URI string

    """
    if sensitive_params is None:
        sensitive_params = DEFAULT_SENSITIVE_PARAMS

    # Parse URI
    parsed = urlparse(uri)

    # If no query string, return as-is
    if not parsed.query:
        return uri

    # Parse query parameters
    params = parse_qs(parsed.query, keep_blank_values=True)

    # Convert sensitive params to lowercase for case-insensitive matching
    sensitive_lower = {p.lower() for p in sensitive_params}

    # Sanitize sensitive parameters
    sanitized_params = {}
    for key, values in params.items():
        if key.lower() in sensitive_lower:
            # Redact all values for this parameter
            sanitized_params[key] = [redacted] * len(values)
        else:
            sanitized_params[key] = values

    # Rebuild query string
    new_query = urlencode(sanitized_params, doseq=True)

    # Rebuild URI
    return urlunparse(None)

x_sanitize_uri__mutmut_mutants : ClassVar[MutantDict] = {
'x_sanitize_uri__mutmut_1': x_sanitize_uri__mutmut_1, 
    'x_sanitize_uri__mutmut_2': x_sanitize_uri__mutmut_2, 
    'x_sanitize_uri__mutmut_3': x_sanitize_uri__mutmut_3, 
    'x_sanitize_uri__mutmut_4': x_sanitize_uri__mutmut_4, 
    'x_sanitize_uri__mutmut_5': x_sanitize_uri__mutmut_5, 
    'x_sanitize_uri__mutmut_6': x_sanitize_uri__mutmut_6, 
    'x_sanitize_uri__mutmut_7': x_sanitize_uri__mutmut_7, 
    'x_sanitize_uri__mutmut_8': x_sanitize_uri__mutmut_8, 
    'x_sanitize_uri__mutmut_9': x_sanitize_uri__mutmut_9, 
    'x_sanitize_uri__mutmut_10': x_sanitize_uri__mutmut_10, 
    'x_sanitize_uri__mutmut_11': x_sanitize_uri__mutmut_11, 
    'x_sanitize_uri__mutmut_12': x_sanitize_uri__mutmut_12, 
    'x_sanitize_uri__mutmut_13': x_sanitize_uri__mutmut_13, 
    'x_sanitize_uri__mutmut_14': x_sanitize_uri__mutmut_14, 
    'x_sanitize_uri__mutmut_15': x_sanitize_uri__mutmut_15, 
    'x_sanitize_uri__mutmut_16': x_sanitize_uri__mutmut_16, 
    'x_sanitize_uri__mutmut_17': x_sanitize_uri__mutmut_17, 
    'x_sanitize_uri__mutmut_18': x_sanitize_uri__mutmut_18, 
    'x_sanitize_uri__mutmut_19': x_sanitize_uri__mutmut_19, 
    'x_sanitize_uri__mutmut_20': x_sanitize_uri__mutmut_20, 
    'x_sanitize_uri__mutmut_21': x_sanitize_uri__mutmut_21, 
    'x_sanitize_uri__mutmut_22': x_sanitize_uri__mutmut_22, 
    'x_sanitize_uri__mutmut_23': x_sanitize_uri__mutmut_23, 
    'x_sanitize_uri__mutmut_24': x_sanitize_uri__mutmut_24, 
    'x_sanitize_uri__mutmut_25': x_sanitize_uri__mutmut_25, 
    'x_sanitize_uri__mutmut_26': x_sanitize_uri__mutmut_26
}

def sanitize_uri(*args, **kwargs):
    result = _mutmut_trampoline(x_sanitize_uri__mutmut_orig, x_sanitize_uri__mutmut_mutants, args, kwargs)
    return result 

sanitize_uri.__signature__ = _mutmut_signature(x_sanitize_uri__mutmut_orig)
x_sanitize_uri__mutmut_orig.__name__ = 'x_sanitize_uri'


def x_sanitize_dict__mutmut_orig(
    data: dict[str, Any],
    sensitive_keys: list[str] | None = None,
    redacted: str = REDACTED_VALUE,
    recursive: bool = True,
) -> dict[str, Any]:
    """Sanitize sensitive keys in dictionary for safe logging.

    Args:
        data: Dictionary to sanitize
        sensitive_keys: List of keys to redact (case-insensitive)
        redacted: Replacement value for redacted values
        recursive: Whether to recursively sanitize nested dicts

    Returns:
        Sanitized dictionary

    """
    if sensitive_keys is None:
        # Use combined list of headers and params as defaults
        sensitive_keys = DEFAULT_SENSITIVE_HEADERS + DEFAULT_SENSITIVE_PARAMS

    # Convert sensitive keys to lowercase for case-insensitive matching
    sensitive_lower = {k.lower() for k in sensitive_keys}

    sanitized: dict[str, Any] = {}
    for key, value in data.items():
        if key.lower() in sensitive_lower:
            sanitized[key] = redacted
        elif recursive and isinstance(value, dict):
            sanitized[key] = sanitize_dict(value, sensitive_keys, redacted, recursive)
        elif recursive and isinstance(value, list):
            # Sanitize list elements if they're dicts
            sanitized[key] = [
                sanitize_dict(item, sensitive_keys, redacted, recursive) if isinstance(item, dict) else item
                for item in value
            ]
        else:
            sanitized[key] = value

    return sanitized


def x_sanitize_dict__mutmut_1(
    data: dict[str, Any],
    sensitive_keys: list[str] | None = None,
    redacted: str = REDACTED_VALUE,
    recursive: bool = False,
) -> dict[str, Any]:
    """Sanitize sensitive keys in dictionary for safe logging.

    Args:
        data: Dictionary to sanitize
        sensitive_keys: List of keys to redact (case-insensitive)
        redacted: Replacement value for redacted values
        recursive: Whether to recursively sanitize nested dicts

    Returns:
        Sanitized dictionary

    """
    if sensitive_keys is None:
        # Use combined list of headers and params as defaults
        sensitive_keys = DEFAULT_SENSITIVE_HEADERS + DEFAULT_SENSITIVE_PARAMS

    # Convert sensitive keys to lowercase for case-insensitive matching
    sensitive_lower = {k.lower() for k in sensitive_keys}

    sanitized: dict[str, Any] = {}
    for key, value in data.items():
        if key.lower() in sensitive_lower:
            sanitized[key] = redacted
        elif recursive and isinstance(value, dict):
            sanitized[key] = sanitize_dict(value, sensitive_keys, redacted, recursive)
        elif recursive and isinstance(value, list):
            # Sanitize list elements if they're dicts
            sanitized[key] = [
                sanitize_dict(item, sensitive_keys, redacted, recursive) if isinstance(item, dict) else item
                for item in value
            ]
        else:
            sanitized[key] = value

    return sanitized


def x_sanitize_dict__mutmut_2(
    data: dict[str, Any],
    sensitive_keys: list[str] | None = None,
    redacted: str = REDACTED_VALUE,
    recursive: bool = True,
) -> dict[str, Any]:
    """Sanitize sensitive keys in dictionary for safe logging.

    Args:
        data: Dictionary to sanitize
        sensitive_keys: List of keys to redact (case-insensitive)
        redacted: Replacement value for redacted values
        recursive: Whether to recursively sanitize nested dicts

    Returns:
        Sanitized dictionary

    """
    if sensitive_keys is not None:
        # Use combined list of headers and params as defaults
        sensitive_keys = DEFAULT_SENSITIVE_HEADERS + DEFAULT_SENSITIVE_PARAMS

    # Convert sensitive keys to lowercase for case-insensitive matching
    sensitive_lower = {k.lower() for k in sensitive_keys}

    sanitized: dict[str, Any] = {}
    for key, value in data.items():
        if key.lower() in sensitive_lower:
            sanitized[key] = redacted
        elif recursive and isinstance(value, dict):
            sanitized[key] = sanitize_dict(value, sensitive_keys, redacted, recursive)
        elif recursive and isinstance(value, list):
            # Sanitize list elements if they're dicts
            sanitized[key] = [
                sanitize_dict(item, sensitive_keys, redacted, recursive) if isinstance(item, dict) else item
                for item in value
            ]
        else:
            sanitized[key] = value

    return sanitized


def x_sanitize_dict__mutmut_3(
    data: dict[str, Any],
    sensitive_keys: list[str] | None = None,
    redacted: str = REDACTED_VALUE,
    recursive: bool = True,
) -> dict[str, Any]:
    """Sanitize sensitive keys in dictionary for safe logging.

    Args:
        data: Dictionary to sanitize
        sensitive_keys: List of keys to redact (case-insensitive)
        redacted: Replacement value for redacted values
        recursive: Whether to recursively sanitize nested dicts

    Returns:
        Sanitized dictionary

    """
    if sensitive_keys is None:
        # Use combined list of headers and params as defaults
        sensitive_keys = None

    # Convert sensitive keys to lowercase for case-insensitive matching
    sensitive_lower = {k.lower() for k in sensitive_keys}

    sanitized: dict[str, Any] = {}
    for key, value in data.items():
        if key.lower() in sensitive_lower:
            sanitized[key] = redacted
        elif recursive and isinstance(value, dict):
            sanitized[key] = sanitize_dict(value, sensitive_keys, redacted, recursive)
        elif recursive and isinstance(value, list):
            # Sanitize list elements if they're dicts
            sanitized[key] = [
                sanitize_dict(item, sensitive_keys, redacted, recursive) if isinstance(item, dict) else item
                for item in value
            ]
        else:
            sanitized[key] = value

    return sanitized


def x_sanitize_dict__mutmut_4(
    data: dict[str, Any],
    sensitive_keys: list[str] | None = None,
    redacted: str = REDACTED_VALUE,
    recursive: bool = True,
) -> dict[str, Any]:
    """Sanitize sensitive keys in dictionary for safe logging.

    Args:
        data: Dictionary to sanitize
        sensitive_keys: List of keys to redact (case-insensitive)
        redacted: Replacement value for redacted values
        recursive: Whether to recursively sanitize nested dicts

    Returns:
        Sanitized dictionary

    """
    if sensitive_keys is None:
        # Use combined list of headers and params as defaults
        sensitive_keys = DEFAULT_SENSITIVE_HEADERS - DEFAULT_SENSITIVE_PARAMS

    # Convert sensitive keys to lowercase for case-insensitive matching
    sensitive_lower = {k.lower() for k in sensitive_keys}

    sanitized: dict[str, Any] = {}
    for key, value in data.items():
        if key.lower() in sensitive_lower:
            sanitized[key] = redacted
        elif recursive and isinstance(value, dict):
            sanitized[key] = sanitize_dict(value, sensitive_keys, redacted, recursive)
        elif recursive and isinstance(value, list):
            # Sanitize list elements if they're dicts
            sanitized[key] = [
                sanitize_dict(item, sensitive_keys, redacted, recursive) if isinstance(item, dict) else item
                for item in value
            ]
        else:
            sanitized[key] = value

    return sanitized


def x_sanitize_dict__mutmut_5(
    data: dict[str, Any],
    sensitive_keys: list[str] | None = None,
    redacted: str = REDACTED_VALUE,
    recursive: bool = True,
) -> dict[str, Any]:
    """Sanitize sensitive keys in dictionary for safe logging.

    Args:
        data: Dictionary to sanitize
        sensitive_keys: List of keys to redact (case-insensitive)
        redacted: Replacement value for redacted values
        recursive: Whether to recursively sanitize nested dicts

    Returns:
        Sanitized dictionary

    """
    if sensitive_keys is None:
        # Use combined list of headers and params as defaults
        sensitive_keys = DEFAULT_SENSITIVE_HEADERS + DEFAULT_SENSITIVE_PARAMS

    # Convert sensitive keys to lowercase for case-insensitive matching
    sensitive_lower = None

    sanitized: dict[str, Any] = {}
    for key, value in data.items():
        if key.lower() in sensitive_lower:
            sanitized[key] = redacted
        elif recursive and isinstance(value, dict):
            sanitized[key] = sanitize_dict(value, sensitive_keys, redacted, recursive)
        elif recursive and isinstance(value, list):
            # Sanitize list elements if they're dicts
            sanitized[key] = [
                sanitize_dict(item, sensitive_keys, redacted, recursive) if isinstance(item, dict) else item
                for item in value
            ]
        else:
            sanitized[key] = value

    return sanitized


def x_sanitize_dict__mutmut_6(
    data: dict[str, Any],
    sensitive_keys: list[str] | None = None,
    redacted: str = REDACTED_VALUE,
    recursive: bool = True,
) -> dict[str, Any]:
    """Sanitize sensitive keys in dictionary for safe logging.

    Args:
        data: Dictionary to sanitize
        sensitive_keys: List of keys to redact (case-insensitive)
        redacted: Replacement value for redacted values
        recursive: Whether to recursively sanitize nested dicts

    Returns:
        Sanitized dictionary

    """
    if sensitive_keys is None:
        # Use combined list of headers and params as defaults
        sensitive_keys = DEFAULT_SENSITIVE_HEADERS + DEFAULT_SENSITIVE_PARAMS

    # Convert sensitive keys to lowercase for case-insensitive matching
    sensitive_lower = {k.upper() for k in sensitive_keys}

    sanitized: dict[str, Any] = {}
    for key, value in data.items():
        if key.lower() in sensitive_lower:
            sanitized[key] = redacted
        elif recursive and isinstance(value, dict):
            sanitized[key] = sanitize_dict(value, sensitive_keys, redacted, recursive)
        elif recursive and isinstance(value, list):
            # Sanitize list elements if they're dicts
            sanitized[key] = [
                sanitize_dict(item, sensitive_keys, redacted, recursive) if isinstance(item, dict) else item
                for item in value
            ]
        else:
            sanitized[key] = value

    return sanitized


def x_sanitize_dict__mutmut_7(
    data: dict[str, Any],
    sensitive_keys: list[str] | None = None,
    redacted: str = REDACTED_VALUE,
    recursive: bool = True,
) -> dict[str, Any]:
    """Sanitize sensitive keys in dictionary for safe logging.

    Args:
        data: Dictionary to sanitize
        sensitive_keys: List of keys to redact (case-insensitive)
        redacted: Replacement value for redacted values
        recursive: Whether to recursively sanitize nested dicts

    Returns:
        Sanitized dictionary

    """
    if sensitive_keys is None:
        # Use combined list of headers and params as defaults
        sensitive_keys = DEFAULT_SENSITIVE_HEADERS + DEFAULT_SENSITIVE_PARAMS

    # Convert sensitive keys to lowercase for case-insensitive matching
    sensitive_lower = {k.lower() for k in sensitive_keys}

    sanitized: dict[str, Any] = None
    for key, value in data.items():
        if key.lower() in sensitive_lower:
            sanitized[key] = redacted
        elif recursive and isinstance(value, dict):
            sanitized[key] = sanitize_dict(value, sensitive_keys, redacted, recursive)
        elif recursive and isinstance(value, list):
            # Sanitize list elements if they're dicts
            sanitized[key] = [
                sanitize_dict(item, sensitive_keys, redacted, recursive) if isinstance(item, dict) else item
                for item in value
            ]
        else:
            sanitized[key] = value

    return sanitized


def x_sanitize_dict__mutmut_8(
    data: dict[str, Any],
    sensitive_keys: list[str] | None = None,
    redacted: str = REDACTED_VALUE,
    recursive: bool = True,
) -> dict[str, Any]:
    """Sanitize sensitive keys in dictionary for safe logging.

    Args:
        data: Dictionary to sanitize
        sensitive_keys: List of keys to redact (case-insensitive)
        redacted: Replacement value for redacted values
        recursive: Whether to recursively sanitize nested dicts

    Returns:
        Sanitized dictionary

    """
    if sensitive_keys is None:
        # Use combined list of headers and params as defaults
        sensitive_keys = DEFAULT_SENSITIVE_HEADERS + DEFAULT_SENSITIVE_PARAMS

    # Convert sensitive keys to lowercase for case-insensitive matching
    sensitive_lower = {k.lower() for k in sensitive_keys}

    sanitized: dict[str, Any] = {}
    for key, value in data.items():
        if key.upper() in sensitive_lower:
            sanitized[key] = redacted
        elif recursive and isinstance(value, dict):
            sanitized[key] = sanitize_dict(value, sensitive_keys, redacted, recursive)
        elif recursive and isinstance(value, list):
            # Sanitize list elements if they're dicts
            sanitized[key] = [
                sanitize_dict(item, sensitive_keys, redacted, recursive) if isinstance(item, dict) else item
                for item in value
            ]
        else:
            sanitized[key] = value

    return sanitized


def x_sanitize_dict__mutmut_9(
    data: dict[str, Any],
    sensitive_keys: list[str] | None = None,
    redacted: str = REDACTED_VALUE,
    recursive: bool = True,
) -> dict[str, Any]:
    """Sanitize sensitive keys in dictionary for safe logging.

    Args:
        data: Dictionary to sanitize
        sensitive_keys: List of keys to redact (case-insensitive)
        redacted: Replacement value for redacted values
        recursive: Whether to recursively sanitize nested dicts

    Returns:
        Sanitized dictionary

    """
    if sensitive_keys is None:
        # Use combined list of headers and params as defaults
        sensitive_keys = DEFAULT_SENSITIVE_HEADERS + DEFAULT_SENSITIVE_PARAMS

    # Convert sensitive keys to lowercase for case-insensitive matching
    sensitive_lower = {k.lower() for k in sensitive_keys}

    sanitized: dict[str, Any] = {}
    for key, value in data.items():
        if key.lower() not in sensitive_lower:
            sanitized[key] = redacted
        elif recursive and isinstance(value, dict):
            sanitized[key] = sanitize_dict(value, sensitive_keys, redacted, recursive)
        elif recursive and isinstance(value, list):
            # Sanitize list elements if they're dicts
            sanitized[key] = [
                sanitize_dict(item, sensitive_keys, redacted, recursive) if isinstance(item, dict) else item
                for item in value
            ]
        else:
            sanitized[key] = value

    return sanitized


def x_sanitize_dict__mutmut_10(
    data: dict[str, Any],
    sensitive_keys: list[str] | None = None,
    redacted: str = REDACTED_VALUE,
    recursive: bool = True,
) -> dict[str, Any]:
    """Sanitize sensitive keys in dictionary for safe logging.

    Args:
        data: Dictionary to sanitize
        sensitive_keys: List of keys to redact (case-insensitive)
        redacted: Replacement value for redacted values
        recursive: Whether to recursively sanitize nested dicts

    Returns:
        Sanitized dictionary

    """
    if sensitive_keys is None:
        # Use combined list of headers and params as defaults
        sensitive_keys = DEFAULT_SENSITIVE_HEADERS + DEFAULT_SENSITIVE_PARAMS

    # Convert sensitive keys to lowercase for case-insensitive matching
    sensitive_lower = {k.lower() for k in sensitive_keys}

    sanitized: dict[str, Any] = {}
    for key, value in data.items():
        if key.lower() in sensitive_lower:
            sanitized[key] = None
        elif recursive and isinstance(value, dict):
            sanitized[key] = sanitize_dict(value, sensitive_keys, redacted, recursive)
        elif recursive and isinstance(value, list):
            # Sanitize list elements if they're dicts
            sanitized[key] = [
                sanitize_dict(item, sensitive_keys, redacted, recursive) if isinstance(item, dict) else item
                for item in value
            ]
        else:
            sanitized[key] = value

    return sanitized


def x_sanitize_dict__mutmut_11(
    data: dict[str, Any],
    sensitive_keys: list[str] | None = None,
    redacted: str = REDACTED_VALUE,
    recursive: bool = True,
) -> dict[str, Any]:
    """Sanitize sensitive keys in dictionary for safe logging.

    Args:
        data: Dictionary to sanitize
        sensitive_keys: List of keys to redact (case-insensitive)
        redacted: Replacement value for redacted values
        recursive: Whether to recursively sanitize nested dicts

    Returns:
        Sanitized dictionary

    """
    if sensitive_keys is None:
        # Use combined list of headers and params as defaults
        sensitive_keys = DEFAULT_SENSITIVE_HEADERS + DEFAULT_SENSITIVE_PARAMS

    # Convert sensitive keys to lowercase for case-insensitive matching
    sensitive_lower = {k.lower() for k in sensitive_keys}

    sanitized: dict[str, Any] = {}
    for key, value in data.items():
        if key.lower() in sensitive_lower:
            sanitized[key] = redacted
        elif recursive or isinstance(value, dict):
            sanitized[key] = sanitize_dict(value, sensitive_keys, redacted, recursive)
        elif recursive and isinstance(value, list):
            # Sanitize list elements if they're dicts
            sanitized[key] = [
                sanitize_dict(item, sensitive_keys, redacted, recursive) if isinstance(item, dict) else item
                for item in value
            ]
        else:
            sanitized[key] = value

    return sanitized


def x_sanitize_dict__mutmut_12(
    data: dict[str, Any],
    sensitive_keys: list[str] | None = None,
    redacted: str = REDACTED_VALUE,
    recursive: bool = True,
) -> dict[str, Any]:
    """Sanitize sensitive keys in dictionary for safe logging.

    Args:
        data: Dictionary to sanitize
        sensitive_keys: List of keys to redact (case-insensitive)
        redacted: Replacement value for redacted values
        recursive: Whether to recursively sanitize nested dicts

    Returns:
        Sanitized dictionary

    """
    if sensitive_keys is None:
        # Use combined list of headers and params as defaults
        sensitive_keys = DEFAULT_SENSITIVE_HEADERS + DEFAULT_SENSITIVE_PARAMS

    # Convert sensitive keys to lowercase for case-insensitive matching
    sensitive_lower = {k.lower() for k in sensitive_keys}

    sanitized: dict[str, Any] = {}
    for key, value in data.items():
        if key.lower() in sensitive_lower:
            sanitized[key] = redacted
        elif recursive and isinstance(value, dict):
            sanitized[key] = None
        elif recursive and isinstance(value, list):
            # Sanitize list elements if they're dicts
            sanitized[key] = [
                sanitize_dict(item, sensitive_keys, redacted, recursive) if isinstance(item, dict) else item
                for item in value
            ]
        else:
            sanitized[key] = value

    return sanitized


def x_sanitize_dict__mutmut_13(
    data: dict[str, Any],
    sensitive_keys: list[str] | None = None,
    redacted: str = REDACTED_VALUE,
    recursive: bool = True,
) -> dict[str, Any]:
    """Sanitize sensitive keys in dictionary for safe logging.

    Args:
        data: Dictionary to sanitize
        sensitive_keys: List of keys to redact (case-insensitive)
        redacted: Replacement value for redacted values
        recursive: Whether to recursively sanitize nested dicts

    Returns:
        Sanitized dictionary

    """
    if sensitive_keys is None:
        # Use combined list of headers and params as defaults
        sensitive_keys = DEFAULT_SENSITIVE_HEADERS + DEFAULT_SENSITIVE_PARAMS

    # Convert sensitive keys to lowercase for case-insensitive matching
    sensitive_lower = {k.lower() for k in sensitive_keys}

    sanitized: dict[str, Any] = {}
    for key, value in data.items():
        if key.lower() in sensitive_lower:
            sanitized[key] = redacted
        elif recursive and isinstance(value, dict):
            sanitized[key] = sanitize_dict(None, sensitive_keys, redacted, recursive)
        elif recursive and isinstance(value, list):
            # Sanitize list elements if they're dicts
            sanitized[key] = [
                sanitize_dict(item, sensitive_keys, redacted, recursive) if isinstance(item, dict) else item
                for item in value
            ]
        else:
            sanitized[key] = value

    return sanitized


def x_sanitize_dict__mutmut_14(
    data: dict[str, Any],
    sensitive_keys: list[str] | None = None,
    redacted: str = REDACTED_VALUE,
    recursive: bool = True,
) -> dict[str, Any]:
    """Sanitize sensitive keys in dictionary for safe logging.

    Args:
        data: Dictionary to sanitize
        sensitive_keys: List of keys to redact (case-insensitive)
        redacted: Replacement value for redacted values
        recursive: Whether to recursively sanitize nested dicts

    Returns:
        Sanitized dictionary

    """
    if sensitive_keys is None:
        # Use combined list of headers and params as defaults
        sensitive_keys = DEFAULT_SENSITIVE_HEADERS + DEFAULT_SENSITIVE_PARAMS

    # Convert sensitive keys to lowercase for case-insensitive matching
    sensitive_lower = {k.lower() for k in sensitive_keys}

    sanitized: dict[str, Any] = {}
    for key, value in data.items():
        if key.lower() in sensitive_lower:
            sanitized[key] = redacted
        elif recursive and isinstance(value, dict):
            sanitized[key] = sanitize_dict(value, None, redacted, recursive)
        elif recursive and isinstance(value, list):
            # Sanitize list elements if they're dicts
            sanitized[key] = [
                sanitize_dict(item, sensitive_keys, redacted, recursive) if isinstance(item, dict) else item
                for item in value
            ]
        else:
            sanitized[key] = value

    return sanitized


def x_sanitize_dict__mutmut_15(
    data: dict[str, Any],
    sensitive_keys: list[str] | None = None,
    redacted: str = REDACTED_VALUE,
    recursive: bool = True,
) -> dict[str, Any]:
    """Sanitize sensitive keys in dictionary for safe logging.

    Args:
        data: Dictionary to sanitize
        sensitive_keys: List of keys to redact (case-insensitive)
        redacted: Replacement value for redacted values
        recursive: Whether to recursively sanitize nested dicts

    Returns:
        Sanitized dictionary

    """
    if sensitive_keys is None:
        # Use combined list of headers and params as defaults
        sensitive_keys = DEFAULT_SENSITIVE_HEADERS + DEFAULT_SENSITIVE_PARAMS

    # Convert sensitive keys to lowercase for case-insensitive matching
    sensitive_lower = {k.lower() for k in sensitive_keys}

    sanitized: dict[str, Any] = {}
    for key, value in data.items():
        if key.lower() in sensitive_lower:
            sanitized[key] = redacted
        elif recursive and isinstance(value, dict):
            sanitized[key] = sanitize_dict(value, sensitive_keys, None, recursive)
        elif recursive and isinstance(value, list):
            # Sanitize list elements if they're dicts
            sanitized[key] = [
                sanitize_dict(item, sensitive_keys, redacted, recursive) if isinstance(item, dict) else item
                for item in value
            ]
        else:
            sanitized[key] = value

    return sanitized


def x_sanitize_dict__mutmut_16(
    data: dict[str, Any],
    sensitive_keys: list[str] | None = None,
    redacted: str = REDACTED_VALUE,
    recursive: bool = True,
) -> dict[str, Any]:
    """Sanitize sensitive keys in dictionary for safe logging.

    Args:
        data: Dictionary to sanitize
        sensitive_keys: List of keys to redact (case-insensitive)
        redacted: Replacement value for redacted values
        recursive: Whether to recursively sanitize nested dicts

    Returns:
        Sanitized dictionary

    """
    if sensitive_keys is None:
        # Use combined list of headers and params as defaults
        sensitive_keys = DEFAULT_SENSITIVE_HEADERS + DEFAULT_SENSITIVE_PARAMS

    # Convert sensitive keys to lowercase for case-insensitive matching
    sensitive_lower = {k.lower() for k in sensitive_keys}

    sanitized: dict[str, Any] = {}
    for key, value in data.items():
        if key.lower() in sensitive_lower:
            sanitized[key] = redacted
        elif recursive and isinstance(value, dict):
            sanitized[key] = sanitize_dict(value, sensitive_keys, redacted, None)
        elif recursive and isinstance(value, list):
            # Sanitize list elements if they're dicts
            sanitized[key] = [
                sanitize_dict(item, sensitive_keys, redacted, recursive) if isinstance(item, dict) else item
                for item in value
            ]
        else:
            sanitized[key] = value

    return sanitized


def x_sanitize_dict__mutmut_17(
    data: dict[str, Any],
    sensitive_keys: list[str] | None = None,
    redacted: str = REDACTED_VALUE,
    recursive: bool = True,
) -> dict[str, Any]:
    """Sanitize sensitive keys in dictionary for safe logging.

    Args:
        data: Dictionary to sanitize
        sensitive_keys: List of keys to redact (case-insensitive)
        redacted: Replacement value for redacted values
        recursive: Whether to recursively sanitize nested dicts

    Returns:
        Sanitized dictionary

    """
    if sensitive_keys is None:
        # Use combined list of headers and params as defaults
        sensitive_keys = DEFAULT_SENSITIVE_HEADERS + DEFAULT_SENSITIVE_PARAMS

    # Convert sensitive keys to lowercase for case-insensitive matching
    sensitive_lower = {k.lower() for k in sensitive_keys}

    sanitized: dict[str, Any] = {}
    for key, value in data.items():
        if key.lower() in sensitive_lower:
            sanitized[key] = redacted
        elif recursive and isinstance(value, dict):
            sanitized[key] = sanitize_dict(sensitive_keys, redacted, recursive)
        elif recursive and isinstance(value, list):
            # Sanitize list elements if they're dicts
            sanitized[key] = [
                sanitize_dict(item, sensitive_keys, redacted, recursive) if isinstance(item, dict) else item
                for item in value
            ]
        else:
            sanitized[key] = value

    return sanitized


def x_sanitize_dict__mutmut_18(
    data: dict[str, Any],
    sensitive_keys: list[str] | None = None,
    redacted: str = REDACTED_VALUE,
    recursive: bool = True,
) -> dict[str, Any]:
    """Sanitize sensitive keys in dictionary for safe logging.

    Args:
        data: Dictionary to sanitize
        sensitive_keys: List of keys to redact (case-insensitive)
        redacted: Replacement value for redacted values
        recursive: Whether to recursively sanitize nested dicts

    Returns:
        Sanitized dictionary

    """
    if sensitive_keys is None:
        # Use combined list of headers and params as defaults
        sensitive_keys = DEFAULT_SENSITIVE_HEADERS + DEFAULT_SENSITIVE_PARAMS

    # Convert sensitive keys to lowercase for case-insensitive matching
    sensitive_lower = {k.lower() for k in sensitive_keys}

    sanitized: dict[str, Any] = {}
    for key, value in data.items():
        if key.lower() in sensitive_lower:
            sanitized[key] = redacted
        elif recursive and isinstance(value, dict):
            sanitized[key] = sanitize_dict(value, redacted, recursive)
        elif recursive and isinstance(value, list):
            # Sanitize list elements if they're dicts
            sanitized[key] = [
                sanitize_dict(item, sensitive_keys, redacted, recursive) if isinstance(item, dict) else item
                for item in value
            ]
        else:
            sanitized[key] = value

    return sanitized


def x_sanitize_dict__mutmut_19(
    data: dict[str, Any],
    sensitive_keys: list[str] | None = None,
    redacted: str = REDACTED_VALUE,
    recursive: bool = True,
) -> dict[str, Any]:
    """Sanitize sensitive keys in dictionary for safe logging.

    Args:
        data: Dictionary to sanitize
        sensitive_keys: List of keys to redact (case-insensitive)
        redacted: Replacement value for redacted values
        recursive: Whether to recursively sanitize nested dicts

    Returns:
        Sanitized dictionary

    """
    if sensitive_keys is None:
        # Use combined list of headers and params as defaults
        sensitive_keys = DEFAULT_SENSITIVE_HEADERS + DEFAULT_SENSITIVE_PARAMS

    # Convert sensitive keys to lowercase for case-insensitive matching
    sensitive_lower = {k.lower() for k in sensitive_keys}

    sanitized: dict[str, Any] = {}
    for key, value in data.items():
        if key.lower() in sensitive_lower:
            sanitized[key] = redacted
        elif recursive and isinstance(value, dict):
            sanitized[key] = sanitize_dict(value, sensitive_keys, recursive)
        elif recursive and isinstance(value, list):
            # Sanitize list elements if they're dicts
            sanitized[key] = [
                sanitize_dict(item, sensitive_keys, redacted, recursive) if isinstance(item, dict) else item
                for item in value
            ]
        else:
            sanitized[key] = value

    return sanitized


def x_sanitize_dict__mutmut_20(
    data: dict[str, Any],
    sensitive_keys: list[str] | None = None,
    redacted: str = REDACTED_VALUE,
    recursive: bool = True,
) -> dict[str, Any]:
    """Sanitize sensitive keys in dictionary for safe logging.

    Args:
        data: Dictionary to sanitize
        sensitive_keys: List of keys to redact (case-insensitive)
        redacted: Replacement value for redacted values
        recursive: Whether to recursively sanitize nested dicts

    Returns:
        Sanitized dictionary

    """
    if sensitive_keys is None:
        # Use combined list of headers and params as defaults
        sensitive_keys = DEFAULT_SENSITIVE_HEADERS + DEFAULT_SENSITIVE_PARAMS

    # Convert sensitive keys to lowercase for case-insensitive matching
    sensitive_lower = {k.lower() for k in sensitive_keys}

    sanitized: dict[str, Any] = {}
    for key, value in data.items():
        if key.lower() in sensitive_lower:
            sanitized[key] = redacted
        elif recursive and isinstance(value, dict):
            sanitized[key] = sanitize_dict(value, sensitive_keys, redacted, )
        elif recursive and isinstance(value, list):
            # Sanitize list elements if they're dicts
            sanitized[key] = [
                sanitize_dict(item, sensitive_keys, redacted, recursive) if isinstance(item, dict) else item
                for item in value
            ]
        else:
            sanitized[key] = value

    return sanitized


def x_sanitize_dict__mutmut_21(
    data: dict[str, Any],
    sensitive_keys: list[str] | None = None,
    redacted: str = REDACTED_VALUE,
    recursive: bool = True,
) -> dict[str, Any]:
    """Sanitize sensitive keys in dictionary for safe logging.

    Args:
        data: Dictionary to sanitize
        sensitive_keys: List of keys to redact (case-insensitive)
        redacted: Replacement value for redacted values
        recursive: Whether to recursively sanitize nested dicts

    Returns:
        Sanitized dictionary

    """
    if sensitive_keys is None:
        # Use combined list of headers and params as defaults
        sensitive_keys = DEFAULT_SENSITIVE_HEADERS + DEFAULT_SENSITIVE_PARAMS

    # Convert sensitive keys to lowercase for case-insensitive matching
    sensitive_lower = {k.lower() for k in sensitive_keys}

    sanitized: dict[str, Any] = {}
    for key, value in data.items():
        if key.lower() in sensitive_lower:
            sanitized[key] = redacted
        elif recursive and isinstance(value, dict):
            sanitized[key] = sanitize_dict(value, sensitive_keys, redacted, recursive)
        elif recursive or isinstance(value, list):
            # Sanitize list elements if they're dicts
            sanitized[key] = [
                sanitize_dict(item, sensitive_keys, redacted, recursive) if isinstance(item, dict) else item
                for item in value
            ]
        else:
            sanitized[key] = value

    return sanitized


def x_sanitize_dict__mutmut_22(
    data: dict[str, Any],
    sensitive_keys: list[str] | None = None,
    redacted: str = REDACTED_VALUE,
    recursive: bool = True,
) -> dict[str, Any]:
    """Sanitize sensitive keys in dictionary for safe logging.

    Args:
        data: Dictionary to sanitize
        sensitive_keys: List of keys to redact (case-insensitive)
        redacted: Replacement value for redacted values
        recursive: Whether to recursively sanitize nested dicts

    Returns:
        Sanitized dictionary

    """
    if sensitive_keys is None:
        # Use combined list of headers and params as defaults
        sensitive_keys = DEFAULT_SENSITIVE_HEADERS + DEFAULT_SENSITIVE_PARAMS

    # Convert sensitive keys to lowercase for case-insensitive matching
    sensitive_lower = {k.lower() for k in sensitive_keys}

    sanitized: dict[str, Any] = {}
    for key, value in data.items():
        if key.lower() in sensitive_lower:
            sanitized[key] = redacted
        elif recursive and isinstance(value, dict):
            sanitized[key] = sanitize_dict(value, sensitive_keys, redacted, recursive)
        elif recursive and isinstance(value, list):
            # Sanitize list elements if they're dicts
            sanitized[key] = None
        else:
            sanitized[key] = value

    return sanitized


def x_sanitize_dict__mutmut_23(
    data: dict[str, Any],
    sensitive_keys: list[str] | None = None,
    redacted: str = REDACTED_VALUE,
    recursive: bool = True,
) -> dict[str, Any]:
    """Sanitize sensitive keys in dictionary for safe logging.

    Args:
        data: Dictionary to sanitize
        sensitive_keys: List of keys to redact (case-insensitive)
        redacted: Replacement value for redacted values
        recursive: Whether to recursively sanitize nested dicts

    Returns:
        Sanitized dictionary

    """
    if sensitive_keys is None:
        # Use combined list of headers and params as defaults
        sensitive_keys = DEFAULT_SENSITIVE_HEADERS + DEFAULT_SENSITIVE_PARAMS

    # Convert sensitive keys to lowercase for case-insensitive matching
    sensitive_lower = {k.lower() for k in sensitive_keys}

    sanitized: dict[str, Any] = {}
    for key, value in data.items():
        if key.lower() in sensitive_lower:
            sanitized[key] = redacted
        elif recursive and isinstance(value, dict):
            sanitized[key] = sanitize_dict(value, sensitive_keys, redacted, recursive)
        elif recursive and isinstance(value, list):
            # Sanitize list elements if they're dicts
            sanitized[key] = [
                sanitize_dict(None, sensitive_keys, redacted, recursive) if isinstance(item, dict) else item
                for item in value
            ]
        else:
            sanitized[key] = value

    return sanitized


def x_sanitize_dict__mutmut_24(
    data: dict[str, Any],
    sensitive_keys: list[str] | None = None,
    redacted: str = REDACTED_VALUE,
    recursive: bool = True,
) -> dict[str, Any]:
    """Sanitize sensitive keys in dictionary for safe logging.

    Args:
        data: Dictionary to sanitize
        sensitive_keys: List of keys to redact (case-insensitive)
        redacted: Replacement value for redacted values
        recursive: Whether to recursively sanitize nested dicts

    Returns:
        Sanitized dictionary

    """
    if sensitive_keys is None:
        # Use combined list of headers and params as defaults
        sensitive_keys = DEFAULT_SENSITIVE_HEADERS + DEFAULT_SENSITIVE_PARAMS

    # Convert sensitive keys to lowercase for case-insensitive matching
    sensitive_lower = {k.lower() for k in sensitive_keys}

    sanitized: dict[str, Any] = {}
    for key, value in data.items():
        if key.lower() in sensitive_lower:
            sanitized[key] = redacted
        elif recursive and isinstance(value, dict):
            sanitized[key] = sanitize_dict(value, sensitive_keys, redacted, recursive)
        elif recursive and isinstance(value, list):
            # Sanitize list elements if they're dicts
            sanitized[key] = [
                sanitize_dict(item, None, redacted, recursive) if isinstance(item, dict) else item
                for item in value
            ]
        else:
            sanitized[key] = value

    return sanitized


def x_sanitize_dict__mutmut_25(
    data: dict[str, Any],
    sensitive_keys: list[str] | None = None,
    redacted: str = REDACTED_VALUE,
    recursive: bool = True,
) -> dict[str, Any]:
    """Sanitize sensitive keys in dictionary for safe logging.

    Args:
        data: Dictionary to sanitize
        sensitive_keys: List of keys to redact (case-insensitive)
        redacted: Replacement value for redacted values
        recursive: Whether to recursively sanitize nested dicts

    Returns:
        Sanitized dictionary

    """
    if sensitive_keys is None:
        # Use combined list of headers and params as defaults
        sensitive_keys = DEFAULT_SENSITIVE_HEADERS + DEFAULT_SENSITIVE_PARAMS

    # Convert sensitive keys to lowercase for case-insensitive matching
    sensitive_lower = {k.lower() for k in sensitive_keys}

    sanitized: dict[str, Any] = {}
    for key, value in data.items():
        if key.lower() in sensitive_lower:
            sanitized[key] = redacted
        elif recursive and isinstance(value, dict):
            sanitized[key] = sanitize_dict(value, sensitive_keys, redacted, recursive)
        elif recursive and isinstance(value, list):
            # Sanitize list elements if they're dicts
            sanitized[key] = [
                sanitize_dict(item, sensitive_keys, None, recursive) if isinstance(item, dict) else item
                for item in value
            ]
        else:
            sanitized[key] = value

    return sanitized


def x_sanitize_dict__mutmut_26(
    data: dict[str, Any],
    sensitive_keys: list[str] | None = None,
    redacted: str = REDACTED_VALUE,
    recursive: bool = True,
) -> dict[str, Any]:
    """Sanitize sensitive keys in dictionary for safe logging.

    Args:
        data: Dictionary to sanitize
        sensitive_keys: List of keys to redact (case-insensitive)
        redacted: Replacement value for redacted values
        recursive: Whether to recursively sanitize nested dicts

    Returns:
        Sanitized dictionary

    """
    if sensitive_keys is None:
        # Use combined list of headers and params as defaults
        sensitive_keys = DEFAULT_SENSITIVE_HEADERS + DEFAULT_SENSITIVE_PARAMS

    # Convert sensitive keys to lowercase for case-insensitive matching
    sensitive_lower = {k.lower() for k in sensitive_keys}

    sanitized: dict[str, Any] = {}
    for key, value in data.items():
        if key.lower() in sensitive_lower:
            sanitized[key] = redacted
        elif recursive and isinstance(value, dict):
            sanitized[key] = sanitize_dict(value, sensitive_keys, redacted, recursive)
        elif recursive and isinstance(value, list):
            # Sanitize list elements if they're dicts
            sanitized[key] = [
                sanitize_dict(item, sensitive_keys, redacted, None) if isinstance(item, dict) else item
                for item in value
            ]
        else:
            sanitized[key] = value

    return sanitized


def x_sanitize_dict__mutmut_27(
    data: dict[str, Any],
    sensitive_keys: list[str] | None = None,
    redacted: str = REDACTED_VALUE,
    recursive: bool = True,
) -> dict[str, Any]:
    """Sanitize sensitive keys in dictionary for safe logging.

    Args:
        data: Dictionary to sanitize
        sensitive_keys: List of keys to redact (case-insensitive)
        redacted: Replacement value for redacted values
        recursive: Whether to recursively sanitize nested dicts

    Returns:
        Sanitized dictionary

    """
    if sensitive_keys is None:
        # Use combined list of headers and params as defaults
        sensitive_keys = DEFAULT_SENSITIVE_HEADERS + DEFAULT_SENSITIVE_PARAMS

    # Convert sensitive keys to lowercase for case-insensitive matching
    sensitive_lower = {k.lower() for k in sensitive_keys}

    sanitized: dict[str, Any] = {}
    for key, value in data.items():
        if key.lower() in sensitive_lower:
            sanitized[key] = redacted
        elif recursive and isinstance(value, dict):
            sanitized[key] = sanitize_dict(value, sensitive_keys, redacted, recursive)
        elif recursive and isinstance(value, list):
            # Sanitize list elements if they're dicts
            sanitized[key] = [
                sanitize_dict(sensitive_keys, redacted, recursive) if isinstance(item, dict) else item
                for item in value
            ]
        else:
            sanitized[key] = value

    return sanitized


def x_sanitize_dict__mutmut_28(
    data: dict[str, Any],
    sensitive_keys: list[str] | None = None,
    redacted: str = REDACTED_VALUE,
    recursive: bool = True,
) -> dict[str, Any]:
    """Sanitize sensitive keys in dictionary for safe logging.

    Args:
        data: Dictionary to sanitize
        sensitive_keys: List of keys to redact (case-insensitive)
        redacted: Replacement value for redacted values
        recursive: Whether to recursively sanitize nested dicts

    Returns:
        Sanitized dictionary

    """
    if sensitive_keys is None:
        # Use combined list of headers and params as defaults
        sensitive_keys = DEFAULT_SENSITIVE_HEADERS + DEFAULT_SENSITIVE_PARAMS

    # Convert sensitive keys to lowercase for case-insensitive matching
    sensitive_lower = {k.lower() for k in sensitive_keys}

    sanitized: dict[str, Any] = {}
    for key, value in data.items():
        if key.lower() in sensitive_lower:
            sanitized[key] = redacted
        elif recursive and isinstance(value, dict):
            sanitized[key] = sanitize_dict(value, sensitive_keys, redacted, recursive)
        elif recursive and isinstance(value, list):
            # Sanitize list elements if they're dicts
            sanitized[key] = [
                sanitize_dict(item, redacted, recursive) if isinstance(item, dict) else item
                for item in value
            ]
        else:
            sanitized[key] = value

    return sanitized


def x_sanitize_dict__mutmut_29(
    data: dict[str, Any],
    sensitive_keys: list[str] | None = None,
    redacted: str = REDACTED_VALUE,
    recursive: bool = True,
) -> dict[str, Any]:
    """Sanitize sensitive keys in dictionary for safe logging.

    Args:
        data: Dictionary to sanitize
        sensitive_keys: List of keys to redact (case-insensitive)
        redacted: Replacement value for redacted values
        recursive: Whether to recursively sanitize nested dicts

    Returns:
        Sanitized dictionary

    """
    if sensitive_keys is None:
        # Use combined list of headers and params as defaults
        sensitive_keys = DEFAULT_SENSITIVE_HEADERS + DEFAULT_SENSITIVE_PARAMS

    # Convert sensitive keys to lowercase for case-insensitive matching
    sensitive_lower = {k.lower() for k in sensitive_keys}

    sanitized: dict[str, Any] = {}
    for key, value in data.items():
        if key.lower() in sensitive_lower:
            sanitized[key] = redacted
        elif recursive and isinstance(value, dict):
            sanitized[key] = sanitize_dict(value, sensitive_keys, redacted, recursive)
        elif recursive and isinstance(value, list):
            # Sanitize list elements if they're dicts
            sanitized[key] = [
                sanitize_dict(item, sensitive_keys, recursive) if isinstance(item, dict) else item
                for item in value
            ]
        else:
            sanitized[key] = value

    return sanitized


def x_sanitize_dict__mutmut_30(
    data: dict[str, Any],
    sensitive_keys: list[str] | None = None,
    redacted: str = REDACTED_VALUE,
    recursive: bool = True,
) -> dict[str, Any]:
    """Sanitize sensitive keys in dictionary for safe logging.

    Args:
        data: Dictionary to sanitize
        sensitive_keys: List of keys to redact (case-insensitive)
        redacted: Replacement value for redacted values
        recursive: Whether to recursively sanitize nested dicts

    Returns:
        Sanitized dictionary

    """
    if sensitive_keys is None:
        # Use combined list of headers and params as defaults
        sensitive_keys = DEFAULT_SENSITIVE_HEADERS + DEFAULT_SENSITIVE_PARAMS

    # Convert sensitive keys to lowercase for case-insensitive matching
    sensitive_lower = {k.lower() for k in sensitive_keys}

    sanitized: dict[str, Any] = {}
    for key, value in data.items():
        if key.lower() in sensitive_lower:
            sanitized[key] = redacted
        elif recursive and isinstance(value, dict):
            sanitized[key] = sanitize_dict(value, sensitive_keys, redacted, recursive)
        elif recursive and isinstance(value, list):
            # Sanitize list elements if they're dicts
            sanitized[key] = [
                sanitize_dict(item, sensitive_keys, redacted, ) if isinstance(item, dict) else item
                for item in value
            ]
        else:
            sanitized[key] = value

    return sanitized


def x_sanitize_dict__mutmut_31(
    data: dict[str, Any],
    sensitive_keys: list[str] | None = None,
    redacted: str = REDACTED_VALUE,
    recursive: bool = True,
) -> dict[str, Any]:
    """Sanitize sensitive keys in dictionary for safe logging.

    Args:
        data: Dictionary to sanitize
        sensitive_keys: List of keys to redact (case-insensitive)
        redacted: Replacement value for redacted values
        recursive: Whether to recursively sanitize nested dicts

    Returns:
        Sanitized dictionary

    """
    if sensitive_keys is None:
        # Use combined list of headers and params as defaults
        sensitive_keys = DEFAULT_SENSITIVE_HEADERS + DEFAULT_SENSITIVE_PARAMS

    # Convert sensitive keys to lowercase for case-insensitive matching
    sensitive_lower = {k.lower() for k in sensitive_keys}

    sanitized: dict[str, Any] = {}
    for key, value in data.items():
        if key.lower() in sensitive_lower:
            sanitized[key] = redacted
        elif recursive and isinstance(value, dict):
            sanitized[key] = sanitize_dict(value, sensitive_keys, redacted, recursive)
        elif recursive and isinstance(value, list):
            # Sanitize list elements if they're dicts
            sanitized[key] = [
                sanitize_dict(item, sensitive_keys, redacted, recursive) if isinstance(item, dict) else item
                for item in value
            ]
        else:
            sanitized[key] = None

    return sanitized

x_sanitize_dict__mutmut_mutants : ClassVar[MutantDict] = {
'x_sanitize_dict__mutmut_1': x_sanitize_dict__mutmut_1, 
    'x_sanitize_dict__mutmut_2': x_sanitize_dict__mutmut_2, 
    'x_sanitize_dict__mutmut_3': x_sanitize_dict__mutmut_3, 
    'x_sanitize_dict__mutmut_4': x_sanitize_dict__mutmut_4, 
    'x_sanitize_dict__mutmut_5': x_sanitize_dict__mutmut_5, 
    'x_sanitize_dict__mutmut_6': x_sanitize_dict__mutmut_6, 
    'x_sanitize_dict__mutmut_7': x_sanitize_dict__mutmut_7, 
    'x_sanitize_dict__mutmut_8': x_sanitize_dict__mutmut_8, 
    'x_sanitize_dict__mutmut_9': x_sanitize_dict__mutmut_9, 
    'x_sanitize_dict__mutmut_10': x_sanitize_dict__mutmut_10, 
    'x_sanitize_dict__mutmut_11': x_sanitize_dict__mutmut_11, 
    'x_sanitize_dict__mutmut_12': x_sanitize_dict__mutmut_12, 
    'x_sanitize_dict__mutmut_13': x_sanitize_dict__mutmut_13, 
    'x_sanitize_dict__mutmut_14': x_sanitize_dict__mutmut_14, 
    'x_sanitize_dict__mutmut_15': x_sanitize_dict__mutmut_15, 
    'x_sanitize_dict__mutmut_16': x_sanitize_dict__mutmut_16, 
    'x_sanitize_dict__mutmut_17': x_sanitize_dict__mutmut_17, 
    'x_sanitize_dict__mutmut_18': x_sanitize_dict__mutmut_18, 
    'x_sanitize_dict__mutmut_19': x_sanitize_dict__mutmut_19, 
    'x_sanitize_dict__mutmut_20': x_sanitize_dict__mutmut_20, 
    'x_sanitize_dict__mutmut_21': x_sanitize_dict__mutmut_21, 
    'x_sanitize_dict__mutmut_22': x_sanitize_dict__mutmut_22, 
    'x_sanitize_dict__mutmut_23': x_sanitize_dict__mutmut_23, 
    'x_sanitize_dict__mutmut_24': x_sanitize_dict__mutmut_24, 
    'x_sanitize_dict__mutmut_25': x_sanitize_dict__mutmut_25, 
    'x_sanitize_dict__mutmut_26': x_sanitize_dict__mutmut_26, 
    'x_sanitize_dict__mutmut_27': x_sanitize_dict__mutmut_27, 
    'x_sanitize_dict__mutmut_28': x_sanitize_dict__mutmut_28, 
    'x_sanitize_dict__mutmut_29': x_sanitize_dict__mutmut_29, 
    'x_sanitize_dict__mutmut_30': x_sanitize_dict__mutmut_30, 
    'x_sanitize_dict__mutmut_31': x_sanitize_dict__mutmut_31
}

def sanitize_dict(*args, **kwargs):
    result = _mutmut_trampoline(x_sanitize_dict__mutmut_orig, x_sanitize_dict__mutmut_mutants, args, kwargs)
    return result 

sanitize_dict.__signature__ = _mutmut_signature(x_sanitize_dict__mutmut_orig)
x_sanitize_dict__mutmut_orig.__name__ = 'x_sanitize_dict'


def x_should_sanitize_body__mutmut_orig(content_type: str | None) -> bool:
    """Determine if body should be sanitized based on content type.

    Args:
        content_type: Content-Type header value

    Returns:
        True if body should be sanitized

    """
    if not content_type:
        return False

    # Sanitize JSON and form data, skip binary formats
    content_type_lower = content_type.lower()
    return any(
        ct in content_type_lower
        for ct in [
            "application/json",
            "application/x-www-form-urlencoded",
            "multipart/form-data",
            "text/plain",
        ]
    )


def x_should_sanitize_body__mutmut_1(content_type: str | None) -> bool:
    """Determine if body should be sanitized based on content type.

    Args:
        content_type: Content-Type header value

    Returns:
        True if body should be sanitized

    """
    if content_type:
        return False

    # Sanitize JSON and form data, skip binary formats
    content_type_lower = content_type.lower()
    return any(
        ct in content_type_lower
        for ct in [
            "application/json",
            "application/x-www-form-urlencoded",
            "multipart/form-data",
            "text/plain",
        ]
    )


def x_should_sanitize_body__mutmut_2(content_type: str | None) -> bool:
    """Determine if body should be sanitized based on content type.

    Args:
        content_type: Content-Type header value

    Returns:
        True if body should be sanitized

    """
    if not content_type:
        return True

    # Sanitize JSON and form data, skip binary formats
    content_type_lower = content_type.lower()
    return any(
        ct in content_type_lower
        for ct in [
            "application/json",
            "application/x-www-form-urlencoded",
            "multipart/form-data",
            "text/plain",
        ]
    )


def x_should_sanitize_body__mutmut_3(content_type: str | None) -> bool:
    """Determine if body should be sanitized based on content type.

    Args:
        content_type: Content-Type header value

    Returns:
        True if body should be sanitized

    """
    if not content_type:
        return False

    # Sanitize JSON and form data, skip binary formats
    content_type_lower = None
    return any(
        ct in content_type_lower
        for ct in [
            "application/json",
            "application/x-www-form-urlencoded",
            "multipart/form-data",
            "text/plain",
        ]
    )


def x_should_sanitize_body__mutmut_4(content_type: str | None) -> bool:
    """Determine if body should be sanitized based on content type.

    Args:
        content_type: Content-Type header value

    Returns:
        True if body should be sanitized

    """
    if not content_type:
        return False

    # Sanitize JSON and form data, skip binary formats
    content_type_lower = content_type.upper()
    return any(
        ct in content_type_lower
        for ct in [
            "application/json",
            "application/x-www-form-urlencoded",
            "multipart/form-data",
            "text/plain",
        ]
    )


def x_should_sanitize_body__mutmut_5(content_type: str | None) -> bool:
    """Determine if body should be sanitized based on content type.

    Args:
        content_type: Content-Type header value

    Returns:
        True if body should be sanitized

    """
    if not content_type:
        return False

    # Sanitize JSON and form data, skip binary formats
    content_type_lower = content_type.lower()
    return any(
        None
    )


def x_should_sanitize_body__mutmut_6(content_type: str | None) -> bool:
    """Determine if body should be sanitized based on content type.

    Args:
        content_type: Content-Type header value

    Returns:
        True if body should be sanitized

    """
    if not content_type:
        return False

    # Sanitize JSON and form data, skip binary formats
    content_type_lower = content_type.lower()
    return any(
        ct not in content_type_lower
        for ct in [
            "application/json",
            "application/x-www-form-urlencoded",
            "multipart/form-data",
            "text/plain",
        ]
    )


def x_should_sanitize_body__mutmut_7(content_type: str | None) -> bool:
    """Determine if body should be sanitized based on content type.

    Args:
        content_type: Content-Type header value

    Returns:
        True if body should be sanitized

    """
    if not content_type:
        return False

    # Sanitize JSON and form data, skip binary formats
    content_type_lower = content_type.lower()
    return any(
        ct in content_type_lower
        for ct in [
            "XXapplication/jsonXX",
            "application/x-www-form-urlencoded",
            "multipart/form-data",
            "text/plain",
        ]
    )


def x_should_sanitize_body__mutmut_8(content_type: str | None) -> bool:
    """Determine if body should be sanitized based on content type.

    Args:
        content_type: Content-Type header value

    Returns:
        True if body should be sanitized

    """
    if not content_type:
        return False

    # Sanitize JSON and form data, skip binary formats
    content_type_lower = content_type.lower()
    return any(
        ct in content_type_lower
        for ct in [
            "APPLICATION/JSON",
            "application/x-www-form-urlencoded",
            "multipart/form-data",
            "text/plain",
        ]
    )


def x_should_sanitize_body__mutmut_9(content_type: str | None) -> bool:
    """Determine if body should be sanitized based on content type.

    Args:
        content_type: Content-Type header value

    Returns:
        True if body should be sanitized

    """
    if not content_type:
        return False

    # Sanitize JSON and form data, skip binary formats
    content_type_lower = content_type.lower()
    return any(
        ct in content_type_lower
        for ct in [
            "application/json",
            "XXapplication/x-www-form-urlencodedXX",
            "multipart/form-data",
            "text/plain",
        ]
    )


def x_should_sanitize_body__mutmut_10(content_type: str | None) -> bool:
    """Determine if body should be sanitized based on content type.

    Args:
        content_type: Content-Type header value

    Returns:
        True if body should be sanitized

    """
    if not content_type:
        return False

    # Sanitize JSON and form data, skip binary formats
    content_type_lower = content_type.lower()
    return any(
        ct in content_type_lower
        for ct in [
            "application/json",
            "APPLICATION/X-WWW-FORM-URLENCODED",
            "multipart/form-data",
            "text/plain",
        ]
    )


def x_should_sanitize_body__mutmut_11(content_type: str | None) -> bool:
    """Determine if body should be sanitized based on content type.

    Args:
        content_type: Content-Type header value

    Returns:
        True if body should be sanitized

    """
    if not content_type:
        return False

    # Sanitize JSON and form data, skip binary formats
    content_type_lower = content_type.lower()
    return any(
        ct in content_type_lower
        for ct in [
            "application/json",
            "application/x-www-form-urlencoded",
            "XXmultipart/form-dataXX",
            "text/plain",
        ]
    )


def x_should_sanitize_body__mutmut_12(content_type: str | None) -> bool:
    """Determine if body should be sanitized based on content type.

    Args:
        content_type: Content-Type header value

    Returns:
        True if body should be sanitized

    """
    if not content_type:
        return False

    # Sanitize JSON and form data, skip binary formats
    content_type_lower = content_type.lower()
    return any(
        ct in content_type_lower
        for ct in [
            "application/json",
            "application/x-www-form-urlencoded",
            "MULTIPART/FORM-DATA",
            "text/plain",
        ]
    )


def x_should_sanitize_body__mutmut_13(content_type: str | None) -> bool:
    """Determine if body should be sanitized based on content type.

    Args:
        content_type: Content-Type header value

    Returns:
        True if body should be sanitized

    """
    if not content_type:
        return False

    # Sanitize JSON and form data, skip binary formats
    content_type_lower = content_type.lower()
    return any(
        ct in content_type_lower
        for ct in [
            "application/json",
            "application/x-www-form-urlencoded",
            "multipart/form-data",
            "XXtext/plainXX",
        ]
    )


def x_should_sanitize_body__mutmut_14(content_type: str | None) -> bool:
    """Determine if body should be sanitized based on content type.

    Args:
        content_type: Content-Type header value

    Returns:
        True if body should be sanitized

    """
    if not content_type:
        return False

    # Sanitize JSON and form data, skip binary formats
    content_type_lower = content_type.lower()
    return any(
        ct in content_type_lower
        for ct in [
            "application/json",
            "application/x-www-form-urlencoded",
            "multipart/form-data",
            "TEXT/PLAIN",
        ]
    )

x_should_sanitize_body__mutmut_mutants : ClassVar[MutantDict] = {
'x_should_sanitize_body__mutmut_1': x_should_sanitize_body__mutmut_1, 
    'x_should_sanitize_body__mutmut_2': x_should_sanitize_body__mutmut_2, 
    'x_should_sanitize_body__mutmut_3': x_should_sanitize_body__mutmut_3, 
    'x_should_sanitize_body__mutmut_4': x_should_sanitize_body__mutmut_4, 
    'x_should_sanitize_body__mutmut_5': x_should_sanitize_body__mutmut_5, 
    'x_should_sanitize_body__mutmut_6': x_should_sanitize_body__mutmut_6, 
    'x_should_sanitize_body__mutmut_7': x_should_sanitize_body__mutmut_7, 
    'x_should_sanitize_body__mutmut_8': x_should_sanitize_body__mutmut_8, 
    'x_should_sanitize_body__mutmut_9': x_should_sanitize_body__mutmut_9, 
    'x_should_sanitize_body__mutmut_10': x_should_sanitize_body__mutmut_10, 
    'x_should_sanitize_body__mutmut_11': x_should_sanitize_body__mutmut_11, 
    'x_should_sanitize_body__mutmut_12': x_should_sanitize_body__mutmut_12, 
    'x_should_sanitize_body__mutmut_13': x_should_sanitize_body__mutmut_13, 
    'x_should_sanitize_body__mutmut_14': x_should_sanitize_body__mutmut_14
}

def should_sanitize_body(*args, **kwargs):
    result = _mutmut_trampoline(x_should_sanitize_body__mutmut_orig, x_should_sanitize_body__mutmut_mutants, args, kwargs)
    return result 

should_sanitize_body.__signature__ = _mutmut_signature(x_should_sanitize_body__mutmut_orig)
x_should_sanitize_body__mutmut_orig.__name__ = 'x_should_sanitize_body'


__all__ = [
    "DEFAULT_SENSITIVE_HEADERS",
    "DEFAULT_SENSITIVE_PARAMS",
    "REDACTED_VALUE",
    "sanitize_dict",
    "sanitize_headers",
    "sanitize_uri",
    "should_sanitize_body",
]


# <3 🧱🤝🛡️🪄
