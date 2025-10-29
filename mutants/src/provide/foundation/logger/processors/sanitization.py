# provide/foundation/logger/processors/sanitization.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from typing import Any

import structlog

from provide.foundation.security import mask_secrets, sanitize_dict

"""Security sanitization processor for logger.

Automatically sanitizes sensitive data from log messages using Foundation's
security utilities.
"""
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


def x_create_sanitization_processor__mutmut_orig(
    enabled: bool = True,
    mask_patterns: bool = True,
    sanitize_dicts: bool = True,
) -> Any:
    """Create a processor that sanitizes sensitive data from logs.

    This processor uses Foundation's security utilities to automatically:
    - Mask secrets based on common patterns (API keys, tokens, passwords)
    - Sanitize dictionary keys (Authorization, X-API-Key, etc.)

    Args:
        enabled: Whether sanitization is enabled
        mask_patterns: Whether to apply pattern-based secret masking
        sanitize_dicts: Whether to sanitize dictionary values

    Returns:
        Structlog processor function

    Examples:
        >>> log.info("API call", headers={"Authorization": "Bearer secret123"})
        # Logs: {"Authorization": "Bearer ***"}

        >>> log.info("Config loaded", api_key="sk-1234567890abcdef")
        # Logs: api_key="***"

    """

    def sanitization_processor(
        _logger: Any,
        _method_name: str,
        event_dict: structlog.types.EventDict,
    ) -> structlog.types.EventDict:
        """Apply sanitization to event dictionary."""
        if not enabled:
            return event_dict

        # Create a new dict to avoid modifying the original
        sanitized = event_dict.copy()

        # Sanitize dictionary values (headers, config, etc.)
        if sanitize_dicts:
            for key, value in list(sanitized.items()):
                if isinstance(value, dict):
                    sanitized[key] = sanitize_dict(value)

        # Mask secrets in string values
        if mask_patterns:
            for key, value in list(sanitized.items()):
                if isinstance(value, str):
                    sanitized[key] = mask_secrets(value)

        return sanitized

    return sanitization_processor


def x_create_sanitization_processor__mutmut_1(
    enabled: bool = False,
    mask_patterns: bool = True,
    sanitize_dicts: bool = True,
) -> Any:
    """Create a processor that sanitizes sensitive data from logs.

    This processor uses Foundation's security utilities to automatically:
    - Mask secrets based on common patterns (API keys, tokens, passwords)
    - Sanitize dictionary keys (Authorization, X-API-Key, etc.)

    Args:
        enabled: Whether sanitization is enabled
        mask_patterns: Whether to apply pattern-based secret masking
        sanitize_dicts: Whether to sanitize dictionary values

    Returns:
        Structlog processor function

    Examples:
        >>> log.info("API call", headers={"Authorization": "Bearer secret123"})
        # Logs: {"Authorization": "Bearer ***"}

        >>> log.info("Config loaded", api_key="sk-1234567890abcdef")
        # Logs: api_key="***"

    """

    def sanitization_processor(
        _logger: Any,
        _method_name: str,
        event_dict: structlog.types.EventDict,
    ) -> structlog.types.EventDict:
        """Apply sanitization to event dictionary."""
        if not enabled:
            return event_dict

        # Create a new dict to avoid modifying the original
        sanitized = event_dict.copy()

        # Sanitize dictionary values (headers, config, etc.)
        if sanitize_dicts:
            for key, value in list(sanitized.items()):
                if isinstance(value, dict):
                    sanitized[key] = sanitize_dict(value)

        # Mask secrets in string values
        if mask_patterns:
            for key, value in list(sanitized.items()):
                if isinstance(value, str):
                    sanitized[key] = mask_secrets(value)

        return sanitized

    return sanitization_processor


def x_create_sanitization_processor__mutmut_2(
    enabled: bool = True,
    mask_patterns: bool = False,
    sanitize_dicts: bool = True,
) -> Any:
    """Create a processor that sanitizes sensitive data from logs.

    This processor uses Foundation's security utilities to automatically:
    - Mask secrets based on common patterns (API keys, tokens, passwords)
    - Sanitize dictionary keys (Authorization, X-API-Key, etc.)

    Args:
        enabled: Whether sanitization is enabled
        mask_patterns: Whether to apply pattern-based secret masking
        sanitize_dicts: Whether to sanitize dictionary values

    Returns:
        Structlog processor function

    Examples:
        >>> log.info("API call", headers={"Authorization": "Bearer secret123"})
        # Logs: {"Authorization": "Bearer ***"}

        >>> log.info("Config loaded", api_key="sk-1234567890abcdef")
        # Logs: api_key="***"

    """

    def sanitization_processor(
        _logger: Any,
        _method_name: str,
        event_dict: structlog.types.EventDict,
    ) -> structlog.types.EventDict:
        """Apply sanitization to event dictionary."""
        if not enabled:
            return event_dict

        # Create a new dict to avoid modifying the original
        sanitized = event_dict.copy()

        # Sanitize dictionary values (headers, config, etc.)
        if sanitize_dicts:
            for key, value in list(sanitized.items()):
                if isinstance(value, dict):
                    sanitized[key] = sanitize_dict(value)

        # Mask secrets in string values
        if mask_patterns:
            for key, value in list(sanitized.items()):
                if isinstance(value, str):
                    sanitized[key] = mask_secrets(value)

        return sanitized

    return sanitization_processor


def x_create_sanitization_processor__mutmut_3(
    enabled: bool = True,
    mask_patterns: bool = True,
    sanitize_dicts: bool = False,
) -> Any:
    """Create a processor that sanitizes sensitive data from logs.

    This processor uses Foundation's security utilities to automatically:
    - Mask secrets based on common patterns (API keys, tokens, passwords)
    - Sanitize dictionary keys (Authorization, X-API-Key, etc.)

    Args:
        enabled: Whether sanitization is enabled
        mask_patterns: Whether to apply pattern-based secret masking
        sanitize_dicts: Whether to sanitize dictionary values

    Returns:
        Structlog processor function

    Examples:
        >>> log.info("API call", headers={"Authorization": "Bearer secret123"})
        # Logs: {"Authorization": "Bearer ***"}

        >>> log.info("Config loaded", api_key="sk-1234567890abcdef")
        # Logs: api_key="***"

    """

    def sanitization_processor(
        _logger: Any,
        _method_name: str,
        event_dict: structlog.types.EventDict,
    ) -> structlog.types.EventDict:
        """Apply sanitization to event dictionary."""
        if not enabled:
            return event_dict

        # Create a new dict to avoid modifying the original
        sanitized = event_dict.copy()

        # Sanitize dictionary values (headers, config, etc.)
        if sanitize_dicts:
            for key, value in list(sanitized.items()):
                if isinstance(value, dict):
                    sanitized[key] = sanitize_dict(value)

        # Mask secrets in string values
        if mask_patterns:
            for key, value in list(sanitized.items()):
                if isinstance(value, str):
                    sanitized[key] = mask_secrets(value)

        return sanitized

    return sanitization_processor


def x_create_sanitization_processor__mutmut_4(
    enabled: bool = True,
    mask_patterns: bool = True,
    sanitize_dicts: bool = True,
) -> Any:
    """Create a processor that sanitizes sensitive data from logs.

    This processor uses Foundation's security utilities to automatically:
    - Mask secrets based on common patterns (API keys, tokens, passwords)
    - Sanitize dictionary keys (Authorization, X-API-Key, etc.)

    Args:
        enabled: Whether sanitization is enabled
        mask_patterns: Whether to apply pattern-based secret masking
        sanitize_dicts: Whether to sanitize dictionary values

    Returns:
        Structlog processor function

    Examples:
        >>> log.info("API call", headers={"Authorization": "Bearer secret123"})
        # Logs: {"Authorization": "Bearer ***"}

        >>> log.info("Config loaded", api_key="sk-1234567890abcdef")
        # Logs: api_key="***"

    """

    def sanitization_processor(
        _logger: Any,
        _method_name: str,
        event_dict: structlog.types.EventDict,
    ) -> structlog.types.EventDict:
        """Apply sanitization to event dictionary."""
        if enabled:
            return event_dict

        # Create a new dict to avoid modifying the original
        sanitized = event_dict.copy()

        # Sanitize dictionary values (headers, config, etc.)
        if sanitize_dicts:
            for key, value in list(sanitized.items()):
                if isinstance(value, dict):
                    sanitized[key] = sanitize_dict(value)

        # Mask secrets in string values
        if mask_patterns:
            for key, value in list(sanitized.items()):
                if isinstance(value, str):
                    sanitized[key] = mask_secrets(value)

        return sanitized

    return sanitization_processor


def x_create_sanitization_processor__mutmut_5(
    enabled: bool = True,
    mask_patterns: bool = True,
    sanitize_dicts: bool = True,
) -> Any:
    """Create a processor that sanitizes sensitive data from logs.

    This processor uses Foundation's security utilities to automatically:
    - Mask secrets based on common patterns (API keys, tokens, passwords)
    - Sanitize dictionary keys (Authorization, X-API-Key, etc.)

    Args:
        enabled: Whether sanitization is enabled
        mask_patterns: Whether to apply pattern-based secret masking
        sanitize_dicts: Whether to sanitize dictionary values

    Returns:
        Structlog processor function

    Examples:
        >>> log.info("API call", headers={"Authorization": "Bearer secret123"})
        # Logs: {"Authorization": "Bearer ***"}

        >>> log.info("Config loaded", api_key="sk-1234567890abcdef")
        # Logs: api_key="***"

    """

    def sanitization_processor(
        _logger: Any,
        _method_name: str,
        event_dict: structlog.types.EventDict,
    ) -> structlog.types.EventDict:
        """Apply sanitization to event dictionary."""
        if not enabled:
            return event_dict

        # Create a new dict to avoid modifying the original
        sanitized = None

        # Sanitize dictionary values (headers, config, etc.)
        if sanitize_dicts:
            for key, value in list(sanitized.items()):
                if isinstance(value, dict):
                    sanitized[key] = sanitize_dict(value)

        # Mask secrets in string values
        if mask_patterns:
            for key, value in list(sanitized.items()):
                if isinstance(value, str):
                    sanitized[key] = mask_secrets(value)

        return sanitized

    return sanitization_processor


def x_create_sanitization_processor__mutmut_6(
    enabled: bool = True,
    mask_patterns: bool = True,
    sanitize_dicts: bool = True,
) -> Any:
    """Create a processor that sanitizes sensitive data from logs.

    This processor uses Foundation's security utilities to automatically:
    - Mask secrets based on common patterns (API keys, tokens, passwords)
    - Sanitize dictionary keys (Authorization, X-API-Key, etc.)

    Args:
        enabled: Whether sanitization is enabled
        mask_patterns: Whether to apply pattern-based secret masking
        sanitize_dicts: Whether to sanitize dictionary values

    Returns:
        Structlog processor function

    Examples:
        >>> log.info("API call", headers={"Authorization": "Bearer secret123"})
        # Logs: {"Authorization": "Bearer ***"}

        >>> log.info("Config loaded", api_key="sk-1234567890abcdef")
        # Logs: api_key="***"

    """

    def sanitization_processor(
        _logger: Any,
        _method_name: str,
        event_dict: structlog.types.EventDict,
    ) -> structlog.types.EventDict:
        """Apply sanitization to event dictionary."""
        if not enabled:
            return event_dict

        # Create a new dict to avoid modifying the original
        sanitized = event_dict.copy()

        # Sanitize dictionary values (headers, config, etc.)
        if sanitize_dicts:
            for key, value in list(None):
                if isinstance(value, dict):
                    sanitized[key] = sanitize_dict(value)

        # Mask secrets in string values
        if mask_patterns:
            for key, value in list(sanitized.items()):
                if isinstance(value, str):
                    sanitized[key] = mask_secrets(value)

        return sanitized

    return sanitization_processor


def x_create_sanitization_processor__mutmut_7(
    enabled: bool = True,
    mask_patterns: bool = True,
    sanitize_dicts: bool = True,
) -> Any:
    """Create a processor that sanitizes sensitive data from logs.

    This processor uses Foundation's security utilities to automatically:
    - Mask secrets based on common patterns (API keys, tokens, passwords)
    - Sanitize dictionary keys (Authorization, X-API-Key, etc.)

    Args:
        enabled: Whether sanitization is enabled
        mask_patterns: Whether to apply pattern-based secret masking
        sanitize_dicts: Whether to sanitize dictionary values

    Returns:
        Structlog processor function

    Examples:
        >>> log.info("API call", headers={"Authorization": "Bearer secret123"})
        # Logs: {"Authorization": "Bearer ***"}

        >>> log.info("Config loaded", api_key="sk-1234567890abcdef")
        # Logs: api_key="***"

    """

    def sanitization_processor(
        _logger: Any,
        _method_name: str,
        event_dict: structlog.types.EventDict,
    ) -> structlog.types.EventDict:
        """Apply sanitization to event dictionary."""
        if not enabled:
            return event_dict

        # Create a new dict to avoid modifying the original
        sanitized = event_dict.copy()

        # Sanitize dictionary values (headers, config, etc.)
        if sanitize_dicts:
            for key, value in list(sanitized.items()):
                if isinstance(value, dict):
                    sanitized[key] = None

        # Mask secrets in string values
        if mask_patterns:
            for key, value in list(sanitized.items()):
                if isinstance(value, str):
                    sanitized[key] = mask_secrets(value)

        return sanitized

    return sanitization_processor


def x_create_sanitization_processor__mutmut_8(
    enabled: bool = True,
    mask_patterns: bool = True,
    sanitize_dicts: bool = True,
) -> Any:
    """Create a processor that sanitizes sensitive data from logs.

    This processor uses Foundation's security utilities to automatically:
    - Mask secrets based on common patterns (API keys, tokens, passwords)
    - Sanitize dictionary keys (Authorization, X-API-Key, etc.)

    Args:
        enabled: Whether sanitization is enabled
        mask_patterns: Whether to apply pattern-based secret masking
        sanitize_dicts: Whether to sanitize dictionary values

    Returns:
        Structlog processor function

    Examples:
        >>> log.info("API call", headers={"Authorization": "Bearer secret123"})
        # Logs: {"Authorization": "Bearer ***"}

        >>> log.info("Config loaded", api_key="sk-1234567890abcdef")
        # Logs: api_key="***"

    """

    def sanitization_processor(
        _logger: Any,
        _method_name: str,
        event_dict: structlog.types.EventDict,
    ) -> structlog.types.EventDict:
        """Apply sanitization to event dictionary."""
        if not enabled:
            return event_dict

        # Create a new dict to avoid modifying the original
        sanitized = event_dict.copy()

        # Sanitize dictionary values (headers, config, etc.)
        if sanitize_dicts:
            for key, value in list(sanitized.items()):
                if isinstance(value, dict):
                    sanitized[key] = sanitize_dict(None)

        # Mask secrets in string values
        if mask_patterns:
            for key, value in list(sanitized.items()):
                if isinstance(value, str):
                    sanitized[key] = mask_secrets(value)

        return sanitized

    return sanitization_processor


def x_create_sanitization_processor__mutmut_9(
    enabled: bool = True,
    mask_patterns: bool = True,
    sanitize_dicts: bool = True,
) -> Any:
    """Create a processor that sanitizes sensitive data from logs.

    This processor uses Foundation's security utilities to automatically:
    - Mask secrets based on common patterns (API keys, tokens, passwords)
    - Sanitize dictionary keys (Authorization, X-API-Key, etc.)

    Args:
        enabled: Whether sanitization is enabled
        mask_patterns: Whether to apply pattern-based secret masking
        sanitize_dicts: Whether to sanitize dictionary values

    Returns:
        Structlog processor function

    Examples:
        >>> log.info("API call", headers={"Authorization": "Bearer secret123"})
        # Logs: {"Authorization": "Bearer ***"}

        >>> log.info("Config loaded", api_key="sk-1234567890abcdef")
        # Logs: api_key="***"

    """

    def sanitization_processor(
        _logger: Any,
        _method_name: str,
        event_dict: structlog.types.EventDict,
    ) -> structlog.types.EventDict:
        """Apply sanitization to event dictionary."""
        if not enabled:
            return event_dict

        # Create a new dict to avoid modifying the original
        sanitized = event_dict.copy()

        # Sanitize dictionary values (headers, config, etc.)
        if sanitize_dicts:
            for key, value in list(sanitized.items()):
                if isinstance(value, dict):
                    sanitized[key] = sanitize_dict(value)

        # Mask secrets in string values
        if mask_patterns:
            for key, value in list(None):
                if isinstance(value, str):
                    sanitized[key] = mask_secrets(value)

        return sanitized

    return sanitization_processor


def x_create_sanitization_processor__mutmut_10(
    enabled: bool = True,
    mask_patterns: bool = True,
    sanitize_dicts: bool = True,
) -> Any:
    """Create a processor that sanitizes sensitive data from logs.

    This processor uses Foundation's security utilities to automatically:
    - Mask secrets based on common patterns (API keys, tokens, passwords)
    - Sanitize dictionary keys (Authorization, X-API-Key, etc.)

    Args:
        enabled: Whether sanitization is enabled
        mask_patterns: Whether to apply pattern-based secret masking
        sanitize_dicts: Whether to sanitize dictionary values

    Returns:
        Structlog processor function

    Examples:
        >>> log.info("API call", headers={"Authorization": "Bearer secret123"})
        # Logs: {"Authorization": "Bearer ***"}

        >>> log.info("Config loaded", api_key="sk-1234567890abcdef")
        # Logs: api_key="***"

    """

    def sanitization_processor(
        _logger: Any,
        _method_name: str,
        event_dict: structlog.types.EventDict,
    ) -> structlog.types.EventDict:
        """Apply sanitization to event dictionary."""
        if not enabled:
            return event_dict

        # Create a new dict to avoid modifying the original
        sanitized = event_dict.copy()

        # Sanitize dictionary values (headers, config, etc.)
        if sanitize_dicts:
            for key, value in list(sanitized.items()):
                if isinstance(value, dict):
                    sanitized[key] = sanitize_dict(value)

        # Mask secrets in string values
        if mask_patterns:
            for key, value in list(sanitized.items()):
                if isinstance(value, str):
                    sanitized[key] = None

        return sanitized

    return sanitization_processor


def x_create_sanitization_processor__mutmut_11(
    enabled: bool = True,
    mask_patterns: bool = True,
    sanitize_dicts: bool = True,
) -> Any:
    """Create a processor that sanitizes sensitive data from logs.

    This processor uses Foundation's security utilities to automatically:
    - Mask secrets based on common patterns (API keys, tokens, passwords)
    - Sanitize dictionary keys (Authorization, X-API-Key, etc.)

    Args:
        enabled: Whether sanitization is enabled
        mask_patterns: Whether to apply pattern-based secret masking
        sanitize_dicts: Whether to sanitize dictionary values

    Returns:
        Structlog processor function

    Examples:
        >>> log.info("API call", headers={"Authorization": "Bearer secret123"})
        # Logs: {"Authorization": "Bearer ***"}

        >>> log.info("Config loaded", api_key="sk-1234567890abcdef")
        # Logs: api_key="***"

    """

    def sanitization_processor(
        _logger: Any,
        _method_name: str,
        event_dict: structlog.types.EventDict,
    ) -> structlog.types.EventDict:
        """Apply sanitization to event dictionary."""
        if not enabled:
            return event_dict

        # Create a new dict to avoid modifying the original
        sanitized = event_dict.copy()

        # Sanitize dictionary values (headers, config, etc.)
        if sanitize_dicts:
            for key, value in list(sanitized.items()):
                if isinstance(value, dict):
                    sanitized[key] = sanitize_dict(value)

        # Mask secrets in string values
        if mask_patterns:
            for key, value in list(sanitized.items()):
                if isinstance(value, str):
                    sanitized[key] = mask_secrets(None)

        return sanitized

    return sanitization_processor


x_create_sanitization_processor__mutmut_mutants: ClassVar[MutantDict] = {
    "x_create_sanitization_processor__mutmut_1": x_create_sanitization_processor__mutmut_1,
    "x_create_sanitization_processor__mutmut_2": x_create_sanitization_processor__mutmut_2,
    "x_create_sanitization_processor__mutmut_3": x_create_sanitization_processor__mutmut_3,
    "x_create_sanitization_processor__mutmut_4": x_create_sanitization_processor__mutmut_4,
    "x_create_sanitization_processor__mutmut_5": x_create_sanitization_processor__mutmut_5,
    "x_create_sanitization_processor__mutmut_6": x_create_sanitization_processor__mutmut_6,
    "x_create_sanitization_processor__mutmut_7": x_create_sanitization_processor__mutmut_7,
    "x_create_sanitization_processor__mutmut_8": x_create_sanitization_processor__mutmut_8,
    "x_create_sanitization_processor__mutmut_9": x_create_sanitization_processor__mutmut_9,
    "x_create_sanitization_processor__mutmut_10": x_create_sanitization_processor__mutmut_10,
    "x_create_sanitization_processor__mutmut_11": x_create_sanitization_processor__mutmut_11,
}


def create_sanitization_processor(*args, **kwargs):
    result = _mutmut_trampoline(
        x_create_sanitization_processor__mutmut_orig,
        x_create_sanitization_processor__mutmut_mutants,
        args,
        kwargs,
    )
    return result


create_sanitization_processor.__signature__ = _mutmut_signature(x_create_sanitization_processor__mutmut_orig)
x_create_sanitization_processor__mutmut_orig.__name__ = "x_create_sanitization_processor"


__all__ = [
    "create_sanitization_processor",
]


# <3 🧱🤝📝🪄
