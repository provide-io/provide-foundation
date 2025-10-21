# provide/foundation/config/errors.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from typing import Any

from provide.foundation.errors.base import FoundationError

"""Configuration-specific error types and utilities.

Provides standardized error handling for configuration parsing and validation
with consistent messages and diagnostic context.
"""
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


class ConfigError(FoundationError):
    """Base configuration error."""

    def xǁConfigErrorǁ_default_code__mutmut_orig(self) -> str:
        return "CONFIG_ERROR"

    def xǁConfigErrorǁ_default_code__mutmut_1(self) -> str:
        return "XXCONFIG_ERRORXX"

    def xǁConfigErrorǁ_default_code__mutmut_2(self) -> str:
        return "config_error"
    
    xǁConfigErrorǁ_default_code__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁConfigErrorǁ_default_code__mutmut_1': xǁConfigErrorǁ_default_code__mutmut_1, 
        'xǁConfigErrorǁ_default_code__mutmut_2': xǁConfigErrorǁ_default_code__mutmut_2
    }
    
    def _default_code(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁConfigErrorǁ_default_code__mutmut_orig"), object.__getattribute__(self, "xǁConfigErrorǁ_default_code__mutmut_mutants"), args, kwargs, self)
        return result 
    
    _default_code.__signature__ = _mutmut_signature(xǁConfigErrorǁ_default_code__mutmut_orig)
    xǁConfigErrorǁ_default_code__mutmut_orig.__name__ = 'xǁConfigErrorǁ_default_code'


class ParseError(ConfigError):
    """Configuration value parsing failed."""

    def xǁParseErrorǁ__init____mutmut_orig(
        self,
        message: str,
        *,
        value: str | Any,
        field_name: str | None = None,
        expected_type: str | None = None,
        valid_options: list[str] | None = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(
            message,
            value=value,
            field_name=field_name,
            expected_type=expected_type,
            valid_options=valid_options,
            **kwargs,
        )

    def xǁParseErrorǁ__init____mutmut_1(
        self,
        message: str,
        *,
        value: str | Any,
        field_name: str | None = None,
        expected_type: str | None = None,
        valid_options: list[str] | None = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(
            None,
            value=value,
            field_name=field_name,
            expected_type=expected_type,
            valid_options=valid_options,
            **kwargs,
        )

    def xǁParseErrorǁ__init____mutmut_2(
        self,
        message: str,
        *,
        value: str | Any,
        field_name: str | None = None,
        expected_type: str | None = None,
        valid_options: list[str] | None = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(
            message,
            value=None,
            field_name=field_name,
            expected_type=expected_type,
            valid_options=valid_options,
            **kwargs,
        )

    def xǁParseErrorǁ__init____mutmut_3(
        self,
        message: str,
        *,
        value: str | Any,
        field_name: str | None = None,
        expected_type: str | None = None,
        valid_options: list[str] | None = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(
            message,
            value=value,
            field_name=None,
            expected_type=expected_type,
            valid_options=valid_options,
            **kwargs,
        )

    def xǁParseErrorǁ__init____mutmut_4(
        self,
        message: str,
        *,
        value: str | Any,
        field_name: str | None = None,
        expected_type: str | None = None,
        valid_options: list[str] | None = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(
            message,
            value=value,
            field_name=field_name,
            expected_type=None,
            valid_options=valid_options,
            **kwargs,
        )

    def xǁParseErrorǁ__init____mutmut_5(
        self,
        message: str,
        *,
        value: str | Any,
        field_name: str | None = None,
        expected_type: str | None = None,
        valid_options: list[str] | None = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(
            message,
            value=value,
            field_name=field_name,
            expected_type=expected_type,
            valid_options=None,
            **kwargs,
        )

    def xǁParseErrorǁ__init____mutmut_6(
        self,
        message: str,
        *,
        value: str | Any,
        field_name: str | None = None,
        expected_type: str | None = None,
        valid_options: list[str] | None = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(
            value=value,
            field_name=field_name,
            expected_type=expected_type,
            valid_options=valid_options,
            **kwargs,
        )

    def xǁParseErrorǁ__init____mutmut_7(
        self,
        message: str,
        *,
        value: str | Any,
        field_name: str | None = None,
        expected_type: str | None = None,
        valid_options: list[str] | None = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(
            message,
            field_name=field_name,
            expected_type=expected_type,
            valid_options=valid_options,
            **kwargs,
        )

    def xǁParseErrorǁ__init____mutmut_8(
        self,
        message: str,
        *,
        value: str | Any,
        field_name: str | None = None,
        expected_type: str | None = None,
        valid_options: list[str] | None = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(
            message,
            value=value,
            expected_type=expected_type,
            valid_options=valid_options,
            **kwargs,
        )

    def xǁParseErrorǁ__init____mutmut_9(
        self,
        message: str,
        *,
        value: str | Any,
        field_name: str | None = None,
        expected_type: str | None = None,
        valid_options: list[str] | None = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(
            message,
            value=value,
            field_name=field_name,
            valid_options=valid_options,
            **kwargs,
        )

    def xǁParseErrorǁ__init____mutmut_10(
        self,
        message: str,
        *,
        value: str | Any,
        field_name: str | None = None,
        expected_type: str | None = None,
        valid_options: list[str] | None = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(
            message,
            value=value,
            field_name=field_name,
            expected_type=expected_type,
            **kwargs,
        )

    def xǁParseErrorǁ__init____mutmut_11(
        self,
        message: str,
        *,
        value: str | Any,
        field_name: str | None = None,
        expected_type: str | None = None,
        valid_options: list[str] | None = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(
            message,
            value=value,
            field_name=field_name,
            expected_type=expected_type,
            valid_options=valid_options,
            )
    
    xǁParseErrorǁ__init____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁParseErrorǁ__init____mutmut_1': xǁParseErrorǁ__init____mutmut_1, 
        'xǁParseErrorǁ__init____mutmut_2': xǁParseErrorǁ__init____mutmut_2, 
        'xǁParseErrorǁ__init____mutmut_3': xǁParseErrorǁ__init____mutmut_3, 
        'xǁParseErrorǁ__init____mutmut_4': xǁParseErrorǁ__init____mutmut_4, 
        'xǁParseErrorǁ__init____mutmut_5': xǁParseErrorǁ__init____mutmut_5, 
        'xǁParseErrorǁ__init____mutmut_6': xǁParseErrorǁ__init____mutmut_6, 
        'xǁParseErrorǁ__init____mutmut_7': xǁParseErrorǁ__init____mutmut_7, 
        'xǁParseErrorǁ__init____mutmut_8': xǁParseErrorǁ__init____mutmut_8, 
        'xǁParseErrorǁ__init____mutmut_9': xǁParseErrorǁ__init____mutmut_9, 
        'xǁParseErrorǁ__init____mutmut_10': xǁParseErrorǁ__init____mutmut_10, 
        'xǁParseErrorǁ__init____mutmut_11': xǁParseErrorǁ__init____mutmut_11
    }
    
    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁParseErrorǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁParseErrorǁ__init____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __init__.__signature__ = _mutmut_signature(xǁParseErrorǁ__init____mutmut_orig)
    xǁParseErrorǁ__init____mutmut_orig.__name__ = 'xǁParseErrorǁ__init__'

    def xǁParseErrorǁ_default_code__mutmut_orig(self) -> str:
        return "PARSE_ERROR"

    def xǁParseErrorǁ_default_code__mutmut_1(self) -> str:
        return "XXPARSE_ERRORXX"

    def xǁParseErrorǁ_default_code__mutmut_2(self) -> str:
        return "parse_error"
    
    xǁParseErrorǁ_default_code__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁParseErrorǁ_default_code__mutmut_1': xǁParseErrorǁ_default_code__mutmut_1, 
        'xǁParseErrorǁ_default_code__mutmut_2': xǁParseErrorǁ_default_code__mutmut_2
    }
    
    def _default_code(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁParseErrorǁ_default_code__mutmut_orig"), object.__getattribute__(self, "xǁParseErrorǁ_default_code__mutmut_mutants"), args, kwargs, self)
        return result 
    
    _default_code.__signature__ = _mutmut_signature(xǁParseErrorǁ_default_code__mutmut_orig)
    xǁParseErrorǁ_default_code__mutmut_orig.__name__ = 'xǁParseErrorǁ_default_code'


class ValidationError(ConfigError):
    """Configuration value validation failed."""

    def xǁValidationErrorǁ__init____mutmut_orig(
        self,
        message: str,
        *,
        value: Any,
        field_name: str,
        constraint: str | None = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(
            message,
            value=value,
            field_name=field_name,
            constraint=constraint,
            **kwargs,
        )

    def xǁValidationErrorǁ__init____mutmut_1(
        self,
        message: str,
        *,
        value: Any,
        field_name: str,
        constraint: str | None = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(
            None,
            value=value,
            field_name=field_name,
            constraint=constraint,
            **kwargs,
        )

    def xǁValidationErrorǁ__init____mutmut_2(
        self,
        message: str,
        *,
        value: Any,
        field_name: str,
        constraint: str | None = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(
            message,
            value=None,
            field_name=field_name,
            constraint=constraint,
            **kwargs,
        )

    def xǁValidationErrorǁ__init____mutmut_3(
        self,
        message: str,
        *,
        value: Any,
        field_name: str,
        constraint: str | None = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(
            message,
            value=value,
            field_name=None,
            constraint=constraint,
            **kwargs,
        )

    def xǁValidationErrorǁ__init____mutmut_4(
        self,
        message: str,
        *,
        value: Any,
        field_name: str,
        constraint: str | None = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(
            message,
            value=value,
            field_name=field_name,
            constraint=None,
            **kwargs,
        )

    def xǁValidationErrorǁ__init____mutmut_5(
        self,
        message: str,
        *,
        value: Any,
        field_name: str,
        constraint: str | None = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(
            value=value,
            field_name=field_name,
            constraint=constraint,
            **kwargs,
        )

    def xǁValidationErrorǁ__init____mutmut_6(
        self,
        message: str,
        *,
        value: Any,
        field_name: str,
        constraint: str | None = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(
            message,
            field_name=field_name,
            constraint=constraint,
            **kwargs,
        )

    def xǁValidationErrorǁ__init____mutmut_7(
        self,
        message: str,
        *,
        value: Any,
        field_name: str,
        constraint: str | None = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(
            message,
            value=value,
            constraint=constraint,
            **kwargs,
        )

    def xǁValidationErrorǁ__init____mutmut_8(
        self,
        message: str,
        *,
        value: Any,
        field_name: str,
        constraint: str | None = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(
            message,
            value=value,
            field_name=field_name,
            **kwargs,
        )

    def xǁValidationErrorǁ__init____mutmut_9(
        self,
        message: str,
        *,
        value: Any,
        field_name: str,
        constraint: str | None = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(
            message,
            value=value,
            field_name=field_name,
            constraint=constraint,
            )
    
    xǁValidationErrorǁ__init____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁValidationErrorǁ__init____mutmut_1': xǁValidationErrorǁ__init____mutmut_1, 
        'xǁValidationErrorǁ__init____mutmut_2': xǁValidationErrorǁ__init____mutmut_2, 
        'xǁValidationErrorǁ__init____mutmut_3': xǁValidationErrorǁ__init____mutmut_3, 
        'xǁValidationErrorǁ__init____mutmut_4': xǁValidationErrorǁ__init____mutmut_4, 
        'xǁValidationErrorǁ__init____mutmut_5': xǁValidationErrorǁ__init____mutmut_5, 
        'xǁValidationErrorǁ__init____mutmut_6': xǁValidationErrorǁ__init____mutmut_6, 
        'xǁValidationErrorǁ__init____mutmut_7': xǁValidationErrorǁ__init____mutmut_7, 
        'xǁValidationErrorǁ__init____mutmut_8': xǁValidationErrorǁ__init____mutmut_8, 
        'xǁValidationErrorǁ__init____mutmut_9': xǁValidationErrorǁ__init____mutmut_9
    }
    
    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁValidationErrorǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁValidationErrorǁ__init____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __init__.__signature__ = _mutmut_signature(xǁValidationErrorǁ__init____mutmut_orig)
    xǁValidationErrorǁ__init____mutmut_orig.__name__ = 'xǁValidationErrorǁ__init__'

    def xǁValidationErrorǁ_default_code__mutmut_orig(self) -> str:
        return "VALIDATION_ERROR"

    def xǁValidationErrorǁ_default_code__mutmut_1(self) -> str:
        return "XXVALIDATION_ERRORXX"

    def xǁValidationErrorǁ_default_code__mutmut_2(self) -> str:
        return "validation_error"
    
    xǁValidationErrorǁ_default_code__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁValidationErrorǁ_default_code__mutmut_1': xǁValidationErrorǁ_default_code__mutmut_1, 
        'xǁValidationErrorǁ_default_code__mutmut_2': xǁValidationErrorǁ_default_code__mutmut_2
    }
    
    def _default_code(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁValidationErrorǁ_default_code__mutmut_orig"), object.__getattribute__(self, "xǁValidationErrorǁ_default_code__mutmut_mutants"), args, kwargs, self)
        return result 
    
    _default_code.__signature__ = _mutmut_signature(xǁValidationErrorǁ_default_code__mutmut_orig)
    xǁValidationErrorǁ_default_code__mutmut_orig.__name__ = 'xǁValidationErrorǁ_default_code'


# Standardized error message formatters


def x_format_invalid_value_error__mutmut_orig(
    field_name: str,
    value: Any,
    expected_type: str | None = None,
    valid_options: list[str] | None = None,
    additional_info: str | None = None,
) -> str:
    """Create a standardized invalid value error message.

    Args:
        field_name: Name of the field being parsed
        value: The invalid value
        expected_type: Expected type (e.g., "boolean", "float")
        valid_options: List of valid option strings
        additional_info: Additional context about the error

    Returns:
        Formatted error message

    Examples:
        >>> format_invalid_value_error("log_level", "INVALID", valid_options=["DEBUG", "INFO"])
        "Invalid log_level 'INVALID'. Valid options: DEBUG, INFO"

        >>> format_invalid_value_error("sample_rate", "abc", expected_type="float")
        "Invalid sample_rate 'abc'. Expected: float"

    """
    parts = [f"Invalid {field_name} '{value}'."]

    if valid_options:
        parts.append(f"Valid options: {', '.join(valid_options)}")
    elif expected_type:
        parts.append(f"Expected: {expected_type}")

    if additional_info:
        parts.append(additional_info)

    return " ".join(parts)


# Standardized error message formatters


def x_format_invalid_value_error__mutmut_1(
    field_name: str,
    value: Any,
    expected_type: str | None = None,
    valid_options: list[str] | None = None,
    additional_info: str | None = None,
) -> str:
    """Create a standardized invalid value error message.

    Args:
        field_name: Name of the field being parsed
        value: The invalid value
        expected_type: Expected type (e.g., "boolean", "float")
        valid_options: List of valid option strings
        additional_info: Additional context about the error

    Returns:
        Formatted error message

    Examples:
        >>> format_invalid_value_error("log_level", "INVALID", valid_options=["DEBUG", "INFO"])
        "Invalid log_level 'INVALID'. Valid options: DEBUG, INFO"

        >>> format_invalid_value_error("sample_rate", "abc", expected_type="float")
        "Invalid sample_rate 'abc'. Expected: float"

    """
    parts = None

    if valid_options:
        parts.append(f"Valid options: {', '.join(valid_options)}")
    elif expected_type:
        parts.append(f"Expected: {expected_type}")

    if additional_info:
        parts.append(additional_info)

    return " ".join(parts)


# Standardized error message formatters


def x_format_invalid_value_error__mutmut_2(
    field_name: str,
    value: Any,
    expected_type: str | None = None,
    valid_options: list[str] | None = None,
    additional_info: str | None = None,
) -> str:
    """Create a standardized invalid value error message.

    Args:
        field_name: Name of the field being parsed
        value: The invalid value
        expected_type: Expected type (e.g., "boolean", "float")
        valid_options: List of valid option strings
        additional_info: Additional context about the error

    Returns:
        Formatted error message

    Examples:
        >>> format_invalid_value_error("log_level", "INVALID", valid_options=["DEBUG", "INFO"])
        "Invalid log_level 'INVALID'. Valid options: DEBUG, INFO"

        >>> format_invalid_value_error("sample_rate", "abc", expected_type="float")
        "Invalid sample_rate 'abc'. Expected: float"

    """
    parts = [f"Invalid {field_name} '{value}'."]

    if valid_options:
        parts.append(None)
    elif expected_type:
        parts.append(f"Expected: {expected_type}")

    if additional_info:
        parts.append(additional_info)

    return " ".join(parts)


# Standardized error message formatters


def x_format_invalid_value_error__mutmut_3(
    field_name: str,
    value: Any,
    expected_type: str | None = None,
    valid_options: list[str] | None = None,
    additional_info: str | None = None,
) -> str:
    """Create a standardized invalid value error message.

    Args:
        field_name: Name of the field being parsed
        value: The invalid value
        expected_type: Expected type (e.g., "boolean", "float")
        valid_options: List of valid option strings
        additional_info: Additional context about the error

    Returns:
        Formatted error message

    Examples:
        >>> format_invalid_value_error("log_level", "INVALID", valid_options=["DEBUG", "INFO"])
        "Invalid log_level 'INVALID'. Valid options: DEBUG, INFO"

        >>> format_invalid_value_error("sample_rate", "abc", expected_type="float")
        "Invalid sample_rate 'abc'. Expected: float"

    """
    parts = [f"Invalid {field_name} '{value}'."]

    if valid_options:
        parts.append(f"Valid options: {', '.join(None)}")
    elif expected_type:
        parts.append(f"Expected: {expected_type}")

    if additional_info:
        parts.append(additional_info)

    return " ".join(parts)


# Standardized error message formatters


def x_format_invalid_value_error__mutmut_4(
    field_name: str,
    value: Any,
    expected_type: str | None = None,
    valid_options: list[str] | None = None,
    additional_info: str | None = None,
) -> str:
    """Create a standardized invalid value error message.

    Args:
        field_name: Name of the field being parsed
        value: The invalid value
        expected_type: Expected type (e.g., "boolean", "float")
        valid_options: List of valid option strings
        additional_info: Additional context about the error

    Returns:
        Formatted error message

    Examples:
        >>> format_invalid_value_error("log_level", "INVALID", valid_options=["DEBUG", "INFO"])
        "Invalid log_level 'INVALID'. Valid options: DEBUG, INFO"

        >>> format_invalid_value_error("sample_rate", "abc", expected_type="float")
        "Invalid sample_rate 'abc'. Expected: float"

    """
    parts = [f"Invalid {field_name} '{value}'."]

    if valid_options:
        parts.append(f"Valid options: {'XX, XX'.join(valid_options)}")
    elif expected_type:
        parts.append(f"Expected: {expected_type}")

    if additional_info:
        parts.append(additional_info)

    return " ".join(parts)


# Standardized error message formatters


def x_format_invalid_value_error__mutmut_5(
    field_name: str,
    value: Any,
    expected_type: str | None = None,
    valid_options: list[str] | None = None,
    additional_info: str | None = None,
) -> str:
    """Create a standardized invalid value error message.

    Args:
        field_name: Name of the field being parsed
        value: The invalid value
        expected_type: Expected type (e.g., "boolean", "float")
        valid_options: List of valid option strings
        additional_info: Additional context about the error

    Returns:
        Formatted error message

    Examples:
        >>> format_invalid_value_error("log_level", "INVALID", valid_options=["DEBUG", "INFO"])
        "Invalid log_level 'INVALID'. Valid options: DEBUG, INFO"

        >>> format_invalid_value_error("sample_rate", "abc", expected_type="float")
        "Invalid sample_rate 'abc'. Expected: float"

    """
    parts = [f"Invalid {field_name} '{value}'."]

    if valid_options:
        parts.append(f"Valid options: {', '.join(valid_options)}")
    elif expected_type:
        parts.append(None)

    if additional_info:
        parts.append(additional_info)

    return " ".join(parts)


# Standardized error message formatters


def x_format_invalid_value_error__mutmut_6(
    field_name: str,
    value: Any,
    expected_type: str | None = None,
    valid_options: list[str] | None = None,
    additional_info: str | None = None,
) -> str:
    """Create a standardized invalid value error message.

    Args:
        field_name: Name of the field being parsed
        value: The invalid value
        expected_type: Expected type (e.g., "boolean", "float")
        valid_options: List of valid option strings
        additional_info: Additional context about the error

    Returns:
        Formatted error message

    Examples:
        >>> format_invalid_value_error("log_level", "INVALID", valid_options=["DEBUG", "INFO"])
        "Invalid log_level 'INVALID'. Valid options: DEBUG, INFO"

        >>> format_invalid_value_error("sample_rate", "abc", expected_type="float")
        "Invalid sample_rate 'abc'. Expected: float"

    """
    parts = [f"Invalid {field_name} '{value}'."]

    if valid_options:
        parts.append(f"Valid options: {', '.join(valid_options)}")
    elif expected_type:
        parts.append(f"Expected: {expected_type}")

    if additional_info:
        parts.append(None)

    return " ".join(parts)


# Standardized error message formatters


def x_format_invalid_value_error__mutmut_7(
    field_name: str,
    value: Any,
    expected_type: str | None = None,
    valid_options: list[str] | None = None,
    additional_info: str | None = None,
) -> str:
    """Create a standardized invalid value error message.

    Args:
        field_name: Name of the field being parsed
        value: The invalid value
        expected_type: Expected type (e.g., "boolean", "float")
        valid_options: List of valid option strings
        additional_info: Additional context about the error

    Returns:
        Formatted error message

    Examples:
        >>> format_invalid_value_error("log_level", "INVALID", valid_options=["DEBUG", "INFO"])
        "Invalid log_level 'INVALID'. Valid options: DEBUG, INFO"

        >>> format_invalid_value_error("sample_rate", "abc", expected_type="float")
        "Invalid sample_rate 'abc'. Expected: float"

    """
    parts = [f"Invalid {field_name} '{value}'."]

    if valid_options:
        parts.append(f"Valid options: {', '.join(valid_options)}")
    elif expected_type:
        parts.append(f"Expected: {expected_type}")

    if additional_info:
        parts.append(additional_info)

    return " ".join(None)


# Standardized error message formatters


def x_format_invalid_value_error__mutmut_8(
    field_name: str,
    value: Any,
    expected_type: str | None = None,
    valid_options: list[str] | None = None,
    additional_info: str | None = None,
) -> str:
    """Create a standardized invalid value error message.

    Args:
        field_name: Name of the field being parsed
        value: The invalid value
        expected_type: Expected type (e.g., "boolean", "float")
        valid_options: List of valid option strings
        additional_info: Additional context about the error

    Returns:
        Formatted error message

    Examples:
        >>> format_invalid_value_error("log_level", "INVALID", valid_options=["DEBUG", "INFO"])
        "Invalid log_level 'INVALID'. Valid options: DEBUG, INFO"

        >>> format_invalid_value_error("sample_rate", "abc", expected_type="float")
        "Invalid sample_rate 'abc'. Expected: float"

    """
    parts = [f"Invalid {field_name} '{value}'."]

    if valid_options:
        parts.append(f"Valid options: {', '.join(valid_options)}")
    elif expected_type:
        parts.append(f"Expected: {expected_type}")

    if additional_info:
        parts.append(additional_info)

    return "XX XX".join(parts)

x_format_invalid_value_error__mutmut_mutants : ClassVar[MutantDict] = {
'x_format_invalid_value_error__mutmut_1': x_format_invalid_value_error__mutmut_1, 
    'x_format_invalid_value_error__mutmut_2': x_format_invalid_value_error__mutmut_2, 
    'x_format_invalid_value_error__mutmut_3': x_format_invalid_value_error__mutmut_3, 
    'x_format_invalid_value_error__mutmut_4': x_format_invalid_value_error__mutmut_4, 
    'x_format_invalid_value_error__mutmut_5': x_format_invalid_value_error__mutmut_5, 
    'x_format_invalid_value_error__mutmut_6': x_format_invalid_value_error__mutmut_6, 
    'x_format_invalid_value_error__mutmut_7': x_format_invalid_value_error__mutmut_7, 
    'x_format_invalid_value_error__mutmut_8': x_format_invalid_value_error__mutmut_8
}

def format_invalid_value_error(*args, **kwargs):
    result = _mutmut_trampoline(x_format_invalid_value_error__mutmut_orig, x_format_invalid_value_error__mutmut_mutants, args, kwargs)
    return result 

format_invalid_value_error.__signature__ = _mutmut_signature(x_format_invalid_value_error__mutmut_orig)
x_format_invalid_value_error__mutmut_orig.__name__ = 'x_format_invalid_value_error'


def x_format_validation_error__mutmut_orig(
    field_name: str,
    value: Any,
    constraint: str,
    additional_info: str | None = None,
) -> str:
    """Create a standardized validation error message.

    Args:
        field_name: Name of the field being validated
        value: The invalid value
        constraint: Description of the constraint that failed
        additional_info: Additional context

    Returns:
        Formatted error message

    Examples:
        >>> format_validation_error("port", 0, "must be between 1 and 65535")
        "Value 0 for port must be between 1 and 65535"

        >>> format_validation_error("sample_rate", 1.5, "must be between 0.0 and 1.0")
        "Value 1.5 for sample_rate must be between 0.0 and 1.0"

    """
    parts = [f"Value {value} for {field_name} {constraint}"]

    if additional_info:
        parts.append(f"({additional_info})")

    return "".join(parts)


def x_format_validation_error__mutmut_1(
    field_name: str,
    value: Any,
    constraint: str,
    additional_info: str | None = None,
) -> str:
    """Create a standardized validation error message.

    Args:
        field_name: Name of the field being validated
        value: The invalid value
        constraint: Description of the constraint that failed
        additional_info: Additional context

    Returns:
        Formatted error message

    Examples:
        >>> format_validation_error("port", 0, "must be between 1 and 65535")
        "Value 0 for port must be between 1 and 65535"

        >>> format_validation_error("sample_rate", 1.5, "must be between 0.0 and 1.0")
        "Value 1.5 for sample_rate must be between 0.0 and 1.0"

    """
    parts = None

    if additional_info:
        parts.append(f"({additional_info})")

    return "".join(parts)


def x_format_validation_error__mutmut_2(
    field_name: str,
    value: Any,
    constraint: str,
    additional_info: str | None = None,
) -> str:
    """Create a standardized validation error message.

    Args:
        field_name: Name of the field being validated
        value: The invalid value
        constraint: Description of the constraint that failed
        additional_info: Additional context

    Returns:
        Formatted error message

    Examples:
        >>> format_validation_error("port", 0, "must be between 1 and 65535")
        "Value 0 for port must be between 1 and 65535"

        >>> format_validation_error("sample_rate", 1.5, "must be between 0.0 and 1.0")
        "Value 1.5 for sample_rate must be between 0.0 and 1.0"

    """
    parts = [f"Value {value} for {field_name} {constraint}"]

    if additional_info:
        parts.append(None)

    return "".join(parts)


def x_format_validation_error__mutmut_3(
    field_name: str,
    value: Any,
    constraint: str,
    additional_info: str | None = None,
) -> str:
    """Create a standardized validation error message.

    Args:
        field_name: Name of the field being validated
        value: The invalid value
        constraint: Description of the constraint that failed
        additional_info: Additional context

    Returns:
        Formatted error message

    Examples:
        >>> format_validation_error("port", 0, "must be between 1 and 65535")
        "Value 0 for port must be between 1 and 65535"

        >>> format_validation_error("sample_rate", 1.5, "must be between 0.0 and 1.0")
        "Value 1.5 for sample_rate must be between 0.0 and 1.0"

    """
    parts = [f"Value {value} for {field_name} {constraint}"]

    if additional_info:
        parts.append(f"({additional_info})")

    return "".join(None)


def x_format_validation_error__mutmut_4(
    field_name: str,
    value: Any,
    constraint: str,
    additional_info: str | None = None,
) -> str:
    """Create a standardized validation error message.

    Args:
        field_name: Name of the field being validated
        value: The invalid value
        constraint: Description of the constraint that failed
        additional_info: Additional context

    Returns:
        Formatted error message

    Examples:
        >>> format_validation_error("port", 0, "must be between 1 and 65535")
        "Value 0 for port must be between 1 and 65535"

        >>> format_validation_error("sample_rate", 1.5, "must be between 0.0 and 1.0")
        "Value 1.5 for sample_rate must be between 0.0 and 1.0"

    """
    parts = [f"Value {value} for {field_name} {constraint}"]

    if additional_info:
        parts.append(f"({additional_info})")

    return "XXXX".join(parts)

x_format_validation_error__mutmut_mutants : ClassVar[MutantDict] = {
'x_format_validation_error__mutmut_1': x_format_validation_error__mutmut_1, 
    'x_format_validation_error__mutmut_2': x_format_validation_error__mutmut_2, 
    'x_format_validation_error__mutmut_3': x_format_validation_error__mutmut_3, 
    'x_format_validation_error__mutmut_4': x_format_validation_error__mutmut_4
}

def format_validation_error(*args, **kwargs):
    result = _mutmut_trampoline(x_format_validation_error__mutmut_orig, x_format_validation_error__mutmut_mutants, args, kwargs)
    return result 

format_validation_error.__signature__ = _mutmut_signature(x_format_validation_error__mutmut_orig)
x_format_validation_error__mutmut_orig.__name__ = 'x_format_validation_error'


__all__ = [
    "ConfigError",
    "ParseError",
    "ValidationError",
    "format_invalid_value_error",
    "format_validation_error",
]


# <3 🧱🤝⚙️🪄
